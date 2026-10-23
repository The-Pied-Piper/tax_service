"""English text for the trace lines of `app.jurisdictions.ca.trace.foreign_tax`: one
renderer class per line class, each registered with `@english_renderer`.
"""

from __future__ import annotations

from app.adapters.inbound.trace_english.figures import EnglishFigures
from app.adapters.inbound.trace_english.registry import english_renderer
from app.jurisdictions.ca.trace.foreign_tax import ForeignTaxCreditLine, PooledForeignTaxCreditLine


@english_renderer
class ForeignTaxCreditRenderer:
    """English text for ForeignTaxCreditLine."""

    line_class = ForeignTaxCreditLine

    def render(self, line: ForeignTaxCreditLine) -> str:
        """The English sentence for `line`."""
        money = EnglishFigures.money
        return (
            f"{line.output.label}: country {line.position}: tax paid {money(line.tax_paid)}, "
            f"{money(line.income)} net foreign income x {money(line.basic_federal_tax)} basic "
            f"federal tax / {money(line.net_income)} net income = {money(line.line_2)} "
            f"({EnglishFigures.rounding(line.rounding)}); credit {money(line.result)}"
        )


@english_renderer
class PooledForeignTaxCreditRenderer:
    """English text for PooledForeignTaxCreditLine."""

    line_class = PooledForeignTaxCreditLine

    def render(self, line: PooledForeignTaxCreditLine) -> str:
        """The English sentence for `line`."""
        money = EnglishFigures.money
        if line.countries == 1:
            start = f"one country: tax paid {money(line.tax_paid)},"
        else:
            start = (
                f"all {line.countries} countries pooled, total tax paid {money(line.tax_paid)} "
                f"is not more than {money(line.threshold)}:"
            )
        return (
            f"{line.output.label}: {start} {money(line.income)} net foreign income x "
            f"{money(line.basic_federal_tax)} basic federal tax / {money(line.net_income)} net "
            f"income = {money(line.line_2)} ({EnglishFigures.rounding(line.rounding)}); "
            f"credit {money(line.result)}"
        )
