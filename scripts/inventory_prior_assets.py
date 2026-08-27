#!/usr/bin/env python3
"""Inventory prior HML repositories and assets without mutating their sources."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
from typing import Any, Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO_ROOT / "data/registry/datasets.yaml"
DEFAULT_OUTPUT = REPO_ROOT / "data/registry/prior_assets.json"

REPOSITORIES = [
    Path("/Users/moheet/Documents/ChatGPT/hamiltonian-lang-final-signal"),
    Path("/Users/moheet/Documents/ChatGPT/hmlt-reasoning-corpus"),
    Path("/Users/moheet/Documents/ChatGPT/hmlt-reasoning-corpus/hml_core"),
    Path("/Users/moheet/Projects/Hamiltonian-Labs/hml-standard"),
    Path("/Users/moheet/Projects/Hamiltonian-Labs/hml-model-experiments"),
    Path("/Users/moheet/Documents/ChatGPT/prm800k"),
    Path("/Users/moheet/Projects/Hamiltonian-Labs/hml_research_artifacts/prm800k_raw"),
]

DATA_CENSUS_ROOTS = [
    Path("/Users/moheet/Documents/ChatGPT/hmlt-reasoning-corpus/data"),
    Path("/Users/moheet/Documents/ChatGPT/hmlt-reasoning-corpus/experiments"),
    Path("/Users/moheet/Projects/Hamiltonian-Labs/hml_research_artifacts"),
    Path("/Users/moheet/Projects/Hamiltonian-Labs/hml-model-experiments/data"),
    Path("/Users/moheet/Projects/Hamiltonian-Labs/hml-model-experiments/experiments"),
]

DATA_SUFFIXES = (".jsonl", ".jsonl.gz", ".parquet", ".csv", ".csv.gz", ".tar.gz")
SKIP_PARTS = {".git", ".venv", "__pycache__", ".pytest_cache"}

EXPERIMENT_ASSETS = [
    {
        "asset_id": "final_hml_signal",
        "name": "FINAL_HML_SIGNAL",
        "path": "/Users/moheet/Documents/ChatGPT/hamiltonian-lang-final-signal/experiments/final_hml_signal",
        "source": "hamiltonian-lang experiment history",
        "repository": "MoheetBrain/hamiltonian-lang",
        "branch_commit": "701f99ec137326a91e8d61faae686a3baf5f0120",
        "dataset_version": "FINAL_HML_SIGNAL",
        "license": "Internal research artifact",
        "trust": "HISTORICAL_EXPERIMENT",
        "usefulness": "Forensic record of a +35.55pp result later explained by arm-specific envelope confounding.",
        "duplicate_status": "Report also frozen in hml-reasoning-corpus; payload referenced once.",
        "ingestion_status": "HISTORICAL_ONLY",
        "result_status": "CONFOUNDED",
        "categories": ["experiments", "prior_hml"],
    },
    {
        "asset_id": "common_envelope_10k",
        "name": "COMMON_ENVELOPE_10K",
        "path": "/Users/moheet/Documents/ChatGPT/hamiltonian-lang-final-signal/experiments/common_envelope_10k",
        "source": "hamiltonian-lang experiment history",
        "repository": "MoheetBrain/hamiltonian-lang",
        "branch_commit": "273a5145fb4128daf37493de396126aa8cc84d97",
        "dataset_version": "common-envelope-10k-final-20260824",
        "license": "Internal research artifact",
        "trust": "CONTROLLED_EXPERIMENT",
        "usefulness": "Causal correction: common envelope reversed the apparent HML gain to -2.77pp.",
        "duplicate_status": "Unique frozen control; references shared upstream corpus.",
        "ingestion_status": "REFERENCE",
        "result_status": "NEGATIVE",
        "categories": ["experiments", "prior_hml"],
    },
    {
        "asset_id": "exp_rep_validity_stage1",
        "name": "EXP_REP_VALIDITY_V1 Stage 1",
        "path": "/Users/moheet/Documents/ChatGPT/hmlt-reasoning-corpus/experiments/max_ev_representation_v1",
        "source": "hml-reasoning-corpus experiment history",
        "repository": "MoheetBrain/hml-reasoning-corpus",
        "branch_commit": "bf2cd75a0676afdb73ab15fe5963cb6138e27060",
        "dataset_version": "DATASET_V1-1.0.0",
        "license": "Internal derived artifact; source licenses apply",
        "trust": "CONTROLLED_EXPERIMENT_WITH_LIMITATIONS",
        "usefulness": "Latest clean four-arm representation comparison and lexical-shortcut warning.",
        "duplicate_status": "Unique experiment; derived from prior Lean trace source.",
        "ingestion_status": "REFERENCE",
        "result_status": "NEGATIVE_OR_UNCERTAIN",
        "categories": ["experiments", "prior_hml"],
    },
    {
        "asset_id": "hml_model_experiments",
        "name": "Prior HML model experiment history",
        "path": "/Users/moheet/Projects/Hamiltonian-Labs/hml-model-experiments",
        "source": "local Git repository",
        "repository": "local/hml-model-experiments",
        "branch_commit": "26d1140",
        "dataset_version": None,
        "license": "No repository license found",
        "trust": "HISTORICAL_EXPERIMENT_COLLECTION",
        "usefulness": "Syntax acquisition, B1/B2, VNext, reverse-projection, and causal-autopsy evidence.",
        "duplicate_status": "Contains experiment-specific records; some source datasets overlap corpus assets.",
        "ingestion_status": "REFERENCE",
        "result_status": "MIXED_NEGATIVE_INVALIDATED",
        "categories": ["experiments", "prior_hml"],
    },
    {
        "asset_id": "minilang_audit",
        "name": "MiniLang OOPSLA26 v2 audit",
        "path": "/Users/moheet/Documents/ChatGPT/hmlt-reasoning-corpus/experiments/minilang_audit",
        "source": "prior corpus audit",
        "repository": "MoheetBrain/hml-reasoning-corpus",
        "branch_commit": "9d67e54450b9db897ee2ed20ec2e4cbbc16a3780",
        "dataset_version": "OOPSLA26-v2 artifact",
        "license": "See ARTIFACT_LICENSE_NOTICE.txt",
        "trust": "EXTERNAL_FORMAL_LANGUAGE_ARTIFACT_AUDIT",
        "usefulness": "Operation semantics, translation failures, and lessons for representation-neutral design.",
        "duplicate_status": "Source tree compressed once; reports reference it.",
        "ingestion_status": "REFERENCE",
        "result_status": "AUDIT",
        "categories": ["experiments", "external_sources"],
    },
    {
        "asset_id": "lean_runtime_attestation",
        "name": "Lean Runtime Evidence Attestation V1",
        "path": "/Users/moheet/Documents/ChatGPT/hmlt-reasoning-corpus-lean-attestation/synthetic_factory/lean_attestation",
        "source": "hml-reasoning-corpus worktree",
        "repository": "MoheetBrain/hml-reasoning-corpus",
        "branch_commit": "b4e2d9856c584ec53727b501bc0372bf3f867a65",
        "dataset_version": "lean-attestation-certificate-1.0.0",
        "license": "Internal derived artifact; source licenses apply",
        "trust": "RUNTIME_REPLAY_EVIDENCE",
        "usefulness": "Fresh verifier certificates and exact limits of flattened LeanDojo traces.",
        "duplicate_status": "Two deterministic runs intentionally duplicate semantic content.",
        "ingestion_status": "REFERENCE",
        "result_status": "PARTIAL_PASS_GATE_FAIL",
        "categories": ["experiments", "proof_data"],
    },
    {
        "asset_id": "hml_eval_001",
        "name": "HML-EVAL-001",
        "path": "/Users/moheet/Documents/ChatGPT/hamiltonian-lang-final-signal/benchmarks/eval001",
        "source": "hamiltonian-lang all-ref history",
        "repository": "MoheetBrain/hamiltonian-lang",
        "branch_commit": "71b0ee69dbea27d5a0c8fe59682a96e2370bee74",
        "dataset_version": "hml-v0 evaluation baseline",
        "license": "Apache-2.0 repository",
        "trust": "HISTORICAL_EVALUATION",
        "usefulness": "Earliest frozen paired HML evaluation and protocol lessons.",
        "duplicate_status": "Historical benchmark retained in Git history.",
        "ingestion_status": "HISTORICAL_ONLY",
        "result_status": "NEGATIVE_NULL_REDESIGN",
        "categories": ["experiments", "prior_hml"],
    },
    {
        "asset_id": "representation_arena_b1_b2",
        "name": "Representation Arena B1/B2 and Endpoint A",
        "path": "/Users/moheet/Documents/ChatGPT/hamiltonian-lang-final-signal/evaluation/arena",
        "source": "hamiltonian-lang all-ref history",
        "repository": "MoheetBrain/hamiltonian-lang",
        "branch_commit": "22b4bb79e589dcd5e9b52d92d6d20c94ee2e0b7c",
        "dataset_version": "arena B1/B2 frozen results",
        "license": "Apache-2.0 repository",
        "trust": "CONTROLLED_SMALL_N_EXPERIMENT",
        "usefulness": "Implication, next-action replication, binder, quantifier-scope, and generic S-expression evidence.",
        "duplicate_status": "Individual result JSON/JSONL files share the same arena worlds and model calibration.",
        "ingestion_status": "REFERENCE",
        "result_status": "MIXED_NEGATIVE; B2_GENERIC_SEXPR_WON",
        "categories": ["experiments", "prior_hml"],
    },
    {
        "asset_id": "domino_v1",
        "name": "DOMINO_V1",
        "path": "/Users/moheet/Projects/Hamiltonian-Labs/hml-model-experiments/experiments/domino_v1",
        "source": "local hml-model-experiments Git history",
        "repository": "local/hml-model-experiments",
        "branch_commit": "b6270795be4e5c33eb5f8dea2efb059385ed7ccc",
        "dataset_version": "DEV_PILOT",
        "license": "No repository license found",
        "trust": "HISTORICAL_LEARNING_EXPERIMENT",
        "usefulness": "Next-action candidate semantics and an example of a benchmark that was not diagnostic.",
        "duplicate_status": "Derived from Gold-125; candidate data is unique.",
        "ingestion_status": "HISTORICAL_ONLY",
        "result_status": "NOT_DIAGNOSTIC",
        "categories": ["experiments", "prior_hml"],
    },
    {
        "asset_id": "domino_v2",
        "name": "DOMINO_V2 / Gate-B repair ladder",
        "path": "/Users/moheet/Projects/Hamiltonian-Labs/hml-model-experiments/experiments/domino_v2",
        "source": "local hml-model-experiments Git history",
        "repository": "local/hml-model-experiments",
        "branch_commit": "25d02533b7778375f01d71d4b72de4d0f7789f12",
        "dataset_version": "Gate-B repair ladder",
        "license": "No repository license found",
        "trust": "HISTORICAL_LEARNING_EXPERIMENT",
        "usefulness": "Failure evidence for target learnability, leakage, loss/pooling, and capacity hypotheses.",
        "duplicate_status": "Shares source semantics with Lean DOMINO and the paired signal corpus.",
        "ingestion_status": "HISTORICAL_ONLY",
        "result_status": "NEGATIVE_STILL_COLLAPSED",
        "categories": ["experiments", "prior_hml"],
    },
    {
        "asset_id": "pretrained_hml_signal",
        "name": "Pretrained HML signal experiments",
        "path": "/Users/moheet/Projects/Hamiltonian-Labs/hml-model-experiments/experiments/pretrained_hml_signal",
        "source": "local hml-model-experiments Git history",
        "repository": "local/hml-model-experiments",
        "branch_commit": "bfc9626a95f2241508350c9dc8b05df3709dde77",
        "dataset_version": "paired 241,265-record HML/AST study",
        "license": "No repository license found; source licenses apply",
        "trust": "HISTORICAL_REPRESENTATION_EXPERIMENT",
        "usefulness": "Zero-shot, direct-head, adapter, depth, token, and full-DEV evidence.",
        "duplicate_status": "Rendered views duplicate the Lean canonical semantic source.",
        "ingestion_status": "REFERENCE",
        "result_status": "HML_AST_EQUIVALENT_SO_FAR",
        "categories": ["experiments", "prior_hml"],
    },
    {
        "asset_id": "hml_phase2_vnext",
        "name": "HML Phase II / VNext execution and causal autopsy",
        "path": "/Users/moheet/Projects/Hamiltonian-Labs/hml-model-experiments/experiments/hml_phase2",
        "source": "local hml-model-experiments Git history",
        "repository": "local/hml-model-experiments",
        "branch_commit": "26d114001f5900c0325e8aa576d9adeb868b6f52",
        "dataset_version": "Phase II final causal autopsy",
        "license": "No repository license found; source licenses apply",
        "trust": "HISTORICAL_REPRESENTATION_EXPERIMENT_COLLECTION",
        "usefulness": "Syntax acquisition, verdict/applicability, state delta, execution LoRA, four-arm VNext, reverse projection, and causal-mechanism evidence.",
        "duplicate_status": "Many payloads are projections of VNext-10K or synthetic-math pools; manifests distinguish them.",
        "ingestion_status": "REFERENCE",
        "result_status": "MIXED_NEGATIVE; HML_INPUT_HURTS; NO_COHERENT_V2_MECHANISM",
        "categories": ["experiments", "prior_hml"],
    },
    {
        "asset_id": "reasoning_layer_v1",
        "name": "Reasoning-layer discovery and confirmatory experiment",
        "path": "/Users/moheet/Documents/ChatGPT/hmlt-reasoning-corpus/experiments/reasoning_layer_v1_confirmatory",
        "source": "hml-reasoning-corpus Git history",
        "repository": "MoheetBrain/hml-reasoning-corpus",
        "branch_commit": "cc2312543290f32ef8c8acd0c52d067ab8cdebce",
        "dataset_version": "FINAL_A",
        "license": "Internal derived artifact; source licenses apply",
        "trust": "CONFIRMATORY_EXPERIMENT",
        "usefulness": "Evidence about where one-step state/action signal lives after the common-envelope correction.",
        "duplicate_status": "Uses frozen upstream formal-trace source with a dedicated holdout.",
        "ingestion_status": "REFERENCE",
        "result_status": "VALID_HISTORICAL_RESULT",
        "categories": ["experiments", "prior_hml"],
    },
    {
        "asset_id": "closed_loop_solver_pilot",
        "name": "HML closed-loop theorem pilot",
        "path": "/Users/moheet/Documents/ChatGPT/hmlt-reasoning-corpus/experiments/hml_closed_loop_pilot",
        "source": "hml-reasoning-corpus Git history",
        "repository": "MoheetBrain/hml-reasoning-corpus",
        "branch_commit": "3a1f3d15be67b349d1ffce5069bc4594d65b399e",
        "dataset_version": "closed-loop pilot",
        "license": "Internal derived artifact; source licenses apply",
        "trust": "LEAN_VERIFIER_IN_LOOP_PILOT",
        "usefulness": "Long-horizon calibration evidence and failure taxonomy.",
        "duplicate_status": "Pilot theorem set is separately manifested.",
        "ingestion_status": "REFERENCE",
        "result_status": "NEGATIVE_ZERO_SOLVED_ALL_ARMS",
        "categories": ["experiments", "proof_data", "prior_hml"],
    },
    {
        "asset_id": "lossless_hml_solver",
        "name": "Lossless HML solver calibration",
        "path": "/Users/moheet/Documents/ChatGPT/hmlt-reasoning-corpus/experiments/lossless_hml_final",
        "source": "hml-reasoning-corpus Git history",
        "repository": "MoheetBrain/hml-reasoning-corpus",
        "branch_commit": "d6f03ea8b99236f5e1b727c36c74e2717a8faeba",
        "dataset_version": "lossless_hml_final",
        "license": "Internal derived artifact; source licenses apply",
        "trust": "LEAN_VERIFIER_IN_LOOP_CALIBRATION",
        "usefulness": "Hard stop evidence: RAW solved 2/48, below the preregistered floor, so HML training/evaluation did not run.",
        "duplicate_status": "Separate from the earlier closed-loop pilot.",
        "ingestion_status": "REFERENCE",
        "result_status": "SOLVER_NOT_CALIBRATED",
        "categories": ["experiments", "proof_data", "prior_hml"],
    },
]


def run_git(path: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(path), *args],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    return proc.stdout.strip()


def byte_size(path: Path) -> int | None:
    if not path.exists():
        return None
    if path.is_file():
        return path.stat().st_size
    proc = subprocess.run(
        ["du", "-sk", str(path)], check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
    )
    if proc.returncode != 0 or not proc.stdout:
        return None
    return int(proc.stdout.split()[0]) * 1024


def sha256_file(path: Path, maximum: int = 1_100_000_000) -> str | None:
    if not path.is_file() or path.stat().st_size > maximum:
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def format_for(path: Path) -> str:
    if path.is_dir():
        return "directory"
    suffixes = "".join(path.suffixes).lower()
    return suffixes.lstrip(".") or "file"


def lines(value: str) -> list[str]:
    return [line for line in value.splitlines() if line]


def repository_record(path: Path) -> dict[str, Any]:
    head = run_git(path, "rev-parse", "HEAD")
    branch = run_git(path, "branch", "--show-current") or "DETACHED"
    status = lines(run_git(path, "status", "--porcelain=v1"))
    remotes = lines(run_git(path, "remote", "-v"))
    historical_paths = sorted(set(lines(run_git(path, "log", "--all", "--name-only", "--pretty=format:"))))
    return {
        "name": path.name,
        "location": str(path),
        "repository": remotes[0].split()[1] if remotes else "LOCAL_NO_REMOTE",
        "branch": branch,
        "commit": head,
        "branches": lines(run_git(path, "for-each-ref", "--format=%(refname:short)", "refs/heads", "refs/remotes")),
        "tags": lines(run_git(path, "tag", "--list")),
        "worktrees": lines(run_git(path, "worktree", "list", "--porcelain")),
        "all_history": lines(run_git(path, "log", "--all", "--oneline", "--decorate")),
        "historical_manifest_paths": [
            item for item in historical_paths if "manifest" in item.lower() or item.lower().endswith("protocol.yaml")
        ],
        "historical_experiment_paths": [
            item for item in historical_paths if item.startswith(("experiments/", "evaluation/", "benchmarks/"))
        ],
        "dirty": bool(status),
        "status_entries": status,
        "byte_size": byte_size(path),
        "semantic_trust_level": "SOURCE_HISTORY",
        "ingestion_status": "REFERENCE",
    }


def dataset_file_census() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    seen: set[Path] = set()
    for root in DATA_CENSUS_ROOTS:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file() or any(part in SKIP_PARTS for part in path.parts):
                continue
            lower = path.name.lower()
            if not (lower.endswith(DATA_SUFFIXES) or "manifest" in lower):
                continue
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            records.append(
                {
                    "path": str(resolved),
                    "byte_size": path.stat().st_size,
                    "format": format_for(path),
                    "sha256": sha256_file(path, maximum=32_000_000),
                    "hash_status": "COMPUTED" if path.stat().st_size <= 32_000_000 else "OMITTED_OVER_32MB",
                }
            )
    return sorted(records, key=lambda record: record["path"])


def load_registry() -> dict[str, Any]:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def dataset_asset(record: dict[str, Any]) -> dict[str, Any]:
    path = Path(record["local_path"])
    return {
        "asset_id": record["dataset_id"],
        "name": record["name"],
        "source": record["source_url"],
        "location": str(path),
        "repository": record["source_url"],
        "branch_commit": record["source_commit"],
        "dataset_version": record["source_version"],
        "rows_items": record["rows"],
        "format": format_for(path),
        "byte_size": byte_size(path),
        "sha256": record["sha256"] or sha256_file(path),
        "license": record["license"],
        "semantic_trust_level": f"TIER_{record['trust_tier']}:{record['verification_status']}",
        "usefulness_for_hml_v3": record["notes"],
        "duplicate_status": record["contamination_notes"],
        "ingestion_status": "REFERENCE" if path.exists() else "REACQUIRE",
        "exists": path.exists(),
        "result_status": record["verification_status"],
        "categories": ["datasets"] + (["proof_data"] if record["formal_system"] else []),
    }


def extra_asset(record: dict[str, Any]) -> dict[str, Any]:
    path = Path(record["path"])
    return {
        "asset_id": record["asset_id"],
        "name": record["name"],
        "source": record["source"],
        "location": str(path),
        "repository": record["repository"],
        "branch_commit": record["branch_commit"],
        "dataset_version": record["dataset_version"],
        "rows_items": None,
        "format": format_for(path),
        "byte_size": byte_size(path),
        "sha256": sha256_file(path),
        "license": record["license"],
        "semantic_trust_level": record["trust"],
        "usefulness_for_hml_v3": record["usefulness"],
        "duplicate_status": record["duplicate_status"],
        "ingestion_status": record["ingestion_status"] if path.exists() else "REACQUIRE",
        "exists": path.exists(),
        "result_status": record["result_status"],
        "categories": record["categories"],
    }


def markdown_table(rows: Iterable[dict[str, Any]], columns: list[tuple[str, str]]) -> str:
    header = "| " + " | ".join(label for label, _ in columns) + " |"
    divider = "|" + "|".join("---" for _ in columns) + "|"
    body = []
    for row in rows:
        values = []
        for _, key in columns:
            value = row.get(key)
            if isinstance(value, list):
                value = ", ".join(str(item) for item in value)
            values.append(str(value if value is not None else "UNKNOWN").replace("|", "\\|"))
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, divider, *body])


def write_reports(payload: dict[str, Any]) -> None:
    report_dir = REPO_ROOT / "research/asset_inventory"
    report_dir.mkdir(parents=True, exist_ok=True)
    repos = payload["repositories"]
    assets = payload["assets"]
    repo_table = markdown_table(
        repos,
        [("Repository", "name"), ("Location", "location"), ("Branch", "branch"), ("Commit", "commit"), ("Dirty", "dirty")],
    )
    (report_dir / "ALL_REPOSITORIES.md").write_text(
        "# All repositories\n\nGenerated read-only inventory. Branches, tags, worktrees, complete all-ref commit history, and historical manifest/experiment paths are preserved in `data/registry/prior_assets.json`.\n\n"
        + repo_table
        + "\n",
        encoding="utf-8",
    )

    def report(filename: str, title: str, category: str) -> None:
        selected = [a for a in assets if category in a["categories"]]
        table = markdown_table(
            selected,
            [
                ("Asset", "name"), ("Location", "location"), ("Rows/items", "rows_items"),
                ("Bytes", "byte_size"), ("Trust/status", "semantic_trust_level"),
                ("Decision", "ingestion_status"),
            ],
        )
        (report_dir / filename).write_text(
            f"# {title}\n\nGenerated from the canonical registry and read-only filesystem inspection. Missing values remain `UNKNOWN`; they are not guessed.\n\n{table}\n",
            encoding="utf-8",
        )

    report("ALL_DATASETS.md", "All datasets", "datasets")
    report("ALL_PROOF_DATA.md", "All proof data", "proof_data")
    report("ALL_EXPERIMENTS.md", "All experiments", "experiments")
    report("ALL_PRIOR_HML_ARTIFACTS.md", "All prior HML artifacts", "prior_hml")
    report("ALL_EXTERNAL_SOURCES.md", "All external sources", "external_sources")

    decisions = sorted(assets, key=lambda row: row["asset_id"])
    decision_table = markdown_table(
        decisions,
        [("Asset", "asset_id"), ("Decision", "ingestion_status"), ("Status", "result_status"), ("Use in V3", "usefulness_for_hml_v3")],
    )
    (report_dir / "PRIOR_ASSET_DECISIONS.md").write_text(
        "# Prior asset decisions\n\n`REFERENCE` means use in place without copying; `REACQUIRE` means no local artifact was found; `HISTORICAL_ONLY` excludes an asset from new truth/training while preserving it for audit.\n\n"
        + decision_table
        + "\n",
        encoding="utf-8",
    )


def build_inventory(output: Path) -> dict[str, Any]:
    registry = load_registry()
    repositories = [repository_record(path) for path in REPOSITORIES if run_git(path, "rev-parse", "--git-dir")]
    assets = [dataset_asset(record) for record in registry["datasets"]]
    assets.extend(extra_asset(record) for record in EXPERIMENT_ASSETS)
    data_files = dataset_file_census()
    payload = {
        "schema_version": "hml-v3-prior-asset-inventory-1.0.0",
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "generator": str(Path(__file__).resolve()),
        "repositories": repositories,
        "assets": assets,
        "dataset_file_census": data_files,
        "summary": {
            "repositories": len(repositories),
            "assets": len(assets),
            "datasets": sum("datasets" in asset["categories"] for asset in assets),
            "proof_data": sum("proof_data" in asset["categories"] for asset in assets),
            "experiments": sum("experiments" in asset["categories"] for asset in assets),
            "missing_local_assets": sum(not asset["exists"] for asset in assets),
            "dataset_like_files": len(data_files),
        },
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_reports(payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    payload = build_inventory(args.output)
    print(json.dumps(payload["summary"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
