"""Unit tests for BracketSchedule: the form's bracket columns over ascending thresholds.

Each bracket holds what a form prints in its column: the threshold it starts `from` (`lower`), its
`rate` and `tax_at_start`, the tax at the bracket's start as a dollars-and-cents constant. The tax
on an amount is the form's two lines for the bracket the amount falls in: the rate on the excess
over the bracket's lower, plus its constant. The schedule checks each constant against the exact
tax on the brackets below, rounded half-up to the cent; the first bracket's constant is 0. An
amount at a threshold falls in the lower bracket ("more than ... but not more than ...").

Values are made up; real jurisdictions' brackets are tested with the pilot data.
"""

from __future__ import annotations

from dataclasses import fields
from decimal import Decimal

import pytest

from app.domain.errors import DomainError, InvalidBracketScheduleError
from app.domain.parameters.brackets import Bracket, BracketColumn, BracketSchedule

D = Decimal

# 10% to 100, 20% from 100 to 300, 30% above 300; constants exact: 10% of 100, plus 20% of 200.
SCHEDULE = BracketSchedule(
    (
        Bracket(D(0), D("0.10"), D(0)),
        Bracket(D(100), D("0.20"), D("10.00")),
        Bracket(D(300), D("0.30"), D("50.00")),
    )
)

# Constants the form rounds: 10.5% of 105 is 11.025, printed 11.03 (half-up); plus 20.5% of 105
# (21.525) is 32.55 exactly, printed 32.55. Chaining from the printed 11.03 would give 32.56.
ROUNDED = BracketSchedule(
    (
        Bracket(D(0), D("0.105"), D(0)),
        Bracket(D(105), D("0.205"), D("11.03")),
        Bracket(D(210), D("0.30"), D("32.55")),
    )
)


@pytest.mark.parametrize(
    ("amount", "tax"),
    [
        ("0", "0"),
        ("50", "5.0"),
        ("100", "10.0"),  # at the threshold: the lower bracket's column
        ("250", "40.0"),  # 20% of (250 - 100) + 10.00
        ("300", "50.0"),
        ("1000", "260.0"),  # 30% of (1000 - 300) + 50.00
        ("100.01", "10.002"),  # exact: no rounding of the excess times the rate
    ],
)
def test_tax_on_is_the_rate_on_the_excess_plus_the_brackets_constant(amount: str, tax: str) -> None:
    assert SCHEDULE.tax_on(D(amount)) == D(tax)


@pytest.mark.parametrize(
    ("amount", "tax"),
    [
        ("150", "20.255"),  # 20.5% of 45 = 9.225, plus the printed 11.03, not the exact 11.025
        ("210", "32.555"),  # at the threshold: 20.5% of 105 + 11.03, not the next column's 32.55
        ("310", "62.55"),  # 30% of 100 + 32.55
        ("105", "11.025"),  # at the first threshold: 10.5% of 105 + 0, not the printed 11.03
    ],
)
def test_tax_on_uses_the_printed_constant_not_the_exact_tax_below(amount: str, tax: str) -> None:
    assert ROUNDED.tax_on(D(amount)) == D(tax)


def test_column_for_is_the_bracket_the_amount_falls_in() -> None:
    assert SCHEDULE.column_for(D(250)) == BracketColumn(
        lower=D(100), rate=D("0.20"), excess=D(150), tax_at_start=D("10.00"), tax=D("40.00")
    )


def test_column_for_an_amount_at_a_threshold_is_the_lower_brackets() -> None:
    assert SCHEDULE.column_for(D(300)) == BracketColumn(
        lower=D(100), rate=D("0.20"), excess=D(200), tax_at_start=D("10.00"), tax=D("50.00")
    )


def test_column_for_zero_is_the_first_brackets() -> None:
    assert SCHEDULE.column_for(D(0)) == BracketColumn(
        lower=D(0), rate=D("0.10"), excess=D(0), tax_at_start=D(0), tax=D(0)
    )


def test_top_bracket_is_open_ended() -> None:
    top = SCHEDULE.column_for(D(1000))

    assert (top.lower, top.excess, top.tax_at_start, top.tax) == (
        D(300),
        D(700),
        D("50.00"),
        D("260.00"),
    )


def test_tax_on_is_the_columns_tax() -> None:
    for amount in (D(0), D(50), D(250), D(1000)):
        assert SCHEDULE.tax_on(amount) == SCHEDULE.column_for(amount).tax


def test_a_column_holds_its_fields_in_order() -> None:
    assert [field.name for field in fields(BracketColumn)] == [
        "lower",
        "rate",
        "excess",
        "tax_at_start",
        "tax",
    ]


def test_a_column_holds_no_upper_bound() -> None:
    assert "upper" not in [field.name for field in fields(BracketColumn)]


def test_the_schedule_offers_one_column_per_amount_and_its_tax() -> None:
    public = {name for name in vars(BracketSchedule) if not name.startswith("_")}

    assert public == {"column_for", "tax_on"}


def test_single_bracket_is_a_flat_rate() -> None:
    assert BracketSchedule((Bracket(D(0), D("0.25"), D(0)),)).tax_on(D(80)) == D("20.00")


@pytest.mark.parametrize("amount", [D(-1), D("-0.01")])
def test_rejects_negative_amount(amount: Decimal) -> None:
    with pytest.raises(ValueError, match="must not be negative"):
        SCHEDULE.tax_on(amount)
    with pytest.raises(ValueError, match="must not be negative"):
        SCHEDULE.column_for(amount)


def test_rejects_non_decimal_amount() -> None:
    with pytest.raises(TypeError, match="must be a Decimal"):
        SCHEDULE.tax_on(100)  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="must be a Decimal"):
        SCHEDULE.column_for(100)  # type: ignore[arg-type]


# --- the bracket and its printed constant ---------------------------------------------


def test_a_bracket_holds_its_fields_in_order() -> None:
    assert [field.name for field in fields(Bracket)] == ["lower", "rate", "tax_at_start"]


def test_a_bracket_is_built_positionally_in_field_order() -> None:
    assert Bracket(D(100), D("0.20"), D("10.00")) == Bracket(
        lower=D(100), rate=D("0.20"), tax_at_start=D("10.00")
    )


def test_a_bracket_needs_its_constant() -> None:
    with pytest.raises(TypeError):
        Bracket(D(0), D("0.10"))  # type: ignore[call-arg]


@pytest.mark.parametrize(
    "tax_at_start",
    [
        D("11.03"),  # the exact 11.025, rounded half-up to the cent
        D("11.030"),  # the same figure, written with another exponent
    ],
)
def test_accepts_a_constant_that_is_the_rounded_tax_below(tax_at_start: Decimal) -> None:
    schedule = BracketSchedule(
        (Bracket(D(0), D("0.105"), D(0)), Bracket(D(105), D("0.205"), tax_at_start))
    )

    assert schedule.brackets[1].tax_at_start == D("11.03")


def test_checks_each_constant_against_the_exact_cumulative_tax_rounded() -> None:
    # 10.5% of 105 + 20.5% of 105 = 32.55 exactly; chaining from the printed 11.03 gives 32.56.
    with pytest.raises(InvalidBracketScheduleError, match="from 210"):
        BracketSchedule(
            (
                Bracket(D(0), D("0.105"), D(0)),
                Bracket(D(105), D("0.205"), D("11.03")),
                Bracket(D(210), D("0.30"), D("32.56")),
            )
        )


@pytest.mark.parametrize(
    ("brackets", "named", "given", "expected"),
    [
        pytest.param(
            (Bracket(D(0), D("0.105"), D(0)), Bracket(D(105), D("0.205"), D("11.02"))),
            "from 105",
            "11.02",
            "11.03",
            id="rounded-half-even",
        ),
        pytest.param(
            (Bracket(D(0), D("0.105"), D(0)), Bracket(D(105), D("0.205"), D("11.025"))),
            "from 105",
            "11.025",
            "11.03",
            id="exact-unrounded",
        ),
        pytest.param(
            (
                Bracket(D(0), D("0.10"), D(0)),
                Bracket(D(100), D("0.20"), D("10.00")),
                Bracket(D(300), D("0.30"), D("5.00")),
            ),
            "from 300",
            "5.00",
            "50.00",
            id="mistyped-top",
        ),
        pytest.param(
            (Bracket(D(0), D("0.10"), D(0)), Bracket(D(100), D("0.20"), D(0))),
            "from 100",
            "0",
            "10.00",
            id="missing-constant-as-zero",
        ),
    ],
)
def test_rejects_a_constant_that_is_not_the_rounded_tax_below(
    brackets: tuple[Bracket, ...], named: str, given: str, expected: str
) -> None:
    with pytest.raises(InvalidBracketScheduleError, match=named) as raised:
        BracketSchedule(brackets)

    message = str(raised.value)
    assert "tax_at_start" in message
    assert given in message
    assert expected in message


@pytest.mark.parametrize("tax_at_start", [D("0.01"), D("10")])
def test_the_first_brackets_constant_must_be_zero(tax_at_start: Decimal) -> None:
    with pytest.raises(InvalidBracketScheduleError, match="first bracket.*tax_at_start.*0"):
        BracketSchedule((Bracket(D(0), D("0.10"), tax_at_start),))


def test_the_first_brackets_constant_may_be_written_with_cents() -> None:
    assert BracketSchedule((Bracket(D(0), D("0.10"), D("0.00")),)).tax_on(D(10)) == D("1.0")


@pytest.mark.parametrize(
    ("brackets", "message"),
    [
        ((), "at least one bracket"),
        ((Bracket(D(10), D("0.1"), D(0)),), "first bracket must start at 0"),
        ((Bracket(D(0), D("0.1"), D(0)), Bracket(D(0), D("0.2"), D(0))), "strictly ascending"),
        (
            (
                Bracket(D(0), D("0.1"), D(0)),
                Bracket(D(200), D("0.2"), D(20)),
                Bracket(D(100), D("0.3"), D(0)),
            ),
            "strictly ascending",
        ),
    ],
)
def test_rejects_invalid_schedules(brackets: tuple[Bracket, ...], message: str) -> None:
    with pytest.raises(InvalidBracketScheduleError, match=message):
        BracketSchedule(brackets)


@pytest.mark.parametrize(
    ("lower", "rate", "tax_at_start", "message"),
    [
        (D(-1), D("0.1"), D(0), "lower must not be negative"),
        (D(0), D("-0.1"), D(0), "rate must be between 0 and 1"),
        (D(0), D("1.01"), D(0), "rate must be between 0 and 1"),
        (D("NaN"), D("0.1"), D(0), "must be finite"),
        (D(0), D("0.1"), D("-0.01"), "tax_at_start must not be negative"),
        (D(0), D("0.1"), D("NaN"), "tax_at_start must be finite"),
        (D(0), D("0.1"), D("Infinity"), "tax_at_start must be finite"),
    ],
)
def test_rejects_invalid_brackets(
    lower: Decimal, rate: Decimal, tax_at_start: Decimal, message: str
) -> None:
    with pytest.raises(InvalidBracketScheduleError, match=message):
        Bracket(lower, rate, tax_at_start)


@pytest.mark.parametrize(
    ("lower", "rate", "tax_at_start", "name"),
    [
        (0, D("0.1"), D(0), "lower"),
        (D(0), 0.1, D(0), "rate"),
        (D(0), D("0.1"), 0, "tax_at_start"),
        (D(0), D("0.1"), "0", "tax_at_start"),
    ],
)
def test_rejects_non_decimal_bracket_values(
    lower: object, rate: object, tax_at_start: object, name: str
) -> None:
    with pytest.raises(TypeError, match=f"bracket {name} must be a Decimal"):
        Bracket(lower, rate, tax_at_start)  # type: ignore[arg-type]


def test_invalid_schedule_is_a_domain_error() -> None:
    assert issubclass(InvalidBracketScheduleError, DomainError)
