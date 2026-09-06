"""N-choice probing of V2 items, with the four calibration arms.

V1 probed a 2-alternative forced choice over a transposition pair. V2 items carry up to four
plausible options and a state-level ablation, so the arms are built differently:

    EXPLICIT_POSITIVE  the relation is stated outright, beside the question
    ABLATED_NEGATIVE   the relation is destroyed in the state itself
    <control>          the strongest general control representation
    <candidate>        the representation under test

`MISSION §18`: the reader is an adversary, not an oracle. It is asked to solve the negative
arm as hard as it is asked to solve the candidate, and success there is a fact about the
benchmark rather than about any representation.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import subprocess
from typing import Any, Sequence

SYSTEM = """\
You read a machine-oriented representation of a formal proof state and answer one structural
question about it. The representation may be unfamiliar; everything you need is in the text.
Identifiers are opaque tags with no meaning beyond the structure that relates them.

Answer with EXACTLY ONE of the options given, copied verbatim. No explanation, no
punctuation, no other words."""

#: Models that reason into a separate channel and return EMPTY content unless the think block
#: is closed for them. `FM-032` established this for Qwen; `FM-056` found that `gemma4` does
#: the same and was NOT covered, so every Gemma-4 probe returned "" and scored as wrong. The
#: visible symptom is a reader scoring 0.000 on the arm that STATES the answer, which reads as
#: "this reader cannot do the task" when it is really "this harness cannot hear it".
#: The marker is "gemma4", not "gemma", so `gemma3:4b` -- not a thinking model -- is untouched.
THINKING_MARKERS = ("qwen", "deepseek-r1", "qwq", "gemma4")
EMPTY_THINK_PREFILL = "<think>\n\n</think>\n\n"

EXPLICIT_POSITIVE = "EXPLICIT_POSITIVE"
ABLATED_NEGATIVE = "ABLATED_NEGATIVE"


@dataclass
class Probe:
    item_id: str
    stress: str
    domain: str
    arm: str
    rendering: str
    question: str
    options: tuple[str, ...]
    answer: str
    #: For the positive arm: the relation stated outright, placed ADJACENT to the question.
    stated: str | None = None


@dataclass
class Outcome:
    probe: Probe
    predicted: str | None
    correct: bool
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {"item_id": self.probe.item_id, "stress": self.probe.stress,
                "domain": self.probe.domain, "arm": self.probe.arm,
                "predicted": self.predicted, "answer": self.probe.answer,
                "correct": self.correct, "error": self.error}


def _encode_options(rendered, options: Sequence[str]) -> list[str] | None:
    """Rewrite options the way this representation's identity codec writes them.

    `FM-039`: offering a model the raw canonical id when the page shows a codec-encoded one
    asks it to choose between strings that are not in the text, which measures nothing.
    """

    encoded = []
    for option in options:
        try:
            value = rendered.codec.encode(option)
        except Exception:  # noqa: BLE001
            value = option
        encoded.append(value if isinstance(value, str) and value else option)
    return encoded if len(set(encoded)) == len(options) else None


def build_probes(compiler, items, arm_label: str, *, use_ablated: bool = False,
                 positive_header: str | None = None) -> list[Probe]:
    """One probe per item. Items whose options collide under the codec are dropped."""

    probes: list[Probe] = []
    for item in items:
        state = item.ablated if use_ablated else item.state
        try:
            rendered = compiler.render(state)
        except Exception:  # noqa: BLE001
            continue
        encoded = _encode_options(rendered, item.options)
        if encoded is None:
            continue
        answer = encoded[list(item.options).index(item.answer)]
        stated = None
        if positive_header is not None:
            # `MISSION §25`: the positive arm must be nearly trivial. Putting the stated fact
            # at the TOP of the document did not achieve that -- it sat seven thousand
            # characters from the question and the reader ignored it, answering bv11 when the
            # header read "DEEPEST_REFERENCE = bv91". The arm scored 0.417 against a chance of
            # 0.304 while literally being told the answer, which measures whether a reader
            # trusts a distant header, not what it can do when readability is not the
            # obstacle. The fact is now placed immediately beside the question.
            stated = f"{positive_header} = {answer}"
        probes.append(Probe(
            item_id=item.item_id, stress=item.stress, domain=item.domain, arm=arm_label,
            rendering=rendered.text, question=item.question, options=tuple(encoded),
            answer=answer, stated=stated))
    return probes


def ask(model: str, probe: Probe, timeout: int = 180) -> Outcome:
    listed = "\n".join(f"- {option}" for option in probe.options)
    stated = (f"\n\nSTATED FACT (authoritative, use it): {probe.stated}"
              if probe.stated else "")
    user = (f"{probe.rendering}\n\nQUESTION: {probe.question}{stated}\n\n"
            f"OPTIONS:\n{listed}\n\nAnswer with exactly one option, copied verbatim.")
    messages = [{"role": "system", "content": SYSTEM},
                {"role": "user", "content": user}]
    if any(marker in model.lower() for marker in THINKING_MARKERS):
        # FM-032: without an empty-think prefill these models spend the whole budget inside
        # <think> and return an empty completion.
        messages.append({"role": "assistant", "content": EMPTY_THINK_PREFILL})
    payload = {"model": model, "messages": messages, "stream": False,
               "options": {"temperature": 0.0, "num_predict": 24}}
    try:
        result = subprocess.run(
            ["curl", "-s", "--max-time", str(timeout),
             "http://localhost:11434/api/chat", "-d", json.dumps(payload)],
            capture_output=True, text=True, check=True, timeout=timeout + 20)
        raw = json.loads(result.stdout)["message"]["content"]
    except Exception as error:  # noqa: BLE001
        return Outcome(probe, None, False, f"{type(error).__name__}: {error}"[:160])
    predicted = parse_choice(raw, probe.options)
    return Outcome(probe, predicted, predicted == probe.answer)


def parse_choice(raw: str, options: Sequence[str]) -> str | None:
    """Recover the chosen option. Exact match first, then a unique containment."""

    text = (raw or "").strip()
    if text.startswith(EMPTY_THINK_PREFILL.strip()[:7]):
        text = text.split("</think>")[-1].strip()
    stripped = text.strip().strip(".,;:!?\"'`*").strip()
    for option in options:
        if stripped == option:
            return option
    hits = [option for option in options if option in text]
    return hits[0] if len(hits) == 1 else None


def run(model: str, probes: Sequence[Probe]) -> tuple[int, int, list[Outcome]]:
    outcomes = [ask(model, probe) for probe in probes]
    successes = sum(1 for outcome in outcomes if outcome.correct)
    return successes, len(outcomes), outcomes
