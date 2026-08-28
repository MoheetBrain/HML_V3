#!/usr/bin/env python3
"""Build the deterministic 1,000-transition LEAN_PIPELINE_V1 evidence corpus."""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import sys
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hml_v3.adapters.lean.adapter import adapt_lean_transition, lean_transition_from_record  # noqa: E402
from hml_v3.adapters.lean.parser import parse_lean_state  # noqa: E402
from hml_v3.canonical.models import stable_sha256  # noqa: E402


DEFAULT_SOURCE = Path(
    "/Users/moheet/Projects/Hamiltonian-Labs/hml_research_artifacts/"
    "lean_domino_v2/lean_canonical_records.jsonl"
)
DEFAULT_ATTESTATION = Path(
    "/Users/moheet/Documents/ChatGPT/hmlt-reasoning-corpus-lean-attestation/"
    "synthetic_factory/lean_attestation/data/stage100"
)
SOURCE_ARTIFACT_SHA256 = "8ac0ce010cedaecb1f9edf0d0ef7b0a5700620de52a66e508fd6e71778719869"
MATHLIB_COMMIT = "29dcec074de168ac2bf835a77ef68bbe069194c5"
BENCHMARK_ROOT = Path(
    "/Users/moheet/Projects/Hamiltonian-Labs/hml_research_artifacts/"
    "leandojo_raw/leandojo_benchmark_4"
)
SELECTION_SEED = "hml-v3-lean-pipeline-v1-balanced-effects"
EXTRA_ROWS = 900


def json_line(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_deterministic_gzip(path: Path, rows: Iterable[dict[str, Any]]) -> tuple[int, str]:
    path.parent.mkdir(parents=True, exist_ok=True)
    uncompressed = hashlib.sha256()
    count = 0
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
            for row in rows:
                encoded = json_line(row)
                compressed.write(encoded)
                uncompressed.update(encoded)
                count += 1
    return count, uncompressed.hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def parser_eligible(record: dict[str, Any]) -> bool:
    for phase, raw_key in (("state_before", "raw_state_before"), ("state_after", "raw_state_after")):
        parsed = parse_lean_state(record["lean"][raw_key])
        if not parsed.clean or len(parsed.goals) != int(record[phase]["n_goals"]):
            return False
    return True


def candidate_score(effect: str, example_id: str) -> str:
    return hashlib.sha256(f"{SELECTION_SEED}|{effect}|{example_id}".encode()).hexdigest()


def select_extra_ids(source_path: Path, excluded_theorems: set[str]) -> tuple[list[str], Counter[str]]:
    best_by_effect_theorem: dict[str, dict[str, tuple[str, str]]] = {}
    with source_path.open(encoding="utf-8") as handle:
        for line in handle:
            record = json.loads(line)
            if record["lean_official_split"] != "train" or record["theorem_id"] in excluded_theorems:
                continue
            if not parser_eligible(record):
                continue
            effect = record["observed_action"]["effect_class"]
            score = candidate_score(effect, record["example_id"])
            current = best_by_effect_theorem.setdefault(effect, {}).get(record["theorem_id"])
            if current is None or (score, record["example_id"]) < current:
                best_by_effect_theorem[effect][record["theorem_id"]] = (score, record["example_id"])

    effects = sorted(best_by_effect_theorem)
    if not effects:
        raise RuntimeError("no eligible effects found")
    base, remainder = divmod(EXTRA_ROWS, len(effects))
    quotas = {effect: base + (index < remainder) for index, effect in enumerate(effects)}
    used_theorems = set(excluded_theorems)
    selected: list[tuple[str, str, str]] = []
    for effect in effects:
        ordered = sorted(
            (score, example_id, theorem_id)
            for theorem_id, (score, example_id) in best_by_effect_theorem[effect].items()
        )
        for score, example_id, theorem_id in ordered:
            if theorem_id in used_theorems:
                continue
            selected.append((effect, score, example_id))
            used_theorems.add(theorem_id)
            if sum(1 for item in selected if item[0] == effect) == quotas[effect]:
                break
        actual = sum(1 for item in selected if item[0] == effect)
        if actual != quotas[effect]:
            raise RuntimeError(f"effect {effect} yielded {actual}, expected {quotas[effect]}")
    ordered_ids = [item[2] for item in sorted(selected)]
    return ordered_ids, Counter(item[0] for item in selected)


def source_records_by_id(source_path: Path, wanted: set[str]) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    with source_path.open(encoding="utf-8") as handle:
        for line in handle:
            record = json.loads(line)
            if record["example_id"] in wanted:
                records[record["example_id"]] = record
    missing = sorted(wanted - records.keys())
    if missing:
        raise RuntimeError(f"missing {len(missing)} selected source records; first={missing[0]}")
    return records


def theorem_declarations(
    wanted: set[tuple[str, str]],
) -> dict[tuple[str, str], dict[str, Any]]:
    wanted_paths = {path for path, _ in wanted}
    declarations: dict[tuple[str, str], dict[str, Any]] = {}
    with (BENCHMARK_ROOT / "corpus.jsonl").open(encoding="utf-8") as handle:
        for line in handle:
            file_record = json.loads(line)
            if file_record["path"] not in wanted_paths:
                continue
            for premise in file_record["premises"]:
                key = (file_record["path"], premise["full_name"])
                if key in wanted:
                    declarations[key] = premise
    missing = sorted(wanted - declarations.keys())
    if missing:
        raise RuntimeError(f"corpus has no theorem declaration for {len(missing)} rows; first={missing[0]}")
    return declarations


def enrich_formal_source(records: list[dict[str, Any]]) -> dict[str, int]:
    wanted = {(item["source_file"], item["theorem_id"]): item for item in records}
    declarations = theorem_declarations(set(wanted))
    matched: set[tuple[str, str]] = set()
    counters: Counter[str] = Counter()
    for split in ("train", "val", "test"):
        split_wanted = {
            key: item for key, item in wanted.items() if item["lean_official_split"] == split
        }
        if not split_wanted:
            continue
        with (BENCHMARK_ROOT / f"random/{split}.json").open(encoding="utf-8") as handle:
            theorem_rows = json.load(handle)
        for theorem in theorem_rows:
            key = (theorem["file_path"], theorem["full_name"])
            record = split_wanted.get(key)
            if record is None:
                continue
            index = int(record["transition_index"])
            if index >= len(theorem["traced_tactics"]):
                raise RuntimeError(f"transition index outside theorem trace: {record['example_id']}")
            trace = theorem["traced_tactics"][index]
            exact_matches = {
                "tactic": trace["tactic"] == record["lean"]["raw_tactic"],
                "state_before": trace["state_before"] == record["lean"]["raw_state_before"],
                "state_after": trace["state_after"] == record["lean"]["raw_state_after"],
            }
            if not all(exact_matches.values()):
                raise RuntimeError(f"LeanDojo source join mismatch: {record['example_id']} {exact_matches}")
            annotated_text, premise_records = trace["annotated_tactic"]
            premise_names = list(dict.fromkeys(item["full_name"] for item in premise_records))
            declaration = declarations[key]
            theorem_source = declaration["code"]
            record["v3_formal_source_enrichment"] = {
                "schema_version": "lean-v3-formal-source-enrichment-1.0.0",
                "benchmark_family": "LeanDojo Benchmark 4 random split",
                "benchmark_split": split,
                "source_repository": theorem["url"],
                "source_commit": theorem["commit"],
                "theorem_start": theorem["start"],
                "theorem_end": theorem["end"],
                "theorem_declaration_and_proof": theorem_source,
                "theorem_declaration_and_proof_sha256": stable_sha256(theorem_source),
                "theorem_kind": declaration["kind"],
                "corpus_source_start": declaration["start"],
                "corpus_source_end": declaration["end"],
                "annotated_tactic": annotated_text,
                "premises": premise_records,
                "premise_full_names": premise_names,
                "exact_source_join": exact_matches,
            }
            matched.add(key)
            counters["transitions_enriched"] += 1
            counters["transitions_with_premises"] += bool(premise_names)
            counters["premise_references"] += len(premise_names)
            counters["theorem_source_spans"] += 1
        del theorem_rows
    missing = sorted(wanted.keys() - matched)
    if missing:
        raise RuntimeError(f"formal source enrichment missed {len(missing)} theorem rows; first={missing[0]}")
    return dict(counters)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--attestation", type=Path, default=DEFAULT_ATTESTATION)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "data/samples")
    args = parser.parse_args()

    certificates = {
        item["source_record_id"]: item
        for item in load_jsonl(args.attestation / "certificates_run1.jsonl")
    }
    selection = sorted(
        load_jsonl(args.attestation / "selection.jsonl"), key=lambda item: item["selection_index"]
    )
    stage_ids = [item["source_record"]["example_id"] for item in selection]
    if len(stage_ids) != 100 or set(stage_ids) != certificates.keys():
        raise RuntimeError("Stage100 selection/certificate identity mismatch")
    excluded_theorems = {item["source_record"]["theorem_id"] for item in selection}
    extra_ids, extra_effect_counts = select_extra_ids(args.source, excluded_theorems)
    all_ids = stage_ids + extra_ids
    if len(all_ids) != 1000 or len(set(all_ids)) != 1000:
        raise RuntimeError("selection is not exactly 1,000 unique transitions")
    records = source_records_by_id(args.source, set(all_ids))
    ordered_records = [records[example_id] for example_id in all_ids]
    enrichment_counts = enrich_formal_source(ordered_records)

    canonical_rows: list[dict[str, Any]] = []
    for record in ordered_records:
        certificate = certificates.get(record["example_id"])
        source = lean_transition_from_record(record, certificate)
        if certificate and source.source_record_sha256 != certificate["source_record_sha256"]:
            raise RuntimeError(f"certificate source hash mismatch: {record['example_id']}")
        canonical_rows.append(adapt_lean_transition(source).to_dict())

    source_out = args.output_dir / "lean_pipeline_v1.source.jsonl.gz"
    canonical_out = args.output_dir / "lean_pipeline_v1.canonical.jsonl.gz"
    source_count, source_stream_sha = write_deterministic_gzip(source_out, ordered_records)
    canonical_count, canonical_stream_sha = write_deterministic_gzip(canonical_out, canonical_rows)

    split_counts = Counter(record["lean_official_split"] for record in ordered_records)
    effect_counts = Counter(record["observed_action"]["effect_class"] for record in ordered_records)
    replay_counts = Counter(cert["replay_status"] for cert in certificates.values())
    before_multigoal = sum(record["state_before"]["n_goals"] > 1 for record in ordered_records)
    after_multigoal = sum(record["state_after"]["n_goals"] > 1 for record in ordered_records)
    decomposition_failures = sum(
        not parse_lean_state(record["lean"][raw_key]).clean
        for record in ordered_records
        for raw_key in ("raw_state_before", "raw_state_after")
    )
    adapter_disagreements = sum(
        bool(state["source_specific"]["adapter_inconsistencies"])
        for row in canonical_rows
        for state in (row["state_before"], row["state_after"])
    )
    manifest = {
        "schema_version": "lean-pipeline-v1-manifest-1.0.0",
        "dataset_id": "lean_pipeline_v1",
        "created_at": "2026-08-27T00:00:00+01:00",
        "source": {
            "dataset_id": "lean_domino_v2_canonical_records",
            "artifact_sha256": SOURCE_ARTIFACT_SHA256,
            "mathlib_commit": MATHLIB_COMMIT,
            "lean_version": "v4.10.0-rc1",
            "leandojo_version": "2.0.0",
            "formal_trace_transitions_available": 241265,
        },
        "selection": {
            "policy": "All Stage100 attestation rows, then deterministic TRAIN-only, unique-theorem, parser-clean rows balanced over eight recorded effect classes.",
            "seed": SELECTION_SEED,
            "attestation_rows": 100,
            "additional_rows": EXTRA_ROWS,
            "additional_effect_counts": dict(sorted(extra_effect_counts.items())),
            "evaluation_protection": "Official split remains attached per row. The 100 attestation QA rows are never an unqualified training set.",
        },
        "counts": {
            "transitions": source_count,
            "canonical_transitions": canonical_count,
            "unique_transition_ids": len(set(all_ids)),
            "unique_theorem_ids": len({record["theorem_id"] for record in ordered_records}),
            "official_splits": dict(sorted(split_counts.items())),
            "effect_classes": dict(sorted(effect_counts.items())),
            "states": 2000,
            "states_before_with_multiple_goals": before_multigoal,
            "states_after_with_multiple_goals": after_multigoal,
            "raw_state_decomposition_failures": decomposition_failures,
            "source_structured_projection_disagreements": adapter_disagreements,
            **enrichment_counts,
            "formal_trace_accepted": 1000,
            "fresh_replay_pass": replay_counts.get("REPLAY_PASS", 0),
            "fresh_replay_nonpass": 100 - replay_counts.get("REPLAY_PASS", 0),
            "without_fresh_replay_certificate": 900,
        },
        "files": {
            "source": {
                "path": source_out.relative_to(ROOT).as_posix(),
                "rows": source_count,
                "sha256": file_sha256(source_out),
                "uncompressed_stream_sha256": source_stream_sha,
            },
            "canonical": {
                "path": canonical_out.relative_to(ROOT).as_posix(),
                "rows": canonical_count,
                "sha256": file_sha256(canonical_out),
                "uncompressed_stream_sha256": canonical_stream_sha,
            },
        },
        "verification_semantics": {
            "FORMAL_TRACE_ACCEPTED": "Transition is from the pinned LeanDojo formal trace; this is not a claim of fresh per-row replay.",
            "FRESH_REPLAY_PASS": "Pinned runtime reached the exact before-state, executed the exact action, and matched exact before/after states.",
            "nonpass_certificates": dict(sorted(replay_counts.items())),
        },
    }
    manifest_path = ROOT / "data/manifests/lean_pipeline_v1.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "status": "PASS",
                "rows": source_count,
                "fresh_replay_pass": replay_counts.get("REPLAY_PASS", 0),
                "source_sha256": manifest["files"]["source"]["sha256"],
                "canonical_sha256": manifest["files"]["canonical"]["sha256"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
