# Project Status

## Project Objective

Discover, by evidence rather than by design taste, which machine-facing representation of
mathematical state best supports verified mathematical reasoning. Mathematical truth is held
fixed as a `CanonicalMathState` derived from Lean; the representation `R_phi(M)` is the
dependent variable and is searched over.

## Current Stage

`OPEN_ENDED_SEARCH_V2_CONVERGED`. The closed 42-axis search is frozen and preserved. The
open-ended loop ran from generation 0 on the 918-transition search pool and reached
**structural convergence at generation 106** — frontier position, frontier membership and
genome size all unchanged for five consecutive generations. `SEALED_FINAL_V2` has not been
read.

## Current Branch

`codex/open-ended-search-v2` (V1 frozen at tag `hml-v3-closed-search-v1-2026-08-28`)

## Current System Architecture

```text
Lean 4.10.0-rc1 @ 3b58e0649156, Mathlib 29dcec074de168ac2bf835a77ef68bbe069194c5
        |
        |  scripts/extract/LeanRuntimeExtractV2.lean   fresh whole-file elaboration
        v
LeanRuntimeState V2      exact Expr trees, FVarId/MVarId identity, metavariable context,
        |                local dependencies, InfoTree path, environment provenance
        |  src/hml_v3/adapters/lean/runtime_v2.py      normalization + canonicalization
        v
CanonicalMathTransition V2  (data/corpus/lean_runtime_v2.canonical.jsonl.gz)
        |
        |  src/hml_v3/representation_search/            THE SEARCH
        |     genome.py       42 axes, 4.095e19 points
        |     projection.py   canonical <-> Document  (what is written)
        |     document.py     Document <-> text       (how it is written)
        |     expressions.py  expression tree <-> text
        |     compiler.py     one generic compiler, genome-configured
        |     gates.py        six hard gates
        |     metrics.py      21 measured metrics, 7 Pareto axes
        |     pareto.py       non-dominated sorting, crowding, novelty, epsilon front
        |     mutations.py    hypothesis-carrying mutation library
        |     failure_memory.py  19 recorded lessons, enforced
        |     adversarial.py  14 synthetic structural fixtures
        |     sealing.py      family-level split, sealed evaluator
        |     controller.py   recursive loop, checkpoint and resume
        v
data/representation_search/   search_state.json, candidate_registry.jsonl, generations/
reports/representation_search/PRETRAINING_FRONTIER_V1.{md,json}
```

## What Changed in V2

V1's controller called `targeted_proposals`, `local_neighbourhood` and `random_walk` against a
hard-coded `AXIS_MECHANISM` table. That made it a recombination engine: if the best
representation needed an idea absent from the 42 axes, the search had zero probability of
finding it. V2 replaces that with a proposal channel.

| Defect in V1 | What V2 does |
|---|---|
| Claude built the engine but was not in the loop | `MetaDesignerBackend` with a deterministic control and an `LLMMetaDesigner` running a local frozen model |
| Search confined to 42 human-chosen axes | `NEW_AXIS`/`NEW_PRIMITIVE` proposals bind to executable projection hooks and grow the genome |
| Corruption applied to rendered *text*, biasing syntax families | `semantic_mutations` corrupts the canonical state once, upstream of every candidate |
| Validation received but not enforced | a child enters the elite population only if its dev gain reproduces on validation |
| Sealed split isolated by discipline | isolated by construction: separate process, aggregates only, child-side access log |
| One tokenizer (GPT-2) | four exact byte-level BPE vocabularies |
| No mechanism-specific instruments | nine CPU query suites measuring structural access cost |

## Capabilities Implemented

- Fresh Lean elaboration capturing exact `Expr` trees, stable `FVarId`/`MVarId` identity,
  metavariable declarations and assignments, local dependency references, `InfoTree` paths
  and environment provenance.
- Streaming, crash-safe ingestion of a multi-gigabyte raw campaign into a canonical corpus
  with per-exclusion accounting, written as size-capped shards whose concatenation is
  byte-identical to the single-file form.
- A machine-readable representation genome with a generated JSON Schema.
- One generic representation compiler: genome in, matched renderer and parser out.
- Six hard semantic gates, each traceable to a recorded prior failure.
- A 21-metric static evaluator with two independent token measurements.
- Non-dominated selection with crowding, novelty slots and pinned baselines.
- A hypothesis-carrying mutation library with a causal model per axis, plus group crossover
  and diversity jumps.
- A persistent failure memory that blocks mutations reproducing recorded negatives.
- A synthetic adversarial generator for structures real traces under-represent.
- Family-level corpus splitting with an aggregates-only, access-logged sealed evaluator.
- A recursive controller that checkpoints every generation and resumes exactly.
- A typed, schema-validated, statically safety-checked proposal channel; free-form model text
  never reaches a file, a genome or the compiler.
- A projection algebra (`neighbourhood_capsule`, `duplicate_adjacent`, `section_partition`,
  `record_reorder`) that invented axes bind to, with unbindable proposals recorded as
  `ACCEPTED_UNIMPLEMENTABLE` rather than silently dropped.
- Genome migration: an axis added at schema v2.N is absent-means-`NONE` in every older
  genome, so a candidate evaluated before the axis existed re-renders byte-identically.
- Ten canonical-level semantic mutation families with an applicability report.
- Nine structural-access microtest suites whose ground truth is the canonical state.
- Targeted corpus acquisition that selects for the strata a measured gap says are missing.
- Inference-only neural microprobes with matched counterfactuals, dumb-control vetoes and a
  preregistered sequential stopping rule.
- An observable-effect gate: a newly invented axis is rendered at every value and kept only if
  at least two differ, so the search cannot inflate its own space with inert dimensions.

## Work Completed to Date

1. **Foundation (Codex, inherited).** Asset inventory over 7 repositories and 26 datasets;
   `LEAN_PIPELINE_V1` with 1,000 unique-theorem transitions; ten V1 renderer candidates;
   `LeanRuntimeState` V2 extractor and campaign driver.
2. **Substrate certification (this stage).** The 500-target V2 campaign was aggregated. The
   original driver aborted on a truncated 350 MB document; a streaming reader replaced it and
   records every defect instead of aborting.
3. **Corpus.** Two Lean campaigns over the complementary halves of the V1 sample: 1,000
   selected transitions, 608 recovered into the canonical corpus across 27 Mathlib domains,
   mean 13.4 local declarations and 63.4 intra-context references per transition. Every one
   of the 392 unrecovered selections is counted by reason.
4. **Failure memory.** 22 lessons: 17 carried in from prior repositories and 5 measured
   here (`FM-018` to `FM-022`).
5. **Search engine.** Built and tested; 38 dedicated tests, 58 in the suite.
6. **Pilot search run.** 12 generations over the 317-transition corpus: 208 candidates
   registered, 165 evaluated, 27 hard-rejected, 182 hypotheses refuted. It measured five new
   negatives, all now in the failure memory: goal-centred ordering loses again with real
   dependencies present; DAG hoisting costs +136% tokens; identifier-corruption detection
   saturates; goal linearization is unmeasurable at 1.01 goals per state; and the glyph
   escaping penalty reproduces under a second vocabulary while absolute token counts do not.
7. **Second campaign.** Complete: 500 files, 498 jobs passed, 2 failed. Merged into the
   corpus, which doubled from 317 to 608 transitions.
8. **Definitive search.** 30 generations on the merged corpus, re-run from generation zero
   after a metric defect was found and fixed (`FM-023`). 616 candidates registered, 489
   evaluated, 107 hard-rejected (82 semantic round-trip, 13 ambiguous lexicon, 12 glyph
   fidelity). Every one of the sixteen hand-specified seeds — prior HML, Structured English,
   Lean-like, typed AST included — was pushed off the strict Pareto front by candidates the
   search constructed. The cheapest finalist costs 5,131 GPT-2 tokens per transition against
   5,979 for the best seed.
9. **Verification of the search itself.** 373 candidates re-render byte-identically in a
   fresh subprocess under a different hash seed; 296 gate verdicts are unchanged on a
   disjoint dev slice; 5 of 7 axis leaders survive on the validation split selection never
   read; the sealed split was read once, for the 6 finalists, and all 6 pass every gate on it.

## Important Files and Artifacts

| Path | What it is |
|---|---|
| `data/corpus/lean_runtime_v2.canonical.part-*.jsonl.gz` | the canonical transition corpus, in three size-capped shards; content SHA-256 `125f8add19741df9...78d6`, recorded with the shard layout in the corpus audit |
| `reports/audits/LEAN_RUNTIME_V2_CORPUS.md` | corpus accounting, every exclusion counted |
| `research/representation_search/HML_FAILURE_MEMORY.md` | the persistent failure memory |
| `research/representation_search/SEARCH_SPACE.md` | the 42 axes and what they mean |
| `research/representation_search/OBJECTIVES.md` | gates, metrics, and the epistemic limit |
| `research/representation_search/SEALED_EVALUATION_POLICY.md` | what may read the sealed split |
| `schemas/representation_search_genome.schema.json` | generated from the axis registry |
| `data/representation_search/` | search state, registry, per-generation checkpoints |
| `data/tokenizer/gpt2/` | pinned GPT-2 BPE with acquisition receipt |

## Data Sources and Provenance

Lean 4.10.0-rc1 (`3b58e0649156`) over Mathlib `29dcec074de168ac2bf835a77ef68bbe069194c5`,
joined to the pinned LeanDojo Benchmark 4 trace. The committed corpus carries a content hash
over its concatenated rows that is independent of how they are sharded, so the corpus every
result was measured on is identifiable from the repository alone. The GPT-2 tokenizer is pinned by SHA-256
with a reproducible acquisition script. Raw campaign captures (54 GB and growing) remain
external and ignored; only the canonical corpus and audits are committed.

Two non-Lean sources are registered with explicit evidence roles (`D-021`). PRM800K is
`DISCOVERY_GRAPH_EVIDENCE`: it names the five discovery dimensions a Lean trace structurally
cannot contain, because a trace holds only the steps that were kept. GSM8K is
`NATURAL_LANGUAGE_MATH_EVIDENCE` at pinned commit `3101c7d5`, MIT, 8,792 rows. Neither may
carry the role `LEAN_FORMAL_TRUTH` or a trust tier of A or B, and
`tests/test_registry_and_manifests.py` enforces that mechanically rather than by convention.

## Decisions and Rationale

`D-001` to `D-009` are inherited. `D-010` to `D-017` were added at this stage and cover: the
genome-as-data architecture, the declared semantic contract, layout versus order, per-family
corruption reporting, saturated-instrument handling, the sealed split, vocabulary-named token
claims, and the size-bounded corpus.

## Open-Ended Search Results

106 generations on the 918-transition search pool (`search_pool_v2`), 5h03m wall clock,
three meta-designer backends. **Converged**, not stopped on a budget.

| Field | Value |
|---|---|
| Corpus | `search_pool_v2`, 918 transitions, 612 families; dev 717 / validation 201 |
| Genome axes | 42 -> 47 (schema `representation-genome-v2.5.0`) |
| Search space | 4.422e21 points |
| Candidates registered / evaluated / killed | 566 / 531 / 33 |
| Strict Pareto front | 104 |
| Reported finalists | 7 |
| Axis proposals reaching the registry | 289 |
| — accepted as new dimensions | 5 |
| — rejected as behavioural duplicates | **205** (`FM-033`) |
| — rejected as unimplementable | 79 |
| Finalists using an invented axis | **2 of 7** (`FM-034`) |
| Quarantined as non-generalising | 12 |
| Structural convergence | **YES**, generation 106 |
| Sealed split reads | **0** |

**Every one of the sixteen hand-specified seeds was pushed off the strict Pareto front** —
prior HML, Structured English, Lean-like, typed AST, canonical S-expression and JSON
included. None is a finalist.

**The frontier moved a long way and then stopped.** Between generation 0 and generation 60
the per-axis frontier minima improved by 20.5% on tokens, 18.5% on binder-use distance, 24.3%
on binder-query distance and 24.1% on dependency-query distance. From generation 60 the
position was byte-identical on all six axes; from generation 101 no candidate entered or left
the front at all.

**Locality improved far more than cost.** Token count moved 20.5% while the three locality
axes moved 18–24%, and on the previous 608-transition corpus locality was the thing that could
not be optimised at all. This is the acquisition campaign paying off: locality is only
measurable where states have multiple goals and real dependencies (`FM-020`, `FM-028`).

**An invented axis reached the finalists**, which `FM-030` reported had never happened. Both
are values of `dependency_capsule`: `R_159628756bc5` (`GOAL_LOCAL`) is the cheapest candidate
under all four tokenizer vocabularies, and `R_fcd13f8d56a5` (`ACTION_LOCAL`) reaches 11.84
dependency-query token distance against roughly 27.8 for the rest, a 57% reduction. That axis
is also the one the meta-designers re-proposed endlessly under fresh names; registering it
once and blocking 205 aliases is what let it be judged on its merits.

**Multi-tokenizer audit**: four exact BPE vocabularies (`gpt2`, `gptneox`, `qwen25`,
`starcoder2`) agree on the cheapest finalist. `FM-018` binds the reading: the escaping penalty
reproduces across vocabularies, the absolute counts do not.

Five defects were found in this project's own instruments during this stage, each by checking
the instrument against a real measurement rather than trusting the number it produced:

| Lesson | Defect |
|---|---|
| `FM-029` | the semantic corruption metric replaced text-level bias with saturation at 1.000; removed from selection (`D-018`) |
| `FM-031` | prefix sampling hid the multi-goal structure the acquisition campaign had just bought; no prefix up to 128 rows contained a state with more than four goals (`D-019`) |
| `FM-032` | the wrong ollama endpoint made a second meta-designer return an empty string on every prompt, silently, for as long as there was only one backend |
| `FM-033` | nine of the first thirty invented axes were one axis under nine names; the space figure was inflated and convergence was unreachable (`D-022`) |
| `FM-035` | a mid-run churn rate was read as proof a convergence criterion could not be met; it could, and was |

## Verification and Test Results

- `.venv/bin/python -m pytest` — **156 tests, 338 subtests, all passing**. Note that the
  repository ships no `.venv` and the system interpreter has no pytest, so a bare
  `python3 -m pytest` prints `No module named pytest` and **exits 0** — a run that looks
  clean and verifies nothing. `pyproject.toml` now pins `testpaths = ["tests"]`, without
  which pytest collects the vendored LeanDojo checkouts and dies on their imports.
- `scripts/search/validate_frontier.py` — 5 of 7 axis leaders keep their lead on the
  validation split that selection never read.
- Expression codec: every lossless configuration round-trips (192 configurations).
- Document codec: 7,776 grammar/lexicon/notation configurations round-trip.
- Every single-axis genome change either round-trips or is declared lossy, and every declared
  lossy value actually fails a gate.
- All 16 generation-zero seeds pass all six hard gates on the real corpus.
- Checkpoint and resume verified: a fresh controller resumes at the exact next generation with
  an identical population and registry.

## Known Failures and Limitations

- **The corpus is 608 transitions, not 50,000.** 392 of 1,000 selected transitions were not
  recovered: 272 exceeded the declared canonical size budget, 96 exceeded the raw element
  budget, 9 were duplicate record ids, 7 elaboration jobs failed with Lean memory errors, and
  1 raw document is truncated. All are counted in `reports/audits/LEAN_RUNTIME_V2_CORPUS.md`.
  Reaching 50,000 at this fidelity would need roughly 80 more campaigns of this size,
  something on the order of 4 TB of raw captures and days of elaboration.
- **Lean's metavariable inventory is quadratic in some proofs.** Four raw documents are
  between 6.8 GiB and 24 GiB. Nothing is wrong with the extractor's fidelity; the inventory
  is genuinely that large, and bounding it would change the V2 contract.
- **`GAP-003`, `GAP-005` and `GAP-007` remain open** — Lean 4.10 exposes no standalone
  constraint table, a tactic can consult locals without leaving a `TermInfo`, and consulted
  simp sets are not generally recoverable.
- **No model evidence exists.** Every result here is static.
- **Token counts are vocabulary-specific.** Under GPT-2 the corpus's mathematical glyphs cost
  2–3 tokens each; the prior audit measured 1 under Qwen3-8B.
- **The pilot run's locality numbers are wrong and are retained only as archived history.**
  They were computed before `FM-023` — a substring match that overcounted short identity
  mentions by 25% — was found and fixed. The definitive run is not comparable to them.

## Risks and Technical Debt

- Strict non-dominated sorting over seven axes puts most of a grown population on the front;
  reporting uses an epsilon-front, which introduces a reported-shortlist parameter.
- The synthetic adversarial fixtures are a correctness probe, never model evidence (`FM-014`).
- The V1 renderer family in `src/hml_v3/renderers/` is superseded by the generic compiler but
  retained; it should not be mistaken for a comparable candidate set.

## Current Blockers

None.

## Exact Next Actions

1. **Decide whether to read `SEALED_FINAL_V2`.** The search has converged and the seal has
   been read zero times, so the precondition its policy names is met. Reading it is a
   one-shot, irreversible act — after it, no frontier chosen with knowledge of the result is
   being tested against data that never influenced it. It should be read once, on these seven
   finalists, through `sealed_service.py`, and only on an explicit decision to do so.
2. **Re-measure the previous run's space-growth claim.** `FM-033` shows that the 42 -> 55
   axes / 1.548e26 points figure counted duplicate axes as new dimensions. It should not be
   repeated without re-measurement.
3. **Consider revising the meta-designer brief.** Its worked example is `dependency_capsule`,
   and the backends copied that shape 205 times. The duplicate gate makes this harmless but
   wasteful; changing the brief would change what the backends propose and should be a
   recorded decision, not a side effect.
4. **Design the model experiment** on the seven finalists: matched envelope (`FM-001`), the
   six lexical controls (`FM-003`), and a task that does not saturate (`FM-010`). Frozen
   inference first. Ask before any paid GPU run.
