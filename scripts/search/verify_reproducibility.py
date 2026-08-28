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

CHILD = """
import gzip, hashlib, json, sys
sys.path.insert(0, {src!r})
from hml_v3.representation_search.compiler import build
from hml_v3.representation_search.genome import RepresentationGenome

payload = json.loads(sys.stdin.read())
with gzip.open(payload["corpus"], "rt", encoding="utf-8") as handle:
    rows = [json.loads(line) for line in handle if line.strip()]
rows = [row for row in rows if row["transition_id"] in set(payload["transition_ids"])]
rows.sort(key=lambda row: row["transition_id"])
out = {{}}
for entry in payload["genomes"]:
    compiler = build(RepresentationGenome.from_dict(entry))
    digest = hashlib.sha256()
    for row in rows:
        digest.update(compiler.render_text(row).encode())
    out[entry["candidate_id"]] = digest.hexdigest()
print(json.dumps(out))
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path,
                        default=ROOT / "data/corpus/lean_runtime_v2.canonical.jsonl.gz")
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

    local: dict[str, str] = {}
    for record in records:
        compiler = build(record.genome)
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
            "genomes": [record.genome.to_dict() for record in records],
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
