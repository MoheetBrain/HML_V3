"""The shared model-facing semantic projection used by every renderer candidate."""

from __future__ import annotations

from typing import Any

from .models import CanonicalMathState, CanonicalTransition


def state_projection(state: CanonicalMathState) -> dict[str, Any]:
    return {
        "source_system": state.source_system,
        "declarations": [
            {
                "name": item.name,
                "type": item.type_expression.surface,
                "value": item.value_expression.surface if item.value_expression else None,
                "binder_info": item.binder_info,
                "scope_id": item.scope_id,
            }
            for item in state.declarations
        ],
        "goals": [
            {
                "target": goal.target.surface,
                "status": goal.status,
                "local_context_indices": [
                    index
                    for index, declaration in enumerate(state.declarations)
                    if declaration.declaration_id in goal.local_context_ids
                ],
                "source_label": goal.source_label,
            }
            for goal in state.goals
        ],
        "metavariables": list(state.metavariables),
        "constraints": list(state.constraints),
        "obligations": list(state.obligations),
        "dependencies": list(state.dependencies),
        "premise_refs": list(state.premise_refs),
        "scopes": list(state.scopes),
        "namespace_environment_refs": state.namespace_environment_refs,
    }


def transition_projection(transition: CanonicalTransition) -> dict[str, Any]:
    return {
        "state_before": state_projection(transition.state_before),
        "action": {
            "kind": transition.action.action_kind,
            "target_goal_indices": [
                index
                for index, goal in enumerate(transition.state_before.goals)
                if goal.goal_id in transition.action.target_goal_ids
            ],
            "arguments": list(transition.action.arguments),
            "substitutions": list(transition.action.substitutions),
            "source_syntax": transition.action.source_syntax,
            "referenced_premises": list(transition.action.referenced_premises),
            "expected_effect": transition.action.expected_effect,
        },
        "state_delta": {
            "declarations_added": list(transition.state_delta.declarations_added),
            "declarations_removed": list(transition.state_delta.declarations_removed),
            "declarations_rebound": list(transition.state_delta.declarations_rebound),
            "goals_before": transition.state_delta.goals_before,
            "goals_after": transition.state_delta.goals_after,
            "goals_generated": transition.state_delta.goals_generated,
            "goals_solved": transition.state_delta.goals_solved,
            "focused_target_changed": transition.state_delta.focused_target_changed,
            "recorded_effect_class": transition.state_delta.recorded_effect_class,
        },
        "state_after": state_projection(transition.state_after),
    }
