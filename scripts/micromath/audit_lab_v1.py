#!/usr/bin/env python3
"""Phase 5-7: shortcut audit, deterministic Level-A measurement, and the first heatmap."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hml_v3.micromath import deterministic, shortcut_controls  # noqa: E402
from hml_v3.micromath.candidates import load_controls, load_finalists  # noqa: E402
from hml_v3.micromath.corpus import load_split as _load_rows  # noqa: E402
from hml_v3.micromath.schema import MicroPair  # noqa: E402


def load_split(directory: Path, name: str) -> list[MicroPair]:
    return [MicroPair.from_dict(row) for row in _load_rows(directory, name)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lab", type=Path, default=ROOT / "data/micromath_lab_v1")
    parser.add_argument("--workspace", type=Path,
                        default=ROOT / "data/representation_search_v2")
    parser.add_argument("--frontier", type=Path,
                        default=ROOT / "reports/representation_search_v2/FINAL_FRONTIER.json")
    parser.add_argument("--split", default="micro_dev")
    parser.add_argument("--out", type=Path, default=ROOT / "reports/micromath_lab_v1")
    args = parser.parse_args()

    if args.split == "micro_hidden":
        raise SystemExit(
            "REFUSED: MICRO_HIDDEN is read once, after local optimisation has stabilised, "
            "by scripts/micromath/finalize_hidden.py -- not by the audit loop.")

    pairs = load_split(args.lab, args.split)
    candidates = load_finalists(args.workspace, args.frontier) + load_controls()
    print(f"{len(pairs)} pairs, {len(candidates)} representations "
          f"({sum(1 for c in candidates if c.kind == 'FINALIST')} finalists, "
          f"{sum(1 for c in candidates if c.kind == 'CONTROL')} controls)", flush=True)

    report: dict[str, object] = {"split": args.split, "pairs": len(pairs),
                                 "candidates": [], "shortcut_audit": {},
                                 "measurements": {}}
    for candidate in candidates:
        audit = shortcut_controls.audit(candidate.compiler, pairs)
        measurements = deterministic.measure(candidate.compiler, pairs)
        report["candidates"].append(candidate.to_dict())
        report["shortcut_audit"][candidate.label] = audit
        report["measurements"][candidate.label] = [m.to_dict() for m in measurements]
        expressible = sum(1 for m in measurements if m.expressible)
        print(f"  {candidate.kind:8s} {candidate.label:22s} "
              f"expressible={expressible:>2}/{len(measurements)} "
              f"shortcut={audit['verdict']:17s} "
              f"best_control_rule={max(audit['answer_targeted_controls']['accuracy'].values()):.3f} "
              f"layout_sensitive={len(audit['layout_sensitivity'])}", flush=True)

    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / f"AUDIT_{args.split}.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(f"wrote {args.out / f'AUDIT_{args.split}.json'}")


if __name__ == "__main__":
    main()
