"""CA-ON 2025 end to end: return bp (the ticket's example: a T4 for Ontario employment and a T4 for
Quebec employment, no CPT20 election and Part 4 of Form RC381 not completed)."""

from __future__ import annotations

from decimal import Decimal

from app.domain.worksheet import Worksheet
from app.jurisdictions.ca.catalog import (
    CPP_BASE_CONTRIBUTIONS_ON_RETURN,
    CPP_BASE_CONTRIBUTIONS_ON_SELF_EMPLOYMENT_AND_OTHER_EARNINGS,
    CPP_DEDUCTION_ON_SELF_EMPLOYMENT_AND_OTHER_EARNINGS,
    CPP_ENHANCED_CONTRIBUTIONS_ON_RETURN,
    CPP_OVERPAYMENT,
    CPP_PAYABLE_ON_SELF_EMPLOYMENT_AND_OTHER_EARNINGS,
)
from tests.jurisdictions.ca_on.end_to_end.support import D, compute


def return_bp(quebec_t4_slip_count: int = 1) -> Worksheet:
    """Return BP's inputs (`returns/2025_return_bp.yaml`): employment income of 70000 on a T4 for
    Ontario employment (box 26 of 30000, box 16 of 1800.00) and a T4 for Quebec employment (box 26
    of 40000, box 17 of 2500.00), with no CPT20 election."""
    return compute(
        "70000",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
        cpp_months=12,
        qpp_months=12,
        t4_cpp_pensionable_earnings_outside_quebec="30000",
        t4_qpp_pensionable_earnings_in_quebec="40000",
        cpp_t4_base_and_first_additional_contributions="1800.00",
        t4_qpp_contributions_box_17="2500.00",
        quebec_t4_slip_count=quebec_t4_slip_count,
        income_tax_deducted="12000",
    )


def t1_lines(worksheet: Worksheet) -> dict[str, Decimal]:
    """The six T1 lines of `worksheet` that Schedule 8 or Form RC381 reaches."""
    return {
        "line_30800": worksheet.get(CPP_BASE_CONTRIBUTIONS_ON_RETURN).value,
        "line_22215": worksheet.get(CPP_ENHANCED_CONTRIBUTIONS_ON_RETURN).value,
        "line_44800": worksheet.get(CPP_OVERPAYMENT).value,
        "line_42100": worksheet.get(CPP_PAYABLE_ON_SELF_EMPLOYMENT_AND_OTHER_EARNINGS).value,
        "line_31000": worksheet.get(
            CPP_BASE_CONTRIBUTIONS_ON_SELF_EMPLOYMENT_AND_OTHER_EARNINGS
        ).value,
        "line_22200": worksheet.get(CPP_DEDUCTION_ON_SELF_EMPLOYMENT_AND_OTHER_EARNINGS).value,
    }


def test_return_bp_t1_lines_30800_22215_and_44800_are_the_tickets_figures() -> None:
    # Part 3a: line 70 (3,462.75), line 73 (665.00) and line 74 (172.25) are carried to the T1.
    worksheet = return_bp()

    assert worksheet.get(CPP_BASE_CONTRIBUTIONS_ON_RETURN).value == D("3462.75")
    assert worksheet.get(CPP_ENHANCED_CONTRIBUTIONS_ON_RETURN).value == D("665.00")
    assert worksheet.get(CPP_OVERPAYMENT).value == D("172.25")


def test_return_bp_lines_42100_31000_and_22200_are_zero_without_part_4() -> None:
    worksheet = return_bp()

    assert worksheet.get(CPP_PAYABLE_ON_SELF_EMPLOYMENT_AND_OTHER_EARNINGS).value == D("0")
    assert worksheet.get(CPP_BASE_CONTRIBUTIONS_ON_SELF_EMPLOYMENT_AND_OTHER_EARNINGS).value == D(
        "0"
    )
    assert worksheet.get(CPP_DEDUCTION_ON_SELF_EMPLOYMENT_AND_OTHER_EARNINGS).value == D("0")


def test_return_bp_without_a_quebec_t4_slip_the_t1_lines_are_schedule_8s() -> None:
    # The same slips with a Quebec T4 slip count of 0: Schedule 8 on the whole employment income
    # of 70,000 requires 3,291.75 and 665.00 but only 1,800.00 was paid (box 16), so Part 3b takes
    # the contributions actually paid: 1,497.48 and 302.52, and nothing is overpaid.
    assert t1_lines(return_bp(quebec_t4_slip_count=0)) == {
        "line_30800": D("1497.48"),
        "line_22215": D("302.52"),
        "line_44800": D("0.00"),
        "line_42100": D("0"),
        "line_31000": D("0"),
        "line_22200": D("0"),
    }
