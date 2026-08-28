#!/bin/sh
# Reproducible acquisition of the pinned GPT-2 BPE tokenizer assets.
# The files are small, MIT-licensed and committed; this script exists so the pin is
# verifiable rather than trusted.
set -eu
DEST="$(dirname "$0")/../../data/tokenizer/gpt2"
mkdir -p "$DEST"
curl -sSL -o "$DEST/encoder.json" \
  https://openaipublic.blob.core.windows.net/gpt-2/models/117M/encoder.json
curl -sSL -o "$DEST/vocab.bpe" \
  https://openaipublic.blob.core.windows.net/gpt-2/models/117M/vocab.bpe
printf '%s  %s\n' 196139668be63f3b5d6574427317ae82f612a97c5d1cdaf36ed2256dbf636783 "$DEST/encoder.json" | shasum -a 256 -c -
printf '%s  %s\n' 1ce1664773c50f3e0cc8842619a93edc4624525b728b188a9e0be33b7726adc5 "$DEST/vocab.bpe" | shasum -a 256 -c -
