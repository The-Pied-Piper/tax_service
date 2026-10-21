"""CA-ON 2025 end to end: return bh (Form T657 Charts 2021 to 2024 into Chart 2025)."""

from __future__ import annotations

from typing import Any

from app.domain.worksheet import Worksheet
from app.jurisdictions.ca.catalog import (
    ANNUAL_GAINS_LIMIT_2025,
    CAPITAL_GAINS_DEDUCTION,
    CHART_2021_AMOUNT_D,
    CHART_2021_PART_1_AMOUNT_A,
    CHART_2021_PART_1_AMOUNT_E,
    CHART_2021_PART_1_AMOUNT_J,
    CHART_2021_PART_1_AMOUNT_K,
    CHART_2021_PART_1_AMOUNT_M,
    CHART_2021_PART_1_AMOUNT_N,
    CHART_2021_PART_1_AMOUNTS_F_AND_G,
    CHART_2021_PART_2_AMOUNT_C,
    CHART_2021_PART_2_AMOUNT_E,
    CHART_2021_PART_2_AMOUNT_K,
    CHART_2021_PART_2_AMOUNT_L,
    CHART_2021_PART_2_APPLIES,
    CHART_2021_TOTAL_CARRIED,
    CHART_2022_PART_1_AMOUNT_C,
    CHART_2022_PART_1_AMOUNT_E,
    CHART_2022_PART_1_AMOUNT_K,
    CHART_2022_PART_1_AMOUNT_M,
    CHART_2022_PART_2_AMOUNT_C,
    CHART_2022_PART_2_AMOUNT_E,
    CHART_2022_PART_2_AMOUNT_L,
    CHART_2022_PART_2_APPLIES,
    CHART_2022_TOTAL_CARRIED,
    CHART_2023_PART_1_AMOUNT_C,
    CHART_2023_PART_1_AMOUNT_E,
    CHART_2023_PART_1_AMOUNT_M,
    CHART_2023_PART_1_AMOUNT_N,
    CHART_2023_TOTAL_CARRIED,
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
    line 25400), two reserves reported in 2025 for 2024: 40000 on Form T2017 line 12 for Chart 2024
    Period 1, and 30000 on Form T2017 line 6 for Chart 2024 Period 2; and a 2021 reserve of 40000 on
    Form T2017 line 12 for Chart 2021 (QSBCS), with 100000 of earlier years' deductions entered as
    Chart 2 line 18.
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
        "t657_chart_2_line_18": "100000",
        "t657_chart_2021_amount_g": "40000",
        "t657_chart_2024_period_1_amount_g": "40000",
        "t657_chart_2024_period_2_amount_f": "30000",
        "capital_gains_deduction_claimed": "155000",
    }
    return compute(**{**inputs, **overrides})


def test_chart_2021_takes_the_40000_reserve_to_amount_n_of_20000() -> None:
    # Chart 2021 Part 1: A 446109.00; B 0 (no 2016 to 2020 charts), so C is 446109.00; D is Chart 2
    # line 19, 100000 (line 18 entered as 100000), so E is 346109.00. G is 40000, F and G add to
    # 40000.00 and H is 20000.00; I is 0 and J is 20000.00. K is the lesser of E and J: 20000.00. M
    # is K plus B, 20000.00, and N is the lesser of 155000.00, 255000.00 and M: 20000.00.
    # Part 2: A 500000.00; B is Part 1's M, so C is 480000.00 and E is 480000.00 less D, 380000.00.
    # F, G and H are 0, so I is 0; K is I plus Part 1's M: 20000.00; L is the lesser of H and K: 0.
    # Part 2 does not apply (no QFFP reserve and no wish for the additional deduction), so the
    # total carried forward is Part 1's M, 20000.00.
    worksheet = return_bh()

    assert worksheet.get(CHART_2021_PART_1_AMOUNT_A).value == D("446109")
    assert worksheet.get(CHART_2021_AMOUNT_D).value == D("100000.00")
    assert worksheet.get(CHART_2021_PART_1_AMOUNT_E).value == D("346109.00")
    assert worksheet.get(CHART_2021_PART_1_AMOUNTS_F_AND_G).value == D("40000.00")
    assert worksheet.get(CHART_2021_PART_1_AMOUNT_J).value == D("20000.00")
    assert worksheet.get(CHART_2021_PART_1_AMOUNT_K).value == D("20000.00")
    assert worksheet.get(CHART_2021_PART_1_AMOUNT_M).value == D("20000.00")
    assert worksheet.get(CHART_2021_PART_1_AMOUNT_N).value == D("20000.00")
    assert worksheet.get(CHART_2021_PART_2_AMOUNT_C).value == D("480000.00")
    assert worksheet.get(CHART_2021_PART_2_AMOUNT_E).value == D("380000.00")
    assert worksheet.get(CHART_2021_PART_2_AMOUNT_K).value == D("20000.00")
    assert worksheet.get(CHART_2021_PART_2_AMOUNT_L).value == D("0.00")
    assert worksheet.get(CHART_2021_PART_2_APPLIES).value == 0
    assert worksheet.get(CHART_2021_TOTAL_CARRIED).value == D("20000.00")


def test_charts_2022_and_2023_pass_the_20000_total_through() -> None:
    # Chart 2022: A 456815.00 less B (Chart 2021's 20000.00) is C, 436815.00, and E 336815.00 (D
    # 100000.00). Nothing is reported, so K is 0 and M is 20000.00 (K plus B), N 20000.00; the Part
    # 2
    # gate is 0 and the total carried is 20000.00. Chart 2023: A 485595.00 less B (20000.00) is C,
    # 465595.00, E 365595.00; M is 20000.00 and the total carried is 20000.00.
    worksheet = return_bh()

    assert worksheet.get(CHART_2022_PART_1_AMOUNT_C).value == D("436815.00")
    assert worksheet.get(CHART_2022_PART_1_AMOUNT_E).value == D("336815.00")
    assert worksheet.get(CHART_2022_PART_1_AMOUNT_K).value == D("0.00")
    assert worksheet.get(CHART_2022_PART_1_AMOUNT_M).value == D("20000.00")
    assert worksheet.get(CHART_2022_PART_2_AMOUNT_C).value == D("480000.00")
    assert worksheet.get(CHART_2022_PART_2_AMOUNT_E).value == D("380000.00")
    assert worksheet.get(CHART_2022_PART_2_APPLIES).value == 0
    assert worksheet.get(CHART_2022_TOTAL_CARRIED).value == D("20000.00")
    assert worksheet.get(CHART_2023_PART_1_AMOUNT_C).value == D("465595.00")
    assert worksheet.get(CHART_2023_PART_1_AMOUNT_E).value == D("365595.00")
    assert worksheet.get(CHART_2023_PART_1_AMOUNT_M).value == D("20000.00")
    assert worksheet.get(CHART_2023_PART_1_AMOUNT_N).value == D("20000.00")
    assert worksheet.get(CHART_2023_TOTAL_CARRIED).value == D("20000.00")


def test_period_1_of_2024_takes_chart_2023s_total_of_20000_as_amount_b() -> None:
    # Period 1: A 508418.00 less B (Chart 2023's total, 20000.00) is C, 488418.00, and E is
    # 388418.00
    # (D 100000.00). G is 40000, so F to H add to 40000 and I is 20000.00; J is 0, so K is 20000.00.
    # L is the lesser of E and K: 20000.00. N is L plus B, 40000.00, and O is the lesser of
    # 155000.00, 255000.00 and N: 40000.00.
    worksheet = return_bh()

    assert worksheet.get(CHART_2024_PERIOD_1_AMOUNT_A).value == D("508418")
    assert worksheet.get(CHART_2024_PERIOD_1_AMOUNT_E).value == D("388418.00")
    assert worksheet.get(CHART_2024_PERIOD_1_AMOUNTS_F_TO_H).value == D("40000")
    assert worksheet.get(CHART_2024_PERIOD_1_AMOUNT_I).value == D("20000.00")
    assert worksheet.get(CHART_2024_PERIOD_1_AMOUNT_L).value == D("20000.00")
    assert worksheet.get(CHART_2024_PERIOD_1_AMOUNT_N).value == D("40000.00")
    assert worksheet.get(CHART_2024_PERIOD_1_AMOUNT_O).value == D("40000.00")


def test_period_2_of_2024_takes_period_1s_total_of_40000_as_amount_b() -> None:
    # Period 2: A 625000.00 less B (Period 1's N, 40000.00) is C, 585000.00, and E is 485000.00 (D
    # 100000.00). F is 30000, so I is 15000.00; L is the lesser of E and K, 15000.00. N is L plus
    # B, 15000.00 + 40000.00 = 55000.00, and O is the lesser of 155000.00, 255000.00 and N:
    # 55000.00.
    worksheet = return_bh()

    assert worksheet.get(CHART_2024_PERIOD_2_AMOUNT_C).value == D("585000.00")
    assert worksheet.get(CHART_2024_PERIOD_2_AMOUNT_E).value == D("485000.00")
    assert worksheet.get(CHART_2024_PERIOD_2_AMOUNT_I).value == D("15000.00")
    assert worksheet.get(CHART_2024_PERIOD_2_AMOUNT_L).value == D("15000.00")
    assert worksheet.get(CHART_2024_PERIOD_2_AMOUNT_N).value == D("55000.00")
    assert worksheet.get(CHART_2024_PERIOD_2_AMOUNT_O).value == D("55000.00")


def test_chart_2025_part_1_takes_period_2s_total_of_55000_as_amount_b() -> None:
    # Part 1: A 522145.00 less B (Period 2's N, 55000.00) is C, 467145.00, and E is 367145.00 (D
    # 100000.00). Nothing is reported in F to J, so K and M are 0 and N is 0. O is B, 55000.00, so
    # P is 55000.00, and Q is the lesser of 155000.00, 255000.00 and P: 55000.00.
    worksheet = return_bh()

    assert worksheet.get(CHART_2025_PART_1_AMOUNT_C).value == D("467145.00")
    assert worksheet.get(CHART_2025_PART_1_AMOUNT_E).value == D("367145.00")
    assert worksheet.get(CHART_2025_PART_1_AMOUNT_N).value == D("0.00")
    assert worksheet.get(CHART_2025_PART_1_AMOUNT_P).value == D("55000.00")
    assert worksheet.get(CHART_2025_PART_1_AMOUNT_Q).value == D("55000.00")


def test_chart_2025_part_2_takes_part_1s_total_as_amount_b_and_line_25400_stays_at_155000() -> None:
    # Part 2: A 625000.00 less B (Part 1's P, 55000.00) is C, 570000.00, and E is 470000.00 (D
    # 100000.00). F is 350000, the other amounts 0, so K is 175000.00 and M is 175000.00; N is the
    # lesser of E and M, 175000.00. O is B, 55000.00, so P is 230000.00, and Q is the lesser of
    # 155000.00, 255000.00 and P: 155000.00. The reserves are inside that cap: the filer claims
    # 155000, so line 25400 is 155000.00.
    worksheet = return_bh()

    assert worksheet.get(CHART_2025_PART_2_AMOUNT_C).value == D("570000.00")
    assert worksheet.get(CHART_2025_PART_2_AMOUNT_E).value == D("470000.00")
    assert worksheet.get(CHART_2025_PART_2_AMOUNT_N).value == D("175000.00")
    assert worksheet.get(CHART_2025_PART_2_AMOUNT_P).value == D("230000.00")
    assert worksheet.get(CHART_2025_PART_2_AMOUNT_Q).value == D("155000.00")
    assert worksheet.get(ANNUAL_GAINS_LIMIT_2025).value == D("155000.00")
    assert worksheet.get(CAPITAL_GAINS_DEDUCTION).value == D("155000")


def test_reserves_in_2021_and_2023_carry_the_2021_total_into_2022_2023_and_onward() -> None:
    # A 2023 QSBCS reserve of 20000 (Form T2017 line 12) on Chart 2023 Part 1: Chart 2022 carries
    # its total of 20000.00 into Chart 2023 (C is 465595.00); Chart 2023 F plus G is 20000, H is
    # 10000.00, J is 10000.00, K is 10000.00, and M is K plus B, 30000.00, so Chart 2023 carries
    # 30000.00 into Period 1 of 2024 (C is 478418.00, and N is 50000.00). Period 2 takes 50000.00
    # (C 575000.00, N 65000.00), and Chart 2025 Part 1 and Part 2 take 65000.00 (Part 1 P and
    # Part 2 P: 65000.00 and 240000.00, line 25400 stays at 155000.00).
    worksheet = return_bh(t657_chart_2023_amount_g="20000")

    assert worksheet.get(CHART_2022_TOTAL_CARRIED).value == D("20000.00")
    assert worksheet.get(CHART_2023_PART_1_AMOUNT_C).value == D("465595.00")
    assert worksheet.get(CHART_2023_TOTAL_CARRIED).value == D("30000.00")
    assert worksheet.get(CHART_2024_PERIOD_1_AMOUNT_N).value == D("50000.00")
    assert worksheet.get(CHART_2024_PERIOD_2_AMOUNT_N).value == D("65000.00")
    assert worksheet.get(CHART_2025_PART_1_AMOUNT_P).value == D("65000.00")
    assert worksheet.get(CHART_2025_PART_2_AMOUNT_P).value == D("240000.00")
    assert worksheet.get(CAPITAL_GAINS_DEDUCTION).value == D("155000")


def test_part_2_of_2022_applies_with_a_qffp_reserve_and_replaces_part_1s_m_as_the_total() -> None:
    # A 2022 QFFP reserve of 40000 (Form T2017 line 6) on Chart 2022 Part 1 and Part 2, with the
    # additional deduction claimed (count 1), and Chart 2 line 18 of 400000 so that amount E is
    # within the limits. Part 1: C 436815.00, E 36815.00, F 40000 gives H 20000.00, K 20000.00 and
    # M 40000.00. Part 2: C 460000.00, E 60000.00; F is 20000.00 (40000 times 1/2), H 20000.00, I
    # 20000.00 and K 60000.00; L is the lesser of H and K: 20000.00. Part 1 E (36815.00) is within
    # the annual limit, the cumulative limit and amount M (40000.00), so Part 2 applies, and its
    # L replaces Part 1's M as the total carried into Chart 2023 (20000.00, not 40000.00).
    worksheet = return_bh(
        t657_chart_2_line_18="400000",
        t657_chart_2022_amount_f="40000",
        t657_chart_2022_claims_additional_deduction=1,
    )

    assert worksheet.get(CHART_2022_PART_1_AMOUNT_E).value == D("36815.00")
    assert worksheet.get(CHART_2022_PART_1_AMOUNT_M).value == D("40000.00")
    assert worksheet.get(CHART_2022_PART_2_AMOUNT_L).value == D("20000.00")
    assert worksheet.get(CHART_2022_PART_2_APPLIES).value == 1
    assert worksheet.get(CHART_2022_TOTAL_CARRIED).value == D("20000.00")
    assert worksheet.get(CHART_2023_PART_1_AMOUNT_M).value == D("20000.00")


def test_part_2_of_2022_with_no_additional_deduction_carries_part_1s_m() -> None:
    # The same 2022 reserve and Chart 2 line 18 of 400000, with the additional deduction not
    # claimed (count 0): the gate is 0, so Part 2 is not completed and the total carried is Part
    # 1's M, 40000.00, although Part 2's L is computed (20000.00).
    worksheet = return_bh(t657_chart_2_line_18="400000", t657_chart_2022_amount_f="40000")

    assert worksheet.get(CHART_2022_PART_2_AMOUNT_L).value == D("20000.00")
    assert worksheet.get(CHART_2022_PART_2_APPLIES).value == 0
    assert worksheet.get(CHART_2022_TOTAL_CARRIED).value == D("40000.00")
    assert worksheet.get(CHART_2023_PART_1_AMOUNT_M).value == D("40000.00")


def test_part_2_of_2022_is_refused_when_part_1_e_exceeds_the_annual_limit() -> None:
    # The same 2022 QFFP reserve and the additional deduction claimed, but Chart 2 line 18 is
    # 100000: amount E of Part 1 is 336815.00, more than the annual gains limit of 155000.00, so
    # Part 2 is not completed and the total carried is Part 1's M, 40000.00.
    worksheet = return_bh(
        t657_chart_2022_amount_f="40000", t657_chart_2022_claims_additional_deduction=1
    )

    assert worksheet.get(CHART_2022_PART_1_AMOUNT_E).value == D("336815.00")
    assert worksheet.get(CHART_2022_PART_2_APPLIES).value == 0
    assert worksheet.get(CHART_2022_TOTAL_CARRIED).value == D("40000.00")
    assert worksheet.get(CHART_2023_PART_1_AMOUNT_M).value == D("40000.00")


def test_uses_d_instead_takes_the_callers_amount_at_amount_d_of_chart_2021() -> None:
    # Chart 2021 D is the caller's 30000.00 (uses_d_instead 1) rather than Chart 2 line 19 (100000),
    # so E is 416109.00 (446109.00 less 30000.00); Part 2's E is 450000.00 (480000.00 less
    # 30000.00).
    # The total carried is unchanged, 20000.00, because the other charts read the same figures.
    worksheet = return_bh(
        t657_chart_2021_uses_d_instead=1,
        t657_chart_2021_amount_d_instead="30000",
    )

    assert worksheet.get(CHART_2021_AMOUNT_D).value == D("30000.00")
    assert worksheet.get(CHART_2021_PART_1_AMOUNT_E).value == D("416109.00")
    assert worksheet.get(CHART_2021_PART_2_AMOUNT_E).value == D("450000.00")
    assert worksheet.get(CHART_2021_TOTAL_CARRIED).value == D("20000.00")
    assert worksheet.get(CHART_2024_PERIOD_1_AMOUNT_N).value == D("40000.00")
