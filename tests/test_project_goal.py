"""The permanent goal document must stay present, intact, and reachable.

`PROJECT_GOAL.md` states what this project is for. Everything else here -- the search, the
metrics, the frontier, the MicroMath Lab -- is instrumental to it, and section 14 of that
document lists the intermediate signals that specifically do NOT count as success. It is
easy for a long-running project to start optimising one of those instead, so the goal is
pinned by a test rather than by good intentions.
"""

from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
GOAL = ROOT / "PROJECT_GOAL.md"


class ProjectGoalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.assertTrue(GOAL.is_file(), "PROJECT_GOAL.md must exist")
        self.text = GOAL.read_text(encoding="utf-8")

    def test_the_one_sentence_goal_is_present_verbatim(self) -> None:
        for fragment in (
            "DISCOVER AND BUILD A MATHEMATICAL REPRESENTATION SYSTEM THAT ALLOWS",
            "MOHEET + AI TO SOLVE MATHEMATICAL PROBLEMS MORE ACCURATELY, MORE",
            "QUICKLY, AND OVER LONGER REASONING HORIZONS THAN CONVENTIONAL",
            "MATHEMATICAL NOTATION, WHILE PRESERVING EXACT MATHEMATICAL MEANING",
            "AND SUBJECTING EVERY CLAIMED ADVANTAGE TO CONTROLLED EMPIRICAL TESTING.",
        ):
            self.assertIn(fragment, self.text)

    def test_the_falsification_section_survives(self) -> None:
        """A goal that cannot fail is not a research goal."""

        self.assertIn("18. FALSIFICATION", self.text)
        self.assertIn("Do not make HML win by changing the experiment.", self.text)
        self.assertIn("no representation consistently beats strong controls", self.text)

    def test_the_non_success_criteria_survive(self) -> None:
        """Section 14 is the one most likely to be quietly forgotten."""

        self.assertIn("14. WHAT DOES NOT COUNT AS SUCCESS", self.text)
        for fragment in ("the representation search converges",
                         "HML beats one weak control",
                         "a metric improves"):
            self.assertIn(fragment, self.text)

    def test_every_numbered_section_is_present(self) -> None:
        for number in range(1, 22):
            self.assertRegex(self.text, rf"# {number}\. ", f"section {number} missing")

    def test_the_readme_points_at_the_goal(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("PROJECT_GOAL.md", readme,
                      "a permanent goal nobody is pointed at is not permanent")


if __name__ == "__main__":
    unittest.main()
