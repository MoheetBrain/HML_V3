"""The domain x structural-stress heatmap, and the failure gradient it feeds.

`MICROMATH §8` and `§30`: the point is to SEE the failure shape. The cell is the primitive
unit and results are not collapsed to an overall accuracy, because "geometry is bad" is not
an actionable diagnosis while "dependency recovery is weak in three domains at once" is.

`§15`: the number that matters is never the candidate's own score. It is
``score(candidate) - max(score(controls))`` on the same items.
`§33`: any column whose spread is nil is labelled and excluded from guiding selection.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

from hml_v3.micromath.domains import DOMAINS
from hml_v3.micromath.stresses import STRESSES

DISCRIMINATIVE = "DISCRIMINATIVE"
LOW_VARIANCE = "LOW_VARIANCE"
NEAR_SATURATED = "NEAR_SATURATED"
SATURATED = "SATURATED"


def saturation(values: Sequence[float]) -> str:
    """`§33`: saturation diagnostics are first class, not a footnote."""

    numeric = [v for v in values if v is not None]
    if not numeric:
        return SATURATED
    low, high = min(numeric), max(numeric)
    spread = high - low
    scale = max(abs(high), abs(low), 1e-12)
    if len({round(v, 9) for v in numeric}) <= 1 or spread <= 1e-9:
        return SATURATED
    if spread / scale <= 0.02:
        return NEAR_SATURATED
    if spread / scale <= 0.10:
        return LOW_VARIANCE
    return DISCRIMINATIVE


@dataclass
class CellScore:
    domain: str
    stress: str
    value: float | None
    items: int

    def to_dict(self) -> dict[str, Any]:
        return {"domain": self.domain, "stress": self.stress,
                "value": None if self.value is None else round(self.value, 4),
                "items": self.items}


def build(probe_payload: dict[str, Any]) -> dict[str, Any]:
    """Turn a probe run into per-candidate matrices plus the best-control deltas."""

    cell_accuracy = probe_payload["cell_accuracy"]
    kinds = probe_payload.get("kinds", {})
    controls = [label for label in cell_accuracy if kinds.get(label) == "CONTROL"]
    if not controls:
        controls = [l for l in cell_accuracy
                    if l in {"LEAN_LIKE", "STRUCTURED_ENGLISH", "TYPED_AST", "OLD_HML"}]

    def cell(label: str, domain: str, stress: str) -> float | None:
        return cell_accuracy.get(label, {}).get(f"{domain}|{stress}")

    best_control: dict[str, float] = {}
    for domain in DOMAINS:
        for stress in STRESSES:
            values = [cell(c, domain, stress) for c in controls]
            values = [v for v in values if v is not None]
            if values:
                best_control[f"{domain}|{stress}"] = max(values)

    matrices: dict[str, Any] = {}
    for label in cell_accuracy:
        rows: dict[str, dict[str, Any]] = {}
        for stress in STRESSES:
            rows[stress] = {}
            for domain in DOMAINS:
                key = f"{domain}|{stress}"
                value = cell(label, domain, stress)
                rows[stress][domain] = {
                    "accuracy": None if value is None else round(value, 4),
                    "delta_best_control": (
                        None if value is None or key not in best_control
                        else round(value - best_control[key], 4)),
                }
        matrices[label] = rows

    by_stress: dict[str, str] = {}
    for stress in STRESSES:
        column = [cell(label, domain, stress)
                  for label in cell_accuracy for domain in DOMAINS]
        by_stress[stress] = saturation([v for v in column if v is not None])

    return {
        "controls": sorted(controls),
        "best_control_per_cell": best_control,
        "matrices": matrices,
        "saturation_by_stress": by_stress,
        "note": ("delta_best_control is the reported signal. A candidate's own accuracy is "
                 "not evidence of superiority on its own."),
    }


def render_markdown(heat: dict[str, Any], label: str) -> list[str]:
    rows = heat["matrices"][label]
    header = "| stress | " + " | ".join(d[:9] for d in DOMAINS) + " |"
    lines = [header, "|---" * (len(DOMAINS) + 1) + "|"]
    for stress in STRESSES:
        cells = []
        for domain in DOMAINS:
            entry = rows[stress][domain]
            if entry["accuracy"] is None:
                cells.append("—")
            else:
                delta = entry["delta_best_control"]
                cells.append(f"{entry['accuracy']:.2f} ({delta:+.2f})"
                             if delta is not None else f"{entry['accuracy']:.2f}")
        lines.append(f"| `{stress}` | " + " | ".join(cells) + " |")
    return lines
