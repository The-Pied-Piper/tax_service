"""English text for the trace lines of `app.domain.trace.gains`: one renderer class
per line class, each registered with `@english_renderer`.
"""

from __future__ import annotations

from app.adapters.inbound.trace_english.figures import EnglishFigures
from app.adapters.inbound.trace_english.registry import english_renderer
from app.domain.trace.gains import (
    DispositionGainLine,
    DispositionGainOnlyLine,
    PrincipalResidenceGainLine,
)


@english_renderer
class PrincipalResidenceGainRenderer(EnglishFigures):
    """English text for PrincipalResidenceGainLine."""

    line_class = PrincipalResidenceGainLine

    def render(self, line: PrincipalResidenceGainLine) -> str:
        """The English sentence for `line`."""
        output = line.output
        position = line.position
        designated = line.designated
        owned = line.owned
        plus_one = line.plus_one
        proceeds = line.proceeds
        cost_base = line.adjusted_cost_base
        outlays = line.outlays
        gain = line.gain
        exempt = line.exempt
        rule = line.rounding
        result = line.result
        return (
            f"{output.label}: property {position}: gain {self._money(gain)} = proceeds "
            f"{self._money(proceeds)} less adjusted cost base {self._money(cost_base)} "
            f"less outlays {self._money(outlays)}; exempt {self._money(exempt)} = "
            f"{self._money(gain)} × ({designated} designated + {plus_one}) ÷ {owned} "
            f"owned ({self._rounding(rule)}); taxable gain {self._money(result)} = "
            f"{self._money(gain)} less {self._money(exempt)}, not below 0"
        )


@english_renderer
class DispositionGainRenderer(EnglishFigures):
    """English text for DispositionGainLine."""

    line_class = DispositionGainLine

    def render(self, line: DispositionGainLine) -> str:
        """The English sentence for `line`."""
        output = line.output
        position = line.position
        proceeds = line.proceeds
        cost_base = line.adjusted_cost_base
        outlays = line.outlays
        result = line.result
        return (
            f"{output.label}: disposition {position}: gain or loss {self._money(result)} "
            f"= proceeds {self._money(proceeds)} less adjusted cost base "
            f"{self._money(cost_base)} less outlays {self._money(outlays)}"
        )


@english_renderer
class DispositionGainOnlyRenderer(EnglishFigures):
    """English text for DispositionGainOnlyLine."""

    line_class = DispositionGainOnlyLine

    def render(self, line: DispositionGainOnlyLine) -> str:
        """The English sentence for `line`."""
        output = line.output
        position = line.position
        proceeds = line.proceeds
        cost_base = line.adjusted_cost_base
        outlays = line.outlays
        gain = line.gain
        result = line.result
        return (
            f"{output.label}: disposition {position}: gain {self._money(gain)} = "
            f"proceeds {self._money(proceeds)} less adjusted cost base "
            f"{self._money(cost_base)} less outlays {self._money(outlays)}; gain only "
            f"{self._money(result)}, not below 0"
        )
