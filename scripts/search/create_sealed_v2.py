#!/usr/bin/env python3
"""Freeze SEALED_FINAL_V2 into its own file, from families the V1 search never touched.

V1's sealed split was evaluated once, exactly as its policy allowed, which also means it has
been read. A frontier chosen after seeing an aggregate from those families is no longer being
tested against data it never influenced, so that split is retired as HISTORICAL_SEALED_V1.

V2's seal is drawn preferentially from theorem families acquired *after* the V1 search, and it
is written to a separate file so the search process holds a path rather than the rows.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hml_v3.representation_search.corpus import corpus_sha256, load_corpus, write_corpus  # noqa: E402
from hml_v3.representation_search.sealing import family_of  # noqa: E402

SPLIT_KEY = "hml-v3-sealed-final-v2"


def bucket(family: str) -> float:
    digest = hashlib.sha256(f"{SPLIT_KEY}|{family}".encode()).hexdigest()
    return int(digest[:16], 16) / float(1 << 64)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path,
                        default=ROOT / "data/corpus/lean_runtime_v2.canonical.jsonl.gz")
    parser.add_argument("--historical-split", type=Path,
                        default=ROOT / "data/representation_search/split_manifest.json")
    parser.add_argument("--sealed-out", type=Path,
                        default=ROOT / "data/corpus/sealed_final_v2.jsonl.gz")
    parser.add_argument("--search-out", type=Path,
                        default=ROOT / "data/corpus/search_pool_v2.jsonl.gz")
    parser.add_argument("--manifest", type=Path,
                        default=ROOT / "data/corpus/SEALED_V2_MANIFEST.json")
    parser.add_argument("--share", type=float, default=0.20)
    args = parser.parse_args()

    rows = load_corpus(args.corpus)
    by_family: dict[str, list[dict]] = {}
    for row in rows:
        by_family.setdefault(family_of(row), []).append(row)

    # Families acquired after the V1 search are preferred for the new seal: they cannot have
    # influenced the V1 frontier, so they are the cleanest thing available.
    fresh = {
        family for family, items in by_family.items()
        if any((row.get("corpus_metadata") or {}).get("raw_file", "").startswith(
            "campaign_targeted") for row in items)
    }

    ranked = sorted(by_family, key=lambda family: (family not in fresh, bucket(family)))
    target = int(len(rows) * args.share)
    sealed_families: set[str] = set()
    count = 0
    for family in ranked:
        if count >= target:
            break
        sealed_families.add(family)
        count += len(by_family[family])

    sealed = sorted(
        (row for row in rows if family_of(row) in sealed_families),
        key=lambda row: row["transition_id"])
    search = sorted(
        (row for row in rows if family_of(row) not in sealed_families),
        key=lambda row: row["transition_id"])

    write_corpus(sealed, args.sealed_out)
    write_corpus(search, args.search_out)

    manifest = {
        "name": "SEALED_FINAL_V2",
        "split_key": SPLIT_KEY,
        "unit": "MATHLIB_SOURCE_FILE",
        "sealed_transitions": len(sealed),
        "search_transitions": len(search),
        "sealed_families": len(sealed_families),
        "families_from_post_v1_acquisition": len(sealed_families & fresh),
        "sealed_sha256": corpus_sha256(args.sealed_out),
        "search_sha256": corpus_sha256(args.search_out),
        "families_sha256": hashlib.sha256(
            json.dumps(sorted(sealed_families), separators=(",", ":")).encode()).hexdigest(),
        "historical_sealed_v1": {
            "status": "RETIRED",
            "reason": (
                "evaluated once during the V1 search, exactly as its policy allowed; it is "
                "therefore no longer pristine for a new architecture search"
            ),
        },
        "policy": "read once, after convergence, on the reported finalists only, "
                  "through the isolated sealed evaluator process",
    }
    args.manifest.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
