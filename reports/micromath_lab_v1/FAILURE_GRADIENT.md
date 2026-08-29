# Failure gradient — MicroMath Lab V1

Reader `qwen38-rvn:latest`, split `micro_dev`, candidate `R_015b8cd926da`.
Machine-readable sources: `heatmap_qwen38-rvn_latest.json`, `heatmap_gemma3_4b.json`.
Rendered heatmaps: `HEATMAP_qwen38-rvn_latest.md`, `HEATMAP_gemma3_4b.md`.

MICROMATH §42: a low domain score locates a failure; the structure it shares with other
domains identifies the cause. A domain-specific primitive is never proposed from a single
weak domain.

## Structural ranking as it stood before calibration

| Rank | Stress | Mean acc. | Δ vs best control | Domains | Cross-domain | Certification (after) |
|---|---|---|---|---|---|---|
| 1 | MULTI_GOAL | 0.500 | -0.167 | 3 | no | **CONTROL_PARITY** |
| 2 | DEPENDENCY | 0.875 | -0.125 | 4 | no | **INSTRUMENT_INVALID** |
| 3 | EXPRESSION_DEPTH | 0.500 | -0.125 | 4 | no | **CONTROL_PARITY** |
| 4 | BINDER | 0.625 | +0.000 | 4 | no | **INSTRUMENT_LIMIT** |
| 5 | SCOPE | 0.750 | +0.000 | 2 | no | **INSTRUMENT_INVALID** |
| 6 | TYPE | 1.000 | +0.000 | 4 | no | **INSTRUMENT_INVALID** |
| 7 | PREMISE | 1.000 | +0.000 | 4 | no | **INSTRUMENT_INVALID** |
| 8 | ACTION_ARGUMENT | 0.625 | +0.000 | 4 | no | **INSTRUMENT_LIMIT** |

Recommended next mutation target at the time: **MULTI_GOAL**.

## Domain gradient

| Domain | Mean Δ vs best control |
|---|---|
| ALGEBRA | +0.0000 |
| CALCULUS_ANALYSIS | +0.0000 |
| GEOMETRY | -0.0714 |
| LINEAR_ALGEBRA | +0.0000 |
| LOGIC_SET_THEORY | +0.0000 |
| PROBABILITY_STATISTICS | -0.1667 |

## Reading, after calibration

The gradient was two-thirds right and one-third wasted, and it could not have known which.

Its top pick, **MULTI_GOAL**, is a calibrated-valid cell — cycle 1 was correctly aimed. Rank 3,
**EXPRESSION_DEPTH**, is also valid — cycle 2 was correctly aimed. Rank 2, **DEPENDENCY**, is
`INSTRUMENT_INVALID`: its negative arm scores 0.792, so the −0.125 gap that promoted it was a
difference in how well two representations exploit identifier priors, not a difference in
structural readability. Cycle 3 and its two mutations were spent there and return no
information.

Ranks 4–8 all show Δ +0.000 against the best control. That flat tail is not a finding that the
candidate matches controls on five relations; it is the signature of five cells that are
saturated, invalid or unreadable. The gradient cannot distinguish "no difference" from "no
measurement", because Δ-vs-control is computed identically in both cases.

**A failure gradient computed over uncalibrated cells ranks partly noise, and gives no warning
which entries are which.** Any future gradient must be restricted to cells whose negative arm
sits at chance — which, today, means a ranking of length two.

This is recorded as FM-042.
