#!/bin/sh
set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
python3 "$repo_root/scripts/acquire/clone_pinned.py" \
  --name proofnet_lean4 \
  --url https://github.com/kripner/proofnet.git \
  --commit 5da820b6510cd2a1d4237036d8227357cb9944d9 \
  --destination "$repo_root/external/checkouts/proofnet-lean4"
