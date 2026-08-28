"""Theorem-family partitioning and the sealed evaluator.

Architecture search can overfit its own evaluation set, so the corpus is split at the
**theorem family** level, not the transition level: two transitions from the same theorem
never straddle a boundary, and neither do two theorems from the same Mathlib module.

`SEARCH_DEV` and `SEARCH_VALIDATION` are readable by the controller. `SEALED_FINAL` is not:
:class:`SealedEvaluator` returns aggregate statistics only and refuses to hand back an
individual example. The split is defined by a keyed hash of the family name, so it is
reproducible from the corpus alone and cannot drift with corpus order.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

SPLIT_KEY = "hml-v3-representation-search-split-v1"
DEV, VALIDATION, SEALED = "SEARCH_DEV", "SEARCH_VALIDATION", "SEALED_FINAL_EVALUATION"
TARGET_SHARES = {DEV: 0.70, VALIDATION: 0.10, SEALED: 0.20}


def family_of(transition: dict[str, Any]) -> str:
    """The partition unit: the Mathlib module a theorem lives in.

    Splitting on the theorem name alone would leak: sibling lemmas in one file share
    notation, instances and premise vocabulary, so a candidate tuned on one would be tuned
    on the other.
    """

    metadata = transition.get("corpus_metadata") or {}
    source_file = metadata.get("source_file")
    if source_file:
        return source_file
    return metadata.get("theorem_family") or transition["transition_id"]


def _bucket(family: str) -> float:
    digest = hashlib.sha256(f"{SPLIT_KEY}|{family}".encode()).hexdigest()
    return int(digest[:16], 16) / float(1 << 64)


def assign_split(family: str) -> str:
    position = _bucket(family)
    if position < TARGET_SHARES[DEV]:
        return DEV
    if position < TARGET_SHARES[DEV] + TARGET_SHARES[VALIDATION]:
        return VALIDATION
    return SEALED


@dataclass
class CorpusSplit:
    dev: list[dict[str, Any]]
    validation: list[dict[str, Any]]
    sealed: list[dict[str, Any]]
    families: dict[str, str]

    def manifest(self) -> dict[str, Any]:
        def digest(rows: list[dict[str, Any]]) -> str:
            payload = json.dumps(
                sorted(row["transition_id"] for row in rows), separators=(",", ":"))
            return hashlib.sha256(payload.encode()).hexdigest()

        return {
            "split_key": SPLIT_KEY,
            "unit": "MATHLIB_SOURCE_FILE",
            "target_shares": TARGET_SHARES,
            "counts": {
                DEV: len(self.dev), VALIDATION: len(self.validation), SEALED: len(self.sealed),
            },
            "family_counts": {
                DEV: sum(1 for split in self.families.values() if split == DEV),
                VALIDATION: sum(1 for split in self.families.values() if split == VALIDATION),
                SEALED: sum(1 for split in self.families.values() if split == SEALED),
            },
            "transition_id_sha256": {
                DEV: digest(self.dev),
                VALIDATION: digest(self.validation),
                SEALED: digest(self.sealed),
            },
            "families_sha256": hashlib.sha256(
                json.dumps(self.families, sort_keys=True, separators=(",", ":")).encode()
            ).hexdigest(),
        }


def split_corpus(transitions: Iterable[dict[str, Any]]) -> CorpusSplit:
    dev: list[dict[str, Any]] = []
    validation: list[dict[str, Any]] = []
    sealed: list[dict[str, Any]] = []
    families: dict[str, str] = {}
    for transition in transitions:
        family = family_of(transition)
        split = families.setdefault(family, assign_split(family))
        {DEV: dev, VALIDATION: validation, SEALED: sealed}[split].append(transition)
    for bucket in (dev, validation, sealed):
        bucket.sort(key=lambda row: row["transition_id"])
    return CorpusSplit(dev, validation, sealed, families)


class SealedEvaluator:
    """Aggregate-only access to the sealed split.

    The controller may call :meth:`evaluate`; it may not read the transitions. Each call is
    logged so the number of times the sealed split was touched is auditable, and the
    controller is expected to touch it once, at the end.
    """

    def __init__(self, transitions: list[dict[str, Any]], log_path: Path | None = None) -> None:
        self._transitions = transitions
        self._log_path = log_path
        self.access_log: list[dict[str, Any]] = []

    @property
    def size(self) -> int:
        return len(self._transitions)

    def evaluate(self, compiler, purpose: str, sample: int = 96) -> dict[str, Any]:
        from hml_v3.representation_search.gates import run_gates
        from hml_v3.representation_search.metrics import PARETO_AXES, measure

        subset = self._transitions[:sample]
        report = run_gates(compiler, subset)
        result: dict[str, Any] = {
            "candidate_id": compiler.candidate_id,
            "purpose": purpose,
            "sealed_sample_size": len(subset),
            "gates_passed": report.passed,
            "first_gate_failure": report.first_failure,
        }
        if report.passed:
            vector = measure(compiler, subset)
            result["pareto_axes"] = {
                axis: round(vector.values.get(axis, 0.0), 6) for axis in PARETO_AXES
            }
        self.access_log.append({
            "candidate_id": compiler.candidate_id, "purpose": purpose,
            "sample": len(subset),
        })
        if self._log_path is not None:
            self._log_path.parent.mkdir(parents=True, exist_ok=True)
            with self._log_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(self.access_log[-1], sort_keys=True) + "\n")
        return result
