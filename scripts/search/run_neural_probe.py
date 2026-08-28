#!/usr/bin/env python3
"""Run inference-only neural microprobes between representation arms.

Not training. A frozen local model answers matched multiple-choice questions whose ground
truth comes from the canonical state; the arms differ only in how that state is written.

The dumb controls run first and can veto the whole experiment: if a bag-of-words-grade
heuristic solves the questions, no model result from them would mean anything (`FM-003`).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hml_v3.representation_search.compiler import build  # noqa: E402
from hml_v3.representation_search.corpus import load_corpus  # noqa: E402
from hml_v3.representation_search.lineage import CandidateRegistry  # noqa: E402
from hml_v3.representation_search.neural_probe import (  # noqa: E402
    OllamaProbe,
    SequentialRule,
    build_items,
    controls_pass,
    run_arm,
)
from hml_v3.representation_search.sealing import split_corpus  # noqa: E402
from hml_v3.representation_search.seeds import SEEDS  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path,
                        default=ROOT / "data/corpus/lean_runtime_v2.canonical.jsonl.gz")
    parser.add_argument("--workspace", type=Path,
                        default=ROOT / "data/representation_search_v2")
    parser.add_argument("--arms", nargs="+", required=True,
                        help="seed labels or candidate ids; the first is the reference")
    parser.add_argument("--model", default="gemma3:4b")
    parser.add_argument("--mechanisms", nargs="+", default=["binder", "premise"])
    parser.add_argument("--checkpoint", type=int, default=20)
    parser.add_argument("--out", type=Path,
                        default=ROOT / "reports/representation_search_v2/NEURAL_PROBE.json")
    args = parser.parse_args()

    rows = load_corpus(args.corpus)
    dev = split_corpus(rows).dev
    by_id = {row["transition_id"]: row for row in dev}
    items = build_items(dev, args.mechanisms, seed=20260828, limit=args.checkpoint)

    usable, controls = controls_pass(items)
    rule = SequentialRule()
    payload: dict = {
        "model": args.model,
        "training_performed": False,
        "gpu_training": False,
        "mechanisms": args.mechanisms,
        "checkpoint": args.checkpoint,
        "items": len(items),
        "dumb_controls": controls,
        "benchmark_usable": usable,
        "stopping_rule": rule.to_dict(),
    }
    if not usable:
        payload["verdict"] = "INVALID_MICROBENCHMARK"
        payload["note"] = (
            "a cheap control solved the questions, so no model result from them would be "
            "evidence about representation (FM-003)"
        )
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        print(json.dumps(payload, indent=2)[:1200])
        return

    probe = OllamaProbe(args.model)
    if not probe.available():
        payload["verdict"] = "PROBE_UNAVAILABLE"
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        print(json.dumps(payload, indent=2)[:800])
        return

    registry = CandidateRegistry(args.workspace / "candidate_registry.jsonl")

    def compiler_for(name: str):
        if name in SEEDS:
            return build(SEEDS[name]), name
        record = registry.get(name)
        if record is None:
            raise SystemExit(f"unknown arm {name!r}")
        return build(record.genome), name

    results = []
    outcomes: dict[str, list[bool]] = {}
    for name in args.arms:
        compiler, label = compiler_for(name)
        result, arm_outcomes = run_arm(compiler, items, by_id, probe)
        outcomes[label] = arm_outcomes
        row = result.to_dict()
        row["arm"] = label
        results.append(row)
        print(f"{label:28s} accuracy {result.accuracy:.3f} "
              f"({result.correct}/{result.answered})", flush=True)

    reference = args.arms[0]
    comparisons = []
    for name in args.arms[1:]:
        decision = rule.decide(outcomes[name], outcomes[reference])
        decision["arm"] = name
        decision["reference"] = reference
        comparisons.append(decision)
        print(f"  {name} vs {reference}: {decision['verdict']} "
              f"(mean diff {decision['mean_difference']:+.3f}, z={decision['z']})")

    payload["arms"] = results
    payload["comparisons"] = comparisons
    payload["reference"] = reference
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
