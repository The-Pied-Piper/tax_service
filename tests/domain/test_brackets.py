"""Unit tests for BracketSchedule: marginal rates over ascending thresholds.

Values are made up; real jurisdictions' brackets are tested with the pilot data.
"""

from __future__ import annotations

from decimal import Decimal

import pytest

from app.domain.brackets import Bracket, BracketSchedule, BracketSlice
from app.domain.errors import DomainError, InvalidBracketScheduleError

D = Decimal

# 10% to 100, 20% from 100 to 300, 30% above 300.
SCHEDULE = BracketSchedule(
    (Bracket(D(0), D("0.10")), Bracket(D(100), D("0.20")), Bracket(D(300), D("0.30")))
)


@pytest.mark.parametrize(
    ("amount", "tax"),
    [
        ("0", "0"),
        ("50", "5.0"),
        ("100", "10.0"),
        ("250", "40.0"),  # 10 + 150 × 0.20
        ("300", "50.0"),
        ("1000", "260.0"),  # 10 + 40 + 700 × 0.30
        ("100.01", "10.002"),  # exact: no rounding inside the schedule
    ],
)
def test_tax_on_applies_each_rate_to_its_slice(amount: str, tax: str) -> None:
    assert SCHEDULE.tax_on(D(amount)) == D(tax)


def test_slices_break_the_amount_down_by_bracket() -> None:
    assert SCHEDULE.slices(D(250)) == (
        BracketSlice(lower=D(0), upper=D(100), rate=D("0.10"), taxed=D(100), tax=D("10.0")),
        BracketSlice(lower=D(100), upper=D(300), rate=D("0.20"), taxed=D(150), tax=D("30.0")),
    )


def test_top_slice_is_open_ended() -> None:
    top = SCHEDULE.slices(D(1000))[-1]

    assert top.upper is None
    assert top.taxed == D(700)


def test_single_bracket_is_a_flat_rate() -> None:
    assert BracketSchedule((Bracket(D(0), D("0.25")),)).tax_on(D(80)) == D("20.00")


def test_rejects_negative_amount() -> None:
    with pytest.raises(ValueError, match="must not be negative"):
        SCHEDULE.tax_on(D(-1))


def test_rejects_non_decimal_amount() -> None:
    with pytest.raises(TypeError, match="must be a Decimal"):
        SCHEDULE.tax_on(100)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("brackets", "message"),
    [
        ((), "at least one bracket"),
        ((Bracket(D(10), D("0.1")),), "first bracket must start at 0"),
        ((Bracket(D(0), D("0.1")), Bracket(D(0), D("0.2"))), "strictly ascending"),
        (
            (Bracket(D(0), D("0.1")), Bracket(D(200), D("0.2")), Bracket(D(100), D("0.3"))),
            "strictly ascending",
        ),
    ],
)
def test_rejects_invalid_schedules(brackets: tuple[Bracket, ...], message: str) -> None:
    with pytest.raises(InvalidBracketScheduleError, match=message):
        BracketSchedule(brackets)


@pytest.mark.parametrize(
    ("lower", "rate", "message"),
    [
        (D(-1), D("0.1"), "lower must not be negative"),
        (D(0), D("-0.1"), "rate must be between 0 and 1"),
        (D(0), D("1.01"), "rate must be between 0 and 1"),
        (D("NaN"), D("0.1"), "must be finite"),
    ],
)
def test_rejects_invalid_brackets(lower: Decimal, rate: Decimal, message: str) -> None:
    with pytest.raises(InvalidBracketScheduleError, match=message):
        Bracket(lower, rate)


@pytest.mark.parametrize(("lower", "rate"), [(0, D("0.1")), (D(0), 0.1)])
def test_rejects_non_decimal_bracket_values(lower: object, rate: object) -> None:
    with pytest.raises(TypeError, match="must be a Decimal"):
        Bracket(lower, rate)  # type: ignore[arg-type]


def test_invalid_schedule_is_a_domain_error() -> None:
    assert issubclass(InvalidBracketScheduleError, DomainError)
