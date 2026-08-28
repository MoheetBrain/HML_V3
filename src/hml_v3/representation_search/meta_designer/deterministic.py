"""The rule-based meta-designer, preserved as a control.

This backend reproduces the V1 controller's behaviour behind the new interface: it mutates
existing axes according to a hard-coded causal model. It is kept for two reasons — it is
free, and it is the baseline the model-driven backend has to beat. If the LLM backend never
proposes anything this one could not have, the open-endedness is decorative and the reports
should say so.
"""

from __future__ import annotations

import random
from typing import Any

from hml_v3.representation_search.meta_designer.base import (
    MetaDesignerBackend,
    ProposalBatch,
    ScientistReport,
)
from hml_v3.representation_search.mutations import AXIS_MECHANISM


class DeterministicMetaDesigner(MetaDesignerBackend):
    name = "deterministic"

    def __init__(self, seed: int = 20260828, per_elite: int = 4) -> None:
        self.rng = random.Random(seed)
        self.per_elite = per_elite

    def propose(self, report: ScientistReport) -> ProposalBatch:
        payloads: list[dict[str, Any]] = []
        for elite in report.elites[:6]:
            weaknesses = set(elite.get("weaknesses") or [])
            genome = elite.get("genome") or {}
            targeted = [
                axis for axis, (metric, _mechanism) in AXIS_MECHANISM.items()
                if metric in weaknesses and axis in report.genome_axes
            ]
            if not targeted:
                targeted = [axis for axis in report.genome_axes if axis in AXIS_MECHANISM]
            self.rng.shuffle(targeted)
            for axis in targeted[: self.per_elite]:
                values = [
                    value for value in report.genome_axes[axis]
                    if value != genome.get(axis)
                ]
                if not values:
                    continue
                metric, mechanism = AXIS_MECHANISM.get(
                    axis, ("bpe_tokens_per_transition", "no recorded causal mechanism"))
                payloads.append({
                    "proposal_type": "AXIS_MUTATION",
                    "parent_id": elite["candidate_id"],
                    "axis": axis,
                    "value": self.rng.choice(values),
                    "target_metric": metric,
                    "hypothesis": (
                        f"changing {axis} from {genome.get(axis)} improves {metric} on this "
                        "corpus"
                    ),
                    "mechanism": mechanism,
                    "falsification": (
                        f"reject if {metric} does not improve against the parent"
                    ),
                })
        # The rule-based backend can also notice an unmeasurable axis, but only because the
        # report tells it which ones they are; it cannot invent a new axis.
        for axis in report.unmeasurable_axes[:2]:
            payloads.append({
                "proposal_type": "CORPUS_ACQUISITION",
                "reason": (
                    f"axis {axis} did not change the measurement on any mutation, so the "
                    "corpus cannot identify it"
                ),
                "stratum": "goal_count" if "goal" in axis or "graph" in axis else "context_size",
                "values": ["2", "3-5", ">5"] if "goal" in axis or "graph" in axis else ["31+"],
                "desired_per_value": 200,
            })
        return self._validate_all(payloads, report)
