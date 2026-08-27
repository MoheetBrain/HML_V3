#!/usr/bin/env python3
"""Read-only compatibility bridge to the frozen previous HML transition view.

The previous repository is imported at an attested commit and is never modified. Fields
that its semantic-state schema does not own are visible in its supported ``source`` JSON
block; the core claims, goals, action, premises, and effects use native previous-HML nodes.
"""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
from typing import Any


FROZEN_REPOSITORY = Path("/Users/moheet/Documents/ChatGPT/hamiltonian-lang-final-signal")
FROZEN_COMMIT = "b011511e72572608eb7836d3b8a1a6bb794c890d"


def _verify_and_import() -> dict[str, Any]:
    actual = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=FROZEN_REPOSITORY,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    ).stdout.strip()
    if actual != FROZEN_COMMIT:
        raise RuntimeError(f"frozen HML commit mismatch: expected {FROZEN_COMMIT}, found {actual}")
    sys.path.insert(0, str(FROZEN_REPOSITORY / "src"))
    from hamiltonian_lang.semantic_state.model import (  # noqa: PLC0415
        Action,
        Claim,
        ClaimStatus,
        Goal,
        GoalStatus,
        SemanticState,
        Transition,
    )
    from hamiltonian_lang.semantic_state.view import parse_transition, render_transition  # noqa: PLC0415

    return locals()


HML = _verify_and_import()


def _compact(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _state_to_hml(state: dict[str, Any]) -> tuple[Any, dict[str, Any]]:
    claims: dict[str, Any] = {}
    declaration_order: list[str] = []
    declaration_metadata: dict[str, Any] = {}
    for index, declaration in enumerate(state["declarations"]):
        claim_id = f"decl:{index}"
        declaration_order.append(claim_id)
        proposition = _compact(
            {
                "name": declaration["name"],
                "type": declaration["type"],
                "value": declaration["value"],
            }
        )
        claims[claim_id] = HML["Claim"](
            claim_id,
            proposition,
            HML["ClaimStatus"].GIVEN,
            declaration["scope_id"],
        )
        declaration_metadata[claim_id] = {"binder_info": declaration["binder_info"]}

    goals: dict[str, Any] = {}
    goal_order: list[str] = []
    goal_metadata: dict[str, Any] = {}
    for index, goal in enumerate(state["goals"]):
        goal_id = f"goal:{index}"
        goal_order.append(goal_id)
        status = (
            HML["GoalStatus"].OPEN
            if goal["status"] == "OPEN"
            else HML["GoalStatus"].DISCHARGED
        )
        goals[goal_id] = HML["Goal"](goal_id, goal["target"], status, f"goal:{index}:context")
        goal_metadata[goal_id] = {
            "local_context_indices": goal["local_context_indices"],
            "source_label": goal["source_label"],
        }

    active_scopes = tuple(
        dict.fromkeys(
            [*state["scopes"], *(item["scope_id"] for item in state["declarations"])]
        )
    )
    hml_state = HML["SemanticState"](claims=claims, goals=goals, active_scopes=active_scopes)
    bridge = {
        "source_system": state["source_system"],
        "declaration_order": declaration_order,
        "declaration_metadata": declaration_metadata,
        "goal_order": goal_order,
        "goal_metadata": goal_metadata,
        "metavariables": state["metavariables"],
        "constraints": state["constraints"],
        "obligations": state["obligations"],
        "dependencies": state["dependencies"],
        "premise_refs": state["premise_refs"],
        "scopes": state["scopes"],
        "namespace_environment_refs": state["namespace_environment_refs"],
    }
    return hml_state, bridge


def _projection_to_hml(projection: dict[str, Any]) -> Any:
    before, before_bridge = _state_to_hml(projection["state_before"])
    after, after_bridge = _state_to_hml(projection["state_after"])
    action = projection["action"]
    hml_action = HML["Action"](
        id="transition_action",
        operation=action["kind"],
        summary=action["source_syntax"],
        dependencies=tuple(action["referenced_premises"]),
        preconditions=tuple(action["arguments"]),
        typing={"v3_substitutions": action["substitutions"]},
        goal_effect={
            "v3_target_goal_indices": action["target_goal_indices"],
            "v3_expected_effect": action["expected_effect"],
            "v3_state_delta": projection["state_delta"],
        },
    )
    return HML["Transition"](
        case_id="v3_transition",
        schema_version="hml-v3-over-previous-hml-view-1.0.0",
        action=hml_action,
        state_before=before,
        state_after=after,
        source={
            "bridge_version": "hml-v3-previous-hml-bridge-1.0.0",
            "frozen_hml_commit": FROZEN_COMMIT,
            "state_before": before_bridge,
            "state_after": after_bridge,
        },
    )


def _state_from_hml(state: Any, bridge: dict[str, Any]) -> dict[str, Any]:
    declarations: list[dict[str, Any]] = []
    for claim_id in bridge["declaration_order"]:
        claim = state.claims[claim_id]
        core = json.loads(claim.proposition)
        declarations.append(
            {
                "name": core["name"],
                "type": core["type"],
                "value": core["value"],
                "binder_info": bridge["declaration_metadata"][claim_id]["binder_info"],
                "scope_id": claim.scope,
            }
        )
    goals: list[dict[str, Any]] = []
    for goal_id in bridge["goal_order"]:
        goal = state.goals[goal_id]
        metadata = bridge["goal_metadata"][goal_id]
        goals.append(
            {
                "target": goal.proposition,
                "status": str(goal.status),
                "local_context_indices": metadata["local_context_indices"],
                "source_label": metadata["source_label"],
            }
        )
    return {
        "source_system": bridge["source_system"],
        "declarations": declarations,
        "goals": goals,
        "metavariables": bridge["metavariables"],
        "constraints": bridge["constraints"],
        "obligations": bridge["obligations"],
        "dependencies": bridge["dependencies"],
        "premise_refs": bridge["premise_refs"],
        "scopes": bridge["scopes"],
        "namespace_environment_refs": bridge["namespace_environment_refs"],
    }


def _hml_to_projection(transition: Any) -> dict[str, Any]:
    bridge = transition.source
    if bridge.get("frozen_hml_commit") != FROZEN_COMMIT:
        raise ValueError("previous-HML bridge commit is absent or incorrect")
    action = transition.action
    expected = action.goal_effect
    substitutions = action.typing.get("v3_substitutions", [])
    return {
        "state_before": _state_from_hml(transition.state_before, bridge["state_before"]),
        "action": {
            "kind": action.operation,
            "target_goal_indices": expected["v3_target_goal_indices"],
            "arguments": list(action.preconditions),
            "substitutions": substitutions,
            "source_syntax": action.summary,
            "referenced_premises": list(action.dependencies),
            "expected_effect": expected["v3_expected_effect"],
        },
        "state_delta": expected["v3_state_delta"],
        "state_after": _state_from_hml(transition.state_after, bridge["state_after"]),
    }


def main() -> int:
    request = json.load(sys.stdin)
    operation = request["operation"]
    if operation == "render_many":
        result = [HML["render_transition"](_projection_to_hml(item)) for item in request["items"]]
    elif operation == "parse_many":
        result = [_hml_to_projection(HML["parse_transition"](item)) for item in request["items"]]
    else:
        raise ValueError(f"unknown operation: {operation}")
    json.dump(result, sys.stdout, ensure_ascii=False, separators=(",", ":"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
