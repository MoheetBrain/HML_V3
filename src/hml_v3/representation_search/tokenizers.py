"""Multi-tokenizer accounting.

`FM-018` recorded that the escaping penalty reproduces across vocabularies while the absolute
token counts do not: every mathematical glyph the corpus needs is one token under Qwen3-8B
and two or three under GPT-2. Optimising against a single vocabulary therefore risks
selecting for that vocabulary rather than for the representation.

This module prices every finalist under several tokenizers and separates the two kinds of
result: an ordering that survives every vocabulary is a property of the representation, and
one that flips is a property of the vocabulary.

Tokenizers are loaded from whatever is locally available. A vocabulary that cannot be loaded
is reported as unavailable rather than silently skipped, because "we did not check" and "it
agreed" must never look the same.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
import re
from typing import Any, Callable

from hml_v3.representation_search.tokenizer import GPT2Tokenizer, pretokens

ROOT = Path(__file__).resolve().parents[3]

#: The glyph family FM-004 and FM-018 priced. Kept explicit so the audit is comparable.
MATH_GLYPHS = ("⊢", "∀", "∃", "ℝ", "ℕ", "ℤ", "𝕜", "✝", "≠", "→", "↔", "∈", "⁻¹")


@dataclass
class TokenizerReport:
    name: str
    available: bool
    tokens_per_transition: float = 0.0
    identifier_fragmentation: float = 0.0
    role_word_fragmentation: float = 0.0
    math_glyph_tokens: dict[str, int] = field(default_factory=dict)
    note: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "available": self.available,
            "tokens_per_transition": round(self.tokens_per_transition, 3),
            "identifier_fragmentation": round(self.identifier_fragmentation, 4),
            "role_word_fragmentation": round(self.role_word_fragmentation, 4),
            "math_glyph_tokens": self.math_glyph_tokens,
            "note": self.note,
        }


class HFByteLevelBPE:
    """Exact byte-level BPE for a HuggingFace ``tokenizer.json`` with a merge table.

    Not a proxy: this replays the model's own merge sequence in rank order, the same
    algorithm the reference GPT-2 implementation uses. Qwen2.5, GPT-NeoX and StarCoder2 are
    all byte-level BPE, so one implementation prices all of them exactly.
    """

    def __init__(self, payload: dict[str, Any], name: str) -> None:
        model = payload["model"]
        self.name = name
        self.vocab: dict[str, int] = model["vocab"]
        merges = model["merges"]
        pairs = (
            [tuple(item) if isinstance(item, list) else tuple(item.split(" ", 1))
             for item in merges]
        )
        self.ranks = {pair: index for index, pair in enumerate(pairs) if len(pair) == 2}
        self.byte_encoder = _bytes_to_unicode()
        self._cache: dict[str, int] = {}

    def _merge_count(self, token: str) -> int:
        cached = self._cache.get(token)
        if cached is not None:
            return cached
        word = tuple(token)
        while len(word) > 1:
            candidate = min(
                {(word[i], word[i + 1]) for i in range(len(word) - 1)},
                key=lambda pair: self.ranks.get(pair, float("inf")),
            )
            if candidate not in self.ranks:
                break
            first, second = candidate
            merged: list[str] = []
            index = 0
            while index < len(word):
                if (index < len(word) - 1 and word[index] == first
                        and word[index + 1] == second):
                    merged.append(first + second)
                    index += 2
                else:
                    merged.append(word[index])
                    index += 1
            word = tuple(merged)
        self._cache[token] = len(word)
        return len(word)

    def count(self, text: str) -> int:
        total = 0
        for token in pretokens(text):
            mapped = "".join(self.byte_encoder[byte] for byte in token.encode("utf-8"))
            total += self._merge_count(mapped)
        return total


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


IDENTIFIER = re.compile(r"[^\W\d][\w.]*", re.UNICODE)


def _load_gpt2() -> Callable[[str], int] | None:
    try:
        encoder = GPT2Tokenizer()
    except Exception:  # noqa: BLE001
        return None
    return encoder.count


def _load_vocab_file(path: Path, name: str) -> Callable[[str], int] | None:
    """Load a HuggingFace byte-level BPE tokenizer.json if one is present locally.

    Vocabularies are stored gzipped: Qwen2.5's is 6.7 MB raw, over the repository's
    tracked-file limit, and these are the artifacts that make the multi-tokenizer audit
    reproducible rather than a claim.
    """

    compressed = path.with_suffix(path.suffix + ".gz")
    try:
        if compressed.exists():
            import gzip

            with gzip.open(compressed, "rt", encoding="utf-8") as handle:
                payload = json.load(handle)
        elif path.exists():
            payload = json.loads(path.read_text())
        else:
            return None
    except Exception:  # noqa: BLE001
        return None
    model = payload.get("model") if isinstance(payload, dict) else None
    if not isinstance(model, dict) or model.get("type") != "BPE":
        return None
    if not model.get("merges") or not model.get("vocab"):
        return None
    return HFByteLevelBPE(payload, name).count


def available_tokenizers(search_paths: dict[str, Path] | None = None) -> dict[str, Any]:
    """Every tokenizer this machine can actually run, plus why the others are missing."""

    found: dict[str, Any] = {}
    gpt2 = _load_gpt2()
    found["gpt2"] = {
        "count": gpt2,
        "available": gpt2 is not None,
        "note": "pinned GPT-2 byte-level BPE, exact reference implementation",
    }
    defaults = {
        "qwen25": ROOT / "data/tokenizer/qwen25/tokenizer.json",
        "gptneox": ROOT / "data/tokenizer/gptneox/tokenizer.json",
        "starcoder2": ROOT / "data/tokenizer/starcoder2/tokenizer.json",
        # Gemma's tokenizer is gated on HuggingFace and returned HTTP 401. It is listed so
        # the report says "not checked" rather than leaving a silent gap.
        "gemma": ROOT / "data/tokenizer/gemma/tokenizer.json",
    }
    for name, path in (search_paths or defaults).items():
        counter = _load_vocab_file(path, name)
        found[name] = {
            "count": counter,
            "available": counter is not None,
            "note": (
                "exact byte-level BPE replayed from the model's own merge table"
                if counter is not None
                else f"no local vocabulary at {path}"
            ),
        }
    return found


def audit(
    renderings: list[str], role_words: list[str],
    tokenizers: dict[str, Any] | None = None,
) -> dict[str, TokenizerReport]:
    """Price a candidate's renderings under every available vocabulary."""

    tokenizers = tokenizers or available_tokenizers()
    reports: dict[str, TokenizerReport] = {}
    identifiers = [
        name for text in renderings[:8] for name in IDENTIFIER.findall(text)
    ][:4000]
    for name, entry in tokenizers.items():
        if not entry["available"]:
            reports[name] = TokenizerReport(name, False, note=entry["note"])
            continue
        count = entry["count"]
        total = sum(count(text) for text in renderings)
        reports[name] = TokenizerReport(
            name=name, available=True,
            tokens_per_transition=total / max(1, len(renderings)),
            identifier_fragmentation=(
                sum(count(item) for item in identifiers) / max(1, len(identifiers))
            ),
            role_word_fragmentation=(
                sum(count(word) for word in role_words) / max(1, len(role_words))
            ),
            math_glyph_tokens={glyph: count(glyph) for glyph in MATH_GLYPHS},
            note=entry["note"],
        )
    return reports


def ordering_agreement(
    per_candidate: dict[str, dict[str, TokenizerReport]],
) -> dict[str, Any]:
    """Does the token-cost ranking survive a change of vocabulary?

    Returns the ranking under each vocabulary and whether the cheapest candidate is the same
    one throughout. A ranking that flips is a vocabulary effect and must not be reported as a
    property of the representation.
    """

    rankings: dict[str, list[str]] = {}
    for name in {
        tokenizer_name
        for reports in per_candidate.values()
        for tokenizer_name, report in reports.items() if report.available
    }:
        ordered = sorted(
            (candidate for candidate, reports in per_candidate.items()
             if reports.get(name) and reports[name].available),
            key=lambda candidate: per_candidate[candidate][name].tokens_per_transition,
        )
        if ordered:
            rankings[name] = ordered
    leaders = {name: order[0] for name, order in rankings.items() if order}
    return {
        "rankings": rankings,
        "leaders": leaders,
        "same_leader_everywhere": len(set(leaders.values())) <= 1 if leaders else False,
        "vocabularies_compared": len(rankings),
    }
