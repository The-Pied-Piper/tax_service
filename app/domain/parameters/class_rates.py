"""Class rates: a form's table of classes, each with its rate, its rules and its two factors.

Each class is keyed by its number as printed, an exact `Decimal` so a class such as 10.1 is a
number; it holds its `rate`, whether the half-year rule applies to it or it is exempt, whether
recapture and a terminal loss apply to it or it is excluded, and two factors, the `aiip_factor` and
the `riip_factor`. The factors are `Fraction`s, the `fraction` kind's values, kept as given: a form
can print a factor of 0 as well as one such as seven eighths. The table holds at least one
class, no class number twice (by value), in the order given; a class it does not list is `None`.
The code holds no jurisdiction's tables.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum

from app.domain.errors import InvalidClassRatesError
from app.domain.parameters.fraction import Fraction
from app.domain.parameters.kind import ParameterKind
from app.domain.parameters.rate import Rate


class HalfYearRule(Enum):
    """Whether the half-year rule applies to a class's net additions or the class is exempt."""

    APPLIES = "applies"
    EXEMPT = "exempt"


class RecaptureAndTerminalLoss(Enum):
    """Whether recapture and a terminal loss apply to a class or the class is excluded."""

    APPLIES = "applies"
    EXCLUDED = "excluded"


@dataclass(frozen=True)
class ClassRate:
    """One class: its positive `class_number`, its `rate`, its `half_year_rule`, its
    `recapture_and_terminal_loss` and its `aiip_factor` and `riip_factor`, each a `Fraction`.

    Anything else is refused when it is built.
    """

    class_number: Decimal
    rate: Rate
    half_year_rule: HalfYearRule
    recapture_and_terminal_loss: RecaptureAndTerminalLoss
    aiip_factor: Fraction
    riip_factor: Fraction

    def __post_init__(self) -> None:
        if not isinstance(self.class_number, Decimal):
            raise TypeError(
                f"class_number must be a Decimal, got {type(self.class_number).__name__}"
            )
        if not self.class_number.is_finite():
            raise InvalidClassRatesError(f"class_number must be finite, got {self.class_number}")
        if self.class_number <= 0:
            raise InvalidClassRatesError(f"class_number must be positive, got {self.class_number}")
        if not isinstance(self.rate, Rate):
            raise TypeError(f"rate must be a Rate, got {type(self.rate).__name__}")
        if not isinstance(self.half_year_rule, HalfYearRule):
            raise TypeError(
                f"half_year_rule must be a HalfYearRule, got {type(self.half_year_rule).__name__}"
            )
        if not isinstance(self.recapture_and_terminal_loss, RecaptureAndTerminalLoss):
            raise TypeError(
                "recapture_and_terminal_loss must be a RecaptureAndTerminalLoss, "
                f"got {type(self.recapture_and_terminal_loss).__name__}"
            )
        self._check_factor("aiip_factor", self.aiip_factor)
        self._check_factor("riip_factor", self.riip_factor)

    @staticmethod
    def _check_factor(name: str, value: Fraction) -> None:
        # A `Fraction` checks its own parts.
        if not isinstance(value, Fraction):
            raise TypeError(f"{name} must be a Fraction, got {type(value).__name__}")


@dataclass(frozen=True)
class ClassRates:
    """At least one `ClassRate`, no class number twice, in the order given."""

    classes: tuple[ClassRate, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.classes, tuple):
            raise TypeError(f"classes must be a tuple, got {type(self.classes).__name__}")
        for index, entry in enumerate(self.classes):
            if not isinstance(entry, ClassRate):
                raise TypeError(f"classes[{index}] must be a ClassRate, got {type(entry).__name__}")
        if not self.classes:
            raise InvalidClassRatesError("class rates need at least one class")
        for index, entry in enumerate(self.classes):
            if any(entry.class_number == earlier.class_number for earlier in self.classes[:index]):
                raise InvalidClassRatesError(f"class {entry.class_number} is listed more than once")

    def for_class(self, class_number: Decimal) -> ClassRate | None:
        """The class numbered `class_number`, compared by value, or `None` if it is not listed."""
        for entry in self.classes:
            if entry.class_number == class_number:
                return entry
        return None


CLASS_RATES: ParameterKind[ClassRates] = ParameterKind("class_rates", ClassRates)
