"""The mutation library and the meta-designer's proposal interface.

One mutation targets one causal mechanism. A proposal carries a hypothesis, a predicted
mechanism, an expected benefit and a possible downside, and the failure memory can veto it
before any compute is spent.

Crossover is restricted to axis groups so that a child inherits a *coherent* trait set —
recombining single axes across incompatible surfaces mostly produces candidates that fail to
compile, which is expensive and uninformative.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import random
from typing import Any, Sequence

from hml_v3.representation_search.failure_memory import FailureMemory
from hml_v3.representation_search.genome import (
    AXES,
    AXES_BY_NAME,
    RepresentationGenome,
    axes_for_phase,
)


@dataclass
class Hypothesis:
    """A falsifiable claim about why one axis change should move one metric."""

    statement: str
    mechanism: str
    axis: str
    from_value: str
    to_value: str
    predicted_improvement: str
    predicted_cost: str
    target_metric: str
    changed_condition: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "statement": self.statement,
            "mechanism": self.mechanism,
            "axis": self.axis,
            "from_value": self.from_value,
            "to_value": self.to_value,
            "predicted_improvement": self.predicted_improvement,
            "predicted_cost": self.predicted_cost,
            "target_metric": self.target_metric,
            "changed_condition": self.changed_condition,
        }


@dataclass
class Proposal:
    parent_ids: tuple[str, ...]
    genome: RepresentationGenome
    kind: str
    hypothesis: Hypothesis | None
    blocked_reason: str | None = None
    detail: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "parents": list(self.parent_ids),
            "hypothesis": self.hypothesis.to_dict() if self.hypothesis else None,
            "blocked_reason": self.blocked_reason,
            "detail": self.detail,
        }


#: Which metric each axis is expected to move, and by what mechanism. This is the
#: meta-designer's causal model; when a mutation moves the metric in the opposite direction
#: the search records a refuted hypothesis rather than silently keeping the winner.
AXIS_MECHANISM: dict[str, tuple[str, str]] = {
    "context_order": ("binder_use_distance_tokens",
                      "laying a declaration out nearer the site that consumes it shortens "
                      "the span the reader must carry"),
    "graph_serialization": ("max_reference_span_tokens",
                            "the linearization decides how far apart two related records land"),
    "premise_locality": ("premise_to_action_distance_tokens",
                         "a premise stated beside the action it justifies is adjacent to its use"),
    "binder_use_reminder": ("binder_use_distance_tokens",
                            "restating a compact binder identity at the use site removes the "
                            "need to reach back to the binding record"),
    "redundancy_level": ("detect_drop_field",
                         "restated information makes a dropped field inconsistent rather than "
                         "merely absent"),
    "checksum_policy": ("detect_corrupt_identity",
                        "a per-state digest turns any silent alteration into a mismatch"),
    "count_assertions": ("detect_drop_line",
                         "an asserted cardinality makes a missing record detectable"),
    "syntax_family": ("detect_swap_records",
                      "record scaffolding decides whether exchanging two lines is recoverable"),
    "lexicon_register": ("bpe_tokens_per_transition",
                         "role words are emitted once per record, so their length multiplies"),
    "role_word_length": ("bpe_tokens_per_transition", "shorter role words cost fewer pieces"),
    "identity_scheme": ("identifier_fragmentation",
                        "short identities segment into fewer subword pieces than paths"),
    "expression_notation": ("bpe_tokens_per_transition",
                            "notation decides how much punctuation each node costs"),
    "application_style": ("bpe_tokens_per_transition",
                          "a flattened spine emits one head instead of one per application"),
    "shared_subterm_handling": ("bpe_tokens_per_transition",
                                "a repeated maximal subterm is written once instead of n times"),
    "tree_vs_graph_projection": ("max_reference_span_tokens",
                                 "stating a relation as an edge decouples it from nesting depth"),
    "universe_visibility": ("bpe_tokens_per_transition",
                            "trivial universe lists are pure scaffolding"),
    "block_delimiter": ("detect_drop_line", "explicit terminators localise a missing line"),
    "goal_position": ("premise_to_action_distance_tokens",
                      "the goal's position decides how far the action sits from its target"),
    "action_position": ("premise_to_action_distance_tokens",
                        "moving the action moves every distance measured to it"),
    "alpha_normalization": ("bpe_tokens_per_transition",
                            "carrying Lean's display spelling beside the identity doubles the "
                            "identifier budget"),
    "literal_form": ("bpe_tokens_per_transition", "an untagged literal drops its kind word"),
    "const_name_form": ("identifier_fragmentation",
                        "a shorter constant spelling segments into fewer pieces"),
    "list_syntax": ("bpe_tokens_per_transition", "separators are emitted once per element"),
    "field_marker": ("bpe_tokens_per_transition", "the marker is emitted once per field"),
    "identity_sigil": ("identifier_fragmentation",
                       "a sigil makes an identity lexically distinct at a token cost"),
}


def _phase_axes(phase: str | None) -> list[str]:
    if phase is None:
        return [axis.name for axis in AXES]
    return [axis.name for axis in axes_for_phase(phase)]


def single_axis_mutation(
    parent: RepresentationGenome, axis: str, value: str, memory: FailureMemory,
    changed_condition: str | None = None,
) -> Proposal:
    current = parent.get(axis)
    if current == value:
        return Proposal((parent.candidate_id(),), parent, "NO_OP", None,
                        blocked_reason="AXIS_ALREADY_AT_VALUE")
    allowed, reason = memory.may_apply(axis, value, changed_condition)
    metric, mechanism = AXIS_MECHANISM.get(axis, ("bpe_tokens_per_transition",
                                                  "no recorded causal mechanism"))
    hypothesis = Hypothesis(
        statement=f"setting {axis} from {current} to {value} improves {metric}",
        mechanism=mechanism,
        axis=axis, from_value=current, to_value=value,
        predicted_improvement=metric,
        predicted_cost="bpe_tokens_per_transition",
        target_metric=metric,
        changed_condition=changed_condition,
    )
    if not allowed:
        return Proposal((parent.candidate_id(),), parent, "SINGLE_AXIS", hypothesis,
                        blocked_reason=reason)
    child = parent.with_values(**{axis: value})
    child = RepresentationGenome(
        child.resolved(),
        label=f"{parent.label or parent.candidate_id()}+{axis}={value}",
        notes=hypothesis.statement,
        tags=parent.tags,
    )
    return Proposal((parent.candidate_id(),), child, "SINGLE_AXIS", hypothesis,
                    detail={"memory": reason})


def local_neighbourhood(
    parent: RepresentationGenome, memory: FailureMemory, phase: str | None = None,
) -> list[Proposal]:
    """Every single-axis change around one elite, restricted to the active phase."""

    proposals: list[Proposal] = []
    for axis_name in _phase_axes(phase):
        axis = AXES_BY_NAME[axis_name]
        for value in axis.values:
            if value == parent.get(axis_name):
                continue
            proposals.append(single_axis_mutation(parent, axis_name, value, memory))
    return proposals


def group_crossover(
    left: RepresentationGenome, right: RepresentationGenome, groups: Sequence[str],
    rng: random.Random,
) -> Proposal:
    """Take whole axis groups from ``right`` into ``left``.

    Groups rather than individual axes, because a surface's grammar axes only make sense
    together: half of one syntax family and half of another is usually not a language.
    """

    values = dict(left.resolved())
    taken: list[str] = []
    for axis in AXES:
        if axis.group in groups:
            values[axis.name] = right.get(axis.name)
            taken.append(axis.name)
    child = RepresentationGenome(
        values,
        label=f"{left.label or left.candidate_id()}x{right.label or right.candidate_id()}",
        notes=f"crossover taking {sorted(set(groups))} from the second parent",
        tags=("crossover",),
    )
    return Proposal((left.candidate_id(), right.candidate_id()), child, "CROSSOVER", None,
                    detail={"groups": sorted(set(groups)), "axes": taken})


def random_walk(
    parent: RepresentationGenome, memory: FailureMemory, rng: random.Random,
    steps: int = 3, phase: str | None = None,
) -> Proposal:
    """A multi-axis jump, used only to keep the population from collapsing."""

    values = dict(parent.resolved())
    changed: list[str] = []
    candidates = _phase_axes(phase)
    for _ in range(steps):
        axis_name = rng.choice(candidates)
        axis = AXES_BY_NAME[axis_name]
        value = rng.choice([item for item in axis.values if item != values[axis_name]])
        allowed, _reason = memory.may_apply(axis_name, value)
        if not allowed:
            continue
        values[axis_name] = value
        changed.append(f"{axis_name}={value}")
    child = RepresentationGenome(
        values, label=f"walk:{parent.candidate_id()}",
        notes="diversity jump: " + ", ".join(changed), tags=("novelty",),
    )
    return Proposal((parent.candidate_id(),), child, "RANDOM_WALK", None,
                    detail={"changed": changed})


def targeted_proposals(
    parent: RepresentationGenome, weaknesses: Sequence[str], memory: FailureMemory,
    phase: str | None = None,
) -> list[Proposal]:
    """Propose only the axes whose recorded mechanism targets a measured weakness.

    This is what makes the loop a search rather than a sweep: the meta-designer reads the
    failure profile and spends the generation's budget on the axes that could plausibly move
    the metric the elite is worst on.
    """

    wanted = set(weaknesses)
    proposals: list[Proposal] = []
    for axis_name in _phase_axes(phase):
        metric, _mechanism = AXIS_MECHANISM.get(axis_name, (None, ""))
        if metric not in wanted:
            continue
        axis = AXES_BY_NAME[axis_name]
        for value in axis.values:
            if value == parent.get(axis_name):
                continue
            proposals.append(single_axis_mutation(parent, axis_name, value, memory))
    return proposals
