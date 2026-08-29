"""Pre-registered instrument-validity rule, V2 -- with uncertainty.

`MISSION §8`: pre-register instrument validity BEFORE inspecting candidate results, use a
statistically defensible rule, and do not change the criterion after seeing which
representation wins.

V1's rule compared point estimates to fixed thresholds. On 24 items one flipped answer moves
an arm by 0.042, so a negative arm at 0.583 and one at 0.500 were treated as categorically
different when they are two coin flips apart. V2 asks the question the rule is actually
about -- *is this arm distinguishable from chance* -- with an exact binomial interval, and
refuses to classify when the sample cannot answer.

The rule, fixed here before any V2 candidate has been rendered:

    POSITIVE valid   iff the exact binomial lower bound on P exceeds chance.
                          The instrument must demonstrably reach the relation when told it.
    NEGATIVE valid   iff the exact binomial lower bound on N does NOT exceed chance.
                          A negative arm that is significantly above chance proves the
                          question is answerable without the relation.
    RANGE valid      iff the observed dynamic range P - N is at least MINIMUM_RANGE.

An instrument passing all three may judge a representation. One failing any may not, and the
failure is attributed to the instrument -- never to the language.

Comparison between candidate and control is a *paired* question on the same items, so it
uses a paired bootstrap rather than two independent intervals.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
import math
from typing import Any, Sequence

# --------------------------------------------------------------------- pre-registered

#: Two-sided confidence level for every arm interval.
CONFIDENCE = 0.90
#: The smallest P - N that can support a judgement. Below this a real improvement would be
#: indistinguishable from sampling noise no matter how many representations were compared.
MINIMUM_RANGE = 0.20
#: Candidate and control are called equal inside this margin on the paired difference.
PARITY_MARGIN = 0.10
#: Sequential ladder. Stop as soon as the verdict is decided; escalate only when ambiguous.
LADDER: tuple[int, ...] = (12, 24, 32, 48)

PREREGISTERED = {
    "rule_version": "micromath-calibration-v2.0.0",
    "confidence": CONFIDENCE,
    "minimum_range": MINIMUM_RANGE,
    "parity_margin": PARITY_MARGIN,
    "ladder": list(LADDER),
    "positive_rule": "exact binomial lower bound on P must exceed chance",
    "negative_rule": "exact binomial lower bound on N must NOT exceed chance",
    "range_rule": "P - N >= minimum_range",
    "comparison_rule": "paired bootstrap over matched items, 10000 resamples",
    "fixed_before": "any V2 candidate rendering was scored",
}

INSTRUMENT_INVALID = "INSTRUMENT_INVALID"
INSTRUMENT_LIMIT = "INSTRUMENT_LIMIT"
INSTRUMENT_UNDECIDED = "INSTRUMENT_UNDECIDED"
INSTRUMENT_VALID = "INSTRUMENT_VALID"

ADVANTAGE = "ADVANTAGE"
CONTROL_PARITY = "CONTROL_PARITY"
LANGUAGE_WEAKNESS = "LANGUAGE_WEAKNESS"
UNTESTED = "UNTESTED"


# ------------------------------------------------------------------------- statistics

def _betainc_regularised(a: float, b: float, x: float) -> float:
    """Regularised incomplete beta, by continued fraction. Exact-binomial machinery."""

    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    log_front = (math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
                 + a * math.log(x) + b * math.log1p(-x))
    front = math.exp(log_front)
    if x < (a + 1.0) / (a + b + 2.0):
        return front * _cf(a, b, x) / a
    return 1.0 - math.exp(
        math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
        + b * math.log1p(-x) + a * math.log(x)) * _cf(b, a, 1.0 - x) / b


def _cf(a: float, b: float, x: float, iterations: int = 300) -> float:
    tiny = 1e-30
    f, c, d = 1.0, 1.0, 0.0
    for index in range(iterations):
        m = index // 2
        if index == 0:
            numerator = 1.0
        elif index % 2 == 0:
            numerator = (m * (b - m) * x) / ((a + 2.0 * m - 1.0) * (a + 2.0 * m))
        else:
            numerator = -((a + m) * (a + b + m) * x) / ((a + 2.0 * m) * (a + 2.0 * m + 1.0))
        d = 1.0 + numerator * d
        d = tiny if abs(d) < tiny else d
        d = 1.0 / d
        c = 1.0 + numerator / c
        c = tiny if abs(c) < tiny else c
        f *= c * d
        if abs(1.0 - c * d) < 1e-12:
            break
    return f


def clopper_pearson(successes: int, trials: int,
                    confidence: float = CONFIDENCE) -> tuple[float, float]:
    """Exact binomial interval. Conservative, and correct at the small n this lab runs."""

    if trials <= 0:
        return (0.0, 1.0)
    alpha = 1.0 - confidence
    lower = 0.0 if successes == 0 else _invert(alpha / 2.0, successes, trials, upper=False)
    upper = 1.0 if successes == trials else _invert(alpha / 2.0, successes, trials, upper=True)
    return (lower, upper)


def _invert(tail: float, successes: int, trials: int, upper: bool) -> float:
    low, high = 0.0, 1.0
    for _ in range(200):
        mid = (low + high) / 2.0
        if upper:
            probability = _betainc_regularised(successes + 1, trials - successes, mid)
            if probability > 1.0 - tail:
                high = mid
            else:
                low = mid
        else:
            probability = 1.0 - _betainc_regularised(successes, trials - successes + 1, mid)
            if probability > 1.0 - tail:
                low = mid
            else:
                high = mid
    return (low + high) / 2.0


def paired_bootstrap(candidate: Sequence[bool], control: Sequence[bool],
                     resamples: int = 10000, seed: int = 20260829) -> dict[str, float]:
    """Bootstrap the paired difference. Deterministic: seeded LCG, no global RNG."""

    if len(candidate) != len(control) or not candidate:
        return {"difference": 0.0, "lower": 0.0, "upper": 0.0}
    n = len(candidate)
    differences = [float(a) - float(b) for a, b in zip(candidate, control)]
    observed = sum(differences) / n
    state = seed & 0xFFFFFFFF
    draws: list[float] = []
    for _ in range(resamples):
        total = 0.0
        for _index in range(n):
            state = (1103515245 * state + 12345) & 0x7FFFFFFF
            total += differences[state % n]
        draws.append(total / n)
    draws.sort()
    tail = (1.0 - CONFIDENCE) / 2.0
    return {
        "difference": observed,
        "lower": draws[max(0, int(tail * resamples) - 1)],
        "upper": draws[min(resamples - 1, int((1.0 - tail) * resamples))],
    }


# --------------------------------------------------------------------------- verdicts

@dataclass
class ArmResult:
    label: str
    successes: int
    trials: int

    @property
    def accuracy(self) -> float:
        return self.successes / self.trials if self.trials else 0.0

    def interval(self) -> tuple[float, float]:
        return clopper_pearson(self.successes, self.trials)


@dataclass
class InstrumentVerdict:
    status: str
    reason: str
    chance: float
    positive: float
    negative: float
    dynamic_range: float
    positive_lower: float
    negative_lower: float
    decisive: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def classify_instrument(positive: ArmResult, negative: ArmResult,
                        chance: float) -> InstrumentVerdict:
    """Apply the pre-registered rule. Instrument only -- no candidate is consulted here."""

    positive_lower, _ = positive.interval()
    negative_lower, negative_upper = negative.interval()
    dynamic_range = positive.accuracy - negative.accuracy

    def verdict(status: str, reason: str, decisive: bool = True) -> InstrumentVerdict:
        return InstrumentVerdict(
            status=status, reason=reason, chance=chance,
            positive=round(positive.accuracy, 4), negative=round(negative.accuracy, 4),
            dynamic_range=round(dynamic_range, 4),
            positive_lower=round(positive_lower, 4),
            negative_lower=round(negative_lower, 4), decisive=decisive)

    if negative_lower > chance:
        return verdict(
            INSTRUMENT_INVALID,
            f"the negative arm scores {negative.accuracy:.3f} with a {CONFIDENCE:.0%} lower "
            f"bound of {negative_lower:.3f}, above chance {chance:.3f}; the question is "
            f"answerable with the relation destroyed, so it never tested the relation")
    if positive_lower <= chance:
        # Undecided rather than invalid: a positive arm that has not separated from chance
        # may simply not have been given enough items yet.
        if positive.accuracy > chance and positive.trials < LADDER[-1]:
            return verdict(
                INSTRUMENT_UNDECIDED,
                f"the positive arm is {positive.accuracy:.3f} but its lower bound "
                f"{positive_lower:.3f} has not cleared chance at n={positive.trials}",
                decisive=False)
        return verdict(
            INSTRUMENT_LIMIT,
            f"stating the relation outright only reaches {positive.accuracy:.3f} "
            f"(lower bound {positive_lower:.3f}); this reader cannot do the task at any "
            f"readability, so no representation is to blame")
    if dynamic_range < MINIMUM_RANGE:
        return verdict(
            INSTRUMENT_LIMIT,
            f"dynamic range {dynamic_range:.3f} is below the pre-registered "
            f"{MINIMUM_RANGE:.2f} and cannot separate representations")
    return verdict(INSTRUMENT_VALID,
                   f"positive {positive.accuracy:.3f} (lower {positive_lower:.3f}) is above "
                   f"chance {chance:.3f}, negative {negative.accuracy:.3f} is not, and the "
                   f"range is {dynamic_range:.3f}")


def compare(candidate_items: Sequence[bool], control_items: Sequence[bool]) -> tuple[str, str]:
    """Candidate against the best general control, on the same items."""

    stats = paired_bootstrap(candidate_items, control_items)
    difference = stats["difference"]
    if difference > PARITY_MARGIN and stats["lower"] > 0.0:
        return ADVANTAGE, (f"candidate leads by {difference:+.3f} "
                           f"(bootstrap {stats['lower']:+.3f} to {stats['upper']:+.3f})")
    if difference < -PARITY_MARGIN and stats["upper"] < 0.0:
        return LANGUAGE_WEAKNESS, (f"candidate trails by {difference:+.3f} "
                                   f"(bootstrap {stats['lower']:+.3f} to {stats['upper']:+.3f})")
    return CONTROL_PARITY, (f"candidate differs by {difference:+.3f}, within the "
                            f"{PARITY_MARGIN:.2f} parity margin "
                            f"(bootstrap {stats['lower']:+.3f} to {stats['upper']:+.3f})")


def normalised_readability(candidate: float, positive: float, negative: float) -> float | None:
    """Where the candidate sits between a destroyed relation and an explicit one."""

    span = positive - negative
    if span < MINIMUM_RANGE:
        return None
    return round((candidate - negative) / span, 4)
