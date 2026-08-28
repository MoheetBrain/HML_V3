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

## Open lessons this search is expected to add

The mission brief lists two further beliefs that this repository has **no local artifact
for**: that "generic structured representations sometimes matched or beat HML" beyond the
Stage-1 table above, and that "excessive compression is not automatically beneficial" as a
measured result rather than a design principle. They are recorded in the JSON with
`evidence_status: ASSERTED_WITHOUT_LOCAL_ARTIFACT` so a later session neither cites them as
measured nor loses them.
