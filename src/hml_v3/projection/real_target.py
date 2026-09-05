"""Real Lean EXPRESSION_DEPTH items as a projection source.

`REAL_LEAN_GAP_V1 §1`. The 0.167 result was measured on `micro_dev_v2` through the TYPED_AST
control's full document -- goal, context, metavariables, action, state-after -- and the
items were never inspected mechanically after the fact. This module makes them inspectable:
it loads the items, isolates the rendered goal target, recovers the depth of every reference
from the rendered text alone, and renders the same canonical target in the parenthesised
form the synthetic experiments use, so the real target can be shown on its own.

Two depth notions are kept apart on purpose:

    key depth        ``len(path)`` over the canonical tree, which is what keyed the answer
    rendered depth   nesting counted in the text the reader actually saw

An item is only valid if they agree on which option is deepest. `FM-047` and `FM-051` were
both cases of an answer key that described a document other than the one on the page.
"""

from __future__ import annotations

import gzip
import glob
import re
from pathlib import Path
from typing import Any

from hml_v3.micromath import instruments_v2 as IV2
from hml_v3.micromath import stresses as S

#: Canonical child keys that carry a subexpression. One step down any of them is one level
#: of nesting, in the key and in every rendering here.
CHILD_KEYS: tuple[str, ...] = ("function", "argument", "body", "binder_type", "expression")


def load_expression_depth_items(lab: Path) -> list[IV2.MicroItem]:
    """All EXPRESSION_DEPTH dev items, in the order the certification consumed them."""

    rows: list[dict[str, Any]] = []
    for path in sorted(glob.glob(str(lab / "micro_dev_v2.part-*.jsonl.gz"))):
        with gzip.open(path, "rt") as handle:
            for line in handle:
                if line.strip():
                    rows.append(__import__("json").loads(line))
    items = [IV2.MicroItem.from_dict(r) for r in rows if r["stress"] == S.EXPRESSION_DEPTH]
    return sorted(items, key=lambda i: i.item_id)


def goal_target(item: IV2.MicroItem) -> dict[str, Any]:
    return item.state["state_before"]["goals"][0]["target"]


def key_depths(target: Any) -> dict[str, int]:
    """identity -> deepest key depth, exactly as `instruments_v2.build_expression_depth`."""

    out: dict[str, int] = {}
    for path, identity in S.local_references(target):
        out[identity] = max(out.get(identity, 0), len(path))
    return out


def occurrence_depths(target: Any) -> dict[str, list[int]]:
    out: dict[str, list[int]] = {}
    for path, identity in S.local_references(target):
        out.setdefault(identity, []).append(len(path))
    return out


# ------------------------------------------------------------------ rendered depth

def first_target_line(rendered_text: str) -> str:
    """The first goal's ``tgt:`` line in a TYPED_AST document."""

    match = re.search(r"^\s*tgt: (.*)$", rendered_text, re.M)
    return match.group(1) if match else ""


def brace_depths(line: str) -> dict[str, list[int]]:
    """Depth of every ``{fv|X}`` token in a TYPED_AST expression, counted by braces.

    The token's own opening brace is included, so a reference at key depth ``d`` reads at
    brace depth ``d + 1``. The audit compares orderings, not raw numbers, and reports the
    offset it found rather than assuming it.
    """

    out: dict[str, list[int]] = {}
    depth = 0
    for index, char in enumerate(line):
        if char == "{":
            depth += 1
            match = re.match(r"\{fv\|([A-Za-z0-9_]+)\}", line[index:])
            if match:
                out.setdefault(match.group(1), []).append(depth)
        elif char == "}":
            depth -= 1
    return out


def render_paren(node: Any) -> str:
    """The synthetic experiments' nested rendering, extended to every real node kind.

    One pair of parentheses per canonical node, so parenthesis depth equals key depth
    exactly. Binder types are kept because they are part of the tree the key walks; a
    rendering that dropped them would put the reader and the key in different trees.
    """

    if not isinstance(node, dict):
        return str(node)
    kind = node.get("node")
    if kind in ("local_reference", "symbol", "metavariable_reference"):
        return str(node.get("identity"))
    if kind == "bound_variable":
        return f"#{node.get('index')}"
    if kind == "literal":
        return str(node.get("value"))
    if kind == "application":
        return f"({render_paren(node.get('function'))} {render_paren(node.get('argument'))})"
    if kind in ("lambda", "dependent_function"):
        head = "fun" if kind == "lambda" else "pi"
        return (f"({head} {render_paren(node.get('binder_type'))} "
                f"{render_paren(node.get('body'))})")
    if kind == "annotated":
        return f"(ann {render_paren(node.get('expression'))})"
    return str(kind)


def paren_depths(text: str) -> dict[str, list[int]]:
    """Depth of every bare identifier token in a parenthesised rendering."""

    out: dict[str, list[int]] = {}
    depth = 0
    token = ""
    for char in text + " ":
        if char == "(":
            depth += 1
        elif char == ")":
            if token:
                out.setdefault(token, []).append(depth)
                token = ""
            depth -= 1
        elif char == " ":
            if token:
                out.setdefault(token, []).append(depth)
                token = ""
        else:
            token += char
    return out


def context_depths(item: IV2.MicroItem) -> dict[str, int]:
    """identity -> deepest key depth at which it occurs inside any context declaration's type.

    The real document renders these types beside the target, and several are near-copies
    of it. Whether an option sits deeper in one of them than in the target is a property
    of the regime the reader faced, and the audit records it.
    """

    out: dict[str, int] = {}
    for declaration in item.state["state_before"]["goals"][0].get("local_context") or []:
        for path, identity in S.local_references(declaration.get("type")):
            out[identity] = max(out.get(identity, 0), len(path))
    return out
