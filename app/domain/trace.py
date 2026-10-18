"""The structured trace: what each capability did, recorded as facts.

A trace line holds the domain objects and amounts involved (`ArtifactKind`, `Rate`, `Credit`,
`Amount`, `ContributionTier`, `RoundingRule`), never text; its `amount` is the figure the line is
about. Rendering lines as human-readable text lives outside the domain, in the adapters.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal

from app.domain.artifact import Money
from app.domain.parameters.amount import Amount
from app.domain.parameters.contribution_tier import ContributionTier
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
    """A credit worked out once: `amounts_value` (the value of `amounts`) × `rate`, rounded."""

    amounts: Money
    amounts_value: Decimal
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


@dataclass(frozen=True)
class CreditAmountLine(TraceLine):
    """A credit dataset's amount `basis` produced as `output`, rounded with `rounding` to `value`.

    Its own class, not a `CreditLine`: no rate is applied, and the amount itself is the result.
    """

    output: Money
    basis: Credit
    rounding: RoundingRule
    value: Decimal

    @property
    def amount(self) -> Decimal:
        """The rounded credit amount."""
        return self.value


@dataclass(frozen=True)
class CappedAmountLine(TraceLine):
    """The `result` produced as `output`: the lesser of `base` (worth `base_amount`) and `cap`,
    rounded with `rounding`."""

    output: Money
    base: Money
    base_amount: Decimal
    cap: Amount
    rounding: RoundingRule
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The rounded lesser."""
        return self.result


@dataclass(frozen=True)
class LesserOfLine(TraceLine):
    """The `result` produced as `output`: the least of `parts`, each a kind and its value."""

    output: Money
    parts: tuple[tuple[Money, Decimal], ...]
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The least of the parts."""
        return self.result


@dataclass(frozen=True)
class ContributionTierLine(TraceLine):
    """The `result` produced as `output`: `tier`'s rate on `contributory`, the part of `earnings`
    (worth `earnings_amount`) inside the tier's band, rounded with `rounding`, at most the tier's
    maximum."""

    output: Money
    earnings: Money
    earnings_amount: Decimal
    tier: ContributionTier
    rounding: RoundingRule
    contributory: Decimal
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The contribution: the rounded, capped result."""
        return self.result
