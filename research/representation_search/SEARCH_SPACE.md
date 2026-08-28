# The Representation Search Space

The language is data. A candidate representation in this search is a `RepresentationGenome`
— a point in a 42-axis discrete space — plus one generic compiler. There is no per-candidate
renderer code, so two candidates cannot differ by an implementation accident and any
candidate is reproducible from

    (genome_sha256, compiler_version, canonical_state_version)

alone. The candidate id is the first twelve hex digits of the genome hash, so `R_8611f712...`
names one language and always the same one.

## The pipeline

```text
CanonicalMathTransition (V2, elaborated Lean identities)
        |
        |  projection.py    -- what is written: exposure, identity, ordering, redundancy
        v
     Document               -- sections of records of typed fields
        |
        |  document.py      -- how it is written: grammar and lexicon
        |  expressions.py   -- how an expression tree is written
        v
       text
```

Parsing runs the same pipeline backwards from the same genome, which is why losslessness is
a property of the codec rather than a per-candidate promise.

## What losslessness means here

The declared semantic contract is `projection.semantic_core`: goals with their identities,
targets as elaborated expression trees, local contexts with identity, binder role,
declaration role, type and value, focus order, the relevant metavariables, and the action's
identity together with its external premise references and resolved local references.

Explicitly **outside** the contract, in line with `D-002` and `D-009`:

- Lean's display spelling of a binder (`alpha_normalization` may drop it);
- content hashes and the raw-id maps in `source_reference`;
- environment provenance;
- corpus bookkeeping.

A genome that hides contract content fails the round-trip gate and is rejected. It is not
scored, so it cannot buy a smaller token count with a semantic loss.

## The axes

`†` marks a value that a hard gate is expected to reject. Those values are kept in the space
on purpose: a search whose gates never fire has not demonstrated that its gates work.

### ACTIONS

| Axis | Phase | Values | Default |
|---|---|---|---|
| `action_encoding` | A | `SOURCE_TACTIC` · `GENERIC_SEMANTIC`† · `STRUCTURED_ARGS` · `SOURCE_PLUS_STRUCTURED` | `SOURCE_PLUS_STRUCTURED` |
| `action_position` | A | `BETWEEN_STATES` · `HEADER` · `TRAILER` | `BETWEEN_STATES` |

### EXPRESSIONS

| Axis | Phase | Values | Default |
|---|---|---|---|
| `expression_notation` | C | `SEXPR_PREFIX` · `FUNCTIONAL_APPLICATION` · `TAGGED_NESTED` · `POSTFIX_RPN` | `SEXPR_PREFIX` |
| `application_style` | C | `CURRIED_BINARY` · `FLATTENED_SPINE` | `CURRIED_BINARY` |
| `binder_encoding` | C | `DE_BRUIJN` · `NAMED` · `NAMED_PLUS_DE_BRUIJN` | `DE_BRUIJN` |
| `universe_visibility` | A | `FULL` · `ELIDED_WHEN_TRIVIAL` · `OMITTED`† | `FULL` |
| `const_name_form` | D | `FULL_NAME` · `LAST_COMPONENT`† · `FULL_NAME_WITH_ALIAS_TABLE` | `FULL_NAME` |
| `literal_form` | D | `TAGGED` · `BARE` | `TAGGED` |

### GRAMMAR

| Axis | Phase | Values | Default |
|---|---|---|---|
| `block_delimiter` | C | `INDENT` · `BRACE` · `KEYWORD_END` | `INDENT` |
| `field_marker` | C | `COLON` · `EQUALS` · `ARROW` | `COLON` |
| `record_separator` | C | `NEWLINE` · `NEWLINE_BLANK` | `NEWLINE` |
| `type_attachment` | C | `COLON_SUFFIX` · `TYPE_FIELD` | `TYPE_FIELD` |
| `list_syntax` | C | `BRACKET_COMMA` · `SPACE_SEPARATED` · `PAREN` | `BRACKET_COMMA` |

### GRAPH_SERIALIZATION

| Axis | Phase | Values | Default |
|---|---|---|---|
| `graph_serialization` | B | `DFS_PREORDER` · `BFS` · `TOPOLOGICAL` · `DEPENDENCY_LOCAL` · `GOAL_CENTRED` · `EDGE_LIST` · `NODE_LIST_THEN_EDGES` | `DFS_PREORDER` |
| `shared_subterm_handling` | B | `DUPLICATE` · `HOISTED_DAG_LETS` | `DUPLICATE` |

### IDENTITY

| Axis | Phase | Values | Default |
|---|---|---|---|
| `identity_scheme` | A | `SEMANTIC_ID` · `SHORT_ID` · `DISPLAY_NAME`† · `DISPLAY_PLUS_SHORT_ID` | `SHORT_ID` |
| `alpha_normalization` | A | `NORMALIZED` · `PRESERVE_DISPLAY` · `BOTH` | `NORMALIZED` |
| `identity_sigil` | D | `NONE` · `PREFIX_SIGIL` · `BRACKETED` | `NONE` |

### LEXICON

| Axis | Phase | Values | Default |
|---|---|---|---|
| `lexicon_register` | D | `HUMAN_WORDS` · `COMPACT_MNEMONIC` · `SYMBOLIC_ROLE` · `MATH_NOTATION` | `HUMAN_WORDS` |
| `keyword_case` | D | `LOWER` · `UPPER` | `LOWER` |
| `role_word_length` | D | `FULL` · `ABBREVIATED` · `SINGLE_CHAR` | `FULL` |
| `glyph_policy` | D | `UNICODE_NATIVE` · `ASCII_TRANSLITERATION` · `ASCII_ESCAPE`† | `UNICODE_NATIVE` |

### REDUNDANCY

| Axis | Phase | Values | Default |
|---|---|---|---|
| `redundancy_level` | B | `NONE` · `LOW` · `SELECTIVE` · `EXPLICIT` · `ERROR_CORRECTING` | `LOW` |
| `binder_use_reminder` | B | `NONE` · `TYPE_AT_USE` · `SHORT_TAG_AT_USE` | `NONE` |
| `checksum_policy` | B | `NONE` · `PER_STATE` | `NONE` |
| `count_assertions` | B | `NONE` · `PER_BLOCK` | `NONE` |

### SEMANTIC_EXPOSURE

| Axis | Phase | Values | Default |
|---|---|---|---|
| `type_explicitness` | A | `FULL_TREE` · `HEAD_SYMBOL_ONLY`† · `OMITTED`† | `FULL_TREE` |
| `implicit_argument_visibility` | A | `ALL` · `MARKED_ELIDED`† | `ALL` |
| `binder_metadata` | A | `FULL` · `ROLE_ONLY` · `NONE`† | `FULL` |
| `scope_metadata` | A | `EXPLICIT_SCOPE_IDS` · `IMPLICIT_BY_NESTING` | `IMPLICIT_BY_NESTING` |
| `goal_identity_visibility` | A | `SEMANTIC_ID` · `ORDINAL` · `BOTH` · `NONE`† | `SEMANTIC_ID` |
| `dependency_visibility` | A | `EXPLICIT_EDGES` · `INLINE_REFS` · `NONE`† | `INLINE_REFS` |
| `obligation_visibility` | A | `EXPLICIT_METAVAR_BLOCK` · `ASSIGNED_ONLY`† · `NONE`† | `EXPLICIT_METAVAR_BLOCK` |
| `provenance_visibility` | A | `IDENTITY_ONLY` · `NONE` | `IDENTITY_ONLY` |
| `delta_visibility` | A | `EXPLICIT_DELTA_BLOCK` · `DERIVABLE_ONLY` | `EXPLICIT_DELTA_BLOCK` |
| `local_instance_visibility` | A | `EXPLICIT` · `MERGED_INTO_CONTEXT` | `MERGED_INTO_CONTEXT` |

### STRUCTURE

| Axis | Phase | Values | Default |
|---|---|---|---|
| `syntax_family` | C | `BLOCK` · `SEXPR` · `TAGGED_LINE` · `INDENTED_TREE` · `JSONISH` · `PROSE` | `BLOCK` |
| `state_partitioning` | A | `BEFORE_AFTER_FULL` · `BEFORE_PLUS_DELTA` · `INTERLEAVED_BY_GOAL` | `BEFORE_AFTER_FULL` |
| `goal_position` | A | `FIRST` · `LAST` · `AFTER_CONTEXT` · `INLINE_WITH_CONTEXT` | `AFTER_CONTEXT` |
| `context_order` | B | `DECLARATION_INDEX` · `DEPENDENCY_TOPOLOGICAL` · `GOAL_CENTRED` · `REVERSE_INDEX` · `TYPE_GROUPED` | `DECLARATION_INDEX` |
| `premise_locality` | B | `HEADER_BLOCK` · `ADJACENT_TO_ACTION` · `TRAILING_BLOCK` | `ADJACENT_TO_ACTION` |
| `tree_vs_graph_projection` | B | `TREE_NESTED` · `GRAPH_EDGE_LIST` · `HYBRID_NESTED_WITH_EDGES` | `TREE_NESTED` |

## Phase order

Searching lexicon before architecture wastes generations: role words are cheap to change and
their effect is small next to a structural decision, so a lexicon optimum found under one
architecture rarely survives the next structural change. The controller therefore restricts
each generation to one phase:

| Phase | What varies | Generations (default schedule) |
|---|---|---|
| A | semantic and structural exposure, identity, actions | 0–1 |
| B | graph/sequence architecture, ordering, redundancy | 2–4 |
| C | grammar and expression notation | 5–6 |
| D | lexicon | 7–8 |
| — | unrestricted | 9+ |

## What the space deliberately does not contain

- **A tactic-text axis.** The canonical V2 record does not carry raw tactic text: an action's
  identity is its elaborated occurrence plus its tactic family, and the surface text is a
  source observation. A genome cannot vary what the canonical layer does not hold.
- **Semantic content axes.** Nothing in this space changes what is true. `M` is fixed;
  `R_phi(M)` varies.
- **Prompt-envelope axes.** `FM-001` recorded that the entire historical HML advantage was a
  prompt-envelope artifact. Envelope bytes are not part of a representation and are not
  searchable here.
