# The Recursive Scientist

## State

```
X_t = ( corpus,
        representation_population,
        genome_schema,          <- grows; this is what V1 could not do
        instruments,            <- microtests, tokenizers, mutation families
        static_results,
        validation_results,
        neural_microresults,
        lineage,
        failure_memory,
        unresolved_questions,
        experiment_budget )
```

## Actions

| Action | Implemented by |
|---|---|
| `mutate_representation` | `AXIS_MUTATION` / `ARCHITECTURAL_HYPOTHESIS` |
| `invent_primitive` | `NEW_AXIS` / `NEW_PRIMITIVE` -> `primitive_registry` |
| `acquire_targeted_data` | `CORPUS_ACQUISITION` -> `active_corpus` |
| `add_microtest` | `NEW_MICROTEST` |
| `repair_instrument` | `INSTRUMENT_FIX` |
| `run_probe` | `neural_probe` under a preregistered sequential rule |
| `eliminate_candidate` | `ELIMINATE_CANDIDATE`, or the ladder |

## Why the non-representation actions matter most

The failure mode of a representation search is to keep mutating representations when the
problem is elsewhere. Three of the measured results in this project were not about
representations at all:

- `FM-020` — goal linearization was unmeasurable because the corpus averaged **1.01 goals per
  state**. Eleven mutations of `graph_serialization` changed the measurement zero times. The
  correct action was `CORPUS_ACQUISITION`, not another mutation.
- `FM-019` — identifier-corruption detection read 1.000 for all sixteen seeds. The correct
  action was `INSTRUMENT_FIX`: remove a saturated axis from selection.
- `FM-023`, `FM-025` — two locality instruments were measuring the wrong thing. Both were
  `INSTRUMENT_FIX`.

A loop that could only mutate languages would have produced confident numbers in all four
cases and learned nothing.

## Reward

Not a scalar. A generation is judged on: movement of the defensible Pareto frontier, reduction
in unresolved uncertainty, whether gains reproduced on validation, and cost. These are reported
separately because they trade off, and collapsing them would hide exactly the trades a reader
needs to see.

## The condition for stopping

Structural convergence requires all of: no material frontier movement for five generations;
validation movement also stalled; the major architecture families represented; single-axis
neighbours of the elites explored; the meta-designer proposing no high-confidence untested
structural primitive; remaining differences primarily model-dependent; and semantic gates
still perfect.

If the budget expires first, the answer is `STRUCTURAL_CONVERGENCE: NO`, said plainly.
