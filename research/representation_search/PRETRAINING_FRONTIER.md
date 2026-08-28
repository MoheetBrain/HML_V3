# The Pretraining Frontier — method

The generated result lives in
[`reports/representation_search/PRETRAINING_FRONTIER_V1.md`](../../reports/representation_search/PRETRAINING_FRONTIER_V1.md);
this file records how it is produced and what it is allowed to say.

## What "frontier" means here

A single winner is not claimed unless the evidence produces one. The output is the
non-dominated set over seven Pareto axes. Candidates on it are *incomparable*, not tied: each
buys something on one axis by paying on another, and choosing between them is a decision about
what the later model experiment should optimise, not something static evidence can settle.

## Reproducing it

```sh
PYTHONPATH=src python3 scripts/audit/stream_runtime_v2_corpus.py \
    --campaign-dir external/runtime_probe/campaign500
PYTHONPATH=src python3 scripts/search/run_representation_search.py --generations 12
PYTHONPATH=src python3 scripts/search/run_representation_search.py --generations 0 --seal-final
PYTHONPATH=src python3 scripts/search/build_search_report.py
```

The second command is resumable: state lives in `data/representation_search/` and re-running
it continues from the exact next generation. The third performs the single sealed evaluation.

## Convergence

Structural convergence is declared when the **frontier signature** — the best value on each
Pareto axis across the whole evaluated population — fails to improve for five consecutive
generations, or the generation budget runs out. Both outcomes are reported by name; a search
that stopped on its budget is not described as converged.

## The claim ladder

| Statement | Supported by this work? |
|---|---|
| These candidates preserve the declared semantic contract exactly | Yes — hard gate, every dev transition |
| These candidates are deterministic and UTF-8 faithful | Yes — hard gates |
| Candidate A costs fewer GPT-2 tokens than candidate B on this corpus | Yes — measured |
| Candidate A costs fewer tokens under any tokenizer | **No** — vocabulary-dependent; see the Qwen3 comparison |
| Candidate A keeps a binder nearer its use than candidate B | Yes — measured in characters and tokens |
| Shorter binder-use distance helps a model | **No** — untested here |
| Candidate A is the best machine language for mathematics | **No** — requires model evidence |

## Required next stage

Freezing this frontier does not end the question; it makes the next experiment cheap enough
to be worth running. The minimum honest sequence, none of which is performed here:

1. frozen-model inference over the finalists, with a matched envelope (`FM-001`);
2. the six lexical controls (`FM-003`) reported beside every arm;
3. a task that does not saturate (`FM-010`);
4. only then, any adaptation or training.
