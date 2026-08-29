#!/usr/bin/env python
"""Build MicroMath Lab V2: fresh splits behind a base-state firewall.

`MISSION §10`. The V1 holdouts are spent (`FM-043`) and are retired here rather than reused.
V2 splits are minted from base states that no prior run has consumed, registered by
provenance hash, and enforced by :class:`SplitFirewall` -- so a script that asks for the
wrong split by name still cannot reach the mathematics behind it.

    .venv/bin/python scripts/micromath/build_lab_v2.py
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

from hml_v3.micromath import instruments_v2 as IV2  # noqa: E402
from hml_v3.micromath import stresses as S  # noqa: E402
from hml_v3.micromath.candidates import load_controls  # noqa: E402
from hml_v3.micromath.corpus import load_base_pool, load_split  # noqa: E402
from hml_v3.micromath.domains import classify  # noqa: E402
from hml_v3.micromath.firewall import DEV, HIDDEN, SHADOW, SplitFirewall  # noqa: E402
from hml_v3.representation_search.corpus import write_corpus  # noqa: E402

#: `MISSION §21`: same-domain distractors. Capped so the opaque tags stay short -- a pool of
#: 500 forces four-digit tags, which costs tokens on every page for no gain in plausibility.
PREMISE_POOL_CAP = 40

#: A rendering the reader cannot fit is not a measurement (`FM-040`). Measured under the
#: strongest control; 14k characters is roughly 4.4k tokens, leaving room for the question
#: and the options inside a 7k window.
MAX_RENDERED_CHARS = 14000

#: Deterministic 4-slot cycle, applied within each stress stratum.
CYCLE = (DEV, DEV, SHADOW, HIDDEN)

#: Rarest structures first. MULTI_GOAL and SCOPE need several populated goals, and
#: ACTION_ARGUMENT needs a resolved argument alongside an unused declaration; all three are
#: far rarer than BINDER or TYPE and must claim their base states before the common ones do.
SCARCITY_ORDER = (S.ACTION_ARGUMENT, S.MULTI_GOAL, S.SCOPE, S.PREMISE,
                  S.EXPRESSION_DEPTH, S.DEPENDENCY, S.TYPE, S.BINDER)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path,
                        default=ROOT / "data/corpus/lean_runtime_v2_full.canonical.jsonl.gz")
    parser.add_argument("--v1-lab", type=Path, default=ROOT / "data/micromath_lab_v1")
    parser.add_argument("--out", type=Path, default=ROOT / "data/micromath_lab_v2")
    parser.add_argument("--per-stress", type=int, default=96,
                        help="items to mint per stress before splitting 2:1:1")
    args = parser.parse_args()

    started = time.time()
    pool, provenance = load_base_pool(args.corpus)
    print(f"pool: {len(pool)} base states available", flush=True)

    firewall = SplitFirewall()

    # ---------------------------------------------------------------- retire V1 (FM-043)
    by_id = {t["transition_id"]: t for t in pool}
    retired_counts = {}
    for name in ("micro_dev", "micro_shadow", "micro_hidden"):
        rows = load_split(args.v1_lab, name)
        spent = [by_id[r["base_transition_id"]] for r in rows
                 if r.get("base_transition_id") in by_id]
        retired_counts[name] = firewall.retire(f"V1_{name.upper()}", spent)
    print(f"retired V1 base states: {retired_counts}", flush=True)

    available = firewall.available(pool)
    print(f"available after retirement: {len(available)}", flush=True)

    # ------------------------------------------------------------- same-domain premises
    premises: dict[str, set[str]] = collections.defaultdict(set)
    for transition in available:
        domain, _confidence = classify(transition)
        premises[domain].update(
            (transition.get("action") or {}).get("external_premise_refs") or [])
    premise_pools = {domain: sorted(names)[:PREMISE_POOL_CAP]
                     for domain, names in premises.items()}
    print("premise pools: "
          + ", ".join(f"{d}={len(p)}" for d, p in sorted(premise_pools.items())), flush=True)

    # ------------------------------------------------------------------- size budget
    control = {c.label: c for c in load_controls()}["TYPED_AST"]
    sized: list[dict] = []
    oversize = 0
    for transition in available:
        try:
            if len(control.compiler.render_text(transition)) <= MAX_RENDERED_CHARS:
                sized.append(transition)
            else:
                oversize += 1
        except Exception:  # noqa: BLE001
            oversize += 1
    print(f"within the {MAX_RENDERED_CHARS}-char budget: {len(sized)} "
          f"({oversize} too large or unrenderable)", flush=True)

    # ----------------------------------------------------------------------- build items
    # A base state may carry several stresses -- BINDER, TYPE and DEPENDENCY often live in
    # the same state -- and forbidding that starved the scarce stresses: the common ones
    # claimed every state first and MULTI_GOAL, SCOPE and ACTION_ARGUMENT were left with
    # what remained. Splits are therefore assigned BY BASE STATE below, so every item drawn
    # from one state travels together and the firewall invariant survives the sharing.
    items_by_stress: dict[str, list] = collections.defaultdict(list)
    rejected: collections.Counter = collections.Counter()
    # Scarce stresses first, so they get their pick of the pool rather than its leftovers.
    order = sorted(S.STRESSES, key=lambda s: SCARCITY_ORDER.index(s))
    for stress in order:
        for transition in sized:
            if len(items_by_stress[stress]) >= args.per_stress:
                break
            domain, confidence = classify(transition)
            try:
                item = IV2.build(transition, stress, domain, confidence,
                                 premise_pools.get(domain, []))
            except IV2.NotEligible as error:
                rejected[(stress, str(error)[:48])] += 1
                continue
            except Exception as error:  # noqa: BLE001
                rejected[(stress, f"ERROR {type(error).__name__}")] += 1
                continue
            items_by_stress[stress].append(item)

    total = sum(len(v) for v in items_by_stress.values())
    print(f"\nminted {total} items across {len(items_by_stress)} stresses", flush=True)
    for stress in S.STRESSES:
        print(f"  {stress:<18}{len(items_by_stress[stress]):>4}", flush=True)

    # ---------------------------------------------------------------------- split & register
    buckets: dict[str, list] = {DEV: [], SHADOW: [], HIDDEN: []}
    assigned: dict[str, str] = {}
    for stress in sorted(items_by_stress):
        ordered = sorted(items_by_stress[stress], key=lambda i: i.item_id)
        for index, item in enumerate(ordered):
            # Assignment is keyed on the base state, not the item, so a state shared by
            # several stresses cannot straddle two splits. This is the FM-043 invariant
            # expressed at construction time rather than checked afterwards.
            target = assigned.get(item.base_transition_id)
            if target is None:
                target = CYCLE[index % len(CYCLE)]
                assigned[item.base_transition_id] = target
            buckets[target].append(item)

    for compartment, items in buckets.items():
        seen: set[str] = set()
        records = []
        for item in items:
            if item.base_transition_id in seen:
                continue
            seen.add(item.base_transition_id)
            records.append({"transition_id": item.base_transition_id,
                            "source_specific_reference": item.source_file,
                            "provenance": {}})
        firewall.register(compartment, records)
    firewall.assert_disjoint()

    args.out.mkdir(parents=True, exist_ok=True)
    names = {DEV: "micro_dev_v2", SHADOW: "micro_shadow_v2", HIDDEN: "micro_hidden_v2"}
    for compartment, label in names.items():
        write_corpus([i.to_dict() for i in sorted(buckets[compartment],
                                                  key=lambda i: i.item_id)],
                     args.out / f"{label}.jsonl.gz")
    firewall.save(args.out / "firewall.json")

    def profile(items: list) -> dict:
        return {
            "count": len(items),
            "by_stress": dict(sorted(collections.Counter(i.stress for i in items).items())),
            "by_domain": dict(sorted(collections.Counter(i.domain for i in items).items())),
            "by_options": dict(sorted(
                collections.Counter(len(i.options) for i in items).items())),
            "distinct_base_states": len({i.base_transition_id for i in items}),
        }

    manifest = {
        "lab_version": IV2.LAB_VERSION,
        "built_seconds": round(time.time() - started, 1),
        "corpus_provenance": provenance,
        "retired_v1_base_states": retired_counts,
        "retired_reason": "FM-043: consumed by the V1 certification top-up; spent as holdouts",
        "available_after_retirement": len(available),
        "size_budget_chars": MAX_RENDERED_CHARS,
        "within_budget": len(sized),
        "premise_pool_cap": PREMISE_POOL_CAP,
        "premise_pools": {d: len(p) for d, p in sorted(premise_pools.items())},
        "splits": {names[c]: profile(buckets[c]) for c in (DEV, SHADOW, HIDDEN)},
        "base_state_overlap": {
            "dev_shadow": len({i.base_transition_id for i in buckets[DEV]}
                              & {i.base_transition_id for i in buckets[SHADOW]}),
            "dev_hidden": len({i.base_transition_id for i in buckets[DEV]}
                              & {i.base_transition_id for i in buckets[HIDDEN]}),
            "shadow_hidden": len({i.base_transition_id for i in buckets[SHADOW]}
                                 & {i.base_transition_id for i in buckets[HIDDEN]}),
        },
        "sealed_final_v2": "NOT OPENED",
        "top_rejections": [{"stress": s, "reason": r, "count": n}
                           for (s, r), n in rejected.most_common(15)],
    }
    (args.out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")

    print("\nsplits:")
    for compartment in (DEV, SHADOW, HIDDEN):
        p = profile(buckets[compartment])
        print(f"  {names[compartment]:<18}{p['count']:>4} items, "
              f"{p['distinct_base_states']} base states, options {p['by_options']}")
    print(f"\nbase-state overlap: {manifest['base_state_overlap']}")
    print(f"wrote {args.out} in {manifest['built_seconds']}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
