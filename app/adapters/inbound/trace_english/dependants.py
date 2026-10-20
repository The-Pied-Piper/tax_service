"""English text for the trace lines of `app.domain.trace.dependants`: one renderer class
per line class, each registered with `@english_renderer`.
"""

from __future__ import annotations

from app.adapters.inbound.trace_english.figures import EnglishFigures
from app.adapters.inbound.trace_english.registry import english_renderer
from app.domain.trace.dependants import (
    CaregiverClaimLessClaimedLine,
    CaregiverClaimLine,
    DisabilityTransferLine,
    OtherDependantMedicalLine,
)


@english_renderer
class CaregiverClaimRenderer(EnglishFigures):
    """English text for CaregiverClaimLine."""

    line_class = CaregiverClaimLine

    def render(self, line: CaregiverClaimLine) -> str:
        """The English sentence for `line`."""
        output = line.output
        position = line.position
        base = line.base
        net_income = line.net_income
        maximum = line.maximum
        rule = line.rounding
        result = line.result
        return (
            f"{output.label}: dependant {position}: {self._money(base.value)} less net "
            f"income {self._money(net_income)}, at most {self._money(maximum.value)} = "
            f"{self._money(result)} ({self._rounding(rule)})"
        )


@english_renderer
class CaregiverClaimLessClaimedRenderer(EnglishFigures):
    """English text for CaregiverClaimLessClaimedLine."""

    line_class = CaregiverClaimLessClaimedLine

    def render(self, line: CaregiverClaimLessClaimedLine) -> str:
        """The English sentence for `line`."""
        output = line.output
        position = line.position
        base = line.base
        net_income = line.net_income
        maximum = line.maximum
        allowable = line.allowable_before_claimed
        claimed = line.claimed
        rule = line.rounding
        result = line.result
        return (
            f"{output.label}: dependant {position}: {self._money(base.value)} less net "
            f"income {self._money(net_income)}, at most {self._money(maximum.value)} = "
            f"{self._money(allowable)}, less claimed {self._money(claimed)} = "
            f"{self._money(result)} ({self._rounding(rule)})"
        )


@english_renderer
class OtherDependantMedicalRenderer(EnglishFigures):
    """English text for OtherDependantMedicalLine."""

    line_class = OtherDependantMedicalLine

    def render(self, line: OtherDependantMedicalLine) -> str:
        """The English sentence for `line`."""
        output = line.output
        position = line.position
        expenses = line.expenses
        net_income = line.net_income
        reduction = line.reduction
        rule = line.rounding
        result = line.result
        at_most = "" if reduction.maximum is None else f", at most {self._money(reduction.maximum)}"
        return (
            f"{output.label}: dependant {position}: expenses {self._money(expenses)} "
            f"less the lesser of {self._percent(reduction.rate.value)}% of net income "
            f"{self._money(net_income)} and {self._money(reduction.ceiling)} = "
            f"{self._money(result)}{at_most} ({self._rounding(rule)})"
        )


@english_renderer
class DisabilityTransferRenderer(EnglishFigures):
    """English text for DisabilityTransferLine."""

    line_class = DisabilityTransferLine

    def render(self, line: DisabilityTransferLine) -> str:
        """The English sentence for `line`."""
        output = line.output
        position = line.position
        base = line.base
        supplement = line.supplement
        threshold = line.threshold
        maximum = line.maximum
        under_18 = line.under_18
        care_expenses = line.care_expenses
        line_5 = line.line_5
        line_6 = line.line_6
        line_7 = line.line_7
        line_8 = line.line_8
        credit_amounts = line.credit_amounts
        taxable_income = line.taxable_income
        line_12 = line.line_12
        rule = line.rounding
        result = line.result
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
