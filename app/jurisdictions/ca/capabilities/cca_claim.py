"""CcaClaim: the total capital cost allowance claim of the CCA table, T776 and T2125 Area A.

T776 "Line ii: Total CCA claim for the year: Total of column 23" and T2125 "Total CCA claim for the
year: Total of column 21": each class of the consumed record list is one row of the table, worked
on its own as `CcaTable` works it, with its rate, factors and half-year rule from the
`class_rates` dataset and columns 15, 17 and 18 and the maximum rounded once each with the
dataset's rule. The claim of each row is the caller's, from 0 up to column 21 ("column 19
multiplied by column 20, or a lower amount") less column 22 ("Non-compliant amount of CCA (see Chart
B below)", from the consumed `non_compliant` record list, 0 for a class it does not list), which is
column 23 as printed ("column 21 minus column 22"), and refused above it. The output is the total of
the claims, 0 when there are no classes. It records one `CcaClaimLine` for each class, by
position from 1, then an `ItemsTotalLine`.
"""

from __future__ import annotations

from collections.abc import Mapping
from decimal import Decimal
from typing import Any, ClassVar

from app.domain.artifact import Artifact, ArtifactKind, Money
from app.domain.capability import CapabilityResult, capability
from app.domain.parameters.class_rates import ClassRates
from app.domain.parameters.datasets import ParameterDataset
from app.domain.record_list import RecordList
from app.domain.trace import ItemsTotalLine
from app.jurisdictions.ca.capabilities.cca_table import CcaClaimTable
from app.jurisdictions.ca.trace import CcaClaimLine


@capability(identifier="cca_claim")
class CcaClaim(CcaClaimTable):
    """Produces `output`: the total, over the consumed `classes`, of each class's CCA claimed, at
    most its maximum from the `class_rates` dataset less its column 22 from `non_compliant`."""

    CONSUMES: ClassVar[Mapping[str, type]] = {"classes": RecordList, "non_compliant": RecordList}
    PRODUCES: ClassVar[Mapping[str, type]] = {"output": Decimal}

    def __init__(
        self,
        class_rates: ParameterDataset[ClassRates],
        classes: ArtifactKind[RecordList],
        non_compliant: ArtifactKind[RecordList],
        output: Money,
    ) -> None:
        """Wire the capability: its class-rate dataset, the record list it reads, the record list
        of column 22 amounts, the kind produced."""
        super().__init__(class_rates, classes, non_compliant, output)
        self._output = output

    def compute(self, inputs: tuple[Artifact[Any], ...]) -> CapabilityResult:
        lines: list[CcaClaimLine] = []
        column_22 = self._column_22(inputs)
        for row in self._rows(inputs):
            columns = self._checked_columns(row, column_22)
            lines.append(
                CcaClaimLine(
                    output=self._output,
                    position=row.position,
                    class_rate=row.class_rate,
                    no_property_left=row.no_property_left,
                    column_7=row.column_7,
                    column_14=columns.column_14,
                    column_15=columns.column_15,
                    column_16=columns.column_16,
                    column_17=columns.column_17,
                    column_18=columns.column_18,
                    column_19=columns.column_19,
                    zero_reason=row.zero_reason,
                    maximum=columns.maximum,
                    rounding=self._class_rates.rounding,
                    claim=row.claimed,
                )
            )
        items = tuple((line.position, line.claim) for line in lines)
        total = sum((amount for _position, amount in items), Decimal(0))
        return CapabilityResult(
            outputs=(Artifact(self._output, total),),
            trace=(*lines, ItemsTotalLine(self._output, items, total)),
        )
