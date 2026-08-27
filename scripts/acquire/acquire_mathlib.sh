#!/bin/sh
set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
python3 "$repo_root/scripts/acquire/clone_pinned.py" \
  --name mathlib_leandojo_benchmark4 \
  --url https://github.com/leanprover-community/mathlib4.git \
  --commit 29dcec074de168ac2bf835a77ef68bbe069194c5 \
  --destination "$repo_root/external/checkouts/mathlib4-29dcec0"
