# Discovery Representation Analysis

PRM800K labels are **human judgements of usefulness**. They are not verdicts of logical validity and are never promoted into the verifier-backed status that `D-008` keeps calibrated. They are used here for one purpose: to name the dimensions a formal Lean trace cannot express, and then to ask whether any representation in the search space could express them.

## What the labels contain

Read 60,949 labelled attempts containing 452,899 steps and 670,790 rated continuations (first 60,000 rows of each file).

| Step judgement | Count | Share |
|---|---:|---:|
| `DEAD_END_OR_ERROR` | 169,844 | 25.3% |
| `VALID_BUT_NOT_PROGRESSING` | 67,455 | 10.1% |
| `PROGRESS_TOWARD_SOLUTION` | 404,675 | 60.3% |
| `UNRATED` | 28,816 | 4.3% |

| Attempt outcome | Attempts |
|---|---:|
| `found_error` | 48,621 |
| `solution` | 9,391 |
| `give_up` | 2,662 |
| `bad_problem` | 275 |

Mean steps per attempt: **7.431**. Steps where a human had to write the continuation because every offered one was unacceptable: **51,152**.

| Continuations offered at a step | Steps |
|---|---:|
| 0 | 24 |
| 1 | 398,367 |
| 2 | 814 |
| 3 | 1,938 |
| 4 | 4,694 |
| 5 | 41,457 |
| 6 | 315 |
| 7 | 5,290 |

## The finding

**No representation in the current search space can express any of these dimensions, and the reason is not the representation.** A candidate exposes what `CanonicalMathState` carries; every discovery dimension below is absent from the canonical layer, so no genome — however structured — can surface it.

| Dimension | PRM800K signal | Canonical V2 field | Expressible by any genome? |
|---|---|---|---|
| `step_progress` | completion rating +1 | **none** | **no** |
| `valid_but_useless` | completion rating 0 | **none** | **no** |
| `dead_end` | completion rating -1 | **none** | **no** |
| `alternative_branch` | multiple completions offered at one step | **none** | **no** |
| `no_acceptable_alternative` | human_completion present with chosen_completion null | **none** | **no** |
| `solution_outcome` | label.finish_reason | verifier evidence exists per transition, not per attempt | **no** |

### Why each is absent

- **`step_progress`** — CanonicalMathTransition carries the verifier's acceptance of a step, not a judgement of whether the step helped. No axis can expose an absent field.
- **`valid_but_useless`** — the structured delta records what changed, and a legal no-op is visible as an empty delta, but 'legal and unhelpful' is a judgement the delta does not make.
- **`dead_end`** — a Lean trace contains only steps that were kept. Abandoned branches leave no TacticInfo, so the corpus has no negative examples at all.
- **`alternative_branch`** — a CanonicalMathTransition is a single before/action/after triple. Siblings would require a state-to-many-actions record the schema does not have.
- **`no_acceptable_alternative`** — same structural absence as alternative_branch.
- **`solution_outcome`** — the corpus unit is one transition; an attempt-level outcome has no home.

## The structural asymmetry this exposes

A Lean trace contains only the steps that were kept. Abandoned branches leave no `TacticInfo`, so the formal corpus has **no negative examples at all** — every one of its 317 transitions is a step that worked. PRM800K's rated continuations are 25.3% dead ends and 10.1% valid-but-not-progressing. A representation search optimised only on the formal corpus is therefore tuned on a distribution with no failure in it.

## What would have to change, and what must not

**Must not change.** PRM800K ratings are not verifier verdicts. Nothing here licenses labelling a canonical transition `DEAD_END` because a human rated a natural-language step `-1`. The two live in different columns permanently.

**Would have to change, if this line is pursued.** The canonical layer would need a record that a formal trace does not currently produce: a state paired with several candidate actions and a per-candidate outcome. Producing it from Lean means running actions that were never taken and recording their results — a proof-search acquisition problem, not a representation problem, and explicitly out of scope for this mission.

Until such a record exists, the honest position is that this search optimises representations of *verified transitions* and says nothing about representations of *search state*. Those are different objects and the current evidence separates them.
