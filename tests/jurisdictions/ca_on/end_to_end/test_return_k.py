"""CA-ON 2025 end to end: return k."""

from __future__ import annotations

from app.adapters.inbound.trace_english import EnglishTraceRenderer
from app.jurisdictions.ca.catalog import (
    CREDITS_AGAINST_BASIC_FEDERAL_TAX,
    DEDUCTIONS_FROM_NET_INCOME,
    DEDUCTIONS_FROM_TOTAL_INCOME,
    DIVIDEND_TAX_CREDIT,
    DIVIDENDS_AMOUNT_A,
    DIVIDENDS_AMOUNT_A_LESS_B,
    DIVIDENDS_AMOUNT_B,
    DIVIDENDS_WITHOUT_A_SLIP_GROSSED_UP,
    ELIGIBLE_DIVIDENDS_CREDIT,
    ELIGIBLE_DIVIDENDS_GROSSED_UP,
    FEDERAL_BASIC_TAX,
    FEDERAL_TAX_AFTER_CREDITS,
    INCOME_SUPPORT_BENEFITS,
    NET_CAPITAL_LOSSES_OF_OTHER_YEARS,
    NET_FEDERAL_TAX,
    NET_INCOME,
    NET_INCOME_LESS_UCCB_AND_RDSP_INCOME,
    NO_SLIP_DIVIDEND_TAX_CREDIT,
    NON_REFUNDABLE_TAX_CREDITS,
    OTHER_DIVIDENDS_CREDIT,
    OTHER_DIVIDENDS_GROSSED_UP,
    OTHER_PAYMENTS_DEDUCTION,
    OTHER_PAYMENTS_DEDUCTION_AFTER_LIMIT,
    OTHER_PAYMENTS_LIMIT_INCOME,
    REFUND_OR_BALANCE_OWING,
    SLIP_DIVIDEND_TAX_CREDIT,
    SLIP_TAXABLE_DIVIDENDS,
    SLIP_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
    TAXABLE_CAPITAL_GAINS,
    TAXABLE_DIVIDENDS,
    TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
    TAXABLE_INCOME,
    TOTAL_INCOME,
    TOTAL_PAYABLE,
    UCCB_AND_RDSP_INCOME,
    UCCB_AND_RDSP_INCOME_REPAYMENTS,
)
from app.jurisdictions.ca_on import catalog as ontario
from tests.jurisdictions.ca_on.end_to_end.support import D, compute, return_k


def test_return_ks_taxable_dividends_are_the_federal_worksheets_lines_12000_and_12010() -> None:
    # The Federal Worksheet for lines 12000 and 12010: a T5 slip with box 11 of 200 (line 3) and
    # boxes 11 and 25 of 500 (line 8), so lines 5 and 10; no information slip for eligible
    # dividends of 1000 (line 11) and dividends other than eligible of 500 (line 14): line 13 is
    # 1000 x 138% = 1380.00, line 16 is 500 x 115% = 575.00 and line 17 is 1955.00. Line 12010 is
    # line 5 plus line 16, 775.00, and line 12000 is line 10 plus line 17, 2455.00.
    worksheet = return_k()

    assert worksheet.get(SLIP_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE).value == D("200")
    assert worksheet.get(SLIP_TAXABLE_DIVIDENDS).value == D("500")
    assert worksheet.get(ELIGIBLE_DIVIDENDS_GROSSED_UP).value == D("1380.00")
    assert worksheet.get(OTHER_DIVIDENDS_GROSSED_UP).value == D("575.00")
    assert worksheet.get(DIVIDENDS_WITHOUT_A_SLIP_GROSSED_UP).value == D("1955.00")
    assert worksheet.get(TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE).value == D("775.00")
    assert worksheet.get(TAXABLE_DIVIDENDS).value == D("2455.00")
    assert worksheet.get(TOTAL_INCOME).value == D("52455.00")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    for line in (
        "slip_taxable_dividends_other_than_eligible: t3_taxable_dividends_other_than_eligible 0 "
        "+ t4ps_taxable_dividends_other_than_eligible 0 "
        "+ t5_taxable_dividends_other_than_eligible 200 "
        "+ t5013_taxable_dividends_other_than_eligible 0 = 200",
        "slip_taxable_dividends: t3_taxable_dividends 0 + t4ps_taxable_dividends 0 "
        "+ t5_taxable_dividends 500 + t5013_taxable_dividends 0 = 500",
        "eligible_dividends_grossed_up: 138/100 of eligible_dividends_received_without_a_slip "
        "1000 (half-up to 0.01)",
        "other_dividends_grossed_up: 115/100 of other_dividends_received_without_a_slip 500 "
        "(half-up to 0.01)",
        "dividends_without_a_slip_grossed_up: eligible_dividends_grossed_up 1380 "
        "+ other_dividends_grossed_up 575 = 1955",
        "taxable_dividends_other_than_eligible: slip_taxable_dividends_other_than_eligible 200 "
        "+ other_dividends_grossed_up 575 = 775",
        "taxable_dividends: slip_taxable_dividends 500 "
        "+ dividends_without_a_slip_grossed_up 1955 = 2455",
    ):
        assert line in rendered, line


def test_return_ks_federal_dividend_tax_credit_counts_the_no_slip_dividends_only() -> None:
    # The Federal Worksheet's "Line 40425": line 5 is the slip credit, 60.00 (T5 boxes 12 and
    # 26). Note 1 "Enter only the amount of dividends that were not shown on an information
    # slip." makes line A the worksheet's line 17, 1955.00, not the 2455.00 of line 12000, and
    # line B its line 16, 575.00, not the 775.00 of line 12010. Line 6 is 575.00 x 9.0301% =
    # 51.92, line C is 1955.00 - 575.00 = 1380.00, line 7 is 1380.00 x 15.0198% = 207.27, line
    # 8 is 259.19 and line 9, and so line 40425, is 60.00 + 259.19 = 319.19.
    worksheet = return_k()

    assert worksheet.get(SLIP_DIVIDEND_TAX_CREDIT).value == D("60.00")
    assert worksheet.get(DIVIDENDS_AMOUNT_A).value == D("1955.00")
    assert worksheet.get(DIVIDENDS_AMOUNT_B).value == D("575.00")
    assert worksheet.get(OTHER_DIVIDENDS_CREDIT).value == D("51.92")
    assert worksheet.get(DIVIDENDS_AMOUNT_A_LESS_B).value == D("1380.00")
    assert worksheet.get(ELIGIBLE_DIVIDENDS_CREDIT).value == D("207.27")
    assert worksheet.get(NO_SLIP_DIVIDEND_TAX_CREDIT).value == D("259.19")
    assert worksheet.get(DIVIDEND_TAX_CREDIT).value == D("319.19")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    for line in (
        "slip_dividend_tax_credit: t3_dividend_tax_credit 0 + t4ps_dividend_tax_credit 0 "
        "+ t5_dividend_tax_credit 60 + t5013_dividend_tax_credit 0 = 60",
        "dividends_amount_a: dividends_without_a_slip_grossed_up 1955 = 1955",
        "dividends_amount_b: other_dividends_grossed_up 575 = 575",
        "other_dividends_credit: 9.0301% of dividends_amount_b 575 (half-up to 0.01)",
        "dividends_amount_a_less_b: dividends_amount_a 1955 less dividends_amount_b 575 = 1380",
        "eligible_dividends_credit: 15.0198% of dividends_amount_a_less_b 1380 (half-up to 0.01)",
        "no_slip_dividend_tax_credit: other_dividends_credit 51.92 "
        "+ eligible_dividends_credit 207.27 = 259.19",
        "dividend_tax_credit: slip_dividend_tax_credit 60 + no_slip_dividend_tax_credit 259.19 "
        "= 319.19",
    ):
        assert line in rendered, line


def test_the_dividend_tax_credit_comes_off_the_basic_federal_tax_with_the_other_credits() -> None:
    # T1 line 125 "Add lines 122 to 124.": line 122 (35000) 3004.65 and line 123 (40425)
    # 319.19, 3323.84; line 126 "Line 121 minus line 125 (if negative, enter "0")" is
    # 7538.55 - 3323.84 = 4214.71, the federal tax after credits carried to the net federal tax.
    worksheet = return_k()

    assert worksheet.get(NON_REFUNDABLE_TAX_CREDITS).value == D("3004.65")
    assert worksheet.get(CREDITS_AGAINST_BASIC_FEDERAL_TAX).value == D("3323.84")
    assert worksheet.get(FEDERAL_BASIC_TAX).value == D("7538.55")
    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("4214.71")
    assert worksheet.get(NET_FEDERAL_TAX).value == D("4214.71")
    assert worksheet.get(ontario.ONTARIO_TAX).value == D("2232.99")
    assert worksheet.get(TOTAL_PAYABLE).value == D("6447.70")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-2552.30")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "credits_against_basic_federal_tax: non_refundable_tax_credits 3004.65 "
        "+ dividend_tax_credit 319.19 = 3323.84"
    ) in rendered
    assert (
        "federal_tax_after_credits: federal_basic_tax 7538.55 "
        "less credits_against_basic_federal_tax 3323.84, not below 0 = 4214.71"
    ) in rendered


def test_slip_credits_of_100_and_no_other_dividends_give_line_40425_of_100() -> None:
    # Line 5 of the credit chart is 100.00 and nothing is on line A or B: "Otherwise, enter the
    # amount from line 5 on line 40425 of your return."
    worksheet = compute("50000", "0", "0", "0", "0", "0", "0", t5_dividend_tax_credit="100.00")

    assert worksheet.get(SLIP_DIVIDEND_TAX_CREDIT).value == D("100.00")
    assert worksheet.get(OTHER_DIVIDENDS_CREDIT).value == D("0")
    assert worksheet.get(ELIGIBLE_DIVIDENDS_CREDIT).value == D("0")
    assert worksheet.get(NO_SLIP_DIVIDEND_TAX_CREDIT).value == D("0")
    assert worksheet.get(DIVIDEND_TAX_CREDIT).value == D("100.00")
    assert worksheet.get(TAXABLE_DIVIDENDS).value == D("0")
    assert worksheet.get(CREDITS_AGAINST_BASIC_FEDERAL_TAX).value == (
        worksheet.get(NON_REFUNDABLE_TAX_CREDITS).value + D("100.00")
    )


def test_dividends_on_slips_alone_are_not_grossed_up_and_leave_lines_a_and_b_at_zero() -> None:
    # Slip amounts of 800 (T5 boxes 11 and 25) and 300 (box 11) are lines 12000 and 12010 as
    # they stand, and the slip credit of 70.00 is line 40425: with nothing received without a
    # slip, lines A and B and the credits computed from them are 0.
    worksheet = compute(
        "50000",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        t5_taxable_dividends_other_than_eligible="300",
        t5_taxable_dividends="800",
        t5_dividend_tax_credit="70.00",
    )

    assert worksheet.get(TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE).value == D("300")
    assert worksheet.get(TAXABLE_DIVIDENDS).value == D("800")
    assert worksheet.get(DIVIDENDS_AMOUNT_A).value == D("0")
    assert worksheet.get(DIVIDENDS_AMOUNT_B).value == D("0")
    assert worksheet.get(NO_SLIP_DIVIDEND_TAX_CREDIT).value == D("0")
    assert worksheet.get(DIVIDEND_TAX_CREDIT).value == D("70.00")
    assert worksheet.get(TOTAL_INCOME).value == D("50800")


def test_each_slip_box_adds_to_its_worksheet_line_once() -> None:
    # Distinct powers of two, one per slip line, so a line left out or added twice changes the
    # sum: lines 1 to 4 (T3, T4PS, T5, T5013) 1 + 2 + 4 + 8 = 15, lines 6 to 9 16 + 32 + 64 +
    # 128 = 240, and credit lines 1 to 4 256 + 512 + 1024 + 2048 = 3840.
    worksheet = compute(
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        t3_taxable_dividends_other_than_eligible="1",
        t4ps_taxable_dividends_other_than_eligible="2",
        t5_taxable_dividends_other_than_eligible="4",
        t5013_taxable_dividends_other_than_eligible="8",
        t3_taxable_dividends="16",
        t4ps_taxable_dividends="32",
        t5_taxable_dividends="64",
        t5013_taxable_dividends="128",
        t3_dividend_tax_credit="256",
        t4ps_dividend_tax_credit="512",
        t5_dividend_tax_credit="1024",
        t5013_dividend_tax_credit="2048",
    )

    assert worksheet.get(SLIP_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE).value == D("15")
    assert worksheet.get(SLIP_TAXABLE_DIVIDENDS).value == D("240")
    assert worksheet.get(SLIP_DIVIDEND_TAX_CREDIT).value == D("3840")
    assert worksheet.get(DIVIDEND_TAX_CREDIT).value == D("3840")


def test_a_dividend_credit_above_the_basic_tax_leaves_zero_federal_tax_not_a_refund() -> None:
    # Low income, so a small basic tax: the credits against it (35000 and 40425) are more, and
    # the unused part is lost, as line 126 is "if negative, enter "0"".
    worksheet = compute("10000", "0", "0", "0", "0", "0", "0", t5_dividend_tax_credit="5000")

    assert (
        worksheet.get(CREDITS_AGAINST_BASIC_FEDERAL_TAX).value
        > worksheet.get(FEDERAL_BASIC_TAX).value
    )
    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("0")


def test_the_other_payments_deduction_is_line_14700_when_nothing_was_entered_on_line_14600() -> (
    None
):
    # T1 line 60 and line 25000 "enter the amount from line 14700 if you did not enter an amount on
    # line 14600": workers' compensation 2000 (line 14400) and social assistance 300 (line 14500)
    # make line 14700 2300, and with no amount on line 14600 (count 0) that is line 25000, whatever
    # the chart amount of 999 and the count of 1 for a line 9 over the limit, which only the
    # worksheet reads. Employment income 30000: enhanced CPP contributions 1% x (30000 - 3500) =
    # 265.00, total income 30000 + 2300 = 32300, net income 32035.00, taxable income
    # 32035.00 - 2300 = 29735.00.
    worksheet = compute(
        "30000",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        workers_compensation_benefits="2000",
        social_assistance_payments="300",
        other_payments_deduction_above_limit="999",
        other_payments_worksheet_line_9_over_limit=1,
    )

    assert worksheet.get(INCOME_SUPPORT_BENEFITS).value == D("2300")
    assert worksheet.get(OTHER_PAYMENTS_DEDUCTION_AFTER_LIMIT).value == D("999")
    assert worksheet.get(OTHER_PAYMENTS_DEDUCTION).value == D("2300")
    assert worksheet.get(DEDUCTIONS_FROM_NET_INCOME).value == D("2300")
    assert worksheet.get(NET_INCOME).value == D("32035.00")
    assert worksheet.get(TAXABLE_INCOME).value == D("29735.00")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "other_payments_deduction: income_support_benefits 2300, "
        "chosen as other_payments_worksheet_required is 0"
    ) in rendered


def test_the_worksheets_lines_4_5_8_and_9_with_supplements_uccb_rdsp_income_and_repayments() -> (
    None
):
    # Federal Worksheet "Line 25000 - Other payments deduction" for a filer with net federal
    # supplements of 400 on line 14600 (count 1). Employment income 50000, UCCB 1000 (line
    # 11700), RDSP income 3000 (line 12500): total income 50000 + 1000 + 3000 + 400 = 54400,
    # enhanced CPP contributions 1% x (50000 - 3500) = 465.00. Line 6 (UCCB repayment) 200 is
    # also T1 line 21300, and line 7 (RDSP income repayment) 100 is "included in the amount on
    # line 23200 of your return", so line 23200 is 100: total deductions are 200 + 100 + 465.00 =
    # 765.00, so net income (line 1) is 54400 - 765.00 = 53635.00. Line 4 is 1000 + 3000 = 4000;
    # line 5 is 53635.00 - 4000 = 49635.00; lines 6 and 7 make line 8 300; line 9 is 49635.00 +
    # 300 = 49935.00, not more than $93,454 (count 0), so line 25000 is line 14700, 400, and
    # taxable income is 53635.00 - 400 = 53235.00.
    worksheet = compute(
        "50000",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        universal_child_care_benefit="1000",
        rdsp_income="3000",
        net_federal_supplements="400",
        uccb_repayment="200",
        rdsp_income_repayment="100",
        other_deductions="100",
        other_payments_worksheet_required=1,
    )

    assert worksheet.get(DEDUCTIONS_FROM_TOTAL_INCOME).value == D("765.00")
    assert worksheet.get(NET_INCOME).value == D("53635.00")
    assert worksheet.get(UCCB_AND_RDSP_INCOME).value == D("4000")
    assert worksheet.get(NET_INCOME_LESS_UCCB_AND_RDSP_INCOME).value == D("49635.00")
    assert worksheet.get(UCCB_AND_RDSP_INCOME_REPAYMENTS).value == D("300")
    assert worksheet.get(OTHER_PAYMENTS_LIMIT_INCOME).value == D("49935.00")
    assert worksheet.get(OTHER_PAYMENTS_DEDUCTION_AFTER_LIMIT).value == D("400")
    assert worksheet.get(OTHER_PAYMENTS_DEDUCTION).value == D("400")
    assert worksheet.get(TAXABLE_INCOME).value == D("53235.00")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert "uccb_and_rdsp_income: universal_child_care_benefit 1000 + rdsp_income 3000 = 4000" in (
        rendered
    )
    assert (
        "net_income_less_uccb_and_rdsp_income: net_income 53635 less uccb_and_rdsp_income 4000 "
        "= 49635"
    ) in rendered
    assert (
        "uccb_and_rdsp_income_repayments: uccb_repayment 200 + rdsp_income_repayment 100 = 300"
    ) in rendered
    assert (
        "other_payments_limit_income: net_income_less_uccb_and_rdsp_income 49635 "
        "+ uccb_and_rdsp_income_repayments 300 = 49935"
    ) in rendered
    assert (
        "other_payments_deduction_after_limit: income_support_benefits 400, "
        "chosen as other_payments_worksheet_line_9_over_limit is 0"
    ) in rendered
    assert (
        "other_payments_deduction: other_payments_deduction_after_limit 400, "
        "chosen as other_payments_worksheet_required is 1"
    ) in rendered


def test_a_line_9_over_93454_takes_the_charts_amount_as_line_25000() -> None:
    # "If the amount on line 9 is more than $93,454, go to canada.ca/line-25000 to find out how
    # much you can deduct": employment income 100000, workers' compensation 1500 and net federal
    # supplements 500 (line 14700 is 2000), total income 102000, enhanced CPP contributions
    # 678.00 + 396.00 = 1074.00, net income 100926.00; with no UCCB, RDSP income or repayments
    # line 9 is 100926.00, over the limit (count 1), so line 25000 is the chart's amount, a
    # chosen 700, not line 14700, and taxable income is 100926.00 - 700 = 100226.00.
    worksheet = compute(
        "100000",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        workers_compensation_benefits="1500",
        net_federal_supplements="500",
        other_payments_deduction_above_limit="700",
        other_payments_worksheet_required=1,
        other_payments_worksheet_line_9_over_limit=1,
    )

    assert worksheet.get(INCOME_SUPPORT_BENEFITS).value == D("2000")
    assert worksheet.get(NET_INCOME).value == D("100926.00")
    assert worksheet.get(OTHER_PAYMENTS_LIMIT_INCOME).value == D("100926.00")
    assert worksheet.get(OTHER_PAYMENTS_DEDUCTION_AFTER_LIMIT).value == D("700")
    assert worksheet.get(OTHER_PAYMENTS_DEDUCTION).value == D("700")
    assert worksheet.get(TAXABLE_INCOME).value == D("100226.00")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "other_payments_deduction_after_limit: other_payments_deduction_above_limit 700, "
        "chosen as other_payments_worksheet_line_9_over_limit is 1"
    ) in rendered
    assert (
        "other_payments_deduction: other_payments_deduction_after_limit 700, "
        "chosen as other_payments_worksheet_required is 1"
    ) in rendered


def test_line_9_may_be_negative_as_the_form_prints_no_floor() -> None:
    # Net income 0 (UCCB of 1000 less union dues of 1500, not below zero) less line 4 (1000) is
    # line 5, -1000, with no repayments line 9 is -1000, not over the limit, so with an amount on
    # line 14600 of 0 entered as such (count 1) line 25000 is line 14700, 0.
    worksheet = compute(
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        "1500",
        universal_child_care_benefit="1000",
        other_payments_worksheet_required=1,
    )

    assert worksheet.get(NET_INCOME).value == D("0")
    assert worksheet.get(NET_INCOME_LESS_UCCB_AND_RDSP_INCOME).value == D("-1000")
    assert worksheet.get(OTHER_PAYMENTS_LIMIT_INCOME).value == D("-1000")
    assert worksheet.get(OTHER_PAYMENTS_DEDUCTION).value == D("0")


def test_deductions_from_net_income_add_lines_58_to_63_and_67_once_each() -> None:
    # T1 line 68 and line 25700 "Add lines 58 to 67.": one distinct power of two for each of the
    # seven lines wired: line 24400 1, line 24900 2, line 25000 4 (workers' compensation of 4, so
    # line 14700, with no amount on line 14600), line 25100 8, line 25200 16, line 25300 32 (a
    # capital gain of 64, taxable capital gains of 32.00, and unapplied net capital losses of 32
    # claimed whole) and line 25600 64, so a line left out or added twice changes the sum: 127.
    # Other income 1000 and workers' compensation 4 and taxable capital gains 32.00 give total
    # income 1036.00 and taxable income 1036.00 - 127 = 909.00.
    worksheet = compute(
        "0",
        "64",
        "0",
        "0",
        "0",
        "0",
        "0",
        other_income="1000",
        workers_compensation_benefits="4",
        canadian_armed_forces_and_police_deduction="1",
        security_options_deductions="2",
        limited_partnership_losses_of_other_years="8",
        non_capital_losses_of_other_years="16",
        unapplied_net_capital_losses_2001_to_2024="32",
        net_capital_losses_claimed="32",
        additional_deductions="64",
    )

    assert worksheet.get(TAXABLE_CAPITAL_GAINS).value == D("32.00")
    assert worksheet.get(OTHER_PAYMENTS_DEDUCTION).value == D("4")
    assert worksheet.get(NET_CAPITAL_LOSSES_OF_OTHER_YEARS).value == D("32")
    assert worksheet.get(DEDUCTIONS_FROM_NET_INCOME).value == D("127")
    assert worksheet.get(TAXABLE_INCOME).value == D("909.00")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "deductions_from_net_income: canadian_armed_forces_and_police_deduction 1 "
        "+ security_options_deductions 2 + other_payments_deduction 4 "
        "+ limited_partnership_losses_of_other_years 8 + non_capital_losses_of_other_years 16 "
        "+ net_capital_losses_of_other_years 32 + additional_deductions 64 = 127"
    ) in rendered


def test_return_ls_deductions_from_net_income_are_8500_and_its_taxable_income_34500() -> None:
    # Return L: employment income 40000 and other income 1365 (line 13000), both chosen, and
    # workers' compensation 2000 (line 14400): total income 43365; enhanced CPP contributions
    # 1% x (40000 - 3500) = 365.00; net income 43000.00. Line 25000 is line 14700, 2000.00;
    # security options deduction 1500 (line 24900) and non-capital losses of other years 5000
    # (line 25200): line 25700 is 1500 + 2000 + 5000 = 8500, taxable income 43000.00 - 8500 =
    # 34500.00.
    worksheet = compute(
        "40000",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        other_income="1365",
        workers_compensation_benefits="2000",
        security_options_deductions="1500",
        non_capital_losses_of_other_years="5000",
    )

    assert worksheet.get(TOTAL_INCOME).value == D("43365")
    assert worksheet.get(NET_INCOME).value == D("43000.00")
    assert worksheet.get(OTHER_PAYMENTS_DEDUCTION).value == D("2000")
    assert worksheet.get(DEDUCTIONS_FROM_NET_INCOME).value == D("8500")
    assert worksheet.get(TAXABLE_INCOME).value == D("34500.00")
