"""CA-ON 2025 end to end: return bn."""

from __future__ import annotations

from app.jurisdictions.ca.catalog import (
    CPP_ACTUAL_BASE_CONTRIBUTIONS,
    CPP_ACTUAL_FIRST_ADDITIONAL_CONTRIBUTIONS,
    CPP_BASE_AND_FIRST_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE,
    CPP_BASE_CONTRIBUTIONS,
    CPP_BASE_CONTRIBUTIONS_DIFFERENCE,
    CPP_CONTRIBUTIONS_DIFFERENCE,
    CPP_FIRST_ADDITIONAL_CONTRIBUTIONS,
    CPP_FIRST_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE,
    CPP_REQUIRED_BASE_AND_FIRST_ADDITIONAL_CONTRIBUTIONS,
    CPP_SECOND_ADDITIONAL_CONTRIBUTIONS,
    CPP_SECOND_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE,
    CPP_T4_BASE_AND_FIRST_ADDITIONAL_CONTRIBUTIONS,
    CPP_T4_SECOND_ADDITIONAL_CONTRIBUTIONS,
)
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
