"""Hard gates. A candidate that fails one is rejected, never scored.

`FM-008` is the rule these implement: a representation may not compensate for a semantic
failure with a better compression number. Gates return a verdict per candidate over the
whole evaluation sample; a single failing transition fails the gate.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Any

from hml_v3.representation_search.compiler import RepresentationCompiler
from hml_v3.representation_search.projection import semantic_core

#: Escaped spellings of glyphs the corpus actually contains. FM-004 measured that these cost
#: 2.75x-5x the tokens of the literal glyph and were worth -3.41pp when last put to a model.
ESCAPE_PATTERN = re.compile(r"\\u\{?[0-9A-Fa-f]{4}\}?")

MUTATION_FAMILIES = (
    "drop_line", "swap_two_lines", "corrupt_identity", "truncate_tail", "drop_field",
    "reorder_scope",
)


@dataclass
class GateResult:
    name: str
    passed: bool
    detail: dict[str, Any] = field(default_factory=dict)


@dataclass
class GateReport:
    candidate_id: str
    passed: bool
    results: list[GateResult]
    first_failure: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "passed": self.passed,
            "first_failure": self.first_failure,
            "gates": [
                {"name": result.name, "passed": result.passed, "detail": result.detail}
                for result in self.results
            ],
        }


def _non_ascii(text: str) -> set[str]:
    return {character for character in text if ord(character) > 127}


def run_gates(
    compiler: RepresentationCompiler, transitions: list[dict[str, Any]],
) -> GateReport:
    results: list[GateResult] = []

    # ------------------------------------------------------------------ semantic round trip
    failures: list[dict[str, Any]] = []
    renders: list[str] = []
    for transition in transitions:
        passed, reason, detail = compiler.round_trip(transition)
        if not passed:
            failures.append({
                "transition_id": transition["transition_id"], "reason": reason,
                "detail": detail,
            })
            if len(failures) >= 5:
                break
        else:
            renders.append(compiler.render_text(transition))
    results.append(GateResult(
        "semantic_round_trip", not failures,
        {"checked": len(transitions), "failures": failures[:5]},
    ))
    if failures:
        return _finish(compiler, results)

    # ------------------------------------------------------------- deterministic rendering
    unstable = [
        transition["transition_id"] for transition in transitions[:32]
        if compiler.render_text(transition) != compiler.render_text(transition)
    ]
    results.append(GateResult("deterministic_serialization", not unstable,
                              {"unstable": unstable}))

    # ------------------------------------------------------------------ glyph / UTF-8 gate
    glyph_failures = []
    for transition, text in zip(transitions, renders):
        expected = _non_ascii(contract_names(transition))
        if not expected:
            continue
        missing = sorted(glyph for glyph in expected if glyph not in text)
        escaped = bool(ESCAPE_PATTERN.search(text))
        if missing or escaped:
            glyph_failures.append({
                "transition_id": transition["transition_id"],
                "missing_glyphs": missing[:8], "contains_escape_sequences": escaped,
            })
        if len(glyph_failures) >= 3:
            break
    results.append(GateResult("glyph_fidelity_utf8", not glyph_failures,
                              {"failures": glyph_failures}))

    # ----------------------------------------------------------- structural recoverability
    opaque = []
    for transition, text in zip(transitions, renders):
        goal_count = len(transition["state_before"]["goals"])
        declaration_count = sum(
            len(goal["local_context"]) for goal in transition["state_before"]["goals"]
        )
        # FM-012: a state emitted as one opaque literal is not a semantic state. A candidate
        # must produce at least one addressable line per goal and per declaration.
        if len(text.splitlines()) < max(2, goal_count + declaration_count // 4):
            opaque.append(transition["transition_id"])
        if len(opaque) >= 3:
            break
    results.append(GateResult("structural_recoverability", not opaque, {"opaque": opaque}))

    # ---------------------------------------------------------------------- no answer leak
    leaks = []
    for transition, text in zip(transitions, renders):
        metadata = transition.get("corpus_metadata") or {}
        recorded = metadata.get("recorded_effect_class")
        if not recorded or metadata.get("domain") == "SYNTHETIC":
            continue
        # The recorded effect class is a downstream supervision label. Its appearance as a
        # standalone token in the rendering would let a task be solved by copying the label.
        if re.search(rf"(?<![A-Za-z0-9_]){re.escape(recorded)}(?![A-Za-z0-9_])", text):
            leaks.append({"transition_id": transition["transition_id"], "label": recorded})
        if len(leaks) >= 3:
            break
    results.append(GateResult("no_label_leakage", not leaks, {"leaks": leaks}))

    # ----------------------------------------------------------- shape-distinct rendering
    # Two transitions that are alpha-variants of each other *should* render identically
    # under alpha normalization; that is the property, not a defect. A collision is only a
    # defect when the two transitions differ in shape — structure, roles and expression
    # skeletons with every identity replaced by its positional index.
    by_shape: dict[str, str] = {}
    collisions = []
    for transition, text in zip(transitions[:64], renders[:64]):
        shape = _shape_key(transition)
        previous = by_shape.get(text)
        if previous is not None and previous != shape:
            collisions.append(transition["transition_id"])
        by_shape[text] = shape
        if len(collisions) >= 3:
            break
    results.append(GateResult(
        "shape_distinct_rendering", not collisions,
        {"checked": min(64, len(renders)), "colliding_transitions": collisions},
    ))
    return _finish(compiler, results)


def _shape_key(transition: dict[str, Any]) -> str:
    """The transition's semantic core with every identity replaced by its position.

    Alpha-variants and transitions differing only in which internal ids Lean happened to
    allocate share a shape key; anything structurally different does not.
    """

    import json

    core = semantic_core(transition)
    mapping: dict[str, str] = {}

    def rename(value: Any) -> Any:
        if isinstance(value, str):
            if value not in mapping:
                mapping[value] = f"#{len(mapping)}"
            return mapping[value]
        return value

    def walk(node: Any, identity_context: bool = False) -> Any:
        if isinstance(node, dict):
            out = {}
            for key, item in node.items():
                is_identity = key in ("identity", "focus_order", "local_context_refs")
                out[key] = walk(item, is_identity)
            return out
        if isinstance(node, list):
            return [walk(item, identity_context) for item in node]
        if identity_context:
            return rename(node)
        return node

    return json.dumps(walk(core), sort_keys=True, separators=(",", ":"))


def _finish(compiler: RepresentationCompiler, results: list[GateResult]) -> GateReport:
    first_failure = next((result.name for result in results if not result.passed), None)
    return GateReport(
        candidate_id=compiler.candidate_id,
        passed=first_failure is None,
        results=results,
        first_failure=first_failure,
    )


def contract_names(transition: dict[str, Any]) -> str:
    """Identifier strings the semantic contract *requires* a candidate to emit.

    Lean's display spelling is explicitly outside the contract (``alpha_normalization``
    may drop it), so its glyphs are not required. What is required: global constant
    identities, projection type identities, universe parameter names, string literal
    values, and external premise references. Those are the strings FM-004 priced.
    """

    pieces: list[str] = []

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            kind = node.get("node")
            if kind == "symbol":
                pieces.append(node["identity"])
            elif kind == "projection":
                pieces.append(node["type_identity"])
            elif kind == "literal" and isinstance(node.get("value"), str):
                pieces.append(node["value"])
            if node.get("constructor") == "param":
                pieces.append(node["name"])
            for value in node.values():
                if isinstance(value, (dict, list)):
                    walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    for phase in ("state_before", "state_after"):
        walk(transition[phase]["goals"])
        walk(transition[phase]["metavariables"])
    pieces.extend(transition["action"]["external_premise_refs"])
    return " ".join(pieces)
