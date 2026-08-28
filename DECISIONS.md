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

## D-010 — The language is data, and there is exactly one compiler

**Status:** ACTIVE

A candidate representation is a `RepresentationGenome` — a point in a 42-axis discrete space
— consumed by one generic compiler. No candidate has renderer code of its own. Two
candidates therefore cannot differ by an implementation accident, and any candidate is
reproducible from `(genome_sha256, compiler_version, canonical_state_version)`. The candidate
id is the first twelve hex digits of the genome hash.

This supersedes the V1 practice of writing one renderer class per candidate. Those ten V1
renderers remain as historical artifacts; they wrapped the same canonical JSON in different
headers and could not vary structure, ordering, identity or notation independently.

## D-011 — The declared semantic contract is `projection.semantic_core`

**Status:** ACTIVE

A candidate claims losslessness against goals with identities, targets as elaborated
expression trees, local contexts with identity/binder role/declaration role/type/value, focus
order, relevant metavariables, and the action's identity with its premise and local
references. Lean's display spelling, content hashes, environment provenance and corpus
bookkeeping are outside it, consistent with `D-002` and `D-009`.

A genome that hides contract content fails the round-trip gate and is never scored. That is
what stops compression buying its way past a semantic loss.

## D-012 — Local-context order is stated once, layout is free

**Status:** ACTIVE

Lean's local-context order is semantic: a declaration may only mention earlier free
variables. A representation may therefore permute *record layout* for locality, but the
goal's `context` field always states canonical declaration order. Reordering is presentation;
discarding the order is a semantic loss.

## D-013 — Corruption detection is reported per family, never averaged before selection

**Status:** ACTIVE

`FM-007` recorded a candidate that scored 0.800 overall while being completely blind
(`0.000`) to record-order corruption. A mean would have hidden that. Six mutation families
are measured separately and reported separately.

## D-014 — A saturated instrument is excluded from selection and said to be saturated

**Status:** ACTIVE

`detect_corrupt_identity` read `1.000` for all sixteen generation-zero seeds on the real V2
corpus. Following `FM-010`, it is measured, reported as non-discriminative, and removed from
the Pareto axes; `detect_drop_field` replaced it. The decision was made before the search
began, so every candidate is compared on the same axes.

## D-015 — The corpus is split by Mathlib source file and the final split is sealed

**Status:** ACTIVE

Sibling lemmas in one file share notation, instances and premise vocabulary, so a
transition-level or theorem-level split leaks. Assignment is a keyed SHA-256 of the file
path, reproducible from the corpus alone. The sealed 20% is reachable only through
`SealedEvaluator`, which returns aggregates and logs every access.

## D-016 — Token counts are named with their vocabulary

**Status:** ACTIVE

Under the pinned GPT-2 byte-level BPE, `⊢` costs 3 tokens, `ℝ` 3, `𝕜` 3. The prior
tokenization audit measured all of them at 1 token under Qwen3-8B. `FM-004`'s escaping
penalty reproduces under both vocabularies — escaping costs 2.3x–2.7x under GPT-2 — but the
absolute counts do not. Every token claim names its vocabulary, and byte counts plus
tokenizer-free pre-tokens are reported beside every token count.

## D-017 — The V2 corpus is size-bounded and the exclusions are counted

**Status:** ACTIVE

Lean's accumulated metavariable inventory is quadratic in some proofs: four of the campaign's
250 raw documents are between 6.8 GiB and 24 GiB, and one was truncated when the original
driver died. The corpus builder streams each document, excludes any transition whose
canonical form exceeds a declared 256 KiB budget, and counts every exclusion by reason. 317
of 500 selected transitions were recovered; the other 183 are accounted for in
`reports/audits/LEAN_RUNTIME_V2_CORPUS.md` rather than quietly dropped.
