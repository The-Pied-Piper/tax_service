"""CA-ON 2025 end to end: return bo (Form RC381 Part 2 and Part 3 lines 1 to 93)."""

from __future__ import annotations

from decimal import Decimal
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
from app.domain.capabilities.sum_not_below_zero import SumNotBelowZero
from app.domain.errors import InputBelowBoundError, NoAmountForCountError
from app.domain.parameters.rate import Rate
from app.domain.worksheet import Worksheet
from app.jurisdictions.ca.capabilities.amount_when_more import AmountWhenMore
from app.jurisdictions.ca.capabilities.choose_by_sign import ChooseBySign
from app.jurisdictions.ca.capabilities.count_at_least import CountAtLeast
from app.jurisdictions.ca.capabilities.lesser_of_when_positive import LesserOfWhenPositive
from app.jurisdictions.ca.capabilities.positive_part_of_negation import PositivePartOfNegation
from app.jurisdictions.ca.capabilities.ratio_truncated import RatioTruncated
from app.jurisdictions.ca.catalog import (
    CPP_ADDITIONAL_MAXIMUM_PENSIONABLE_EARNINGS,
    CPP_BASE_CONTRIBUTIONS,
    CPP_BASIC_EXEMPTION,
    CPP_ENHANCED_CONTRIBUTIONS,
    CPP_MAXIMUM_PENSIONABLE_EARNINGS,
    CPP_SECOND_ADDITIONAL_EARNINGS_MAXIMUM,
    NET_INCOME,
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
    TOTAL_PAYABLE,
)
from tests.jurisdictions.ca_on.end_to_end.support import D, compute


def return_bo(
    line_1: str = "30000",
    line_2: str = "40000",
    line_19: str = "1800.00",
    line_39: str = "2500.00",
    *,
    line_25: str = "0",
    line_45: str = "0",
    cpp_months: int = 12,
    qpp_months: int = 12,
) -> Worksheet:
    """Return BO's inputs (`returns/2025_return_bo.yaml`): employment income of 70000 on a T4 for
    Ontario employment (box 26 `line_1`, box 16 `line_19`, box 16A `line_25`) and a T4 for Quebec
    employment (box 26 `line_2`, box 17 `line_39`, box 17A `line_45`)."""
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
        cpp_t4_base_and_first_additional_contributions=line_19,
        t4_cpp_second_additional_box_16a=line_25,
        t4_qpp_contributions_box_17=line_39,
        t4_qpp_second_additional_box_17a=line_45,
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


# Part 3, the QPP side.


def test_return_bo_lines_27_to_30_are_the_qpp_row_of_the_table_less_lines_7_to_10() -> None:
    # Line 27 = line I (81,200.00) less line 7 (34,799.88) = 46,400.12; line 28 = line G
    # (71,300.00) less line 8 (30,557.04) = 40,742.96; line 29 = line J (3,500.00) less line 9
    # (1,500.00) = 2,000.00; line 30 = line H (9,900.00) less line 10 (4,242.84) = 5,657.16.
    worksheet = return_bo()

    assert worksheet.get(RC381_PART_3_LINE_27).value == D("46400.12")
    assert worksheet.get(RC381_PART_3_LINE_28).value == D("40742.96")
    assert worksheet.get(RC381_PART_3_LINE_29).value == D("2000.00")
    assert worksheet.get(RC381_PART_3_LINE_30).value == D("5657.16")


def test_return_bo_lines_27_to_30_are_subtractions_of_lines_7_to_10() -> None:
    worksheet = return_bo()

    for kind in (
        RC381_PART_3_LINE_27,
        RC381_PART_3_LINE_28,
        RC381_PART_3_LINE_29,
        RC381_PART_3_LINE_30,
    ):
        assert isinstance(worksheet.producer_of(kind), Subtract), kind.identifier


def test_return_bo_line_31_is_the_lesser_of_line_2_and_line_27() -> None:
    # Line 2 is 40,000 and line 27 is 46,400.12: line 31 is 40,000.00.
    worksheet = return_bo()

    assert worksheet.get(RC381_PART_3_LINE_31).value == D("40000")


def test_return_bo_line_31_is_line_27_when_that_is_the_lesser() -> None:
    # Line 1 is 80,000 and line 2 is 40,000: line 3 is 120,000.00 and line 6 is 0.66666. Line 7 =
    # 81,200.00 x 0.66666 = 54,132.79 (54,132.7920), so line 27 = 81,200.00 less 54,132.79 =
    # 27,067.21, less than line 2 (40,000): line 31 is 27,067.21.
    worksheet = return_bo(line_1="80000", line_2="40000", line_19="0", line_39="0")

    assert worksheet.get(RC381_PART_3_LINE_27).value == D("27067.21")
    assert worksheet.get(RC381_PART_3_LINE_31).value == D("27067.21")


def test_return_bo_line_34_is_line_31_less_line_28_and_not_below_zero() -> None:
    # Line 31 is 40,000.00 and line 28 is 40,742.96: the difference is negative, so line 34 is 0.
    worksheet = return_bo()

    assert worksheet.get(RC381_PART_3_LINE_34).value == D("0")


def test_return_bo_line_35_is_zero_when_line_3_is_not_more_than_line_g() -> None:
    # Line 3 (70,000.00) is not more than line G (71,300.00), so lines 32 to 35 are not completed:
    # line 35 is 0 (line 34, line 31 less line 28 = 40,000.00 less 40,742.96, is 0 as it is
    # negative, so the lesser of line 30 (5,657.16) and line 34 is 0), the amount from line 31 is
    # entered on line 36 (40,000.00 less 0), and line 38 = line 36 less line 29 = 38,000.00.
    worksheet = return_bo()

    assert worksheet.get(RC381_PART_3_LINE_35_LESSER).value == D("0")
    assert worksheet.get(RC381_PART_3_LINE_35).value == D("0")
    assert worksheet.get(RC381_PART_3_LINE_36).value == D("40000")
    assert worksheet.get(RC381_PART_3_LINE_38).value == D("38000.00")


def test_return_bo_line_35_is_zero_when_line_3_is_exactly_line_g() -> None:
    # Line 1 is 17,825 and line 2 is 53,475: line 3 is 71,300, which is line G, not more. Line 6
    # is 0.25, line 8 is 17,825.00 so line 28 is 53,475.00 and line 34 (53,475 less 53,475.00) is
    # 0.00, line 35 is 0, line 36 is 53,475 and line 38 = 53,475 less line 29 (2,625.00) =
    # 50,850.00.
    worksheet = return_bo(line_1="17825", line_2="53475", line_19="0", line_39="0")

    assert worksheet.get(RC381_PART_3_LINE_28).value == D("53475.00")
    assert worksheet.get(RC381_PART_3_LINE_34).value == D("0.00")
    assert worksheet.get(RC381_PART_3_LINE_35_LESSER).value == D("0.00")
    assert worksheet.get(RC381_PART_3_LINE_35).value == D("0")
    assert worksheet.get(RC381_PART_3_LINE_36).value == D("53475")
    assert worksheet.get(RC381_PART_3_LINE_38).value == D("50850.00")
    assert worksheet.get(RC381_PART_3_LINE_46).value == D("0.00")


def test_return_bo_line_35_is_the_lesser_when_line_3_is_one_dollar_more_than_line_g() -> None:
    # Line 2 of 53,476 makes line 3 71,301, more than line G. Line 6 is 0.24999; line 7 =
    # 20,299.19, line 8 = 17,824.29, line 9 = 874.97, line 10 = 2,474.90. Line 27 = 60,900.81,
    # line 28 = 53,475.71, line 29 = 2,625.03, line 30 = 7,425.10; line 31 = 53,476 (line 2), line
    # 34 = 53,476 less 53,475.71 = 0.29 and line 35 is the lesser of line 30 (7,425.10) and line
    # 34 (0.29): 0.29. Line 36 = 53,476 less 0.29 = 53,475.71 and line 38 = 53,475.71 less
    # 2,625.03 = 50,850.68; line 46 = 0.29 x 4% = 0.0116, 0.01.
    worksheet = return_bo(line_1="17825", line_2="53476", line_19="0", line_39="0")

    assert worksheet.get(RC381_PART_3_LINE_27).value == D("60900.81")
    assert worksheet.get(RC381_PART_3_LINE_28).value == D("53475.71")
    assert worksheet.get(RC381_PART_3_LINE_29).value == D("2625.03")
    assert worksheet.get(RC381_PART_3_LINE_30).value == D("7425.10")
    assert worksheet.get(RC381_PART_3_LINE_31).value == D("53476")
    assert worksheet.get(RC381_PART_3_LINE_34).value == D("0.29")
    assert worksheet.get(RC381_PART_3_LINE_35_LESSER).value == D("0.29")
    assert worksheet.get(RC381_PART_3_LINE_35).value == D("0.29")
    assert worksheet.get(RC381_PART_3_LINE_36).value == D("53475.71")
    assert worksheet.get(RC381_PART_3_LINE_38).value == D("50850.68")
    assert worksheet.get(RC381_PART_3_LINE_46).value == D("0.01")


def test_return_bo_above_line_g_lines_32_to_35_are_completed() -> None:
    # Line 1 is 50,000 and line 2 is 40,000 (box 17 of 2,800.00, box 17A of 100.00, box 16 of
    # 3,500.00 and box 16A of 150.00): line 3 is 90,000.00, more than line G (71,300.00). The CPP
    # side is the same as in the test of lines 12 to 15 above (line 7 45,110.66, line 8 39,610.72,
    # line 9 1,944.43, line 10 5,499.95). Line 27 = 81,200.00 less 45,110.66 = 36,089.34, line 28
    # = 71,300.00 less 39,610.72 = 31,689.28, line 29 = 3,500.00 less 1,944.43 = 1,555.57, line 30
    # = 9,900.00 less 5,499.95 = 4,400.05. Line 31 = the lesser of 40,000 and 36,089.34 =
    # 36,089.34. Line 34 = 36,089.34 less 31,689.28 = 4,400.06; line 35 = the lesser of line 30
    # (4,400.05) and line 34 (4,400.06) = 4,400.05. Line 36 = 36,089.34 less 4,400.05 = 31,689.29;
    # line 38 = 31,689.29 less 1,555.57 = 30,133.72. Line 40 = 2,800.00 x 84.375% = 2,362.50; line
    # 41 = 437.50. Line 42 = 30,133.72 x 5.4% = 1,627.22 (1,627.2209); line 43 = 301.34
    # (301.3372); line 44 = 1,928.56; line 46 = 4,400.05 x 4% = 176.00 (176.002). Line 49 =
    # 2,911.77 + 2,362.50 = 5,274.27; line 52 = 1,864.48 + 1,627.22 = 3,491.70; line 53 =
    # 1,782.57. Line 56 = 588.23 + 437.50 = 1,025.73; line 59 = 376.66 + 301.34 = 678.00; line 60
    # = 347.73; line 61 = 2,130.30. Line 64 = 150.00 + 100.00 = 250.00; line 67 = 220.00 + 176.00
    # = 396.00; line 68 = 250.00 less 396.00 = -146.00; line 69 = 2,130.30 less 146.00 = 1,984.30.
    worksheet = return_bo(
        line_1="50000",
        line_2="40000",
        line_19="3500.00",
        line_39="2800.00",
        line_25="150.00",
        line_45="100.00",
    )

    assert worksheet.get(RC381_PART_3_LINE_27).value == D("36089.34")
    assert worksheet.get(RC381_PART_3_LINE_28).value == D("31689.28")
    assert worksheet.get(RC381_PART_3_LINE_29).value == D("1555.57")
    assert worksheet.get(RC381_PART_3_LINE_30).value == D("4400.05")
    assert worksheet.get(RC381_PART_3_LINE_31).value == D("36089.34")
    assert worksheet.get(RC381_PART_3_LINE_34).value == D("4400.06")
    assert worksheet.get(RC381_PART_3_LINE_35_LESSER).value == D("4400.05")
    assert worksheet.get(RC381_PART_3_LINE_35).value == D("4400.05")
    assert worksheet.get(RC381_PART_3_LINE_36).value == D("31689.29")
    assert worksheet.get(RC381_PART_3_LINE_38).value == D("30133.72")
    assert worksheet.get(RC381_PART_3_LINE_40).value == D("2362.50")
    assert worksheet.get(RC381_PART_3_LINE_41).value == D("437.50")
    assert worksheet.get(RC381_PART_3_LINE_42).value == D("1627.22")
    assert worksheet.get(RC381_PART_3_LINE_43).value == D("301.34")
    assert worksheet.get(RC381_PART_3_LINE_44).value == D("1928.56")
    assert worksheet.get(RC381_PART_3_LINE_46).value == D("176.00")
    assert worksheet.get(RC381_PART_3_LINE_49).value == D("5274.27")
    assert worksheet.get(RC381_PART_3_LINE_52).value == D("3491.70")
    assert worksheet.get(RC381_PART_3_LINE_53).value == D("1782.57")
    assert worksheet.get(RC381_PART_3_LINE_56).value == D("1025.73")
    assert worksheet.get(RC381_PART_3_LINE_59).value == D("678.00")
    assert worksheet.get(RC381_PART_3_LINE_60).value == D("347.73")
    assert worksheet.get(RC381_PART_3_LINE_61).value == D("2130.30")
    assert worksheet.get(RC381_PART_3_LINE_64).value == D("250.00")
    assert worksheet.get(RC381_PART_3_LINE_67).value == D("396.00")
    assert worksheet.get(RC381_PART_3_LINE_68).value == D("-146.00")
    assert worksheet.get(RC381_PART_3_LINE_69).value == D("1984.30")


def test_return_bo_line_35_is_capped_by_line_30_and_line_38_by_the_table() -> None:
    # Line 1 is 0 and line 2 is 85,000 (the Quebec slips together): line 6 is 0, so lines 27 to 30
    # are the table's row (81,200.00, 71,300.00, 3,500.00 and 9,900.00). Line 31 = the lesser of
    # 85,000 and 81,200.00 = 81,200.00; line 34 = 81,200.00 less 71,300.00 = 9,900.00; line 35 =
    # the lesser of line 30 (9,900.00) and line 34 (9,900.00) = 9,900.00 (line 3 of 85,000.00 is
    # more than line G). Line 36 = 71,300.00; line 38 = 71,300.00 less 3,500.00 = 67,800.00, so
    # the required contributions are the maxima: line 42 3,661.20, line 43 678.00, line 44
    # 4,339.20, line 46 396.00.
    worksheet = return_bo(
        line_1="0", line_2="85000", line_19="0", line_39="3000.00", line_45="400.00"
    )

    assert worksheet.get(RC381_PART_3_LINE_27).value == D("81200.00")
    assert worksheet.get(RC381_PART_3_LINE_28).value == D("71300.00")
    assert worksheet.get(RC381_PART_3_LINE_29).value == D("3500.00")
    assert worksheet.get(RC381_PART_3_LINE_30).value == D("9900.00")
    assert worksheet.get(RC381_PART_3_LINE_31).value == D("81200.00")
    assert worksheet.get(RC381_PART_3_LINE_34).value == D("9900.00")
    assert worksheet.get(RC381_PART_3_LINE_35).value == D("9900.00")
    assert worksheet.get(RC381_PART_3_LINE_36).value == D("71300.00")
    assert worksheet.get(RC381_PART_3_LINE_38).value == D("67800.00")
    assert worksheet.get(RC381_PART_3_LINE_42).value == D("3661.20")
    assert worksheet.get(RC381_PART_3_LINE_43).value == D("678.00")
    assert worksheet.get(RC381_PART_3_LINE_44).value == D("4339.20")
    assert worksheet.get(RC381_PART_3_LINE_46).value == D("396.00")
    assert worksheet.get(RC381_PART_3_LINE_68).value == D("4.00")
    assert worksheet.get(RC381_PART_3_LINE_69).value == D("-1335.20")


def test_return_bo_line_40_is_84_375_percent_of_line_39() -> None:
    # 2,500.00 x 84.375% = 2,109.375, which rounds half up to 2,109.38.
    worksheet = return_bo()

    assert worksheet.get(RC381_PART_3_LINE_40).value == D("2109.38")


def test_return_bo_line_40_is_produced_by_apply_rate_and_line_41_by_subtract() -> None:
    worksheet = return_bo()

    assert isinstance(worksheet.producer_of(RC381_PART_3_LINE_40), ApplyRate)
    assert isinstance(worksheet.producer_of(RC381_PART_3_LINE_41), Subtract)


def test_return_bo_line_41_is_line_39_less_line_40() -> None:
    # 2,500.00 less 2,109.38 is 390.62.
    worksheet = return_bo()

    assert worksheet.get(RC381_PART_3_LINE_41).value == D("390.62")


def test_return_bo_line_42_is_5_4_percent_of_line_38() -> None:
    # 38,000.00 x 5.4% = 2,052.00.
    worksheet = return_bo()

    assert worksheet.get(RC381_PART_3_LINE_42).value == D("2052.00")


def test_return_bo_line_43_is_1_percent_of_line_38() -> None:
    # 38,000.00 x 1% = 380.00.
    worksheet = return_bo()

    assert worksheet.get(RC381_PART_3_LINE_43).value == D("380.00")


def test_return_bo_line_44_adds_lines_42_and_43() -> None:
    # 2,052.00 plus 380.00 is 2,432.00.
    worksheet = return_bo()

    assert worksheet.get(RC381_PART_3_LINE_44).value == D("2432.00")


def test_return_bo_line_46_is_4_percent_of_line_35() -> None:
    # Line 35 is 0, so 0 x 4% is 0.00.
    worksheet = return_bo()

    assert worksheet.get(RC381_PART_3_LINE_46).value == D("0.00")


def test_return_bo_the_qpp_required_lines_are_tiered_contributions() -> None:
    worksheet = return_bo()

    for kind in (RC381_PART_3_LINE_42, RC381_PART_3_LINE_43, RC381_PART_3_LINE_46):
        assert isinstance(worksheet.producer_of(kind), TieredContribution), kind.identifier
    assert isinstance(worksheet.producer_of(RC381_PART_3_LINE_44), Sum)
    assert isinstance(worksheet.producer_of(RC381_PART_3_LINE_35), AmountWhenMore)
    assert isinstance(worksheet.producer_of(RC381_PART_3_LINE_35_LESSER), LesserOf)
    assert isinstance(worksheet.producer_of(RC381_PART_3_LINE_31), LesserOf)
    assert isinstance(worksheet.producer_of(RC381_PART_3_LINE_34), SubtractNotBelowZero)
    assert isinstance(worksheet.producer_of(RC381_PART_3_LINE_38), SubtractNotBelowZero)


# Part 3 lines 49 to 69, the totals.


def test_return_bo_lines_49_and_52_are_the_base_contribution_totals() -> None:
    # Line 49 = line 20 (1,497.48) + line 40 (2,109.38) = 3,606.86; line 52 = line 22 (1,410.75) +
    # line 42 (2,052.00) = 3,462.75.
    worksheet = return_bo()

    assert worksheet.get(RC381_PART_3_LINE_49).value == D("3606.86")
    assert worksheet.get(RC381_PART_3_LINE_52).value == D("3462.75")


def test_return_bo_line_53_is_line_49_less_line_52() -> None:
    # 3,606.86 less 3,462.75 is 144.11.
    worksheet = return_bo()

    assert worksheet.get(RC381_PART_3_LINE_53).value == D("144.11")


def test_return_bo_lines_56_and_59_are_the_first_additional_totals() -> None:
    # Line 56 = line 21 (302.52) + line 41 (390.62) = 693.14; line 59 = line 23 (285.00) + line 43
    # (380.00) = 665.00.
    worksheet = return_bo()

    assert worksheet.get(RC381_PART_3_LINE_56).value == D("693.14")
    assert worksheet.get(RC381_PART_3_LINE_59).value == D("665.00")


def test_return_bo_line_60_is_line_56_less_line_59() -> None:
    # 693.14 less 665.00 is 28.14.
    worksheet = return_bo()

    assert worksheet.get(RC381_PART_3_LINE_60).value == D("28.14")


def test_return_bo_line_61_is_line_53_plus_line_60() -> None:
    # 144.11 plus 28.14 is 172.25.
    worksheet = return_bo()

    assert worksheet.get(RC381_PART_3_LINE_61).value == D("172.25")


def test_return_bo_lines_64_and_67_are_the_second_additional_contributions() -> None:
    # With no box 16A or 17A, line 64 is 0 + 0 = 0, and line 67 = line 26 (0) + line 46 (0) = 0.
    worksheet = return_bo()

    assert worksheet.get(RC381_PART_3_LINE_64).value == D("0")
    assert worksheet.get(RC381_PART_3_LINE_67).value == D("0.00")


def test_return_bo_line_68_is_zero_when_there_are_no_second_additional_contributions() -> None:
    # Line 64 (0) less line 67 (0) is 0.
    worksheet = return_bo()

    assert worksheet.get(RC381_PART_3_LINE_68).value == D("0.00")


def test_return_bo_line_69_is_line_61_plus_line_68_and_matches_the_tickets_example() -> None:
    # 172.25 plus 0 is 172.25: positive, so Part 3a will carry line 52 (3,462.75) to line 30800,
    # line 59 + line 67 (665.00) to line 22215 and line 69 (172.25) to line 44800.
    worksheet = return_bo()

    assert worksheet.get(RC381_PART_3_LINE_27).value == D("46400.12")
    assert worksheet.get(RC381_PART_3_LINE_28).value == D("40742.96")
    assert worksheet.get(RC381_PART_3_LINE_29).value == D("2000.00")
    assert worksheet.get(RC381_PART_3_LINE_30).value == D("5657.16")
    assert worksheet.get(RC381_PART_3_LINE_31).value == D("40000")
    assert worksheet.get(RC381_PART_3_LINE_34).value == D("0")
    assert worksheet.get(RC381_PART_3_LINE_35_LESSER).value == D("0")
    assert worksheet.get(RC381_PART_3_LINE_35).value == D("0")
    assert worksheet.get(RC381_PART_3_LINE_36).value == D("40000")
    assert worksheet.get(RC381_PART_3_LINE_38).value == D("38000.00")
    assert worksheet.get(RC381_PART_3_LINE_40).value == D("2109.38")
    assert worksheet.get(RC381_PART_3_LINE_41).value == D("390.62")
    assert worksheet.get(RC381_PART_3_LINE_42).value == D("2052.00")
    assert worksheet.get(RC381_PART_3_LINE_43).value == D("380.00")
    assert worksheet.get(RC381_PART_3_LINE_44).value == D("2432.00")
    assert worksheet.get(RC381_PART_3_LINE_46).value == D("0.00")
    assert worksheet.get(RC381_PART_3_LINE_49).value == D("3606.86")
    assert worksheet.get(RC381_PART_3_LINE_52).value == D("3462.75")
    assert worksheet.get(RC381_PART_3_LINE_53).value == D("144.11")
    assert worksheet.get(RC381_PART_3_LINE_56).value == D("693.14")
    assert worksheet.get(RC381_PART_3_LINE_59).value == D("665.00")
    assert worksheet.get(RC381_PART_3_LINE_60).value == D("28.14")
    assert worksheet.get(RC381_PART_3_LINE_61).value == D("172.25")
    assert worksheet.get(RC381_PART_3_LINE_64).value == D("0")
    assert worksheet.get(RC381_PART_3_LINE_67).value == D("0.00")
    assert worksheet.get(RC381_PART_3_LINE_68).value == D("0.00")
    assert worksheet.get(RC381_PART_3_LINE_69).value == D("172.25")


def test_return_bo_the_totals_are_sums_and_differences() -> None:
    worksheet = return_bo()

    for kind in (
        RC381_PART_3_LINE_49,
        RC381_PART_3_LINE_52,
        RC381_PART_3_LINE_56,
        RC381_PART_3_LINE_59,
        RC381_PART_3_LINE_61,
        RC381_PART_3_LINE_64,
        RC381_PART_3_LINE_67,
        RC381_PART_3_LINE_69,
    ):
        assert isinstance(worksheet.producer_of(kind), Sum), kind.identifier
    for kind in (RC381_PART_3_LINE_53, RC381_PART_3_LINE_60, RC381_PART_3_LINE_68):
        assert isinstance(worksheet.producer_of(kind), Subtract), kind.identifier


# Part 3 totals that are negative.


def test_return_bo_line_53_is_negative_when_actual_base_is_less_than_required() -> None:
    # With no box 16 or 17 contributions, line 49 is 0.00 and line 52 is 3,462.75: line 53 is
    # -3,462.75 (shown in brackets). Line 56 is 0.00 and line 59 is 665.00: line 60 is -665.00,
    # line 61 = -3,462.75 + -665.00 = -4,127.75, and so is line 69.
    worksheet = return_bo(line_19="0", line_39="0")

    assert worksheet.get(RC381_PART_3_LINE_49).value == D("0.00")
    assert worksheet.get(RC381_PART_3_LINE_52).value == D("3462.75")
    assert worksheet.get(RC381_PART_3_LINE_53).value == D("-3462.75")
    assert worksheet.get(RC381_PART_3_LINE_56).value == D("0.00")
    assert worksheet.get(RC381_PART_3_LINE_59).value == D("665.00")
    assert worksheet.get(RC381_PART_3_LINE_60).value == D("-665.00")
    assert worksheet.get(RC381_PART_3_LINE_61).value == D("-4127.75")
    assert worksheet.get(RC381_PART_3_LINE_64).value == D("0")
    assert worksheet.get(RC381_PART_3_LINE_67).value == D("0.00")
    assert worksheet.get(RC381_PART_3_LINE_68).value == D("0.00")
    assert worksheet.get(RC381_PART_3_LINE_69).value == D("-4127.75")


def test_return_bo_line_53_may_be_negative_while_line_60_is_positive() -> None:
    # Line 1 is 0, line 2 is 40,000, box 16 is 2,300.00 and box 17 is 0 (chosen figures; the form
    # takes the totals as entered): line 20 = 2,300.00 x 83.1933% = 1,913.45 (1,913.4459), line 21
    # = 386.55, line 38 = 36,500.00, line 42 = 1,971.00, line 43 = 365.00. Line 49 = 1,913.45 +
    # 0.00 and line 52 = 0.00 + 1,971.00: line 53 = -57.55. Line 56 = 386.55 and line 59 = 365.00:
    # line 60 = 21.55. Line 61 = -57.55 + 21.55 = -36.00.
    worksheet = return_bo(line_1="0", line_2="40000", line_19="2300.00", line_39="0")

    assert worksheet.get(RC381_PART_3_LINE_38).value == D("36500.00")
    assert worksheet.get(RC381_PART_3_LINE_42).value == D("1971.00")
    assert worksheet.get(RC381_PART_3_LINE_43).value == D("365.00")
    assert worksheet.get(RC381_PART_3_LINE_49).value == D("1913.45")
    assert worksheet.get(RC381_PART_3_LINE_52).value == D("1971.00")
    assert worksheet.get(RC381_PART_3_LINE_53).value == D("-57.55")
    assert worksheet.get(RC381_PART_3_LINE_56).value == D("386.55")
    assert worksheet.get(RC381_PART_3_LINE_59).value == D("365.00")
    assert worksheet.get(RC381_PART_3_LINE_60).value == D("21.55")
    assert worksheet.get(RC381_PART_3_LINE_61).value == D("-36.00")
    assert worksheet.get(RC381_PART_3_LINE_69).value == D("-36.00")


def test_return_bo_line_60_is_negative_when_line_53_is_positive() -> None:
    # Line 1 is 30,000 and line 2 is 0, box 16 is 0 and box 17 is 1,600.00 (chosen figures; the
    # form takes the totals as entered). Line 6 is 1, line 18 = 30,000 less 3,500.00 = 26,500.00,
    # line 22 = 1,311.75 and line 23 = 265.00; lines 27 to 30 are 0 (the whole QPP row is taken by
    # line 6), so line 38 is 0 and lines 42 and 43 are 0. Line 40 = 1,600.00 x 84.375% = 1,350.00
    # and line 41 = 250.00. Line 53 = (0 + 1,350.00) less (1,311.75 + 0) = 38.25; line 60 = (0 +
    # 250.00) less (265.00 + 0) = -15.00 (shown in brackets); line 61 = 38.25 + -15.00 = 23.25.
    worksheet = return_bo(line_1="30000", line_2="0", line_19="0", line_39="1600.00")

    assert worksheet.get(RC381_PART_3_LINE_6).value == Rate(D("1.00000"))
    assert worksheet.get(RC381_PART_3_LINE_18).value == D("26500.00")
    assert worksheet.get(RC381_PART_3_LINE_22).value == D("1311.75")
    assert worksheet.get(RC381_PART_3_LINE_23).value == D("265.00")
    assert worksheet.get(RC381_PART_3_LINE_27).value == D("0.00")
    assert worksheet.get(RC381_PART_3_LINE_38).value == D("0.00")
    assert worksheet.get(RC381_PART_3_LINE_40).value == D("1350.00")
    assert worksheet.get(RC381_PART_3_LINE_41).value == D("250.00")
    assert worksheet.get(RC381_PART_3_LINE_42).value == D("0.00")
    assert worksheet.get(RC381_PART_3_LINE_43).value == D("0.00")
    assert worksheet.get(RC381_PART_3_LINE_49).value == D("1350.00")
    assert worksheet.get(RC381_PART_3_LINE_52).value == D("1311.75")
    assert worksheet.get(RC381_PART_3_LINE_53).value == D("38.25")
    assert worksheet.get(RC381_PART_3_LINE_56).value == D("250.00")
    assert worksheet.get(RC381_PART_3_LINE_59).value == D("265.00")
    assert worksheet.get(RC381_PART_3_LINE_60).value == D("-15.00")
    assert worksheet.get(RC381_PART_3_LINE_61).value == D("23.25")
    assert worksheet.get(RC381_PART_3_LINE_69).value == D("23.25")


def test_return_bo_line_68_is_negative_when_actual_is_less_than_required() -> None:
    # Line 1 is 50,000 and line 2 is 40,000 with box 16A and box 17A of 0: line 26 = 220.00 and
    # line 46 = 176.00, so line 67 = 396.00 and line 64 = 0.00: line 68 = -396.00. Line 61 is
    # -669.70 (line 53 -579.93, line 60 -89.77), so line 69 = -669.70 + -396.00 = -1,065.70.
    worksheet = return_bo(line_1="50000", line_2="40000", line_19="3500.00", line_39="0")

    assert worksheet.get(RC381_PART_3_LINE_26).value == D("220.00")
    assert worksheet.get(RC381_PART_3_LINE_46).value == D("176.00")
    assert worksheet.get(RC381_PART_3_LINE_53).value == D("-579.93")
    assert worksheet.get(RC381_PART_3_LINE_60).value == D("-89.77")
    assert worksheet.get(RC381_PART_3_LINE_61).value == D("-669.70")
    assert worksheet.get(RC381_PART_3_LINE_64).value == D("0")
    assert worksheet.get(RC381_PART_3_LINE_67).value == D("396.00")
    assert worksheet.get(RC381_PART_3_LINE_68).value == D("-396.00")
    assert worksheet.get(RC381_PART_3_LINE_69).value == D("-1065.70")


def test_return_bo_line_68_is_positive_when_actual_is_more_than_required() -> None:
    # Line 1 is 40,000 and line 2 is 40,000 (box 16 of 3,000.00, box 16A of 200.00, box 17 of
    # 3,000.00 and box 17A of 300.00): line 15 = 4,350.00 and line 35 = 4,350.00, so line 26 =
    # line 46 = 174.00 and line 67 = 348.00; line 64 = 200.00 + 300.00 = 500.00 and line 68 =
    # 152.00. Line 61 = 1,813.35, so line 69 = 1,965.35.
    worksheet = return_bo(
        line_1="40000",
        line_2="40000",
        line_19="3000.00",
        line_39="3000.00",
        line_25="200.00",
        line_45="300.00",
    )

    assert worksheet.get(RC381_PART_3_LINE_15).value == D("4350.00")
    assert worksheet.get(RC381_PART_3_LINE_26).value == D("174.00")
    assert worksheet.get(RC381_PART_3_LINE_35).value == D("4350.00")
    assert worksheet.get(RC381_PART_3_LINE_46).value == D("174.00")
    assert worksheet.get(RC381_PART_3_LINE_61).value == D("1813.35")
    assert worksheet.get(RC381_PART_3_LINE_64).value == D("500.00")
    assert worksheet.get(RC381_PART_3_LINE_67).value == D("348.00")
    assert worksheet.get(RC381_PART_3_LINE_68).value == D("152.00")
    assert worksheet.get(RC381_PART_3_LINE_69).value == D("1965.35")


def test_return_bo_with_6_and_12_months_lines_27_to_30_read_line_b() -> None:
    # Line A is 6 (lines C to F: 35,650.00, 4,950.00, 40,600.00 and 1,750.00), line B is 12 (lines
    # G to J: 71,300.00, 9,900.00, 81,200.00 and 3,500.00). Line 6 = 0.42857: line 7 = 40,600.00 x
    # 0.42857 = 17,399.94, line 8 = 15,278.52, line 9 = 750.00 and line 10 = 2,121.42. Line 27 =
    # 81,200.00 less 17,399.94 = 63,800.06, line 28 = 71,300.00 less 15,278.52 = 56,021.48, line
    # 29 = 3,500.00 less 750.00 = 2,750.00, line 30 = 9,900.00 less 2,121.42 = 7,778.58. Line 3
    # (70,000.00) is more than line C (35,650.00), so line 15 = 2,121.42 and line 26 = 84.86, but
    # not more than line G (71,300.00), so line 35 is 0. Line 38 = 40,000.00 less 2,750.00 =
    # 37,250.00, line 42 = 2,011.50, line 43 = 372.50. Line 52 = 719.16 + 2,011.50 = 2,730.66,
    # line 53 = 3,606.86 less 2,730.66 = 876.20; line 59 = 145.29 + 372.50 = 517.79, line 60 =
    # 693.14 less 517.79 = 175.35; line 61 = 1,051.55. Line 67 = 84.86 + 0 = 84.86, line 68 =
    # -84.86, so line 69 = 966.69.
    worksheet = return_bo(cpp_months=6, qpp_months=12)

    assert worksheet.get(RC381_PART_3_LINE_7).value == D("17399.94")
    assert worksheet.get(RC381_PART_3_LINE_8).value == D("15278.52")
    assert worksheet.get(RC381_PART_3_LINE_9).value == D("750.00")
    assert worksheet.get(RC381_PART_3_LINE_10).value == D("2121.42")
    assert worksheet.get(RC381_PART_3_LINE_15).value == D("2121.42")
    assert worksheet.get(RC381_PART_3_LINE_26).value == D("84.86")
    assert worksheet.get(RC381_PART_3_LINE_27).value == D("63800.06")
    assert worksheet.get(RC381_PART_3_LINE_28).value == D("56021.48")
    assert worksheet.get(RC381_PART_3_LINE_29).value == D("2750.00")
    assert worksheet.get(RC381_PART_3_LINE_30).value == D("7778.58")
    assert worksheet.get(RC381_PART_3_LINE_31).value == D("40000")
    assert worksheet.get(RC381_PART_3_LINE_34).value == D("0")
    assert worksheet.get(RC381_PART_3_LINE_35_LESSER).value == D("0")
    assert worksheet.get(RC381_PART_3_LINE_35).value == D("0")
    assert worksheet.get(RC381_PART_3_LINE_36).value == D("40000")
    assert worksheet.get(RC381_PART_3_LINE_38).value == D("37250.00")
    assert worksheet.get(RC381_PART_3_LINE_40).value == D("2109.38")
    assert worksheet.get(RC381_PART_3_LINE_41).value == D("390.62")
    assert worksheet.get(RC381_PART_3_LINE_42).value == D("2011.50")
    assert worksheet.get(RC381_PART_3_LINE_43).value == D("372.50")
    assert worksheet.get(RC381_PART_3_LINE_44).value == D("2384.00")
    assert worksheet.get(RC381_PART_3_LINE_46).value == D("0.00")
    assert worksheet.get(RC381_PART_3_LINE_49).value == D("3606.86")
    assert worksheet.get(RC381_PART_3_LINE_52).value == D("2730.66")
    assert worksheet.get(RC381_PART_3_LINE_53).value == D("876.20")
    assert worksheet.get(RC381_PART_3_LINE_56).value == D("693.14")
    assert worksheet.get(RC381_PART_3_LINE_59).value == D("517.79")
    assert worksheet.get(RC381_PART_3_LINE_60).value == D("175.35")
    assert worksheet.get(RC381_PART_3_LINE_61).value == D("1051.55")
    assert worksheet.get(RC381_PART_3_LINE_64).value == D("0")
    assert worksheet.get(RC381_PART_3_LINE_67).value == D("84.86")
    assert worksheet.get(RC381_PART_3_LINE_68).value == D("-84.86")
    assert worksheet.get(RC381_PART_3_LINE_69).value == D("966.69")


# Part 3a and Part 3b (lines 70 to 93, "If your earnings subject to contributions are from
# employment income only and line 69 is: positive, complete Part 3a ... "0", complete Part 3b ...
# negative ... If not, complete Part 3b").

# Part 3b's lines by number ("87h" is the "result of line 68 minus line 80" inside line 87).
PART_3B_KINDS: dict[str, ArtifactKind[Decimal]] = {
    "75": RC381_PART_3_LINE_75,
    "76": RC381_PART_3_LINE_76,
    "77": RC381_PART_3_LINE_77,
    "78": RC381_PART_3_LINE_78,
    "79": RC381_PART_3_LINE_79,
    "80": RC381_PART_3_LINE_80,
    "81": RC381_PART_3_LINE_81,
    "82": RC381_PART_3_LINE_82,
    "83": RC381_PART_3_LINE_83,
    "84": RC381_PART_3_LINE_84,
    "85": RC381_PART_3_LINE_85,
    "86": RC381_PART_3_LINE_86,
    "87h": RC381_PART_3_LINE_87_DIFFERENCE,
    "87": RC381_PART_3_LINE_87,
    "88": RC381_PART_3_LINE_88,
    "89": RC381_PART_3_LINE_89,
    "90": RC381_PART_3_LINE_90,
    "91": RC381_PART_3_LINE_91,
    "92": RC381_PART_3_LINE_92,
    "93": RC381_PART_3_LINE_93,
}


def part_3b(worksheet: Worksheet) -> dict[str, Decimal]:
    """Part 3b's lines 75 to 93 of `worksheet`, by line number."""
    return {line: worksheet.get(kind).value for line, kind in PART_3B_KINDS.items()}


def results(worksheet: Worksheet) -> tuple[Decimal, Decimal, Decimal]:
    """The amounts for line 30800, line 22215 and line 44800 of the return."""
    return (
        worksheet.get(RC381_EMPLOYMENT_CPP_BASE_CONTRIBUTIONS).value,
        worksheet.get(RC381_EMPLOYMENT_CPP_ENHANCED_CONTRIBUTIONS).value,
        worksheet.get(RC381_CPP_OVERPAYMENT).value,
    )


def test_return_bo_part_3a_matches_the_tickets_example() -> None:
    # The ticket's example: line 69 = 172.25 is positive, so Part 3a. Line 70 "Enter the amount
    # from line 52" = 3,462.75, line 71 "Enter the amount from line 59" = 665.00, line 72 "Enter the
    # amount from line 67 (if any)" = 0, line 73 "Line 71 plus line 72" = 665.00 and line 74
    # "Enter the amount from line 69" = 172.25: line 30800 = 3,462.75, line 22215 = 665.00 and
    # line 44800 = 172.25. Lines 70, 71, 72 and 74 only copy lines 52, 59, 67 and 69.
    worksheet = return_bo()

    assert worksheet.get(RC381_PART_3_LINE_52).value == D("3462.75")
    assert worksheet.get(RC381_PART_3_LINE_59).value == D("665.00")
    assert worksheet.get(RC381_PART_3_LINE_67).value == D("0")
    assert worksheet.get(RC381_PART_3_LINE_73).value == D("665.00")
    assert worksheet.get(RC381_PART_3_LINE_69).value == D("172.25")
    assert results(worksheet) == (D("3462.75"), D("665.00"), D("172.25"))


def test_return_bo_line_73_is_line_71_plus_line_72() -> None:
    # Line 40,000 and 40,000 with box 16 and box 17 of 3,000.00 each: line 52 = 1,678.05 + 1,830.60
    # = 3,508.65, line 59 = 339.00 + 339.00 = 678.00, line 67 = 174.00 + 174.00 = 348.00 and line
    # 64 = 0, so line 68 = -348.00 and line 61 = 1,518.40 + 294.95 = 1,813.35: line 69 = 1,465.35,
    # positive. Part 3a: line 73 = 678.00 + 348.00 = 1,026.00, so line 30800 = 3,508.65, line 22215
    # = 1,026.00 and line 44800 = 1,465.35.
    worksheet = return_bo(line_1="40000", line_2="40000", line_19="3000.00", line_39="3000.00")

    assert worksheet.get(RC381_PART_3_LINE_52).value == D("3508.65")
    assert worksheet.get(RC381_PART_3_LINE_59).value == D("678.00")
    assert worksheet.get(RC381_PART_3_LINE_67).value == D("348.00")
    assert worksheet.get(RC381_PART_3_LINE_68).value == D("-348.00")
    assert worksheet.get(RC381_PART_3_LINE_69).value == D("1465.35")
    assert worksheet.get(RC381_PART_3_LINE_73).value == D("1026.00")
    assert results(worksheet) == (D("3508.65"), D("1026.00"), D("1465.35"))


def test_return_bo_part_3a_with_second_additional_contributions_paid() -> None:
    # The same T4 totals with box 16A of 200.00 and box 17A of 300.00: line 64 = 500.00, line 68 =
    # 152.00, line 69 = 1,813.35 + 152.00 = 1,965.35. Line 73 is still 678.00 + 348.00 = 1,026.00.
    worksheet = return_bo(
        line_1="40000",
        line_2="40000",
        line_19="3000.00",
        line_39="3000.00",
        line_25="200.00",
        line_45="300.00",
    )

    assert worksheet.get(RC381_PART_3_LINE_69).value == D("1965.35")
    assert results(worksheet) == (D("3508.65"), D("1026.00"), D("1965.35"))


def test_return_bo_part_3a_ignores_a_negative_line_53() -> None:
    # Line 1 = 0, line 2 = 40,000, box 16 = 2,300.00 (as in the line 53 test above): line 53 =
    # -57.55, line 60 = 21.55, line 61 = -36.00. With box 16A of 500.00 line 64 = 500.00 and line 68
    # = 500.00 less line 67 (0) = 500.00: line 69 = -36.00 + 500.00 = 464.00, positive, so Part 3a
    # takes line 52 (1,971.00), line 59 + line 67 (365.00 + 0) and line 69 whatever line 53 is.
    worksheet = return_bo(
        line_1="0", line_2="40000", line_19="2300.00", line_39="0", line_25="500.00"
    )

    assert worksheet.get(RC381_PART_3_LINE_53).value == D("-57.55")
    assert worksheet.get(RC381_PART_3_LINE_69).value == D("464.00")
    assert results(worksheet) == (D("1971.00"), D("365.00"), D("464.00"))


def test_return_bo_a_line_69_of_one_cent_is_positive_and_takes_part_3a() -> None:
    # Box 16 of 1,695.20 and box 17 of 2,432.56 (chosen figures): line 20 = 1,695.20 x 83.1933% =
    # 1,410.29 (1,410.2886), line 40 = 2,432.56 x 84.375% = 2,052.47 (2,052.4725); line 49 =
    # 3,462.76 against line 52 = 3,462.75, so line 53 = 0.01. Line 21 = 284.91 and line 41 =
    # 380.09: line 56 = 665.00 = line 59, line 60 = 0 and line 68 = 0, so line 69 = 0.01.
    worksheet = return_bo(line_19="1695.20", line_39="2432.56")

    assert worksheet.get(RC381_PART_3_LINE_49).value == D("3462.76")
    assert worksheet.get(RC381_PART_3_LINE_56).value == D("665.00")
    assert worksheet.get(RC381_PART_3_LINE_69).value == D("0.01")
    assert results(worksheet) == (D("3462.75"), D("665.00"), D("0.01"))


def test_return_bo_a_line_69_of_zero_takes_part_3b_with_lines_53_60_and_68_all_zero() -> None:
    # Box 16 of 1,695.20 and box 17 of 2,432.55 (chosen figures): line 20 = 1,410.29, line 40 =
    # 2,052.46 (2,052.4640), line 49 = 3,462.75 = line 52, line 53 = 0. Line 21 = 284.91 and line 41
    # = 380.09: line 56 = 665.00 = line 59, line 60 = 0; line 64 = line 67 = 0, line 68 = 0, so
    # line 69 = 0: Part 3b. Line 53 is "positive or 0": line 75 = line 52 = 3,462.75; line 76 = 0,
    # lines 77, 78, 80 = 0, line 79 = 3,462.75 and line 81 = 3,462.75. Line 60 is "positive or 0":
    # line 82 = line 59 = 665.00, lines 83, 84, 85, 87 = 0, line 86 = line 88 = 665.00. Line 68 is
    # "positive or 0": line 89 = line 67 = 0, lines 90, 91 = 0, line 92 = 0, line 93 = 665.00.
    # Part 3b has no overpayment, so line 44800 is 0.
    worksheet = return_bo(line_19="1695.20", line_39="2432.55")

    assert worksheet.get(RC381_PART_3_LINE_53).value == D("0.00")
    assert worksheet.get(RC381_PART_3_LINE_60).value == D("0.00")
    assert worksheet.get(RC381_PART_3_LINE_68).value == D("0.00")
    assert worksheet.get(RC381_PART_3_LINE_69).value == D("0.00")
    assert part_3b(worksheet) == {
        "75": D("3462.75"),
        "76": D("0"),
        "77": D("0"),
        "78": D("0"),
        "79": D("3462.75"),
        "80": D("0"),
        "81": D("3462.75"),
        "82": D("665.00"),
        "83": D("0"),
        "84": D("0"),
        "85": D("0"),
        "86": D("665.00"),
        "87h": D("0"),
        "87": D("0"),
        "88": D("665.00"),
        "89": D("0"),
        "90": D("0"),
        "91": D("0"),
        "92": D("0"),
        "93": D("665.00"),
    }
    assert results(worksheet) == (D("3462.75"), D("665.00"), D("0"))


def test_return_bo_part_3b_with_line_53_negative_and_line_60_positive_adds_line_77_to_line_75() -> (
    None
):
    # Box 16 of 4,127.75 and no box 17: line 20 = 4,127.75 x 83.1933% = 3,434.01 (3,434.0116) and
    # line 21 = 693.74, so line 49 = 3,434.01, line 53 = 3,434.01 less 3,462.75 = -28.74; line 56 =
    # 693.74, line 60 = 693.74 less 665.00 = 28.74. Line 61 = 0 and line 68 = 0, so line 69 = 0:
    # Part 3b. Line 53 is negative: line 75 = line 49 = 3,434.01, line 76 = 28.74. Line 60 is
    # positive: line 77 = the lesser of 28.74 and 28.74 = 28.74, line 78 = 0, line 79 = 3,434.01 +
    # 28.74 = 3,462.75, line 80 = 0 (line 68 is 0), line 81 = 3,462.75. Line 60 is positive: line
    # 82 = line 59 = 665.00 and lines 83 to 85 = 0; line 88 = 665.00; line 89 = line 67 = 0 and line
    # 93 = 665.00. The base is made up to the required base from the first additional.
    worksheet = return_bo(line_19="4127.75", line_39="0")

    assert worksheet.get(RC381_PART_3_LINE_49).value == D("3434.01")
    assert worksheet.get(RC381_PART_3_LINE_53).value == D("-28.74")
    assert worksheet.get(RC381_PART_3_LINE_56).value == D("693.74")
    assert worksheet.get(RC381_PART_3_LINE_60).value == D("28.74")
    assert worksheet.get(RC381_PART_3_LINE_69).value == D("0.00")
    assert part_3b(worksheet) == {
        "75": D("3434.01"),
        "76": D("28.74"),
        "77": D("28.74"),
        "78": D("0"),
        "79": D("3462.75"),
        "80": D("0"),
        "81": D("3462.75"),
        "82": D("665.00"),
        "83": D("0"),
        "84": D("0"),
        "85": D("0"),
        "86": D("665.00"),
        "87h": D("0"),
        "87": D("0"),
        "88": D("665.00"),
        "89": D("0"),
        "90": D("0"),
        "91": D("0"),
        "92": D("0"),
        "93": D("665.00"),
    }
    assert results(worksheet) == (D("3462.75"), D("665.00"), D("0"))


def test_return_bo_part_3b_with_line_53_positive_and_line_60_negative_adds_line_84_to_line_82() -> (
    None
):
    # No box 16 and box 17 of 4,127.75: line 40 = 4,127.75 x 84.375% = 3,482.79 (3,482.7890), line
    # 41 = 644.96; line 53 = 3,482.79 less 3,462.75 = 20.04, line 60 = 644.96 less 665.00 = -20.04,
    # line 61 = 0, line 69 = 0: Part 3b. Line 53 is positive: line 75 = line 52 = 3,462.75, lines
    # 76 to 80 = 0, line 81 = 3,462.75. Line 60 is negative: line 82 = line 56 = 644.96, line 83 =
    # 20.04, line 84 = the lesser of 20.04 and 20.04 = 20.04, line 85 = 0, line 86 = 644.96 +
    # 20.04 = 665.00, line 87 = 0, line 88 = 665.00, line 93 = 665.00 + 0.
    worksheet = return_bo(line_19="0", line_39="4127.75")

    assert worksheet.get(RC381_PART_3_LINE_53).value == D("20.04")
    assert worksheet.get(RC381_PART_3_LINE_56).value == D("644.96")
    assert worksheet.get(RC381_PART_3_LINE_60).value == D("-20.04")
    assert worksheet.get(RC381_PART_3_LINE_69).value == D("0.00")
    assert part_3b(worksheet) == {
        "75": D("3462.75"),
        "76": D("0"),
        "77": D("0"),
        "78": D("0"),
        "79": D("3462.75"),
        "80": D("0"),
        "81": D("3462.75"),
        "82": D("644.96"),
        "83": D("20.04"),
        "84": D("20.04"),
        "85": D("0"),
        "86": D("665.00"),
        "87h": D("0"),
        "87": D("0"),
        "88": D("665.00"),
        "89": D("0"),
        "90": D("0"),
        "91": D("0"),
        "92": D("0"),
        "93": D("665.00"),
    }
    assert results(worksheet) == (D("3462.75"), D("665.00"), D("0"))


def test_return_bo_part_3b_with_no_contributions_paid_gives_zero_for_both_results() -> None:
    # No box 16 or box 17: line 49 = 0, line 53 = -3,462.75; line 56 = 0, line 60 = -665.00; line 69
    # = -4,127.75, negative, so Part 3b ("If not, complete Part 3b"). Line 53 is negative: line 75 =
    # line 49 = 0; line 76 = 3,462.75; line 60 is negative, not positive, so line 77 = "0"; line 78
    # = 3,462.75; line 79 = 0; line 68 is 0, so line 80 = "0"; line 81 = 0. Line 60 is negative:
    # line 82 = line 56 = 0; line 83 = 665.00; line 53 is negative, not positive, so line 84 = "0";
    # line 85 = 665.00; line 86 = 0; line 87 = 0 (line 68 is 0); line 88 = 0; line 93 = 0.
    worksheet = return_bo(line_19="0", line_39="0")

    assert worksheet.get(RC381_PART_3_LINE_69).value == D("-4127.75")
    assert part_3b(worksheet) == {
        "75": D("0"),
        "76": D("3462.75"),
        "77": D("0"),
        "78": D("3462.75"),
        "79": D("0"),
        "80": D("0"),
        "81": D("0"),
        "82": D("0"),
        "83": D("665.00"),
        "84": D("0"),
        "85": D("665.00"),
        "86": D("0"),
        "87h": D("0"),
        "87": D("0"),
        "88": D("0"),
        "89": D("0"),
        "90": D("0"),
        "91": D("0"),
        "92": D("0"),
        "93": D("0"),
    }
    assert results(worksheet) == (D("0"), D("0"), D("0"))


def test_return_bo_part_3b_with_lines_53_and_60_both_negative_gives_the_actual_contributions() -> (
    None
):
    # No box 16 and box 17 of 4,000.00: line 40 = 4,000.00 x 84.375% = 3,375.00, line 41 = 625.00;
    # line 53 = 3,375.00 less 3,462.75 = -87.75, line 60 = 625.00 less 665.00 = -40.00, line 61 =
    # -127.75, line 69 = -127.75. Line 75 = line 49 = 3,375.00, line 76 = 87.75, line 77 = "0" (line
    # 60 is not positive), line 78 = 87.75, line 79 = 3,375.00, line 80 = "0" (line 68 is 0), line
    # 81 = 3,375.00. Line 82 = line 56 = 625.00, line 83 = 40.00, line 84 = "0" (line 53 is not
    # positive), line 85 = 40.00, line 86 = 625.00, line 87 = "0", line 88 = 625.00, line 93 =
    # 625.00.
    worksheet = return_bo(line_19="0", line_39="4000.00")

    assert worksheet.get(RC381_PART_3_LINE_53).value == D("-87.75")
    assert worksheet.get(RC381_PART_3_LINE_60).value == D("-40.00")
    assert worksheet.get(RC381_PART_3_LINE_69).value == D("-127.75")
    assert part_3b(worksheet) == {
        "75": D("3375.00"),
        "76": D("87.75"),
        "77": D("0"),
        "78": D("87.75"),
        "79": D("3375.00"),
        "80": D("0"),
        "81": D("3375.00"),
        "82": D("625.00"),
        "83": D("40.00"),
        "84": D("0"),
        "85": D("40.00"),
        "86": D("625.00"),
        "87h": D("0"),
        "87": D("0"),
        "88": D("625.00"),
        "89": D("0"),
        "90": D("0"),
        "91": D("0"),
        "92": D("0"),
        "93": D("625.00"),
    }
    assert results(worksheet) == (D("3375.00"), D("625.00"), D("0"))


def test_return_bo_part_3b_line_80_is_line_68_when_line_53_is_negative_and_line_60_positive() -> (
    None
):
    # Box 16 of 4,100.00, no box 17, box 16A of 20.00: line 20 = 3,410.93 (3,410.9253), line 21 =
    # 689.07; line 53 = 3,410.93 less 3,462.75 = -51.82, line 60 = 689.07 less 665.00 = 24.07, line
    # 61 = -27.75; line 64 = 20.00, line 67 = 0, line 68 = 20.00, line 69 = -7.75: Part 3b. Line
    # 75 = line 49 = 3,410.93, line 76 = 51.82, line 77 = the lesser of 24.07 and 51.82 = 24.07,
    # line 78 = 27.75, line 79 = 3,435.00. Line 68 and line 78 are both positive: line 80 = the
    # lesser of 20.00 and 27.75 = 20.00, line 81 = 3,455.00. Line 60 is positive: line 82 = line 59
    # = 665.00, lines 83 to 85 = 0, line 86 = 665.00, line 87 = "0" (line 85 is 0), line 88 =
    # 665.00. Line 68 is positive: line 89 = line 67 = 0, line 92 = 0, line 93 = 665.00.
    worksheet = return_bo(line_19="4100.00", line_39="0", line_25="20.00")

    assert worksheet.get(RC381_PART_3_LINE_53).value == D("-51.82")
    assert worksheet.get(RC381_PART_3_LINE_60).value == D("24.07")
    assert worksheet.get(RC381_PART_3_LINE_68).value == D("20.00")
    assert worksheet.get(RC381_PART_3_LINE_69).value == D("-7.75")
    assert part_3b(worksheet) == {
        "75": D("3410.93"),
        "76": D("51.82"),
        "77": D("24.07"),
        "78": D("27.75"),
        "79": D("3435.00"),
        "80": D("20.00"),
        "81": D("3455.00"),
        "82": D("665.00"),
        "83": D("0"),
        "84": D("0"),
        "85": D("0"),
        "86": D("665.00"),
        "87h": D("0"),
        "87": D("0"),
        "88": D("665.00"),
        "89": D("0"),
        "90": D("0"),
        "91": D("0"),
        "92": D("0"),
        "93": D("665.00"),
    }
    assert results(worksheet) == (D("3455.00"), D("665.00"), D("0"))


def test_return_bo_part_3b_line_87_is_line_68_less_line_80_when_that_is_less_than_line_85() -> None:
    # No box 16, box 17 of 4,000.00 (lines 53 = -87.75, 60 = -40.00 as above) and box 16A of 100.00:
    # line 68 = 100.00, line 69 = -127.75 + 100.00 = -27.75: Part 3b. Line 75 = 3,375.00, line 76 =
    # 87.75, line 77 = "0", line 78 = 87.75, line 79 = 3,375.00; lines 68 and 78 both positive:
    # line 80 = the lesser of 100.00 and 87.75 = 87.75, line 81 = 3,462.75. Line 82 = line 56 =
    # 625.00, line 83 = 40.00, line 84 = "0", line 85 = 40.00, line 86 = 625.00; lines 68 and 85
    # both positive: line 87 = the lesser of 40.00 and (100.00 less 87.75 = 12.25) = 12.25, line 88
    # = 637.25. Line 89 = line 67 = 0, line 92 = 0, line 93 = 637.25.
    worksheet = return_bo(line_19="0", line_39="4000.00", line_25="100.00")

    assert worksheet.get(RC381_PART_3_LINE_68).value == D("100.00")
    assert worksheet.get(RC381_PART_3_LINE_69).value == D("-27.75")
    assert part_3b(worksheet) == {
        "75": D("3375.00"),
        "76": D("87.75"),
        "77": D("0"),
        "78": D("87.75"),
        "79": D("3375.00"),
        "80": D("87.75"),
        "81": D("3462.75"),
        "82": D("625.00"),
        "83": D("40.00"),
        "84": D("0"),
        "85": D("40.00"),
        "86": D("625.00"),
        "87h": D("12.25"),
        "87": D("12.25"),
        "88": D("637.25"),
        "89": D("0"),
        "90": D("0"),
        "91": D("0"),
        "92": D("0"),
        "93": D("637.25"),
    }
    assert results(worksheet) == (D("3462.75"), D("637.25"), D("0"))


def test_return_bo_part_3b_line_87_is_zero_when_line_80_takes_all_of_line_68() -> None:
    # The same T4 totals with box 16A of 50.00: line 68 = 50.00, line 69 = -127.75 + 50.00 =
    # -77.75. Lines 68 and 78 (87.75) are both positive: line 80 = the lesser of 50.00 and 87.75 =
    # 50.00, line 81 = 3,375.00 + 50.00 = 3,425.00. Lines 68 and 85 (40.00) are both positive, but
    # line 68 less line 80 is 0, so the lesser of 40.00 and 0 is 0: line 87 = 0, line 88 = 625.00.
    worksheet = return_bo(line_19="0", line_39="4000.00", line_25="50.00")

    assert worksheet.get(RC381_PART_3_LINE_68).value == D("50.00")
    assert worksheet.get(RC381_PART_3_LINE_69).value == D("-77.75")
    assert part_3b(worksheet) == {
        "75": D("3375.00"),
        "76": D("87.75"),
        "77": D("0"),
        "78": D("87.75"),
        "79": D("3375.00"),
        "80": D("50.00"),
        "81": D("3425.00"),
        "82": D("625.00"),
        "83": D("40.00"),
        "84": D("0"),
        "85": D("40.00"),
        "86": D("625.00"),
        "87h": D("0"),
        "87": D("0"),
        "88": D("625.00"),
        "89": D("0"),
        "90": D("0"),
        "91": D("0"),
        "92": D("0"),
        "93": D("625.00"),
    }
    assert results(worksheet) == (D("3425.00"), D("625.00"), D("0"))


def test_return_bo_part_3b_line_87_with_line_53_positive_is_all_of_line_68() -> None:
    # No box 16, box 17 of 4,110.00 and box 16A of 10.00: line 40 = 3,467.81 (3,467.8125), line 41 =
    # 642.19; line 53 = 3,467.81 less 3,462.75 = 5.06, line 60 = 642.19 less 665.00 = -22.81, line
    # 61 = -17.75; line 68 = 10.00, line 69 = -7.75: Part 3b. Line 53 is positive: line 75 = line
    # 52 = 3,462.75, line 76 = 0, line 77 = 0, line 78 = 0, line 79 = 3,462.75; line 78 is not
    # positive, so line 80 = "0", line 81 = 3,462.75. Line 60 is negative: line 82 = line 56 =
    # 642.19, line 83 = 22.81, line 84 = the lesser of 5.06 and 22.81 = 5.06, line 85 = 17.75, line
    # 86 = 647.25; lines 68 and 85 both positive: line 87 = the lesser of 17.75 and (10.00 less 0
    # = 10.00) = 10.00, line 88 = 657.25. Line 89 = line 67 = 0, line 93 = 657.25.
    worksheet = return_bo(line_19="0", line_39="4110.00", line_25="10.00")

    assert worksheet.get(RC381_PART_3_LINE_53).value == D("5.06")
    assert worksheet.get(RC381_PART_3_LINE_60).value == D("-22.81")
    assert worksheet.get(RC381_PART_3_LINE_68).value == D("10.00")
    assert worksheet.get(RC381_PART_3_LINE_69).value == D("-7.75")
    assert part_3b(worksheet) == {
        "75": D("3462.75"),
        "76": D("0"),
        "77": D("0"),
        "78": D("0"),
        "79": D("3462.75"),
        "80": D("0"),
        "81": D("3462.75"),
        "82": D("642.19"),
        "83": D("22.81"),
        "84": D("5.06"),
        "85": D("17.75"),
        "86": D("647.25"),
        "87h": D("10.00"),
        "87": D("10.00"),
        "88": D("657.25"),
        "89": D("0"),
        "90": D("0"),
        "91": D("0"),
        "92": D("0"),
        "93": D("657.25"),
    }
    assert results(worksheet) == (D("3462.75"), D("657.25"), D("0"))


def test_return_bo_part_3b_with_line_68_negative_and_line_61_positive_adds_line_91() -> None:
    # Lines 1 and 2 of 40,000 (line 52 = 3,508.65, line 59 = 678.00, line 67 = 348.00), no box 16
    # and box 17 of 4,300.00: line 40 = 3,628.13 (3,628.125), line 41 = 671.87; line 53 = 119.48,
    # line 60 = 671.87 less 678.00 = -6.13, line 61 = 113.35; line 64 = 0, line 68 = -348.00, line
    # 69 = 113.35 - 348.00 = -234.65: Part 3b. Line 53 is positive: line 75 = 3,508.65, lines 76 to
    # 80 = 0, line 81 = 3,508.65. Line 60 is negative: line 82 = line 56 = 671.87, line 83 = 6.13,
    # line 84 = the lesser of 119.48 and 6.13 = 6.13, line 85 = 0, line 86 = 678.00; line 68 is
    # negative, so line 87 = "0"; line 88 = 678.00. Line 68 is negative: line 89 = line 64 = 0, line
    # 90 = 348.00, line 61 is positive: line 91 = the lesser of 113.35 and 348.00 = 113.35, line 92
    # = 113.35, line 93 = 678.00 + 113.35 = 791.35.
    worksheet = return_bo(line_1="40000", line_2="40000", line_19="0", line_39="4300.00")

    assert worksheet.get(RC381_PART_3_LINE_61).value == D("113.35")
    assert worksheet.get(RC381_PART_3_LINE_68).value == D("-348.00")
    assert worksheet.get(RC381_PART_3_LINE_69).value == D("-234.65")
    assert part_3b(worksheet) == {
        "75": D("3508.65"),
        "76": D("0"),
        "77": D("0"),
        "78": D("0"),
        "79": D("3508.65"),
        "80": D("0"),
        "81": D("3508.65"),
        "82": D("671.87"),
        "83": D("6.13"),
        "84": D("6.13"),
        "85": D("0"),
        "86": D("678.00"),
        "87h": D("-348.00"),
        "87": D("0"),
        "88": D("678.00"),
        "89": D("0"),
        "90": D("348.00"),
        "91": D("113.35"),
        "92": D("113.35"),
        "93": D("791.35"),
    }
    assert results(worksheet) == (D("3508.65"), D("791.35"), D("0"))


def test_return_bo_part_3b_line_89_is_line_64_when_line_68_is_negative() -> None:
    # The same lines 1 and 2 with box 17 of 4,386.65 and box 16A of 100.00: line 40 = 3,701.24
    # (3,701.2397), line 41 = 685.41; line 53 = 192.59, line 60 = 7.41, line 61 = 200.00; line 64 =
    # 100.00, line 67 = 348.00, line 68 = -248.00, line 69 = -48.00: Part 3b. Line 75 = line 52 =
    # 3,508.65, line 81 = 3,508.65. Line 60 is positive: line 82 = line 59 = 678.00, line 88 =
    # 678.00. Line 68 is negative: line 89 = line 64 = 100.00; line 90 = 248.00; line 61 is
    # positive: line 91 = the lesser of 200.00 and 248.00 = 200.00; line 92 = 300.00; line 93 =
    # 678.00 + 300.00 = 978.00.
    worksheet = return_bo(
        line_1="40000", line_2="40000", line_19="0", line_39="4386.65", line_25="100.00"
    )

    assert worksheet.get(RC381_PART_3_LINE_61).value == D("200.00")
    assert worksheet.get(RC381_PART_3_LINE_64).value == D("100.00")
    assert worksheet.get(RC381_PART_3_LINE_68).value == D("-248.00")
    assert worksheet.get(RC381_PART_3_LINE_69).value == D("-48.00")
    assert part_3b(worksheet) == {
        "75": D("3508.65"),
        "76": D("0"),
        "77": D("0"),
        "78": D("0"),
        "79": D("3508.65"),
        "80": D("0"),
        "81": D("3508.65"),
        "82": D("678.00"),
        "83": D("0"),
        "84": D("0"),
        "85": D("0"),
        "86": D("678.00"),
        "87h": D("-248.00"),
        "87": D("0"),
        "88": D("678.00"),
        "89": D("100.00"),
        "90": D("248.00"),
        "91": D("200.00"),
        "92": D("300.00"),
        "93": D("978.00"),
    }
    assert results(worksheet) == (D("3508.65"), D("978.00"), D("0"))


def test_return_bo_part_3a_and_3b_steps_are_the_form_capabilities() -> None:
    worksheet = return_bo()

    for kind in (
        RC381_PART_3_LINE_73,
        RC381_PART_3_LINE_79,
        RC381_PART_3_LINE_81,
        RC381_PART_3_LINE_86,
        RC381_PART_3_LINE_88,
        RC381_PART_3_LINE_92,
        RC381_PART_3_LINE_93,
    ):
        assert isinstance(worksheet.producer_of(kind), Sum), kind.identifier
    for kind in (
        RC381_PART_3_LINE_78,
        RC381_PART_3_LINE_85,
        RC381_PART_3_LINE_87_DIFFERENCE,
    ):
        assert isinstance(worksheet.producer_of(kind), Subtract), kind.identifier
    for kind in (RC381_PART_3_LINE_76, RC381_PART_3_LINE_83, RC381_PART_3_LINE_90):
        assert isinstance(worksheet.producer_of(kind), PositivePartOfNegation), kind.identifier
    for kind in (
        RC381_PART_3_LINE_77,
        RC381_PART_3_LINE_80,
        RC381_PART_3_LINE_84,
        RC381_PART_3_LINE_87,
        RC381_PART_3_LINE_91,
    ):
        assert isinstance(worksheet.producer_of(kind), LesserOfWhenPositive), kind.identifier
    for kind in (
        RC381_PART_3_LINE_75,
        RC381_PART_3_LINE_82,
        RC381_PART_3_LINE_89,
        RC381_EMPLOYMENT_CPP_BASE_CONTRIBUTIONS,
        RC381_EMPLOYMENT_CPP_ENHANCED_CONTRIBUTIONS,
    ):
        assert isinstance(worksheet.producer_of(kind), ChooseBySign), kind.identifier
    # Line 74 "Enter the amount from line 69" is the sign's own amount, so line 44800 is line 69
    # not below zero.
    assert isinstance(worksheet.producer_of(RC381_CPP_OVERPAYMENT), SumNotBelowZero)


# A return with no Quebec figures.


def test_a_return_with_no_quebec_figures_is_unchanged_and_rc381_part_3_is_zero() -> None:
    # Employment income of 60,000 and none of the Quebec figures: the T1 lines are Schedule 8's,
    # base contributions 4.95% x (60,000 less 3,500) = 2,796.75 and enhanced 1% x 56,500 = 565.00.
    # The T4 box 16 total is the Schedule 8 Part 3 line 8 input, here the required 3,361.75, so
    # line 20 (83.1933% of it) is the base contributions 2,796.75 and line 21 the enhanced 565.00;
    # lines 49, 53, 56, 60, 61 and 69 carry those actual figures (the required figures being 0, as
    # no pensionable earnings are entered), as does line 44800's overpayment; every other Part 3
    # line is 0.
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
        RC381_PART_3_LINE_22,
        RC381_PART_3_LINE_23,
        RC381_PART_3_LINE_24,
        RC381_PART_3_LINE_26,
        RC381_PART_3_LINE_31,
        RC381_PART_3_LINE_34,
        RC381_PART_3_LINE_35_LESSER,
        RC381_PART_3_LINE_35,
        RC381_PART_3_LINE_36,
        RC381_PART_3_LINE_38,
        RC381_PART_3_LINE_40,
        RC381_PART_3_LINE_41,
        RC381_PART_3_LINE_42,
        RC381_PART_3_LINE_43,
        RC381_PART_3_LINE_44,
        RC381_PART_3_LINE_46,
        RC381_PART_3_LINE_52,
        RC381_PART_3_LINE_59,
        RC381_PART_3_LINE_64,
        RC381_PART_3_LINE_67,
        RC381_PART_3_LINE_68,
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
        RC381_PART_3_LINE_87_DIFFERENCE,
        RC381_PART_3_LINE_87,
        RC381_PART_3_LINE_88,
        RC381_PART_3_LINE_89,
        RC381_PART_3_LINE_90,
        RC381_PART_3_LINE_91,
        RC381_PART_3_LINE_92,
        RC381_PART_3_LINE_93,
        RC381_EMPLOYMENT_CPP_BASE_CONTRIBUTIONS,
        RC381_EMPLOYMENT_CPP_ENHANCED_CONTRIBUTIONS,
    )
    assert worksheet.get(RC381_PART_3_LINE_20).value == D("2796.75")
    assert worksheet.get(RC381_PART_3_LINE_21).value == D("565.00")
    assert worksheet.get(RC381_PART_3_LINE_6).value == Rate(D("0"))
    assert worksheet.get(RC381_PART_3_LINE_49).value == D("2796.75")
    assert worksheet.get(RC381_PART_3_LINE_53).value == D("2796.75")
    assert worksheet.get(RC381_PART_3_LINE_56).value == D("565.00")
    assert worksheet.get(RC381_PART_3_LINE_60).value == D("565.00")
    assert worksheet.get(RC381_PART_3_LINE_61).value == D("3361.75")
    assert worksheet.get(RC381_PART_3_LINE_69).value == D("3361.75")
    # Line 69 is positive, so Part 3a's line 44800 result is it; the other two results are lines
    # 52 and 73, which are 0 as no pensionable earnings are entered.
    assert worksheet.get(RC381_CPP_OVERPAYMENT).value == D("3361.75")
    # Lines 27 to 30 are the QPP row of the table less lines 7 to 10, which are 0.
    assert worksheet.get(RC381_PART_3_LINE_27).value == D("81200.00")
    assert worksheet.get(RC381_PART_3_LINE_28).value == D("71300.00")
    assert worksheet.get(RC381_PART_3_LINE_29).value == D("3500.00")
    assert worksheet.get(RC381_PART_3_LINE_30).value == D("9900.00")
    for kind in kinds:
        assert worksheet.get(kind).value == D("0"), kind.identifier


def test_the_rc381_figures_do_not_change_the_t1_lines_yet() -> None:
    # This part of Form RC381 reaches no line of the return: the same employment income and T4 box
    # 16 total (which Schedule 8 reads too) with and without the pensionable earnings totals and the
    # T4 box 17 total gives the same Schedule 8 contributions, net income and total payable.
    with_totals = return_bo()
    without_totals = return_bo(line_1="0", line_2="0", line_39="0")

    for kind in (CPP_BASE_CONTRIBUTIONS, CPP_ENHANCED_CONTRIBUTIONS, NET_INCOME, TOTAL_PAYABLE):
        assert with_totals.get(kind).value == without_totals.get(kind).value, kind.identifier
