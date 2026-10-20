"""English text for the trace lines of `app.jurisdictions.ca.trace.rentals`: one
renderer class per line class, each registered with `@english_renderer`.
"""

from __future__ import annotations

from app.adapters.inbound.trace_english.figures import EnglishFigures
from app.adapters.inbound.trace_english.registry import english_renderer
from app.jurisdictions.ca.trace.rentals import ShortTermRentalNonCompliantLine


@english_renderer
class ShortTermRentalNonCompliantRenderer:
    """English text for ShortTermRentalNonCompliantLine."""

    line_class = ShortTermRentalNonCompliantLine

    def render(self, line: ShortTermRentalNonCompliantLine) -> str:
        """The English sentence for `line`."""
        output = line.output
        position = line.position
        related_expenses = line.related_expenses
        non_compliant_days = line.non_compliant_days
        days = line.days
        rule = line.rounding
        result = line.result
        return (
            f"{output.label}: row {position}: expenses {EnglishFigures.money(related_expenses)} "
            f"for {non_compliant_days} non-compliant days of {days} short-term days = "
            f"{EnglishFigures.money(result)} ({EnglishFigures.rounding(rule)})"
        )
