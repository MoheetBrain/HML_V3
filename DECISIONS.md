# Decisions

Decisions are additive. Superseded decisions remain in this file with their status changed;
they are not deleted.

## D-001 — Representation is the dependent variable

**Status:** ACTIVE

Canonical mathematical state and verifier outcomes are held fixed while renderers vary.
No representation is named the final HML V3 language during the foundation milestone.

## D-002 — Raw source observations remain authoritative

**Status:** ACTIVE

Lean pretty-printed states, tactics, source locations, versions, and verifier evidence are
preserved verbatim. Parsed canonical fields are an adapter output, not a replacement for the
source observation.

## D-003 — Trust tier is not verification status

**Status:** ACTIVE

A source can be formally structured yet only trace-recorded, or naturally written yet later
verified. Registry entries therefore carry both `trust_tier` and `verification_status`.

## D-004 — External payloads stay external by default

**Status:** ACTIVE

Large datasets and repositories are referenced by immutable source identity, size, hash when
feasible, license, and reproducible acquisition method. Small samples may be committed when
their license permits it and their provenance is complete.

## D-005 — Prior HML is one candidate renderer

**Status:** ACTIVE

Previous HML contributes semantic design ideas, regression artifacts, and an empirical
baseline. Its syntax and ontology do not define the canonical IR.

## D-006 — Exact raw Lean state outranks the prior structured projection

**Status:** ACTIVE

The old derived `hypotheses` and `target` fields disagree with conservative raw-state
decomposition on 659 of 2,000 V1 observations, primarily because multiline constructs were
truncated or misparsed. V3 preserves those disagreements but derives displayed goals and
contexts from the exact raw state.

## D-007 — Premises come from the official annotated tactic

**Status:** ACTIVE

Every one of the 241,265 prior derived records has an empty `premises_used` list. V3 joins
selected rows back to the pinned LeanDojo Benchmark 4 trace and accepts premise identities
only after exact tactic/before/after equality. Local-context dependencies remain an explicit
gap.

## D-008 — Formal trace and fresh replay are distinct verdicts

**Status:** ACTIVE

All V1 rows are accepted trace transitions from the pinned formal corpus. Only the 32 rows
whose Stage100 certificates reached and exactly matched the transition are labelled
`FRESH_REPLAY_PASS`; no other row inherits that label.

## D-009 — The initial representation family has no winner

**Status:** ACTIVE

All ten required candidate families are implemented and semantically parity-checked. Byte
length and whitespace counts are descriptive diagnostics, not a selection criterion. Model
experiments wait for stronger, shortcut-resistant tasks.

## D-010 — The language is data, and there is exactly one compiler

**Status:** ACTIVE

A candidate representation is a `RepresentationGenome` — a point in a 42-axis discrete space
— consumed by one generic compiler. No candidate has renderer code of its own. Two
candidates therefore cannot differ by an implementation accident, and any candidate is
reproducible from `(genome_sha256, compiler_version, canonical_state_version)`. The candidate
id is the first twelve hex digits of the genome hash.

This supersedes the V1 practice of writing one renderer class per candidate. Those ten V1
renderers remain as historical artifacts; they wrapped the same canonical JSON in different
headers and could not vary structure, ordering, identity or notation independently.

## D-011 — The declared semantic contract is `projection.semantic_core`

**Status:** ACTIVE

A candidate claims losslessness against goals with identities, targets as elaborated
expression trees, local contexts with identity/binder role/declaration role/type/value, focus
order, relevant metavariables, and the action's identity with its premise and local
references. Lean's display spelling, content hashes, environment provenance and corpus
bookkeeping are outside it, consistent with `D-002` and `D-009`.

A genome that hides contract content fails the round-trip gate and is never scored. That is
what stops compression buying its way past a semantic loss.

## D-012 — Local-context order is stated once, layout is free

**Status:** ACTIVE

Lean's local-context order is semantic: a declaration may only mention earlier free
variables. A representation may therefore permute *record layout* for locality, but the
goal's `context` field always states canonical declaration order. Reordering is presentation;
discarding the order is a semantic loss.

## D-013 — Corruption detection is reported per family, never averaged before selection

**Status:** ACTIVE

`FM-007` recorded a candidate that scored 0.800 overall while being completely blind
(`0.000`) to record-order corruption. A mean would have hidden that. Six mutation families
are measured separately and reported separately.

## D-014 — A saturated instrument is excluded from selection and said to be saturated

**Status:** ACTIVE

`detect_corrupt_identity` read `1.000` for all sixteen generation-zero seeds on the real V2
corpus. Following `FM-010`, it is measured, reported as non-discriminative, and removed from
the Pareto axes; `detect_drop_field` replaced it. The decision was made before the search
began, so every candidate is compared on the same axes.

## D-015 — The corpus is split by Mathlib source file and the final split is sealed

**Status:** ACTIVE

Sibling lemmas in one file share notation, instances and premise vocabulary, so a
transition-level or theorem-level split leaks. Assignment is a keyed SHA-256 of the file
path, reproducible from the corpus alone. The sealed 20% is reachable only through
`SealedEvaluator`, which returns aggregates and logs every access.

## D-016 — Token counts are named with their vocabulary

**Status:** ACTIVE

Under the pinned GPT-2 byte-level BPE, `⊢` costs 3 tokens, `ℝ` 3, `𝕜` 3. The prior
tokenization audit measured all of them at 1 token under Qwen3-8B. `FM-004`'s escaping
penalty reproduces under both vocabularies — escaping costs 2.3x–2.7x under GPT-2 — but the
absolute counts do not. Every token claim names its vocabulary, and byte counts plus
tokenizer-free pre-tokens are reported beside every token count.

## D-017 — The V2 corpus is size-bounded and the exclusions are counted

**Status:** ACTIVE

Lean's accumulated metavariable inventory is quadratic in some proofs: four of the campaign's
250 raw documents are between 6.8 GiB and 24 GiB, and one was truncated when the original
driver died. The corpus builder streams each document, excludes any transition whose
canonical form exceeds a declared 256 KiB budget, and counts every exclusion by reason. 317
of 500 selected transitions were recovered; the other 183 are accounted for in
`reports/audits/LEAN_RUNTIME_V2_CORPUS.md` rather than quietly dropped.

## D-018 — A saturated instrument is removed from selection by measurement, not by hand

**Status:** ACTIVE

`FM-010`, `FM-019` and `FM-029` are the same defect three times: a metric that read the same
value on every candidate, entered selection, and was caught only by reading a finished run.
Each was then corrected by editing the axis tuple by hand.

Selection now runs `enforce_discrimination()` every generation. Any selection axis whose
spread across the evaluated population is zero is demoted to diagnostic, with the measured
spread recorded on the generation report and in the search state. Demotion is one-way — an
axis is never restored because a wider population finally moved it by a rounding error — and
it will not reduce selection below three axes, because `FM-008` forbids collapsing toward a
single objective.

`semantic_detect_rate` is removed from the preregistered vector on this evidence: 1.000 on
all 201 candidates of the first V2 run, and 1.000 on all 16 generation-zero seeds of the
second. `detect_corrupt_identity` stays out for the same reason. Both are still measured and
still reported; neither selects.

`detect_drop_field` takes the freed slot. Without it the vector is five axes that are all
minimised, with nothing in selection rewarding the preservation of information; it is the
detection family with real spread on the same population (0.000–0.750, twelve distinct
values, coefficient of variation 1.506).

## D-019 — Samples are stratified by structure, never taken as prefixes

**Status:** ACTIVE

`FM-028` recorded that targeted acquisition closed the measurability gap `FM-020` named: the
V2 search pool reaches twelve goals per state and is 19.0% multi-goal, against 1.01 mean
goals and 1.2% before.

The controller then sampled dev, microtest and mutation sets as prefixes of a list sorted by
transition id. Measured on that pool, no prefix up to 128 rows contains a state with more
than four goals, `dev[:28]` caps at three, and the twelve-row mutation sample is 8.3%
multi-goal — near the corpus it replaced. Acquiring the structure and never sampling it is
indistinguishable from never acquiring it.

`representation_search.sampling.structural_sample` allocates by goal-count stratum,
proportional to the population with a floor of one per non-empty stratum, deterministic given
a seed. Every report that claims an axis is measurable states the profile of the **sample**,
not of the population.

## D-020 — Convergence is structural, and a generation cap is reported as a failure to converge

**Status:** ACTIVE

The first V2 run stopped on its generation budget and reported `STRUCTURAL_CONVERGENCE: NO`.
That honesty has to survive a controller being asked to "run to convergence", so the two
outcomes are different return values with different names.

Convergence requires three conditions together for `stall_limit` consecutive generations: the
frontier did not improve materially on any selection axis; the frontier's **membership** did
not change, since a frontier swapping candidates at a fixed signature is still exploring; and
no new axis entered the genome, since a search still growing its own space has not finished
searching the space it has. Reaching `max_generations` returns
`GENERATION_CAP_REACHED_NOT_CONVERGED` and says so in the reason string.

## D-021 — Evidence carries a role, and non-Lean material cannot be promoted into formal truth

**Status:** ACTIVE

Two sources are needed for things a Lean trace structurally cannot contain, and both are
dangerous to hold next to verifier output without a declared boundary.

PRM800K is registered `DISCOVERY_GRAPH_EVIDENCE`. Its value is naming the five discovery
dimensions — progress, valid-but-useless, dead end, alternative branch, attempt outcome —
that `DISCOVERY_REPRESENTATION_ANALYSIS.md` measured and found no representation in the
search space can express, because `CanonicalMathState` carries none of them. A Lean trace
holds only steps that were kept, so it contains no negative examples at all, while 25.3% of
PRM800K's rated continuations are dead ends. Its −1/0/+1 are human judgements of usefulness
and are never verdicts of logical validity.

GSM8K is registered `NATURAL_LANGUAGE_MATH_EVIDENCE` at pinned commit `3101c7d5`, MIT. It is
evidence about how mathematics is *written*; it carries no proof term, no tactic, no proof
state and no verifier, so nothing in it can enter a `CanonicalMathTransition`.

`not_lean_truth` is derived from `formal_system`, never asserted independently, and
`tests/test_registry_and_manifests.py` refuses any dataset carrying it the role
`LEAN_FORMAL_TRUTH` or a trust tier of A or B.

## D-022 — An invented axis must differ from every axis the genome already has

**Status:** ACTIVE

`D-014`'s observable-effect gate asks whether a new axis does anything. It does not ask
whether the genome already has an axis that does exactly the same thing, and `FM-033` records
what that permitted: of the first thirty axes accepted on the 918-transition pool, nine were
`neighbourhood_capsule` over `NONE/GOAL_LOCAL/ACTION_LOCAL` with empty params, under nine
different names. They render identically to one another and applying two is idempotent with
applying one.

Acceptance now also requires behavioural novelty: the candidate axis is rendered at every
value and rejected if the resulting *set* of renderings equals that of any active axis.
Comparison is behavioural rather than by `(hook, params, values)` signature, because two axes
with different hooks or different value names can still reach the same renderings. Rejections
are recorded as `ACCEPTED_DUPLICATE` with the axis they duplicate, alongside
`ACCEPTED_UNIMPLEMENTABLE`.

This matters beyond tidiness for two reasons. The reported search-space size is a product over
axes, so each duplicate multiplied it by three while adding no reachable representation — the
nine-axis group alone inflated it by 6,561x. And structural convergence (`D-020`) is
unreachable while a meta-designer can mint a fresh *name* for an axis that already exists.

## D-023 — A component is judged only through an instrument that has been proved to work

Date: 2026-08-29. Branch: `main` (HML_V3). Status: **ACCEPTED, ENFORCED BY MEASUREMENT.**

Before the certification arms existed, MicroMath Lab V1 reported a per-cell accuracy for each
representation and ranked targets by the gap to the best control. Every one of those numbers was
read as a statement about readability. Four of the eight were not.

The rule adopted is that **no component may be reported, ranked, mutated against, or certified
until its instrument has passed calibration on that same reader.** Calibration runs four arms on
identical pairs: the relation stated outright (`EXPLICIT_POSITIVE`), the relation destroyed and
a decoy prepended (`SCRAMBLED_NEGATIVE`), the best general control, and the candidate. The
thresholds are preregistered in `src/hml_v3/micromath/calibration.py`:

```
POSITIVE_MUST_EXCEED_CHANCE = 0.15
NEGATIVE_MAX_ABOVE_CHANCE   = 0.15
MINIMUM_DYNAMIC_RANGE       = 0.20
PARITY_MARGIN               = 0.10
```

An instrument whose negative arm does not return to chance is `INSTRUMENT_INVALID`: the question
is answerable with the relation destroyed, so it was never testing that relation. An instrument
whose positive arm cannot lift the reader is `INSTRUMENT_LIMIT`: the reader cannot do the task at
any readability, and the representation is neither credited nor blamed. Only the remainder yield
`ADVANTAGE`, `CONTROL_PARITY` or `LANGUAGE_WEAKNESS`.

Three consequences were accepted along with the rule.

**A clean shortcut audit does not license a measurement.** The audit's best dumb rule reaches
0.509 in aggregate and 0.5625 on any single cell — the benchmark is genuinely immune to
positional and frequency tricks — and four instruments were still invalid. Transposition
equalises the token multiset but not semantic plausibility (`FM-041`). Surface controls and
calibration test different things and neither substitutes for the other.

**Results measured before calibration are withdrawn, not reinterpreted.** The candidate's
reported 0.741 drew 75.9 % of its items from cells now known to be invalid or limited; on the
two valid cells it scores 0.500 (`FM-042`). The correct disposition for such a number is
withdrawal.

**A rejection on an invalid instrument is `VOID`, not `REFUTED`.** Five of seven rejected
mutations ran on valid instruments and are now readable as `WRONG_CAUSAL_HYPOTHESIS`. Two ran on
DEPENDENCY and must be re-run; one of those was the only mutation ever to clear the material
threshold, and it was overruled by a regression measured on `BINDER`, an `INSTRUMENT_LIMIT` cell.

The cost of the rule is one calibration run per component per reader — 8190 s for eight
components locally, at zero incremental spend. The cost of not having it was three hours of
probing, a failure gradient that ranked partly noise, and seven mutation evaluations of which
two must be discarded.

## D-024 — The shortcut audit is a hard gate that runs before any inference

Date: 2026-08-29. Branch: `codex/open-ended-search-v2`. Status: **ACCEPTED, ENFORCED IN CODE.**

`D-023` established that a component may only be judged through a calibrated instrument. It is
not sufficient. Calibration asks whether a reader can recover the relation when told it and
loses it when the relation is destroyed. It cannot see a question that is answerable without
reading anything at all.

The first MicroMath Lab V2 build had `g1` as the answer to every one of its 43 MULTI_GOAL
items. Calibration reported the negative arm at 0.833 against a chance of 0.440 — the right
signal, arrived at the wrong way, after 277 seconds of Qwen inference. Counting distinct
answers would have said the same thing in milliseconds.

So the audit runs first, on every item of every split, and gates certification:

- Seven rules that read only the option strings and their order — first, second, last,
  shortest, longest, alphabetically first, alphabetically last — none of which look at the
  mathematics. A cell any of them can solve is not an instrument.
- **Answer entropy.** Below one distinct answer per four items the cell is `CONSTANT_ANSWER`
  regardless of what the rules score.
- A cell that fails is `BENCHMARK_DEFECT`. It is not calibrated, not probed, and not reported
  as a fact about any representation.

Three properties of the rule were fixed by things that went wrong while building it.

**The rules read the order the model is shown.** The first version sorted the options and
scored position against that, which measured an ordering no reader sees; it reported BINDER
leaking at 0.447 while the presented positions were 17/11/10/9 across four slots (`FM-046`).

**Judgement is by interval, not by margin.** A flat 0.15 tolerance made the verdict a function
of sample size — the same construction came out CLEAN on one split and LEAKS on another,
because at fourteen items a rule at 0.43 against chance 0.25 is noise. The best of seven rules
is now tested by an exact binomial lower bound at a Bonferroni-corrected confidence, the same
discipline `D-023` applies to instrument arms.

**A key-aware rule is reported but never used to condemn.** "Pick the globally most common
answer" is fitted to the answer key of the cell it scores, so on forty items it approaches
reading the answers off the page. It measures the risk of publishing the benchmark beside its
key — a real risk, and a different one from "a reader can shortcut this" — so it is reported
separately and carries no verdict.

The cost is a few milliseconds per build. The cost of not having it was a component reported
to the user as the project's most important measurement when its answer never varied.
