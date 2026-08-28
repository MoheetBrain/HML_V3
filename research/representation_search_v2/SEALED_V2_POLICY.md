# Sealed Evaluation V2

## Why V1's seal is spent

The V1 sealed split was evaluated once, on six finalists, exactly as its policy allowed. That
was correct, and it also means the split has been read. A frontier chosen *after* seeing an
aggregate from those families is no longer being tested against data it has never influenced.

That split is therefore retired under the name `HISTORICAL_SEALED_V1`. It remains in the
repository as evidence and its access log stands at six entries. It is not used to evaluate
anything produced by the V2 search.

## Isolation by construction, not by discipline

V1's sealed evaluator was logically separated but loaded the sealed rows into the same Python
process as the search. Separation by discipline is weaker than separation by construction: any
later controller change, or any debugging session, could read them.

```text
  search process                      sealed process
  --------------                      --------------
  holds a Path                        loads the rows
  sends {candidate genomes}     -->   runs gates + metrics
  receives aggregate JSON       <--   writes the access log FIRST, then answers
```

The parent never holds a sealed transition. The child returns only keys on an allow-list —
`candidate_id`, `sample_size`, `gates_passed`, `first_gate_failure`, `pareto_axes`,
`microtests`, `access_index`, `corpus_sha256` — and the parent strips anything else as defence
in depth. The child writes the access log *before* answering, so an access that happened is
recorded even if the parent dies mid-call.

## Leakage rules for `SEALED_FINAL_V2`

The split unit is the **Mathlib source file**, not the transition and not the theorem. Sibling
lemmas in one file share notation, instances and premise vocabulary, so a theorem-level split
leaks. Assignment is a keyed SHA-256 of the file path, reproducible from the corpus alone.

`SEALED_FINAL_V2` is additionally drawn from theorem families acquired *after* V1's search, so
no family that influenced the V1 frontier can appear in it.

## When it may be read

Once, after convergence, on the reported finalists only. Not to choose the finalists, not to
tune a metric, not to decide when to stop. If it is read at any other time, the honest response
is to record that in the ledger, treat the split as consumed, and cut a `SEALED_FINAL_V3` from
families that have never been read.
