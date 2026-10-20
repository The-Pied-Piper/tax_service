"""English rendering of the structured trace: one readable sentence per trace line.

The domain records facts; this adapter turns them into the text a reader sees, line by line, like
the tax authority's own worksheet. Other languages get their own renderer class.
"""

from __future__ import annotations

import decimal
from collections.abc import Iterable
from decimal import Decimal
from fractions import Fraction as ExactFraction

from app.domain.parameters.class_rates import ClassRate, RecaptureAndTerminalLoss
from app.domain.parameters.rounding import NO_ROUNDING, RoundingRule, RoundTo
from app.domain.trace import (
    AtMostLine,
    BracketColumnLine,
    CappedAmountLine,
    CaregiverClaimLessClaimedLine,
    CaregiverClaimLine,
    CcaClaimLine,
    CcaZeroReason,
    ChosenByCountLine,
    ChosenByRangeLine,
    ChosenRateAppliedLine,
    ClosingUccLine,
    ContributionTierLine,
    CreditAmountLine,
    DisabilityTransferLine,
    FractionAppliedLine,
    GreaterOfLine,
    ItemsTotalLine,
    LesserOfLine,
    MultipleOverLine,
    OtherDependantMedicalLine,
    PerUnitAmountLine,
    PlacementCreditLine,
    PrincipalResidenceGainLine,
    QuotientLine,
    RateAppliedLine,
    RateByIncomeBandLine,
    RecapturedCcaLine,
    RecordCountLine,
    RecordTotalLine,
    RoundedTotalLine,
    ShortTermRentalNonCompliantLine,
    SubtractedLine,
    SubtractedNotBelowZeroLine,
    SumLine,
    SurchargeTierLine,
    TaperedAmountLine,
    TerminalLossLine,
    ThresholdGateLine,
    TimesCountLine,
    TraceLine,
)


class EnglishTraceRenderer:
    """Renders trace lines as English text."""

    def render(self, line: TraceLine) -> str:
        """The English sentence for `line`; raises TypeError for a line class it does not know."""
        match line:
            case BracketColumnLine(
                lower=lower, rate=rate, excess=excess, tax_at_start=tax_at_start
            ):
                return (
                    f"{self._percent(rate)}% on {self._money(excess)} "
                    f"over {self._money(lower)} plus {self._money(tax_at_start)}"
                )
            case RoundedTotalLine(output=output, base=base, base_amount=amount, rounding=rule):
                return (
                    f"{output.label} on {base.label} {self._money(amount)} ({self._rounding(rule)})"
                )
            case CreditAmountLine(output=output, basis=basis, rounding=rule):
                return (
                    f"{output.label}: credit amount {self._money(basis.amount)} "
                    f"({self._rounding(rule)})"
                )
            case SumLine(output=output, parts=parts, total=total):
                terms = " + ".join(f"{kind.label} {self._money(amount)}" for kind, amount in parts)
                return f"{output.label}: {terms or 'no parts'} = {self._money(total)}"
            case RateAppliedLine(
                output=output, base=base, base_amount=amount, rate=rate, rounding=rule
            ):
                return (
                    f"{output.label}: {self._percent(rate.value)}% of {base.label} "
                    f"{self._money(amount)} ({self._rounding(rule)})"
                )
            case SubtractedNotBelowZeroLine(
                output=output,
                minuend=minuend,
                minuend_amount=minuend_amount,
                subtrahend=subtrahend,
                subtrahend_amount=subtrahend_amount,
                result=result,
            ):
                return (
                    f"{output.label}: {minuend.label} {self._money(minuend_amount)} "
                    f"less {subtrahend.label} {self._money(subtrahend_amount)}, "
                    f"not below 0 = {self._money(result)}"
                )
            case SubtractedLine(
                output=output,
                minuend=minuend,
                minuend_amount=minuend_amount,
                subtrahend=subtrahend,
                subtrahend_amount=subtrahend_amount,
                result=result,
            ):
                return (
                    f"{output.label}: {minuend.label} {self._money(minuend_amount)} "
                    f"less {subtrahend.label} {self._money(subtrahend_amount)} "
                    f"= {self._money(result)}"
                )
            case CappedAmountLine(
                output=output, base=base, base_amount=amount, cap=cap, rounding=rule
            ):
                return (
                    f"{output.label}: lesser of {base.label} {self._money(amount)} "
                    f"and {self._money(cap.value)} ({self._rounding(rule)})"
                )
            case LesserOfLine(output=output, parts=parts, result=result):
                terms = " and ".join(
                    f"{kind.label} {self._money(amount)}" for kind, amount in parts
                )
                return f"{output.label}: lesser of {terms} = {self._money(result)}"
            case GreaterOfLine(output=output, parts=parts, result=result):
                terms = " and ".join(
                    f"{kind.label} {self._money(amount)}" for kind, amount in parts
                )
                return f"{output.label}: greater of {terms} = {self._money(result)}"
            case ContributionTierLine(
                output=output,
                earnings=earnings,
                tier=tier,
                rounding=rule,
                contributory=contributory,
            ):
                return (
                    f"{output.label}: {self._percent(tier.rate.value)}% of {earnings.label} "
                    f"between {self._money(tier.lower)} and {self._money(tier.upper)} "
                    f"({self._money(contributory)}), "
                    f"at most {self._money(tier.maximum)} ({self._rounding(rule)})"
                )
            case SurchargeTierLine(
                output=output,
                base=base,
                base_amount=amount,
                threshold=threshold,
                rate=rate,
                rounding=rule,
                maximum=maximum,
            ):
                at_most = "" if maximum is None else f", at most {self._money(maximum)}"
                return (
                    f"{output.label}: {self._percent(rate.value)}% of {base.label} "
                    f"{self._money(amount)} over {self._money(threshold)}{at_most} "
                    f"({self._rounding(rule)})"
                )
            case TaperedAmountLine(
                output=output,
                base=base,
                base_amount=amount,
                taper=taper,
                rounding=rule,
                reduction=reduction,
            ):
                return (
                    f"{output.label}: {self._money(taper.base)} "
                    f"plus {self._money(taper.supplement)} less {self._exact(reduction)} "
                    f"for {base.label} {self._money(amount)} "
                    f"over {self._money(taper.threshold)} (range {self._money(taper.range)}), "
                    f"not below {self._money(taper.base)} ({self._rounding(rule)})"
                )
            case PerUnitAmountLine(
                output=output,
                count_kind=count_kind,
                count=count,
                per_unit=per_unit,
                rounding=rule,
                result=result,
            ):
                return (
                    f"{output.label}: {self._money(per_unit.value)} for each of {count} "
                    f"{count_kind.label} = {self._money(result)} ({self._rounding(rule)})"
                )
            case MultipleOverLine(
                output=output,
                base=base,
                base_amount=amount,
                factor=factor,
                less=less,
                less_amount=less_amount,
                rounding=rule,
            ):
                return (
                    f"{output.label}: {self._money(factor.value)} × {base.label} "
                    f"{self._money(amount)} over {less.label} {self._money(less_amount)}, "
                    f"not below 0 ({self._rounding(rule)})"
                )
            case AtMostLine(
                output=output,
                amount_kind=amount_kind,
                amount_value=amount,
                bound=bound,
                bound_value=bound_value,
            ):
                return (
                    f"{output.label}: {amount_kind.label} {self._money(amount)}, "
                    f"at most {bound.label} {self._money(bound_value)}"
                )
            case ThresholdGateLine(
                output=output,
                amount_kind=amount_kind,
                amount_value=amount,
                gate_kind=gate_kind,
                gate_value=gate_value,
                threshold=threshold,
                rounding=rule,
                result=result,
            ):
                return (
                    f"{output.label}: {amount_kind.label} {self._money(amount)} "
                    f"if {gate_kind.label} {self._money(gate_value)} is at least "
                    f"{self._money(threshold.value)} ({self._rounding(rule)}) = "
                    f"{self._money(result)}"
                )
            case FractionAppliedLine(
                output=output, base=base, base_amount=amount, fraction=fraction, rounding=rule
            ):
                return (
                    f"{output.label}: {fraction.numerator}/{fraction.denominator} of {base.label} "
                    f"{self._money(amount)} ({self._rounding(rule)})"
                )
            case TimesCountLine(
                output=output,
                amount_kind=amount_kind,
                amount_value=amount,
                count_kind=count_kind,
                count=count,
                result=result,
            ):
                return (
                    f"{output.label}: {amount_kind.label} {self._money(amount)} for each of "
                    f"{count} {count_kind.label} = {self._money(result)}"
                )
            case ChosenByCountLine(
                output=output,
                count_kind=count_kind,
                count=count,
                chosen_kind=chosen_kind,
                chosen_value=chosen,
            ):
                return (
                    f"{output.label}: {chosen_kind.label} {self._money(chosen)}, "
                    f"chosen as {count_kind.label} is {count}"
                )
            case RecordTotalLine(output=output, field=field, amounts=amounts, total=total):
                items = " + ".join(
                    f"item {position} {field.label} {self._money(amount)}"
                    for position, amount in enumerate(amounts, start=1)
                )
                return f"{output.label}: {items or 'no items'} = {self._money(total)}"
            case ChosenByRangeLine(
                output=output,
                tested_kind=tested_kind,
                tested_value=tested,
                chosen_kind=chosen_kind,
                chosen_value=chosen,
            ):
                return (
                    f"{output.label}: {chosen_kind.label} {self._money(chosen)}, "
                    f"chosen as {tested_kind.label} is {self._money(tested)}"
                )
            case RateByIncomeBandLine(
                output=output, income=income, income_amount=amount, row=row, rate=rate
            ):
                if row is None:
                    band = "which is 0"
                elif row.not_more_than is None:
                    band = f"more than {self._money(row.more_than)}"
                else:
                    band = (
                        f"more than {self._money(row.more_than)} "
                        f"but not more than {self._money(row.not_more_than)}"
                    )
                return (
                    f"{output.label}: {income.label} {self._money(amount)}, "
                    f"{band}: {self._percent(rate.value)}%"
                )
            case ChosenRateAppliedLine(
                output=output,
                base=base,
                base_amount=amount,
                rate_kind=rate_kind,
                rate=rate,
                rounding=rule,
            ):
                return (
                    f"{output.label}: {rate_kind.label} {self._percent(rate.value)}% of "
                    f"{base.label} {self._money(amount)} ({self._rounding(rule)})"
                )
            case CaregiverClaimLine(
                output=output,
                position=position,
                base=base,
                net_income=net_income,
                maximum=maximum,
                rounding=rule,
                result=result,
            ):
                return (
                    f"{output.label}: dependant {position}: {self._money(base.value)} less net "
                    f"income {self._money(net_income)}, at most {self._money(maximum.value)} = "
                    f"{self._money(result)} ({self._rounding(rule)})"
                )
            case OtherDependantMedicalLine(
                output=output,
                position=position,
                expenses=expenses,
                net_income=net_income,
                reduction=reduction,
                rounding=rule,
                result=result,
            ):
                at_most = (
                    ""
                    if reduction.maximum is None
                    else f", at most {self._money(reduction.maximum)}"
                )
                return (
                    f"{output.label}: dependant {position}: expenses {self._money(expenses)} "
                    f"less the lesser of {self._percent(reduction.rate.value)}% of net income "
                    f"{self._money(net_income)} and {self._money(reduction.ceiling)} = "
                    f"{self._money(result)}{at_most} ({self._rounding(rule)})"
                )
            case ShortTermRentalNonCompliantLine(
                output=output,
                position=position,
                related_expenses=related_expenses,
                non_compliant_days=non_compliant_days,
                days=days,
                rounding=rule,
                result=result,
            ):
                return (
                    f"{output.label}: row {position}: expenses {self._money(related_expenses)} "
                    f"for {non_compliant_days} non-compliant days of {days} short-term days = "
                    f"{self._money(result)} ({self._rounding(rule)})"
                )
            case CaregiverClaimLessClaimedLine(
                output=output,
                position=position,
                base=base,
                net_income=net_income,
                maximum=maximum,
                allowable_before_claimed=allowable,
                claimed=claimed,
                rounding=rule,
                result=result,
            ):
                return (
                    f"{output.label}: dependant {position}: {self._money(base.value)} less net "
                    f"income {self._money(net_income)}, at most {self._money(maximum.value)} = "
                    f"{self._money(allowable)}, less claimed {self._money(claimed)} = "
                    f"{self._money(result)} ({self._rounding(rule)})"
                )
            case DisabilityTransferLine(
                output=output,
                position=position,
                base=base,
                supplement=supplement,
                threshold=threshold,
                maximum=maximum,
                under_18=under_18,
                care_expenses=care_expenses,
                line_5=line_5,
                line_6=line_6,
                line_7=line_7,
                line_8=line_8,
                credit_amounts=credit_amounts,
                taxable_income=taxable_income,
                line_12=line_12,
                rounding=rule,
                result=result,
            ):
                steps = []
                if under_18:
                    steps.append(
                        f"care expenses {self._money(care_expenses)} less threshold "
                        f"{self._money(threshold.value)} = {self._money(line_5)}"
                    )
                    steps.append(
                        f"supplement {self._money(supplement.value)} less {self._money(line_5)} "
                        f"= {self._money(line_6)}"
                    )
                steps.append(
                    f"base {self._money(base.value)} + {self._money(line_7)}, at most "
                    f"{self._money(maximum.value)} = {self._money(line_8)}"
                )
                steps.append(
                    f"{self._money(line_8)} + credit amounts {self._money(credit_amounts)} less "
                    f"taxable income {self._money(taxable_income)} = {self._money(line_12)}"
                )
                steps.append(
                    f"the lesser of {self._money(line_8)} and {self._money(line_12)} = "
                    f"{self._money(result)} ({self._rounding(rule)})"
                )
                age = "under 18" if under_18 else "18 or older"
                return f"{output.label}: dependant {position}: {age}: {'; '.join(steps)}"
            case PrincipalResidenceGainLine(
                output=output,
                position=position,
                designated=designated,
                owned=owned,
                plus_one=plus_one,
                proceeds=proceeds,
                adjusted_cost_base=cost_base,
                outlays=outlays,
                gain=gain,
                exempt=exempt,
                rounding=rule,
                result=result,
            ):
                return (
                    f"{output.label}: property {position}: gain {self._money(gain)} = proceeds "
                    f"{self._money(proceeds)} less adjusted cost base {self._money(cost_base)} "
                    f"less outlays {self._money(outlays)}; exempt {self._money(exempt)} = "
                    f"{self._money(gain)} × ({designated} designated + {plus_one}) ÷ {owned} "
                    f"owned ({self._rounding(rule)}); taxable gain {self._money(result)} = "
                    f"{self._money(gain)} less {self._money(exempt)}, not below 0"
                )
            case QuotientLine(
                output=output,
                dividend=dividend,
                dividend_amount=dividend_amount,
                divisor=divisor,
                divisor_amount=divisor_amount,
                result=result,
            ):
                return (
                    f"{output.label}: {dividend.label} {self._money(dividend_amount)} "
                    f"divided by {divisor.label} {self._money(divisor_amount)} "
                    f"= {self._money(result)}"
                )
            case RecordCountLine(output=output, records=records, count=count):
                noun = "item" if count == 1 else "items"
                counted = "no items" if count == 0 else f"{count} {noun}"
                return f"{output.label}: {counted} in {records.label} = {count}"
            case PlacementCreditLine(
                output=output,
                position=position,
                field=field,
                expenditure=expenditure,
                line_1=line_1,
                line_3=line_3,
                line_12=line_12,
                line_13=line_13,
                rounding=rule,
            ):
                return (
                    f"{output.label}: item {position} {field.label} {self._money(expenditure)}: "
                    f"line 1 {self._money(line_1)}, line 3 {self._money(line_3)}, "
                    f"line 12 {self._money(line_12)}, line 13 {self._money(line_13)} "
                    f"({self._rounding(rule)})"
                )
            case CcaClaimLine(
                output=output,
                position=position,
                class_rate=class_rate,
                column_7=column_7,
                column_14=column_14,
                column_15=column_15,
                column_16=column_16,
                column_17=column_17,
                column_18=column_18,
                column_19=column_19,
                zero_reason=zero_reason,
                maximum=maximum,
                rounding=rule,
                claim=claim,
            ):
                columns = ", ".join(
                    f"column {number} {self._money(amount)}"
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
                        f"maximum {self._percent(class_rate.rate.value)}% of column 19 = "
                        f"{self._money(maximum)} ({self._rounding(rule)})"
                    )
                return (
                    f"{self._cca_class(output.label, position, class_rate)}: {columns}, "
                    f"{available}, claim {self._money(claim)}"
                )
            case RecapturedCcaLine(
                output=output,
                position=position,
                class_rate=class_rate,
                column_7=column_7,
                zero_reason=zero_reason,
                result=result,
            ):
                if zero_reason is not CcaZeroReason.COLUMN_7_NEGATIVE:
                    found = f"column 7 {self._money(column_7)} is not negative"
                elif class_rate.recapture_and_terminal_loss is RecaptureAndTerminalLoss.EXCLUDED:
                    found = (
                        f"column 7 {self._money(column_7)} is negative, but recapture does not "
                        f"apply to class {self._money(class_rate.class_number)}"
                    )
                else:
                    found = f"column 7 {self._money(column_7)} is negative"
                return (
                    f"{self._cca_class(output.label, position, class_rate)}: {found}: "
                    f"recapture {self._money(result)}"
                )
            case TerminalLossLine(
                output=output,
                position=position,
                class_rate=class_rate,
                column_7=column_7,
                zero_reason=zero_reason,
                column_7_positive=column_7_positive,
                result=result,
            ):
                if zero_reason is CcaZeroReason.NO_PROPERTY_LEFT:
                    if class_rate.recapture_and_terminal_loss is RecaptureAndTerminalLoss.EXCLUDED:
                        found = (
                            f"column 7 {self._money(column_7)} with no property left, but a "
                            f"terminal loss does not apply to class "
                            f"{self._money(class_rate.class_number)}"
                        )
                    else:
                        found = f"column 7 {self._money(column_7)} with no property left"
                elif zero_reason is CcaZeroReason.NONE and column_7_positive:
                    found = f"column 7 {self._money(column_7)} with property left"
                else:
                    found = f"column 7 {self._money(column_7)} is not positive"
                return (
                    f"{self._cca_class(output.label, position, class_rate)}: {found}: "
                    f"terminal loss {self._money(result)}"
                )
            case ClosingUccLine(
                output=output,
                position=position,
                class_rate=class_rate,
                column_7=column_7,
                zero_reason=zero_reason,
                claim=claim,
                result=result,
            ):
                if zero_reason is CcaZeroReason.COLUMN_7_NEGATIVE:
                    found = f"column 7 {self._money(column_7)} is negative:"
                elif zero_reason is CcaZeroReason.NO_PROPERTY_LEFT:
                    found = f"column 7 {self._money(column_7)} with no property left:"
                else:
                    found = f"column 7 {self._money(column_7)} less claim {self._money(claim)} ="
                return (
                    f"{self._cca_class(output.label, position, class_rate)}: {found} "
                    f"{self._money(result)}"
                )
            case ItemsTotalLine(output=output, items=items, total=total):
                terms = " + ".join(
                    f"item {position} {self._money(amount)}" for position, amount in items
                )
                return f"{output.label}: {terms or 'no items'} = {self._money(total)}"
        raise TypeError(f"no English rendering for trace line {type(line).__name__}")

    def render_all(self, trace: Iterable[TraceLine]) -> tuple[str, ...]:
        """The English sentence for each line of `trace`, in order."""
        return tuple(self.render(line) for line in trace)

    @classmethod
    def _cca_class(cls, label: str, position: int, class_rate: ClassRate) -> str:
        """The start of a CCA table line: its output, its item and its class number."""
        return f"{label}: item {position} class {cls._money(class_rate.class_number)}"

    @staticmethod
    def _percent(rate: Decimal) -> str:
        """`rate` as a plain percentage figure, e.g. 0.125 -> "12.5"."""
        return format((rate * 100).normalize(), "f")

    @staticmethod
    def _money(amount: Decimal) -> str:
        """`amount` as a plain figure without trailing zeros, e.g. 115000.00 -> "115000"."""
        text = format(amount, "f")  # fixed-point, every digit; never an exponent
        return text.rstrip("0").rstrip(".") if "." in text else text

    @staticmethod
    def _exact(amount: ExactFraction) -> str:
        """An exact fraction as a plain figure if it terminates, else "numerator/denominator"."""
        try:
            return EnglishTraceRenderer._money(NO_ROUNDING.apply(amount))
        except decimal.Inexact:
            return f"{amount.numerator}/{amount.denominator}"

    @staticmethod
    def _rounding(rule: RoundingRule) -> str:
        """How `rule` rounds, e.g. "no rounding" or "half-up to 0.01"."""
        if rule == NO_ROUNDING:
            return "no rounding"
        if isinstance(rule, RoundTo):
            return f"{rule.mode.value.replace('_', '-')} to {rule.increment}"
        raise TypeError(f"no English rendering for rounding rule {type(rule).__name__}")
