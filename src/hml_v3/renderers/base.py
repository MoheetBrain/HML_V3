"""Renderer interface and strict projection equality helpers."""

from __future__ import annotations

from abc import ABC, abstractmethod
import json
from typing import Any


Projection = dict[str, Any]


def canonical_projection_json(projection: Projection) -> str:
    return json.dumps(projection, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


class Renderer(ABC):
    renderer_id: str
    version: str = "1.0.0"

    @abstractmethod
    def render(self, projection: Projection) -> str:
        raise NotImplementedError

    @abstractmethod
    def parse(self, text: str) -> Projection:
        raise NotImplementedError

    def roundtrip(self, projection: Projection) -> Projection:
        return self.parse(self.render(projection))
