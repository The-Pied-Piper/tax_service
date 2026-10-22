"""English text for the trace lines of `app.jurisdictions.ca_on.trace.foreign_tax`: one
renderer class per line class, each registered with `@english_renderer`.
"""

from __future__ import annotations

from app.adapters.inbound.trace_english.figures import EnglishFigures
from app.adapters.inbound.trace_english.registry import english_renderer
from app.jurisdictions.ca_on.trace.foreign_tax import ProvincialForeignTaxCreditLine


@english_renderer
class ProvincialForeignTaxCreditRenderer:
    """English text for ProvincialForeignTaxCreditLine."""

    line_class = ProvincialForeignTaxCreditLine

    def render(self, line: ProvincialForeignTaxCreditLine) -> str:
        """The English sentence for `line`."""
        money = EnglishFigures.money
        return (
            f"{line.output.label}: sheet {line.position}: tax paid {money(line.tax_paid)} less "
            f"federal credit {money(line.federal_credit)} = {money(line.line_3)}; "
            f"{money(line.income)} net foreign income x {money(line.provincial_tax)} provincial "
            f"tax / {money(line.net_income)} net income = {money(line.line_4)} "
            f"({EnglishFigures.rounding(line.rounding)}); credit {money(line.result)}"
        )
