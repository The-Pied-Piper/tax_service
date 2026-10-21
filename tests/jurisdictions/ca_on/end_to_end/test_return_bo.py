"""CA-ON 2025 end to end: return bo (Form RC381 Part 2 and Part 3 lines 1 to 26)."""

from __future__ import annotations

from typing import Any

import pytest

from app.domain.artifact import ArtifactKind
from app.domain.capabilities.amount_by_count import AmountForCount
from app.domain.capabilities.apply_rate import ApplyRate
from app.domain.capabilities.contribution_tier import TieredContribution
from app.domain.capabilities.lesser_of import LesserOf
from app.domain.capabilities.subtract import Subtract
from app.domain.capabilities.subtract_not_below_zero import SubtractNotBelowZero
from app.domain.capabilities.sum import Sum
from app.domain.errors import InputBelowBoundError, NoAmountForCountError
from app.domain.parameters.rate import Rate
from app.domain.worksheet import Worksheet
from app.jurisdictions.ca.capabilities.amount_when_more import AmountWhenMore
from app.jurisdictions.ca.capabilities.count_at_least import CountAtLeast
from app.jurisdictions.ca.capabilities.ratio_truncated import RatioTruncated
from app.jurisdictions.ca.catalog import (
    CPP_ADDITIONAL_MAXIMUM_PENSIONABLE_EARNINGS,
    CPP_BASE_CONTRIBUTIONS,
    CPP_BASIC_EXEMPTION,
    CPP_ENHANCED_CONTRIBUTIONS,
    CPP_MAXIMUM_PENSIONABLE_EARNINGS,
    CPP_SECOND_ADDITIONAL_EARNINGS_MAXIMUM,
    NET_INCOME,
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
    TOTAL_PAYABLE,
)
from tests.jurisdictions.ca_on.end_to_end.support import D, compute


def return_bo(
    line_1: str = "30000",
    line_2: str = "40000",
    line_19: str = "1800.00",
    *,
    cpp_months: int = 12,
    qpp_months: int = 12,
) -> Worksheet:
    """Return BO's inputs (`returns/2025_return_bo.yaml`): employment income of 70000 on a T4 for
    Ontario employment (box 26 `line_1`) and a T4 for Quebec employment (box 26 `line_2`)."""
    return compute(
        "70000",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
        cpp_months=cpp_months,
        qpp_months=qpp_months,
        t4_cpp_pensionable_earnings_outside_quebec=line_1,
        t4_qpp_pensionable_earnings_in_quebec=line_2,
        t4_cpp_contributions_box_16=line_19,
        income_tax_deducted="12000",
    )


# Part 2.


def test_return_bo_line_b_is_the_qpp_months_when_line_a_is_not_more() -> None:
    # Lines A and B are both 12 (chosen figures): "The number you enter on line A cannot be more
    # than the number you enter on line B." is met, and line B is passed on as entered.
    worksheet = return_bo()

    assert worksheet.get(RC381_PART_2_LINE_B).value == 12
    assert isinstance(worksheet.producer_of(RC381_PART_2_LINE_B), CountAtLeast)


def test_return_bo_line_b_may_be_more_than_line_a() -> None:
    # Line A is 6 and line B is 12 (the months differ when, for example, a CPP election to stop
    # contributing applies): line B is 12.
    worksheet = return_bo(cpp_months=6, qpp_months=12)

    assert worksheet.get(RC381_PART_2_LINE_B).value == 12


def test_return_bo_lines_g_to_j_are_the_row_of_the_table_for_12_months() -> None:
    # Line B is 12, the table's row "12": 71,300.00, 9,900.00, 81,200.00 and 3,500.00.
    worksheet = return_bo()

    assert worksheet.get(RC381_PART_2_LINE_G).value == D("71300.00")
    assert worksheet.get(RC381_PART_2_LINE_H).value == D("9900.00")
    assert worksheet.get(RC381_PART_2_LINE_I).value == D("81200.00")
    assert worksheet.get(RC381_PART_2_LINE_J).value == D("3500.00")
    for kind in (
        RC381_PART_2_LINE_G,
        RC381_PART_2_LINE_H,
        RC381_PART_2_LINE_I,
        RC381_PART_2_LINE_J,
    ):
        assert isinstance(worksheet.producer_of(kind), AmountForCount)


def test_return_bo_lines_g_to_j_read_line_b_and_lines_c_to_f_read_line_a() -> None:
    # Line A is 6: lines C to F are the row "6" (35,650.00, 4,950.00, 40,600.00 and 1,750.00),
    # the existing Schedule 8 lines. Line B is 12: lines G to J are the row "12".
    worksheet = return_bo(cpp_months=6, qpp_months=12)

    assert worksheet.get(CPP_MAXIMUM_PENSIONABLE_EARNINGS).value == D("35650.00")
    assert worksheet.get(CPP_SECOND_ADDITIONAL_EARNINGS_MAXIMUM).value == D("4950.00")
    assert worksheet.get(CPP_ADDITIONAL_MAXIMUM_PENSIONABLE_EARNINGS).value == D("40600.00")
    assert worksheet.get(CPP_BASIC_EXEMPTION).value == D("1750.00")
    assert worksheet.get(RC381_PART_2_LINE_G).value == D("71300.00")
    assert worksheet.get(RC381_PART_2_LINE_H).value == D("9900.00")
    assert worksheet.get(RC381_PART_2_LINE_I).value == D("81200.00")
    assert worksheet.get(RC381_PART_2_LINE_J).value == D("3500.00")


def test_return_bo_lines_g_to_j_for_6_months_when_both_months_are_6() -> None:
    # Lines A and B are 6 (equal is allowed): lines G to J are the row "6".
    worksheet = return_bo(cpp_months=6, qpp_months=6)

    assert worksheet.get(RC381_PART_2_LINE_G).value == D("35650.00")
    assert worksheet.get(RC381_PART_2_LINE_H).value == D("4950.00")
    assert worksheet.get(RC381_PART_2_LINE_I).value == D("40600.00")
    assert worksheet.get(RC381_PART_2_LINE_J).value == D("1750.00")


def test_return_bo_line_a_more_than_line_b_is_an_input_error() -> None:
    # "The number you enter on line A cannot be more than the number you enter on line B.": 12
    # months of CPP against 11 of QPP is refused, not corrected.
    with pytest.raises(InputBelowBoundError, match="qpp_months"):
        return_bo(cpp_months=12, qpp_months=11)


def test_return_bo_a_blank_line_b_is_an_input_error_when_line_a_is_filled() -> None:
    # A line B of 0 (left blank) is below line A's 12.
    with pytest.raises(InputBelowBoundError):
        return_bo(cpp_months=12, qpp_months=0)


def test_return_bo_a_line_b_without_a_row_in_the_table_is_refused() -> None:
    # The table has rows for 1 to 12 months: 13 is not below line A, but has no row.
    with pytest.raises(NoAmountForCountError):
        return_bo(cpp_months=12, qpp_months=13)


# Part 3, the ticket's example.


def test_return_bo_line_3_adds_lines_1_and_2() -> None:
    # Line 1 (50339) 30,000 plus line 2 (50329) 40,000 is 70,000.00.
    worksheet = return_bo()

    assert worksheet.get(RC381_PART_3_LINE_3).value == D("70000.00")
    assert isinstance(worksheet.producer_of(RC381_PART_3_LINE_3), Sum)


def test_return_bo_line_6_is_line_4_over_line_5_cut_at_the_fifth_decimal_place() -> None:
    # 30,000 / 70,000 = 0.4285714..., calculated to the fifth decimal place without rounding:
    # 0.42857 (rounding would give the same here, so see the next test for a tie that goes down).
    worksheet = return_bo()

    assert worksheet.get(RC381_PART_3_LINE_6).value == Rate(D("0.42857"))
    assert isinstance(worksheet.producer_of(RC381_PART_3_LINE_6), RatioTruncated)


def test_return_bo_line_6_is_cut_not_rounded() -> None:
    # 20,000 / 30,000 = 0.66666..., which rounding would make 0.66667.
    worksheet = return_bo(line_1="20000", line_2="10000")

    assert worksheet.get(RC381_PART_3_LINE_6).value == Rate(D("0.66666"))


def test_return_bo_line_6_is_zero_when_there_are_no_pensionable_earnings() -> None:
    # Line 3 is 0, so line 6 is 0 and not an error.
    worksheet = return_bo(line_1="0", line_2="0", line_19="0")

    assert worksheet.get(RC381_PART_3_LINE_3).value == D("0")
    assert worksheet.get(RC381_PART_3_LINE_6).value == Rate(D("0"))


def test_return_bo_lines_7_to_10_are_the_table_amounts_times_line_6() -> None:
    # Line 6 is 0.42857. Line 7: line E 81,200.00 x 0.42857 = 34,799.884, 34,799.88; line 8: line
    # C 71,300.00 x 0.42857 = 30,557.041, 30,557.04; line 9: line F 3,500.00 x 0.42857 =
    # 1,499.995, 1,500.00 (half up); line 10: line D 9,900.00 x 0.42857 = 4,242.843, 4,242.84.
    worksheet = return_bo()

    assert worksheet.get(RC381_PART_3_LINE_7).value == D("34799.88")
    assert worksheet.get(RC381_PART_3_LINE_8).value == D("30557.04")
    assert worksheet.get(RC381_PART_3_LINE_9).value == D("1500.00")
    assert worksheet.get(RC381_PART_3_LINE_10).value == D("4242.84")


def test_return_bo_line_11_is_the_lesser_of_line_1_and_line_7() -> None:
    # The lesser of 30,000 and 34,799.88 is 30,000.00.
    worksheet = return_bo()

    assert worksheet.get(RC381_PART_3_LINE_11).value == D("30000.00")
    assert isinstance(worksheet.producer_of(RC381_PART_3_LINE_11), LesserOf)


def test_return_bo_line_14_is_line_11_less_line_8_and_not_below_zero() -> None:
    # 30,000.00 less 30,557.04 is negative, entered as "0".
    worksheet = return_bo()

    assert worksheet.get(RC381_PART_3_LINE_14).value == D("0")
    assert isinstance(worksheet.producer_of(RC381_PART_3_LINE_14), SubtractNotBelowZero)


def test_return_bo_line_15_is_zero_when_line_3_is_not_more_than_line_c() -> None:
    # Line 3 (70,000.00) is not more than line C (71,300.00): "If not, enter the amount from line
    # 11 on line 16", so line 15 is 0 and line 16 is line 11 less 0 = 30,000.00.
    worksheet = return_bo()

    assert worksheet.get(RC381_PART_3_LINE_15_LESSER).value == D("0")
    assert worksheet.get(RC381_PART_3_LINE_15).value == D("0")
    assert worksheet.get(RC381_PART_3_LINE_16).value == D("30000.00")
    assert isinstance(worksheet.producer_of(RC381_PART_3_LINE_15), AmountWhenMore)
    assert isinstance(worksheet.producer_of(RC381_PART_3_LINE_16), Subtract)


def test_return_bo_line_18_is_line_16_less_line_9() -> None:
    # 30,000.00 less 1,500.00 is 28,500.00.
    worksheet = return_bo()

    assert worksheet.get(RC381_PART_3_LINE_18).value == D("28500.00")
    assert isinstance(worksheet.producer_of(RC381_PART_3_LINE_18), SubtractNotBelowZero)


def test_return_bo_line_18_is_zero_when_line_9_is_more_than_line_16() -> None:
    # Line 1 is 1,000 and line 2 is 1,000: line 6 is 0.5, line 9 is 3,500.00 x 0.5 = 1,750.00, line
    # 11 is the lesser of 1,000 and 40,600.00, 1,000; line 3 (2,000) is not more than line C, so
    # line 15 is 0 and line 16 is 1,000. Line 16 less line 9 is negative, entered as "0", so lines
    # 22 and 23 are 0.00.
    worksheet = return_bo(line_1="1000", line_2="1000", line_19="50.00")

    assert worksheet.get(RC381_PART_3_LINE_9).value == D("1750.00")
    assert worksheet.get(RC381_PART_3_LINE_16).value == D("1000")
    assert worksheet.get(RC381_PART_3_LINE_18).value == D("0")
    assert worksheet.get(RC381_PART_3_LINE_22).value == D("0")
    assert worksheet.get(RC381_PART_3_LINE_23).value == D("0")


def test_return_bo_a_small_share_outside_quebec_scales_every_line_down() -> None:
    # Line 1 is 1,000 and line 2 is 99,000: line 3 is 100,000, line 6 is 0.01 and line 9 is 3,500.00
    # x 0.01 = 35.00. Line 7 is 812.00, so line 11 is the lesser of 1,000 and 812.00, 812.00. Line 3
    # is more than line C: line 14 is 812.00 less line 8 (713.00) = 99.00, line 15 is the lesser of
    # line 10 (99.00) and line 14 (99.00), 99.00, line 16 is 812.00 less 99.00 = 713.00 and line
    # 18 is 713.00 less 35.00 = 678.00.
    worksheet = return_bo(line_1="1000", line_2="99000", line_19="0")

    assert worksheet.get(RC381_PART_3_LINE_6).value == Rate(D("0.01"))
    assert worksheet.get(RC381_PART_3_LINE_9).value == D("35.00")
    assert worksheet.get(RC381_PART_3_LINE_15).value == D("99.00")
    assert worksheet.get(RC381_PART_3_LINE_16).value == D("713.00")
    assert worksheet.get(RC381_PART_3_LINE_18).value == D("678.00")
    assert worksheet.get(RC381_PART_3_LINE_26).value == D("3.96")


def test_return_bo_line_20_is_83_1933_percent_of_line_19() -> None:
    # 1,800.00 x 83.1933% = 1,497.4794, 1,497.48.
    worksheet = return_bo()

    assert worksheet.get(RC381_PART_3_LINE_20).value == D("1497.48")
    assert isinstance(worksheet.producer_of(RC381_PART_3_LINE_20), ApplyRate)


def test_return_bo_line_21_is_line_19_less_line_20() -> None:
    # 1,800.00 less 1,497.48 is 302.52.
    worksheet = return_bo()

    assert worksheet.get(RC381_PART_3_LINE_21).value == D("302.52")
    assert isinstance(worksheet.producer_of(RC381_PART_3_LINE_21), Subtract)


def test_return_bo_line_22_is_4_95_percent_of_line_18() -> None:
    # 28,500.00 x 4.95% = 1,410.75.
    worksheet = return_bo()

    assert worksheet.get(RC381_PART_3_LINE_22).value == D("1410.75")
    assert isinstance(worksheet.producer_of(RC381_PART_3_LINE_22), TieredContribution)


def test_return_bo_line_23_is_1_percent_of_line_18() -> None:
    # 28,500.00 x 1% = 285.00.
    worksheet = return_bo()

    assert worksheet.get(RC381_PART_3_LINE_23).value == D("285.00")
    assert isinstance(worksheet.producer_of(RC381_PART_3_LINE_23), TieredContribution)


def test_return_bo_line_24_adds_lines_22_and_23() -> None:
    # 1,410.75 plus 285.00 is 1,695.75.
    worksheet = return_bo()

    assert worksheet.get(RC381_PART_3_LINE_24).value == D("1695.75")
    assert isinstance(worksheet.producer_of(RC381_PART_3_LINE_24), Sum)


def test_return_bo_line_26_is_4_percent_of_line_15() -> None:
    # Line 15 is 0, so 0 x 4% is 0.00.
    worksheet = return_bo()

    assert worksheet.get(RC381_PART_3_LINE_26).value == D("0")
    assert isinstance(worksheet.producer_of(RC381_PART_3_LINE_26), TieredContribution)


# Part 3 above line C.


def test_return_bo_above_line_c_lines_12_to_15_are_completed() -> None:
    # Line 1 is 50,000 and line 2 is 40,000: line 3 is 90,000.00, more than line C (71,300.00).
    # Line 6 = 50,000 / 90,000 = 0.555555... cut at 0.55555. Line 7 = 81,200.00 x 0.55555 =
    # 45,110.66 (45,110.660), line 8 = 71,300.00 x 0.55555 = 39,610.715, 39,610.72 (half up),
    # line 9 = 3,500.00 x 0.55555 = 1,944.425, 1,944.43, line 10 = 9,900.00 x 0.55555 = 5,499.945,
    # 5,499.95. Line 11 = the lesser of 50,000 and 45,110.66 = 45,110.66. Line 14 = 45,110.66 less
    # 39,610.72 = 5,499.94. Line 15 = the lesser of line 10 (5,499.95) and line 14 (5,499.94) =
    # 5,499.94. Line 16 = 45,110.66 less 5,499.94 = 39,610.72. Line 18 = 39,610.72 less 1,944.43 =
    # 37,666.29. Line 22 = 37,666.29 x 4.95% = 1,864.48 (1,864.4814), line 23 = 376.66, line 24 =
    # 2,241.14, line 26 = 5,499.94 x 4% = 219.9976, 220.00.
    worksheet = return_bo(line_1="50000", line_2="40000", line_19="3500.00")

    assert worksheet.get(RC381_PART_3_LINE_3).value == D("90000")
    assert worksheet.get(RC381_PART_3_LINE_6).value == Rate(D("0.55555"))
    assert worksheet.get(RC381_PART_3_LINE_7).value == D("45110.66")
    assert worksheet.get(RC381_PART_3_LINE_8).value == D("39610.72")
    assert worksheet.get(RC381_PART_3_LINE_9).value == D("1944.43")
    assert worksheet.get(RC381_PART_3_LINE_10).value == D("5499.95")
    assert worksheet.get(RC381_PART_3_LINE_11).value == D("45110.66")
    assert worksheet.get(RC381_PART_3_LINE_14).value == D("5499.94")
    assert worksheet.get(RC381_PART_3_LINE_15_LESSER).value == D("5499.94")
    assert worksheet.get(RC381_PART_3_LINE_15).value == D("5499.94")
    assert worksheet.get(RC381_PART_3_LINE_16).value == D("39610.72")
    assert worksheet.get(RC381_PART_3_LINE_18).value == D("37666.29")
    assert worksheet.get(RC381_PART_3_LINE_20).value == D("2911.77")
    assert worksheet.get(RC381_PART_3_LINE_21).value == D("588.23")
    assert worksheet.get(RC381_PART_3_LINE_22).value == D("1864.48")
    assert worksheet.get(RC381_PART_3_LINE_23).value == D("376.66")
    assert worksheet.get(RC381_PART_3_LINE_24).value == D("2241.14")
    assert worksheet.get(RC381_PART_3_LINE_26).value == D("220.00")


def test_return_bo_line_15_is_zero_when_line_3_is_exactly_line_c() -> None:
    # Line 1 is 30,000 and line 2 is 41,300: line 3 is 71,300, which is line C, not more. Line 6 is
    # 0.42075, line 8 is 29,999.48, so line 14 is 30,000 less 29,999.48 = 0.52 and the lesser of
    # lines 10 (4,165.43) and 14 is 0.52, but line 3 is not more than line C: line 15 is 0.
    worksheet = return_bo(line_1="30000", line_2="41300", line_19="0")

    assert worksheet.get(RC381_PART_3_LINE_14).value == D("0.52")
    assert worksheet.get(RC381_PART_3_LINE_15_LESSER).value == D("0.52")
    assert worksheet.get(RC381_PART_3_LINE_15).value == D("0")
    assert worksheet.get(RC381_PART_3_LINE_16).value == D("30000")
    assert worksheet.get(RC381_PART_3_LINE_18).value == D("28527.37")


def test_return_bo_line_15_is_the_lesser_when_line_3_is_one_dollar_more_than_line_c() -> None:
    # Line 2 of 41,301 makes line 3 71,301, more than line C: line 15 is 0.52, line 16 is 30,000
    # less 0.52 = 29,999.48 and line 18 is 29,999.48 less line 9 (1,472.63) = 28,526.85.
    worksheet = return_bo(line_1="30000", line_2="41301", line_19="0")

    assert worksheet.get(RC381_PART_3_LINE_15).value == D("0.52")
    assert worksheet.get(RC381_PART_3_LINE_16).value == D("29999.48")
    assert worksheet.get(RC381_PART_3_LINE_18).value == D("28526.85")


def test_return_bo_with_all_the_earnings_outside_quebec_line_6_is_1() -> None:
    # Line 1 is 80,000 and line 2 is 0: line 6 is 1, so lines 7 to 10 are the table's own amounts
    # (81,200.00, 71,300.00, 3,500.00 and 9,900.00). Line 11 is the lesser of 80,000 and 81,200.00,
    # 80,000. Line 3 is above line C: line 14 = 80,000 less 71,300.00 = 8,700.00 = line 15 (below
    # line 10), line 16 = 71,300.00, line 18 = 67,800.00 and the required contributions are the
    # maxima: line 22 3,356.10, line 23 678.00, line 24 4,034.10, line 26 8,700.00 x 4% = 348.00.
    worksheet = return_bo(line_1="80000", line_2="0", line_19="4000.00")

    assert worksheet.get(RC381_PART_3_LINE_6).value == Rate(D("1"))
    assert worksheet.get(RC381_PART_3_LINE_7).value == D("81200.00")
    assert worksheet.get(RC381_PART_3_LINE_8).value == D("71300.00")
    assert worksheet.get(RC381_PART_3_LINE_9).value == D("3500.00")
    assert worksheet.get(RC381_PART_3_LINE_10).value == D("9900.00")
    assert worksheet.get(RC381_PART_3_LINE_11).value == D("80000")
    assert worksheet.get(RC381_PART_3_LINE_15).value == D("8700.00")
    assert worksheet.get(RC381_PART_3_LINE_16).value == D("71300.00")
    assert worksheet.get(RC381_PART_3_LINE_18).value == D("67800.00")
    assert worksheet.get(RC381_PART_3_LINE_20).value == D("3327.73")
    assert worksheet.get(RC381_PART_3_LINE_21).value == D("672.27")
    assert worksheet.get(RC381_PART_3_LINE_22).value == D("3356.10")
    assert worksheet.get(RC381_PART_3_LINE_23).value == D("678.00")
    assert worksheet.get(RC381_PART_3_LINE_24).value == D("4034.10")
    assert worksheet.get(RC381_PART_3_LINE_26).value == D("348.00")


def test_return_bo_with_6_months_the_lines_read_the_row_of_line_a() -> None:
    # Line A is 6 (lines C to F: 35,650.00, 4,950.00, 40,600.00 and 1,750.00), line B is 12. Line
    # 1 is 20,000 and line 2 is 10,000: line 6 = 0.66666 (cut). Line 7 = 40,600.00 x 0.66666 =
    # 27,066.396, 27,066.40; line 8 = 35,650.00 x 0.66666 = 23,766.429, 23,766.43; line 9 =
    # 1,750.00 x 0.66666 = 1,166.655, 1,166.66; line 10 = 4,950.00 x 0.66666 = 3,299.967, 3,299.97.
    # Line 11 = the lesser of 20,000 and 27,066.40 = 20,000; line 3 (30,000) is not more than line C
    # (35,650.00), so line 15 is 0, line 16 20,000, line 18 20,000 less 1,166.66 = 18,833.34.
    worksheet = return_bo(
        line_1="20000", line_2="10000", line_19="900.00", cpp_months=6, qpp_months=12
    )

    assert worksheet.get(RC381_PART_3_LINE_6).value == Rate(D("0.66666"))
    assert worksheet.get(RC381_PART_3_LINE_7).value == D("27066.40")
    assert worksheet.get(RC381_PART_3_LINE_8).value == D("23766.43")
    assert worksheet.get(RC381_PART_3_LINE_9).value == D("1166.66")
    assert worksheet.get(RC381_PART_3_LINE_10).value == D("3299.97")
    assert worksheet.get(RC381_PART_3_LINE_11).value == D("20000")
    assert worksheet.get(RC381_PART_3_LINE_15).value == D("0")
    assert worksheet.get(RC381_PART_3_LINE_16).value == D("20000")
    assert worksheet.get(RC381_PART_3_LINE_18).value == D("18833.34")
    assert worksheet.get(RC381_PART_3_LINE_20).value == D("748.74")
    assert worksheet.get(RC381_PART_3_LINE_21).value == D("151.26")
    assert worksheet.get(RC381_PART_3_LINE_22).value == D("932.25")
    assert worksheet.get(RC381_PART_3_LINE_23).value == D("188.33")
    assert worksheet.get(RC381_PART_3_LINE_24).value == D("1120.58")


# A return with no Quebec figures.


def test_a_return_with_no_quebec_figures_is_unchanged_and_rc381_part_3_is_zero() -> None:
    # Employment income of 60,000 and none of the RC381 totals: the T1 lines are Schedule 8's, base
    # contributions 4.95% x (60,000 less 3,500) = 2,796.75 and enhanced 1% x 56,500 = 565.00, and
    # every Part 3 line is 0.
    worksheet = compute("60000", (), "0", "0", "0", "0", "0")

    assert worksheet.get(CPP_BASE_CONTRIBUTIONS).value == D("2796.75")
    assert worksheet.get(CPP_ENHANCED_CONTRIBUTIONS).value == D("565.00")
    assert worksheet.get(NET_INCOME).value == D("59435.00")
    kinds: tuple[ArtifactKind[Any], ...] = (
        RC381_PART_3_LINE_3,
        RC381_PART_3_LINE_7,
        RC381_PART_3_LINE_8,
        RC381_PART_3_LINE_9,
        RC381_PART_3_LINE_10,
        RC381_PART_3_LINE_11,
        RC381_PART_3_LINE_14,
        RC381_PART_3_LINE_15,
        RC381_PART_3_LINE_16,
        RC381_PART_3_LINE_18,
        RC381_PART_3_LINE_20,
        RC381_PART_3_LINE_21,
        RC381_PART_3_LINE_22,
        RC381_PART_3_LINE_23,
        RC381_PART_3_LINE_24,
        RC381_PART_3_LINE_26,
    )
    assert worksheet.get(RC381_PART_3_LINE_6).value == Rate(D("0"))
    for kind in kinds:
        assert worksheet.get(kind).value == D("0"), kind.identifier


def test_the_rc381_figures_do_not_change_the_t1_lines_yet() -> None:
    # This part of Form RC381 reaches no line of the return: the same employment income with and
    # without the T4 totals gives the same Schedule 8 contributions, net income and total payable.
    with_totals = return_bo()
    without_totals = return_bo(line_1="0", line_2="0", line_19="0")

    for kind in (CPP_BASE_CONTRIBUTIONS, CPP_ENHANCED_CONTRIBUTIONS, NET_INCOME, TOTAL_PAYABLE):
        assert with_totals.get(kind).value == without_totals.get(kind).value, kind.identifier
