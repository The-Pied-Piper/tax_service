"""Unit tests for rounding rules (design.md §3, Rounding).

Rounding is a parameter: a capability decides *where* it rounds and the rule
decides *how*. The default is no rounding, and only exact decimals are accepted.
"""

from __future__ import annotations

import copy
from dataclasses import FrozenInstanceError
from decimal import Decimal
from fractions import Fraction

import pytest

from app.domain import rounding as rounding_module
from app.domain.errors import DomainError, InvalidRoundingRuleError
from app.domain.rounding import NO_ROUNDING, RoundingMode, RoundingRule, RoundTo

D = Decimal
CENT = D("0.01")


def rule(mode: RoundingMode, increment: str = "0.01") -> RoundTo:
    return RoundTo(increment=D(increment), mode=mode)


# --- no rounding ---------------------------------------------------------------


@pytest.mark.parametrize("amount", ["0", "1.005", "-1.005", "123456.789012345", "-0.0000001"])
def test_no_rounding_returns_amount_unchanged(amount: str) -> None:
    result = NO_ROUNDING.apply(D(amount))

    assert result == D(amount)
    assert result.as_tuple() == D(amount).as_tuple()  # same digits and scale


def test_both_rule_kinds_are_rounding_rules() -> None:
    assert isinstance(NO_ROUNDING, RoundingRule)
    assert isinstance(rule(RoundingMode.HALF_UP), RoundingRule)


def test_no_rounding_is_only_exposed_as_the_constant() -> None:
    assert not hasattr(rounding_module, "NoRounding")


@pytest.mark.parametrize("copier", [copy.copy, copy.deepcopy])
def test_copies_of_no_rounding_still_equal_the_constant(copier: object) -> None:
    # Copying or serialising creates a new instance; value equality keeps it the same rule.
    duplicate = copier(NO_ROUNDING)  # type: ignore[operator]

    assert duplicate == NO_ROUNDING
    assert hash(duplicate) == hash(NO_ROUNDING)


@pytest.mark.parametrize("rounding", [NO_ROUNDING, RoundTo(CENT, RoundingMode.HALF_UP)])
@pytest.mark.parametrize("attribute", ["increment", "extra"])
def test_rules_are_immutable(rounding: RoundingRule, attribute: str) -> None:
    with pytest.raises(FrozenInstanceError):
        setattr(rounding, attribute, 1)


# --- modes ---------------------------------------------------------------------


@pytest.mark.parametrize(
    ("mode", "amount", "expected"),
    [
        # half-up: ties away from zero
        (RoundingMode.HALF_UP, "1.005", "1.01"),
        (RoundingMode.HALF_UP, "1.004", "1.00"),
        (RoundingMode.HALF_UP, "-1.005", "-1.01"),
        (RoundingMode.HALF_UP, "2.675", "2.68"),  # 2.67 with binary floats
        # half-even: ties to the even neighbour
        (RoundingMode.HALF_EVEN, "1.005", "1.00"),
        (RoundingMode.HALF_EVEN, "1.015", "1.02"),
        (RoundingMode.HALF_EVEN, "1.0151", "1.02"),
        (RoundingMode.HALF_EVEN, "-1.005", "-1.00"),
        # down: toward zero (drops the remainder)
        (RoundingMode.DOWN, "1.019", "1.01"),
        (RoundingMode.DOWN, "-1.019", "-1.01"),
        # up: away from zero
        (RoundingMode.UP, "1.001", "1.01"),
        (RoundingMode.UP, "-1.001", "-1.01"),
        # floor: toward negative infinity
        (RoundingMode.FLOOR, "1.019", "1.01"),
        (RoundingMode.FLOOR, "-1.011", "-1.02"),
        # ceiling: toward positive infinity
        (RoundingMode.CEILING, "1.001", "1.01"),
        (RoundingMode.CEILING, "-1.019", "-1.01"),
    ],
)
def test_rounds_to_a_cent_by_mode(mode: RoundingMode, amount: str, expected: str) -> None:
    assert rule(mode).apply(D(amount)) == D(expected)


@pytest.mark.parametrize("mode", list(RoundingMode))
def test_amount_already_on_the_increment_is_unchanged(mode: RoundingMode) -> None:
    assert rule(mode).apply(D("-42.17")) == D("-42.17")


# --- mode resolution ------------------------------------------------------------

F = Fraction


@pytest.mark.parametrize(
    ("mode", "value", "expected"),
    [
        (RoundingMode.HALF_UP, F(5, 2), 3),
        (RoundingMode.HALF_UP, F(-5, 2), -3),
        (RoundingMode.HALF_UP, F(12, 5), 2),
        (RoundingMode.HALF_UP, F(13, 5), 3),
        (RoundingMode.HALF_EVEN, F(5, 2), 2),
        (RoundingMode.HALF_EVEN, F(7, 2), 4),
        (RoundingMode.HALF_EVEN, F(-5, 2), -2),
        (RoundingMode.HALF_EVEN, F(-7, 2), -4),
        (RoundingMode.HALF_EVEN, F(13, 5), 3),
        (RoundingMode.DOWN, F(29, 10), 2),
        (RoundingMode.DOWN, F(-29, 10), -2),
        (RoundingMode.UP, F(21, 10), 3),
        (RoundingMode.UP, F(-21, 10), -3),
        (RoundingMode.FLOOR, F(29, 10), 2),
        (RoundingMode.FLOOR, F(-21, 10), -3),
        (RoundingMode.CEILING, F(21, 10), 3),
        (RoundingMode.CEILING, F(-29, 10), -2),
    ],
)
def test_mode_resolves_a_fraction_to_an_integer(
    mode: RoundingMode, value: Fraction, expected: int
) -> None:
    assert mode.to_integer(value) == expected


@pytest.mark.parametrize("mode", list(RoundingMode))
@pytest.mark.parametrize("value", [F(0), F(4), F(-4)])
def test_mode_leaves_integers_unchanged(mode: RoundingMode, value: Fraction) -> None:
    assert mode.to_integer(value) == value


# --- increments ----------------------------------------------------------------


@pytest.mark.parametrize(
    ("increment", "mode", "amount", "expected"),
    [
        ("1", RoundingMode.HALF_UP, "2.5", "3"),
        ("1", RoundingMode.HALF_UP, "2.49", "2"),
        ("1", RoundingMode.DOWN, "2.99", "2"),
        ("0.05", RoundingMode.HALF_UP, "1.024", "1.00"),
        ("0.05", RoundingMode.HALF_UP, "1.025", "1.05"),
        ("0.05", RoundingMode.HALF_UP, "1.074", "1.05"),
        ("0.05", RoundingMode.HALF_UP, "1.075", "1.10"),
        # A non-decimal ratio: 0.045 / 0.03 is exactly 1.5, a tie.
        ("0.03", RoundingMode.HALF_UP, "0.045", "0.06"),
        ("0.03", RoundingMode.HALF_EVEN, "0.045", "0.06"),
        ("0.03", RoundingMode.DOWN, "0.045", "0.03"),
    ],
)
def test_rounds_to_any_positive_increment(
    increment: str, mode: RoundingMode, amount: str, expected: str
) -> None:
    assert rule(mode, increment).apply(D(amount)) == D(expected)


def test_result_carries_the_increments_scale() -> None:
    result = rule(RoundingMode.HALF_UP).apply(D("7"))

    assert str(result) == "7.00"


# --- rejected inputs -----------------------------------------------------------


@pytest.mark.parametrize("increment", ["0", "-0.01", "NaN", "Infinity"])
def test_rejects_non_positive_or_non_finite_increment(increment: str) -> None:
    with pytest.raises(InvalidRoundingRuleError, match="increment"):
        RoundTo(increment=D(increment), mode=RoundingMode.HALF_UP)


def test_invalid_rule_is_a_domain_error() -> None:
    assert issubclass(InvalidRoundingRuleError, DomainError)


@pytest.mark.parametrize("increment", [0.01, 1, "0.01"])
def test_rejects_increment_that_is_not_a_decimal(increment: object) -> None:
    with pytest.raises(TypeError, match="increment must be a Decimal"):
        RoundTo(increment=increment, mode=RoundingMode.HALF_UP)  # type: ignore[arg-type]


def test_rejects_mode_that_is_not_a_rounding_mode() -> None:
    with pytest.raises(TypeError, match="mode must be a RoundingMode"):
        RoundTo(increment=CENT, mode="half_up")  # type: ignore[arg-type]


@pytest.mark.parametrize("rounding", [NO_ROUNDING, RoundTo(CENT, RoundingMode.HALF_UP)])
@pytest.mark.parametrize("amount", [1.005, 1, "1.005"])
def test_rejects_amount_that_is_not_a_decimal(rounding: RoundingRule, amount: object) -> None:
    with pytest.raises(TypeError, match="amount must be a Decimal"):
        rounding.apply(amount)  # type: ignore[arg-type]


@pytest.mark.parametrize("rounding", [NO_ROUNDING, RoundTo(CENT, RoundingMode.HALF_UP)])
@pytest.mark.parametrize("amount", ["NaN", "Infinity", "-Infinity"])
def test_rejects_non_finite_amount(rounding: RoundingRule, amount: str) -> None:
    with pytest.raises(ValueError, match="amount must be finite"):
        rounding.apply(D(amount))


# --- value semantics and description --------------------------------------------


def test_rules_are_equal_by_value_and_hashable() -> None:
    assert rule(RoundingMode.HALF_UP) == rule(RoundingMode.HALF_UP)
    assert rule(RoundingMode.HALF_UP) != rule(RoundingMode.HALF_EVEN)
    assert len({rule(RoundingMode.HALF_UP), rule(RoundingMode.HALF_UP), NO_ROUNDING}) == 2


@pytest.mark.parametrize(
    ("rounding", "text"),
    [
        (NO_ROUNDING, "no rounding"),
        (RoundTo(CENT, RoundingMode.HALF_UP), "half-up to 0.01"),
        (RoundTo(D("1"), RoundingMode.FLOOR), "floor to 1"),
        (RoundTo(D("0.05"), RoundingMode.HALF_EVEN), "half-even to 0.05"),
    ],
)
def test_describes_itself_for_the_trace(rounding: RoundingRule, text: str) -> None:
    assert str(rounding) == text


def test_mode_values_are_stable_identifiers() -> None:
    assert [m.value for m in RoundingMode] == [
        "half_up",
        "half_even",
        "down",
        "up",
        "floor",
        "ceiling",
    ]
