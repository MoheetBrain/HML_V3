"""The eight structural stresses, and tree walkers over the canonical expression form.

A representation rarely fails because "geometry is bad". It fails because of a mathematical
STRUCTURE -- binders, scope, dependency, type, multiple goals, expression depth, premises,
action arguments -- and that failure then shows up in whichever domains happen to exercise
that structure. The diagnostic unit is therefore ``domain x stress``, never domain alone.
"""

from __future__ import annotations

from typing import Any, Iterator

BINDER = "BINDER"
SCOPE = "SCOPE"
DEPENDENCY = "DEPENDENCY"
TYPE = "TYPE"
MULTI_GOAL = "MULTI_GOAL"
EXPRESSION_DEPTH = "EXPRESSION_DEPTH"
PREMISE = "PREMISE"
ACTION_ARGUMENT = "ACTION_ARGUMENT"

STRESSES: tuple[str, ...] = (
    BINDER, SCOPE, DEPENDENCY, TYPE,
    MULTI_GOAL, EXPRESSION_DEPTH, PREMISE, ACTION_ARGUMENT,
)

#: What each stress asks of a representation, in one line, for the reports.
STRESS_QUESTION: dict[str, str] = {
    BINDER: "which local declaration does a given use in the goal refer to",
    SCOPE: "which goal a given local declaration lives in",
    DEPENDENCY: "which declaration the type of another declaration depends on",
    TYPE: "which type belongs to a given declaration",
    MULTI_GOAL: "which goal the action acts on",
    EXPRESSION_DEPTH: "which reference sits deepest in the goal target",
    PREMISE: "which external premise the action cites",
    ACTION_ARGUMENT: "which local declaration the action uses as an argument",
}


# ----------------------------------------------------------------------------- tree walking

def walk(node: Any, path: tuple[Any, ...] = ()) -> Iterator[tuple[tuple[Any, ...], Any]]:
    """Every subnode with the path that reaches it. Deterministic: dict keys are sorted."""

    yield path, node
    if isinstance(node, dict):
        for key in sorted(node):
            yield from walk(node[key], path + (key,))
    elif isinstance(node, list):
        for index, item in enumerate(node):
            yield from walk(item, path + (index,))


def local_references(node: Any) -> list[tuple[tuple[Any, ...], str]]:
    """``(path, identity)`` for every ``local_reference`` node, in deterministic order."""

    found: list[tuple[tuple[Any, ...], str]] = []
    for path, item in walk(node):
        if isinstance(item, dict) and item.get("node") == "local_reference":
            identity = item.get("identity")
            if isinstance(identity, str):
                found.append((path, identity))
    return found


def depth_of(node: Any) -> int:
    if isinstance(node, dict):
        return 1 + max((depth_of(v) for v in node.values()), default=-1)
    if isinstance(node, list):
        return 1 + max((depth_of(v) for v in node), default=-1)
    return 0


def get_path(root: Any, path: tuple[Any, ...]) -> Any:
    node = root
    for step in path:
        node = node[step]
    return node


def set_path(root: Any, path: tuple[Any, ...], value: Any) -> None:
    node = root
    for step in path[:-1]:
        node = node[step]
    node[path[-1]] = value


# ------------------------------------------------------------------------------ eligibility

def _first_goal(transition: dict[str, Any]) -> dict[str, Any] | None:
    goals = transition["state_before"]["goals"]
    return goals[0] if goals else None


def eligible_stresses(transition: dict[str, Any]) -> set[str]:
    """Which stresses this transition can carry a non-trivial matched pair for.

    A stress is only eligible when the state contains at least two *distinguishable*
    instances of the relation, because the counterfactual is built by transposing two of
    them. One instance cannot be transposed, and a pair built from it would differ from its
    twin by an addition rather than a permutation -- which is exactly the kind of surface
    difference a shortcut can exploit.
    """

    goal = _first_goal(transition)
    if goal is None:
        return set()
    goals = transition["state_before"]["goals"]
    context = goal.get("local_context") or []
    action = transition.get("action") or {}
    ok: set[str] = set()

    target_refs = local_references(goal.get("target"))
    if len({identity for _path, identity in target_refs}) >= 2:
        ok.add(BINDER)
        if len(target_refs) >= 2:
            ok.add(EXPRESSION_DEPTH)
    if len(goals) >= 2:
        # Both need a second goal: a single-goal state has exactly one scope, so "which
        # goal contains D" and "which goal does the action act on" are trivially answerable
        # without reading anything.
        ok.add(MULTI_GOAL)
        # SCOPE needs more than two populated goals: sibling goals from a case split
        # routinely share their entire ambient context, and when every declaration sits in
        # both scopes the question "which goal holds D" has no single answer. Requiring an
        # actual disagreement keeps the eligibility count honest rather than counting cells
        # that will fail at construction.
        populated = [g.get("local_context") or [] for g in goals]
        populated = [c for c in populated if c]
        if len(populated) >= 2 and any(
            left[index]["identity"] != right[index]["identity"]
            for left, right in zip(populated, populated[1:])
            for index in range(min(len(left), len(right)))
        ):
            ok.add(SCOPE)
    typed = [d for d in context if local_references(d.get("type"))]
    if len(typed) >= 2:
        ok.add(DEPENDENCY)
    if len(context) >= 2:
        ok.add(TYPE)
    # Both of these are membership questions, not ordering questions: semantic_core stores
    # each as a sorted set, so a cell built on position would test a distinction the
    # canonical contract declares not to exist.
    cited = set(action.get("external_premise_refs") or [])
    ambient = {
        node.get("identity") or node.get("name")
        for _path, node in walk(transition["state_before"].get("goals"))
        if isinstance(node, dict) and node.get("node") == "symbol"
    }
    ambient.discard(None)
    if cited and (ambient - cited):
        ok.add(PREMISE)
    resolved = {r.get("canonical_id") for r in (action.get("local_context_refs") or [])
                if isinstance(r, dict) and r.get("resolved") and r.get("canonical_id")}
    declared = {d["identity"] for d in (context or [])}
    if resolved and (declared - resolved):
        ok.add(ACTION_ARGUMENT)
    return ok
