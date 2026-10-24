"""Trace lines for capital cost allowance: one class's claim, recapture, terminal loss and
closing balance, one class's immediate expensing, and why a claim is zero.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum

from app.domain.artifact import ArtifactKind, Money
from app.domain.parameters.class_rates import ClassRate
from app.domain.parameters.rounding import RoundingRule
from app.domain.record_list import RecordList, RecordListKind
from app.domain.trace.base import TraceLine

__all__ = [
    "CcaZeroReason",
    "CcaClaimLine",
    "RecapturedCcaLine",
    "TerminalLossLine",
    "CcaVehicleProceedsLine",
    "CcaZepvProceedsLine",
    "ClosingUccLine",
    "ImmediateExpensingLine",
    "ImmediateExpensingAgreedLimitLine",
    "FiscalPeriodDaysLine",
    "ProratedByDaysLine",
]


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
    with `rounding`; the claim is the caller's, at most the maximum plus `column_9` (the immediate
    expensing amount, 0 unless the class has a DIEP) and at least `column_9`. Under the
    `half_year_rule_on_sale` (Class 10.1, column 2 above 0, no property left) column 19
    is one half of column 2 and the zero for no property left or a negative column 7 does not apply.
    A `fiscal_period_days` below `full_year_days` (the dataset's days of a full fiscal period, 365
    by default) prorates the maximum (Guide T4002: the CCA "based on the number of days in your
    fiscal period compared to 365 days"); equal to it is no proration.

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
    column_9: Decimal = Decimal(0)
    half_year_rule_on_sale: bool = False
    fiscal_period_days: int = 365
    full_year_days: int = 365

    @property
    def amount(self) -> Decimal:
        """The class's claim."""
        return self.claim


@dataclass(frozen=True)
class RecapturedCcaLine(TraceLine):
    """The recapture `result` of one class, by `position` (from 1), for `output`: `column_7` (the
    UCC after additions and dispositions) made positive when it is negative, which `zero_reason`
    records, else 0, and 0 for a class `class_rate` that recapture does not apply to unless the row
    `has_diep` (it has DIEP additions, column 4), which Note 3 excepts.
    """

    output: Money
    position: int
    class_rate: ClassRate
    column_7: Decimal
    zero_reason: CcaZeroReason
    result: Decimal
    has_diep: bool = False

    @property
    def amount(self) -> Decimal:
        """The class's recapture."""
        return self.result


@dataclass(frozen=True)
class TerminalLossLine(TraceLine):
    """The terminal loss `result` of one class, by `position` (from 1), for `output`: `column_7`
    (the UCC after additions and dispositions) less `column_9` (the immediate expensing amount),
    not below 0, when column 7 is positive with `no_property_left` (1 if no property is left in the
    class, else 0), which `zero_reason` records, else 0, and 0 for a class `class_rate` that a
    terminal loss does not apply to unless the row `has_diep` (it has DIEP additions, column 4),
    which Note 3 excepts. `column_7_positive` records whether column 7 is above 0, so a row with
    property left reads apart from one with nothing to lose. `column_9` is the amount the class
    expensed, which is not deducted as CCA and so is not a terminal loss. A row that used the
    `half_year_rule_on_sale` has no terminal loss.
    """

    output: Money
    position: int
    class_rate: ClassRate
    no_property_left: int
    column_7: Decimal
    zero_reason: CcaZeroReason
    column_7_positive: bool
    result: Decimal
    has_diep: bool = False
    column_9: Decimal = Decimal(0)
    half_year_rule_on_sale: bool = False

    @property
    def amount(self) -> Decimal:
        """The class's terminal loss."""
        return self.result


@dataclass(frozen=True)
class CcaVehicleProceedsLine(TraceLine):
    """The proceeds of one class's vehicle, by `position` (from 1), a record of the list `output`:
    when `applied`, the `proceeds` (column 5) and the `diep_proceeds` (column 6) become the
    `adjusted_proceeds` and the `adjusted_diep_proceeds`, scaled by the `prescribed_amount` (with
    tax) as a proportion of the `actual_cost` of the vehicle (its cost less the government
    assistance), because the cost is more than the prescribed amount (T2125 Area A endnote 2).
    When not `applied`, the adjusted figures are the ones entered: the row has no vehicle year, or
    its actual cost is not more than the prescribed amount. The `prescribed_amount` and the
    `actual_cost` are 0 for a row with no vehicle year.

    Its own class, not a `RecordTotalLine`: each class gives a record of a list, not a part of a
    total.
    """

    output: ArtifactKind[RecordList]
    position: int
    applied: bool
    prescribed_amount: Decimal
    actual_cost: Decimal
    proceeds: Decimal
    adjusted_proceeds: Decimal
    diep_proceeds: Decimal
    adjusted_diep_proceeds: Decimal

    @property
    def amount(self) -> Decimal:
        """The class's proceeds after the adjustment."""
        return self.adjusted_proceeds


@dataclass(frozen=True)
class CcaZepvProceedsLine(TraceLine):
    """The proceeds of one zero-emission passenger vehicle sold from a Class 54 row, by `position`
    of the row and `vehicle` (both from 1), of the list `output`: when `applied`, the `proceeds` and
    the `diep_proceeds` become the `adjusted_proceeds` and the `adjusted_diep_proceeds`, scaled by
    the `prescribed_amount` (with tax) as a proportion of the `actual_cost` of the vehicle (its cost
    less the government assistance), because the cost is more than the prescribed amount (Guide
    T4036 "Class 54 (30%)"). When not `applied`, the adjusted figures are the ones entered: the
    vehicle has no year, or its actual cost is not more than the prescribed amount. The
    `prescribed_amount` and the `actual_cost` are 0 for a vehicle with no year.

    Its own class, not a `RecordTotalLine`: each vehicle gives a part of a record of a list, not a
    part of a total.
    """

    output: ArtifactKind[RecordList]
    position: int
    vehicle: int
    applied: bool
    prescribed_amount: Decimal
    actual_cost: Decimal
    proceeds: Decimal
    adjusted_proceeds: Decimal
    diep_proceeds: Decimal
    adjusted_diep_proceeds: Decimal

    @property
    def amount(self) -> Decimal:
        """The vehicle's proceeds after the adjustment."""
        return self.adjusted_proceeds


@dataclass(frozen=True)
class ClosingUccLine(TraceLine):
    """The UCC at the end of the year `result` of one class, by `position` (from 1), a record of
    the list `output`: `column_7` (the UCC after additions and dispositions) less the `claim`, or
    0 for the `zero_reason` it records when column 7 is negative or is positive with
    `no_property_left` (1 if no property is left in the class `class_rate`, else 0). The `claim`
    includes `column_9`, the immediate expensing amount of the class (0 unless it has a DIEP). A
    row that used the `half_year_rule_on_sale` closes at 0: the rest is not deductible later. A
    `fiscal_period_days` below `full_year_days` (365 by default) says the claim was prorated. The
    `personal_part_remaining` (T776 Area A Note 9, 0 unless the list lists it) is subtracted from
    column 7 less the claim after it.

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
    column_9: Decimal = Decimal(0)
    half_year_rule_on_sale: bool = False
    fiscal_period_days: int = 365
    full_year_days: int = 365
    personal_part_remaining: Decimal = Decimal(0)

    @property
    def amount(self) -> Decimal:
        """The class's UCC at the end of the year."""
        return self.result


@dataclass(frozen=True)
class ImmediateExpensingLine(TraceLine):
    """The immediate expensing amount `column_9` of one class, by `position` (from 1), for
    `output`: the class `class_rate`'s `column_4` (cost of additions that are DIEPs) less
    `column_6` (proceeds of dispositions of DIEP) is `column_8` (the UCC of DIEP), at most
    `column_7` (the UCC after additions and dispositions) and at least 0; the amount is the
    caller's, at most `column_8`.
    """

    output: Money
    position: int
    class_rate: ClassRate
    column_4: Decimal
    column_6: Decimal
    column_7: Decimal
    column_8: Decimal
    column_9: Decimal

    @property
    def amount(self) -> Decimal:
        """The class's immediate expensing amount."""
        return self.column_9


@dataclass(frozen=True)
class ImmediateExpensingAgreedLimitLine(TraceLine):
    """The person's one immediate expensing limit `limit` for `output`, across the statements of
    Forms T776, T2125, T2042 and T2121. `statements` are the statements compared, those claiming
    above 0: each is the kind of the statement's limit list, its position from 1 in that list, its
    claim (the total of column 9) and its limit. Area A endnote 5: "The total immediate expensing
    amount for the tax year (total of column 9) is limited to the lesser of: the immediate
    expensing limit"; Guides T4002 and T4036: "The deduction is limited to $1.5 million per tax
    year". The limit is 0 when no statement claims.
    """

    output: Money
    statements: tuple[tuple[RecordListKind, int, Decimal, Decimal], ...]
    limit: Decimal

    @property
    def amount(self) -> Decimal:
        """The agreed limit."""
        return self.limit


@dataclass(frozen=True)
class FiscalPeriodDaysLine(TraceLine):
    """The days of the fiscal period `fiscal_period_days` for `output`: the days `entered` when
    above 0, else the `full_year_days` of a full year (0 entered is none entered). Guide T4002
    "You were asking?": a fiscal period shorter than `full_year_days` prorates the CCA claim.
    """

    output: ArtifactKind[int]
    entered: int
    fiscal_period_days: int
    full_year_days: int

    @property
    def amount(self) -> Decimal:
        """The days of the fiscal period."""
        return Decimal(self.fiscal_period_days)


@dataclass(frozen=True)
class ProratedByDaysLine(TraceLine):
    """The amount `result` produced as `output`: `amount_kind` (worth `amount_value`) times
    `days_kind` (worth `fiscal_period_days`) over `full_year_days`, rounded once. Guide T4002 and
    Guide T4036, "Immediate expensing incentive": "The limit is also prorated for tax years shorter
    than 365 days". `fiscal_period_days` of `full_year_days` is no proration.
    """

    output: ArtifactKind[Decimal]
    amount_kind: ArtifactKind[Decimal]
    amount_value: Decimal
    days_kind: ArtifactKind[int]
    fiscal_period_days: int
    full_year_days: int
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The prorated amount."""
        return self.result
