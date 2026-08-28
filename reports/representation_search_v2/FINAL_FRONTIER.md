# PRETRAINING_REPRESENTATION_FRONTIER_V2

**This is not a claim that any representation is optimal for neural mathematical reasoning.** It is what an open-ended search found before model adaptation, together with the evidence that produced it and the limits of that evidence.

## Provenance

| Field | Value |
|---|---|
| Compiler | `representation-compiler-v1.0.0` |
| Canonical state | `canonical-math-transition-v2.0.0` |
| Genome schema | `representation-genome-v2.8.0` |
| Axes before / after | 42 / 50 |
| Search space | 3.582e+23 points |
| Generations | 4 |
| Candidates registered | 96 |
| Candidates evaluated | 62 |
| Candidates killed | 6 |
| Strict Pareto front | 28 |
| Reported finalists | 6 |
| Structural convergence | NO |

## Where candidates died

The ladder exists so a candidate is killed at the cheapest level that can kill it.

| Level | Killed |
|---|---:|
| `compile` | 2 |
| `semantics` | 4 |

## The meta-designer

| Backend | Proposals accepted | Rejected |
|---|---:|---:|
| `deterministic` | 85 | 0 |
| `llm/ollama:gemma3:4b` | 21 | 25 |

Proposal types seen: `AXIS_MUTATION`, `CORPUS_ACQUISITION`, `NEW_AXIS`, `NEW_PRIMITIVE`

Invented axes accepted: **8**. Proposals recorded as unimplementable: **0** — kept as evidence about what the meta-designer wanted and what the projection algebra could not express.

## The frontier

| # | Candidate | Shortlisted because | Origin | Invented axes |
|---|---|---|---|---|
| 1 | `SEED_CANONICAL_SEXPR` | best_on:semantic_detect_rate, best_on:binder_query_token_distance | SEED | — |
| 2 | `R_623a343174ec` | knee | AXIS_MUTATION | — |
| 3 | `R_8f1e3d8b7028` | best_on:dependency_query_token_distance | AXIS_MUTATION | — |
| 4 | `R_c62e7380ee50` | best_on:bpe_tokens_per_transition | AXIS_MUTATION | — |
| 5 | `R_f5d8e89eb43a` | best_on:identifier_fragmentation | AXIS_MUTATION | — |
| 6 | `R_f9041d48927f` | best_on:binder_use_distance_tokens | AXIS_MUTATION | — |

| Candidate | `bpe_tokens_per_transition` | `binder_use_distance_tokens` | `semantic_detect_rate` | `binder_query_token_distance` | `dependency_query_token_distance` | `identifier_fragmentation` |
|---|---|---|---|---|---|---|
| `SEED_CANONICAL_SEXPR` | 7417.786 | 264.876 | 1.000 | 16.320 | 45.033 | 1.890 |
| `R_623a343174ec` | 6785.000 | 207.338 | 1.000 | 17.400 | 39.967 | 1.883 |
| `R_8f1e3d8b7028` | 8193.464 | 293.753 | 1.000 | 160.787 | 14.933 | 1.933 |
| `R_c62e7380ee50` | 6092.929 | 218.453 | 1.000 | 21.760 | 44.167 | 2.079 |
| `R_f5d8e89eb43a` | 18523.857 | 204.320 | 1.000 | 20.107 | 93.456 | 1.822 |
| `R_f9041d48927f` | 17369.750 | 196.996 | 1.000 | 19.880 | 98.744 | 1.953 |

## Controls

`FM-002` requires the recorded baselines to stay visible whether or not they survive.

| Baseline | Status | Strict front | Finalist |
|---|---|---|---|
| `SEED_CANONICAL_SEXPR` | EVALUATED | no | **yes** |
| `SEED_DELTA_FIRST` | EVALUATED | no | no |
| `SEED_DEPENDENCY_TOPOLOGICAL` | EVALUATED | no | no |
| `SEED_EXPLICIT_REDUNDANT` | EVALUATED | no | no |
| `SEED_GOAL_LOCAL` | EVALUATED | yes | no |
| `SEED_GRAPH_EDGE` | EVALUATED | no | no |
| `SEED_HEADER_PREMISE` | EVALUATED | no | no |
| `SEED_HYBRID_COMPACT_BLOCK` | EVALUATED | no | no |
| `SEED_HYBRID_LOCAL_DAG` | EVALUATED | no | no |
| `SEED_HYBRID_RPN_MACHINE` | EVALUATED | yes | no |
| `SEED_JSON_BASELINE` | EVALUATED | no | no |
| `SEED_LEAN_LIKE` | EVALUATED | no | no |
| `SEED_MINIMAL_MACHINE` | EVALUATED | no | no |
| `SEED_PRIOR_HML` | EVALUATED | no | no |
| `SEED_STRUCTURED_ENGLISH` | EVALUATED | no | no |
| `SEED_TYPED_AST` | EVALUATED | no | no |

## Multi-tokenizer audit

Vocabularies compared: **4**. Same cheapest candidate under every vocabulary: **yes**.

| Vocabulary | Cheapest finalist |
|---|---|
| `gpt2` | `R_c62e7380ee50` |
| `gptneox` | `R_c62e7380ee50` |
| `qwen25` | `R_c62e7380ee50` |
| `starcoder2` | `R_c62e7380ee50` |

`FM-018` binds the reading: the escaping penalty reproduces across vocabularies, the absolute counts do not. A ranking that flips between vocabularies is a vocabulary effect and is not a property of the representation.

## Validation-governed selection

Quarantined as non-generalising: **0**.


## Generations

| Gen | Evaluated | Killed | Front | Moved | New axes | Seconds |
|---|---:|---:|---:|---|---|---:|
| 0 | 16 | 0 | 7 | yes | ['context_signature', 'dependency_weight', 'record_reorder', 'goal_context_depth'] | 62 |
| 1 | 29 | 5 | 15 | yes | ['goal_context_signature', 'dependency_capsule'] | 84 |
| 2 | 41 | 1 | 25 | yes | ['metavariable_grouping'] | 111 |
| 3 | 40 | 0 | 24 | no | ['goal_signature'] | 99 |

## What this does not establish

- That any of these makes mathematical reasoning easier for a model. The neural probes here are inference-only, tiny, and reported with their sequential rule.
- That the frontier is global. The space has 3.582e+23 points and this search evaluated 62.
- That the search converged. `STRUCTURAL_CONVERGENCE = NO`.
- That open-endedness is unbounded. An invented axis must bind to one of four projection hooks; proposals outside that algebra are recorded, not run.
