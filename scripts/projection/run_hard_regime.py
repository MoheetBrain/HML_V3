#!/usr/bin/env python
"""REAL_LEAN_GAP_V1 §3-§4: compare every view inside the hard regime, then find the floor.

Two experiments over one pair of regimes.

`§3` -- the view comparison. Seven views of the same states, EASY and HARD, so the number
that matters is not any view's accuracy but its DROP. A view that scores well only where
nothing is failing has not been shown to help; the mission's whole point is the view with
the smallest collapse.

`§4` -- selective context. The tree-hop ladder in `selective.py` is degenerate here (the
union of the candidates' ancestor chains is the whole target, because depth is a global
property), so the ladder that can be measured is over the material AROUND the target:
target only, plus declarations, plus referencing types, plus verbatim state copies, full
state. Accuracy is reported beside exposed characters, so the minimum sufficient context is
read off the point where accuracy stops improving.

Every regime carries its own positive and negative arm.

    .venv/bin/python scripts/projection/run_hard_regime.py
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
from hml_v3.projection import realism as RE  # noqa: E402
from hml_v3.projection import selective as SEL  # noqa: E402
from hml_v3.projection import serialize as SZ  # noqa: E402
from run_expression_experiment import ask  # noqa: E402

VIEWS: tuple[str, ...] = (
    EX.NESTED_ONLY, EX.PATH_TO_ROOT, EX.LOCAL_SUBTREE, EX.DUAL_VIEW,
    EX.EXPLICIT_EDGE_LIST, EX.DEPTH_ADAPTIVE, SEL.SELECTIVE_LOCAL_CONTEXT,
)

REAL_LEAN_ACCURACY = 0.167


def make_pool(items: int, depth: int, distinct: int, recurrence: int, lead: int) -> list:
    return [DN.generate_dense_v2(i, depth, distinct, recurrence, lead)
            for i in range(items)]


def build_view(view: str, expression, options: list[str], levels: dict[str, int]):
    """Every view gets the same surrounding material; only the target's projection changes."""

    if view == SEL.SELECTIVE_LOCAL_CONTEXT:
        # The selective view keeps the target and drops the surroundings -- that IS the view.
        return SEL.build_document(expression, options, 0, levels)
    built = EX.build(view, expression, options)
    if not levels:
        return built
    # Give the non-selective views the regime's surrounding material, so the comparison is
    # between projections of the target and not between different amounts of context.
    realistic = RE.build_view(expression, options, levels, label=view)
    merged = realistic.__class__(label=view, source_id=expression.state_id)
    merged.provenance = built.provenance
    for block in realistic.blocks:
        if block.kind == "context":
            merged.add(block)
    for block in built.blocks:
        if block.kind != "context":
            merged.add(block)
    for block in realistic.blocks:
        if block.kind == "elsewhere_in_the_state":
            merged.add(block)
    merged.exposure = built.exposure
    return merged


def measure(model: str, pool: list, builder, arm: str = "CANDIDATE") -> dict[str, Any]:
    correct: list[bool] = []
    chars: list[int] = []
    for expression in pool:
        options = EX.options_for(expression)
        if not RE.answer_still_unique(expression, options):
            continue
        view = (EX.build(EX.FLATTENED_BAG, expression, options)
                if arm == "ABLATED_NEGATIVE" else builder(expression, options))
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
    parser.add_argument("--depth", type=int, default=10)
    parser.add_argument("--distinct", type=int, default=5)
    parser.add_argument("--easy", default="1,2", help="recurrence,lead for the easy regime")
    parser.add_argument("--hard", default="8,1", help="recurrence,lead for the hard regime")
    parser.add_argument("--hard-realism", default="1",
                        help="1 to add the realism factors to the hard regime, 0 for bare")
    parser.add_argument("--out", type=Path, default=ROOT / "reports/content_projection_v1")
    args = parser.parse_args()

    easy_r, easy_l = (int(v) for v in args.easy.split(","))
    hard_r, hard_l = (int(v) for v in args.hard.split(","))
    hard_levels: dict[str, int] = ({RE.TARGET_COPIES: 2, RE.DEEPER_IN_CONTEXT: 3,
                                    RE.CONTEXT_SIZE: 16}
                                   if args.hard_realism == "1" else {})
    regimes = {
        "EASY": {"recurrence": easy_r, "lead": easy_l, "levels": {}},
        "HARD": {"recurrence": hard_r, "lead": hard_l, "levels": hard_levels},
    }

    started = time.time()
    args.out.mkdir(parents=True, exist_ok=True)
    report: dict[str, Any] = {
        "model": args.model, "items": args.items, "depth": args.depth,
        "distinct": args.distinct, "generator": DN.DENSE_VERSION,
        "realism": RE.REALISM_VERSION, "regimes": {k: dict(v) for k, v in regimes.items()},
        "real_lean_accuracy": REAL_LEAN_ACCURACY, "views": {}, "selective_context": {},
        "instrument": {},
    }

    pools = {name: make_pool(args.items, args.depth, args.distinct,
                             spec["recurrence"], spec["lead"])
             for name, spec in regimes.items()}

    # Two views that render the same bytes are one experiment run twice, and reporting them
    # as separate arms would double-count. DEPTH_ADAPTIVE is defined to materialise edges at
    # depth >= 5, so at depth 10 it IS DUAL_VIEW; that is a property of the regime, not a
    # defect, and it is recorded rather than hidden.
    sample = pools["HARD"][0]
    sample_options = EX.options_for(sample)
    rendered_sample = {v: SZ.render(build_view(v, sample, sample_options,
                                               regimes["HARD"]["levels"])) for v in VIEWS}
    duplicates: dict[str, list[str]] = {}
    for left in VIEWS:
        for right in VIEWS:
            if left < right and rendered_sample[left] == rendered_sample[right]:
                duplicates.setdefault(left, []).append(right)
    report["identical_views_in_hard_regime"] = duplicates
    if duplicates:
        print(f"note: views that render identically in the hard regime: {duplicates}",
              flush=True)

    # ---------------------------------------------------------------- instrument per regime
    for name, spec in regimes.items():
        pool = pools[name]
        positive = measure(args.model, pool,
                           lambda e, o, lv=spec["levels"]: build_view(EX.NESTED_ONLY, e, o, lv),
                           arm="EXPLICIT_POSITIVE")
        negative = measure(args.model, pool, None, arm="ABLATED_NEGATIVE")
        chance = 1.0 / len(EX.options_for(pool[0]))
        verdict = C.classify_instrument(
            C.ArmResult("positive", sum(positive["per_item"]), positive["items"]),
            C.ArmResult("negative", sum(negative["per_item"]), negative["items"]), chance)
        report["instrument"][name] = {
            "positive": {k: v for k, v in positive.items() if k != "per_item"},
            "negative": {k: v for k, v in negative.items() if k != "per_item"},
            "verdict": verdict.to_dict()}
        print(f"{name:<5} instrument: positive {positive['accuracy']:.3f}  "
              f"negative {negative['accuracy']:.3f}  {verdict.status}  "
              f"({time.time() - started:.0f}s)", flush=True)

    # -------------------------------------------------------------------- §3 view comparison
    print(f"\n=== §3 VIEWS: {'view':<24}{'EASY':>8}{'HARD':>8}{'DROP':>8}", flush=True)
    for view in VIEWS:
        record: dict[str, Any] = {}
        for name, spec in regimes.items():
            record[name] = measure(
                args.model, pools[name],
                lambda e, o, v=view, lv=spec["levels"]: build_view(v, e, o, lv))
        drop = record["EASY"]["accuracy"] - record["HARD"]["accuracy"]
        record["drop"] = round(drop, 4)
        report["views"][view] = {
            **{k: {kk: vv for kk, vv in v.items() if kk != "per_item"}
               for k, v in record.items() if k in regimes},
            "drop": record["drop"],
            "per_item": {k: record[k]["per_item"] for k in regimes},
        }
        print(f"  {view:<24}{record['EASY']['accuracy']:>8.3f}"
              f"{record['HARD']['accuracy']:>8.3f}{drop:>+8.3f}  "
              f"({record['HARD']['mean_characters']} chars, {time.time() - started:.0f}s)",
              flush=True)
        (args.out / "HARD_REGIME.json").write_text(json.dumps(
            {**report, "elapsed_seconds": round(time.time() - started, 1)},
            indent=2, sort_keys=True) + "\n")

    # Every view is compared against NESTED_ONLY inside the hard regime, paired on items.
    nested_hard = report["views"][EX.NESTED_ONLY]["per_item"]["HARD"]
    for view in VIEWS:
        items = report["views"][view]["per_item"]["HARD"]
        if len(items) == len(nested_hard):
            status, reason, decided = C.compare(items, nested_hard)
            report["views"][view]["vs_nested_in_hard"] = {
                "status": status, "reason": reason, "decisive": decided}

    # ------------------------------------------------------------ §4 selective context ladder
    if hard_levels:
        print(f"\n=== §4 SELECTIVE CONTEXT in the HARD regime ===", flush=True)
        for label, level in SEL.DOCUMENT_LADDER:
            record = measure(
                args.model, pools["HARD"],
                lambda e, o, lv=level: SEL.build_document(e, o, lv, hard_levels))
            report["selective_context"][label] = {
                **{k: v for k, v in record.items() if k != "per_item"},
                "inclusion_level": level, "per_item": record["per_item"]}
            print(f"  {label:<24}{record['accuracy']:>8.3f} "
                  f"[{record['lower']:.2f},{record['upper']:.2f}]  "
                  f"{record['mean_characters']:>6} chars  "
                  f"({time.time() - started:.0f}s)", flush=True)
            (args.out / "HARD_REGIME.json").write_text(json.dumps(
                {**report, "elapsed_seconds": round(time.time() - started, 1)},
                indent=2, sort_keys=True) + "\n")

    # ------------------------------------------------------------------------------ summary
    print("\n=== §3 RESULT ===")
    print(f"  {'view':<24}{'EASY':>8}{'HARD':>8}{'DROP':>8}  vs NESTED in HARD")
    for view in VIEWS:
        entry = report["views"][view]
        comparison = entry.get("vs_nested_in_hard", {}).get("status", "-")
        print(f"  {view:<24}{entry['EASY']['accuracy']:>8.3f}{entry['HARD']['accuracy']:>8.3f}"
              f"{entry['drop']:>+8.3f}  {comparison}")
    best = min(VIEWS, key=lambda v: report["views"][v]["drop"])
    nested_drop = report["views"][EX.NESTED_ONLY]["drop"]
    print(f"\nsmallest collapse: {best} at {report['views'][best]['drop']:+.3f} "
          f"(NESTED_ONLY {nested_drop:+.3f}, delta "
          f"{nested_drop - report['views'][best]['drop']:+.3f})")
    if report["selective_context"]:
        print("\n=== §4 RESULT (minimum sufficient context) ===")
        for label, _level in SEL.DOCUMENT_LADDER:
            entry = report["selective_context"][label]
            print(f"  {label:<24}{entry['accuracy']:>8.3f}  {entry['mean_characters']:>6} chars")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
