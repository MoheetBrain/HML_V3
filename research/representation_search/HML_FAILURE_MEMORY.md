# HML Failure Memory

Persistent, machine-readable memory of every prior representation experiment whose result
constrains this search. The companion artifact is
[`hml_failure_memory.json`](hml_failure_memory.json); the search controller loads that file
every generation and refuses to spend budget re-deriving a result that is already recorded
here.

**These are not arguments for natural language.** They are constraints on experiment design
and on which mutations are worth a generation's budget. A representation may still be
proposed against a recorded negative — but only with a stated mechanism for why the earlier
refutation does not apply, and the proposal is tagged `RETRY_WITH_CHANGED_CONDITION`.

## Reading the dispositions

| Disposition | Meaning for this search |
|---|---|
| `REJECTED_CAUSAL_CLAIM` | The effect existed in the numbers and disappeared under control. Never cite the uncontrolled number again. |
| `DO_NOT_RETRY_UNCHANGED` | The intervention was measured and lost. Re-proposing it verbatim wastes a generation. |
| `RETAIN_AS_BASELINE` | The candidate beat prior HML and must stay in the population as a control even if it leaves the Pareto front. |
| `EXPERIMENT_DESIGN_CONSTRAINT` | A property every future benchmark must have. Binding on task construction, not on genomes. |
| `METRIC_DEFECT` | A metric that produced a persuasive wrong answer. The corrected definition is mandatory. |
| `INSTRUMENT_SATURATED` | The measurement could not discriminate. Do not reuse without hardening. |

---

## FM-001 — The headline HML advantage was a prompt-envelope artifact

**Recorded result.** Two 10K-seed runs measured HML − Neutral at **+35.55pp**, pooled CI
[+33.53, +37.50]pp. The common-envelope control, which equalised every non-state byte in the
prompt, measured HML 85.33% against Neutral 88.10% — a delta of **−2.77pp**, CI
[−3.72, −1.81]pp. The zero-shot common-envelope arm measured **−3.97pp**, CI [−4.87, −3.07]pp.

**Mechanism.** The Neutral arm carried a materially worse instruction envelope. The measured
gain was attributable to prompt scaffolding, not to state serialization.

**Disposition:** `REJECTED_CAUSAL_CLAIM`.
**Binding on this search:** every comparison must hold non-state bytes byte-identical across
arms. A genome that changes the envelope rather than the state encoding is not a
representation difference.

---

## FM-002 — Prior HML syntax is not privileged among reasonable surfaces

**Recorded result.** `EXP_REP_VALIDITY_V1` Stage 1, IID macro-F1: Structured English
**0.7939**, Lean-like **0.7759**, prior HML **0.7701**, typed AST **0.7664**. Out of
distribution, Structured English won 6/7 splits and Lean-like won the alpha-rename split.
HML was never significantly best and led no split.

**Disposition:** `RETAIN_AS_BASELINE` (Structured English, Lean-like), plus
`DO_NOT_RETRY_UNCHANGED` for "prior HML syntax is inherently superior".
**Binding on this search:** Structured English, Lean-like, prior-HML and typed-AST seeds are
carried to the end of the search whether or not they remain Pareto-optimal.

---

## FM-003 — Most of the measured accuracy was lexical

**Recorded result.** Bag-of-words controls reached **0.7213–0.7559** macro-F1 on the same
task where the frozen transformer reached 0.7664–0.7939. The transformer's uplift over its
own lexical control was only **+0.0219 to +0.0546**.

**Disposition:** `EXPERIMENT_DESIGN_CONSTRAINT`.
**Binding on this search:** any future model-facing task must be gated by class-prior,
length-only, structural-count, bag-of-words, character n-gram, and shallow-lexical controls
*before* a representation difference is reported. Static search cannot discharge this; it is
recorded so the eventual model experiment cannot forget it.

---

## FM-004 — A serializer asymmetry can dominate the representation effect

**Recorded result.** The HML50K forensic audit found decoded literal Unicode escape payloads
present asymmetrically in the HML model rows while the canonical source stayed clean. The
comparison was invalidated. A separate tokenizer audit priced the defect: `⊢`, `∀`, `ℝ`, `𝕜`
and `✝` are **one token each** in the Qwen3-8B vocabulary, while their escaped spellings cost
**5**, and `inst✝⁵` goes from 4 tokens to **11**. The measured accuracy cost when this was
last put to a model was **−3.41pp**.

**Disposition:** `REJECTED_CAUSAL_CLAIM` for the HML50K comparison; `HARD_GATE` for the
encoding.
**Binding on this search:** UTF-8 correctness is a hard gate, not a metric. Any candidate
emitting escaped spellings of glyphs that exist in the corpus is rejected before scoring.

---

## FM-005 — Goal-centred ordering does not improve locality; it worsens it

**Recorded result.** On structurally rich fixtures, mean citation distance was
`canonical` **910c/340t**, `topological` **818c/306t (−10.1%)**, `goal_centered`
**948c/355t (+4.2%, worse)** — at identical token cost for all three. On 400 real
transitions `goal_centered` rendered **byte-identically** to `canonical`, because those
states had nothing to reorder. This was the second independent negative for goal-relevance,
after the causal autopsy found that *supplying* relevance changed nothing measurable.

**Mechanism.** Relevance and dependency proximity are different relations; grouping by
relevance separates a fact from the facts it cites.

**Disposition:** `DO_NOT_RETRY_UNCHANGED`.
**Changed condition that would justify a retry:** the prior corpus averaged **1.00 claims per
state and zero dependencies**. The V2 runtime corpus has real elaborated local contexts and
real reference edges, so ordering is measurable on real data for the first time. A
goal-centred genome may therefore be re-entered **once**, explicitly tagged, and must be
re-rejected on the new evidence if it loses again.

---

## FM-006 — Dependency-topological ordering is a free improvement

**Recorded result.** Same fixtures: `topological` cut citation distance ~10% at **identical**
token cost and slightly better mutation detection (0.977 against 0.970). It degrades to key
order when a state has no dependencies, rendering byte-identically to the incumbent on
400/400 real transitions.

**Disposition:** `RETAIN_AS_BASELINE` — carried into Generation 0 as a seed trait, not as a
conclusion.

---

## FM-007 — S-expressions destroy record-order error detection

**Recorded result.** Mutation detection by family, 400 real transitions:
`R2_CANONICAL_SEXPR` scored **0.000** on `swap_two_lines` against **0.877–0.884** for the
block forms, for an overall 0.800 against 0.948–0.950. Its compensating win was `drop_line`
(1.000 against 0.865). Its token saving was **0.6%**.

**Mechanism.** A self-contained parenthesised record per line means exchanging two lines
decodes to the same mapping; order carries no checkable information.

**Disposition:** `DO_NOT_RETRY_UNCHANGED` for "flat one-record-per-line S-expressions are
strictly better".
**Binding on this search:** error-detection is measured per mutation family and never
collapsed to a single mean before selection, because a candidate can be excellent on average
while being blind to an entire corruption class.

---

## FM-008 — Compression is a diagnostic, never the objective

**Recorded result.** Across every candidate, the total token spread was **1.4%**
(1,092.5 to 1,108.4) and the gzip spread was ~2%. Meanwhile the single largest cost in the
design was not syntax at all: **18.8% of the prompt** was re-emitting state records unchanged
between before and after.

**Disposition:** `EXPERIMENT_DESIGN_CONSTRAINT`.
**Binding on this search:** token count is one axis of a Pareto vector and never a scalar
objective. A candidate that compresses by deleting structure fails the hard gates first.

---

## FM-009 — The line-based locality metric was an artifact

**Recorded result.** Measured in **lines**, `R2_CANONICAL_SEXPR` appeared to improve locality
**6.3×** (2.50 against 15.75). Re-measured in characters and tokens it was marginally
*worse* (979c against 976c) and identical in tokens. A block form uses ~5 lines where an
S-expression uses 1, so a line metric measures line density, not distance.

**Disposition:** `METRIC_DEFECT`.
**Binding on this search:** every distance metric is defined in characters **and** tokens.
Line counts are never a distance unit.

---

## FM-010 — The minimal-pair instrument saturated

**Recorded result.** Stage 1 minimal pairs scored **0.9647–0.9853** across all arms.

**Disposition:** `INSTRUMENT_SATURATED`.
**Binding on this search:** a benchmark whose arms all exceed ~0.95 is reported as
non-discriminative rather than as agreement.

---

## FM-011 — Non-determinism in the shipped renderer

**Recorded result.** `R0_SOURCE_BLOCK` rendered in mapping-construction order: `A == B` while
`render(A) != render(B)`. Corpus builds were not reproducible and the model was shown an
ordering signal with no meaning.

**Disposition:** `HARD_GATE`. Deterministic serialization is a gate in this search, not a
metric.

---

## FM-012 — An opaque wrapper is not a semantic state

**Recorded result.** Prior measurement found structurally empty wrappers — one claim
containing an entire Lean state as text — despite rich content inside.

**Disposition:** `HARD_GATE`. A candidate must expose goals, local declarations and
expression structure as addressable units; a genome that emits the state as one opaque
literal is rejected by the structural-recoverability gate.

---

## FM-013 — Derived structured projections were lossy where it mattered

**Recorded result.** The prior source projection's `hypotheses`/`target` fields disagree with
exact raw-state decomposition on **659 of 2,000** V1 observations, chiefly multiline
truncation. All **241,265** prior derived records had an empty `premises_used` list.

**Disposition:** `EXPERIMENT_DESIGN_CONSTRAINT`. The search reads elaborated Lean runtime
identities, never a re-parse of pretty-printed text.

---

## FM-014 — Real corpora can be too structurally trivial to discriminate

**Recorded result.** The prior real corpus averaged **1.00 claims per state**, zero
candidates, branches, goals and obligations. Ordering, locality and dependency metrics were
therefore unmeasurable on real data, and every ordering conclusion rested on synthetic
fixtures.

**Disposition:** `EXPERIMENT_DESIGN_CONSTRAINT`.
**Binding on this search:** structural-richness statistics of the corpus are reported
alongside every locality result, and a locality claim measured only on synthetic states is
labelled as such.

---

## FM-015 — Trace provenance is not fresh replay

**Recorded result.** Lean attestation Stage100 produced **32** exact replay passes and 68
non-passes; 56/100 rows were `UNSUPPORTED` for path reconstruction. Every target action that
was actually reached matched its exact before/after state.

**Disposition:** `EXPERIMENT_DESIGN_CONSTRAINT`. Verifier language stays calibrated:
`FRESH_REPLAY_PASS` is never inferred from `FORMAL_TRACE_ACCEPTED`.

---

---

# Lessons measured by this search

Everything above was carried in from prior repositories. Everything below was measured here,
and each entry names the run that produced it.

---

## FM-018 — Glyph token cost is a property of the vocabulary, not of the representation

**Measured by.** The pinned GPT-2 byte-level BPE, against the prior audit's Qwen3-8B figures.

| glyph | Qwen3-8B (prior audit) | GPT-2 (this search) | escaped, GPT-2 |
|---|---:|---:|---:|
| `⊢` | 1 | 3 | 7 |
| `∀` | 1 | 2 | — |
| `ℝ` | 1 | 3 | — |
| `𝕜` | 1 | 3 | 8 |
| `✝` | 1 | 2 | — |
| `inst✝⁵` | 4 | 5 | 12 |

**Two readings, and they point in different directions.** `FM-004`'s escaping penalty
**reproduces** under a second, independent vocabulary: escaping costs 2.3x–2.7x under GPT-2,
so the UTF-8 hard gate is not an artifact of one tokenizer. The absolute counts do **not**
reproduce: every glyph the corpus needs is one token under Qwen3-8B and two or three under
GPT-2.

**Disposition:** `EXPERIMENT_DESIGN_CONSTRAINT`. Every token claim names its vocabulary, and
byte counts plus tokenizer-free pre-tokens are reported beside every token count.

---

## FM-019 — Identifier-corruption detection saturates across every candidate

**Measured by.** All sixteen generation-zero seeds, 24 real V2 transitions.

`detect_corrupt_identity` read **1.000 for every seed**. An altered identifier either fails to
resolve or resolves to a different declaration, so every representation over an
identity-carrying canonical state catches it. For contrast, `detect_drop_field` spread
0.000–0.792 and `detect_truncate_tail` 0.000–0.833 over the same seeds.

**Disposition:** `INSTRUMENT_SATURATED`. Following `FM-010`, the axis was removed from Pareto
selection **before the search began** and `detect_drop_field` took its place. It is still
measured and still reported.

`detect_truncate_tail` reads 0.000 for fifteen of sixteen seeds for a different and benign
reason: the trailing block is usually the structured delta, which is outside the declared
semantic contract. The one exception drops the delta entirely, which makes its tail contract
content.

---

## FM-020 — Goal linearization is unmeasurable on a corpus of single-goal states

**Measured by.** The pilot run over the 317-transition V2 corpus.

`graph_serialization` was mutated 11 times as a single-axis change. It changed the
measurement **0 times**. The corpus averages **1.01 goals per state** with a maximum of 2, so
every linearization strategy renders identically. Five other axes also measured at 0%:
`const_name_form`, `keyword_case`, `local_instance_visibility`, `role_word_length`,
`type_attachment`.

This is `FM-014`'s problem in a new place and now quantified per axis. The same corpus is
richly structured in the *other* direction — mean 13.4 local declarations and 63.4
intra-context references — so `context_order` moved the measurement 90% of the time.

**Disposition:** `EXPERIMENT_DESIGN_CONSTRAINT`. The share of single-axis mutations that
changed the measurement is reported per axis beside any claim about that axis. An axis at 0%
is reported as unmeasurable on this corpus, never as tied.

---

## FM-021 — Goal-centred ordering loses again, now with real dependencies present

**Measured by.** The pilot run. `FM-005` granted exactly one retry on a named changed
condition: the V2 corpus carries real local-context dependency structure where the prior
corpus averaged 1.00 claims and zero dependencies. The retry was taken.

`context_order: DEPENDENCY_TOPOLOGICAL -> GOAL_CENTRED` changed
`binder_use_distance_tokens` by **+3.8%** across 2 parents with 100% sign agreement — worse,
in the same direction as before. `SEED_GOAL_LOCAL` finished 119th of 165 on token cost.

The mechanism `FM-005` named — relevance and dependency proximity are different relations —
now has support from a corpus that actually has dependencies to separate.

**Disposition:** `DO_NOT_RETRY_UNCHANGED`, retry budget now **0**. `SEED_GOAL_LOCAL` remains
in the population as a seed so the baseline stays visible; only new mutations toward
goal-centred ordering are blocked.

---

## FM-022 — Hoisting shared subterms into a DAG more than doubles token cost

**Measured by.** The pilot run.

`shared_subterm_handling: DUPLICATE -> HOISTED_DAG_LETS` changed
`bpe_tokens_per_transition` by **+136.4%** across 2 parents with 100% sign agreement.
`SEED_HYBRID_LOCAL_DAG` measured 20,625 tokens against 7,013 for the cheapest seed, and its
record-order corruption detection fell to **0.375**.

**Mechanism.** The intuition is that a subterm repeated n times should be written once.
Measured on real elaborated Lean expression trees, the alias table plus the reference
machinery costs far more than the sharing saves: subterms that repeat are mostly small, and
the ones large enough to be worth hoisting are rarely repeated. Detection falls because an
alias section separates a record from the content that identifies it.

**Disposition:** `DO_NOT_RETRY_UNCHANGED`, with one retry available on a named changed
condition: a corpus whose expression trees repeat *large* maximal subterms. Measure the
repeat-size distribution before spending that retry.

---

## FM-023 — Naive substring matching inflated the locality metric

**Measured by.** Found while the definitive run was in progress, by checking the metric
against a real rendering rather than trusting it.

Short identity tokens are prefixes of longer ones. Searching for `bf1` with a plain substring
scan also matches inside `bf10` through `bf19`. On the first transition checked that was
**80 matches against a true 64 — a 25% overcount** — and every distance derived from those
positions inherited the error. Premise names had the same defect: `Nat.add` matches inside
`Nat.add_comm`.

**Disposition:** `METRIC_DEFECT`. Occurrences are now counted with token boundaries on both
sides. This is `FM-009`'s failure mode repeating in a new place: a locality metric that looks
reasonable, produces confident numbers, and measures something other than what it claims.

**Consequence, stated plainly.** The pilot run's locality figures were computed before this
fix and are inflated. The definitive run is **not comparable** to them, and the pilot's
numbers are retained only as archived history under
`data/representation_search/archive/`.

---

## FM-024 — Cost and locality rank stably; corruption detection does not

**Measured by.** Two independent checks that agree.

*Across a held-out split selection never read* — the finalists measured on `SEARCH_DEV` and
on `SEARCH_VALIDATION`, Spearman rho between the two orderings:

| Axis | rho | Same leader? |
|---|---:|---|
| `identifier_fragmentation` | +1.000 | yes |
| `bpe_tokens_per_transition` | +0.976 | yes |
| `max_reference_span_tokens` | +0.976 | yes |
| `binder_use_distance_tokens` | +0.952 | yes |
| `premise_to_action_distance_tokens` | +0.929 | yes |
| `detect_drop_field` | +0.929 | **no** |
| `detect_swap_records` | **+0.357** | **no** |

*Across sixteen Mathlib domains* — the share of domains in which one finalist leads the axis:
100% for token cost, binder distance and identifier fragmentation; 94% for premise distance;
**38–56%** for the two corruption-detection axes.

**The reading.** Cost and locality are properties of the representation: they rank the same
way on data selection never saw, and the same way in every branch of mathematics measured.
Corruption detection depends on what the state happens to contain — how many records there
are, how much of the text is contract content, whether a dropped line leaves a still-valid
record.

**Disposition:** `EXPERIMENT_DESIGN_CONSTRAINT`. A corruption-detection claim names its
sample and carries its cross-split rank correlation. A cost or locality claim may be stated
for the representation itself.

---

## Open lessons this search is expected to add

The mission brief lists two further beliefs that this repository has **no local artifact
for**: that "generic structured representations sometimes matched or beat HML" beyond the
Stage-1 table above, and that "excessive compression is not automatically beneficial" as a
measured result rather than a design principle. They are recorded in the JSON with
`evidence_status: ASSERTED_WITHOUT_LOCAL_ARTIFACT` so a later session neither cites them as
measured nor loses them.
