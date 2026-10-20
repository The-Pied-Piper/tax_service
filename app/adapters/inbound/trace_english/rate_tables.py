"""English text for the trace lines of `app.domain.trace.rate_tables`: one renderer class
per line class, each registered with `@english_renderer`.
"""

from __future__ import annotations

from app.adapters.inbound.trace_english.figures import EnglishFigures
from app.adapters.inbound.trace_english.registry import english_renderer
from app.domain.trace.rate_tables import (
    AmountByCountLine,
    BracketColumnLine,
    ChosenRateAppliedLine,
    ContributionTierLine,
    RateByIncomeBandLine,
    SurchargeTierLine,
    TaperedAmountLine,
)


@english_renderer
class BracketColumnRenderer(EnglishFigures):
    """English text for BracketColumnLine."""

    line_class = BracketColumnLine

    def render(self, line: BracketColumnLine) -> str:
        """The English sentence for `line`."""
        lower = line.lower
        rate = line.rate
        excess = line.excess
        tax_at_start = line.tax_at_start
        return (
            f"{self._percent(rate)}% on {self._money(excess)} "
            f"over {self._money(lower)} plus {self._money(tax_at_start)}"
        )


@english_renderer
class ContributionTierRenderer(EnglishFigures):
    """English text for ContributionTierLine."""

    line_class = ContributionTierLine

    def render(self, line: ContributionTierLine) -> str:
        """The English sentence for `line`."""
        output = line.output
        earnings = line.earnings
        tier = line.tier
        rule = line.rounding
        contributory = line.contributory
        return (
            f"{output.label}: {self._percent(tier.rate.value)}% of {earnings.label} "
            f"between {self._money(tier.lower)} and {self._money(tier.upper)} "
            f"({self._money(contributory)}), "
            f"at most {self._money(tier.maximum)} ({self._rounding(rule)})"
        )


@english_renderer
class SurchargeTierRenderer(EnglishFigures):
    """English text for SurchargeTierLine."""

    line_class = SurchargeTierLine

    def render(self, line: SurchargeTierLine) -> str:
        """The English sentence for `line`."""
        output = line.output
        base = line.base
        amount = line.base_amount
        threshold = line.threshold
        rate = line.rate
        rule = line.rounding
        maximum = line.maximum
        at_most = "" if maximum is None else f", at most {self._money(maximum)}"
        return (
            f"{output.label}: {self._percent(rate.value)}% of {base.label} "
            f"{self._money(amount)} over {self._money(threshold)}{at_most} "
            f"({self._rounding(rule)})"
        )


@english_renderer
class TaperedAmountRenderer(EnglishFigures):
    """English text for TaperedAmountLine."""

    line_class = TaperedAmountLine

    def render(self, line: TaperedAmountLine) -> str:
        """The English sentence for `line`."""
        output = line.output
        base = line.base
        amount = line.base_amount
        taper = line.taper
        rule = line.rounding
        reduction = line.reduction
        return (
            f"{output.label}: {self._money(taper.base)} "
            f"plus {self._money(taper.supplement)} less {self._exact(reduction)} "
            f"for {base.label} {self._money(amount)} "
            f"over {self._money(taper.threshold)} (range {self._money(taper.range)}), "
            f"not below {self._money(taper.base)} ({self._rounding(rule)})"
        )


@english_renderer
class RateByIncomeBandRenderer(EnglishFigures):
    """English text for RateByIncomeBandLine."""

    line_class = RateByIncomeBandLine

    def render(self, line: RateByIncomeBandLine) -> str:
        """The English sentence for `line`."""
        output = line.output
        income = line.income
        amount = line.income_amount
        row = line.row
        rate = line.rate
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


@english_renderer
class ChosenRateAppliedRenderer(EnglishFigures):
    """English text for ChosenRateAppliedLine."""

    line_class = ChosenRateAppliedLine

    def render(self, line: ChosenRateAppliedLine) -> str:
        """The English sentence for `line`."""
        output = line.output
        base = line.base
        amount = line.base_amount
        rate_kind = line.rate_kind
        rate = line.rate
        rule = line.rounding
        return (
            f"{output.label}: {rate_kind.label} {self._percent(rate.value)}% of "
            f"{base.label} {self._money(amount)} ({self._rounding(rule)})"
        )


@english_renderer
class AmountByCountRenderer(EnglishFigures):
    """English text for AmountByCountLine."""

    line_class = AmountByCountLine

    def render(self, line: AmountByCountLine) -> str:
        """The English sentence for `line`."""
        output = line.output
        count_kind = line.count_kind
        count = line.count
        row = line.row
        rule = line.rounding
        return (
            f"{output.label}: {self._money(row)} for {count_kind.label} {count} "
            f"({self._rounding(rule)})"
        )
