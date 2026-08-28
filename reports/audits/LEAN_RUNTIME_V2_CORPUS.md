# Lean Runtime V2 Canonical Corpus Audit

Selected transitions: **1000**. Recovered into the canonical corpus: **608**. Unrecovered: **392**.

## Campaign process status

| Status | Jobs |
|---|---|
| `PROCESS_FAIL` | 7 |
| `PROCESS_PASS` | 744 |

## Capture accounting

| Counter | Value |
|---|---|
| `captures_duplicate_record_id` | 9 |
| `captures_kept` | 608 |
| `captures_over_element_budget` | 96 |
| `captures_over_size_budget` | 272 |
| `captures_read` | 985 |
| `files_truncated` | 1 |

Transitions whose canonical JSON exceeds the declared 262144-byte budget are excluded and counted; they are not silently dropped and not truncated.

## Canonical size distribution

| Canonical bytes | Transitions |
|---|---|
| <=4KiB | 0 |
| <=16KiB | 0 |
| <=64KiB | 63 |
| <=256KiB | 545 |
| <=1MiB | 226 |
| >1MiB | 142 |

## Raw files that did not read cleanly

| Raw file | Bytes | Status | Captures recovered before the defect |
|---|---|---|---|
| `campaign500/0207.json` | 350,795,253 | `TRUNCATED` | 1 |

## Domain coverage of the recovered corpus

| Mathlib domain | Transitions |
|---|---|
| `Data` | 95 |
| `Algebra` | 64 |
| `MeasureTheory` | 51 |
| `Analysis` | 50 |
| `Topology` | 43 |
| `NumberTheory` | 36 |
| `RingTheory` | 36 |
| `Order` | 30 |
| `SetTheory` | 27 |
| `CategoryTheory` | 25 |
| `Combinatorics` | 22 |
| `LinearAlgebra` | 21 |
| `packages` | 19 |
| `Computability` | 17 |
| `GroupTheory` | 14 |
| `Probability` | 13 |
| `Geometry` | 11 |
| `Tactic` | 8 |
| `FieldTheory` | 7 |
| `AlgebraicGeometry` | 6 |
| `Dynamics` | 3 |
| `ModelTheory` | 3 |
| `Init` | 2 |
| `Logic` | 2 |
| `Control` | 1 |
| `Deprecated` | 1 |
| `Testing` | 1 |
