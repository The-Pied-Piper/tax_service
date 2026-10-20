"""CA-ON 2025 end to end: return o deductions."""

from __future__ import annotations

from app.adapters.inbound.trace_english import EnglishTraceRenderer
from app.jurisdictions.ca.catalog import (
    ALLOWABLE_BUSINESS_INVESTMENT_LOSS,
    CARRYING_CHARGES_INTEREST_EXPENSES_AND_OTHER_EXPENSES,
    DEDUCTIONS_FROM_TOTAL_INCOME,
    FHSA_DEDUCTION,
    NET_INCOME,
    NET_INCOME_BEFORE_ADJUSTMENTS,
    RRSP_DEDUCTION,
    TAXABLE_INCOME,
    TOTAL_INCOME,
    UCCB_AND_RDSP_INCOME_REPAYMENTS,
)
from tests.jurisdictions.ca_on.end_to_end.support import D, compute, step_3


def test_line_23300_adds_every_wired_deduction_once_in_the_forms_line_order() -> None:
    # T1 line 53 and line 23300 "Add lines 35 to 52.": one distinct power of two for each line
    # wired but the child care expenses and the enhanced CPP contributions (0 here, with no child
    # and no employment income), so a line left out or added twice changes the sum: RPP deduction
    # 1 (line 20700), RRSP deduction 2 (line 20800), FHSA deduction 4 (line 20805), split-pension
    # deduction 8 (line 21000), union dues 16 (line 21200), UCCB repayment 32 (line 21300), the
    # allowable business investment loss 64.00 (line 21700, 50% of a loss of 128), the deductible
    # support payments 128 (line 22000), the Federal Worksheet's 100 + 100 + 56 = 256 (line
    # 22100), exploration and development expenses 512 (line 22400) and other deductions 1024
    # (line 23200): 2047. Other income of 5000 is total income, so line 23400 is 2953.
    worksheet = compute(
        "0",
        "0",
        "0",
        "2",
        "2",
        "2",
        "16",
        other_income="5000",
        rpp_deduction="1",
        fhsa_contributions_in_2025="4",
        fhsa_contributions_deducted="4",
        elected_split_pension_deduction="8",
        uccb_repayment="32",
        business_investment_loss="128",
        support_payments_deduction="128",
        total_carrying_charges="100",
        total_interest_expenses="100",
        total_other_expenses="56",
        exploration_and_development_expenses="512",
        other_deductions="1024",
    )

    assert worksheet.get(RRSP_DEDUCTION).value == D("2")
    assert worksheet.get(FHSA_DEDUCTION).value == D("4")
    assert worksheet.get(ALLOWABLE_BUSINESS_INVESTMENT_LOSS).value == D("64.00")
    assert worksheet.get(CARRYING_CHARGES_INTEREST_EXPENSES_AND_OTHER_EXPENSES).value == D("256")
    assert worksheet.get(DEDUCTIONS_FROM_TOTAL_INCOME).value == D("2047")
    assert worksheet.get(NET_INCOME_BEFORE_ADJUSTMENTS).value == D("2953")
    assert worksheet.get(NET_INCOME).value == D("2953")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "deductions_from_total_income: rpp_deduction 1 + rrsp_deduction 2 + fhsa_deduction 4 "
        "+ elected_split_pension_deduction 8 + union_dues 16 + uccb_repayment 32 "
        "+ child_care_expenses 0 + allowable_business_investment_loss 64 "
        "+ support_payments_deduction 128 "
        "+ carrying_charges_interest_expenses_and_other_expenses 256 "
        "+ cpp_enhanced_contributions 0 + exploration_and_development_expenses 512 "
        "+ other_deductions 1024 = 2047"
    ) in rendered


def test_line_23400_is_negative_when_the_deductions_exceed_total_income() -> None:
    # T1 line 54 and line 23400 "Line 34 minus line 53 (if negative, show in brackets)": total
    # income of 1000 less deductions of 2047 (the same lines as above) is -1047. The net income of
    # line 56 (line 23600) "Line 54 minus line 55 (if negative, enter "0")" is 0, as is the
    # taxable income, until line 23500 is wired.
    worksheet = compute(
        "0",
        "0",
        "0",
        "2",
        "2",
        "2",
        "16",
        other_income="1000",
        rpp_deduction="1",
        fhsa_contributions_in_2025="4",
        fhsa_contributions_deducted="4",
        elected_split_pension_deduction="8",
        uccb_repayment="32",
        business_investment_loss="128",
        support_payments_deduction="128",
        total_carrying_charges="100",
        total_interest_expenses="100",
        total_other_expenses="56",
        exploration_and_development_expenses="512",
        other_deductions="1024",
    )

    assert worksheet.get(TOTAL_INCOME).value == D("1000")
    assert worksheet.get(DEDUCTIONS_FROM_TOTAL_INCOME).value == D("2047")
    assert worksheet.get(NET_INCOME_BEFORE_ADJUSTMENTS).value == D("-1047")
    assert worksheet.get(NET_INCOME).value == D("0")
    assert worksheet.get(TAXABLE_INCOME).value == D("0")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "net_income_before_adjustments: total_income 1000 "
        "less deductions_from_total_income 2047 = -1047"
    ) in rendered
    assert (
        "net_income: total_income 1000 less deductions_from_total_income 2047, not below 0 = 0"
    ) in rendered


def test_line_23400_equals_net_income_when_the_deductions_are_below_total_income() -> None:
    worksheet = step_3(other_income="1000", other_deductions="400")

    assert worksheet.get(NET_INCOME_BEFORE_ADJUSTMENTS).value == D("600")
    assert worksheet.get(NET_INCOME).value == D("600")


def test_the_uccb_repayment_is_a_deduction_on_line_21300_and_still_the_worksheets_line_6() -> None:
    # T1 line 40 and line 21300 "Universal child care benefit (UCCB) repayment": the same input
    # the Federal Worksheet's line 6 "Amount from line 21300 of your return" reads. UCCB of 1000
    # (line 11700) and a repayment of 300: total income 1000, line 23300 300, net income 700, and
    # the worksheet's line 8 is 300.
    worksheet = step_3(universal_child_care_benefit="1000", uccb_repayment="300")

    assert worksheet.get(DEDUCTIONS_FROM_TOTAL_INCOME).value == D("300")
    assert worksheet.get(NET_INCOME).value == D("700")
    assert worksheet.get(UCCB_AND_RDSP_INCOME_REPAYMENTS).value == D("300")
