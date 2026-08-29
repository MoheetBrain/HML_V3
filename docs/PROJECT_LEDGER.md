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

## 2026-08-28 — fourteen generations, the corpus gap closed, and two results that did not go my way

**Branch:** `codex/open-ended-search-v2`
**Stage:** OPEN_ENDED_SEARCH_V2

**The search.** 14 generations, 255 candidates registered, 201 evaluated, 14 killed. The
model-driven meta-designer proposed axes the genome did not have; thirteen bound to executable
projection hooks, passed the observable-effect gate, and grew the genome from 42 to 55 axes and
the space from 4.095e19 to 1.548e26 points.

**The corpus gap is closed.** `FM-020` recorded eleven `graph_serialization` mutations changing
the measurement zero times, because the corpus averaged 1.01 goals per state. Scanning 250,814
LeanDojo transitions and elaborating 1,125 targeted ones raised the multi-goal share from 1.2%
to 18.1% and the maximum from 2 goals to 12. On multi-goal states `graph_serialization` now
separates into three distinct rendering groups, and `REORDER_GOAL_FOCUS`, `SWAP_GOAL_IDENTITY`
and `CHANGE_SCOPE_PARENT` went from 3% applicable to 100%. The axis was never uninformative;
the corpus could not ask the question. Recorded as `FM-028`.

**`SEALED_FINAL_V2` frozen and unread.** 232 transitions across 126 families, all acquired
after the V1 search, so none influenced the V1 frontier. It lives in its own file behind the
isolated evaluator process. V1's split is retired as `HISTORICAL_SEALED_V1`.

**Two results that did not go my way, both recorded.**

`FM-029` — the semantic corruption metric I built to replace V1's biased text-level suite is
itself **saturated**: it read exactly 1.000 for all 201 evaluated candidates and contributed
nothing to selection. The architecture is right — corrupt the canonical state once, upstream of
every candidate — but the predicate was "does the rendering change", and every representation
of a changed state renders differently. Fixing the bias produced a saturated instrument, which
is the `FM-010`/`FM-019` pattern for a third time. The predicate needs to be
recoverability-based: does the candidate's own reader detect a violated invariant from the
rendering alone.

`FM-030` — thirteen invented axes were accepted, five were exercised by a candidate that
survived to evaluation, sixteen candidates carried one, and **none of the six finalists uses
one**. The open-ended machinery demonstrably works; on these selection axes and this corpus it
has not yet paid. Three untested explanations are recorded rather than one asserted.

**Verification actually executed.**
- `PYTHONPATH=src python3 -m unittest discover -s tests` — **120 tests, all passing**.
- Corpus merge: base 608 + targeted 542 = 1,150 transitions, content SHA-256
  `950cb040af8c14da…`; mean goals 1.369, max 12, multi-goal 22.4%.
- `create_sealed_v2.py`: 232 sealed / 918 search transitions, 126 sealed families all from
  post-V1 acquisition.
- `build_frontier_v2.py` and `emit_side_by_side_examples.py`: 6 finalists, 20 transitions
  rendered across 9 arms.

**Failures and unresolved uncertainty.** `STRUCTURAL_CONVERGENCE = NO`: the run stopped on its
generation budget. The strict front holds 49 of 201 candidates, so selection pressure is still
weak. Three selection-adjacent metrics are saturated and must be removed before the next run.
The 14-generation search ran on the 608-transition corpus; the enlarged 1,150-transition corpus
and `SEALED_FINAL_V2` are built but a search has not yet been run on them.

**Next intended step.** Remove the saturated axes, re-run on the enlarged corpus where goal
ordering is measurable, and only then consider reading `SEALED_FINAL_V2`.

## 2026-08-29 — Saturated metrics removed, a second meta-designer, and the search run to structural convergence

**Branch:** `codex/open-ended-search-v2`  **Stage:** `OPEN_ENDED_SEARCH_V2_CONVERGED`

**Objective.** Remove saturated and non-discriminative metrics from selection; add Qwen as a
second zero-cost MetaDesigner; register PRM800K as DiscoveryGraph evidence and GSM8K as
natural-language math evidence, neither as Lean truth; restart the open-ended search from
generation 0 on the 918-transition pool and run it to structural convergence rather than to a
generation budget; leave `SEALED_FINAL_V2` untouched.

**Selection.** `semantic_detect_rate` is out. Measured across all 201 candidates of the prior
run it read exactly 1.000, and it reads 1.000 on all sixteen generation-zero seeds of this one
(`FM-029`). Rather than edit the tuple again — the third time this has been done by hand —
`enforce_discrimination()` now runs every generation and demotes any selection axis with zero
spread, recording the measurement. Replayed against the prior run's own registry it reproduces
FM-029 mechanically. Near-saturation is reported but never demoted on: on the new pool the same
metric reads 0.9899–1.0, which the strict rule correctly does not fire on. `detect_drop_field`
takes the freed slot so selection retains an error-detection dimension rather than becoming
five axes that are all minimised (`D-018`).

**Second meta-designer.** `qwen38-rvn` (27B, local, inference only) alongside `gemma3:4b`. Two
defects had to be fixed first, both of which produced zero proposals rather than an error
(`FM-032`): the transport posted to `/api/generate`, which bypasses the chat template and made
Qwen return a single token and an empty string on every prompt — invisible while there was one
backend — and on `/api/chat` the model spent its whole 4096-token budget inside `<think>`.
With an empty-think prefill it returns valid proposals in ~60s.

**Evidence roles.** Registry schema 1.1.0 adds `evidence_role` and `not_lean_truth`. PRM800K is
`DISCOVERY_GRAPH_EVIDENCE`; GSM8K was acquired at pinned commit `3101c7d5` (MIT, 8,792 rows,
per-file SHA-256s) and is `NATURAL_LANGUAGE_MATH_EVIDENCE`. `not_lean_truth` is derived from
`formal_system`, never asserted, and a test refuses any dataset carrying it the role
`LEAN_FORMAL_TRUTH` or a trust tier of A or B (`D-021`).

**A defect caught before the run.** The controller sampled dev, microtest and mutation sets as
prefixes. On the new pool no prefix up to 128 rows contains a state with more than four goals,
and the twelve-row mutation sample was 8.3% multi-goal — near the corpus it replaced. The
search would have re-derived `FM-020` on the corpus acquired to fix it. Replaced with
deterministic stratified sampling; every sample now reaches six or more goals (`FM-031`,
`D-019`).

**A defect caught during the run, which cost a restart.** Fifteen generations in, nine of
thirty accepted axes were `neighbourhood_capsule` over `NONE/GOAL_LOCAL/ACTION_LOCAL` under
nine different names. Measured directly: two such axes render identically and stacking them is
idempotent. They inflated the reported space by 3^8 with no new reachable rendering, filled the
front with candidates differing by id and not by output, and made convergence unreachable,
since a fresh *name* is always available. Acceptance now requires the axis's set of renderings
to differ from every active axis (`FM-033`, `D-022`). The run was restarted from generation 0.

**The run.** 106 generations, 5h03m, three backends, converged — frontier position, frontier
membership and genome size all unchanged for five consecutive generations. 566 candidates
registered, 531 evaluated, 33 killed. Of 289 axis proposals, 5 were new dimensions, 205 were
behavioural duplicates and 79 unimplementable. All sixteen hand-specified seeds were pushed off
the strict Pareto front. Frontier minima improved 20.5% on tokens and 18–24% on the three
locality axes between generations 0 and 60, then held.

**A result that reversed a recorded negative.** `FM-030` reported that no invented axis had
ever reached the frontier. Two of the seven finalists now carry one, both values of
`dependency_capsule`: the `GOAL_LOCAL` variant is cheapest under all four tokenizer
vocabularies, and the `ACTION_LOCAL` variant reaches 11.84 dependency-query token distance
against ~27.8 for the rest. It is the same axis the backends re-proposed 205 times under fresh
names; registering it once and blocking the aliases is what let it be judged (`FM-034`).

**A judgement I got wrong, and corrected.** At generation 70 the frontier position had been
frozen for ten generations but membership was churning at 2.3 entrants per generation with no
visible trend. I read that as unsatisfiable-by-construction, recommended replacing the clause
with shortlist stability, and drafted the change. It was wrong: churn kept falling, generations
101–105 had no entrant and no departure, and the run converged on the original criterion. The
replacement was reverted unused (`FM-035`).

**Verification actually executed.**
- `.venv/bin/python -m pytest` — **158 tests, 338 subtests, all passing** (was 120 at the start
  of this session). The repository ships no `.venv` and the system interpreter has no pytest, so
  the previously quoted `python3 -m pytest` printed `No module named pytest` and exited 0.
- `scripts/search/build_frontier_v2.py` — 7 finalists, 5 invented axes accepted.
- `scripts/search/validate_frontier.py` — 5 of 7 axis leaders keep their lead on the validation
  split selection never read.
- `scripts/search/verify_reproducibility.py` — 60 candidates including 10 invented-axis
  carriers re-render byte-identically in a fresh subprocess under a different PYTHONHASHSEED;
  **0 mismatches**. This required fixing the verifier itself: it built compilers from the
  genome alone, with no invented axes, and keyed the child's results by the genome id rather
  than the record id, so it reported its own blind spot as "NOT REPRODUCIBLE: 2 candidates
  differ" (`FM-036`).
- Registry reload after the change: `PrimitiveRegistry` crashed on `ACCEPTED_DUPLICATE` rows
  because the loader enumerated rejection statuses instead of testing positively for a
  primitive. That broke resume, not the running search, and was found by a report script.

**Failures and unresolved uncertainty.** The prior run's headline space figure (42 → 55 axes,
1.548e26 points) counted duplicate axes as new dimensions and should not be repeated without
re-measurement. Two of seven axis leaders do not keep their lead on validation. No model
evidence exists; every result here is static. The meta-designer brief's worked example is
`dependency_capsule`, which is what the backends copied 205 times — harmless now, but the brief
was deliberately left unchanged rather than edited mid-project.

**Effect on the project.** The representation search has, for the first time, converged rather
than stopped on a budget, on a corpus where locality is measurable, with an instrument set
whose saturated members are excluded by measurement rather than by hand.

**Next intended step.** Decide whether to read `SEALED_FINAL_V2`. The precondition its policy
names is met — convergence reached, zero prior reads — but reading it is irreversible and has
not been authorised, so it remains unread.

## 2026-08-29 — The permanent goal is written down, and MicroMath Lab V1 is built

**Branch:** `codex/open-ended-search-v2`  **Stage:** `MICROMATH_LAB_V1`

**Objective.** Record the project's permanent objective so it cannot drift, and replace the
multi-hour global search as the default experiment with a cheap surgical diagnostic that
finds *which structure* a representation handles badly before any broad search is run.

**`PROJECT_GOAL.md`.** Written verbatim from the user's statement and pinned by
`tests/test_project_goal.py`, which requires the one-sentence goal, the falsification section
and the "what does not count as success" list to survive intact, and requires `README.md` to
point at it. That last section matters most here: it names a converged search, an improving
metric and beating one weak control as things that are *not* success, and this repository has
recently produced all three.

**Checkpoint.** `hml-v3-pre-micromath-2026-08-29` tags the converged 106-generation search and
is pushed, so that result is recoverable exactly regardless of what follows.

**MicroMath Lab V1.** 45 matched pairs / 90 states over 45 of 48 domain x structural-stress
cells, from 45 distinct base states drawn from the 862 transitions the converged search never
measured on. `SEALED_FINAL_V2` was not opened, and a path guard refuses it.

Every counterfactual is a **transposition**: B is a permutation of A, so the canonical token
multiset is identical by construction rather than by hope. Measured, the best dumb rule scores
**0.509 against 0.500 chance**, per stress and per candidate, across all eleven
representations.

**Five defects found in this project's own instruments while building it**, each by measuring
rather than assuming:

- `FM-037` — PREMISE and ACTION_ARGUMENT were built on list *order*, which
  `projection.semantic_core` stores `sorted()`. All eleven representations "failed" those
  twelve cells. It read as a universal representation weakness and was a benchmark bug; both
  stresses were rebuilt on set membership.
- `FM-038` — the shortcut audit was aggregate-only and reported 0.62 against a 0.65 limit.
  Split by stress, MULTI_GOAL and PREMISE both scored **1.000** for "pick whichever option
  appears earlier". Six sound cells were diluting two broken ones.
- `FM-039` — the audit counted raw canonical ids while renderings write codec-encoded ones, so
  both counts were zero, every item scored undecided, and it returned a spotless 0.509 having
  examined nothing.
- `FM-040` — ranking base states by structural richness produced a median item of 16,158
  pre-tokens that no local model could read; adding a size budget then collapsed 45 cells onto
  17 base states, nine spanning two splits, so MICRO_HIDDEN shared mathematics with MICRO_DEV.
- A strided char-n-gram feature that reported a difference on every sound pair and would have
  condemned a valid benchmark.

**Three cells cannot be populated and are recorded as acquisition requests, not guesses.**
LinearAlgebra has zero multi-goal states in the entire non-sealed pool and Geometry has no
state whose two goals hold different scopes.

**Verification actually executed.**
- `.venv/bin/python -m pytest` — **187 tests, 338 subtests, all passing** (158 before this
  stage). Includes mutation tests that require the lab to catch a representation which hides
  the relation, and to fail a benchmark that leaks the answer.
- `scripts/micromath/build_lab_v1.py` — 45 pairs, 45 distinct base states, all 8 stresses
  present in each of MICRO_DEV / MICRO_SHADOW / MICRO_HIDDEN.
- `scripts/micromath/audit_lab_v1.py` — SHORTCUT_AUDIT **PASS** for all 11 representations;
  deterministic Level A reports 29/29 expressible for every one, which is **SATURATED** and
  therefore cannot guide selection.

**Failures and unresolved uncertainty.** The Level A deterministic layer is saturated: every
representation expresses every relation, so it works as a gate and not as a discriminator.
The first neural probe (`gemma3:4b`) is scoring 0.40-0.60 across all eleven representations
including controls, which is chance; if that holds it is an INSTRUMENT_LIMIT of a 4B reader
rather than a result about any representation, and the second model becomes necessary rather
than confirmatory. No targeted mutation cycle has been run yet.

**Next intended step.** Finish the two-model probe, produce the first heatmap and failure
gradient, and run the targeted surgical cycles. `MICRO_HIDDEN` stays unread until local
optimisation stabilises; `SEALED_FINAL_V2` stays unread.

---

## 2026-08-29 — Component certification: 0 of 8 certified, and 6 of 8 instruments were broken

**Branch.** `codex/open-ended-search-v2`.
**Stage.** `MICROMATH_LAB_V1` → `MICROMATH_LAB_V1_CERTIFIED`.

**Objective.** Run `COMPONENT_CERTIFICATION_V1`: certify each structural component against
positive and negative control arms before drawing any conclusion about the language, so that
`INSTRUMENT_LIMIT` can be separated from `LANGUAGE_WEAKNESS`. Then close out MicroMath Lab V1.

**Files and systems changed.** `scripts/micromath/run_component_certification.py` (new, plus an
`FM-043` fix); `scripts/micromath/run_targeted_search.py`, `src/hml_v3/micromath/calibration.py`,
`src/hml_v3/micromath/targeted_search.py` (new, previously uncommitted); eight reports under
`reports/micromath_lab_v1/`; `DECISIONS.md` (`D-023`);
`research/representation_search/hml_failure_memory.json` (`FM-041`, `FM-042`, `FM-043`);
`tests/test_micromath_lab.py`; `docs/PROJECT_STATUS.md`.

**What was completed.** All eight components certified on `qwen38-rvn:latest` — 8 components x
4 arms x 12 pairs = 768 probe items, 8190 s, £0 incremental. **Zero components certified.**

- **Two valid instruments, both CONTROL_PARITY.** MULTI_GOAL: positive 0.958, negative 0.500,
  candidate = best control = 0.583, normalised readability **0.182**. EXPRESSION_DEPTH: positive
  0.917, negative 0.458, candidate = best control = 0.500, normalised readability **0.091**.
  0.375 and 0.417 of dynamic range are reached by no representation, discovered or hand-written.
- **Four INSTRUMENT_INVALID** — DEPENDENCY, SCOPE, TYPE, PREMISE, negative arms 0.79–0.88. The
  question is answerable with the relation destroyed.
- **Two INSTRUMENT_LIMIT** — BINDER (range 0.167) and ACTION_ARGUMENT (positive arm 0.542).

**Decisions made and why.** `D-023`: a component is judged only through an instrument proved to
work, with thresholds preregistered before the run. Adopted because the alternative — the
practice in force until this run — produced three hours of measurements of which 76 % were not
measurements. Two consequences were accepted explicitly: results taken before calibration are
*withdrawn* rather than reinterpreted, and a rejection on an invalid instrument is `VOID`
rather than `REFUTED`.

**Tests and verification actually executed.**
- `.venv/bin/python -m pytest` — **192 tests, 338 subtests, all passing** (187 before). Five new:
  four pin the `D-023` verdicts against the arms actually measured, one pins the `FM-043` leak.
- `scripts/micromath/run_component_certification.py` — completed all 8 components, 8190 s;
  output `reports/micromath_lab_v1/COMPONENT_CERTIFICATION.json`.
- Recomputation of `PROBE_micro_dev_qwen38-rvn_latest.json` against the certification: the
  candidate's reported 0.741 decomposes to **0.500 on 14 calibrated-valid items** and 0.818 on
  44 invalid or limited ones; 75.9 % of the items came from broken instruments.
- Replay of `build_targeted_suite` with the run's own arguments, intersecting
  `base_transition_id` against the reserved splits: **8 of 8 `micro_hidden` and 8 of 8
  `micro_shadow` base states consumed.** After the fix, re-verified: **0 overlap, and every
  component still reaches 12 pairs.**

**Results.** The mission asked which component is weakest. The answer is that six of the eight
test rigs were broken, and on the two that work the discovered representation performs exactly
as well as a plain typed AST, both at under a fifth of the achievable range. The seven
previously rejected mutations split five interpretable (`WRONG_CAUSAL_HYPOTHESIS` — surface
syntax does not move structural readability; five hypotheses moved a combined 0.031) and two
void.

**Failures and unresolved uncertainty.**
- `FM-041` — transposition equalises the token multiset but not semantic plausibility. The
  per-stress shortcut audit is clean (0.509 aggregate, 0.5625 worst cell) and four instruments
  were still invalid, because the answer stays recoverable from the identifiers. A surface
  control is necessary and not sufficient.
- `FM-042` — three hours of probing, one failure gradient and seven mutation evaluations ran
  uncalibrated. The gradient's top and third picks were valid, its second was not, and its flat
  Δ +0.000 tail across five cells was absence of measurement read as parity.
- `FM-043` — **my defect, found by checking rather than assuming.** The certification topped each
  component up from the shared pool with an exclusion set covering `micro_dev` only, and spent
  both holdout splits. I asserted in a draft of the dataset card and final report that they were
  untouched; I withdrew that after intersecting the identifiers. Nothing was fitted on them and
  no verdict depends on them, but neither can support a generalisation claim. The existing
  hidden-split guard missed it because it checks the split *name* a script is given, not the
  base states a run consumes.
- Not attempted, stated plainly: §16 `PREMISE_V2`, §17–19 the E/D/G ladders, §21–22 the
  integration matrix, §23 the reasoning ladder.
- Google Cloud was not used. `compute.instances.list`/`.get` worked earlier in the session and
  then returned 403; `h3` had already been stopped and could not be restarted, and the `a100`
  the user started could not be seen or reached. Stopping `h3` before verifying I could start it
  was my error. All work ran locally at zero incremental cost.

**Effect on the overall project.** `PROJECT_GOAL.md` §18 names as falsifying evidence the
absence of a measurable readability advantage over existing notations. On every instrument that
survives calibration, there is no such advantage. This does not settle the question — two
components, 12 pairs each — but it is the strongest negative evidence to date, and it redirects
the project from searching to instrument repair.

**Next intended step.** Repair the four invalid instruments so the answer is not recoverable
from identifiers, re-run calibration until their negative arms return to chance, mint a fresh
holdout to replace the two that are spent, and only then resume mutation cycles — against
structural rather than surface hypotheses. No global search until a component is certified.
`SEALED_FINAL_V2` and `TARGET_HOLDOUT` stay unread.

---

## 2026-08-29 — Instrument repair V2: a firewall, a free guard, and one component withdrawn

**Branch.** `codex/open-ended-search-v2`.
**Stage.** `MICROMATH_LAB_V1_CERTIFIED` → `INSTRUMENT_REPAIR_V2`.

**Objective.** Execute `COMPONENT_CERTIFICATION_V2`: repair the six instruments V1 showed to
be broken or beyond the reader, mint fresh splits behind a firewall that a wrong split name
cannot bypass, and stage architectural rather than cosmetic hypotheses for the components
whose instruments work.

**Files and systems changed.** New: `src/hml_v3/micromath/{firewall,anonymise,ablate,
calibration_v2,instruments_v2,probe_v2,shortcut_v2,architectures,ladders}.py`;
`scripts/micromath/{build_lab_v2,run_certification_v2,run_known_bad_v2,run_architectures_v2,
build_dashboard_v2}.py`; `tests/test_micromath_v2.py`; `data/micromath_lab_v2/`. Modified:
`DECISIONS.md` (`D-024`), `research/representation_search/hml_failure_memory.json`
(`FM-044`–`FM-046`), `docs/PROJECT_STATUS.md`.

**What was completed.** MicroMath Lab V2: 611 items over seven stresses, split
300 / 135 / 176 across dev, shadow and hidden with **zero base-state overlap**, built from
1051 base states after retiring the 43 the V1 certification spent. 238 of 300 dev items are
four-choice with same-family distractors drawn from the same state. Negative controls are now
state-level ablations that destroy the target relation by derangement, so the token multiset
survives and the relation does not.

**Decisions made and why.** `D-024`: the shortcut audit is a hard gate that runs before any
inference. Calibration cannot see a question answerable without reading anything, and the
first V2 build proved it — 43 of 43 MULTI_GOAL items had the answer `g1`, and it cost 277
seconds of Qwen inference to notice what counting answers says instantly.

**Tests and verification actually executed.**
- `.venv/bin/python -m pytest` — **239 tests, 338 subtests, all passing** (192 before).
- `scripts/micromath/build_lab_v2.py` — 611 items, 0 base-state overlap between splits.
- Shortcut audit over all three splits — **21 of 21 cells CLEAN** against seven key-free
  rules judged by Bonferroni-corrected exact binomial bounds.
- V2 certification in flight; `EXPLICIT_POSITIVE` reached 12/12 on the withdrawn MULTI_GOAL
  and 10/12 on EXPRESSION_DEPTH at chance 0.304.
- Verified against `projection.py` that no axis renders the action-to-goal relation.

**Failures and unresolved uncertainty.**
- `FM-044` — **a correction to what I reported to the user.** I called V1's MULTI_GOAL result
  the most important number the project had produced: 0.958 positive, 0.500 negative,
  candidate and control both 0.583, leaving 0.375 of headroom. It is not headroom. The
  relation is absent from the projection — the action section never names a goal, and the
  delta section names goals in a `_uniq.*` namespace the codec leaves unmapped. Both
  representations sat near chance because neither could answer. MULTI_GOAL is withdrawn.
- `FM-045` — one seed drove both the content choice and the option ordering, making them
  perfectly correlated; on two-goal SCOPE items the answer landed first every time and
  "always take the first option" scored 1.000.
- `FM-046` — the audit shipped with two defects of its own: it re-sorted the options the
  model is shown, and used a flat tolerance that made its verdict a function of sample size,
  so one construction came out CLEAN on one split and LEAKS on another. A third defect,
  measuring constant answers as distinct-over-total, would have condemned every cell with a
  small option vocabulary at scale; all three are fixed and pinned by tests.
- SCOPE was gated out of this certification run by that third defect before it was found. It
  passes the corrected audit and will be run separately; the results file now merges.
- The pre-registered ladders are largely unpopulated on this corpus — G5 and D1–D2 are empty.
  The boundaries are kept as written and the emptiness reported.

**Effect on the overall project.** The binding constraint has moved. After V1 it looked like
the representation was the problem; the V2 work says the instruments were, and that one of the
two components V1 called valid was measuring a relation no representation carries. What
remains testable is EXPRESSION_DEPTH and five repaired components. The long-horizon
prediction in `PROJECT_GOAL` §18 cannot be tested on this corpus, which makes corpus depth —
not notation — the next real obstacle.

**Next intended step.** Finish certification, add SCOPE, run known-bad detection, run the
eight architectural hypotheses through the kill-early funnel, and publish the dashboard.

---

## 2026-08-29 (later) — Four construction defects, and a positive control that was not one

**Branch.** `codex/open-ended-search-v2`. **Stage.** `INSTRUMENT_REPAIR_V2` (continuing).

**Objective.** Get a V2 certification run whose arms mean what they claim, after the first
three attempts each surfaced a defect that would have made the numbers uninterpretable.

**Files and systems changed.** `src/hml_v3/micromath/{instruments_v2,shortcut_v2,probe_v2,
ladders}.py`; `tests/test_micromath_v2.py`; `research/representation_search/
hml_failure_memory.json` (`FM-047`, `FM-048`); `docs/PROJECT_STATUS.md`.

**What was completed.** Four defects found and fixed, three of them in my own guards rather
than in the lab:

1. `FM-045` — one seed drove two decisions and correlated them perfectly; the answer landed
   first on every two-goal SCOPE item.
2. `FM-046` — the shortcut audit re-sorted the options the model actually sees, used a flat
   tolerance that made its verdict a function of n, and measured constant answers in a way
   that would have condemned every small-vocabulary cell at scale.
3. `FM-047` — EXPRESSION_DEPTH was ill-posed. "Which reference sits deepest" has no single
   answer when one identity occurs at depths 11, 9, 9 and 8. It **passed the pre-registered
   calibration rule** and returned `INSTRUMENT_VALID` with `CONTROL_PARITY` at a normalised
   readability of 0.000 — which reads as "both representations are maximally unreadable".
4. `FM-048` — the positive control was prepended to the top of a 7000-character rendering and
   the reader ignored it, scoring 0.417 against chance 0.304 while being handed the answer.

**Decisions made and why.** EXPRESSION_DEPTH now requires a **strictly unique deepest**
reference. A two-level margin would have been safer but costs 88% of the corpus (7.6% of
states qualify against 62.8%); that is a difficulty preference dressed as a correctness rule,
so the lead size is recorded per item and used to stratify difficulty instead. The positive
control is now placed **beside the question** rather than at the top of the document, which is
the remedy `MISSION §25` names explicitly.

**Tests and verification actually executed.**
- `.venv/bin/python -m pytest` — **243 tests, 338 subtests, all passing** (239 before).
- Direct inspection of one raw completion: header `DEEPEST_REFERENCE = bv91`, reply `bv11`.
- Positive arm after the fix: **4/4 on EXPRESSION_DEPTH, TYPE and BINDER**.
- Shortcut audit after every rebuild: **21 of 21 cells CLEAN** across all three splits,
  SCOPE included once its measure was corrected.
- Lab rebuilt: 611 items, 301/135/175, base-state overlap 0.

**Failures and unresolved uncertainty.**
- `FM-047` and `FM-048` were both caught by a number looking wrong, not by a test. Three arms
  at exactly 0/12, and a positive arm at 0.417 while being told the answer. Neither the
  calibration rule nor the shortcut audit could see either, and I have added a reading-time
  check for the first and a placement fix for the second, but the general lesson is that
  automated guards did not substitute for looking at one raw completion.
- **Every V1 dynamic range is understated** because V1 used the same distant-header positive
  control. The V1 verdicts of INSTRUMENT_INVALID stand — those turned on negative arms, not
  positive ones — but the V1 normalised-readability figures should not be compared with V2.
- Four restarts of the certification run. Each was the right call and each cost roughly
  twenty minutes of local inference, at zero incremental spend.

**Effect on the overall project.** No component has completed V2 certification yet. What has
changed is that the instruments now have a demonstrated ceiling, a state-level floor, a clean
construction audit and a firewall — so when the numbers arrive they will mean something.

**Next intended step.** Complete the seven-component run, then known-bad detection and the
eight architectural hypotheses, then the dashboard and the mission report.

---

## 2026-08-29 (later still) — V2 certification completes and overturns the V1 conclusion

**Branch.** `codex/open-ended-search-v2`. **Stage.** `INSTRUMENT_REPAIR_V2` →
`COMPONENT_CERTIFICATION_V2`.

**Objective.** Run the V2 certification to completion on repaired instruments.

**Files and systems changed.** `src/hml_v3/micromath/{ablate,calibration_v2}.py`;
`scripts/micromath/{run_certification_v2,run_architectures_v2,resolve_unseparated_v2,
reablate_v2,build_final_report_v2}.py`; `tests/test_micromath_v2.py`;
`research/representation_search/hml_failure_memory.json` (`FM-049`, `FM-050`);
`reports/micromath_lab_v2/`; `docs/PROJECT_STATUS.md`.

**What was completed.** Seven components certified in 3975 s. **Six of seven instruments
valid**, against two of eight in V1.

**Results.** ACTION_ARGUMENT 0.900 readability, TYPE 0.875, PREMISE 0.833, SCOPE 0.625,
DEPENDENCY 0.444, EXPRESSION_DEPTH 0.091. Five of six are `CONTROL_PARITY`, four exact ties.

**Decisions made and why.** `FM-049`: the ladder now escalates when the *comparison* is
unresolved, not only the instrument — DEPENDENCY's +0.167 with an interval touching zero is
exactly what `§9` reserves items for. Disclosed plainly: that change was made after seeing a
result favourable to the candidate, no threshold moved, and it completes a ladder the mission
already required.

**Tests and verification actually executed.**
- `.venv/bin/python -m pytest` — **246 tests, 338 subtests, all passing**.
- `run_certification_v2.py` — 7 components, 4 arms, 12 items each, 3975 s, zero spend.
- `reablate_v2.py --stresses BINDER` — 96 items rewritten in place, 0 lost, splits untouched.
- Shortcut audit before every run — 21 of 21 cells CLEAN.

**Failures and unresolved uncertainty.**
- **The V1 conclusion is overturned and I reported it wrongly at the time.** I described V1's
  result as the language reading at under a fifth of the achievable range on the only two
  valid instruments. Four of the relations V1 called unmeasurable are read at 0.83–0.90 by
  *both* representations once identifiers are anonymised and the negative control moved into
  the state. The instruments were the problem, not the representation.
- `FM-050` — BINDER is `INSTRUMENT_INVALID` through my defect: the question was changed to
  remove a counting task and the ablation was not re-derived, so a derangement permuted
  within the set the question asked about. Negative arm 0.750 against chance 0.277.
- DEPENDENCY's +0.167 is **unresolved**, not a result. Interval [+0.000, +0.333].
- Every figure rests on 12 items, and nothing has been reproduced on shadow or holdout.
- **No component is CERTIFIED.** `§29` requires known-bad detection and reproduction; neither
  has completed.
- Defects found this session: seven, all in my own instruments and guards, none in the
  language. That ratio is the honest summary of the work.

**Effect on the overall project.** The diagnostic now has range: it separates a relation read
at 0.900 from one read at 0.091, where V1 returned a flat near-chance verdict on everything.
Expression depth is isolated as the single genuine structural weakness, and it is what the
architectural hypotheses target.

**Next intended step.** Known-bad detection, the eight architectures, the DEPENDENCY re-run at
higher n, then the dashboard and final report.
