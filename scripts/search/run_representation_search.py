#!/usr/bin/env python3
"""Run the recursive representation architecture search.

    python3 scripts/search/run_representation_search.py --generations 10

The run is resumable: state lives in ``data/representation_search/``, and re-invoking the
script continues from the exact next generation. The sealed split is never read during the
search; ``--seal-final`` performs the single end-of-search sealed evaluation.
"""

from __future__ import annotations

import argparse
import gzip
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hml_v3.representation_search.corpus import load_corpus  # noqa: E402
from hml_v3.representation_search.compiler import build  # noqa: E402
from hml_v3.representation_search.controller import SearchConfig, SearchController  # noqa: E402
from hml_v3.representation_search.failure_memory import FailureMemory  # noqa: E402
from hml_v3.representation_search.pareto import shortlist  # noqa: E402
from hml_v3.representation_search.sealing import SealedEvaluator, split_corpus  # noqa: E402

DEFAULT_CORPUS = ROOT / "data/corpus/lean_runtime_v2.canonical.jsonl.gz"
DEFAULT_WORKSPACE = ROOT / "data/representation_search"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument("--workspace", type=Path, default=DEFAULT_WORKSPACE)
    parser.add_argument("--generations", type=int, default=5)
    parser.add_argument("--population", type=int, default=24)
    parser.add_argument("--children", type=int, default=16)
    parser.add_argument("--dev-sample", type=int, default=48)
    parser.add_argument("--validation-sample", type=int, default=32)
    parser.add_argument("--max-generations", type=int, default=40)
    parser.add_argument("--stall-limit", type=int, default=5)
    parser.add_argument("--fresh", action="store_true", help="ignore any saved state")
    parser.add_argument("--seal-final", action="store_true",
                        help="run the single sealed evaluation of the current Pareto front")
    args = parser.parse_args()

    corpus = load_corpus(args.corpus)
    split = split_corpus(corpus)
    args.workspace.mkdir(parents=True, exist_ok=True)
    manifest_path = args.workspace / "split_manifest.json"
    manifest = split.manifest()
    if manifest_path.exists():
        previous = json.loads(manifest_path.read_text())
        if previous["families_sha256"] != manifest["families_sha256"]:
            if not args.fresh:
                raise SystemExit(
                    "SPLIT_DRIFT: the corpus changed after the split was fixed. Refusing to "
                    "continue a search whose dev/sealed boundary has moved. Re-run with "
                    "--fresh to archive this search and start a new one on the new corpus."
                )
            # A new corpus is a new experiment. The previous search is archived rather than
            # overwritten: its registry, checkpoints and split manifest are the evidence that
            # a result was produced under a different corpus.
            archive = args.workspace / "archive" / previous["families_sha256"][:12]
            archive.mkdir(parents=True, exist_ok=True)
            for name in ("split_manifest.json", "search_state.json",
                         "candidate_registry.jsonl", "sealed_access_log.jsonl",
                         "sealed_final_evaluation.json"):
                source = args.workspace / name
                if source.exists():
                    source.replace(archive / name)
            generations = args.workspace / "generations"
            if generations.exists():
                generations.replace(archive / "generations")
            print(f"archived the previous search to {archive}")
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

    config = SearchConfig(
        population_capacity=args.population,
        children_per_generation=args.children,
        dev_sample=args.dev_sample,
        validation_sample=args.validation_sample,
        max_generations=args.max_generations,
        stall_limit=args.stall_limit,
    )
    controller = SearchController(
        split.dev, split.validation, args.workspace, config, FailureMemory.load(),
    )
    resumed = False if args.fresh else controller.resume()
    print(json.dumps({
        "corpus_transitions": len(corpus),
        "dev": len(split.dev), "validation": len(split.validation),
        "sealed": len(split.sealed),
        "resumed": resumed, "starting_generation": controller.generation,
    }, indent=2))

    started = time.time()
    for _ in range(args.generations):
        done, reason = controller.converged()
        if done:
            print(f"STOP: {reason}")
            break
        report = controller.step()
        print(
            f"gen {report.generation:>3} phase={report.phase} "
            f"evaluated={len(report.evaluated):>3} rejected={len(report.hard_rejected):>3} "
            f"front={len(report.front):>2} moved={report.frontier_moved} "
            f"blocked={len(report.blocked_by_memory):>2} "
            f"refuted={len(report.refuted_hypotheses):>2} "
            f"{report.elapsed_seconds:.1f}s"
        )
    print(f"total {time.time() - started:.1f}s; registry {len(controller.registry)} candidates")
    print(json.dumps(controller.registry.statistics(), indent=2))

    if args.seal_final:
        evaluator = SealedEvaluator(split.sealed, args.workspace / "sealed_access_log.jsonl")
        front = controller.history[-1] if controller.history else {}
        # Seal only the reported finalists. The strict front can hold most of a grown
        # population, and every extra sealed evaluation is another read of a split that is
        # supposed to be touched once.
        population = [
            (record.candidate_id, record.metrics or {})
            for record in controller.registry.accepted()
        ]
        front_ids, shortlist_reasons = shortlist(population)
        results = []
        for candidate_id in front_ids:
            record = controller.registry.get(candidate_id)
            if record is None:
                continue
            results.append(evaluator.evaluate(
                build(record.genome), purpose="PRETRAINING_FRONTIER_V1_FINAL"))
        output = args.workspace / "sealed_final_evaluation.json"
        output.write_text(json.dumps({
            "sealed_transitions": evaluator.size,
            "front_size": len(front_ids),
            "shortlist_reasons": shortlist_reasons,
            "results": results,
            "generation_history_tail": front,
        }, indent=2, sort_keys=True) + "\n")
        print(f"sealed evaluation written to {output}")


if __name__ == "__main__":
    main()
