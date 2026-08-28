"""Conservative parsing of Lean's pretty-printed tactic-state observations.

This module decomposes context and goal boundaries only. It deliberately does not
claim to parse or elaborate Lean expressions.
"""

from __future__ import annotations

from dataclasses import dataclass
import re


_DECLARATION = re.compile(
    r"^(?P<names>[^\s:(){}\[\],→←↔⊢=<>|]+(?:[ \t]+[^\s:(){}\[\],→←↔⊢=<>|]+)*)"
    r"[ \t]*:[ \t]?(?P<body>.*)$"
)
_METAVARIABLE = re.compile(r"\?(?:[A-Za-z_][A-Za-z0-9_'.]*|[um]\.\d+)")


@dataclass(frozen=True)
class ParsedDeclaration:
    names: tuple[str, ...]
    type_text: str
    value_text: str | None = None


@dataclass(frozen=True)
class ParsedGoal:
    case_label: str | None
    declarations: tuple[ParsedDeclaration, ...]
    target: str


@dataclass(frozen=True)
class ParsedLeanState:
    goals: tuple[ParsedGoal, ...]
    no_goals: bool
    unparsed_lines: tuple[str, ...]

    @property
    def clean(self) -> bool:
        return not self.unparsed_lines and (self.no_goals or bool(self.goals))


def metavariables_in(*texts: str) -> tuple[str, ...]:
    values: set[str] = set()
    for text in texts:
        values.update(_METAVARIABLE.findall(text))
    return tuple(sorted(values))


def case_label(raw_state: str) -> str | None:
    first = raw_state.splitlines()[0].strip() if raw_state else ""
    return first[5:].strip() if first.startswith("case ") else None


def _split_definition(body: str) -> tuple[str, str | None]:
    depth = 0
    for index, character in enumerate(body[:-1]):
        if character in "([{":
            depth += 1
        elif character in ")]}":
            depth = max(depth - 1, 0)
        elif depth == 0 and body[index : index + 2] == ":=":
            return body[:index].strip(), body[index + 2 :].strip()
    return body.strip(), None


def _parse_goal_block(lines: list[str]) -> tuple[ParsedGoal | None, list[str]]:
    label: str | None = None
    declarations: list[ParsedDeclaration] = []
    target_lines: list[str] = []
    unparsed: list[str] = []
    pending: list[str] | None = None
    in_target = False

    def flush_declaration() -> None:
        nonlocal pending
        if pending is None:
            return
        match = _DECLARATION.match(pending[0])
        if match is None:
            unparsed.extend(pending)
            pending = None
            return
        continuation = " ".join(part.strip() for part in pending[1:])
        body = " ".join(part for part in (match.group("body").strip(), continuation) if part)
        type_text, value_text = _split_definition(body)
        declarations.append(
            ParsedDeclaration(tuple(match.group("names").split()), type_text, value_text)
        )
        pending = None

    for raw_line in lines:
        line = raw_line.rstrip()
        if not line.strip():
            continue
        if in_target:
            target_lines.append(line.strip())
            continue
        if line.startswith("case "):
            flush_declaration()
            label = line[5:].strip()
            continue
        if line.lstrip().startswith("⊢"):
            flush_declaration()
            in_target = True
            target_lines.append(line.lstrip()[1:].strip())
            continue
        if raw_line.startswith((" ", "\t")) and pending is not None:
            pending.append(line)
            continue
        if _DECLARATION.match(line):
            flush_declaration()
            pending = [line]
            continue
        if pending is not None:
            pending.append(line)
            continue
        unparsed.append(line)
    flush_declaration()
    target = " ".join(target_lines).strip()
    if not target:
        return None, unparsed + [line for line in lines if line.strip()]
    return ParsedGoal(label, tuple(declarations), target), unparsed


def parse_lean_state(raw_state: str) -> ParsedLeanState:
    """Parse every displayed goal; partial parses carry their unclassified lines."""
    stripped = raw_state.strip()
    if not stripped or stripped.startswith("no goals"):
        return ParsedLeanState((), True, ())
    goals: list[ParsedGoal] = []
    unparsed: list[str] = []
    for chunk in re.split(r"\n[ \t]*\n", stripped):
        goal, failures = _parse_goal_block(chunk.splitlines())
        unparsed.extend(failures)
        if goal is not None:
            goals.append(goal)
    return ParsedLeanState(tuple(goals), False, tuple(unparsed))


def validate_observation(
    raw_state: str,
    hypotheses: tuple[dict[str, str], ...],
    target: str,
    expected_goal_count: int,
) -> list[str]:
    """Return source/decomposition inconsistencies; never repair them silently."""
    failures: list[str] = []
    parsed = parse_lean_state(raw_state)
    if expected_goal_count != len(parsed.goals):
        failures.append(
            f"goal count mismatch: source={expected_goal_count}, decomposed={len(parsed.goals)}"
        )
    if expected_goal_count == 0 and not parsed.no_goals:
        failures.append("source says zero goals but raw state is not terminal")
    if target and (not parsed.goals or parsed.goals[0].target != target):
        failures.append("focused target differs from the first raw-state goal")
    if parsed.goals:
        decomposed = [
            {"name": name, "type": declaration.type_text}
            for declaration in parsed.goals[0].declarations
            for name in declaration.names
        ]
        if decomposed != list(hypotheses):
            failures.append("focused local context differs from source decomposition")
    if parsed.unparsed_lines:
        failures.append(f"raw-state decomposition left {len(parsed.unparsed_lines)} unparsed lines")
    return failures
