# MicroMath Lab V1 — specification

Lab version `micromath-lab-v1.0.0`. Package `src/hml_v3/micromath/`.

## Purpose

Locate a representation's *specific* structural weakness cheaply, before spending hours on a
global search. The unit of measurement is a **domain × structural-stress cell**, not an
aggregate score.

## Design

**Matched transposition counterfactuals.** Every item is a pair of states `(A, B)` where B is a
permutation of A. The token multiset is therefore identical by construction, which controls for
length, vocabulary and token frequency without any post-hoc normalisation. A reader that scores
above chance must be reading structure — or, as the certification later established, priors
carried in the identifiers (FM-041).

**Two-choice questions.** Each pair poses one question with two options; chance is 0.500.
Both arms of the pair are asked, so a representation cannot profit from a constant answer.

**Eight structural stresses**, each naming one relation:

| Stress | Question |
|---|---|
| BINDER | which local declaration a given use in the goal refers to |
| SCOPE | which goal a given local declaration lives in |
| TYPE | which type belongs to a given declaration |
| DEPENDENCY | which declaration the type of another declaration depends on |
| PREMISE | which external premise the action cites |
| ACTION_ARGUMENT | which local declaration the action uses as an argument |
| MULTI_GOAL | which goal the action acts on |
| EXPRESSION_DEPTH | which reference sits deepest in the goal target |

**Six domains**, assigned from Mathlib module path with a recorded confidence: ALGEBRA,
CALCULUS_ANALYSIS, GEOMETRY, LINEAR_ALGEBRA, LOGIC_SET_THEORY, PROBABILITY_STATISTICS.

## Instrument calibration (the part that mattered)

Preregistered in `src/hml_v3/micromath/calibration.py` before any certification run.

Four arms are run per component on identical pairs:

1. `EXPLICIT_POSITIVE` — the answer is prepended in words. Establishes the ceiling this reader
   can reach when readability is not the obstacle.
2. `SCRAMBLED_NEGATIVE` — a *decoy* answer is prepended and the relation is destroyed.
   Establishes the floor. **Must return to chance.**
3. the best general control representation.
4. the candidate.

Thresholds:

```
POSITIVE_MUST_EXCEED_CHANCE = 0.15
NEGATIVE_MAX_ABOVE_CHANCE   = 0.15
MINIMUM_DYNAMIC_RANGE       = 0.20
PARITY_MARGIN               = 0.10
```

Verdicts, in evaluation order:

- `INSTRUMENT_INVALID` — the negative arm scores too high. The question is answerable with the
  relation destroyed, so it was never testing that relation. No conclusion may be drawn.
- `INSTRUMENT_LIMIT` — the positive arm cannot lift the reader, or the range is too narrow.
  The reader cannot do this task at any readability; the representation is not to blame.
- `ADVANTAGE` — the candidate beats the best control by more than the parity margin.
- `CONTROL_PARITY` — candidate and best control are within the parity margin.
- `LANGUAGE_WEAKNESS` — the candidate trails the best control by more than the parity margin.

Normalised readability, reported only when the range is adequate:

```
(candidate − negative) / (positive − negative)
```

**No component may be reported as certified without a valid instrument.** This ordering — build
the instrument, prove it works, only then judge the language — is the single most valuable thing
in the lab, and it invalidated most of the lab's own earlier output.

## Anti-gaming

- Per-stress shortcut audit against four answer-targeted dumb rules (FM-038 required this to be
  per-cell; an aggregate audit hid two leaking cells).
- Options are compared as codec-encoded ids, not raw canonical ids the codec never emits
  (FM-039).
- Base-state-disjoint splits, stratified by stress, so `micro_hidden` cannot share mathematics
  with `micro_dev` (FM-040).
- Size-budgeted base states so items fit the reader's context (FM-040).
- Stresses are defined on set membership, never on list order, because `semantic_core` stores
  those fields `sorted()` (FM-037).

## Cost and constraints honoured

£0 incremental paid API, £0 paid GPU. All inference local via ollama. No LLM-generated
mathematical answer was used as ground truth — every answer is derived from `semantic_core`.
`SEALED_FINAL_V2` was not read, not loaded, and not used in construction or evaluation.
