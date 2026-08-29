# MicroMath Lab V2 — final report

Reader `qwen38-rvn:latest`, candidate `R_015b8cd926da`, best general control `TYPED_AST`.
Lab `micromath-lab-v2.0.0`, rule `micromath-calibration-v2.0.0` fixed before any V2 result existed.

`SEALED_FINAL_V2` was not read. No paid API, no paid GPU, no training, no global search. All inference local.

## 1. The instruments

| Component | Chance | Told the answer | Relation destroyed | Control | Candidate | Norm. read. | Instrument | Verdict |
|---|---|---|---|---|---|---|---|---|
| BINDER | — | — | — | — | — | — | NOT_RUN | NOT_RUN |
| SCOPE | — | — | — | — | — | — | NOT_RUN | NOT_RUN |
| DEPENDENCY | — | — | — | — | — | — | NOT_RUN | NOT_RUN |
| TYPE | — | — | — | — | — | — | NOT_RUN | NOT_RUN |
| MULTI_GOAL | — | — | — | — | — | — | — | **UNTESTED** |
| EXPRESSION_DEPTH | 0.304 | 1.000 | 0.083 | 0.167 | 0.167 | 0.091 | INSTRUMENT_VALID | **CONTROL_PARITY** |
| PREMISE | — | — | — | — | — | — | NOT_RUN | NOT_RUN |
| ACTION_ARGUMENT | — | — | — | — | — | — | NOT_RUN | NOT_RUN |

**Valid instruments: 1 of 1 measured** (of 8 components; the rest were withdrawn or gated). ['EXPRESSION_DEPTH']

- INSTRUMENT_INVALID: none
- INSTRUMENT_LIMIT: none
- INSTRUMENT_UNDECIDED at the ladder cap: none
- BENCHMARK_DEFECT (gated by the shortcut audit): none

## 2. What the valid instruments say about the language

- **ADVANTAGE**: none
- **CONTROL_PARITY**: ['EXPRESSION_DEPTH']
- **LANGUAGE_WEAKNESS**: none

**On no valid instrument does the discovered representation beat a plain typed AST.** That is the same answer V1 gave, now on repaired instruments with a demonstrated ceiling, a state-level floor and a clean construction audit.

## 3. Withdrawn and gated components

**MULTI_GOAL — `RELATION_NOT_PROJECTED` (`FM-044`).** No axis of the representation space renders which goal the action acts on. Verified twice against `projection.py`. This withdraws V1's largest reported result: its 0.375 of MULTI_GOAL 'headroom' was an absent projection, not a readability gap, and no notation could have claimed it.

## 4. Testing the tests (`§27`)

Known-bad detection: **NOT_RUN**.

## 5. Architectural hypotheses (`§13`, `§14`)

Not run.

## 6. What was not attempted

- **§16 the horizon test** — the corpus cannot populate the pre-registered ladders. G5 and D1–D2 are empty and G4 holds one item, so the prediction that a representation's advantage grows with structural complexity **cannot be tested here**. That is a statement about the corpus.
- **§30 the integration matrix** and **§31 the reasoning ladder** — gated behind certified components, and none is certified.
- **`micro_shadow_v2` and `micro_hidden_v2` are unread.** No result in this report is measured on held-out data.

## 7. Honest accounting of this run

Seven defects were found during V2 construction, and **four of them were in my own instruments or guards rather than in the language**:

| | Defect | How it surfaced |
|---|---|---|
| `FM-043` | the certification top-up spent both V1 holdouts | intersecting identifiers, after I claimed they were untouched |
| `FM-044` | MULTI_GOAL's relation is rendered by no axis | reading `projection.py` when a negative arm scored 0.833 |
| `FM-045` | one seed drove two decisions and correlated them | 'always first option' scoring 1.000 |
| `FM-046` | the audit re-sorted options, and its tolerance depended on n | one construction judged CLEAN and LEAKS on different splits |
| `FM-047` | EXPRESSION_DEPTH was ill-posed | three arms at exactly 0/12 — **it passed the pre-registered calibration rule** |
| `FM-048` | the positive control sat 7000 chars from the question | 0.417 while being handed the answer |

`FM-047` and `FM-048` were both caught by a number looking wrong, not by a test. Neither the calibration rule nor the shortcut audit could see either. **The automated guards did not substitute for reading one raw completion.**

`FM-048` also means every V1 dynamic range is understated, because V1 used the same distant-header positive control. The V1 `INSTRUMENT_INVALID` verdicts stand — those turned on negative arms — but V1 and V2 normalised-readability figures are not comparable.

## 8. Falsification status (`PROJECT_GOAL` §18)

The central claim — that a discovered representation can be made measurably more readable to a model than existing notations — **remains unsupported**. On every instrument that survives calibration the discovered representation is at parity with a plain typed AST, and both sit far below what the same reader achieves when the relation is stated outright.

What V2 adds beyond V1 is that this can no longer be blamed on the instruments. It can still be blamed on the corpus: over half the base states are too large to render, and the structures the long-horizon hypothesis is about are absent.

## 9. Exact next actions

1. **Acquire deeper base states.** States with more than four goals and expression depth beyond sixteen. Without them `PROJECT_GOAL` §18 cannot be tested, and that is now the binding constraint — not the notation.
2. **Add the action-to-goal edge to the projection** if MULTI_GOAL is to be measurable at all. This is a semantic-contract change and needs a decision record, not a quiet patch.
3. **Reproduce any surviving result on `micro_shadow_v2`** before it is believed, and only then on `micro_hidden_v2`.
4. **Do not train and do not launch a global search.** No component is certified.
5. **Leave `SEALED_FINAL_V2` alone.**

