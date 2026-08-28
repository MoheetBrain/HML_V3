"""Pareto selection with diversity preservation.

Selection is multi-objective on purpose. `FM-008` records that the entire token spread across
every prior candidate was 1.4%, so a scalarised objective would have selected on noise.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Sequence

from hml_v3.representation_search.genome import RepresentationGenome
from hml_v3.representation_search.metrics import MAXIMISED, PARETO_AXES


def _oriented(values: dict[str, float], axes: Sequence[str]) -> list[float]:
    """Rewrite every axis so that smaller is better."""

    return [
        -values.get(axis, 0.0) if axis in MAXIMISED else values.get(axis, 0.0)
        for axis in axes
    ]


def dominates(left: dict[str, float], right: dict[str, float],
              axes: Sequence[str] = PARETO_AXES, tolerance: float = 1e-9) -> bool:
    a, b = _oriented(left, axes), _oriented(right, axes)
    no_worse = all(x <= y + tolerance for x, y in zip(a, b))
    strictly_better = any(x < y - tolerance for x, y in zip(a, b))
    return no_worse and strictly_better


def pareto_front(
    population: Sequence[tuple[str, dict[str, float]]], axes: Sequence[str] = PARETO_AXES,
) -> list[str]:
    front: list[str] = []
    for candidate_id, values in population:
        if not any(
            dominates(other_values, values, axes)
            for other_id, other_values in population
            if other_id != candidate_id
        ):
            front.append(candidate_id)
    return front


def non_dominated_sort(
    population: Sequence[tuple[str, dict[str, float]]], axes: Sequence[str] = PARETO_AXES,
) -> list[list[str]]:
    """Rank into successive fronts; front 0 is the Pareto frontier."""

    remaining = list(population)
    fronts: list[list[str]] = []
    while remaining:
        front = pareto_front(remaining, axes)
        if not front:
            fronts.append([candidate_id for candidate_id, _ in remaining])
            break
        fronts.append(front)
        chosen = set(front)
        remaining = [item for item in remaining if item[0] not in chosen]
    return fronts


def crowding_distance(
    population: Sequence[tuple[str, dict[str, float]]], axes: Sequence[str] = PARETO_AXES,
) -> dict[str, float]:
    """NSGA-II crowding: keep the ends of each axis and the sparsest interior points."""

    distances = {candidate_id: 0.0 for candidate_id, _ in population}
    if len(population) <= 2:
        return {candidate_id: float("inf") for candidate_id, _ in population}
    for index, axis in enumerate(axes):
        ordered = sorted(population, key=lambda item: _oriented(item[1], axes)[index])
        low = _oriented(ordered[0][1], axes)[index]
        high = _oriented(ordered[-1][1], axes)[index]
        spread = high - low
        distances[ordered[0][0]] = float("inf")
        distances[ordered[-1][0]] = float("inf")
        if spread <= 0:
            continue
        for position in range(1, len(ordered) - 1):
            previous = _oriented(ordered[position - 1][1], axes)[index]
            following = _oriented(ordered[position + 1][1], axes)[index]
            distances[ordered[position][0]] += (following - previous) / spread
    return distances


@dataclass
class SelectionResult:
    survivors: list[str]
    front: list[str]
    fronts: list[list[str]]
    novelty: dict[str, float]
    crowding: dict[str, float]
    pinned: list[str]


def genome_novelty(
    genomes: dict[str, RepresentationGenome], candidate_ids: Iterable[str],
) -> dict[str, float]:
    """Mean axis-space distance to the rest of the population."""

    ids = list(candidate_ids)
    novelty: dict[str, float] = {}
    for candidate_id in ids:
        others = [other for other in ids if other != candidate_id]
        if not others:
            novelty[candidate_id] = 0.0
            continue
        novelty[candidate_id] = sum(
            genomes[candidate_id].distance(genomes[other]) for other in others
        ) / len(others)
    return novelty


def select(
    population: Sequence[tuple[str, dict[str, float]]],
    genomes: dict[str, RepresentationGenome],
    capacity: int,
    pinned: Sequence[str] = (),
    novelty_slots: int = 3,
    axes: Sequence[str] = PARETO_AXES,
) -> SelectionResult:
    """Elitist selection: pinned baselines, then Pareto fronts, then novelty.

    ``pinned`` implements the `FM-002`/`FM-006` requirement that the recorded baselines stay
    in the population for the whole search even after they fall off the frontier.
    """

    fronts = non_dominated_sort(population, axes)
    crowding = crowding_distance(population, axes)
    novelty = genome_novelty(genomes, [candidate_id for candidate_id, _ in population])

    survivors: list[str] = []
    seen: set[str] = set()
    for candidate_id in pinned:
        if candidate_id in {item[0] for item in population} and candidate_id not in seen:
            survivors.append(candidate_id)
            seen.add(candidate_id)

    for front in fronts:
        ordered = sorted(front, key=lambda cid: (-crowding.get(cid, 0.0), cid))
        for candidate_id in ordered:
            if len(survivors) >= max(0, capacity - novelty_slots):
                break
            if candidate_id not in seen:
                survivors.append(candidate_id)
                seen.add(candidate_id)
        if len(survivors) >= max(0, capacity - novelty_slots):
            break

    remaining = sorted(
        (candidate_id for candidate_id, _ in population if candidate_id not in seen),
        key=lambda cid: (-novelty.get(cid, 0.0), cid),
    )
    for candidate_id in remaining:
        if len(survivors) >= capacity:
            break
        survivors.append(candidate_id)
        seen.add(candidate_id)

    return SelectionResult(
        survivors=survivors,
        front=fronts[0] if fronts else [],
        fronts=fronts,
        novelty=novelty,
        crowding=crowding,
        pinned=list(pinned),
    )


def epsilon_dominates(
    left: dict[str, float], right: dict[str, float], epsilon: float,
    axes: Sequence[str] = PARETO_AXES,
) -> bool:
    """Domination after allowing ``epsilon`` relative slack on every axis.

    Strict non-dominated sorting over seven axes leaves almost everything on the front once
    the population grows: with enough axes, any candidate is best at *something*. That makes
    the strict front correct but uninformative as a shortlist. Epsilon-dominance asks the
    sharper question — is this candidate better by an amount worth caring about? — and is
    used for **reporting finalists only**. Selection continues to use the strict front, so
    the search itself is never biased by the choice of epsilon.
    """

    a, b = _oriented(left, axes), _oriented(right, axes)
    scaled = [value * (1.0 + epsilon) if value > 0 else value * (1.0 - epsilon) for value in a]
    no_worse = all(x <= y for x, y in zip(scaled, b))
    strictly_better = any(x < y for x, y in zip(scaled, b))
    return no_worse and strictly_better


def epsilon_pareto_front(
    population: Sequence[tuple[str, dict[str, float]]], epsilon: float = 0.02,
    axes: Sequence[str] = PARETO_AXES,
) -> list[str]:
    return [
        candidate_id for candidate_id, values in population
        if not any(
            epsilon_dominates(other_values, values, epsilon, axes)
            for other_id, other_values in population
            if other_id != candidate_id
        )
    ]


def frontier_hypervolume(
    population: Sequence[tuple[str, dict[str, float]]], axes: Sequence[str] = PARETO_AXES,
) -> float:
    """A scalar *progress indicator* only: the mean normalised best value per axis.

    It is never used for selection. Its only job is to answer "did this generation move the
    frontier?" for the convergence rule.
    """

    if not population:
        return 0.0
    total = 0.0
    for index, axis in enumerate(axes):
        column = [_oriented(values, axes)[index] for _, values in population]
        low, high = min(column), max(column)
        spread = high - low
        total += 0.0 if spread <= 0 else (high - low) / max(abs(high), abs(low), 1e-9)
    return total / len(axes)


def frontier_signature(
    population: Sequence[tuple[str, dict[str, float]]], axes: Sequence[str] = PARETO_AXES,
) -> tuple[float, ...]:
    """Best value per axis on the whole population; the convergence test compares these."""

    if not population:
        return tuple(0.0 for _ in axes)
    return tuple(
        min(_oriented(values, axes)[index] for _, values in population)
        for index, _ in enumerate(axes)
    )


def metric_signature(values: dict[str, float], axes: Sequence[str] = PARETO_AXES,
                     places: int = 4) -> tuple[float, ...]:
    return tuple(round(value, places) for value in _oriented(values, axes))


def equivalence_classes(
    population: Sequence[tuple[str, dict[str, float]]], axes: Sequence[str] = PARETO_AXES,
) -> dict[tuple[float, ...], list[str]]:
    """Group candidates whose Pareto vectors are identical.

    Two genomes that differ on an axis and measure identically are evidence that the axis has
    no effect *on this corpus*. That is a result, not noise, and it is reported rather than
    hidden by keeping only one representative in the shortlist.
    """

    groups: dict[tuple[float, ...], list[str]] = {}
    for candidate_id, values in population:
        groups.setdefault(metric_signature(values, axes), []).append(candidate_id)
    return {key: sorted(value) for key, value in groups.items()}


def extreme_points(
    population: Sequence[tuple[str, dict[str, float]]], axes: Sequence[str] = PARETO_AXES,
) -> dict[str, str]:
    """The best candidate on each axis taken alone."""

    best: dict[str, str] = {}
    for index, axis in enumerate(axes):
        winner = min(population, key=lambda item: (_oriented(item[1], axes)[index], item[0]))
        best[axis] = winner[0]
    return best


def knee_point(
    population: Sequence[tuple[str, dict[str, float]]], axes: Sequence[str] = PARETO_AXES,
) -> str | None:
    """The candidate closest to the ideal point after per-axis min-max normalisation.

    Not a winner: a compromise. It is reported because a decision-maker asking "which single
    candidate is least bad everywhere?" is asking a different question from "which candidate
    is best on axis k?", and both answers belong in the shortlist.
    """

    if not population:
        return None
    columns = list(zip(*[_oriented(values, axes) for _, values in population]))
    bounds = [(min(column), max(column)) for column in columns]
    best_id, best_distance = None, float("inf")
    for candidate_id, values in population:
        oriented = _oriented(values, axes)
        distance = 0.0
        for value, (low, high) in zip(oriented, bounds):
            spread = high - low
            distance += 0.0 if spread <= 0 else ((value - low) / spread) ** 2
        if distance < best_distance or (distance == best_distance and candidate_id < (best_id or "~")):
            best_id, best_distance = candidate_id, distance
    return best_id


def shortlist(
    population: Sequence[tuple[str, dict[str, float]]], axes: Sequence[str] = PARETO_AXES,
) -> tuple[list[str], dict[str, list[str]]]:
    """The reported finalists: every axis winner plus the knee, deduplicated.

    An epsilon-front is a diagnostic, not a shortlist: at any epsilon small enough to be
    defensible it keeps most of the population, and at any epsilon large enough to cut it
    down the cut is arbitrary. Extreme points plus the knee is a rule that states exactly why
    each finalist is present.
    """

    classes = equivalence_classes(population, axes)
    representatives = {members[0]: members for members in classes.values()}
    deduped = [
        (candidate_id, values) for candidate_id, values in population
        if candidate_id in representatives
    ]
    chosen: dict[str, list[str]] = {}
    for axis, candidate_id in extreme_points(deduped, axes).items():
        chosen.setdefault(candidate_id, []).append(f"best_on:{axis}")
    knee = knee_point(deduped, axes)
    if knee is not None:
        chosen.setdefault(knee, []).append("knee")
    ordered = sorted(chosen, key=lambda cid: (-len(chosen[cid]), cid))
    return ordered, chosen
