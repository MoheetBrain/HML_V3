# Formal Source Acquisition V1

All checkouts are ignored local evidence under `external/checkouts/`. The committed authority is `data/manifests/formal_sources.json` plus deterministic acquisition scripts; no external repository was vendored or modified.

| Source | Exact identity | Local result | License/use decision |
|---|---|---|---|
| Mathlib for LeanDojo Benchmark 4 | `29dcec074de168ac2bf835a77ef68bbe069194c5`, Lean `v4.10.0-rc1` | clean checkout; 4,835 non-Git files; tree receipt `7b9014f4…` | Apache-2.0 Mathlib; primary trajectory environment |
| LeanDojo V2 | `baed5eae6e87a65a446d9f54af07aab2154e7599`, package 1.0.9 | clean checkout; 98 files; tree receipt `16b500c3…` | MIT; tooling viability only, not substituted for legacy 2.0.0 replay evidence |
| Lean Workbook | `2e066e310b2c6d2c27616927ae131f82901c8f1c` | clean metadata-only checkout; LFS skipped; tree receipt `0c60fadc…` | Apache-2.0; Tier B pending payload acquisition and replay |
| miniF2F Lean 4 | `f0a20e14c1eeccd859d51bb4c2b3ee487889c303`, Lean `v4.27.0`, Mathlib `a3a10db0…` | clean checkout; 13 files; tree receipt `dc919de0…` | Apache-2.0; evaluation-only; statements mostly contain `sorry`/`admit` |
| ProofNet Lean 4 community port | `5da820b6510cd2a1d4237036d8227357cb9944d9`, Lean `v4.27.0`, Mathlib `a3a10db0…` | clean checkout; 10 files; tree receipt `35be2f51…` | MIT; 371 rows per README, evaluation-only, theorem bodies remain `sorry` |

The ignored receipts contain acquisition timestamps, absolute local paths, full exact commits, file/byte counts, and tree fingerprints. Re-running a script verifies origin, fetches the exact commit, detaches HEAD, refuses a dirty checkout, and emits a new local receipt.

## Primary source decision

`LEAN_PIPELINE_V1` remains on LeanDojo Benchmark 4 / Mathlib `29dcec…` because a 241,265-transition local trace and Stage100 replay evidence already exist at that exact environment. Newer LeanDojo V2 is separately pinned, not silently mixed into those claims.

The pipeline joins each selected transition back to the official Benchmark 4 random split. Exact tactic, before-state, and after-state equality are required. Official annotated premise records and the theorem declaration/proof from `corpus.jsonl` are then retained with hashes. All 1,000 joins passed.
