"""Non-refundable credit: applies a rate once to the summed credit amounts and reduces a tax.

The credit amounts arrive already summed, as one consumed artifact; the credit is that sum × the
`rate` dataset's rate, rounded with the `rate` dataset's rule, which defaults to no rounding. The
credit reduces the consumed tax, never below zero: the part that exceeds the tax is lost, not
refunded.
"""

from __future__ import annotations

from collections.abc import Mapping
from decimal import Decimal
from typing import Any, ClassVar

from app.domain.artifact import Artifact, Money
from app.domain.capability import Capability, CapabilityResult, capability
from app.domain.parameters.datasets import ParameterDataset
from app.domain.parameters.kind import ParameterKind
from app.domain.parameters.rate import RATE, Rate
from app.domain.trace import CreditAppliedLine, CreditLine, TraceLine, UnusedCreditLine


@capability(identifier="non_refundable_credit")
class NonRefundableCredit(Capability):
    """Produces `output`: the consumed `tax` less `amounts` × `rate`, never below zero."""

    PARAMETERS: ClassVar[Mapping[str, ParameterKind[Rate]]] = {"rate": RATE}
    CONSUMES: ClassVar[Mapping[str, type]] = {"amounts": Decimal, "tax": Decimal}
    PRODUCES: ClassVar[Mapping[str, type]] = {"output": Decimal}

    def __init__(
        self, rate: ParameterDataset[Rate], amounts: Money, tax: Money, output: Money
    ) -> None:
        """Wire the capability: its rate dataset, the kinds it consumes, the kind it produces."""
        super().__init__(amounts=amounts, tax=tax, output=output)
        self._rate = rate
        self._amounts = amounts
        self._tax = tax
        self._output = output

    def compute(self, inputs: tuple[Artifact[Any], ...]) -> CapabilityResult:
        amounts = self._non_negative(inputs, self._amounts)
        tax = self._non_negative(inputs, self._tax)
        rate, rounding = self._rate.values, self._rate.rounding
        credit = rounding.apply(amounts * rate.value)
        applied = min(credit, tax)
        after = tax - applied
        trace: tuple[TraceLine, ...] = (
            CreditLine(self._amounts, amounts, rate, rounding, credit),
            CreditAppliedLine(self._output, self._tax, tax, after),
        )
        if credit > applied:
            trace += (UnusedCreditLine(credit - applied),)
        return CapabilityResult(outputs=(Artifact(self._output, after),), trace=trace)

    def _non_negative(self, inputs: tuple[Artifact[Any], ...], kind: Money) -> Decimal:
        """The value of `kind` in `inputs`; raises ValueError if it is negative."""
        value = self._input(inputs, kind).value
        if value < 0:
            raise ValueError(f"{kind.label} must not be negative, got {value}")
        return value
