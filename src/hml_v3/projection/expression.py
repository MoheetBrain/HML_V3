"""Content-bearing projections of expression structure.

`MISSION §9`, `§10`. Expression depth is the clearest live target the project has: the reader
scores 1.000 when told the answer and 0.167 -- chance -- reading either the discovered
representation or a typed AST, on an instrument with a floor of 0.083. Everything needed is
on the page and nothing surfaces it.

Six views, differing in **what structural information is exposed**, not in punctuation. All
six are written by the single frozen serializer, so any behavioural difference between them
is a content difference by construction.

**A hazard worth naming.** `LOCAL_SUBTREE` and `PATH_TO_ROOT` are built per *candidate*, never
per *answer*. Keying either on the correct declaration would smuggle the answer into the view
and turn an intervention into a positive control wearing a disguise -- the same class of
error as `FM-047`. Every candidate gets identical treatment; the reader still has to compare.

`PATH_TO_ROOT` in particular comes close to *computing* the answer: materialising each
candidate's ancestry means depth can be read off by counting rows. That is a legitimate
intervention -- it exposes information rather than stating a conclusion -- but it is the most
expensive one here, and its cost is reported beside its accuracy so the trade is visible
(`§19`, `§20`).
"""

from __future__ import annotations

from typing import Any

from hml_v3.projection import model_view as MV
from hml_v3.projection.model_view import SelectiveModelView, ViewBlock
from hml_v3.projection.synthetic import SyntheticExpression

NESTED_ONLY = "NESTED_ONLY"
EXPLICIT_EDGE_LIST = "EXPLICIT_EDGE_LIST"
LOCAL_SUBTREE = "LOCAL_SUBTREE"
DUAL_VIEW = "DUAL_VIEW"
PATH_TO_ROOT = "PATH_TO_ROOT"
DEPTH_ADAPTIVE = "DEPTH_ADAPTIVE"
FLATTENED_BAG = "FLATTENED_BAG"

VIEWS: tuple[str, ...] = (
    NESTED_ONLY, EXPLICIT_EDGE_LIST, LOCAL_SUBTREE, DUAL_VIEW, PATH_TO_ROOT,
    DEPTH_ADAPTIVE, FLATTENED_BAG,
)

#: `MISSION §10 F`: below this depth the adaptive view stays compact; at or above it the
#: view spends tokens on explicit relational structure.
ADAPTIVE_THRESHOLD = 5


def _nested_text(node: Any) -> str:
    """The conventional rendering: structure recoverable only from nesting."""

    if not isinstance(node, dict):
        return str(node)
    kind = node.get("node")
    if kind == "local_reference":
        return str(node.get("identity"))
    if kind == "symbol":
        return str(node.get("identity"))
    if kind == "application":
        return f"({_nested_text(node.get('function'))} {_nested_text(node.get('argument'))})"
    return str(node.get("identity") or kind)


def _context_block(expression: SyntheticExpression) -> ViewBlock:
    goal = expression.transition["state_before"]["goals"][0]
    rows = [("declaration", d["identity"]) for d in goal.get("local_context") or []]
    return ViewBlock("context", rows)


def _parent_of(expression: SyntheticExpression) -> dict[str, str]:
    return {child: parent for child, parent in expression.edges}


def _ancestry(expression: SyntheticExpression, node_id: str) -> list[str]:
    parent = _parent_of(expression)
    chain = [node_id]
    seen = {node_id}
    while chain[-1] in parent and parent[chain[-1]] not in seen:
        nxt = parent[chain[-1]]
        chain.append(nxt)
        seen.add(nxt)
    return chain


def _candidates(expression: SyntheticExpression, options: list[str]) -> list[tuple[str, str]]:
    """``(identity, node id)`` for EVERY occurrence of each option, answer-blind.

    The first version kept one node id per identity (``setdefault`` over the sorted node
    reference map). On the clean ladder that is exact -- every identity occurs exactly once --
    but on a dense target where an identity occurs at depths 11, 9, 9 and 8 it silently picked
    an arbitrary occurrence, so `LOCAL_SUBTREE` and `PATH_TO_ROOT` described a reference the
    question was not about and could not answer it at all. Judging those views in the hard
    regime on that basis would have been `FM-051` a second time: reporting a view as
    unreadable when the view BUILDER, not the view, was broken.

    Every occurrence of every option is now listed, which is both correct and answer-blind --
    the reader still has to compare maxima across the occurrences it is shown.

    **The row order is the option order, and that is load-bearing.** Sorting the rows by node
    id instead would put the answer first on every item: the generators build the target's
    deepest occurrence first, so it always holds ``n1``. The option order is already a
    rotation keyed on the state id and carries nothing about which option is correct, so it
    is the ordering used here; occurrences within one option are ordered by node id.
    """

    by_identity: dict[str, list[str]] = {}
    for node_id, identity in expression.node_reference.items():
        by_identity.setdefault(identity, []).append(node_id)
    return [(identity, node_id)
            for identity in options
            for node_id in sorted(by_identity.get(identity, []),
                                  key=lambda n: (len(n), n))]


# ----------------------------------------------------------------------------- views

def build(view: str, expression: SyntheticExpression,
          options: list[str]) -> SelectiveModelView:
    """Project one synthetic state into one ModelView. Options are the offered answers."""

    goal = expression.transition["state_before"]["goals"][0]
    out = SelectiveModelView(label=view, source_id=expression.state_id)
    out.provenance = {"generator": expression.to_dict()["generator"],
                      "rung": expression.rung, "depth": expression.depth,
                      "origin": "TYPED_GENERATOR"}
    out.add(_context_block(expression))

    nested = ViewBlock("goal_target", [("expression", _nested_text(goal.get("target")))])
    edges = ViewBlock("expression_edges", [
        ("edge", f"{child} -> {parent}") for child, parent in expression.edges])
    carriers = ViewBlock("node_reference", [
        (node_id, identity)
        for node_id, identity in sorted(expression.node_reference.items())])

    if view == NESTED_ONLY:
        out.add(nested)
        out.expose(MV.EXPRESSION_PARENT, MV.IMPLICIT_RECOVERABLE,
                   "parentage is recoverable only by matching brackets")
        out.expose(MV.EXPRESSION_DEPTH, MV.IMPLICIT_RECOVERABLE,
                   "depth is recoverable only by counting nesting")

    elif view == EXPLICIT_EDGE_LIST:
        out.add(edges)
        out.add(carriers)
        out.expose(MV.EXPRESSION_PARENT, MV.EXPLICIT, "every parent stated as its own edge")
        out.expose(MV.EXPRESSION_DEPTH, MV.IMPLICIT_RECOVERABLE,
                   "depth is a path length over stated edges; still to be computed")

    elif view == LOCAL_SUBTREE:
        out.add(nested)
        rows: list[tuple[str, Any]] = []
        parent = _parent_of(expression)
        children: dict[str, list[str]] = {}
        for child, up in expression.edges:
            children.setdefault(up, []).append(child)
        for identity, node_id in _candidates(expression, options):
            up = parent.get(node_id)
            rows.append((f"{identity}@{node_id}", {
                "parent": up, "grandparent": parent.get(up) if up else None,
                "siblings": sorted(c for c in children.get(up, []) if c != node_id),
                "children": sorted(children.get(node_id, [])),
            }))
        out.add(ViewBlock("local_neighbourhood", rows))
        out.expose(MV.EXPRESSION_PARENT, MV.EXPLICIT,
                   "each candidate's parent, grandparent and siblings are stated")
        out.expose(MV.EXPRESSION_DEPTH, MV.IMPLICIT_RECOVERABLE,
                   "local structure only; absolute depth is not given")

    elif view == DUAL_VIEW:
        out.add(nested)
        out.add(edges)
        out.add(carriers)
        out.expose(MV.EXPRESSION_PARENT, MV.EXPLICIT,
                   "nested form and an explicit edge table, both present")
        out.expose(MV.EXPRESSION_DEPTH, MV.IMPLICIT_RECOVERABLE,
                   "two independent routes to depth, neither of them stated")

    elif view == PATH_TO_ROOT:
        rows = []
        for identity, node_id in _candidates(expression, options):
            chain = _ancestry(expression, node_id)
            # Labelled by occurrence, not by identity: a dense target has several
            # occurrences of the same identity and they have different ancestries.
            rows.append((f"{identity}@{node_id}", " -> ".join(chain)))
        out.add(ViewBlock("ancestry", rows))
        out.expose(MV.EXPRESSION_PARENT, MV.EXPLICIT, "the full ancestor chain is stated")
        out.expose(MV.EXPRESSION_DEPTH, MV.EXPLICIT,
                   "depth is the length of a stated chain; countable without inference")

    elif view == DEPTH_ADAPTIVE:
        out.add(nested)
        if expression.depth >= ADAPTIVE_THRESHOLD:
            out.add(edges)
            out.add(carriers)
            out.expose(MV.EXPRESSION_PARENT, MV.EXPLICIT,
                       f"depth {expression.depth} >= {ADAPTIVE_THRESHOLD}: edges materialised")
        else:
            out.expose(MV.EXPRESSION_PARENT, MV.IMPLICIT_RECOVERABLE,
                       f"depth {expression.depth} < {ADAPTIVE_THRESHOLD}: nesting only")
        out.expose(MV.EXPRESSION_DEPTH, MV.IMPLICIT_RECOVERABLE,
                   "depth is never stated outright in either regime")
        out.notes["regime"] = ("EXPLICIT" if expression.depth >= ADAPTIVE_THRESHOLD
                               else "COMPACT")

    elif view == FLATTENED_BAG:
        # `MISSION §14`: a true known-bad. Parentage is genuinely gone -- the references are
        # present as an unordered bag with no structure relating them.
        out.add(ViewBlock("references_unordered", [
            ("reference", identity)
            for identity in sorted(set(expression.node_reference.values()))]))
        out.expose(MV.EXPRESSION_PARENT, MV.ABSENT, "no parentage of any kind is present")
        out.expose(MV.EXPRESSION_DEPTH, MV.ABSENT, "no ordering or nesting survives")

    else:
        raise ValueError(f"unknown view {view!r}")

    return out


def question(options: list[str]) -> tuple[str, tuple[str, ...]]:
    return ("Which of these declarations is referenced at the greatest nesting depth in the "
            "goal target?", tuple(options))


def options_for(expression: SyntheticExpression, want: int = 4) -> list[str]:
    """The answer plus the next-deepest distractors, in a deterministic answer-blind order.

    Distractors are the references that genuinely appear in the target, so no option can be
    eliminated by noticing it is absent -- the mistake that made several V2 known-bads
    meaningless. The presented order is rotated on the state id so position carries nothing.
    """

    ranked = sorted(expression.depth_of.items(), key=lambda kv: (-kv[1], kv[0]))
    chosen = [identity for identity, _d in ranked[:max(2, want)]]
    if expression.deepest not in chosen:
        chosen = [expression.deepest, *chosen[: max(1, want - 1)]]
    ordered = sorted(set(chosen))
    spin = sum(ord(c) for c in expression.state_id) % len(ordered)
    return ordered[spin:] + ordered[:spin]
