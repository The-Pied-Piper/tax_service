"""Trace lines for the foreign tax credit: one country's line 3, or all countries pooled."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from app.domain.artifact import Money
from app.domain.parameters.rounding import RoundingRule
from app.domain.trace.base import TraceLine

__all__ = ["ForeignTaxCreditLine", "PooledForeignTaxCreditLine"]


@dataclass(frozen=True)
class ForeignTaxCreditLine(TraceLine):
    """The federal non-business foreign tax credit `result` of one country, by `position` (from
    1), for `output`.

    Line 2 is the country's `income` (already capped at `net_income`) times `basic_federal_tax`
    divided by `net_income`, rounded once with `rounding`; the result is the lesser of the
    country's `tax_paid` (line 1) and `line_2`.
    """

    output: Money
    position: int
    tax_paid: Decimal
    income: Decimal
    net_income: Decimal
    basic_federal_tax: Decimal
    rounding: RoundingRule
    line_2: Decimal
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The country's credit."""
        return self.result


@dataclass(frozen=True)
class PooledForeignTaxCreditLine(TraceLine):
    """The federal non-business foreign tax credit `result` of all `countries` worked as one, for
    `output`.

    The countries are pooled when there is one of them or when their total `tax_paid` is not more
    than `threshold`. Line 2 is the total `income` (already capped at `net_income`) times
    `basic_federal_tax` divided by `net_income`, rounded once with `rounding`; the result is the
    lesser of `tax_paid` and `line_2`.
    """

    output: Money
    countries: int
    tax_paid: Decimal
    income: Decimal
    net_income: Decimal
    basic_federal_tax: Decimal
    threshold: Decimal
    rounding: RoundingRule
    line_2: Decimal
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The pooled credit."""
        return self.result
