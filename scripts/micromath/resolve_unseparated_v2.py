#!/usr/bin/env python
"""Re-run, at a higher rung, every component whose candidate-vs-control gap is unresolved.

`MISSION §9`. A point estimate that clears the parity margin while its bootstrap interval
still contains zero is not a result in either direction -- it is a sample-size problem, and
the ladder exists to spend items exactly there and nowhere else.

The first V2 pass stopped every component at twelve items because escalation was wired to
instrument uncertainty only, not to comparison uncertainty (`FM-049`). This finds the
components where more items would actually change the answer and re-runs only those.

    .venv/bin/python scripts/micromath/resolve_unseparated_v2.py
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hml_v3.micromath import calibration_v2 as C  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reports", type=Path, default=ROOT / "reports/micromath_lab_v2")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    path = args.reports / "COMPONENT_CERTIFICATION_V2.json"
    payload = json.loads(path.read_text())
    components = payload.get("components", {})

    wanted: list[str] = []
    for name, record in sorted(components.items()):
        instrument = record.get("instrument") or {}
        if instrument.get("status") != C.INSTRUMENT_VALID:
            continue
        candidate, control = record.get("candidate"), record.get("best_control")
        if not isinstance(candidate, (int, float)) or not isinstance(control, (int, float)):
            continue
        gap = candidate - control
        used = record.get("items_used", 0)
        already = record.get("comparison_decisive")
        if abs(gap) > C.PARITY_MARGIN and already is not True and used < C.LADDER[-1]:
            wanted.append(name)
            print(f"  {name:<18}gap {gap:+.3f} at n={used} — unresolved, re-running")
        else:
            print(f"  {name:<18}gap {gap:+.3f} at n={used} — settled, leaving alone")

    if not wanted:
        print("\nnothing to resolve")
        return 0
    print(f"\nre-running {len(wanted)}: {wanted}")
    if args.dry_run:
        return 0

    # Merge-on-write in the certification script means these overwrite only themselves.
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/micromath/run_certification_v2.py"),
         "--components", ",".join(wanted)], cwd=ROOT)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
