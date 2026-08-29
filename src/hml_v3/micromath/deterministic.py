"""Level A: CPU-only structural measurement. No model, no GPU.

`MICROMATH §10` is the binding constraint here: a representation must not win because its
binder-use distance is small. Distance is a structural proxy and nothing more. So the
columns are kept apart and never combined into one number:

``INFORMATION_PRESENCE``   does the representation express the relation at all -- do A and B
                           render differently? If not, no reader of any kind can recover it.
``PARSER_RECOVERABILITY``  does the representation's own parser read the difference back?
                           A rendering can differ textually while decoding to the same
                           object, which is a lossy surface, not a working one.
``ACCESS_DISTANCE``        how far apart the question anchor and the answer sit, in tokens.
``AMBIGUITY``              how many places the answer could be read from.

A cell that scores 1.0 on presence and recoverability has been shown only to *contain* the
relation. Whether a reader uses it is Level C's question.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from hml_v3.representation_search.tokenizer import pretokens


@dataclass
class PairMeasurement:
    pair_id: str
    domain: str
    stress: str
    renders_differ: bool
    parse_recovers: bool
    render_failed: bool
    option_ambiguity_a: int
    option_ambiguity_b: int
    access_distance_tokens: float
    chars_a: int
    chars_b: int
    tokens_a: int
    tokens_b: int
    notes: dict[str, Any] = field(default_factory=dict)

    @property
    def expressible(self) -> bool:
        """The relation is present AND survives the representation's own decoder."""

        return self.renders_differ and self.parse_recovers

    def to_dict(self) -> dict[str, Any]:
        return {
            "pair_id": self.pair_id, "domain": self.domain, "stress": self.stress,
            "renders_differ": self.renders_differ,
            "parse_recovers": self.parse_recovers,
            "render_failed": self.render_failed,
            "expressible": self.expressible,
            "option_ambiguity_a": self.option_ambiguity_a,
            "option_ambiguity_b": self.option_ambiguity_b,
            "access_distance_tokens": round(self.access_distance_tokens, 3),
            "chars_a": self.chars_a, "chars_b": self.chars_b,
            "tokens_a": self.tokens_a, "tokens_b": self.tokens_b,
            "notes": self.notes,
        }


def _occurrences(text: str, needle: str) -> int:
    if not needle:
        return 0
    return text.count(needle)


def _token_gap(text: str, left: str, right: str) -> float:
    """Distance in pre-tokens between the first occurrences of two strings."""

    a, b = text.find(left), text.find(right)
    if a < 0 or b < 0:
        return float("inf")
    low, high = (a, b) if a <= b else (b, a)
    return float(len(pretokens(text[low:high])))


def measure_pair(compiler, pair) -> PairMeasurement:
    try:
        rendered_a = compiler.render(pair.state_a)
        rendered_b = compiler.render(pair.state_b)
    except Exception:  # noqa: BLE001 - a candidate that cannot render this state is a result
        return PairMeasurement(
            pair.pair_id, pair.domain, pair.stress, False, False, True,
            0, 0, float("inf"), 0, 0, 0, 0, {"error": "RENDER_FAILED"})

    text_a, text_b = rendered_a.text, rendered_b.text
    differ = text_a != text_b

    parse_recovers = False
    note: dict[str, Any] = {}
    try:
        core_a = compiler.parse_core(text_a, rendered_a.codec)
        core_b = compiler.parse_core(text_b, rendered_b.codec)
        parse_recovers = core_a != core_b
    except Exception as error:  # noqa: BLE001
        note["parse_error"] = type(error).__name__

    left, right = pair.options
    encoded_left = rendered_a.codec.encode(left) if hasattr(rendered_a.codec, "encode") else left
    encoded_right = rendered_a.codec.encode(right) if hasattr(rendered_a.codec, "encode") else right
    if not isinstance(encoded_left, str):
        encoded_left = left
    if not isinstance(encoded_right, str):
        encoded_right = right

    return PairMeasurement(
        pair_id=pair.pair_id, domain=pair.domain, stress=pair.stress,
        renders_differ=differ, parse_recovers=parse_recovers, render_failed=False,
        option_ambiguity_a=_occurrences(text_a, encoded_left),
        option_ambiguity_b=_occurrences(text_a, encoded_right),
        access_distance_tokens=_token_gap(text_a, encoded_left, encoded_right),
        chars_a=len(text_a), chars_b=len(text_b),
        tokens_a=len(pretokens(text_a)), tokens_b=len(pretokens(text_b)),
        notes=note,
    )


def measure(compiler, pairs) -> list[PairMeasurement]:
    return [measure_pair(compiler, pair) for pair in pairs]
