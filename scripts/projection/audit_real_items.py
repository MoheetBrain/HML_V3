#!/usr/bin/env python
"""REAL_LEAN_GAP_V1 §1: audit the real EXPRESSION_DEPTH task before explaining its result.

Every EXPRESSION_DEPTH dev item is checked against the document the reader actually saw:

    target occurrence   the answer identity occurs in the goal target
    unique answer       one identity is strictly deepest, by key and by rendered nesting
    occurrence form     the question is about identities by deepest occurrence, so a
                        recurring identity is not ambiguous; recorded, not assumed
    option fidelity     every option occurs in the rendered target, encodes to a distinct
                        token, and round-trips through the answer parser
    no codec mismatch   rendered ordering of the options by depth equals the key ordering
    relation present    the target is rendered as nested structure, not a flat bag

No model is consulted. The output is a per-item verdict and a profile of the regime the
real items occupy, for the synthetic work to match.

    .venv/bin/python scripts/projection/audit_real_items.py
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import statistics
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hml_v3.micromath import probe_v2 as P  # noqa: E402
from hml_v3.micromath.candidates import load_controls  # noqa: E402
from hml_v3.projection import real_target as RT  # noqa: E402

CERTIFICATION_ITEMS = 12


def audit_item(item, compiler, used: bool) -> dict:
    rendered = compiler.render(item.state)
    encode = rendered.codec.encode
    options = list(item.options)
    encoded = [encode(o) for o in options]
    answer_enc = encode(item.answer)
    text = rendered.text
    target_line = RT.first_target_line(text)
    target = RT.goal_target(item)

    key = RT.key_depths(target)
    occurrences = RT.occurrence_depths(target)
    braces = RT.brace_depths(target_line)
    rendered_deep = {k: max(v) for k, v in braces.items()}
    paren_text = RT.render_paren(target)
    parens = RT.paren_depths(paren_text)
    paren_deep = {k: max(v) for k, v in parens.items()}

    # ---- uniqueness, three ways
    key_ranked = sorted(key.items(), key=lambda kv: (-kv[1], kv[0]))
    key_unique = len(key_ranked) >= 2 and key_ranked[0][1] > key_ranked[1][1]
    key_winner = key_ranked[0][0]
    render_best = max(rendered_deep.values()) if rendered_deep else None
    render_winners = [k for k, v in rendered_deep.items() if v == render_best]
    paren_best = max(paren_deep.get(k, -1) for k in key) if key else None
    paren_winners = [k for k in key if paren_deep.get(k) == paren_best]

    # ---- option fidelity
    options_in_target = [enc in target_line for enc in encoded]
    distinct_encoding = len(set(encoded)) == len(encoded)
    parse_ok = P.parse_choice(answer_enc, tuple(encoded)) == answer_enc
    containment = [(a, b) for a in encoded for b in encoded if a != b and a in b]

    # ---- codec / ordering agreement: rendered depth minus key depth must be one constant
    offsets = {o: rendered_deep.get(e, -10 ** 6) - key.get(o, 0) for o, e in zip(options, encoded)}
    offset_values = set(offsets.values())
    paren_offsets = {o: paren_deep.get(o, -10 ** 6) - key.get(o, 0) for o in options}

    # ---- regime profile
    context = RT.context_depths(item)
    answer_depth = key[item.answer]
    deeper_in_context = [o for o in options if context.get(o, -1) >= answer_depth]
    sites = sum(len(v) for v in occurrences.values())

    verdict = "VALID"
    reasons: list[str] = []
    if not key_unique or key_winner != item.answer:
        verdict, _ = "AMBIGUOUS", reasons.append("key does not single out the answer")
    if render_winners != [answer_enc]:
        verdict, _ = "AMBIGUOUS", reasons.append(
            f"rendered deepest is {render_winners}, key answer {answer_enc}")
    if paren_winners != [item.answer]:
        verdict, _ = "AMBIGUOUS", reasons.append(f"paren deepest is {paren_winners}")
    if not all(options_in_target):
        verdict, _ = "INVALID", reasons.append("an option is absent from the rendered target")
    if not distinct_encoding or not parse_ok or containment:
        verdict, _ = "INVALID", reasons.append("option encoding or parser round-trip fails")
    if len(offset_values) != 1:
        verdict, _ = "INVALID", reasons.append(f"rendered/key depth offsets differ: {offsets}")
    if set(paren_offsets.values()) != {0}:
        verdict, _ = "INVALID", reasons.append(f"paren/key depth offsets: {paren_offsets}")
    if "{ap|" not in target_line and "{lam|" not in target_line:
        verdict, _ = "INVALID", reasons.append("target is not rendered as nested structure")

    return {
        "item_id": item.item_id, "used_in_certification": used, "verdict": verdict,
        "reasons": reasons, "answer": item.answer, "answer_encoded": answer_enc,
        "options": options, "options_encoded": encoded,
        "key_depth_by_option": {o: key.get(o) for o in options},
        "rendered_depth_by_option": {o: rendered_deep.get(e) for o, e in zip(options, encoded)},
        "rendered_minus_key_offset": sorted(offset_values),
        "answer_occurrence_depths": sorted(occurrences.get(item.answer, []), reverse=True),
        "regime": {
            "document_chars": len(text), "target_chars": len(target_line),
            "target_copies_in_document": text.count(target_line) if target_line else 0,
            "paren_target_chars": len(paren_text),
            "sites": sites, "distinct_identities": len(key),
            "recurrence": round(sites / max(1, len(key)), 2),
            "max_occurrences_one_identity": max(len(v) for v in occurrences.values()),
            "answer_occurrences": len(occurrences.get(item.answer, [])),
            "depth": answer_depth, "lead": item.detail.get("lead"),
            "options_deeper_in_context_types": deeper_in_context,
            "answer_max_depth_in_context_types": context.get(item.answer),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lab", type=Path, default=ROOT / "data/micromath_lab_v2")
    parser.add_argument("--out", type=Path, default=ROOT / "reports/content_projection_v1")
    args = parser.parse_args()

    items = RT.load_expression_depth_items(args.lab)
    control = {c.label: c for c in load_controls()}["TYPED_AST"]
    records = [audit_item(item, control.compiler, index < CERTIFICATION_ITEMS)
               for index, item in enumerate(items)]

    verdicts = {v: sum(1 for r in records if r["verdict"] == v)
                for v in ("VALID", "AMBIGUOUS", "INVALID")}
    used = [r for r in records if r["used_in_certification"]]

    def profile(rows: list[dict], field: str) -> dict:
        values = [r["regime"][field] for r in rows if r["regime"][field] is not None]
        if not values:
            return {}
        return {"min": min(values), "median": statistics.median(values), "max": max(values),
                "mean": round(sum(values) / len(values), 2)}

    fields = ("document_chars", "target_chars", "target_copies_in_document", "sites",
              "distinct_identities", "recurrence", "max_occurrences_one_identity",
              "answer_occurrences", "depth", "lead")
    report = {
        "items_audited": len(records), "verdicts": verdicts,
        "certification_items_audited": len(used),
        "certification_verdicts": {v: sum(1 for r in used if r["verdict"] == v)
                                   for v in ("VALID", "AMBIGUOUS", "INVALID")},
        "rendered_minus_key_offsets_seen": sorted({o for r in records
                                                   for o in r["rendered_minus_key_offset"]}),
        "items_with_an_option_deeper_in_context_types": sum(
            1 for r in records if r["regime"]["options_deeper_in_context_types"]),
        "items_with_lead_1": sum(1 for r in records if r["regime"]["lead"] == 1),
        "regime_profile_all": {f: profile(records, f) for f in fields},
        "regime_profile_certification_12": {f: profile(used, f) for f in fields},
        "items": records,
    }
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "REAL_ITEM_AUDIT.json").write_text(json.dumps(report, indent=2) + "\n")

    print(f"REAL_ITEMS_AUDITED {len(records)}  (certification subset {len(used)})")
    print(f"AMBIGUOUS_ITEMS    {verdicts['AMBIGUOUS']}")
    print(f"INVALID_ITEMS      {verdicts['INVALID']}")
    print(f"rendered-minus-key depth offset(s) seen: {report['rendered_minus_key_offsets_seen']}")
    print(f"items with lead 1: {report['items_with_lead_1']}/{len(records)}; items with an "
          f"option deeper in a context type than the answer is in the target: "
          f"{report['items_with_an_option_deeper_in_context_types']}")
    for field in fields:
        print(f"  {field:<32}{report['regime_profile_all'][field]}")
    for record in records:
        if record["verdict"] != "VALID":
            print(f"  {record['verdict']:<10}{record['item_id']}  {record['reasons']}")
    print(f"wrote {args.out}/REAL_ITEM_AUDIT.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
