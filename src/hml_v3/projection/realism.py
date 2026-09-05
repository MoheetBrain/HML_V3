"""The factors that actually separate a real Lean document from a clean synthetic one.

`REAL_LEAN_GAP_V1 §5`, `§6`. The first factor sweep varied nine kinds of surrounding clutter
and none of them reproduced the 0.708 collapse. It could not have: every one of them added
material that has nothing to do with the target relation, and the iso-token experiment showed
neutral filler at 6,400 characters costs nothing at all. The only filler that moved anything
was `D_NONTARGET_MATH` at -0.167 -- structure that is *about* the same identities.

The mechanical audit of the 45 real items (`REAL_ITEM_AUDIT.json`) says what the synthetic
states never modelled, and none of it is clutter:

    lead 1                   35 of 45 real items; the answer beats the runner-up by one
                             level. Clean synthetic states are built at lead 2.
    recurrence ~3.7          every identity occurs several times at several depths; the
                             answer identity a median of 7 times. Clean states: exactly once.
    target copies 2-6        the goal target is reprinted verbatim elsewhere in the document
                             -- as the metavariable's type, and again in state-after.
    deeper elsewhere         on 33 of 45 items, one of the OPTIONS occurs deeper inside a
                             context declaration's type than the answer does in the target.
                             The question says "in the goal target"; the page does not stop
                             a reader from answering about the deepest thing it can see.

The first two are internal to the target and belong to the dense generator. The last two are
this module: they are relation-bearing material that competes with the target, which is a
different object from the unrelated clutter already measured and found null.

Answer validity is unaffected and that is checked, not assumed. A verbatim copy of the target
has the target's own answer, and a context type is not the goal target, so the recorded
answer stays the unique deepest reference *of the goal target* under every factor here.
"""

from __future__ import annotations

from typing import Any

import hashlib

from hml_v3.projection import clutter as CL
from hml_v3.projection.dense import true_depths
from hml_v3.projection.model_view import ViewBlock
from hml_v3.projection.synthetic import SyntheticExpression, _apply, _reference, _symbol

REALISM_VERSION = "realism-v1.0.0"

#: Verbatim reprints of the goal target elsewhere in the document. Real median 2, max 6.
TARGET_COPIES = "target_copies"
#: Context declarations whose types embed an OPTION deeper than the answer sits in the target.
DEEPER_IN_CONTEXT = "deeper_in_context"
#: Neutral declaration filler, carried over so the pre-registered factor is still represented.
CONTEXT_SIZE = "context_size"

FACTORS: tuple[str, ...] = (TARGET_COPIES, DEEPER_IN_CONTEXT, CONTEXT_SIZE)

#: The labels a real document reprints the target under, in the order TYPED_AST emits them.
COPY_LABELS: tuple[str, ...] = ("metavariable_type", "state_after_target", "goal_1_target",
                                "metavariable_type_2", "state_after_target_2")


def _h(seed: str, modulus: int) -> int:
    return int(hashlib.sha256(seed.encode()).hexdigest()[:8], 16) % max(1, modulus)


def _embed_at_depth(identity: str, depth: int, tag: str) -> dict[str, Any]:
    """A type expression carrying ``identity`` at exactly ``depth`` levels of nesting."""

    node: dict[str, Any] = _reference(identity)
    for level in range(depth):
        spin = _h(f"{tag}|{level}", 2)
        other = _symbol(f"t{level % 7}")
        node = _apply(node, other) if spin == 0 else _apply(other, node)
    return node


def context_rows(expression: SyntheticExpression, options: list[str], *,
                 deeper_in_context: int, context_size: int) -> list[tuple[str, Any]]:
    """The context block: the real declarations, plus whichever filler the factors ask for."""

    rows: list[tuple[str, Any]] = [
        ("declaration", name) for name in sorted(expression.depth_of)]

    if deeper_in_context:
        # Each planted type carries a DISTRACTOR option deeper than the answer sits in the
        # target, exactly the configuration 33 of 45 real items are in. The answer identity
        # is never planted: that would put the answer's own deepest occurrence outside the
        # goal target and change what the question is about.
        distractors = [o for o in options if o != expression.deepest]
        for slot in range(deeper_in_context):
            identity = distractors[slot % len(distractors)]
            depth = expression.depth + 1 + slot
            rendered = CL._render_expression(
                _embed_at_depth(identity, depth, f"{expression.state_id}|deep|{slot}"))
            rows.append(("declaration", f"w{20 + slot} : {rendered}"))

    for slot in range(context_size):
        rows.append(("declaration", f"w{40 + slot} : t{slot % 7}"))
    return rows


def build_view(expression: SyntheticExpression, options: list[str], levels: dict[str, int],
               *, label: str = "REALISTIC"):
    """A NESTED_ONLY view of a dense target under the realism factors."""

    from hml_v3.projection.model_view import SelectiveModelView
    from hml_v3.projection import model_view as MV

    target = expression.transition["state_before"]["goals"][0]["target"]
    rendered_target = CL._render_expression(target)

    view = SelectiveModelView(label=label, source_id=expression.state_id)
    view.provenance = {"generator": expression.to_dict()["generator"],
                       "realism": REALISM_VERSION, "levels": dict(sorted(levels.items())),
                       "origin": "TYPED_GENERATOR"}
    view.add(ViewBlock("context", context_rows(
        expression, options,
        deeper_in_context=levels.get(DEEPER_IN_CONTEXT, 0),
        context_size=levels.get(CONTEXT_SIZE, 0))))
    view.add(ViewBlock("goal_target", [("expression", rendered_target)]))

    copies = levels.get(TARGET_COPIES, 0)
    if copies:
        view.add(ViewBlock("elsewhere_in_the_state", [
            (COPY_LABELS[slot % len(COPY_LABELS)], rendered_target)
            for slot in range(copies)]))
    view.expose(MV.EXPRESSION_PARENT, MV.IMPLICIT_RECOVERABLE,
                "parentage is recoverable only by matching brackets")
    view.expose(MV.EXPRESSION_DEPTH, MV.IMPLICIT_RECOVERABLE,
                "depth is recoverable only by counting nesting")
    return view


def answer_still_unique(expression: SyntheticExpression, options: list[str]) -> bool:
    """The recorded answer is still the unique deepest reference OF THE GOAL TARGET.

    Nothing in this module edits the target, so this should always hold; it is checked on
    every item anyway, because `FM-054` was precisely a generator whose recorded answer was
    trusted rather than re-derived.
    """

    target = expression.transition["state_before"]["goals"][0]["target"]
    walked = true_depths(target)
    if expression.deepest not in walked:
        return False
    maxima = {identity: max(depths) for identity, depths in walked.items()}
    best = max(maxima.values())
    winners = [identity for identity, depth in maxima.items() if depth == best]
    return winners == [expression.deepest] and all(o in maxima for o in options)


def deepest_anywhere(expression: SyntheticExpression, options: list[str],
                     levels: dict[str, int]) -> str:
    """What a reader answering about the DEEPEST THING ON THE PAGE would pick.

    Reported beside every cell. If accuracy collapses and the errors concentrate on this
    identity, the failure is a scope failure -- the reader answered a different question --
    rather than an inability to count nesting.
    """

    if not levels.get(DEEPER_IN_CONTEXT):
        return expression.deepest
    distractors = [o for o in options if o != expression.deepest]
    # The last planted declaration is the deepest one.
    return distractors[(levels[DEEPER_IN_CONTEXT] - 1) % len(distractors)]
