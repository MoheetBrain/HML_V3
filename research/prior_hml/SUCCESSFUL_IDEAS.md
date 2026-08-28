# Successful Ideas Retained from Previous HML

These are design ideas supported by implementation or experimental evidence. Retaining them does not privilege the old surface syntax.

1. **Semantic state is primary; text is a view.** The old model-facing view already enforced `parse(render(transition)) == transition`. V3 generalizes this by placing a representation-neutral projection ahead of every candidate renderer.
2. **Determinism is testable.** Stable ordering, explicit identifiers, and byte-level renderer checks are kept. All ten V3 candidates currently pass deterministic re-rendering on 1,000 transitions.
3. **Literal UTF-8 is model-facing data.** The old forensic work measured a 3.41 percentage-point penalty from ASCII Unicode escaping on its task. V3 serializers use literal mathematical glyphs and audit literal `\\uXXXX` sequences.
4. **Verification is separate from proposal.** The old rule that status is verifier-owned is preserved and strengthened: formal-trace acceptance and fresh exact replay are separate V3 labels.
5. **Unknown is not false.** Missing expression ASTs, binder info, metavariable assignments, and replay paths are explicit information-accounting states, never guessed values.
6. **Claims, goals, candidates, branches, and obligations are different roles.** V3 does not collapse these distinctions; it only instantiates roles justified by current Lean data.
7. **Open source-specific fields are safer than invented grammar.** The previous view used JSON for genuinely open payloads. V3 uses an explicit source-specific fallback to preserve raw Lean observations while the canonical schema remains honest.
8. **Failure classification matters.** Representation, data, verifier, source-acquisition, policy, and core-language gaps are separated so a bad experiment does not automatically mutate semantics.

The retained ideas are architectural controls. Whether their old textual realization helps a neural policy remains an empirical question.
