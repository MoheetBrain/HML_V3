#!/usr/bin/env python3
"""Run and audit the pinned Lean runtime extraction campaign.

Each source file is freshly elaborated by Lean.  The selected `TacticInfo` is identified by
the exact source byte range recovered from the immutable historical trace, so nested tactic
execution follows Lean's real info-tree path rather than a guessed flat tactic prefix.
"""

from __future__ import annotations

import argparse
import collections
import concurrent.futures
import gzip
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hml_v3.canonical.delta_v2 import structured_delta as canonical_structured_delta  # noqa: E402


LEAN_VERSION = "v4.10.0-rc1"
LEAN_BUILD_COMMIT = "3b58e0649156"
MATHLIB_COMMIT = "29dcec074de168ac2bf835a77ef68bbe069194c5"


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def text_sha(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n")


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(canonical_json(row) + "\n")


def load_source_records(path: Path) -> dict[str, dict[str, Any]]:
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        return {row["example_id"]: row for row in map(json.loads, handle)}


def run_checked(command: list[str], cwd: Path, timeout: int) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
        check=False,
    )


def run_job(
    job: dict[str, Any], runtime_root: Path, extractor: Path, timeout: int,
) -> dict[str, Any]:
    output = Path(job["output_file"])
    output.parent.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    command = [
        "lake", "env", "lean", "--run", str(extractor), job["source_file"],
        job["target_file"], str(output),
    ]
    try:
        completed = run_checked(command, runtime_root, timeout)
        status = "PROCESS_PASS" if completed.returncode == 0 else "PROCESS_FAIL"
        error = None
    except subprocess.TimeoutExpired as exc:
        completed = None
        status = "PROCESS_TIMEOUT"
        error = str(exc)
    return {
        **job,
        "process_status": status,
        "returncode": completed.returncode if completed else None,
        "elapsed_seconds": time.monotonic() - started,
        "stdout": completed.stdout if completed else "",
        "stderr": completed.stderr if completed else "",
        "error": error,
    }


def goal_map(state: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {goal["mvar_id"]: goal for goal in state["goals"]}


def local_map(state: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for goal in state["goals"]:
        for decl in goal.get("local_context", []):
            result[decl["fvar_id"]] = decl
    return result


def mvar_map(state: dict[str, Any]) -> dict[str, dict[str, Any]]:
    inventory = state["metavariable_context"]["declaration_inventory"]
    return {decl["mvar_id"]: decl for decl in inventory}


def changed_ids(
    before: dict[str, dict[str, Any]], after: dict[str, dict[str, Any]],
) -> list[str]:
    return sorted(
        key for key in before.keys() & after.keys()
        if digest(before[key]) != digest(after[key])
    )


def structured_delta(capture: dict[str, Any]) -> dict[str, Any]:
    before_state, after_state = capture["state_before"], capture["state_after"]
    before_goals, after_goals = goal_map(before_state), goal_map(after_state)
    before_order, after_order = before_state["goal_order"], after_state["goal_order"]
    shared_goals = before_goals.keys() & after_goals.keys()
    before_locals, after_locals = local_map(before_state), local_map(after_state)
    before_mvars, after_mvars = mvar_map(before_state), mvar_map(after_state)
    assigned = sorted(
        key for key in before_mvars.keys() & after_mvars.keys()
        if not before_mvars[key]["is_assigned"] and after_mvars[key]["is_assigned"]
    )
    return {
        "delta_source": "ELABORATED_STABLE_IDENTITIES",
        "goals_created": sorted(after_goals.keys() - before_goals.keys()),
        "goals_solved": sorted(before_goals.keys() - after_goals.keys()),
        "goals_preserved": sorted(shared_goals),
        "goals_reordered": (
            set(before_order) == set(after_order) and before_order != after_order
        ),
        "goals_modified": sorted(
            key for key in shared_goals
            if digest(before_goals[key].get("target")) != digest(after_goals[key].get("target"))
            or [d["fvar_id"] for d in before_goals[key].get("local_context", [])]
            != [d["fvar_id"] for d in after_goals[key].get("local_context", [])]
        ),
        "focus_before": before_state["focused_goal_id"],
        "focus_after": after_state["focused_goal_id"],
        "focus_changed": before_state["focused_goal_id"] != after_state["focused_goal_id"],
        "local_declarations_added": sorted(after_locals.keys() - before_locals.keys()),
        "local_declarations_removed": sorted(before_locals.keys() - after_locals.keys()),
        "local_declarations_changed": changed_ids(before_locals, after_locals),
        "metavariables_created": sorted(after_mvars.keys() - before_mvars.keys()),
        "metavariables_removed_from_inventory": sorted(before_mvars.keys() - after_mvars.keys()),
        "metavariables_assigned": assigned,
        "metavariables_changed": changed_ids(before_mvars, after_mvars),
        "external_premises_used": capture["external_constant_refs"],
        "local_context_refs_used": capture["local_context_refs"],
        "expression_changes": {
            "goal_targets_changed": sorted(
                key for key in shared_goals
                if digest(before_goals[key].get("target")) != digest(after_goals[key].get("target"))
            )
        },
    }


def constructor_counts(value: Any, counter: collections.Counter[str]) -> None:
    if isinstance(value, dict):
        constructor = value.get("constructor")
        if isinstance(constructor, str):
            counter[constructor] += 1
        for child in value.values():
            constructor_counts(child, counter)
    elif isinstance(value, list):
        for child in value:
            constructor_counts(child, counter)


def audit_capture(
    capture: dict[str, Any], selection: dict[str, Any], source_record: dict[str, Any],
    raw_file: Path,
) -> dict[str, Any]:
    before_exact = capture["pretty_before_diagnostic"] == source_record["lean"]["raw_state_before"]
    after_exact = capture["pretty_after_diagnostic"] == source_record["lean"]["raw_state_after"]
    location_exact = (
        capture["source_start"]["raw"] == selection["source_start_raw"]
        and capture["source_end"]["raw"] == selection["source_end_raw"]
    )
    identity_exact = (
        capture["record_id"] == selection["record_id"]
        and capture["theorem_id"] == selection["theorem_id"]
        and capture["transition_index"] == selection["transition_index"]
    )
    status = "EXACT_REPLAY_PASS" if all(
        (before_exact, after_exact, location_exact, identity_exact)
    ) else "EXACT_REPLAY_FAIL"
    counts: collections.Counter[str] = collections.Counter()
    constructor_counts(capture["state_before"], counts)
    constructor_counts(capture["state_after"], counts)
    official_external = source_record["v3_formal_source_enrichment"]["premise_full_names"]
    delta = canonical_structured_delta(
        capture["state_before"], capture["state_after"],
        official_external, capture["local_context_refs"],
        capture.get("metavariable_delta"),
    )
    local_by_id = local_map(capture["state_before"])
    resolved_refs = [
        {
            "fvar_id": fvar_id,
            "user_name": local_by_id.get(fvar_id, {}).get("user_name"),
            "resolved_in_before_goal_context": fvar_id in local_by_id,
        }
        for fvar_id in capture["local_context_refs"]
    ]
    return {
        "record_id": selection["record_id"],
        "source_file": selection["source_file"],
        "theorem_id": selection["theorem_id"],
        "transition_index": selection["transition_index"],
        "replay_status": status,
        "reconstruction_method": "FRESH_WHOLE_FILE_ELABORATION_EXACT_INFO_TREE_PATH",
        "before_exact_text_match": before_exact,
        "after_exact_text_match": after_exact,
        "source_location_exact": location_exact,
        "record_identity_exact": identity_exact,
        "action_identity": {
            "source_sha256": selection["action_sha256"],
            "mechanism": "EXACT_HISTORICAL_SOURCE_RANGE_EXECUTED_DURING_FRESH_ELABORATION",
        },
        "info_tree_path": capture["info_tree_path"],
        "fresh_trace_ordinal": capture["fresh_trace_ordinal"],
        "state_before_runtime_sha256": digest(capture["state_before"]),
        "state_after_runtime_sha256": digest(capture["state_after"]),
        "environment_fingerprint_sha256": digest(capture["environment"]),
        "expr_constructor_counts": dict(sorted(counts.items())),
        "local_context_refs": resolved_refs,
        "local_reference_mechanism": capture["reference_mechanism"],
        "local_reference_completeness": capture["reference_completeness"],
        "official_external_premise_refs": official_external,
        "elaborated_external_constant_refs": capture["external_constant_refs"],
        "structured_delta": delta,
        "raw_capture_file": str(raw_file),
        "raw_capture_file_sha256": hashlib.sha256(raw_file.read_bytes()).hexdigest(),
    }


def environment_identity(runtime_root: Path) -> dict[str, Any]:
    lean = run_checked(["lake", "env", "lean", "--version"], runtime_root, 30)
    git = run_checked(["git", "rev-parse", "HEAD"], runtime_root, 30)
    identity = {
        "lean_version_output": lean.stdout.strip(),
        "mathlib_commit": git.stdout.strip(),
        "platform_machine": platform.machine(),
        "platform_system": platform.system(),
        "expected_lean_version": LEAN_VERSION,
        "expected_lean_build_commit": LEAN_BUILD_COMMIT,
        "expected_mathlib_commit": MATHLIB_COMMIT,
    }
    identity["exact_pin_verified"] = (
        LEAN_VERSION.removeprefix("v") in identity["lean_version_output"]
        and LEAN_BUILD_COMMIT in identity["lean_version_output"]
        and identity["mathlib_commit"] == MATHLIB_COMMIT
    )
    identity["fingerprint_sha256"] = digest(identity)
    return identity


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--campaign-dir", type=Path, required=True)
    parser.add_argument("--runtime-root", type=Path, required=True)
    parser.add_argument("--extractor", type=Path, required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--timeout", type=int, default=600)
    args = parser.parse_args()
    args.extractor = args.extractor.resolve()
    args.runtime_root = args.runtime_root.resolve()

    environment = environment_identity(args.runtime_root)
    if not environment["exact_pin_verified"]:
        raise SystemExit(f"ENVIRONMENT_MISMATCH: {environment}")
    jobs = json.loads((args.campaign_dir / "jobs.json").read_text())
    selections = {
        row["record_id"]: row
        for row in map(json.loads, (args.campaign_dir / "selection.jsonl").open())
    }
    source_records = load_source_records(args.source)
    started = time.monotonic()
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        job_results = list(pool.map(
            lambda job: run_job(job, args.runtime_root, args.extractor, args.timeout), jobs
        ))
    write_json(args.campaign_dir / "job_results.json", job_results)

    audits: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    captured_ids: set[str] = set()
    for job in job_results:
        if job["process_status"] != "PROCESS_PASS":
            failures.append({
                "source_file": job["source_file"],
                "targets": job["targets"],
                "status": "ENVIRONMENT_MISMATCH" if "object file" in job["stderr"] else "UNSUPPORTED_PATH",
                "diagnostic": (job["stderr"] or job["error"] or "")[-4000:],
            })
            continue
        raw_file = Path(job["output_file"])
        payload = json.loads(raw_file.read_text())
        for capture in payload["captures"]:
            record_id = capture["record_id"]
            captured_ids.add(record_id)
            audits.append(audit_capture(
                capture, selections[record_id], source_records[record_id], raw_file
            ))
        if payload["captured_targets"] != payload["requested_targets"]:
            failures.append({
                "source_file": job["source_file"],
                "targets": job["targets"] - payload["captured_targets"],
                "status": "UNSUPPORTED_PATH",
                "diagnostic": (
                    f"captured {payload['captured_targets']} of {payload['requested_targets']} "
                    "exact source targets"
                ),
            })
    for record_id in selections.keys() - captured_ids:
        if not any(f["source_file"] == selections[record_id]["source_file"] for f in failures):
            failures.append({
                "source_file": selections[record_id]["source_file"],
                "record_id": record_id,
                "targets": 1,
                "status": "UNSUPPORTED_PATH",
                "diagnostic": "exact TacticInfo source location was not captured",
            })
    audits.sort(key=lambda row: row["record_id"])
    write_jsonl(args.campaign_dir / "audit_rows.jsonl", audits)
    exact_pass = sum(row["replay_status"] == "EXACT_REPLAY_PASS" for row in audits)
    exact_fail = len(audits) - exact_pass
    unsupported = sum(f["targets"] for f in failures if f["status"] == "UNSUPPORTED_PATH")
    environment_mismatch = sum(
        f["targets"] for f in failures if f["status"] == "ENVIRONMENT_MISMATCH"
    )
    constructor_totals: collections.Counter[str] = collections.Counter()
    for row in audits:
        constructor_totals.update(row["expr_constructor_counts"])
    summary = {
        "schema_version": "lean-runtime-replay-campaign-v2.0.0",
        "selected": len(selections),
        "replayable": len(audits),
        "exact_pass": exact_pass,
        "exact_fail": exact_fail,
        "unsupported": unsupported,
        "environment_mismatch": environment_mismatch,
        "primary_exact_pass_rate": exact_pass / len(selections),
        "conditional_exact_pass_rate": exact_pass / len(audits) if audits else 0.0,
        "elapsed_seconds": time.monotonic() - started,
        "workers": args.workers,
        "environment": environment,
        "process_status_counts": dict(sorted(collections.Counter(
            job["process_status"] for job in job_results
        ).items())),
        "failure_diagnostics": failures,
        "expr_constructor_totals": dict(sorted(constructor_totals.items())),
        "records_with_local_refs": sum(bool(row["local_context_refs"]) for row in audits),
        "audit_rows_sha256": digest(audits),
    }
    write_json(args.campaign_dir / "campaign_summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
