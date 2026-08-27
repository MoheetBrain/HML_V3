"""Five independent initial surfaces over one shared semantic projection."""

from __future__ import annotations

import json
from typing import Any

from .base import Projection, Renderer, canonical_projection_json


def _load_object(text: str) -> Projection:
    value = json.loads(text)
    if not isinstance(value, dict):
        raise ValueError("renderer payload must decode to an object")
    return value


class LeanLikeRenderer(Renderer):
    renderer_id = "lean_like"

    _ORDER = ("state_before", "action", "state_delta", "state_after")

    def render(self, projection: Projection) -> str:
        lines = ["-- HML V3 candidate: Lean-like transition"]
        lines.extend(f"{key} := {canonical_projection_json(projection[key])}" for key in self._ORDER)
        return "\n".join(lines) + "\n"

    def parse(self, text: str) -> Projection:
        rows: Projection = {}
        for line in text.splitlines():
            if not line or line.startswith("--"):
                continue
            key, separator, value = line.partition(" := ")
            if not separator or key not in self._ORDER:
                raise ValueError(f"invalid Lean-like row: {line[:80]}")
            rows[key] = json.loads(value)
        if tuple(rows) != self._ORDER:
            raise ValueError("Lean-like transition has missing or reordered sections")
        return rows


class StructuredEnglishRenderer(Renderer):
    renderer_id = "structured_english"

    _ROWS = (
        ("Before the action, the mathematical state is", "state_before"),
        ("The proposed action is", "action"),
        ("The observed state change is", "state_delta"),
        ("After the action, the mathematical state is", "state_after"),
    )

    def render(self, projection: Projection) -> str:
        return "\n".join(
            f"{sentence}: {canonical_projection_json(projection[key])}" for sentence, key in self._ROWS
        ) + "\n"

    def parse(self, text: str) -> Projection:
        lines = text.splitlines()
        if len(lines) != len(self._ROWS):
            raise ValueError("structured-English transition must contain four statements")
        result: Projection = {}
        for line, (sentence, key) in zip(lines, self._ROWS):
            prefix = f"{sentence}: "
            if not line.startswith(prefix):
                raise ValueError(f"expected statement prefix: {sentence}")
            result[key] = json.loads(line[len(prefix) :])
        return result


def _tag(value: Any, label: str) -> Any:
    if isinstance(value, dict):
        return {
            "node_type": label,
            "fields": {key: _tag(child, key) for key, child in sorted(value.items())},
        }
    if isinstance(value, list):
        return {"node_type": f"{label}_list", "items": [_tag(child, label) for child in value]}
    return {"node_type": f"{label}_scalar", "value": value}


def _untag(value: Any) -> Any:
    if not isinstance(value, dict) or "node_type" not in value:
        raise ValueError("invalid typed-AST node")
    if "fields" in value:
        return {key: _untag(child) for key, child in value["fields"].items()}
    if "items" in value:
        return [_untag(child) for child in value["items"]]
    if "value" not in value:
        raise ValueError("typed-AST scalar has no value")
    return value["value"]


class TypedAstRenderer(Renderer):
    renderer_id = "typed_ast"

    def render(self, projection: Projection) -> str:
        return json.dumps(_tag(projection, "transition"), ensure_ascii=False, sort_keys=True) + "\n"

    def parse(self, text: str) -> Projection:
        value = _untag(json.loads(text))
        if not isinstance(value, dict):
            raise ValueError("typed-AST root is not a transition")
        return value


class SExpressionRenderer(Renderer):
    renderer_id = "canonical_sexpr"

    _ORDER = ("state_before", "action", "state_delta", "state_after")

    def render(self, projection: Projection) -> str:
        lines = ["(transition"]
        lines.extend(f"  ({key} {canonical_projection_json(projection[key])})" for key in self._ORDER)
        lines.append(")")
        return "\n".join(lines) + "\n"

    def parse(self, text: str) -> Projection:
        lines = text.splitlines()
        if not lines or lines[0] != "(transition" or lines[-1] != ")":
            raise ValueError("invalid transition S-expression envelope")
        result: Projection = {}
        if len(lines[1:-1]) != len(self._ORDER):
            raise ValueError("transition S-expression must contain four fields")
        for line, expected in zip(lines[1:-1], self._ORDER):
            prefix = f"  ({expected} "
            if not line.startswith(prefix) or not line.endswith(")"):
                raise ValueError(f"invalid S-expression field: {expected}")
            result[expected] = json.loads(line[len(prefix) : -1])
        return result


class GraphEdgeRenderer(Renderer):
    renderer_id = "graph_edges"

    def render(self, projection: Projection) -> str:
        graph = {
            "format": "hml-v3-transition-graph-1.0.0",
            "nodes": [
                {"id": "before", "role": "state_before", "payload": projection["state_before"]},
                {"id": "action", "role": "action", "payload": projection["action"]},
                {"id": "delta", "role": "state_delta", "payload": projection["state_delta"]},
                {"id": "after", "role": "state_after", "payload": projection["state_after"]},
            ],
            "edges": [
                {"source": "before", "relation": "ENABLES", "target": "action"},
                {"source": "action", "relation": "HAS_DELTA", "target": "delta"},
                {"source": "action", "relation": "PRODUCES", "target": "after"},
            ],
        }
        return json.dumps(graph, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"

    def parse(self, text: str) -> Projection:
        graph = _load_object(text)
        if graph.get("format") != "hml-v3-transition-graph-1.0.0":
            raise ValueError("unknown graph-edge format")
        expected_edges = {
            ("before", "ENABLES", "action"),
            ("action", "HAS_DELTA", "delta"),
            ("action", "PRODUCES", "after"),
        }
        actual_edges = {
            (item["source"], item["relation"], item["target"]) for item in graph["edges"]
        }
        if actual_edges != expected_edges:
            raise ValueError("graph-edge connectivity is invalid")
        by_role = {node["role"]: node["payload"] for node in graph["nodes"]}
        expected_roles = {"state_before", "action", "state_delta", "state_after"}
        if by_role.keys() != expected_roles:
            raise ValueError("graph-edge roles are incomplete")
        return {key: by_role[key] for key in ("state_before", "action", "state_delta", "state_after")}


def _goal_local_state(state: Projection) -> Projection:
    metadata = {key: value for key, value in state.items() if key not in ("declarations", "goals")}
    referenced: set[int] = set()
    frames = []
    for goal in state["goals"]:
        indices = goal["local_context_indices"]
        referenced.update(indices)
        frames.append(
            {
                "target": goal["target"],
                "status": goal["status"],
                "source_label": goal["source_label"],
                "local_context": [
                    {"source_index": index, "declaration": state["declarations"][index]}
                    for index in indices
                ],
            }
        )
    unreferenced = [
        {"source_index": index, "declaration": declaration}
        for index, declaration in enumerate(state["declarations"])
        if index not in referenced
    ]
    return {
        "metadata": metadata,
        "declaration_count": len(state["declarations"]),
        "goal_frames": frames,
        "unreferenced_declarations": unreferenced,
    }


def _from_goal_local_state(encoded: Projection) -> Projection:
    declarations: dict[int, Projection] = {}
    goals = []
    for frame in encoded["goal_frames"]:
        indices = []
        for item in frame["local_context"]:
            index = item["source_index"]
            if index in declarations and declarations[index] != item["declaration"]:
                raise ValueError("goal-local declaration copies disagree")
            declarations[index] = item["declaration"]
            indices.append(index)
        goals.append(
            {
                "target": frame["target"],
                "status": frame["status"],
                "local_context_indices": indices,
                "source_label": frame["source_label"],
            }
        )
    for item in encoded["unreferenced_declarations"]:
        index = item["source_index"]
        if index in declarations and declarations[index] != item["declaration"]:
            raise ValueError("goal-local unreferenced declaration disagrees")
        declarations[index] = item["declaration"]
    count = encoded["declaration_count"]
    if set(declarations) != set(range(count)):
        raise ValueError("goal-local declaration table is incomplete")
    return {
        **encoded["metadata"],
        "declarations": [declarations[index] for index in range(count)],
        "goals": goals,
    }


class GoalLocalRenderer(Renderer):
    renderer_id = "goal_local"

    def render(self, projection: Projection) -> str:
        encoded = {
            "format": "hml-v3-goal-local-1.0.0",
            "state_before": _goal_local_state(projection["state_before"]),
            "action": projection["action"],
            "state_delta": projection["state_delta"],
            "state_after": _goal_local_state(projection["state_after"]),
        }
        return json.dumps(encoded, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"

    def parse(self, text: str) -> Projection:
        encoded = _load_object(text)
        if encoded.get("format") != "hml-v3-goal-local-1.0.0":
            raise ValueError("unknown goal-local format")
        return {
            "state_before": _from_goal_local_state(encoded["state_before"]),
            "action": encoded["action"],
            "state_delta": encoded["state_delta"],
            "state_after": _from_goal_local_state(encoded["state_after"]),
        }


def _topological_state(state: Projection) -> Projection:
    declarations = state["declarations"]
    dependencies: dict[int, set[int]] = {index: set() for index in range(len(declarations))}
    for index, declaration in enumerate(declarations):
        surface = f"{declaration['type']} {declaration['value'] or ''}"
        for prior in range(index):
            if declarations[prior]["name"] in surface:
                dependencies[index].add(prior)
    remaining = set(dependencies)
    emitted: list[int] = []
    while remaining:
        ready = sorted(
            (index for index in remaining if not (dependencies[index] & remaining)), reverse=True
        )
        if not ready:
            ready = [max(remaining)]
        for index in ready:
            emitted.append(index)
            remaining.remove(index)
    return {
        "metadata": {key: value for key, value in state.items() if key != "declarations"},
        "declarations_dependency_topological": [
            {
                "source_index": index,
                "depends_on_indices": sorted(dependencies[index]),
                "declaration": declarations[index],
            }
            for index in emitted
        ],
    }


def _from_topological_state(encoded: Projection) -> Projection:
    rows = encoded["declarations_dependency_topological"]
    indices = [item["source_index"] for item in rows]
    if set(indices) != set(range(len(rows))):
        raise ValueError("dependency-topological source indices are incomplete")
    position = {index: order for order, index in enumerate(indices)}
    for item in rows:
        if any(position[dependency] > position[item["source_index"]] for dependency in item["depends_on_indices"]):
            raise ValueError("dependency appears after its dependent declaration")
    declarations = [None] * len(rows)
    for item in rows:
        declarations[item["source_index"]] = item["declaration"]
    return {**encoded["metadata"], "declarations": declarations}


class DependencyTopologicalRenderer(Renderer):
    renderer_id = "dependency_topological"

    def render(self, projection: Projection) -> str:
        encoded = {
            "format": "hml-v3-dependency-topological-1.0.0",
            "state_before": _topological_state(projection["state_before"]),
            "action": projection["action"],
            "state_delta": projection["state_delta"],
            "state_after": _topological_state(projection["state_after"]),
        }
        return json.dumps(encoded, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"

    def parse(self, text: str) -> Projection:
        encoded = _load_object(text)
        if encoded.get("format") != "hml-v3-dependency-topological-1.0.0":
            raise ValueError("unknown dependency-topological format")
        return {
            "state_before": _from_topological_state(encoded["state_before"]),
            "action": encoded["action"],
            "state_delta": encoded["state_delta"],
            "state_after": _from_topological_state(encoded["state_after"]),
        }


class ExplicitRedundantRenderer(Renderer):
    renderer_id = "explicit_redundant_state"

    @staticmethod
    def _summary(projection: Projection) -> Projection:
        return {
            "before_goal_targets": [goal["target"] for goal in projection["state_before"]["goals"]],
            "action": projection["action"]["source_syntax"],
            "premises": projection["action"]["referenced_premises"],
            "effect_class": projection["state_delta"]["recorded_effect_class"],
            "after_goal_targets": [goal["target"] for goal in projection["state_after"]["goals"]],
        }

    def render(self, projection: Projection) -> str:
        encoded = {
            "format": "hml-v3-explicit-redundant-1.0.0",
            "transition": projection,
            "local_recap": self._summary(projection),
        }
        return json.dumps(encoded, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"

    def parse(self, text: str) -> Projection:
        encoded = _load_object(text)
        projection = encoded.get("transition")
        if encoded.get("format") != "hml-v3-explicit-redundant-1.0.0" or not isinstance(projection, dict):
            raise ValueError("unknown explicit-redundant format")
        if encoded.get("local_recap") != self._summary(projection):
            raise ValueError("explicit redundant recap disagrees with transition")
        return projection


def _minimal_state(state: Projection) -> list[Any]:
    return [
        state["source_system"],
        [
            [item["name"], item["type"], item["value"], item["binder_info"], item["scope_id"]]
            for item in state["declarations"]
        ],
        [
            [item["target"], item["status"], item["local_context_indices"], item["source_label"]]
            for item in state["goals"]
        ],
        state["metavariables"],
        state["constraints"],
        state["obligations"],
        state["dependencies"],
        state["premise_refs"],
        state["scopes"],
        state["namespace_environment_refs"],
    ]


def _from_minimal_state(row: list[Any]) -> Projection:
    if len(row) != 10:
        raise ValueError("minimal state has incorrect arity")
    return {
        "source_system": row[0],
        "declarations": [
            {"name": item[0], "type": item[1], "value": item[2], "binder_info": item[3], "scope_id": item[4]}
            for item in row[1]
        ],
        "goals": [
            {"target": item[0], "status": item[1], "local_context_indices": item[2], "source_label": item[3]}
            for item in row[2]
        ],
        "metavariables": row[3],
        "constraints": row[4],
        "obligations": row[5],
        "dependencies": row[6],
        "premise_refs": row[7],
        "scopes": row[8],
        "namespace_environment_refs": row[9],
    }


class MinimalMachineCodeRenderer(Renderer):
    renderer_id = "minimal_machine_code"

    def render(self, projection: Projection) -> str:
        action = projection["action"]
        delta = projection["state_delta"]
        encoded = [
            "H3M1",
            _minimal_state(projection["state_before"]),
            [
                action["kind"], action["target_goal_indices"], action["arguments"],
                action["substitutions"], action["source_syntax"], action["referenced_premises"],
                action["expected_effect"],
            ],
            [
                delta["declarations_added"], delta["declarations_removed"],
                delta["declarations_rebound"], delta["goals_before"], delta["goals_after"],
                delta["goals_generated"], delta["goals_solved"], delta["focused_target_changed"],
                delta["recorded_effect_class"],
            ],
            _minimal_state(projection["state_after"]),
        ]
        return json.dumps(encoded, ensure_ascii=False, separators=(",", ":")) + "\n"

    def parse(self, text: str) -> Projection:
        row = json.loads(text)
        if not isinstance(row, list) or len(row) != 5 or row[0] != "H3M1":
            raise ValueError("unknown minimal machine-code format")
        action, delta = row[2], row[3]
        if len(action) != 7 or len(delta) != 9:
            raise ValueError("minimal action/delta has incorrect arity")
        return {
            "state_before": _from_minimal_state(row[1]),
            "action": {
                "kind": action[0], "target_goal_indices": action[1], "arguments": action[2],
                "substitutions": action[3], "source_syntax": action[4],
                "referenced_premises": action[5], "expected_effect": action[6],
            },
            "state_delta": {
                "declarations_added": delta[0], "declarations_removed": delta[1],
                "declarations_rebound": delta[2], "goals_before": delta[3], "goals_after": delta[4],
                "goals_generated": delta[5], "goals_solved": delta[6],
                "focused_target_changed": delta[7], "recorded_effect_class": delta[8],
            },
            "state_after": _from_minimal_state(row[4]),
        }
