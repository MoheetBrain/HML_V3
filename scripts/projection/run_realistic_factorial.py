#!/usr/bin/env python
"""REAL_LEAN_GAP_V1 §5-§6: a factorial over the factors the real-item audit actually found.

`§5` pre-registers a factorial over ``dense_target x context_size x competing_expressions x
dependency_clutter``. Three of those four are kept only for continuity: the first sweep
already measured competing_expressions at -0.208 and dependency_clutter at -0.125 with
neutral filler at zero, and the mechanical audit of the 45 real items names four different
differences, two of which no experiment has ever varied. Substituting measured differences
for assumed ones is a deviation from the letter of the plan and is recorded as one.

Five two-level factors, full factorial, 32 cells:

    lead                1 / 2      real: 1 on 35 of 45 items; clean synthetic: always 2
    recurrence          1 / 4      real median 3.67 occurrences per identity; clean: 1
    target_copies       0 / 2      real median 2 verbatim reprints of the goal target
    deeper_in_context   0 / 3      real: 33 of 45 items have an option deeper in a context
                                   type than the answer is in the target
    context_size        0 / 16     the pre-registered load factor, kept as the control

Every cell carries its own positive and negative arm, so a low score is attributable to
readability rather than to a broken instrument. Main effects and two-way interactions are
estimated from the full design.

    .venv/bin/python scripts/projection/run_realistic_factorial.py
"""

from __future__ import annotations

from typing import Any

import argparse
import itertools
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts" / "projection"))

from hml_v3.micromath import calibration_v2 as C  # noqa: E402
from hml_v3.projection import dense as DN  # noqa: E402
from hml_v3.projection import expression as EX  # noqa: E402
from hml_v3.projection import realism as RE  # noqa: E402
from hml_v3.projection import serialize as SZ  # noqa: E402
from run_expression_experiment import ask  # noqa: E402

DEPTH = 10
DISTINCT = 5

#: (name, low, high). Low is always the clean-synthetic setting; high is the real-matched one.
FACTORS: tuple[tuple[str, int, int], ...] = (
    ("lead", 2, 1),
    ("recurrence", 1, 4),
    (RE.TARGET_COPIES, 0, 2),
    (RE.DEEPER_IN_CONTEXT, 0, 3),
    (RE.CONTEXT_SIZE, 0, 16),
)

REAL_LEAN_ACCURACY = 0.167


def cell_key(assignment: dict[str, int]) -> str:
    return "".join("1" if assignment[name] == high else "0"
                   for name, _low, high in FACTORS)


def measure(model: str, pool: list, levels: dict[str, int], arm: str) -> dict[str, Any]:
    correct: list[bool] = []
    chars: list[int] = []
    chose_deepest_anywhere = 0
    skipped = 0
    for expression in pool:
        options = EX.options_for(expression)
        if not RE.answer_still_unique(expression, options):
            skipped += 1
            continue
        if arm == "ABLATED_NEGATIVE":
            view = EX.build(EX.FLATTENED_BAG, expression, options)
        else:
            view = RE.build_view(expression, options, levels)
        rendered = SZ.render(view)
        chars.append(len(rendered))
        question, _ = EX.question(options)
        predicted, ok, _err = ask(
            model, rendered, question, options, expression.deepest,
            stated=expression.deepest if arm == "EXPLICIT_POSITIVE" else None)
        correct.append(ok)
        if predicted is not None and predicted == RE.deepest_anywhere(
                expression, options, levels) and predicted != expression.deepest:
            chose_deepest_anywhere += 1
    accuracy = sum(correct) / len(correct) if correct else 0.0
    lower, upper = C.clopper_pearson(sum(correct), len(correct)) if correct else (0.0, 0.0)
    return {"accuracy": round(accuracy, 4), "items": len(correct), "skipped": skipped,
            "lower": round(lower, 4), "upper": round(upper, 4),
            "chose_deepest_anywhere": chose_deepest_anywhere,
            "mean_characters": round(sum(chars) / len(chars)) if chars else 0,
            "per_item": correct}


def effects(cells: dict[str, dict]) -> dict[str, Any]:
    """Main effects and two-way interactions on NESTED_ONLY accuracy, from the 2^5 design."""

    names = [name for name, _low, _high in FACTORS]

    def accuracy(key: str) -> float:
        return cells[key]["arms"]["NESTED_ONLY"]["accuracy"]

    keys = list(cells)
    main: dict[str, float] = {}
    for index, name in enumerate(names):
        high = [accuracy(k) for k in keys if k[index] == "1"]
        low = [accuracy(k) for k in keys if k[index] == "0"]
        main[name] = round(sum(high) / len(high) - sum(low) / len(low), 4)

    interactions: dict[str, float] = {}
    for (i, left), (j, right) in itertools.combinations(list(enumerate(names)), 2):
        same = [accuracy(k) for k in keys if k[i] == k[j]]
        differ = [accuracy(k) for k in keys if k[i] != k[j]]
        interactions[f"{left} x {right}"] = round(
            (sum(same) / len(same) - sum(differ) / len(differ)) / 2.0, 4)
    return {"main_effects": main, "two_way_interactions": interactions}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="qwen38-rvn:latest")
    parser.add_argument("--items", type=int, default=24)
    parser.add_argument("--out", type=Path, default=ROOT / "reports/content_projection_v1")
    args = parser.parse_args()

    started = time.time()
    args.out.mkdir(parents=True, exist_ok=True)
    cells: dict[str, Any] = {}
    combinations = list(itertools.product(*[(low, high) for _n, low, high in FACTORS]))
    print(f"{len(combinations)} cells x 3 arms x {args.items} items = "
          f"{len(combinations) * 3 * args.items} probes\n", flush=True)

    for values in combinations:
        assignment = {name: value for (name, _l, _h), value in zip(FACTORS, values)}
        key = cell_key(assignment)
        pool = [DN.generate_dense_v2(i, DEPTH, DISTINCT, assignment["recurrence"],
                                     assignment["lead"])
                for i in range(args.items)]
        levels = {k: v for k, v in assignment.items() if k in RE.FACTORS}
        arms = {arm: measure(args.model, pool, levels, arm)
                for arm in ("NESTED_ONLY", "EXPLICIT_POSITIVE", "ABLATED_NEGATIVE")}
        chance = 1.0 / len(EX.options_for(pool[0]))
        verdict = C.classify_instrument(
            C.ArmResult("positive", sum(arms["EXPLICIT_POSITIVE"]["per_item"]),
                        arms["EXPLICIT_POSITIVE"]["items"]),
            C.ArmResult("negative", sum(arms["ABLATED_NEGATIVE"]["per_item"]),
                        arms["ABLATED_NEGATIVE"]["items"]), chance)
        cells[key] = {
            "levels": assignment, "chance": round(chance, 4),
            "arms": {k: {kk: vv for kk, vv in v.items() if kk != "per_item"}
                     for k, v in arms.items()},
            "per_item": {k: v["per_item"] for k, v in arms.items()},
            "instrument": verdict.to_dict(),
        }
        nested = arms["NESTED_ONLY"]
        print(f"  {key}  " + " ".join(
            f"{n}={assignment[n]}" for n, _l, _h in FACTORS) +
            f"  NESTED {nested['accuracy']:.3f} [{nested['lower']:.2f},{nested['upper']:.2f}]"
            f"  pos {arms['EXPLICIT_POSITIVE']['accuracy']:.3f}"
            f"  neg {arms['ABLATED_NEGATIVE']['accuracy']:.3f}"
            f"  scope-err {nested['chose_deepest_anywhere']:>2}"
            f"  {verdict.status:<18}({time.time() - started:.0f}s)", flush=True)

        payload = {
            "model": args.model, "items": args.items, "depth": DEPTH, "distinct": DISTINCT,
            "generator": DN.DENSE_VERSION, "realism": RE.REALISM_VERSION,
            "factors": [{"name": n, "low": l, "high": h} for n, l, h in FACTORS],
            "real_lean_accuracy": REAL_LEAN_ACCURACY,
            "elapsed_seconds": round(time.time() - started, 1),
            "cells": cells,
        }
        if len(cells) == len(combinations):
            payload["effects"] = effects(cells)
        (args.out / "REALISTIC_FACTORIAL.json").write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n")

    result = effects(cells)
    print("\n=== MAIN EFFECTS on NESTED_ONLY accuracy (high level minus low) ===")
    for name, value in sorted(result["main_effects"].items(), key=lambda kv: kv[1]):
        print(f"  {name:<22}{value:+.4f}")
    print("\n=== TWO-WAY INTERACTIONS ===")
    for name, value in sorted(result["two_way_interactions"].items(), key=lambda kv: kv[1]):
        print(f"  {name:<44}{value:+.4f}")

    worst = min(cells.items(), key=lambda kv: kv[1]["arms"]["NESTED_ONLY"]["accuracy"])
    best = max(cells.items(), key=lambda kv: kv[1]["arms"]["NESTED_ONLY"]["accuracy"])
    print(f"\nhighest cell {best[0]} at {best[1]['arms']['NESTED_ONLY']['accuracy']:.3f}")
    print(f"lowest  cell {worst[0]} at {worst[1]['arms']['NESTED_ONLY']['accuracy']:.3f}  "
          f"(real Lean {REAL_LEAN_ACCURACY:.3f})  levels {worst[1]['levels']}  "
          f"instrument {worst[1]['instrument']['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
