"""Layer 3, deliberately frozen.

`MISSION §10`: the expression experiment must differ in INFORMATION EXPOSURE, not
punctuation. The cleanest way to guarantee that is to have exactly one serializer, with no
options, shared by every view under test. Then any behavioural difference between two views
is attributable to their content, because their surface treatment is byte-for-byte the same
function.

This is the opposite of the old pipeline, which offered thirty-nine surface axes and one
content axis. `D-025` is what that asymmetry cost.

The format is intentionally plain: a block header, then indented ``label: value`` rows. It
is not competing to be a good notation. It is a constant.
"""

from __future__ import annotations

from typing import Any

from hml_v3.projection.model_view import SelectiveModelView, ViewBlock

INDENT = "  "


def _value(value: Any) -> str:
    if isinstance(value, (list, tuple)):
        return "[" + ", ".join(_value(v) for v in value) + "]"
    if value is None:
        return "-"
    return str(value)


def render_block(block: ViewBlock) -> str:
    lines = [block.kind if block.retrieval_key is None
             else f"{block.kind} (retrievable as {block.retrieval_key})"]
    for label, value in block.rows:
        lines.append(f"{INDENT}{label}: {_value(value)}")
    return "\n".join(lines)


def render(view: SelectiveModelView, *, include_retrievable: bool = False) -> str:
    """Serialize a view. Retrievable blocks are withheld unless explicitly asked for.

    A `RETRIEVAL_REQUIRED` block that is printed anyway would be an `EXPLICIT` block wearing
    a different label, and the audit would then be describing a view that does not exist.
    """

    blocks = view.blocks if include_retrievable else view.visible_blocks()
    return "\n".join(render_block(b) for b in blocks)


def render_with_retrieval(view: SelectiveModelView, keys: list[str]) -> str:
    """The visible view plus the named side views, for testing a retrieval policy."""

    wanted = set(keys)
    blocks = [b for b in view.blocks
              if b.retrieval_key is None or b.retrieval_key in wanted]
    return "\n".join(render_block(b) for b in blocks)
