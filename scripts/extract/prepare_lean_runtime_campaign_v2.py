#!/usr/bin/env python3
"""Join V1 rows to exact LeanDojo source spans and prepare a V2 runtime campaign.

The join is evidence-based: the historical `.ast.json` must contain exactly the recorded
before/after states, and its source slice must reproduce the recorded tactic after the same
indentation normalization used by LeanDojo.  No goal or expression identity is inferred from
pretty text; text is used here only to recover the historical source location at which the
fresh Lean-side extractor must observe elaborator objects.
"""

from __future__ import annotations

import argparse
import collections
import gzip
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def text_sha(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def read_jsonl_gz(path: Path) -> list[dict[str, Any]]:
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle]


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n")


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(canonical_json(row) + "\n")


def fix_indentation(tactic: str, indent: int) -> str:
    lines = tactic.splitlines()
    if len(lines) == 1:
        return tactic
    fixed = [lines[0]]
    for line in lines[1:]:
        for index, char in enumerate(line):
            if char != " " or index >= indent:
                fixed.append(line[index:])
                break
        else:
            fixed.append("")
    return "\n".join(fixed)


def tactic_at(source: bytes, start: int, end: int) -> str:
    prefix = source[:start].rsplit(b"\n", 1)[-1]
    indent = len(prefix.decode("utf-8"))
    return fix_indentation(source[start:end].decode("utf-8"), indent).strip()


def line_start_raw(source: bytes, line: int) -> int:
    if line <= 1:
        return 0
    cursor = 0
    for _ in range(line - 1):
        cursor = source.index(b"\n", cursor) + 1
    return cursor


def trace_path(runtime_root: Path, source_file: str) -> Path:
    relative = Path(source_file)
    parts = relative.parts
    if len(parts) >= 4 and parts[:2] == (".lake", "packages"):
        package_root = runtime_root.joinpath(*parts[:3])
        package_relative = Path(*parts[3:]).with_suffix(".ast.json")
        return package_root / ".lake" / "build" / "ir" / package_relative
    return runtime_root / ".lake" / "build" / "ir" / relative.with_suffix(".ast.json")


def source_location_join(
    record: dict[str, Any], runtime_root: Path, trace_cache: dict[str, dict[str, Any]],
    source_cache: dict[str, bytes],
) -> dict[str, Any]:
    source_file = record["source_file"]
    if source_file not in trace_cache:
        trace_cache[source_file] = json.loads(trace_path(runtime_root, source_file).read_text())
        source_cache[source_file] = (runtime_root / source_file).read_bytes()
    trace = trace_cache[source_file]
    source = source_cache[source_file]
    lean = record["lean"]
    enrichment = record["v3_formal_source_enrichment"]
    theorem_start = line_start_raw(source, int(enrichment["theorem_start"][0]))
    theorem_end_line = int(enrichment["theorem_end"][0]) + 1
    theorem_end = (
        line_start_raw(source, theorem_end_line)
        if source.count(b"\n") + 1 >= theorem_end_line
        else len(source)
    )
    theorem_tactics: list[tuple[dict[str, Any], str]] = []
    signatures: set[tuple[str, str, str]] = set()
    for tactic in trace["tactics"]:
        if not (theorem_start <= tactic["pos"] < theorem_end):
            continue
        action = tactic_at(source, tactic["pos"], tactic["endPos"])
        if tactic["stateBefore"] == "no goals" or "·" in action:
            continue
        signature = (tactic["stateBefore"], action, tactic["stateAfter"])
        if signature in signatures:
            continue
        signatures.add(signature)
        theorem_tactics.append((tactic, action))
    index = int(record["transition_index"])
    indexed = theorem_tactics[index] if index < len(theorem_tactics) else None
    if indexed is not None and (
        indexed[0]["stateBefore"] == lean["raw_state_before"]
        and indexed[0]["stateAfter"] == lean["raw_state_after"]
        and indexed[1] == lean["raw_tactic"]
    ):
        tactic = indexed[0]
        return {
            "source_start_raw": tactic["pos"],
            "source_end_raw": tactic["endPos"],
            "historical_state_pair_exact": True,
            "historical_action_exact": True,
            "join_mechanism": "THEOREM_SCOPED_FILTERED_DEDUPLICATED_TRACE_INDEX",
        }
    candidates = [
        tactic for tactic in trace["tactics"]
        if tactic["stateBefore"] == lean["raw_state_before"]
        and tactic["stateAfter"] == lean["raw_state_after"]
    ]
    exact_action = [
        tactic for tactic in candidates
        if tactic_at(source, tactic["pos"], tactic["endPos"]) == lean["raw_tactic"]
    ]
    if not exact_action:
        raise RuntimeError(
            f"source location join for {record['example_id']} has "
            f"{len(candidates)} state candidates and {len(exact_action)} exact actions"
        )
    tactic = exact_action[0]
    return {
        "source_start_raw": tactic["pos"],
        "source_end_raw": tactic["endPos"],
        "historical_state_pair_exact": True,
        "historical_action_exact": True,
        "join_mechanism": (
            "UNIQUE_EXACT_SIGNATURE_FALLBACK" if len(exact_action) == 1
            else "FIRST_EXACT_SIGNATURE_FALLBACK_AFTER_INDEX_DIVERGENCE"
        ),
    }


def domain(record: dict[str, Any]) -> str:
    parts = Path(record["source_file"]).parts
    return parts[1] if len(parts) > 1 else parts[0]


def tactic_family(record: dict[str, Any]) -> str:
    tactic = record["lean"]["raw_tactic"].lstrip("· ").strip()
    return tactic.split(maxsplit=1)[0] if tactic else "EMPTY"


def depth_bin(depth: int) -> str:
    return "0-3" if depth <= 3 else "4-15" if depth <= 15 else "16-39" if depth <= 39 else "40+"


def goal_bin(count: int) -> str:
    return "0" if count == 0 else "1" if count == 1 else "2" if count == 2 else "3+"


def context_bin(count: int) -> str:
    return "0-5" if count <= 5 else "6-15" if count <= 15 else "16-30" if count <= 30 else "31+"


def compact_row(record: dict[str, Any], joined: dict[str, Any]) -> dict[str, Any]:
    return {
        "record_id": record["example_id"],
        "source_file": record["source_file"],
        "theorem_id": record["theorem_id"],
        "transition_index": record["transition_index"],
        "source_start_raw": joined["source_start_raw"],
        "source_end_raw": joined["source_end_raw"],
        "before_sha256": text_sha(record["lean"]["raw_state_before"]),
        "action_sha256": text_sha(record["lean"]["raw_tactic"]),
        "after_sha256": text_sha(record["lean"]["raw_state_after"]),
        "official_external_premise_refs": record["v3_formal_source_enrichment"]["premise_full_names"],
        "strata": {
            "domain": domain(record),
            "tactic_family": tactic_family(record),
            "proof_depth": depth_bin(int(record["proof_depth"])),
            "goal_count": goal_bin(int(record["state_before"]["n_goals"])),
            "local_context_size": context_bin(len(record["state_before"]["hypotheses"])),
            "state_change_type": record["observed_action"]["effect_class"],
            "official_split": record["lean_official_split"],
        },
        "join_evidence": joined,
    }


def select_files(rows: list[dict[str, Any]], runtime_root: Path, count: int) -> list[dict[str, Any]]:
    by_file: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for row in rows:
        by_file[row["source_file"]].append(row)
    selected: list[dict[str, Any]] = []
    remaining = dict(by_file)
    covered: dict[str, set[str]] = collections.defaultdict(set)
    while remaining and len(selected) < count:
        capacity = count - len(selected)

        def score(item: tuple[str, list[dict[str, Any]]]) -> tuple[Any, ...]:
            file_name, file_rows = item
            usable = file_rows[:capacity]
            novelty = sum(
                row["strata"][key] not in covered[key]
                for row in usable
                for key in row["strata"]
            )
            size = (runtime_root / file_name).stat().st_size
            tie = hashlib.sha256(file_name.encode()).hexdigest()
            return (len(usable), novelty, -size, tie)

        file_name, file_rows = max(remaining.items(), key=score)
        take = file_rows[:capacity]
        selected.extend(take)
        for row in take:
            for key, value in row["strata"].items():
                covered[key].add(value)
        del remaining[file_name]
    if len(selected) != count:
        raise RuntimeError(f"selected {len(selected)} rows, expected {count}")
    return sorted(selected, key=lambda row: row["record_id"])


def distribution(rows: list[dict[str, Any]], field: str) -> dict[str, int]:
    return dict(sorted(collections.Counter(row["strata"][field] for row in rows).items()))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--runtime-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--count", type=int, default=500)
    parser.add_argument(
        "--exclude-selection", type=Path, action="append", default=[],
        help="a prior campaign's selection.jsonl; its record_ids are removed before "
             "stratified selection, so a second campaign extends the corpus instead of "
             "re-elaborating transitions that are already captured",
    )
    args = parser.parse_args()

    excluded: set[str] = set()
    for path in args.exclude_selection:
        for line in path.open(encoding="utf-8"):
            if line.strip():
                excluded.add(json.loads(line)["record_id"])

    records = [
        record for record in read_jsonl_gz(args.source)
        if record["example_id"] not in excluded
    ]
    records_by_file: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for record in records:
        records_by_file[record["source_file"]].append(record)
    joined_rows: list[dict[str, Any]] = []
    unjoined: list[dict[str, str]] = []
    for file_records in records_by_file.values():
        trace_cache: dict[str, dict[str, Any]] = {}
        source_cache: dict[str, bytes] = {}
        for record in file_records:
            # A record that does not join to an exact source byte range is dropped and
            # counted, never approximated. Batch acquisition from a large trace will always
            # contain some records whose tactic text differs from the source spelling
            # (indentation, comments, elaborated sugar); aborting the whole campaign on the
            # first one would make targeted acquisition impossible.
            try:
                joined = source_location_join(
                    record, args.runtime_root, trace_cache, source_cache)
            except Exception as error:  # noqa: BLE001 - the outcome is recorded, not raised
                unjoined.append({
                    "record_id": record["example_id"],
                    "reason": f"{type(error).__name__}: {str(error)[:160]}",
                })
                continue
            joined_rows.append(compact_row(record, joined))
    if not joined_rows:
        raise SystemExit(
            f"no record joined to an exact source location ({len(unjoined)} failures)"
        )
    requested = args.count
    args.count = min(args.count, len(joined_rows))
    selected = select_files(joined_rows, args.runtime_root, args.count)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.output_dir / "selection.jsonl", selected)
    target_dir = args.output_dir / "targets"
    target_dir.mkdir(parents=True, exist_ok=True)
    selected_by_file: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for row in selected:
        selected_by_file[row["source_file"]].append(row)
    file_jobs = []
    for index, (source_file, file_rows) in enumerate(sorted(selected_by_file.items())):
        target_path = target_dir / f"{index:04d}.tsv"
        target_path.write_text(
            "".join(
                f"{row['theorem_id']}\t{row['transition_index']}\t{row['record_id']}\t"
                f"{row['source_start_raw']}\t{row['source_end_raw']}\n"
                for row in file_rows
            ),
            encoding="utf-8",
        )
        file_jobs.append({
            "source_file": source_file,
            "target_file": str(target_path.resolve()),
            "output_file": str((args.output_dir / "raw" / f"{index:04d}.json").resolve()),
            "targets": len(file_rows),
            "source_bytes": (args.runtime_root / source_file).stat().st_size,
        })
    write_json(args.output_dir / "jobs.json", file_jobs)
    manifest = {
        "schema_version": "lean-runtime-campaign-selection-v2.0.0",
        "population": len(joined_rows),
        "selected": len(selected),
        "files": len(file_jobs),
        "selection_sha256": digest(selected),
        "requested": requested,
        "joined_exactly": len(joined_rows),
        "unjoined": len(unjoined),
        "unjoined_examples": unjoined[:10],
        "all_historical_location_joins_exact": all(
            row["join_evidence"]["historical_state_pair_exact"]
            and row["join_evidence"]["historical_action_exact"]
            for row in selected
        ),
        "distributions": {
            key: distribution(selected, key)
            for key in (
                "domain", "tactic_family", "proof_depth", "goal_count",
                "local_context_size", "state_change_type", "official_split",
            )
        },
    }
    write_json(args.output_dir / "selection_manifest.json", manifest)
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
