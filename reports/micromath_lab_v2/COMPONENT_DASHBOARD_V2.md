# Component dashboard — MicroMath Lab V2

Reader `not run`, candidate `?`, control `?`.
Lab `micromath-lab-v2.0.0`. Rule `micromath-calibration-v2.0.0`, fixed before any V2 result existed.

## Instruments

| Component | Chance | Positive | Negative | Range | Control | Candidate | Norm. read. | Known-bad | Status |
|---|---|---|---|---|---|---|---|---|---|
| SEMANTIC_FIDELITY | — | — | — | — | — | — | — | — | NOT_A_MICROMATH_COMPONENT |
| BINDER | — | — | — | — | — | — | — | — | NOT_RUN |
| SCOPE | — | — | — | — | — | — | — | — | NOT_RUN |
| TYPE | — | — | — | — | — | — | — | — | NOT_RUN |
| EXPRESSION_DEPTH | — | — | — | — | — | — | — | — | NOT_RUN |
| DEPENDENCY | — | — | — | — | — | — | — | — | NOT_RUN |
| MULTI_GOAL | — | — | — | — | — | — | — | — | NOT_RUN |
| PREMISE | — | — | — | — | — | — | — | — | NOT_RUN |
| ACTION_ARGUMENT | — | — | — | — | — | — | — | — | NOT_RUN |
| STATE_DELTA | — | — | — | — | — | — | — | — | NOT_BUILT |

## Counts

- valid instruments: **0** []
- invalid: **0** []
- instrument limits: **0** []
- undecided at the ladder cap: **0** []
- ADVANTAGE: **0** []
- CONTROL_PARITY: **0** []
- LANGUAGE_WEAKNESS: **0** []

**CERTIFIED requires all of** `§29`: valid instrument, perfect semantic preservation, at least control parity, reproduction on fresh shadow/holdout, known-bad detection, and no catastrophic regression elsewhere. A component is reported as certified only when every one of those has been executed.

## Splits

| Split | Items | Base states |
|---|---|---|
| `micro_dev_v2` | 341 | 114 |
| `micro_shadow_v2` | 156 | 54 |
| `micro_hidden_v2` | 193 | 63 |

Base-state overlap between splits: `{'dev_shadow': 0, 'dev_hidden': 0, 'shadow_hidden': 0}` — required to be zero everywhere (`FM-043`).

Retired as spent: `{'micro_dev': 28, 'micro_shadow': 8, 'micro_hidden': 7}` — FM-043: consumed by the V1 certification top-up; spent as holdouts

## Architectural hypotheses

Not run.
