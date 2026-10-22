"""Trace line for forms: the lines of one instance's run, grouped under the form's name."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from app.domain.trace.base import TraceLine

__all__ = ["FormInstanceLine"]


@dataclass(frozen=True)
class FormInstanceLine(TraceLine):
    """The `lines` of the run of the form named `form` on its instance at `position` (from 1),
    in the order they were recorded.

    Its own class: the form is a group of capabilities, not a capability, so the lines of an
    instance are kept together here rather than among the lines of the return.
    """

    form: str
    position: int
    lines: tuple[TraceLine, ...]

    @property
    def amount(self) -> Decimal:
        """Zero: the group is not about one figure; its inner lines each are."""
        return Decimal(0)
