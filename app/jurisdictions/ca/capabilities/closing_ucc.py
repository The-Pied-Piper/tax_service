"""ClosingUcc: the UCC at the end of the year of each class of the CCA table, for next year.

T776 Area A "Column 24: UCC at the end of the year (column 7 minus column 23)" (T2125 column 22,
column 7 minus column 21), and Guide T4036 "Column 7": "You cannot claim CCA when the amount in
column 7 is: negative ... positive and you do not have any property left in that class ... In
either case, enter "0" in column 24". Each class of the consumed record list is one row of the
table, worked on its own as `CcaTable` works it, its claim refused above its column 21 less its
column 22 (the `non_compliant` record list) as `CcaClaimTable` refuses it. The output is a record
list of the class number and the UCC at the end of the year, one record per class in the caller's
order: column 7 less the claim, or 0 when column 7 is negative or is positive with no property
left. It records one `ClosingUccLine` for each class, by position from 1, which names why column 24
is 0 when it is, and no total.
"""

from __future__ import annotations

from collections.abc import Mapping
from decimal import Decimal
from typing import Any, ClassVar

from app.domain.artifact import Artifact, ArtifactKind
from app.domain.capability import CapabilityResult, capability
from app.domain.parameters.class_rates import ClassRates
from app.domain.parameters.datasets import ParameterDataset
from app.domain.record_list import RecordList
from app.jurisdictions.ca.capabilities.cca_table import CcaClaimTable
from app.jurisdictions.ca.catalog import CCA_CLASS_NUMBER, CCA_UCC_AT_END
from app.jurisdictions.ca.trace import CcaZeroReason, ClosingUccLine


@capability(identifier="closing_ucc")
class ClosingUcc(CcaClaimTable):
    """Produces `output`: for each of the consumed `classes`, its class number and its UCC at the
    end of the year, with its maximum from the `class_rates` dataset less its column 22."""

    CONSUMES: ClassVar[Mapping[str, type]] = {"classes": RecordList, "non_compliant": RecordList}
    PRODUCES: ClassVar[Mapping[str, type]] = {"output": RecordList}

    def __init__(
        self,
        class_rates: ParameterDataset[ClassRates],
        classes: ArtifactKind[RecordList],
        non_compliant: ArtifactKind[RecordList],
        output: ArtifactKind[RecordList],
    ) -> None:
        """Wire the capability: its class-rate dataset, the record list it reads, the record list
        of column 22 amounts, the record list kind produced, of the class number and the UCC at
        the end of the year."""
        super().__init__(class_rates, classes, non_compliant, output)
        self._output = output

    def compute(self, inputs: tuple[Artifact[Any], ...]) -> CapabilityResult:
        lines: list[ClosingUccLine] = []
        records: list[dict[ArtifactKind[Any], Decimal]] = []
        column_22 = self._column_22(inputs)
        for row in self._rows(inputs):
            self._checked_columns(row, column_22)
            closes_at_zero = row.zero_reason is not CcaZeroReason.NONE
            result = Decimal(0) if closes_at_zero else row.column_7 - row.claimed
            lines.append(
                ClosingUccLine(
                    self._output,
                    row.position,
                    row.class_rate,
                    row.no_property_left,
                    row.column_7,
                    row.zero_reason,
                    row.claimed,
                    result,
                )
            )
            records.append({CCA_CLASS_NUMBER: row.class_number, CCA_UCC_AT_END: result})
        return CapabilityResult(
            outputs=(
                Artifact(self._output, RecordList((CCA_CLASS_NUMBER, CCA_UCC_AT_END), records)),
            ),
            trace=tuple(lines),
        )
