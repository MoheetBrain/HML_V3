#!/usr/bin/env python
"""REAL_LEAN_GAP_V1 §2 and §4: is it token load, or is it semantic interference?

`context_size` and `competing_expressions` were the only two factors to move the needle, and
both increase prompt length. That confounds two very different explanations:

    token load          the reader degrades because the prompt is long, whatever is in it
    interference        the reader degrades because competing MATHEMATICAL structure
                        creates candidate relations it must rule out

They imply opposite remedies. If it is load, the fix is selective context -- show less. If it
is interference, showing less only helps insofar as it removes *competing structure*, and
neutral text would be harmless.

Five fillers at matched character budgets:

    A NEUTRAL_FILLER      prose-like tokens with no mathematical structure
    B IRRELEVANT_DECLS    declarations that exist but are never referenced
    C COMPETING_EXPRS     other expression trees over the same identifiers
    D NONTARGET_MATH      mathematical structure about other relations entirely
    E RELEVANT_LOCAL      structure about the target's own neighbourhood

Same target relation, same question, same serializer throughout.

    .venv/bin/python scripts/projection/run_iso_token.py
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
from hml_v3.projection.model_view import SelectiveModelView, ViewBlock, cost_of  # noqa: E402
from run_expression_experiment import ask  # noqa: E402

NEUTRAL_FILLER = "A_NEUTRAL_FILLER"
IRRELEVANT_DECLS = "B_IRRELEVANT_DECLS"
COMPETING_EXPRS = "C_COMPETING_EXPRS"
NONTARGET_MATH = "D_NONTARGET_MATH"
RELEVANT_LOCAL = "E_RELEVANT_LOCAL"

FILLERS = (NEUTRAL_FILLER, IRRELEVANT_DECLS, COMPETING_EXPRS, NONTARGET_MATH, RELEVANT_LOCAL)

#: Character budgets. The top of the range is chosen to reach the length of the real Lean
#: renderings that score 0.167, so load is tested where the collapse actually happens.
BUDGETS = (0, 400, 800, 1600, 3200, 6400)

WORDS = ("the", "note", "observe", "consider", "hence", "further", "recall", "moreover",
         "state", "record", "remark", "given", "above", "below", "prior", "later")


def _neutral(budget: int, seed: int) -> list[tuple[str, Any]]:
    rows: list[tuple[str, Any]] = []
    size = 0
    index = 0
    while size < budget:
        text = " ".join(WORDS[(seed + index + w) % len(WORDS)] for w in range(9))
        rows.append(("note", text))
        size += len(text) + 8
        index += 1
    return rows


def _declarations(budget: int, seed: int) -> list[tuple[str, Any]]:
    rows: list[tuple[str, Any]] = []
    size = 0
    index = 0
    while size < budget:
        name = f"w{10 + index}"
        rows.append(("declaration", f"{name} : t{(seed + index) % 9}"))
        size += 22
        index += 1
    return rows


def _competing(budget: int, seed: int, names: list[str]) -> list[tuple[str, Any]]:
    rows: list[tuple[str, Any]] = []
    size = 0
    index = 0
    while size < budget:
        node = CL._decoy_expression(seed + index, 4 + (index % 5), names)
        text = CL._render_expression(node)
        rows.append((f"expr{index}", text))
        size += len(text) + 8
        index += 1
    return rows


def _nontarget_math(budget: int, seed: int, names: list[str]) -> list[tuple[str, Any]]:
    """Mathematics about other relations: dependencies, scopes, premises. Not expressions."""

    rows: list[tuple[str, Any]] = []
    size = 0
    index = 0
    while size < budget:
        left = names[index % len(names)]
        right = f"w{10 + (index * 3) % 40}"
        kind = ("depends", "scope", "cites")[index % 3]
        text = {"depends": f"{right} <- {left}",
                "scope": f"binder b{index} over {right}",
                "cites": f"premise p{(seed + index) % 50} used by a{index}"}[kind]
        rows.append((kind, text))
        size += len(text) + 10
        index += 1
    return rows


def _relevant_local(budget: int, seed: int, expression) -> list[tuple[str, Any]]:
    """Structure about the target's own neighbourhood: real, relevant, and redundant."""

    rows: list[tuple[str, Any]] = []
    size = 0
    index = 0
    parents = {child: parent for child, parent in expression.edges}
    pairs = sorted(parents.items())
    while size < budget and pairs:
        child, parent = pairs[index % len(pairs)]
        text = f"{child} is a child of {parent}"
        rows.append(("edge", text))
        size += len(text) + 8
        index += 1
    return rows


def build(filler: str, budget: int, expression, options: list[str]) -> SelectiveModelView:
    seed = sum(ord(c) for c in expression.state_id)
    names = sorted(expression.depth_of)
    view = SelectiveModelView(label=f"{filler}@{budget}", source_id=expression.state_id)
    view.add(ViewBlock("context", [("declaration", n) for n in names]))
    if budget:
        rows = {
            NEUTRAL_FILLER: lambda: _neutral(budget, seed),
            IRRELEVANT_DECLS: lambda: _declarations(budget, seed),
            COMPETING_EXPRS: lambda: _competing(budget, seed, names),
            NONTARGET_MATH: lambda: _nontarget_math(budget, seed, names),
            RELEVANT_LOCAL: lambda: _relevant_local(budget, seed, expression),
        }[filler]()
        view.add(ViewBlock("surrounding_material", rows))
    target = expression.transition["state_before"]["goals"][0]["target"]
    view.add(ViewBlock("goal_target", [("expression", CL._render_expression(target))]))
    return view


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="qwen38-rvn:latest")
    parser.add_argument("--items", type=int, default=24)
    parser.add_argument("--out", type=Path, default=ROOT / "reports/content_projection_v1")
    args = parser.parse_args()

    pool = [SY.generate(i, "MIX", 3 + (i % 8)) for i in range(args.items)]
    if any(SY.verify(e) for e in pool):
        print("invalid states; refusing to run")
        return 1

    started = time.time()
    results: dict[str, dict[str, Any]] = {}
    args.out.mkdir(parents=True, exist_ok=True)
    print(f"pool {len(pool)} states; budgets {BUDGETS}\n", flush=True)

    for filler in FILLERS:
        curve: dict[str, Any] = {}
        for budget in BUDGETS:
            correct: list[bool] = []
            chars: list[int] = []
            for expression in pool:
                options = EX.options_for(expression)
                view = build(filler, budget, expression, options)
                rendered = SZ.render(view)
                chars.append(cost_of(view, rendered).characters)
                question, _ = EX.question(options)
                _p, ok, _e = ask(args.model, rendered, question, options, expression.deepest)
                correct.append(ok)
            accuracy = sum(correct) / len(correct)
            curve[str(budget)] = {
                "accuracy": round(accuracy, 4), "items": len(correct),
                "mean_characters": round(sum(chars) / len(chars)),
                "per_item": correct}
            print(f"  {filler:<20}{budget:>5} -> {accuracy:.3f}  "
                  f"({round(sum(chars) / len(chars)):>5} chars)  "
                  f"({time.time() - started:.0f}s)", flush=True)
        base = curve["0"]
        top = curve[str(BUDGETS[-1])]
        status, reason, decided = C.compare(top["per_item"], base["per_item"])
        results[filler] = {
            "curve": {k: {kk: vv for kk, vv in v.items() if kk != "per_item"}
                      for k, v in curve.items()},
            "drop": round(base["accuracy"] - top["accuracy"], 4),
            "top_vs_zero": {"status": status, "reason": reason, "decisive": decided},
        }
        print(f"  {filler:<20}drop {results[filler]['drop']:+.3f}  {status}\n", flush=True)
        (args.out / "ISO_TOKEN.json").write_text(json.dumps({
            "model": args.model, "items": args.items, "budgets": list(BUDGETS),
            "elapsed_seconds": round(time.time() - started, 1),
            "fillers": results}, indent=2, sort_keys=True) + "\n")

    print("=== ISO-TOKEN RESULT ===")
    for filler in FILLERS:
        print(f"  {filler:<20}drop {results[filler]['drop']:+.3f}  "
              f"{results[filler]['top_vs_zero']['status']}")
    neutral = results[NEUTRAL_FILLER]["drop"]
    structured = max(results[f]["drop"] for f in (COMPETING_EXPRS, NONTARGET_MATH))
    print(f"\nneutral filler drop {neutral:+.3f} vs structured drop {structured:+.3f}")
    if structured - neutral > 0.15:
        print("-> INTERFERENCE dominates: competing structure hurts more than length alone")
    elif neutral > 0.15:
        print("-> TOKEN LOAD dominates: even neutral text of the same length hurts")
    else:
        print("-> neither reproduces the collapse at these budgets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
