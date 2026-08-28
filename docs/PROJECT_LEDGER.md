# Project Ledger

## 2026-08-27 — repository bootstrap

**Branch:** `codex/evidence-first-foundation`

The repository was initialized as an evidence-first mathematical representation discovery
system. The first milestone is a real Lean transition pipeline with an explicit canonical IR
boundary and matched renderers. Prior HML is retained as evidence and a candidate renderer,
not adopted as the foundation. No GPU or training work is authorized in this milestone.

## 2026-08-27 — complete prior-asset inventory

Read-only inspection covered seven repositories, all visible Git refs and worktrees,
historical dataset/experiment manifests, 803 dataset-like files, and external caches. The
machine inventory classifies 41 assets and reports zero missing registered local artifacts.
The central registry now contains 26 datasets across trust tiers A–E.

## 2026-08-27 — pin formal source family

Mathlib/LeanDojo Benchmark 4, LeanDojo V2, Lean Workbook, miniF2F, and the ProofNet Lean 4
port were acquired or metadata-pinned at exact commits through reproducible scripts. Large
payloads/checkouts remain ignored. Lean Workbook is Apache-2.0 per its pinned card; miniF2F
and ProofNet are protected evaluation sources and are not mislabelled as verified proofs.

## 2026-08-27 — LEAN_PIPELINE_V1

A deterministic sample selects all 100 Stage100 attestation rows plus 900 parser-clean,
official-train, unique-theorem rows balanced across eight recorded effect classes. Every row
joins exactly to the official LeanDojo tactic/before/after trace and the theorem source.
The join recovers 1,353 official external premise references on 578 rows. The adapter keeps
raw states/tactics byte-exact, decomposes all displayed goal contexts, and records 659
disagreements with the old lossy structured projection.

Declared-observation losslessness passes 1,000/1,000. Ten renderer candidates—Lean-like,
previous HML, typed AST, Structured English, S-expression, graph edges, goal-local,
dependency-topological, explicit-redundant, and minimal machine code—pass 10,000/10,000
combined semantic round trips and deterministic byte checks. The previous-HML renderer is a
read-only compatibility-bridged baseline at `b011511e72572608eb7836d3b8a1a6bb794c890d`.

Verifier language remains calibrated: 32 rows are fresh exact-replay passes; 968 are formal
trace accepted, including 68 with nonpass Stage100 certificates. Eight empirical real-math
gaps are registered. No GPU was used and no training was performed.

## 2026-08-28 — certify the V2 runtime substrate and build the canonical corpus

**Branch:** `codex/lean-runtime-semantic-capture-v2`
**Stage:** LEAN_RUNTIME_V2 -> REPRESENTATION_SEARCH_V1

**Objective.** The inherited V2 mission ended partially: the Lean extractor and campaign
driver existed, a 500-target campaign had produced 54 GB of raw captures, but the aggregation
step had never completed and no canonical corpus existed. Nothing downstream could be trusted
until the substrate was certified.

**What was found.** Re-running the driver's audit phase reproduced its failure: it aborts on
`json.loads` of a raw document truncated at 350 MB. Two further defects were then measured:
four of the 250 raw documents are between 6.8 GiB and 24 GiB because Lean's accumulated
metavariable inventory is quadratic in some proofs, and the driver loads each document whole.

**What was built.** `scripts/audit/stream_runtime_v2_corpus.py` streams the top-level
`captures` array element by element with a byte-exact scanner that tracks JSON string and
escape state while jumping between structural bytes with a regex. The first implementation
iterated per byte and would have taken about two hours over 54 GB; the regex version runs at
roughly 100 MB/s. Every defect is recorded per file rather than aborting the run, and every
excluded capture is counted by reason.

**Result.** 317 canonical transitions across 26 Mathlib domains, from 500 selected. The 183
that were not recovered are accounted for: 117 exceeded the declared 256 KiB canonical size
budget, 51 exceeded the raw element budget, 7 were duplicate record ids, 5 elaboration jobs
had failed with Lean memory errors, 1 raw document is truncated.

**Verification actually executed.**
- `python3 scripts/audit/stream_runtime_v2_corpus.py --campaign-dir external/runtime_probe/campaign500`
  — completed; wrote `reports/audits/LEAN_RUNTIME_V2_CORPUS.{md,json}`.
- Scanner correctness: streamed captures compared byte-for-byte against `json.load` on four
  small documents — identical.
- Corpus structure measured: mean 13.4 local declarations, 63.4 intra-context references,
  1.12 external premises per transition; 305 of 317 transitions carry at least one dependency
  edge.

**Effect on the project.** `FM-014` recorded that the prior corpus averaged 1.00 claims per
state and zero dependencies, which made every ordering and locality result synthetic. This
corpus is structurally rich, so locality is measurable on real mathematics for the first time.

**Next intended step.** Build the representation search on top of it.

## 2026-08-28 — the representation architecture search engine

**Branch:** `codex/lean-runtime-semantic-capture-v2`
**Stage:** REPRESENTATION_SEARCH_V1

**Objective.** Stop designing a language by hand. Make the language data, and search it.

**What was built.** `src/hml_v3/representation_search/` — a 42-axis `RepresentationGenome`
(4.095e19 points) with a generated JSON Schema; one generic compiler that turns a genome into
a matched renderer and parser; six hard semantic gates; a 21-metric static evaluator with two
independent token measurements; non-dominated selection with crowding, novelty and pinned
baselines; a hypothesis-carrying mutation library with a causal model per axis; a persistent
failure memory that blocks mutations reproducing recorded negatives; a synthetic adversarial
generator; family-level corpus splitting with an aggregates-only sealed evaluator; and a
recursive controller that checkpoints every generation and resumes exactly.

**Decisions made and why.** `D-010` through `D-017` are recorded in `DECISIONS.md`. The two
that changed the experiment most:

- *Local-context order is stated once, layout is free* (`D-012`). Lean's local-context order
  is semantic. Making layout free while the goal's context list always states canonical order
  is what lets the ordering axes be searched at all without discarding information.
- *A saturated instrument is excluded and said to be saturated* (`D-014`). Measured across
  all sixteen seeds, `detect_corrupt_identity` read 1.000 everywhere. Following `FM-010` it
  was removed from the Pareto axes **before** the search began, and `detect_drop_field`
  replaced it.

**Verification actually executed.**
- `PYTHONPATH=src python3 -m unittest discover -s tests` — 58 tests, all passing.
- 192 expression-codec configurations round-trip; 7,776 document-codec configurations
  round-trip.
- Every single-axis genome change either round-trips or is declared lossy, and every declared
  lossy value actually fails a gate. This test found three real defects: `binder_encoding`
  clamped a de Bruijn index with no binder in scope, `implicit_argument_visibility` was
  declared lossy but unimplemented, and `literal_form=BARE` renamed every literal because the
  synthetic fixtures spelled Lean's `NAT` kind as `natural`.
- All 16 generation-zero seeds pass all six hard gates on the real corpus.
- Checkpoint and resume verified against a live workspace.

**Failures and unresolved uncertainty.** Strict non-dominated sorting over seven axes leaves
most of a grown population on the front; the reported shortlist is therefore an epsilon-front
at 2%, which introduces a reporting parameter that selection does not use. The corpus is 317
transitions, not the 50,000 the mission asked for, and the reason is measured rather than
estimated.

**Next intended step.** Run generations to structural convergence, extend the corpus with a
second campaign, then perform the single sealed evaluation.

## 2026-08-28 — PRM800K discovery analysis

**Branch:** `codex/lean-runtime-semantic-capture-v2`

**Objective.** Use PRM800K for what it can support — naming dimensions a formal trace cannot
express — without contaminating verifier-backed status.

**Result.** Over 20,949 labelled attempts, 168,513 steps and 256,429 rated continuations:
61.1% progress, 11.7% valid-but-not-progressing, 24.4% dead ends, and 16,750 steps where every
offered continuation was rejected. **No representation in the search space can express any of
these dimensions**, and the reason is not the representation: `CanonicalMathState` has no
field for progress, usefulness, dead ends, alternative branches, or attempt outcome. A Lean
trace contains only steps that were kept, so the formal corpus has no negative examples at
all.

**Verification actually executed.**
`python3 scripts/analysis/prm800k_discovery_analysis.py` — completed; wrote
`reports/representation_search/DISCOVERY_REPRESENTATION_ANALYSIS.{md,json}`.

**Effect on the project.** The search is scoped honestly: it optimises representations of
*verified transitions* and says nothing about representations of *search state*. Producing the
latter needs a state paired with several candidate actions and per-candidate outcomes, which
is a proof-search acquisition problem and out of scope for this mission.

**Next intended step.** Finish the second campaign, rebuild the corpus, and run the search to
convergence on the extended corpus.
