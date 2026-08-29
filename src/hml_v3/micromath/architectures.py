"""Architectural hypotheses, and the known-bad representations that test the tests.

Two populations live here, and they exist for opposite reasons.

**Architectures** (`MISSION §13`, `§14`). The seven mutations tried in V1 were cosmetic --
delimiters, sigils, field markers, serialisation order, JSON-vs-bespoke. Five ran on valid
instruments and moved a combined 0.031, so surface syntax is refuted as a lever on structural
readability. What remains untested is whether *exposing a different structure* moves it. Each
architecture below names a causal hypothesis, the axes that realise it, a prediction, and the
observation that would falsify it. They are hypotheses, not improvements.

**Known-bad representations** (`MISSION §27`). A valid instrument must detect a representation
that deliberately hides the relation it measures. If DELETE_DEPENDENCY_EDGES scores as well as
the candidate on the DEPENDENCY instrument, that instrument cannot see dependencies, and its
verdict about any real representation is worthless. This is the mutation test for the
benchmark itself, and it is the reason a clean calibration is necessary but not sufficient.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from hml_v3.micromath import stresses as S
from hml_v3.representation_search.compiler import build
from hml_v3.representation_search.genome import AXES_BY_NAME, RepresentationGenome
from hml_v3.representation_search.seeds import SEEDS


@dataclass
class Architecture:
    label: str
    stress: str
    hypothesis: str
    axes: dict[str, str]
    prediction: str
    falsifier: str
    cost: str

    def genome(self, base: RepresentationGenome) -> RepresentationGenome:
        return base.with_values(**self.axes)

    def to_dict(self) -> dict[str, Any]:
        return {"label": self.label, "stress": self.stress, "hypothesis": self.hypothesis,
                "axes": self.axes, "prediction": self.prediction,
                "falsifier": self.falsifier, "cost": self.cost}


# ------------------------------------------------------------------------ GOAL STRUCTURE
# These four were written against MULTI_GOAL, which is now withdrawn: the action-to-goal
# relation is rendered by no axis at all (`FM-044`), so no mutation of the representation
# could have moved it and testing them there would have measured nothing.
#
# They are not discarded, because what they actually attack is **goal structure** -- making
# ownership explicit, keeping a goal's material contiguous, repeating a goal tag where it is
# used. SCOPE asks which goal holds a given declaration, is a live instrument, and is exactly
# the relation these changes are designed to expose. So they are evaluated there.
#
# One of them, G_EXPLICIT_SCOPE_IDS, is the closest legal analogue of the explicit positive
# control for this family, and is the single most direct test of whether stating goal
# ownership -- rather than leaving it to nesting -- is what a reader needs.

GOAL_STRUCTURE_ARCHITECTURES: tuple[Architecture, ...] = (
    Architecture(
        label="G_INTERLEAVED_PER_GOAL",
        stress=S.SCOPE,
        hypothesis=(
            "the action-to-goal link is unreadable because the state is serialised as one "
            "flat before/after block, so a goal and the action that touches it are far "
            "apart in the token stream; interleaving by goal puts each goal next to its own "
            "material and makes the link local"),
        axes={"state_partitioning": "INTERLEAVED_BY_GOAL",
              "action_position": "HEADER"},
        prediction="SCOPE accuracy rises materially above the control",
        falsifier="no change, or a rise that does not survive the paired bootstrap",
        cost="no new tokens; reorders existing ones"),
    Architecture(
        label="G_EXPLICIT_SCOPE_IDS",
        stress=S.SCOPE,
        hypothesis=(
            "goal ownership is currently implicit in nesting, which a reader must infer from "
            "indentation depth; naming the owning goal on every declaration and on the "
            "action converts an inferred relation into a stated one"),
        axes={"scope_metadata": "EXPLICIT_SCOPE_IDS",
              "goal_identity_visibility": "BOTH"},
        prediction="SCOPE rises substantially; this is the closest legal analogue of the "
                   "explicit positive control, so it should capture most of whatever gap "
                   "exists if the gap is about stating ownership at all",
        falsifier="the positive arm stays far above it, which would mean the gap is not "
                  "about naming the link but about where the naming sits",
        cost="one identifier per declaration; measurable token increase"),
    Architecture(
        label="G_GOAL_CENTRED_CONTEXT",
        stress=S.SCOPE,
        hypothesis=(
            "the declaration order is by declaration index, which cuts across goals; "
            "ordering context by goal and serialising the expression graph goal-first "
            "groups everything belonging to one goal into one contiguous run"),
        axes={"context_order": "GOAL_CENTRED",
              "graph_serialization": "GOAL_CENTRED",
              "goal_position": "FIRST"},
        prediction="SCOPE rises through locality alone, without naming ownership",
        falsifier="no change, which would separate 'locality' from 'explicit naming' as "
                  "causes and point at naming",
        cost="reordering only"),
    Architecture(
        label="G_REDUNDANT_GOAL_ANCHOR",
        stress=S.SCOPE,
        hypothesis=(
            "the link is stated once and then never repeated, so it must be held in memory "
            "across the whole rendering; repeating a short goal tag at each use restates it "
            "where it is needed"),
        axes={"redundancy_level": "SELECTIVE",
              "binder_use_reminder": "SHORT_TAG_AT_USE",
              "scope_metadata": "EXPLICIT_SCOPE_IDS"},
        prediction="SCOPE rises, and rises more on states with many goals than on states "
                   "with two -- the long-horizon prediction of PROJECT_GOAL",
        falsifier="a flat profile across goal count, which would refute the "
                  "horizon-interaction hypothesis for this component",
        cost="highest of the four; repeated tags at every use site"),
)


# -------------------------------------------------------------------- EXPRESSION_STRUCTURE
# Measured: positive 0.917, candidate 0.500 -- exactly chance, the largest headroom in the
# lab. The candidate exposes essentially nothing about relative depth.

EXPRESSION_ARCHITECTURES: tuple[Architecture, ...] = (
    Architecture(
        label="E_GRAPH_EDGE_LIST",
        stress=S.EXPRESSION_DEPTH,
        hypothesis=(
            "depth is currently implicit in nesting, and recovering it requires counting "
            "brackets across a long span; an explicit parent-child edge list states each "
            "structural relation as its own record, so depth becomes a path length over "
            "stated edges rather than a bracket-matching exercise"),
        axes={"tree_vs_graph_projection": "GRAPH_EDGE_LIST",
              "graph_serialization": "NODE_LIST_THEN_EDGES"},
        prediction="EXPRESSION_DEPTH rises materially off its 0.500 floor",
        falsifier="no change, which would mean the reader cannot follow an edge list either "
                  "and the limit is compositional rather than notational",
        cost="edge records add tokens; shared subterms stop being duplicated"),
    Architecture(
        label="E_HYBRID_NESTED_WITH_EDGES",
        stress=S.EXPRESSION_DEPTH,
        hypothesis=(
            "a pure edge list loses the locality that nesting provides, while pure nesting "
            "loses explicit relations; carrying both gives a reader two independent routes "
            "to the same structure and it can use whichever it reads better"),
        axes={"tree_vs_graph_projection": "HYBRID_NESTED_WITH_EDGES",
              "shared_subterm_handling": "HOISTED_DAG_LETS"},
        prediction="at least as good as the better of nesting and edge list alone",
        falsifier="worse than both, which would be evidence that redundant structure "
                  "actively interferes rather than helping -- an important result either way",
        cost="highest; both projections present"),
    Architecture(
        label="E_DEPENDENCY_LOCAL_SERIAL",
        stress=S.EXPRESSION_DEPTH,
        hypothesis=(
            "depth is hard to read because a DFS pre-order interleaves subtrees that belong "
            "to different branches; serialising dependency-locally keeps each reference "
            "adjacent to the material it depends on, shortening the span a reader must hold"),
        axes={"graph_serialization": "DEPENDENCY_LOCAL",
              "dependency_visibility": "EXPLICIT_EDGES",
              "context_order": "DEPENDENCY_TOPOLOGICAL"},
        prediction="EXPRESSION_DEPTH and DEPENDENCY both rise",
        falsifier="DEPENDENCY rises but EXPRESSION_DEPTH does not, which would separate the "
                  "two relations and say depth is not a dependency-locality problem",
        cost="reordering plus explicit edges"),
    Architecture(
        label="E_HEAD_ONLY_WITH_REMINDERS",
        stress=S.EXPRESSION_DEPTH,
        hypothesis=(
            "the rendering is dominated by full type trees, and the depth signal is buried "
            "in that volume; collapsing types to their head symbol and spending the saved "
            "tokens on per-use reminders raises the signal-to-noise of the structure itself"),
        axes={"type_explicitness": "HEAD_SYMBOL_ONLY",
              "binder_use_reminder": "TYPE_AT_USE",
              "universe_visibility": "OMITTED"},
        prediction="EXPRESSION_DEPTH rises while TYPE falls -- a deliberate trade that tests "
                   "whether the components compete for the reader's attention",
        falsifier="both fall, which would mean the omitted material was carrying the "
                  "structure rather than obscuring it",
        cost="net token reduction"),
)


ARCHITECTURES: dict[str, tuple[Architecture, ...]] = {
    S.SCOPE: GOAL_STRUCTURE_ARCHITECTURES,
    S.EXPRESSION_DEPTH: EXPRESSION_ARCHITECTURES,
}

#: Kept under the old name so nothing that imported it breaks silently.
MULTI_GOAL_ARCHITECTURES = GOAL_STRUCTURE_ARCHITECTURES


# ------------------------------------------------------------------------- known-bad set
# `MISSION §27`. Each hides the relation named by its stress. A valid instrument MUST rank
# the matching known-bad below a competent representation; if it does not, the instrument is
# blind to the very thing it claims to measure.

KNOWN_BAD: dict[str, dict[str, str]] = {
    "DELETE_DEPENDENCY_EDGES": {"dependency_visibility": "NONE"},
    "REMOVE_TYPE_LINK": {"type_explicitness": "OMITTED"},
    "HIDE_BINDER_RELATION": {"binder_metadata": "NONE", "binder_encoding": "DE_BRUIJN",
                             "identity_scheme": "DISPLAY_NAME"},
    "SCRAMBLE_SCOPE": {"scope_metadata": "IMPLICIT_BY_NESTING",
                       "goal_identity_visibility": "NONE"},
    "REMOVE_GOAL_ASSOCIATION": {"goal_identity_visibility": "NONE",
                                "action_encoding": "SOURCE_TACTIC"},
    "FLATTEN_EXPRESSION_PARENTAGE": {"graph_serialization": "EDGE_LIST",
                                     "expression_notation": "POSTFIX_RPN"},
    "SCRAMBLE_ACTION_ARGS": {"action_encoding": "SOURCE_TACTIC"},
    "STRIP_PROVENANCE": {"provenance_visibility": "NONE", "premise_locality": "TRAILING_BLOCK"},
}

#: Which known-bad each instrument must be able to detect.
DETECTS: dict[str, str] = {
    S.DEPENDENCY: "DELETE_DEPENDENCY_EDGES",
    S.TYPE: "REMOVE_TYPE_LINK",
    S.BINDER: "HIDE_BINDER_RELATION",
    S.SCOPE: "SCRAMBLE_SCOPE",
    S.MULTI_GOAL: "REMOVE_GOAL_ASSOCIATION",
    S.EXPRESSION_DEPTH: "FLATTEN_EXPRESSION_PARENTAGE",
    S.ACTION_ARGUMENT: "SCRAMBLE_ACTION_ARGS",
    S.PREMISE: "STRIP_PROVENANCE",
}


def _legal(axes: dict[str, str]) -> dict[str, str]:
    """Drop axis values this build does not offer, rather than failing the whole set.

    The axis vocabulary has grown across versions; a hypothesis written against a value that
    no longer exists should degrade to a weaker version of itself and say so, not abort a
    run that has seven other proposals in it.
    """

    out: dict[str, str] = {}
    for name, value in axes.items():
        axis = AXES_BY_NAME.get(name)
        if axis is not None and value in axis.values:
            out[name] = value
    return out


def realise(architecture: Architecture, base_label: str = "SEED_TYPED_AST",
            base: RepresentationGenome | None = None):
    """Compile an architecture onto a base genome. Returns (compiler, applied, dropped).

    ``base`` overrides the seed so a hypothesis can be tested as a mutation *of the
    candidate* rather than of a control. That is the interesting form: the question is
    whether this structural change rescues the representation the search actually found.
    """

    genome_base = base if base is not None else SEEDS[base_label]
    applied = _legal(architecture.axes)
    dropped = {k: v for k, v in architecture.axes.items() if k not in applied}
    return build(genome_base.with_values(**applied)), applied, dropped


def realise_known_bad(label: str, base_label: str = "SEED_TYPED_AST",
                      base: RepresentationGenome | None = None):
    axes = _legal(KNOWN_BAD[label])
    genome_base = base if base is not None else SEEDS[base_label]
    return build(genome_base.with_values(**axes)), axes


def behavioural_digest(compiler, items, limit: int = 8) -> str:
    """A hash of what this representation actually puts on the page.

    `MISSION §17` Level 2, and `FM-033`: two genomes differing on an axis the renderer never
    consults produce byte-identical output, and evaluating both spends inference to learn
    nothing. Deduplicating on the rendering rather than on the genome catches that.
    """

    import hashlib

    digest = hashlib.sha256()
    for item in items[:limit]:
        try:
            digest.update(compiler.render(item.state).text.encode())
        except Exception:  # noqa: BLE001
            digest.update(b"<unrenderable>")
    return digest.hexdigest()[:16]
