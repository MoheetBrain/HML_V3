#!/usr/bin/env python3
"""Turn a completed search workspace into the committed frontier report.

Reads only ``data/representation_search/`` — the candidate registry, the per-generation
checkpoints, the split manifest and, if it exists, the single sealed evaluation. Writes
``reports/representation_search/PRETRAINING_FRONTIER_V1.{md,json}``.

The report states what was measured and what was not. It never claims optimality.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hml_v3.representation_search.compiler import (  # noqa: E402
    CANONICAL_STATE_VERSION,
    COMPILER_VERSION,
    build,
)
from hml_v3.representation_search.genome import AXES, space_size  # noqa: E402
from hml_v3.representation_search.lineage import CandidateRegistry  # noqa: E402
from hml_v3.representation_search.metrics import MAXIMISED, PARETO_AXES  # noqa: E402
from hml_v3.representation_search.pareto import (  # noqa: E402
    epsilon_pareto_front,
    equivalence_classes,
    metric_signature,
    non_dominated_sort,
    shortlist,
)
from hml_v3.representation_search.seeds import SEEDS  # noqa: E402

WORKSPACE = ROOT / "data/representation_search"
OUT_DIR = ROOT / "reports/representation_search"


def label_for(record) -> str:
    for name, genome in SEEDS.items():
        if genome.candidate_id() == record.candidate_id:
            return name
    return record.candidate_id


def derivation(record, registry) -> tuple[str, list[str]]:
    """Which seed this candidate descends from, and how its genome differs from it."""

    ancestry = registry.ancestry(record.candidate_id)
    seed_ids = {genome.candidate_id(): name for name, genome in SEEDS.items()}
    for candidate_id in ancestry:
        if candidate_id in seed_ids:
            seed_genome = SEEDS[seed_ids[candidate_id]]
            differences = [
                f"{axis}={record.genome.get(axis)}"
                for axis in record.genome.differing_axes(seed_genome)
            ]
            return seed_ids[candidate_id], sorted(differences)
    return "unknown", []


def measured_effects(registry) -> list[dict]:
    """Aggregate every single-axis mutation into a per-transition effect size.

    One parent-child pair is an anecdote. The same axis transition applied to several
    different parents, agreeing in sign, is a mechanism. This aggregates all of them and
    reports the relative change in the axis's own target metric, so a reader can see which
    structural decisions actually cost or bought something on this corpus.
    """

    buckets: dict[tuple[str, str, str, str], list[float]] = {}
    for record in registry.accepted():
        if record.origin != "SINGLE_AXIS" or not record.parents or not record.hypothesis:
            continue
        parent = registry.get(record.parents[0])
        if parent is None or not parent.metrics or not record.metrics:
            continue
        axis = record.hypothesis.get("axis")
        metric = record.hypothesis.get("target_metric")
        if not axis or not metric:
            continue
        before = parent.metrics.get(metric)
        after = record.metrics.get(metric)
        if before is None or after is None or abs(before) < 1e-9:
            continue
        key = (axis, record.hypothesis.get("from_value"), record.hypothesis.get("to_value"),
               metric)
        buckets.setdefault(key, []).append((after - before) / abs(before))
    rows = []
    for (axis, from_value, to_value, metric), deltas in buckets.items():
        if len(deltas) < 2:
            continue
        mean = sum(deltas) / len(deltas)
        agree = sum(1 for delta in deltas if (delta > 0) == (mean > 0))
        rows.append({
            "axis": axis, "from": from_value, "to": to_value, "metric": metric,
            "observations": len(deltas),
            "mean_relative_change": round(mean, 4),
            "sign_agreement": round(agree / len(deltas), 3),
            "improves": (mean < 0) if metric not in MAXIMISED else (mean > 0),
        })
    return sorted(rows, key=lambda row: -abs(row["mean_relative_change"]))


def axis_effect_table(registry) -> list[dict]:
    """For each axis, how often a single-axis mutation changed the Pareto vector at all.

    An axis that never changes the measurement on this corpus is not a bad axis; it is an
    axis this corpus cannot speak to, and saying so is more useful than reporting a search
    that appears to have explored it.
    """

    attempts: dict[str, int] = {}
    effective: dict[str, int] = {}
    for record in registry.accepted():
        if record.origin != "SINGLE_AXIS" or not record.parents or not record.hypothesis:
            continue
        parent = registry.get(record.parents[0])
        if parent is None or not parent.metrics or not record.metrics:
            continue
        axis = record.hypothesis.get("axis")
        if not axis:
            continue
        attempts[axis] = attempts.get(axis, 0) + 1
        if metric_signature(record.metrics) != metric_signature(parent.metrics):
            effective[axis] = effective.get(axis, 0) + 1
    return sorted(
        (
            {
                "axis": axis,
                "single_axis_mutations": count,
                "changed_the_measurement": effective.get(axis, 0),
                "share": round(effective.get(axis, 0) / count, 3) if count else 0.0,
            }
            for axis, count in attempts.items()
        ),
        key=lambda row: (row["share"], row["axis"]),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=Path, default=WORKSPACE)
    parser.add_argument("--out-dir", type=Path, default=OUT_DIR)
    parser.add_argument("--corpus-audit", type=Path,
                        default=ROOT / "reports/audits/LEAN_RUNTIME_V2_CORPUS.json")
    args = parser.parse_args()

    registry = CandidateRegistry(args.workspace / "candidate_registry.jsonl")
    state = json.loads((args.workspace / "search_state.json").read_text())
    split = json.loads((args.workspace / "split_manifest.json").read_text())
    generations = sorted((args.workspace / "generations").glob("generation_*.json"))
    reports = [json.loads(path.read_text()) for path in generations]
    sealed_path = args.workspace / "sealed_final_evaluation.json"
    sealed = json.loads(sealed_path.read_text()) if sealed_path.exists() else None
    corpus_audit = (
        json.loads(args.corpus_audit.read_text()) if args.corpus_audit.exists() else {}
    )

    evaluated = registry.accepted()
    population = [(record.candidate_id, record.metrics or {}) for record in evaluated]
    fronts = non_dominated_sort(population)
    strict_front = fronts[0] if fronts else []
    # Strict non-dominated sorting over seven axes leaves most of a grown population on the
    # front. The shortlist is therefore the epsilon-front: candidates no other candidate
    # beats by more than 2% on every axis at once. Selection during the search used the
    # strict front, so this choice cannot have steered the search.
    epsilon = 0.02
    epsilon_front = epsilon_pareto_front(population, epsilon)
    classes = equivalence_classes(population)
    finalists, reasons = shortlist(population)
    front = finalists
    ranked = sorted(
        (registry.get(candidate_id) for candidate_id in finalists),
        key=lambda record: record.metrics.get("bpe_tokens_per_transition", 1e9),
    )
    seed_ids = {genome.candidate_id(): name for name, genome in SEEDS.items()}
    rank_by_tokens = sorted(
        evaluated, key=lambda record: record.metrics.get("bpe_tokens_per_transition", 1e9)
    )
    token_rank = {record.candidate_id: index + 1 for index, record in enumerate(rank_by_tokens)}

    payload = {
        "name": "PRETRAINING_REPRESENTATION_FRONTIER_V1",
        "claim_of_universal_optimality": False,
        "compiler_version": COMPILER_VERSION,
        "canonical_state_version": CANONICAL_STATE_VERSION,
        "genome_axes": len(AXES),
        "space_size": f"{space_size():.3e}",
        "generations_completed": len(reports),
        "strict_front_size": len(strict_front),
        "epsilon": epsilon,
        "epsilon_front_size": len(epsilon_front),
        "metric_equivalence_classes": len(classes),
        "shortlist_reasons": reasons,
        "axis_effects": axis_effect_table(registry),
        "measured_effects": measured_effects(registry),
        "no_effect_groups": sorted(
            (sorted(members) for members in classes.values() if len(members) > 1),
            key=lambda members: (-len(members), members[0]),
        )[:12],
        "candidates_registered": len(registry),
        "candidates_evaluated": len(evaluated),
        "candidates_hard_rejected": len(registry.rejected()),
        "registry_statistics": registry.statistics(),
        "split_manifest": split,
        "corpus": {
            "transitions": corpus_audit.get("corpus_transitions"),
            "selected": corpus_audit.get("selected_transitions"),
            "domains": len(corpus_audit.get("domains", {})),
        },
        "pareto_axes": list(PARETO_AXES),
        "front": [
            {
                "candidate_id": record.candidate_id,
                "label": label_for(record),
                "why_shortlisted": reasons.get(record.candidate_id, []),
                "derived_from": derivation(record, registry)[0],
                "genome_differences_from_seed": derivation(record, registry)[1],
                "seed": seed_ids.get(record.candidate_id),
                "origin": record.origin,
                "parents": list(record.parents),
                "ancestry": registry.ancestry(record.candidate_id),
                "token_rank": token_rank.get(record.candidate_id),
                "metrics": {
                    axis: round(record.metrics.get(axis, 0.0), 4) for axis in PARETO_AXES
                },
                "all_metrics": {
                    key: round(value, 4) for key, value in sorted((record.metrics or {}).items())
                },
                "genome": record.genome.to_dict()["axes"],
            }
            for record in ranked
        ],
        "controls": [
            {
                "label": name,
                "candidate_id": genome.candidate_id(),
                "status": (registry.get(genome.candidate_id()).status
                           if registry.get(genome.candidate_id()) else "NOT_REGISTERED"),
                "on_front": genome.candidate_id() in front,
                "on_strict_front": genome.candidate_id() in strict_front,
                "token_rank": token_rank.get(genome.candidate_id()),
                "rejection_reason": (registry.get(genome.candidate_id()).rejection_reason
                                     if registry.get(genome.candidate_id()) else None),
                "metrics": {
                    axis: round((registry.get(genome.candidate_id()).metrics or {}).get(axis, 0.0), 4)
                    for axis in PARETO_AXES
                } if registry.get(genome.candidate_id()) and registry.get(genome.candidate_id()).metrics else None,
            }
            for name, genome in sorted(SEEDS.items())
        ],
        "generations": [
            {
                "generation": report["generation"],
                "phase": report["phase"],
                "evaluated": len(report["evaluated"]),
                "hard_rejected": len(report["hard_rejected"]),
                "front_size": len(report["front"]),
                "frontier_moved": report["frontier_moved"],
                "blocked_by_memory": len(report["blocked_by_memory"]),
                "refuted_hypotheses": len(report["refuted_hypotheses"]),
                "elapsed_seconds": report["elapsed_seconds"],
            }
            for report in reports
        ],
        "refuted_hypotheses": [
            item for report in reports for item in report["refuted_hypotheses"]
        ],
        "blocked_by_memory": [
            item for report in reports for item in report["blocked_by_memory"]
        ],
        "rejection_reasons": registry.statistics()["by_rejection_reason"],
        "stall_count": state.get("stall_count"),
        "sealed_final_evaluation": sealed,
    }

    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "PRETRAINING_FRONTIER_V1.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    (args.out_dir / "PRETRAINING_FRONTIER_V1.md").write_text(render_markdown(payload, registry))
    print(f"wrote {args.out_dir}/PRETRAINING_FRONTIER_V1.md")


def render_markdown(payload: dict, registry: CandidateRegistry) -> str:
    lines: list[str] = [
        "# PRETRAINING_REPRESENTATION_FRONTIER_V1",
        "",
        "**This is not a claim that any representation is optimal for neural mathematical "
        "reasoning.** It is the strongest Pareto frontier obtainable from static evidence "
        "before model adaptation, together with the evidence that produced it.",
        "",
        "## Provenance",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Compiler | `{payload['compiler_version']}` |",
        f"| Canonical state | `{payload['canonical_state_version']}` |",
        f"| Genome axes | {payload['genome_axes']} |",
        f"| Search space | {payload['space_size']} points |",
        f"| Corpus transitions | {payload['corpus']['transitions']} |",
        f"| Mathlib domains | {payload['corpus']['domains']} |",
        f"| Generations completed | {payload['generations_completed']} |",
        f"| Candidates registered | {payload['candidates_registered']} |",
        f"| Candidates evaluated | {payload['candidates_evaluated']} |",
        f"| Candidates hard-rejected | {payload['candidates_hard_rejected']} |",
        f"| Strict Pareto front | {payload['strict_front_size']} |",
        f"| Distinct measurement vectors | {payload['metric_equivalence_classes']} |",
        f"| Reported finalists | {len(payload['front'])} |",
        "",
        "## Corpus split",
        "",
        "| Split | Transitions | Families |",
        "|---|---|---|",
    ]
    counts = payload["split_manifest"]["counts"]
    families = payload["split_manifest"]["family_counts"]
    for key in ("SEARCH_DEV", "SEARCH_VALIDATION", "SEALED_FINAL_EVALUATION"):
        lines.append(f"| `{key}` | {counts[key]} | {families[key]} |")
    lines += [
        "",
        f"Split unit: `{payload['split_manifest']['unit']}`. "
        f"Families hash `{payload['split_manifest']['families_sha256'][:16]}`.",
        "",
        "## The frontier",
        "",
        f"Strict non-dominated sorting over seven axes leaves {payload['strict_front_size']} "
        f"of {payload['candidates_evaluated']} evaluated candidates on the front, and an "
        f"epsilon-front at eps={payload['epsilon']} still keeps "
        f"{payload['epsilon_front_size']}. With enough axes almost every candidate is best at "
        "something, so neither is a shortlist.",
        "",
        "The finalists below follow a rule that states why each one is present: **the best "
        "candidate on each Pareto axis taken alone, plus the knee** - the candidate closest "
        "to the ideal point after per-axis normalisation. Candidates with identical "
        "measurement vectors are collapsed first. Selection during the search used the strict "
        "front, so this reporting rule could not have steered it.",
        "",
        "| # | Candidate | Shortlisted because | BPE tokens | Binder distance | "
        "Premise distance | Swap detect | Drop-field detect | Ident. frag | Max span |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for index, item in enumerate(payload["front"], start=1):
        metrics = item["metrics"]
        lines.append(
            f"| {index} | `{item['label']}` | {', '.join(item['why_shortlisted'])} | "
            f"{metrics['bpe_tokens_per_transition']:.1f} | "
            f"{metrics['binder_use_distance_tokens']:.1f} | "
            f"{metrics['premise_to_action_distance_tokens']:.1f} | "
            f"{metrics['detect_swap_records']:.3f} | "
            f"{metrics['detect_drop_field']:.3f} | "
            f"{metrics['identifier_fragmentation']:.2f} | "
            f"{metrics['max_reference_span_tokens']:.1f} |"
        )
    lines += ["", "## Controls", "",
              "Every seeded baseline, whether or not it survived. `FM-002` and `FM-006` "
              "require the recorded baselines to remain visible for the whole search. "
              "Token rank is out of the whole evaluated population, lower is cheaper.",
              "",
              "| Baseline | Status | Strict front | Finalist | Token rank | BPE tokens | "
              "Binder distance | Rejection |",
              "|---|---|---|---|---:|---:|---:|---|"]
    for control in payload["controls"]:
        metrics = control.get("metrics") or {}
        lines.append(
            f"| `{control['label']}` | {control['status']} | "
            f"{'yes' if control.get('on_strict_front') else 'no'} | "
            f"{'**yes**' if control['on_front'] else 'no'} | "
            f"{control['token_rank'] if control['token_rank'] else '—'} | "
            + (f"{metrics['bpe_tokens_per_transition']:.0f}" if metrics else "—") + " | "
            + (f"{metrics['binder_use_distance_tokens']:.0f}" if metrics else "—") + " | "
            f"{control['rejection_reason'] or '—'} |"
        )
    lines += ["", "## Generations", "",
              "| Gen | Phase | Evaluated | Rejected | Front | Frontier moved | "
              "Memory blocks | Refuted | Seconds |",
              "|---|---|---:|---:|---:|---|---:|---:|---:|"]
    for report in payload["generations"]:
        lines.append(
            f"| {report['generation']} | {report['phase'] or '—'} | {report['evaluated']} | "
            f"{report['hard_rejected']} | {report['front_size']} | "
            f"{'yes' if report['frontier_moved'] else 'no'} | "
            f"{report['blocked_by_memory']} | {report['refuted_hypotheses']} | "
            f"{report['elapsed_seconds']:.1f} |"
        )
    lines += ["", "## Why candidates were rejected", "",
              "Rejections are evidence, not waste: they are what demonstrates that the hard "
              "gates bite.", "", "| Reason | Candidates |", "|---|---:|"]
    for reason, count in sorted(payload["rejection_reasons"].items(),
                                key=lambda item: -item[1]):
        lines.append(f"| `{reason}` | {count} |")

    refuted = payload["refuted_hypotheses"]
    lines += ["", "## Refuted hypotheses", "",
              f"{len(refuted)} proposed mutations moved their target metric the wrong way. "
              "Each is a recorded negative result.", ""]
    if refuted:
        lines += ["| Axis | From | To | Metric | Parent | Child |", "|---|---|---|---|---:|---:|"]
        seen = set()
        for item in refuted:
            key = (item["axis"], item["from"], item["to"], item["metric"])
            if key in seen:
                continue
            seen.add(key)
            lines.append(
                f"| `{item['axis']}` | `{item['from']}` | `{item['to']}` | "
                f"`{item['metric']}` | {item['parent_value']:.3f} | {item['child_value']:.3f} |"
            )
    blocked = payload["blocked_by_memory"]
    if blocked:
        lines += ["", "## Mutations the failure memory blocked", "",
                  "| Axis | Value | Reason |", "|---|---|---|"]
        seen = set()
        for item in blocked:
            key = (item["axis"], item["value"], item["reason"])
            if key in seen:
                continue
            seen.add(key)
            lines.append(f"| `{item['axis']}` | `{item['value']}` | `{item['reason']}` |")

    lines += ["", "## Finalist profiles", ""]
    for index, item in enumerate(payload["front"][:5], start=1):
        record = registry.get(item["candidate_id"])
        differences = item["genome_differences_from_seed"]
        lines += [
            f"### {index}. `{item['candidate_id']}`",
            "",
            f"**Shortlisted because:** {', '.join(item['why_shortlisted'])}.",
            "",
            f"**Descends from:** `{item['derived_from']}` via "
            f"{max(0, len(item['ancestry']) - 1)} recorded step(s); origin `{item['origin']}`.",
            "",
            "**Genome differences from that seed:** "
            + (", ".join(f"`{diff}`" for diff in differences) if differences else "none"),
            "",
            "| Metric | Value |", "|---|---:|",
        ]
        for key, value in item["all_metrics"].items():
            lines.append(f"| `{key}` | {value} |")
        lines += ["", "<details><summary>Genome</summary>", "",
                  "| Axis | Value |", "|---|---|"]
        for axis, value in sorted(item["genome"].items()):
            lines.append(f"| `{axis}` | `{value}` |")
        lines += ["", "</details>", ""]

    effects = [row for row in payload["measured_effects"] if row["sign_agreement"] >= 0.75]
    lines += ["", "## Measured structural effects", "",
              "One parent-child pair is an anecdote. The table below aggregates every "
              "single-axis mutation applied to two or more different parents and reports the "
              "mean relative change in the metric that axis was predicted to move, with the "
              "fraction of observations agreeing in sign. Only transitions with at least 75% "
              "sign agreement are shown.",
              "",
              "| Axis | From | To | Metric | Mean change | n | Agreement | Verdict |",
              "|---|---|---|---|---:|---:|---:|---|"]
    for row in effects[:24]:
        lines.append(
            f"| `{row['axis']}` | `{row['from']}` | `{row['to']}` | `{row['metric']}` | "
            f"{row['mean_relative_change']:+.1%} | {row['observations']} | "
            f"{row['sign_agreement']:.0%} | "
            f"{'improves' if row['improves'] else '**costs**'} |"
        )

    lines += ["", "## Which axes this corpus can speak to", "",
              "Every single-axis mutation whose child measured identically to its parent is "
              "evidence that the axis has no effect **on this corpus** — not that it is a bad "
              "axis. Reporting it is more useful than reporting a search that appears to have "
              "explored it.",
              "",
              "| Axis | Single-axis mutations | Changed the measurement | Share |",
              "|---|---:|---:|---:|"]
    for row in payload["axis_effects"]:
        lines.append(
            f"| `{row['axis']}` | {row['single_axis_mutations']} | "
            f"{row['changed_the_measurement']} | {row['share']:.0%} |"
        )
    if payload["no_effect_groups"]:
        lines += ["", "### Largest groups of candidates that measure identically", "",
                  "| Candidates | Group size |", "|---|---:|"]
        for members in payload["no_effect_groups"]:
            lines.append(
                f"| {', '.join('`' + item + '`' for item in members[:4])}"
                + (f" and {len(members) - 4} more" if len(members) > 4 else "")
                + f" | {len(members)} |"
            )

    sealed = payload.get("sealed_final_evaluation")
    lines += ["", "## Sealed evaluation", ""]
    if sealed:
        lines += [
            f"The sealed split holds {sealed['sealed_transitions']} transitions from "
            "families never read during the search. It was evaluated once, after the "
            "frontier was frozen.",
            "",
            "| Candidate | Gates | BPE tokens | Binder distance | Swap detect |",
            "|---|---|---:|---:|---:|",
        ]
        for result in sealed["results"]:
            axes = result.get("pareto_axes", {})
            lines.append(
                f"| `{result['candidate_id']}` | "
                f"{'PASS' if result['gates_passed'] else result['first_gate_failure']} | "
                f"{axes.get('bpe_tokens_per_transition', float('nan')):.1f} | "
                f"{axes.get('binder_use_distance_tokens', float('nan')):.1f} | "
                f"{axes.get('detect_swap_records', float('nan')):.3f} |"
            )
    else:
        lines.append("Not yet run. The sealed split has never been read.")

    lines += [
        "",
        "## Companion reports",
        "",
        "- [`FINALIST_DOMAIN_PROFILES.md`](FINALIST_DOMAIN_PROFILES.md) — each finalist "
        "measured per Mathlib domain, because a frontier table reports averages and a user "
        "of the language asks about their own mathematics.",
        "- [`DISCOVERY_REPRESENTATION_ANALYSIS.md`](DISCOVERY_REPRESENTATION_ANALYSIS.md) — "
        "what PRM800K's step labels expose that no representation in this space can, and why.",
        "- [`NOTATION_COVERAGE.md`](NOTATION_COVERAGE.md) — which human mathematical "
        "constructs the formal corpus barely exercises.",
        "- [`FRONTIER_VALIDATION.md`](FRONTIER_VALIDATION.md) — the finalists re-measured on "
        "the validation split selection never read, with rank correlations.",
        "- [`GATE_HOLDOUT_AUDIT.json`](GATE_HOLDOUT_AUDIT.json) — every gate verdict re-run "
        "on a disjoint dev slice, to catch a verdict that held only by evaluation order.",
        "- [`REPRODUCIBILITY.json`](REPRODUCIBILITY.json) — candidates re-rendered in a fresh "
        "subprocess under a different hash seed, testing the claim that a genome hash "
        "determines a language.",
        "- [`../audits/LEAN_RUNTIME_V2_CORPUS.md`](../audits/LEAN_RUNTIME_V2_CORPUS.md) — the "
        "corpus accounting, with every excluded transition counted by reason.",
        "",
        "## What this does not establish",
        "",
        "- That any of these representations makes mathematical reasoning easier for a model. "
        "No model was run, and `FM-003` records that on the last task most of the measured "
        "accuracy was lexical.",
        "- That the token rankings generalise. They are measured under one pinned GPT-2 "
        "vocabulary; the prior audit used Qwen3-8B, where every mathematical glyph the corpus "
        "needs is a single token and these numbers would differ.",
        "- That the frontier is the global frontier. The space has "
        f"{payload['space_size']} points and this search evaluated "
        f"{payload['candidates_evaluated']}.",
        "",
        "The next step that would change any of this is a matched, controlled model "
        "experiment on the finalists, gated by the six lexical controls `FM-003` requires.",
    ]
    return "\n".join(lines).rstrip() + "\n"


if __name__ == "__main__":
    main()
