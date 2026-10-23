"""PrincipalResidenceWorksheetPart2: Part 2 of Form T2091(IND)-WS (lines 28 to 58) of one property.

Part 2 is completed for a property for which Form T664 or T664(Seniors) was filed and for which
Part 2 of Form T2091(IND) applies. It has areas A (adjusted pre-1982 gain, lines 28 to 36), B
(adjusted post-1981 gain, lines 37 to 47), C (adjusted post-1981 loss, lines 48 to 50), D (net
adjusted gain, lines 51 to 55) and E (the lesser of lines 56 and 57, line 58). A line the form says
not to complete is 0, and so is every line of a property whose Part 2 is not completed. Only the
ratios of lines 35 and 46 are rounded, with the worksheet's rounding rule.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from app.domain.capabilities.apply_ratio import ApplyRatio
from app.domain.parameters.rounding import RoundingRule


@dataclass(frozen=True)
class PrincipalResidenceWorksheetPart2:
    """The Part 2 lines of one property, `line_N` with N the worksheet's number.

    `completed` is True when Part 2 is completed (the election filed and Part 2 of Form T2091(IND)
    applying), and `area_a`, `area_b` and `area_c` when the area is completed rather than skipped.
    Line 56 is the property's line 27 and line 57 its line 55.
    """

    completed: bool
    area_a: bool
    area_b: bool
    area_c: bool
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
    line_54: Decimal
    line_55: Decimal
    line_56: Decimal
    line_57: Decimal
    line_58: Decimal

    @classmethod
    def not_completed(cls) -> PrincipalResidenceWorksheetPart2:
        """Part 2 of a property whose election was not filed or whose Part 2 does not apply: every
        line is 0."""
        zero = Decimal(0)
        return cls(
            completed=False,
            area_a=False,
            area_b=False,
            area_c=False,
            line_28=zero,
            line_29=zero,
            line_30=zero,
            line_31=zero,
            line_32=0,
            line_33=zero,
            line_34=0,
            line_35=zero,
            line_36=zero,
            line_37=zero,
            line_38=zero,
            line_39=zero,
            line_40=zero,
            line_41=zero,
            line_42=zero,
            line_43=0,
            line_44=zero,
            line_45=0,
            line_46=zero,
            line_47=zero,
            line_48=zero,
            line_49=zero,
            line_50=zero,
            line_51=zero,
            line_52=zero,
            line_53=zero,
            line_54=zero,
            line_55=zero,
            line_56=zero,
            line_57=zero,
            line_58=zero,
        )

    @classmethod
    def worked(
        cls,
        *,
        line_1: int,
        line_2: int,
        line_4: int,
        line_5: int,
        plus_one: int,
        line_9: Decimal,
        line_11: Decimal,
        line_12: Decimal,
        line_19: Decimal,
        line_27: Decimal,
        rounding: RoundingRule,
    ) -> PrincipalResidenceWorksheetPart2:
        """Part 2 of a property for which it is completed, from the worksheet's lines 1, 2, 4, 5,
        12, 19 and 27, the "plus one", and lines 9 and 11 (lines 11 and 12 of Form T2091(IND))."""
        zero = Decimal(0)
        area_a = line_2 < line_5
        area_b = line_1 < line_4 and line_11 <= line_19
        area_c = line_1 < line_4
        # A. Adjusted pre-1982 gain.
        line_28 = line_11 if area_a else zero
        line_29 = line_9 if area_a else zero
        line_30 = line_28 - line_29
        line_32 = line_2 + plus_one if area_a else 0
        line_33 = line_30 * line_32 + zero
        line_34 = line_5 if area_a else 0
        line_35 = (
            ApplyRatio.ratio_of(line_33, Decimal(1), Decimal(line_34), rounding) if area_a else zero
        )
        line_36 = max(zero, line_30 - line_35)
        # B. Adjusted post-1981 gain.
        line_37 = line_19 if area_b else zero
        line_38 = line_11 if area_b else zero
        line_39 = line_12 if area_b else zero
        line_40 = line_38 + line_39
        line_41 = line_37 - line_40
        line_43 = line_1 if area_b else 0
        line_44 = line_41 * line_43 + zero
        line_45 = line_4 if area_b else 0
        line_46 = (
            ApplyRatio.ratio_of(line_44, Decimal(1), Decimal(line_45), rounding) if area_b else zero
        )
        line_47 = max(zero, line_41 - line_46)
        # C. Adjusted post-1981 loss.
        line_48 = line_11 if area_c else zero
        line_49 = line_19 if area_c else zero
        line_50 = max(zero, line_48 - line_49)
        # D. Net adjusted gain, and E. the lesser of lines 56 and 57.
        line_53 = line_36 + line_47
        line_55 = max(zero, line_53 - line_50)
        return cls(
            completed=True,
            area_a=area_a,
            area_b=area_b,
            area_c=area_c,
            line_28=line_28,
            line_29=line_29,
            line_30=line_30,
            line_31=line_30,
            line_32=line_32,
            line_33=line_33,
            line_34=line_34,
            line_35=line_35,
            line_36=line_36,
            line_37=line_37,
            line_38=line_38,
            line_39=line_39,
            line_40=line_40,
            line_41=line_41,
            line_42=line_41,
            line_43=line_43,
            line_44=line_44,
            line_45=line_45,
            line_46=line_46,
            line_47=line_47,
            line_48=line_48,
            line_49=line_49,
            line_50=line_50,
            line_51=line_36,
            line_52=line_47,
            line_53=line_53,
            line_54=line_50,
            line_55=line_55,
            line_56=line_27,
            line_57=line_55,
            line_58=min(line_27, line_55),
        )
