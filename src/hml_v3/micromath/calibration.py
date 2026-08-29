"""Positive and negative control arms: certifying the INSTRUMENT before the language.

`COMPONENT_CERTIFICATION §4-5`. Every accuracy this project has reported so far shares one
hole: a candidate scoring 0.625 on a component could mean the representation hides the
relation, or it could mean no reader can answer that question however plainly it is written.
Those two readings demand opposite responses -- repair the language, or repair the benchmark
-- and nothing measured so far can tell them apart.

Two extra arms close it, and neither is a candidate language:

``EXPLICIT_POSITIVE`` states the target relation in the plainest form the question admits,
next to the same mathematics. It answers "can this reader do this task at all?". If it sits
near chance the cell is an ``INSTRUMENT_LIMIT`` and the candidate is not to blame.

``SCRAMBLED_NEGATIVE`` keeps every superficial property and destroys the relation. It answers
"is the task solvable without the relation?". If it scores well above chance the cell is
leaking and is ``INSTRUMENT_INVALID``.

The gap between them is the instrument's dynamic range. A component measured on an
instrument with no range cannot be certified, whatever the candidate scored.
"""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Any

from hml_v3.micromath import stresses as S

#: How the target relation is written out for the positive control, per stress.
RELATION_HEADER = {
    S.BINDER: "USE_TO_BINDER",
    S.SCOPE: "DECLARATION_TO_GOAL",
    S.DEPENDENCY: "TYPE_TO_DEPENDENCY",
    S.TYPE: "DECLARATION_TO_TYPE_HEAD",
    S.MULTI_GOAL: "ACTION_TO_FOCUSED_GOAL",
    S.EXPRESSION_DEPTH: "DEEPEST_REFERENCE",
    S.PREMISE: "ACTION_TO_CITED_PREMISE",
    S.ACTION_ARGUMENT: "ACTION_TO_USED_DECLARATION",
}


@dataclass
class CalibrationArm:
    """A renderer-shaped object. Deliberately not a genome: it is instrumentation."""

    label: str
    kind: str          # EXPLICIT_POSITIVE | SCRAMBLED_NEGATIVE
    base: Any          # the compiler whose rendering it wraps
    answers: dict[str, str]
    stress: str
    seed: int = 20260829

    candidate_id = "CALIBRATION"

    @property
    def surface(self):
        return self.base.surface

    def _key(self, state: dict[str, Any]) -> str:
        from hml_v3.micromath.schema import state_digest
        return state_digest(state)

    def render(self, state: dict[str, Any]):
        rendered = self.base.render(state)
        answer = self.answers.get(self._key(state))
        if answer is None:
            return rendered
        encoded = rendered.codec.encode(answer)
        name = encoded if isinstance(encoded, str) else answer
        header = RELATION_HEADER.get(self.stress, "TARGET_RELATION")
        if self.kind == "EXPLICIT_POSITIVE":
            # The relation, stated once, in the plainest form the question admits.
            rendered.text = f"{header} = {name}\n\n{rendered.text}"
        else:
            # Same shape, same length class, no information: a decoy binding that is
            # independent of the truth. Superficial properties are preserved so a length or
            # token-count reader gains nothing.
            rng = random.Random(f"{self.seed}|{self._key(state)}")
            decoy = rng.choice(sorted({name, *_visible_names(rendered.text)}) or [name])
            rendered.text = f"{header} = {decoy}\n\n{rendered.text}"
        return rendered

    def render_text(self, state: dict[str, Any]) -> str:
        return self.render(state).text

    def parse_core(self, text: str, codec):
        body = text.split("\n\n", 1)[1] if "\n\n" in text else text
        return self.base.parse_core(body, codec)


def _visible_names(text: str) -> set[str]:
    import re
    return set(re.findall(r"\b[a-z]{1,3}\d{1,3}\b", text))


def build_arms(base_compiler, pairs, stress: str) -> tuple[CalibrationArm, CalibrationArm]:
    """The two instrument arms for one component, over one suite of matched pairs."""

    from hml_v3.micromath.schema import state_digest

    answers: dict[str, str] = {}
    for pair in pairs:
        answers[state_digest(pair.state_a)] = pair.answer_a
        answers[state_digest(pair.state_b)] = pair.answer_b
    return (
        CalibrationArm("EXPLICIT_POSITIVE", "EXPLICIT_POSITIVE", base_compiler, answers, stress),
        CalibrationArm("SCRAMBLED_NEGATIVE", "SCRAMBLED_NEGATIVE", base_compiler, answers, stress),
    )


# ------------------------------------------------------------------- component verdicts

UNTESTED = "UNTESTED"
INSTRUMENT_INVALID = "INSTRUMENT_INVALID"
INSTRUMENT_LIMIT = "INSTRUMENT_LIMIT"
LANGUAGE_WEAKNESS = "LANGUAGE_WEAKNESS"
CONTROL_PARITY = "CONTROL_PARITY"
ADVANTAGE = "ADVANTAGE"

#: Preregistered, before any calibration number was seen.
#: The positive arm must clear chance by more than sampling noise on a 16-pair suite
#: (SE at p=0.5, n=32 items is 0.088, so 2 SE is 0.177 -- rounded to 0.15 with the paired
#: bootstrap's variance reduction taken into account).
POSITIVE_MUST_EXCEED_CHANCE = 0.15
#: The negative arm must not: if the relation can be destroyed and the question still
#: answered, the question was never about the relation.
NEGATIVE_MAX_ABOVE_CHANCE = 0.15
#: Below this the instrument cannot separate a good representation from a bad one.
MINIMUM_DYNAMIC_RANGE = 0.20
#: How far a candidate may trail the best general control and still be called parity.
PARITY_MARGIN = 0.10


def normalised_readability(candidate: float, positive: float, negative: float) -> float | None:
    """``(candidate - negative) / (positive - negative)``, or None without range.

    `§6`: reported *alongside* raw accuracy and never instead of it. It lets a component
    measured on a 0.80-ceiling instrument be compared with one measured on a 0.99 ceiling,
    and it is meaningless when the denominator is small -- which is exactly when the
    component should not be certified at all.
    """

    span = positive - negative
    if span < MINIMUM_DYNAMIC_RANGE:
        return None
    return (candidate - negative) / span


def classify(positive: float, negative: float, candidate: float,
             best_control: float) -> tuple[str, str]:
    """The component's status, and why."""

    chance = 0.5
    span = positive - negative
    if negative - chance > NEGATIVE_MAX_ABOVE_CHANCE:
        return INSTRUMENT_INVALID, (
            f"the negative arm scores {negative:.3f}; the question is answerable with the "
            "relation destroyed, so it was never testing the relation")
    if positive - chance < POSITIVE_MUST_EXCEED_CHANCE:
        return INSTRUMENT_LIMIT, (
            f"even stating the relation outright only reaches {positive:.3f}; this reader "
            "cannot do this task at any readability, so the candidate is not to blame")
    if span < MINIMUM_DYNAMIC_RANGE:
        return INSTRUMENT_LIMIT, (
            f"dynamic range {span:.3f} is too small to separate representations")
    if candidate > best_control + PARITY_MARGIN:
        return ADVANTAGE, (
            f"candidate {candidate:.3f} exceeds the best general control "
            f"{best_control:.3f} by more than the parity margin")
    if candidate >= best_control - PARITY_MARGIN:
        return CONTROL_PARITY, (
            f"candidate {candidate:.3f} is within {PARITY_MARGIN} of the best general "
            f"control {best_control:.3f}")
    return LANGUAGE_WEAKNESS, (
        f"the instrument is valid (range {span:.3f}) and the candidate {candidate:.3f} "
        f"trails the best general control {best_control:.3f}; this is the representation, "
        "not the measurement")
