# PRETRAINING_REPRESENTATION_FRONTIER_V1

**This is not a claim that any representation is optimal for neural mathematical reasoning.** It is the strongest Pareto frontier obtainable from static evidence before model adaptation, together with the evidence that produced it.

## Provenance

| Field | Value |
|---|---|
| Compiler | `representation-compiler-v1.0.0` |
| Canonical state | `canonical-math-transition-v2.0.0` |
| Genome axes | 42 |
| Search space | 4.095e+19 points |
| Corpus transitions | 317 |
| Mathlib domains | 26 |
| Generations completed | 12 |
| Candidates registered | 208 |
| Candidates evaluated | 165 |
| Candidates hard-rejected | 27 |
| Strict Pareto front | 85 |
| Distinct measurement vectors | 120 |
| Reported finalists | 7 |

## Corpus split

| Split | Transitions | Families |
|---|---|---|
| `SEARCH_DEV` | 224 | 126 |
| `SEARCH_VALIDATION` | 37 | 24 |
| `SEALED_FINAL_EVALUATION` | 56 | 37 |

Split unit: `MATHLIB_SOURCE_FILE`. Families hash `c6c1befad5ca82e3`.

## The frontier

Strict non-dominated sorting over seven axes leaves 85 of 165 evaluated candidates on the front, and an epsilon-front at eps=0.02 still keeps 147. With enough axes almost every candidate is best at something, so neither is a shortlist.

The finalists below follow a rule that states why each one is present: **the best candidate on each Pareto axis taken alone, plus the knee** - the candidate closest to the ideal point after per-axis normalisation. Candidates with identical measurement vectors are collapsed first. Selection during the search used the strict front, so this reporting rule could not have steered it.

| # | Candidate | Shortlisted because | BPE tokens | Binder distance | Premise distance | Swap detect | Drop-field detect | Ident. frag | Max span |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | `R_26259b75353b` | best_on:bpe_tokens_per_transition, best_on:identifier_fragmentation | 7161.7 | 194.3 | 623.9 | 0.696 | 0.000 | 1.80 | 3176.1 |
| 2 | `R_3c2d80a45f5f` | best_on:max_reference_span_tokens | 7337.1 | 195.5 | 882.4 | 0.913 | 0.000 | 2.13 | 3012.5 |
| 3 | `R_d51968446f17` | knee | 7422.0 | 203.5 | 648.0 | 0.955 | 0.917 | 1.90 | 3281.8 |
| 4 | `R_07e59bff963f` | best_on:detect_drop_field | 7512.8 | 206.2 | 1033.6 | 0.957 | 0.917 | 1.86 | 3314.9 |
| 5 | `R_f3d7d713e16a` | best_on:premise_to_action_distance_tokens | 9017.3 | 241.8 | 49.3 | 0.864 | 0.000 | 1.93 | 3740.7 |
| 6 | `SEED_DELTA_FIRST` | best_on:detect_swap_records | 9466.9 | 246.7 | 63.8 | 1.000 | 0.583 | 1.99 | 4453.8 |
| 7 | `R_74de39415d66` | best_on:binder_use_distance_tokens | 18096.7 | 147.1 | 2742.3 | 0.682 | 0.292 | 2.12 | 5180.4 |

## Controls

Every seeded baseline, whether or not it survived. `FM-002` and `FM-006` require the recorded baselines to remain visible for the whole search.

| Baseline | Status | On front | Token rank | Rejection |
|---|---|---|---|---|
| `SEED_CANONICAL_SEXPR` | EVALUATED | no | 77 | — |
| `SEED_DELTA_FIRST` | EVALUATED | yes | 100 | — |
| `SEED_DEPENDENCY_TOPOLOGICAL` | EVALUATED | no | 102 | — |
| `SEED_EXPLICIT_REDUNDANT` | EVALUATED | no | 136 | — |
| `SEED_GOAL_LOCAL` | EVALUATED | no | 119 | — |
| `SEED_GRAPH_EDGE` | EVALUATED | no | 132 | — |
| `SEED_HEADER_PREMISE` | EVALUATED | no | 113 | — |
| `SEED_HYBRID_COMPACT_BLOCK` | EVALUATED | no | 55 | — |
| `SEED_HYBRID_LOCAL_DAG` | EVALUATED | no | 165 | — |
| `SEED_HYBRID_RPN_MACHINE` | EVALUATED | no | 14 | — |
| `SEED_JSON_BASELINE` | EVALUATED | no | 89 | — |
| `SEED_LEAN_LIKE` | EVALUATED | no | 151 | — |
| `SEED_MINIMAL_MACHINE` | EVALUATED | no | 29 | — |
| `SEED_PRIOR_HML` | EVALUATED | no | 101 | — |
| `SEED_STRUCTURED_ENGLISH` | EVALUATED | no | 150 | — |
| `SEED_TYPED_AST` | EVALUATED | no | 144 | — |

## Generations

| Gen | Phase | Evaluated | Rejected | Front | Frontier moved | Memory blocks | Refuted | Seconds |
|---|---|---:|---:|---:|---|---:|---:|---:|
| 0 | A | 16 | 0 | 12 | yes | 0 | 0 | 33.8 |
| 1 | A | 27 | 5 | 22 | yes | 0 | 6 | 19.3 |
| 2 | B | 35 | 5 | 27 | yes | 17 | 14 | 18.5 |
| 3 | B | 40 | 0 | 36 | no | 26 | 18 | 31.6 |
| 4 | B | 40 | 0 | 37 | yes | 25 | 18 | 36.5 |
| 5 | C | 40 | 0 | 37 | yes | 0 | 17 | 28.2 |
| 6 | C | 40 | 0 | 25 | yes | 0 | 16 | 34.9 |
| 7 | D | 40 | 0 | 30 | yes | 0 | 20 | 34.3 |
| 8 | D | 34 | 6 | 23 | yes | 0 | 14 | 17.2 |
| 9 | — | 35 | 5 | 23 | yes | 9 | 14 | 32.5 |
| 10 | — | 38 | 2 | 29 | yes | 14 | 22 | 27.6 |
| 11 | — | 36 | 4 | 27 | yes | 13 | 23 | 17.4 |

## Why candidates were rejected

Rejections are evidence, not waste: they are what demonstrates that the hard gates bite.

| Reason | Candidates |
|---|---:|
| `semantic_round_trip` | 15 |
| `AMBIGUOUS_LEXICON` | 7 |
| `glyph_fidelity_utf8` | 5 |

## Refuted hypotheses

182 proposed mutations moved their target metric the wrong way. Each is a recorded negative result.

| Axis | From | To | Metric | Parent | Child |
|---|---|---|---|---:|---:|
| `action_position` | `BETWEEN_STATES` | `TRAILER` | `premise_to_action_distance_tokens` | 390.440 | 1045.764 |
| `goal_position` | `AFTER_CONTEXT` | `INLINE_WITH_CONTEXT` | `premise_to_action_distance_tokens` | 421.268 | 421.268 |
| `identity_scheme` | `SHORT_ID` | `DISPLAY_PLUS_SHORT_ID` | `identifier_fragmentation` | 2.049 | 2.374 |
| `local_instance_visibility` | `MERGED_INTO_CONTEXT` | `EXPLICIT` | `bpe_tokens_per_transition` | 9040.562 | 9040.562 |
| `goal_identity_visibility` | `SEMANTIC_ID` | `BOTH` | `bpe_tokens_per_transition` | 9469.938 | 9482.844 |
| `provenance_visibility` | `NONE` | `IDENTITY_ONLY` | `bpe_tokens_per_transition` | 7977.000 | 8014.500 |
| `goal_position` | `AFTER_CONTEXT` | `LAST` | `premise_to_action_distance_tokens` | 371.810 | 371.810 |
| `alpha_normalization` | `NORMALIZED` | `BOTH` | `bpe_tokens_per_transition` | 7667.156 | 8029.969 |
| `scope_metadata` | `IMPLICIT_BY_NESTING` | `EXPLICIT_SCOPE_IDS` | `bpe_tokens_per_transition` | 9040.562 | 9237.406 |
| `premise_locality` | `ADJACENT_TO_ACTION` | `TRAILING_BLOCK` | `premise_to_action_distance_tokens` | 63.849 | 63.849 |
| `context_order` | `DEPENDENCY_TOPOLOGICAL` | `GOAL_CENTRED` | `binder_use_distance_tokens` | 235.002 | 244.100 |
| `tree_vs_graph_projection` | `TREE_NESTED` | `GRAPH_EDGE_LIST` | `max_reference_span_tokens` | 3147.469 | 3195.844 |
| `context_order` | `DEPENDENCY_TOPOLOGICAL` | `DECLARATION_INDEX` | `binder_use_distance_tokens` | 240.440 | 240.440 |
| `graph_serialization` | `TOPOLOGICAL` | `EDGE_LIST` | `max_reference_span_tokens` | 4039.312 | 4039.312 |
| `graph_serialization` | `DFS_PREORDER` | `TOPOLOGICAL` | `max_reference_span_tokens` | 3933.344 | 3933.344 |
| `tree_vs_graph_projection` | `TREE_NESTED` | `HYBRID_NESTED_WITH_EDGES` | `max_reference_span_tokens` | 3147.469 | 3195.844 |
| `graph_serialization` | `DFS_PREORDER` | `BFS` | `max_reference_span_tokens` | 3595.031 | 3595.031 |
| `shared_subterm_handling` | `DUPLICATE` | `HOISTED_DAG_LETS` | `bpe_tokens_per_transition` | 9466.938 | 22420.406 |
| `checksum_policy` | `NONE` | `PER_STATE` | `detect_corrupt_identity` | 1.000 | 1.000 |
| `count_assertions` | `NONE` | `PER_BLOCK` | `detect_drop_line` | 0.833 | 0.708 |
| `redundancy_level` | `NONE` | `ERROR_CORRECTING` | `detect_drop_field` | 0.000 | 0.000 |
| `graph_serialization` | `DFS_PREORDER` | `EDGE_LIST` | `max_reference_span_tokens` | 4786.844 | 4786.844 |
| `graph_serialization` | `DFS_PREORDER` | `NODE_LIST_THEN_EDGES` | `max_reference_span_tokens` | 3694.031 | 3694.031 |
| `redundancy_level` | `NONE` | `EXPLICIT` | `detect_drop_field` | 0.000 | 0.000 |
| `redundancy_level` | `LOW` | `SELECTIVE` | `detect_drop_field` | 0.708 | 0.708 |
| `redundancy_level` | `NONE` | `SELECTIVE` | `detect_drop_field` | 0.000 | 0.000 |
| `tree_vs_graph_projection` | `HYBRID_NESTED_WITH_EDGES` | `GRAPH_EDGE_LIST` | `max_reference_span_tokens` | 3979.625 | 3979.625 |
| `expression_notation` | `POSTFIX_RPN` | `SEXPR_PREFIX` | `bpe_tokens_per_transition` | 7667.156 | 8701.281 |
| `syntax_family` | `BLOCK` | `SEXPR` | `detect_swap_records` | 0.909 | 0.909 |
| `block_delimiter` | `INDENT` | `BRACE` | `detect_drop_line` | 0.625 | 0.375 |
| `binder_encoding` | `DE_BRUIJN` | `NAMED` | `bpe_tokens_per_transition` | 7667.156 | 7667.156 |
| `binder_encoding` | `DE_BRUIJN` | `NAMED_PLUS_DE_BRUIJN` | `bpe_tokens_per_transition` | 9720.531 | 9861.844 |
| `syntax_family` | `SEXPR` | `BLOCK` | `detect_swap_records` | 0.909 | 0.792 |
| `block_delimiter` | `INDENT` | `KEYWORD_END` | `detect_drop_line` | 0.708 | 0.542 |
| `field_marker` | `COLON` | `EQUALS` | `bpe_tokens_per_transition` | 9720.531 | 9720.531 |
| `type_attachment` | `TYPE_FIELD` | `COLON_SUFFIX` | `bpe_tokens_per_transition` | 9898.156 | 9898.156 |
| `expression_notation` | `POSTFIX_RPN` | `FUNCTIONAL_APPLICATION` | `bpe_tokens_per_transition` | 7807.125 | 8634.281 |
| `syntax_family` | `INDENTED_TREE` | `JSONISH` | `detect_swap_records` | 0.909 | 0.909 |
| `application_style` | `CURRIED_BINARY` | `FLATTENED_SPINE` | `bpe_tokens_per_transition` | 7643.344 | 7738.562 |
| `syntax_family` | `TAGGED_LINE` | `PROSE` | `detect_swap_records` | 0.667 | 0.667 |
| `record_separator` | `NEWLINE` | `NEWLINE_BLANK` | `bpe_tokens_per_transition` | 9040.562 | 9045.562 |
| `lexicon_register` | `COMPACT_MNEMONIC` | `MATH_NOTATION` | `bpe_tokens_per_transition` | 9040.562 | 9070.781 |
| `lexicon_register` | `COMPACT_MNEMONIC` | `HUMAN_WORDS` | `bpe_tokens_per_transition` | 8634.281 | 8704.688 |
| `identity_sigil` | `NONE` | `BRACKETED` | `identifier_fragmentation` | 2.133 | 2.133 |
| `identity_sigil` | `NONE` | `PREFIX_SIGIL` | `identifier_fragmentation` | 1.976 | 1.976 |
| `role_word_length` | `FULL` | `SINGLE_CHAR` | `bpe_tokens_per_transition` | 9332.406 | 9332.406 |
| `lexicon_register` | `SYMBOLIC_ROLE` | `MATH_NOTATION` | `bpe_tokens_per_transition` | 20171.281 | 20254.625 |
| `lexicon_register` | `SYMBOLIC_ROLE` | `COMPACT_MNEMONIC` | `bpe_tokens_per_transition` | 20171.281 | 20311.344 |
| `keyword_case` | `LOWER` | `UPPER` | `bpe_tokens_per_transition` | 7977.000 | 7977.000 |
| `const_name_form` | `FULL_NAME` | `FULL_NAME_WITH_ALIAS_TABLE` | `identifier_fragmentation` | 1.931 | 1.931 |
| `field_marker` | `COLON` | `ARROW` | `bpe_tokens_per_transition` | 20171.281 | 20203.250 |
| `redundancy_level` | `LOW` | `EXPLICIT` | `detect_drop_field` | 0.917 | 0.542 |
| `redundancy_level` | `LOW` | `ERROR_CORRECTING` | `detect_drop_field` | 0.417 | 0.375 |
| `redundancy_level` | `NONE` | `LOW` | `detect_drop_field` | 0.000 | 0.000 |
| `syntax_family` | `BLOCK` | `INDENTED_TREE` | `detect_swap_records` | 0.909 | 0.909 |
| `delta_visibility` | `DERIVABLE_ONLY` | `EXPLICIT_DELTA_BLOCK` | `bpe_tokens_per_transition` | 7739.781 | 7960.656 |
| `syntax_family` | `TAGGED_LINE` | `JSONISH` | `detect_swap_records` | 0.667 | 0.652 |
| `graph_serialization` | `DFS_PREORDER` | `DEPENDENCY_LOCAL` | `max_reference_span_tokens` | 3314.938 | 3314.938 |
| `syntax_family` | `BLOCK` | `PROSE` | `detect_swap_records` | 0.875 | 0.696 |
| `context_order` | `REVERSE_INDEX` | `DECLARATION_INDEX` | `binder_use_distance_tokens` | 274.323 | 275.552 |

## Mutations the failure memory blocked

| Axis | Value | Reason |
|---|---|---|
| `graph_serialization` | `GOAL_CENTRED` | `BLOCKED_BY:FM-005` |

## Finalist profiles

### 1. `R_26259b75353b`

**Shortlisted because:** best_on:bpe_tokens_per_transition, best_on:identifier_fragmentation.

**Descends from:** `SEED_HEADER_PREMISE` via 6 recorded step(s); origin `SINGLE_AXIS`.

**Genome differences from that seed:** `context_order=REVERSE_INDEX`, `delta_visibility=DERIVABLE_ONLY`, `expression_notation=POSTFIX_RPN`, `goal_identity_visibility=BOTH`, `lexicon_register=MATH_NOTATION`, `syntax_family=PROSE`

| Metric | Value |
|---|---:|
| `binder_use_distance_chars` | 426.1555 |
| `binder_use_distance_tokens` | 194.2581 |
| `bpe_tokens_per_transition` | 7161.7188 |
| `bytes_per_transition` | 15822.0938 |
| `chars_per_transition` | 15722.625 |
| `detect_corrupt_identity` | 1.0 |
| `detect_drop_field` | 0.0 |
| `detect_drop_line` | 1.0 |
| `detect_reorder_scope` | 0.4583 |
| `detect_swap_records` | 0.6957 |
| `detect_truncate_tail` | 1.0 |
| `forward_reference_rate` | 0.4148 |
| `gzip_bytes_per_transition` | 1116.5 |
| `gzip_ratio` | 14.1712 |
| `identifier_fragmentation` | 1.803 |
| `max_reference_span_tokens` | 3176.0625 |
| `premise_to_action_distance_tokens` | 623.8673 |
| `pretokens_per_transition` | 5309.8438 |
| `role_vocabulary_entropy` | 3.4888 |
| `role_word_fragmentation` | 1.8333 |
| `structural_density` | 0.6235 |

<details><summary>Genome</summary>

| Axis | Value |
|---|---|
| `action_encoding` | `SOURCE_PLUS_STRUCTURED` |
| `action_position` | `TRAILER` |
| `alpha_normalization` | `NORMALIZED` |
| `application_style` | `CURRIED_BINARY` |
| `binder_encoding` | `DE_BRUIJN` |
| `binder_metadata` | `FULL` |
| `binder_use_reminder` | `NONE` |
| `block_delimiter` | `INDENT` |
| `checksum_policy` | `NONE` |
| `const_name_form` | `FULL_NAME` |
| `context_order` | `REVERSE_INDEX` |
| `count_assertions` | `NONE` |
| `delta_visibility` | `DERIVABLE_ONLY` |
| `dependency_visibility` | `INLINE_REFS` |
| `expression_notation` | `POSTFIX_RPN` |
| `field_marker` | `COLON` |
| `glyph_policy` | `UNICODE_NATIVE` |
| `goal_identity_visibility` | `BOTH` |
| `goal_position` | `AFTER_CONTEXT` |
| `graph_serialization` | `DFS_PREORDER` |
| `identity_scheme` | `SHORT_ID` |
| `identity_sigil` | `NONE` |
| `implicit_argument_visibility` | `ALL` |
| `keyword_case` | `LOWER` |
| `lexicon_register` | `MATH_NOTATION` |
| `list_syntax` | `BRACKET_COMMA` |
| `literal_form` | `TAGGED` |
| `local_instance_visibility` | `MERGED_INTO_CONTEXT` |
| `obligation_visibility` | `EXPLICIT_METAVAR_BLOCK` |
| `premise_locality` | `HEADER_BLOCK` |
| `provenance_visibility` | `IDENTITY_ONLY` |
| `record_separator` | `NEWLINE` |
| `redundancy_level` | `LOW` |
| `role_word_length` | `FULL` |
| `scope_metadata` | `IMPLICIT_BY_NESTING` |
| `shared_subterm_handling` | `DUPLICATE` |
| `state_partitioning` | `BEFORE_AFTER_FULL` |
| `syntax_family` | `PROSE` |
| `tree_vs_graph_projection` | `TREE_NESTED` |
| `type_attachment` | `TYPE_FIELD` |
| `type_explicitness` | `FULL_TREE` |
| `universe_visibility` | `FULL` |

</details>

### 2. `R_3c2d80a45f5f`

**Shortlisted because:** best_on:max_reference_span_tokens.

**Descends from:** `SEED_HYBRID_RPN_MACHINE` via 3 recorded step(s); origin `SINGLE_AXIS`.

**Genome differences from that seed:** `action_position=TRAILER`, `block_delimiter=KEYWORD_END`, `syntax_family=SEXPR`

| Metric | Value |
|---|---:|
| `binder_use_distance_chars` | 404.09 |
| `binder_use_distance_tokens` | 195.4709 |
| `bpe_tokens_per_transition` | 7337.0938 |
| `bytes_per_transition` | 15211.375 |
| `chars_per_transition` | 15209.4375 |
| `detect_corrupt_identity` | 1.0 |
| `detect_drop_field` | 0.0 |
| `detect_drop_line` | 0.875 |
| `detect_reorder_scope` | 0.4583 |
| `detect_swap_records` | 0.913 |
| `detect_truncate_tail` | 0.0 |
| `forward_reference_rate` | 0.0 |
| `gzip_bytes_per_transition` | 1184.8125 |
| `gzip_ratio` | 12.8386 |
| `identifier_fragmentation` | 2.1331 |
| `max_reference_span_tokens` | 3012.5312 |
| `premise_to_action_distance_tokens` | 882.4071 |
| `pretokens_per_transition` | 5227.6562 |
| `role_vocabulary_entropy` | 3.7418 |
| `role_word_fragmentation` | 1.3333 |
| `structural_density` | 0.6904 |

<details><summary>Genome</summary>

| Axis | Value |
|---|---|
| `action_encoding` | `SOURCE_PLUS_STRUCTURED` |
| `action_position` | `TRAILER` |
| `alpha_normalization` | `NORMALIZED` |
| `application_style` | `FLATTENED_SPINE` |
| `binder_encoding` | `DE_BRUIJN` |
| `binder_metadata` | `FULL` |
| `binder_use_reminder` | `NONE` |
| `block_delimiter` | `KEYWORD_END` |
| `checksum_policy` | `NONE` |
| `const_name_form` | `FULL_NAME` |
| `context_order` | `DECLARATION_INDEX` |
| `count_assertions` | `NONE` |
| `delta_visibility` | `EXPLICIT_DELTA_BLOCK` |
| `dependency_visibility` | `INLINE_REFS` |
| `expression_notation` | `POSTFIX_RPN` |
| `field_marker` | `COLON` |
| `glyph_policy` | `UNICODE_NATIVE` |
| `goal_identity_visibility` | `SEMANTIC_ID` |
| `goal_position` | `AFTER_CONTEXT` |
| `graph_serialization` | `DFS_PREORDER` |
| `identity_scheme` | `SHORT_ID` |
| `identity_sigil` | `NONE` |
| `implicit_argument_visibility` | `ALL` |
| `keyword_case` | `LOWER` |
| `lexicon_register` | `COMPACT_MNEMONIC` |
| `list_syntax` | `BRACKET_COMMA` |
| `literal_form` | `TAGGED` |
| `local_instance_visibility` | `MERGED_INTO_CONTEXT` |
| `obligation_visibility` | `EXPLICIT_METAVAR_BLOCK` |
| `premise_locality` | `ADJACENT_TO_ACTION` |
| `provenance_visibility` | `IDENTITY_ONLY` |
| `record_separator` | `NEWLINE` |
| `redundancy_level` | `LOW` |
| `role_word_length` | `FULL` |
| `scope_metadata` | `IMPLICIT_BY_NESTING` |
| `shared_subterm_handling` | `DUPLICATE` |
| `state_partitioning` | `BEFORE_AFTER_FULL` |
| `syntax_family` | `SEXPR` |
| `tree_vs_graph_projection` | `TREE_NESTED` |
| `type_attachment` | `TYPE_FIELD` |
| `type_explicitness` | `FULL_TREE` |
| `universe_visibility` | `FULL` |

</details>

### 3. `R_d51968446f17`

**Shortlisted because:** knee.

**Descends from:** `SEED_HEADER_PREMISE` via 6 recorded step(s); origin `SINGLE_AXIS`.

**Genome differences from that seed:** `checksum_policy=PER_STATE`, `context_order=REVERSE_INDEX`, `delta_visibility=DERIVABLE_ONLY`, `expression_notation=POSTFIX_RPN`, `goal_identity_visibility=BOTH`, `lexicon_register=MATH_NOTATION`

| Metric | Value |
|---|---:|
| `binder_use_distance_chars` | 412.5307 |
| `binder_use_distance_tokens` | 203.4928 |
| `bpe_tokens_per_transition` | 7422.0 |
| `bytes_per_transition` | 15449.5 |
| `chars_per_transition` | 15350.0312 |
| `detect_corrupt_identity` | 1.0 |
| `detect_drop_field` | 0.9167 |
| `detect_drop_line` | 0.5833 |
| `detect_reorder_scope` | 1.0 |
| `detect_swap_records` | 0.9545 |
| `detect_truncate_tail` | 0.7917 |
| `forward_reference_rate` | 0.4081 |
| `gzip_bytes_per_transition` | 1101.7188 |
| `gzip_ratio` | 14.0231 |
| `identifier_fragmentation` | 1.899 |
| `max_reference_span_tokens` | 3281.8438 |
| `premise_to_action_distance_tokens` | 647.9774 |
| `pretokens_per_transition` | 5164.375 |
| `role_vocabulary_entropy` | 3.3722 |
| `role_word_fragmentation` | 1.8333 |
| `structural_density` | 2.2631 |

<details><summary>Genome</summary>

| Axis | Value |
|---|---|
| `action_encoding` | `SOURCE_PLUS_STRUCTURED` |
| `action_position` | `TRAILER` |
| `alpha_normalization` | `NORMALIZED` |
| `application_style` | `CURRIED_BINARY` |
| `binder_encoding` | `DE_BRUIJN` |
| `binder_metadata` | `FULL` |
| `binder_use_reminder` | `NONE` |
| `block_delimiter` | `INDENT` |
| `checksum_policy` | `PER_STATE` |
| `const_name_form` | `FULL_NAME` |
| `context_order` | `REVERSE_INDEX` |
| `count_assertions` | `NONE` |
| `delta_visibility` | `DERIVABLE_ONLY` |
| `dependency_visibility` | `INLINE_REFS` |
| `expression_notation` | `POSTFIX_RPN` |
| `field_marker` | `COLON` |
| `glyph_policy` | `UNICODE_NATIVE` |
| `goal_identity_visibility` | `BOTH` |
| `goal_position` | `AFTER_CONTEXT` |
| `graph_serialization` | `DFS_PREORDER` |
| `identity_scheme` | `SHORT_ID` |
| `identity_sigil` | `NONE` |
| `implicit_argument_visibility` | `ALL` |
| `keyword_case` | `LOWER` |
| `lexicon_register` | `MATH_NOTATION` |
| `list_syntax` | `BRACKET_COMMA` |
| `literal_form` | `TAGGED` |
| `local_instance_visibility` | `MERGED_INTO_CONTEXT` |
| `obligation_visibility` | `EXPLICIT_METAVAR_BLOCK` |
| `premise_locality` | `HEADER_BLOCK` |
| `provenance_visibility` | `IDENTITY_ONLY` |
| `record_separator` | `NEWLINE` |
| `redundancy_level` | `LOW` |
| `role_word_length` | `FULL` |
| `scope_metadata` | `IMPLICIT_BY_NESTING` |
| `shared_subterm_handling` | `DUPLICATE` |
| `state_partitioning` | `BEFORE_AFTER_FULL` |
| `syntax_family` | `BLOCK` |
| `tree_vs_graph_projection` | `TREE_NESTED` |
| `type_attachment` | `TYPE_FIELD` |
| `type_explicitness` | `FULL_TREE` |
| `universe_visibility` | `FULL` |

</details>

### 4. `R_07e59bff963f`

**Shortlisted because:** best_on:detect_drop_field.

**Descends from:** `SEED_HEADER_PREMISE` via 6 recorded step(s); origin `SINGLE_AXIS`.

**Genome differences from that seed:** `block_delimiter=KEYWORD_END`, `context_order=REVERSE_INDEX`, `delta_visibility=DERIVABLE_ONLY`, `expression_notation=POSTFIX_RPN`, `goal_identity_visibility=BOTH`, `lexicon_register=COMPACT_MNEMONIC`

| Metric | Value |
|---|---:|
| `binder_use_distance_chars` | 426.852 |
| `binder_use_distance_tokens` | 206.2414 |
| `bpe_tokens_per_transition` | 7512.7812 |
| `bytes_per_transition` | 15773.7812 |
| `chars_per_transition` | 15771.8438 |
| `detect_corrupt_identity` | 1.0 |
| `detect_drop_field` | 0.9167 |
| `detect_drop_line` | 0.4583 |
| `detect_reorder_scope` | 1.0 |
| `detect_swap_records` | 0.9565 |
| `detect_truncate_tail` | 0.0 |
| `forward_reference_rate` | 0.4081 |
| `gzip_bytes_per_transition` | 1090.9062 |
| `gzip_ratio` | 14.4593 |
| `identifier_fragmentation` | 1.8649 |
| `max_reference_span_tokens` | 3314.9375 |
| `premise_to_action_distance_tokens` | 1033.5673 |
| `pretokens_per_transition` | 5281.7188 |
| `role_vocabulary_entropy` | 3.6358 |
| `role_word_fragmentation` | 1.3333 |
| `structural_density` | 2.7769 |

<details><summary>Genome</summary>

| Axis | Value |
|---|---|
| `action_encoding` | `SOURCE_PLUS_STRUCTURED` |
| `action_position` | `TRAILER` |
| `alpha_normalization` | `NORMALIZED` |
| `application_style` | `CURRIED_BINARY` |
| `binder_encoding` | `DE_BRUIJN` |
| `binder_metadata` | `FULL` |
| `binder_use_reminder` | `NONE` |
| `block_delimiter` | `KEYWORD_END` |
| `checksum_policy` | `NONE` |
| `const_name_form` | `FULL_NAME` |
| `context_order` | `REVERSE_INDEX` |
| `count_assertions` | `NONE` |
| `delta_visibility` | `DERIVABLE_ONLY` |
| `dependency_visibility` | `INLINE_REFS` |
| `expression_notation` | `POSTFIX_RPN` |
| `field_marker` | `COLON` |
| `glyph_policy` | `UNICODE_NATIVE` |
| `goal_identity_visibility` | `BOTH` |
| `goal_position` | `AFTER_CONTEXT` |
| `graph_serialization` | `DFS_PREORDER` |
| `identity_scheme` | `SHORT_ID` |
| `identity_sigil` | `NONE` |
| `implicit_argument_visibility` | `ALL` |
| `keyword_case` | `LOWER` |
| `lexicon_register` | `COMPACT_MNEMONIC` |
| `list_syntax` | `BRACKET_COMMA` |
| `literal_form` | `TAGGED` |
| `local_instance_visibility` | `MERGED_INTO_CONTEXT` |
| `obligation_visibility` | `EXPLICIT_METAVAR_BLOCK` |
| `premise_locality` | `HEADER_BLOCK` |
| `provenance_visibility` | `IDENTITY_ONLY` |
| `record_separator` | `NEWLINE` |
| `redundancy_level` | `LOW` |
| `role_word_length` | `FULL` |
| `scope_metadata` | `IMPLICIT_BY_NESTING` |
| `shared_subterm_handling` | `DUPLICATE` |
| `state_partitioning` | `BEFORE_AFTER_FULL` |
| `syntax_family` | `BLOCK` |
| `tree_vs_graph_projection` | `TREE_NESTED` |
| `type_attachment` | `TYPE_FIELD` |
| `type_explicitness` | `FULL_TREE` |
| `universe_visibility` | `FULL` |

</details>

### 5. `R_f3d7d713e16a`

**Shortlisted because:** best_on:premise_to_action_distance_tokens.

**Descends from:** `SEED_CANONICAL_SEXPR` via 3 recorded step(s); origin `SINGLE_AXIS`.

**Genome differences from that seed:** `action_position=HEADER`, `lexicon_register=SYMBOLIC_ROLE`

| Metric | Value |
|---|---:|
| `binder_use_distance_chars` | 475.5902 |
| `binder_use_distance_tokens` | 241.7673 |
| `bpe_tokens_per_transition` | 9017.2812 |
| `bytes_per_transition` | 17835.9375 |
| `chars_per_transition` | 17834.0 |
| `detect_corrupt_identity` | 1.0 |
| `detect_drop_field` | 0.0 |
| `detect_drop_line` | 0.8333 |
| `detect_reorder_scope` | 0.4167 |
| `detect_swap_records` | 0.8636 |
| `detect_truncate_tail` | 0.0 |
| `forward_reference_rate` | 0.0 |
| `gzip_bytes_per_transition` | 1190.7188 |
| `gzip_ratio` | 14.9791 |
| `identifier_fragmentation` | 1.9331 |
| `max_reference_span_tokens` | 3740.6875 |
| `premise_to_action_distance_tokens` | 49.2988 |
| `pretokens_per_transition` | 6860.9375 |
| `role_vocabulary_entropy` | 3.4053 |
| `role_word_fragmentation` | 1.1667 |
| `structural_density` | 0.5618 |

<details><summary>Genome</summary>

| Axis | Value |
|---|---|
| `action_encoding` | `SOURCE_PLUS_STRUCTURED` |
| `action_position` | `HEADER` |
| `alpha_normalization` | `NORMALIZED` |
| `application_style` | `CURRIED_BINARY` |
| `binder_encoding` | `DE_BRUIJN` |
| `binder_metadata` | `FULL` |
| `binder_use_reminder` | `NONE` |
| `block_delimiter` | `INDENT` |
| `checksum_policy` | `NONE` |
| `const_name_form` | `FULL_NAME` |
| `context_order` | `DECLARATION_INDEX` |
| `count_assertions` | `NONE` |
| `delta_visibility` | `EXPLICIT_DELTA_BLOCK` |
| `dependency_visibility` | `INLINE_REFS` |
| `expression_notation` | `SEXPR_PREFIX` |
| `field_marker` | `COLON` |
| `glyph_policy` | `UNICODE_NATIVE` |
| `goal_identity_visibility` | `SEMANTIC_ID` |
| `goal_position` | `AFTER_CONTEXT` |
| `graph_serialization` | `DFS_PREORDER` |
| `identity_scheme` | `SHORT_ID` |
| `identity_sigil` | `NONE` |
| `implicit_argument_visibility` | `ALL` |
| `keyword_case` | `LOWER` |
| `lexicon_register` | `SYMBOLIC_ROLE` |
| `list_syntax` | `BRACKET_COMMA` |
| `literal_form` | `TAGGED` |
| `local_instance_visibility` | `MERGED_INTO_CONTEXT` |
| `obligation_visibility` | `EXPLICIT_METAVAR_BLOCK` |
| `premise_locality` | `ADJACENT_TO_ACTION` |
| `provenance_visibility` | `IDENTITY_ONLY` |
| `record_separator` | `NEWLINE` |
| `redundancy_level` | `NONE` |
| `role_word_length` | `FULL` |
| `scope_metadata` | `IMPLICIT_BY_NESTING` |
| `shared_subterm_handling` | `DUPLICATE` |
| `state_partitioning` | `BEFORE_AFTER_FULL` |
| `syntax_family` | `SEXPR` |
| `tree_vs_graph_projection` | `TREE_NESTED` |
| `type_attachment` | `TYPE_FIELD` |
| `type_explicitness` | `FULL_TREE` |
| `universe_visibility` | `FULL` |

</details>


## Which axes this corpus can speak to

Every single-axis mutation whose child measured identically to its parent is evidence that the axis has no effect **on this corpus** — not that it is a bad axis. Reporting it is more useful than reporting a search that appears to have explored it.

| Axis | Single-axis mutations | Changed the measurement | Share |
|---|---:|---:|---:|
| `const_name_form` | 2 | 0 | 0% |
| `graph_serialization` | 11 | 0 | 0% |
| `keyword_case` | 1 | 0 | 0% |
| `local_instance_visibility` | 2 | 0 | 0% |
| `role_word_length` | 2 | 0 | 0% |
| `type_attachment` | 1 | 0 | 0% |
| `goal_position` | 6 | 1 | 17% |
| `premise_locality` | 5 | 1 | 20% |
| `field_marker` | 2 | 1 | 50% |
| `redundancy_level` | 12 | 6 | 50% |
| `binder_encoding` | 7 | 5 | 71% |
| `tree_vs_graph_projection` | 9 | 8 | 89% |
| `context_order` | 10 | 9 | 90% |
| `action_encoding` | 2 | 2 | 100% |
| `action_position` | 6 | 6 | 100% |
| `alpha_normalization` | 3 | 3 | 100% |
| `application_style` | 3 | 3 | 100% |
| `binder_use_reminder` | 4 | 4 | 100% |
| `block_delimiter` | 4 | 4 | 100% |
| `checksum_policy` | 3 | 3 | 100% |
| `count_assertions` | 2 | 2 | 100% |
| `delta_visibility` | 2 | 2 | 100% |
| `expression_notation` | 5 | 5 | 100% |
| `goal_identity_visibility` | 1 | 1 | 100% |
| `identity_scheme` | 1 | 1 | 100% |
| `identity_sigil` | 5 | 5 | 100% |
| `lexicon_register` | 13 | 13 | 100% |
| `list_syntax` | 2 | 2 | 100% |
| `literal_form` | 1 | 1 | 100% |
| `provenance_visibility` | 2 | 2 | 100% |
| `record_separator` | 1 | 1 | 100% |
| `scope_metadata` | 1 | 1 | 100% |
| `shared_subterm_handling` | 2 | 2 | 100% |
| `syntax_family` | 13 | 13 | 100% |

### Largest groups of candidates that measure identically

| Candidates | Group size |
|---|---:|
| `R_124568b25991`, `R_5d5c1e231af2`, `R_7943f3bad185`, `R_ca96225a3105` and 4 more | 8 |
| `R_8b297a184ca2`, `R_8dfb038fbaee`, `R_d09714dfaab5`, `R_e6b1d8e8e992` and 1 more | 5 |
| `R_07e59bff963f`, `R_09976fa51d66`, `R_72e243fe3dce`, `R_f5966e97e791` | 4 |
| `R_09eef74441f2`, `R_0b69bd4ddbfc`, `R_1d441775d5fc`, `R_f8c6e06c24ad` | 4 |
| `R_7e6d29d9faa7`, `R_97bec3a66267`, `R_a0ddbc4d5ca3`, `R_f88bd2345a61` | 4 |
| `R_0efd778653d8`, `R_2ec8cdca17ba`, `R_717f85b2ff79` | 3 |
| `R_3227a8ac3a06`, `R_6eb003bf8b58`, `R_c78387a58962` | 3 |
| `R_3de8b45034d1`, `R_c6e19b272841`, `R_e14b56bb2695` | 3 |
| `R_4f7435f0252a`, `R_7313e666736f`, `R_a4bb78b644b2` | 3 |
| `R_93fd5967d1e2`, `R_be204d70d432`, `R_da06b2129f21` | 3 |
| `R_02a757cf3ef8`, `R_1c9b5e72a8c1` | 2 |
| `R_0eaf36f22de1`, `R_9d23ae334dc3` | 2 |

## Sealed evaluation

Not yet run. The sealed split has never been read.

## What this does not establish

- That any of these representations makes mathematical reasoning easier for a model. No model was run, and `FM-003` records that on the last task most of the measured accuracy was lexical.
- That the token rankings generalise. They are measured under one pinned GPT-2 vocabulary; the prior audit used Qwen3-8B, where every mathematical glyph the corpus needs is a single token and these numbers would differ.
- That the frontier is the global frontier. The space has 4.095e+19 points and this search evaluated 165.

The next step that would change any of this is a matched, controlled model experiment on the finalists, gated by the six lexical controls `FM-003` requires.
