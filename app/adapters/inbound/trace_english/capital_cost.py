"""English text for the trace lines of `app.domain.trace.capital_cost`: one renderer class
per line class, each registered with `@english_renderer`.
"""

from __future__ import annotations

from app.adapters.inbound.trace_english.figures import EnglishFigures
from app.adapters.inbound.trace_english.registry import english_renderer
from app.domain.parameters.class_rates import RecaptureAndTerminalLoss
from app.domain.trace.capital_cost import (
    CcaClaimLine,
    CcaZeroReason,
    ClosingUccLine,
    RecapturedCcaLine,
    TerminalLossLine,
)


@english_renderer
class CcaClaimRenderer:
    """English text for CcaClaimLine."""

    line_class = CcaClaimLine

    def render(self, line: CcaClaimLine) -> str:
        """The English sentence for `line`."""
        output = line.output
        position = line.position
        class_rate = line.class_rate
        column_7 = line.column_7
        column_14 = line.column_14
        column_15 = line.column_15
        column_16 = line.column_16
        column_17 = line.column_17
        column_18 = line.column_18
        column_19 = line.column_19
        zero_reason = line.zero_reason
        maximum = line.maximum
        rule = line.rounding
        claim = line.claim
        columns = ", ".join(
            f"column {number} {EnglishFigures.money(amount)}"
            for number, amount in (
                (7, column_7),
                (14, column_14),
                (15, column_15),
                (16, column_16),
                (17, column_17),
                (18, column_18),
                (19, column_19),
            )
        )
        if zero_reason is CcaZeroReason.COLUMN_7_NEGATIVE:
            available = "maximum 0 as column 7 is negative"
        elif zero_reason is CcaZeroReason.NO_PROPERTY_LEFT:
            available = "maximum 0 as no property is left in the class"
        else:
            available = (
                f"maximum {EnglishFigures.percent(class_rate.rate.value)}% of column 19 = "
                f"{EnglishFigures.money(maximum)} ({EnglishFigures.rounding(rule)})"
            )
        return (
            f"{EnglishFigures.cca_class(output.label, position, class_rate)}: {columns}, "
            f"{available}, claim {EnglishFigures.money(claim)}"
        )


@english_renderer
class RecapturedCcaRenderer:
    """English text for RecapturedCcaLine."""

    line_class = RecapturedCcaLine

    def render(self, line: RecapturedCcaLine) -> str:
        """The English sentence for `line`."""
        output = line.output
        position = line.position
        class_rate = line.class_rate
        column_7 = line.column_7
        zero_reason = line.zero_reason
        result = line.result
        if zero_reason is not CcaZeroReason.COLUMN_7_NEGATIVE:
            found = f"column 7 {EnglishFigures.money(column_7)} is not negative"
        elif class_rate.recapture_and_terminal_loss is RecaptureAndTerminalLoss.EXCLUDED:
            found = (
                f"column 7 {EnglishFigures.money(column_7)} is negative, but recapture does not "
                f"apply to class {EnglishFigures.money(class_rate.class_number)}"
            )
        else:
            found = f"column 7 {EnglishFigures.money(column_7)} is negative"
        return (
            f"{EnglishFigures.cca_class(output.label, position, class_rate)}: {found}: "
            f"recapture {EnglishFigures.money(result)}"
        )


@english_renderer
class TerminalLossRenderer:
    """English text for TerminalLossLine."""

    line_class = TerminalLossLine

    def render(self, line: TerminalLossLine) -> str:
        """The English sentence for `line`."""
        output = line.output
        position = line.position
        class_rate = line.class_rate
        column_7 = line.column_7
        zero_reason = line.zero_reason
        column_7_positive = line.column_7_positive
        result = line.result
        if zero_reason is CcaZeroReason.NO_PROPERTY_LEFT:
            if class_rate.recapture_and_terminal_loss is RecaptureAndTerminalLoss.EXCLUDED:
                found = (
                    f"column 7 {EnglishFigures.money(column_7)} with no property left, but a "
                    f"terminal loss does not apply to class "
                    f"{EnglishFigures.money(class_rate.class_number)}"
                )
            else:
                found = f"column 7 {EnglishFigures.money(column_7)} with no property left"
        elif zero_reason is CcaZeroReason.NONE and column_7_positive:
            found = f"column 7 {EnglishFigures.money(column_7)} with property left"
        else:
            found = f"column 7 {EnglishFigures.money(column_7)} is not positive"
        return (
            f"{EnglishFigures.cca_class(output.label, position, class_rate)}: {found}: "
            f"terminal loss {EnglishFigures.money(result)}"
        )


@english_renderer
class ClosingUccRenderer:
    """English text for ClosingUccLine."""

    line_class = ClosingUccLine

    def render(self, line: ClosingUccLine) -> str:
        """The English sentence for `line`."""
        output = line.output
        position = line.position
        class_rate = line.class_rate
        column_7 = line.column_7
        zero_reason = line.zero_reason
        claim = line.claim
        result = line.result
        if zero_reason is CcaZeroReason.COLUMN_7_NEGATIVE:
            found = f"column 7 {EnglishFigures.money(column_7)} is negative:"
        elif zero_reason is CcaZeroReason.NO_PROPERTY_LEFT:
            found = f"column 7 {EnglishFigures.money(column_7)} with no property left:"
        else:
            found = (
                f"column 7 {EnglishFigures.money(column_7)} less claim "
                f"{EnglishFigures.money(claim)} ="
            )
        return (
            f"{EnglishFigures.cca_class(output.label, position, class_rate)}: {found} "
            f"{EnglishFigures.money(result)}"
        )
