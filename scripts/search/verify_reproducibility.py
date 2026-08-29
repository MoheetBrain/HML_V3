#!/usr/bin/env python3
"""Verify the claim that a candidate is reproducible from its genome hash alone.

`D-010` says a candidate representation is fully determined by
``(genome_sha256, compiler_version, canonical_state_version)``. That is a claim about a
*different process*, not about calling render twice in one: a rendering that depended on
hash-seed order, dictionary insertion order or an interpreter-local cache would pass an
in-process check and fail this one.

Each candidate is therefore rendered in a fresh subprocess, launched with a different
PYTHONHASHSEED, and the resulting digests are compared with the digests from this process.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hml_v3.representation_search.corpus import load_corpus  # noqa: E402
from hml_v3.representation_search.compiler import (  # noqa: E402
    CANONICAL_STATE_VERSION,
    COMPILER_VERSION,
    build,
)
from hml_v3.representation_search.genome import RepresentationGenome  # noqa: E402
from hml_v3.representation_search.lineage import CandidateRegistry  # noqa: E402
from hml_v3.representation_search.primitive_registry import (  # noqa: E402
    PrimitiveRegistry,
)

CHILD = """
import hashlib, json, sys
from pathlib import Path
sys.path.insert(0, {src!r})
from hml_v3.representation_search.compiler import build
from hml_v3.representation_search.corpus import load_corpus
from hml_v3.representation_search.genome import RepresentationGenome
from hml_v3.representation_search.primitive_registry import PrimitiveRegistry

payload = json.loads(sys.stdin.read())
# Shard-aware. Opening the base name with gzip.open worked only while the corpus was a
# single file; it is written as size-capped shards and the base name does not exist.
rows = load_corpus(Path(payload["corpus"]))
rows = [row for row in rows if row["transition_id"] in set(payload["transition_ids"])]
rows.sort(key=lambda row: row["transition_id"])
registry = PrimitiveRegistry(Path(payload["primitives"])) if payload.get("primitives") else None
out = {{}}
for entry in payload["candidates"]:
    invented = entry.get("invented") or {{}}
    compiler = build(
        RepresentationGenome.from_dict(entry["genome"]),
        invented,
        registry if invented else None,
    )
    digest = hashlib.sha256()
    for row in rows:
        digest.update(compiler.render_text(row).encode())
    # Keyed by the RECORD id, never by the genome's own id. An invented-axis candidate
    # shares its base genome with its parent, so keying by the genome id collides for one
    # and returns nothing for the other -- which reads as a reproducibility failure.
    out[entry["candidate_id"]] = digest.hexdigest()
print(json.dumps(out))
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path,
                        default=ROOT / "data/corpus/search_pool_v2.jsonl.gz")
    parser.add_argument("--workspace", type=Path, default=ROOT / "data/representation_search")
    parser.add_argument("--candidates", type=int, default=24)
    parser.add_argument("--transitions", type=int, default=12)
    parser.add_argument("--out", type=Path,
                        default=ROOT / "reports/representation_search/REPRODUCIBILITY.json")
    args = parser.parse_args()

    rows = load_corpus(args.corpus)
    rows.sort(key=lambda row: row["transition_id"])
    sample = rows[: args.transitions]
    transition_ids = [row["transition_id"] for row in sample]

    registry = CandidateRegistry(args.workspace / "candidate_registry.jsonl")
    records = sorted(registry.accepted(), key=lambda record: record.candidate_id)
    records = records[: args.candidates]

    # Invented axes are part of what a candidate IS. Rendering without them verifies a
    # different object: 92 of this run's 566 candidates carry one, and every one of them
    # would be checked against a rendering it never produced.
    state_path = args.workspace / "search_state.json"
    invented_by_candidate: dict[str, dict[str, str]] = {}
    if state_path.exists():
        invented_by_candidate = json.loads(state_path.read_text()).get("invented", {}) or {}
    primitives_path = args.workspace / "primitive_registry.jsonl"
    primitives = PrimitiveRegistry(primitives_path) if primitives_path.exists() else None

    local: dict[str, str] = {}
    for record in records:
        invented = invented_by_candidate.get(record.candidate_id) or {}
        compiler = build(record.genome, invented, primitives if invented else None)
        digest = hashlib.sha256()
        for row in sample:
            digest.update(compiler.render_text(row).encode())
        local[record.candidate_id] = digest.hexdigest()

    environment = dict(os.environ)
    environment["PYTHONHASHSEED"] = "12345"
    process = subprocess.run(
        [sys.executable, "-c", CHILD.format(src=str(ROOT / "src"))],
        input=json.dumps({
            "corpus": str(args.corpus),
            "transition_ids": transition_ids,
            "primitives": str(primitives_path) if primitives_path.exists() else None,
            "candidates": [
                {
                    "candidate_id": record.candidate_id,
                    "genome": record.genome.to_dict(),
                    "invented": invented_by_candidate.get(record.candidate_id) or {},
                }
                for record in records
            ],
        }),
        text=True, capture_output=True, check=True, env=environment,
    )
    remote = json.loads(process.stdout)

    mismatches = sorted(
        candidate_id for candidate_id in local
        if local[candidate_id] != remote.get(candidate_id)
    )
    result = {
        "compiler_version": COMPILER_VERSION,
        "canonical_state_version": CANONICAL_STATE_VERSION,
        "candidates_checked": len(local),
        "candidates_carrying_an_invented_axis": sum(
            1 for record in records if invented_by_candidate.get(record.candidate_id)),
        "transitions_per_candidate": len(sample),
        "child_pythonhashseed": "12345",
        "parent_pythonhashseed": os.environ.get("PYTHONHASHSEED", "unset"),
        "mismatches": mismatches,
        "reproducible": not mismatches,
        "digests": local,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "digests"}, indent=2))
    if mismatches:
        raise SystemExit(f"NOT REPRODUCIBLE: {len(mismatches)} candidates differ across processes")


if __name__ == "__main__":
    main()
