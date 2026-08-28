"""Candidate registry and lineage.

Every candidate ever compiled is recorded once, with its genome, its parents, the mutation
that produced it, the hypothesis behind that mutation, and its outcome. Rejections are
first-class records: a candidate that failed a hard gate is evidence, not waste.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any, Iterator

from hml_v3.representation_search.genome import RepresentationGenome


@dataclass
class CandidateRecord:
    candidate_id: str
    genome: RepresentationGenome
    generation: int
    origin: str
    parents: tuple[str, ...] = ()
    mutation: dict[str, Any] | None = None
    hypothesis: dict[str, Any] | None = None
    status: str = "PENDING"
    rejection_reason: str | None = None
    gates: dict[str, Any] | None = None
    metrics: dict[str, float] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "generation": self.generation,
            "origin": self.origin,
            "parents": list(self.parents),
            "mutation": self.mutation,
            "hypothesis": self.hypothesis,
            "status": self.status,
            "rejection_reason": self.rejection_reason,
            "gates": self.gates,
            "metrics": self.metrics,
            "genome": self.genome.to_dict(),
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "CandidateRecord":
        return cls(
            candidate_id=value["candidate_id"],
            genome=RepresentationGenome.from_dict(value["genome"]),
            generation=value["generation"],
            origin=value["origin"],
            parents=tuple(value.get("parents", ())),
            mutation=value.get("mutation"),
            hypothesis=value.get("hypothesis"),
            status=value.get("status", "PENDING"),
            rejection_reason=value.get("rejection_reason"),
            gates=value.get("gates"),
            metrics=value.get("metrics"),
        )


class CandidateRegistry:
    """Append-only JSONL registry with an in-memory index."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.records: dict[str, CandidateRecord] = {}
        if path.exists():
            for line in path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    record = CandidateRecord.from_dict(json.loads(line))
                    self.records[record.candidate_id] = record

    def __contains__(self, candidate_id: str) -> bool:
        return candidate_id in self.records

    def __iter__(self) -> Iterator[CandidateRecord]:
        return iter(self.records.values())

    def __len__(self) -> int:
        return len(self.records)

    def get(self, candidate_id: str) -> CandidateRecord | None:
        return self.records.get(candidate_id)

    def add(self, record: CandidateRecord) -> CandidateRecord:
        existing = self.records.get(record.candidate_id)
        if existing is not None:
            return existing
        self.records[record.candidate_id] = record
        return record

    def update(self, record: CandidateRecord) -> None:
        self.records[record.candidate_id] = record

    def flush(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            json.dumps(record.to_dict(), ensure_ascii=False, sort_keys=True,
                       separators=(",", ":"))
            for record in sorted(self.records.values(),
                                 key=lambda item: (item.generation, item.candidate_id))
        ]
        self.path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # -------------------------------------------------------------------------- lineage
    def ancestry(self, candidate_id: str) -> list[str]:
        chain: list[str] = []
        seen: set[str] = set()
        frontier = [candidate_id]
        while frontier:
            current = frontier.pop(0)
            if current in seen:
                continue
            seen.add(current)
            chain.append(current)
            record = self.records.get(current)
            if record:
                frontier.extend(record.parents)
        return chain

    def accepted(self) -> list[CandidateRecord]:
        return [record for record in self.records.values() if record.status == "EVALUATED"]

    def rejected(self) -> list[CandidateRecord]:
        return [record for record in self.records.values() if record.status == "HARD_REJECTED"]

    def statistics(self) -> dict[str, Any]:
        by_status: dict[str, int] = {}
        by_reason: dict[str, int] = {}
        for record in self.records.values():
            by_status[record.status] = by_status.get(record.status, 0) + 1
            if record.rejection_reason:
                by_reason[record.rejection_reason] = by_reason.get(record.rejection_reason, 0) + 1
        return {
            "total": len(self.records),
            "by_status": dict(sorted(by_status.items())),
            "by_rejection_reason": dict(sorted(by_reason.items())),
        }
