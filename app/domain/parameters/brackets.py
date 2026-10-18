"""Progressive bracket schedules: the form's bracket columns over ascending thresholds.

Each bracket holds what a form prints in its column: the threshold it starts from (`lower`), its
`rate` and `tax_at_start`, the tax at the bracket's start as a dollars-and-cents constant. The tax
on an amount is the form's two lines for the bracket the amount falls in: the rate on the excess
over the bracket's lower, plus that constant. An amount at a threshold falls in the lower bracket,
as the columns read "more than ... but not more than ...".

A schedule checks each constant against the exact tax on the brackets below, rounded half-up to
the cent, so a mistyped constant is refused when the schedule is built. A schedule is parameter
data, resolved per (family, tax_year); the code holds no jurisdiction's thresholds, rates or
constants. Arithmetic is exact: rounding the result is the capability's decision, made with its
rounding rule.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import ClassVar

from app.domain.errors import InvalidBracketScheduleError
from app.domain.parameters.kind import ParameterKind
from app.domain.parameters.rounding import RoundingMode, RoundTo


@dataclass(frozen=True)
class Bracket:
    """One column: `rate` on amounts above `lower`, plus `tax_at_start`, the printed constant."""

    lower: Decimal
    rate: Decimal
    tax_at_start: Decimal

    def __post_init__(self) -> None:
        """Check: finite Decimal figures, `lower` and `tax_at_start` >= 0, `rate` in [0, 1]."""
        figures = (("lower", self.lower), ("rate", self.rate), ("tax_at_start", self.tax_at_start))
        for name, value in figures:
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
        if self.tax_at_start < 0:
            raise InvalidBracketScheduleError(
                f"bracket tax_at_start must not be negative, got {self.tax_at_start}"
            )


@dataclass(frozen=True)
class BracketColumn:
    """The column an amount falls in: `rate` on the `excess` over `lower`, plus `tax_at_start`."""

    lower: Decimal
    rate: Decimal
    excess: Decimal
    tax_at_start: Decimal
    tax: Decimal


@dataclass(frozen=True)
class BracketSchedule:
    """Brackets from 0, strictly ascending, each constant the rounded exact tax below it."""

    brackets: tuple[Bracket, ...]

    _CONSTANT_ROUNDING: ClassVar[RoundTo] = RoundTo(Decimal("0.01"), RoundingMode.HALF_UP)

    def __post_init__(self) -> None:
        """Check the thresholds, then each bracket's constant against the exact tax below it."""
        if not self.brackets:
            raise InvalidBracketScheduleError("a schedule needs at least one bracket")
        first = self.brackets[0]
        if first.lower != 0:
            raise InvalidBracketScheduleError(
                f"the first bracket must start at 0, got {first.lower}"
            )
        for below, above in zip(self.brackets, self.brackets[1:], strict=False):
            if above.lower <= below.lower:
                raise InvalidBracketScheduleError(
                    f"bracket thresholds must be strictly ascending: {above.lower} "
                    f"follows {below.lower}"
                )
        if first.tax_at_start != 0:
            raise InvalidBracketScheduleError(
                f"the first bracket's tax_at_start must be 0, got {first.tax_at_start}"
            )
        exact = Decimal(0)
        for below, above in zip(self.brackets, self.brackets[1:], strict=False):
            exact += (above.lower - below.lower) * below.rate
            expected = self._CONSTANT_ROUNDING.apply(exact)
            if above.tax_at_start != expected:
                raise InvalidBracketScheduleError(
                    f"bracket from {above.lower}: tax_at_start {above.tax_at_start} is not the "
                    f"tax on the brackets below rounded half-up to the cent, {expected}"
                )

    def column_for(self, amount: Decimal) -> BracketColumn:
        """The column `amount` falls in, with the rate on its excess plus the bracket's constant."""
        if not isinstance(amount, Decimal):
            raise TypeError(f"amount must be a Decimal, got {type(amount).__name__}")
        if amount < 0:
            raise ValueError(f"amount must not be negative, got {amount}")
        bracket = self.brackets[0]
        for candidate in self.brackets[1:]:
            if amount <= candidate.lower:
                break
            bracket = candidate
        excess = amount - bracket.lower
        return BracketColumn(
            bracket.lower,
            bracket.rate,
            excess,
            bracket.tax_at_start,
            excess * bracket.rate + bracket.tax_at_start,
        )

    def tax_on(self, amount: Decimal) -> Decimal:
        """Exact tax on `amount`: the tax of the column it falls in."""
        return self.column_for(amount).tax


BRACKETS: ParameterKind[BracketSchedule] = ParameterKind("brackets", BracketSchedule)
