# Dataset card — MicroMath Lab V2

Version `micromath-lab-v2.0.0`. Location `data/micromath_lab_v2/` (sharded gzip JSONL).
Manifest: `manifest.json`. Split registry: `firewall.json`.

## Provenance and the retirement of V1

Built from **1051 base states**, after retiring the **43** that the V1 certification consumed ({'micro_dev': 28, 'micro_shadow': 8, 'micro_hidden': 7}).

*FM-043: consumed by the V1 certification top-up; spent as holdouts*

Retired states are refused by the firewall permanently, in every compartment. Excluding a
spent holdout from future runs does not make it clean again, and treating it as though it
were would be `FM-043` a second time.

Of those, **456 fall within the 14000-character
rendering budget** and are eligible; the rest are too large for the reader's context
(`FM-040`). The lab is therefore built from the smaller half of the corpus, and any claim
about it inherits that.

## Splits

| Split | Items | Base states | Purpose | Read so far |
|---|---|---|---|---|
| `micro_dev_v2` | 301 | 99 | calibration, probing, architecture screening | yes |
| `micro_shadow_v2` | 135 | 49 | regression guard for a promoted mutation | **no** |
| `micro_hidden_v2` | 175 | 55 | generalisation, gated on a certified component | **no** |

Base-state overlap between all three: `{'dev_shadow': 0, 'dev_hidden': 0, 'shadow_hidden': 0}` — required to be
zero, asserted at construction and again by the firewall at every load.

## Composition

| Stress | dev | shadow | hidden | Options (dev) | Chance (dev) |
|---|---|---|---|---|---|
| ACTION_ARGUMENT | 48 | 24 | 24 | {2: 2, 3: 2, 4: 44} | 0.264 |
| BINDER | 47 | 20 | 29 | {2: 4, 3: 3, 4: 40} | 0.277 |
| DEPENDENCY | 46 | 21 | 29 | {4: 46} | 0.250 |
| EXPRESSION_DEPTH | 45 | 22 | 29 | {2: 6, 3: 11, 4: 28} | 0.304 |
| PREMISE | 46 | 19 | 31 | {4: 46} | 0.250 |
| SCOPE | 21 | 10 | 4 | {2: 17, 3: 3, 4: 1} | 0.464 |
| TYPE | 48 | 19 | 29 | {2: 7, 3: 8, 4: 33} | 0.300 |

**MULTI_GOAL carries zero items in every split** and this is deliberate (`FM-044`): the
relation is not rendered by any axis of the representation space, so no representation can
be scored on it. See `SPEC.md` §8.

## Domains

| Domain | dev items |
|---|---|
| ALGEBRA | 127 |
| CALCULUS_ANALYSIS | 43 |
| GEOMETRY | 9 |
| LOGIC_SET_THEORY | 20 |
| MIXED | 101 |
| PROBABILITY_STATISTICS | 1 |

## Shortcut audit

| Split | Cells | Failing |
|---|---|---|
| `micro_dev_v2` | 7 | none |
| `micro_shadow_v2` | 7 | none |
| `micro_hidden_v2` | 7 | none |

Seven rules that read only the options as presented, judged against chance by
Bonferroni-corrected exact binomial bounds, plus a constant-answer check. See `SPEC.md` §6.

## Difficulty ladders

The `MISSION §15` rungs are kept exactly as specified and **not re-cut after seeing the
data**, because re-cutting them would be the error `§8` forbids for the calibration rule.
Several are empty on this corpus, and that emptiness is itself the finding.

| Ladder | Population (dev) |
|---|---|
| MULTI_GOAL | **no items** (withdrawn) |
| EXPRESSION_DEPTH | E1=1, E2=6, E3=10, E4=26, E5=2 |
| DEPENDENCY | D1=0, D2=0, D3=1, D4=6, D5=39 |

For EXPRESSION_DEPTH the real difficulty axis turned out to be the **lead** — how far
the deepest reference outranks the runner-up — not absolute depth (`FM-047`). Distribution
in dev: `{1: 35, 2: 4, 3: 2, 4: 1, 7: 1, 9: 1, 12: 1}`. A lead of one is the hard case and covers most of
the corpus.

## Known limitations

1. **MULTI_GOAL is unmeasurable here** and withdrawn (`FM-044`).
2. **SCOPE is underpowered.** ~20 dev items, because most states carry two goals. It passes
   the audit, but any verdict rests on a small sample and says so.
3. **The pre-registered ladders barely populate.** G5 and D1–D2 are empty. **The long-horizon
   prediction of `PROJECT_GOAL` §18 cannot be tested on this corpus** — that is a statement
   about the corpus, not about any representation.
4. **Over half the available base states exceed the rendering budget** and are excluded.
5. **Ground truth is mechanical.** Every question, option and answer is derived from
   `semantic_core`. No LLM-generated mathematical answer is used as truth anywhere.
6. State A is a real Lean-derived canonical state, anonymised. The ablated state is a
   well-formed CanonicalMathState that is **not** claimed to be a provable proof state; it is
   a negative control whose relation is known-destroyed by construction.

