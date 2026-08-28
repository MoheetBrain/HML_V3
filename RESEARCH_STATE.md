# Research State

Checkpoint: 2026-08-27 (Europe/London)

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

Next action: improve Lean extraction for elaborated expressions, stable goal/free-variable IDs,
metavariable constraints, and local dependency edges, then design a shortcut-resistant real
premise-selection or next-action benchmark. No paid GPU run is justified yet.
