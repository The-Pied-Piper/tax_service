"""Non-refundable credit: reduces a tax artifact, never below zero.

The part of the credit that exceeds the tax is lost, not refunded. The credit is
amount × rate, rounded with the `amount` dataset's rule before it is applied; the
`rate` dataset's rule is never applied.

With one credit, applying amount × rate per credit equals what a return form
does: sum all credit amounts, then apply the rate once. More credits will need
amounts folded into a total first, with the rate applied once.
"""

from __future__ import annotations

from collections.abc import Mapping
from decimal import Decimal
from typing import Any, ClassVar

from app.domain.artifact import Artifact, Money
from app.domain.capability import Capability, CapabilityResult, TraceLine, capability
from app.domain.parameters.credit import CREDIT, Credit
from app.domain.parameters.datasets import ParameterDataset
from app.domain.parameters.kind import ParameterKind
from app.domain.parameters.rate import RATE, Rate


@capability(identifier="non_refundable_credit")
class NonRefundableCredit(Capability):
    """Produces `output`: the consumed `tax` less `amount` × `rate`, never below zero."""

    PARAMETERS: ClassVar[Mapping[str, ParameterKind[Any]]] = {"amount": CREDIT, "rate": RATE}
    CONSUMES: ClassVar[Mapping[str, type]] = {"tax": Decimal}
    PRODUCES: ClassVar[Mapping[str, type]] = {"output": Decimal}

    def __init__(
        self,
        tax: Money,
        output: Money,
        amount: ParameterDataset[Credit],
        rate: ParameterDataset[Rate],
    ) -> None:
        """Wire the capability: the kinds it consumes and produces, its amount and rate datasets."""
        super().__init__(tax=tax, output=output)
        self._tax = tax
        self._output = output
        self._amount = amount
        self._rate = rate

    def compute(self, inputs: tuple[Artifact[Any], ...]) -> CapabilityResult:
        tax = self._input(inputs, self._tax).value
        if tax < 0:
            raise ValueError(f"{self._tax.label} must not be negative, got {tax}")
        amount, rate, rounding = self._amount.values, self._rate.values.value, self._amount.rounding
        credit = rounding.apply(amount.at(rate))
        applied = min(credit, tax)
        after = tax - applied
        trace: tuple[TraceLine, ...] = (
            TraceLine(f"credit: {amount.describe_at(rate)} ({rounding})", credit),
            TraceLine(
                f"{self._output.label}: {self._tax.label} {tax} less credit, not below 0", after
            ),
        )
        if credit > applied:
            trace += (TraceLine("unused credit, not refunded", credit - applied),)
        return CapabilityResult(outputs=(Artifact(self._output, after),), trace=trace)
