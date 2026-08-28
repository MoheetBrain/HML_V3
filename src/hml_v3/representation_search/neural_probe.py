"""Inference-only neural microprobes with a preregistered sequential stopping rule.

Static metrics cannot tell you whether a representation is *readable*. A candidate can be
cheap, local and perfectly recoverable and still be harder for a model to parse than a more
expensive one. These probes are the cheapest possible evidence about that, and they are
deliberately small.

This is not training. No weights are updated, no adapter is fitted, no GPU job is submitted.
A frozen model is asked multiple-choice questions whose ground truth comes from the canonical
state, and the arms differ only in how that state is written.

Two disciplines make the result worth anything:

*Matched counterfactuals.* Every question's distractors are built from the same state, so the
symbols, lengths and operators are near-identical across options and only the structural
relation differs. A model that answers by surface statistics scores at chance.

*A stopping rule fixed in advance.* `SequentialRule` is written down before any arm is run,
and the decision to stop is a function of the evidence, never of who is winning. Without
that, running "until it looks clear" manufactures significance.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
import random
import re
import subprocess
from typing import Any, Callable, Sequence

from hml_v3.representation_search.compiler import RepresentationCompiler

CHOICE_LABELS = ("A", "B", "C", "D")


@dataclass
class ProbeItem:
    """One matched multiple-choice question."""

    question: str
    options: list[str]
    correct_index: int
    mechanism: str
    transition_id: str

    def prompt(self, rendering: str) -> str:
        choices = "\n".join(
            f"{CHOICE_LABELS[index]}. {option}"
            for index, option in enumerate(self.options)
        )
        return (
            "Below is one step of a formal mathematical proof, written in a machine-facing "
            "notation.\n\n"
            f"{rendering}\n\n"
            f"Question: {self.question}\n{choices}\n\n"
            "Answer with a single letter and nothing else."
        )


@dataclass
class ArmResult:
    candidate_id: str
    correct: int = 0
    answered: int = 0
    items: int = 0
    responses: list[str] = field(default_factory=list)

    @property
    def accuracy(self) -> float:
        return self.correct / self.answered if self.answered else 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "items": self.items,
            "answered": self.answered,
            "correct": self.correct,
            "accuracy": round(self.accuracy, 4),
        }


# ------------------------------------------------------------------------- item builders


def _local_references(node: Any, found: list[str]) -> None:
    if isinstance(node, dict):
        if node.get("node") == "local_reference":
            found.append(node["identity"])
        for value in node.values():
            if isinstance(value, (dict, list)):
                _local_references(value, found)
    elif isinstance(node, list):
        for item in node:
            _local_references(item, found)


def binder_items(transition: dict[str, Any], rng: random.Random) -> list[ProbeItem]:
    """Which declaration does the goal's target actually use?

    The distractors are other declarations from the same state, so every option is a real
    identifier of the same shape appearing in the same rendering. Length, vocabulary and
    formatting carry no signal; only the binding edge does.
    """

    items: list[ProbeItem] = []
    for goal in transition["state_before"]["goals"]:
        used: list[str] = []
        _local_references(goal["target"], used)
        declared = [d["identity"] for d in goal["local_context"]]
        cited = [identity for identity in dict.fromkeys(used) if identity in declared]
        distractors = [identity for identity in declared if identity not in set(cited)]
        if not cited or len(distractors) < 3:
            continue
        correct = rng.choice(cited)
        options = [correct, *rng.sample(distractors, 3)]
        rng.shuffle(options)
        items.append(ProbeItem(
            question="Which local declaration is used in the goal's target?",
            options=options, correct_index=options.index(correct),
            mechanism="binder", transition_id=transition["transition_id"],
        ))
    return items


def premise_items(transition: dict[str, Any], rng: random.Random) -> list[ProbeItem]:
    """Which premise does this step cite? Distractors are constants from the same state."""

    premises = list(transition["action"]["external_premise_refs"])
    if not premises:
        return []
    symbols: list[str] = []

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            if node.get("node") == "symbol":
                symbols.append(node["identity"])
            for value in node.values():
                if isinstance(value, (dict, list)):
                    walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(transition["state_before"]["goals"])
    distractors = [s for s in dict.fromkeys(symbols) if s not in set(premises)]
    if len(distractors) < 3:
        return []
    correct = rng.choice(premises)
    options = [correct, *rng.sample(distractors, 3)]
    rng.shuffle(options)
    return [ProbeItem(
        question="Which external premise does the proof step cite?",
        options=options, correct_index=options.index(correct),
        mechanism="premise", transition_id=transition["transition_id"],
    )]


BUILDERS: dict[str, Callable[[dict[str, Any], random.Random], list[ProbeItem]]] = {
    "binder": binder_items,
    "premise": premise_items,
}


def build_items(
    transitions: Sequence[dict[str, Any]], mechanisms: Sequence[str], seed: int,
    limit: int = 160,
) -> list[ProbeItem]:
    rng = random.Random(seed)
    items: list[ProbeItem] = []
    for transition in transitions:
        for mechanism in mechanisms:
            items.extend(BUILDERS[mechanism](transition, rng))
            if len(items) >= limit:
                return items[:limit]
    return items[:limit]


# --------------------------------------------------------------------------- dumb controls


TOKEN = re.compile(r"[^\W\d_]+", re.UNICODE)


def dumb_control_accuracy(items: list[ProbeItem]) -> dict[str, float]:
    """Can cheap heuristics solve these questions without reading the structure?

    `FM-003` recorded that bag-of-words reached 0.72-0.76 macro-F1 on a task where the
    transformer reached 0.77-0.79. If a control does well here, the benchmark is measuring
    surface statistics and must not be run against a model at all.
    """

    if not items:
        return {}
    chance = 1.0 / len(CHOICE_LABELS)
    longest = sum(
        1 for item in items
        if item.options.index(max(item.options, key=len)) == item.correct_index
    ) / len(items)
    shortest = sum(
        1 for item in items
        if item.options.index(min(item.options, key=len)) == item.correct_index
    ) / len(items)
    first = sum(1 for item in items if item.correct_index == 0) / len(items)
    alphabetical = sum(
        1 for item in items
        if item.options.index(sorted(item.options)[0]) == item.correct_index
    ) / len(items)
    return {
        "class_prior": round(chance, 4),
        "longest_option": round(longest, 4),
        "shortest_option": round(shortest, 4),
        "first_option": round(first, 4),
        "alphabetical_first": round(alphabetical, 4),
    }


def controls_pass(items: list[ProbeItem], margin: float = 0.15) -> tuple[bool, dict[str, float]]:
    """The benchmark is usable only when no dumb control beats chance by ``margin``."""

    controls = dumb_control_accuracy(items)
    if not controls:
        return False, {}
    chance = controls["class_prior"]
    worst = max(
        value for key, value in controls.items() if key != "class_prior"
    )
    return worst <= chance + margin, controls


# ------------------------------------------------------------------ the sequential rule


@dataclass
class SequentialRule:
    """Preregistered. Written before any arm is evaluated and not changed afterwards.

    Paired evaluation with a normal approximation to the paired-difference test. A candidate
    is eliminated when the evidence that it is worse than the reference is strong enough at
    the current sample size, and the sample sizes at which that is checked are fixed here.
    """

    checkpoints: tuple[int, ...] = (20, 40, 80, 160)
    elimination_z: float = 1.64      # one-sided, ~5%
    superiority_z: float = 1.96      # two-sided, ~5%
    minimum_effect: float = 0.05

    def to_dict(self) -> dict[str, Any]:
        return {
            "checkpoints": list(self.checkpoints),
            "elimination_z": self.elimination_z,
            "superiority_z": self.superiority_z,
            "minimum_effect": self.minimum_effect,
            "method": "paired difference, normal approximation, fixed checkpoints",
            "preregistered": True,
            "rule": (
                "at each checkpoint compute the paired difference between the candidate and "
                "the reference; eliminate when the candidate is worse by more than "
                "elimination_z standard errors; declare superiority only at "
                "superiority_z with an effect of at least minimum_effect; otherwise "
                "continue to the next checkpoint and stop at the last one"
            ),
        }

    def decide(self, candidate: list[bool], reference: list[bool]) -> dict[str, Any]:
        paired = [
            (1 if a else 0) - (1 if b else 0)
            for a, b in zip(candidate, reference)
        ]
        n = len(paired)
        if n == 0:
            return {"verdict": "NO_DATA", "n": 0}
        mean = sum(paired) / n
        variance = sum((value - mean) ** 2 for value in paired) / max(1, n - 1)
        standard_error = (variance / n) ** 0.5 if n > 1 and variance > 0 else 0.0
        z = mean / standard_error if standard_error > 0 else 0.0
        verdict = "CONTINUE"
        if standard_error == 0.0 and mean == 0.0:
            verdict = "INDISTINGUISHABLE"
        elif z <= -self.elimination_z:
            verdict = "ELIMINATED"
        elif z >= self.superiority_z and mean >= self.minimum_effect:
            verdict = "SUPERIOR"
        if n >= self.checkpoints[-1] and verdict == "CONTINUE":
            verdict = "INCONCLUSIVE_AT_BUDGET"
        return {
            "verdict": verdict, "n": n, "mean_difference": round(mean, 4),
            "z": round(z, 3), "standard_error": round(standard_error, 5),
        }


# --------------------------------------------------------------------------- the runner


class OllamaProbe:
    """A frozen local model answering multiple choice. Inference only."""

    def __init__(self, model: str = "gemma3:4b", timeout: int = 120) -> None:
        self.model = model
        self.timeout = timeout
        self.name = f"ollama:{model}"

    def available(self) -> bool:
        try:
            listed = subprocess.run(
                ["ollama", "list"], capture_output=True, text=True, timeout=30, check=False)
        except (OSError, subprocess.SubprocessError):
            return False
        return listed.returncode == 0 and self.model.split(":")[0] in listed.stdout

    def answer(self, prompt: str) -> str | None:
        payload = {
            "model": self.model, "prompt": prompt, "stream": False,
            # Greedy: the same prompt must give the same answer, or arms are not comparable.
            "options": {"temperature": 0.0, "num_predict": 4, "num_ctx": 8192},
        }
        try:
            process = subprocess.run(
                ["curl", "-sS", "-m", str(self.timeout),
                 "http://127.0.0.1:11434/api/generate",
                 "-H", "Content-Type: application/json", "-d", json.dumps(payload)],
                capture_output=True, text=True, timeout=self.timeout + 20, check=False,
            )
            if process.returncode != 0:
                return None
            text = json.loads(process.stdout).get("response", "")
        except Exception:  # noqa: BLE001
            return None
        match = re.search(r"\b([ABCD])\b", text.strip().upper())
        return match.group(1) if match else None


def run_arm(
    compiler: RepresentationCompiler, items: list[ProbeItem],
    transitions_by_id: dict[str, dict[str, Any]], probe: OllamaProbe,
) -> tuple[ArmResult, list[bool]]:
    result = ArmResult(candidate_id=compiler.candidate_id, items=len(items))
    outcomes: list[bool] = []
    for item in items:
        transition = transitions_by_id.get(item.transition_id)
        if transition is None:
            outcomes.append(False)
            continue
        rendering = compiler.render_text(transition)
        answer = probe.answer(item.prompt(rendering))
        if answer is None:
            outcomes.append(False)
            continue
        result.answered += 1
        correct = CHOICE_LABELS.index(answer) == item.correct_index
        result.correct += int(correct)
        result.responses.append(answer)
        outcomes.append(correct)
    return result, outcomes
