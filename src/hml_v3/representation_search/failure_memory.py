"""Loader and enforcement for the persistent failure memory.

Every generation consults this. A mutation that reproduces a trait recorded as
`DO_NOT_RETRY_UNCHANGED` is blocked unless the proposing hypothesis names the changed
condition that makes the earlier refutation inapplicable, and the retry budget for that
lesson has not been spent.

New negative results are appended here as they are measured, so a later session does not
re-derive them.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

MEMORY_JSON = Path(__file__).resolve().parents[3] / "research/representation_search/hml_failure_memory.json"


@dataclass
class Lesson:
    id: str
    title: str
    disposition: str
    evidence_status: str
    blocked_traits: tuple[str, ...]
    pinned_seed_candidates: tuple[str, ...]
    retry_budget: int
    changed_condition: str | None
    payload: dict[str, Any]


@dataclass
class FailureMemory:
    path: Path
    lessons: list[Lesson] = field(default_factory=list)
    retries_used: dict[str, int] = field(default_factory=dict)

    @classmethod
    def load(cls, path: Path = MEMORY_JSON) -> "FailureMemory":
        payload = json.loads(path.read_text(encoding="utf-8"))
        lessons = [
            Lesson(
                id=item["id"],
                title=item["title"],
                disposition=item["disposition"],
                evidence_status=item.get("evidence_status", "UNKNOWN"),
                blocked_traits=tuple(item.get("blocked_traits", ())),
                pinned_seed_candidates=tuple(item.get("pinned_seed_candidates", ())),
                retry_budget=int(item.get("retry_budget", 0)),
                changed_condition=item.get("changed_condition_permitting_one_retry"),
                payload=item,
            )
            for item in payload["lessons"]
        ]
        return cls(path=path, lessons=lessons)

    # ------------------------------------------------------------------------- queries
    def pinned_seeds(self) -> list[str]:
        pinned: list[str] = []
        for lesson in self.lessons:
            pinned.extend(lesson.pinned_seed_candidates)
        return sorted(set(pinned))

    def blocking_lesson(self, axis: str, value: str) -> Lesson | None:
        trait = f"{axis}={value}"
        for lesson in self.lessons:
            if lesson.disposition != "DO_NOT_RETRY_UNCHANGED":
                continue
            if trait in lesson.blocked_traits:
                return lesson
        return None

    def may_apply(self, axis: str, value: str, changed_condition: str | None = None) -> tuple[bool, str]:
        """Returns ``(allowed, reason)`` for setting ``axis`` to ``value``."""

        lesson = self.blocking_lesson(axis, value)
        if lesson is None:
            return True, "NO_RECORDED_NEGATIVE"
        used = self.retries_used.get(lesson.id, 0)
        if changed_condition and used < lesson.retry_budget:
            return True, f"RETRY_WITH_CHANGED_CONDITION:{lesson.id}"
        if changed_condition:
            return False, f"RETRY_BUDGET_EXHAUSTED:{lesson.id}"
        return False, f"BLOCKED_BY:{lesson.id}"

    def consume_retry(self, lesson_id: str) -> None:
        self.retries_used[lesson_id] = self.retries_used.get(lesson_id, 0) + 1

    def hard_gate_lessons(self) -> list[Lesson]:
        return [lesson for lesson in self.lessons if lesson.disposition == "HARD_GATE"]

    # ------------------------------------------------------------------------- writing
    def append_lesson(self, lesson: dict[str, Any]) -> None:
        """Append a newly measured negative result and persist it."""

        payload = json.loads(self.path.read_text(encoding="utf-8"))
        existing = {item["id"] for item in payload["lessons"]}
        if lesson["id"] in existing:
            payload["lessons"] = [
                lesson if item["id"] == lesson["id"] else item for item in payload["lessons"]
            ]
        else:
            payload["lessons"].append(lesson)
        self.path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
            encoding="utf-8",
        )
        self.lessons = FailureMemory.load(self.path).lessons

    def summary(self) -> dict[str, Any]:
        by_disposition: dict[str, list[str]] = {}
        for lesson in self.lessons:
            by_disposition.setdefault(lesson.disposition, []).append(lesson.id)
        return {
            "path": str(self.path),
            "lesson_count": len(self.lessons),
            "by_disposition": {key: sorted(value) for key, value in sorted(by_disposition.items())},
            "retries_used": dict(self.retries_used),
        }
