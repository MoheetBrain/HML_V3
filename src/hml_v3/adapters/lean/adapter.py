"""Explicit LeanTransition -> CanonicalTransition adapter."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from hml_v3.canonical.models import (
    CanonicalAction,
    CanonicalMathState,
    CanonicalTransition,
    Declaration,
    Expression,
    Goal,
    StateDelta,
    VerifierResult,
    stable_sha256,
)

from .models import LeanActionObservation, LeanStateObservation, LeanTransition
from .parser import ParsedDeclaration, ParsedGoal, metavariables_in, parse_lean_state, validate_observation


SCHEMA_VERSION = "canonical-transition-0.1.0"


def _source_record_sha(record: dict[str, Any]) -> str:
    original = {key: value for key, value in record.items() if key != "v3_formal_source_enrichment"}
    encoded = json.dumps(original, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def lean_transition_from_record(
    record: dict[str, Any], replay_certificate: dict[str, Any] | None = None
) -> LeanTransition:
    lean = record["lean"]
    before = record["state_before"]
    after = record["state_after"]
    observed = record["observed_action"]
    enrichment = record.get("v3_formal_source_enrichment", {})
    mathlib = record.get("provenance", {}).get("mathlib_commit") or record.get("mathlib_commit")
    if not mathlib:
        mathlib = "29dcec074de168ac2bf835a77ef68bbe069194c5"
    return LeanTransition(
        transition_id=record["example_id"],
        theorem_id=record["theorem_id"],
        source_file=record["source_file"],
        transition_index=int(record["transition_index"]),
        official_split=record["lean_official_split"],
        mathlib_commit=mathlib,
        lean_version="v4.10.0-rc1",
        state_before=LeanStateObservation(
            raw_state=lean["raw_state_before"],
            hypotheses=tuple(dict(item) for item in before["hypotheses"]),
            focused_target=before["target"],
            goal_count=int(before["n_goals"]),
        ),
        action=LeanActionObservation(
            raw_tactic=lean["raw_tactic"],
            premises_used=tuple(
                enrichment.get("premise_full_names", observed.get("premises_used", ()))
            ),
            effect_class=observed["effect_class"],
            recorded_effect=dict(observed),
        ),
        state_after=LeanStateObservation(
            raw_state=lean["raw_state_after"],
            hypotheses=tuple(dict(item) for item in after["hypotheses"]),
            focused_target=after["target"],
            goal_count=int(after["n_goals"]),
        ),
        source_record_sha256=_source_record_sha(record),
        source_record=record,
        replay_certificate=replay_certificate,
    )


def _state(transition: LeanTransition, observation: LeanStateObservation, phase: str) -> CanonicalMathState:
    state_id = f"{transition.transition_id}:{phase}"
    parsed = parse_lean_state(observation.raw_state)
    declarations: list[Declaration] = []
    declaration_ids: dict[tuple[str, str, str | None], str] = {}
    goal_contexts: list[tuple[str, ...]] = []
    source_goals = parsed.goals
    if not source_goals and observation.goal_count:
        fallback = tuple(
            ParsedDeclaration((item["name"],), item["type"]) for item in observation.hypotheses
        )
        source_goals = (ParsedGoal(None, fallback, observation.focused_target),)
    for goal_index, parsed_goal in enumerate(source_goals):
        context_ids: list[str] = []
        for group in parsed_goal.declarations:
            for name in group.names:
                key = (name, group.type_text, group.value_text)
                declaration_id = declaration_ids.get(key)
                if declaration_id is None:
                    index = len(declarations)
                    declaration_id = f"{state_id}:decl:{index}"
                    declaration_ids[key] = declaration_id
                    value_expression = None
                    if group.value_text is not None:
                        value_expression = Expression.from_surface(
                            f"{declaration_id}:value", group.value_text, "LOCAL_DEFINITION_VALUE"
                        )
                    declarations.append(
                        Declaration(
                            declaration_id=declaration_id,
                            name=name,
                            type_expression=Expression.from_surface(
                                f"{declaration_id}:type", group.type_text, "DECLARATION_TYPE"
                            ),
                            value_expression=value_expression,
                            scope_id=f"{state_id}:goal:{goal_index}:context",
                        )
                    )
                context_ids.append(declaration_id)
        goal_contexts.append(tuple(context_ids))
    goal_status = "SOLVED" if observation.goal_count == 0 else "OPEN"
    goals = tuple(
        Goal(
            f"{state_id}:goal:{index}",
            Expression.from_surface(
                f"{state_id}:goal:{index}:target", parsed_goal.target, "GOAL_TARGET"
            ),
            goal_status,
            goal_contexts[index],
            parsed_goal.case_label,
        )
        for index, parsed_goal in enumerate(source_goals)
    )
    inconsistencies = validate_observation(
        observation.raw_state,
        observation.hypotheses,
        observation.focused_target,
        observation.goal_count,
    )
    accounting = {
        "raw_state": "REPRESENTED",
        "local_context_names_and_types": "REPRESENTED",
        "focused_goal": "REPRESENTED",
        "nonfocused_goals": "REPRESENTED" if observation.goal_count > 1 and parsed.clean else "NOT_APPLICABLE",
        "expression_ast": "SOURCE_SYSTEM_SPECIFIC_NOT_AVAILABLE_IN_SOURCE_RECORD",
        "binder_structure": "SOURCE_SYSTEM_SPECIFIC_NOT_AVAILABLE_IN_SOURCE_RECORD",
        "metavariable_assignments": "SOURCE_SYSTEM_SPECIFIC_NOT_AVAILABLE_IN_SOURCE_RECORD",
        "namespace_environment": "EXTERNAL_REFERENCE",
    }
    if inconsistencies:
        accounting["adapter_consistency"] = "INFORMATION_LOSS_OR_SOURCE_INCONSISTENCY"
    else:
        accounting["adapter_consistency"] = "REPRESENTED"
    return CanonicalMathState(
        state_id=state_id,
        source_system="LEAN4",
        declarations=tuple(declarations),
        goals=goals,
        metavariables=metavariables_in(
            observation.raw_state,
            *(item["type"] for item in observation.hypotheses),
            observation.focused_target,
        ),
        namespace_environment_refs={
            "mathlib_commit": transition.mathlib_commit,
            "lean_version": transition.lean_version,
            "source_file": transition.source_file,
        },
        evidence=({"kind": "LEAN_PRETTY_PRINTED_TACTIC_STATE", "raw_sha256": stable_sha256(observation.raw_state)},),
        provenance={
            "theorem_id": transition.theorem_id,
            "transition_index": transition.transition_index,
            "official_split": transition.official_split,
        },
        source_specific={
            "raw_state": observation.raw_state,
            "raw_state_sha256": stable_sha256(observation.raw_state),
            "goal_count": observation.goal_count,
            "decomposed_goal_count": len(parsed.goals),
            "decomposition_clean": parsed.clean,
            "unparsed_lines": list(parsed.unparsed_lines),
            "adapter_inconsistencies": inconsistencies,
        },
        information_accounting=accounting,
    )


def _delta(before: CanonicalMathState, after: CanonicalMathState, observed: dict[str, Any]) -> StateDelta:
    before_by_name = {item.name: item.type_expression.surface for item in before.declarations}
    after_by_name = {item.name: item.type_expression.surface for item in after.declarations}
    added = tuple(name for name in after_by_name if name not in before_by_name)
    removed = tuple(name for name in before_by_name if name not in after_by_name)
    rebound = tuple(name for name in before_by_name.keys() & after_by_name.keys() if before_by_name[name] != after_by_name[name])
    goals_before = int(before.source_specific["goal_count"])
    goals_after = int(after.source_specific["goal_count"])
    return StateDelta(
        declarations_added=added,
        declarations_removed=removed,
        declarations_rebound=rebound,
        goals_before=goals_before,
        goals_after=goals_after,
        goals_generated=max(goals_after - goals_before, 0),
        goals_solved=max(goals_before - goals_after, 0),
        focused_target_changed=bool(observed.get("target_changed")),
        recorded_effect_class=str(observed["effect_class"]),
    )


def adapt_lean_transition(source: LeanTransition) -> CanonicalTransition:
    before = _state(source, source.state_before, "before")
    after = _state(source, source.state_after, "after")
    certificate = source.replay_certificate
    replay_status = certificate.get("replay_status") if certificate else None
    verifier = VerifierResult(
        authority="LEAN_DOJO_BENCHMARK4_FORMAL_TRACE",
        status="FRESH_REPLAY_PASS" if replay_status == "REPLAY_PASS" else "FORMAL_TRACE_ACCEPTED",
        accepted=True,
        fresh_replay_status=replay_status,
        source_record_sha256=source.source_record_sha256,
        certificate_id=certificate.get("certificate_id") if certificate else None,
        certificate_content_sha256=certificate.get("content_sha256_excluding_created_at") if certificate else None,
    )
    action = CanonicalAction(
        action_id=f"{source.transition_id}:action",
        action_kind="LEAN_TACTIC",
        target_goal_ids=tuple(goal.goal_id for goal in before.goals[:1]),
        arguments=(),
        substitutions=(),
        referenced_premises=source.action.premises_used,
        expected_effect=dict(source.action.recorded_effect),
        source_syntax=source.action.raw_tactic,
        source_syntax_sha256=stable_sha256(source.action.raw_tactic),
    )
    return CanonicalTransition(
        transition_id=source.transition_id,
        schema_version=SCHEMA_VERSION,
        state_before=before,
        action=action,
        state_delta=_delta(before, after, source.action.recorded_effect),
        state_after=after,
        verifier_result=verifier,
        provenance={
            "source_repository": "https://github.com/leanprover-community/mathlib4",
            "source_commit": source.mathlib_commit,
            "source_file": source.source_file,
            "theorem_id": source.theorem_id,
            "transition_index": source.transition_index,
            "official_split": source.official_split,
            "source_record_sha256": source.source_record_sha256,
        },
    )
