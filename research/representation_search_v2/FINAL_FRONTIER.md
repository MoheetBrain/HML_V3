# The V2 Frontier — method

The generated result lives in
[`reports/representation_search_v2/FINAL_FRONTIER.md`](../../reports/representation_search_v2/FINAL_FRONTIER.md).
This file records how it is produced and what it is allowed to say.

## Reproducing it

```sh
# 1. acquire transitions targeted at a measured gap, not at random
PYTHONPATH=src python3 scripts/extract/acquire_targeted_transitions.py \
    --runtime-root external/runtime_work/.../mathlib4 \
    --exclude-selection external/runtime_probe/campaign500/selection.jsonl \
    --exclude-selection external/runtime_probe/campaign500b/selection.jsonl \
    --output data/manifests/targeted_pool_v2.source.jsonl.gz \
    --manifest data/manifests/targeted_pool_v2.manifest.json

# 2. elaborate them in Lean, canonicalize, merge
PYTHONPATH=src python3 scripts/extract/prepare_lean_runtime_campaign_v2.py ...
PYTHONPATH=src python3 scripts/replay/run_lean_runtime_campaign_v2.py ...
PYTHONPATH=src python3 scripts/audit/stream_runtime_v2_corpus.py ...

# 3. freeze the new seal BEFORE the search
PYTHONPATH=src python3 scripts/search/create_sealed_v2.py

# 4. the open-ended search; resumable, never reads the seal
PYTHONPATH=src python3 scripts/search/run_open_ended_search.py --generations 14

# 5. evidence
PYTHONPATH=src python3 scripts/search/run_neural_probe.py --arms ... --checkpoint 20
PYTHONPATH=src python3 scripts/search/build_frontier_v2.py
PYTHONPATH=src python3 scripts/search/emit_side_by_side_examples.py
```

## What a finalist has survived

| Stage | What it proves |
|---|---|
| compile + lexicon | the genome describes a language at all |
| semantic round-trip | the declared contract is recoverable |
| determinism, glyph fidelity, structural recoverability | it is a function of the object, in UTF-8, not one opaque literal |
| semantic-level corruption | it exposes defects introduced upstream of every candidate |
| nine structural-access suites | specific questions are answerable, and how expensively |
| static cost and locality | what it costs under a named vocabulary |
| four exact tokenizers | whether that cost ordering is a vocabulary artifact |
| validation replication | the gain was not an artifact of the dev sample |
| neural microprobe | a frozen model can or cannot read it, at a preregistered sample size |
| sealed evaluation | it holds on families the search never influenced |

## Why more than one finalist is the honest answer

The axes trade against each other and there is no principled exchange rate between "costs 20%
fewer tokens" and "answers binder queries in half the distance". Forcing a single winner would
mean inventing that exchange rate and hiding it in a weighting. The shortlist rule is stated
instead: the best candidate on each selection axis, plus the knee, with equivalent measurement
vectors collapsed first.

## The claim ladder

| Statement | Supported? |
|---|---|
| These preserve the declared semantic contract | Yes — hard gate |
| A candidate is reproducible from its genome hash across processes | Yes — verified |
| An invented axis changed the measurement | Yes — observable-effect gate, `FM-026` |
| Candidate A costs fewer tokens than B under vocabulary V | Yes — exact BPE |
| Candidate A costs fewer tokens under *any* vocabulary | Only if the multi-tokenizer audit agrees |
| Candidate A answers binder queries more cheaply | Yes — microtest, canonical ground truth |
| A frozen model reads A better than B | **Only** at the sample size and rule reported |
| A is the best machine language for mathematics | **No** |

## What would change the answer

A matched, control-gated model experiment on the finalists: frozen inference first, the six
lexical controls `FM-003` requires, a task that does not saturate (`FM-010`), and only then any
adaptation. Nothing in this repository performs that experiment.
