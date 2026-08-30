# Component dashboard — MicroMath Lab V2

Reader `qwen38-rvn:latest`, candidate `R_015b8cd926da`, control `TYPED_AST`.
Lab `micromath-lab-v2.0.0`. Rule `micromath-calibration-v2.0.0`, fixed before any V2 result existed.

## Instruments

| Component | Chance | Positive | Negative | Range | Control | Candidate | Norm. read. | Known-bad | Status |
|---|---|---|---|---|---|---|---|---|---|
| SEMANTIC_FIDELITY | — | — | — | — | — | — | — | — | NOT_A_MICROMATH_COMPONENT |
| BINDER | 0.277 | 1.000 | 0.250 | 0.750 | 0.833 | 0.917 | 0.889 | INSTRUMENT_DEFECT | **CONTROL_PARITY** |
| SCOPE | 0.464 | 0.917 | 0.250 | 0.667 | 0.750 | 0.667 | 0.625 | INSTRUMENT_DEFECT | **CONTROL_PARITY** |
| TYPE | 0.300 | 1.000 | 0.333 | 0.667 | 0.917 | 0.917 | 0.875 | DETECTED | **CONTROL_PARITY** |
| EXPRESSION_DEPTH | 0.304 | 1.000 | 0.083 | 0.917 | 0.167 | 0.167 | 0.091 | INSTRUMENT_DEFECT | **CONTROL_PARITY** |
| DEPENDENCY | 0.250 | 1.000 | 0.333 | 0.667 | 0.542 | 0.625 | 0.438 | INSTRUMENT_DEFECT | **CONTROL_PARITY** |
| MULTI_GOAL | — | — | — | — | — | — | — | UNTESTED | **UNTESTED** |
| PREMISE | 0.250 | 1.000 | 0.000 | 1.000 | 0.833 | 0.833 | 0.833 | INSTRUMENT_DEFECT | **CONTROL_PARITY** |
| ACTION_ARGUMENT | 0.264 | 1.000 | 0.167 | 0.833 | 0.917 | 0.917 | 0.900 | INSTRUMENT_DEFECT | **CONTROL_PARITY** |
| STATE_DELTA | — | — | — | — | — | — | — | — | NOT_BUILT |

## Counts

- valid instruments: **7** ['ACTION_ARGUMENT', 'BINDER', 'DEPENDENCY', 'EXPRESSION_DEPTH', 'PREMISE', 'SCOPE', 'TYPE']
- invalid: **0** []
- instrument limits: **0** []
- undecided at the ladder cap: **0** []
- ADVANTAGE: **0** []
- CONTROL_PARITY: **7** ['ACTION_ARGUMENT', 'BINDER', 'DEPENDENCY', 'EXPRESSION_DEPTH', 'PREMISE', 'SCOPE', 'TYPE']
- LANGUAGE_WEAKNESS: **0** []

**Negative arm below chance: ['EXPRESSION_DEPTH', 'PREMISE', 'SCOPE'].** The ablation for these inverted the relation rather than erasing it -- the reader follows the damaged structure to the answer the damage created. The pre-registered rule only requires the negative not to be ABOVE chance, so no verdict changes, but the dynamic range is wider than an honest guessing floor and any normalised readability against it flatters its denominator. Read those figures with that in mind.

**CERTIFIED requires all of** `§29`: valid instrument, perfect semantic preservation, at least control parity, reproduction on fresh shadow/holdout, known-bad detection, and no catastrophic regression elsewhere. A component is reported as certified only when every one of those has been executed.

## Splits

| Split | Items | Base states |
|---|---|---|
| `micro_dev_v2` | 301 | 99 |
| `micro_shadow_v2` | 135 | 49 |
| `micro_hidden_v2` | 175 | 55 |

Base-state overlap between splits: `{'dev_shadow': 0, 'dev_hidden': 0, 'shadow_hidden': 0}` — required to be zero everywhere (`FM-043`).

Retired as spent: `{'micro_dev': 28, 'micro_shadow': 8, 'micro_hidden': 7}` — FM-043: consumed by the V1 certification top-up; spent as holdouts

## Architectural hypotheses

| Component | Architecture | Screen | Δ vs candidate | Verdict |
|---|---|---|---|---|
| SCOPE | `G_INTERLEAVED_PER_GOAL` | 0.417 | -0.250 | REJECTED_NO_TARGETED_GAIN |
| SCOPE | `G_EXPLICIT_SCOPE_IDS` | 0.750 | 0.083 | HELD_NOT_SEPARATED_FROM_CANDIDATE |
| SCOPE | `G_GOAL_CENTRED_CONTEXT` | 0.750 | 0.083 | HELD_NOT_SEPARATED_FROM_CANDIDATE |
| SCOPE | `G_REDUNDANT_GOAL_ANCHOR` | 0.667 | 0.000 | REJECTED_NO_TARGETED_GAIN |
| EXPRESSION_DEPTH | `E_GRAPH_EDGE_LIST` | 0.167 | 0.000 | REJECTED_NO_TARGETED_GAIN |
| EXPRESSION_DEPTH | `E_HYBRID_NESTED_WITH_EDGES` | 0.167 | 0.000 | REJECTED_NO_TARGETED_GAIN |
| EXPRESSION_DEPTH | `E_DEPENDENCY_LOCAL_SERIAL` | 0.333 | 0.167 | REJECTED_CROSS_COMPONENT_REGRESSION |
| EXPRESSION_DEPTH | `E_HEAD_ONLY_WITH_REMINDERS` | 0.250 | 0.083 | REJECTED_CROSS_COMPONENT_REGRESSION |
