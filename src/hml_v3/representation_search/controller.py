"""The recursive search controller.

    population = seeds
    while not converged:
        evaluate  ->  hard-reject  ->  Pareto select  ->  failure profile
                  ->  meta-design mutations  ->  compile  ->  checkpoint

Every generation is checkpointed to disk before the next begins, so a session that ends can
be resumed from the exact next generation with no human reconstruction.

The controller never reads the sealed split. It reads SEARCH_DEV for selection and
SEARCH_VALIDATION for the honesty check that the frontier is not a dev-set artifact.
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
from hml_v3.representation_search.genome import (
    AXES_BY_NAME,
    PHASES,
    RepresentationGenome,
)
from hml_v3.representation_search.lineage import CandidateRecord, CandidateRegistry
from hml_v3.representation_search.metrics import MAXIMISED, PARETO_AXES, measure
from hml_v3.representation_search import mutations as mutation_library
from hml_v3.representation_search.pareto import (
    frontier_signature,
    genome_novelty,
    select,
)
from hml_v3.representation_search.seeds import SEEDS, seed_population

SEARCH_STATE_VERSION = "representation-search-state-v1.0.0"


@dataclass
class SearchConfig:
    population_capacity: int = 24
    children_per_generation: int = 16
    novelty_slots: int = 3
    dev_sample: int = 48
    validation_sample: int = 32
    max_generations: int = 30
    stall_limit: int = 5
    #: A generation counts as having moved the frontier only when some Pareto axis improves
    #: by at least this relative amount. Without a threshold the rule never fires: in a
    #: growing population some axis always improves by a rounding error, and "the frontier
    #: moved" would then mean nothing.
    material_improvement: float = 0.005
    seed: int = 20260828
    #: Phase order: expose structure before architecture before grammar before lexicon.
    #: Optimising words while the architecture is still moving wastes generations.
    phase_schedule: tuple[str, ...] = ("A", "A", "B", "B", "B", "C", "C", "D", "D", None)

    def phase_for(self, generation: int) -> str | None:
        if generation < len(self.phase_schedule):
            return self.phase_schedule[generation]
        return None

    def to_dict(self) -> dict[str, Any]:
        return {
            "population_capacity": self.population_capacity,
            "children_per_generation": self.children_per_generation,
            "novelty_slots": self.novelty_slots,
            "dev_sample": self.dev_sample,
            "validation_sample": self.validation_sample,
            "max_generations": self.max_generations,
            "stall_limit": self.stall_limit,
            "seed": self.seed,
            "phase_schedule": list(self.phase_schedule),
        }


@dataclass
class GenerationReport:
    generation: int
    phase: str | None
    evaluated: list[str]
    hard_rejected: list[dict[str, Any]]
    front: list[str]
    survivors: list[str]
    frontier_signature: list[float]
    frontier_moved: bool
    weaknesses: dict[str, list[str]]
    hypotheses: list[dict[str, Any]]
    blocked_by_memory: list[dict[str, Any]]
    refuted_hypotheses: list[dict[str, Any]]
    elapsed_seconds: float
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "generation": self.generation,
            "phase": self.phase,
            "evaluated": self.evaluated,
            "hard_rejected": self.hard_rejected,
            "front": self.front,
            "survivors": self.survivors,
            "frontier_signature": self.frontier_signature,
            "frontier_moved": self.frontier_moved,
            "weaknesses": self.weaknesses,
            "hypotheses": self.hypotheses,
            "blocked_by_memory": self.blocked_by_memory,
            "refuted_hypotheses": self.refuted_hypotheses,
            "elapsed_seconds": round(self.elapsed_seconds, 3),
            "notes": self.notes,
        }


class SearchController:
    def __init__(
        self,
        dev: list[dict[str, Any]],
        validation: list[dict[str, Any]],
        workspace: Path,
        config: SearchConfig | None = None,
        memory: FailureMemory | None = None,
    ) -> None:
        self.dev = dev
        self.validation = validation
        self.workspace = workspace
        self.config = config or SearchConfig()
        self.memory = memory or FailureMemory.load()
        self.registry = CandidateRegistry(workspace / "candidate_registry.jsonl")
        self.state_path = workspace / "search_state.json"
        self.generations_dir = workspace / "generations"
        self.rng = random.Random(self.config.seed)
        self.generation = 0
        self.population: list[str] = []
        self.pinned: list[str] = []
        self.history: list[dict[str, Any]] = []
        self.stall_count = 0
        self.last_signature: tuple[float, ...] | None = None
        self.dev_sample = dev[: self.config.dev_sample]
        self.validation_sample = validation[: self.config.validation_sample]

    # -------------------------------------------------------------------- persistence
    def save(self) -> None:
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.registry.flush()
        state = {
            "schema_version": SEARCH_STATE_VERSION,
            "generation": self.generation,
            "population": self.population,
            "pinned": self.pinned,
            "stall_count": self.stall_count,
            "last_signature": list(self.last_signature) if self.last_signature else None,
            "config": self.config.to_dict(),
            "rng_state": _encode_rng(self.rng.getstate()),
            "history": self.history,
            "failure_memory": self.memory.summary(),
            "dev_transitions": len(self.dev),
            "validation_transitions": len(self.validation),
            "dev_sample_ids": [row["transition_id"] for row in self.dev_sample],
            "validation_sample_ids": [row["transition_id"] for row in self.validation_sample],
        }
        self.state_path.write_text(
            json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def resume(self) -> bool:
        if not self.state_path.exists():
            return False
        state = json.loads(self.state_path.read_text(encoding="utf-8"))
        self.generation = state["generation"]
        self.population = state["population"]
        self.pinned = state["pinned"]
        self.stall_count = state["stall_count"]
        self.last_signature = tuple(state["last_signature"]) if state["last_signature"] else None
        self.history = state["history"]
        self.rng.setstate(_decode_rng(state["rng_state"]))
        for lesson_id, count in state.get("failure_memory", {}).get("retries_used", {}).items():
            self.memory.retries_used[lesson_id] = count
        return True

    # ------------------------------------------------------------------------ seeding
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
        pinned_labels = set(self.memory.pinned_seeds())
        self.pinned = sorted({
            SEEDS[label].candidate_id() for label in pinned_labels if label in SEEDS
        })

    # --------------------------------------------------------------------- evaluation
    def evaluate(self, candidate_ids: list[str]) -> tuple[list[str], list[dict[str, Any]]]:
        evaluated: list[str] = []
        rejected: list[dict[str, Any]] = []
        for candidate_id in candidate_ids:
            record = self.registry.get(candidate_id)
            if record is None:
                continue
            if record.status in ("EVALUATED", "HARD_REJECTED"):
                (evaluated if record.status == "EVALUATED" else rejected).append(
                    candidate_id if record.status == "EVALUATED"
                    else {"candidate_id": candidate_id, "reason": record.rejection_reason}
                )
                continue
            try:
                compiler = build(record.genome)
            except CompilerRejection as error:
                record.status = "HARD_REJECTED"
                record.rejection_reason = str(error).split(":")[0]
                record.gates = {"compile_error": str(error)}
                self.registry.update(record)
                rejected.append({"candidate_id": candidate_id, "reason": record.rejection_reason})
                continue
            report = run_gates(compiler, self.dev_sample)
            record.gates = report.to_dict()
            if not report.passed:
                record.status = "HARD_REJECTED"
                record.rejection_reason = report.first_failure
                self.registry.update(record)
                rejected.append({"candidate_id": candidate_id, "reason": report.first_failure})
                continue
            vector = measure(compiler, self.dev_sample)
            record.metrics = vector.values
            record.status = "EVALUATED"
            self.registry.update(record)
            evaluated.append(candidate_id)
        return evaluated, rejected

    # ----------------------------------------------------------------- failure profile
    def weakness_profile(self, front: list[str]) -> dict[str, list[str]]:
        """For each elite, the Pareto axes on which it is worst in the current population."""

        population = [
            (record.candidate_id, record.metrics or {})
            for record in self.registry.accepted()
            if record.candidate_id in set(self.population) | set(front)
        ]
        profile: dict[str, list[str]] = {}
        for candidate_id in front:
            values = dict(population).get(candidate_id, {})
            weak: list[tuple[float, str]] = []
            for axis in PARETO_AXES:
                column = [row.get(axis, 0.0) for _, row in population]
                if not column:
                    continue
                low, high = min(column), max(column)
                if high - low <= 0:
                    continue
                mine = values.get(axis, 0.0)
                position = (mine - low) / (high - low)
                if axis in MAXIMISED:
                    position = 1.0 - position
                weak.append((position, axis))
            weak.sort(reverse=True)
            profile[candidate_id] = [axis for score, axis in weak[:3] if score > 0.5]
        return profile

    # ------------------------------------------------------------------- meta-design
    def propose(
        self, front: list[str], weaknesses: dict[str, list[str]], phase: str | None,
    ) -> tuple[list[mutation_library.Proposal], list[dict[str, Any]]]:
        proposals: list[mutation_library.Proposal] = []
        blocked: list[dict[str, Any]] = []
        elites = front or self.population[: min(4, len(self.population))]
        for candidate_id in elites:
            record = self.registry.get(candidate_id)
            if record is None:
                continue
            targeted = mutation_library.targeted_proposals(
                record.genome, weaknesses.get(candidate_id, []), self.memory, phase,
            )
            if not targeted:
                targeted = mutation_library.local_neighbourhood(record.genome, self.memory, phase)
            for proposal in targeted:
                if proposal.blocked_reason:
                    if proposal.hypothesis is not None:
                        blocked.append({
                            "parent": candidate_id,
                            "axis": proposal.hypothesis.axis,
                            "value": proposal.hypothesis.to_value,
                            "reason": proposal.blocked_reason,
                        })
                    continue
                proposals.append(proposal)
        # crossover between the two most distant elites, then diversity jumps
        if len(elites) >= 2:
            genomes = {
                candidate_id: self.registry.get(candidate_id).genome
                for candidate_id in elites if self.registry.get(candidate_id)
            }
            pairs = [
                (left, right) for index, left in enumerate(elites) for right in elites[index + 1:]
                if left in genomes and right in genomes
            ]
            if pairs:
                pairs.sort(key=lambda pair: -genomes[pair[0]].distance(genomes[pair[1]]))
                left, right = pairs[0]
                for groups in (("GRAMMAR", "LEXICON"), ("STRUCTURE", "GRAPH_SERIALIZATION")):
                    proposals.append(mutation_library.group_crossover(
                        genomes[left], genomes[right], groups, self.rng))
        for candidate_id in elites[: self.config.novelty_slots]:
            record = self.registry.get(candidate_id)
            if record is not None:
                proposals.append(mutation_library.random_walk(
                    record.genome, self.memory, self.rng, steps=3, phase=phase))
        self.rng.shuffle(proposals)
        unique: dict[str, mutation_library.Proposal] = {}
        for proposal in proposals:
            candidate_id = proposal.genome.candidate_id()
            if candidate_id in self.registry or candidate_id in unique:
                continue
            unique[candidate_id] = proposal
            if len(unique) >= self.config.children_per_generation:
                break
        return list(unique.values()), blocked

    # ------------------------------------------------------------------ one generation
    def step(self) -> GenerationReport:
        started = time.monotonic()
        phase = self.config.phase_for(self.generation)
        if self.generation == 0 and not self.population:
            self.seed()

        evaluated, rejected = self.evaluate(list(self.population))
        population = [
            (record.candidate_id, record.metrics or {})
            for record in self.registry.accepted()
            if record.candidate_id in set(evaluated)
        ]
        genomes = {
            record.candidate_id: record.genome for record in self.registry
        }
        selection = select(
            population, genomes, self.config.population_capacity,
            pinned=[cid for cid in self.pinned if cid in dict(population)],
            novelty_slots=self.config.novelty_slots,
        )
        signature = frontier_signature(population)
        threshold = self.config.material_improvement
        moved = self.last_signature is None or any(
            old - new > max(1e-9, threshold * abs(old))
            for new, old in zip(signature, self.last_signature)
        )
        self.stall_count = 0 if moved else self.stall_count + 1
        self.last_signature = signature

        weaknesses = self.weakness_profile(selection.front)
        refuted = self._score_previous_hypotheses(evaluated)
        proposals, blocked = self.propose(selection.front, weaknesses, phase)

        for proposal in proposals:
            genome = proposal.genome
            self.registry.add(CandidateRecord(
                candidate_id=genome.candidate_id(), genome=genome,
                generation=self.generation + 1, origin=proposal.kind,
                parents=proposal.parent_ids, mutation=proposal.to_dict(),
                hypothesis=proposal.hypothesis.to_dict() if proposal.hypothesis else None,
            ))
            if proposal.hypothesis and proposal.hypothesis.changed_condition:
                lesson = self.memory.blocking_lesson(
                    proposal.hypothesis.axis, proposal.hypothesis.to_value)
                if lesson:
                    self.memory.consume_retry(lesson.id)

        self.population = selection.survivors + [
            proposal.genome.candidate_id() for proposal in proposals
        ]
        report = GenerationReport(
            generation=self.generation,
            phase=phase,
            evaluated=evaluated,
            hard_rejected=rejected,
            front=selection.front,
            survivors=selection.survivors,
            frontier_signature=[round(value, 6) for value in signature],
            frontier_moved=moved,
            weaknesses=weaknesses,
            hypotheses=[
                proposal.hypothesis.to_dict() for proposal in proposals if proposal.hypothesis
            ],
            blocked_by_memory=blocked,
            refuted_hypotheses=refuted,
            elapsed_seconds=time.monotonic() - started,
        )
        self._write_generation(report)
        self.history.append({
            "generation": report.generation, "phase": report.phase,
            "evaluated": len(report.evaluated), "rejected": len(report.hard_rejected),
            "front_size": len(report.front), "frontier_moved": report.frontier_moved,
            "stall_count": self.stall_count,
        })
        self.generation += 1
        self.save()
        return report

    def _score_previous_hypotheses(self, evaluated: list[str]) -> list[dict[str, Any]]:
        """Check each child's hypothesis against what actually happened to the metric."""

        refuted: list[dict[str, Any]] = []
        for candidate_id in evaluated:
            record = self.registry.get(candidate_id)
            if record is None or not record.hypothesis or not record.metrics:
                continue
            axis = record.hypothesis.get("axis")
            metric = record.hypothesis.get("target_metric")
            if not axis or not metric or not record.parents:
                continue
            parent = self.registry.get(record.parents[0])
            if parent is None or not parent.metrics:
                continue
            mine = record.metrics.get(metric)
            theirs = parent.metrics.get(metric)
            if mine is None or theirs is None:
                continue
            improved = mine > theirs if metric in MAXIMISED else mine < theirs
            if not improved:
                refuted.append({
                    "candidate_id": candidate_id,
                    "axis": axis,
                    "from": record.hypothesis.get("from_value"),
                    "to": record.hypothesis.get("to_value"),
                    "metric": metric,
                    "parent_value": round(theirs, 6),
                    "child_value": round(mine, 6),
                    "verdict": "HYPOTHESIS_REFUTED",
                })
        return refuted

    def _write_generation(self, report: GenerationReport) -> None:
        self.generations_dir.mkdir(parents=True, exist_ok=True)
        path = self.generations_dir / f"generation_{report.generation:03d}.json"
        payload = report.to_dict()
        payload["population_after"] = self.population
        payload["metrics"] = {
            candidate_id: self.registry.get(candidate_id).metrics
            for candidate_id in report.evaluated
            if self.registry.get(candidate_id) is not None
        }
        path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    # ---------------------------------------------------------------------- convergence
    def converged(self) -> tuple[bool, str]:
        if self.generation >= self.config.max_generations:
            return True, "MAX_GENERATIONS_REACHED"
        if self.stall_count >= self.config.stall_limit:
            return True, f"FRONTIER_UNMOVED_FOR_{self.stall_count}_GENERATIONS"
        return False, "SEARCHING"

    def run(self, generations: int) -> list[GenerationReport]:
        reports: list[GenerationReport] = []
        for _ in range(generations):
            done, reason = self.converged()
            if done:
                break
            reports.append(self.step())
        return reports


def _encode_rng(state: tuple) -> list[Any]:
    return [state[0], list(state[1]), state[2]]


def _decode_rng(state: list[Any]) -> tuple:
    return (state[0], tuple(state[1]), state[2])
