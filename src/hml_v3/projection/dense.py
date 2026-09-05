"""Dense-target generator, second version, with truth checked rather than asserted.

`REAL_LEAN_GAP_V1 §2`. The first dense generator (`synthetic.generate_dense`) recorded the
depth it *intended* for each distractor and never re-derived it from the tree it built. It
placed the first distractor of every level as a sibling of the spine, so that distractor sat
at exactly the target's depth: the recorded answer was not the unique deepest reference on
14 to 20 of every 20 items in every cell (`FM-054`). Every number in `DENSE_TARGET.json` is
therefore a measurement of a mis-keyed question and is withdrawn.

This generator controls four things independently and verifies all of them by walking the
finished tree:

    depth        the answer's depth; the spine is exactly this long
    distinct     how many distractor identities exist
    recurrence   how many times EVERY identity occurs, the answer included -- real failing
                 states have the answer identity at depths 21, 20, 19, 18 ... as well as at
                 its maximum, so "find the deepest token" is a comparison over occurrences
    lead         how far the answer's deepest occurrence exceeds the runner-up's; the real
                 corpus is at 1 on 35 of 45 items

Sites in the target are ``(distinct + 1) * recurrence``. Every occurrence other than the
answer's deepest sits strictly above ``depth - lead`` or at it, and exactly one distractor
occurrence is placed at ``depth - lead`` so the lead is what was asked for. The association
direction of every level comes from a hash, so the answer is not a string-end token.

Truth flows one way: construction, then an independent walk, and the item is refused if the
walk disagrees with the construction.
"""

from __future__ import annotations

import hashlib
from typing import Any

from hml_v3.projection.synthetic import (GENERATOR_VERSION, SyntheticExpression, _apply,
                                         _reference, _symbol, _tag)

DENSE_VERSION = "synthetic-dense-v2.0.0"


def _h(seed: str, modulus: int) -> int:
    return int(hashlib.sha256(seed.encode()).hexdigest()[:8], 16) % max(1, modulus)


def true_depths(node: Any, depth: int = 0,
                out: dict[str, list[int]] | None = None) -> dict[str, list[int]]:
    """Every occurrence depth of every local reference, from the tree as built."""

    out = {} if out is None else out
    if isinstance(node, dict):
        if node.get("node") == "local_reference":
            out.setdefault(str(node.get("identity")), []).append(depth)
        for key in ("function", "argument", "body", "binder_type", "expression"):
            if key in node:
                true_depths(node[key], depth + 1, out)
    return out


class _Builder:
    def __init__(self) -> None:
        self.counter = 0
        self.edges: list[tuple[str, str]] = []
        self.node_reference: dict[str, str] = {}
        self.ids: dict[int, str] = {}

    def fresh(self) -> str:
        self.counter += 1
        return f"n{self.counter}"

    def reference(self, identity: str) -> dict[str, Any]:
        node = _reference(identity)
        node_id = self.fresh()
        self.ids[id(node)] = node_id
        self.node_reference[node_id] = identity
        return node

    def apply(self, function: dict[str, Any], argument: dict[str, Any]) -> dict[str, Any]:
        node = _apply(function, argument)
        node_id = self.fresh()
        self.ids[id(node)] = node_id
        for child in (function, argument):
            child_id = self.ids.get(id(child))
            if child_id is not None:
                self.edges.append((child_id, node_id))
        return node


def _hanger(builder: _Builder, leaves: list[dict[str, Any]], height: int,
            seed: str) -> dict[str, Any]:
    """A binary tree over ``leaves`` no taller than ``height``, shaped by the seed."""

    if len(leaves) == 1:
        return leaves[0]
    if height < 1 or len(leaves) > 2 ** height:
        raise ValueError("hanger cannot fit its leaves within the height bound")
    capacity = 2 ** (height - 1)
    low = max(1, len(leaves) - capacity)
    high = min(capacity, len(leaves) - 1)
    split = low + _h(f"{seed}|split|{len(leaves)}", high - low + 1)
    left = _hanger(builder, leaves[:split], height - 1, seed + "L")
    right = _hanger(builder, leaves[split:], height - 1, seed + "R")
    return builder.apply(left, right)


def generate_dense_v2(index: int, depth: int, distinct: int, recurrence: int,
                      lead: int = 1) -> SyntheticExpression:
    if depth < 3:
        raise ValueError("depth must be at least 3")
    if distinct < 2:
        raise ValueError("at least two distractor identities are needed for a question")
    if recurrence < 1:
        raise ValueError("recurrence must be at least 1")
    if not 1 <= lead <= depth - 2:
        raise ValueError("lead must leave room for at least one shallower level")

    # Identities, unique, in the synthetic experiments' naming scheme.
    names: list[str] = []
    seen: set[str] = set()
    probe = 0
    while len(names) < distinct + 1:
        candidate = _tag("v", 10 + (index * 7 + probe * 13) % 80)
        probe += 1
        if candidate not in seen:
            seen.add(candidate)
            names.append(candidate)
    target, distractors = names[0], names[1:]

    builder = _Builder()

    # Occurrence requests: the answer's extra occurrences and every distractor occurrence.
    requests = [target] * (recurrence - 1) + [d for d in distractors for _ in range(recurrence)]
    # One distractor is pinned at depth - lead so the lead is exact. Which one is hashed.
    pinned = distractors[_h(f"dense2|{index}|pin", len(distractors))]
    requests.remove(pinned)

    # Free slots live at levels 1 .. depth-1. A reference may only occupy a slot whose
    # subtree cannot reach the answer's depth: level i hosts a hanger of height at most
    # (depth - lead - i), whose leaves sit at depths i .. depth - lead. The pinned level
    # depth - lead has height 0 and takes exactly the pinned reference.
    levels = list(range(1, depth - lead))
    per_level: dict[int, list[str]] = {i: [] for i in range(1, depth)}
    per_level[depth - lead].append(pinned)
    for position, identity in enumerate(requests):
        # Spread requests over the eligible levels, weighted towards the deeper half so
        # occurrences land at a spread of depths rather than piling up near the root.
        if not levels:
            raise ValueError("no level can host a distractor at this depth and lead")
        choice = levels[_h(f"dense2|{index}|level|{position}|{identity}", len(levels))]
        if len(per_level[choice]) >= 2 ** (depth - lead - choice):
            # This level is full; take the shallowest level with room.
            for alternative in levels:
                if len(per_level[alternative]) < 2 ** (depth - lead - alternative):
                    choice = alternative
                    break
            else:
                raise ValueError("no capacity for the requested recurrence at this depth")
        per_level[choice].append(identity)

    # Build bottom-up. The answer's deepest occurrence is the only reference at ``depth``.
    bottom = builder.reference(target)
    node: dict[str, Any] = bottom
    path = [builder.ids[id(bottom)]]
    for step in range(depth):
        level = depth - step  # the free slot at this spine node sits at depth ``level``
        hosted = per_level.get(level, []) if level <= depth - 1 else []
        if hosted:
            leaves = [builder.reference(identity) for identity in hosted]
            height = depth - lead - level
            free = _hanger(builder, leaves, height, f"dense2|{index}|{level}")
        else:
            free = _symbol(f"c{level}")
        spin = _h(f"dense2|{index}|assoc|{level}", 2)
        node = builder.apply(node, free) if spin == 0 else builder.apply(free, node)
        path.append(builder.ids[id(node)])

    # Truth is re-derived from the tree, never copied from the plan.
    walked = true_depths(node)
    depth_of = {identity: max(depths) for identity, depths in walked.items()}

    context = [{
        "identity": name, "user_name_diagnostic": name, "binder_role": "EXPLICIT",
        "declaration_role": "cdecl", "value": None,
        "type": _symbol(f"t{10 + (index + position) % 40}"),
    } for position, name in enumerate(names)]
    digest = hashlib.sha256(
        f"{DENSE_VERSION}|{index}|{depth}|{distinct}|{recurrence}|{lead}".encode()
    ).hexdigest()[:12]
    state_id = f"SE_{digest}"
    transition = {
        "transition_id": state_id, "schema_version": "synthetic-1",
        "source_specific_reference": {"generator": DENSE_VERSION},
        "corpus_metadata": {"source_file": "synthetic/DenseV2.lean"},
        "provenance": {"declaration": state_id, "origin": "TYPED_GENERATOR"},
        "state_before": {"goals": [{"identity": "m0", "local_context": context,
                                    "local_instances": [], "target": node}]},
        "state_after": {"goals": []},
        "state_delta": {"goals_created": [], "goals_solved": [], "goals_modified": [],
                        "external_premises_used": []},
        "action": {"kind": "SYNTHETIC_STRUCTURAL", "external_premise_refs": [],
                   "local_context_refs": []},
    }
    expression = SyntheticExpression(
        state_id=state_id, rung=f"D{distinct}R{recurrence}", depth=depth,
        transition=transition, deepest=target,
        others=[n for n in depth_of if n != target], depth_of=depth_of,
        edges=builder.edges, node_reference=builder.node_reference,
        path_to_root=list(reversed(path)))
    problems = verify_dense(expression, distinct, recurrence, lead)
    if problems:
        raise ValueError(f"dense generator produced an invalid item: {problems}")
    return expression


def verify_dense(expression: SyntheticExpression, distinct: int, recurrence: int,
                 lead: int) -> list[str]:
    """Independent checks on the finished tree. Any failure makes the item unusable."""

    problems: list[str] = []
    target = expression.transition["state_before"]["goals"][0]["target"]
    walked = true_depths(target)
    if expression.deepest not in walked:
        return ["the answer does not occur in the target"]
    maxima = {identity: max(depths) for identity, depths in walked.items()}
    best = max(maxima.values())
    winners = [identity for identity, d in maxima.items() if d == best]
    if winners != [expression.deepest]:
        problems.append(f"deepest reference is not unique or not the answer: {winners}")
    if best != expression.depth:
        problems.append(f"answer depth {best} differs from the requested {expression.depth}")
    rivals = [d for identity, d in maxima.items() if identity != expression.deepest]
    if not rivals or best - max(rivals) != lead:
        problems.append(f"lead is {best - max(rivals) if rivals else None}, not {lead}")
    if len(maxima) != distinct + 1:
        problems.append(f"{len(maxima)} identities occur, expected {distinct + 1}")
    counts = {identity: len(depths) for identity, depths in walked.items()}
    if any(count != recurrence for count in counts.values()):
        problems.append(f"occurrence counts {counts} are not all {recurrence}")
    if maxima != expression.depth_of:
        problems.append("depth_of disagrees with the walk")
    if sum(counts.values()) != len(expression.node_reference):
        problems.append("node_reference does not list every occurrence")
    children = [child for child, _parent in expression.edges]
    if len(children) != len(set(children)):
        problems.append("a node has two parents")
    if expression.path_to_root[0] != expression.edges[-1][1]:
        problems.append("path_to_root does not start at the root")
    return problems


def sites(distinct: int, recurrence: int) -> int:
    return (distinct + 1) * recurrence
