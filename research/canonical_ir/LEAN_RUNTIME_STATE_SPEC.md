# LeanRuntimeState V2 Specification

Version: `lean-runtime-state-v2.0.0`  
Authority: Lean `v4.10.0-rc1` (`3b58e0649156`) at Mathlib `29dcec074de168ac2bf835a77ef68bbe069194c5`.

## Boundary

`LeanRuntimeState` is source-specific. It is emitted inside Lean while a file is freshly elaborated and is not CanonicalMathState. The extractor reads `TacticInfo.mctxBefore`, `goalsBefore`, `mctxAfter`, and `goalsAfter`; Python never recovers an identity or expression tree from pretty text.

The transport root records the source file, direct imports, target counts, and captures. Each capture records the theorem, historical transition index, fresh trace ordinal, exact UTF-8 byte range, `InfoTree` path, before/after runtime states, elaborated references, context provenance, and a diagnostic pretty view.

## Expression serialization

The recursive `Expr` union preserves all Lean 4.10 constructors:

| Lean constructor | Serialized evidence |
|---|---|
| `bvar` | De Bruijn index |
| `fvar` | raw `FVarId.name` |
| `mvar` | raw `MVarId.name` |
| `sort` | recursive universe `Level` |
| `const` | declaration `Name` and every universe argument |
| `app` | function and argument, including implicit elaborated applications/coercions |
| `lam` | binder display name, `BinderInfo`, type, and body |
| `forallE` | binder display name, `BinderInfo`, type, and body |
| `letE` | name, type, value, body, and Lean's non-dependent hint |
| `lit` | tagged natural or string value |
| `mdata` | tagged `KVMap` projection plus underlying expression |
| `proj` | structure type name, field index, and structure expression |

`Level` preserves `zero`, `succ`, `max`, `imax`, `param`, and universe metavariables. No delaboration, pretty parsing, implicit-argument reconstruction, or coercion guessing occurs.

Syntax-valued metadata is retained as a tagged diagnostic projection rather than claimed to be a lossless `Syntax` serialization. `Expr.mdata` is definitionally transparent, so the canonical adapter delegates its source payload while retaining the underlying expression.

## Local context and binders

Every goal declaration retains:

- raw `FVarId`;
- local-context index;
- user-facing name (diagnostic, never identity);
- `BinderInfo`;
- `cdecl`/`ldecl` role;
- `LocalDeclKind`, including generated/implementation-detail declarations;
- elaborated type and optional value;
- local-instance class and FVar expression.

Alpha-renaming changes only diagnostic binder spelling. Shadowed declarations remain distinct by FVar identity and context index.

## Goals and metavariables

Goal identity is the real `MVarId`. The ordered goal list and focused first goal are explicit. Reordering therefore preserves goal identity and changes order/focus rather than manufacturing delete/create events.

The state records full `MetavarContext` declaration/assignment counts and a typed inventory for the transitive closure reachable from goals, their targets, local declarations, and assignments. A direct Lean-side before/after comparison separately emits every created or newly assigned metavariable and changed assignment, including compact expression fingerprints. Fully serialized declarations are retained for the relevant closure. This avoids duplicating gigabytes of accumulated inactive contexts while preserving the identity changes caused by the selected tactic.

Expression assignments, universe assignments/depths, delayed assignments, `syntheticOpaque`, and context counters are source fields. Lean 4.10 exposes no standalone generic constraint table; V2 says so explicitly instead of inventing one.

## References

For each selected `TacticInfo`, the extractor traverses descendant elaborated `TermInfo.expr` values:

- `Expr.const` occurrences become external constant evidence;
- `Expr.fvar` occurrences become local-context reference evidence.

Mechanism: `DIRECT_TRAVERSAL_OF_ELABORATED_TERMINFO_EXPRS`.

Completeness is `PARTIAL_TACTICS_WITHOUT_TERMINFO_MAY_HIDE_INTERNAL_USE`: tactic implementations such as search procedures can consult hypotheses or declarations without leaving a descendant `TermInfo`. These references are stronger than lexical matching but are not mislabelled as complete dependency traces.

## Environment provenance

The inner Lean capture retains the parent declaration, current namespace, open declarations, active options, transitive imported modules, main module, and local instances. The transport envelope adds source file and direct imports. The campaign manifest adds the exact Lean build, Mathlib commit, LeanDojo commit, host platform, and a runtime-pin fingerprint. The canonical adapter explicitly joins these three layers; compact audit rows retain their hashes and small identity fields rather than duplicating the entire Mathlib environment per state.

## Replay path

The historical `.ast.json` supplies the exact source byte range after theorem-scoped filtering and deduplication. Fresh file elaboration executes the real nested proof prefix. The new extractor selects the corresponding `TacticInfo` by byte range and records its complete `InfoTree` child-index path. This is classified as `FRESH_WHOLE_FILE_ELABORATION_EXACT_INFO_TREE_PATH`, not a guessed flat tactic list.

## Determinism and ordering

Raw FVar/MVar names are stable within one elaboration and authoritative for identity-aware deltas. They may be ephemeral across independent runs. Arrays whose order is semantically meaningful—local context, goals, focus—preserve Lean order. Hash-map inventories are treated as unordered and normalized by declaration creation index at the canonical boundary.

The JSON Schema is [`schemas/lean_runtime_state_v2.schema.json`](../../schemas/lean_runtime_state_v2.schema.json). The implementation is [`scripts/extract/LeanRuntimeExtractV2.lean`](../../scripts/extract/LeanRuntimeExtractV2.lean).
