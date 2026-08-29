"""The failure gradient: where to spend the next mutation, and why.

`MICROMATH §17` and `§42` are the methodological core. A low score in one domain is where a
failure APPEARS. The cause is a structure. So weaknesses are aggregated by structural stress
ACROSS domains, and a weakness present in several domains at once outranks a weakness
confined to one -- because the first is a representation problem and the second may be a
corpus accident.

`§18`: a domain-specific primitive is not proposed on this evidence. The recommended target
is always a universal structural mechanism.
"""

from __future__ import annotations

from typing import Any

from hml_v3.micromath.domains import DOMAINS
from hml_v3.micromath.stresses import STRESS_QUESTION, STRESSES

#: A cell counts as weak when it trails the best control by more than this.
WEAK_MARGIN = 0.10
#: A structural weakness is called cross-domain once it appears in this many domains.
CROSS_DOMAIN_MIN = 2


def gradient(heat: dict[str, Any], label: str) -> dict[str, Any]:
    rows = heat["matrices"][label]
    cells: list[dict[str, Any]] = []
    for stress in STRESSES:
        for domain in DOMAINS:
            entry = rows[stress][domain]
            if entry["accuracy"] is None or entry["delta_best_control"] is None:
                continue
            cells.append({
                "domain": domain, "stress": stress,
                "accuracy": entry["accuracy"],
                "delta_best_control": entry["delta_best_control"],
            })

    by_stress: dict[str, list[dict[str, Any]]] = {}
    for cell in cells:
        by_stress.setdefault(cell["stress"], []).append(cell)

    structural: list[dict[str, Any]] = []
    for stress, group in by_stress.items():
        deltas = [c["delta_best_control"] for c in group]
        weak = [c for c in group if c["delta_best_control"] < -WEAK_MARGIN]
        structural.append({
            "stress": stress,
            "question": STRESS_QUESTION[stress],
            "domains_measured": len(group),
            "mean_delta_best_control": round(sum(deltas) / len(deltas), 4),
            "worst_delta": round(min(deltas), 4),
            "mean_accuracy": round(sum(c["accuracy"] for c in group) / len(group), 4),
            "weak_domains": sorted(c["domain"] for c in weak),
            "cross_domain": len(weak) >= CROSS_DOMAIN_MIN,
        })
    structural.sort(key=lambda item: (not item["cross_domain"],
                                      item["mean_delta_best_control"]))

    worst_cell = min(cells, key=lambda c: c["delta_best_control"]) if cells else None
    by_domain: dict[str, list[float]] = {}
    for cell in cells:
        by_domain.setdefault(cell["domain"], []).append(cell["delta_best_control"])
    domain_means = {d: round(sum(v) / len(v), 4) for d, v in by_domain.items()}

    target = structural[0] if structural else None
    return {
        "candidate": label,
        "worst_structure": target["stress"] if target else None,
        "worst_domain": (min(domain_means, key=domain_means.get)
                         if domain_means else None),
        "worst_cell": worst_cell,
        "structural_ranking": structural,
        "domain_mean_delta": domain_means,
        "cross_domain_structural_gaps": [
            item["stress"] for item in structural if item["cross_domain"]],
        "recommended_next_mutation_target": target["stress"] if target else None,
        "why": (
            f"{target['stress']} trails the best control by "
            f"{target['mean_delta_best_control']:+.3f} across "
            f"{target['domains_measured']} domains"
            + (f" and is weak in {len(target['weak_domains'])} of them, which points at the "
               "representation of that structure rather than at any one domain"
               if target["cross_domain"] else
               ", but is not weak in two or more domains, so the evidence does not yet "
               "distinguish a representation problem from a corpus accident")
        ) if target else "no measured cells",
        "rule": ("MICROMATH §42: a low domain score locates a failure; the structure it "
                 "shares with other domains identifies the cause. Never propose a "
                 "domain-specific primitive from a single weak domain."),
    }
