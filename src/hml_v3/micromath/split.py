"""Pair-level splitting of the lab.

`MICROMATH §7`: the microbenchmark can overfit like anything else, so it is split -- but by
PAIR, never by individual state. Splitting states would put A in dev and B in shadow, and
since B is a transposition of A that leaks the answer completely.

MICRO_DEV allows item-level inspection by the meta-designers. MICRO_SHADOW exposes only
aggregates to the mutation loop. MICRO_HIDDEN is not read during optimisation at all.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Iterable

SPLIT_KEY = "hml-v3-micromath-lab-v1"
DEV, SHADOW, HIDDEN = "MICRO_DEV", "MICRO_SHADOW", "MICRO_HIDDEN"
#: 24 / 12 / 12 pairs at a full 48-cell lab.
TARGET_SHARES = {DEV: 0.50, SHADOW: 0.25, HIDDEN: 0.25}


def bucket(pair_id: str) -> float:
    digest = hashlib.sha256(f"{SPLIT_KEY}|{pair_id}".encode()).hexdigest()
    return int(digest[:16], 16) / float(1 << 64)


def assign(pair_id: str) -> str:
    position = bucket(pair_id)
    if position < TARGET_SHARES[DEV]:
        return DEV
    if position < TARGET_SHARES[DEV] + TARGET_SHARES[SHADOW]:
        return SHADOW
    return HIDDEN


@dataclass
class LabSplit:
    dev: list[Any]
    shadow: list[Any]
    hidden: list[Any]

    def manifest(self) -> dict[str, Any]:
        def digest(pairs: list[Any]) -> str:
            payload = json.dumps(sorted(p.pair_id for p in pairs), separators=(",", ":"))
            return hashlib.sha256(payload.encode()).hexdigest()

        def balance(pairs: list[Any]) -> dict[str, dict[str, int]]:
            domains: dict[str, int] = {}
            stresses: dict[str, int] = {}
            for item in pairs:
                domains[item.domain] = domains.get(item.domain, 0) + 1
                stresses[item.stress] = stresses.get(item.stress, 0) + 1
            return {"by_domain": dict(sorted(domains.items())),
                    "by_stress": dict(sorted(stresses.items()))}

        return {
            "split_key": SPLIT_KEY,
            "unit": "MATCHED_PAIR",
            "target_shares": TARGET_SHARES,
            "counts": {
                DEV: len(self.dev), SHADOW: len(self.shadow), HIDDEN: len(self.hidden)},
            "states": {
                DEV: 2 * len(self.dev), SHADOW: 2 * len(self.shadow),
                HIDDEN: 2 * len(self.hidden)},
            "pair_id_sha256": {
                DEV: digest(self.dev), SHADOW: digest(self.shadow),
                HIDDEN: digest(self.hidden)},
            "balance": {
                DEV: balance(self.dev), SHADOW: balance(self.shadow),
                HIDDEN: balance(self.hidden)},
        }


#: Deterministic 4-slot cycle realising 50/25/25 within each stratum.
_CYCLE = (DEV, DEV, SHADOW, HIDDEN)


def split_pairs(pairs: Iterable[Any]) -> LabSplit:
    """Stratify by stress, then assign deterministically inside each stratum.

    A plain keyed hash over 45 pairs is lumpy: it produced 27/6/12, and a MICRO_SHADOW of
    six pairs cannot cover eight structural stresses, so the shadow check -- the thing that
    decides whether a targeted improvement generalises -- would have been blind to most of
    the matrix. Stratifying by stress keeps every split able to speak about every structure
    while the *order within a stratum* stays hash-driven, so the assignment is still
    reproducible from the pair ids alone and carries no knowledge of any result.
    """

    buckets: dict[str, list[Any]] = {DEV: [], SHADOW: [], HIDDEN: []}
    # Any pairs that happen to share a base state move together. A pair's two arms are the
    # same mathematics, so a base state appearing in both MICRO_DEV and MICRO_HIDDEN would
    # leave the hidden split measuring generalisation to states it had already shown.
    assigned_base: dict[str, str] = {}
    by_stress: dict[str, list[Any]] = {}
    for pair in pairs:
        by_stress.setdefault(pair.stress, []).append(pair)
    for stress in sorted(by_stress):
        ordered = sorted(by_stress[stress], key=lambda item: bucket(item.pair_id))
        for index, pair in enumerate(ordered):
            target = assigned_base.get(pair.base_transition_id)
            if target is None:
                target = _CYCLE[index % len(_CYCLE)]
                assigned_base[pair.base_transition_id] = target
            buckets[target].append(pair)
    for items in buckets.values():
        items.sort(key=lambda item: item.pair_id)
    return LabSplit(buckets[DEV], buckets[SHADOW], buckets[HIDDEN])
