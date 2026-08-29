# HML V3 — Mathematical Representation Discovery System

> **Read [`PROJECT_GOAL.md`](PROJECT_GOAL.md) first.** It states the permanent objective and
> outranks every roadmap, milestone and report here. The short version: the project succeeds
> only if a discovered representation measurably improves a human-plus-AI system's
> mathematical reasoning — not because a metric improved, a search converged, or the syntax
> looks clean.

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

## Open-ended representation discovery

Since `OPEN_ENDED_SEARCH_V2` the search can widen its own space. V1 could only recombine 42
human-chosen axes, so an idea outside the genome had zero probability of being found. V2 puts a
model-driven meta-designer inside the loop, behind a typed channel:

```text
    meta-designer  ->  JSON proposal  ->  schema validation  ->  static safety check
                                                              ->  projection-hook binding
                                                              ->  genome v2.N+1  ->  candidate
```

It can propose eight things, and the five that are not representation mutations matter most: it
can say the **corpus** cannot answer a question, that an **instrument** is measuring the wrong
thing, or that a **microtest** is missing. Three of this project's measured results were of
exactly that kind — goal linearization was unmeasurable at 1.01 goals per state, a detection
metric had saturated, and two locality instruments were wrong.

Free-form model text never reaches a file, a genome or the compiler. An invented axis is
accepted only when its stated behaviour binds to an executable projection hook **and** at least
two of its values render differently; the loop has produced axes that pass both checks and axes
that fail the second, and both outcomes are recorded.

```sh
PYTHONPATH=src python3 scripts/search/run_open_ended_search.py --generations 14
PYTHONPATH=src python3 scripts/search/run_neural_probe.py --arms A B --checkpoint 20
PYTHONPATH=src python3 scripts/search/build_frontier_v2.py
```

Start with
[`research/representation_search_v2/OPEN_ENDED_SEARCH_SPEC.md`](research/representation_search_v2/OPEN_ENDED_SEARCH_SPEC.md).

## Representation architecture search (V1, frozen)

The language is a dependent variable, and since `REPRESENTATION_SEARCH_V1` it is also *data*.
A candidate representation is a `RepresentationGenome` — a point in a 42-axis discrete space
of 4.095e19 points — consumed by **one** generic compiler. No candidate has renderer code of
its own, so two candidates cannot differ by an implementation accident and any candidate is
reproducible from `(genome_sha256, compiler_version, canonical_state_version)`.

```text
CanonicalMathTransition V2  ->  projection  ->  Document  ->  surface  ->  text
                            <-              <-            <-
```

Parsing runs the same pipeline backwards from the same genome, so losslessness is a property
of the codec rather than a per-candidate promise. A candidate that hides declared-contract
content fails the round-trip gate and is never scored — it cannot buy a smaller token count
with a semantic loss.

```sh
PYTHONPATH=src python3 scripts/audit/stream_runtime_v2_corpus.py \
    --campaign-dir external/runtime_probe/campaign500
PYTHONPATH=src python3 scripts/search/run_representation_search.py --generations 12
PYTHONPATH=src python3 scripts/search/build_search_report.py
```

The search is resumable: state lives in `data/representation_search/` and re-invoking the
driver continues from the exact next generation. It never reads the sealed split.

Start with [`research/representation_search/OBJECTIVES.md`](research/representation_search/OBJECTIVES.md)
for what the search can and cannot establish, and
[`research/representation_search/HML_FAILURE_MEMORY.md`](research/representation_search/HML_FAILURE_MEMORY.md)
for the recorded negatives that constrain it.

## Scientific rules

- Verifiers certify truth; model and human outputs are proposals until checked.
- Raw source observations remain preserved beside normalized fields.
- Dataset trust tier and verification status are separate, explicit fields.
- Invalidated and negative results remain visible historical evidence.
- Large external datasets are referenced by manifests and acquisition scripts, not copied
  into Git.
- A renderer may lose presentation detail only when the loss is documented and excluded
  from the declared semantic parity contract.
- A measurement that cannot discriminate is reported as non-discriminative, never as
  agreement.
- Token counts name their vocabulary; byte counts and tokenizer-free pre-token counts are
  reported beside them.
- No representation is claimed optimal for neural reasoning without model evidence. What
  exists is inference-only microprobe evidence at a preregistered sample size, reported with
  the rule that produced it and with its dumb-control veto.
- Corruption tests are applied to the canonical state, upstream of every candidate, so no
  syntax family is asked an easier question than another.
- An instrument is checked against a real rendering before any number it produces is reported.

See [ROADMAP.md](ROADMAP.md), [DECISIONS.md](DECISIONS.md), and
[data/README.md](data/README.md).

Reproduce the foundation gates with:

```sh
PYTHONPATH=src python3 scripts/verify/audit_losslessness.py
PYTHONPATH=src python3 scripts/verify/audit_renderer_parity.py
PYTHONPATH=src python3 -m unittest discover -s tests -v
```
