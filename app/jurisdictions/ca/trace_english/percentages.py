"""English wording of the percentage-applied trace line."""

from __future__ import annotations

from app.adapters.inbound.trace_english.figures import EnglishFigures
from app.adapters.inbound.trace_english.registry import english_renderer
from app.jurisdictions.ca.trace.percentages import PercentageAppliedLine


@english_renderer
class PercentageAppliedRenderer:
    line_class = PercentageAppliedLine

    def render(self, line: PercentageAppliedLine) -> str:
        return (
            f"{line.output.label}: {line.percentage_kind.label} "
            f"{EnglishFigures.money(line.percentage_value)}% of {line.amount_kind.label} "
            f"{EnglishFigures.money(line.amount_value)} = {EnglishFigures.money(line.result)} "
            f"({EnglishFigures.rounding(line.rounding)})"
        )
