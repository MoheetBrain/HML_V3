"""Corruption tests at the semantic layer, not the text layer.

The V1 corruption suite mutated *rendered text*: it deleted indented lines, swapped lines,
and reordered blocks. That measures a syntax family as much as a representation. A block form
with one field per line loses one field when a line is dropped; an S-expression with a whole
record per line loses a whole record. The two are not being asked the same question, so their
detection rates were never comparable.

The corrected architecture applies the corruption once, upstream of every candidate:

    CanonicalMathState M
        -> SemanticMutation mu
        -> corrupted state M'
        -> R_i(M') for every candidate i
        -> each candidate's consistency checker

Every representation sees the *same* semantic defect. What differs is whether its rendering
carries enough structure for the defect to be visible. A candidate that never states
dependency edges genuinely cannot detect a corrupted dependency, and that is the finding.

Each mutation violates a canonical well-formedness invariant, so "detected" has a precise
meaning: reading the rendering back and checking the invariants it exposes reveals the
violation. Text-level robustness remains a separate suite; the two are never mixed.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import copy
import random
from typing import Any, Callable

MutationFn = Callable[[dict[str, Any], random.Random], dict[str, Any] | None]


@dataclass
class MutationResult:
    family: str
    state: dict[str, Any]
    #: The invariant the mutation breaks, in the vocabulary the checker uses.
    broken_invariant: str
    detail: dict[str, Any] = field(default_factory=dict)


def _goals(transition: dict[str, Any], phase: str = "state_before") -> list[dict[str, Any]]:
    return transition[phase]["goals"]


def _all_declarations(transition: dict[str, Any], phase: str = "state_before") -> list[dict[str, Any]]:
    return [
        declaration
        for goal in _goals(transition, phase)
        for declaration in goal["local_context"]
    ]


def _local_references(node: Any, found: list[dict[str, Any]]) -> None:
    if isinstance(node, dict):
        if node.get("node") == "local_reference":
            found.append(node)
        for value in node.values():
            if isinstance(value, (dict, list)):
                _local_references(value, found)
    elif isinstance(node, list):
        for item in node:
            _local_references(item, found)


# ------------------------------------------------------------------------------ mutations


def drop_declaration(transition: dict[str, Any], rng: random.Random) -> MutationResult | None:
    """Remove a declaration that something still references.

    Detectable by any representation whose goal states its context membership, or whose
    expressions name the declaration they use.
    """

    for goal in _goals(transition):
        referenced: list[dict[str, Any]] = []
        _local_references(goal["target"], referenced)
        used = {reference["identity"] for reference in referenced}
        candidates = [
            declaration for declaration in goal["local_context"]
            if declaration["identity"] in used
        ]
        if not candidates:
            continue
        victim = rng.choice(candidates)
        goal["local_context"] = [
            declaration for declaration in goal["local_context"]
            if declaration["identity"] != victim["identity"]
        ]
        return MutationResult(
            "DROP_DECLARATION", transition, "every referenced local identity is declared",
            {"removed": victim["identity"]},
        )
    return None


def alter_binder_target(transition: dict[str, Any], rng: random.Random) -> MutationResult | None:
    """Repoint a use to a different declaration that exists.

    This is the hardest family: the state stays internally *resolvable*, so only a
    representation that restates something about the binder at the use site, or that states
    the dependency edge explicitly, can see it.
    """

    for goal in _goals(transition):
        referenced: list[dict[str, Any]] = []
        _local_references(goal["target"], referenced)
        identities = [declaration["identity"] for declaration in goal["local_context"]]
        if len(identities) < 2 or not referenced:
            continue
        reference = rng.choice(referenced)
        alternatives = [item for item in identities if item != reference["identity"]]
        if not alternatives:
            continue
        original = reference["identity"]
        reference["identity"] = rng.choice(alternatives)
        return MutationResult(
            "ALTER_BINDER_TARGET", transition,
            "a use resolves to the binder that actually introduced it",
            {"from": original, "to": reference["identity"]},
        )
    return None


def swap_goal_identity(transition: dict[str, Any], rng: random.Random) -> MutationResult | None:
    """Exchange two goal identities without exchanging the focus order that names them."""

    goals = _goals(transition)
    if len(goals) < 2:
        return None
    first, second = rng.sample(range(len(goals)), 2)
    goals[first]["identity"], goals[second]["identity"] = (
        goals[second]["identity"], goals[first]["identity"],
    )
    return MutationResult(
        "SWAP_GOAL_IDENTITY", transition, "focus order names the goals that exist",
        {"swapped": [goals[first]["identity"], goals[second]["identity"]]},
    )


def remove_premise_edge(transition: dict[str, Any], rng: random.Random) -> MutationResult | None:
    premises = list(transition["action"]["external_premise_refs"])
    if not premises:
        return None
    victim = rng.choice(premises)
    transition["action"]["external_premise_refs"] = [
        premise for premise in premises if premise != victim
    ]
    return MutationResult(
        "REMOVE_PREMISE_EDGE", transition, "the action cites every premise it uses",
        {"removed": victim},
    )


def change_scope_parent(transition: dict[str, Any], rng: random.Random) -> MutationResult | None:
    """Move a declaration into a different goal's context."""

    goals = _goals(transition)
    donors = [goal for goal in goals if goal["local_context"]]
    if len(goals) < 2 or not donors:
        return None
    donor = rng.choice(donors)
    receivers = [goal for goal in goals if goal is not donor]
    if not receivers:
        return None
    receiver = rng.choice(receivers)
    moved = rng.choice(donor["local_context"])
    donor["local_context"] = [
        declaration for declaration in donor["local_context"]
        if declaration["identity"] != moved["identity"]
    ]
    receiver["local_context"] = list(receiver["local_context"]) + [moved]
    return MutationResult(
        "CHANGE_SCOPE_PARENT", transition, "a declaration belongs to the goal that scopes it",
        {"moved": moved["identity"]},
    )


def alter_type(transition: dict[str, Any], rng: random.Random) -> MutationResult | None:
    """Rewrite a declaration's type head to a different constant."""

    declarations = [
        declaration for declaration in _all_declarations(transition)
        if isinstance(declaration.get("type"), dict)
    ]
    if not declarations:
        return None
    victim = rng.choice(declarations)
    node = victim["type"]
    while node.get("node") == "application":
        node = node["function"]
    if node.get("node") != "symbol":
        return None
    original = node["identity"]
    node["identity"] = original + ".corrupted"
    return MutationResult(
        "ALTER_TYPE", transition, "a declaration's stated type is its real type",
        {"declaration": victim["identity"], "from": original},
    )


def delete_action_argument(transition: dict[str, Any], rng: random.Random) -> MutationResult | None:
    references = [
        reference for reference in transition["action"]["local_context_refs"]
        if reference.get("resolved")
    ]
    if not references:
        return None
    victim = rng.choice(references)
    transition["action"]["local_context_refs"] = [
        reference for reference in transition["action"]["local_context_refs"]
        if reference is not victim
    ]
    return MutationResult(
        "DELETE_ACTION_ARGUMENT", transition, "the action names every local it consumes",
        {"removed": victim.get("canonical_id")},
    )


def corrupt_dependency(transition: dict[str, Any], rng: random.Random) -> MutationResult | None:
    """Repoint an action's local reference at a declaration it does not use."""

    references = [
        reference for reference in transition["action"]["local_context_refs"]
        if reference.get("resolved")
    ]
    identities = [declaration["identity"] for declaration in _all_declarations(transition)]
    if not references or len(identities) < 2:
        return None
    reference = rng.choice(references)
    alternatives = [item for item in identities if item != reference.get("canonical_id")]
    if not alternatives:
        return None
    original = reference.get("canonical_id")
    reference["canonical_id"] = rng.choice(alternatives)
    return MutationResult(
        "CORRUPT_DEPENDENCY", transition, "the action's local edges point at what it uses",
        {"from": original, "to": reference["canonical_id"]},
    )


def change_metavar_assignment(
    transition: dict[str, Any], rng: random.Random,
) -> MutationResult | None:
    metavariables = transition["state_before"]["metavariables"]
    if not metavariables:
        return None
    victim = rng.choice(metavariables)
    victim["assigned"] = not victim["assigned"]
    if not victim["assigned"]:
        victim["assignment"] = None
    return MutationResult(
        "CHANGE_METAVAR_ASSIGNMENT", transition,
        "an obligation is assigned exactly when it carries an assignment",
        {"metavariable": victim["identity"], "now_assigned": victim["assigned"]},
    )


def reorder_goal_focus(transition: dict[str, Any], rng: random.Random) -> MutationResult | None:
    order = transition["state_before"]["focus_order"]
    if len(order) < 2:
        return None
    first, second = rng.sample(range(len(order)), 2)
    order[first], order[second] = order[second], order[first]
    return MutationResult(
        "REORDER_GOAL_FOCUS", transition, "focus order matches the order goals are stated",
        {"positions": [first, second]},
    )


MUTATIONS: dict[str, MutationFn] = {
    "DROP_DECLARATION": drop_declaration,
    "ALTER_BINDER_TARGET": alter_binder_target,
    "SWAP_GOAL_IDENTITY": swap_goal_identity,
    "REMOVE_PREMISE_EDGE": remove_premise_edge,
    "CHANGE_SCOPE_PARENT": change_scope_parent,
    "ALTER_TYPE": alter_type,
    "DELETE_ACTION_ARGUMENT": delete_action_argument,
    "CORRUPT_DEPENDENCY": corrupt_dependency,
    "CHANGE_METAVAR_ASSIGNMENT": change_metavar_assignment,
    "REORDER_GOAL_FOCUS": reorder_goal_focus,
}

FAMILIES = tuple(sorted(MUTATIONS))


def apply_mutation(
    transition: dict[str, Any], family: str, rng: random.Random,
) -> MutationResult | None:
    """Apply one semantic mutation to a deep copy. Returns None when inapplicable.

    Inapplicability is information, not failure: `REORDER_GOAL_FOCUS` cannot apply to a
    single-goal state, and a corpus where it never applies is a corpus that cannot measure
    goal-ordering axes at all.
    """

    return MUTATIONS[family](copy.deepcopy(transition), rng)


def applicability(
    transitions: list[dict[str, Any]], seed: int = 20260828,
) -> dict[str, dict[str, int]]:
    """How often each family can even be applied to this corpus."""

    report: dict[str, dict[str, int]] = {}
    for family in FAMILIES:
        rng = random.Random(seed)
        applied = sum(
            1 for transition in transitions
            if apply_mutation(transition, family, rng) is not None
        )
        report[family] = {
            "applicable": applied,
            "checked": len(transitions),
            "share": round(applied / max(1, len(transitions)), 4),
        }
    return report
