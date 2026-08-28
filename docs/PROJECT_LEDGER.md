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

## 2026-08-28 — pilot search run and its five measured negatives

**Branch:** `codex/lean-runtime-semantic-capture-v2`
**Stage:** REPRESENTATION_SEARCH_V1

**Objective.** Exercise the engine end to end on the real corpus and see whether it produces
mechanism-level results rather than a leaderboard.

**What ran.** 12 generations across the phase schedule (exposure, then architecture, then
grammar, then lexicon): 208 candidates registered, 165 evaluated, 27 hard-rejected, 182
hypotheses refuted.

**Measured negatives, all appended to the failure memory.**

- `FM-021` — goal-centred context ordering changed `binder_use_distance_tokens` by **+3.8%**
  across two parents with 100% sign agreement. `FM-005` had granted exactly one retry on the
  stated changed condition that the V2 corpus carries real dependency structure. The retry
  was taken, the result reproduced, and the budget is now spent.
- `FM-022` — hoisting shared subterms into a DAG changed `bpe_tokens_per_transition` by
  **+136.4%** and dropped record-order corruption detection to 0.375. The alias table costs
  more than the sharing saves on real elaborated Lean trees.
- `FM-019` — `detect_corrupt_identity` read **1.000 for all sixteen seeds**. Following
  `FM-010` it was removed from the Pareto axes before the search began.
- `FM-020` — `graph_serialization` was mutated 11 times and changed the measurement **0
  times**, because the corpus averages 1.01 goals per state. Five further axes measured at 0%.
- `FM-018` — `FM-004`'s escaping penalty reproduces under GPT-2 (2.3x–2.7x), but the absolute
  glyph costs do not: 1 token under Qwen3-8B, 2–3 under GPT-2.

**Decisions made.** Reporting a shortlist by extreme points plus the knee rather than by an
epsilon-front: at eps=0.02 the epsilon-front still held 147 of 165 candidates, so it was not a
shortlist. Selection continued to use the strict front, so the reporting rule could not steer
the search. A material-improvement threshold of 0.5% was added to the convergence test,
because without one "the frontier moved" fires on rounding error in a growing population.

**Tests actually executed.** `PYTHONPATH=src python3 -m unittest discover -s tests` — 58
tests, all passing, after each change above. The sealed-evaluation CLI path was exercised end
to end against a synthetic corpus so the real sealed split stayed untouched.

**Failures and unresolved uncertainty.** The strict Pareto front holds 85 of 165 candidates;
seven axes is enough dimensionality that most candidates are best at something. The pilot ran
on 317 transitions and did not reach structural convergence — the frontier was still moving
at generation 11.

**Next intended step.** Merge the second campaign into the corpus, re-run the search to
convergence, perform the single sealed evaluation.

## 2026-08-28 — merged corpus, a metric defect, and the definitive search

**Branch:** `codex/lean-runtime-semantic-capture-v2`
**Stage:** REPRESENTATION_SEARCH_V1

**Objective.** Extend the corpus with the second Lean campaign and run the search that the
frontier report would be based on.

**Corpus.** Both campaigns merged: 1,000 selected transitions, **608 recovered** across 27
Mathlib domains. 392 unrecovered, all counted: 272 over the canonical size budget, 96 over
the raw element budget, 9 duplicate record ids, 7 failed elaboration jobs, 1 truncated
document. Structure is unchanged from the smaller corpus — mean 13.4 local declarations,
1.01 goals per state.

**A metric defect, found mid-run.** The definitive search had reached generation 3 when a
check of the locality metric against a real rendering showed that `bf1` was matching inside
`bf10` through `bf19`: **80 apparent mentions against a true 64, a 25% overcount**. Premise
names had the same defect (`Nat.add` inside `Nat.add_comm`). This is `FM-009`'s failure mode
in a new place. The run was killed, the metric fixed to require token boundaries, a
regression test added, the defect recorded as `FM-023`, and the search restarted from
generation zero. **The pilot run's locality numbers are inflated and are retained only as
archived history** under `data/representation_search/archive/`.

**The definitive run.** 30 generations. 616 candidates registered, 489 evaluated, 107
hard-rejected — 82 on semantic round-trip, 13 on ambiguous lexicon, 12 on glyph fidelity.
661 proposed hypotheses were refuted by measurement; 1,133 mutations were blocked by the
failure memory before any compute was spent on them.

**Result.** Six finalists, chosen by a stated rule: the best candidate on each Pareto axis
plus the knee. **Every one of the sixteen hand-specified seeds was pushed off the strict
Pareto front** — prior HML, Structured English, Lean-like and typed AST included. The
cheapest finalist costs 5,131 GPT-2 tokens per transition against 5,979 for the best seed,
and it simultaneously leads premise-to-action distance and maximum reference span.

**Strongest measured effects**, aggregated across parents with 100% sign agreement:
postfix expression notation saves **17.5%** tokens (n=5); moving the action to a header cuts
premise-to-action distance **92%** (n=5); reversing DAG hoisting improves tokens **50.9%**
(n=4), confirming `FM-022`; and `redundancy_level=EXPLICIT` *reduces* dropped-field detection
by 15–19% (n=3), which is the opposite of its predicted mechanism.

**Verification actually executed.**
- `python3 -m unittest discover -s tests` — 60 tests, all passing.
- `verify_reproducibility.py --candidates 400 --transitions 24` — 373 candidates re-rendered
  in a fresh subprocess under `PYTHONHASHSEED=12345`; **0 mismatches**.
- `audit_gates_on_holdout.py --offset 150 --size 60` — 246 evaluated and 50 hard-rejected
  candidates re-gated on a disjoint dev slice; **0 verdict disagreements**.
- `validate_frontier.py --sample 48` — **5 of 7** axis leaders unchanged on the validation
  split selection never read; Spearman rho +0.93 to +1.00 on cost and locality, **+0.357** on
  record-swap detection.
- `build_domain_profiles.py` — across 16 Mathlib domains, token cost, binder distance and
  identifier fragmentation have one leader in **100%** of domains; the detection axes in
  **38–56%**. Recorded as `FM-024`.
- `run_representation_search.py --generations 0 --seal-final` — the sealed split (120
  transitions from 101 families never read during the search) was evaluated **once**, on the
  six finalists. All six pass every hard gate on it. `sealed_access_log.jsonl` records exactly
  6 accesses.

**Failures and unresolved uncertainty.** The search **did not structurally converge**: it
stopped on its 30-generation budget with a stall count of 1, so the frontier was still moving.
Any claim that this is the frontier is a claim about 489 of 4.095e19 points. The strict front
holds 92 of 489 candidates, which is why the shortlist follows a stated rule rather than
front membership.

**One further change, forced by the commit guard.** The corpus is 8.3 MiB gzipped and the
guard caps a tracked file at 5 MiB. The corpus is a generated artifact but it is also the
object every result here is measured on, and it is not reproducible from the repository alone
because the 63 GB of raw captures stay external. Leaving it out of Git would make the results
uncheckable. It is therefore written as size-capped shards, with a shared reader that
concatenates them in name order. Verified: 608 rows in and 608 rows out, list-equal, and the
content hash `125f8add19741df90858c7976bc7c10bfce50853ff09aa09688ad802a4de78d6` is identical
to the single-file form and independent of the shard size chosen. That hash and the shard
layout are recorded in `reports/audits/LEAN_RUNTIME_V2_CORPUS.json`.

*Correction, applied 2026-08-28 in the following commit:* this paragraph originally quoted
the content hash as `125f8add19741df9`, a 16-character prefix presented as if it were the
digest. The full SHA-256 is above. The corpus itself was not affected; only this record was.

**Next intended step.** Resume the search for further generations; design the matched,
control-gated model experiment on the six finalists.

## 2026-08-28 — record the shard layout and the full corpus content hash

**Branch:** `codex/lean-runtime-semantic-capture-v2`
**Stage:** REPRESENTATION_SEARCH_V1

**Objective.** Make the corpus sharding verifiable from the committed audit rather than from
a claim in a commit message.

**What changed.** `reports/audits/LEAN_RUNTIME_V2_CORPUS.json` now carries the shard layout
with per-shard byte counts, and `corpus_content_sha256` — a SHA-256 over the concatenated
canonical rows *as read back*, in shard-name order. That is a different quantity from the
builder's existing `corpus_sha256`, which hashes the list of per-row canonical hashes. The
new field is the one that verifies sharding changed nothing, because it is independent of how
many shards the rows were split across.

The previous ledger entry quoted a 16-character prefix as if it were the digest. That was a
factual error; it is corrected in place and the correction is noted inside that entry, as the
protocol requires.

**Verification actually executed.**
- `corpus_sha256(base)` over the three committed shards:
  `125f8add19741df90858c7976bc7c10bfce50853ff09aa09688ad802a4de78d6`.
- Shard sizes 4,212,415 / 4,196,355 / 272,587 bytes — each below the 5 MiB tracked-file cap.
- `python3 -m unittest discover -s tests` — 64 tests, all passing, including the sharding
  tests that assert the content hash is independent of shard size.
- `audit_gates_on_holdout.py` re-run against the sharded corpus: 489 evaluated and 107
  hard-rejected candidates, **0 verdict disagreements** — confirming the readers see the same
  corpus after sharding as before.

**Failures and unresolved uncertainty.** None introduced. The search's own limitation is
unchanged: it stopped on its generation budget, not on structural convergence.

**Next intended step.** Resume the search for further generations; design the matched,
control-gated model experiment on the six finalists.

## 2026-08-28 — rebuild the loop so the search can widen its own space

**Branch:** `codex/open-ended-search-v2` (V1 preserved at tag
`hml-v3-closed-search-v1-2026-08-28`)
**Stage:** REPRESENTATION_SEARCH_V1 -> OPEN_ENDED_SEARCH_V2

**Objective.** The V1 search could only recombine 42 human-chosen axes. Its controller called
fixed proposal functions against a hard-coded causal table, so an idea outside the genome had
zero probability of being found. This entry records rebuilding that loop.

**What was built.**

- `meta_designer/`: a typed proposal channel. `schemas.py` defines eight proposal types and
  validates every one; `static_safety` refuses anything naming the canonical layer, the
  verifier, the sealed split or the host. `DeterministicMetaDesigner` reproduces V1's
  behaviour as a control. `LLMMetaDesigner` runs a local frozen model through a pluggable
  transport.
- `primitive_registry.py`: a projection algebra of four executable hooks. An invented axis is
  accepted only when its stated behaviour binds to one; anything else is recorded as
  `ACCEPTED_UNIMPLEMENTABLE`. This is a real envelope and it is stated rather than hidden.
- `genome_migrations.py`: absent-means-`NONE`, so a candidate evaluated before an axis existed
  re-renders byte-identically after it exists.
- `semantic_mutations.py`: ten corruption families applied to the *canonical state*.
- `microtests/`: nine structural-access suites with canonical ground truth.
- `validation.py`: a preregistered rule making eliteness conditional on reproduction.
- `sealed_service.py`: the sealed split in a separate process, aggregates only.
- `tokenizers.py`: four exact byte-level BPE vocabularies.
- `active_corpus.py`: acquisition targeted at measured gaps.
- `controller_v2.py`: the ladder, wiring all of the above.

**Two defects found in my own instruments, both fixed and recorded.**

1. The microtest suites initially read 100% unanswerable on four of nine suites. The cause was
   a heuristic of mine: I decided whether to route an identity through the codec by testing
   for a colon in it. The committed corpus uses short identities (`m9`, `f17`), so the test was
   false and the suite searched for `m9` in a rendering containing `bm9`. Every identity now
   routes through the codec, which returns unknown names unchanged. Recorded as FM-025.
2. The delta suite reported a hidden relation as answered, because it found the goal id
   anywhere in the rendering rather than inside a stated delta. Relational queries are now
   scoped to their section.

**Verification actually executed.**
- `PYTHONPATH=src python3 -m unittest discover -s tests` — **114 tests, all passing**, including
  all 64 inherited V1 tests unchanged.
- End-to-end invented axis: a `NEW_PRIMITIVE` proposal validated, bound to
  `neighbourhood_capsule`, registered, grew the genome 42 -> 43 axes
  (4.095e19 -> 1.228e20 points), produced a distinct candidate id, passed every hard gate, and
  under `goal_position=FIRST` moved binder-query distance **176.9 -> 104.7 tokens (-41%)** with
  round-trip intact. Under `goal_position=AFTER_CONTEXT` it is a no-op and renders identically,
  which is the correct behaviour and a genuine axis interaction the closed search could not
  have found.
- LLM backend against local `gemma3:4b`: proposes valid `AXIS_MUTATION` and `NEW_AXIS`
  proposals. Its first attempts used synonym field names and were all rejected; after adding
  worked examples and the executable-hook list to the brief, it proposed three implementable
  new axes in direct response to the measured weakness that scope queries cost ~2,400 tokens.
- Tokenizers: GPT-2, Qwen2.5, GPT-NeoX and StarCoder2 load as exact byte-level BPE. Gemma is
  gated on HuggingFace (HTTP 401) and is reported unavailable rather than skipped silently.
  FM-018 reproduces exactly: `⊢` costs 1 token under Qwen2.5 and 2-4 under the others.

**Corpus acquisition.** 250,814 LeanDojo transitions were scanned and 1,134 selected against
the strata the measured gaps name — 565 multi-goal states against a current corpus averaging
1.01 goals per state, 487 with 31+ hypotheses, 215 with 6+ premises. 1,125 joined to an exact
source byte range; the 9 that did not are counted. The prepare step no longer aborts the whole
campaign when one record fails to join.

**Failures and unresolved uncertainty.** The open-endedness has a stated envelope: a proposal
whose behaviour does not bind to one of four projection hooks cannot be executed. `gemma3:4b`
is a small model and roughly a third of its proposals are still malformed. The targeted Lean
campaign is still elaborating, so the enlarged corpus is not yet in the search.

**Next intended step.** Finish the campaign, rebuild the corpus, freeze `SEALED_FINAL_V2`, add
inference-only neural microprobes, and run the open-ended search.

## 2026-08-28 — the loop invents three axes, and three of them are inert

**Branch:** `codex/open-ended-search-v2`
**Stage:** OPEN_ENDED_SEARCH_V2

**Objective.** Run the open-ended loop for real and see what it actually does.

**What happened.** In the first live generation the model-driven meta-designer proposed three
new axes with plausible mechanisms — `goal_refinement`, `context_signature`, `context_range` —
and the system accepted all three, registering them and bumping the genome schema to
`v2.3.0`. Checking them rather than trusting them showed that **all nine of their axis-value
combinations rendered identically**. The search had grown its own space by three dimensions of
nothing.

**Two causes, both mine.**

1. The projection hooks matched value names literally (`GOAL_LOCAL`, `BEFORE`, `REVERSE`). An
   axis whose inventor chose `WIDE`/`NARROW` fell through to a branch that happened to
   reproduce the existing layout. Hooks now index behaviour by the value's *position* among
   the non-`NONE` values, so any naming an inventor picks is functional.
2. Acceptance condition 6 — "at least one value differs observably on the corpus" — was
   written in the spec and never enforced. Registration now renders every value of a new axis
   on a sample and rejects it as `NO_OBSERVABLE_EFFECT` if they all agree.

An inert axis is worse than no axis: it consumes search budget and inflates the apparent size
of the space, which would have made the frontier report overstate what the search explored.

**Verification actually executed.**
- `PYTHONPATH=src python3 -m unittest discover -s tests` — **114 tests, all passing**, with four
  new regression tests covering positional hook dispatch, an axis named `WIDE`/`NARROW`
  rendering differently, an inert axis being rejected, and an effective axis passing.
- Re-run after the fix: three axes accepted (`goal_context_fragment`, `meta_cache_probe`,
  `binder_context_depth`), each producing 2/3 or 3/3 distinct renderings with round-trip
  preserved, and one (`variable_type_signature`) correctly rejected as inert.
- Recorded as `FM-026`, typed `SEARCH_SPACE_LIMITATION`.

**Neural microprobes.** A first checkpoint ran at 20 matched items against a frozen local
`gemma3:4b`, inference only. Dumb controls first: the best cheap heuristic reached 0.325
against a 0.25 chance level, under the 15pp veto threshold, so the benchmark is usable.
Accuracies were prior HML 0.450, Structured English 0.474, minimal machine 0.350 — all well
above chance, so the model is reading structure rather than guessing. The preregistered
sequential rule returned `CONTINUE` for both comparisons, which is the correct answer at
n=20 and is reported as such rather than as a ranking.

**Failures and unresolved uncertainty.** The open-endedness envelope is real and now
demonstrated in both directions: the loop can invent an axis that works, and it can invent one
that does nothing. `gemma3:4b` is small and roughly a third of its proposals are still
malformed. The targeted Lean campaign is still elaborating.

**Next intended step.** Finish the campaign, rebuild the corpus with the multi-goal states,
freeze `SEALED_FINAL_V2`, and run the search to convergence or budget.

## 2026-08-28 — a third instrument defect, and the loop running on real mathematics

**Branch:** `codex/open-ended-search-v2`
**Stage:** OPEN_ENDED_SEARCH_V2

**Objective.** Run the open-ended loop to a reportable state and acquire the corpus that makes
the unmeasurable axes measurable.

**A third defect in my own instruments.** Watching the live verdict stream, a child whose
target metric got 2.2% worse on dev and 2.1% worse on validation was labelled
`NON_GENERALIZING_MUTATION` and blocked from the elite population. Dev and validation agreed
almost exactly — there was no dev-set claim for validation to fail to reproduce. The gate's
job is specifically to catch improvements that exist only on dev; a candidate that failed on
both is a failed hypothesis and belongs to Pareto selection, which may still keep it for being
best on a different axis. Blocking it let the validation gate silently override the selector.
Fixed with a distinct `HYPOTHESIS_FAILED_CONSISTENTLY` verdict that is elite-eligible, with two
regression tests. Recorded as `FM-027`.

**The loop running.** Over its first four generations on the 608-transition corpus the search
accepted **eight invented axes**, taking the genome from 42 to 50 dimensions and the space from
4.095e19 to 3.582e23 points. It killed six candidates — two at compile, four at semantics —
and the model-driven backend proposed four distinct proposal types including
`CORPUS_ACQUISITION`, which is the loop noticing that the problem is the data rather than the
language.

**Corpus.** The targeted campaign elaborated 655 Lean files, 652 passing, covering 1,125
transitions selected for the strata the measured gaps named. Merging is in progress.

**Neural microprobes.** A second checkpoint at 40 matched items, frozen local `gemma3:4b`,
inference only: prior HML 0.368, Structured English 0.378, hybrid RPN 0.324, against a 0.25
chance level. The preregistered sequential rule has not eliminated any arm, which at this
sample size is the correct and uninteresting answer.

**Verification actually executed.**
- `PYTHONPATH=src python3 -m unittest discover -s tests` — **120 tests, all passing**.
- `scripts/search/build_frontier_v2.py` produces the frontier report from the live workspace.
- `scripts/search/emit_side_by_side_examples.py` renders 20 transitions across 9 arms for
  human audit.

**Failures and unresolved uncertainty.** `STRUCTURAL_CONVERGENCE = NO`: the search is running
against a generation budget, not to a stalled frontier. The strict front holds 28 of 62
evaluated candidates, so selection pressure at this stage is weak. Three instrument defects
have now been found by checking instruments against real renderings rather than trusting them;
that rate suggests more remain.

**Next intended step.** Finish the merge, freeze `SEALED_FINAL_V2`, and continue the search on
the enlarged corpus.
