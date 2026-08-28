"""The static fitness vector.

Nothing here is collapsed into a scalar. `FM-008` forbids optimising token count, and
`FM-007` forbids averaging error detection before selection, so the evaluator reports a
vector and the Pareto layer selects on it.

`FM-009` binds every distance metric: distances are in **characters and tokens**, never in
lines. The line-based version of this metric produced a persuasive 6.3x improvement that was
entirely an artifact of records-per-line density.
"""

from __future__ import annotations

from dataclasses import dataclass
import gzip
import math
import random
import re
from typing import Any

from hml_v3.representation_search.compiler import RepresentationCompiler
from hml_v3.representation_search.tokenizer import pretokens, tokenizer

#: Higher is better for these; every other metric is minimised.
MAXIMISED = frozenset({
    "detect_drop_line", "detect_swap_records", "detect_corrupt_identity",
    "detect_truncate_tail", "detect_drop_field", "detect_reorder_scope",
    "gzip_ratio", "structural_density",
})

#: The axes the Pareto front is computed over. Deliberately small: adding a weakly
#: informative axis to a Pareto computation makes almost everything non-dominated.
#: ``detect_corrupt_identity`` is deliberately absent. Measured across all sixteen
#: generation-zero seeds on the real V2 corpus it was 1.000 everywhere: every candidate
#: detects a corrupted identifier, because an altered identity either fails to resolve or
#: resolves to a different declaration. FM-010's rule applies — an instrument whose arms all
#: saturate is reported as non-discriminative rather than as agreement — so it is measured
#: and reported but does not participate in selection. ``detect_drop_field`` takes its place:
#: it spread 0.000-0.792 across the same seeds.
PARETO_AXES = (
    "bpe_tokens_per_transition",
    "binder_use_distance_tokens",
    "premise_to_action_distance_tokens",
    "detect_swap_records",
    "detect_drop_field",
    "identifier_fragmentation",
    "max_reference_span_tokens",
)


@dataclass
class MetricVector:
    candidate_id: str
    values: dict[str, float]
    sample_size: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "sample_size": self.sample_size,
            "values": {key: round(value, 6) for key, value in sorted(self.values.items())},
        }


IDENTIFIER_RE = re.compile(r"[^\W\d][\w.]*", re.UNICODE)


def token_positions(text: str, token: str) -> list[int]:
    """Character offsets where ``token`` occurs as a whole identifier.

    A naive substring search is wrong here and wrong in a way that inflates the locality
    numbers: with short identities, ``bf1`` also matches inside ``bf10`` through ``bf19``.
    Measured on one real transition that was an 80-against-64 overcount, 25% high. This is
    the same class of defect as FM-009, where a line-based distance unit produced a
    persuasive 6.3x improvement that did not exist.
    """

    pattern = re.compile(rf"(?<![A-Za-z0-9_]){re.escape(token)}(?![A-Za-z0-9_])")
    return [match.start() for match in pattern.finditer(text)]


# ------------------------------------------------------------------------------ utilities


def _token_positions(text: str) -> tuple[list[str], list[int]]:
    """BPE pieces and the character offset at which each piece starts."""

    encoder = tokenizer()
    pieces: list[str] = []
    offsets: list[int] = []
    cursor = 0
    for token in pretokens(text):
        start = text.index(token, cursor)
        cursor = start + len(token)
        merged = encoder.encode_pieces(token)
        share = len(token) / max(1, len(merged))
        for index, piece in enumerate(merged):
            pieces.append(piece)
            offsets.append(start + int(index * share))
    return pieces, offsets


def _char_to_token_index(offsets: list[int], position: int) -> int:
    low, high = 0, len(offsets)
    while low < high:
        middle = (low + high) // 2
        if offsets[middle] <= position:
            low = middle + 1
        else:
            high = middle
    return max(0, low - 1)


# --------------------------------------------------------------------------- locality


def _reference_distances(
    text: str, identities: list[str], offsets: list[int],
) -> tuple[float, float, float]:
    """Mean character and token distance between consecutive mentions of an identity.

    Returns ``(mean_chars, mean_tokens, max_tokens)``. An identity mentioned once
    contributes nothing, so a representation cannot be rewarded for hiding references.
    """

    char_gaps: list[int] = []
    token_gaps: list[int] = []
    for identity in identities:
        positions = token_positions(text, identity)
        if len(positions) < 2:
            continue
        for previous, current in zip(positions, positions[1:]):
            char_gaps.append(current - previous)
            token_gaps.append(
                _char_to_token_index(offsets, current) - _char_to_token_index(offsets, previous)
            )
    if not char_gaps:
        return 0.0, 0.0, 0.0
    return (
        sum(char_gaps) / len(char_gaps),
        sum(token_gaps) / len(token_gaps),
        float(max(token_gaps)),
    )


def _forward_reference_rate(text: str, identities: list[str]) -> float:
    """Fraction of identities used before the line that introduces them."""

    forward = 0
    counted = 0
    lines = text.splitlines()
    for identity in identities:
        introduced = None
        first_use = None
        for index, line in enumerate(lines):
            if not token_positions(line, identity):
                continue
            if first_use is None:
                first_use = index
            stripped = line.strip()
            if introduced is None and stripped.split(" ")[1:2] == [identity]:
                introduced = index
        if introduced is None or first_use is None:
            continue
        counted += 1
        if introduced > first_use:
            forward += 1
    return forward / counted if counted else 0.0


# ------------------------------------------------------------------------ error detection


def _mutate(text: str, family: str, rng: random.Random) -> str | None:
    lines = text.split("\n")
    if len(lines) < 4:
        return None
    if family == "drop_line":
        index = rng.randrange(len(lines))
        return "\n".join(lines[:index] + lines[index + 1:])
    if family == "swap_two_lines":
        first, second = rng.sample(range(len(lines)), 2)
        lines[first], lines[second] = lines[second], lines[first]
        return "\n".join(lines)
    if family == "truncate_tail":
        return "\n".join(lines[: max(1, len(lines) - 1 - rng.randrange(2))])
    if family == "corrupt_identity":
        candidates = [index for index, line in enumerate(lines) if IDENTIFIER_RE.search(line)]
        if not candidates:
            return None
        index = rng.choice(candidates)
        match = IDENTIFIER_RE.search(lines[index])
        assert match is not None
        token = match.group(0)
        lines[index] = lines[index].replace(token, token + "x", 1)
        return "\n".join(lines)
    if family == "drop_field":
        candidates = [index for index, line in enumerate(lines) if line.startswith("    ")]
        if not candidates:
            return None
        index = rng.choice(candidates)
        return "\n".join(lines[:index] + lines[index + 1:])
    if family == "reorder_scope":
        candidates = [
            index for index, line in enumerate(lines)
            if line.startswith("  ") and not line.startswith("    ")
        ]
        if len(candidates) < 2:
            return None
        first, second = rng.sample(candidates, 2)
        lines[first], lines[second] = lines[second], lines[first]
        return "\n".join(lines)
    return None


def _detection_rate(
    compiler: RepresentationCompiler, transitions: list[dict[str, Any]],
    family: str, seed: int,
) -> float:
    """Fraction of corruptions the reader refuses or decodes into a different object.

    Silent acceptance of an altered state is the failure that matters: a reader returning a
    plausible-but-wrong state is worse than one that raises.
    """

    rng = random.Random(seed)
    detected = 0
    attempted = 0
    for transition in transitions:
        rendered = compiler.render(transition)
        try:
            original = compiler.parse_core(rendered.text, rendered.codec)
        except Exception:  # noqa: BLE001
            continue
        mutated = _mutate(rendered.text, family, rng)
        if mutated is None or mutated == rendered.text:
            continue
        attempted += 1
        try:
            recovered = compiler.parse_core(mutated, rendered.codec)
        except Exception:  # noqa: BLE001 - a refusal is a detection
            detected += 1
            continue
        if recovered != original:
            detected += 1
    return detected / attempted if attempted else 0.0


# -------------------------------------------------------------------------- the evaluator


def measure(
    compiler: RepresentationCompiler, transitions: list[dict[str, Any]], seed: int = 20260828,
) -> MetricVector:
    values: dict[str, float] = {}
    encoder = tokenizer()

    total_bytes = total_chars = total_bpe = total_pre = gzip_bytes = 0
    binder_chars: list[float] = []
    binder_tokens: list[float] = []
    max_spans: list[float] = []
    premise_distances: list[float] = []
    forward_rates: list[float] = []
    identifier_pieces: list[float] = []
    structural_lines: list[float] = []

    action_word = compiler.surface.lexicon.word("action")
    for transition in transitions:
        rendered = compiler.render(transition)
        text = rendered.text
        total_bytes += len(text.encode("utf-8"))
        total_chars += len(text)
        total_bpe += encoder.count(text)
        total_pre += len(pretokens(text))
        gzip_bytes += len(gzip.compress(text.encode("utf-8"), 9, mtime=0))

        _, offsets = _token_positions(text)
        identities = sorted({
            declaration["identity"]
            for goal in transition["state_before"]["goals"]
            for declaration in goal["local_context"]
        })
        encoded = [rendered.codec.encode(item) for item in identities]
        chars, tokens, span = _reference_distances(text, encoded, offsets)
        if chars:
            binder_chars.append(chars)
            binder_tokens.append(tokens)
            max_spans.append(span)
        forward_rates.append(_forward_reference_rate(text, encoded))

        premises = list(transition["action"]["external_premise_refs"])
        action_position = text.find(action_word)
        if premises and action_position >= 0:
            gaps = []
            for premise in premises:
                found = token_positions(text, premise)
                position = found[0] if found else -1
                if position >= 0:
                    gaps.append(abs(
                        _char_to_token_index(offsets, position)
                        - _char_to_token_index(offsets, action_position)
                    ))
            if gaps:
                premise_distances.append(sum(gaps) / len(gaps))

        found = IDENTIFIER_RE.findall(text)
        if found:
            identifier_pieces.append(
                sum(len(encoder.encode_pieces(name)) for name in found) / len(found)
            )
        structural_lines.append(len(text.splitlines()))

    count = max(1, len(transitions))
    role_words = [
        compiler.surface.lexicon.word(key)
        for key in ("goal", "decl", "target", "context", "action", "delta")
    ]

    values["bytes_per_transition"] = total_bytes / count
    values["chars_per_transition"] = total_chars / count
    values["bpe_tokens_per_transition"] = total_bpe / count
    values["pretokens_per_transition"] = total_pre / count
    values["gzip_bytes_per_transition"] = gzip_bytes / count
    values["gzip_ratio"] = total_bytes / max(1, gzip_bytes)
    values["binder_use_distance_chars"] = _mean(binder_chars)
    values["binder_use_distance_tokens"] = _mean(binder_tokens)
    values["max_reference_span_tokens"] = _mean(max_spans)
    values["forward_reference_rate"] = _mean(forward_rates)
    values["premise_to_action_distance_tokens"] = _mean(premise_distances)
    values["identifier_fragmentation"] = _mean(identifier_pieces)
    values["role_word_fragmentation"] = _mean(
        [float(len(encoder.encode_pieces(word))) for word in role_words]
    )
    values["structural_density"] = (
        _mean(structural_lines) / max(1.0, values["bpe_tokens_per_transition"]) * 100
    )

    detection_sample = transitions[: min(24, len(transitions))]
    for family, key, offset in (
        ("drop_line", "detect_drop_line", 0),
        ("swap_two_lines", "detect_swap_records", 1),
        ("corrupt_identity", "detect_corrupt_identity", 2),
        ("truncate_tail", "detect_truncate_tail", 3),
        ("drop_field", "detect_drop_field", 4),
        ("reorder_scope", "detect_reorder_scope", 5),
    ):
        values[key] = _detection_rate(compiler, detection_sample, family, seed + offset)
    values["role_vocabulary_entropy"] = _role_entropy(compiler, transitions[: min(16, count)])
    return MetricVector(compiler.candidate_id, values, len(transitions))


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def _role_entropy(compiler: RepresentationCompiler, transitions: list[dict[str, Any]]) -> float:
    """Shannon entropy of the role-word distribution, in bits.

    A proxy for how much of the surface is scaffolding. It is a proxy: it says nothing about
    any model's conditional distribution and is never presented as if it did.
    """

    counts: dict[str, int] = {}
    words = set(compiler.surface.lexicon.backward)
    for transition in transitions:
        for token in pretokens(compiler.render_text(transition)):
            stripped = token.strip()
            if stripped in words:
                counts[stripped] = counts.get(stripped, 0) + 1
    total = sum(counts.values())
    if total == 0:
        return 0.0
    return -sum((count / total) * math.log2(count / total) for count in counts.values())
