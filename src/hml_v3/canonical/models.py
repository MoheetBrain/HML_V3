"""Representation-independent mathematical state and transition records.

The first adapter preserves Lean source observations exactly while exposing only the
structure justified by the source trace. Source-specific fallbacks and information losses
are explicit; no field pretends that pretty-printed text is a universal mathematical AST.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
import hashlib
import json
from typing import Any


def stable_sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class Expression:
    expression_id: str
    language: str
    surface: str
    role: str
    source_sha256: str
    ast_status: str = "SOURCE_SYSTEM_SPECIFIC"

    @classmethod
    def from_surface(cls, expression_id: str, surface: str, role: str) -> "Expression":
        return cls(expression_id, "LEAN4_PRETTY_PRINTED", surface, role, stable_sha256(surface))


@dataclass(frozen=True)
class Declaration:
    declaration_id: str
    name: str
    type_expression: Expression
    value_expression: Expression | None = None
    binder_info: str = "UNKNOWN_FROM_PRETTY_PRINTED_STATE"
    scope_id: str = "lean_local_context"


@dataclass(frozen=True)
class Goal:
    goal_id: str
    target: Expression
    status: str
    local_context_ids: tuple[str, ...]
    source_label: str | None = None


@dataclass(frozen=True)
class CanonicalMathState:
    state_id: str
    source_system: str
    declarations: tuple[Declaration, ...]
    goals: tuple[Goal, ...]
    metavariables: tuple[str, ...] = ()
    constraints: tuple[dict[str, Any], ...] = ()
    obligations: tuple[dict[str, Any], ...] = ()
    dependencies: tuple[str, ...] = ()
    premise_refs: tuple[str, ...] = ()
    scopes: tuple[str, ...] = ("lean_local_context",)
    namespace_environment_refs: dict[str, Any] = field(default_factory=dict)
    evidence: tuple[dict[str, Any], ...] = ()
    provenance: dict[str, Any] = field(default_factory=dict)
    source_specific: dict[str, Any] = field(default_factory=dict)
    information_accounting: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class CanonicalAction:
    action_id: str
    action_kind: str
    target_goal_ids: tuple[str, ...]
    arguments: tuple[dict[str, Any], ...]
    substitutions: tuple[dict[str, Any], ...]
    referenced_premises: tuple[str, ...]
    expected_effect: dict[str, Any]
    source_syntax: str
    source_syntax_sha256: str


@dataclass(frozen=True)
class StateDelta:
    declarations_added: tuple[str, ...]
    declarations_removed: tuple[str, ...]
    declarations_rebound: tuple[str, ...]
    goals_before: int
    goals_after: int
    goals_generated: int
    goals_solved: int
    focused_target_changed: bool
    recorded_effect_class: str


@dataclass(frozen=True)
class VerifierResult:
    authority: str
    status: str
    accepted: bool | None
    fresh_replay_status: str | None
    source_record_sha256: str
    certificate_id: str | None = None
    certificate_content_sha256: str | None = None


@dataclass(frozen=True)
class CanonicalTransition:
    transition_id: str
    schema_version: str
    state_before: CanonicalMathState
    action: CanonicalAction
    state_delta: StateDelta
    state_after: CanonicalMathState
    verifier_result: VerifierResult
    provenance: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "CanonicalTransition":
        def expression(raw: dict[str, Any]) -> Expression:
            return Expression(**raw)

        def declaration(raw: dict[str, Any]) -> Declaration:
            raw = dict(raw)
            raw["type_expression"] = expression(raw["type_expression"])
            if raw.get("value_expression") is not None:
                raw["value_expression"] = expression(raw["value_expression"])
            return Declaration(**raw)

        def goal(raw: dict[str, Any]) -> Goal:
            raw = dict(raw)
            raw["target"] = expression(raw["target"])
            raw["local_context_ids"] = tuple(raw["local_context_ids"])
            return Goal(**raw)

        def state(raw: dict[str, Any]) -> CanonicalMathState:
            raw = dict(raw)
            raw["declarations"] = tuple(declaration(item) for item in raw["declarations"])
            raw["goals"] = tuple(goal(item) for item in raw["goals"])
            for key in ("metavariables", "constraints", "obligations", "dependencies", "premise_refs", "scopes", "evidence"):
                raw[key] = tuple(raw[key])
            return CanonicalMathState(**raw)

        action_raw = dict(value["action"])
        for key in ("target_goal_ids", "arguments", "substitutions", "referenced_premises"):
            action_raw[key] = tuple(action_raw[key])
        delta_raw = dict(value["state_delta"])
        for key in ("declarations_added", "declarations_removed", "declarations_rebound"):
            delta_raw[key] = tuple(delta_raw[key])
        return cls(
            transition_id=value["transition_id"],
            schema_version=value["schema_version"],
            state_before=state(value["state_before"]),
            action=CanonicalAction(**action_raw),
            state_delta=StateDelta(**delta_raw),
            state_after=state(value["state_after"]),
            verifier_result=VerifierResult(**value["verifier_result"]),
            provenance=dict(value["provenance"]),
        )

    def canonical_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":"))

    def content_sha256(self) -> str:
        return stable_sha256(self.canonical_json())
