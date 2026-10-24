"""ProratedByFiscalPeriodDays: an amount prorated by the days of the fiscal period, rounded once.

Guide T4002 2025 and Guide T4036 2025, "Immediate expensing incentive": "The deduction is limited
to $1.5 million per tax year: ... The limit is also prorated for tax years shorter than 365 days".
The guides print no arithmetic, so the proration is taken as their CCA rule is ("base your CCA
claim on the number of days in your fiscal period compared to 365 days"): the amount times the days
of the fiscal period over the days of a full year. The output is `rounding.apply(amount x
fiscal_period_days / full_year_days)`, formed as one exact fraction and rounded once with the
`rounding_only` dataset's rule. The `full_year_days` (365 in 2025) come from the `class_rates`
dataset. Days below 1 are an `InputBelowBoundError` and days above `full_year_days` an
`InputAboveBoundError`. It records one `ProratedByDaysLine`.
"""

from __future__ import annotations

from collections.abc import Mapping
from decimal import Decimal
from fractions import Fraction as ExactFraction
from typing import Any, ClassVar

from app.domain.artifact import Artifact, ArtifactKind, Money
from app.domain.capability import Capability, CapabilityResult, capability
from app.domain.errors import InputAboveBoundError, InputBelowBoundError
from app.domain.parameters.class_rates import CLASS_RATES, ClassRates
from app.domain.parameters.datasets import ParameterDataset
from app.domain.parameters.kind import ParameterKind
from app.domain.parameters.rounding_only import ROUNDING_ONLY, RoundingOnly
from app.jurisdictions.ca.trace import ProratedByDaysLine


@capability(identifier="prorated_by_fiscal_period_days")
class ProratedByFiscalPeriodDays(Capability):
    """Produces `output`: the consumed `amount` × `fiscal_period_days` / `full_year_days`, rounded
    once."""

    PARAMETERS: ClassVar[Mapping[str, ParameterKind[Any]]] = {
        "rounding": ROUNDING_ONLY,
        "class_rates": CLASS_RATES,
    }
    CONSUMES: ClassVar[Mapping[str, type]] = {"amount": Decimal, "fiscal_period_days": int}
    PRODUCES: ClassVar[Mapping[str, type]] = {"output": Decimal}

    def __init__(
        self,
        rounding: ParameterDataset[RoundingOnly],
        class_rates: ParameterDataset[ClassRates],
        amount: Money,
        fiscal_period_days: ArtifactKind[int],
        output: Money,
    ) -> None:
        """Wire the capability: its rounding and class-rate datasets, the Decimal amount, the int
        kind of the days of the fiscal period, the Decimal kind of the output."""
        super().__init__(amount=amount, fiscal_period_days=fiscal_period_days, output=output)
        self._rounding = rounding
        self._class_rates = class_rates
        self._amount = amount
        self._days = fiscal_period_days
        self._output = output

    def compute(self, inputs: tuple[Artifact[Any], ...]) -> CapabilityResult:
        amount: Decimal = self._input(inputs, self._amount).value
        days: int = self._input(inputs, self._days).value
        full_year = self._class_rates.values.full_year_days
        identifier = self._days.identifier
        if days < 1:
            raise InputBelowBoundError(f"{identifier} {days} is below the minimum 1")
        if days > full_year:
            raise InputAboveBoundError(f"{identifier} {days} is above the maximum {full_year}")
        rounding = self._rounding.rounding
        result = rounding.apply(ExactFraction(amount) * days / full_year)
        return CapabilityResult(
            outputs=(Artifact(self._output, result),),
            trace=(
                ProratedByDaysLine(
                    self._output,
                    self._amount,
                    amount,
                    self._days,
                    days,
                    full_year,
                    result,
                ),
            ),
        )
