#!/usr/bin/env python
"""Test the tests: can each instrument detect a representation that hides its relation?

`MISSION §27`. Calibration proves an instrument *can* separate "relation stated" from
"relation destroyed" when the destruction happens in the state. It does not prove the
instrument can see the difference between representations, which is what it will actually be
asked to do.

So each instrument is shown a representation built to hide precisely the relation it measures
-- DELETE_DEPENDENCY_EDGES for DEPENDENCY, REMOVE_TYPE_LINK for TYPE, and so on -- and must
rank it below a competent control. An instrument that scores the known-bad as highly as the
control cannot see the relation, and its verdict about any real representation is worthless.

    .venv/bin/python scripts/micromath/run_known_bad_v2.py
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

from hml_v3.micromath import architectures as A  # noqa: E402
from hml_v3.micromath import calibration_v2 as C  # noqa: E402
from hml_v3.micromath import instruments_v2 as IV2  # noqa: E402
from hml_v3.micromath import probe_v2 as P  # noqa: E402
from hml_v3.micromath import stresses as S  # noqa: E402
from hml_v3.micromath.candidates import load_controls  # noqa: E402
from hml_v3.micromath.corpus import load_split  # noqa: E402

ITEMS = 12
#: The control must beat its matching known-bad by at least this for the instrument to be
#: credited with detection. Below it, the instrument saw nothing.
DETECTION_MARGIN = 0.08


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lab", type=Path, default=ROOT / "data/micromath_lab_v2")
    parser.add_argument("--control", default="TYPED_AST")
    parser.add_argument("--model", default="qwen38-rvn:latest")
    parser.add_argument("--components", default="")
    parser.add_argument("--out", type=Path, default=ROOT / "reports/micromath_lab_v2")
    args = parser.parse_args()

    items = [IV2.MicroItem.from_dict(r) for r in load_split(args.lab, "micro_dev_v2")]
    by_stress: dict[str, list] = collections.defaultdict(list)
    for item in items:
        by_stress[item.stress].append(item)
    for stress in by_stress:
        by_stress[stress].sort(key=lambda i: i.item_id)

    control = {c.label: c for c in load_controls()}[args.control]
    wanted = [s.strip() for s in args.components.split(",") if s.strip()] or list(S.STRESSES)

    started = time.time()
    results: dict[str, dict] = {}
    args.out.mkdir(parents=True, exist_ok=True)

    for stress in wanted:
        suite = by_stress.get(stress, [])[:ITEMS]
        label = A.DETECTS[stress]
        if not suite:
            results[stress] = {"status": "UNTESTED", "reason": "no dev items"}
            continue
        chance = sum(i.chance for i in suite) / len(suite)

        bad_compiler, axes = A.realise_known_bad(label)
        good = P.build_probes(control.compiler, suite, args.control)
        bad = P.build_probes(bad_compiler, suite, label)

        # A known-bad that renders identically to the control is not a known-bad; it is the
        # control under another name, and scoring it would prove nothing either way.
        if (A.behavioural_digest(control.compiler, suite)
                == A.behavioural_digest(bad_compiler, suite)):
            results[stress] = {
                "status": "KNOWN_BAD_INEFFECTIVE", "known_bad": label, "axes": axes,
                "reason": "the known-bad renders identically to the control, so it does not "
                          "hide anything and cannot test the instrument"}
            print(f"{stress:<18}KNOWN_BAD_INEFFECTIVE ({label} renders like the control)",
                  flush=True)
            continue

        good_successes, good_trials, good_outcomes = P.run(args.model, good)
        bad_successes, bad_trials, bad_outcomes = P.run(args.model, bad)
        good_accuracy = good_successes / good_trials if good_trials else 0.0
        bad_accuracy = bad_successes / bad_trials if bad_trials else 0.0
        margin = good_accuracy - bad_accuracy

        shared = sorted({o.probe.item_id for o in good_outcomes}
                        & {o.probe.item_id for o in bad_outcomes})
        left = {o.probe.item_id: o.correct for o in good_outcomes}
        right = {o.probe.item_id: o.correct for o in bad_outcomes}
        paired = C.paired_bootstrap([left[i] for i in shared], [right[i] for i in shared])

        status = "DETECTED" if margin >= DETECTION_MARGIN else "INSTRUMENT_DEFECT"
        results[stress] = {
            "status": status, "known_bad": label, "axes": axes, "chance": round(chance, 4),
            "control": round(good_accuracy, 4), "known_bad_score": round(bad_accuracy, 4),
            "margin": round(margin, 4), "paired": paired, "items": len(shared),
            "reason": (f"the control beats {label} by {margin:+.3f}"
                       if status == "DETECTED" else
                       f"{label} hides the relation and still scores {bad_accuracy:.3f} "
                       f"against the control's {good_accuracy:.3f}; this instrument cannot "
                       f"see the relation it claims to measure"),
        }
        print(f"{stress:<18}{status:<20}control {good_accuracy:.3f} vs {label} "
              f"{bad_accuracy:.3f}  margin {margin:+.3f}  ({time.time() - started:.0f}s)",
              flush=True)

        (args.out / "KNOWN_BAD_V2.json").write_text(json.dumps({
            "model": args.model, "control": args.control, "items": ITEMS,
            "detection_margin": DETECTION_MARGIN, "lab": IV2.LAB_VERSION,
            "elapsed_seconds": round(time.time() - started, 1),
            "components": results}, indent=2, sort_keys=True) + "\n")

    detected = sum(1 for r in results.values() if r.get("status") == "DETECTED")
    print(f"\n=== KNOWN-BAD DETECTION: {detected}/{len(results)} instruments detected "
          f"their matching known-bad ({time.time() - started:.0f}s) ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
