# Lean Runtime V2 Canonical Corpus Audit

Selected transitions: **500**. Recovered into the canonical corpus: **317**. Unrecovered: **183**.

## Campaign process status

| Status | Jobs |
|---|---|
| `PROCESS_FAIL` | 5 |
| `PROCESS_PASS` | 246 |

## Capture accounting

| Counter | Value |
|---|---|
| `captures_duplicate_record_id` | 7 |
| `captures_kept` | 317 |
| `captures_over_element_budget` | 51 |
| `captures_over_size_budget` | 117 |
| `captures_read` | 492 |
| `files_truncated` | 1 |

Transitions whose canonical JSON exceeds the declared 262144-byte budget are excluded and counted; they are not silently dropped and not truncated.

## Canonical size distribution

| Canonical bytes | Transitions |
|---|---|
| <=4KiB | 0 |
| <=16KiB | 0 |
| <=64KiB | 39 |
| <=256KiB | 278 |
| <=1MiB | 106 |
| >1MiB | 62 |

## Raw files that did not read cleanly

| Raw file | Bytes | Status | Captures recovered before the defect |
|---|---|---|---|
| `0207.json` | 350,795,253 | `TRUNCATED` | 1 |

## Domain coverage of the recovered corpus

| Mathlib domain | Transitions |
|---|---|
| `Data` | 59 |
| `Algebra` | 26 |
| `Analysis` | 25 |
| `MeasureTheory` | 21 |
| `Topology` | 21 |
| `NumberTheory` | 20 |
| `SetTheory` | 20 |
| `Computability` | 16 |
| `RingTheory` | 15 |
| `packages` | 15 |
| `CategoryTheory` | 14 |
| `Order` | 13 |
| `LinearAlgebra` | 9 |
| `Combinatorics` | 7 |
| `Geometry` | 7 |
| `AlgebraicGeometry` | 6 |
| `Tactic` | 6 |
| `GroupTheory` | 5 |
| `Probability` | 4 |
| `ModelTheory` | 2 |
| `Deprecated` | 1 |
| `Dynamics` | 1 |
| `FieldTheory` | 1 |
| `Init` | 1 |
| `Logic` | 1 |
| `Testing` | 1 |
