"""CcaTable: the base of the capabilities of the capital cost allowance table, not registered
itself.

T776 and T2125 Area A, "Calculation of capital cost allowance (CCA) claim", one row per class:
each record of the consumed list is one row, holding the caller's columns as the table takes them:
column 1 the class number, column 2 the UCC at the start, column 3 the additions, column 5 the
proceeds, column 11 the AIIP additions, column 12 the RIIP additions, the CCA claimed and whether
no property is left in the class (Note 3). Columns 4, 6, 8 and 9 (DIEPs) are taken as 0, so column
10 is column 3 and column 13 is column 7. Columns 11 and 12 are "Cost of remaining additions from
column 10", so a row whose columns 11 and 12 are above its column 3 is refused, as is a class the
`class_rates` dataset does not list (`InvalidRecordError`, naming the item).

As printed: column 7 is column 2 plus column 3 minus column 5; column 14 is column 5 minus column
10 plus columns 11 and 12; column 15 is column 11 minus column 14 times the class's AIIP factor
(Note 7); column 16 is column 14 minus column 11; column 17 is column 12 minus column 16 times the
class's RIIP factor (Note 8); column 18 is one half of column 10 minus columns 11, 12 and 5, or 0
for a class exempt from the half-year rule; each "If negative, enter "0"". Column 19 is column 13
plus columns 15 and 17 minus column 18, and the maximum is column 19 times the class's rate.
Columns 15, 17 and 18 and the maximum are worked as exact fractions and rounded once each with the
dataset's rule. Guide T4036 "Column 7": "You cannot claim CCA when the amount in column 7 is:
negative ... positive and you do not have any property left in that class ... In either case,
enter "0" in column 24", so the maximum and column 24 are 0 for those rows, for the recorded
`CcaZeroReason`. The claim is the caller's election, refused above the maximum
(`InputAboveBoundError`). Note 3: a negative column 7 is a recapture, and a positive one with no
property left a terminal loss, neither for a class the dataset excludes from them. A subclass is
one capability for each form line the table gives, building its own trace lines and output.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction as ExactFraction
from typing import Any, ClassVar

from app.domain.artifact import Artifact, ArtifactKind
from app.domain.capability import Capability
from app.domain.errors import InputAboveBoundError, InvalidRecordError
from app.domain.parameters.class_rates import (
    CLASS_RATES,
    ClassRate,
    ClassRates,
    HalfYearRule,
    RecaptureAndTerminalLoss,
)
from app.domain.parameters.datasets import ParameterDataset
from app.domain.parameters.kind import ParameterKind
from app.domain.parameters.rounding import RoundingRule
from app.domain.record_list import Record, RecordList
from app.jurisdictions.ca.catalog import (
    CCA_ADDITIONS,
    CCA_AIIP_ADDITIONS,
    CCA_CLAIMED,
    CCA_CLASS_NUMBER,
    CCA_NO_PROPERTY_LEFT,
    CCA_PROCEEDS,
    CCA_RIIP_ADDITIONS,
    CCA_UCC_AT_START,
)
from app.jurisdictions.ca.trace import CcaZeroReason

_ZERO = Decimal(0)


@dataclass(frozen=True)
class CcaRow:
    """One row of the table as the caller entered it, the class at `position` (from 1): its
    `class_number` (column 1), its `class_rate` from the dataset, columns 2, 3, 5, 11 and 12, the
    `claimed` CCA and `no_property_left` (1 if none, else 0); and `column_7`."""

    position: int
    class_number: Decimal
    class_rate: ClassRate
    ucc_at_start: Decimal
    additions: Decimal
    proceeds: Decimal
    aiip_additions: Decimal
    riip_additions: Decimal
    claimed: Decimal
    no_property_left: int

    @property
    def column_7(self) -> Decimal:
        """The UCC after additions and dispositions: column 2 plus column 3 minus column 5."""
        return self.ucc_at_start + self.additions - self.proceeds

    @property
    def zero_reason(self) -> CcaZeroReason:
        """Why the row allows no claim and closes at 0, if it does."""
        if self.column_7 < 0:
            return CcaZeroReason.COLUMN_7_NEGATIVE
        if self.column_7 > 0 and self.no_property_left:
            return CcaZeroReason.NO_PROPERTY_LEFT
        return CcaZeroReason.NONE

    @property
    def note_3_applies(self) -> bool:
        """Whether recapture and a terminal loss apply to the row's class."""
        return self.class_rate.recapture_and_terminal_loss is RecaptureAndTerminalLoss.APPLIES


@dataclass(frozen=True)
class CcaColumns:
    """Columns 14 to 19 of one row and its maximum, columns 15, 17 and 18 and the maximum rounded
    once each."""

    column_14: Decimal
    column_15: Decimal
    column_16: Decimal
    column_17: Decimal
    column_18: Decimal
    column_19: Decimal
    maximum: Decimal


class CcaTable(Capability):
    """Reads the consumed `classes`, one row each, with their classes from the `class_rates`
    dataset, and works the columns of a row; a subclass produces `output` from the rows."""

    PARAMETERS: ClassVar[Mapping[str, ParameterKind[ClassRates]]] = {"class_rates": CLASS_RATES}
    CONSUMES: ClassVar[Mapping[str, type]] = {"classes": RecordList}

    def __init__(
        self,
        class_rates: ParameterDataset[ClassRates],
        classes: ArtifactKind[RecordList],
        output: ArtifactKind[Any],
    ) -> None:
        """Wire the class-rate dataset and the record list read; the subclass keeps `output`."""
        super().__init__(classes=classes, output=output)
        self._class_rates = class_rates
        self._classes = classes

    def _rows(self, inputs: tuple[Artifact[Any], ...]) -> tuple[CcaRow, ...]:
        """Each consumed record, in order, as a row with its class found in the dataset."""
        records = self._input(inputs, self._classes).value.records
        return tuple(self._row(position, record) for position, record in enumerate(records, 1))

    def _row(self, position: int, record: Record) -> CcaRow:
        item = f"item {position}"
        class_number = Decimal(record[CCA_CLASS_NUMBER])
        class_rate = self._class_rates.values.for_class(class_number)
        if class_rate is None:
            raise InvalidRecordError(f"{item}: class {class_number} is not in the class rates")
        additions = Decimal(record[CCA_ADDITIONS])
        aiip_additions = Decimal(record[CCA_AIIP_ADDITIONS])
        riip_additions = Decimal(record[CCA_RIIP_ADDITIONS])
        if aiip_additions + riip_additions > additions:
            raise InvalidRecordError(
                f"{item}: columns 11 and 12 ({aiip_additions + riip_additions}) are above "
                f"column 3 ({additions})"
            )
        return CcaRow(
            position=position,
            class_number=class_number,
            class_rate=class_rate,
            ucc_at_start=Decimal(record[CCA_UCC_AT_START]),
            additions=additions,
            proceeds=Decimal(record[CCA_PROCEEDS]),
            aiip_additions=aiip_additions,
            riip_additions=riip_additions,
            # A non-negative field, so only a claim of -0 changes: it is 0.
            claimed=Decimal(record[CCA_CLAIMED]).copy_abs(),
            no_property_left=1 if record[CCA_NO_PROPERTY_LEFT] else 0,
        )

    def _columns(self, row: CcaRow) -> CcaColumns:
        """Columns 14 to 19 of `row` and its maximum, rounded with the dataset's rule; a claim
        above the maximum is an InputAboveBoundError naming the item."""
        rounding = self._class_rates.rounding
        rate = row.class_rate
        column_10 = row.additions
        column_14 = max(_ZERO, row.proceeds - column_10 + row.aiip_additions + row.riip_additions)
        column_15 = self._rounded(
            rounding,
            ExactFraction(row.aiip_additions - column_14)
            * rate.aiip_factor.numerator
            / rate.aiip_factor.denominator,
        )
        column_16 = max(_ZERO, column_14 - row.aiip_additions)
        column_17 = self._rounded(
            rounding,
            ExactFraction(row.riip_additions - column_16)
            * rate.riip_factor.numerator
            / rate.riip_factor.denominator,
        )
        net_additions = column_10 - row.aiip_additions - row.riip_additions - row.proceeds
        column_18 = (
            _ZERO
            if rate.half_year_rule is HalfYearRule.EXEMPT
            else self._rounded(rounding, ExactFraction(net_additions) / 2)
        )
        column_19 = row.column_7 + column_15 + column_17 - column_18
        maximum = (
            _ZERO
            if row.zero_reason is not CcaZeroReason.NONE
            else rounding.apply(column_19 * rate.rate.value)
        )
        if row.claimed > maximum:
            raise InputAboveBoundError(
                f"item {row.position}: {CCA_CLAIMED.identifier} {row.claimed} is above the "
                f"maximum {maximum}"
            )
        return CcaColumns(column_14, column_15, column_16, column_17, column_18, column_19, maximum)

    @staticmethod
    def _rounded(rounding: RoundingRule, exact: ExactFraction) -> Decimal:
        """`exact` rounded once with `rounding`, or 0 if it is negative ("If negative, enter
        "0"")."""
        return _ZERO if exact < 0 else rounding.apply(exact)
