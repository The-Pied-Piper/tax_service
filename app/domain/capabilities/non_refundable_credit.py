"""Non-refundable credit: reduces a tax artifact, never below zero.

The part of the credit that exceeds the tax is lost, not refunded. The credit's
value is rounded with the rule it is given before it is applied.

With one credit, applying amount × rate per credit equals what a return form
does: sum all credit amounts, then apply the rate once. More credits will need
amounts folded into a total first, with the rate applied once.
"""

from __future__ import annotations

from typing import Any, ClassVar

from app.domain.artifact import Artifact, ArtifactKind, Money
from app.domain.capability import Capability, CapabilityResult, TraceLine, capability
from app.domain.parameters.credit import CREDIT, Credit
from app.domain.parameters.kind import ParameterKind
from app.domain.parameters.rounding import RoundingRule


@capability(identifier="non_refundable_credit")
class NonRefundableCredit(Capability):
    PARAMETERS: ClassVar[ParameterKind[Credit]] = CREDIT

    def __init__(self, tax: Money, output: Money, credit: Credit, rounding: RoundingRule) -> None:
        self._tax = tax
        self._output = output
        self._credit = credit
        self._rounding = rounding

    @property
    def consumes(self) -> frozenset[ArtifactKind[Any]]:
        return frozenset({self._tax})

    @property
    def produces(self) -> frozenset[ArtifactKind[Any]]:
        return frozenset({self._output})

    def compute(self, inputs: tuple[Artifact[Any], ...]) -> CapabilityResult:
        tax = self._input(inputs, self._tax).value
        if tax < 0:
            raise ValueError(f"{self._tax.label} must not be negative, got {tax}")
        credit = self._rounding.apply(self._credit.value)
        applied = min(credit, tax)
        after = tax - applied
        trace: tuple[TraceLine, ...] = (
            TraceLine(f"credit: {self._credit.describe()} ({self._rounding})", credit),
            TraceLine(
                f"{self._output.label}: {self._tax.label} {tax} less credit, not below 0", after
            ),
        )
        if credit > applied:
            trace += (TraceLine("unused credit, not refunded", credit - applied),)
        return CapabilityResult(outputs=(Artifact(self._output, after),), trace=trace)
