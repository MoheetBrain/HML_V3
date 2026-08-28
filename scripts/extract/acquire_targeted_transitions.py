#!/usr/bin/env python3
"""Acquire a structurally targeted transition pool from the pinned LeanDojo trace.

Answers a specific measured defect rather than "get more data": `FM-020` recorded that goal
linearization is unmeasurable because the corpus averages 1.01 goals per state. This selects
for the strata that make the unmeasurable axes measurable, and emits records in the V1 source
schema so the existing prepare/replay pipeline elaborates every one of them in Lean.
"""

from __future__ import annotations

import argparse
import gzip
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hml_v3.representation_search.active_corpus import (  # noqa: E402
    AcquisitionRequest,
    iter_transitions,
    load_leandojo,
    select_stratified,
)

DEFAULT_LEANDOJO = Path(
    "/Users/moheet/Projects/Hamiltonian-Labs/hml_research_artifacts/leandojo_raw/"
    "leandojo_benchmark_4/random"
)

#: The measured gaps this acquisition is meant to close.
DEFAULT_REQUESTS = [
    AcquisitionRequest(
        reason="FM-020: goal linearization axes are unidentifiable at 1.01 goals per state",
        stratum="goal_count", values=("2", "3-5", ">5"), desired_per_value=260,
    ),
    AcquisitionRequest(
        reason="premise_locality effects need states that actually cite several premises",
        stratum="premises", values=("3-5", "6+"), desired_per_value=170,
    ),
    AcquisitionRequest(
        reason="binder axes need deep binder nesting, rare in the current corpus",
        stratum="binder_depth", values=("9+",), desired_per_value=170,
    ),
    AcquisitionRequest(
        reason="context_order axes need heavy local contexts to separate",
        stratum="context_size", values=("31+",), desired_per_value=170,
    ),
]


def existing_ids(paths: list[Path]) -> set[str]:
    found: set[str] = set()
    for path in paths:
        if not path.exists():
            continue
        for line in path.open(encoding="utf-8"):
            if line.strip():
                found.add(json.loads(line)["record_id"])
    return found


def traced_files(runtime_root: Path) -> set[str]:
    """Source files whose .ast.json trace exists, so the join can succeed."""

    available: set[str] = set()
    build = runtime_root / ".lake/build/ir"
    for path in build.rglob("*.ast.json"):
        relative = path.relative_to(build).as_posix()[: -len(".ast.json")] + ".lean"
        available.add(relative)
    for package in (runtime_root / ".lake/packages").glob("*/.lake/build/ir"):
        for path in package.rglob("*.ast.json"):
            relative = path.relative_to(package).as_posix()[: -len(".ast.json")] + ".lean"
            available.add(f".lake/packages/{package.parents[1].name}/{relative}")
    return available


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--leandojo-dir", type=Path, default=DEFAULT_LEANDOJO)
    parser.add_argument("--splits", nargs="+", default=["train.json"])
    parser.add_argument("--runtime-root", type=Path, required=True)
    parser.add_argument("--exclude-selection", type=Path, action="append", default=[])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--total-cap", type=int, default=None)
    args = parser.parse_args()

    records: list[dict] = []
    for split in args.splits:
        path = args.leandojo_dir / split
        if not path.exists():
            print(f"skipping missing {path}", flush=True)
            continue
        print(f"loading {path} ({path.stat().st_size / 1e6:.0f} MB)", flush=True)
        theorems = load_leandojo(path)
        print(f"  {len(theorems):,} theorems", flush=True)
        records.extend(iter_transitions(theorems))
        print(f"  cumulative transitions: {len(records):,}", flush=True)

    available = traced_files(args.runtime_root)
    print(f"traced source files available: {len(available):,}", flush=True)

    selected, manifest = select_stratified(
        records, DEFAULT_REQUESTS, existing_ids(args.exclude_selection),
        available_files=available or None, total_cap=args.total_cap,
    )
    manifest["total_transitions_scanned"] = len(records)
    manifest["traced_files_available"] = len(available)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as zipped:
            for record in selected:
                zipped.write((json.dumps(record, ensure_ascii=False, sort_keys=True,
                                         separators=(",", ":")) + "\n").encode())
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps(manifest, indent=2)[:2500])


if __name__ == "__main__":
    main()
