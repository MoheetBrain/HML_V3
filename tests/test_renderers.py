from __future__ import annotations

import gzip
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hml_v3.canonical.models import CanonicalTransition
from hml_v3.canonical.projection import transition_projection
from hml_v3.renderers import (
    DependencyTopologicalRenderer,
    ExplicitRedundantRenderer,
    GoalLocalRenderer,
    GraphEdgeRenderer,
    LeanLikeRenderer,
    MinimalMachineCodeRenderer,
    PreviousHmlRenderer,
    SExpressionRenderer,
    StructuredEnglishRenderer,
    TypedAstRenderer,
)


class RendererTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with gzip.open(ROOT / "data/samples/lean_pipeline_v1.canonical.jsonl.gz", "rt", encoding="utf-8") as handle:
            transition = CanonicalTransition.from_dict(json.loads(next(handle)))
        cls.projection = transition_projection(transition)

    def test_all_ten_candidates_are_deterministic_and_lossless(self) -> None:
        renderers = [
            LeanLikeRenderer(), PreviousHmlRenderer(), TypedAstRenderer(),
            StructuredEnglishRenderer(), SExpressionRenderer(), GraphEdgeRenderer(),
            GoalLocalRenderer(), DependencyTopologicalRenderer(), ExplicitRedundantRenderer(),
            MinimalMachineCodeRenderer(),
        ]
        for renderer in renderers:
            with self.subTest(renderer=renderer.renderer_id):
                rendered = renderer.render(self.projection)
                self.assertEqual(rendered, renderer.render(self.projection))
                self.assertEqual(renderer.parse(rendered), self.projection)

    def test_full_corpus_audit_artifact_passes(self) -> None:
        report = json.loads((ROOT / "reports/representation/SEMANTIC_PARITY_V1.json").read_text())
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["rows"], 1000)
        self.assertEqual(len(report["renderers"]), 10)
        self.assertTrue(all(item["exact_semantic_roundtrips"] == 1000 for item in report["renderers"]))


if __name__ == "__main__":
    unittest.main()
