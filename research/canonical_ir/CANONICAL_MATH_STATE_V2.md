# CanonicalMathState V2

Version: `canonical-math-transition-v2.0.0`.

## Purpose

CanonicalMathState V2 carries mathematical distinctions demonstrated necessary by actual elaborated Lean states. It does not copy Lean bookkeeping wholesale. `LeanRuntimeState → CanonicalMathState` is an explicit adapter boundary.

## Canonical additions over V1

1. **Neutral expression trees.** Lean constructors map to bound variables, local/metavariable references, sorts, symbols, applications, lambdas, dependent functions, lets, literals, annotations, and projections. Constant identity and universe arguments survive. Coercions survive as their elaborated symbol/application structure.
2. **Scoped declaration identity.** A declaration has a canonical state-local identity derived from source context order; raw FVar IDs remain in the source reference.
3. **Goal identity and focus order.** Goals retain canonical identities derived from Lean metavariable creation identity, with an explicit ordered focus list.
4. **Relevant metavariables.** Types, assignments, kinds, and relevant universe assignments survive where they affect the mathematical state.
5. **Separated dependencies.** Actions distinguish official annotated `external_premise_refs` from elaborated `local_context_refs`, including mechanism and completeness. The broader descendant-TermInfo constant set remains source-specific because a type/function constant occurrence is not automatically a premise label.
6. **Identity-aware deltas.** Goal, local declaration, metavariable, focus, reference, and expression changes come from elaborated identities.
7. **Information accounting.** Every state distinguishes preserved content, source-delegated content, Lean-specific content, and information Lean did not expose.

## Source-specific fields not promoted

- raw `_uniq` spelling of FVar/MVar/LMVar identities;
- name-generator state and metavariable counters/depth policy;
- `LocalDeclKind` implementation details except their evidence reference;
- complete inactive/irrelevant metavariable payloads (delegated by counts; created/assigned changes remain explicit);
- raw `Expr.mdata` key/value payloads;
- tactic elaborator names and `InfoTree` path;
- Lean option encodings, open-declaration syntax, and module tables;
- pretty-printed states.

These fields remain accessible through a hashed source reference because they support replay/debugging but do not yet have a demonstrated cross-system mathematical interpretation.

## `LeanStateEquivalent`

Independent runtime states are equivalent only when their normalized structural projections are exactly equal. V2 normalization:

1. maps FVar identity by local-context declaration order;
2. maps MVar identity by `MetavarDecl.index` (creation order), not display ordinal or current focus order;
3. maps referenced universe metavariables by first structural occurrence;
4. replaces lambda/forall/let binder spelling with `_` because bodies use De Bruijn indices;
5. sorts unordered relevant metavariable records by normalized identity;
6. excludes raw metadata payloads while retaining the annotated expression;
7. excludes the irrelevant full metavariable inventory from neutral equivalence; the source snapshot retains full context counts, while every created, assigned, or changed metavariable is represented explicitly.

No beta/iota/zeta reduction, unfolding, pretty-text normalization, theorem proving, typeclass search, or definitional-equality assumption is part of this relation. A goal reorder remains observable, including when targets are equal, because normalized MVar creation identities remain in `focus_order`.

## Losslessness criterion

`ELABORATED_LOSSLESSNESS` is not byte reconstruction of every Lean object. It asks whether all distinctions declared canonical-required above survive the adapter. Results are reported in five bins: preserved, delegated by source reference, intentionally Lean-specific, information lost, and unknown. Any loss that can change action legality blocks the benchmark gate.

The schema is [`schemas/canonical_math_state_v2.schema.json`](../../schemas/canonical_math_state_v2.schema.json), and the adapter/equivalence implementation is [`src/hml_v3/adapters/lean/runtime_v2.py`](../../src/hml_v3/adapters/lean/runtime_v2.py).
