"""Reversible surface codecs for normalized Lean expression trees.

The input is the neutral expression node produced by
:func:`hml_v3.adapters.lean.runtime_v2.normalize_expr`. Every codec here is a matched
``emit``/``parse`` pair: the parser is derived from the same genome that drove emission, so
losslessness is a property of the codec rather than a per-candidate promise.

Where a genome axis deliberately discards information (``universe_visibility=OMITTED``,
``const_name_form=LAST_COMPONENT``) the parser reconstructs what it can and the hard
round-trip gate rejects the candidate. That is the intended behaviour: the space contains
lossy points so the gates can be shown to bite.
"""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any

LEVEL_NODES = {"zero", "succ", "max", "imax", "param", "mvar"}

#: Lean 4.10 spells its literal kinds ``NAT`` and ``STRING``. The untagged literal form has
#: to reproduce that spelling exactly, or it silently renames every literal in the corpus.
NATURAL_LITERAL = "NAT"
STRING_LITERAL = "STRING"


def _literal_value(kind: str, raw: str):
    if kind.upper().startswith("NAT") and raw.lstrip("-").isdigit():
        return int(raw)
    return raw

#: Characters that terminate a bare atom in every surface this module emits.
_ATOM_BREAK = set(" \t\n()[]{},=<>|;")


@dataclass(frozen=True)
class ExprStyle:
    notation: str
    application_style: str
    binder_encoding: str
    universe_visibility: str
    const_name_form: str
    literal_form: str
    glyph_policy: str


class ExprParseError(Exception):
    pass


# --------------------------------------------------------------------------- glyph policy

_ESCAPE_RE = re.compile(r"\\u\{([0-9A-Fa-f]{1,6})\}")


def encode_glyphs(text: str, policy: str) -> str:
    if policy == "UNICODE_NATIVE":
        return text
    if policy == "ASCII_TRANSLITERATION":
        # Bijective: the marker's own backslash is escaped, so this round-trips. It still
        # fails the glyph-fidelity gate, which is the point of keeping it in the space.
        out = []
        for character in text:
            if character == "\\":
                out.append("\\\\")
            elif ord(character) < 128:
                out.append(character)
            else:
                out.append(f"\\u{{{ord(character):04X}}}")
        return "".join(out)
    if policy == "ASCII_ESCAPE":
        # The historical defect recorded in FM-004: the escape marker is not itself escaped,
        # so a literal backslash-u sequence in the source is indistinguishable from an
        # escaped glyph. Non-injective by construction.
        return "".join(
            character if ord(character) < 128 else f"\\u{{{ord(character):04X}}}"
            for character in text
        )
    raise ValueError(policy)


def decode_glyphs(text: str, policy: str) -> str:
    if policy == "UNICODE_NATIVE":
        return text
    if policy == "ASCII_ESCAPE":
        return _ESCAPE_RE.sub(lambda match: chr(int(match.group(1), 16)), text)
    out: list[str] = []
    index = 0
    while index < len(text):
        if text[index] == "\\" and index + 1 < len(text):
            if text[index + 1] == "\\":
                out.append("\\")
                index += 2
                continue
            match = _ESCAPE_RE.match(text, index)
            if match:
                out.append(chr(int(match.group(1), 16)))
                index = match.end()
                continue
        out.append(text[index])
        index += 1
    return "".join(out)


def needs_quote(atom: str) -> bool:
    return atom == "" or any(character in _ATOM_BREAK for character in atom) or atom.startswith('"')


def quote_atom(atom: str, policy: str) -> str:
    encoded = encode_glyphs(atom, policy)
    if needs_quote(encoded):
        return '"' + encoded.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return encoded


# --------------------------------------------------------------------------------- lexer

TOKEN_RE = re.compile(r'"(?:[^"\\]|\\.)*"|[()\[\]{},=<>|;]|[^\s()\[\]{},=<>|;]+')


def lex(text: str) -> list[str]:
    return TOKEN_RE.findall(text)


class Cursor:
    def __init__(self, tokens: list[str]) -> None:
        self.tokens = tokens
        self.index = 0

    def peek(self) -> str | None:
        return self.tokens[self.index] if self.index < len(self.tokens) else None

    def next(self) -> str:
        if self.index >= len(self.tokens):
            raise ExprParseError("unexpected end of input")
        token = self.tokens[self.index]
        self.index += 1
        return token

    def expect(self, token: str) -> None:
        actual = self.next()
        if actual != token:
            raise ExprParseError(f"expected {token!r}, found {actual!r}")

    def done(self) -> bool:
        return self.index >= len(self.tokens)


def unquote(token: str, policy: str) -> str:
    if token.startswith('"') and token.endswith('"') and len(token) >= 2:
        body = token[1:-1]
        out: list[str] = []
        index = 0
        while index < len(body):
            if body[index] == "\\" and index + 1 < len(body):
                out.append(body[index + 1])
                index += 2
            else:
                out.append(body[index])
                index += 1
        return decode_glyphs("".join(out), policy)
    return decode_glyphs(token, policy)


# --------------------------------------------------------------------------------- levels


def emit_level(level: dict[str, Any], style: ExprStyle) -> str:
    constructor = level["constructor"]
    if constructor == "zero":
        return "u0"
    if constructor == "param":
        return "up" + _open(style) + quote_atom(level["name"], style.glyph_policy) + _close(style)
    if constructor == "mvar":
        return "um" + _open(style) + quote_atom(level["lmvar_id"], style.glyph_policy) + _close(style)
    if constructor == "succ":
        return "us" + _open(style) + emit_level(level["of"], style) + _close(style)
    return (
        f"u{constructor}" + _open(style)
        + emit_level(level["left"], style) + _separator(style) + emit_level(level["right"], style)
        + _close(style)
    )


def parse_level(cursor: Cursor, style: ExprStyle) -> dict[str, Any]:
    head = cursor.next()
    if head == "u0":
        return {"constructor": "zero"}
    opener, closer = _open(style).strip(), _close(style).strip()
    if opener:
        cursor.expect(opener)
    if head == "up":
        value = {"constructor": "param", "name": unquote(cursor.next(), style.glyph_policy)}
    elif head == "um":
        value = {"constructor": "mvar", "lmvar_id": unquote(cursor.next(), style.glyph_policy)}
    elif head == "us":
        value = {"constructor": "succ", "of": parse_level(cursor, style)}
    elif head in ("umax", "uimax"):
        left = parse_level(cursor, style)
        _skip_separator(cursor, style)
        right = parse_level(cursor, style)
        value = {"constructor": head[1:], "left": left, "right": right}
    else:
        raise ExprParseError(f"unknown level head {head!r}")
    if closer:
        cursor.expect(closer)
    return value


# ------------------------------------------------------------------------------ notation

def _open(style: ExprStyle) -> str:
    return {"SEXPR_PREFIX": "(", "FUNCTIONAL_APPLICATION": "(", "TAGGED_NESTED": "{",
            "POSTFIX_RPN": "("}[style.notation]


def _close(style: ExprStyle) -> str:
    return {"SEXPR_PREFIX": ")", "FUNCTIONAL_APPLICATION": ")", "TAGGED_NESTED": "}",
            "POSTFIX_RPN": ")"}[style.notation]


def _separator(style: ExprStyle) -> str:
    return "," if style.notation in ("FUNCTIONAL_APPLICATION", "TAGGED_NESTED") else " "


def _skip_separator(cursor: Cursor, style: ExprStyle) -> None:
    if _separator(style) == "," and cursor.peek() == ",":
        cursor.next()


def _head(style: ExprStyle, name: str) -> str:
    return name


def _flatten_application(expr: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    args: list[dict[str, Any]] = []
    while expr.get("node") == "application":
        args.append(expr["argument"])
        expr = expr["function"]
    return expr, list(reversed(args))


def _const_name(identity: str, style: ExprStyle) -> str:
    if style.const_name_form == "LAST_COMPONENT":
        return identity.rsplit(".", 1)[-1]
    return identity


# --------------------------------------------------------------------------------- emit


def emit_expr(expr: dict[str, Any], style: ExprStyle, depth: int = 0) -> str:
    if style.notation == "POSTFIX_RPN":
        return " ".join(_emit_rpn(expr, style, depth))
    return _emit_nested(expr, style, depth)


def _binder_token(depth: int, style: ExprStyle) -> str:
    if style.binder_encoding == "DE_BRUIJN":
        return ""
    return f"b{depth}"


def _emit_nested(expr: dict[str, Any], style: ExprStyle, depth: int) -> str:
    node = expr["node"]
    opener, closer, sep = _open(style), _close(style), _separator(style)

    def wrap(head: str, parts: list[str]) -> str:
        if style.notation == "SEXPR_PREFIX":
            return "(" + " ".join([head, *parts]) + ")"
        if style.notation == "FUNCTIONAL_APPLICATION":
            return head + "(" + ",".join(parts) + ")" if parts else head + "()"
        return "{" + head + ("|" + ",".join(parts) if parts else "") + "}"

    if node == "bound_variable":
        # An index can point past every binder in scope when a subterm is quoted out of its
        # binding context. Naming it is impossible, so the free case keeps the raw index
        # behind a distinct marker rather than clamping and silently changing the term.
        named = (
            f"b{depth - 1 - expr['index']}" if expr["index"] < depth
            else f"z{expr['index'] - depth}"
        )
        if style.binder_encoding == "NAMED":
            return wrap("bv", [named])
        if style.binder_encoding == "NAMED_PLUS_DE_BRUIJN":
            return wrap("bv", [named, str(expr["index"])])
        return wrap("bv", [str(expr["index"])])
    if node == "local_reference":
        return wrap("fv", [quote_atom(expr["identity"], style.glyph_policy)])
    if node == "metavariable_reference":
        return wrap("mv", [quote_atom(expr["identity"], style.glyph_policy)])
    if node == "sort":
        return wrap("sort", [emit_level(expr["level"], style)])
    if node == "symbol":
        parts = [quote_atom(_const_name(expr["identity"], style), style.glyph_policy)]
        universes = expr.get("universe_arguments", [])
        if style.universe_visibility == "FULL" or (
            style.universe_visibility == "ELIDED_WHEN_TRIVIAL" and universes
        ):
            parts.append("[" + " ".join(emit_level(level, style) for level in universes) + "]")
        return wrap("sym", parts)
    if node == "application":
        if style.application_style == "FLATTENED_SPINE":
            head, args = _flatten_application(expr)
            return wrap("ap", [_emit_nested(head, style, depth),
                               *[_emit_nested(arg, style, depth) for arg in args]])
        return wrap("ap", [_emit_nested(expr["function"], style, depth),
                           _emit_nested(expr["argument"], style, depth)])
    if node in ("lambda", "dependent_function"):
        head = "lam" if node == "lambda" else "pi"
        parts = []
        binder = _binder_token(depth, style)
        if binder:
            parts.append(binder)
        parts.append(expr["binder_role"])
        parts.append(_emit_nested(expr["binder_type"], style, depth))
        parts.append(_emit_nested(expr["body"], style, depth + 1))
        return wrap(head, parts)
    if node == "let":
        parts = []
        binder = _binder_token(depth, style)
        if binder:
            parts.append(binder)
        parts.append(_emit_nested(expr["type"], style, depth))
        parts.append(_emit_nested(expr["value"], style, depth))
        parts.append(_emit_nested(expr["body"], style, depth + 1))
        return wrap("let", parts)
    if node == "literal":
        if style.literal_form == "BARE":
            return wrap("lit", [quote_atom(str(expr["value"]), style.glyph_policy)])
        return wrap("lit", [expr["literal_kind"], quote_atom(str(expr["value"]), style.glyph_policy)])
    if node == "annotated":
        return wrap("ann", [_emit_nested(expr["expression"], style, depth)])
    if node == "projection":
        return wrap("proj", [quote_atom(expr["type_identity"], style.glyph_policy),
                             str(expr["field_index"]),
                             _emit_nested(expr["structure"], style, depth)])
    raise ValueError(f"unknown expression node: {node}")


def _emit_rpn(expr: dict[str, Any], style: ExprStyle, depth: int) -> list[str]:
    node = expr["node"]
    if node == "bound_variable":
        return [str(expr["index"]), "bv"]
    if node == "local_reference":
        return [quote_atom(expr["identity"], style.glyph_policy), "fv"]
    if node == "metavariable_reference":
        return [quote_atom(expr["identity"], style.glyph_policy), "mv"]
    if node == "sort":
        return [emit_level(expr["level"], style), "sort"]
    if node == "symbol":
        universes = expr.get("universe_arguments", [])
        pieces = [quote_atom(_const_name(expr["identity"], style), style.glyph_policy)]
        if style.universe_visibility == "FULL" or (
            style.universe_visibility == "ELIDED_WHEN_TRIVIAL" and universes
        ):
            pieces.append("[" + " ".join(emit_level(level, style) for level in universes) + "]")
        else:
            pieces.append("[]")
        return [*pieces, "sym"]
    if node == "application":
        if style.application_style == "FLATTENED_SPINE":
            head, args = _flatten_application(expr)
            pieces = _emit_rpn(head, style, depth)
            for arg in args:
                pieces += _emit_rpn(arg, style, depth)
            return [*pieces, str(len(args)), "apn"]
        return [*_emit_rpn(expr["function"], style, depth),
                *_emit_rpn(expr["argument"], style, depth), "ap"]
    if node in ("lambda", "dependent_function"):
        return [expr["binder_role"], *_emit_rpn(expr["binder_type"], style, depth),
                *_emit_rpn(expr["body"], style, depth + 1),
                "lam" if node == "lambda" else "pi"]
    if node == "let":
        return [*_emit_rpn(expr["type"], style, depth), *_emit_rpn(expr["value"], style, depth),
                *_emit_rpn(expr["body"], style, depth + 1), "let"]
    if node == "literal":
        if style.literal_form == "BARE":
            return [quote_atom(str(expr["value"]), style.glyph_policy), "lit"]
        return [expr["literal_kind"], quote_atom(str(expr["value"]), style.glyph_policy), "lit"]
    if node == "annotated":
        return [*_emit_rpn(expr["expression"], style, depth), "ann"]
    if node == "projection":
        return [quote_atom(expr["type_identity"], style.glyph_policy), str(expr["field_index"]),
                *_emit_rpn(expr["structure"], style, depth), "proj"]
    raise ValueError(f"unknown expression node: {node}")


# --------------------------------------------------------------------------------- parse


def parse_expr(cursor: Cursor, style: ExprStyle, depth: int = 0) -> dict[str, Any]:
    if style.notation == "POSTFIX_RPN":
        raise ExprParseError("RPN expressions are parsed by parse_expr_text")
    return _parse_nested(cursor, style, depth)


def _read_head(cursor: Cursor, style: ExprStyle) -> str:
    if style.notation == "SEXPR_PREFIX":
        cursor.expect("(")
        return cursor.next()
    if style.notation == "FUNCTIONAL_APPLICATION":
        head = cursor.next()
        cursor.expect("(")
        return head
    cursor.expect("{")
    head = cursor.next()
    if cursor.peek() == "|":
        cursor.next()
    return head


def _read_close(cursor: Cursor, style: ExprStyle) -> None:
    cursor.expect(_close(style))


def _maybe_comma(cursor: Cursor, style: ExprStyle) -> None:
    if _separator(style) == "," and cursor.peek() == ",":
        cursor.next()


def _parse_universe_list(cursor: Cursor, style: ExprStyle) -> list[dict[str, Any]]:
    cursor.expect("[")
    levels: list[dict[str, Any]] = []
    while cursor.peek() != "]":
        levels.append(parse_level(cursor, style))
    cursor.expect("]")
    return levels


def _parse_nested(cursor: Cursor, style: ExprStyle, depth: int) -> dict[str, Any]:
    head = _read_head(cursor, style)
    result: dict[str, Any]
    if head == "bv":
        first = cursor.next()
        if style.binder_encoding == "NAMED":
            index = (
                int(first[1:]) + depth if first.startswith("z")
                else depth - 1 - int(first[1:])
            )
            result = {"node": "bound_variable", "index": index}
        elif style.binder_encoding == "NAMED_PLUS_DE_BRUIJN":
            _maybe_comma(cursor, style)
            result = {"node": "bound_variable", "index": int(cursor.next())}
        else:
            result = {"node": "bound_variable", "index": int(first)}
    elif head == "fv":
        result = {"node": "local_reference", "identity": unquote(cursor.next(), style.glyph_policy)}
    elif head == "mv":
        result = {"node": "metavariable_reference",
                  "identity": unquote(cursor.next(), style.glyph_policy)}
    elif head == "sort":
        result = {"node": "sort", "level": parse_level(cursor, style)}
    elif head == "sym":
        identity = unquote(cursor.next(), style.glyph_policy)
        _maybe_comma(cursor, style)
        universes: list[dict[str, Any]] = []
        if cursor.peek() == "[":
            universes = _parse_universe_list(cursor, style)
        result = {"node": "symbol", "identity": identity, "universe_arguments": universes}
    elif head in ("ap", "apn"):
        parts = []
        while cursor.peek() != _close(style):
            parts.append(_parse_nested(cursor, style, depth))
            _maybe_comma(cursor, style)
        result = parts[0]
        for argument in parts[1:]:
            result = {"node": "application", "function": result, "argument": argument}
    elif head in ("lam", "pi"):
        if style.binder_encoding != "DE_BRUIJN":
            cursor.next()
            _maybe_comma(cursor, style)
        role = cursor.next()
        _maybe_comma(cursor, style)
        binder_type = _parse_nested(cursor, style, depth)
        _maybe_comma(cursor, style)
        body = _parse_nested(cursor, style, depth + 1)
        result = {
            "node": "lambda" if head == "lam" else "dependent_function",
            "binder_name": "_", "binder_role": role,
            "binder_type": binder_type, "body": body,
        }
    elif head == "let":
        if style.binder_encoding != "DE_BRUIJN":
            cursor.next()
            _maybe_comma(cursor, style)
        type_expr = _parse_nested(cursor, style, depth)
        _maybe_comma(cursor, style)
        value = _parse_nested(cursor, style, depth)
        _maybe_comma(cursor, style)
        body = _parse_nested(cursor, style, depth + 1)
        result = {"node": "let", "binder_name": "_", "type": type_expr,
                  "value": value, "body": body}
    elif head == "lit":
        if style.literal_form == "BARE":
            raw = unquote(cursor.next(), style.glyph_policy)
            kind = NATURAL_LITERAL if raw.isdigit() else STRING_LITERAL
        else:
            kind = cursor.next()
            _maybe_comma(cursor, style)
            raw = unquote(cursor.next(), style.glyph_policy)
        result = {"node": "literal", "literal_kind": kind, "value": _literal_value(kind, raw)}
    elif head == "ann":
        result = {"node": "annotated", "expression": _parse_nested(cursor, style, depth),
                  "source_metadata_delegated": True}
    elif head == "proj":
        type_identity = unquote(cursor.next(), style.glyph_policy)
        _maybe_comma(cursor, style)
        field_index = int(cursor.next())
        _maybe_comma(cursor, style)
        structure = _parse_nested(cursor, style, depth)
        result = {"node": "projection", "type_identity": type_identity,
                  "field_index": field_index, "structure": structure}
    else:
        raise ExprParseError(f"unknown expression head {head!r}")
    _maybe_comma(cursor, style)
    _read_close(cursor, style)
    return result


def _parse_rpn(cursor: Cursor, style: ExprStyle) -> dict[str, Any]:
    stack: list[Any] = []
    while not cursor.done():
        token = cursor.next()
        if token == "bv":
            stack.append({"node": "bound_variable", "index": int(stack.pop())})
        elif token == "fv":
            stack.append({"node": "local_reference",
                          "identity": unquote(str(stack.pop()), style.glyph_policy)})
        elif token == "mv":
            stack.append({"node": "metavariable_reference",
                          "identity": unquote(str(stack.pop()), style.glyph_policy)})
        elif token == "sort":
            stack.append({"node": "sort", "level": stack.pop()})
        elif token == "sym":
            universes = stack.pop()
            identity = unquote(str(stack.pop()), style.glyph_policy)
            stack.append({"node": "symbol", "identity": identity,
                          "universe_arguments": universes if isinstance(universes, list) else []})
        elif token == "ap":
            argument = stack.pop()
            function = stack.pop()
            stack.append({"node": "application", "function": function, "argument": argument})
        elif token == "apn":
            count = int(stack.pop())
            args = [stack.pop() for _ in range(count)][::-1]
            result = stack.pop()
            for argument in args:
                result = {"node": "application", "function": result, "argument": argument}
            stack.append(result)
        elif token in ("lam", "pi"):
            body = stack.pop()
            binder_type = stack.pop()
            role = str(stack.pop())
            stack.append({"node": "lambda" if token == "lam" else "dependent_function",
                          "binder_name": "_", "binder_role": role,
                          "binder_type": binder_type, "body": body})
        elif token == "let":
            body, value, type_expr = stack.pop(), stack.pop(), stack.pop()
            stack.append({"node": "let", "binder_name": "_", "type": type_expr,
                          "value": value, "body": body})
        elif token == "lit":
            raw = unquote(str(stack.pop()), style.glyph_policy)
            if style.literal_form == "BARE":
                kind = NATURAL_LITERAL if raw.isdigit() else STRING_LITERAL
            else:
                kind = str(stack.pop())
            stack.append({"node": "literal", "literal_kind": kind,
                          "value": _literal_value(kind, raw)})
        elif token == "ann":
            stack.append({"node": "annotated", "expression": stack.pop(),
                          "source_metadata_delegated": True})
        elif token == "proj":
            structure = stack.pop()
            field_index = int(stack.pop())
            type_identity = unquote(str(stack.pop()), style.glyph_policy)
            stack.append({"node": "projection", "type_identity": type_identity,
                          "field_index": field_index, "structure": structure})
        elif token == "[":
            levels = []
            while cursor.peek() != "]":
                levels.append(parse_level(cursor, style))
            cursor.expect("]")
            stack.append(levels)
        elif token in ("u0", "up", "um", "us", "umax", "uimax"):
            cursor.index -= 1
            stack.append(parse_level(cursor, style))
        else:
            stack.append(token)
    if len(stack) != 1:
        raise ExprParseError(f"RPN stack did not reduce to one expression: {len(stack)}")
    return stack[0]


def parse_expr_text(text: str, style: ExprStyle) -> dict[str, Any]:
    cursor = Cursor(lex(text))
    if style.notation == "POSTFIX_RPN":
        return _parse_rpn(cursor, style)
    return _parse_nested(cursor, style, 0)
