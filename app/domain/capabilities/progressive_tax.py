"""Progressive tax: a bracket schedule applied to a taxable base.

One mechanism, wired per use: the same class computes, say, national and
regional basic tax from the same base, with different schedules and outputs.
Rounding happens once, on the total, using the schedule dataset's rule.
"""

from __future__ import annotations

from collections.abc import Mapping
from decimal import Decimal
from typing import Any, ClassVar

from app.domain.artifact import Artifact, ArtifactKind, Money
from app.domain.capability import Capability, CapabilityResult, TraceLine, capability
from app.domain.parameters.brackets import BRACKETS, BracketSchedule
from app.domain.parameters.datasets import ParameterDataset
from app.domain.parameters.kind import ParameterKind


@capability(identifier="progressive_tax")
class ProgressiveTax(Capability):
    """Produces `output`: tax on the consumed `base` from the `schedule` dataset's brackets."""

    PARAMETERS: ClassVar[Mapping[str, ParameterKind[Any]]] = {"schedule": BRACKETS}
    CONSUMES: ClassVar[Mapping[str, type]] = {"base": Decimal}
    PRODUCES: ClassVar[Mapping[str, type]] = {"output": Decimal}

    def __init__(
        self, base: Money, output: Money, schedule: ParameterDataset[BracketSchedule]
    ) -> None:
        """Wire the capability: the kinds it consumes and produces, and its schedule dataset."""
        self._base = base
        self._output = output
        self._schedule = schedule

    @property
    def consumes(self) -> frozenset[ArtifactKind[Any]]:
        return frozenset({self._base})

    @property
    def produces(self) -> frozenset[ArtifactKind[Any]]:
        return frozenset({self._output})

    def compute(self, inputs: tuple[Artifact[Any], ...]) -> CapabilityResult:
        base = self._input(inputs, self._base).value
        schedule, rounding = self._schedule.values, self._schedule.rounding
        slices = schedule.slices(base)
        tax = rounding.apply(schedule.tax_on(base))
        trace = tuple(TraceLine(s.describe(), s.tax) for s in slices) + (
            TraceLine(f"{self._output.label} on {self._base.label} {base} ({rounding})", tax),
        )
        return CapabilityResult(outputs=(Artifact(self._output, tax),), trace=trace)
