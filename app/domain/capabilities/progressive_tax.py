"""Progressive tax: a bracket schedule applied to a taxable base.

One mechanism, wired per use: the same class computes, say, national and
regional basic tax from the same base, with different schedules and outputs.
Rounding happens once, on the total, using the rule it is given.
"""

from __future__ import annotations

from collections.abc import Mapping
from decimal import Decimal

from app.domain.artifact import Artifact
from app.domain.capability import Capability, CapabilityResult, TraceLine
from app.domain.parameters.brackets import BracketSchedule
from app.domain.parameters.rounding import RoundingRule


class ProgressiveTax(Capability):
    def __init__(
        self,
        base: Artifact,
        output: Artifact,
        schedule: BracketSchedule,
        rounding: RoundingRule,
    ) -> None:
        if base == output:
            raise ValueError(f"base and output must differ, got {base} for both")
        self._base = base
        self._output = output
        self._schedule = schedule
        self._rounding = rounding

    @property
    def consumes(self) -> frozenset[Artifact]:
        return frozenset({self._base})

    @property
    def produces(self) -> frozenset[Artifact]:
        return frozenset({self._output})

    def _compute(self, inputs: Mapping[Artifact, Decimal]) -> CapabilityResult:
        base = inputs[self._base]
        slices = self._schedule.slices(base)
        tax = self._rounding.apply(sum((s.tax for s in slices), Decimal(0)))
        trace = tuple(TraceLine(s.describe(), s.tax) for s in slices) + (
            TraceLine(f"{self._output} on {self._base} {base} ({self._rounding})", tax),
        )
        return CapabilityResult(outputs={self._output: tax}, trace=trace)
