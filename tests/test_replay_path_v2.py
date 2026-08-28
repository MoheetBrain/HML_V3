from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "prepare_lean_runtime_campaign_v2",
    ROOT / "scripts/extract/prepare_lean_runtime_campaign_v2.py",
)
assert SPEC is not None and SPEC.loader is not None
PREPARE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PREPARE)


class ReplayPathV2Tests(unittest.TestCase):
    def test_theorem_scoped_trace_join_recovers_exact_nested_source_range(self) -> None:
        source = b"theorem demo : True := by\n  trivial\n"
        start = source.index(b"trivial")
        end = start + len(b"trivial")
        trace = {
            "tactics": [
                {"pos": start, "endPos": end, "stateBefore": "\u22a2 True", "stateAfter": "no goals"},
                # LeanDojo traces may repeat an identical event; theorem-scoped indexing deduplicates it.
                {"pos": start, "endPos": end, "stateBefore": "\u22a2 True", "stateAfter": "no goals"},
            ]
        }
        record = {
            "example_id": "Mathlib/Demo.lean::demo::0",
            "source_file": "Mathlib/Demo.lean",
            "transition_index": 0,
            "lean": {
                "raw_state_before": "\u22a2 True",
                "raw_tactic": "trivial",
                "raw_state_after": "no goals",
            },
            "v3_formal_source_enrichment": {
                "theorem_start": [1, 0],
                "theorem_end": [2, 9],
            },
        }
        with tempfile.TemporaryDirectory() as temporary:
            runtime_root = Path(temporary)
            source_path = runtime_root / "Mathlib/Demo.lean"
            trace_path = runtime_root / ".lake/build/ir/Mathlib/Demo.ast.json"
            source_path.parent.mkdir(parents=True)
            trace_path.parent.mkdir(parents=True)
            source_path.write_bytes(source)
            trace_path.write_text(json.dumps(trace), encoding="utf-8")
            joined = PREPARE.source_location_join(record, runtime_root, {}, {})
        self.assertEqual(joined["source_start_raw"], start)
        self.assertEqual(joined["source_end_raw"], end)
        self.assertTrue(joined["historical_state_pair_exact"])
        self.assertTrue(joined["historical_action_exact"])
        self.assertEqual(
            joined["join_mechanism"],
            "THEOREM_SCOPED_FILTERED_DEDUPLICATED_TRACE_INDEX",
        )


if __name__ == "__main__":
    unittest.main()
