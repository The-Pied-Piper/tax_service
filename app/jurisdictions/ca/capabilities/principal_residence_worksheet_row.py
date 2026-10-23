"""PrincipalResidenceWorksheetRow: one property's lines of Form T2091(IND)-WS and of Part 4 of Form
T2091(IND), as `PrincipalResidenceWorksheetRows` works them.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from app.domain.parameters.rounding import RoundingRule


@dataclass(frozen=True)
class PrincipalResidenceWorksheetRow:
    """One property's worksheet and Part 4 lines, by `position` (from 1).

    `filed` is True when Form T664 or T664(Seniors) was filed for the property, and
    `chart_completed` when Chart 1 applies (line 7 is more than line 10, and the election was
    filed). A line the form says not to complete is 0. The worksheet lines are `line_N` with N the
    worksheet's number. Copies of earlier figures are kept where a trace line reads them: `line_2`
    and `line_5` are the form's lines 2 and 6, `line_15` is line 7, `line_20` is line 8, and
    `line_54` is the property's total capital gain (Part 3 line 54, which is line 55 of Part 4).
    Lines 28 to 58 are Part 2 (`part_2_completed` when the election was filed and Part 2 of Form
    T2091(IND) applies; `pre_1982_completed`, `post_1981_completed` and `post_1981_loss_completed`
    for areas A, B and C); its lines 56 and 57 are `part_2_line_56` and `part_2_line_57`, as
    `line_56` and `line_57` are those of Part 4. `line_59` is line 58 when Part 2 is completed,
    else line 27. `factor` is the printed 1.1, `rounding` the worksheet's rule for
    lines 26, 35, 46 and 63, and `chart_rounding` the rule of line 16.
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
    part_2_completed: bool
    pre_1982_completed: bool
    post_1981_completed: bool
    post_1981_loss_completed: bool
    line_28: Decimal
    line_29: Decimal
    line_30: Decimal
    line_31: Decimal
    line_32: int
    line_33: Decimal
    line_34: int
    line_35: Decimal
    line_36: Decimal
    line_37: Decimal
    line_38: Decimal
    line_39: Decimal
    line_40: Decimal
    line_41: Decimal
    line_42: Decimal
    line_43: int
    line_44: Decimal
    line_45: int
    line_46: Decimal
    line_47: Decimal
    line_48: Decimal
    line_49: Decimal
    line_50: Decimal
    line_51: Decimal
    line_52: Decimal
    line_53: Decimal
    part_2_line_54: Decimal
    line_55: Decimal
    part_2_line_56: Decimal
    part_2_line_57: Decimal
    line_58: Decimal
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
