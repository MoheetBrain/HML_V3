#!/usr/bin/env python
"""Regenerate the ablated state for named stresses, in place.

When an ablation is found not to destroy its relation (`FM-050`), the fix belongs in
`ablate` -- but rebuilding the whole lab to apply it would re-run eligibility and reshuffle
every split, invalidating results for components that were measured correctly. If every
affected item survives the new ablation, only the `ablated` field needs rewriting, and the
splits, the item ids and every other component's numbers are untouched.

The script refuses to write unless EVERY item of the named stresses survives, because a
partial rewrite would silently drop items and change the very assignment it exists to
preserve.

    .venv/bin/python scripts/micromath/reablate_v2.py --stresses BINDER
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hml_v3.micromath import ablate  # noqa: E402
from hml_v3.micromath import instruments_v2 as IV2  # noqa: E402
from hml_v3.micromath import stresses as S  # noqa: E402
from hml_v3.micromath.corpus import load_split  # noqa: E402
from hml_v3.representation_search.corpus import write_corpus  # noqa: E402

SPLITS = ("micro_dev_v2", "micro_shadow_v2", "micro_hidden_v2")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lab", type=Path, default=ROOT / "data/micromath_lab_v2")
    parser.add_argument("--stresses", default=S.BINDER)
    args = parser.parse_args()
    wanted = {s.strip() for s in args.stresses.split(",") if s.strip()}

    loaded = {name: [IV2.MicroItem.from_dict(r) for r in load_split(args.lab, name)]
              for name in SPLITS}
    changed = refused = 0
    for name, items in loaded.items():
        for item in items:
            if item.stress not in wanted:
                continue
            seed = IV2._seed(item.base_transition_id)
            try:
                fresh = ablate.ablate(item.stress, item.state, seed)
            except ablate.AblationFailed as error:
                print(f"  REFUSED {item.item_id} ({item.stress}): {error}")
                refused += 1
                continue
            if not ablate.changed(item.state, fresh):
                print(f"  REFUSED {item.item_id}: the new ablation is a no-op")
                refused += 1
                continue
            item.ablated = fresh
            changed += 1

    if refused:
        print(f"\n{refused} items would be lost; refusing to write. Rebuild the lab instead "
              f"so eligibility and splits are recomputed consistently.")
        return 1

    for name, items in loaded.items():
        write_corpus([i.to_dict() for i in sorted(items, key=lambda i: i.item_id)],
                     args.lab / f"{name}.jsonl.gz")
    print(f"\nrewrote the ablated state of {changed} items across {len(SPLITS)} splits; "
          f"item ids, splits and every other component are unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
