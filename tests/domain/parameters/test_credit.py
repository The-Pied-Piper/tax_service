"""Unit tests for Credit: a credit amount and the rate that turns it into tax relief."""

from __future__ import annotations

from decimal import Decimal

import pytest

from app.domain.errors import DomainError, InvalidCreditError
from app.domain.parameters.credit import Credit

D = Decimal


def test_value_is_amount_times_rate_exactly() -> None:
    assert Credit(amount=D("1000"), rate=D("0.125")).value == D("125.000")


@pytest.mark.parametrize(
    ("amount", "rate", "message"),
    [
        (D("-1"), D("0.1"), "amount must not be negative"),
        (D("1"), D("-0.1"), "rate must be between 0 and 1"),
        (D("1"), D("1.5"), "rate must be between 0 and 1"),
        (D("Infinity"), D("0.1"), "must be finite"),
    ],
)
def test_rejects_invalid_values(amount: Decimal, rate: Decimal, message: str) -> None:
    with pytest.raises(InvalidCreditError, match=message):
        Credit(amount=amount, rate=rate)


@pytest.mark.parametrize(("amount", "rate"), [(1000, D("0.1")), (D("1000"), 0.1)])
def test_rejects_non_decimal_values(amount: object, rate: object) -> None:
    with pytest.raises(TypeError, match="must be a Decimal"):
        Credit(amount=amount, rate=rate)  # type: ignore[arg-type]


def test_invalid_credit_is_a_domain_error() -> None:
    assert issubclass(InvalidCreditError, DomainError)
