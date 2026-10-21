"""Trace lines for gains: a principal residence's taxable gain and one disposition's gain or
loss.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from app.domain.artifact import Money
from app.domain.parameters.rounding import RoundingRule
from app.domain.trace.base import TraceLine

__all__ = [
    "PrincipalResidenceGainLine",
    "DispositionGainLine",
    "DispositionGainOnlyLine",
    "DispositionProceedsLine",
]


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
class DispositionProceedsLine(TraceLine):
    """The `proceeds` of one disposition, by `position` (from 1), for `output`.

    It follows a row of Schedule 3 Part 3 whose line is "Total proceeds of disposition": column 2
    "Proceeds of disposition", the figure the row adds. Exact.

    Its own class, not a `DispositionGainLine`: it carries only the proceeds.
    """

    output: Money
    position: int
    proceeds: Decimal

    @property
    def amount(self) -> Decimal:
        """The row's proceeds of disposition."""
        return self.proceeds
