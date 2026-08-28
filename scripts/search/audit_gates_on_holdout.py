#!/usr/bin/env python3
"""Re-run every hard gate for every evaluated candidate on a disjoint dev sample.

The controller evaluates gates on the first N dev transitions. A gate that passed only
because of that particular slice — an evaluation-order accident — would be invisible to the
search itself. This re-audits every candidate in the registry on a *different* slice of the
same dev split, and fails loudly if any candidate's verdict changes.

The sealed split is not read.
"""

from __future__ import annotations

import argparse
import gzip
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hml_v3.representation_search.corpus import load_corpus  # noqa: E402
from hml_v3.representation_search.compiler import CompilerRejection, build  # noqa: E402
from hml_v3.representation_search.gates import run_gates  # noqa: E402
from hml_v3.representation_search.lineage import CandidateRegistry  # noqa: E402
from hml_v3.representation_search.sealing import split_corpus  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path,
                        default=ROOT / "data/corpus/lean_runtime_v2.canonical.jsonl.gz")
    parser.add_argument("--workspace", type=Path, default=ROOT / "data/representation_search")
    parser.add_argument("--offset", type=int, default=100,
                        help="start of the holdout slice; must exceed the controller's dev sample")
    parser.add_argument("--size", type=int, default=40)
    parser.add_argument("--out", type=Path,
                        default=ROOT / "reports/representation_search/GATE_HOLDOUT_AUDIT.json")
    args = parser.parse_args()

    rows = load_corpus(args.corpus)
    dev = split_corpus(rows).dev
    sample = dev[args.offset: args.offset + args.size]
    if len(sample) < args.size:
        raise SystemExit(
            f"dev split has {len(dev)} transitions; cannot take {args.size} from {args.offset}"
        )

    registry = CandidateRegistry(args.workspace / "candidate_registry.jsonl")
    accepted = registry.accepted()
    rejected = registry.rejected()

    disagreements = []
    for record in accepted:
        try:
            compiler = build(record.genome)
        except CompilerRejection as error:
            disagreements.append({
                "candidate_id": record.candidate_id, "search_verdict": "EVALUATED",
                "holdout_verdict": f"COMPILE_REJECT:{error}",
            })
            continue
        report = run_gates(compiler, sample)
        if not report.passed:
            disagreements.append({
                "candidate_id": record.candidate_id, "search_verdict": "EVALUATED",
                "holdout_verdict": report.first_failure,
            })
    for record in rejected:
        try:
            compiler = build(record.genome)
        except CompilerRejection:
            continue
        report = run_gates(compiler, sample)
        if report.passed:
            disagreements.append({
                "candidate_id": record.candidate_id,
                "search_verdict": f"HARD_REJECTED:{record.rejection_reason}",
                "holdout_verdict": "PASSED_ON_HOLDOUT",
            })

    result = {
        "corpus": str(args.corpus),
        "holdout_slice": {"offset": args.offset, "size": len(sample)},
        "candidates_evaluated": len(accepted),
        "candidates_hard_rejected": len(rejected),
        "disagreements": disagreements,
        "verdicts_stable": not disagreements,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2)[:1200])
    if disagreements:
        raise SystemExit(
            f"GATE_VERDICT_UNSTABLE: {len(disagreements)} candidates changed verdict on a "
            "disjoint dev sample"
        )


if __name__ == "__main__":
    main()
