"""Matched counterfactual construction by transposition.

`MICROMATH §5` requires that for every cell two states differ in exactly one semantic
relation while their superficial features stay matched, so that bag-of-words, length, token
count and identifier frequency are uninformative and the answer can only come from
structure.

Every constructor here is a **transposition**: it exchanges two existing things in the state
and adds nothing. That is a stronger guarantee than "matched" -- the multiset of tokens in
the canonical state is *identical* between A and B, because B is a permutation of A. Any
control that reads only counts, frequencies or lengths is therefore at chance by
construction rather than by hope, and `shortcut_controls` verifies that empirically instead
of taking it on trust.

Each constructor returns a :class:`Counterfactual`: the mutated state, the question, the two
options, and the answer under A and under B. Options are always the two transposed entities,
so a matched pair is a 2-alternative forced choice at 50% chance.

**Provenance.** STATE_A is an exact real Lean-derived canonical state. STATE_B is a
structural perturbation of it and is *not* claimed to be a provable Lean proof state; it is
a well-formed CanonicalMathState whose ground-truth relation is known by construction. That
distinction is recorded on every pair and must not be blurred: this benchmark measures
whether a representation lets a reader recover a relation, not whether a state is provable.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Any, Callable

from hml_v3.micromath import stresses as S


@dataclass
class Counterfactual:
    state_b: dict[str, Any]
    question: str
    options: tuple[str, str]
    answer_a: str
    answer_b: str
    relation: str
    detail: dict[str, Any] = field(default_factory=dict)


def _goal(transition: dict[str, Any], index: int = 0) -> dict[str, Any]:
    return transition["state_before"]["goals"][index]


def _constants_in_state(state: dict[str, Any]) -> set[str]:
    """Constant names occurring inside the goals, which every renderer emits."""

    names: set[str] = set()
    for _path, node in S.walk(state.get("goals")):
        if isinstance(node, dict) and node.get("node") == "symbol":
            # The canonical node kind for an external constant is `symbol`, not
            # `constant`. Keying on the wrong name silently found nothing and emptied the
            # PREMISE row of the matrix in all six domains.
            name = node.get("identity") or node.get("name")
            if isinstance(name, str):
                names.add(name)
    return names


def _pick_two(items: list[Any], seed: int) -> tuple[int, int]:
    """Deterministic index pair, spread apart so the transposition is not a local wobble."""

    if len(items) < 2:
        raise ValueError("need two items to transpose")
    first = seed % len(items)
    second = (first + max(1, len(items) // 2)) % len(items)
    if first == second:
        second = (first + 1) % len(items)
    return (first, second) if first < second else (second, first)


# ------------------------------------------------------------------------------- BINDER

def binder(transition: dict[str, Any], seed: int) -> Counterfactual | None:
    """Exchange which declaration two uses in the goal target refer to."""

    state_b = copy.deepcopy(transition)
    refs = S.local_references(_goal(transition).get("target"))
    distinct = {}
    for path, identity in refs:
        distinct.setdefault(identity, path)
    if len(distinct) < 2:
        return None
    identities = sorted(distinct)
    i, j = _pick_two(identities, seed)
    left, right = identities[i], identities[j]
    path_left, path_right = distinct[left], distinct[right]
    goal_b = _goal(state_b)
    S.set_path(goal_b["target"], path_left + ("identity",), right)
    S.set_path(goal_b["target"], path_right + ("identity",), left)
    return Counterfactual(
        state_b=state_b,
        question=("In the goal target, the first use written at reference site 1 (the "
                  "earlier of the two sites below in canonical order) refers to which local "
                  "declaration?"),
        options=(left, right), answer_a=left, answer_b=right,
        relation="use -> binder",
        detail={"site_a": list(path_left), "site_b": list(path_right)},
    )


# --------------------------------------------------------------------------- DEPENDENCY

def dependency(transition: dict[str, Any], seed: int) -> Counterfactual | None:
    """Exchange the declarations that two declaration *types* depend on."""

    state_b = copy.deepcopy(transition)
    context = _goal(transition).get("local_context") or []
    carriers = [
        (index, S.local_references(decl.get("type")))
        for index, decl in enumerate(context)
    ]
    carriers = [(index, refs) for index, refs in carriers if refs]
    if len(carriers) < 2:
        return None
    i, j = _pick_two(carriers, seed)
    (index_left, refs_left), (index_right, refs_right) = carriers[i], carriers[j]
    left, right = refs_left[0][1], refs_right[0][1]
    if left == right:
        return None
    context_b = _goal(state_b)["local_context"]
    S.set_path(context_b[index_left]["type"], refs_left[0][0] + ("identity",), right)
    S.set_path(context_b[index_right]["type"], refs_right[0][0] + ("identity",), left)
    holder = context[index_left]["identity"]
    return Counterfactual(
        state_b=state_b,
        question=(f"The type of local declaration {holder} depends on which local "
                  "declaration at its first reference?"),
        options=(left, right), answer_a=left, answer_b=right,
        relation="declaration type -> dependency",
        detail={"holder": holder, "other": context[index_right]["identity"]},
    )


# --------------------------------------------------------------------------------- TYPE

def type_assignment(transition: dict[str, Any], seed: int) -> Counterfactual | None:
    """Exchange the whole type subtrees of two declarations.

    Both types are present in A and in B, so the set of tokens is untouched; only which
    declaration owns which type changes.
    """

    state_b = copy.deepcopy(transition)
    context = _goal(transition).get("local_context") or []
    if len(context) < 2:
        return None
    i, j = _pick_two(context, seed)
    left_decl, right_decl = context[i], context[j]
    left_type, right_type = left_decl.get("type"), right_decl.get("type")
    if left_type == right_type:
        return None
    context_b = _goal(state_b)["local_context"]
    context_b[i]["type"], context_b[j]["type"] = (
        copy.deepcopy(right_type), copy.deepcopy(left_type))
    left_head, right_head = type_head(left_type), type_head(right_type)
    if left_head == right_head:
        return None
    # Options are the two DECLARATIONS, not the two type descriptors. A descriptor like
    # "sort" or "symbol" is this module's own vocabulary and need not appear in the
    # rendering at all, so a reader was being asked to choose between strings it could not
    # see. Declaration identities are in the text by construction.
    left_id, right_id = left_decl["identity"], right_decl["identity"]
    if left_id == right_id:
        return None
    return Counterfactual(
        state_b=state_b,
        question=(f"Which local declaration has the type whose outermost structure is "
                  f"{left_head}?"),
        options=(left_id, right_id), answer_a=left_id, answer_b=right_id,
        relation="declaration -> type",
        detail={"head_sought": left_head, "other_head": right_head},
    )


def type_head(node: Any) -> str:
    """A short, stable descriptor of a type's outermost structure."""

    if not isinstance(node, dict):
        return "atom"
    kind = node.get("node") or node.get("constructor") or "unknown"
    if kind == "local_reference":
        return f"local_reference:{node.get('identity')}"
    if kind == "constant":
        return f"constant:{node.get('name')}"
    if kind == "application":
        return f"application:{type_head(node.get('function'))}"
    return str(kind)


# -------------------------------------------------------------------------------- SCOPE

def scope(transition: dict[str, Any], seed: int) -> Counterfactual | None:
    """Move one declaration from goal i to goal j and one back: which scope holds which."""

    state_b = copy.deepcopy(transition)
    goals = transition["state_before"]["goals"]
    populated = [k for k, g in enumerate(goals) if (g.get("local_context") or [])]
    if len(populated) < 2:
        return None
    i, j = _pick_two(populated, seed)
    left_goal, right_goal = populated[i], populated[j]
    goals_b = state_b["state_before"]["goals"]
    left_context = goals_b[left_goal]["local_context"]
    right_context = goals_b[right_goal]["local_context"]
    # Sibling goals routinely share a prefix of the ambient context, so the last declaration
    # of each is often literally the same declaration and swapping it is a no-op. Search for
    # a position where the two scopes genuinely differ instead of assuming the tail does.
    position = None
    for index in range(min(len(left_context), len(right_context)) - 1, -1, -1):
        if left_context[index]["identity"] != right_context[index]["identity"]:
            position = index
            break
    if position is None:
        return None
    left_decl, right_decl = left_context[position], right_context[position]
    left_context[position], right_context[position] = right_decl, left_decl
    left_id = goals[left_goal].get("identity") or f"goal{left_goal}"
    right_id = goals[right_goal].get("identity") or f"goal{right_goal}"
    return Counterfactual(
        state_b=state_b,
        question=f"Which goal holds local declaration {left_decl['identity']} in its scope?",
        options=(left_id, right_id), answer_a=left_id, answer_b=right_id,
        relation="declaration -> enclosing goal",
        detail={"moved": left_decl["identity"], "swapped_with": right_decl["identity"]},
    )


# --------------------------------------------------------------------------- MULTI_GOAL

def multi_goal(transition: dict[str, Any], seed: int) -> Counterfactual | None:
    """Exchange which goal the action acts on."""

    state_b = copy.deepcopy(transition)
    goals = transition["state_before"]["goals"]
    if len(goals) < 2:
        return None
    identities = [g.get("identity") or f"goal{k}" for k, g in enumerate(goals)]
    i, j = _pick_two(identities, seed)
    left, right = identities[i], identities[j]
    if left == right:
        return None
    # The focus order is the state's own statement of which goal is acted on.
    order_b = list(state_b["state_before"].get("focus_order") or [])
    if left in order_b and right in order_b:
        a_index, b_index = order_b.index(left), order_b.index(right)
        order_b[a_index], order_b[b_index] = order_b[b_index], order_b[a_index]
    else:
        order_b = [right if item == left else item for item in order_b] or [right]
    state_b["state_before"]["focus_order"] = order_b
    # The goal LIST is deliberately left alone. An earlier version also swapped the two
    # goals' positions, which made "whichever option is written earlier" a perfect rule:
    # the focused goal was always the first one rendered, so the cell scored 1.000 for a
    # control that reads nothing. Only the focus moves now, so position carries no answer.
    return Counterfactual(
        state_b=state_b,
        question="Which goal is the focused goal the action acts on?",
        options=(left, right), answer_a=left, answer_b=right,
        relation="action -> focused goal",
        detail={"focus_order_a": list(transition["state_before"].get("focus_order") or [])},
    )


# --------------------------------------------------------------------- EXPRESSION_DEPTH

def expression_depth(transition: dict[str, Any], seed: int) -> Counterfactual | None:
    """Exchange a shallow reference with the deepest one in the goal target."""

    state_b = copy.deepcopy(transition)
    refs = S.local_references(_goal(transition).get("target"))
    if len(refs) < 2:
        return None
    ordered = sorted(refs, key=lambda item: (len(item[0]), item[0]))
    shallow_path, shallow_id = ordered[0]
    deep_path, deep_id = ordered[-1]
    if shallow_id == deep_id or len(shallow_path) == len(deep_path):
        return None
    goal_b = _goal(state_b)
    S.set_path(goal_b["target"], deep_path + ("identity",), shallow_id)
    S.set_path(goal_b["target"], shallow_path + ("identity",), deep_id)
    return Counterfactual(
        state_b=state_b,
        question="Which local declaration is referenced at the deepest point of the goal target?",
        options=(deep_id, shallow_id), answer_a=deep_id, answer_b=shallow_id,
        relation="deepest reference -> declaration",
        detail={"deep_depth": len(deep_path), "shallow_depth": len(shallow_path)},
    )


# ------------------------------------------------------------------------------ PREMISE

def premise(transition: dict[str, Any], seed: int) -> Counterfactual | None:
    """Exchange a *cited* premise with an uncited external constant.

    The first version of this swapped two premises' positions in the citation list. That was
    an instrument defect: ``projection.semantic_core`` stores
    ``sorted(action.external_premise_refs)``, so the declared contract treats citations as a
    SET and order carries no meaning. Every representation therefore "failed" to preserve
    something the canonical layer says does not exist, and the cell would have reported a
    universal representation weakness that was really a benchmark bug.

    Membership *is* semantic. B cites a constant the state already mentions but the action
    did not use, and stops citing one it did, so the multiset of names in the document is
    unchanged while the cited set genuinely differs.
    """

    cited = list(transition["action"].get("external_premise_refs") or [])
    # The replacement must be a name the rendering already shows for another reason.
    # Drawing it from `elaborated_external_constant_refs` did not: that list is source
    # metadata and no renderer emits it, so the cited premise appeared in A and the
    # replacement only in B, and "whichever option is present" answered the question
    # perfectly without reading anything. Constants occurring inside the goals are rendered.
    available = sorted(_constants_in_state(transition["state_before"]))
    uncited = [name for name in available if name not in set(cited)]
    if not cited or not uncited:
        return None
    kept = sorted(cited)[seed % len(cited)]
    swapped_in = sorted(uncited)[seed % len(uncited)]
    if kept == swapped_in:
        return None

    state_b = copy.deepcopy(transition)
    refs_b = [swapped_in if name == kept else name
              for name in state_b["action"]["external_premise_refs"]]
    state_b["action"]["external_premise_refs"] = refs_b
    constants_b = state_b.setdefault("source_specific_reference", {}).get(
        "elaborated_external_constant_refs")
    if isinstance(constants_b, list):
        # Keep the document's name multiset identical: the constant that entered the
        # citation set leaves the ambient constant list and vice versa.
        state_b["source_specific_reference"]["elaborated_external_constant_refs"] = [
            kept if name == swapped_in else name for name in constants_b]
    used = list((state_b.get("state_delta") or {}).get("external_premises_used") or [])
    if kept in used:
        state_b["state_delta"]["external_premises_used"] = [
            swapped_in if name == kept else name for name in used]
    return Counterfactual(
        state_b=state_b,
        question="Which external premise does the action cite?",
        options=(kept, swapped_in), answer_a=kept, answer_b=swapped_in,
        relation="action -> cited premise set",
        detail={"cited_in_a": kept, "cited_in_b": swapped_in},
    )


# ---------------------------------------------------------------------- ACTION_ARGUMENT

def action_argument(transition: dict[str, Any], seed: int) -> Counterfactual | None:
    """Exchange which local declaration the action takes as an argument.

    Same correction as :func:`premise`. ``semantic_core`` stores
    ``sorted(resolved local_context_refs)``, so argument *position* is not semantic and no
    renderer emitted it -- the original version produced byte-identical renderings for A and
    B and reported that as a universal failure. Which declarations are used **is** semantic,
    so B uses one the action did not and drops one it did.
    """

    refs = list(transition["action"].get("local_context_refs") or [])
    resolved = [r for r in refs if isinstance(r, dict) and r.get("resolved")
                and r.get("canonical_id")]
    if not resolved:
        return None
    goal = _goal(transition)
    context_ids = [d["identity"] for d in (goal.get("local_context") or [])]
    used = {r["canonical_id"] for r in resolved}
    unused = [identity for identity in context_ids if identity not in used]
    if not unused:
        return None
    dropped = sorted(used)[seed % len(used)]
    added = sorted(unused)[seed % len(unused)]
    if dropped == added:
        return None

    state_b = copy.deepcopy(transition)
    for reference in state_b["action"]["local_context_refs"]:
        if isinstance(reference, dict) and reference.get("canonical_id") == dropped:
            reference["canonical_id"] = added
    delta_b = state_b.get("state_delta") or {}
    if isinstance(delta_b.get("local_context_refs_used"), list):
        delta_b["local_context_refs_used"] = [
            added if item == dropped else item
            for item in delta_b["local_context_refs_used"]]
    return Counterfactual(
        state_b=state_b,
        question="Which local declaration does the action use as an argument?",
        options=(dropped, added), answer_a=dropped, answer_b=added,
        relation="action -> used local declarations",
        detail={"used_in_a": dropped, "used_in_b": added},
    )


BUILDERS: dict[str, Callable[[dict[str, Any], int], Counterfactual | None]] = {
    S.BINDER: binder,
    S.SCOPE: scope,
    S.DEPENDENCY: dependency,
    S.TYPE: type_assignment,
    S.MULTI_GOAL: multi_goal,
    S.EXPRESSION_DEPTH: expression_depth,
    S.PREMISE: premise,
    S.ACTION_ARGUMENT: action_argument,
}
