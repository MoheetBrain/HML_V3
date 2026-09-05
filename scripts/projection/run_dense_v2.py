#!/usr/bin/env python
"""REAL_LEAN_GAP_V1 §2: does INTERNAL target density reproduce the collapse?

The first dense sweep is withdrawn (`FM-054`): its generator recorded an intended depth for
each distractor and never re-derived it, so on 14 to 20 of every 20 items the recorded answer
was not the unique deepest reference. This runs the same question on a generator whose truth
is verified by walking the finished tree.

Four internal factors, varied independently, with depth and the answer's uniqueness held:

    recurrence   occurrences of EVERY identity, the answer included (1, 2, 4, 8, 12)
    distinct     how many distractor identities exist (3, 5)
    lead         how far the answer's deepest occurrence beats the runner-up (1, 2)
    depth        the answer's depth (6, 10, 14)

``sites`` -- the reference-site count the mission asks about -- is ``(distinct+1) *
recurrence``, so the grid spans 4 to 72 sites against a real median of 18.

**Every cell carries its own instrument.** A cell scoring 0.2 means nothing until the same
cell's positive arm (told the answer) is high and its negative arm (parentage genuinely
absent) is not. Reporting a low number without them is how `FM-051` happened.

    .venv/bin/python scripts/projection/run_dense_v2.py
"""

from __future__ import annotations

from typing import Any

import argparse
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
from hml_v3.projection import serialize as SZ  # noqa: E402
from run_expression_experiment import ask  # noqa: E402

#: (depth, distinct, recurrence, lead). The main grid is a full factorial over recurrence,
#: distinct and lead at the real corpus's median depth; the last rows probe depth and the
#: recurrence extreme separately so the factorial stays balanced.
def build_grid() -> list[tuple[int, int, int, int]]:
    cells: list[tuple[int, int, int, int]] = []
    for distinct in (3, 5):
        for recurrence in (1, 2, 4, 8):
            for lead in (1, 2):
                cells.append((10, distinct, recurrence, lead))
    cells.append((10, 5, 12, 1))          # 72 sites: past the real median, near its tail
    cells.append((6, 5, 4, 1))            # depth check, low
    cells.append((14, 5, 4, 1))           # depth check, high
    return cells


REAL_LEAN_ACCURACY = 0.167
CLEAN_BASELINE = 0.933


def measure(model: str, pool: list, arm: str, items: int) -> dict[str, Any]:
    correct: list[bool] = []
    chars: list[int] = []
    for expression in pool:
        options = EX.options_for(expression)
        if expression.deepest not in options or len(options) < 2:
            continue
        view = EX.build(EX.FLATTENED_BAG if arm == "ABLATED_NEGATIVE" else EX.NESTED_ONLY,
                        expression, options)
        rendered = SZ.render(view)
        chars.append(len(rendered))
        question, _ = EX.question(options)
        _pred, ok, _err = ask(model, rendered, question, options, expression.deepest,
                              stated=expression.deepest if arm == "EXPLICIT_POSITIVE" else None)
        correct.append(ok)
    accuracy = sum(correct) / len(correct) if correct else 0.0
    lower, upper = C.clopper_pearson(sum(correct), len(correct)) if correct else (0.0, 0.0)
    return {"accuracy": round(accuracy, 4), "items": len(correct),
            "lower": round(lower, 4), "upper": round(upper, 4),
            "mean_characters": round(sum(chars) / len(chars)) if chars else 0,
            "per_item": correct}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="qwen38-rvn:latest")
    parser.add_argument("--items", type=int, default=24)
    parser.add_argument("--out", type=Path, default=ROOT / "reports/content_projection_v1")
    args = parser.parse_args()

    started = time.time()
    args.out.mkdir(parents=True, exist_ok=True)
    results: dict[str, Any] = {}
    grid = build_grid()
    print(f"{len(grid)} cells x 3 arms x {args.items} items = "
          f"{len(grid) * 3 * args.items} probes\n", flush=True)

    for depth, distinct, recurrence, lead in grid:
        pool = [DN.generate_dense_v2(i, depth, distinct, recurrence, lead)
                for i in range(args.items)]
        # The generator raises on any disagreement between plan and walk, so reaching here
        # means every item's answer is the verified unique deepest reference.
        key = f"d{depth}_n{distinct}_r{recurrence}_l{lead}"
        arms = {arm: measure(args.model, pool, arm, args.items)
                for arm in ("NESTED_ONLY", "EXPLICIT_POSITIVE", "ABLATED_NEGATIVE")}
        chance = 1.0 / len(EX.options_for(pool[0]))
        verdict = C.classify_instrument(
            C.ArmResult("positive", sum(arms["EXPLICIT_POSITIVE"]["per_item"]),
                        arms["EXPLICIT_POSITIVE"]["items"]),
            C.ArmResult("negative", sum(arms["ABLATED_NEGATIVE"]["per_item"]),
                        arms["ABLATED_NEGATIVE"]["items"]), chance)
        results[key] = {
            "depth": depth, "distinct": distinct, "recurrence": recurrence, "lead": lead,
            "sites": DN.sites(distinct, recurrence), "chance": round(chance, 4),
            "arms": {k: {kk: vv for kk, vv in v.items() if kk != "per_item"}
                     for k, v in arms.items()},
            "per_item": {k: v["per_item"] for k, v in arms.items()},
            "instrument": verdict.to_dict(),
        }
        nested = arms["NESTED_ONLY"]
        print(f"  {key:<22}sites {DN.sites(distinct, recurrence):>3}  "
              f"NESTED {nested['accuracy']:.3f} [{nested['lower']:.2f},{nested['upper']:.2f}]  "
              f"pos {arms['EXPLICIT_POSITIVE']['accuracy']:.3f}  "
              f"neg {arms['ABLATED_NEGATIVE']['accuracy']:.3f}  "
              f"{verdict.status:<18}({time.time() - started:.0f}s)", flush=True)

        (args.out / "DENSE_TARGET_V2.json").write_text(json.dumps({
            "model": args.model, "items": args.items,
            "generator": DN.DENSE_VERSION,
            "real_lean_accuracy": REAL_LEAN_ACCURACY, "clean_baseline": CLEAN_BASELINE,
            "withdrawn": "DENSE_TARGET.json (FM-054: mis-keyed answers)",
            "elapsed_seconds": round(time.time() - started, 1),
            "cells": results}, indent=2, sort_keys=True) + "\n")

    print("\n=== DENSE TARGET V2 (NESTED_ONLY accuracy) ===")
    print(f"  {'cell':<22}{'sites':>6}{'nested':>9}{'pos':>7}{'neg':>7}  instrument")
    for key, record in results.items():
        a = record["arms"]
        print(f"  {key:<22}{record['sites']:>6}{a['NESTED_ONLY']['accuracy']:>9.3f}"
              f"{a['EXPLICIT_POSITIVE']['accuracy']:>7.3f}"
              f"{a['ABLATED_NEGATIVE']['accuracy']:>7.3f}  {record['instrument']['status']}")

    valid = {k: v for k, v in results.items()
             if v["instrument"]["status"] == C.INSTRUMENT_VALID}
    print(f"\ncells with a valid instrument: {len(valid)}/{len(results)}")
    if valid:
        worst = min(valid.items(), key=lambda kv: kv[1]["arms"]["NESTED_ONLY"]["accuracy"])
        print(f"lowest valid cell: {worst[0]} at "
              f"{worst[1]['arms']['NESTED_ONLY']['accuracy']:.3f} "
              f"(real Lean {REAL_LEAN_ACCURACY:.3f}, clean synthetic {CLEAN_BASELINE:.3f})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
