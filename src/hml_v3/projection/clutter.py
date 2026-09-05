"""Controlled clutter: the bridge from clean synthetic states to real Lean states.

`REAL_LEAN_GAP_V1`. The same question, the same reader and the same nested rendering score
**0.933 on clean synthetic states and 0.167 on real Lean states**. Expression depth is not
the explanation -- accuracy is flat from depth 1 to depth 17. Something else about real states
destroys structural recovery, and this module exists to find out what, one factor at a time.

Each factor is an independent knob with a ladder. The target relation is held fixed
throughout: whatever clutter is applied, the deepest reference remains unique, remains the
recorded answer, and remains strictly deeper than every distractor. A factor that cannot
preserve that is not applied.

**What is deliberately NOT assumed.** The mission is explicit that clutter must not be
presumed to be the cause before it is measured. Several of these factors may do nothing. The
result of interest is which one -- or which interaction -- reproduces the collapse, and a
finding that none of them does would send the search back to what else differs between
synthetic and real states.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import copy
import hashlib
from typing import Any

from hml_v3.projection.model_view import ViewBlock
from hml_v3.projection.synthetic import SyntheticExpression, _apply, _reference, _symbol

CLUTTER_VERSION = "clutter-v1.0.0"

CONTEXT_SIZE = "context_size"
COMPETING_EXPRESSIONS = "competing_expressions"
IDENTIFIER_CONFUSABILITY = "identifier_confusability"
REPEATED_SYMBOLS = "repeated_symbols"
TYPE_CLUTTER = "type_clutter"
GOAL_CLUTTER = "goal_clutter"
DEPENDENCY_CLUTTER = "dependency_clutter"
SCOPE_BINDER_CLUTTER = "scope_binder_clutter"
STRUCTURAL_DISTRACTORS = "structural_distractors"

FACTORS: tuple[str, ...] = (
    CONTEXT_SIZE, COMPETING_EXPRESSIONS, IDENTIFIER_CONFUSABILITY, REPEATED_SYMBOLS,
    TYPE_CLUTTER, GOAL_CLUTTER, DEPENDENCY_CLUTTER, SCOPE_BINDER_CLUTTER,
    STRUCTURAL_DISTRACTORS,
)

#: Ladders. Level 0 is always "clean", so every ladder starts from the 0.933 baseline.
LADDERS: dict[str, tuple[int, ...]] = {
    CONTEXT_SIZE: (0, 4, 8, 16, 32, 64),
    COMPETING_EXPRESSIONS: (0, 1, 2, 4, 8, 16),
    IDENTIFIER_CONFUSABILITY: (0, 1, 2),          # spread / medium / tight cluster
    REPEATED_SYMBOLS: (0, 1, 2),                  # distinct / partly shared / all identical
    TYPE_CLUTTER: (0, 1, 2, 3),                   # none / shallow / nested / deep nested
    GOAL_CLUTTER: (0, 1, 2, 4, 8),
    DEPENDENCY_CLUTTER: (0, 4, 8, 16, 32),
    SCOPE_BINDER_CLUTTER: (0, 2, 4, 8),
    STRUCTURAL_DISTRACTORS: (0, 2, 4, 8, 16),
}


@dataclass
class Clutter:
    """One point in factor space. Absent factors are clean."""

    levels: dict[str, int] = field(default_factory=dict)

    def get(self, factor: str) -> int:
        return self.levels.get(factor, 0)

    def label(self) -> str:
        active = {k: v for k, v in sorted(self.levels.items()) if v}
        return "clean" if not active else ",".join(f"{k}={v}" for k, v in active.items())

    def to_dict(self) -> dict[str, int]:
        return dict(sorted(self.levels.items()))


def _rng(seed: str, modulus: int) -> int:
    return int(hashlib.sha256(seed.encode()).hexdigest()[:8], 16) % max(1, modulus)


def _nested_type(depth: int, tag: str) -> dict[str, Any]:
    node: dict[str, Any] = _symbol(tag)
    for level in range(depth):
        node = {"node": "pi", "binder_role": "IMPLICIT",
                "domain": _symbol(f"{tag}d{level}"), "codomain": node}
    return node


def _decoy_expression(index: int, size: int, names: list[str]) -> dict[str, Any]:
    node: dict[str, Any] = _symbol(f"k{index}")
    for step in range(size):
        argument = (_reference(names[step % len(names)]) if names and step % 2 == 0
                    else _symbol(f"k{index}_{step}"))
        node = _apply(node, argument)
    return node


def apply_clutter(expression: SyntheticExpression,
                  clutter: Clutter) -> tuple[dict[str, Any], list[ViewBlock], dict[str, Any]]:
    """Return ``(target expression node, extra blocks, notes)`` under this clutter.

    The target node is returned separately because some factors modify it (structural
    distractors add occurrences inside it) while others only add material around it.
    """

    goal = copy.deepcopy(expression.transition["state_before"]["goals"][0])
    target = goal["target"]
    extra: list[ViewBlock] = []
    notes: dict[str, Any] = {"clutter_version": CLUTTER_VERSION}

    real_names = list(expression.depth_of)

    # ------------------------------------------------------------- identifier confusability
    rename: dict[str, str] = {}
    level = clutter.get(IDENTIFIER_CONFUSABILITY)
    if level:
        # Level 1 packs identities into a 20-wide band, level 2 into a 5-wide one, so the
        # reader must tell v41 from v42 rather than v13 from v70.
        width = 20 if level == 1 else 5
        base = 40
        for position, name in enumerate(sorted(real_names)):
            rename[name] = f"v{base + (position % width)}"
        # A collision would make the answer ambiguous, so widen until injective.
        while len(set(rename.values())) != len(rename):
            width += 1
            for position, name in enumerate(sorted(real_names)):
                rename[name] = f"v{base + (position % width)}"
        notes["rename"] = rename

    def rn(name: str) -> str:
        return rename.get(name, name)

    if rename:
        def rewrite(node: Any) -> None:
            if isinstance(node, dict):
                if node.get("node") == "local_reference" and node.get("identity") in rename:
                    node["identity"] = rename[node["identity"]]
                for value in node.values():
                    rewrite(value)
            elif isinstance(node, list):
                for item in node:
                    rewrite(item)
        rewrite(target)

    # ------------------------------------------------------------- structural distractors
    count = clutter.get(STRUCTURAL_DISTRACTORS)
    if count:
        # Extra occurrences of the OPTION identities, all placed strictly shallower than the
        # target's deepest occurrence so the answer stays unique. This is what the real
        # corpus looks like -- one identity appearing at depths 11, 9, 9 and 8 -- and it is
        # what made the real question ill-posed until a unique maximum was required.
        pool = [rn(n) for n in real_names if n != expression.deepest]
        if pool:
            wrapper = target
            for slot in range(count):
                pick = pool[slot % len(pool)]
                wrapper = _apply(wrapper, _reference(pick))
            target = wrapper
            notes["extra_occurrences"] = count

    # ------------------------------------------------------------------------ context size
    filler = clutter.get(CONTEXT_SIZE)
    context_rows: list[tuple[str, Any]] = [
        ("declaration", rn(d["identity"])) for d in goal.get("local_context") or []]
    type_depth = clutter.get(TYPE_CLUTTER)
    for slot in range(filler):
        tag = f"w{10 + slot}"
        if type_depth:
            context_rows.append((
                "declaration",
                f"{tag} : {_render_type(_nested_type(type_depth, f't{slot % 7}'))}"))
        else:
            context_rows.append(("declaration", tag))
    if type_depth and not filler:
        context_rows = [
            ("declaration",
             f"{name} : {_render_type(_nested_type(type_depth, f't{index % 7}'))}")
            for index, (_label, name) in enumerate(context_rows)]
    extra.append(ViewBlock("context", context_rows))
    notes["context_declarations"] = len(context_rows)

    # ------------------------------------------------------------- competing expressions
    competing = clutter.get(COMPETING_EXPRESSIONS)
    if competing:
        names = [rn(n) for n in real_names]
        rows = []
        for index in range(competing):
            size = 3 + _rng(f"{expression.state_id}|comp|{index}", 6)
            rows.append((f"expr{index}", _render_expression(
                _decoy_expression(index, size, names))))
        extra.append(ViewBlock("other_expressions", rows))
        notes["competing_expressions"] = competing

    # ------------------------------------------------------------------- repeated symbols
    shared = clutter.get(REPEATED_SYMBOLS)
    if shared:
        replacement = "op" if shared == 2 else None

        def share(node: Any) -> None:
            if isinstance(node, dict):
                if node.get("node") == "symbol":
                    name = node.get("identity", "")
                    if replacement is not None:
                        node["identity"] = replacement
                    elif isinstance(name, str) and name.startswith("c"):
                        node["identity"] = f"c{int(_rng(name, 2))}"
                for value in node.values():
                    share(value)
            elif isinstance(node, list):
                for item in node:
                    share(item)
        share(target)
        notes["repeated_symbols"] = shared

    # ------------------------------------------------------------------------ goal clutter
    goals = clutter.get(GOAL_CLUTTER)
    if goals:
        rows = []
        for index in range(goals):
            members = [f"w{10 + (index * 3 + s)}" for s in range(3)]
            rows.append((f"g{index + 2}", members))
        extra.append(ViewBlock("other_goals", rows))
        notes["other_goals"] = goals

    # ------------------------------------------------------------------ dependency clutter
    dependencies = clutter.get(DEPENDENCY_CLUTTER)
    if dependencies:
        pool = [rn(n) for n in real_names] + [f"w{10 + i}" for i in range(max(4, filler))]
        rows = []
        for index in range(dependencies):
            left = pool[index % len(pool)]
            right = pool[(index * 3 + 1) % len(pool)]
            if left != right:
                rows.append(("depends", f"{left} <- {right}"))
        extra.append(ViewBlock("unrelated_dependencies", rows))
        notes["dependency_edges"] = len(rows)

    # --------------------------------------------------------------- scope / binder clutter
    scopes = clutter.get(SCOPE_BINDER_CLUTTER)
    if scopes:
        rows = []
        for index in range(scopes):
            binders = " ".join(f"b{index}_{s}" for s in range(1 + index % 3))
            rows.append((f"scope{index}", f"binders [{binders}] over w{10 + index}"))
        extra.append(ViewBlock("unrelated_scopes", rows))
        notes["scopes"] = scopes

    return target, extra, notes


def _render_type(node: Any) -> str:
    if not isinstance(node, dict):
        return str(node)
    if node.get("node") == "symbol":
        return str(node.get("identity"))
    if node.get("node") == "pi":
        return f"({_render_type(node.get('domain'))} -> {_render_type(node.get('codomain'))})"
    return str(node.get("node"))


def _render_expression(node: Any) -> str:
    if not isinstance(node, dict):
        return str(node)
    kind = node.get("node")
    if kind in ("local_reference", "symbol"):
        return str(node.get("identity"))
    if kind == "application":
        return (f"({_render_expression(node.get('function'))} "
                f"{_render_expression(node.get('argument'))})")
    return str(kind)


def answer_still_unique(expression: SyntheticExpression, clutter: Clutter,
                        target: dict[str, Any], notes: dict[str, Any]) -> bool:
    """The clutter must not have made the recorded answer wrong or ambiguous.

    Structural distractors add occurrences of other identities; every one is added ABOVE the
    original target node, so it is strictly shallower. This re-derives depth from the mutated
    tree and checks that rather than trusting the construction.
    """

    depths: dict[str, int] = {}

    def walk(node: Any, depth: int) -> None:
        if isinstance(node, dict):
            if node.get("node") == "local_reference":
                identity = str(node.get("identity"))
                depths[identity] = max(depths.get(identity, 0), depth)
            for key in ("function", "argument", "domain", "codomain", "body"):
                if key in node:
                    walk(node[key], depth + 1)
        elif isinstance(node, list):
            for item in node:
                walk(item, depth + 1)

    walk(target, 0)
    if not depths:
        return False
    rename = notes.get("rename") or {}
    answer = rename.get(expression.deepest, expression.deepest)
    if answer not in depths:
        return False
    best = max(depths.values())
    winners = [name for name, d in depths.items() if d == best]
    return winners == [answer]
