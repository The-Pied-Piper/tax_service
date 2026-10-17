"""The structured trace: what each capability did, recorded as facts.

A trace line holds the domain objects and amounts involved (`ArtifactKind`, `Rate`, `Credit`,
`RoundingRule`), never text; its `amount` is the figure the line is about. Rendering lines as
human-readable text lives outside the domain, in the adapters.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal

from app.domain.artifact import Money
from app.domain.parameters.credit import Credit
from app.domain.parameters.rate import Rate
from app.domain.parameters.rounding import RoundingRule


@dataclass(frozen=True)
class TraceLine(ABC):
    """One fact in a capability's explanation of its result; subclasses are frozen dataclasses.

    A dataclass itself (with no fields) so every line supports `dataclasses.fields`.
    """

    @property
    @abstractmethod
    def amount(self) -> Decimal:
        """The figure this line is about."""


@dataclass(frozen=True)
class BracketSliceLine(TraceLine):
    """The part of a base from `lower` to `upper` taxed at `rate`; `upper` is `None` at the top."""

    lower: Decimal
    upper: Decimal | None
    rate: Decimal
    taxed: Decimal
    tax: Decimal

    @property
    def amount(self) -> Decimal:
        """The tax on this slice."""
        return self.tax


@dataclass(frozen=True)
class RoundedTotalLine(TraceLine):
    """The total produced as `output` on `base` (worth `base_amount`), rounded with `rounding`."""

    output: Money
    base: Money
    base_amount: Decimal
    rounding: RoundingRule
    total: Decimal

    @property
    def amount(self) -> Decimal:
        """The rounded total."""
        return self.total


@dataclass(frozen=True)
class CreditLine(TraceLine):
    """A credit worked out as `basis` × `rate`, rounded with `rounding`."""

    basis: Credit
    rate: Rate
    rounding: RoundingRule
    credit: Decimal

    @property
    def amount(self) -> Decimal:
        """The rounded credit."""
        return self.credit


@dataclass(frozen=True)
class CreditAppliedLine(TraceLine):
    """A credit taken off `tax` (worth `tax_amount`), not below zero, producing `output`."""

    output: Money
    tax: Money
    tax_amount: Decimal
    after: Decimal

    @property
    def amount(self) -> Decimal:
        """The tax left after the credit."""
        return self.after


@dataclass(frozen=True)
class UnusedCreditLine(TraceLine):
    """The part of a non-refundable credit that exceeded the tax and was lost."""

    unused: Decimal

    @property
    def amount(self) -> Decimal:
        """The unused part of the credit."""
        return self.unused


@dataclass(frozen=True)
class SumLine(TraceLine):
    """The `total` produced as `output` by adding `parts`, each a kind and its value, in order."""

    output: Money
    parts: tuple[tuple[Money, Decimal], ...]
    total: Decimal

    @property
    def amount(self) -> Decimal:
        """The total of the parts."""
        return self.total


@dataclass(frozen=True)
class RateAppliedLine(TraceLine):
    """The `result` produced as `output` by `base` (worth `base_amount`) × `rate`, rounded."""

    output: Money
    base: Money
    base_amount: Decimal
    rate: Rate
    rounding: RoundingRule
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The rounded product."""
        return self.result


@dataclass(frozen=True)
class SubtractedLine(TraceLine):
    """`output` = `minuend` (worth `minuend_amount`) less `subtrahend` (worth `subtrahend_amount`),
    exact; `result` may be negative."""

    output: Money
    minuend: Money
    minuend_amount: Decimal
    subtrahend: Money
    subtrahend_amount: Decimal
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The difference."""
        return self.result


@dataclass(frozen=True)
class SubtractedNotBelowZeroLine(TraceLine):
    """`output` = `minuend` (worth `minuend_amount`) less `subtrahend` (worth `subtrahend_amount`),
    not below zero: `result` is the exact difference, or 0 when that would not be above zero.

    Its own class, not a `SubtractedLine`: the floor is a different fact, and a renderer or a
    check matching plain subtractions must not catch floored ones.
    """

    output: Money
    minuend: Money
    minuend_amount: Decimal
    subtrahend: Money
    subtrahend_amount: Decimal
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The floored result."""
        return self.result
