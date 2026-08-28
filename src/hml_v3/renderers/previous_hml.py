"""Candidate wrapper for the pinned, read-only previous HML transition view."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys

from .base import Projection, Renderer


ROOT = Path(__file__).resolve().parents[3]
BRIDGE = ROOT / "scripts/render/frozen_hml_bridge.py"


def _modern_python() -> str:
    override = os.environ.get("HML_V3_MODERN_PYTHON")
    candidates = [override, sys.executable, "/opt/homebrew/bin/python3", "/usr/local/bin/python3"]
    for candidate in candidates:
        if not candidate or not Path(candidate).is_file():
            continue
        check = subprocess.run(
            [candidate, "-c", "import sys; raise SystemExit(sys.version_info < (3, 10))"],
            check=False,
        )
        if check.returncode == 0:
            return candidate
    raise RuntimeError("the frozen previous HML source requires Python 3.10 or newer")


class PreviousHmlRenderer(Renderer):
    renderer_id = "previous_hml"

    def _invoke(self, operation: str, items: list[object]) -> list[object]:
        process = subprocess.run(
            [_modern_python(), str(BRIDGE)],
            input=json.dumps({"operation": operation, "items": items}, ensure_ascii=False),
            text=True,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if process.returncode:
            raise RuntimeError(f"frozen HML bridge failed: {process.stderr.strip()}")
        result = json.loads(process.stdout)
        if not isinstance(result, list) or len(result) != len(items):
            raise RuntimeError("frozen HML bridge returned an invalid batch")
        return result

    def render_many(self, projections: list[Projection]) -> list[str]:
        return [str(item) for item in self._invoke("render_many", projections)]

    def parse_many(self, texts: list[str]) -> list[Projection]:
        return [dict(item) for item in self._invoke("parse_many", texts)]

    def render(self, projection: Projection) -> str:
        return self.render_many([projection])[0]

    def parse(self, text: str) -> Projection:
        return self.parse_many([text])[0]
