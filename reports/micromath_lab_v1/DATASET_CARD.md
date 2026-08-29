# Dataset card — MicroMath Lab V1

Version `micromath-lab-v1.0.0`. Location `data/micromath_lab_v1/` (sharded gzip JSONL).
Manifest: `data/micromath_lab_v1/manifest.json`.

## Contents

- **45 pairs / 90 states**, one pair per populated cell.
- **45 of 48 cells populated** (6 domains x 8 stresses).
- **45 distinct base states** for 45 pairs — no base state is reused, and no
  base state straddles two splits.

## Unpopulated cells

- GEOMETRY x SCOPE — `NO_ELIGIBLE_BASE_STATE` (0 candidates)
- LINEAR_ALGEBRA x SCOPE — `NO_ELIGIBLE_BASE_STATE` (0 candidates)
- LINEAR_ALGEBRA x MULTI_GOAL — `NO_ELIGIBLE_BASE_STATE` (0 candidates)

These are corpus-acquisition requests, not failures: no eligible base state in the V2 pool
exercises that relation in that domain within the size budget.

## Splits

| Split | Pairs | Purpose | Status |
|---|---|---|---|
| `micro_dev` | 29 | all probing, heatmaps, targeted search, certification | used as intended |
| `micro_hidden` | 8 | generalisation check | **spent — see below** |
| `micro_shadow` | 8 | regression guard for accepted mutations | used once (cycle 3); **spent — see below** |

Splits are assigned **by base state** and stratified by stress, so `micro_hidden` shares no
mathematics with `micro_dev` by construction (FM-040).

### Both holdouts are contaminated (FM-043)

`micro_dev` carries only 2–4 pairs per stress, so the certification run topped each component up
to 12 by minting fresh pairs from the V2 base pool. Its exclusion set was initialised from
`micro_dev` alone, so the builder was free to draw base states reserved for the other two splits
— and took **all 8 of `micro_hidden` and all 8 of `micro_shadow`**.

Nothing was fitted or selected on them: no mutation was accepted, and the contamination does not
affect any certification verdict, because instrument validity is a property of the question
design rather than of which base states were sampled. But both splits have now been measured on
and are spent as clean holdouts. **No generalisation claim can be made from `micro_hidden`.**

The cause is fixed in `scripts/micromath/run_component_certification.py`: the exclusion set is
now initialised from all three splits. Verified — every component still reaches 12 pairs with
zero overlap, so the pool was always deep enough to have avoided this.

A future generalisation check needs a freshly minted holdout, excluded from every prior run.

## Composition of `micro_dev`

| Domain | Pairs |
|---|---|
| ALGEBRA | 4 |
| CALCULUS_ANALYSIS | 5 |
| GEOMETRY | 7 |
| LINEAR_ALGEBRA | 2 |
| LOGIC_SET_THEORY | 5 |
| PROBABILITY_STATISTICS | 6 |

| Stress | Pairs |
|---|---|
| ACTION_ARGUMENT | 4 |
| BINDER | 4 |
| DEPENDENCY | 4 |
| EXPRESSION_DEPTH | 4 |
| MULTI_GOAL | 3 |
| PREMISE | 4 |
| SCOPE | 2 |
| TYPE | 4 |

## Provenance and ground truth

Base states are Lean 4 / Mathlib proof transitions from the V2 corpus pool. Every field of every
item — the question, both options, and the correct answer — is derived mechanically from
`semantic_core`. **No LLM-generated mathematical answer is used as ground truth anywhere in this
dataset.** Domain labels come from the Mathlib module path and carry a `domain_confidence`.

Per-row fields: `pair_id`, `stress`, `domain`, `domain_confidence`, `relation`, `question`,
`options`, `answer_a`, `answer_b`, `state_a`, `state_b`, `base_transition_id`, `source_file`,
`provenance`, `detail`.

## Known limitations

1. **Four of the eight stresses do not measure the relation they name.** DEPENDENCY, SCOPE,
   TYPE and PREMISE are answerable with the relation destroyed (negative arms 0.79–0.88):
   transposition equalises the token multiset but not semantic plausibility, and the answer
   remains recoverable from the identifiers. See FM-041 and `COMPONENT_DASHBOARD.md`.
2. **Two stresses are beyond the current reader.** ACTION_ARGUMENT tops out at 0.542 even when
   the answer is stated outright; BINDER has a dynamic range of 0.167.
3. **Only MULTI_GOAL and EXPRESSION_DEPTH are usable as measured.** Any analysis over all eight
   cells — including the published heatmaps and the 0.741 aggregate probe — mixes measurement
   with non-measurement.
4. **Two choices is too few** for cells with strong identifier priors. PREMISE_V2 (four choices,
   plausible distractors) is specified but not built.
5. Small: 12 pairs per component in certification, 29 in `micro_dev`. Adequate for detecting a
   broken instrument, marginal for resolving small differences between representations.
6. **Both holdout splits are spent** (FM-043). Any generalisation check requires a new one.
