"""CA-ON 2025 end to end: return bm."""

from __future__ import annotations

from typing import Any

from app.domain.worksheet import Worksheet
from app.jurisdictions.ca.catalog import (
    ITC_AGRICULTURAL_SRED_CREDIT,
    ITC_APPRENTICESHIP_CREDIT,
    ITC_APPRENTICESHIP_WAGES_TOTAL,
    ITC_APPRENTICESHIP_WAGES_WITH_T3,
    ITC_CRITICAL_MINERAL_CREDIT,
    ITC_MINERAL_EXPLORATION_CREDIT,
    ITC_NONREFUNDABLE_CREDITS,
    ITC_QUALIFIED_PROPERTY_CREDIT,
    ITC_REFUNDABLE_CREDITS,
    ITC_SRED_CREDIT,
    ITC_SRED_REPAYMENT_CREDIT,
    ITC_SRED_REPAYMENT_CREDIT_2014_AND_PRIOR,
    ITC_SRED_REPAYMENT_CREDIT_2015_AND_AFTER,
)
from tests.jurisdictions.ca_on.end_to_end.support import D, compute

# The lines of the return that the investment tax credit reads, all zero: the filer has no income,
# deduction or credit beyond the investment tax credit lines of Parts A and B.
NO_OTHER_LINES: dict[str, Any] = {
    "employment_income": "0",
    "share_dispositions": (),
    "unused_rrsp_contributions": "0",
    "rrsp_contributions": "0",
    "rrsp_deduction_limit": "0",
    "rrsp_amount_deducted": "0",
    "union_dues": "0",
}


def return_bm(**overrides: Any) -> Worksheet:
    """Return BM's Parts A and B lines, as in `returns/2025_return_bm.yaml`, with overrides."""
    inputs: dict[str, Any] = {
        **NO_OTHER_LINES,
        "itc_sred_expenditures": "40000",
        "itc_agricultural_sred_contributions": "10000",
        "itc_sred_partnership_allocation": "2000",
        "itc_qualified_property": "10000",
        "itc_mineral_exploration_expenditures": "20000",
        "itc_critical_mineral_expenditures": "5000",
        "itc_apprentices": ("25000", "15000"),
        "itc_apprenticeship_t3_box_40": "5000",
        "itc_sred_repayment_2014_and_prior": "1000",
        "itc_sred_repayment_2015_and_after": "2000",
    }
    return compute(**{**inputs, **overrides})


def test_return_bm_amount_1_is_the_sred_expenditures_at_15_percent() -> None:
    # Return BM, Part A line 1: line 67120 of 40000.00 times 0.15 is 6000.00.
    worksheet = return_bm()

    assert worksheet.get(ITC_SRED_CREDIT).value == D("6000.00")


def test_return_bm_amount_2_is_the_agricultural_contributions_at_15_percent() -> None:
    # Return BM, Part A line 2: line 67130 of 10000.00 times 0.15 is 1500.00.
    worksheet = return_bm()

    assert worksheet.get(ITC_AGRICULTURAL_SRED_CREDIT).value == D("1500.00")


def test_return_bm_amount_4_is_the_qualified_property_at_10_percent() -> None:
    # Return BM, Part A line 4: line 67140 of 10000.00 times 0.10 is 1000.00.
    worksheet = return_bm()

    assert worksheet.get(ITC_QUALIFIED_PROPERTY_CREDIT).value == D("1000.00")


def test_return_bm_amount_a_adds_amounts_1_to_4_with_the_partnership_allocation() -> None:
    # Return BM, Part A amount A: 6000.00 plus 1500.00 plus the partnership allocation of 2000.00
    # (line 67135, read as it is) plus 1000.00, 10500.00.
    worksheet = return_bm()

    assert worksheet.get(ITC_REFUNDABLE_CREDITS).value == D("10500.00")


def test_return_bm_amounts_b_and_c_are_at_15_and_30_percent() -> None:
    # Return BM, Part B: line 67170 of 20000.00 times 0.15 is amount B, 3000.00; line 67175 of
    # 5000.00 times 0.30 is amount C, 1500.00.
    worksheet = return_bm()

    assert worksheet.get(ITC_MINERAL_EXPLORATION_CREDIT).value == D("3000.00")
    assert worksheet.get(ITC_CRITICAL_MINERAL_CREDIT).value == D("1500.00")


def test_return_bm_table_1_column_3_is_the_lesser_of_each_apprentice_and_20000() -> None:
    # Return BM, Table 1: the apprentice of 25000.00 counts 20000.00, the one of 15000.00 counts
    # 15000.00, so column 3 totals 35000.00.
    worksheet = return_bm()

    assert worksheet.get(ITC_APPRENTICESHIP_WAGES_TOTAL).value == D("35000.00")


def test_return_bm_one_apprentice_over_20000_is_counted_at_20000() -> None:
    # Table 1 column 3 for a single apprentice of 25000.00: the lesser of that and 20000.00.
    worksheet = return_bm(itc_apprentices=("25000",))

    assert worksheet.get(ITC_APPRENTICESHIP_WAGES_TOTAL).value == D("20000.00")


def test_return_bm_line_67180_adds_the_t3_box_40_amount_and_amount_d_is_10_percent() -> None:
    # Return BM, Part B line 67180: 35000.00 plus the T3 box 40 amount of 5000.00 is 40000.00, and
    # amount D is 40000.00 times 0.10, 4000.00.
    worksheet = return_bm()

    assert worksheet.get(ITC_APPRENTICESHIP_WAGES_WITH_T3).value == D("40000.00")
    assert worksheet.get(ITC_APPRENTICESHIP_CREDIT).value == D("4000.00")


def test_return_bm_amount_e_adds_the_2014_and_prior_and_2015_and_after_repayments() -> None:
    # Return BM, Part B repayments: line 67184 of 1000.00 times 0.20 is amount 1, 200.00; line
    # 67185 of 2000.00 times 0.15 is amount 2, 300.00; amount E is 500.00.
    worksheet = return_bm()

    assert worksheet.get(ITC_SRED_REPAYMENT_CREDIT_2014_AND_PRIOR).value == D("200.00")
    assert worksheet.get(ITC_SRED_REPAYMENT_CREDIT_2015_AND_AFTER).value == D("300.00")
    assert worksheet.get(ITC_SRED_REPAYMENT_CREDIT).value == D("500.00")


def test_return_bm_amount_f_adds_amounts_b_c_d_and_e() -> None:
    # Return BM, Part B amount F: 3000.00 plus 1500.00 plus 4000.00 plus 500.00, 9000.00.
    worksheet = return_bm()

    assert worksheet.get(ITC_NONREFUNDABLE_CREDITS).value == D("9000.00")


def test_the_ticket_acceptance_qualified_property_of_10000_gives_amount_4_and_a_of_1000() -> None:
    # The acceptance figure: 10,000 of qualified property (line 67140) and no other entries
    # gives amount 4 of 1,000.00, and amount A of 1,000.00.
    worksheet = compute(**{**NO_OTHER_LINES, "itc_qualified_property": "10000"})

    assert worksheet.get(ITC_QUALIFIED_PROPERTY_CREDIT).value == D("1000.00")
    assert worksheet.get(ITC_REFUNDABLE_CREDITS).value == D("1000.00")
