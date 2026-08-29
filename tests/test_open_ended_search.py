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


class InstrumentSaturationTests(unittest.TestCase):
    """`FM-010`, `FM-019` and `FM-029` were the same defect three times.

    Each was a metric that read the same value on every candidate, reached selection, and was
    only caught by reading a finished run. These tests are the mechanical form of that
    lesson: a saturated axis must be removed *before* it influences a choice.
    """

    def test_a_constant_axis_is_reported_as_non_discriminative(self) -> None:
        from hml_v3.representation_search.metrics import saturated_axes

        population = [
            ("a", {"constant": 1.0, "varies": 2.0}),
            ("b", {"constant": 1.0, "varies": 9.0}),
        ]
        report = saturated_axes(population, ["constant", "varies"])
        self.assertIn("constant", report)
        self.assertNotIn("varies", report)
        self.assertEqual(report["constant"]["distinct"], 1.0)

    def test_an_axis_no_candidate_carries_is_not_confused_with_a_saturated_one(self) -> None:
        from hml_v3.representation_search.metrics import axis_spread, saturated_axes

        population = [("a", {"present": 1.0}), ("b", {"present": 2.0})]
        self.assertIsNone(axis_spread(population, "absent"))
        self.assertNotIn("absent", saturated_axes(population, ["absent"]))

    def test_near_saturation_is_reported_but_never_demoted(self) -> None:
        """A 1% spread is a judgement call, and the guard does not make judgement calls."""

        from hml_v3.representation_search.metrics import (
            near_saturated_axes,
            saturated_axes,
        )

        # semantic_detect_rate as actually measured on the 918-transition pool.
        population = [(f"c{index}", {"barely": 1.0}) for index in range(201)]
        population.append(("c201", {"barely": 0.98989898989899}))
        self.assertNotIn("barely", saturated_axes(population, ["barely"]))
        self.assertIn("barely", near_saturated_axes(population, ["barely"]))

    def test_the_semantic_detection_metric_does_not_select(self) -> None:
        """FM-029, as a regression test rather than a note in a report."""

        from hml_v3.representation_search.controller_v2 import (
            DIAGNOSTIC_AXES,
            SELECTION_AXES,
        )

        self.assertNotIn("semantic_detect_rate", SELECTION_AXES)
        self.assertIn("semantic_detect_rate", DIAGNOSTIC_AXES)
        # FM-019's instrument stays out too.
        self.assertNotIn("detect_corrupt_identity", SELECTION_AXES)
        # Selection keeps an error-detection dimension rather than becoming five axes that
        # are all minimised.
        self.assertIn("detect_drop_field", SELECTION_AXES)

    def test_the_measured_v2_run_would_have_had_its_saturated_axis_demoted(self) -> None:
        """Replay: the guard must reproduce FM-029 from the finished run's own registry.

        Reads the *archived* first V2 run, not the live workspace. The live workspace is
        whatever search ran last, and pointing a regression test at moving data means it
        stops testing the thing it was written for.
        """

        from hml_v3.representation_search.metrics import saturated_axes

        # There is more than one archived run. Identify the 608-transition run FM-029 was
        # measured on by its split key, not by directory order: on the later 918-transition
        # pool the same metric reads 0.9899-1.0, which is near-saturated but not constant,
        # and picking the wrong archive silently tests the wrong claim.
        registry = None
        for manifest in (ROOT / "data/representation_search_v2/archive").glob(
                "*/split_manifest.json"):
            if json.loads(manifest.read_text()).get("split_key") == \
                    "hml-v3-representation-search-split-v1":
                candidate = manifest.parent / "candidate_registry.jsonl"
                if candidate.exists():
                    registry = candidate
                    break
        if registry is None:
            self.skipTest("the 608-transition run's archived registry is not present")
        latest: dict[str, dict] = {}
        for line in registry.read_text().splitlines():
            if line.strip():
                record = json.loads(line)
                latest[record["candidate_id"]] = record
        population = [
            (record["candidate_id"], record["metrics"]) for record in latest.values()
            if record.get("status") == "EVALUATED" and record.get("metrics")
        ]
        self.assertGreater(len(population), 100)
        saturated = saturated_axes(population, ["semantic_detect_rate"])
        self.assertIn("semantic_detect_rate", saturated)
        self.assertEqual(saturated["semantic_detect_rate"]["min"], 1.0)
        self.assertEqual(saturated["semantic_detect_rate"]["max"], 1.0)


class SearchPoolSplitTests(unittest.TestCase):
    def setUp(self) -> None:
        from hml_v3.representation_search.corpus import load_corpus, shard_paths

        pool = ROOT / "data/corpus/search_pool_v2.jsonl.gz"
        # The corpus is stored as size-capped shards, so the base name never exists as a
        # file. Checking it with Path.exists() silently skips the whole class.
        if not shard_paths(pool):
            self.skipTest("the V2 search pool is not present")
        self.rows = load_corpus(pool)

    def test_the_pool_split_reserves_no_second_seal(self) -> None:
        from hml_v3.representation_search.sealing import split_search_pool

        split = split_search_pool(self.rows)
        self.assertEqual(split.sealed, [])
        self.assertEqual(len(split.dev) + len(split.validation), len(self.rows))

    def test_no_theorem_family_straddles_dev_and_validation(self) -> None:
        from hml_v3.representation_search.sealing import family_of, split_search_pool

        split = split_search_pool(self.rows)
        dev = {family_of(row) for row in split.dev}
        validation = {family_of(row) for row in split.validation}
        self.assertEqual(dev & validation, set())

    def test_the_pool_split_key_cannot_be_confused_with_the_three_way_split(self) -> None:
        from hml_v3.representation_search.sealing import SPLIT_KEY, split_search_pool

        split = split_search_pool(self.rows)
        self.assertNotEqual(split.manifest()["split_key"], SPLIT_KEY)

    def test_the_pool_carries_the_multi_goal_structure_the_old_corpus_lacked(self) -> None:
        """FM-020/FM-028: goal ordering was unmeasurable at 1.01 goals per state."""

        goals = [len(row["state_before"]["goals"]) for row in self.rows]
        multi_goal = sum(1 for count in goals if count >= 2) / len(goals)
        self.assertGreater(multi_goal, 0.10)
        self.assertGreater(max(goals), 2)


class SealedRefusalTests(unittest.TestCase):
    def test_the_search_driver_refuses_a_sealed_corpus_path(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/search/run_open_ended_search.py"),
             "--corpus", str(ROOT / "data/corpus/sealed_final_v2.jsonl.gz"),
             "--generations", "1"],
            capture_output=True, text=True, check=False, cwd=ROOT,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("REFUSED", result.stdout + result.stderr)

    def test_sealed_final_v2_has_never_been_read(self) -> None:
        manifest = ROOT / "data/corpus/SEALED_V2_MANIFEST.json"
        if not manifest.exists():
            self.skipTest("SEALED_FINAL_V2 has not been created")
        payload = json.loads(manifest.read_text())
        self.assertEqual(payload["name"], "SEALED_FINAL_V2")
        log = ROOT / "data/representation_search_v2/sealed_access_log.jsonl"
        accesses = 0 if not log.exists() else sum(
            1 for line in log.read_text().splitlines() if line.strip())
        self.assertEqual(accesses, 0, "SEALED_FINAL_V2 must be unread until convergence")


class ConvergenceTests(unittest.TestCase):
    """A generation cap is not convergence, and the reason string has to say so."""

    def _controller(self, **overrides):
        from hml_v3.representation_search.controller_v2 import (
            OpenEndedController,
            SearchConfigV2,
        )

        config = SearchConfigV2(**overrides)
        workspace = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, workspace, True)
        return OpenEndedController([], [], workspace, [], config)

    def test_a_search_still_moving_has_not_converged(self) -> None:
        controller = self._controller(max_generations=40, stall_limit=5)
        controller.generation = 12
        controller.structural_stall = 2
        done, reason = controller.converged()
        self.assertFalse(done)
        self.assertEqual(reason, "SEARCHING")

    def test_the_generation_cap_reports_that_it_is_not_convergence(self) -> None:
        controller = self._controller(max_generations=40, stall_limit=5)
        controller.generation = 40
        controller.structural_stall = 1
        done, reason = controller.converged()
        self.assertTrue(done)
        self.assertIn("NOT_CONVERGED", reason)
        self.assertFalse(controller.convergence_state()["structurally_converged"])

    def test_structural_convergence_is_reported_as_convergence(self) -> None:
        controller = self._controller(max_generations=40, stall_limit=5)
        controller.generation = 22
        controller.structural_stall = 5
        done, reason = controller.converged()
        self.assertTrue(done)
        self.assertIn("STRUCTURAL_CONVERGENCE", reason)
        self.assertTrue(controller.convergence_state()["structurally_converged"])

    def test_convergence_outranks_the_cap(self) -> None:
        """Reaching both at once is convergence, not a budget exhaustion."""

        controller = self._controller(max_generations=40, stall_limit=5)
        controller.generation = 40
        controller.structural_stall = 5
        _done, reason = controller.converged()
        self.assertIn("STRUCTURAL_CONVERGENCE", reason)


class OllamaTransportTests(unittest.TestCase):
    """The defect that made a second backend look like a model with nothing to say."""

    def test_a_thinking_model_gets_an_empty_think_prefill(self) -> None:
        from hml_v3.representation_search.meta_designer.llm import (
            EMPTY_THINK_PREFILL,
            OllamaTransport,
        )

        transport = OllamaTransport("qwen38-rvn:latest")
        self.assertTrue(transport.suppress_thinking)
        messages = transport.messages("sys", "user")
        self.assertEqual([m["role"] for m in messages], ["system", "user", "assistant"])
        self.assertEqual(messages[-1]["content"], EMPTY_THINK_PREFILL)

    def test_a_non_thinking_model_is_left_alone(self) -> None:
        from hml_v3.representation_search.meta_designer.llm import OllamaTransport

        transport = OllamaTransport("gemma3:4b")
        self.assertFalse(transport.suppress_thinking)
        self.assertEqual([m["role"] for m in transport.messages("s", "u")], ["system", "user"])

    def test_a_reasoning_block_is_stripped_before_parsing(self) -> None:
        payloads = extract_proposals(
            '<think>I will use [brackets] and {braces} while thinking.</think>\n'
            '[{"proposal_type": "AXIS_MUTATION"}]'
        )
        self.assertEqual(payloads, [{"proposal_type": "AXIS_MUTATION"}])

    def test_output_that_is_only_a_reasoning_block_yields_nothing(self) -> None:
        self.assertEqual(extract_proposals("<think>still thinking</think>"), [])


class StructuralSamplingTests(unittest.TestCase):
    """A corpus the search never sees is a corpus that was not acquired.

    FM-028 recorded that targeted acquisition closed FM-020's measurability gap. These tests
    guard the step after that: the sample handed to the evaluator has to carry the structure
    the campaign bought.
    """

    def setUp(self) -> None:
        from hml_v3.representation_search.corpus import load_corpus, shard_paths

        pool = ROOT / "data/corpus/search_pool_v2.jsonl.gz"
        if not shard_paths(pool):
            self.skipTest("the V2 search pool is not present")
        from hml_v3.representation_search.sealing import split_search_pool

        self.dev = split_search_pool(load_corpus(pool)).dev

    def test_a_prefix_sample_hides_the_structure_a_stratified_one_shows(self) -> None:
        from hml_v3.representation_search.sampling import profile, structural_sample

        prefix = profile(self.dev[:28])
        stratified = profile(structural_sample(self.dev, 28))
        # The regression this whole module exists to prevent.
        self.assertLessEqual(prefix["max_goals"], 3)
        self.assertGreaterEqual(stratified["max_goals"], 6)
        self.assertGreater(stratified["multi_goal_share"], prefix["multi_goal_share"])

    def test_every_non_empty_stratum_survives_even_a_tiny_sample(self) -> None:
        from hml_v3.representation_search.sampling import stratify, structural_sample

        population = set(stratify(self.dev))
        for size in (8, 12, 14, 28):
            sampled = set(stratify(structural_sample(self.dev, size)))
            self.assertEqual(sampled, population, f"size={size}")

    def test_the_sample_is_exactly_the_requested_size(self) -> None:
        from hml_v3.representation_search.sampling import structural_sample

        for size in (1, 4, 8, 12, 28, 64, 200):
            self.assertEqual(len(structural_sample(self.dev, size)), size, f"size={size}")

    def test_sampling_is_deterministic_for_a_fixed_seed(self) -> None:
        from hml_v3.representation_search.sampling import structural_sample

        first = [row["transition_id"] for row in structural_sample(self.dev, 28, seed=7)]
        second = [row["transition_id"] for row in structural_sample(self.dev, 28, seed=7)]
        other = [row["transition_id"] for row in structural_sample(self.dev, 28, seed=8)]
        self.assertEqual(first, second)
        self.assertNotEqual(first, other)

    def test_asking_for_more_than_exists_returns_everything_once(self) -> None:
        from hml_v3.representation_search.sampling import structural_sample

        everything = structural_sample(self.dev, len(self.dev) + 50)
        self.assertEqual(len(everything), len(self.dev))
        ids = [row["transition_id"] for row in everything]
        self.assertEqual(len(ids), len(set(ids)))

    def test_the_controller_samples_structurally(self) -> None:
        from hml_v3.representation_search.controller_v2 import (
            OpenEndedController,
            SearchConfigV2,
        )
        from hml_v3.representation_search.sampling import profile

        workspace = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, workspace, True)
        controller = OpenEndedController(
            self.dev, self.dev[:100], workspace, [],
            SearchConfigV2(dev_sample=28, mutation_sample=12))
        self.assertGreaterEqual(profile(controller.dev_sample)["max_goals"], 6)
        self.assertGreaterEqual(profile(controller.mutation_sample)["max_goals"], 6)


class DuplicateAxisTests(unittest.TestCase):
    """`FM-033`: an axis can change the rendering and still already exist.

    The observable-effect gate asks "does this axis do anything". It does not ask "does the
    genome already have an axis that does exactly this", and nine of the first thirty axes
    accepted on the pool run were the same `neighbourhood_capsule` dimension under nine
    different names.
    """

    VALUES = ("NONE", "GOAL_LOCAL", "ACTION_LOCAL")

    def _registry(self):
        from hml_v3.representation_search.primitive_registry import PrimitiveRegistry

        workspace = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, workspace, True)
        return PrimitiveRegistry(workspace / "primitives.jsonl")

    def _primitive(self, name, hook="neighbourhood_capsule", values=None):
        from hml_v3.representation_search.primitive_registry import RegisteredPrimitive

        return RegisteredPrimitive(
            axis_name=name, values=values or self.VALUES, hook=hook, params={},
            proposal_id=f"P_{name}", generation=1, proposer="test",
            hypothesis="h", mechanism="m", falsification="f",
            schema_version="representation-genome-v2.1.0")

    def _factory(self, registry):
        from hml_v3.representation_search.compiler import build
        from hml_v3.representation_search.genome import RepresentationGenome

        base = RepresentationGenome({})
        return lambda invented: build(base, invented, registry)

    def _transitions(self):
        from hml_v3.representation_search.corpus import load_corpus, shard_paths
        from hml_v3.representation_search.sealing import split_search_pool

        pool = ROOT / "data/corpus/search_pool_v2.jsonl.gz"
        if not shard_paths(pool):
            self.skipTest("the V2 search pool is not present")
        return split_search_pool(load_corpus(pool)).dev[:3]

    def test_a_renamed_copy_of_an_existing_axis_is_rejected(self) -> None:
        registry = self._registry()
        transitions = self._transitions()
        first = self._primitive("dependency_capsule")
        registry.register(first)
        second = self._primitive("semantic_summary")
        registry.register(second)
        duplicate_of, evidence = registry.duplicates_an_existing_axis(
            second, self._factory(registry), transitions)
        self.assertEqual(duplicate_of, "dependency_capsule")
        registry.reject_duplicate(second, evidence)
        self.assertNotIn("semantic_summary", registry.primitives)
        self.assertEqual(
            registry.unimplementable[-1]["status"], "ACCEPTED_DUPLICATE")

    def test_a_genuinely_different_axis_is_kept(self) -> None:
        registry = self._registry()
        transitions = self._transitions()
        registry.register(self._primitive("dependency_capsule"))
        other = self._primitive(
            "metavar_partitioning", hook="section_partition",
            values=("NONE", "INLINE", "SECTION_BLOCK"))
        registry.register(other)
        duplicate_of, _evidence = registry.duplicates_an_existing_axis(
            other, self._factory(registry), transitions)
        self.assertIsNone(duplicate_of)

    def test_the_first_axis_of_its_kind_is_not_a_duplicate_of_itself(self) -> None:
        registry = self._registry()
        transitions = self._transitions()
        only = self._primitive("dependency_capsule")
        registry.register(only)
        duplicate_of, _evidence = registry.duplicates_an_existing_axis(
            only, self._factory(registry), transitions)
        self.assertIsNone(duplicate_of)

    def test_stacking_two_copies_is_idempotent_which_is_why_they_are_redundant(self) -> None:
        """The measurement that made the verdict unambiguous."""

        registry = self._registry()
        transitions = self._transitions()
        registry.register(self._primitive("axis_alpha"))
        registry.register(self._primitive("axis_beta"))
        factory = self._factory(registry)

        def render(invented):
            compiler = factory(invented)
            return "\n".join(compiler.render_text(row) for row in transitions)

        alpha = render({"axis_alpha": "GOAL_LOCAL"})
        beta = render({"axis_beta": "GOAL_LOCAL"})
        both = render({"axis_alpha": "GOAL_LOCAL", "axis_beta": "GOAL_LOCAL"})
        self.assertNotEqual(alpha, render({}))
        self.assertEqual(alpha, beta)
        self.assertEqual(both, alpha)


class ConvergenceTrajectoryTests(unittest.TestCase):
    """The preregistered criterion was satisfiable, and the run satisfied it.

    Mid-run it did not look that way: at generation 70 entrants averaged 2.3 per generation
    with no visible downward trend, which is the sort of observation that invites weakening a
    criterion. Churn kept falling and reached zero. This test pins the trajectory so the
    conclusion rests on the record rather than on anybody's recollection of it.
    """

    def setUp(self) -> None:
        self.state_path = ROOT / "data/representation_search_v2/search_state.json"
        if not self.state_path.exists():
            self.skipTest("no completed search in the workspace")
        self.state = json.loads(self.state_path.read_text())

    def test_the_run_converged_on_the_preregistered_criterion(self) -> None:
        self.assertGreaterEqual(
            self.state["structural_stall"], self.state["config"]["stall_limit"])

    def test_the_final_generations_had_no_frontier_churn_at_all(self) -> None:
        generations = sorted(
            (ROOT / "data/representation_search_v2/generations").glob("generation_*.json"))
        payloads = [json.loads(path.read_text()) for path in generations]
        limit = self.state["config"]["stall_limit"]
        tail = payloads[-(limit + 1):]
        for earlier, later in zip(tail, tail[1:]):
            before, after = set(earlier["front"]), set(later["front"])
            self.assertEqual(after - before, set(), f"gen {later['generation']} gained members")
            self.assertEqual(before - after, set(), f"gen {later['generation']} lost members")
            self.assertFalse(later["frontier_moved"], f"gen {later['generation']} moved")
            self.assertEqual(later["new_axes"], [], f"gen {later['generation']} grew the genome")

    def test_selection_never_had_to_demote_an_axis(self) -> None:
        """All six preregistered axes discriminated for the whole run."""

        self.assertEqual(self.state["demoted_axes"], {})
        self.assertEqual(
            self.state["selection_axes"], self.state["preregistered_selection_axes"])


class RegistryReloadTests(unittest.TestCase):
    def test_a_registry_containing_rejections_reloads(self) -> None:
        """Resume must survive every rejection kind, including ones added later."""

        from hml_v3.representation_search.primitive_registry import (
            PrimitiveRegistry,
            RegisteredPrimitive,
        )

        workspace = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, workspace, True)
        path = workspace / "primitive_registry.jsonl"
        registry = PrimitiveRegistry(path)
        registry.register(RegisteredPrimitive(
            axis_name="kept", values=("NONE", "ON"), hook="section_partition", params={},
            proposal_id="P_1", generation=1, proposer="test",
            hypothesis="h", mechanism="m", falsification="f",
            schema_version="representation-genome-v2.1.0"))
        registry.unimplementable.append(
            {"status": "ACCEPTED_UNIMPLEMENTABLE", "axis_name": "no_hook"})
        registry.unimplementable.append(
            {"status": "ACCEPTED_DUPLICATE", "axis_name": "copy",
             "evidence": {"duplicate_of": "kept"}})
        registry.unimplementable.append(
            {"status": "SOME_FUTURE_REJECTION", "axis_name": "later"})
        registry.flush()

        reloaded = PrimitiveRegistry(path)
        self.assertEqual(sorted(reloaded.primitives), ["kept"])
        self.assertEqual(len(reloaded.unimplementable), 3)
        self.assertEqual(reloaded.rejection_counts()["ACCEPTED_DUPLICATE"], 1)

    def test_the_completed_run_registry_reloads(self) -> None:
        from hml_v3.representation_search.primitive_registry import PrimitiveRegistry

        path = ROOT / "data/representation_search_v2/primitive_registry.jsonl"
        if not path.exists():
            self.skipTest("no completed search in the workspace")
        registry = PrimitiveRegistry(path)
        self.assertGreater(len(registry.primitives), 0)
        for primitive in registry.primitives.values():
            self.assertIn("NONE", primitive.values)


class InventedAxisIdentityTests(unittest.TestCase):
    """`FM-036`: an invented-axis candidate does not own its base genome's id.

    Anything that keys results by ``genome.candidate_id()`` rather than by the record id
    collides for the parent and returns nothing for the child.
    """

    def test_an_invented_axis_candidate_has_an_id_its_base_genome_does_not(self) -> None:
        from hml_v3.representation_search.genome import default_genome
        from hml_v3.representation_search.genome_migrations import ExtendedGenome

        base = default_genome()
        extended = ExtendedGenome(base, {"dependency_capsule": "GOAL_LOCAL"})
        self.assertNotEqual(extended.candidate_id(), base.candidate_id())
        self.assertEqual(
            ExtendedGenome(base, {}).candidate_id(), base.candidate_id())

    def test_the_completed_run_has_candidates_sharing_a_base_genome(self) -> None:
        state = ROOT / "data/representation_search_v2/search_state.json"
        if not state.exists():
            self.skipTest("no completed search in the workspace")
        invented = json.loads(state.read_text()).get("invented") or {}
        self.assertGreater(len(invented), 0,
                           "the run accepted invented axes, so carriers must exist")
