"""The preregistered sequential stopping rule.

`MICROMATH §14` forbids running every item against every candidate, and forbids changing the
rule once it is clear which representation is winning. So the rule is fixed here, in code,
before any neural result exists:

* evaluate on a rung of the ladder ``20 -> 40 -> 80 -> 160`` items, truncated to what the
  split actually holds;
* at each rung compare the candidate with the best control **on the same items**, because a
  paired comparison is the only one that removes item difficulty from the contrast;
* eliminate the candidate when the 95% paired bootstrap interval of
  ``candidate - best_control`` lies entirely below zero -- that is what "clearly dominated"
  means, stated numerically;
* otherwise promote it to the next rung; survivors of the last rung are the finalists.

The bootstrap resamples *pairs*, not items, because the two items of a matched pair share a
base state and are not independent.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from typing import Any, Sequence

LADDER: tuple[int, ...] = (20, 40, 80, 160)
CONFIDENCE = 0.95
BOOTSTRAP_RESAMPLES = 2000


def _rng_stream(seed: str, count: int):
    """Deterministic pseudo-random integers. No global RNG, so a run is reproducible."""

    state = hashlib.sha256(seed.encode()).digest()
    produced = 0
    while produced < count:
        state = hashlib.sha256(state).digest()
        for index in range(0, 32, 4):
            if produced >= count:
                return
            yield int.from_bytes(state[index:index + 4], "big")
            produced += 1


@dataclass
class PairedVerdict:
    n_pairs: int
    candidate_accuracy: float
    control_accuracy: float
    difference: float
    low: float
    high: float

    @property
    def dominated(self) -> bool:
        """The whole interval sits below zero: the candidate is worse, not merely unproven."""

        return self.high < 0.0

    @property
    def superior(self) -> bool:
        return self.low > 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "n_pairs": self.n_pairs,
            "candidate_accuracy": round(self.candidate_accuracy, 4),
            "control_accuracy": round(self.control_accuracy, 4),
            "delta_best_control": round(self.difference, 4),
            "ci95_low": round(self.low, 4),
            "ci95_high": round(self.high, 4),
            "dominated": self.dominated,
            "superior": self.superior,
        }


def paired_bootstrap(
    candidate: Sequence[float], control: Sequence[float], seed: str = "micromath",
    resamples: int = BOOTSTRAP_RESAMPLES,
) -> PairedVerdict:
    """``candidate`` and ``control`` are per-pair accuracies over the same pairs."""

    count = len(candidate)
    if count == 0:
        return PairedVerdict(0, 0.0, 0.0, 0.0, 0.0, 0.0)
    differences = [c - k for c, k in zip(candidate, control)]
    observed = sum(differences) / count
    draws = list(_rng_stream(seed, resamples * count))
    means: list[float] = []
    cursor = 0
    for _ in range(resamples):
        total = 0.0
        for _ in range(count):
            total += differences[draws[cursor] % count]
            cursor += 1
        means.append(total / count)
    means.sort()
    tail = (1.0 - CONFIDENCE) / 2.0
    low = means[int(tail * (resamples - 1))]
    high = means[int((1.0 - tail) * (resamples - 1))]
    return PairedVerdict(
        n_pairs=count,
        candidate_accuracy=sum(candidate) / count,
        control_accuracy=sum(control) / count,
        difference=observed, low=low, high=high,
    )


def rungs(available_items: int) -> list[int]:
    """The ladder truncated to the items that exist, always ending at the full split."""

    steps = [step for step in LADDER if step < available_items]
    return steps + [available_items]
