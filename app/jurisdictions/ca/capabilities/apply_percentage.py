"""ApplyPercentage: an amount times a percentage, rounded once."""

from __future__ import annotations

from collections.abc import Mapping
from decimal import Decimal
from fractions import Fraction as ExactFraction
from typing import Any, ClassVar

from app.domain.artifact import Artifact, Money
from app.domain.capability import Capability, CapabilityResult, capability
from app.domain.parameters.datasets import ParameterDataset
from app.domain.parameters.kind import ParameterKind
from app.domain.parameters.rounding_only import ROUNDING_ONLY, RoundingOnly
from app.jurisdictions.ca.trace.percentages import PercentageAppliedLine


@capability(identifier="apply_percentage")
class ApplyPercentage(Capability):
    """Produces `output`: the consumed `amount` × `percentage` / 100, rounded once."""

    PARAMETERS: ClassVar[Mapping[str, ParameterKind[RoundingOnly]]] = {"rounding": ROUNDING_ONLY}
    CONSUMES: ClassVar[Mapping[str, type]] = {"amount": Decimal, "percentage": Decimal}
    PRODUCES: ClassVar[Mapping[str, type]] = {"output": Decimal}

    def __init__(
        self,
        rounding: ParameterDataset[RoundingOnly],
        amount: Money,
        percentage: Money,
        output: Money,
    ) -> None:
        super().__init__(amount=amount, percentage=percentage, output=output)
        self._rounding = rounding
        self._amount = amount
        self._percentage = percentage
        self._output = output

    def compute(self, inputs: tuple[Artifact[Any], ...]) -> CapabilityResult:
        amount = self._input(inputs, self._amount).value
        percentage = self._input(inputs, self._percentage).value
        rounding = self._rounding.rounding
        result = rounding.apply(ExactFraction(amount) * ExactFraction(percentage) / 100)
        return CapabilityResult(
            outputs=(Artifact(self._output, result),),
            trace=(
                PercentageAppliedLine(
                    self._output,
                    self._amount,
                    amount,
                    self._percentage,
                    percentage,
                    rounding,
                    result,
                ),
            ),
        )
