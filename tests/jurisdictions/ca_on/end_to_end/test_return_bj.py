"""CA-ON 2025 end to end: return bj, two Form T2125 statements on one return."""

from __future__ import annotations

from typing import Any

from app.domain.artifact import ArtifactRegistry
from app.domain.record_list import RecordList
from app.domain.trace import FormInstanceLine
from app.domain.worksheet import Worksheet
from app.jurisdictions.ca.catalog import (
    BUSINESS_INCOME,
    NET_SELF_EMPLOYMENT_INCOME,
    TOTAL_INCOME,
)
from tests.jurisdictions.ca_on.end_to_end.support import CA_ON, D, compute, run, service

# T2125 amount 3A "Gross sales, commissions, or fees": the first business has 12,000 of it and no
# expenses, so its line 9946 "Your net income (loss)" is 12,000. The second has no sales and
# advertising (line 8521) of 2,000, so its line 9946 is 0 - 2,000 = -2,000: a loss.
BUSINESS_1: dict[str, Any] = {"business": {"gross_sales": "12000"}}
BUSINESS_2: dict[str, Any] = {"business": {"advertising": "2000"}}


def bj_inputs(statements: tuple[dict[str, Any], ...]) -> dict[str, Any]:
    """Return BJ's inputs, as in `returns/2025_return_bj.yaml`: a sole proprietor with the T2125
    `statements` given (none: no business), no farm, no rental operation and no other income."""
    return {
        "employment_income": "0",
        "share_dispositions": (),
        "unused_rrsp_contributions": "0",
        "rrsp_contributions": "0",
        "rrsp_deduction_limit": "0",
        "rrsp_amount_deducted": "0",
        "union_dues": "0",
        "rental_statements": (),
        "business_statements": statements,
        "farm_statements": (),
    }


def return_bj(*statements: dict[str, Any]) -> Worksheet:
    """The return form's worksheet of return BJ with the T2125 `statements`."""
    return compute(**bj_inputs(statements))


def run_bj(*statements: dict[str, Any]) -> dict[str, tuple[Worksheet, ...]]:
    """Every form's worksheets of return BJ with the T2125 `statements`."""
    return run(**bj_inputs(statements))


def net_incomes(worksheet: Worksheet) -> list[Any]:
    """Line 9946 of each statement, in statement order, as the return receives it."""
    kind = ArtifactRegistry.shared().kind("ca/t2125.business_income")
    value = worksheet.get(kind).value
    assert isinstance(value, RecordList)
    return [record[BUSINESS_INCOME] for record in value.records]


def test_two_statements_with_lines_9946_of_12000_and_minus_2000_give_line_13500_of_10000() -> None:
    # T1 line 13500 "Net" adds the lines 9946 of the statements: 12,000.00 + (-2,000.00).
    worksheet = return_bj(BUSINESS_1, BUSINESS_2)

    assert worksheet.get(BUSINESS_INCOME).value == D("10000.00")


def test_line_13500_is_the_whole_of_net_self_employment_income_and_total_income() -> None:
    worksheet = return_bj(BUSINESS_1, BUSINESS_2)

    assert worksheet.get(NET_SELF_EMPLOYMENT_INCOME).value == D("10000.00")
    assert worksheet.get(TOTAL_INCOME).value == D("10000.00")


def test_the_return_receives_line_9946_of_each_statement_in_statement_order() -> None:
    worksheet = return_bj(BUSINESS_1, BUSINESS_2)

    assert net_incomes(worksheet) == [D("12000.00"), D("-2000.00")]


def test_the_order_of_the_statements_does_not_change_the_total() -> None:
    worksheet = return_bj(BUSINESS_2, BUSINESS_1)

    assert net_incomes(worksheet) == [D("-2000.00"), D("12000.00")]
    assert worksheet.get(BUSINESS_INCOME).value == D("10000.00")


def test_one_statement_gives_its_own_line_9946_a_loss_staying_a_loss() -> None:
    assert return_bj(BUSINESS_1).get(BUSINESS_INCOME).value == D("12000.00")
    assert return_bj(BUSINESS_2).get(BUSINESS_INCOME).value == D("-2000.00")


def test_a_third_statement_is_added_too() -> None:
    worksheet = return_bj(BUSINESS_1, BUSINESS_2, BUSINESS_1)

    assert worksheet.get(BUSINESS_INCOME).value == D("22000.00")


def test_a_return_with_no_statement_has_line_13500_of_zero() -> None:
    worksheet = return_bj()

    assert worksheet.get(BUSINESS_INCOME).value == D("0")
    assert worksheet.get(NET_SELF_EMPLOYMENT_INCOME).value == D("0")
    assert worksheet.get(TOTAL_INCOME).value == D("0")
    assert net_incomes(worksheet) == []


def test_each_statement_has_its_own_worksheet_with_its_line_9946() -> None:
    result = run_bj(BUSINESS_1, BUSINESS_2)

    assert [worksheet.get(BUSINESS_INCOME).value for worksheet in result["ca/t2125"]] == [
        D("12000.00"),
        D("-2000.00"),
    ]
    assert len(result["ca/t2125"]) == 2


def test_a_return_with_no_statement_runs_the_form_on_no_instance() -> None:
    assert run_bj()["ca/t2125"] == ()


def test_the_trace_keeps_the_lines_of_each_statement_under_its_position() -> None:
    result = run_bj(BUSINESS_1, BUSINESS_2)

    groups = [
        line
        for line in service().compose(CA_ON, 2025).trace(result)
        if isinstance(line, FormInstanceLine)
    ]

    assert [(group.form, group.position) for group in groups] == [
        ("ca/t2125", 1),
        ("ca/t2125", 2),
        ("ca-on/return", 1),
    ]
    assert all(group.lines for group in groups)
