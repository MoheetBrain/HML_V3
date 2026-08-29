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
from hml_v3.representation_search.sealing import split_search_pool  # noqa: E402

#: Any corpus whose path matches one of these is the sealed split. The search process must
#: never open it -- not to count it, not to hash it, not to sanity-check it. The guard is a
#: path check rather than a convention because SEALED_FINAL_V2's whole value is that it has
#: been read zero times, and a single accidental read is not recoverable.
SEALED_PATH_MARKERS = ("sealed_final", "sealed_v2", "SEALED")


def refuse_sealed(path: Path) -> None:
    resolved = str(path.resolve())
    for marker in SEALED_PATH_MARKERS:
        if marker in resolved:
            raise SystemExit(
                f"REFUSED: {resolved} looks like a sealed split (matched {marker!r}). The "
                "search process never reads the seal; it is read once, after convergence, on "
                "the reported finalists only, through the isolated sealed evaluator."
            )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path,
                        default=ROOT / "data/corpus/search_pool_v2.jsonl.gz",
                        help="the search pool, with SEALED_FINAL_V2 already removed")
    parser.add_argument("--workspace", type=Path,
                        default=ROOT / "data/representation_search_v2")
    parser.add_argument(
        "--generations", type=int, default=None,
        help="stop after this many generations regardless of convergence; omit to run until "
             "the search structurally converges")
    parser.add_argument("--population", type=int, default=24)
    parser.add_argument("--children", type=int, default=18)
    parser.add_argument("--dev-sample", type=int, default=28)
    parser.add_argument("--validation-sample", type=int, default=20)
    parser.add_argument("--microtest-sample", type=int, default=14)
    parser.add_argument("--mutation-sample", type=int, default=12)
    parser.add_argument("--max-generations", type=int, default=40)
    parser.add_argument("--stall-limit", type=int, default=5)
    parser.add_argument(
        "--llm-models", default="gemma3:4b,qwen38-rvn:latest",
        help="comma-separated locally served models, one meta-designer backend each; "
             "every one that is not installed is reported and skipped")
    parser.add_argument("--llm-model", default=None,
                        help="deprecated alias for a single --llm-models entry")
    parser.add_argument("--no-llm", action="store_true")
    parser.add_argument("--fresh", action="store_true")
    args = parser.parse_args()

    refuse_sealed(args.corpus)
    corpus = load_corpus(args.corpus)
    # The pool's seal is already a separate file, so this splits dev/validation only. Running
    # the three-way split here would withhold a fifth of the pool for a second seal nothing
    # reads -- and that fifth is the multi-goal structure acquired to make goal ordering
    # measurable in the first place.
    split = split_search_pool(corpus)
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
    unavailable: list[str] = []
    if not args.no_llm:
        requested = [args.llm_model] if args.llm_model else [
            name.strip() for name in args.llm_models.split(",") if name.strip()
        ]
        # Several independent local proposers, not one. A single model's blind spots become
        # the search's blind spots; two families disagreeing is the cheapest available
        # diversity, and neither costs anything beyond local inference.
        for model in requested:
            backend = LLMMetaDesigner(OllamaTransport(model))
            if backend.available():
                backends.append(backend)
                print(f"model-driven meta-designer active: {backend.name}")
            else:
                unavailable.append(model)
                print(f"model-driven meta-designer UNAVAILABLE ({model}); skipped")
    if len(backends) == 1:
        print("no model-driven proposer is available; running rule-based only")

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
        "corpus": str(args.corpus),
        "corpus_transitions": len(corpus),
        "dev": len(split.dev), "validation": len(split.validation),
        "sealed_in_this_file": len(split.sealed),
        "sealed_final_v2": "NOT OPENED BY THIS PROCESS",
        "resumed": resumed, "starting_generation": controller.generation,
        "genome_schema": controller.primitives.schema_version,
        "backends": [backend.name for backend in backends],
        "llm_backends_unavailable": unavailable,
    }, indent=2))

    started = time.time()
    budget = args.generations if args.generations is not None else args.max_generations + 1
    stop_reason = "GENERATIONS_ARGUMENT_EXHAUSTED"
    for _ in range(budget):
        done, reason = controller.converged()
        if done:
            stop_reason = reason
            print(f"STOP: {reason}", flush=True)
            break
        report = controller.step()
        proposals = report.proposals
        print(
            f"gen {report.generation:>3} eval={len(report.evaluated):>3} "
            f"killed={len(report.killed):>2} front={len(report.front):>2} "
            f"moved={report.frontier_moved} newaxes={report.new_axes} "
            f"proposals={proposals['accepted']}/{proposals['accepted'] + proposals['rejected']} "
            f"quarantined={sum(1 for v in report.validation_verdicts if not v['elite_eligible'])} "
            f"stall={controller.structural_stall}/{controller.config.stall_limit} "
            f"schema={report.genome_schema} {report.elapsed_seconds:.0f}s",
            flush=True,
        )
        for demotion in report.axis_demotions:
            print(f"     AXIS {demotion['action']}: {demotion['axis']} -- "
                  f"{demotion['reason']}", flush=True)
    print(f"total {time.time() - started:.0f}s")
    print("STOP_REASON:", stop_reason)
    print(json.dumps(controller.convergence_state(), indent=2))
    print(json.dumps(controller.registry.statistics(), indent=2))
    print(json.dumps(controller.primitives.statistics(), indent=2))
    finalists, reasons = controller.finalists()
    print(json.dumps({"finalists": finalists, "reasons": reasons}, indent=2))


if __name__ == "__main__":
    main()
