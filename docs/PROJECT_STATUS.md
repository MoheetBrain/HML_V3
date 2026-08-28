# Project Status

## Project Objective

Discover, by evidence rather than by design taste, which machine-facing representation of
mathematical state best supports verified mathematical reasoning. Mathematical truth is held
fixed as a `CanonicalMathState` derived from Lean; the representation `R_phi(M)` is the
dependent variable and is searched over.

## Current Stage

`OPEN_ENDED_SEARCH_V2`. The closed 42-axis search is frozen and preserved; the loop has been
rebuilt so a model-driven meta-designer sits inside it and can widen the search space itself.

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

## Decisions and Rationale

`D-001` to `D-009` are inherited. `D-010` to `D-017` were added at this stage and cover: the
genome-as-data architecture, the declared semantic contract, layout versus order, per-family
corruption reporting, saturated-instrument handling, the sealed split, vocabulary-named token
claims, and the size-bounded corpus.

## Open-Ended Search Results (live)

| Field | Value |
|---|---|
| Genome axes | 42 -> 50 (schema `representation-genome-v2.8.0`) |
| Search space | 4.095e19 -> 3.582e23 points |
| Invented axes accepted | 8 |
| Invented axes rejected as inert | recorded, `FM-026` |
| Candidates killed at compile / semantics | 2 / 4 |
| Proposal types the model produced | `AXIS_MUTATION`, `ARCHITECTURAL_HYPOTHESIS`, `NEW_AXIS`, `NEW_PRIMITIVE`, `CORPUS_ACQUISITION` |
| Structural convergence | **NO** — running against a generation budget |

Three defects were found in this project's own instruments, each by checking the instrument
against a real rendering rather than trusting the number it produced:

| Lesson | Defect |
|---|---|
| `FM-023` | a substring scan overcounted identity mentions by 25% |
| `FM-025` | a colon heuristic made four of nine microtest suites read 100% unanswerable |
| `FM-026` | three invented axes were accepted whose nine value combinations rendered identically |
| `FM-027` | the validation gate blocked candidates that failed consistently rather than divergently |

## Verification and Test Results

- `PYTHONPATH=src python3 -m unittest discover -s tests` — **120 tests, all passing**, of
  which 64 are the inherited V1 tests, unchanged.
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

1. **Continue the search.** It stopped on its 30-generation budget with a stall count of 1,
   not on structural convergence — the frontier was still moving. The state resumes exactly:
   `python3 scripts/search/run_representation_search.py --generations 20`.
2. **Enlarge the corpus** if the frontier keeps moving. Two more campaigns over untouched
   Mathlib files would roughly double it again; 50,000 at this fidelity needs ~80.
3. **Design the model experiment** on the six finalists: matched envelope (`FM-001`), the six
   lexical controls (`FM-003`), and a task that does not saturate (`FM-010`). Frozen
   inference first.
