"""Fractions: a fraction of two positive whole numbers, such as a form's "two-thirds".

A rate must be a finite decimal, and two-thirds is not, so a fraction is carried as its numerator
and denominator, kept as given (never reduced), and the one division is left to the capability that
applies it. The code holds no jurisdiction's fractions.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.errors import InvalidFractionError
from app.domain.parameters.kind import ParameterKind


@dataclass(frozen=True)
class Fraction:
    """A fraction of a positive whole numerator and denominator, kept as given; others refused."""

    numerator: int
    denominator: int

    def __post_init__(self) -> None:
        for part, value in (("numerator", self.numerator), ("denominator", self.denominator)):
            # bool is an int subclass; True must not become a part of 1.
            if not isinstance(value, int) or isinstance(value, bool):
                raise TypeError(f"fraction {part} must be an int, got {type(value).__name__}")
            if value <= 0:
                raise InvalidFractionError(f"fraction {part} must be positive, got {value}")


FRACTION: ParameterKind[Fraction] = ParameterKind("fraction", Fraction)
