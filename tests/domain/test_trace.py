"""Unit tests for the structured trace: one frozen line class per fact, with made-up values.

Each line records what happened with the domain objects involved (`ArtifactKind`, `Rate`,
`Credit`, `RoundingRule`), never text; its `amount` is the figure the line is about.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError, fields
from decimal import Decimal
from typing import Any, cast

import pytest

from app.domain.artifact import ArtifactKind
from app.domain.parameters.credit import Credit
from app.domain.parameters.rate import Rate
from app.domain.parameters.rounding import NO_ROUNDING, RoundingMode, RoundTo
from app.domain.trace import (
    BracketSliceLine,
    CreditAppliedLine,
    CreditLine,
    RateAppliedLine,
    RoundedTotalLine,
    SubtractedLine,
    SumLine,
    TraceLine,
    UnusedCreditLine,
)

D = Decimal
CENT = RoundTo(D("0.01"), RoundingMode.HALF_UP)
BASE = ArtifactKind("ex/base", Decimal)
TAX = ArtifactKind("ex/tax", Decimal)
AFTER = ArtifactKind("ex/after", Decimal)
PART_ONE = ArtifactKind("ex/part_one", Decimal)
PART_TWO = ArtifactKind("ex/part_two", Decimal)
TOTAL = ArtifactKind("ex/total", Decimal)
RATED = ArtifactKind("ex/rated", Decimal)
GROSS = ArtifactKind("ex/gross", Decimal)
REDUCTION = ArtifactKind("ex/reduction", Decimal)
NET = ArtifactKind("ex/net", Decimal)


def slice_line() -> BracketSliceLine:
    return BracketSliceLine(D(0), D(100), D("0.10"), D(100), D("10.0"))


def total_line() -> RoundedTotalLine:
    return RoundedTotalLine(TAX, BASE, D(250), CENT, D("40.00"))


def credit_line() -> CreditLine:
    return CreditLine(Credit(D(1000)), Rate(D("0.125")), NO_ROUNDING, D("125.000"))


def applied_line() -> CreditAppliedLine:
    return CreditAppliedLine(AFTER, TAX, D(500), D("375.000"))


def unused_line() -> UnusedCreditLine:
    return UnusedCreditLine(D("25.000"))


def sum_line() -> SumLine:
    return SumLine(TOTAL, ((PART_ONE, D("1.25")), (PART_TWO, D(2))), D("3.25"))


def rate_applied_line() -> RateAppliedLine:
    return RateAppliedLine(RATED, BASE, D("200.01"), Rate(D("0.5")), CENT, D("100.01"))


def subtracted_line() -> SubtractedLine:
    return SubtractedLine(NET, GROSS, D("100.25"), REDUCTION, D(40), D("60.25"))


ALL_LINES = [
    slice_line,
    total_line,
    credit_line,
    applied_line,
    unused_line,
    sum_line,
    rate_applied_line,
    subtracted_line,
]


def test_the_base_line_cannot_be_built() -> None:
    with pytest.raises(TypeError):
        cast(Any, TraceLine)()


@pytest.mark.parametrize("make", ALL_LINES)
def test_every_line_is_a_trace_line(make: Any) -> None:
    assert isinstance(make(), TraceLine)


@pytest.mark.parametrize("make", ALL_LINES)
def test_lines_are_equal_by_value(make: Any) -> None:
    assert make() == make()
    assert make() is not make()


@pytest.mark.parametrize("make", ALL_LINES)
def test_lines_are_frozen(make: Any) -> None:
    line = make()
    with pytest.raises(FrozenInstanceError):
        setattr(line, fields(line)[0].name, D(1))


def test_bracket_slice_line_fields_in_order() -> None:
    line = slice_line()

    assert line == BracketSliceLine(
        lower=D(0), upper=D(100), rate=D("0.10"), taxed=D(100), tax=D("10.0")
    )
    assert (line.lower, line.upper, line.rate, line.taxed, line.tax) == (
        D(0),
        D(100),
        D("0.10"),
        D(100),
        D("10.0"),
    )
    assert line.amount == D("10.0")


def test_bracket_slice_line_open_top_slice_has_no_upper() -> None:
    line = BracketSliceLine(D(300), None, D("0.30"), D(100), D("30.0"))

    assert line.upper is None
    assert line.amount == D("30.0")


def test_bracket_slice_lines_differ_by_any_field() -> None:
    assert slice_line() != BracketSliceLine(D(0), D(100), D("0.10"), D(100), D("11.0"))
    assert slice_line() != BracketSliceLine(D(0), None, D("0.10"), D(100), D("10.0"))


def test_rounded_total_line_fields_in_order() -> None:
    line = total_line()

    assert line == RoundedTotalLine(
        output=TAX, base=BASE, base_amount=D(250), rounding=CENT, total=D("40.00")
    )
    assert line.output is TAX
    assert line.base is BASE
    assert line.base_amount == D(250)
    assert line.rounding == CENT
    assert line.total == D("40.00")
    assert line.amount == D("40.00")


def test_rounded_total_lines_differ_by_rounding() -> None:
    assert total_line() != RoundedTotalLine(TAX, BASE, D(250), NO_ROUNDING, D("40.00"))


def test_credit_line_fields_in_order() -> None:
    line = credit_line()

    assert line == CreditLine(
        basis=Credit(D(1000)), rate=Rate(D("0.125")), rounding=NO_ROUNDING, credit=D("125.000")
    )
    # Settled: `basis` is the Credit the rate applies to; the line's figure is `credit`.
    assert line.basis == Credit(D(1000))
    assert line.rate == Rate(D("0.125"))
    assert line.rounding == NO_ROUNDING
    assert line.credit == D("125.000")
    assert line.amount == D("125.000")


def test_credit_applied_line_fields_in_order() -> None:
    line = applied_line()

    assert line == CreditAppliedLine(output=AFTER, tax=TAX, tax_amount=D(500), after=D("375.000"))
    assert line.output is AFTER
    assert line.tax is TAX
    assert line.tax_amount == D(500)
    assert line.after == D("375.000")
    assert line.amount == D("375.000")


def test_unused_credit_line_holds_the_unused_part() -> None:
    line = unused_line()

    assert line == UnusedCreditLine(unused=D("25.000"))
    assert line.unused == D("25.000")
    assert line.amount == D("25.000")


def test_sum_line_fields_in_order() -> None:
    line = sum_line()

    assert line == SumLine(
        output=TOTAL, parts=((PART_ONE, D("1.25")), (PART_TWO, D(2))), total=D("3.25")
    )
    assert [f.name for f in fields(line)] == ["output", "parts", "total"]
    assert line.output is TOTAL
    assert line.parts == ((PART_ONE, D("1.25")), (PART_TWO, D(2)))
    assert line.total == D("3.25")
    assert line.amount == D("3.25")


def test_sum_line_may_have_no_parts() -> None:
    line = SumLine(TOTAL, (), D(0))

    assert line.parts == ()
    assert line.amount == D(0)


def test_sum_lines_differ_by_the_order_of_their_parts() -> None:
    assert sum_line() != SumLine(TOTAL, ((PART_TWO, D(2)), (PART_ONE, D("1.25"))), D("3.25"))


def test_sum_lines_are_hashable() -> None:
    assert hash(sum_line()) == hash(sum_line())


def test_rate_applied_line_fields_in_order() -> None:
    line = rate_applied_line()

    assert line == RateAppliedLine(
        output=RATED,
        base=BASE,
        base_amount=D("200.01"),
        rate=Rate(D("0.5")),
        rounding=CENT,
        result=D("100.01"),
    )
    assert [f.name for f in fields(line)] == [
        "output",
        "base",
        "base_amount",
        "rate",
        "rounding",
        "result",
    ]
    assert line.output is RATED
    assert line.base is BASE
    assert line.base_amount == D("200.01")
    assert line.rate == Rate(D("0.5"))
    assert line.rounding == CENT
    assert line.result == D("100.01")
    assert line.amount == D("100.01")


def test_rate_applied_lines_differ_by_rounding() -> None:
    assert rate_applied_line() != RateAppliedLine(
        RATED, BASE, D("200.01"), Rate(D("0.5")), NO_ROUNDING, D("100.01")
    )


def test_rate_applied_lines_are_hashable() -> None:
    assert hash(rate_applied_line()) == hash(rate_applied_line())


def test_subtracted_line_fields_in_order() -> None:
    line = subtracted_line()

    assert line == SubtractedLine(
        output=NET,
        minuend=GROSS,
        minuend_amount=D("100.25"),
        subtrahend=REDUCTION,
        subtrahend_amount=D(40),
        result=D("60.25"),
    )
    assert [f.name for f in fields(line)] == [
        "output",
        "minuend",
        "minuend_amount",
        "subtrahend",
        "subtrahend_amount",
        "result",
    ]
    assert line.output is NET
    assert line.minuend is GROSS
    assert line.minuend_amount == D("100.25")
    assert line.subtrahend is REDUCTION
    assert line.subtrahend_amount == D(40)
    assert line.result == D("60.25")
    assert line.amount == D("60.25")


def test_subtracted_line_may_hold_a_negative_result() -> None:
    line = SubtractedLine(NET, GROSS, D(10), REDUCTION, D("25.5"), D("-15.5"))

    assert line.result == D("-15.5")
    assert line.amount == D("-15.5")


def test_subtracted_lines_differ_by_which_kind_is_taken_off() -> None:
    assert subtracted_line() != SubtractedLine(
        NET, REDUCTION, D("100.25"), GROSS, D(40), D("60.25")
    )


def test_subtracted_lines_are_hashable() -> None:
    assert hash(subtracted_line()) == hash(subtracted_line())


def test_lines_of_different_classes_are_not_equal() -> None:
    assert cast(Any, UnusedCreditLine(D(10))) != BracketSliceLine(
        D(0), None, D("0.10"), D(100), D(10)
    )
