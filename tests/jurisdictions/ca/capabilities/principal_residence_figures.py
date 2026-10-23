"""Shared fixtures for the principal residence tests: one property's figures as one record of the
`ca/principal_residence_properties` record list, Form T2091(IND) Part 1 and Part 2. A property is
given as twelve figures in the order of the record's fields: the years designated after 1981 (line
1) and from 1972 to 1981 (line 2), the years owned in the same two periods (lines 5 and 6), the
proceeds (line 8), the outlays (line 9), the adjusted cost base (line 10), the "plus one" (1 if the
property may use it, else 0), whether Part 2 applies (1 if the property is one of two or more
principal residences a family member owned on December 31, 1981, and continuously until its
disposition, else 0), the adjusted cost base on December 31, 1981 (line 11), the fair market value
on December 31, 1981 (line 12) and the cost base adjustments after 1981 (line 13). A property that
does not use Part 2 may be given with the first eight figures only; the other four are then 0.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Any

from app.domain.artifact import Artifact, ArtifactKind
from app.domain.parameters.datasets import ParameterDataset
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
    RESIDENCE_YEARS_DESIGNATED_1972_TO_1981,
    RESIDENCE_YEARS_DESIGNATED_AFTER_1981,
    RESIDENCE_YEARS_OWNED_1972_TO_1981,
    RESIDENCE_YEARS_OWNED_AFTER_1981,
)

D = Decimal
CENT = RoundTo(D("0.01"), RoundingMode.HALF_UP)
DOLLAR_FLOOR = RoundTo(D("1"), RoundingMode.FLOOR)

Figures = tuple[int, int, int, int, str, str, str, int]
"""A property that does not use Part 2: lines 1, 2, 5, 6, 8, 9 and 10 and the "plus one"."""

Part2Figures = tuple[int, int, int, int, str, str, str, int, int, str, str, str]
"""A property with its Part 2 figures: the eight of `Figures`, whether Part 2 applies, then lines
11, 12 and 13."""


def part_2_figures(figures: Figures | Part2Figures) -> Part2Figures:
    """`figures` with the Part 2 figures added as 0 when it has only the first eight."""
    if len(figures) == 8:
        return (*figures, 0, "0.00", "0.00", "0.00")
    return figures


def property_record(figures: Figures | Part2Figures) -> dict[ArtifactKind[Any], object]:
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
    ) = part_2_figures(figures)
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
    }


def properties(*given: Figures | Part2Figures) -> Artifact[Any]:
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
