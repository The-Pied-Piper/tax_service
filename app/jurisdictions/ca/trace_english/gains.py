"""English text for the trace lines of `app.jurisdictions.ca.trace.gains`: one
renderer class per line class, each registered with `@english_renderer`.
"""

from __future__ import annotations

from decimal import Decimal

from app.adapters.inbound.trace_english.figures import EnglishFigures
from app.adapters.inbound.trace_english.registry import english_renderer
from app.domain.artifact import Money
from app.jurisdictions.ca.trace.gains import (
    DispositionGainLine,
    DispositionGainOnlyLine,
    DispositionProceedsLine,
    NetCapitalLossesRowLine,
    PrincipalResidenceGainLine,
    PrincipalResidenceLine27,
    PrincipalResidenceLine29,
    PrincipalResidenceLine30,
    PrincipalResidenceLine32,
    PrincipalResidenceLine33,
    PrincipalResidenceLine38,
    PrincipalResidenceLine39,
    PrincipalResidenceLine42,
    PrincipalResidenceLine44,
    PrincipalResidenceLine45,
    PrincipalResidenceLine48,
    PrincipalResidenceLine51,
    PrincipalResidenceLine53,
)


def _part_2_step(
    output: Money, position: int, number: int, result: Decimal, body: str, completed: bool
) -> str:
    """The sentence of Part 2 line `number`: its figure, then `body` (the figures it takes). A step
    the form says not to complete reads as 0."""
    if not completed:
        return f"{output.label}: property {position}: line {number} not completed, 0"
    return (
        f"{output.label}: property {position}: line {number} "
        f"{EnglishFigures.money(result)} = {body}"
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
        line_24 = line.line_24
        text = (
            f"{output.label}: property {position}: gain {EnglishFigures.money(gain)} = proceeds "
            f"{EnglishFigures.money(proceeds)} less adjusted cost base "
            f"{EnglishFigures.money(cost_base)} "
            f"less outlays {EnglishFigures.money(outlays)}; exempt {EnglishFigures.money(exempt)} "
            f"= "
            f"{EnglishFigures.money(gain)} × ({designated} designated + {plus_one}) ÷ {owned} "
            f"owned ({EnglishFigures.rounding(rule)}); taxable gain "
            f"{EnglishFigures.money(line_24)} "
            f"= "
            f"{EnglishFigures.money(gain)} less {EnglishFigures.money(exempt)}, not below 0"
        )
        if line.part_2_applies != 1:
            return text
        return (
            f"{text}; Part 2 net capital gain {EnglishFigures.money(line.line_53)}; "
            f"total capital gain {EnglishFigures.money(result)} = lesser of "
            f"{EnglishFigures.money(line.line_53)} and {EnglishFigures.money(line_24)}"
        )


@english_renderer
class PrincipalResidenceLine27Renderer:
    """English text for PrincipalResidenceLine27."""

    line_class = PrincipalResidenceLine27

    def render(self, line: PrincipalResidenceLine27) -> str:
        """The English sentence for `line`."""
        return _part_2_step(
            line.output,
            line.position,
            27,
            line.result,
            f"line 12 {EnglishFigures.money(line.line_12)} less line 11 "
            f"{EnglishFigures.money(line.line_11)}",
            line.completed,
        )


@english_renderer
class PrincipalResidenceLine29Renderer:
    """English text for PrincipalResidenceLine29."""

    line_class = PrincipalResidenceLine29

    def render(self, line: PrincipalResidenceLine29) -> str:
        """The English sentence for `line`."""
        return _part_2_step(
            line.output,
            line.position,
            29,
            line.result,
            f"line 2 {line.line_2} plus {line.plus_one}",
            line.completed,
        )


@english_renderer
class PrincipalResidenceLine30Renderer:
    """English text for PrincipalResidenceLine30."""

    line_class = PrincipalResidenceLine30

    def render(self, line: PrincipalResidenceLine30) -> str:
        """The English sentence for `line`."""
        return _part_2_step(
            line.output,
            line.position,
            30,
            line.result,
            f"line 27 {EnglishFigures.money(line.line_27)} times line 29 {int(line.line_29)}",
            line.completed,
        )


@english_renderer
class PrincipalResidenceLine32Renderer:
    """English text for PrincipalResidenceLine32."""

    line_class = PrincipalResidenceLine32

    def render(self, line: PrincipalResidenceLine32) -> str:
        """The English sentence for `line`."""
        return _part_2_step(
            line.output,
            line.position,
            32,
            line.result,
            f"line 30 {EnglishFigures.money(line.line_30)} divided by line 6 {line.line_6} "
            f"({EnglishFigures.rounding(line.rounding)})",
            line.completed,
        )


@english_renderer
class PrincipalResidenceLine33Renderer:
    """English text for PrincipalResidenceLine33."""

    line_class = PrincipalResidenceLine33

    def render(self, line: PrincipalResidenceLine33) -> str:
        """The English sentence for `line`."""
        return _part_2_step(
            line.output,
            line.position,
            33,
            line.result,
            f"line 27 {EnglishFigures.money(line.line_27)} less line 32 "
            f"{EnglishFigures.money(line.line_32)}, not below 0",
            line.completed,
        )


@english_renderer
class PrincipalResidenceLine38Renderer:
    """English text for PrincipalResidenceLine38."""

    line_class = PrincipalResidenceLine38

    def render(self, line: PrincipalResidenceLine38) -> str:
        """The English sentence for `line`."""
        return _part_2_step(
            line.output,
            line.position,
            38,
            line.result,
            f"line 12 {EnglishFigures.money(line.line_12)} plus line 13 "
            f"{EnglishFigures.money(line.line_13)} plus line 9 {EnglishFigures.money(line.line_9)}",
            line.completed,
        )


@english_renderer
class PrincipalResidenceLine39Renderer:
    """English text for PrincipalResidenceLine39."""

    line_class = PrincipalResidenceLine39

    def render(self, line: PrincipalResidenceLine39) -> str:
        """The English sentence for `line`."""
        return _part_2_step(
            line.output,
            line.position,
            39,
            line.result,
            f"line 8 {EnglishFigures.money(line.line_8)} less line 38 "
            f"{EnglishFigures.money(line.line_38)}",
            line.completed,
        )


@english_renderer
class PrincipalResidenceLine42Renderer:
    """English text for PrincipalResidenceLine42."""

    line_class = PrincipalResidenceLine42

    def render(self, line: PrincipalResidenceLine42) -> str:
        """The English sentence for `line`."""
        return _part_2_step(
            line.output,
            line.position,
            42,
            line.result,
            f"line 39 {EnglishFigures.money(line.line_39)} times line 1 {line.line_1}",
            line.completed,
        )


@english_renderer
class PrincipalResidenceLine44Renderer:
    """English text for PrincipalResidenceLine44."""

    line_class = PrincipalResidenceLine44

    def render(self, line: PrincipalResidenceLine44) -> str:
        """The English sentence for `line`."""
        return _part_2_step(
            line.output,
            line.position,
            44,
            line.result,
            f"line 42 {EnglishFigures.money(line.line_42)} divided by line 5 {line.line_5} "
            f"({EnglishFigures.rounding(line.rounding)})",
            line.completed,
        )


@english_renderer
class PrincipalResidenceLine45Renderer:
    """English text for PrincipalResidenceLine45."""

    line_class = PrincipalResidenceLine45

    def render(self, line: PrincipalResidenceLine45) -> str:
        """The English sentence for `line`."""
        return _part_2_step(
            line.output,
            line.position,
            45,
            line.result,
            f"line 39 {EnglishFigures.money(line.line_39)} less line 44 "
            f"{EnglishFigures.money(line.line_44)}, not below 0",
            line.completed,
        )


@english_renderer
class PrincipalResidenceLine48Renderer:
    """English text for PrincipalResidenceLine48."""

    line_class = PrincipalResidenceLine48

    def render(self, line: PrincipalResidenceLine48) -> str:
        """The English sentence for `line`."""
        return _part_2_step(
            line.output,
            line.position,
            48,
            line.result,
            f"line 12 {EnglishFigures.money(line.line_12)} less line 8 "
            f"{EnglishFigures.money(line.line_8)}, not below 0",
            line.completed,
        )


@english_renderer
class PrincipalResidenceLine51Renderer:
    """English text for PrincipalResidenceLine51."""

    line_class = PrincipalResidenceLine51

    def render(self, line: PrincipalResidenceLine51) -> str:
        """The English sentence for `line`."""
        return _part_2_step(
            line.output,
            line.position,
            51,
            line.result,
            f"line 33 {EnglishFigures.money(line.line_33)} plus line 45 "
            f"{EnglishFigures.money(line.line_45)}",
            line.completed,
        )


@english_renderer
class PrincipalResidenceLine53Renderer:
    """English text for PrincipalResidenceLine53."""

    line_class = PrincipalResidenceLine53

    def render(self, line: PrincipalResidenceLine53) -> str:
        """The English sentence for `line`."""
        return _part_2_step(
            line.output,
            line.position,
            53,
            line.result,
            f"line 51 {EnglishFigures.money(line.line_51)} less line 48 "
            f"{EnglishFigures.money(line.line_48)}, not below 0",
            line.completed,
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
