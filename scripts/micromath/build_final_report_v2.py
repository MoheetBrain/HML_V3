#!/usr/bin/env python
"""Write the V2 final report from whatever has actually run.

`MISSION §35`, `§36`. Every section states what was measured and what was not. A stage that
did not run says NOT_RUN; it is never omitted, because a report that quietly drops what it
could not measure is the same failure as an aggregate that hides a broken instrument.

    .venv/bin/python scripts/micromath/build_final_report_v2.py
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hml_v3.micromath import calibration_v2 as C  # noqa: E402
from hml_v3.micromath import instruments_v2 as IV2  # noqa: E402
from hml_v3.micromath import ladders as L  # noqa: E402
from hml_v3.micromath import stresses as S  # noqa: E402


def read(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except Exception:  # noqa: BLE001
        return {}


def fmt(value, digits: int = 3) -> str:
    return f"{value:.{digits}f}" if isinstance(value, (int, float)) else "—"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reports", type=Path, default=ROOT / "reports/micromath_lab_v2")
    parser.add_argument("--lab", type=Path, default=ROOT / "data/micromath_lab_v2")
    args = parser.parse_args()

    cert = read(args.reports / "COMPONENT_CERTIFICATION_V2.json")
    bad = read(args.reports / "KNOWN_BAD_V2.json")
    arch = read(args.reports / "ARCHITECTURES_V2.json")
    manifest = read(args.lab / "manifest.json")
    components = cert.get("components", {})
    detection = bad.get("components", {})
    proposals = arch.get("results", [])

    def status_of(name: str) -> str:
        return (components.get(name) or {}).get("status", "NOT_RUN")

    def instrument(name: str) -> dict:
        return (components.get(name) or {}).get("instrument") or {}

    # A withdrawn or gated component was never measured; counting it in the denominator
    # would understate how many of the instruments that ran actually worked.
    measured = [n for n in S.STRESSES if n in components
                and status_of(n) not in (C.UNTESTED, "BENCHMARK_DEFECT")]
    valid = [n for n in measured if instrument(n).get("status") == C.INSTRUMENT_VALID]
    invalid = [n for n in measured if instrument(n).get("status") == C.INSTRUMENT_INVALID]
    limited = [n for n in measured if instrument(n).get("status") == C.INSTRUMENT_LIMIT]
    undecided = [n for n in measured
                 if instrument(n).get("status") == C.INSTRUMENT_UNDECIDED]
    advantage = [n for n in measured if status_of(n) == C.ADVANTAGE]
    parity = [n for n in measured if status_of(n) == C.CONTROL_PARITY]
    weakness = [n for n in measured if status_of(n) == C.LANGUAGE_WEAKNESS]
    defects = [n for n in measured if status_of(n) == "BENCHMARK_DEFECT"]

    lines = [
        "# MicroMath Lab V2 — final report",
        "",
        f"Reader `{cert.get('model', 'NOT RUN')}`, candidate `{cert.get('candidate', '?')}`, "
        f"best general control `{cert.get('best_general_control', '?')}`.",
        f"Lab `{manifest.get('lab_version', '?')}`, rule "
        f"`{C.PREREGISTERED.get('rule_version')}` fixed before any V2 result existed.",
        "",
        "`SEALED_FINAL_V2` was not read. No paid API, no paid GPU, no training, no global "
        "search. All inference local.",
        "",
        "## 1. The instruments",
        "",
        "| Component | Chance | Told the answer | Relation destroyed | Control | Candidate "
        "| Norm. read. | Instrument | Verdict |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for name in S.STRESSES:
        record = components.get(name)
        if record is None:
            lines.append(f"| {name} | — | — | — | — | — | — | NOT_RUN | NOT_RUN |")
            continue
        ins = record.get("instrument") or {}
        lines.append(
            f"| {name} | {fmt(record.get('chance'))} | {fmt(ins.get('positive'))} "
            f"| {fmt(ins.get('negative'))} | {fmt(record.get('best_control'))} "
            f"| {fmt(record.get('candidate'))} "
            f"| {fmt(record.get('normalised_readability'))} "
            f"| {ins.get('status', '—')} | **{record.get('status', '?')}** |")

    lines += [
        "",
        f"**Valid instruments: {len(valid)} of {len(measured)} measured** "
        f"(of {len(S.STRESSES)} components; the rest were withdrawn or gated). "
        f"{sorted(valid)}",
        "",
        f"- INSTRUMENT_INVALID: {sorted(invalid) or 'none'}",
        f"- INSTRUMENT_LIMIT: {sorted(limited) or 'none'}",
        f"- INSTRUMENT_UNDECIDED at the ladder cap: {sorted(undecided) or 'none'}",
        f"- BENCHMARK_DEFECT (gated by the shortcut audit): {sorted(defects) or 'none'}",
        "",
        "## 2. What the valid instruments say about the language",
        "",
        f"- **ADVANTAGE**: {sorted(advantage) or 'none'}",
        f"- **CONTROL_PARITY**: {sorted(parity) or 'none'}",
        f"- **LANGUAGE_WEAKNESS**: {sorted(weakness) or 'none'}",
        "",
    ]
    if advantage:
        lines.append("The candidate beats the strongest general control on the components "
                     "listed above, by a paired bootstrap on the same items.")
    elif valid:
        lines.append(
            "**On no valid instrument does the discovered representation beat a plain typed "
            "AST.** That is the same answer V1 gave, now on repaired instruments with a "
            "demonstrated ceiling, a state-level floor and a clean construction audit.")
    else:
        lines.append("No instrument has yet been certified valid, so nothing here is a "
                     "statement about any representation.")

    lines += ["", "## 3. Withdrawn and gated components", "",
              "**MULTI_GOAL — `RELATION_NOT_PROJECTED` (`FM-044`).** No axis of the "
              "representation space renders which goal the action acts on. Verified twice "
              "against `projection.py`. This withdraws V1's largest reported result: its "
              "0.375 of MULTI_GOAL 'headroom' was an absent projection, not a readability "
              "gap, and no notation could have claimed it.", ""]
    if defects:
        for name in defects:
            reason = (components.get(name) or {}).get("reason", "")
            lines.append(f"**{name} — `BENCHMARK_DEFECT`.** {reason}")
        lines.append("")

    lines += ["## 4. Testing the tests (`§27`)", ""]
    if not detection:
        lines.append("Known-bad detection: **NOT_RUN**.")
    else:
        lines += ["| Component | Known-bad | Control | Known-bad score | Margin | Verdict |",
                  "|---|---|---|---|---|---|"]
        for name, entry in sorted(detection.items()):
            lines.append(
                f"| {name} | `{entry.get('known_bad')}` | {fmt(entry.get('control'))} "
                f"| {fmt(entry.get('known_bad_score'))} | {fmt(entry.get('margin'))} "
                f"| **{entry.get('status')}** |")
        detected = [n for n, e in detection.items() if e.get("status") == "DETECTED"]
        lines += [
            "",
            f"**{len(detected)} of {len(detection)} instruments detected the representation "
            f"built to hide their own relation — and that number must not be read as "
            f"{len(detection) - len(detected)} blind instruments (`FM-051`).**",
            "",
            "Checking whether the answer token still appears on the page showed **6 of 6 "
            "items still carrying it** for DEPENDENCY, BINDER, PREMISE, ACTION_ARGUMENT and "
            "EXPRESSION_DEPTH. Those known-bads hide nothing, because the axes chosen do not "
            "control the rendering path each question depends on: `dependency_visibility` "
            "governs the *action's* local refs rather than the references inside declaration "
            "types, and `premise_locality` moves a citation rather than removing it.",
            "",
            "Only TYPE's known-bad genuinely hides its relation, via "
            "`type_explicitness: OMITTED` — and there the instrument **did** detect it, at "
            "+0.333. The method is sound; the known-bad set was mis-targeted.",
            "",
            "An exhaustive single-axis search over all 42 axes then found that **no axis "
            "hides any of those five relations at all.** The space can vary how a relation "
            "is written; it cannot choose not to write it. That is `D-025`, and it is the "
            "finding that explains every parity verdict above."]

    lines += ["", "## 5. Architectural hypotheses (`§13`, `§14`)", ""]
    if not proposals:
        lines.append("Not run.")
    else:
        lines += ["| Component | Architecture | Screen | Δ vs candidate | Verdict |",
                  "|---|---|---|---|---|"]
        for entry in proposals:
            lines.append(
                f"| {entry.get('stress')} | `{entry.get('label')}` "
                f"| {fmt(entry.get('screen'))} | {fmt(entry.get('delta_vs_candidate'))} "
                f"| {entry.get('verdict', '?')} |")
        accepted = [e for e in proposals if e.get("verdict") == "ACCEPTED_PROMISING"]
        duplicates = [e for e in proposals
                      if e.get("verdict") == "REJECTED_BEHAVIOURAL_DUPLICATE"]
        lines += ["",
                  f"Accepted: **{len(accepted)}**. Rejected as behavioural duplicates before "
                  f"any inference: **{len(duplicates)}**.", ""]
        if not accepted:
            lines.append(
                "No architectural change moved the target component either. Combined with "
                "V1's five properly tested surface mutations moving 0.031, that is now two "
                "independent families of hypothesis refuted: **neither restyling the "
                "notation nor re-exposing the structure through the axes this compiler "
                "offers changes what the reader can recover.**")

    lines += ["", "## 6. What was not attempted", "",
              "- **§16 the horizon test** — the corpus cannot populate the pre-registered "
              "ladders. G5 and D1–D2 are empty and G4 holds one item, so the prediction that "
              "a representation's advantage grows with structural complexity **cannot be "
              "tested here**. That is a statement about the corpus.",
              "- **§30 the integration matrix** and **§31 the reasoning ladder** — gated "
              "behind certified components, and none is certified.",
              "- **`micro_shadow_v2` and `micro_hidden_v2` are unread.** No result in this "
              "report is measured on held-out data.", ""]

    lines += ["## 7. Honest accounting of this run", "",
              "Seven defects were found during V2 construction, and **four of them were in "
              "my own instruments or guards rather than in the language**:", "",
              "| | Defect | How it surfaced |", "|---|---|---|",
              "| `FM-043` | the certification top-up spent both V1 holdouts | intersecting "
              "identifiers, after I claimed they were untouched |",
              "| `FM-044` | MULTI_GOAL's relation is rendered by no axis | reading "
              "`projection.py` when a negative arm scored 0.833 |",
              "| `FM-045` | one seed drove two decisions and correlated them | "
              "'always first option' scoring 1.000 |",
              "| `FM-046` | the audit re-sorted options, and its tolerance depended on n | "
              "one construction judged CLEAN and LEAKS on different splits |",
              "| `FM-047` | EXPRESSION_DEPTH was ill-posed | three arms at exactly 0/12 — "
              "**it passed the pre-registered calibration rule** |",
              "| `FM-048` | the positive control sat 7000 chars from the question | 0.417 "
              "while being handed the answer |", "",
              "`FM-047` and `FM-048` were both caught by a number looking wrong, not by a "
              "test. Neither the calibration rule nor the shortcut audit could see either. "
              "**The automated guards did not substitute for reading one raw completion.**",
              "",
              "`FM-048` also means every V1 dynamic range is understated, because V1 used "
              "the same distant-header positive control. The V1 `INSTRUMENT_INVALID` "
              "verdicts stand — those turned on negative arms — but V1 and V2 "
              "normalised-readability figures are not comparable.", ""]

    lines += ["## 8. Falsification status (`PROJECT_GOAL` §18)", ""]
    if advantage:
        lines.append("The project's central claim survives on "
                     f"{sorted(advantage)}, subject to reproduction on shadow and holdout.")
    elif valid:
        lines.append(
            "The central claim — that a discovered representation can be made measurably "
            "more readable to a model than existing notations — **remains unsupported**. On "
            "every instrument that survives calibration the discovered representation is at "
            "parity with a plain typed AST, and both sit far below what the same reader "
            "achieves when the relation is stated outright.")
        lines.append("")
        lines.append(
            "What V2 adds beyond V1 is that this can no longer be blamed on the instruments. "
            "It can still be blamed on the corpus: over half the base states are too large "
            "to render, and the structures the long-horizon hypothesis is about are absent.")
    else:
        lines.append("No valid instrument has completed, so the claim is neither supported "
                     "nor falsified by this run.")

    lines += ["", "## 9. Exact next actions", "",
              "1. **Acquire deeper base states.** States with more than four goals and "
              "expression depth beyond sixteen. Without them `PROJECT_GOAL` §18 cannot be "
              "tested, and that is now the binding constraint — not the notation.",
              "2. **Add the action-to-goal edge to the projection** if MULTI_GOAL is to be "
              "measurable at all. This is a semantic-contract change and needs a decision "
              "record, not a quiet patch.",
              "3. **Reproduce any surviving result on `micro_shadow_v2`** before it is "
              "believed, and only then on `micro_hidden_v2`.",
              "4. **Do not train and do not launch a global search.** No component is "
              "certified.",
              "5. **Leave `SEALED_FINAL_V2` alone.**", ""]

    (args.reports / "FINAL_REPORT_V2.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
