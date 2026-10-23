"""The CA-ON manifest entries of one family of lines (see `test_manifest.py`).

Form RC381 (2025), "Inter-Provincial Calculation for CPP and QPP Contributions and Overpayments",
Part 2 and Part 3 lines 1 to 26 (the first of several wiring PRs). Part 2 lines C to F are
Schedule 8 Part 2's lines B to E, the same table read with the same months (line A), so they are
the existing artifacts and no step is repeated for them. The manifest part for these entries is
`08a_rc381_part_2_and_3.yaml`.
"""

from __future__ import annotations

from app.domain.capabilities.amount_by_count import AmountForCount
from app.domain.capabilities.apply_rate import ApplyRate
from app.domain.capabilities.contribution_tier import TieredContribution
from app.domain.capabilities.lesser_of import LesserOf
from app.domain.capabilities.subtract import Subtract
from app.domain.capabilities.subtract_not_below_zero import SubtractNotBelowZero
from app.domain.capabilities.sum import Sum
from app.domain.manifest import CapabilitySelection
from app.jurisdictions.ca.capabilities.amount_when_more import AmountWhenMore
from app.jurisdictions.ca.capabilities.apply_chosen_rate import ApplyChosenRate
from app.jurisdictions.ca.capabilities.count_at_least import CountAtLeast
from app.jurisdictions.ca.capabilities.ratio_truncated import RatioTruncated
from app.jurisdictions.ca.catalog import (
    CPP_ADDITIONAL_MAXIMUM_PENSIONABLE_EARNINGS,
    CPP_BASIC_EXEMPTION,
    CPP_MAXIMUM_PENSIONABLE_EARNINGS,
    CPP_MONTHS,
    CPP_SECOND_ADDITIONAL_EARNINGS_MAXIMUM,
    CPP_T4_BASE_AND_FIRST_ADDITIONAL_CONTRIBUTIONS,
    QPP_MONTHS,
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
    T4_CPP_PENSIONABLE_EARNINGS_OUTSIDE_QUEBEC,
    T4_QPP_PENSIONABLE_EARNINGS_IN_QUEBEC,
)

# Part 2 line B and the Part 3 lines 1, 2 and 19 are the filer's entries. Line 25 (box 16A) is
# read by Part 3 line 64, which a later PR wires, and the composition refuses an input that
# nothing consumes, so it is declared there.
INPUTS = frozenset(
    {
        "ca/qpp_months",
        "ca/t4_cpp_pensionable_earnings_outside_quebec",
        "ca/t4_qpp_pensionable_earnings_in_quebec",
    }
)

# Nothing reads these yet (the PRs that wire Part 3 lines 27 onward read them, and each removes
# its own from this set): Part 2 lines G to J, the QPP side of the monthly proration table (read
# by Part 3 lines 27 to 30 and 37), and the lines of Part 3's CPP side no step of this PR reads.
OUTPUTS = frozenset(
    {
        "ca/rc381_part_2_line_g",
        "ca/rc381_part_2_line_h",
        "ca/rc381_part_2_line_i",
        "ca/rc381_part_2_line_j",
        "ca/rc381_part_3_line_21",
        "ca/rc381_part_3_line_24",
        "ca/rc381_part_3_line_26",
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
        consumes={"base": "ca/cpp_t4_base_and_first_additional_contributions"},
        produces={"output": "ca/rc381_part_3_line_20"},
    ),
    # Line 21 "Actual first additional contributions on CPP pensionable earnings: Line 19 minus
    # line 20".
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/cpp_t4_base_and_first_additional_contributions",
            "less": "ca/rc381_part_3_line_20",
        },
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
    (
        ApplyRate,
        frozenset({CPP_T4_BASE_AND_FIRST_ADDITIONAL_CONTRIBUTIONS}),
        frozenset({RC381_PART_3_LINE_20}),
    ),
    (
        Subtract,
        frozenset({CPP_T4_BASE_AND_FIRST_ADDITIONAL_CONTRIBUTIONS, RC381_PART_3_LINE_20}),
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
}
