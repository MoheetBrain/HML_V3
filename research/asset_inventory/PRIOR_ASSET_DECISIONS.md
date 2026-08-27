# Prior asset decisions

`REFERENCE` means use in place without copying; `REACQUIRE` means no local artifact was found; `HISTORICAL_ONLY` excludes an asset from new truth/training while preserving it for audit.

| Asset | Decision | Status | Use in V3 |
|---|---|---|---|
| amps_khan_local | REFERENCE | NATURAL_LANGUAGE_UNVERIFIED | 721 topics. Redistribution blocked until source and license are resolved. |
| closed_loop_solver_pilot | REFERENCE | NEGATIVE_ZERO_SOLVED_ALL_ARMS | Long-horizon calibration evidence and failure taxonomy. |
| common_envelope_10k | REFERENCE | NEGATIVE | Causal correction: common envelope reversed the apparent HML gain to -2.77pp. |
| domino_v1 | HISTORICAL_ONLY | NOT_DIAGNOSTIC | Next-action candidate semantics and an example of a benchmark that was not diagnostic. |
| domino_v1_historical | REFERENCE | HISTORICAL_NEXT_ACTION_INSTRUMENT_NOT_DIAGNOSTIC | Preserve candidate semantics and the negative/non-diagnostic learning result. |
| domino_v2 | HISTORICAL_ONLY | NEGATIVE_STILL_COLLAPSED | Failure evidence for target learnability, leakage, loss/pooling, and capacity hypotheses. |
| exp_rep_validity_stage1 | REFERENCE | NEGATIVE_OR_UNCERTAIN | Latest clean four-arm representation comparison and lexical-shortcut warning. |
| exp_rep_validity_v1 | REFERENCE | VALID_INSTRUMENT_WITH_LEXICAL_SHORTCUT_LIMITATION | Stage 1: Structured English > Lean-like > HML > typed AST on IID; HML led no split. Preserve as negative/uncertain evidence. |
| final_hml_signal | HISTORICAL_ONLY | CONFOUNDED | Forensic record of a +35.55pp result later explained by arm-specific envelope confounding. |
| gold_10_historical | REFERENCE | HISTORICAL_ADJUDICATED_NOT_FORMAL_PROOF | Keep manifests, trajectories, rerun reports, and gap triage together. |
| gold_125_historical | REFERENCE | HISTORICAL_ADJUDICATED_NOT_FORMAL_PROOF | Preserve branch audits, dependency graphs, disagreements, selection, and gap reports. |
| gold_25_historical | REFERENCE | HISTORICAL_ADJUDICATED_NOT_FORMAL_PROOF | Preserve selection, operation registry, audits, and semantic gaps. |
| hendrycks_math_train_local | REFERENCE | NATURAL_LANGUAGE_UNVERIFIED | Fields: problem, level, type, solution. Natural-language solutions are not proof certificates. Redistribution blocked until license is resolved. |
| herald_proofs_local | REFERENCE | FORMAL_PROOF_TEXT_NOT_REPLAYED_IN_V3 | Strong source for aligned formal/informal proof research after replay and mismatch filtering. |
| hml50k_final_historical | REFERENCE | FORMAL_TRACE; REPRESENTATION_INFERENCE_INVALIDATED | Retain for regression, serializer failure analysis, and source recovery only. |
| hml_eval_001 | HISTORICAL_ONLY | NEGATIVE_NULL_REDESIGN | Earliest frozen paired HML evaluation and protocol lessons. |
| hml_model_experiments | REFERENCE | MIXED_NEGATIVE_INVALIDATED | Syntax acquisition, B1/B2, VNext, reverse-projection, and causal-autopsy evidence. |
| hml_phase2_vnext | REFERENCE | MIXED_NEGATIVE; HML_INPUT_HURTS; NO_COHERENT_V2_MECHANISM | Syntax acquisition, verdict/applicability, state delta, execution LoRA, four-arm VNext, reverse projection, and causal-mechanism evidence. |
| lean_attestation_stage100 | REFERENCE | 32_REPLAY_PASS; 68_NONPASS; STAGE1K_BLOCKED | All 32 reached target actions matched both recorded states exactly; Stage100 overall gate failed due nested-state reconstruction coverage. |
| lean_domino_v2_canonical_records | REFERENCE | FORMAL_TRACE; 32_OF_SEPARATE_STAGE100_FRESHLY_REPLAY_CERTIFIED | Contains raw tactic and raw before/after states plus parsed hypotheses/target. This is the initial V3 adapter input. |
| lean_pipeline_v1 | REFERENCE | 1000_FORMAL_TRACE_ACCEPTED; 32_FRESH_EXACT_REPLAY_PASS; 968_NOT_FRESHLY_REPLAYED | Balanced across eight observed effect classes; 1,353 official annotated premise references on 578 rows; every transition has exact theorem source and exact before/action/after join. |
| lean_runtime_attestation | REFERENCE | PARTIAL_PASS_GATE_FAIL | Fresh verifier certificates and exact limits of flattened LeanDojo traces. |
| lean_workbook_pinned | REFERENCE | DATASET_CARD_COUNTS; PROOFS_NOT_REPLAYED_IN_V3 | Registered as a formalization/proof source, not as verified transitions. Acquisition is metadata-only by default. |
| leandojo_benchmark4 | REFERENCE | FORMAL_TRACE_SOURCE; NOT_FRESHLY_REPLAYED_PER_ROW | Primary current local source of real proof-state trajectories. |
| lossless_hml_solver | REFERENCE | SOLVER_NOT_CALIBRATED | Hard stop evidence: RAW solved 2/48, below the preregistered floor, so HML training/evaluation did not run. |
| minif2f_lean4_pinned | REFERENCE | PINNED_BENCHMARK_STATEMENTS; 498_SORRY_OR_ADMIT_OCCURRENCES | Useful for later evaluation after an explicit split audit and build/replay verification. |
| minilang_audit | REFERENCE | AUDIT | Operation semantics, translation failures, and lessons for representation-neutral design. |
| numinamath_lean_local | REFERENCE | MIXED; 37,168_ROWS_HAVE_TEXTUALLY_SORRY_FREE_PROOF_BUT_NOT_REPLAYED_HERE | Potential formal-statement/proof source after environment pinning and replay verification. |
| openai_prm800k_official | REFERENCE | NATURAL_PROCESS_LABELS_NOT_LOGICAL_VALIDITY | Useful for action utility, failure, progress, and discovery graphs; never treat -1/0/+1 as Lean validity. |
| pretrained_hml_signal | REFERENCE | HML_AST_EQUIVALENT_SO_FAR | Zero-shot, direct-head, adapter, depth, token, and full-DEV evidence. |
| pretrained_hml_signal_paired | REFERENCE | HISTORICAL_REPRESENTATION_DATA; RESULT_CHAIN_MIXED_NEGATIVE | Reference for prior paired-rendering methods and failures; do not duplicate the 694MB payload. |
| proofnet_lean4_port_pinned | REFERENCE | PINNED_PORT_STATEMENTS; THEOREM_BODIES_REMAIN_SORRY | Potential translation/evaluation source, not current formal-trace evidence. |
| pythagoras_sft_local | REFERENCE | MIXED_SFT_TEXT; NOT_FORMAL_TRAJECTORY_TRUTH | Historical external source; keep referenced until a V3-specific audit determines utility. |
| reasoning_layer_v1 | REFERENCE | VALID_HISTORICAL_RESULT | Evidence about where one-step state/action signal lives after the common-envelope correction. |
| representation_arena_b1_b2 | REFERENCE | MIXED_NEGATIVE; B2_GENERIC_SEXPR_WON | Implication, next-action replication, binder, quantifier-scope, and generic S-expression evidence. |
| semantic_firewall_fx2 | REFERENCE | FROZEN_INTEGRATOR_FIXTURES; 13_INTENTIONAL_REFERENCE_DIVERGENCES | Regression and semantic-gap evidence only. |
| semantic_firewall_v1 | REFERENCE | FROZEN_EXTERNAL_ACCEPTANCE_FIXTURES_WITH_KNOWN_BLIND_SPOT | Historical regression asset, not formal mathematical truth. |
| state_tactic_pairs_local | REFERENCE | STATE_ACTION_ONLY; NO_AFTER_STATE; NOT_REPLAYED | Usable only after stripping prompt/retrieval material, reconstructing theorem keys, and replaying tactics. |
| stp_lean_0320_local | REFERENCE | CLAIMED_MACHINE_CHECKED_AT_GENERATION; NOT_REPLAYED_IN_V3 | Large candidate source. Do not ingest before environment/version recovery and a replay sample. |
| vnext_10k_historical | REFERENCE | MIXED_PROVENANCE_HISTORICAL; NOT_UNIFORM_FORMAL_TRUTH | Preserve canonical records, all four views, reverse projection, leakage audits, and exact manifest. |
| vnext_600_historical | REFERENCE | SYNTHETIC_HML_VERIFIER_LABELLED | Historical regression and failure-analysis source only. |
