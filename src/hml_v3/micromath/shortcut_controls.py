"""Level B: prove the benchmark cannot be solved without reading structure.

`MICROMATH §11` requires dumb baselines to sit at chance before any neural result is
believed. Because every counterfactual is a transposition, the *canonical* token multiset of
A and B is identical by construction -- but the question is whether that survives
**rendering**. A representation that, say, sorts declarations by identity will render the two
states with different token orders and could leak the answer through surface statistics.

So the audit is empirical, per candidate representation. For each shallow feature and each
pair it compares f(render(A)) against f(render(B)):

* ``identical`` -- the feature cannot separate the pair at all; it is at chance by
  construction, which is the outcome the design intends;
* ``consistent_sign`` -- the feature separates the pair *and* separates it the same way
  across pairs, which is exploitable and therefore leakage.

A feature that differs with no consistent direction is noise, not a shortcut: a reader
cannot know which sign means which answer without already knowing the answer.
"""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, Callable

from hml_v3.representation_search.tokenizer import pretokens

IDENTIFIER = re.compile(r"[^\W\d][\w.]*", re.UNICODE)
OPERATOR = re.compile(r"[^\w\s]")

#: Leakage threshold. A feature that points the same way on more than this share of the
#: separable pairs could be turned into a rule that beats chance without reading structure.
CONSISTENCY_LIMIT = 0.75


def _bag(text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for token in pretokens(text):
        stripped = token.strip()
        if stripped:
            counts[stripped] = counts.get(stripped, 0) + 1
    return counts


def _char_ngrams(text: str, size: int = 4) -> dict[str, int]:
    """Full bag of character n-grams.

    The first version of this sampled every seventh position, which made it a function of
    *where* things sat rather than of what was present. It then reported a difference on
    every pair for every candidate, including ones whose renderings were identical in every
    scalar statistic -- an instrument defect that would have condemned a sound benchmark.
    """

    counts: dict[str, int] = {}
    for index in range(max(0, len(text) - size + 1)):
        gram = text[index:index + size]
        counts[gram] = counts.get(gram, 0) + 1
    return counts


FEATURES: dict[str, Callable[[str], Any]] = {
    "class_prior": lambda text: 0,
    "length_chars": len,
    "token_count": lambda text: len(pretokens(text)),
    "line_count": lambda text: text.count("\n"),
    "field_count": lambda text: text.count(":") + text.count("="),
    "punctuation_count": lambda text: len(OPERATOR.findall(text)),
    "bag_of_words": _bag,
    "char_ngram": _char_ngrams,
    "identifier_frequency": lambda text: len(IDENTIFIER.findall(text)),
    "operator_frequency": lambda text: len(OPERATOR.findall(text)),
}

#: Order-insensitive features. For these, equality means the multiset matched even if the
#: layout moved, which is exactly the property a transposition is supposed to preserve.
MULTISET_FEATURES = frozenset({"bag_of_words", "char_ngram"})


@dataclass
class FeatureAudit:
    feature: str
    pairs: int
    identical: int
    separable: int
    consistent_sign: int

    @property
    def identical_share(self) -> float:
        return self.identical / self.pairs if self.pairs else 0.0

    @property
    def consistency(self) -> float:
        return self.consistent_sign / self.separable if self.separable else 0.0

    @property
    def leaks(self) -> bool:
        return self.separable > 0 and self.consistency > CONSISTENCY_LIMIT

    def to_dict(self) -> dict[str, Any]:
        return {
            "feature": self.feature, "pairs": self.pairs,
            "identical": self.identical, "identical_share": round(self.identical_share, 4),
            "separable": self.separable, "consistent_sign": self.consistent_sign,
            "consistency": round(self.consistency, 4), "leaks": self.leaks,
        }


def _first_index(text: str, needle: str) -> int:
    position = text.find(needle)
    return position if position >= 0 else len(text) + 1


def answer_targeted_controls(compiler, pairs) -> dict[str, Any]:
    """The shortcuts a reader could actually use, scored as accuracy over every item.

    A multiset differing between A and B is not by itself a shortcut: a bag has no
    direction, so a reader cannot turn "these bags differ" into an answer without already
    knowing the answer. What *is* exploitable is an asymmetry attached to the options
    themselves -- the correct option appearing more often than the distractor, or earlier,
    or last. Each rule below is applied to every rendering and scored against the truth, so
    the output is directly comparable to the 0.5 a coin gets.
    """

    rules = ("always_first_option", "more_frequent_option",
             "earlier_option", "later_option")
    hits = {name: 0 for name in rules}
    total = 0
    for pair in pairs:
        for state, answer in ((pair.state_a, pair.answer_a), (pair.state_b, pair.answer_b)):
            try:
                rendered = compiler.render(state)
            except Exception:  # noqa: BLE001
                continue
            text = rendered.text
            # The options must be the SAME strings the probe shows the model. Counting raw
            # canonical ids that the codec never writes to the page returns zero for both
            # options, scores every item as undecided, and reports a spotless 0.509 for a
            # benchmark that was never examined.
            encoded = []
            for option in pair.options:
                value = rendered.codec.encode(option)
                encoded.append(value if isinstance(value, str) else option)
            if len(set(encoded)) != 2:
                continue
            left, right = encoded
            answer = encoded[list(pair.options).index(answer)]
            total += 1
            if left == answer:
                hits["always_first_option"] += 1
            count_left, count_right = text.count(left), text.count(right)
            if count_left != count_right:
                guess = left if count_left > count_right else right
                if guess == answer:
                    hits["more_frequent_option"] += 1
            else:
                hits["more_frequent_option"] += 0.5  # undecided; scored as a coin flip
            first_left, first_right = _first_index(text, left), _first_index(text, right)
            if first_left != first_right:
                if (left if first_left < first_right else right) == answer:
                    hits["earlier_option"] += 1
                if (left if first_left > first_right else right) == answer:
                    hits["later_option"] += 1
            else:
                hits["earlier_option"] += 0.5
                hits["later_option"] += 0.5
    return {
        "items": total,
        "accuracy": {name: round(hits[name] / total, 4) if total else 0.0
                     for name in rules},
        "chance": 0.5,
    }


#: How far above chance an answer-targeted rule may sit before the benchmark is unusable.
#: Deliberately tight: at 29 dev pairs (58 items) the standard error of a proportion at
#: chance is about 0.066, so 0.65 is roughly two standard errors and will fire on a real
#: asymmetry without firing on ordinary sampling noise.
ANSWER_CONTROL_LIMIT = 0.65


def audit(compiler, pairs) -> dict[str, Any]:
    results: dict[str, FeatureAudit] = {
        name: FeatureAudit(name, 0, 0, 0, 0) for name in FEATURES}
    for pair in pairs:
        try:
            text_a = compiler.render_text(pair.state_a)
            text_b = compiler.render_text(pair.state_b)
        except Exception:  # noqa: BLE001
            continue
        for name, function in FEATURES.items():
            value_a, value_b = function(text_a), function(text_b)
            entry = results[name]
            entry.pairs += 1
            if value_a == value_b:
                entry.identical += 1
                continue
            entry.separable += 1
            if isinstance(value_a, (int, float)) and isinstance(value_b, (int, float)):
                if value_a > value_b:
                    entry.consistent_sign += 1

    scalar = [entry.to_dict() for name, entry in results.items()
              if name not in MULTISET_FEATURES]
    multiset = [entry.to_dict() for name, entry in results.items()
                if name in MULTISET_FEATURES]
    targeted = answer_targeted_controls(compiler, pairs)

    # The verdict rests on answer prediction alone.
    #
    # A scalar feature separating A from B with a consistent sign was originally treated as
    # leakage. It is not, once the option order is balanced: telling A from B yields an
    # answer only if one side always carries the first option, and it no longer does. What
    # such a feature really measures is that this candidate's LAYOUT depends on the relation
    # being transposed -- a property of the representation worth reporting, and reported
    # below as layout_sensitivity, but not something a zero-shot reader can turn into a
    # choice. The tests build a deliberately leaky benchmark and require this function to
    # fail it, so the narrower verdict is not a weaker one.
    # Per stress as well as overall. An aggregate hides a cell: MULTI_GOAL and PREMISE both
    # scored 1.000 for "pick whichever option appears earlier" while the aggregate sat at
    # 0.62 and read as a pass. `MICROMATH §8` -- the cell is the primitive diagnostic unit --
    # applies to the audit exactly as it applies to the results.
    by_stress: dict[str, list[Any]] = {}
    for pair in pairs:
        by_stress.setdefault(pair.stress, []).append(pair)
    per_stress = {
        stress: answer_targeted_controls(compiler, group)
        for stress, group in sorted(by_stress.items())
    }
    leaking = [name for name, value in targeted["accuracy"].items()
               if value > ANSWER_CONTROL_LIMIT]
    leaking += [
        f"{stress}:{rule}"
        for stress, report in per_stress.items()
        for rule, value in report["accuracy"].items()
        if value > ANSWER_CONTROL_LIMIT
    ]
    layout_sensitive = [entry["feature"] for entry in scalar if entry["leaks"]]
    return {
        "layout_sensitivity": sorted(layout_sensitive),
        "answer_targeted_controls_by_stress": {
            stress: {"items": report["items"], "accuracy": report["accuracy"]}
            for stress, report in per_stress.items()
        },
        "scalar_features": sorted(scalar, key=lambda item: item["feature"]),
        "multiset_features": sorted(multiset, key=lambda item: item["feature"]),
        "answer_targeted_controls": targeted,
        "leaking_features": sorted(set(leaking)),
        "verdict": "BENCHMARK_INVALID" if leaking else "PASS",
        "consistency_limit": CONSISTENCY_LIMIT,
        "answer_control_limit": ANSWER_CONTROL_LIMIT,
        "note": (
            "Every pair is a transposition, so the canonical token multiset is identical by "
            "construction. Scalar features are judged by consistent sign. Multiset features "
            "are reported but never counted as leakage on their own: a bag has no direction, "
            "so a difference in it is not usable as an answer. What can be exploited is an "
            "asymmetry attached to the options, which the answer-targeted controls measure "
            "directly as accuracy against chance."
        ),
    }
