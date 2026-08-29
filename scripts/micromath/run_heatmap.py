#!/usr/bin/env python3
"""Phase 7/8: the heatmap and the failure gradient."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hml_v3.micromath import failure_gradient, heatmap  # noqa: E402
from hml_v3.micromath.domains import DOMAINS  # noqa: E402
from hml_v3.micromath.stresses import STRESSES  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", type=Path, required=True)
    parser.add_argument("--audit", type=Path,
                        default=ROOT / "reports/micromath_lab_v1/AUDIT_micro_dev.json")
    parser.add_argument("--out", type=Path, default=ROOT / "reports/micromath_lab_v1")
    args = parser.parse_args()

    probe = json.loads(args.probe.read_text())
    audit = json.loads(args.audit.read_text()) if args.audit.exists() else {}
    kinds = {c["label"]: c["kind"] for c in audit.get("candidates", [])}
    probe["kinds"] = kinds
    heat = heatmap.build(probe)

    gradients = {label: failure_gradient.gradient(heat, label)
                 for label in heat["matrices"]}
    payload = {"model": probe["model"], "split": probe["split"],
               "heatmap": heat, "failure_gradients": gradients}
    args.out.mkdir(parents=True, exist_ok=True)
    name = probe["model"].replace(":", "_").replace("/", "_")
    (args.out / f"heatmap_{name}.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n")

    lines = [f"# MicroMath Lab V1 — heatmap ({probe['model']}, {probe['split']})", "",
             "Cells are `accuracy (delta vs best control)`. Chance is 0.50 by construction: "
             "every item is a 2-alternative forced choice over a matched transposition. "
             "`—` marks a cell the corpus could not populate.", ""]
    order = ([l for l in heat["matrices"] if kinds.get(l) == "FINALIST"]
             + [l for l in heat["matrices"] if kinds.get(l) == "CONTROL"]
             + [l for l in heat["matrices"] if l not in kinds])
    for label in order:
        kind = kinds.get(label, "?")
        lines += [f"## `{label}` ({kind})", ""]
        lines += heatmap.render_markdown(heat, label)
        gradient = gradients[label]
        lines += ["",
                  f"Worst structure: **{gradient['worst_structure']}**. "
                  f"Cross-domain structural gaps: "
                  f"{gradient['cross_domain_structural_gaps'] or 'none'}.", ""]
    lines += ["## Saturation", "",
              "`MICROMATH §33`: a saturated column is reported and must not guide selection.",
              "", "| stress | verdict |", "|---|---|"]
    for stress in STRESSES:
        lines.append(f"| `{stress}` | {heat['saturation_by_stress'][stress]} |")
    (args.out / f"HEATMAP_{name}.md").write_text("\n".join(lines) + "\n")

    print(f"wrote HEATMAP_{name}.md")
    for label in order:
        gradient = gradients[label]
        print(f"  {kinds.get(label,'?'):8s} {label:22s} worst={gradient['worst_structure']} "
              f"cross_domain={gradient['cross_domain_structural_gaps']}")


if __name__ == "__main__":
    main()
