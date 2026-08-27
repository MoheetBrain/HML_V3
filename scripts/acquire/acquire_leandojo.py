#!/usr/bin/env python3
"""Acquire the pinned LeanDojo-v2 source checkout."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from clone_pinned import REPO_ROOT, acquire  # noqa: E402


if __name__ == "__main__":
    receipt = acquire(
        "leandojo_v2",
        "https://github.com/lean-dojo/LeanDojo-v2.git",
        "baed5eae6e87a65a446d9f54af07aab2154e7599",
        REPO_ROOT / "external/checkouts/LeanDojo-v2",
        False,
    )
    print(receipt["status"])
