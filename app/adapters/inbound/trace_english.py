"""English rendering of the structured trace: one readable sentence per trace line.

The domain records facts; this adapter turns them into the text a reader sees, line by line, like
the tax authority's own worksheet. Other languages get their own renderer class.
"""

from __future__ import annotations

import decimal
from collections.abc import Iterable
from decimal import Decimal
from fractions import Fraction as ExactFraction

from app.domain.parameters.rounding import NO_ROUNDING, RoundingRule, RoundTo
from app.domain.trace import (
    AtMostLine,
    BracketColumnLine,
    CappedAmountLine,
    ChosenByCountLine,
    ChosenByRangeLine,
    ContributionTierLine,
    CreditAmountLine,
    FractionAppliedLine,
    LesserOfLine,
    MultipleOverLine,
    PerUnitAmountLine,
    RateAppliedLine,
    RecordTotalLine,
    RoundedTotalLine,
    SubtractedLine,
    SubtractedNotBelowZeroLine,
    SumLine,
    SurchargeTierLine,
    TaperedAmountLine,
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
        raise TypeError(f"no English rendering for trace line {type(line).__name__}")

    def render_all(self, trace: Iterable[TraceLine]) -> tuple[str, ...]:
        """The English sentence for each line of `trace`, in order."""
        return tuple(self.render(line) for line in trace)

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
