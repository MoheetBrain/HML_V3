# Real-Math Gap Register

Evidence base: `LEAN_PIPELINE_V1`, 1,000 unique Mathlib theorems, 2,000 exact tactic-state observations, eight balanced effect classes. These are gaps in current source acquisition or canonical semantics—not requests to change previous HML.

V2 status summary: **5 closed (four in the neutral IR, one in source acquisition) and 3 still open.** The original counterexamples remain below as scientific history. `ELABORATED_LOSSLESSNESS` remains blocked by the three open completeness questions even though declared-observation V1 losslessness still passes.

## GAP-001 — Elaborated expression trees are absent

- **Source theorem:** `LinearMap.not_hasEigenvalue_zero_tfae`, `Mathlib/LinearAlgebra/Eigenspace/Zero.lean`, transition 7.
- **Exact state fragment:** `⊢ m ≠ 0 → φ m ≠ 0 ↔ φ m = 0 → m = 0`
- **Reasoning step:** `apply not_imp_not`
- **Information lost:** Lean `Expr` constructors, constants, implicit arguments, coercions, universe levels, and elaborated types behind the pretty-printed target.
- **Why it matters:** two surface-identical terms can depend on different elaboration environments; typed substitution and alpha-equivalence cannot be certified from text alone.
- **Smallest counterexample:** the overloaded `0` and coercions in the displayed target do not identify their elaborated constants.
- **Proposed layer:** Lean adapter/source acquisition; ingest serialized `Expr` data with environment identity before extending the neutral expression schema.
- **V2 evidence:** `LeanRuntimeExtractV2.lean` serializes all 12 Lean 4.10 `Expr` constructors directly from `TacticInfo` runtime expressions, including levels, constant identities, implicit elaborated applications, coercion structure, annotations, and projections. `LeanRuntimeState` stays separate from the neutral adapter.
- **V2 adjudication:** `CLOSED_IR`.

## GAP-002 — Binder kind and free-variable identity are not recoverable

- **Source theorem:** `Algebra.intTrace_eq_trace`, `Mathlib/RingTheory/IntegralRestrict.lean`, transition 0.
- **Exact state fragment:** `A : Type u_1` and `inst✝³⁰ : CommRing A`.
- **Reasoning step:** `ext x`.
- **Information lost:** Lean `BinderInfo`, internal `FVarId`, synthetic-opaque provenance, and the identity behind inaccessible names.
- **Why it matters:** pretty names can be regenerated or shadowed; binder identity is required for hygienic substitutions and stable state matching.
- **Smallest counterexample:** `inst✝` is a display name, not a stable internal identifier.
- **Proposed layer:** Lean adapter; add verified binder/FVar metadata only when emitted by Lean.
- **V2 evidence:** each actual `LocalDecl` now carries `FVarId`, context index, user name, `BinderInfo`, declaration kind, type, optional value, and instance membership. Canonical IDs derive from declaration order; alpha spelling is explicitly non-semantic, and alpha/shadow/instance behavior is tested.
- **V2 adjudication:** `CLOSED_IR`.

## GAP-003 — Metavariable assignments and constraints are only visible as names

- **Source theorem:** `CategoryTheory.isVanKampenColimit_extendCofan`, `Mathlib/CategoryTheory/Limits/VanKampen.lean`, transition 36.
- **Exact state fragment:** universe metavariables `?u.306842`, `?u.306849` occur in the before-state.
- **Reasoning step:** a `simpa [...] using ...` action closes the goal.
- **Information lost:** metavariable declarations, types, assignments, delayed constraints, synthetic-opaque flags, and unification state.
- **Why it matters:** a tactic can change the metavariable context without a sufficient pretty-print difference; legality depends on constraint solving.
- **Smallest counterexample:** V3 can record the token `?u.306842` but cannot state what it ranges over or whether it was assigned.
- **Proposed layer:** Lean adapter plus canonical metavariable/constraint records.
- **V2 evidence:** the source snapshot preserves relevant `MetavarDecl` types, assignments, kinds, local contexts, universe assignments/depths, delayed assignments, full context counts, and exact created/newly-assigned/changed records across the step.
- **Remaining limit:** Lean 4.10 exposes no standalone generic constraint table, and the neutral projection deliberately excludes inactive implementation state. That unknown may still affect action legality.
- **V2 adjudication:** `STILL_OPEN`.

## GAP-004 — Goal identity does not survive focus reordering

- **Source theorem:** `CategoryTheory.mono_of_cofan_isVanKampen`, `Mathlib/CategoryTheory/Limits/VanKampen.lean`, transition 7.
- **Exact state fragment:** three displayed goals, including `⊢ 𝟙 ((Discrete.functor f).obj i) = ?convert_4 ≫ ...`.
- **Reasoning step:** `swap` reorders the three goals while leaving their mathematical targets otherwise present.
- **Information lost:** stable Lean goal/metavariable IDs and focus-stack identity across states.
- **Why it matters:** V3 currently assigns goal IDs by display ordinal, so it cannot prove that after-goal 0 is the same internal goal as before-goal 1.
- **Smallest counterexample:** two goals exchanged by `swap` are distinguishable by surface target but not linked by stable identity.
- **Proposed layer:** Lean source adapter; capture `MVarId` identity, then add cross-state goal correspondence to `StateDelta`.
- **V2 evidence:** real goal `MVarId`, ordered focus list, and cross-state identity deltas are captured. A reorder test with identical targets proves that `swap`-like changes are not misclassified as delete/create.
- **V2 adjudication:** `CLOSED_IR`.

## GAP-005 — Local-hypothesis dependencies are not in official annotated premises

- **Source theorem:** `AkraBazziRecurrence.T_isBigO_smoothingFn_mul_asympBound`, `Mathlib/Computability/AkraBazzi/AkraBazzi.lean`, transition 55.
- **Exact state fragment:** local declarations include `R`, `i`, `n`, and `n₀_ge_Rn₀`.
- **Reasoning step:** `exact add_eq_of_eq_sub <| Finset.sum_Ico_eq_sub _ <| le_of_lt <| R.r_lt_n i n <| n₀_ge_Rn₀.trans hn`.
- **Information lost:** the official annotated tactic identifies external premises `add_eq_of_eq_sub`, `Finset.sum_Ico_eq_sub`, and `le_of_lt`, but not a typed dependency graph over the cited local hypotheses.
- **Why it matters:** premise selection, context pruning, and dependency-topological representations need both external declarations and local facts.
- **Smallest counterexample:** `R.r_lt_n`, `i`, `n`, `n₀_ge_Rn₀`, and `hn` are semantically used but absent from `referenced_premises`.
- **Proposed layer:** Lean elaboration adapter; distinguish `external_premise_refs` from `local_context_refs`.
- **V2 evidence:** descendant elaborated `TermInfo.expr` trees are traversed for typed FVar references and separated from official LeanDojo external premises; raw IDs are resolved against the before-goal context and the mechanism/confidence are recorded.
- **Remaining limit:** a tactic can consult locals internally without emitting a descendant `TermInfo`; V2 therefore does not claim complete local-dependency labels.
- **V2 adjudication:** `STILL_OPEN`.

## GAP-006 — Nested tactic execution paths prevent broad fresh replay

- **Source theorem:** `AkraBazziRecurrence.T_isBigO_smoothingFn_mul_asympBound`, transition 55.
- **Exact state/action:** the transition above is present inside a compound proof; its Stage100 certificate reports `NO_EXACT_RECORDED_STATE_PATH`.
- **Required meaning:** independently reach the exact recorded before-state, execute the exact action, and compare the exact runtime after-state.
- **Why it matters:** formal trace provenance is strong, but a fresh replay certificate is stronger and isolates environment/tool drift.
- **Smallest counterexample:** 56/100 Stage100 rows were `UNSUPPORTED` for path reconstruction; this row is one of them.
- **Proposed layer:** verifier/extractor, not canonical syntax; retain nested tactic tree and executable prefix path during tracing.
- **V2 evidence:** exact historical byte ranges now identify real nested `InfoTree` occurrences during fresh whole-file elaboration. The 500-transition campaign reports selected, replayable, exact-fail, unsupported, and environment-mismatch denominators separately in `reports/LEAN_RUNTIME_REPLAY_V2.md`.
- **V2 adjudication:** `CLOSED_SOURCE` for broad nested-path acquisition; unsupported individual paths remain explicit campaign outcomes rather than claimed support.

## GAP-007 — Per-state namespace, notation, simp, and instance environments are only pinned indirectly

- **Source theorem:** `CategoryTheory.isVanKampenColimit_extendCofan`, transition 36.
- **Exact action fragment:** `simpa [Functor.const_obj_obj, Discrete.functor_obj, ...] using ...`.
- **Information lost:** open namespaces, scoped notation, local attributes, active simp lemmas, synthesized instances, and imports actually consulted by elaboration.
- **Why it matters:** the same tactic text and pretty state can elaborate differently when these environments differ.
- **Smallest counterexample:** the action names selected rewrite lemmas but not the implicit simp set or typeclass search trace.
- **Proposed layer:** environment provenance plus optional verifier trace; do not copy the whole environment into every state.
- **V2 evidence:** the snapshot records exact Lean/Mathlib identities, source and parent declaration, direct/transitive imports, namespace, open declarations, options, local instances, and an environment fingerprint.
- **Remaining limit:** consulted simp lemmas and typeclass/search traces are not generally present when the tactic emits no explanatory `TermInfo`; exact replay proves outcomes but does not explain all search dependencies.
- **V2 adjudication:** `STILL_OPEN`.

## GAP-008 — Prior structured deltas are unreliable on multiline states

- **Source theorem:** `AkraBazziRecurrence.T_isBigO_smoothingFn_mul_asympBound`, transition 55.
- **Exact state fragment:** the target spans two physical lines and local definitions such as `base_max : ℝ := ...` span multiple lines.
- **Information lost/distorted upstream:** the old source projection truncated the focused target and misparsed multiline declaration continuations. Across V3's sample, 659/2,000 state observations disagree with that old structured projection.
- **Why it matters:** `names_added`, `names_removed`, `target_changed`, and effect classes derived from a lossy parser can become incorrect supervision even when raw before/after states are valid.
- **Smallest counterexample:** the old target stops at the first line ending in `=`, while V3's raw-state decomposition retains the continuation.
- **Proposed layer:** replace derived effect labels with deltas computed from elaborated Lean identities; until then retain old labels as `recorded_effect`, not truth.
- **V2 evidence:** goals, locals, metavariables, focus, and targets are compared by real identities and expression trees. Historical effect classes remain `RECORDED_HISTORICAL_METADATA` and never determine V2 deltas.
- **V2 adjudication:** `CLOSED_IR`.

## Extension rule

Future canonical extensions still require source evidence, a mathematical role, a demonstrated loss, a cross-system interpretation, and a test. GAP-003, GAP-005, and GAP-007 remain acquisition/completeness problems; they do not justify copying arbitrary Lean implementation state into the neutral IR.
