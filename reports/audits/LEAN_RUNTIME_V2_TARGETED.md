# Lean Runtime V2 Canonical Corpus Audit

Selected transitions: **1125**. Recovered into the canonical corpus: **542**. Unrecovered: **583**.

## Campaign process status

| Status | Jobs |
|---|---|
| `PROCESS_FAIL` | 3 |
| `PROCESS_PASS` | 652 |

## Capture accounting

| Counter | Value |
|---|---|
| `captures_duplicate_record_id` | 69 |
| `captures_kept` | 542 |
| `captures_over_element_budget` | 164 |
| `captures_over_size_budget` | 399 |
| `captures_read` | 1174 |
| `files_truncated` | 1 |

Transitions whose canonical JSON exceeds the declared 262144-byte budget are excluded and counted; they are not silently dropped and not truncated.

## Canonical size distribution

| Canonical bytes | Transitions |
|---|---|
| <=4KiB | 0 |
| <=16KiB | 0 |
| <=64KiB | 33 |
| <=256KiB | 509 |
| <=1MiB | 316 |
| >1MiB | 247 |

## Raw files that did not read cleanly

| Raw file | Bytes | Status | Captures recovered before the defect |
|---|---|---|---|
| `campaign_targeted/0085.json` | 369,076,952 | `TRUNCATED` | 1 |

## Domain coverage of the recovered corpus

| Mathlib domain | Transitions |
|---|---|
| `MeasureTheory` | 68 |
| `Data` | 67 |
| `Analysis` | 65 |
| `Algebra` | 58 |
| `Topology` | 41 |
| `SetTheory` | 38 |
| `NumberTheory` | 31 |
| `Order` | 29 |
| `RingTheory` | 27 |
| `Computability` | 25 |
| `LinearAlgebra` | 15 |
| `Combinatorics` | 14 |
| `GroupTheory` | 11 |
| `CategoryTheory` | 10 |
| `Geometry` | 9 |
| `Probability` | 9 |
| `Dynamics` | 5 |
| `FieldTheory` | 5 |
| `Init` | 5 |
| `ModelTheory` | 4 |
| `AlgebraicGeometry` | 3 |
| `Logic` | 2 |
| `Tactic` | 1 |
