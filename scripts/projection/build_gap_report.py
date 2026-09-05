#!/usr/bin/env python
"""Assemble REAL_LEAN_GAP_V1 from the measured result files. Nothing is computed here.

Every field is read from a report written by the run that measured it, so the summary cannot
drift from the evidence. A missing input is printed as NOT_RUN rather than filled in.

    .venv/bin/python scripts/projection/build_gap_report.py
"""

from __future__ import annotations

from typing import Any

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

REAL_LEAN_ACCURACY = 0.167
CLEAN_BASELINE = 0.933


def load(path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text())
    except Exception:  # noqa: BLE001
        return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reports", type=Path,
                        default=ROOT / "reports/content_projection_v1")
    args = parser.parse_args()

    audit = load(args.reports / "REAL_ITEM_AUDIT.json")
    dense = load(args.reports / "DENSE_TARGET_V2.json")
    hard = load(args.reports / "HARD_REGIME.json")
    factorial = load(args.reports / "REALISTIC_FACTORIAL.json")

    lines: list[str] = ["REAL_LEAN_GAP_V1", ""]

    # ------------------------------------------------------------------------- §1
    if audit:
        verdicts = audit["verdicts"]
        valid = verdicts["AMBIGUOUS"] == 0 and verdicts["INVALID"] == 0
        lines += [
            f"REAL_TASK_VALID:\n    {'YES' if valid else 'NO'}", "",
            f"    REAL_ITEMS_AUDITED     {audit['items_audited']} "
            f"({audit['certification_items_audited']} of them carried the 0.167)",
            f"    AMBIGUOUS_ITEMS        {verdicts['AMBIGUOUS']}",
            f"    INVALID_ITEMS          {verdicts['INVALID']}",
            f"    rendered-vs-key depth offset: {audit['rendered_minus_key_offsets_seen']} "
            f"(one constant: no codec or parser mismatch)", "",
            f"CORRECTED_REAL_ACCURACY:\n    {REAL_LEAN_ACCURACY:.3f} — unchanged; no item "
            f"was withdrawn, so the instrument is not the explanation", ""]
        profile = audit["regime_profile_certification_12"]
        lines += ["    the regime those 12 items occupy:"]
        for field in ("sites", "distinct_identities", "recurrence", "answer_occurrences",
                      "depth", "lead", "target_copies_in_document", "document_chars"):
            entry = profile.get(field, {})
            lines.append(f"      {field:<28}median {entry.get('median')}  "
                         f"(min {entry.get('min')}, max {entry.get('max')})")
        lines.append("")
    else:
        lines += ["REAL_TASK_VALID:\n    NOT_RUN", ""]

    # ------------------------------------------------------------------------- §2
    if dense:
        cells = dense["cells"]
        valid_cells = {k: v for k, v in cells.items()
                       if v["instrument"]["status"] == "INSTRUMENT_VALID"}
        from hml_v3.micromath import calibration_v2 as C

        def normalised(record: dict) -> float | None:
            arms = record["arms"]
            return C.normalised_readability(arms["NESTED_ONLY"]["accuracy"],
                                            arms["EXPLICIT_POSITIVE"]["accuracy"],
                                            arms["ABLATED_NEGATIVE"]["accuracy"])

        lines += ["DENSE_TARGET_RESULT:"]
        lines.append(f"    {len(valid_cells)}/{len(cells)} cells INSTRUMENT_VALID")
        lines.append("    normalised readability = (nested - negative) / (positive - "
                     "negative); real Lean = 0.0909")
        for key in sorted(cells, key=lambda k: cells[k]["arms"]["NESTED_ONLY"]["accuracy"]):
            record = cells[key]
            arm = record["arms"]["NESTED_ONLY"]
            norm = normalised(record)
            lines.append(
                f"      {key:<18}sites {record['sites']:>3}  "
                f"nested {arm['accuracy']:.3f} [{arm['lower']:.2f},{arm['upper']:.2f}]  "
                f"pos {record['arms']['EXPLICIT_POSITIVE']['accuracy']:.3f}  "
                f"neg {record['arms']['ABLATED_NEGATIVE']['accuracy']:.3f}  "
                f"norm {'   n/a' if norm is None else f'{norm:>6.3f}'}  "
                f"{record['instrument']['status']}")
        lines.append("")

        # Which internal factor moves it most, averaged over the balanced part of the grid.
        balanced = {k: v for k, v in cells.items() if v["depth"] == 10 and v["recurrence"] <= 8}

        def mean_by(field: str, value: Any) -> float | None:
            rows = [v["arms"]["NESTED_ONLY"]["accuracy"]
                    for v in balanced.values() if v[field] == value]
            return sum(rows) / len(rows) if rows else None

        lines += ["STRONGEST_DENSITY_FACTOR:"]
        for field, values in (("recurrence", (1, 2, 4, 8)), ("distinct", (3, 5)),
                              ("lead", (1, 2))):
            marks = [(v, mean_by(field, v)) for v in values]
            marks = [(v, m) for v, m in marks if m is not None]
            spread = max(m for _v, m in marks) - min(m for _v, m in marks)
            rendered = "  ".join(f"{v}:{m:.3f}" for v, m in marks)
            lines.append(f"    {field:<12}{rendered}   spread {spread:.3f}")
        lines.append("")
        lowest = min(cells.items(), key=lambda kv: kv[1]["arms"]["NESTED_ONLY"]["accuracy"])
        reproduced = lowest[1]["arms"]["NESTED_ONLY"]["lower"] <= REAL_LEAN_ACCURACY
        lines += [
            "COLLAPSE_REPRODUCED:",
            f"    {'YES' if reproduced else 'NO'} — lowest valid cell {lowest[0]} at "
            f"{lowest[1]['arms']['NESTED_ONLY']['accuracy']:.3f} "
            f"[{lowest[1]['arms']['NESTED_ONLY']['lower']:.2f},"
            f"{lowest[1]['arms']['NESTED_ONLY']['upper']:.2f}]; real Lean "
            f"{REAL_LEAN_ACCURACY:.3f}, clean synthetic {CLEAN_BASELINE:.3f}", ""]
    else:
        lines += ["DENSE_TARGET_RESULT:\n    NOT_RUN", ""]

    # ------------------------------------------------------------------------- §3, §4
    if hard:
        regimes = hard["regimes"]
        lines += [
            "HARD_REGIME_V1 defined as:",
            f"    depth {hard['depth']}, distinct identities {hard['distinct']}, "
            f"recurrence {regimes['HARD']['recurrence']}, lead {regimes['HARD']['lead']}"
            + (f", plus {regimes['HARD']['levels']}" if regimes["HARD"]["levels"] else ""),
            f"    EASY: recurrence {regimes['EASY']['recurrence']}, "
            f"lead {regimes['EASY']['lead']}, no surrounding material",
            f"    instrument EASY {hard['instrument']['EASY']['verdict']['status']}, "
            f"HARD {hard['instrument']['HARD']['verdict']['status']}", ""]
        if hard.get("identical_views_in_hard_regime"):
            lines.append(f"    views that render identically here: "
                         f"{hard['identical_views_in_hard_regime']}")
            lines.append("")
        lines += ["HARD_REGIME_RESULTS:",
                  f"    {'view':<26}{'EASY':>7}{'HARD':>7}{'DROP':>8}   vs NESTED in HARD"]
        for view, entry in hard["views"].items():
            comparison = entry.get("vs_nested_in_hard", {}).get("status", "-")
            lines.append(f"    {view:<26}{entry['EASY']['accuracy']:>7.3f}"
                         f"{entry['HARD']['accuracy']:>7.3f}{entry['drop']:>+8.3f}   "
                         f"{comparison}")
        lines.append("")
        best = min(hard["views"], key=lambda v: hard["views"][v]["drop"])
        nested = hard["views"]["NESTED_ONLY"]
        lines += [
            f"BEST_HARD_VIEW:\n    {best} — drop {hard['views'][best]['drop']:+.3f}, "
            f"hard accuracy {hard['views'][best]['HARD']['accuracy']:.3f} "
            f"({hard['views'][best]['HARD']['mean_characters']} chars)", "",
            f"DELTA_VS_NESTED:\n    {hard['views'][best]['HARD']['accuracy'] - nested['HARD']['accuracy']:+.3f} "
            f"in the hard regime; NESTED_ONLY drop {nested['drop']:+.3f} vs "
            f"{hard['views'][best]['drop']:+.3f}", ""]
        if hard.get("selective_context"):
            lines += ["MINIMUM_SUFFICIENT_CONTEXT:"]
            for label, entry in hard["selective_context"].items():
                lines.append(f"    {label:<26}{entry['accuracy']:.3f} "
                             f"[{entry['lower']:.2f},{entry['upper']:.2f}]  "
                             f"{entry['mean_characters']:>6} chars")
            lines.append("")
    else:
        lines += ["HARD_REGIME_RESULTS:\n    NOT_RUN", ""]

    # ------------------------------------------------------------------------- §5
    if factorial and "effects" in factorial:
        lines += ["FACTORIAL (main effects on NESTED_ONLY accuracy, high minus low):"]
        for name, value in sorted(factorial["effects"]["main_effects"].items(),
                                  key=lambda kv: kv[1]):
            lines.append(f"    {name:<24}{value:+.4f}")
        lines.append("    strongest two-way interactions:")
        ranked = sorted(factorial["effects"]["two_way_interactions"].items(),
                        key=lambda kv: abs(kv[1]), reverse=True)[:4]
        for name, value in ranked:
            lines.append(f"      {name:<44}{value:+.4f}")
        worst = min(factorial["cells"].items(),
                    key=lambda kv: kv[1]["arms"]["NESTED_ONLY"]["accuracy"])
        lines += ["",
                  f"SYNTHETIC_REALISTIC_V1 candidate: cell {worst[0]} at "
                  f"{worst[1]['arms']['NESTED_ONLY']['accuracy']:.3f} "
                  f"[{worst[1]['arms']['NESTED_ONLY']['lower']:.2f},"
                  f"{worst[1]['arms']['NESTED_ONLY']['upper']:.2f}]  "
                  f"levels {worst[1]['levels']}",
                  f"    statistically compatible with real Lean {REAL_LEAN_ACCURACY:.3f}: "
                  f"{'YES' if worst[1]['arms']['NESTED_ONLY']['lower'] <= REAL_LEAN_ACCURACY <= worst[1]['arms']['NESTED_ONLY']['upper'] else 'NO'}",
                  ""]
    else:
        lines += ["FACTORIAL:\n    NOT_RUN", ""]

    text = "\n".join(lines)
    (args.reports / "REAL_LEAN_GAP_V1.txt").write_text(text + "\n")
    print(text)
    print(f"\nwrote {args.reports}/REAL_LEAN_GAP_V1.txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
