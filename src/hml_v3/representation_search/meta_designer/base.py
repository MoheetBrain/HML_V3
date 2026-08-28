"""The meta-designer interface: what a scientist in this loop is allowed to see and say.

The V1 controller called `targeted_proposals`, `local_neighbourhood` and `random_walk`
directly, against a hard-coded `AXIS_MECHANISM` table. That made the search a *recombination*
engine: it could only reach points already spanned by the 42 axes. If the best representation
needed an idea absent from the genome, the search had zero probability of finding it.

This interface breaks that ceiling. A backend receives a compact report of what the search
has measured and returns typed proposals — including proposals to add axes the genome does
not have, and to acquire data or build instruments the search is missing. The backend cannot
edit files, cannot see the sealed split, and cannot touch the canonical layer; everything it
can ask for goes through `schemas.validate`.
"""

from __future__ import annotations

import abc
from dataclasses import dataclass, field
import json
from typing import Any

from hml_v3.representation_search.meta_designer.schemas import (
    ProposalRejected,
    ValidatedProposal,
    static_safety,
    validate,
)


@dataclass
class ScientistReport:
    """What the meta-designer is told. Compact by design — never the whole repository.

    Everything here is aggregate or genome-level. No sealed transition, no raw corpus row,
    and no canonical state ever appears in a report.
    """

    generation: int
    phase: str | None
    genome_axes: dict[str, list[str]]
    elites: list[dict[str, Any]]
    metric_directions: dict[str, str]
    validation_divergence: list[dict[str, Any]] = field(default_factory=list)
    microtest_failures: list[dict[str, Any]] = field(default_factory=list)
    neural_failures: list[dict[str, Any]] = field(default_factory=list)
    failure_memory: list[dict[str, Any]] = field(default_factory=list)
    corpus_profile: dict[str, Any] = field(default_factory=dict)
    unmeasurable_axes: list[str] = field(default_factory=list)
    unresolved_questions: list[str] = field(default_factory=list)
    lineage_summary: dict[str, Any] = field(default_factory=dict)
    budget: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "generation": self.generation,
            "phase": self.phase,
            "genome_axes": self.genome_axes,
            "elites": self.elites,
            "metric_directions": self.metric_directions,
            "validation_divergence": self.validation_divergence,
            "microtest_failures": self.microtest_failures,
            "neural_failures": self.neural_failures,
            "failure_memory": self.failure_memory,
            "corpus_profile": self.corpus_profile,
            "unmeasurable_axes": self.unmeasurable_axes,
            "unresolved_questions": self.unresolved_questions,
            "lineage_summary": self.lineage_summary,
            "budget": self.budget,
        }

    def compact_json(self, max_bytes: int = 24000) -> str:
        """Serialize, trimming the longest lists first if the report is oversized."""

        payload = self.to_dict()
        blob = json.dumps(payload, ensure_ascii=False, indent=1, sort_keys=True)
        trimmable = ["failure_memory", "microtest_failures", "validation_divergence",
                     "neural_failures", "elites"]
        while len(blob.encode()) > max_bytes:
            longest = max(
                trimmable,
                key=lambda key: len(payload.get(key) or []),
                default=None,
            )
            if longest is None or not payload.get(longest):
                break
            payload[longest] = payload[longest][: max(1, len(payload[longest]) // 2)]
            payload[f"{longest}_truncated"] = True
            blob = json.dumps(payload, ensure_ascii=False, indent=1, sort_keys=True)
        return blob


@dataclass
class ProposalBatch:
    accepted: list[ValidatedProposal] = field(default_factory=list)
    rejected: list[dict[str, Any]] = field(default_factory=list)
    raw: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "accepted": [proposal.to_dict() for proposal in self.accepted],
            "rejected": self.rejected,
        }


class MetaDesignerBackend(abc.ABC):
    """A source of proposals. Deterministic or model-driven; the loop cannot tell."""

    name: str = "abstract"

    @abc.abstractmethod
    def propose(self, report: ScientistReport) -> ProposalBatch:
        ...

    def _validate_all(
        self, payloads: list[Any], report: ScientistReport, raw: str | None = None,
    ) -> ProposalBatch:
        """Validate, safety-check and de-duplicate a backend's raw output.

        A backend that returns twenty proposals of which eighteen are malformed is not a
        failure of the loop — the eighteen are recorded with their rejection reasons and
        become evidence about that backend.
        """

        batch = ProposalBatch(raw=raw)
        axes = set(report.genome_axes)
        seen: set[str] = set()
        for payload in payloads:
            try:
                unsafe = static_safety(payload) if isinstance(payload, dict) else ["not-an-object"]
                if unsafe:
                    raise ProposalRejected(
                        f"static safety: proposal references {unsafe}; a meta-designer may "
                        "propose representations, not changes to the semantic substrate, the "
                        "sealed split, or the host"
                    )
                proposal = validate(payload, self.name, report.generation, axes)
                if proposal.proposal_id in seen:
                    raise ProposalRejected("duplicate proposal in the same batch")
                seen.add(proposal.proposal_id)
                batch.accepted.append(proposal)
            except ProposalRejected as error:
                batch.rejected.append({
                    "reason": str(error),
                    "payload": payload if isinstance(payload, dict) else repr(payload)[:400],
                })
        return batch
