#!/bin/sh
set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
python3 "$repo_root/scripts/acquire/clone_pinned.py" \
  --name minif2f_lean4 \
  --url https://github.com/google-deepmind/miniF2F.git \
  --commit f0a20e14c1eeccd859d51bb4c2b3ee487889c303 \
  --destination "$repo_root/external/checkouts/miniF2F"
