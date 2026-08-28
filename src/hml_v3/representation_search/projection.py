"""Genome-driven projection between a canonical transition and a Document.

This layer answers *what is written* — which semantic units exist, how they are named, in
what order they appear, and what redundancy is added. The surface layer answers *how*.

The declared semantic contract is defined here by :func:`semantic_core`. A candidate claims
losslessness against that contract and nothing else: diagnostic spellings, content hashes,
environment provenance and corpus bookkeeping are explicitly outside it, exactly as
`D-002`/`D-009` require. The hard round-trip gate compares ``semantic_core`` before and
after, so a genome that hides contract content is rejected rather than quietly rewarded with
a smaller token count.
"""

from __future__ import annotations

import hashlib
from typing import Any

from hml_v3.representation_search.document import Document, Record, Section
from hml_v3.representation_search.genome import RepresentationGenome

BINDER_ROLE_DEFAULT = "default"
#: Lean 4.10 emits these spellings; the lower-case forms are the synthetic fixtures'.
IMPLICIT_BINDER_ROLES = frozenset({
    "IMPLICIT", "STRICT_IMPLICIT", "INSTANCE_IMPLICIT",
    "implicit", "strict_implicit", "inst_implicit",
})
DECLARATION_ROLE_DEFAULT = "cdecl"


# ------------------------------------------------------------------- the semantic contract


def semantic_core(transition: dict[str, Any]) -> dict[str, Any]:
    """The content a lossless candidate must recover, and nothing else."""

    return {
        "before": _state_core(transition["state_before"]),
        "after": _state_core(transition["state_after"]),
        "action": {
            "identity": action_identity(transition),
            "external_premise_refs": sorted(transition["action"]["external_premise_refs"]),
            "local_context_refs": sorted(
                reference["canonical_id"]
                for reference in transition["action"]["local_context_refs"]
                if reference.get("resolved")
            ),
        },
    }


def action_identity(transition: dict[str, Any]) -> str:
    """The action's semantic identity: its elaborated kind and its tactic family.

    The canonical V2 record deliberately does not carry raw tactic text — the tactic's
    *identity* is its elaborated occurrence, and the surface text is a source observation.
    What a representation must recover is this pair.
    """

    kind = transition["action"]["kind"]
    family = (transition.get("corpus_metadata") or {}).get("tactic_family") or "-"
    return f"{kind}/{family}"


def _state_core(state: dict[str, Any]) -> dict[str, Any]:
    return {
        "focus_order": list(state["focus_order"]),
        "goals": [
            {
                "identity": goal["identity"],
                "target": goal["target"],
                "context": [
                    {
                        "identity": declaration["identity"],
                        "binder_role": declaration["binder_role"],
                        "declaration_role": declaration["declaration_role"],
                        "type": declaration["type"],
                        "value": declaration["value"],
                    }
                    for declaration in goal["local_context"]
                ],
            }
            for goal in state["goals"]
        ],
        "metavariables": [
            {
                "identity": metavariable["identity"],
                "kind": metavariable["kind"],
                "type": metavariable["type"],
                "assigned": metavariable["assigned"],
                "assignment": metavariable["assignment"],
            }
            for metavariable in state["metavariables"]
        ],
    }


# ------------------------------------------------------------------------------ identities


def _short(identity: str) -> str:
    """``t:before:local:f3`` -> ``f3``. Short ids stay unique inside one transition."""

    return identity.rsplit(":", 1)[-1]


class IdentityCodec:
    """Encodes and decodes the token that names a goal, declaration or metavariable."""

    def __init__(self, transition: dict[str, Any], genome: RepresentationGenome) -> None:
        self.scheme = genome.get("identity_scheme")
        self.transition_id = transition["transition_id"]
        self.forward: dict[str, str] = {}
        self.backward: dict[str, str] = {}
        self.collisions = 0
        for phase in ("state_before", "state_after"):
            state = transition[phase]
            prefix = f"{self.transition_id}:{'before' if phase == 'state_before' else 'after'}"
            for goal in state["goals"]:
                self._register(goal["identity"], goal["identity"], prefix)
                for declaration in goal["local_context"]:
                    self._register(
                        declaration["identity"], declaration["identity"], prefix,
                        display=declaration.get("user_name_diagnostic"),
                    )
            for metavariable in state["metavariables"]:
                self._register(metavariable["identity"], metavariable["identity"], prefix)

    def _register(self, canonical: str, _identity: str, prefix: str, display: str | None = None) -> None:
        if canonical in self.forward:
            return
        if self.scheme == "SEMANTIC_ID":
            token = canonical
        elif self.scheme == "SHORT_ID":
            token = f"{'b' if prefix.endswith('before') else 'a'}{_short(canonical)}"
        elif self.scheme == "DISPLAY_NAME":
            token = display or _short(canonical)
        else:  # DISPLAY_PLUS_SHORT_ID
            side = "b" if prefix.endswith("before") else "a"
            token = f"{display}~{side}{_short(canonical)}" if display else f"{side}{_short(canonical)}"
        if token in self.backward and self.backward[token] != canonical:
            # A display-name scheme cannot separate shadowed declarations. The collision is
            # recorded rather than repaired; the round-trip gate then rejects the candidate.
            self.collisions += 1
        self.forward[canonical] = token
        self.backward.setdefault(token, canonical)

    def encode(self, canonical: str) -> str:
        return self.forward.get(canonical, canonical)

    def decode(self, token: str) -> str:
        return self.backward.get(token, token)


# ------------------------------------------------------------------------------- ordering


def _declaration_dependencies(declaration: dict[str, Any]) -> set[str]:
    found: set[str] = set()

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            if node.get("node") == "local_reference":
                found.add(node["identity"])
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(declaration.get("type"))
    walk(declaration.get("value"))
    return found


def order_context(
    goal: dict[str, Any], genome: RepresentationGenome, action_refs: set[str],
) -> list[dict[str, Any]]:
    declarations = list(goal["local_context"])
    order = genome.get("context_order")
    if order == "DECLARATION_INDEX":
        return declarations
    if order == "REVERSE_INDEX":
        return list(reversed(declarations))
    if order == "TYPE_GROUPED":
        return sorted(
            declarations,
            key=lambda declaration: (
                declaration["declaration_role"], declaration["binder_role"],
                _position(declarations, declaration),
            ),
        )
    if order == "DEPENDENCY_TOPOLOGICAL":
        return _topological(declarations)
    if order == "GOAL_CENTRED":
        target_refs = _declaration_dependencies({"type": goal["target"], "value": None})
        relevant = target_refs | action_refs
        closure = set(relevant)
        by_id = {declaration["identity"]: declaration for declaration in declarations}
        frontier = list(relevant)
        while frontier:
            current = frontier.pop()
            declaration = by_id.get(current)
            if declaration is None:
                continue
            for dependency in _declaration_dependencies(declaration):
                if dependency not in closure:
                    closure.add(dependency)
                    frontier.append(dependency)
        front = [d for d in declarations if d["identity"] in closure]
        back = [d for d in declarations if d["identity"] not in closure]
        return front + back
    return declarations


def _position(declarations: list[dict[str, Any]], declaration: dict[str, Any]) -> int:
    return declarations.index(declaration)


def _topological(declarations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {declaration["identity"]: declaration for declaration in declarations}
    ordered: list[dict[str, Any]] = []
    placed: set[str] = set()
    visiting: set[str] = set()

    def visit(identity: str) -> None:
        if identity in placed or identity not in by_id or identity in visiting:
            return
        visiting.add(identity)
        declaration = by_id[identity]
        for dependency in sorted(_declaration_dependencies(declaration)):
            visit(dependency)
        visiting.discard(identity)
        placed.add(identity)
        ordered.append(declaration)

    for declaration in declarations:
        visit(declaration["identity"])
    return ordered


def order_goals(state: dict[str, Any], genome: RepresentationGenome) -> list[dict[str, Any]]:
    goals = list(state["goals"])
    strategy = genome.get("graph_serialization")
    if strategy == "BFS":
        return sorted(goals, key=lambda goal: len(goal["local_context"]))
    if strategy in ("TOPOLOGICAL", "DEPENDENCY_LOCAL"):
        return goals
    if strategy == "GOAL_CENTRED":
        focus = state["focus_order"][0] if state["focus_order"] else None
        return sorted(goals, key=lambda goal: (goal["identity"] != focus, goal["identity"]))
    return goals


# ------------------------------------------------------------------------------- projection


def _digest(value: Any) -> str:
    import json

    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()[:8]


class Projection:
    """Builds a Document from a canonical transition, and rebuilds the core from one."""

    def __init__(self, genome: RepresentationGenome) -> None:
        self.genome = genome

    # ------------------------------------------------------------------------- encode
    def to_document(self, transition: dict[str, Any]) -> tuple[Document, IdentityCodec]:
        genome = self.genome
        codec = IdentityCodec(transition, genome)
        action_refs = {
            reference["canonical_id"]
            for reference in transition["action"]["local_context_refs"]
            if reference.get("resolved")
        }
        sections: list[Section] = []

        if genome.get("provenance_visibility") == "IDENTITY_ONLY":
            sections.append(Section("meta", [Record("summary", None, [
                ("theorem", transition["source_specific_reference"]["theorem_id"]),
                ("file", transition["provenance"].get("source_file", "")),
            ])]))

        action_section = self._action_section(transition, codec)
        before_sections = self._state_sections(
            transition["state_before"], "state_before", codec, action_refs, transition,
        )
        after_sections: list[Section] = []
        if genome.get("state_partitioning") != "BEFORE_PLUS_DELTA":
            after_sections = self._state_sections(
                transition["state_after"], "state_after", codec, action_refs, transition,
            )
        delta_section = self._delta_section(transition, codec)

        if genome.get("action_position") == "HEADER":
            sections += [action_section, *before_sections, *after_sections]
        elif genome.get("action_position") == "TRAILER":
            sections += [*before_sections, *after_sections, action_section]
        else:
            sections += [*before_sections, action_section, *after_sections]
        if delta_section is not None:
            sections.append(delta_section)
        return Document(sections), codec

    def _state_sections(
        self, state: dict[str, Any], kind: str, codec: IdentityCodec,
        action_refs: set[str], transition: dict[str, Any],
    ) -> list[Section]:
        genome = self.genome
        records: list[Record] = []
        edges: list[Record] = []
        goals = order_goals(state, genome)
        emit_scope = genome.get("scope_metadata") == "EXPLICIT_SCOPE_IDS"
        for goal in goals:
            declarations = order_context(goal, genome, action_refs)
            goal_fields: list[tuple[str, Any]] = []
            if genome.get("goal_position") == "FIRST":
                goal_fields.append(("target", goal["target"]))
            # The goal's context list always states canonical declaration order, so record
            # layout can be permuted for locality without making the order unrecoverable.
            # Lean's local-context order is semantic; a candidate may re-lay-out records, it
            # may not silently discard the ordering.
            goal_fields.append(("context", [
                codec.encode(d["identity"]) for d in goal["local_context"]
            ]))
            if genome.get("goal_position") in ("AFTER_CONTEXT", "LAST", "INLINE_WITH_CONTEXT"):
                goal_fields.append(("target", goal["target"]))
            if genome.get("count_assertions") == "PER_BLOCK":
                goal_fields.append(("count", len(declarations)))
            visibility = genome.get("goal_identity_visibility")
            ordinal = state["focus_order"].index(goal["identity"]) \
                if goal["identity"] in state["focus_order"] else 0
            if visibility == "NONE":
                goal_token = None
            elif visibility == "ORDINAL":
                goal_token = f"g{ordinal}"
            else:
                goal_token = codec.encode(goal["identity"])
            if visibility == "BOTH":
                goal_fields.append(("index", ordinal))
            goal_record = Record("goal", goal_token, goal_fields)
            declaration_records = [
                self._declaration_record(declaration, codec, goal, emit_scope, position)
                for position, declaration in enumerate(declarations)
            ]
            reminder_records = self._reminder_records(goal, declarations, codec)
            if genome.get("goal_position") == "FIRST":
                records.append(goal_record)
                records.extend(reminder_records)
                records.extend(declaration_records)
            else:
                records.extend(declaration_records)
                records.extend(reminder_records)
                records.append(goal_record)
            if genome.get("tree_vs_graph_projection") in (
                "GRAPH_EDGE_LIST", "HYBRID_NESTED_WITH_EDGES",
            ):
                for declaration in declarations:
                    for dependency in sorted(_declaration_dependencies(declaration)):
                        edges.append(Record("edge", None, [
                            ("from", codec.encode(declaration["identity"])),
                            ("to", codec.encode(dependency)),
                            ("relation", "depends"),
                        ]))
        if genome.get("obligation_visibility") != "NONE":
            for metavariable in state["metavariables"]:
                if (genome.get("obligation_visibility") == "ASSIGNED_ONLY"
                        and not metavariable["assigned"]):
                    continue
                fields: list[tuple[str, Any]] = [
                    ("kind", metavariable["kind"]),
                    ("type", metavariable["type"]),
                    ("assigned", "yes" if metavariable["assigned"] else "no"),
                ]
                if metavariable["assignment"] is not None:
                    fields.append(("assignment", metavariable["assignment"]))
                records.append(Record("mvar", codec.encode(metavariable["identity"]), fields))
        if genome.get("goal_identity_visibility") == "NONE":
            focus_tokens: list[str] = []
        elif genome.get("goal_identity_visibility") == "ORDINAL":
            focus_tokens = [f"g{index}" for index in range(len(state["focus_order"]))]
        else:
            focus_tokens = [codec.encode(identity) for identity in state["focus_order"]]
        records.append(Record("summary", None, [("focus_order", focus_tokens)]))
        if self.genome.get("checksum_policy") == "PER_STATE":
            records.append(Record("summary", None, [("digest", _digest(state))]))
        sections = [Section(kind, records)]
        if edges:
            sections.append(Section("edges", edges))
        return sections

    def _reminder_records(
        self, goal: dict[str, Any], declarations: list[dict[str, Any]], codec: IdentityCodec,
    ) -> list[Record]:
        """Restate something about each binder the goal's target actually uses.

        This is the §13 mutation the failure memory suggests for long binder-use distance:
        it moves a compact copy of the binder identity next to the site that consumes it, at
        a token cost, without adding information the state does not already carry.
        """

        policy = self.genome.get("binder_use_reminder")
        if policy == "NONE":
            return []
        used = _declaration_dependencies({"type": goal["target"], "value": None})
        by_id = {declaration["identity"]: declaration for declaration in declarations}
        records: list[Record] = []
        for identity in sorted(used):
            declaration = by_id.get(identity)
            if declaration is None:
                continue
            if policy == "TYPE_AT_USE":
                records.append(Record("alias", codec.encode(identity), [
                    ("reminder", declaration["type"]),
                ]))
            else:
                records.append(Record("alias", codec.encode(identity), [
                    ("tag", _head_symbol(declaration["type"])),
                ]))
        return records

    def _declaration_record(
        self, declaration: dict[str, Any], codec: IdentityCodec,
        goal: dict[str, Any], emit_scope: bool, position: int = 0,
    ) -> Record:
        genome = self.genome
        fields: list[tuple[str, Any]] = []
        if genome.get("alpha_normalization") in ("PRESERVE_DISPLAY", "BOTH"):
            fields.append(("display", declaration.get("user_name_diagnostic", "")))
        if genome.get("binder_metadata") == "FULL":
            fields.append(("binder_role", declaration["binder_role"]))
            fields.append(("declaration_role", declaration["declaration_role"]))
        elif genome.get("binder_metadata") == "ROLE_ONLY":
            fields.append(("binder_role", declaration["binder_role"]))
        if emit_scope:
            fields.append(("scope", codec.encode(goal["identity"])))
        explicitness = genome.get("type_explicitness")
        elided = (
            genome.get("implicit_argument_visibility") == "MARKED_ELIDED"
            and declaration["binder_role"] in IMPLICIT_BINDER_ROLES
        )
        if elided:
            fields.append(("tag", "ELIDED_IMPLICIT"))
        elif explicitness == "FULL_TREE":
            fields.append(("type", declaration["type"]))
        elif explicitness == "HEAD_SYMBOL_ONLY":
            fields.append(("tag", _head_symbol(declaration["type"])))
        if declaration["value"] is not None and explicitness == "FULL_TREE" and not elided:
            fields.append(("value", declaration["value"]))
        if genome.get("redundancy_level") in ("EXPLICIT", "ERROR_CORRECTING"):
            fields.append(("index", position))
        return Record("decl", codec.encode(declaration["identity"]), fields)

    def _action_section(self, transition: dict[str, Any], codec: IdentityCodec) -> Section:
        genome = self.genome
        action = transition["action"]
        source = transition["source_specific_reference"]
        fields: list[tuple[str, Any]] = []
        encoding = genome.get("action_encoding")
        identity = action_identity(transition)
        kind, _, family = identity.partition("/")
        if encoding in ("SOURCE_TACTIC", "SOURCE_PLUS_STRUCTURED"):
            fields.append(("source", identity))
        if encoding == "GENERIC_SEMANTIC":
            fields.append(("kind", "TRANSFORM"))
        if encoding in ("STRUCTURED_ARGS", "SOURCE_PLUS_STRUCTURED"):
            fields.append(("kind", kind))
            fields.append(("elaborator", family))
        if genome.get("premise_locality") != "HEADER_BLOCK":
            fields.append(("premises", list(action["external_premise_refs"])))
        if genome.get("dependency_visibility") == "INLINE_REFS":
            fields.append(("local_refs", sorted(
                codec.encode(reference["canonical_id"])
                for reference in action["local_context_refs"] if reference.get("resolved")
            )))
        records = [Record("step", None, fields)]
        if genome.get("premise_locality") == "HEADER_BLOCK":
            records.insert(0, Record("summary", None, [
                ("premises", list(action["external_premise_refs"])),
            ]))
        if genome.get("dependency_visibility") == "EXPLICIT_EDGES":
            for reference in action["local_context_refs"]:
                if reference.get("resolved"):
                    records.append(Record("edge", None, [
                        ("from", "step"), ("to", codec.encode(reference["canonical_id"])),
                        ("relation", "uses"),
                    ]))
        return Section("action", records)

    def _delta_section(self, transition: dict[str, Any], codec: IdentityCodec) -> Section | None:
        if self.genome.get("delta_visibility") != "EXPLICIT_DELTA_BLOCK":
            return None
        delta = transition["state_delta"]
        fields = [
            ("goals_created", [codec.encode(i) for i in delta["goals_created"]]),
            ("goals_solved", [codec.encode(i) for i in delta["goals_solved"]]),
            ("goals_modified", [codec.encode(i) for i in delta["goals_modified"]]),
            ("locals_added", [codec.encode(i) for i in delta["local_declarations_added"]]),
            ("locals_removed", [codec.encode(i) for i in delta["local_declarations_removed"]]),
            ("mvars_assigned", [codec.encode(i) for i in delta["metavariables_assigned"]]),
            ("reordered", "yes" if delta["goals_reordered"] else "no"),
        ]
        return Section("delta", [Record("summary", None, fields)])

    # ------------------------------------------------------------------------- decode
    def core_from_document(
        self, document: Document, codec: IdentityCodec,
    ) -> dict[str, Any]:
        genome = self.genome
        states: dict[str, dict[str, Any]] = {}
        action: dict[str, Any] = {
            "external_premise_refs": [], "local_context_refs": [],
            "identity": None, "kind": None, "family": None,
        }
        for section in document.sections:
            if section.kind in ("state_before", "state_after"):
                states[section.kind] = self._state_from_records(section.records, codec)
            elif section.kind == "action":
                for record in section.records:
                    values = dict(record.fields)
                    if "source" in values:
                        action["identity"] = values["source"]
                    if "kind" in values:
                        action["kind"] = values["kind"]
                    if "elaborator" in values:
                        action["family"] = values["elaborator"]
                    if "premises" in values:
                        action["external_premise_refs"] = list(values["premises"])
                    if "local_refs" in values:
                        action["local_context_refs"] = [
                            codec.decode(token) for token in values["local_refs"]
                        ]
                    if record.kind == "edge" and values.get("relation") == "uses":
                        action["local_context_refs"].append(codec.decode(values["to"]))
        before = states.get("state_before", {"goals": [], "focus_order": [], "metavariables": []})
        after = states.get("state_after")
        if after is None:
            after = {"goals": [], "focus_order": [], "metavariables": [],
                     "reconstruction": "UNAVAILABLE_UNDER_THIS_GENOME"}
        return {
            "before": before,
            "after": after,
            "action": {
                "identity": self._recovered_action_identity(action),
                "external_premise_refs": sorted(action["external_premise_refs"]),
                "local_context_refs": sorted(set(action["local_context_refs"])),
            },
        }

    @staticmethod
    def _recovered_action_identity(action: dict[str, Any]) -> str | None:
        if action["identity"] is not None:
            return action["identity"]
        if action["kind"] is not None and action["family"] is not None:
            return f"{action['kind']}/{action['family']}"
        return None

    def _state_from_records(
        self, records: list[Record], codec: IdentityCodec,
    ) -> dict[str, Any]:
        declarations: dict[str, dict[str, Any]] = {}
        goals: list[dict[str, Any]] = []
        metavariables: list[dict[str, Any]] = []
        focus_order: list[str] = []
        for record in records:
            values = dict(record.fields)
            if record.kind == "alias":
                continue
            if record.kind == "decl":
                identity = codec.decode(record.identity or "")
                declarations[record.identity or ""] = {
                    "identity": identity,
                    "binder_role": values.get("binder_role", BINDER_ROLE_DEFAULT),
                    "declaration_role": values.get(
                        "declaration_role", DECLARATION_ROLE_DEFAULT,
                    ),
                    "type": values.get("type"),
                    "value": values.get("value"),
                }
            elif record.kind == "goal":
                goals.append({
                    "identity": codec.decode(record.identity or ""),
                    "target": values.get("target"),
                    "context_tokens": list(values.get("context", [])),
                })
            elif record.kind == "mvar":
                metavariables.append({
                    "identity": codec.decode(record.identity or ""),
                    "kind": values.get("kind"),
                    "type": values.get("type"),
                    "assigned": values.get("assigned") == "yes",
                    "assignment": values.get("assignment"),
                })
            elif record.kind == "summary" and "focus_order" in values:
                focus_order = [codec.decode(token) for token in values["focus_order"]]
        rebuilt_goals = []
        for goal in goals:
            rebuilt_goals.append({
                "identity": goal["identity"],
                "target": goal["target"],
                "context": [
                    declarations[token] for token in goal["context_tokens"]
                    if token in declarations
                ],
            })
        by_identity = {goal["identity"]: goal for goal in rebuilt_goals}
        ordered = [by_identity[identity] for identity in focus_order if identity in by_identity]
        ordered += [goal for goal in rebuilt_goals if goal["identity"] not in set(focus_order)]
        return {"focus_order": focus_order, "goals": ordered, "metavariables": metavariables}


def map_expression_identities(document: Document, rewrite) -> Document:
    """Rewrite every ``local_reference``/``metavariable_reference`` identity in a Document.

    Identity encoding has to reach *inside* expressions, not only record headers and
    reference lists. A candidate whose short ids appear in the context list but whose
    expression bodies still carry full canonical paths would be measured with the wrong
    token cost and the wrong binder-use distance.
    """

    from hml_v3.representation_search.document import EXPR, FIELD_TYPES

    def walk(node: Any) -> Any:
        if isinstance(node, dict):
            if node.get("node") in ("local_reference", "metavariable_reference"):
                return {**node, "identity": rewrite(node["identity"])}
            return {key: walk(value) for key, value in node.items()}
        if isinstance(node, list):
            return [walk(item) for item in node]
        return node

    sections = []
    for section in document.sections:
        records = []
        for record in section.records:
            fields = [
                (name, walk(value) if FIELD_TYPES.get(name) == EXPR else value)
                for name, value in record.fields
            ]
            records.append(Record(record.kind, record.identity, fields))
        sections.append(Section(section.kind, records))
    return Document(sections)


def _head_symbol(expr: dict[str, Any] | None) -> str:
    node = expr
    while isinstance(node, dict) and node.get("node") == "application":
        node = node["function"]
    if isinstance(node, dict):
        if node.get("node") == "symbol":
            return node["identity"]
        return str(node.get("node", "unknown"))
    return "unknown"
