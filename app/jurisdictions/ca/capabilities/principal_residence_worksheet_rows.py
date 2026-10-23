"""PrincipalResidenceWorksheetRows: the base of the capabilities of Form T2091(IND)-WS, the
Principal Residence Worksheet, and of Part 4 of Form T2091(IND), not registered itself.

Part 4 of Form T2091(IND) applies to a property for which Form T664 or T664(Seniors) was filed
(the 1994 capital gains election). The worksheet works that property's figures: Chart 1 (lines
14 to 19), Part 1 (lines 21 to 27) and Part 3 (lines 59 to 66). Part 4 takes line 66 as the
reduction (line 56) of the total capital gain (line 55, line 54 of Part 3), floored at 0 (line
57). Each property is worked on its own, as in `PrincipalResidenceRows`, which supplies its Part
1 and Part 2 lines. A property not filed has every worksheet line 0 and not completed, and its
line 57 is its line 54. Worksheet Part 2 (lines 28 to 58) is not built: a property filed with
Part 2 applying is refused with a ValidationError.

Line 16 multiplies line 14 by the printed factor of the `chart_1_factor` dataset and rounds it
with that dataset's rule; lines 26 and 63 divide and round with the `rounding` dataset's rule. A
filed property whose years owned before 1995 (lines 4 and 5, so line 6) are 0, or whose months
owned after 1971 (line 62) are 0, is refused, as the quotient would have no divisor. Every other
line is exact.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, ClassVar

from app.domain.artifact import Artifact, ArtifactKind
from app.domain.capabilities.apply_ratio import ApplyRatio
from app.domain.errors import ValidationError
from app.domain.parameters.datasets import ParameterDataset
from app.domain.parameters.factor import FACTOR, Factor
from app.domain.parameters.kind import ParameterKind
from app.domain.parameters.rounding import RoundingRule
from app.domain.parameters.rounding_only import ROUNDING_ONLY, RoundingOnly
from app.domain.record_list import Record, RecordList
from app.jurisdictions.ca.capabilities.principal_residence_rows import (
    PrincipalResidenceRow,
    PrincipalResidenceRows,
)
from app.jurisdictions.ca.catalog import (
    RESIDENCE_T664_FILED,
    RESIDENCE_WS_ADJUSTED_COST_BASE_FEB_22_1994,
    RESIDENCE_WS_DESIGNATED_PROCEEDS,
    RESIDENCE_WS_ELECTED_CAPITAL_GAIN,
    RESIDENCE_WS_FMV_FEB_22_1994,
    RESIDENCE_WS_MONTHS_OWNED_AFTER_1971,
    RESIDENCE_WS_MONTHS_OWNED_AFTER_FEB_1992,
    RESIDENCE_WS_YEARS_DESIGNATED_AFTER_1981,
    RESIDENCE_WS_YEARS_OWNED_AFTER_1981,
)


@dataclass(frozen=True)
class PrincipalResidenceWorksheetRow:
    """One property's worksheet and Part 4 lines, by `position` (from 1).

    `filed` is True when Form T664 or T664(Seniors) was filed for the property, and
    `chart_completed` when Chart 1 applies (line 7 is more than line 10, and the election was
    filed). A line the form says not to complete is 0. The worksheet lines are `line_N` with N the
    worksheet's number. Copies of earlier figures are kept where a trace line reads them: `line_2`
    and `line_5` are the form's lines 2 and 6, `line_15` is line 7, `line_20` is line 8, and
    `line_54` is the property's total capital gain (Part 3 line 54, which is line 55 of Part 4).
    `factor` is the printed 1.1, `rounding` the worksheet's rule for lines 26 and 63, and
    `chart_rounding` the rule of line 16.
    """

    position: int
    filed: bool
    chart_completed: bool
    plus_one: int
    factor: Decimal
    rounding: RoundingRule
    chart_rounding: RoundingRule
    line_1: int
    line_2: int
    line_3: int
    line_4: int
    line_5: int
    line_6: int
    line_10: Decimal
    line_14: Decimal
    line_15: Decimal
    line_16: Decimal
    line_17: Decimal
    line_18: Decimal
    line_19: Decimal
    line_20: Decimal
    line_21: Decimal
    line_22: Decimal
    line_23: int
    line_24: Decimal
    line_26: Decimal
    line_27: Decimal
    line_54: Decimal
    line_56: Decimal
    line_57: Decimal
    line_59: Decimal
    line_60: int
    line_61: Decimal
    line_62: int
    line_63: Decimal
    line_64: Decimal
    line_65: Decimal
    line_66: Decimal


class PrincipalResidenceWorksheetRows(PrincipalResidenceRows):
    """Works the worksheet and Part 4 lines of each consumed property; a subclass produces
    `output` from the rows, one line per capability."""

    PARAMETERS: ClassVar[Mapping[str, ParameterKind[Any]]] = {
        "rounding": ROUNDING_ONLY,
        "chart_1_factor": FACTOR,
    }

    def __init__(
        self,
        rounding: ParameterDataset[RoundingOnly],
        chart_1_factor: ParameterDataset[Factor],
        properties: ArtifactKind[RecordList],
        output: ArtifactKind[Any],
    ) -> None:
        """Wire the rounding dataset, the Chart 1 factor dataset, the record list read and the kind
        the subclass produces."""
        super().__init__(rounding, properties, output)
        self._chart_1_factor = chart_1_factor

    def _worksheet_rows(
        self, inputs: tuple[Artifact[Any], ...]
    ) -> tuple[PrincipalResidenceWorksheetRow, ...]:
        """Each consumed property's worksheet and Part 4 lines, in order."""
        bases = self._rows(inputs)
        records = self._input(inputs, self._properties).value.records
        return tuple(
            self._worksheet_row(base, record) for base, record in zip(bases, records, strict=True)
        )

    def _worksheet_row(
        self, base: PrincipalResidenceRow, record: Record
    ) -> PrincipalResidenceWorksheetRow:
        """The worksheet and Part 4 lines of one property, from its Part 1 row and its record."""
        factor = self._chart_1_factor.values.value
        chart_rounding = self._chart_1_factor.rounding
        rule = self._rounding.rounding
        if record[RESIDENCE_T664_FILED] != 1:
            return self._not_filed(base, factor, chart_rounding, rule)
        if base.applies:
            raise ValidationError(
                f"property {base.position}: Part 2 of Form T2091(IND)-WS (lines 28 to 58) is not "
                "built, so a property with Form T664 filed and Part 2 applying cannot be worked"
            )
        zero = Decimal(0)
        line_1 = record[RESIDENCE_WS_YEARS_DESIGNATED_AFTER_1981]
        line_4 = record[RESIDENCE_WS_YEARS_OWNED_AFTER_1981]
        line_3 = line_1 + base.designated_before
        line_6 = line_4 + base.owned_before
        if line_6 == 0:
            raise ValidationError(
                f"property {base.position}: worksheet line 4 plus line 5 (line 6) is 0, "
                "so worksheet line 26 cannot be divided by it"
            )
        line_62 = record[RESIDENCE_WS_MONTHS_OWNED_AFTER_1971]
        if line_62 == 0:
            raise ValidationError(
                f"property {base.position}: worksheet line 62 (months owned after 1971) is 0, "
                "so worksheet line 63 cannot be divided by it"
            )
        # Chart 1: line 14 is the fair market value at February 22, 1994 (line 10); line 15 the
        # designated proceeds (line 7). Chart 1 applies only when line 15 is more than line 14.
        line_14 = record[RESIDENCE_WS_FMV_FEB_22_1994]
        line_15 = record[RESIDENCE_WS_DESIGNATED_PROCEEDS]
        chart = line_15 > line_14
        line_16 = (
            ApplyRatio.ratio_of(line_14, factor, Decimal(1), chart_rounding) if chart else zero
        )
        line_17 = max(zero, line_15 - line_16) if chart else zero
        line_18 = line_14 - line_17 if chart else zero
        line_19 = line_18 if chart else line_14
        # Part 1 of the worksheet.
        line_20 = record[RESIDENCE_WS_ADJUSTED_COST_BASE_FEB_22_1994]
        line_21 = line_19 - line_20
        line_22 = line_21
        line_23 = line_3 + base.plus_one
        line_24 = line_22 * line_23 + zero
        line_26 = ApplyRatio.ratio_of(line_24, Decimal(1), Decimal(line_6), rule)
        line_27 = line_21 - line_26
        # Part 3 of the worksheet.
        line_59 = line_27
        line_60 = record[RESIDENCE_WS_MONTHS_OWNED_AFTER_FEB_1992]
        line_61 = line_59 * line_60 + zero
        line_63 = ApplyRatio.ratio_of(line_61, Decimal(1), Decimal(line_62), rule)
        line_64 = line_59 - line_63
        line_65 = record[RESIDENCE_WS_ELECTED_CAPITAL_GAIN]
        line_66 = min(line_64, line_65)
        # Part 4 of Form T2091(IND): line 56 is worksheet line 66; line 57 is line 54 less it.
        line_56 = line_66
        line_57 = max(zero, base.line_54 - line_56)
        return PrincipalResidenceWorksheetRow(
            position=base.position,
            filed=True,
            chart_completed=chart,
            plus_one=base.plus_one,
            factor=factor,
            rounding=rule,
            chart_rounding=chart_rounding,
            line_1=line_1,
            line_2=base.designated_before,
            line_3=line_3,
            line_4=line_4,
            line_5=base.owned_before,
            line_6=line_6,
            line_10=line_14,
            line_14=line_14,
            line_15=line_15,
            line_16=line_16,
            line_17=line_17,
            line_18=line_18,
            line_19=line_19,
            line_20=line_20,
            line_21=line_21,
            line_22=line_22,
            line_23=line_23,
            line_24=line_24,
            line_26=line_26,
            line_27=line_27,
            line_54=base.line_54,
            line_56=line_56,
            line_57=line_57,
            line_59=line_59,
            line_60=line_60,
            line_61=line_61,
            line_62=line_62,
            line_63=line_63,
            line_64=line_64,
            line_65=line_65,
            line_66=line_66,
        )

    @staticmethod
    def _not_filed(
        base: PrincipalResidenceRow,
        factor: Decimal,
        chart_rounding: RoundingRule,
        rule: RoundingRule,
    ) -> PrincipalResidenceWorksheetRow:
        """The row of a property whose T664 election was not filed: every worksheet line is 0, and
        line 57 is its line 54."""
        zero = Decimal(0)
        return PrincipalResidenceWorksheetRow(
            position=base.position,
            filed=False,
            chart_completed=False,
            plus_one=base.plus_one,
            factor=factor,
            rounding=rule,
            chart_rounding=chart_rounding,
            line_1=0,
            line_2=base.designated_before,
            line_3=0,
            line_4=0,
            line_5=base.owned_before,
            line_6=0,
            line_10=zero,
            line_14=zero,
            line_15=zero,
            line_16=zero,
            line_17=zero,
            line_18=zero,
            line_19=zero,
            line_20=zero,
            line_21=zero,
            line_22=zero,
            line_23=0,
            line_24=zero,
            line_26=zero,
            line_27=zero,
            line_54=base.line_54,
            line_56=zero,
            line_57=base.line_54,
            line_59=zero,
            line_60=0,
            line_61=zero,
            line_62=0,
            line_63=zero,
            line_64=zero,
            line_65=zero,
            line_66=zero,
        )
