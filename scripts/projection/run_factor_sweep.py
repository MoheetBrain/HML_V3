#!/usr/bin/env python
"""REAL_LEAN_GAP_V1 §1-§3: which factor collapses readability from 0.93 to 0.17?

The same question, reader and nested rendering score 0.933 on clean synthetic states and
0.167 on real Lean states. Expression depth is not the explanation -- accuracy is flat from
depth 1 to 17. This sweeps nine candidate factors one at a time, each on its own ladder from
clean, and locates where the curve breaks.

Nothing here assumes clutter is the cause. Several factors may do nothing, and a sweep in
which none of them reproduces the collapse is a real answer that sends the search back to
what else differs between synthetic and real states.

    .venv/bin/python scripts/projection/run_factor_sweep.py
"""

from __future__ import annotations

from typing import Any

import argparse
import collections
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
from hml_v3.projection.model_view import SelectiveModelView, ViewBlock, cost_of  # noqa: E402
from run_expression_experiment import ask  # noqa: E402

#: Real Lean EXPRESSION_DEPTH, measured on micro_dev_v2 with the same reader and question.
REAL_LEAN_ACCURACY = 0.167
CLEAN_BASELINE = 0.933


def build_view(expression, clutter: CL.Clutter, options: list[str], view: str = EX.NESTED_ONLY):
    """A ModelView of a cluttered state. Serialization stays the frozen one."""

    target, extra, notes = CL.apply_clutter(expression, clutter)
    if not CL.answer_still_unique(expression, clutter, target, notes):
        return None, None, notes
    rename = notes.get("rename") or {}
    mapped = [rename.get(o, o) for o in options]
    answer = rename.get(expression.deepest, expression.deepest)

    out = SelectiveModelView(label=view, source_id=expression.state_id)
    for block in extra:
        out.add(block)
    if view == EX.NESTED_ONLY:
        out.add(ViewBlock("goal_target", [("expression", CL._render_expression(target))]))
    else:
        # The other views are built from the clean structure and then given the same
        # surrounding clutter, so the comparison isolates the view rather than the state.
        clean = EX.build(view, expression, options)
        for block in clean.blocks:
            if block.kind != "context":
                out.add(block)
        out.exposure = clean.exposure
    return out, (mapped, answer), notes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="qwen38-rvn:latest")
    parser.add_argument("--items", type=int, default=24)
    parser.add_argument("--out", type=Path, default=ROOT / "reports/content_projection_v1")
    args = parser.parse_args()

    # A fixed pool spanning depths, so a factor effect is not confounded with depth.
    pool = [SY.generate(i, "MIX", 3 + (i % 8)) for i in range(args.items)]
    if any(SY.verify(e) for e in pool):
        print("generator produced invalid states; refusing to run")
        return 1
    print(f"pool: {len(pool)} verified states, depths "
          f"{sorted({e.depth for e in pool})}", flush=True)

    started = time.time()
    results: dict[str, dict[str, Any]] = {}
    args.out.mkdir(parents=True, exist_ok=True)

    def measure(clutter: CL.Clutter) -> dict:
        correct: list[bool] = []
        chars: list[int] = []
        skipped = 0
        for expression in pool:
            options = EX.options_for(expression)
            view, mapping, _notes = build_view(expression, clutter, options)
            if view is None:
                skipped += 1
                continue
            mapped, answer = mapping
            rendered = SZ.render(view)
            chars.append(cost_of(view, rendered).characters)
            question, _ = EX.question(mapped)
            _pred, ok, _err = ask(args.model, rendered, question, mapped, answer)
            correct.append(ok)
        return {"accuracy": round(sum(correct) / len(correct), 4) if correct else None,
                "items": len(correct), "skipped": skipped,
                "mean_characters": round(sum(chars) / len(chars)) if chars else 0,
                "per_item": correct}

    baseline = measure(CL.Clutter({}))
    print(f"\nclean baseline: {baseline['accuracy']:.3f} "
          f"({baseline['mean_characters']} chars)  [real Lean = {REAL_LEAN_ACCURACY}]\n",
          flush=True)
    results["clean"] = baseline

    for factor in CL.FACTORS:
        curve: dict[str, Any] = {}
        for level in CL.LADDERS[factor]:
            if level == 0:
                curve[str(level)] = {k: v for k, v in baseline.items() if k != "per_item"}
                curve[str(level)]["per_item"] = baseline["per_item"]
                continue
            record = measure(CL.Clutter({factor: level}))
            curve[str(level)] = record
            drop = baseline["accuracy"] - (record["accuracy"] or 0)
            print(f"  {factor:<26}{level:>3} -> {record['accuracy']:.3f}  "
                  f"({record['mean_characters']:>5} chars, drop {drop:+.3f})  "
                  f"({time.time() - started:.0f}s)", flush=True)
        top = CL.LADDERS[factor][-1]
        best = curve[str(top)]
        status, reason, decided = C.compare(best["per_item"], baseline["per_item"])
        results[factor] = {
            "ladder": list(CL.LADDERS[factor]),
            "curve": {k: {kk: vv for kk, vv in v.items() if kk != "per_item"}
                      for k, v in curve.items()},
            "max_drop": round(baseline["accuracy"] - min(
                v["accuracy"] for v in curve.values() if v["accuracy"] is not None), 4),
            "top_level_vs_clean": {"status": status, "reason": reason, "decisive": decided},
        }
        print(f"  {factor:<26}max drop {results[factor]['max_drop']:+.3f}  "
              f"top vs clean: {status}\n", flush=True)

        (args.out / "FACTOR_SWEEP.json").write_text(json.dumps({
            "model": args.model, "items": args.items,
            "clean_baseline": baseline["accuracy"],
            "real_lean_accuracy": REAL_LEAN_ACCURACY,
            "clutter_version": CL.CLUTTER_VERSION,
            "elapsed_seconds": round(time.time() - started, 1),
            "factors": {k: v for k, v in results.items() if k != "clean"},
        }, indent=2, sort_keys=True) + "\n")

    ranked = sorted(((v["max_drop"], k) for k, v in results.items() if k != "clean"),
                    reverse=True)
    print("=== FACTOR RANKING (max drop from clean) ===")
    for drop, factor in ranked:
        print(f"  {factor:<26}{drop:+.3f}")
    print(f"\nclean {baseline['accuracy']:.3f} -> real Lean {REAL_LEAN_ACCURACY:.3f} "
          f"is a drop of {baseline['accuracy'] - REAL_LEAN_ACCURACY:+.3f}")
    reproduced = [f for d, f in ranked if d >= 0.5]
    print(f"factors reproducing at least half the collapse: {reproduced or 'NONE'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
