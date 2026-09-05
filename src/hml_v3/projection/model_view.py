"""Layer 2: the ModelView -- what the reasoner is shown, distinct from how it is written.

`MISSION §4` fixes three layers and forbids conflating them again:

    Layer 1  CanonicalMathState      complete mathematical truth, verifier-grounded
    Layer 2  ModelView               the information selected for this reasoning operation
    Layer 3  SurfaceSerialization    how that selection becomes tokens

`D-025` is why this exists. The 42-axis genome searched Layer 3 for 106 generations and
readability was approximately invariant across it, because no axis could change *whether* a
relation reached the page -- only its spelling. A space that cannot vary content cannot
answer the question `PROJECT_GOAL` asks.

**Selectivity is not corruption** (`MISSION §5`). The canonical state remains lossless and
the verifier keeps access to it. A ModelView may omit, summarise or duplicate, exactly as
retrieval, attention and database projection do. What it may never do is fabricate: every
element carries provenance back to a canonical source, and `LosslessRepresentation` and
`SelectiveModelView` are separate types so nothing silently loses the distinction.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable

# ------------------------------------------------------------------- exposure levels

#: The relation is stated as its own record or edge. Reading it requires no inference.
EXPLICIT = "EXPLICIT"
#: The relation is not stated, but is derivable from structure that IS present -- nesting
#: depth, ordering, containment. This is where the old genome lived.
IMPLICIT_RECOVERABLE = "IMPLICIT_RECOVERABLE"
#: Not in the main view; obtainable through a named side view if the reader asks.
RETRIEVAL_REQUIRED = "RETRIEVAL_REQUIRED"
#: Not present in any form. A reader cannot recover it from this view at all.
ABSENT = "ABSENT"

EXPOSURE_LEVELS: tuple[str, ...] = (EXPLICIT, IMPLICIT_RECOVERABLE, RETRIEVAL_REQUIRED, ABSENT)

#: Ordered from most to least available, so an audit can compare two views.
_RANK = {EXPLICIT: 3, IMPLICIT_RECOVERABLE: 2, RETRIEVAL_REQUIRED: 1, ABSENT: 0}


def rank(level: str) -> int:
    return _RANK.get(level, 0)


# ------------------------------------------------------------------- relation kinds

EXPRESSION_PARENT = "EXPRESSION_PARENT"
EXPRESSION_DEPTH = "EXPRESSION_DEPTH"
BINDER_USE = "BINDER_USE"
TERM_TYPE = "TERM_TYPE"
DECLARATION_DEPENDENCY = "DECLARATION_DEPENDENCY"
ACTION_PREMISE = "ACTION_PREMISE"
ACTION_ARGUMENT = "ACTION_ARGUMENT"
ACTION_GOAL = "ACTION_GOAL"
SCOPE_OWNERSHIP = "SCOPE_OWNERSHIP"

RELATIONS: tuple[str, ...] = (
    EXPRESSION_PARENT, EXPRESSION_DEPTH, BINDER_USE, TERM_TYPE, DECLARATION_DEPENDENCY,
    ACTION_PREMISE, ACTION_ARGUMENT, ACTION_GOAL, SCOPE_OWNERSHIP,
)


@dataclass(frozen=True)
class RelationExposure:
    """How one relation is exposed in one view, and on what evidence.

    ``evidence`` names the concrete mechanism -- an edge block, nesting, a retrieval key --
    so the audit reports a fact about the view's structure rather than a claim about it.
    `FM-051` happened because a known-bad was judged by the name of its mutation instead of
    by whether the answer had actually left the page.
    """

    relation: str
    level: str
    evidence: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"relation": self.relation, "level": self.level, "evidence": self.evidence}


# ----------------------------------------------------------------------- the view

@dataclass
class ViewBlock:
    """One addressable region of the view. Blocks are the unit of content selection."""

    kind: str
    #: Rows of (label, value). Values are already resolved to strings or simple scalars;
    #: nothing here is a canonical node, because Layer 2 has already made its selection.
    rows: list[tuple[str, Any]] = field(default_factory=list)
    #: Only set when the block is reachable on demand rather than shown outright.
    retrieval_key: str | None = None

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"kind": self.kind, "rows": [list(r) for r in self.rows]}
        if self.retrieval_key:
            payload["retrieval_key"] = self.retrieval_key
        return payload


@dataclass
class SelectiveModelView:
    """A deliberately partial view of a canonical state, with its exposure declared.

    The name is the contract. A `SelectiveModelView` does NOT promise to reconstruct the
    canonical state -- `MISSION §5` explicitly permits that, because requiring it would make
    content selection impossible and is the mistake that would keep the project inside
    Layer 3 forever. What it promises instead is provenance, determinism and no fabrication.
    """

    label: str
    source_id: str
    blocks: list[ViewBlock] = field(default_factory=list)
    exposure: dict[str, RelationExposure] = field(default_factory=dict)
    provenance: dict[str, Any] = field(default_factory=dict)
    notes: dict[str, Any] = field(default_factory=dict)

    # ------------------------------------------------------------------ construction

    def expose(self, relation: str, level: str, evidence: str = "") -> None:
        if relation not in RELATIONS:
            raise ValueError(f"unknown relation {relation!r}")
        if level not in EXPOSURE_LEVELS:
            raise ValueError(f"unknown exposure level {level!r}")
        self.exposure[relation] = RelationExposure(relation, level, evidence)

    def add(self, block: ViewBlock) -> None:
        self.blocks.append(block)

    # ------------------------------------------------------------------ inspection

    def level_of(self, relation: str) -> str:
        record = self.exposure.get(relation)
        return record.level if record else ABSENT

    def visible_blocks(self) -> list[ViewBlock]:
        return [b for b in self.blocks if b.retrieval_key is None]

    def retrievable_blocks(self) -> list[ViewBlock]:
        return [b for b in self.blocks if b.retrieval_key is not None]

    def row_count(self) -> int:
        return sum(len(b.rows) for b in self.visible_blocks())

    def to_dict(self) -> dict[str, Any]:
        return {
            "label": self.label, "source_id": self.source_id,
            "kind": "SELECTIVE_MODEL_VIEW",
            "blocks": [b.to_dict() for b in self.blocks],
            "exposure": {k: v.to_dict() for k, v in sorted(self.exposure.items())},
            "provenance": self.provenance, "notes": self.notes,
        }


@dataclass
class LosslessRepresentation:
    """A view that carries the whole canonical state, as the old pipeline always did.

    Kept as a separate type so the round-trip gate can continue to apply to exactly the
    thing it was written for. `MISSION §5`: do not delete a gate that would forbid useful
    selective views -- introduce the distinction and record why.
    """

    label: str
    source_id: str
    state: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {"label": self.label, "source_id": self.source_id,
                "kind": "LOSSLESS_REPRESENTATION", "state": self.state}


# ------------------------------------------------------------------------ cost

@dataclass
class ViewCost:
    """`MISSION §19`: a content view can win by dumping everything, so cost is measured.

    Reported alongside every behavioural number and never collapsed into a single scalar --
    `§19` warns against that explicitly, because the trade between exposure and signal is
    the object of study rather than a nuisance to be summarised away.
    """

    blocks: int
    visible_rows: int
    retrievable_rows: int
    characters: int
    explicit_relations: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "blocks": self.blocks, "visible_rows": self.visible_rows,
            "retrievable_rows": self.retrievable_rows, "characters": self.characters,
            "explicit_relations": self.explicit_relations,
        }


def cost_of(view: SelectiveModelView, rendered: str) -> ViewCost:
    return ViewCost(
        blocks=len(view.visible_blocks()),
        visible_rows=view.row_count(),
        retrievable_rows=sum(len(b.rows) for b in view.retrievable_blocks()),
        characters=len(rendered),
        explicit_relations=sum(1 for e in view.exposure.values() if e.level == EXPLICIT),
    )


def exposure_table(views: Iterable[SelectiveModelView]) -> dict[str, dict[str, str]]:
    """``{view label: {relation: level}}`` for the audit and the reports."""

    return {v.label: {r: v.level_of(r) for r in RELATIONS} for v in views}
