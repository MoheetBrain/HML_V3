"""Strip semantic priors from a canonical state without changing its structure.

`FM-041`: four instruments were invalid because the answer stayed recoverable from the
identifiers after the relation was destroyed. ``n : Nat`` does not need a TYPE relation to
answer "what is the type of n" -- the name carries it. Transposition equalises the token
multiset; it does not equalise plausibility.

`MISSION §4`: replace names that could reveal the answer with opaque tags -- ``v17``, ``t4``,
``h12``, ``p3`` -- so that recovering the relation requires reading the relation.

Two rules govern what may be renamed.

**A rename must be a bijection within the state.** Two declarations that were distinct stay
distinct, and every use site moves with its declaration, or the state stops being
well-formed and the question stops having an answer.

**A rename must not destroy the relation under test.** The anonymiser removes *priors*, not
*structure*. It never touches the edge the instrument is asking about; that is `ablate`'s
job, and confusing the two would make every negative arm look valid for the wrong reason.
"""

from __future__ import annotations

import copy
import hashlib
from typing import Any

from hml_v3.micromath import stresses as S

#: Opaque tag families. Distinct prefixes per role so a reader can still tell a declaration
#: from a type from a premise -- that distinction is structural, not a prior.
TERM_PREFIX = "v"
HYP_PREFIX = "h"
TYPE_PREFIX = "t"
PREMISE_PREFIX = "p"
GOAL_PREFIX = "g"

#: Names that carry no subject-matter prior and whose removal would make states unreadable.
STRUCTURAL_KEEP = frozenset({
    "Prop", "Type", "Sort", "forall", "fun", "let", "->",
})


def _stable_index(name: str, salt: str, modulus: int) -> int:
    digest = hashlib.sha256(f"{salt}|{name}".encode()).hexdigest()
    return int(digest[:8], 16) % modulus


def _tag(name: str, salt: str, prefix: str, used: set[str], population: int) -> str:
    """A collision-free opaque tag, with a space that always exceeds the population.

    The first version fixed the space at 90 and probed with ``index % 99 + 10``. With more
    than 90 names to tag -- which a same-domain premise pool comfortably exceeds -- every
    probe hit an occupied slot and the loop never terminated. The space is now sized from
    the population, and probing is linear over that space so it is guaranteed to finish.
    """

    span = max(90, 4 * max(1, population))
    start = _stable_index(name, f"{salt}|{prefix}", span)
    for step in range(span):
        tag = f"{prefix}{10 + (start + step) % span}"
        if tag not in used:
            used.add(tag)
            return tag
    raise RuntimeError("tag space exhausted despite being sized from the population")


def _is_hypothesis(declaration: dict[str, Any]) -> bool:
    """A declaration whose type is a proposition reads as a hypothesis to a mathematician."""

    node = declaration.get("type") or {}
    if isinstance(node, dict) and node.get("node") == "sort":
        return False
    diagnostic = declaration.get("user_name_diagnostic") or ""
    return diagnostic.startswith("h") or declaration.get("declaration_role") == "ldecl"


def declaration_tags(state: dict[str, Any], salt: str = "") -> dict[str, str]:
    """Map every local declaration identity in the state to an opaque tag.

    Numbering is drawn from a hash rather than from position, so the tag ordering carries no
    information about declaration order -- ``v3`` before ``v17`` says nothing about which
    came first, and a reader cannot recover the answer from a monotone sequence.
    """

    tags: dict[str, str] = {}
    used: set[str] = set()
    population = sum(len(g.get("local_context") or []) for g in (state.get("goals") or []))
    for goal in state.get("goals") or []:
        for declaration in goal.get("local_context") or []:
            identity = declaration.get("identity")
            if not isinstance(identity, str) or identity in tags:
                continue
            prefix = HYP_PREFIX if _is_hypothesis(declaration) else TERM_PREFIX
            tags[identity] = _tag(identity, f"{salt}|decl", prefix, used, population)
    return tags


def symbol_tags(state: dict[str, Any], salt: str = "",
                prefix: str = TYPE_PREFIX) -> dict[str, str]:
    """Map external symbol identities to opaque tags, skipping structural keywords."""

    tags: dict[str, str] = {}
    used: set[str] = set()
    names: list[str] = ["Sort"]
    tags["Sort"] = ""
    for _path, node in S.walk(state.get("goals")):
        if isinstance(node, dict) and node.get("node") == "symbol":
            name = node.get("identity") or node.get("name")
            if isinstance(name, str) and name not in STRUCTURAL_KEEP and name not in tags:
                names.append(name)
                tags[name] = ""
    for name in names:
        tags[name] = _tag(name, f"{salt}|sym", prefix, used, len(names))
    return tags


def premise_tags(action: dict[str, Any], candidates: list[str],
                 salt: str = "") -> dict[str, str]:
    """Map premise names to opaque tags.

    ``Nat.le_add_right`` announces its own subject. A reader can pick it out of a list
    without reading which premise the action cites, which is precisely why the PREMISE
    negative arm scored 0.875.
    """

    tags: dict[str, str] = {}
    used: set[str] = set()
    names = sorted(set(candidates) | set(action.get("external_premise_refs") or []))
    for name in names:
        tags[name] = _tag(name, f"{salt}|prem", PREMISE_PREFIX, used, len(names))
    return tags


# ------------------------------------------------------------------------- application

def apply(transition: dict[str, Any], *, rename_declarations: bool = True,
          rename_symbols: bool = False, rename_premises: bool = False,
          premise_pool: list[str] | None = None,
          salt: str = "") -> tuple[dict[str, Any], dict[str, dict[str, str]]]:
    """Return an anonymised copy of the transition and the maps that produced it.

    The rewrite walks the **whole record**, not just ``state_before``. The identity codec is
    built across both phases, the delta section is rendered from ``state_delta``, and
    ``local_instances`` carries class names outside the ``symbol`` node kind -- so a rewrite
    confined to one phase produces a page where one declaration wears two names. That is
    both inconsistent and a fresh shortcut, which is the opposite of the point.

    Which families are renamed is a per-instrument decision: TYPE needs the type symbols and
    the human diagnostics gone, PREMISE needs the lemma names gone, BINDER only needs opaque
    declarations. Renaming more than an instrument requires costs readability for no gain in
    validity, so each caller asks for what it needs.
    """

    out = copy.deepcopy(transition)
    maps: dict[str, dict[str, str]] = {}
    state = out.get("state_before") or {}

    decl_map = declaration_tags(state, salt) if rename_declarations else {}
    sym_map = symbol_tags(state, salt) if rename_symbols else {}
    prem_map: dict[str, str] = {}
    if rename_premises:
        # `MISSION §21`: distractors must be plausible same-domain premises, so the pool of
        # real lemma names is tagged into the SAME p-family as the answer. Tagging only what
        # this state cites would leave the answer as the only p-tag on the page -- a louder
        # shortcut than the name it was meant to hide.
        prem_map = premise_tags(out.get("action") or {},
                                list(premise_pool or _ambient_symbols(state)), salt)

    def rewrite(node: Any) -> None:
        if isinstance(node, dict):
            kind = node.get("node")
            if kind == "local_reference" and node.get("identity") in decl_map:
                node["identity"] = decl_map[node["identity"]]
            elif kind == "symbol":
                name = node.get("identity") or node.get("name")
                if name in sym_map and sym_map[name]:
                    node["identity"] = sym_map[name]
            # `local_instances` names its class outside the symbol node kind.
            klass = node.get("class_identity")
            if isinstance(klass, str) and sym_map.get(klass):
                node["class_identity"] = sym_map[klass]
            for value in node.values():
                rewrite(value)
        elif isinstance(node, list):
            for item in node:
                rewrite(item)

    for phase in ("state_before", "state_after"):
        phase_state = out.get(phase) or {}
        for goal in phase_state.get("goals") or []:
            for declaration in goal.get("local_context") or []:
                identity = declaration.get("identity")
                if identity in decl_map:
                    declaration["identity"] = decl_map[identity]
                # The diagnostic name is the loudest prior in the record: a human chose it
                # to be evocative. It goes whenever anything is renamed.
                if decl_map or sym_map:
                    declaration["user_name_diagnostic"] = declaration.get("identity")
        rewrite(phase_state)

    action = out.get("action") or {}
    if prem_map:
        action["external_premise_refs"] = [
            prem_map.get(name, name)
            for name in (action.get("external_premise_refs") or [])]
        delta = out.get("state_delta") or {}
        if isinstance(delta.get("external_premises_used"), list):
            delta["external_premises_used"] = [
                prem_map.get(name, name) for name in delta["external_premises_used"]]
    if decl_map:
        for reference in action.get("local_context_refs") or []:
            canonical = reference.get("canonical_id")
            if isinstance(canonical, str):
                head, _sep, tail = canonical.rpartition(":")
                if tail in decl_map:
                    reference["canonical_id"] = f"{head}:{decl_map[tail]}"

    maps["declarations"] = decl_map
    maps["symbols"] = {k: v for k, v in sym_map.items() if v}
    maps["premises"] = prem_map
    return out, maps


def _ambient_symbols(state: dict[str, Any]) -> set[str]:
    names: set[str] = set()
    for _path, node in S.walk(state.get("goals")):
        if isinstance(node, dict) and node.get("node") == "symbol":
            name = node.get("identity") or node.get("name")
            if isinstance(name, str):
                names.add(name)
    return names


def leaks_answer(options: list[str], answer: str) -> bool:
    """True when the answer is guessable from the option strings alone.

    A crude but load-bearing check: if the answer is the only option carrying a dotted
    namespace, or the only one of its prefix family, then the option set itself is the
    shortcut and no amount of state anonymisation will save the cell.
    """

    if answer not in options or len(options) < 2:
        return True
    dotted = [o for o in options if "." in o]
    if dotted == [answer]:
        return True
    families = {}
    for option in options:
        head = option[0] if option else ""
        families.setdefault(head, []).append(option)
    return families.get(answer[0] if answer else "", []) == [answer] and len(families) > 1
