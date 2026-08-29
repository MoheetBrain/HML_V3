"""Loading the representations under audit: finalists plus the required controls.

`MICROMATH §15` fixes the signal that matters. A candidate scoring 85% is not a result; the
result is ``score(candidate) - max(score(controls))``, and the controls have to be able to
represent the *same* canonical state or the comparison is not paired.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from hml_v3.representation_search.compiler import build
from hml_v3.representation_search.lineage import CandidateRegistry
from hml_v3.representation_search.primitive_registry import PrimitiveRegistry
from hml_v3.representation_search.seeds import SEEDS

#: The four controls the mission names, mapped onto this repository's seed labels.
CONTROLS: dict[str, str] = {
    "LEAN_LIKE": "SEED_LEAN_LIKE",
    "STRUCTURED_ENGLISH": "SEED_STRUCTURED_ENGLISH",
    "TYPED_AST": "SEED_TYPED_AST",
    "OLD_HML": "SEED_PRIOR_HML",
}


@dataclass
class Candidate:
    label: str
    kind: str          # FINALIST | CONTROL
    candidate_id: str
    compiler: Any
    invented: dict[str, str]

    def to_dict(self) -> dict[str, Any]:
        return {"label": self.label, "kind": self.kind,
                "candidate_id": self.candidate_id, "invented_axes": self.invented}


def load_controls() -> list[Candidate]:
    controls: list[Candidate] = []
    for label, seed in CONTROLS.items():
        genome = SEEDS[seed]
        controls.append(Candidate(
            label=label, kind="CONTROL", candidate_id=genome.candidate_id(),
            compiler=build(genome), invented={}))
    return controls


def load_finalists(workspace: Path, frontier: Path) -> list[Candidate]:
    payload = json.loads(frontier.read_text())
    registry = CandidateRegistry(workspace / "candidate_registry.jsonl")
    primitives_path = workspace / "primitive_registry.jsonl"
    primitives = PrimitiveRegistry(primitives_path) if primitives_path.exists() else None
    state = json.loads((workspace / "search_state.json").read_text())
    invented_by_candidate = state.get("invented", {}) or {}

    finalists: list[Candidate] = []
    for entry in payload["finalists"]:
        candidate_id = entry["label"]
        record = registry.get(candidate_id)
        if record is None:
            continue
        invented = invented_by_candidate.get(candidate_id) or {}
        finalists.append(Candidate(
            label=candidate_id, kind="FINALIST", candidate_id=candidate_id,
            compiler=build(record.genome, invented, primitives if invented else None),
            invented=invented))
    return finalists
