# Component certification dashboard — MicroMath Lab V1

Reader: `qwen38-rvn:latest`, local, zero incremental cost.
Run: 8 components x 4 arms x 12 pairs (24 items per arm) = 768 probe items, 8190 s (2 h 16 m).
Rule preregistered before the run: `src/hml_v3/micromath/calibration.py`.
Machine-readable source: `COMPONENT_CERTIFICATION.json`.

## Verdicts

| Component | Positive | Negative | Best control | Candidate | Range | Norm. read. | Verdict |
|---|---|---|---|---|---|---|---|
| MULTI_GOAL | 0.958 | 0.500 | 0.583 | 0.583 | 0.458 | **0.182** | CONTROL_PARITY |
| EXPRESSION_DEPTH | 0.917 | 0.458 | 0.500 | 0.500 | 0.458 | **0.091** | CONTROL_PARITY |
| DEPENDENCY | 0.792 | 0.792 | 0.792 | 0.708 | 0.000 | — | INSTRUMENT_INVALID |
| SCOPE | 0.833 | 0.792 | 0.750 | 0.833 | 0.042 | — | INSTRUMENT_INVALID |
| TYPE | 0.833 | 0.833 | 0.833 | 0.833 | 0.000 | — | INSTRUMENT_INVALID |
| PREMISE | 0.875 | 0.875 | 0.875 | 0.875 | 0.000 | — | INSTRUMENT_INVALID |
| BINDER | 0.667 | 0.500 | 0.542 | 0.500 | 0.167 | — | INSTRUMENT_LIMIT |
| ACTION_ARGUMENT | 0.542 | 0.542 | 0.542 | 0.542 | 0.000 | — | INSTRUMENT_LIMIT |

**Certified components: 0 of 8.**

## What each verdict means

- **CONTROL_PARITY (2)** — the instrument works: stating the relation outright reaches 0.92–0.96,
  destroying it drops to chance. The candidate reads the relation no better than the best
  hand-written control, and both sit near the floor.
- **INSTRUMENT_INVALID (4)** — the negative arm, which prepends a *decoy* answer and is meant to
  score at chance, instead scores 0.79–0.88. The question is answerable with the relation
  destroyed. These four cells were never measuring the relation they are named after.
- **INSTRUMENT_LIMIT (2)** — the positive arm cannot lift the reader far enough
  (ACTION_ARGUMENT tops out at 0.542 even when told the answer). No representation can be
  blamed or credited on a question this reader cannot do at any readability.

## The headroom on the two valid instruments

Normalised readability is `(candidate - negative) / (positive - negative)`: 0 = the relation is
as unreadable as if it had been destroyed, 1 = as readable as stating it in words.

```
MULTI_GOAL         neg 0.500 ......... cand/ctrl 0.583 ................................ pos 0.958
                   |----18.2%----|                    <-- 0.375 unclaimed -->
EXPRESSION_DEPTH   neg 0.458 .. cand/ctrl 0.500 ....................................... pos 0.917
                   |--9.1%--|                         <-- 0.417 unclaimed -->
```

On the only two questions this lab can legitimately ask, **no representation — discovered,
hand-written, or legacy — reads more than 18 % of the way from "relation destroyed" to
"relation stated in words."** The gap is not between HML and its rivals. It is between every
representation tested and the ceiling.
