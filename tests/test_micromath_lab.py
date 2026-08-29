"""Tests for MicroMath Lab V1.

`MICROMATH §32` is the load-bearing one here: the suites are mutation-tested against
representations with deliberately introduced defects, because a suite whose own unit tests
pass can still be blind to the thing it exists to detect. Two defects found while building
this lab are pinned as regressions -- a strided char-n-gram feature that condemned a sound
benchmark, and two stresses built on an ordering the semantic contract declares to be a set.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hml_v3.micromath import counterfactuals as CF  # noqa: E402
from hml_v3.micromath import deterministic, shortcut_controls, stresses as S  # noqa: E402
from hml_v3.micromath.candidates import CONTROLS, load_controls  # noqa: E402
from hml_v3.micromath.corpus import load_split  # noqa: E402
from hml_v3.micromath.domains import DOMAINS, MODULE_MAP, classify  # noqa: E402
from hml_v3.micromath.neural import build_items, parse_choice  # noqa: E402
from hml_v3.micromath.schema import MicroPair, state_digest  # noqa: E402
from hml_v3.micromath.sequential import paired_bootstrap, rungs  # noqa: E402
from hml_v3.micromath.split import assign, split_pairs  # noqa: E402
from hml_v3.representation_search.projection import semantic_core  # noqa: E402

LAB = ROOT / "data/micromath_lab_v1"


def load(name: str) -> list[MicroPair]:
    return [MicroPair.from_dict(row) for row in load_split(LAB, name)]


class LabIntegrityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.dev, self.shadow, self.hidden = load("micro_dev"), load("micro_shadow"), load("micro_hidden")
        if not self.dev:
            self.skipTest("lab not built")
        self.all = self.dev + self.shadow + self.hidden

    def test_no_pair_crosses_a_split(self) -> None:
        dev = {p.pair_id for p in self.dev}
        shadow = {p.pair_id for p in self.shadow}
        hidden = {p.pair_id for p in self.hidden}
        self.assertEqual(dev & shadow, set())
        self.assertEqual(dev & hidden, set())
        self.assertEqual(shadow & hidden, set())

    def test_no_base_state_crosses_a_split(self) -> None:
        """A pair's two arms share a base state, so a leaked base leaks the answer."""

        seen: dict[str, str] = {}
        for split, pairs in (("dev", self.dev), ("shadow", self.shadow),
                             ("hidden", self.hidden)):
            for pair in pairs:
                previous = seen.setdefault(pair.base_transition_id, split)
                self.assertEqual(previous, split, pair.base_transition_id)

    def test_every_split_can_speak_about_every_stress(self) -> None:
        for name, pairs in (("dev", self.dev), ("shadow", self.shadow),
                            ("hidden", self.hidden)):
            covered = {p.stress for p in pairs}
            self.assertEqual(covered, set(S.STRESSES), f"{name} covers only {covered}")

    def test_one_pair_per_cell_and_the_cell_is_real(self) -> None:
        cells = [p.cell for p in self.all]
        self.assertEqual(len(cells), len(set(cells)))
        for domain, stress in cells:
            self.assertIn(domain, DOMAINS)
            self.assertIn(stress, S.STRESSES)

    def test_the_two_arms_differ_and_the_answers_differ(self) -> None:
        for pair in self.all:
            self.assertNotEqual(state_digest(pair.state_a), state_digest(pair.state_b),
                                pair.pair_id)
            self.assertNotEqual(pair.answer_a, pair.answer_b, pair.pair_id)
            self.assertEqual(set(pair.options), {pair.answer_a, pair.answer_b},
                             pair.pair_id)

    def test_the_counterfactual_changes_the_declared_semantic_core(self) -> None:
        """A transposition the contract calls a no-op would have no ground truth.

        Two stresses originally failed this: PREMISE and ACTION_ARGUMENT permuted lists that
        `semantic_core` stores sorted, so A and B were the same object by declaration and
        every representation "failed" a question that had no answer.
        """

        for pair in self.all:
            self.assertNotEqual(
                semantic_core(pair.state_a), semantic_core(pair.state_b), pair.pair_id)

    def test_the_option_order_is_balanced(self) -> None:
        """Otherwise telling A from B by any means at all hands over the answer."""

        first_is_answer_a = sum(1 for p in self.all if p.options[0] == p.answer_a)
        self.assertGreater(first_is_answer_a, 0)
        self.assertLess(first_is_answer_a, len(self.all))

    def test_split_assignment_is_deterministic(self) -> None:
        for pair in self.all[:8]:
            self.assertEqual(assign(pair.pair_id), assign(pair.pair_id))

    def test_manifest_records_unpopulated_cells_rather_than_hiding_them(self) -> None:
        manifest = json.loads((LAB / "manifest.json").read_text())
        self.assertEqual(manifest["cells_total"], len(DOMAINS) * len(S.STRESSES))
        self.assertEqual(manifest["cells_populated"], len(self.all))
        self.assertEqual(
            manifest["cells_populated"] + len(manifest["cells_unpopulated"]),
            manifest["cells_total"])
        for entry in manifest["cells_unpopulated"]:
            self.assertIn("reason", entry)

    def test_the_lab_never_touched_the_sealed_split(self) -> None:
        manifest = json.loads((LAB / "manifest.json").read_text())
        self.assertEqual(manifest["provenance"]["sealed_final_v2"], "NOT OPENED")
        self.assertNotIn("sealed", manifest["provenance"]["corpus"].lower().replace(
            "search_pool", ""))


class DomainTests(unittest.TestCase):
    def test_a_non_mathlib_path_is_mixed_not_forced_into_a_domain(self) -> None:
        row = {"corpus_metadata": {"source_file": ".lake/packages/batteries/X.lean"}}
        domain, confidence = classify(row)
        self.assertEqual(domain, "MIXED")
        self.assertEqual(confidence, "NOT_MATHLIB")

    def test_every_mapped_module_lands_in_a_declared_domain(self) -> None:
        for module, (domain, confidence) in MODULE_MAP.items():
            self.assertIn(domain, DOMAINS, module)
            self.assertIn(confidence, {"HIGH", "MEDIUM"}, module)


class KnownBadRepresentationTests(unittest.TestCase):
    """§32: build representations with known defects and require detection."""

    def setUp(self) -> None:
        self.pairs = load("micro_dev")
        if not self.pairs:
            self.skipTest("lab not built")
        self.control = {c.label: c for c in load_controls()}["LEAN_LIKE"]

    def _broken(self, mutate):
        compiler = self.control.compiler

        class Broken:
            surface = compiler.surface
            candidate_id = "BROKEN"

            def render_text(self, state):
                return mutate(compiler.render_text(state))

            def render(self, state):
                rendered = compiler.render(state)
                rendered.text = mutate(rendered.text)
                return rendered

            def parse_core(self, text, codec):
                return compiler.parse_core(text, codec)

        return Broken()

    def test_a_representation_that_hides_the_relation_is_caught(self) -> None:
        """Collapse the two transposed entities to one name; the arms must go identical.

        The first version of this substituted ``f\\d+``, which is not how every candidate
        encodes an identity, so the mutation silently did nothing and the test passed a
        representation it had not actually broken. The defect is injected against the pair's
        own option strings instead, which is what the transposition moved.
        """

        compiler = self.control.compiler
        checked = 0
        for pair in self.pairs:
            if pair.stress not in (S.BINDER, S.DEPENDENCY, S.EXPRESSION_DEPTH):
                continue
            rendered = compiler.render(pair.state_a)
            # Identities reach the page through the codec, so the defect has to be injected
            # against the encoded forms. Substituting the raw canonical ids matched nothing
            # and "broke" a representation that was still working perfectly.
            names = [rendered.codec.encode(option) for option in pair.options]
            names = [n for n in names if isinstance(n, str)]
            if len(names) != 2:
                continue
            broken = self._broken(
                lambda text, names=names:
                text.replace(names[0], "COLLAPSED").replace(names[1], "COLLAPSED"))
            measurement = deterministic.measure_pair(broken, pair)
            self.assertFalse(
                measurement.renders_differ,
                f"{pair.pair_id}: hiding both identities must make the arms identical")
            intact = deterministic.measure_pair(compiler, pair)
            self.assertTrue(intact.renders_differ,
                            f"{pair.pair_id}: the sound representation must keep them apart")
            checked += 1
        self.assertGreater(checked, 0)

    def test_a_leaky_benchmark_is_caught_by_the_shortcut_audit(self) -> None:
        """Append the correct answer to the rendering: a shortcut rule must find it."""

        pairs = self.pairs
        compiler = self.control.compiler
        answer_by_state = {}
        for pair in pairs:
            answer_by_state[state_digest(pair.state_a)] = pair.answer_a
            answer_by_state[state_digest(pair.state_b)] = pair.answer_b

        class Leaky:
            surface = compiler.surface
            candidate_id = "LEAKY"

            def render(self, state):
                rendered = compiler.render(state)
                answer = answer_by_state.get(state_digest(state))
                if answer is not None:
                    # Repeat the answer in the form the page actually uses, or the injected
                    # defect is invisible to an audit that reads encoded identities.
                    encoded = rendered.codec.encode(answer)
                    name = encoded if isinstance(encoded, str) else answer
                    rendered.text = f"{rendered.text}\n{name} {name} {name}"
                return rendered

            def render_text(self, state):
                return self.render(state).text

            def parse_core(self, text, codec):
                return compiler.parse_core(text, codec)

        audit = shortcut_controls.audit(Leaky(), pairs)
        self.assertEqual(audit["verdict"], "BENCHMARK_INVALID")
        self.assertIn("more_frequent_option", audit["leaking_features"])

    def test_the_sound_benchmark_passes_the_same_audit(self) -> None:
        audit = shortcut_controls.audit(self.control.compiler, self.pairs)
        self.assertEqual(audit["verdict"], "PASS", audit["leaking_features"])
        for rule, accuracy in audit["answer_targeted_controls"]["accuracy"].items():
            self.assertLessEqual(accuracy, shortcut_controls.ANSWER_CONTROL_LIMIT, rule)

    def test_char_ngrams_are_a_bag_not_a_stride(self) -> None:
        """Regression: the strided version reported a difference on every sound pair."""

        grams = shortcut_controls._char_ngrams("abcdefgh", 4)
        self.assertEqual(sum(grams.values()), 5)
        self.assertEqual(shortcut_controls._char_ngrams("abcd", 4), {"abcd": 1})


class ProbeTests(unittest.TestCase):
    def test_a_response_naming_both_options_is_not_a_choice(self) -> None:
        self.assertIsNone(parse_choice("either f3 or f7", ("f3", "f7")))
        self.assertEqual(parse_choice("f7", ("f3", "f7")), "f7")
        self.assertEqual(parse_choice("The answer is f3.", ("f3", "f7")), "f3")
        self.assertIsNone(parse_choice("", ("f3", "f7")))

    def test_items_are_built_two_per_pair_and_stay_paired(self) -> None:
        pairs = load("micro_dev")
        if not pairs:
            self.skipTest("lab not built")
        control = {c.label: c for c in load_controls()}["LEAN_LIKE"]
        items = build_items(control.compiler, pairs[:4])
        self.assertEqual(len(items), 8)
        self.assertEqual({i.arm for i in items}, {"A", "B"})

    def test_the_four_required_controls_exist(self) -> None:
        self.assertEqual(set(CONTROLS), {"LEAN_LIKE", "STRUCTURED_ENGLISH",
                                         "TYPED_AST", "OLD_HML"})
        self.assertEqual(len(load_controls()), 4)


class SequentialTests(unittest.TestCase):
    def test_the_ladder_ends_at_the_available_items(self) -> None:
        self.assertEqual(rungs(58)[-1], 58)
        self.assertEqual(rungs(12), [12])
        self.assertTrue(all(a < b for a, b in zip(rungs(200), rungs(200)[1:])))

    def test_a_clearly_worse_candidate_is_dominated(self) -> None:
        verdict = paired_bootstrap([0.0] * 24, [1.0] * 24)
        self.assertTrue(verdict.dominated)
        self.assertFalse(verdict.superior)

    def test_an_identical_candidate_is_neither_dominated_nor_superior(self) -> None:
        verdict = paired_bootstrap([0.5] * 24, [0.5] * 24)
        self.assertFalse(verdict.dominated)
        self.assertFalse(verdict.superior)

    def test_the_bootstrap_is_deterministic(self) -> None:
        left = paired_bootstrap([1.0, 0.0, 0.5] * 8, [0.5] * 24, seed="x")
        right = paired_bootstrap([1.0, 0.0, 0.5] * 8, [0.5] * 24, seed="x")
        self.assertEqual(left.to_dict(), right.to_dict())


class HiddenGuardTests(unittest.TestCase):
    def test_the_audit_script_refuses_micro_hidden(self) -> None:
        import subprocess

        for script in ("audit_lab_v1.py", "run_neural_probe.py"):
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts/micromath" / script),
                 "--split", "micro_hidden"],
                capture_output=True, text=True, check=False, cwd=ROOT)
            self.assertNotEqual(result.returncode, 0, script)
            self.assertIn("REFUSED", result.stdout + result.stderr, script)


if __name__ == "__main__":
    unittest.main()
