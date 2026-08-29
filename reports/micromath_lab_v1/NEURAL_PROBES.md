# Neural probes — MicroMath Lab V1

Split `micro_dev`: 29 pairs / 58 items. Chance = 0.500. Both readers local, £0 incremental.
Sequential stopping ladder 20 → 40 → 58.

## Aggregate accuracy, both readers

| Representation | qwen38-rvn | gemma3:4b |
|---|---|---|
| `OLD_HML` | 0.741 | 0.569 |
| `R_015b8cd926da` *(candidate)* | 0.741 | 0.586 |
| `TYPED_AST` | 0.741 | 0.569 |
| `R_bbfdfa5a9249` | 0.724 | 0.569 |
| `R_21f62bd82c7e` | 0.707 | 0.534 |
| `R_a7ef0cd3b92e` | 0.707 | 0.569 |
| `R_159628756bc5` | 0.690 | 0.500 |
| `R_fcd13f8d56a5` | 0.672 | 0.603 |
| `R_03812c646290` | 0.655 | 0.483 |
| `STRUCTURED_ENGLISH` | 0.603 | 0.517 |
| `LEAN_LIKE` | 0.552 | 0.448 |

## The same probe, split by certification status

This is the table that matters. The aggregate above mixes measurements from instruments that
were later shown not to measure the relation they are named after.

| Stress | Certification | candidate | TYPED_AST | OLD_HML | LEAN_LIKE |
|---|---|---|---|---|---|
| EXPRESSION_DEPTH | CONTROL_PARITY | 0.500 | 0.500 | 0.625 | 0.250 |
| MULTI_GOAL | CONTROL_PARITY | 0.500 | 0.500 | 0.667 | 0.500 |
| ACTION_ARGUMENT | INSTRUMENT_LIMIT | 0.625 | 0.625 | 0.625 | 0.625 |
| BINDER | INSTRUMENT_LIMIT | 0.625 | 0.625 | 0.500 | 0.250 |
| DEPENDENCY | INSTRUMENT_INVALID | 0.875 | 1.000 | 0.875 | 0.375 |
| PREMISE | INSTRUMENT_INVALID | 1.000 | 1.000 | 1.000 | 1.000 |
| SCOPE | INSTRUMENT_INVALID | 0.750 | 0.750 | 0.750 | 0.500 |
| TYPE | INSTRUMENT_INVALID | 1.000 | 0.875 | 0.875 | 0.875 |

## Decomposition of the candidate's headline number

| | items | accuracy |
|---|---|---|
| overall | 58 | **0.741** |
| calibrated-valid stresses only | 14 | **0.500** |
| invalid / limited stresses | 44 | **0.818** |

The previously reported 0.741 is an average over four cells that are answerable with the
target relation destroyed and two the reader cannot do at all. On the two cells that survive
calibration the candidate scores chance, and so does every control.

`LEAN_LIKE` (0.552) and `STRUCTURED_ENGLISH` (0.603) remain the two lowest-scoring
representations under qwen — the most human-readable controls are the least machine-readable —
but that ordering is drawn from the same contaminated aggregate and should not be relied on.

Machine-readable sources: `PROBE_micro_dev_qwen38-rvn_latest.json`,
`PROBE_micro_dev_gemma3_4b.json`.
