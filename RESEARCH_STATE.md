# Research State

Checkpoint: 2026-08-28 (Europe/London)

The evidence inventory and `LEAN_PIPELINE_V1` foundation are complete on branch
`codex/evidence-first-foundation`. The project must not optimize or select a new language
syntax yet.

Current historical evidence does not privilege prior HML syntax. The most recent clean
Stage-1 validity probe placed Structured English first, Lean-like second, prior HML third,
and typed AST fourth on IID macro-F1. HML led no split, and the frozen transformer exceeded
its own bag-of-words control by only 0.022–0.055 macro-F1. This is one lexical-heavy task,
not a general ranking of representations.

Current evidence:

- 7 prior/local repositories and 26 datasets are registered; no known curated local asset is missing.
- 1,000 unique Mathlib transitions preserve exact theorem source and before/action/after observations.
- 578 transitions carry 1,353 official annotated premise references.
- 32 transitions pass fresh exact replay; 968 are honestly labelled formal-trace accepted.
- declared-observation losslessness passes 1,000/1,000;
- ten renderer candidates pass 10,000/10,000 combined semantic round trips;
- eight real-math gaps are open, principally elaboration metadata and replay-path acquisition.

## Since that checkpoint

The V2 runtime substrate is certified: 317 canonical transitions across 26 Mathlib domains,
with all 183 unrecovered selections counted by reason. The corpus is structurally rich where
the prior one was not — mean 13.4 local declarations and 63.4 intra-context references per
transition, against the prior corpus's 1.00 claims and zero dependencies — so locality and
ordering are measurable on real mathematics for the first time.

The representation architecture search is built and run. Measured here:

- Goal-centred ordering loses **again**, now on a corpus that has real dependencies
  (`FM-021`). `FM-005`'s single retry is spent.
- Hoisting shared subterms into a DAG costs **+136%** tokens and halves record-order
  corruption detection (`FM-022`).
- Identifier-corruption detection **saturates** at 1.000 across all sixteen seeds and was
  removed from selection before the search began (`FM-019`).
- Goal linearization is **unmeasurable** on this corpus: 11 single-axis mutations, 0 changed
  the measurement, because states average 1.01 goals (`FM-020`).
- `FM-004`'s escaping penalty **reproduces** under a second vocabulary, but absolute token
  counts do not: the corpus's glyphs are 1 token under Qwen3-8B and 2–3 under GPT-2
  (`FM-018`).
- PRM800K names five discovery dimensions — progress, valid-but-useless, dead end,
  alternative branch, attempt outcome — and **no representation in the space can express any
  of them**, because `CanonicalMathState` carries none of them. A Lean trace holds only steps
  that were kept, so the formal corpus contains no negative examples at all.

Next action: extend the corpus with the second Lean campaign, run the search to structural
convergence, perform the single sealed evaluation, and publish
`PRETRAINING_REPRESENTATION_FRONTIER_V1`. No paid GPU run is justified yet.
