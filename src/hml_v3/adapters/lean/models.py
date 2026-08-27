"""Source-faithful Lean transition records used at the adapter boundary."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class LeanStateObservation:
    raw_state: str
    hypotheses: tuple[dict[str, str], ...]
    focused_target: str
    goal_count: int


@dataclass(frozen=True)
class LeanActionObservation:
    raw_tactic: str
    premises_used: tuple[str, ...]
    effect_class: str
    recorded_effect: dict[str, Any]


@dataclass(frozen=True)
class LeanTransition:
    transition_id: str
    theorem_id: str
    source_file: str
    transition_index: int
    official_split: str
    mathlib_commit: str
    lean_version: str
    state_before: LeanStateObservation
    action: LeanActionObservation
    state_after: LeanStateObservation
    source_record_sha256: str
    source_record: dict[str, Any]
    replay_certificate: dict[str, Any] | None = None
