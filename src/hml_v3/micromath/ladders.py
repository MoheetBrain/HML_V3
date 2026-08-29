"""Difficulty ladders, and the horizon-interaction estimate they exist to support.

`MISSION §15`, `§16`. One average score per component hides the thing `PROJECT_GOAL` actually
predicts: that a representation's advantage should grow with structural complexity, because
that is where a reader's own bookkeeping fails first. A candidate that ties a control at depth
two and beats it at depth sixteen is a far more interesting result than either number alone,
and a flat profile is a real refutation rather than a null.

Rungs are computed from the structure each item already recorded at construction, so a ladder
costs no new items -- only a regrouping of the ones the lab holds.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

from hml_v3.micromath import stresses as S

#: (label, lower, upper) with upper exclusive; the last rung is open-ended.
LADDERS: dict[str, tuple[tuple[str, int, int], ...]] = {
    S.MULTI_GOAL: (("G1", 1, 2), ("G2", 2, 3), ("G3", 3, 5), ("G4", 5, 9),
                   ("G5", 9, 10**9)),
    S.EXPRESSION_DEPTH: (("E1", 0, 3), ("E2", 3, 5), ("E3", 5, 9), ("E4", 9, 17),
                         ("E5", 17, 10**9)),
    S.DEPENDENCY: (("D1", 1, 2), ("D2", 2, 4), ("D3", 4, 8), ("D4", 8, 16),
                   ("D5", 16, 10**9)),
}

#: `MISSION §15` fixes these boundaries, and they are kept as written even though the corpus
#: does not populate all of them: G4 holds one item, G5 and D1-D2 hold none. Re-cutting the
#: rungs after seeing the distribution is the same error `§8` forbids for the calibration
#: rule, so the pre-registered ladder stays primary and the empty rungs are reported as
#: empty. That the corpus contains almost no states with more than four goals is itself a
#: finding: the long-horizon prediction cannot be tested on MULTI_GOAL with this material.
PREREGISTERED_LADDERS = LADDERS

#: A secondary cut taken from the observed distribution, reported separately and clearly
#: marked post-hoc. It exists so the horizon question can be asked at all on EXPRESSION_DEPTH
#: and DEPENDENCY; it may not be used to claim a result the pre-registered ladder did not.
#: EXPRESSION_DEPTH's real difficulty axis turned out to be the LEAD -- how far the deepest
#: reference outranks the runner-up -- not the absolute depth. A one-level lead is the hard
#: case and covers most of the corpus; a large lead is nearly visible. That is a better
#: ladder than absolute depth, and it is available because the lead is recorded per item.
LEAD_LADDER: tuple[tuple[str, int, int], ...] = (
    ("L1", 1, 2), ("L2", 2, 4), ("L3", 4, 8), ("L4", 8, 10**9))

ADAPTED_LADDERS: dict[str, tuple[tuple[str, int, int], ...]] = {
    S.EXPRESSION_DEPTH: (("E*1", 0, 5), ("E*2", 5, 9), ("E*3", 9, 13), ("E*4", 13, 10**9)),
    S.DEPENDENCY: (("D*1", 0, 20), ("D*2", 20, 40), ("D*3", 40, 80), ("D*4", 80, 10**9)),
    S.MULTI_GOAL: (("G*1", 0, 3), ("G*2", 3, 10**9)),
}

#: Which field of ``item.detail`` carries the complexity for each ladder.
MEASURE: dict[str, str] = {
    S.MULTI_GOAL: "goals",
    S.EXPRESSION_DEPTH: "depth",
    S.DEPENDENCY: "edges",
}


def complexity(item: Any) -> int | None:
    field = MEASURE.get(item.stress)
    if field is None:
        return None
    value = (item.detail or {}).get(field)
    return value if isinstance(value, int) else None


def rung(item: Any, ladders: dict[str, tuple] | None = None) -> str | None:
    """Which ladder rung this item sits on, or None if its stress has no ladder."""

    size = complexity(item)
    ladder = (ladders or LADDERS).get(item.stress)
    if size is None or ladder is None:
        return None
    for label, low, high in ladder:
        if low <= size < high:
            return label
    return None


def stratify(items: Sequence[Any],
             ladders: dict[str, tuple] | None = None) -> dict[str, list[Any]]:
    buckets: dict[str, list[Any]] = {}
    for item in items:
        label = rung(item, ladders)
        if label is not None:
            buckets.setdefault(label, []).append(item)
    return buckets


@dataclass
class Slope:
    """A least-squares slope of accuracy against rung index, with its span.

    Reported alongside the per-rung numbers rather than instead of them: with five rungs and
    a dozen items each, a slope is a summary and not an inference, and saying so is part of
    reporting it honestly.
    """

    slope: float
    first: float
    last: float
    rungs: int

    def to_dict(self) -> dict[str, Any]:
        return {"slope_per_rung": round(self.slope, 4), "first_rung": round(self.first, 4),
                "last_rung": round(self.last, 4), "rungs_measured": self.rungs,
                "interpretation": (
                    "positive means the gap widens with complexity, which is the "
                    "long-horizon prediction; a flat slope refutes it for this component")}


def degradation(by_rung: dict[str, float], order: Sequence[str]) -> Slope | None:
    """Least-squares slope of the values against their rung index."""

    points = [(index, by_rung[label]) for index, label in enumerate(order)
              if label in by_rung]
    if len(points) < 2:
        return None
    n = len(points)
    mean_x = sum(x for x, _y in points) / n
    mean_y = sum(y for _x, y in points) / n
    denominator = sum((x - mean_x) ** 2 for x, _y in points)
    if denominator == 0:
        return None
    slope = sum((x - mean_x) * (y - mean_y) for x, y in points) / denominator
    return Slope(slope=slope, first=points[0][1], last=points[-1][1], rungs=n)


def interaction(candidate_by_rung: dict[str, float], control_by_rung: dict[str, float],
                stress: str, ladders: dict[str, tuple] | None = None) -> dict[str, Any]:
    """`MISSION §16`: does the candidate degrade more slowly than the control?

    The quantity of interest is not ``candidate > control`` but the slope of their
    difference. A representation that helps only where the structure is small is not the
    representation this project is trying to find.
    """

    order = [label for label, _low, _high in (ladders or LADDERS).get(stress, ())]
    shared = [label for label in order
              if label in candidate_by_rung and label in control_by_rung]
    delta = {label: candidate_by_rung[label] - control_by_rung[label] for label in shared}
    slope = degradation(delta, order)
    return {
        "stress": stress,
        "rungs": shared,
        "candidate_by_rung": {k: round(candidate_by_rung[k], 4) for k in shared},
        "control_by_rung": {k: round(control_by_rung[k], 4) for k in shared},
        "delta_by_rung": {k: round(v, 4) for k, v in delta.items()},
        "delta_slope": slope.to_dict() if slope else None,
        "verdict": _verdict(slope, len(shared)),
    }


def _verdict(slope: Slope | None, rungs: int) -> str:
    if slope is None or rungs < 3:
        return "INSUFFICIENT_RUNGS"
    if slope.slope > 0.05:
        return "WIDENS_WITH_COMPLEXITY"
    if slope.slope < -0.05:
        return "NARROWS_WITH_COMPLEXITY"
    return "FLAT_NO_HORIZON_INTERACTION"
