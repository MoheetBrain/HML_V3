#!/usr/bin/env python3
"""Run the open-ended representation search.

    python3 scripts/search/run_open_ended_search.py --generations 12

Resumable: state lives in ``data/representation_search_v2/`` and re-invoking continues from
the exact next generation, including the genome schema version if the search grew its own
space. The sealed split is never read here.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hml_v3.representation_search.controller_v2 import (  # noqa: E402
    OpenEndedController,
    SearchConfigV2,
)
from hml_v3.representation_search.corpus import load_corpus  # noqa: E402
from hml_v3.representation_search.failure_memory import FailureMemory  # noqa: E402
from hml_v3.representation_search.meta_designer.deterministic import (  # noqa: E402
    DeterministicMetaDesigner,
)
from hml_v3.representation_search.meta_designer.llm import (  # noqa: E402
    LLMMetaDesigner,
    OllamaTransport,
)
from hml_v3.representation_search.sealing import split_corpus  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path,
                        default=ROOT / "data/corpus/lean_runtime_v2.canonical.jsonl.gz")
    parser.add_argument("--workspace", type=Path,
                        default=ROOT / "data/representation_search_v2")
    parser.add_argument("--generations", type=int, default=12)
    parser.add_argument("--population", type=int, default=24)
    parser.add_argument("--children", type=int, default=18)
    parser.add_argument("--dev-sample", type=int, default=28)
    parser.add_argument("--validation-sample", type=int, default=20)
    parser.add_argument("--microtest-sample", type=int, default=14)
    parser.add_argument("--mutation-sample", type=int, default=12)
    parser.add_argument("--max-generations", type=int, default=40)
    parser.add_argument("--stall-limit", type=int, default=5)
    parser.add_argument("--llm-model", default="gemma3:4b")
    parser.add_argument("--no-llm", action="store_true")
    parser.add_argument("--fresh", action="store_true")
    args = parser.parse_args()

    corpus = load_corpus(args.corpus)
    split = split_corpus(corpus)
    args.workspace.mkdir(parents=True, exist_ok=True)

    manifest_path = args.workspace / "split_manifest.json"
    manifest = split.manifest()
    if manifest_path.exists() and not args.fresh:
        previous = json.loads(manifest_path.read_text())
        if previous["families_sha256"] != manifest["families_sha256"]:
            raise SystemExit(
                "SPLIT_DRIFT: the corpus changed after the split was fixed. Re-run with "
                "--fresh to archive this search and start a new one on the new corpus."
            )
    if args.fresh and manifest_path.exists():
        previous = json.loads(manifest_path.read_text())
        archive = args.workspace / "archive" / previous["families_sha256"][:12]
        archive.mkdir(parents=True, exist_ok=True)
        for name in ("split_manifest.json", "search_state.json", "candidate_registry.jsonl",
                     "primitive_registry.jsonl", "proposal_history.jsonl"):
            source = args.workspace / name
            if source.exists():
                source.replace(archive / name)
        generations = args.workspace / "generations"
        if generations.exists():
            generations.replace(archive / "generations")
        print(f"archived the previous search to {archive}")
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

    backends = [DeterministicMetaDesigner()]
    if not args.no_llm:
        transport = OllamaTransport(args.llm_model)
        backend = LLMMetaDesigner(transport)
        if backend.available():
            backends.append(backend)
            print(f"model-driven meta-designer active: {backend.name}")
        else:
            print(f"model-driven meta-designer UNAVAILABLE ({args.llm_model}); "
                  "running rule-based only")

    config = SearchConfigV2(
        population_capacity=args.population, children_per_generation=args.children,
        dev_sample=args.dev_sample, validation_sample=args.validation_sample,
        microtest_sample=args.microtest_sample, mutation_sample=args.mutation_sample,
        max_generations=args.max_generations, stall_limit=args.stall_limit,
    )
    controller = OpenEndedController(
        split.dev, split.validation, args.workspace, backends, config, FailureMemory.load())
    resumed = False if args.fresh else controller.resume()
    print(json.dumps({
        "corpus_transitions": len(corpus),
        "dev": len(split.dev), "validation": len(split.validation),
        "sealed_not_read": len(split.sealed),
        "resumed": resumed, "starting_generation": controller.generation,
        "genome_schema": controller.primitives.schema_version,
        "backends": [backend.name for backend in backends],
    }, indent=2))

    started = time.time()
    for _ in range(args.generations):
        done, reason = controller.converged()
        if done:
            print(f"STOP: {reason}")
            break
        report = controller.step()
        proposals = report.proposals
        print(
            f"gen {report.generation:>3} eval={len(report.evaluated):>3} "
            f"killed={len(report.killed):>2} front={len(report.front):>2} "
            f"moved={report.frontier_moved} newaxes={report.new_axes} "
            f"proposals={proposals['accepted']}/{proposals['accepted'] + proposals['rejected']} "
            f"quarantined={sum(1 for v in report.validation_verdicts if not v['elite_eligible'])} "
            f"schema={report.genome_schema} {report.elapsed_seconds:.0f}s",
            flush=True,
        )
    print(f"total {time.time() - started:.0f}s")
    print(json.dumps(controller.registry.statistics(), indent=2))
    print(json.dumps(controller.primitives.statistics(), indent=2))
    finalists, reasons = controller.finalists()
    print(json.dumps({"finalists": finalists, "reasons": reasons}, indent=2))


if __name__ == "__main__":
    main()
