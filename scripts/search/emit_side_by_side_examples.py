#!/usr/bin/env python3
"""Write the same mathematical states in every candidate language, side by side.

Selection is by measurement, never by how the output looks. But a discovered language that
nobody can read is not a result anyone can check, so this exists for human audit: the same
canonical transitions rendered as Lean-like, prior HML, Structured English, typed AST and each
finalist, with the canonical ground truth alongside.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hml_v3.representation_search.compiler import build  # noqa: E402
from hml_v3.representation_search.controller_v2 import SELECTION_AXES  # noqa: E402
from hml_v3.representation_search.corpus import load_corpus  # noqa: E402
from hml_v3.representation_search.lineage import CandidateRegistry  # noqa: E402
from hml_v3.representation_search.pareto import shortlist  # noqa: E402
from hml_v3.representation_search.primitive_registry import PrimitiveRegistry  # noqa: E402
from hml_v3.representation_search.sealing import split_corpus  # noqa: E402
from hml_v3.representation_search.seeds import SEEDS  # noqa: E402

CONTROLS = ("SEED_LEAN_LIKE", "SEED_PRIOR_HML", "SEED_STRUCTURED_ENGLISH", "SEED_TYPED_AST")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path,
                        default=ROOT / "data/corpus/lean_runtime_v2.canonical.jsonl.gz")
    parser.add_argument("--workspace", type=Path,
                        default=ROOT / "data/representation_search_v2")
    parser.add_argument("--out", type=Path,
                        default=ROOT / "reports/representation_search_v2/SIDE_BY_SIDE_EXAMPLES.md")
    parser.add_argument("--examples", type=int, default=20)
    parser.add_argument("--max-chars", type=int, default=2400)
    args = parser.parse_args()

    rows = load_corpus(args.corpus)
    split = split_corpus(rows)
    # Spread across structural shapes rather than taking the first N, or every example looks
    # the same and the comparison shows nothing.
    ordered = sorted(
        split.dev,
        key=lambda row: (
            len(row["state_before"]["goals"]),
            sum(len(goal["local_context"]) for goal in row["state_before"]["goals"]),
        ),
    )
    step = max(1, len(ordered) // args.examples)
    chosen = ordered[::step][: args.examples]

    arms: list[tuple[str, object, dict]] = [
        (name, SEEDS[name], {}) for name in CONTROLS if name in SEEDS
    ]
    registry = CandidateRegistry(args.workspace / "candidate_registry.jsonl")
    primitives = PrimitiveRegistry(args.workspace / "primitive_registry.jsonl")
    state_path = args.workspace / "search_state.json"
    invented_map = (
        json.loads(state_path.read_text()).get("invented", {}) if state_path.exists() else {}
    )
    if len(registry):
        population = [(r.candidate_id, r.metrics or {}) for r in registry.accepted()]
        finalists, reasons = shortlist(population, SELECTION_AXES)
        for candidate_id in finalists[:5]:
            record = registry.get(candidate_id)
            if record is None:
                continue
            label = next(
                (name for name, genome in SEEDS.items()
                 if genome.candidate_id() == candidate_id), candidate_id)
            arms.append((f"FINALIST {label}", record.genome,
                         invented_map.get(candidate_id, {})))

    lines = [
        "# Side-by-Side Examples",
        "",
        "The same verified Lean transitions written in every candidate language. Selection in "
        "this project is by measurement and never by appearance; this file exists so a human "
        "can check what the search actually produced.",
        "",
        f"Rendered arms: {len(arms)}. Examples: {len(chosen)}, spread across goal count and "
        "local-context size rather than taken consecutively.",
        "",
    ]

    compiled = []
    for label, genome, invented in arms:
        try:
            compiled.append((label, build(genome, invented, primitives if invented else None)))
        except Exception as error:  # noqa: BLE001
            lines.append(f"- `{label}` failed to compile: {type(error).__name__}")

    for index, transition in enumerate(chosen, start=1):
        goals = transition["state_before"]["goals"]
        declarations = sum(len(goal["local_context"]) for goal in goals)
        lines += [
            f"## Example {index} — `{transition['transition_id'][:96]}`",
            "",
            f"**Shape:** {len(goals)} goal(s), {declarations} local declaration(s), "
            f"{len(transition['action']['external_premise_refs'])} external premise(s). "
            f"Domain `{(transition.get('corpus_metadata') or {}).get('domain', 'unknown')}`.",
            "",
        ]
        for label, compiler in compiled:
            text = compiler.render_text(transition)
            truncated = text[: args.max_chars]
            suffix = "" if len(text) <= args.max_chars else (
                f"\n... [{len(text) - args.max_chars} more characters]")
            lines += [
                f"### {label}",
                "",
                f"*{len(text):,} characters*",
                "",
                "```text",
                truncated + suffix,
                "```",
                "",
            ]

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"wrote {args.out}: {len(chosen)} examples x {len(compiled)} arms")


if __name__ == "__main__":
    main()
