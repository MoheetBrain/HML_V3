#!/usr/bin/env python3
"""Phase 6/12: sequential frozen-model probing of every representation.

Zero cost: local ollama only. The ladder and the elimination rule come from
`micromath.sequential` and were fixed before any result was seen.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hml_v3.micromath import neural, sequential  # noqa: E402
from hml_v3.micromath.candidates import load_controls, load_finalists  # noqa: E402
from hml_v3.micromath.corpus import load_split as _load_rows  # noqa: E402
from hml_v3.micromath.schema import MicroPair  # noqa: E402


def load_split(directory: Path, name: str) -> list[MicroPair]:
    return [MicroPair.from_dict(row) for row in _load_rows(directory, name)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lab", type=Path, default=ROOT / "data/micromath_lab_v1")
    parser.add_argument("--split", default="micro_dev")
    parser.add_argument("--workspace", type=Path,
                        default=ROOT / "data/representation_search_v2")
    parser.add_argument("--frontier", type=Path,
                        default=ROOT / "reports/representation_search_v2/FINAL_FRONTIER.json")
    parser.add_argument("--model", default="gemma3:4b")
    parser.add_argument("--out", type=Path, default=ROOT / "reports/micromath_lab_v1")
    parser.add_argument("--only", default="", help="comma-separated labels to probe")
    parser.add_argument("--max-items", type=int, default=0)
    args = parser.parse_args()

    if args.split == "micro_hidden":
        raise SystemExit("REFUSED: MICRO_HIDDEN is not read by the probe loop.")

    pairs = load_split(args.lab, args.split)
    candidates = load_finalists(args.workspace, args.frontier) + load_controls()
    if args.only:
        wanted = {name.strip() for name in args.only.split(",") if name.strip()}
        candidates = [c for c in candidates if c.label in wanted or c.kind == "CONTROL"]

    model = neural.LocalModel(args.model)
    if not model.available():
        raise SystemExit(f"model {args.model} is not installed locally")

    items = {c.label: neural.build_items(c.compiler, pairs) for c in candidates}
    total = min(len(v) for v in items.values())
    if args.max_items:
        total = min(total, args.max_items)
    ladder = sequential.rungs(total)
    print(f"model={args.model} split={args.split} pairs={len(pairs)} items={total} "
          f"ladder={ladder}", flush=True)

    alive = {c.label: c for c in candidates}
    results: dict[str, list] = {}
    history: list[dict] = []
    started = time.time()

    for rung in ladder:
        rung_results: dict[str, list] = {}
        for label, candidate in list(alive.items()):
            probe = neural.run_probe(model, items[label][:rung])
            rung_results[label] = probe
            results[label] = probe
            accuracy = sum(1 for r in probe if r.correct) / max(1, len(probe))
            unparsed = sum(1 for r in probe if r.predicted is None)
            print(f"  rung {rung:>3} {candidate.kind:8s} {label:22s} "
                  f"acc={accuracy:.3f} unparsed={unparsed:>2} "
                  f"{time.time() - started:.0f}s", flush=True)

        controls = {l: r for l, r in rung_results.items() if alive[l].kind == "CONTROL"}
        control_pair_acc = {
            l: neural.per_pair_accuracy(r) for l, r in controls.items()}
        best_control = max(
            control_pair_acc,
            key=lambda l: sum(control_pair_acc[l].values()) / max(1, len(control_pair_acc[l])),
        ) if control_pair_acc else None

        entry = {"rung": rung, "best_control": best_control, "verdicts": {}}
        if best_control:
            reference = control_pair_acc[best_control]
            order = sorted(reference)
            for label, probe in rung_results.items():
                if alive[label].kind == "CONTROL":
                    continue
                mine = neural.per_pair_accuracy(probe)
                verdict = sequential.paired_bootstrap(
                    [mine.get(p, 0.0) for p in order],
                    [reference[p] for p in order], seed=f"{label}|{rung}")
                entry["verdicts"][label] = verdict.to_dict()
                if verdict.dominated and rung != ladder[-1]:
                    print(f"       ELIMINATED {label}: dominated by {best_control} "
                          f"(delta {verdict.difference:+.3f}, "
                          f"CI [{verdict.low:+.3f}, {verdict.high:+.3f}])", flush=True)
                    alive.pop(label, None)
        history.append(entry)

    payload = {
        "model": args.model, "split": args.split, "pairs": len(pairs),
        "ladder": ladder, "history": history,
        "stopping_rule": {
            "ladder": list(sequential.LADDER), "confidence": sequential.CONFIDENCE,
            "resamples": sequential.BOOTSTRAP_RESAMPLES,
            "unit": "MATCHED_PAIR",
            "rule": ("eliminate when the 95% paired bootstrap interval of "
                     "candidate - best_control lies entirely below zero"),
            "preregistered": True,
        },
        "results": {label: [r.to_dict() for r in probe]
                    for label, probe in results.items()},
        "cell_accuracy": {
            label: {f"{d}|{s}": round(v, 4)
                    for (d, s), v in neural.cell_accuracy(probe).items()}
            for label, probe in results.items()},
    }
    args.out.mkdir(parents=True, exist_ok=True)
    name = args.model.replace(":", "_").replace("/", "_")
    (args.out / f"PROBE_{args.split}_{name}.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(f"wrote PROBE_{args.split}_{name}.json in {time.time() - started:.0f}s")


if __name__ == "__main__":
    main()
