# MicroMath Lab V2 — specification

Lab version `micromath-lab-v2.0.0`. Rule `micromath-calibration-v2.0.0`.
Package `src/hml_v3/micromath/`.

V2 exists because V1 measured six broken instruments and reported the results as facts about a
language. Every change below is traceable to a specific measured failure.

## 1. What V1 got wrong, and what V2 does instead

| V1 | Why it failed | V2 |
|---|---|---|
| Identifiers left intact | `n : Nat` answers the TYPE question without the TYPE relation (`FM-041`) | Opaque tags: `v17`, `h4`, `t23`, `p8` |
| 2-choice, chance 0.500 | Too much room for priors to carry the answer | Up to 4 same-family distractors, chance ≈ 0.27 |
| Negative arm = decoy in the prompt | The relation was still in the text, so the reader read past the decoy | Negative arm = the relation **destroyed in the state** |
| Guard checked the split *name* | The run that spent both holdouts never named a split (`FM-043`) | Firewall keyed on a **provenance hash of the base state** |
| Fixed thresholds on point estimates | One flipped answer moves an arm by 0.042 at n=24 | Exact binomial bounds, Bonferroni where several rules are tested |
| Shortcut audit run once, at the end | 277 s of inference to discover a constant answer | Audit is a **hard gate before any inference** (`D-024`) |

## 2. Anonymisation (`MISSION §4`)

`anonymise.apply` rewrites the **whole record**, not one phase. The identity codec spans both
before and after states and the delta section is rendered from `state_delta`, so a rewrite
confined to `state_before` produces a page where one declaration wears two names — both
inconsistent and a fresh shortcut.

Two rules govern it. A rename is a **bijection within the state**: distinct declarations stay
distinct and every use site moves with its declaration. And a rename **never touches the
relation under test** — removing priors is `anonymise`'s job, destroying structure is
`ablate`'s, and confusing them would make every negative arm look valid for the wrong reason.

Which families are stripped is per-instrument: TYPE and PREMISE carry the loudest priors and
get the most aggressive treatment; the reference-following instruments only need opaque
declarations.

Tag spaces are sized from the population. The first version fixed the space at 90 and probed
by `index % 99 + 10`, which never terminated on a premise pool larger than 90.

## 3. Negative controls (`MISSION §7`)

The relation is destroyed **in the state**, before rendering, so every representation sees the
damage equally. Each ablation prefers a **derangement over a deletion**: permuting which type
attaches to which declaration keeps the token multiset identical and leaves every candidate
answer present and plausible, where deleting the types would shorten the page and announce
that something is missing.

| Component | What is destroyed | What is preserved |
|---|---|---|
| TYPE | the term→type association | every declaration, every type, every token |
| DEPENDENCY | the reference inside each declaration's type | objects, types, names, surrounding state |
| BINDER | which declaration each use in the target refers to | binders and uses |
| SCOPE | goal ownership | all declarations, all goals |
| PREMISE | which premise the action cites | a citation of the same shape and length |
| ACTION_ARGUMENT | the argument binding | the action and every candidate argument |
| EXPRESSION_DEPTH | the positions of the target's references | the reference set |

`ablate.changed` asserts the state actually moved. An ablation that silently returned its input
would make its own negative arm score like the positive one.

## 4. The split firewall (`MISSION §10`, `§11`)

`FM-043` was not caught by the guard in place, and the reason matters more than the bug: that
guard refused a script invoked with `--split micro_hidden`, and the run that consumed both
holdouts never named a split. It asked a shared pool for twelve fresh pairs and the pool
obliged.

So the firewall is keyed on `base_state_identity` — a hash of the transition id with its source
and provenance — and it:

- **fails closed**: an unregistered state is refused unless the caller explicitly asks to mint
- **refuses retired states permanently**: the V1 splits are spent, and excluding them from
  future runs does not make them clean again
- **asserts pairwise disjointness at runtime** across DEV, SHADOW, HIDDEN and SEALED
- **refuses a registry written by another version**, since the hash inputs may have changed

## 5. The calibration rule (`MISSION §8`, `D-023`)

Fixed before any V2 candidate was rendered:

```
CONFIDENCE     = 0.90     two-sided, exact binomial (Clopper-Pearson)
MINIMUM_RANGE  = 0.20     smallest P - N that can support a judgement
PARITY_MARGIN  = 0.10     on the paired difference
LADDER         = 12 → 24 → 32 → 48
```

- **POSITIVE valid** iff the lower bound on P exceeds chance.
- **NEGATIVE valid** iff the lower bound on N does *not* exceed chance.
- **RANGE valid** iff `P − N ≥ MINIMUM_RANGE`.

`INSTRUMENT_UNDECIDED` escalates the ladder rather than blaming the reader for a sample size —
V1 called BINDER an `INSTRUMENT_LIMIT` at 0.667 on 24 items when its interval had simply not
separated from chance yet.

Candidate against control is a **paired** question on the same items, so it uses a seeded
paired bootstrap rather than two independent intervals.

## 6. The shortcut audit (`MISSION §5`, `D-024`)

Seven rules that read only the options **as presented**: first, second, last, shortest,
longest, alphabetically first, alphabetically last. Plus a constant-answer check measured as
the share of items carrying the single most common answer. Both are judged against chance by
the same exact-binomial machinery, Bonferroni-corrected for the seven rules.

A cell that fails is `BENCHMARK_DEFECT`: not calibrated, not probed, not reported as a fact
about any representation.

A key-aware rule — "pick the globally most common answer" — is reported but **never used to
condemn**. It is fitted to the answer key of the cell it scores, so on forty items it
approaches reading the answers off the page. It measures publication risk, which is a real
risk and a different one.

## 7. What the audit and calibration together still cannot catch

`FM-047`. EXPRESSION_DEPTH asked "which reference sits deepest" and keyed the answer on a
single occurrence, when one identity occurred at depths 11, 9, 9 and 8. The question had no
single defensible answer. It passed calibration — positive 0.833, negative 0.000, range 0.833 —
and returned `INSTRUMENT_VALID` with `CONTROL_PARITY` at a normalised readability of 0.000,
which reads as "both representations are maximally unreadable".

The tell was that **all three real arms scored exactly 0/12** against a chance of 0.304, which
has probability 0.006 under guessing. The positive arm could not detect it because the header
hands over the answer; the shortcut audit could not detect it because no positional rule wins.

So a third check now applies at reading time: **when the control and candidate arms both
collapse to a single extreme value, suspect the answer key before concluding anything about a
representation.**

## 8. Withdrawn components

**MULTI_GOAL** (`FM-044`) — `RELATION_NOT_PROJECTED`. No axis of the representation space
renders which goal the action acts on. Verified twice against `projection.py`:
`_action_section` emits source, kind, elaborator, premises and local refs and never names a
goal; and the delta section names goals as `_uniq.*` ids the identity codec leaves unmapped,
while the goal section renders `m3`/`m7`. The two namespaces never meet on the page.

This withdraws V1's largest reported result. V1's MULTI_GOAL passed calibration and was
reported as 0.375 of readable headroom. The positive arm was high because it stated the answer
in the header; candidate and control sat near chance because **neither could answer a question
the projection does not carry**.

## 9. Cost

£0 incremental. All inference local via ollama (`qwen38-rvn:latest`, `gemma3:4b`). No paid API,
no paid GPU, no training, no global search. No LLM-generated mathematical answer is used as
ground truth anywhere: every answer is derived mechanically from `semantic_core`.
`SEALED_FINAL_V2` was not read.
