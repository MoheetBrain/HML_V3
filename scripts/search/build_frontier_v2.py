#!/usr/bin/env python3
"""Build the V2 frontier report from a completed open-ended search workspace.

Reads only ``data/representation_search_v2/``. Writes
``reports/representation_search_v2/FINAL_FRONTIER.{md,json}``.

The report states what was measured, what was not, and where the search stopped and why. It
never claims optimality.
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
from hml_v3.representation_search.controller_v2 import SELECTION_AXES  # noqa: E402
from hml_v3.representation_search.corpus import load_corpus  # noqa: E402
from hml_v3.representation_search.genome import AXES  # noqa: E402
from hml_v3.representation_search.genome_migrations import (  # noqa: E402
    extended_space,
    space_size,
)
from hml_v3.representation_search.lineage import CandidateRegistry  # noqa: E402
from hml_v3.representation_search.metrics import MAXIMISED  # noqa: E402
from hml_v3.representation_search.pareto import non_dominated_sort, shortlist  # noqa: E402
from hml_v3.representation_search.primitive_registry import PrimitiveRegistry  # noqa: E402
from hml_v3.representation_search.sealing import split_search_pool  # noqa: E402
from hml_v3.representation_search.seeds import SEEDS  # noqa: E402
from hml_v3.representation_search.tokenizers import audit, ordering_agreement  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=Path,
                        default=ROOT / "data/representation_search_v2")
    parser.add_argument("--corpus", type=Path,
                        default=ROOT / "data/corpus/search_pool_v2.jsonl.gz",
                        help="the search pool; the seal is a separate file and is not read here")
    parser.add_argument("--out-dir", type=Path,
                        default=ROOT / "reports/representation_search_v2")
    args = parser.parse_args()

    registry = CandidateRegistry(args.workspace / "candidate_registry.jsonl")
    primitives = PrimitiveRegistry(args.workspace / "primitive_registry.jsonl")
    state = json.loads((args.workspace / "search_state.json").read_text())
    split_manifest = json.loads((args.workspace / "split_manifest.json").read_text())
    generations = sorted((args.workspace / "generations").glob("generation_*.json"))
    reports = [json.loads(path.read_text()) for path in generations]

    rows = load_corpus(args.corpus)
    split = split_search_pool(rows)
    sample = split.dev[:16]

    accepted = registry.accepted()
    population = [(record.candidate_id, record.metrics or {}) for record in accepted]
    strict = non_dominated_sort(population, SELECTION_AXES)
    finalists, reasons = shortlist(population, SELECTION_AXES)
    space = extended_space(primitives)
    seed_ids = {genome.candidate_id(): name for name, genome in SEEDS.items()}

    # Multi-tokenizer audit over the finalists.
    per_candidate = {}
    for candidate_id in finalists:
        record = registry.get(candidate_id)
        if record is None:
            continue
        compiler = build(record.genome)
        renderings = [compiler.render_text(row) for row in sample]
        role_words = [
            compiler.surface.lexicon.word(key)
            for key in ("goal", "decl", "target", "context", "action")
        ]
        per_candidate[seed_ids.get(candidate_id, candidate_id)] = audit(renderings, role_words)
    agreement = ordering_agreement(per_candidate)

    proposal_types: dict[str, int] = {}
    backend_stats: dict[str, dict[str, int]] = {}
    for report in reports:
        for name, info in (report.get("proposals", {}).get("by_backend") or {}).items():
            entry = backend_stats.setdefault(name, {"accepted": 0, "rejected": 0})
            entry["accepted"] += info.get("accepted", 0)
            entry["rejected"] += info.get("rejected", 0)
            for kind in info.get("types", []):
                proposal_types[kind] = proposal_types.get(kind, 0) + 1

    payload = {
        "name": "PRETRAINING_REPRESENTATION_FRONTIER_V2",
        "claim_of_universal_optimality": False,
        "compiler_version": COMPILER_VERSION,
        "canonical_state_version": CANONICAL_STATE_VERSION,
        "genome_schema": primitives.schema_version,
        "axes_before": len(AXES),
        "axes_after": len(space.axes),
        "space_size": f"{space_size(space):.3e}",
        "generations_completed": len(reports),
        "candidates_registered": len(registry),
        "candidates_evaluated": len(accepted),
        "candidates_killed": len(registry.rejected()),
        "kill_levels": _kill_levels(reports),
        "strict_front_size": len(strict[0]) if strict else 0,
        "finalists": [],
        "controls": [],
        "primitives": primitives.statistics(),
        "unimplementable_proposals": len(primitives.unimplementable),
        "proposal_types_seen": dict(sorted(proposal_types.items())),
        "backends": backend_stats,
        "quarantine": state.get("quarantine", {}),
        "split_manifest": split_manifest,
        "selection_axes": list(SELECTION_AXES),
        "tokenizer_agreement": agreement,
        "generations": [
            {
                "generation": report["generation"],
                "evaluated": len(report["evaluated"]),
                "killed": len(report["killed"]),
                "front": len(report["front"]),
                "new_axes": report["new_axes"],
                "moved": report["frontier_moved"],
                "ladder": report.get("ladder", {}),
                "seconds": report["elapsed_seconds"],
            }
            for report in reports
        ],
        "stall_count": state.get("stall_count"),
        "structural_convergence": bool(
            state.get("stall_count", 0) >= state.get("config", {}).get("stall_limit", 5)),
    }

    for candidate_id in finalists:
        record = registry.get(candidate_id)
        if record is None:
            continue
        payload["finalists"].append({
            "candidate_id": candidate_id,
            "label": seed_ids.get(candidate_id, candidate_id),
            "why_shortlisted": reasons.get(candidate_id, []),
            "origin": record.origin,
            "parents": list(record.parents),
            "invented_axes": state.get("invented", {}).get(candidate_id, {}),
            "metrics": {
                axis: round((record.metrics or {}).get(axis, 0.0), 4)
                for axis in SELECTION_AXES
            },
            "all_metrics": {
                key: round(value, 4)
                for key, value in sorted((record.metrics or {}).items())
                if not key.startswith("_")
            },
            "genome": record.genome.to_dict()["axes"],
        })

    for name, genome in sorted(SEEDS.items()):
        record = registry.get(genome.candidate_id())
        payload["controls"].append({
            "label": name,
            "candidate_id": genome.candidate_id(),
            "status": record.status if record else "NOT_REGISTERED",
            "on_strict_front": bool(strict and genome.candidate_id() in strict[0]),
            "finalist": genome.candidate_id() in finalists,
            "metrics": {
                axis: round((record.metrics or {}).get(axis, 0.0), 4)
                for axis in SELECTION_AXES
            } if record and record.metrics else None,
        })

    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "FINAL_FRONTIER.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    (args.out_dir / "FINAL_FRONTIER.md").write_text(_markdown(payload))
    print(f"wrote {args.out_dir}/FINAL_FRONTIER.md")
    print(f"{len(payload['finalists'])} finalists, "
          f"{payload['axes_after'] - payload['axes_before']} invented axes accepted")


def _kill_levels(reports: list[dict]) -> dict[str, int]:
    levels: dict[str, int] = {}
    for report in reports:
        for kill in report.get("killed", []):
            level = kill.get("level", "unknown")
            levels[level] = levels.get(level, 0) + 1
    return dict(sorted(levels.items()))


def _markdown(payload: dict) -> str:
    lines = [
        "# PRETRAINING_REPRESENTATION_FRONTIER_V2",
        "",
        "**This is not a claim that any representation is optimal for neural mathematical "
        "reasoning.** It is what an open-ended search found before model adaptation, together "
        "with the evidence that produced it and the limits of that evidence.",
        "",
        "## Provenance",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Compiler | `{payload['compiler_version']}` |",
        f"| Canonical state | `{payload['canonical_state_version']}` |",
        f"| Genome schema | `{payload['genome_schema']}` |",
        f"| Axes before / after | {payload['axes_before']} / {payload['axes_after']} |",
        f"| Search space | {payload['space_size']} points |",
        f"| Generations | {payload['generations_completed']} |",
        f"| Candidates registered | {payload['candidates_registered']} |",
        f"| Candidates evaluated | {payload['candidates_evaluated']} |",
        f"| Candidates killed | {payload['candidates_killed']} |",
        f"| Strict Pareto front | {payload['strict_front_size']} |",
        f"| Reported finalists | {len(payload['finalists'])} |",
        f"| Structural convergence | {'YES' if payload['structural_convergence'] else 'NO'} |",
        "",
        "## Where candidates died",
        "",
        "The ladder exists so a candidate is killed at the cheapest level that can kill it.",
        "",
        "| Level | Killed |",
        "|---|---:|",
    ]
    for level, count in payload["kill_levels"].items():
        lines.append(f"| `{level}` | {count} |")

    lines += ["", "## The meta-designer", "",
              "| Backend | Proposals accepted | Rejected |", "|---|---:|---:|"]
    for name, stats in sorted(payload["backends"].items()):
        lines.append(f"| `{name}` | {stats['accepted']} | {stats['rejected']} |")
    lines += ["",
              f"Proposal types seen: {', '.join(f'`{k}`' for k in payload['proposal_types_seen'])}"
              or "none",
              "",
              f"Invented axes accepted: **{payload['axes_after'] - payload['axes_before']}**. "
              f"Proposals recorded as unimplementable: **{payload['unimplementable_proposals']}** "
              "— kept as evidence about what the meta-designer wanted and what the projection "
              "algebra could not express."]

    lines += ["", "## The frontier", "",
              "| # | Candidate | Shortlisted because | Origin | Invented axes |",
              "|---|---|---|---|---|"]
    for index, item in enumerate(payload["finalists"], start=1):
        lines.append(
            f"| {index} | `{item['label']}` | {', '.join(item['why_shortlisted'])} | "
            f"{item['origin']} | {item['invented_axes'] or '—'} |"
        )

    if payload["finalists"]:
        axes = payload["selection_axes"]
        lines += ["", "| Candidate | " + " | ".join(f"`{a}`" for a in axes) + " |",
                  "|---" * (len(axes) + 1) + "|"]
        for item in payload["finalists"]:
            cells = " | ".join(f"{item['metrics'].get(a, 0):.3f}" for a in axes)
            lines.append(f"| `{item['label']}` | {cells} |")

    lines += ["", "## Controls", "",
              "`FM-002` requires the recorded baselines to stay visible whether or not they "
              "survive.", "",
              "| Baseline | Status | Strict front | Finalist |", "|---|---|---|---|"]
    for control in payload["controls"]:
        lines.append(
            f"| `{control['label']}` | {control['status']} | "
            f"{'yes' if control['on_strict_front'] else 'no'} | "
            f"{'**yes**' if control['finalist'] else 'no'} |"
        )

    agreement = payload["tokenizer_agreement"]
    lines += ["", "## Multi-tokenizer audit", "",
              f"Vocabularies compared: **{agreement.get('vocabularies_compared', 0)}**. "
              f"Same cheapest candidate under every vocabulary: "
              f"**{'yes' if agreement.get('same_leader_everywhere') else 'no'}**.", ""]
    if agreement.get("leaders"):
        lines += ["| Vocabulary | Cheapest finalist |", "|---|---|"]
        for name, leader in sorted(agreement["leaders"].items()):
            lines.append(f"| `{name}` | `{leader}` |")
    lines += ["",
              "`FM-018` binds the reading: the escaping penalty reproduces across "
              "vocabularies, the absolute counts do not. A ranking that flips between "
              "vocabularies is a vocabulary effect and is not a property of the "
              "representation."]

    quarantine = payload.get("quarantine") or {}
    lines += ["", "## Validation-governed selection", "",
              f"Quarantined as non-generalising: **{quarantine.get('quarantined', 0)}**.", ""]
    if quarantine.get("by_verdict"):
        lines += ["| Verdict | Candidates |", "|---|---:|"]
        for verdict, count in quarantine["by_verdict"].items():
            lines.append(f"| `{verdict}` | {count} |")

    lines += ["", "## Generations", "",
              "| Gen | Evaluated | Killed | Front | Moved | New axes | Seconds |",
              "|---|---:|---:|---:|---|---|---:|"]
    for report in payload["generations"]:
        lines.append(
            f"| {report['generation']} | {report['evaluated']} | {report['killed']} | "
            f"{report['front']} | {'yes' if report['moved'] else 'no'} | "
            f"{report['new_axes'] or '—'} | {report['seconds']:.0f} |"
        )

    lines += [
        "", "## What this does not establish", "",
        "- That any of these makes mathematical reasoning easier for a model. The neural "
        "probes here are inference-only, tiny, and reported with their sequential rule.",
        "- That the frontier is global. The space has "
        f"{payload['space_size']} points and this search evaluated "
        f"{payload['candidates_evaluated']}.",
        f"- That the search converged. `STRUCTURAL_CONVERGENCE = "
        f"{'YES' if payload['structural_convergence'] else 'NO'}`.",
        "- That open-endedness is unbounded. An invented axis must bind to one of four "
        "projection hooks; proposals outside that algebra are recorded, not run.",
    ]
    return "\n".join(lines).rstrip() + "\n"


if __name__ == "__main__":
    main()
