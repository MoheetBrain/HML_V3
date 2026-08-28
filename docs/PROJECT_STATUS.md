# Project Status

## Project Objective

Discover, by evidence rather than by design taste, which machine-facing representation of
mathematical state best supports verified mathematical reasoning. Mathematical truth is held
fixed as a `CanonicalMathState` derived from Lean; the representation `R_phi(M)` is the
dependent variable and is searched over.

## Current Stage

`REPRESENTATION_SEARCH_V1`. The Lean runtime truth substrate is certified, a canonical
transition corpus is built and split, and a recursive architecture search over a 42-axis
representation genome has been implemented and run.

## Current Branch

`codex/lean-runtime-semantic-capture-v2`

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

## Capabilities Implemented

- Fresh Lean elaboration capturing exact `Expr` trees, stable `FVarId`/`MVarId` identity,
  metavariable declarations and assignments, local dependency references, `InfoTree` paths
  and environment provenance.
- Streaming, crash-safe ingestion of a multi-gigabyte raw campaign into a canonical corpus
  with per-exclusion accounting.
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

## Work Completed to Date

1. **Foundation (Codex, inherited).** Asset inventory over 7 repositories and 26 datasets;
   `LEAN_PIPELINE_V1` with 1,000 unique-theorem transitions; ten V1 renderer candidates;
   `LeanRuntimeState` V2 extractor and campaign driver.
2. **Substrate certification (this stage).** The 500-target V2 campaign was aggregated. The
   original driver aborted on a truncated 350 MB document; a streaming reader replaced it and
   records every defect instead of aborting.
3. **Corpus.** 317 canonical transitions over 26 Mathlib domains, mean 13.4 local
   declarations and 63.4 intra-context references per transition.
4. **Failure memory.** 19 lessons, 17 from prior repositories and 2 measured here.
5. **Search engine.** Built and tested; 38 dedicated tests, 58 in the suite.
6. **Search run.** Recursive generations over the dev split, checkpointed and resumable.
7. **Second campaign.** A complementary 500-target campaign over the untouched half of the
   V1 sample is running to extend the corpus.

## Important Files and Artifacts

| Path | What it is |
|---|---|
| `data/corpus/lean_runtime_v2.canonical.jsonl.gz` | the canonical transition corpus |
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
joined to the pinned LeanDojo Benchmark 4 trace. The GPT-2 tokenizer is pinned by SHA-256
with a reproducible acquisition script. Raw campaign captures (54 GB and growing) remain
external and ignored; only the canonical corpus and audits are committed.

## Decisions and Rationale

`D-001` to `D-009` are inherited. `D-010` to `D-017` were added at this stage and cover: the
genome-as-data architecture, the declared semantic contract, layout versus order, per-family
corruption reporting, saturated-instrument handling, the sealed split, vocabulary-named token
claims, and the size-bounded corpus.

## Verification and Test Results

- `PYTHONPATH=src python3 -m unittest discover -s tests` — 58 tests, all passing.
- Expression codec: every lossless configuration round-trips (192 configurations).
- Document codec: 7,776 grammar/lexicon/notation configurations round-trip.
- Every single-axis genome change either round-trips or is declared lossy, and every declared
  lossy value actually fails a gate.
- All 16 generation-zero seeds pass all six hard gates on the real corpus.
- Checkpoint and resume verified: a fresh controller resumes at the exact next generation with
  an identical population and registry.

## Known Failures and Limitations

- **The corpus is 317 transitions, not 50,000.** 183 of 500 selected transitions were not
  recovered: 117 exceeded the declared canonical size budget, 51 exceeded the raw element
  budget, 7 were duplicate record ids, 5 elaboration jobs failed with Lean memory errors, and
  1 raw document was truncated. All are counted in the corpus audit.
- **Lean's metavariable inventory is quadratic in some proofs.** Four raw documents are
  between 6.8 GiB and 24 GiB. Nothing is wrong with the extractor's fidelity; the inventory
  is genuinely that large, and bounding it would change the V2 contract.
- **`GAP-003`, `GAP-005` and `GAP-007` remain open** — Lean 4.10 exposes no standalone
  constraint table, a tactic can consult locals without leaving a `TermInfo`, and consulted
  simp sets are not generally recoverable.
- **No model evidence exists.** Every result here is static.
- **Token counts are vocabulary-specific.** Under GPT-2 the corpus's mathematical glyphs cost
  2–3 tokens each; the prior audit measured 1 under Qwen3-8B.

## Risks and Technical Debt

- Strict non-dominated sorting over seven axes puts most of a grown population on the front;
  reporting uses an epsilon-front, which introduces a reported-shortlist parameter.
- The synthetic adversarial fixtures are a correctness probe, never model evidence (`FM-014`).
- The V1 renderer family in `src/hml_v3/renderers/` is superseded by the generic compiler but
  retained; it should not be mistaken for a comparable candidate set.

## Current Blockers

None blocking. The second Lean campaign is running; the corpus will be rebuilt and the search
extended when it finishes.

## Exact Next Actions

1. Finish the second 500-target campaign and rebuild the corpus.
2. Re-run the search on the extended corpus and continue to structural convergence.
3. Perform the single sealed evaluation and publish `PRETRAINING_REPRESENTATION_FRONTIER_V1`.
4. Only then design a matched, control-gated model experiment on the finalists.
