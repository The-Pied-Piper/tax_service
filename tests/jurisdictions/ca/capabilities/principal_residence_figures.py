"""Shared fixtures for the principal residence tests: one property's figures as one record of the
`ca/principal_residence_properties` record list, Form T2091(IND) Part 1 and Part 2, and the
T2091(IND)-WS worksheet that Part 4 of Form T2091(IND) reads. A property is given as twelve figures
in the order of the record's fields: the years designated after 1981 (line 1) and from 1972 to 1981
(line 2), the years owned in the same two periods (lines 5 and 6), the proceeds (line 8), the
outlays (line 9), the adjusted cost base (line 10), the "plus one" (1 if the property may use it,
else 0), whether Part 2 applies (1 if the property is one of two or more principal residences a
family member owned on December 31, 1981, and continuously until its disposition, else 0), the
adjusted cost base on December 31, 1981 (line 11), the fair market value on December 31, 1981 (line
12) and the cost base adjustments after 1981 (line 13). A property that does not use Part 2 may be
given with the first eight figures only; the other four are then 0.

A property given with twenty-one figures also has its worksheet figures: whether Form T664 or
T664(Seniors) was filed for it (1 or 0), the years designated after 1981 and before 1995 (worksheet
line 1), the years owned in the same period (line 4), the designated proceeds (line 7), the adjusted
cost base at the end of February 22, 1994 (line 8), the fair market value at that date (line 10),
the elected capital gain (line 13), the months owned after February 1992 and before March 1994 (line
60) and the months owned after 1971 and before March 1994 (line 62). A property given with twelve or
eight figures has those nine as 0, and "0.00" for the money.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Any, cast

from app.domain.artifact import Artifact, ArtifactKind
from app.domain.parameters.datasets import ParameterDataset
from app.domain.parameters.factor import FACTOR, Factor
from app.domain.parameters.rounding import RoundingMode, RoundingRule, RoundTo
from app.domain.parameters.rounding_only import ROUNDING_ONLY, RoundingOnly
from app.domain.record_list import RecordList
from app.jurisdictions.ca.catalog import (
    PRINCIPAL_RESIDENCE_PROPERTIES,
    RESIDENCE_ADJUSTED_COST_BASE,
    RESIDENCE_ADJUSTED_COST_BASE_DEC_31_1981,
    RESIDENCE_COST_BASE_ADJUSTMENTS_AFTER_1981,
    RESIDENCE_FMV_DEC_31_1981,
    RESIDENCE_OUTLAYS,
    RESIDENCE_PART_2_APPLIES,
    RESIDENCE_PLUS_ONE_YEAR,
    RESIDENCE_PROCEEDS,
    RESIDENCE_T664_FILED,
    RESIDENCE_WS_ADJUSTED_COST_BASE_FEB_22_1994,
    RESIDENCE_WS_DESIGNATED_PROCEEDS,
    RESIDENCE_WS_ELECTED_CAPITAL_GAIN,
    RESIDENCE_WS_FMV_FEB_22_1994,
    RESIDENCE_WS_MONTHS_OWNED_AFTER_1971,
    RESIDENCE_WS_MONTHS_OWNED_AFTER_FEB_1992,
    RESIDENCE_WS_YEARS_DESIGNATED_AFTER_1981,
    RESIDENCE_WS_YEARS_OWNED_AFTER_1981,
    RESIDENCE_YEARS_DESIGNATED_1972_TO_1981,
    RESIDENCE_YEARS_DESIGNATED_AFTER_1981,
    RESIDENCE_YEARS_OWNED_1972_TO_1981,
    RESIDENCE_YEARS_OWNED_AFTER_1981,
)

D = Decimal
CENT = RoundTo(D("0.01"), RoundingMode.HALF_UP)
DOLLAR_FLOOR = RoundTo(D("1"), RoundingMode.FLOOR)
CHART_1_FACTOR_SOURCE = (
    "https://www.canada.ca/content/dam/cra-arc/formspubs/pbg/t2091ind-ws/t2091ind-ws-23e.pdf"
)

Figures = tuple[int, int, int, int, str, str, str, int]
"""A property that does not use Part 2: lines 1, 2, 5, 6, 8, 9 and 10 and the "plus one"."""

Part2Figures = tuple[int, int, int, int, str, str, str, int, int, str, str, str]
"""A property with its Part 2 figures: the eight of `Figures`, whether Part 2 applies, then lines
11, 12 and 13."""

WorksheetFigures = tuple[
    int,
    int,
    int,
    int,
    str,
    str,
    str,
    int,
    int,
    str,
    str,
    str,
    int,
    int,
    int,
    str,
    str,
    str,
    str,
    int,
    int,
]
"""A property with its worksheet figures: the twelve of `Part2Figures`, whether T664 was filed, then
worksheet lines 1, 4, 7, 8, 10 and 13 and lines 60 and 62."""


def part_2_figures(figures: Figures | Part2Figures) -> Part2Figures:
    """`figures` with the Part 2 figures added as 0 when it has only the first eight."""
    if len(figures) == 8:
        return (*figures, 0, "0.00", "0.00", "0.00")
    return figures


def worksheet_figures(figures: Figures | Part2Figures | WorksheetFigures) -> WorksheetFigures:
    """`figures` with the worksheet figures added as 0 (and "0.00") when it has fewer than 21."""
    if len(figures) == 21:
        return cast(WorksheetFigures, figures)
    twelve = part_2_figures(cast(Figures | Part2Figures, figures))
    return (*twelve, 0, 0, 0, "0.00", "0.00", "0.00", "0.00", 0, 0)


def property_record(
    figures: Figures | Part2Figures | WorksheetFigures,
) -> dict[ArtifactKind[Any], object]:
    """One property's record, with every field of `PRINCIPAL_RESIDENCE_PROPERTIES`."""
    (
        designated_after,
        designated_before,
        owned_after,
        owned_before,
        proceeds,
        outlays,
        cost_base,
        plus_one,
        part_2_applies,
        cost_base_1981,
        fmv_1981,
        adjustments_after_1981,
        t664_filed,
        worksheet_designated_after,
        worksheet_owned_after,
        designated_proceeds,
        worksheet_cost_base,
        worksheet_fmv,
        elected_gain,
        months_after_feb_1992,
        months_after_1971,
    ) = worksheet_figures(figures)
    return {
        RESIDENCE_YEARS_DESIGNATED_AFTER_1981: designated_after,
        RESIDENCE_YEARS_DESIGNATED_1972_TO_1981: designated_before,
        RESIDENCE_YEARS_OWNED_AFTER_1981: owned_after,
        RESIDENCE_YEARS_OWNED_1972_TO_1981: owned_before,
        RESIDENCE_PROCEEDS: D(proceeds),
        RESIDENCE_OUTLAYS: D(outlays),
        RESIDENCE_ADJUSTED_COST_BASE: D(cost_base),
        RESIDENCE_PLUS_ONE_YEAR: plus_one,
        RESIDENCE_PART_2_APPLIES: part_2_applies,
        RESIDENCE_ADJUSTED_COST_BASE_DEC_31_1981: D(cost_base_1981),
        RESIDENCE_FMV_DEC_31_1981: D(fmv_1981),
        RESIDENCE_COST_BASE_ADJUSTMENTS_AFTER_1981: D(adjustments_after_1981),
        RESIDENCE_T664_FILED: t664_filed,
        RESIDENCE_WS_YEARS_DESIGNATED_AFTER_1981: worksheet_designated_after,
        RESIDENCE_WS_YEARS_OWNED_AFTER_1981: worksheet_owned_after,
        RESIDENCE_WS_DESIGNATED_PROCEEDS: D(designated_proceeds),
        RESIDENCE_WS_ADJUSTED_COST_BASE_FEB_22_1994: D(worksheet_cost_base),
        RESIDENCE_WS_FMV_FEB_22_1994: D(worksheet_fmv),
        RESIDENCE_WS_ELECTED_CAPITAL_GAIN: D(elected_gain),
        RESIDENCE_WS_MONTHS_OWNED_AFTER_FEB_1992: months_after_feb_1992,
        RESIDENCE_WS_MONTHS_OWNED_AFTER_1971: months_after_1971,
    }


def properties(*given: Figures | Part2Figures | WorksheetFigures) -> Artifact[Any]:
    """A `ca/principal_residence_properties` artifact of one record per property, in the order
    given."""
    records = [property_record(figures) for figures in given]
    return Artifact(
        PRINCIPAL_RESIDENCE_PROPERTIES,
        RecordList(PRINCIPAL_RESIDENCE_PROPERTIES.fields, records),
    )


def rounding(rule: RoundingRule = CENT) -> ParameterDataset[RoundingOnly]:
    """The `ca/principal_residence_gain_rounding` dataset, rounding by `rule` (half up to the cent
    by default)."""
    return ParameterDataset(
        "ca/principal_residence_gain_rounding",
        2025,
        ROUNDING_ONLY,
        RoundingOnly(),
        rule,
        ("https://example.org/t2091",),
    )


def chart_1_factor(value: str = "1.1", rule: RoundingRule = CENT) -> ParameterDataset[Factor]:
    """The `ca/principal_residence_chart_1_factor` dataset: the printed factor `value` (1.1 by
    default), rounding line 16 by `rule` (half up to the cent by default)."""
    return ParameterDataset(
        "ca/principal_residence_chart_1_factor",
        2025,
        FACTOR,
        Factor(D(value)),
        rule,
        (CHART_1_FACTOR_SOURCE,),
    )


# Part 2 properties, worked by hand in the comments of the tests that use them. Each gives twelve
# figures: lines 1, 2, 5, 6, 8, 9, 10, the "plus one", whether Part 2 applies, lines 11, 12, 13.

# Worked example: line 18 = 300,000.00 - (100,000.00 + 5,000.00) = 195,000.00; line 20 = 7 + 1 = 8;
# line 21 = 1,560,000.00; line 23 = 1,560,000.00 / 14 = 111,428.57; line 24 = 83,571.43.
# Area A: line 27 = 90,000.00 - 40,000.00 = 50,000.00; line 29 = 1 + 1 = 2; line 30 = 100,000.00;
# line 32 = 100,000.00 / 4 = 25,000.00; line 33 = 25,000.00. Area B: line 38 = 90,000.00 + 10,000.00
# + 5,000.00 = 105,000.00; line 39 = 195,000.00; line 42 = 1,170,000.00; line 44 = 117,000.00;
# line 45 = 78,000.00. Area C gives line 48 = 0, the FMV being below the proceeds. Area D:
# line 51 = 25,000.00 + 78,000.00 = 103,000.00; line 53 = 103,000.00. Line 54 = 83,571.43.
PART_2_WORKED: Part2Figures = (
    6,
    1,
    10,
    4,
    "300000.00",
    "5000.00",
    "100000.00",
    1,
    1,
    "40000.00",
    "90000.00",
    "10000.00",
)

# Line 53 below line 24. Area A is skipped (2 designated of 2 owned before 1982). Line 18 =
# 200,000.00; line 20 = 4; line 21 = 800,000.00; line 23 = 800,000.00 / 12 = 66,666.67; line 24 =
# 133,333.33. Area B: line 38 = 280,000.00; line 39 = 20,000.00; line 42 = 40,000.00; line 44 =
# 4,000.00; line 45 = 16,000.00. Line 48 = 0. Line 53 = 16,000.00 and line 54 = 16,000.00.
PART_2_LESSER_IS_LINE_53: Part2Figures = (
    2,
    2,
    10,
    2,
    "300000.00",
    "0.00",
    "100000.00",
    0,
    1,
    "150000.00",
    "280000.00",
    "0.00",
)

# A post-1981 loss: the FMV on December 31, 1981 (120,000.00) is more than the proceeds
# (100,000.00), so area B is not worked and area C is: line 48 = 120,000.00 - 100,000.00 =
# 20,000.00. Area A: line 27 = 120,000.00 - 60,000.00 = 60,000.00; line 29 = 1 + 0 = 1; line 30 =
# 60,000.00; line 32 = 60,000.00 / 2 = 30,000.00; line 33 = 30,000.00. Line 51 = 30,000.00; line 53
# = 30,000.00 - 20,000.00 = 10,000.00. Part 1: line 18 = 50,000.00; line 20 = 4; line 21 =
# 200,000.00; line 23 = 33,333.33; line 24 = 16,666.67, so line 54 = 10,000.00.
PART_2_LOSS: Part2Figures = (
    3,
    1,
    4,
    2,
    "100000.00",
    "0.00",
    "50000.00",
    0,
    1,
    "60000.00",
    "120000.00",
    "0.00",
)

# Designated for every year after 1981 (4 of 4): area B is not worked, so line 45 and line 48 are 0
# even though the FMV (120,000.00) is more than the proceeds (100,000.00). Area A as in PART_2_LOSS:
# line 33 = 30,000.00; line 53 = 30,000.00 (not 10,000.00). Part 1: line 20 = 5; line 21 =
# 250,000.00; line 23 = 41,666.67; line 24 = 8,333.33, so line 54 = 8,333.33.
PART_2_ALL_YEARS_AFTER_1981: Part2Figures = (
    4,
    1,
    4,
    2,
    "100000.00",
    "0.00",
    "50000.00",
    0,
    1,
    "60000.00",
    "120000.00",
    "0.00",
)

# Designated for every year before 1982 (2 of 2): area A is not worked, so line 27 is 0 even though
# the FMV (40,000.00) is less than the adjusted cost base (60,000.00). Area B: line 38 = 40,000.00;
# line 39 = 60,000.00; line 42 = 60,000.00; line 44 = 20,000.00; line 45 = 40,000.00; line 48 = 0.
# Line 53 = 40,000.00. Part 1: line 20 = 3; line 21 = 150,000.00; line 23 = 30,000.00; line 24 =
# 20,000.00, so line 54 = 20,000.00.
PART_2_ALL_YEARS_BEFORE_1982: Part2Figures = (
    1,
    2,
    3,
    2,
    "100000.00",
    "0.00",
    "50000.00",
    0,
    1,
    "60000.00",
    "40000.00",
    "0.00",
)

# Area A with a division that does not end: line 32 = 50,000.00 / 3 = 16,666.67 (cent), 16,666
# (whole dollar, rounded down); line 33 = 33,333.33 or 33,334.
PART_2_ROUNDED_LINE_32: Part2Figures = (
    1,
    0,
    4,
    3,
    "300000.00",
    "0.00",
    "100000.00",
    1,
    1,
    "40000.00",
    "90000.00",
    "0.00",
)

# Area B with a division that does not end: line 44 = 100,000.00 / 3 = 33,333.33 (cent), 33,333
# (whole dollar); line 45 = 66,666.67 or 66,667. Area A is skipped (1 of 1 before 1982).
PART_2_ROUNDED_LINE_44: Part2Figures = (
    1,
    1,
    3,
    1,
    "100000.00",
    "0.00",
    "50000.00",
    0,
    1,
    "0.00",
    "0.00",
    "0.00",
)

# Area B with a tie at the cent: line 44 = 1.00 / 8 = 0.125, rounded half up to 0.13 (whole dollar,
# 0); line 45 = 1.00 - 0.13 = 0.87. Area A is worked on 0 of 1 years owned before 1982, with line
# 27 = 0.00 - 0.00 = 0.00.
PART_2_HALF_CENT_LINE_44: Part2Figures = (
    1,
    0,
    8,
    1,
    "1.00",
    "0.00",
    "0.00",
    0,
    1,
    "0.00",
    "0.00",
    "0.00",
)

# A property that does not use Part 2, with figures that would otherwise be worked.
PART_2_NOT_APPLYING: Part2Figures = (
    6,
    1,
    10,
    4,
    "300000.00",
    "5000.00",
    "100000.00",
    1,
    0,
    "40000.00",
    "90000.00",
    "10000.00",
)

# No years owned at all: refused, as line 23 divides by them, whatever the Part 2 figures.
PART_2_NO_YEARS_OWNED: Part2Figures = (
    0,
    0,
    0,
    0,
    "300000.00",
    "5000.00",
    "100000.00",
    1,
    1,
    "40000.00",
    "90000.00",
    "10000.00",
)

# --- The worksheet properties, worked by hand in the tests that use them -----------------------

# Worked example of the ticket, with T664 filed. Owned 1983 to 1994 (12 years, worksheet line 4)
# and designated 1983 to 1987 (5 years, line 1); nothing before 1982. T2091 Part 1: line 18 =
# 400,000.00 - 100,000.00 = 300,000.00; line 20 = 5 + 0 + 1 = 6; line 21 = 1,800,000.00; line 23 =
# 150,000.00 (12 years), so line 54 = 150,000.00 (no Part 2). Worksheet: line 3 = 5; line 6 = 12;
# line 7 (200,000.00) is not more than line 10 (200,000.00), so no Chart 1 and line 19 = 200,000.00;
# line 21 = 200,000.00 - 100,000.00 = 100,000.00; line 23 = 5 + 1 = 6; line 24 = 600,000.00;
# line 26 = 600,000.00 / 12 = 50,000.00; line 27 = 50,000.00; line 59 = 50,000.00; line 60 = 24
# months, line 61 = 1,200,000.00; line 62 = 74 months, line 63 = 16,216.22; line 64 = 33,783.78;
# line 65 = 100,000.00, so line 66 = 33,783.78. T2091 line 56 = 33,783.78; line 57 = 116,216.22.
WORKSHEET_WORKED: WorksheetFigures = (
    5,
    0,
    12,
    0,
    "400000.00",
    "0.00",
    "100000.00",
    1,
    0,
    "0.00",
    "0.00",
    "0.00",
    1,
    5,
    12,
    "200000.00",
    "100000.00",
    "200000.00",
    "100000.00",
    24,
    74,
)

# The worked example with T664 not filed: no worksheet line is completed, so every one is 0, and
# line 57 is line 54 (150,000.00) unchanged; the figures are the example's, election unused.
WORKSHEET_NOT_FILED: WorksheetFigures = (
    5,
    0,
    12,
    0,
    "400000.00",
    "0.00",
    "100000.00",
    1,
    0,
    "0.00",
    "0.00",
    "0.00",
    0,
    5,
    12,
    "200000.00",
    "100000.00",
    "200000.00",
    "100000.00",
    24,
    74,
)

# Chart 1 applies: line 7 (230,000.00) is more than line 10 (200,000.00). Line 14 = 200,000.00;
# line 15 = 230,000.00; line 16 = 200,000.00 x 1.1 = 220,000.00; line 17 = 230,000.00 - 220,000.00 =
# 10,000.00; line 18 = 200,000.00 - 10,000.00 = 190,000.00; line 19 = 190,000.00. Then line 21 =
# 190,000.00 - 100,000.00 = 90,000.00; line 24 = 90,000.00 x 6 = 540,000.00; line 26 = 45,000.00;
# line 27 = 45,000.00; line 61 = 1,080,000.00; line 63 = 14,594.59; line 64 = 30,405.41; line 66 =
# 30,405.41; T2091 line 57 = 150,000.00 - 30,405.41 = 119,594.59.
WORKSHEET_CHART_1: WorksheetFigures = (
    5,
    0,
    12,
    0,
    "400000.00",
    "0.00",
    "100000.00",
    1,
    0,
    "0.00",
    "0.00",
    "0.00",
    1,
    5,
    12,
    "230000.00",
    "100000.00",
    "200000.00",
    "100000.00",
    24,
    74,
)

# Chart 1 with line 7 (500,000.00) far above line 10 (200,000.00): line 16 = 220,000.00; line 17 =
# 500,000.00 - 220,000.00 = 280,000.00; line 18 = 200,000.00 - 280,000.00 = -80,000.00, which the
# form does not floor, so line 19 = -80,000.00 and line 21 = -180,000.00.
WORKSHEET_CHART_1_NEGATIVE: WorksheetFigures = (
    5,
    0,
    12,
    0,
    "400000.00",
    "0.00",
    "100000.00",
    1,
    0,
    "0.00",
    "0.00",
    "0.00",
    1,
    5,
    12,
    "500000.00",
    "100000.00",
    "200000.00",
    "100000.00",
    24,
    74,
)

# Chart 1 with a line 10 of 100,000.05, so line 16 = 110,000.055 before rounding: half up to the
# cent it is 110,000.06, and under a whole-dollar rule 110,000.
WORKSHEET_CHART_1_CENTS: WorksheetFigures = (
    5,
    0,
    12,
    0,
    "400000.00",
    "0.00",
    "100000.00",
    1,
    0,
    "0.00",
    "0.00",
    "0.00",
    1,
    5,
    12,
    "200000.00",
    "0.00",
    "100000.05",
    "100000.00",
    24,
    74,
)

# Line 26 does not end: line 24 = 200,000.00 x 2 = 400,000.00 and line 25 = 3 years, so line 26 =
# 133,333.33 (cent) or 133,333 (whole dollar, rounded down); line 27 = 200,000.00 - line 26.
# T2091 owns 3 years after 1981 with 1 designated and the "plus one": line 23 = 1 + 1 = 2.
WORKSHEET_ROUNDED_LINE_26: WorksheetFigures = (
    1,
    0,
    3,
    0,
    "300000.00",
    "0.00",
    "100000.00",
    1,
    0,
    "0.00",
    "0.00",
    "0.00",
    1,
    1,
    3,
    "0.00",
    "0.00",
    "200000.00",
    "300000.00",
    12,
    36,
)

# Line 63 is a half cent: line 27 = 1.00 (line 21 = 1.00 - 0.00, line 26 = 0 since line 23 is 0), so
# line 61 = 1.00 x 1 = 1.00 and line 63 = 1.00 / 8 = 0.125, half up to 0.13; line 64 = 0.87; line
# 66 = lesser of 0.87 and 5.00 = 0.87. T2091 line 57 = 1.00 - 0.87 = 0.13 (line 54 is 1.00).
WORKSHEET_HALF_CENT_LINE_63: WorksheetFigures = (
    0,
    0,
    1,
    0,
    "1.00",
    "0.00",
    "0.00",
    0,
    0,
    "0.00",
    "0.00",
    "0.00",
    1,
    0,
    1,
    "0.00",
    "0.00",
    "1.00",
    "5.00",
    1,
    8,
)

# Line 66 is the lesser of line 64 and line 65, and the reduction is larger than the gain: T2091
# line 54 is 20,000.00 (line 24 of Part 1: 100,000.00 - 60,000.00 = 40,000.00; line 21 = 40,000.00 x
# 6 = 240,000.00; line 23 = 240,000.00 / 12 = 20,000.00; line 24 = 20,000.00). The worksheet's line
# 66 is 33,783.78 as in the worked example, so line 57 = max(0, 20,000.00 - 33,783.78) = 0.
WORKSHEET_REDUCTION_EXCEEDS_GAIN: WorksheetFigures = (
    5,
    0,
    12,
    0,
    "100000.00",
    "0.00",
    "60000.00",
    1,
    0,
    "0.00",
    "0.00",
    "0.00",
    1,
    5,
    12,
    "200000.00",
    "100000.00",
    "200000.00",
    "100000.00",
    24,
    74,
)

# T664 filed and Part 2 applies: refused, as the worksheet's Part 2 (lines 28 to 58) is not built.
WORKSHEET_FILED_WITH_PART_2: WorksheetFigures = (
    6,
    1,
    10,
    4,
    "300000.00",
    "5000.00",
    "100000.00",
    1,
    1,
    "40000.00",
    "90000.00",
    "10000.00",
    1,
    6,
    10,
    "200000.00",
    "100000.00",
    "200000.00",
    "100000.00",
    24,
    74,
)

# The same property, T664 not filed: Part 2 of the worksheet is not needed, so not refused.
WORKSHEET_NOT_FILED_WITH_PART_2: WorksheetFigures = (
    6,
    1,
    10,
    4,
    "300000.00",
    "5000.00",
    "100000.00",
    1,
    1,
    "40000.00",
    "90000.00",
    "10000.00",
    0,
    6,
    10,
    "200000.00",
    "100000.00",
    "200000.00",
    "100000.00",
    24,
    74,
)

# T664 filed with no worksheet years owned before 1995 (line 4 is 0, and line 5 is 0 too): line 6
# is 0 and line 26 divides by it, so the property is refused.
WORKSHEET_NO_YEARS_OWNED_1995: WorksheetFigures = (
    5,
    0,
    12,
    0,
    "400000.00",
    "0.00",
    "100000.00",
    1,
    0,
    "0.00",
    "0.00",
    "0.00",
    1,
    5,
    0,
    "200000.00",
    "100000.00",
    "200000.00",
    "100000.00",
    24,
    74,
)

# T664 filed with no months owned after 1971 (line 62 is 0): line 63 divides by it, so refused.
WORKSHEET_NO_MONTHS_AFTER_1971: WorksheetFigures = (
    5,
    0,
    12,
    0,
    "400000.00",
    "0.00",
    "100000.00",
    1,
    0,
    "0.00",
    "0.00",
    "0.00",
    1,
    5,
    12,
    "200000.00",
    "100000.00",
    "200000.00",
    "100000.00",
    24,
    0,
)

# The worked example with an elected capital gain of 20,000.00 (line 13), less than line 64 of
# 33,783.78: line 66 = the lesser, 20,000.00.
WORKSHEET_SMALL_ELECTION: WorksheetFigures = (
    5,
    0,
    12,
    0,
    "400000.00",
    "0.00",
    "100000.00",
    1,
    0,
    "0.00",
    "0.00",
    "0.00",
    1,
    5,
    12,
    "200000.00",
    "100000.00",
    "200000.00",
    "20000.00",
    24,
    74,
)
