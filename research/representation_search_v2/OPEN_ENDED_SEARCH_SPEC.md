# Open-Ended Search V2 — specification

## The defect this replaces

V1 searched 42 axes chosen by a person. Its controller called `targeted_proposals`,
`local_neighbourhood` and `random_walk` against a hard-coded `AXIS_MECHANISM` table, so every
candidate it could reach was a recombination of dimensions that already existed. The
consequence is worth stating plainly:

> If the best machine-facing representation of mathematics requires an idea not present in the
> 42-axis genome, the V1 search had **zero probability** of discovering it.

V2 does not remove that ceiling by making the genome bigger. It removes it by letting the
search add axes to its own genome, through a channel narrow enough to stay safe.

## The channel

```text
    meta-designer  ->  JSON proposal
                       |
                       |  schemas.validate      typed, falsifiable, layer-checked
                       |  static_safety         refuses the substrate, the seal, the host
                       v
                   ValidatedProposal
                       |
                       |  primitive_registry.consider   binds behaviour to an executable hook
                       v
                   genome v2.N+1   ->   candidate   ->   the ladder
```

Free-form model output never reaches a file, a genome or the compiler. Everything a
meta-designer can ask for is one of eight proposal types, and each is validated before any
compute is spent.

## What a meta-designer may propose

| Type | Purpose |
|---|---|
| `AXIS_MUTATION` | change one existing axis on one parent |
| `ARCHITECTURAL_HYPOTHESIS` | several axes together as one coherent intervention |
| `NEW_AXIS` | a dimension the genome does not have |
| `NEW_PRIMITIVE` | a new representation mechanism, with projection behaviour |
| `CORPUS_ACQUISITION` | the corpus cannot answer the question |
| `NEW_MICROTEST` | the instruments cannot answer the question |
| `INSTRUMENT_FIX` | an instrument is measuring the wrong thing |
| `ELIMINATE_CANDIDATE` | retire a candidate, with a typed reason |

The last five matter as much as the first three. A search that can only mutate languages will
keep mutating languages when the real problem is that the corpus has 1.01 goals per state.

## The envelope, stated rather than hidden

An invented axis is executable only if its declared behaviour binds to one of four projection
hooks:

| Hook | What it does |
|---|---|
| `neighbourhood_capsule` | move the declarations a goal cites adjacent to that goal |
| `duplicate_adjacent` | restate one field next to the record that consumes it |
| `section_partition` | emit one record kind in its own block |
| `record_reorder` | reorder records of one kind by a declared key |

A proposal outside this algebra is recorded as `ACCEPTED_UNIMPLEMENTABLE` — kept as evidence
about what the meta-designer wanted and what the compiler could not do. Growing the algebra is
a code change with tests, not a runtime trick.

This is a real limit on open-endedness and the reports say so. What the system genuinely has is
the ability to invent *combinations and applications* within a projection algebra, and to
notice when the problem is not the language at all.

## Migration: why old candidates stay comparable

Every invented axis has an off position. An axis added at schema `v2.N` is absent from every
genome recorded under `v2.<N`, and absent means `NONE`. A candidate evaluated before the axis
existed therefore re-renders **byte-identically** afterwards, which is the only reason
cross-generation comparisons remain legitimate. This is asserted by a test.

## The ladder

A child is killed at the cheapest level that can kill it.

| Level | Test | Typical cost |
|---|---|---|
| 0 | compiles; lexicon unambiguous | microseconds |
| 1 | semantic round-trip, determinism, glyph fidelity, structural recoverability | milliseconds |
| 2 | mechanism-specific structural-access microtests | milliseconds |
| 3 | static cost, locality, tokenizer | ~1 second |
| 4 | `SEARCH_DEV` broad measurement | seconds |
| 5 | `SEARCH_VALIDATION` replication — required for eliteness | seconds |
| 6–8 | neural microprobes at 20 / 40–80 / 160 items, sequential | minutes |
| 9 | sealed evaluation, once, after convergence | minutes |

## Two loops, not one

**Parameter evolution** is fast: change an axis value, re-measure. Many per generation.

**Ontology evolution** is slow: invent an axis, bind it to a hook, register it, bump the
schema. It changes what the language design space *is*, so it requires the proposal to name a
mechanism, a falsification condition and a test. The two are never conflated: a generation
report lists `new_axes` separately from `evaluated`.

## What V2 deliberately does not do

- It does not let a meta-designer change `CanonicalMathState`. A proposed semantic change
  requires an exact Lean counterexample, an information-loss argument, a minimal state, a
  reason it affects legal reasoning, and a regression test. Nothing in the automated loop can
  supply those, so the loop cannot make one.
- It does not read `SEALED_FINAL` during search. The split lives in another process.
- It does not train anything.
