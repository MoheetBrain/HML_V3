#!/bin/sh
set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
python3 "$repo_root/scripts/acquire/clone_pinned.py" \
  --name openai_prm800k \
  --url https://github.com/openai/prm800k.git \
  --commit 7ecc794703b2877f63226f2477a49b34f9b25163 \
  --destination "$repo_root/external/checkouts/prm800k" \
  --lfs-skip
