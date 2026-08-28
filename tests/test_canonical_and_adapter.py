from __future__ import annotations

import gzip
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hml_v3.adapters.lean.adapter import adapt_lean_transition, lean_transition_from_record
from hml_v3.adapters.lean.parser import parse_lean_state
from hml_v3.canonical.models import CanonicalTransition


class CanonicalAndAdapterTests(unittest.TestCase):
    def test_parser_preserves_multiline_declaration_and_multiple_goals(self) -> None:
        raw = """case first
x : Nat
h :
  x = x
⊢ x = x

case second
y : Nat
⊢ y = y"""
        parsed = parse_lean_state(raw)
        self.assertTrue(parsed.clean)
        self.assertEqual(len(parsed.goals), 2)
        self.assertEqual(parsed.goals[0].declarations[1].type_text, "x = x")
        self.assertEqual(parsed.goals[1].case_label, "second")

    def test_real_source_adapter_and_canonical_roundtrip(self) -> None:
        with gzip.open(ROOT / "data/samples/lean_pipeline_v1.source.jsonl.gz", "rt", encoding="utf-8") as handle:
            source_record = json.loads(next(handle))
        transition = adapt_lean_transition(lean_transition_from_record(source_record))
        reconstructed = CanonicalTransition.from_dict(json.loads(transition.canonical_json()))
        self.assertEqual(reconstructed.canonical_json(), transition.canonical_json())
        enrichment = source_record["v3_formal_source_enrichment"]
        self.assertEqual(list(transition.action.referenced_premises), enrichment["premise_full_names"])
        self.assertTrue(all(enrichment["exact_source_join"].values()))
        self.assertEqual(transition.state_before.source_specific["raw_state"], source_record["lean"]["raw_state_before"])

    def test_committed_canonical_rows_have_calibrated_verifier_labels(self) -> None:
        statuses: dict[str, int] = {}
        with gzip.open(ROOT / "data/samples/lean_pipeline_v1.canonical.jsonl.gz", "rt", encoding="utf-8") as handle:
            for line in handle:
                transition = CanonicalTransition.from_dict(json.loads(line))
                statuses[transition.verifier_result.status] = statuses.get(transition.verifier_result.status, 0) + 1
        self.assertEqual(statuses, {"FRESH_REPLAY_PASS": 32, "FORMAL_TRACE_ACCEPTED": 968})


if __name__ == "__main__":
    unittest.main()
