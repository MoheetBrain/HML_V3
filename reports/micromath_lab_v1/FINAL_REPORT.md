# MicroMath Lab V1 — final report

Status: **complete for the components it could measure; zero components certified.**
Reader: `qwen38-rvn:latest` (local, £0 incremental). Second reader: `gemma3:4b`.
Candidate under test: `R_015b8cd926da`, the strongest finalist of the converged search
(generation 106). `SEALED_FINAL_V2` was never read, never loaded, and never used to build
any part of this lab.

## 1. The headline

The lab was built to find *which* structural relation the discovered representation reads
badly, so that a surgical fix could be attempted before any further global search.

It found something more basic. **Six of the eight instruments do not measure what they claim
to measure**, and on the two that do, the discovered representation and every hand-written
control are statistically indistinguishable and both sit near the floor.

## 2. The retroactive correction

The earlier neural probe reported the candidate at **0.741**, tying `TYPED_AST` and `OLD_HML`,
with nine of eleven representations above chance under Bonferroni correction. That number
does not survive calibration.

| | items | candidate accuracy |
|---|---|---|
| overall (as previously reported) | 58 | **0.741** |
| on the two calibrated-valid instruments | 14 | **0.500** |
| on the six invalid / limited instruments | 44 | 0.818 |

**75.9 % of the items behind the 0.741 headline came from instruments now known to be
invalid or limited.** The apparent above-chance performance was carried by PREMISE (1.000),
TYPE (1.000) and DEPENDENCY (0.875) — the three cells whose negative arms score 0.875, 0.833
and 0.792 respectively, i.e. cells that are answerable with the relation destroyed.

On the two cells that survive calibration, the candidate scores exactly chance.

I reported 0.741 as a measurement of readability. It was not one. This report supersedes that
reading.

## 3. Why four instruments are invalid

The pairs are matched **transposition counterfactuals**: state B is a permutation of state A,
so the token multiset is identical by construction. That controls for length, vocabulary and
surface frequency — and the per-stress shortcut audit confirms no positional or frequency
heuristic beats 0.51 on any cell.

It does not control for **semantic plausibility**. A transposed pair can still be told apart by
"which assignment makes sense": `n : Nat` is recoverable from the name alone, a premise about
measurability attaches to the measurable object, a declaration's type is guessable from its
identifier. The reader answers those four questions from mathematical priors carried in the
identifiers, not from the structure of the notation — which is exactly why prepending a decoy
answer fails to move it.

Token-multiset equality is a weaker control than it appears. This is recorded as FM-041.

## 4. What the two valid instruments say

| | MULTI_GOAL | EXPRESSION_DEPTH |
|---|---|---|
| relation stated outright | 0.958 | 0.917 |
| relation destroyed | 0.500 | 0.458 |
| best hand-written control | 0.583 | 0.500 |
| discovered candidate | 0.583 | 0.500 |
| normalised readability | 0.182 | 0.091 |

Both instruments are unambiguously valid — near-ceiling when the answer is stated, exactly at
chance when the relation is destroyed. Both show the candidate at parity with the control, and
both leave **0.375 and 0.417 of dynamic range that no representation reaches.**

This is a real, measured, negative result about the discovered language: on the structural
relations we can actually test, it buys nothing over a plain typed AST. It is also a real
result about the controls: they buy nothing either.

## 5. What this does to the seven rejected mutations

Three surgical cycles proposed seven mutations; all seven were rejected. Calibration splits
them:

| Cycle | Component | Mutation | Δ | Now reads as |
|---|---|---|---|---|
| 1 | MULTI_GOAL | `graph_serialization=DEPENDENCY_LOCAL` | +0.000 | WRONG_CAUSAL_HYPOTHESIS |
| 1 | MULTI_GOAL | `block_delimiter=KEYWORD_END` | −0.031 | WRONG_CAUSAL_HYPOTHESIS |
| 2 | EXPRESSION_DEPTH | `field_marker=EQUALS` | +0.000 | WRONG_CAUSAL_HYPOTHESIS |
| 2 | EXPRESSION_DEPTH | `identity_sigil=PREFIX_SIGIL` | +0.000 | WRONG_CAUSAL_HYPOTHESIS |
| 2 | EXPRESSION_DEPTH | `syntax_family=JSONISH` | +0.000 | WRONG_CAUSAL_HYPOTHESIS |
| 3 | DEPENDENCY | `expression_notation=POSTFIX_RPN` | +0.062 | **VOID** — invalid instrument |
| 3 | DEPENDENCY | `count_assertions=PER_BLOCK` | +0.031 | **VOID** — invalid instrument |

Five rejections stand and are now interpretable: the instrument was working, the mutation
genuinely did not help, and the causal hypothesis behind it was wrong. Surface syntax —
delimiters, sigils, field markers, serialisation order, JSON-vs-bespoke — does not move
multi-goal or expression-depth readability at all. Five of five surface-level hypotheses
produced a total absolute change of 0.031.

Two rejections are void: they were measured against a broken instrument and carry no
information either way. `expression_notation=POSTFIX_RPN` in particular showed +0.062 on the
targeted metric and must not be read as either a success or a failure.

## 6. What was not attempted

Stated plainly, against the 36 sections of the mission:

- **§16 PREMISE_V2** — not built. PREMISE is confirmed saturated (positive = negative = 0.875);
  the redesign to four choices with plausible distractors is specified but unimplemented.
- **§17–19 the E / D / G ladders** — not started. The five-rung ladders for EXPRESSION_DEPTH,
  DEPENDENCY and MULTI_GOAL were superseded in priority by calibration, which then showed that
  the D ladder would have run on an invalid instrument.
- **§21–22 integration matrix** — not started.
- **§23 reasoning ladder** — not started.
- **Three unpopulated cells** — GEOMETRY×SCOPE, LINEAR_ALGEBRA×SCOPE, LINEAR_ALGEBRA×MULTI_GOAL
  remain corpus-acquisition requests; 45 of 48 cells are populated.
- **`micro_hidden` and `micro_shadow`** — **contaminated, not reserved (FM-043).** The
  certification topped each component from `micro_dev`'s 2–4 pairs up to 12 by minting fresh
  pairs from the V2 pool, and its exclusion set covered `micro_dev` only. It consumed all 8
  base states of `micro_hidden` and all 8 of `micro_shadow`. Nothing was fitted or selected on
  them and no verdict in this report depends on them, but both are spent as clean holdouts and
  **no generalisation claim can be made**. The cause is fixed and verified; the pool was always
  deep enough to reach 12 pairs per component with zero overlap. I stated in a draft of this
  report that both splits were untouched; that was wrong, and I withdrew it after checking the
  identifiers rather than the intent.
- **`TARGET_HOLDOUT`** — correctly untouched. It is gated on a component appearing certified,
  and none did.

## 7. What the mission asked, and the answer

> "Build the robot one body part at a time."

Eight body parts were put on the bench. Six of the eight test rigs turned out to be broken, and
the two working rigs report that the part performs exactly as well as the off-the-shelf part,
and that both are running at under a fifth of the achievable range.

The correct next action is therefore **not** another mutation cycle and **not** a global search.
It is to repair the instruments — because five of the six failures are repairable and the
project currently has no valid way to measure six of the eight relations it cares about.

## 8. Exact next actions

1. **Rebuild the four invalid instruments so the answer is not recoverable from identifiers.**
   Anonymise or type-neutralise identifiers within a pair, or replace the 2-choice format with
   4 choices whose distractors are equally plausible under the same priors. Re-run calibration;
   an instrument is only usable once its negative arm returns to chance.
2. **Retire ACTION_ARGUMENT and BINDER for this reader** or move them to a stronger local
   reader. A positive arm of 0.542 is not a measurement.
3. **Re-run the DEPENDENCY cycle** once its instrument is valid — the two void mutations are
   untested, not refuted.
4. **Attack the 0.375 / 0.417 headroom with structural, not surface, hypotheses.** The five
   surface mutations that were properly tested moved nothing. The open question is what
   *does* move multi-goal readability, and no tested axis has yet done so.
5. **Mint a fresh holdout.** `micro_hidden` and `micro_shadow` are spent; excluding them from
   future runs no longer makes them clean. Build a new reserved split from base states used by
   no prior run, and gate it behind an actual certification.
6. Leave `SEALED_FINAL_V2` and `TARGET_HOLDOUT` alone.

## 9. Falsification status

Per `PROJECT_GOAL.md` §18, the project's central claim is that a discovered representation can
be made measurably more readable to a model than existing notations. **That claim is not
supported by any evidence in this report.** On every instrument that survives calibration, the
discovered representation is at parity with a plain typed AST. This is the strongest negative
evidence the project has produced to date, and it was produced at zero incremental cost.
