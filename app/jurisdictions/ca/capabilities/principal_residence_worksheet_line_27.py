"""PrincipalResidenceWorksheetLine27Capability: line 27 of Form T2091(IND)-WS, line 21 less line 26.

It records one `PrincipalResidenceWorksheetLine27` for each property, by position from 1, then an
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
from app.jurisdictions.ca.trace import PrincipalResidenceWorksheetLine27


@capability(identifier="principal_residence_worksheet_line_27")
class PrincipalResidenceWorksheetLine27Capability(PrincipalResidenceWorksheetRows):
    """Produces `output`: the total over the consumed `properties` of worksheet line 27."""

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
                PrincipalResidenceWorksheetLine27(
                    self._output, row.position, row.filed, row.line_21, row.line_26, row.line_27
                )
                for row in self._worksheet_rows(inputs)
            ]
        )
