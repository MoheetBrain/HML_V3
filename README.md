# HML V3 — Mathematical Representation Discovery System

HML V3 is an evidence-first research system for discovering which machine-facing
representation best supports verified mathematical reasoning.

The mathematical substrate is held fixed while representations vary:

```text
formal source -> verified proof transition -> CanonicalMathState
                                                |
                      +-------------------------+-------------------------+
                      |            |            |            |           |
                   Lean-like   prior HML    typed AST   English     other views
```

The language is a dependent variable. This repository does not presume that previous HML
syntax, Lean syntax, a graph encoding, or natural language is optimal.

## Foundation result

`LEAN_PIPELINE_V1` is implemented on 1,000 unique Mathlib theorems: exact theorem source,
before/action/after observations, 1,353 official annotated premise references, a canonical
adapter, and ten deterministic renderer candidates. Declared-observation losslessness and
semantic parity both pass on all 1,000 rows. Only 32 transitions carry fresh exact-replay
certificates; the other 968 retain the calibrated `FORMAL_TRACE_ACCEPTED` label.

No renderer is selected as the final language. No model training or GPU work was performed.

## Lean runtime V2 workflow

V2 uses a Lean-side extractor over exact `TacticInfo` objects; it does not parse identities
from the pretty goal view. The CPU-only workflow is:

1. `scripts/extract/prepare_lean_runtime_campaign_v2.py` joins selected V1 records to exact
   source byte ranges in the pinned LeanDojo trace;
2. `scripts/replay/run_lean_runtime_campaign_v2.py` freshly elaborates the pinned Mathlib
   files and captures structured before/after states at those nested occurrences;
3. `scripts/audit/build_runtime_v2_audits.py` produces compact, content-hashed reports and
   canonical samples while raw multi-gigabyte captures remain ignored.

The runtime and canonical contracts are documented under `research/canonical_ir/`.
Representation benchmarking remains gated; V2 does not select a language.

## Scientific rules

- Verifiers certify truth; model and human outputs are proposals until checked.
- Raw source observations remain preserved beside normalized fields.
- Dataset trust tier and verification status are separate, explicit fields.
- Invalidated and negative results remain visible historical evidence.
- Large external datasets are referenced by manifests and acquisition scripts, not copied
  into Git.
- A renderer may lose presentation detail only when the loss is documented and excluded
  from the declared semantic parity contract.

See [ROADMAP.md](ROADMAP.md), [DECISIONS.md](DECISIONS.md), and
[data/README.md](data/README.md).

Reproduce the foundation gates with:

```sh
PYTHONPATH=src python3 scripts/verify/audit_losslessness.py
PYTHONPATH=src python3 scripts/verify/audit_renderer_parity.py
PYTHONPATH=src python3 -m unittest discover -s tests -v
```
