#!/usr/bin/env python
"""EXPERIMENT 1 (`MISSION §28`): does changing information exposure change readability?

Six ModelViews of the same synthetic expression states, differing only in **what structural
information is exposed**, all written by one frozen serializer so no surface variable moves.
Plus a positive control that states the answer beside the question and a verified known-bad
whose parentage is genuinely `ABSENT`.

This is the experiment `D-025` implies. The 42-axis space could not vary content, so 106
generations of search over it produced invariant readability. Here content is the only thing
that varies.

    .venv/bin/python scripts/projection/run_expression_experiment.py
"""

from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hml_v3.micromath import calibration_v2 as C  # noqa: E402
from hml_v3.micromath import probe_v2 as P  # noqa: E402
from hml_v3.projection import audit as AU  # noqa: E402
from hml_v3.projection import expression as EX  # noqa: E402
from hml_v3.projection import model_view as MV  # noqa: E402
from hml_v3.projection import serialize as SZ  # noqa: E402
from hml_v3.projection import synthetic as SY  # noqa: E402

SYSTEM = """\
You read a structured view of a mathematical expression and answer one question about its
shape. Identifiers are opaque tags with no meaning beyond the structure relating them.

Answer with EXACTLY ONE of the options given, copied verbatim. No explanation, no
punctuation, no other words."""

#: The view under test, plus the two calibration arms.
ARMS = (EX.NESTED_ONLY, EX.EXPLICIT_EDGE_LIST, EX.LOCAL_SUBTREE, EX.DUAL_VIEW,
        EX.PATH_TO_ROOT, EX.DEPTH_ADAPTIVE)


def ask(model: str, rendered: str, question: str, options, answer: str,
        stated: str | None = None, timeout: int = 120):
    listed = "\n".join(f"- {o}" for o in options)
    fact = f"\n\nSTATED FACT (authoritative, use it): DEEPEST_REFERENCE = {stated}" if stated else ""
    user = (f"{rendered}\n\nQUESTION: {question}{fact}\n\nOPTIONS:\n{listed}\n\n"
            f"Answer with exactly one option, copied verbatim.")
    messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}]
    if any(m in model.lower() for m in P.THINKING_MARKERS):
        messages.append({"role": "assistant", "content": P.EMPTY_THINK_PREFILL})
    import subprocess
    payload = {"model": model, "messages": messages, "stream": False,
               "options": {"temperature": 0.0, "num_predict": 24}}
    try:
        result = subprocess.run(
            ["curl", "-s", "--max-time", str(timeout),
             "http://localhost:11434/api/chat", "-d", json.dumps(payload)],
            capture_output=True, text=True, check=True, timeout=timeout + 20)
        raw = json.loads(result.stdout)["message"]["content"]
    except Exception as error:  # noqa: BLE001
        return None, False, f"{type(error).__name__}"[:60]
    predicted = P.parse_choice(raw, list(options))
    return predicted, predicted == answer, None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="qwen38-rvn:latest")
    parser.add_argument("--per-rung", type=int, default=8)
    parser.add_argument("--out", type=Path, default=ROOT / "reports/content_projection_v1")
    args = parser.parse_args()

    ladder = SY.build_ladder(per_rung=args.per_rung)
    broken = [e.state_id for e in ladder if SY.verify(e)]
    if broken:
        print(f"generator produced {len(broken)} invalid states; refusing to run")
        return 1
    print(f"ladder: {len(ladder)} verified states across {len(SY.LADDER)} rungs", flush=True)

    # ------------------------------------------------------------------ exposure audit
    sample = ladder[0]
    sample_options = EX.options_for(sample)
    sample_views = [EX.build(v, sample, sample_options) for v in EX.VIEWS]
    exposure = AU.audit_views(sample_views)
    print(f"information exposure audit: {exposure['status']}", flush=True)
    if exposure["status"] != "PASS":
        print(f"  disagreements in {exposure['failing']}; refusing to run")
        return 1
    known_bad = AU.verify_known_bad(
        [v for v in sample_views if v.label == EX.FLATTENED_BAG][0], MV.EXPRESSION_PARENT)
    print(f"known-bad FLATTENED_BAG: {known_bad['status']}", flush=True)
    if not known_bad["hides_the_relation"]:
        print("  the known-bad does not hide the relation; refusing to run (FM-051)")
        return 1

    # Views must differ in content, or they are the same experiment run twice.
    by_label = {v.label: v for v in sample_views}
    distinct: dict[str, list[str]] = {}
    for left in ARMS:
        for right in ARMS:
            if left < right:
                shared = AU.differ_in_content(by_label[left], by_label[right])
                if not shared:
                    distinct.setdefault(left, []).append(right)
    if distinct:
        print(f"  note: views with identical exposure: {distinct}", flush=True)

    started = time.time()
    results: dict[str, dict] = {}
    args.out.mkdir(parents=True, exist_ok=True)

    def run_arm(label: str, builder, stated: bool = False) -> dict:
        per_rung: dict[str, list[bool]] = collections.defaultdict(list)
        costs: list[int] = []
        for state in ladder:
            options = EX.options_for(state)
            view = builder(state, options)
            rendered = SZ.render(view)
            costs.append(MV.cost_of(view, rendered).characters)
            question, _ = EX.question(options)
            _pred, correct, _err = ask(
                args.model, rendered, question, options, state.deepest,
                stated=state.deepest if stated else None)
            per_rung[state.rung].append(correct)
        flat = [c for v in per_rung.values() for c in v]
        return {
            "label": label,
            "accuracy": round(sum(flat) / len(flat), 4) if flat else 0.0,
            "items": len(flat),
            "by_rung": {r: round(sum(v) / len(v), 4) for r, v in sorted(per_rung.items())},
            "items_by_rung": {r: len(v) for r, v in sorted(per_rung.items())},
            "mean_characters": round(sum(costs) / len(costs)) if costs else 0,
            "per_item": {r: v for r, v in sorted(per_rung.items())},
        }

    plans = [
        ("EXPLICIT_POSITIVE",
         lambda s, o: EX.build(EX.NESTED_ONLY, s, o), True),
        ("ABLATED_NEGATIVE",
         lambda s, o: EX.build(EX.FLATTENED_BAG, s, o), False),
    ] + [(v, (lambda view: (lambda s, o: EX.build(view, s, o)))(v), False) for v in ARMS]

    for label, builder, stated in plans:
        record = run_arm(label, builder, stated)
        results[label] = record
        print(f"  {label:<20}{record['accuracy']:.3f}  "
              f"({record['items']} items, {record['mean_characters']} chars) "
              f"by rung {record['by_rung']}  ({time.time() - started:.0f}s)", flush=True)
        (args.out / "EXPRESSION_RESULTS.json").write_text(json.dumps({
            "model": args.model, "generator": SY.GENERATOR_VERSION,
            "ladder": [list(r) for r in SY.LADDER],
            "per_rung": args.per_rung,
            "exposure_audit": exposure, "known_bad": known_bad,
            "exposure_matrix": AU.exposure_matrix(sample_views),
            "elapsed_seconds": round(time.time() - started, 1),
            "arms": results}, indent=2, sort_keys=True) + "\n")

    # ------------------------------------------------------------------------ verdicts
    positive = results["EXPLICIT_POSITIVE"]["accuracy"]
    negative = results["ABLATED_NEGATIVE"]["accuracy"]
    chance = 0.25
    print(f"\ninstrument: positive {positive:.3f}, negative {negative:.3f}, "
          f"chance {chance:.3f}", flush=True)
    baseline = results[EX.NESTED_ONLY]["accuracy"]
    print(f"baseline (NESTED_ONLY, the conventional rendering): {baseline:.3f}\n")
    for view in ARMS:
        record = results[view]
        left = [c for r in record["per_item"] for c in record["per_item"][r]]
        right = [c for r in results[EX.NESTED_ONLY]["per_item"]
                 for c in results[EX.NESTED_ONLY]["per_item"][r]]
        status, reason, decided = C.compare(left, right)
        record["vs_nested"] = {"status": status, "reason": reason, "decisive": decided}
        print(f"  {view:<20}{record['accuracy']:.3f}  vs NESTED_ONLY: {status} — {reason}",
              flush=True)

    (args.out / "EXPRESSION_RESULTS.json").write_text(json.dumps({
        "model": args.model, "generator": SY.GENERATOR_VERSION,
        "ladder": [list(r) for r in SY.LADDER], "per_rung": args.per_rung,
        "exposure_audit": exposure, "known_bad": known_bad,
        "exposure_matrix": AU.exposure_matrix(sample_views),
        "instrument": {"positive": positive, "negative": negative, "chance": chance},
        "elapsed_seconds": round(time.time() - started, 1),
        "arms": results}, indent=2, sort_keys=True) + "\n")
    print(f"\nwrote {args.out}/EXPRESSION_RESULTS.json in {time.time() - started:.0f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
