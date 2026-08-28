#!/usr/bin/env python3
"""Stream a raw Lean runtime V2 campaign into a committed canonical corpus.

The V2 campaign writes one raw JSON document per Mathlib source file. Four of those
documents exceed 6 GiB because Lean's accumulated metavariable inventory is quadratic in
some proofs, and at least one was truncated when the driver died. ``json.load`` therefore
cannot be used: this reader walks the top-level ``captures`` array element by element and
records every per-file outcome instead of aborting the whole audit on the first defect.

Outputs
-------
* ``data/corpus/lean_runtime_v2.canonical.jsonl.gz`` — canonical transitions, one per line.
* ``reports/audits/LEAN_RUNTIME_V2_CORPUS.json`` — machine audit with exact denominators.
* ``reports/audits/LEAN_RUNTIME_V2_CORPUS.md`` — the same audit as prose.

No capture is repaired, re-elaborated, or inferred. A capture that cannot be parsed,
validated, canonicalized, or kept within the declared size budget is *excluded and counted*,
never silently dropped.
"""

from __future__ import annotations

import argparse
import collections
import gzip
import json
from pathlib import Path
import re
import sys
from typing import Any, Iterator

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hml_v3.adapters.lean.runtime_v2 import (  # noqa: E402
    canonicalize_capture,
    digest,
    validate_runtime_payload,
)
from hml_v3.canonical.delta_v2 import structured_delta  # noqa: E402
from hml_v3.representation_search.corpus import write_corpus  # noqa: E402

READ_CHUNK = 8 * 1024 * 1024


class TruncatedCapture(Exception):
    """The raw document ended inside the captures array."""


def _prefix_header(path: Path) -> tuple[dict[str, Any], int]:
    """Parse the object fields written before ``"captures"`` and return the array offset."""

    with path.open("rb") as handle:
        head = handle.read(READ_CHUNK)
    marker = head.find(b'"captures"')
    if marker < 0:
        raise TruncatedCapture("no captures key in first chunk")
    open_bracket = head.index(b"[", marker)
    prefix = head[:marker].rstrip()
    if prefix.endswith(b","):
        prefix = prefix[:-1]
    header = json.loads(prefix + b"}")
    return header, open_bracket + 1


STRUCTURAL = re.compile(rb'[\\"{}\]]')


def iter_captures(path: Path, max_element_bytes: int = 0):
    """Yield each top-level element of the ``captures`` array.

    The scan is byte-exact — it tracks JSON string and escape state, so braces inside Lean
    identifiers or pretty-printed diagnostics cannot desynchronise the depth counter — but
    it jumps between structural bytes with ``re.finditer`` instead of iterating every byte
    in Python. The campaign's four largest raw documents are 6.8-24 GiB and a per-byte loop
    over them costs hours.

    A capture larger than ``max_element_bytes`` is not decoded: its byte length is yielded
    as an ``int`` so the caller can count it without materialising a huge object.
    """

    _, offset = _prefix_header(path)
    depth = 0
    in_string = False
    started = False
    oversize = False
    chunks: list[bytes] = []
    held = 0
    escaped_position = -1
    base = offset
    cursor = 0
    with path.open("rb") as handle:
        handle.seek(offset)
        while True:
            data = handle.read(READ_CHUNK)
            if not data:
                break
            cursor = 0
            for match in STRUCTURAL.finditer(data):
                index = match.start()
                if base + index == escaped_position:
                    continue
                byte = data[index]
                if byte == 0x5C:  # backslash
                    if in_string:
                        escaped_position = base + index + 1
                    continue
                if in_string:
                    if byte == 0x22:
                        in_string = False
                    continue
                if byte == 0x22:
                    in_string = True
                    continue
                if byte == 0x5D:  # ] closing the captures array
                    if depth == 0:
                        return
                    continue
                if byte == 0x7B:  # {
                    if depth == 0:
                        started = True
                        cursor = index
                        chunks = []
                        held = 0
                        oversize = False
                    depth += 1
                    continue
                depth -= 1  # }
                if depth == 0 and started:
                    piece = data[cursor:index + 1]
                    if oversize:
                        yield held + len(piece)
                    else:
                        chunks.append(piece)
                        yield json.loads(b"".join(chunks))
                    chunks = []
                    held = 0
                    started = False
                    cursor = index + 1
            if started:
                piece = data[cursor:]
                held += len(piece)
                if oversize or (max_element_bytes and held > max_element_bytes):
                    oversize = True
                    chunks = []
                else:
                    chunks.append(piece)
            base += len(data)
    if started or depth != 0:
        raise TruncatedCapture("document ended inside a capture element")


def canonical_bytes(value: Any) -> int:
    return len(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode())


def validate_single_capture(capture: dict[str, Any]) -> None:
    validate_runtime_payload({
        "schema_version": "lean-runtime-state-v2.0.0",
        "captured_targets": 1,
        "captures": [capture],
    })


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--campaign-dir", type=Path, required=True, action="append",
                        help="repeatable; several campaigns merge into one corpus")
    parser.add_argument("--source", type=Path, default=ROOT / "data/samples/lean_pipeline_v1.source.jsonl.gz")
    parser.add_argument("--corpus", type=Path, default=ROOT / "data/corpus/lean_runtime_v2.canonical.jsonl.gz")
    parser.add_argument("--audit-json", type=Path, default=ROOT / "reports/audits/LEAN_RUNTIME_V2_CORPUS.json")
    parser.add_argument("--audit-md", type=Path, default=ROOT / "reports/audits/LEAN_RUNTIME_V2_CORPUS.md")
    parser.add_argument(
        "--skip-files-larger-than", type=int, default=0,
        help="raw documents above this size are excluded and counted without being read. "
             "Four of the campaign's documents are 6.8-24 GiB because Lean's accumulated "
             "metavariable inventory is quadratic in some proofs, and each holds a single "
             "capture that the canonical size budget excludes anyway. Zero means read all.",
    )
    parser.add_argument(
        "--max-element-bytes", type=int, default=8 * 1024 * 1024,
        help="raw capture elements larger than this are counted without being decoded",
    )
    parser.add_argument(
        "--max-canonical-bytes", type=int, default=262144,
        help="declared per-transition canonical size budget; larger transitions are excluded and counted",
    )
    args = parser.parse_args()

    with gzip.open(args.source, "rt", encoding="utf-8") as handle:
        source_records = {row["example_id"]: row for row in map(json.loads, handle)}
    selections: dict[str, dict[str, Any]] = {}
    job_results: list[dict[str, Any]] = []
    jobs_by_output: dict[str, dict[str, Any]] = {}
    for campaign in args.campaign_dir:
        for row in map(json.loads, (campaign / "selection.jsonl").open(encoding="utf-8")):
            selections[row["record_id"]] = row
        campaign_jobs = json.loads((campaign / "job_results.json").read_text())
        job_results.extend(campaign_jobs)
        for job in campaign_jobs:
            jobs_by_output[f"{campaign.name}/{Path(job['output_file']).name}"] = job

    file_outcomes: list[dict[str, Any]] = []
    size_histogram: collections.Counter[str] = collections.Counter()
    kept: list[dict[str, Any]] = []
    counters: collections.Counter[str] = collections.Counter()
    domains: collections.Counter[str] = collections.Counter()
    tactic_families: collections.Counter[str] = collections.Counter()
    seen_record_ids: set[str] = set()

    raw_files = [
        path for campaign in args.campaign_dir
        for path in sorted((campaign / "raw").glob("*.json"))
    ]
    for position, raw_path in enumerate(raw_files, start=1):
        print(
            f"[{position}/{len(raw_files)}] {raw_path.parent.parent.name}/{raw_path.name} "
            f"{raw_path.stat().st_size / 1e6:.1f} MB kept={counters['captures_kept']}",
            flush=True,
        )
        job = jobs_by_output.get(f"{raw_path.parent.parent.name}/{raw_path.name}", {})
        outcome = {
            "raw_file": f"{raw_path.parent.parent.name}/{raw_path.name}",
            "source_file": job.get("source_file"),
            "bytes": raw_path.stat().st_size,
            "captures_read": 0,
            "captures_kept": 0,
            "status": "OK",
            "detail": None,
        }
        if args.skip_files_larger_than and outcome["bytes"] > args.skip_files_larger_than:
            outcome["status"] = "SKIPPED_OVER_FILE_SIZE_LIMIT"
            outcome["detail"] = f"{outcome['bytes']} bytes exceeds the declared file limit"
            counters["files_skipped_over_size_limit"] += 1
            file_outcomes.append(outcome)
            continue
        try:
            header, _ = _prefix_header(raw_path)
            direct_imports = header.get("direct_imports", [])
            source_file = header.get("source_file")
        except Exception as error:  # noqa: BLE001 - the outcome is recorded, not raised
            outcome["status"] = "HEADER_UNREADABLE"
            outcome["detail"] = f"{type(error).__name__}: {error}"
            file_outcomes.append(outcome)
            counters["files_header_unreadable"] += 1
            continue

        try:
            for capture in iter_captures(raw_path, args.max_element_bytes):
                outcome["captures_read"] += 1
                counters["captures_read"] += 1
                if isinstance(capture, int):
                    counters["captures_over_element_budget"] += 1
                    size_histogram[">1MiB"] += 1
                    outcome["detail"] = outcome["detail"] or (
                        f"one or more captures exceed the {args.max_element_bytes}-byte raw element budget"
                    )
                    continue
                record_id = capture.get("record_id")
                if record_id in seen_record_ids:
                    counters["captures_duplicate_record_id"] += 1
                    continue
                selection = selections.get(record_id)
                if selection is None:
                    counters["captures_unselected"] += 1
                    continue
                try:
                    validate_single_capture(capture)
                except Exception as error:  # noqa: BLE001
                    counters["captures_validation_failed"] += 1
                    outcome["detail"] = outcome["detail"] or f"validation: {error}"
                    continue
                official = source_records[record_id]["v3_formal_source_enrichment"]["premise_full_names"]
                delta = structured_delta(
                    capture["state_before"], capture["state_after"],
                    official, capture["local_context_refs"], capture.get("metavariable_delta"),
                )
                enveloped = dict(capture)
                enveloped["environment"] = {
                    "source_file": source_file,
                    "direct_imports": direct_imports,
                    "lean_runtime_snapshot": capture["environment"],
                }
                canonical = canonicalize_capture(enveloped, delta, official)
                size = canonical_bytes(canonical)
                bucket = (
                    "<=4KiB" if size <= 4096 else
                    "<=16KiB" if size <= 16384 else
                    "<=64KiB" if size <= 65536 else
                    "<=256KiB" if size <= 262144 else
                    "<=1MiB" if size <= 1048576 else ">1MiB"
                )
                size_histogram[bucket] += 1
                if size > args.max_canonical_bytes:
                    counters["captures_over_size_budget"] += 1
                    continue
                canonical["corpus_metadata"] = {
                    "raw_file": f"{raw_path.parent.parent.name}/{raw_path.name}",
                    "source_file": source_file,
                    "theorem_family": selection["theorem_id"].rsplit(".", 1)[0]
                    if "." in selection["theorem_id"] else selection["theorem_id"],
                    "domain": (source_file or "").split("/")[1] if (source_file or "").count("/") >= 1 else "unknown",
                    "tactic_family": selection.get("tactic_family"),
                    "official_split": selection.get("official_split"),
                    "recorded_effect_class": selection.get("state_change_type"),
                    "canonical_bytes": size,
                    "canonical_sha256": digest(canonical),
                }
                domains[canonical["corpus_metadata"]["domain"]] += 1
                tactic_families[canonical["corpus_metadata"]["tactic_family"]] += 1
                seen_record_ids.add(record_id)
                kept.append(canonical)
                outcome["captures_kept"] += 1
                counters["captures_kept"] += 1
        except TruncatedCapture as error:
            outcome["status"] = "TRUNCATED"
            outcome["detail"] = str(error)
            counters["files_truncated"] += 1
        except json.JSONDecodeError as error:
            outcome["status"] = "CORRUPT_JSON"
            outcome["detail"] = f"{error}"
            counters["files_corrupt"] += 1
        except MemoryError as error:  # noqa: PERF203
            outcome["status"] = "MEMORY_EXHAUSTED"
            outcome["detail"] = f"{error}"
            counters["files_memory_exhausted"] += 1
        file_outcomes.append(outcome)

    kept.sort(key=lambda row: row["transition_id"])
    # Written as size-capped shards: the corpus is the object every result is measured on, so
    # it is committed rather than left external, and the commit guard caps a tracked file at
    # 5 MiB. Readers concatenate the shards in name order.
    shards = write_corpus(kept, args.corpus)

    process_status = collections.Counter(job["process_status"] for job in job_results)
    audit = {
        "campaign_dirs": [str(path) for path in args.campaign_dir],
        "selected_transitions": len(selections),
        "jobs_planned": len(job_results),
        "job_process_status": dict(process_status),
        "max_canonical_bytes": args.max_canonical_bytes,
        "max_element_bytes": args.max_element_bytes,
        "skip_files_larger_than": args.skip_files_larger_than,
        "counters": dict(counters),
        "canonical_size_histogram": dict(size_histogram),
        "corpus_transitions": len(kept),
        "corpus_shards": [path.name for path in shards],
        "corpus_sha256": digest([row["corpus_metadata"]["canonical_sha256"] for row in kept]),
        "domains": dict(domains),
        "tactic_families": dict(tactic_families),
        "file_outcomes": file_outcomes,
        "unrecovered_record_ids": sorted(set(selections) - seen_record_ids),
    }
    args.audit_json.parent.mkdir(parents=True, exist_ok=True)
    args.audit_json.write_text(json.dumps(audit, ensure_ascii=False, sort_keys=True, indent=2) + "\n")

    failed_files = [row for row in file_outcomes if row["status"] != "OK"]
    lines = [
        "# Lean Runtime V2 Canonical Corpus Audit",
        "",
        f"Selected transitions: **{len(selections)}**. Recovered into the canonical corpus: "
        f"**{len(kept)}**. Unrecovered: **{len(audit['unrecovered_record_ids'])}**.",
        "",
        "## Campaign process status",
        "",
        "| Status | Jobs |",
        "|---|---|",
    ]
    for status, count in sorted(process_status.items()):
        lines.append(f"| `{status}` | {count} |")
    lines += [
        "",
        "## Capture accounting",
        "",
        "| Counter | Value |",
        "|---|---|",
    ]
    for name, value in sorted(counters.items()):
        lines.append(f"| `{name}` | {value} |")
    lines += [
        "",
        f"Transitions whose canonical JSON exceeds the declared {args.max_canonical_bytes}-byte "
        "budget are excluded and counted; they are not silently dropped and not truncated.",
        "",
        "## Canonical size distribution",
        "",
        "| Canonical bytes | Transitions |",
        "|---|---|",
    ]
    for bucket in ("<=4KiB", "<=16KiB", "<=64KiB", "<=256KiB", "<=1MiB", ">1MiB"):
        lines.append(f"| {bucket} | {size_histogram.get(bucket, 0)} |")
    lines += ["", "## Raw files that did not read cleanly", ""]
    if failed_files:
        lines += ["| Raw file | Bytes | Status | Captures recovered before the defect |", "|---|---|---|---|"]
        for row in failed_files:
            lines.append(
                f"| `{row['raw_file']}` | {row['bytes']:,} | `{row['status']}` | {row['captures_read']} |"
            )
    else:
        lines.append("Every raw file parsed to completion.")
    lines += [
        "",
        "## Domain coverage of the recovered corpus",
        "",
        "| Mathlib domain | Transitions |",
        "|---|---|",
    ]
    for domain, count in sorted(domains.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| `{domain}` | {count} |")
    args.audit_md.parent.mkdir(parents=True, exist_ok=True)
    args.audit_md.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in audit.items() if k != "file_outcomes"}, indent=2)[:4000])


if __name__ == "__main__":
    main()
