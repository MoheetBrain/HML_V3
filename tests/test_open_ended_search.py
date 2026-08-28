"""Tests for the open-ended search: the parts that let the space grow, safely.

The load-bearing properties are different from V1's. There, the question was whether one
generic compiler round-trips every configuration. Here it is whether a *proposal channel* can
widen the search space without letting anything through that should not get through: a
malformed proposal, a proposal reaching for the semantic substrate, a candidate whose dev-set
gain does not reproduce, or a sealed row leaking into the search process.
"""

from __future__ import annotations

import json
from pathlib import Path
import random
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hml_v3.representation_search import semantic_mutations  # noqa: E402
from hml_v3.representation_search.adversarial import all_fixtures  # noqa: E402
from hml_v3.representation_search.compiler import build  # noqa: E402
from hml_v3.representation_search.corpus import write_corpus  # noqa: E402
from hml_v3.representation_search.genome import AXES, default_genome  # noqa: E402
from hml_v3.representation_search.genome_migrations import (  # noqa: E402
    ExtendedGenome,
    extended_space,
    migrate,
    space_size,
)
from hml_v3.representation_search.meta_designer.base import (  # noqa: E402
    MetaDesignerBackend,
    ScientistReport,
)
from hml_v3.representation_search.meta_designer.deterministic import (  # noqa: E402
    DeterministicMetaDesigner,
)
from hml_v3.representation_search.meta_designer.llm import (  # noqa: E402
    CallableTransport,
    LLMMetaDesigner,
    extract_proposals,
    normalise,
)
from hml_v3.representation_search.meta_designer.schemas import (  # noqa: E402
    ProposalRejected,
    static_safety,
    validate,
)
from hml_v3.representation_search.microtests import SUITES, run_all_suites  # noqa: E402
from hml_v3.representation_search.primitive_registry import (  # noqa: E402
    HOOKS,
    PrimitiveRegistry,
    apply_primitives,
    infer_hook,
)
from hml_v3.representation_search.sealed_service import (  # noqa: E402
    ALLOWED_KEYS,
    SealedEvaluatorClient,
)
from hml_v3.representation_search.seeds import SEEDS  # noqa: E402
from hml_v3.representation_search.tokenizers import (  # noqa: E402
    available_tokenizers,
    ordering_agreement,
)
from hml_v3.representation_search.validation import (  # noqa: E402
    QUARANTINED,
    REPRODUCED,
    Quarantine,
    assess,
)

FIXTURES = all_fixtures()
AXIS_NAMES = {axis.name for axis in AXES}


def _valid_new_axis(name: str = "dependency_capsule") -> dict:
    return {
        "proposal_type": "NEW_PRIMITIVE",
        "name": name,
        "values": ["NONE", "GOAL_LOCAL", "ACTION_LOCAL"],
        "implementation_layer": "projection_only",
        "projection_hook": "neighbourhood_capsule",
        "hypothesis": "co-locating cited declarations next to their goal shortens binder distance",
        "mechanism": "the declarations a goal cites are laid out adjacent to that goal, so the "
                     "binder-to-use span stops scaling with total context size",
        "projection_behaviour": "co-locate the cited declarations into a capsule adjacent to "
                                "the goal record without removing the global context",
        "falsification": "reject if binder distance improves by less than 10%",
        "tests_required": ["semantic_roundtrip"],
    }


class ProposalSchemaTests(unittest.TestCase):
    def test_a_well_formed_new_axis_validates(self) -> None:
        proposal = validate(_valid_new_axis(), "test", 1, AXIS_NAMES)
        self.assertEqual(proposal.proposal_type, "NEW_PRIMITIVE")
        self.assertTrue(proposal.proposal_id.startswith("P_"))

    def test_every_intervention_must_be_falsifiable(self) -> None:
        payload = _valid_new_axis()
        del payload["falsification"]
        with self.assertRaises(ProposalRejected):
            validate(payload, "test", 1, AXIS_NAMES)

    def test_a_new_axis_needs_at_least_two_values(self) -> None:
        payload = _valid_new_axis()
        payload["values"] = ["GOAL_LOCAL"]
        with self.assertRaises(ProposalRejected):
            validate(payload, "test", 1, AXIS_NAMES)

    def test_an_axis_that_already_exists_is_refused(self) -> None:
        payload = _valid_new_axis(name="context_order")
        with self.assertRaises(ProposalRejected):
            validate(payload, "test", 1, AXIS_NAMES)

    def test_a_semantic_layer_change_is_refused(self) -> None:
        payload = _valid_new_axis()
        payload["implementation_layer"] = "canonical_state"
        with self.assertRaises(ProposalRejected):
            validate(payload, "test", 1, AXIS_NAMES)

    def test_malformed_proposals_are_rejected_not_crashed_on(self) -> None:
        for payload in (None, [], "a string", {}, {"proposal_type": "WISH"}):
            with self.subTest(payload=payload):
                with self.assertRaises(ProposalRejected):
                    validate(payload, "test", 1, AXIS_NAMES)  # type: ignore[arg-type]

    def test_static_safety_blocks_reaching_outside_the_representation(self) -> None:
        """A proposal naming the substrate, the sealed split or the host must not run."""

        for blob in (
            {"proposal_type": "NEW_AXIS", "mechanism": "modify the canonical_math_state"},
            {"proposal_type": "NEW_AXIS", "mechanism": "read the sealed split for tuning"},
            {"proposal_type": "NEW_AXIS", "mechanism": "use subprocess to patch the verifier"},
        ):
            with self.subTest(blob=blob):
                self.assertTrue(static_safety(blob))

    def test_safety_passes_an_ordinary_representation_proposal(self) -> None:
        self.assertEqual(static_safety(_valid_new_axis()), [])


class MetaDesignerTests(unittest.TestCase):
    def _report(self) -> ScientistReport:
        return ScientistReport(
            generation=1, phase=None,
            genome_axes={axis.name: list(axis.values) for axis in AXES},
            elites=[{
                "candidate_id": SEEDS["SEED_PRIOR_HML"].candidate_id(),
                "genome": {"context_order": "DEPENDENCY_TOPOLOGICAL"},
                "metrics": {"bpe_tokens_per_transition": 7000.0},
                "weaknesses": ["bpe_tokens_per_transition"],
            }],
            metric_directions={"bpe_tokens_per_transition": "minimise"},
        )

    def test_deterministic_backend_proposes_only_existing_axes(self) -> None:
        batch = DeterministicMetaDesigner(per_elite=3).propose(self._report())
        self.assertTrue(batch.accepted)
        for proposal in batch.accepted:
            if proposal.proposal_type == "AXIS_MUTATION":
                self.assertIn(proposal.payload["axis"], AXIS_NAMES)

    def test_llm_backend_accepts_a_well_formed_batch(self) -> None:
        payload = json.dumps([_valid_new_axis()])
        backend = LLMMetaDesigner(CallableTransport(lambda system, user: payload))
        batch = backend.propose(self._report())
        self.assertEqual(len(batch.accepted), 1)
        self.assertEqual(batch.accepted[0].proposal_type, "NEW_PRIMITIVE")

    def test_llm_backend_survives_garbage_output(self) -> None:
        for text in ("", "I cannot help with that.", "{not json", "null"):
            with self.subTest(text=text):
                backend = LLMMetaDesigner(CallableTransport(lambda s, u, t=text: t))
                batch = backend.propose(self._report())
                self.assertEqual(batch.accepted, [])
                self.assertTrue(batch.rejected)

    def test_llm_backend_survives_a_dead_transport(self) -> None:
        def explode(system: str, user: str) -> str:
            raise ConnectionError("no model here")

        batch = LLMMetaDesigner(CallableTransport(explode)).propose(self._report())
        self.assertEqual(batch.accepted, [])
        self.assertIn("transport unavailable", batch.rejected[0]["reason"])

    def test_a_proposal_reaching_for_the_substrate_is_rejected_by_the_backend(self) -> None:
        payload = _valid_new_axis()
        payload["mechanism"] = "rewrite the canonical_math_state to add the field directly"
        backend = LLMMetaDesigner(
            CallableTransport(lambda s, u: json.dumps([payload])))
        batch = backend.propose(self._report())
        self.assertEqual(batch.accepted, [])
        self.assertIn("static safety", batch.rejected[0]["reason"])

    def test_field_synonyms_are_normalised_and_recorded(self) -> None:
        raw = {"proposal_type": "AXIS_MUTATION", "axis_name": "context_order",
               "axis_value": "REVERSE_INDEX", "hypothesis": "x" * 30,
               "mechanism": "y" * 30, "falsification": "z" * 20}
        fixed = normalise(raw, "R_parent")
        self.assertEqual(fixed["axis"], "context_order")
        self.assertEqual(fixed["value"], "REVERSE_INDEX")
        self.assertEqual(fixed["parent_id"], "R_parent")
        self.assertIn("axis_name->axis", fixed["_normalised"])

    def test_json_is_extracted_from_fenced_output(self) -> None:
        payload = json.dumps([_valid_new_axis()])
        self.assertEqual(len(extract_proposals(f"```json\n{payload}\n```")), 1)
        self.assertEqual(len(extract_proposals(f"Here you go:\n{payload}\nHope that helps")), 1)


class PrimitiveRegistryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = Path(tempfile.mkdtemp(prefix="hml-prim-"))
        self.registry = PrimitiveRegistry(self.directory / "primitive_registry.jsonl")

    def tearDown(self) -> None:
        shutil.rmtree(self.directory, ignore_errors=True)

    def test_an_implementable_axis_is_accepted_and_bumps_the_schema(self) -> None:
        before = self.registry.schema_version
        primitive, reason = self.registry.consider(
            _valid_new_axis(), "P_1", 1, "test", AXIS_NAMES)
        self.assertEqual(reason, "IMPLEMENTABLE")
        self.assertIsNotNone(primitive)
        self.registry.register(primitive)
        self.assertNotEqual(before, self.registry.schema_version)

    def test_an_unimplementable_axis_is_recorded_not_silently_dropped(self) -> None:
        payload = _valid_new_axis(name="vibes_axis")
        payload.pop("projection_hook")
        payload["mechanism"] = "it makes the state feel more natural to read somehow"
        payload["projection_behaviour"] = "the representation becomes generally nicer overall"
        primitive, reason = self.registry.consider(payload, "P_2", 1, "test", AXIS_NAMES)
        self.assertIsNone(primitive)
        self.assertEqual(reason, "NO_EXECUTABLE_HOOK")
        self.assertEqual(len(self.registry.unimplementable), 1)

    def test_every_accepted_axis_gets_an_off_position(self) -> None:
        payload = _valid_new_axis()
        payload["values"] = ["GOAL_LOCAL", "ACTION_LOCAL"]
        primitive, _ = self.registry.consider(payload, "P_3", 1, "test", AXIS_NAMES)
        self.assertIn("NONE", primitive.values)

    def test_an_inert_axis_is_rejected_not_kept(self) -> None:
        """An axis whose values all render identically consumes budget and inflates the space."""

        primitive, _ = self.registry.consider(_valid_new_axis(), "P_9", 1, "t", AXIS_NAMES)
        self.registry.register(primitive)
        genome = default_genome()

        # A factory that ignores the invented axis entirely, so nothing can differ.
        observable, evidence = self.registry.has_observable_effect(
            primitive, lambda invented: build(genome), FIXTURES[:3])
        self.assertFalse(observable)
        self.assertEqual(evidence["distinct_renderings"], 1)

        self.registry.reject_inert(primitive, evidence)
        self.assertNotIn("dependency_capsule", self.registry.primitives)
        self.assertTrue(self.registry.unimplementable)

    def test_an_effective_axis_passes_the_observable_effect_check(self) -> None:
        primitive, _ = self.registry.consider(_valid_new_axis(), "P_10", 1, "t", AXIS_NAMES)
        self.registry.register(primitive)
        genome = default_genome(goal_position="FIRST")
        observable, evidence = self.registry.has_observable_effect(
            primitive,
            lambda invented: build(genome, invented, self.registry),
            FIXTURES[:4],
        )
        self.assertTrue(observable, evidence)
        self.assertGreater(evidence["distinct_renderings"], 1)

    def test_hook_behaviour_is_indexed_by_position_not_by_value_name(self) -> None:
        """An invented axis must work whatever its inventor called the values."""

        from hml_v3.representation_search.primitive_registry import variant

        self.assertEqual(variant("WIDE", ["NONE", "WIDE", "NARROW"]), 0)
        self.assertEqual(variant("NARROW", ["NONE", "WIDE", "NARROW"]), 1)
        self.assertEqual(variant("GOAL_LOCAL", ["NONE", "GOAL_LOCAL", "ACTION_LOCAL"]), 0)

    def test_an_axis_with_unusual_value_names_still_renders_differently(self) -> None:
        payload = _valid_new_axis(name="context_range")
        payload["values"] = ["NONE", "WIDE", "NARROW"]
        primitive, _ = self.registry.consider(payload, "P_11", 1, "t", AXIS_NAMES)
        self.registry.register(primitive)
        genome = default_genome(goal_position="FIRST")
        observable, evidence = self.registry.has_observable_effect(
            primitive,
            lambda invented: build(genome, invented, self.registry),
            FIXTURES[:4],
        )
        self.assertTrue(observable, f"WIDE/NARROW axis was inert: {evidence}")

    def test_registry_round_trips_through_disk(self) -> None:
        primitive, _ = self.registry.consider(_valid_new_axis(), "P_4", 1, "test", AXIS_NAMES)
        self.registry.register(primitive)
        self.registry.flush()
        reloaded = PrimitiveRegistry(self.registry.path)
        self.assertIn("dependency_capsule", reloaded.primitives)
        self.assertEqual(reloaded.primitives["dependency_capsule"].hook,
                         "neighbourhood_capsule")

    def test_hooks_are_inferable_from_behaviour_text(self) -> None:
        self.assertEqual(infer_hook({"mechanism": "co-locate them in a capsule"}),
                         "neighbourhood_capsule")
        self.assertEqual(infer_hook({"mechanism": "restate the type at each use"}),
                         "duplicate_adjacent")
        self.assertIsNone(infer_hook({"mechanism": "make it better"}))

    def test_every_registered_hook_exists(self) -> None:
        for name in HOOKS:
            self.assertTrue(callable(HOOKS[name]))


class GenomeMigrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = Path(tempfile.mkdtemp(prefix="hml-mig-"))
        self.registry = PrimitiveRegistry(self.directory / "primitive_registry.jsonl")
        primitive, _ = self.registry.consider(_valid_new_axis(), "P_1", 1, "t", AXIS_NAMES)
        self.registry.register(primitive)

    def tearDown(self) -> None:
        shutil.rmtree(self.directory, ignore_errors=True)

    def test_the_space_grows(self) -> None:
        space = extended_space(self.registry)
        self.assertEqual(len(space.axes), len(AXES) + 1)
        self.assertGreater(space_size(space), 1)

    def test_an_older_genome_reads_at_the_off_position(self) -> None:
        space = extended_space(self.registry)
        migrated = migrate(default_genome().resolved(), space)
        self.assertEqual(migrated["dependency_capsule"], "NONE")

    def test_a_pre_axis_candidate_renders_identically_after_the_axis_exists(self) -> None:
        """This is what makes cross-generation comparison legitimate."""

        genome = default_genome()
        before = build(genome).render_text(FIXTURES[0])
        after = build(genome, {}, self.registry).render_text(FIXTURES[0])
        self.assertEqual(before, after)

    def test_turning_an_invented_axis_on_changes_the_candidate_id(self) -> None:
        genome = default_genome()
        off = ExtendedGenome(genome, {})
        on = ExtendedGenome(genome, {"dependency_capsule": "GOAL_LOCAL"})
        self.assertNotEqual(off.candidate_id(), on.candidate_id())
        self.assertEqual(off.candidate_id(), genome.candidate_id())

    def test_an_invented_axis_preserves_the_semantic_contract(self) -> None:
        compiler = build(default_genome(goal_position="FIRST"),
                         {"dependency_capsule": "GOAL_LOCAL"}, self.registry)
        for fixture in FIXTURES:
            passed, reason, _ = compiler.round_trip(fixture)
            self.assertTrue(passed, f"{fixture['transition_id']}: {reason}")

    def test_an_invented_axis_actually_changes_the_rendering(self) -> None:
        """An axis that never changes anything is not a discovery, it is decoration."""

        genome = default_genome(goal_position="FIRST")
        off = build(genome, {}, self.registry).render_text(FIXTURES[5])
        on = build(genome, {"dependency_capsule": "GOAL_LOCAL"},
                   self.registry).render_text(FIXTURES[5])
        self.assertNotEqual(off, on)

    def test_apply_primitives_is_a_no_op_when_every_axis_is_off(self) -> None:
        from hml_v3.representation_search.projection import Projection

        document, _ = Projection(default_genome()).to_document(FIXTURES[0])
        self.assertEqual(
            apply_primitives(document, {"dependency_capsule": "NONE"}, self.registry),
            document,
        )


class SemanticMutationTests(unittest.TestCase):
    def test_mutations_are_applied_to_the_state_not_the_text(self) -> None:
        rng = random.Random(1)
        fixture = next(f for f in FIXTURES if f["transition_id"] == "SYN_LONG_DEPENDENCY_CHAIN")
        result = semantic_mutations.apply_mutation(fixture, "DROP_DECLARATION", rng)
        self.assertIsNotNone(result)
        self.assertNotEqual(
            len(result.state["state_before"]["goals"][0]["local_context"]),
            len(fixture["state_before"]["goals"][0]["local_context"]),
        )

    def test_the_original_state_is_never_modified(self) -> None:
        rng = random.Random(1)
        fixture = FIXTURES[5]
        before = json.dumps(fixture, sort_keys=True)
        for family in semantic_mutations.FAMILIES:
            semantic_mutations.apply_mutation(fixture, family, rng)
        self.assertEqual(before, json.dumps(fixture, sort_keys=True))

    def test_every_candidate_sees_the_same_corruption(self) -> None:
        """The point of the redesign: the mutation is upstream of the representation."""

        rng = random.Random(7)
        fixture = next(f for f in FIXTURES if f["transition_id"] == "SYN_LONG_DEPENDENCY_CHAIN")
        result = semantic_mutations.apply_mutation(fixture, "ALTER_BINDER_TARGET", rng)
        self.assertIsNotNone(result)
        for label in ("SEED_PRIOR_HML", "SEED_CANONICAL_SEXPR", "SEED_MINIMAL_MACHINE"):
            compiler = build(SEEDS[label])
            self.assertNotEqual(
                compiler.render_text(fixture),
                compiler.render_text(result.state),
                f"{label} rendered a corrupted state identically to the clean one",
            )

    def test_inapplicability_is_reported_not_hidden(self) -> None:
        single_goal = next(
            f for f in FIXTURES if len(f["state_before"]["goals"]) == 1)
        self.assertIsNone(
            semantic_mutations.apply_mutation(single_goal, "REORDER_GOAL_FOCUS", random.Random(1))
        )

    def test_applicability_report_covers_every_family(self) -> None:
        report = semantic_mutations.applicability(FIXTURES[:6])
        self.assertEqual(set(report), set(semantic_mutations.FAMILIES))
        for row in report.values():
            self.assertLessEqual(row["applicable"], row["checked"])


class MicrotestTests(unittest.TestCase):
    def test_every_suite_runs_and_reports(self) -> None:
        results = run_all_suites(build(default_genome()), FIXTURES[:6], max_queries=40)
        self.assertEqual(set(results), set(SUITES))
        for result in results.values():
            self.assertGreaterEqual(result.unanswerable_rate, 0.0)
            self.assertLessEqual(result.unanswerable_rate, 1.0)

    def test_suites_discriminate_between_representations(self) -> None:
        """If every candidate scores the same, the instrument is not measuring anything."""

        distances = {}
        for label in ("SEED_STRUCTURED_ENGLISH", "SEED_MINIMAL_MACHINE"):
            results = run_all_suites(build(SEEDS[label]), FIXTURES[:8], max_queries=60)
            distances[label] = results["binder_query"].mean_token_distance
        self.assertNotEqual(
            round(distances["SEED_STRUCTURED_ENGLISH"], 3),
            round(distances["SEED_MINIMAL_MACHINE"], 3),
        )

    def test_a_hidden_relation_is_reported_unanswerable(self) -> None:
        """A relation the rendering omits must be unanswerable, not answered by coincidence.

        The synthetic fixtures carry empty deltas, so the delta suite would otherwise have
        nothing to ask. One is given a real solved goal here, which is also what makes the
        section-scoping meaningful: the goal id appears in the state either way, and only a
        stated delta answers "which goal did this step solve?".
        """

        transition = json.loads(json.dumps(FIXTURES[0]))
        solved = transition["state_before"]["goals"][0]["identity"]
        transition["state_delta"]["goals_solved"] = [solved]

        stated = build(default_genome(delta_visibility="EXPLICIT_DELTA_BLOCK"))
        hidden = build(default_genome(delta_visibility="DERIVABLE_ONLY"))
        stated_result = run_all_suites(stated, [transition], max_queries=10)["delta_query"]
        hidden_result = run_all_suites(hidden, [transition], max_queries=10)["delta_query"]

        self.assertEqual(stated_result.queries, hidden_result.queries)
        self.assertGreater(stated_result.queries, 0)
        self.assertEqual(stated_result.unanswerable_rate, 0.0)
        self.assertEqual(hidden_result.unanswerable_rate, 1.0)

    def test_a_suite_with_no_queries_reports_zero_queries(self) -> None:
        """Zero queries and 100% answered must not look the same in a report."""

        result = run_all_suites(
            build(default_genome()), FIXTURES[:2], max_queries=10)["delta_query"]
        self.assertEqual(result.queries, 0)


class ValidationTests(unittest.TestCase):
    def test_a_reproduced_gain_is_elite_eligible(self) -> None:
        verdict = assess(
            "R_child", "bpe_tokens_per_transition",
            {"bpe_tokens_per_transition": 100.0}, {"bpe_tokens_per_transition": 80.0},
            {"bpe_tokens_per_transition": 100.0}, {"bpe_tokens_per_transition": 82.0},
        )
        self.assertEqual(verdict.verdict, REPRODUCED)
        self.assertTrue(verdict.elite_eligible)

    def test_a_dev_only_gain_is_quarantined(self) -> None:
        """DEV -30%, VALIDATION +8% is the case the mission names explicitly."""

        verdict = assess(
            "R_child", "binder_use_distance_tokens",
            {"binder_use_distance_tokens": 100.0}, {"binder_use_distance_tokens": 70.0},
            {"binder_use_distance_tokens": 100.0}, {"binder_use_distance_tokens": 108.0},
        )
        self.assertFalse(verdict.elite_eligible)
        self.assertIn(verdict.verdict, (QUARANTINED, "VALIDATION_CONTRADICTS_DEV"))

    def test_direction_is_respected_for_maximised_metrics(self) -> None:
        verdict = assess(
            "R_child", "detect_swap_records",
            {"detect_swap_records": 0.5}, {"detect_swap_records": 0.9},
            {"detect_swap_records": 0.5}, {"detect_swap_records": 0.88},
        )
        self.assertEqual(verdict.verdict, REPRODUCED)

    def test_quarantine_blocks_eliteness(self) -> None:
        quarantine = Quarantine()
        verdict = assess(
            "R_bad", "bpe_tokens_per_transition",
            {"bpe_tokens_per_transition": 100.0}, {"bpe_tokens_per_transition": 70.0},
            {"bpe_tokens_per_transition": 100.0}, {"bpe_tokens_per_transition": 130.0},
        )
        quarantine.record(verdict)
        self.assertTrue(quarantine.is_quarantined("R_bad"))
        self.assertFalse(quarantine.is_quarantined("R_good"))

    def test_a_consistently_worse_child_is_not_called_non_generalizing(self) -> None:
        """Worse on both splits is a failed hypothesis, not a generalization failure.

        Quarantining it would let this gate override Pareto selection: the candidate may
        still be the best thing available on a different axis.
        """

        from hml_v3.representation_search.validation import FAILED_ON_BOTH

        verdict = assess(
            "R_child", "binder_use_distance_tokens",
            {"binder_use_distance_tokens": 100.0}, {"binder_use_distance_tokens": 102.2},
            {"binder_use_distance_tokens": 100.0}, {"binder_use_distance_tokens": 102.1},
        )
        self.assertEqual(verdict.verdict, FAILED_ON_BOTH)
        self.assertTrue(verdict.elite_eligible)

    def test_only_a_dev_only_gain_blocks_eliteness(self) -> None:
        reproduced = assess(
            "R_a", "bpe_tokens_per_transition",
            {"bpe_tokens_per_transition": 100.0}, {"bpe_tokens_per_transition": 80.0},
            {"bpe_tokens_per_transition": 100.0}, {"bpe_tokens_per_transition": 81.0})
        dev_only = assess(
            "R_b", "bpe_tokens_per_transition",
            {"bpe_tokens_per_transition": 100.0}, {"bpe_tokens_per_transition": 80.0},
            {"bpe_tokens_per_transition": 100.0}, {"bpe_tokens_per_transition": 99.0})
        self.assertTrue(reproduced.elite_eligible)
        self.assertFalse(dev_only.elite_eligible)

    def test_the_policy_is_preregistered(self) -> None:
        self.assertTrue(Quarantine().policy.to_dict()["preregistered"])


class SealedIsolationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = Path(tempfile.mkdtemp(prefix="hml-sealed-"))
        rows = []
        for index in range(8):
            row = json.loads(json.dumps(FIXTURES[index % len(FIXTURES)]))
            row["transition_id"] = f"SEALED{index:03d}"
            rows.append(row)
        self.sealed = self.directory / "sealed.jsonl.gz"
        write_corpus(rows, self.sealed)
        self.client = SealedEvaluatorClient(self.sealed, self.directory / "access.jsonl")

    def tearDown(self) -> None:
        shutil.rmtree(self.directory, ignore_errors=True)

    def test_the_evaluator_runs_in_a_separate_process(self) -> None:
        result = self.client.evaluate(
            [{"candidate_id": "R_test", "genome": default_genome().to_dict()}],
            purpose="unit-test", sample=4, microtests=False,
        )
        self.assertEqual(result["isolation"], "SEPARATE_PROCESS")
        self.assertEqual(len(result["results"]), 1)

    def test_only_aggregate_keys_come_back(self) -> None:
        result = self.client.evaluate(
            [{"candidate_id": "R_test", "genome": default_genome().to_dict()}],
            purpose="unit-test", sample=4, microtests=False,
        )
        for row in result["results"]:
            self.assertTrue(set(row).issubset(ALLOWED_KEYS))
            self.assertNotIn("transitions", row)
            self.assertNotIn("state_before", row)

    def test_every_access_is_logged(self) -> None:
        self.assertEqual(self.client.access_count(), 0)
        self.client.evaluate(
            [{"candidate_id": "R_test", "genome": default_genome().to_dict()}],
            purpose="unit-test", sample=4, microtests=False,
        )
        self.assertEqual(self.client.access_count(), 1)

    def test_the_parent_process_never_imports_the_sealed_rows(self) -> None:
        """The search process holds a path, not data. Checked by construction."""

        self.assertIsInstance(self.client.sealed_path, Path)
        self.assertFalse(hasattr(self.client, "_transitions"))
        self.assertFalse(hasattr(self.client, "rows"))


class TokenizerAuditTests(unittest.TestCase):
    def test_several_vocabularies_are_available(self) -> None:
        found = available_tokenizers()
        usable = [name for name, entry in found.items() if entry["available"]]
        self.assertIn("gpt2", usable)
        self.assertGreaterEqual(len(usable), 2, "multi-tokenizer audit needs >1 vocabulary")

    def test_an_unavailable_vocabulary_is_reported_not_skipped(self) -> None:
        found = available_tokenizers()
        for name, entry in found.items():
            if not entry["available"]:
                self.assertTrue(entry["note"], f"{name} unavailable without a reason")

    def test_glyph_cost_is_vocabulary_specific(self) -> None:
        """FM-018, re-derived exactly: the same glyph costs different amounts."""

        found = available_tokenizers()
        costs = {
            name: entry["count"]("⊢")
            for name, entry in found.items() if entry["available"]
        }
        self.assertGreater(len(set(costs.values())), 1, f"expected disagreement, got {costs}")

    def test_ordering_agreement_detects_a_flip(self) -> None:
        from hml_v3.representation_search.tokenizers import TokenizerReport

        per_candidate = {
            "A": {"v1": TokenizerReport("v1", True, tokens_per_transition=100),
                  "v2": TokenizerReport("v2", True, tokens_per_transition=200)},
            "B": {"v1": TokenizerReport("v1", True, tokens_per_transition=150),
                  "v2": TokenizerReport("v2", True, tokens_per_transition=150)},
        }
        agreement = ordering_agreement(per_candidate)
        self.assertEqual(agreement["vocabularies_compared"], 2)
        self.assertFalse(agreement["same_leader_everywhere"])


if __name__ == "__main__":
    unittest.main()
