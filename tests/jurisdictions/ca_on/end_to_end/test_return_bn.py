"""CA-ON 2025 end to end: return bn."""

from __future__ import annotations

from collections.abc import Mapping
from decimal import Decimal
from typing import Any

from app.domain.artifact import ArtifactKind
from app.domain.parameters.fraction import Fraction
from app.domain.parameters.rate import Rate
from app.domain.parameters.rounding import RoundingMode, RoundTo
from app.domain.trace import ChosenByCountLine, DividedByRateLine, FractionAppliedLine
from app.domain.worksheet import Worksheet
from app.jurisdictions.ca.catalog import (
    AMT_DEDUCTIONS_TOTAL,
    CPP_ACTUAL_BASE_CONTRIBUTIONS,
    CPP_ACTUAL_FIRST_ADDITIONAL_CONTRIBUTIONS,
    CPP_BASE_AND_FIRST_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE,
    CPP_BASE_CONTRIBUTIONS,
    CPP_BASE_CONTRIBUTIONS_DIFFERENCE,
    CPP_BASE_CONTRIBUTIONS_ON_RETURN,
    CPP_CONTRIBUTIONS_DIFFERENCE,
    CPP_ENHANCED_CONTRIBUTIONS,
    CPP_ENHANCED_CONTRIBUTIONS_ON_RETURN,
    CPP_FIRST_ADDITIONAL_CONTRIBUTIONS,
    CPP_FIRST_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE,
    CPP_LINE_16_NEGATIVE_LINE_19_POSITIVE,
    CPP_LINE_16_NOT_NEGATIVE,
    CPP_LINE_16_POSITIVE,
    CPP_LINE_19_NOT_NEGATIVE,
    CPP_LINE_20_POSITIVE,
    CPP_LINE_23_AND_LINE_33_POSITIVE,
    CPP_LINE_23_AND_LINE_40_POSITIVE,
    CPP_LINE_23_NOT_NEGATIVE,
    CPP_LINE_24_POSITIVE,
    CPP_OVERPAYMENT,
    CPP_PART_3B_LINE_30,
    CPP_PART_3B_LINE_31,
    CPP_PART_3B_LINE_32,
    CPP_PART_3B_LINE_33,
    CPP_PART_3B_LINE_34,
    CPP_PART_3B_LINE_35,
    CPP_PART_3B_LINE_36,
    CPP_PART_3B_LINE_37,
    CPP_PART_3B_LINE_38,
    CPP_PART_3B_LINE_39,
    CPP_PART_3B_LINE_40,
    CPP_PART_3B_LINE_41,
    CPP_PART_3B_LINE_42,
    CPP_PART_3B_LINE_43,
    CPP_PART_3B_LINE_44,
    CPP_PART_3B_LINE_45,
    CPP_PART_3B_LINE_46,
    CPP_PART_3B_LINE_47,
    CPP_PART_3B_LINE_48,
    CPP_PART_5_LINE_4,
    CPP_PART_5_LINE_6,
    CPP_PART_5_LINE_7,
    CPP_PART_5_LINE_8,
    CPP_PART_5_LINE_9,
    CPP_PART_5_LINE_9_LESSER,
    CPP_PART_5_LINE_10,
    CPP_PART_5_LINE_12,
    CPP_PART_5_LINE_13,
    CPP_PART_5_LINE_14,
    CPP_PART_5_LINE_15,
    CPP_PART_5_LINE_15_LESSER,
    CPP_PART_5_LINE_16,
    CPP_PART_5_LINE_19,
    CPP_PART_5_LINE_20,
    CPP_PART_5_LINE_20_NEGATIVE_LINE_23_POSITIVE,
    CPP_PART_5_LINE_20_POSITIVE_LINE_23_NEGATIVE,
    CPP_PART_5_LINE_21,
    CPP_PART_5_LINE_22,
    CPP_PART_5_LINE_25,
    CPP_PART_5_LINE_28,
    CPP_PART_5_LINE_29,
    CPP_PART_5_LINE_30,
    CPP_PART_5_LINE_33,
    CPP_PART_5_LINE_33_MORE_THAN_LINE_17,
    CPP_PART_5_LINE_35,
    CPP_PART_5_LINE_36,
    CPP_PART_5_LINE_39,
    CPP_PART_5_LINE_41,
    CPP_PART_5_LINE_42,
    CPP_PART_5_LINE_42_LESSER,
    CPP_REQUIRED_BASE_AND_FIRST_ADDITIONAL_CONTRIBUTIONS,
    CPP_SECOND_ADDITIONAL_CONTRIBUTIONS,
    CPP_SECOND_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE,
    CPP_T4_BASE_AND_FIRST_ADDITIONAL_CONTRIBUTIONS,
    CPP_T4_SECOND_ADDITIONAL_CONTRIBUTIONS,
    CPP_ZERO,
    DEDUCTIONS_FROM_TOTAL_INCOME,
    NON_REFUNDABLE_CREDIT_AMOUNTS,
    REFUND_OR_BALANCE_OWING,
    TOTAL_CREDITS,
)
from app.jurisdictions.ca_on import catalog as ontario
from tests.jurisdictions.ca_on.end_to_end.support import D, compute

CENT = RoundTo(D("0.01"), RoundingMode.HALF_UP)

# Return BN: employment income of $60,000, the T4 box 16 total of $3,500.00 (Schedule 8 line 8)
# and box 16A of $0 (line 21), so line 24 is positive. The required amounts are base 4.95% x
# 56,500 = 2,796.75 (line 11), first additional 1% x 56,500 = 565.00 (line 12) and so line 13 is
# 3,361.75 and line 22 is 0. Line 9 is 2,911.7655 rounded to 2,911.77, line 10 is 588.23, line 16
# is 115.02, line 19 is 23.23, line 20 is 138.25 and line 24 is 138.25. The other cases of the
# same employment income: box 16 of $3,300.00 gives line 24 of -61.75 (in brackets), and box 16
# equal to the required $3,361.75 gives 0.


def test_t4_contributions_above_the_required_ones_give_a_positive_line_24() -> None:
    # Return BN as filed: box 16 of $3,500.00 is 138.25 more than line 13.
    worksheet = compute(
        "60000",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
        cpp_t4_base_and_first_additional_contributions="3500.00",
        cpp_t4_second_additional_contributions="0",
    )

    assert worksheet.get(CPP_BASE_CONTRIBUTIONS).value == D("2796.75")
    assert worksheet.get(CPP_FIRST_ADDITIONAL_CONTRIBUTIONS).value == D("565.00")
    assert worksheet.get(CPP_SECOND_ADDITIONAL_CONTRIBUTIONS).value == D("0.00")
    # Line 9: 83.1933% of 3,500.00, 2,911.7655, rounded half-up to the cent.
    assert worksheet.get(CPP_ACTUAL_BASE_CONTRIBUTIONS).value == D("2911.77")
    # Line 10: line 8 minus line 9.
    assert worksheet.get(CPP_ACTUAL_FIRST_ADDITIONAL_CONTRIBUTIONS).value == D("588.23")
    # Line 13: line 11 plus line 12.
    assert worksheet.get(CPP_REQUIRED_BASE_AND_FIRST_ADDITIONAL_CONTRIBUTIONS).value == D("3361.75")
    # Line 16: line 14 (line 9) minus line 15 (line 11); line 19: line 17 (line 10) minus line 18
    # (line 12); line 20: line 16 plus line 19.
    assert worksheet.get(CPP_BASE_CONTRIBUTIONS_DIFFERENCE).value == D("115.02")
    assert worksheet.get(CPP_FIRST_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE).value == D("23.23")
    assert worksheet.get(CPP_BASE_AND_FIRST_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE).value == D(
        "138.25"
    )
    # Line 23: line 21 ($0) minus line 22 ($0); line 24: line 20 plus line 23.
    assert worksheet.get(CPP_SECOND_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE).value == D("0.00")
    assert worksheet.get(CPP_CONTRIBUTIONS_DIFFERENCE).value == D("138.25")


def test_t4_contributions_below_the_required_ones_give_a_negative_line_24_in_brackets() -> None:
    # Box 16 of $3,300.00: line 9 is 2,745.38, line 16 is -51.37, line 10 is 554.62, line 19 is
    # -10.38, line 20 is -61.75 and line 24 is -61.75 (shown in brackets on the form).
    worksheet = compute(
        "60000",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
        cpp_t4_base_and_first_additional_contributions="3300.00",
        cpp_t4_second_additional_contributions="0",
    )

    assert worksheet.get(CPP_ACTUAL_BASE_CONTRIBUTIONS).value == D("2745.38")
    assert worksheet.get(CPP_ACTUAL_FIRST_ADDITIONAL_CONTRIBUTIONS).value == D("554.62")
    assert worksheet.get(CPP_BASE_CONTRIBUTIONS_DIFFERENCE).value == D("-51.37")
    assert worksheet.get(CPP_FIRST_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE).value == D("-10.38")
    assert worksheet.get(CPP_BASE_AND_FIRST_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE).value == D(
        "-61.75"
    )
    assert worksheet.get(CPP_CONTRIBUTIONS_DIFFERENCE).value == D("-61.75")


def test_t4_contributions_equal_to_the_required_ones_give_line_24_zero() -> None:
    # Box 16 of $3,361.75 is line 13: line 9 is 2,796.75 (equal to line 11) and line 24 is 0.
    worksheet = compute(
        "60000",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
        cpp_t4_base_and_first_additional_contributions="3361.75",
        cpp_t4_second_additional_contributions="0",
    )

    assert worksheet.get(CPP_ACTUAL_BASE_CONTRIBUTIONS).value == D("2796.75")
    assert worksheet.get(CPP_ACTUAL_FIRST_ADDITIONAL_CONTRIBUTIONS).value == D("565.00")
    assert worksheet.get(CPP_BASE_CONTRIBUTIONS_DIFFERENCE).value == D("0.00")
    assert worksheet.get(CPP_FIRST_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE).value == D("0.00")
    assert worksheet.get(CPP_CONTRIBUTIONS_DIFFERENCE).value == D("0.00")


def test_without_t4_inputs_the_required_contributions_are_the_default_so_line_24_is_zero() -> None:
    # The helper's default is the required amount for the employment income: box 16 of
    # $3,361.75 and box 16A of $0 at $60,000, so line 24 is 0 with no T4 input given.
    worksheet = compute("60000", (), "0", "0", "0", "0", "0")

    assert worksheet.get(CPP_T4_BASE_AND_FIRST_ADDITIONAL_CONTRIBUTIONS).value == D("3361.75")
    assert worksheet.get(CPP_T4_SECOND_ADDITIONAL_CONTRIBUTIONS).value == D("0")
    assert worksheet.get(CPP_CONTRIBUTIONS_DIFFERENCE).value == D("0.00")


def test_a_second_additional_contribution_above_the_required_one_is_a_positive_line_23() -> None:
    # Employment income of $90,000: line 22 is 4% of 9,900 = 396.00. Box 16A of $500.00 is 104.00
    # more, so line 23 and line 24 are 104.00 (the base and first parts are the required ones).
    worksheet = compute(
        "90000",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
        cpp_t4_base_and_first_additional_contributions="4034.10",
        cpp_t4_second_additional_contributions="500",
    )

    assert worksheet.get(CPP_SECOND_ADDITIONAL_CONTRIBUTIONS).value == D("396.00")
    assert worksheet.get(CPP_SECOND_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE).value == D("104.00")
    assert worksheet.get(CPP_BASE_AND_FIRST_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE).value == D("0.00")
    assert worksheet.get(CPP_CONTRIBUTIONS_DIFFERENCE).value == D("104.00")


def test_form_rounding_moves_lines_16_and_19_a_cent_each_way_but_line_24_stays_zero() -> None:
    # Employment income of $6,900.50: the required base is 168.32 and first additional 34.01, so
    # line 13 is 202.33. Line 9 of 202.33 is 168.33, a cent above line 11, so line 16 is 0.01;
    # line 10 is 34.00, a cent below line 12, so line 19 is -0.01. Line 20 is 0.00 and line 24
    # is 0.00: line 20 is line 8 less line 13, whatever line 9 rounds to.
    worksheet = compute("6900.50", (), "0", "0", "0", "0", "0")

    assert worksheet.get(CPP_REQUIRED_BASE_AND_FIRST_ADDITIONAL_CONTRIBUTIONS).value == D("202.33")
    assert worksheet.get(CPP_ACTUAL_BASE_CONTRIBUTIONS).value == D("168.33")
    assert worksheet.get(CPP_BASE_CONTRIBUTIONS_DIFFERENCE).value == D("0.01")
    assert worksheet.get(CPP_FIRST_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE).value == D("-0.01")
    assert worksheet.get(CPP_BASE_AND_FIRST_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE).value == D("0.00")
    assert worksheet.get(CPP_CONTRIBUTIONS_DIFFERENCE).value == D("0.00")


def assert_values(
    worksheet: Worksheet, expected: Mapping[ArtifactKind[Any], Decimal | int]
) -> None:
    for kind, value in expected.items():
        assert worksheet.get(kind).value == value, kind.identifier


# Schedule 8 Part 3a and Part 3b (T1 lines 30800, 22215 and 44800). Every figure below is derived
# by hand from the form's lines, in order, from the employment income and the two T4 totals:
# line 7 is employment income less 3,500 (to 67,800), line 11 is 4.95% of it (maximum 3,356.10),
# line 12 is 1% of it (maximum 678.00), line 4 is employment income over 71,300 (to 9,900) and
# line 22 is 4% of that (maximum 396.00). Line 9 is box 16 times 83.1933% to the cent. The cases:
# line 24 positive (Part 3a, three cases); line 24 "0" (the helper's default, and two cases where
# the cent rounding of line 9 splits lines 16 and 19); line 24 negative (both differences
# negative; line 23 positive with line 33 positive; line 20 positive with line 23 negative).


def test_part_3a_routes_lines_25_28_and_29_to_lines_30800_22215_and_44800() -> None:
    # Return BN as filed (box 16 of $3,500.00, 138.25 more than line 13): line 24 is positive,
    # so Part 3a applies.
    worksheet = compute(
        "60000",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
        cpp_t4_base_and_first_additional_contributions="3500.00",
        cpp_t4_second_additional_contributions="0",
    )

    assert_values(
        worksheet,
        {
            CPP_BASE_CONTRIBUTIONS_DIFFERENCE: D("115.02"),
            CPP_FIRST_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE: D("23.23"),
            CPP_BASE_AND_FIRST_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE: D("138.25"),
            CPP_SECOND_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE: D("0.00"),
            CPP_CONTRIBUTIONS_DIFFERENCE: D("138.25"),
            CPP_LINE_24_POSITIVE: 1,
            CPP_BASE_CONTRIBUTIONS: D("2796.75"),
            CPP_FIRST_ADDITIONAL_CONTRIBUTIONS: D("565.00"),
            CPP_SECOND_ADDITIONAL_CONTRIBUTIONS: D("0.00"),
            CPP_ENHANCED_CONTRIBUTIONS: D("565.00"),
            CPP_BASE_CONTRIBUTIONS_ON_RETURN: D("2796.75"),
            CPP_ENHANCED_CONTRIBUTIONS_ON_RETURN: D("565.00"),
            CPP_OVERPAYMENT: D("138.25"),
        },
    )


def test_part_3a_with_a_positive_line_23_adds_line_22_to_the_enhanced_deduction() -> None:
    # Employment income of $90,000 and box 16A of $500.00, 104.00 more than line 22: box 16 is
    # the required $4,034.10, so line 24 is line 23, 104.00, and Part 3a applies with line 27
    # (line 22) of 396.00.
    worksheet = compute(
        "90000",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
        cpp_t4_base_and_first_additional_contributions="4034.10",
        cpp_t4_second_additional_contributions="500",
    )

    assert_values(
        worksheet,
        {
            CPP_BASE_CONTRIBUTIONS_DIFFERENCE: D("0.00"),
            CPP_FIRST_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE: D("0.00"),
            CPP_BASE_AND_FIRST_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE: D("0.00"),
            CPP_SECOND_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE: D("104.00"),
            CPP_CONTRIBUTIONS_DIFFERENCE: D("104.00"),
            CPP_LINE_24_POSITIVE: 1,
            CPP_BASE_CONTRIBUTIONS: D("3356.10"),
            CPP_FIRST_ADDITIONAL_CONTRIBUTIONS: D("678.00"),
            CPP_SECOND_ADDITIONAL_CONTRIBUTIONS: D("396.00"),
            CPP_ENHANCED_CONTRIBUTIONS: D("1074.00"),
            CPP_BASE_CONTRIBUTIONS_ON_RETURN: D("3356.10"),
            CPP_ENHANCED_CONTRIBUTIONS_ON_RETURN: D("1074.00"),
            CPP_OVERPAYMENT: D("104.00"),
        },
    )


def test_part_3a_applies_when_a_larger_line_20_outweighs_a_negative_line_23() -> None:
    # Box 16 of $4,300.00 is 265.90 over line 13 and box 16A of $300.00 is 96.00 under line 22,
    # so line 24 is positive (169.90) and Part 3a applies.
    worksheet = compute(
        "90000",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
        cpp_t4_base_and_first_additional_contributions="4300.00",
        cpp_t4_second_additional_contributions="300",
    )

    assert_values(
        worksheet,
        {
            CPP_BASE_CONTRIBUTIONS_DIFFERENCE: D("221.21"),
            CPP_FIRST_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE: D("44.69"),
            CPP_BASE_AND_FIRST_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE: D("265.90"),
            CPP_SECOND_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE: D("-96.00"),
            CPP_CONTRIBUTIONS_DIFFERENCE: D("169.90"),
            CPP_LINE_24_POSITIVE: 1,
            CPP_BASE_CONTRIBUTIONS: D("3356.10"),
            CPP_FIRST_ADDITIONAL_CONTRIBUTIONS: D("678.00"),
            CPP_SECOND_ADDITIONAL_CONTRIBUTIONS: D("396.00"),
            CPP_ENHANCED_CONTRIBUTIONS: D("1074.00"),
            CPP_BASE_CONTRIBUTIONS_ON_RETURN: D("3356.10"),
            CPP_ENHANCED_CONTRIBUTIONS_ON_RETURN: D("1074.00"),
            CPP_OVERPAYMENT: D("169.90"),
        },
    )


def test_part_3b_with_line_24_zero_takes_the_required_lines_11_12_and_22() -> None:
    # Box 16 equal to line 13 (the helper's default): lines 16, 19, 23 and 24 are 0, so Part 3b
    # applies and every count that asks for a positive amount is 0.
    worksheet = compute(
        "60000",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
    )

    assert_values(
        worksheet,
        {
            CPP_BASE_CONTRIBUTIONS_DIFFERENCE: D("0.00"),
            CPP_FIRST_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE: D("0.00"),
            CPP_BASE_AND_FIRST_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE: D("0.00"),
            CPP_SECOND_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE: D("0.00"),
            CPP_CONTRIBUTIONS_DIFFERENCE: D("0.00"),
            CPP_LINE_24_POSITIVE: 0,
            CPP_LINE_16_NOT_NEGATIVE: 1,
            CPP_LINE_19_NOT_NEGATIVE: 1,
            CPP_LINE_23_NOT_NEGATIVE: 1,
            CPP_LINE_16_NEGATIVE_LINE_19_POSITIVE: 0,
            CPP_LINE_23_AND_LINE_33_POSITIVE: 0,
            CPP_LINE_16_POSITIVE: 0,
            CPP_LINE_23_AND_LINE_40_POSITIVE: 0,
            CPP_LINE_20_POSITIVE: 0,
            CPP_PART_3B_LINE_30: D("2796.75"),
            CPP_PART_3B_LINE_31: D("0"),
            CPP_PART_3B_LINE_32: D("0"),
            CPP_PART_3B_LINE_33: D("0"),
            CPP_PART_3B_LINE_34: D("2796.75"),
            CPP_PART_3B_LINE_35: D("0"),
            CPP_PART_3B_LINE_36: D("2796.75"),
            CPP_PART_3B_LINE_37: D("565.00"),
            CPP_PART_3B_LINE_38: D("0"),
            CPP_PART_3B_LINE_39: D("0"),
            CPP_PART_3B_LINE_40: D("0"),
            CPP_PART_3B_LINE_41: D("565.00"),
            CPP_PART_3B_LINE_42: D("0"),
            CPP_PART_3B_LINE_43: D("565.00"),
            CPP_PART_3B_LINE_44: D("0.00"),
            CPP_PART_3B_LINE_45: D("0"),
            CPP_PART_3B_LINE_46: D("0"),
            CPP_PART_3B_LINE_47: D("0.00"),
            CPP_PART_3B_LINE_48: D("565.00"),
            CPP_BASE_CONTRIBUTIONS_ON_RETURN: D("2796.75"),
            CPP_ENHANCED_CONTRIBUTIONS_ON_RETURN: D("565.00"),
            CPP_OVERPAYMENT: D("0"),
        },
    )


def test_part_3b_a_cent_split_between_lines_16_and_19_is_added_back_on_line_39() -> None:
    # Employment income of $6,900.50, box 16 equal to line 13 (202.33): line 9 rounds a cent
    # over line 11 and line 10 a cent under line 12, so line 16 is positive (0.01) and line 19
    # negative (-0.01); line 39 takes the lesser of line 16 and line 38, 0.01, and line 41 adds
    # it to line 37.
    worksheet = compute(
        "6900.50",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
    )

    assert_values(
        worksheet,
        {
            CPP_BASE_CONTRIBUTIONS_DIFFERENCE: D("0.01"),
            CPP_FIRST_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE: D("-0.01"),
            CPP_BASE_AND_FIRST_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE: D("0.00"),
            CPP_SECOND_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE: D("0.00"),
            CPP_CONTRIBUTIONS_DIFFERENCE: D("0.00"),
            CPP_LINE_24_POSITIVE: 0,
            CPP_LINE_16_NOT_NEGATIVE: 1,
            CPP_LINE_19_NOT_NEGATIVE: 0,
            CPP_LINE_23_NOT_NEGATIVE: 1,
            CPP_LINE_16_NEGATIVE_LINE_19_POSITIVE: 0,
            CPP_LINE_23_AND_LINE_33_POSITIVE: 0,
            CPP_LINE_16_POSITIVE: 1,
            CPP_LINE_23_AND_LINE_40_POSITIVE: 0,
            CPP_LINE_20_POSITIVE: 0,
            CPP_PART_3B_LINE_30: D("168.32"),
            CPP_PART_3B_LINE_31: D("0"),
            CPP_PART_3B_LINE_32: D("0"),
            CPP_PART_3B_LINE_33: D("0"),
            CPP_PART_3B_LINE_34: D("168.32"),
            CPP_PART_3B_LINE_35: D("0"),
            CPP_PART_3B_LINE_36: D("168.32"),
            CPP_PART_3B_LINE_37: D("34.00"),
            CPP_PART_3B_LINE_38: D("0.01"),
            CPP_PART_3B_LINE_39: D("0.01"),
            CPP_PART_3B_LINE_40: D("0.00"),
            CPP_PART_3B_LINE_41: D("34.01"),
            CPP_PART_3B_LINE_42: D("0"),
            CPP_PART_3B_LINE_43: D("34.01"),
            CPP_PART_3B_LINE_44: D("0.00"),
            CPP_PART_3B_LINE_45: D("0"),
            CPP_PART_3B_LINE_46: D("0"),
            CPP_PART_3B_LINE_47: D("0.00"),
            CPP_PART_3B_LINE_48: D("34.01"),
            CPP_BASE_CONTRIBUTIONS_ON_RETURN: D("168.32"),
            CPP_ENHANCED_CONTRIBUTIONS_ON_RETURN: D("34.01"),
            CPP_OVERPAYMENT: D("0"),
        },
    )


def test_part_3b_with_a_cent_over_on_line_16_and_a_cent_under_on_line_23() -> None:
    # Box 16 of $4,034.11 is a cent over line 13 and box 16A of $395.99 a cent under line 22:
    # line 24 is 0.00, so Part 3b applies; line 16 is positive but line 19 is 0, so line 39 is
    # the lesser of 0.01 and 0 (line 38); line 20 is positive and line 23 negative, so line 46
    # is the lesser of 0.01 (line 20) and 0.01 (line 45).
    worksheet = compute(
        "90000",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
        cpp_t4_base_and_first_additional_contributions="4034.11",
        cpp_t4_second_additional_contributions="395.99",
    )

    assert_values(
        worksheet,
        {
            CPP_BASE_CONTRIBUTIONS_DIFFERENCE: D("0.01"),
            CPP_FIRST_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE: D("0.00"),
            CPP_BASE_AND_FIRST_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE: D("0.01"),
            CPP_SECOND_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE: D("-0.01"),
            CPP_CONTRIBUTIONS_DIFFERENCE: D("0.00"),
            CPP_LINE_24_POSITIVE: 0,
            CPP_LINE_16_NOT_NEGATIVE: 1,
            CPP_LINE_19_NOT_NEGATIVE: 1,
            CPP_LINE_23_NOT_NEGATIVE: 0,
            CPP_LINE_16_NEGATIVE_LINE_19_POSITIVE: 0,
            CPP_LINE_23_AND_LINE_33_POSITIVE: 0,
            CPP_LINE_16_POSITIVE: 1,
            CPP_LINE_23_AND_LINE_40_POSITIVE: 0,
            CPP_LINE_20_POSITIVE: 1,
            CPP_PART_3B_LINE_30: D("3356.10"),
            CPP_PART_3B_LINE_31: D("0"),
            CPP_PART_3B_LINE_32: D("0"),
            CPP_PART_3B_LINE_33: D("0"),
            CPP_PART_3B_LINE_34: D("3356.10"),
            CPP_PART_3B_LINE_35: D("0"),
            CPP_PART_3B_LINE_36: D("3356.10"),
            CPP_PART_3B_LINE_37: D("678.00"),
            CPP_PART_3B_LINE_38: D("0"),
            CPP_PART_3B_LINE_39: D("0"),
            CPP_PART_3B_LINE_40: D("0"),
            CPP_PART_3B_LINE_41: D("678.00"),
            CPP_PART_3B_LINE_42: D("0"),
            CPP_PART_3B_LINE_43: D("678.00"),
            CPP_PART_3B_LINE_44: D("395.99"),
            CPP_PART_3B_LINE_45: D("0.01"),
            CPP_PART_3B_LINE_46: D("0.01"),
            CPP_PART_3B_LINE_47: D("396.00"),
            CPP_PART_3B_LINE_48: D("1074.00"),
            CPP_BASE_CONTRIBUTIONS_ON_RETURN: D("3356.10"),
            CPP_ENHANCED_CONTRIBUTIONS_ON_RETURN: D("1074.00"),
            CPP_OVERPAYMENT: D("0"),
        },
    )


def test_part_3b_with_both_differences_negative_adds_back_lines_31_and_38() -> None:
    # Box 16 of $3,300.00 is 61.75 under line 13: line 16 and line 19 are both negative, line 23
    # is 0, so lines 32, 35, 39, 42 and 46 are all 0 and lines 31 and 38 are the shortfalls as
    # positive amounts.
    worksheet = compute(
        "60000",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
        cpp_t4_base_and_first_additional_contributions="3300.00",
        cpp_t4_second_additional_contributions="0",
    )

    assert_values(
        worksheet,
        {
            CPP_BASE_CONTRIBUTIONS_DIFFERENCE: D("-51.37"),
            CPP_FIRST_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE: D("-10.38"),
            CPP_BASE_AND_FIRST_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE: D("-61.75"),
            CPP_SECOND_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE: D("0.00"),
            CPP_CONTRIBUTIONS_DIFFERENCE: D("-61.75"),
            CPP_LINE_24_POSITIVE: 0,
            CPP_LINE_16_NOT_NEGATIVE: 0,
            CPP_LINE_19_NOT_NEGATIVE: 0,
            CPP_LINE_23_NOT_NEGATIVE: 1,
            CPP_LINE_16_NEGATIVE_LINE_19_POSITIVE: 0,
            CPP_LINE_23_AND_LINE_33_POSITIVE: 0,
            CPP_LINE_16_POSITIVE: 0,
            CPP_LINE_23_AND_LINE_40_POSITIVE: 0,
            CPP_LINE_20_POSITIVE: 0,
            CPP_PART_3B_LINE_30: D("2745.38"),
            CPP_PART_3B_LINE_31: D("51.37"),
            CPP_PART_3B_LINE_32: D("0"),
            CPP_PART_3B_LINE_33: D("51.37"),
            CPP_PART_3B_LINE_34: D("2745.38"),
            CPP_PART_3B_LINE_35: D("0"),
            CPP_PART_3B_LINE_36: D("2745.38"),
            CPP_PART_3B_LINE_37: D("554.62"),
            CPP_PART_3B_LINE_38: D("10.38"),
            CPP_PART_3B_LINE_39: D("0"),
            CPP_PART_3B_LINE_40: D("10.38"),
            CPP_PART_3B_LINE_41: D("554.62"),
            CPP_PART_3B_LINE_42: D("0"),
            CPP_PART_3B_LINE_43: D("554.62"),
            CPP_PART_3B_LINE_44: D("0.00"),
            CPP_PART_3B_LINE_45: D("0"),
            CPP_PART_3B_LINE_46: D("0"),
            CPP_PART_3B_LINE_47: D("0.00"),
            CPP_PART_3B_LINE_48: D("554.62"),
            CPP_BASE_CONTRIBUTIONS_ON_RETURN: D("2745.38"),
            CPP_ENHANCED_CONTRIBUTIONS_ON_RETURN: D("554.62"),
            CPP_OVERPAYMENT: D("0"),
        },
    )


def test_part_3b_line_35_takes_line_23_when_it_is_less_than_line_33() -> None:
    # Box 16 of $3,434.10 (600.00 under line 13) and box 16A of $401.00 (5.00 over line 22):
    # line 24 is -595.00, line 23 and line 33 are both positive and line 23 is the lesser, so
    # line 35 is 5.00; line 42 is then the lesser of line 40 and line 23 minus line 35, which is
    # 0.
    worksheet = compute(
        "90000",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
        cpp_t4_base_and_first_additional_contributions="3434.10",
        cpp_t4_second_additional_contributions="401.00",
    )

    assert_values(
        worksheet,
        {
            CPP_BASE_CONTRIBUTIONS_DIFFERENCE: D("-499.16"),
            CPP_FIRST_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE: D("-100.84"),
            CPP_BASE_AND_FIRST_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE: D("-600.00"),
            CPP_SECOND_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE: D("5.00"),
            CPP_CONTRIBUTIONS_DIFFERENCE: D("-595.00"),
            CPP_LINE_24_POSITIVE: 0,
            CPP_LINE_16_NOT_NEGATIVE: 0,
            CPP_LINE_19_NOT_NEGATIVE: 0,
            CPP_LINE_23_NOT_NEGATIVE: 1,
            CPP_LINE_16_NEGATIVE_LINE_19_POSITIVE: 0,
            CPP_LINE_23_AND_LINE_33_POSITIVE: 1,
            CPP_LINE_16_POSITIVE: 0,
            CPP_LINE_23_AND_LINE_40_POSITIVE: 1,
            CPP_LINE_20_POSITIVE: 0,
            CPP_PART_3B_LINE_30: D("2856.94"),
            CPP_PART_3B_LINE_31: D("499.16"),
            CPP_PART_3B_LINE_32: D("0"),
            CPP_PART_3B_LINE_33: D("499.16"),
            CPP_PART_3B_LINE_34: D("2856.94"),
            CPP_PART_3B_LINE_35: D("5.00"),
            CPP_PART_3B_LINE_36: D("2861.94"),
            CPP_PART_3B_LINE_37: D("577.16"),
            CPP_PART_3B_LINE_38: D("100.84"),
            CPP_PART_3B_LINE_39: D("0"),
            CPP_PART_3B_LINE_40: D("100.84"),
            CPP_PART_3B_LINE_41: D("577.16"),
            CPP_PART_3B_LINE_42: D("0.00"),
            CPP_PART_3B_LINE_43: D("577.16"),
            CPP_PART_3B_LINE_44: D("396.00"),
            CPP_PART_3B_LINE_45: D("0"),
            CPP_PART_3B_LINE_46: D("0"),
            CPP_PART_3B_LINE_47: D("396.00"),
            CPP_PART_3B_LINE_48: D("973.16"),
            CPP_BASE_CONTRIBUTIONS_ON_RETURN: D("2861.94"),
            CPP_ENHANCED_CONTRIBUTIONS_ON_RETURN: D("973.16"),
            CPP_OVERPAYMENT: D("0"),
        },
    )


def test_part_3b_line_35_takes_line_33_and_line_42_the_rest_of_line_23() -> None:
    # Box 16 of $3,564.10 (470.00 under line 13) and box 16A of $791.00 (395.00 over line 22):
    # line 24 is -75.00. Line 33 (391.01) is less than line 23, so line 35 is 391.01 and line 42
    # is the lesser of line 40 (78.99) and line 23 minus line 35 (3.99), 3.99.
    worksheet = compute(
        "90000",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
        cpp_t4_base_and_first_additional_contributions="3564.10",
        cpp_t4_second_additional_contributions="791.00",
    )

    assert_values(
        worksheet,
        {
            CPP_BASE_CONTRIBUTIONS_DIFFERENCE: D("-391.01"),
            CPP_FIRST_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE: D("-78.99"),
            CPP_BASE_AND_FIRST_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE: D("-470.00"),
            CPP_SECOND_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE: D("395.00"),
            CPP_CONTRIBUTIONS_DIFFERENCE: D("-75.00"),
            CPP_LINE_24_POSITIVE: 0,
            CPP_LINE_16_NOT_NEGATIVE: 0,
            CPP_LINE_19_NOT_NEGATIVE: 0,
            CPP_LINE_23_NOT_NEGATIVE: 1,
            CPP_LINE_16_NEGATIVE_LINE_19_POSITIVE: 0,
            CPP_LINE_23_AND_LINE_33_POSITIVE: 1,
            CPP_LINE_16_POSITIVE: 0,
            CPP_LINE_23_AND_LINE_40_POSITIVE: 1,
            CPP_LINE_20_POSITIVE: 0,
            CPP_PART_3B_LINE_30: D("2965.09"),
            CPP_PART_3B_LINE_31: D("391.01"),
            CPP_PART_3B_LINE_32: D("0"),
            CPP_PART_3B_LINE_33: D("391.01"),
            CPP_PART_3B_LINE_34: D("2965.09"),
            CPP_PART_3B_LINE_35: D("391.01"),
            CPP_PART_3B_LINE_36: D("3356.10"),
            CPP_PART_3B_LINE_37: D("599.01"),
            CPP_PART_3B_LINE_38: D("78.99"),
            CPP_PART_3B_LINE_39: D("0"),
            CPP_PART_3B_LINE_40: D("78.99"),
            CPP_PART_3B_LINE_41: D("599.01"),
            CPP_PART_3B_LINE_42: D("3.99"),
            CPP_PART_3B_LINE_43: D("603.00"),
            CPP_PART_3B_LINE_44: D("396.00"),
            CPP_PART_3B_LINE_45: D("0"),
            CPP_PART_3B_LINE_46: D("0"),
            CPP_PART_3B_LINE_47: D("396.00"),
            CPP_PART_3B_LINE_48: D("999.00"),
            CPP_BASE_CONTRIBUTIONS_ON_RETURN: D("3356.10"),
            CPP_ENHANCED_CONTRIBUTIONS_ON_RETURN: D("999.00"),
            CPP_OVERPAYMENT: D("0"),
        },
    )


def test_part_3b_line_46_takes_line_20_when_line_23_is_negative_and_line_24_is_not_positive() -> (
    None
):
    # Box 16 of $4,100.00 (65.90 over line 13) and box 16A of $300.00 (96.00 under line 22):
    # line 24 is -30.10, so Part 3b applies; line 20 is positive and line 23 negative, so line
    # 46 is the lesser of line 20 (65.90) and line 45 (96.00), 65.90, and line 44 is line 21
    # (300.00).
    worksheet = compute(
        "90000",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
        cpp_t4_base_and_first_additional_contributions="4100.00",
        cpp_t4_second_additional_contributions="300",
    )

    assert_values(
        worksheet,
        {
            CPP_BASE_CONTRIBUTIONS_DIFFERENCE: D("54.83"),
            CPP_FIRST_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE: D("11.07"),
            CPP_BASE_AND_FIRST_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE: D("65.90"),
            CPP_SECOND_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE: D("-96.00"),
            CPP_CONTRIBUTIONS_DIFFERENCE: D("-30.10"),
            CPP_LINE_24_POSITIVE: 0,
            CPP_LINE_16_NOT_NEGATIVE: 1,
            CPP_LINE_19_NOT_NEGATIVE: 1,
            CPP_LINE_23_NOT_NEGATIVE: 0,
            CPP_LINE_16_NEGATIVE_LINE_19_POSITIVE: 0,
            CPP_LINE_23_AND_LINE_33_POSITIVE: 0,
            CPP_LINE_16_POSITIVE: 1,
            CPP_LINE_23_AND_LINE_40_POSITIVE: 0,
            CPP_LINE_20_POSITIVE: 1,
            CPP_PART_3B_LINE_30: D("3356.10"),
            CPP_PART_3B_LINE_31: D("0"),
            CPP_PART_3B_LINE_32: D("0"),
            CPP_PART_3B_LINE_33: D("0"),
            CPP_PART_3B_LINE_34: D("3356.10"),
            CPP_PART_3B_LINE_35: D("0"),
            CPP_PART_3B_LINE_36: D("3356.10"),
            CPP_PART_3B_LINE_37: D("678.00"),
            CPP_PART_3B_LINE_38: D("0"),
            CPP_PART_3B_LINE_39: D("0"),
            CPP_PART_3B_LINE_40: D("0"),
            CPP_PART_3B_LINE_41: D("678.00"),
            CPP_PART_3B_LINE_42: D("0"),
            CPP_PART_3B_LINE_43: D("678.00"),
            CPP_PART_3B_LINE_44: D("300"),
            CPP_PART_3B_LINE_45: D("96.00"),
            CPP_PART_3B_LINE_46: D("65.90"),
            CPP_PART_3B_LINE_47: D("365.90"),
            CPP_PART_3B_LINE_48: D("1043.90"),
            CPP_BASE_CONTRIBUTIONS_ON_RETURN: D("3356.10"),
            CPP_ENHANCED_CONTRIBUTIONS_ON_RETURN: D("1043.90"),
            CPP_OVERPAYMENT: D("0"),
        },
    )


def test_part_3a_adds_the_overpayment_to_total_credits_and_changes_nothing_else() -> None:
    # Return BN as filed against the same return with box 16 equal to line 13: lines 30800 and
    # 22215 are the required 2,796.75 and 565.00 in both, so the only difference is line 44800,
    # 138.25, which joins total credits (T1 line 166) and lowers the balance owing by as much.
    base = compute("60000", (), "0", "0", "0", "0", "0", income_tax_deducted="5000")
    over = compute(
        "60000",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
        income_tax_deducted="5000",
        cpp_t4_base_and_first_additional_contributions="3500.00",
        cpp_t4_second_additional_contributions="0",
    )

    assert base.get(CPP_OVERPAYMENT).value == D("0")
    assert over.get(CPP_OVERPAYMENT).value == D("138.25")
    assert over.get(TOTAL_CREDITS).value - base.get(TOTAL_CREDITS).value == D("138.25")
    assert base.get(REFUND_OR_BALANCE_OWING).value - over.get(REFUND_OR_BALANCE_OWING).value == D(
        "138.25"
    )
    assert (
        over.get(NON_REFUNDABLE_CREDIT_AMOUNTS).value
        == base.get(NON_REFUNDABLE_CREDIT_AMOUNTS).value
    )
    assert (
        over.get(DEDUCTIONS_FROM_TOTAL_INCOME).value == base.get(DEDUCTIONS_FROM_TOTAL_INCOME).value
    )


def test_part_3b_lines_36_and_48_feed_the_credit_and_the_deductions() -> None:
    # Box 16 of $3,300.00 against the required 3,361.75: line 30800 is line 36, 2,745.38, that is
    # 51.37 less than line 11, and line 22215 is line 48, 554.62, that is 10.38 less than line 12.
    # Each reader of line 30800 (the federal and Ontario credit amounts, ON428 line 58240) and of
    # line 22215 (the deductions and the minimum tax deductions) moves by exactly those amounts.
    base = compute("60000", (), "0", "0", "0", "0", "0")
    short = compute(
        "60000",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
        cpp_t4_base_and_first_additional_contributions="3300.00",
        cpp_t4_second_additional_contributions="0",
    )

    assert base.get(CPP_BASE_CONTRIBUTIONS_ON_RETURN).value == D("2796.75")
    assert short.get(CPP_BASE_CONTRIBUTIONS_ON_RETURN).value == D("2745.38")
    assert short.get(NON_REFUNDABLE_CREDIT_AMOUNTS).value - base.get(
        NON_REFUNDABLE_CREDIT_AMOUNTS
    ).value == D("-51.37")
    assert short.get(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS).value - base.get(
        ontario.NON_REFUNDABLE_CREDIT_AMOUNTS
    ).value == D("-51.37")
    assert base.get(CPP_ENHANCED_CONTRIBUTIONS_ON_RETURN).value == D("565.00")
    assert short.get(CPP_ENHANCED_CONTRIBUTIONS_ON_RETURN).value == D("554.62")
    assert short.get(DEDUCTIONS_FROM_TOTAL_INCOME).value - base.get(
        DEDUCTIONS_FROM_TOTAL_INCOME
    ).value == D("-10.38")
    assert short.get(AMT_DEDUCTIONS_TOTAL).value - base.get(AMT_DEDUCTIONS_TOTAL).value == D(
        "-10.38"
    )
    # The required lines 11, 12 and 22 are unchanged: only the routing differs.
    assert short.get(CPP_BASE_CONTRIBUTIONS).value == base.get(CPP_BASE_CONTRIBUTIONS).value
    assert short.get(CPP_ENHANCED_CONTRIBUTIONS).value == base.get(CPP_ENHANCED_CONTRIBUTIONS).value


def chosen_lines(worksheet: Worksheet) -> dict[ArtifactKind[Any], ChosenByCountLine]:
    return {line.output: line for line in worksheet.trace if isinstance(line, ChosenByCountLine)}


def test_the_trace_names_the_part_the_three_return_lines_were_taken_from() -> None:
    # Line 24 positive: Part 3a line 25 (line 15, the amount from line 11), line 28 and line 29.
    positive = chosen_lines(
        compute(
            "60000",
            (),
            "0",
            "0",
            "0",
            "0",
            "0",
            cpp_t4_base_and_first_additional_contributions="3500.00",
            cpp_t4_second_additional_contributions="0",
        )
    )
    assert positive[CPP_BASE_CONTRIBUTIONS_ON_RETURN] == ChosenByCountLine(
        output=CPP_BASE_CONTRIBUTIONS_ON_RETURN,
        count_kind=CPP_LINE_24_POSITIVE,
        count=1,
        chosen_kind=CPP_BASE_CONTRIBUTIONS,
        chosen_value=D("2796.75"),
    )
    assert positive[CPP_ENHANCED_CONTRIBUTIONS_ON_RETURN] == ChosenByCountLine(
        output=CPP_ENHANCED_CONTRIBUTIONS_ON_RETURN,
        count_kind=CPP_LINE_24_POSITIVE,
        count=1,
        chosen_kind=CPP_ENHANCED_CONTRIBUTIONS,
        chosen_value=D("565.00"),
    )
    assert positive[CPP_OVERPAYMENT] == ChosenByCountLine(
        output=CPP_OVERPAYMENT,
        count_kind=CPP_LINE_24_POSITIVE,
        count=1,
        chosen_kind=CPP_CONTRIBUTIONS_DIFFERENCE,
        chosen_value=D("138.25"),
    )
    # Line 24 "0" or negative: Part 3b line 36 and line 48, and "0" for the overpayment.
    zero = chosen_lines(compute("60000", (), "0", "0", "0", "0", "0"))
    assert zero[CPP_BASE_CONTRIBUTIONS_ON_RETURN] == ChosenByCountLine(
        output=CPP_BASE_CONTRIBUTIONS_ON_RETURN,
        count_kind=CPP_LINE_24_POSITIVE,
        count=0,
        chosen_kind=CPP_PART_3B_LINE_36,
        chosen_value=D("2796.75"),
    )
    assert zero[CPP_ENHANCED_CONTRIBUTIONS_ON_RETURN] == ChosenByCountLine(
        output=CPP_ENHANCED_CONTRIBUTIONS_ON_RETURN,
        count_kind=CPP_LINE_24_POSITIVE,
        count=0,
        chosen_kind=CPP_PART_3B_LINE_48,
        chosen_value=D("565.00"),
    )
    assert zero[CPP_OVERPAYMENT] == ChosenByCountLine(
        output=CPP_OVERPAYMENT,
        count_kind=CPP_LINE_24_POSITIVE,
        count=0,
        chosen_kind=CPP_ZERO,
        chosen_value=D("0"),
    )
    # Line 30 of Part 3b chooses between line 9 ("amount from line 14") and line 11, by line 16.
    short = chosen_lines(
        compute(
            "60000",
            (),
            "0",
            "0",
            "0",
            "0",
            "0",
            cpp_t4_base_and_first_additional_contributions="3300.00",
            cpp_t4_second_additional_contributions="0",
        )
    )
    assert short[CPP_PART_3B_LINE_30] == ChosenByCountLine(
        output=CPP_PART_3B_LINE_30,
        count_kind=CPP_LINE_16_NOT_NEGATIVE,
        count=0,
        chosen_kind=CPP_ACTUAL_BASE_CONTRIBUTIONS,
        chosen_value=D("2745.38"),
    )
    assert zero[CPP_PART_3B_LINE_30] == ChosenByCountLine(
        output=CPP_PART_3B_LINE_30,
        count_kind=CPP_LINE_16_NOT_NEGATIVE,
        count=1,
        chosen_kind=CPP_BASE_CONTRIBUTIONS,
        chosen_value=D("2796.75"),
    )


# Schedule 8 Part 5 lines 1 to 42 (no routing yet: lines 30 and 42 are declared outputs that the
# lines 43 to 88 of a later change will read). Every figure below is derived by hand from the form's
# lines, in order, from the employment income, the self-employment income (T1 line 23, which is
# line 27 of the return), the two T4 totals and the two CPT20 amounts. Without a T4 total given, box
# 16 and 16A are the required contributions (see `required_cpp_contributions`), so lines 20 and 23
# of Part 3 are 0. The cases: (a) the worked example, employment income 60,000 and line 27 of
# 20,000; (b) employment income above 71,300; (c) T4 contributions above and below the required
# ones, hitting lines 6, 15, 8 and 9; (d) CPT20 earnings; (e) employment income below the
# exemption, hitting lines 25 and 29; no self-employment income; and a loss.


def test_part_5_with_employment_income_of_60000_and_line_27_of_20000_prints_the_form() -> None:
    # Case (a), the worked example. Part 3 for employment income of $60,000: line 11 is 4.95%
    # x 56,500 = 2,796.75, line 12 is 1% x 56,500 = 565.00, line 13 is 3,361.75 and line 22 is
    # 0. The T4 box 16 total is the required 3,361.75, so Part 3 line 9 is 2,796.75 and line 10
    # is 565.00; lines 16, 19, 20 and 23 are 0. Part 5: line 1 is 20,000 (line 12200 of 0 plus
    # line 27 of 20,000), lines 2 and 3 are 0, line 4 is 20,000. Line 5 is 3,361.75, line 6 is 0
    # (line 20 of Part 3 is not positive) and line 7 is 3,361.75; lines 8 and 9 are 0 (line 20
    # of Part 3 is not negative) and line 10 is 3,361.75. Lines 11 to 16 are 0 (box 16A of 0,
    # line 23 of 0). Line 17 is 71,300 and line 18 is 3,500, so line 19 is 67,800. Line 20 is
    # 3,361.75 x 16.80672 = 56,499.99096, to the cent 56,499.99 (not 56,500.00), line 21 is
    # 67,800 - 56,499.99 = 11,300.01 and line 22, the lesser of line 4 (20,000) and line 21, is
    # 11,300.01. Employment income of 60,000 is not less than line 18, so line 25 is 0 and so is
    # line 29 (line 28 is 20,000 - 67,800, below zero, so 0); line 30 is 11,300.01. Line 32 is
    # the lesser of 81,200 and 60,000, 60,000, and line 33 is 80,000, more than 71,300, so lines
    # 34 to 42 are computed: line 34 is 9,900, line 35 is 0 / 4% = 0, line 36 is 9,900, line 37
    # is 20,000, line 38 is 0, line 39 is 20,000, line 40 is 11,300.01, line 41 is 8,699.99 and
    # line 42, the lesser of lines 36 and 41, is 8,699.99.
    worksheet = compute(
        "60000",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
        professional_income="20000",
    )

    assert_values(
        worksheet,
        {
            CPP_PART_5_LINE_4: D("20000"),
            CPP_PART_5_LINE_6: D("0"),
            CPP_PART_5_LINE_7: D("3361.75"),
            CPP_PART_5_LINE_8: D("0"),
            CPP_PART_5_LINE_9: D("0"),
            CPP_PART_5_LINE_10: D("3361.75"),
            CPP_PART_5_LINE_12: D("0"),
            CPP_PART_5_LINE_13: D("0"),
            CPP_PART_5_LINE_14: D("0"),
            CPP_PART_5_LINE_15: D("0"),
            CPP_PART_5_LINE_16: D("0"),
            CPP_PART_5_LINE_19: D("67800"),
            CPP_PART_5_LINE_20: D("56499.99"),
            CPP_PART_5_LINE_21: D("11300.01"),
            CPP_PART_5_LINE_22: D("11300.01"),
            CPP_PART_5_LINE_25: D("0"),
            CPP_PART_5_LINE_28: D("0"),
            CPP_PART_5_LINE_29: D("0"),
            CPP_PART_5_LINE_30: D("11300.01"),
            CPP_PART_5_LINE_33: D("80000"),
            CPP_PART_5_LINE_35: D("0"),
            CPP_PART_5_LINE_36: D("9900"),
            CPP_PART_5_LINE_39: D("20000"),
            CPP_PART_5_LINE_41: D("8699.99"),
            CPP_PART_5_LINE_42: D("8699.99"),
            CPP_PART_5_LINE_20_NEGATIVE_LINE_23_POSITIVE: 0,
            CPP_PART_5_LINE_20_POSITIVE_LINE_23_NEGATIVE: 0,
            CPP_PART_5_LINE_33_MORE_THAN_LINE_17: 1,
        },
    )


def test_part_5_lines_34_to_42_use_line_16_when_employment_income_is_above_71300() -> None:
    # Case (b). Employment income of $80,000 and line 27 of 15,000. Part 3: line 11 is 4.95% x
    # 67,800 = 3,356.10 (the maximum), line 12 is 678.00, line 13 is 4,034.10 and line 22 is 4%
    # x (80,000 - 71,300) = 348.00; the T4 totals are the required 4,034.10 and 348.00, so lines
    # 16, 19, 20 and 23 of Part 3 are 0. Part 5: line 4 is 15,000, line 7 is 4,034.10 and line
    # 10 is 4,034.10; line 11 is 348.00, line 12 is 0, line 13 is 348.00 and line 16 is 348.00.
    # Line 19 is 67,800 and line 20 is 4,034.10 x 16.80672 = 67,799.989152, to the cent
    # 67,799.99, so line 21 is 0.01 and line 22, the lesser of 15,000 and 0.01, is 0.01; lines
    # 25, 28 and 29 are 0 and line 30 is 0.01. Line 32 is 80,000 and line 33 is 95,000, more
    # than 71,300: line 34 is 9,900, line 35 is 348.00 / 4% = 8,700.00, line 36 is 1,200.00,
    # line 37 is 15,000, line 38 is 0, line 39 is 15,000, line 40 is 0.01, line 41 is 14,999.99
    # and line 42, the lesser of 1,200.00 and 14,999.99, is 1,200.00.
    worksheet = compute(
        "80000",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
        professional_income="15000",
    )

    assert_values(
        worksheet,
        {
            CPP_PART_5_LINE_4: D("15000"),
            CPP_PART_5_LINE_6: D("0"),
            CPP_PART_5_LINE_7: D("4034.1"),
            CPP_PART_5_LINE_8: D("0"),
            CPP_PART_5_LINE_9: D("0"),
            CPP_PART_5_LINE_10: D("4034.1"),
            CPP_PART_5_LINE_12: D("0"),
            CPP_PART_5_LINE_13: D("348"),
            CPP_PART_5_LINE_14: D("0"),
            CPP_PART_5_LINE_15: D("0"),
            CPP_PART_5_LINE_16: D("348"),
            CPP_PART_5_LINE_19: D("67800"),
            CPP_PART_5_LINE_20: D("67799.99"),
            CPP_PART_5_LINE_21: D("0.01"),
            CPP_PART_5_LINE_22: D("0.01"),
            CPP_PART_5_LINE_25: D("0"),
            CPP_PART_5_LINE_28: D("0"),
            CPP_PART_5_LINE_29: D("0"),
            CPP_PART_5_LINE_30: D("0.01"),
            CPP_PART_5_LINE_33: D("95000"),
            CPP_PART_5_LINE_35: D("8700"),
            CPP_PART_5_LINE_36: D("1200"),
            CPP_PART_5_LINE_39: D("15000"),
            CPP_PART_5_LINE_41: D("14999.99"),
            CPP_PART_5_LINE_42: D("1200"),
            CPP_PART_5_LINE_20_NEGATIVE_LINE_23_POSITIVE: 0,
            CPP_PART_5_LINE_20_POSITIVE_LINE_23_NEGATIVE: 0,
            CPP_PART_5_LINE_33_MORE_THAN_LINE_17: 1,
        },
    )


def test_part_5_line_6_takes_the_overpaid_line_20_of_part_3_off_line_5() -> None:
    # Case (c), contributions above the required ones: Return BN as filed, employment income of
    # $60,000 with the T4 box 16 total of 3,500.00 (138.25 more than line 13) and line 27 of
    # 20,000. Part 3: line 9 is 2,911.77, line 10 is 588.23, line 16 is 115.02, line 19 is
    # 23.23, line 20 is 138.25 and line 23 is 0. Part 5: line 5 is 3,500.00, line 6 is 138.25
    # (line 20 of Part 3, positive) and line 7 is 3,500.00 - 138.25 = 3,361.75, so line 10 is
    # 3,361.75 as in case (a) (line 20 of Part 3 is not negative, so lines 8 and 9 are 0) and
    # lines 19 to 42 are the same as in case (a).
    worksheet = compute(
        "60000",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
        professional_income="20000",
        cpp_t4_base_and_first_additional_contributions="3500.00",
    )

    assert_values(
        worksheet,
        {
            CPP_PART_5_LINE_4: D("20000"),
            CPP_PART_5_LINE_6: D("138.25"),
            CPP_PART_5_LINE_7: D("3361.75"),
            CPP_PART_5_LINE_8: D("0"),
            CPP_PART_5_LINE_9: D("0"),
            CPP_PART_5_LINE_10: D("3361.75"),
            CPP_PART_5_LINE_12: D("0"),
            CPP_PART_5_LINE_13: D("0"),
            CPP_PART_5_LINE_14: D("0"),
            CPP_PART_5_LINE_15: D("0"),
            CPP_PART_5_LINE_16: D("0"),
            CPP_PART_5_LINE_19: D("67800"),
            CPP_PART_5_LINE_20: D("56499.99"),
            CPP_PART_5_LINE_21: D("11300.01"),
            CPP_PART_5_LINE_22: D("11300.01"),
            CPP_PART_5_LINE_25: D("0"),
            CPP_PART_5_LINE_28: D("0"),
            CPP_PART_5_LINE_29: D("0"),
            CPP_PART_5_LINE_30: D("11300.01"),
            CPP_PART_5_LINE_33: D("80000"),
            CPP_PART_5_LINE_35: D("0"),
            CPP_PART_5_LINE_36: D("9900"),
            CPP_PART_5_LINE_39: D("20000"),
            CPP_PART_5_LINE_41: D("8699.99"),
            CPP_PART_5_LINE_42: D("8699.99"),
            CPP_PART_5_LINE_20_NEGATIVE_LINE_23_POSITIVE: 0,
            CPP_PART_5_LINE_20_POSITIVE_LINE_23_NEGATIVE: 0,
            CPP_PART_5_LINE_33_MORE_THAN_LINE_17: 1,
        },
    )


def test_part_5_line_15_is_the_lesser_of_line_20_of_part_3_and_line_14() -> None:
    # Case (c), line 20 of Part 3 positive and line 23 negative. Employment income of $80,000
    # and line 27 of 15,000, with box 16 of 4,100.00 and box 16A of 300.00 (required 4,034.10
    # and 348.00). Part 3: line 9 is 3,410.9253, to the cent 3,410.93, line 10 is 689.07, line
    # 16 is 3,410.93 - 3,356.10 = 54.83, line 19 is 689.07 - 678.00 = 11.07, line 20 is 65.90
    # and line 23 is 300.00 - 348.00 = -48.00. Part 5: line 6 is 65.90 and line 7 is 4,100.00 -
    # 65.90 = 4,034.10; line 8 is 0 (line 20 is not negative), line 9 is 0 and line 10 is
    # 4,034.10. Line 11 is 300.00, line 12 is 0 (line 23 is negative) and line 13 is 300.00;
    # line 14 is 48.00 and line 15, the lesser of line 20 of Part 3 (65.90) and line 14 (48.00),
    # is 48.00; line 16 is 300.00 + 48.00 = 348.00. Lines 17 to 42 are those of case (b).
    worksheet = compute(
        "80000",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
        professional_income="15000",
        cpp_t4_base_and_first_additional_contributions="4100.00",
        cpp_t4_second_additional_contributions="300.00",
    )

    assert_values(
        worksheet,
        {
            CPP_PART_5_LINE_4: D("15000"),
            CPP_PART_5_LINE_6: D("65.90"),
            CPP_PART_5_LINE_7: D("4034.10"),
            CPP_PART_5_LINE_8: D("0"),
            CPP_PART_5_LINE_9: D("0"),
            CPP_PART_5_LINE_10: D("4034.10"),
            CPP_PART_5_LINE_12: D("0"),
            CPP_PART_5_LINE_13: D("300.00"),
            CPP_PART_5_LINE_14: D("48.00"),
            CPP_PART_5_LINE_15: D("48.00"),
            CPP_PART_5_LINE_16: D("348.00"),
            CPP_PART_5_LINE_19: D("67800"),
            CPP_PART_5_LINE_20: D("67799.99"),
            CPP_PART_5_LINE_21: D("0.01"),
            CPP_PART_5_LINE_22: D("0.01"),
            CPP_PART_5_LINE_25: D("0"),
            CPP_PART_5_LINE_28: D("0"),
            CPP_PART_5_LINE_29: D("0"),
            CPP_PART_5_LINE_30: D("0.01"),
            CPP_PART_5_LINE_33: D("95000"),
            CPP_PART_5_LINE_35: D("8700"),
            CPP_PART_5_LINE_36: D("1200"),
            CPP_PART_5_LINE_39: D("15000"),
            CPP_PART_5_LINE_41: D("14999.99"),
            CPP_PART_5_LINE_42: D("1200"),
            CPP_PART_5_LINE_20_NEGATIVE_LINE_23_POSITIVE: 0,
            CPP_PART_5_LINE_20_POSITIVE_LINE_23_NEGATIVE: 1,
            CPP_PART_5_LINE_33_MORE_THAN_LINE_17: 1,
        },
    )


def test_part_5_line_9_is_the_lesser_of_line_23_of_part_3_and_line_8() -> None:
    # Case (c), line 20 of Part 3 negative and line 23 positive. Employment income of $80,000
    # and line 27 of 15,000, with box 16 of 4,000.00 and box 16A of 400.00. Part 3: line 9 is
    # 3,327.732, to the cent 3,327.73, line 10 is 672.27, line 16 is 3,327.73 - 3,356.10 =
    # -28.37, line 19 is 672.27 - 678.00 = -5.73, line 20 is -34.10 and line 23 is 400.00 -
    # 348.00 = 52.00. Part 5: line 6 is 0 (line 20 is negative) and line 7 is 4,000.00; line 8
    # is 34.10 and line 9, the lesser of line 23 of Part 3 (52.00) and line 8 (34.10), is 34.10;
    # line 10 is 4,034.10. Line 11 is 400.00, line 12 is 52.00 and line 13 is 348.00; line 14
    # and line 15 are 0 (line 20 is not positive) and line 16 is 348.00. Lines 17 to 42 are
    # those of case (b).
    worksheet = compute(
        "80000",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
        professional_income="15000",
        cpp_t4_base_and_first_additional_contributions="4000.00",
        cpp_t4_second_additional_contributions="400.00",
    )

    assert_values(
        worksheet,
        {
            CPP_PART_5_LINE_4: D("15000"),
            CPP_PART_5_LINE_6: D("0"),
            CPP_PART_5_LINE_7: D("4000.00"),
            CPP_PART_5_LINE_8: D("34.10"),
            CPP_PART_5_LINE_9: D("34.10"),
            CPP_PART_5_LINE_10: D("4034.10"),
            CPP_PART_5_LINE_12: D("52.00"),
            CPP_PART_5_LINE_13: D("348.00"),
            CPP_PART_5_LINE_14: D("0"),
            CPP_PART_5_LINE_15: D("0"),
            CPP_PART_5_LINE_16: D("348.00"),
            CPP_PART_5_LINE_19: D("67800"),
            CPP_PART_5_LINE_20: D("67799.99"),
            CPP_PART_5_LINE_21: D("0.01"),
            CPP_PART_5_LINE_22: D("0.01"),
            CPP_PART_5_LINE_25: D("0"),
            CPP_PART_5_LINE_28: D("0"),
            CPP_PART_5_LINE_29: D("0"),
            CPP_PART_5_LINE_30: D("0.01"),
            CPP_PART_5_LINE_33: D("95000"),
            CPP_PART_5_LINE_35: D("8700"),
            CPP_PART_5_LINE_36: D("1200"),
            CPP_PART_5_LINE_39: D("15000"),
            CPP_PART_5_LINE_41: D("14999.99"),
            CPP_PART_5_LINE_42: D("1200"),
            CPP_PART_5_LINE_20_NEGATIVE_LINE_23_POSITIVE: 1,
            CPP_PART_5_LINE_20_POSITIVE_LINE_23_NEGATIVE: 0,
            CPP_PART_5_LINE_33_MORE_THAN_LINE_17: 1,
        },
    )


def test_part_5_line_3_adds_the_cpt20_earnings_shown_on_a_t4_slip() -> None:
    # Case (d). Employment income of $60,000, line 27 of 20,000, CPT20 earnings not on a T4 slip
    # (line 2) of 3,000 and on a T4 slip (line 3) of 5,000, with box 16 the required 3,361.75.
    # Part 3 and lines 5 to 21 are those of case (a). Line 4 is 20,000 + 3,000 + 5,000 = 28,000,
    # so line 22 is the lesser of 28,000 and 11,300.01, 11,300.01, and line 30 is 11,300.01.
    # Line 33 is 28,000 + 60,000 = 88,000: line 36 is 9,900, line 39 is 28,000, line 41 is
    # 28,000 - 11,300.01 = 16,699.99 and line 42, the lesser of 9,900 and 16,699.99, is 9,900.
    worksheet = compute(
        "60000",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
        professional_income="20000",
        cpt20_earnings="3000",
        cpt20_t4_earnings="5000",
    )

    assert_values(
        worksheet,
        {
            CPP_PART_5_LINE_4: D("28000"),
            CPP_PART_5_LINE_6: D("0"),
            CPP_PART_5_LINE_7: D("3361.75"),
            CPP_PART_5_LINE_8: D("0"),
            CPP_PART_5_LINE_9: D("0"),
            CPP_PART_5_LINE_10: D("3361.75"),
            CPP_PART_5_LINE_12: D("0"),
            CPP_PART_5_LINE_13: D("0"),
            CPP_PART_5_LINE_14: D("0"),
            CPP_PART_5_LINE_15: D("0"),
            CPP_PART_5_LINE_16: D("0"),
            CPP_PART_5_LINE_19: D("67800"),
            CPP_PART_5_LINE_20: D("56499.99"),
            CPP_PART_5_LINE_21: D("11300.01"),
            CPP_PART_5_LINE_22: D("11300.01"),
            CPP_PART_5_LINE_25: D("0"),
            CPP_PART_5_LINE_28: D("0"),
            CPP_PART_5_LINE_29: D("0"),
            CPP_PART_5_LINE_30: D("11300.01"),
            CPP_PART_5_LINE_33: D("88000"),
            CPP_PART_5_LINE_35: D("0"),
            CPP_PART_5_LINE_36: D("9900"),
            CPP_PART_5_LINE_39: D("28000"),
            CPP_PART_5_LINE_41: D("16699.99"),
            CPP_PART_5_LINE_42: D("9900"),
            CPP_PART_5_LINE_20_NEGATIVE_LINE_23_POSITIVE: 0,
            CPP_PART_5_LINE_20_POSITIVE_LINE_23_NEGATIVE: 0,
            CPP_PART_5_LINE_33_MORE_THAN_LINE_17: 1,
        },
    )


def test_part_5_lines_25_and_29_when_employment_income_is_below_the_exemption() -> None:
    # Case (e). Employment income of $2,000, below the 3,500 of line 18, and line 27 of 40,000;
    # no T4 contributions are required (Part 3 lines 7 to 24 are 0). Part 5: line 4 is 40,000,
    # lines 5 to 18 are 0 or the limits (line 19 is 67,800) and line 20 is 0, so line 21 is
    # 67,800 and line 22 is 40,000. Line 24 (employment income) is 2,000, less than line 23
    # (3,500): line 25 is 1,500. Line 28 is 40,000 - 67,800, below zero, so 0, and line 29 is
    # 1,500 - 0 = 1,500; line 30 is 40,000 - 1,500 = 38,500. Line 32 is 2,000 and line 33 is
    # 42,000, not more than 71,300, so line 42 is 0 (lines 34 to 41 are still computed: line 36
    # is 9,900, line 39 is 40,000 - 1,500 = 38,500 and line 41 is 38,500 - 38,500 = 0).
    worksheet = compute(
        "2000",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
        professional_income="40000",
    )

    assert_values(
        worksheet,
        {
            CPP_PART_5_LINE_4: D("40000"),
            CPP_PART_5_LINE_6: D("0"),
            CPP_PART_5_LINE_7: D("0"),
            CPP_PART_5_LINE_8: D("0"),
            CPP_PART_5_LINE_9: D("0"),
            CPP_PART_5_LINE_10: D("0"),
            CPP_PART_5_LINE_12: D("0"),
            CPP_PART_5_LINE_13: D("0"),
            CPP_PART_5_LINE_14: D("0"),
            CPP_PART_5_LINE_15: D("0"),
            CPP_PART_5_LINE_16: D("0"),
            CPP_PART_5_LINE_19: D("67800"),
            CPP_PART_5_LINE_20: D("0"),
            CPP_PART_5_LINE_21: D("67800"),
            CPP_PART_5_LINE_22: D("40000"),
            CPP_PART_5_LINE_25: D("1500"),
            CPP_PART_5_LINE_28: D("0"),
            CPP_PART_5_LINE_29: D("1500"),
            CPP_PART_5_LINE_30: D("38500"),
            CPP_PART_5_LINE_33: D("42000"),
            CPP_PART_5_LINE_35: D("0"),
            CPP_PART_5_LINE_36: D("9900"),
            CPP_PART_5_LINE_39: D("38500"),
            CPP_PART_5_LINE_41: D("0"),
            CPP_PART_5_LINE_42: D("0"),
            CPP_PART_5_LINE_20_NEGATIVE_LINE_23_POSITIVE: 0,
            CPP_PART_5_LINE_20_POSITIVE_LINE_23_NEGATIVE: 0,
            CPP_PART_5_LINE_33_MORE_THAN_LINE_17: 0,
        },
    )


def test_part_5_line_28_takes_what_line_4_has_over_line_19_off_line_29() -> None:
    # Case (e), with line 27 of 68,800. Employment income of $2,000, so line 25 is 1,500. Line 4
    # is 68,800, line 21 is 67,800 and line 22, the lesser of the two, is 67,800. Line 28 is
    # 68,800 - 67,800 = 1,000, so line 29 is 1,500 - 1,000 = 500 and line 30 is 67,800 - 500 =
    # 67,300. Line 33 is 68,800 + 2,000 = 70,800, not more than 71,300, so line 42 is 0 (line 39
    # is 68,800 - 1,500 = 67,300 and line 41 is 67,300 - 67,300 = 0).
    worksheet = compute(
        "2000",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
        professional_income="68800",
    )

    assert_values(
        worksheet,
        {
            CPP_PART_5_LINE_4: D("68800"),
            CPP_PART_5_LINE_6: D("0"),
            CPP_PART_5_LINE_7: D("0"),
            CPP_PART_5_LINE_8: D("0"),
            CPP_PART_5_LINE_9: D("0"),
            CPP_PART_5_LINE_10: D("0"),
            CPP_PART_5_LINE_12: D("0"),
            CPP_PART_5_LINE_13: D("0"),
            CPP_PART_5_LINE_14: D("0"),
            CPP_PART_5_LINE_15: D("0"),
            CPP_PART_5_LINE_16: D("0"),
            CPP_PART_5_LINE_19: D("67800"),
            CPP_PART_5_LINE_20: D("0"),
            CPP_PART_5_LINE_21: D("67800"),
            CPP_PART_5_LINE_22: D("67800"),
            CPP_PART_5_LINE_25: D("1500"),
            CPP_PART_5_LINE_28: D("1000"),
            CPP_PART_5_LINE_29: D("500"),
            CPP_PART_5_LINE_30: D("67300"),
            CPP_PART_5_LINE_33: D("70800"),
            CPP_PART_5_LINE_35: D("0"),
            CPP_PART_5_LINE_36: D("9900"),
            CPP_PART_5_LINE_39: D("67300"),
            CPP_PART_5_LINE_41: D("0"),
            CPP_PART_5_LINE_42: D("0"),
            CPP_PART_5_LINE_20_NEGATIVE_LINE_23_POSITIVE: 0,
            CPP_PART_5_LINE_20_POSITIVE_LINE_23_NEGATIVE: 0,
            CPP_PART_5_LINE_33_MORE_THAN_LINE_17: 0,
        },
    )


def test_part_5_without_self_employment_income_only_the_part_3_lines_are_not_zero() -> None:
    # No self-employment income and no CPT20 earnings: employment income of $60,000 with box 16
    # the required 3,361.75. Lines 1 to 4, 22, 30, 39, 41 and 42 are 0; lines 7 and 10 are the
    # T4 box 16 total, 3,361.75 (lines 5 and 20 of Part 3 are not positive, so lines 6 and 8 are
    # 0), lines 19, 20 and 21 are 67,800, 56,499.99 and 11,300.01 as in case (a), and line 36 is
    # 9,900; line 33 is the 60,000 of Part 3 line 2, not more than 71,300.
    worksheet = compute(
        "60000",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
    )

    assert_values(
        worksheet,
        {
            CPP_PART_5_LINE_4: D("0"),
            CPP_PART_5_LINE_6: D("0"),
            CPP_PART_5_LINE_7: D("3361.75"),
            CPP_PART_5_LINE_8: D("0"),
            CPP_PART_5_LINE_9: D("0"),
            CPP_PART_5_LINE_10: D("3361.75"),
            CPP_PART_5_LINE_12: D("0"),
            CPP_PART_5_LINE_13: D("0"),
            CPP_PART_5_LINE_14: D("0"),
            CPP_PART_5_LINE_15: D("0"),
            CPP_PART_5_LINE_16: D("0"),
            CPP_PART_5_LINE_19: D("67800"),
            CPP_PART_5_LINE_20: D("56499.99"),
            CPP_PART_5_LINE_21: D("11300.01"),
            CPP_PART_5_LINE_22: D("0"),
            CPP_PART_5_LINE_25: D("0"),
            CPP_PART_5_LINE_28: D("0"),
            CPP_PART_5_LINE_29: D("0"),
            CPP_PART_5_LINE_30: D("0"),
            CPP_PART_5_LINE_33: D("60000"),
            CPP_PART_5_LINE_35: D("0"),
            CPP_PART_5_LINE_36: D("9900"),
            CPP_PART_5_LINE_39: D("0"),
            CPP_PART_5_LINE_41: D("0"),
            CPP_PART_5_LINE_42: D("0"),
            CPP_PART_5_LINE_20_NEGATIVE_LINE_23_POSITIVE: 0,
            CPP_PART_5_LINE_20_POSITIVE_LINE_23_NEGATIVE: 0,
            CPP_PART_5_LINE_33_MORE_THAN_LINE_17: 0,
        },
    )


def test_part_5_without_self_employment_income_lines_13_16_and_35_come_from_box_16a() -> None:
    # No self-employment income and employment income of $80,000: box 16A is the required
    # 348.00, so line 13 and line 16 are 348.00 and line 35 is 348.00 / 4% = 8,700.00, line 36
    # is 1,200.00. Line 33 is 80,000, more than 71,300, so line 42 is the lesser of 1,200.00 and
    # line 41 (0 - 0 = 0), 0. Line 20 is 4,034.10 x 16.80672 = 67,799.99 and line 21 is 0.01.
    worksheet = compute(
        "80000",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
    )

    assert_values(
        worksheet,
        {
            CPP_PART_5_LINE_4: D("0"),
            CPP_PART_5_LINE_6: D("0"),
            CPP_PART_5_LINE_7: D("4034.1"),
            CPP_PART_5_LINE_8: D("0"),
            CPP_PART_5_LINE_9: D("0"),
            CPP_PART_5_LINE_10: D("4034.1"),
            CPP_PART_5_LINE_12: D("0"),
            CPP_PART_5_LINE_13: D("348"),
            CPP_PART_5_LINE_14: D("0"),
            CPP_PART_5_LINE_15: D("0"),
            CPP_PART_5_LINE_16: D("348"),
            CPP_PART_5_LINE_19: D("67800"),
            CPP_PART_5_LINE_20: D("67799.99"),
            CPP_PART_5_LINE_21: D("0.01"),
            CPP_PART_5_LINE_22: D("0"),
            CPP_PART_5_LINE_25: D("0"),
            CPP_PART_5_LINE_28: D("0"),
            CPP_PART_5_LINE_29: D("0"),
            CPP_PART_5_LINE_30: D("0"),
            CPP_PART_5_LINE_33: D("80000"),
            CPP_PART_5_LINE_35: D("8700"),
            CPP_PART_5_LINE_36: D("1200"),
            CPP_PART_5_LINE_39: D("0"),
            CPP_PART_5_LINE_41: D("0"),
            CPP_PART_5_LINE_42: D("0"),
            CPP_PART_5_LINE_20_NEGATIVE_LINE_23_POSITIVE: 0,
            CPP_PART_5_LINE_20_POSITIVE_LINE_23_NEGATIVE: 0,
            CPP_PART_5_LINE_33_MORE_THAN_LINE_17: 1,
        },
    )


def test_part_5_line_42_is_negative_when_line_4_is_a_loss_and_line_33_is_above_71300() -> None:
    # A loss: employment income of $80,000 and line 27 of -5,000 (professional income). Line 4
    # prints no floor, so it is -5,000, line 22 is the lesser of -5,000 and 0.01, -5,000, and
    # lines 25, 28, 29 and 30 are 0 (line 30 is -5,000 - 0, below zero, so 0). Line 33 is -5,000
    # + 80,000 = 75,000, more than 71,300: line 36 is 9,900 - 8,700.00 = 1,200.00, line 39 is
    # -5,000, line 40 is 0, line 41 is -5,000 and line 42, the lesser of 1,200.00 and -5,000, is
    # -5,000: the form prints no floor on lines 36 to 42, so line 42 is signed (a later change
    # decides what lines 45 and 46 do with it).
    worksheet = compute(
        "80000",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
        professional_income="-5000",
    )

    assert_values(
        worksheet,
        {
            CPP_PART_5_LINE_4: D("-5000"),
            CPP_PART_5_LINE_6: D("0"),
            CPP_PART_5_LINE_7: D("4034.1"),
            CPP_PART_5_LINE_8: D("0"),
            CPP_PART_5_LINE_9: D("0"),
            CPP_PART_5_LINE_10: D("4034.1"),
            CPP_PART_5_LINE_12: D("0"),
            CPP_PART_5_LINE_13: D("348"),
            CPP_PART_5_LINE_14: D("0"),
            CPP_PART_5_LINE_15: D("0"),
            CPP_PART_5_LINE_16: D("348"),
            CPP_PART_5_LINE_19: D("67800"),
            CPP_PART_5_LINE_20: D("67799.99"),
            CPP_PART_5_LINE_21: D("0.01"),
            CPP_PART_5_LINE_22: D("-5000"),
            CPP_PART_5_LINE_25: D("0"),
            CPP_PART_5_LINE_28: D("0"),
            CPP_PART_5_LINE_29: D("0"),
            CPP_PART_5_LINE_30: D("0"),
            CPP_PART_5_LINE_33: D("75000"),
            CPP_PART_5_LINE_35: D("8700"),
            CPP_PART_5_LINE_36: D("1200"),
            CPP_PART_5_LINE_39: D("-5000"),
            CPP_PART_5_LINE_41: D("-5000"),
            CPP_PART_5_LINE_42: D("-5000"),
            CPP_PART_5_LINE_20_NEGATIVE_LINE_23_POSITIVE: 0,
            CPP_PART_5_LINE_20_POSITIVE_LINE_23_NEGATIVE: 0,
            CPP_PART_5_LINE_33_MORE_THAN_LINE_17: 1,
        },
    )


def test_part_5_changes_no_other_line_of_the_return() -> None:
    # The Part 5 lines are only declared outputs: the CPT20 earnings shown on a T4 slip (line 3)
    # feed Part 5 alone, so the deductions, the credits and the balance owing do not move.
    without = compute("60000", (), "0", "0", "0", "0", "0", professional_income="20000")
    with_cpt20 = compute(
        "60000",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
        professional_income="20000",
        cpt20_t4_earnings="5000",
    )

    assert with_cpt20.get(CPP_PART_5_LINE_4).value == D("25000")
    assert without.get(CPP_PART_5_LINE_4).value == D("20000")
    for kind in (DEDUCTIONS_FROM_TOTAL_INCOME, TOTAL_CREDITS, REFUND_OR_BALANCE_OWING):
        assert with_cpt20.get(kind).value == without.get(kind).value, kind.identifier


def part_5_trace(worksheet: Worksheet, line_type: type) -> dict[ArtifactKind[Any], Any]:
    lines: list[Any] = [line for line in worksheet.trace if isinstance(line, line_type)]
    return {line.output: line for line in lines}


def test_the_trace_records_line_20_as_a_fraction_and_line_35_as_a_division() -> None:
    # Case (a): line 20 is line 10 of 3,361.75 times 16.80672 (a fraction, 1,680,672 / 100,000, to
    # the cent: 56,499.99096 is 56,499.99).
    case_a = compute("60000", (), "0", "0", "0", "0", "0", professional_income="20000")
    assert part_5_trace(case_a, FractionAppliedLine)[CPP_PART_5_LINE_20] == FractionAppliedLine(
        output=CPP_PART_5_LINE_20,
        base=CPP_PART_5_LINE_10,
        base_amount=D("3361.75"),
        fraction=Fraction(1680672, 100000),
        rounding=CENT,
        result=D("56499.99"),
    )
    # Case (b): line 35 is line 16 of 348.00 divided by 4%, 8,700.00.
    case_b = compute("80000", (), "0", "0", "0", "0", "0", professional_income="15000")
    assert part_5_trace(case_b, DividedByRateLine)[CPP_PART_5_LINE_35] == DividedByRateLine(
        output=CPP_PART_5_LINE_35,
        dividend=CPP_PART_5_LINE_16,
        dividend_amount=D("348.00"),
        rate=Rate(D("0.04")),
        rounding=CENT,
        result=D("8700.00"),
    )


def test_the_trace_names_the_candidate_lines_9_15_and_42_took_or_the_zero() -> None:
    # Line 9 takes its lesser (34.10) when line 20 of Part 3 is negative and line 23 positive.
    case_c3 = compute(
        "80000",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
        professional_income="15000",
        cpp_t4_base_and_first_additional_contributions="4000.00",
        cpp_t4_second_additional_contributions="400.00",
    )
    chosen = part_5_trace(case_c3, ChosenByCountLine)
    assert chosen[CPP_PART_5_LINE_9] == ChosenByCountLine(
        output=CPP_PART_5_LINE_9,
        count_kind=CPP_PART_5_LINE_20_NEGATIVE_LINE_23_POSITIVE,
        count=1,
        chosen_kind=CPP_PART_5_LINE_9_LESSER,
        chosen_value=D("34.10"),
    )
    assert chosen[CPP_PART_5_LINE_15] == ChosenByCountLine(
        output=CPP_PART_5_LINE_15,
        count_kind=CPP_PART_5_LINE_20_POSITIVE_LINE_23_NEGATIVE,
        count=0,
        chosen_kind=CPP_ZERO,
        chosen_value=D("0"),
    )
    # Line 15 takes its lesser (48.00) when line 20 of Part 3 is positive and line 23 negative.
    case_c2 = compute(
        "80000",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
        professional_income="15000",
        cpp_t4_base_and_first_additional_contributions="4100.00",
        cpp_t4_second_additional_contributions="300.00",
    )
    chosen = part_5_trace(case_c2, ChosenByCountLine)
    assert chosen[CPP_PART_5_LINE_15] == ChosenByCountLine(
        output=CPP_PART_5_LINE_15,
        count_kind=CPP_PART_5_LINE_20_POSITIVE_LINE_23_NEGATIVE,
        count=1,
        chosen_kind=CPP_PART_5_LINE_15_LESSER,
        chosen_value=D("48.00"),
    )
    # Line 42 takes its lesser (8,699.99) when line 33 is more than line 17, else "0".
    case_a = compute("60000", (), "0", "0", "0", "0", "0", professional_income="20000")
    assert part_5_trace(case_a, ChosenByCountLine)[CPP_PART_5_LINE_42] == ChosenByCountLine(
        output=CPP_PART_5_LINE_42,
        count_kind=CPP_PART_5_LINE_33_MORE_THAN_LINE_17,
        count=1,
        chosen_kind=CPP_PART_5_LINE_42_LESSER,
        chosen_value=D("8699.99"),
    )
    below = compute("2000", (), "0", "0", "0", "0", "0", professional_income="40000")
    assert part_5_trace(below, ChosenByCountLine)[CPP_PART_5_LINE_42] == ChosenByCountLine(
        output=CPP_PART_5_LINE_42,
        count_kind=CPP_PART_5_LINE_33_MORE_THAN_LINE_17,
        count=0,
        chosen_kind=CPP_ZERO,
        chosen_value=D("0"),
    )
