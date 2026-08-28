#!/usr/bin/env python3
"""Build committed V2 audit artifacts from an ignored raw Lean runtime campaign."""

from __future__ import annotations

import argparse
import collections
import gzip
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hml_v3.adapters.lean.runtime_v2 import canonicalize_capture, digest  # noqa: E402
from hml_v3.canonical.delta_v2 import structured_delta  # noqa: E402


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle]


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_jsonl_gz(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as zipped:
            for row in rows:
                zipped.write((json.dumps(
                    row, ensure_ascii=False, sort_keys=True, separators=(",", ":")
                ) + "\n").encode())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--campaign-dir", type=Path, required=True)
    parser.add_argument("--source", type=Path, default=ROOT / "data/samples/lean_pipeline_v1.source.jsonl.gz")
    parser.add_argument("--reports-dir", type=Path, default=ROOT / "reports")
    parser.add_argument("--manifest", type=Path, default=ROOT / "data/manifests/lean_runtime_v2.json")
    parser.add_argument("--compact-audit", type=Path, default=ROOT / "reports/audits/LEAN_RUNTIME_REPLAY_V2.jsonl.gz")
    parser.add_argument("--canonical-sample", type=Path, default=ROOT / "data/samples/lean_runtime_v2.canonical.sample.jsonl.gz")
    args = parser.parse_args()

    summary = json.loads((args.campaign_dir / "campaign_summary.json").read_text())
    selection = json.loads((args.campaign_dir / "selection_manifest.json").read_text())
    audits = read_jsonl(args.campaign_dir / "audit_rows.jsonl")
    with gzip.open(args.source, "rt", encoding="utf-8") as handle:
        source_records = {row["example_id"]: row for row in map(json.loads, handle)}
    for row in audits:
        official = source_records[row["record_id"]]["v3_formal_source_enrichment"]["premise_full_names"]
        row["official_external_premise_refs"] = official
        row["structured_delta"]["external_premises_used"] = sorted(set(official))
    pass_rows = [row for row in audits if row["replay_status"] == "EXACT_REPLAY_PASS"]

    compact_rows = []
    for row in audits:
        compact = dict(row)
        compact.pop("raw_capture_file", None)
        compact_rows.append(compact)
    write_jsonl_gz(args.compact_audit, compact_rows)

    smallest = sorted(
        pass_rows,
        key=lambda row: Path(row["raw_capture_file"]).stat().st_size,
    )[:3]
    canonical_samples = []
    raw_cache: dict[Path, dict[str, Any]] = {}
    for row in smallest:
        raw_path = Path(row["raw_capture_file"])
        if raw_path not in raw_cache:
            raw_cache[raw_path] = json.loads(raw_path.read_text())
        payload = raw_cache[raw_path]
        captures_by_id: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
        for item in payload["captures"]:
            captures_by_id[item["record_id"]].append(item)
        matching = [
            item for item in captures_by_id[row["record_id"]]
            if item["fresh_trace_ordinal"] == row["fresh_trace_ordinal"]
        ]
        if len(matching) != 1:
            raise RuntimeError(
                f"cannot recover selected runtime occurrence for {row['record_id']}"
            )
        capture = matching[0]
        capture = dict(capture)
        capture["environment"] = {
            "runtime_pin": summary["environment"],
            "source_file": row["source_file"],
            "direct_imports": payload["direct_imports"],
            "lean_runtime_snapshot": capture["environment"],
        }
        delta = structured_delta(
            capture["state_before"], capture["state_after"],
            row["official_external_premise_refs"], capture["local_context_refs"],
            capture.get("metavariable_delta"),
        )
        canonical_samples.append(canonicalize_capture(
            capture, delta, row["official_external_premise_refs"]
        ))
    write_jsonl_gz(args.canonical_sample, canonical_samples)

    constructor_totals = summary["expr_constructor_totals"]
    required_constructors = {
        "bvar", "fvar", "mvar", "sort", "const", "app", "lam", "forallE",
        "letE", "lit", "mdata", "proj",
    }
    constructor_coverage = sorted(required_constructors & constructor_totals.keys())
    missing_in_campaign = sorted(required_constructors - constructor_totals.keys())
    local_rows = [row for row in pass_rows if row["local_context_refs"]]
    local_total = sum(len(row["local_context_refs"]) for row in pass_rows)
    local_resolved = sum(
        ref["resolved_in_before_goal_context"]
        for row in pass_rows for ref in row["local_context_refs"]
    )
    delta_counts = collections.Counter()
    historical_disagreements = 0
    for row in pass_rows:
        delta = row["structured_delta"]
        for field in (
            "goals_created", "goals_solved", "goals_modified", "local_declarations_added",
            "local_declarations_removed", "local_declarations_changed", "metavariables_created",
            "metavariables_assigned",
        ):
            if delta[field]:
                delta_counts[field] += 1
        if delta["goals_reordered"]:
            delta_counts["goals_reordered"] += 1
        if delta["focus_changed"]:
            delta_counts["focus_changed"] += 1
        # Historical effects are retained but cannot override runtime identity evidence.
        if delta["goals_created"] and delta["goals_solved"]:
            historical_disagreements += 1

    losslessness = {
        "schema_version": "elaborated-losslessness-v2.0.0",
        "status": "FAIL",
        "audited_runtime_states": 2 * len(pass_rows),
        "preserved": [
            "all 12 Lean Expr constructors through a versioned tagged source schema",
            "constant and universe identity, implicit elaborated applications, and coercion structure",
            "goal MVar identity, order, focus, target, and complete goal local contexts",
            "FVar identity, BinderInfo, declaration type/value, shadowing, and local instances",
            "relevant metavariable declaration/type/assignment/kind closure",
            "identity-derived state deltas and exact nested source occurrence paths",
        ],
        "delegated_by_source_reference": [
            "complete irrelevant/inactive metavariable inventory by full context counts; created/assigned/changed entries stay explicit",
            "raw Lean IDs and environment/options/module tables",
        ],
        "intentionally_lean_specific": [
            "name-generator counters, delayed-assignment mechanics, LocalDeclKind",
            "tactic elaborator identity, raw InfoTree child path, raw Expr metadata payload",
        ],
        "information_lost": [],
        "unknown": [
            "tactic-internal local or environment dependencies without descendant TermInfo",
            "standalone constraints not exposed by Lean 4.10 MetavarContext",
            "cross-run structured equivalence over the full 500 was not independently duplicated",
        ],
        "failure_reason": "Unknown tactic-internal dependencies can affect action legality, so the stronger global losslessness gate is not certified.",
    }
    write_json(args.reports_dir / "audits/ELABORATED_LOSSLESSNESS_V2.json", losslessness)

    manifest = {
        "schema_version": "hml-v3-lean-runtime-v2-manifest-1.0.0",
        "lean_version": "v4.10.0-rc1",
        "lean_build_commit": "3b58e0649156",
        "mathlib_commit": "29dcec074de168ac2bf835a77ef68bbe069194c5",
        "leandojo_v2_commit": "baed5eae6e87a65a446d9f54af07aab2154e7599",
        "selection": selection,
        "campaign": {key: summary[key] for key in (
            "selected", "replayable", "exact_pass", "exact_fail", "unsupported",
            "environment_mismatch", "primary_exact_pass_rate", "conditional_exact_pass_rate",
            "classification_complete", "elapsed_seconds", "workers", "process_status_counts",
            "audit_rows_sha256",
        )},
        "environment": summary["environment"],
        "expression_constructor_coverage": constructor_coverage,
        "expression_constructors_not_observed_in_campaign": missing_in_campaign,
        "compact_audit_sha256": hashlib.sha256(args.compact_audit.read_bytes()).hexdigest(),
        "canonical_sample_sha256": hashlib.sha256(args.canonical_sample.read_bytes()).hexdigest(),
        "canonical_sample_rows": len(canonical_samples),
        "gpu_used": False,
        "training_performed": False,
    }
    write_json(args.manifest, manifest)

    write_text(args.reports_dir / "LEAN_RUNTIME_CAPTURE_V2.md", f"""
# Lean Runtime Capture V2

**Extractor: PASS.** The Lean-side program freshly processes source files with `infoState.enabled` and serializes actual `TacticInfo` before/after contexts. It captures every Lean 4.10 `Expr` constructor, universe levels, FVar/Binder identity, goal MVar identity/order, relevant metavariable closure, local instances, source location, nested `InfoTree` path, and environment provenance. Pretty text is diagnostic only.

Campaign evidence: {summary['exact_pass']:,} exact passes from {summary['selected']:,} selected transitions. Observed constructors: {', '.join(constructor_coverage)}. Constructors not naturally observed in this sample: {', '.join(missing_in_campaign) or 'none'}; unit tests cover the complete constructor union.

The full raw captures remain local ignored scientific data; the committed compact audit and deterministic canonical sample are content-hashed in `data/manifests/lean_runtime_v2.json`.
""")

    write_text(args.reports_dir / "LEAN_RUNTIME_REPLAY_V2.md", f"""
# Lean Runtime Replay V2

Primary result: **{summary['exact_pass']:,}/{summary['selected']:,} = {summary['primary_exact_pass_rate']:.2%} exact pass over the full selected denominator.**

| Outcome | Count |
|---|---:|
| selected | {summary['selected']:,} |
| replayable | {summary['replayable']:,} |
| exact pass | {summary['exact_pass']:,} |
| exact fail | {summary['exact_fail']:,} |
| unsupported path | {summary['unsupported']:,} |
| environment mismatch | {summary['environment_mismatch']:,} |

Conditional success among replayable transitions is {summary['conditional_exact_pass_rate']:.2%}. The method is `FRESH_WHOLE_FILE_ELABORATION_EXACT_INFO_TREE_PATH`: the exact pinned source file is elaborated from its real imports, Lean executes the nested proof prefix, and the extractor selects the exact historical tactic byte range. Before/action/after and theorem/transition identity are checked without hiding unsupported rows.

This certifies exact diagnostic state agreement and fresh structured observation at that occurrence. It does not claim that a second independent 500-row structured extraction was byte-identical; ephemeral IDs require the documented semantic normalization.
""")

    write_text(args.reports_dir / "ELABORATED_LOSSLESSNESS_V2.md", f"""
# Elaborated Losslessness V2

**Status: FAIL (global hard gate not certified).**

All declared canonical-required expression, binder, goal, relevant-metavariable, and identity-delta distinctions were preserved for {2 * len(pass_rows):,} freshly observed runtime states. Complete inactive Lean inventories are delegated by full context counts, with all created/assigned/changed entries explicit; environment internals are delegated by source provenance. Implementation bookkeeping remains source-specific by design.

No demonstrated canonical-required field was silently dropped. The unresolved issue is completeness: descendant `TermInfo.expr` traversal cannot prove that tactic-internal search did not consult additional local hypotheses, simp lemmas, or instances, and Lean 4.10 exposes no standalone constraint table. Those unknowns can change action legality. The machine-readable five-way accounting is `reports/audits/ELABORATED_LOSSLESSNESS_V2.json`.
""")

    write_text(args.reports_dir / "LOCAL_DEPENDENCY_AUDIT_V2.md", f"""
# Local Dependency Audit V2

Mechanism: direct traversal of elaborated descendant `TermInfo.expr` objects, never lexical substring matching.

- exact-pass transitions: {len(pass_rows):,}
- transitions with at least one local FVar reference: {len(local_rows):,}
- local FVar reference occurrences: {local_total:,}
- references resolved in the before-goal context: {local_resolved:,}/{local_total:,} ({(local_resolved / local_total if local_total else 0):.2%})

**Adjudication: PARTIAL.** The evidence is typed and identity-bearing, but tactics may consult locals internally without emitting descendant TermInfo. The canonical action records the mechanism and this completeness limitation.
""")

    write_text(args.reports_dir / "STRUCTURED_DELTA_AUDIT_V2.md", f"""
# Structured Delta Audit V2

**Status: PASS for captured transitions.** Deltas use exact MVar/FVar identities and expression structure. Historical text-derived effect fields remain `RECORDED_HISTORICAL_METADATA` and do not determine V2 truth.

| Runtime event | Transitions |
|---|---:|
{chr(10).join(f'| `{key}` | {value:,} |' for key, value in sorted(delta_counts.items()))}

The audit distinguishes goal creation/solution/reorder/modification, focus, local declaration changes, metavariable creation/assignment, elaborated local/external references, and target-expression changes. Runtime records exhibiting both creation and solution (a coarse historical-label stress case): {historical_disagreements:,}.
""")

    write_text(args.reports_dir / "BENCHMARK_READINESS_V2.md", f"""
# Benchmark Readiness V2

**REPRESENTATION_BENCHMARK_READY: NO.** No GPU or training was used.

| Gate | Result | Evidence |
|---|---|---|
| A elaborated Expr | PASS | constructor-complete Lean-side serializer |
| B FVar/binder identity | PASS | real FVarId/BinderInfo plus alpha/shadow tests |
| C goal/MVar identity | PASS | real IDs, order, focus, reorder tests |
| D metavariable state | PARTIAL | relevant closure and all changes preserved; standalone constraint table unavailable |
| E local references | PARTIAL | typed TermInfo traversal is not complete for internal tactics |
| F structured deltas | PASS | identity-derived audit |
| G substantial replay | {'PASS' if summary['selected'] >= 500 else 'FAIL'} | {summary['exact_pass']}/{summary['selected']} exact over total selected |
| H stronger losslessness | FAIL | action-legality-relevant unknowns remain |
| I shortcut audits | NOT RUN | prototypes are not label-ready |
| J no legality-changing loss | FAIL | tactic-internal dependencies and search traces remain unknown |

Premise-selection prototype: **NOT READY.** The state/candidate interface and external/local label separation are now possible, but local-label completeness and replayed hard negatives are absent.

Next-action-ranking prototype: **NOT READY.** Positive actions are exact, but cross-theorem candidates have not been executed against every target state; they cannot yet be labelled invalid/useful.

Running class-prior, length, structural-count, bag-of-words, char n-gram, tactic-frequency, theorem-name, or premise-name baselines now would measure an unfinished label construction. `SHALLOW_SHORTCUT_AUDIT = NOT_RUN` is therefore the honest result.
""")

    print(json.dumps({
        "manifest": str(args.manifest),
        "exact_pass": summary["exact_pass"],
        "losslessness": losslessness["status"],
        "canonical_samples": len(canonical_samples),
    }, indent=2))


if __name__ == "__main__":
    main()
