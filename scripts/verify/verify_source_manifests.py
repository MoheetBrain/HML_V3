#!/usr/bin/env python3
"""Validate pinned formal sources and cross-check them against the dataset registry."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "data/manifests/formal_sources.json"
REGISTRY = ROOT / "data/registry/datasets.yaml"


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    sources = manifest["sources"]
    assert manifest["schema_version"] == "hml-v3-formal-source-manifest-1.0.0"
    assert len({source["source_id"] for source in sources}) == len(sources)
    local_verified = 0
    for source in sources:
        commit = source["source_commit"]
        assert len(commit) == 40 and all(char in "0123456789abcdef" for char in commit)
        assert source["source_url"].startswith("https://")
        assert (ROOT / source["acquisition_script"]).is_file()
        assert source["license"]
        if source.get("local_checkout"):
            checkout = ROOT / source["local_checkout"]
            assert (checkout / ".git").exists(), f"missing local checkout: {checkout}"
            head = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=checkout, check=True, text=True,
                stdout=subprocess.PIPE,
            ).stdout.strip()
            status = subprocess.run(
                ["git", "status", "--porcelain=v1"], cwd=checkout, check=True, text=True,
                stdout=subprocess.PIPE,
            ).stdout.strip()
            assert head == commit, f"checkout commit differs for {source['source_id']}"
            assert not status, f"checkout is dirty for {source['source_id']}"
            local_verified += 1
    registry_by_id = {record["dataset_id"]: record for record in registry["datasets"]}
    primary = registry_by_id["leandojo_benchmark4"]
    source = next(item for item in sources if item["source_id"] == "mathlib_leandojo_benchmark4")
    assert primary["source_commit"] == source["source_commit"]
    assert primary["lean_version"].startswith("v4.10.0-rc1")
    assert primary["trust_tier"] == "A"
    print(
        f"PASS: {len(sources)} pinned formal sources; {local_verified} clean exact checkouts; "
        "primary registry identity agrees"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
