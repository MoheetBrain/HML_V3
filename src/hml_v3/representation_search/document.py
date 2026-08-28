"""A representation-neutral document model and its genome-driven surface codec.

Every candidate language in this search is the same pipeline:

    canonical transition  ->  Document  ->  text
                          <-            <-

``Document`` is an ordered list of sections of records of typed fields. The projection layer
(``projection.py``) decides *what* is in the document; this module decides *how it is
written*, driven only by the grammar and lexicon axes. One generic emitter and one generic
parser cover every syntax family, so no candidate needs bespoke renderer code and no two
candidates can differ by an implementation accident.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Any

from hml_v3.representation_search.expressions import (
    Cursor,
    ExprParseError,
    ExprStyle,
    emit_expr,
    encode_glyphs,
    decode_glyphs,
    lex,
    parse_expr_text,
    quote_atom,
    unquote,
)


class DocumentParseError(Exception):
    pass


@dataclass
class Record:
    kind: str
    identity: str | None
    fields: list[tuple[str, Any]] = field(default_factory=list)


@dataclass
class Section:
    kind: str
    records: list[Record] = field(default_factory=list)


@dataclass
class Document:
    sections: list[Section] = field(default_factory=list)


# ------------------------------------------------------------------------------- schema
# The declared type of every field the projection can emit. The parser needs it because the
# surface is deliberately allowed to be ambiguous between an atom and a list otherwise.

ATOM, EXPR, LIST, INT, REFLIST = "atom", "expr", "list", "int", "reflist"

FIELD_TYPES: dict[str, str] = {
    "target": EXPR,
    "type": EXPR,
    "value": EXPR,
    "assignment": EXPR,
    "binder_role": ATOM,
    "declaration_role": ATOM,
    "display": ATOM,
    "scope": ATOM,
    "kind": ATOM,
    "assigned": ATOM,
    "class": ATOM,
    "term": EXPR,
    "context": REFLIST,
    "focus_order": REFLIST,
    "premises": LIST,
    "local_refs": REFLIST,
    "source": ATOM,
    "elaborator": ATOM,
    "goals_created": REFLIST,
    "goals_solved": REFLIST,
    "goals_modified": REFLIST,
    "goals_preserved": REFLIST,
    "locals_added": REFLIST,
    "locals_removed": REFLIST,
    "locals_changed": REFLIST,
    "mvars_created": REFLIST,
    "mvars_assigned": REFLIST,
    "focus_before": ATOM,
    "focus_after": ATOM,
    "reordered": ATOM,
    "theorem": ATOM,
    "file": ATOM,
    "digest": ATOM,
    "count": INT,
    "edge": ATOM,
    "from": ATOM,
    "to": ATOM,
    "relation": ATOM,
    "index": INT,
    "reminder": EXPR,
    "tag": ATOM,
}


# ------------------------------------------------------------------------------ lexicon

CANONICAL_WORDS = (
    "state_before", "state_after", "action", "delta", "meta", "edges", "aliases",
    "goal", "decl", "mvar", "instance", "edge", "alias", "step", "summary",
    "target", "type", "value", "assignment", "binder_role", "declaration_role", "display",
    "scope", "kind", "assigned", "class", "term", "context", "focus_order", "premises",
    "local_refs", "source", "elaborator", "goals_created", "goals_solved", "goals_modified",
    "goals_preserved", "locals_added", "locals_removed", "locals_changed", "mvars_created",
    "mvars_assigned", "focus_before", "focus_after", "reordered", "theorem", "file",
    "digest", "count", "from", "to", "relation", "index", "reminder", "tag",
)

_COMPACT = {
    "state_before": "sb", "state_after": "sa", "action": "act", "delta": "dlt",
    "meta": "mta", "edges": "edg", "aliases": "als", "goal": "gl", "decl": "dc",
    "mvar": "mv", "instance": "ins", "edge": "eg", "alias": "al", "step": "stp",
    "summary": "smy", "target": "tgt", "type": "ty", "value": "val",
    "assignment": "asg", "binder_role": "br", "declaration_role": "dr", "display": "dsp",
    "scope": "scp", "kind": "knd", "assigned": "asd", "class": "cls", "term": "trm",
    "context": "ctx", "focus_order": "fo", "premises": "prm", "local_refs": "lr",
    "source": "src", "elaborator": "elb", "goals_created": "gc", "goals_solved": "gs",
    "goals_modified": "gm", "goals_preserved": "gp", "locals_added": "la",
    "locals_removed": "lrm", "locals_changed": "lc", "mvars_created": "mc",
    "mvars_assigned": "ma", "focus_before": "fb", "focus_after": "fa",
    "reordered": "ro", "theorem": "thm", "file": "fl", "digest": "dg", "count": "cnt",
    "from": "frm", "to": "to", "relation": "rel", "index": "ix", "reminder": "rmd",
    "tag": "tg",
}

_SYMBOLIC = {
    "state_before": "S0", "state_after": "S1", "action": "@", "delta": "%", "meta": "#",
    "edges": "&", "aliases": "$", "goal": "G", "decl": "D", "mvar": "M", "instance": "I",
    "edge": "E", "alias": "A", "step": "T", "summary": "Y", "target": "|-", "type": ":",
    "value": ":=", "assignment": "<-", "binder_role": "b", "declaration_role": "d",
    "display": "n", "scope": "s", "kind": "k", "assigned": "a", "class": "c", "term": "t",
    "context": "C", "focus_order": "F", "premises": "P", "local_refs": "L", "source": "R",
    "elaborator": "e", "goals_created": "G+", "goals_solved": "G-", "goals_modified": "G~",
    "goals_preserved": "G=", "locals_added": "L+", "locals_removed": "L-",
    "locals_changed": "L~", "mvars_created": "M+", "mvars_assigned": "M<",
    "focus_before": "F0", "focus_after": "F1", "reordered": "RO", "theorem": "TH",
    "file": "FL", "digest": "DG", "count": "N", "from": "f", "to": "o", "relation": "r",
    "index": "i", "reminder": "rm", "tag": "tg",
}

_MATH = dict(_SYMBOLIC)
_MATH.update({
    "target": "⊢", "type": "∈", "value": "≔", "assignment": "≡", "context": "Γ",
    "action": "→", "delta": "Δ", "goal": "□", "premises": "⊨", "state_before": "Σ₀",
    "state_after": "Σ₁", "focus_order": "◆", "mvar": "?",
})

_ABBREV_LENGTH = 4


class Lexicon:
    """Maps canonical role keys to surface words and back."""

    def __init__(self, register: str, length: str, case: str) -> None:
        self.register, self.length, self.case = register, length, case
        self.forward: dict[str, str] = {}
        for key in CANONICAL_WORDS:
            self.forward[key] = self._surface(key)
        self.backward: dict[str, str] = {}
        self.injective = True
        for key, word in self.forward.items():
            if word in self.backward:
                self.injective = False
            self.backward[word] = key
        # Longest first so that a short role word can never shadow a longer one that starts
        # with the same characters (``G`` against ``G+`` in the symbolic register).
        self.sorted_words = sorted(self.backward, key=lambda word: (-len(word), word))

    def _surface(self, key: str) -> str:
        if self.register == "COMPACT_MNEMONIC":
            word = _COMPACT[key]
        elif self.register == "SYMBOLIC_ROLE":
            word = _SYMBOLIC[key]
        elif self.register == "MATH_NOTATION":
            word = _MATH[key]
        else:
            word = key
        if self.register in ("HUMAN_WORDS", "COMPACT_MNEMONIC"):
            if self.length == "ABBREVIATED":
                word = "".join(part[:2] for part in word.split("_"))[:_ABBREV_LENGTH]
            elif self.length == "SINGLE_CHAR":
                word = "".join(part[0] for part in word.split("_"))
            if self.case == "UPPER":
                word = word.upper()
        return word

    def word(self, key: str) -> str:
        return self.forward[key]

    def key(self, word: str) -> str:
        try:
            return self.backward[word]
        except KeyError as error:
            raise DocumentParseError(f"unknown role word {word!r}") from error


# --------------------------------------------------------------------------- surface style


@dataclass(frozen=True)
class SurfaceStyle:
    syntax_family: str
    block_delimiter: str
    field_marker: str
    record_separator: str
    list_syntax: str
    type_attachment: str
    identity_sigil: str
    glyph_policy: str
    expr: ExprStyle
    lexicon: Lexicon

    def marker(self) -> str:
        return {"COLON": ":", "EQUALS": "=", "ARROW": "->"}[self.field_marker]

    def sigil(self, identity: str) -> str:
        if self.identity_sigil == "PREFIX_SIGIL":
            return "$" + identity
        if self.identity_sigil == "BRACKETED":
            return "[" + identity + "]"
        return identity

    def unsigil(self, token: str) -> str:
        if self.identity_sigil == "PREFIX_SIGIL" and token.startswith("$"):
            return token[1:]
        if self.identity_sigil == "BRACKETED" and token.startswith("[") and token.endswith("]"):
            return token[1:-1]
        return token


# ---------------------------------------------------------------------------- value codec


def emit_value(name: str, value: Any, style: SurfaceStyle) -> str:
    kind = FIELD_TYPES.get(name, ATOM)
    if kind == EXPR:
        return emit_expr(value, style.expr)
    if kind == INT:
        return str(value)
    if kind in (LIST, REFLIST):
        items = [
            style.sigil(item) if kind == REFLIST else quote_atom(item, style.glyph_policy)
            for item in value
        ]
        if style.list_syntax == "BRACKET_COMMA":
            return "[" + ",".join(items) + "]"
        if style.list_syntax == "PAREN":
            return "(" + " ".join(items) + ")"
        return "{" + " ".join(items) + "}"
    return quote_atom(str(value), style.glyph_policy)


def parse_value(name: str, text: str, style: SurfaceStyle) -> Any:
    kind = FIELD_TYPES.get(name, ATOM)
    text = text.strip()
    if kind == EXPR:
        return parse_expr_text(text, style.expr)
    if kind == INT:
        return int(text)
    if kind in (LIST, REFLIST):
        if style.list_syntax == "BRACKET_COMMA":
            body = text[1:-1]
            raw = [piece for piece in _split_top(body, ",") if piece.strip()]
        else:
            body = text[1:-1]
            raw = _lex_atoms(body)
        if kind == REFLIST:
            return [style.unsigil(piece.strip()) for piece in raw]
        return [unquote(piece.strip(), style.glyph_policy) for piece in raw]
    return unquote(text, style.glyph_policy)


def split_field(text: str, style: "SurfaceStyle") -> tuple[str, str]:
    """Split ``role<marker> value`` without assuming the role word is marker-free.

    The symbolic and mathematical registers spell roles as punctuation (``:``, ``:=``,
    ``<-``), so partitioning on the field marker mis-parses them. Matching the longest known
    role word first is exact for every register and is what makes the lexicon axis safe to
    search over.
    """

    body = text.strip()
    marker = style.marker()
    for word in style.lexicon.sorted_words:
        if not body.startswith(word):
            continue
        rest = body[len(word):]
        if rest.startswith(marker):
            return style.lexicon.key(word), rest[len(marker):]
        stripped = rest.lstrip()
        if stripped.startswith(marker):
            return style.lexicon.key(word), stripped[len(marker):]
    raise DocumentParseError(f"no role word with a field marker in {text!r}")


def split_top_delimited(text: str, separator: str) -> list[str]:
    """Split on a multi-character separator at bracket depth zero, outside strings."""

    parts, depth, current, in_string = [], 0, [], False
    index = 0
    while index < len(text):
        character = text[index]
        if in_string:
            current.append(character)
            if character == "\\" and index + 1 < len(text):
                current.append(text[index + 1])
                index += 2
                continue
            if character == '"':
                in_string = False
            index += 1
            continue
        if character == '"':
            in_string = True
            current.append(character)
            index += 1
            continue
        if character in "([{":
            depth += 1
        elif character in ")]}":
            depth -= 1
        if depth == 0 and text.startswith(separator, index):
            parts.append("".join(current))
            current = []
            index += len(separator)
            continue
        current.append(character)
        index += 1
    parts.append("".join(current))
    return parts


def _split_top(text: str, separator: str) -> list[str]:
    parts, depth, current, in_string = [], 0, [], False
    index = 0
    while index < len(text):
        character = text[index]
        if in_string:
            current.append(character)
            if character == "\\" and index + 1 < len(text):
                current.append(text[index + 1])
                index += 2
                continue
            if character == '"':
                in_string = False
            index += 1
            continue
        if character == '"':
            in_string = True
            current.append(character)
        elif character in "([{":
            depth += 1
            current.append(character)
        elif character in ")]}":
            depth -= 1
            current.append(character)
        elif character == separator and depth == 0:
            parts.append("".join(current))
            current = []
        else:
            current.append(character)
        index += 1
    parts.append("".join(current))
    return parts


def _lex_atoms(text: str) -> list[str]:
    return [token for token in lex(text) if token not in {"[", "]", "(", ")", "{", "}", ","}]


# ------------------------------------------------------------------------------- emitters


def _record_head(record: Record, style: SurfaceStyle) -> str:
    head = style.lexicon.word(record.kind)
    if record.identity is not None:
        return f"{head} {style.sigil(record.identity)}"
    return head


def _fields_inline(record: Record, style: SurfaceStyle, joiner: str) -> str:
    marker = style.marker()
    parts = []
    for name, value in record.fields:
        parts.append(f"{style.lexicon.word(name)}{marker} {emit_value(name, value, style)}")
    return joiner.join(parts)


def emit_document(document: Document, style: SurfaceStyle) -> str:
    family = style.syntax_family
    lines: list[str] = []
    blank = style.record_separator == "NEWLINE_BLANK"
    for section in document.sections:
        section_word = style.lexicon.word(section.kind)
        if family == "JSONISH":
            lines.append(f'"{section_word}": [')
        elif family == "SEXPR":
            lines.append(f"({section_word}")
        elif family == "PROSE":
            lines.append(f"In {section_word}:")
        elif style.block_delimiter == "BRACE":
            lines.append(section_word + " {")
        else:
            lines.append(section_word)
        for record in section.records:
            lines.extend(_emit_record(record, style, family))
            if blank:
                lines.append("")
        if family == "JSONISH":
            lines.append("]")
        elif family == "SEXPR":
            lines.append(")")
        elif family in ("BLOCK", "INDENTED_TREE") and style.block_delimiter == "BRACE":
            lines.append("}")
        elif family in ("BLOCK", "INDENTED_TREE") and style.block_delimiter == "KEYWORD_END":
            lines.append("end " + section_word)
    return "\n".join(line for line in lines if line is not None)


def _emit_record(record: Record, style: SurfaceStyle, family: str) -> list[str]:
    marker = style.marker()
    head = _record_head(record, style)
    if family == "TAGGED_LINE":
        body = _fields_inline(record, style, " ;; ")
        return [f"  {head}" + (" ;; " + body if body else "")]
    if family == "SEXPR":
        parts = " ".join(
            f"({style.lexicon.word(name)} {emit_value(name, value, style)})"
            for name, value in record.fields
        )
        return [f"  ({head}" + (" " + parts if parts else "") + ")"]
    if family == "JSONISH":
        parts = ", ".join(
            f'"{style.lexicon.word(name)}": {emit_value(name, value, style)}'
            for name, value in record.fields
        )
        return ['  {"' + style.lexicon.word(record.kind) + '": '
                + (f'"{style.sigil(record.identity)}"' if record.identity is not None else "null")
                + (", " + parts if parts else "") + "}"]
    if family == "PROSE":
        clauses = [
            f"{style.lexicon.word(name)} is {emit_value(name, value, style)}"
            for name, value in record.fields
        ]
        sentence = f"  {head}" + (" has " + "; and ".join(clauses) if clauses else " has nothing")
        return [sentence + " ."]
    # BLOCK / INDENTED_TREE
    bullet = "- " if family == "INDENTED_TREE" else ""
    opener = " {" if style.block_delimiter == "BRACE" else ""
    lines = [f"  {bullet}{head}{opener}"]
    for name, value in record.fields:
        lines.append(f"    {style.lexicon.word(name)}{marker} {emit_value(name, value, style)}")
    if style.block_delimiter == "BRACE":
        lines.append("  }")
    elif style.block_delimiter == "KEYWORD_END":
        lines.append("  end")
    return lines


# -------------------------------------------------------------------------------- parsers


def parse_document(text: str, style: SurfaceStyle) -> Document:
    family = style.syntax_family
    document = Document()
    section: Section | None = None
    record: Record | None = None
    marker = style.marker()
    for raw_line in text.split("\n"):
        line = raw_line.rstrip()
        if not line.strip():
            continue
        stripped = line.strip()
        indent = len(line) - len(line.lstrip())
        if indent == 0:
            if stripped in ("]", ")", "}"):
                section = None
                continue
            if stripped.startswith("end "):
                section = None
                continue
            head = stripped
            for suffix in (" {", ":", " ["):
                if head.endswith(suffix):
                    head = head[: -len(suffix)]
            head = head.strip().lstrip("(").strip()
            if head.startswith('"') and head.endswith('":'):
                head = head[1:-2]
            head = head.rstrip(":").strip()
            if family == "PROSE" and head.startswith("In "):
                head = head[3:].rstrip(":")
            if family == "JSONISH":
                head = head.strip('"').rstrip(":").strip().rstrip("[").strip().strip('"')
            section = Section(style.lexicon.key(head))
            document.sections.append(section)
            record = None
            continue
        if section is None:
            raise DocumentParseError(f"record outside a section: {stripped!r}")
        if stripped in ("}", "end"):
            record = None
            continue
        if family == "TAGGED_LINE":
            document.sections[-1].records.append(_parse_tagged_line(stripped, style, marker))
        elif family == "SEXPR":
            document.sections[-1].records.append(_parse_sexpr_record(stripped, style))
        elif family == "JSONISH":
            document.sections[-1].records.append(_parse_jsonish_record(stripped, style))
        elif family == "PROSE":
            document.sections[-1].records.append(_parse_prose_record(stripped, style))
        else:
            if indent <= 2 or record is None:
                record = _parse_block_head(stripped, style)
                section.records.append(record)
            else:
                key, value = split_field(stripped, style)
                record.fields.append((key, parse_value(key, value, style)))
    return document


def _head_parts(head: str, style: SurfaceStyle) -> tuple[str, str | None]:
    pieces = head.split(None, 1)
    kind = style.lexicon.key(pieces[0])
    identity = style.unsigil(pieces[1].strip()) if len(pieces) > 1 else None
    return kind, identity


def _parse_block_head(line: str, style: SurfaceStyle) -> Record:
    head = line
    if head.startswith("- "):
        head = head[2:]
    if head.endswith(" {"):
        head = head[:-2]
    kind, identity = _head_parts(head.strip(), style)
    return Record(kind, identity)


def _parse_tagged_line(line: str, style: SurfaceStyle, marker: str) -> Record:
    pieces = split_top_delimited(line, ";;")
    kind, identity = _head_parts(pieces[0].strip(), style)
    record = Record(kind, identity)
    for piece in pieces[1:]:
        key, value = split_field(piece, style)
        record.fields.append((key, parse_value(key, value, style)))
    return record


def _parse_sexpr_record(line: str, style: SurfaceStyle) -> Record:
    body = line.strip()
    if not (body.startswith("(") and body.endswith(")")):
        raise DocumentParseError(f"malformed record {line!r}")
    body = body[1:-1]
    depth, split_at = 0, len(body)
    for index, character in enumerate(body):
        if character == "(" and depth == 0:
            split_at = index
            break
    head = body[:split_at].strip()
    kind, identity = _head_parts(head, style)
    record = Record(kind, identity)
    rest = body[split_at:]
    for group in _top_groups(rest):
        inner = group[1:-1]
        name, _, value = inner.partition(" ")
        key = style.lexicon.key(name.strip())
        record.fields.append((key, parse_value(key, value, style)))
    return record


def _top_groups(text: str) -> list[str]:
    groups, depth, start, in_string = [], 0, None, False
    index = 0
    while index < len(text):
        character = text[index]
        if in_string:
            if character == "\\":
                index += 2
                continue
            if character == '"':
                in_string = False
            index += 1
            continue
        if character == '"':
            in_string = True
        elif character == "(":
            if depth == 0:
                start = index
            depth += 1
        elif character == ")":
            depth -= 1
            if depth == 0 and start is not None:
                groups.append(text[start: index + 1])
                start = None
        index += 1
    return groups


def _parse_jsonish_record(line: str, style: SurfaceStyle) -> Record:
    body = line.strip()
    if body.endswith(","):
        body = body[:-1]
    body = body[1:-1]
    pieces = _split_top(body, ",")
    name, value = _json_pair(pieces[0])
    kind = style.lexicon.key(name)
    identity = None if value == "null" else style.unsigil(value.strip('"'))
    record = Record(kind, identity)
    for piece in pieces[1:]:
        name, value = _json_pair(piece)
        key = style.lexicon.key(name)
        record.fields.append((key, parse_value(key, value, style)))
    return record


_JSON_PAIR = re.compile(r'^\s*"((?:[^"\\]|\\.)*)"\s*:\s*(.*)$', re.DOTALL)


def _json_pair(piece: str) -> tuple[str, str]:
    match = _JSON_PAIR.match(piece)
    if not match:
        raise DocumentParseError(f"malformed JSON-ish field {piece!r}")
    return match.group(1), match.group(2).strip()


def _parse_prose_record(line: str, style: SurfaceStyle) -> Record:
    body = line.strip()
    if body.endswith(" ."):
        body = body[:-2]
    head, _, rest = body.partition(" has ")
    kind, identity = _head_parts(head.strip(), style)
    record = Record(kind, identity)
    if rest.strip() in ("", "nothing"):
        return record
    for clause in split_top_delimited(rest, "; and "):
        clause = clause.strip()
        name, _, value = clause.partition(" is ")
        key = style.lexicon.key(name.strip())
        record.fields.append((key, parse_value(key, value, style)))
    return record
