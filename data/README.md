# Data policy

`data/registry/datasets.yaml` is the canonical dataset ledger. `data/manifests/` records
immutable source identities and checksums. Large payloads live outside Git under local cache
roots and are reacquired through scripts.

Trust tiers:

- **A — FORMALLY_VERIFIED_TRAJECTORY:** verifier-checked proof or transition. Fresh replay
  evidence and source-trace evidence remain distinguishable in `verification_status`.
- **B — FORMAL_STATEMENT_OR_PARTIAL_OBJECT:** formal statement without a checked proof.
- **C — NATURAL_REASONING_PROCESS_SIGNAL:** human/model reasoning with process labels.
- **D — NATURAL_MATH_PROBLEM_SOLUTION:** informal problem and solution.
- **E — OLD_SYNTHETIC_HML:** historical synthetic HML data.

An external source is not copied into this repository unless its license, size, provenance,
and scientific need justify redistribution.

