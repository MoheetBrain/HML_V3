"""The open-ended search controller.

Differences from V1 that matter:

* proposals come from a `MetaDesignerBackend`, so a model can propose axes the genome does
  not have — the search is no longer confined to recombining 42 human-chosen dimensions;
* a child climbs a ladder (compile, semantics, microtests, static, validation) and is killed
  at the cheapest level that can kill it;
* eliteness requires the dev-set claim to reproduce on validation;
* corruption is applied to the canonical state, once, upstream of every candidate;
* the sealed split lives in another process and is never touched during search.

Every generation is checkpointed, including the genome schema version, so a run that grows
its own search space can still be resumed exactly.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
import random
import time
from typing import Any

from hml_v3.representation_search.compiler import CompilerRejection, build
from hml_v3.representation_search.failure_memory import FailureMemory
from hml_v3.representation_search.gates import run_gates
from hml_v3.representation_search.genome import AXES, RepresentationGenome
from hml_v3.representation_search.genome_migrations import (
    ExtendedGenome,
    extended_space,
    space_size,
)
from hml_v3.representation_search.lineage import CandidateRecord, CandidateRegistry
from hml_v3.representation_search.meta_designer.base import (
    MetaDesignerBackend,
    ScientistReport,
)
from hml_v3.representation_search.metrics import (
    MAXIMISED,
    PARETO_AXES,
    measure,
    near_saturated_axes,
    saturated_axes,
)
from hml_v3.representation_search.microtests import SUITES, run_all_suites
from hml_v3.representation_search.pareto import frontier_signature, select, shortlist
from hml_v3.representation_search.sampling import profile as sample_profile
from hml_v3.representation_search.sampling import structural_sample
from hml_v3.representation_search.primitive_registry import PrimitiveRegistry
from hml_v3.representation_search.seeds import SEEDS, seed_population
from hml_v3.representation_search import semantic_mutations
from hml_v3.representation_search.validation import (
    Quarantine,
    ValidationPolicy,
    assess,
)

STATE_VERSION = "open-ended-search-state-v2.0.0"

#: Microtest metrics promoted into selection. Chosen because they discriminate: the V1 Pareto
#: vector measured aggregate locality and could not see that a candidate was cheap on average
#: while every specific structural query was expensive.
MICROTEST_AXES = (
    "binder_query_token_distance",
    "dependency_query_token_distance",
    "premise_query_token_distance",
    "scope_query_token_distance",
)

#: The axes selection is computed over. Every one of these must be *measured to discriminate*
#: on the corpus actually in use; an axis that reads the same on every candidate is removed by
#: :meth:`OpenEndedController.enforce_discrimination` before it can influence a single choice.
#:
#: ``semantic_detect_rate`` is deliberately absent. It was built to replace the text-level
#: corruption metric FM-019 found saturated, and measured across all 201 candidates of the
#: first V2 run it was 1.000 everywhere (`FM-029`): its predicate asks whether the rendering
#: changes when the canonical state is corrupted, and every representation that renders the
#: state at all fails that test identically. It is still measured and still reported; it does
#: not select.
#:
#: ``detect_drop_field`` takes its place so selection keeps an error-detection dimension
#: rather than becoming five cost-and-locality axes that are all minimised. It was chosen
#: because it is the detection family with real spread on the same 201 candidates:
#: 0.000-0.750, twelve distinct values, coefficient of variation 1.506.
SELECTION_AXES = (
    "bpe_tokens_per_transition",
    "binder_use_distance_tokens",
    "detect_drop_field",
    "binder_query_token_distance",
    "dependency_query_token_distance",
    "identifier_fragmentation",
)

#: Measured every generation and reported, but never selected on. An axis lands here either
#: because it was preregistered as diagnostic-only or because the saturation guard demoted it.
DIAGNOSTIC_AXES = (
    "semantic_detect_rate",
    "detect_corrupt_identity",
)


@dataclass
class SearchConfigV2:
    population_capacity: int = 24
    children_per_generation: int = 18
    novelty_slots: int = 3
    dev_sample: int = 32
    validation_sample: int = 24
    microtest_sample: int = 16
    mutation_sample: int = 16
    max_generations: int = 40
    stall_limit: int = 5
    material_improvement: float = 0.005
    seed: int = 20260828
    llm_every: int = 1

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


@dataclass
class GenerationReportV2:
    generation: int
    evaluated: list[str]
    killed: list[dict[str, Any]]
    front: list[str]
    survivors: list[str]
    proposals: dict[str, Any]
    new_axes: list[str]
    validation_verdicts: list[dict[str, Any]]
    frontier_signature: list[float]
    frontier_moved: bool
    genome_schema: str
    elapsed_seconds: float
    ladder: dict[str, int] = field(default_factory=dict)
    selection_axes: list[str] = field(default_factory=list)
    axis_demotions: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "generation": self.generation,
            "evaluated": self.evaluated,
            "killed": self.killed,
            "front": self.front,
            "survivors": self.survivors,
            "proposals": self.proposals,
            "new_axes": self.new_axes,
            "validation_verdicts": self.validation_verdicts,
            "frontier_signature": self.frontier_signature,
            "frontier_moved": self.frontier_moved,
            "genome_schema": self.genome_schema,
            "ladder": self.ladder,
            "selection_axes": self.selection_axes,
            "axis_demotions": self.axis_demotions,
            "elapsed_seconds": round(self.elapsed_seconds, 3),
        }


class OpenEndedController:
    def __init__(
        self, dev: list[dict[str, Any]], validation: list[dict[str, Any]],
        workspace: Path, backends: list[MetaDesignerBackend],
        config: SearchConfigV2 | None = None,
        memory: FailureMemory | None = None,
    ) -> None:
        self.dev = dev
        self.validation = validation
        self.workspace = workspace
        self.backends = backends
        self.config = config or SearchConfigV2()
        self.memory = memory or FailureMemory.load()
        self.registry = CandidateRegistry(workspace / "candidate_registry.jsonl")
        self.primitives = PrimitiveRegistry(workspace / "primitive_registry.jsonl")
        self.proposals_path = workspace / "proposal_history.jsonl"
        self.state_path = workspace / "search_state.json"
        self.generations_dir = workspace / "generations"
        self.quarantine = Quarantine(ValidationPolicy())
        self.rng = random.Random(self.config.seed)
        self.generation = 0
        self.population: list[str] = []
        self.pinned: list[str] = []
        self.history: list[dict[str, Any]] = []
        self.stall_count = 0
        self.last_signature: tuple[float, ...] | None = None
        #: Consecutive generations in which the frontier did not improve, its membership did
        #: not change, and the genome did not grow. This -- not a generation count -- is what
        #: the run stops on.
        self.structural_stall = 0
        self.last_front: tuple[str, ...] | None = None
        # Stratified, not prefixed. A prefix of the V2 pool sorted by transition id contains
        # no state with more than three goals, so a prefix-sampled search would have
        # re-derived FM-020 on the very corpus that was acquired to fix it. See
        # representation_search.sampling for the measured comparison.
        self.dev_sample = structural_sample(dev, self.config.dev_sample, self.config.seed)
        self.validation_sample = structural_sample(
            validation, self.config.validation_sample, self.config.seed)
        self.microtest_sample = structural_sample(
            dev, self.config.microtest_sample, self.config.seed)
        self.mutation_sample = structural_sample(
            dev, self.config.mutation_sample, self.config.seed)
        self.invented: dict[str, dict[str, str]] = {}
        #: Live selection vector. Starts as the preregistered SELECTION_AXES and can only
        #: ever shrink, when the saturation guard measures an axis to be non-discriminative.
        self.selection_axes: list[str] = list(SELECTION_AXES)
        #: axis -> the measured spread that demoted it, kept as evidence.
        self.demoted_axes: dict[str, dict[str, float]] = {}

    # ----------------------------------------------------------------------- persistence
    def save(self) -> None:
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.registry.flush()
        self.primitives.flush()
        self.state_path.write_text(json.dumps({
            "schema_version": STATE_VERSION,
            "genome_schema": self.primitives.schema_version,
            "generation": self.generation,
            "population": self.population,
            "pinned": self.pinned,
            "stall_count": self.stall_count,
            "structural_stall": self.structural_stall,
            "last_front": list(self.last_front) if self.last_front else None,
            "last_signature": list(self.last_signature) if self.last_signature else None,
            "config": self.config.to_dict(),
            "rng_state": _encode_rng(self.rng.getstate()),
            "history": self.history,
            "invented": self.invented,
            "quarantine": self.quarantine.summary(),
            "primitives": self.primitives.statistics(),
            "selection_axes": list(self.selection_axes),
            "preregistered_selection_axes": list(SELECTION_AXES),
            "diagnostic_axes": list(DIAGNOSTIC_AXES),
            "demoted_axes": self.demoted_axes,
            "backends": [backend.name for backend in self.backends],
        }, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    def resume(self) -> bool:
        if not self.state_path.exists():
            return False
        state = json.loads(self.state_path.read_text(encoding="utf-8"))
        self.generation = state["generation"]
        self.population = state["population"]
        self.pinned = state["pinned"]
        self.stall_count = state["stall_count"]
        self.structural_stall = state.get("structural_stall", 0)
        self.last_front = tuple(state["last_front"]) if state.get("last_front") else None
        self.last_signature = (
            tuple(state["last_signature"]) if state["last_signature"] else None)
        self.history = state["history"]
        self.invented = state.get("invented", {})
        self.selection_axes = state.get("selection_axes") or list(SELECTION_AXES)
        self.demoted_axes = state.get("demoted_axes", {})
        self.rng.setstate(_decode_rng(state["rng_state"]))
        return True

    # --------------------------------------------------------------------------- seeding
    def seed(self) -> None:
        for genome in seed_population():
            record = CandidateRecord(
                candidate_id=genome.candidate_id(), genome=genome, generation=0,
                origin="SEED", parents=(),
                hypothesis={"statement": genome.notes, "source": "GENERATION_ZERO_SEED"},
            )
            self.registry.add(record)
            if genome.candidate_id() not in self.population:
                self.population.append(genome.candidate_id())
        pinned = set(self.memory.pinned_seeds())
        self.pinned = sorted(
            SEEDS[label].candidate_id() for label in pinned if label in SEEDS)

    def _compiler(self, record: CandidateRecord):
        invented = self.invented.get(record.candidate_id, {})
        return build(record.genome, invented, self.primitives if invented else None)

    # ------------------------------------------------------------------------- the ladder
    def evaluate(self, candidate_ids: list[str]) -> tuple[list[str], list[dict[str, Any]], dict[str, int]]:
        """Climb the ladder; kill at the cheapest level that can kill.

        A candidate that fails semantics never reaches the tokenizer, and one that is
        structurally opaque never reaches validation. This is where the budget is saved.
        """

        evaluated: list[str] = []
        killed: list[dict[str, Any]] = []
        ladder = {"compile": 0, "semantics": 0, "microtests": 0, "static": 0, "passed": 0}

        for candidate_id in candidate_ids:
            record = self.registry.get(candidate_id)
            if record is None:
                continue
            if record.status == "EVALUATED":
                evaluated.append(candidate_id)
                continue
            if record.status == "HARD_REJECTED":
                killed.append({"candidate_id": candidate_id, "level": "cached",
                               "reason": record.rejection_reason})
                continue

            # LEVEL 0 — does it compile at all?
            try:
                compiler = self._compiler(record)
            except CompilerRejection as error:
                ladder["compile"] += 1
                self._kill(record, "compile", str(error).split(":")[0], killed)
                continue

            # LEVEL 1 — semantics. Non-negotiable.
            report = run_gates(compiler, self.dev_sample)
            record.gates = report.to_dict()
            if not report.passed:
                ladder["semantics"] += 1
                self._kill(record, "semantics", report.first_failure or "gate", killed)
                continue

            # LEVEL 2 — mechanism-specific structural access.
            suites = run_all_suites(compiler, self.microtest_sample, max_queries=90)
            microtest_metrics: dict[str, float] = {}
            for result in suites.values():
                microtest_metrics.update(result.metrics())
            if microtest_metrics.get("binder_query_unanswerable", 0.0) >= 1.0:
                ladder["microtests"] += 1
                self._kill(record, "microtests", "binder_query_unanswerable", killed)
                continue

            # LEVEL 3 — static cost, locality, tokenizer.
            vector = measure(compiler, self.dev_sample)
            values = dict(vector.values)
            values.update(microtest_metrics)
            values["semantic_detect_rate"] = self._semantic_detection(compiler)
            record.metrics = values
            record.status = "EVALUATED"
            self.registry.update(record)
            ladder["static"] += 1
            ladder["passed"] += 1
            evaluated.append(candidate_id)
        return evaluated, killed, ladder

    def _kill(
        self, record: CandidateRecord, level: str, reason: str, killed: list[dict[str, Any]],
    ) -> None:
        record.status = "HARD_REJECTED"
        record.rejection_reason = reason
        self.registry.update(record)
        killed.append({"candidate_id": record.candidate_id, "level": level, "reason": reason})

    def _semantic_detection(self, compiler) -> float:
        """Fraction of canonical-level corruptions this representation can expose.

        The corruption is applied to the state, once, upstream. Every candidate is asked the
        same question, so a syntax family cannot win by having more lines to delete.
        """

        rng = random.Random(self.config.seed)
        detected = 0
        attempted = 0
        for transition in self.mutation_sample:
            for family in semantic_mutations.FAMILIES:
                result = semantic_mutations.apply_mutation(transition, family, rng)
                if result is None:
                    continue
                attempted += 1
                try:
                    clean = compiler.render_text(transition)
                    corrupted = compiler.render_text(result.state)
                except Exception:  # noqa: BLE001 - a render failure is a detection
                    detected += 1
                    continue
                # The representation exposes the corruption when the rendering changes: a
                # candidate that renders a corrupted state identically has hidden the defect.
                if clean != corrupted:
                    detected += 1
        return detected / attempted if attempted else 0.0

    # ------------------------------------------------------------ instrument saturation
    #: The guard will not act on fewer candidates than this. Sixteen generation-zero seeds
    #: were enough to catch FM-019 by hand, but acting on three would demote an axis for
    #: having had no chance to vary yet.
    MIN_POPULATION_FOR_DEMOTION = 12
    #: Selection must never collapse to a single objective; FM-008 forbids it.
    MIN_SELECTION_AXES = 3

    def enforce_discrimination(self) -> list[dict[str, Any]]:
        """Demote any selection axis that measured identically on every candidate.

        Three times now a saturated instrument reached selection and was only caught by
        reading a finished run: `FM-010` (minimal pairs), `FM-019` (identifier corruption)
        and `FM-029` (semantic corruption). Each was corrected by editing the axis list by
        hand, after the run it had already influenced. This runs the same check every
        generation, on the population actually evaluated, and removes the axis before it can
        influence the next selection.

        Demotion is one-way and recorded. An axis is never restored on a later generation:
        re-admitting an instrument because a wider population finally moved it by a rounding
        error is how a saturated axis gets a second life.
        """

        population = [
            (record.candidate_id, record.metrics or {})
            for record in self.registry.accepted()
            if record.metrics
        ]
        if len(population) < self.MIN_POPULATION_FOR_DEMOTION:
            return []
        saturated = saturated_axes(population, self.selection_axes)
        actions: list[dict[str, Any]] = []
        for axis, spread in sorted(
                near_saturated_axes(population, self.selection_axes).items()):
            # Reported, never demoted. A human decides whether a 1% spread is an effect.
            actions.append({
                "axis": axis, "action": "REPORTED_NEAR_SATURATED",
                "reason": "discriminates barely; not demoted, because demotion on a "
                          "threshold can discard a real but small effect",
                "spread": {key: round(value, 9) for key, value in spread.items()},
                "generation": self.generation,
            })
        for axis, spread in sorted(saturated.items()):
            if len(self.selection_axes) <= self.MIN_SELECTION_AXES:
                actions.append({
                    "axis": axis, "action": "RETAINED_UNDER_PROTEST",
                    "reason": "demoting it would drop selection below MIN_SELECTION_AXES",
                    "spread": {key: round(value, 9) for key, value in spread.items()},
                    "generation": self.generation,
                })
                continue
            self.selection_axes.remove(axis)
            self.demoted_axes[axis] = {
                **{key: round(value, 9) for key, value in spread.items()},
                "demoted_at_generation": float(self.generation),
            }
            actions.append({
                "axis": axis, "action": "DEMOTED_TO_DIAGNOSTIC",
                "reason": "non-discriminative: identical on every evaluated candidate",
                "spread": {key: round(value, 9) for key, value in spread.items()},
                "generation": self.generation,
            })
        return actions

    # ---------------------------------------------------------------------- validation
    def validate_children(self, evaluated: list[str]) -> list[dict[str, Any]]:
        verdicts: list[dict[str, Any]] = []
        for candidate_id in evaluated:
            record = self.registry.get(candidate_id)
            if record is None or not record.parents or not record.hypothesis:
                continue
            parent = self.registry.get(record.parents[0])
            if parent is None or not parent.metrics or not record.metrics:
                continue
            metric = record.hypothesis.get("target_metric")
            if metric not in (record.metrics or {}):
                continue
            child_validation = self._validation_metrics(record)
            parent_validation = self._validation_metrics(parent)
            if child_validation is None or parent_validation is None:
                continue
            verdict = assess(
                candidate_id, metric, parent.metrics, record.metrics,
                parent_validation, child_validation,
                self.quarantine.policy.tolerance, self.quarantine.policy.noise_floor,
            )
            self.quarantine.record(verdict)
            verdicts.append(verdict.to_dict())
        return verdicts

    def _validation_metrics(self, record: CandidateRecord) -> dict[str, float] | None:
        cached = (record.gates or {}).get("_validation_metrics")
        if cached:
            return cached
        try:
            compiler = self._compiler(record)
        except CompilerRejection:
            return None
        report = run_gates(compiler, self.validation_sample[:8])
        if not report.passed:
            return None
        values = dict(measure(compiler, self.validation_sample).values)
        record.gates = dict(record.gates or {})
        record.gates["_validation_metrics"] = values
        self.registry.update(record)
        return values

    # ------------------------------------------------------------------- the report out
    def build_report(self, front: list[str], evaluated: list[str]) -> ScientistReport:
        space = extended_space(self.primitives)
        population = [
            (record.candidate_id, record.metrics or {})
            for record in self.registry.accepted()
        ]
        elites = []
        for candidate_id in front[:6]:
            record = self.registry.get(candidate_id)
            if record is None:
                continue
            elites.append({
                "candidate_id": candidate_id,
                "genome": {
                    axis: record.genome.get(axis)
                    for axis in ("syntax_family", "expression_notation", "context_order",
                                 "action_position", "premise_locality", "lexicon_register",
                                 "identity_scheme", "redundancy_level")
                },
                "invented": self.invented.get(candidate_id, {}),
                "metrics": {
                    axis: round((record.metrics or {}).get(axis, 0.0), 3)
                    for axis in self.selection_axes
                },
                "weaknesses": self._weaknesses(candidate_id, population),
            })
        return ScientistReport(
            generation=self.generation, phase=None,
            genome_axes=space.values(),
            elites=elites,
            metric_directions={
                axis: ("maximise" if axis in MAXIMISED else "minimise")
                for axis in self.selection_axes
            },
            validation_divergence=self.quarantine.summary()["worst_divergences"][:5],
            microtest_failures=self._microtest_failures(front),
            failure_memory=[
                {"id": lesson.id, "title": lesson.title, "disposition": lesson.disposition}
                for lesson in self.memory.lessons
                if lesson.disposition in ("DO_NOT_RETRY_UNCHANGED", "HARD_GATE")
            ],
            corpus_profile=self._corpus_profile(),
            unmeasurable_axes=self._unmeasurable_axes(),
            unresolved_questions=self._unresolved(),
            lineage_summary=self.registry.statistics(),
            budget={"generation": self.generation, "max": self.config.max_generations},
        )

    def _weaknesses(self, candidate_id: str, population: list[tuple[str, dict[str, float]]]) -> list[str]:
        record = self.registry.get(candidate_id)
        if record is None or not record.metrics:
            return []
        weak: list[tuple[float, str]] = []
        for axis in self.selection_axes:
            column = [values.get(axis, 0.0) for _, values in population if values]
            if not column:
                continue
            low, high = min(column), max(column)
            if high - low <= 0:
                continue
            position = (record.metrics.get(axis, 0.0) - low) / (high - low)
            if axis in MAXIMISED:
                position = 1.0 - position
            weak.append((position, axis))
        weak.sort(reverse=True)
        return [axis for score, axis in weak[:3] if score > 0.5]

    def _microtest_failures(self, front: list[str]) -> list[dict[str, Any]]:
        failures: list[dict[str, Any]] = []
        for candidate_id in front[:6]:
            record = self.registry.get(candidate_id)
            if record is None or not record.metrics:
                continue
            for suite in SUITES:
                key = f"{suite}_unanswerable"
                rate = record.metrics.get(key)
                if rate is not None and rate > 0.25:
                    failures.append({
                        "candidate_id": candidate_id, "suite": suite,
                        "unanswerable_rate": round(rate, 3),
                    })
        return failures[:12]

    def _corpus_profile(self) -> dict[str, Any]:
        goals = [len(row["state_before"]["goals"]) for row in self.dev]
        declarations = [
            sum(len(goal["local_context"]) for goal in row["state_before"]["goals"])
            for row in self.dev
        ]
        applicability = semantic_mutations.applicability(self.mutation_sample)
        return {
            "dev_transitions": len(self.dev),
            "validation_transitions": len(self.validation),
            # The population profile above is not what anything is measured on. These are.
            "sampling": "STRUCTURALLY_STRATIFIED_BY_GOAL_COUNT",
            "dev_sample_profile": sample_profile(self.dev_sample),
            "mutation_sample_profile": sample_profile(self.mutation_sample),
            "mean_goals_per_state": round(sum(goals) / max(1, len(goals)), 3),
            "max_goals_per_state": max(goals) if goals else 0,
            "multi_goal_share": round(
                sum(1 for value in goals if value >= 2) / max(1, len(goals)), 3),
            "mean_local_declarations": round(
                sum(declarations) / max(1, len(declarations)), 2),
            "mutation_applicability": {
                family: row["share"] for family, row in applicability.items()
            },
        }

    def _unmeasurable_axes(self) -> list[str]:
        """Axes whose single-axis mutations never changed the measurement."""

        attempts: dict[str, int] = {}
        effective: dict[str, int] = {}
        for record in self.registry.accepted():
            if not record.hypothesis or not record.parents or not record.metrics:
                continue
            axis = record.hypothesis.get("axis")
            parent = self.registry.get(record.parents[0])
            if not axis or parent is None or not parent.metrics:
                continue
            attempts[axis] = attempts.get(axis, 0) + 1
            changed = any(
                abs(record.metrics.get(key, 0.0) - parent.metrics.get(key, 0.0)) > 1e-9
                for key in self.selection_axes
            )
            if changed:
                effective[axis] = effective.get(axis, 0) + 1
        return sorted(
            axis for axis, count in attempts.items()
            if count >= 3 and effective.get(axis, 0) == 0
        )

    def _unresolved(self) -> list[str]:
        questions: list[str] = []
        profile = self._corpus_profile()
        if profile["multi_goal_share"] < 0.15:
            questions.append(
                f"only {profile['multi_goal_share']:.0%} of dev states have 2+ goals, so "
                "goal-ordering axes are weakly identified"
            )
        for family, share in profile["mutation_applicability"].items():
            if share < 0.05:
                questions.append(
                    f"semantic mutation {family} applies to {share:.0%} of states, so the "
                    "corruption it tests is barely measured"
                )
        return questions[:6]

    # ------------------------------------------------------------------------- proposals
    def collect_proposals(self, report: ScientistReport) -> dict[str, Any]:
        summary: dict[str, Any] = {"by_backend": {}, "accepted": 0, "rejected": 0}
        accepted: list[Any] = []
        for backend in self.backends:
            batch = backend.propose(report)
            summary["by_backend"][backend.name] = {
                "accepted": len(batch.accepted),
                "rejected": len(batch.rejected),
                "types": sorted({p.proposal_type for p in batch.accepted}),
                "rejection_reasons": [r["reason"][:120] for r in batch.rejected[:4]],
            }
            summary["accepted"] += len(batch.accepted)
            summary["rejected"] += len(batch.rejected)
            accepted.extend(batch.accepted)
            self._record_proposals(batch)
        summary["proposals"] = accepted
        return summary

    def _record_proposals(self, batch) -> None:
        self.proposals_path.parent.mkdir(parents=True, exist_ok=True)
        with self.proposals_path.open("a", encoding="utf-8") as handle:
            for proposal in batch.accepted:
                handle.write(json.dumps(
                    {**proposal.to_dict(), "outcome": "ACCEPTED"}, sort_keys=True) + "\n")
            for rejection in batch.rejected:
                handle.write(json.dumps({
                    "outcome": "REJECTED", "generation": self.generation,
                    "reason": rejection["reason"],
                }, sort_keys=True) + "\n")

    def apply_proposals(self, proposals: list[Any]) -> tuple[list[str], list[str]]:
        """Turn validated proposals into candidates, and invented axes into genome axes."""

        new_axes: list[str] = []
        children: list[str] = []
        known = {axis.name for axis in AXES} | set(self.primitives.primitives)

        for proposal in proposals:
            payload = proposal.payload
            kind = proposal.proposal_type

            if kind in ("NEW_AXIS", "NEW_PRIMITIVE"):
                primitive, reason = self.primitives.consider(
                    payload, proposal.proposal_id, self.generation, proposal.source, known)
                if primitive is None:
                    continue
                self.primitives.register(primitive)
                # Enforce acceptance condition 6: an axis that changes nothing is not an
                # axis. Registering first and checking after is deliberate -- the check
                # needs the axis present so the compiler can run its hook.
                parent_for_test = self.registry.get(
                    self.population[0]) if self.population else None
                base_genome = (
                    parent_for_test.genome if parent_for_test else RepresentationGenome({}))
                factory = lambda invented: build(base_genome, invented, self.primitives)  # noqa: E731
                probe = self.microtest_sample[:3]
                observable, evidence = self.primitives.has_observable_effect(
                    primitive, factory, probe)
                if not observable:
                    self.primitives.reject_inert(primitive, evidence)
                    continue
                # An axis that changes the rendering can still be an axis the genome already
                # has, under a new name. Nine of the first thirty accepted axes were.
                duplicate_of, duplicate_evidence = self.primitives.duplicates_an_existing_axis(
                    primitive, factory, probe)
                if duplicate_of is not None:
                    self.primitives.reject_duplicate(primitive, duplicate_evidence)
                    continue
                known.add(primitive.axis_name)
                new_axes.append(primitive.axis_name)
                # Immediately create a candidate that exercises the new axis against the
                # best current elite, or the axis is registered but never tested.
                parent_id = self.population[0] if self.population else None
                parent = self.registry.get(parent_id) if parent_id else None
                if parent is not None:
                    for value in primitive.values:
                        if value == "NONE":
                            continue
                        child = self._invented_child(parent, primitive.axis_name, value,
                                                     proposal)
                        if child:
                            children.append(child)
                continue

            if kind == "AXIS_MUTATION":
                child = self._axis_child(payload, proposal)
                if child:
                    children.append(child)
            elif kind == "ARCHITECTURAL_HYPOTHESIS":
                child = self._architectural_child(payload, proposal)
                if child:
                    children.append(child)
        return children, new_axes

    def _blocked(self, axis: str, value: str) -> bool:
        allowed, _reason = self.memory.may_apply(axis, value)
        return not allowed

    def _axis_child(self, payload: dict[str, Any], proposal) -> str | None:
        parent = self.registry.get(payload["parent_id"])
        if parent is None:
            return None
        axis, value = payload["axis"], payload["value"]
        if axis in self.primitives.primitives:
            return self._invented_child(parent, axis, value, proposal)
        if self._blocked(axis, value):
            return None
        try:
            genome = parent.genome.with_values(**{axis: value})
        except ValueError:
            return None
        return self._register_child(genome, parent, proposal, payload, "AXIS_MUTATION")

    def _architectural_child(self, payload: dict[str, Any], proposal) -> str | None:
        parent = self.registry.get(payload["parent_id"])
        if parent is None:
            return None
        changes = {
            axis: value for axis, value in payload["changes"].items()
            if axis not in self.primitives.primitives and not self._blocked(axis, value)
        }
        if not changes:
            return None
        try:
            genome = parent.genome.with_values(**changes)
        except ValueError:
            return None
        return self._register_child(
            genome, parent, proposal, payload, "ARCHITECTURAL_HYPOTHESIS")

    def _invented_child(self, parent: CandidateRecord, axis: str, value: str, proposal) -> str | None:
        invented = dict(self.invented.get(parent.candidate_id, {}))
        invented[axis] = value
        extended = ExtendedGenome(parent.genome, invented)
        candidate_id = extended.candidate_id()
        if candidate_id in self.registry:
            return None
        self.registry.add(CandidateRecord(
            candidate_id=candidate_id, genome=parent.genome,
            generation=self.generation + 1, origin="INVENTED_AXIS",
            parents=(parent.candidate_id,),
            mutation={"axis": axis, "value": value, "proposal_id": proposal.proposal_id},
            hypothesis={
                "axis": axis, "to_value": value, "from_value": "NONE",
                "target_metric": _target_metric(proposal.payload),
                "statement": proposal.payload.get("hypothesis", ""),
                "mechanism": proposal.payload.get("mechanism", ""),
                "source": proposal.source,
            },
        ))
        self.invented[candidate_id] = invented
        return candidate_id

    def _register_child(
        self, genome: RepresentationGenome, parent: CandidateRecord, proposal,
        payload: dict[str, Any], origin: str,
    ) -> str | None:
        candidate_id = genome.candidate_id()
        if candidate_id in self.registry:
            return None
        inherited = self.invented.get(parent.candidate_id)
        self.registry.add(CandidateRecord(
            candidate_id=candidate_id, genome=genome,
            generation=self.generation + 1, origin=origin,
            parents=(parent.candidate_id,),
            mutation={"proposal_id": proposal.proposal_id, "payload": payload},
            hypothesis={
                "axis": payload.get("axis"),
                "from_value": parent.genome.get(payload["axis"]) if payload.get("axis") else None,
                "to_value": payload.get("value"),
                "target_metric": _target_metric(payload),
                "statement": payload.get("hypothesis", ""),
                "mechanism": payload.get("mechanism", ""),
                "source": proposal.source,
            },
        ))
        if inherited:
            self.invented[candidate_id] = dict(inherited)
        return candidate_id

    # ---------------------------------------------------------------------- one generation
    def step(self) -> GenerationReportV2:
        started = time.monotonic()
        if self.generation == 0 and not self.population:
            self.seed()

        evaluated, killed, ladder = self.evaluate(list(self.population))
        population = [
            (record.candidate_id, record.metrics or {})
            for record in self.registry.accepted()
            if record.candidate_id in set(evaluated)
        ]
        genomes = {record.candidate_id: record.genome for record in self.registry}
        verdicts = self.validate_children(evaluated)
        # Before anything is selected on, check that every selection axis still separates
        # candidates. An axis that does not is removed here, not after the run.
        demotions = self.enforce_discrimination()

        eligible = [
            (candidate_id, values) for candidate_id, values in population
            if not self.quarantine.is_quarantined(candidate_id)
        ]
        selection = select(
            eligible or population, genomes, self.config.population_capacity,
            pinned=[cid for cid in self.pinned if cid in dict(population)],
            novelty_slots=self.config.novelty_slots, axes=self.selection_axes,
        )
        signature = frontier_signature(eligible or population, self.selection_axes)
        moved = self.last_signature is None or any(
            old - new > max(1e-9, self.config.material_improvement * abs(old))
            for new, old in zip(signature, self.last_signature)
        )
        self.stall_count = 0 if moved else self.stall_count + 1
        self.last_signature = signature

        report = self.build_report(selection.front, evaluated)
        proposal_summary = self.collect_proposals(report)
        children, new_axes = self.apply_proposals(proposal_summary.pop("proposals", []))

        # Structural convergence, evaluated only once everything that could move this
        # generation has moved: the frontier's position, its membership, and the size of the
        # space it was searched in.
        front_now = tuple(sorted(selection.front))
        membership_stable = self.last_front is not None and front_now == self.last_front
        space_stable = not new_axes
        if (not moved) and membership_stable and space_stable:
            self.structural_stall += 1
        else:
            self.structural_stall = 0
        self.last_front = front_now

        self.population = selection.survivors + children[: self.config.children_per_generation]
        generation_report = GenerationReportV2(
            generation=self.generation, evaluated=evaluated, killed=killed,
            front=selection.front, survivors=selection.survivors,
            proposals=proposal_summary, new_axes=new_axes,
            validation_verdicts=verdicts,
            frontier_signature=[round(value, 6) for value in signature],
            frontier_moved=moved, genome_schema=self.primitives.schema_version,
            elapsed_seconds=time.monotonic() - started, ladder=ladder,
            selection_axes=list(self.selection_axes), axis_demotions=demotions,
        )
        self._write_generation(generation_report)
        self.history.append({
            "generation": self.generation, "evaluated": len(evaluated),
            "killed": len(killed), "front": len(selection.front),
            "new_axes": new_axes, "moved": moved, "stall": self.stall_count,
            "structural_stall": self.structural_stall,
            "demoted_axes": [item["axis"] for item in demotions
                             if item["action"] == "DEMOTED_TO_DIAGNOSTIC"],
        })
        self.generation += 1
        self.save()
        return generation_report

    def _write_generation(self, report: GenerationReportV2) -> None:
        self.generations_dir.mkdir(parents=True, exist_ok=True)
        payload = report.to_dict()
        payload["population_after"] = self.population
        payload["metrics"] = {
            candidate_id: self.registry.get(candidate_id).metrics
            for candidate_id in report.evaluated
            if self.registry.get(candidate_id) is not None
        }
        payload["space_size"] = f"{space_size(extended_space(self.primitives)):.3e}"
        (self.generations_dir / f"generation_{report.generation:03d}.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")

    def converged(self) -> tuple[bool, str]:
        """Has the search structurally converged, or has it merely run out of budget?

        These are different outcomes and the distinction is the whole point of the return
        value. The first V2 run stopped at its generation budget with the frontier still
        moving and reported ``STRUCTURAL_CONVERGENCE: NO``; that honesty must survive
        contact with a controller that is asked to "run to convergence", so the budget is a
        safety cap whose reason string says, in as many words, that it is not convergence.

        Convergence requires three things to hold together for ``stall_limit`` consecutive
        generations, because any one of them alone is satisfiable by a search that is still
        making progress:

        * the frontier did not improve materially on any selection axis;
        * the frontier's *membership* did not change -- a frontier swapping candidates at a
          fixed signature is still exploring. Measured: this clause looked unsatisfiable at
          generation 70, where entrants averaged 2.3 per generation with no visible trend.
          It was satisfiable; churn kept declining and reached zero. Generations 101-105 had
          no entrant and no departure, and the search converged at 106. An extrapolation from
          a mid-run churn rate is not evidence that a criterion cannot be met;
        * no new axis entered the genome -- a search that is still growing its own space has
          not finished searching the space it has.
        """

        if self.structural_stall >= self.config.stall_limit:
            return True, (
                f"STRUCTURAL_CONVERGENCE: frontier position, frontier membership and genome "
                f"size all unchanged for {self.structural_stall} consecutive generations"
            )
        if self.generation >= self.config.max_generations:
            return True, (
                f"GENERATION_CAP_REACHED_NOT_CONVERGED: stopped at the safety cap of "
                f"{self.config.max_generations} generations with structural_stall="
                f"{self.structural_stall} of {self.config.stall_limit} required; the search "
                f"had not converged"
            )
        return False, "SEARCHING"

    def convergence_state(self) -> dict[str, Any]:
        """Everything a report needs to say whether the stop was convergence or a cap."""

        done, reason = self.converged()
        return {
            "generation": self.generation,
            "stopped": done,
            "reason": reason,
            "structurally_converged": self.structural_stall >= self.config.stall_limit,
            "structural_stall": self.structural_stall,
            "stall_limit": self.config.stall_limit,
            "signature_stall": self.stall_count,
            "max_generations_safety_cap": self.config.max_generations,
            "selection_axes": list(self.selection_axes),
            "demoted_axes": self.demoted_axes,
        }

    def run(self, generations: int) -> list[GenerationReportV2]:
        reports: list[GenerationReportV2] = []
        for _ in range(generations):
            done, _reason = self.converged()
            if done:
                break
            reports.append(self.step())
        return reports

    def finalists(self) -> tuple[list[str], dict[str, list[str]]]:
        population = [
            (record.candidate_id, record.metrics or {})
            for record in self.registry.accepted()
            if not self.quarantine.is_quarantined(record.candidate_id)
        ]
        return shortlist(population, self.selection_axes)


def _target_metric(payload: dict[str, Any]) -> str:
    named = payload.get("target_metric")
    if named in SELECTION_AXES:
        return named
    return "bpe_tokens_per_transition"


def _encode_rng(state: tuple) -> list[Any]:
    return [state[0], list(state[1]), state[2]]


def _decode_rng(state: list[Any]) -> tuple:
    return (state[0], tuple(state[1]), state[2])
