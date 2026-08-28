"""The representation genome: a machine-readable description of one candidate language.

A genome is data, not code. Every candidate representation in this search is reproducible
from ``(genome, compiler_commit, canonical_state_version)`` alone, and its identity is the
SHA-256 of its canonical genome JSON. Nothing about a candidate is decided by hand-written
per-experiment renderer code.

The axes are grouped exactly as the search phases are ordered: PHASE A varies semantic and
structural exposure, PHASE B varies graph/sequence architecture, PHASE C varies grammar, and
PHASE D varies lexicon. Searching lexicon before architecture is explicitly wasteful, so the
controller uses ``Axis.phase`` to restrict which axes a generation may touch.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
from typing import Any, Iterable

GENOME_SCHEMA_VERSION = "representation-genome-v1.0.0"


@dataclass(frozen=True)
class Axis:
    name: str
    group: str
    phase: str
    values: tuple[str, ...]
    default: str
    description: str
    #: Axis values that a hard gate is expected to reject. They stay in the space on purpose:
    #: the search must be able to demonstrate that the gates bite.
    known_lossy: tuple[str, ...] = ()


def _axis(name, group, phase, values, default, description, known_lossy=()) -> Axis:
    return Axis(name, group, phase, tuple(values), default, description, tuple(known_lossy))


AXES: tuple[Axis, ...] = (
    # ---------------------------------------------------------------- STRUCTURE (phase A/B)
    _axis("syntax_family", "STRUCTURE", "C",
          ["BLOCK", "SEXPR", "TAGGED_LINE", "INDENTED_TREE", "JSONISH", "PROSE"],
          "BLOCK", "Overall surface shape of a record."),
    _axis("state_partitioning", "STRUCTURE", "A",
          ["BEFORE_AFTER_FULL", "BEFORE_PLUS_DELTA", "INTERLEAVED_BY_GOAL"],
          "BEFORE_AFTER_FULL",
          "Whether the after-state is emitted in full, replaced by a delta, or interleaved. "
          "BEFORE_PLUS_DELTA is the 18.8%-duplication saving FM-008 identified as the "
          "largest single cost in the prior design; it is kept in the space so the search "
          "can demonstrate that the identity-aware delta does not in fact determine the "
          "after-state's modified targets.",
          known_lossy=["BEFORE_PLUS_DELTA"]),
    _axis("goal_position", "STRUCTURE", "A",
          ["FIRST", "LAST", "AFTER_CONTEXT", "INLINE_WITH_CONTEXT"],
          "AFTER_CONTEXT", "Where a goal's target sits relative to its local context."),
    _axis("context_order", "STRUCTURE", "B",
          ["DECLARATION_INDEX", "DEPENDENCY_TOPOLOGICAL", "GOAL_CENTRED", "REVERSE_INDEX",
           "TYPE_GROUPED"],
          "DECLARATION_INDEX", "Order of local declarations inside a goal."),
    _axis("premise_locality", "STRUCTURE", "B",
          ["HEADER_BLOCK", "ADJACENT_TO_ACTION", "TRAILING_BLOCK"],
          "ADJACENT_TO_ACTION", "Where external premise references are stated."),
    _axis("tree_vs_graph_projection", "STRUCTURE", "B",
          ["TREE_NESTED", "GRAPH_EDGE_LIST", "HYBRID_NESTED_WITH_EDGES"],
          "TREE_NESTED", "Whether reference relations are embedded or stated as edges."),
    # -------------------------------------------------------- SEMANTIC EXPOSURE (phase A)
    _axis("type_explicitness", "SEMANTIC_EXPOSURE", "A",
          ["FULL_TREE", "HEAD_SYMBOL_ONLY", "OMITTED"],
          "FULL_TREE", "How much of a local declaration's type is shown.",
          known_lossy=["HEAD_SYMBOL_ONLY", "OMITTED"]),
    _axis("implicit_argument_visibility", "SEMANTIC_EXPOSURE", "A",
          ["ALL", "MARKED_ELIDED"],
          "ALL",
          "MARKED_ELIDED replaces the type of every implicit or instance-implicit local "
          "declaration with a marker, mirroring Lean's own inst-dagger display convention.",
          known_lossy=["MARKED_ELIDED"]),
    _axis("binder_metadata", "SEMANTIC_EXPOSURE", "A",
          ["FULL", "ROLE_ONLY", "NONE"],
          "FULL",
          "BinderInfo plus Lean's LocalDeclKind, binder role only, or neither. ROLE_ONLY "
          "drops the declaration kind, which also distinguishes implementation-detail and "
          "auxiliary declarations and is therefore not recoverable from the value field.",
          known_lossy=["NONE", "ROLE_ONLY"]),
    _axis("scope_metadata", "SEMANTIC_EXPOSURE", "A",
          ["EXPLICIT_SCOPE_IDS", "IMPLICIT_BY_NESTING"],
          "IMPLICIT_BY_NESTING", "Whether each declaration names its owning goal explicitly."),
    _axis("goal_identity_visibility", "SEMANTIC_EXPOSURE", "A",
          ["SEMANTIC_ID", "ORDINAL", "BOTH", "NONE"],
          "SEMANTIC_ID", "How a goal is identified across before/after states.",
          known_lossy=["NONE", "ORDINAL"]),
    _axis("dependency_visibility", "SEMANTIC_EXPOSURE", "A",
          ["EXPLICIT_EDGES", "INLINE_REFS", "NONE"],
          "INLINE_REFS", "How the action's local-context references are stated.",
          known_lossy=["NONE"]),
    _axis("obligation_visibility", "SEMANTIC_EXPOSURE", "A",
          ["EXPLICIT_METAVAR_BLOCK", "ASSIGNED_ONLY", "NONE"],
          "EXPLICIT_METAVAR_BLOCK", "How open metavariable obligations are exposed.",
          known_lossy=["ASSIGNED_ONLY", "NONE"]),
    _axis("provenance_visibility", "SEMANTIC_EXPOSURE", "A",
          ["IDENTITY_ONLY", "NONE"],
          "IDENTITY_ONLY", "Whether theorem/source identity accompanies the transition."),
    _axis("delta_visibility", "SEMANTIC_EXPOSURE", "A",
          ["EXPLICIT_DELTA_BLOCK", "DERIVABLE_ONLY"],
          "EXPLICIT_DELTA_BLOCK", "Whether the structured delta is stated or left derivable."),
    _axis("local_instance_visibility", "SEMANTIC_EXPOSURE", "A",
          ["EXPLICIT", "MERGED_INTO_CONTEXT"],
          "MERGED_INTO_CONTEXT", "Whether typeclass instances get their own records."),
    # ------------------------------------------------------------------ IDENTITY (phase A)
    _axis("identity_scheme", "IDENTITY", "A",
          ["SEMANTIC_ID", "SHORT_ID", "DISPLAY_NAME", "DISPLAY_PLUS_SHORT_ID"],
          "SHORT_ID", "The token used to name a local declaration or goal.",
          known_lossy=["DISPLAY_NAME"]),
    _axis("alpha_normalization", "IDENTITY", "A",
          ["NORMALIZED", "PRESERVE_DISPLAY", "BOTH"],
          "NORMALIZED", "Whether Lean's display spelling is retained beside the identity."),
    _axis("identity_sigil", "IDENTITY", "D",
          ["NONE", "PREFIX_SIGIL", "BRACKETED"],
          "NONE", "Lexical marking that distinguishes an identity from a word."),
    # --------------------------------------------------------------- EXPRESSIONS (phase C)
    _axis("expression_notation", "EXPRESSIONS", "C",
          ["SEXPR_PREFIX", "FUNCTIONAL_APPLICATION", "TAGGED_NESTED", "POSTFIX_RPN"],
          "SEXPR_PREFIX", "Surface encoding of an elaborated expression tree."),
    _axis("application_style", "EXPRESSIONS", "C",
          ["CURRIED_BINARY", "FLATTENED_SPINE"],
          "CURRIED_BINARY", "Whether nested applications are flattened to a head and args."),
    _axis("binder_encoding", "EXPRESSIONS", "C",
          ["DE_BRUIJN", "NAMED", "NAMED_PLUS_DE_BRUIJN"],
          "DE_BRUIJN", "How bound variables and their binders are written."),
    _axis("universe_visibility", "EXPRESSIONS", "A",
          ["FULL", "ELIDED_WHEN_TRIVIAL", "OMITTED"],
          "FULL", "Whether universe level arguments are printed.",
          known_lossy=["OMITTED"]),
    _axis("const_name_form", "EXPRESSIONS", "D",
          ["FULL_NAME", "LAST_COMPONENT", "FULL_NAME_WITH_ALIAS_TABLE"],
          "FULL_NAME", "How a global constant is spelled.",
          known_lossy=["LAST_COMPONENT"]),
    _axis("literal_form", "EXPRESSIONS", "D",
          ["TAGGED", "BARE"],
          "TAGGED",
          "Whether literals carry their kind tag. BARE recovers the kind from the value's "
          "shape, which is exact for Lean 4.10's two literal kinds (NAT, STRING) and would "
          "stop being exact if a source system introduced a third that a digit string "
          "could also denote."),
    # ---------------------------------------------------------- GRAPH SERIALIZATION (B)
    _axis("graph_serialization", "GRAPH_SERIALIZATION", "B",
          ["DFS_PREORDER", "BFS", "TOPOLOGICAL", "DEPENDENCY_LOCAL", "GOAL_CENTRED",
           "EDGE_LIST", "NODE_LIST_THEN_EDGES"],
          "DFS_PREORDER", "Linearization strategy applied to the record graph."),
    _axis("shared_subterm_handling", "GRAPH_SERIALIZATION", "B",
          ["DUPLICATE", "HOISTED_DAG_LETS"],
          "DUPLICATE", "Whether repeated subterms are hoisted into a shared table."),
    # ---------------------------------------------------------------- REDUNDANCY (phase B)
    _axis("redundancy_level", "REDUNDANCY", "B",
          ["NONE", "LOW", "SELECTIVE", "EXPLICIT", "ERROR_CORRECTING"],
          "LOW", "How much recoverable information is deliberately restated."),
    _axis("binder_use_reminder", "REDUNDANCY", "B",
          ["NONE", "TYPE_AT_USE", "SHORT_TAG_AT_USE"],
          "NONE", "Whether a local reference restates something about its binder."),
    _axis("checksum_policy", "REDUNDANCY", "B",
          ["NONE", "PER_STATE"],
          "NONE", "Whether a short content digest is emitted for corruption detection."),
    _axis("count_assertions", "REDUNDANCY", "B",
          ["NONE", "PER_BLOCK"],
          "NONE", "Whether block cardinalities are asserted in the text."),
    # ------------------------------------------------------------------- GRAMMAR (phase C)
    _axis("block_delimiter", "GRAMMAR", "C",
          ["INDENT", "BRACE", "KEYWORD_END"],
          "INDENT", "How a record's extent is marked."),
    _axis("field_marker", "GRAMMAR", "C",
          ["COLON", "EQUALS", "ARROW"],
          "COLON", "The separator between a field name and its value."),
    _axis("record_separator", "GRAMMAR", "C",
          ["NEWLINE", "NEWLINE_BLANK"],
          "NEWLINE", "What separates two records."),
    _axis("type_attachment", "GRAMMAR", "C",
          ["COLON_SUFFIX", "TYPE_FIELD"],
          "TYPE_FIELD", "Whether a declaration's type is a suffix or a named field."),
    _axis("list_syntax", "GRAMMAR", "C",
          ["BRACKET_COMMA", "SPACE_SEPARATED", "PAREN"],
          "BRACKET_COMMA", "How a list of atoms is written."),
    # ------------------------------------------------------------------- LEXICON (phase D)
    _axis("lexicon_register", "LEXICON", "D",
          ["HUMAN_WORDS", "COMPACT_MNEMONIC", "SYMBOLIC_ROLE", "MATH_NOTATION"],
          "HUMAN_WORDS", "The vocabulary family used for role words."),
    _axis("keyword_case", "LEXICON", "D",
          ["LOWER", "UPPER"],
          "LOWER", "Case of role keywords."),
    _axis("role_word_length", "LEXICON", "D",
          ["FULL", "ABBREVIATED", "SINGLE_CHAR"],
          "FULL", "Length of role words."),
    _axis("glyph_policy", "LEXICON", "D",
          ["UNICODE_NATIVE", "ASCII_TRANSLITERATION", "ASCII_ESCAPE"],
          "UNICODE_NATIVE",
          "How non-ASCII mathematical glyphs are written. ASCII_ESCAPE is retained only so "
          "the UTF-8 hard gate recorded in FM-004 can be demonstrated to bite.",
          known_lossy=["ASCII_ESCAPE"]),
    # ------------------------------------------------------------------- ACTIONS (phase A)
    _axis("action_encoding", "ACTIONS", "A",
          ["SOURCE_TACTIC", "GENERIC_SEMANTIC", "STRUCTURED_ARGS", "SOURCE_PLUS_STRUCTURED"],
          "SOURCE_PLUS_STRUCTURED", "What the action record states.",
          known_lossy=["GENERIC_SEMANTIC"]),
    _axis("action_position", "ACTIONS", "A",
          ["BETWEEN_STATES", "HEADER", "TRAILER"],
          "BETWEEN_STATES", "Where the action record sits in the document."),
)

AXES_BY_NAME: dict[str, Axis] = {axis.name: axis for axis in AXES}
PHASES = ("A", "B", "C", "D")


@dataclass(frozen=True)
class RepresentationGenome:
    """One point in the representation space."""

    values: dict[str, str]
    label: str = ""
    notes: str = ""
    tags: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        unknown = set(self.values) - set(AXES_BY_NAME)
        if unknown:
            raise ValueError(f"unknown genome axes: {sorted(unknown)}")
        for name, value in self.values.items():
            if value not in AXES_BY_NAME[name].values:
                raise ValueError(f"axis {name} cannot take value {value!r}")

    def get(self, axis: str) -> str:
        return self.values.get(axis, AXES_BY_NAME[axis].default)

    def resolved(self) -> dict[str, str]:
        return {axis.name: self.get(axis.name) for axis in AXES}

    def with_values(self, **overrides: str) -> "RepresentationGenome":
        merged = dict(self.resolved())
        merged.update(overrides)
        return RepresentationGenome(merged, self.label, self.notes, self.tags)

    def canonical_json(self) -> str:
        return json.dumps(
            {"schema_version": GENOME_SCHEMA_VERSION, "axes": self.resolved()},
            ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        )

    def sha256(self) -> str:
        return hashlib.sha256(self.canonical_json().encode()).hexdigest()

    def candidate_id(self) -> str:
        return f"R_{self.sha256()[:12]}"

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id(),
            "genome_sha256": self.sha256(),
            "schema_version": GENOME_SCHEMA_VERSION,
            "label": self.label,
            "notes": self.notes,
            "tags": list(self.tags),
            "axes": self.resolved(),
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "RepresentationGenome":
        return cls(
            values=dict(value["axes"]),
            label=value.get("label", ""),
            notes=value.get("notes", ""),
            tags=tuple(value.get("tags", ())),
        )

    def distance(self, other: "RepresentationGenome") -> int:
        """Hamming distance in axis space; the search's diversity coordinate."""

        mine, theirs = self.resolved(), other.resolved()
        return sum(1 for axis in AXES if mine[axis.name] != theirs[axis.name])

    def differing_axes(self, other: "RepresentationGenome") -> list[str]:
        mine, theirs = self.resolved(), other.resolved()
        return [axis.name for axis in AXES if mine[axis.name] != theirs[axis.name]]


def default_genome(**overrides: str) -> RepresentationGenome:
    return RepresentationGenome({axis.name: axis.default for axis in AXES}).with_values(**overrides)


def space_size() -> int:
    total = 1
    for axis in AXES:
        total *= len(axis.values)
    return total


def axes_for_phase(phase: str) -> list[Axis]:
    return [axis for axis in AXES if axis.phase == phase]


def axis_names(groups: Iterable[str] | None = None) -> list[str]:
    if groups is None:
        return [axis.name for axis in AXES]
    wanted = set(groups)
    return [axis.name for axis in AXES if axis.group in wanted]
