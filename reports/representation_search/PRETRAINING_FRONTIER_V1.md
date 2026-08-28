# PRETRAINING_REPRESENTATION_FRONTIER_V1

**This is not a claim that any representation is optimal for neural mathematical reasoning.** It is the strongest Pareto frontier obtainable from static evidence before model adaptation, together with the evidence that produced it.

## Provenance

| Field | Value |
|---|---|
| Compiler | `representation-compiler-v1.0.0` |
| Canonical state | `canonical-math-transition-v2.0.0` |
| Genome axes | 42 |
| Search space | 4.095e+19 points |
| Corpus transitions | 608 |
| Mathlib domains | 27 |
| Generations completed | 30 |
| Candidates registered | 616 |
| Candidates evaluated | 489 |
| Candidates hard-rejected | 107 |
| Strict Pareto front | 92 |
| Distinct measurement vectors | 328 |
| Reported finalists | 6 |

## Corpus split

| Split | Transitions | Families |
|---|---|---|
| `SEARCH_DEV` | 421 | 323 |
| `SEARCH_VALIDATION` | 67 | 54 |
| `SEALED_FINAL_EVALUATION` | 120 | 101 |

Split unit: `MATHLIB_SOURCE_FILE`. Families hash `b75c99e695393069`.

## The frontier

Strict non-dominated sorting over seven axes leaves 92 of 489 evaluated candidates on the front, and an epsilon-front at eps=0.02 still keeps 266. With enough axes almost every candidate is best at something, so neither is a shortlist.

The finalists below follow a rule that states why each one is present: **the best candidate on each Pareto axis taken alone, plus the knee** - the candidate closest to the ideal point after per-axis normalisation. Candidates with identical measurement vectors are collapsed first. Selection during the search used the strict front, so this reporting rule could not have steered it.

| # | Candidate | Shortlisted because | BPE tokens | Binder distance | Premise distance | Swap detect | Drop-field detect | Ident. frag | Max span |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | `R_c8a70a62eebb` | best_on:bpe_tokens_per_transition, best_on:premise_to_action_distance_tokens, best_on:max_reference_span_tokens | 5130.6 | 190.7 | 11.5 | 0.708 | 0.000 | 1.83 | 2339.2 |
| 2 | `R_211cd0165db9` | best_on:detect_swap_records | 5416.2 | 200.3 | 211.6 | 1.000 | 0.708 | 1.84 | 2831.4 |
| 3 | `R_0412a34e70c7` | best_on:detect_drop_field | 5450.0 | 203.6 | 612.1 | 0.739 | 0.833 | 1.90 | 2867.7 |
| 4 | `R_9044f4984fce` | knee | 5495.5 | 191.0 | 18.2 | 0.917 | 0.750 | 1.84 | 2570.3 |
| 5 | `R_cf8323f05a83` | best_on:identifier_fragmentation | 8124.9 | 257.8 | 415.1 | 0.750 | 0.000 | 1.71 | 3142.3 |
| 6 | `R_9f3eb215d943` | best_on:binder_use_distance_tokens | 13677.0 | 159.8 | 843.5 | 0.542 | 0.000 | 1.83 | 3659.7 |

## Controls

Every seeded baseline, whether or not it survived. `FM-002` and `FM-006` require the recorded baselines to remain visible for the whole search. Token rank is out of the whole evaluated population, lower is cheaper.

| Baseline | Status | Strict front | Finalist | Token rank | BPE tokens | Binder distance | Rejection |
|---|---|---|---|---:|---:|---:|---|
| `SEED_CANONICAL_SEXPR` | EVALUATED | no | no | 232 | 6978 | 246 | — |
| `SEED_DELTA_FIRST` | EVALUATED | no | no | 305 | 7362 | 246 | — |
| `SEED_DEPENDENCY_TOPOLOGICAL` | EVALUATED | no | no | 307 | 7362 | 262 | — |
| `SEED_EXPLICIT_REDUNDANT` | EVALUATED | no | no | 379 | 8087 | 296 | — |
| `SEED_GOAL_LOCAL` | EVALUATED | no | no | 349 | 7576 | 270 | — |
| `SEED_GRAPH_EDGE` | EVALUATED | no | no | 362 | 7782 | 247 | — |
| `SEED_HEADER_PREMISE` | EVALUATED | no | no | 318 | 7365 | 256 | — |
| `SEED_HYBRID_COMPACT_BLOCK` | EVALUATED | no | no | 217 | 6792 | 242 | — |
| `SEED_HYBRID_LOCAL_DAG` | EVALUATED | no | no | 463 | 17144 | 193 | — |
| `SEED_HYBRID_RPN_MACHINE` | EVALUATED | no | no | 154 | 5979 | 212 | — |
| `SEED_JSON_BASELINE` | EVALUATED | no | no | 269 | 7203 | 256 | — |
| `SEED_LEAN_LIKE` | EVALUATED | no | no | 405 | 9196 | 336 | — |
| `SEED_MINIMAL_MACHINE` | EVALUATED | no | no | 180 | 6106 | 224 | — |
| `SEED_PRIOR_HML` | EVALUATED | no | no | 306 | 7362 | 262 | — |
| `SEED_STRUCTURED_ENGLISH` | EVALUATED | no | no | 401 | 8956 | 327 | — |
| `SEED_TYPED_AST` | EVALUATED | no | no | 393 | 8552 | 304 | — |

## Generations

| Gen | Phase | Evaluated | Rejected | Front | Frontier moved | Memory blocks | Refuted | Seconds |
|---|---|---:|---:|---:|---|---:|---:|---:|
| 0 | A | 16 | 0 | 12 | yes | 0 | 0 | 31.2 |
| 1 | A | 30 | 6 | 19 | yes | 0 | 9 | 27.1 |
| 2 | B | 38 | 10 | 22 | no | 30 | 16 | 25.1 |
| 3 | B | 48 | 0 | 34 | yes | 68 | 22 | 45.5 |
| 4 | B | 48 | 0 | 41 | no | 91 | 24 | 45.6 |
| 5 | C | 48 | 0 | 44 | yes | 0 | 27 | 49.8 |
| 6 | C | 48 | 0 | 34 | yes | 0 | 29 | 41.6 |
| 7 | D | 48 | 0 | 30 | yes | 0 | 24 | 41.0 |
| 8 | D | 44 | 4 | 27 | no | 0 | 20 | 48.9 |
| 9 | — | 39 | 9 | 30 | no | 27 | 17 | 20.6 |
| 10 | — | 45 | 3 | 39 | yes | 36 | 25 | 40.0 |
| 11 | — | 44 | 4 | 32 | yes | 36 | 23 | 33.9 |
| 12 | — | 44 | 4 | 35 | no | 36 | 27 | 46.4 |
| 13 | — | 41 | 7 | 34 | no | 37 | 24 | 25.1 |
| 14 | — | 45 | 3 | 37 | yes | 41 | 25 | 47.0 |
| 15 | — | 44 | 4 | 23 | yes | 26 | 24 | 44.7 |
| 16 | — | 47 | 1 | 26 | no | 34 | 25 | 39.6 |
| 17 | — | 45 | 3 | 32 | yes | 57 | 26 | 36.0 |
| 18 | — | 41 | 7 | 33 | yes | 48 | 24 | 28.1 |
| 19 | — | 42 | 6 | 34 | no | 49 | 22 | 29.9 |
| 20 | — | 43 | 5 | 35 | no | 49 | 22 | 34.6 |
| 21 | — | 45 | 3 | 37 | no | 58 | 23 | 31.7 |
| 22 | — | 44 | 4 | 33 | no | 55 | 20 | 46.5 |
| 23 | — | 44 | 4 | 27 | yes | 41 | 23 | 34.8 |
| 24 | — | 46 | 2 | 29 | no | 55 | 20 | 43.4 |
| 25 | — | 42 | 6 | 27 | yes | 48 | 23 | 27.9 |
| 26 | — | 43 | 5 | 29 | yes | 57 | 25 | 22.2 |
| 27 | — | 45 | 3 | 33 | yes | 53 | 24 | 38.9 |
| 28 | — | 46 | 2 | 34 | yes | 54 | 23 | 53.1 |
| 29 | — | 46 | 2 | 29 | no | 47 | 25 | 43.7 |

## Why candidates were rejected

Rejections are evidence, not waste: they are what demonstrates that the hard gates bite.

| Reason | Candidates |
|---|---:|
| `semantic_round_trip` | 82 |
| `AMBIGUOUS_LEXICON` | 13 |
| `glyph_fidelity_utf8` | 12 |

## Refuted hypotheses

661 proposed mutations moved their target metric the wrong way. Each is a recorded negative result.

| Axis | From | To | Metric | Parent | Child |
|---|---|---|---|---:|---:|
| `action_position` | `BETWEEN_STATES` | `TRAILER` | `premise_to_action_distance_tokens` | 352.460 | 738.558 |
| `goal_position` | `AFTER_CONTEXT` | `INLINE_WITH_CONTEXT` | `premise_to_action_distance_tokens` | 378.880 | 378.880 |
| `identity_scheme` | `SHORT_ID` | `DISPLAY_PLUS_SHORT_ID` | `identifier_fragmentation` | 2.008 | 2.321 |
| `local_instance_visibility` | `MERGED_INTO_CONTEXT` | `EXPLICIT` | `bpe_tokens_per_transition` | 6978.200 | 6978.200 |
| `goal_identity_visibility` | `SEMANTIC_ID` | `BOTH` | `bpe_tokens_per_transition` | 7365.325 | 7377.575 |
| `provenance_visibility` | `NONE` | `IDENTITY_ONLY` | `bpe_tokens_per_transition` | 6105.575 | 6142.200 |
| `state_partitioning` | `BEFORE_AFTER_FULL` | `INTERLEAVED_BY_GOAL` | `bpe_tokens_per_transition` | 7575.550 | 7575.550 |
| `goal_position` | `AFTER_CONTEXT` | `LAST` | `premise_to_action_distance_tokens` | 2316.804 | 2316.804 |
| `goal_position` | `AFTER_CONTEXT` | `FIRST` | `premise_to_action_distance_tokens` | 54.215 | 54.215 |
| `goal_position` | `LAST` | `INLINE_WITH_CONTEXT` | `premise_to_action_distance_tokens` | 2316.804 | 2316.804 |
| `identity_scheme` | `SHORT_ID` | `SEMANTIC_ID` | `identifier_fragmentation` | 1.955 | 1.955 |
| `redundancy_level` | `LOW` | `NONE` | `detect_drop_field` | 0.000 | 0.000 |
| `context_order` | `DEPENDENCY_TOPOLOGICAL` | `DECLARATION_INDEX` | `binder_use_distance_tokens` | 234.789 | 234.789 |
| `redundancy_level` | `LOW` | `ERROR_CORRECTING` | `detect_drop_field` | 0.750 | 0.708 |
| `graph_serialization` | `DFS_PREORDER` | `NODE_LIST_THEN_EDGES` | `max_reference_span_tokens` | 3059.700 | 3059.700 |
| `graph_serialization` | `DFS_PREORDER` | `TOPOLOGICAL` | `max_reference_span_tokens` | 2980.875 | 2980.875 |
| `premise_locality` | `ADJACENT_TO_ACTION` | `TRAILING_BLOCK` | `premise_to_action_distance_tokens` | 63.165 | 63.165 |
| `premise_locality` | `HEADER_BLOCK` | `ADJACENT_TO_ACTION` | `premise_to_action_distance_tokens` | 762.056 | 803.880 |
| `count_assertions` | `NONE` | `PER_BLOCK` | `detect_drop_line` | 0.625 | 0.625 |
| `redundancy_level` | `LOW` | `EXPLICIT` | `detect_drop_field` | 0.750 | 0.667 |
| `graph_serialization` | `DEPENDENCY_LOCAL` | `DFS_PREORDER` | `max_reference_span_tokens` | 4802.275 | 4802.275 |
| `graph_serialization` | `DFS_PREORDER` | `EDGE_LIST` | `max_reference_span_tokens` | 3293.150 | 3293.150 |
| `graph_serialization` | `TOPOLOGICAL` | `DEPENDENCY_LOCAL` | `max_reference_span_tokens` | 2980.875 | 2980.875 |
| `redundancy_level` | `LOW` | `SELECTIVE` | `detect_drop_field` | 0.625 | 0.625 |
| `tree_vs_graph_projection` | `HYBRID_NESTED_WITH_EDGES` | `GRAPH_EDGE_LIST` | `max_reference_span_tokens` | 4802.425 | 4802.425 |
| `checksum_policy` | `NONE` | `PER_STATE` | `detect_corrupt_identity` | 1.000 | 1.000 |
| `graph_serialization` | `DEPENDENCY_LOCAL` | `NODE_LIST_THEN_EDGES` | `max_reference_span_tokens` | 4802.425 | 4802.425 |
| `graph_serialization` | `NODE_LIST_THEN_EDGES` | `BFS` | `max_reference_span_tokens` | 3059.700 | 3059.700 |
| `graph_serialization` | `DEPENDENCY_LOCAL` | `EDGE_LIST` | `max_reference_span_tokens` | 4629.300 | 4629.300 |
| `premise_locality` | `HEADER_BLOCK` | `TRAILING_BLOCK` | `premise_to_action_distance_tokens` | 2274.980 | 2316.804 |
| `graph_serialization` | `DFS_PREORDER` | `DEPENDENCY_LOCAL` | `max_reference_span_tokens` | 2690.275 | 2690.275 |
| `graph_serialization` | `TOPOLOGICAL` | `DFS_PREORDER` | `max_reference_span_tokens` | 2925.325 | 2925.325 |
| `context_order` | `DEPENDENCY_TOPOLOGICAL` | `REVERSE_INDEX` | `binder_use_distance_tokens` | 240.678 | 240.758 |
| `expression_notation` | `POSTFIX_RPN` | `TAGGED_NESTED` | `bpe_tokens_per_transition` | 6169.275 | 7753.400 |
| `field_marker` | `COLON` | `EQUALS` | `bpe_tokens_per_transition` | 17144.275 | 17144.275 |
| `syntax_family` | `BLOCK` | `INDENTED_TREE` | `detect_swap_records` | 0.458 | 0.458 |
| `binder_encoding` | `DE_BRUIJN` | `NAMED` | `bpe_tokens_per_transition` | 6978.200 | 7071.775 |
| `syntax_family` | `BLOCK` | `JSONISH` | `detect_swap_records` | 0.875 | 0.870 |
| `application_style` | `FLATTENED_SPINE` | `CURRIED_BINARY` | `bpe_tokens_per_transition` | 6791.500 | 7307.900 |
| `field_marker` | `COLON` | `ARROW` | `bpe_tokens_per_transition` | 6795.500 | 6795.500 |
| `syntax_family` | `BLOCK` | `PROSE` | `detect_swap_records` | 0.750 | 0.667 |
| `syntax_family` | `BLOCK` | `TAGGED_LINE` | `detect_swap_records` | 0.750 | 0.667 |
| `syntax_family` | `BLOCK` | `SEXPR` | `detect_swap_records` | 0.909 | 0.870 |
| `record_separator` | `NEWLINE` | `NEWLINE_BLANK` | `bpe_tokens_per_transition` | 7374.575 | 7379.575 |
| `expression_notation` | `SEXPR_PREFIX` | `TAGGED_NESTED` | `bpe_tokens_per_transition` | 7148.625 | 8355.975 |
| `syntax_family` | `SEXPR` | `JSONISH` | `detect_swap_records` | 0.870 | 0.870 |
| `syntax_family` | `TAGGED_LINE` | `PROSE` | `detect_swap_records` | 0.750 | 0.750 |
| `expression_notation` | `POSTFIX_RPN` | `FUNCTIONAL_APPLICATION` | `bpe_tokens_per_transition` | 5962.175 | 7277.325 |
| `syntax_family` | `INDENTED_TREE` | `BLOCK` | `detect_swap_records` | 0.875 | 0.875 |
| `lexicon_register` | `HUMAN_WORDS` | `COMPACT_MNEMONIC` | `bpe_tokens_per_transition` | 17147.275 | 17205.875 |
| `const_name_form` | `FULL_NAME` | `FULL_NAME_WITH_ALIAS_TABLE` | `identifier_fragmentation` | 1.951 | 1.951 |
| `lexicon_register` | `COMPACT_MNEMONIC` | `HUMAN_WORDS` | `bpe_tokens_per_transition` | 7210.650 | 7265.075 |
| `identity_sigil` | `NONE` | `PREFIX_SIGIL` | `identifier_fragmentation` | 1.994 | 1.994 |
| `identity_sigil` | `NONE` | `BRACKETED` | `identifier_fragmentation` | 1.894 | 1.894 |
| `lexicon_register` | `SYMBOLIC_ROLE` | `MATH_NOTATION` | `bpe_tokens_per_transition` | 6105.575 | 6181.725 |
| `keyword_case` | `LOWER` | `UPPER` | `bpe_tokens_per_transition` | 7781.675 | 8104.800 |
| `alpha_normalization` | `NORMALIZED` | `PRESERVE_DISPLAY` | `bpe_tokens_per_transition` | 17034.650 | 17326.975 |
| `redundancy_level` | `NONE` | `ERROR_CORRECTING` | `detect_drop_field` | 0.000 | 0.000 |
| `field_marker` | `EQUALS` | `ARROW` | `bpe_tokens_per_transition` | 7291.800 | 7291.800 |
| `goal_position` | `FIRST` | `LAST` | `premise_to_action_distance_tokens` | 2145.785 | 2145.785 |
| `redundancy_level` | `EXPLICIT` | `LOW` | `detect_drop_field` | 0.000 | 0.000 |
| `universe_visibility` | `FULL` | `ELIDED_WHEN_TRIVIAL` | `bpe_tokens_per_transition` | 5736.225 | 5736.225 |
| `redundancy_level` | `SELECTIVE` | `LOW` | `detect_drop_field` | 0.042 | 0.042 |
| `goal_position` | `FIRST` | `INLINE_WITH_CONTEXT` | `premise_to_action_distance_tokens` | 2145.785 | 2145.785 |
| `graph_serialization` | `TOPOLOGICAL` | `EDGE_LIST` | `max_reference_span_tokens` | 3404.750 | 3404.750 |
| `block_delimiter` | `INDENT` | `KEYWORD_END` | `detect_drop_line` | 0.750 | 0.542 |
| `lexicon_register` | `SYMBOLIC_ROLE` | `COMPACT_MNEMONIC` | `bpe_tokens_per_transition` | 17031.650 | 17201.875 |
| `expression_notation` | `POSTFIX_RPN` | `SEXPR_PREFIX` | `bpe_tokens_per_transition` | 5736.225 | 7208.450 |
| `alpha_normalization` | `NORMALIZED` | `BOTH` | `bpe_tokens_per_transition` | 5736.225 | 6028.550 |
| `tree_vs_graph_projection` | `TREE_NESTED` | `HYBRID_NESTED_WITH_EDGES` | `max_reference_span_tokens` | 2629.050 | 2833.125 |
| `graph_serialization` | `DEPENDENCY_LOCAL` | `TOPOLOGICAL` | `max_reference_span_tokens` | 4598.425 | 4598.425 |
| `type_attachment` | `TYPE_FIELD` | `COLON_SUFFIX` | `bpe_tokens_per_transition` | 7265.075 | 7265.075 |
| `graph_serialization` | `DFS_PREORDER` | `BFS` | `max_reference_span_tokens` | 3770.825 | 3770.825 |
| `scope_metadata` | `IMPLICIT_BY_NESTING` | `EXPLICIT_SCOPE_IDS` | `bpe_tokens_per_transition` | 7265.075 | 7478.300 |
| `graph_serialization` | `EDGE_LIST` | `BFS` | `max_reference_span_tokens` | 3509.200 | 3509.200 |
| `context_order` | `DECLARATION_INDEX` | `DEPENDENCY_TOPOLOGICAL` | `binder_use_distance_tokens` | 301.600 | 301.600 |
| `literal_form` | `BARE` | `TAGGED` | `bpe_tokens_per_transition` | 15936.950 | 15949.650 |
| `redundancy_level` | `EXPLICIT` | `ERROR_CORRECTING` | `detect_drop_field` | 0.500 | 0.500 |
| `universe_visibility` | `ELIDED_WHEN_TRIVIAL` | `FULL` | `bpe_tokens_per_transition` | 16966.650 | 17031.650 |
| `dependency_visibility` | `INLINE_REFS` | `EXPLICIT_EDGES` | `bpe_tokens_per_transition` | 5537.150 | 5575.450 |
| `redundancy_level` | `NONE` | `EXPLICIT` | `detect_drop_field` | 0.625 | 0.458 |
| `syntax_family` | `INDENTED_TREE` | `PROSE` | `detect_swap_records` | 0.913 | 0.708 |
| `alpha_normalization` | `BOTH` | `PRESERVE_DISPLAY` | `bpe_tokens_per_transition` | 6062.800 | 6062.800 |
| `graph_serialization` | `DEPENDENCY_LOCAL` | `BFS` | `max_reference_span_tokens` | 4779.000 | 4779.000 |
| `list_syntax` | `BRACKET_COMMA` | `PAREN` | `bpe_tokens_per_transition` | 5575.450 | 5596.875 |
| `delta_visibility` | `DERIVABLE_ONLY` | `EXPLICIT_DELTA_BLOCK` | `bpe_tokens_per_transition` | 5450.000 | 5675.950 |
| `type_attachment` | `COLON_SUFFIX` | `TYPE_FIELD` | `bpe_tokens_per_transition` | 6227.850 | 6227.850 |
| `state_partitioning` | `INTERLEAVED_BY_GOAL` | `BEFORE_AFTER_FULL` | `bpe_tokens_per_transition` | 5675.950 | 5675.950 |
| `graph_serialization` | `BFS` | `EDGE_LIST` | `max_reference_span_tokens` | 4779.000 | 4779.000 |
| `redundancy_level` | `NONE` | `SELECTIVE` | `detect_drop_field` | 0.458 | 0.458 |
| `binder_encoding` | `NAMED` | `NAMED_PLUS_DE_BRUIJN` | `bpe_tokens_per_transition` | 5675.950 | 5675.950 |
| `redundancy_level` | `NONE` | `LOW` | `detect_drop_field` | 0.833 | 0.833 |
| `application_style` | `CURRIED_BINARY` | `FLATTENED_SPINE` | `bpe_tokens_per_transition` | 5578.450 | 5661.625 |
| `list_syntax` | `PAREN` | `SPACE_SEPARATED` | `bpe_tokens_per_transition` | 6085.575 | 6089.850 |
| `identity_sigil` | `BRACKETED` | `NONE` | `identifier_fragmentation` | 1.844 | 1.844 |
| `binder_encoding` | `NAMED` | `DE_BRUIJN` | `bpe_tokens_per_transition` | 5540.150 | 5540.150 |
| `block_delimiter` | `INDENT` | `BRACE` | `detect_drop_line` | 0.667 | 0.458 |
| `binder_use_reminder` | `NONE` | `SHORT_TAG_AT_USE` | `binder_use_distance_tokens` | 200.939 | 202.023 |
| `role_word_length` | `FULL` | `SINGLE_CHAR` | `bpe_tokens_per_transition` | 5689.800 | 5689.800 |
| `expression_notation` | `FUNCTIONAL_APPLICATION` | `TAGGED_NESTED` | `bpe_tokens_per_transition` | 16662.950 | 19742.225 |
| `identity_scheme` | `SEMANTIC_ID` | `DISPLAY_PLUS_SHORT_ID` | `identifier_fragmentation` | 1.897 | 2.200 |
| `role_word_length` | `FULL` | `ABBREVIATED` | `bpe_tokens_per_transition` | 5531.950 | 5531.950 |
| `list_syntax` | `BRACKET_COMMA` | `SPACE_SEPARATED` | `bpe_tokens_per_transition` | 5495.475 | 5522.525 |
| `expression_notation` | `FUNCTIONAL_APPLICATION` | `SEXPR_PREFIX` | `bpe_tokens_per_transition` | 16662.950 | 16967.650 |
| `redundancy_level` | `SELECTIVE` | `EXPLICIT` | `detect_drop_field` | 0.750 | 0.417 |
| `lexicon_register` | `SYMBOLIC_ROLE` | `HUMAN_WORDS` | `bpe_tokens_per_transition` | 5416.250 | 5527.900 |
| `identity_scheme` | `SEMANTIC_ID` | `SHORT_ID` | `identifier_fragmentation` | 1.844 | 1.844 |
| `syntax_family` | `PROSE` | `BLOCK` | `detect_swap_records` | 0.667 | 0.619 |

## Mutations the failure memory blocked

| Axis | Value | Reason |
|---|---|---|
| `context_order` | `GOAL_CENTRED` | `BLOCKED_BY:FM-021` |
| `graph_serialization` | `GOAL_CENTRED` | `BLOCKED_BY:FM-005` |
| `shared_subterm_handling` | `HOISTED_DAG_LETS` | `BLOCKED_BY:FM-022` |

## Finalist profiles

### 1. `R_c8a70a62eebb`

**Shortlisted because:** best_on:bpe_tokens_per_transition, best_on:premise_to_action_distance_tokens, best_on:max_reference_span_tokens.

**Descends from:** `SEED_HEADER_PREMISE` via 19 recorded step(s); origin `SINGLE_AXIS`.

**Genome differences from that seed:** `action_position=HEADER`, `binder_encoding=NAMED`, `checksum_policy=PER_STATE`, `context_order=DEPENDENCY_TOPOLOGICAL`, `delta_visibility=DERIVABLE_ONLY`, `expression_notation=POSTFIX_RPN`, `goal_identity_visibility=BOTH`, `identity_scheme=SEMANTIC_ID`, `lexicon_register=SYMBOLIC_ROLE`, `literal_form=BARE`, `provenance_visibility=NONE`, `redundancy_level=NONE`, `scope_metadata=EXPLICIT_SCOPE_IDS`, `state_partitioning=INTERLEAVED_BY_GOAL`, `syntax_family=TAGGED_LINE`, `universe_visibility=ELIDED_WHEN_TRIVIAL`

| Metric | Value |
|---|---:|
| `binder_use_distance_chars` | 419.2555 |
| `binder_use_distance_tokens` | 190.7149 |
| `bpe_tokens_per_transition` | 5130.55 |
| `bytes_per_transition` | 11368.65 |
| `chars_per_transition` | 11368.5 |
| `detect_corrupt_identity` | 1.0 |
| `detect_drop_field` | 0.0 |
| `detect_drop_line` | 0.9167 |
| `detect_reorder_scope` | 0.625 |
| `detect_swap_records` | 0.7083 |
| `detect_truncate_tail` | 0.3333 |
| `forward_reference_rate` | 0.1739 |
| `gzip_bytes_per_transition` | 951.275 |
| `gzip_ratio` | 11.951 |
| `identifier_fragmentation` | 1.8325 |
| `max_reference_span_tokens` | 2339.175 |
| `premise_to_action_distance_tokens` | 11.5149 |
| `pretokens_per_transition` | 4083.775 |
| `role_vocabulary_entropy` | 2.4451 |
| `role_word_fragmentation` | 1.1667 |
| `structural_density` | 0.8016 |

<details><summary>Genome</summary>

| Axis | Value |
|---|---|
| `action_encoding` | `SOURCE_PLUS_STRUCTURED` |
| `action_position` | `HEADER` |
| `alpha_normalization` | `NORMALIZED` |
| `application_style` | `CURRIED_BINARY` |
| `binder_encoding` | `NAMED` |
| `binder_metadata` | `FULL` |
| `binder_use_reminder` | `NONE` |
| `block_delimiter` | `INDENT` |
| `checksum_policy` | `PER_STATE` |
| `const_name_form` | `FULL_NAME` |
| `context_order` | `DEPENDENCY_TOPOLOGICAL` |
| `count_assertions` | `NONE` |
| `delta_visibility` | `DERIVABLE_ONLY` |
| `dependency_visibility` | `INLINE_REFS` |
| `expression_notation` | `POSTFIX_RPN` |
| `field_marker` | `COLON` |
| `glyph_policy` | `UNICODE_NATIVE` |
| `goal_identity_visibility` | `BOTH` |
| `goal_position` | `AFTER_CONTEXT` |
| `graph_serialization` | `DFS_PREORDER` |
| `identity_scheme` | `SEMANTIC_ID` |
| `identity_sigil` | `NONE` |
| `implicit_argument_visibility` | `ALL` |
| `keyword_case` | `LOWER` |
| `lexicon_register` | `SYMBOLIC_ROLE` |
| `list_syntax` | `BRACKET_COMMA` |
| `literal_form` | `BARE` |
| `local_instance_visibility` | `MERGED_INTO_CONTEXT` |
| `obligation_visibility` | `EXPLICIT_METAVAR_BLOCK` |
| `premise_locality` | `HEADER_BLOCK` |
| `provenance_visibility` | `NONE` |
| `record_separator` | `NEWLINE` |
| `redundancy_level` | `NONE` |
| `role_word_length` | `FULL` |
| `scope_metadata` | `EXPLICIT_SCOPE_IDS` |
| `shared_subterm_handling` | `DUPLICATE` |
| `state_partitioning` | `INTERLEAVED_BY_GOAL` |
| `syntax_family` | `TAGGED_LINE` |
| `tree_vs_graph_projection` | `TREE_NESTED` |
| `type_attachment` | `TYPE_FIELD` |
| `type_explicitness` | `FULL_TREE` |
| `universe_visibility` | `ELIDED_WHEN_TRIVIAL` |

</details>

### 2. `R_211cd0165db9`

**Shortlisted because:** best_on:detect_swap_records.

**Descends from:** `SEED_HEADER_PREMISE` via 15 recorded step(s); origin `SINGLE_AXIS`.

**Genome differences from that seed:** `binder_encoding=NAMED`, `context_order=DEPENDENCY_TOPOLOGICAL`, `delta_visibility=DERIVABLE_ONLY`, `expression_notation=POSTFIX_RPN`, `identity_scheme=SEMANTIC_ID`, `identity_sigil=BRACKETED`, `lexicon_register=SYMBOLIC_ROLE`, `redundancy_level=NONE`, `role_word_length=ABBREVIATED`, `universe_visibility=ELIDED_WHEN_TRIVIAL`

| Metric | Value |
|---|---:|
| `binder_use_distance_chars` | 417.4163 |
| `binder_use_distance_tokens` | 200.3486 |
| `bpe_tokens_per_transition` | 5416.25 |
| `bytes_per_transition` | 11452.1 |
| `chars_per_transition` | 11451.9 |
| `detect_corrupt_identity` | 1.0 |
| `detect_drop_field` | 0.7083 |
| `detect_drop_line` | 0.7917 |
| `detect_reorder_scope` | 1.0 |
| `detect_swap_records` | 1.0 |
| `detect_truncate_tail` | 0.8333 |
| `forward_reference_rate` | 0.75 |
| `gzip_bytes_per_transition` | 959.925 |
| `gzip_ratio` | 11.9302 |
| `identifier_fragmentation` | 1.8442 |
| `max_reference_span_tokens` | 2831.375 |
| `premise_to_action_distance_tokens` | 211.5708 |
| `pretokens_per_transition` | 4038.625 |
| `role_vocabulary_entropy` | 2.2521 |
| `role_word_fragmentation` | 1.1667 |
| `structural_density` | 2.7574 |

<details><summary>Genome</summary>

| Axis | Value |
|---|---|
| `action_encoding` | `SOURCE_PLUS_STRUCTURED` |
| `action_position` | `TRAILER` |
| `alpha_normalization` | `NORMALIZED` |
| `application_style` | `CURRIED_BINARY` |
| `binder_encoding` | `NAMED` |
| `binder_metadata` | `FULL` |
| `binder_use_reminder` | `NONE` |
| `block_delimiter` | `INDENT` |
| `checksum_policy` | `NONE` |
| `const_name_form` | `FULL_NAME` |
| `context_order` | `DEPENDENCY_TOPOLOGICAL` |
| `count_assertions` | `NONE` |
| `delta_visibility` | `DERIVABLE_ONLY` |
| `dependency_visibility` | `INLINE_REFS` |
| `expression_notation` | `POSTFIX_RPN` |
| `field_marker` | `COLON` |
| `glyph_policy` | `UNICODE_NATIVE` |
| `goal_identity_visibility` | `SEMANTIC_ID` |
| `goal_position` | `AFTER_CONTEXT` |
| `graph_serialization` | `DFS_PREORDER` |
| `identity_scheme` | `SEMANTIC_ID` |
| `identity_sigil` | `BRACKETED` |
| `implicit_argument_visibility` | `ALL` |
| `keyword_case` | `LOWER` |
| `lexicon_register` | `SYMBOLIC_ROLE` |
| `list_syntax` | `BRACKET_COMMA` |
| `literal_form` | `TAGGED` |
| `local_instance_visibility` | `MERGED_INTO_CONTEXT` |
| `obligation_visibility` | `EXPLICIT_METAVAR_BLOCK` |
| `premise_locality` | `HEADER_BLOCK` |
| `provenance_visibility` | `IDENTITY_ONLY` |
| `record_separator` | `NEWLINE` |
| `redundancy_level` | `NONE` |
| `role_word_length` | `ABBREVIATED` |
| `scope_metadata` | `IMPLICIT_BY_NESTING` |
| `shared_subterm_handling` | `DUPLICATE` |
| `state_partitioning` | `BEFORE_AFTER_FULL` |
| `syntax_family` | `BLOCK` |
| `tree_vs_graph_projection` | `TREE_NESTED` |
| `type_attachment` | `TYPE_FIELD` |
| `type_explicitness` | `FULL_TREE` |
| `universe_visibility` | `ELIDED_WHEN_TRIVIAL` |

</details>

### 3. `R_0412a34e70c7`

**Shortlisted because:** best_on:detect_drop_field.

**Descends from:** `SEED_HEADER_PREMISE` via 15 recorded step(s); origin `SINGLE_AXIS`.

**Genome differences from that seed:** `binder_encoding=NAMED`, `checksum_policy=PER_STATE`, `context_order=DEPENDENCY_TOPOLOGICAL`, `delta_visibility=DERIVABLE_ONLY`, `expression_notation=POSTFIX_RPN`, `goal_identity_visibility=BOTH`, `graph_serialization=EDGE_LIST`, `identity_scheme=SEMANTIC_ID`, `literal_form=BARE`, `premise_locality=ADJACENT_TO_ACTION`, `provenance_visibility=NONE`, `redundancy_level=NONE`, `state_partitioning=INTERLEAVED_BY_GOAL`, `universe_visibility=ELIDED_WHEN_TRIVIAL`

| Metric | Value |
|---|---:|
| `binder_use_distance_chars` | 456.6253 |
| `binder_use_distance_tokens` | 203.5982 |
| `bpe_tokens_per_transition` | 5450.0 |
| `bytes_per_transition` | 12279.45 |
| `chars_per_transition` | 12279.3 |
| `detect_corrupt_identity` | 1.0 |
| `detect_drop_field` | 0.8333 |
| `detect_drop_line` | 0.7083 |
| `detect_reorder_scope` | 1.0 |
| `detect_swap_records` | 0.7391 |
| `detect_truncate_tail` | 0.9167 |
| `forward_reference_rate` | 0.0 |
| `gzip_bytes_per_transition` | 1029.575 |
| `gzip_ratio` | 11.9267 |
| `identifier_fragmentation` | 1.8969 |
| `max_reference_span_tokens` | 2867.675 |
| `premise_to_action_distance_tokens` | 612.1208 |
| `pretokens_per_transition` | 4050.025 |
| `role_vocabulary_entropy` | 3.2589 |
| `role_word_fragmentation` | 1.1667 |
| `structural_density` | 2.7541 |

<details><summary>Genome</summary>

| Axis | Value |
|---|---|
| `action_encoding` | `SOURCE_PLUS_STRUCTURED` |
| `action_position` | `TRAILER` |
| `alpha_normalization` | `NORMALIZED` |
| `application_style` | `CURRIED_BINARY` |
| `binder_encoding` | `NAMED` |
| `binder_metadata` | `FULL` |
| `binder_use_reminder` | `NONE` |
| `block_delimiter` | `INDENT` |
| `checksum_policy` | `PER_STATE` |
| `const_name_form` | `FULL_NAME` |
| `context_order` | `DEPENDENCY_TOPOLOGICAL` |
| `count_assertions` | `NONE` |
| `delta_visibility` | `DERIVABLE_ONLY` |
| `dependency_visibility` | `INLINE_REFS` |
| `expression_notation` | `POSTFIX_RPN` |
| `field_marker` | `COLON` |
| `glyph_policy` | `UNICODE_NATIVE` |
| `goal_identity_visibility` | `BOTH` |
| `goal_position` | `AFTER_CONTEXT` |
| `graph_serialization` | `EDGE_LIST` |
| `identity_scheme` | `SEMANTIC_ID` |
| `identity_sigil` | `NONE` |
| `implicit_argument_visibility` | `ALL` |
| `keyword_case` | `LOWER` |
| `lexicon_register` | `HUMAN_WORDS` |
| `list_syntax` | `BRACKET_COMMA` |
| `literal_form` | `BARE` |
| `local_instance_visibility` | `MERGED_INTO_CONTEXT` |
| `obligation_visibility` | `EXPLICIT_METAVAR_BLOCK` |
| `premise_locality` | `ADJACENT_TO_ACTION` |
| `provenance_visibility` | `NONE` |
| `record_separator` | `NEWLINE` |
| `redundancy_level` | `NONE` |
| `role_word_length` | `FULL` |
| `scope_metadata` | `IMPLICIT_BY_NESTING` |
| `shared_subterm_handling` | `DUPLICATE` |
| `state_partitioning` | `INTERLEAVED_BY_GOAL` |
| `syntax_family` | `BLOCK` |
| `tree_vs_graph_projection` | `TREE_NESTED` |
| `type_attachment` | `TYPE_FIELD` |
| `type_explicitness` | `FULL_TREE` |
| `universe_visibility` | `ELIDED_WHEN_TRIVIAL` |

</details>

### 4. `R_9044f4984fce`

**Shortlisted because:** knee.

**Descends from:** `SEED_HEADER_PREMISE` via 16 recorded step(s); origin `SINGLE_AXIS`.

**Genome differences from that seed:** `action_position=HEADER`, `binder_encoding=NAMED`, `context_order=DEPENDENCY_TOPOLOGICAL`, `delta_visibility=DERIVABLE_ONLY`, `expression_notation=POSTFIX_RPN`, `goal_identity_visibility=BOTH`, `goal_position=FIRST`, `identity_scheme=SEMANTIC_ID`, `identity_sigil=BRACKETED`, `lexicon_register=COMPACT_MNEMONIC`, `redundancy_level=SELECTIVE`, `universe_visibility=ELIDED_WHEN_TRIVIAL`

| Metric | Value |
|---|---:|
| `binder_use_distance_chars` | 397.8451 |
| `binder_use_distance_tokens` | 191.0147 |
| `bpe_tokens_per_transition` | 5495.475 |
| `bytes_per_transition` | 11641.8 |
| `chars_per_transition` | 11641.6 |
| `detect_corrupt_identity` | 1.0 |
| `detect_drop_field` | 0.75 |
| `detect_drop_line` | 0.7083 |
| `detect_reorder_scope` | 0.9583 |
| `detect_swap_records` | 0.9167 |
| `detect_truncate_tail` | 0.8333 |
| `forward_reference_rate` | 0.7417 |
| `gzip_bytes_per_transition` | 977.325 |
| `gzip_ratio` | 11.9119 |
| `identifier_fragmentation` | 1.8444 |
| `max_reference_span_tokens` | 2570.275 |
| `premise_to_action_distance_tokens` | 18.1649 |
| `pretokens_per_transition` | 4080.35 |
| `role_vocabulary_entropy` | 3.7541 |
| `role_word_fragmentation` | 1.3333 |
| `structural_density` | 2.7495 |

<details><summary>Genome</summary>

| Axis | Value |
|---|---|
| `action_encoding` | `SOURCE_PLUS_STRUCTURED` |
| `action_position` | `HEADER` |
| `alpha_normalization` | `NORMALIZED` |
| `application_style` | `CURRIED_BINARY` |
| `binder_encoding` | `NAMED` |
| `binder_metadata` | `FULL` |
| `binder_use_reminder` | `NONE` |
| `block_delimiter` | `INDENT` |
| `checksum_policy` | `NONE` |
| `const_name_form` | `FULL_NAME` |
| `context_order` | `DEPENDENCY_TOPOLOGICAL` |
| `count_assertions` | `NONE` |
| `delta_visibility` | `DERIVABLE_ONLY` |
| `dependency_visibility` | `INLINE_REFS` |
| `expression_notation` | `POSTFIX_RPN` |
| `field_marker` | `COLON` |
| `glyph_policy` | `UNICODE_NATIVE` |
| `goal_identity_visibility` | `BOTH` |
| `goal_position` | `FIRST` |
| `graph_serialization` | `DFS_PREORDER` |
| `identity_scheme` | `SEMANTIC_ID` |
| `identity_sigil` | `BRACKETED` |
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
| `redundancy_level` | `SELECTIVE` |
| `role_word_length` | `FULL` |
| `scope_metadata` | `IMPLICIT_BY_NESTING` |
| `shared_subterm_handling` | `DUPLICATE` |
| `state_partitioning` | `BEFORE_AFTER_FULL` |
| `syntax_family` | `BLOCK` |
| `tree_vs_graph_projection` | `TREE_NESTED` |
| `type_attachment` | `TYPE_FIELD` |
| `type_explicitness` | `FULL_TREE` |
| `universe_visibility` | `ELIDED_WHEN_TRIVIAL` |

</details>

### 5. `R_cf8323f05a83`

**Shortlisted because:** best_on:identifier_fragmentation.

**Descends from:** `SEED_GRAPH_EDGE` via 2 recorded step(s); origin `SINGLE_AXIS`.

**Genome differences from that seed:** `redundancy_level=ERROR_CORRECTING`, `syntax_family=PROSE`

| Metric | Value |
|---|---:|
| `binder_use_distance_chars` | 583.1195 |
| `binder_use_distance_tokens` | 257.7927 |
| `bpe_tokens_per_transition` | 8124.9 |
| `bytes_per_transition` | 18464.375 |
| `chars_per_transition` | 18464.175 |
| `detect_corrupt_identity` | 1.0 |
| `detect_drop_field` | 0.0 |
| `detect_drop_line` | 0.5417 |
| `detect_reorder_scope` | 0.4167 |
| `detect_swap_records` | 0.75 |
| `detect_truncate_tail` | 0.0 |
| `forward_reference_rate` | 0.0 |
| `gzip_bytes_per_transition` | 1442.825 |
| `gzip_ratio` | 12.7974 |
| `identifier_fragmentation` | 1.7104 |
| `max_reference_span_tokens` | 3142.325 |
| `premise_to_action_distance_tokens` | 415.1095 |
| `pretokens_per_transition` | 6407.075 |
| `role_vocabulary_entropy` | 3.7136 |
| `role_word_fragmentation` | 1.1667 |
| `structural_density` | 1.0446 |

<details><summary>Genome</summary>

| Axis | Value |
|---|---|
| `action_encoding` | `SOURCE_PLUS_STRUCTURED` |
| `action_position` | `BETWEEN_STATES` |
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
| `dependency_visibility` | `EXPLICIT_EDGES` |
| `expression_notation` | `SEXPR_PREFIX` |
| `field_marker` | `COLON` |
| `glyph_policy` | `UNICODE_NATIVE` |
| `goal_identity_visibility` | `SEMANTIC_ID` |
| `goal_position` | `AFTER_CONTEXT` |
| `graph_serialization` | `NODE_LIST_THEN_EDGES` |
| `identity_scheme` | `SHORT_ID` |
| `identity_sigil` | `NONE` |
| `implicit_argument_visibility` | `ALL` |
| `keyword_case` | `LOWER` |
| `lexicon_register` | `HUMAN_WORDS` |
| `list_syntax` | `BRACKET_COMMA` |
| `literal_form` | `TAGGED` |
| `local_instance_visibility` | `MERGED_INTO_CONTEXT` |
| `obligation_visibility` | `EXPLICIT_METAVAR_BLOCK` |
| `premise_locality` | `ADJACENT_TO_ACTION` |
| `provenance_visibility` | `IDENTITY_ONLY` |
| `record_separator` | `NEWLINE` |
| `redundancy_level` | `ERROR_CORRECTING` |
| `role_word_length` | `FULL` |
| `scope_metadata` | `IMPLICIT_BY_NESTING` |
| `shared_subterm_handling` | `DUPLICATE` |
| `state_partitioning` | `BEFORE_AFTER_FULL` |
| `syntax_family` | `PROSE` |
| `tree_vs_graph_projection` | `GRAPH_EDGE_LIST` |
| `type_attachment` | `TYPE_FIELD` |
| `type_explicitness` | `FULL_TREE` |
| `universe_visibility` | `FULL` |

</details>


## Measured structural effects

One parent-child pair is an anecdote. The table below aggregates every single-axis mutation applied to two or more different parents and reports the mean relative change in the metric that axis was predicted to move, with the fraction of observations agreeing in sign. Only transitions with at least 75% sign agreement are shown.

| Axis | From | To | Metric | Mean change | n | Agreement | Verdict |
|---|---|---|---|---:|---:|---:|---|
| `premise_locality` | `HEADER_BLOCK` | `TRAILING_BLOCK` | `premise_to_action_distance_tokens` | +146.3% | 2 | 100% | **costs** |
| `action_position` | `TRAILER` | `HEADER` | `premise_to_action_distance_tokens` | -92.0% | 5 | 100% | improves |
| `action_position` | `BETWEEN_STATES` | `TRAILER` | `premise_to_action_distance_tokens` | +60.6% | 2 | 100% | **costs** |
| `action_position` | `BETWEEN_STATES` | `HEADER` | `premise_to_action_distance_tokens` | -58.4% | 3 | 100% | improves |
| `shared_subterm_handling` | `HOISTED_DAG_LETS` | `DUPLICATE` | `bpe_tokens_per_transition` | -50.9% | 4 | 100% | improves |
| `premise_locality` | `ADJACENT_TO_ACTION` | `HEADER_BLOCK` | `premise_to_action_distance_tokens` | -29.1% | 9 | 100% | improves |
| `expression_notation` | `POSTFIX_RPN` | `SEXPR_PREFIX` | `bpe_tokens_per_transition` | +26.3% | 4 | 100% | **costs** |
| `expression_notation` | `POSTFIX_RPN` | `FUNCTIONAL_APPLICATION` | `bpe_tokens_per_transition` | +22.5% | 5 | 100% | **costs** |
| `redundancy_level` | `LOW` | `EXPLICIT` | `detect_drop_field` | -19.4% | 3 | 100% | **costs** |
| `expression_notation` | `SEXPR_PREFIX` | `POSTFIX_RPN` | `bpe_tokens_per_transition` | -17.5% | 5 | 100% | improves |
| `identity_scheme` | `SHORT_ID` | `DISPLAY_PLUS_SHORT_ID` | `identifier_fragmentation` | +16.2% | 4 | 100% | **costs** |
| `redundancy_level` | `NONE` | `EXPLICIT` | `detect_drop_field` | -15.6% | 3 | 100% | **costs** |
| `syntax_family` | `BLOCK` | `PROSE` | `detect_swap_records` | -15.4% | 4 | 100% | **costs** |
| `expression_notation` | `SEXPR_PREFIX` | `TAGGED_NESTED` | `bpe_tokens_per_transition` | +14.1% | 4 | 100% | **costs** |
| `redundancy_level` | `LOW` | `ERROR_CORRECTING` | `detect_drop_field` | -13.9% | 2 | 100% | **costs** |
| `syntax_family` | `BLOCK` | `TAGGED_LINE` | `detect_swap_records` | -10.1% | 7 | 100% | **costs** |
| `count_assertions` | `NONE` | `PER_BLOCK` | `detect_drop_line` | -9.0% | 6 | 83% | **costs** |
| `premise_locality` | `HEADER_BLOCK` | `ADJACENT_TO_ACTION` | `premise_to_action_distance_tokens` | +4.9% | 2 | 100% | **costs** |
| `context_order` | `DEPENDENCY_TOPOLOGICAL` | `TYPE_GROUPED` | `binder_use_distance_tokens` | -4.9% | 6 | 100% | improves |
| `context_order` | `DECLARATION_INDEX` | `TYPE_GROUPED` | `binder_use_distance_tokens` | -4.8% | 3 | 100% | improves |
| `syntax_family` | `BLOCK` | `JSONISH` | `detect_swap_records` | -4.7% | 8 | 75% | **costs** |
| `delta_visibility` | `DERIVABLE_ONLY` | `EXPLICIT_DELTA_BLOCK` | `bpe_tokens_per_transition` | +4.0% | 3 | 100% | **costs** |
| `alpha_normalization` | `NORMALIZED` | `BOTH` | `bpe_tokens_per_transition` | +3.8% | 5 | 100% | **costs** |
| `alpha_normalization` | `NORMALIZED` | `PRESERVE_DISPLAY` | `bpe_tokens_per_transition` | +3.7% | 7 | 100% | **costs** |

## Which axes this corpus can speak to

Every single-axis mutation whose child measured identically to its parent is evidence that the axis has no effect **on this corpus** — not that it is a bad axis. Reporting it is more useful than reporting a search that appears to have explored it.

| Axis | Single-axis mutations | Changed the measurement | Share |
|---|---:|---:|---:|
| `const_name_form` | 8 | 0 | 0% |
| `graph_serialization` | 41 | 0 | 0% |
| `local_instance_visibility` | 7 | 0 | 0% |
| `role_word_length` | 4 | 0 | 0% |
| `state_partitioning` | 5 | 0 | 0% |
| `type_attachment` | 3 | 0 | 0% |
| `field_marker` | 18 | 2 | 11% |
| `universe_visibility` | 13 | 6 | 46% |
| `binder_encoding` | 8 | 4 | 50% |
| `redundancy_level` | 35 | 19 | 54% |
| `goal_position` | 20 | 11 | 55% |
| `premise_locality` | 21 | 13 | 62% |
| `keyword_case` | 6 | 4 | 67% |
| `context_order` | 26 | 20 | 77% |
| `alpha_normalization` | 14 | 12 | 86% |
| `tree_vs_graph_projection` | 17 | 15 | 88% |
| `action_encoding` | 4 | 4 | 100% |
| `action_position` | 11 | 11 | 100% |
| `application_style` | 5 | 5 | 100% |
| `binder_use_reminder` | 17 | 17 | 100% |
| `block_delimiter` | 2 | 2 | 100% |
| `checksum_policy` | 5 | 5 | 100% |
| `count_assertions` | 6 | 6 | 100% |
| `delta_visibility` | 4 | 4 | 100% |
| `dependency_visibility` | 2 | 2 | 100% |
| `expression_notation` | 27 | 27 | 100% |
| `goal_identity_visibility` | 4 | 4 | 100% |
| `identity_scheme` | 16 | 16 | 100% |
| `identity_sigil` | 11 | 11 | 100% |
| `lexicon_register` | 27 | 27 | 100% |
| `list_syntax` | 12 | 12 | 100% |
| `literal_form` | 10 | 10 | 100% |
| `provenance_visibility` | 6 | 6 | 100% |
| `record_separator` | 5 | 5 | 100% |
| `scope_metadata` | 3 | 3 | 100% |
| `shared_subterm_handling` | 4 | 4 | 100% |
| `syntax_family` | 40 | 40 | 100% |

### Largest groups of candidates that measure identically

| Candidates | Group size |
|---|---:|
| `R_133e0575e6f6`, `R_29cb0362c8b2`, `R_976cbbb627b6`, `R_9e56b93f27ea` and 4 more | 8 |
| `R_1ff680fbb3ad`, `R_2c552f801dad`, `R_337432a1846e`, `R_4fac0c397a3d` and 4 more | 8 |
| `R_029c0fe16673`, `R_265a0f4a303d`, `R_2f8d4430dd0c`, `R_300c57fb1e12` and 3 more | 7 |
| `R_038ca3dda088`, `R_0abca3babb97`, `R_59f8c6ce9f88`, `R_6fec85005dd3` and 3 more | 7 |
| `R_0332c5230135`, `R_23943bdc2877`, `R_71bf2c9db5b0`, `R_9cddd8624de7` and 2 more | 6 |
| `R_0412a34e70c7`, `R_24adc5bd59eb`, `R_7ffa309c0238`, `R_8c52ac5d1ea5` and 2 more | 6 |
| `R_6562b34fe896`, `R_853fdf135675`, `R_97de5f3a3036`, `R_b0c0ce88854b` and 2 more | 6 |
| `R_020d202641d8`, `R_0e598fc43238`, `R_7a63a101c412`, `R_7d92f6278cef` and 1 more | 5 |
| `R_082b4047298e`, `R_91f83d5e51a4`, `R_95d2f5128c2f`, `R_9b4b5c39c663` and 1 more | 5 |
| `R_211cd0165db9`, `R_396cb082c6d5`, `R_6feaeda6b049`, `R_8ae4ba2c1f7e` and 1 more | 5 |
| `R_2c8e9cdf0c7b`, `R_6abd635f7aea`, `R_860dd7e7a2dc`, `R_9022db3b9e5b` and 1 more | 5 |
| `R_2f3730d1f435`, `R_39af64a11104`, `R_83cb39bb63ed`, `R_88caf5ea3b27` and 1 more | 5 |

## Sealed evaluation

The sealed split holds 120 transitions from families never read during the search. It was evaluated once, after the frontier was frozen.

| Candidate | Gates | BPE tokens | Binder distance | Swap detect |
|---|---|---:|---:|---:|
| `R_c8a70a62eebb` | PASS | 5864.7 | 251.6 | 0.708 |
| `R_0412a34e70c7` | PASS | 6234.9 | 270.6 | 0.955 |
| `R_211cd0165db9` | PASS | 6202.2 | 267.3 | 0.957 |
| `R_9044f4984fce` | PASS | 6301.1 | 271.5 | 0.917 |
| `R_9f3eb215d943` | PASS | 16414.3 | 201.1 | 0.522 |
| `R_cf8323f05a83` | PASS | 9085.9 | 326.4 | 0.792 |

## Companion reports

- [`FINALIST_DOMAIN_PROFILES.md`](FINALIST_DOMAIN_PROFILES.md) — each finalist measured per Mathlib domain, because a frontier table reports averages and a user of the language asks about their own mathematics.
- [`DISCOVERY_REPRESENTATION_ANALYSIS.md`](DISCOVERY_REPRESENTATION_ANALYSIS.md) — what PRM800K's step labels expose that no representation in this space can, and why.
- [`NOTATION_COVERAGE.md`](NOTATION_COVERAGE.md) — which human mathematical constructs the formal corpus barely exercises.
- [`FRONTIER_VALIDATION.md`](FRONTIER_VALIDATION.md) — the finalists re-measured on the validation split selection never read, with rank correlations.
- [`GATE_HOLDOUT_AUDIT.json`](GATE_HOLDOUT_AUDIT.json) — every gate verdict re-run on a disjoint dev slice, to catch a verdict that held only by evaluation order.
- [`REPRODUCIBILITY.json`](REPRODUCIBILITY.json) — candidates re-rendered in a fresh subprocess under a different hash seed, testing the claim that a genome hash determines a language.
- [`../audits/LEAN_RUNTIME_V2_CORPUS.md`](../audits/LEAN_RUNTIME_V2_CORPUS.md) — the corpus accounting, with every excluded transition counted by reason.

## What this does not establish

- That any of these representations makes mathematical reasoning easier for a model. No model was run, and `FM-003` records that on the last task most of the measured accuracy was lexical.
- That the token rankings generalise. They are measured under one pinned GPT-2 vocabulary; the prior audit used Qwen3-8B, where every mathematical glyph the corpus needs is a single token and these numbers would differ.
- That the frontier is the global frontier. The space has 4.095e+19 points and this search evaluated 489.

The next step that would change any of this is a matched, controlled model experiment on the finalists, gated by the six lexical controls `FM-003` requires.
