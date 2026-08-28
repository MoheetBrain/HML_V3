# Roadmap

## M0 — Evidence inventory

**Status: COMPLETE (V1).** Seven repositories, all visible ref histories/worktrees, 803
dataset-like files, 15 experiment families, and registered local/external evidence are
captured in the machine inventory and reports.

- Inventory prior repositories across branches, tags, worktrees, datasets, experiments, and
  external caches.
- Assign trust tier, verification status, license state, duplicate status, and ingestion
  decision without copying large payloads.
- Preserve negative, confounded, invalidated, and saturated results as first-class evidence.

## M1 — LEAN_PIPELINE_V1

**Status: COMPLETE.** The committed sample contains 1,000 unique-theorem transitions and
all ten initial renderer families. Losslessness and semantic parity pass.

- Pin Lean, Mathlib, LeanDojo, and source artifacts.
- Preserve at least 1,000 real Lean proof transitions when the available trace supports it.
- Separate source `LeanTransition` from `CanonicalTransition` through an explicit adapter.
- Test losslessness against declared semantic observations.
- Render the same canonical object as Lean-like, prior-HML-compatible, typed AST,
  Structured English, canonical S-expression, graph edges, goal-local,
  dependency-topological, explicit-redundant, and minimal-machine views.
- Run deterministic round-trip and cross-renderer semantic-parity tests.

## M2 — Real-math gap discovery

**Status: INITIAL REGISTER COMPLETE; stronger source extraction remains open.** Eight
empirical gaps are recorded without extending the IR speculatively.

- Sample across Mathlib domains and state shapes.
- Record the smallest empirical counterexample for each information loss.
- Extend the IR only when real verified mathematics demonstrates the need.

## M2.5 — Representation architecture search

**Status: ENGINE COMPLETE; SEARCH RUN.** The language became data: a 42-axis
`RepresentationGenome` over 4.095e19 points, one generic compiler, six hard semantic gates, a
21-metric evaluator, Pareto selection with pinned baselines, a hypothesis-carrying mutation
library, an enforced failure memory, a synthetic adversarial generator, family-level corpus
sealing, and a checkpointing controller.

- Certify the Lean V2 runtime substrate and build a canonical corpus with every exclusion
  counted.
- Make every candidate reproducible from a genome hash rather than from renderer code.
- Reject on semantics before scoring on cost.
- Record every measured negative into the failure memory so it is never re-derived.
- Report the frontier without claiming optimality.

## M3 — Representation benchmark V3

- Build premise-selection, next-action, transition-validity, and state-delta tasks from
  formal traces.
- Gate every task with class-prior, length-only, structural-count, bag-of-words,
  character n-gram, and shallow lexical controls.
- Use theorem-family and dependency-aware splits.
- Ask before any paid GPU run.

## Later

- Free-running proof search.
- Additional formal-system adapters.
- Search over representation genomes only after the substrate and tasks are trusted.
- A matched, control-gated model experiment on the pretraining frontier's finalists — frozen
  inference first, then a tiny probe, and only then any adaptation.
