"""CA-ON 2025 end to end: return ay."""

from __future__ import annotations

from app.domain.parameters.rate import Rate
from app.domain.worksheet import Worksheet
from app.jurisdictions.ca.catalog import (
    CHILD_CARE_EXPENSES,
    NET_INCOME_BEFORE_ADJUSTMENTS,
    NET_INCOME_SIGNED,
    TOSI_ADJUSTED_NET_INCOME,
    TOTAL_SPLIT_INCOME,
)
from app.jurisdictions.ca_on.catalog import (
    CARE_ADJUSTED_INCOME,
    CARE_CREDIT,
    CARE_CREDIT_PERCENTAGE,
    CARE_FAMILY_ADJUSTED_INCOME,
)
from tests.jurisdictions.ca_on.end_to_end.support import D, compute


def return_ay() -> Worksheet:
    """Return AY's inputs, as in `returns/2025_return_ay.yaml`: Return Y's, with 10000 of
    dividends other than eligible dividends received with no slip, all of it split income."""
    return compute(
        "60000",
        (),
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
        other_dividends_received_without_a_slip="10000",
        split_income_dividends="11500",
        split_income_dividends_other_than_eligible="11500",
    )


def test_return_ays_care_credit_reads_line_23600_before_its_floor_on_line_1() -> None:
    # Form T1206 Part 1: line 4 is the split income, 11500, and line 5 is the net income before
    # adjustments, 54435.00 (line 23200 takes the split income out again), so line 6 is
    # 11500 + 54435.00 = 65935.00. Schedule ON479-A column 1: line 1 is line 23600 before its
    # floor, 54435.00 (line 23500 is 0), not that 65935.00, line 2 the child care expenses
    # deduction, 5000, line 3 is 0 and line 4 is 59435.00; line 5 adds the supporting person's
    # 30000: 89435.00, in the 33% row (as Return Y's); line 8 is 5000 x 33% = 1650.00.
    worksheet = return_ay()

    assert worksheet.get(TOTAL_SPLIT_INCOME).value == D("11500")
    assert worksheet.get(NET_INCOME_BEFORE_ADJUSTMENTS).value == D("54435.00")
    assert worksheet.get(TOSI_ADJUSTED_NET_INCOME).value == D("65935.00")
    assert worksheet.get(CHILD_CARE_EXPENSES).value == D("5000.00")
    assert worksheet.get(NET_INCOME_SIGNED).value == D("54435.00")
    assert worksheet.get(CARE_ADJUSTED_INCOME).value == D("59435.00")
    assert worksheet.get(CARE_FAMILY_ADJUSTED_INCOME).value == D("89435.00")
    assert worksheet.get(CARE_CREDIT_PERCENTAGE).value == Rate(D("0.33"))
    assert worksheet.get(CARE_CREDIT).value == D("1650.00")
