"""Trace lines for capital cost allowance: one class's claim, recapture, terminal loss and
closing balance, and why a claim is zero.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum

from app.domain.artifact import ArtifactKind, Money
from app.domain.parameters.class_rates import ClassRate
from app.domain.parameters.rounding import RoundingRule
from app.domain.record_list import RecordList
from app.domain.trace.base import TraceLine

__all__ = [
    "CcaZeroReason",
    "CcaClaimLine",
    "RecapturedCcaLine",
    "TerminalLossLine",
    "ClosingUccLine",
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
