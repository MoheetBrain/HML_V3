#!/usr/bin/env python3
"""Build MICROMATH_LAB_V1: one matched counterfactual pair per domain x stress cell."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hml_v3.micromath import counterfactuals as CF  # noqa: E402
from hml_v3.micromath import stresses as S  # noqa: E402
from hml_v3.micromath.corpus import load_base_pool  # noqa: E402
from hml_v3.representation_search.corpus import write_corpus  # noqa: E402
from hml_v3.micromath.domains import DOMAINS, classify  # noqa: E402
from hml_v3.micromath.schema import LAB_VERSION, MicroPair, pair_id, state_digest  # noqa: E402
from hml_v3.micromath.split import split_pairs  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path,
                        default=ROOT / "data/corpus/search_pool_v2.jsonl.gz")
    parser.add_argument("--out", type=Path, default=ROOT / "data/micromath_lab_v1")
    args = parser.parse_args()

    pool, provenance = load_base_pool(args.corpus)

    # Index candidate base states per cell, preferring HIGH domain confidence and richer
    # structure so a cell is filled by the most informative state available to it.
    by_cell: dict[tuple[str, str], list[dict]] = {}
    for row in pool:
        domain, confidence = classify(row)
        if domain not in DOMAINS:
            continue
        for stress in S.eligible_stresses(row):
            by_cell.setdefault((domain, stress), []).append((confidence, row))

    #: A canonical state larger than this renders to more tokens than a local model's
    #: context can hold. Measured: ranking by structural richness alone selected states whose
    #: median LEAN_LIKE rendering was 16,158 pre-tokens, and only 11 of 29 fitted a 16k
    #: window. A benchmark no reader can be run on cannot answer the question the lab exists
    #: to ask, so size is a hard filter and richness only breaks ties beneath it.
    PROBE_BYTE_BUDGET = 60_000

    used_base_states: set[str] = set()

    def rank(entry):
        confidence, row = entry
        goal = row["state_before"]["goals"][0]
        richness = (
            len(goal.get("local_context") or [])
            + len(S.local_references(goal.get("target")))
            + 4 * len(row["state_before"]["goals"])
        )
        size = (row.get("corpus_metadata") or {}).get("canonical_bytes") or 0
        return (
            0 if confidence == "HIGH" else 1,
            # Diversity before everything except domain confidence. Without this the
            # size filter concentrated 45 cells onto 17 base states, nine of which then
            # spanned two splits: MICRO_HIDDEN was sharing mathematics with MICRO_DEV, so
            # it could not have measured generalisation to unseen states.
            1 if row["transition_id"] in used_base_states else 0,
            0 if size and size <= PROBE_BYTE_BUDGET else 1,
            size,
            -richness,
            row["transition_id"],
        )

    pairs: list[MicroPair] = []
    unpopulated: list[dict] = []
    for domain in DOMAINS:
        for stress in S.STRESSES:
            candidates = sorted(by_cell.get((domain, stress), []), key=rank)
            built = None
            for seed, (confidence, row) in enumerate(candidates[:24]):
                counterfactual = CF.BUILDERS[stress](row, seed + 1)
                if counterfactual is None:
                    continue
                if state_digest(row) == state_digest(counterfactual.state_b):
                    continue  # the transposition was a no-op; not a usable pair
                identifier = pair_id(domain, stress, row["transition_id"])
                # Balance which side of the pair carries the first option.
                #
                # Every builder returns options=(answer_a, answer_b), so without this the
                # correct answer for STATE_A is always the option listed first. Any feature
                # that tells A from B -- and for a representation whose layout depends on
                # the transposed relation, line count alone does -- then yields the answer
                # without reading anything. Flipping half the pairs by a hash of the pair id
                # breaks that link while keeping the assignment reproducible and independent
                # of any result.
                flip = int(hashlib.sha256(identifier.encode()).hexdigest()[:8], 16) % 2 == 1
                options = counterfactual.options
                if flip:
                    options = (options[1], options[0])
                built = MicroPair(
                    pair_id=identifier,
                    domain=domain, domain_confidence=confidence, stress=stress,
                    base_transition_id=row["transition_id"],
                    source_file=(row["corpus_metadata"] or {}).get("source_file", ""),
                    question=counterfactual.question, options=options,
                    answer_a=counterfactual.answer_a, answer_b=counterfactual.answer_b,
                    relation=counterfactual.relation,
                    state_a=row, state_b=counterfactual.state_b,
                    detail={**counterfactual.detail,
                            "options_flipped": flip},
                )
                break
            if built is None:
                unpopulated.append({
                    "domain": domain, "stress": stress,
                    "candidate_base_states": len(candidates),
                    "reason": ("NO_ELIGIBLE_BASE_STATE" if not candidates
                               else "NO_VALID_TRANSPOSITION_AMONG_CANDIDATES"),
                })
            else:
                pairs.append(built)
                used_base_states.add(built.base_transition_id)

    split = split_pairs(pairs)
    args.out.mkdir(parents=True, exist_ok=True)
    # Written as size-capped gzip shards through the same helper the corpus uses. A single
    # micro_dev.jsonl is 5.7 MB of canonical states, over the commit guard's per-file cap.
    for name, items in (("micro_dev", split.dev), ("micro_shadow", split.shadow),
                        ("micro_hidden", split.hidden)):
        for stale in args.out.glob(f"{name}.jsonl"):
            stale.unlink()
        write_corpus((item.to_dict() for item in items),
                     args.out / f"{name}.jsonl.gz")

    manifest = {
        "lab_version": LAB_VERSION,
        "distinct_base_states": len({p.base_transition_id for p in pairs}),
        "provenance": provenance,
        "cells_total": len(DOMAINS) * len(S.STRESSES),
        "cells_populated": len(pairs),
        "cells_unpopulated": unpopulated,
        "pairs": len(pairs),
        "states": 2 * len(pairs),
        "domains": list(DOMAINS),
        "stresses": list(S.STRESSES),
        "domain_confidence": {
            level: sum(1 for p in pairs if p.domain_confidence == level)
            for level in sorted({p.domain_confidence for p in pairs})
        },
        "split": split.manifest(),
    }
    (args.out / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: v for k, v in manifest.items() if k != "split"}, indent=2))
    print(json.dumps(manifest["split"]["counts"], indent=2))


if __name__ == "__main__":
    main()
