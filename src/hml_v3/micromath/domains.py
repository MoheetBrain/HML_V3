"""Mathematical domain classification, with confidence recorded rather than assumed.

`MICROMATH §29` forbids classifying a domain from a filename when that is unreliable. The
existing corpus already carries a ``corpus_metadata.domain`` field, but it is the first path
segment: for a transition under ``.lake/packages/batteries/...`` it reads ``packages``, which
is not a mathematical domain at all. Classification here is by Mathlib module, every mapping
is declared, and anything unmapped becomes ``MIXED`` rather than being forced into a bucket.
"""

from __future__ import annotations

from typing import Any

ALGEBRA = "ALGEBRA"
GEOMETRY = "GEOMETRY"
CALCULUS_ANALYSIS = "CALCULUS_ANALYSIS"
PROBABILITY_STATISTICS = "PROBABILITY_STATISTICS"
LOGIC_SET_THEORY = "LOGIC_SET_THEORY"
LINEAR_ALGEBRA = "LINEAR_ALGEBRA"
MIXED = "MIXED"

DOMAINS: tuple[str, ...] = (
    ALGEBRA, GEOMETRY, CALCULUS_ANALYSIS,
    PROBABILITY_STATISTICS, LOGIC_SET_THEORY, LINEAR_ALGEBRA,
)

#: Mathlib top-level module -> (domain, confidence). HIGH means the module *is* the domain.
#: MEDIUM means the module belongs to the domain by convention but draws heavily on another,
#: and a reader could reasonably disagree; those are reported separately.
MODULE_MAP: dict[str, tuple[str, str]] = {
    "Algebra": (ALGEBRA, "HIGH"),
    "RingTheory": (ALGEBRA, "HIGH"),
    "GroupTheory": (ALGEBRA, "HIGH"),
    "FieldTheory": (ALGEBRA, "HIGH"),
    "Geometry": (GEOMETRY, "HIGH"),
    "AlgebraicGeometry": (GEOMETRY, "MEDIUM"),
    "Analysis": (CALCULUS_ANALYSIS, "HIGH"),
    "Dynamics": (CALCULUS_ANALYSIS, "MEDIUM"),
    "Probability": (PROBABILITY_STATISTICS, "HIGH"),
    "MeasureTheory": (PROBABILITY_STATISTICS, "HIGH"),
    "SetTheory": (LOGIC_SET_THEORY, "HIGH"),
    "Logic": (LOGIC_SET_THEORY, "HIGH"),
    "Order": (LOGIC_SET_THEORY, "MEDIUM"),
    "Computability": (LOGIC_SET_THEORY, "MEDIUM"),
    "LinearAlgebra": (LINEAR_ALGEBRA, "HIGH"),
}


def classify(transition: dict[str, Any]) -> tuple[str, str]:
    """``(domain, confidence)`` for one canonical transition."""

    source = (transition.get("corpus_metadata") or {}).get("source_file") or ""
    parts = source.split("/")
    if len(parts) > 1 and parts[0] == "Mathlib":
        mapped = MODULE_MAP.get(parts[1])
        if mapped is not None:
            return mapped
        return MIXED, "UNMAPPED_MATHLIB_MODULE"
    return MIXED, "NOT_MATHLIB"
