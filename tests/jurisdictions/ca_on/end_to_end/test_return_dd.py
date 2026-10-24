"""CA-ON 2025 end to end: return dd."""

from __future__ import annotations

from typing import Any

from app.domain.worksheet import Worksheet
from app.jurisdictions.ca.catalog import (
    EI_OVERPAYMENT,
    EI_PAYABLE_ON_SELF_EMPLOYMENT,
    EI_PREMIUMS,
    REFUND_OR_BALANCE_OWING,
    T2204_EXEMPTION,
    T2204_LINE_1,
    T2204_LINE_3,
    T2204_LINE_6,
    T2204_LINE_7,
    T2204_LINE_8,
    T2204_LINE_9,
    T2204_LINE_10,
    T2204_LINE_12,
    T2204_LINE_13,
    T2204_LINE_14,
    T2204_LINE_15,
    T2204_LINE_16,
    T2204_SELF_EMPLOYMENT_EARNINGS,
    TOTAL_CREDITS,
)
from tests.jurisdictions.ca_on.end_to_end.support import D, compute

# Return DD's inputs beyond the all-zero ones `starting` defaults to, as in
# `returns/2025_return_dd.yaml`: the employment income (T4 box 14) and the T4 box 24 insurable
# earnings are the same figure, and the income tax deducted (T4 box 22) is a chosen 11000.
RETURN_DD: dict[str, Any] = {"income_tax_deducted": "11000"}


def dd(insurable: str, premiums: str, self_employment: str = "0", **changes: Any) -> Worksheet:
    """Return DD's worksheet of `ca-on/return`: T4 box 24 `insurable` (with box 14 and the
    Schedule 13 insurable earnings the same), T4 box 18 `premiums` (Form T2204 line 4),
    `self_employment` (Form T2204 line 2) and `changes` to the inputs of the return."""
    inputs = {
        "ei_insurable_earnings": insurable,
        "t2204_insurable_earnings": insurable,
        "t2204_self_employment_earnings": self_employment,
        "t2204_premiums_deducted": premiums,
        **RETURN_DD,
        **changes,
    }
    return compute(insurable, (), "0", "0", "0", "0", "0", **inputs)


def return_dd() -> Worksheet:
    """Return DD, as in `returns/2025_return_dd.yaml`: the worked example, insurable earnings of
    70000 and premiums of 1200.00, no self-employment earnings and no agreement."""
    return dd("70000", "1200.00")


def test_the_worked_example_gives_line_45000_of_122_52_and_line_16_of_1077_48() -> None:
    worksheet = return_dd()

    # Line 3 is 70000, capped at 65700; line 7 is 65700 - 2000 = 63700, so line 8 is
    # max(1200 - 63700, 0) = 0. Line 10 is 70000 x 1.64% = 1148.00, the maximum 1077.48 (line 1, not
    # line 3, is the base). Line 13 is 1200.00 - 1077.48 = 122.52, line 14 is 122.52 and line 15 is
    # the lesser of 1200.00 and 122.52, 122.52, which is more than $1, so line 45000 is 122.52.
    # Line 16 is the least of 63700, 1200.00 and 1077.48, 1077.48.
    assert worksheet.get(T2204_LINE_1).value == D("70000")
    assert worksheet.get(T2204_LINE_3).value == D("65700")
    assert worksheet.get(T2204_LINE_7).value == D("63700")
    assert worksheet.get(T2204_LINE_8).value == D("0")
    assert worksheet.get(T2204_LINE_9).value == D("1200.00")
    assert worksheet.get(T2204_LINE_10).value == D("1077.48")
    assert worksheet.get(T2204_LINE_12).value == D("1077.48")
    assert worksheet.get(T2204_LINE_13).value == D("122.52")
    assert worksheet.get(T2204_LINE_14).value == D("122.52")
    assert worksheet.get(T2204_LINE_15).value == D("122.52")
    assert worksheet.get(EI_OVERPAYMENT).value == D("122.52")
    assert worksheet.get(T2204_LINE_16).value == D("1077.48")


def test_line_16_is_the_employment_insurance_premium_on_line_31200_of_the_worked_return() -> None:
    worksheet = return_dd()

    # Both are 1.64% of the employment income up to the $65,700 maximum, 1077.48. Nothing reads
    # line 16; the comparison is the check that the two lines agree on this return.
    assert worksheet.get(EI_PREMIUMS).value == D("1077.48")
    assert worksheet.get(T2204_LINE_16).value == worksheet.get(EI_PREMIUMS).value


def test_line_45000_flows_into_total_credits_and_the_refund_of_the_worked_return() -> None:
    worksheet = return_dd()

    # Total credits (line 48200) are the income tax deducted, 11000.00, and line 45000, 122.52:
    # 11122.52. The total payable is 11497.09 (the federal tax after credits 7585.64 and the
    # Ontario tax 3911.45), so the refund or balance owing (line 167) is 11497.09 - 11122.52 =
    # 374.57, a balance owing.
    assert worksheet.get(TOTAL_CREDITS).value == D("11122.52")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("374.57")


def test_note_1_zeroes_line_1_under_2000_so_line_45000_is_all_the_premiums() -> None:
    worksheet = dd("1800", "29.52")

    # Note (1) applies: line 1 is "0", so line 3 and line 7 are 0 and line 8 is 29.52. Line 10 is
    # 0, line 13 is 29.52 - 0 = 29.52, and line 15 is 29.52, more than $1, so line 45000 is 29.52.
    # Line 16 is the least of 0, 29.52 and 0, which is 0.
    assert worksheet.get(T2204_LINE_1).value == D("0")
    assert worksheet.get(T2204_LINE_3).value == D("0")
    assert worksheet.get(T2204_LINE_7).value == D("0")
    assert worksheet.get(T2204_LINE_8).value == D("29.52")
    assert worksheet.get(T2204_LINE_10).value == D("0")
    assert worksheet.get(T2204_LINE_13).value == D("29.52")
    assert worksheet.get(EI_OVERPAYMENT).value == D("29.52")
    assert worksheet.get(T2204_LINE_16).value == D("0")


def test_40000_insurable_with_800_of_premiums_gives_line_13_of_144_and_line_16_of_656() -> None:
    worksheet = dd("40000", "800.00")

    # Line 10 is 40000 x 1.64% = 656.00 (under the maximum), so line 13 is 800.00 - 656.00 =
    # 144.00, line 14 and line 15 are 144.00 and line 45000 is 144.00. Line 16 is the least of
    # 38000.00, 800.00 and 656.00, which is 656.00, the same as line 31200.
    assert worksheet.get(T2204_LINE_10).value == D("656.00")
    assert worksheet.get(T2204_LINE_13).value == D("144.00")
    assert worksheet.get(T2204_LINE_15).value == D("144.00")
    assert worksheet.get(EI_OVERPAYMENT).value == D("144.00")
    assert worksheet.get(T2204_LINE_16).value == D("656.00")
    assert worksheet.get(EI_PREMIUMS).value == D("656.00")


def test_an_overpayment_of_exactly_1_00_gives_0_on_line_45000() -> None:
    worksheet = dd("40000", "657.00")

    # Line 13 is 657.00 - 656.00 = 1.00. Line 15 is 1.00, which is not more than $1, so the
    # overpayment on line 45000 is 0.
    assert worksheet.get(T2204_LINE_13).value == D("1.00")
    assert worksheet.get(T2204_LINE_15).value == D("1.00")
    assert worksheet.get(EI_OVERPAYMENT).value == D("0")


def test_an_overpayment_of_1_01_gives_1_01_on_line_45000() -> None:
    worksheet = dd("40000", "657.01")

    # Line 13 is 657.01 - 656.00 = 1.01, which is more than $1, so line 45000 is 1.01.
    assert worksheet.get(T2204_LINE_13).value == D("1.01")
    assert worksheet.get(EI_OVERPAYMENT).value == D("1.01")


def test_self_employment_with_an_agreement_puts_schedule_13_into_lines_5_and_6() -> None:
    # Self-employment earnings of 50000 eligible under the agreement (line 2, the input), with
    # Schedule 13 line 9 for one agreement. Schedule 13 takes the T4 box 24 insurable earnings of
    # 40000 from the maximum of 65700, leaving 25700, and 1.64% of 25700 = 421.48 (line 5, the
    # existing `ca/ei_payable_on_self_employment`). Line 3 is 40000 + 50000, capped at 65700, so
    # line 7 is 63700. Line 6 is 800.00 + 421.48 = 1221.48, and line 8 is max(1221.48 - 63700,
    # 0) = 0, so the agreement does not move line 45000, which is still 144.00.
    worksheet = dd(
        "40000",
        "800.00",
        self_employment="50000",
        business_statements=({"business": {"gross_sales": "50000"}},),
        ei_special_benefits_agreement=1,
    )

    assert worksheet.get(T2204_SELF_EMPLOYMENT_EARNINGS).value == D("50000")
    assert worksheet.get(T2204_LINE_3).value == D("65700")
    assert worksheet.get(T2204_LINE_7).value == D("63700")
    assert worksheet.get(EI_PAYABLE_ON_SELF_EMPLOYMENT).value == D("421.48")
    assert worksheet.get(T2204_LINE_6).value == D("1221.48")
    assert worksheet.get(T2204_LINE_8).value == D("0")
    assert worksheet.get(EI_OVERPAYMENT).value == D("144.00")
    assert worksheet.get(T2204_LINE_16).value == D("656.00")


def test_the_exemption_is_claimed_whole_on_line_7() -> None:
    worksheet = return_dd()

    # Line 7 "Amount from line 3 – $2,000": the $2,000 is the exemption, claimed whole.
    assert worksheet.get(T2204_EXEMPTION).value == D("2000.00")
