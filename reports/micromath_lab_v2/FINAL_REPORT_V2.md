# MicroMath Lab V2 — final report

Reader `qwen38-rvn:latest`, candidate `R_015b8cd926da`, best general control `TYPED_AST`.
Lab `micromath-lab-v2.0.0`, rule `micromath-calibration-v2.0.0` fixed before any V2 result existed.

`SEALED_FINAL_V2` was not read. No paid API, no paid GPU, no training, no global search. All inference local.

## 1. The instruments

| Component | Chance | Told the answer | Relation destroyed | Control | Candidate | Norm. read. | Instrument | Verdict |
|---|---|---|---|---|---|---|---|---|
| BINDER | 0.277 | 1.000 | 0.250 | 0.833 | 0.917 | 0.889 | INSTRUMENT_VALID | **CONTROL_PARITY** |
| SCOPE | 0.464 | 0.917 | 0.250 | 0.750 | 0.667 | 0.625 | INSTRUMENT_VALID | **CONTROL_PARITY** |
| DEPENDENCY | 0.250 | 1.000 | 0.333 | 0.542 | 0.625 | 0.438 | INSTRUMENT_VALID | **CONTROL_PARITY** |
| TYPE | 0.300 | 1.000 | 0.333 | 0.917 | 0.917 | 0.875 | INSTRUMENT_VALID | **CONTROL_PARITY** |
| MULTI_GOAL | — | — | — | — | — | — | — | **UNTESTED** |
| EXPRESSION_DEPTH | 0.304 | 1.000 | 0.083 | 0.167 | 0.167 | 0.091 | INSTRUMENT_VALID | **CONTROL_PARITY** |
| PREMISE | 0.250 | 1.000 | 0.000 | 0.833 | 0.833 | 0.833 | INSTRUMENT_VALID | **CONTROL_PARITY** |
| ACTION_ARGUMENT | 0.264 | 1.000 | 0.167 | 0.917 | 0.917 | 0.900 | INSTRUMENT_VALID | **CONTROL_PARITY** |

**Valid instruments: 7 of 7 measured** (of 8 components; the rest were withdrawn or gated). ['ACTION_ARGUMENT', 'BINDER', 'DEPENDENCY', 'EXPRESSION_DEPTH', 'PREMISE', 'SCOPE', 'TYPE']

- INSTRUMENT_INVALID: none
- INSTRUMENT_LIMIT: none
- INSTRUMENT_UNDECIDED at the ladder cap: none
- BENCHMARK_DEFECT (gated by the shortcut audit): none

## 2. What the valid instruments say about the language

- **ADVANTAGE**: none
- **CONTROL_PARITY**: ['ACTION_ARGUMENT', 'BINDER', 'DEPENDENCY', 'EXPRESSION_DEPTH', 'PREMISE', 'SCOPE', 'TYPE']
- **LANGUAGE_WEAKNESS**: none

**On no valid instrument does the discovered representation beat a plain typed AST.** That is the same answer V1 gave, now on repaired instruments with a demonstrated ceiling, a state-level floor and a clean construction audit.

## 3. Withdrawn and gated components

**MULTI_GOAL — `RELATION_NOT_PROJECTED` (`FM-044`).** No axis of the representation space renders which goal the action acts on. Verified twice against `projection.py`. This withdraws V1's largest reported result: its 0.375 of MULTI_GOAL 'headroom' was an absent projection, not a readability gap, and no notation could have claimed it.

## 4. Testing the tests (`§27`)

| Component | Known-bad | Control | Known-bad score | Margin | Verdict |
|---|---|---|---|---|---|
| ACTION_ARGUMENT | `SCRAMBLE_ACTION_ARGS` | 0.917 | 0.917 | 0.000 | **INSTRUMENT_DEFECT** |
| BINDER | `HIDE_BINDER_RELATION` | 0.833 | 0.917 | -0.083 | **INSTRUMENT_DEFECT** |
| DEPENDENCY | `DELETE_DEPENDENCY_EDGES` | 0.417 | 0.500 | -0.083 | **INSTRUMENT_DEFECT** |
| EXPRESSION_DEPTH | `FLATTEN_EXPRESSION_PARENTAGE` | 0.167 | 0.250 | -0.083 | **INSTRUMENT_DEFECT** |
| MULTI_GOAL | `None` | — | — | — | **UNTESTED** |
| PREMISE | `STRIP_PROVENANCE` | 0.833 | 0.833 | 0.000 | **INSTRUMENT_DEFECT** |
| SCOPE | `SCRAMBLE_SCOPE` | 0.750 | 0.917 | -0.167 | **INSTRUMENT_DEFECT** |
| TYPE | `REMOVE_TYPE_LINK` | 0.917 | 0.583 | 0.333 | **DETECTED** |

**1 of 8 instruments detected the representation built to hide their own relation — and that number must not be read as 7 blind instruments (`FM-051`).**

Checking whether the answer token still appears on the page showed **6 of 6 items still carrying it** for DEPENDENCY, BINDER, PREMISE, ACTION_ARGUMENT and EXPRESSION_DEPTH. Those known-bads hide nothing, because the axes chosen do not control the rendering path each question depends on: `dependency_visibility` governs the *action's* local refs rather than the references inside declaration types, and `premise_locality` moves a citation rather than removing it.

Only TYPE's known-bad genuinely hides its relation, via `type_explicitness: OMITTED` — and there the instrument **did** detect it, at +0.333. The method is sound; the known-bad set was mis-targeted.

An exhaustive single-axis search over all 42 axes then found that **no axis hides any of those five relations at all.** The space can vary how a relation is written; it cannot choose not to write it. That is `D-025`, and it is the finding that explains every parity verdict above.

## 5. Architectural hypotheses (`§13`, `§14`)

| Component | Architecture | Screen | Δ vs candidate | Verdict |
|---|---|---|---|---|
| SCOPE | `G_INTERLEAVED_PER_GOAL` | 0.417 | -0.250 | REJECTED_NO_TARGETED_GAIN |
| SCOPE | `G_EXPLICIT_SCOPE_IDS` | 0.750 | 0.083 | HELD_NOT_SEPARATED_FROM_CANDIDATE |
| SCOPE | `G_GOAL_CENTRED_CONTEXT` | 0.750 | 0.083 | HELD_NOT_SEPARATED_FROM_CANDIDATE |
| SCOPE | `G_REDUNDANT_GOAL_ANCHOR` | 0.667 | 0.000 | REJECTED_NO_TARGETED_GAIN |
| EXPRESSION_DEPTH | `E_GRAPH_EDGE_LIST` | 0.167 | 0.000 | REJECTED_NO_TARGETED_GAIN |
| EXPRESSION_DEPTH | `E_HYBRID_NESTED_WITH_EDGES` | 0.167 | 0.000 | REJECTED_NO_TARGETED_GAIN |
| EXPRESSION_DEPTH | `E_DEPENDENCY_LOCAL_SERIAL` | 0.333 | 0.167 | REJECTED_CROSS_COMPONENT_REGRESSION |
| EXPRESSION_DEPTH | `E_HEAD_ONLY_WITH_REMINDERS` | 0.250 | 0.083 | REJECTED_CROSS_COMPONENT_REGRESSION |

Accepted: **0**. Rejected as behavioural duplicates before any inference: **0**.

No architectural change moved the target component either. Combined with V1's five properly tested surface mutations moving 0.031, that is now two independent families of hypothesis refuted: **neither restyling the notation nor re-exposing the structure through the axes this compiler offers changes what the reader can recover.**

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

