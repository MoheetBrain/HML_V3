"""Level C: frozen local models as READERS of a representation.

`MICROMATH §12` and `§36`: zero-cost local inference only -- no paid API, no GPU job, no
training, no adaptation. The models are not judges of mathematical truth; Lean is. They are
instruments for one question: given this rendering, can a reader recover the relation?

Each item is a 2-alternative forced choice over a matched pair, so chance is exactly 0.5 and
the two options are the same strings in both arms. `§13`: when more than one model is
available each is recorded separately, because an improvement that holds for one
architecture only is still evidence, but it is MODEL_SPECIFIC evidence.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
import subprocess
from typing import Any

SYSTEM = """\
You read a machine-oriented representation of a formal proof state and answer one structural
question about it. The representation may be unfamiliar; everything you need is in the text.

Answer with EXACTLY ONE of the two options given, copied verbatim. No explanation, no
punctuation, no other words."""

THINKING_MARKERS = ("qwen", "deepseek-r1", "qwq")
EMPTY_THINK_PREFILL = "<think>\n\n</think>\n\n"


@dataclass
class ProbeItem:
    pair_id: str
    domain: str
    stress: str
    arm: str              # "A" or "B"
    rendering: str
    question: str
    options: tuple[str, str]
    answer: str


@dataclass
class ProbeResult:
    item: ProbeItem
    raw: str
    predicted: str | None
    correct: bool
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "pair_id": self.item.pair_id, "domain": self.item.domain,
            "stress": self.item.stress, "arm": self.item.arm,
            "predicted": self.predicted, "answer": self.item.answer,
            "correct": self.correct, "error": self.error,
        }


def build_items(compiler, pairs) -> list[ProbeItem]:
    """One item per arm, with the options written the way the rendering writes them.

    Identities reach the page through the candidate's identity codec: a canonical ``m3`` may
    appear as ``bm3``, and a declaration may appear under a display name. Offering the model
    the raw canonical ids would ask it to choose between strings that are not in the text,
    which measures nothing about the representation. The options are therefore encoded per
    candidate, and an item whose options do not survive encoding is dropped rather than
    scored.
    """

    items: list[ProbeItem] = []
    for pair in pairs:
        for arm, state, answer in (("A", pair.state_a, pair.answer_a),
                                   ("B", pair.state_b, pair.answer_b)):
            try:
                rendered = compiler.render(state)
            except Exception:  # noqa: BLE001
                continue
            encoded = []
            for option in pair.options:
                value = rendered.codec.encode(option)
                encoded.append(value if isinstance(value, str) else option)
            if len(set(encoded)) != 2:
                continue
            answer_encoded = encoded[list(pair.options).index(answer)]
            items.append(ProbeItem(
                pair_id=pair.pair_id, domain=pair.domain, stress=pair.stress, arm=arm,
                rendering=rendered.text, question=pair.question,
                options=(encoded[0], encoded[1]), answer=answer_encoded))
    return items


def prompt_for(item: ProbeItem) -> str:
    left, right = item.options
    return (
        f"REPRESENTATION:\n{item.rendering}\n\n"
        f"QUESTION: {item.question}\n\n"
        f"OPTIONS (answer with exactly one):\n- {left}\n- {right}\n\nANSWER:"
    )


def parse_choice(text: str, options: tuple[str, str]) -> str | None:
    """Whichever option the model actually committed to, or None.

    A response mentioning both options has not chosen; scoring it by first mention would
    reward verbosity. Only a response that names exactly one counts.
    """

    if not text:
        return None
    cleaned = text.strip().strip("`\"' \n.")
    left, right = options
    if cleaned == left:
        return left
    if cleaned == right:
        return right
    has_left, has_right = left in text, right in text
    if has_left and not has_right:
        return left
    if has_right and not has_left:
        return right
    return None


class LocalModel:
    """A locally served frozen model reached through ollama's chat endpoint."""

    def __init__(self, name: str, num_ctx: int = 16384, timeout: int = 300) -> None:
        self.name = name
        self.num_ctx = num_ctx
        self.timeout = timeout
        self.suppress_thinking = any(m in name.lower() for m in THINKING_MARKERS)

    def available(self) -> bool:
        try:
            listed = subprocess.run(["ollama", "list"], capture_output=True, text=True,
                                    timeout=30, check=False)
        except (OSError, subprocess.SubprocessError):
            return False
        return listed.returncode == 0 and self.name.split(":")[0] in listed.stdout

    def ask(self, prompt: str) -> str:
        messages = [{"role": "system", "content": SYSTEM},
                    {"role": "user", "content": prompt}]
        if self.suppress_thinking:
            messages.append({"role": "assistant", "content": EMPTY_THINK_PREFILL})
        payload = {
            "model": self.name, "messages": messages, "stream": False,
            "options": {"temperature": 0.0, "num_ctx": self.num_ctx, "num_predict": 24},
        }
        process = subprocess.run(
            ["curl", "-sS", "-m", str(self.timeout), "http://127.0.0.1:11434/api/chat",
             "-H", "Content-Type: application/json", "-d", json.dumps(payload)],
            capture_output=True, text=True, timeout=self.timeout + 30, check=False)
        if process.returncode != 0:
            raise RuntimeError(f"transport failed: {process.stderr[:200]}")
        body = json.loads(process.stdout)
        if body.get("error"):
            raise RuntimeError(f"model error: {str(body['error'])[:200]}")
        return (body.get("message") or {}).get("content", "")


def run_probe(model: LocalModel, items: list[ProbeItem]) -> list[ProbeResult]:
    results: list[ProbeResult] = []
    for item in items:
        try:
            raw = model.ask(prompt_for(item))
            predicted = parse_choice(raw, item.options)
            results.append(ProbeResult(item, raw[:200], predicted,
                                       predicted == item.answer))
        except Exception as error:  # noqa: BLE001 - a failed item is recorded, not fatal
            results.append(ProbeResult(item, "", None, False, str(error)[:160]))
    return results


def per_pair_accuracy(results: list[ProbeResult]) -> dict[str, float]:
    """Accuracy per matched pair: 0.0, 0.5 or 1.0 over its two arms.

    The pair is the unit because its two arms share a base state; treating them as
    independent items would understate the uncertainty.
    """

    buckets: dict[str, list[bool]] = {}
    for result in results:
        buckets.setdefault(result.item.pair_id, []).append(result.correct)
    return {pair_id: sum(values) / len(values) for pair_id, values in buckets.items()}


def cell_accuracy(results: list[ProbeResult]) -> dict[tuple[str, str], float]:
    buckets: dict[tuple[str, str], list[bool]] = {}
    for result in results:
        buckets.setdefault((result.item.domain, result.item.stress), []).append(result.correct)
    return {cell: sum(v) / len(v) for cell, v in buckets.items()}
