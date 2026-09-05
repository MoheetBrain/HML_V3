"""Information-exposure auditing on structured view semantics.

`MISSION §15`. The V2 known-bad set failed because "badness" was inferred from the name of a
mutation: `DELETE_DEPENDENCY_EDGES` sounded like it removed dependency edges and did not, and
the answer was still on the page on 6 of 6 items (`FM-051`). Seven instruments were reported
as blind when they had simply never been tested.

The fix is not a better substring search. A substring check answers "does this token appear",
which is neither necessary nor sufficient: an option can appear in a context block while the
*relation* under test is gone, and a relation can be present while the identity is spelled
differently. This audit reads the view's declared exposure and then **verifies that
declaration against the view's own structure**, so a view cannot claim an exposure it does
not have.

Two questions are answered for every (view, relation) pair:

    declared    what the projection says it exposes
    verified    what the blocks actually contain

A disagreement is an audit failure and the view is not usable until it is resolved.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Sequence

from hml_v3.projection import model_view as MV
from hml_v3.projection.model_view import SelectiveModelView

#: Which block kinds constitute evidence that a relation is stated outright. A relation is
#: only EXPLICIT if some block that carries it is actually present and non-empty.
EXPLICIT_EVIDENCE: dict[str, tuple[str, ...]] = {
    MV.EXPRESSION_PARENT: ("expression_edges", "local_neighbourhood", "ancestry"),
    MV.EXPRESSION_DEPTH: ("ancestry", "depth_table"),
    MV.ACTION_GOAL: ("action_goal_edge", "goals_with_local_action"),
    MV.BINDER_USE: ("binder_use_edges",),
    MV.TERM_TYPE: ("term_type_edges", "context_types"),
    MV.DECLARATION_DEPENDENCY: ("dependency_edges",),
    MV.ACTION_PREMISE: ("action_premise_edges",),
    MV.ACTION_ARGUMENT: ("action_argument_edges",),
    MV.SCOPE_OWNERSHIP: ("scope_edges",),
}

#: Some relations need more than a block being present. ACTION_GOAL is only recoverable from
#: an ``action`` block if that block actually names declarations a reader could trace to a
#: goal; an action naming nothing leaves the relation genuinely ABSENT even though the block
#: exists. Checking kind alone reported a verified known-bad as recoverable.
ROW_REQUIREMENTS: dict[tuple[str, str], Callable[[list], bool]] = {
    (MV.ACTION_GOAL, "action"): lambda rows: any(
        label == "uses" and value for label, value in rows),
}

#: Which block kinds leave a relation recoverable but unstated.
IMPLICIT_EVIDENCE: dict[str, tuple[str, ...]] = {
    MV.EXPRESSION_PARENT: ("goal_target",),
    MV.EXPRESSION_DEPTH: ("goal_target", "expression_edges", "local_neighbourhood"),
    MV.ACTION_GOAL: ("action",),
    MV.BINDER_USE: ("goal_target",),
    MV.TERM_TYPE: ("context",),
    MV.DECLARATION_DEPENDENCY: ("context",),
    MV.ACTION_PREMISE: ("action",),
    MV.ACTION_ARGUMENT: ("action",),
    MV.SCOPE_OWNERSHIP: ("goals",),
}


@dataclass
class RelationAudit:
    relation: str
    declared: str
    verified: str
    agrees: bool
    detail: str

    def to_dict(self) -> dict[str, Any]:
        return {"relation": self.relation, "declared": self.declared,
                "verified": self.verified, "agrees": self.agrees, "detail": self.detail}


def _present(view: SelectiveModelView, kinds: Sequence[str], relation: str = "",
             include_retrievable: bool = False) -> list[str]:
    blocks = view.blocks if include_retrievable else view.visible_blocks()
    out = []
    for block in blocks:
        if block.kind not in kinds or not block.rows:
            continue
        requirement = ROW_REQUIREMENTS.get((relation, block.kind))
        if requirement is not None and not requirement(block.rows):
            continue
        out.append(block.kind)
    return out


def verify_relation(view: SelectiveModelView, relation: str) -> RelationAudit:
    """Check the view's declared exposure of one relation against its actual blocks."""

    declared = view.level_of(relation)
    explicit = _present(view, EXPLICIT_EVIDENCE.get(relation, ()), relation)
    implicit = _present(view, IMPLICIT_EVIDENCE.get(relation, ()), relation)
    retrievable = _present(view, EXPLICIT_EVIDENCE.get(relation, ()), relation,
                           include_retrievable=True)
    retrievable = [k for k in retrievable if k not in explicit]

    if explicit:
        verified = MV.EXPLICIT
        detail = f"stated by block(s) {sorted(set(explicit))}"
    elif retrievable:
        verified = MV.RETRIEVAL_REQUIRED
        detail = f"available only on retrieval from {sorted(set(retrievable))}"
    elif implicit:
        verified = MV.IMPLICIT_RECOVERABLE
        detail = f"recoverable from {sorted(set(implicit))} but not stated"
    else:
        verified = MV.ABSENT
        detail = "no block carries this relation in any form"

    return RelationAudit(relation, declared, verified, declared == verified, detail)


def audit_view(view: SelectiveModelView,
               relations: Sequence[str] = MV.RELATIONS) -> dict[str, Any]:
    audits = [verify_relation(view, relation) for relation in relations
              if relation in view.exposure or view.level_of(relation) != MV.ABSENT]
    disagreements = [a for a in audits if not a.agrees]
    return {
        "view": view.label,
        "source_id": view.source_id,
        "relations": [a.to_dict() for a in audits],
        "disagreements": [a.to_dict() for a in disagreements],
        "status": "PASS" if not disagreements else "FAIL",
    }


def audit_views(views: Sequence[SelectiveModelView]) -> dict[str, Any]:
    reports = [audit_view(v) for v in views]
    failing = [r["view"] for r in reports if r["status"] == "FAIL"]
    return {"views": reports, "failing": failing,
            "status": "PASS" if not failing else "FAIL"}


# ------------------------------------------------------------------ known-bad checking

def answer_is_recoverable(view: SelectiveModelView, relation: str) -> bool:
    """Is the relation available at all, in any form the reader could use?

    `MISSION §14`: a known-bad must actually remove the relation from the ModelView. This is
    the mechanical check that the V2 set never had -- it asks about the RELATION, not about
    whether an answer token happens to appear somewhere on the page.
    """

    return MV.rank(verify_relation(view, relation).verified) >= MV.rank(
        MV.IMPLICIT_RECOVERABLE)


def verify_known_bad(view: SelectiveModelView, relation: str) -> dict[str, Any]:
    """Confirm a known-bad genuinely hides its relation before it is used to judge anything."""

    audit = verify_relation(view, relation)
    hidden = audit.verified == MV.ABSENT
    return {
        "view": view.label, "relation": relation, "verified": audit.verified,
        "hides_the_relation": hidden, "detail": audit.detail,
        "status": "VALID_KNOWN_BAD" if hidden else "DOES_NOT_HIDE_THE_RELATION",
        "note": ("" if hidden else
                 "this representation does not remove the relation, so an instrument that "
                 "fails against it has been slandered rather than tested (FM-051)"),
    }


def exposure_matrix(views: Sequence[SelectiveModelView],
                    relations: Sequence[str] = MV.RELATIONS) -> dict[str, dict[str, str]]:
    """``{view: {relation: verified level}}`` -- the table the reports print."""

    return {v.label: {r: verify_relation(v, r).verified for r in relations
                      if r in v.exposure} for v in views}


def differ_in_content(left: SelectiveModelView, right: SelectiveModelView,
                      relations: Sequence[str] = MV.RELATIONS) -> list[str]:
    """Relations on which two views genuinely differ in exposure.

    Two views that differ nowhere are the same experiment run twice, whatever their labels
    say -- the content-layer analogue of the behavioural duplicate check that caught nine
    invented axes in `FM-033`.
    """

    out = []
    for relation in relations:
        if relation not in left.exposure and relation not in right.exposure:
            continue
        if verify_relation(left, relation).verified != verify_relation(
                right, relation).verified:
            out.append(relation)
    return out
