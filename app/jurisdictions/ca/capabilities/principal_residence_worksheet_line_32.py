"""PrincipalResidenceWorksheetLine32Capability: line 32 of Form T2091(IND)-WS, line 2 plus the "plus
one".

It records one `PrincipalResidenceWorksheetLine32` for each property, by position from 1, then an
`ItemsTotalLine`.
"""

from __future__ import annotations

from collections.abc import Mapping
from decimal import Decimal
from typing import Any, ClassVar

from app.domain.artifact import Artifact, ArtifactKind, Money
from app.domain.capability import CapabilityResult, capability
from app.domain.parameters.datasets import ParameterDataset
from app.domain.parameters.factor import Factor
from app.domain.parameters.rounding_only import RoundingOnly
from app.domain.record_list import RecordList
from app.jurisdictions.ca.capabilities.principal_residence_worksheet_rows import (
    PrincipalResidenceWorksheetRows,
)
from app.jurisdictions.ca.trace import PrincipalResidenceWorksheetLine32


@capability(identifier="principal_residence_worksheet_line_32")
class PrincipalResidenceWorksheetLine32Capability(PrincipalResidenceWorksheetRows):
    """Produces `output`: the total over the consumed `properties` of worksheet line 32."""

    PRODUCES: ClassVar[Mapping[str, type]] = {"output": Decimal}

    def __init__(
        self,
        rounding: ParameterDataset[RoundingOnly],
        chart_1_factor: ParameterDataset[Factor],
        properties: ArtifactKind[RecordList],
        output: Money,
    ) -> None:
        """Wire the capability: its rounding and Chart 1 factor datasets, the record list read and
        the kind produced."""
        super().__init__(rounding, chart_1_factor, properties, output)
        self._output = output

    def compute(self, inputs: tuple[Artifact[Any], ...]) -> CapabilityResult:
        return self._result(
            [
                PrincipalResidenceWorksheetLine32(
                    self._output,
                    row.position,
                    row.part_2.area_a,
                    row.line_2,
                    row.plus_one,
                    Decimal(row.part_2.line_32),
                )
                for row in self._worksheet_rows(inputs)
            ]
        )
