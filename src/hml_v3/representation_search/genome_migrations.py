"""Genome schema evolution: adding an axis without invalidating what came before.

The search must be able to grow its own space, and every candidate ever evaluated must remain
reproducible after it does. Those two requirements are only compatible if a new axis has an
explicit off position and old genomes are read as sitting at it.

That is the whole migration rule: an axis added at schema v2.N is absent from every genome
recorded under v2.<N, and absent means ``NONE``. A candidate evaluated before the axis existed
therefore re-renders byte-identically after it exists, which is what makes cross-generation
comparisons legitimate.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from hml_v3.representation_search.genome import AXES, Axis, RepresentationGenome
from hml_v3.representation_search.primitive_registry import PrimitiveRegistry


@dataclass(frozen=True)
class ExtendedSpace:
    """The base 42 axes plus every accepted invented axis."""

    axes: tuple[Axis, ...]
    schema_version: str

    @property
    def by_name(self) -> dict[str, Axis]:
        return {axis.name: axis for axis in self.axes}

    def names(self) -> list[str]:
        return [axis.name for axis in self.axes]

    def values(self) -> dict[str, list[str]]:
        return {axis.name: list(axis.values) for axis in self.axes}

    def defaults(self) -> dict[str, str]:
        return {axis.name: axis.default for axis in self.axes}


def extended_space(registry: PrimitiveRegistry) -> ExtendedSpace:
    invented = tuple(
        Axis(
            name=primitive.axis_name,
            group="INVENTED",
            phase="B",
            values=tuple(primitive.values),
            default="NONE",
            description=(
                f"Invented at generation {primitive.generation} by {primitive.proposer}. "
                f"{primitive.hypothesis}"
            ),
            known_lossy=(),
        )
        for primitive in sorted(registry.active(), key=lambda p: p.axis_name)
    )
    return ExtendedSpace(axes=AXES + invented, schema_version=registry.schema_version)


def migrate(values: dict[str, str], space: ExtendedSpace) -> dict[str, str]:
    """Read an older genome in the current space. Absent axes sit at their off position."""

    defaults = space.defaults()
    return {name: values.get(name, defaults[name]) for name in space.names()}


def space_size(space: ExtendedSpace) -> int:
    total = 1
    for axis in space.axes:
        total *= len(axis.values)
    return total


class ExtendedGenome:
    """A genome over the extended space.

    ``RepresentationGenome`` validates against the frozen 42 axes, so invented-axis values are
    carried alongside it rather than inside it. The candidate id hashes both, which means a
    candidate that differs only in an invented axis is a genuinely different candidate.
    """

    def __init__(self, base: RepresentationGenome, invented: dict[str, str] | None = None) -> None:
        self.base = base
        self.invented = dict(invented or {})

    def get(self, axis: str) -> str:
        if axis in self.invented:
            return self.invented[axis]
        try:
            return self.base.get(axis)
        except KeyError:
            return "NONE"

    def resolved(self, space: ExtendedSpace) -> dict[str, str]:
        merged = dict(self.base.resolved())
        for axis in space.axes:
            if axis.group == "INVENTED":
                merged[axis.name] = self.invented.get(axis.name, "NONE")
        return merged

    def with_invented(self, axis: str, value: str) -> "ExtendedGenome":
        invented = dict(self.invented)
        if value == "NONE":
            invented.pop(axis, None)
        else:
            invented[axis] = value
        return ExtendedGenome(self.base, invented)

    def candidate_id(self) -> str:
        import hashlib
        import json

        if not self.invented:
            return self.base.candidate_id()
        payload = json.dumps(
            {"base": self.base.sha256(), "invented": dict(sorted(self.invented.items()))},
            sort_keys=True, separators=(",", ":"),
        )
        return f"R_{hashlib.sha256(payload.encode()).hexdigest()[:12]}"

    def to_dict(self) -> dict[str, Any]:
        payload = self.base.to_dict()
        payload["candidate_id"] = self.candidate_id()
        payload["invented_axes"] = dict(sorted(self.invented.items()))
        return payload

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "ExtendedGenome":
        return cls(
            RepresentationGenome.from_dict(value),
            value.get("invented_axes") or {},
        )
