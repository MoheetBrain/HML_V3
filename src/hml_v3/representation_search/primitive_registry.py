"""How an invented axis becomes a real axis.

A meta-designer can propose anything. The question this module answers is which proposals the
compiler can actually *execute*, and it answers it honestly: a new axis is accepted only when
its declared behaviour binds to a projection hook the compiler already knows how to run.

That is a real envelope, and it is stated rather than hidden. The system is open-ended within
a projection algebra — records can be duplicated near their use sites, grouped into
neighbourhood capsules, hoisted, annotated, partitioned or reordered — and a proposal outside
that algebra is recorded as `ACCEPTED_UNIMPLEMENTABLE` rather than silently dropped or
silently faked. Growing the algebra is a code change with tests, not a runtime trick.

Every accepted primitive bumps the genome schema version and is replayable from its proposal.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any, Callable, Sequence

from hml_v3.representation_search.document import Document, Record, Section

#: A hook transforms a Document given the axis value and the proposal's parameters.
ProjectionHook = Callable[[Document, str, dict[str, Any]], Document]


def variant(value: str, values: Sequence[str]) -> int:
    """Which behaviour an axis value selects, by position rather than by name.

    An earlier version matched value names literally (``GOAL_LOCAL``, ``BEFORE``), so an
    invented axis whose values were ``WIDE``/``NARROW`` silently did nothing: it took the
    fallback branch, which happened to reproduce the existing layout. Three axes were
    accepted that way and all nine of their axis-value combinations rendered identically.

    Hooks now index behaviour by the value's position among the non-``NONE`` values, so any
    naming an inventor chooses is functional.
    """

    active = [item for item in values if item != "NONE"]
    try:
        return active.index(value)
    except ValueError:
        return 0

REGISTRY_VERSION = "primitive-registry-v1.0.0"


# --------------------------------------------------------------------- projection algebra


def _copy(document: Document) -> Document:
    return Document([
        Section(section.kind, [
            Record(record.kind, record.identity, list(record.fields))
            for record in section.records
        ])
        for section in document.sections
    ])


def hook_neighbourhood_capsule(
    document: Document, value: str, params: dict[str, Any],
) -> Document:
    """Move the declarations a goal actually cites adjacent to that goal.

    The global context is not removed: every declaration record still exists exactly once.
    Only the layout changes, so the semantic contract is untouched while the span between a
    binder and the goal that uses it collapses.
    """

    if value == "NONE":
        return document
    out = _copy(document)
    for section in out.sections:
        if section.kind not in ("state_before", "state_after"):
            continue
        goals = [record for record in section.records if record.kind == "goal"]
        if not goals:
            continue
        declarations = {
            record.identity: record for record in section.records if record.kind == "decl"
        }
        others = [
            record for record in section.records
            if record.kind not in ("decl", "goal")
        ]
        rebuilt: list[Record] = []
        placed: set[str] = set()
        for goal in goals:
            cited = [
                token for name, item in goal.fields if name == "context"
                for token in (item if isinstance(item, list) else [])
            ]
            capsule = [
                declarations[token] for token in cited
                if token in declarations and token not in placed
            ]
            for record in capsule:
                placed.add(record.identity or "")
            if variant(value, params.get("values", ())) == 0:
                rebuilt.extend(capsule)
                rebuilt.append(goal)
            else:
                rebuilt.append(goal)
                rebuilt.extend(capsule)
        rebuilt.extend(
            record for record in declarations.values()
            if (record.identity or "") not in placed
        )
        rebuilt.extend(others)
        section.records = rebuilt
    return out


def hook_duplicate_adjacent(
    document: Document, value: str, params: dict[str, Any],
) -> Document:
    """Restate one field of a record next to the record that consumes it."""

    if value == "NONE":
        return document
    source_kind = params.get("source_kind", "decl")
    field_name = params.get("field", "tag")
    target_kind = params.get("target_kind", "goal")
    out = _copy(document)
    for section in out.sections:
        values = {
            record.identity: dict(record.fields).get(field_name)
            for record in section.records if record.kind == source_kind
        }
        rebuilt: list[Record] = []
        for record in section.records:
            rebuilt.append(record)
            if record.kind != target_kind:
                continue
            cited = [
                token for name, item in record.fields if name == "context"
                for token in (item if isinstance(item, list) else [])
            ]
            for token in cited:
                if values.get(token) is not None:
                    rebuilt.append(Record("alias", token, [(field_name, values[token])]))
        section.records = rebuilt
    return out


def hook_section_partition(
    document: Document, value: str, params: dict[str, Any],
) -> Document:
    """Split a state section so one record kind is emitted in its own block."""

    if value == "NONE":
        return document
    kind = params.get("record_kind", "mvar")
    out = _copy(document)
    sections: list[Section] = []
    for section in out.sections:
        if section.kind not in ("state_before", "state_after"):
            sections.append(section)
            continue
        matching = [record for record in section.records if record.kind == kind]
        rest = [record for record in section.records if record.kind != kind]
        if not matching:
            sections.append(section)
            continue
        if variant(value, params.get("values", ())) == 0:
            sections.append(Section(section.kind, matching + rest))
        else:
            sections.append(Section(section.kind, rest + matching))
    out.sections = sections
    return out


def hook_record_reorder(
    document: Document, value: str, params: dict[str, Any],
) -> Document:
    """Reorder records of one kind by a declared key."""

    if value == "NONE":
        return document
    kind = params.get("record_kind", "decl")
    out = _copy(document)
    for section in out.sections:
        matching = [record for record in section.records if record.kind == kind]
        if len(matching) < 2:
            continue
        position = variant(value, params.get("values", ()))
        if position == 0:
            ordered = list(reversed(matching))
        elif position == 1:
            ordered = sorted(
                matching, key=lambda record: (len(record.fields), record.identity or ""))
        else:
            ordered = sorted(matching, key=lambda record: record.identity or "")
        iterator = iter(ordered)
        section.records = [
            next(iterator) if record.kind == kind else record
            for record in section.records
        ]
    return out


HOOKS: dict[str, ProjectionHook] = {
    "neighbourhood_capsule": hook_neighbourhood_capsule,
    "duplicate_adjacent": hook_duplicate_adjacent,
    "section_partition": hook_section_partition,
    "record_reorder": hook_record_reorder,
}

#: Words a proposal may use to describe its behaviour, mapped to the hook that runs it.
BEHAVIOUR_KEYWORDS: dict[str, str] = {
    "capsule": "neighbourhood_capsule",
    "neighbourhood": "neighbourhood_capsule",
    "adjacent": "neighbourhood_capsule",
    "co-locate": "neighbourhood_capsule",
    "colocate": "neighbourhood_capsule",
    "local group": "neighbourhood_capsule",
    "duplicate": "duplicate_adjacent",
    "restate": "duplicate_adjacent",
    "reminder": "duplicate_adjacent",
    "repeat": "duplicate_adjacent",
    "partition": "section_partition",
    "separate block": "section_partition",
    "own block": "section_partition",
    "split": "section_partition",
    "reorder": "record_reorder",
    "sort": "record_reorder",
    "order": "record_reorder",
}


def infer_hook(payload: dict[str, Any]) -> str | None:
    """Bind a proposal's stated behaviour to an executable hook, or return None."""

    explicit = payload.get("projection_hook")
    if explicit in HOOKS:
        return explicit
    text = " ".join(
        str(payload.get(key, ""))
        for key in ("projection_behaviour", "mechanism", "hypothesis", "name")
    ).lower()
    for keyword, hook in BEHAVIOUR_KEYWORDS.items():
        if keyword in text:
            return hook
    return None


# ------------------------------------------------------------------------------ registry


@dataclass
class RegisteredPrimitive:
    axis_name: str
    values: tuple[str, ...]
    hook: str
    params: dict[str, Any]
    proposal_id: str
    generation: int
    proposer: str
    hypothesis: str
    mechanism: str
    falsification: str
    schema_version: str
    status: str = "ACTIVE"
    evidence: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "axis_name": self.axis_name,
            "values": list(self.values),
            "hook": self.hook,
            "params": self.params,
            "proposal_id": self.proposal_id,
            "generation": self.generation,
            "proposer": self.proposer,
            "hypothesis": self.hypothesis,
            "mechanism": self.mechanism,
            "falsification": self.falsification,
            "schema_version": self.schema_version,
            "status": self.status,
            "evidence": self.evidence,
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "RegisteredPrimitive":
        return cls(
            axis_name=value["axis_name"], values=tuple(value["values"]),
            hook=value["hook"], params=value.get("params", {}),
            proposal_id=value["proposal_id"], generation=value["generation"],
            proposer=value["proposer"], hypothesis=value["hypothesis"],
            mechanism=value["mechanism"], falsification=value["falsification"],
            schema_version=value["schema_version"], status=value.get("status", "ACTIVE"),
            evidence=value.get("evidence", {}),
        )


class PrimitiveRegistry:
    """Append-only record of every invented axis, accepted or not."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.primitives: dict[str, RegisteredPrimitive] = {}
        self.unimplementable: list[dict[str, Any]] = []
        if path.exists():
            for line in path.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                row = json.loads(line)
                # Test positively for a primitive rather than enumerating rejection
                # statuses. Enumerating them means every new rejection kind added later
                # crashes the loader on resume, which is exactly what ACCEPTED_DUPLICATE
                # did: the running search kept its registry in memory and was unaffected,
                # so the breakage only appeared when something re-read the file.
                if "values" in row and "hook" in row:
                    primitive = RegisteredPrimitive.from_dict(row)
                    self.primitives[primitive.axis_name] = primitive
                else:
                    self.unimplementable.append(row)

    @property
    def schema_version(self) -> str:
        return f"representation-genome-v2.{len(self.primitives)}.0"

    def active(self) -> list[RegisteredPrimitive]:
        return [p for p in self.primitives.values() if p.status == "ACTIVE"]

    def consider(
        self, payload: dict[str, Any], proposal_id: str, generation: int, proposer: str,
        known_axes: set[str],
    ) -> tuple[RegisteredPrimitive | None, str]:
        """Decide whether an invented axis can enter the genome.

        Returns ``(primitive, reason)``. A ``None`` primitive with a reason is a recorded
        outcome, not an error: the proposal is kept as evidence about what the meta-designer
        wanted and what the compiler could not do.
        """

        name = payload["name"]
        if name in known_axes or name in self.primitives:
            return None, "AXIS_ALREADY_EXISTS"
        hook = infer_hook(payload)
        if hook is None:
            self.unimplementable.append({
                "status": "ACCEPTED_UNIMPLEMENTABLE", "axis_name": name,
                "proposal_id": proposal_id, "generation": generation, "proposer": proposer,
                "reason": "no projection hook matches the stated behaviour",
                "payload": payload,
            })
            return None, "NO_EXECUTABLE_HOOK"
        values = tuple(payload["values"])
        if "NONE" not in values:
            # Every new axis needs an off position, or it cannot be attributed: without a
            # NONE value there is no candidate that differs only by not having the feature.
            values = ("NONE", *values)
        primitive = RegisteredPrimitive(
            axis_name=name, values=values, hook=hook,
            params=payload.get("params", {}) if isinstance(payload.get("params"), dict) else {},
            proposal_id=proposal_id, generation=generation, proposer=proposer,
            hypothesis=payload["hypothesis"], mechanism=payload["mechanism"],
            falsification=payload["falsification"],
            schema_version=f"representation-genome-v2.{len(self.primitives) + 1}.0",
        )
        return primitive, "IMPLEMENTABLE"

    def register(self, primitive: RegisteredPrimitive) -> None:
        self.primitives[primitive.axis_name] = primitive

    def has_observable_effect(
        self, primitive: RegisteredPrimitive, compiler_factory, transitions,
    ) -> tuple[bool, dict[str, Any]]:
        """Does at least one value of this axis change the rendering?

        Acceptance condition 6 in the spec, now enforced rather than merely stated. Three
        axes were accepted before this check existed whose nine axis-value combinations all
        rendered identically: the meta-designer had proposed real-sounding mechanisms that
        the projection algebra turned into no-ops. An inert axis is worse than no axis --
        it consumes search budget and inflates the apparent size of the space.
        """

        if not transitions:
            return False, {"reason": "no transitions to test against"}
        renderings: dict[str, str] = {}
        for value in primitive.values:
            invented = {primitive.axis_name: value}
            try:
                compiler = compiler_factory(invented)
                renderings[value] = "\n@@\n".join(
                    compiler.render_text(transition) for transition in transitions)
            except Exception as error:  # noqa: BLE001
                return False, {"reason": f"render failed for {value}: {type(error).__name__}"}
        distinct = len({text for text in renderings.values()})
        return distinct > 1, {
            "values_tested": list(primitive.values),
            "distinct_renderings": distinct,
            "transitions_tested": len(transitions),
        }

    def duplicates_an_existing_axis(
        self, primitive: RegisteredPrimitive, compiler_factory, transitions,
    ) -> tuple[str | None, dict[str, Any]]:
        """Does this axis produce renderings an axis already in the genome produces?

        `FM-026` established that an axis changing nothing must be rejected. This is its
        sibling and it went unnoticed for longer because the axis is *not* inert: it changes
        the rendering, passes the observable-effect gate, and is a perfect copy of an axis
        already registered under a different name.

        Measured on the first 15 generations of the pool run, nine of thirty accepted axes --
        ``action_scope``, ``dependency_capsule``, ``goal_id_projection``, ``hash_projection``,
        ``local_context_fragment``, ``local_dependency_capsule``, ``local_dependency_scope``,
        ``semantic_context_grouping`` and ``semantic_summary`` -- were all
        ``neighbourhood_capsule`` with empty params over ``NONE/GOAL_LOCAL/ACTION_LOCAL``.
        They render identically to one another, and applying two of them is idempotent, so
        they are one axis registered nine times. The damage is threefold: the reported space
        size is a product over axes and each copy multiplied it by three while adding no
        reachable rendering; the Pareto front fills with candidates that differ by
        candidate_id and not by output; and structural convergence becomes unreachable,
        because a meta-designer can always mint a fresh *name* for an axis that already
        exists. The brief's own worked example is ``dependency_capsule``, which is where the
        models were copying it from.

        The comparison is behavioural rather than by signature: two axes with different hooks
        or different value names that produce the same renderings are still the same axis.
        """

        if not transitions:
            return None, {"reason": "no transitions to test against"}

        def fingerprint(axis_name: str, values: tuple[str, ...]) -> list[str] | None:
            texts: list[str] = []
            for value in values:
                try:
                    compiler = compiler_factory({axis_name: value})
                    texts.append("\n@@\n".join(
                        compiler.render_text(transition) for transition in transitions))
                except Exception:  # noqa: BLE001
                    return None
            return texts

        mine = fingerprint(primitive.axis_name, primitive.values)
        if mine is None:
            return None, {"reason": "candidate axis failed to render"}
        # Compare as a set: two axes are the same dimension when they reach the same
        # renderings, whatever order or names their values carry.
        mine_set = set(mine)
        for other in self.active():
            if other.axis_name == primitive.axis_name:
                continue
            theirs = fingerprint(other.axis_name, other.values)
            if theirs is None:
                continue
            if set(theirs) == mine_set:
                return other.axis_name, {
                    "duplicate_of": other.axis_name,
                    "hook": primitive.hook,
                    "other_hook": other.hook,
                    "values": list(primitive.values),
                    "other_values": list(other.values),
                    "distinct_renderings": len(mine_set),
                    "transitions_tested": len(transitions),
                }
        return None, {"distinct_renderings": len(mine_set),
                      "compared_against": len(self.active())}

    def reject_duplicate(
        self, primitive: RegisteredPrimitive, evidence: dict[str, Any],
    ) -> None:
        """Record an accepted-then-duplicate axis instead of leaving it in the genome."""

        self.primitives.pop(primitive.axis_name, None)
        self.unimplementable.append({
            "status": "ACCEPTED_DUPLICATE",
            "axis_name": primitive.axis_name,
            "proposal_id": primitive.proposal_id,
            "generation": primitive.generation,
            "proposer": primitive.proposer,
            "reason": (
                "DUPLICATES_EXISTING_AXIS: renders identically to "
                f"{evidence.get('duplicate_of')}, so it adds no reachable representation"
            ),
            "evidence": evidence,
            "payload": {"hypothesis": primitive.hypothesis, "mechanism": primitive.mechanism},
        })

    def reject_inert(self, primitive: RegisteredPrimitive, evidence: dict[str, Any]) -> None:
        """Record an accepted-then-inert axis instead of leaving it in the genome."""

        self.primitives.pop(primitive.axis_name, None)
        self.unimplementable.append({
            "status": "ACCEPTED_UNIMPLEMENTABLE",
            "axis_name": primitive.axis_name,
            "proposal_id": primitive.proposal_id,
            "generation": primitive.generation,
            "proposer": primitive.proposer,
            "reason": "NO_OBSERVABLE_EFFECT: every value rendered identically on the sample",
            "evidence": evidence,
            "payload": {"hypothesis": primitive.hypothesis, "mechanism": primitive.mechanism},
        })

    def flush(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            json.dumps(primitive.to_dict(), sort_keys=True, separators=(",", ":"))
            for primitive in sorted(self.primitives.values(), key=lambda p: p.axis_name)
        ]
        lines += [
            json.dumps(row, sort_keys=True, separators=(",", ":"))
            for row in self.unimplementable
        ]
        self.path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")

    def rejection_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for row in self.unimplementable:
            status = row.get("status", "UNKNOWN")
            counts[status] = counts.get(status, 0) + 1
        return dict(sorted(counts.items()))

    def statistics(self) -> dict[str, Any]:
        return {
            "registry_version": REGISTRY_VERSION,
            "genome_schema_version": self.schema_version,
            "rejected_by_status": self.rejection_counts(),
            "accepted": len(self.primitives),
            "active": len(self.active()),
            "unimplementable": len(self.unimplementable),
            "hooks_available": sorted(HOOKS),
            "axes": sorted(self.primitives),
        }


def apply_primitives(
    document: Document, genome_values: dict[str, str], registry: PrimitiveRegistry,
) -> Document:
    """Run every active invented axis whose value is not NONE, in a deterministic order."""

    result = document
    for primitive in sorted(registry.active(), key=lambda p: p.axis_name):
        value = genome_values.get(primitive.axis_name, "NONE")
        if value == "NONE":
            continue
        params = dict(primitive.params)
        params.setdefault("values", list(primitive.values))
        result = HOOKS[primitive.hook](result, value, params)
    return result
