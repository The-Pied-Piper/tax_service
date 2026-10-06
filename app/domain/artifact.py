"""Artifacts: named intermediate values that capabilities consume and produce.

Ordering in the engine is expressed through artifacts, never through direct
capability-to-capability dependencies (design.md §2). Each artifact is a class,
which is its identity; an instance carries its value in one computation. Names
come from the jurisdiction's own law or return, never from another system's.

The hierarchy has two levels: value types such as `Amount` subclass `Artifact`,
and each concrete artifact subclasses one value type. The value type is the
artifact's unit, so wiring money where a count is expected is the wrong class.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Self


class Artifact:
    """Root of all artifacts; subclass a value type such as `Amount`, not this."""

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        (parent,) = cls.__bases__
        if parent is not Artifact and parent.__bases__ != (Artifact,):
            raise TypeError(
                f"{cls.__name__} must subclass a value type such as Amount, "
                f"not the artifact {parent.__name__}"
            )

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        if cls is Artifact or cls.__bases__ == (Artifact,):
            raise TypeError(f"{cls.__name__} is not an artifact; subclass it to define one")
        return super().__new__(cls)

    @classmethod
    def label(cls) -> str:
        """The artifact's name in snake_case, for traces and messages."""
        words = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", cls.__name__)
        return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", words).lower()


@dataclass(frozen=True)
class Amount(Artifact):
    """A money artifact: its value is an exact `Decimal` in the jurisdiction's currency."""

    value: Decimal

    def __post_init__(self) -> None:
        if not isinstance(self.value, Decimal):
            raise TypeError(
                f"{type(self).__name__} must be a Decimal, got {type(self.value).__name__}"
            )
