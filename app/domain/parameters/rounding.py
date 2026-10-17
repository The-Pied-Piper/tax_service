"""Rounding rules (design.md §3, Rounding).

Rounding is a parameter, never a jurisdiction constant in code. A capability
decides *where* it rounds; the `RoundingRule` it is given decides *how*. The
default is `NO_ROUNDING`, which leaves amounts exact, so capabilities always call
`apply` at their rounding points and an unconfigured rule changes nothing.

Only exact decimals are accepted. Rounding works on exact fractions, so any
positive increment (0.01, 1, 0.05, ...) rounds without an inexact division.
"""

from __future__ import annotations

import math
from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from fractions import Fraction

from app.domain.errors import InvalidRoundingRuleError

_HALF = Fraction(1, 2)


class RoundingMode(Enum):
    """How an amount between two increments is resolved.

    Values are stable identifiers, used when rules are read from parameter data.
    """

    HALF_UP = "half_up"  # nearest; ties away from zero
    HALF_EVEN = "half_even"  # nearest; ties to the even neighbour
    DOWN = "down"  # toward zero
    UP = "up"  # away from zero
    FLOOR = "floor"  # toward negative infinity
    CEILING = "ceiling"  # toward positive infinity

    def to_integer(self, value: Fraction) -> int:
        """Resolve an exact value to a whole number according to this mode."""
        lower, upper = math.floor(value), math.ceil(value)
        if lower == upper:
            return lower
        toward_zero, away_from_zero = (lower, upper) if value > 0 else (upper, lower)
        match self:
            case RoundingMode.DOWN:
                return toward_zero
            case RoundingMode.UP:
                return away_from_zero
            case RoundingMode.FLOOR:
                return lower
            case RoundingMode.CEILING:
                return upper
        distance = value - lower
        if distance != _HALF:
            return lower if distance < _HALF else upper
        if self is RoundingMode.HALF_UP:
            return away_from_zero
        return lower if lower % 2 == 0 else upper


class RoundingRule(ABC):
    """How a capability rounds an amount. Capabilities depend on this type."""

    @abstractmethod
    def apply(self, amount: Decimal) -> Decimal:
        """Return `amount` rounded by this rule."""

    @staticmethod
    def _check_amount(amount: Decimal) -> None:
        if not isinstance(amount, Decimal):
            raise TypeError(f"amount must be a Decimal, got {type(amount).__name__}")
        if not amount.is_finite():
            raise ValueError(f"amount must be finite, got {amount}")


@dataclass(frozen=True)
class _NoRounding(RoundingRule):
    """The default rule: amounts stay exact. Use `NO_ROUNDING`, never this class.

    A dataclass for value equality: a copy of `NO_ROUNDING` (e.g. after
    serialisation) is still equal to it.
    """

    def apply(self, amount: Decimal) -> Decimal:
        self._check_amount(amount)
        return amount

    def __str__(self) -> str:
        """A developer repr; trace text is rendered by adapters, not by this method."""
        return "no rounding"


NO_ROUNDING: RoundingRule = _NoRounding()


@dataclass(frozen=True)
class RoundTo(RoundingRule):
    """Round to a multiple of `increment` using `mode`.

    The result carries the increment's scale: 7 rounded to 0.01 is 7.00.
    """

    increment: Decimal
    mode: RoundingMode

    def __post_init__(self) -> None:
        if not isinstance(self.increment, Decimal):
            raise TypeError(f"increment must be a Decimal, got {type(self.increment).__name__}")
        if not isinstance(self.mode, RoundingMode):
            raise TypeError(f"mode must be a RoundingMode, got {type(self.mode).__name__}")
        if not self.increment.is_finite() or self.increment <= 0:
            raise InvalidRoundingRuleError(
                f"increment must be a positive finite decimal, got {self.increment}"
            )

    def apply(self, amount: Decimal) -> Decimal:
        self._check_amount(amount)
        steps = self.mode.to_integer(Fraction(amount) / Fraction(self.increment))
        return steps * self.increment

    def __str__(self) -> str:
        """A developer repr; trace text is rendered by adapters, not by this method."""
        return f"{self.mode.value.replace('_', '-')} to {self.increment}"
