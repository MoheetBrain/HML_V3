from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hml_v3.adapters.lean.runtime_v2 import (
    EXPR_CONSTRUCTORS,
    canonicalize_capture,
    iter_expression_nodes,
    lean_state_equivalent,
    normalize_expr,
    normalize_runtime_state,
    validate_runtime_payload,
)
from hml_v3.canonical.delta_v2 import structured_delta


def const(name: str) -> dict:
    return {"constructor": "const", "decl_name": name, "universe_args": []}


def fvar(identity: str) -> dict:
    return {"constructor": "fvar", "fvar_id": identity}


def local(identity: str, index: int, name: str = "x") -> dict:
    return {
        "declaration_kind": "cdecl",
        "index": index,
        "fvar_id": identity,
        "user_name": name,
        "binder_info": "EXPLICIT",
        "local_decl_kind": "DEFAULT",
        "type": const("Nat"),
        "value": None,
        "non_dependent_hint": None,
    }


def inventory(identity: str, index: int, assigned: bool = False) -> dict:
    return {
        "mvar_id": identity,
        "user_name": "[anonymous]",
        "kind": "SYNTHETIC_OPAQUE",
        "depth": 0,
        "index": index,
        "is_assigned": assigned,
        "type_inventory": {"constructor": "const", "lean_hash": "1"},
        "assignment_inventory": ({"constructor": "const", "lean_hash": "2"} if assigned else None),
        "local_context_size": 0,
        "local_instance_count": 0,
    }


def goal(identity: str, target: dict, locals_: list[dict] | None = None, ordinal: int = 0) -> dict:
    return {
        "mvar_id": identity,
        "ordinal": ordinal,
        "focused": ordinal == 0,
        "declaration_available": True,
        "target": target,
        "local_context": locals_ or [],
        "local_instances": [],
        "user_name": "[anonymous]",
        "kind": "SYNTHETIC_OPAQUE",
    }


def state(goals: list[dict], inventories: list[dict] | None = None) -> dict:
    order = [item["mvar_id"] for item in goals]
    return {
        "goal_order": order,
        "focused_goal_id": order[0] if order else None,
        "goals": goals,
        "metavariable_context": {
            "declaration_count": len(inventories or []),
            "declaration_inventory": inventories or [],
            "relevant_declarations": [],
            "level_assignments": [],
            "delayed_assignments": [],
        },
    }


class LeanRuntimeV2Tests(unittest.TestCase):
    def test_expr_constructor_serialization_contract_is_complete(self) -> None:
        expressions = [
            {"constructor": "bvar", "debruijn_index": 0},
            fvar("f.1"),
            {"constructor": "mvar", "mvar_id": "m.1"},
            {"constructor": "sort", "level": {"constructor": "zero"}},
            const("Nat"),
            {"constructor": "app", "function": const("Nat.succ"), "argument": fvar("f.1")},
            {"constructor": "lam", "binder_name": "x", "binder_info": "EXPLICIT", "binder_type": const("Nat"), "body": {"constructor": "bvar", "debruijn_index": 0}},
            {"constructor": "forallE", "binder_name": "x", "binder_info": "IMPLICIT", "binder_type": const("Nat"), "body": const("Prop")},
            {"constructor": "letE", "decl_name": "x", "type": const("Nat"), "value": {"constructor": "lit", "literal_kind": "NAT", "value": 1}, "body": {"constructor": "bvar", "debruijn_index": 0}, "non_dependent_hint": True},
            {"constructor": "lit", "literal_kind": "STRING", "value": "x"},
            {"constructor": "mdata", "metadata": [], "expr": const("Nat")},
            {"constructor": "proj", "type_name": "Prod", "field_index": 0, "struct": fvar("f.1")},
        ]
        seen = {node["constructor"] for node in iter_expression_nodes(expressions)}
        self.assertEqual(seen, EXPR_CONSTRUCTORS)

    def test_alpha_renaming_is_normalized_but_binder_role_is_not(self) -> None:
        left = {"constructor": "lam", "binder_name": "x", "binder_info": "EXPLICIT", "binder_type": const("Nat"), "body": {"constructor": "bvar", "debruijn_index": 0}}
        right = {**left, "binder_name": "renamed"}
        maps = {"fvar": {}, "mvar": {}, "lmvar": {}}
        self.assertEqual(normalize_expr(left, deepcopy(maps)), normalize_expr(right, deepcopy(maps)))
        implicit = {**right, "binder_info": "IMPLICIT"}
        self.assertNotEqual(normalize_expr(left, deepcopy(maps)), normalize_expr(implicit, deepcopy(maps)))

    def test_shadowed_fvars_keep_distinct_identity(self) -> None:
        locals_ = [local("raw.a", 0, "x"), local("raw.b", 1, "x")]
        a = state([goal("g", fvar("raw.a"), locals_)], [inventory("g", 0)])
        b = state([goal("g", fvar("raw.b"), locals_)], [inventory("g", 0)])
        self.assertNotEqual(normalize_runtime_state(a), normalize_runtime_state(b))

    def test_goal_reordering_preserves_mvar_correspondence(self) -> None:
        inventories = [inventory("goal.a", 0), inventory("goal.b", 1)]
        a = state([goal("goal.a", const("P"), ordinal=0), goal("goal.b", const("P"), ordinal=1)], inventories)
        b = state([goal("goal.b", const("P"), ordinal=0), goal("goal.a", const("P"), ordinal=1)], inventories)
        delta = structured_delta(a, b)
        self.assertTrue(delta["goals_reordered"])
        self.assertTrue(delta["focus_changed"])
        self.assertEqual(delta["goals_created"], [])
        self.assertEqual(delta["goals_solved"], [])
        self.assertFalse(lean_state_equivalent(a, b))

    def test_metavariable_assignment_is_an_identity_delta(self) -> None:
        before = state([], [inventory("m", 0, assigned=False)])
        after = state([], [inventory("m", 0, assigned=True)])
        delta = structured_delta(before, after)
        self.assertEqual(delta["metavariables_assigned"], ["m"])

    def test_local_dependencies_and_nested_path_survive_canonical_adapter(self) -> None:
        before = state([goal("g", fvar("f"), [local("f", 0)])], [inventory("g", 0)])
        after = state([], [inventory("g", 0, assigned=True)])
        capture = {
            "record_id": "r",
            "theorem_id": "T",
            "transition_index": 2,
            "fresh_trace_ordinal": 3,
            "source_start": {"raw": 10, "line": 2, "column": 3},
            "source_end": {"raw": 20, "line": 2, "column": 13},
            "info_tree_path": [1, 4, 2],
            "state_before": before,
            "state_after": after,
            "local_context_refs": ["f"],
            "external_constant_refs": ["Nat.succ"],
            "reference_mechanism": "DIRECT_TRAVERSAL_OF_ELABORATED_TERMINFO_EXPRS",
            "reference_completeness": "PARTIAL_TACTICS_WITHOUT_TERMINFO_MAY_HIDE_INTERNAL_USE",
            "environment": {"current_namespace": "N"},
        }
        delta = structured_delta(before, after, ["Nat.succ"], ["f"])
        canonical = canonicalize_capture(capture, delta)
        self.assertEqual(canonical["action"]["source_location"]["info_tree_path"], [1, 4, 2])
        self.assertTrue(canonical["action"]["local_context_refs"][0]["resolved"])
        self.assertEqual(canonical["state_delta"]["delta_source"], "ELABORATED_STABLE_IDENTITIES")

    def test_payload_validation_checks_goal_identity(self) -> None:
        runtime_state = state([goal("g", const("P"))], [inventory("g", 0)])
        payload = {
            "schema_version": "lean-runtime-state-v2.0.0",
            "captured_targets": 1,
            "captures": [{"record_id": "r", "state_before": runtime_state, "state_after": state([])}],
        }
        validate_runtime_payload(payload)
        broken = deepcopy(payload)
        broken["captures"][0]["state_before"]["goal_order"] = ["other"]
        with self.assertRaises(ValueError):
            validate_runtime_payload(broken)

    def test_v2_schemas_are_versioned_json(self) -> None:
        lean_schema = json.loads((ROOT / "schemas/lean_runtime_state_v2.schema.json").read_text())
        canonical_schema = json.loads((ROOT / "schemas/canonical_math_state_v2.schema.json").read_text())
        self.assertEqual(lean_schema["properties"]["schema_version"]["const"], "lean-runtime-state-v2.0.0")
        self.assertEqual(canonical_schema["properties"]["schema_version"]["const"], "canonical-math-transition-v2.0.0")


if __name__ == "__main__":
    unittest.main()
