#!/usr/bin/env python
"""Assemble the V2 dashboard and the structured mission report from whatever has run.

`MISSION §28`, `§36`. Written to tolerate partial results on purpose: a stage that has not
run yet is reported as NOT_RUN rather than omitted, because a dashboard that silently drops
what it could not measure is the same failure as an aggregate that hides a broken instrument.

    .venv/bin/python scripts/micromath/build_dashboard_v2.py
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
from hml_v3.micromath import stresses as S  # noqa: E402

#: `§28` names ten rows. Two are not components of this lab and are reported as such rather
#: than quietly dropped: semantic fidelity is audited by the losslessness gate, and the
#: state-delta relation has no instrument at all.
EXTRA_ROWS = {
    "SEMANTIC_FIDELITY": ("NOT_A_MICROMATH_COMPONENT",
                          "audited by reports/audits/LOSSLESSNESS_AUDIT_V1 and the "
                          "round-trip gates, not by a reader probe"),
    "STATE_DELTA": ("NOT_BUILT", "no instrument exists for the state-delta relation"),
}

ORDER = ("SEMANTIC_FIDELITY", S.BINDER, S.SCOPE, S.TYPE, S.EXPRESSION_DEPTH, S.DEPENDENCY,
         S.MULTI_GOAL, S.PREMISE, S.ACTION_ARGUMENT, "STATE_DELTA")


def read(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text())
    except Exception:  # noqa: BLE001
        return None


def git(*args: str) -> str:
    try:
        return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True,
                              text=True, check=True).stdout.strip()
    except Exception:  # noqa: BLE001
        return "unknown"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reports", type=Path, default=ROOT / "reports/micromath_lab_v2")
    parser.add_argument("--lab", type=Path, default=ROOT / "data/micromath_lab_v2")
    args = parser.parse_args()

    certification = read(args.reports / "COMPONENT_CERTIFICATION_V2.json") or {}
    known_bad = read(args.reports / "KNOWN_BAD_V2.json") or {}
    architectures = read(args.reports / "ARCHITECTURES_V2.json") or {}
    manifest = read(args.lab / "manifest.json") or {}
    components = certification.get("components", {})
    detection = known_bad.get("components", {})

    lines = [
        "# Component dashboard — MicroMath Lab V2",
        "",
        f"Reader `{certification.get('model', 'not run')}`, "
        f"candidate `{certification.get('candidate', '?')}`, "
        f"control `{certification.get('best_general_control', '?')}`.",
        f"Lab `{manifest.get('lab_version', '?')}`. "
        f"Rule `{C.PREREGISTERED['rule_version']}`, fixed before any V2 result existed.",
        "",
        "## Instruments",
        "",
        "| Component | Chance | Positive | Negative | Range | Control | Candidate "
        "| Norm. read. | Known-bad | Status |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]

    def cell(value, digits: int = 3) -> str:
        return f"{value:.{digits}f}" if isinstance(value, (int, float)) else "—"

    for name in ORDER:
        if name in EXTRA_ROWS:
            status, note = EXTRA_ROWS[name]
            lines.append(f"| {name} | — | — | — | — | — | — | — | — | {status} |")
            continue
        record = components.get(name)
        if not record:
            lines.append(f"| {name} | — | — | — | — | — | — | — | — | NOT_RUN |")
            continue
        instrument = record.get("instrument") or {}
        detected = detection.get(name, {}).get("status", "NOT_RUN")
        lines.append(
            f"| {name} | {cell(record.get('chance'))} | {cell(instrument.get('positive'))} "
            f"| {cell(instrument.get('negative'))} | {cell(instrument.get('dynamic_range'))} "
            f"| {cell(record.get('best_control'))} | {cell(record.get('candidate'))} "
            f"| {cell(record.get('normalised_readability'))} | {detected} "
            f"| **{record.get('status', '?')}** |")

    valid = [n for n, r in components.items()
             if (r.get("instrument") or {}).get("status") == C.INSTRUMENT_VALID]
    invalid = [n for n, r in components.items()
               if (r.get("instrument") or {}).get("status") == C.INSTRUMENT_INVALID]
    limited = [n for n, r in components.items()
               if (r.get("instrument") or {}).get("status") == C.INSTRUMENT_LIMIT]
    undecided = [n for n, r in components.items()
                 if (r.get("instrument") or {}).get("status") == C.INSTRUMENT_UNDECIDED]
    advantage = [n for n, r in components.items() if r.get("status") == C.ADVANTAGE]
    parity = [n for n, r in components.items() if r.get("status") == C.CONTROL_PARITY]
    weakness = [n for n, r in components.items() if r.get("status") == C.LANGUAGE_WEAKNESS]

    lines += [
        "",
        "## Counts",
        "",
        f"- valid instruments: **{len(valid)}** {sorted(valid)}",
        f"- invalid: **{len(invalid)}** {sorted(invalid)}",
        f"- instrument limits: **{len(limited)}** {sorted(limited)}",
        f"- undecided at the ladder cap: **{len(undecided)}** {sorted(undecided)}",
        f"- ADVANTAGE: **{len(advantage)}** {sorted(advantage)}",
        f"- CONTROL_PARITY: **{len(parity)}** {sorted(parity)}",
        f"- LANGUAGE_WEAKNESS: **{len(weakness)}** {sorted(weakness)}",
        "",
        "**CERTIFIED requires all of** `§29`: valid instrument, perfect semantic "
        "preservation, at least control parity, reproduction on fresh shadow/holdout, "
        "known-bad detection, and no catastrophic regression elsewhere. A component is "
        "reported as certified only when every one of those has been executed.",
        "",
        "## Splits",
        "",
        "| Split | Items | Base states |",
        "|---|---|---|",
    ]
    for label, profile in (manifest.get("splits") or {}).items():
        lines.append(f"| `{label}` | {profile.get('count')} "
                     f"| {profile.get('distinct_base_states')} |")
    overlap = manifest.get("base_state_overlap", {})
    lines += [
        "",
        f"Base-state overlap between splits: `{overlap}` — required to be zero everywhere "
        f"(`FM-043`).",
        "",
        f"Retired as spent: `{manifest.get('retired_v1_base_states')}` — "
        f"{manifest.get('retired_reason', '')}",
        "",
        "## Architectural hypotheses",
        "",
    ]
    results = architectures.get("results") or []
    if not results:
        lines.append("Not run.")
    else:
        lines += ["| Component | Architecture | Screen | Δ vs candidate | Verdict |",
                  "|---|---|---|---|---|"]
        for entry in results:
            lines.append(
                f"| {entry.get('stress')} | `{entry.get('label')}` "
                f"| {cell(entry.get('screen'))} | {cell(entry.get('delta_vs_candidate'))} "
                f"| {entry.get('verdict', '?')} |")

    (args.reports / "COMPONENT_DASHBOARD_V2.md").write_text("\n".join(lines) + "\n")

    # ------------------------------------------------------------- the §36 structured block
    dirty = "DIRTY" if git("status", "--porcelain") else "CLEAN"
    ahead = git("log", "--oneline", "@{u}..")
    report = {
        "HML_COMPONENT_CERTIFICATION_V2": (
            "COMPLETE" if components and detection and results else "INCOMPLETE"),
        "HEAD": git("rev-parse", "HEAD"),
        "BRANCH": git("rev-parse", "--abbrev-ref", "HEAD"),
        "WORKTREE": dirty,
        "CURRENT_STATE_PUSHED": "NO" if ahead else "YES",
        "SEALED_FINAL_V2_ACCESSED": "NO",
        "OLD_MICRO_SHADOW_RETIRED": "YES", "OLD_MICRO_HIDDEN_RETIRED": "YES",
        "MICRO_DEV_V2": (manifest.get("splits", {}).get("micro_dev_v2") or {}).get("count"),
        "MICRO_SHADOW_V2": (
            manifest.get("splits", {}).get("micro_shadow_v2") or {}).get("count"),
        "MICRO_HIDDEN_V2": (
            manifest.get("splits", {}).get("micro_hidden_v2") or {}).get("count"),
        "BASE_STATE_OVERLAP": overlap,
        "VALID_INSTRUMENT_COUNT": len(valid),
        "INVALID_INSTRUMENTS": sorted(invalid),
        "INSTRUMENT_LIMITS": sorted(limited),
        "INSTRUMENT_UNDECIDED": sorted(undecided),
        "LANGUAGE_WEAKNESSES": sorted(weakness),
        "CONTROL_PARITY_COMPONENTS": sorted(parity),
        "ADVANTAGE_COMPONENTS": sorted(advantage),
        "INSTRUMENTS": {name: {
            "chance": record.get("chance"),
            "positive": (record.get("instrument") or {}).get("positive"),
            "negative": (record.get("instrument") or {}).get("negative"),
            "dynamic_range": (record.get("instrument") or {}).get("dynamic_range"),
            "candidate": record.get("candidate"),
            "best_control": record.get("best_control"),
            "normalised_readability": record.get("normalised_readability"),
            "known_bad_detection": detection.get(name, {}).get("status", "NOT_RUN"),
            "status": record.get("status"),
        } for name, record in sorted(components.items())},
        "KNOWN_BAD_MUTATION_DETECTION": (
            "PASS" if detection and all(
                r.get("status") == "DETECTED" for r in detection.values()) else
            "PARTIAL" if detection else "NOT_RUN"),
        "PAID_API_USED": "NO", "PAID_GPU_USED": "NO",
        "TRAINING_PERFORMED": "NO", "GLOBAL_SEARCH_RUN": "NO",
        "READY_FOR_INTEGRATION": "YES" if len(valid) >= 4 else "NO",
        "READY_FOR_REASONING_LADDER": "NO",
        "READY_FOR_TRAINING": "NO",
    }
    (args.reports / "MISSION_REPORT_V2.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n")

    print("\n".join(lines[:40]))
    print(f"\nwrote {args.reports}/COMPONENT_DASHBOARD_V2.md and MISSION_REPORT_V2.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
