"""Trace lines for arithmetic and comparisons: totals and sums, rates, fractions and ratios
applied, differences, caps and bounds, the lesser or greater of figures, quotients and
gates.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from app.domain.artifact import ArtifactKind, Money
from app.domain.parameters.amount import Amount
from app.domain.parameters.credit import Credit
from app.domain.parameters.factor import Factor
from app.domain.parameters.fraction import Fraction
from app.domain.parameters.rate import Rate
from app.domain.parameters.rounding import RoundingRule
from app.domain.parameters.threshold_rate import ThresholdRate
from app.domain.trace.base import TraceLine

__all__ = [
    "RoundedTotalLine",
    "SumLine",
    "SumNotBelowZeroLine",
    "RateAppliedLine",
    "SubtractedLine",
    "SubtractedNotBelowZeroLine",
    "CreditAmountLine",
    "CappedAmountLine",
    "LesserOfLine",
    "GreaterOfLine",
    "PerUnitAmountLine",
    "MultipleOverLine",
    "AtMostLine",
    "FractionAppliedLine",
    "RatioAppliedLine",
    "TimesCountLine",
    "QuotientLine",
    "ThresholdGateLine",
    "AmountOrDividedByRateLine",
]


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
class SumNotBelowZeroLine(TraceLine):
    """The `total` produced as `output` by adding `parts`, each a kind and its value, in order, and
    taking 0 when the sum would not be above zero.

    Its own class, not a `SumLine`: the floor is a different fact, and a renderer or a check
    matching plain sums must not catch floored ones.
    """

    output: Money
    parts: tuple[tuple[Money, Decimal], ...]
    total: Decimal

    @property
    def amount(self) -> Decimal:
        """The floored total."""
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

    Its own class, not a `RateAppliedLine`: no rate is applied, and the amount itself is the result.
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
class GreaterOfLine(TraceLine):
    """The `result` produced as `output`: the greatest of `parts`, each a kind and its value."""

    output: Money
    parts: tuple[tuple[Money, Decimal], ...]
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The greatest of the parts."""
        return self.result


@dataclass(frozen=True)
class PerUnitAmountLine(TraceLine):
    """The `result` produced as `output`: `per_unit` for each of `count` units of `count_kind`,
    rounded once with `rounding`."""

    output: Money
    count_kind: ArtifactKind[int]
    count: int
    per_unit: Amount
    rounding: RoundingRule
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The rounded product."""
        return self.result


@dataclass(frozen=True)
class MultipleOverLine(TraceLine):
    """The `result` produced as `output`: `factor` × `base` (worth `base_amount`) less `less`
    (worth `less_amount`), not below zero, rounded once with `rounding`.

    Its own class, not a `SubtractedNotBelowZeroLine`: the multiple is a different fact.
    """

    output: Money
    base: Money
    base_amount: Decimal
    factor: Factor
    less: Money
    less_amount: Decimal
    rounding: RoundingRule
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The floored, rounded result."""
        return self.result


@dataclass(frozen=True)
class AtMostLine(TraceLine):
    """`output` = `amount_kind` (worth `amount_value`), unchanged, being at most `bound` (worth
    `bound_value`).

    Its own class, not a `LesserOfLine` or `CappedAmountLine`: the amount is not capped, it is
    checked; an amount above its bound is an error, and no line is recorded for it.
    """

    output: Money
    amount_kind: Money
    amount_value: Decimal
    bound: Money
    bound_value: Decimal

    @property
    def amount(self) -> Decimal:
        """The amount, as produced."""
        return self.amount_value


@dataclass(frozen=True)
class FractionAppliedLine(TraceLine):
    """The `result` produced as `output` by `base` (worth `base_amount`) × `fraction`, rounded.

    Its own class, not a `RateAppliedLine`: a fraction is not a rate, and its amount may be
    unrounded (a quotient with no finite decimal expansion is never recorded under no rounding).
    """

    output: Money
    base: Money
    base_amount: Decimal
    fraction: Fraction
    rounding: RoundingRule
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The rounded product."""
        return self.result


@dataclass(frozen=True)
class RatioAppliedLine(TraceLine):
    """The `result` produced as `output` by `amount_kind` (worth `amount_value`) ×
    `numerator_kind` (worth `numerator_value`) / `denominator_kind` (worth `denominator_value`),
    rounded once with `rounding`.

    Its own class, not a `FractionAppliedLine`: the ratio is two artifacts, not a dataset's
    fraction, so the line names the kinds it came from.
    """

    output: Money
    amount_kind: Money
    amount_value: Decimal
    numerator_kind: Money
    numerator_value: Decimal
    denominator_kind: Money
    denominator_value: Decimal
    rounding: RoundingRule
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The rounded quotient."""
        return self.result


@dataclass(frozen=True)
class TimesCountLine(TraceLine):
    """The `result` produced as `output`: `amount_kind` (worth `amount_value`) for each of
    `count` units of `count_kind`, exactly.

    Its own class, not a `PerUnitAmountLine`: the amount is an artifact, not a dataset's amount,
    and the product is never rounded.
    """

    output: Money
    amount_kind: Money
    amount_value: Decimal
    count_kind: ArtifactKind[int]
    count: int
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The exact product."""
        return self.result


@dataclass(frozen=True)
class QuotientLine(TraceLine):
    """The `result` produced as `output`: `dividend` (worth `dividend_amount`) divided by
    `divisor` (worth `divisor_amount`), exactly.

    Its own class, not a `FractionAppliedLine`: both parts are artifacts, no dataset is read and
    nothing is rounded.
    """

    output: Money
    dividend: Money
    dividend_amount: Decimal
    divisor: Money
    divisor_amount: Decimal
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The exact quotient."""
        return self.result


@dataclass(frozen=True)
class ThresholdGateLine(TraceLine):
    """The `result` produced as `output`: `amount_kind` (worth `amount_value`) when `gate_kind`
    (worth `gate_value`) is at least `threshold`, otherwise 0, rounded with `rounding`.

    Its own class, not a `CappedAmountLine`: the gate decides whether the amount passes at all,
    it does not limit it.
    """

    output: Money
    amount_kind: Money
    amount_value: Decimal
    gate_kind: Money
    gate_value: Decimal
    threshold: Amount
    rounding: RoundingRule
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The rounded amount, or 0 when gated off."""
        return self.result


@dataclass(frozen=True)
class AmountOrDividedByRateLine(TraceLine):
    """The figure `result` for `output`: the tested amount passed through, or a figure divided.

    The tested amount (`amount_kind`, `amount_value`) is compared with the `limit`'s threshold.
    At or below it the amount is the result; over it the result is the `dividend_value` of
    `dividend_kind` divided by the limit's rate. Either way it is rounded with `rounding`.

    The tested amount's fields are named `amount_kind` and `amount_value` because `amount` is
    the result.
    """

    output: Money
    amount_kind: Money
    amount_value: Decimal
    dividend_kind: Money
    dividend_value: Decimal
    limit: ThresholdRate
    rounding: RoundingRule
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The figure chosen."""
        return self.result
