"""CA-ON 2025 end to end: return bn."""

from __future__ import annotations

from collections.abc import Mapping
from decimal import Decimal
from typing import Any

from app.domain.artifact import ArtifactKind
from app.domain.trace import ChosenByCountLine
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
