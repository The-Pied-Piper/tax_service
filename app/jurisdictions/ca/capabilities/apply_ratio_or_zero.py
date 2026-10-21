"""ApplyRatioOrZero: an amount times a ratio, zero when the denominator is zero."""

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
from app.domain.trace import RatioAppliedLine


@capability(identifier="apply_ratio_or_zero")
class ApplyRatioOrZero(Capability):
    """Produces `output`: `amount` × `numerator` / `denominator`, rounded once; 0 if zero."""

    PARAMETERS: ClassVar[Mapping[str, ParameterKind[RoundingOnly]]] = {"rounding": ROUNDING_ONLY}
    CONSUMES: ClassVar[Mapping[str, type]] = {
        "amount": Decimal,
        "numerator": Decimal,
        "denominator": Decimal,
    }
    PRODUCES: ClassVar[Mapping[str, type]] = {"output": Decimal}

    def __init__(
        self,
        rounding: ParameterDataset[RoundingOnly],
        amount: Money,
        numerator: Money,
        denominator: Money,
        output: Money,
    ) -> None:
        super().__init__(amount=amount, numerator=numerator, denominator=denominator, output=output)
        self._rounding = rounding
        self._amount = amount
        self._numerator = numerator
        self._denominator = denominator
        self._output = output

    def compute(self, inputs: tuple[Artifact[Any], ...]) -> CapabilityResult:
        amount = self._input(inputs, self._amount).value
        numerator = self._input(inputs, self._numerator).value
        denominator = self._input(inputs, self._denominator).value
        rounding = self._rounding.rounding
        if denominator == 0:
            result = rounding.apply(ExactFraction(0))
        else:
            result = rounding.apply(
                ExactFraction(amount) * ExactFraction(numerator) / ExactFraction(denominator)
            )
        return CapabilityResult(
            outputs=(Artifact(self._output, result),),
            trace=(
                RatioAppliedLine(
                    self._output,
                    self._amount,
                    amount,
                    self._numerator,
                    numerator,
                    self._denominator,
                    denominator,
                    rounding,
                    result,
                ),
            ),
        )
