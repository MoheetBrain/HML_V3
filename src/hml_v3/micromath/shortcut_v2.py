"""Answer-targeted shortcut audit for N-choice items, run before any inference.

`FM-038` made this per-cell rather than aggregate. V2 adds the check that would have caught
its own worst defect for free: **answer entropy**. Every MULTI_GOAL item in the first V2 build
had the answer ``g1``, so "always say g1" scored 1.000 -- and it cost 277 seconds of Qwen
inference to notice, when a two-line count would have said so instantly.

The rules here read only the option strings and the answer. None of them look at the
mathematics, so any rule that beats chance is measuring a defect in the construction rather
than a property of a representation.

This is cheap, so it runs on every item of every split before a single probe is sent.
"""

from __future__ import annotations

import collections
from typing import Any, Callable, Sequence

from hml_v3.micromath.calibration_v2 import clopper_pearson

#: A rule is judged the same way an instrument arm is (`D-023`, `MISSION §8`): by an exact
#: binomial lower bound, not by a fixed margin. A flat tolerance made the verdict a function
#: of sample size -- at n=14 one rule landing 0.43 against chance 0.25 is ordinary noise, and
#: the first version called that a leak on one split and clean on another from the same
#: construction. Seven rules are tested at once, so the confidence is Bonferroni-corrected.
RULES_TESTED = 7
FAMILY_CONFIDENCE = 0.90
#: A constant answer is measured as the SHARE of items carrying the single most common
#: answer string, judged against chance by the same interval as the rules. Counting distinct
#: answers over item count was wrong and sample-size dependent: a cell whose options come
#: from a fixed vocabulary of four can never exceed 4/n, so at a hundred items every such
#: cell scored 0.04 and would have been condemned no matter how well balanced it was.


# The positional rules read the order the model is SHOWN, not a re-sorted copy. Sorting
# inside the audit measured an ordering no reader ever sees: it reported BINDER leaking at
# 0.447 while the presented positions were 17/11/10/9, which is close to uniform.
def _first(item: Any) -> str:
    return item.options[0]


def _last(item: Any) -> str:
    return item.options[-1]


def _second(item: Any) -> str:
    return item.options[1] if len(item.options) > 1 else item.options[0]


def _shortest(item: Any) -> str:
    return min(item.options, key=lambda o: (len(o), o))


def _longest(item: Any) -> str:
    return max(item.options, key=lambda o: (len(o), o))


def _most_common_globally(items: Sequence[Any]) -> Callable[[Any], str]:
    """Pick whichever option string is the most frequent answer across the whole cell.

    This is the rule that catches a constant answer, and it is the strongest dumb rule
    available to anyone who has seen the answer key -- which is the right adversary for a
    benchmark that will be published alongside its answers.
    """

    tally = collections.Counter(item.answer for item in items)
    def rule(item: Any) -> str:
        ranked = sorted(item.options, key=lambda o: (-tally.get(o, 0), o))
        return ranked[0]
    return rule


#: Rules that need nothing but the item in front of them. This is the honest adversary: a
#: reader who has never seen the answer key and is guessing from surface position or length.
#: A cell that these beat is leaky, full stop.
RULES: dict[str, Callable[[Any], str]] = {
    "always_first_option": _first,
    "always_second_option": _second,
    "always_last_option": _last,
    "shortest_option": _shortest,
    "longest_option": _longest,
    "alphabetically_first": lambda item: sorted(item.options)[0],
    "alphabetically_last": lambda item: sorted(item.options)[-1],
}


def audit(items: Sequence[Any]) -> dict[str, Any]:
    """Per-cell audit of one homogeneous group of items."""

    if not items:
        return {"items": 0, "status": "EMPTY"}
    chance = sum(item.chance for item in items) / len(items)
    scores = {name: sum(1 for item in items if rule(item) == item.answer) / len(items)
              for name, rule in RULES.items()}

    # Reported separately, and NOT used to condemn a cell. This rule is fitted to the answer
    # key of the very cell it is scored on, so on forty-odd items it is close to reading the
    # answers off the page. It measures the risk of publishing the benchmark beside its key,
    # which is a real risk and a different one from "a reader can shortcut this".
    global_rule = _most_common_globally(items)
    key_aware = sum(1 for item in items if global_rule(item) == item.answer) / len(items)

    answers = collections.Counter(item.answer for item in items)
    entropy = len(answers) / len(items)
    worst_name = max(scores, key=lambda name: scores[name])
    worst = scores[worst_name]

    # Bonferroni: testing seven rules at 90% family confidence needs each interval at
    # 1 - 0.10/7 two-sided, or the best-of-seven would clear chance by luck alone.
    per_rule = 1.0 - (1.0 - FAMILY_CONFIDENCE) / RULES_TESTED
    lower, _upper = clopper_pearson(round(worst * len(items)), len(items), per_rule)

    top_answer, top_count = answers.most_common(1)[0]
    constant_share = top_count / len(items)
    constant_lower, _ = clopper_pearson(top_count, len(items), per_rule)

    if constant_lower > chance:
        status = "CONSTANT_ANSWER"
        reason = (f"the single answer {top_answer!r} covers {constant_share:.3f} of items "
                  f"(lower bound {constant_lower:.3f}) against chance {chance:.3f}; always "
                  f"saying it beats guessing, so the cell is solvable without reading")
    elif lower > chance:
        status = "LEAKS"
        reason = (f"{worst_name} scores {worst:.3f} with a Bonferroni-corrected lower bound "
                  f"of {lower:.3f}, above chance {chance:.3f}; a rule that never reads the "
                  f"mathematics should not do that")
    else:
        status = "CLEAN"
        reason = (f"best of {RULES_TESTED} dumb rules is {worst_name} at {worst:.3f}, lower "
                  f"bound {lower:.3f}, not separated from chance {chance:.3f}")

    return {"items": len(items), "chance": round(chance, 4),
            "answer_entropy": round(entropy, 4), "distinct_answers": len(answers),
            "most_common_answer_share": round(constant_share, 4),
            "most_common_answer_lower_bound": round(constant_lower, 4),
            "scores": {k: round(v, 4) for k, v in sorted(scores.items())},
            "worst_rule": worst_name, "worst_score": round(worst, 4),
            "worst_lower_bound": round(lower, 4),
            "key_aware_most_common_answer": round(key_aware, 4),
            "key_aware_note": ("fitted to this cell's own answer key; an upper bound on "
                               "publication risk, not evidence that a reader can shortcut"),
            "status": status, "reason": reason}


def audit_by_stress(items: Sequence[Any]) -> dict[str, dict[str, Any]]:
    groups: dict[str, list[Any]] = collections.defaultdict(list)
    for item in items:
        groups[item.stress].append(item)
    return {stress: audit(group) for stress, group in sorted(groups.items())}


def clean(report: dict[str, dict[str, Any]]) -> list[str]:
    return sorted(name for name, entry in report.items() if entry.get("status") == "CLEAN")


def failing(report: dict[str, dict[str, Any]]) -> list[str]:
    return sorted(name for name, entry in report.items()
                  if entry.get("status") not in ("CLEAN", "EMPTY"))
