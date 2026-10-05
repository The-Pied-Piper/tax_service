"""Non-refundable credit: reduces a tax artifact, never below zero.

The part of the credit that exceeds the tax is lost, not refunded. The credit's
value is rounded with the rule it is given before it is applied.

With one credit, applying amount × rate per credit equals what a return form
does: sum all credit amounts, then apply the rate once. More credits will need
amounts folded into a total first, with the rate applied once.
"""

from __future__ import annotations

from typing import ClassVar

from app.domain.artifact import Artifact
from app.domain.capability import Capability, CapabilityResult, TraceLine
from app.domain.parameters.credit import CREDIT, Credit
from app.domain.parameters.kind import ParameterKind
from app.domain.parameters.rounding import RoundingRule
from app.domain.worksheet import WorksheetView


class NonRefundableCredit(Capability):
    PARAMETERS: ClassVar[ParameterKind[Credit]] = CREDIT

    def __init__(
        self, tax: Artifact, output: Artifact, credit: Credit, rounding: RoundingRule
    ) -> None:
        if tax == output:
            raise ValueError(f"tax and output must differ, got {tax} for both")
        self._tax = tax
        self._output = output
        self._credit = credit
        self._rounding = rounding

    @property
    def consumes(self) -> frozenset[Artifact]:
        return frozenset({self._tax})

    @property
    def produces(self) -> frozenset[Artifact]:
        return frozenset({self._output})

    def compute(self, worksheet: WorksheetView) -> CapabilityResult:
        tax = worksheet.get(self._tax)
        if tax < 0:
            raise ValueError(f"{self._tax} must not be negative, got {tax}")
        credit = self._rounding.apply(self._credit.value)
        applied = min(credit, tax)
        after = tax - applied
        trace: tuple[TraceLine, ...] = (
            TraceLine(f"credit: {self._credit.describe()} ({self._rounding})", credit),
            TraceLine(f"{self._output}: {self._tax} {tax} less credit, not below 0", after),
        )
        if credit > applied:
            trace += (TraceLine("unused credit, not refunded", credit - applied),)
        return CapabilityResult(outputs={self._output: after}, trace=trace)
