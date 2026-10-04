"""Credits: an amount that, multiplied by a rate, reduces tax.

The amount and rate are parameter data, resolved per (family, tax_year); the
code holds no jurisdiction's figures.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from app.domain.errors import InvalidCreditError


@dataclass(frozen=True)
class Credit:
    amount: Decimal
    rate: Decimal

    def __post_init__(self) -> None:
        for name, value in (("amount", self.amount), ("rate", self.rate)):
            if not isinstance(value, Decimal):
                raise TypeError(f"credit {name} must be a Decimal, got {type(value).__name__}")
            if not value.is_finite():
                raise InvalidCreditError(f"credit {name} must be finite, got {value}")
        if self.amount < 0:
            raise InvalidCreditError(f"credit amount must not be negative, got {self.amount}")
        if not 0 <= self.rate <= 1:
            raise InvalidCreditError(f"credit rate must be between 0 and 1, got {self.rate}")

    @property
    def value(self) -> Decimal:
        """The exact reduction in tax: amount × rate."""
        return self.amount * self.rate

    def describe(self) -> str:
        percent = format((self.rate * 100).normalize(), "f")
        return f"{percent}% of {self.amount}"
