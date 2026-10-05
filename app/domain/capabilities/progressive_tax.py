"""Progressive tax: a bracket schedule applied to a taxable base.

One mechanism, wired per use: the same class computes, say, national and
regional basic tax from the same base, with different schedules and outputs.
Rounding happens once, on the total, using the rule it is given.
"""

from __future__ import annotations

from decimal import Decimal
from typing import ClassVar

from app.domain.artifact import Amount, Artifact
from app.domain.capability import Capability, CapabilityResult, TraceLine
from app.domain.parameters.brackets import BRACKETS, BracketSchedule
from app.domain.parameters.kind import ParameterKind
from app.domain.parameters.rounding import RoundingRule


class ProgressiveTax[In: Amount, Out: Amount](Capability):
    PARAMETERS: ClassVar[ParameterKind[BracketSchedule]] = BRACKETS

    def __init__(
        self,
        base: type[In],
        output: type[Out],
        schedule: BracketSchedule,
        rounding: RoundingRule,
    ) -> None:
        if base is output:
            raise ValueError(f"base and output must differ, got {base.label()} for both")
        self._base = base
        self._output = output
        self._schedule = schedule
        self._rounding = rounding

    @property
    def consumes(self) -> frozenset[type[Artifact]]:
        return frozenset({self._base})

    @property
    def produces(self) -> frozenset[type[Artifact]]:
        return frozenset({self._output})

    def compute(self, inputs: tuple[Artifact, ...]) -> CapabilityResult:
        base = self._input(inputs, self._base).value
        slices = self._schedule.slices(base)
        tax = self._rounding.apply(sum((s.tax for s in slices), Decimal(0)))
        trace = tuple(TraceLine(s.describe(), s.tax) for s in slices) + (
            TraceLine(
                f"{self._output.label()} on {self._base.label()} {base} ({self._rounding})", tax
            ),
        )
        return CapabilityResult(outputs=(self._output(tax),), trace=trace)
