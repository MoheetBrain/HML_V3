# PRETRAINING_REPRESENTATION_FRONTIER_V2

**This is not a claim that any representation is optimal for neural mathematical reasoning.** It is what an open-ended search found before model adaptation, together with the evidence that produced it and the limits of that evidence.

## Provenance

| Field | Value |
|---|---|
| Compiler | `representation-compiler-v1.0.0` |
| Canonical state | `canonical-math-transition-v2.0.0` |
| Genome schema | `representation-genome-v2.13.0` |
| Axes before / after | 42 / 55 |
| Search space | 1.548e+26 points |
| Generations | 14 |
| Candidates registered | 255 |
| Candidates evaluated | 201 |
| Candidates killed | 14 |
| Strict Pareto front | 49 |
| Reported finalists | 6 |
| Structural convergence | NO |

## Where candidates died

The ladder exists so a candidate is killed at the cheapest level that can kill it.

| Level | Killed |
|---|---:|
| `compile` | 2 |
| `semantics` | 12 |

## The meta-designer

| Backend | Proposals accepted | Rejected |
|---|---:|---:|
| `deterministic` | 315 | 0 |
| `llm/ollama:gemma3:4b` | 69 | 85 |

Proposal types seen: `AXIS_MUTATION`, `CORPUS_ACQUISITION`, `NEW_AXIS`, `NEW_PRIMITIVE`

Invented axes accepted: **13**. Proposals recorded as unimplementable: **2** — kept as evidence about what the meta-designer wanted and what the projection algebra could not express.

## The frontier

| # | Candidate | Shortlisted because | Origin | Invented axes |
|---|---|---|---|---|
| 1 | `R_5b2eb732ac8b` | best_on:dependency_query_token_distance, knee | AXIS_MUTATION | — |
| 2 | `R_000441b08de4` | best_on:semantic_detect_rate | AXIS_MUTATION | — |
| 3 | `R_01d4e489af53` | best_on:binder_query_token_distance | AXIS_MUTATION | — |
| 4 | `R_101e806690b0` | best_on:identifier_fragmentation | AXIS_MUTATION | — |
| 5 | `R_28b291b5ebe6` | best_on:binder_use_distance_tokens | AXIS_MUTATION | — |
| 6 | `R_54183872d1bd` | best_on:bpe_tokens_per_transition | AXIS_MUTATION | — |

| Candidate | `bpe_tokens_per_transition` | `binder_use_distance_tokens` | `semantic_detect_rate` | `binder_query_token_distance` | `dependency_query_token_distance` | `identifier_fragmentation` |
|---|---|---|---|---|---|---|
| `R_5b2eb732ac8b` | 6420.536 | 215.232 | 1.000 | 116.493 | 14.478 | 1.896 |
| `R_000441b08de4` | 5915.321 | 211.210 | 1.000 | 18.280 | 37.822 | 1.885 |
| `R_01d4e489af53` | 7144.536 | 254.462 | 1.000 | 16.307 | 43.611 | 1.893 |
| `R_101e806690b0` | 18552.464 | 205.133 | 1.000 | 20.107 | 95.167 | 1.822 |
| `R_28b291b5ebe6` | 6440.786 | 193.408 | 1.000 | 17.520 | 38.633 | 1.883 |
| `R_54183872d1bd` | 5658.143 | 201.218 | 1.000 | 17.053 | 37.011 | 1.893 |

## Controls

`FM-002` requires the recorded baselines to stay visible whether or not they survive.

| Baseline | Status | Strict front | Finalist |
|---|---|---|---|
| `SEED_CANONICAL_SEXPR` | EVALUATED | no | no |
| `SEED_DELTA_FIRST` | EVALUATED | no | no |
| `SEED_DEPENDENCY_TOPOLOGICAL` | EVALUATED | no | no |
| `SEED_EXPLICIT_REDUNDANT` | EVALUATED | no | no |
| `SEED_GOAL_LOCAL` | EVALUATED | no | no |
| `SEED_GRAPH_EDGE` | EVALUATED | no | no |
| `SEED_HEADER_PREMISE` | EVALUATED | no | no |
| `SEED_HYBRID_COMPACT_BLOCK` | EVALUATED | no | no |
| `SEED_HYBRID_LOCAL_DAG` | EVALUATED | no | no |
| `SEED_HYBRID_RPN_MACHINE` | EVALUATED | no | no |
| `SEED_JSON_BASELINE` | EVALUATED | no | no |
| `SEED_LEAN_LIKE` | EVALUATED | no | no |
| `SEED_MINIMAL_MACHINE` | EVALUATED | no | no |
| `SEED_PRIOR_HML` | EVALUATED | no | no |
| `SEED_STRUCTURED_ENGLISH` | EVALUATED | no | no |
| `SEED_TYPED_AST` | EVALUATED | no | no |

## Multi-tokenizer audit

Vocabularies compared: **4**. Same cheapest candidate under every vocabulary: **no**.

| Vocabulary | Cheapest finalist |
|---|---|
| `gpt2` | `R_54183872d1bd` |
| `gptneox` | `R_54183872d1bd` |
| `qwen25` | `R_000441b08de4` |
| `starcoder2` | `R_000441b08de4` |

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
| 4 | 40 | 0 | 22 | yes | — | 101 |
| 5 | 36 | 1 | 24 | no | — | 69 |
| 6 | 39 | 2 | 18 | no | — | 59 |
| 7 | 35 | 1 | 22 | no | — | 50 |
| 8 | 38 | 0 | 19 | yes | — | 61 |
| 9 | 38 | 2 | 22 | yes | — | 60 |
| 10 | 35 | 0 | 21 | no | ['lexical_cache', 'dependency_signature'] | 76 |
| 11 | 40 | 2 | 21 | yes | — | 58 |
| 12 | 36 | 0 | 15 | no | ['action_signature'] | 49 |
| 13 | 42 | 0 | 25 | no | ['semantic_graph', 'precedence_ordering'] | 97 |

## What this does not establish

- That any of these makes mathematical reasoning easier for a model. The neural probes here are inference-only, tiny, and reported with their sequential rule.
- That the frontier is global. The space has 1.548e+26 points and this search evaluated 201.
- That the search converged. `STRUCTURAL_CONVERGENCE = NO`.
- That open-endedness is unbounded. An invented axis must bind to one of four projection hooks; proposals outside that algebra are recorded, not run.
