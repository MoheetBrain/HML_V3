# PRETRAINING_REPRESENTATION_FRONTIER_V2

**This is not a claim that any representation is optimal for neural mathematical reasoning.** It is what an open-ended search found before model adaptation, together with the evidence that produced it and the limits of that evidence.

## Provenance

| Field | Value |
|---|---|
| Compiler | `representation-compiler-v1.0.0` |
| Canonical state | `canonical-math-transition-v2.0.0` |
| Genome schema | `representation-genome-v2.5.0` |
| Axes before / after | 42 / 47 |
| Search space | 4.422e+21 points |
| Generations | 106 |
| Candidates registered | 566 |
| Candidates evaluated | 531 |
| Candidates killed | 33 |
| Strict Pareto front | 104 |
| Reported finalists | 7 |
| Structural convergence | YES |

## Where candidates died

The ladder exists so a candidate is killed at the cheapest level that can kill it.

| Level | Killed |
|---|---:|
| `compile` | 7 |
| `semantics` | 26 |

## The meta-designer

| Backend | Proposals accepted | Rejected |
|---|---:|---:|
| `deterministic` | 1527 | 0 |
| `llm/ollama:gemma3:4b` | 508 | 623 |
| `llm/ollama:qwen38-rvn:latest` | 372 | 527 |

Proposal types seen: `AXIS_MUTATION`, `CORPUS_ACQUISITION`, `NEW_AXIS`, `NEW_PRIMITIVE`

Invented axes accepted: **5**. Proposals recorded as unimplementable: **284** — kept as evidence about what the meta-designer wanted and what the projection algebra could not express.

## The frontier

| # | Candidate | Shortlisted because | Origin | Invented axes |
|---|---|---|---|---|
| 1 | `R_015b8cd926da` | best_on:detect_drop_field | AXIS_MUTATION | — |
| 2 | `R_03812c646290` | knee | AXIS_MUTATION | — |
| 3 | `R_159628756bc5` | best_on:bpe_tokens_per_transition | INVENTED_AXIS | {'dependency_capsule': 'GOAL_LOCAL'} |
| 4 | `R_21f62bd82c7e` | best_on:binder_query_token_distance | AXIS_MUTATION | — |
| 5 | `R_a7ef0cd3b92e` | best_on:identifier_fragmentation | AXIS_MUTATION | — |
| 6 | `R_bbfdfa5a9249` | best_on:binder_use_distance_tokens | AXIS_MUTATION | — |
| 7 | `R_fcd13f8d56a5` | best_on:dependency_query_token_distance | INVENTED_AXIS | {'dependency_capsule': 'ACTION_LOCAL'} |

| Candidate | `bpe_tokens_per_transition` | `binder_use_distance_tokens` | `detect_drop_field` | `binder_query_token_distance` | `dependency_query_token_distance` | `identifier_fragmentation` |
|---|---|---|---|---|---|---|
| `R_015b8cd926da` | 11091.594 | 402.119 | 0.708 | 33.067 | 41.089 | 1.921 |
| `R_03812c646290` | 6928.094 | 257.109 | 0.667 | 23.767 | 29.322 | 1.925 |
| `R_159628756bc5` | 5820.406 | 250.692 | 0.000 | 21.578 | 27.789 | 1.935 |
| `R_21f62bd82c7e` | 6483.031 | 253.514 | 0.000 | 20.400 | 27.789 | 1.924 |
| `R_a7ef0cd3b92e` | 10982.562 | 396.496 | 0.000 | 30.267 | 42.267 | 1.798 |
| `R_bbfdfa5a9249` | 17023.562 | 199.578 | 0.458 | 23.767 | 43.478 | 1.876 |
| `R_fcd13f8d56a5` | 5820.406 | 292.743 | 0.000 | 23.389 | 11.844 | 1.935 |

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

Vocabularies compared: **4**. Same cheapest candidate under every vocabulary: **yes**.

| Vocabulary | Cheapest finalist |
|---|---|
| `gpt2` | `R_159628756bc5` |
| `gptneox` | `R_159628756bc5` |
| `qwen25` | `R_159628756bc5` |
| `starcoder2` | `R_159628756bc5` |

`FM-018` binds the reading: the escaping penalty reproduces across vocabularies, the absolute counts do not. A ranking that flips between vocabularies is a vocabulary effect and is not a property of the representation.

## Validation-governed selection

Quarantined as non-generalising: **12**.

| Verdict | Candidates |
|---|---:|
| `NON_GENERALIZING_MUTATION` | 8 |
| `VALIDATION_CONTRADICTS_DEV` | 4 |

## Generations

| Gen | Evaluated | Killed | Front | Moved | New axes | Seconds |
|---|---:|---:|---:|---|---|---:|
| 0 | 16 | 0 | 12 | yes | ['dependency_capsule', 'delta_explicitness'] | 208 |
| 1 | 33 | 1 | 24 | no | ['record_reorder'] | 193 |
| 2 | 38 | 1 | 29 | no | — | 185 |
| 3 | 30 | 0 | 24 | yes | — | 238 |
| 4 | 31 | 1 | 22 | no | — | 202 |
| 5 | 32 | 0 | 21 | no | — | 201 |
| 6 | 30 | 0 | 24 | no | — | 152 |
| 7 | 32 | 0 | 23 | yes | — | 140 |
| 8 | 26 | 0 | 21 | no | — | 103 |
| 9 | 25 | 0 | 19 | no | — | 134 |
| 10 | 30 | 1 | 24 | no | — | 165 |
| 11 | 28 | 0 | 21 | no | — | 117 |
| 12 | 29 | 1 | 23 | yes | — | 156 |
| 13 | 31 | 1 | 20 | no | — | 154 |
| 14 | 38 | 2 | 18 | yes | — | 208 |
| 15 | 31 | 0 | 19 | no | — | 172 |
| 16 | 32 | 0 | 20 | no | — | 194 |
| 17 | 33 | 0 | 25 | no | — | 169 |
| 18 | 33 | 1 | 25 | no | — | 164 |
| 19 | 31 | 1 | 22 | no | — | 212 |
| 20 | 30 | 0 | 20 | yes | — | 222 |
| 21 | 39 | 1 | 24 | no | ['field_presence_checksum'] | 234 |
| 22 | 36 | 1 | 22 | yes | — | 282 |
| 23 | 31 | 1 | 24 | no | — | 144 |
| 24 | 30 | 0 | 25 | no | — | 161 |
| 25 | 28 | 1 | 23 | yes | — | 173 |
| 26 | 33 | 2 | 27 | no | — | 173 |
| 27 | 35 | 0 | 25 | yes | — | 177 |
| 28 | 33 | 1 | 27 | no | — | 144 |
| 29 | 31 | 0 | 22 | yes | — | 196 |
| 30 | 28 | 0 | 20 | no | — | 133 |
| 31 | 32 | 1 | 23 | no | — | 184 |
| 32 | 30 | 3 | 20 | yes | — | 263 |
| 33 | 35 | 0 | 24 | yes | — | 254 |
| 34 | 31 | 1 | 20 | yes | — | 145 |
| 35 | 35 | 0 | 23 | yes | — | 164 |
| 36 | 30 | 0 | 21 | no | — | 182 |
| 37 | 31 | 0 | 19 | no | — | 140 |
| 38 | 33 | 0 | 21 | no | — | 184 |
| 39 | 29 | 0 | 18 | no | — | 135 |
| 40 | 34 | 1 | 24 | no | — | 104 |
| 41 | 31 | 1 | 19 | no | — | 188 |
| 42 | 34 | 0 | 20 | no | — | 159 |
| 43 | 33 | 1 | 22 | no | — | 160 |
| 44 | 30 | 0 | 20 | no | — | 239 |
| 45 | 33 | 0 | 19 | no | — | 210 |
| 46 | 33 | 0 | 22 | no | — | 174 |
| 47 | 27 | 0 | 17 | no | — | 185 |
| 48 | 28 | 1 | 14 | no | — | 202 |
| 49 | 32 | 0 | 18 | no | — | 193 |
| 50 | 32 | 1 | 18 | no | — | 144 |
| 51 | 32 | 0 | 20 | yes | — | 199 |
| 52 | 31 | 0 | 19 | yes | — | 143 |
| 53 | 29 | 0 | 17 | no | — | 231 |
| 54 | 30 | 2 | 18 | yes | — | 204 |
| 55 | 30 | 0 | 18 | no | — | 202 |
| 56 | 31 | 0 | 22 | no | — | 136 |
| 57 | 31 | 0 | 22 | no | — | 167 |
| 58 | 31 | 1 | 24 | no | — | 143 |
| 59 | 26 | 0 | 20 | no | — | 152 |
| 60 | 27 | 0 | 22 | yes | — | 179 |
| 61 | 26 | 2 | 21 | no | — | 120 |
| 62 | 28 | 0 | 22 | no | — | 176 |
| 63 | 28 | 0 | 21 | no | — | 198 |
| 64 | 29 | 0 | 18 | no | — | 218 |
| 65 | 29 | 0 | 19 | no | — | 160 |
| 66 | 27 | 0 | 17 | no | — | 226 |
| 67 | 28 | 0 | 20 | no | — | 186 |
| 68 | 32 | 0 | 22 | no | — | 232 |
| 69 | 26 | 0 | 19 | no | — | 134 |
| 70 | 27 | 0 | 21 | no | ['metavar_partition'] | 123 |
| 71 | 26 | 0 | 19 | no | — | 216 |
| 72 | 26 | 0 | 20 | no | — | 186 |
| 73 | 25 | 1 | 19 | no | — | 129 |
| 74 | 25 | 0 | 19 | no | — | 147 |
| 75 | 24 | 0 | 19 | no | — | 196 |
| 76 | 25 | 0 | 19 | no | — | 241 |
| 77 | 25 | 0 | 20 | no | — | 143 |
| 78 | 24 | 0 | 19 | no | — | 145 |
| 79 | 24 | 0 | 19 | no | — | 153 |
| 80 | 26 | 0 | 20 | no | — | 154 |
| 81 | 24 | 0 | 19 | no | — | 143 |
| 82 | 25 | 0 | 20 | no | — | 167 |
| 83 | 24 | 0 | 19 | no | — | 82 |
| 84 | 24 | 0 | 19 | no | — | 224 |
| 85 | 25 | 0 | 19 | no | — | 144 |
| 86 | 25 | 0 | 20 | no | — | 193 |
| 87 | 26 | 0 | 20 | yes | — | 119 |
| 88 | 25 | 0 | 20 | no | — | 115 |
| 89 | 27 | 0 | 21 | no | — | 201 |
| 90 | 27 | 0 | 22 | yes | — | 198 |
| 91 | 24 | 0 | 19 | no | — | 132 |
| 92 | 24 | 0 | 19 | no | — | 220 |
| 93 | 24 | 0 | 19 | no | — | 110 |
| 94 | 24 | 0 | 19 | no | — | 129 |
| 95 | 26 | 0 | 19 | no | — | 193 |
| 96 | 25 | 0 | 20 | no | — | 90 |
| 97 | 25 | 0 | 19 | no | — | 174 |
| 98 | 24 | 0 | 19 | no | — | 119 |
| 99 | 25 | 0 | 20 | no | — | 134 |
| 100 | 24 | 0 | 19 | no | — | 176 |
| 101 | 25 | 0 | 19 | no | — | 130 |
| 102 | 24 | 0 | 19 | no | — | 162 |
| 103 | 25 | 0 | 19 | no | — | 157 |
| 104 | 24 | 0 | 19 | no | — | 192 |
| 105 | 24 | 0 | 19 | no | — | 100 |

## What this does not establish

- That any of these makes mathematical reasoning easier for a model. The neural probes here are inference-only, tiny, and reported with their sequential rule.
- That the frontier is global. The space has 4.422e+21 points and this search evaluated 531.
- That the search converged. `STRUCTURAL_CONVERGENCE = YES`.
- That open-endedness is unbounded. An invented axis must bind to one of four projection hooks; proposals outside that algebra are recorded, not run.
