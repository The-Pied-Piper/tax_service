"""Progressive bracket schedules: a marginal rate per slice of an amount.

A schedule is parameter data, resolved per (family, tax_year); the code holds
no jurisdiction's thresholds or rates. Arithmetic is exact: rounding is the
capability's decision, made with its rounding rule.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from app.domain.errors import InvalidBracketScheduleError
from app.domain.parameters.kind import ParameterKind


@dataclass(frozen=True)
class Bracket:
    """The rate applying to amounts from `lower` up to the next bracket's lower."""

    lower: Decimal
    rate: Decimal

    def __post_init__(self) -> None:
        for name, value in (("lower", self.lower), ("rate", self.rate)):
            if not isinstance(value, Decimal):
                raise TypeError(f"bracket {name} must be a Decimal, got {type(value).__name__}")
            if not value.is_finite():
                raise InvalidBracketScheduleError(f"bracket {name} must be finite, got {value}")
        if self.lower < 0:
            raise InvalidBracketScheduleError(
                f"bracket lower must not be negative, got {self.lower}"
            )
        if not 0 <= self.rate <= 1:
            raise InvalidBracketScheduleError(
                f"bracket rate must be between 0 and 1, got {self.rate}"
            )


@dataclass(frozen=True)
class BracketSlice:
    """The part of an amount falling in one bracket, and the tax on it."""

    lower: Decimal
    upper: Decimal | None
    rate: Decimal
    taxed: Decimal
    tax: Decimal


@dataclass(frozen=True)
class BracketSchedule:
    brackets: tuple[Bracket, ...]

    def __post_init__(self) -> None:
        if not self.brackets:
            raise InvalidBracketScheduleError("a schedule needs at least one bracket")
        if self.brackets[0].lower != 0:
            raise InvalidBracketScheduleError(
                f"the first bracket must start at 0, got {self.brackets[0].lower}"
            )
        for below, above in zip(self.brackets, self.brackets[1:], strict=False):
            if above.lower <= below.lower:
                raise InvalidBracketScheduleError(
                    f"bracket thresholds must be strictly ascending: {above.lower} "
                    f"follows {below.lower}"
                )

    def slices(self, amount: Decimal) -> tuple[BracketSlice, ...]:
        """The non-empty slices of `amount`, lowest bracket first."""
        if not isinstance(amount, Decimal):
            raise TypeError(f"amount must be a Decimal, got {type(amount).__name__}")
        if amount < 0:
            raise ValueError(f"amount must not be negative, got {amount}")
        uppers: list[Decimal | None] = [b.lower for b in self.brackets[1:]] + [None]
        result = []
        for bracket, upper in zip(self.brackets, uppers, strict=True):
            if amount <= bracket.lower:
                break
            taxed = (amount if upper is None else min(amount, upper)) - bracket.lower
            result.append(
                BracketSlice(bracket.lower, upper, bracket.rate, taxed, taxed * bracket.rate)
            )
        return tuple(result)

    def tax_on(self, amount: Decimal) -> Decimal:
        """Exact tax on `amount`: each slice taxed at its bracket's rate."""
        return sum((s.tax for s in self.slices(amount)), Decimal(0))


BRACKETS: ParameterKind[BracketSchedule] = ParameterKind("brackets", BracketSchedule)
