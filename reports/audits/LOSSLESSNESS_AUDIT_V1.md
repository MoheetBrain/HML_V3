# Losslessness Audit V1

**Status: PASS.** V3 is lossless for the declared observable boundary across 1,000 real Lean transitions.

| Check | Result |
|---|---:|
| Exact source/canonical transition pairs | 1,000 |
| Exact raw states checked | 2,000 |
| Exact raw tactics checked | 1,000 |
| Exact premise/effect/delta observations checked | 1,000 |
| Audit failures | 0 |
| Old structured-projection disagreements retained | 659 state observations |

The disagreement count is not a V3 loss: it records cases where the old source parser truncated or misread multiline Lean text. The exact raw text is retained and V3's conservative decomposition is checked back against it.

## Explicit boundary

This pass does not assert elaborated-expression losslessness. Lean `Expr` trees, binder metadata, metavariable assignments/constraints, and a fully resolved namespace environment are absent from the source trace. Those are registered gaps, not guessed fields.

Verification labels remain calibrated: every row comes from the pinned accepted formal trace, while only 32 rows passed fresh exact-state replay. The remaining rows are not described as freshly replayed.
