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
    CreditAppliedLine,
    CreditLine,
    RoundedTotalLine,
    TraceLine,
    UnusedCreditLine,
)

D = Decimal
CENT = RoundTo(D("0.01"), RoundingMode.HALF_UP)

TAXABLE_BASE = ArtifactKind("ex/taxable_base", Decimal)
BASIC_TAX = ArtifactKind("ex/basic_tax", Decimal)
TAX_AFTER_CREDIT = ArtifactKind("ex/tax_after_credit", Decimal)


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


# --- whole traces and unknown lines ----------------------------------------------


def test_render_all_renders_each_line_in_order() -> None:
    trace = (
        BracketSliceLine(D(0), D(100), D("0.10"), D(100), D("10.0")),
        RoundedTotalLine(BASIC_TAX, TAXABLE_BASE, D(100), NO_ROUNDING, D("10.0")),
        CreditLine(Credit(D("1000")), Rate(D("0.125")), NO_ROUNDING, D("125.000")),
        CreditAppliedLine(TAX_AFTER_CREDIT, BASIC_TAX, D("10.0"), D("0")),
        UnusedCreditLine(D("115.000")),
    )

    assert EnglishTraceRenderer().render_all(trace) == (
        "10% on 100 (0 to 100)",
        "basic_tax on taxable_base 100 (no rounding)",
        "credit: 12.5% of 1000 (no rounding)",
        "tax_after_credit: basic_tax 10.0 less credit, not below 0",
        "unused credit, not refunded",
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
