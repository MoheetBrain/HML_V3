#!/usr/bin/env python
"""EXPERIMENT 2 (`MISSION §13`, `§28`): does materialising the action-to-goal edge help?

This is the cleanest possible test of the content-bearing thesis, because the intervention
is not a different spelling of an existing relation -- `FM-044` established that no axis of
the 42-axis genome renders the action-to-goal link at all. There is nothing to respell. The
intervention is putting the relation on the page.

Five arms:

    IMPLICIT_ADJACENCY   everything needed is present; the link itself is never stated
    EXPLICIT_EDGE        the link stated as its own record
    GOAL_LOCAL_ACTION    the action placed inside its goal's block -- organisation, not a
                         new statement
    SCRAMBLED_NEGATIVE   the arguments point at a goal the action does not act on
    ABSENT_NEGATIVE      verified known-bad; the action names nothing at all

Plus an explicit positive control. The purpose is the causal answer, not a permanent design
commitment to labelling goals (`§13`).

    .venv/bin/python scripts/projection/run_action_goal_experiment.py
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
from hml_v3.projection import action_goal as AG  # noqa: E402
from hml_v3.projection import audit as AU  # noqa: E402
from hml_v3.projection import model_view as MV  # noqa: E402
from hml_v3.projection import serialize as SZ  # noqa: E402

sys.path.insert(0, str(ROOT / "scripts" / "projection"))
from run_expression_experiment import ask  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="qwen38-rvn:latest")
    parser.add_argument("--items", type=int, default=40)
    parser.add_argument("--goals", type=int, default=4)
    parser.add_argument("--out", type=Path, default=ROOT / "reports/content_projection_v1")
    args = parser.parse_args()

    states = [AG.generate(i, goals=args.goals) for i in range(args.items)]
    chance = 1.0 / args.goals

    # Construction guards before any inference, in the order the session learned to need
    # them: is the answer constant, does its position leak, and does each view expose what
    # it claims (`FM-044`, `FM-045`, `FM-051`).
    targets = collections.Counter(s.target_goal for s in states)
    positions = collections.Counter()
    for state in states:
        _q, options, answer = AG.question(state)
        positions[list(options).index(answer)] += 1
    print(f"target goal distribution: {dict(sorted(targets.items()))}", flush=True)
    print(f"answer position distribution: {dict(sorted(positions.items()))}", flush=True)
    if max(targets.values()) > 0.6 * len(states):
        print("the target goal is near-constant; refusing to run")
        return 1
    if max(positions.values()) > 0.6 * len(states):
        print("the answer sits in one option slot too often; refusing to run")
        return 1

    sample = [AG.build(v, states[0]) for v in AG.VIEWS]
    exposure = AU.audit_views(sample)
    print(f"information exposure audit: {exposure['status']} {exposure['failing']}", flush=True)
    if exposure["status"] != "PASS":
        return 1
    known_bad = AU.verify_known_bad(
        [v for v in sample if v.label == AG.ABSENT_NEGATIVE][0], MV.ACTION_GOAL)
    print(f"known-bad ABSENT_NEGATIVE: {known_bad['status']}", flush=True)
    if not known_bad["hides_the_relation"]:
        return 1

    started = time.time()
    results: dict[str, dict] = {}
    args.out.mkdir(parents=True, exist_ok=True)

    def run(label: str, view: str | None, stated: bool = False) -> dict:
        correct: list[bool] = []
        costs: list[int] = []
        for state in states:
            question, options, answer = AG.question(state)
            built = AG.build(view or AG.IMPLICIT_ADJACENCY, state)
            rendered = SZ.render(built)
            costs.append(MV.cost_of(built, rendered).characters)
            listed_answer = answer if stated else None
            _pred, ok, _err = ask(args.model, rendered, question, options, answer,
                                  stated=listed_answer)
            correct.append(ok)
        return {"label": label, "accuracy": round(sum(correct) / len(correct), 4),
                "items": len(correct), "per_item": correct,
                "mean_characters": round(sum(costs) / len(costs)),
                "exposure": AU.verify_relation(
                    AG.build(view or AG.IMPLICIT_ADJACENCY, states[0]),
                    MV.ACTION_GOAL).verified}

    plans = [("EXPLICIT_POSITIVE", AG.IMPLICIT_ADJACENCY, True)] + [
        (v, v, False) for v in AG.VIEWS]
    for label, view, stated in plans:
        record = run(label, view, stated)
        results[label] = record
        print(f"  {label:<22}{record['accuracy']:.3f}  ({record['items']} items, "
              f"{record['mean_characters']} chars, {record['exposure']})  "
              f"({time.time() - started:.0f}s)", flush=True)

    implicit = results[AG.IMPLICIT_ADJACENCY]
    for label in (AG.EXPLICIT_EDGE, AG.GOAL_LOCAL_ACTION):
        status, reason, decided = C.compare(results[label]["per_item"],
                                            implicit["per_item"])
        results[label]["vs_implicit"] = {"status": status, "reason": reason,
                                         "decisive": decided}
        print(f"\n  {label} vs IMPLICIT_ADJACENCY: {status}\n    {reason}", flush=True)

    payload = {
        "model": args.model, "generator": AG.GENERATOR_VERSION, "items": args.items,
        "goals": args.goals, "chance": chance,
        "target_distribution": dict(sorted(targets.items())),
        "answer_position_distribution": dict(sorted(positions.items())),
        "exposure_audit": exposure, "known_bad": known_bad,
        "instrument": {
            "positive": results["EXPLICIT_POSITIVE"]["accuracy"],
            "negative_scrambled": results[AG.SCRAMBLED_NEGATIVE]["accuracy"],
            "negative_absent": results[AG.ABSENT_NEGATIVE]["accuracy"],
            "chance": chance},
        "elapsed_seconds": round(time.time() - started, 1),
        "arms": {k: {kk: vv for kk, vv in v.items() if kk != "per_item"}
                 for k, v in results.items()},
    }
    (args.out / "ACTION_GOAL_RESULTS.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(f"\nwrote {args.out}/ACTION_GOAL_RESULTS.json in {time.time() - started:.0f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
