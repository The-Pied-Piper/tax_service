"""CA-ON 2025 end to end: return al."""

from __future__ import annotations

from typing import Any

from app.adapters.inbound.trace_english import EnglishTraceRenderer
from app.domain.parameters.rate import Rate
from app.domain.trace import (
    GreaterOfLine,
    RateAppliedLine,
    SubtractedLine,
    SubtractedNotBelowZeroLine,
    SumLine,
    SumNotBelowZeroLine,
)
from app.domain.worksheet import Worksheet
from app.jurisdictions.ca.catalog import (
    ADJUSTED_FAMILY_NET_INCOME,
    AGE_AMOUNT,
    AGE_AMOUNT_BEFORE_COUNT,
    AGE_INCOME_OVER_THRESHOLD,
    BASIC_PERSONAL_AMOUNT,
    CREDITS_AGAINST_BASIC_FEDERAL_TAX,
    DEDUCTIONS_FROM_TOTAL_INCOME,
    FEDERAL_BASIC_TAX,
    FEDERAL_TAX_AFTER_CREDITS,
    FEDERAL_TAX_ON_SPLIT_INCOME,
    FEDERAL_TAX_WITH_SPLIT_INCOME,
    MEDICAL_SUPPLEMENT_COLUMN_1_LINE_3,
    MEDICAL_SUPPLEMENT_COLUMN_1_LINE_5,
    MEDICAL_SUPPLEMENT_LINE_6,
    NET_FEDERAL_TAX,
    NET_INCOME,
    NET_INCOME_BEFORE_ADJUSTMENTS,
    REFUND_OR_BALANCE_OWING,
    SPECIAL_TAXES,
    SPLIT_INCOME_DIVIDENDS_OTHER_THAN_ELIGIBLE,
    SPLIT_INCOME_LINE_10,
    SPLIT_INCOME_LINE_13,
    SPLIT_INCOME_LINE_14,
    SPLIT_INCOME_LINE_15,
    SPLIT_INCOME_LINE_18,
    SPLIT_INCOME_LINE_19,
    SPLIT_INCOME_LINE_20,
    SPLIT_INCOME_LINE_21,
    SPLIT_INCOME_LINE_22,
    SPLIT_INCOME_LINE_24,
    SPLIT_INCOME_LINE_29,
    SPLIT_INCOME_LINE_30,
    TOSI_ADJUSTED_NET_INCOME,
    TOSI_ADJUSTED_NET_INCOME_NOT_BELOW_ZERO,
    TOTAL_INCOME,
    TOTAL_PAYABLE,
    TOTAL_SPLIT_INCOME,
)
from tests.jurisdictions.ca_on.end_to_end.support import CENT, D, compute, return_a


def return_al(**overrides: Any) -> Worksheet:
    """Return AL's inputs, as in `returns/2025_return_al.yaml`, over the keyword overrides given.

    A single filer, aged 20, whose only income is 10000 of dividends other than eligible dividends
    from a private corporation controlled by a relative, received with no slip: 11500.00 grossed
    up, all of it split income, so Form T1206's lines 1, 2 and 4 are 11500 and line 3 is 0. The
    tax on split income (line 8, T1 line 40424) is 3795.00.
    """
    inputs: dict[str, Any] = {
        "other_dividends_received_without_a_slip": "10000",
        "split_income_dividends": "11500",
        "split_income_dividends_other_than_eligible": "11500",
    }
    inputs.update(overrides)
    return compute("0", "0", "0", "0", "0", "0", "0", **inputs)


def test_return_al_pays_the_tax_on_split_income_of_3795_on_line_40424() -> None:
    worksheet = return_al()

    # Form T1206 Part 1: line 4 is line 1 plus line 3, all of it a deduction of line 23300 (so the
    # net income is 0.00), and line 6 adds line 5 back: 11500 + 0.00.
    assert worksheet.get(TOTAL_INCOME).value == D("11500.00")
    assert worksheet.get(TOTAL_SPLIT_INCOME).value == D("11500")
    assert worksheet.get(DEDUCTIONS_FROM_TOTAL_INCOME).value == D("11500.00")
    assert worksheet.get(NET_INCOME_BEFORE_ADJUSTMENTS).value == D("0.00")
    assert worksheet.get(NET_INCOME).value == D("0.00")
    assert worksheet.get(TOSI_ADJUSTED_NET_INCOME).value == D("11500.00")
    assert worksheet.get(TOSI_ADJUSTED_NET_INCOME_NOT_BELOW_ZERO).value == D("11500.00")
    # Line 8, 11500 x 33% = 3795.00, enters T1 line 121 with the basic tax of 0.00.
    assert worksheet.get(FEDERAL_TAX_ON_SPLIT_INCOME).value == D("3795.00")
    assert worksheet.get(FEDERAL_BASIC_TAX).value == D("0.00")
    assert worksheet.get(FEDERAL_TAX_WITH_SPLIT_INCOME).value == D("3795.00")
    # Part 2 lines 9 to 15: no advanced Canada workers benefit and no disability amounts.
    assert worksheet.get(SPLIT_INCOME_LINE_10).value == D("3795.00")
    assert worksheet.get(SPLIT_INCOME_LINE_13).value == D("0")
    assert worksheet.get(SPLIT_INCOME_LINE_14).value == D("0.00")
    assert worksheet.get(SPLIT_INCOME_LINE_15).value == D("3795.00")
    # Lines 16 to 22: line 18 is 11500 less 11500, 0; line 19 is 11500 x 9.0301% = 1038.4615,
    # rounded half-up to the cent, 1038.46; line 22 is 3795.00 - 1038.46 = 2756.54.
    assert worksheet.get(SPLIT_INCOME_LINE_18).value == D("0")
    assert worksheet.get(SPLIT_INCOME_LINE_19).value == D("1038.46")
    assert worksheet.get(SPLIT_INCOME_LINE_20).value == D("0.00")
    assert worksheet.get(SPLIT_INCOME_LINE_21).value == D("1038.46")
    assert worksheet.get(SPLIT_INCOME_LINE_22).value == D("2756.54")
    assert worksheet.get(SPLIT_INCOME_LINE_24).value == D("2756.54")
    # Line 29 is the T1's federal tax less credits, 3795.00 - (2338.71 + 1038.46) = 417.83, and
    # line 30 is the more of lines 24 and 29, which is line 24 here.
    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("417.83")
    assert worksheet.get(SPLIT_INCOME_LINE_29).value == D("417.83")
    assert worksheet.get(SPLIT_INCOME_LINE_30).value == D("2756.54")
    assert worksheet.get(NET_FEDERAL_TAX).value == D("2756.54")
    assert worksheet.get(TOTAL_PAYABLE).value == D("2756.54")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("2756.54")


def test_return_als_trace_follows_form_t1206_line_by_line() -> None:
    worksheet = return_al()
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)

    for line in (
        "total_split_income: split_income_dividends 11500 + other_split_income 0 = 11500",
        "tosi_adjusted_net_income: total_split_income 11500 + net_income_before_adjustments 0 "
        "= 11500",
        "tosi_adjusted_net_income_not_below_zero: total_split_income 11500 "
        "+ net_income_before_adjustments 0, not below 0 = 11500",
        "federal_tax_on_split_income: 33% of total_split_income 11500 (half-up to 0.01)",
        "federal_tax_with_split_income: federal_basic_tax 0 + federal_tax_on_split_income 3795 "
        "= 3795",
        "split_income_line_10: federal_tax_on_split_income 3795 "
        "+ advanced_canada_workers_benefit 0 = 3795",
        "split_income_line_13: disability_amount_for_self 0 + disability_transferred_amount 0 = 0",
        "split_income_line_14: 14.5% of split_income_line_13 0 (half-up to 0.01)",
        "split_income_line_15: split_income_line_10 3795 less split_income_line_14 0 = 3795",
        "split_income_line_18: split_income_dividends 11500 "
        "less split_income_dividends_other_than_eligible 11500, not below 0 = 0",
        "split_income_line_19: 9.0301% of split_income_dividends_other_than_eligible 11500 "
        "(half-up to 0.01)",
        "split_income_line_20: 15.0198% of split_income_line_18 0 (half-up to 0.01)",
        "split_income_line_21: split_income_line_19 1038.46 + split_income_line_20 0 = 1038.46",
        "split_income_line_22: split_income_line_15 3795 less split_income_line_21 1038.46 "
        "= 2756.54",
        "split_income_line_24: split_income_line_22 2756.54, not below 0 = 2756.54",
        "split_income_line_29: federal_tax_less_credits 417.83 "
        "+ advanced_canada_workers_benefit 0 = 417.83",
        "split_income_line_30: greater of split_income_line_24 2756.54 "
        "and split_income_line_29 417.83 = 2756.54",
        "net_federal_tax: split_income_line_30 2756.54 + special_taxes 0 = 2756.54",
        "federal_tax_after_credits: federal_tax_with_split_income 3795 "
        "less credits_against_basic_federal_tax 3377.17, not below 0 = 417.83",
        "basic_personal_amount: 14538 plus 1591 less 0 for "
        "tosi_adjusted_net_income_not_below_zero 11500 over 177882 (range 75532), "
        "not below 14538 (half-up to 0.01)",
        "adjusted_family_net_income: tosi_adjusted_net_income_not_below_zero 11500 = 11500",
    ):
        assert line in rendered, line


def test_return_als_trace_records_the_split_income_lines_as_structured_lines() -> None:
    trace = return_al().trace

    assert (
        RateAppliedLine(
            FEDERAL_TAX_ON_SPLIT_INCOME,
            TOTAL_SPLIT_INCOME,
            D("11500"),
            Rate(D("0.33")),
            CENT,
            D("3795.00"),
        )
        in trace
    )
    assert (
        RateAppliedLine(
            SPLIT_INCOME_LINE_19,
            SPLIT_INCOME_DIVIDENDS_OTHER_THAN_ELIGIBLE,
            D("11500"),
            Rate(D("0.090301")),
            CENT,
            D("1038.46"),
        )
        in trace
    )
    assert (
        SubtractedLine(
            output=SPLIT_INCOME_LINE_22,
            minuend=SPLIT_INCOME_LINE_15,
            minuend_amount=D("3795.00"),
            subtrahend=SPLIT_INCOME_LINE_21,
            subtrahend_amount=D("1038.46"),
            result=D("2756.54"),
        )
        in trace
    )
    assert (
        SumNotBelowZeroLine(
            output=SPLIT_INCOME_LINE_24,
            parts=((SPLIT_INCOME_LINE_22, D("2756.54")),),
            total=D("2756.54"),
        )
        in trace
    )
    assert (
        GreaterOfLine(
            output=SPLIT_INCOME_LINE_30,
            parts=((SPLIT_INCOME_LINE_24, D("2756.54")), (SPLIT_INCOME_LINE_29, D("417.83"))),
            result=D("2756.54"),
        )
        in trace
    )
    assert (
        SumNotBelowZeroLine(
            output=TOSI_ADJUSTED_NET_INCOME_NOT_BELOW_ZERO,
            parts=((TOTAL_SPLIT_INCOME, D("11500")), (NET_INCOME_BEFORE_ADJUSTMENTS, D("0.00"))),
            total=D("11500.00"),
        )
        in trace
    )
    assert (
        SubtractedNotBelowZeroLine(
            output=FEDERAL_TAX_AFTER_CREDITS,
            minuend=FEDERAL_TAX_WITH_SPLIT_INCOME,
            minuend_amount=D("3795.00"),
            subtrahend=CREDITS_AGAINST_BASIC_FEDERAL_TAX,
            subtrahend_amount=D("3377.17"),
            result=D("417.83"),
        )
        in trace
    )


def return_b_with_split_income_dividends(**overrides: Any) -> Worksheet:
    """Return B's filer (employment income of 30000, tax deducted 3000) with split income.

    Dividends of 1000 with no slip, all split income: grossed up by 115% to 1150, the Form T1206
    lines 1, 2 and 4 being 1150. The disability amount of line 31600, a chosen 10138 (the figure
    asked for line 31600 for 2025), is larger than the tax on split income of 379.50.
    """
    inputs: dict[str, Any] = {
        "income_tax_deducted": "3000",
        "other_dividends_received_without_a_slip": "1000",
        "split_income_dividends": "1150",
        "split_income_dividends_other_than_eligible": "1150",
        "disability_amount_for_self": "10138",
    }
    inputs.update(overrides)
    return compute("30000", "0", "0", "0", "5400", "0", "0", **inputs)


def test_a_disability_amount_larger_than_the_tax_leaves_line_22_negative_and_line_24_at_zero() -> (
    None
):
    worksheet = return_b_with_split_income_dividends()

    # Line 8 is 1150 x 33% = 379.50 and line 10 the same (no advanced Canada workers benefit).
    assert worksheet.get(TOTAL_SPLIT_INCOME).value == D("1150")
    assert worksheet.get(FEDERAL_TAX_ON_SPLIT_INCOME).value == D("379.50")
    assert worksheet.get(SPLIT_INCOME_LINE_10).value == D("379.50")
    # Line 13 is 10138 + 0 and line 14 is 14.5% of it, 1470.01 (exactly); line 15, which prints no
    # floor, is 379.50 - 1470.01 = -1090.51.
    assert worksheet.get(SPLIT_INCOME_LINE_13).value == D("10138")
    assert worksheet.get(SPLIT_INCOME_LINE_14).value == D("1470.01")
    assert worksheet.get(SPLIT_INCOME_LINE_15).value == D("-1090.51")
    # Line 19 is 1150 x 9.0301% = 103.84615, rounded half-up to the cent, 103.85; line 18 is 0.
    assert worksheet.get(SPLIT_INCOME_LINE_19).value == D("103.85")
    assert worksheet.get(SPLIT_INCOME_LINE_21).value == D("103.85")
    # Line 22 is -1090.51 - 103.85 = -1194.36, and line 24 takes 0 for a negative line 22.
    assert worksheet.get(SPLIT_INCOME_LINE_22).value == D("-1194.36")
    assert worksheet.get(SPLIT_INCOME_LINE_24).value == D("0")
    # Line 29: the T1 tax of line 121, 4311.58 + 379.50 = 4691.08, less the credits of
    # 2813.54 + 103.85 = 2917.39 (the federal dividend tax credit, line 40425, counts the same
    # 1150), is 1773.69; the more of 0 and 1773.69 is line 29, which is not floored at line 24.
    assert worksheet.get(FEDERAL_BASIC_TAX).value == D("4311.58")
    assert worksheet.get(FEDERAL_TAX_WITH_SPLIT_INCOME).value == D("4691.08")
    assert worksheet.get(CREDITS_AGAINST_BASIC_FEDERAL_TAX).value == D("2917.39")
    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("1773.69")
    assert worksheet.get(SPLIT_INCOME_LINE_29).value == D("1773.69")
    assert worksheet.get(SPLIT_INCOME_LINE_30).value == D("1773.69")
    assert worksheet.get(NET_FEDERAL_TAX).value == D("1773.69")


def test_a_negative_line_22_is_recorded_signed_and_floored_by_line_24_alone() -> None:
    trace = return_b_with_split_income_dividends().trace

    assert (
        SubtractedLine(
            output=SPLIT_INCOME_LINE_22,
            minuend=SPLIT_INCOME_LINE_15,
            minuend_amount=D("-1090.51"),
            subtrahend=SPLIT_INCOME_LINE_21,
            subtrahend_amount=D("103.85"),
            result=D("-1194.36"),
        )
        in trace
    )
    assert (
        SumNotBelowZeroLine(
            output=SPLIT_INCOME_LINE_24,
            parts=((SPLIT_INCOME_LINE_22, D("-1194.36")),),
            total=D("0"),
        )
        in trace
    )
    assert (
        GreaterOfLine(
            output=SPLIT_INCOME_LINE_30,
            parts=((SPLIT_INCOME_LINE_24, D("0")), (SPLIT_INCOME_LINE_29, D("1773.69"))),
            result=D("1773.69"),
        )
        in trace
    )
    rendered = EnglishTraceRenderer().render_all(trace)
    assert (
        "split_income_line_22: split_income_line_15 -1090.51 less split_income_line_21 103.85 "
        "= -1194.36"
    ) in rendered
    assert "split_income_line_24: split_income_line_22 -1194.36, not below 0 = 0" in rendered


def test_a_negative_tosi_adjusted_net_income_is_zero_in_the_twin_and_negative_on_line_45200() -> (
    None
):
    # 1150 of split income (1000 of dividends grossed up) is the only income; the other deductions
    # of 5000 (line 23200) are larger than it: line 23300 is 5000 + 1150 = 6150, line 23400 is
    # 1150 - 6150 = -5000.00 and the net income (line 23600) is 0. Form T1206 line 6 is
    # 1150 + (-5000.00) = -3850.00.
    worksheet = compute(
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        other_dividends_received_without_a_slip="1000",
        split_income_dividends="1150",
        split_income_dividends_other_than_eligible="1150",
        other_deductions="5000",
    )

    assert worksheet.get(DEDUCTIONS_FROM_TOTAL_INCOME).value == D("6150")
    assert worksheet.get(NET_INCOME_BEFORE_ADJUSTMENTS).value == D("-5000.00")
    assert worksheet.get(NET_INCOME).value == D("0")
    assert worksheet.get(TOSI_ADJUSTED_NET_INCOME).value == D("-3850.00")
    # "(If the TOSI-adjusted net income at line 6 is negative, use the negative value when it is
    # part of an adjusted net income calculation, otherwise use zero.)"
    assert worksheet.get(TOSI_ADJUSTED_NET_INCOME_NOT_BELOW_ZERO).value == D("0")
    assert worksheet.get(BASIC_PERSONAL_AMOUNT).value == D("16129.00")
    assert worksheet.get(ADJUSTED_FAMILY_NET_INCOME).value == D("0")
    # Line 45200 column 1: line 3 reads the signed line 6, line 5 takes 0 for a negative line 3.
    assert worksheet.get(MEDICAL_SUPPLEMENT_COLUMN_1_LINE_3).value == D("-3850.00")
    assert worksheet.get(MEDICAL_SUPPLEMENT_COLUMN_1_LINE_5).value == D("0")
    assert worksheet.get(MEDICAL_SUPPLEMENT_LINE_6).value == D("0")
    trace = worksheet.trace
    assert (
        SumLine(
            output=TOSI_ADJUSTED_NET_INCOME,
            parts=((TOTAL_SPLIT_INCOME, D("1150")), (NET_INCOME_BEFORE_ADJUSTMENTS, D("-5000.00"))),
            total=D("-3850.00"),
        )
        in trace
    )
    assert (
        SumNotBelowZeroLine(
            output=TOSI_ADJUSTED_NET_INCOME_NOT_BELOW_ZERO,
            parts=((TOTAL_SPLIT_INCOME, D("1150")), (NET_INCOME_BEFORE_ADJUSTMENTS, D("-5000.00"))),
            total=D("0"),
        )
        in trace
    )


def test_line_23200_other_deductions_and_the_total_split_income_are_both_in_line_23300() -> None:
    # Other deductions of 300 and the split income of 11500: line 23300 is 11800 (line 23200 and
    # Form T1206 line 4), line 23400 is 11500.00 - 11800 = -300.00, and line 6 is
    # 11500 + (-300.00) = 11200.00.
    worksheet = return_al(other_deductions="300")

    assert worksheet.get(DEDUCTIONS_FROM_TOTAL_INCOME).value == D("11800")
    assert worksheet.get(NET_INCOME_BEFORE_ADJUSTMENTS).value == D("-300.00")
    assert worksheet.get(NET_INCOME).value == D("0")
    assert worksheet.get(TOSI_ADJUSTED_NET_INCOME).value == D("11200.00")
    assert worksheet.get(TOSI_ADJUSTED_NET_INCOME_NOT_BELOW_ZERO).value == D("11200.00")
    assert worksheet.get(ADJUSTED_FAMILY_NET_INCOME).value == D("11200.00")


def test_split_income_over_the_threshold_tapers_the_basic_amount_and_ends_the_age_amount() -> None:
    # Other income of 200000, all of it split income (a chosen figure): line 23300 is 200000, the
    # net income is 0.00, and the TOSI-adjusted net income is 200000.00. The basic personal amount
    # is 14538 + 1591 less 1591 x (200000 - 177882) / 75532 = 465.89..., 15663.11 rounded half-up
    # to the cent, where the net income of 0.00 would give the full 16129.00. A filer born in 1960
    # or earlier: line 4 of the Federal Worksheet is 200000.00 - 45522.00 = 154478.00, the age
    # reduction 15% of it, 23171.70, is more than the 9028.00, so the age amount is 0.
    worksheet = return_al(
        other_dividends_received_without_a_slip="0",
        other_income="200000",
        split_income_dividends="0",
        split_income_dividends_other_than_eligible="0",
        other_split_income="200000",
        born_in_1960_or_earlier=1,
    )

    assert worksheet.get(NET_INCOME).value == D("0.00")
    assert worksheet.get(TOSI_ADJUSTED_NET_INCOME_NOT_BELOW_ZERO).value == D("200000.00")
    assert worksheet.get(BASIC_PERSONAL_AMOUNT).value == D("15663.11")
    assert worksheet.get(AGE_INCOME_OVER_THRESHOLD).value == D("154478.00")
    assert worksheet.get(AGE_AMOUNT_BEFORE_COUNT).value == D("0")
    assert worksheet.get(AGE_AMOUNT).value == D("0")
    assert worksheet.get(ADJUSTED_FAMILY_NET_INCOME).value == D("200000.00")
    # Line 4 is all the split income: line 8 is 200000 x 33% = 66000.00 and line 24 the same, as
    # nothing is claimed against it (lines 13 and 19 are 0).
    assert worksheet.get(TOTAL_SPLIT_INCOME).value == D("200000")
    assert worksheet.get(FEDERAL_TAX_ON_SPLIT_INCOME).value == D("66000.00")
    assert worksheet.get(SPLIT_INCOME_LINE_22).value == D("66000.00")
    assert worksheet.get(SPLIT_INCOME_LINE_24).value == D("66000.00")


def test_the_advanced_canada_workers_benefit_joins_lines_10_and_29() -> None:
    # Return AL with 200 on line 41500: line 10 is 3795.00 + 200 = 3995.00, line 22 is
    # 3995.00 - 1038.46 = 2956.54 and line 29 is 417.83 + 200 = 617.83, so line 30 is 2956.54.
    worksheet = return_al(advanced_canada_workers_benefit="200")

    assert worksheet.get(SPLIT_INCOME_LINE_10).value == D("3995.00")
    assert worksheet.get(SPLIT_INCOME_LINE_15).value == D("3995.00")
    assert worksheet.get(SPLIT_INCOME_LINE_22).value == D("2956.54")
    assert worksheet.get(SPLIT_INCOME_LINE_29).value == D("617.83")
    assert worksheet.get(SPLIT_INCOME_LINE_30).value == D("2956.54")
    assert worksheet.get(NET_FEDERAL_TAX).value == D("2956.54")


def test_the_special_taxes_of_line_41800_are_added_to_line_30_of_form_t1206() -> None:
    # Return AL with 7 from the RL-10 slip on line 41800: 2756.54 + 7 = 2763.54.
    worksheet = return_al(rl_10_labour_sponsored_fund_amount="7")

    assert worksheet.get(SPECIAL_TAXES).value == D("7")
    assert worksheet.get(SPLIT_INCOME_LINE_30).value == D("2756.54")
    assert worksheet.get(NET_FEDERAL_TAX).value == D("2763.54")
    assert worksheet.get(TOTAL_PAYABLE).value == D("2763.54")


def test_without_split_income_the_net_federal_tax_is_line_29_and_line_24_is_zero() -> None:
    worksheet = return_a()

    assert worksheet.get(TOTAL_SPLIT_INCOME).value == D("0")
    assert worksheet.get(FEDERAL_TAX_ON_SPLIT_INCOME).value == D("0.00")
    assert worksheet.get(TOSI_ADJUSTED_NET_INCOME).value == worksheet.get(NET_INCOME).value
    assert (
        worksheet.get(FEDERAL_TAX_WITH_SPLIT_INCOME).value == worksheet.get(FEDERAL_BASIC_TAX).value
    )
    assert worksheet.get(SPLIT_INCOME_LINE_24).value == D("0")
    assert worksheet.get(SPLIT_INCOME_LINE_29).value == D("16951.38")
    assert worksheet.get(SPLIT_INCOME_LINE_30).value == D("16951.38")
    assert worksheet.get(NET_FEDERAL_TAX).value == D("16951.38")
