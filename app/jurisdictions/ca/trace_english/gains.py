"""English text for the trace lines of `app.jurisdictions.ca.trace.gains`: one
renderer class per line class, each registered with `@english_renderer`.
"""

from __future__ import annotations

from app.adapters.inbound.trace_english.figures import EnglishFigures
from app.adapters.inbound.trace_english.registry import english_renderer
from app.jurisdictions.ca.trace.gains import (
    DispositionGainLine,
    DispositionGainOnlyLine,
    DispositionProceedsLine,
    NetCapitalLossesRowLine,
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


@english_renderer
class DispositionProceedsRenderer:
    """English text for DispositionProceedsLine."""

    line_class = DispositionProceedsLine

    def render(self, line: DispositionProceedsLine) -> str:
        """The English sentence for `line`."""
        output = line.output
        position = line.position
        proceeds = line.proceeds
        return f"{output.label}: disposition {position}: proceeds {EnglishFigures.money(proceeds)}"


@english_renderer
class NetCapitalLossesRowRenderer:
    """English text for NetCapitalLossesRowLine."""

    line_class = NetCapitalLossesRowLine

    def render(self, line: NetCapitalLossesRowLine) -> str:
        """The English sentence for `line`."""
        money = EnglishFigures.money
        return (
            f"{line.output.label}: item {line.position}: column E {money(line.column_e)} = "
            f"column C {money(line.column_c)} less column D {money(line.column_d)}, not below 0; "
            f"column F {money(line.column_f)} = column B {money(line.column_b)} plus column E "
            f"{money(line.column_e)}; column G {money(line.column_g)} = column A "
            f"{money(line.column_a)} less column F {money(line.column_f)}, not below 0"
        )
