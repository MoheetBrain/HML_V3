#!/usr/bin/env python3
"""What PRM800K can and cannot tell a representation search.

PRM800K's step labels are **human judgements of usefulness**, not verdicts of logical
validity. Promoting them to formal truth would contaminate the verifier-backed status that
`D-008` keeps calibrated. What they *can* do is name dimensions the formal corpus never
exposes: whether a step made progress, whether it was valid but useless, whether it was a
dead end, and what the alternatives at that point were.

This analysis extracts those dimensions from the real labels and then asks a question about
the search itself: **does any representation in the genome space have the structure to
express them?** A representation can only expose what the canonical state carries, so the
answer is a property of `CanonicalMathState`, not of any genome.
"""

from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

DEFAULT_PRM = Path("/Users/moheet/Documents/ChatGPT/prm800k/prm800k/data")

RATING_MEANING = {
    1: "PROGRESS_TOWARD_SOLUTION",
    0: "VALID_BUT_NOT_PROGRESSING",
    -1: "DEAD_END_OR_ERROR",
    None: "UNRATED",
}

#: The discovery dimensions the labels expose, and where each would have to live if the
#: canonical layer were ever extended to carry it. Nothing here is implemented: the extension
#: rule in the gap register requires source evidence, a mathematical role, a demonstrated
#: loss, a cross-system interpretation and a test before the IR grows.
DIMENSIONS = {
    "step_progress": {
        "question": "did this action move the proof toward a solution?",
        "prm800k_signal": "completion rating +1",
        "canonical_v2_field": None,
        "expressible_by_any_genome": False,
        "why": "CanonicalMathTransition carries the verifier's acceptance of a step, not a "
               "judgement of whether the step helped. No axis can expose an absent field.",
    },
    "valid_but_useless": {
        "question": "was this action legal yet unhelpful?",
        "prm800k_signal": "completion rating 0",
        "canonical_v2_field": None,
        "expressible_by_any_genome": False,
        "why": "the structured delta records what changed, and a legal no-op is visible as an "
               "empty delta, but 'legal and unhelpful' is a judgement the delta does not make.",
    },
    "dead_end": {
        "question": "did this action make the goal unreachable or wrong?",
        "prm800k_signal": "completion rating -1",
        "canonical_v2_field": None,
        "expressible_by_any_genome": False,
        "why": "a Lean trace contains only steps that were kept. Abandoned branches leave no "
               "TacticInfo, so the corpus has no negative examples at all.",
    },
    "alternative_branch": {
        "question": "what else could have been done at this state?",
        "prm800k_signal": "multiple completions offered at one step",
        "canonical_v2_field": None,
        "expressible_by_any_genome": False,
        "why": "a CanonicalMathTransition is a single before/action/after triple. Siblings "
               "would require a state-to-many-actions record the schema does not have.",
    },
    "no_acceptable_alternative": {
        "question": "were all offered continuations rejected?",
        "prm800k_signal": "human_completion present with chosen_completion null",
        "canonical_v2_field": None,
        "expressible_by_any_genome": False,
        "why": "same structural absence as alternative_branch.",
    },
    "solution_outcome": {
        "question": "did the whole attempt end in a solution, an error, or a give-up?",
        "prm800k_signal": "label.finish_reason",
        "canonical_v2_field": "verifier evidence exists per transition, not per attempt",
        "expressible_by_any_genome": False,
        "why": "the corpus unit is one transition; an attempt-level outcome has no home.",
    },
}


def analyse(paths: list[Path], limit: int) -> dict:
    ratings: collections.Counter = collections.Counter()
    finish: collections.Counter = collections.Counter()
    branching: collections.Counter = collections.Counter()
    steps_per_attempt: list[int] = []
    attempts = 0
    steps = 0
    human_written = 0
    all_rejected = 0
    flagged = 0
    files_read: list[str] = []

    for path in paths:
        if not path.exists():
            continue
        files_read.append(str(path))
        with path.open(encoding="utf-8") as handle:
            for index, line in enumerate(handle):
                if index >= limit:
                    break
                if not line.strip():
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                label = row.get("label") or {}
                attempts += 1
                finish[label.get("finish_reason")] += 1
                attempt_steps = label.get("steps") or []
                steps_per_attempt.append(len(attempt_steps))
                for step in attempt_steps:
                    steps += 1
                    completions = step.get("completions") or []
                    branching[min(len(completions), 10)] += 1
                    for completion in completions:
                        ratings[completion.get("rating")] += 1
                        if completion.get("flagged"):
                            flagged += 1
                    if step.get("human_completion"):
                        human_written += 1
                    if completions and step.get("chosen_completion") is None:
                        all_rejected += 1

    total_ratings = sum(ratings.values()) or 1
    return {
        "files_read": files_read,
        "rows_per_file_limit": limit,
        "attempts": attempts,
        "steps": steps,
        "completions": total_ratings,
        "mean_steps_per_attempt": round(
            sum(steps_per_attempt) / max(1, len(steps_per_attempt)), 3),
        "rating_distribution": {
            RATING_MEANING[key]: {"count": value, "share": round(value / total_ratings, 4)}
            for key, value in sorted(ratings.items(), key=lambda item: (item[0] is None, item[0]))
        },
        "finish_reasons": {str(key): value for key, value in finish.most_common()},
        "branching_factor": {
            str(key): value for key, value in sorted(branching.items())
        },
        "steps_with_a_human_written_continuation": human_written,
        "steps_where_every_offered_continuation_was_rejected": all_rejected,
        "flagged_completions": flagged,
    }


def render(stats: dict) -> str:
    lines = [
        "# Discovery Representation Analysis",
        "",
        "PRM800K labels are **human judgements of usefulness**. They are not verdicts of "
        "logical validity and are never promoted into the verifier-backed status that "
        "`D-008` keeps calibrated. They are used here for one purpose: to name the "
        "dimensions a formal Lean trace cannot express, and then to ask whether any "
        "representation in the search space could express them.",
        "",
        "## What the labels contain",
        "",
        f"Read {stats['attempts']:,} labelled attempts containing {stats['steps']:,} steps "
        f"and {stats['completions']:,} rated continuations "
        f"(first {stats['rows_per_file_limit']:,} rows of each file).",
        "",
        "| Step judgement | Count | Share |",
        "|---|---:|---:|",
    ]
    for name, value in stats["rating_distribution"].items():
        lines.append(f"| `{name}` | {value['count']:,} | {value['share']:.1%} |")
    lines += [
        "",
        "| Attempt outcome | Attempts |",
        "|---|---:|",
    ]
    for reason, count in stats["finish_reasons"].items():
        lines.append(f"| `{reason}` | {count:,} |")
    lines += [
        "",
        f"Mean steps per attempt: **{stats['mean_steps_per_attempt']}**. "
        f"Steps where a human had to write the continuation because every offered one was "
        f"unacceptable: **{stats['steps_where_every_offered_continuation_was_rejected']:,}**.",
        "",
        "| Continuations offered at a step | Steps |",
        "|---|---:|",
    ]
    for size, count in stats["branching_factor"].items():
        lines.append(f"| {size}{'+' if size == '10' else ''} | {count:,} |")

    lines += [
        "",
        "## The finding",
        "",
        "**No representation in the current search space can express any of these "
        "dimensions, and the reason is not the representation.** A candidate exposes what "
        "`CanonicalMathState` carries; every discovery dimension below is absent from the "
        "canonical layer, so no genome — however structured — can surface it.",
        "",
        "| Dimension | PRM800K signal | Canonical V2 field | Expressible by any genome? |",
        "|---|---|---|---|",
    ]
    for name, item in DIMENSIONS.items():
        lines.append(
            f"| `{name}` | {item['prm800k_signal']} | "
            f"{item['canonical_v2_field'] or '**none**'} | "
            f"{'yes' if item['expressible_by_any_genome'] else '**no**'} |"
        )
    lines += ["", "### Why each is absent", ""]
    for name, item in DIMENSIONS.items():
        lines.append(f"- **`{name}`** — {item['why']}")

    lines += [
        "",
        "## The structural asymmetry this exposes",
        "",
        "A Lean trace contains only the steps that were kept. Abandoned branches leave no "
        "`TacticInfo`, so the formal corpus has **no negative examples at all** — every one "
        "of its 317 transitions is a step that worked. PRM800K's rated continuations are "
        f"{stats['rating_distribution'].get('DEAD_END_OR_ERROR', {}).get('share', 0):.1%} "
        "dead ends and "
        f"{stats['rating_distribution'].get('VALID_BUT_NOT_PROGRESSING', {}).get('share', 0):.1%} "
        "valid-but-not-progressing. A representation search optimised only on the formal "
        "corpus is therefore tuned on a distribution with no failure in it.",
        "",
        "## What would have to change, and what must not",
        "",
        "**Must not change.** PRM800K ratings are not verifier verdicts. Nothing here "
        "licenses labelling a canonical transition `DEAD_END` because a human rated a "
        "natural-language step `-1`. The two live in different columns permanently.",
        "",
        "**Would have to change, if this line is pursued.** The canonical layer would need a "
        "record that a formal trace does not currently produce: a state paired with several "
        "candidate actions and a per-candidate outcome. Producing it from Lean means running "
        "actions that were never taken and recording their results — a proof-search "
        "acquisition problem, not a representation problem, and explicitly out of scope for "
        "this mission.",
        "",
        "Until such a record exists, the honest position is that this search optimises "
        "representations of *verified transitions* and says nothing about representations of "
        "*search state*. Those are different objects and the current evidence separates them.",
    ]
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prm800k-dir", type=Path, default=DEFAULT_PRM)
    parser.add_argument("--limit", type=int, default=20000,
                        help="rows read per file; the full phase2 train file is 456 MB")
    parser.add_argument("--out-dir", type=Path,
                        default=ROOT / "reports/representation_search")
    args = parser.parse_args()

    paths = [
        args.prm800k_dir / "phase1_train.jsonl",
        args.prm800k_dir / "phase2_train.jsonl",
    ]
    stats = analyse(paths, args.limit)
    stats["dimensions"] = DIMENSIONS
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "DISCOVERY_REPRESENTATION_ANALYSIS.json").write_text(
        json.dumps(stats, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    (args.out_dir / "DISCOVERY_REPRESENTATION_ANALYSIS.md").write_text(render(stats))
    print(f"wrote {args.out_dir}/DISCOVERY_REPRESENTATION_ANALYSIS.md")
    print(json.dumps({k: v for k, v in stats.items() if k != "dimensions"}, indent=2)[:1600])


if __name__ == "__main__":
    main()
