#!/usr/bin/env python3
"""Acquire pinned Lean Workbook metadata without downloading large LFS payloads."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from clone_pinned import REPO_ROOT, acquire  # noqa: E402


if __name__ == "__main__":
    receipt = acquire(
        "lean_workbook_metadata",
        "https://huggingface.co/datasets/internlm/Lean-Workbook",
        "2e066e310b2c6d2c27616927ae131f82901c8f1c",
        REPO_ROOT / "external/checkouts/Lean-Workbook",
        True,
    )
    print(receipt["status"])
