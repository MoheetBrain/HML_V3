"""Destroy exactly one relation in a canonical state, and nothing else.

This replaces the negative arm that failed. V1 built its negative by prepending a *decoy
answer* to the prompt and leaving the state intact. The relation was still in the text, so
the reader read it and ignored the decoy -- which is why DEPENDENCY, SCOPE, TYPE and PREMISE
all returned negative arms of 0.79 to 0.88 instead of chance (`FM-041`).

`MISSION §7`: the negative control must destroy ONLY the target relation while preserving as
much other information as possible. So the ablation happens in the state, before rendering,
and every representation sees the damage equally.

Each ablation prefers a **derangement over a deletion**. Shuffling which type attaches to
which declaration keeps the token multiset identical and leaves every candidate answer
present and plausible; deleting the types would shorten the rendering and announce that
something is missing. A derangement is used wherever the relation is a mapping between two
existing populations, and deletion only where there is nothing to permute.

If a reader still answers above chance after this, the instrument is not measuring the
relation. That is the whole point, and it is not a statement about any representation.
"""

from __future__ import annotations

import copy
from typing import Any, Callable

from hml_v3.micromath import stresses as S


class AblationFailed(RuntimeError):
    """The relation could not be destroyed without also destroying something else."""


def _derange(count: int, seed: int) -> list[int]:
    """A permutation with no fixed point, so every element genuinely moves."""

    if count < 2:
        raise AblationFailed("a derangement needs at least two elements")
    order = [(index + 1 + seed % max(1, count - 1)) % count for index in range(count)]
    if any(order[i] == i for i in range(count)):
        order = [(index + 1) % count for index in range(count)]
    return order


def _goals(transition: dict[str, Any]) -> list[dict[str, Any]]:
    return transition["state_before"]["goals"]


# ------------------------------------------------------------------------------- TYPE

def type_relation(transition: dict[str, Any], seed: int) -> dict[str, Any]:
    """Permute which type attaches to which declaration.

    Keeps every declaration, every type, and every token. Destroys the term-to-type
    association: after this, "the type of v17" is not recoverable, though every candidate
    type is still present and still plausible for something.
    """

    out = copy.deepcopy(transition)
    context = _goals(out)[0].get("local_context") or []
    if len(context) < 2:
        raise AblationFailed("TYPE ablation needs two declarations")
    types = [copy.deepcopy(d.get("type")) for d in context]
    for index, target in enumerate(_derange(len(context), seed)):
        context[index]["type"] = types[target]
    return out


# ------------------------------------------------------------------------- DEPENDENCY

def dependency_relation(transition: dict[str, Any], seed: int) -> dict[str, Any]:
    """Rewire the local references inside declaration types.

    `MISSION §23`: keep objects, keep types, keep names, keep surrounding state; scramble
    the dependency edge. Every reference still points at a real declaration -- just not the
    one it pointed at -- so the state stays well-formed and the option set stays plausible.
    """

    out = copy.deepcopy(transition)
    context = _goals(out)[0].get("local_context") or []
    sites: list[tuple[int, tuple[Any, ...]]] = []
    targets: list[str] = []
    for index, declaration in enumerate(context):
        for path, identity in S.local_references(declaration.get("type")):
            sites.append((index, path))
            targets.append(identity)
    if len(set(targets)) < 2:
        raise AblationFailed("DEPENDENCY ablation needs two distinct referents")
    order = _derange(len(sites), seed)
    for position, (index, path) in enumerate(sites):
        node = S.get_path(context[index].get("type"), path)
        if isinstance(node, dict):
            node["identity"] = targets[order[position]]
    return out


# ----------------------------------------------------------------------------- BINDER

def binder_relation(transition: dict[str, Any], seed: int) -> dict[str, Any]:
    """Rewire which declaration each use in the goal target refers to."""

    out = copy.deepcopy(transition)
    goal = _goals(out)[0]
    sites = S.local_references(goal.get("target"))
    if len({identity for _p, identity in sites}) < 2:
        raise AblationFailed("BINDER ablation needs two distinct referents in the target")
    identities = [identity for _p, identity in sites]
    order = _derange(len(sites), seed)
    for position, (path, _identity) in enumerate(sites):
        node = S.get_path(goal.get("target"), path)
        if isinstance(node, dict):
            node["identity"] = identities[order[position]]
    return out


# ------------------------------------------------------------------------------ SCOPE

def scope_relation(transition: dict[str, Any], seed: int) -> dict[str, Any]:
    """Move declarations between goals, keeping every declaration and every goal.

    Scope ownership is destroyed; the populations on both sides are unchanged.
    """

    out = copy.deepcopy(transition)
    goals = [g for g in _goals(out) if g.get("local_context")]
    if len(goals) < 2:
        raise AblationFailed("SCOPE ablation needs two populated goals")
    contexts = [list(g["local_context"]) for g in goals]
    order = _derange(len(goals), seed)
    for index, goal in enumerate(goals):
        goal["local_context"] = copy.deepcopy(contexts[order[index]])
    return out


# ---------------------------------------------------------------------------- PREMISE

def premise_relation(transition: dict[str, Any], seed: int,
                     candidates: list[str] | None = None) -> dict[str, Any]:
    """Replace the cited premises with a different plausible selection.

    Deleting the citation would announce its own absence. Substituting other ambient
    symbols keeps a citation present, of the same shape and length, pointing elsewhere.
    """

    out = copy.deepcopy(transition)
    action = out.get("action") or {}
    cited = list(action.get("external_premise_refs") or [])
    if not cited:
        raise AblationFailed("PREMISE ablation needs a citation to destroy")
    pool = [c for c in (candidates or []) if c not in cited]
    if not pool:
        pool = sorted(_ambient(out) - set(cited))
    if not pool:
        raise AblationFailed("PREMISE ablation needs an alternative symbol to cite")
    action["external_premise_refs"] = [pool[(seed + i) % len(pool)] for i in range(len(cited))]
    return out


def _ambient(transition: dict[str, Any]) -> set[str]:
    names: set[str] = set()
    for _path, node in S.walk(transition["state_before"].get("goals")):
        if isinstance(node, dict) and node.get("node") == "symbol":
            name = node.get("identity") or node.get("name")
            if isinstance(name, str):
                names.add(name)
    return names


# -------------------------------------------------------------------- ACTION_ARGUMENT

def action_argument_relation(transition: dict[str, Any], seed: int) -> dict[str, Any]:
    """Rebind the action's arguments to declarations it did not use."""

    out = copy.deepcopy(transition)
    action = out.get("action") or {}
    references = [r for r in (action.get("local_context_refs") or [])
                  if isinstance(r, dict) and r.get("canonical_id")]
    if not references:
        raise AblationFailed("ACTION_ARGUMENT ablation needs a resolved argument")
    declared = [d["identity"] for d in (_goals(out)[0].get("local_context") or [])]
    used = {r["canonical_id"].rsplit(":", 1)[-1] for r in references}
    spare = [d for d in declared if d not in used]
    if not spare:
        raise AblationFailed("ACTION_ARGUMENT ablation needs an unused declaration")
    for index, reference in enumerate(references):
        head = reference["canonical_id"].rsplit(":", 1)[0]
        reference["canonical_id"] = f"{head}:{spare[(seed + index) % len(spare)]}"
    return out


# --------------------------------------------------------------------------- MULTI_GOAL

def multi_goal_relation(transition: dict[str, Any], seed: int) -> dict[str, Any]:
    """Reassign which goal the action acts on by permuting the goal order.

    The goals themselves, their contexts and their targets are untouched; only the
    association between the action and its goal moves.
    """

    out = copy.deepcopy(transition)
    goals = _goals(out)
    if len(goals) < 2:
        raise AblationFailed("MULTI_GOAL ablation needs two goals")
    order = _derange(len(goals), seed)
    out["state_before"]["goals"] = [copy.deepcopy(goals[i]) for i in order]
    return out


# --------------------------------------------------------------------- EXPRESSION_DEPTH

def expression_depth_relation(transition: dict[str, Any], seed: int) -> dict[str, Any]:
    """Permute the positions of the target's local references, destroying relative depth."""

    out = copy.deepcopy(transition)
    goal = _goals(out)[0]
    sites = S.local_references(goal.get("target"))
    if len(sites) < 2:
        raise AblationFailed("EXPRESSION_DEPTH ablation needs two references")
    nodes = [copy.deepcopy(S.get_path(goal.get("target"), path)) for path, _i in sites]
    order = _derange(len(sites), seed)
    for position, (path, _identity) in enumerate(sites):
        S.set_path(goal.get("target"), path, nodes[order[position]])
    return out


ABLATIONS: dict[str, Callable[..., dict[str, Any]]] = {
    S.TYPE: type_relation,
    S.DEPENDENCY: dependency_relation,
    S.BINDER: binder_relation,
    S.SCOPE: scope_relation,
    S.PREMISE: premise_relation,
    S.ACTION_ARGUMENT: action_argument_relation,
    S.MULTI_GOAL: multi_goal_relation,
    S.EXPRESSION_DEPTH: expression_depth_relation,
}


def ablate(stress: str, transition: dict[str, Any], seed: int, **kwargs: Any) -> dict[str, Any]:
    ablation = ABLATIONS.get(stress)
    if ablation is None:
        raise AblationFailed(f"no ablation defined for {stress}")
    return ablation(transition, seed, **kwargs)


def changed(before: dict[str, Any], after: dict[str, Any]) -> bool:
    """Did the ablation actually change the state? A no-op negative arm is a silent lie."""

    import json
    return (json.dumps(before.get("state_before"), sort_keys=True) !=
            json.dumps(after.get("state_before"), sort_keys=True)
            or json.dumps(before.get("action"), sort_keys=True) !=
            json.dumps(after.get("action"), sort_keys=True))
