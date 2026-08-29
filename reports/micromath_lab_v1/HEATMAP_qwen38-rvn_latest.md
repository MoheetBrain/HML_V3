# MicroMath Lab V1 — heatmap (qwen38-rvn:latest, micro_dev)

Cells are `accuracy (delta vs best control)`. Chance is 0.50 by construction: every item is a 2-alternative forced choice over a matched transposition. `—` marks a cell the corpus could not populate.

## `R_015b8cd926da` (FINALIST)

| stress | ALGEBRA | GEOMETRY | CALCULUS_ | PROBABILI | LOGIC_SET | LINEAR_AL |
|---|---|---|---|---|---|---|
| `BINDER` | 0.50 (+0.00) | 1.00 (+0.00) | — | 0.50 (+0.00) | 0.50 (+0.00) | — |
| `SCOPE` | — | — | 0.50 (+0.00) | — | 1.00 (+0.00) | — |
| `DEPENDENCY` | — | 1.00 (+0.00) | 1.00 (+0.00) | 0.50 (-0.50) | 1.00 (+0.00) | — |
| `TYPE` | 1.00 (+0.00) | 1.00 (+0.00) | 1.00 (+0.00) | — | 1.00 (+0.00) | — |
| `MULTI_GOAL` | 0.50 (+0.00) | 0.50 (-0.50) | — | 0.50 (+0.00) | — | — |
| `EXPRESSION_DEPTH` | 0.50 (+0.00) | 0.50 (+0.00) | 0.50 (+0.00) | 0.50 (-0.50) | — | — |
| `PREMISE` | — | 1.00 (+0.00) | 1.00 (+0.00) | 1.00 (+0.00) | — | 1.00 (+0.00) |
| `ACTION_ARGUMENT` | — | 0.50 (+0.00) | — | 0.50 (+0.00) | 1.00 (+0.00) | 0.50 (+0.00) |

Worst structure: **MULTI_GOAL**. Cross-domain structural gaps: none.

## `R_03812c646290` (FINALIST)

| stress | ALGEBRA | GEOMETRY | CALCULUS_ | PROBABILI | LOGIC_SET | LINEAR_AL |
|---|---|---|---|---|---|---|
| `BINDER` | 0.50 (+0.00) | 1.00 (+0.00) | — | 0.50 (+0.00) | 0.50 (+0.00) | — |
| `SCOPE` | — | — | 0.50 (+0.00) | — | 1.00 (+0.00) | — |
| `DEPENDENCY` | — | 1.00 (+0.00) | 1.00 (+0.00) | 0.50 (-0.50) | 0.50 (-0.50) | — |
| `TYPE` | 0.50 (-0.50) | 1.00 (+0.00) | 0.50 (-0.50) | — | 0.50 (-0.50) | — |
| `MULTI_GOAL` | 0.50 (+0.00) | 0.50 (-0.50) | — | 0.50 (+0.00) | — | — |
| `EXPRESSION_DEPTH` | 0.50 (+0.00) | 1.00 (+0.50) | 0.50 (+0.00) | 0.50 (-0.50) | — | — |
| `PREMISE` | — | 1.00 (+0.00) | 1.00 (+0.00) | 1.00 (+0.00) | — | 1.00 (+0.00) |
| `ACTION_ARGUMENT` | — | 0.50 (+0.00) | — | 0.00 (-0.50) | 0.50 (-0.50) | 0.50 (+0.00) |

Worst structure: **TYPE**. Cross-domain structural gaps: ['TYPE', 'DEPENDENCY', 'ACTION_ARGUMENT'].

## `R_159628756bc5` (FINALIST)

| stress | ALGEBRA | GEOMETRY | CALCULUS_ | PROBABILI | LOGIC_SET | LINEAR_AL |
|---|---|---|---|---|---|---|
| `BINDER` | 0.50 (+0.00) | 0.50 (-0.50) | — | 0.50 (+0.00) | 0.50 (+0.00) | — |
| `SCOPE` | — | — | 0.50 (+0.00) | — | 1.00 (+0.00) | — |
| `DEPENDENCY` | — | 1.00 (+0.00) | 1.00 (+0.00) | 0.50 (-0.50) | 1.00 (+0.00) | — |
| `TYPE` | 1.00 (+0.00) | 1.00 (+0.00) | 1.00 (+0.00) | — | 0.50 (-0.50) | — |
| `MULTI_GOAL` | 0.50 (+0.00) | 0.50 (-0.50) | — | 0.50 (+0.00) | — | — |
| `EXPRESSION_DEPTH` | 0.50 (+0.00) | 0.50 (+0.00) | 0.50 (+0.00) | 1.00 (+0.00) | — | — |
| `PREMISE` | — | 1.00 (+0.00) | 1.00 (+0.00) | 1.00 (+0.00) | — | 1.00 (+0.00) |
| `ACTION_ARGUMENT` | — | 0.50 (+0.00) | — | 0.00 (-0.50) | 0.50 (-0.50) | 0.50 (+0.00) |

Worst structure: **ACTION_ARGUMENT**. Cross-domain structural gaps: ['ACTION_ARGUMENT'].

## `R_21f62bd82c7e` (FINALIST)

| stress | ALGEBRA | GEOMETRY | CALCULUS_ | PROBABILI | LOGIC_SET | LINEAR_AL |
|---|---|---|---|---|---|---|
| `BINDER` | 0.50 (+0.00) | 0.50 (-0.50) | — | 0.50 (+0.00) | 0.50 (+0.00) | — |
| `SCOPE` | — | — | 0.50 (+0.00) | — | 1.00 (+0.00) | — |
| `DEPENDENCY` | — | 1.00 (+0.00) | 1.00 (+0.00) | 0.50 (-0.50) | 1.00 (+0.00) | — |
| `TYPE` | 1.00 (+0.00) | 1.00 (+0.00) | 1.00 (+0.00) | — | 0.50 (-0.50) | — |
| `MULTI_GOAL` | 0.50 (+0.00) | 0.50 (-0.50) | — | 0.50 (+0.00) | — | — |
| `EXPRESSION_DEPTH` | 0.50 (+0.00) | 1.00 (+0.50) | 0.50 (+0.00) | 0.50 (-0.50) | — | — |
| `PREMISE` | — | 1.00 (+0.00) | 1.00 (+0.00) | 1.00 (+0.00) | — | 1.00 (+0.00) |
| `ACTION_ARGUMENT` | — | 0.50 (+0.00) | — | 0.50 (+0.00) | 0.50 (-0.50) | 0.50 (+0.00) |

Worst structure: **MULTI_GOAL**. Cross-domain structural gaps: none.

## `R_a7ef0cd3b92e` (FINALIST)

| stress | ALGEBRA | GEOMETRY | CALCULUS_ | PROBABILI | LOGIC_SET | LINEAR_AL |
|---|---|---|---|---|---|---|
| `BINDER` | 0.50 (+0.00) | 0.50 (-0.50) | — | 0.50 (+0.00) | 0.50 (+0.00) | — |
| `SCOPE` | — | — | 0.50 (+0.00) | — | 1.00 (+0.00) | — |
| `DEPENDENCY` | — | 1.00 (+0.00) | 0.50 (-0.50) | 0.50 (-0.50) | 0.50 (-0.50) | — |
| `TYPE` | 1.00 (+0.00) | 1.00 (+0.00) | 1.00 (+0.00) | — | 0.50 (-0.50) | — |
| `MULTI_GOAL` | 0.50 (+0.00) | 1.00 (+0.00) | — | 0.50 (+0.00) | — | — |
| `EXPRESSION_DEPTH` | 0.50 (+0.00) | 1.00 (+0.50) | 0.50 (+0.00) | 0.50 (-0.50) | — | — |
| `PREMISE` | — | 1.00 (+0.00) | 1.00 (+0.00) | 1.00 (+0.00) | — | 1.00 (+0.00) |
| `ACTION_ARGUMENT` | — | 0.50 (+0.00) | — | 0.50 (+0.00) | 1.00 (+0.00) | 0.50 (+0.00) |

Worst structure: **DEPENDENCY**. Cross-domain structural gaps: ['DEPENDENCY'].

## `R_bbfdfa5a9249` (FINALIST)

| stress | ALGEBRA | GEOMETRY | CALCULUS_ | PROBABILI | LOGIC_SET | LINEAR_AL |
|---|---|---|---|---|---|---|
| `BINDER` | 0.50 (+0.00) | 1.00 (+0.00) | — | 0.50 (+0.00) | 1.00 (+0.50) | — |
| `SCOPE` | — | — | 0.50 (+0.00) | — | 1.00 (+0.00) | — |
| `DEPENDENCY` | — | 0.50 (-0.50) | 1.00 (+0.00) | 0.50 (-0.50) | 1.00 (+0.00) | — |
| `TYPE` | 1.00 (+0.00) | 1.00 (+0.00) | 0.50 (-0.50) | — | 1.00 (+0.00) | — |
| `MULTI_GOAL` | 0.50 (+0.00) | 0.00 (-1.00) | — | 0.50 (+0.00) | — | — |
| `EXPRESSION_DEPTH` | 0.50 (+0.00) | 1.00 (+0.50) | 0.50 (+0.00) | 1.00 (+0.00) | — | — |
| `PREMISE` | — | 1.00 (+0.00) | 1.00 (+0.00) | 1.00 (+0.00) | — | 1.00 (+0.00) |
| `ACTION_ARGUMENT` | — | 0.50 (+0.00) | — | 0.00 (-0.50) | 1.00 (+0.00) | 0.50 (+0.00) |

Worst structure: **DEPENDENCY**. Cross-domain structural gaps: ['DEPENDENCY'].

## `R_fcd13f8d56a5` (FINALIST)

| stress | ALGEBRA | GEOMETRY | CALCULUS_ | PROBABILI | LOGIC_SET | LINEAR_AL |
|---|---|---|---|---|---|---|
| `BINDER` | 0.50 (+0.00) | 0.50 (-0.50) | — | 0.50 (+0.00) | 0.50 (+0.00) | — |
| `SCOPE` | — | — | 0.50 (+0.00) | — | 1.00 (+0.00) | — |
| `DEPENDENCY` | — | 0.50 (-0.50) | 1.00 (+0.00) | 0.50 (-0.50) | 1.00 (+0.00) | — |
| `TYPE` | 1.00 (+0.00) | 0.50 (-0.50) | 1.00 (+0.00) | — | 0.50 (-0.50) | — |
| `MULTI_GOAL` | 0.50 (+0.00) | 0.50 (-0.50) | — | 0.50 (+0.00) | — | — |
| `EXPRESSION_DEPTH` | 0.50 (+0.00) | 1.00 (+0.50) | 0.50 (+0.00) | 0.50 (-0.50) | — | — |
| `PREMISE` | — | 1.00 (+0.00) | 1.00 (+0.00) | 1.00 (+0.00) | — | 1.00 (+0.00) |
| `ACTION_ARGUMENT` | — | 0.50 (+0.00) | — | 0.50 (+0.00) | 0.50 (-0.50) | 0.50 (+0.00) |

Worst structure: **DEPENDENCY**. Cross-domain structural gaps: ['DEPENDENCY', 'TYPE'].

## `LEAN_LIKE` (CONTROL)

| stress | ALGEBRA | GEOMETRY | CALCULUS_ | PROBABILI | LOGIC_SET | LINEAR_AL |
|---|---|---|---|---|---|---|
| `BINDER` | 0.50 (+0.00) | 0.50 (-0.50) | — | 0.00 (-0.50) | 0.00 (-0.50) | — |
| `SCOPE` | — | — | 0.50 (+0.00) | — | 0.50 (-0.50) | — |
| `DEPENDENCY` | — | 0.00 (-1.00) | 0.00 (-1.00) | 0.50 (-0.50) | 1.00 (+0.00) | — |
| `TYPE` | 1.00 (+0.00) | 0.50 (-0.50) | 1.00 (+0.00) | — | 1.00 (+0.00) | — |
| `MULTI_GOAL` | 0.50 (+0.00) | 0.50 (-0.50) | — | 0.50 (+0.00) | — | — |
| `EXPRESSION_DEPTH` | 0.50 (+0.00) | 0.00 (-0.50) | 0.50 (+0.00) | 0.00 (-1.00) | — | — |
| `PREMISE` | — | 1.00 (+0.00) | 1.00 (+0.00) | 1.00 (+0.00) | — | 1.00 (+0.00) |
| `ACTION_ARGUMENT` | — | 0.50 (+0.00) | — | 0.50 (+0.00) | 1.00 (+0.00) | 0.50 (+0.00) |

Worst structure: **DEPENDENCY**. Cross-domain structural gaps: ['DEPENDENCY', 'BINDER', 'EXPRESSION_DEPTH'].

## `OLD_HML` (CONTROL)

| stress | ALGEBRA | GEOMETRY | CALCULUS_ | PROBABILI | LOGIC_SET | LINEAR_AL |
|---|---|---|---|---|---|---|
| `BINDER` | 0.50 (+0.00) | 0.50 (-0.50) | — | 0.50 (+0.00) | 0.50 (+0.00) | — |
| `SCOPE` | — | — | 0.50 (+0.00) | — | 1.00 (+0.00) | — |
| `DEPENDENCY` | — | 1.00 (+0.00) | 1.00 (+0.00) | 0.50 (-0.50) | 1.00 (+0.00) | — |
| `TYPE` | 1.00 (+0.00) | 1.00 (+0.00) | 1.00 (+0.00) | — | 0.50 (-0.50) | — |
| `MULTI_GOAL` | 0.50 (+0.00) | 1.00 (+0.00) | — | 0.50 (+0.00) | — | — |
| `EXPRESSION_DEPTH` | 0.50 (+0.00) | 0.50 (+0.00) | 0.50 (+0.00) | 1.00 (+0.00) | — | — |
| `PREMISE` | — | 1.00 (+0.00) | 1.00 (+0.00) | 1.00 (+0.00) | — | 1.00 (+0.00) |
| `ACTION_ARGUMENT` | — | 0.50 (+0.00) | — | 0.50 (+0.00) | 1.00 (+0.00) | 0.50 (+0.00) |

Worst structure: **BINDER**. Cross-domain structural gaps: none.

## `STRUCTURED_ENGLISH` (CONTROL)

| stress | ALGEBRA | GEOMETRY | CALCULUS_ | PROBABILI | LOGIC_SET | LINEAR_AL |
|---|---|---|---|---|---|---|
| `BINDER` | 0.50 (+0.00) | 0.50 (-0.50) | — | 0.50 (+0.00) | 0.00 (-0.50) | — |
| `SCOPE` | — | — | 0.50 (+0.00) | — | 0.50 (-0.50) | — |
| `DEPENDENCY` | — | 0.50 (-0.50) | 0.50 (-0.50) | 1.00 (+0.00) | 0.50 (-0.50) | — |
| `TYPE` | 1.00 (+0.00) | 0.50 (-0.50) | 1.00 (+0.00) | — | 0.50 (-0.50) | — |
| `MULTI_GOAL` | 0.50 (+0.00) | 0.50 (-0.50) | — | 0.50 (+0.00) | — | — |
| `EXPRESSION_DEPTH` | 0.50 (+0.00) | 0.00 (-0.50) | 0.50 (+0.00) | 0.50 (-0.50) | — | — |
| `PREMISE` | — | 1.00 (+0.00) | 1.00 (+0.00) | 1.00 (+0.00) | — | 1.00 (+0.00) |
| `ACTION_ARGUMENT` | — | 0.50 (+0.00) | — | 0.50 (+0.00) | 1.00 (+0.00) | 0.50 (+0.00) |

Worst structure: **DEPENDENCY**. Cross-domain structural gaps: ['DEPENDENCY', 'BINDER', 'TYPE', 'EXPRESSION_DEPTH'].

## `TYPED_AST` (CONTROL)

| stress | ALGEBRA | GEOMETRY | CALCULUS_ | PROBABILI | LOGIC_SET | LINEAR_AL |
|---|---|---|---|---|---|---|
| `BINDER` | 0.50 (+0.00) | 1.00 (+0.00) | — | 0.50 (+0.00) | 0.50 (+0.00) | — |
| `SCOPE` | — | — | 0.50 (+0.00) | — | 1.00 (+0.00) | — |
| `DEPENDENCY` | — | 1.00 (+0.00) | 1.00 (+0.00) | 1.00 (+0.00) | 1.00 (+0.00) | — |
| `TYPE` | 1.00 (+0.00) | 1.00 (+0.00) | 1.00 (+0.00) | — | 0.50 (-0.50) | — |
| `MULTI_GOAL` | 0.50 (+0.00) | 0.50 (-0.50) | — | 0.50 (+0.00) | — | — |
| `EXPRESSION_DEPTH` | 0.50 (+0.00) | 0.50 (+0.00) | 0.50 (+0.00) | 0.50 (-0.50) | — | — |
| `PREMISE` | — | 1.00 (+0.00) | 1.00 (+0.00) | 1.00 (+0.00) | — | 1.00 (+0.00) |
| `ACTION_ARGUMENT` | — | 0.50 (+0.00) | — | 0.50 (+0.00) | 1.00 (+0.00) | 0.50 (+0.00) |

Worst structure: **MULTI_GOAL**. Cross-domain structural gaps: none.

## Saturation

`MICROMATH §33`: a saturated column is reported and must not guide selection.

| stress | verdict |
|---|---|
| `BINDER` | DISCRIMINATIVE |
| `SCOPE` | DISCRIMINATIVE |
| `DEPENDENCY` | DISCRIMINATIVE |
| `TYPE` | DISCRIMINATIVE |
| `MULTI_GOAL` | DISCRIMINATIVE |
| `EXPRESSION_DEPTH` | DISCRIMINATIVE |
| `PREMISE` | SATURATED |
| `ACTION_ARGUMENT` | DISCRIMINATIVE |
