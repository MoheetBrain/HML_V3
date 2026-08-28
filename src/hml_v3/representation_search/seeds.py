"""Generation-zero population: real hypotheses, not decoration.

Every seed is an existing claim about how machine-facing mathematics should be written.
Prior HML gets no privilege (`D-005`, `FM-002`); Structured English, Lean-like, typed AST and
dependency-topological are pinned as controls because the failure memory records them as
having beaten or matched prior HML.
"""

from __future__ import annotations

from hml_v3.representation_search.genome import RepresentationGenome, default_genome


def _seed(label: str, notes: str, tags: tuple[str, ...] = (), **axes: str) -> RepresentationGenome:
    genome = default_genome(**axes)
    return RepresentationGenome(genome.resolved(), label=label, notes=notes, tags=tags)


SEEDS: dict[str, RepresentationGenome] = {
    "SEED_LEAN_LIKE": _seed(
        "SEED_LEAN_LIKE",
        "Lean's own presentation order: hypotheses then turnstile then target, "
        "mathematical glyphs, declaration order preserved.",
        ("baseline", "pinned"),
        syntax_family="BLOCK", goal_position="AFTER_CONTEXT",
        context_order="DECLARATION_INDEX", expression_notation="FUNCTIONAL_APPLICATION",
        lexicon_register="MATH_NOTATION", identity_scheme="DISPLAY_PLUS_SHORT_ID",
        alpha_normalization="BOTH", type_attachment="COLON_SUFFIX",
    ),
    "SEED_PRIOR_HML": _seed(
        "SEED_PRIOR_HML",
        "Prior HML's surface conventions expressed over V2 content: canonical role "
        "blocks, indented paragraphs, human role words, short ids, dependency-topological "
        "order inside each block, and a full before/after pair. This is a reconstruction "
        "of the conventions the frozen renderer used, not the frozen renderer itself: that "
        "renderer speaks the prior claim/goal ontology and cannot consume a V2 state.",
        ("baseline", "pinned"),
        syntax_family="BLOCK", block_delimiter="INDENT", field_marker="COLON",
        context_order="DEPENDENCY_TOPOLOGICAL", graph_serialization="TOPOLOGICAL",
        lexicon_register="HUMAN_WORDS", redundancy_level="LOW",
        delta_visibility="EXPLICIT_DELTA_BLOCK", record_separator="NEWLINE",
    ),
    "SEED_TYPED_AST": _seed(
        "SEED_TYPED_AST",
        "A typed abstract syntax tree: everything nested, tags on every node, "
        "no prose scaffolding.",
        ("baseline", "pinned"),
        syntax_family="INDENTED_TREE", expression_notation="TAGGED_NESTED",
        tree_vs_graph_projection="TREE_NESTED", lexicon_register="COMPACT_MNEMONIC",
        binder_encoding="DE_BRUIJN", type_attachment="TYPE_FIELD",
    ),
    "SEED_STRUCTURED_ENGLISH": _seed(
        "SEED_STRUCTURED_ENGLISH",
        "Controlled English sentences over the same semantic units. The strongest arm in "
        "the Stage-1 probe (FM-002); pinned as a control for the whole search.",
        ("baseline", "pinned"),
        syntax_family="PROSE", lexicon_register="HUMAN_WORDS", role_word_length="FULL",
        expression_notation="FUNCTIONAL_APPLICATION", identity_scheme="DISPLAY_PLUS_SHORT_ID",
        alpha_normalization="BOTH", goal_position="AFTER_CONTEXT",
    ),
    "SEED_CANONICAL_SEXPR": _seed(
        "SEED_CANONICAL_SEXPR",
        "One self-contained parenthesised record per line. FM-007 records that this "
        "destroys record-order error detection; carried to test whether that reproduces.",
        ("baseline",),
        syntax_family="SEXPR", expression_notation="SEXPR_PREFIX",
        lexicon_register="COMPACT_MNEMONIC", redundancy_level="NONE",
    ),
    "SEED_GRAPH_EDGE": _seed(
        "SEED_GRAPH_EDGE",
        "Nodes carry intrinsic content only; every reference becomes an edge record. "
        "FM's R4: best locality and best error detection, rejected on cost.",
        ("baseline",),
        tree_vs_graph_projection="GRAPH_EDGE_LIST", dependency_visibility="EXPLICIT_EDGES",
        graph_serialization="NODE_LIST_THEN_EDGES", syntax_family="TAGGED_LINE",
    ),
    "SEED_GOAL_LOCAL": _seed(
        "SEED_GOAL_LOCAL",
        "Goal first, then only its own context. FM-005 recorded goal-centred ordering as a "
        "negative; re-entered once because the V2 corpus has real dependency structure.",
        ("baseline", "retry_with_changed_condition"),
        goal_position="FIRST", context_order="GOAL_CENTRED",
        graph_serialization="GOAL_CENTRED", scope_metadata="EXPLICIT_SCOPE_IDS",
    ),
    "SEED_DEPENDENCY_TOPOLOGICAL": _seed(
        "SEED_DEPENDENCY_TOPOLOGICAL",
        "FM-006's trait in isolation: dependency-topological local-context order on an "
        "otherwise default genome, so the ordering axis can be attributed on its own. It "
        "differs from SEED_PRIOR_HML only in leaving goal linearization at the default.",
        ("baseline", "pinned"),
        context_order="DEPENDENCY_TOPOLOGICAL",
    ),
    "SEED_EXPLICIT_REDUNDANT": _seed(
        "SEED_EXPLICIT_REDUNDANT",
        "Everything restated: scope ids, block counts, per-state digests, positional "
        "indices. The maximum-error-detection end of the space.",
        ("baseline",),
        redundancy_level="ERROR_CORRECTING", checksum_policy="PER_STATE",
        count_assertions="PER_BLOCK", scope_metadata="EXPLICIT_SCOPE_IDS",
        goal_identity_visibility="BOTH", alpha_normalization="BOTH",
    ),
    "SEED_MINIMAL_MACHINE": _seed(
        "SEED_MINIMAL_MACHINE",
        "The compression end of the space: symbolic role words, short ids, no redundancy, "
        "flattened application spines.",
        ("baseline",),
        syntax_family="TAGGED_LINE", lexicon_register="SYMBOLIC_ROLE",
        identity_scheme="SHORT_ID", redundancy_level="NONE",
        application_style="FLATTENED_SPINE", universe_visibility="ELIDED_WHEN_TRIVIAL",
        delta_visibility="DERIVABLE_ONLY", provenance_visibility="NONE",
        literal_form="BARE",
    ),
    "SEED_JSON_BASELINE": _seed(
        "SEED_JSON_BASELINE",
        "A generic structured serialization. FM-001 recorded that a frozen model preferred "
        "canonical JSON to prior HML on the common-envelope zero-shot arm.",
        ("baseline",),
        syntax_family="JSONISH", lexicon_register="HUMAN_WORDS",
        expression_notation="FUNCTIONAL_APPLICATION", list_syntax="BRACKET_COMMA",
    ),
    "SEED_HYBRID_LOCAL_DAG": _seed(
        "SEED_HYBRID_LOCAL_DAG",
        "Deliberate hybrid: topological layout, hoisted shared subterms, edges alongside "
        "nesting, and a binder reminder at each use.",
        ("hybrid",),
        context_order="DEPENDENCY_TOPOLOGICAL", graph_serialization="DEPENDENCY_LOCAL",
        shared_subterm_handling="HOISTED_DAG_LETS",
        tree_vs_graph_projection="HYBRID_NESTED_WITH_EDGES",
        binder_use_reminder="SHORT_TAG_AT_USE", redundancy_level="SELECTIVE",
    ),
    "SEED_HYBRID_COMPACT_BLOCK": _seed(
        "SEED_HYBRID_COMPACT_BLOCK",
        "Deliberate hybrid: block scaffolding for error detection, compact mnemonics for "
        "cost, flattened spines, premises adjacent to the action.",
        ("hybrid",),
        syntax_family="BLOCK", lexicon_register="COMPACT_MNEMONIC",
        application_style="FLATTENED_SPINE", premise_locality="ADJACENT_TO_ACTION",
        context_order="DEPENDENCY_TOPOLOGICAL", identity_scheme="SHORT_ID",
    ),
    "SEED_HYBRID_RPN_MACHINE": _seed(
        "SEED_HYBRID_RPN_MACHINE",
        "Deliberate hybrid: postfix expressions with block record scaffolding, testing "
        "whether stack notation buys tokens without losing record-order detection.",
        ("hybrid",),
        expression_notation="POSTFIX_RPN", application_style="FLATTENED_SPINE",
        syntax_family="BLOCK", lexicon_register="COMPACT_MNEMONIC",
    ),
    "SEED_HEADER_PREMISE": _seed(
        "SEED_HEADER_PREMISE",
        "Premises declared once in a header block rather than beside the action, testing "
        "whether premise-to-action distance is worth paying for.",
        ("hybrid",),
        premise_locality="HEADER_BLOCK", action_position="TRAILER",
    ),
    "SEED_DELTA_FIRST": _seed(
        "SEED_DELTA_FIRST",
        "Action first, then before-state, then after-state. Tests whether stating the "
        "operation before the operand changes obligation-to-action distance.",
        ("hybrid",),
        action_position="HEADER", delta_visibility="EXPLICIT_DELTA_BLOCK",
        goal_position="FIRST",
    ),
}


def seed_population() -> list[RepresentationGenome]:
    return [SEEDS[name] for name in sorted(SEEDS)]


PINNED_LABELS = tuple(
    name for name, genome in sorted(SEEDS.items()) if "pinned" in genome.tags
)
