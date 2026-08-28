#!/usr/bin/env python3
"""Where does each finalist actually do well?

A single frontier table hides the question a user of the language will ask first: does the
candidate that wins on average also win on the states I care about? This measures every
finalist on each Mathlib domain separately and reports, per domain, which finalist leads on
each Pareto axis.

It reads the dev and validation splits only. The sealed split is never touched.
"""

from __future__ import annotations

import argparse
import collections
import gzip
import json
from pathlib import Path
import statistics
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path,
                        default=ROOT / "data/corpus/lean_runtime_v2.canonical.jsonl.gz")
    parser.add_argument("--workspace", type=Path, default=ROOT / "data/representation_search")
    parser.add_argument("--out-dir", type=Path, default=ROOT / "reports/representation_search")
    parser.add_argument("--min-domain-size", type=int, default=8)
    parser.add_argument("--per-domain-sample", type=int, default=16)
    args = parser.parse_args()

    corpus = load_corpus(args.corpus)
    split = split_corpus(corpus)
    visible = split.dev + split.validation

    by_domain: dict[str, list[dict]] = collections.defaultdict(list)
    for row in visible:
        by_domain[(row.get("corpus_metadata") or {}).get("domain", "unknown")].append(row)
    domains = {
        name: rows[: args.per_domain_sample]
        for name, rows in sorted(by_domain.items())
        if len(rows) >= args.min_domain_size
    }

    registry = CandidateRegistry(args.workspace / "candidate_registry.jsonl")
    population = [(record.candidate_id, record.metrics or {}) for record in registry.accepted()]
    finalists, reasons = shortlist(population)
    seed_ids = {genome.candidate_id(): name for name, genome in SEEDS.items()}

    results: dict[str, dict[str, dict[str, float]]] = {}
    for candidate_id in finalists:
        record = registry.get(candidate_id)
        if record is None:
            continue
        compiler = build(record.genome)
        results[candidate_id] = {}
        for domain, rows in domains.items():
            vector = measure(compiler, rows)
            results[candidate_id][domain] = {
                axis: round(vector.values.get(axis, 0.0), 4) for axis in PARETO_AXES
            }

    leaders: dict[str, dict[str, str]] = {}
    for domain in domains:
        leaders[domain] = {}
        for axis in PARETO_AXES:
            ranked = sorted(
                results,
                key=lambda cid: (
                    -results[cid][domain][axis] if axis in MAXIMISED
                    else results[cid][domain][axis],
                    cid,
                ),
            )
            leaders[domain][axis] = ranked[0] if ranked else ""

    wins: dict[str, collections.Counter] = {
        candidate_id: collections.Counter() for candidate_id in results
    }
    for domain, per_axis in leaders.items():
        for axis, candidate_id in per_axis.items():
            if candidate_id:
                wins[candidate_id][domain] += 1

    payload = {
        "corpus": str(args.corpus),
        "domains_measured": {name: len(rows) for name, rows in domains.items()},
        "min_domain_size": args.min_domain_size,
        "per_domain_sample": args.per_domain_sample,
        "finalists": finalists,
        "shortlist_reasons": reasons,
        "per_candidate": results,
        "axis_leaders_by_domain": leaders,
        "domain_wins": {cid: dict(counter) for cid, counter in wins.items()},
        "note": "Dev and validation splits only. The sealed split is never read here.",
    }
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "FINALIST_DOMAIN_PROFILES.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")

    lines = [
        "# Finalist Domain Profiles",
        "",
        "A frontier table reports averages. This asks the question a user of the language "
        "asks first: **does the candidate that wins on average also win on the mathematics I "
        "work in?** Each finalist is measured on each Mathlib domain separately.",
        "",
        f"Domains with at least {args.min_domain_size} transitions in the dev and validation "
        f"splits, sampled to {args.per_domain_sample} transitions each. The sealed split is "
        "not read.",
        "",
        "| Domain | Transitions available |",
        "|---|---:|",
    ]
    for name, count in sorted(payload["domains_measured"].items(),
                              key=lambda item: (-item[1], item[0])):
        lines.append(f"| `{name}` | {count} |")

    lines += ["", "## Where each finalist leads", "",
              "Number of Pareto axes on which the finalist is the best of the finalists, "
              "per domain. Seven axes, so seven is a clean sweep.",
              "", "| Finalist | Shortlisted because | Domains led | Best domains |",
              "|---|---|---:|---|"]
    for candidate_id in finalists:
        counter = wins.get(candidate_id, collections.Counter())
        total = sum(counter.values())
        top = ", ".join(
            f"`{domain}` ({count}/7)" for domain, count in counter.most_common(3)
        ) or "none"
        label = seed_ids.get(candidate_id, candidate_id)
        lines.append(
            f"| `{label}` | {', '.join(reasons.get(candidate_id, []))} | {total} | {top} |"
        )

    lines += ["", "## Per-domain axis leaders", "",
              "| Domain | " + " | ".join(f"`{axis}`" for axis in PARETO_AXES) + " |",
              "|---" * (len(PARETO_AXES) + 1) + "|"]
    for domain in sorted(leaders):
        cells = " | ".join(
            f"`{seed_ids.get(leaders[domain][axis], leaders[domain][axis])}`"
            for axis in PARETO_AXES
        )
        lines.append(f"| `{domain}` | {cells} |")

    stability = {}
    for axis in PARETO_AXES:
        winners = collections.Counter(leaders[domain][axis] for domain in leaders)
        modal, count = winners.most_common(1)[0] if winners else ("", 0)
        stability[axis] = {
            "modal_leader": modal,
            "domains_led": count,
            "domains": len(leaders),
            "share": round(count / max(1, len(leaders)), 3),
        }
    payload["axis_stability"] = stability
    lines += ["", "## Is the ranking a property of the representation or of the mathematics?",
              "",
              "For each axis: the finalist that leads in the most domains, and in how many. "
              "A high share means the ranking on that axis is a property of the "
              "representation; a low share means the axis is measuring the mathematics as "
              "much as the encoding.",
              "", "| Axis | Modal leader | Domains led | Share |", "|---|---|---:|---:|"]
    for axis, row in stability.items():
        lines.append(
            f"| `{axis}` | `{seed_ids.get(row['modal_leader'], row['modal_leader'])}` | "
            f"{row['domains_led']}/{row['domains']} | {row['share']:.0%} |"
        )

    spreads = []
    for axis in PARETO_AXES:
        per_domain_best = []
        for domain in domains:
            values = [results[cid][domain][axis] for cid in results]
            if values:
                per_domain_best.append(min(values) if axis not in MAXIMISED else max(values))
        if len(per_domain_best) > 1:
            spreads.append((axis, min(per_domain_best), max(per_domain_best),
                            statistics.pstdev(per_domain_best)))
    lines += ["", "## How much the domain changes the answer", "",
              "The best achievable value on each axis, across domains. A wide range means the "
              "axis is measuring the mathematics as much as the representation.",
              "", "| Axis | Best domain value | Worst domain value | SD across domains |",
              "|---|---:|---:|---:|"]
    for axis, low, high, sd in spreads:
        lines.append(f"| `{axis}` | {low:,.3f} | {high:,.3f} | {sd:,.3f} |")

    (args.out_dir / "FINALIST_DOMAIN_PROFILES.md").write_text("\n".join(lines).rstrip() + "\n")
    print(f"wrote {args.out_dir}/FINALIST_DOMAIN_PROFILES.md")
    print(f"{len(finalists)} finalists over {len(domains)} domains")


if __name__ == "__main__":
    main()
