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
class PrincipalResidenceGainRenderer:
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
            f"{output.label}: property {position}: gain {EnglishFigures.money(gain)} = proceeds "
            f"{EnglishFigures.money(proceeds)} less adjusted cost base "
            f"{EnglishFigures.money(cost_base)} "
            f"less outlays {EnglishFigures.money(outlays)}; exempt {EnglishFigures.money(exempt)} "
            f"= "
            f"{EnglishFigures.money(gain)} × ({designated} designated + {plus_one}) ÷ {owned} "
            f"owned ({EnglishFigures.rounding(rule)}); taxable gain {EnglishFigures.money(result)} "
            f"= "
            f"{EnglishFigures.money(gain)} less {EnglishFigures.money(exempt)}, not below 0"
        )


@english_renderer
class DispositionGainRenderer:
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
            f"{output.label}: disposition {position}: gain or loss {EnglishFigures.money(result)} "
            f"= proceeds {EnglishFigures.money(proceeds)} less adjusted cost base "
            f"{EnglishFigures.money(cost_base)} less outlays {EnglishFigures.money(outlays)}"
        )


@english_renderer
class DispositionGainOnlyRenderer:
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
            f"{output.label}: disposition {position}: gain {EnglishFigures.money(gain)} = "
            f"proceeds {EnglishFigures.money(proceeds)} less adjusted cost base "
            f"{EnglishFigures.money(cost_base)} less outlays {EnglishFigures.money(outlays)}; gain "
            f"only "
            f"{EnglishFigures.money(result)}, not below 0"
        )
