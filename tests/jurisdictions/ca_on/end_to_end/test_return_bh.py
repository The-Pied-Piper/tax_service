"""CA-ON 2025 end to end: return bh (Form T657 Chart 2024 into Chart 2025)."""

from __future__ import annotations

from typing import Any

from app.domain.worksheet import Worksheet
from app.jurisdictions.ca.catalog import (
    ANNUAL_GAINS_LIMIT_2025,
    CAPITAL_GAINS_DEDUCTION,
    CHART_2024_PERIOD_1_AMOUNT_A,
    CHART_2024_PERIOD_1_AMOUNT_E,
    CHART_2024_PERIOD_1_AMOUNT_I,
    CHART_2024_PERIOD_1_AMOUNT_L,
    CHART_2024_PERIOD_1_AMOUNT_N,
    CHART_2024_PERIOD_1_AMOUNT_O,
    CHART_2024_PERIOD_1_AMOUNTS_F_TO_H,
    CHART_2024_PERIOD_2_AMOUNT_C,
    CHART_2024_PERIOD_2_AMOUNT_E,
    CHART_2024_PERIOD_2_AMOUNT_I,
    CHART_2024_PERIOD_2_AMOUNT_L,
    CHART_2024_PERIOD_2_AMOUNT_N,
    CHART_2024_PERIOD_2_AMOUNT_O,
    CHART_2025_PART_1_AMOUNT_C,
    CHART_2025_PART_1_AMOUNT_E,
    CHART_2025_PART_1_AMOUNT_N,
    CHART_2025_PART_1_AMOUNT_P,
    CHART_2025_PART_1_AMOUNT_Q,
    CHART_2025_PART_2_AMOUNT_C,
    CHART_2025_PART_2_AMOUNT_E,
    CHART_2025_PART_2_AMOUNT_N,
    CHART_2025_PART_2_AMOUNT_P,
    CHART_2025_PART_2_AMOUNT_Q,
)
from tests.jurisdictions.ca_on.end_to_end.support import D, compute


def return_bh(**overrides: Any) -> Worksheet:
    """Return BH's inputs, as in `returns/2025_return_bh.yaml`.

    Return BF's inputs (one QSBCS disposition in 2025 for a gain of 350000, 20000 of net capital
    losses of other years, 100000 of taxable capital gains for 2002 to 2024 and 155000 claimed on
    line 25400), and two reserves reported in 2025: 40000 on Form T2017 line 12 for Chart 2024
    Period 1, and 30000 on Form T2017 line 6 for Chart 2024 Period 2.
    """
    inputs: dict[str, Any] = {
        "employment_income": "0",
        "share_dispositions": (),
        "unused_rrsp_contributions": "0",
        "rrsp_contributions": "0",
        "rrsp_deduction_limit": "0",
        "rrsp_amount_deducted": "0",
        "union_dues": "0",
        "other_income": "10000",
        "qsbcs_dispositions": (("500000", "150000", "0"),),
        "unapplied_net_capital_losses_2001_to_2024": "20000",
        "net_capital_losses_claimed": "20000",
        "t657_gains_2002_to_2024": "100000",
        "t657_chart_2024_period_1_amount_g": "40000",
        "t657_chart_2024_period_2_amount_f": "30000",
        "capital_gains_deduction_claimed": "155000",
    }
    return compute(**{**inputs, **overrides})


def test_period_1_of_2024_takes_the_40000_reserve_to_amount_n_of_20000() -> None:
    # Period 1: A 508418.00; B 0, so C and E are 508418.00 (D 0). G is 40000, so F to H add to
    # 40000 and I is 20000.00; J is 0, so K is 20000.00. L is the lesser of E and K: 20000.00; M
    # is B, 0, so N is 20000.00. O is the lesser of 155000.00, 255000.00 and N: 20000.00.
    worksheet = return_bh()

    assert worksheet.get(CHART_2024_PERIOD_1_AMOUNT_A).value == D("508418")
    assert worksheet.get(CHART_2024_PERIOD_1_AMOUNT_E).value == D("508418.00")
    assert worksheet.get(CHART_2024_PERIOD_1_AMOUNTS_F_TO_H).value == D("40000")
    assert worksheet.get(CHART_2024_PERIOD_1_AMOUNT_I).value == D("20000.00")
    assert worksheet.get(CHART_2024_PERIOD_1_AMOUNT_L).value == D("20000.00")
    assert worksheet.get(CHART_2024_PERIOD_1_AMOUNT_N).value == D("20000.00")
    assert worksheet.get(CHART_2024_PERIOD_1_AMOUNT_O).value == D("20000.00")


def test_period_2_of_2024_takes_period_1s_total_of_20000_as_amount_b() -> None:
    # Period 2: A 625000.00 less B (Period 1's N, 20000.00) is C, 605000.00, and E the same (D 0).
    # F is 30000, so I is 15000.00; L is the lesser of E and K, 15000.00. M is B, 20000.00, so N is
    # 35000.00, and O is the lesser of 155000.00, 255000.00 and N: 35000.00.
    worksheet = return_bh()

    assert worksheet.get(CHART_2024_PERIOD_2_AMOUNT_C).value == D("605000.00")
    assert worksheet.get(CHART_2024_PERIOD_2_AMOUNT_E).value == D("605000.00")
    assert worksheet.get(CHART_2024_PERIOD_2_AMOUNT_I).value == D("15000.00")
    assert worksheet.get(CHART_2024_PERIOD_2_AMOUNT_L).value == D("15000.00")
    assert worksheet.get(CHART_2024_PERIOD_2_AMOUNT_N).value == D("35000.00")
    assert worksheet.get(CHART_2024_PERIOD_2_AMOUNT_O).value == D("35000.00")


def test_chart_2025_part_1_takes_period_2s_total_of_35000_as_amount_b() -> None:
    # Part 1: A 522145.00 less B (Period 2's N, 35000.00) is C, 487145.00, and E the same (D 0).
    # Nothing is reported in F to J, so K and M are 0 and N is 0. O is B, 35000.00, so P is
    # 35000.00, and Q is the lesser of 155000.00, 255000.00 and P: 35000.00.
    worksheet = return_bh()

    assert worksheet.get(CHART_2025_PART_1_AMOUNT_C).value == D("487145.00")
    assert worksheet.get(CHART_2025_PART_1_AMOUNT_E).value == D("487145.00")
    assert worksheet.get(CHART_2025_PART_1_AMOUNT_N).value == D("0.00")
    assert worksheet.get(CHART_2025_PART_1_AMOUNT_P).value == D("35000.00")
    assert worksheet.get(CHART_2025_PART_1_AMOUNT_Q).value == D("35000.00")


def test_chart_2025_part_2_takes_part_1s_total_as_amount_b_and_line_25400_stays_at_155000() -> None:
    # Part 2: A 625000.00 less B (Part 1's P, 35000.00) is C, 590000.00, and E the same. F is
    # 350000, the other amounts 0, so K is 175000.00 and M is 175000.00; N is 175000.00. O is B,
    # 35000.00, so P is 210000.00, and Q is the lesser of 155000.00, 255000.00 and P: 155000.00.
    # The reserves are inside that cap: the filer claims 155000, so line 25400 is 155000.00.
    worksheet = return_bh()

    assert worksheet.get(CHART_2025_PART_2_AMOUNT_C).value == D("590000.00")
    assert worksheet.get(CHART_2025_PART_2_AMOUNT_E).value == D("590000.00")
    assert worksheet.get(CHART_2025_PART_2_AMOUNT_N).value == D("175000.00")
    assert worksheet.get(CHART_2025_PART_2_AMOUNT_P).value == D("210000.00")
    assert worksheet.get(CHART_2025_PART_2_AMOUNT_Q).value == D("155000.00")
    assert worksheet.get(ANNUAL_GAINS_LIMIT_2025).value == D("155000.00")
    assert worksheet.get(CAPITAL_GAINS_DEDUCTION).value == D("155000")
