"""Trace line for capped records: one item of a record list, capped at a dataset's maximum."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from app.domain.artifact import Money
from app.domain.parameters.amount import Amount
from app.domain.parameters.rounding import RoundingRule
from app.domain.trace.base import TraceLine

__all__ = ["CappedRecordLine"]


@dataclass(frozen=True)
class CappedRecordLine(TraceLine):
    """The capped amount `result` of one item of a record list, by `position` (from 1), for
    `output`.

    The item's `expenditure` is the lesser of itself and the `cap` dataset's amount, rounded with
    `rounding` to `result`. Its own class, not a `CappedAmountLine`: it names the item by its
    position, and the total of the items is an `ItemsTotalLine`.
    """

    output: Money
    position: int
    expenditure: Decimal
    cap: Amount
    rounding: RoundingRule
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The item's expenditure, before the cap."""
        return self.expenditure
