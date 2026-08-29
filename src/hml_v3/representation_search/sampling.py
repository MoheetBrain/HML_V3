"""Structurally stratified sampling of the corpus.

`FM-020` recorded that goal linearization was unmeasurable because the corpus averaged 1.01
goals per state, and `FM-028` recorded that targeted acquisition closed that gap: the V2
search pool reaches twelve goals and is 19.0% multi-goal.

Acquiring the data is not the same as showing it to the search. The controller sampled its
dev, microtest and mutation sets as *prefixes* — ``dev[:28]`` — of a list sorted by
transition id. Measured on the new pool, those prefixes are structurally unrepresentative in
exactly the direction that matters:

===================  ==========  =============  ===============
sample               n           max goals      multi-goal share
===================  ==========  =============  ===============
full dev             717         12             19.0%
``dev[:28]``         28          3              14.3%
``dev[:12]``         12          2              8.3%
===================  ==========  =============  ===============

No prefix up to 128 rows contains a state with more than four goals. A search sampling that
way would have re-derived FM-020 on a corpus that had already fixed it, and the acquisition
campaign would have bought nothing.

This module samples by structural stratum instead. It is deterministic given a seed, so a run
remains exactly reproducible, and it guarantees that every non-empty stratum is represented
however small the sample is.
"""

from __future__ import annotations

import random
from typing import Any, Sequence

#: Goal-count strata. The boundaries are the ones the failure memory argues about: one goal
#: (where ordering is definitionally unmeasurable), two, a working multi-goal range, and the
#: deep states targeted acquisition went and got.
GOAL_STRATA: tuple[tuple[str, int, int], ...] = (
    ("goals_1", 1, 1),
    ("goals_2", 2, 2),
    ("goals_3_5", 3, 5),
    ("goals_6_plus", 6, 10_000),
)


def goal_count(transition: dict[str, Any]) -> int:
    return len(transition["state_before"]["goals"])


def stratum_of(transition: dict[str, Any]) -> str:
    count = goal_count(transition)
    for name, low, high in GOAL_STRATA:
        if low <= count <= high:
            return name
    return "goals_0"


def stratify(transitions: Sequence[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    buckets: dict[str, list[dict[str, Any]]] = {}
    for transition in transitions:
        buckets.setdefault(stratum_of(transition), []).append(transition)
    return buckets


def structural_sample(
    transitions: Sequence[dict[str, Any]], size: int, seed: int = 20260828,
) -> list[dict[str, Any]]:
    """A deterministic sample that preserves the goal-count distribution.

    Allocation is proportional to each stratum's share of the population, with a floor of one
    per non-empty stratum so the deep multi-goal states cannot be rounded out of existence —
    they are 1.5% of the pool, so proportional allocation alone drops them from any sample
    smaller than about 67 rows.

    The floor cannot hold when ``size`` is smaller than the number of non-empty strata. The
    requested size wins there, and the strata retained are the most populous; every sample
    size this search actually uses is comfortably larger than the four goal-count strata.

    The result is sorted by ``transition_id`` so it is stable and diffable, and so that two
    runs with the same seed measure the same rows in the same order.
    """

    if size <= 0 or not transitions:
        return []
    if size >= len(transitions):
        return sorted(transitions, key=lambda row: row["transition_id"])

    buckets = stratify(transitions)
    ordered = [name for name, _low, _high in GOAL_STRATA if buckets.get(name)]
    ordered += sorted(name for name in buckets if name not in ordered)

    if size < len(ordered):
        # Fewer rows than strata: the floor and the requested size cannot both hold. The
        # requested size wins, and the strata kept are the most populous ones. Preserving the
        # rarest instead would return a sample made entirely of exotica and would skew every
        # cost metric measured on it.
        ordered = sorted(ordered, key=lambda name: (-len(buckets[name]), name))[:size]

    total = sum(len(buckets[name]) for name in ordered)
    allocation: dict[str, int] = {}
    for name in ordered:
        share = len(buckets[name]) / total
        allocation[name] = max(1, round(share * size))

    # Proportional rounding plus a floor will not sum to `size`. Correct the difference
    # against the largest strata first, never below the floor of one.
    def trim_or_grow() -> None:
        while sum(allocation.values()) > size:
            candidates = [name for name in ordered if allocation[name] > 1]
            if not candidates:
                break
            biggest = max(candidates, key=lambda name: (allocation[name], name))
            allocation[biggest] -= 1
        while sum(allocation.values()) < size:
            candidates = [
                name for name in ordered if allocation[name] < len(buckets[name])
            ]
            if not candidates:
                break
            biggest = max(
                candidates,
                key=lambda name: (len(buckets[name]) - allocation[name], name),
            )
            allocation[biggest] += 1

    for name in ordered:
        allocation[name] = min(allocation[name], len(buckets[name]))
    trim_or_grow()

    chosen: list[dict[str, Any]] = []
    for name in ordered:
        pool = sorted(buckets[name], key=lambda row: row["transition_id"])
        take = min(allocation[name], len(pool))
        if take <= 0:
            continue
        rng = random.Random(f"{seed}|{name}")
        chosen.extend(rng.sample(pool, take))
    return sorted(chosen, key=lambda row: row["transition_id"])


def profile(transitions: Sequence[dict[str, Any]]) -> dict[str, Any]:
    """What a sample actually contains, so a report can state it rather than assume it."""

    if not transitions:
        return {"n": 0, "mean_goals": 0.0, "max_goals": 0, "multi_goal_share": 0.0,
                "strata": {}}
    counts = [goal_count(row) for row in transitions]
    buckets = stratify(transitions)
    return {
        "n": len(counts),
        "mean_goals": round(sum(counts) / len(counts), 3),
        "max_goals": max(counts),
        "multi_goal_share": round(
            sum(1 for value in counts if value >= 2) / len(counts), 4),
        "strata": {name: len(rows) for name, rows in sorted(buckets.items())},
    }
