"""The sealed evaluator as a separate process.

V1's sealed evaluator was logically separated but loaded the sealed rows into the same
Python process as the search. Separation by discipline is weaker than separation by
construction: any future controller change, or any debugging session, could read them.

Here the sealed split lives in its own file, is loaded only by a child process, and the
parent receives JSON containing aggregate metrics and nothing else. The search process never
holds a sealed transition in memory, so it cannot leak one even by accident.

Access is append-only logged with a monotonic counter, and the log is written by the *child*
before it answers — a parent that crashes mid-call still leaves the access recorded.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
SERVICE_VERSION = "sealed-service-v1.0.0"

#: Keys the child is permitted to return. Anything else is dropped by the parent.
ALLOWED_KEYS = frozenset({
    "candidate_id", "purpose", "sample_size", "gates_passed", "first_gate_failure",
    "pareto_axes", "microtests", "service_version", "corpus_sha256", "access_index",
})


def _child_main() -> int:
    """Runs in the isolated process. This is the only code that reads sealed rows."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--sealed", type=Path, required=True)
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--log", type=Path, required=True)
    arguments = parser.parse_args()

    sys.path.insert(0, str(ROOT / "src"))
    from hml_v3.representation_search.compiler import build
    from hml_v3.representation_search.corpus import load_corpus
    from hml_v3.representation_search.gates import run_gates
    from hml_v3.representation_search.genome import RepresentationGenome
    from hml_v3.representation_search.metrics import PARETO_AXES, measure
    from hml_v3.representation_search.microtests import run_all_suites

    request = json.loads(arguments.request.read_text())
    rows = load_corpus(arguments.sealed)
    subset = rows[: request.get("sample", 96)]
    digest = hashlib.sha256(
        json.dumps(sorted(row["transition_id"] for row in rows), separators=(",", ":")).encode()
    ).hexdigest()

    arguments.log.parent.mkdir(parents=True, exist_ok=True)
    existing = (
        sum(1 for line in arguments.log.read_text(encoding="utf-8").splitlines() if line.strip())
        if arguments.log.exists() else 0
    )

    results: list[dict[str, Any]] = []
    for index, entry in enumerate(request["candidates"]):
        genome = RepresentationGenome.from_dict(entry["genome"])
        compiler = build(genome)
        report = run_gates(compiler, subset)
        row: dict[str, Any] = {
            "candidate_id": entry.get("candidate_id") or compiler.candidate_id,
            "purpose": request.get("purpose", "unspecified"),
            "sample_size": len(subset),
            "gates_passed": report.passed,
            "first_gate_failure": report.first_failure,
            "service_version": SERVICE_VERSION,
            "corpus_sha256": digest,
            "access_index": existing + index + 1,
        }
        if report.passed:
            vector = measure(compiler, subset)
            row["pareto_axes"] = {
                axis: round(vector.values.get(axis, 0.0), 6) for axis in PARETO_AXES
            }
            if request.get("microtests"):
                row["microtests"] = {
                    name: result.metrics()
                    for name, result in run_all_suites(compiler, subset, max_queries=120).items()
                }
        results.append({key: value for key, value in row.items() if key in ALLOWED_KEYS})

    # Log before answering: an access that happened is recorded even if the parent dies.
    with arguments.log.open("a", encoding="utf-8") as handle:
        for row in results:
            handle.write(json.dumps({
                "candidate_id": row["candidate_id"], "purpose": row["purpose"],
                "sample_size": row["sample_size"], "access_index": row["access_index"],
                "corpus_sha256": row["corpus_sha256"],
            }, sort_keys=True) + "\n")

    print(json.dumps({"results": results, "sealed_transitions": len(rows)}))
    return 0


class SealedEvaluatorClient:
    """The parent side. Holds a path, never a sealed row."""

    def __init__(self, sealed_path: Path, log_path: Path, timeout: int = 1800) -> None:
        self.sealed_path = sealed_path
        self.log_path = log_path
        self.timeout = timeout

    def available(self) -> bool:
        from hml_v3.representation_search.corpus import shard_paths

        return bool(shard_paths(self.sealed_path))

    def evaluate(
        self, candidates: list[dict[str, Any]], purpose: str,
        sample: int = 96, microtests: bool = True, workspace: Path | None = None,
    ) -> dict[str, Any]:
        """Ask the isolated process for aggregates. Returns only what it is allowed to return."""

        workspace = workspace or self.log_path.parent
        workspace.mkdir(parents=True, exist_ok=True)
        request_path = workspace / "sealed_request.json"
        request_path.write_text(json.dumps({
            "candidates": candidates, "purpose": purpose,
            "sample": sample, "microtests": microtests,
        }, sort_keys=True))

        process = subprocess.run(
            [sys.executable, str(Path(__file__).resolve()),
             "--sealed", str(self.sealed_path),
             "--request", str(request_path),
             "--log", str(self.log_path)],
            capture_output=True, text=True, timeout=self.timeout, check=False,
        )
        if process.returncode != 0:
            raise RuntimeError(
                f"sealed evaluator process failed ({process.returncode}): "
                f"{process.stderr[-600:]}"
            )
        payload = json.loads(process.stdout)
        # Defence in depth: strip anything the child was not supposed to send.
        payload["results"] = [
            {key: value for key, value in row.items() if key in ALLOWED_KEYS}
            for row in payload.get("results", [])
        ]
        payload["isolation"] = "SEPARATE_PROCESS"
        payload["service_version"] = SERVICE_VERSION
        return payload

    def access_count(self) -> int:
        if not self.log_path.exists():
            return 0
        return sum(1 for line in self.log_path.read_text(encoding="utf-8").splitlines() if line.strip())


if __name__ == "__main__":
    raise SystemExit(_child_main())
