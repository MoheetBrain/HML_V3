#!/usr/bin/env python
"""REAL_LEAN_GAP_V1: is the collapse caused by the TARGET, not by what surrounds it?

Every factor in the first sweep added material around the target expression and the best of
them recovered 0.250 of a 0.708 collapse. Neutral filler at 1600 characters cost nothing at
all, which rules out raw token load.

What none of them varied is the target itself. Real failing Lean states carry 21 to 28
reference sites inside the goal target, with a single identity recurring at depths 11, 9, 9
and 8. The synthetic states carried six sites, each identity exactly once.

This holds the answer's depth fixed and varies how dense the target is.

    .venv/bin/python scripts/projection/run_dense_target.py
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
from hml_v3.projection import clutter as CL  # noqa: E402
from hml_v3.projection import expression as EX  # noqa: E402
from hml_v3.projection import serialize as SZ  # noqa: E402
from hml_v3.projection import synthetic as SY  # noqa: E402
from hml_v3.projection.model_view import SelectiveModelView, ViewBlock  # noqa: E402
from run_expression_experiment import ask  # noqa: E402

SITES = (2, 4, 8, 16, 24, 32, 48)
DEPTHS = (6, 10)


def view_for(expression, options):
    view = SelectiveModelView(label="NESTED_ONLY", source_id=expression.state_id)
    names = sorted(expression.depth_of)
    view.add(ViewBlock("context", [("declaration", n) for n in names]))
    target = expression.transition["state_before"]["goals"][0]["target"]
    view.add(ViewBlock("goal_target", [("expression", CL._render_expression(target))]))
    return view


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="qwen38-rvn:latest")
    parser.add_argument("--items", type=int, default=20)
    parser.add_argument("--out", type=Path, default=ROOT / "reports/content_projection_v1")
    args = parser.parse_args()

    started = time.time()
    results: dict[str, Any] = {}
    args.out.mkdir(parents=True, exist_ok=True)
    baseline_items: list[bool] = []

    for depth in DEPTHS:
        for sites in SITES:
            pool = [SY.generate_dense(i, depth, sites) for i in range(args.items)]
            pool = [e for e in pool if not SY.verify(e)]
            correct: list[bool] = []
            chars: list[int] = []
            recurrence: list[float] = []
            for expression in pool:
                options = EX.options_for(expression)
                if expression.deepest not in options or len(options) < 2:
                    continue
                view = view_for(expression, options)
                rendered = SZ.render(view)
                chars.append(len(rendered))
                occurrences = len(expression.node_reference)
                distinct = len(set(expression.node_reference.values()))
                recurrence.append(occurrences / max(1, distinct))
                question, _ = EX.question(options)
                _p, ok, _e = ask(args.model, rendered, question, options,
                                 expression.deepest)
                correct.append(ok)
            if not correct:
                continue
            accuracy = sum(correct) / len(correct)
            key = f"depth{depth}_sites{sites}"
            results[key] = {
                "depth": depth, "sites": sites, "accuracy": round(accuracy, 4),
                "items": len(correct),
                "mean_characters": round(sum(chars) / len(chars)),
                "mean_recurrence": round(sum(recurrence) / len(recurrence), 2),
                "per_item": correct}
            if sites == SITES[0] and depth == DEPTHS[0]:
                baseline_items = correct
            print(f"  depth {depth:>2} sites {sites:>3} -> {accuracy:.3f}  "
                  f"({round(sum(chars) / len(chars)):>5} chars, "
                  f"recurrence {results[key]['mean_recurrence']:.2f}x)  "
                  f"({time.time() - started:.0f}s)", flush=True)

    for key, record in results.items():
        if baseline_items and len(record["per_item"]) == len(baseline_items):
            status, reason, decided = C.compare(record["per_item"], baseline_items)
            record["vs_sparsest"] = {"status": status, "reason": reason,
                                     "decisive": decided}

    (args.out / "DENSE_TARGET.json").write_text(json.dumps({
        "model": args.model, "items": args.items, "sites": list(SITES),
        "depths": list(DEPTHS),
        "elapsed_seconds": round(time.time() - started, 1),
        "cells": {k: {kk: vv for kk, vv in v.items() if kk != "per_item"}
                  for k, v in results.items()}}, indent=2, sort_keys=True) + "\n")

    print("\n=== DENSE TARGET ===")
    for depth in DEPTHS:
        row = [results.get(f"depth{depth}_sites{s}") for s in SITES]
        print(f"  depth {depth:>2}: " + "  ".join(
            f"{s}={r['accuracy']:.2f}" if r else f"{s}=--" for s, r in zip(SITES, row)))
    best = min((r["accuracy"], k) for k, r in results.items())
    print(f"\nlowest cell: {best[1]} at {best[0]:.3f}  (real Lean = 0.167)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
