"""Artifacts: named intermediate values that capabilities consume and produce.

Ordering in the engine is expressed through artifacts, never through direct
capability-to-capability dependencies (design.md §2). Names are snake_case and
come from the jurisdiction's own law or return, never from another system's.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_SNAKE_CASE = re.compile(r"[a-z][a-z0-9]*(_[a-z0-9]+)*")


@dataclass(frozen=True)
class Artifact:
    name: str

    def __post_init__(self) -> None:
        if not isinstance(self.name, str):
            raise TypeError(f"artifact name must be a str, got {type(self.name).__name__}")
        if not _SNAKE_CASE.fullmatch(self.name):
            raise ValueError(f"invalid artifact name {self.name!r}: expected snake_case")

    def __str__(self) -> str:
        return self.name
