"""The generic representation compiler.

    RepresentationGenome  ->  RepresentationCompiler  ->  render / parse

There is exactly one compiler. A candidate is not a hand-written renderer; it is this
compiler configured by a genome. Two candidates therefore cannot differ by an implementation
accident, and any candidate is reproducible from ``(genome_sha256, compiler_version,
canonical_state_version)``.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from typing import Any

from hml_v3.representation_search.document import (
    Document,
    DocumentParseError,
    Lexicon,
    Record,
    Section,
    SurfaceStyle,
    emit_document,
    parse_document,
)
from hml_v3.representation_search.expressions import ExprStyle
from hml_v3.representation_search.genome import RepresentationGenome
from hml_v3.representation_search.projection import (
    IdentityCodec,
    Projection,
    map_expression_identities,
    semantic_core,
)

COMPILER_VERSION = "representation-compiler-v1.0.0"
CANONICAL_STATE_VERSION = "canonical-math-transition-v2.0.0"

ALIAS_PREFIX = "$a"


class CompilerRejection(Exception):
    """The genome does not describe a well-formed language."""


@dataclass
class RenderResult:
    text: str
    document: Document
    codec: IdentityCodec
    aliases: dict[str, Any]


class RepresentationCompiler:
    def __init__(self, genome: RepresentationGenome) -> None:
        self.genome = genome
        self.projection = Projection(genome)
        lexicon = Lexicon(
            genome.get("lexicon_register"),
            genome.get("role_word_length"),
            genome.get("keyword_case"),
        )
        if not lexicon.injective:
            raise CompilerRejection(
                "AMBIGUOUS_LEXICON: two distinct semantic roles share one surface word"
            )
        self.surface = SurfaceStyle(
            syntax_family=genome.get("syntax_family"),
            block_delimiter=genome.get("block_delimiter"),
            field_marker=genome.get("field_marker"),
            record_separator=genome.get("record_separator"),
            list_syntax=genome.get("list_syntax"),
            type_attachment=genome.get("type_attachment"),
            identity_sigil=genome.get("identity_sigil"),
            glyph_policy=genome.get("glyph_policy"),
            expr=ExprStyle(
                notation=genome.get("expression_notation"),
                application_style=genome.get("application_style"),
                binder_encoding=genome.get("binder_encoding"),
                universe_visibility=genome.get("universe_visibility"),
                const_name_form=genome.get("const_name_form"),
                literal_form=genome.get("literal_form"),
                glyph_policy=genome.get("glyph_policy"),
            ),
            lexicon=lexicon,
        )

    # ------------------------------------------------------------------------- identity
    @property
    def candidate_id(self) -> str:
        return self.genome.candidate_id()

    def fingerprint(self) -> str:
        payload = "|".join([
            self.genome.sha256(), COMPILER_VERSION, CANONICAL_STATE_VERSION,
        ])
        return hashlib.sha256(payload.encode()).hexdigest()

    # --------------------------------------------------------------------------- render
    def render(self, transition: dict[str, Any]) -> RenderResult:
        document, codec = self.projection.to_document(transition)
        document = map_expression_identities(document, codec.encode)
        aliases: dict[str, Any] = {}
        if self.genome.get("shared_subterm_handling") == "HOISTED_DAG_LETS":
            document, aliases = _hoist_shared_subterms(document)
        text = emit_document(document, self.surface)
        return RenderResult(text, document, codec, aliases)

    def render_text(self, transition: dict[str, Any]) -> str:
        return self.render(transition).text

    # ---------------------------------------------------------------------------- parse
    def parse_core(self, text: str, codec: IdentityCodec) -> dict[str, Any]:
        document = parse_document(text, self.surface)
        if self.genome.get("shared_subterm_handling") == "HOISTED_DAG_LETS":
            document = _resolve_aliases(document)
        document = map_expression_identities(document, codec.decode)
        return self.projection.core_from_document(document, codec)

    # ----------------------------------------------------------------------- round trip
    def round_trip(self, transition: dict[str, Any]) -> tuple[bool, str, dict[str, Any]]:
        """Returns ``(passed, reason, detail)`` for one transition."""

        try:
            rendered = self.render(transition)
        except Exception as error:  # noqa: BLE001 - a render failure is a candidate defect
            return False, f"RENDER_ERROR:{type(error).__name__}", {"message": str(error)}
        if rendered.codec.collisions:
            return False, "IDENTITY_COLLISION", {"collisions": rendered.codec.collisions}
        try:
            recovered = self.parse_core(rendered.text, rendered.codec)
        except (DocumentParseError, Exception) as error:  # noqa: BLE001
            return False, f"PARSE_ERROR:{type(error).__name__}", {"message": str(error)[:200]}
        expected = semantic_core(transition)
        if recovered == expected:
            return True, "OK", {}
        return False, "SEMANTIC_MISMATCH", _first_difference(expected, recovered)


# ---------------------------------------------------------------------- shared subterms


def _expression_fields(record: Record) -> list[int]:
    from hml_v3.representation_search.document import EXPR, FIELD_TYPES

    return [
        index for index, (name, _) in enumerate(record.fields)
        if FIELD_TYPES.get(name) == EXPR
    ]


def _subtree_key(node: Any) -> str:
    import json

    return json.dumps(node, sort_keys=True, separators=(",", ":"))


def _walk_subtrees(node: Any, sizes: dict[str, int], counts: dict[str, int]) -> int:
    if not isinstance(node, dict) or "node" not in node:
        return 0
    size = 1
    for value in node.values():
        if isinstance(value, dict):
            size += _walk_subtrees(value, sizes, counts)
        elif isinstance(value, list):
            for item in value:
                size += _walk_subtrees(item, sizes, counts)
    key = _subtree_key(node)
    sizes[key] = size
    counts[key] = counts.get(key, 0) + 1
    return size


def _substitute(node: Any, table: dict[str, str]) -> Any:
    if isinstance(node, dict) and "node" in node:
        key = _subtree_key(node)
        if key in table:
            return {"node": "local_reference", "identity": table[key]}
        return {
            field: _substitute(value, table) if isinstance(value, (dict, list)) else value
            for field, value in node.items()
        }
    if isinstance(node, list):
        return [_substitute(item, table) for item in node]
    return node


def _hoist_shared_subterms(document: Document) -> tuple[Document, dict[str, Any]]:
    sizes: dict[str, int] = {}
    counts: dict[str, int] = {}
    for section in document.sections:
        for record in section.records:
            for index in _expression_fields(record):
                _walk_subtrees(record.fields[index][1], sizes, counts)
    shared = sorted(
        (key for key, count in counts.items() if count >= 2 and sizes[key] >= 4),
        key=lambda key: (-sizes[key], key),
    )
    table: dict[str, str] = {}
    aliases: dict[str, Any] = {}
    import json

    for ordinal, key in enumerate(shared):
        # A hoisted subterm must not itself contain another hoisted subterm's alias, so only
        # maximal subtrees are taken: skip anything already covered by an earlier alias.
        if any(previous in key for previous in table):
            continue
        name = f"{ALIAS_PREFIX}{ordinal}"
        table[key] = name
        aliases[name] = json.loads(key)
    if not table:
        return document, {}
    sections = []
    alias_records = [
        Record("alias", name, [("term", aliases[name])])
        for name in sorted(aliases, key=lambda name: int(name[len(ALIAS_PREFIX):]))
    ]
    for section in document.sections:
        records = []
        for record in section.records:
            fields = list(record.fields)
            for index in _expression_fields(record):
                name, value = fields[index]
                fields[index] = (name, _substitute(value, table))
            records.append(Record(record.kind, record.identity, fields))
        sections.append(Section(section.kind, records))
    return Document([Section("aliases", alias_records), *sections]), aliases


def _expand(node: Any, table: dict[str, Any]) -> Any:
    if isinstance(node, dict):
        if node.get("node") == "local_reference" and node.get("identity", "").startswith(ALIAS_PREFIX):
            return _expand(table[node["identity"]], table)
        return {
            field: _expand(value, table) if isinstance(value, (dict, list)) else value
            for field, value in node.items()
        }
    if isinstance(node, list):
        return [_expand(item, table) for item in node]
    return node


def _resolve_aliases(document: Document) -> Document:
    table: dict[str, Any] = {}
    for section in document.sections:
        if section.kind != "aliases":
            continue
        for record in section.records:
            values = dict(record.fields)
            if record.identity is not None and "term" in values:
                table[record.identity] = values["term"]
    if not table:
        return Document([s for s in document.sections if s.kind != "aliases"])
    sections = []
    for section in document.sections:
        if section.kind == "aliases":
            continue
        records = []
        for record in section.records:
            fields = [
                (name, _expand(value, table) if isinstance(value, (dict, list)) else value)
                for name, value in record.fields
            ]
            records.append(Record(record.kind, record.identity, fields))
        sections.append(Section(section.kind, records))
    return Document(sections)


# --------------------------------------------------------------------------- diagnostics


def _first_difference(expected: Any, actual: Any, path: str = "") -> dict[str, Any]:
    if type(expected) is not type(actual):
        return {"path": path or "/", "expected_type": type(expected).__name__,
                "actual_type": type(actual).__name__}
    if isinstance(expected, dict):
        for key in expected:
            if key not in actual:
                return {"path": f"{path}/{key}", "missing": True}
            if expected[key] != actual[key]:
                return _first_difference(expected[key], actual[key], f"{path}/{key}")
        for key in actual:
            if key not in expected:
                return {"path": f"{path}/{key}", "unexpected": True}
        return {"path": path or "/", "note": "dicts compare equal"}
    if isinstance(expected, list):
        if len(expected) != len(actual):
            return {"path": path, "expected_length": len(expected), "actual_length": len(actual)}
        for index, (left, right) in enumerate(zip(expected, actual)):
            if left != right:
                return _first_difference(left, right, f"{path}[{index}]")
        return {"path": path, "note": "lists compare equal"}
    return {"path": path or "/", "expected": str(expected)[:120], "actual": str(actual)[:120]}


def build(genome: RepresentationGenome) -> RepresentationCompiler:
    return RepresentationCompiler(genome)
