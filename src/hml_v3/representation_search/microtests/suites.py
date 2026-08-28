"""Structural-access microtests over rendered representations.

Every suite follows the same shape:

    question  -> derived from the canonical state
    answer    -> derived from the canonical state
    measured  -> how expensive the answer is to locate in R(M)

"Expensive" is deterministic and representation-independent in definition: character and
token distance from the question site to the answer site, how many competing occurrences the
reader must disambiguate between, and whether the answer is present at all.

A suite reports `unanswerable` when the rendering does not contain the information. That is
not a crash — it is the measurement. A candidate that omits dependency edges genuinely cannot
answer a dependency query, and the number that matters is how often.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import re
import statistics
from typing import Any, Callable

from hml_v3.representation_search.compiler import RepresentationCompiler
from hml_v3.representation_search.metrics import token_positions
from hml_v3.representation_search.tokenizer import tokenizer


@dataclass
class Query:
    """One structural question with its canonical ground truth."""

    kind: str
    site: str           # the token in the rendering the reader starts from
    answer: str         # the token that answers it
    #: When set, the answer only counts if it appears inside this section. A relational
    #: question ("which goals did this step solve?") is not answered by finding the goal id
    #: somewhere in the state; it is answered by the relation being stated.
    region: str | None = None
    detail: dict[str, Any] = field(default_factory=dict)


@dataclass
class SuiteResult:
    suite: str
    queries: int
    answerable: int
    mean_char_distance: float
    mean_token_distance: float
    mean_competing_occurrences: float
    max_token_distance: float
    unanswerable_rate: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "suite": self.suite,
            "queries": self.queries,
            "answerable": self.answerable,
            "unanswerable_rate": round(self.unanswerable_rate, 4),
            "mean_char_distance": round(self.mean_char_distance, 3),
            "mean_token_distance": round(self.mean_token_distance, 3),
            "mean_competing_occurrences": round(self.mean_competing_occurrences, 3),
            "max_token_distance": round(self.max_token_distance, 3),
        }

    def metrics(self) -> dict[str, float]:
        prefix = self.suite
        return {
            f"{prefix}_token_distance": round(self.mean_token_distance, 4),
            f"{prefix}_unanswerable": round(self.unanswerable_rate, 4),
            f"{prefix}_ambiguity": round(self.mean_competing_occurrences, 4),
        }


def _walk_local_references(node: Any, found: list[str]) -> None:
    if isinstance(node, dict):
        if node.get("node") == "local_reference":
            found.append(node["identity"])
        for value in node.values():
            if isinstance(value, (dict, list)):
                _walk_local_references(value, found)
    elif isinstance(node, list):
        for item in node:
            _walk_local_references(item, found)


def _walk_metavariable_references(node: Any, found: list[str]) -> None:
    if isinstance(node, dict):
        if node.get("node") == "metavariable_reference":
            found.append(node["identity"])
        for value in node.values():
            if isinstance(value, (dict, list)):
                _walk_metavariable_references(value, found)
    elif isinstance(node, list):
        for item in node:
            _walk_metavariable_references(item, found)


def _head_symbol(expr: Any) -> str | None:
    node = expr
    while isinstance(node, dict) and node.get("node") == "application":
        node = node["function"]
    if isinstance(node, dict) and node.get("node") == "symbol":
        return node["identity"]
    return None


# ------------------------------------------------------------------------ query builders


def binder_queries(transition: dict[str, Any]) -> list[Query]:
    """Which binder owns this free-variable use?"""

    queries: list[Query] = []
    for goal in transition["state_before"]["goals"]:
        used: list[str] = []
        _walk_local_references(goal["target"], used)
        declared = {d["identity"] for d in goal["local_context"]}
        for identity in dict.fromkeys(used):
            if identity in declared:
                queries.append(Query("binder", goal["identity"], identity))
    return queries


def scope_queries(transition: dict[str, Any]) -> list[Query]:
    """Which goal scopes this declaration?"""

    queries: list[Query] = []
    for goal in transition["state_before"]["goals"]:
        for declaration in goal["local_context"][:6]:
            queries.append(Query("scope", declaration["identity"], goal["identity"]))
    return queries


def dependency_queries(transition: dict[str, Any]) -> list[Query]:
    """Which declaration does this declaration's type depend on?"""

    queries: list[Query] = []
    for goal in transition["state_before"]["goals"]:
        for declaration in goal["local_context"]:
            found: list[str] = []
            _walk_local_references(declaration.get("type"), found)
            for dependency in list(dict.fromkeys(found))[:2]:
                queries.append(Query("dependency", declaration["identity"], dependency))
    return queries


def premise_queries(transition: dict[str, Any]) -> list[Query]:
    """Which premise does the action cite?"""

    action = transition["action"]
    return [
        Query("premise", "ACTION", premise, None)
        for premise in list(action["external_premise_refs"])[:4]
    ]


def goal_queries(transition: dict[str, Any]) -> list[Query]:
    """Which goal is focused, and do the after-state goals correspond to before-state ones?"""

    queries: list[Query] = []
    before = transition["state_before"]
    after = transition["state_after"]
    if before["focus_order"]:
        queries.append(Query("goal", "FOCUS", before["focus_order"][0]))
    shared = {g["identity"] for g in before["goals"]} & {g["identity"] for g in after["goals"]}
    for identity in sorted(shared)[:3]:
        queries.append(Query("goal", identity, identity, detail={"cross_state": True}))
    return queries


def type_queries(transition: dict[str, Any]) -> list[Query]:
    """What is the head symbol of this declaration's type?"""

    queries: list[Query] = []
    for goal in transition["state_before"]["goals"]:
        for declaration in goal["local_context"][:6]:
            head = _head_symbol(declaration.get("type"))
            if head:
                queries.append(Query("type", declaration["identity"], head))
    return queries


def metavar_queries(transition: dict[str, Any]) -> list[Query]:
    """Which obligation does this metavariable reference point at?"""

    queries: list[Query] = []
    declared = {m["identity"] for m in transition["state_before"]["metavariables"]}
    for goal in transition["state_before"]["goals"]:
        found: list[str] = []
        _walk_metavariable_references(goal["target"], found)
        for identity in dict.fromkeys(found):
            if identity in declared:
                queries.append(Query("metavar", goal["identity"], identity))
    return queries


def action_argument_queries(transition: dict[str, Any]) -> list[Query]:
    """Which local declaration does the action consume?"""

    return [
        Query("action_argument", "ACTION", reference["canonical_id"], "action")
        for reference in transition["action"]["local_context_refs"][:4]
        if reference.get("resolved") and reference.get("canonical_id")
    ]


def delta_queries(transition: dict[str, Any]) -> list[Query]:
    """Which goals did this step solve or create?"""

    delta = transition.get("state_delta") or {}
    queries: list[Query] = []
    for identity in (delta.get("goals_solved") or [])[:2]:
        queries.append(Query("delta", "DELTA", identity, "delta", detail={"relation": "solved"}))
    for identity in (delta.get("goals_created") or [])[:2]:
        queries.append(Query("delta", "DELTA", identity, "delta", detail={"relation": "created"}))
    return queries


BUILDERS: dict[str, Callable[[dict[str, Any]], list[Query]]] = {
    "binder_query": binder_queries,
    "scope_query": scope_queries,
    "dependency_query": dependency_queries,
    "premise_query": premise_queries,
    "goal_query": goal_queries,
    "type_query": type_queries,
    "metavar_query": metavar_queries,
    "action_argument_query": action_argument_queries,
    "delta_query": delta_queries,
}

SUITES = tuple(sorted(BUILDERS))


#: Anchors that name a *record* rather than an identity. Measuring from character 0 would
#: report "distance into the document", which is a property of document length, not of the
#: representation's structure.
RECORD_ANCHORS = {"ACTION": "action", "DELTA": "delta", "FOCUS": "focus_order"}


def _section_span(
    text: str, section_kind: str, compiler: RepresentationCompiler,
) -> tuple[int, int] | None:
    """Character extent of one section, or None when the rendering omits it.

    Sections are emitted with their role word at the start of a line, so the span runs from
    that header to the next unindented line.
    """

    word = compiler.surface.lexicon.word(section_kind)
    lines = text.split("\n")
    offset = 0
    start: int | None = None
    for line in lines:
        length = len(line) + 1
        if start is None:
            if line.strip() == word or line.strip().startswith(word + " "):
                if not line.startswith((" ", "\t")):
                    start = offset
        elif line and not line.startswith((" ", "\t")):
            return (start, offset)
        offset += length
    return (start, len(text)) if start is not None else None


def _anchor_positions(
    text: str, token: str, encoded: str | None, compiler: RepresentationCompiler,
) -> list[int]:
    role = RECORD_ANCHORS.get(token)
    if role is not None:
        word = compiler.surface.lexicon.word(role)
        found = token_positions(text, word)
        return found or [0]
    return token_positions(text, encoded or token)


def run_suite(
    compiler: RepresentationCompiler, transitions: list[dict[str, Any]], suite: str,
    max_queries: int = 240,
) -> SuiteResult:
    """Measure how expensive one class of structural question is under one representation."""

    builder = BUILDERS[suite]
    encoder = tokenizer()
    char_distances: list[float] = []
    token_distances: list[float] = []
    competing: list[float] = []
    answerable = 0
    total = 0

    for transition in transitions:
        queries = builder(transition)
        if not queries:
            continue
        rendered = compiler.render(transition)
        text = rendered.text
        codec = rendered.codec
        for query in queries:
            if total >= max_queries:
                break
            total += 1
            # Always route through the codec. It returns the input unchanged for names it
            # does not know (a premise like ``Nat.add``), so this is correct for both
            # canonical identities and global constants. An earlier version guessed which
            # was which from the presence of a colon and was wrong for every corpus whose
            # identities are short.
            answer_token = codec.encode(query.answer)
            if query.region is not None:
                span = _section_span(text, query.region, compiler)
                if span is None:
                    # The rendering has no such section, so the relation is not stated.
                    continue
                low, high = span
                answer_positions = [
                    low + position
                    for position in token_positions(text[low:high], answer_token)
                ]
            else:
                answer_positions = token_positions(text, answer_token)
            if not answer_positions:
                # The rendering does not contain the answer. That is the measurement.
                continue
            site_token = codec.encode(query.site)
            site_positions = _anchor_positions(text, query.site, site_token, compiler)
            if not site_positions:
                continue
            answerable += 1
            start = site_positions[0]
            nearest = min(answer_positions, key=lambda position: abs(position - start))
            char_gap = abs(nearest - start)
            char_distances.append(char_gap)
            token_distances.append(
                abs(encoder.count(text[min(start, nearest): max(start, nearest)]))
            )
            competing.append(len(answer_positions))
        if total >= max_queries:
            break

    return SuiteResult(
        suite=suite,
        queries=total,
        answerable=answerable,
        mean_char_distance=statistics.fmean(char_distances) if char_distances else 0.0,
        mean_token_distance=statistics.fmean(token_distances) if token_distances else 0.0,
        mean_competing_occurrences=statistics.fmean(competing) if competing else 0.0,
        max_token_distance=max(token_distances) if token_distances else 0.0,
        unanswerable_rate=(total - answerable) / total if total else 0.0,
    )


def run_all_suites(
    compiler: RepresentationCompiler, transitions: list[dict[str, Any]],
    suites: tuple[str, ...] = SUITES, max_queries: int = 240,
) -> dict[str, SuiteResult]:
    return {
        suite: run_suite(compiler, transitions, suite, max_queries)
        for suite in suites
    }
