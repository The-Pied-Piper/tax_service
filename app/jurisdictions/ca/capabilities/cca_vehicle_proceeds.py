"""CcaVehicleProceeds: the proceeds of disposition of a Class 10.1 passenger vehicle scaled to its
prescribed amount, for the CCA table of Form T2125 Area A (columns 5 and 6).

T2125 (2025) Area A endnote 2 (T776 Column 5 Note 2, and T2042 and T2121 endnote 2, say the same):
"The proceeds of disposition of a zero-emission passenger vehicle (ZEPV) that has been included in
Class 54, or a passenger vehicle bought after April 18, 2021, that has been included in Class
10.1, and whose cost is more than the prescribed amount will be adjusted based on a factor equal
to its prescribed amount as a proportion of the actual cost of the vehicle. For dispositions after
July 29, 2019, you will have to adjust the actual cost of the vehicle for any payments or
repayments of government assistance that you may have received or repaid for the vehicle. If the
passenger vehicle in Class 10.1 is not designated for immediate expensing treatment, this special
rule does not apply." Guide T4036, "Class 10.1 (30%)": the prescribed amounts are $30,000
(acquired before 2022), $34,000 (2022), $36,000 (2023), $37,000 (2024) and $38,000 (2025), each
"plus the GST/HST or PST".

Each record of the consumed `classes` is one row of the table. A record holds the year the vehicle
was acquired (0 when the rule does not apply to the row, which the caller decides: the vehicle is
not designated for immediate expensing, or was not sold at arm's length), its actual cost and the
government assistance received less repaid. A row of year 0 is copied as it is. For a year, the
class must be 10.1 (Class 54 is not modelled) and the year 2021 or later (a vehicle bought after
April 18, 2021), else the row is refused (`InvalidRecordError`, naming the item); a year later
than the newest row of the `prescribed_amounts` dataset uses that row. The prescribed amount with
tax is the year's amount plus that amount times the consumed `sales_tax_rate` (the caller's GST
or HST rate, in percent), rounded; the actual cost is the cost less the assistance. When the
actual cost is more than the prescribed amount with tax, the proceeds (column 5) and the DIEP part
of them (column 6) each become the exact product of the column and the prescribed amount with
tax over the actual cost, rounded once with the dataset's rule; otherwise they are unchanged. The
output is a record list of the row's other fields, one record per row in the caller's order. It
records one `CcaVehicleProceedsLine` for each row, by position from 1, and no total.
"""

from __future__ import annotations

from collections.abc import Mapping
from decimal import Decimal
from fractions import Fraction as ExactFraction
from typing import Any, ClassVar

from app.domain.artifact import Artifact, ArtifactKind, Money
from app.domain.capability import Capability, CapabilityResult, capability
from app.domain.errors import InvalidRecordError
from app.domain.parameters.datasets import ParameterDataset
from app.domain.parameters.kind import ParameterKind
from app.domain.parameters.rounding import RoundingRule
from app.domain.parameters.year_amounts import YEAR_AMOUNTS, YearAmounts
from app.domain.record_list import Record, RecordList, RecordListKind
from app.jurisdictions.ca.catalog import (
    CCA_CLASS_NUMBER,
    CCA_DIEP_PROCEEDS,
    CCA_PROCEEDS,
    CCA_VEHICLE_ACQUIRED_YEAR,
    CCA_VEHICLE_COST,
    CCA_VEHICLE_GOVERNMENT_ASSISTANCE,
)
from app.jurisdictions.ca.trace import CcaVehicleProceedsLine

CLASS_10_1 = Decimal("10.1")
FIRST_YEAR = 2021  # "a passenger vehicle bought after April 18, 2021"


@capability(identifier="cca_vehicle_proceeds")
class CcaVehicleProceeds(Capability):
    """Produces `output`: the consumed `classes` with the proceeds of each Class 10.1 vehicle
    scaled to its prescribed amount, at the consumed `sales_tax_rate`."""

    PARAMETERS: ClassVar[Mapping[str, ParameterKind[Any]]] = {"prescribed_amounts": YEAR_AMOUNTS}
    CONSUMES: ClassVar[Mapping[str, type]] = {"classes": RecordList, "sales_tax_rate": Decimal}
    PRODUCES: ClassVar[Mapping[str, type]] = {"output": RecordList}

    def __init__(
        self,
        prescribed_amounts: ParameterDataset[YearAmounts],
        classes: ArtifactKind[RecordList],
        sales_tax_rate: Money,
        output: RecordListKind,
    ) -> None:
        """Wire the capability: its prescribed amounts dataset, the record list and the sales tax
        rate it reads, the record list kind produced."""
        super().__init__(classes=classes, sales_tax_rate=sales_tax_rate, output=output)
        self._prescribed_amounts = prescribed_amounts.values
        self._rounding: RoundingRule = prescribed_amounts.rounding
        self._classes = classes
        self._sales_tax_rate = sales_tax_rate
        self._output = output

    def compute(self, inputs: tuple[Artifact[Any], ...]) -> CapabilityResult:
        rows = self._input(inputs, self._classes).value.records
        rate = self._input(inputs, self._sales_tax_rate).value
        lines: list[CcaVehicleProceedsLine] = []
        records: list[dict[ArtifactKind[Any], Decimal | int]] = []
        for position, row in enumerate(rows, 1):
            line, record = self._row(position, row, rate)
            lines.append(line)
            records.append(record)
        return CapabilityResult(
            outputs=(Artifact(self._output, RecordList(self._output.fields, records)),),
            trace=tuple(lines),
        )

    def _row(
        self, position: int, row: Record, rate: Decimal
    ) -> tuple[CcaVehicleProceedsLine, dict[ArtifactKind[Any], Decimal | int]]:
        """The line and the output record of one row."""
        proceeds = row[CCA_PROCEEDS]
        diep_proceeds = row[CCA_DIEP_PROCEEDS]
        year = row[CCA_VEHICLE_ACQUIRED_YEAR]
        prescribed = Decimal(0)
        actual_cost = Decimal(0)
        applied = False
        adjusted_proceeds = proceeds
        adjusted_diep_proceeds = diep_proceeds
        if year > 0:
            if row[CCA_CLASS_NUMBER] != CLASS_10_1:
                raise InvalidRecordError(
                    f"item {position}: a vehicle year is given but the class is "
                    f"{row[CCA_CLASS_NUMBER]}, not 10.1"
                )
            if year < FIRST_YEAR:
                raise InvalidRecordError(
                    f"item {position}: a vehicle acquired in {year} is not a passenger vehicle "
                    f"bought after April 18, 2021"
                )
            amounts = self._prescribed_amounts.row_for(year)
            if amounts is None:
                raise InvalidRecordError(f"item {position}: no prescribed amount for {year}")
            printed = amounts.amount("prescribed_amount")
            tax = self._rounding.apply(ExactFraction(printed) * ExactFraction(rate) / 100)
            prescribed = printed + tax
            actual_cost = row[CCA_VEHICLE_COST] - row[CCA_VEHICLE_GOVERNMENT_ASSISTANCE]
            if actual_cost > prescribed:
                applied = True
                factor = ExactFraction(prescribed) / ExactFraction(actual_cost)
                adjusted_proceeds = self._rounding.apply(ExactFraction(proceeds) * factor)
                adjusted_diep_proceeds = self._rounding.apply(ExactFraction(diep_proceeds) * factor)
        record: dict[ArtifactKind[Any], Decimal | int] = {
            field: row[field] for field in self._output.fields
        }
        record[CCA_PROCEEDS] = adjusted_proceeds
        record[CCA_DIEP_PROCEEDS] = adjusted_diep_proceeds
        line = CcaVehicleProceedsLine(
            self._output,
            position,
            applied,
            prescribed,
            actual_cost,
            proceeds,
            adjusted_proceeds,
            diep_proceeds,
            adjusted_diep_proceeds,
        )
        return line, record
