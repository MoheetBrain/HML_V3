"""Tests for MicroMath Lab V2: the firewall, the anonymiser, the ablations, the rule.

The load-bearing one is `ReservedSplitTests`. `FM-043` happened because the guard in place
checked the split *name* a script was given, and the run that consumed both holdouts never
named a split -- it asked a shared pool for fresh states and the pool obliged. So the tests
here attack the firewall the way that run did: by never mentioning a split at all.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hml_v3.micromath import ablate  # noqa: E402
from hml_v3.micromath import anonymise  # noqa: E402
from hml_v3.micromath import calibration_v2 as C  # noqa: E402
from hml_v3.micromath import instruments_v2 as IV2  # noqa: E402
from hml_v3.micromath import ladders as L  # noqa: E402
from hml_v3.micromath import shortcut_v2 as SC  # noqa: E402
from hml_v3.micromath import stresses as S  # noqa: E402
from hml_v3.micromath.architectures import (  # noqa: E402
    DETECTS, EXPRESSION_ARCHITECTURES, KNOWN_BAD, MULTI_GOAL_ARCHITECTURES,
    realise, realise_known_bad)
from hml_v3.micromath.corpus import load_split  # noqa: E402
from hml_v3.micromath.firewall import (  # noqa: E402
    DEV, HIDDEN, SHADOW, SplitFirewall, SplitViolation, base_state_identity)

LAB = ROOT / "data/micromath_lab_v2"


def items(name: str) -> list[IV2.MicroItem]:
    return [IV2.MicroItem.from_dict(row) for row in load_split(LAB, name)]


def transition(identifier: str, source: str = "Mathlib/Algebra/X.lean") -> dict:
    return {"transition_id": identifier, "source_specific_reference": source,
            "provenance": {"declaration": identifier}}


class FirewallTests(unittest.TestCase):
    def setUp(self) -> None:
        self.firewall = SplitFirewall()
        self.dev = [transition(f"dev{i}") for i in range(3)]
        self.hidden = [transition(f"hid{i}") for i in range(3)]
        self.firewall.register(DEV, self.dev)
        self.firewall.register(HIDDEN, self.hidden)

    def test_a_state_cannot_be_registered_to_two_compartments(self) -> None:
        with self.assertRaises(SplitViolation):
            self.firewall.register(SHADOW, self.dev)

    def test_dev_cannot_consume_a_hidden_state_even_by_asking_for_dev(self) -> None:
        # The FM-043 shape exactly: the caller names its own compartment and hands over a
        # state that belongs to another. A name check passes this; the firewall must not.
        with self.assertRaises(SplitViolation):
            self.firewall.admit(DEV, self.hidden)

    def test_unregistered_states_are_refused_by_default(self) -> None:
        with self.assertRaises(SplitViolation):
            self.firewall.admit(DEV, [transition("fresh")])
        # Minting genuinely new items is legitimate, but it has to be asked for.
        self.assertEqual(
            len(self.firewall.admit(DEV, [transition("fresh")], allow_unregistered=True)), 1)

    def test_a_retired_state_can_never_be_admitted_again(self) -> None:
        spent = [transition("v1")]
        self.firewall.retire("V1_MICRO_HIDDEN", spent)
        for compartment in (DEV, SHADOW, HIDDEN):
            with self.assertRaises(SplitViolation):
                self.firewall.admit(compartment, spent, allow_unregistered=True)

    def test_available_excludes_registered_and_retired(self) -> None:
        self.firewall.retire("V1", [transition("old")])
        pool = self.dev + self.hidden + [transition("old"), transition("free")]
        available = self.firewall.available(pool)
        self.assertEqual([t["transition_id"] for t in available], ["free"])

    def test_identity_survives_a_round_trip_and_ignores_unrelated_fields(self) -> None:
        base = transition("x")
        noisy = dict(base, state_after={"goals": []}, corpus_metadata={"anything": 1})
        self.assertEqual(base_state_identity(base), base_state_identity(noisy))

    def test_a_registry_from_another_version_is_refused(self) -> None:
        path = ROOT / "reports/.firewall_version_probe.json"
        payload = self.firewall.to_dict()
        payload["firewall_version"] = "micromath-firewall-v0.0.0"
        path.write_text(json.dumps(payload))
        try:
            with self.assertRaises(SplitViolation):
                SplitFirewall.load(path)
        finally:
            path.unlink(missing_ok=True)


class ShippedLabTests(unittest.TestCase):
    """The lab as built, not a fixture."""

    def setUp(self) -> None:
        self.dev, self.shadow, self.hidden = (
            items("micro_dev_v2"), items("micro_shadow_v2"), items("micro_hidden_v2"))
        if not self.dev:
            self.skipTest("lab v2 not built")

    def test_the_three_splits_share_no_base_state(self) -> None:
        dev = {i.base_transition_id for i in self.dev}
        shadow = {i.base_transition_id for i in self.shadow}
        hidden = {i.base_transition_id for i in self.hidden}
        self.assertEqual(dev & shadow, set())
        self.assertEqual(dev & hidden, set())
        self.assertEqual(shadow & hidden, set())

    def test_the_shipped_firewall_registry_is_disjoint_and_retires_v1(self) -> None:
        firewall = SplitFirewall.load(LAB / "firewall.json")
        firewall.assert_disjoint()
        self.assertTrue(firewall.retired, "the spent V1 splits must be recorded as retired")
        self.assertGreater(sum(len(v) for v in firewall.retired.values()), 0)

    def test_no_v1_base_state_reappears_in_v2(self) -> None:
        firewall = SplitFirewall.load(LAB / "firewall.json")
        for item in self.dev + self.shadow + self.hidden:
            record = {"transition_id": item.base_transition_id,
                      "source_specific_reference": item.source_file, "provenance": {}}
            self.assertIsNone(firewall.is_retired(record), item.item_id)

    def test_every_item_carries_a_real_answer_among_its_options(self) -> None:
        for item in self.dev + self.shadow + self.hidden:
            self.assertIn(item.answer, item.options, item.item_id)
            self.assertGreaterEqual(len(item.options), IV2.MINIMUM_OPTIONS, item.item_id)
            self.assertEqual(len(set(item.options)), len(item.options), item.item_id)

    def test_every_ablation_actually_changed_the_state(self) -> None:
        # A negative arm built on an unchanged state would score like the positive one and
        # invalidate its own instrument -- silently.
        for item in self.dev:
            self.assertTrue(ablate.changed(item.state, item.ablated), item.item_id)

    def test_the_option_set_alone_does_not_identify_the_answer(self) -> None:
        for item in self.dev + self.shadow + self.hidden:
            self.assertFalse(
                anonymise.leaks_answer(list(item.options), item.answer), item.item_id)

    def test_identifiers_are_anonymous_where_the_instrument_requires_it(self) -> None:
        for item in self.dev:
            if item.stress not in (S.TYPE, S.PREMISE):
                continue
            blob = json.dumps(item.state)
            for option in item.options:
                self.assertRegex(option, r"^[a-z]+\d+$",
                                 f"{item.item_id}: {option} is not an opaque tag")
            self.assertNotIn("user_name_diagnostic\": \"\\u03b1", blob)


class AnonymiserTests(unittest.TestCase):
    def test_renaming_is_a_bijection_that_moves_every_use_site(self) -> None:
        record = {
            "transition_id": "t", "state_before": {"goals": [{
                "identity": "g", "local_context": [
                    {"identity": "f0", "user_name_diagnostic": "n", "type": {
                        "node": "symbol", "identity": "Nat"}},
                    {"identity": "f1", "user_name_diagnostic": "h", "type": {
                        "node": "local_reference", "identity": "f0"}}],
                "target": {"node": "local_reference", "identity": "f0"}}]},
            "state_after": {"goals": []}, "action": {}}
        out, maps = anonymise.apply(record, rename_symbols=True, salt="t")
        decl = maps["declarations"]
        self.assertEqual(len(set(decl.values())), 2, "two declarations must stay distinct")
        goal = out["state_before"]["goals"][0]
        self.assertEqual(goal["target"]["identity"], decl["f0"],
                         "a use site must move with its declaration")
        self.assertEqual(goal["local_context"][1]["type"]["identity"], decl["f0"])
        self.assertNotIn("n", [d["user_name_diagnostic"]
                               for d in goal["local_context"]],
                         "the human diagnostic name is the loudest prior and must go")

    def test_the_type_head_sort_is_tagged_like_any_other_type(self) -> None:
        # Leaving "Sort" alone made it the only non-tag among t-tags, which is a shortcut.
        tags = anonymise.symbol_tags({"goals": []}, salt="s")
        self.assertTrue(tags.get("Sort", "").startswith(anonymise.TYPE_PREFIX))

    def test_tagging_terminates_on_a_population_larger_than_the_tag_space(self) -> None:
        used: set[str] = set()
        tags = [anonymise._tag(f"n{i}", "s", "p", used, 500) for i in range(500)]
        self.assertEqual(len(set(tags)), 500)


class AblationTests(unittest.TestCase):
    def _state(self) -> dict:
        return {"transition_id": "t", "state_before": {"goals": [{
            "identity": "g0",
            "local_context": [
                {"identity": "a", "type": {"node": "symbol", "identity": "T1"}},
                {"identity": "b", "type": {"node": "symbol", "identity": "T2"}}],
            "target": {"node": "application",
                       "function": {"node": "local_reference", "identity": "a"},
                       "argument": {"node": "local_reference", "identity": "b"}}},
            {"identity": "g1", "local_context": [
                {"identity": "c", "type": {"node": "symbol", "identity": "T3"}}],
             "target": {"node": "symbol", "identity": "T3"}}]},
            "state_after": {"goals": []},
            "action": {"external_premise_refs": ["P1"], "local_context_refs": [
                {"canonical_id": "f::0:before:local:a", "resolved": True}]}}

    def test_type_ablation_permutes_types_and_keeps_every_declaration(self) -> None:
        before = self._state()
        after = ablate.type_relation(before, 1)
        context = after["state_before"]["goals"][0]["local_context"]
        self.assertEqual([d["identity"] for d in context], ["a", "b"])
        self.assertNotEqual(context[0]["type"]["identity"], "T1",
                            "the term-to-type association must actually be destroyed")
        self.assertEqual({d["type"]["identity"] for d in context}, {"T1", "T2"},
                         "the multiset of types must be preserved")

    def test_scope_ablation_moves_declarations_between_goals(self) -> None:
        after = ablate.scope_relation(self._state(), 1)
        goals = after["state_before"]["goals"]
        self.assertNotEqual([d["identity"] for d in goals[0]["local_context"]], ["a", "b"])

    def test_every_ablation_reports_a_real_change_or_refuses(self) -> None:
        base = self._state()
        for stress in S.STRESSES:
            try:
                after = ablate.ablate(stress, base, 3)
            except ablate.AblationFailed:
                continue
            self.assertTrue(ablate.changed(base, after), stress)

    def test_an_ablation_that_cannot_run_refuses_rather_than_returning_the_input(self) -> None:
        thin = {"transition_id": "t", "state_before": {"goals": [
            {"identity": "g", "local_context": [], "target": {"node": "symbol",
                                                              "identity": "T"}}]},
            "state_after": {"goals": []}, "action": {}}
        for stress in S.STRESSES:
            with self.assertRaises(ablate.AblationFailed, msg=stress):
                ablate.ablate(stress, thin, 1)


class CalibrationRuleTests(unittest.TestCase):
    """`D-023` / `MISSION §8`: the rule is fixed, and it accounts for uncertainty."""

    def test_clopper_pearson_brackets_the_point_estimate(self) -> None:
        for successes, trials in ((0, 12), (6, 12), (12, 12), (20, 24)):
            low, high = C.clopper_pearson(successes, trials)
            self.assertLessEqual(low, successes / trials)
            self.assertGreaterEqual(high, successes / trials)

    def test_the_v1_arms_reproduce_their_v1_verdicts_under_the_v2_rule(self) -> None:
        measured = {"DEPENDENCY": (19, 19), "SCOPE": (20, 19), "TYPE": (20, 20),
                    "PREMISE": (21, 21)}
        for name, (positive, negative) in measured.items():
            verdict = C.classify_instrument(
                C.ArmResult("p", positive, 24), C.ArmResult("n", negative, 24), 0.5)
            self.assertEqual(verdict.status, C.INSTRUMENT_INVALID, name)

    def test_a_valid_instrument_needs_a_positive_above_and_a_negative_at_chance(self) -> None:
        verdict = C.classify_instrument(
            C.ArmResult("p", 23, 24), C.ArmResult("n", 12, 24), 0.5)
        self.assertEqual(verdict.status, C.INSTRUMENT_VALID)

    def test_an_unseparated_positive_escalates_rather_than_condemning(self) -> None:
        # BINDER at 0.667 on 24 items: above chance by eye, not by interval. Calling that an
        # INSTRUMENT_LIMIT would blame the reader for a sample size.
        verdict = C.classify_instrument(
            C.ArmResult("p", 16, 24), C.ArmResult("n", 12, 24), 0.5)
        self.assertEqual(verdict.status, C.INSTRUMENT_UNDECIDED)
        self.assertFalse(verdict.decisive)

    def test_the_paired_comparison_is_deterministic(self) -> None:
        left = [True, False, True, True, False, True]
        right = [False, False, True, False, False, True]
        first = C.paired_bootstrap(left, right)
        self.assertEqual(first, C.paired_bootstrap(left, right))
        self.assertAlmostEqual(first["difference"], 2 / 6)

    def test_normalised_readability_refuses_a_range_too_small_to_carry_it(self) -> None:
        self.assertIsNone(C.normalised_readability(0.6, 0.7, 0.6))
        self.assertAlmostEqual(C.normalised_readability(0.6, 1.0, 0.2), 0.5)


class ShortcutAuditTests(unittest.TestCase):
    """`D-024`: the guard that runs before inference, and the two bugs it shipped with."""

    class Item:
        def __init__(self, options, answer, stress="X"):
            self.options, self.answer, self.stress = tuple(options), answer, stress

        @property
        def chance(self):
            return 1.0 / len(self.options)

    def test_a_constant_answer_is_caught_regardless_of_any_rule(self) -> None:
        # The first V2 build: 43 MULTI_GOAL items, answer "g1" on every one.
        items = [self.Item(("g1", "g2", "g3"), "g1") for _ in range(43)]
        report = SC.audit(items)
        self.assertEqual(report["status"], "CONSTANT_ANSWER")
        self.assertEqual(report["most_common_answer_share"], 1.0)
        self.assertGreater(report["most_common_answer_lower_bound"], report["chance"])

    def test_the_rules_read_the_presented_order_not_a_sorted_copy(self) -> None:
        # FM-046: the answer is alphabetically last but sits first on the page. An audit
        # that re-sorts sees a leak that no reader could ever exploit.
        items = [self.Item(("z", "a", "b", "c"), "z") for _ in range(24)]
        report = SC.audit(items)
        self.assertEqual(report["scores"]["always_first_option"], 1.0)
        self.assertEqual(report["scores"]["always_last_option"], 0.0)

    def test_a_small_sample_is_not_condemned_for_ordinary_noise(self) -> None:
        # 16 items, chance 0.25, best rule at 0.375 -- ordinary noise, not a leak.
        items = ([self.Item(("a", "b", "c", "d"), "a") for _ in range(6)]
                 + [self.Item(("a", "b", "c", "d"), "b") for _ in range(4)]
                 + [self.Item(("a", "b", "c", "d"), "c") for _ in range(3)]
                 + [self.Item(("a", "b", "c", "d"), "d") for _ in range(3)])
        self.assertEqual(SC.audit(items)["status"], "CLEAN")

    def test_the_constant_answer_measure_does_not_punish_a_small_vocabulary(self) -> None:
        # A cell whose options come from four labels can never have more than four distinct
        # answers. Scoring distinct-over-total condemned every such cell at scale.
        balanced = [self.Item(("a", "b", "c", "d"), x) for x in ["a", "b", "c", "d"] * 25]
        self.assertEqual(SC.audit(balanced)["status"], "CLEAN")
        self.assertLess(SC.audit(balanced)["answer_entropy"], 0.05)

    def test_a_real_positional_leak_is_still_caught_at_scale(self) -> None:
        items = [self.Item(("a", "b", "c", "d"), "a") for _ in range(80)]
        self.assertIn(SC.audit(items)["status"], ("LEAKS", "CONSTANT_ANSWER"))

    def test_the_key_aware_rule_is_reported_but_carries_no_verdict(self) -> None:
        items = ([self.Item(("a", "b", "c", "d"), "a") for _ in range(10)]
                 + [self.Item(("a", "b", "c", "d"), "b") for _ in range(5)]
                 + [self.Item(("a", "b", "c", "d"), "c") for _ in range(5)]
                 + [self.Item(("a", "b", "c", "d"), "d") for _ in range(5)])
        report = SC.audit(items)
        self.assertIn("key_aware_most_common_answer", report)
        self.assertNotIn("key_aware", report["reason"])

    def test_the_shipped_dev_split_passes_or_is_gated(self) -> None:
        dev = items("micro_dev_v2")
        if not dev:
            self.skipTest("lab v2 not built")
        report = SC.audit_by_stress(dev)
        # SCOPE is known to be underpowered by the corpus and is gated out of certification
        # rather than silently scored; nothing else may fail.
        self.assertLessEqual(set(SC.failing(report)), {S.SCOPE},
                             f"unexpected leaky cells: {SC.failing(report)}")


class WellPosednessTests(unittest.TestCase):
    """`FM-047`: a question with no single defensible answer passes calibration."""

    def test_expression_depth_requires_a_strictly_unique_deepest_reference(self) -> None:
        dev = items("micro_dev_v2")
        if not dev:
            self.skipTest("lab v2 not built")
        for item in dev:
            if item.stress != S.EXPRESSION_DEPTH:
                continue
            self.assertGreaterEqual(item.detail["lead"], IV2.DEPTH_MARGIN, item.item_id)
            self.assertGreater(item.detail["depth"], item.detail["runner_up_depth"],
                               f"{item.item_id}: 'deepest' must name exactly one declaration")

    def test_a_tied_deepest_reference_refuses_to_build(self) -> None:
        tied = {"transition_id": "t", "state_before": {"goals": [{
            "identity": "g", "local_context": [
                {"identity": "a", "type": {"node": "symbol", "identity": "T"}},
                {"identity": "b", "type": {"node": "symbol", "identity": "T"}}],
            # Both references sit at the same depth, so "deepest" has two answers.
            "target": {"node": "application",
                       "function": {"node": "local_reference", "identity": "a"},
                       "argument": {"node": "local_reference", "identity": "b"}}}]},
            "state_after": {"goals": []}, "action": {}}
        with self.assertRaises(IV2.NotEligible):
            IV2.build(tied, S.EXPRESSION_DEPTH, "MIXED")

    def test_every_option_is_a_declaration_the_target_actually_references(self) -> None:
        # Distractors drawn from outside the target would let a reader answer by spotting
        # the one that appears at all, which is not the depth relation.
        dev = items("micro_dev_v2")
        if not dev:
            self.skipTest("lab v2 not built")
        for item in dev:
            if item.stress != S.EXPRESSION_DEPTH:
                continue
            referenced = {identity for _p, identity in S.local_references(
                item.state["state_before"]["goals"][0].get("target"))}
            for option in item.options:
                self.assertIn(option, referenced, item.item_id)


class LadderTests(unittest.TestCase):
    """`MISSION §15`, `§16`."""

    def test_the_preregistered_boundaries_are_not_re_cut_after_seeing_the_data(self) -> None:
        self.assertIs(L.PREREGISTERED_LADDERS, L.LADDERS)
        self.assertEqual([label for label, _l, _h in L.LADDERS[S.EXPRESSION_DEPTH]],
                         ["E1", "E2", "E3", "E4", "E5"])

    def test_the_lead_ladder_stratifies_the_real_difficulty_axis(self) -> None:
        # FM-047: absolute depth was not the difficulty axis; how far the deepest reference
        # leads the runner-up is. 35 of 45 dev items lead by exactly one level.
        dev = [i for i in items("micro_dev_v2") if i.stress == S.EXPRESSION_DEPTH]
        if not dev:
            self.skipTest("lab v2 not built")
        leads = [i.detail["lead"] for i in dev]
        self.assertTrue(all(lead >= 1 for lead in leads))
        self.assertEqual([label for label, _l, _h in L.LEAD_LADDER],
                         ["L1", "L2", "L3", "L4"])

    def test_the_adapted_ladder_is_labelled_as_secondary(self) -> None:
        for ladder in L.ADAPTED_LADDERS.values():
            for label, _low, _high in ladder:
                self.assertIn("*", label, "post-hoc rungs must be visibly distinguishable")

    def test_a_flat_profile_reads_as_refutation_not_as_absence(self) -> None:
        flat = {"E1": 0.5, "E2": 0.5, "E3": 0.5, "E4": 0.5}
        result = L.interaction(flat, flat, S.EXPRESSION_DEPTH)
        self.assertEqual(result["verdict"], "FLAT_NO_HORIZON_INTERACTION")

    def test_a_widening_gap_is_reported_as_the_horizon_prediction(self) -> None:
        candidate = {"E1": 0.50, "E2": 0.58, "E3": 0.70, "E4": 0.82}
        control = {"E1": 0.50, "E2": 0.50, "E3": 0.50, "E4": 0.50}
        result = L.interaction(candidate, control, S.EXPRESSION_DEPTH)
        self.assertEqual(result["verdict"], "WIDENS_WITH_COMPLEXITY")

    def test_too_few_rungs_refuses_to_call_a_slope(self) -> None:
        result = L.interaction({"E1": 0.5, "E2": 0.9}, {"E1": 0.5, "E2": 0.5},
                               S.EXPRESSION_DEPTH)
        self.assertEqual(result["verdict"], "INSUFFICIENT_RUNGS")


class WithdrawnComponentTests(unittest.TestCase):
    """`FM-044`: MULTI_GOAL is withdrawn, and the reason is recorded in code."""

    def test_multi_goal_refuses_to_build_and_says_why(self) -> None:
        with self.assertRaises(IV2.NotEligible) as caught:
            IV2.BUILDERS[S.MULTI_GOAL]({}, 1)
        self.assertIn("RELATION_NOT_PROJECTED", str(caught.exception))

    def test_the_shipped_lab_contains_no_multi_goal_items(self) -> None:
        for name in ("micro_dev_v2", "micro_shadow_v2", "micro_hidden_v2"):
            self.assertEqual([i for i in items(name) if i.stress == S.MULTI_GOAL], [])


class ArchitectureTests(unittest.TestCase):
    """`MISSION §13`, `§14`, `§27`."""

    def test_every_architecture_names_a_hypothesis_and_a_falsifier(self) -> None:
        for architecture in MULTI_GOAL_ARCHITECTURES + EXPRESSION_ARCHITECTURES:
            self.assertTrue(architecture.hypothesis.strip(), architecture.label)
            self.assertTrue(architecture.falsifier.strip(), architecture.label)
            self.assertTrue(architecture.prediction.strip(), architecture.label)
            self.assertTrue(architecture.axes, architecture.label)

    def test_at_least_three_architectures_per_valid_component(self) -> None:
        self.assertGreaterEqual(len(MULTI_GOAL_ARCHITECTURES), 3)
        self.assertGreaterEqual(len(EXPRESSION_ARCHITECTURES), 3)

    def test_every_architecture_realises_with_no_dropped_axis_value(self) -> None:
        for architecture in MULTI_GOAL_ARCHITECTURES + EXPRESSION_ARCHITECTURES:
            _compiler, applied, dropped = realise(architecture)
            self.assertEqual(dropped, {}, f"{architecture.label} names a value that is gone")
            self.assertEqual(set(applied), set(architecture.axes), architecture.label)

    def test_architectures_are_not_cosmetic_restyling(self) -> None:
        # The five properly tested V1 mutations moved 0.031 between them. An architecture
        # that only touches the same grammar axes would be that experiment again.
        cosmetic = {"block_delimiter", "field_marker", "identity_sigil", "record_separator",
                    "list_syntax", "keyword_case", "role_word_length"}
        for architecture in MULTI_GOAL_ARCHITECTURES + EXPRESSION_ARCHITECTURES:
            self.assertTrue(set(architecture.axes) - cosmetic, architecture.label)

    def test_every_stress_has_a_known_bad_representation_to_detect(self) -> None:
        for stress in S.STRESSES:
            self.assertIn(stress, DETECTS, stress)
            self.assertIn(DETECTS[stress], KNOWN_BAD, stress)

    def test_every_known_bad_realises_fully(self) -> None:
        for label in KNOWN_BAD:
            _compiler, axes = realise_known_bad(label)
            self.assertEqual(set(axes), set(KNOWN_BAD[label]), label)


if __name__ == "__main__":
    unittest.main()
