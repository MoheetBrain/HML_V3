"""Typed generator for canonical expression structures at controlled depth.

`MISSION §11`, `§30`, `§31`. The real corpus cannot populate a depth ladder: 35 of 45
EXPRESSION_DEPTH items lead by exactly one level and the deep rungs are empty, so the
representation-by-horizon question is untestable on it. That is a `CORPUS_LIMIT`, not a
reason to abandon the question.

**Truth flows one way only** (`§31`):

    typed generator -> canonical structure -> CanonicalMathState -> ground truth

Ground truth here is known *by construction*: the generator places one reference at a known
depth and every other reference strictly shallower, so "which declaration is referenced
deepest" has a unique answer that no model, and no inference, was consulted about. No LLM
proposes, judges or validates any answer in this module.

The mathematics is deliberately trivial -- opaque symbols and applications over anonymous
declarations. `§11` asks for exactly that: keep content simple so that structural complexity,
not domain knowledge, is what varies.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from typing import Any

#: `MISSION §11`. E5 is included; whether the corpus or the reader can carry it is measured
#: rather than assumed.
LADDER: tuple[tuple[str, int, int], ...] = (
    ("E1", 1, 2), ("E2", 3, 4), ("E3", 5, 8), ("E4", 9, 16), ("E5", 17, 32),
)

GENERATOR_VERSION = "synthetic-expression-v1.0.0"


def _tag(prefix: str, index: int) -> str:
    return f"{prefix}{index}"


def _symbol(name: str) -> dict[str, Any]:
    return {"node": "symbol", "identity": name, "universe_arguments": []}


def _reference(identity: str) -> dict[str, Any]:
    return {"node": "local_reference", "identity": identity}


def _apply(function: dict[str, Any], argument: dict[str, Any]) -> dict[str, Any]:
    return {"node": "application", "function": function, "argument": argument}


@dataclass
class SyntheticExpression:
    """One generated state, with the structural truth the generator knows by construction."""

    state_id: str
    rung: str
    depth: int
    transition: dict[str, Any]
    #: The declaration referenced at the greatest nesting depth. Unique by construction.
    deepest: str
    #: Every other referenced declaration, all strictly shallower.
    others: list[str]
    #: identity -> its deepest occurrence, for the audit and for distractor difficulty.
    depth_of: dict[str, int]
    #: (child node id, parent node id) for every edge, so a projection can materialise them.
    edges: list[tuple[str, str]]
    #: node id -> the reference identity it carries, where it carries one.
    node_reference: dict[str, str]
    #: The chain from the deepest reference up to the root.
    path_to_root: list[str]

    @property
    def lead(self) -> int:
        """How far the deepest reference outranks the runner-up. Always at least 1."""

        rivals = [d for identity, d in self.depth_of.items() if identity != self.deepest]
        return self.depth - (max(rivals) if rivals else 0)

    def to_dict(self) -> dict[str, Any]:
        return {
            "state_id": self.state_id, "rung": self.rung, "depth": self.depth,
            "deepest": self.deepest, "others": self.others, "lead": self.lead,
            "depth_of": self.depth_of, "edges": [list(e) for e in self.edges],
            "node_reference": self.node_reference, "path_to_root": self.path_to_root,
            "generator": GENERATOR_VERSION, "transition": self.transition,
            "provenance": {
                "origin": "TYPED_GENERATOR",
                "truth": "KNOWN_BY_CONSTRUCTION",
                "llm_involvement": "NONE",
            },
        }


def generate(index: int, rung: str, depth: int, declarations: int = 6) -> SyntheticExpression:
    """Build one state whose deepest reference is unique and known.

    The spine is an application chain of the requested depth. The target reference sits at
    the bottom; distractors hang off the spine at strictly shallower positions, so none
    shares the target's depth.

    **The association alternates WITHIN each spine, and that is load-bearing.** A uniformly
    left-nested chain renders as ``((((v31 c5) v44) v57) v70)``, in which the deepest
    reference is always the leftmost token; "pick the leftmost" then scores 100% without
    reading any structure. Alternating direction per item is not enough either -- it only
    moves the target between the two extremes, so "pick whichever end" still scores 100%.
    The association is therefore chosen per level from a hash of the item and the level, so
    the target lands in the interior of the token string and no positional rule survives.
    Without this, NESTED_ONLY would look readable for entirely the wrong reason and every
    explicit view would be understated by comparison.
    """

    if depth < 1:
        raise ValueError("depth must be at least 1")
    if declarations < 2:
        raise ValueError("need at least two declarations to pose a question")

    names = [_tag("v", 10 + (index * 7 + i * 13) % 80) for i in range(declarations)]
    # Deduplicate while preserving order; a collision would make the answer ambiguous.
    seen: set[str] = set()
    unique: list[str] = []
    for name in names:
        if name not in seen:
            seen.add(name)
            unique.append(name)
    while len(unique) < declarations:
        candidate = _tag("v", 10 + (len(unique) * 31 + index) % 80)
        if candidate not in seen:
            seen.add(candidate)
            unique.append(candidate)
    names = unique

    target, distractors = names[0], names[1:]

    edges: list[tuple[str, str]] = []
    node_reference: dict[str, str] = {}
    depth_of: dict[str, int] = {}

    # Build bottom-up so the target sits at the deepest point of the spine.
    node_counter = [0]

    def fresh() -> str:
        node_counter[0] += 1
        return f"n{node_counter[0]}"

    bottom = fresh()
    node_reference[bottom] = target
    depth_of[target] = depth
    node: dict[str, Any] = _reference(target)
    node_ids: list[str] = [bottom]
    current = bottom
    path = [bottom]

    # Distractors are attached at levels depth-2, depth-3, ... so every one is strictly
    # shallower than the target and no two share a level where that can be avoided.
    placement: dict[int, str] = {}
    level = depth - 2
    for distractor in distractors:
        if level < 0:
            level = max(0, depth - 2)
        placement[level] = distractor
        level -= 1
        if level < 0:
            break

    for step in range(depth):
        this_level = depth - 1 - step
        parent = fresh()
        node_ids.append(parent)
        edges.append((current, parent))
        attached = placement.get(this_level)
        if attached is not None:
            leaf = fresh()
            node_ids.append(leaf)
            node_reference[leaf] = attached
            edges.append((leaf, parent))
            depth_of[attached] = this_level
            argument = _reference(attached)
        else:
            argument = _symbol(f"c{this_level}")
        # Per-level association, drawn from a hash of the item and the level, so the target
        # sits in the interior of the rendered string rather than at either end.
        spin = int(hashlib.sha256(f"assoc|{index}|{this_level}".encode()).hexdigest()[:6], 16)
        node = (_apply(node, argument) if spin % 2 == 0 else _apply(argument, node))
        current = parent
        path.append(parent)

    root = current
    referenced = [n for n in names if n in depth_of]
    others = [n for n in referenced if n != target]

    context = [{
        "identity": name, "user_name_diagnostic": name, "binder_role": "EXPLICIT",
        "declaration_role": "cdecl", "value": None,
        "type": _symbol(f"t{10 + (index + position) % 40}"),
    } for position, name in enumerate(names)]

    digest = hashlib.sha256(
        f"{GENERATOR_VERSION}|{index}|{rung}|{depth}".encode()).hexdigest()[:12]
    state_id = f"SX_{digest}"
    goal = {"identity": "m0", "local_context": context, "local_instances": [],
            "target": node}
    transition = {
        "transition_id": state_id,
        "schema_version": "synthetic-1",
        "source_specific_reference": {"generator": GENERATOR_VERSION},
        "corpus_metadata": {"source_file": "synthetic/Expression.lean"},
        "provenance": {"declaration": state_id, "origin": "TYPED_GENERATOR"},
        "state_before": {"goals": [goal]},
        "state_after": {"goals": []},
        "state_delta": {"goals_created": [], "goals_solved": [], "goals_modified": [],
                        "external_premises_used": []},
        "action": {"kind": "SYNTHETIC_STRUCTURAL", "external_premise_refs": [],
                   "local_context_refs": []},
    }

    return SyntheticExpression(
        state_id=state_id, rung=rung, depth=depth, transition=transition,
        deepest=target, others=others, depth_of=depth_of, edges=edges,
        node_reference=node_reference, path_to_root=list(reversed(path)))


def build_ladder(per_rung: int = 12, declarations: int = 6) -> list[SyntheticExpression]:
    """One ladder: ``per_rung`` states at each depth rung of `MISSION §11`."""

    out: list[SyntheticExpression] = []
    index = 0
    for rung, low, high in LADDER:
        for slot in range(per_rung):
            depth = low + (slot % max(1, high - low + 1))
            out.append(generate(index, rung, depth, declarations))
            index += 1
    return out


def verify(expression: SyntheticExpression) -> list[str]:
    """Structural checks. The generator's claims must hold, or the item is not usable.

    `§31`: synthetic data is only admissible if its truth is verifiable without asking a
    model. These are the checks that make the ground truth a fact rather than an intention.
    """

    problems: list[str] = []
    if expression.deepest not in expression.depth_of:
        problems.append("the target is not among the referenced declarations")
    rivals = [d for name, d in expression.depth_of.items() if name != expression.deepest]
    if rivals and max(rivals) >= expression.depth_of.get(expression.deepest, -1):
        problems.append("the deepest reference is not strictly deepest")
    if len(expression.others) < 1:
        problems.append("no distractor is actually referenced in the target")
    children = [child for child, _parent in expression.edges]
    if len(children) != len(set(children)):
        problems.append("a node has two parents; the expression is not a tree")
    if expression.path_to_root and expression.path_to_root[0] != expression.edges[-1][1]:
        problems.append("path_to_root does not start at the root")
    return problems


# --------------------------------------------------------------- dense target expressions

def generate_dense(index: int, depth: int, sites: int,
                   declarations: int = 6) -> SyntheticExpression:
    """A target expression that is itself large, with identities recurring at many depths.

    Every factor in the first sweep added material *around* the target and none reproduced
    the real-Lean collapse. Real failing states differ in a way none of them modelled: the
    TARGET ITSELF carries 21 to 28 reference sites, and one identity appears at depths 11, 9,
    9 and 8 rather than exactly once.

    So this generator holds the maximum depth of the answer fixed and varies how many
    reference sites the target contains and how often each identity recurs. The answer stays
    unique -- the target identity holds the strict maximum depth and every recurrence of a
    distractor is placed strictly shallower -- so the question is unchanged while the
    expression around it thickens.
    """

    if sites < 2:
        raise ValueError("a dense target needs at least two reference sites")
    names = [_tag("v", 10 + (index * 7 + i * 13) % 80) for i in range(declarations)]
    seen: set[str] = set()
    unique: list[str] = []
    for name in names:
        if name not in seen:
            seen.add(name)
            unique.append(name)
    names = unique
    target, distractors = names[0], names[1:] or [names[0]]

    node_counter = [0]

    def fresh() -> str:
        node_counter[0] += 1
        return f"n{node_counter[0]}"

    edges: list[tuple[str, str]] = []
    node_reference: dict[str, str] = {}
    depth_of: dict[str, int] = {target: depth}

    bottom = fresh()
    node_reference[bottom] = target
    node: dict[str, Any] = _reference(target)
    current = bottom
    path = [bottom]

    # Distractor recurrences are spread across every level strictly above the answer, so a
    # single identity genuinely appears many times at many depths, as in the real corpus.
    placed = 0
    for step in range(depth):
        this_level = depth - 1 - step
        parent = fresh()
        edges.append((current, parent))
        per_level = max(1, sites // max(1, depth))
        arguments: list[dict[str, Any]] = []
        for slot in range(per_level):
            if placed >= sites - 1:
                break
            pick = distractors[(index + placed) % len(distractors)]
            leaf = fresh()
            node_reference[leaf] = pick
            edges.append((leaf, parent))
            depth_of[pick] = max(depth_of.get(pick, 0), this_level)
            arguments.append(_reference(pick))
            placed += 1
        if not arguments:
            arguments = [_symbol(f"c{this_level}")]
        for argument in arguments:
            spin = int(hashlib.sha256(
                f"dense|{index}|{this_level}|{len(arguments)}".encode()).hexdigest()[:6], 16)
            node = (_apply(node, argument) if spin % 2 == 0 else _apply(argument, node))
        current = parent
        path.append(parent)

    context = [{
        "identity": name, "user_name_diagnostic": name, "binder_role": "EXPLICIT",
        "declaration_role": "cdecl", "value": None,
        "type": _symbol(f"t{10 + (index + position) % 40}"),
    } for position, name in enumerate(names)]

    digest = hashlib.sha256(
        f"{GENERATOR_VERSION}|dense|{index}|{depth}|{sites}".encode()).hexdigest()[:12]
    state_id = f"SD_{digest}"
    transition = {
        "transition_id": state_id, "schema_version": "synthetic-1",
        "source_specific_reference": {"generator": GENERATOR_VERSION},
        "corpus_metadata": {"source_file": "synthetic/Dense.lean"},
        "provenance": {"declaration": state_id, "origin": "TYPED_GENERATOR"},
        "state_before": {"goals": [{"identity": "m0", "local_context": context,
                                    "local_instances": [], "target": node}]},
        "state_after": {"goals": []},
        "state_delta": {"goals_created": [], "goals_solved": [], "goals_modified": [],
                        "external_premises_used": []},
        "action": {"kind": "SYNTHETIC_STRUCTURAL", "external_premise_refs": [],
                   "local_context_refs": []},
    }
    return SyntheticExpression(
        state_id=state_id, rung=f"D{sites}", depth=depth, transition=transition,
        deepest=target, others=[n for n in depth_of if n != target], depth_of=depth_of,
        edges=edges, node_reference=node_reference, path_to_root=list(reversed(path)))
