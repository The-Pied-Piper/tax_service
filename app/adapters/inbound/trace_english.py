"""English rendering of the structured trace: one readable sentence per trace line.

The domain records facts; this adapter turns them into the text a reader sees, line by line, like
the tax authority's own worksheet. Other languages get their own renderer class.
"""

from __future__ import annotations

from collections.abc import Iterable
from decimal import Decimal

from app.domain.parameters.rounding import NO_ROUNDING, RoundingRule, RoundTo
from app.domain.trace import (
    BracketSliceLine,
    CreditAppliedLine,
    CreditLine,
    RateAppliedLine,
    RoundedTotalLine,
    SubtractedLine,
    SumLine,
    TraceLine,
    UnusedCreditLine,
)


class EnglishTraceRenderer:
    """Renders trace lines as English text."""

    def render(self, line: TraceLine) -> str:
        """The English sentence for `line`; raises TypeError for a line class it does not know."""
        match line:
            case BracketSliceLine(lower=lower, upper=None, rate=rate, taxed=taxed):
                return f"{self._percent(rate)}% on {taxed} (over {lower})"
            case BracketSliceLine(lower=lower, upper=upper, rate=rate, taxed=taxed):
                return f"{self._percent(rate)}% on {taxed} ({lower} to {upper})"
            case RoundedTotalLine(output=output, base=base, base_amount=amount, rounding=rule):
                return f"{output.label} on {base.label} {amount} ({self._rounding(rule)})"
            case CreditLine(basis=basis, rate=rate, rounding=rule):
                return (
                    f"credit: {self._percent(rate.value)}% of {basis.amount} "
                    f"({self._rounding(rule)})"
                )
            case CreditAppliedLine(output=output, tax=tax, tax_amount=amount):
                return f"{output.label}: {tax.label} {amount} less credit, not below 0"
            case UnusedCreditLine():
                return "unused credit, not refunded"
            case SumLine(output=output, parts=parts, total=total):
                terms = " + ".join(f"{kind.label} {amount}" for kind, amount in parts)
                return f"{output.label}: {terms or 'no parts'} = {total}"
            case RateAppliedLine(
                output=output, base=base, base_amount=amount, rate=rate, rounding=rule
            ):
                return (
                    f"{output.label}: {self._percent(rate.value)}% of {base.label} {amount} "
                    f"({self._rounding(rule)})"
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
                    f"{output.label}: {minuend.label} {minuend_amount} "
                    f"less {subtrahend.label} {subtrahend_amount} = {result}"
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
    def _rounding(rule: RoundingRule) -> str:
        """How `rule` rounds, e.g. "no rounding" or "half-up to 0.01"."""
        if rule == NO_ROUNDING:
            return "no rounding"
        if isinstance(rule, RoundTo):
            return f"{rule.mode.value.replace('_', '-')} to {rule.increment}"
        raise TypeError(f"no English rendering for rounding rule {type(rule).__name__}")
