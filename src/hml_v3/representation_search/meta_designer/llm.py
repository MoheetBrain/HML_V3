"""The model-driven meta-designer.

This is the backend that removes the ceiling. A rule-based proposer can only recombine axes
that already exist; a model reading the measured failure profile can propose an axis the
genome does not have, ask for data the corpus lacks, or say that an instrument is measuring
the wrong thing.

Safety comes from the channel, not from trust in the model. The model receives a compact
aggregate report — never a corpus row, never a sealed transition, never source code — and
returns JSON. That JSON is schema-validated, statically safety-checked, and only then does it
become a candidate. Free-form model text never reaches a file, a genome, or the compiler.

Transport is deliberately pluggable. ``OllamaTransport`` runs a local frozen model with no
training and no network egress; ``CallableTransport`` accepts any function for tests or for a
hosted model. Absence of a backend is not an error: the loop falls back and records that it
ran without a model-driven proposer.
"""

from __future__ import annotations

import abc
import json
import re
import subprocess
from typing import Any, Callable

from hml_v3.representation_search.meta_designer.base import (
    MetaDesignerBackend,
    ProposalBatch,
    ScientistReport,
)

SYSTEM_BRIEF = """\
You are the meta-designer in an automated representation-discovery loop for machine-facing
mathematics. Mathematical truth is FIXED: a CanonicalMathState derived from verified Lean 4
proof transitions. You may only change how that state is WRITTEN, never what it contains.

You are given aggregate measurements from the current search. Propose experiments.

You may return these proposal types:
  AXIS_MUTATION            change one existing genome axis on one parent candidate
  ARCHITECTURAL_HYPOTHESIS change several axes together as one coherent intervention
  NEW_AXIS                 add a NEW dimension the genome does not have
  NEW_PRIMITIVE            add a new representation mechanism (with projection behaviour)
  CORPUS_ACQUISITION       say the corpus cannot answer a question, and what to acquire
  NEW_MICROTEST            say the instruments cannot answer a question
  INSTRUMENT_FIX           say an instrument is measuring the wrong thing
  ELIMINATE_CANDIDATE      retire a candidate and say why

The most valuable proposals are the ones the rule-based proposer CANNOT make: NEW_AXIS,
NEW_PRIMITIVE, CORPUS_ACQUISITION, NEW_MICROTEST, INSTRUMENT_FIX.

For NEW_AXIS and NEW_PRIMITIVE you must say HOW the projection changes, using one of the
mechanisms the compiler can actually execute. Set "projection_hook" to exactly one of:

  "neighbourhood_capsule"  move the declarations a goal cites so they sit adjacent to that
                           goal. Global context unchanged; every declaration still appears
                           once. Use for binder/dependency distance problems.
  "duplicate_adjacent"     restate one field of a record next to the record that consumes
                           it. Costs tokens, buys locality and corruption detection.
  "section_partition"      emit one record kind (e.g. metavariables) in its own block,
                           before or after the rest of the state.
  "record_reorder"         reorder records of one kind by a declared key.

A NEW_AXIS whose behaviour is not one of these is recorded but cannot be run, so prefer one
of these unless the idea genuinely needs something else.

Hard rules:
- Never propose changing the canonical state, the verifier, or the sealed split.
- implementation_layer must be one of: representation_only, projection_only, surface_only.
- Every proposal needs a real "hypothesis", a real "mechanism", and a "falsification"
  condition stating what result would make you abandon it.
- Axis names are lower_snake_case. Axis values are UPPER_SNAKE_CASE, at least two of them.
- Do not repeat an intervention the failure memory records as already falsified under the
  same conditions.

Return ONLY a JSON array of proposal objects. No prose, no markdown fence, no commentary.

Use EXACTLY these field names. Two worked examples:

[
 {"proposal_type": "AXIS_MUTATION",
  "parent_id": "R_abc123456789",
  "axis": "premise_locality",
  "value": "HEADER_BLOCK",
  "target_metric": "premise_to_action_distance_tokens",
  "hypothesis": "stating premises once in a header puts them a fixed distance from the action instead of a distance that grows with context size",
  "mechanism": "the action record and the premise list become adjacent, so the reader never scans the local context to find a cited premise",
  "falsification": "reject if premise_to_action_distance_tokens does not fall by at least 10% against the parent"},

 {"proposal_type": "NEW_AXIS",
  "name": "dependency_capsule",
  "values": ["NONE", "GOAL_LOCAL", "ACTION_LOCAL"],
  "implementation_layer": "projection_only",
  "hypothesis": "emitting the minimal dependency neighbourhood of the focused goal next to that goal shortens binder-use distance without hiding the global context",
  "mechanism": "declarations the goal target actually cites are laid out adjacent to it, so the span between a binder and its use stops scaling with total context size",
  "falsification": "reject if binder_use_distance_tokens improves by less than 10%, or if semantic round-trip fails",
  "projection_hook": "neighbourhood_capsule",
  "tests_required": ["semantic_roundtrip", "binder_query_suite"],
  "predicted_costs": {"tokens": "+8%"}}
]
"""

JSON_ARRAY = re.compile(r"\[\s*\{.*}\s*]", re.DOTALL)

#: Field spellings small models reliably produce instead of the schema's names. Normalising
#: them is not a weakening of the schema: the content requirements are unchanged, and every
#: rename is recorded on the proposal so the report can show how much cleanup a backend needed.
FIELD_SYNONYMS = {
    "axis_name": "axis",
    "axis_value": "value",
    "new_value": "value",
    "primitive_name": "name",
    "axis_values": "values",
    "candidate_values": "values",
    "layer": "implementation_layer",
    "parent": "parent_id",
    "parent_candidate": "parent_id",
    "candidate": "candidate_id",
    "target": "stratum",
    "rationale": "hypothesis",
    "why": "hypothesis",
    "predicted_improvements": "predicted_improvement",
    "tests": "tests_required",
    "required_tests": "tests_required",
    "metric": "target_metric",
}


def normalise(payload: Any, default_parent: str | None) -> Any:
    """Rename known synonym fields and supply an obvious default parent.

    A model that proposes ``axis_name``/``axis_value`` has made a spelling mistake, not a
    scientific one. A model that proposes an axis mutation without naming a parent was
    clearly proposing against the elite it was shown. Both are repaired here and recorded;
    everything substantive still has to pass validation.
    """

    if not isinstance(payload, dict):
        return payload
    out: dict[str, Any] = {}
    renamed: list[str] = []
    for key, value in payload.items():
        target = FIELD_SYNONYMS.get(key, key)
        if target != key and target not in payload:
            renamed.append(f"{key}->{target}")
            out[target] = value
        else:
            out.setdefault(key, value)
    kind = out.get("proposal_type")
    if kind in ("AXIS_MUTATION", "ARCHITECTURAL_HYPOTHESIS") and not out.get("parent_id"):
        if default_parent:
            out["parent_id"] = default_parent
            renamed.append("parent_id<-first_elite")
    if kind == "NEW_PRIMITIVE" and not out.get("projection_behaviour"):
        mechanism = out.get("mechanism")
        if isinstance(mechanism, str) and len(mechanism) >= 40:
            out["projection_behaviour"] = mechanism
            renamed.append("projection_behaviour<-mechanism")
    if renamed:
        out["_normalised"] = renamed
    return out


class Transport(abc.ABC):
    """How a prompt reaches a model. Kept narrow so backends are swappable."""

    name: str = "abstract"

    @abc.abstractmethod
    def complete(self, system: str, user: str) -> str:
        ...

    def available(self) -> bool:
        return True


class OllamaTransport(Transport):
    """A locally served frozen model. Inference only: no training, no adaptation, no GPU job."""

    def __init__(self, model: str = "gemma3:4b", timeout: int = 240,
                 num_ctx: int = 16384) -> None:
        self.model = model
        self.timeout = timeout
        self.num_ctx = num_ctx
        self.name = f"ollama:{model}"

    def available(self) -> bool:
        try:
            listed = subprocess.run(
                ["ollama", "list"], capture_output=True, text=True, timeout=30, check=False)
        except (OSError, subprocess.SubprocessError):
            return False
        return listed.returncode == 0 and self.model.split(":")[0] in listed.stdout

    def complete(self, system: str, user: str) -> str:
        payload = {
            "model": self.model,
            "prompt": f"{system}\n\n{user}",
            "stream": False,
            "options": {"temperature": 0.8, "num_ctx": self.num_ctx, "num_predict": 2048},
        }
        process = subprocess.run(
            ["curl", "-sS", "-m", str(self.timeout),
             "http://127.0.0.1:11434/api/generate",
             "-H", "Content-Type: application/json",
             "-d", json.dumps(payload)],
            capture_output=True, text=True, timeout=self.timeout + 30, check=False,
        )
        if process.returncode != 0:
            raise RuntimeError(f"ollama transport failed: {process.stderr[:300]}")
        try:
            return json.loads(process.stdout)["response"]
        except (json.JSONDecodeError, KeyError) as error:
            raise RuntimeError(f"unparseable ollama response: {process.stdout[:300]}") from error


class CallableTransport(Transport):
    """Any function of ``(system, user) -> str``. Used by tests and by hosted backends."""

    def __init__(self, function: Callable[[str, str], str], name: str = "callable") -> None:
        self.function = function
        self.name = name

    def complete(self, system: str, user: str) -> str:
        return self.function(system, user)


def extract_proposals(text: str) -> list[Any]:
    """Pull a JSON array out of model output that may be wrapped in prose or a fence."""

    if not text or not text.strip():
        return []
    stripped = text.strip()
    for candidate in (stripped, *(match.group(0) for match in [JSON_ARRAY.search(stripped)] if match)):
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, list):
            return parsed
        if isinstance(parsed, dict):
            if isinstance(parsed.get("proposals"), list):
                return parsed["proposals"]
            return [parsed]
    return []


class LLMMetaDesigner(MetaDesignerBackend):
    name = "llm"

    def __init__(self, transport: Transport, max_proposals: int = 12) -> None:
        self.transport = transport
        self.max_proposals = max_proposals
        self.name = f"llm/{transport.name}"

    def available(self) -> bool:
        return self.transport.available()

    def build_prompt(self, report: ScientistReport) -> str:
        return (
            "Here is the current state of the search.\n\n"
            f"{report.compact_json()}\n\n"
            f"Propose at most {self.max_proposals} experiments as a JSON array. Prioritise "
            "proposals that address a measured failure: an unmeasurable axis, a validation "
            "divergence, a microtest the elites fail, or an instrument defect. If an axis "
            "cannot be measured on this corpus, propose CORPUS_ACQUISITION rather than "
            "mutating it again."
        )

    def propose(self, report: ScientistReport) -> ProposalBatch:
        user = self.build_prompt(report)
        try:
            raw = self.transport.complete(SYSTEM_BRIEF, user)
        except Exception as error:  # noqa: BLE001 - a transport failure is recorded, not fatal
            batch = ProposalBatch()
            batch.rejected.append({
                "reason": f"transport unavailable: {type(error).__name__}: {str(error)[:200]}",
                "payload": None,
            })
            return batch
        default_parent = report.elites[0]["candidate_id"] if report.elites else None
        payloads = [
            normalise(payload, default_parent)
            for payload in extract_proposals(raw)[: self.max_proposals * 3]
        ]
        batch = self._validate_all(payloads, report, raw=raw[:4000])
        if not payloads:
            batch.rejected.append({
                "reason": "model returned no parseable JSON array",
                "payload": raw[:400],
            })
        return batch
