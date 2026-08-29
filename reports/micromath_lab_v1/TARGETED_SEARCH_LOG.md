# Targeted search log — MicroMath Lab V1

Reader `qwen38-rvn:latest`. Elapsed 4175 s (70 min).
Start and end candidate: `R_015b8cd926da` — **no mutation was accepted.**
Preregistered material-improvement threshold: **+0.06** on the targeted cell.
Excluded as saturated before the run: PREMISE.

A cycle picks the weakest cross-domain structure from the failure gradient, proposes single-axis
mutations against a named causal hypothesis, and accepts only on a targeted gain that clears the
threshold without regressing the shadow set.

## Cycles

| Cycle | Component | Axis → value | Before | After | Δ | Verdict | Instrument (certified after) |
|---|---|---|---|---|---|---|---|
| 1 | MULTI_GOAL | `graph_serialization` → `DEPENDENCY_LOCAL` | 0.594 | 0.594 | +0.000 | REJECTED_NO_TARGETED_GAIN | CONTROL_PARITY |
| 1 | MULTI_GOAL | `block_delimiter` → `KEYWORD_END` | 0.594 | 0.562 | -0.031 | REJECTED_NO_TARGETED_GAIN | CONTROL_PARITY |
| 2 | EXPRESSION_DEPTH | `field_marker` → `EQUALS` | 0.500 | 0.500 | +0.000 | REJECTED_NO_TARGETED_GAIN | CONTROL_PARITY |
| 2 | EXPRESSION_DEPTH | `identity_sigil` → `PREFIX_SIGIL` | 0.500 | 0.500 | +0.000 | REJECTED_NO_TARGETED_GAIN | CONTROL_PARITY |
| 2 | EXPRESSION_DEPTH | `syntax_family` → `JSONISH` | 0.500 | 0.500 | +0.000 | REJECTED_NO_TARGETED_GAIN | CONTROL_PARITY |
| 3 | DEPENDENCY | `expression_notation` → `POSTFIX_RPN` | 0.625 | 0.688 | +0.062 | REJECTED_REGRESSION | INSTRUMENT_INVALID |
| 3 | DEPENDENCY | `count_assertions` → `PER_BLOCK` | 0.625 | 0.656 | +0.031 | REJECTED_NO_TARGETED_GAIN | INSTRUMENT_INVALID |

## Hypotheses tested

- **graph_serialization** — changing graph_serialization from DFS_PREORDER improves max_reference_span_tokens on this corpus → *delta +0.000 below the preregistered 0.06*
- **block_delimiter** — changing block_delimiter from None improves detect_drop_line on this corpus → *delta -0.031 below the preregistered 0.06*
- **field_marker** — changing field_marker from None improves bpe_tokens_per_transition on this corpus → *delta +0.000 below the preregistered 0.06*
- **identity_sigil** — changing identity_sigil from None improves identifier_fragmentation on this corpus → *delta +0.000 below the preregistered 0.06*
- **syntax_family** — a JSONISH syntax may provide a more concise and accurate representation of expression depth → *delta +0.000 below the preregistered 0.06*
- **expression_notation** — changing expression_notation from None improves bpe_tokens_per_transition on this corpus → *worst regression -0.250*
- **count_assertions** — changing count_assertions from None improves detect_drop_line on this corpus → *delta +0.031 below the preregistered 0.06*

## Reading, after calibration

Seven mutations, zero accepted, total absolute movement 0.124 across all seven.

**Five rejections stand and are interpretable.** Cycles 1 and 2 ran against MULTI_GOAL and
EXPRESSION_DEPTH, both later certified `CONTROL_PARITY` — valid instruments with a 0.458
dynamic range. The instrument was capable of registering an improvement and registered none.
Those five are therefore `WRONG_CAUSAL_HYPOTHESIS`, not `UNMEASURABLE`: serialisation order,
block delimiters, field markers, identity sigils and syntax family do not move structural
readability. Five of five surface-syntax hypotheses moved a combined 0.031.

**Two rejections are void, and one of them was rejected twice over by broken instruments.**
Cycle 3 ran against DEPENDENCY, later certified `INSTRUMENT_INVALID` (negative arm 0.792).

`expression_notation=POSTFIX_RPN` was the only mutation in the whole log to clear the
preregistered +0.06 threshold, at +0.062. It was rejected on a shadow regression — worst cell
−0.250, on **BINDER**, which is itself certified `INSTRUMENT_LIMIT` with a dynamic range of
0.167. So a gain measured on an invalid instrument was overruled by a regression measured on an
unusable one. That verdict carries no information in either direction.

`count_assertions=PER_BLOCK` showed +0.031 on the same invalid instrument.

Both hypotheses remain **untested**, not refuted, and must be re-run once the DEPENDENCY
instrument is repaired and the regression guard is restricted to calibrated-valid cells.

The most useful thing this log now says is negative and specific: **the axes the representation
compiler exposes at the surface level are not the axes that control machine readability of
multi-goal and expression-depth structure.** Every axis tried was cosmetic. The 0.375–0.417 of
unclaimed dynamic range is untouched by all of them.

Machine-readable source: `TARGETED_SEARCH.json`.
