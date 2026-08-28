"""LeanRuntimeState V2 validation, normalization, and canonical adaptation.

Raw Lean IDs remain authoritative inside one extraction.  Independent-run equivalence uses
only the documented normalization in :func:`normalize_runtime_state`; it never performs
pretty-text parsing, reduction, unfolding, or unproved definitional equality.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Iterator


EXPR_CONSTRUCTORS = {
    "bvar", "fvar", "mvar", "sort", "const", "app", "lam", "forallE",
    "letE", "lit", "mdata", "proj",
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def iter_expression_nodes(value: Any) -> Iterator[dict[str, Any]]:
    if isinstance(value, dict):
        if value.get("constructor") in EXPR_CONSTRUCTORS:
            yield value
        for child in value.values():
            yield from iter_expression_nodes(child)
    elif isinstance(value, list):
        for child in value:
            yield from iter_expression_nodes(child)


def validate_runtime_payload(payload: dict[str, Any]) -> None:
    if payload.get("schema_version") != "lean-runtime-state-v2.0.0":
        raise ValueError("unexpected Lean runtime schema")
    if payload.get("captured_targets") != len(payload.get("captures", [])):
        raise ValueError("captured_targets does not match captures")
    for capture in payload["captures"]:
        for phase in ("state_before", "state_after"):
            state = capture[phase]
            goal_ids = [goal["mvar_id"] for goal in state["goals"]]
            if goal_ids != state["goal_order"]:
                raise ValueError(f"goal order mismatch in {capture['record_id']}:{phase}")
            if state["focused_goal_id"] != (goal_ids[0] if goal_ids else None):
                raise ValueError(f"focused goal mismatch in {capture['record_id']}:{phase}")
            constructors = {node["constructor"] for node in iter_expression_nodes(state)}
            if not constructors.issubset(EXPR_CONSTRUCTORS):
                raise ValueError("unknown expression constructor")


def _local_declarations(state: dict[str, Any]) -> list[dict[str, Any]]:
    declarations: dict[str, dict[str, Any]] = {}
    for goal in state["goals"]:
        for declaration in goal.get("local_context", []):
            declarations.setdefault(declaration["fvar_id"], declaration)
    return sorted(declarations.values(), key=lambda declaration: declaration["index"])


def _identity_maps(state: dict[str, Any]) -> dict[str, dict[str, str]]:
    fvars = {
        declaration["fvar_id"]: f"f{index}"
        for index, declaration in enumerate(_local_declarations(state))
    }
    inventory = sorted(
        state["metavariable_context"]["declaration_inventory"],
        key=lambda declaration: (declaration["index"], declaration["mvar_id"]),
    )
    mvars: dict[str, str] = {
        declaration["mvar_id"]: f"m{index}"
        for index, declaration in enumerate(inventory)
    }
    for raw_id in state["goal_order"]:
        mvars.setdefault(raw_id, f"m{len(mvars)}")
    return {"fvar": fvars, "mvar": mvars, "lmvar": {}}


def _mapped(mapping: dict[str, str], raw: str, prefix: str) -> str:
    if raw not in mapping:
        mapping[raw] = f"{prefix}{len(mapping)}"
    return mapping[raw]


def _normalize_level(level: dict[str, Any], maps: dict[str, dict[str, str]]) -> dict[str, Any]:
    constructor = level["constructor"]
    if constructor == "zero":
        return {"constructor": "zero"}
    if constructor == "param":
        return {"constructor": "param", "name": level["name"]}
    if constructor == "mvar":
        return {
            "constructor": "mvar",
            "lmvar_id": _mapped(maps["lmvar"], level["lmvar_id"], "u"),
        }
    if constructor == "succ":
        return {"constructor": "succ", "of": _normalize_level(level["of"], maps)}
    return {
        "constructor": constructor,
        "left": _normalize_level(level["left"], maps),
        "right": _normalize_level(level["right"], maps),
    }


def normalize_expr(expr: dict[str, Any], maps: dict[str, dict[str, str]]) -> dict[str, Any]:
    """Normalize only ephemeral identities and alpha-irrelevant binder spellings."""

    constructor = expr["constructor"]
    if constructor == "bvar":
        return {"node": "bound_variable", "index": expr["debruijn_index"]}
    if constructor == "fvar":
        return {
            "node": "local_reference",
            "identity": _mapped(maps["fvar"], expr["fvar_id"], "f"),
        }
    if constructor == "mvar":
        return {
            "node": "metavariable_reference",
            "identity": _mapped(maps["mvar"], expr["mvar_id"], "m"),
        }
    if constructor == "sort":
        return {"node": "sort", "level": _normalize_level(expr["level"], maps)}
    if constructor == "const":
        return {
            "node": "symbol",
            "identity": expr["decl_name"],
            "universe_arguments": [
                _normalize_level(level, maps) for level in expr["universe_args"]
            ],
        }
    if constructor == "app":
        return {
            "node": "application",
            "function": normalize_expr(expr["function"], maps),
            "argument": normalize_expr(expr["argument"], maps),
        }
    if constructor in {"lam", "forallE"}:
        return {
            "node": "lambda" if constructor == "lam" else "dependent_function",
            "binder_name": "_",  # De Bruijn indices make spelling alpha-irrelevant.
            "binder_role": expr["binder_info"],
            "binder_type": normalize_expr(expr["binder_type"], maps),
            "body": normalize_expr(expr["body"], maps),
        }
    if constructor == "letE":
        return {
            "node": "let",
            "binder_name": "_",
            "type": normalize_expr(expr["type"], maps),
            "value": normalize_expr(expr["value"], maps),
            "body": normalize_expr(expr["body"], maps),
        }
    if constructor == "lit":
        return {"node": "literal", "literal_kind": expr["literal_kind"], "value": expr["value"]}
    if constructor == "mdata":
        return {
            "node": "annotated",
            "expression": normalize_expr(expr["expr"], maps),
            "source_metadata_delegated": True,
        }
    if constructor == "proj":
        return {
            "node": "projection",
            "type_identity": expr["type_name"],
            "field_index": expr["field_index"],
            "structure": normalize_expr(expr["struct"], maps),
        }
    raise ValueError(f"unknown Lean Expr constructor: {constructor}")


def _normalize_local_decl(
    declaration: dict[str, Any], maps: dict[str, dict[str, str]],
) -> dict[str, Any]:
    return {
        "identity": _mapped(maps["fvar"], declaration["fvar_id"], "f"),
        "user_name_diagnostic": declaration["user_name"],
        "binder_role": declaration["binder_info"],
        "declaration_role": declaration["declaration_kind"],
        "type": normalize_expr(declaration["type"], maps),
        "value": (
            normalize_expr(declaration["value"], maps)
            if declaration.get("value") is not None else None
        ),
    }


def normalize_runtime_state(state: dict[str, Any]) -> dict[str, Any]:
    maps = _identity_maps(state)
    goals = []
    for goal in state["goals"]:
        goals.append({
            "identity": _mapped(maps["mvar"], goal["mvar_id"], "m"),
            "target": normalize_expr(goal["target"], maps),
            "local_context": [
                _normalize_local_decl(declaration, maps)
                for declaration in goal.get("local_context", [])
            ],
            "local_instances": [
                {
                    "class_identity": instance["class_name"],
                    "term": normalize_expr(instance["fvar"], maps),
                }
                for instance in goal.get("local_instances", [])
            ],
        })
    relevant = []
    for declaration in state["metavariable_context"]["relevant_declarations"]:
        relevant.append({
            "identity": _mapped(maps["mvar"], declaration["mvar_id"], "m"),
            "kind": declaration["kind"],
            "type": normalize_expr(declaration["type"], maps),
            "assigned": declaration["is_assigned"],
            "assignment": (
                normalize_expr(declaration["assignment"], maps)
                if declaration["assignment"] is not None else None
            ),
        })
    return {
        "goals": goals,
        "focus_order": [goal["identity"] for goal in goals],
        "relevant_metavariables": sorted(relevant, key=lambda item: item["identity"]),
        "level_assignments": sorted(
            (
                maps["lmvar"][assignment["lmvar_id"]],
                _normalize_level(assignment["assignment"], maps),
            )
            for assignment in state["metavariable_context"]["level_assignments"]
            if assignment["lmvar_id"] in maps["lmvar"]
        ),
    }


def lean_state_equivalent(left: dict[str, Any], right: dict[str, Any]) -> bool:
    """Exact normalized structural equivalence; no definitional equality is guessed."""

    return normalize_runtime_state(left) == normalize_runtime_state(right)


def canonicalize_runtime_state(state: dict[str, Any], state_id: str) -> dict[str, Any]:
    maps = _identity_maps(state)
    normalized = normalize_runtime_state(state)
    raw_to_canonical_fvar = {
        raw: f"{state_id}:local:{normalized_id}" for raw, normalized_id in maps["fvar"].items()
    }
    raw_to_canonical_mvar = {
        raw: f"{state_id}:metavar:{normalized_id}" for raw, normalized_id in maps["mvar"].items()
    }
    return {
        "state_id": state_id,
        "source_system": "LEAN4",
        "goals": normalized["goals"],
        "focus_order": normalized["focus_order"],
        "metavariables": normalized["relevant_metavariables"],
        "universe_assignments": normalized["level_assignments"],
        "source_reference": {
            "runtime_state_sha256": digest(state),
            "raw_fvar_to_canonical": raw_to_canonical_fvar,
            "raw_mvar_to_canonical": raw_to_canonical_mvar,
            "relevant_metavariable_inventory_sha256": digest(
                state["metavariable_context"]["declaration_inventory"]
            ),
            "full_metavariable_inventory_count": state["metavariable_context"]["declaration_count"],
            "full_assigned_expression_count": state["metavariable_context"].get("assigned_expression_count"),
        },
        "information_accounting": {
            "expression_structure": "PRESERVED",
            "binder_and_local_identity": "PRESERVED_WITH_CROSS_RUN_NORMALIZATION",
            "goal_identity_and_order": "PRESERVED_WITH_CROSS_RUN_NORMALIZATION",
            "relevant_metavariables": "PRESERVED",
            "full_lean_metavariable_inventory": "DELEGATED_BY_HASHED_SOURCE_REFERENCE",
            "lean_metadata_payload": "SOURCE_SPECIFIC_BY_DESIGN",
            "standalone_constraint_table": "UNEXPOSED_BY_LEAN_4_10",
        },
    }


def canonicalize_capture(
    capture: dict[str, Any], delta: dict[str, Any],
    official_external_premise_refs: list[str] | None = None,
) -> dict[str, Any]:
    transition_id = capture["record_id"]
    before_id, after_id = f"{transition_id}:before", f"{transition_id}:after"
    before = canonicalize_runtime_state(capture["state_before"], before_id)
    after = canonicalize_runtime_state(capture["state_after"], after_id)
    before_fvars = before["source_reference"]["raw_fvar_to_canonical"]
    return {
        "schema_version": "canonical-math-transition-v2.0.0",
        "transition_id": transition_id,
        "state_before": before,
        "action": {
            "kind": "LEAN_ELABORATED_TACTIC_OCCURRENCE",
            "source_location": {
                "start": capture["source_start"], "end": capture["source_end"],
                "info_tree_path": capture["info_tree_path"],
            },
            "external_premise_refs": sorted(set(official_external_premise_refs or [])),
            "local_context_refs": [
                {
                    "canonical_id": before_fvars.get(raw_id),
                    "source_fvar_id": raw_id,
                    "resolved": raw_id in before_fvars,
                }
                for raw_id in capture["local_context_refs"]
            ],
            "reference_mechanism": capture["reference_mechanism"],
            "reference_completeness": capture["reference_completeness"],
        },
        "state_delta": delta,
        "state_after": after,
        "provenance": capture["environment"],
        "source_specific_reference": {
            "theorem_id": capture["theorem_id"],
            "transition_index": capture["transition_index"],
            "fresh_trace_ordinal": capture["fresh_trace_ordinal"],
            "elaborated_external_constant_refs": capture["external_constant_refs"],
        },
    }
