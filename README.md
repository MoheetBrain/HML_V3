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

## Current milestone

`LEAN_PIPELINE_V1`: pin a real Lean/Mathlib source, preserve proof-state transitions,
adapt them into a representation-independent IR, and test information preservation across
multiple deterministic renderers. No model training or GPU work belongs in this milestone.

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
