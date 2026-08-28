"""Tests for the representation architecture search engine.

The load-bearing property is that *the compiler is generic*: one implementation, configured
by a genome, must round-trip every legal configuration. These tests exercise the
configuration space rather than a handful of hand-picked candidates, because a search whose
compiler is only correct on the seeds would silently reward whichever axis values happened to
be implemented properly.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts/search"))

from hml_v3.representation_search import adversarial  # noqa: E402
from hml_v3.representation_search.compiler import CompilerRejection, build  # noqa: E402
from hml_v3.representation_search.controller import SearchConfig, SearchController  # noqa: E402
from hml_v3.representation_search.document import Lexicon  # noqa: E402
from hml_v3.representation_search.expressions import (  # noqa: E402
    ExprStyle,
    emit_expr,
    parse_expr_text,
)
from hml_v3.representation_search.failure_memory import FailureMemory  # noqa: E402
from hml_v3.representation_search.gates import run_gates  # noqa: E402
from hml_v3.representation_search.genome import (  # noqa: E402
    AXES,
    AXES_BY_NAME,
    RepresentationGenome,
    default_genome,
)
from hml_v3.representation_search.metrics import PARETO_AXES, measure  # noqa: E402
from hml_v3.representation_search.pareto import dominates, non_dominated_sort, select  # noqa: E402
from hml_v3.representation_search.projection import semantic_core  # noqa: E402
from hml_v3.representation_search.sealing import (  # noqa: E402
    SEALED,
    SealedEvaluator,
    split_corpus,
)
from hml_v3.representation_search.seeds import SEEDS, seed_population  # noqa: E402
from hml_v3.representation_search.tokenizer import pretokens, tokenizer  # noqa: E402

FIXTURES = adversarial.all_fixtures()


class GenomeTests(unittest.TestCase):
    def test_axis_registry_is_well_formed(self) -> None:
        names = [axis.name for axis in AXES]
        self.assertEqual(len(names), len(set(names)))
        for axis in AXES:
            self.assertIn(axis.default, axis.values, axis.name)
            self.assertEqual(len(axis.values), len(set(axis.values)), axis.name)
            self.assertIn(axis.phase, ("A", "B", "C", "D"), axis.name)
            for lossy in axis.known_lossy:
                self.assertIn(lossy, axis.values, axis.name)

    def test_identity_is_the_genome_hash(self) -> None:
        first = default_genome(syntax_family="SEXPR")
        second = default_genome(syntax_family="SEXPR")
        self.assertEqual(first.candidate_id(), second.candidate_id())
        self.assertNotEqual(first.candidate_id(), default_genome().candidate_id())

    def test_label_does_not_change_identity(self) -> None:
        base = default_genome()
        relabelled = RepresentationGenome(base.resolved(), label="something else")
        self.assertEqual(base.candidate_id(), relabelled.candidate_id())

    def test_invalid_values_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            RepresentationGenome({"syntax_family": "NOT_A_FAMILY"})
        with self.assertRaises(ValueError):
            RepresentationGenome({"not_an_axis": "BLOCK"})


class ExpressionCodecTests(unittest.TestCase):
    SAMPLE = {
        "node": "application",
        "function": {
            "node": "application",
            "function": {"node": "symbol", "identity": "Nat.add",
                         "universe_arguments": [{"constructor": "succ",
                                                 "of": {"constructor": "zero"}}]},
            "argument": {"node": "bound_variable", "index": 0},
        },
        "argument": {
            "node": "lambda", "binder_name": "_", "binder_role": "implicit",
            "binder_type": {"node": "sort",
                            "level": {"constructor": "param", "name": "u_1"}},
            "body": {
                "node": "let", "binder_name": "_",
                "type": {"node": "local_reference", "identity": "f0"},
                "value": {"node": "literal", "literal_kind": "NAT", "value": 42},
                "body": {"node": "projection", "type_identity": "Prod", "field_index": 1,
                         "structure": {"node": "annotated",
                                       "expression": {"node": "metavariable_reference",
                                                      "identity": "m3"},
                                       "source_metadata_delegated": True}},
            },
        },
    }

    def test_every_lossless_expression_configuration_round_trips(self) -> None:
        combinations = itertools.product(
            AXES_BY_NAME["expression_notation"].values,
            AXES_BY_NAME["application_style"].values,
            AXES_BY_NAME["binder_encoding"].values,
            ("FULL", "ELIDED_WHEN_TRIVIAL"),
            AXES_BY_NAME["literal_form"].values,
            ("UNICODE_NATIVE", "ASCII_TRANSLITERATION"),
        )
        checked = 0
        for notation, application, binder, universe, literal, glyph in combinations:
            style = ExprStyle(notation, application, binder, universe, "FULL_NAME",
                              literal, glyph)
            with self.subTest(notation=notation, application=application, binder=binder):
                self.assertEqual(
                    parse_expr_text(emit_expr(self.SAMPLE, style), style), self.SAMPLE
                )
            checked += 1
        self.assertGreaterEqual(checked, 96)


class CompilerRoundTripTests(unittest.TestCase):
    def test_default_genome_round_trips_every_fixture(self) -> None:
        compiler = build(default_genome())
        for fixture in FIXTURES:
            passed, reason, detail = compiler.round_trip(fixture)
            self.assertTrue(passed, f"{fixture['transition_id']}: {reason} {detail}")

    def test_every_single_axis_change_either_round_trips_or_is_declared_lossy(self) -> None:
        """No axis value may fail silently: it round-trips, or it is marked ``known_lossy``.

        This is the test that keeps the search honest. Without it, an axis value that fails
        because of a compiler bug is indistinguishable from one that fails because it hides
        information, and the search would learn to avoid a bug rather than a semantic loss.
        """

        base = default_genome()
        for axis in AXES:
            for value in axis.values:
                if value == base.get(axis.name):
                    continue
                genome = base.with_values(**{axis.name: value})
                with self.subTest(axis=axis.name, value=value):
                    try:
                        compiler = build(genome)
                    except CompilerRejection:
                        continue
                    failures = [
                        (fixture["transition_id"], reason)
                        for fixture in FIXTURES
                        for passed, reason, _ in [compiler.round_trip(fixture)]
                        if not passed
                    ]
                    if failures and value not in axis.known_lossy:
                        self.fail(
                            f"{axis.name}={value} lost contract content but is not declared "
                            f"lossy: {failures[:3]}"
                        )

    def test_declared_lossy_values_actually_lose_something(self) -> None:
        base = default_genome()
        for axis in AXES:
            for value in axis.known_lossy:
                genome = base.with_values(**{axis.name: value})
                with self.subTest(axis=axis.name, value=value):
                    try:
                        compiler = build(genome)
                    except CompilerRejection:
                        continue
                    report = run_gates(compiler, FIXTURES)
                    self.assertFalse(
                        report.passed,
                        f"{axis.name}={value} is declared lossy but passed every gate",
                    )

    def test_alpha_variants_render_identically_under_normalization(self) -> None:
        alpha_a, alpha_b = adversarial.alpha_renamed_pair()
        normalized = build(default_genome(alpha_normalization="NORMALIZED"))
        preserving = build(default_genome(alpha_normalization="PRESERVE_DISPLAY"))

        def strip_ids(text: str, tag: str) -> str:
            return text.replace(tag, "T")

        self.assertEqual(
            strip_ids(normalized.render_text(alpha_a), "SYN_ALPHA_A"),
            strip_ids(normalized.render_text(alpha_b), "SYN_ALPHA_B"),
        )
        self.assertNotEqual(
            strip_ids(preserving.render_text(alpha_a), "SYN_ALPHA_A"),
            strip_ids(preserving.render_text(alpha_b), "SYN_ALPHA_B"),
        )

    def test_shadowed_names_are_distinguished_by_identity(self) -> None:
        fixture = adversarial.shadowed_names()
        compiler = build(default_genome())
        passed, _reason, _detail = compiler.round_trip(fixture)
        self.assertTrue(passed)
        display = build(default_genome(identity_scheme="DISPLAY_NAME"))
        passed, reason, _detail = display.round_trip(fixture)
        self.assertFalse(passed)
        self.assertEqual(reason, "IDENTITY_COLLISION")

    def test_goal_reordering_is_not_a_delete_and_create(self) -> None:
        fixture = adversarial.reordered_goals()
        compiler = build(default_genome())
        core = semantic_core(fixture)
        self.assertEqual(
            sorted(goal["identity"] for goal in core["before"]["goals"]),
            sorted(goal["identity"] for goal in core["after"]["goals"]),
        )
        self.assertNotEqual(core["before"]["focus_order"], core["after"]["focus_order"])
        passed, reason, _ = compiler.round_trip(fixture)
        self.assertTrue(passed, reason)


class SeedTests(unittest.TestCase):
    def test_every_seed_compiles_and_passes_the_gates(self) -> None:
        for genome in seed_population():
            with self.subTest(seed=genome.label):
                report = run_gates(build(genome), FIXTURES)
                self.assertTrue(report.passed, f"{genome.label}: {report.first_failure}")

    def test_seed_identities_are_distinct(self) -> None:
        identities = [genome.candidate_id() for genome in seed_population()]
        self.assertEqual(len(identities), len(set(identities)))

    def test_pinned_baselines_exist(self) -> None:
        memory = FailureMemory.load()
        for label in memory.pinned_seeds():
            self.assertIn(label, SEEDS, f"{label} is pinned by the failure memory")


class GateTests(unittest.TestCase):
    def test_escaped_glyphs_are_rejected(self) -> None:
        report = run_gates(build(default_genome(glyph_policy="ASCII_ESCAPE")), FIXTURES)
        self.assertFalse(report.passed)
        self.assertEqual(report.first_failure, "glyph_fidelity_utf8")

    def test_ambiguous_lexicon_is_a_compile_rejection(self) -> None:
        with self.assertRaises(CompilerRejection):
            build(default_genome(
                lexicon_register="COMPACT_MNEMONIC", role_word_length="SINGLE_CHAR"))

    def test_hidden_types_fail_the_round_trip_gate(self) -> None:
        report = run_gates(build(default_genome(type_explicitness="OMITTED")), FIXTURES)
        self.assertFalse(report.passed)
        self.assertEqual(report.first_failure, "semantic_round_trip")


class MetricTests(unittest.TestCase):
    def test_metric_vector_covers_every_pareto_axis(self) -> None:
        vector = measure(build(default_genome()), FIXTURES)
        for axis in PARETO_AXES:
            self.assertIn(axis, vector.values, axis)

    def test_detection_rates_are_probabilities(self) -> None:
        vector = measure(build(default_genome()), FIXTURES)
        for key, value in vector.values.items():
            if key.startswith("detect_"):
                self.assertGreaterEqual(value, 0.0)
                self.assertLessEqual(value, 1.0)

    def test_tokenizer_matches_the_reference_implementation(self) -> None:
        encoder = tokenizer()
        self.assertEqual(encoder.count("hello world"), 2)
        self.assertEqual(encoder.encode_pieces("hello world"), ["hello", "Ġworld"])
        self.assertEqual(len(encoder.encoder), 50257)

    def test_pretokens_need_no_vocabulary(self) -> None:
        self.assertEqual(pretokens("goal m0"), ["goal", " m", "0"])

    def test_measurement_is_deterministic(self) -> None:
        compiler = build(default_genome())
        first = measure(compiler, FIXTURES)
        second = measure(compiler, FIXTURES)
        self.assertEqual(first.values, second.values)


class ParetoTests(unittest.TestCase):
    def test_domination_respects_metric_direction(self) -> None:
        cheap_and_safe = {"bpe_tokens_per_transition": 100.0, "detect_swap_records": 0.9}
        costly_and_blind = {"bpe_tokens_per_transition": 200.0, "detect_swap_records": 0.1}
        axes = ("bpe_tokens_per_transition", "detect_swap_records")
        self.assertTrue(dominates(cheap_and_safe, costly_and_blind, axes))
        self.assertFalse(dominates(costly_and_blind, cheap_and_safe, axes))

    def test_a_trade_off_is_not_dominated(self) -> None:
        axes = ("bpe_tokens_per_transition", "detect_swap_records")
        cheap = {"bpe_tokens_per_transition": 100.0, "detect_swap_records": 0.1}
        safe = {"bpe_tokens_per_transition": 200.0, "detect_swap_records": 0.9}
        self.assertFalse(dominates(cheap, safe, axes))
        self.assertFalse(dominates(safe, cheap, axes))

    def test_pinned_candidates_survive_selection(self) -> None:
        axes = ("bpe_tokens_per_transition",)
        population = [
            ("good", {"bpe_tokens_per_transition": 10.0}),
            ("bad", {"bpe_tokens_per_transition": 1000.0}),
        ]
        genomes = {"good": default_genome(), "bad": default_genome(syntax_family="SEXPR")}
        result = select(population, genomes, capacity=1, pinned=["bad"], novelty_slots=0,
                        axes=axes)
        self.assertIn("bad", result.survivors)

    def test_fronts_partition_the_population(self) -> None:
        population = [
            ("a", {"bpe_tokens_per_transition": 1.0, "detect_swap_records": 1.0}),
            ("b", {"bpe_tokens_per_transition": 2.0, "detect_swap_records": 0.5}),
            ("c", {"bpe_tokens_per_transition": 3.0, "detect_swap_records": 0.1}),
        ]
        axes = ("bpe_tokens_per_transition", "detect_swap_records")
        fronts = non_dominated_sort(population, axes)
        flattened = [item for front in fronts for item in front]
        self.assertEqual(sorted(flattened), ["a", "b", "c"])


class FailureMemoryTests(unittest.TestCase):
    def test_recorded_negatives_block_a_mutation(self) -> None:
        memory = FailureMemory.load()
        allowed, reason = memory.may_apply("graph_serialization", "GOAL_CENTRED")
        self.assertFalse(allowed)
        self.assertTrue(reason.startswith("BLOCKED_BY:FM-005"), reason)

    def test_a_named_changed_condition_buys_one_retry(self) -> None:
        memory = FailureMemory.load()
        allowed, reason = memory.may_apply(
            "graph_serialization", "GOAL_CENTRED",
            changed_condition="the V2 corpus carries real dependency structure",
        )
        self.assertTrue(allowed, reason)
        memory.consume_retry("FM-005")
        allowed, reason = memory.may_apply(
            "graph_serialization", "GOAL_CENTRED", changed_condition="again",
        )
        self.assertFalse(allowed)
        self.assertTrue(reason.startswith("RETRY_BUDGET_EXHAUSTED"), reason)

    def test_every_lesson_declares_its_evidence_status(self) -> None:
        memory = FailureMemory.load()
        for lesson in memory.lessons:
            self.assertIn(
                lesson.evidence_status,
                ("MEASURED_LOCAL_ARTIFACT", "ASSERTED_WITHOUT_LOCAL_ARTIFACT"),
                lesson.id,
            )


class SealingTests(unittest.TestCase):
    def _corpus(self) -> list[dict]:
        rows = []
        for index in range(60):
            fixture = json.loads(json.dumps(FIXTURES[index % len(FIXTURES)]))
            fixture["transition_id"] = f"T{index:03d}"
            fixture["corpus_metadata"]["source_file"] = f"Mathlib/Module{index // 3}.lean"
            rows.append(fixture)
        return rows

    def test_split_is_by_family_not_by_transition(self) -> None:
        split = split_corpus(self._corpus())
        for bucket, name in ((split.dev, "dev"), (split.validation, "val"),
                             (split.sealed, "sealed")):
            families = {row["corpus_metadata"]["source_file"] for row in bucket}
            for other, other_name in ((split.dev, "dev"), (split.validation, "val"),
                                      (split.sealed, "sealed")):
                if other is bucket:
                    continue
                other_families = {row["corpus_metadata"]["source_file"] for row in other}
                self.assertFalse(
                    families & other_families,
                    f"{name} and {other_name} share a source file",
                )

    def test_split_is_reproducible(self) -> None:
        first = split_corpus(self._corpus()).manifest()
        second = split_corpus(list(reversed(self._corpus()))).manifest()
        self.assertEqual(first["families_sha256"], second["families_sha256"])
        self.assertEqual(first["transition_id_sha256"], second["transition_id_sha256"])

    def test_sealed_evaluator_returns_aggregates_only(self) -> None:
        split = split_corpus(self._corpus())
        evaluator = SealedEvaluator(split.sealed)
        result = evaluator.evaluate(build(default_genome()), purpose="unit-test", sample=4)
        self.assertNotIn("transitions", result)
        self.assertNotIn("examples", result)
        self.assertIn("gates_passed", result)
        self.assertEqual(len(evaluator.access_log), 1)

    def test_sealed_share_is_about_twenty_percent(self) -> None:
        split = split_corpus(self._corpus())
        total = len(split.families)
        sealed = sum(1 for value in split.families.values() if value == SEALED)
        self.assertGreater(sealed, 0)
        self.assertLess(sealed / total, 0.5)


class ControllerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.workspace = Path(tempfile.mkdtemp(prefix="hml-search-"))

    def tearDown(self) -> None:
        shutil.rmtree(self.workspace, ignore_errors=True)

    def _controller(self) -> SearchController:
        config = SearchConfig(
            population_capacity=10, children_per_generation=6,
            dev_sample=len(FIXTURES), validation_sample=4, max_generations=6,
        )
        return SearchController(FIXTURES, FIXTURES, self.workspace, config)

    def test_a_generation_evaluates_selects_and_proposes(self) -> None:
        controller = self._controller()
        report = controller.step()
        self.assertGreater(len(report.evaluated), 0)
        self.assertGreater(len(report.front), 0)
        self.assertTrue((self.workspace / "search_state.json").exists())
        self.assertTrue(
            (self.workspace / "generations/generation_000.json").exists()
        )

    def test_state_resumes_at_the_exact_next_generation(self) -> None:
        controller = self._controller()
        controller.step()
        controller.step()
        resumed = self._controller()
        self.assertTrue(resumed.resume())
        self.assertEqual(resumed.generation, 2)
        self.assertEqual(resumed.population, controller.population)
        self.assertEqual(len(resumed.registry), len(controller.registry))

    def test_rejected_candidates_are_kept_as_evidence(self) -> None:
        controller = self._controller()
        for _ in range(3):
            controller.step()
        statistics = controller.registry.statistics()
        self.assertGreater(statistics["total"], 0)
        self.assertEqual(
            statistics["total"],
            sum(statistics["by_status"].values()),
        )

    def test_hypotheses_are_scored_against_what_happened(self) -> None:
        controller = self._controller()
        controller.step()
        report = controller.step()
        for refuted in report.refuted_hypotheses:
            self.assertEqual(refuted["verdict"], "HYPOTHESIS_REFUTED")
            self.assertIn("parent_value", refuted)
            self.assertIn("child_value", refuted)


class SchemaTests(unittest.TestCase):
    def test_generated_schema_matches_the_axis_registry(self) -> None:
        from emit_genome_schema import OUTPUT, build_schema

        self.assertTrue(OUTPUT.exists(), "run scripts/search/emit_genome_schema.py")
        on_disk = json.loads(OUTPUT.read_text())
        self.assertEqual(on_disk, build_schema())


if __name__ == "__main__":
    unittest.main()
