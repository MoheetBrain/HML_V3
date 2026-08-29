#!/usr/bin/env python
"""Evaluate architectural hypotheses on the two components whose instruments work.

`MISSION §13`, `§14`, `§17`. The seven V1 mutations were cosmetic and moved a combined 0.031
on valid instruments, so surface syntax is refuted as a lever. These proposals change what
structure is *exposed*, and each carries a stated causal hypothesis and a falsifier.

The funnel kills early (`§17`):

    Level 0  the compiler builds
    Level 2  behavioural novelty -- a rendering identical to something already queued is
             dropped without inference, because evaluating it could not distinguish them
    Level 4  the target component on MICRO_DEV_V2, at the first ladder rung
    Level 5  escalate only what looks promising
    Level 7  cross-component regression on the other valid instrument

    .venv/bin/python scripts/micromath/run_architectures_v2.py
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

from hml_v3.micromath import architectures as A  # noqa: E402
from hml_v3.micromath import calibration_v2 as C  # noqa: E402
from hml_v3.micromath import instruments_v2 as IV2  # noqa: E402
from hml_v3.micromath import probe_v2 as P  # noqa: E402
from hml_v3.micromath import stresses as S  # noqa: E402
from hml_v3.micromath.candidates import load_controls, load_finalists  # noqa: E402
from hml_v3.micromath.corpus import load_split  # noqa: E402
from hml_v3.representation_search.lineage import CandidateRegistry  # noqa: E402

#: Level 4 sample. Small on purpose: an architecture that does nothing should cost 12 items.
SCREEN = 12
#: Level 5 sample, spent only on a proposal that cleared the screen.
CONFIRM = 32
#: A screen result must beat the candidate by at least this to earn confirmation.
PROMISING = 0.08


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lab", type=Path, default=ROOT / "data/micromath_lab_v2")
    parser.add_argument("--workspace", type=Path, default=ROOT / "data/representation_search_v2")
    parser.add_argument("--frontier", type=Path,
                        default=ROOT / "reports/representation_search_v2/FINAL_FRONTIER.json")
    parser.add_argument("--candidate", default="R_015b8cd926da")
    parser.add_argument("--control", default="TYPED_AST")
    parser.add_argument("--model", default="qwen38-rvn:latest")
    parser.add_argument("--out", type=Path, default=ROOT / "reports/micromath_lab_v2")
    args = parser.parse_args()

    items = [IV2.MicroItem.from_dict(r) for r in load_split(args.lab, "micro_dev_v2")]
    by_stress: dict[str, list] = collections.defaultdict(list)
    for item in items:
        by_stress[item.stress].append(item)
    for stress in by_stress:
        by_stress[stress].sort(key=lambda i: i.item_id)

    controls = {c.label: c for c in load_controls()}
    finalists = {c.label: c for c in load_finalists(args.workspace, args.frontier)}
    candidate = finalists[args.candidate]
    registry = CandidateRegistry(args.workspace / "candidate_registry.jsonl")
    record = registry.get(args.candidate)
    base_genome = record.genome if record is not None else None

    started = time.time()
    results: list[dict] = []
    args.out.mkdir(parents=True, exist_ok=True)

    for stress, proposals in A.ARCHITECTURES.items():
        suite = by_stress.get(stress, [])
        if not suite:
            print(f"{stress}: no dev items, skipped", flush=True)
            continue
        other = S.EXPRESSION_DEPTH if stress == S.MULTI_GOAL else S.MULTI_GOAL
        chance = sum(i.chance for i in suite[:SCREEN]) / len(suite[:SCREEN])
        print(f"\n=== {stress} — {len(proposals)} architectures "
              f"({len(suite)} items, chance {chance:.3f}) ===", flush=True)

        # Baselines, measured once and shared by every proposal in this component.
        seen: dict[str, str] = {}
        baselines = {}
        for label, compiler in ((args.candidate, candidate.compiler),
                                (args.control, controls[args.control].compiler)):
            digest = A.behavioural_digest(compiler, suite)
            seen[digest] = label
            probes = P.build_probes(compiler, suite[:SCREEN], label)
            successes, trials, _ = P.run(args.model, probes)
            baselines[label] = successes / trials if trials else 0.0
            print(f"  baseline {label:<24}{successes}/{trials} = {baselines[label]:.3f} "
                  f"({time.time() - started:.0f}s)", flush=True)
        floor = max(baselines.values())

        for architecture in proposals:
            entry: dict = {"stress": stress, **architecture.to_dict()}
            try:
                compiler, applied, dropped = A.realise(architecture, base=base_genome)
            except Exception as error:  # noqa: BLE001
                entry.update(level="LEVEL_0_COMPILE", verdict="REJECTED_DOES_NOT_BUILD",
                             detail=str(error)[:200])
                results.append(entry)
                print(f"  {architecture.label:<30} REJECTED_DOES_NOT_BUILD", flush=True)
                continue
            entry["applied_axes"] = applied
            entry["dropped_axes"] = dropped

            digest = A.behavioural_digest(compiler, suite)
            if digest in seen:
                entry.update(level="LEVEL_2_NOVELTY",
                             verdict="REJECTED_BEHAVIOURAL_DUPLICATE",
                             duplicate_of=seen[digest])
                results.append(entry)
                print(f"  {architecture.label:<30} REJECTED_BEHAVIOURAL_DUPLICATE "
                      f"(renders identically to {seen[digest]})", flush=True)
                continue
            seen[digest] = architecture.label

            probes = P.build_probes(compiler, suite[:SCREEN], architecture.label)
            if not probes:
                entry.update(level="LEVEL_2_NOVELTY", verdict="REJECTED_UNRENDERABLE")
                results.append(entry)
                print(f"  {architecture.label:<30} REJECTED_UNRENDERABLE", flush=True)
                continue
            successes, trials, _ = P.run(args.model, probes)
            screen = successes / trials if trials else 0.0
            entry.update(level="LEVEL_4_SCREEN", screen=round(screen, 4),
                         screen_items=trials, delta_vs_candidate=round(
                             screen - baselines[args.candidate], 4))
            print(f"  {architecture.label:<30} screen {successes}/{trials} = {screen:.3f}  "
                  f"(cand {baselines[args.candidate]:.3f}, best {floor:.3f})", flush=True)

            if screen - baselines[args.candidate] < PROMISING:
                entry["verdict"] = "REJECTED_NO_TARGETED_GAIN"
                results.append(entry)
                continue

            # Level 5: confirm on a larger sample before believing a 12-item difference.
            probes = P.build_probes(compiler, suite[:CONFIRM], architecture.label)
            successes, trials, outcomes = P.run(args.model, probes)
            confirm = successes / trials if trials else 0.0
            base_probes = P.build_probes(candidate.compiler, suite[:CONFIRM], args.candidate)
            base_successes, base_trials, base_outcomes = P.run(args.model, base_probes)
            shared = sorted({o.probe.item_id for o in outcomes}
                            & {o.probe.item_id for o in base_outcomes})
            left = {o.probe.item_id: o.correct for o in outcomes}
            right = {o.probe.item_id: o.correct for o in base_outcomes}
            status, reason = C.compare([left[i] for i in shared], [right[i] for i in shared])
            entry.update(level="LEVEL_5_CONFIRM", confirm=round(confirm, 4),
                         confirm_items=trials,
                         candidate_on_same_items=round(
                             base_successes / base_trials if base_trials else 0.0, 4),
                         paired=status, paired_reason=reason)
            print(f"    confirm {successes}/{trials} = {confirm:.3f} vs candidate "
                  f"{base_successes}/{base_trials}; {status}: {reason}", flush=True)

            # Level 7: cross-component regression on the other valid instrument.
            regression_suite = by_stress.get(other, [])[:SCREEN]
            if regression_suite:
                probes = P.build_probes(compiler, regression_suite, architecture.label)
                r_successes, r_trials, _ = P.run(args.model, probes)
                base = P.build_probes(candidate.compiler, regression_suite, args.candidate)
                b_successes, b_trials, _ = P.run(args.model, base)
                delta = ((r_successes / r_trials if r_trials else 0.0)
                         - (b_successes / b_trials if b_trials else 0.0))
                entry["regression"] = {other: round(delta, 4)}
                print(f"    regression on {other}: {delta:+.3f}", flush=True)
                if delta < -PROMISING:
                    entry["verdict"] = "REJECTED_CROSS_COMPONENT_REGRESSION"
                    results.append(entry)
                    continue

            entry["verdict"] = ("ACCEPTED_PROMISING" if status == C.ADVANTAGE
                                else "HELD_NOT_SEPARATED_FROM_CANDIDATE")
            results.append(entry)

        (args.out / "ARCHITECTURES_V2.json").write_text(json.dumps({
            "model": args.model, "candidate": args.candidate, "control": args.control,
            "lab": IV2.LAB_VERSION, "screen_items": SCREEN, "confirm_items": CONFIRM,
            "promising_threshold": PROMISING,
            "elapsed_seconds": round(time.time() - started, 1),
            "results": results}, indent=2, sort_keys=True) + "\n")

    print(f"\n=== ARCHITECTURES ({time.time() - started:.0f}s) ===")
    for entry in results:
        print(f"  {entry['stress']:<18}{entry['label']:<30}{entry.get('verdict', '?')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
