"""Trace line for rentals: the non-compliant amount of one short-term rental row."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from app.domain.artifact import Money
from app.domain.parameters.rounding import RoundingRule
from app.domain.trace.base import TraceLine

__all__ = ["ShortTermRentalNonCompliantLine"]


@dataclass(frozen=True)
class ShortTermRentalNonCompliantLine(TraceLine):
    """The non-compliant amount `result` of one short-term rental row, by `position` (from 1),
    for `output`.

    It is the row's `related_expenses` times its `non_compliant_days` divided by its `days`, as an
    exact fraction rounded once with `rounding`.
    """

    output: Money
    position: int
    related_expenses: Decimal
    non_compliant_days: int
    days: int
    rounding: RoundingRule
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The row's non-compliant amount."""
        return self.result
