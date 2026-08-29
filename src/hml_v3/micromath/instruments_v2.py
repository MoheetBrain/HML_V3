"""V2 instruments: anonymised states, plausible distractors, state-level negative arms.

Three changes from V1, each aimed at one measured failure.

**Anonymised identifiers** (`MISSION §4`). ``n : Nat`` is answerable without the TYPE
relation. Declarations become ``v17``/``h4``, types become ``t23``, premises become ``p8``,
so the only route to the answer is the relation itself.

**Plausible distractors** (`MISSION §5`). Every option is drawn from the same state, carries
the same tag family as the answer, and is individually a sensible answer to the question. A
distractor that is obviously wrong is not a distractor; it is a hint.

**State-level negative arms** (`MISSION §7`). The relation is destroyed in the state by
`ablate`, not contradicted in the prompt. V1 prepended a decoy and left the relation in the
text, so the reader read past it.

Every option appears in the rendering, so the token-multiset argument that justified the V1
transposition design still holds: no option can be picked out by length, frequency or
position. `shortcut_controls` re-verifies that empirically rather than on trust.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
from typing import Any, Callable

from hml_v3.micromath import ablate, anonymise
from hml_v3.micromath import stresses as S

LAB_VERSION = "micromath-lab-v2.0.0"

#: Target option count. `MISSION §6`: four plausible choices where they help, never at the
#: cost of new leakage, and never fewer than two.
TARGET_OPTIONS = 4
MINIMUM_OPTIONS = 2

#: How the positive control states the relation outright. `MISSION §25` wants this arm to be
#: close to trivial, so the phrasing is a bare machine-style fact, not a sentence.
POSITIVE_HEADER: dict[str, str] = {
    S.BINDER: "USE_OWNER",
    S.SCOPE: "SCOPE_OWNER",
    S.TYPE: "TYPE_OF",
    S.DEPENDENCY: "DEPENDS_ON",
    S.PREMISE: "ACTION_REQUIRES",
    S.ACTION_ARGUMENT: "ACTION_ARG",
    S.MULTI_GOAL: "ACTION_GOAL",
    S.EXPRESSION_DEPTH: "DEEPEST_REFERENCE",
}


class NotEligible(RuntimeError):
    """This transition cannot carry a valid item for this stress."""


@dataclass
class MicroItem:
    item_id: str
    domain: str
    domain_confidence: str
    stress: str
    base_transition_id: str
    source_file: str
    question: str
    options: tuple[str, ...]
    answer: str
    relation: str
    state: dict[str, Any]
    ablated: dict[str, Any]
    detail: dict[str, Any] = field(default_factory=dict)

    @property
    def chance(self) -> float:
        return 1.0 / len(self.options)

    @property
    def cell(self) -> tuple[str, str]:
        return (self.domain, self.stress)

    def to_dict(self) -> dict[str, Any]:
        return {
            "item_id": self.item_id, "domain": self.domain,
            "domain_confidence": self.domain_confidence, "stress": self.stress,
            "base_transition_id": self.base_transition_id, "source_file": self.source_file,
            "question": self.question, "options": list(self.options), "answer": self.answer,
            "relation": self.relation, "chance": self.chance,
            "lab_version": LAB_VERSION,
            "provenance": {
                "state": "REAL_LEAN_DERIVED_BASE_ANONYMISED",
                "ablated": "STRUCTURAL_RELATION_ABLATION_NEGATIVE_CONTROL"},
            "detail": self.detail, "state": self.state, "ablated": self.ablated,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "MicroItem":
        return cls(
            item_id=payload["item_id"], domain=payload["domain"],
            domain_confidence=payload["domain_confidence"], stress=payload["stress"],
            base_transition_id=payload["base_transition_id"],
            source_file=payload["source_file"], question=payload["question"],
            options=tuple(payload["options"]), answer=payload["answer"],
            relation=payload["relation"], state=payload["state"],
            ablated=payload["ablated"], detail=payload.get("detail", {}))


#: What a renderer actually consumes. ``state_after`` is required -- the identity codec is
#: built over both phases and a transition without it cannot be rendered at all -- so it
#: stays, and is anonymised under the same maps as ``state_before``. Rendering a real before
#: state beside an un-anonymised after state would show ``v17`` in one and ``f6`` in the
#: other, which is both inconsistent and a fresh leak. What is dropped is only the material
#: no renderer reads: corpus metadata and the raw delta record.
#: Only ``corpus_metadata`` is dropped: it is provenance the renderer never reads, and the
#: domain is captured from it before pruning. Everything else stays, because the projection
#: needs both phases and the delta to build a document at all.
DROPPED_FIELDS = ("corpus_metadata",)


def prune(transition: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in transition.items() if key not in DROPPED_FIELDS}


def item_id(domain: str, stress: str, transition_id: str) -> str:
    digest = hashlib.sha256(
        f"{LAB_VERSION}|{domain}|{stress}|{transition_id}".encode()).hexdigest()
    return f"MI_{digest[:12]}"


def _seed(transition_id: str) -> int:
    return int(hashlib.sha256(transition_id.encode()).hexdigest()[:8], 16)


def _choose_distractors(answer: str, pool: list[str], seed: int,
                        want: int = TARGET_OPTIONS) -> tuple[str, ...]:
    """Pick distractors deterministically and spread through the pool.

    Taking the first N would systematically favour whatever the state happens to declare
    early, which is a positional prior of exactly the kind this lab is supposed to exclude.
    """

    candidates = [c for c in pool if c != answer]
    if len(candidates) < MINIMUM_OPTIONS - 1:
        raise NotEligible(f"only {len(candidates)} distractors available")
    stride = max(1, len(candidates) // max(1, want - 1))
    picked: list[str] = []
    index = seed % len(candidates)
    while len(picked) < min(want - 1, len(candidates)):
        candidate = candidates[index % len(candidates)]
        if candidate not in picked:
            picked.append(candidate)
        index += stride if stride > 1 else 1
    chosen = sorted({answer, *picked})
    if len(chosen) < MINIMUM_OPTIONS:
        raise NotEligible("fewer than two distinct options")
    # Presenting the options in sorted order made position informative: BINDER answers tend
    # to carry higher tags, so "always take the last option" scored 0.447 against chance
    # 0.277. The order is a deterministic rotation instead -- stable and reproducible, but
    # carrying nothing about which option is correct.
    #
    # The rotation is keyed on a SEPARATE hash of the seed, not the seed itself. Reusing one
    # seed for both the content choice and the ordering made them perfectly correlated: on
    # two-goal SCOPE items the owner index and the rotation offset were both ``seed % 2``,
    # so the answer landed first every single time and "always take the first option" scored
    # 1.000. Two independent decisions need two independent draws.
    spin = int(hashlib.sha256(f"order|{seed}".encode()).hexdigest()[:8], 16)
    offset = spin % len(chosen)
    return tuple(chosen[offset:] + chosen[:offset])


# ------------------------------------------------------------------------------- builders
# Each returns (question, options, answer, relation, detail) against an ALREADY anonymised
# transition, plus the anonymisation flags it needs.

def _goal(transition: dict[str, Any], index: int = 0) -> dict[str, Any]:
    return transition["state_before"]["goals"][index]


def _type_head(node: Any) -> str | None:
    """The outermost symbol naming a type -- what a reader would call 'the type'."""

    if isinstance(node, dict):
        if node.get("node") == "symbol":
            name = node.get("identity") or node.get("name")
            return name if isinstance(name, str) else None
        if node.get("node") == "application":
            return _type_head(node.get("function"))
        if node.get("node") == "sort":
            return "Sort"
        for key in ("body", "codomain", "type"):
            if key in node:
                return _type_head(node[key])
    return None


def build_type(transition: dict[str, Any], seed: int) -> tuple:
    """`MISSION §22`: confusable type families, and no option that stands out.

    Sort-headed declarations are excluded. ``alpha : Type u`` is a type variable, so "which
    type belongs to alpha" answers "Sort" -- a degenerate question, and worse, ``Sort`` is
    the one head no symbol map renames, so it sat among the ``t`` tags as a visible outlier.
    Nineteen of forty-three TYPE items carried it before this exclusion.
    """

    context = _goal(transition).get("local_context") or []
    heads: list[tuple[str, str]] = []
    for declaration in context:
        head = _type_head(declaration.get("type"))
        if head == "Sort" or not head:
            continue
        if isinstance(declaration.get("identity"), str):
            heads.append((declaration["identity"], head))
    if len(heads) < 2:
        raise NotEligible("TYPE needs two typed declarations")
    distinct = sorted({head for _identity, head in heads})
    if len(distinct) < MINIMUM_OPTIONS:
        raise NotEligible("TYPE needs two distinct type heads")
    subject, answer = heads[seed % len(heads)]
    options = _choose_distractors(answer, distinct, seed)
    return (f"Which type belongs to the declaration {subject}?", options, answer,
            f"TYPE_OF({subject})", {"subject": subject})


def build_dependency(transition: dict[str, Any], seed: int) -> tuple:
    context = _goal(transition).get("local_context") or []
    declared = [d["identity"] for d in context if isinstance(d.get("identity"), str)]
    edges: list[tuple[str, str]] = []
    for declaration in context:
        for _path, identity in S.local_references(declaration.get("type")):
            if identity in declared and identity != declaration.get("identity"):
                edges.append((declaration["identity"], identity))
    if not edges:
        raise NotEligible("DEPENDENCY needs a type that references another declaration")
    subject, answer = edges[seed % len(edges)]
    pool = [d for d in declared if d != subject]
    options = _choose_distractors(answer, pool, seed)
    return (f"The type of {subject} depends on which other declaration?", options, answer,
            f"DEPENDS_ON({subject})", {"subject": subject, "edges": len(edges)})


def build_binder(transition: dict[str, Any], seed: int) -> tuple:
    """Which declaration the goal target actually uses.

    The first version asked "use number 41 refers to which declaration?", which made the
    reader count forty-one reference sites before it could even start on the binder
    relation. That measures counting, not binding. Asking instead which declaration is used
    *at all* keeps the relation under test and removes the arithmetic: the answer is a
    declaration the target references, and every distractor is a declaration in scope that
    it does not.
    """

    goal = _goal(transition)
    declared = [d["identity"] for d in (goal.get("local_context") or [])
                if isinstance(d.get("identity"), str)]
    used = {identity for _path, identity in S.local_references(goal.get("target"))}
    referenced = sorted(used & set(declared))
    unreferenced = [d for d in declared if d not in used]
    if not referenced:
        raise NotEligible("BINDER needs a target reference resolving to a declaration")
    if len(unreferenced) < MINIMUM_OPTIONS - 1:
        raise NotEligible("BINDER needs in-scope declarations the target does not use")
    answer = referenced[seed % len(referenced)]
    options = _choose_distractors(answer, [answer, *unreferenced], seed)
    return ("Which of these declarations is used in the goal target?", options, answer,
            "USE_OWNER", {"referenced": len(referenced), "in_scope": len(declared)})


def build_scope(transition: dict[str, Any], seed: int) -> tuple:
    goals = transition["state_before"]["goals"]
    ownership: dict[str, set[int]] = {}
    for index, goal in enumerate(goals):
        for declaration in goal.get("local_context") or []:
            identity = declaration.get("identity")
            if isinstance(identity, str):
                ownership.setdefault(identity, set()).add(index)
    unique = sorted(i for i, owners in ownership.items() if len(owners) == 1)
    if not unique or len(goals) < MINIMUM_OPTIONS:
        raise NotEligible("SCOPE needs a declaration owned by exactly one of several goals")
    # The owning goal must vary across the cell. Taking whatever came to hand gave "g1" or
    # "g2" on 85% of items; preferring a late owner then gave "g2" on 18 of 20, which is
    # worse. Grouping the candidates BY owner and rotating over the owners spreads the
    # answer across whatever goals the corpus actually offers.
    by_owner: dict[int, list[str]] = {}
    for identity in unique:
        by_owner.setdefault(next(iter(ownership[identity])), []).append(identity)
    owners = sorted(by_owner)
    owner = owners[seed % len(owners)]
    subject = by_owner[owner][seed % len(by_owner[owner])]
    labels = [f"{anonymise.GOAL_PREFIX}{index + 1}" for index in range(len(goals))]
    options = _choose_distractors(labels[owner], labels, seed)
    return (f"Which goal holds the declaration {subject} in its local context?",
            options, labels[owner], f"SCOPE_OWNER({subject})",
            {"subject": subject, "goals": len(goals)})


def build_premise(transition: dict[str, Any], seed: int,
                  tagged_pool: list[str] | None = None) -> tuple:
    """`MISSION §21`: four same-domain premises, all individually plausible.

    ``tagged_pool`` is the p-family tag of every real lemma name drawn from the same domain.
    Every option therefore looks like a premise, and only the citation says which one the
    action actually requires.
    """

    action = transition.get("action") or {}
    cited = [p for p in (action.get("external_premise_refs") or []) if isinstance(p, str)]
    if not cited:
        raise NotEligible("PREMISE needs a citation")
    pool = sorted(set(tagged_pool or []) | set(cited))
    if len(pool) < MINIMUM_OPTIONS:
        raise NotEligible("PREMISE needs same-domain alternatives to offer")
    answer = cited[seed % len(cited)]
    options = _choose_distractors(answer, pool, seed)
    return ("Which premise does the action cite?", options, answer, "ACTION_REQUIRES",
            {"cited": len(cited), "pool": len(pool)})


def build_action_argument(transition: dict[str, Any], seed: int) -> tuple:
    action = transition.get("action") or {}
    used = [r["canonical_id"].rsplit(":", 1)[-1]
            for r in (action.get("local_context_refs") or [])
            if isinstance(r, dict) and r.get("resolved") and r.get("canonical_id")]
    declared = [d["identity"] for d in (_goal(transition).get("local_context") or [])
                if isinstance(d.get("identity"), str)]
    present = [u for u in used if u in declared]
    if not present or len(declared) < MINIMUM_OPTIONS:
        raise NotEligible("ACTION_ARGUMENT needs a resolved argument among the declarations")
    answer = present[seed % len(present)]
    unused = [d for d in declared if d not in used]
    if not unused:
        raise NotEligible("ACTION_ARGUMENT needs an unused declaration as a distractor")
    options = _choose_distractors(answer, [answer, *unused], seed)
    return ("Which declaration does the action use as an argument?", options, answer,
            "ACTION_ARG", {"arguments": len(present)})


#: MULTI_GOAL is withdrawn from the V2 lab, and the reason is a finding rather than a bug.
#:
#: The question "which goal does the action act on" is not answerable from ANY rendering in
#: this representation space. Two independent reasons, both verified against
#: `projection.py`: ``_action_section`` emits source, kind, elaborator, premises and local
#: refs but never names a goal; and the delta section names goals as ``_uniq.*`` ids, which
#: the identity codec leaves unmapped while the goal section renders ``m3``/``m7``. The two
#: namespaces never meet on the page.
#:
#: So the relation is missing from the canonical-to-document projection, not merely rendered
#: badly. Defining the answer positionally -- the only option left -- produced ``g1`` on 43
#: of 43 items, which the shortcut audit called CONSTANT_ANSWER at an entropy of 0.023.
#:
#: This also corrects the V1 reading. V1's MULTI_GOAL passed calibration (positive 0.958,
#: negative 0.500) and was reported as the project's largest readable headroom. The positive
#: arm was high because it stated the answer in the header; the candidate and control sat
#: near chance because NEITHER could answer a question the projection does not carry. That
#: is not headroom a better notation could claim. It is an absent projection.
MULTI_GOAL_WITHDRAWN = (
    "RELATION_NOT_PROJECTED: no axis of the representation space renders which goal the "
    "action acts on, so no representation can be scored on it")


def build_multi_goal(transition: dict[str, Any], seed: int) -> tuple:
    raise NotEligible(MULTI_GOAL_WITHDRAWN)


def build_expression_depth(transition: dict[str, Any], seed: int) -> tuple:
    goal = _goal(transition)
    sites = S.local_references(goal.get("target"))
    if len(sites) < MINIMUM_OPTIONS:
        raise NotEligible("EXPRESSION_DEPTH needs two references in the target")
    deepest = max(sites, key=lambda entry: (len(entry[0]), entry[0]))
    answer = deepest[1]
    pool = sorted({identity for _p, identity in sites})
    if len(pool) < MINIMUM_OPTIONS:
        raise NotEligible("EXPRESSION_DEPTH needs two distinct references")
    options = _choose_distractors(answer, pool, seed)
    return ("Which reference sits deepest in the goal target?", options, answer,
            "DEEPEST_REFERENCE", {"depth": len(deepest[0]), "references": len(sites)})


BUILDERS: dict[str, Callable[[dict[str, Any], int], tuple]] = {
    S.TYPE: build_type,
    S.DEPENDENCY: build_dependency,
    S.BINDER: build_binder,
    S.SCOPE: build_scope,
    S.PREMISE: build_premise,
    S.ACTION_ARGUMENT: build_action_argument,
    S.MULTI_GOAL: build_multi_goal,
    S.EXPRESSION_DEPTH: build_expression_depth,
}

#: Which prior families each instrument must strip. TYPE and PREMISE carry the loudest
#: priors and need the most aggressive anonymisation; the reference-following instruments
#: only need their declarations opaque.
ANONYMISATION: dict[str, dict[str, bool]] = {
    S.TYPE: {"rename_declarations": True, "rename_symbols": True, "rename_premises": False},
    S.PREMISE: {"rename_declarations": True, "rename_symbols": True, "rename_premises": True},
    S.DEPENDENCY: {"rename_declarations": True, "rename_symbols": True, "rename_premises": False},
    S.SCOPE: {"rename_declarations": True, "rename_symbols": False, "rename_premises": False},
    S.BINDER: {"rename_declarations": True, "rename_symbols": False, "rename_premises": False},
    S.ACTION_ARGUMENT: {"rename_declarations": True, "rename_symbols": False,
                        "rename_premises": False},
    S.MULTI_GOAL: {"rename_declarations": True, "rename_symbols": False,
                   "rename_premises": False},
    S.EXPRESSION_DEPTH: {"rename_declarations": True, "rename_symbols": False,
                         "rename_premises": False},
}


def build(transition: dict[str, Any], stress: str, domain: str,
          domain_confidence: str = "UNKNOWN",
          premise_pool: list[str] | None = None) -> MicroItem:
    """Build one V2 item: anonymise, ask, distract, ablate, and check the ablation bit."""

    builder = BUILDERS.get(stress)
    if builder is None:
        raise NotEligible(f"no V2 builder for {stress}")
    transition_id = transition["transition_id"]
    seed = _seed(transition_id)

    anonymised, maps = anonymise.apply(
        prune(transition), salt=f"{LAB_VERSION}|{stress}",
        premise_pool=premise_pool, **ANONYMISATION[stress])
    if stress == S.PREMISE:
        cited = set((anonymised.get("action") or {}).get("external_premise_refs") or [])
        tagged = [tag for tag in maps["premises"].values() if tag not in cited]
        question, options, answer, relation, detail = builder(anonymised, seed, tagged)
    else:
        question, options, answer, relation, detail = builder(anonymised, seed)

    if anonymise.leaks_answer(list(options), answer):
        raise NotEligible("the option set alone identifies the answer")

    kwargs: dict[str, Any] = {}
    if stress == S.PREMISE:
        kwargs["candidates"] = [o for o in options if o != answer]
    try:
        ablated = ablate.ablate(stress, anonymised, seed, **kwargs)
    except ablate.AblationFailed as error:
        raise NotEligible(f"negative control unavailable: {error}") from error
    if not ablate.changed(anonymised, ablated):
        raise NotEligible("the ablation left the state unchanged; the negative arm would lie")

    detail = dict(detail)
    detail["anonymisation"] = {k: len(v) for k, v in maps.items()}
    return MicroItem(
        item_id=item_id(domain, stress, transition_id), domain=domain,
        domain_confidence=domain_confidence, stress=stress,
        base_transition_id=transition_id,
        source_file=(transition.get("corpus_metadata") or {}).get("source_file", ""),
        question=question, options=options, answer=answer, relation=relation,
        state=anonymised, ablated=ablated, detail=detail)
