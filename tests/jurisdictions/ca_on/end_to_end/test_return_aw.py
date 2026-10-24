"""CA-ON 2025 end to end: return aw."""

from __future__ import annotations

from decimal import Decimal
from typing import Any

from app.adapters.inbound.trace_english import EnglishTraceRenderer
from app.domain.capabilities.lesser_of import LesserOf
from app.domain.capabilities.multiple_over import MultipleOver
from app.domain.capabilities.subtract_not_below_zero import SubtractNotBelowZero
from app.domain.capabilities.sum import Sum
from app.domain.capabilities.times_count import TimesCount
from app.domain.record_list import RecordList
from app.domain.trace import ItemsTotalLine, SubtractedLine, SumLine
from app.domain.worksheet import Worksheet
from app.jurisdictions.ca.capabilities.count_by_conditions import CountByConditions
from app.jurisdictions.ca.catalog import (
    AMT_ALTERNATIVE_MINIMUM_TAX_PAYABLE,
    BASIC_FEDERAL_TAX_WITH_DIVIDEND_CREDIT,
    DIVIDEND_TAX_CREDIT,
    FEDERAL_BUSINESS_FOREIGN_TAX_CREDIT,
    FEDERAL_FOREIGN_TAX_CREDIT,
    FEDERAL_FOREIGN_TAX_CREDIT_BEFORE_LIMIT,
    FEDERAL_NON_BUSINESS_FOREIGN_TAX_CREDIT,
    FEDERAL_TAX_AFTER_CREDITS,
    FEDERAL_TAX_LESS_CREDITS,
    FEDERAL_TAX_LESS_FOREIGN_TAX_CREDIT,
    FEDERAL_TAX_WITH_ITC_RECAPTURE,
    FOREIGN_BUSINESS_TAX_CREDIT_LINE_4,
    FOREIGN_BUSINESS_TAX_CREDIT_LINE_5,
    FOREIGN_BUSINESS_TAX_CREDIT_LINE_7,
    FOREIGN_BUSINESS_TAX_CREDIT_LINE_8,
    FOREIGN_BUSINESS_TAX_CREDIT_LINE_10,
    FOREIGN_NON_BUSINESS_TAX_PAID,
    FOREIGN_TAX_CREDIT_BASIC_FEDERAL_TAX,
    FOREIGN_TAX_CREDIT_NET_INCOME,
    FOREIGN_TAX_CREDIT_NET_INCOME_BEFORE_SPLIT_INCOME,
    FOREIGN_TAX_CREDIT_NET_INCOME_DEDUCTIONS,
    FOREIGN_TAX_CREDIT_NET_INCOME_WITH_SPLIT_INCOME,
    FOREIGN_TAX_CREDIT_SHEET_LINE_3,
    FOREIGN_TAX_CREDIT_SHEETS,
    NET_FEDERAL_TAX,
    NET_FOREIGN_NON_BUSINESS_INCOME,
    NET_INCOME,
    NET_INCOME_BEFORE_ADJUSTMENTS,
    REFUND,
    REFUND_OR_BALANCE_OWING,
    SOCIAL_BENEFITS_REPAYMENT,
    TAXABLE_INCOME,
    TOSI_ADJUSTED_NET_INCOME,
    TOTAL_INCOME,
    TOTAL_PAYABLE,
    TOTAL_SPLIT_INCOME,
)
from app.jurisdictions.ca.trace import (
    ForeignBusinessLine4,
    ForeignBusinessLine5,
    ForeignBusinessLine7,
    ForeignBusinessLine8,
    ForeignBusinessLine10,
    ForeignBusinessLine11,
    ForeignTaxCreditLine,
    PooledForeignTaxCreditLine,
)
from app.jurisdictions.ca_on import catalog as ontario
from app.jurisdictions.ca_on.capabilities.provincial_foreign_tax_credit import (
    ProvincialForeignTaxCredit,
)
from app.jurisdictions.ca_on.trace import ProvincialForeignTaxCreditLine
from tests.jurisdictions.ca_on.end_to_end.support import (
    CENT,
    D,
    compute,
    return_be,
    return_bf,
    return_k,
)

US = ("1500", "10000")
UK = ("100", "5000")
# The same countries with their business figures, in the order of the form: business income tax
# paid for the year (note 5), unused business foreign tax credits (note 6), net foreign business
# income (line 43900) and the federal surtax on income allocated outside Canada (line 6).
US_WITH_BUSINESS = (*US, "400", "50", "6000", "0")
UK_WITH_BUSINESS = (*UK, "60", "0", "3000", "0")


def return_aw(**overrides: Any) -> Worksheet:
    """Return AW's inputs, as in `returns/2025_return_aw.yaml`.

    The filer is Return K's: employment income of 50000, a T5 slip and dividends with no slip, and
    income tax deducted of 9000. Added are foreign investment income of 15000 (the dividends of two
    countries) and the two countries of Form T2209: the United States, 1500 of tax paid on 10000
    of net foreign non-business income, and the United Kingdom, 100 on 5000. They have no business
    figures (lines 4 to 6 of Form T2209 are 0), so the business credit is 0; `return_aw_business`
    adds them.
    """
    inputs: dict[str, Any] = {
        "employment_income": "50000",
        "share_dispositions": (),
        "unused_rrsp_contributions": "0",
        "rrsp_contributions": "0",
        "rrsp_deduction_limit": "0",
        "rrsp_amount_deducted": "0",
        "union_dues": "0",
        "t5_taxable_dividends_other_than_eligible": "200",
        "t5_taxable_dividends": "500",
        "t5_dividend_tax_credit": "60.00",
        "eligible_dividends_received_without_a_slip": "1000",
        "other_dividends_received_without_a_slip": "500",
        "foreign_investment_income": "15000",
        "income_tax_deducted": "9000",
        "foreign_tax_countries_rows": (US, UK),
    }
    return compute(**{**inputs, **overrides})


def return_aw_business(**overrides: Any) -> Worksheet:
    """Return AW in full, as in `returns/2025_return_aw.yaml`: `return_aw` with the business figures
    of both countries.

    The United States paid 400 of business income tax for the year, with 50 of unused business
    foreign tax credits, on 6000 of net foreign business income; the United Kingdom paid 60, with 0
    unused, on 3000. Line 6, the federal surtax on income allocated outside Canada, is 0 for both.
    """
    return return_aw(
        **{"foreign_tax_countries_rows": (US_WITH_BUSINESS, UK_WITH_BUSINESS), **overrides}
    )


def test_return_aws_net_income_and_basic_federal_tax_for_form_t2209_are_66990_and_7285_81() -> None:
    # Total income: 50000 + 2455.00 (line 12000, as Return K) + 15000 (line 12100, the foreign
    # investment income) = 67455.00. The enhanced CPP contributions, 1% x (50000 - 3500) =
    # 465.00, come off it: net income 66990.00, as is the TOSI-adjusted net income (no split
    # income) and taxable income. Note (3) subtracts the deductions it lists, none claimed: 0, so
    # net income is 66990.00 - 0. The federal tax on taxable income is 8319.38 + (66990.00 -
    # 57375.00) x 20.5% = 8319.38 + 1971.075 = 10290.455, half-up 10290.46; less the credits
    # against it, 3004.65 + 319.19 = 3323.84, line 42900 is 6966.62. Note (4): 6966.62 + the
    # dividend tax credit 319.19 = 7285.81, less a line 44100 of 0.
    worksheet = return_aw()

    assert worksheet.get(TOTAL_INCOME).value == D("67455.00")
    assert worksheet.get(NET_INCOME).value == D("66990.00")
    assert worksheet.get(TAXABLE_INCOME).value == D("66990.00")
    assert worksheet.get(TOSI_ADJUSTED_NET_INCOME).value == D("66990.00")
    assert worksheet.get(DIVIDEND_TAX_CREDIT).value == D("319.19")
    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("6966.62")
    assert worksheet.get(FOREIGN_TAX_CREDIT_NET_INCOME_DEDUCTIONS).value == D("0")
    assert worksheet.get(FOREIGN_TAX_CREDIT_NET_INCOME_BEFORE_SPLIT_INCOME).value == D("66990.00")
    assert worksheet.get(FOREIGN_TAX_CREDIT_NET_INCOME_WITH_SPLIT_INCOME).value == D("66990.00")
    assert worksheet.get(FOREIGN_TAX_CREDIT_NET_INCOME).value == D("66990.00")
    assert worksheet.get(BASIC_FEDERAL_TAX_WITH_DIVIDEND_CREDIT).value == D("7285.81")
    assert worksheet.get(FOREIGN_TAX_CREDIT_BASIC_FEDERAL_TAX).value == D("7285.81")


def test_two_countries_with_1600_of_foreign_tax_are_worked_one_by_one_giving_1187_60() -> None:
    # The total tax, 1500 + 100 = 1600, is more than 200 and there are two countries, so each is
    # worked on its own. United States: line 2 = 10000 x 7285.81 / 66990.00 = 1087.5966...,
    # half-up 1087.60; line 3 = lesser(1500, 1087.60) = 1087.60. United Kingdom: line 2 = 5000 x
    # 7285.81 / 66990.00 = 543.7983..., half-up 543.80; line 3 = lesser(100, 543.80) = 100. The
    # total is 1087.60 + 100 = 1187.60, not the pooled lesser(1600, 15000 x 7285.81 / 66990.00 =
    # 1631.39) = 1600.
    worksheet = return_aw()

    assert worksheet.get(FEDERAL_NON_BUSINESS_FOREIGN_TAX_CREDIT).value == D("1187.60")
    countries = [line for line in worksheet.trace if isinstance(line, ForeignTaxCreditLine)]
    assert countries == [
        ForeignTaxCreditLine(
            output=FEDERAL_NON_BUSINESS_FOREIGN_TAX_CREDIT,
            position=1,
            tax_paid=D("1500"),
            income=D("10000"),
            net_income=D("66990.00"),
            basic_federal_tax=D("7285.81"),
            rounding=CENT,
            line_2=D("1087.60"),
            result=D("1087.60"),
        ),
        ForeignTaxCreditLine(
            output=FEDERAL_NON_BUSINESS_FOREIGN_TAX_CREDIT,
            position=2,
            tax_paid=D("100"),
            income=D("5000"),
            net_income=D("66990.00"),
            basic_federal_tax=D("7285.81"),
            rounding=CENT,
            line_2=D("543.80"),
            result=D("100"),
        ),
    ]
    totals = [line for line in worksheet.trace if isinstance(line, ItemsTotalLine)]
    assert (
        ItemsTotalLine(
            FEDERAL_NON_BUSINESS_FOREIGN_TAX_CREDIT,
            ((1, D("1087.60")), (2, D("100"))),
            D("1187.60"),
        )
        in totals
    )
    assert not [line for line in worksheet.trace if isinstance(line, PooledForeignTaxCreditLine)]


def test_the_trace_names_each_country_and_the_federal_foreign_tax_credit() -> None:
    worksheet = return_aw()

    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "federal_non_business_foreign_tax_credit: country 1: tax paid 1500, "
        "10000 net foreign income x 7285.81 basic federal tax / 66990 net income = 1087.6 "
        "(half-up to 0.01); credit 1087.6"
    ) in rendered
    assert (
        "federal_non_business_foreign_tax_credit: country 2: tax paid 100, "
        "5000 net foreign income x 7285.81 basic federal tax / 66990 net income = 543.8 "
        "(half-up to 0.01); credit 100"
    ) in rendered
    assert (
        "federal_foreign_tax_credit: lesser of federal_foreign_tax_credit_before_limit 1187.6 "
        "and federal_tax_with_surtax 6966.62 = 1187.6"
    ) in rendered


def test_line_13_and_t1_line_129_are_1187_60_and_line_130_is_5779_02() -> None:
    # The credit, 1187.60, is less than line 42900 (6966.62), so line 13 is 1187.60 and so is T1
    # line 129 (line 40500). T1 line 130 is line 128 (line 126, 6966.62, as line 127 is not
    # triggered) less it, 6966.62 - 1187.60 = 5779.02; line 132 adds the recapture of 0.
    worksheet = return_aw()

    assert worksheet.get(FEDERAL_FOREIGN_TAX_CREDIT).value == D("1187.60")
    assert worksheet.get(FEDERAL_TAX_LESS_FOREIGN_TAX_CREDIT).value == D("5779.02")
    assert worksheet.get(FEDERAL_TAX_WITH_ITC_RECAPTURE).value == D("5779.02")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "federal_tax_less_foreign_tax_credit: federal_tax_with_surtax 6966.62 "
        "less federal_foreign_tax_credit 1187.6, not below 0 = 5779.02"
    ) in rendered
    assert (
        "federal_tax_with_itc_recapture: federal_tax_less_foreign_tax_credit 5779.02 "
        "+ itc_recapture 0 = 5779.02"
    ) in rendered


def test_the_credit_comes_off_the_net_federal_tax_the_total_payable_and_the_balance_owing() -> None:
    # Line 130 is 5779.02, and lines 132, 134 and 139 carry it (no recapture, no logging tax
    # credit, no credit against federal tax), so the net federal tax (line 142) is 5779.02. The
    # Ontario tax (line 147) is 3156.35 (see the return file), so the total payable (line 148) is
    # 5779.02 + 3156.35 = 8935.37 and, with 9000 of tax deducted, there is a refund of 64.63.
    worksheet = return_aw()

    assert worksheet.get(FEDERAL_TAX_LESS_CREDITS).value == D("5779.02")
    assert worksheet.get(NET_FEDERAL_TAX).value == D("5779.02")
    assert worksheet.get(ontario.ONTARIO_TAX).value == D("3156.35")
    assert worksheet.get(TOTAL_PAYABLE).value == D("8935.37")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-64.63")


def business_lines(worksheet: Worksheet, kind: type) -> list[Any]:
    """The trace lines of class `kind` the return produced, in order."""
    return [line for line in worksheet.trace if isinstance(line, kind)]


def test_the_business_lines_of_each_sheet_are_worked_with_the_basic_federal_tax_of_note_8() -> None:
    # Net income (note 3) is 66990.00 and the basic federal tax of note (8), "Line 42900 of your
    # return plus any federal dividend tax credit (line 40425 of your return).", is 6966.62 +
    # 319.19 = 7285.81. Both countries stay on their own sheets: the total foreign tax is 1500 +
    # 100 + 400 + 60 = 2060, more than 200 (the unused 50 is not tax paid). United States: line 4
    # = 400 + 50 = 450; line 5 = 6000 x 7285.81 / 66990.00 = 43714860.00 / 66990.00 = 652.5579...,
    # half-up 652.56; line 6 = 0; line 7 = 652.56; line 8 = 7285.81; line 9 = the line 3 of
    # 1087.60; line 10 = 7285.81 - 1087.60 = 6198.21; line 11 = least(450, 652.56, 6198.21) =
    # 450. United Kingdom: line 4 = 60; line 5 = 3000 x 7285.81 / 66990.00 = 326.2789..., half-up
    # 326.28; line 7 = 326.28; line 8 = 7285.81; line 9 = 100; line 10 = 7185.81; line 11 =
    # least(60, 326.28, 7185.81) = 60. Totals: line 4 510, line 5 978.84, line 7 978.84, line 8
    # 14571.62, line 10 13384.02, line 11 510.
    worksheet = return_aw_business()

    assert worksheet.get(FOREIGN_BUSINESS_TAX_CREDIT_LINE_4).value == D("510")
    assert worksheet.get(FOREIGN_BUSINESS_TAX_CREDIT_LINE_5).value == D("978.84")
    assert worksheet.get(FOREIGN_BUSINESS_TAX_CREDIT_LINE_7).value == D("978.84")
    assert worksheet.get(FOREIGN_BUSINESS_TAX_CREDIT_LINE_8).value == D("14571.62")
    assert worksheet.get(FOREIGN_BUSINESS_TAX_CREDIT_LINE_10).value == D("13384.02")
    assert worksheet.get(FEDERAL_BUSINESS_FOREIGN_TAX_CREDIT).value == D("510")
    assert worksheet.get(FEDERAL_NON_BUSINESS_FOREIGN_TAX_CREDIT).value == D("1187.60")
    assert not business_lines(worksheet, PooledForeignTaxCreditLine)


def test_the_trace_has_a_line_for_each_sheet_of_each_business_line_and_a_total() -> None:
    worksheet = return_aw_business()

    assert business_lines(worksheet, ForeignBusinessLine4) == [
        ForeignBusinessLine4(
            FOREIGN_BUSINESS_TAX_CREDIT_LINE_4,
            position=1,
            tax_paid=D("400"),
            unused_credits=D("50"),
            result=D("450"),
        ),
        ForeignBusinessLine4(
            FOREIGN_BUSINESS_TAX_CREDIT_LINE_4,
            position=2,
            tax_paid=D("60"),
            unused_credits=D("0"),
            result=D("60"),
        ),
    ]
    assert [
        (line.position, line.income, line.net_income, line.basic_federal_tax, line.result)
        for line in business_lines(worksheet, ForeignBusinessLine5)
    ] == [
        (1, D("6000"), D("66990.00"), D("7285.81"), D("652.56")),
        (2, D("3000"), D("66990.00"), D("7285.81"), D("326.28")),
    ]
    assert all(line.rounding == CENT for line in business_lines(worksheet, ForeignBusinessLine5))
    assert [
        (line.position, line.line_5, line.line_6, line.result)
        for line in business_lines(worksheet, ForeignBusinessLine7)
    ] == [(1, D("652.56"), D("0"), D("652.56")), (2, D("326.28"), D("0"), D("326.28"))]
    assert [
        (line.position, line.basic_federal_tax, line.line_6, line.result)
        for line in business_lines(worksheet, ForeignBusinessLine8)
    ] == [(1, D("7285.81"), D("0"), D("7285.81")), (2, D("7285.81"), D("0"), D("7285.81"))]
    assert [
        (line.position, line.line_8, line.line_3, line.result)
        for line in business_lines(worksheet, ForeignBusinessLine10)
    ] == [
        (1, D("7285.81"), D("1087.60"), D("6198.21")),
        (2, D("7285.81"), D("100"), D("7185.81")),
    ]
    assert [
        (line.position, line.line_4, line.line_7, line.line_10, line.result)
        for line in business_lines(worksheet, ForeignBusinessLine11)
    ] == [
        (1, D("450"), D("652.56"), D("6198.21"), D("450")),
        (2, D("60"), D("326.28"), D("7185.81"), D("60")),
    ]
    totals = business_lines(worksheet, ItemsTotalLine)
    assert (
        ItemsTotalLine(FEDERAL_BUSINESS_FOREIGN_TAX_CREDIT, ((1, D("450")), (2, D("60"))), D("510"))
        in totals
    )
    assert (
        ItemsTotalLine(
            FOREIGN_BUSINESS_TAX_CREDIT_LINE_5,
            ((1, D("652.56")), (2, D("326.28"))),
            D("978.84"),
        )
        in totals
    )


def test_the_trace_names_each_sheet_of_the_business_lines_line_13_and_the_limit() -> None:
    worksheet = return_aw_business()

    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "foreign_business_tax_credit_line_4: sheet 1: line 4 = business income tax paid 400 + "
        "unused foreign tax credits 50 = 450"
    ) in rendered
    assert (
        "foreign_business_tax_credit_line_5: sheet 2: line 5 = 3000 net foreign business income "
        "x 7285.81 basic federal tax / 66990 net income = 326.28 (half-up to 0.01)"
    ) in rendered
    assert (
        "federal_business_foreign_tax_credit: sheet 1: line 11 = least of line 4 450, line 7 "
        "652.56, line 10 6198.21 = 450"
    ) in rendered
    assert (
        "federal_foreign_tax_credit_before_limit: federal_business_foreign_tax_credit 510 + "
        "federal_non_business_foreign_tax_credit 1187.6 = 1697.6"
    ) in rendered
    assert (
        "federal_foreign_tax_credit: lesser of federal_foreign_tax_credit_before_limit 1697.6 "
        "and federal_tax_with_surtax 6966.62 = 1697.6"
    ) in rendered


def test_line_13_is_lines_11_and_12_and_t1_line_129_is_1697_60_and_line_130_is_5269_02() -> None:
    # Line 11 is 510 and line 12 "the amount from line 3" is 1187.60, so line 13 "Add lines 11 and
    # 12." is 510 + 1187.60 = 1697.60. It is less than line 42900 (6966.62), so T1 line 129 (line
    # 40500) is 1697.60; line 130 is 6966.62 - 1697.60 = 5269.02, and lines 132 to 142 carry it.
    worksheet = return_aw_business()

    assert worksheet.get(FEDERAL_FOREIGN_TAX_CREDIT_BEFORE_LIMIT).value == D("1697.60")
    assert worksheet.get(FEDERAL_FOREIGN_TAX_CREDIT).value == D("1697.60")
    assert worksheet.get(FEDERAL_TAX_LESS_FOREIGN_TAX_CREDIT).value == D("5269.02")
    assert worksheet.get(FEDERAL_TAX_WITH_ITC_RECAPTURE).value == D("5269.02")
    assert worksheet.get(FEDERAL_TAX_LESS_CREDITS).value == D("5269.02")
    assert worksheet.get(NET_FEDERAL_TAX).value == D("5269.02")


def test_the_business_credit_comes_off_the_net_federal_tax_the_total_payable_and_the_refund() -> (
    None
):
    # Net federal tax 5269.02 + Ontario tax 3156.35 (form T2036 reads the non-business figures
    # only, so it is unchanged) = 8425.37 against 9000 deducted: a refund of 574.63, which is the
    # net refund as there is no donation to the opportunities fund.
    worksheet = return_aw_business()

    assert worksheet.get(ontario.PROVINCIAL_FOREIGN_TAX_CREDIT).value == D("412.40")
    assert worksheet.get(ontario.ONTARIO_TAX).value == D("3156.35")
    assert worksheet.get(TOTAL_PAYABLE).value == D("8425.37")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-574.63")
    assert worksheet.get(REFUND).value == D("574.63")
    assert worksheet.get(ontario.NET_REFUND).value == D("574.63")


def test_the_business_tax_paid_counts_toward_the_200_that_chooses_separate_sheets() -> None:
    # Non-business tax of 50 + 100 = 150 is not more than 200, but with the business tax paid, 30 +
    # 40, the total foreign tax is 220, so each country is on its own sheet (the non-business tax
    # alone would pool them). Sheet 1: line 2 = 1000 x 7285.81 / 66990.00 = 108.76, line 3 =
    # least(50, 108.76) = 50; line 4 = 30, line 5 = 1000 x 7285.81 / 66990.00 = 108.76, line 8 =
    # 7285.81, line 10 = 7285.81 - 50 = 7235.81, line 11 = least(30, 108.76, 7235.81) = 30.
    # Sheet 2: line 2 = 500 x 7285.81 / 66990.00 = 54.38, line 3 = 54.38; line 4 = 40, line 5 =
    # 54.38, line 10 = 7285.81 - 54.38 = 7231.43, line 11 = least(40, 54.38, 7231.43) = 40. Line
    # 3 total 104.38, line 11 total 70, line 13 = 174.38, line 130 = 6966.62 - 174.38 = 6792.24.
    worksheet = return_aw(
        foreign_tax_countries_rows=(
            ("50", "1000", "30", "0", "1000", "0"),
            ("100", "500", "40", "0", "500", "0"),
        )
    )

    assert not business_lines(worksheet, PooledForeignTaxCreditLine)
    assert worksheet.get(FEDERAL_NON_BUSINESS_FOREIGN_TAX_CREDIT).value == D("104.38")
    assert worksheet.get(FOREIGN_BUSINESS_TAX_CREDIT_LINE_4).value == D("70")
    assert worksheet.get(FEDERAL_BUSINESS_FOREIGN_TAX_CREDIT).value == D("70")
    assert worksheet.get(FEDERAL_FOREIGN_TAX_CREDIT).value == D("174.38")
    assert worksheet.get(FEDERAL_TAX_LESS_FOREIGN_TAX_CREDIT).value == D("6792.24")


def test_line_6_is_added_into_lines_7_and_8_and_so_into_the_least_of_lines_4_7_and_10() -> None:
    # One country with no non-business figures, 1000 of business tax paid on 5000 of net foreign
    # business income and a line 6 of 100: line 4 = 1000; line 5 = 5000 x 7285.81 / 66990.00 =
    # 543.7983..., half-up 543.80; line 7 = 543.80 + 100 = 643.80; line 8 = 7285.81 + 100 =
    # 7385.81; line 9 = 0; line 10 = 7385.81; line 11 = least(1000, 643.80, 7385.81) = 643.80.
    # Line 13 = 643.80 + 0, below line 42900, so line 130 = 6966.62 - 643.80 = 6322.82.
    worksheet = return_aw(foreign_tax_countries_rows=(("0", "0", "1000", "0", "5000", "100"),))

    assert worksheet.get(FOREIGN_BUSINESS_TAX_CREDIT_LINE_4).value == D("1000")
    assert worksheet.get(FOREIGN_BUSINESS_TAX_CREDIT_LINE_5).value == D("543.80")
    assert worksheet.get(FOREIGN_BUSINESS_TAX_CREDIT_LINE_7).value == D("643.80")
    assert worksheet.get(FOREIGN_BUSINESS_TAX_CREDIT_LINE_8).value == D("7385.81")
    assert worksheet.get(FOREIGN_BUSINESS_TAX_CREDIT_LINE_10).value == D("7385.81")
    assert worksheet.get(FEDERAL_BUSINESS_FOREIGN_TAX_CREDIT).value == D("643.80")
    assert worksheet.get(FEDERAL_FOREIGN_TAX_CREDIT).value == D("643.80")
    assert worksheet.get(FEDERAL_TAX_LESS_FOREIGN_TAX_CREDIT).value == D("6322.82")


def test_business_income_above_net_income_is_capped_and_line_13_cannot_exceed_line_42900() -> None:
    # Note (7): 100000 of net foreign business income is more than the net income of 66990.00, so
    # the net income is used: line 5 = 66990.00 x 7285.81 / 66990.00 = 7285.81. With 8000 of
    # business tax paid, line 4 = 8000, line 7 = 7285.81, line 8 = 7285.81 and line 10 = 7285.81 -
    # 0 (no non-business figures) = 7285.81, so line 11 = 7285.81. Line 13 is 7285.81, but "should
    # not be more than" line 42900, 6966.62: T1 line 129 is 6966.62 and line 130 is 0.
    worksheet = return_aw(foreign_tax_countries_rows=(("0", "0", "8000", "0", "100000", "0"),))

    assert worksheet.get(FOREIGN_BUSINESS_TAX_CREDIT_LINE_5).value == D("7285.81")
    assert worksheet.get(FEDERAL_BUSINESS_FOREIGN_TAX_CREDIT).value == D("7285.81")
    assert worksheet.get(FEDERAL_FOREIGN_TAX_CREDIT_BEFORE_LIMIT).value == D("7285.81")
    assert worksheet.get(FEDERAL_FOREIGN_TAX_CREDIT).value == D("6966.62")
    assert worksheet.get(FEDERAL_TAX_LESS_FOREIGN_TAX_CREDIT).value == D("0")
    assert worksheet.get(NET_FEDERAL_TAX).value == D("0")


def test_a_return_with_no_countries_has_no_business_credit_either() -> None:
    worksheet = return_aw(foreign_tax_countries_rows=())

    assert worksheet.get(FOREIGN_BUSINESS_TAX_CREDIT_LINE_4).value == D("0")
    assert worksheet.get(FOREIGN_BUSINESS_TAX_CREDIT_LINE_10).value == D("0")
    assert worksheet.get(FEDERAL_BUSINESS_FOREIGN_TAX_CREDIT).value == D("0")
    assert worksheet.get(FEDERAL_FOREIGN_TAX_CREDIT_BEFORE_LIMIT).value == D("0")
    assert worksheet.get(FEDERAL_FOREIGN_TAX_CREDIT).value == D("0")


def test_a_total_of_exactly_200_of_foreign_tax_is_pooled() -> None:
    # Two countries paying 50 and 150, total 200, which is not more than 200: one calculation on
    # the totals. Income 1000 + 500 = 1500, line 2 = 1500 x 7285.81 / 66990.00 = 163.1394...,
    # half-up 163.14; line 3 = lesser(200, 163.14) = 163.14. Worked one by one it would be
    # lesser(50, 108.76) + lesser(150, 54.38) = 50 + 54.38 = 104.38. Line 130 is 6966.62 -
    # 163.14 = 6803.48.
    worksheet = return_aw(foreign_tax_countries_rows=(("50", "1000"), ("150", "500")))

    assert worksheet.get(FEDERAL_NON_BUSINESS_FOREIGN_TAX_CREDIT).value == D("163.14")
    assert worksheet.get(FEDERAL_FOREIGN_TAX_CREDIT).value == D("163.14")
    assert worksheet.get(FEDERAL_TAX_LESS_FOREIGN_TAX_CREDIT).value == D("6803.48")
    assert [line for line in worksheet.trace if isinstance(line, PooledForeignTaxCreditLine)] == [
        PooledForeignTaxCreditLine(
            output=FEDERAL_NON_BUSINESS_FOREIGN_TAX_CREDIT,
            countries=2,
            tax_paid=D("200"),
            income=D("1500"),
            net_income=D("66990.00"),
            basic_federal_tax=D("7285.81"),
            total_foreign_taxes=D("200"),
            threshold=D("200"),
            rounding=CENT,
            line_2=D("163.14"),
            result=D("163.14"),
        )
    ]
    assert not [line for line in worksheet.trace if isinstance(line, ForeignTaxCreditLine)]
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "federal_non_business_foreign_tax_credit: all 2 countries pooled, total foreign taxes "
        "200 is not more than 200: tax paid 200, 1500 net foreign income x 7285.81 basic federal "
        "tax / 66990 net income = 163.14 (half-up to 0.01); credit 163.14"
    ) in rendered


def test_a_total_of_200_01_of_foreign_tax_is_worked_country_by_country() -> None:
    # The same two countries with 150.01 paid to the second: the total, 200.01, is more than 200,
    # so each is worked on its own. First: lesser(50, 1000 x 7285.81 / 66990.00 = 108.76) = 50.
    # Second: lesser(150.01, 500 x 7285.81 / 66990.00 = 54.38) = 54.38. The total is 104.38, and
    # line 130 is 6966.62 - 104.38 = 6862.24.
    worksheet = return_aw(foreign_tax_countries_rows=(("50", "1000"), ("150.01", "500")))

    assert worksheet.get(FEDERAL_NON_BUSINESS_FOREIGN_TAX_CREDIT).value == D("104.38")
    assert worksheet.get(FEDERAL_TAX_LESS_FOREIGN_TAX_CREDIT).value == D("6862.24")
    lines = [line for line in worksheet.trace if isinstance(line, ForeignTaxCreditLine)]
    assert [(line.position, line.line_2, line.result) for line in lines] == [
        (1, D("108.76"), D("50")),
        (2, D("54.38"), D("54.38")),
    ]
    assert not [line for line in worksheet.trace if isinstance(line, PooledForeignTaxCreditLine)]


def test_a_single_country_is_one_calculation_whatever_it_paid() -> None:
    # One country (the form asks for a separate sheet only for "more than one foreign country"):
    # the United States alone, 1500 of tax on 10000 of income: line 2 = 1087.60, line 3 = 1087.60,
    # the same figure pooled or not.
    worksheet = return_aw(foreign_tax_countries_rows=(US,))

    assert worksheet.get(FEDERAL_NON_BUSINESS_FOREIGN_TAX_CREDIT).value == D("1087.60")
    assert worksheet.get(FEDERAL_TAX_LESS_FOREIGN_TAX_CREDIT).value == D("5879.02")
    pooled = [line for line in worksheet.trace if isinstance(line, PooledForeignTaxCreditLine)]
    assert [(line.countries, line.tax_paid, line.result) for line in pooled] == [
        (1, D("1500"), D("1087.60"))
    ]


def test_income_above_net_income_is_capped_and_the_credit_cannot_exceed_line_42900() -> None:
    # Note (2): a country's income of 100000 is more than the net income of 66990.00, so the net
    # income is used: line 2 = 66990.00 x 7285.81 / 66990.00 = 7285.81 and line 3 = lesser(8000,
    # 7285.81) = 7285.81. Basic federal tax (note 4) is more than line 42900 by the dividend tax
    # credit, so line 13 "should not be more than" line 42900, 6966.62: 6966.62. Line 130 is
    # 6966.62 - 6966.62 = 0, so the net federal tax is 0 and the total payable is the Ontario tax.
    # Form T2036 has the same sheet (line 1 8000, line 2 the T2209 line 3 7285.81, line 3 =
    # 714.19; line 4 = 66990.00 x 3159.89 / 66990.00 = 3159.89; line 5 = 714.19), so ON428 line 83
    # is 2968.75 - 714.19 = 2254.56 and the Ontario tax is 2254.56 + 600 = 2854.56, with a refund
    # of 9000 - 2854.56 = 6145.44.
    worksheet = return_aw(foreign_tax_countries_rows=(("8000", "100000"),))

    assert worksheet.get(FEDERAL_NON_BUSINESS_FOREIGN_TAX_CREDIT).value == D("7285.81")
    assert worksheet.get(FEDERAL_FOREIGN_TAX_CREDIT).value == D("6966.62")
    assert worksheet.get(FEDERAL_TAX_LESS_FOREIGN_TAX_CREDIT).value == D("0")
    assert worksheet.get(NET_FEDERAL_TAX).value == D("0")
    assert worksheet.get(ontario.PROVINCIAL_FOREIGN_TAX_CREDIT).value == D("714.19")
    assert worksheet.get(ontario.ONTARIO_TAX).value == D("2854.56")
    assert worksheet.get(TOTAL_PAYABLE).value == D("2854.56")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-6145.44")


def test_the_deductions_of_note_3_come_off_net_income_in_the_basic_federal_tax_ratio() -> None:
    # Income: 67455.00 + 800 of workers' compensation (line 14400) = 68255.00, less the 465.00
    # of enhanced CPP contributions: net income 67790.00. Note (3) subtracts: line 24400 1000,
    # line 24900 500, line 25000 800 (the other payments deduction, line 14700), line 25300 0,
    # lines 25395 and 25400 0 (the Forms T2048 and T657 deductions, tested below) and the 200 of
    # line 25600 that is exempt income: 2500, so its net income is 67790.00 - 2500 = 65290.00. Lines
    # 24400, 24900, 25000 and 25600 (200 entered as additional deductions) come off for taxable
    # income, 67790.00 - 2500 = 65290.00. The federal tax on it is
    # 8319.38 + (65290.00 - 57375.00) x 20.5% = 8319.38 + 1622.575 = 9941.955, half-up 9941.96;
    # less 3323.84, line 42900 is 6618.12 and the basic federal tax is 6618.12 + 319.19 =
    # 6937.31. United States:
    # line 2 = 10000 x 6937.31 / 65290.00 = 1062.5..., half-up 1062.54, below 1500; United
    # Kingdom: 5000 x 6937.31 / 65290.00 = 531.2..., half-up 531.27, above 100. The credit is
    # 1062.54 + 100 = 1162.54.
    worksheet = return_aw(
        workers_compensation_benefits="800",
        canadian_armed_forces_and_police_deduction="1000",
        security_options_deductions="500",
        additional_deductions="200",
        exempt_income_deductions="200",
    )

    assert worksheet.get(NET_INCOME).value == D("67790.00")
    assert worksheet.get(TAXABLE_INCOME).value == D("65290.00")
    assert worksheet.get(FOREIGN_TAX_CREDIT_NET_INCOME_DEDUCTIONS).value == D("2500.00")
    assert worksheet.get(FOREIGN_TAX_CREDIT_NET_INCOME).value == D("65290.00")
    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("6618.12")
    assert worksheet.get(FOREIGN_TAX_CREDIT_BASIC_FEDERAL_TAX).value == D("6937.31")
    assert worksheet.get(FEDERAL_NON_BUSINESS_FOREIGN_TAX_CREDIT).value == D("1162.54")
    assert worksheet.get(FEDERAL_TAX_LESS_FOREIGN_TAX_CREDIT).value == D("5455.58")


def test_the_form_t2048_deduction_comes_off_net_income_in_the_basic_federal_tax_ratio() -> None:
    # Line 25395 is Form T2048's line 27, 60500 for the Return BE filer (the deduction is
    # computed, not entered); with the two countries of Return AW added, note (3) subtracts it and
    # the 30000 of line 25300: 90500.00.
    worksheet = return_be(foreign_tax_countries_rows=(US, UK))

    assert worksheet.get(FOREIGN_TAX_CREDIT_NET_INCOME_DEDUCTIONS).value == D("90500.00")


def test_the_form_t657_deduction_comes_off_net_income_in_the_basic_federal_tax_ratio() -> None:
    # Line 25400 is Form T657's claim, 155000 for the Return BF filer; with the two countries of
    # Return AW added, note (3) subtracts it and the 20000 of line 25300: 175000.00.
    worksheet = return_bf(foreign_tax_countries_rows=(US, UK))

    assert worksheet.get(FOREIGN_TAX_CREDIT_NET_INCOME_DEDUCTIONS).value == D("175000.00")


def test_the_first_nations_abatement_comes_off_the_basic_federal_tax() -> None:
    # Note (4), "minus any" "federal refundable First Nations abatement (line 44100 of your
    # return)": 7285.81 - 500 = 6785.81. United States: line 2 = 10000 x 6785.81 / 66990.00 =
    # 1012.9586..., half-up 1012.96; United Kingdom: 5000 x 6785.81 / 66990.00 = 506.4793...,
    # half-up 506.48, above 100. The credit is 1012.96 + 100 = 1112.96. Nothing else reads the
    # abatement, so line 42900 is unchanged and line 130 is 6966.62 - 1112.96 = 5853.66.
    worksheet = return_aw(first_nations_abatement="500")

    assert worksheet.get(BASIC_FEDERAL_TAX_WITH_DIVIDEND_CREDIT).value == D("7285.81")
    assert worksheet.get(FOREIGN_TAX_CREDIT_BASIC_FEDERAL_TAX).value == D("6785.81")
    assert worksheet.get(FEDERAL_NON_BUSINESS_FOREIGN_TAX_CREDIT).value == D("1112.96")
    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("6966.62")
    assert worksheet.get(FEDERAL_TAX_LESS_FOREIGN_TAX_CREDIT).value == D("5853.66")


def test_a_return_with_no_countries_has_no_credit_and_line_130_is_line_126() -> None:
    # The same filer with no country listed: the total of line 3 is 0 without consulting the
    # net income, so line 13 is 0 and line 130 is 6966.62 - 0. The net federal tax is 6966.62,
    # the total payable 6966.62 + 3568.75 = 10535.37 and the balance owing 10535.37 - 9000 =
    # 1535.37.
    worksheet = return_aw(foreign_tax_countries_rows=())

    assert worksheet.get(FEDERAL_NON_BUSINESS_FOREIGN_TAX_CREDIT).value == D("0")
    assert worksheet.get(FEDERAL_FOREIGN_TAX_CREDIT).value == D("0")
    assert worksheet.get(FEDERAL_TAX_LESS_FOREIGN_TAX_CREDIT).value == D("6966.62")
    assert worksheet.get(FEDERAL_TAX_WITH_ITC_RECAPTURE).value == D("6966.62")
    assert worksheet.get(NET_FEDERAL_TAX).value == D("6966.62")
    assert worksheet.get(TOTAL_PAYABLE).value == D("10535.37")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("1535.37")
    totals = [line for line in worksheet.trace if isinstance(line, ItemsTotalLine)]
    assert ItemsTotalLine(FEDERAL_NON_BUSINESS_FOREIGN_TAX_CREDIT, (), D("0")) in totals


def test_a_return_without_the_list_is_unchanged_by_the_foreign_tax_credit() -> None:
    # Return K lists no country: its credit is 0 and its lines 126 to 148 are what they were,
    # 4214.71 for the basic federal tax and the net federal tax, and 6447.70 for the total
    # payable (see `returns/2025_return_k.yaml`).
    worksheet = return_k()

    assert worksheet.get(FEDERAL_NON_BUSINESS_FOREIGN_TAX_CREDIT).value == D("0")
    assert worksheet.get(FEDERAL_FOREIGN_TAX_CREDIT).value == D("0")
    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("4214.71")
    assert worksheet.get(FEDERAL_TAX_LESS_FOREIGN_TAX_CREDIT).value == D("4214.71")
    assert worksheet.get(FEDERAL_TAX_WITH_ITC_RECAPTURE).value == D("4214.71")
    assert worksheet.get(NET_FEDERAL_TAX).value == D("4214.71")
    assert worksheet.get(TOTAL_PAYABLE).value == D("6447.70")


def test_note_3_net_income_and_tosi_adjusted_net_income_take_line_23500_off() -> None:
    # Return AS's filer, employment income of 92074 and old age security of 9000 (line 11300), with
    # no dividends or foreign income and no tax deducted. Total income is 92074 + 9000 = 101074; the
    # enhanced CPP contributions (678.00 + 396.00 = 1074.00) come off it, so line 23400 is
    # 100000.00. The social benefits repayment (line 23500) is 15% x (100000.00 - 93343.00) =
    # 998.55, so line 23600 is 99001.45 and note (3) starts from it: 100000.00 - 998.55 =
    # 99001.45, plus a line 68360 of 0 and less deductions of 0, so net income is 99001.45. The
    # TOSI-adjusted net income is 0 + 99001.45 = 99001.45, line 23600 before its floor plus the
    # split income, so it is note (3)'s starting point too.
    # Taxable income is 99001.45: the federal tax is 8319.38 + (99001.45 - 57375) x 20.5% =
    # 8319.38 + 8533.42225, 16852.80; the credits are (16129 + 3356.10 + 1077.48 + 1471) x 14.5% =
    # 22033.58 x 14.5% = 3194.87, so line 42900 is 13657.93, the basic federal tax (note 4) with no
    # dividend credit or abatement. Line 2 for the one country is 10000 x 13657.93 / 99001.45 =
    # 1379.5712, 1379.57, below its 1500 paid: line 3 and line 13 (40500) are 1379.57, and T1
    # line 130 is 13657.93 - 1379.57 = 12278.36. The total payable is 12278.36 + 998.55 (line
    # 42200) + 6714.79 (the Ontario tax, see below) = 19991.70; nothing was deducted at source.
    # Ontario: line 69 is 6085.22 (Return AS's 6835.22 less its health premium of 750.00), with no
    # dividends line 70 is 0, so the tax otherwise payable is 6085.22. Form T2036: line 1 is 1500,
    # line 2 the T2209 line 3, 1379.57, line 3 is 120.43; line 4 is 10000 x 6085.22 / 99001.45 =
    # 614.6596..., rounded 614.66, so line 5 is 120.43; ON428 line 83 is 6085.22 - 120.43 = 5964.79
    # and the Ontario tax is 5964.79 + 750.00 = 6714.79.
    worksheet = return_aw(
        employment_income="92074",
        old_age_security="9000",
        t5_taxable_dividends_other_than_eligible="0",
        t5_taxable_dividends="0",
        t5_dividend_tax_credit="0",
        eligible_dividends_received_without_a_slip="0",
        other_dividends_received_without_a_slip="0",
        foreign_investment_income="0",
        income_tax_deducted="0",
        foreign_tax_countries_rows=(US,),
    )

    assert worksheet.get(NET_INCOME_BEFORE_ADJUSTMENTS).value == D("100000.00")
    assert worksheet.get(SOCIAL_BENEFITS_REPAYMENT).value == D("998.55")
    assert worksheet.get(NET_INCOME).value == D("99001.45")
    assert worksheet.get(TOSI_ADJUSTED_NET_INCOME).value == D("99001.45")
    assert worksheet.get(FOREIGN_TAX_CREDIT_NET_INCOME_BEFORE_SPLIT_INCOME).value == D("99001.45")
    assert worksheet.get(FOREIGN_TAX_CREDIT_NET_INCOME_WITH_SPLIT_INCOME).value == D("99001.45")
    assert worksheet.get(FOREIGN_TAX_CREDIT_NET_INCOME).value == D("99001.45")
    assert [
        line
        for line in worksheet.trace
        if isinstance(line, SubtractedLine)
        and line.output == FOREIGN_TAX_CREDIT_NET_INCOME_BEFORE_SPLIT_INCOME
    ] == [
        SubtractedLine(
            output=FOREIGN_TAX_CREDIT_NET_INCOME_BEFORE_SPLIT_INCOME,
            minuend=NET_INCOME_BEFORE_ADJUSTMENTS,
            minuend_amount=D("100000.00"),
            subtrahend=SOCIAL_BENEFITS_REPAYMENT,
            subtrahend_amount=D("998.55"),
            result=D("99001.45"),
        )
    ]
    assert [
        line
        for line in worksheet.trace
        if isinstance(line, SumLine)
        and line.output == FOREIGN_TAX_CREDIT_NET_INCOME_WITH_SPLIT_INCOME
    ] == [
        SumLine(
            FOREIGN_TAX_CREDIT_NET_INCOME_WITH_SPLIT_INCOME,
            (
                (FOREIGN_TAX_CREDIT_NET_INCOME_BEFORE_SPLIT_INCOME, D("99001.45")),
                (TOTAL_SPLIT_INCOME, D("0")),
            ),
            D("99001.45"),
        )
    ]
    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("13657.93")
    assert worksheet.get(BASIC_FEDERAL_TAX_WITH_DIVIDEND_CREDIT).value == D("13657.93")
    assert worksheet.get(FOREIGN_TAX_CREDIT_BASIC_FEDERAL_TAX).value == D("13657.93")
    assert worksheet.get(FEDERAL_NON_BUSINESS_FOREIGN_TAX_CREDIT).value == D("1379.57")
    assert worksheet.get(FEDERAL_FOREIGN_TAX_CREDIT).value == D("1379.57")
    assert worksheet.get(FEDERAL_TAX_LESS_FOREIGN_TAX_CREDIT).value == D("12278.36")
    assert worksheet.get(NET_FEDERAL_TAX).value == D("12278.36")
    assert worksheet.get(ontario.TAX_OTHERWISE_PAYABLE).value == D("6085.22")
    assert worksheet.get(ontario.PROVINCIAL_FOREIGN_TAX_CREDIT).value == D("120.43")
    assert worksheet.get(ontario.ONTARIO_TAX).value == D("6714.79")
    assert worksheet.get(TOTAL_PAYABLE).value == D("19991.70")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("19991.70")


# --- Ontario: Form T2036 and ON428 lines 82 and 83 ------------------------------------------------


def sheets_of(worksheet: Worksheet) -> list[tuple[Decimal, Decimal, Decimal]]:
    """The T2209 sheets (line 1, income used on line 2, line 3) the return produced, in order."""
    value = worksheet.get(FOREIGN_TAX_CREDIT_SHEETS).value
    assert isinstance(value, RecordList)
    return [
        (
            Decimal(record[FOREIGN_NON_BUSINESS_TAX_PAID]),
            Decimal(record[NET_FOREIGN_NON_BUSINESS_INCOME]),
            Decimal(record[FOREIGN_TAX_CREDIT_SHEET_LINE_3]),
        )
        for record in value.records
    ]


def t2036_lines(worksheet: Worksheet) -> list[ProvincialForeignTaxCreditLine]:
    return [line for line in worksheet.trace if isinstance(line, ProvincialForeignTaxCreditLine)]


def test_the_tax_otherwise_payable_is_on428_line_81_with_0_on_lines_70_and_72() -> None:
    # Form T2036 note (4): "If you were a resident of Ontario, calculate this amount by entering
    # "0" on lines 70 and 72 of Form ON428 and continue the calculation. The result from line 81
    # is your provincial or territorial tax otherwise payable." Line 69 is 3159.89. With "0" on
    # line 70 (the Ontario dividend tax credit of 191.14 is not taken off) line 71 is 3159.89 -
    # 0 = 3159.89, and with "0" on line 72 line 73 is 3159.89 + 0. The reduction amounts, 294.00
    # twice, 588.00, less line 79 (3159.89) is negative, so line 80 is 0 and line 81 is 3159.89.
    # The Ontario tax itself still takes the credit off: line 81 is 2968.75.
    worksheet = return_aw()

    assert worksheet.get(ontario.ONTARIO_TAX_WITH_SURTAX).value == D("3159.89")
    assert worksheet.get(ontario.DIVIDEND_CREDIT_FROM_LINE_57).value == D("191.14")
    assert worksheet.get(ontario.TAX_OTHERWISE_PAYABLE_LINE_71).value == D("3159.89")
    assert worksheet.get(ontario.TAX_OTHERWISE_PAYABLE_LINE_73).value == D("3159.89")
    assert worksheet.get(ontario.TAX_REDUCTION_AMOUNTS).value == D("294.00")
    assert worksheet.get(ontario.TAX_OTHERWISE_PAYABLE_REDUCTION_BEFORE_CONDITIONS).value == D("0")
    assert worksheet.get(ontario.TAX_OTHERWISE_PAYABLE_REDUCTION_CLAIMABLE).value == 1
    assert worksheet.get(ontario.TAX_OTHERWISE_PAYABLE_REDUCTION).value == D("0")
    assert worksheet.get(ontario.TAX_OTHERWISE_PAYABLE).value == D("3159.89")
    assert worksheet.get(ontario.ONTARIO_TAX_AFTER_DIVIDEND_CREDIT).value == D("2968.75")
    assert worksheet.get(ontario.ONTARIO_TAX_BEFORE_REDUCTION).value == D("2968.75")
    assert worksheet.get(ontario.ONTARIO_TAX_AFTER_REDUCTION).value == D("2968.75")
    assert [
        line
        for line in worksheet.trace
        if isinstance(line, SumLine)
        and line.output
        in (ontario.TAX_OTHERWISE_PAYABLE_LINE_71, ontario.TAX_OTHERWISE_PAYABLE_LINE_73)
    ] == [
        SumLine(
            ontario.TAX_OTHERWISE_PAYABLE_LINE_71,
            ((ontario.ONTARIO_TAX_WITH_SURTAX, D("3159.89")),),
            D("3159.89"),
        ),
        SumLine(
            ontario.TAX_OTHERWISE_PAYABLE_LINE_73,
            ((ontario.TAX_OTHERWISE_PAYABLE_LINE_71, D("3159.89")),),
            D("3159.89"),
        ),
    ]


def test_two_countries_give_a_provincial_credit_of_412_40_from_form_t2036() -> None:
    # The two sheets of Form T2209. United States: line 1 1500; line 2 the T2209 line 3, 1087.60;
    # line 3 = 1500 - 1087.60 = 412.40; line 4 = 10000 x 3159.89 / 66990.00 = 471.6957..., half-up
    # 471.70; line 5 = lesser(412.40, 471.70) = 412.40. United Kingdom: line 1 100; line 2 100;
    # line 3 = 0; line 4 = 5000 x 3159.89 / 66990.00 = 235.8478..., half-up 235.85; line 5 =
    # lesser(0, 235.85) = 0. The total of line 5 is 412.40, which is not more than the tax
    # otherwise payable, 3159.89, so ON428 line 82 is 412.40 and line 83 = 2968.75 - 412.40 =
    # 2556.35, which lines 84 and 86 carry (the LIFT credit is 0) to line 88: 2556.35, and the
    # Ontario tax (line 90) is 2556.35 + 600 = 3156.35.
    worksheet = return_aw()

    assert sheets_of(worksheet) == [
        (D("1500"), D("10000"), D("1087.60")),
        (D("100"), D("5000"), D("100")),
    ]
    assert t2036_lines(worksheet) == [
        ProvincialForeignTaxCreditLine(
            output=ontario.PROVINCIAL_FOREIGN_TAX_CREDIT_BEFORE_LIMIT,
            position=1,
            tax_paid=D("1500"),
            federal_credit=D("1087.60"),
            line_3=D("412.40"),
            income=D("10000"),
            net_income=D("66990.00"),
            provincial_tax=D("3159.89"),
            rounding=CENT,
            line_4=D("471.70"),
            result=D("412.40"),
        ),
        ProvincialForeignTaxCreditLine(
            output=ontario.PROVINCIAL_FOREIGN_TAX_CREDIT_BEFORE_LIMIT,
            position=2,
            tax_paid=D("100"),
            federal_credit=D("100"),
            line_3=D("0"),
            income=D("5000"),
            net_income=D("66990.00"),
            provincial_tax=D("3159.89"),
            rounding=CENT,
            line_4=D("235.85"),
            result=D("0"),
        ),
    ]
    totals = [line for line in worksheet.trace if isinstance(line, ItemsTotalLine)]
    assert (
        ItemsTotalLine(
            ontario.PROVINCIAL_FOREIGN_TAX_CREDIT_BEFORE_LIMIT,
            ((1, D("412.40")), (2, D("0"))),
            D("412.40"),
        )
        in totals
    )
    assert worksheet.get(ontario.PROVINCIAL_FOREIGN_TAX_CREDIT_BEFORE_LIMIT).value == D("412.40")
    assert worksheet.get(ontario.PROVINCIAL_FOREIGN_TAX_CREDIT).value == D("412.40")
    assert worksheet.get(ontario.ONTARIO_TAX_AFTER_FOREIGN_TAX_CREDIT).value == D("2556.35")
    assert worksheet.get(ontario.LIFT_CREDIT).value == D("0")
    assert worksheet.get(ontario.ONTARIO_TAX_AFTER_LIFT_CREDIT).value == D("2556.35")
    assert worksheet.get(ontario.ONTARIO_TAX_AFTER_FOOD_CREDIT).value == D("2556.35")
    assert worksheet.get(ontario.ONTARIO_HEALTH_PREMIUM).value == D("600.00")
    assert worksheet.get(ontario.ONTARIO_TAX).value == D("3156.35")


def test_the_trace_names_each_sheet_the_limit_and_line_83() -> None:
    worksheet = return_aw()

    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "provincial_foreign_tax_credit_before_limit: sheet 1: tax paid 1500 less federal credit "
        "1087.6 = 412.4; 10000 net foreign income x 3159.89 provincial tax / 66990 net income = "
        "471.7 (half-up to 0.01); credit 412.4"
    ) in rendered
    assert (
        "provincial_foreign_tax_credit_before_limit: sheet 2: tax paid 100 less federal credit "
        "100 = 0; 5000 net foreign income x 3159.89 provincial tax / 66990 net income = 235.85 "
        "(half-up to 0.01); credit 0"
    ) in rendered
    assert (
        "provincial_foreign_tax_credit: lesser of provincial_foreign_tax_credit_before_limit "
        "412.4 and tax_otherwise_payable 3159.89 = 412.4"
    ) in rendered
    assert (
        "ontario_tax_after_foreign_tax_credit: ontario_tax_after_reduction 2968.75 less "
        "provincial_foreign_tax_credit 412.4, not below 0 = 2556.35"
    ) in rendered
    assert (
        "ontario_tax_after_lift_credit: ontario_tax_after_foreign_tax_credit 2556.35 less "
        "lift_credit 0, not below 0 = 2556.35"
    ) in rendered


def test_the_provincial_credit_comes_off_the_ontario_tax_the_total_payable_and_the_refund() -> None:
    # Net federal tax 5779.02 + Ontario tax 3156.35 = 8935.37 against 9000 deducted: a refund of
    # 64.63, which is the net refund as there is no donation to the opportunities fund.
    worksheet = return_aw()

    assert worksheet.get(NET_FEDERAL_TAX).value == D("5779.02")
    assert worksheet.get(TOTAL_PAYABLE).value == D("8935.37")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-64.63")
    assert worksheet.get(REFUND).value == D("64.63")
    assert worksheet.get(ontario.NET_REFUND).value == D("64.63")


def test_the_ontario_credit_lines_are_made_by_the_named_capabilities() -> None:
    worksheet = return_aw()

    assert isinstance(worksheet.producer_of(ontario.TAX_OTHERWISE_PAYABLE_LINE_71), Sum)
    assert isinstance(worksheet.producer_of(ontario.TAX_OTHERWISE_PAYABLE_LINE_73), Sum)
    assert isinstance(
        worksheet.producer_of(ontario.TAX_OTHERWISE_PAYABLE_REDUCTION_BEFORE_CONDITIONS),
        MultipleOver,
    )
    assert isinstance(
        worksheet.producer_of(ontario.TAX_OTHERWISE_PAYABLE_REDUCTION_CLAIMABLE),
        CountByConditions,
    )
    assert isinstance(worksheet.producer_of(ontario.TAX_OTHERWISE_PAYABLE_REDUCTION), TimesCount)
    assert isinstance(worksheet.producer_of(ontario.TAX_OTHERWISE_PAYABLE), SubtractNotBelowZero)
    assert isinstance(
        worksheet.producer_of(ontario.PROVINCIAL_FOREIGN_TAX_CREDIT_BEFORE_LIMIT),
        ProvincialForeignTaxCredit,
    )
    assert isinstance(worksheet.producer_of(ontario.PROVINCIAL_FOREIGN_TAX_CREDIT), LesserOf)
    assert isinstance(
        worksheet.producer_of(ontario.ONTARIO_TAX_AFTER_FOREIGN_TAX_CREDIT), SubtractNotBelowZero
    )
    # Four different subtractions: the tax otherwise payable, line 81 itself, line 83 and line 86.
    assert (
        len(
            {
                id(worksheet.producer_of(kind))
                for kind in (
                    ontario.TAX_OTHERWISE_PAYABLE,
                    ontario.ONTARIO_TAX_AFTER_REDUCTION,
                    ontario.ONTARIO_TAX_AFTER_FOREIGN_TAX_CREDIT,
                    ontario.ONTARIO_TAX_AFTER_LIFT_CREDIT,
                )
            }
        )
        == 4
    )


def test_a_pooled_sheet_of_exactly_200_of_foreign_tax_gives_one_t2036_form() -> None:
    # Two countries paying 50 and 150 are pooled for Form T2209 (one sheet: line 1 200, income
    # 1500, line 3 163.14). Form T2036 has that one sheet too: line 1 200; line 2 163.14; line 3 =
    # 36.86; line 4 = 1500 x 3159.89 / 66990.00 = 70.7543..., half-up 70.75; line 5 =
    # lesser(36.86, 70.75) = 36.86. ON428 line 82 is 36.86 and line 83 = 2968.75 - 36.86 =
    # 2931.89; the Ontario tax is 2931.89 + 600 = 3531.89. T1 line 130 is 6966.62 - 163.14 =
    # 6803.48, so the total payable is 6803.48 + 3531.89 = 10335.37 and the balance owing, with
    # 9000 deducted, is 1335.37.
    worksheet = return_aw(foreign_tax_countries_rows=(("50", "1000"), ("150", "500")))

    assert sheets_of(worksheet) == [(D("200"), D("1500"), D("163.14"))]
    assert t2036_lines(worksheet) == [
        ProvincialForeignTaxCreditLine(
            output=ontario.PROVINCIAL_FOREIGN_TAX_CREDIT_BEFORE_LIMIT,
            position=1,
            tax_paid=D("200"),
            federal_credit=D("163.14"),
            line_3=D("36.86"),
            income=D("1500"),
            net_income=D("66990.00"),
            provincial_tax=D("3159.89"),
            rounding=CENT,
            line_4=D("70.75"),
            result=D("36.86"),
        )
    ]
    assert worksheet.get(ontario.PROVINCIAL_FOREIGN_TAX_CREDIT).value == D("36.86")
    assert worksheet.get(ontario.ONTARIO_TAX_AFTER_FOREIGN_TAX_CREDIT).value == D("2931.89")
    assert worksheet.get(ontario.ONTARIO_TAX).value == D("3531.89")
    assert worksheet.get(NET_FEDERAL_TAX).value == D("6803.48")
    assert worksheet.get(TOTAL_PAYABLE).value == D("10335.37")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("1335.37")


def test_no_countries_give_a_provincial_credit_of_0_and_leave_every_ontario_line_alone() -> None:
    # No sheets: the total of line 5 is 0 (net income is not consulted), ON428 line 82 is 0 and
    # line 83 is line 81, 2968.75 - 0, so the lines after it are what they were without the credit:
    # the Ontario tax is 3568.75. The tax otherwise payable is still worked, 3159.89.
    worksheet = return_aw(foreign_tax_countries_rows=())

    assert sheets_of(worksheet) == []
    assert t2036_lines(worksheet) == []
    totals = [line for line in worksheet.trace if isinstance(line, ItemsTotalLine)]
    assert ItemsTotalLine(ontario.PROVINCIAL_FOREIGN_TAX_CREDIT_BEFORE_LIMIT, (), D("0")) in totals
    assert worksheet.get(ontario.TAX_OTHERWISE_PAYABLE).value == D("3159.89")
    assert worksheet.get(ontario.PROVINCIAL_FOREIGN_TAX_CREDIT_BEFORE_LIMIT).value == D("0")
    assert worksheet.get(ontario.PROVINCIAL_FOREIGN_TAX_CREDIT).value == D("0")
    assert worksheet.get(ontario.ONTARIO_TAX_AFTER_REDUCTION).value == D("2968.75")
    assert worksheet.get(ontario.ONTARIO_TAX_AFTER_FOREIGN_TAX_CREDIT).value == D("2968.75")
    assert worksheet.get(ontario.ONTARIO_TAX_AFTER_LIFT_CREDIT).value == D("2968.75")
    assert worksheet.get(ontario.ONTARIO_TAX_AFTER_FOOD_CREDIT).value == D("2968.75")
    assert worksheet.get(ontario.ONTARIO_HEALTH_PREMIUM).value == D("600.00")
    assert worksheet.get(ontario.ONTARIO_TAX).value == D("3568.75")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("1535.37")


def test_a_return_without_the_list_has_no_provincial_credit_and_keeps_its_ontario_tax() -> None:
    # Return K lists no country: line 83 is line 81, so line 86 starts from line 81 as it did.
    worksheet = return_k()

    assert sheets_of(worksheet) == []
    assert worksheet.get(ontario.PROVINCIAL_FOREIGN_TAX_CREDIT).value == D("0")
    assert (
        worksheet.get(ontario.ONTARIO_TAX_AFTER_FOREIGN_TAX_CREDIT).value
        == worksheet.get(ontario.ONTARIO_TAX_AFTER_REDUCTION).value
    )
    assert worksheet.get(TOTAL_PAYABLE).value == D("6447.70")


def test_the_credit_is_limited_by_the_tax_otherwise_payable_and_line_83_is_not_below_zero() -> None:
    # Two countries, each with 10000 of tax paid on 40000 of net foreign income (total tax over
    # 200, so one sheet each). Form T2209: line 2 = 40000 x 7285.81 / 66990.00 = 4350.3943...,
    # half-up 4350.39, so each sheet's line 3 is 4350.39 and the total, 8700.78, is limited to
    # line 42900, 6966.62, so T1 line 130 is 0. Form T2036 for each sheet: line 3 = 10000 -
    # 4350.39 = 5649.61; line 4 = 40000 x 3159.89 / 66990.00 = 1886.7790..., half-up 1886.78;
    # line 5 = lesser(5649.61, 1886.78) = 1886.78. The total of line 5, 3773.56, "should not be
    # more than" the tax otherwise payable, 3159.89, so ON428 line 82 is 3159.89. Line 83 =
    # 2968.75 - 3159.89 is negative, so 0 (line 81 is lower than the tax otherwise payable by the
    # dividend tax credit): the Ontario tax is 0 + the health premium 600.00 = 600.00. The net
    # federal tax is 0, so the total payable is 600.00 and the refund 9000 - 600.00 = 8400.00.
    worksheet = return_aw(foreign_tax_countries_rows=(("10000", "40000"), ("10000", "40000")))

    assert sheets_of(worksheet) == [
        (D("10000"), D("40000"), D("4350.39")),
        (D("10000"), D("40000"), D("4350.39")),
    ]
    assert [(line.line_3, line.line_4, line.result) for line in t2036_lines(worksheet)] == [
        (D("5649.61"), D("1886.78"), D("1886.78")),
        (D("5649.61"), D("1886.78"), D("1886.78")),
    ]
    assert worksheet.get(ontario.PROVINCIAL_FOREIGN_TAX_CREDIT_BEFORE_LIMIT).value == D("3773.56")
    assert worksheet.get(ontario.TAX_OTHERWISE_PAYABLE).value == D("3159.89")
    assert worksheet.get(ontario.PROVINCIAL_FOREIGN_TAX_CREDIT).value == D("3159.89")
    assert worksheet.get(ontario.ONTARIO_TAX_AFTER_REDUCTION).value == D("2968.75")
    assert worksheet.get(ontario.ONTARIO_TAX_AFTER_FOREIGN_TAX_CREDIT).value == D("0")
    assert worksheet.get(ontario.ONTARIO_TAX_AFTER_LIFT_CREDIT).value == D("0")
    assert worksheet.get(ontario.ONTARIO_TAX).value == D("600.00")
    assert worksheet.get(NET_FEDERAL_TAX).value == D("0")
    assert worksheet.get(TOTAL_PAYABLE).value == D("600.00")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-8400.00")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "provincial_foreign_tax_credit: lesser of provincial_foreign_tax_credit_before_limit "
        "3773.56 and tax_otherwise_payable 3159.89 = 3159.89"
    ) in rendered
    assert (
        "ontario_tax_after_foreign_tax_credit: ontario_tax_after_reduction 2968.75 less "
        "provincial_foreign_tax_credit 3159.89, not below 0 = 0"
    ) in rendered


def test_line_72_and_the_tax_reduction_conditions_do_not_enter_the_tax_otherwise_payable() -> None:
    # A filer with employment income of 24000 and one country (500 of tax on 3000 of income), as
    # in `test_the_tax_reduction_lowers_a_tax_below_twice_the_reduction_amounts`, with an amount on
    # line 72 (additional tax for minimum tax purposes): security options of 200000 (T4 boxes 39
    # and 91) give Form T691 Part 5 line 11 of 7361.00, so Worksheet ON428 line 1 is 24.63% x
    # 7361.00 = 1813.0143, 1813.01, and line 72 is that, as line 3 (1813.01 + 486.80 = 2299.81) is
    # not more than $5,710. Net income is 23795.00 and the basic federal
    # tax 694.07, so the T2209 line 2 is 3000 x 694.07 / 23795.00 = 87.5062..., half-up 87.51,
    # below the 500 paid: the sheet's line 3 is 87.51. ON428 line 69 is 486.80; the tax itself has
    # line 73 = 486.80 + 1813.01 = 2299.81, and "There is an amount on line 72" so line 80 is 0 and
    # line 81 is 2299.81. The tax otherwise payable has "0" on line 72: line 73 = 486.80, the
    # reduction amounts 294.00 twice, 588.00, less line 79 (486.80) is 101.20 (no condition
    # applies), and line 81 = 486.80 - 101.20 = 385.60. Form T2036: line 3 = 500 - 87.51 = 412.49;
    # line 4 = 3000 x 385.60 / 23795.00 = 48.6152..., half-up 48.62; line 5 = lesser(412.49,
    # 48.62) = 48.62, which is less than 385.60, so line 82 is 48.62 and line 83 = 2299.81 - 48.62
    # = 2251.19. The LIFT credit is 875 (5.05% x 24000 = 1212.00, at most 875, no reduction), so
    # line 86 is 2251.19 - 875 = 1376.19 and the Ontario tax is that plus the health premium,
    # 6% x (23795.00 - 20000) = 227.70: 1603.89. As Part 5 line 11 is positive, T2036 line 2 is the
    # special foreign tax credit share: with the 500 on T691 Part 4 line 7 (and no foreign income
    # on its line 2, so line 10 is 0) line 11 is the greater of 87.51 and 0, 87.51; the total
    # foreign tax, 500, is more than $200, so line 2 = 500 / (333.33 / 66.6666% + 0) x 87.51 =
    # 87.5107..., half-up 87.51, the same as the T2209 line 2 above.
    worksheet = compute(
        "24000",
        (),
        "0",
        "0",
        "4320",
        "0",
        "0",
        foreign_tax_countries_rows=(("500", "3000"),),
        amt_t4_security_options_boxes_39_and_91="200000",
        amt_foreign_non_business_tax_paid="500",
    )

    assert worksheet.get(NET_INCOME).value == D("23795.00")
    assert worksheet.get(FOREIGN_TAX_CREDIT_NET_INCOME).value == D("23795.00")
    assert worksheet.get(FOREIGN_TAX_CREDIT_BASIC_FEDERAL_TAX).value == D("694.07")
    assert sheets_of(worksheet) == [(D("500"), D("3000"), D("87.51"))]
    assert worksheet.get(ontario.ONTARIO_TAX_WITH_SURTAX).value == D("486.80")
    assert worksheet.get(AMT_ALTERNATIVE_MINIMUM_TAX_PAYABLE).value == D("7361.00")
    assert worksheet.get(ontario.WORKSHEET_ON428_LINE_1).value == D("1813.01")
    assert worksheet.get(ontario.WORKSHEET_ON428_LINE_3).value == D("2299.81")
    assert worksheet.get(ontario.ONTARIO_MINIMUM_TAX).value == D("1813.01")
    assert worksheet.get(ontario.ONTARIO_TAX_BEFORE_REDUCTION).value == D("2299.81")
    assert worksheet.get(ontario.TAX_REDUCTION_CLAIMABLE).value == 0
    assert worksheet.get(ontario.ONTARIO_TAX_REDUCTION).value == D("0")
    assert worksheet.get(ontario.ONTARIO_TAX_AFTER_REDUCTION).value == D("2299.81")
    assert worksheet.get(ontario.TAX_OTHERWISE_PAYABLE_LINE_73).value == D("486.80")
    assert worksheet.get(ontario.TAX_OTHERWISE_PAYABLE_REDUCTION_BEFORE_CONDITIONS).value == D(
        "101.20"
    )
    assert worksheet.get(ontario.TAX_OTHERWISE_PAYABLE_REDUCTION_CLAIMABLE).value == 1
    assert worksheet.get(ontario.TAX_OTHERWISE_PAYABLE_REDUCTION).value == D("101.20")
    assert worksheet.get(ontario.TAX_OTHERWISE_PAYABLE).value == D("385.60")
    assert [(line.line_3, line.line_4, line.result) for line in t2036_lines(worksheet)] == [
        (D("412.49"), D("48.62"), D("48.62"))
    ]
    assert worksheet.get(ontario.PROVINCIAL_FOREIGN_TAX_CREDIT).value == D("48.62")
    assert worksheet.get(ontario.ONTARIO_TAX_AFTER_FOREIGN_TAX_CREDIT).value == D("2251.19")
    assert worksheet.get(ontario.LIFT_CREDIT).value == D("875")
    assert worksheet.get(ontario.ONTARIO_TAX_AFTER_LIFT_CREDIT).value == D("1376.19")
    assert worksheet.get(ontario.ONTARIO_TAX).value == D("1603.89")


def test_another_condition_on_line_80_zeroes_the_reduction_of_the_tax_otherwise_payable() -> None:
    # The same filer without the 100 on line 72 and not choosing an Ontario tax reduction
    # ("You are choosing not to claim an Ontario tax reduction"): both line 80s are 0, so the tax
    # otherwise payable is line 73, 486.80, itself, and the tax itself is 486.80.
    worksheet = compute(
        "24000",
        (),
        "0",
        "0",
        "4320",
        "0",
        "0",
        foreign_tax_countries_rows=(("500", "3000"),),
        not_claiming_ontario_tax_reduction=1,
    )

    assert worksheet.get(ontario.TAX_OTHERWISE_PAYABLE_REDUCTION_CLAIMABLE).value == 0
    assert worksheet.get(ontario.TAX_OTHERWISE_PAYABLE_REDUCTION).value == D("0")
    assert worksheet.get(ontario.TAX_OTHERWISE_PAYABLE).value == D("486.80")
    assert worksheet.get(ontario.ONTARIO_TAX_AFTER_REDUCTION).value == D("486.80")
    # Line 4 = 3000 x 486.80 / 23795.00 = 61.3742..., half-up 61.37, below the sheet's line 3.
    assert worksheet.get(ontario.PROVINCIAL_FOREIGN_TAX_CREDIT).value == D("61.37")
    assert worksheet.get(ontario.ONTARIO_TAX_AFTER_FOREIGN_TAX_CREDIT).value == D("425.43")
