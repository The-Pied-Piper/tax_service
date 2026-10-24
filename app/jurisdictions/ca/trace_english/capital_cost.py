"""English text for the trace lines of `app.jurisdictions.ca.trace.capital_cost`: one
renderer class per line class, each registered with `@english_renderer`.
"""

from __future__ import annotations

from fractions import Fraction as ExactFraction

from app.adapters.inbound.trace_english.figures import EnglishFigures
from app.adapters.inbound.trace_english.registry import english_renderer
from app.domain.parameters.class_rates import RecaptureAndTerminalLoss
from app.jurisdictions.ca.trace.capital_cost import (
    CcaClaimLine,
    CcaVehicleProceedsLine,
    CcaZeroReason,
    ClosingUccLine,
    FiscalPeriodDaysLine,
    ImmediateExpensingLine,
    ProratedByDaysLine,
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
        column_9 = line.column_9
        on_sale = " (half-year rule on sale)" if line.half_year_rule_on_sale else ""
        columns = ", ".join(
            f"column {number} {EnglishFigures.money(amount)}{note}"
            for number, amount, note in (
                (7, column_7, ""),
                *(((9, column_9, ""),) if column_9 > 0 else ()),
                (14, column_14, ""),
                (15, column_15, ""),
                (16, column_16, ""),
                (17, column_17, ""),
                (18, column_18, ""),
                (19, column_19, on_sale),
            )
        )
        if zero_reason is CcaZeroReason.COLUMN_7_NEGATIVE and not line.half_year_rule_on_sale:
            available = "maximum 0 as column 7 is negative"
        elif zero_reason is CcaZeroReason.NO_PROPERTY_LEFT:
            available = "maximum 0 as no property is left in the class"
        else:
            percent = EnglishFigures.percent(class_rate.rate.value)
            rate_of_column_19 = column_19 * class_rate.rate.value
            days = line.fiscal_period_days
            full_year = line.full_year_days
            reached = maximum
            if days != full_year:
                # The rate of column 19 as worked, before the proration.
                reached = rule.apply(rate_of_column_19)
            available = (
                f"maximum {percent}% of column 19 = {EnglishFigures.money(reached)} "
                f"({EnglishFigures.rounding(rule)})"
            )
            if days != full_year:
                reached = rule.apply(ExactFraction(rate_of_column_19) * days / full_year)
                available += f", prorated {days}/{full_year} = {EnglishFigures.money(reached)}"
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
        elif (
            class_rate.recapture_and_terminal_loss is RecaptureAndTerminalLoss.EXCLUDED
            and not line.has_diep
        ):
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
        column_9 = line.column_9
        result = line.result
        if line.half_year_rule_on_sale:
            found = (
                f"column 7 {EnglishFigures.money(column_7)} with no property left, but a terminal "
                f"loss does not apply to class {EnglishFigures.money(class_rate.class_number)} "
                f"(half-year rule on sale used)"
            )
        elif zero_reason is CcaZeroReason.NO_PROPERTY_LEFT:
            expensed = f" less column 9 {EnglishFigures.money(column_9)}" if column_9 > 0 else ""
            if (
                class_rate.recapture_and_terminal_loss is RecaptureAndTerminalLoss.EXCLUDED
                and not line.has_diep
            ):
                found = (
                    f"column 7 {EnglishFigures.money(column_7)}{expensed} with no property left, "
                    f"but a terminal loss does not apply to class "
                    f"{EnglishFigures.money(class_rate.class_number)}"
                )
            else:
                found = f"column 7 {EnglishFigures.money(column_7)}{expensed} with no property left"
        elif zero_reason is CcaZeroReason.NONE and column_7_positive:
            found = f"column 7 {EnglishFigures.money(column_7)} with property left"
        else:
            found = f"column 7 {EnglishFigures.money(column_7)} is not positive"
        return (
            f"{EnglishFigures.cca_class(output.label, position, class_rate)}: {found}: "
            f"terminal loss {EnglishFigures.money(result)}"
        )


@english_renderer
class CcaVehicleProceedsRenderer:
    """English text for CcaVehicleProceedsLine."""

    line_class = CcaVehicleProceedsLine

    def render(self, line: CcaVehicleProceedsLine) -> str:
        """The English sentence for `line`."""
        start = f"{line.output.label}: item {line.position}: "
        proceeds = (
            f"proceeds {EnglishFigures.money(line.proceeds)} and DIEP proceeds "
            f"{EnglishFigures.money(line.diep_proceeds)}"
        )
        if not line.applied:
            return f"{start}{proceeds} not adjusted"
        return (
            f"{start}{proceeds} adjusted by prescribed amount "
            f"{EnglishFigures.money(line.prescribed_amount)} / actual cost "
            f"{EnglishFigures.money(line.actual_cost)} = proceeds "
            f"{EnglishFigures.money(line.adjusted_proceeds)} and DIEP proceeds "
            f"{EnglishFigures.money(line.adjusted_diep_proceeds)}"
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
        column_9 = line.column_9
        on_sale = " (half-year rule on sale)" if line.half_year_rule_on_sale else ""
        if line.half_year_rule_on_sale:
            found = (
                f"column 7 {EnglishFigures.money(column_7)} less claim "
                f"{EnglishFigures.money(claim)}{on_sale}, the rest is not deductible later:"
            )
        elif zero_reason is CcaZeroReason.COLUMN_7_NEGATIVE:
            found = f"column 7 {EnglishFigures.money(column_7)} is negative:"
        elif zero_reason is CcaZeroReason.NO_PROPERTY_LEFT:
            found = f"column 7 {EnglishFigures.money(column_7)} with no property left:"
        else:
            including = (
                f" (including column 9 {EnglishFigures.money(column_9)})" if column_9 > 0 else ""
            )
            prorated = (
                f" (prorated {line.fiscal_period_days}/{line.full_year_days})"
                if line.fiscal_period_days != line.full_year_days
                else ""
            )
            part = (
                f" less personal part {EnglishFigures.money(line.personal_part_remaining)}"
                if line.personal_part_remaining > 0
                else ""
            )
            found = (
                f"column 7 {EnglishFigures.money(column_7)} less claim "
                f"{EnglishFigures.money(claim)}{on_sale}{prorated}{including}{part} ="
            )
        return (
            f"{EnglishFigures.cca_class(output.label, position, class_rate)}: {found} "
            f"{EnglishFigures.money(result)}"
        )


@english_renderer
class ImmediateExpensingRenderer:
    """English text for ImmediateExpensingLine."""

    line_class = ImmediateExpensingLine

    def render(self, line: ImmediateExpensingLine) -> str:
        """The English sentence for `line`."""
        return (
            f"{EnglishFigures.cca_class(line.output.label, line.position, line.class_rate)}: "
            f"column 4 {EnglishFigures.money(line.column_4)} less column 6 "
            f"{EnglishFigures.money(line.column_6)}, column 7 "
            f"{EnglishFigures.money(line.column_7)}: "
            f"column 8 {EnglishFigures.money(line.column_8)}, column 9 "
            f"{EnglishFigures.money(line.column_9)}"
        )


@english_renderer
class FiscalPeriodDaysRenderer:
    """English text for FiscalPeriodDaysLine."""

    line_class = FiscalPeriodDaysLine

    def render(self, line: FiscalPeriodDaysLine) -> str:
        """The English sentence for `line`."""
        found = (
            f"a full year of {line.full_year_days} days"
            if line.entered == 0
            else f"fiscal period {line.fiscal_period_days} days"
        )
        return f"{line.output.label}: entered {line.entered}, {found}"


@english_renderer
class ProratedByDaysRenderer:
    """English text for ProratedByDaysLine."""

    line_class = ProratedByDaysLine

    def render(self, line: ProratedByDaysLine) -> str:
        """The English sentence for `line`."""
        return (
            f"{line.output.label}: {line.amount_kind.label} "
            f"{EnglishFigures.money(line.amount_value)} × {line.days_kind.label} "
            f"{line.fiscal_period_days} / {line.full_year_days} = "
            f"{EnglishFigures.money(line.result)}"
        )
