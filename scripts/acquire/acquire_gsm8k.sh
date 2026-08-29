#!/bin/sh
set -eu

# GSM8K — grade-school word problems with natural-language solutions.
#
# This is NOT formal evidence. It carries no Lean, no proof term, and no verifier: its
# answers are human-written arithmetic narratives. It is registered so that natural-language
# mathematics has a named, pinned source instead of being invoked informally, and the
# registry marks it not_lean_truth so nothing can promote it into the formal tier.

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
python3 "$repo_root/scripts/acquire/clone_pinned.py" \
  --name openai_gsm8k \
  --url https://github.com/openai/grade-school-math.git \
  --commit 3101c7d5072418e28b9008a6636bde82a006892c \
  --destination "$repo_root/external/checkouts/grade-school-math"
