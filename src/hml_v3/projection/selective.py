"""SELECTIVE_LOCAL_CONTEXT: keep the structure the question needs, drop the rest.

`REAL_LEAN_GAP_V1 §4`. Every other view in `expression.py` either shows the whole target or
adds a table beside it. This one asks the opposite question: what is the SMALLEST piece of
the state that still answers "which option is referenced deepest", and how much surrounding
structure can be carried before the answer stops arriving.

**The relation fixes the floor.** Depth is distance to the root, so no neighbourhood around a
candidate can answer the question unless it reaches the root. The ladder is therefore built
outward from each candidate's ancestor chain -- radius 0 is the chains alone, radius k adds
every node within k edges of them, and FULL is the entire edge list. That measures what can
be discarded, which is the useful direction: the chains are the irreducible content and
everything else is the surrounding material whose cost is being measured.

**Answer-blindness is structural, not promised.** The chains are built for EVERY option, by
the same code, in a deterministic answer-blind order. Keying the neighbourhood on the correct
option would state the answer in the shape of the view -- the `FM-047` mistake, and the one
`expression.py` names as the hazard for `LOCAL_SUBTREE` and `PATH_TO_ROOT`.
"""

from __future__ import annotations

from typing import Any

from hml_v3.projection import model_view as MV
from hml_v3.projection.model_view import SelectiveModelView, ViewBlock
from hml_v3.projection.synthetic import SyntheticExpression

SELECTIVE_LOCAL_CONTEXT = "SELECTIVE_LOCAL_CONTEXT"

#: ``(label, radius)``. ``None`` means the whole state: every edge, nothing dropped.
RADII: tuple[tuple[str, Any], ...] = (
    ("CHAINS_ONLY", 0),
    ("PARENT_CHILD", 1),
    ("HOP2", 2),
    ("HOP4", 4),
    ("HOP8", 8),
    ("FULL_STATE", None),
)


def _parents(expression: SyntheticExpression) -> dict[str, str]:
    return {child: parent for child, parent in expression.edges}


def _children(expression: SyntheticExpression) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for child, parent in expression.edges:
        out.setdefault(parent, []).append(child)
    return out


def _ancestry(parents: dict[str, str], node_id: str) -> list[str]:
    chain = [node_id]
    seen = {node_id}
    while chain[-1] in parents and parents[chain[-1]] not in seen:
        nxt = parents[chain[-1]]
        chain.append(nxt)
        seen.add(nxt)
    return chain


def occurrence_nodes(expression: SyntheticExpression, identity: str) -> list[str]:
    """Every node carrying this identity, in deterministic order."""

    return sorted(node_id for node_id, name in expression.node_reference.items()
                  if name == identity)


def relevant_nodes(expression: SyntheticExpression, options: list[str]) -> set[str]:
    """The union of every candidate's ancestor chains. The irreducible content."""

    parents = _parents(expression)
    keep: set[str] = set()
    for identity in sorted(options):
        for node_id in occurrence_nodes(expression, identity):
            keep.update(_ancestry(parents, node_id))
    return keep


def selected_nodes(expression: SyntheticExpression, options: list[str],
                   radius: Any) -> set[str]:
    """Chains plus everything within ``radius`` undirected edges of them."""

    all_nodes = {n for edge in expression.edges for n in edge}
    if radius is None:
        return all_nodes
    keep = relevant_nodes(expression, options)
    parents = _parents(expression)
    children = _children(expression)
    frontier = set(keep)
    for _step in range(radius):
        nxt: set[str] = set()
        for node_id in frontier:
            if node_id in parents:
                nxt.add(parents[node_id])
            nxt.update(children.get(node_id, []))
        nxt -= keep
        if not nxt:
            break
        keep |= nxt
        frontier = nxt
    return keep


def build(expression: SyntheticExpression, options: list[str], radius: Any,
          label: str | None = None) -> SelectiveModelView:
    """One selective view at one radius."""

    keep = selected_nodes(expression, options, radius)
    view = SelectiveModelView(
        label=label or f"{SELECTIVE_LOCAL_CONTEXT}@{radius if radius is not None else 'FULL'}",
        source_id=expression.state_id)
    view.provenance = {"generator": expression.to_dict()["generator"],
                       "radius": radius, "origin": "TYPED_GENERATOR"}

    view.add(ViewBlock("context", [
        ("declaration", name) for name in sorted(expression.depth_of)]))
    edges = [(child, parent) for child, parent in expression.edges
             if child in keep and parent in keep]
    view.add(ViewBlock("expression_edges", [
        ("edge", f"{child} -> {parent}") for child, parent in edges]))
    view.add(ViewBlock("node_reference", [
        (node_id, identity) for node_id, identity in sorted(expression.node_reference.items())
        if node_id in keep]))

    view.expose(MV.EXPRESSION_PARENT, MV.EXPLICIT,
                "the retained parent edges are stated individually")
    view.expose(MV.EXPRESSION_DEPTH, MV.IMPLICIT_RECOVERABLE,
                "depth is a path length over the retained edges; still to be counted")
    return view


# --------------------------------------------------------- selective context over the STATE

#: The tree-hop ladder above turns out to be degenerate on dense targets: with four options
#: recurring four times each, the union of their ancestor chains already covers every internal
#: node, so `CHAINS_ONLY` and `FULL_STATE` are the same view and nothing can be dropped. That
#: is a finding about the relation -- depth is a global property, so its relevant set is the
#: whole target -- and it means selective context has to be measured over the material AROUND
#: the target instead. This ladder is nested: each level is the previous one plus one block.
DOCUMENT_LADDER: tuple[tuple[str, int], ...] = (
    ("TARGET_ONLY", 0),
    ("PLUS_DECLARATIONS", 1),
    ("PLUS_REFERENCING_TYPES", 2),
    ("PLUS_STATE_COPIES", 3),
    ("FULL_STATE", 4),
)


def build_document(expression: SyntheticExpression, options: list[str], level: int,
                   full_levels: dict[str, int]) -> SelectiveModelView:
    """The realistic document, truncated to inclusion ``level`` of `DOCUMENT_LADDER`.

    Level 0 shows the goal target and nothing else -- the minimum that can possibly carry the
    answer, since depth is a property of the target alone. Each further level restores one
    kind of surrounding material, in increasing order of how much it competes with the
    question. The answer is unchanged at every level; only what surrounds it moves.
    """

    from hml_v3.projection import clutter as CL
    from hml_v3.projection import realism as RE

    target = expression.transition["state_before"]["goals"][0]["target"]
    rendered_target = CL._render_expression(target)

    view = SelectiveModelView(label=f"SELECTIVE@{level}", source_id=expression.state_id)
    view.provenance = {"generator": expression.to_dict()["generator"],
                       "inclusion_level": level, "origin": "TYPED_GENERATOR"}

    if level >= 1:
        rows: list[tuple[str, Any]] = [
            ("declaration", name) for name in sorted(expression.depth_of)]
        if level >= 2 and full_levels.get(RE.DEEPER_IN_CONTEXT):
            rows += RE.context_rows(
                expression, options,
                deeper_in_context=full_levels[RE.DEEPER_IN_CONTEXT],
                context_size=0)[len(expression.depth_of):]
        if level >= 4 and full_levels.get(RE.CONTEXT_SIZE):
            rows += [("declaration", f"w{40 + slot} : t{slot % 7}")
                     for slot in range(full_levels[RE.CONTEXT_SIZE])]
        view.add(ViewBlock("context", rows))

    view.add(ViewBlock("goal_target", [("expression", rendered_target)]))

    if level >= 3 and full_levels.get(RE.TARGET_COPIES):
        view.add(ViewBlock("elsewhere_in_the_state", [
            (RE.COPY_LABELS[slot % len(RE.COPY_LABELS)], rendered_target)
            for slot in range(full_levels[RE.TARGET_COPIES])]))

    view.expose(MV.EXPRESSION_PARENT, MV.IMPLICIT_RECOVERABLE,
                "parentage is recoverable only by matching brackets")
    view.expose(MV.EXPRESSION_DEPTH, MV.IMPLICIT_RECOVERABLE,
                "depth is recoverable only by counting nesting")
    return view


def preservation(expression: SyntheticExpression, options: list[str],
                 radius: Any) -> dict[str, Any]:
    """How much of the question-relevant structure survives, and how much else is carried."""

    keep = selected_nodes(expression, options, radius)
    needed = relevant_nodes(expression, options)
    all_nodes = {n for edge in expression.edges for n in edge}
    needed_edges = [(c, p) for c, p in expression.edges if c in needed and p in needed]
    kept_needed = [(c, p) for c, p in needed_edges if c in keep and p in keep]
    return {
        "nodes_kept": len(keep), "nodes_total": len(all_nodes),
        "relevant_nodes": len(needed),
        "relevant_edges_preserved": round(
            len(kept_needed) / len(needed_edges), 4) if needed_edges else 1.0,
        "fraction_of_state_exposed": round(len(keep) / len(all_nodes), 4) if all_nodes else 0.0,
    }
