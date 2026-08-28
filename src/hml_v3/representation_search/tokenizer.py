"""Deterministic, offline token accounting.

Two independent measurements are reported for every rendering, because neither alone is
honest:

``pretokens``
    A tokenizer-free segmentation using the GPT-2 pre-tokenization regex. It depends on no
    vocabulary, so it cannot favour whichever language a vocabulary was trained on.

``bpe_tokens``
    Real GPT-2 byte-level BPE with the pinned 50,257-entry vocabulary. This is a *proxy*: it
    prices a representation under one pretrained English-heavy vocabulary. FM-004 recorded
    that vocabulary effects can be worth more than every syntax difference combined, so the
    measurement matters — but it is never presented as the segmentation a future model will
    use.

The implementation is pure standard library and fully deterministic.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
import re
from typing import Iterable

TOKENIZER_DIR = Path(__file__).resolve().parents[3] / "data/tokenizer/gpt2"

# The GPT-2 pre-tokenization pattern. Python's `re` lacks `\p{L}`/`\p{N}`, so the Unicode
# classes are expressed with the equivalent `[^\W\d_]` / `\d` under the default Unicode
# semantics of `str` patterns.
PRETOKEN_PATTERN = re.compile(
    r"""'s|'t|'re|'ve|'m|'ll|'d| ?[^\W\d_]+| ?\d+| ?[^\s\w]+|\s+(?!\S)|\s+"""
)


def _bytes_to_unicode() -> dict[int, str]:
    printable = (
        list(range(ord("!"), ord("~") + 1))
        + list(range(ord("\xa1"), ord("\xac") + 1))
        + list(range(ord("\xae"), ord("\xff") + 1))
    )
    mapped = list(printable)
    shift = 0
    for code in range(2**8):
        if code not in printable:
            printable.append(code)
            mapped.append(2**8 + shift)
            shift += 1
    return dict(zip(printable, (chr(value) for value in mapped)))


def pretokens(text: str) -> list[str]:
    return PRETOKEN_PATTERN.findall(text)


class GPT2Tokenizer:
    """Byte-level BPE, faithful to the reference implementation."""

    def __init__(self, directory: Path = TOKENIZER_DIR) -> None:
        self.encoder: dict[str, int] = json.loads((directory / "encoder.json").read_text())
        merges = (directory / "vocab.bpe").read_text(encoding="utf-8").split("\n")[1:-1]
        self.ranks = {
            tuple(line.split()): index for index, line in enumerate(merges) if line
        }
        self.byte_encoder = _bytes_to_unicode()
        self._cache: dict[str, tuple[str, ...]] = {}

    def _merge(self, token: str) -> tuple[str, ...]:
        cached = self._cache.get(token)
        if cached is not None:
            return cached
        word = tuple(token)
        if len(word) > 1:
            while True:
                pairs = {(word[i], word[i + 1]) for i in range(len(word) - 1)}
                candidate = min(pairs, key=lambda pair: self.ranks.get(pair, float("inf")))
                if candidate not in self.ranks:
                    break
                first, second = candidate
                merged: list[str] = []
                index = 0
                while index < len(word):
                    try:
                        found = word.index(first, index)
                    except ValueError:
                        merged.extend(word[index:])
                        break
                    merged.extend(word[index:found])
                    index = found
                    if index < len(word) - 1 and word[index + 1] == second:
                        merged.append(first + second)
                        index += 2
                    else:
                        merged.append(word[index])
                        index += 1
                word = tuple(merged)
                if len(word) == 1:
                    break
        self._cache[token] = word
        return word

    def encode_pieces(self, text: str) -> list[str]:
        pieces: list[str] = []
        for token in pretokens(text):
            mapped = "".join(self.byte_encoder[byte] for byte in token.encode("utf-8"))
            pieces.extend(self._merge(mapped))
        return pieces

    def encode(self, text: str) -> list[int]:
        return [self.encoder[piece] for piece in self.encode_pieces(text)]

    def count(self, text: str) -> int:
        total = 0
        for token in pretokens(text):
            mapped = "".join(self.byte_encoder[byte] for byte in token.encode("utf-8"))
            total += len(self._merge(mapped))
        return total

    def offsets(self, text: str) -> list[tuple[int, int]]:
        """Character span of each emitted token, for character/token distance metrics."""

        spans: list[tuple[int, int]] = []
        cursor = 0
        for token in pretokens(text):
            start = text.index(token, cursor)
            cursor = start + len(token)
            merged = self._merge("".join(self.byte_encoder[b] for b in token.encode("utf-8")))
            # Distribute the token's characters across its BPE pieces by decoded byte length.
            offset = start
            for piece in merged:
                length = max(1, round(len(piece) * len(token) / max(1, sum(len(p) for p in merged))))
                spans.append((offset, min(cursor, offset + length)))
                offset = min(cursor, offset + length)
            if spans:
                spans[-1] = (spans[-1][0], cursor)
        return spans


@lru_cache(maxsize=1)
def tokenizer() -> GPT2Tokenizer:
    return GPT2Tokenizer()


def token_count(text: str) -> int:
    return tokenizer().count(text)


def fragmentation(words: Iterable[str]) -> float:
    """Mean BPE pieces per supplied word. 1.0 means every word is a single token."""

    encoder = tokenizer()
    words = [word for word in words if word]
    if not words:
        return 0.0
    return sum(len(encoder.encode_pieces(word)) for word in words) / len(words)
