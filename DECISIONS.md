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

