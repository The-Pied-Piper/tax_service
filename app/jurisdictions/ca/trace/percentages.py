"""The percentage-applied trace line: an amount times a percentage, rounded once."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from app.domain.artifact import Money
from app.domain.parameters.rounding import RoundingRule
from app.domain.trace.base import TraceLine

__all__ = ["PercentageAppliedLine"]


@dataclass(frozen=True)
class PercentageAppliedLine(TraceLine):
    """An amount times a percentage over 100, rounded once with the dataset rounding."""

    output: Money
    amount_kind: Money
    amount_value: Decimal
    percentage_kind: Money
    percentage_value: Decimal
    rounding: RoundingRule
    result: Decimal

    @property
    def amount(self) -> Decimal:
        return self.result
