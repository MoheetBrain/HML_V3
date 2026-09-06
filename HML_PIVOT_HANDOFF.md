# HML_PIVOT_HANDOFF

**Date:** 2026-09-06
**Decision:** `STATIC_REPRESENTATION_THESIS_V1: NOT SUPPORTED`
**Consequence:** static machine-facing language optimisation stops here. The canonical-state,
verifier and benchmark infrastructure survives and transfers.

This document exists so a reader with no conversation history can see exactly what was
tested, what the strongest negative evidence is, and what is worth carrying into Hamiltonian
Chess. It does not argue for the pivot; it records the measurements that forced it.

---

## 1. The thesis that was tested

> Holding mathematical truth, task, reader and scoring fixed, some machine-facing
> representation of mathematical state reliably improves verified reasoning over strong
> conventional controls.

This was tested three independent ways over the life of the project. All three came back
negative or unresolved.

## 2. The strongest negative evidence

### 2.1 The search space could not vary the thing being measured (`D-025`)

An open-ended search ran **106 generations** over a 42-axis representation genome. An
exhaustive single-axis sweep then showed that **no axis of the 42 can remove any relation
from the page** except `type_explicitness`. Seven of seven valid instruments reported
`CONTROL_PARITY`; four were exact ties on every item. Thirteen mutation hypotheses across two
families moved a combined **0.031**.

The space was rich in typography and empty of content selection. A search over it could not
have found a more readable notation, because readability barely varies across it.

### 2.2 The one positive result was a statistics defect (`FM-057`)

`PATH_TO_ROOT` — materialising each candidate's ancestor chain so depth becomes row counting —
was the **only** representation that ever beat a control on a valid instrument: 0.500 against
`NESTED_ONLY`'s 0.292 in `HARD_REGIME_V1`, reported as `ADVANTAGE`.

That verdict was produced by a broken resampler. `paired_bootstrap` advanced an LCG modulo
2³¹ and used `state % n` as the index; the low *k* bits of such a generator have period 2ᵏ, so
at sample sizes that are powers of two every resample drew the identical multiset and the
interval had **zero width**. Recomputed with a correct resampler, that same measurement is:

| | delta | 90% interval | verdict |
|---|---|---|---|
| reported at the time | +0.208 | (degenerate) | `ADVANTAGE` |
| **corrected** | +0.208 | **[+0.000, +0.417]** | **`COMPARISON_UNSEPARATED`** |

It was never a decisive result. Exactly one verdict in the whole corpus changed when the
resampler was fixed, and it was this one. No accuracy figure changed — point estimates were
never affected.

### 2.3 It does not replicate across readers

Pre-registered before any number was read: continue only if the advantage is positive on
**both** readers, the pooled interval excludes zero, and the pooled effect is ≥ +0.10.

Fresh items (indices 1000–1127, **zero overlap** with the original 24), the `PATH_TO_ROOT`
implementation frozen at sha256 `6707891a010fbb0b6d02b791b7a99fe70ac553c9429245b27a4477860bfab227`,
128 paired items per reader, both instruments independently calibrated and both valid:

| reader | model | family | NESTED_ONLY | PATH_TO_ROOT | delta | 90% CI |
|---|---|---|---|---|---|---|
| A | `qwen38-rvn` | qwen35 | 0.305 | 0.875 | **+0.5703** | [+0.4922, +0.6484] |
| B | `gemma4:31b` | gemma4 | 0.383 | 0.328 | **−0.0547** | [−0.1484, +0.0391] |
| pooled | — | — | 0.344 | 0.602 | +0.2578 | [+0.1875, +0.3242] |

The effect is enormous on one reader and absent on the other. The pooled figure is positive
only because reader A dominates it; pooling two readers that disagree in sign measures the
mixture, not the representation. **`KILL_PATH`.**

The most plausible mechanism is cost, and it is worth stating because it generalises:
`PATH_TO_ROOT` renders at 1,100 characters against `NESTED_ONLY`'s 297 — a 3.7× multiple.
A representation that pays 3.7× the tokens to help one model family and not another is a
property of that model family, not of mathematics.

### 2.4 Matched adaptation showed no candidate advantage either

One A100, five surfaces, identical base checkpoint per arm, matched examples/optimizer/LoRA/
seed/context, successive halving with a rule fixed in advance:

| Stage A (224 examples) | exact | train tokens |
|---|---|---|
| L3_JSON_AST | 0.979 | 101,920 |
| L5_COMPACT_SYMBOLIC | 0.958 | 94,080 |
| L0_STRUCTURED_ENGLISH | 0.938 | 101,850 |
| L1_CURRENT_HML | 0.896 | 103,642 |
| L2_SEXPR | 0.833 | 130,507 |

Only `L2_SEXPR`'s deficit excluded zero — a **penalty**, not an advantage, and it occurred
while that arm consumed 1.39× the cheapest arm's tokens, so it was not token-starved. By 576
examples both finalists reached **1.000** on dev and on a fresh slice with a paired delta of
exactly zero. No candidate beat the strongest control at any stage. The task saturates, so the
larger-budget stages cannot rank anything.

### 2.5 What *was* established, and it is real

The project did produce one solid, replicated-by-construction scientific result — about why
ordinary notation fails, not about how to fix it. `REAL_LEAN_GAP_V1`: the real Lean
expression-depth collapse (0.933 → 0.167) is caused by **repeated occurrences of the same
identity at several depths with a one-level winning margin**, internal to the target
expression. A 32-cell factorial gives recurrence a main effect of **−0.2891**, lead −0.0911,
and the external factors null or mildly positive, with every interaction ≤ 0.0247. The
internal-only cell reaches normalised readability of **exactly 0.000** — the nested rendering
carries nothing over one with parentage destroyed — against the real task's 0.091.

Both recurrence and depth are **non-monotonic**: difficulty peaks at recurrence 4 and depth 10
and eases at 12 and 14. "Denser is harder" is false as stated.

This is a diagnostic result. It explains a failure. It does not identify a representation that
avoids it, and the one candidate that looked like it might does not survive a second reader.

## 3. Why this stops, rather than iterating again

Every remaining move is a known dead end or an escape hatch:

- **More axes / more syntax** — `D-025` shows the axis vocabulary cannot vary content.
- **More search generations** — 106 converged on a space where the target quantity is
  near-constant.
- **A new representation family** — this is the escape hatch the gate explicitly forbids, and
  the honest read of §2.3 is that the last candidate failed a basic cross-reader check.
- **Bigger models** — the effect direction *reversed* between two local families; scale is not
  the free variable.

The count that settled it: across this project, **defects found in my own instruments and
generators outnumber findings about the language**, and the single positive language result
turned out to be one of those defects. `FM-043` through `FM-058`.

## 4. What transfers to Hamiltonian Chess

All of this is representation-agnostic and none of it depends on HML being superior.

**Transfers directly:**

| Component | Where | Why it transfers |
|---|---|---|
| `CanonicalMathState` / Arena canonical schema | `HML_V3/src/hml_v3/`, `hamiltonian_chess/arena/canonical/` | Immutable typed state with stable hashes; a game needs exactly this |
| Verifier / assurance suite | `arena/assurance/`, `arena/verifier/` | Physics rather than a player; SymPy/Z3/exhaustive/fuzz already wired |
| Typed actions + trajectory machinery | `arena/tasks/`, `arena/canonical/` | Legal-move generation and state transition are the same shape |
| World generator | `arena/tasks/generators/world_v0.py` | 676 deterministic worlds across 13 domains, balanced and seeded |
| Refuter and Curriculum | `arena/players/`, `arena/tasks/curriculum.py` | Adversarial probing and disagreement-based task selection |
| League / Pareto / Hall of Fame | `arena/league/` | Multi-axis rating for agent populations |
| Instrument calibration | `hml_v3/micromath/calibration_v2.py` | Positive/negative arms, exact binomial intervals, the corrected paired bootstrap, the sequential ladder |
| Matched-adaptation runner | `arena/training/gpu_matched_runner.py` | Identical-checkpoint-per-arm discipline, pre-declared halving, provenance capture |
| Failure memory | `research/representation_search/hml_failure_memory.json` | 58 recorded failures; anti-Goodhart constraints that cost real time to learn |
| Synthetic generators | `hml_v3/projection/dense.py`, `synthetic.py` | Truth verified by walking the artefact, not by trusting construction |

**Does not transfer:** the 42-axis genome, the eight surface seeds, the representation search
controller, and every result that ranks one notation against another. They are answers to a
question that is now closed.

**The transferable methodological lessons**, which are worth more than the code:

1. Calibrate every instrument with a positive and a relation-destroyed negative arm before
   believing any comparison.
2. Re-derive a generator's claimed truth by walking what it built (`FM-054`).
3. Test a hand-rolled RNG for degeneracy at the sample sizes actually used; a zero-width
   interval is a defect signature (`FM-057`).
4. A reader scoring 0.000 on an arm that states the answer is a harness bug until proven
   otherwise (`FM-056`).
5. Fix the decision rule before reading the numbers, and pool readers only when they agree in
   sign.

## 5. Instruction for the chess project

Do **not** make Hamiltonian Chess's success depend on HML being a better representation. It is
not established that it is. Use the canonical state, the verifier and the tournament
machinery because they are good engineering, and pick the game's representation on ordinary
engineering grounds.

The Arena evidence branch (`codex/arena-v0-fitness`) must be preserved, not overwritten. Game
work belongs on a new repository or a clean branch.
