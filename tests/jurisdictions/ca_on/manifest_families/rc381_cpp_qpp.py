"""The CA-ON manifest entries of one family of lines (see `test_manifest.py`).

Form RC381 (2025), "Inter-Provincial Calculation for CPP and QPP Contributions and Overpayments",
Part 2 and Part 3 lines 1 to 26 (`08a_rc381_part_2_and_3.yaml`, the first of several wiring PRs),
then Part 3 lines 27 to 69 on the QPP side and the totals (`08b_rc381_part_3_qpp_and_totals.yaml`,
the second), then Part 3a and Part 3b, lines 70 to 93, and the three results for earnings from
employment income only (`08c_rc381_part_3a_and_3b.yaml`, the third; lines 70, 71, 72 and 74 only
copy lines 52, 59, 67 and 69, so they have no step of their own), then Part 4 lines 1 to 27, the
CPP side of the self-employment calculation before the QPP gross-up
(`08d_rc381_part_4_lines_1_to_27.yaml`, the fourth; lines 1 to 3, 5, 6, 7, 9, 10, 15, 16, 18, 19
and 25 only copy or enter other artifacts, so they have no step of their own), then Part 4 lines 31
to 56, the QPP side before its gross-up, line 42 and the second additional contributions and the
totals (`08e_rc381_part_4_lines_31_to_56.yaml`, the fifth; lines 28, 29, 30, 37, 43, 44, 45, 48, 49
and 50 only copy or enter other artifacts, so they have no step of their own), then Part 4 lines 57
to 91, the earnings subject to contributions, the self-employed contributions, the contributions
payable and the overpayment (`08f_rc381_part_4_lines_59_to_91.yaml`, the sixth; lines 57, 58, 60,
63, 64, 66, 67, 71, 72, 73, 75, 78, 79 and 81 only copy other artifacts, so they have no step of
their own). Part 2 lines C to F are Schedule 8 Part 2's lines B to E, the same table read with
the same months (line A), so they are the existing artifacts and no step is repeated for them.
Lines 43 and 46 print the figures of lines 23 and 26, so they read the same datasets.
"""

from __future__ import annotations

from app.domain.capabilities.amount_by_count import AmountForCount
from app.domain.capabilities.apply_fraction import ApplyFraction
from app.domain.capabilities.apply_rate import ApplyRate
from app.domain.capabilities.contribution_tier import TieredContribution
from app.domain.capabilities.lesser_of import LesserOf
from app.domain.capabilities.subtract import Subtract
from app.domain.capabilities.subtract_not_below_zero import SubtractNotBelowZero
from app.domain.capabilities.sum import Sum
from app.domain.capabilities.sum_not_below_zero import SumNotBelowZero
from app.domain.manifest import CapabilitySelection
from app.jurisdictions.ca.capabilities.amount_when_more import AmountWhenMore
from app.jurisdictions.ca.capabilities.apply_chosen_rate import ApplyChosenRate
from app.jurisdictions.ca.capabilities.choose_by_sign import ChooseBySign
from app.jurisdictions.ca.capabilities.count_at_least import CountAtLeast
from app.jurisdictions.ca.capabilities.divided_by_rate import DividedByRate
from app.jurisdictions.ca.capabilities.lesser_of_when_positive import (
    LesserOfWhenPositive,
    LesserOfWhenPositiveInBrackets,
)
from app.jurisdictions.ca.capabilities.positive_part_of_negation import PositivePartOfNegation
from app.jurisdictions.ca.capabilities.ratio_truncated import (
    RatioTruncated,
    RatioTruncatedAtMostOne,
)
from app.jurisdictions.ca.catalog import (
    CPP_ADDITIONAL_MAXIMUM_PENSIONABLE_EARNINGS,
    CPP_BASIC_EXEMPTION,
    CPP_MAXIMUM_PENSIONABLE_EARNINGS,
    CPP_MONTHS,
    CPP_SECOND_ADDITIONAL_EARNINGS_MAXIMUM,
    CPT20_EARNINGS,
    CPT20_T4_EARNINGS,
    PENSIONABLE_NET_SELF_EMPLOYMENT_EARNINGS,
    QPP_MONTHS,
    RC381_CPP_OVERPAYMENT,
    RC381_EMPLOYMENT_CPP_BASE_CONTRIBUTIONS,
    RC381_EMPLOYMENT_CPP_ENHANCED_CONTRIBUTIONS,
    RC381_PART_2_LINE_B,
    RC381_PART_2_LINE_G,
    RC381_PART_2_LINE_H,
    RC381_PART_2_LINE_I,
    RC381_PART_2_LINE_J,
    RC381_PART_3_LINE_3,
    RC381_PART_3_LINE_6,
    RC381_PART_3_LINE_7,
    RC381_PART_3_LINE_8,
    RC381_PART_3_LINE_9,
    RC381_PART_3_LINE_10,
    RC381_PART_3_LINE_11,
    RC381_PART_3_LINE_14,
    RC381_PART_3_LINE_15,
    RC381_PART_3_LINE_15_LESSER,
    RC381_PART_3_LINE_16,
    RC381_PART_3_LINE_18,
    RC381_PART_3_LINE_20,
    RC381_PART_3_LINE_21,
    RC381_PART_3_LINE_22,
    RC381_PART_3_LINE_23,
    RC381_PART_3_LINE_24,
    RC381_PART_3_LINE_26,
    RC381_PART_3_LINE_27,
    RC381_PART_3_LINE_28,
    RC381_PART_3_LINE_29,
    RC381_PART_3_LINE_30,
    RC381_PART_3_LINE_31,
    RC381_PART_3_LINE_34,
    RC381_PART_3_LINE_35,
    RC381_PART_3_LINE_35_LESSER,
    RC381_PART_3_LINE_36,
    RC381_PART_3_LINE_38,
    RC381_PART_3_LINE_40,
    RC381_PART_3_LINE_41,
    RC381_PART_3_LINE_42,
    RC381_PART_3_LINE_43,
    RC381_PART_3_LINE_44,
    RC381_PART_3_LINE_46,
    RC381_PART_3_LINE_49,
    RC381_PART_3_LINE_52,
    RC381_PART_3_LINE_53,
    RC381_PART_3_LINE_56,
    RC381_PART_3_LINE_59,
    RC381_PART_3_LINE_60,
    RC381_PART_3_LINE_61,
    RC381_PART_3_LINE_64,
    RC381_PART_3_LINE_67,
    RC381_PART_3_LINE_68,
    RC381_PART_3_LINE_69,
    RC381_PART_3_LINE_73,
    RC381_PART_3_LINE_75,
    RC381_PART_3_LINE_76,
    RC381_PART_3_LINE_77,
    RC381_PART_3_LINE_78,
    RC381_PART_3_LINE_79,
    RC381_PART_3_LINE_80,
    RC381_PART_3_LINE_81,
    RC381_PART_3_LINE_82,
    RC381_PART_3_LINE_83,
    RC381_PART_3_LINE_84,
    RC381_PART_3_LINE_85,
    RC381_PART_3_LINE_86,
    RC381_PART_3_LINE_87,
    RC381_PART_3_LINE_87_DIFFERENCE,
    RC381_PART_3_LINE_88,
    RC381_PART_3_LINE_89,
    RC381_PART_3_LINE_90,
    RC381_PART_3_LINE_91,
    RC381_PART_3_LINE_92,
    RC381_PART_3_LINE_93,
    RC381_PART_4_LINE_4,
    RC381_PART_4_LINE_8,
    RC381_PART_4_LINE_11,
    RC381_PART_4_LINE_12,
    RC381_PART_4_LINE_13,
    RC381_PART_4_LINE_13_DIFFERENCE,
    RC381_PART_4_LINE_14,
    RC381_PART_4_LINE_17,
    RC381_PART_4_LINE_17A,
    RC381_PART_4_LINE_20,
    RC381_PART_4_LINE_21,
    RC381_PART_4_LINE_21_FROM_LINE_17,
    RC381_PART_4_LINE_21_LESSER,
    RC381_PART_4_LINE_22,
    RC381_PART_4_LINE_23,
    RC381_PART_4_LINE_23_LESSER,
    RC381_PART_4_LINE_23_MULTIPLIED,
    RC381_PART_4_LINE_24,
    RC381_PART_4_LINE_24_LESSER,
    RC381_PART_4_LINE_25A,
    RC381_PART_4_LINE_26,
    RC381_PART_4_LINE_27,
    RC381_PART_4_LINE_31,
    RC381_PART_4_LINE_31_DIFFERENCE,
    RC381_PART_4_LINE_32,
    RC381_PART_4_LINE_33,
    RC381_PART_4_LINE_34,
    RC381_PART_4_LINE_35,
    RC381_PART_4_LINE_35A,
    RC381_PART_4_LINE_35AA,
    RC381_PART_4_LINE_35AA_FROM_LINE_17,
    RC381_PART_4_LINE_35AB,
    RC381_PART_4_LINE_35AB_FROM_LINE_20,
    RC381_PART_4_LINE_35AB_WHEN_LINE_35_ZERO,
    RC381_PART_4_LINE_36,
    RC381_PART_4_LINE_38,
    RC381_PART_4_LINE_39,
    RC381_PART_4_LINE_40,
    RC381_PART_4_LINE_41,
    RC381_PART_4_LINE_42,
    RC381_PART_4_LINE_46,
    RC381_PART_4_LINE_46_DIFFERENCE,
    RC381_PART_4_LINE_47,
    RC381_PART_4_LINE_51,
    RC381_PART_4_LINE_51_DIFFERENCE,
    RC381_PART_4_LINE_52,
    RC381_PART_4_LINE_53,
    RC381_PART_4_LINE_54,
    RC381_PART_4_LINE_55,
    RC381_PART_4_LINE_56,
    RC381_PART_4_LINE_59,
    RC381_PART_4_LINE_61,
    RC381_PART_4_LINE_62,
    RC381_PART_4_LINE_65,
    RC381_PART_4_LINE_68,
    RC381_PART_4_LINE_69,
    RC381_PART_4_LINE_70,
    RC381_PART_4_LINE_74,
    RC381_PART_4_LINE_76,
    RC381_PART_4_LINE_77,
    RC381_PART_4_LINE_80,
    RC381_PART_4_LINE_82,
    RC381_PART_4_LINE_83,
    RC381_PART_4_LINE_83_LESSER,
    RC381_PART_4_LINE_84,
    RC381_PART_4_LINE_85,
    RC381_PART_4_LINE_86,
    RC381_PART_4_LINE_87,
    RC381_PART_4_LINE_88,
    RC381_PART_4_LINE_89,
    RC381_PART_4_LINE_89_FROM_LINE_69,
    RC381_PART_4_LINE_90,
    RC381_PART_4_LINE_91,
    RC381_PART_4_LINE_91_FROM_LINE_90,
    RC381_SELF_EMPLOYMENT_CPP_CONTRIBUTIONS,
    T4_CPP_CONTRIBUTIONS_BOX_16,
    T4_CPP_PENSIONABLE_EARNINGS_OUTSIDE_QUEBEC,
    T4_CPP_SECOND_ADDITIONAL_BOX_16A,
    T4_QPP_CONTRIBUTIONS_BOX_17,
    T4_QPP_PENSIONABLE_EARNINGS_IN_QUEBEC,
    T4_QPP_SECOND_ADDITIONAL_BOX_17A,
)

# Part 2 line B and the Part 3 lines 1, 2, 19, 25, 39 and 45 are the filer's entries: line 25
# (box 16A, 50341) and line 45 (box 17A, 50331) are read by line 64, line 39 (box 17, 50330) by
# lines 40 and 41. Part 4 line 3 (50399) is the one entry of Part 4 lines 1 to 27 that Schedule 8
# does not have (line 1 and line 2, 50373, are Schedule 8 Part 4's), read by line 4.
INPUTS = frozenset(
    {
        "ca/cpt20_t4_earnings",
        "ca/qpp_months",
        "ca/t4_cpp_pensionable_earnings_outside_quebec",
        "ca/t4_qpp_pensionable_earnings_in_quebec",
        "ca/t4_cpp_contributions_box_16",
        "ca/t4_cpp_second_additional_box_16a",
        "ca/t4_qpp_contributions_box_17",
        "ca/t4_qpp_second_additional_box_17a",
    }
)

# Nothing reads these yet (the PR that routes the T1 lines reads them and removes them from this
# set): Part 4 line 90 "Line 88 minus 89. If positive, enter the amount (in dollars and
# cents) on line 42100 of your return", the amount for line 42100, and line 91 "amount from line 90
# entered as a positive amount × 50%", which the T1 lines read later, and the three results
# of Part 3a and Part 3b for earnings from employment income only, "Enter this amount (in dollars
# and cents) on line 30800 of your return.", "... on line 22215 of your return." and "... on line
# 44800 of your return.", which the T1 lines and Form ON428 line 19 and line 58240 read
# later. Part 4 line 4 "Add lines 1 to 3.", line 42 "Line 27 plus line 41" and line 56 "Line 53 plus
# line 55" are read by lines 62, 66, 71 and 78, line 60 and line 76 now.
OUTPUTS = frozenset(
    {
        "ca/rc381_self_employment_cpp_contributions",
        "ca/rc381_part_4_line_91",
        "ca/rc381_employment_cpp_base_contributions",
        "ca/rc381_employment_cpp_enhanced_contributions",
        "ca/rc381_cpp_overpayment",
    }
)

STEPS = {
    # Part 2 "The number you enter on line A cannot be more than the number you enter on line
    # B.": line B is the QPP months, produced unchanged when it is at least line A's months and
    # refused (an input error) when it is less; the QPP lookups below read this checked line B.
    CapabilitySelection(
        name="ca/count_at_least",
        params={},
        consumes={"count": "ca/qpp_months", "minimum": "ca/cpp_months"},
        produces={"output": "ca/rc381_part_2_line_b"},
    ),
    # Part 2 "Enter the corresponding amounts from the monthly proration table above using the
    # number of months from lines A and B." QPP: line G "Your maximum pensionable earnings for
    # 2025 (maximum $71,300)", line H "Your maximum amount subject to second additional
    # contributions for 2025 (maximum $9,900)", line I "Your additional maximum pensionable
    # earnings for 2025 (maximum $81,200)" and line J "Your maximum basic exemption for 2025
    # (maximum $3,500)": the row of the table for line B's months, the table of Schedule 8
    # Part 2 (lines C to F are the same table read with line A, the existing artifacts).
    CapabilitySelection(
        name="core/amount_by_count",
        params={"table": "ca/cpp_maximum_pensionable_earnings"},
        consumes={"count": "ca/rc381_part_2_line_b"},
        produces={"output": "ca/rc381_part_2_line_g"},
    ),
    CapabilitySelection(
        name="core/amount_by_count",
        params={"table": "ca/cpp_second_additional_earnings_maximum"},
        consumes={"count": "ca/rc381_part_2_line_b"},
        produces={"output": "ca/rc381_part_2_line_h"},
    ),
    CapabilitySelection(
        name="core/amount_by_count",
        params={"table": "ca/cpp_additional_maximum_pensionable_earnings"},
        consumes={"count": "ca/rc381_part_2_line_b"},
        produces={"output": "ca/rc381_part_2_line_i"},
    ),
    CapabilitySelection(
        name="core/amount_by_count",
        params={"table": "ca/cpp_basic_exemption"},
        consumes={"count": "ca/rc381_part_2_line_b"},
        produces={"output": "ca/rc381_part_2_line_j"},
    ),
    # Part 3 line 3 "Line 1 plus line 2 Total pensionable earnings", line 1 "Total CPP
    # pensionable earnings from box 26 of all of your T4 slips where the province of employment
    # is not Quebec" (50339) and line 2 "Total QPP pensionable earnings from box 26 of all of
    # your T4 slips where the province of employment is Quebec" (50329).
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/t4_cpp_pensionable_earnings_outside_quebec",
                "ca/t4_qpp_pensionable_earnings_in_quebec",
            )
        },
        produces={"output": "ca/rc381_part_3_line_3"},
    ),
    # Line 6 "Line 4 divided by line 5 (calculated to the fifth decimal place without
    # rounding)", line 4 "Amount from line 1" and line 5 "Amount from line 3": truncated, not
    # rounded, to 0.00001; 0 when line 3 is 0.
    CapabilitySelection(
        name="ca/ratio_truncated",
        params={"rounding": "ca/rc381_ratio_truncation"},
        consumes={
            "dividend": "ca/t4_cpp_pensionable_earnings_outside_quebec",
            "divisor": "ca/rc381_part_3_line_3",
        },
        produces={"output": "ca/rc381_part_3_line_6"},
    ),
    # Lines 7 to 10 "Amount from line E of Part 2 multiplied by the rate at line 6", "Amount from
    # line C of Part 2 ...", "Amount from line F of Part 2 ..." and "Amount from line D of Part
    # 2 ...": each product rounds half up to the cent.
    CapabilitySelection(
        name="ca/apply_chosen_rate",
        params={"rounding": "ca/rc381_cents_rounding"},
        consumes={
            "base": "ca/cpp_additional_maximum_pensionable_earnings",
            "rate": "ca/rc381_part_3_line_6",
        },
        produces={"output": "ca/rc381_part_3_line_7"},
    ),
    CapabilitySelection(
        name="ca/apply_chosen_rate",
        params={"rounding": "ca/rc381_cents_rounding"},
        consumes={
            "base": "ca/cpp_maximum_pensionable_earnings",
            "rate": "ca/rc381_part_3_line_6",
        },
        produces={"output": "ca/rc381_part_3_line_8"},
    ),
    CapabilitySelection(
        name="ca/apply_chosen_rate",
        params={"rounding": "ca/rc381_cents_rounding"},
        consumes={"base": "ca/cpp_basic_exemption", "rate": "ca/rc381_part_3_line_6"},
        produces={"output": "ca/rc381_part_3_line_9"},
    ),
    CapabilitySelection(
        name="ca/apply_chosen_rate",
        params={"rounding": "ca/rc381_cents_rounding"},
        consumes={
            "base": "ca/cpp_second_additional_earnings_maximum",
            "rate": "ca/rc381_part_3_line_6",
        },
        produces={"output": "ca/rc381_part_3_line_10"},
    ),
    # Line 11 "Earnings subject to CPP contributions: Enter whichever is less: amount from line
    # 1 or line 7."
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={
            "amounts": (
                "ca/t4_cpp_pensionable_earnings_outside_quebec",
                "ca/rc381_part_3_line_7",
            )
        },
        produces={"output": "ca/rc381_part_3_line_11"},
    ),
    # Line 14 "Line 12 minus line 13 (if negative, enter "0")", line 12 "Amount from line 11"
    # and line 13 "Amount from line 8".
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={"amount": "ca/rc381_part_3_line_11", "less": "ca/rc381_part_3_line_8"},
        produces={"output": "ca/rc381_part_3_line_14"},
    ),
    # Line 15 "Earnings subject to second additional CPP contributions: Enter whichever is less:
    # amount from line 10 or line 14.", which line 3's instruction "If the amount from line 3 is
    # more than the amount from line C of Part 2, complete lines 12 to 15. If not, enter the
    # amount from line 11 on line 16 and continue at line 17." makes 0 when it does not apply:
    # the lesser of lines 10 and 14 (the printed sub-calculation of line 15) ...
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={"amounts": ("ca/rc381_part_3_line_10", "ca/rc381_part_3_line_14")},
        produces={"output": "ca/rc381_part_3_line_15_lesser"},
    ),
    # ... and line 15 itself, that amount only when line 3 is more than line C.
    CapabilitySelection(
        name="ca/amount_when_more",
        params={},
        consumes={
            "amount": "ca/rc381_part_3_line_15_lesser",
            "more": "ca/rc381_part_3_line_3",
            "than": "ca/cpp_maximum_pensionable_earnings",
        },
        produces={"output": "ca/rc381_part_3_line_15"},
    ),
    # Line 16 "Line 11 minus line 15".
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ca/rc381_part_3_line_11", "less": "ca/rc381_part_3_line_15"},
        produces={"output": "ca/rc381_part_3_line_16"},
    ),
    # Line 18 "Earnings subject to base and first additional CPP contributions: Line 16 minus
    # line 17 (if negative, enter "0")", line 17 "Amount from line 9".
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={"amount": "ca/rc381_part_3_line_16", "less": "ca/rc381_part_3_line_9"},
        produces={"output": "ca/rc381_part_3_line_18"},
    ),
    # Line 20 "Actual base contributions on CPP pensionable earnings: amount from line 19 x
    # 83.1933%", line 19 "Total actual base and first additional contributions on CPP
    # pensionable earnings from box 16 of all of your T4 slips" (50340).
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/rc381_cpp_base_share_rate"},
        consumes={"base": "ca/t4_cpp_contributions_box_16"},
        produces={"output": "ca/rc381_part_3_line_20"},
    ),
    # Line 21 "Actual first additional contributions on CPP pensionable earnings: Line 19 minus
    # line 20".
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ca/t4_cpp_contributions_box_16", "less": "ca/rc381_part_3_line_20"},
        produces={"output": "ca/rc381_part_3_line_21"},
    ),
    # Line 22 "Required base contributions on CPP pensionable earnings: amount from line 18 x
    # 4.95% = (maximum $3,356.10)".
    CapabilitySelection(
        name="core/contribution_tier",
        params={"tier": "ca/rc381_required_cpp_base"},
        consumes={"earnings": "ca/rc381_part_3_line_18"},
        produces={"output": "ca/rc381_part_3_line_22"},
    ),
    # Line 23 "Required first additional contributions on CPP pensionable earnings: amount from
    # line 18 x 1% = (maximum $678.00)".
    CapabilitySelection(
        name="core/contribution_tier",
        params={"tier": "ca/rc381_required_first_additional"},
        consumes={"earnings": "ca/rc381_part_3_line_18"},
        produces={"output": "ca/rc381_part_3_line_23"},
    ),
    # Line 24 "Required base and first additional contributions on CPP pensionable earnings:
    # Line 22 plus line 23".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/rc381_part_3_line_22", "ca/rc381_part_3_line_23")},
        produces={"output": "ca/rc381_part_3_line_24"},
    ),
    # Line 26 "Required second additional contributions on CPP pensionable earnings: amount from
    # line 15 x 4% = (maximum $396.00)".
    CapabilitySelection(
        name="core/contribution_tier",
        params={"tier": "ca/rc381_required_second_additional"},
        consumes={"earnings": "ca/rc381_part_3_line_15"},
        produces={"output": "ca/rc381_part_3_line_26"},
    ),
    # Lines 27 to 30 "Amount from line I of Part 2 minus the amount from line 7", "Amount from
    # line G of Part 2 minus the amount from line 8", "Amount from line J of Part 2 minus the
    # amount from line 9" and "Amount from line H of Part 2 minus the amount from line 10": the
    # QPP maximums less the shares taken by the CPP side.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ca/rc381_part_2_line_i", "less": "ca/rc381_part_3_line_7"},
        produces={"output": "ca/rc381_part_3_line_27"},
    ),
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ca/rc381_part_2_line_g", "less": "ca/rc381_part_3_line_8"},
        produces={"output": "ca/rc381_part_3_line_28"},
    ),
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ca/rc381_part_2_line_j", "less": "ca/rc381_part_3_line_9"},
        produces={"output": "ca/rc381_part_3_line_29"},
    ),
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ca/rc381_part_2_line_h", "less": "ca/rc381_part_3_line_10"},
        produces={"output": "ca/rc381_part_3_line_30"},
    ),
    # Line 31 "Earnings subject to QPP contributions: Enter whichever is less: amount from line
    # 2 or line 27."
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={
            "amounts": ("ca/t4_qpp_pensionable_earnings_in_quebec", "ca/rc381_part_3_line_27")
        },
        produces={"output": "ca/rc381_part_3_line_31"},
    ),
    # Line 34 "Line 32 minus line 33 (if negative, enter "0")", line 32 "Amount from line 31"
    # and line 33 "Amount from line 28".
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={"amount": "ca/rc381_part_3_line_31", "less": "ca/rc381_part_3_line_28"},
        produces={"output": "ca/rc381_part_3_line_34"},
    ),
    # Line 35 "Earnings subject to second additional QPP contributions: Enter whichever is less:
    # amount from line 30 or line 34.", which line 3's instruction "If the amount from line 3 is
    # more than the amount from line G of Part 2, complete lines 32 to 35. If not, enter the
    # amount from line 31 on line 36 and continue at line 37." makes 0 when it does not apply:
    # the lesser of lines 30 and 34 (the printed sub-calculation of line 35) ...
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={"amounts": ("ca/rc381_part_3_line_30", "ca/rc381_part_3_line_34")},
        produces={"output": "ca/rc381_part_3_line_35_lesser"},
    ),
    # ... and line 35 itself, that amount only when line 3 is more than line G.
    CapabilitySelection(
        name="ca/amount_when_more",
        params={},
        consumes={
            "amount": "ca/rc381_part_3_line_35_lesser",
            "more": "ca/rc381_part_3_line_3",
            "than": "ca/rc381_part_2_line_g",
        },
        produces={"output": "ca/rc381_part_3_line_35"},
    ),
    # Line 36 "Line 31 minus line 35".
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ca/rc381_part_3_line_31", "less": "ca/rc381_part_3_line_35"},
        produces={"output": "ca/rc381_part_3_line_36"},
    ),
    # Line 38 "Earnings subject to base and first additional QPP contributions: Line 36 minus
    # line 37 (if negative, enter "0")", line 37 "Amount from line 29".
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={"amount": "ca/rc381_part_3_line_36", "less": "ca/rc381_part_3_line_29"},
        produces={"output": "ca/rc381_part_3_line_38"},
    ),
    # Line 40 "Actual base contributions on QPP pensionable earnings: amount from line 39 x
    # 84.375%", line 39 "Total actual base and first additional contributions on QPP pensionable
    # earnings from box 17 of all of your T4 slips" (50330).
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/rc381_qpp_base_share_rate"},
        consumes={"base": "ca/t4_qpp_contributions_box_17"},
        produces={"output": "ca/rc381_part_3_line_40"},
    ),
    # Line 41 "Actual first additional contributions on QPP pensionable earnings: Line 39 minus
    # line 40".
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ca/t4_qpp_contributions_box_17", "less": "ca/rc381_part_3_line_40"},
        produces={"output": "ca/rc381_part_3_line_41"},
    ),
    # Line 42 "Required base contributions on QPP pensionable earnings: amount from line 38 x
    # 5.4% = (maximum $3,661.20)".
    CapabilitySelection(
        name="core/contribution_tier",
        params={"tier": "ca/rc381_required_qpp_base"},
        consumes={"earnings": "ca/rc381_part_3_line_38"},
        produces={"output": "ca/rc381_part_3_line_42"},
    ),
    # Line 43 "Required first additional contributions on QPP pensionable earnings: amount from
    # line 38 x 1% = (maximum $678.00)", the figures of line 23, so the same dataset.
    CapabilitySelection(
        name="core/contribution_tier",
        params={"tier": "ca/rc381_required_first_additional"},
        consumes={"earnings": "ca/rc381_part_3_line_38"},
        produces={"output": "ca/rc381_part_3_line_43"},
    ),
    # Line 44 "Required base and first additional contributions on QPP pensionable earnings:
    # Line 42 plus line 43".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/rc381_part_3_line_42", "ca/rc381_part_3_line_43")},
        produces={"output": "ca/rc381_part_3_line_44"},
    ),
    # Line 46 "Required second additional contributions on QPP pensionable earnings: amount from
    # line 35 x 4% = (maximum $396.00)", the figures of line 26, so the same dataset.
    CapabilitySelection(
        name="core/contribution_tier",
        params={"tier": "ca/rc381_required_second_additional"},
        consumes={"earnings": "ca/rc381_part_3_line_35"},
        produces={"output": "ca/rc381_part_3_line_46"},
    ),
    # Line 49 "Total actual base contributions: line 47 plus line 48", line 47 "Amount from line
    # 20" and line 48 "Amount from line 40".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/rc381_part_3_line_20", "ca/rc381_part_3_line_40")},
        produces={"output": "ca/rc381_part_3_line_49"},
    ),
    # Line 52 "Total required base contributions: line 50 plus line 51", line 50 "Amount from
    # line 22" and line 51 "Amount from line 42".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/rc381_part_3_line_22", "ca/rc381_part_3_line_42")},
        produces={"output": "ca/rc381_part_3_line_52"},
    ),
    # Line 53 "Line 49 minus line 52 (if negative, show in brackets)".
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ca/rc381_part_3_line_49", "less": "ca/rc381_part_3_line_52"},
        produces={"output": "ca/rc381_part_3_line_53"},
    ),
    # Line 56 "Total actual first additional contributions: Line 54 plus line 55", line 54
    # "Amount from line 21" and line 55 "Amount from line 41".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/rc381_part_3_line_21", "ca/rc381_part_3_line_41")},
        produces={"output": "ca/rc381_part_3_line_56"},
    ),
    # Line 59 "Total required first additional contributions: Line 57 plus line 58", line 57
    # "Amount from line 23" and line 58 "Amount from line 43".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/rc381_part_3_line_23", "ca/rc381_part_3_line_43")},
        produces={"output": "ca/rc381_part_3_line_59"},
    ),
    # Line 60 "Line 56 minus line 59 (if negative, show in brackets)".
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ca/rc381_part_3_line_56", "less": "ca/rc381_part_3_line_59"},
        produces={"output": "ca/rc381_part_3_line_60"},
    ),
    # Line 61 "Line 53 plus line 60 (if negative, show in brackets)".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/rc381_part_3_line_53", "ca/rc381_part_3_line_60")},
        produces={"output": "ca/rc381_part_3_line_61"},
    ),
    # Line 64 "Total actual second additional contributions: Line 62 plus line 63", line 62
    # "Amount from line 25" (box 16A, 50341) and line 63 "Amount from line 45" (box 17A, 50331).
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": ("ca/t4_cpp_second_additional_box_16a", "ca/t4_qpp_second_additional_box_17a")
        },
        produces={"output": "ca/rc381_part_3_line_64"},
    ),
    # Line 67 "Total required second additional contributions: Line 65 plus line 66", line 65
    # "Amount from line 26" and line 66 "Amount from line 46".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/rc381_part_3_line_26", "ca/rc381_part_3_line_46")},
        produces={"output": "ca/rc381_part_3_line_67"},
    ),
    # Line 68 "Line 64 minus line 67 (if negative, show in brackets)".
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ca/rc381_part_3_line_64", "less": "ca/rc381_part_3_line_67"},
        produces={"output": "ca/rc381_part_3_line_68"},
    ),
    # Line 69 "Line 61 plus line 68 (if negative, show in brackets)".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/rc381_part_3_line_61", "ca/rc381_part_3_line_68")},
        produces={"output": "ca/rc381_part_3_line_69"},
    ),
    # Part 3a, line 73 "Deduction for enhanced contributions on employment income: Line 71 plus
    # line 72", line 71 "Enter the amount from line 59." and line 72 "Enter the amount from line 67
    # (if any).": copies of lines 59 and 67, so no step of their own.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/rc381_part_3_line_59", "ca/rc381_part_3_line_67")},
        produces={"output": "ca/rc381_part_3_line_73"},
    ),
    # Part 3b, line 75 "If line 53 is positive or "0", enter the amount from line 52 at line 75 and
    # line 81, and continue at line 82. If not, enter the amount from line 49 and continue at
    # line 76." (The lines it skips come out the same by their own rules: line 76 is "0", so lines
    # 77, 78 and 80 are "0" and line 81 is line 79, line 52.)
    CapabilitySelection(
        name="ca/choose_by_sign",
        params={},
        consumes={
            "sign": "ca/rc381_part_3_line_53",
            "when_positive": (),
            "when_zero": (),
            "when_negative": ("ca/rc381_part_3_line_49",),
            "when_non_positive": (),
            "when_non_negative": ("ca/rc381_part_3_line_52",),
        },
        produces={"output": "ca/rc381_part_3_line_75"},
    ),
    # Line 76 "If line 53 is negative: Enter the amount from line 53 as a positive amount."
    CapabilitySelection(
        name="ca/positive_part_of_negation",
        params={},
        consumes={"amount": "ca/rc381_part_3_line_53"},
        produces={"output": "ca/rc381_part_3_line_76"},
    ),
    # Line 77 "If line 53 is negative and line 60 is positive, enter whichever is less: amount from
    # line 60 or line 76. If not, enter "0"." Line 76 is above zero only when line 53 is negative,
    # so the least of lines 60 and 76 when both are above zero is the form's rule.
    CapabilitySelection(
        name="ca/lesser_of_when_positive",
        params={},
        consumes={"amounts": ("ca/rc381_part_3_line_60", "ca/rc381_part_3_line_76")},
        produces={"output": "ca/rc381_part_3_line_77"},
    ),
    # Line 78 "Line 76 minus line 77".
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ca/rc381_part_3_line_76", "less": "ca/rc381_part_3_line_77"},
        produces={"output": "ca/rc381_part_3_line_78"},
    ),
    # Line 79 "Line 75 plus line 77".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/rc381_part_3_line_75", "ca/rc381_part_3_line_77")},
        produces={"output": "ca/rc381_part_3_line_79"},
    ),
    # Line 80 "If line 68 and line 78 are both positive, enter whichever is less. If not, enter
    # "0"" (the lesser of lines 68 and 78).
    CapabilitySelection(
        name="ca/lesser_of_when_positive",
        params={},
        consumes={"amounts": ("ca/rc381_part_3_line_68", "ca/rc381_part_3_line_78")},
        produces={"output": "ca/rc381_part_3_line_80"},
    ),
    # Line 81 "Base contributions through employment income: Line 79 plus line 80".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/rc381_part_3_line_79", "ca/rc381_part_3_line_80")},
        produces={"output": "ca/rc381_part_3_line_81"},
    ),
    # Line 82 "If line 60 is positive or "0", enter the amount from line 59 at line 82 and line 88,
    # and continue at line 89. If not, enter the amount from line 56 and continue at line 83."
    # (The lines it skips come out the same by their own rules: line 83 is "0", so lines 84, 85 and
    # 87 are "0" and line 88 is line 86, line 59.)
    CapabilitySelection(
        name="ca/choose_by_sign",
        params={},
        consumes={
            "sign": "ca/rc381_part_3_line_60",
            "when_positive": (),
            "when_zero": (),
            "when_negative": ("ca/rc381_part_3_line_56",),
            "when_non_positive": (),
            "when_non_negative": ("ca/rc381_part_3_line_59",),
        },
        produces={"output": "ca/rc381_part_3_line_82"},
    ),
    # Line 83 "If line 60 is negative: Enter the amount from line 60 as a positive amount."
    CapabilitySelection(
        name="ca/positive_part_of_negation",
        params={},
        consumes={"amount": "ca/rc381_part_3_line_60"},
        produces={"output": "ca/rc381_part_3_line_83"},
    ),
    # Line 84 "If line 53 is positive, enter whichever is less: amount from line 53 or line 83. If
    # not, enter "0"." Line 83 is above zero only when line 60 is negative.
    CapabilitySelection(
        name="ca/lesser_of_when_positive",
        params={},
        consumes={"amounts": ("ca/rc381_part_3_line_53", "ca/rc381_part_3_line_83")},
        produces={"output": "ca/rc381_part_3_line_84"},
    ),
    # Line 85 "Line 83 minus line 84".
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ca/rc381_part_3_line_83", "less": "ca/rc381_part_3_line_84"},
        produces={"output": "ca/rc381_part_3_line_85"},
    ),
    # Line 86 "Line 82 plus line 84".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/rc381_part_3_line_82", "ca/rc381_part_3_line_84")},
        produces={"output": "ca/rc381_part_3_line_86"},
    ),
    # The result printed inside line 87, "the result of line 68 minus line 80", which is above zero
    # only when line 68 is.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ca/rc381_part_3_line_68", "less": "ca/rc381_part_3_line_80"},
        produces={"output": "ca/rc381_part_3_line_87_difference"},
    ),
    # Line 87 "If line 68 and line 85 are both positive, enter whichever is less: amount from line
    # 85 or the result of line 68 minus line 80. If not, enter "0"." Line 80 is never more than a
    # positive line 68, so the difference is above zero exactly when line 68 is more than line 80;
    # when it is "0" or line 68 is not positive the lesser is not above zero and the line is "0"
    # either way.
    CapabilitySelection(
        name="ca/lesser_of_when_positive",
        params={},
        consumes={"amounts": ("ca/rc381_part_3_line_85", "ca/rc381_part_3_line_87_difference")},
        produces={"output": "ca/rc381_part_3_line_87"},
    ),
    # Line 88 "Line 86 plus line 87".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/rc381_part_3_line_86", "ca/rc381_part_3_line_87")},
        produces={"output": "ca/rc381_part_3_line_88"},
    ),
    # Line 89 "If line 68 is positive or "0", enter the amount from line 67 at line 89 and line 92,
    # and continue at line 93. If not, enter the amount from line 64 and continue at line 90."
    CapabilitySelection(
        name="ca/choose_by_sign",
        params={},
        consumes={
            "sign": "ca/rc381_part_3_line_68",
            "when_positive": (),
            "when_zero": (),
            "when_negative": ("ca/rc381_part_3_line_64",),
            "when_non_positive": (),
            "when_non_negative": ("ca/rc381_part_3_line_67",),
        },
        produces={"output": "ca/rc381_part_3_line_89"},
    ),
    # Line 90 "If line 68 is negative: Enter the amount from line 68 as a positive amount."
    CapabilitySelection(
        name="ca/positive_part_of_negation",
        params={},
        consumes={"amount": "ca/rc381_part_3_line_68"},
        produces={"output": "ca/rc381_part_3_line_90"},
    ),
    # Line 91 "If line 61 is positive, enter whichever is less: amount from line 61 or line 90. If
    # not, enter "0"." Line 90 is above zero only when line 68 is negative.
    CapabilitySelection(
        name="ca/lesser_of_when_positive",
        params={},
        consumes={"amounts": ("ca/rc381_part_3_line_61", "ca/rc381_part_3_line_90")},
        produces={"output": "ca/rc381_part_3_line_91"},
    ),
    # Line 92 "Line 89 plus line 91".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/rc381_part_3_line_89", "ca/rc381_part_3_line_91")},
        produces={"output": "ca/rc381_part_3_line_92"},
    ),
    # Line 93 "Deduction for enhanced contributions on employment income: Line 88 plus line 92".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/rc381_part_3_line_88", "ca/rc381_part_3_line_92")},
        produces={"output": "ca/rc381_part_3_line_93"},
    ),
    # The result for line 30800 of the return, "If your earnings subject to contributions are from
    # employment income only and line 69 is: positive, complete Part 3a ... "0", complete Part 3b
    # ... negative ... If not, complete Part 3b": Part 3a line 70 "Base contributions through
    # employment income: Enter the amount from line 52." when line 69 is positive, else Part 3b
    # line 81 "Base contributions through employment income".
    CapabilitySelection(
        name="ca/choose_by_sign",
        params={},
        consumes={
            "sign": "ca/rc381_part_3_line_69",
            "when_positive": ("ca/rc381_part_3_line_52",),
            "when_zero": (),
            "when_negative": (),
            "when_non_positive": ("ca/rc381_part_3_line_81",),
            "when_non_negative": (),
        },
        produces={"output": "ca/rc381_employment_cpp_base_contributions"},
    ),
    # The result for line 22215 of the return: Part 3a line 73 "Deduction for enhanced
    # contributions on employment income: Line 71 plus line 72" when line 69 is positive, else Part
    # 3b line 93 "Deduction for enhanced contributions on employment income".
    CapabilitySelection(
        name="ca/choose_by_sign",
        params={},
        consumes={
            "sign": "ca/rc381_part_3_line_69",
            "when_positive": ("ca/rc381_part_3_line_73",),
            "when_zero": (),
            "when_negative": (),
            "when_non_positive": ("ca/rc381_part_3_line_93",),
            "when_non_negative": (),
        },
        produces={"output": "ca/rc381_employment_cpp_enhanced_contributions"},
    ),
    # The result for line 44800 of the return: Part 3a line 74 "Overpayment: Enter the amount from
    # line 69." when line 69 is positive; Part 3b has no overpayment, so "0" otherwise. Line 69 is
    # its own sign, so the amount is line 69 not below zero.
    CapabilitySelection(
        name="core/sum_not_below_zero",
        params={},
        consumes={"parts": ("ca/rc381_part_3_line_69",)},
        produces={"output": "ca/rc381_cpp_overpayment"},
    ),
    # Part 4 (for residents of a province or territory other than Quebec), lines 1 to 27. Line 1
    # "Pensionable net self-employment earnings: amount from line 12200 of your return plus line
    # 27 of your return", line 2 "Employment earnings not shown on a T4 slip that you elect to
    # pay additional CPP contributions on (complete Form CPT20)" (50373) and line 5 "Total actual
    # base and first additional CPP contributions from line 19 of Part 3" are the existing
    # artifacts of Schedule 8 Part 4 and of Part 3, so they have no step of their own.
    # Line 4 "Add lines 1 to 3.", line 3 "Employment earnings shown on a T4 slip that you elect to
    # pay additional CPP contributions on (complete Form CPT20)" (50399): no floor is printed, so
    # a loss on line 1 stays in line 4.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/pensionable_net_self_employment_earnings",
                "ca/cpt20_earnings",
                "ca/cpt20_t4_earnings",
            )
        },
        produces={"output": "ca/rc381_part_4_line_4"},
    ),
    # Line 8 "Line 6 minus line 7 (if negative, show in brackets)", line 6 "Amount from line 47 of
    # Part 3" (the amount from line 20) and line 7 "Amount from line 50 of Part 3" (the amount
    # from line 22).
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ca/rc381_part_3_line_20", "less": "ca/rc381_part_3_line_22"},
        produces={"output": "ca/rc381_part_4_line_8"},
    ),
    # Line 11 "Line 9 minus line 10 (if negative, show in brackets)", line 9 "Amount from line 54
    # of Part 3" (the amount from line 21) and line 10 "Amount from line 57 of Part 3" (the amount
    # from line 23).
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ca/rc381_part_3_line_21", "less": "ca/rc381_part_3_line_23"},
        produces={"output": "ca/rc381_part_4_line_11"},
    ),
    # Line 12 "Line 8 plus line 11 (if negative, show in brackets)".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/rc381_part_4_line_8", "ca/rc381_part_4_line_11")},
        produces={"output": "ca/rc381_part_4_line_12"},
    ),
    # The result printed inside line 13, "Line 5 minus line 12", entered when line 61 of Part 3 is
    # positive.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ca/t4_cpp_contributions_box_16", "less": "ca/rc381_part_4_line_12"},
        produces={"output": "ca/rc381_part_4_line_13_difference"},
    ),
    # Line 13 "Line 5 minus line 12", with the block "If line 61 of Part 3 is: "0", do not complete
    # lines 6 to 24. Enter the amount from line 5 on line 26 ... positive, complete lines 6 to 13
    # only, and continue at line 25. negative, enter the amount from line 5 on line 13 and continue
    # at line 14.": line 5 when line 61 is "0" (line 25 is line 13, so line 26 is line 5, as the
    # block says) or negative, else line 5 minus line 12.
    CapabilitySelection(
        name="ca/choose_by_sign",
        params={},
        consumes={
            "sign": "ca/rc381_part_3_line_61",
            "when_positive": ("ca/rc381_part_4_line_13_difference",),
            "when_zero": (),
            "when_negative": (),
            "when_non_positive": ("ca/t4_cpp_contributions_box_16",),
            "when_non_negative": (),
        },
        produces={"output": "ca/rc381_part_4_line_13"},
    ),
    # Line 14 "Enter the amount from line 61 of Part 3 as a positive amount." (above zero only when
    # line 61 is negative).
    CapabilitySelection(
        name="ca/positive_part_of_negation",
        params={},
        consumes={"amount": "ca/rc381_part_3_line_61"},
        produces={"output": "ca/rc381_part_4_line_14"},
    ),
    # Line 17 "Line 15 minus line 16 (if negative, show in brackets)", line 15 "Amount from line
    # 19 of Part 3" and line 16 "Amount from line 24 of Part 3".
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/t4_cpp_contributions_box_16",
            "less": "ca/rc381_part_3_line_24",
        },
        produces={"output": "ca/rc381_part_4_line_17"},
    ),
    # Line 17A "If line 17 is negative, enter it as a positive amount. If not, enter "0"."
    CapabilitySelection(
        name="ca/positive_part_of_negation",
        params={},
        consumes={"amount": "ca/rc381_part_4_line_17"},
        produces={"output": "ca/rc381_part_4_line_17a"},
    ),
    # Line 20 "Line 18 minus line 19 (if negative, show in brackets)", line 18 "Amount from line
    # 39 of Part 3" and line 19 "Amount from line 44 of Part 3".
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/t4_qpp_contributions_box_17",
            "less": "ca/rc381_part_3_line_44",
        },
        produces={"output": "ca/rc381_part_4_line_20"},
    ),
    # The result printed inside line 21, "If line 17 is positive, enter the amount from line 17
    # (show in brackets)": the negative of line 17 when it is above zero, else "0".
    CapabilitySelection(
        name="ca/lesser_of_when_positive_in_brackets",
        params={},
        consumes={"amounts": ("ca/rc381_part_4_line_17",)},
        produces={"output": "ca/rc381_part_4_line_21_from_line_17"},
    ),
    # The result printed inside line 21, "If line 20 is positive, enter whichever is less: amount
    # from line 20 or line 17A.": the lesser of lines 20 and 17A when both are above zero (line
    # 17A is above zero only when line 17 is negative), else "0".
    CapabilitySelection(
        name="ca/lesser_of_when_positive",
        params={},
        consumes={"amounts": ("ca/rc381_part_4_line_20", "ca/rc381_part_4_line_17a")},
        produces={"output": "ca/rc381_part_4_line_21_lesser"},
    ),
    # Line 21 "If line 17 and line 20 are both negative or either amount is "0", enter "0". If line
    # 17 is positive, enter the amount from line 17 (show in brackets). If line 20 is positive,
    # enter whichever is less: amount from line 20 or line 17A.", read by the sign of line 20:
    # positive, the lesser of lines 20 and 17A ("0" when line 17 is not negative, which is also
    # the reading when lines 17 and 20 are both positive, a case the form does not settle);
    # negative, line 17 in brackets ("0" when line 17 is not positive); "0", "0".
    CapabilitySelection(
        name="ca/choose_by_sign",
        params={},
        consumes={
            "sign": "ca/rc381_part_4_line_20",
            "when_positive": ("ca/rc381_part_4_line_21_lesser",),
            "when_zero": (),
            "when_negative": ("ca/rc381_part_4_line_21_from_line_17",),
            "when_non_positive": (),
            "when_non_negative": (),
        },
        produces={"output": "ca/rc381_part_4_line_21"},
    ),
    # Line 22 "If line 17A is more than line 14, enter "1". If not, enter the result of line 17A
    # divided by line 14 (calculated to the fifth decimal place without rounding).": truncated,
    # not rounded, to 0.00001; 1 when line 17A is more than line 14 (even when line 14 is 0); 0
    # when line 14 is 0 and line 17A is not more.
    CapabilitySelection(
        name="ca/ratio_truncated_at_most_one",
        params={"rounding": "ca/rc381_ratio_truncation"},
        consumes={
            "dividend": "ca/rc381_part_4_line_17a",
            "divisor": "ca/rc381_part_4_line_14",
        },
        produces={"output": "ca/rc381_part_4_line_22"},
    ),
    # The first result printed inside line 23, "If line 69 of Part 3 is positive or "0", enter
    # whichever is less: amount from line 68 of Part 3 or line 17A."
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={"amounts": ("ca/rc381_part_3_line_68", "ca/rc381_part_4_line_17a")},
        produces={"output": "ca/rc381_part_4_line_23_lesser"},
    ),
    # The second result printed inside line 23, "If not, enter the result of line 68 of Part 3
    # multiplied by the rate at line 22.": a dollars-and-cents box, so it rounds half up to the
    # cent, and it is negative when line 68 is.
    CapabilitySelection(
        name="ca/apply_chosen_rate",
        params={"rounding": "ca/rc381_cents_rounding"},
        consumes={"base": "ca/rc381_part_3_line_68", "rate": "ca/rc381_part_4_line_22"},
        produces={"output": "ca/rc381_part_4_line_23_multiplied"},
    ),
    # Line 23, by the sign of line 69 of Part 3: "0" or positive, the lesser; negative, the
    # product.
    CapabilitySelection(
        name="ca/choose_by_sign",
        params={},
        consumes={
            "sign": "ca/rc381_part_3_line_69",
            "when_positive": (),
            "when_zero": (),
            "when_negative": ("ca/rc381_part_4_line_23_multiplied",),
            "when_non_positive": (),
            "when_non_negative": ("ca/rc381_part_4_line_23_lesser",),
        },
        produces={"output": "ca/rc381_part_4_line_23"},
    ),
    # Line 24 "Enter whichever is less: amount from line 17A or line 23.", before the block's "If
    # line 61 of Part 3 is ... negative" decides whether line 24 takes it: the lesser of lines
    # 17A and 23.
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={"amounts": ("ca/rc381_part_4_line_17a", "ca/rc381_part_4_line_23")},
        produces={"output": "ca/rc381_part_4_line_24_lesser"},
    ),
    # ... and line 24 itself, that amount only when line 61 of Part 3 is negative (lines 14 to 24
    # are completed then, and not when line 61 is "0" or positive).
    CapabilitySelection(
        name="ca/choose_by_sign",
        params={},
        consumes={
            "sign": "ca/rc381_part_3_line_61",
            "when_positive": (),
            "when_zero": (),
            "when_negative": ("ca/rc381_part_4_line_24_lesser",),
            "when_non_positive": (),
            "when_non_negative": (),
        },
        produces={"output": "ca/rc381_part_4_line_24"},
    ),
    # Line 25 "Amount from line 13" is a copy of line 13, so no step of its own. Line 25A "Amount
    # from line 21": that amount only when line 61 of Part 3 is negative (the block completes
    # lines 14 to 24 then), else "0".
    CapabilitySelection(
        name="ca/choose_by_sign",
        params={},
        consumes={
            "sign": "ca/rc381_part_3_line_61",
            "when_positive": (),
            "when_zero": (),
            "when_negative": ("ca/rc381_part_4_line_21",),
            "when_non_positive": (),
            "when_non_negative": (),
        },
        produces={"output": "ca/rc381_part_4_line_25a"},
    ),
    # Line 26 "Add lines 24 to 25A.", line 25 being the amount from line 13: with line 61 of Part
    # 3 at "0" lines 24 and 25A are "0" and line 13 is line 5, "Enter the amount from line 5 on line
    # 26".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/rc381_part_4_line_24",
                "ca/rc381_part_4_line_13",
                "ca/rc381_part_4_line_25a",
            )
        },
        produces={"output": "ca/rc381_part_4_line_26"},
    ),
    # Line 27 "Amount from line 26 × 16.80672 =": the product rounds half up to the cent, the
    # owner's decision, as the form states no rounding rule.
    CapabilitySelection(
        name="core/apply_fraction",
        params={"fraction": "ca/rc381_cpp_gross_up_fraction"},
        consumes={"base": "ca/rc381_part_4_line_26"},
        produces={"output": "ca/rc381_part_4_line_27"},
    ),
    # Part 4 line 31's printed difference, "Line 29 minus line 30" (the amount from line 61
    # of Part 3 less the amount from line 12), entered when line 61 is positive.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/rc381_part_3_line_61",
            "less": "ca/rc381_part_4_line_12",
        },
        produces={"output": "ca/rc381_part_4_line_31_difference"},
    ),
    # Line 31, by the block "If line 61 of Part 3 is: ... positive, complete lines 28 to 32 only
    # ... negative, complete line 28 and enter "0" at line 31": the difference when line 61 is
    # positive, else "0".
    CapabilitySelection(
        name="ca/choose_by_sign",
        params={},
        consumes={
            "sign": "ca/rc381_part_3_line_61",
            "when_positive": ("ca/rc381_part_4_line_31_difference",),
            "when_zero": (),
            "when_negative": (),
            "when_non_positive": (),
            "when_non_negative": (),
        },
        produces={"output": "ca/rc381_part_4_line_31"},
    ),
    # Line 32 "Line 28 minus line 31", line 28 being the amount from line 39 of Part 3 (box 17).
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/t4_qpp_contributions_box_17",
            "less": "ca/rc381_part_4_line_31",
        },
        produces={"output": "ca/rc381_part_4_line_32"},
    ),
    # Line 33 "Enter the amount from line 61 of Part 3 as a positive amount."
    CapabilitySelection(
        name="ca/positive_part_of_negation",
        params={},
        consumes={
            "amount": "ca/rc381_part_3_line_61",
        },
        produces={"output": "ca/rc381_part_4_line_33"},
    ),
    # Line 34 "If line 17A is positive, enter whichever is less: amount from line 17A or line
    # 33. If not, enter "0"."
    CapabilitySelection(
        name="ca/lesser_of_when_positive",
        params={},
        consumes={
            "amounts": ("ca/rc381_part_4_line_17a", "ca/rc381_part_4_line_33"),
        },
        produces={"output": "ca/rc381_part_4_line_34"},
    ),
    # Line 35 "Line 33 minus line 34".
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/rc381_part_4_line_33",
            "less": "ca/rc381_part_4_line_34",
        },
        produces={"output": "ca/rc381_part_4_line_35"},
    ),
    # Line 35A's first sentence, "If line 35 and line 17 are both positive, enter the amount
    # from line 17.": the amount from line 17 when it is positive ...
    CapabilitySelection(
        name="ca/lesser_of_when_positive",
        params={},
        consumes={
            "amounts": ("ca/rc381_part_4_line_17",),
        },
        produces={"output": "ca/rc381_part_4_line_35aa_from_line_17"},
    ),
    # ... taken when line 35 is positive too.
    CapabilitySelection(
        name="ca/choose_by_sign",
        params={},
        consumes={
            "sign": "ca/rc381_part_4_line_35",
            "when_positive": ("ca/rc381_part_4_line_35aa_from_line_17",),
            "when_zero": (),
            "when_negative": (),
            "when_non_positive": (),
            "when_non_negative": (),
        },
        produces={"output": "ca/rc381_part_4_line_35aa"},
    ),
    # Line 35A's second sentence, "If line 35 is \"0\" and line 20 is positive, enter the amount
    # from line 20 (show in brackets).": line 20 in brackets when it is positive ...
    CapabilitySelection(
        name="ca/lesser_of_when_positive_in_brackets",
        params={},
        consumes={
            "amounts": ("ca/rc381_part_4_line_20",),
        },
        produces={"output": "ca/rc381_part_4_line_35ab_from_line_20"},
    ),
    # ... taken when line 35 is "0" ...
    CapabilitySelection(
        name="ca/choose_by_sign",
        params={},
        consumes={
            "sign": "ca/rc381_part_4_line_35",
            "when_positive": (),
            "when_zero": ("ca/rc381_part_4_line_35ab_from_line_20",),
            "when_negative": (),
            "when_non_positive": (),
            "when_non_negative": (),
        },
        produces={"output": "ca/rc381_part_4_line_35ab_when_line_35_zero"},
    ),
    # ... and only when line 61 of Part 3 is negative (lines 33 to 39 are completed then).
    CapabilitySelection(
        name="ca/choose_by_sign",
        params={},
        consumes={
            "sign": "ca/rc381_part_3_line_61",
            "when_positive": (),
            "when_zero": (),
            "when_negative": ("ca/rc381_part_4_line_35ab_when_line_35_zero",),
            "when_non_positive": (),
            "when_non_negative": (),
        },
        produces={"output": "ca/rc381_part_4_line_35ab"},
    ),
    # Line 35A, the two sentences added (at most one is not "0").
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": ("ca/rc381_part_4_line_35aa", "ca/rc381_part_4_line_35ab"),
        },
        produces={"output": "ca/rc381_part_4_line_35a"},
    ),
    # Line 36 "Enter the amount from line 68 of Part 3 if positive. If not, enter \"0\"."
    CapabilitySelection(
        name="core/sum_not_below_zero",
        params={},
        consumes={
            "parts": ("ca/rc381_part_3_line_68",),
        },
        produces={"output": "ca/rc381_part_4_line_36"},
    ),
    # Line 38 "Line 36 minus line 37", line 37 being the amount from line 24.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/rc381_part_4_line_36",
            "less": "ca/rc381_part_4_line_24",
        },
        produces={"output": "ca/rc381_part_4_line_38"},
    ),
    # Line 39 "Enter whichever is less: amount from line 35 or line 38."
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={
            "amounts": ("ca/rc381_part_4_line_35", "ca/rc381_part_4_line_38"),
        },
        produces={"output": "ca/rc381_part_4_line_39"},
    ),
    # Line 40 "Add lines 32, 35A, and 39."
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/rc381_part_4_line_32",
                "ca/rc381_part_4_line_35a",
                "ca/rc381_part_4_line_39",
            ),
        },
        produces={"output": "ca/rc381_part_4_line_40"},
    ),
    # Line 41 "Amount from line 40 × 15.625 =": rounds half up to the cent, the owner's
    # decision, as the form states no rounding rule.
    CapabilitySelection(
        name="core/apply_fraction",
        params={"fraction": "ca/rc381_qpp_gross_up_fraction"},
        consumes={
            "base": "ca/rc381_part_4_line_40",
        },
        produces={"output": "ca/rc381_part_4_line_41"},
    ),
    # Line 42 "Line 27 plus line 41".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": ("ca/rc381_part_4_line_27", "ca/rc381_part_4_line_41"),
        },
        produces={"output": "ca/rc381_part_4_line_42"},
    ),
    # Line 46's printed difference, "Line 44 minus line 45" (the amount from line 62 of Part 3,
    # which is line 25, less the amount from line 65 of Part 3, which is line 26).
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/t4_cpp_second_additional_box_16a",
            "less": "ca/rc381_part_3_line_26",
        },
        produces={"output": "ca/rc381_part_4_line_46_difference"},
    ),
    # Line 46, by "If line 68 of Part 3 is positive, complete lines 44 to 46. If not, enter \"0\"
    # on line 46".
    CapabilitySelection(
        name="ca/choose_by_sign",
        params={},
        consumes={
            "sign": "ca/rc381_part_3_line_68",
            "when_positive": ("ca/rc381_part_4_line_46_difference",),
            "when_zero": (),
            "when_negative": (),
            "when_non_positive": (),
            "when_non_negative": (),
        },
        produces={"output": "ca/rc381_part_4_line_46"},
    ),
    # Line 47 "Line 43 minus line 46".
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/t4_cpp_second_additional_box_16a",
            "less": "ca/rc381_part_4_line_46",
        },
        produces={"output": "ca/rc381_part_4_line_47"},
    ),
    # Line 51's printed difference, "Line 49 minus line 50" (the amount from line 68 of Part 3
    # less the amount from line 46).
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/rc381_part_3_line_68",
            "less": "ca/rc381_part_4_line_46",
        },
        produces={"output": "ca/rc381_part_4_line_51_difference"},
    ),
    # Line 51, by "If line 68 of Part 3 is positive, complete lines 49 to 51. If not, enter \"0\"
    # on line 51".
    CapabilitySelection(
        name="ca/choose_by_sign",
        params={},
        consumes={
            "sign": "ca/rc381_part_3_line_68",
            "when_positive": ("ca/rc381_part_4_line_51_difference",),
            "when_zero": (),
            "when_negative": (),
            "when_non_positive": (),
            "when_non_negative": (),
        },
        produces={"output": "ca/rc381_part_4_line_51"},
    ),
    # Line 52 "Line 48 minus line 51", line 48 being the amount from line 45 of Part 3 (box 17A).
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/t4_qpp_second_additional_box_17a",
            "less": "ca/rc381_part_4_line_51",
        },
        produces={"output": "ca/rc381_part_4_line_52"},
    ),
    # Line 53 "Line 47 plus line 52".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": ("ca/rc381_part_4_line_47", "ca/rc381_part_4_line_52"),
        },
        produces={"output": "ca/rc381_part_4_line_53"},
    ),
    # Line 54 "Enter the amount from line 68 of Part 3 as a positive amount."
    CapabilitySelection(
        name="ca/positive_part_of_negation",
        params={},
        consumes={
            "amount": "ca/rc381_part_3_line_68",
        },
        produces={"output": "ca/rc381_part_4_line_54"},
    ),
    # Line 55 "If line 61 of Part 3 is positive, enter whichever is less: amount from line 61
    # of Part 3 or line 54."
    CapabilitySelection(
        name="ca/lesser_of_when_positive",
        params={},
        consumes={
            "amounts": ("ca/rc381_part_3_line_61", "ca/rc381_part_4_line_54"),
        },
        produces={"output": "ca/rc381_part_4_line_55"},
    ),
    # Line 56 "Line 53 plus line 55".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": ("ca/rc381_part_4_line_53", "ca/rc381_part_4_line_55"),
        },
        produces={"output": "ca/rc381_part_4_line_56"},
    ),
    # Line 59 "Line 57 minus line 58 (if negative, enter "0") (maximum $67,800)", line 57
    # "Amount from line C of Part 2" and line 58 "Amount from line F of Part 2".
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/cpp_maximum_pensionable_earnings",
            "less": "ca/cpp_basic_exemption",
        },
        produces={"output": "ca/rc381_part_4_line_59"},
    ),
    # Line 61 "Line 59 minus line 60 (if negative, enter "0")", line 60 "Amount from line 42".
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/rc381_part_4_line_59",
            "less": "ca/rc381_part_4_line_42",
        },
        produces={"output": "ca/rc381_part_4_line_61"},
    ),
    # Line 62 "Enter whichever is less: amount from line 4 or line 61."
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={
            "amounts": ("ca/rc381_part_4_line_4", "ca/rc381_part_4_line_61"),
        },
        produces={"output": "ca/rc381_part_4_line_62"},
    ),
    # Line 65 "Line 63 minus line 64 (if negative, enter "0" on lines 65 and 69, and continue at
    # line 70)", line 63 "Amount from line 58" and line 64 "Amount from line 3 of Part 3". The
    # block "If line 3 of Part 3 is less than line 58, complete lines 63 to 69. If not, enter "0"
    # on line 69" is met by this floor: line 3 is not less than line 58 exactly when this line
    # is "0" (and then line 69 is "0" too).
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/cpp_basic_exemption",
            "less": "ca/rc381_part_3_line_3",
        },
        produces={"output": "ca/rc381_part_4_line_65"},
    ),
    # Line 68 "Line 66 minus line 67 (if negative, enter "0")", line 66 "Amount from line 4" and
    # line 67 "Amount from line 59".
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/rc381_part_4_line_4",
            "less": "ca/rc381_part_4_line_59",
        },
        produces={"output": "ca/rc381_part_4_line_68"},
    ),
    # Line 69 "Line 65 minus line 68 (if negative, enter "0")".
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/rc381_part_4_line_65",
            "less": "ca/rc381_part_4_line_68",
        },
        produces={"output": "ca/rc381_part_4_line_69"},
    ),
    # Line 70 "Self-employment income and other earnings subject to base and first additional
    # contributions: Line 62 minus line 69". The form prints no floor.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/rc381_part_4_line_62",
            "less": "ca/rc381_part_4_line_69",
        },
        produces={"output": "ca/rc381_part_4_line_70"},
    ),
    # Line 74 "Add lines 71 to 73.", line 71 "Amount from line 4", line 72 "Amount from line 11
    # of Part 3" and line 73 "Amount from line 31 of Part 3".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/rc381_part_4_line_4",
                "ca/rc381_part_3_line_11",
                "ca/rc381_part_3_line_31",
            ),
        },
        produces={"output": "ca/rc381_part_4_line_74"},
    ),
    # Line 76 "Amount from line 56 ÷ 4% =" (line 75, the amount from line D of Part 2, is read
    # by line 77).
    CapabilitySelection(
        name="ca/divided_by_rate",
        params={"rate": "ca/rc381_second_additional_rate"},
        consumes={
            "dividend": "ca/rc381_part_4_line_56",
        },
        produces={"output": "ca/rc381_part_4_line_76"},
    ),
    # Line 77 "Line 75 minus line 76 (if negative, enter "0")", line 75 "Amount from line D of
    # Part 2".
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/cpp_second_additional_earnings_maximum",
            "less": "ca/rc381_part_4_line_76",
        },
        produces={"output": "ca/rc381_part_4_line_77"},
    ),
    # Line 80 "Line 78 minus line 79", line 78 "Amount from line 4" and line 79 "Amount from
    # line 65 (if any)".
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/rc381_part_4_line_4",
            "less": "ca/rc381_part_4_line_65",
        },
        produces={"output": "ca/rc381_part_4_line_80"},
    ),
    # Line 82 "Line 80 minus line 81", line 81 "Amount from line 70".
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/rc381_part_4_line_80",
            "less": "ca/rc381_part_4_line_70",
        },
        produces={"output": "ca/rc381_part_4_line_82"},
    ),
    # Line 83 "Self-employment income and other earnings subject to second additional
    # contributions: Enter whichever is less: amount from line 77 or line 82." ...
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={
            "amounts": ("ca/rc381_part_4_line_77", "ca/rc381_part_4_line_82"),
        },
        produces={"output": "ca/rc381_part_4_line_83_lesser"},
    ),
    # ... which the instruction "If line 74 is more than line 57, complete lines 75 to 83. If
    # not, enter "0" on line 83 and continue at line 84." completes only when line 74 is more
    # than line 57 (the amount from line C of Part 2).
    CapabilitySelection(
        name="ca/amount_when_more",
        params={},
        consumes={
            "amount": "ca/rc381_part_4_line_83_lesser",
            "more": "ca/rc381_part_4_line_74",
            "than": "ca/cpp_maximum_pensionable_earnings",
        },
        produces={"output": "ca/rc381_part_4_line_83"},
    ),
    # Line 84 "Required base contributions on CPP pensionable earnings: amount from line 70 ×
    # 9.9% = (maximum $6,712.20)", line 85 "Required first additional contributions on CPP
    # pensionable earnings: amount from line 70 × 2% = (maximum $1,356.00)" and line 86 "Required
    # second additional contributions on CPP pensionable earnings: amount from line 83 × 8% =
    # (maximum $792.00)": the self-employed person's tiers of Schedule 8 Part 4 (the same
    # figures), on the earnings of lines 70 and 83. A line 70 below zero contributes nothing.
    CapabilitySelection(
        name="core/contribution_tier",
        params={"tier": "ca/cpp_self_employed_base_contribution"},
        consumes={
            "earnings": "ca/rc381_part_4_line_70",
        },
        produces={"output": "ca/rc381_part_4_line_84"},
    ),
    CapabilitySelection(
        name="core/contribution_tier",
        params={"tier": "ca/cpp_self_employed_first_additional_contribution"},
        consumes={
            "earnings": "ca/rc381_part_4_line_70",
        },
        produces={"output": "ca/rc381_part_4_line_85"},
    ),
    CapabilitySelection(
        name="core/contribution_tier",
        params={"tier": "ca/cpp_self_employed_second_additional_contribution"},
        consumes={
            "earnings": "ca/rc381_part_4_line_83",
        },
        produces={"output": "ca/rc381_part_4_line_86"},
    ),
    # Line 87 "Line 85 plus line 86".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": ("ca/rc381_part_4_line_85", "ca/rc381_part_4_line_86"),
        },
        produces={"output": "ca/rc381_part_4_line_87"},
    ),
    # Line 88 "Line 84 plus line 87".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": ("ca/rc381_part_4_line_84", "ca/rc381_part_4_line_87"),
        },
        produces={"output": "ca/rc381_part_4_line_88"},
    ),
    # The amount printed inside line 89, "Amount from line 69 of Part 3 (if positive)": line 69
    # of Part 3 floored at zero ...
    CapabilitySelection(
        name="core/sum_not_below_zero",
        params={},
        consumes={
            "parts": ("ca/rc381_part_3_line_69",),
        },
        produces={"output": "ca/rc381_part_4_line_89_from_line_69"},
    ),
    # ... and line 89 "× 2 =": twice that amount. 2 is above one, which a rate refuses, so it is
    # a fraction, 2/1, kept as printed.
    CapabilitySelection(
        name="core/apply_fraction",
        params={"fraction": "ca/rc381_double_fraction"},
        consumes={
            "base": "ca/rc381_part_4_line_89_from_line_69",
        },
        produces={"output": "ca/rc381_part_4_line_89"},
    ),
    # Line 90 "CPP contributions payable on self-employment income and other earnings: Line 88
    # minus 89." (if negative, show in brackets).
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/rc381_part_4_line_88",
            "less": "ca/rc381_part_4_line_89",
        },
        produces={"output": "ca/rc381_part_4_line_90"},
    ),
    # Line 90 "If positive, enter the amount (in dollars and cents) on line 42100 of your
    # return": line 90 floored at zero.
    CapabilitySelection(
        name="core/sum_not_below_zero",
        params={},
        consumes={
            "parts": ("ca/rc381_part_4_line_90",),
        },
        produces={"output": "ca/rc381_self_employment_cpp_contributions"},
    ),
    # The amount printed inside line 91, "amount from line 90 entered as a positive amount":
    # above zero only when line 90 is negative ("If negative, show in brackets and continue at
    # line 91").
    CapabilitySelection(
        name="ca/positive_part_of_negation",
        params={},
        consumes={
            "amount": "ca/rc381_part_4_line_90",
        },
        produces={"output": "ca/rc381_part_4_line_91_from_line_90"},
    ),
    # Line 91 "CPP overpayment: ... amount from line 90 entered as a positive amount × 50% =",
    # the result for line 44800 of the return; the 50% is the base credit rate of Schedule 8 Part
    # 4 (line 15, "multiplied by 50%").
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/cpp_self_employed_base_credit_rate"},
        consumes={
            "base": "ca/rc381_part_4_line_91_from_line_90",
        },
        produces={"output": "ca/rc381_part_4_line_91"},
    ),
}

WIRING = {
    (CountAtLeast, frozenset({QPP_MONTHS, CPP_MONTHS}), frozenset({RC381_PART_2_LINE_B})),
    (AmountForCount, frozenset({RC381_PART_2_LINE_B}), frozenset({RC381_PART_2_LINE_G})),
    (AmountForCount, frozenset({RC381_PART_2_LINE_B}), frozenset({RC381_PART_2_LINE_H})),
    (AmountForCount, frozenset({RC381_PART_2_LINE_B}), frozenset({RC381_PART_2_LINE_I})),
    (AmountForCount, frozenset({RC381_PART_2_LINE_B}), frozenset({RC381_PART_2_LINE_J})),
    (
        Sum,
        frozenset(
            {T4_CPP_PENSIONABLE_EARNINGS_OUTSIDE_QUEBEC, T4_QPP_PENSIONABLE_EARNINGS_IN_QUEBEC}
        ),
        frozenset({RC381_PART_3_LINE_3}),
    ),
    (
        RatioTruncated,
        frozenset({T4_CPP_PENSIONABLE_EARNINGS_OUTSIDE_QUEBEC, RC381_PART_3_LINE_3}),
        frozenset({RC381_PART_3_LINE_6}),
    ),
    (
        ApplyChosenRate,
        frozenset({CPP_ADDITIONAL_MAXIMUM_PENSIONABLE_EARNINGS, RC381_PART_3_LINE_6}),
        frozenset({RC381_PART_3_LINE_7}),
    ),
    (
        ApplyChosenRate,
        frozenset({CPP_MAXIMUM_PENSIONABLE_EARNINGS, RC381_PART_3_LINE_6}),
        frozenset({RC381_PART_3_LINE_8}),
    ),
    (
        ApplyChosenRate,
        frozenset({CPP_BASIC_EXEMPTION, RC381_PART_3_LINE_6}),
        frozenset({RC381_PART_3_LINE_9}),
    ),
    (
        ApplyChosenRate,
        frozenset({CPP_SECOND_ADDITIONAL_EARNINGS_MAXIMUM, RC381_PART_3_LINE_6}),
        frozenset({RC381_PART_3_LINE_10}),
    ),
    (
        LesserOf,
        frozenset({T4_CPP_PENSIONABLE_EARNINGS_OUTSIDE_QUEBEC, RC381_PART_3_LINE_7}),
        frozenset({RC381_PART_3_LINE_11}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({RC381_PART_3_LINE_11, RC381_PART_3_LINE_8}),
        frozenset({RC381_PART_3_LINE_14}),
    ),
    (
        LesserOf,
        frozenset({RC381_PART_3_LINE_10, RC381_PART_3_LINE_14}),
        frozenset({RC381_PART_3_LINE_15_LESSER}),
    ),
    (
        AmountWhenMore,
        frozenset(
            {RC381_PART_3_LINE_15_LESSER, RC381_PART_3_LINE_3, CPP_MAXIMUM_PENSIONABLE_EARNINGS}
        ),
        frozenset({RC381_PART_3_LINE_15}),
    ),
    (
        Subtract,
        frozenset({RC381_PART_3_LINE_11, RC381_PART_3_LINE_15}),
        frozenset({RC381_PART_3_LINE_16}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({RC381_PART_3_LINE_16, RC381_PART_3_LINE_9}),
        frozenset({RC381_PART_3_LINE_18}),
    ),
    (ApplyRate, frozenset({T4_CPP_CONTRIBUTIONS_BOX_16}), frozenset({RC381_PART_3_LINE_20})),
    (
        Subtract,
        frozenset({T4_CPP_CONTRIBUTIONS_BOX_16, RC381_PART_3_LINE_20}),
        frozenset({RC381_PART_3_LINE_21}),
    ),
    (TieredContribution, frozenset({RC381_PART_3_LINE_18}), frozenset({RC381_PART_3_LINE_22})),
    (TieredContribution, frozenset({RC381_PART_3_LINE_18}), frozenset({RC381_PART_3_LINE_23})),
    (
        Sum,
        frozenset({RC381_PART_3_LINE_22, RC381_PART_3_LINE_23}),
        frozenset({RC381_PART_3_LINE_24}),
    ),
    (TieredContribution, frozenset({RC381_PART_3_LINE_15}), frozenset({RC381_PART_3_LINE_26})),
    (
        Subtract,
        frozenset({RC381_PART_2_LINE_I, RC381_PART_3_LINE_7}),
        frozenset({RC381_PART_3_LINE_27}),
    ),
    (
        Subtract,
        frozenset({RC381_PART_2_LINE_G, RC381_PART_3_LINE_8}),
        frozenset({RC381_PART_3_LINE_28}),
    ),
    (
        Subtract,
        frozenset({RC381_PART_2_LINE_J, RC381_PART_3_LINE_9}),
        frozenset({RC381_PART_3_LINE_29}),
    ),
    (
        Subtract,
        frozenset({RC381_PART_2_LINE_H, RC381_PART_3_LINE_10}),
        frozenset({RC381_PART_3_LINE_30}),
    ),
    (
        LesserOf,
        frozenset({T4_QPP_PENSIONABLE_EARNINGS_IN_QUEBEC, RC381_PART_3_LINE_27}),
        frozenset({RC381_PART_3_LINE_31}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({RC381_PART_3_LINE_31, RC381_PART_3_LINE_28}),
        frozenset({RC381_PART_3_LINE_34}),
    ),
    (
        LesserOf,
        frozenset({RC381_PART_3_LINE_30, RC381_PART_3_LINE_34}),
        frozenset({RC381_PART_3_LINE_35_LESSER}),
    ),
    (
        AmountWhenMore,
        frozenset({RC381_PART_3_LINE_35_LESSER, RC381_PART_3_LINE_3, RC381_PART_2_LINE_G}),
        frozenset({RC381_PART_3_LINE_35}),
    ),
    (
        Subtract,
        frozenset({RC381_PART_3_LINE_31, RC381_PART_3_LINE_35}),
        frozenset({RC381_PART_3_LINE_36}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({RC381_PART_3_LINE_36, RC381_PART_3_LINE_29}),
        frozenset({RC381_PART_3_LINE_38}),
    ),
    (ApplyRate, frozenset({T4_QPP_CONTRIBUTIONS_BOX_17}), frozenset({RC381_PART_3_LINE_40})),
    (
        Subtract,
        frozenset({T4_QPP_CONTRIBUTIONS_BOX_17, RC381_PART_3_LINE_40}),
        frozenset({RC381_PART_3_LINE_41}),
    ),
    (TieredContribution, frozenset({RC381_PART_3_LINE_38}), frozenset({RC381_PART_3_LINE_42})),
    (TieredContribution, frozenset({RC381_PART_3_LINE_38}), frozenset({RC381_PART_3_LINE_43})),
    (
        Sum,
        frozenset({RC381_PART_3_LINE_42, RC381_PART_3_LINE_43}),
        frozenset({RC381_PART_3_LINE_44}),
    ),
    (TieredContribution, frozenset({RC381_PART_3_LINE_35}), frozenset({RC381_PART_3_LINE_46})),
    (
        Sum,
        frozenset({RC381_PART_3_LINE_20, RC381_PART_3_LINE_40}),
        frozenset({RC381_PART_3_LINE_49}),
    ),
    (
        Sum,
        frozenset({RC381_PART_3_LINE_22, RC381_PART_3_LINE_42}),
        frozenset({RC381_PART_3_LINE_52}),
    ),
    (
        Subtract,
        frozenset({RC381_PART_3_LINE_49, RC381_PART_3_LINE_52}),
        frozenset({RC381_PART_3_LINE_53}),
    ),
    (
        Sum,
        frozenset({RC381_PART_3_LINE_21, RC381_PART_3_LINE_41}),
        frozenset({RC381_PART_3_LINE_56}),
    ),
    (
        Sum,
        frozenset({RC381_PART_3_LINE_23, RC381_PART_3_LINE_43}),
        frozenset({RC381_PART_3_LINE_59}),
    ),
    (
        Subtract,
        frozenset({RC381_PART_3_LINE_56, RC381_PART_3_LINE_59}),
        frozenset({RC381_PART_3_LINE_60}),
    ),
    (
        Sum,
        frozenset({RC381_PART_3_LINE_53, RC381_PART_3_LINE_60}),
        frozenset({RC381_PART_3_LINE_61}),
    ),
    (
        Sum,
        frozenset({T4_CPP_SECOND_ADDITIONAL_BOX_16A, T4_QPP_SECOND_ADDITIONAL_BOX_17A}),
        frozenset({RC381_PART_3_LINE_64}),
    ),
    (
        Sum,
        frozenset({RC381_PART_3_LINE_26, RC381_PART_3_LINE_46}),
        frozenset({RC381_PART_3_LINE_67}),
    ),
    (
        Subtract,
        frozenset({RC381_PART_3_LINE_64, RC381_PART_3_LINE_67}),
        frozenset({RC381_PART_3_LINE_68}),
    ),
    (
        Sum,
        frozenset({RC381_PART_3_LINE_61, RC381_PART_3_LINE_68}),
        frozenset({RC381_PART_3_LINE_69}),
    ),
    (
        Sum,
        frozenset({RC381_PART_3_LINE_59, RC381_PART_3_LINE_67}),
        frozenset({RC381_PART_3_LINE_73}),
    ),
    (
        ChooseBySign,
        frozenset({RC381_PART_3_LINE_49, RC381_PART_3_LINE_52, RC381_PART_3_LINE_53}),
        frozenset({RC381_PART_3_LINE_75}),
    ),
    (
        PositivePartOfNegation,
        frozenset({RC381_PART_3_LINE_53}),
        frozenset({RC381_PART_3_LINE_76}),
    ),
    (
        LesserOfWhenPositive,
        frozenset({RC381_PART_3_LINE_60, RC381_PART_3_LINE_76}),
        frozenset({RC381_PART_3_LINE_77}),
    ),
    (
        Subtract,
        frozenset({RC381_PART_3_LINE_76, RC381_PART_3_LINE_77}),
        frozenset({RC381_PART_3_LINE_78}),
    ),
    (
        Sum,
        frozenset({RC381_PART_3_LINE_75, RC381_PART_3_LINE_77}),
        frozenset({RC381_PART_3_LINE_79}),
    ),
    (
        LesserOfWhenPositive,
        frozenset({RC381_PART_3_LINE_68, RC381_PART_3_LINE_78}),
        frozenset({RC381_PART_3_LINE_80}),
    ),
    (
        Sum,
        frozenset({RC381_PART_3_LINE_79, RC381_PART_3_LINE_80}),
        frozenset({RC381_PART_3_LINE_81}),
    ),
    (
        ChooseBySign,
        frozenset({RC381_PART_3_LINE_56, RC381_PART_3_LINE_59, RC381_PART_3_LINE_60}),
        frozenset({RC381_PART_3_LINE_82}),
    ),
    (
        PositivePartOfNegation,
        frozenset({RC381_PART_3_LINE_60}),
        frozenset({RC381_PART_3_LINE_83}),
    ),
    (
        LesserOfWhenPositive,
        frozenset({RC381_PART_3_LINE_53, RC381_PART_3_LINE_83}),
        frozenset({RC381_PART_3_LINE_84}),
    ),
    (
        Subtract,
        frozenset({RC381_PART_3_LINE_83, RC381_PART_3_LINE_84}),
        frozenset({RC381_PART_3_LINE_85}),
    ),
    (
        Sum,
        frozenset({RC381_PART_3_LINE_82, RC381_PART_3_LINE_84}),
        frozenset({RC381_PART_3_LINE_86}),
    ),
    (
        Subtract,
        frozenset({RC381_PART_3_LINE_68, RC381_PART_3_LINE_80}),
        frozenset({RC381_PART_3_LINE_87_DIFFERENCE}),
    ),
    (
        LesserOfWhenPositive,
        frozenset({RC381_PART_3_LINE_85, RC381_PART_3_LINE_87_DIFFERENCE}),
        frozenset({RC381_PART_3_LINE_87}),
    ),
    (
        Sum,
        frozenset({RC381_PART_3_LINE_86, RC381_PART_3_LINE_87}),
        frozenset({RC381_PART_3_LINE_88}),
    ),
    (
        ChooseBySign,
        frozenset({RC381_PART_3_LINE_64, RC381_PART_3_LINE_67, RC381_PART_3_LINE_68}),
        frozenset({RC381_PART_3_LINE_89}),
    ),
    (
        PositivePartOfNegation,
        frozenset({RC381_PART_3_LINE_68}),
        frozenset({RC381_PART_3_LINE_90}),
    ),
    (
        LesserOfWhenPositive,
        frozenset({RC381_PART_3_LINE_61, RC381_PART_3_LINE_90}),
        frozenset({RC381_PART_3_LINE_91}),
    ),
    (
        Sum,
        frozenset({RC381_PART_3_LINE_89, RC381_PART_3_LINE_91}),
        frozenset({RC381_PART_3_LINE_92}),
    ),
    (
        Sum,
        frozenset({RC381_PART_3_LINE_88, RC381_PART_3_LINE_92}),
        frozenset({RC381_PART_3_LINE_93}),
    ),
    (
        ChooseBySign,
        frozenset({RC381_PART_3_LINE_52, RC381_PART_3_LINE_69, RC381_PART_3_LINE_81}),
        frozenset({RC381_EMPLOYMENT_CPP_BASE_CONTRIBUTIONS}),
    ),
    (
        ChooseBySign,
        frozenset({RC381_PART_3_LINE_69, RC381_PART_3_LINE_73, RC381_PART_3_LINE_93}),
        frozenset({RC381_EMPLOYMENT_CPP_ENHANCED_CONTRIBUTIONS}),
    ),
    (
        SumNotBelowZero,
        frozenset({RC381_PART_3_LINE_69}),
        frozenset({RC381_CPP_OVERPAYMENT}),
    ),
    (
        Sum,
        frozenset({PENSIONABLE_NET_SELF_EMPLOYMENT_EARNINGS, CPT20_EARNINGS, CPT20_T4_EARNINGS}),
        frozenset({RC381_PART_4_LINE_4}),
    ),
    (
        Subtract,
        frozenset({RC381_PART_3_LINE_20, RC381_PART_3_LINE_22}),
        frozenset({RC381_PART_4_LINE_8}),
    ),
    (
        Subtract,
        frozenset({RC381_PART_3_LINE_21, RC381_PART_3_LINE_23}),
        frozenset({RC381_PART_4_LINE_11}),
    ),
    (
        Sum,
        frozenset({RC381_PART_4_LINE_8, RC381_PART_4_LINE_11}),
        frozenset({RC381_PART_4_LINE_12}),
    ),
    (
        Subtract,
        frozenset({T4_CPP_CONTRIBUTIONS_BOX_16, RC381_PART_4_LINE_12}),
        frozenset({RC381_PART_4_LINE_13_DIFFERENCE}),
    ),
    (
        ChooseBySign,
        frozenset(
            {RC381_PART_3_LINE_61, RC381_PART_4_LINE_13_DIFFERENCE, T4_CPP_CONTRIBUTIONS_BOX_16}
        ),
        frozenset({RC381_PART_4_LINE_13}),
    ),
    (
        PositivePartOfNegation,
        frozenset({RC381_PART_3_LINE_61}),
        frozenset({RC381_PART_4_LINE_14}),
    ),
    (
        Subtract,
        frozenset({T4_CPP_CONTRIBUTIONS_BOX_16, RC381_PART_3_LINE_24}),
        frozenset({RC381_PART_4_LINE_17}),
    ),
    (
        PositivePartOfNegation,
        frozenset({RC381_PART_4_LINE_17}),
        frozenset({RC381_PART_4_LINE_17A}),
    ),
    (
        Subtract,
        frozenset({T4_QPP_CONTRIBUTIONS_BOX_17, RC381_PART_3_LINE_44}),
        frozenset({RC381_PART_4_LINE_20}),
    ),
    (
        LesserOfWhenPositiveInBrackets,
        frozenset({RC381_PART_4_LINE_17}),
        frozenset({RC381_PART_4_LINE_21_FROM_LINE_17}),
    ),
    (
        LesserOfWhenPositive,
        frozenset({RC381_PART_4_LINE_20, RC381_PART_4_LINE_17A}),
        frozenset({RC381_PART_4_LINE_21_LESSER}),
    ),
    (
        ChooseBySign,
        frozenset(
            {
                RC381_PART_4_LINE_20,
                RC381_PART_4_LINE_21_LESSER,
                RC381_PART_4_LINE_21_FROM_LINE_17,
            }
        ),
        frozenset({RC381_PART_4_LINE_21}),
    ),
    (
        RatioTruncatedAtMostOne,
        frozenset({RC381_PART_4_LINE_17A, RC381_PART_4_LINE_14}),
        frozenset({RC381_PART_4_LINE_22}),
    ),
    (
        LesserOf,
        frozenset({RC381_PART_3_LINE_68, RC381_PART_4_LINE_17A}),
        frozenset({RC381_PART_4_LINE_23_LESSER}),
    ),
    (
        ApplyChosenRate,
        frozenset({RC381_PART_3_LINE_68, RC381_PART_4_LINE_22}),
        frozenset({RC381_PART_4_LINE_23_MULTIPLIED}),
    ),
    (
        ChooseBySign,
        frozenset(
            {
                RC381_PART_3_LINE_69,
                RC381_PART_4_LINE_23_MULTIPLIED,
                RC381_PART_4_LINE_23_LESSER,
            }
        ),
        frozenset({RC381_PART_4_LINE_23}),
    ),
    (
        LesserOf,
        frozenset({RC381_PART_4_LINE_17A, RC381_PART_4_LINE_23}),
        frozenset({RC381_PART_4_LINE_24_LESSER}),
    ),
    (
        ChooseBySign,
        frozenset({RC381_PART_3_LINE_61, RC381_PART_4_LINE_24_LESSER}),
        frozenset({RC381_PART_4_LINE_24}),
    ),
    (
        ChooseBySign,
        frozenset({RC381_PART_3_LINE_61, RC381_PART_4_LINE_21}),
        frozenset({RC381_PART_4_LINE_25A}),
    ),
    (
        Sum,
        frozenset({RC381_PART_4_LINE_24, RC381_PART_4_LINE_13, RC381_PART_4_LINE_25A}),
        frozenset({RC381_PART_4_LINE_26}),
    ),
    (ApplyFraction, frozenset({RC381_PART_4_LINE_26}), frozenset({RC381_PART_4_LINE_27})),
    (
        Subtract,
        frozenset({RC381_PART_3_LINE_61, RC381_PART_4_LINE_12}),
        frozenset({RC381_PART_4_LINE_31_DIFFERENCE}),
    ),
    (
        ChooseBySign,
        frozenset({RC381_PART_3_LINE_61, RC381_PART_4_LINE_31_DIFFERENCE}),
        frozenset({RC381_PART_4_LINE_31}),
    ),
    (
        Subtract,
        frozenset({T4_QPP_CONTRIBUTIONS_BOX_17, RC381_PART_4_LINE_31}),
        frozenset({RC381_PART_4_LINE_32}),
    ),
    (PositivePartOfNegation, frozenset({RC381_PART_3_LINE_61}), frozenset({RC381_PART_4_LINE_33})),
    (
        LesserOfWhenPositive,
        frozenset({RC381_PART_4_LINE_17A, RC381_PART_4_LINE_33}),
        frozenset({RC381_PART_4_LINE_34}),
    ),
    (
        Subtract,
        frozenset({RC381_PART_4_LINE_33, RC381_PART_4_LINE_34}),
        frozenset({RC381_PART_4_LINE_35}),
    ),
    (
        LesserOfWhenPositive,
        frozenset({RC381_PART_4_LINE_17}),
        frozenset({RC381_PART_4_LINE_35AA_FROM_LINE_17}),
    ),
    (
        ChooseBySign,
        frozenset({RC381_PART_4_LINE_35, RC381_PART_4_LINE_35AA_FROM_LINE_17}),
        frozenset({RC381_PART_4_LINE_35AA}),
    ),
    (
        LesserOfWhenPositiveInBrackets,
        frozenset({RC381_PART_4_LINE_20}),
        frozenset({RC381_PART_4_LINE_35AB_FROM_LINE_20}),
    ),
    (
        ChooseBySign,
        frozenset({RC381_PART_4_LINE_35, RC381_PART_4_LINE_35AB_FROM_LINE_20}),
        frozenset({RC381_PART_4_LINE_35AB_WHEN_LINE_35_ZERO}),
    ),
    (
        ChooseBySign,
        frozenset({RC381_PART_3_LINE_61, RC381_PART_4_LINE_35AB_WHEN_LINE_35_ZERO}),
        frozenset({RC381_PART_4_LINE_35AB}),
    ),
    (
        Sum,
        frozenset({RC381_PART_4_LINE_35AA, RC381_PART_4_LINE_35AB}),
        frozenset({RC381_PART_4_LINE_35A}),
    ),
    (SumNotBelowZero, frozenset({RC381_PART_3_LINE_68}), frozenset({RC381_PART_4_LINE_36})),
    (
        Subtract,
        frozenset({RC381_PART_4_LINE_36, RC381_PART_4_LINE_24}),
        frozenset({RC381_PART_4_LINE_38}),
    ),
    (
        LesserOf,
        frozenset({RC381_PART_4_LINE_35, RC381_PART_4_LINE_38}),
        frozenset({RC381_PART_4_LINE_39}),
    ),
    (
        Sum,
        frozenset({RC381_PART_4_LINE_32, RC381_PART_4_LINE_35A, RC381_PART_4_LINE_39}),
        frozenset({RC381_PART_4_LINE_40}),
    ),
    (ApplyFraction, frozenset({RC381_PART_4_LINE_40}), frozenset({RC381_PART_4_LINE_41})),
    (
        Sum,
        frozenset({RC381_PART_4_LINE_27, RC381_PART_4_LINE_41}),
        frozenset({RC381_PART_4_LINE_42}),
    ),
    (
        Subtract,
        frozenset({T4_CPP_SECOND_ADDITIONAL_BOX_16A, RC381_PART_3_LINE_26}),
        frozenset({RC381_PART_4_LINE_46_DIFFERENCE}),
    ),
    (
        ChooseBySign,
        frozenset({RC381_PART_3_LINE_68, RC381_PART_4_LINE_46_DIFFERENCE}),
        frozenset({RC381_PART_4_LINE_46}),
    ),
    (
        Subtract,
        frozenset({T4_CPP_SECOND_ADDITIONAL_BOX_16A, RC381_PART_4_LINE_46}),
        frozenset({RC381_PART_4_LINE_47}),
    ),
    (
        Subtract,
        frozenset({RC381_PART_3_LINE_68, RC381_PART_4_LINE_46}),
        frozenset({RC381_PART_4_LINE_51_DIFFERENCE}),
    ),
    (
        ChooseBySign,
        frozenset({RC381_PART_3_LINE_68, RC381_PART_4_LINE_51_DIFFERENCE}),
        frozenset({RC381_PART_4_LINE_51}),
    ),
    (
        Subtract,
        frozenset({T4_QPP_SECOND_ADDITIONAL_BOX_17A, RC381_PART_4_LINE_51}),
        frozenset({RC381_PART_4_LINE_52}),
    ),
    (
        Sum,
        frozenset({RC381_PART_4_LINE_47, RC381_PART_4_LINE_52}),
        frozenset({RC381_PART_4_LINE_53}),
    ),
    (PositivePartOfNegation, frozenset({RC381_PART_3_LINE_68}), frozenset({RC381_PART_4_LINE_54})),
    (
        LesserOfWhenPositive,
        frozenset({RC381_PART_3_LINE_61, RC381_PART_4_LINE_54}),
        frozenset({RC381_PART_4_LINE_55}),
    ),
    (
        Sum,
        frozenset({RC381_PART_4_LINE_53, RC381_PART_4_LINE_55}),
        frozenset({RC381_PART_4_LINE_56}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({CPP_MAXIMUM_PENSIONABLE_EARNINGS, CPP_BASIC_EXEMPTION}),
        frozenset({RC381_PART_4_LINE_59}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({RC381_PART_4_LINE_59, RC381_PART_4_LINE_42}),
        frozenset({RC381_PART_4_LINE_61}),
    ),
    (
        LesserOf,
        frozenset({RC381_PART_4_LINE_4, RC381_PART_4_LINE_61}),
        frozenset({RC381_PART_4_LINE_62}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({CPP_BASIC_EXEMPTION, RC381_PART_3_LINE_3}),
        frozenset({RC381_PART_4_LINE_65}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({RC381_PART_4_LINE_4, RC381_PART_4_LINE_59}),
        frozenset({RC381_PART_4_LINE_68}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({RC381_PART_4_LINE_65, RC381_PART_4_LINE_68}),
        frozenset({RC381_PART_4_LINE_69}),
    ),
    (
        Subtract,
        frozenset({RC381_PART_4_LINE_62, RC381_PART_4_LINE_69}),
        frozenset({RC381_PART_4_LINE_70}),
    ),
    (
        Sum,
        frozenset({RC381_PART_4_LINE_4, RC381_PART_3_LINE_11, RC381_PART_3_LINE_31}),
        frozenset({RC381_PART_4_LINE_74}),
    ),
    (DividedByRate, frozenset({RC381_PART_4_LINE_56}), frozenset({RC381_PART_4_LINE_76})),
    (
        SubtractNotBelowZero,
        frozenset({CPP_SECOND_ADDITIONAL_EARNINGS_MAXIMUM, RC381_PART_4_LINE_76}),
        frozenset({RC381_PART_4_LINE_77}),
    ),
    (
        Subtract,
        frozenset({RC381_PART_4_LINE_4, RC381_PART_4_LINE_65}),
        frozenset({RC381_PART_4_LINE_80}),
    ),
    (
        Subtract,
        frozenset({RC381_PART_4_LINE_80, RC381_PART_4_LINE_70}),
        frozenset({RC381_PART_4_LINE_82}),
    ),
    (
        LesserOf,
        frozenset({RC381_PART_4_LINE_77, RC381_PART_4_LINE_82}),
        frozenset({RC381_PART_4_LINE_83_LESSER}),
    ),
    (
        AmountWhenMore,
        frozenset(
            {RC381_PART_4_LINE_83_LESSER, RC381_PART_4_LINE_74, CPP_MAXIMUM_PENSIONABLE_EARNINGS}
        ),
        frozenset({RC381_PART_4_LINE_83}),
    ),
    (TieredContribution, frozenset({RC381_PART_4_LINE_70}), frozenset({RC381_PART_4_LINE_84})),
    (TieredContribution, frozenset({RC381_PART_4_LINE_70}), frozenset({RC381_PART_4_LINE_85})),
    (TieredContribution, frozenset({RC381_PART_4_LINE_83}), frozenset({RC381_PART_4_LINE_86})),
    (
        Sum,
        frozenset({RC381_PART_4_LINE_85, RC381_PART_4_LINE_86}),
        frozenset({RC381_PART_4_LINE_87}),
    ),
    (
        Sum,
        frozenset({RC381_PART_4_LINE_84, RC381_PART_4_LINE_87}),
        frozenset({RC381_PART_4_LINE_88}),
    ),
    (
        SumNotBelowZero,
        frozenset({RC381_PART_3_LINE_69}),
        frozenset({RC381_PART_4_LINE_89_FROM_LINE_69}),
    ),
    (
        ApplyFraction,
        frozenset({RC381_PART_4_LINE_89_FROM_LINE_69}),
        frozenset({RC381_PART_4_LINE_89}),
    ),
    (
        Subtract,
        frozenset({RC381_PART_4_LINE_88, RC381_PART_4_LINE_89}),
        frozenset({RC381_PART_4_LINE_90}),
    ),
    (
        SumNotBelowZero,
        frozenset({RC381_PART_4_LINE_90}),
        frozenset({RC381_SELF_EMPLOYMENT_CPP_CONTRIBUTIONS}),
    ),
    (
        PositivePartOfNegation,
        frozenset({RC381_PART_4_LINE_90}),
        frozenset({RC381_PART_4_LINE_91_FROM_LINE_90}),
    ),
    (ApplyRate, frozenset({RC381_PART_4_LINE_91_FROM_LINE_90}), frozenset({RC381_PART_4_LINE_91})),
}
