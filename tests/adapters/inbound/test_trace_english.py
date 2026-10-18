"""Unit tests for EnglishTraceRenderer: structured trace lines as English text, made-up values.

The renderer reproduces the trace text capabilities used to compose themselves, so the move to
structured lines changes only the structure. Rates print as percentages, `(rate * 100)` normalised
in fixed-point notation; money figures print the same way, normalised in fixed-point notation, so
no figure carries trailing zeros after the decimal point or an exponent (the value is untouched;
only its text changes); rounding rules print as "no rounding" or "<mode> to <increment>".
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

import pytest

from app.adapters.inbound.trace_english import EnglishTraceRenderer
from app.domain.artifact import ArtifactKind
from app.domain.parameters.amount import Amount
from app.domain.parameters.contribution_tier import ContributionTier
from app.domain.parameters.credit import Credit
from app.domain.parameters.factor import Factor
from app.domain.parameters.fraction import Fraction
from app.domain.parameters.rate import Rate
from app.domain.parameters.rounding import NO_ROUNDING, RoundingMode, RoundingRule, RoundTo
from app.domain.parameters.taper import Taper
from app.domain.trace import (
    AtMostLine,
    BracketColumnLine,
    CappedAmountLine,
    ContributionTierLine,
    CreditAmountLine,
    FractionAppliedLine,
    LesserOfLine,
    MultipleOverLine,
    PerUnitAmountLine,
    RateAppliedLine,
    RoundedTotalLine,
    SubtractedLine,
    SubtractedNotBelowZeroLine,
    SumLine,
    SurchargeTierLine,
    TaperedAmountLine,
    TimesCountLine,
    TraceLine,
)

D = Decimal
CENT = RoundTo(D("0.01"), RoundingMode.HALF_UP)

TAXABLE_BASE = ArtifactKind("ex/taxable_base", Decimal)
BASIC_TAX = ArtifactKind("ex/basic_tax", Decimal)
PART_ONE = ArtifactKind("ex/part_one", Decimal)
PART_TWO = ArtifactKind("ex/part_two", Decimal)
PART_THREE = ArtifactKind("ex/part_three", Decimal)
TOTAL = ArtifactKind("ex/total", Decimal)
GROSS_AMOUNT = ArtifactKind("ex/gross_amount", Decimal)
RATED_AMOUNT = ArtifactKind("ex/rated_amount", Decimal)
REDUCTION = ArtifactKind("ex/reduction", Decimal)
NET_AMOUNT = ArtifactKind("ex/net_amount", Decimal)
PERSONAL_AMOUNT = ArtifactKind("ex/personal_amount", Decimal)
CAPPED_AMOUNT = ArtifactKind("ex/capped_amount", Decimal)
LESSER_AMOUNT = ArtifactKind("ex/lesser_amount", Decimal)
EARNINGS = ArtifactKind("ex/earnings", Decimal)
CONTRIBUTION = ArtifactKind("ex/contribution", Decimal)
TIER = ContributionTier(Rate(D("0.05")), D("3000"), D("50000"), D("2350"))
SURCHARGE = ArtifactKind("ex/surcharge", Decimal)
TAX_SO_FAR = ArtifactKind("ex/tax_so_far", Decimal)
INCOME = ArtifactKind("ex/income", Decimal)
TAPER = Taper(D("1000"), D("500"), D("20000"), D("10000"))
CHILDREN = ArtifactKind("ex/child_count", int)
CHILD_AMOUNT = ArtifactKind("ex/child_amount", Decimal)
REDUCTION_AMOUNTS = ArtifactKind("ex/reduction_amounts", Decimal)
CLAIMED_AMOUNT = ArtifactKind("ex/claimed_amount", Decimal)
CLAIM_LIMIT = ArtifactKind("ex/claim_limit", Decimal)
ALLOWED_AMOUNT = ArtifactKind("ex/allowed_amount", Decimal)
EARNED_INCOME = ArtifactKind("ex/earned_income", Decimal)
EARNED_PORTION = ArtifactKind("ex/earned_portion", Decimal)
AMOUNT_EACH = ArtifactKind("ex/amount_each", Decimal)
PERSONS = ArtifactKind("ex/person_count", int)
AMOUNT_CLAIMED = ArtifactKind("ex/amount_claimed", Decimal)


def render(line: TraceLine) -> str:
    return EnglishTraceRenderer().render(line)


# --- bracket columns -------------------------------------------------------------
#
# One line for the bracket the base falls in, read like the form's column: the rate on the
# excess over the bracket's lower, plus the bracket's printed constant.


def test_renders_the_bracket_the_base_falls_in() -> None:
    line = BracketColumnLine(D(100), D("0.20"), D(150), D("10.00"), D("40.00"))

    assert render(line) == "20% on 150 over 100 plus 10"


def test_renders_a_constant_with_its_cents() -> None:
    line = BracketColumnLine(D(105), D("0.205"), D("45.00"), D("11.03"), D("20.255"))

    assert render(line) == "20.5% on 45 over 105 plus 11.03"


def test_renders_the_first_bracket_over_zero_plus_zero() -> None:
    line = BracketColumnLine(D(0), D("0.10"), D(100), D(0), D("10.0"))

    assert render(line) == "10% on 100 over 0 plus 0"


def test_renders_the_open_top_bracket_like_any_other() -> None:
    line = BracketColumnLine(D(300), D("0.30"), D(100), D("50.00"), D("80.00"))

    assert render(line) == "30% on 100 over 300 plus 50"


@pytest.mark.parametrize(
    ("rate", "percent"),
    [
        ("0.10", "10"),
        ("0.1", "10"),
        ("0.125", "12.5"),
        ("0.0505", "5.05"),
        ("0", "0"),
        ("1", "100"),
    ],
)
def test_renders_the_rate_as_a_plain_percentage(rate: str, percent: str) -> None:
    line = BracketColumnLine(D(0), D(rate), D(100), D(0), D(0))

    assert render(line) == f"{percent}% on 100 over 0 plus 0"


# --- rounded totals --------------------------------------------------------------


def test_renders_a_rounded_total() -> None:
    line = RoundedTotalLine(BASIC_TAX, TAXABLE_BASE, D(250), CENT, D("40.00"))

    assert render(line) == "basic_tax on taxable_base 250 (half-up to 0.01)"


def test_renders_a_total_without_rounding() -> None:
    line = RoundedTotalLine(BASIC_TAX, TAXABLE_BASE, D(400), NO_ROUNDING, D("80.0"))

    assert render(line) == "basic_tax on taxable_base 400 (no rounding)"


@pytest.mark.parametrize(
    ("rounding", "text"),
    [
        (NO_ROUNDING, "no rounding"),
        (CENT, "half-up to 0.01"),
        (RoundTo(D("1"), RoundingMode.FLOOR), "floor to 1"),
        (RoundTo(D("0.05"), RoundingMode.HALF_EVEN), "half-even to 0.05"),
        (RoundTo(D("0.01"), RoundingMode.DOWN), "down to 0.01"),
        (RoundTo(D("0.01"), RoundingMode.UP), "up to 0.01"),
        (RoundTo(D("0.01"), RoundingMode.CEILING), "ceiling to 0.01"),
    ],
)
def test_renders_each_rounding_rule(rounding: RoundingRule, text: str) -> None:
    line = RoundedTotalLine(BASIC_TAX, TAXABLE_BASE, D(250), rounding, D(25))

    assert render(line) == f"basic_tax on taxable_base 250 ({text})"


# --- sums ------------------------------------------------------------------------


def test_renders_a_sum_of_three_parts() -> None:
    line = SumLine(
        TOTAL,
        ((PART_ONE, D("100.25")), (PART_TWO, D("40")), (PART_THREE, D("9.75"))),
        D("150.00"),
    )

    assert render(line) == "total: part_one 100.25 + part_two 40 + part_three 9.75 = 150"


def test_renders_the_parts_in_the_order_of_the_line() -> None:
    line = SumLine(TOTAL, ((PART_THREE, D("9.75")), (PART_ONE, D("100.25"))), D("110.00"))

    assert render(line) == "total: part_three 9.75 + part_one 100.25 = 110"


def test_renders_a_sum_of_one_part() -> None:
    line = SumLine(TOTAL, ((PART_TWO, D("40.5")),), D("40.5"))

    assert render(line) == "total: part_two 40.5 = 40.5"


def test_renders_a_sum_of_no_parts() -> None:
    assert render(SumLine(TOTAL, (), D(0))) == "total: no parts = 0"


# --- rates applied --------------------------------------------------------------


def test_renders_a_rate_applied_without_rounding() -> None:
    line = RateAppliedLine(
        RATED_AMOUNT, GROSS_AMOUNT, D("1000.05"), Rate(D("0.125")), NO_ROUNDING, D("125.00625")
    )

    assert render(line) == "rated_amount: 12.5% of gross_amount 1000.05 (no rounding)"


def test_renders_a_rounded_rate_applied() -> None:
    line = RateAppliedLine(
        RATED_AMOUNT, GROSS_AMOUNT, D("200.01"), Rate(D("0.5")), CENT, D("100.01")
    )

    assert render(line) == "rated_amount: 50% of gross_amount 200.01 (half-up to 0.01)"


@pytest.mark.parametrize(("rate", "percent"), [("0", "0"), ("1", "100"), ("0.0505", "5.05")])
def test_renders_the_applied_rate_as_a_plain_percentage(rate: str, percent: str) -> None:
    line = RateAppliedLine(RATED_AMOUNT, GROSS_AMOUNT, D("40"), Rate(D(rate)), NO_ROUNDING, D(0))

    assert render(line) == f"rated_amount: {percent}% of gross_amount 40 (no rounding)"


# --- subtractions ---------------------------------------------------------------


def test_renders_a_subtraction() -> None:
    line = SubtractedLine(NET_AMOUNT, GROSS_AMOUNT, D("100.25"), REDUCTION, D("40"), D("60.25"))

    assert render(line) == "net_amount: gross_amount 100.25 less reduction 40 = 60.25"


def test_renders_a_subtraction_with_a_negative_result() -> None:
    line = SubtractedLine(NET_AMOUNT, GROSS_AMOUNT, D("10"), REDUCTION, D("25.5"), D("-15.5"))

    assert render(line) == "net_amount: gross_amount 10 less reduction 25.5 = -15.5"


def test_renders_a_subtraction_to_zero() -> None:
    line = SubtractedLine(NET_AMOUNT, GROSS_AMOUNT, D("40.50"), REDUCTION, D("40.50"), D("0.00"))

    assert render(line) == "net_amount: gross_amount 40.5 less reduction 40.5 = 0"


# --- subtractions not below zero ---------------------------------------------------------


def test_renders_a_subtraction_not_below_zero() -> None:
    line = SubtractedNotBelowZeroLine(
        NET_AMOUNT, GROSS_AMOUNT, D("100.25"), REDUCTION, D("40"), D("60.25")
    )

    assert render(line) == "net_amount: gross_amount 100.25 less reduction 40, not below 0 = 60.25"


def test_renders_a_subtraction_floored_at_zero() -> None:
    line = SubtractedNotBelowZeroLine(
        NET_AMOUNT, GROSS_AMOUNT, D("10"), REDUCTION, D("25.5"), D("0")
    )

    assert render(line) == "net_amount: gross_amount 10 less reduction 25.5, not below 0 = 0"


def test_renders_a_subtraction_not_below_zero_to_exactly_zero() -> None:
    line = SubtractedNotBelowZeroLine(
        NET_AMOUNT, GROSS_AMOUNT, D("40.50"), REDUCTION, D("40.50"), D("0")
    )

    assert render(line) == "net_amount: gross_amount 40.5 less reduction 40.5, not below 0 = 0"


# --- credit amounts ------------------------------------------------------------------------


def test_renders_a_credit_amount_without_rounding() -> None:
    line = CreditAmountLine(PERSONAL_AMOUNT, Credit(D("1000.005")), NO_ROUNDING, D("1000.005"))

    assert render(line) == "personal_amount: credit amount 1000.005 (no rounding)"


def test_renders_a_rounded_credit_amount() -> None:
    line = CreditAmountLine(PERSONAL_AMOUNT, Credit(D("1000.005")), CENT, D("1000.01"))

    assert render(line) == "personal_amount: credit amount 1000.005 (half-up to 0.01)"


def test_renders_the_credit_amount_with_another_rounding_rule() -> None:
    line = CreditAmountLine(
        PERSONAL_AMOUNT, Credit(D("1000.99")), RoundTo(D("1"), RoundingMode.FLOOR), D("1000")
    )

    assert render(line) == "personal_amount: credit amount 1000.99 (floor to 1)"


# --- capped amounts --------------------------------------------------------------------


def test_renders_a_base_above_the_cap() -> None:
    line = CappedAmountLine(
        CAPPED_AMOUNT, GROSS_AMOUNT, D("1500.25"), Amount(D("1000")), NO_ROUNDING, D("1000")
    )

    assert render(line) == "capped_amount: lesser of gross_amount 1500.25 and 1000 (no rounding)"


def test_renders_a_base_below_the_cap() -> None:
    line = CappedAmountLine(
        CAPPED_AMOUNT, GROSS_AMOUNT, D("400.50"), Amount(D("1000")), NO_ROUNDING, D("400.50")
    )

    assert render(line) == "capped_amount: lesser of gross_amount 400.5 and 1000 (no rounding)"


def test_renders_a_rounded_capped_amount() -> None:
    line = CappedAmountLine(
        CAPPED_AMOUNT, GROSS_AMOUNT, D("400.005"), Amount(D("1000.00")), CENT, D("400.01")
    )

    assert (
        render(line) == "capped_amount: lesser of gross_amount 400.005 and 1000 (half-up to 0.01)"
    )


def test_renders_the_cap_as_given() -> None:
    line = CappedAmountLine(
        CAPPED_AMOUNT, GROSS_AMOUNT, D("0"), Amount(D("1471.5")), NO_ROUNDING, D("0")
    )

    assert render(line) == "capped_amount: lesser of gross_amount 0 and 1471.5 (no rounding)"


# --- lesser of amounts -------------------------------------------------------------------


def test_renders_the_lesser_of_two_amounts() -> None:
    line = LesserOfLine(LESSER_AMOUNT, ((PART_ONE, D("1500.25")), (PART_TWO, D("1000"))), D("1000"))

    assert render(line) == "lesser_amount: lesser of part_one 1500.25 and part_two 1000 = 1000"


def test_renders_the_lesser_of_amounts_in_the_order_of_the_line() -> None:
    line = LesserOfLine(
        LESSER_AMOUNT, ((PART_TWO, D("1000")), (PART_ONE, D("400.50"))), D("400.50")
    )

    assert render(line) == "lesser_amount: lesser of part_two 1000 and part_one 400.5 = 400.5"


def test_renders_the_lesser_of_three_amounts_with_and_between_each() -> None:
    line = LesserOfLine(
        LESSER_AMOUNT,
        ((PART_ONE, D("100.25")), (PART_TWO, D("40")), (PART_THREE, D("9.75"))),
        D("9.75"),
    )

    assert render(line) == (
        "lesser_amount: lesser of part_one 100.25 and part_two 40 and part_three 9.75 = 9.75"
    )


def test_renders_the_lesser_of_equal_amounts() -> None:
    line = LesserOfLine(LESSER_AMOUNT, ((PART_ONE, D("40.50")), (PART_TWO, D("40.5"))), D("40.50"))

    assert render(line) == "lesser_amount: lesser of part_one 40.5 and part_two 40.5 = 40.5"


def test_renders_the_lesser_of_one_amount() -> None:
    line = LesserOfLine(LESSER_AMOUNT, ((PART_TWO, D("40.5")),), D("40.5"))

    assert render(line) == "lesser_amount: lesser of part_two 40.5 = 40.5"


# --- contribution tiers ---------------------------------------------------------------


def test_renders_a_contribution_tier() -> None:
    line = ContributionTierLine(
        CONTRIBUTION, EARNINGS, D("23000"), TIER, NO_ROUNDING, D("20000"), D("1000")
    )

    assert render(line) == (
        "contribution: 5% of earnings between 3000 and 50000 (20000), at most 2350 (no rounding)"
    )


def test_renders_a_rounded_contribution_tier() -> None:
    line = ContributionTierLine(
        CONTRIBUTION, EARNINGS, D("23000.10"), TIER, CENT, D("20000.10"), D("1000.01")
    )

    assert render(line) == (
        "contribution: 5% of earnings between 3000 and 50000 (20000.1), at most 2350 "
        "(half-up to 0.01)"
    )


def test_renders_earnings_above_the_band_as_the_band() -> None:
    line = ContributionTierLine(
        CONTRIBUTION, EARNINGS, D("80000"), TIER, NO_ROUNDING, D("47000"), D("2350")
    )

    assert render(line) == (
        "contribution: 5% of earnings between 3000 and 50000 (47000), at most 2350 (no rounding)"
    )


def test_renders_zero_contributory_earnings() -> None:
    line = ContributionTierLine(CONTRIBUTION, EARNINGS, D("-500"), TIER, NO_ROUNDING, D(0), D(0))

    assert render(line) == (
        "contribution: 5% of earnings between 3000 and 50000 (0), at most 2350 (no rounding)"
    )


def test_renders_the_tiers_figures() -> None:
    tier = ContributionTier(Rate(D("0.0505")), D("2500.00"), D("61000"), D("2954.20"))
    line = ContributionTierLine(
        CONTRIBUTION, EARNINGS, D("90000"), tier, CENT, D("58500.00"), D("2954.20")
    )

    assert render(line) == (
        "contribution: 5.05% of earnings between 2500 and 61000 (58500), at most 2954.2 "
        "(half-up to 0.01)"
    )


# --- surcharge tiers -------------------------------------------------------------------


def test_renders_a_surcharge_tier() -> None:
    line = SurchargeTierLine(
        SURCHARGE, TAX_SO_FAR, D("400"), D("300"), Rate(D("0.25")), NO_ROUNDING, D("25")
    )

    assert render(line) == "surcharge: 25% of tax_so_far 400 over 300 (no rounding)"


def test_renders_a_rounded_surcharge_tier() -> None:
    line = SurchargeTierLine(
        SURCHARGE, TAX_SO_FAR, D("300.06"), D("100"), Rate(D("0.10")), CENT, D("20.01")
    )

    assert render(line) == "surcharge: 10% of tax_so_far 300.06 over 100 (half-up to 0.01)"


def test_renders_a_surcharge_tier_the_base_does_not_reach() -> None:
    line = SurchargeTierLine(
        SURCHARGE, TAX_SO_FAR, D("200"), D("300"), Rate(D("0.25")), NO_ROUNDING, D("0")
    )

    assert render(line) == "surcharge: 25% of tax_so_far 200 over 300 (no rounding)"


def test_renders_the_threshold_and_base() -> None:
    line = SurchargeTierLine(
        SURCHARGE, TAX_SO_FAR, D("1000.50"), D("1471.5"), Rate(D("0.0505")), NO_ROUNDING, D(0)
    )

    assert render(line) == "surcharge: 5.05% of tax_so_far 1000.5 over 1471.5 (no rounding)"


def test_renders_a_surcharge_tiers_maximum_before_the_rounding() -> None:
    line = SurchargeTierLine(
        SURCHARGE, TAX_SO_FAR, D("400"), D("300"), Rate(D("0.06")), NO_ROUNDING, D("6"), D("300")
    )

    assert render(line) == "surcharge: 6% of tax_so_far 400 over 300, at most 300 (no rounding)"


def test_renders_a_capped_surcharge_tier_with_its_rounding() -> None:
    line = SurchargeTierLine(
        SURCHARGE, TAX_SO_FAR, D("1000"), D("100"), Rate(D("0.10")), CENT, D("15.56"), D("15.555")
    )

    assert render(line) == (
        "surcharge: 10% of tax_so_far 1000 over 100, at most 15.555 (half-up to 0.01)"
    )


def test_renders_a_zero_maximum() -> None:
    line = SurchargeTierLine(
        SURCHARGE, TAX_SO_FAR, D("400"), D("300"), Rate(D("0.25")), NO_ROUNDING, D("0"), D("0")
    )

    assert render(line) == "surcharge: 25% of tax_so_far 400 over 300, at most 0 (no rounding)"


def test_renders_a_maximum_on_a_tier_the_base_does_not_reach() -> None:
    line = SurchargeTierLine(
        SURCHARGE, TAX_SO_FAR, D("200"), D("300"), Rate(D("0.25")), NO_ROUNDING, D("0"), D("150")
    )

    assert render(line) == "surcharge: 25% of tax_so_far 200 over 300, at most 150 (no rounding)"


@pytest.mark.parametrize(
    ("maximum", "text"),
    [
        (D("1.500E+2"), "at most 150"),
        (D("150.50"), "at most 150.5"),
        (D("0.00"), "at most 0"),
    ],
)
def test_renders_a_surcharge_tiers_maximum_without_trailing_zeros(
    maximum: Decimal, text: str
) -> None:
    line = SurchargeTierLine(
        SURCHARGE,
        TAX_SO_FAR,
        D("400.50"),
        D("3E+2"),
        Rate(D("0.25")),
        NO_ROUNDING,
        D("25"),
        maximum,
    )

    assert render(line) == f"surcharge: 25% of tax_so_far 400.5 over 300, {text} (no rounding)"


# --- tapered amounts -------------------------------------------------------------------


def test_renders_a_tapered_amount() -> None:
    line = TaperedAmountLine(
        PERSONAL_AMOUNT, INCOME, D("22000"), TAPER, NO_ROUNDING, D("100"), D("1400")
    )

    assert render(line) == (
        "personal_amount: 1000 plus 500 less 100 for income 22000 over 20000 (range 10000), "
        "not below 1000 (no rounding)"
    )


def test_renders_a_rounded_tapered_amount() -> None:
    line = TaperedAmountLine(
        PERSONAL_AMOUNT, INCOME, D("22000.5"), TAPER, CENT, D("100.025"), D("1399.98")
    )

    assert render(line) == (
        "personal_amount: 1000 plus 500 less 100.025 for income 22000.5 over 20000 "
        "(range 10000), not below 1000 (half-up to 0.01)"
    )


def test_renders_a_tapered_amount_below_the_threshold() -> None:
    line = TaperedAmountLine(
        PERSONAL_AMOUNT, INCOME, D("15000"), TAPER, NO_ROUNDING, D("0"), D("1500")
    )

    assert render(line) == (
        "personal_amount: 1000 plus 500 less 0 for income 15000 over 20000 (range 10000), "
        "not below 1000 (no rounding)"
    )


def test_renders_a_reduction_above_the_supplement_as_recorded() -> None:
    line = TaperedAmountLine(
        PERSONAL_AMOUNT, INCOME, D("80000"), TAPER, NO_ROUNDING, D("3000"), D("1000")
    )

    assert render(line) == (
        "personal_amount: 1000 plus 500 less 3000 for income 80000 over 20000 (range 10000), "
        "not below 1000 (no rounding)"
    )


def test_renders_an_inexact_reduction_with_every_digit() -> None:
    taper = Taper(D("1000"), D("500"), D("20000"), D("7000"))
    line = TaperedAmountLine(
        PERSONAL_AMOUNT,
        INCOME,
        D("21000"),
        taper,
        CENT,
        D("71.42857142857142857142857143"),
        D("1428.57"),
    )

    assert render(line) == (
        "personal_amount: 1000 plus 500 less 71.42857142857142857142857143 for income 21000 "
        "over 20000 (range 7000), not below 1000 (half-up to 0.01)"
    )


# --- per-unit amounts ------------------------------------------------------------------


def test_renders_a_per_unit_amount() -> None:
    line = PerUnitAmountLine(CHILD_AMOUNT, CHILDREN, 2, Amount(D("544")), NO_ROUNDING, D("1088"))

    assert render(line) == "child_amount: 544 for each of 2 child_count = 1088 (no rounding)"


def test_renders_a_per_unit_amount_for_one_unit() -> None:
    line = PerUnitAmountLine(CHILD_AMOUNT, CHILDREN, 1, Amount(D("544")), NO_ROUNDING, D("544"))

    assert render(line) == "child_amount: 544 for each of 1 child_count = 544 (no rounding)"


def test_renders_a_per_unit_amount_for_no_units() -> None:
    line = PerUnitAmountLine(CHILD_AMOUNT, CHILDREN, 0, Amount(D("544")), NO_ROUNDING, D("0"))

    assert render(line) == "child_amount: 544 for each of 0 child_count = 0 (no rounding)"


def test_renders_a_fractional_per_unit_amount() -> None:
    line = PerUnitAmountLine(CHILD_AMOUNT, CHILDREN, 3, Amount(D("0.333")), NO_ROUNDING, D("0.999"))

    assert render(line) == "child_amount: 0.333 for each of 3 child_count = 0.999 (no rounding)"


def test_renders_a_rounded_per_unit_amount() -> None:
    line = PerUnitAmountLine(CHILD_AMOUNT, CHILDREN, 3, Amount(D("0.333")), CENT, D("1.00"))

    assert render(line) == "child_amount: 0.333 for each of 3 child_count = 1 (half-up to 0.01)"


# --- multiples over a figure -----------------------------------------------------------


def test_renders_a_multiple_over_a_figure() -> None:
    line = MultipleOverLine(
        REDUCTION,
        REDUCTION_AMOUNTS,
        D("294"),
        Factor(D("2")),
        TAX_SO_FAR,
        D("8195.7644476"),
        NO_ROUNDING,
        D("0"),
    )

    assert render(line) == (
        "reduction: 2 × reduction_amounts 294 over tax_so_far 8195.7644476, not below 0 "
        "(no rounding)"
    )


def test_renders_a_multiple_above_the_figure() -> None:
    line = MultipleOverLine(
        REDUCTION,
        REDUCTION_AMOUNTS,
        D("294"),
        Factor(D("2")),
        TAX_SO_FAR,
        D("100"),
        NO_ROUNDING,
        D("488"),
    )

    assert render(line) == (
        "reduction: 2 × reduction_amounts 294 over tax_so_far 100, not below 0 (no rounding)"
    )


def test_renders_a_rounded_multiple_over_a_figure() -> None:
    line = MultipleOverLine(
        REDUCTION,
        REDUCTION_AMOUNTS,
        D("294.005"),
        Factor(D("2")),
        TAX_SO_FAR,
        D("0.0001"),
        CENT,
        D("588.01"),
    )

    assert render(line) == (
        "reduction: 2 × reduction_amounts 294.005 over tax_so_far 0.0001, not below 0 "
        "(half-up to 0.01)"
    )


def test_renders_a_fractional_factor() -> None:
    line = MultipleOverLine(
        REDUCTION,
        REDUCTION_AMOUNTS,
        D("294"),
        Factor(D("2.5")),
        TAX_SO_FAR,
        D("100.5"),
        NO_ROUNDING,
        D("634.5"),
    )

    assert render(line) == (
        "reduction: 2.5 × reduction_amounts 294 over tax_so_far 100.5, not below 0 (no rounding)"
    )


# --- amounts at most a bound ----------------------------------------------------------


def test_renders_an_amount_at_most_a_bound() -> None:
    line = AtMostLine(ALLOWED_AMOUNT, CLAIMED_AMOUNT, D("1500.25"), CLAIM_LIMIT, D("1926"))

    assert render(line) == "allowed_amount: claimed_amount 1500.25, at most claim_limit 1926"


def test_renders_an_amount_equal_to_its_bound() -> None:
    line = AtMostLine(ALLOWED_AMOUNT, CLAIMED_AMOUNT, D("1926"), CLAIM_LIMIT, D("1926"))

    assert render(line) == "allowed_amount: claimed_amount 1926, at most claim_limit 1926"


def test_renders_a_zero_amount_at_most_a_zero_bound() -> None:
    line = AtMostLine(ALLOWED_AMOUNT, CLAIMED_AMOUNT, D("0"), CLAIM_LIMIT, D("0"))

    assert render(line) == "allowed_amount: claimed_amount 0, at most claim_limit 0"


def test_renders_an_amount_at_most_a_bound_with_every_digit() -> None:
    line = AtMostLine(ALLOWED_AMOUNT, CLAIMED_AMOUNT, D("0.0049"), CLAIM_LIMIT, D("0.005"))

    assert render(line) == "allowed_amount: claimed_amount 0.0049, at most claim_limit 0.005"


# --- fractions applied -----------------------------------------------------------------
#
# The fraction prints as its two whole parts, "<numerator>/<denominator>", as given.


def test_renders_a_fraction_applied_without_rounding() -> None:
    line = FractionAppliedLine(
        EARNED_PORTION, EARNED_INCOME, D("60000"), Fraction(2, 3), NO_ROUNDING, D("40000")
    )

    assert render(line) == "earned_portion: 2/3 of earned_income 60000 (no rounding)"


def test_renders_a_rounded_fraction_applied() -> None:
    line = FractionAppliedLine(
        EARNED_PORTION, EARNED_INCOME, D("50000"), Fraction(2, 3), CENT, D("33333.33")
    )

    assert render(line) == "earned_portion: 2/3 of earned_income 50000 (half-up to 0.01)"


def test_renders_an_unrounded_inexact_fraction_applied() -> None:
    line = FractionAppliedLine(
        EARNED_PORTION,
        EARNED_INCOME,
        D("50000"),
        Fraction(2, 3),
        NO_ROUNDING,
        D("33333.33333333333333333333333"),
    )

    assert render(line) == "earned_portion: 2/3 of earned_income 50000 (no rounding)"


@pytest.mark.parametrize(
    ("numerator", "denominator", "text"), [(1, 1, "1/1"), (3, 2, "3/2"), (4, 6, "4/6")]
)
def test_renders_the_fraction_as_given(numerator: int, denominator: int, text: str) -> None:
    line = FractionAppliedLine(
        EARNED_PORTION,
        EARNED_INCOME,
        D("120"),
        Fraction(numerator, denominator),
        NO_ROUNDING,
        D("0"),
    )

    assert render(line) == f"earned_portion: {text} of earned_income 120 (no rounding)"


# --- amounts times a count -------------------------------------------------------------
#
# The amount is an artifact, so it prints with its label, unlike a per-unit amount's dataset
# figure; there is no rounding rule to print.


def test_renders_an_amount_times_a_count_of_one() -> None:
    line = TimesCountLine(AMOUNT_CLAIMED, AMOUNT_EACH, D("16129"), PERSONS, 1, D("16129"))

    assert render(line) == "amount_claimed: amount_each 16129 for each of 1 person_count = 16129"


def test_renders_an_amount_times_a_count_of_two() -> None:
    line = TimesCountLine(AMOUNT_CLAIMED, AMOUNT_EACH, D("16129"), PERSONS, 2, D("32258"))

    assert render(line) == "amount_claimed: amount_each 16129 for each of 2 person_count = 32258"


def test_renders_an_amount_times_a_count_of_zero() -> None:
    line = TimesCountLine(AMOUNT_CLAIMED, AMOUNT_EACH, D("16129"), PERSONS, 0, D("0"))

    assert render(line) == "amount_claimed: amount_each 16129 for each of 0 person_count = 0"


def test_renders_an_amount_times_a_count_with_every_digit() -> None:
    line = TimesCountLine(AMOUNT_CLAIMED, AMOUNT_EACH, D("0.333"), PERSONS, 3, D("0.999"))

    assert render(line) == "amount_claimed: amount_each 0.333 for each of 3 person_count = 0.999"


def test_renders_a_negative_amount_times_a_count() -> None:
    line = TimesCountLine(AMOUNT_CLAIMED, AMOUNT_EACH, D("-250.75"), PERSONS, 2, D("-501.50"))

    assert render(line) == (
        "amount_claimed: amount_each -250.75 for each of 2 person_count = -501.5"
    )


# --- money figures ---------------------------------------------------------------


@pytest.mark.parametrize(
    ("figure", "text"),
    [
        (D("20146.2500"), "20146.25"),
        (D("115000.00"), "115000"),
        (D("0.00"), "0"),
        (D("8539.5965"), "8539.5965"),
        (D("1.15E+5"), "115000"),
        (D("115000"), "115000"),
        (D("-15.50"), "-15.5"),
        # Longer than the Decimal context precision: the text still shows every digit.
        (D("1234567890123456789012345678.95"), "1234567890123456789012345678.95"),
    ],
)
def test_renders_a_money_figure_without_trailing_zeros_or_an_exponent(
    figure: Decimal, text: str
) -> None:
    line = SumLine(TOTAL, ((PART_ONE, figure),), figure)

    assert render(line) == f"total: part_one {text} = {text}"


@pytest.mark.parametrize(
    ("line", "text"),
    [
        (
            BracketColumnLine(D("100.00"), D("0.20"), D("150.00"), D("10.00"), D("40.00")),
            "20% on 150 over 100 plus 10",
        ),
        (
            BracketColumnLine(D("3E+2"), D("0.30"), D("1.0E+2"), D("5.0E+1"), D("80.0")),
            "30% on 100 over 300 plus 50",
        ),
        (
            RoundedTotalLine(BASIC_TAX, TAXABLE_BASE, D("250.00"), CENT, D("40.00")),
            "basic_tax on taxable_base 250 (half-up to 0.01)",
        ),
        (
            CreditAmountLine(PERSONAL_AMOUNT, Credit(D("1000.50")), NO_ROUNDING, D("1000.50")),
            "personal_amount: credit amount 1000.5 (no rounding)",
        ),
        (
            SumLine(TOTAL, ((PART_ONE, D("100.250")), (PART_TWO, D("4E+1"))), D("140.250")),
            "total: part_one 100.25 + part_two 40 = 140.25",
        ),
        (
            RateAppliedLine(
                RATED_AMOUNT, GROSS_AMOUNT, D("1000.00"), Rate(D("0.5")), NO_ROUNDING, D("500.000")
            ),
            "rated_amount: 50% of gross_amount 1000 (no rounding)",
        ),
        (
            SubtractedLine(
                NET_AMOUNT, GROSS_AMOUNT, D("100.250"), REDUCTION, D("40.00"), D("60.250")
            ),
            "net_amount: gross_amount 100.25 less reduction 40 = 60.25",
        ),
        (
            SubtractedNotBelowZeroLine(
                NET_AMOUNT, GROSS_AMOUNT, D("100.250"), REDUCTION, D("4.0E+1"), D("60.250")
            ),
            "net_amount: gross_amount 100.25 less reduction 40, not below 0 = 60.25",
        ),
        (
            CappedAmountLine(
                CAPPED_AMOUNT,
                GROSS_AMOUNT,
                D("1500.2500"),
                Amount(D("1471.50")),
                NO_ROUNDING,
                D("1471.50"),
            ),
            "capped_amount: lesser of gross_amount 1500.25 and 1471.5 (no rounding)",
        ),
        (
            LesserOfLine(
                LESSER_AMOUNT, ((PART_ONE, D("1500.2500")), (PART_TWO, D("1E+3"))), D("1E+3")
            ),
            "lesser_amount: lesser of part_one 1500.25 and part_two 1000 = 1000",
        ),
        (
            ContributionTierLine(
                CONTRIBUTION,
                EARNINGS,
                D("23000.00"),
                ContributionTier(Rate(D("0.05")), D("3.0E+3"), D("50000.00"), D("2350.50")),
                NO_ROUNDING,
                D("2.00E+4"),
                D("1000.000"),
            ),
            "contribution: 5% of earnings between 3000 and 50000 (20000), at most 2350.5 "
            "(no rounding)",
        ),
        (
            SurchargeTierLine(
                SURCHARGE,
                TAX_SO_FAR,
                D("400.50"),
                D("3E+2"),
                Rate(D("0.25")),
                NO_ROUNDING,
                D("25.125"),
            ),
            "surcharge: 25% of tax_so_far 400.5 over 300 (no rounding)",
        ),
        (
            TaperedAmountLine(
                PERSONAL_AMOUNT,
                INCOME,
                D("22000.50"),
                Taper(D("1000.00"), D("5.0E+2"), D("20000.00"), D("1E+4")),
                NO_ROUNDING,
                D("100.0250"),
                D("1399.9750"),
            ),
            "personal_amount: 1000 plus 500 less 100.025 for income 22000.5 over 20000 "
            "(range 10000), not below 1000 (no rounding)",
        ),
        (
            PerUnitAmountLine(
                CHILD_AMOUNT, CHILDREN, 2, Amount(D("544.00")), NO_ROUNDING, D("1088.00")
            ),
            "child_amount: 544 for each of 2 child_count = 1088 (no rounding)",
        ),
        (
            MultipleOverLine(
                REDUCTION,
                REDUCTION_AMOUNTS,
                D("294.00"),
                Factor(D("2.0")),
                TAX_SO_FAR,
                D("1.000E+2"),
                NO_ROUNDING,
                D("488.00"),
            ),
            "reduction: 2 × reduction_amounts 294 over tax_so_far 100, not below 0 (no rounding)",
        ),
        (
            AtMostLine(ALLOWED_AMOUNT, CLAIMED_AMOUNT, D("1926.00"), CLAIM_LIMIT, D("1.9260E+3")),
            "allowed_amount: claimed_amount 1926, at most claim_limit 1926",
        ),
        (
            FractionAppliedLine(
                EARNED_PORTION,
                EARNED_INCOME,
                D("6.0000E+4"),
                Fraction(2, 3),
                NO_ROUNDING,
                D("40000.00"),
            ),
            "earned_portion: 2/3 of earned_income 60000 (no rounding)",
        ),
        (
            TimesCountLine(
                AMOUNT_CLAIMED, AMOUNT_EACH, D("1.612900E+4"), PERSONS, 2, D("32258.00")
            ),
            "amount_claimed: amount_each 16129 for each of 2 person_count = 32258",
        ),
    ],
)
def test_renders_every_money_figure_of_a_line_without_trailing_zeros(
    line: TraceLine, text: str
) -> None:
    assert render(line) == text


# --- whole traces and unknown lines ----------------------------------------------


def test_render_all_renders_each_line_in_order() -> None:
    trace = (
        BracketColumnLine(D(0), D("0.10"), D(100), D(0), D("10.0")),
        RoundedTotalLine(BASIC_TAX, TAXABLE_BASE, D(100), NO_ROUNDING, D("10.0")),
        SumLine(TOTAL, ((PART_ONE, D("1")), (PART_TWO, D("2"))), D("3")),
        RateAppliedLine(RATED_AMOUNT, TOTAL, D("3"), Rate(D("0.5")), NO_ROUNDING, D("1.5")),
        SubtractedLine(NET_AMOUNT, TOTAL, D("3"), RATED_AMOUNT, D("1.5"), D("1.5")),
        SubtractedNotBelowZeroLine(TOTAL, RATED_AMOUNT, D("1.5"), PART_TWO, D("2"), D("0")),
        CreditAmountLine(PERSONAL_AMOUNT, Credit(D("1000")), NO_ROUNDING, D("1000")),
        CappedAmountLine(CAPPED_AMOUNT, TOTAL, D("3"), Amount(D("2")), NO_ROUNDING, D("2")),
        LesserOfLine(LESSER_AMOUNT, ((TOTAL, D("3")), (CAPPED_AMOUNT, D("2"))), D("2")),
        ContributionTierLine(
            CONTRIBUTION, EARNINGS, D("23000"), TIER, NO_ROUNDING, D("20000"), D("1000")
        ),
        SurchargeTierLine(SURCHARGE, TOTAL, D("3"), D("1"), Rate(D("0.5")), NO_ROUNDING, D("1")),
        TaperedAmountLine(
            PERSONAL_AMOUNT, INCOME, D("22000"), TAPER, NO_ROUNDING, D("100"), D("1400")
        ),
        PerUnitAmountLine(CHILD_AMOUNT, CHILDREN, 2, Amount(D("544")), NO_ROUNDING, D("1088")),
        MultipleOverLine(
            REDUCTION,
            CHILD_AMOUNT,
            D("1088"),
            Factor(D("2")),
            TOTAL,
            D("3"),
            NO_ROUNDING,
            D("2173"),
        ),
        AtMostLine(ALLOWED_AMOUNT, TOTAL, D("3"), CAPPED_AMOUNT, D("3")),
        FractionAppliedLine(EARNED_PORTION, TOTAL, D("3"), Fraction(2, 3), NO_ROUNDING, D("2")),
        TimesCountLine(AMOUNT_CLAIMED, TOTAL, D("3"), PERSONS, 1, D("3")),
    )

    assert EnglishTraceRenderer().render_all(trace) == (
        "10% on 100 over 0 plus 0",
        "basic_tax on taxable_base 100 (no rounding)",
        "total: part_one 1 + part_two 2 = 3",
        "rated_amount: 50% of total 3 (no rounding)",
        "net_amount: total 3 less rated_amount 1.5 = 1.5",
        "total: rated_amount 1.5 less part_two 2, not below 0 = 0",
        "personal_amount: credit amount 1000 (no rounding)",
        "capped_amount: lesser of total 3 and 2 (no rounding)",
        "lesser_amount: lesser of total 3 and capped_amount 2 = 2",
        "contribution: 5% of earnings between 3000 and 50000 (20000), at most 2350 (no rounding)",
        "surcharge: 50% of total 3 over 1 (no rounding)",
        "personal_amount: 1000 plus 500 less 100 for income 22000 over 20000 (range 10000), "
        "not below 1000 (no rounding)",
        "child_amount: 544 for each of 2 child_count = 1088 (no rounding)",
        "reduction: 2 × child_amount 1088 over total 3, not below 0 (no rounding)",
        "allowed_amount: total 3, at most capped_amount 3",
        "earned_portion: 2/3 of total 3 (no rounding)",
        "amount_claimed: total 3 for each of 1 person_count = 3",
    )


def test_render_all_of_an_empty_trace_is_empty() -> None:
    assert EnglishTraceRenderer().render_all(()) == ()


@dataclass(frozen=True)
class MadeUpLine(TraceLine):
    """A made-up line class the renderer does not know."""

    figure: Decimal

    @property
    def amount(self) -> Decimal:
        return self.figure


def test_rejects_a_line_class_it_does_not_know() -> None:
    with pytest.raises(TypeError, match="MadeUpLine"):
        render(MadeUpLine(D(1)))


def test_render_all_rejects_a_line_class_it_does_not_know() -> None:
    with pytest.raises(TypeError, match="MadeUpLine"):
        EnglishTraceRenderer().render_all((SumLine(TOTAL, (), D(1)), MadeUpLine(D(1))))
