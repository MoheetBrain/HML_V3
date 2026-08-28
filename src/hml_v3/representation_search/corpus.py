"""Sharded storage for the canonical corpus.

The corpus is a generated artifact, but it is also the scientific object every result in this
repository is measured on, so it is committed rather than left external. The commit-continuity
guard caps a single tracked file at 5 MiB, and the corpus exceeds that, so it is written as
size-capped shards. Sharding changes nothing about the content: readers concatenate the parts
in name order and the result is byte-identical to the single-file form.
"""

from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Iterator

SHARD_SUFFIX = ".jsonl.gz"
DEFAULT_SHARD_BYTES = 4 * 1024 * 1024


def shard_paths(base: Path) -> list[Path]:
    """Every shard for ``base``, in name order.

    ``base`` may be the historical single file, its stem, or the directory holding shards.
    """

    if base.is_dir():
        return sorted(base.glob(f"*{SHARD_SUFFIX}"))
    stem = base.name
    for suffix in (SHARD_SUFFIX, ".jsonl", ".gz"):
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]
            break
    shards = sorted(base.parent.glob(f"{stem}.part-*{SHARD_SUFFIX}"))
    if shards:
        return shards
    return [base] if base.exists() else []


def load_corpus(base: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    paths = shard_paths(base)
    if not paths:
        raise FileNotFoundError(f"no corpus shards for {base}")
    for path in paths:
        with gzip.open(path, "rt", encoding="utf-8") as handle:
            rows.extend(json.loads(line) for line in handle if line.strip())
    return rows


def iter_corpus(base: Path) -> Iterator[dict[str, Any]]:
    for path in shard_paths(base):
        with gzip.open(path, "rt", encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    yield json.loads(line)


def _encode(row: dict[str, Any]) -> bytes:
    return (json.dumps(row, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")) + "\n").encode()


def write_corpus(
    rows: Iterable[dict[str, Any]], base: Path, max_bytes: int = DEFAULT_SHARD_BYTES,
) -> list[Path]:
    """Write ``rows`` as gzip shards, each at most ``max_bytes`` on disk.

    Deterministic: ``mtime=0`` in every member, rows written in the order given, and a shard
    boundary taken only when adding the next row would exceed the cap.
    """

    base.parent.mkdir(parents=True, exist_ok=True)
    stem = base.name
    for suffix in (SHARD_SUFFIX, ".jsonl", ".gz"):
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]
            break
    for stale in base.parent.glob(f"{stem}.part-*{SHARD_SUFFIX}"):
        stale.unlink()
    if base.exists() and base.is_file():
        base.unlink()

    written: list[Path] = []
    index = 0
    handle = None
    raw = None

    def open_shard(number: int):
        path = base.parent / f"{stem}.part-{number:03d}{SHARD_SUFFIX}"
        stream = path.open("wb")
        return path, stream, gzip.GzipFile(filename="", mode="wb", fileobj=stream, mtime=0)

    path, raw, handle = open_shard(index)
    written.append(path)
    for row in rows:
        handle.write(_encode(row))
        handle.flush()
        if raw.tell() >= max_bytes:
            handle.close()
            raw.close()
            index += 1
            path, raw, handle = open_shard(index)
            written.append(path)
    handle.close()
    raw.close()
    if written and written[-1].stat().st_size == 0:
        written.pop().unlink()
    return written


def corpus_sha256(base: Path) -> str:
    """Content hash over the concatenated rows, independent of how they are sharded."""

    digest = hashlib.sha256()
    for row in iter_corpus(base):
        digest.update(_encode(row))
    return digest.hexdigest()
