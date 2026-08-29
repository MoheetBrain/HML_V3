#!/usr/bin/env python3
"""COMPONENT_CERTIFICATION_V1: calibrate the instrument, then judge the language.

Four arms per component (§4): EXPLICIT_POSITIVE, SCRAMBLED_NEGATIVE, the strong general
controls, and the current candidate. The verdict rule is preregistered in
`micromath.calibration` and was fixed before any calibration number existed.
"""

from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hml_v3.micromath import calibration, neural, targeted_search as TS  # noqa: E402
from hml_v3.micromath.candidates import CONTROLS, load_controls, load_finalists  # noqa: E402
from hml_v3.micromath.corpus import load_base_pool, load_split  # noqa: E402
from hml_v3.micromath.schema import MicroPair  # noqa: E402
from hml_v3.micromath.stresses import STRESS_QUESTION, STRESSES  # noqa: E402

#: §32: the three weakest components first, so a partial run still answers the live question.
PRIORITY = ("MULTI_GOAL", "EXPRESSION_DEPTH", "DEPENDENCY")


def probe(model, compiler, pairs):
    items = neural.build_items(compiler, pairs)
    if not items:
        return 0.0, 0
    results = neural.run_probe(model, items)
    return sum(1 for r in results if r.correct) / len(results), len(items)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lab", type=Path, default=ROOT / "data/micromath_lab_v1")
    parser.add_argument("--workspace", type=Path,
                        default=ROOT / "data/representation_search_v2")
    parser.add_argument("--frontier", type=Path,
                        default=ROOT / "reports/representation_search_v2/FINAL_FRONTIER.json")
    parser.add_argument("--corpus", type=Path,
                        default=ROOT / "data/corpus/search_pool_v2.jsonl.gz")
    parser.add_argument("--probe-report", type=Path,
                        default=ROOT / "reports/micromath_lab_v1/PROBE_micro_dev_qwen38-rvn_latest.json")
    parser.add_argument("--model", default="qwen38-rvn:latest")
    parser.add_argument("--pairs-per-component", type=int, default=12)
    parser.add_argument("--components", default="")
    parser.add_argument("--out", type=Path, default=ROOT / "reports/micromath_lab_v1")
    args = parser.parse_args()

    model = neural.LocalModel(args.model)
    if not model.available():
        raise SystemExit(f"{args.model} not installed")

    report = json.loads(args.probe_report.read_text())
    overall = {l: sum(1 for r in rows if r["correct"]) / len(rows)
               for l, rows in report["results"].items()}
    finalists = {c.label: c for c in load_finalists(args.workspace, args.frontier)}
    controls = {c.label: c for c in load_controls()}
    candidate = finalists[max(finalists, key=lambda l: overall[l])]
    best_control_label = max(CONTROLS, key=lambda l: overall.get(l, 0.0))
    best_control = controls[best_control_label]
    print(f"candidate: {candidate.label} ({overall[candidate.label]:.3f}) | "
          f"best general control: {best_control_label} "
          f"({overall[best_control_label]:.3f})", flush=True)

    pool, _prov = load_base_pool(args.corpus)
    dev = [MicroPair.from_dict(r) for r in load_split(args.lab, "micro_dev")]
    by_stress = collections.defaultdict(list)
    for pair in dev:
        by_stress[pair.stress].append(pair)
    # FM-043: the top-up must exclude every reserved split, not just micro_dev.
    # Initialising `used` from dev alone let build_targeted_suite mint certification
    # pairs on base states belonging to micro_hidden and micro_shadow, spending both.
    used = {p.base_transition_id for p in dev}
    for reserved in ("micro_hidden", "micro_shadow"):
        used |= {MicroPair.from_dict(r).base_transition_id
                 for r in load_split(args.lab, reserved)}

    wanted = ([s.strip() for s in args.components.split(",") if s.strip()]
              or list(PRIORITY) + [s for s in STRESSES if s not in PRIORITY])
    components: dict[str, dict] = {}
    started = time.time()

    for stress in wanted:
        suite = list(by_stress.get(stress, []))
        need = args.pairs_per_component - len(suite)
        if need > 0:
            extra = TS.build_targeted_suite(pool, stress, used, need)
            used |= {p.base_transition_id for p in extra}
            suite += extra
        if not suite:
            components[stress] = {"status": calibration.UNTESTED,
                                  "reason": "no pairs available"}
            print(f"\n{stress}: UNTESTED (no pairs)", flush=True)
            continue

        positive, negative = calibration.build_arms(best_control.compiler, suite, stress)
        print(f"\n=== {stress} — {STRESS_QUESTION[stress]} "
              f"({len(suite)} pairs) ===", flush=True)
        arms = {}
        for label, compiler in (("EXPLICIT_POSITIVE", positive),
                                ("SCRAMBLED_NEGATIVE", negative),
                                (best_control_label, best_control.compiler),
                                (candidate.label, candidate.compiler)):
            accuracy, items = probe(model, compiler, suite)
            arms[label] = accuracy
            print(f"  {label:22s} {accuracy:.3f}  ({items} items, "
                  f"{time.time()-started:.0f}s)", flush=True)

        status, reason = calibration.classify(
            arms["EXPLICIT_POSITIVE"], arms["SCRAMBLED_NEGATIVE"],
            arms[candidate.label], arms[best_control_label])
        readability = calibration.normalised_readability(
            arms[candidate.label], arms["EXPLICIT_POSITIVE"], arms["SCRAMBLED_NEGATIVE"])
        components[stress] = {
            "status": status, "reason": reason,
            "pairs": len(suite),
            "positive": round(arms["EXPLICIT_POSITIVE"], 4),
            "negative": round(arms["SCRAMBLED_NEGATIVE"], 4),
            "dynamic_range": round(
                arms["EXPLICIT_POSITIVE"] - arms["SCRAMBLED_NEGATIVE"], 4),
            "candidate": round(arms[candidate.label], 4),
            "best_control": round(arms[best_control_label], 4),
            "normalised_readability": (None if readability is None
                                       else round(readability, 4)),
        }
        print(f"  -> {status}: {reason}", flush=True)

        payload = {
            "model": args.model, "candidate": candidate.label,
            "best_general_control": best_control_label,
            "rule": {
                "positive_must_exceed_chance_by": calibration.POSITIVE_MUST_EXCEED_CHANCE,
                "negative_max_above_chance": calibration.NEGATIVE_MAX_ABOVE_CHANCE,
                "minimum_dynamic_range": calibration.MINIMUM_DYNAMIC_RANGE,
                "parity_margin": calibration.PARITY_MARGIN,
                "preregistered": True,
            },
            "components": components,
            "elapsed_seconds": round(time.time() - started, 1),
        }
        args.out.mkdir(parents=True, exist_ok=True)
        (args.out / "COMPONENT_CERTIFICATION.json").write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(f"\n=== COMPONENT CERTIFICATION ({time.time()-started:.0f}s) ===")
    for stress, entry in components.items():
        print(f"  {stress:20s} {entry['status']}")


if __name__ == "__main__":
    main()
