"""Selecting base states for the lab.

Two exclusions matter and both are enforced here rather than remembered.

`SEALED_FINAL_V2` is never opened: the lab is built from ``search_pool_v2``, which is the
corpus with the seal already removed, and a path guard refuses anything that looks sealed.

The 56 transitions the converged global search actually measured on are also excluded. The
pool holds 918 transitions but the controller only ever sampled 32 dev and 24 validation
rows, so 862 states were never seen by the search that produced the candidates this lab is
about to audit. Building the lab from those 862 keeps the diagnosis independent of the
optimisation that chose the candidates.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from hml_v3.representation_search.corpus import load_corpus
from hml_v3.representation_search.sampling import structural_sample
from hml_v3.representation_search.sealing import split_search_pool

SEALED_MARKERS = ("sealed_final", "sealed_v2", "SEALED")


def refuse_sealed(path: Path) -> None:
    resolved = str(path.resolve())
    for marker in SEALED_MARKERS:
        if marker in resolved:
            raise SystemExit(
                f"REFUSED: {resolved} looks like a sealed split. MicroMath Lab is never "
                "built from SEALED_FINAL_V2."
            )


def search_measured_ids(pool: list[dict[str, Any]], dev_sample: int = 32,
                        validation_sample: int = 24, seed: int = 20260828) -> set[str]:
    """Exactly the transitions the converged global search evaluated candidates on."""

    split = split_search_pool(pool)
    measured = structural_sample(split.dev, dev_sample, seed)
    measured += structural_sample(split.validation, validation_sample, seed)
    return {row["transition_id"] for row in measured}


def load_base_pool(path: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    refuse_sealed(path)
    pool = load_corpus(path)
    measured = search_measured_ids(pool)
    untouched = [row for row in pool if row["transition_id"] not in measured]
    return untouched, {
        "corpus": str(path),
        "pool_transitions": len(pool),
        "excluded_because_the_global_search_measured_them": len(measured),
        "available_base_states": len(untouched),
        "sealed_final_v2": "NOT OPENED",
    }


def load_split(directory: Path, name: str) -> list[dict[str, Any]]:
    """Read one lab split. Shard-aware, and tolerant of the older single-file layout."""

    from hml_v3.representation_search.corpus import load_corpus as _load, shard_paths

    base = directory / f"{name}.jsonl.gz"
    if shard_paths(base):
        return _load(base)
    plain = directory / f"{name}.jsonl"
    if plain.exists():
        return [json.loads(line) for line in plain.read_text().splitlines() if line.strip()]
    return []
