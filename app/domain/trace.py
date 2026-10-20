"""The structured trace: what each capability did, recorded as facts.

A trace line holds the domain objects and amounts involved (`ArtifactKind`, `Rate`, `Credit`,
`Amount`, `ContributionTier`, `Taper`, `Factor`, `Fraction`, `RateTableRow`, `RoundingRule`), never
text; its `amount` is the figure the line is about. A count is an `int` artifact kind and its `int`
value; a chosen rate is a `Rate` artifact kind and its `Rate` value.
Rendering lines as human-readable text lives outside the domain, in the adapters.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction as ExactFraction

from app.domain.artifact import ArtifactKind, Money
from app.domain.parameters.amount import Amount
from app.domain.parameters.claim_reduction import ClaimReduction
from app.domain.parameters.contribution_tier import ContributionTier
from app.domain.parameters.credit import Credit
from app.domain.parameters.factor import Factor
from app.domain.parameters.fraction import Fraction
from app.domain.parameters.rate import Rate
from app.domain.parameters.rate_table import RateTableRow
from app.domain.parameters.rounding import RoundingRule
from app.domain.parameters.taper import Taper
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
