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
            "verification_status", "train_allowed", "evaluation_only", "contamination_notes",
            "notes", "evidence_role", "not_lean_truth",
        }
        ids = [item["dataset_id"] for item in registry["datasets"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(ids), 27)
        for item in registry["datasets"]:
            self.assertEqual(set(item), required)
            self.assertIn(item["trust_tier"], {"A", "B", "C", "D", "E"})

    def test_evidence_roles_cannot_launder_non_lean_material_into_formal_truth(self) -> None:
        """The prohibited conflation, enforced rather than documented.

        PRM800K's -1/0/+1 are human judgements of usefulness and GSM8K's answers are
        arithmetic narratives. Neither is a verifier verdict. This test is what stops a
        later edit from quietly promoting either into the tier the Lean corpus occupies.
        """

        registry = json.loads((ROOT / "data/registry/datasets.yaml").read_text())
        vocabulary = set(registry["evidence_roles"])
        self.assertIn("DISCOVERY_GRAPH_EVIDENCE", vocabulary)
        self.assertIn("NATURAL_LANGUAGE_MATH_EVIDENCE", vocabulary)
        for item in registry["datasets"]:
            self.assertIn(item["evidence_role"], vocabulary, item["dataset_id"])
            # not_lean_truth is derived from formal_system, never asserted independently.
            self.assertEqual(
                item["not_lean_truth"], item["formal_system"] != "Lean 4", item["dataset_id"])
            if item["not_lean_truth"]:
                self.assertNotEqual(
                    item["evidence_role"], "LEAN_FORMAL_TRUTH", item["dataset_id"])
                self.assertNotIn(item["trust_tier"], {"A", "B"}, item["dataset_id"])

    def test_prm800k_and_gsm8k_are_registered_with_their_declared_roles(self) -> None:
        registry = json.loads((ROOT / "data/registry/datasets.yaml").read_text())
        by_id = {item["dataset_id"]: item for item in registry["datasets"]}

        prm = by_id["openai_prm800k_official"]
        self.assertEqual(prm["evidence_role"], "DISCOVERY_GRAPH_EVIDENCE")
        self.assertTrue(prm["not_lean_truth"])

        gsm = by_id["openai_gsm8k"]
        self.assertEqual(gsm["evidence_role"], "NATURAL_LANGUAGE_MATH_EVIDENCE")
        self.assertTrue(gsm["not_lean_truth"])
        self.assertIsNone(gsm["formal_system"])
        self.assertEqual(gsm["trust_tier"], "D")
        self.assertRegex(gsm["source_commit"], r"^[0-9a-f]{40}$")
        self.assertFalse(gsm["train_allowed"])
        # 7,473 train + 1,319 test, counted by reading the files at the pinned commit.
        self.assertEqual(gsm["rows"], 8792)
        self.assertTrue((ROOT / "scripts/acquire/acquire_gsm8k.sh").is_file())

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
