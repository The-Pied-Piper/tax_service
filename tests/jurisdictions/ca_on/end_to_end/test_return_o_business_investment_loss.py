"""CA-ON 2025 end to end: return o business investment loss."""

from __future__ import annotations

import pytest

from app.adapters.inbound.trace_english import EnglishTraceRenderer
from app.jurisdictions.ca.catalog import (
    ALLOWABLE_BUSINESS_INVESTMENT_LOSS,
    BUSINESS_INVESTMENT_LOSS_AFTER_REDUCTION,
    BUSINESS_INVESTMENT_LOSS_REDUCTION,
    BUSINESS_INVESTMENT_LOSS_REDUCTION_AVAILABLE,
    CAPITAL_GAINS_DEDUCTIONS_CLAIMED_1985_TO_2024,
    DEDUCTIONS_FROM_TOTAL_INCOME,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_2024,
)
from tests.jurisdictions.ca_on.end_to_end.support import D, step_3


@pytest.mark.parametrize(
    ("gains_deductions", "other_reductions", "line_15", "line_17", "line_18", "line_20"),
    [
        # No capital gains deduction in earlier years: the whole loss of 10000 is reduced by
        # nothing, and 50% of it is deductible.
        ("0", "0", "0", "0", "10000", "5000.00"),
        # Line 15 of 4000 and a loss of 10000 give line 17 of 4000 and line 21700 of 3000.00.
        ("4000", "0", "4000", "4000", "6000", "3000.00"),
        # Line 7 is 6000 and line 14 is 2000 (the 2024 amounts of Schedule 3): line 15 is 4000.
        ("6000", "2000", "4000", "4000", "6000", "3000.00"),
        # Line 15 above the loss: line 17 is the loss itself, so nothing is left to deduct.
        ("12000", "0", "12000", "10000", "0", "0.00"),
        # Line 15 equal to the loss.
        ("10000", "0", "10000", "10000", "0", "0.00"),
    ],
)
def test_the_business_investment_loss_is_reduced_by_the_earlier_gains_deductions_then_halved(
    gains_deductions: str,
    other_reductions: str,
    line_15: str,
    line_17: str,
    line_18: str,
    line_20: str,
) -> None:
    # Form T1436 line 21700: line 15 "Line 7 minus line 14"; line 16 the loss in 2025; line 17
    # "Enter whichever is less: amount from line 15 or line 16."; line 18 "Line 16 minus line
    # 17"; line 20 "Line 18 multiplied by the percentage on line 19" (50 %).
    worksheet = step_3(
        capital_gains_deductions_2001_to_2024=gains_deductions,
        other_business_investment_loss_reductions_2024=other_reductions,
        business_investment_loss="10000",
    )

    assert worksheet.get(BUSINESS_INVESTMENT_LOSS_REDUCTION_AVAILABLE).value == D(line_15)
    assert worksheet.get(BUSINESS_INVESTMENT_LOSS_REDUCTION).value == D(line_17)
    assert worksheet.get(BUSINESS_INVESTMENT_LOSS_AFTER_REDUCTION).value == D(line_18)
    assert worksheet.get(ALLOWABLE_BUSINESS_INVESTMENT_LOSS).value == D(line_20)
    assert worksheet.get(DEDUCTIONS_FROM_TOTAL_INCOME).value == D(line_20)


def test_a_line_15_of_4000_renders_the_reduction_lines_of_the_trace() -> None:
    # Line 15 of 4000 (line 6, the 2001 to 2024 deductions) and a loss of 10000.
    worksheet = step_3(
        capital_gains_deductions_2001_to_2024="4000", business_investment_loss="10000"
    )

    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "business_investment_loss_reduction: lesser of "
        "business_investment_loss_reduction_available 4000 and business_investment_loss 10000 "
        "= 4000"
    ) in rendered
    assert (
        "business_investment_loss_after_reduction: business_investment_loss 10000 "
        "less business_investment_loss_reduction 4000 = 6000"
    ) in rendered
    assert (
        "allowable_business_investment_loss: 50% of business_investment_loss_after_reduction "
        "6000 (half-up to 0.01)"
    ) in rendered


def test_t1436_line_15_goes_negative_when_line_14_exceeds_line_7() -> None:
    # Form T1436 line 15 "Line 7 minus line 14" prints no "(if negative, enter "0")", and line 17
    # "Enter whichever is less: amount from line 15 or line 16." prints no floor either, so the
    # lines follow the form as printed: line 7 of 0 and line 14 of 2000 give line 15 of -2000,
    # line 17 of -2000 (the lesser of -2000 and 10000), line 18 of 10000 - (-2000) = 12000 and
    # line 21700 of 12000 x 50% = 6000.00, more than half of the loss of 10000. The form states
    # no treatment of this case, so this records the printed arithmetic, not a confirmed one.
    worksheet = step_3(
        other_business_investment_loss_reductions_2024="2000", business_investment_loss="10000"
    )

    assert worksheet.get(BUSINESS_INVESTMENT_LOSS_REDUCTION_AVAILABLE).value == D("-2000")
    assert worksheet.get(BUSINESS_INVESTMENT_LOSS_REDUCTION).value == D("-2000")
    assert worksheet.get(BUSINESS_INVESTMENT_LOSS_AFTER_REDUCTION).value == D("12000")
    assert worksheet.get(ALLOWABLE_BUSINESS_INVESTMENT_LOSS).value == D("6000.00")
    assert worksheet.get(DEDUCTIONS_FROM_TOTAL_INCOME).value == D("6000.00")


def test_t1436_lines_7_and_14_add_lines_1_to_6_and_8_to_13_once_each() -> None:
    # Line 7 "Add lines 1 to 6." and line 14 "Add lines 8 to 13.": one distinct power of two for
    # each of the twelve lines, so a line left out or added twice changes the sums: 1 + 2 + 4 + 8
    # + 16 + 32 = 63 and 64 + 128 + 256 + 512 + 1024 + 2048 = 4032. Line 15, "Line 7 minus line
    # 14", is -3969: the form prints no "(if negative, enter "0")".
    worksheet = step_3(
        capital_gains_deductions_1985_to_1987="1",
        capital_gains_deductions_1988_and_1989_other_than_eligible_capital_property="2",
        capital_gains_deductions_1988_and_1989_eligible_capital_property="4",
        capital_gains_deductions_1990_to_1999="8",
        capital_gains_deductions_2000="16",
        capital_gains_deductions_2001_to_2024="32",
        other_business_investment_loss_reductions_1986_to_1994="64",
        other_business_investment_loss_reductions_1994_to_1996="128",
        other_business_investment_loss_reductions_1997_to_1999="256",
        other_business_investment_loss_reductions_2000="512",
        other_business_investment_loss_reductions_2001_to_2023="1024",
        other_business_investment_loss_reductions_2024="2048",
    )

    assert worksheet.get(CAPITAL_GAINS_DEDUCTIONS_CLAIMED_1985_TO_2024).value == D("63")
    assert worksheet.get(OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_2024).value == D("4032")
    assert worksheet.get(BUSINESS_INVESTMENT_LOSS_REDUCTION_AVAILABLE).value == D("-3969")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "capital_gains_deductions_claimed_1985_to_2024: capital_gains_deductions_1985_to_1987 1 "
        "+ capital_gains_deductions_1988_and_1989_other_than_eligible_capital_property 2 "
        "+ capital_gains_deductions_1988_and_1989_eligible_capital_property 4 "
        "+ capital_gains_deductions_1990_to_1999 8 + capital_gains_deductions_2000 16 "
        "+ capital_gains_deductions_2001_to_2024 32 = 63"
    ) in rendered
    assert (
        "other_business_investment_loss_reductions_1986_to_2024: "
        "other_business_investment_loss_reductions_1986_to_1994 64 "
        "+ other_business_investment_loss_reductions_1994_to_1996 128 "
        "+ other_business_investment_loss_reductions_1997_to_1999 256 "
        "+ other_business_investment_loss_reductions_2000 512 "
        "+ other_business_investment_loss_reductions_2001_to_2023 1024 "
        "+ other_business_investment_loss_reductions_2024 2048 = 4032"
    ) in rendered
    assert (
        "business_investment_loss_reduction_available: "
        "capital_gains_deductions_claimed_1985_to_2024 63 "
        "less other_business_investment_loss_reductions_1986_to_2024 4032 = -3969"
    ) in rendered


def test_line_15_may_be_negative_as_the_form_prints_no_floor() -> None:
    # Other reductions (line 14) of 500 and no capital gains deductions (line 7): line 15 is -500,
    # and line 17 "Enter whichever is less: amount from line 15 or line 16." is -500 too, so line 18
    # "Line 16 minus line 17" is 10000 + 500 = 10500 and line 20 is 5250.00. The form prints no
    # floor on lines 15 and 17, so the kinds are signed and the result follows the printed lines.
    worksheet = step_3(
        other_business_investment_loss_reductions_2024="500", business_investment_loss="10000"
    )

    assert worksheet.get(BUSINESS_INVESTMENT_LOSS_REDUCTION_AVAILABLE).value == D("-500")
    assert worksheet.get(BUSINESS_INVESTMENT_LOSS_REDUCTION).value == D("-500")
    assert worksheet.get(BUSINESS_INVESTMENT_LOSS_AFTER_REDUCTION).value == D("10500")
    assert worksheet.get(ALLOWABLE_BUSINESS_INVESTMENT_LOSS).value == D("5250.00")


def test_the_allowable_business_investment_loss_is_rounded_half_up_to_the_cent() -> None:
    # Line 20 is a dollars-and-cents box: 10000.01 x 50% = 5000.005, a tie, up to 5000.01.
    worksheet = step_3(business_investment_loss="10000.01")

    assert worksheet.get(ALLOWABLE_BUSINESS_INVESTMENT_LOSS).value == D("5000.01")


def test_a_loss_of_0_gives_an_allowable_loss_of_0() -> None:
    worksheet = step_3()

    assert worksheet.get(ALLOWABLE_BUSINESS_INVESTMENT_LOSS).value == D("0")
