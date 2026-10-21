"""PrincipalResidenceGain: the gain left after the principal residence exemption, one property each.

For Form T2091(IND) Part 1 and Part 3, completed for each property sold: the proceeds (line 8)
less the adjusted cost base (line 10) and the outlays (line 9) is the gain (line 18); the years
designated after 1981 and from 1972 to 1981 (lines 1 and 2) added to the "plus one" year when it
applies (line 20) multiply the gain (line 21), which is divided by the years owned (line 7, the
sum of lines 5 and 6) to give the exempt part (line 23); and the gain less that, from 0, is line
24, which is line 54 since Part 2 and Part 4 are not modelled. The figures of each property are
fields of each record in the consumed record list. The output is the total of those taxable gains,
0 when there are no properties. Each property is worked on its own, never pooled with the others,
and line 23 is the exact fraction rounded once, with the `rounding` dataset's rule, before it is
taken off; the other lines stay exact. A property owned for no years is refused, line 22 being the
divisor. It records one `PrincipalResidenceGainLine` for each property, by position from 1, then
an `ItemsTotalLine`.
"""

from __future__ import annotations

from collections.abc import Mapping
from decimal import Decimal
from fractions import Fraction as ExactFraction
from typing import Any, ClassVar

from app.domain.artifact import Artifact, ArtifactKind, Money
from app.domain.capability import Capability, CapabilityResult, capability
from app.domain.errors import ValidationError
from app.domain.parameters.datasets import ParameterDataset
from app.domain.parameters.kind import ParameterKind
from app.domain.parameters.rounding_only import ROUNDING_ONLY, RoundingOnly
from app.domain.record_list import RecordList
from app.domain.trace import ItemsTotalLine
from app.jurisdictions.ca.catalog import (
    RESIDENCE_ADJUSTED_COST_BASE,
    RESIDENCE_OUTLAYS,
    RESIDENCE_PLUS_ONE_YEAR,
    RESIDENCE_PROCEEDS,
    RESIDENCE_YEARS_DESIGNATED_1972_TO_1981,
    RESIDENCE_YEARS_DESIGNATED_AFTER_1981,
    RESIDENCE_YEARS_OWNED_1972_TO_1981,
    RESIDENCE_YEARS_OWNED_AFTER_1981,
)
from app.jurisdictions.ca.trace import PrincipalResidenceGainLine


@capability(identifier="principal_residence_gain")
class PrincipalResidenceGain(Capability):
    """Produces `output`: the total, over the consumed `properties`, of each one's gain less its
    principal residence exemption, from 0, the exemption rounded by the `rounding` dataset."""

    PARAMETERS: ClassVar[Mapping[str, ParameterKind[RoundingOnly]]] = {"rounding": ROUNDING_ONLY}
    CONSUMES: ClassVar[Mapping[str, type]] = {"properties": RecordList}
    PRODUCES: ClassVar[Mapping[str, type]] = {"output": Decimal}

    def __init__(
        self,
        rounding: ParameterDataset[RoundingOnly],
        properties: ArtifactKind[RecordList],
        output: Money,
    ) -> None:
        """Wire the capability: its rounding dataset, the record list it reads, the kind
        produced."""
        super().__init__(properties=properties, output=output)
        self._rounding = rounding
        self._properties = properties
        self._output = output

    def compute(self, inputs: tuple[Artifact[Any], ...]) -> CapabilityResult:
        records = self._input(inputs, self._properties).value.records
        rounding = self._rounding.rounding
        lines: list[PrincipalResidenceGainLine] = []
        for position, record in enumerate(records, start=1):
            designated_after = int(record[RESIDENCE_YEARS_DESIGNATED_AFTER_1981])
            designated_before = int(record[RESIDENCE_YEARS_DESIGNATED_1972_TO_1981])
            owned_after = int(record[RESIDENCE_YEARS_OWNED_AFTER_1981])
            owned_before = int(record[RESIDENCE_YEARS_OWNED_1972_TO_1981])
            plus_one = int(record[RESIDENCE_PLUS_ONE_YEAR])
            proceeds = Decimal(record[RESIDENCE_PROCEEDS])
            outlays = Decimal(record[RESIDENCE_OUTLAYS])
            cost_base = Decimal(record[RESIDENCE_ADJUSTED_COST_BASE])
            designated = designated_after + designated_before
            owned = owned_after + owned_before
            if owned == 0:
                raise ValidationError(
                    f"property {position}: the years owned (lines 5 and 6) are 0, "
                    "so the exemption (line 23) cannot be divided by them"
                )
            gain = proceeds - (cost_base + outlays)
            line_20 = designated + plus_one
            line_21 = gain * line_20
            exempt = rounding.apply(ExactFraction(line_21) / owned)
            result = max(Decimal(0), gain - exempt)
            lines.append(
                PrincipalResidenceGainLine(
                    self._output,
                    position,
                    designated_after,
                    designated_before,
                    designated,
                    owned_after,
                    owned_before,
                    owned,
                    plus_one,
                    proceeds,
                    cost_base,
                    outlays,
                    gain,
                    line_20,
                    line_21,
                    rounding,
                    exempt,
                    result,
                )
            )
        items = tuple((line.position, line.result) for line in lines)
        total = sum((amount for _position, amount in items), Decimal(0))
        return CapabilityResult(
            outputs=(Artifact(self._output, total),),
            trace=(*lines, ItemsTotalLine(self._output, items, total)),
        )
