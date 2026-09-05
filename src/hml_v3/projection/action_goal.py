"""The action-to-goal edge: a relation the old space could not express at all.

`MISSION §13`. `FM-044` established that no axis of the 42-axis genome renders which goal an
action acts on. `_action_section` emits source, kind, elaborator, premises and local refs and
never names a goal; the delta section names goals as `_uniq.*` ids that the identity codec
leaves unmapped while the goal section renders `m3`/`m7`, so the two namespaces never meet on
the page.

That made MULTI_GOAL unmeasurable and forced its withdrawal. It also makes it the cleanest
possible test of the content-bearing thesis, because the intervention is not "spell the
relation differently" -- there is no existing spelling. It is "put the relation on the page
at all".

The question is causal and narrow:

    DOES MATERIALISING THE RELATION IMPROVE READABILITY?

Not "should the language always carry explicit goal labels". `§13` is explicit that the
purpose is the causal answer, not a permanent design commitment.

Synthetic states again, because the relation is absent from the corpus by construction and
ground truth must come from a typed generator (`§31`), never from a model.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from typing import Any

from hml_v3.projection import model_view as MV
from hml_v3.projection.model_view import SelectiveModelView, ViewBlock

GENERATOR_VERSION = "synthetic-action-goal-v1.0.0"

IMPLICIT_ADJACENCY = "IMPLICIT_ADJACENCY"
EXPLICIT_EDGE = "EXPLICIT_EDGE"
GOAL_LOCAL_ACTION = "GOAL_LOCAL_ACTION"
SCRAMBLED_NEGATIVE = "SCRAMBLED_NEGATIVE"
ABSENT_NEGATIVE = "ABSENT_NEGATIVE"

VIEWS: tuple[str, ...] = (
    IMPLICIT_ADJACENCY, EXPLICIT_EDGE, GOAL_LOCAL_ACTION, SCRAMBLED_NEGATIVE, ABSENT_NEGATIVE)


@dataclass
class SyntheticActionGoal:
    """A multi-goal state whose acted-on goal is known by construction."""

    state_id: str
    goals: list[str]
    #: The goal the action actually acts on.
    target_goal: str
    action_id: str
    #: goal -> the declarations in its local context.
    context: dict[str, list[str]]
    #: The declarations the action consumes; all of them live in the target goal.
    arguments: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {"state_id": self.state_id, "goals": self.goals,
                "target_goal": self.target_goal, "action_id": self.action_id,
                "context": self.context, "arguments": self.arguments,
                "generator": GENERATOR_VERSION,
                "provenance": {"origin": "TYPED_GENERATOR",
                               "truth": "KNOWN_BY_CONSTRUCTION",
                               "llm_involvement": "NONE"}}


def generate(index: int, goals: int = 4, per_goal: int = 3) -> SyntheticActionGoal:
    """Build a state with several goals, one of which the action acts on.

    The target goal is chosen by hash rather than by position, so it is not systematically
    first -- the defect that made the V2 MULTI_GOAL instrument a constant-answer question
    (`FM-044`) and cost 277 seconds of inference to notice.
    """

    digest = hashlib.sha256(f"{GENERATOR_VERSION}|{index}".encode()).hexdigest()
    labels = [f"g{i + 1}" for i in range(goals)]
    target = labels[int(digest[:4], 16) % goals]
    context: dict[str, list[str]] = {}
    used: set[str] = set()
    for position, label in enumerate(labels):
        names = []
        for slot in range(per_goal):
            tag = f"v{10 + (index * 11 + position * 17 + slot * 5) % 80}"
            while tag in used:
                tag = f"v{10 + (int(tag[1:]) - 10 + 1) % 80}"
            used.add(tag)
            names.append(tag)
        context[label] = names
    return SyntheticActionGoal(
        state_id=f"AG_{digest[:12]}", goals=labels, target_goal=target,
        action_id=f"a{10 + index % 80}", context=context,
        arguments=context[target][:2])


def build(view: str, state: SyntheticActionGoal) -> SelectiveModelView:
    """Project one state into one ModelView. Serialization is the frozen one, as always."""

    out = SelectiveModelView(label=view, source_id=state.state_id)
    out.provenance = {"generator": GENERATOR_VERSION, "origin": "TYPED_GENERATOR"}

    goal_rows: list[tuple[str, Any]] = []
    for label in state.goals:
        goal_rows.append((label, state.context[label]))
    out.add(ViewBlock("goals", goal_rows))

    if view == IMPLICIT_ADJACENCY:
        # Everything a reader needs is present -- the action names the declarations it uses,
        # and those declarations appear in exactly one goal's context -- but the link itself
        # is never stated. This is the closest analogue of what the old space could express.
        out.add(ViewBlock("action", [("id", state.action_id),
                                     ("uses", state.arguments)]))
        out.expose(MV.ACTION_GOAL, MV.IMPLICIT_RECOVERABLE,
                   "recoverable by finding which goal's context holds the used declarations")

    elif view == EXPLICIT_EDGE:
        out.add(ViewBlock("action", [("id", state.action_id),
                                     ("uses", state.arguments)]))
        out.add(ViewBlock("action_goal_edge", [
            ("action", state.action_id), ("target_goal", state.target_goal)]))
        out.expose(MV.ACTION_GOAL, MV.EXPLICIT, "the edge is stated as its own record")

    elif view == GOAL_LOCAL_ACTION:
        # The action is placed inside its goal's block rather than named separately, so the
        # relation is carried by containment. Organisation, not a new statement.
        rows: list[tuple[str, Any]] = []
        for label in state.goals:
            if label == state.target_goal:
                rows.append((label, {"context": state.context[label],
                                     "action": state.action_id,
                                     "uses": state.arguments}))
            else:
                rows.append((label, {"context": state.context[label]}))
        out.blocks = [ViewBlock("goals_with_local_action", rows)]
        out.expose(MV.ACTION_GOAL, MV.EXPLICIT,
                   "the action sits inside the block of the goal it acts on")

    elif view == SCRAMBLED_NEGATIVE:
        # The relation is destroyed: the action cites declarations from a goal it does not
        # act on, so following the arguments leads to the wrong answer.
        others = [g for g in state.goals if g != state.target_goal]
        decoy = others[int(state.state_id[-1], 16) % len(others)] if others else state.goals[0]
        out.add(ViewBlock("action", [("id", state.action_id),
                                     ("uses", state.context[decoy][:2])]))
        out.expose(MV.ACTION_GOAL, MV.IMPLICIT_RECOVERABLE,
                   "arguments point at a goal the action does not act on")
        out.notes["decoy_goal"] = decoy

    elif view == ABSENT_NEGATIVE:
        # `MISSION §14`: a true known-bad. The action names no declarations at all, so the
        # relation is not recoverable by any route.
        out.add(ViewBlock("action", [("id", state.action_id)]))
        out.expose(MV.ACTION_GOAL, MV.ABSENT,
                   "the action names nothing that could locate a goal")

    else:
        raise ValueError(f"unknown view {view!r}")

    return out


def question(state: SyntheticActionGoal) -> tuple[str, tuple[str, ...], str]:
    """Options in an order drawn independently of how the target was chosen.

    The first version rotated by ``state_id[3:7]``, which is the same hash slice that picks
    the target goal -- so the rotation exactly cancelled the target's index and the answer
    sat at position 0 on all 48 items. That is `FM-045` a second time: two decisions must be
    drawn from two independent hashes or they are not independent.
    """

    spin = int(hashlib.sha256(f"options|{state.state_id}".encode()).hexdigest()[:6], 16)
    offset = spin % len(state.goals)
    options = tuple(state.goals[offset:] + state.goals[:offset])
    return ("Which goal does the action act on?", options, state.target_goal)
