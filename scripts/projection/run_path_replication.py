#!/usr/bin/env python
"""FINAL_HML_KILL_GATE §1: replicate PATH_TO_ROOT, or kill the static-language thesis.

`PATH_TO_ROOT` is the only positive representation result the project has produced. In
`HARD_REGIME_V1` it scored 0.500 against `NESTED_ONLY`'s 0.292 -- a +0.208 advantage, and the
only `ADVANTAGE` verdict among seven views. It rests on **one reader and 24 items**, which is
not enough to justify building an evolutionary search engine on top of it.

This replicates it on FRESH items from the already-validated generator, across two reader
families, with the decision rule fixed in `DECISION_RULE` below **before any number is read**.

What is deliberately held fixed: the `PATH_TO_ROOT` implementation is frozen and its source
hash is recorded in the output. It was not touched, tuned or reordered for this run.

The items are generated from indices 1000+ so they cannot overlap the 0..23 used in the
original measurement. Nothing sealed or hidden is read.

    .venv/bin/python scripts/projection/run_path_replication.py --items 128
"""

from __future__ import annotations

from typing import Any

import argparse
import hashlib
import inspect
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

#: HARD_REGIME_V1, exactly as frozen in PROJECT_STATUS.md.
DEPTH, DISTINCT, RECURRENCE, LEAD = 10, 5, 4, 1

#: Fresh index range. The original measurement used 0..23.
FIRST_INDEX = 1000

#: Reader A is the model the original result was measured on. Reader B must be a genuinely
#: different family -- not another alias or quantisation of the same base -- or the
#: replication tests nothing. qwen38-rvn is family qwen35; gemma4:31b is family gemma4.
READERS: tuple[tuple[str, str], ...] = (
    ("reader_A", "qwen38-rvn:latest"),
    ("reader_B", "gemma4:31b"),
)

ARMS: tuple[str, ...] = ("EXPLICIT_POSITIVE", "ABLATED_NEGATIVE", "NESTED_ONLY",
                         "PATH_TO_ROOT")

#: FIXED BEFORE THE RUN. Not to be redefined after seeing numbers.
DECISION_RULE = {
    "primary": "delta = accuracy(PATH_TO_ROOT) - accuracy(NESTED_ONLY), paired on items",
    "CONTINUE_PATH": "delta positive on BOTH readers AND pooled paired interval excludes "
                     "zero AND pooled delta >= +0.10 AND both instruments valid",
    "BORDERLINE": "direction replicates on both readers but the magnitude or interval "
                  "condition fails",
    "KILL_PATH": "the advantage disappears, reverses on either reader, is explained by an "
                 "instrument defect, or the pooled evidence is effectively parity",
    "material_threshold": 0.10,
    "fixed_before": "any replication number was observed",
}


def impl_hash() -> str:
    source = (inspect.getsource(EX.build) + inspect.getsource(EX._candidates)
              + inspect.getsource(EX._ancestry) + inspect.getsource(SZ.render)
              + inspect.getsource(SZ.render_block))
    return hashlib.sha256(source.encode()).hexdigest()


def measure(model: str, pool: list, arm: str) -> dict[str, Any]:
    correct: list[bool] = []
    chars: list[int] = []
    errors = 0
    for expression in pool:
        options = EX.options_for(expression)
        view_name = {"EXPLICIT_POSITIVE": EX.NESTED_ONLY,
                     "ABLATED_NEGATIVE": EX.FLATTENED_BAG,
                     "NESTED_ONLY": EX.NESTED_ONLY,
                     "PATH_TO_ROOT": EX.PATH_TO_ROOT}[arm]
        rendered = SZ.render(EX.build(view_name, expression, options))
        chars.append(len(rendered))
        question, _ = EX.question(options)
        predicted, ok, err = ask(
            model, rendered, question, options, expression.deepest,
            stated=expression.deepest if arm == "EXPLICIT_POSITIVE" else None)
        if predicted is None:
            errors += 1
        correct.append(ok)
    n = len(correct)
    lower, upper = C.clopper_pearson(sum(correct), n)
    return {"accuracy": round(sum(correct) / n, 4), "n": n,
            "lower": round(lower, 4), "upper": round(upper, 4),
            "unparsed": errors,
            "mean_characters": round(sum(chars) / len(chars)),
            "per_item": correct}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--items", type=int, default=128)
    parser.add_argument("--out", type=Path, default=ROOT / "reports/content_projection_v1")
    args = parser.parse_args()

    started = time.time()
    args.out.mkdir(parents=True, exist_ok=True)

    pool = [DN.generate_dense_v2(i, DEPTH, DISTINCT, RECURRENCE, LEAD)
            for i in range(FIRST_INDEX, FIRST_INDEX + args.items)]
    # The generator refuses to emit an item whose walk disagrees with its construction, so
    # reaching here means every answer is the verified unique deepest reference.
    ids = {e.state_id for e in pool}
    assert len(ids) == len(pool), "duplicate items generated"
    original = {DN.generate_dense_v2(i, DEPTH, DISTINCT, RECURRENCE, LEAD).state_id
                for i in range(24)}
    overlap = ids & original
    print(f"pool: {len(pool)} fresh verified items; overlap with the original 24: "
          f"{len(overlap)}", flush=True)
    print(f"PATH_TO_ROOT impl sha256: {impl_hash()}", flush=True)
    print(f"decision rule fixed before the run: CONTINUE needs both readers positive, "
          f"pooled interval excluding zero, pooled delta >= "
          f"{DECISION_RULE['material_threshold']:+.2f}\n", flush=True)

    report: dict[str, Any] = {
        "regime": {"depth": DEPTH, "distinct": DISTINCT, "recurrence": RECURRENCE,
                   "lead": LEAD, "label": "HARD_REGIME_V1"},
        "items": args.items, "first_index": FIRST_INDEX,
        "overlap_with_original": len(overlap),
        "generator": DN.DENSE_VERSION,
        "path_to_root_impl_sha256": impl_hash(),
        "decision_rule": DECISION_RULE,
        "original_single_reader_result": {"nested": 0.292, "path": 0.500, "delta": 0.208,
                                          "n": 24, "reader": "qwen38-rvn:latest"},
        "readers": {},
    }

    for label, model in READERS:
        print(f"=== {label}: {model}", flush=True)
        arms = {arm: measure(model, pool, arm) for arm in ARMS}
        chance = 1.0 / len(EX.options_for(pool[0]))
        verdict = C.classify_instrument(
            C.ArmResult("positive", sum(arms["EXPLICIT_POSITIVE"]["per_item"]),
                        arms["EXPLICIT_POSITIVE"]["n"]),
            C.ArmResult("negative", sum(arms["ABLATED_NEGATIVE"]["per_item"]),
                        arms["ABLATED_NEGATIVE"]["n"]), chance)
        delta = C.paired_bootstrap(arms["PATH_TO_ROOT"]["per_item"],
                                   arms["NESTED_ONLY"]["per_item"])
        status, reason, decided = C.compare(arms["PATH_TO_ROOT"]["per_item"],
                                            arms["NESTED_ONLY"]["per_item"])
        norm = {a: C.normalised_readability(arms[a]["accuracy"],
                                            arms["EXPLICIT_POSITIVE"]["accuracy"],
                                            arms["ABLATED_NEGATIVE"]["accuracy"])
                for a in ("NESTED_ONLY", "PATH_TO_ROOT")}
        report["readers"][label] = {
            "model": model, "chance": round(chance, 4),
            "arms": {a: {k: v for k, v in r.items() if k != "per_item"}
                     for a, r in arms.items()},
            "per_item": {a: r["per_item"] for a, r in arms.items()},
            "instrument": verdict.to_dict(),
            "delta_path_minus_nested": {"estimate": round(delta["difference"], 4),
                                        "lower": round(delta["lower"], 4),
                                        "upper": round(delta["upper"], 4),
                                        "status": status, "reason": reason,
                                        "decisive": decided},
            "normalised_readability": norm,
        }
        for arm in ARMS:
            r = arms[arm]
            print(f"  {arm:<20}{r['accuracy']:.3f} [{r['lower']:.3f},{r['upper']:.3f}]  "
                  f"{r['mean_characters']:>5} chars  unparsed {r['unparsed']}", flush=True)
        print(f"  instrument: {verdict.status} (pos {verdict.positive:.3f}, "
              f"neg {verdict.negative:.3f}, chance {chance:.3f})", flush=True)
        print(f"  DELTA path-nested {delta['difference']:+.4f} "
              f"[{delta['lower']:+.4f},{delta['upper']:+.4f}]  {status}  "
              f"({time.time() - started:.0f}s)\n", flush=True)
        (args.out / "PATH_REPLICATION.json").write_text(
            json.dumps({**report, "elapsed_seconds": round(time.time() - started, 1)},
                       indent=2, sort_keys=True) + "\n")

    # ------------------------------------------------------------------------ pooled
    pooled_path: list[bool] = []
    pooled_nested: list[bool] = []
    for label, _model in READERS:
        pooled_path += report["readers"][label]["per_item"]["PATH_TO_ROOT"]
        pooled_nested += report["readers"][label]["per_item"]["NESTED_ONLY"]
    pooled = C.paired_bootstrap(pooled_path, pooled_nested)
    pooled_status, pooled_reason, pooled_decided = C.compare(pooled_path, pooled_nested)
    report["pooled"] = {"estimate": round(pooled["difference"], 4),
                        "lower": round(pooled["lower"], 4),
                        "upper": round(pooled["upper"], 4),
                        "status": pooled_status, "reason": pooled_reason,
                        "decisive": pooled_decided, "n": len(pooled_path)}

    deltas = {label: report["readers"][label]["delta_path_minus_nested"]["estimate"]
              for label, _m in READERS}
    instruments_valid = all(
        report["readers"][label]["instrument"]["status"] == C.INSTRUMENT_VALID
        for label, _m in READERS)
    both_positive = all(value > 0 for value in deltas.values())
    excludes_zero = pooled["lower"] > 0.0
    material = pooled["difference"] >= DECISION_RULE["material_threshold"]

    if not instruments_valid:
        decision = "INSTRUMENT_UNRESOLVED"
    elif both_positive and excludes_zero and material:
        decision = "CONTINUE_PATH"
    elif both_positive:
        decision = "BORDERLINE"
    else:
        decision = "KILL_PATH"
    report["verdict"] = {
        "decision": decision,
        "both_readers_positive": both_positive,
        "pooled_excludes_zero": excludes_zero,
        "pooled_meets_material_threshold": material,
        "all_instruments_valid": instruments_valid,
        "per_reader_delta": deltas,
    }

    (args.out / "PATH_REPLICATION.json").write_text(
        json.dumps({**report, "elapsed_seconds": round(time.time() - started, 1)},
                   indent=2, sort_keys=True) + "\n")

    print("=== PATH_TO_ROOT REPLICATION ===")
    print(f"  {'reader':<10}{'model':<22}{'nested':>8}{'path':>8}{'delta':>9}"
          f"{'95% CI':>20}  instrument")
    for label, model in READERS:
        entry = report["readers"][label]
        d = entry["delta_path_minus_nested"]
        interval = f"[{d['lower']:+.3f},{d['upper']:+.3f}]"
        print(f"  {label:<10}{model:<22}{entry['arms']['NESTED_ONLY']['accuracy']:>8.3f}"
              f"{entry['arms']['PATH_TO_ROOT']['accuracy']:>8.3f}{d['estimate']:>+9.4f}"
              f"{interval:>20}  {entry['instrument']['status']}")
    print(f"\n  pooled delta {pooled['difference']:+.4f} "
          f"[{pooled['lower']:+.4f},{pooled['upper']:+.4f}]  n={len(pooled_path)}  "
          f"{pooled_status}")
    print(f"\n  both readers positive:      {both_positive}")
    print(f"  pooled excludes zero:       {excludes_zero}")
    print(f"  pooled >= +0.10:            {material}")
    print(f"  all instruments valid:      {instruments_valid}")
    print(f"\n  VERDICT: {decision}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
