#!/usr/bin/env python3
"""Is the frontier a property of the representations, or of the dev split?

Selection read `SEARCH_DEV` every generation. If the finalists' ordering is an artifact of
that particular sample, the ordering will not survive on `SEARCH_VALIDATION`, which selection
never touched. This measures the finalists on both and compares the per-axis rankings.

Rank correlation is Spearman's rho computed by hand — there is no SciPy here, and a
hand-rolled rho over five to eight candidates is exact rather than approximate.

The sealed split is not read.
"""

from __future__ import annotations

import argparse
import gzip
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hml_v3.representation_search.corpus import load_corpus  # noqa: E402
from hml_v3.representation_search.compiler import build  # noqa: E402
from hml_v3.representation_search.lineage import CandidateRegistry  # noqa: E402
from hml_v3.representation_search.metrics import MAXIMISED, PARETO_AXES, measure  # noqa: E402
from hml_v3.representation_search.pareto import shortlist  # noqa: E402
from hml_v3.representation_search.sealing import split_corpus  # noqa: E402
from hml_v3.representation_search.seeds import SEEDS  # noqa: E402


def ranking(values: dict[str, float], axis: str) -> list[str]:
    reverse = axis in MAXIMISED
    return sorted(values, key=lambda cid: (-values[cid] if reverse else values[cid], cid))


def spearman(first: list[str], second: list[str]) -> float:
    """Spearman's rho between two orderings of the same items."""

    if len(first) < 2:
        return 1.0
    position = {item: index for index, item in enumerate(second)}
    differences = [(index - position[item]) ** 2 for index, item in enumerate(first)]
    n = len(first)
    return 1.0 - (6.0 * sum(differences)) / (n * (n * n - 1))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path,
                        default=ROOT / "data/corpus/lean_runtime_v2.canonical.jsonl.gz")
    parser.add_argument("--workspace", type=Path, default=ROOT / "data/representation_search")
    parser.add_argument("--sample", type=int, default=40)
    parser.add_argument("--out-dir", type=Path, default=ROOT / "reports/representation_search")
    args = parser.parse_args()

    rows = load_corpus(args.corpus)
    split = split_corpus(rows)
    dev = split.dev[: args.sample]
    validation = split.validation[: args.sample]

    registry = CandidateRegistry(args.workspace / "candidate_registry.jsonl")
    population = [(record.candidate_id, record.metrics or {}) for record in registry.accepted()]
    finalists, reasons = shortlist(population)
    seed_ids = {genome.candidate_id(): name for name, genome in SEEDS.items()}

    dev_values: dict[str, dict[str, float]] = {}
    validation_values: dict[str, dict[str, float]] = {}
    for candidate_id in finalists:
        record = registry.get(candidate_id)
        if record is None:
            continue
        compiler = build(record.genome)
        dev_values[candidate_id] = measure(compiler, dev).values
        validation_values[candidate_id] = measure(compiler, validation).values

    comparison = {}
    for axis in PARETO_AXES:
        dev_axis = {cid: values.get(axis, 0.0) for cid, values in dev_values.items()}
        validation_axis = {cid: values.get(axis, 0.0) for cid, values in validation_values.items()}
        dev_order = ranking(dev_axis, axis)
        validation_order = ranking(validation_axis, axis)
        comparison[axis] = {
            "dev_order": [seed_ids.get(cid, cid) for cid in dev_order],
            "validation_order": [seed_ids.get(cid, cid) for cid in validation_order],
            "same_leader": dev_order[0] == validation_order[0] if dev_order else False,
            "spearman_rho": round(spearman(dev_order, validation_order), 4),
        }

    stable = sum(1 for row in comparison.values() if row["same_leader"])
    payload = {
        "dev_sample": len(dev),
        "validation_sample": len(validation),
        "finalists": [seed_ids.get(cid, cid) for cid in finalists],
        "shortlist_reasons": reasons,
        "per_axis": comparison,
        "axes_with_the_same_leader": stable,
        "axes": len(comparison),
        "note": "SEARCH_VALIDATION was never used for selection. The sealed split is not read here.",
    }
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "FRONTIER_VALIDATION.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n")

    lines = [
        "# Frontier Validation",
        "",
        "Selection read `SEARCH_DEV` every generation. If the finalists' ordering were an "
        "artifact of that sample, it would not survive on `SEARCH_VALIDATION`, which "
        "selection never touched. The sealed split is not read here either.",
        "",
        f"Finalists measured on {len(dev)} dev and {len(validation)} validation transitions.",
        "",
        f"**{stable} of {len(comparison)} axes keep the same leader.**",
        "",
        "| Axis | Dev leader | Validation leader | Same | Spearman rho |",
        "|---|---|---|---|---:|",
    ]
    for axis, row in comparison.items():
        lines.append(
            f"| `{axis}` | `{row['dev_order'][0]}` | `{row['validation_order'][0]}` | "
            f"{'yes' if row['same_leader'] else '**no**'} | {row['spearman_rho']:+.3f} |"
        )
    lines += [
        "",
        "A rho near +1 means the finalists rank the same way on data selection never saw. A "
        "rho near 0 means the axis is measuring the sample. Neither is a statement about a "
        "model: both splits are static measurements of the same static representations.",
    ]
    (args.out_dir / "FRONTIER_VALIDATION.md").write_text("\n".join(lines).rstrip() + "\n")
    print(f"wrote {args.out_dir}/FRONTIER_VALIDATION.md")
    print(f"{stable}/{len(comparison)} axes keep the same leader")


if __name__ == "__main__":
    main()
