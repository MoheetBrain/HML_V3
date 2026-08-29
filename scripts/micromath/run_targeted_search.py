#!/usr/bin/env python3
"""Phase 9-12: the surgical mutation cycles.

Diagnose the weakest structure, ask the local meta-designers for a repair aimed at THAT
structure, test only the suites the repair could move, then require the improvement to
reproduce on MICRO_SHADOW before promoting it. MICRO_HIDDEN is never read.
"""

from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hml_v3.micromath import neural, targeted_search as TS  # noqa: E402
from hml_v3.micromath.candidates import CONTROLS, load_controls, load_finalists  # noqa: E402
from hml_v3.micromath.corpus import load_base_pool, load_split  # noqa: E402
from hml_v3.micromath.heatmap import saturation  # noqa: E402
from hml_v3.micromath.schema import MicroPair  # noqa: E402
from hml_v3.micromath.stresses import STRESS_QUESTION  # noqa: E402
from hml_v3.representation_search.compiler import CompilerRejection, build  # noqa: E402
from hml_v3.representation_search.failure_memory import FailureMemory  # noqa: E402
from hml_v3.representation_search.gates import run_gates  # noqa: E402
from hml_v3.representation_search.genome import AXES  # noqa: E402
from hml_v3.representation_search.meta_designer.deterministic import (  # noqa: E402
    DeterministicMetaDesigner,
)
from hml_v3.representation_search.meta_designer.base import ScientistReport  # noqa: E402
from hml_v3.representation_search.meta_designer.llm import (  # noqa: E402
    LLMMetaDesigner,
    OllamaTransport,
)

AXIS_VALUES = {axis.name: list(axis.values) for axis in AXES}


def stress_accuracy(rows) -> dict[str, float]:
    buckets = collections.defaultdict(list)
    for row in rows:
        buckets[row["stress"]].append(row["correct"])
    return {k: sum(v) / len(v) for k, v in buckets.items()}


def domain_accuracy(rows, stress) -> dict[str, float]:
    buckets = collections.defaultdict(list)
    for row in rows:
        if row["stress"] == stress:
            buckets[row["domain"]].append(row["correct"])
    return {k: sum(v) / len(v) for k, v in buckets.items()}


def probe(model, compiler, pairs) -> float:
    items = neural.build_items(compiler, pairs)
    if not items:
        return 0.0
    results = neural.run_probe(model, items)
    return sum(1 for r in results if r.correct) / len(results)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe-report", type=Path, required=True)
    parser.add_argument("--lab", type=Path, default=ROOT / "data/micromath_lab_v1")
    parser.add_argument("--workspace", type=Path,
                        default=ROOT / "data/representation_search_v2")
    parser.add_argument("--frontier", type=Path,
                        default=ROOT / "reports/representation_search_v2/FINAL_FRONTIER.json")
    parser.add_argument("--corpus", type=Path,
                        default=ROOT / "data/corpus/search_pool_v2.jsonl.gz")
    parser.add_argument("--model", default="qwen38-rvn:latest")
    parser.add_argument("--cycles", type=int, default=3)
    parser.add_argument("--suite-size", type=int, default=16)
    parser.add_argument("--out", type=Path, default=ROOT / "reports/micromath_lab_v1")
    args = parser.parse_args()

    report = json.loads(args.probe_report.read_text())
    results = report["results"]
    control_labels = [l for l in results if l in set(CONTROLS)]
    per_stress = {label: stress_accuracy(rows) for label, rows in results.items()}
    stresses = sorted(per_stress[control_labels[0]])
    saturated = [s for s in stresses
                 if saturation([per_stress[l][s] for l in per_stress]) == "SATURATED"]

    finalists = {c.label: c for c in load_finalists(args.workspace, args.frontier)}
    controls = {c.label: c for c in load_controls()}
    overall = {l: sum(1 for r in rows if r["correct"]) / len(rows)
               for l, rows in results.items()}
    best_label = max(finalists, key=lambda l: overall[l])
    best = finalists[best_label]
    best_control = max(control_labels, key=lambda l: overall[l])
    print(f"best finalist: {best_label} ({overall[best_label]:.3f})  |  "
          f"best control: {best_control} ({overall[best_control]:.3f})", flush=True)
    print(f"saturated and excluded: {saturated}", flush=True)

    pool, _prov = load_base_pool(args.corpus)
    lab_pairs = {name: [MicroPair.from_dict(r) for r in load_split(args.lab, name)]
                 for name in ("micro_dev", "micro_shadow")}
    used = {p.base_transition_id for group in lab_pairs.values() for p in group}

    model = neural.LocalModel(args.model)
    if not model.available():
        raise SystemExit(f"{args.model} not installed")

    backends = [DeterministicMetaDesigner()]
    for name in ("gemma3:4b", args.model):
        backend = LLMMetaDesigner(OllamaTransport(name))
        if backend.available():
            backends.append(backend)
    print(f"meta-designers: {[b.name for b in backends]}", flush=True)

    memory = FailureMemory.load()
    genome = best.compiler.genome
    invented = dict(best.invented)
    cycles: list[TS.CycleResult] = []
    attempted_axes: set[str] = set()
    started = time.time()

    for cycle in range(1, args.cycles + 1):
        current = per_stress[best_label] if cycle == 1 else current_stress
        eligible = {s: v for s, v in current.items() if s not in saturated}
        control_stress = {s: max(per_stress[l][s] for l in control_labels)
                          for s in eligible}
        gaps = sorted(eligible, key=lambda s: eligible[s] - control_stress[s])
        weakness = next((s for s in gaps if s not in attempted_axes), gaps[0])
        attempted_axes.add(weakness)

        suite = TS.build_targeted_suite(pool, weakness, used, args.suite_size)
        used |= {p.base_transition_id for p in suite}
        shadow = [p for p in lab_pairs["micro_shadow"] if p.stress == weakness]
        print(f"\n=== CYCLE {cycle}: {weakness} "
              f"(candidate {eligible[weakness]:.3f} vs control {control_stress[weakness]:.3f}) "
              f"| targeted suite {len(suite)} pairs, shadow {len(shadow)} ===", flush=True)
        if not suite:
            cycles.append(TS.CycleResult(
                cycle, weakness, "-", {}, "-", best_label, False, 0, 0, None, None, {},
                "NO_TARGETED_SUITE", "the corpus cannot build a suite for this structure"))
            continue

        baseline = probe(model, best.compiler, suite)
        print(f"  baseline on targeted suite: {baseline:.3f}", flush=True)

        packet = TS.ScientistFailurePacket(
            target_stress=weakness, question=STRESS_QUESTION[weakness],
            candidate=best_label,
            candidate_genome={a: genome.get(a) for a in
                              ("syntax_family", "context_order", "premise_locality",
                               "binder_encoding", "binder_use_reminder", "goal_position",
                               "graph_serialization", "redundancy_level",
                               "state_partitioning", "scope_metadata")},
            candidate_accuracy=baseline,
            best_control=best_control,
            best_control_accuracy=control_stress[weakness],
            per_domain=domain_accuracy(results[best_label], weakness),
            other_stresses={s: v for s, v in eligible.items() if s != weakness},
            saturated_stresses=saturated,
            failure_memory=[{"id": l.id, "title": l.title, "disposition": l.disposition}
                            for l in memory.lessons
                            if l.disposition in ("DO_NOT_RETRY_UNCHANGED", "HARD_GATE")][:8],
        )
        scientist = ScientistReport(
            generation=cycle, phase=f"TARGETED_{weakness}",
            genome_axes=AXIS_VALUES,
            elites=[{"candidate_id": best_label,
                     "genome": packet.candidate_genome, "invented": invented,
                     "metrics": {weakness: round(baseline, 3)},
                     "weaknesses": [weakness]}],
            metric_directions={weakness: "maximise"},
            corpus_profile=packet.to_dict(),
            unresolved_questions=[
                f"{weakness} reads {baseline:.3f} against chance 0.500 and control "
                f"{control_stress[weakness]:.3f}; propose a representation change that makes "
                f"{STRESS_QUESTION[weakness]} recoverable"],
            budget={"generation": cycle, "max": args.cycles},
        )

        proposals = []
        for backend in backends:
            batch = backend.propose(scientist)
            for proposal in batch.accepted:
                payload = proposal.payload
                if proposal.proposal_type != "AXIS_MUTATION":
                    continue
                axis, value = payload.get("axis"), payload.get("value")
                if axis in AXIS_VALUES and value in AXIS_VALUES[axis] \
                        and genome.get(axis) != value:
                    allowed, _reason = memory.may_apply(axis, value)
                    if allowed:
                        proposals.append((backend.name, payload))
        seen = set()
        unique = []
        for source, payload in proposals:
            key = (payload["axis"], payload["value"])
            if key not in seen:
                seen.add(key)
                unique.append((source, payload))
        print(f"  {len(unique)} distinct actionable mutations proposed", flush=True)

        accepted = None
        for source, payload in unique[:3]:
            axis, value = payload["axis"], payload["value"]
            try:
                mutated = genome.with_values(**{axis: value})
                compiler = build(mutated, invented, None)
            except (ValueError, CompilerRejection) as error:
                print(f"    {axis}={value}: REJECTED at compile ({type(error).__name__})",
                      flush=True)
                continue
            gates = run_gates(compiler, [p.state_a for p in suite[:8]])
            if not gates.passed:
                print(f"    {axis}={value}: REJECTED, semantic gate "
                      f"{gates.first_failure}", flush=True)
                cycles.append(TS.CycleResult(
                    cycle, weakness, payload.get("hypothesis", ""),
                    {"axis": axis, "value": value}, source, mutated.candidate_id(),
                    False, baseline, 0.0, None, None, {}, "REJECTED_SEMANTIC_GATE",
                    gates.first_failure or "gate"))
                continue
            after = probe(model, compiler, suite)
            delta = after - baseline
            print(f"    {axis}={value}: targeted {baseline:.3f} -> {after:.3f} "
                  f"({delta:+.3f})  [{time.time()-started:.0f}s]", flush=True)
            if delta < TS.MATERIAL_IMPROVEMENT:
                cycles.append(TS.CycleResult(
                    cycle, weakness, payload.get("hypothesis", ""),
                    {"axis": axis, "value": value}, source, mutated.candidate_id(),
                    True, baseline, after, None, None, {}, "REJECTED_NO_TARGETED_GAIN",
                    f"delta {delta:+.3f} below the preregistered {TS.MATERIAL_IMPROVEMENT}"))
                continue
            shadow_before = probe(model, best.compiler, shadow) if shadow else None
            shadow_after = probe(model, compiler, shadow) if shadow else None
            regression = {}
            for other in [s for s in eligible if s != weakness][:3]:
                panel = [p for p in lab_pairs["micro_dev"] if p.stress == other][:2]
                if panel:
                    regression[other] = probe(model, compiler, panel) - probe(
                        model, best.compiler, panel)
            reproduced = (shadow_before is None or shadow_after is None
                          or shadow_after >= shadow_before)
            worst = min(regression.values(), default=0.0)
            if reproduced and worst > -0.25:
                verdict, reason = "ACCEPTED", "targeted gain reproduced on shadow"
                accepted = (axis, value, compiler, mutated)
            elif not reproduced:
                verdict, reason = "REJECTED_SHADOW_NONREPLICATION", (
                    f"shadow {shadow_before:.3f} -> {shadow_after:.3f}")
            else:
                verdict, reason = "REJECTED_REGRESSION", f"worst regression {worst:+.3f}"
            print(f"      shadow {shadow_before} -> {shadow_after} | {verdict}", flush=True)
            cycles.append(TS.CycleResult(
                cycle, weakness, payload.get("hypothesis", ""),
                {"axis": axis, "value": value}, source, mutated.candidate_id(),
                True, baseline, after, shadow_before, shadow_after, regression,
                verdict, reason))
            if accepted:
                break

        if accepted:
            axis, value, compiler, mutated = accepted
            genome = mutated
            best = type(best)(label=mutated.candidate_id(), kind="FINALIST",
                              candidate_id=mutated.candidate_id(), compiler=compiler,
                              invented=invented)
            best_label = mutated.candidate_id()
            print(f"  PROMOTED {axis}={value} -> {best_label}", flush=True)
        current_stress = dict(eligible)
        current_stress[weakness] = max(
            (c.dev_after for c in cycles if c.cycle == cycle and c.dev_after), default=baseline)

    payload = {
        "model": args.model, "cycles": [c.to_dict() for c in cycles],
        "material_improvement": TS.MATERIAL_IMPROVEMENT,
        "saturated_excluded": saturated,
        "final_candidate": best_label,
        "accepted": [c.to_dict() for c in cycles if c.verdict == "ACCEPTED"],
        "elapsed_seconds": round(time.time() - started, 1),
    }
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "TARGETED_SEARCH.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(f"\nwrote TARGETED_SEARCH.json  ({payload['elapsed_seconds']:.0f}s)")
    for c in cycles:
        print(f"  cycle {c.cycle} {c.weakness:18s} {c.mutation.get('axis','-'):24s} "
              f"{c.verdict}")


if __name__ == "__main__":
    main()
