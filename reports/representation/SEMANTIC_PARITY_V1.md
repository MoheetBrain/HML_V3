# Semantic Parity Audit V1

**Status: PASS.** All candidates are evaluated on the same 1,000 canonical transitions.

Parity means exact render/parse equality of the shared model-facing semantic projection. It does not mean that the surfaces are equally learnable.

| Renderer | Exact round trips | Deterministic | Mean UTF-8 bytes | Mean whitespace tokens | Status |
|---|---:|---:|---:|---:|---|
| `lean_like` | 1,000/1,000 | yes | 8,457.4 | 136.7 | **PASS** |
| `previous_hml` | 1,000/1,000 | yes | 11,656.5 | 643.4 | **PASS** |
| `typed_ast` | 1,000/1,000 | yes | 21,065.4 | 1,380.4 | **PASS** |
| `structured_english` | 1,000/1,000 | yes | 8,504.4 | 145.7 | **PASS** |
| `canonical_sexpr` | 1,000/1,000 | yes | 8,433.4 | 128.7 | **PASS** |
| `graph_edges` | 1,000/1,000 | yes | 8,782.4 | 119.7 | **PASS** |
| `goal_local` | 1,000/1,000 | yes | 9,495.8 | 120.2 | **PASS** |
| `dependency_topological` | 1,000/1,000 | yes | 10,270.0 | 119.7 | **PASS** |
| `explicit_redundant_state` | 1,000/1,000 | yes | 8,845.8 | 158.9 | **PASS** |
| `minimal_machine_code` | 1,000/1,000 | yes | 6,312.5 | 119.7 | **PASS** |

## Previous-HML qualification

The previous HML candidate is imported read-only at commit `b011511e72572608eb7836d3b8a1a6bb794c890d`. Declarations, goals, tactic text, premise dependencies, and effect maps occupy native old-HML fields. Binder metadata, per-goal context membership, metavariables, namespace references, and V3-only state fields are carried in the old view's visible `source` JSON block. Its parity result is therefore a compatibility-bridged baseline, not evidence that old HML natively modeled every V3 field.

## Scope

These checks establish serializer determinism and semantic preservation only. No representation is selected, no model is trained, and the whitespace counts are not used as a proxy for learning quality.
