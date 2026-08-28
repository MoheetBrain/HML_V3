# Decisions

Decisions are additive. Superseded decisions remain in this file with their status changed;
they are not deleted.

## D-001 — Representation is the dependent variable

**Status:** ACTIVE

Canonical mathematical state and verifier outcomes are held fixed while renderers vary.
No representation is named the final HML V3 language during the foundation milestone.

## D-002 — Raw source observations remain authoritative

**Status:** ACTIVE

Lean pretty-printed states, tactics, source locations, versions, and verifier evidence are
preserved verbatim. Parsed canonical fields are an adapter output, not a replacement for the
source observation.

## D-003 — Trust tier is not verification status

**Status:** ACTIVE

A source can be formally structured yet only trace-recorded, or naturally written yet later
verified. Registry entries therefore carry both `trust_tier` and `verification_status`.

## D-004 — External payloads stay external by default

**Status:** ACTIVE

Large datasets and repositories are referenced by immutable source identity, size, hash when
feasible, license, and reproducible acquisition method. Small samples may be committed when
their license permits it and their provenance is complete.

## D-005 — Prior HML is one candidate renderer

**Status:** ACTIVE

Previous HML contributes semantic design ideas, regression artifacts, and an empirical
baseline. Its syntax and ontology do not define the canonical IR.

## D-006 — Exact raw Lean state outranks the prior structured projection

**Status:** ACTIVE

The old derived `hypotheses` and `target` fields disagree with conservative raw-state
decomposition on 659 of 2,000 V1 observations, primarily because multiline constructs were
truncated or misparsed. V3 preserves those disagreements but derives displayed goals and
contexts from the exact raw state.

## D-007 — Premises come from the official annotated tactic

**Status:** ACTIVE

Every one of the 241,265 prior derived records has an empty `premises_used` list. V3 joins
selected rows back to the pinned LeanDojo Benchmark 4 trace and accepts premise identities
only after exact tactic/before/after equality. Local-context dependencies remain an explicit
gap.

## D-008 — Formal trace and fresh replay are distinct verdicts

**Status:** ACTIVE

All V1 rows are accepted trace transitions from the pinned formal corpus. Only the 32 rows
whose Stage100 certificates reached and exactly matched the transition are labelled
`FRESH_REPLAY_PASS`; no other row inherits that label.

## D-009 — The initial representation family has no winner

**Status:** ACTIVE

All ten required candidate families are implemented and semantically parity-checked. Byte
length and whitespace counts are descriptive diagnostics, not a selection criterion. Model
experiments wait for stronger, shortcut-resistant tasks.
