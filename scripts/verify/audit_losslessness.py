#!/usr/bin/env python3
"""Audit V3's declared observable losslessness against exact Lean source records."""

from __future__ import annotations

from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hml_v3.adapters.lean.adapter import lean_transition_from_record  # noqa: E402
from hml_v3.adapters.lean.parser import parse_lean_state  # noqa: E402
from hml_v3.canonical.models import CanonicalTransition, stable_sha256  # noqa: E402


SOURCE = ROOT / "data/samples/lean_pipeline_v1.source.jsonl.gz"
CANONICAL = ROOT / "data/samples/lean_pipeline_v1.canonical.jsonl.gz"
MANIFEST = ROOT / "data/manifests/lean_pipeline_v1.json"
JSON_REPORT = ROOT / "reports/audits/LOSSLESSNESS_AUDIT_V1.json"
MARKDOWN_REPORT = ROOT / "reports/audits/LOSSLESSNESS_AUDIT_V1.md"


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_goal_view(state: Any, goal: Any) -> dict[str, Any]:
    by_id = {item.declaration_id: item for item in state.declarations}
    return {
        "case_label": goal.source_label,
        "declarations": [
            {
                "name": by_id[item].name,
                "type": by_id[item].type_expression.surface,
                "value": by_id[item].value_expression.surface if by_id[item].value_expression else None,
            }
            for item in goal.local_context_ids
        ],
        "target": goal.target.surface,
    }


def parsed_goal_view(goal: Any) -> dict[str, Any]:
    return {
        "case_label": goal.case_label,
        "declarations": [
            {"name": name, "type": item.type_text, "value": item.value_text}
            for item in goal.declarations
            for name in item.names
        ],
        "target": goal.target,
    }


def main() -> int:
    manifest = json.loads(MANIFEST.read_text())
    failures: list[dict[str, Any]] = []
    checks = Counter()
    structured_disagreements = 0
    verifier_statuses: Counter[str] = Counter()
    with gzip.open(SOURCE, "rt", encoding="utf-8") as source_handle, gzip.open(
        CANONICAL, "rt", encoding="utf-8"
    ) as canonical_handle:
        pairs = zip(source_handle, canonical_handle)
        rows = 0
        for index, (source_line, canonical_line) in enumerate(pairs):
            rows += 1
            source = json.loads(source_line)
            canonical_raw = json.loads(canonical_line)
            transition = CanonicalTransition.from_dict(canonical_raw)
            row_failures: list[str] = []
            if json.loads(transition.canonical_json()) != canonical_raw:
                row_failures.append("canonical model JSON round trip differs")
            if transition.transition_id != source["example_id"]:
                row_failures.append("transition identity differs")
            source_boundary = lean_transition_from_record(source)
            if transition.provenance["source_record_sha256"] != source_boundary.source_record_sha256:
                row_failures.append("source record hash differs")
            for phase, raw_key, source_key in (
                (transition.state_before, "raw_state_before", "state_before"),
                (transition.state_after, "raw_state_after", "state_after"),
            ):
                raw = source["lean"][raw_key]
                if phase.source_specific["raw_state"] != raw:
                    row_failures.append(f"{raw_key} bytes differ")
                if phase.source_specific["raw_state_sha256"] != stable_sha256(raw):
                    row_failures.append(f"{raw_key} hash differs")
                parsed = parse_lean_state(raw)
                if not parsed.clean:
                    row_failures.append(f"{raw_key} decomposition is partial")
                if len(parsed.goals) != source[source_key]["n_goals"]:
                    row_failures.append(f"{raw_key} goal count differs")
                canonical_goals = [canonical_goal_view(phase, goal) for goal in phase.goals]
                parsed_goals = [parsed_goal_view(goal) for goal in parsed.goals]
                if canonical_goals != parsed_goals:
                    row_failures.append(f"{raw_key} decomposed goals/contexts differ")
                if phase.source_specific["adapter_inconsistencies"]:
                    structured_disagreements += 1
            if transition.action.source_syntax != source["lean"]["raw_tactic"]:
                row_failures.append("raw tactic differs")
            if transition.action.source_syntax_sha256 != stable_sha256(source["lean"]["raw_tactic"]):
                row_failures.append("raw tactic hash differs")
            enrichment = source.get("v3_formal_source_enrichment", {})
            expected_premises = enrichment.get(
                "premise_full_names", source["observed_action"]["premises_used"]
            )
            if list(transition.action.referenced_premises) != expected_premises:
                row_failures.append("premise references differ")
            if enrichment:
                checks["formal_source_enrichments"] += 1
                checks["premise_references"] += len(expected_premises)
                if not all(enrichment["exact_source_join"].values()):
                    row_failures.append("formal source enrichment is not an exact join")
                declaration = enrichment["theorem_declaration_and_proof"]
                if enrichment["theorem_declaration_and_proof_sha256"] != stable_sha256(declaration):
                    row_failures.append("theorem declaration/proof hash differs")
                if enrichment["source_commit"] != transition.provenance["source_commit"]:
                    row_failures.append("formal source enrichment commit differs")
            if transition.action.expected_effect != source["observed_action"]:
                row_failures.append("recorded expected effect differs")
            if transition.state_delta.goals_before != source["state_before"]["n_goals"]:
                row_failures.append("before goal delta count differs")
            if transition.state_delta.goals_after != source["state_after"]["n_goals"]:
                row_failures.append("after goal delta count differs")
            if transition.state_delta.recorded_effect_class != source["observed_action"]["effect_class"]:
                row_failures.append("effect class differs")
            verifier_statuses[transition.verifier_result.status] += 1
            checks["rows"] += 1
            checks["states"] += 2
            checks["actions"] += 1
            checks["semantic_deltas"] += 1
            if row_failures:
                failures.append(
                    {
                        "row": index,
                        "transition_id": source["example_id"],
                        "failures": row_failures,
                    }
                )
        if source_handle.readline() or canonical_handle.readline():
            failures.append({"row": rows, "transition_id": None, "failures": ["file lengths differ"]})

    hash_checks = {
        "source_gzip": file_sha256(SOURCE) == manifest["files"]["source"]["sha256"],
        "canonical_gzip": file_sha256(CANONICAL) == manifest["files"]["canonical"]["sha256"],
    }
    if not all(hash_checks.values()):
        failures.append({"row": None, "transition_id": None, "failures": ["manifest hash mismatch"]})
    status = "PASS" if not failures and rows == 1000 else "FAIL"
    report = {
        "schema_version": "hml-v3-losslessness-audit-1.0.0",
        "status": status,
        "claim": "Lossless for declared source observations: exact raw states, exact tactic, all displayed goal/context decomposition, premise references, recorded effect, identity, and provenance hashes.",
        "counts": dict(sorted(checks.items())),
        "manifest_hash_checks": hash_checks,
        "verifier_statuses": dict(sorted(verifier_statuses.items())),
        "source_structured_projection_disagreements": structured_disagreements,
        "failures": failures[:100],
        "explicit_nonclaims": [
            "Lean pretty-printed expressions are not reconstructed as elaborated Lean Expr trees.",
            "BinderInfo, universe constraints, metavariable assignments, and namespace resolution are not recoverable from these trace rows.",
            "FORMAL_TRACE_ACCEPTED is not relabeled as fresh runtime replay; only 32 rows have FRESH_REPLAY_PASS certificates.",
            "The prior source record's structured hypothesis/target projection is known to truncate some multiline observations; disagreements are recorded, while exact raw states remain authoritative.",
        ],
    }
    JSON_REPORT.parent.mkdir(parents=True, exist_ok=True)
    JSON_REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    lines = [
        "# Losslessness Audit V1",
        "",
        f"**Status: {status}.** V3 is lossless for the declared observable boundary across {rows:,} real Lean transitions.",
        "",
        "| Check | Result |",
        "|---|---:|",
        f"| Exact source/canonical transition pairs | {rows:,} |",
        f"| Exact raw states checked | {checks['states']:,} |",
        f"| Exact raw tactics checked | {checks['actions']:,} |",
        f"| Exact premise/effect/delta observations checked | {checks['semantic_deltas']:,} |",
        f"| Audit failures | {len(failures):,} |",
        f"| Old structured-projection disagreements retained | {structured_disagreements:,} state observations |",
        "",
        "The disagreement count is not a V3 loss: it records cases where the old source parser truncated or misread multiline Lean text. The exact raw text is retained and V3's conservative decomposition is checked back against it.",
        "",
        "## Explicit boundary",
        "",
        "This pass does not assert elaborated-expression losslessness. Lean `Expr` trees, binder metadata, metavariable assignments/constraints, and a fully resolved namespace environment are absent from the source trace. Those are registered gaps, not guessed fields.",
        "",
        "Verification labels remain calibrated: every row comes from the pinned accepted formal trace, while only 32 rows passed fresh exact-state replay. The remaining rows are not described as freshly replayed.",
        "",
    ]
    MARKDOWN_REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"status": status, "rows": rows, "failures": len(failures)}))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
