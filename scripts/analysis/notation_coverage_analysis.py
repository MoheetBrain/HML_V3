#!/usr/bin/env python3
"""Which human mathematical constructs does the formal corpus actually exercise?

MATH is human-written natural-language mathematics. Its worked solutions are **not**
promoted into Tier-A state transitions here: they are unverified prose, and `D-008` keeps
that boundary. What they are good for is a coverage question the formal corpus cannot answer
about itself — *which mathematical constructs does a representation search over 317 Lean
transitions never see?*

The correspondence below is lexical, not semantic: it checks whether a Mathlib constant
family whose name matches a construct appears in the corpus. It is not autoformalization and
does not claim the corpus proves anything about the construct.
"""

from __future__ import annotations

import argparse
import collections
import gzip
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hml_v3.representation_search.corpus import iter_corpus  # noqa: E402
DEFAULT_MATH = Path("/Users/moheet/Documents/ChatGPT/prm800k/prm800k/math_splits/train.jsonl")

LATEX_TOKEN = re.compile(r"\\[a-zA-Z]+")

#: Construct -> (LaTeX spellings, Mathlib constant-name fragments that would realise it).
#: The Mathlib side is a name fragment, so a match means "the corpus mentions a constant whose
#: name contains this", never "the corpus proves something about this construct".
CONSTRUCTS = {
    "finite sum": (["\\sum"], ["Finset.sum", "List.sum", "Multiset.sum", "tsum"]),
    "finite product": (["\\prod"], ["Finset.prod", "List.prod", "Multiset.prod"]),
    "integral": (["\\int"], ["integral", "MeasureTheory.integral", "intervalIntegral"]),
    "limit": (["\\lim"], ["Tendsto", "Filter.Tendsto", "limUnder"]),
    "derivative": (["\\frac{d}", "\\partial"], ["deriv", "HasDerivAt", "fderiv"]),
    "fraction": (["\\frac", "\\dfrac", "\\tfrac"], ["Rat", "div", "HDiv"]),
    "square root": (["\\sqrt"], ["sqrt", "Real.sqrt", "NNReal.sqrt"]),
    "absolute value": (["\\abs", "\\lvert"], ["abs", "norm", "Norm"]),
    "set membership": (["\\in", "\\notin"], ["Membership.mem", "Set.mem", "Finset.mem"]),
    "subset": (["\\subset", "\\subseteq"], ["HasSubset", "Set.Subset", "subset"]),
    "union / intersection": (["\\cup", "\\cap"], ["Union", "Inter", "sup", "inf"]),
    "universal quantifier": (["\\forall"], ["forall", "Pi"]),
    "existential quantifier": (["\\exists"], ["Exists"]),
    "implication": (["\\implies", "\\Rightarrow", "\\to"], ["Implies", "Function"]),
    "congruence / modular": (["\\pmod", "\\equiv"], ["ZMod", "Nat.ModEq", "Int.ModEq"]),
    "binomial coefficient": (["\\binom", "\\choose"], ["Nat.choose", "Nat.centralBinom"]),
    "factorial": (["!"], ["Nat.factorial", "factorial"]),
    "matrix": (["\\begin{pmatrix}", "\\det"], ["Matrix", "det", "LinearMap"]),
    "vector / inner product": (["\\vec", "\\cdot"], ["inner", "EuclideanSpace", "dotProduct"]),
    "trigonometry": (["\\sin", "\\cos", "\\tan"], ["Real.sin", "Real.cos", "Complex.sin"]),
    "logarithm / exponential": (["\\log", "\\ln", "\\exp"], ["Real.log", "Real.exp", "rexp"]),
    "infinity": (["\\infty"], ["Top", "ENNReal", "atTop", "EReal"]),
    "probability": (["\\Pr", "\\mathbb{P}"], ["ProbabilityTheory", "Measure", "volume"]),
    "real / complex numbers": (["\\mathbb{R}", "\\mathbb{C}"], ["Real", "Complex", "RCLike"]),
    "integers / naturals": (["\\mathbb{Z}", "\\mathbb{N}"], ["Int", "Nat"]),
}


def read_math(path: Path, limit: int) -> tuple[collections.Counter, collections.Counter, int]:
    tokens: collections.Counter = collections.Counter()
    subjects: collections.Counter = collections.Counter()
    rows = 0
    if not path.exists():
        return tokens, subjects, rows
    with path.open(encoding="utf-8") as handle:
        for index, line in enumerate(handle):
            if index >= limit or not line.strip():
                break
            row = json.loads(line)
            rows += 1
            subjects[row.get("subject") or row.get("type") or "unknown"] += 1
            text = f"{row.get('problem', '')}\n{row.get('solution', '')}"
            for token in LATEX_TOKEN.findall(text):
                tokens[token] += 1
            for literal in ("!", "\\begin{pmatrix}", "\\mathbb{R}", "\\mathbb{C}",
                            "\\mathbb{Z}", "\\mathbb{N}", "\\mathbb{P}"):
                if literal in text:
                    tokens[literal] += text.count(literal)
    return tokens, subjects, rows


def corpus_constants(path: Path) -> tuple[collections.Counter, int]:
    constants: collections.Counter = collections.Counter()
    rows = 0

    def walk(node) -> None:
        if isinstance(node, dict):
            if node.get("node") == "symbol":
                constants[node["identity"]] += 1
            for value in node.values():
                if isinstance(value, (dict, list)):
                    walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    for row in iter_corpus(path):
        rows += 1
        walk(row["state_before"])
        walk(row["state_after"])
        for name in row["action"]["external_premise_refs"]:
            constants[name] += 1
    return constants, rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--math", type=Path, default=DEFAULT_MATH)
    parser.add_argument("--corpus", type=Path,
                        default=ROOT / "data/corpus/lean_runtime_v2.canonical.jsonl.gz")
    parser.add_argument("--limit", type=int, default=12500)
    parser.add_argument("--out-dir", type=Path,
                        default=ROOT / "reports/representation_search")
    args = parser.parse_args()

    tokens, subjects, math_rows = read_math(args.math, args.limit)
    constants, corpus_rows = corpus_constants(args.corpus)
    joined = " ".join(constants)

    rows = []
    for construct, (latex, fragments) in CONSTRUCTS.items():
        human = sum(tokens.get(spelling, 0) for spelling in latex)
        matched = sorted({
            fragment for fragment in fragments if fragment in joined
        })
        occurrences = sum(
            count for name, count in constants.items()
            if any(fragment in name for fragment in fragments)
        )
        rows.append({
            "construct": construct,
            "latex_spellings": latex,
            "human_occurrences": human,
            "human_per_1k_problems": round(1000 * human / max(1, math_rows), 2),
            "mathlib_fragments_present": matched,
            "corpus_constant_occurrences": occurrences,
            "corpus_per_transition": round(occurrences / max(1, corpus_rows), 2),
            "covered": bool(matched),
        })
    for row in rows:
        # How much more often humans reach for this than the formal corpus does, after
        # normalising both sides by their own unit. A large ratio marks a construct the
        # search never really exercises even though it is nominally 'covered'.
        row["human_to_corpus_intensity"] = round(
            row["human_per_1k_problems"] / row["corpus_per_transition"], 1
        ) if row["corpus_per_transition"] > 0 else None
    rows.sort(key=lambda row: (
        row["human_to_corpus_intensity"] is None, -(row["human_to_corpus_intensity"] or 0)))
    covered = sum(1 for row in rows if row["covered"])
    under_exercised = [
        row for row in rows
        if (row["human_to_corpus_intensity"] or 0) >= 100 and row["human_occurrences"] >= 100
    ]

    payload = {
        "math_rows_read": math_rows,
        "math_subjects": dict(subjects.most_common()),
        "corpus_transitions": corpus_rows,
        "distinct_corpus_constants": len(constants),
        "constructs_checked": len(rows),
        "constructs_with_a_matching_constant_family": covered,
        "under_exercised_constructs": [row["construct"] for row in under_exercised],
        "rows": rows,
        "top_corpus_constants": constants.most_common(30),
        "epistemic_status": (
            "Lexical correspondence only. A match means the corpus mentions a Mathlib "
            "constant whose name contains the fragment; it does not mean the corpus proves "
            "anything about the construct, and no MATH solution is promoted to a verified "
            "transition."
        ),
    }
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "NOTATION_COVERAGE.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")

    lines = [
        "# Notation and Construct Coverage",
        "",
        "MATH is human-written natural-language mathematics. Its worked solutions are **not** "
        "promoted into verified transitions — they are unverified prose and `D-008` keeps "
        "that boundary. They answer a coverage question the formal corpus cannot answer about "
        "itself: which mathematical constructs does a representation search over "
        f"{corpus_rows} Lean transitions never see?",
        "",
        "**The correspondence below is lexical.** A construct counts as covered when the "
        "corpus mentions a Mathlib constant whose *name* contains a matching fragment. That "
        "is not autoformalization and is not a claim that the corpus proves anything about "
        "the construct.",
        "",
        f"Read {math_rows:,} MATH problems and their solutions; "
        f"{len(constants):,} distinct Mathlib constants appear in the corpus.",
        "",
        f"**{covered} of {len(rows)} constructs** have a matching constant family in the "
        "corpus, so a binary coverage table says almost nothing. The informative number is "
        "the **intensity ratio**: how much more often humans reach for a construct "
        "(per 1,000 MATH problems) than the corpus mentions it (per transition). A large "
        "ratio marks a construct that is nominally covered and effectively unexercised.",
        "",
        f"**{len(under_exercised)} constructs are under-exercised** by at least 100x: "
        + (", ".join(f"`{row['construct']}`" for row in under_exercised) or "none")
        + ".",
        "",
        "| Construct | LaTeX | MATH per 1k problems | Corpus per transition | Intensity ratio |",
        "|---|---|---:|---:|---:|",
    ]
    for row in rows:
        ratio = row["human_to_corpus_intensity"]
        lines.append(
            f"| {row['construct']} | `{' '.join(row['latex_spellings'])}` | "
            f"{row['human_per_1k_problems']:,} | {row['corpus_per_transition']} | "
            + ("—" if ratio is None else
               (f"**{ratio:,.0f}x**" if ratio >= 100 else f"{ratio:,.2f}x"))
            + " |"
        )
    lines += [
        "",
        "## MATH subject distribution",
        "",
        "| Subject | Problems |",
        "|---|---:|",
    ]
    for subject, count in subjects.most_common():
        lines.append(f"| {subject} | {count:,} |")
    lines += [
        "",
        "## What this does and does not license",
        "",
        "- It **does** identify constructs the search never exercises, which bounds any claim "
        "that a finalist representation is good for mathematics in general.",
        "- It **does not** license translating a MATH solution into a canonical transition. "
        "Doing that would need a verifier, and an unverified translation entering the corpus "
        "is precisely the contamination `D-008` exists to prevent.",
    ]
    (args.out_dir / "NOTATION_COVERAGE.md").write_text("\n".join(lines).rstrip() + "\n")
    print(f"wrote {args.out_dir}/NOTATION_COVERAGE.md")
    print(f"{covered}/{len(rows)} constructs covered; {len(constants)} distinct constants")


if __name__ == "__main__":
    main()
