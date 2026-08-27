#!/usr/bin/env python3
"""Acquire a Git source at an exact commit and emit a local provenance receipt."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess


REPO_ROOT = Path(__file__).resolve().parents[2]


def run(command: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None) -> str:
    proc = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode:
        raise RuntimeError(f"command failed ({proc.returncode}): {' '.join(command)}\n{proc.stderr}")
    return proc.stdout.strip()


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_fingerprint(path: Path) -> dict[str, object]:
    files: list[dict[str, object]] = []
    for item in sorted(path.rglob("*")):
        if not item.is_file() or ".git" in item.parts:
            continue
        relative = item.relative_to(path).as_posix()
        files.append({"path": relative, "bytes": item.stat().st_size, "sha256": file_hash(item)})
    digest = hashlib.sha256()
    for record in files:
        digest.update(json.dumps(record, sort_keys=True, separators=(",", ":")).encode())
        digest.update(b"\n")
    return {"files": len(files), "bytes": sum(int(record["bytes"]) for record in files), "sha256": digest.hexdigest()}


def acquire(name: str, url: str, commit: str, destination: Path, lfs_skip: bool) -> dict[str, object]:
    environment = os.environ.copy()
    if lfs_skip:
        environment["GIT_LFS_SKIP_SMUDGE"] = "1"
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not destination.exists():
        run(["git", "clone", "--filter=blob:none", "--no-checkout", url, str(destination)], env=environment)
    if not (destination / ".git").exists():
        raise RuntimeError(f"destination exists but is not a Git checkout: {destination}")
    origin = run(["git", "remote", "get-url", "origin"], cwd=destination)
    if origin.rstrip("/").removesuffix(".git") != url.rstrip("/").removesuffix(".git"):
        raise RuntimeError(f"origin mismatch: expected {url}, found {origin}")
    run(["git", "fetch", "--filter=blob:none", "origin", commit], cwd=destination, env=environment)
    run(["git", "checkout", "--detach", commit], cwd=destination, env=environment)
    actual = run(["git", "rev-parse", "HEAD"], cwd=destination)
    if actual != commit:
        raise RuntimeError(f"commit mismatch: expected {commit}, found {actual}")
    status = run(["git", "status", "--porcelain=v1"], cwd=destination)
    if status:
        raise RuntimeError(f"acquired checkout is dirty:\n{status}")
    fingerprint = tree_fingerprint(destination)
    receipt = {
        "schema_version": "hml-v3-acquisition-receipt-1.0.0",
        "dataset_id": name,
        "source_url": url,
        "source_commit": commit,
        "local_path": str(destination.resolve()),
        "lfs_payload_skipped": lfs_skip,
        "acquired_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "tree": fingerprint,
        "status": "ACQUIRED_PINNED_CLEAN",
    }
    receipt_dir = REPO_ROOT / "data/cache/acquisition_receipts"
    receipt_dir.mkdir(parents=True, exist_ok=True)
    (receipt_dir / f"{name}.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--url", required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument("--lfs-skip", action="store_true")
    args = parser.parse_args()
    receipt = acquire(args.name, args.url, args.commit, args.destination, args.lfs_skip)
    print(json.dumps({key: receipt[key] for key in ("dataset_id", "source_commit", "local_path", "status")}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
