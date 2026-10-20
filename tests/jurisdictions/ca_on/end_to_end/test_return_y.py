"""CA-ON 2025 end to end: return y."""

from __future__ import annotations

from app.adapters.inbound.trace_english import EnglishTraceRenderer
from app.domain.parameters.rate import Rate
from app.jurisdictions.ca.catalog import (
    CHILD_CARE_EXPENSES,
    NET_INCOME_BEFORE_ADJUSTMENTS,
    PROVINCIAL_CREDITS,
    REFUND_OR_BALANCE_OWING,
    TOTAL_CREDITS,
    TOTAL_PAYABLE,
)
from app.jurisdictions.ca_on.catalog import (
    CARE_ADJUSTED_INCOME,
    CARE_CREDIT,
    CARE_CREDIT_PERCENTAGE,
    CARE_FAMILY_ADJUSTED_INCOME,
    CARE_SUPPORTING_PERSONS_ADJUSTED_INCOME,
    ONTARIO_CREDITS_SUBTOTAL,
)
from tests.jurisdictions.ca_on.end_to_end.support import D, compute, return_f_with_credits


def test_return_ys_supporting_person_lowers_the_care_credit_to_1650() -> None:
    # Return Y is Return F with a supporting person's adjusted income of 30000 (Schedule ON479-A
    # column 2 line 4, line 63047). Line 4 is 54435.00 + 5000 = 59435.00, line 5 is 59435.00 +
    # 30000 = 89435.00, in "more than $88,800 but not more than $92,400: 33%", so line 7 is 33%
    # (Return F's 51%) and line 8 is 5000 x 33% = 1650.00. Line 18 and T1 line 47900 are 1650.00,
    # the total credits 8000 + 0 + 1650.00 = 9650.00 and line 167 is 4240.69 - 9650.00 =
    # -5409.31, Return F's -6309.31 plus the 900.00 the supporting person takes off the credit.
    return_f = return_f_with_credits("0", "0")
    worksheet = compute(
        "60000",
        "0",
        "0",
        "0",
        "10800",
        "0",
        "0",
        dependent_children=1,
        eligible_dependants=1,
        cwb_eligible_dependants=1,
        child_care_expenses_paid="6000",
        children_seven_to_sixteen=1,
        income_tax_deducted="8000",
        care_supporting_persons_adjusted_income="30000",
    )

    assert worksheet.get(CARE_SUPPORTING_PERSONS_ADJUSTED_INCOME).value == D("30000")
    assert worksheet.get(CHILD_CARE_EXPENSES).value == D("5000")
    assert worksheet.get(CARE_ADJUSTED_INCOME).value == D("59435.00")
    assert worksheet.get(CARE_FAMILY_ADJUSTED_INCOME).value == D("89435.00")
    assert worksheet.get(CARE_CREDIT_PERCENTAGE).value == Rate(D("0.33"))
    assert worksheet.get(CARE_CREDIT).value == D("1650.00")
    assert worksheet.get(ONTARIO_CREDITS_SUBTOTAL).value == D("1650.00")
    assert worksheet.get(PROVINCIAL_CREDITS).value == D("1650.00")
    assert worksheet.get(TOTAL_PAYABLE).value == D("4240.69")
    assert worksheet.get(TOTAL_CREDITS).value == D("9650.00")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-5409.31")
    assert return_f.get(CARE_CREDIT_PERCENTAGE).value == Rate(D("0.51"))
    assert return_f.get(CARE_FAMILY_ADJUSTED_INCOME).value == D("59435.00")
    assert return_f.get(REFUND_OR_BALANCE_OWING).value - worksheet.get(
        REFUND_OR_BALANCE_OWING
    ).value == D("-900.00")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "care_family_adjusted_income: care_adjusted_income 59435 "
        "+ care_supporting_persons_adjusted_income 30000 = 89435"
    ) in rendered
    assert (
        "care_credit_percentage: care_family_adjusted_income 89435, "
        "more than 88800 but not more than 92400: 33%"
    ) in rendered
    assert (
        "care_credit: care_credit_percentage 33% of child_care_expenses 5000 (half-up to 0.01)"
    ) in rendered
    assert (
        "ontario_credits_subtotal: fertility_credit 0 + care_credit 1650 "
        "+ seniors_care_credit 0 + seniors_transit_credit 0 + political_credit 0 "
        "+ flow_through_share_credit 0 = 1650"
    ) in rendered


def test_a_family_adjusted_income_of_0_is_taxed_at_75_percent() -> None:
    # Schedule ON479-A line 7: "If your family adjusted income on line 5 is "0", enter 75%." No
    # income and no supporting person: line 4 is 0, line 5 is 0, line 7 is 75% and, with no child
    # care expenses (line 6, 0), line 8 is 0 x 75% = 0.00.
    worksheet = compute("0", "0", "0", "0", "0", "0", "0")

    assert worksheet.get(CARE_ADJUSTED_INCOME).value == D("0")
    assert worksheet.get(CARE_FAMILY_ADJUSTED_INCOME).value == D("0")
    assert worksheet.get(CARE_CREDIT_PERCENTAGE).value == Rate(D("0.75"))
    assert worksheet.get(CARE_CREDIT).value == D("0.00")


def test_a_family_adjusted_income_on_a_row_limit_takes_that_rows_rate() -> None:
    # Schedule ON479-A line 5 is the supporting person's 30000 alone: "more than $27,500 but not
    # more than $30,000: 67%" includes 30,000, so line 7 is 67%, not the next row's 65%.
    worksheet = compute(
        "0", "0", "0", "0", "0", "0", "0", care_supporting_persons_adjusted_income="30000"
    )

    assert worksheet.get(CARE_FAMILY_ADJUSTED_INCOME).value == D("30000")
    assert worksheet.get(CARE_CREDIT_PERCENTAGE).value == Rate(D("0.67"))
    assert worksheet.get(CARE_CREDIT).value == D("0.00")


def test_a_net_income_below_zero_is_floored_at_zero_on_line_4() -> None:
    # Schedule ON479-A line 4 "Add lines 1 to 3 (if negative, enter "0")": line 1 is the net income
    # before adjustments, 0 - union dues 1000 = -1000.00, and line 2 is 0, so line 4 is 0, not
    # -1000.00, and line 5 is 0 with no supporting person.
    worksheet = compute("0", "0", "0", "0", "0", "0", "1000")

    assert worksheet.get(NET_INCOME_BEFORE_ADJUSTMENTS).value == D("-1000.00")
    assert worksheet.get(CARE_ADJUSTED_INCOME).value == D("0")
    assert worksheet.get(CARE_FAMILY_ADJUSTED_INCOME).value == D("0")
    assert worksheet.get(CARE_CREDIT_PERCENTAGE).value == Rate(D("0.75"))
    assert (
        "care_adjusted_income: net_income_before_adjustments -1000 + child_care_expenses 0, "
        "not below 0 = 0"
    ) in EnglishTraceRenderer().render_all(worksheet.trace)
