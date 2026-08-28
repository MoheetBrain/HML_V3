"""Targeted corpus acquisition from the pinned LeanDojo trace.

`FM-020` recorded that goal linearization is unmeasurable on the current corpus: eleven
single-axis mutations of ``graph_serialization`` changed the measurement zero times, because
the corpus averages 1.01 goals per state. Acquiring *more* transitions at random would not
fix that — it would add more single-goal states in the same proportion.

This module therefore selects by structure rather than by chance. It streams the pinned
LeanDojo Benchmark 4 trace, measures each transition's structural profile from its
pretty-printed state, and fills declared strata: multi-goal states, deep local contexts, long
premise lists, and the tactic families that produce them.

The records it emits use the V1 source schema, so the existing prepare/replay/canonicalize
pipeline consumes them unchanged and every acquired transition still goes through fresh Lean
elaboration. Nothing here weakens provenance: it changes *which* theorems are elaborated, not
what counts as truth.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Iterator

#: A goal's target line. LeanDojo renders one turnstile per open goal.
TURNSTILE = re.compile(r"^⊢ ", re.MULTILINE)
#: A hypothesis line: ``name : type`` at the start of a line, before the turnstile.
HYPOTHESIS = re.compile(r"^[^\s⊢][^\n]*? : ", re.MULTILINE)
CASE_MARKER = re.compile(r"^case ", re.MULTILINE)
PREMISE_TAG = re.compile(r"<a>([^<]+)</a>")


def count_goals(state: str) -> int:
    if not state or state == "no goals":
        return 0
    return len(TURNSTILE.findall(state))


def count_hypotheses(state: str) -> int:
    if not state or state == "no goals":
        return 0
    return len(HYPOTHESIS.findall(state))


def binder_depth(state: str) -> int:
    """A cheap proxy: the deepest run of nested binders visible in the target."""

    depth = 0
    best = 0
    for character in state:
        if character in "(⟨[{":
            depth += 1
            best = max(best, depth)
        elif character in ")⟩]}":
            depth = max(0, depth - 1)
    return best


@dataclass
class StructuralProfile:
    goals_before: int
    goals_after: int
    hypotheses: int
    premises: int
    binder_depth: int
    state_bytes: int
    tactic_family: str
    multi_goal: bool = field(init=False)

    def __post_init__(self) -> None:
        self.multi_goal = self.goals_before >= 2

    def strata(self) -> dict[str, str]:
        return {
            "goal_count": (
                "1" if self.goals_before <= 1 else
                "2" if self.goals_before == 2 else
                "3-5" if self.goals_before <= 5 else ">5"
            ),
            "context_size": (
                "0-5" if self.hypotheses <= 5 else
                "6-15" if self.hypotheses <= 15 else
                "16-30" if self.hypotheses <= 30 else "31+"
            ),
            "premises": (
                "0" if self.premises == 0 else
                "1-2" if self.premises <= 2 else
                "3-5" if self.premises <= 5 else "6+"
            ),
            "binder_depth": (
                "0-3" if self.binder_depth <= 3 else
                "4-8" if self.binder_depth <= 8 else "9+"
            ),
            "tactic_family": self.tactic_family,
        }


def tactic_family(tactic: str) -> str:
    stripped = tactic.strip()
    if not stripped:
        return "unknown"
    return re.split(r"[\s\[({]", stripped, maxsplit=1)[0] or "unknown"


def profile(tactic_record: dict[str, Any]) -> StructuralProfile:
    before = tactic_record.get("state_before") or ""
    after = tactic_record.get("state_after") or ""
    annotated = tactic_record.get("annotated_tactic")
    annotated_text = annotated[0] if isinstance(annotated, list) and annotated else ""
    return StructuralProfile(
        goals_before=count_goals(before),
        goals_after=count_goals(after),
        hypotheses=count_hypotheses(before),
        premises=len(PREMISE_TAG.findall(annotated_text)),
        binder_depth=binder_depth(before),
        state_bytes=len(before.encode()),
        tactic_family=tactic_family(tactic_record.get("tactic") or ""),
    )


def premise_names(tactic_record: dict[str, Any]) -> list[str]:
    annotated = tactic_record.get("annotated_tactic")
    if not isinstance(annotated, list) or not annotated:
        return []
    return sorted(set(PREMISE_TAG.findall(annotated[0] or "")))


def iter_transitions(theorems: list[dict[str, Any]]) -> Iterator[dict[str, Any]]:
    """Yield one source record per traced tactic, in the V1 source schema.

    ``transition_index`` counts *deduplicated, theorem-scoped* tactics exactly as the
    downstream join does, so a record emitted here lands on the same tactic the join expects.
    """

    for theorem in theorems:
        traced = theorem.get("traced_tactics") or []
        if not traced:
            continue
        seen: set[tuple[str, str, str]] = set()
        index = 0
        for tactic_record in traced:
            before = tactic_record.get("state_before") or ""
            action = tactic_record.get("tactic") or ""
            after = tactic_record.get("state_after") or ""
            if before == "no goals" or "·" in action:
                continue
            signature = (before, action, after)
            if signature in seen:
                continue
            seen.add(signature)
            structural = profile(tactic_record)
            yield {
                "example_id": f"{theorem['file_path']}::{theorem['full_name']}::{index}",
                "source_file": theorem["file_path"],
                "theorem_id": theorem["full_name"],
                "transition_index": index,
                "source_family": "LEANDOJO_BENCHMARK_4_ACTIVE_ACQUISITION",
                "lean_official_split": "train",
                "proof_depth": index,
                "proof_length": len(traced),
                "lean": {
                    "raw_state_before": before,
                    "raw_state_after": after,
                    "raw_tactic": action,
                },
                "v3_formal_source_enrichment": {
                    "annotated_tactic": (
                        tactic_record["annotated_tactic"][0]
                        if isinstance(tactic_record.get("annotated_tactic"), list)
                        and tactic_record["annotated_tactic"] else action
                    ),
                    "premise_full_names": premise_names(tactic_record),
                    "theorem_start": theorem["start"],
                    "theorem_end": theorem["end"],
                },
                # The V1 source schema fields the existing prepare/replay pipeline reads.
                # Emitting them here means an acquired transition goes through exactly the
                # same join, elaboration and canonicalization as an inherited one.
                "state_before": {
                    "n_goals": structural.goals_before,
                    "hypotheses": [{"name": "", "type": ""}] * structural.hypotheses,
                    "target": "",
                },
                "state_after": {
                    "n_goals": structural.goals_after,
                    "hypotheses": [],
                    "target": "",
                },
                "observed_action": {
                    "effect_class": (
                        "CLOSE" if structural.goals_after == 0 else
                        "SPLIT" if structural.goals_after > structural.goals_before else
                        "ELIMINATE" if structural.goals_after < structural.goals_before else
                        "TRANSFORM"
                    ),
                },
                "compatibility": {"exclusion_reason": None, "frozen_hml_representable": True},
                "structural_profile": {
                    "goals_before": structural.goals_before,
                    "goals_after": structural.goals_after,
                    "hypotheses": structural.hypotheses,
                    "premises": structural.premises,
                    "binder_depth": structural.binder_depth,
                    "state_bytes": structural.state_bytes,
                    "tactic_family": structural.tactic_family,
                },
                "strata": structural.strata(),
            }
            index += 1


@dataclass
class AcquisitionRequest:
    """What the meta-designer asks for when a question is unanswerable on the corpus.

    This is the machine-readable form of a `CORPUS_ACQUISITION` proposal: it names the
    stratum that cannot be measured and how many examples would make it measurable.
    """

    reason: str
    stratum: str
    values: tuple[str, ...]
    desired_per_value: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "proposal_type": "CORPUS_ACQUISITION",
            "reason": self.reason,
            "stratum": self.stratum,
            "values": list(self.values),
            "desired_per_value": self.desired_per_value,
        }


def select_stratified(
    records: list[dict[str, Any]],
    requests: list[AcquisitionRequest],
    exclude_ids: set[str],
    available_files: set[str] | None = None,
    total_cap: int | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Fill each requested stratum, then top up with structural diversity.

    Selection is deterministic: candidates are ordered by a keyed hash of their id, so the
    same request against the same trace always produces the same campaign.
    """

    def key(record: dict[str, Any]) -> str:
        return hashlib.sha256(f"active-corpus-v1|{record['example_id']}".encode()).hexdigest()

    pool = [
        record for record in records
        if record["example_id"] not in exclude_ids
        and (available_files is None or record["source_file"] in available_files)
    ]
    pool.sort(key=key)

    chosen: dict[str, dict[str, Any]] = {}
    filled: dict[str, dict[str, int]] = {}
    for request in requests:
        filled[request.stratum] = {}
        for value in request.values:
            taken = 0
            for record in pool:
                if taken >= request.desired_per_value:
                    break
                if record["example_id"] in chosen:
                    continue
                if record["strata"].get(request.stratum) != value:
                    continue
                chosen[record["example_id"]] = record
                taken += 1
            filled[request.stratum][value] = taken

    if total_cap is not None and len(chosen) > total_cap:
        ordered = sorted(chosen.values(), key=key)[:total_cap]
        chosen = {record["example_id"]: record for record in ordered}

    selected = sorted(chosen.values(), key=lambda record: record["example_id"])
    manifest = {
        "pool_size": len(pool),
        "excluded": len(exclude_ids),
        "selected": len(selected),
        "requests": [request.to_dict() for request in requests],
        "filled": filled,
        "goal_count_distribution": _distribution(selected, "goal_count"),
        "context_size_distribution": _distribution(selected, "context_size"),
        "premises_distribution": _distribution(selected, "premises"),
        "binder_depth_distribution": _distribution(selected, "binder_depth"),
        "files": len({record["source_file"] for record in selected}),
        "selection_sha256": hashlib.sha256(
            json.dumps([record["example_id"] for record in selected], sort_keys=True).encode()
        ).hexdigest(),
    }
    return selected, manifest


def _distribution(records: list[dict[str, Any]], stratum: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in records:
        value = record["strata"].get(stratum, "unknown")
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def load_leandojo(path: Path) -> list[dict[str, Any]]:
    return json.loads(path.read_text())
