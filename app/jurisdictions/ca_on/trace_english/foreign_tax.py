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
            f"{self._line_2(line)} = {money(line.line_3)}; "
            f"{money(line.income)} net foreign income x {money(line.provincial_tax)} provincial "
            f"tax / {money(line.net_income)} net income = {money(line.line_4)} "
            f"({EnglishFigures.rounding(line.rounding)}); credit {money(line.result)}"
        )

    @staticmethod
    def _line_2(line: ProvincialForeignTaxCreditLine) -> str:
        """The wording of line 2: the federal credit, or the share of the special credit."""
        money = EnglishFigures.money
        if line.special_credit is None or line.divisor is None:
            return f"federal credit {money(line.federal_credit)}"
        basis = (
            "total foreign taxes paid, separate sheet"
            if line.separate_sheet
            else "total tax paid plus business tax"
        )
        return (
            f"minimum tax line 2 {money(line.federal_credit)} ({money(line.tax_paid)} tax paid x "
            f"{money(line.special_credit)} special foreign tax credit / "
            f"{EnglishFigures.exact(line.divisor)} {basis}, "
            f"{EnglishFigures.rounding(line.rounding)})"
        )
