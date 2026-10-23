"""English text for the trace lines of `app.jurisdictions.ca.trace.vehicles`: one renderer class
per line class, each registered with `@english_renderer`.
"""

from __future__ import annotations

from app.adapters.inbound.trace_english.figures import EnglishFigures
from app.adapters.inbound.trace_english.registry import english_renderer
from app.jurisdictions.ca.trace.vehicles import BusinessVehicleLine


@english_renderer
class BusinessVehicleRenderer:
    """English text for BusinessVehicleLine."""

    line_class = BusinessVehicleLine

    def render(self, line: BusinessVehicleLine) -> str:
        """The English sentence for `line`."""
        money = EnglishFigures.money
        return (
            f"{line.output.label}: item {line.position}: line 12 {money(line.line_12)}, "
            f"line 13 {money(line.line_13)}, line 19 {money(line.line_19)}, "
            f"line 28 {money(line.line_28)}, line 16 {money(line.line_16)}"
        )
