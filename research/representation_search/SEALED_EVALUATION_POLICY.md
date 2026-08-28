# Sealed Evaluation Policy

## The risk this addresses

Representation architecture search can overfit its own evaluation set exactly as model
training can. Every generation reads metrics, proposes mutations against those metrics, and
selects on them; run long enough, the frontier describes the evaluation sample rather than
the representation.

## The partition

The unit is the **Mathlib source file**, not the transition and not the theorem. Two
transitions from one theorem obviously belong together; less obviously, two theorems in one
file share notation, local instances, `open` declarations and premise vocabulary, so a
theorem-level split still leaks.

Assignment is deterministic: `SHA-256("hml-v3-representation-search-split-v1|" + family)`,
first 64 bits read as a fraction of the unit interval, then `< 0.70` to `SEARCH_DEV`,
`< 0.80` to `SEARCH_VALIDATION`, otherwise `SEALED_FINAL_EVALUATION`. It depends on nothing
but the family name, so it is reproducible from the corpus and cannot drift with iteration
order.

## What the controller may do

- Read `SEARCH_DEV` transitions freely: gates, metrics, mutation proposals, selection.
- Read `SEARCH_VALIDATION` transitions to check that a frontier gain is not a dev artifact.
- Call `SealedEvaluator.evaluate(compiler, purpose)`, which returns **aggregate statistics
  only**: gate verdicts and the seven Pareto axis means over the sealed sample.

## What the controller may not do

- Read, print, render or inspect an individual sealed transition.
- Call the sealed evaluator during the search. It is called once, on the finalists, after the
  frontier is frozen.
- Choose a mutation, an axis value, a metric definition or a stopping point using a sealed
  result.

`SealedEvaluator` holds the transitions privately and exposes no accessor for them. Every
call appends `{candidate_id, purpose, sample}` to `data/representation_search/sealed_access_log.jsonl`,
so the number of times the sealed split was touched is auditable after the fact rather than
asserted.

## If the seal is broken

If a sealed transition is read during a search — by a future change to the controller, or by
a person — the honest response is to record it in the ledger, treat the sealed split as
consumed, and cut a fresh sealed split with a new split key from corpus families that have
never been read. Silently continuing would make every subsequent frontier claim untestable.
