"""Trace line for the provincial foreign tax credit: one sheet's lines 1 to 5 of Form T2036."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from app.domain.artifact import Money
from app.domain.parameters.rounding import RoundingRule
from app.domain.trace.base import TraceLine

__all__ = ["ProvincialForeignTaxCreditLine"]


@dataclass(frozen=True)
class ProvincialForeignTaxCreditLine(TraceLine):
    """The provincial foreign tax credit `result` of one sheet of Form T2209, by `position` (from
    1), for `output`.

    Line 3 is the sheet's `tax_paid` (line 1) less the `federal_credit` (line 2, the sheet's line 3
    of Form T2209). Line 4 is the sheet's `income` times `provincial_tax` divided by `net_income`,
    rounded once with `rounding`; the result is the lesser of `line_3` and `line_4`.
    """

    output: Money
    position: int
    tax_paid: Decimal
    federal_credit: Decimal
    line_3: Decimal
    income: Decimal
    net_income: Decimal
    provincial_tax: Decimal
    rounding: RoundingRule
    line_4: Decimal
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The sheet's credit."""
        return self.result
