"""English text for the trace lines of `app.domain.trace.arithmetic`: one renderer class
per line class, each registered with `@english_renderer`.
"""

from __future__ import annotations

from app.adapters.inbound.trace_english.figures import EnglishFigures
from app.adapters.inbound.trace_english.registry import english_renderer
from app.domain.trace.arithmetic import (
    AmountOrDividedByRateLine,
    AtMostLine,
    CappedAmountLine,
    CreditAmountLine,
    FractionAppliedLine,
    GreaterOfLine,
    LesserOfLine,
    MultipleOverLine,
    PerUnitAmountLine,
    QuotientLine,
    RateAppliedLine,
    RatioAppliedLine,
    RoundedTotalLine,
    SubtractedLine,
    SubtractedNotBelowZeroLine,
    SumLine,
    SumNotBelowZeroLine,
    ThresholdGateLine,
    TimesCountLine,
)


@english_renderer
class RoundedTotalRenderer(EnglishFigures):
    """English text for RoundedTotalLine."""

    line_class = RoundedTotalLine

    def render(self, line: RoundedTotalLine) -> str:
        """The English sentence for `line`."""
        output = line.output
        base = line.base
        amount = line.base_amount
        rule = line.rounding
        return f"{output.label} on {base.label} {self._money(amount)} ({self._rounding(rule)})"


@english_renderer
class SumRenderer(EnglishFigures):
    """English text for SumLine."""

    line_class = SumLine

    def render(self, line: SumLine) -> str:
        """The English sentence for `line`."""
        output = line.output
        parts = line.parts
        total = line.total
        terms = " + ".join(f"{kind.label} {self._money(amount)}" for kind, amount in parts)
        return f"{output.label}: {terms or 'no parts'} = {self._money(total)}"


@english_renderer
class SumNotBelowZeroRenderer(EnglishFigures):
    """English text for SumNotBelowZeroLine."""

    line_class = SumNotBelowZeroLine

    def render(self, line: SumNotBelowZeroLine) -> str:
        """The English sentence for `line`."""
        output = line.output
        parts = line.parts
        total = line.total
        terms = " + ".join(f"{kind.label} {self._money(amount)}" for kind, amount in parts)
        return f"{output.label}: {terms or 'no parts'}, not below 0 = {self._money(total)}"


@english_renderer
class RateAppliedRenderer(EnglishFigures):
    """English text for RateAppliedLine."""

    line_class = RateAppliedLine

    def render(self, line: RateAppliedLine) -> str:
        """The English sentence for `line`."""
        output = line.output
        base = line.base
        amount = line.base_amount
        rate = line.rate
        rule = line.rounding
        return (
            f"{output.label}: {self._percent(rate.value)}% of {base.label} "
            f"{self._money(amount)} ({self._rounding(rule)})"
        )


@english_renderer
class SubtractedRenderer(EnglishFigures):
    """English text for SubtractedLine."""

    line_class = SubtractedLine

    def render(self, line: SubtractedLine) -> str:
        """The English sentence for `line`."""
        output = line.output
        minuend = line.minuend
        minuend_amount = line.minuend_amount
        subtrahend = line.subtrahend
        subtrahend_amount = line.subtrahend_amount
        result = line.result
        return (
            f"{output.label}: {minuend.label} {self._money(minuend_amount)} "
            f"less {subtrahend.label} {self._money(subtrahend_amount)} "
            f"= {self._money(result)}"
        )


@english_renderer
class SubtractedNotBelowZeroRenderer(EnglishFigures):
    """English text for SubtractedNotBelowZeroLine."""

    line_class = SubtractedNotBelowZeroLine

    def render(self, line: SubtractedNotBelowZeroLine) -> str:
        """The English sentence for `line`."""
        output = line.output
        minuend = line.minuend
        minuend_amount = line.minuend_amount
        subtrahend = line.subtrahend
        subtrahend_amount = line.subtrahend_amount
        result = line.result
        return (
            f"{output.label}: {minuend.label} {self._money(minuend_amount)} "
            f"less {subtrahend.label} {self._money(subtrahend_amount)}, "
            f"not below 0 = {self._money(result)}"
        )


@english_renderer
class CreditAmountRenderer(EnglishFigures):
    """English text for CreditAmountLine."""

    line_class = CreditAmountLine

    def render(self, line: CreditAmountLine) -> str:
        """The English sentence for `line`."""
        output = line.output
        basis = line.basis
        rule = line.rounding
        return f"{output.label}: credit amount {self._money(basis.amount)} ({self._rounding(rule)})"


@english_renderer
class CappedAmountRenderer(EnglishFigures):
    """English text for CappedAmountLine."""

    line_class = CappedAmountLine

    def render(self, line: CappedAmountLine) -> str:
        """The English sentence for `line`."""
        output = line.output
        base = line.base
        amount = line.base_amount
        cap = line.cap
        rule = line.rounding
        return (
            f"{output.label}: lesser of {base.label} {self._money(amount)} "
            f"and {self._money(cap.value)} ({self._rounding(rule)})"
        )


@english_renderer
class LesserOfRenderer(EnglishFigures):
    """English text for LesserOfLine."""

    line_class = LesserOfLine

    def render(self, line: LesserOfLine) -> str:
        """The English sentence for `line`."""
        output = line.output
        parts = line.parts
        result = line.result
        terms = " and ".join(f"{kind.label} {self._money(amount)}" for kind, amount in parts)
        return f"{output.label}: lesser of {terms} = {self._money(result)}"


@english_renderer
class GreaterOfRenderer(EnglishFigures):
    """English text for GreaterOfLine."""

    line_class = GreaterOfLine

    def render(self, line: GreaterOfLine) -> str:
        """The English sentence for `line`."""
        output = line.output
        parts = line.parts
        result = line.result
        terms = " and ".join(f"{kind.label} {self._money(amount)}" for kind, amount in parts)
        return f"{output.label}: greater of {terms} = {self._money(result)}"


@english_renderer
class PerUnitAmountRenderer(EnglishFigures):
    """English text for PerUnitAmountLine."""

    line_class = PerUnitAmountLine

    def render(self, line: PerUnitAmountLine) -> str:
        """The English sentence for `line`."""
        output = line.output
        count_kind = line.count_kind
        count = line.count
        per_unit = line.per_unit
        rule = line.rounding
        result = line.result
        return (
            f"{output.label}: {self._money(per_unit.value)} for each of {count} "
            f"{count_kind.label} = {self._money(result)} ({self._rounding(rule)})"
        )


@english_renderer
class MultipleOverRenderer(EnglishFigures):
    """English text for MultipleOverLine."""

    line_class = MultipleOverLine

    def render(self, line: MultipleOverLine) -> str:
        """The English sentence for `line`."""
        output = line.output
        base = line.base
        amount = line.base_amount
        factor = line.factor
        less = line.less
        less_amount = line.less_amount
        rule = line.rounding
        return (
            f"{output.label}: {self._money(factor.value)} × {base.label} "
            f"{self._money(amount)} over {less.label} {self._money(less_amount)}, "
            f"not below 0 ({self._rounding(rule)})"
        )


@english_renderer
class AtMostRenderer(EnglishFigures):
    """English text for AtMostLine."""

    line_class = AtMostLine

    def render(self, line: AtMostLine) -> str:
        """The English sentence for `line`."""
        output = line.output
        amount_kind = line.amount_kind
        amount = line.amount_value
        bound = line.bound
        bound_value = line.bound_value
        return (
            f"{output.label}: {amount_kind.label} {self._money(amount)}, "
            f"at most {bound.label} {self._money(bound_value)}"
        )


@english_renderer
class FractionAppliedRenderer(EnglishFigures):
    """English text for FractionAppliedLine."""

    line_class = FractionAppliedLine

    def render(self, line: FractionAppliedLine) -> str:
        """The English sentence for `line`."""
        output = line.output
        base = line.base
        amount = line.base_amount
        fraction = line.fraction
        rule = line.rounding
        return (
            f"{output.label}: {fraction.numerator}/{fraction.denominator} of {base.label} "
            f"{self._money(amount)} ({self._rounding(rule)})"
        )


@english_renderer
class RatioAppliedRenderer(EnglishFigures):
    """English text for RatioAppliedLine."""

    line_class = RatioAppliedLine

    def render(self, line: RatioAppliedLine) -> str:
        """The English sentence for `line`."""
        output = line.output
        amount_kind = line.amount_kind
        amount = line.amount_value
        numerator_kind = line.numerator_kind
        numerator = line.numerator_value
        denominator_kind = line.denominator_kind
        denominator = line.denominator_value
        rule = line.rounding
        return (
            f"{output.label}: {amount_kind.label} {self._money(amount)} × "
            f"{numerator_kind.label} {self._money(numerator)} / "
            f"{denominator_kind.label} {self._money(denominator)} ({self._rounding(rule)})"
        )


@english_renderer
class TimesCountRenderer(EnglishFigures):
    """English text for TimesCountLine."""

    line_class = TimesCountLine

    def render(self, line: TimesCountLine) -> str:
        """The English sentence for `line`."""
        output = line.output
        amount_kind = line.amount_kind
        amount = line.amount_value
        count_kind = line.count_kind
        count = line.count
        result = line.result
        return (
            f"{output.label}: {amount_kind.label} {self._money(amount)} for each of "
            f"{count} {count_kind.label} = {self._money(result)}"
        )


@english_renderer
class QuotientRenderer(EnglishFigures):
    """English text for QuotientLine."""

    line_class = QuotientLine

    def render(self, line: QuotientLine) -> str:
        """The English sentence for `line`."""
        output = line.output
        dividend = line.dividend
        dividend_amount = line.dividend_amount
        divisor = line.divisor
        divisor_amount = line.divisor_amount
        result = line.result
        return (
            f"{output.label}: {dividend.label} {self._money(dividend_amount)} "
            f"divided by {divisor.label} {self._money(divisor_amount)} "
            f"= {self._money(result)}"
        )


@english_renderer
class ThresholdGateRenderer(EnglishFigures):
    """English text for ThresholdGateLine."""

    line_class = ThresholdGateLine

    def render(self, line: ThresholdGateLine) -> str:
        """The English sentence for `line`."""
        output = line.output
        amount_kind = line.amount_kind
        amount = line.amount_value
        gate_kind = line.gate_kind
        gate_value = line.gate_value
        threshold = line.threshold
        rule = line.rounding
        result = line.result
        return (
            f"{output.label}: {amount_kind.label} {self._money(amount)} "
            f"if {gate_kind.label} {self._money(gate_value)} is at least "
            f"{self._money(threshold.value)} ({self._rounding(rule)}) = "
            f"{self._money(result)}"
        )


@english_renderer
class AmountOrDividedByRateRenderer(EnglishFigures):
    """English text for AmountOrDividedByRateLine."""

    line_class = AmountOrDividedByRateLine

    def render(self, line: AmountOrDividedByRateLine) -> str:
        """The English sentence for `line`."""
        output = line.output
        amount_kind = line.amount_kind
        amount_value = line.amount_value
        dividend_kind = line.dividend_kind
        dividend_value = line.dividend_value
        limit = line.limit
        rule = line.rounding
        result = line.result
        return (
            f"{output.label}: {amount_kind.label} {self._money(amount_value)} "
            f"if {self._money(limit.threshold)} or less, otherwise {dividend_kind.label} "
            f"{self._money(dividend_value)} divided by "
            f"{self._percent(limit.rate.value)}% ({self._rounding(rule)}) = "
            f"{self._money(result)}"
        )
