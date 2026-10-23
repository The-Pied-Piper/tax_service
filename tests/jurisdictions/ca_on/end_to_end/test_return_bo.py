"""CA-ON 2025 end to end: return bo (Form RC381 Part 2, Part 3 lines 1 to 93 and Part 4 lines 1
to 110)."""

from __future__ import annotations

from decimal import Decimal
from typing import Any

import pytest

from app.domain.artifact import ArtifactKind
from app.domain.capabilities.amount_by_count import AmountForCount
from app.domain.capabilities.apply_fraction import ApplyFraction
from app.domain.capabilities.apply_rate import ApplyRate
from app.domain.capabilities.contribution_tier import TieredContribution
from app.domain.capabilities.lesser_of import LesserOf
from app.domain.capabilities.subtract import Subtract
from app.domain.capabilities.subtract_not_below_zero import SubtractNotBelowZero
from app.domain.capabilities.sum import Sum
from app.domain.capabilities.sum_not_below_zero import SumNotBelowZero
from app.domain.errors import InputBelowBoundError, NegativeArtifactError, NoAmountForCountError
from app.domain.parameters.rate import Rate
from app.domain.worksheet import Worksheet
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
    RC381_PART_4_LINE_92,
    RC381_PART_4_LINE_93,
    RC381_PART_4_LINE_94,
    RC381_PART_4_LINE_95,
    RC381_PART_4_LINE_96,
    RC381_PART_4_LINE_97,
    RC381_PART_4_LINE_98,
    RC381_PART_4_LINE_99,
    RC381_PART_4_LINE_100,
    RC381_PART_4_LINE_101,
    RC381_PART_4_LINE_102,
    RC381_PART_4_LINE_103,
    RC381_PART_4_LINE_104,
    RC381_PART_4_LINE_104_DIFFERENCE,
    RC381_PART_4_LINE_105,
    RC381_PART_4_LINE_106,
    RC381_PART_4_LINE_107,
    RC381_PART_4_LINE_108,
    RC381_PART_4_LINE_109,
    RC381_PART_4_LINE_110,
    RC381_SELF_EMPLOYMENT_CPP_CONTRIBUTIONS,
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
    cpt20_earnings: str = "10000",
    cpt20_t4_earnings: str = "2500",
    net_partnership_income: str = "0",
) -> Worksheet:
    """Return BO's inputs (`returns/2025_return_bo.yaml`): employment income of 70000 on a T4 for
    Ontario employment (box 26 `line_1`, box 16 `line_19`, box 16A `line_25`) and a T4 for Quebec
    employment (box 26 `line_2`, box 17 `line_39`, box 17A `line_45`), and the CPT20 election
    earnings of Part 4 lines 2 and 3 (50373 and 50399)."""
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
        cpt20_earnings=cpt20_earnings,
        cpt20_t4_earnings=cpt20_t4_earnings,
        net_partnership_income=net_partnership_income,
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


# Part 4, lines 1 to 27 (the CPP side before the QPP gross-up, "for residents of a province or
# territory other than Quebec"). Return BO's Part 3 gives line 61 = line 17 + line 20 of Part 4:
# lines 49 + 56 are line 19 + line 39 of Part 3 and lines 52 + 59 are its lines 24 + 44, so line
# 61 = (line 19 - line 24) + (line 39 - line 44), which are Part 4's lines 17 and 20. With Return
# BO's lines 1 and 2 (30,000 and 40,000) Part 3's lines 22, 23, 24 and 44 are 1,410.75, 285.00,
# 1,695.75 and 2,432.00, so box 16 of 1,695.75 and box 17 of 2,432.00 make line 61 "0".

# Part 4's lines by number ("13h" is the "Line 5 minus line 12" printed inside line 13; "21h17" and
# "21h20" the "enter the amount from line 17 (show in brackets)" and "enter whichever is less:
# amount from line 20 or line 17A" printed inside line 21; "23a" and "23b" the lesser and the
# product printed inside line 23; "24h" line 24's "whichever is less", before the block "If line
# 61 of Part 3 is ... negative" decides whether line 24 takes it). Line 22 is a rate.
PART_4_KINDS: dict[str, ArtifactKind[Decimal]] = {
    "8": RC381_PART_4_LINE_8,
    "11": RC381_PART_4_LINE_11,
    "12": RC381_PART_4_LINE_12,
    "13h": RC381_PART_4_LINE_13_DIFFERENCE,
    "13": RC381_PART_4_LINE_13,
    "14": RC381_PART_4_LINE_14,
    "17": RC381_PART_4_LINE_17,
    "17A": RC381_PART_4_LINE_17A,
    "20": RC381_PART_4_LINE_20,
    "21h17": RC381_PART_4_LINE_21_FROM_LINE_17,
    "21h20": RC381_PART_4_LINE_21_LESSER,
    "21": RC381_PART_4_LINE_21,
    "23a": RC381_PART_4_LINE_23_LESSER,
    "23b": RC381_PART_4_LINE_23_MULTIPLIED,
    "23": RC381_PART_4_LINE_23,
    "24h": RC381_PART_4_LINE_24_LESSER,
    "24": RC381_PART_4_LINE_24,
    "25A": RC381_PART_4_LINE_25A,
    "26": RC381_PART_4_LINE_26,
    "27": RC381_PART_4_LINE_27,
}


def part_4(worksheet: Worksheet) -> dict[str, Decimal]:
    """Part 4's lines 8 to 27 of `worksheet`, by line number (line 22 as its rate's value)."""
    lines = {line: worksheet.get(kind).value for line, kind in PART_4_KINDS.items()}
    lines["22"] = worksheet.get(RC381_PART_4_LINE_22).value.value
    return lines


def test_return_bo_part_4_line_4_adds_lines_1_to_3() -> None:
    # Line 1 (the pensionable net self-employment earnings) is 0, line 2 (50373) is 10,000 and
    # line 3 (50399) is 2,500 (chosen election figures): line 4 = 0 + 10,000 + 2,500 = 12,500.
    # Net partnership income of 300 (T1 line 12200) makes line 1 300 and line 4 = 12,800. No
    # election and no earnings: 0. Line 4 prints no floor.
    worksheet = return_bo()

    assert worksheet.get(RC381_PART_4_LINE_4).value == D("12500")
    assert isinstance(worksheet.producer_of(RC381_PART_4_LINE_4), Sum)
    assert return_bo(net_partnership_income="300").get(RC381_PART_4_LINE_4).value == D("12800")
    no_election = return_bo(cpt20_earnings="0", cpt20_t4_earnings="0")
    assert no_election.get(RC381_PART_4_LINE_4).value == D("0")


def test_return_bo_part_4_line_3_cannot_be_negative() -> None:
    # Line 3 (50399) is an amount the filer enters, like line 2: below zero is refused.
    with pytest.raises(NegativeArtifactError, match="cpt20_t4_earnings"):
        return_bo(cpt20_t4_earnings="-1")


def test_return_bo_part_4_with_line_61_positive_completes_lines_6_to_13_only() -> None:
    # Line 61 of Part 3 is 172.25, positive: complete lines 6 to 13 only, continue at line 25. Line
    # 5 = line 19 of Part 3 = 1,800.00. Line 6 (the amount from line 47, Part 3's line 20) 1,497.48
    # less line 7 (line 50, Part 3's line 22) 1,410.75 = 86.73; line 9 (line 54, line 21) 302.52
    # less line 10 (line 57, line 23) 285.00 = 17.52; line 12 = 86.73 + 17.52 = 104.25; line 13 =
    # line 5 less line 12 = 1,800.00 less 104.25 = 1,695.75 (Part 3's line 24). Line 25 is line 13,
    # so line 26 = 0 + 1,695.75 + 0 = 1,695.75 and line 27 = 1,695.75 x 16.80672 = 28,499.9954...,
    # 28,500.00. Lines 14 to 24 are not completed: line 14 = 0, and lines 24 and 25A are 0. Still
    # computed, as every line is: line 17 = 1,800.00 less 1,695.75 = 104.25, so line 17A = 0; line
    # 20 = 2,500.00 less 2,432.00 = 68.00; line 21 is 0 for two positive lines (the form is silent
    # then; its helper "line 17 in brackets" is -104.25); line 22 = 0 (17A is not more than line
    # 14, which is 0); line 23 (line 69 is positive) = the lesser of line 68 (0.00) and 17A (0).
    worksheet = return_bo()

    assert worksheet.get(RC381_PART_3_LINE_61).value == D("172.25")
    assert part_4(worksheet) == {
        "8": D("86.73"),
        "11": D("17.52"),
        "12": D("104.25"),
        "13h": D("1695.75"),
        "13": D("1695.75"),
        "14": D("0"),
        "17": D("104.25"),
        "17A": D("0"),
        "20": D("68.00"),
        "21h17": D("-104.25"),
        "21h20": D("0"),
        "21": D("0"),
        "22": D("0"),
        "23a": D("0.00"),
        "23b": D("0.00"),
        "23": D("0.00"),
        "24h": D("0"),
        "24": D("0"),
        "25A": D("0"),
        "26": D("1695.75"),
        "27": D("28500.00"),
    }


def test_return_bo_part_4_with_line_61_positive_and_line_17_negative_ignores_lines_14_to_25a() -> (
    None
):
    # Box 16 of 1,000 and box 17 of 3,500 (Part 3: line 20 = 831.93, line 21 = 168.07; line 61 =
    # -695.75 + 1,068.00 = 372.25, positive). Line 8 = 831.93 less 1,410.75 = -578.82, line 11 =
    # 168.07 less 285.00 = -116.93, line 12 = -695.75 and line 13 = 1,000 less -695.75 = 1,695.75.
    # Line 17 = 1,000 less 1,695.75 = -695.75, so line 17A = 695.75; line 20 = 3,500 less 2,432.00 =
    # 1,068.00 and line 21 is the lesser of 1,068.00 and 695.75: 695.75, computed. Line 14 is 0,
    # so 17A is more than line 14 and line 22 is 1. But line 61 is positive: lines 24 and 25A are
    # 0 whatever lines 21 and 23 are, so line 26 = line 13 = 1,695.75 and line 27 = 28,500.00.
    worksheet = return_bo(line_19="1000", line_39="3500")

    assert worksheet.get(RC381_PART_3_LINE_61).value == D("372.25")
    assert part_4(worksheet) == {
        "8": D("-578.82"),
        "11": D("-116.93"),
        "12": D("-695.75"),
        "13h": D("1695.75"),
        "13": D("1695.75"),
        "14": D("0"),
        "17": D("-695.75"),
        "17A": D("695.75"),
        "20": D("1068.00"),
        "21h17": D("0"),
        "21h20": D("695.75"),
        "21": D("695.75"),
        "22": D("1"),
        "23a": D("0.00"),
        "23b": D("0.00"),
        "23": D("0.00"),
        "24h": D("0.00"),
        "24": D("0"),
        "25A": D("0"),
        "26": D("1695.75"),
        "27": D("28500.00"),
    }


def test_return_bo_part_4_with_no_t4_contributions_lines_8_11_and_12_are_negative() -> None:
    # No box 16 and box 17 of 4,500 (Part 3: lines 20 and 21 are 0.00; line 61 = -1,695.75 +
    # 2,068.00 = 372.25, positive). Line 8 = 0.00 less 1,410.75 = -1,410.75, line 11 = 0.00 less
    # 285.00 = -285.00, line 12 = -1,695.75 (in brackets); line 13 = line 5 less line 12 = 0 less
    # -1,695.75 = 1,695.75. Line 17 = 0 less 1,695.75 = -1,695.75, so 17A = 1,695.75; line 20 =
    # 4,500 less 2,432.00 = 2,068.00; line 21 = the lesser of 2,068.00 and 1,695.75 = 1,695.75,
    # computed. Line 61 is positive: lines 24 and 25A are 0, line 26 = 1,695.75, line 27 =
    # 28,500.00.
    worksheet = return_bo(line_19="0", line_39="4500")

    assert part_4(worksheet) == {
        "8": D("-1410.75"),
        "11": D("-285.00"),
        "12": D("-1695.75"),
        "13h": D("1695.75"),
        "13": D("1695.75"),
        "14": D("0"),
        "17": D("-1695.75"),
        "17A": D("1695.75"),
        "20": D("2068.00"),
        "21h17": D("0"),
        "21h20": D("1695.75"),
        "21": D("1695.75"),
        "22": D("1"),
        "23a": D("0.00"),
        "23b": D("0.00"),
        "23": D("0.00"),
        "24h": D("0.00"),
        "24": D("0"),
        "25A": D("0"),
        "26": D("1695.75"),
        "27": D("28500.00"),
    }


def test_return_bo_part_4_with_line_61_positive_line_25a_stays_zero_for_a_negative_line_21() -> (
    None
):
    # Box 16 of 2,500 and box 17 of 2,000 (Part 3: line 20 = 2,500 x 83.1933% = 2,079.83, line 21 =
    # 420.17; line 61 = 804.25 - 432.00 = 372.25, positive). Line 8 = 2,079.83 less 1,410.75 =
    # 669.08, line 11 = 420.17 less 285.00 = 135.17, line 12 = 804.25, line 13 = 2,500 less 804.25 =
    # 1,695.75. Line 17 = 2,500 less 1,695.75 = 804.25 (positive), line 20 = 2,000 less 2,432.00 =
    # -432.00: line 21 is the amount from line 17 in brackets, -804.25, computed; but line 61 is
    # positive, so line 25A is 0 and line 26 = 1,695.75.
    worksheet = return_bo(line_19="2500", line_39="2000")

    assert worksheet.get(RC381_PART_3_LINE_61).value == D("372.25")
    assert part_4(worksheet) == {
        "8": D("669.08"),
        "11": D("135.17"),
        "12": D("804.25"),
        "13h": D("1695.75"),
        "13": D("1695.75"),
        "14": D("0"),
        "17": D("804.25"),
        "17A": D("0"),
        "20": D("-432.00"),
        "21h17": D("-804.25"),
        "21h20": D("0"),
        "21": D("-804.25"),
        "22": D("0"),
        "23a": D("0.00"),
        "23b": D("0.00"),
        "23": D("0.00"),
        "24h": D("0"),
        "24": D("0"),
        "25A": D("0"),
        "26": D("1695.75"),
        "27": D("28500.00"),
    }


def test_return_bo_part_4_with_line_61_positive_line_24_stays_zero_for_a_positive_line_23() -> None:
    # The same box 16 of 1,000 and box 17 of 3,500 (line 61 = 372.25, positive) with box 16A of
    # 100.00: line 68 = 100.00 less 0 = 100.00 and line 69 = 372.25 + 100.00 = 472.25, positive, so
    # line 23 is the lesser of line 68 (100.00) and line 17A (695.75): 100.00, and line 24's
    # "whichever is less" is 100.00; but line 61 is positive, so line 24 is 0 and line 26 =
    # line 13 = 1,695.75.
    worksheet = return_bo(line_19="1000", line_39="3500", line_25="100.00")

    assert worksheet.get(RC381_PART_3_LINE_69).value == D("472.25")
    lines = part_4(worksheet)
    assert lines["23"] == D("100.00")
    assert lines["24h"] == D("100.00")
    assert lines["24"] == D("0")
    assert lines["26"] == D("1695.75")


def test_return_bo_part_4_with_line_61_negative_line_17_negative_and_line_20_positive() -> None:
    # Box 16 of 1,000 and box 17 of 3,000 (Part 3: line 20 = 1,000 x 83.1933% = 831.93, line 21 =
    # 168.07; line 61 = -695.75 + 568.00 = -127.75, negative; line 68 = 0.00, line 69 = -127.75).
    # Line 61 negative: line 5 (1,000) is entered on line 13, and line 14 = 127.75. Line 17 =
    # 1,000 less 1,695.75 = -695.75, so 17A = 695.75; line 20 = 3,000 less 2,432.00 = 568.00.
    # Line 21: line 20 is positive, so the lesser of 568.00 and 695.75 = 568.00. Line 22: 17A
    # (695.75) is more than line 14 (127.75): 1. Line 23: line 69 is negative, so line 68 x the
    # rate at line 22 = 0.00 x 1 = 0.00; line 24 = the lesser of 695.75 and 0.00 = 0.00; line 25A
    # = line 21 = 568.00. Line 26 = 0.00 + 1,000 + 568.00 = 1,568.00 and line 27 = 1,568.00 x
    # 16.80672 = 26,352.93696, 26,352.94.
    worksheet = return_bo(line_19="1000", line_39="3000")

    assert worksheet.get(RC381_PART_3_LINE_61).value == D("-127.75")
    assert part_4(worksheet) == {
        "8": D("-578.82"),
        "11": D("-116.93"),
        "12": D("-695.75"),
        "13h": D("1695.75"),
        "13": D("1000"),
        "14": D("127.75"),
        "17": D("-695.75"),
        "17A": D("695.75"),
        "20": D("568.00"),
        "21h17": D("0"),
        "21h20": D("568.00"),
        "21": D("568.00"),
        "22": D("1"),
        "23a": D("0.00"),
        "23b": D("0.00"),
        "23": D("0.00"),
        "24h": D("0.00"),
        "24": D("0.00"),
        "25A": D("568.00"),
        "26": D("1568.00"),
        "27": D("26352.94"),
    }


def test_return_bo_part_4_line_23_is_line_68_times_the_rate_when_line_69_is_negative() -> None:
    # The same box 16 of 1,000 and box 17 of 3,000 with box 16A of 100.00: line 68 = 100.00 and
    # line 69 = -127.75 + 100.00 = -27.75, still negative: line 23 = 100.00 x the rate at line 22
    # (1) = 100.00. Line 24 = the lesser of line 17A (695.75) and line 23 = 100.00. Line 26 =
    # 100.00 + 1,000 + 568.00 = 1,668.00; line 27 = 1,668.00 x 16.80672 = 28,033.60896, 28,033.61.
    worksheet = return_bo(line_19="1000", line_39="3000", line_25="100.00")

    assert worksheet.get(RC381_PART_3_LINE_69).value == D("-27.75")
    lines = part_4(worksheet)
    assert lines["23a"] == D("100.00")
    assert lines["23b"] == D("100.00")
    assert lines["23"] == D("100.00")
    assert lines["24"] == D("100.00")
    assert lines["25A"] == D("568.00")
    assert lines["26"] == D("1668.00")
    assert lines["27"] == D("28033.61")


def test_return_bo_part_4_line_23_is_the_lesser_when_line_69_is_positive() -> None:
    # Box 16A of 200.00: line 68 = 200.00 and line 69 = -127.75 + 200.00 = 72.25, positive: line
    # 23 = the lesser of line 68 (200.00) and line 17A (695.75) = 200.00; line 24 = 200.00. Line
    # 26 = 200.00 + 1,000 + 568.00 = 1,768.00; line 27 = 1,768.00 x 16.80672 = 29,714.28096,
    # 29,714.28.
    worksheet = return_bo(line_19="1000", line_39="3000", line_25="200.00")

    assert worksheet.get(RC381_PART_3_LINE_69).value == D("72.25")
    lines = part_4(worksheet)
    assert lines["23"] == D("200.00")
    assert lines["24"] == D("200.00")
    assert lines["26"] == D("1768.00")
    assert lines["27"] == D("29714.28")


def test_return_bo_part_4_line_23_takes_the_lesser_branch_when_line_69_is_zero() -> None:
    # Box 16A of 127.75: line 68 = 127.75 and line 69 = -127.75 + 127.75 = 0.00, "positive or
    # "0"": line 23 = the lesser of 127.75 and 695.75 = 127.75. Line 24 = 127.75; line 26 =
    # 127.75 + 1,000 + 568.00 = 1,695.75; line 27 = 28,500.00.
    worksheet = return_bo(line_19="1000", line_39="3000", line_25="127.75")

    assert worksheet.get(RC381_PART_3_LINE_69).value == D("0.00")
    lines = part_4(worksheet)
    assert lines["23"] == D("127.75")
    assert lines["24"] == D("127.75")
    assert lines["26"] == D("1695.75")
    assert lines["27"] == D("28500.00")


def test_return_bo_part_4_line_23_is_line_17a_when_line_68_is_more_and_line_69_is_positive() -> (
    None
):
    # Box 16A of 700.00: line 68 = 700.00 and line 69 = 572.25, positive: line 23 = the lesser of
    # 700.00 and line 17A (695.75) = 695.75, not 700.00 x 1. Line 24 = the lesser of 695.75 and
    # 695.75 = 695.75; line 26 = 695.75 + 1,000 + 568.00 = 2,263.75; line 27 = 2,263.75 x 16.80672
    # = 38,046.2124, 38,046.21.
    worksheet = return_bo(line_19="1000", line_39="3000", line_25="700.00")

    assert worksheet.get(RC381_PART_3_LINE_69).value == D("572.25")
    lines = part_4(worksheet)
    assert lines["23a"] == D("695.75")
    assert lines["23b"] == D("700.00")
    assert lines["23"] == D("695.75")
    assert lines["24"] == D("695.75")
    assert lines["26"] == D("2263.75")
    assert lines["27"] == D("38046.21")


def test_return_bo_part_4_with_line_61_negative_and_lines_17_and_20_both_negative() -> None:
    # Box 16 of 1,000 and box 17 of 2,000 (Part 3: line 20 = 831.93, line 21 = 168.07; line 61 =
    # -695.75 - 432.00 = -1,127.75, line 68 = 0.00, line 69 = -1,127.75). Line 5 (1,000) is entered
    # on line 13; line 14 = 1,127.75. Line 17 = -695.75 (17A = 695.75) and line 20 = 2,000 less
    # 2,432.00 = -432.00, both negative: line 21 = 0. Line 22 = 695.75 / 1,127.75 = 0.61693637...,
    # cut at the fifth decimal place: 0.61693 (rounding would give 0.61694). Line 23 (line 69 is
    # negative) = 0.00 x 0.61693 = 0.00, line 24 = 0.00, line 25A = 0. Line 26 = 0.00 + 1,000 + 0 =
    # 1,000.00; line 27 = 1,000.00 x 16.80672 = 16,806.72.
    worksheet = return_bo(line_19="1000", line_39="2000")

    assert worksheet.get(RC381_PART_3_LINE_61).value == D("-1127.75")
    assert part_4(worksheet) == {
        "8": D("-578.82"),
        "11": D("-116.93"),
        "12": D("-695.75"),
        "13h": D("1695.75"),
        "13": D("1000"),
        "14": D("1127.75"),
        "17": D("-695.75"),
        "17A": D("695.75"),
        "20": D("-432.00"),
        "21h17": D("0"),
        "21h20": D("0"),
        "21": D("0"),
        "22": D("0.61693"),
        "23a": D("0.00"),
        "23b": D("0.00"),
        "23": D("0.00"),
        "24h": D("0.00"),
        "24": D("0.00"),
        "25A": D("0"),
        "26": D("1000.00"),
        "27": D("16806.72"),
    }


def test_return_bo_part_4_line_23_is_line_68_times_the_truncated_rate_to_the_cent() -> None:
    # The same with box 16A of 100.00: line 68 = 100.00, line 69 = -1,127.75 + 100.00 = -1,027.75
    # negative: line 23 = 100.00 x 0.61693 = 61.693, 61.69. Line 24 = the lesser of 695.75 and
    # 61.69 = 61.69; line 26 = 61.69 + 1,000 + 0 = 1,061.69; line 27 = 1,061.69 x 16.80672 =
    # 17,843.52656, 17,843.53.
    worksheet = return_bo(line_19="1000", line_39="2000", line_25="100.00")

    assert worksheet.get(RC381_PART_3_LINE_69).value == D("-1027.75")
    assert isinstance(worksheet.producer_of(RC381_PART_4_LINE_23_MULTIPLIED), ApplyChosenRate)
    lines = part_4(worksheet)
    assert lines["22"] == D("0.61693")
    assert lines["23b"] == D("61.69")
    assert lines["23"] == D("61.69")
    assert lines["24"] == D("61.69")
    assert lines["26"] == D("1061.69")
    assert lines["27"] == D("17843.53")


def test_return_bo_part_4_with_line_61_negative_line_17_positive_and_line_20_negative() -> None:
    # Box 16 of 2,500 and box 17 of 1,000 (Part 3: line 20 = 2,079.83, line 21 = 420.17; line 61 =
    # 804.25 - 1,432.00 = -627.75, negative). Line 5 (2,500) is entered on line 13; line 14 =
    # 627.75. Line 17 = 2,500 less 1,695.75 = 804.25 (positive), 17A = 0; line 20 = 1,000 less
    # 2,432.00 = -1,432.00. Line 21: line 17 is positive: the amount from line 17 in brackets,
    # -804.25. Line 22 = 0 / 627.75 = 0.00000; line 23 = 0.00 x 0 = 0.00; line 24 = the lesser of
    # 0 and 0.00 = 0; line 25A = line 21 = -804.25. Line 26 = 0 + 2,500 + -804.25 = 1,695.75 and
    # line 27 = 1,695.75 x 16.80672 = 28,500.00.
    worksheet = return_bo(line_19="2500", line_39="1000")

    assert worksheet.get(RC381_PART_3_LINE_61).value == D("-627.75")
    assert part_4(worksheet) == {
        "8": D("669.08"),
        "11": D("135.17"),
        "12": D("804.25"),
        "13h": D("1695.75"),
        "13": D("2500"),
        "14": D("627.75"),
        "17": D("804.25"),
        "17A": D("0"),
        "20": D("-1432.00"),
        "21h17": D("-804.25"),
        "21h20": D("0"),
        "21": D("-804.25"),
        "22": D("0"),
        "23a": D("0.00"),
        "23b": D("0.00"),
        "23": D("0.00"),
        "24h": D("0"),
        "24": D("0"),
        "25A": D("-804.25"),
        "26": D("1695.75"),
        "27": D("28500.00"),
    }


def test_return_bo_part_4_line_22_is_1_when_line_17a_equals_line_14() -> None:
    # Box 16 of 1,000 and box 17 of 2,432.00 (Part 3's line 44, so line 20 = 0.00): line 61 =
    # -695.75 + 0.00, line 14 = 695.75 and line 17A = 695.75. 17A is not more than line 14, so
    # line 22 is 695.75 / 695.75 = 1.00000. Line 21 = 0 (line 20 is "0"); line 23 = 0.00 x 1 =
    # 0.00, line 24 = 0.00, line 25A = 0; line 26 = 1,000.00 and line 27 = 16,806.72.
    worksheet = return_bo(line_19="1000", line_39="2432.00")

    lines = part_4(worksheet)
    assert lines["14"] == D("695.75")
    assert lines["17A"] == D("695.75")
    assert lines["20"] == D("0.00")
    assert lines["21"] == D("0")
    assert lines["22"] == D("1.00000")
    assert lines["26"] == D("1000.00")
    assert lines["27"] == D("16806.72")


def test_return_bo_part_4_with_literal_line_68_negative_lines_23_and_24_are_negative() -> None:
    # Lines 1 and 2 of 40,000 each (Part 3: line 22 = 1,678.05, line 23 = 339.00, line 24 =
    # 2,017.05, line 44 = 2,169.60, line 67 = 348.00), box 16 of 1,000 and box 17 of 1,500 (line
    # 20 = 831.93, line 21 = 168.07). Line 8 = 831.93 less 1,678.05 = -846.12, line 11 = 168.07
    # less 339.00 = -170.93, line 12 = -1,017.05. Line 17 = 1,000 less 2,017.05 = -1,017.05 (17A
    # = 1,017.05); line 20 = 1,500 less 2,169.60 = -669.60. Line 61 = -1,017.05 - 669.60 =
    # -1,686.65 (line 14 = 1,686.65); line 68 = 0 less 348.00 = -348.00, line 69 = -2,034.65.
    # Line 22 = 1,017.05 / 1,686.65 = 0.6030000296, 0.60300. Line 69 is negative: line 23 = line 68
    # x 0.60300 = -209.844, -209.84. Line 24 prints "whichever is less: amount from line 17A or
    # line 23" with no floor: the lesser of 1,017.05 and -209.84, -209.84 (to be confirmed: a
    # negative line 24 reduces line 26). Line 25A = 0 (line 21 is 0). Line 26 = -209.84 + 1,000 +
    # 0 = 790.16 and line 27 = 790.16 x 16.80672 = 13,279.99788, 13,280.00.
    worksheet = return_bo(line_1="40000", line_2="40000", line_19="1000", line_39="1500")

    assert worksheet.get(RC381_PART_3_LINE_68).value == D("-348.00")
    assert worksheet.get(RC381_PART_3_LINE_69).value == D("-2034.65")
    assert part_4(worksheet) == {
        "8": D("-846.12"),
        "11": D("-170.93"),
        "12": D("-1017.05"),
        "13h": D("2017.05"),
        "13": D("1000"),
        "14": D("1686.65"),
        "17": D("-1017.05"),
        "17A": D("1017.05"),
        "20": D("-669.60"),
        "21h17": D("0"),
        "21h20": D("0"),
        "21": D("0"),
        "22": D("0.60300"),
        "23a": D("-348.00"),
        "23b": D("-209.84"),
        "23": D("-209.84"),
        "24h": D("-209.84"),
        "24": D("-209.84"),
        "25A": D("0"),
        "26": D("790.16"),
        "27": D("13280.00"),
    }


def test_return_bo_part_4_with_line_61_zero_enters_line_5_on_line_26() -> None:
    # Box 16 of 1,695.75 (Part 3's line 24) and box 17 of 2,432.00 (its line 44): lines 17 and 20
    # are 0.00 and line 61 = 0.00. Do not complete lines 6 to 24: "Enter the amount from line 5 on
    # line 26 and continue at line 27": line 26 = 1,695.75 and line 27 = 1,695.75 x 16.80672 =
    # 28,500.00. Line 13 (the amount carried to line 25) is line 5; lines 24 and 25A are 0.
    worksheet = return_bo(line_19="1695.75", line_39="2432.00")

    assert worksheet.get(RC381_PART_3_LINE_61).value == D("0.00")
    assert part_4(worksheet) == {
        "8": D("0.00"),
        "11": D("0.00"),
        "12": D("0.00"),
        "13h": D("1695.75"),
        "13": D("1695.75"),
        "14": D("0.00"),
        "17": D("0.00"),
        "17A": D("0.00"),
        "20": D("0.00"),
        "21h17": D("0"),
        "21h20": D("0"),
        "21": D("0"),
        "22": D("0"),
        "23a": D("0.00"),
        "23b": D("0.00"),
        "23": D("0.00"),
        "24h": D("0.00"),
        "24": D("0"),
        "25A": D("0"),
        "26": D("1695.75"),
        "27": D("28500.00"),
    }


def test_return_bo_part_4_with_line_61_zero_line_21_is_computed_but_not_entered() -> None:
    # Box 16 of 2,000 and box 17 of 2,127.75: line 17 = 2,000 less 1,695.75 = 304.25 and line 20 =
    # 2,127.75 less 2,432.00 = -304.25, so line 61 = 0.00. Line 26 is line 5 (2,000). Line 21 =
    # the amount from line 17 in brackets, -304.25 (line 20 is negative), but line 25A takes
    # line 21 only when line 61 is negative: 0. Line 27 = 2,000 x 16.80672 = 33,613.44.
    worksheet = return_bo(line_19="2000", line_39="2127.75")

    lines = part_4(worksheet)
    assert worksheet.get(RC381_PART_3_LINE_61).value == D("0.00")
    assert lines["17"] == D("304.25")
    assert lines["20"] == D("-304.25")
    assert lines["21"] == D("-304.25")
    assert lines["25A"] == D("0")
    assert lines["13"] == D("2000")
    assert lines["26"] == D("2000")
    assert lines["27"] == D("33613.44")


def test_return_bo_part_4_with_line_61_zero_line_22_is_1_for_a_positive_line_17a() -> None:
    # Box 16 of 1,000 and box 17 of 3,127.75: line 17 = -695.75 (17A = 695.75), line 20 = 3,127.75
    # less 2,432.00 = 695.75, line 61 = 0.00 and so line 14 = 0.00. 17A is more than line 14: line
    # 22 = 1 (the test comes before any division by 0). Line 21 = the lesser of 695.75 and
    # 695.75, computed; lines 24 and 25A are 0, line 26 = line 5 = 1,000 and line 27 = 16,806.72.
    worksheet = return_bo(line_19="1000", line_39="3127.75")

    lines = part_4(worksheet)
    assert lines["14"] == D("0.00")
    assert lines["17A"] == D("695.75")
    assert lines["22"] == D("1")
    assert lines["21"] == D("695.75")
    assert lines["24"] == D("0")
    assert lines["25A"] == D("0")
    assert lines["26"] == D("1000")
    assert lines["27"] == D("16806.72")


# Part 4 line 21 "If line 17 and line 20 are both negative or either amount is "0", enter "0". If
# line 17 is positive, enter the amount from line 17 (show in brackets). If line 20 is positive,
# enter whichever is less: amount from line 20 or line 17A." (box 16, box 17, line 17, line 20,
# line 21; line 17 = box 16 less 1,695.75 and line 20 = box 17 less 2,432.00)
LINE_21_CASES = [
    # Line 17 negative, line 20 positive: the lesser of line 20 and line 17A (695.75).
    ("1000", "3000", "-695.75", "568.00", "568.00"),
    ("1000", "3500", "-695.75", "1068.00", "695.75"),
    ("1000", "2700", "-695.75", "268.00", "268.00"),
    # Both negative: "0".
    ("1000", "2000", "-695.75", "-432.00", "0"),
    # Line 17 positive, line 20 negative: line 17 in brackets.
    ("2500", "1000", "804.25", "-1432.00", "-804.25"),
    ("2000", "2127.75", "304.25", "-304.25", "-304.25"),
    # Either amount "0": "0", whatever the other is.
    ("2500", "2432.00", "804.25", "0.00", "0"),
    ("1000", "2432.00", "-695.75", "0.00", "0"),
    ("1695.75", "3000", "0.00", "568.00", "0"),
    ("1695.75", "1000", "0.00", "-1432.00", "0"),
    ("1695.75", "2432.00", "0.00", "0.00", "0"),
    # Both positive: the form is silent; the reading is "0" (the lesser of line 20 and line 17A,
    # which is 0 for a line 17 that is not negative, and not line 17 in brackets).
    ("1800.00", "2500.00", "104.25", "68.00", "0"),
]


@pytest.mark.parametrize(("box_16", "box_17", "line_17", "line_20", "line_21"), LINE_21_CASES)
def test_return_bo_part_4_line_21_follows_the_sentences_on_lines_17_and_20(
    box_16: str, box_17: str, line_17: str, line_20: str, line_21: str
) -> None:
    worksheet = return_bo(line_19=box_16, line_39=box_17)

    assert worksheet.get(RC381_PART_4_LINE_17).value == D(line_17)
    assert worksheet.get(RC381_PART_4_LINE_20).value == D(line_20)
    assert worksheet.get(RC381_PART_4_LINE_21).value == D(line_21)


# Part 4 line 22 "If line 17A is more than line 14, enter "1". If not, enter the result of line 17A
# divided by line 14 (calculated to the fifth decimal place without rounding)." (box 16, box 17,
# line 14, line 17A, line 22)
LINE_22_CASES = [
    # More than: 1, even when line 14 is 0.
    ("1000", "3000", "127.75", "695.75", "1"),
    ("1000", "3127.75", "0.00", "695.75", "1"),
    ("1000", "3500", "0", "695.75", "1"),
    # Equal: 17A over 14 is 1.00000.
    ("1000", "2432.00", "695.75", "695.75", "1.00000"),
    # Less than: the quotient cut at the fifth decimal place (0.61693637...).
    ("1000", "2000", "1127.75", "695.75", "0.61693"),
    # Line 17A is 0: 0 over line 14.
    ("2500", "1000", "627.75", "0", "0.00000"),
    # Both 0: a zero divisor gives 0.
    ("1800.00", "2500.00", "0", "0", "0"),
    ("1695.75", "2432.00", "0.00", "0.00", "0"),
]


@pytest.mark.parametrize(("box_16", "box_17", "line_14", "line_17a", "line_22"), LINE_22_CASES)
def test_return_bo_part_4_line_22_is_the_truncated_ratio_capped_at_one(
    box_16: str, box_17: str, line_14: str, line_17a: str, line_22: str
) -> None:
    worksheet = return_bo(line_19=box_16, line_39=box_17)

    assert worksheet.get(RC381_PART_4_LINE_14).value == D(line_14)
    assert worksheet.get(RC381_PART_4_LINE_17A).value == D(line_17a)
    assert worksheet.get(RC381_PART_4_LINE_22).value == Rate(D(line_22))


def test_return_bo_part_4_steps_are_the_form_capabilities() -> None:
    worksheet = return_bo()

    for kind in (RC381_PART_4_LINE_4, RC381_PART_4_LINE_12, RC381_PART_4_LINE_26):
        assert isinstance(worksheet.producer_of(kind), Sum), kind.identifier
    for kind in (
        RC381_PART_4_LINE_8,
        RC381_PART_4_LINE_11,
        RC381_PART_4_LINE_13_DIFFERENCE,
        RC381_PART_4_LINE_17,
        RC381_PART_4_LINE_20,
    ):
        assert isinstance(worksheet.producer_of(kind), Subtract), kind.identifier
    for kind in (RC381_PART_4_LINE_14, RC381_PART_4_LINE_17A):
        assert isinstance(worksheet.producer_of(kind), PositivePartOfNegation), kind.identifier
    for kind in (
        RC381_PART_4_LINE_13,
        RC381_PART_4_LINE_21,
        RC381_PART_4_LINE_23,
        RC381_PART_4_LINE_24,
        RC381_PART_4_LINE_25A,
    ):
        assert isinstance(worksheet.producer_of(kind), ChooseBySign), kind.identifier
    # Line 21's two printed results: the amount from line 17 "(show in brackets)" and "whichever is
    # less: amount from line 20 or line 17A".
    assert isinstance(
        worksheet.producer_of(RC381_PART_4_LINE_21_FROM_LINE_17), LesserOfWhenPositiveInBrackets
    )
    assert isinstance(worksheet.producer_of(RC381_PART_4_LINE_21_LESSER), LesserOfWhenPositive)
    assert isinstance(worksheet.producer_of(RC381_PART_4_LINE_22), RatioTruncatedAtMostOne)
    for kind in (RC381_PART_4_LINE_23_LESSER, RC381_PART_4_LINE_24_LESSER):
        assert isinstance(worksheet.producer_of(kind), LesserOf), kind.identifier
    assert isinstance(worksheet.producer_of(RC381_PART_4_LINE_23_MULTIPLIED), ApplyChosenRate)
    assert isinstance(worksheet.producer_of(RC381_PART_4_LINE_27), ApplyFraction)
    # Form RC381 Part 4 lines 31 to 56: the sums and differences, the signs read by "If line 61 of
    # Part 3 is ..." and "If line 68 of Part 3 is positive ...", the helpers printed inside lines
    # 31, 35A, 46 and 51, the positive parts of lines 33 and 54, the gross-up of line 41.
    for kind in (
        RC381_PART_4_LINE_35A,
        RC381_PART_4_LINE_40,
        RC381_PART_4_LINE_42,
        RC381_PART_4_LINE_53,
        RC381_PART_4_LINE_56,
    ):
        assert isinstance(worksheet.producer_of(kind), Sum), kind.identifier
    for kind in (
        RC381_PART_4_LINE_31_DIFFERENCE,
        RC381_PART_4_LINE_32,
        RC381_PART_4_LINE_35,
        RC381_PART_4_LINE_38,
        RC381_PART_4_LINE_46_DIFFERENCE,
        RC381_PART_4_LINE_47,
        RC381_PART_4_LINE_51_DIFFERENCE,
        RC381_PART_4_LINE_52,
    ):
        assert isinstance(worksheet.producer_of(kind), Subtract), kind.identifier
    for kind in (RC381_PART_4_LINE_33, RC381_PART_4_LINE_54):
        assert isinstance(worksheet.producer_of(kind), PositivePartOfNegation), kind.identifier
    for kind in (
        RC381_PART_4_LINE_31,
        RC381_PART_4_LINE_35AA,
        RC381_PART_4_LINE_35AB_WHEN_LINE_35_ZERO,
        RC381_PART_4_LINE_35AB,
        RC381_PART_4_LINE_46,
        RC381_PART_4_LINE_51,
    ):
        assert isinstance(worksheet.producer_of(kind), ChooseBySign), kind.identifier
    # "Whichever is less ... when positive" (lines 34, 35A's amount from line 17 and 55) and its
    # "show in brackets" sibling (35A's amount from line 20).
    for kind in (RC381_PART_4_LINE_34, RC381_PART_4_LINE_35AA_FROM_LINE_17, RC381_PART_4_LINE_55):
        assert type(worksheet.producer_of(kind)) is LesserOfWhenPositive, kind.identifier
    assert isinstance(
        worksheet.producer_of(RC381_PART_4_LINE_35AB_FROM_LINE_20), LesserOfWhenPositiveInBrackets
    )
    assert isinstance(worksheet.producer_of(RC381_PART_4_LINE_36), SumNotBelowZero)
    assert isinstance(worksheet.producer_of(RC381_PART_4_LINE_39), LesserOf)
    assert isinstance(worksheet.producer_of(RC381_PART_4_LINE_41), ApplyFraction)
    # Form RC381 Part 4 lines 57 to 91: the floored differences of lines 59, 61, 65, 68, 69 and 77,
    # the unfloored differences of lines 70, 80, 82 and 90, the sums of lines 74, 87 and 88, the
    # "whichever is less" of lines 62 and 83 (the latter before "If line 74 is more than line 57"),
    # line 76's division by 4%, the tiers of lines 84 to 86, the "if positive" amounts of line 89
    # and line 42100 (floored sums), line 89's "x 2", the positive amount of line 91 and its 50%.
    for kind in (
        RC381_PART_4_LINE_59,
        RC381_PART_4_LINE_61,
        RC381_PART_4_LINE_65,
        RC381_PART_4_LINE_68,
        RC381_PART_4_LINE_69,
        RC381_PART_4_LINE_77,
    ):
        assert isinstance(worksheet.producer_of(kind), SubtractNotBelowZero), kind.identifier
    for kind in (
        RC381_PART_4_LINE_70,
        RC381_PART_4_LINE_80,
        RC381_PART_4_LINE_82,
        RC381_PART_4_LINE_90,
    ):
        assert isinstance(worksheet.producer_of(kind), Subtract), kind.identifier
    for kind in (RC381_PART_4_LINE_74, RC381_PART_4_LINE_87, RC381_PART_4_LINE_88):
        assert isinstance(worksheet.producer_of(kind), Sum), kind.identifier
    for kind in (RC381_PART_4_LINE_62, RC381_PART_4_LINE_83_LESSER):
        assert isinstance(worksheet.producer_of(kind), LesserOf), kind.identifier
    assert isinstance(worksheet.producer_of(RC381_PART_4_LINE_83), AmountWhenMore)
    assert isinstance(worksheet.producer_of(RC381_PART_4_LINE_76), DividedByRate)
    for kind in (RC381_PART_4_LINE_84, RC381_PART_4_LINE_85, RC381_PART_4_LINE_86):
        assert isinstance(worksheet.producer_of(kind), TieredContribution), kind.identifier
    for kind in (RC381_PART_4_LINE_89_FROM_LINE_69, RC381_SELF_EMPLOYMENT_CPP_CONTRIBUTIONS):
        assert isinstance(worksheet.producer_of(kind), SumNotBelowZero), kind.identifier
    assert isinstance(worksheet.producer_of(RC381_PART_4_LINE_89), ApplyFraction)
    assert isinstance(
        worksheet.producer_of(RC381_PART_4_LINE_91_FROM_LINE_90), PositivePartOfNegation
    )
    assert isinstance(worksheet.producer_of(RC381_PART_4_LINE_91), ApplyRate)
    # Form RC381 Part 4 lines 92 to 110: the choices by the sign of line 53, 60 and 68 of Part 3
    # (lines 92, 99 and 106), the positive amounts of lines 93, 100 and 107, the "whichever is
    # less" of lines 94, 97, 101, 104 and 108 when the lines are positive, the differences of
    # lines 95 and 102 and the one printed inside line 104, and the sums of lines 96, 98, 103, 105,
    # 109 and 110.
    for kind in (RC381_PART_4_LINE_92, RC381_PART_4_LINE_99, RC381_PART_4_LINE_106):
        assert isinstance(worksheet.producer_of(kind), ChooseBySign), kind.identifier
    for kind in (RC381_PART_4_LINE_93, RC381_PART_4_LINE_100, RC381_PART_4_LINE_107):
        assert isinstance(worksheet.producer_of(kind), PositivePartOfNegation), kind.identifier
    for kind in (
        RC381_PART_4_LINE_94,
        RC381_PART_4_LINE_97,
        RC381_PART_4_LINE_101,
        RC381_PART_4_LINE_104,
        RC381_PART_4_LINE_108,
    ):
        assert isinstance(worksheet.producer_of(kind), LesserOfWhenPositive), kind.identifier
    for kind in (
        RC381_PART_4_LINE_95,
        RC381_PART_4_LINE_102,
        RC381_PART_4_LINE_104_DIFFERENCE,
    ):
        assert isinstance(worksheet.producer_of(kind), Subtract), kind.identifier
    for kind in (
        RC381_PART_4_LINE_96,
        RC381_PART_4_LINE_98,
        RC381_PART_4_LINE_103,
        RC381_PART_4_LINE_105,
        RC381_PART_4_LINE_109,
        RC381_PART_4_LINE_110,
    ):
        assert isinstance(worksheet.producer_of(kind), Sum), kind.identifier


def test_return_bo_the_cpt20_election_does_not_reach_the_t1_lines_yet() -> None:
    # Part 4 line 4 is read by lines 62, 68, 74 and 80, which no T1 line reads yet, and Schedule 8
    # Part 4's line 42100 is multiplied by "Part 4 completed" (0 here): the same return with and
    # without lines 2 and 3 (50373 and 50399) gives the same Schedule 8 contributions, net income
    # and total payable.
    with_election = return_bo()
    without_election = return_bo(cpt20_earnings="0", cpt20_t4_earnings="0")

    for kind in (CPP_BASE_CONTRIBUTIONS, CPP_ENHANCED_CONTRIBUTIONS, NET_INCOME, TOTAL_PAYABLE):
        assert with_election.get(kind).value == without_election.get(kind).value, kind.identifier
    # Part 4 lines 5 to 56 do not read line 4, so they are the same too; lines 62 and onward do:
    # line 4 of 12,500 against 0 changes line 62 (1,300.00 against 0), line 74 and the lines after
    # them, down to line 90 and line 91.
    assert part_4(with_election) == part_4(without_election)
    assert part_4_qpp(with_election) == part_4_qpp(without_election)
    assert part_4_earnings(with_election) != part_4_earnings(without_election)
    assert with_election.get(RC381_PART_4_LINE_62).value == D("1300.00")
    assert without_election.get(RC381_PART_4_LINE_62).value == D("0")


# Part 4, lines 31 to 56 (the QPP side before its gross-up, line 42 and the second additional
# contributions and the totals). Line 61 of Part 3 decides lines 31 to 40 ("If line 61 of Part 3 is:
# "0", do not complete lines 29 to 39. Complete line 28 and enter the amount on line 40 and continue
# at line 41. positive, complete lines 28 to 32 only, and continue at line 40. negative, complete
# line 28 and enter "0" at line 31 and continue at line 32."); line 68 of Part 3 decides lines 44
# to 46 and 49 to 51 ("If line 68 of Part 3 is positive, complete ... If not, enter "0" ...") and,
# with line 61, lines 54 and 55. The helper lines the form prints inside a line are computed
# whatever the signs are (as line 21's are), so the dicts below list them too: "31_difference" is
# "Line 29 minus line 30", "35Aa17" the amount from line 17 (when positive) of line 35A's first
# sentence, "35Ab20" the amount from line 20 in brackets (when line 20 is positive) of its second
# sentence and "35Ab0" that amount when line 35 is "0", before line 61 is read ("35Ab");
# "46_difference" and "51_difference" are lines 46 and 51's differences before line 68 is read.
PART_4_QPP_KINDS: dict[str, ArtifactKind[Decimal]] = {
    "31_difference": RC381_PART_4_LINE_31_DIFFERENCE,
    "31": RC381_PART_4_LINE_31,
    "32": RC381_PART_4_LINE_32,
    "33": RC381_PART_4_LINE_33,
    "34": RC381_PART_4_LINE_34,
    "35": RC381_PART_4_LINE_35,
    "35Aa17": RC381_PART_4_LINE_35AA_FROM_LINE_17,
    "35Aa": RC381_PART_4_LINE_35AA,
    "35Ab20": RC381_PART_4_LINE_35AB_FROM_LINE_20,
    "35Ab0": RC381_PART_4_LINE_35AB_WHEN_LINE_35_ZERO,
    "35Ab": RC381_PART_4_LINE_35AB,
    "35A": RC381_PART_4_LINE_35A,
    "36": RC381_PART_4_LINE_36,
    "38": RC381_PART_4_LINE_38,
    "39": RC381_PART_4_LINE_39,
    "40": RC381_PART_4_LINE_40,
    "41": RC381_PART_4_LINE_41,
    "42": RC381_PART_4_LINE_42,
    "46_difference": RC381_PART_4_LINE_46_DIFFERENCE,
    "46": RC381_PART_4_LINE_46,
    "47": RC381_PART_4_LINE_47,
    "51_difference": RC381_PART_4_LINE_51_DIFFERENCE,
    "51": RC381_PART_4_LINE_51,
    "52": RC381_PART_4_LINE_52,
    "53": RC381_PART_4_LINE_53,
    "54": RC381_PART_4_LINE_54,
    "55": RC381_PART_4_LINE_55,
    "56": RC381_PART_4_LINE_56,
}


def part_4_qpp(worksheet: Worksheet) -> dict[str, Decimal]:
    """Part 4's lines 31 to 56 of `worksheet`, by line number (see `PART_4_QPP_KINDS`)."""
    return {line: worksheet.get(kind).value for line, kind in PART_4_QPP_KINDS.items()}


# Each case: box 26 outside and in Quebec (lines 1 and 2 of Part 3), box 16, box 17, box 16A and box
# 17A (lines 19, 39, 25 and 45), then lines 61 and 68 of Part 3, and Part 4's lines 31 to 56. The
# figures are proved by an independent Decimal model of the printed form (not by this engine).
# Part 4's line 17 = box 16 less 1,695.75 and line 20 = box 17 less 2,432.00 when lines 1 and 2 are
# 30,000 and 40,000 (Part 3's lines 24 and 44). With line 2 of 80,000 line 3 is 110,000, more than
# lines C and G, so Part 3's required second additional contributions are 108.00 (line 26) and
# 288.00 (line 46) and line 68 is -396.00 while boxes 16A and 17A are blank; Part 3's lines 24 and
# 44 are then 1,100.18 and 3,155.82.
PART_4_QPP_CASES = [
    # The ticket's example: line 61 of Part 3 is positive, so the form completes lines 28 to 32
    # only and continues at line 40.
    pytest.param(
        "30000",
        "40000",
        "1800.00",
        "2500.00",
        "0",
        "0",
        "172.25",
        "0.00",
        {
            "31_difference": "68.00",
            "31": "68.00",
            "32": "2432.00",
            "33": "0",
            "34": "0",
            "35": "0",
            "35Aa17": "104.25",
            "35Aa": "0",
            "35Ab20": "-68.00",
            "35Ab0": "-68.00",
            "35Ab": "0",
            "35A": "0",
            "36": "0",
            "38": "0",
            "39": "0",
            "40": "2432.00",
            "41": "38000.00",
            "42": "66500.00",
            "46_difference": "0.00",
            "46": "0",
            "47": "0",
            "51_difference": "0.00",
            "51": "0",
            "52": "0",
            "53": "0",
            "54": "0",
            "55": "0",
            "56": "0",
        },
        id="ticket_example_line_61_positive",
    ),
    # Line 61 positive with no box 16 (line 17 is negative).
    pytest.param(
        "30000",
        "40000",
        "0",
        "4500",
        "0",
        "0",
        "372.25",
        "0.00",
        {
            "31_difference": "2068.00",
            "31": "2068.00",
            "32": "2432.00",
            "33": "0",
            "34": "0",
            "35": "0",
            "35Aa17": "0",
            "35Aa": "0",
            "35Ab20": "-2068.00",
            "35Ab0": "-2068.00",
            "35Ab": "0",
            "35A": "0",
            "36": "0",
            "38": "0",
            "39": "0",
            "40": "2432.00",
            "41": "38000.00",
            "42": "66500.00",
            "46_difference": "0.00",
            "46": "0",
            "47": "0",
            "51_difference": "0.00",
            "51": "0",
            "52": "0",
            "53": "0",
            "54": "0",
            "55": "0",
            "56": "0",
        },
        id="line_61_positive_line_17_negative",
    ),
    # Line 61 positive and line 68 negative: lines 54 and 55 are completed.
    pytest.param(
        "30000",
        "80000",
        "1800",
        "2500",
        "0",
        "0",
        "44.00",
        "-396.00",
        {
            "31_difference": "-655.82",
            "31": "-655.82",
            "32": "3155.82",
            "33": "0",
            "34": "0",
            "35": "0",
            "35Aa17": "699.82",
            "35Aa": "0",
            "35Ab20": "0",
            "35Ab0": "0",
            "35Ab": "0",
            "35A": "0",
            "36": "0",
            "38": "0",
            "39": "0",
            "40": "3155.82",
            "41": "49309.69",
            "42": "67800.11",
            "46_difference": "-108.00",
            "46": "0",
            "47": "0",
            "51_difference": "-396.00",
            "51": "0",
            "52": "0",
            "53": "0",
            "54": "396.00",
            "55": "44.00",
            "56": "44.00",
        },
        id="line_61_positive_line_68_negative",
    ),
    # Line 61 positive and line 68 negative but less than line 61: line 55 is line 54.
    pytest.param(
        "30000",
        "80000",
        "1800",
        "2500",
        "380",
        "0",
        "44.00",
        "-16.00",
        {
            "31_difference": "-655.82",
            "31": "-655.82",
            "32": "3155.82",
            "33": "0",
            "34": "0",
            "35": "0",
            "35Aa17": "699.82",
            "35Aa": "0",
            "35Ab20": "0",
            "35Ab0": "0",
            "35Ab": "0",
            "35A": "0",
            "36": "0",
            "38": "0",
            "39": "0",
            "40": "3155.82",
            "41": "49309.69",
            "42": "67800.11",
            "46_difference": "272.00",
            "46": "0",
            "47": "380",
            "51_difference": "-16.00",
            "51": "0",
            "52": "0",
            "53": "380",
            "54": "16.00",
            "55": "16.00",
            "56": "396.00",
        },
        id="line_61_positive_line_68_negative_small",
    ),
    # Line 61 positive and line 68 positive: lines 44 to 46 and 49 to 51 are completed.
    pytest.param(
        "30000",
        "40000",
        "1800",
        "2500",
        "50",
        "50",
        "172.25",
        "100.00",
        {
            "31_difference": "68.00",
            "31": "68.00",
            "32": "2432.00",
            "33": "0",
            "34": "0",
            "35": "0",
            "35Aa17": "104.25",
            "35Aa": "0",
            "35Ab20": "-68.00",
            "35Ab0": "-68.00",
            "35Ab": "0",
            "35A": "0",
            "36": "100.00",
            "38": "100.00",
            "39": "0",
            "40": "2432.00",
            "41": "38000.00",
            "42": "66500.00",
            "46_difference": "50.00",
            "46": "50.00",
            "47": "0.00",
            "51_difference": "50.00",
            "51": "50.00",
            "52": "0.00",
            "53": "0.00",
            "54": "0",
            "55": "0",
            "56": "0.00",
        },
        id="line_61_positive_line_68_positive",
    ),
    # Line 46 is negative (box 16A of 100.00 less line 26 of Part 3).
    pytest.param(
        "30000",
        "80000",
        "1800",
        "2500",
        "100",
        "300",
        "44.00",
        "4.00",
        {
            "31_difference": "-655.82",
            "31": "-655.82",
            "32": "3155.82",
            "33": "0",
            "34": "0",
            "35": "0",
            "35Aa17": "699.82",
            "35Aa": "0",
            "35Ab20": "0",
            "35Ab0": "0",
            "35Ab": "0",
            "35A": "0",
            "36": "4.00",
            "38": "4.00",
            "39": "0",
            "40": "3155.82",
            "41": "49309.69",
            "42": "67800.11",
            "46_difference": "-8.00",
            "46": "-8.00",
            "47": "108.00",
            "51_difference": "12.00",
            "51": "12.00",
            "52": "288.00",
            "53": "396.00",
            "54": "0",
            "55": "0",
            "56": "396.00",
        },
        id="line_61_positive_line_46_negative",
    ),
    # Line 51 is negative (line 68 less a line 46 that is more).
    pytest.param(
        "30000",
        "80000",
        "1800",
        "3500",
        "500",
        "0",
        "1044.00",
        "104.00",
        {
            "31_difference": "344.18",
            "31": "344.18",
            "32": "3155.82",
            "33": "0",
            "34": "0",
            "35": "0",
            "35Aa17": "699.82",
            "35Aa": "0",
            "35Ab20": "-344.18",
            "35Ab0": "-344.18",
            "35Ab": "0",
            "35A": "0",
            "36": "104.00",
            "38": "104.00",
            "39": "0",
            "40": "3155.82",
            "41": "49309.69",
            "42": "67800.11",
            "46_difference": "392.00",
            "46": "392.00",
            "47": "108.00",
            "51_difference": "-288.00",
            "51": "-288.00",
            "52": "288.00",
            "53": "396.00",
            "54": "0",
            "55": "0",
            "56": "396.00",
        },
        id="line_61_positive_line_51_negative",
    ),
    # Line 68 is exactly 0, not positive: lines 44 to 46 and 49 to 51 are not completed.
    pytest.param(
        "30000",
        "80000",
        "1800",
        "2500",
        "396",
        "0",
        "44.00",
        "0.00",
        {
            "31_difference": "-655.82",
            "31": "-655.82",
            "32": "3155.82",
            "33": "0",
            "34": "0",
            "35": "0",
            "35Aa17": "699.82",
            "35Aa": "0",
            "35Ab20": "0",
            "35Ab0": "0",
            "35Ab": "0",
            "35A": "0",
            "36": "0",
            "38": "0",
            "39": "0",
            "40": "3155.82",
            "41": "49309.69",
            "42": "67800.11",
            "46_difference": "288.00",
            "46": "0",
            "47": "396",
            "51_difference": "0.00",
            "51": "0",
            "52": "0",
            "53": "396",
            "54": "0",
            "55": "0",
            "56": "396",
        },
        id="line_68_zero_with_a_line_46_difference",
    ),
    # Line 61 is 0: do not complete lines 29 to 39, complete line 28 and enter it on line 40.
    pytest.param(
        "30000",
        "40000",
        "1695.75",
        "2432",
        "0",
        "0",
        "0.00",
        "0.00",
        {
            "31_difference": "0.00",
            "31": "0",
            "32": "2432",
            "33": "0",
            "34": "0",
            "35": "0",
            "35Aa17": "0",
            "35Aa": "0",
            "35Ab20": "0",
            "35Ab0": "0",
            "35Ab": "0",
            "35A": "0",
            "36": "0",
            "38": "0",
            "39": "0",
            "40": "2432",
            "41": "38000.00",
            "42": "66500.00",
            "46_difference": "0.00",
            "46": "0",
            "47": "0",
            "51_difference": "0.00",
            "51": "0",
            "52": "0",
            "53": "0",
            "54": "0",
            "55": "0",
            "56": "0",
        },
        id="line_61_zero",
    ),
    # Line 61 is 0 with line 17 positive and line 20 negative: line 31 is not entered.
    pytest.param(
        "30000",
        "40000",
        "2000",
        "2127.75",
        "0",
        "0",
        "0.00",
        "0.00",
        {
            "31_difference": "-304.25",
            "31": "0",
            "32": "2127.75",
            "33": "0",
            "34": "0",
            "35": "0",
            "35Aa17": "304.25",
            "35Aa": "0",
            "35Ab20": "0",
            "35Ab0": "0",
            "35Ab": "0",
            "35A": "0",
            "36": "0",
            "38": "0",
            "39": "0",
            "40": "2127.75",
            "41": "33246.09",
            "42": "66859.53",
            "46_difference": "0.00",
            "46": "0",
            "47": "0",
            "51_difference": "0.00",
            "51": "0",
            "52": "0",
            "53": "0",
            "54": "0",
            "55": "0",
            "56": "0",
        },
        id="line_61_zero_line_17_positive_line_20_negative",
    ),
    # Line 61 is 0 and line 40 x 15.625 is not a whole number of cents.
    pytest.param(
        "30000",
        "40000",
        "1000.01",
        "3127.74",
        "0",
        "0",
        "0.00",
        "0.00",
        {
            "31_difference": "695.74",
            "31": "0",
            "32": "3127.74",
            "33": "0",
            "34": "0",
            "35": "0",
            "35Aa17": "0",
            "35Aa": "0",
            "35Ab20": "-695.74",
            "35Ab0": "-695.74",
            "35Ab": "0",
            "35A": "0",
            "36": "0",
            "38": "0",
            "39": "0",
            "40": "3127.74",
            "41": "48870.94",
            "42": "65677.83",
            "46_difference": "0.00",
            "46": "0",
            "47": "0",
            "51_difference": "0.00",
            "51": "0",
            "52": "0",
            "53": "0",
            "54": "0",
            "55": "0",
            "56": "0",
        },
        id="line_61_zero_line_41_rounds_up",
    ),
    # Line 61 is 0 and line 68 positive.
    pytest.param(
        "30000",
        "40000",
        "1695.75",
        "2432",
        "50",
        "50",
        "0.00",
        "100.00",
        {
            "31_difference": "0.00",
            "31": "0",
            "32": "2432",
            "33": "0",
            "34": "0",
            "35": "0",
            "35Aa17": "0",
            "35Aa": "0",
            "35Ab20": "0",
            "35Ab0": "0",
            "35Ab": "0",
            "35A": "0",
            "36": "100.00",
            "38": "100.00",
            "39": "0",
            "40": "2432",
            "41": "38000.00",
            "42": "66500.00",
            "46_difference": "50.00",
            "46": "50.00",
            "47": "0.00",
            "51_difference": "50.00",
            "51": "50.00",
            "52": "0.00",
            "53": "0.00",
            "54": "0",
            "55": "0",
            "56": "0.00",
        },
        id="line_61_zero_line_68_positive",
    ),
    # Line 61 negative with lines 17 and 20 both negative: line 35A is 0.
    pytest.param(
        "30000",
        "40000",
        "1000",
        "2000",
        "0",
        "0",
        "-1127.75",
        "0.00",
        {
            "31_difference": "-432.00",
            "31": "0",
            "32": "2000",
            "33": "1127.75",
            "34": "695.75",
            "35": "432.00",
            "35Aa17": "0",
            "35Aa": "0",
            "35Ab20": "0",
            "35Ab0": "0",
            "35Ab": "0",
            "35A": "0",
            "36": "0",
            "38": "0.00",
            "39": "0.00",
            "40": "2000.00",
            "41": "31250.00",
            "42": "48056.72",
            "46_difference": "0.00",
            "46": "0",
            "47": "0",
            "51_difference": "0.00",
            "51": "0",
            "52": "0",
            "53": "0",
            "54": "0",
            "55": "0",
            "56": "0",
        },
        id="line_61_negative_lines_17_and_20_negative",
    ),
    # Line 61 negative with line 17 exactly 0: line 17A is 0, so line 34 is 0.
    pytest.param(
        "30000",
        "40000",
        "1695.75",
        "1000",
        "0",
        "0",
        "-1432.00",
        "0.00",
        {
            "31_difference": "-1432.00",
            "31": "0",
            "32": "1000",
            "33": "1432.00",
            "34": "0",
            "35": "1432.00",
            "35Aa17": "0",
            "35Aa": "0",
            "35Ab20": "0",
            "35Ab0": "0",
            "35Ab": "0",
            "35A": "0",
            "36": "0",
            "38": "0",
            "39": "0",
            "40": "1000",
            "41": "15625.00",
            "42": "44125.00",
            "46_difference": "0.00",
            "46": "0",
            "47": "0",
            "51_difference": "0.00",
            "51": "0",
            "52": "0",
            "53": "0",
            "54": "0",
            "55": "0",
            "56": "0",
        },
        id="line_61_negative_line_17_zero",
    ),
    # Line 61 negative, 17A at least line 33 (line 35 is 0) and line 20 positive: line 35A takes
    # line 20 in brackets.
    pytest.param(
        "30000",
        "80000",
        "0",
        "3500",
        "0",
        "0",
        "-756.00",
        "-396.00",
        {
            "31_difference": "344.18",
            "31": "0",
            "32": "3500",
            "33": "756.00",
            "34": "756.00",
            "35": "0.00",
            "35Aa17": "0",
            "35Aa": "0",
            "35Ab20": "-344.18",
            "35Ab0": "-344.18",
            "35Ab": "-344.18",
            "35A": "-344.18",
            "36": "0",
            "38": "396.00",
            "39": "0.00",
            "40": "3155.82",
            "41": "49309.69",
            "42": "48438.77",
            "46_difference": "-108.00",
            "46": "0",
            "47": "0",
            "51_difference": "-396.00",
            "51": "0",
            "52": "0",
            "53": "0",
            "54": "396.00",
            "55": "0",
            "56": "0",
        },
        id="line_61_negative_line_35_zero_line_20_positive",
    ),
    # Line 61 negative, line 35 and line 17 both positive: line 35A takes line 17.
    pytest.param(
        "30000",
        "80000",
        "1800",
        "0",
        "0",
        "0",
        "-2456.00",
        "-396.00",
        {
            "31_difference": "-3155.82",
            "31": "0",
            "32": "0",
            "33": "2456.00",
            "34": "0",
            "35": "2456.00",
            "35Aa17": "699.82",
            "35Aa": "699.82",
            "35Ab20": "0",
            "35Ab0": "0",
            "35Ab": "0",
            "35A": "699.82",
            "36": "0",
            "38": "0",
            "39": "0",
            "40": "699.82",
            "41": "10934.69",
            "42": "29425.11",
            "46_difference": "-108.00",
            "46": "0",
            "47": "0",
            "51_difference": "-396.00",
            "51": "0",
            "52": "0",
            "53": "0",
            "54": "396.00",
            "55": "0",
            "56": "0",
        },
        id="line_61_negative_line_35_positive_line_17_positive",
    ),
    # Line 61 negative, line 68 positive: line 36 is line 68, line 39 is the lesser, line 35.
    pytest.param(
        "30000",
        "40000",
        "1800",
        "2000",
        "500",
        "0",
        "-327.75",
        "500.00",
        {
            "31_difference": "-432.00",
            "31": "0",
            "32": "2000",
            "33": "327.75",
            "34": "0",
            "35": "327.75",
            "35Aa17": "104.25",
            "35Aa": "104.25",
            "35Ab20": "0",
            "35Ab0": "0",
            "35Ab": "0",
            "35A": "104.25",
            "36": "500.00",
            "38": "500.00",
            "39": "327.75",
            "40": "2432.00",
            "41": "38000.00",
            "42": "66500.00",
            "46_difference": "500.00",
            "46": "500.00",
            "47": "0.00",
            "51_difference": "0.00",
            "51": "0.00",
            "52": "0.00",
            "53": "0.00",
            "54": "0",
            "55": "0",
            "56": "0.00",
        },
        id="line_61_negative_line_68_positive_line_39_is_line_35",
    ),
    # As above with box 16A of 100.00: line 39 is the lesser, line 38.
    pytest.param(
        "30000",
        "40000",
        "1800",
        "2000",
        "100",
        "0",
        "-327.75",
        "100.00",
        {
            "31_difference": "-432.00",
            "31": "0",
            "32": "2000",
            "33": "327.75",
            "34": "0",
            "35": "327.75",
            "35Aa17": "104.25",
            "35Aa": "104.25",
            "35Ab20": "0",
            "35Ab0": "0",
            "35Ab": "0",
            "35A": "104.25",
            "36": "100.00",
            "38": "100.00",
            "39": "100.00",
            "40": "2204.25",
            "41": "34441.41",
            "42": "62941.41",
            "46_difference": "100.00",
            "46": "100.00",
            "47": "0.00",
            "51_difference": "0.00",
            "51": "0.00",
            "52": "0.00",
            "53": "0.00",
            "54": "0",
            "55": "0",
            "56": "0.00",
        },
        id="line_61_negative_line_68_positive_line_39_is_line_38",
    ),
    # Line 61 negative, line 68 negative and line 69 negative: line 24 is negative, so line 38 is
    # positive.
    pytest.param(
        "30000",
        "80000",
        "0",
        "0",
        "0",
        "0",
        "-4256.00",
        "-396.00",
        {
            "31_difference": "-3155.82",
            "31": "0",
            "32": "0",
            "33": "4256.00",
            "34": "1100.18",
            "35": "3155.82",
            "35Aa17": "0",
            "35Aa": "0",
            "35Ab20": "0",
            "35Ab0": "0",
            "35Ab": "0",
            "35A": "0",
            "36": "0",
            "38": "102.37",
            "39": "102.37",
            "40": "102.37",
            "41": "1599.53",
            "42": "-120.97",
            "46_difference": "-108.00",
            "46": "0",
            "47": "0",
            "51_difference": "-396.00",
            "51": "0",
            "52": "0",
            "53": "0",
            "54": "396.00",
            "55": "0",
            "56": "0",
        },
        id="line_61_negative_line_68_negative_line_24_negative",
    ),
    # Line 61 negative with the second additional contributions of both plans.
    pytest.param(
        "60000",
        "80000",
        "1695.75",
        "2432",
        "500",
        "0",
        "-80.69",
        "104.00",
        {
            "31_difference": "-47.55",
            "31": "0",
            "32": "2432",
            "33": "80.69",
            "34": "33.14",
            "35": "47.55",
            "35Aa17": "0",
            "35Aa": "0",
            "35Ab20": "0",
            "35Ab0": "0",
            "35Ab": "0",
            "35A": "0",
            "36": "104.00",
            "38": "70.86",
            "39": "47.55",
            "40": "2479.55",
            "41": "38742.97",
            "42": "67799.94",
            "46_difference": "330.29",
            "46": "330.29",
            "47": "169.71",
            "51_difference": "-226.29",
            "51": "-226.29",
            "52": "226.29",
            "53": "396.00",
            "54": "0",
            "55": "0",
            "56": "396.00",
        },
        id="line_61_negative_line_68_positive_large_totals",
    ),
]


@pytest.mark.parametrize(
    (
        "line_1",
        "line_2",
        "box_16",
        "box_17",
        "box_16a",
        "box_17a",
        "line_61",
        "line_68",
        "expected",
    ),
    PART_4_QPP_CASES,
)
def test_return_bo_part_4_lines_31_to_56(
    line_1: str,
    line_2: str,
    box_16: str,
    box_17: str,
    box_16a: str,
    box_17a: str,
    line_61: str,
    line_68: str,
    expected: dict[str, str],
) -> None:
    worksheet = return_bo(line_1, line_2, box_16, box_17, line_25=box_16a, line_45=box_17a)

    assert worksheet.get(RC381_PART_3_LINE_61).value == D(line_61)
    assert worksheet.get(RC381_PART_3_LINE_68).value == D(line_68)
    assert part_4_qpp(worksheet) == {line: D(value) for line, value in expected.items()}


# Part 4, lines 57 to 91 (the earnings subject to contributions, the contributions through
# self-employment income and other earnings, the contributions payable and the overpayment). Lines
# 57 and 58 are lines C and F of Part 2, line 60 is line 42, lines 63 and 64 are line 58 and line 3
# of Part 3, lines 66, 71, 78 and 79 are lines 4 and 65, line 67 is line 59, lines 72 and 73 are
# lines 11 and 31 of Part 3, line 75 is line D and line 81 is line 70. "If line 3 of Part 3 is less
# than line 58, complete lines 63 to 69. If not, enter "0" on line 69": line 65 "Line 63 minus line
# 64 (if negative, enter "0" on lines 65 and 69 ...)" is "0" exactly when line 3 is not less than
# line 58, and so is line 69, which the tests below pin; line 68 is still computed when the form
# does not complete it. "If line 74 is more than line 57, complete lines 75 to 83. If not, enter
# "0" on line 83": line 83 is the lesser of lines 77 and 82 only then, and "0" otherwise. The
# helpers the form prints inside a line are computed whatever the signs are, so the dict below
# lists them: "83_lesser" is "Enter whichever is less: amount from line 77 or line 82.", before
# the gate, "89_from_line_69" the "Amount from line 69 of Part 3 (if positive)" and
# "91_from_line_90" the "amount from line 90 entered as a positive amount". "42100" is line 90
# when it is positive ("enter the amount on line 42100 of your return"), else "0".
PART_4_EARNINGS_KINDS: dict[str, ArtifactKind[Decimal]] = {
    "59": RC381_PART_4_LINE_59,
    "61": RC381_PART_4_LINE_61,
    "62": RC381_PART_4_LINE_62,
    "65": RC381_PART_4_LINE_65,
    "68": RC381_PART_4_LINE_68,
    "69": RC381_PART_4_LINE_69,
    "70": RC381_PART_4_LINE_70,
    "74": RC381_PART_4_LINE_74,
    "76": RC381_PART_4_LINE_76,
    "77": RC381_PART_4_LINE_77,
    "80": RC381_PART_4_LINE_80,
    "82": RC381_PART_4_LINE_82,
    "83_lesser": RC381_PART_4_LINE_83_LESSER,
    "83": RC381_PART_4_LINE_83,
    "84": RC381_PART_4_LINE_84,
    "85": RC381_PART_4_LINE_85,
    "86": RC381_PART_4_LINE_86,
    "87": RC381_PART_4_LINE_87,
    "88": RC381_PART_4_LINE_88,
    "89_from_line_69": RC381_PART_4_LINE_89_FROM_LINE_69,
    "89": RC381_PART_4_LINE_89,
    "90": RC381_PART_4_LINE_90,
    "42100": RC381_SELF_EMPLOYMENT_CPP_CONTRIBUTIONS,
    "91_from_line_90": RC381_PART_4_LINE_91_FROM_LINE_90,
    "91": RC381_PART_4_LINE_91,
}


def part_4_earnings(worksheet: Worksheet) -> dict[str, Decimal]:
    """Part 4's lines 59 to 91 of `worksheet`, by line number (see `PART_4_EARNINGS_KINDS`)."""
    return {line: worksheet.get(kind).value for line, kind in PART_4_EARNINGS_KINDS.items()}


def test_return_bo_part_4_lines_59_to_91_match_the_tickets_example() -> None:
    # Return BO: line 4 = 12,500 (the election), line 42 = 66,500.00 (line 27 plus line 41), line 3
    # of Part 3 = 70,000.00 and line 69 of Part 3 = 172.25. Line 59 = line C 71,300.00 less line F
    # 3,500.00 = 67,800.00; line 61 = 67,800.00 less 66,500.00 = 1,300.00; line 62 = the lesser of
    # 12,500 and 1,300.00 = 1,300.00. Line 3 (70,000.00) is not less than line 58 (3,500.00), so
    # line 65 (3,500.00 less 70,000.00, entered as "0") and line 69 are "0" (line 68 = 12,500 less
    # 67,800.00 is "0" too); line 70 = 1,300.00. Line 74 = 12,500 + 30,000.00 + 40,000.00 =
    # 82,500.00 is more than line 57 (71,300.00), so lines 75 to 83 are completed: line 76 = 0.00 /
    # 4% = 0.00 (line 56 is 0), line 77 = 9,900.00 less 0.00 = 9,900.00, line 80 = 12,500 less 0 =
    # 12,500, line 82 = 12,500 less 1,300.00 = 11,200.00 and line 83 = the lesser of 9,900.00 and
    # 11,200.00 = 9,900.00. Line 84 = 1,300.00 x 9.9% = 128.70, line 85 = 1,300.00 x 2% = 26.00,
    # line 86 = 9,900.00 x 8% = 792.00, line 87 = 818.00 and line 88 = 946.70. Line 89 = 172.25 x
    # 2 = 344.50, line 90 = 946.70 less 344.50 = 602.20, positive: line 42100 = 602.20 and line 91
    # is "0".
    worksheet = return_bo()

    assert worksheet.get(RC381_PART_4_LINE_4).value == D("12500")
    assert worksheet.get(RC381_PART_4_LINE_42).value == D("66500.00")
    assert worksheet.get(RC381_PART_3_LINE_69).value == D("172.25")
    assert part_4_earnings(worksheet) == {
        "59": D("67800.00"),
        "61": D("1300.00"),
        "62": D("1300.00"),
        "65": D("0"),
        "68": D("0"),
        "69": D("0"),
        "70": D("1300.00"),
        "74": D("82500"),
        "76": D("0.00"),
        "77": D("9900.00"),
        "80": D("12500"),
        "82": D("11200.00"),
        "83_lesser": D("9900.00"),
        "83": D("9900.00"),
        "84": D("128.70"),
        "85": D("26.00"),
        "86": D("792.00"),
        "87": D("818.00"),
        "88": D("946.70"),
        "89_from_line_69": D("172.25"),
        "89": D("344.50"),
        "90": D("602.20"),
        "42100": D("602.20"),
        "91_from_line_90": D("0"),
        "91": D("0.00"),
    }


def test_return_bo_part_4_without_the_election_line_90_is_negative_and_line_91_is_half_of_it() -> (
    None
):
    # No election and no self-employment income: line 4 = 0, so lines 62, 70, 80, 82 and 83 are 0
    # and lines 84 to 88 are 0.00. Line 69 of Part 3 (172.25) is positive: line 89 = 172.25 x 2 =
    # 344.50 and line 90 = 0.00 less 344.50 = -344.50, in brackets: line 42100 is "0" and
    # line 91 = 344.50 x 50% = 172.25.
    worksheet = return_bo(cpt20_earnings="0", cpt20_t4_earnings="0")

    assert part_4_earnings(worksheet) == {
        "59": D("67800.00"),
        "61": D("1300.00"),
        "62": D("0"),
        "65": D("0"),
        "68": D("0"),
        "69": D("0"),
        "70": D("0"),
        "74": D("70000"),
        "76": D("0.00"),
        "77": D("9900.00"),
        "80": D("0"),
        "82": D("0"),
        "83_lesser": D("0"),
        "83": D("0"),
        "84": D("0.00"),
        "85": D("0.00"),
        "86": D("0.00"),
        "87": D("0.00"),
        "88": D("0.00"),
        "89_from_line_69": D("172.25"),
        "89": D("344.50"),
        "90": D("-344.50"),
        "42100": D("0"),
        "91_from_line_90": D("344.50"),
        "91": D("172.25"),
    }


def test_return_bo_part_4_self_employment_income_and_no_t4_slips_reaches_the_printed_maximums() -> (
    None
):
    # Net partnership income of 80,000 and no T4 slip: line 3 of Part 3 is 0, less than line 58, so
    # lines 63 to 69 are completed: line 65 = 3,500.00 less 0 = 3,500.00 and line 68 = 80,000 less
    # 67,800.00 = 12,200.00, so line 69 = 3,500.00 less 12,200.00, entered as "0". Line 61 =
    # 67,800.00 (line 42 is 0) and line 62 = 67,800.00, so line 70 is the band of 67,800.00: line
    # 84 = 67,800.00 x 9.9% = 6,712.20 and line 85 = 67,800.00 x 2% = 1,356.00 (the printed
    # maximums). Line 74 = 80,000 is more than line 57: line 82 = (80,000 less 3,500.00) less
    # 67,800.00 = 8,700.00 is less than line 77 (9,900.00), so line 83 = 8,700.00 and line 86 =
    # 8,700.00 x 8% = 696.00. Line 69 of Part 3 is 0: line 90 = 8,764.20 = line 42100.
    worksheet = return_bo(
        line_1="0",
        line_2="0",
        line_19="0",
        line_39="0",
        cpt20_earnings="0",
        cpt20_t4_earnings="0",
        net_partnership_income="80000",
    )

    assert worksheet.get(RC381_PART_3_LINE_3).value == D("0")
    assert part_4_earnings(worksheet) == {
        "59": D("67800.00"),
        "61": D("67800.00"),
        "62": D("67800.00"),
        "65": D("3500.00"),
        "68": D("12200.00"),
        "69": D("0"),
        "70": D("67800.00"),
        "74": D("80000"),
        "76": D("0.00"),
        "77": D("9900.00"),
        "80": D("76500.00"),
        "82": D("8700.00"),
        "83_lesser": D("8700.00"),
        "83": D("8700.00"),
        "84": D("6712.20"),
        "85": D("1356.00"),
        "86": D("696.00"),
        "87": D("2052.00"),
        "88": D("8764.20"),
        "89_from_line_69": D("0.00"),
        "89": D("0.00"),
        "90": D("8764.20"),
        "42100": D("8764.20"),
        "91_from_line_90": D("0"),
        "91": D("0.00"),
    }


def test_return_bo_part_4_line_69_is_zero_when_line_3_is_exactly_line_58_and_not_when_less() -> (
    None
):
    # Line 3 of Part 3 = 2,000 + 1,500 = 3,500.00 is not less than line 58 (3,500.00): line 65 is
    # "0", so is line 69, and with net partnership income of 100 line 70 = line 62 = 100.00. One
    # cent less (line 2 of 1,499.99): line 65 = 0.01, line 68 = 0 (100 is not more than
    # 67,800.00), line 69 = 0.01 and line 70 = 100.00 less 0.01 = 99.99.
    at_line_58 = return_bo(
        "2000",
        "1500",
        "0",
        "0",
        net_partnership_income="100",
        cpt20_earnings="0",
        cpt20_t4_earnings="0",
    )
    below_line_58 = return_bo(
        "2000",
        "1499.99",
        "0",
        "0",
        net_partnership_income="100",
        cpt20_earnings="0",
        cpt20_t4_earnings="0",
    )

    assert at_line_58.get(RC381_PART_3_LINE_3).value == D("3500.00")
    assert at_line_58.get(RC381_PART_4_LINE_65).value == D("0")
    assert at_line_58.get(RC381_PART_4_LINE_69).value == D("0")
    assert at_line_58.get(RC381_PART_4_LINE_70).value == D("100")
    assert below_line_58.get(RC381_PART_3_LINE_3).value == D("3499.99")
    assert below_line_58.get(RC381_PART_4_LINE_65).value == D("0.01")
    assert below_line_58.get(RC381_PART_4_LINE_68).value == D("0")
    assert below_line_58.get(RC381_PART_4_LINE_69).value == D("0.01")
    assert below_line_58.get(RC381_PART_4_LINE_70).value == D("99.99")
    # Lines 84 and 85 are 9.9% and 2% of line 70: 99.99 x 9.9% = 9.89901 (9.90) and 99.99 x 2% =
    # 1.9998 (2.00).
    assert below_line_58.get(RC381_PART_4_LINE_84).value == D("9.90")
    assert below_line_58.get(RC381_PART_4_LINE_85).value == D("2.00")


def test_return_bo_part_4_line_83_needs_line_74_to_be_more_than_line_57() -> None:
    # Lines 71 to 73 are line 4 (12,500) and lines 11 and 31 of Part 3 (30,000.00 and the whole of
    # line 2): with line 2 of 28,800 line 74 = 71,300.00, which is line 57 (71,300.00), not more
    # than it: line 83 is "0" although lines 77 (9,900.00) and 82 (12,500 less line 61,
    # 12,499.94, is 0.06) give 0.06; with line 2 of 28,800.01 line 74 = 71,300.01 is more, and line
    # 83 = 0.06.
    equal = return_bo(line_2="28800")
    one_cent_more = return_bo(line_2="28800.01")

    assert equal.get(RC381_PART_4_LINE_74).value == D("71300.00")
    assert equal.get(RC381_PART_4_LINE_83_LESSER).value == D("0.06")
    assert equal.get(RC381_PART_4_LINE_83).value == D("0")
    assert equal.get(RC381_PART_4_LINE_86).value == D("0")
    assert one_cent_more.get(RC381_PART_4_LINE_74).value == D("71300.01")
    assert one_cent_more.get(RC381_PART_4_LINE_83).value == D("0.06")
    assert one_cent_more.get(RC381_PART_4_LINE_86).value == D("0.00")


def test_return_bo_part_4_a_negative_line_70_contributes_nothing_and_is_not_floored() -> None:
    # The form prints no floor on line 70 "Line 62 minus line 69": with line 3 of Part 3 of 2,500.00
    # (1,000 + 1,500) line 65 = line 69 = 1,000.00 and net partnership income of 300 gives line 62 =
    # 300, so line 70 = -700.00. Lines 84 and 85 take earnings below zero as nothing (0.00), line
    # 80 = 300 less 1,000.00 = -700.00 and line 82 = -700.00 less -700.00 = 0.00.
    worksheet = return_bo(
        "1000",
        "1500",
        "0",
        "0",
        net_partnership_income="300",
        cpt20_earnings="0",
        cpt20_t4_earnings="0",
    )

    assert worksheet.get(RC381_PART_4_LINE_70).value == D("-700.00")
    assert worksheet.get(RC381_PART_4_LINE_80).value == D("-700.00")
    assert worksheet.get(RC381_PART_4_LINE_82).value == D("0.00")
    assert worksheet.get(RC381_PART_4_LINE_84).value == D("0")
    assert worksheet.get(RC381_PART_4_LINE_85).value == D("0")
    assert worksheet.get(RC381_PART_4_LINE_90).value == D("0")


def test_return_bo_part_4_line_89_is_twice_line_69_of_part_3_only_when_that_is_positive() -> None:
    # Line 69 of Part 3 = 172.25 (positive): line 89 = 172.25 x 2 = 344.50. A negative line 69
    # (line 2 of 80,000 with no T4 contributions: line 61 = -4,256.00 and line 68 = -396.00, line
    # 69 = -4,652.00) and a line 69 of "0" give "0" ("if positive").
    positive = return_bo()
    negative = return_bo(line_2="80000", line_19="0", line_39="0")
    zero = return_bo(line_19="1695.75", line_39="2432", cpt20_earnings="0", cpt20_t4_earnings="0")

    assert positive.get(RC381_PART_4_LINE_89_FROM_LINE_69).value == D("172.25")
    assert positive.get(RC381_PART_4_LINE_89).value == D("344.50")
    assert negative.get(RC381_PART_3_LINE_69).value == D("-4652.00")
    assert negative.get(RC381_PART_4_LINE_89_FROM_LINE_69).value == D("0")
    assert negative.get(RC381_PART_4_LINE_89).value == D("0")
    assert zero.get(RC381_PART_3_LINE_69).value == D("0")
    assert zero.get(RC381_PART_4_LINE_89).value == D("0")


def test_return_bo_part_4_line_90_positive_goes_to_line_42100_and_negative_to_line_91() -> None:
    # Positive (the ticket's example): line 90 = 602.20, line 42100 = 602.20, line 91 = 0. Negative
    # (no election): line 90 = -344.50, line 42100 = 0 and line 91 = 344.50 x 50% = 172.25 ("amount
    # from line 90 entered as a positive amount"). Zero (no election, line 69 of Part 3 of 0): both
    # are 0. A tie: line 90 of -344.37 gives 172.185, up to 172.19 (half even gives 172.18).
    positive = return_bo()
    negative = return_bo(cpt20_earnings="0", cpt20_t4_earnings="0")
    zero = return_bo(line_19="1695.75", line_39="2432", cpt20_earnings="0", cpt20_t4_earnings="0")
    tie = return_bo(cpt20_earnings="0", cpt20_t4_earnings="0", net_partnership_income="1.07")

    assert positive.get(RC381_PART_4_LINE_90).value == D("602.20")
    assert positive.get(RC381_SELF_EMPLOYMENT_CPP_CONTRIBUTIONS).value == D("602.20")
    assert positive.get(RC381_PART_4_LINE_91_FROM_LINE_90).value == D("0")
    assert positive.get(RC381_PART_4_LINE_91).value == D("0")
    assert negative.get(RC381_PART_4_LINE_90).value == D("-344.50")
    assert negative.get(RC381_SELF_EMPLOYMENT_CPP_CONTRIBUTIONS).value == D("0")
    assert negative.get(RC381_PART_4_LINE_91_FROM_LINE_90).value == D("344.50")
    assert negative.get(RC381_PART_4_LINE_91).value == D("172.25")
    assert zero.get(RC381_PART_4_LINE_90).value == D("0")
    assert zero.get(RC381_SELF_EMPLOYMENT_CPP_CONTRIBUTIONS).value == D("0")
    assert zero.get(RC381_PART_4_LINE_91).value == D("0")
    assert tie.get(RC381_PART_4_LINE_90).value == D("-344.37")
    assert tie.get(RC381_PART_4_LINE_91).value == D("172.19")


def test_return_bo_part_4_with_6_months_lines_57_and_58_are_the_6_month_row() -> None:
    # Lines C and F for 6 months on line A are 35,650.00 and 1,750.00: line 59 = 33,900.00 (the
    # most that line 59 prints for the year is 67,800). Line D is 4,950.00, which line 77 starts
    # from (line 75): line 56 is 198.00, so line 76 = 198.00 / 4% = 4,950.00 and line 77 = 0.00.
    worksheet = return_bo(cpp_months=6, qpp_months=6)

    assert worksheet.get(RC381_PART_2_LINE_B).value == 6
    assert worksheet.get(RC381_PART_4_LINE_56).value == D("198.00")
    assert worksheet.get(RC381_PART_4_LINE_59).value == D("33900.00")
    assert worksheet.get(RC381_PART_4_LINE_76).value == D("4950.00")
    assert worksheet.get(RC381_PART_4_LINE_77).value == D("0.00")


# Each case: box 26 outside and in Quebec (lines 1 and 2 of Part 3), box 16, box 17, box 16A and
# box 17A (lines 19, 39, 25 and 45), net partnership income (T1 line 12200, Part 4 line 1) and the
# election (lines 2 and 3, 50373 and 50399), the months, then the lines of the earlier parts it
# rests on (lines 61 and 69 of Part 3, lines 4, 42 and 56 of Part 4) and Part 4's lines 59 to 91.
# The figures are proved by an independent Decimal model of the printed form (not by this engine).
PART_4_EARNINGS_CASES = [
    # The example of Return BO: employment only on the T4 slips, the CPT20 election of 10,000 and
    # 2,500 and no other self-employment income, so line 4 is 12,500; line 69 of Part 3 is
    # positive.
    pytest.param(
        "30000",
        "40000",
        "1800.00",
        "2500.00",
        "0",
        "0",
        "0",
        "10000",
        "2500",
        12,
        12,
        {
            "part_3_line_61": "172.25",
            "part_3_line_69": "172.25",
            "line_4": "12500",
            "line_42": "66500.00",
            "line_56": "0",
        },
        {
            "59": "67800.00",
            "61": "1300.00",
            "62": "1300.00",
            "65": "0",
            "68": "0",
            "69": "0",
            "70": "1300.00",
            "74": "82500",
            "76": "0.00",
            "77": "9900.00",
            "80": "12500",
            "82": "11200.00",
            "83_lesser": "9900.00",
            "83": "9900.00",
            "84": "128.70",
            "85": "26.00",
            "86": "792.00",
            "87": "818.00",
            "88": "946.70",
            "89_from_line_69": "172.25",
            "89": "344.50",
            "90": "602.20",
            "42100": "602.20",
            "91_from_line_90": "0",
            "91": "0.00",
        },
        id="ticket_example",
    ),
    # Line 4 is 0: lines 70 and 83 are 0, and line 89 (twice line 69 of Part 3) makes line 90
    # negative, so line 42100 is 0 and line 91 is half of it.
    pytest.param(
        "30000",
        "40000",
        "1800.00",
        "2500.00",
        "0",
        "0",
        "0",
        "0",
        "0",
        12,
        12,
        {
            "part_3_line_61": "172.25",
            "part_3_line_69": "172.25",
            "line_4": "0",
            "line_42": "66500.00",
            "line_56": "0",
        },
        {
            "59": "67800.00",
            "61": "1300.00",
            "62": "0",
            "65": "0",
            "68": "0",
            "69": "0",
            "70": "0",
            "74": "70000",
            "76": "0.00",
            "77": "9900.00",
            "80": "0",
            "82": "0",
            "83_lesser": "0",
            "83": "0",
            "84": "0.00",
            "85": "0.00",
            "86": "0.00",
            "87": "0.00",
            "88": "0.00",
            "89_from_line_69": "172.25",
            "89": "344.50",
            "90": "-344.50",
            "42100": "0",
            "91_from_line_90": "344.50",
            "91": "172.25",
        },
        id="no_election_and_no_self_employment_income",
    ),
    # Line 70 is 15.00: 15.00 x 9.9% = 1.485 is a tie and rounds half up to 1.49 (half even gives
    # 1.48).
    pytest.param(
        "30000",
        "40000",
        "1800.00",
        "2500.00",
        "0",
        "0",
        "15",
        "0",
        "0",
        12,
        12,
        {
            "part_3_line_61": "172.25",
            "part_3_line_69": "172.25",
            "line_4": "15",
            "line_42": "66500.00",
            "line_56": "0",
        },
        {
            "59": "67800.00",
            "61": "1300.00",
            "62": "15",
            "65": "0",
            "68": "0",
            "69": "0",
            "70": "15",
            "74": "70015",
            "76": "0.00",
            "77": "9900.00",
            "80": "15",
            "82": "0",
            "83_lesser": "0",
            "83": "0",
            "84": "1.49",
            "85": "0.30",
            "86": "0.00",
            "87": "0.30",
            "88": "1.79",
            "89_from_line_69": "172.25",
            "89": "344.50",
            "90": "-342.71",
            "42100": "0",
            "91_from_line_90": "342.71",
            "91": "171.36",
        },
        id="net_self_employment_income_of_15",
    ),
    # Line 88 is 0.13 and line 90 is -344.37, so line 91 = 344.37 x 50% = 172.185, up to 172.19
    # (half even gives 172.18).
    pytest.param(
        "30000",
        "40000",
        "1800.00",
        "2500.00",
        "0",
        "0",
        "1.07",
        "0",
        "0",
        12,
        12,
        {
            "part_3_line_61": "172.25",
            "part_3_line_69": "172.25",
            "line_4": "1.07",
            "line_42": "66500.00",
            "line_56": "0",
        },
        {
            "59": "67800.00",
            "61": "1300.00",
            "62": "1.07",
            "65": "0",
            "68": "0",
            "69": "0",
            "70": "1.07",
            "74": "70001.07",
            "76": "0.00",
            "77": "9900.00",
            "80": "1.07",
            "82": "0.00",
            "83_lesser": "0.00",
            "83": "0",
            "84": "0.11",
            "85": "0.02",
            "86": "0.00",
            "87": "0.02",
            "88": "0.13",
            "89_from_line_69": "172.25",
            "89": "344.50",
            "90": "-344.37",
            "42100": "0",
            "91_from_line_90": "344.37",
            "91": "172.19",
        },
        id="line_91_rounds_half_up",
    ),
    # No T4 slips: line 3 of Part 3 is 0, less than line 58, so line 65 is 3,500.00; line 68
    # (80,000.00 less 67,800.00) takes it all, line 69 is 0 and line 70 is the line 59 maximum of
    # 67,800.00, where lines 84 and 85 stop at their printed maximums.
    pytest.param(
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        "80000",
        "0",
        "0",
        12,
        12,
        {
            "part_3_line_61": "0.00",
            "part_3_line_69": "0.00",
            "line_4": "80000",
            "line_42": "0.00",
            "line_56": "0",
        },
        {
            "59": "67800.00",
            "61": "67800.00",
            "62": "67800.00",
            "65": "3500.00",
            "68": "12200.00",
            "69": "0",
            "70": "67800.00",
            "74": "80000",
            "76": "0.00",
            "77": "9900.00",
            "80": "76500.00",
            "82": "8700.00",
            "83_lesser": "8700.00",
            "83": "8700.00",
            "84": "6712.20",
            "85": "1356.00",
            "86": "696.00",
            "87": "2052.00",
            "88": "8764.20",
            "89_from_line_69": "0.00",
            "89": "0.00",
            "90": "8764.20",
            "42100": "8764.20",
            "91_from_line_90": "0",
            "91": "0.00",
        },
        id="self_employment_income_and_no_t4_slips",
    ),
    # Line 3 of Part 3 (2,500.00) is less than line 58 (3,500.00): line 65 = 1,000.00, line 68 =
    # 0, so line 69 = 1,000.00 and line 70 = 2,500.00 less 1,000.00 = 1,500.00.
    pytest.param(
        "1000",
        "1500",
        "0",
        "0",
        "0",
        "0",
        "2500",
        "0",
        "0",
        12,
        12,
        {
            "part_3_line_61": "0.00",
            "part_3_line_69": "0.00",
            "line_4": "2500",
            "line_42": "0.00",
            "line_56": "0",
        },
        {
            "59": "67800.00",
            "61": "67800.00",
            "62": "2500",
            "65": "1000.00",
            "68": "0",
            "69": "1000.00",
            "70": "1500.00",
            "74": "5000",
            "76": "0.00",
            "77": "9900.00",
            "80": "1500.00",
            "82": "0.00",
            "83_lesser": "0.00",
            "83": "0",
            "84": "148.50",
            "85": "30.00",
            "86": "0.00",
            "87": "30.00",
            "88": "178.50",
            "89_from_line_69": "0.00",
            "89": "0.00",
            "90": "178.50",
            "42100": "178.50",
            "91_from_line_90": "0",
            "91": "0.00",
        },
        id="earnings_below_the_basic_exemption",
    ),
    # As above with net self-employment income of 300: line 70 = 300.00 less 1,000.00 = -700.00
    # (the form prints no floor), which the tiers of lines 84 and 85 take as no earnings, and line
    # 82 = -700.00 less -700.00 = 0.
    pytest.param(
        "1000",
        "1500",
        "0",
        "0",
        "0",
        "0",
        "300",
        "0",
        "0",
        12,
        12,
        {
            "part_3_line_61": "0.00",
            "part_3_line_69": "0.00",
            "line_4": "300",
            "line_42": "0.00",
            "line_56": "0",
        },
        {
            "59": "67800.00",
            "61": "67800.00",
            "62": "300",
            "65": "1000.00",
            "68": "0",
            "69": "1000.00",
            "70": "-700.00",
            "74": "2800",
            "76": "0.00",
            "77": "9900.00",
            "80": "-700.00",
            "82": "0.00",
            "83_lesser": "0.00",
            "83": "0",
            "84": "0.00",
            "85": "0.00",
            "86": "0.00",
            "87": "0.00",
            "88": "0.00",
            "89_from_line_69": "0.00",
            "89": "0.00",
            "90": "0.00",
            "42100": "0.00",
            "91_from_line_90": "0",
            "91": "0.00",
        },
        id="self_employment_income_less_than_the_unused_exemption",
    ),
    # Line 68 is 12,200.00 (80,000.00 less 67,800.00), more than line 65 (1,000.00): line 69 is 0
    # (not below zero), and line 70 is line 62.
    pytest.param(
        "1000",
        "1500",
        "0",
        "0",
        "0",
        "0",
        "80000",
        "0",
        "0",
        12,
        12,
        {
            "part_3_line_61": "0.00",
            "part_3_line_69": "0.00",
            "line_4": "80000",
            "line_42": "0.00",
            "line_56": "0",
        },
        {
            "59": "67800.00",
            "61": "67800.00",
            "62": "67800.00",
            "65": "1000.00",
            "68": "12200.00",
            "69": "0",
            "70": "67800.00",
            "74": "82500",
            "76": "0.00",
            "77": "9900.00",
            "80": "79000.00",
            "82": "11200.00",
            "83_lesser": "9900.00",
            "83": "9900.00",
            "84": "6712.20",
            "85": "1356.00",
            "86": "792.00",
            "87": "2148.00",
            "88": "8860.20",
            "89_from_line_69": "0.00",
            "89": "0.00",
            "90": "8860.20",
            "42100": "8860.20",
            "91_from_line_90": "0",
            "91": "0.00",
        },
        id="line_68_positive_and_line_3_less_than_line_58",
    ),
    # Line 3 of Part 3 (70,000.00) is not less than line 58, so the form does not complete lines
    # 63 to 69 and line 69 is 0 (line 68 is still computed: 80,000.00 less 67,800.00 = 12,200.00).
    pytest.param(
        "30000",
        "40000",
        "1800.00",
        "2500.00",
        "0",
        "0",
        "80000",
        "0",
        "0",
        12,
        12,
        {
            "part_3_line_61": "172.25",
            "part_3_line_69": "172.25",
            "line_4": "80000",
            "line_42": "66500.00",
            "line_56": "0",
        },
        {
            "59": "67800.00",
            "61": "1300.00",
            "62": "1300.00",
            "65": "0",
            "68": "12200.00",
            "69": "0",
            "70": "1300.00",
            "74": "150000",
            "76": "0.00",
            "77": "9900.00",
            "80": "80000",
            "82": "78700.00",
            "83_lesser": "9900.00",
            "83": "9900.00",
            "84": "128.70",
            "85": "26.00",
            "86": "792.00",
            "87": "818.00",
            "88": "946.70",
            "89_from_line_69": "172.25",
            "89": "344.50",
            "90": "602.20",
            "42100": "602.20",
            "91_from_line_90": "0",
            "91": "0.00",
        },
        id="line_68_positive_and_line_3_not_less_than_line_58",
    ),
    # Line 74 = 12,500 + 30,000.00 + 28,800.00 = 71,300.00, not more than line 57 (71,300.00):
    # line 83 is 0 although lines 77 and 82 are positive.
    pytest.param(
        "30000",
        "28800",
        "1800.00",
        "2500.00",
        "0",
        "0",
        "0",
        "10000",
        "2500",
        12,
        12,
        {
            "part_3_line_61": "887.76",
            "part_3_line_69": "887.76",
            "line_4": "12500",
            "line_42": "55300.06",
            "line_56": "0",
        },
        {
            "59": "67800.00",
            "61": "12499.94",
            "62": "12499.94",
            "65": "0",
            "68": "0",
            "69": "0",
            "70": "12499.94",
            "74": "71300",
            "76": "0.00",
            "77": "9900.00",
            "80": "12500",
            "82": "0.06",
            "83_lesser": "0.06",
            "83": "0",
            "84": "1237.49",
            "85": "250.00",
            "86": "0.00",
            "87": "250.00",
            "88": "1487.49",
            "89_from_line_69": "887.76",
            "89": "1775.52",
            "90": "-288.03",
            "42100": "0",
            "91_from_line_90": "288.03",
            "91": "144.02",
        },
        id="line_74_equal_to_line_c",
    ),
    # Line 74 = 71,300.01 is more than line 57: line 83 is the lesser of lines 77 and 82.
    pytest.param(
        "30000",
        "28800.01",
        "1800.00",
        "2500.00",
        "0",
        "0",
        "0",
        "10000",
        "2500",
        12,
        12,
        {
            "part_3_line_61": "887.76",
            "part_3_line_69": "887.76",
            "line_4": "12500",
            "line_42": "55300.06",
            "line_56": "0",
        },
        {
            "59": "67800.00",
            "61": "12499.94",
            "62": "12499.94",
            "65": "0",
            "68": "0",
            "69": "0",
            "70": "12499.94",
            "74": "71300.01",
            "76": "0.00",
            "77": "9900.00",
            "80": "12500",
            "82": "0.06",
            "83_lesser": "0.06",
            "83": "0.06",
            "84": "1237.49",
            "85": "250.00",
            "86": "0.00",
            "87": "250.00",
            "88": "1487.49",
            "89_from_line_69": "887.76",
            "89": "1775.52",
            "90": "-288.03",
            "42100": "0",
            "91_from_line_90": "288.03",
            "91": "144.02",
        },
        id="line_74_one_cent_more_than_line_c",
    ),
    # Line 4 is 6,000, line 61 is 1,300.00: line 82 = 6,000 less 1,300.00 = 4,700.00 is less than
    # line 77 (9,900.00), so line 83 = 4,700.00.
    pytest.param(
        "30000",
        "40000",
        "1800.00",
        "2500.00",
        "0",
        "0",
        "0",
        "4000",
        "2000",
        12,
        12,
        {
            "part_3_line_61": "172.25",
            "part_3_line_69": "172.25",
            "line_4": "6000",
            "line_42": "66500.00",
            "line_56": "0",
        },
        {
            "59": "67800.00",
            "61": "1300.00",
            "62": "1300.00",
            "65": "0",
            "68": "0",
            "69": "0",
            "70": "1300.00",
            "74": "76000",
            "76": "0.00",
            "77": "9900.00",
            "80": "6000",
            "82": "4700.00",
            "83_lesser": "4700.00",
            "83": "4700.00",
            "84": "128.70",
            "85": "26.00",
            "86": "376.00",
            "87": "402.00",
            "88": "530.70",
            "89_from_line_69": "172.25",
            "89": "344.50",
            "90": "186.20",
            "42100": "186.20",
            "91_from_line_90": "0",
            "91": "0.00",
        },
        id="line_82_less_than_line_77",
    ),
    # Line 2 of 60,000 makes line 3 of Part 3 more than line C: line 56 = 62.50, line 76 = 62.50 /
    # 4% = 1,562.50 and line 77 = 9,900.00 less 1,562.50 = 8,337.50.
    pytest.param(
        "30000",
        "60000",
        "1800.00",
        "2500.00",
        "0",
        "0",
        "0",
        "10000",
        "2500",
        12,
        12,
        {
            "part_3_line_61": "62.50",
            "part_3_line_69": "-333.50",
            "line_4": "12500",
            "line_42": "67799.99",
            "line_56": "62.50",
        },
        {
            "59": "67800.00",
            "61": "0.01",
            "62": "0.01",
            "65": "0",
            "68": "0",
            "69": "0",
            "70": "0.01",
            "74": "93700.00",
            "76": "1562.50",
            "77": "8337.50",
            "80": "12500",
            "82": "12499.99",
            "83_lesser": "8337.50",
            "83": "8337.50",
            "84": "0.00",
            "85": "0.00",
            "86": "667.00",
            "87": "667.00",
            "88": "667.00",
            "89_from_line_69": "0",
            "89": "0",
            "90": "667.00",
            "42100": "667.00",
            "91_from_line_90": "0",
            "91": "0.00",
        },
        id="second_additional_contributions_reduce_line_77",
    ),
    # Line 56 is 396.00: line 76 = 396.00 / 4% = 9,900.00 is line D, so line 77 is 0.
    pytest.param(
        "30000",
        "60000",
        "1800.00",
        "2500.00",
        "500",
        "0",
        "0",
        "10000",
        "2500",
        12,
        12,
        {
            "part_3_line_61": "62.50",
            "part_3_line_69": "166.50",
            "line_4": "12500",
            "line_42": "67799.99",
            "line_56": "396.00",
        },
        {
            "59": "67800.00",
            "61": "0.01",
            "62": "0.01",
            "65": "0",
            "68": "0",
            "69": "0",
            "70": "0.01",
            "74": "93700.00",
            "76": "9900.00",
            "77": "0.00",
            "80": "12500",
            "82": "12499.99",
            "83_lesser": "0.00",
            "83": "0.00",
            "84": "0.00",
            "85": "0.00",
            "86": "0.00",
            "87": "0.00",
            "88": "0.00",
            "89_from_line_69": "166.50",
            "89": "333.00",
            "90": "-333.00",
            "42100": "0",
            "91_from_line_90": "333.00",
            "91": "166.50",
        },
        id="line_76_equal_to_line_d",
    ),
    # 6 months on line A: line D is 4,950.00 and line 76 = 396.00 / 4% = 9,900.00 is more, so line
    # 77 is 0 (negative, entered as 0).
    pytest.param(
        "30000",
        "80000",
        "500",
        "0",
        "396",
        "0",
        "300",
        "10000",
        "2500",
        6,
        12,
        {
            "part_3_line_61": "-3797.60",
            "part_3_line_69": "-3797.60",
            "line_4": "12800",
            "line_42": "8403.36",
            "line_56": "396",
        },
        {
            "59": "33900.00",
            "61": "25496.64",
            "62": "12800",
            "65": "0",
            "68": "0",
            "69": "0",
            "70": "12800",
            "74": "94000.00",
            "76": "9900.00",
            "77": "0",
            "80": "12800",
            "82": "0",
            "83_lesser": "0",
            "83": "0",
            "84": "1267.20",
            "85": "256.00",
            "86": "0.00",
            "87": "256.00",
            "88": "1523.20",
            "89_from_line_69": "0",
            "89": "0",
            "90": "1523.20",
            "42100": "1523.20",
            "91_from_line_90": "0",
            "91": "0.00",
        },
        id="line_76_more_than_line_d_for_6_months",
    ),
    # Line 42 = 67,800.02 is more than line 59 (67,800.00): line 61 is 0 and so is line 62.
    pytest.param(
        "30000",
        "41400",
        "1800.00",
        "2500.00",
        "0",
        "0",
        "0",
        "10000",
        "2500",
        12,
        12,
        {
            "part_3_line_61": "88.99",
            "part_3_line_69": "84.99",
            "line_4": "12500",
            "line_42": "67800.02",
            "line_56": "4.00",
        },
        {
            "59": "67800.00",
            "61": "0",
            "62": "0",
            "65": "0",
            "68": "0",
            "69": "0",
            "70": "0",
            "74": "83900",
            "76": "100.00",
            "77": "9800.00",
            "80": "12500",
            "82": "12500",
            "83_lesser": "9800.00",
            "83": "9800.00",
            "84": "0.00",
            "85": "0.00",
            "86": "784.00",
            "87": "784.00",
            "88": "784.00",
            "89_from_line_69": "84.99",
            "89": "169.98",
            "90": "614.02",
            "42100": "614.02",
            "91_from_line_90": "0",
            "91": "0.00",
        },
        id="line_42_more_than_line_59",
    ),
    # Line 42 is negative (line 35A takes line 20 in brackets), so line 61 is more than line 59
    # and line 70 is more than the 67,800.00 band of lines 84 and 85, which stop at their printed
    # maximums.
    pytest.param(
        "70000",
        "30000",
        "0",
        "0",
        "100",
        "0",
        "80000",
        "10000",
        "2500",
        12,
        12,
        {
            "part_3_line_61": "-4125.63",
            "part_3_line_69": "-4421.63",
            "line_4": "92500",
            "line_42": "-239.41",
            "line_56": "100",
        },
        {
            "59": "67800.00",
            "61": "68039.41",
            "62": "68039.41",
            "65": "0",
            "68": "24700.00",
            "69": "0",
            "70": "68039.41",
            "74": "173700.00",
            "76": "2500.00",
            "77": "7400.00",
            "80": "92500",
            "82": "24460.59",
            "83_lesser": "7400.00",
            "83": "7400.00",
            "84": "6712.20",
            "85": "1356.00",
            "86": "592.00",
            "87": "1948.00",
            "88": "8660.20",
            "89_from_line_69": "0",
            "89": "0",
            "90": "8660.20",
            "42100": "8660.20",
            "91_from_line_90": "0",
            "91": "0.00",
        },
        id="line_42_negative",
    ),
    # 6 months for CPP and QPP: lines C, D and F are 35,650.00, 4,950.00 and 1,750.00.
    pytest.param(
        "30000",
        "40000",
        "1800.00",
        "2500.00",
        "0",
        "0",
        "0",
        "10000",
        "2500",
        6,
        6,
        {
            "part_3_line_61": "2195.78",
            "part_3_line_69": "1997.78",
            "line_4": "12500",
            "line_42": "33899.98",
            "line_56": "198.00",
        },
        {
            "59": "33900.00",
            "61": "0.02",
            "62": "0.02",
            "65": "0",
            "68": "0",
            "69": "0",
            "70": "0.02",
            "74": "53100.00",
            "76": "4950.00",
            "77": "0.00",
            "80": "12500",
            "82": "12499.98",
            "83_lesser": "0.00",
            "83": "0.00",
            "84": "0.00",
            "85": "0.00",
            "86": "0.00",
            "87": "0.00",
            "88": "0.00",
            "89_from_line_69": "1997.78",
            "89": "3995.56",
            "90": "-3995.56",
            "42100": "0",
            "91_from_line_90": "3995.56",
            "91": "1997.78",
        },
        id="6_months_on_lines_a_and_b",
    ),
    # Line A of 6 (C = 35,650.00, D = 4,950.00, F = 1,750.00) and line B of 12 (G to J): net self-
    # employment income of 30,000, so line 83 is line D (4,950.00), the lesser of lines 77 and 82.
    pytest.param(
        "20000",
        "30000",
        "500",
        "1000",
        "0",
        "0",
        "30000",
        "0",
        "0",
        6,
        12,
        {
            "part_3_line_61": "-1047.62",
            "part_3_line_69": "-1126.82",
            "line_4": "30000",
            "line_42": "24000.94",
            "line_56": "0",
        },
        {
            "59": "33900.00",
            "61": "9899.06",
            "62": "9899.06",
            "65": "0",
            "68": "0",
            "69": "0",
            "70": "9899.06",
            "74": "76240.00",
            "76": "0.00",
            "77": "4950.00",
            "80": "30000",
            "82": "20100.94",
            "83_lesser": "4950.00",
            "83": "4950.00",
            "84": "980.01",
            "85": "197.98",
            "86": "396.00",
            "87": "593.98",
            "88": "1573.99",
            "89_from_line_69": "0",
            "89": "0",
            "90": "1573.99",
            "42100": "1573.99",
            "91_from_line_90": "0",
            "91": "0.00",
        },
        id="6_months_for_cpp_and_12_for_qpp",
    ),
    # Line 69 of Part 3 is negative, so the amount of line 89 is 0 and line 90 is line 88.
    pytest.param(
        "30000",
        "80000",
        "0",
        "0",
        "0",
        "0",
        "0",
        "10000",
        "2500",
        12,
        12,
        {
            "part_3_line_61": "-4256.00",
            "part_3_line_69": "-4652.00",
            "line_4": "12500",
            "line_42": "-120.97",
            "line_56": "0",
        },
        {
            "59": "67800.00",
            "61": "67920.97",
            "62": "12500",
            "65": "0",
            "68": "0",
            "69": "0",
            "70": "12500",
            "74": "93700.00",
            "76": "0.00",
            "77": "9900.00",
            "80": "12500",
            "82": "0",
            "83_lesser": "0",
            "83": "0",
            "84": "1237.50",
            "85": "250.00",
            "86": "0.00",
            "87": "250.00",
            "88": "1487.50",
            "89_from_line_69": "0",
            "89": "0",
            "90": "1487.50",
            "42100": "1487.50",
            "91_from_line_90": "0",
            "91": "0.00",
        },
        id="line_69_of_part_3_negative",
    ),
    # Line 69 of Part 3 is 0 and no self-employment income: lines 88 and 89 are 0, so line 90 is
    # 0, neither positive nor negative.
    pytest.param(
        "30000",
        "40000",
        "1695.75",
        "2432",
        "0",
        "0",
        "0",
        "0",
        "0",
        12,
        12,
        {
            "part_3_line_61": "0.00",
            "part_3_line_69": "0.00",
            "line_4": "0",
            "line_42": "66500.00",
            "line_56": "0",
        },
        {
            "59": "67800.00",
            "61": "1300.00",
            "62": "0",
            "65": "0",
            "68": "0",
            "69": "0",
            "70": "0",
            "74": "70000",
            "76": "0.00",
            "77": "9900.00",
            "80": "0",
            "82": "0",
            "83_lesser": "0",
            "83": "0",
            "84": "0.00",
            "85": "0.00",
            "86": "0.00",
            "87": "0.00",
            "88": "0.00",
            "89_from_line_69": "0.00",
            "89": "0.00",
            "90": "0.00",
            "42100": "0.00",
            "91_from_line_90": "0",
            "91": "0.00",
        },
        id="line_90_zero",
    ),
]


@pytest.mark.parametrize(
    (
        "line_1",
        "line_2",
        "box_16",
        "box_17",
        "box_16a",
        "box_17a",
        "line_12200",
        "line_2_of_part_4",
        "line_3_of_part_4",
        "months_a",
        "months_b",
        "upstream",
        "expected",
    ),
    PART_4_EARNINGS_CASES,
)
def test_return_bo_part_4_lines_59_to_91(
    line_1: str,
    line_2: str,
    box_16: str,
    box_17: str,
    box_16a: str,
    box_17a: str,
    line_12200: str,
    line_2_of_part_4: str,
    line_3_of_part_4: str,
    months_a: int,
    months_b: int,
    upstream: dict[str, str],
    expected: dict[str, str],
) -> None:
    worksheet = return_bo(
        line_1,
        line_2,
        box_16,
        box_17,
        line_25=box_16a,
        line_45=box_17a,
        cpp_months=months_a,
        qpp_months=months_b,
        cpt20_earnings=line_2_of_part_4,
        cpt20_t4_earnings=line_3_of_part_4,
        net_partnership_income=line_12200,
    )

    assert worksheet.get(RC381_PART_3_LINE_61).value == D(upstream["part_3_line_61"])
    assert worksheet.get(RC381_PART_3_LINE_69).value == D(upstream["part_3_line_69"])
    assert worksheet.get(RC381_PART_4_LINE_4).value == D(upstream["line_4"])
    assert worksheet.get(RC381_PART_4_LINE_42).value == D(upstream["line_42"])
    assert worksheet.get(RC381_PART_4_LINE_56).value == D(upstream["line_56"])
    assert part_4_earnings(worksheet) == {line: D(value) for line, value in expected.items()}


# Part 4, lines 92 to 110 (the base contributions through employment income, the amount for line
# 30800 of the return, and the deduction for the enhanced contributions on employment income, the
# amount for line 22215). Lines 92, 99 and 106 choose by the sign of lines 53, 60 and 68 of Part 3
# ("If line 53 of Part 3 is positive or "0", enter the amount from line 52 of Part 3 at line 92
# and line 98, and continue at line 99. If not, enter the amount from line 49 of Part 3 and
# continue at line 93."), and the lines in between are completed only for the other sign. They are
# computed whatever the signs are (as Part 4's earlier blocks are), each giving the "0" the form
# enters where it is not completed, which the tests below pin. "104_difference" is the "result of
# line 68 of Part 3 minus line 97" printed inside line 104. Lines 92 to 110 repeat Part 3b's lines
# 75 to 93 on the same Part 3 totals ("PART_3B" maps them).
PART_4_EMPLOYMENT_KINDS: dict[str, ArtifactKind[Decimal]] = {
    "92": RC381_PART_4_LINE_92,
    "93": RC381_PART_4_LINE_93,
    "94": RC381_PART_4_LINE_94,
    "95": RC381_PART_4_LINE_95,
    "96": RC381_PART_4_LINE_96,
    "97": RC381_PART_4_LINE_97,
    "98": RC381_PART_4_LINE_98,
    "99": RC381_PART_4_LINE_99,
    "100": RC381_PART_4_LINE_100,
    "101": RC381_PART_4_LINE_101,
    "102": RC381_PART_4_LINE_102,
    "103": RC381_PART_4_LINE_103,
    "104_difference": RC381_PART_4_LINE_104_DIFFERENCE,
    "104": RC381_PART_4_LINE_104,
    "105": RC381_PART_4_LINE_105,
    "106": RC381_PART_4_LINE_106,
    "107": RC381_PART_4_LINE_107,
    "108": RC381_PART_4_LINE_108,
    "109": RC381_PART_4_LINE_109,
    "110": RC381_PART_4_LINE_110,
}

# Part 4's line, Part 3b's line.
PART_3B_OF_PART_4: dict[str, str] = {
    "92": "75",
    "93": "76",
    "94": "77",
    "95": "78",
    "96": "79",
    "97": "80",
    "98": "81",
    "99": "82",
    "100": "83",
    "101": "84",
    "102": "85",
    "103": "86",
    "104_difference": "87h",
    "104": "87",
    "105": "88",
    "106": "89",
    "107": "90",
    "108": "91",
    "109": "92",
    "110": "93",
}


def part_4_employment(worksheet: Worksheet) -> dict[str, Decimal]:
    """Part 4's lines 92 to 110 of `worksheet`, by line number (see `PART_4_EMPLOYMENT_KINDS`)."""
    return {line: worksheet.get(kind).value for line, kind in PART_4_EMPLOYMENT_KINDS.items()}


def test_return_bo_part_4_lines_92_to_110_match_the_tickets_example() -> None:
    # Return BO: line 53 of Part 3 = 144.11 and line 60 = 28.14 are positive and line 68 = 0, so
    # the form enters line 52 (3,462.75) at lines 92 and 98 and line 59 (665.00) at lines 99 and
    # 105, and line 67 (0) at lines 106 and 109. Lines 93 to 95, 97, 100 to 102, 104, 107 and 108
    # are not completed: "0". Line 98 = 3,462.75 + 0 and line 110 = 665.00 + 0.00: the ticket's
    # amounts for line 30800 and line 22215.
    worksheet = return_bo()

    assert worksheet.get(RC381_PART_3_LINE_53).value == D("144.11")
    assert worksheet.get(RC381_PART_3_LINE_60).value == D("28.14")
    assert worksheet.get(RC381_PART_3_LINE_68).value == D("0")
    assert part_4_employment(worksheet) == {
        "92": D("3462.75"),
        "93": D("0"),
        "94": D("0"),
        "95": D("0"),
        "96": D("3462.75"),
        "97": D("0"),
        "98": D("3462.75"),
        "99": D("665.00"),
        "100": D("0"),
        "101": D("0"),
        "102": D("0"),
        "103": D("665.00"),
        "104_difference": D("0.00"),
        "104": D("0"),
        "105": D("665.00"),
        "106": D("0.00"),
        "107": D("0"),
        "108": D("0"),
        "109": D("0.00"),
        "110": D("665.00"),
    }
    assert worksheet.get(RC381_PART_4_LINE_98).value == worksheet.get(RC381_PART_3_LINE_52).value
    assert worksheet.get(RC381_PART_4_LINE_110).value == worksheet.get(RC381_PART_3_LINE_59).value


def test_return_bo_part_4_lines_92_to_110_with_lines_53_60_and_68_all_zero() -> None:
    # Box 16 of 1,695.20 and box 17 of 2,432.55: lines 53, 60, 61 and 68 of Part 3 are 0, "positive
    # or 0" each: line 92 = line 52 = 3,462.75, line 99 = line 59 = 665.00 and line 106 = line 67 =
    # 0. Line 98 = 3,462.75 and line 110 = 665.00.
    worksheet = return_bo(line_19="1695.20", line_39="2432.55")

    assert worksheet.get(RC381_PART_3_LINE_53).value == D("0")
    assert worksheet.get(RC381_PART_3_LINE_60).value == D("0")
    assert worksheet.get(RC381_PART_3_LINE_68).value == D("0")
    assert part_4_employment(worksheet) == {
        "92": D("3462.75"),
        "93": D("0"),
        "94": D("0"),
        "95": D("0"),
        "96": D("3462.75"),
        "97": D("0"),
        "98": D("3462.75"),
        "99": D("665.00"),
        "100": D("0"),
        "101": D("0"),
        "102": D("0"),
        "103": D("665.00"),
        "104_difference": D("0.00"),
        "104": D("0"),
        "105": D("665.00"),
        "106": D("0.00"),
        "107": D("0"),
        "108": D("0"),
        "109": D("0.00"),
        "110": D("665.00"),
    }


def test_return_bo_part_4_line_92_takes_line_52_at_a_line_53_of_zero_and_line_49_below_it() -> None:
    # Line 53 of Part 3 of exactly 0 is "positive or "0"": line 92 = line 52 (3,462.75), line 93 =
    # 0. A line 53 of -0.01 is negative: line 92 = line 49 (3,462.74), line 93 = 0.01, line 94 = 0
    # (line 60 is 0, not positive), line 95 = 0.01 and, with line 68 at 0, line 97 = 0, so line 98
    # = 3,462.74.
    zero = return_bo(line_19="1695", line_39="2432.73")
    negative = return_bo(line_19="1695.13", line_39="2432.61")

    assert zero.get(RC381_PART_3_LINE_53).value == D("0")
    assert zero.get(RC381_PART_4_LINE_92).value == D("3462.75")
    assert zero.get(RC381_PART_4_LINE_93).value == D("0")
    assert zero.get(RC381_PART_4_LINE_98).value == D("3462.75")
    assert negative.get(RC381_PART_3_LINE_53).value == D("-0.01")
    assert negative.get(RC381_PART_3_LINE_49).value == D("3462.74")
    assert negative.get(RC381_PART_4_LINE_92).value == D("3462.74")
    assert negative.get(RC381_PART_4_LINE_93).value == D("0.01")
    assert negative.get(RC381_PART_4_LINE_94).value == D("0")
    assert negative.get(RC381_PART_4_LINE_95).value == D("0.01")
    assert negative.get(RC381_PART_4_LINE_97).value == D("0")
    assert negative.get(RC381_PART_4_LINE_98).value == D("3462.74")


def test_return_bo_part_4_line_99_takes_line_59_at_a_line_60_of_zero_and_line_56_below_it() -> None:
    # Line 60 of Part 3 of exactly 0 (line 53 = 0.06) or of 0.01 is "positive or "0"": line 99 =
    # line 59 (665.00) and line 100 = 0. A line 60 of -0.02 (line 53 = 0) is negative: line 99 =
    # line 56 (664.98), line 100 = 0.02, line 101 = 0 (line 53 is not positive), line 102 = 0.02,
    # line 103 = 664.98 and line 105 = 664.98 + 0.
    zero = return_bo(line_19="1695", line_39="2432.81")
    cent = return_bo(line_19="1695.79", line_39="2431.97")
    negative = return_bo(line_19="1695", line_39="2432.73")

    assert zero.get(RC381_PART_3_LINE_60).value == D("0")
    assert zero.get(RC381_PART_4_LINE_99).value == D("665.00")
    assert zero.get(RC381_PART_4_LINE_100).value == D("0")
    assert zero.get(RC381_PART_4_LINE_105).value == D("665.00")
    assert cent.get(RC381_PART_3_LINE_60).value == D("0.01")
    assert cent.get(RC381_PART_4_LINE_99).value == D("665.00")
    assert cent.get(RC381_PART_4_LINE_100).value == D("0")
    assert cent.get(RC381_PART_4_LINE_105).value == D("665.00")
    assert negative.get(RC381_PART_3_LINE_60).value == D("-0.02")
    assert negative.get(RC381_PART_3_LINE_56).value == D("664.98")
    assert negative.get(RC381_PART_4_LINE_99).value == D("664.98")
    assert negative.get(RC381_PART_4_LINE_100).value == D("0.02")
    assert negative.get(RC381_PART_4_LINE_101).value == D("0")
    assert negative.get(RC381_PART_4_LINE_102).value == D("0.02")
    assert negative.get(RC381_PART_4_LINE_103).value == D("664.98")
    assert negative.get(RC381_PART_4_LINE_105).value == D("664.98")


def test_return_bo_part_4_line_106_is_line_67_for_a_line_68_of_zero_or_more_and_line_64_below() -> (
    None
):
    # Line 68 of Part 3 of 0 (the ticket's example) or positive (20.00): line 106 = line 67 (0.00
    # and 396.00) and line 107 = 0. Negative (-296.00, line 64 = 100 and line 67 = 396.00): line 106
    # = line 64 (100), line 107 = 296.00 and line 109 = 100 + line 108 (line 61 = 176.00 is the
    # lesser) = 276.00.
    zero = return_bo()
    positive = return_bo(
        line_1="60000", line_2="50000", line_19="3500", line_39="2432", line_25="396", line_45="20"
    )
    negative = return_bo(
        line_1="30000", line_2="80000", line_19="2000", line_39="2432", line_25="100"
    )

    assert zero.get(RC381_PART_3_LINE_68).value == D("0")
    assert zero.get(RC381_PART_4_LINE_106).value == D("0.00")
    assert zero.get(RC381_PART_4_LINE_107).value == D("0")
    assert positive.get(RC381_PART_3_LINE_68).value == D("20.00")
    assert positive.get(RC381_PART_3_LINE_67).value == D("396.00")
    assert positive.get(RC381_PART_4_LINE_106).value == D("396.00")
    assert positive.get(RC381_PART_4_LINE_107).value == D("0")
    assert positive.get(RC381_PART_4_LINE_108).value == D("0")
    assert negative.get(RC381_PART_3_LINE_68).value == D("-296.00")
    assert negative.get(RC381_PART_3_LINE_64).value == D("100")
    assert negative.get(RC381_PART_4_LINE_106).value == D("100")
    assert negative.get(RC381_PART_4_LINE_107).value == D("296.00")
    assert negative.get(RC381_PART_4_LINE_108).value == D("176.00")
    assert negative.get(RC381_PART_4_LINE_109).value == D("276.00")


# Each case: box 26 outside and in Quebec (lines 1 and 2 of Part 3), box 16, box 17, box 16A and
# box 17A (lines 19, 39, 25 and 45), then the lines of Part 3 that Part 4's lines 92 to 110 read
# (49, 52, 53, 56, 59, 60, 61, 64, 67 and 68) and Part 4's lines 92 to 110. The figures are proved
# by an independent Decimal model of the printed form (not by this engine). The cases vary the
# signs of lines 53, 60, 61 and 68 of Part 3 and which of the two lines each "whichever is less"
# takes. The CPT20 election and net self-employment income do not reach lines 92 to 110, so they
# stay at their defaults.
PART_4_EMPLOYMENT_CASES = [
    # The example of Return BO: lines 53 and 60 of Part 3 are positive and line 68 is 0, so lines 92
    # and 99 take lines 52 and 59 and line 106 takes line 67.
    pytest.param(
        "30000",
        "40000",
        "1800.00",
        "2500.00",
        "0",
        "0",
        {
            "part_3_line_49": "3606.86",
            "part_3_line_52": "3462.75",
            "part_3_line_53": "144.11",
            "part_3_line_56": "693.14",
            "part_3_line_59": "665.00",
            "part_3_line_60": "28.14",
            "part_3_line_61": "172.25",
            "part_3_line_64": "0",
            "part_3_line_67": "0.00",
            "part_3_line_68": "0.00",
        },
        {
            "92": "3462.75",
            "93": "0",
            "94": "0",
            "95": "0",
            "96": "3462.75",
            "97": "0",
            "98": "3462.75",
            "99": "665.00",
            "100": "0",
            "101": "0",
            "102": "0",
            "103": "665.00",
            "104_difference": "0.00",
            "104": "0",
            "105": "665.00",
            "106": "0.00",
            "107": "0",
            "108": "0",
            "109": "0.00",
            "110": "665.00",
        },
        id="ticket_example",
    ),
    # Lines 53, 60 and 68 of Part 3 are all 0, each in the "positive or 0" branch.
    pytest.param(
        "30000",
        "40000",
        "1695.20",
        "2432.55",
        "0",
        "0",
        {
            "part_3_line_49": "3462.75",
            "part_3_line_52": "3462.75",
            "part_3_line_53": "0.00",
            "part_3_line_56": "665.00",
            "part_3_line_59": "665.00",
            "part_3_line_60": "0.00",
            "part_3_line_61": "0.00",
            "part_3_line_64": "0",
            "part_3_line_67": "0.00",
            "part_3_line_68": "0.00",
        },
        {
            "92": "3462.75",
            "93": "0",
            "94": "0",
            "95": "0",
            "96": "3462.75",
            "97": "0",
            "98": "3462.75",
            "99": "665.00",
            "100": "0",
            "101": "0",
            "102": "0",
            "103": "665.00",
            "104_difference": "0.00",
            "104": "0",
            "105": "665.00",
            "106": "0.00",
            "107": "0",
            "108": "0",
            "109": "0.00",
            "110": "665.00",
        },
        id="lines_53_60_and_68_all_zero",
    ),
    # Line 53 of Part 3 is -28.74 and line 60 is 28.74: line 92 = line 49, line 93 = 28.74, line 94
    # = the lesser of 28.74 and 28.74, line 95 = 0, and line 98 = 3,434.01 + 28.74 = line 52.
    pytest.param(
        "30000",
        "40000",
        "4127.75",
        "0",
        "0",
        "0",
        {
            "part_3_line_49": "3434.01",
            "part_3_line_52": "3462.75",
            "part_3_line_53": "-28.74",
            "part_3_line_56": "693.74",
            "part_3_line_59": "665.00",
            "part_3_line_60": "28.74",
            "part_3_line_61": "0.00",
            "part_3_line_64": "0",
            "part_3_line_67": "0.00",
            "part_3_line_68": "0.00",
        },
        {
            "92": "3434.01",
            "93": "28.74",
            "94": "28.74",
            "95": "0.00",
            "96": "3462.75",
            "97": "0",
            "98": "3462.75",
            "99": "665.00",
            "100": "0",
            "101": "0",
            "102": "0",
            "103": "665.00",
            "104_difference": "0.00",
            "104": "0",
            "105": "665.00",
            "106": "0.00",
            "107": "0",
            "108": "0",
            "109": "0.00",
            "110": "665.00",
        },
        id="lines_60_and_93_the_same_amount",
    ),
    # Line 60 of Part 3 (39.20) is more than line 93 (15.20): line 94 = line 93 and line 95 = 0.
    pytest.param(
        "0",
        "50000",
        "3000",
        "0",
        "0",
        "0",
        {
            "part_3_line_49": "2495.80",
            "part_3_line_52": "2511.00",
            "part_3_line_53": "-15.20",
            "part_3_line_56": "504.20",
            "part_3_line_59": "465.00",
            "part_3_line_60": "39.20",
            "part_3_line_61": "24.00",
            "part_3_line_64": "0",
            "part_3_line_67": "0.00",
            "part_3_line_68": "0.00",
        },
        {
            "92": "2495.80",
            "93": "15.20",
            "94": "15.20",
            "95": "0.00",
            "96": "2511.00",
            "97": "0",
            "98": "2511.00",
            "99": "465.00",
            "100": "0",
            "101": "0",
            "102": "0",
            "103": "465.00",
            "104_difference": "0.00",
            "104": "0",
            "105": "465.00",
            "106": "0.00",
            "107": "0",
            "108": "0",
            "109": "0.00",
            "110": "465.00",
        },
        id="line_94_is_line_93_when_line_60_is_more",
    ),
    # Line 60 of Part 3 (17.38) is less than line 93 (53.18): line 94 = line 60, line 95 = 35.80;
    # line 68 of Part 3 (50.00, positive) is more than line 95, so line 97 = line 95.
    pytest.param(
        "1000",
        "50000",
        "2000",
        "1000",
        "50",
        "0",
        {
            "part_3_line_49": "2507.62",
            "part_3_line_52": "2560.80",
            "part_3_line_53": "-53.18",
            "part_3_line_56": "492.38",
            "part_3_line_59": "475.00",
            "part_3_line_60": "17.38",
            "part_3_line_61": "-35.80",
            "part_3_line_64": "50",
            "part_3_line_67": "0.00",
            "part_3_line_68": "50.00",
        },
        {
            "92": "2507.62",
            "93": "53.18",
            "94": "17.38",
            "95": "35.80",
            "96": "2525.00",
            "97": "35.80",
            "98": "2560.80",
            "99": "475.00",
            "100": "0",
            "101": "0",
            "102": "0",
            "103": "475.00",
            "104_difference": "14.20",
            "104": "0",
            "105": "475.00",
            "106": "0.00",
            "107": "0",
            "108": "0",
            "109": "0.00",
            "110": "475.00",
        },
        id="line_94_is_line_60_when_that_is_less_and_line_97_is_line_95",
    ),
    # Line 53 negative, line 60 positive and line 68 positive and less than line 95 (20.76): line 97
    # = line 68.
    pytest.param(
        "50000",
        "30000",
        "4127.75",
        "0",
        "50",
        "300",
        {
            "part_3_line_49": "3434.01",
            "part_3_line_52": "3470.51",
            "part_3_line_53": "-36.50",
            "part_3_line_56": "693.74",
            "part_3_line_59": "678.00",
            "part_3_line_60": "15.74",
            "part_3_line_61": "-20.76",
            "part_3_line_64": "350",
            "part_3_line_67": "348.00",
            "part_3_line_68": "2.00",
        },
        {
            "92": "3434.01",
            "93": "36.50",
            "94": "15.74",
            "95": "20.76",
            "96": "3449.75",
            "97": "2.00",
            "98": "3451.75",
            "99": "678.00",
            "100": "0",
            "101": "0",
            "102": "0",
            "103": "678.00",
            "104_difference": "0.00",
            "104": "0",
            "105": "678.00",
            "106": "348.00",
            "107": "0",
            "108": "0",
            "109": "348.00",
            "110": "1026.00",
        },
        id="line_97_is_line_68_when_that_is_the_lesser",
    ),
    # Line 60 of Part 3 is negative and line 53 positive and more than line 100: line 99 = line 56,
    # line 101 = line 100 and line 102 = 0.
    pytest.param(
        "50000",
        "1500",
        "500",
        "2500",
        "0",
        "0",
        {
            "part_3_line_49": "2525.35",
            "part_3_line_52": "2382.29",
            "part_3_line_53": "143.06",
            "part_3_line_56": "474.65",
            "part_3_line_59": "480.00",
            "part_3_line_60": "-5.35",
            "part_3_line_61": "137.71",
            "part_3_line_64": "0",
            "part_3_line_67": "0.00",
            "part_3_line_68": "0.00",
        },
        {
            "92": "2382.29",
            "93": "0",
            "94": "0",
            "95": "0",
            "96": "2382.29",
            "97": "0",
            "98": "2382.29",
            "99": "474.65",
            "100": "5.35",
            "101": "5.35",
            "102": "0.00",
            "103": "480.00",
            "104_difference": "0.00",
            "104": "0",
            "105": "480.00",
            "106": "0.00",
            "107": "0",
            "108": "0",
            "109": "0.00",
            "110": "480.00",
        },
        id="line_101_is_line_100_when_line_53_is_more",
    ),
    # Line 60 of Part 3 is negative and line 53 positive and less than line 100: line 101 = line 53,
    # and line 102 is above 0 while line 68 is 0, so line 104 = 0.
    pytest.param(
        "70000",
        "40000",
        "0",
        "4127.75",
        "396",
        "0",
        {
            "part_3_line_49": "3482.79",
            "part_3_line_52": "3467.05",
            "part_3_line_53": "15.74",
            "part_3_line_56": "644.96",
            "part_3_line_59": "678.00",
            "part_3_line_60": "-33.04",
            "part_3_line_61": "-17.30",
            "part_3_line_64": "396",
            "part_3_line_67": "396.00",
            "part_3_line_68": "0.00",
        },
        {
            "92": "3467.05",
            "93": "0",
            "94": "0",
            "95": "0",
            "96": "3467.05",
            "97": "0",
            "98": "3467.05",
            "99": "644.96",
            "100": "33.04",
            "101": "15.74",
            "102": "17.30",
            "103": "660.70",
            "104_difference": "0.00",
            "104": "0",
            "105": "660.70",
            "106": "396.00",
            "107": "0",
            "108": "0",
            "109": "396.00",
            "110": "1056.70",
        },
        id="line_101_is_line_53_when_that_is_less",
    ),
    # Line 68 of Part 3 (68.00) is positive and line 97 is 0 (line 53 is positive): line 104 = the
    # lesser of line 102 (20.76) and line 68 less line 97 (68.00).
    pytest.param(
        "50000",
        "30000",
        "0",
        "4127.75",
        "396",
        "20",
        {
            "part_3_line_49": "3482.79",
            "part_3_line_52": "3470.51",
            "part_3_line_53": "12.28",
            "part_3_line_56": "644.96",
            "part_3_line_59": "678.00",
            "part_3_line_60": "-33.04",
            "part_3_line_61": "-20.76",
            "part_3_line_64": "416",
            "part_3_line_67": "348.00",
            "part_3_line_68": "68.00",
        },
        {
            "92": "3470.51",
            "93": "0",
            "94": "0",
            "95": "0",
            "96": "3470.51",
            "97": "0",
            "98": "3470.51",
            "99": "644.96",
            "100": "33.04",
            "101": "12.28",
            "102": "20.76",
            "103": "657.24",
            "104_difference": "68.00",
            "104": "20.76",
            "105": "678.00",
            "106": "348.00",
            "107": "0",
            "108": "0",
            "109": "348.00",
            "110": "1026.00",
        },
        id="line_104_is_line_102_when_that_is_the_lesser",
    ),
    # Line 68 of Part 3 (4.00) is positive and line 97 is 0 (line 53 is positive): line 104 = line
    # 68 less line 97 (4.00), less than line 102 (8.05).
    pytest.param(
        "60000",
        "30000",
        "1695.75",
        "2432",
        "100",
        "300",
        {
            "part_3_line_49": "3462.75",
            "part_3_line_52": "3457.80",
            "part_3_line_53": "4.95",
            "part_3_line_56": "665.00",
            "part_3_line_59": "678.00",
            "part_3_line_60": "-13.00",
            "part_3_line_61": "-8.05",
            "part_3_line_64": "400",
            "part_3_line_67": "396.00",
            "part_3_line_68": "4.00",
        },
        {
            "92": "3457.80",
            "93": "0",
            "94": "0",
            "95": "0",
            "96": "3457.80",
            "97": "0",
            "98": "3457.80",
            "99": "665.00",
            "100": "13.00",
            "101": "4.95",
            "102": "8.05",
            "103": "669.95",
            "104_difference": "4.00",
            "104": "4.00",
            "105": "673.95",
            "106": "396.00",
            "107": "0",
            "108": "0",
            "109": "396.00",
            "110": "1069.95",
        },
        id="line_104_is_line_68_less_line_97_when_line_53_is_positive",
    ),
    # Lines 53, 60 and 61 of Part 3 negative and line 68 positive: line 97 = line 95 (190.89, less
    # than line 68), line 104 = the lesser of line 102 (17.55) and line 68 less line 97 (213.11).
    pytest.param(
        "60000",
        "80000",
        "3000",
        "1000",
        "500",
        "300",
        {
            "part_3_line_49": "3339.55",
            "part_3_line_52": "3530.44",
            "part_3_line_53": "-190.89",
            "part_3_line_56": "660.45",
            "part_3_line_59": "678.00",
            "part_3_line_60": "-17.55",
            "part_3_line_61": "-208.44",
            "part_3_line_64": "800",
            "part_3_line_67": "396.00",
            "part_3_line_68": "404.00",
        },
        {
            "92": "3339.55",
            "93": "190.89",
            "94": "0",
            "95": "190.89",
            "96": "3339.55",
            "97": "190.89",
            "98": "3530.44",
            "99": "660.45",
            "100": "17.55",
            "101": "0",
            "102": "17.55",
            "103": "660.45",
            "104_difference": "213.11",
            "104": "17.55",
            "105": "678.00",
            "106": "396.00",
            "107": "0",
            "108": "0",
            "109": "396.00",
            "110": "1074.00",
        },
        id="lines_53_and_60_negative_and_line_104_is_line_102",
    ),
    # Lines 53 and 60 of Part 3 negative and line 68 positive (500.00): line 97 = line 95 (435.00),
    # line 104 = line 68 less line 97 (65.00), less than line 102 (96.25).
    pytest.param(
        "20000",
        "40000",
        "0",
        "3000",
        "500",
        "0",
        {
            "part_3_line_49": "2531.25",
            "part_3_line_52": "2966.25",
            "part_3_line_53": "-435.00",
            "part_3_line_56": "468.75",
            "part_3_line_59": "565.00",
            "part_3_line_60": "-96.25",
            "part_3_line_61": "-531.25",
            "part_3_line_64": "500",
            "part_3_line_67": "0.00",
            "part_3_line_68": "500.00",
        },
        {
            "92": "2531.25",
            "93": "435.00",
            "94": "0",
            "95": "435.00",
            "96": "2531.25",
            "97": "435.00",
            "98": "2966.25",
            "99": "468.75",
            "100": "96.25",
            "101": "0",
            "102": "96.25",
            "103": "468.75",
            "104_difference": "65.00",
            "104": "65.00",
            "105": "533.75",
            "106": "0.00",
            "107": "0",
            "108": "0",
            "109": "0.00",
            "110": "533.75",
        },
        id="lines_53_and_60_negative_and_line_104_is_line_68_less_line_97",
    ),
    # Line 97 = line 68 (20.00, less than line 95): line 68 less line 97 = 0, so line 104 = 0
    # although line 102 (206.23) is above 0.
    pytest.param(
        "40000",
        "30000",
        "1800",
        "1000",
        "0",
        "20",
        {
            "part_3_line_49": "2341.23",
            "part_3_line_52": "3420.00",
            "part_3_line_53": "-1078.77",
            "part_3_line_56": "458.77",
            "part_3_line_59": "665.00",
            "part_3_line_60": "-206.23",
            "part_3_line_61": "-1285.00",
            "part_3_line_64": "20",
            "part_3_line_67": "0.00",
            "part_3_line_68": "20.00",
        },
        {
            "92": "2341.23",
            "93": "1078.77",
            "94": "0",
            "95": "1078.77",
            "96": "2341.23",
            "97": "20.00",
            "98": "2361.23",
            "99": "458.77",
            "100": "206.23",
            "101": "0",
            "102": "206.23",
            "103": "458.77",
            "104_difference": "0.00",
            "104": "0.00",
            "105": "458.77",
            "106": "0.00",
            "107": "0",
            "108": "0",
            "109": "0.00",
            "110": "458.77",
        },
        id="line_104_is_zero_when_line_97_takes_all_of_line_68",
    ),
    # Line 68 of Part 3 is negative (-278.00): line 106 = line 64, line 107 = 278.00 and line 108 =
    # the lesser of line 61 (4,402.96) and line 107.
    pytest.param(
        "30000",
        "50000",
        "4127.75",
        "4500",
        "50",
        "20",
        {
            "part_3_line_49": "7230.89",
            "part_3_line_52": "3546.79",
            "part_3_line_53": "3684.10",
            "part_3_line_56": "1396.86",
            "part_3_line_59": "678.00",
            "part_3_line_60": "718.86",
            "part_3_line_61": "4402.96",
            "part_3_line_64": "70",
            "part_3_line_67": "348.00",
            "part_3_line_68": "-278.00",
        },
        {
            "92": "3546.79",
            "93": "0",
            "94": "0",
            "95": "0",
            "96": "3546.79",
            "97": "0",
            "98": "3546.79",
            "99": "678.00",
            "100": "0",
            "101": "0",
            "102": "0",
            "103": "678.00",
            "104_difference": "-278.00",
            "104": "0",
            "105": "678.00",
            "106": "70",
            "107": "278.00",
            "108": "278.00",
            "109": "348.00",
            "110": "1026.00",
        },
        id="line_108_is_line_107_when_that_is_the_lesser",
    ),
    # Line 68 of Part 3 is negative (-296.00) and line 61 positive and less than line 107: line 108
    # = line 61 (176.00).
    pytest.param(
        "30000",
        "80000",
        "2000",
        "2432",
        "100",
        "0",
        {
            "part_3_line_49": "3715.87",
            "part_3_line_52": "3578.00",
            "part_3_line_53": "137.87",
            "part_3_line_56": "716.13",
            "part_3_line_59": "678.00",
            "part_3_line_60": "38.13",
            "part_3_line_61": "176.00",
            "part_3_line_64": "100",
            "part_3_line_67": "396.00",
            "part_3_line_68": "-296.00",
        },
        {
            "92": "3578.00",
            "93": "0",
            "94": "0",
            "95": "0",
            "96": "3578.00",
            "97": "0",
            "98": "3578.00",
            "99": "678.00",
            "100": "0",
            "101": "0",
            "102": "0",
            "103": "678.00",
            "104_difference": "-296.00",
            "104": "0",
            "105": "678.00",
            "106": "100",
            "107": "296.00",
            "108": "176.00",
            "109": "276.00",
            "110": "954.00",
        },
        id="line_108_is_line_61_when_that_is_the_lesser",
    ),
    # Line 68 of Part 3 is negative but line 61 is not positive: line 108 = 0.
    pytest.param(
        "0",
        "80000",
        "500",
        "0",
        "50",
        "20",
        {
            "part_3_line_49": "415.97",
            "part_3_line_52": "3661.20",
            "part_3_line_53": "-3245.23",
            "part_3_line_56": "84.03",
            "part_3_line_59": "678.00",
            "part_3_line_60": "-593.97",
            "part_3_line_61": "-3839.20",
            "part_3_line_64": "70",
            "part_3_line_67": "348.00",
            "part_3_line_68": "-278.00",
        },
        {
            "92": "415.97",
            "93": "3245.23",
            "94": "0",
            "95": "3245.23",
            "96": "415.97",
            "97": "0",
            "98": "415.97",
            "99": "84.03",
            "100": "593.97",
            "101": "0",
            "102": "593.97",
            "103": "84.03",
            "104_difference": "-278.00",
            "104": "0",
            "105": "84.03",
            "106": "70",
            "107": "278.00",
            "108": "0",
            "109": "70",
            "110": "154.03",
        },
        id="line_68_negative_and_line_61_negative",
    ),
    # Line 68 of Part 3 is positive: line 106 = line 67 and line 108 = 0.
    pytest.param(
        "60000",
        "50000",
        "3500",
        "2432",
        "396",
        "20",
        {
            "part_3_line_49": "4963.77",
            "part_3_line_52": "3494.78",
            "part_3_line_53": "1468.99",
            "part_3_line_56": "968.23",
            "part_3_line_59": "678.01",
            "part_3_line_60": "290.22",
            "part_3_line_61": "1759.21",
            "part_3_line_64": "416",
            "part_3_line_67": "396.00",
            "part_3_line_68": "20.00",
        },
        {
            "92": "3494.78",
            "93": "0",
            "94": "0",
            "95": "0",
            "96": "3494.78",
            "97": "0",
            "98": "3494.78",
            "99": "678.01",
            "100": "0",
            "101": "0",
            "102": "0",
            "103": "678.01",
            "104_difference": "20.00",
            "104": "0",
            "105": "678.01",
            "106": "396.00",
            "107": "0",
            "108": "0",
            "109": "396.00",
            "110": "1074.01",
        },
        id="line_68_positive_and_lines_53_and_60_positive",
    ),
    # Line 53 of Part 3 is exactly 0 ("positive or 0": line 92 = line 52) and line 60 is -0.02
    # (negative): line 99 = line 56, line 100 = 0.02 and line 101 = 0 (line 53 is not positive).
    pytest.param(
        "30000",
        "40000",
        "1695",
        "2432.73",
        "0",
        "0",
        {
            "part_3_line_49": "3462.75",
            "part_3_line_52": "3462.75",
            "part_3_line_53": "0.00",
            "part_3_line_56": "664.98",
            "part_3_line_59": "665.00",
            "part_3_line_60": "-0.02",
            "part_3_line_61": "-0.02",
            "part_3_line_64": "0",
            "part_3_line_67": "0.00",
            "part_3_line_68": "0.00",
        },
        {
            "92": "3462.75",
            "93": "0",
            "94": "0",
            "95": "0",
            "96": "3462.75",
            "97": "0",
            "98": "3462.75",
            "99": "664.98",
            "100": "0.02",
            "101": "0",
            "102": "0.02",
            "103": "664.98",
            "104_difference": "0.00",
            "104": "0",
            "105": "664.98",
            "106": "0.00",
            "107": "0",
            "108": "0",
            "109": "0.00",
            "110": "664.98",
        },
        id="line_53_zero_and_line_60_negative",
    ),
    # Line 60 of Part 3 is exactly 0 ("positive or 0": line 99 = line 59) and line 53 is 0.06.
    pytest.param(
        "30000",
        "40000",
        "1695",
        "2432.81",
        "0",
        "0",
        {
            "part_3_line_49": "3462.81",
            "part_3_line_52": "3462.75",
            "part_3_line_53": "0.06",
            "part_3_line_56": "665.00",
            "part_3_line_59": "665.00",
            "part_3_line_60": "0.00",
            "part_3_line_61": "0.06",
            "part_3_line_64": "0",
            "part_3_line_67": "0.00",
            "part_3_line_68": "0.00",
        },
        {
            "92": "3462.75",
            "93": "0",
            "94": "0",
            "95": "0",
            "96": "3462.75",
            "97": "0",
            "98": "3462.75",
            "99": "665.00",
            "100": "0",
            "101": "0",
            "102": "0",
            "103": "665.00",
            "104_difference": "0.00",
            "104": "0",
            "105": "665.00",
            "106": "0.00",
            "107": "0",
            "108": "0",
            "109": "0.00",
            "110": "665.00",
        },
        id="line_53_positive_and_line_60_zero",
    ),
    # Line 53 of Part 3 is -0.01 (negative: line 92 = line 49, line 93 = 0.01 and line 95 = 0.01)
    # and line 60 is exactly 0: line 94 = 0 (line 60 is not positive).
    pytest.param(
        "30000",
        "40000",
        "1695.13",
        "2432.61",
        "0",
        "0",
        {
            "part_3_line_49": "3462.74",
            "part_3_line_52": "3462.75",
            "part_3_line_53": "-0.01",
            "part_3_line_56": "665.00",
            "part_3_line_59": "665.00",
            "part_3_line_60": "0.00",
            "part_3_line_61": "-0.01",
            "part_3_line_64": "0",
            "part_3_line_67": "0.00",
            "part_3_line_68": "0.00",
        },
        {
            "92": "3462.74",
            "93": "0.01",
            "94": "0",
            "95": "0.01",
            "96": "3462.74",
            "97": "0",
            "98": "3462.74",
            "99": "665.00",
            "100": "0",
            "101": "0",
            "102": "0",
            "103": "665.00",
            "104_difference": "0.00",
            "104": "0",
            "105": "665.00",
            "106": "0.00",
            "107": "0",
            "108": "0",
            "109": "0.00",
            "110": "665.00",
        },
        id="line_53_negative_by_a_cent_and_line_60_zero",
    ),
    # Line 53 of Part 3 is exactly 0 and line 60 is 0.01 (positive): line 92 = line 52 and line 94 =
    # 0 (line 53 is not negative).
    pytest.param(
        "30000",
        "40000",
        "1695.79",
        "2431.97",
        "0",
        "0",
        {
            "part_3_line_49": "3462.75",
            "part_3_line_52": "3462.75",
            "part_3_line_53": "0.00",
            "part_3_line_56": "665.01",
            "part_3_line_59": "665.00",
            "part_3_line_60": "0.01",
            "part_3_line_61": "0.01",
            "part_3_line_64": "0",
            "part_3_line_67": "0.00",
            "part_3_line_68": "0.00",
        },
        {
            "92": "3462.75",
            "93": "0",
            "94": "0",
            "95": "0",
            "96": "3462.75",
            "97": "0",
            "98": "3462.75",
            "99": "665.00",
            "100": "0",
            "101": "0",
            "102": "0",
            "103": "665.00",
            "104_difference": "0.00",
            "104": "0",
            "105": "665.00",
            "106": "0.00",
            "107": "0",
            "108": "0",
            "109": "0.00",
            "110": "665.00",
        },
        id="line_53_zero_and_line_60_positive_by_a_cent",
    ),
]


@pytest.mark.parametrize(
    (
        "line_1",
        "line_2",
        "box_16",
        "box_17",
        "box_16a",
        "box_17a",
        "upstream",
        "expected",
    ),
    PART_4_EMPLOYMENT_CASES,
)
def test_return_bo_part_4_lines_92_to_110(
    line_1: str,
    line_2: str,
    box_16: str,
    box_17: str,
    box_16a: str,
    box_17a: str,
    upstream: dict[str, str],
    expected: dict[str, str],
) -> None:
    worksheet = return_bo(line_1, line_2, box_16, box_17, line_25=box_16a, line_45=box_17a)

    part_3_kinds = {
        "part_3_line_49": RC381_PART_3_LINE_49,
        "part_3_line_52": RC381_PART_3_LINE_52,
        "part_3_line_53": RC381_PART_3_LINE_53,
        "part_3_line_56": RC381_PART_3_LINE_56,
        "part_3_line_59": RC381_PART_3_LINE_59,
        "part_3_line_60": RC381_PART_3_LINE_60,
        "part_3_line_61": RC381_PART_3_LINE_61,
        "part_3_line_64": RC381_PART_3_LINE_64,
        "part_3_line_67": RC381_PART_3_LINE_67,
        "part_3_line_68": RC381_PART_3_LINE_68,
    }
    assert {key: worksheet.get(kind).value for key, kind in part_3_kinds.items()} == {
        key: D(value) for key, value in upstream.items()
    }
    assert part_4_employment(worksheet) == {line: D(value) for line, value in expected.items()}


@pytest.mark.parametrize(
    ("line_1", "line_2", "box_16", "box_17", "box_16a", "box_17a", "upstream", "expected"),
    PART_4_EMPLOYMENT_CASES,
)
def test_return_bo_part_4_lines_92_to_110_are_part_3b_lines_75_to_93(
    line_1: str,
    line_2: str,
    box_16: str,
    box_17: str,
    box_16a: str,
    box_17a: str,
    upstream: dict[str, str],
    expected: dict[str, str],
) -> None:
    # Part 4's lines 92 to 110 are the same procedure as Part 3b's lines 75 to 93 on the same Part 3
    # totals (line 98 is line 81 and line 110 is line 93), whatever the sign of line 69 (Part 3b is
    # computed for every return).
    worksheet = return_bo(line_1, line_2, box_16, box_17, line_25=box_16a, line_45=box_17a)

    part_3b_lines = part_3b(worksheet)
    assert part_4_employment(worksheet) == {
        line: part_3b_lines[PART_3B_OF_PART_4[line]] for line in PART_4_EMPLOYMENT_KINDS
    }


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
        RC381_PART_4_LINE_4,
        RC381_PART_4_LINE_13,
        RC381_PART_4_LINE_13_DIFFERENCE,
        RC381_PART_4_LINE_14,
        RC381_PART_4_LINE_17A,
        RC381_PART_4_LINE_20,
        RC381_PART_4_LINE_21,
        RC381_PART_4_LINE_21_LESSER,
        RC381_PART_4_LINE_23,
        RC381_PART_4_LINE_23_LESSER,
        RC381_PART_4_LINE_23_MULTIPLIED,
        RC381_PART_4_LINE_24,
        RC381_PART_4_LINE_24_LESSER,
        RC381_PART_4_LINE_25A,
        RC381_PART_4_LINE_26,
        RC381_PART_4_LINE_27,
        RC381_PART_4_LINE_31_DIFFERENCE,
        RC381_PART_4_LINE_31,
        RC381_PART_4_LINE_32,
        RC381_PART_4_LINE_33,
        RC381_PART_4_LINE_34,
        RC381_PART_4_LINE_35,
        RC381_PART_4_LINE_35AA,
        RC381_PART_4_LINE_35AB_FROM_LINE_20,
        RC381_PART_4_LINE_35AB_WHEN_LINE_35_ZERO,
        RC381_PART_4_LINE_35AB,
        RC381_PART_4_LINE_35A,
        RC381_PART_4_LINE_36,
        RC381_PART_4_LINE_38,
        RC381_PART_4_LINE_39,
        RC381_PART_4_LINE_40,
        RC381_PART_4_LINE_41,
        RC381_PART_4_LINE_42,
        RC381_PART_4_LINE_46_DIFFERENCE,
        RC381_PART_4_LINE_46,
        RC381_PART_4_LINE_47,
        RC381_PART_4_LINE_51_DIFFERENCE,
        RC381_PART_4_LINE_51,
        RC381_PART_4_LINE_52,
        RC381_PART_4_LINE_53,
        RC381_PART_4_LINE_54,
        RC381_PART_4_LINE_55,
        RC381_PART_4_LINE_56,
        RC381_PART_4_LINE_92,
        RC381_PART_4_LINE_93,
        RC381_PART_4_LINE_94,
        RC381_PART_4_LINE_95,
        RC381_PART_4_LINE_96,
        RC381_PART_4_LINE_97,
        RC381_PART_4_LINE_98,
        RC381_PART_4_LINE_99,
        RC381_PART_4_LINE_100,
        RC381_PART_4_LINE_101,
        RC381_PART_4_LINE_102,
        RC381_PART_4_LINE_103,
        RC381_PART_4_LINE_104_DIFFERENCE,
        RC381_PART_4_LINE_104,
        RC381_PART_4_LINE_105,
        RC381_PART_4_LINE_106,
        RC381_PART_4_LINE_107,
        RC381_PART_4_LINE_108,
        RC381_PART_4_LINE_109,
        RC381_PART_4_LINE_110,
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
    # Part 4: lines 8 and 11 are lines 20 and 21 (less the required 0), line 12 their sum and
    # line 17 the whole T4 box 16 total, so line 13's difference is 0 and line 21 is line 17 in
    # brackets.
    assert worksheet.get(RC381_PART_4_LINE_8).value == D("2796.75")
    assert worksheet.get(RC381_PART_4_LINE_11).value == D("565.00")
    assert worksheet.get(RC381_PART_4_LINE_12).value == D("3361.75")
    assert worksheet.get(RC381_PART_4_LINE_17).value == D("3361.75")
    assert worksheet.get(RC381_PART_4_LINE_21_FROM_LINE_17).value == D("-3361.75")
    # Part 4 line 35aa from line 17 is line 17 itself, as it is positive.
    assert worksheet.get(RC381_PART_4_LINE_35AA_FROM_LINE_17).value == D("3361.75")
    # Part 4 line 22 is 0 over 0: a zero divisor gives 0.
    assert worksheet.get(RC381_PART_4_LINE_22).value == Rate(D("0"))
    # Lines 27 to 30 are the QPP row of the table less lines 7 to 10, which are 0.
    assert worksheet.get(RC381_PART_3_LINE_27).value == D("81200.00")
    assert worksheet.get(RC381_PART_3_LINE_28).value == D("71300.00")
    assert worksheet.get(RC381_PART_3_LINE_29).value == D("3500.00")
    assert worksheet.get(RC381_PART_3_LINE_30).value == D("9900.00")
    for kind in kinds:
        assert worksheet.get(kind).value == D("0"), kind.identifier
    # Part 4 lines 57 to 91 are computed for every return: line 59 = 71,300.00 less 3,500.00 and
    # line 61 = line 59 less line 42 (0). Line 3 of Part 3 (0) is less than line 58, so line 65 =
    # line 69 = 3,500.00 (line 68 = 0 less line 59, entered as "0"), and line 70 = line 62 (the
    # lesser of line 4, 0, and line 61) less line 69 = -3,500.00 (no floor is printed): lines 80
    # and 82 follow (-3,500.00 and 0.00), line 77 = line D 9,900.00 less line 76 (0.00), and lines
    # 84 to 88 are 0; line 89 = 2 x line 69 (3,361.75) = 6,723.50, so line 90 = 0.00 less 6,723.50
    # is negative (line 42100 is 0.00) and line 91 = 6,723.50 x 50% = 3,361.75.
    assert part_4_earnings(worksheet) == {
        "59": D("67800.00"),
        "61": D("67800.00"),
        "62": D("0"),
        "65": D("3500.00"),
        "68": D("0"),
        "69": D("3500.00"),
        "70": D("-3500.00"),
        "74": D("0"),
        "76": D("0.00"),
        "77": D("9900.00"),
        "80": D("-3500.00"),
        "82": D("0.00"),
        "83_lesser": D("0.00"),
        "83": D("0"),
        "84": D("0.00"),
        "85": D("0.00"),
        "86": D("0.00"),
        "87": D("0.00"),
        "88": D("0.00"),
        "89_from_line_69": D("3361.75"),
        "89": D("6723.50"),
        "90": D("-6723.50"),
        "42100": D("0.00"),
        "91_from_line_90": D("6723.50"),
        "91": D("3361.75"),
    }


def test_the_rc381_figures_do_not_change_the_t1_lines_yet() -> None:
    # This part of Form RC381 reaches no line of the return: the same employment income and T4 box
    # 16 total (which Schedule 8 reads too) with and without the pensionable earnings totals and the
    # T4 box 17 total gives the same Schedule 8 contributions, net income and total payable.
    with_totals = return_bo()
    without_totals = return_bo(line_1="0", line_2="0", line_39="0")

    for kind in (CPP_BASE_CONTRIBUTIONS, CPP_ENHANCED_CONTRIBUTIONS, NET_INCOME, TOTAL_PAYABLE):
        assert with_totals.get(kind).value == without_totals.get(kind).value, kind.identifier
