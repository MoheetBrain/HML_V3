"""Proposal schemas: the only channel through which a proposal may reach the search.

A meta-designer — deterministic or model-driven — emits JSON. It never edits files, never
mutates the controller, and never touches the canonical layer. Everything it can ask for is
one of the proposal types below, and every proposal is validated here before any compute is
spent on it.

This is what keeps an open-ended loop safe: the search space can grow, but only through a
typed, checked, recorded interface.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
import re
from typing import Any

SCHEMA_VERSION = "meta-designer-proposal-v1.0.0"

PROPOSAL_TYPES = (
    "AXIS_MUTATION",            # change one existing axis on one parent
    "ARCHITECTURAL_HYPOTHESIS",  # a coherent multi-axis intervention
    "NEW_AXIS",                 # add a value dimension to the genome
    "NEW_PRIMITIVE",            # add a representation mechanism the compiler must learn
    "CORPUS_ACQUISITION",       # the corpus cannot answer the question
    "NEW_MICROTEST",            # the instruments cannot answer the question
    "INSTRUMENT_FIX",           # an instrument is measuring the wrong thing
    "ELIMINATE_CANDIDATE",      # retire a candidate and say why
)

#: A new axis may only change how the canonical state is *written*. Anything claiming to add
#: information is a semantic change and is refused outright.
IMPLEMENTATION_LAYERS = ("representation_only", "projection_only", "surface_only")

NAME_PATTERN = re.compile(r"^[a-z][a-z0-9_]{2,48}$")
VALUE_PATTERN = re.compile(r"^[A-Z][A-Z0-9_]{0,48}$")


class ProposalRejected(Exception):
    """The proposal is malformed, unsafe, or outside what a meta-designer may ask for."""


@dataclass
class ValidatedProposal:
    proposal_type: str
    payload: dict[str, Any]
    proposal_id: str
    source: str
    generation: int
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": SCHEMA_VERSION,
            "proposal_id": self.proposal_id,
            "proposal_type": self.proposal_type,
            "source": self.source,
            "generation": self.generation,
            "warnings": self.warnings,
            "payload": self.payload,
        }


def _require(payload: dict[str, Any], *keys: str) -> None:
    missing = [key for key in keys if key not in payload or payload[key] in (None, "", [])]
    if missing:
        raise ProposalRejected(f"missing required fields: {sorted(missing)}")


def _require_text(payload: dict[str, Any], key: str, minimum: int = 20) -> None:
    value = payload.get(key)
    if not isinstance(value, str) or len(value.strip()) < minimum:
        raise ProposalRejected(
            f"{key} must be at least {minimum} characters of actual reasoning"
        )


def proposal_id(payload: dict[str, Any], source: str, generation: int) -> str:
    digest = hashlib.sha256(
        json.dumps(
            {"payload": payload, "source": source, "generation": generation},
            sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        ).encode()
    ).hexdigest()
    return f"P_{digest[:12]}"


def validate(
    payload: dict[str, Any], source: str, generation: int,
    known_axes: set[str] | None = None,
) -> ValidatedProposal:
    """Validate one proposal. Raises :class:`ProposalRejected` with a specific reason."""

    if not isinstance(payload, dict):
        raise ProposalRejected("a proposal must be a JSON object")
    kind = payload.get("proposal_type")
    if kind not in PROPOSAL_TYPES:
        raise ProposalRejected(
            f"unknown proposal_type {kind!r}; allowed: {list(PROPOSAL_TYPES)}"
        )
    warnings: list[str] = []
    handler = {
        "AXIS_MUTATION": _validate_axis_mutation,
        "ARCHITECTURAL_HYPOTHESIS": _validate_architectural,
        "NEW_AXIS": _validate_new_axis,
        "NEW_PRIMITIVE": _validate_new_primitive,
        "CORPUS_ACQUISITION": _validate_corpus,
        "NEW_MICROTEST": _validate_microtest,
        "INSTRUMENT_FIX": _validate_instrument_fix,
        "ELIMINATE_CANDIDATE": _validate_elimination,
    }[kind]
    handler(payload, known_axes or set(), warnings)
    return ValidatedProposal(
        proposal_type=kind, payload=payload,
        proposal_id=proposal_id(payload, source, generation),
        source=source, generation=generation, warnings=warnings,
    )


def _validate_common_science(payload: dict[str, Any]) -> None:
    """Every intervention must be falsifiable and name its mechanism."""

    _require(payload, "hypothesis", "mechanism", "falsification")
    _require_text(payload, "hypothesis", 20)
    _require_text(payload, "mechanism", 20)
    _require_text(payload, "falsification", 15)


def _validate_axis_mutation(payload: dict[str, Any], axes: set[str], warnings: list[str]) -> None:
    _require(payload, "parent_id", "axis", "value")
    _validate_common_science(payload)
    if axes and payload["axis"] not in axes:
        raise ProposalRejected(
            f"axis {payload['axis']!r} is not in the genome; propose NEW_AXIS instead"
        )
    if "target_metric" not in payload:
        warnings.append("no target_metric named; the hypothesis cannot be scored automatically")


def _validate_architectural(payload: dict[str, Any], axes: set[str], warnings: list[str]) -> None:
    _require(payload, "parent_id", "changes")
    _validate_common_science(payload)
    changes = payload["changes"]
    if not isinstance(changes, dict) or not changes:
        raise ProposalRejected("changes must be a non-empty {axis: value} object")
    if axes:
        unknown = sorted(set(changes) - axes)
        if unknown:
            raise ProposalRejected(f"unknown axes in changes: {unknown}")
    if len(changes) < 2:
        warnings.append("an architectural hypothesis with one axis is an AXIS_MUTATION")


def _validate_new_axis(payload: dict[str, Any], axes: set[str], warnings: list[str]) -> None:
    _require(payload, "name", "values", "implementation_layer", "tests_required")
    _validate_common_science(payload)
    name = payload["name"]
    if not NAME_PATTERN.match(name):
        raise ProposalRejected(f"axis name {name!r} must be lower_snake_case, 3-49 chars")
    if name in axes:
        raise ProposalRejected(f"axis {name!r} already exists")
    values = payload["values"]
    if not isinstance(values, list) or len(values) < 2:
        raise ProposalRejected("a new axis needs at least two values to be searchable")
    if len(set(values)) != len(values):
        raise ProposalRejected("axis values must be distinct")
    for value in values:
        if not isinstance(value, str) or not VALUE_PATTERN.match(value):
            raise ProposalRejected(f"axis value {value!r} must be UPPER_SNAKE_CASE")
    if payload["implementation_layer"] not in IMPLEMENTATION_LAYERS:
        raise ProposalRejected(
            f"implementation_layer must be one of {list(IMPLEMENTATION_LAYERS)}; a proposal "
            "that changes the canonical layer is a semantic change and is refused"
        )
    if not isinstance(payload["tests_required"], list) or not payload["tests_required"]:
        raise ProposalRejected("a new axis must name the tests that would falsify it")
    if "semantic_roundtrip" not in payload["tests_required"]:
        warnings.append("semantic_roundtrip added: it is mandatory for every candidate")
        payload["tests_required"] = ["semantic_roundtrip", *payload["tests_required"]]


def _validate_new_primitive(payload: dict[str, Any], axes: set[str], warnings: list[str]) -> None:
    _validate_new_axis(payload, axes, warnings)
    _require(payload, "projection_behaviour")
    _require_text(payload, "projection_behaviour", 40)
    if payload["implementation_layer"] == "surface_only":
        warnings.append(
            "a surface-only change is an axis, not a primitive; recorded as proposed"
        )


def _validate_corpus(payload: dict[str, Any], axes: set[str], warnings: list[str]) -> None:
    _require(payload, "reason", "stratum", "values", "desired_per_value")
    _require_text(payload, "reason", 20)
    if not isinstance(payload["values"], list) or not payload["values"]:
        raise ProposalRejected("values must be a non-empty list of strata values")
    desired = payload["desired_per_value"]
    if not isinstance(desired, int) or not 1 <= desired <= 5000:
        raise ProposalRejected("desired_per_value must be an integer in 1..5000")


def _validate_microtest(payload: dict[str, Any], axes: set[str], warnings: list[str]) -> None:
    _require(payload, "name", "question", "ground_truth_source", "measured_quantity")
    _require_text(payload, "question", 20)
    if not NAME_PATTERN.match(payload["name"]):
        raise ProposalRejected("microtest name must be lower_snake_case")
    if payload["ground_truth_source"] != "canonical_state":
        raise ProposalRejected(
            "a microtest's ground truth must come from the canonical state, never from a "
            "rendering or a model"
        )


def _validate_instrument_fix(payload: dict[str, Any], axes: set[str], warnings: list[str]) -> None:
    _require(payload, "instrument", "defect", "correction")
    _require_text(payload, "defect", 25)
    _require_text(payload, "correction", 20)


def _validate_elimination(payload: dict[str, Any], axes: set[str], warnings: list[str]) -> None:
    _require(payload, "candidate_id", "reason", "failure_type")
    _require_text(payload, "reason", 20)


# --------------------------------------------------------------------------- safety checks

#: Substrings that indicate a proposal is trying to reach outside the representation layer.
FORBIDDEN_TOKENS = (
    "canonical_math_state", "canonicalmathstate", "semantic_core", "lean_runtime",
    "verifier", "import ", "__import__", "subprocess", "eval(", "exec(", "open(",
    "os.system", "sealed",
)


def static_safety(payload: dict[str, Any]) -> list[str]:
    """Reject anything reaching for the semantic substrate, the sealed split, or the host.

    A meta-designer proposes *representations*. A proposal that names the canonical layer,
    the verifier or the sealed split is either confused or attempting something it must not
    be able to do, and either way it does not run.
    """

    blob = json.dumps(payload, ensure_ascii=False).lower()
    hits = [token for token in FORBIDDEN_TOKENS if token in blob]
    return hits
