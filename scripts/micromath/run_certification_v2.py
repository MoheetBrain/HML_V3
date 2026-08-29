#!/usr/bin/env python
"""Component certification V2: calibrate the instrument, then judge the language.

`MISSION §3`, `§8`, `§9`, `§35`. For every component, run four arms on the same items --
explicit positive, ablated negative, strongest general control, candidate -- and apply the
rule pre-registered in ``calibration_v2`` before any V2 result existed.

The ladder (`§9`) stops as soon as the instrument verdict is decided, so no Qwen inference is
spent proving a point that twelve items already made.

    .venv/bin/python scripts/micromath/run_certification_v2.py
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

from hml_v3.micromath import calibration_v2 as C  # noqa: E402
from hml_v3.micromath import instruments_v2 as IV2  # noqa: E402
from hml_v3.micromath import probe_v2 as P  # noqa: E402
from hml_v3.micromath import shortcut_v2 as SC  # noqa: E402
from hml_v3.micromath import stresses as S  # noqa: E402
from hml_v3.micromath.candidates import CONTROLS, load_controls, load_finalists  # noqa: E402
from hml_v3.micromath.corpus import load_split  # noqa: E402
from hml_v3.micromath.firewall import DEV, SplitFirewall, SplitViolation  # noqa: E402

PRIORITY = (S.MULTI_GOAL, S.EXPRESSION_DEPTH, S.DEPENDENCY, S.TYPE, S.PREMISE, S.BINDER,
            S.SCOPE, S.ACTION_ARGUMENT)


def load_items(lab: Path, name: str) -> list[IV2.MicroItem]:
    return [IV2.MicroItem.from_dict(row) for row in load_split(lab, name)]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lab", type=Path, default=ROOT / "data/micromath_lab_v2")
    parser.add_argument("--workspace", type=Path,
                        default=ROOT / "data/representation_search_v2")
    parser.add_argument("--frontier", type=Path,
                        default=ROOT / "reports/representation_search_v2/FINAL_FRONTIER.json")
    parser.add_argument("--candidate", default="R_015b8cd926da")
    parser.add_argument("--control", default="TYPED_AST")
    parser.add_argument("--model", default="qwen38-rvn:latest")
    parser.add_argument("--components", default="")
    parser.add_argument("--out", type=Path, default=ROOT / "reports/micromath_lab_v2")
    args = parser.parse_args()

    firewall = SplitFirewall.load(args.lab / "firewall.json")
    items = load_items(args.lab, "micro_dev_v2")
    # The firewall is consulted even though these items came from the dev file: FM-043 was
    # a run that never named a split and still consumed two holdouts, so the check that
    # matters is on the base state, every time, not on where the rows were read from.
    firewall.admit(DEV, [{"transition_id": i.base_transition_id,
                          "source_specific_reference": i.source_file,
                          "provenance": {}} for i in items])
    print(f"firewall: {len(items)} dev items admitted, "
          f"{sum(len(v) for v in firewall.retired.values())} retired states refused",
          flush=True)

    controls = {c.label: c for c in load_controls()}
    finalists = {c.label: c for c in load_finalists(args.workspace, args.frontier)}
    candidate = finalists[args.candidate]
    control = controls[args.control]

    by_stress: dict[str, list] = collections.defaultdict(list)
    for item in items:
        by_stress[item.stress].append(item)

    # The shortcut audit is a HARD GATE and it runs before a single probe is sent. It costs
    # nothing, and the first V2 build spent 277 seconds of inference discovering by probe
    # what a two-line answer count says instantly: MULTI_GOAL had the answer "g1" on 43 of
    # 43 items. A cell that a rule which never reads the mathematics can solve is not an
    # instrument, and no calibration of it means anything.
    audit = SC.audit_by_stress(items)
    leaky = set(SC.failing(audit))
    for name, entry in sorted(audit.items()):
        print(f"  audit {name:<18}{entry['status']:<16}best dumb rule "
              f"{entry['worst_score']:.3f} (lower {entry['worst_lower_bound']:.3f}) "
              f"vs chance {entry['chance']:.3f}", flush=True)
    if leaky:
        print(f"  GATED OUT by the shortcut audit: {sorted(leaky)}", flush=True)

    wanted = ([s.strip() for s in args.components.split(",") if s.strip()] or list(PRIORITY))
    # Carry forward anything a previous partial run already measured, so a component added
    # later merges rather than replacing the file. Only the components named in this run are
    # overwritten.
    components: dict[str, dict] = {}
    existing = args.out / "COMPONENT_CERTIFICATION_V2.json"
    if existing.exists():
        try:
            components = json.loads(existing.read_text()).get("components", {})
        except Exception:  # noqa: BLE001
            components = {}
    started = time.time()
    args.out.mkdir(parents=True, exist_ok=True)

    for stress in wanted:
        available = sorted(by_stress.get(stress, []), key=lambda i: i.item_id)
        if not available:
            components[stress] = {
                "status": C.UNTESTED,
                "reason": (IV2.MULTI_GOAL_WITHDRAWN if stress == S.MULTI_GOAL
                           else "no dev items for this stress")}
            print(f"\n=== {stress}: UNTESTED ===", flush=True)
            continue
        if stress in leaky:
            components[stress] = {
                "status": "BENCHMARK_DEFECT", "available": len(available),
                "shortcut_audit": audit[stress],
                "reason": audit[stress]["reason"]}
            print(f"\n=== {stress}: BENCHMARK_DEFECT — {audit[stress]['reason']} ===",
                  flush=True)
            continue

        chance = sum(i.chance for i in available) / len(available)
        print(f"\n=== {stress} — {S.STRESS_QUESTION[stress]} "
              f"({len(available)} available, chance {chance:.3f}) ===", flush=True)

        arms: dict[str, list] = {}
        verdict = None
        used = 0
        for rung in C.LADDER:
            if rung > len(available):
                rung = len(available)
            suite = available[:rung]
            if rung == used:
                break
            used = rung

            plans = (
                (P.EXPLICIT_POSITIVE, control.compiler,
                 {"positive_header": IV2.POSITIVE_HEADER[stress]}),
                (P.ABLATED_NEGATIVE, control.compiler, {"use_ablated": True}),
                (args.control, control.compiler, {}),
                (args.candidate, candidate.compiler, {}),
            )
            arms, per_item = {}, {}
            for label, compiler, kwargs in plans:
                probes = P.build_probes(compiler, suite, label, **kwargs)
                successes, trials, outcomes = P.run(args.model, probes)
                arms[label] = C.ArmResult(label, successes, trials)
                # Kept for the paired comparison. Re-probing candidate and control to get
                # them would double the inference bill for numbers already in hand.
                per_item[label] = {o.probe.item_id: o.correct for o in outcomes}
                print(f"  n={rung:<3} {label:<22}{successes}/{trials} = "
                      f"{successes / trials if trials else 0:.3f}   "
                      f"({time.time() - started:.0f}s)", flush=True)

            verdict = C.classify_instrument(
                arms[P.EXPLICIT_POSITIVE], arms[P.ABLATED_NEGATIVE], chance)
            if verdict.decisive:
                break
            print(f"      undecided at n={rung}; escalating", flush=True)

        record: dict = {"chance": round(chance, 4), "items_used": used,
                        "available": len(available),
                        "instrument": verdict.to_dict() if verdict else None}
        if verdict and verdict.status == C.INSTRUMENT_VALID:
            # Pair on the item ids both arms actually scored; an item dropped by one
            # representation's codec is not a paired observation.
            shared = sorted(set(per_item[args.candidate]) & set(per_item[args.control]))
            candidate_items = [per_item[args.candidate][i] for i in shared]
            control_items = [per_item[args.control][i] for i in shared]
            status, reason = C.compare(candidate_items, control_items)
            record["paired_items"] = len(shared)
            record["status"] = status
            record["reason"] = reason
            record["candidate"] = round(arms[args.candidate].accuracy, 4)
            record["best_control"] = round(arms[args.control].accuracy, 4)
            record["normalised_readability"] = C.normalised_readability(
                arms[args.candidate].accuracy, arms[P.EXPLICIT_POSITIVE].accuracy,
                arms[P.ABLATED_NEGATIVE].accuracy)
            print(f"  -> INSTRUMENT_VALID; {status}: {reason}", flush=True)
        elif verdict:
            record["status"] = verdict.status
            record["reason"] = verdict.reason
            record["candidate"] = round(arms[args.candidate].accuracy, 4)
            record["best_control"] = round(arms[args.control].accuracy, 4)
            print(f"  -> {verdict.status}: {verdict.reason}", flush=True)

        components[stress] = record
        (args.out / "COMPONENT_CERTIFICATION_V2.json").write_text(json.dumps({
            "model": args.model, "candidate": args.candidate,
            "best_general_control": args.control,
            "rule": C.PREREGISTERED, "lab": IV2.LAB_VERSION,
            "shortcut_audit": audit,
            "elapsed_seconds": round(time.time() - started, 1),
            "components": components}, indent=2, sort_keys=True) + "\n")

    print(f"\n=== COMPONENT CERTIFICATION V2 ({time.time() - started:.0f}s) ===")
    for stress in wanted:
        record = components.get(stress, {})
        print(f"  {stress:<18}{record.get('status', 'UNTESTED')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
