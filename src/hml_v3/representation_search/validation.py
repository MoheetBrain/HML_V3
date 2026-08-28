"""Validation as a gate on eliteness, not a report printed afterwards.

In V1 the controller received `SEARCH_VALIDATION` and then selected on `SEARCH_DEV` metrics
anyway. A mutation that improved the dev sample entered the elite population whether or not
the improvement was real, which is how a search overfits its own instrument.

Here a child may only become an elite if the improvement it claimed on dev is *directionally
reproduced* on validation, within a tolerance fixed before the comparison. A mutation that
improves dev by 30% and worsens validation by 8% is not a discovery; it is a
`NON_GENERALIZING_MUTATION`, and it is quarantined and recorded as one.

Validation is never optimised against directly: it returns a verdict and a divergence number,
not a gradient. Nothing here reads the sealed split.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from hml_v3.representation_search.metrics import MAXIMISED

#: Preregistered before any result was seen.
DEFAULT_TOLERANCE = 0.5      # validation may retain as little as half the dev gain
DEFAULT_NOISE_FLOOR = 0.01   # relative changes under 1% are treated as no change

QUARANTINED = "NON_GENERALIZING_MUTATION"
REPRODUCED = "REPRODUCED_ON_VALIDATION"
NEUTRAL = "NO_CLAIM_TO_REPRODUCE"
REGRESSED = "VALIDATION_CONTRADICTS_DEV"
#: The hypothesis simply failed, on both splits, consistently. That is not a generalization
#: problem and must not be treated as one: the candidate may still be Pareto-useful on another
#: axis, and that is the selector's decision to make, not this gate's.
FAILED_ON_BOTH = "HYPOTHESIS_FAILED_CONSISTENTLY"


@dataclass
class DivergenceVerdict:
    candidate_id: str
    metric: str
    dev_change: float
    validation_change: float
    verdict: str
    divergence: float
    detail: dict[str, Any] = field(default_factory=dict)

    @property
    def elite_eligible(self) -> bool:
        """Only a dev-set claim that failed to replicate blocks eliteness.

        A candidate whose target metric got worse on both splits is not quarantined here: it
        is simply a worse candidate on that axis, and Pareto selection is what should decide
        whether it survives on the others.
        """

        return self.verdict in (REPRODUCED, NEUTRAL, FAILED_ON_BOTH)

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "metric": self.metric,
            "dev_change": round(self.dev_change, 5),
            "validation_change": round(self.validation_change, 5),
            "divergence": round(self.divergence, 5),
            "verdict": self.verdict,
            "elite_eligible": self.elite_eligible,
            "detail": self.detail,
        }


def _relative(before: float, after: float) -> float:
    if abs(before) < 1e-12:
        return 0.0
    return (after - before) / abs(before)


def _improvement(metric: str, before: float, after: float) -> float:
    """Signed improvement: positive means better, whichever way the metric points."""

    change = _relative(before, after)
    return change if metric in MAXIMISED else -change


def assess(
    candidate_id: str, metric: str,
    parent_dev: dict[str, float], child_dev: dict[str, float],
    parent_validation: dict[str, float], child_validation: dict[str, float],
    tolerance: float = DEFAULT_TOLERANCE,
    noise_floor: float = DEFAULT_NOISE_FLOOR,
) -> DivergenceVerdict:
    """Did the dev-set claim reproduce on data selection never used?"""

    dev_gain = _improvement(
        metric, parent_dev.get(metric, 0.0), child_dev.get(metric, 0.0))
    validation_gain = _improvement(
        metric, parent_validation.get(metric, 0.0), child_validation.get(metric, 0.0))
    divergence = dev_gain - validation_gain

    if abs(dev_gain) < noise_floor:
        verdict = NEUTRAL
    elif dev_gain > 0 and validation_gain >= dev_gain * tolerance:
        verdict = REPRODUCED
    elif dev_gain > 0 and validation_gain < 0:
        verdict = REGRESSED
    elif dev_gain > 0:
        verdict = QUARANTINED
    else:
        # dev_gain is negative: the child claimed an improvement and did not get one on dev
        # either. There is no dev-set claim for validation to fail to reproduce, so this is
        # a failed hypothesis, not a generalization failure.
        verdict = FAILED_ON_BOTH

    return DivergenceVerdict(
        candidate_id=candidate_id, metric=metric,
        dev_change=dev_gain, validation_change=validation_gain,
        verdict=verdict, divergence=divergence,
        detail={
            "tolerance": tolerance, "noise_floor": noise_floor,
            "direction": "maximise" if metric in MAXIMISED else "minimise",
        },
    )


@dataclass
class ValidationPolicy:
    """The preregistered rule. Written down before results, not tuned to them."""

    tolerance: float = DEFAULT_TOLERANCE
    noise_floor: float = DEFAULT_NOISE_FLOOR
    quarantine_generations: int = 2

    def to_dict(self) -> dict[str, Any]:
        return {
            "tolerance": self.tolerance,
            "noise_floor": self.noise_floor,
            "quarantine_generations": self.quarantine_generations,
            "rule": (
                "a child enters the elite population only when the improvement it claimed on "
                "SEARCH_DEV is reproduced on SEARCH_VALIDATION at >= tolerance x the dev "
                "gain; otherwise it is quarantined and recorded as a "
                "NON_GENERALIZING_MUTATION"
            ),
            "preregistered": True,
        }


class Quarantine:
    """Candidates whose dev gains did not reproduce. Kept as evidence, not deleted."""

    def __init__(self, policy: ValidationPolicy | None = None) -> None:
        self.policy = policy or ValidationPolicy()
        self.entries: dict[str, DivergenceVerdict] = {}
        self.released: dict[str, int] = {}

    def record(self, verdict: DivergenceVerdict) -> None:
        if not verdict.elite_eligible:
            self.entries[verdict.candidate_id] = verdict

    def is_quarantined(self, candidate_id: str) -> bool:
        return candidate_id in self.entries

    def summary(self) -> dict[str, Any]:
        by_verdict: dict[str, int] = {}
        for verdict in self.entries.values():
            by_verdict[verdict.verdict] = by_verdict.get(verdict.verdict, 0) + 1
        return {
            "policy": self.policy.to_dict(),
            "quarantined": len(self.entries),
            "by_verdict": dict(sorted(by_verdict.items())),
            "worst_divergences": [
                verdict.to_dict() for verdict in
                sorted(self.entries.values(), key=lambda item: -abs(item.divergence))[:10]
            ],
        }
