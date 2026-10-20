"""The structured trace: what each capability did, recorded as facts.

A trace line holds the domain objects and amounts involved (`ArtifactKind`, `Rate`, `Credit`,
`Amount`, `ContributionTier`, `Taper`, `Factor`, `Fraction`, `RateTableRow`, `ClassRate`,
`RoundingRule`), never text; its `amount` is the figure the line is about. A count is an `int`
artifact kind and its `int` value; a chosen rate is a `Rate` artifact kind and its `Rate` value.
Rendering lines as human-readable text lives outside the domain, in the adapters.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from fractions import Fraction as ExactFraction

from app.domain.artifact import ArtifactKind, Money
from app.domain.parameters.amount import Amount
from app.domain.parameters.claim_reduction import ClaimReduction
from app.domain.parameters.class_rates import ClassRate
from app.domain.parameters.contribution_tier import ContributionTier
from app.domain.parameters.credit import Credit
from app.domain.parameters.factor import Factor
from app.domain.parameters.fraction import Fraction
from app.domain.parameters.rate import Rate
from app.domain.parameters.rate_table import RateTableRow
from app.domain.parameters.rounding import RoundingRule
from app.domain.parameters.taper import Taper
from app.domain.parameters.threshold_rate import ThresholdRate
from app.domain.record_list import RecordList


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
class BracketColumnLine(TraceLine):
    """The bracket a base falls in: `rate` on the `excess` over `lower`, plus `tax_at_start`."""

    lower: Decimal
    rate: Decimal
    excess: Decimal
    tax_at_start: Decimal
    tax: Decimal

    @property
    def amount(self) -> Decimal:
        """The tax the bracket's column gives."""
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


@dataclass(frozen=True)
class SurchargeTierLine(TraceLine):
    """One tier of a surcharge produced as `output`: `rate` of `base` (worth `base_amount`) over
    `threshold`, not below zero, at most the tier's `maximum` when it has one (`None` otherwise),
    rounded with `rounding` to `part`.

    `base_amount` is the whole base, not the part over the threshold; a base that does not reach
    the threshold still gets its line, with a zero part.
    """

    output: Money
    base: Money
    base_amount: Decimal
    threshold: Decimal
    rate: Rate
    rounding: RoundingRule
    part: Decimal
    maximum: Decimal | None = None

    @property
    def amount(self) -> Decimal:
        """The rounded part charged by this tier."""
        return self.part


@dataclass(frozen=True)
class TaperedAmountLine(TraceLine):
    """The `result` produced as `output`: `taper`'s base plus its supplement less `reduction`, not
    below the base, rounded with `rounding`.

    `reduction` is the supplement's share for how far `base` (worth `base_amount`) sits above the
    taper's threshold, recorded as an exact fraction and before the floor at zero, so it can
    exceed the supplement; a base at or below the threshold gets a zero reduction.
    """

    output: Money
    base: Money
    base_amount: Decimal
    taper: Taper
    rounding: RoundingRule
    reduction: ExactFraction
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The tapered amount: the rounded result."""
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
class ChosenByCountLine(TraceLine):
    """`chosen_kind` (worth `chosen_value`) produced as `output`, chosen as `count_kind` is
    `count`: the first candidate for a count of 0, the second for any other count.

    Its own class, not a `TimesCountLine`: the count chooses between two artifacts and scales
    nothing, so the line names the candidate that was chosen; the one not chosen is not recorded.
    """

    output: Money
    count_kind: ArtifactKind[int]
    count: int
    chosen_kind: Money
    chosen_value: Decimal

    @property
    def amount(self) -> Decimal:
        """The chosen value, unchanged."""
        return self.chosen_value


@dataclass(frozen=True)
class AmountByCountLine(TraceLine):
    """The `result` produced as `output`: the table's `row` for `count` of `count_kind`, rounded
    with `rounding`.

    Its own class, not a `CreditAmountLine`: the figure is one row of a table, chosen by a count
    an artifact holds.
    """

    output: Money
    count_kind: ArtifactKind[int]
    count: int
    row: Decimal
    rounding: RoundingRule
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The rounded result."""
        return self.result


@dataclass(frozen=True)
class ItemSumLine(TraceLine):
    """The `total` produced as `output` for the item at `position` (from 1) of a record list, by
    adding `parts`, each a field kind and its value in that item, in order.

    Its own class, not a `SumLine`: the parts are fields of one item, named by its position.
    """

    output: Money
    position: int
    parts: tuple[tuple[Money, Decimal], ...]
    total: Decimal

    @property
    def amount(self) -> Decimal:
        """The total of the item's parts."""
        return self.total


@dataclass(frozen=True)
class ItemLesserOfLine(TraceLine):
    """The `result` for the item at `position` (from 1) of a record list, produced as `output`:
    the least of `parts`, each a field kind and its value in that item, in order.

    Its own class, not a `LesserOfLine`: the parts are fields of one item, named by its position.
    """

    output: Money
    position: int
    parts: tuple[tuple[Money, Decimal], ...]
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The least of the item's parts."""
        return self.result


@dataclass(frozen=True)
class RecordTotalLine(TraceLine):
    """The `total` produced as `output`: `field` added over the items of a record list, in the
    list's order, each item's `amounts` entry its value of `field`, exactly.

    Its own class, not a `SumLine`: the parts are the items of one list, named by position, not
    artifacts of their own.
    """

    output: Money
    field: Money
    amounts: tuple[Decimal, ...]
    total: Decimal

    @property
    def amount(self) -> Decimal:
        """The exact total."""
        return self.total


@dataclass(frozen=True)
class ChosenByRangeLine(TraceLine):
    """`chosen_kind` (worth `chosen_value`) produced as `output`, chosen as `tested_kind` is
    `tested_value`: the first, second or third candidate by the range the tested amount is in.

    Its own class, not a `ChosenByCountLine`: the tested amount is a money amount compared with
    limits, and the line names the candidate that was chosen; the ones not chosen and the limits
    are not recorded.
    """

    output: Money
    tested_kind: Money
    tested_value: Decimal
    chosen_kind: Money
    chosen_value: Decimal

    @property
    def amount(self) -> Decimal:
        """The chosen value, unchanged."""
        return self.chosen_value


@dataclass(frozen=True)
class RateByIncomeBandLine(TraceLine):
    """`rate` produced as `output`, the rate of the table's `row` that `income` (worth
    `income_amount`) falls in; `row` is `None` for a figure of exactly 0, which takes the table's
    rate at zero.

    Its own class, not a `BracketColumnLine` or `SurchargeTierLine`: the row chooses one rate for
    the whole figure, and nothing is charged or rounded.
    """

    output: ArtifactKind[Rate]
    income: Money
    income_amount: Decimal
    row: RateTableRow | None
    rate: Rate

    @property
    def amount(self) -> Decimal:
        """The chosen rate's value."""
        return self.rate.value


@dataclass(frozen=True)
class ChosenRateAppliedLine(TraceLine):
    """The `result` produced as `output` by `base` (worth `base_amount`) × `rate_kind` (worth
    `rate`), rounded once with `rounding`.

    Its own class, not a `RateAppliedLine`: the rate is an artifact chosen earlier, not a rate
    dataset's, so the line names the kind it came from.
    """

    output: Money
    base: Money
    base_amount: Decimal
    rate_kind: ArtifactKind[Rate]
    rate: Rate
    rounding: RoundingRule
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The rounded product."""
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


@dataclass(frozen=True)
class OtherDependantMedicalLine(TraceLine):
    """The allowable amount `result` of medical expenses for one dependant, by `position` (from
    1), for `output`.

    It is the dependant's `expenses` less the `reduction`'s lesser of its ceiling and its rate
    times their `net_income`, from 0 up to the reduction's maximum when it has one, rounded with
    `rounding`.

    Its own class, not a `CaregiverClaimLine`: it is worked on from expenses and a reduction, not
    from a base amount and a maximum.
    """

    output: Money
    position: int
    expenses: Decimal
    net_income: Decimal
    reduction: ClaimReduction
    rounding: RoundingRule
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The dependant's allowable amount."""
        return self.result


@dataclass(frozen=True)
class ShortTermRentalNonCompliantLine(TraceLine):
    """The non-compliant amount `result` of one short-term rental row, by `position` (from 1),
    for `output`.

    It is the row's `related_expenses` times its `non_compliant_days` divided by its `days`, as an
    exact fraction rounded once with `rounding`.
    """

    output: Money
    position: int
    related_expenses: Decimal
    non_compliant_days: int
    days: int
    rounding: RoundingRule
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The row's non-compliant amount."""
        return self.result


@dataclass(frozen=True)
class CaregiverClaimLine(TraceLine):
    """The allowable amount `result` for one dependant, by `position` (from 1), for `output`.

    It is `base` less the dependant's `net_income`, from 0 up to `maximum`, rounded with
    `rounding`.

    Its own class, not a `CappedAmountLine`: the amount is worked on for one dependant, named by
    position, not for an artifact of its own.
    """

    output: Money
    position: int
    base: Amount
    net_income: Decimal
    maximum: Amount
    rounding: RoundingRule
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The dependant's allowable amount."""
        return self.result


@dataclass(frozen=True)
class CaregiverClaimLessClaimedLine(TraceLine):
    """The allowable amount `result` for one dependant, by `position` (from 1), for `output`.

    It is `base` less the dependant's `net_income`, from 0 up to `maximum`, rounded with
    `rounding` to `allowable_before_claimed`, less the `claimed` amount, not below 0.

    Its own class, not a `CaregiverClaimLine`: it also carries the amount claimed for this
    dependant elsewhere, taken off the rounded amount.
    """

    output: Money
    position: int
    base: Amount
    net_income: Decimal
    maximum: Amount
    allowable_before_claimed: Decimal
    claimed: Decimal
    rounding: RoundingRule
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The dependant's allowable amount."""
        return self.result


@dataclass(frozen=True)
class DisabilityTransferLine(TraceLine):
    """The allowable amount `result` for one dependant, by `position` (from 1), for `output`.

    It follows the worksheet for the disability amount transferred from a dependant: `base`
    (line 1), `supplement` (line 2) and `threshold` (line 4) with `maximum` (the cap on line 8);
    the dependant's `under_18` (1 if under 18 on December 31, else 0) and `care_expenses` (line 3);
    `line_5` the expenses over the threshold and `line_6` the supplement less that, each from 0;
    `line_7` the supplement left, or 0 for a dependant 18 or older; `line_8` the base plus line 7,
    at most `maximum`; `credit_amounts` (line 9) and `line_10` their sum with line 8;
    `taxable_income` (line 11) and `line_12` line 10 less it, from 0; and `result` (line 13) the
    lesser of lines 8 and 12, rounded with `rounding`. Lines 5 to 12 are exact.

    Its own class, not a `CappedAmountLine`: the amount is worked on for one dependant, named by
    position, in many steps that the English rendering shows one by one.
    """

    output: Money
    position: int
    base: Amount
    supplement: Amount
    threshold: Amount
    maximum: Amount
    under_18: int
    care_expenses: Decimal
    line_5: Decimal
    line_6: Decimal
    line_7: Decimal
    line_8: Decimal
    credit_amounts: Decimal
    line_10: Decimal
    taxable_income: Decimal
    line_12: Decimal
    rounding: RoundingRule
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The dependant's allowable amount."""
        return self.result


@dataclass(frozen=True)
class PrincipalResidenceGainLine(TraceLine):
    """The taxable gain `result` of one property, by `position` (from 1), for `output`.

    It follows Part 1 of the form designating a property as a principal residence: the years
    designated after 1981 and from 1972 to 1981 (lines 1 and 2) and their total `designated` (line
    3, carried to line 4), the years owned in the same periods (lines 5 and 6) and their total
    `owned` (line 7), and `plus_one` (1 if the "plus one" applies, else 0); `proceeds`,
    `adjusted_cost_base` and `outlays` (lines 8 to 10) and `gain` (line 18) the proceeds less the
    other two; `line_20` the designated years plus the "plus one" and `line_21` the gain multiplied
    by it; `exempt` (line 23) line 21 divided by the years owned, rounded with `rounding`; and
    `result` (line 24) the gain less the exemption, not below 0. Lines 14 to 21 are exact.

    Its own class, not a `DisabilityTransferLine`: the property is worked in steps of its own that
    the English rendering shows one by one.
    """

    output: Money
    position: int
    years_designated_after_1981: int
    years_designated_1972_to_1981: int
    designated: int
    years_owned_after_1981: int
    years_owned_1972_to_1981: int
    owned: int
    plus_one: int
    proceeds: Decimal
    adjusted_cost_base: Decimal
    outlays: Decimal
    gain: Decimal
    line_20: int
    line_21: Decimal
    rounding: RoundingRule
    exempt: Decimal
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The property's taxable gain."""
        return self.result


@dataclass(frozen=True)
class DispositionGainLine(TraceLine):
    """The gain or loss `result` of one disposition, by `position` (from 1), for `output`.

    It follows a row of Schedule 3 Part 3: column 5 "Gain or loss (column 2 minus columns 3 and
    4)", the `proceeds` (column 2) less the `adjusted_cost_base` (column 3) and the `outlays`
    (column 4). A loss is a negative `result`. Exact.

    Its own class, not a `PrincipalResidenceGainLine`: a row has only the three columns and no
    exemption.
    """

    output: Money
    position: int
    proceeds: Decimal
    adjusted_cost_base: Decimal
    outlays: Decimal
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The row's gain or loss, signed."""
        return self.result


@dataclass(frozen=True)
class DispositionGainOnlyLine(TraceLine):
    """The figure `result` counted for one disposition, by `position` (from 1), for `output`.

    It follows a row of Schedule 3 Part 3 whose line is "Total gain only": the `gain` is column 5
    (the `proceeds` less the `adjusted_cost_base` and the `outlays`), and `result` is that gain
    not below 0, a loss counting 0. Exact.

    Its own class, not a `DispositionGainLine`: it carries the gain and the figure counted.
    """

    output: Money
    position: int
    proceeds: Decimal
    adjusted_cost_base: Decimal
    outlays: Decimal
    gain: Decimal
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The figure counted, never negative."""
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
class RecordCountLine(TraceLine):
    """The `count` of the records of the list `records`, produced as `output`."""

    output: ArtifactKind[int]
    records: ArtifactKind[RecordList]
    count: int

    @property
    def amount(self) -> Decimal:
        """The count, as an amount."""
        return Decimal(self.count)


@dataclass(frozen=True)
class PlacementCreditLine(TraceLine):
    """The credit of one item of a record list, produced as part of `output`: the item at
    `position` (from 1) has `field` (the eligible expenditures) worth `expenditure`; its line 1 is
    that at `expenditure_rate`, its line 3 is that at `supplement_rate`, its line 12 is line 3
    multiplied by `remaining_share` (worth `remaining_share_amount`), and its line 13 is the
    lesser of line 1 plus line 12 and `maximum`, rounded with `rounding`.

    `line_1`, `line_3` and `line_12` are exact; `line_13` is rounded. Its own class, not a
    `RecordTotalLine`: each item carries several lines of its own. The total of the items is an
    `ItemsTotalLine`.
    """

    output: Money
    position: int
    field: Money
    expenditure: Decimal
    line_1: Decimal
    line_3: Decimal
    line_12: Decimal
    line_13: Decimal
    remaining_share: Money
    remaining_share_amount: Decimal
    expenditure_rate: Rate
    supplement_rate: Rate
    maximum: Amount
    rounding: RoundingRule

    @property
    def amount(self) -> Decimal:
        """The item's last line, line 13."""
        return self.line_13


@dataclass(frozen=True)
class ItemsTotalLine(TraceLine):
    """The `total` produced as `output` by adding `items`, each the position (from 1) of an item
    of a record list and its amount, in order. No items is a total of 0.

    Its own class, not a `SumLine`: the parts are items of one list, named by position, not
    artifacts of their own.
    """

    output: Money
    items: tuple[tuple[int, Decimal], ...]
    total: Decimal

    @property
    def amount(self) -> Decimal:
        """The exact total."""
        return self.total


class CcaZeroReason(Enum):
    """Why a row of a CCA table allows no claim and closes at a UCC of 0, if it does: column 7 is
    negative, or it is positive with no property left in the class."""

    NONE = "none"
    COLUMN_7_NEGATIVE = "column_7_negative"
    NO_PROPERTY_LEFT = "no_property_left"


@dataclass(frozen=True)
class CcaClaimLine(TraceLine):
    """The capital cost allowance claimed `claim` for one class, by `position` (from 1), for
    `output`.

    It follows one row of a CCA table for the class `class_rate`: `column_7` the UCC after
    additions and dispositions; `column_14` the proceeds available to reduce the incentive
    additions, `column_15` and `column_17` the two incentive adjustments at the class's factors,
    `column_16` the proceeds left for the second, `column_18` the half-year adjustment and
    `column_19` the base amount; `maximum` the class's rate of column 19, or 0 for the
    `zero_reason` it records when column 7 is negative or is positive with `no_property_left` (1
    if no property is left, else 0). Columns 15, 17 and 18 and the maximum are each rounded once
    with `rounding`; the claim is the caller's, at most the maximum.

    Its own class, not a `CappedAmountLine`: the amount is worked on for one class, named by
    position, in many columns that the English rendering shows one by one.
    """

    output: Money
    position: int
    class_rate: ClassRate
    no_property_left: int
    column_7: Decimal
    column_14: Decimal
    column_15: Decimal
    column_16: Decimal
    column_17: Decimal
    column_18: Decimal
    column_19: Decimal
    zero_reason: CcaZeroReason
    maximum: Decimal
    rounding: RoundingRule
    claim: Decimal

    @property
    def amount(self) -> Decimal:
        """The class's claim."""
        return self.claim


@dataclass(frozen=True)
class RecapturedCcaLine(TraceLine):
    """The recapture `result` of one class, by `position` (from 1), for `output`: `column_7` (the
    UCC after additions and dispositions) made positive when it is negative, which `zero_reason`
    records, else 0, and 0 for a class `class_rate` that recapture does not apply to.
    """

    output: Money
    position: int
    class_rate: ClassRate
    column_7: Decimal
    zero_reason: CcaZeroReason
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The class's recapture."""
        return self.result


@dataclass(frozen=True)
class TerminalLossLine(TraceLine):
    """The terminal loss `result` of one class, by `position` (from 1), for `output`: `column_7`
    (the UCC after additions and dispositions) when it is positive with `no_property_left` (1 if
    no property is left in the class, else 0), which `zero_reason` records, else 0, and 0 for a
    class `class_rate` that a terminal loss does not apply to. `column_7_positive` records whether
    column 7 is above 0, so a row with property left reads apart from one with nothing to lose.
    """

    output: Money
    position: int
    class_rate: ClassRate
    no_property_left: int
    column_7: Decimal
    zero_reason: CcaZeroReason
    column_7_positive: bool
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The class's terminal loss."""
        return self.result


@dataclass(frozen=True)
class ClosingUccLine(TraceLine):
    """The UCC at the end of the year `result` of one class, by `position` (from 1), a record of
    the list `output`: `column_7` (the UCC after additions and dispositions) less the `claim`, or
    0 for the `zero_reason` it records when column 7 is negative or is positive with
    `no_property_left` (1 if no property is left in the class `class_rate`, else 0).

    Its own class, not a `RecordTotalLine`: each class gives a record of a list, not a part of a
    total.
    """

    output: ArtifactKind[RecordList]
    position: int
    class_rate: ClassRate
    no_property_left: int
    column_7: Decimal
    zero_reason: CcaZeroReason
    claim: Decimal
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The class's UCC at the end of the year."""
        return self.result


@dataclass(frozen=True)
class ConditionLine(TraceLine):
    """One condition of a list, the `position` (from 1) of the printed `text`, for `output`.

    `reads` holds each figure the condition's tests read, in the order read: the kind and its
    value, a whole number for a count kind and a Decimal for an amount kind. `applies` is whether
    the condition holds.

    Its own class, not a `SumLine`: a condition is a comparison of figures, not a sum.
    """

    output: ArtifactKind[int]
    position: int
    text: str
    reads: tuple[tuple[ArtifactKind[int] | Money, int | Decimal], ...]
    applies: bool

    @property
    def amount(self) -> Decimal:
        """1 when the condition applies, 0 when it does not."""
        return Decimal(1 if self.applies else 0)


@dataclass(frozen=True)
class ConditionsCountLine(TraceLine):
    """The `count` produced as `output` from a list of conditions: `applied` holds the positions
    (from 1) of the conditions that applied, in order, none when no condition applied.

    Its own class, not an `ItemsTotalLine`: the count is one of two whole numbers, chosen by
    whether any condition applied, not a total of amounts.
    """

    output: ArtifactKind[int]
    applied: tuple[int, ...]
    count: int

    @property
    def amount(self) -> Decimal:
        """The count."""
        return Decimal(self.count)
