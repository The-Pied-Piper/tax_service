"""CA-ON 2025 end to end: return h."""

from __future__ import annotations

from app.adapters.inbound.trace_english import EnglishTraceRenderer
from app.jurisdictions.ca.catalog import (
    CANADA_WORKERS_BENEFIT,
    CPP_ENHANCED_CONTRIBUTIONS,
    DEDUCTIONS_FROM_NET_INCOME,
    FEDERAL_BASIC_TAX,
    FEDERAL_TAX_AFTER_CREDITS,
    INCOME_SUPPORT_BENEFITS,
    INTEREST_AND_OTHER_INVESTMENT_INCOME,
    INVESTMENT_INCOME_BEFORE_PRIOR_YEARS,
    NET_INCOME,
    NON_REFUNDABLE_TAX_CREDITS,
    OTHER_PAYMENTS_DEDUCTION,
    REFUND_OR_BALANCE_OWING,
    TAXABLE_INCOME,
    TOTAL_INCOME,
    TOTAL_PAYABLE,
    WORKING_INCOME,
)
from app.jurisdictions.ca_on import catalog as ontario
from app.jurisdictions.ca_on.catalog import (
    LIFT_CREDIT,
    LIFT_REDUCTION,
    ONTARIO_BASIC_TAX,
    ONTARIO_HEALTH_PREMIUM,
    ONTARIO_TAX,
    ONTARIO_TAX_AFTER_CREDITS,
)
from tests.jurisdictions.ca_on.end_to_end.support import D, compute_with_schedule_8


def test_return_hs_pension_and_benefit_income_is_all_of_its_total_income() -> None:
    # Return H, a retiree: OAS 8000 (line 11300), CPP benefits 9000 (11400), other pensions
    # 20000 (11500), RRSP income 5000 (12900) and workers' compensation 2000 (14400, so line
    # 14700); interest from the Federal Worksheet: T5 slips 1200 (line 2) plus bank interest with
    # no slip 300 (line 7) is 1500 (line 9), less 100 reported in previous years (line 10): 1400
    # (line 12100). Total income 8000 + 9000 + 20000 + 1400 + 5000 + 2000 = 45400, with no
    # employment income, so no CPP contributions, EI premiums, Canada employment amount, LIFT
    # credit or Canada workers benefit. With no amount entered on line 14600, line 25000 is line
    # 14700, 2000, so taxable income is 45400 - 2000 = 43400.
    worksheet = compute_with_schedule_8(
        "0",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
        old_age_security="8000",
        cpp_or_qpp_benefits="9000",
        other_pensions_and_superannuation="20000",
        t5_investment_income="1200",
        investment_income_without_a_slip="300",
        investment_income_reported_in_previous_years="100",
        rrsp_income="5000",
        workers_compensation_benefits="2000",
        income_tax_deducted="3000",
    )

    assert worksheet.get(INVESTMENT_INCOME_BEFORE_PRIOR_YEARS).value == D("1500")
    assert worksheet.get(INTEREST_AND_OTHER_INVESTMENT_INCOME).value == D("1400")
    assert worksheet.get(INCOME_SUPPORT_BENEFITS).value == D("2000")
    assert worksheet.get(TOTAL_INCOME).value == D("45400")
    assert worksheet.get(CPP_ENHANCED_CONTRIBUTIONS).value == D("0")
    assert worksheet.get(NET_INCOME).value == D("45400")
    assert worksheet.get(OTHER_PAYMENTS_DEDUCTION).value == D("2000")
    assert worksheet.get(DEDUCTIONS_FROM_NET_INCOME).value == D("2000")
    assert worksheet.get(TAXABLE_INCOME).value == D("43400.00")
    assert worksheet.get(FEDERAL_BASIC_TAX).value == D("6293.00")
    assert worksheet.get(NON_REFUNDABLE_TAX_CREDITS).value == D("2338.71")
    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("3954.29")
    assert worksheet.get(ONTARIO_BASIC_TAX).value == D("2191.70")
    assert worksheet.get(ontario.NON_REFUNDABLE_TAX_CREDITS).value == D("643.72")
    assert worksheet.get(ONTARIO_TAX_AFTER_CREDITS).value == D("1547.98")
    assert worksheet.get(LIFT_REDUCTION).value == D("645.00")
    assert worksheet.get(LIFT_CREDIT).value == D("0")
    assert worksheet.get(ONTARIO_HEALTH_PREMIUM).value == D("450")
    assert worksheet.get(ONTARIO_TAX).value == D("1997.98")
    assert worksheet.get(TOTAL_PAYABLE).value == D("5952.27")
    assert worksheet.get(WORKING_INCOME).value == D("0")
    assert worksheet.get(CANADA_WORKERS_BENEFIT).value == D("0")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("2952.27")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "total_income: employment_income 0 + other_employment_income 0 + old_age_security 8000 "
        "+ cpp_or_qpp_benefits 9000 + other_pensions_and_superannuation 20000 "
        "+ elected_split_pension_amount 0 + universal_child_care_benefit 0 "
        "+ ei_and_other_benefits 0 + taxable_dividends 0 "
        "+ interest_and_other_investment_income 1400 "
        "+ net_partnership_income 0 + rdsp_income 0 + net_rental_income 0 "
        "+ taxable_capital_gains 0 "
        "+ taxable_support_payments 0 + rrsp_income 5000 + fhsa_income 0 + other_fhsa_income 0 "
        "+ other_income 0 + taxable_scholarships 0 + net_self_employment_income 0 "
        "+ income_support_benefits 2000 = 45400"
    ) in rendered
