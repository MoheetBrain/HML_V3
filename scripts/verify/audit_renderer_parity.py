#!/usr/bin/env python3
"""Audit semantic round trips for every initial renderer on LEAN_PIPELINE_V1."""

from __future__ import annotations

from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import re
import statistics
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hml_v3.canonical.models import CanonicalTransition  # noqa: E402
from hml_v3.canonical.projection import transition_projection  # noqa: E402
from hml_v3.renderers import (  # noqa: E402
    DependencyTopologicalRenderer,
    ExplicitRedundantRenderer,
    GraphEdgeRenderer,
    GoalLocalRenderer,
    LeanLikeRenderer,
    MinimalMachineCodeRenderer,
    PreviousHmlRenderer,
    SExpressionRenderer,
    StructuredEnglishRenderer,
    TypedAstRenderer,
)
from hml_v3.renderers.base import canonical_projection_json  # noqa: E402


CORPUS = ROOT / "data/samples/lean_pipeline_v1.canonical.jsonl.gz"
JSON_REPORT = ROOT / "reports/representation/SEMANTIC_PARITY_V1.json"
MARKDOWN_REPORT = ROOT / "reports/representation/SEMANTIC_PARITY_V1.md"


def percentile(values: list[int], fraction: float) -> int:
    ordered = sorted(values)
    return ordered[min(round((len(ordered) - 1) * fraction), len(ordered) - 1)]


def measurements(texts: list[str]) -> dict[str, Any]:
    characters = [len(text) for text in texts]
    byte_counts = [len(text.encode("utf-8")) for text in texts]
    tokens = [len(re.findall(r"\S+", text)) for text in texts]
    lines = [len(text.splitlines()) for text in texts]
    digest = hashlib.sha256()
    for text in texts:
        payload = text.encode("utf-8")
        digest.update(len(payload).to_bytes(8, "big"))
        digest.update(payload)
    return {
        "characters": {
            "mean": round(statistics.mean(characters), 3),
            "median": statistics.median(characters),
            "p95": percentile(characters, 0.95),
        },
        "utf8_bytes": {
            "mean": round(statistics.mean(byte_counts), 3),
            "median": statistics.median(byte_counts),
            "p95": percentile(byte_counts, 0.95),
        },
        "whitespace_tokens": {
            "mean": round(statistics.mean(tokens), 3),
            "median": statistics.median(tokens),
            "p95": percentile(tokens, 0.95),
        },
        "lines": {
            "mean": round(statistics.mean(lines), 3),
            "median": statistics.median(lines),
            "p95": percentile(lines, 0.95),
        },
        "literal_unicode_escape_sequences": sum(
            len(re.findall(r"\\u[0-9a-fA-F]{4}", text)) for text in texts
        ),
        "rendered_batch_sha256": digest.hexdigest(),
    }


def main() -> int:
    with gzip.open(CORPUS, "rt", encoding="utf-8") as handle:
        transitions = [CanonicalTransition.from_dict(json.loads(line)) for line in handle]
    projections = [transition_projection(item) for item in transitions]
    renderers = [
        LeanLikeRenderer(),
        PreviousHmlRenderer(),
        TypedAstRenderer(),
        StructuredEnglishRenderer(),
        SExpressionRenderer(),
        GraphEdgeRenderer(),
        GoalLocalRenderer(),
        DependencyTopologicalRenderer(),
        ExplicitRedundantRenderer(),
        MinimalMachineCodeRenderer(),
    ]
    results: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    for renderer in renderers:
        if isinstance(renderer, PreviousHmlRenderer):
            texts = renderer.render_many(projections)
            reparsed = renderer.parse_many(texts)
            deterministic = renderer.render_many(projections) == texts
        else:
            texts = [renderer.render(item) for item in projections]
            reparsed = [renderer.parse(text) for text in texts]
            deterministic = all(renderer.render(item) == text for item, text in zip(projections, texts))
        mismatches = [
            index
            for index, (expected, actual) in enumerate(zip(projections, reparsed))
            if canonical_projection_json(expected) != canonical_projection_json(actual)
        ]
        for index in mismatches[:10]:
            failures.append(
                {
                    "renderer_id": renderer.renderer_id,
                    "row": index,
                    "transition_id": transitions[index].transition_id,
                }
            )
        results.append(
            {
                "renderer_id": renderer.renderer_id,
                "renderer_version": renderer.version,
                "rows": len(texts),
                "exact_semantic_roundtrips": len(texts) - len(mismatches),
                "mismatches": len(mismatches),
                "deterministic_bytes": deterministic,
                "status": "PASS" if not mismatches and deterministic else "FAIL",
                "measurements": measurements(texts),
            }
        )

    status = "PASS" if all(item["status"] == "PASS" for item in results) else "FAIL"
    report = {
        "schema_version": "hml-v3-semantic-parity-report-1.0.0",
        "status": status,
        "corpus": "LEAN_PIPELINE_V1",
        "rows": len(projections),
        "semantic_projection": "src/hml_v3/canonical/projection.py",
        "renderers": results,
        "failures": failures,
        "interpretation": {
            "roundtrip": "Exact equality of the shared model-facing semantic projection after render and parse.",
            "previous_hml": "Uses native frozen HML claims/goals/action fields plus a visible source compatibility block only for semantics absent from the old schema.",
            "token_metric": "Whitespace token counts are descriptive only; no model tokenizer or learning claim is made.",
        },
    }
    JSON_REPORT.parent.mkdir(parents=True, exist_ok=True)
    JSON_REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n")

    lines = [
        "# Semantic Parity Audit V1",
        "",
        f"**Status: {status}.** All candidates are evaluated on the same {len(projections):,} canonical transitions.",
        "",
        "Parity means exact render/parse equality of the shared model-facing semantic projection. It does not mean that the surfaces are equally learnable.",
        "",
        "| Renderer | Exact round trips | Deterministic | Mean UTF-8 bytes | Mean whitespace tokens | Status |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for item in results:
        lines.append(
            f"| `{item['renderer_id']}` | {item['exact_semantic_roundtrips']:,}/{item['rows']:,} "
            f"| {'yes' if item['deterministic_bytes'] else 'no'} "
            f"| {item['measurements']['utf8_bytes']['mean']:,.1f} "
            f"| {item['measurements']['whitespace_tokens']['mean']:,.1f} | **{item['status']}** |"
        )
    lines.extend(
        [
            "",
            "## Previous-HML qualification",
            "",
            "The previous HML candidate is imported read-only at commit `b011511e72572608eb7836d3b8a1a6bb794c890d`. Declarations, goals, tactic text, premise dependencies, and effect maps occupy native old-HML fields. Binder metadata, per-goal context membership, metavariables, namespace references, and V3-only state fields are carried in the old view's visible `source` JSON block. Its parity result is therefore a compatibility-bridged baseline, not evidence that old HML natively modeled every V3 field.",
            "",
            "## Scope",
            "",
            "These checks establish serializer determinism and semantic preservation only. No representation is selected, no model is trained, and the whitespace counts are not used as a proxy for learning quality.",
            "",
        ]
    )
    MARKDOWN_REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"status": status, "rows": len(projections), "renderers": len(results)}))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
