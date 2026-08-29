"""The matched pair, and the lab that holds them."""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
from typing import Any

LAB_VERSION = "micromath-lab-v1.0.0"

#: STATE_A is an exact real Lean-derived canonical state. STATE_B is a structural
#: transposition of it: well-formed, ground truth known by construction, and NOT claimed to
#: be a provable Lean proof state. Reports must keep the two shares separate.
REAL_LEAN_BASE = "REAL_LEAN_DERIVED_BASE"
TRANSPOSITION = "STRUCTURAL_TRANSPOSITION_COUNTERFACTUAL"


@dataclass
class MicroPair:
    pair_id: str
    domain: str
    domain_confidence: str
    stress: str
    base_transition_id: str
    source_file: str
    question: str
    options: tuple[str, str]
    answer_a: str
    answer_b: str
    relation: str
    state_a: dict[str, Any]
    state_b: dict[str, Any]
    detail: dict[str, Any] = field(default_factory=dict)

    @property
    def cell(self) -> tuple[str, str]:
        return (self.domain, self.stress)

    def to_dict(self) -> dict[str, Any]:
        return {
            "pair_id": self.pair_id,
            "domain": self.domain,
            "domain_confidence": self.domain_confidence,
            "stress": self.stress,
            "base_transition_id": self.base_transition_id,
            "source_file": self.source_file,
            "question": self.question,
            "options": list(self.options),
            "answer_a": self.answer_a,
            "answer_b": self.answer_b,
            "relation": self.relation,
            "provenance": {"state_a": REAL_LEAN_BASE, "state_b": TRANSPOSITION},
            "detail": self.detail,
            "state_a": self.state_a,
            "state_b": self.state_b,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "MicroPair":
        return cls(
            pair_id=payload["pair_id"], domain=payload["domain"],
            domain_confidence=payload["domain_confidence"], stress=payload["stress"],
            base_transition_id=payload["base_transition_id"],
            source_file=payload["source_file"], question=payload["question"],
            options=tuple(payload["options"]), answer_a=payload["answer_a"],
            answer_b=payload["answer_b"], relation=payload["relation"],
            state_a=payload["state_a"], state_b=payload["state_b"],
            detail=payload.get("detail", {}),
        )


def pair_id(domain: str, stress: str, transition_id: str) -> str:
    digest = hashlib.sha256(
        f"{LAB_VERSION}|{domain}|{stress}|{transition_id}".encode()).hexdigest()
    return f"MP_{digest[:12]}"


def state_digest(state: dict[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(state, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
