"""Progressive tax: a bracket schedule applied to a taxable base.

One mechanism, wired per use: the same class computes, say, national and
regional basic tax from the same base, with different schedules and outputs.
Rounding happens once, on the total, using the rule it is given.
"""

from __future__ import annotations

from typing import Any, ClassVar

from app.domain.artifact import Artifact, ArtifactKind, Money
from app.domain.capability import Capability, CapabilityResult, TraceLine, capability
from app.domain.parameters.brackets import BRACKETS, BracketSchedule
from app.domain.parameters.kind import ParameterKind
from app.domain.parameters.rounding import RoundingRule


@capability(identifier="progressive_tax")
class ProgressiveTax(Capability):
    PARAMETERS: ClassVar[ParameterKind[BracketSchedule]] = BRACKETS

    def __init__(
        self,
        base: Money,
        output: Money,
        schedule: BracketSchedule,
        rounding: RoundingRule,
    ) -> None:
        self._base = base
        self._output = output
        self._schedule = schedule
        self._rounding = rounding

    @property
    def consumes(self) -> frozenset[ArtifactKind[Any]]:
        return frozenset({self._base})

    @property
    def produces(self) -> frozenset[ArtifactKind[Any]]:
        return frozenset({self._output})

    def compute(self, inputs: tuple[Artifact[Any], ...]) -> CapabilityResult:
        base = self._input(inputs, self._base).value
        slices = self._schedule.slices(base)
        tax = self._rounding.apply(self._schedule.tax_on(base))
        trace = tuple(TraceLine(s.describe(), s.tax) for s in slices) + (
            TraceLine(f"{self._output.label} on {self._base.label} {base} ({self._rounding})", tax),
        )
        return CapabilityResult(outputs=(Artifact(self._output, tax),), trace=trace)
