"""Identity-aware deltas over Lean runtime states."""

from __future__ import annotations

from typing import Any

from hml_v3.adapters.lean.runtime_v2 import digest


def goal_map(state: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {goal["mvar_id"]: goal for goal in state["goals"]}


def local_map(state: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for goal in state["goals"]:
        for declaration in goal.get("local_context", []):
            result[declaration["fvar_id"]] = declaration
    return result


def mvar_map(state: dict[str, Any]) -> dict[str, dict[str, Any]]:
    inventory = state["metavariable_context"]["declaration_inventory"]
    return {declaration["mvar_id"]: declaration for declaration in inventory}


def _changed_ids(
    before: dict[str, dict[str, Any]], after: dict[str, dict[str, Any]],
) -> list[str]:
    return sorted(
        key for key in before.keys() & after.keys()
        if digest(before[key]) != digest(after[key])
    )


def structured_delta(
    before_state: dict[str, Any], after_state: dict[str, Any],
    external_premises: list[str] | None = None,
    local_context_refs: list[str] | None = None,
    source_metavariable_delta: dict[str, Any] | None = None,
) -> dict[str, Any]:
    before_goals, after_goals = goal_map(before_state), goal_map(after_state)
    before_order, after_order = before_state["goal_order"], after_state["goal_order"]
    shared_goals = before_goals.keys() & after_goals.keys()
    before_locals, after_locals = local_map(before_state), local_map(after_state)
    before_mvars, after_mvars = mvar_map(before_state), mvar_map(after_state)
    assigned = {
        key for key in before_mvars.keys() & after_mvars.keys()
        if not before_mvars[key]["is_assigned"] and after_mvars[key]["is_assigned"]
    }
    created = set(after_mvars.keys() - before_mvars.keys())
    changed_mvars = set(_changed_ids(before_mvars, after_mvars))
    if source_metavariable_delta:
        created.update(
            item["mvar_id"] for item in source_metavariable_delta["declarations_created"]
        )
        assigned.update(
            item["mvar_id"]
            for item in source_metavariable_delta["expression_metavariables_newly_assigned"]
        )
        changed_mvars.update(
            item["mvar_id"]
            for item in source_metavariable_delta["expression_assignments_changed"]
        )
    target_changes = sorted(
        key for key in shared_goals
        if digest(before_goals[key].get("target")) != digest(after_goals[key].get("target"))
    )
    return {
        "delta_source": "ELABORATED_STABLE_IDENTITIES",
        "goals_created": sorted(after_goals.keys() - before_goals.keys()),
        "goals_solved": sorted(before_goals.keys() - after_goals.keys()),
        "goals_preserved": sorted(shared_goals),
        "goals_reordered": set(before_order) == set(after_order) and before_order != after_order,
        "goals_modified": sorted(
            key for key in shared_goals
            if key in target_changes
            or [item["fvar_id"] for item in before_goals[key].get("local_context", [])]
            != [item["fvar_id"] for item in after_goals[key].get("local_context", [])]
        ),
        "focus_before": before_state["focused_goal_id"],
        "focus_after": after_state["focused_goal_id"],
        "focus_changed": before_state["focused_goal_id"] != after_state["focused_goal_id"],
        "local_declarations_added": sorted(after_locals.keys() - before_locals.keys()),
        "local_declarations_removed": sorted(before_locals.keys() - after_locals.keys()),
        "local_declarations_changed": _changed_ids(before_locals, after_locals),
        "metavariables_created": sorted(created),
        "metavariables_removed_from_inventory": sorted(before_mvars.keys() - after_mvars.keys()),
        "metavariables_assigned": sorted(assigned),
        "metavariables_changed": sorted(changed_mvars),
        "external_premises_used": sorted(set(external_premises or [])),
        "local_context_refs_used": sorted(set(local_context_refs or [])),
        "expression_changes": {"goal_targets_changed": target_changes},
    }
