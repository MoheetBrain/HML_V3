#!/usr/bin/env python3
"""Generate the RepresentationGenome JSON Schema from the axis registry.

The schema is generated rather than hand-written so it can never drift from
``hml_v3.representation_search.genome.AXES``. A test re-runs this and compares.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hml_v3.representation_search.genome import (  # noqa: E402
    AXES,
    GENOME_SCHEMA_VERSION,
    space_size,
)

OUTPUT = ROOT / "schemas/representation_search_genome.schema.json"


def build_schema() -> dict:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://github.com/MoheetBrain/HML_V3/schemas/representation_search_genome.schema.json",
        "title": "HML V3 RepresentationGenome (search)",
        "description": (
            "One point in the representation architecture search space. A candidate "
            "language is fully determined by these axes together with the compiler version "
            "and the canonical state version; there is no per-candidate renderer code. "
            f"The space has {space_size():.3e} points across {len(AXES)} axes."
        ),
        "type": "object",
        "additionalProperties": False,
        "required": ["schema_version", "axes"],
        "properties": {
            "schema_version": {"const": GENOME_SCHEMA_VERSION},
            "candidate_id": {"type": "string", "pattern": "^R_[0-9a-f]{12}$"},
            "genome_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
            "label": {"type": "string"},
            "notes": {"type": "string"},
            "tags": {"type": "array", "items": {"type": "string"}},
            "axes": {
                "type": "object",
                "additionalProperties": False,
                "required": [axis.name for axis in AXES],
                "properties": {
                    axis.name: {
                        "enum": list(axis.values),
                        "default": axis.default,
                        "title": f"{axis.group} / search phase {axis.phase}",
                        "description": axis.description + (
                            "  Values expected to fail a hard gate: "
                            + ", ".join(axis.known_lossy) if axis.known_lossy else ""
                        ),
                    }
                    for axis in AXES
                },
            },
        },
    }


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(build_schema(), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {OUTPUT} with {len(AXES)} axes")


if __name__ == "__main__":
    main()
