"""Unit tests for EnglishTraceRenderer: structured trace lines as English text, made-up values.

The renderer reproduces the trace text capabilities used to compose themselves, so the move to
structured lines changes only the structure. Rates print as percentages, `(rate * 100)` normalised
in fixed-point notation; rounding rules print as "no rounding" or "<mode> to <increment>".
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

import pytest

from app.adapters.inbound.trace_english import EnglishTraceRenderer
from app.domain.artifact import ArtifactKind
from app.domain.parameters.credit import Credit
from app.domain.parameters.rate import Rate
from app.domain.parameters.rounding import NO_ROUNDING, RoundingMode, RoundingRule, RoundTo
from app.domain.trace import (
    BracketSliceLine,
    CreditAmountLine,
    CreditAppliedLine,
    CreditLine,
    RateAppliedLine,
    RoundedTotalLine,
    SubtractedLine,
    SubtractedNotBelowZeroLine,
    SumLine,
    TraceLine,
    UnusedCreditLine,
)

D = Decimal
CENT = RoundTo(D("0.01"), RoundingMode.HALF_UP)

TAXABLE_BASE = ArtifactKind("ex/taxable_base", Decimal)
BASIC_TAX = ArtifactKind("ex/basic_tax", Decimal)
TAX_AFTER_CREDIT = ArtifactKind("ex/tax_after_credit", Decimal)
PART_ONE = ArtifactKind("ex/part_one", Decimal)
PART_TWO = ArtifactKind("ex/part_two", Decimal)
PART_THREE = ArtifactKind("ex/part_three", Decimal)
TOTAL = ArtifactKind("ex/total", Decimal)
GROSS_AMOUNT = ArtifactKind("ex/gross_amount", Decimal)
RATED_AMOUNT = ArtifactKind("ex/rated_amount", Decimal)
REDUCTION = ArtifactKind("ex/reduction", Decimal)
NET_AMOUNT = ArtifactKind("ex/net_amount", Decimal)
PERSONAL_AMOUNT = ArtifactKind("ex/personal_amount", Decimal)


def render(line: TraceLine) -> str:
    return EnglishTraceRenderer().render(line)


# --- bracket slices --------------------------------------------------------------


def test_renders_a_bounded_slice() -> None:
    line = BracketSliceLine(D(0), D(100), D("0.10"), D(100), D("10.0"))

    assert render(line) == "10% on 100 (0 to 100)"


def test_renders_a_middle_slice() -> None:
    line = BracketSliceLine(D(100), D(300), D("0.20"), D(150), D("30.0"))

    assert render(line) == "20% on 150 (100 to 300)"


def test_renders_the_open_top_slice() -> None:
    line = BracketSliceLine(D(300), None, D("0.30"), D(100), D("30.0"))

    assert render(line) == "30% on 100 (over 300)"


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
    line = BracketSliceLine(D(0), D(100), D(rate), D(100), D(0))

    assert render(line) == f"{percent}% on 100 (0 to 100)"


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


# --- credits ---------------------------------------------------------------------


def test_renders_a_credit_without_rounding() -> None:
    line = CreditLine(Credit(D("1000")), Rate(D("0.125")), NO_ROUNDING, D("125.000"))

    assert render(line) == "credit: 12.5% of 1000 (no rounding)"


def test_renders_a_rounded_credit() -> None:
    line = CreditLine(Credit(D("1000.05")), Rate(D("0.1")), CENT, D("100.01"))

    assert render(line) == "credit: 10% of 1000.05 (half-up to 0.01)"


def test_renders_the_credit_applied() -> None:
    line = CreditAppliedLine(TAX_AFTER_CREDIT, BASIC_TAX, D("500"), D("375.000"))

    assert render(line) == "tax_after_credit: basic_tax 500 less credit, not below 0"


def test_renders_the_unused_credit() -> None:
    assert render(UnusedCreditLine(D("25.000"))) == "unused credit, not refunded"


# --- sums ------------------------------------------------------------------------


def test_renders_a_sum_of_three_parts() -> None:
    line = SumLine(
        TOTAL,
        ((PART_ONE, D("100.25")), (PART_TWO, D("40")), (PART_THREE, D("9.75"))),
        D("150.00"),
    )

    assert render(line) == "total: part_one 100.25 + part_two 40 + part_three 9.75 = 150.00"


def test_renders_the_parts_in_the_order_of_the_line() -> None:
    line = SumLine(TOTAL, ((PART_THREE, D("9.75")), (PART_ONE, D("100.25"))), D("110.00"))

    assert render(line) == "total: part_three 9.75 + part_one 100.25 = 110.00"


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

    assert render(line) == "net_amount: gross_amount 40.50 less reduction 40.50 = 0.00"


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

    assert render(line) == "net_amount: gross_amount 40.50 less reduction 40.50, not below 0 = 0"


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


# --- whole traces and unknown lines ----------------------------------------------


def test_render_all_renders_each_line_in_order() -> None:
    trace = (
        BracketSliceLine(D(0), D(100), D("0.10"), D(100), D("10.0")),
        RoundedTotalLine(BASIC_TAX, TAXABLE_BASE, D(100), NO_ROUNDING, D("10.0")),
        CreditLine(Credit(D("1000")), Rate(D("0.125")), NO_ROUNDING, D("125.000")),
        CreditAppliedLine(TAX_AFTER_CREDIT, BASIC_TAX, D("10.0"), D("0")),
        UnusedCreditLine(D("115.000")),
        SumLine(TOTAL, ((PART_ONE, D("1")), (PART_TWO, D("2"))), D("3")),
        RateAppliedLine(RATED_AMOUNT, TOTAL, D("3"), Rate(D("0.5")), NO_ROUNDING, D("1.5")),
        SubtractedLine(NET_AMOUNT, TOTAL, D("3"), RATED_AMOUNT, D("1.5"), D("1.5")),
        SubtractedNotBelowZeroLine(TOTAL, RATED_AMOUNT, D("1.5"), PART_TWO, D("2"), D("0")),
        CreditAmountLine(PERSONAL_AMOUNT, Credit(D("1000")), NO_ROUNDING, D("1000")),
    )

    assert EnglishTraceRenderer().render_all(trace) == (
        "10% on 100 (0 to 100)",
        "basic_tax on taxable_base 100 (no rounding)",
        "credit: 12.5% of 1000 (no rounding)",
        "tax_after_credit: basic_tax 10.0 less credit, not below 0",
        "unused credit, not refunded",
        "total: part_one 1 + part_two 2 = 3",
        "rated_amount: 50% of total 3 (no rounding)",
        "net_amount: total 3 less rated_amount 1.5 = 1.5",
        "total: rated_amount 1.5 less part_two 2, not below 0 = 0",
        "personal_amount: credit amount 1000 (no rounding)",
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
        EnglishTraceRenderer().render_all((UnusedCreditLine(D(1)), MadeUpLine(D(1))))
