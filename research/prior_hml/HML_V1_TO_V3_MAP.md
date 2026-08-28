# Previous HML to V3 Mapping

Status: **complete as an evidence/migration audit; not an assertion of semantic identity.**

Authority inspected read-only:

- executable/model-facing HML at `b011511e72572608eb7836d3b8a1a6bb794c890d`;
- HML Standard at `e879f5f` (inventory HEAD) and its model reference, architecture, schemas, and semantic atlas;
- historical corpus and experiment artifacts catalogued in `research/asset_inventory/`.

V3 does not import the old ontology as its foundation. The table accounts for every old semantic-state record kind and transition component, then states what current Lean evidence justifies.

| Previous HML construct | V3 destination | Mapping | Evidence decision |
|---|---|---|---|
| `SemanticState` | `CanonicalMathState` | partial structural correspondence | V3 owns source-neutral state; HML is one renderer. |
| `Claim` | `Declaration` when it is a Lean local declaration | conditional | A typed local binder is observed. A generic epistemic proposition is not silently converted. |
| `Candidate` | no dedicated V1 pipeline field | intentionally unmapped | The 1,000 formal transitions contain no verified candidate lifecycle observation. Use a future empirically justified extension, not an inherited field. |
| `Branch` | goal labels and multiple goals, but not old branch lifecycle | partial | Lean prints cases/goals; `JOINED`/`ABANDONED` are not present in the trace. |
| `Goal` | `Goal` | direct for target/status/local context | V3 additionally retains per-goal context membership and Lean case labels. |
| `Obligation` | `CanonicalMathState.obligations` | reserved generic record | Current pretty-printed traces expose goals, not separately typed old-HML obligations. |
| `EvidenceRecord` | state `evidence` plus `VerifierResult` | split by role | Source observation and verifier verdict are separated so producers cannot self-certify. |
| `Action.operation` | `CanonicalAction.action_kind` | direct | Initial adapter uses `LEAN_TACTIC`. |
| `Action.summary` | `CanonicalAction.source_syntax` | direct | Exact tactic bytes and SHA-256 are retained. |
| `Action.dependencies` | `referenced_premises` | direct after formal-source join | 1,353 official LeanDojo annotated references occur in 578/1,000 rows. |
| action open maps | `arguments`, `substitutions`, `expected_effect`, `StateDelta` | explicit V3 fields where evidence exists | No HML-specific keys become canonical semantics merely because the old map allowed them. |
| `active_scopes` / claim scope | declaration `scope_id`, goal `local_context_ids`, state `scopes` | refined | V3 represents membership per displayed goal instead of only one active-scope tuple. |
| old status enums | goal status and verifier result | narrowed at this adapter | Only `OPEN`, terminal no-goals, formal trace acceptance, and calibrated replay status are asserted. |
| `Transition.source` | `provenance`, `namespace_environment_refs`, `source_specific` | split | Mathematical environment, corpus provenance, and lossless source fallback are not conflated. |
| old neutral JSON | canonical dataclass JSON | replaced | V3 schema derives from source observations and declares information accounting. |
| old model-facing view | `previous_hml` candidate renderer | preserved read-only | Imported at the exact frozen commit; not copied into the canonical layer. |
| HML parser/compiler/kernel | no V3 canonical authority | historical/external verifier candidate | The pinned prior repositories remain read-only and do not define V3 semantics. |

## Compatibility bridge

The `previous_hml` candidate populates native old-HML claims, goals, action, dependencies, and effect maps. Old HML has no native fields for per-goal context indices, Lean metavariables, binder metadata, or namespace pins, so those appear in its supported, visible `source` JSON block. The bridge is parsed back and checked over all 1,000 rows. This is why previous-HML parity can pass without pretending the old ontology was already complete.

## Decision

Every previous semantic-state component has an explicit V3 disposition: direct, refined, reserved, deliberately unmapped, or historical-only. No old construct is silently dropped, and no construct without real source evidence is promoted into the canonical core.
