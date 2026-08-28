# Search Objectives

## The epistemic limit, stated first

This search establishes a **pretraining representation frontier**. It cannot establish that
any representation is optimal for neural mathematical reasoning, and no result in this
repository should be read that way.

What static evaluation can settle:

- semantic fidelity against a declared contract, and completeness of what is exposed;
- deterministic identity: the same object always renders to the same bytes;
- representational cost in bytes, gzip bytes, tokenizer-free pre-tokens, and BPE tokens;
- locality: how far a reader must reach between a binder and its use, a premise and its
  action, a node and the node it references;
- structural recoverability: whether the reader can rebuild the object, and which
  corruptions it can detect;
- parser reliability, ambiguity, and redundancy;
- tokenizer behaviour under one pinned vocabulary.

What it cannot settle:

- whether any of this changes a model's conditional distribution over next actions;
- whether familiarity with pretrained syntax dominates every structural effect
  (`FM-002` suggests it may);
- whether a benchmark built on these representations would discriminate at all
  (`FM-010`: the last one saturated).

The honest objective is therefore: **find the strongest Pareto frontier obtainable before
expensive model adaptation, and hand a small, well-characterised set of finalists to a later
empirical stage.**

## Hard gates, not objectives

A candidate that fails any of these is rejected and never scored. `FM-008` is the reason:
compression must not be able to buy its way past a semantic failure.

| Gate | What it rejects | Recorded origin |
|---|---|---|
| `semantic_round_trip` | any loss of declared contract content | `D-002`, `D-009` |
| `deterministic_serialization` | a rendering that is a function of construction history | `FM-011` |
| `glyph_fidelity_utf8` | escaped spellings of glyphs the corpus contains | `FM-004` |
| `structural_recoverability` | a state emitted as one opaque literal | `FM-012` |
| `no_label_leakage` | the recorded effect class appearing as a token in the text | `FM-003` |
| `shape_distinct_rendering` | two structurally different transitions rendering identically | new |
| `AMBIGUOUS_LEXICON` (compile) | two semantic roles sharing one surface word | new |

`shape_distinct_rendering` compares *shapes*, not transitions: two alpha-variants should
render identically under alpha normalization, and penalising that would penalise the exact
invariance the canonical layer works to provide.

## The fitness vector

Nothing is collapsed to a scalar. Selection is non-dominated sorting over seven axes chosen
to be individually informative and jointly small — a Pareto computation over twenty weakly
informative axes makes almost everything non-dominated and stops selecting.

| Pareto axis | Direction | What it measures |
|---|---|---|
| `bpe_tokens_per_transition` | minimise | cost under the pinned GPT-2 vocabulary |
| `binder_use_distance_tokens` | minimise | mean token gap between mentions of one local identity |
| `premise_to_action_distance_tokens` | minimise | mean token gap from a premise to the action record |
| `detect_swap_records` | maximise | corruption detection for exchanged records |
| `detect_drop_field` | maximise | corruption detection for a dropped field line |
| `identifier_fragmentation` | minimise | mean BPE pieces per identifier |
| `max_reference_span_tokens` | minimise | the longest span the reader must hold open |

Measured and reported but **not** selected on: bytes, characters, pre-tokens, gzip bytes and
ratio, character distances, forward-reference rate, role-word fragmentation, structural
density, the other four detection families, and role-vocabulary entropy. They are diagnostics
and appear in every report.

`detect_corrupt_identity` was a candidate Pareto axis and was removed before the search
began: measured across all sixteen generation-zero seeds on the real corpus it read **1.000
for every one of them**. An altered identifier either fails to resolve or resolves to a
different declaration, so every candidate catches it. `FM-010` requires a saturated
instrument to be reported as non-discriminative rather than as agreement, so it is measured,
reported, and excluded from selection. `detect_drop_field` replaced it, spreading
0.000–0.792 over the same seeds.

## Two token measurements, both proxies

`pretokens_per_transition` uses the GPT-2 pre-tokenization regex and no vocabulary, so it
cannot favour whichever language a vocabulary was trained on. `bpe_tokens_per_transition`
uses the real pinned GPT-2 byte-level BPE.

The two disagree, and the disagreement is itself a finding worth stating plainly: the prior
tokenization audit used the Qwen3-8B vocabulary, in which every mathematical glyph the corpus
needs — `⊢`, `∀`, `ℝ`, `𝕜`, `✝` — is a **single token**. Under GPT-2 those same glyphs cost
three or more pieces each. Any absolute token ranking is therefore a statement about a
vocabulary, not about a representation. Rankings that survive both measurements are the ones
worth carrying forward.

## Anti-overfitting

The corpus is partitioned at the **Mathlib source file** level, not the transition level.
Sibling lemmas in one file share notation, instances and premise vocabulary, so a
transition-level split would leak.

| Split | Share | Who may read it |
|---|---|---|
| `SEARCH_DEV` | ~70% | the controller, every generation |
| `SEARCH_VALIDATION` | ~10% | the controller, for the honesty check |
| `SEALED_FINAL_EVALUATION` | ~20% | `SealedEvaluator` only, aggregates only, once |

The split is a keyed SHA-256 of the family name, so it is reproducible from the corpus alone
and cannot drift with corpus order. The driver refuses to continue a search whose split
manifest hash has changed. Every sealed access is appended to `sealed_access_log.jsonl`.

## Stopping rule

Structural convergence is declared when the frontier signature — the best value per Pareto
axis over the whole evaluated population — has not improved on any axis for five consecutive
generations, or the generation budget is exhausted. The result is named
`PRETRAINING_REPRESENTATION_FRONTIER_V1`. It is not a claim of universal optimality and the
report says so in those words.
