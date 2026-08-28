from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class AuditArtifactTests(unittest.TestCase):
    def test_losslessness_report(self) -> None:
        report = json.loads((ROOT / "reports/audits/LOSSLESSNESS_AUDIT_V1.json").read_text())
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["counts"]["rows"], 1000)
        self.assertEqual(report["counts"]["states"], 2000)
        self.assertEqual(report["counts"]["premise_references"], 1353)
        self.assertEqual(report["failures"], [])

    def test_gap_register_has_eight_empirical_gaps(self) -> None:
        text = (ROOT / "research/canonical_ir/REAL_MATH_GAP_REGISTER.md").read_text()
        self.assertEqual(text.count("## GAP-"), 8)
        self.assertIn("659/2,000", text)


if __name__ == "__main__":
    unittest.main()
