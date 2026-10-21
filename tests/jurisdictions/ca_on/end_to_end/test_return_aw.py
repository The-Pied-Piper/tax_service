"""CA-ON 2025 end to end: return aw."""

from __future__ import annotations

from typing import Any

from app.adapters.inbound.trace_english import EnglishTraceRenderer
from app.domain.trace import ItemsTotalLine, SubtractedLine, SumLine
from app.domain.worksheet import Worksheet
from app.jurisdictions.ca.catalog import (
    BASIC_FEDERAL_TAX_WITH_DIVIDEND_CREDIT,
    DIVIDEND_TAX_CREDIT,
    FEDERAL_FOREIGN_TAX_CREDIT,
    FEDERAL_NON_BUSINESS_FOREIGN_TAX_CREDIT,
    FEDERAL_TAX_AFTER_CREDITS,
    FEDERAL_TAX_LESS_CREDITS,
    FEDERAL_TAX_LESS_FOREIGN_TAX_CREDIT,
    FEDERAL_TAX_WITH_ITC_RECAPTURE,
    FOREIGN_TAX_CREDIT_BASIC_FEDERAL_TAX,
    FOREIGN_TAX_CREDIT_NET_INCOME,
    FOREIGN_TAX_CREDIT_NET_INCOME_BEFORE_SPLIT_INCOME,
    FOREIGN_TAX_CREDIT_NET_INCOME_DEDUCTIONS,
    FOREIGN_TAX_CREDIT_NET_INCOME_WITH_SPLIT_INCOME,
    NET_FEDERAL_TAX,
    NET_INCOME,
    NET_INCOME_BEFORE_ADJUSTMENTS,
    REFUND_OR_BALANCE_OWING,
    SOCIAL_BENEFITS_REPAYMENT,
    TAXABLE_INCOME,
    TOSI_ADJUSTED_NET_INCOME,
    TOTAL_INCOME,
    TOTAL_PAYABLE,
    TOTAL_SPLIT_INCOME,
)
from app.jurisdictions.ca.trace import ForeignTaxCreditLine, PooledForeignTaxCreditLine
from app.jurisdictions.ca_on import catalog as ontario
from tests.jurisdictions.ca_on.end_to_end.support import CENT, D, compute, return_k

US = ("1500", "10000")
UK = ("100", "5000")


def return_aw(**overrides: Any) -> Worksheet:
    """Return AW's inputs, as in `returns/2025_return_aw.yaml`.

    The filer is Return K's: employment income of 50000, a T5 slip and dividends with no slip, and
    income tax deducted of 9000. Added are foreign investment income of 15000 (the dividends of two
    countries) and the two countries of Form T2209: the United States, 1500 of tax paid on 10000
    of net foreign non-business income, and the United Kingdom, 100 on 5000.
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
        "federal_foreign_tax_credit: lesser of federal_non_business_foreign_tax_credit 1187.6 "
        "and federal_tax_after_credits 6966.62 = 1187.6"
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
        "federal_tax_less_foreign_tax_credit: federal_tax_after_credits 6966.62 "
        "less federal_foreign_tax_credit 1187.6, not below 0 = 5779.02"
    ) in rendered
    assert (
        "federal_tax_with_itc_recapture: federal_tax_less_foreign_tax_credit 5779.02 "
        "+ itc_recapture 0 = 5779.02"
    ) in rendered


def test_the_credit_comes_off_the_net_federal_tax_the_total_payable_and_the_balance_owing() -> None:
    # Line 130 is 5779.02, and lines 132, 134 and 139 carry it (no recapture, no logging tax
    # credit, no credit against federal tax), so the net federal tax (line 142) is 5779.02. The
    # Ontario tax (line 147) is 3568.75 (see the return file), so the total payable (line 148) is
    # 5779.02 + 3568.75 = 9347.77 and, with 9000 of tax deducted, the balance owing is 347.77.
    worksheet = return_aw()

    assert worksheet.get(FEDERAL_TAX_LESS_CREDITS).value == D("5779.02")
    assert worksheet.get(NET_FEDERAL_TAX).value == D("5779.02")
    assert worksheet.get(ontario.ONTARIO_TAX).value == D("3568.75")
    assert worksheet.get(TOTAL_PAYABLE).value == D("9347.77")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("347.77")


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
            threshold=D("200"),
            rounding=CENT,
            line_2=D("163.14"),
            result=D("163.14"),
        )
    ]
    assert not [line for line in worksheet.trace if isinstance(line, ForeignTaxCreditLine)]
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "federal_non_business_foreign_tax_credit: all 2 countries pooled, total tax paid 200 "
        "is not more than 200: 1500 net foreign income x 7285.81 basic federal tax / 66990 "
        "net income = 163.14 (half-up to 0.01); credit 163.14"
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
    # 6966.62 - 6966.62 = 0, so the net federal tax is 0 and the total payable is the Ontario tax,
    # 3568.75, with a refund of 9000 - 3568.75 = 5431.25.
    worksheet = return_aw(foreign_tax_countries_rows=(("8000", "100000"),))

    assert worksheet.get(FEDERAL_NON_BUSINESS_FOREIGN_TAX_CREDIT).value == D("7285.81")
    assert worksheet.get(FEDERAL_FOREIGN_TAX_CREDIT).value == D("6966.62")
    assert worksheet.get(FEDERAL_TAX_LESS_FOREIGN_TAX_CREDIT).value == D("0")
    assert worksheet.get(NET_FEDERAL_TAX).value == D("0")
    assert worksheet.get(TOTAL_PAYABLE).value == D("3568.75")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-5431.25")


def test_the_deductions_of_note_3_come_off_net_income_in_the_basic_federal_tax_ratio() -> None:
    # Income: 67455.00 + 800 of workers' compensation (line 14400) = 68255.00, less the 465.00
    # of enhanced CPP contributions: net income 67790.00. Note (3) subtracts: line 24400 1000,
    # line 24900 500, line 25000 800 (the other payments deduction, line 14700), line 25300 0,
    # line 25395 300, line 25400 700 and the 200 of line 25600 that is exempt income: 3500, so
    # its net income is 67790.00 - 3500 = 64290.00. Lines 24400, 24900, 25000 and 25600 (200
    # entered as additional deductions) come off for taxable income, 67790.00 - 2500 = 65290.00;
    # lines 25395 and 25400 are not wired there. The federal tax on it is 8319.38 + (65290.00 -
    # 57375.00) x 20.5% = 8319.38 + 1622.575 = 9941.955, half-up 9941.96; less 3323.84, line
    # 42900 is 6618.12 and the basic federal tax is 6618.12 + 319.19 = 6937.31. United States:
    # line 2 = 10000 x 6937.31 / 64290.00 = 1079.0651..., half-up 1079.07, below 1500; United
    # Kingdom: 5000 x 6937.31 / 64290.00 = 539.5325..., half-up 539.53, above 100. The credit is
    # 1079.07 + 100 = 1179.07.
    worksheet = return_aw(
        workers_compensation_benefits="800",
        canadian_armed_forces_and_police_deduction="1000",
        security_options_deductions="500",
        qualifying_transfer_capital_gains_deduction="300",
        capital_gains_deduction="700",
        additional_deductions="200",
        exempt_income_deductions="200",
    )

    assert worksheet.get(NET_INCOME).value == D("67790.00")
    assert worksheet.get(TAXABLE_INCOME).value == D("65290.00")
    assert worksheet.get(FOREIGN_TAX_CREDIT_NET_INCOME_DEDUCTIONS).value == D("3500.00")
    assert worksheet.get(FOREIGN_TAX_CREDIT_NET_INCOME).value == D("64290.00")
    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("6618.12")
    assert worksheet.get(FOREIGN_TAX_CREDIT_BASIC_FEDERAL_TAX).value == D("6937.31")
    assert worksheet.get(FEDERAL_NON_BUSINESS_FOREIGN_TAX_CREDIT).value == D("1179.07")
    assert worksheet.get(FEDERAL_TAX_LESS_FOREIGN_TAX_CREDIT).value == D("5439.05")


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


def test_note_3_net_income_takes_line_23500_off_line_23400_but_not_off_the_split_income() -> None:
    # Return AS's filer, employment income of 92074 and old age security of 9000 (line 11300), with
    # no dividends or foreign income and no tax deducted. Total income is 92074 + 9000 = 101074; the
    # enhanced CPP contributions (678.00 + 396.00 = 1074.00) come off it, so line 23400 is
    # 100000.00. The social benefits repayment (line 23500) is 15% x (100000.00 - 93343.00) =
    # 998.55, so line 23600 is 99001.45 and note (3) starts from it: 100000.00 - 998.55 =
    # 99001.45, plus a line 68360 of 0 and less deductions of 0, so net income is 99001.45. The
    # TOSI-adjusted net income is 0 + 100000.00 = 100000.00, which line 23500 is not taken off, so
    # it is not note (3)'s starting point: the ratio would then be 100000.00, not 99001.45.
    # Taxable income is 99001.45: the federal tax is 8319.38 + (99001.45 - 57375) x 20.5% =
    # 8319.38 + 8533.42225, 16852.80; the credits are (16129 + 3356.10 + 1077.48 + 1471) x 14.5% =
    # 22033.58 x 14.5% = 3194.87, so line 42900 is 13657.93, the basic federal tax (note 4) with no
    # dividend credit or abatement. Line 2 for the one country is 10000 x 13657.93 / 99001.45 =
    # 1379.5712, 1379.57, below its 1500 paid: line 3 and line 13 (40500) are 1379.57, and T1
    # line 130 is 13657.93 - 1379.57 = 12278.36. The total payable is 12278.36 + 998.55 (line
    # 42200) + 6835.22 (the Ontario tax, as Return AS) = 20112.13; nothing was deducted at source.
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
    assert worksheet.get(TOSI_ADJUSTED_NET_INCOME).value == D("100000.00")
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
    assert worksheet.get(TOTAL_PAYABLE).value == D("20112.13")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("20112.13")
