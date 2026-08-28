from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class RegistryAndManifestTests(unittest.TestCase):
    def test_dataset_registry_is_complete_and_unique(self) -> None:
        registry = json.loads((ROOT / "data/registry/datasets.yaml").read_text())
        required = {
            "dataset_id", "name", "source_url", "source_commit", "source_version", "license",
            "local_path", "acquisition_method", "sha256", "formal_system", "lean_version",
            "mathlib_version", "rows", "theorems", "proof_states", "transitions", "trust_tier",
            "verification_status", "train_allowed", "evaluation_only", "contamination_notes", "notes",
        }
        ids = [item["dataset_id"] for item in registry["datasets"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(ids), 26)
        for item in registry["datasets"]:
            self.assertEqual(set(item), required)
            self.assertIn(item["trust_tier"], {"A", "B", "C", "D", "E"})

    def test_pipeline_manifest_hashes_counts_and_deterministic_gzip(self) -> None:
        manifest = json.loads((ROOT / "data/manifests/lean_pipeline_v1.json").read_text())
        self.assertEqual(manifest["counts"]["transitions"], 1000)
        self.assertEqual(manifest["counts"]["theorem_source_spans"], 1000)
        self.assertEqual(manifest["counts"]["premise_references"], 1353)
        for descriptor in manifest["files"].values():
            path = ROOT / descriptor["path"]
            self.assertEqual(sha256(path), descriptor["sha256"])
            self.assertEqual(path.read_bytes()[4:8], b"\0\0\0\0")
            with gzip.open(path, "rt", encoding="utf-8") as handle:
                self.assertEqual(sum(1 for _ in handle), descriptor["rows"])

    def test_formal_source_and_representation_manifests(self) -> None:
        sources = json.loads((ROOT / "data/manifests/formal_sources.json").read_text())
        self.assertEqual(len(sources["sources"]), 5)
        for item in sources["sources"]:
            self.assertRegex(item["source_commit"], r"^[0-9a-f]{40}$")
            self.assertTrue((ROOT / item["acquisition_script"]).is_file())
        family = json.loads((ROOT / "data/representations/initial_renderer_genomes.json").read_text())
        self.assertEqual(family["selection_status"], "NO_FINAL_REPRESENTATION_SELECTED")
        self.assertEqual(len(family["candidates"]), 10)
        self.assertEqual(len({item["renderer_id"] for item in family["candidates"]}), 10)


if __name__ == "__main__":
    unittest.main()
