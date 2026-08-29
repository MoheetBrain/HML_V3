"""The surgical loop: diagnose a structure, repair that structure, test only what matters.

`MICROMATH §20`. A three-hour global search is a terrible unit test. When the failure
gradient names a structural weakness, the response is not another population sweep -- it is a
targeted suite for that structure, one to three causal hypotheses aimed at it, and evaluation
restricted to the suites the mutation could plausibly move, plus a regression panel and a
shadow check before anything is promoted.

`§28`: the anchor lab is 45 pairs, which gives three or four per stress -- enough to *locate*
a weakness, nowhere near enough to *resolve* a repair. So a cycle first builds an additional
16-32 pairs for the target structure out of the broader corpus. Those are diagnostic scratch,
not part of the anchor matrix, and MICRO_HIDDEN is never touched.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from hml_v3.micromath import counterfactuals as CF
from hml_v3.micromath import stresses as S
from hml_v3.micromath.domains import DOMAINS, classify
from hml_v3.micromath.schema import MicroPair, pair_id, state_digest

#: A repair must move the target metric by at least this much on the targeted suite before it
#: is worth spending a shadow check on. Preregistered, and deliberately larger than the
#: one-item resolution of a 16-pair suite (1/32 = 0.031).
MATERIAL_IMPROVEMENT = 0.06


def build_targeted_suite(
    pool: list[dict[str, Any]], stress: str, exclude: set[str], size: int = 16,
) -> list[MicroPair]:
    """Extra matched pairs for one structure, from base states the lab does not already use."""

    candidates: list[tuple[str, str, dict[str, Any]]] = []
    for row in pool:
        if row["transition_id"] in exclude:
            continue
        domain, confidence = classify(row)
        if domain not in DOMAINS or confidence != "HIGH":
            continue
        if stress not in S.eligible_stresses(row):
            continue
        candidates.append((domain, row["transition_id"], row))

    # Round-robin across domains so a targeted suite cannot become a single-domain probe --
    # `§42`: a weakness located in one domain must be tested against the others.
    by_domain: dict[str, list[Any]] = {}
    for domain, _tid, row in candidates:
        by_domain.setdefault(domain, []).append(row)
    for rows in by_domain.values():
        rows.sort(key=lambda r: ((r.get("corpus_metadata") or {}).get("canonical_bytes") or 0,
                                 r["transition_id"]))

    suite: list[MicroPair] = []
    index = 0
    while len(suite) < size and any(by_domain.values()):
        for domain in DOMAINS:
            rows = by_domain.get(domain) or []
            if not rows or len(suite) >= size:
                continue
            row = rows.pop(0)
            built = CF.BUILDERS[stress](row, index + 1)
            index += 1
            if built is None or state_digest(row) == state_digest(built.state_b):
                continue
            identifier = pair_id(f"TARGETED_{domain}", stress, row["transition_id"])
            options = built.options
            flip = int(identifier[3:5], 16) % 2 == 1
            if flip:
                options = (options[1], options[0])
            suite.append(MicroPair(
                pair_id=identifier, domain=domain, domain_confidence="HIGH", stress=stress,
                base_transition_id=row["transition_id"],
                source_file=(row["corpus_metadata"] or {}).get("source_file", ""),
                question=built.question, options=options,
                answer_a=built.answer_a, answer_b=built.answer_b, relation=built.relation,
                state_a=row, state_b=built.state_b,
                detail={**built.detail, "targeted": True, "options_flipped": flip}))
    return suite


@dataclass
class ScientistFailurePacket:
    """What a meta-designer is shown. Compact by design -- never the whole corpus."""

    target_stress: str
    question: str
    candidate: str
    candidate_genome: dict[str, Any]
    candidate_accuracy: float
    best_control: str
    best_control_accuracy: float
    per_domain: dict[str, float]
    other_stresses: dict[str, float]
    saturated_stresses: list[str]
    failure_memory: list[dict[str, str]]
    allowed_layer: str = "representation_only"

    def to_dict(self) -> dict[str, Any]:
        return {
            "target_structural_weakness": self.target_stress,
            "what_it_asks": self.question,
            "candidate": self.candidate,
            "candidate_genome": self.candidate_genome,
            "candidate_accuracy_on_target": round(self.candidate_accuracy, 3),
            "best_control": self.best_control,
            "best_control_accuracy_on_target": round(self.best_control_accuracy, 3),
            "delta_best_control": round(
                self.candidate_accuracy - self.best_control_accuracy, 3),
            "target_accuracy_by_domain": {
                k: round(v, 3) for k, v in sorted(self.per_domain.items())},
            "candidate_accuracy_on_other_structures": {
                k: round(v, 3) for k, v in sorted(self.other_stresses.items())},
            "saturated_and_excluded_from_selection": self.saturated_stresses,
            "failure_memory": self.failure_memory,
            "allowed_implementation_layer": self.allowed_layer,
            "chance": 0.5,
        }


@dataclass
class CycleResult:
    cycle: int
    weakness: str
    hypothesis: str
    mutation: dict[str, Any]
    proposer: str
    candidate_id: str
    gates_passed: bool
    dev_before: float
    dev_after: float
    shadow_before: float | None
    shadow_after: float | None
    regression: dict[str, float]
    verdict: str
    reason: str
    detail: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "cycle": self.cycle, "weakness": self.weakness,
            "hypothesis": self.hypothesis, "mutation": self.mutation,
            "proposer": self.proposer, "candidate_id": self.candidate_id,
            "gates_passed": self.gates_passed,
            "targeted_before": round(self.dev_before, 4),
            "targeted_after": round(self.dev_after, 4),
            "targeted_delta": round(self.dev_after - self.dev_before, 4),
            "shadow_before": None if self.shadow_before is None else round(self.shadow_before, 4),
            "shadow_after": None if self.shadow_after is None else round(self.shadow_after, 4),
            "regression": {k: round(v, 4) for k, v in sorted(self.regression.items())},
            "verdict": self.verdict, "reason": self.reason, "detail": self.detail,
        }
