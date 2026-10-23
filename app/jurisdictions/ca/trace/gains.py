"""Trace lines for gains: a principal residence's taxable gain, its Part 2 lines, and one
disposition's gain or loss.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from app.domain.artifact import Money
from app.domain.parameters.rounding import RoundingRule
from app.domain.trace.base import TraceLine

__all__ = [
    "PrincipalResidenceGainLine",
    "PrincipalResidenceLine27",
    "PrincipalResidenceLine29",
    "PrincipalResidenceLine30",
    "PrincipalResidenceLine32",
    "PrincipalResidenceLine33",
    "PrincipalResidenceLine38",
    "PrincipalResidenceLine39",
    "PrincipalResidenceLine42",
    "PrincipalResidenceLine44",
    "PrincipalResidenceLine45",
    "PrincipalResidenceLine48",
    "PrincipalResidenceLine51",
    "PrincipalResidenceLine53",
    "PrincipalResidenceWorksheetLine3",
    "PrincipalResidenceWorksheetLine6",
    "PrincipalResidenceWorksheetLine16",
    "PrincipalResidenceWorksheetLine17",
    "PrincipalResidenceWorksheetLine18",
    "PrincipalResidenceWorksheetLine19",
    "PrincipalResidenceWorksheetLine21",
    "PrincipalResidenceWorksheetLine23",
    "PrincipalResidenceWorksheetLine24",
    "PrincipalResidenceWorksheetLine26",
    "PrincipalResidenceWorksheetLine27",
    "PrincipalResidenceWorksheetLine59",
    "PrincipalResidenceWorksheetLine61",
    "PrincipalResidenceWorksheetLine63",
    "PrincipalResidenceWorksheetLine64",
    "PrincipalResidenceWorksheetLine66",
    "PrincipalResidenceLine56",
    "PrincipalResidenceLine57",
    "DispositionGainLine",
    "DispositionGainOnlyLine",
    "DispositionProceedsLine",
    "NetCapitalLossesRowLine",
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
    by it; `exempt` (line 23) line 21 divided by the years owned, rounded with `rounding`.

    Part 2: `part_2_applies` (1 if the property is one of two or more principal residences a family
    member owned on December 31, 1981, else 0); `line_53` the net capital gain of Part 2 and
    `line_24` the gain of Part 1 (line 24, not below 0). `result` is line 54, the lesser of
    `line_53` and `line_24` when Part 2 applies, else `line_24`. Lines 14 to 21 are exact.

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
    part_2_applies: int
    line_53: Decimal
    line_24: Decimal
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The property's total capital gain, line 54."""
        return self.result


@dataclass(frozen=True)
class PrincipalResidenceLine27(TraceLine):
    """Form T2091(IND) Part 2 line 27 "Line 25 minus line 26" of the property at `position` (from
    1), for `output`: the fair market value on December 31, 1981 (`line_12`) less the adjusted cost
    base on that date (`line_11`), not floored, `result`. `completed` is False when area A is not
    completed, and then `result` is 0.
    """

    output: Money
    position: int
    completed: bool
    line_12: Decimal
    line_11: Decimal
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The property's line 27."""
        return self.result


@dataclass(frozen=True)
class PrincipalResidenceLine29(TraceLine):
    """Form T2091(IND) Part 2 line 29 "Line 2 plus 1 (see note on page 4)" of the property at
    `position` (from 1), for `output`: the years designated from 1972 to 1981 (`line_2`) plus
    `plus_one`, `result`. `completed` is False when area A is not completed, and then `result` is
    0.
    """

    output: Money
    position: int
    completed: bool
    line_2: int
    plus_one: int
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The property's line 29."""
        return self.result


@dataclass(frozen=True)
class PrincipalResidenceLine30(TraceLine):
    """Form T2091(IND) Part 2 line 30 "Multiply line 28 by line 29." of the property at `position`
    (from 1), for `output`: line 27 (`line_27`) multiplied by line 29 (`line_29`), `result`.
    `completed` is False when area A is not completed, and then `result` is 0.
    """

    output: Money
    position: int
    completed: bool
    line_27: Decimal
    line_29: Decimal
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The property's line 30."""
        return self.result


@dataclass(frozen=True)
class PrincipalResidenceLine32(TraceLine):
    """Form T2091(IND) Part 2 line 32 "Divide line 30 by line 31." of the property at `position`
    (from 1), for `output`: line 30 (`line_30`) divided by the years owned from 1972 to 1981
    (`line_6`), rounded with `rounding`, `result`. `completed` is False when area A is not
    completed, and then `result` is 0.
    """

    output: Money
    position: int
    completed: bool
    line_30: Decimal
    line_6: int
    rounding: RoundingRule
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The property's line 32."""
        return self.result


@dataclass(frozen=True)
class PrincipalResidenceLine33(TraceLine):
    """Form T2091(IND) Part 2 line 33 "Line 27 minus line 32 (if negative, enter "0")" of the
    property at `position` (from 1), for `output`: line 27 (`line_27`) less line 32 (`line_32`), not
    below 0, `result`. `completed` is False when area A is not completed, and then `result` is 0.
    """

    output: Money
    position: int
    completed: bool
    line_27: Decimal
    line_32: Decimal
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The property's line 33, the pre-1982 gain."""
        return self.result


@dataclass(frozen=True)
class PrincipalResidenceLine38(TraceLine):
    """Form T2091(IND) Part 2 line 38 "Add lines 35 to 37." of the property at `position` (from 1),
    for `output`: the fair market value on December 31, 1981 (`line_12`), the adjustments made to
    the cost base after 1981 (`line_13`) and the outlays (`line_9`), added, `result`. `completed` is
    False when area B is not completed, and then `result` is 0.
    """

    output: Money
    position: int
    completed: bool
    line_12: Decimal
    line_13: Decimal
    line_9: Decimal
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The property's line 38."""
        return self.result


@dataclass(frozen=True)
class PrincipalResidenceLine39(TraceLine):
    """Form T2091(IND) Part 2 line 39 "Line 34 minus line 38" of the property at `position` (from
    1), for `output`: the proceeds (`line_8`, line 34) less line 38 (`line_38`), not floored,
    `result`. `completed` is False when area B is not completed, and then `result` is 0.
    """

    output: Money
    position: int
    completed: bool
    line_8: Decimal
    line_38: Decimal
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The property's line 39."""
        return self.result


@dataclass(frozen=True)
class PrincipalResidenceLine42(TraceLine):
    """Form T2091(IND) Part 2 line 42 "Multiply line 40 by line 41." of the property at `position`
    (from 1), for `output`: line 39 (`line_39`) multiplied by the years designated after 1981
    (`line_1`), not floored, `result`. `completed` is False when area B is not completed, and then
    `result` is 0.
    """

    output: Money
    position: int
    completed: bool
    line_39: Decimal
    line_1: int
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The property's line 42."""
        return self.result


@dataclass(frozen=True)
class PrincipalResidenceLine44(TraceLine):
    """Form T2091(IND) Part 2 line 44 "Divide line 42 by line 43." of the property at `position`
    (from 1), for `output`: line 42 (`line_42`) divided by the years owned after 1981 (`line_5`),
    rounded with `rounding`, `result`. `completed` is False when area B is not completed, and then
    `result` is 0.
    """

    output: Money
    position: int
    completed: bool
    line_42: Decimal
    line_5: int
    rounding: RoundingRule
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The property's line 44."""
        return self.result


@dataclass(frozen=True)
class PrincipalResidenceLine45(TraceLine):
    """Form T2091(IND) Part 2 line 45 "Line 39 minus line 44 (if negative, enter "0")" of the
    property at `position` (from 1), for `output`: line 39 (`line_39`) less line 44 (`line_44`), not
    below 0, `result`. `completed` is False when area B is not completed, and then `result` is 0.
    """

    output: Money
    position: int
    completed: bool
    line_39: Decimal
    line_44: Decimal
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The property's line 45, the post-1981 gain."""
        return self.result


@dataclass(frozen=True)
class PrincipalResidenceLine48(TraceLine):
    """Form T2091(IND) Part 2 line 48 "Line 46 minus line 47 (if negative, enter "0")" of the
    property at `position` (from 1), for `output`: the fair market value on December 31, 1981
    (`line_12`, line 46) less the proceeds (`line_8`, line 47), not below 0, `result`. `completed`
    is False when area C is not completed, and then `result` is 0.
    """

    output: Money
    position: int
    completed: bool
    line_12: Decimal
    line_8: Decimal
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The property's line 48, the post-1981 loss."""
        return self.result


@dataclass(frozen=True)
class PrincipalResidenceLine51(TraceLine):
    """Form T2091(IND) Part 2 line 51 "Line 49 plus line 50" of the property at `position` (from
    1), for `output`: the pre-1982 gain (`line_33`, line 49) plus the post-1981 gain (`line_45`,
    line 50), `result`. `completed` is False when Part 2 does not apply, and then `result` is 0.
    """

    output: Money
    position: int
    completed: bool
    line_33: Decimal
    line_45: Decimal
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The property's line 51."""
        return self.result


@dataclass(frozen=True)
class PrincipalResidenceLine53(TraceLine):
    """Form T2091(IND) Part 2 line 53 "Line 51 minus line 52 (if negative, enter "0")" of the
    property at `position` (from 1), for `output`: line 51 (`line_51`) less the post-1981 loss
    (`line_48`, line 52), not below 0, `result`. `completed` is False when Part 2 does not apply,
    and then `result` is 0.
    """

    output: Money
    position: int
    completed: bool
    line_51: Decimal
    line_48: Decimal
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The property's line 53, the net capital gain of Part 2."""
        return self.result


@dataclass(frozen=True)
class PrincipalResidenceWorksheetLine3(TraceLine):
    """Form T2091(IND)-WS line 3 "Total number of years designated before 1995 (line 1 plus line 2)"
    of the property at `position` (from 1), for `output`: the years designated after 1981 and before
    1995 (`line_1`) plus the years designated before 1982 (`line_2`, line 2 of Form T2091(IND)),
    `result`. `completed` is False when the T664 election was not filed, and then `result` is 0.
    """

    output: Money
    position: int
    completed: bool
    line_1: int
    line_2: int
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The property's worksheet line 3."""
        return self.result


@dataclass(frozen=True)
class PrincipalResidenceWorksheetLine6(TraceLine):
    """Form T2091(IND)-WS line 6 "Total number of years owned before 1995 (line 4 plus line 5)" of
    the property at `position` (from 1), for `output`: the years owned after 1981 and before 1995
    (`line_4`) plus the years owned before 1982 (`line_5`, line 6 of Form T2091(IND)), `result`.
    `completed` is False when the T664 election was not filed, and then `result` is 0.
    """

    output: Money
    position: int
    completed: bool
    line_4: int
    line_5: int
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The property's worksheet line 6."""
        return self.result


@dataclass(frozen=True)
class PrincipalResidenceWorksheetLine16(TraceLine):
    """Form T2091(IND)-WS Chart 1 line 16 "Multiply line 14 by 1.1." of the property at `position`
    (from 1), for `output`: line 14 (`line_14`) times the printed factor (`factor`), rounded with
    `rounding`, `result`. `completed` is False unless Chart 1 applies, and then `result` is 0.
    """

    output: Money
    position: int
    completed: bool
    line_14: Decimal
    factor: Decimal
    rounding: RoundingRule
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The property's Chart 1 line 16."""
        return self.result


@dataclass(frozen=True)
class PrincipalResidenceWorksheetLine17(TraceLine):
    """Form T2091(IND)-WS Chart 1 line 17 "Line 15 minus line 16 (if negative, enter "0")" of the
    property at `position` (from 1), for `output`: line 15 (`line_15`) less line 16 (`line_16`), not
    below 0, `result`. `completed` is False unless Chart 1 applies, and then `result` is 0.
    """

    output: Money
    position: int
    completed: bool
    line_15: Decimal
    line_16: Decimal
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The property's Chart 1 line 17."""
        return self.result


@dataclass(frozen=True)
class PrincipalResidenceWorksheetLine18(TraceLine):
    """Form T2091(IND)-WS Chart 1 line 18 "Line 14 minus line 17" of the property at `position`
    (from 1), for `output`: line 14 (`line_14`) less line 17 (`line_17`), `result`, not floored.
    `completed` is False unless Chart 1 applies, and then `result` is 0.
    """

    output: Money
    position: int
    completed: bool
    line_14: Decimal
    line_17: Decimal
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The property's Chart 1 line 18."""
        return self.result


@dataclass(frozen=True)
class PrincipalResidenceWorksheetLine19(TraceLine):
    """Form T2091(IND)-WS line 19 "Enter the amount from line 18 if you completed Chart 1.
    Otherwise, enter the amount from line 10." of the property at `position` (from 1), for `output`:
    line 18 (`line_18`) when `chart_completed`, else line 10 (`line_10`), `result`. `completed` is
    False when the T664 election was not filed, and then `result` is 0.
    """

    output: Money
    position: int
    completed: bool
    chart_completed: bool
    line_18: Decimal
    line_10: Decimal
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The property's worksheet line 19."""
        return self.result


@dataclass(frozen=True)
class PrincipalResidenceWorksheetLine21(TraceLine):
    """Form T2091(IND)-WS line 21 "Line 19 minus line 20" of the property at `position` (from 1),
    for `output`: line 19 (`line_19`) less line 20 (`line_20`), not floored, `result`.
    `completed` is False when the T664 election was not filed, and then `result` is 0.
    """

    output: Money
    position: int
    completed: bool
    line_19: Decimal
    line_20: Decimal
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The property's worksheet line 21, the adjusted gain before the exemption."""
        return self.result


@dataclass(frozen=True)
class PrincipalResidenceWorksheetLine23(TraceLine):
    """Form T2091(IND)-WS line 23 "Line 3 plus 1 (see note below)" of the property at `position`
    (from 1), for `output`: line 3 (`line_3`) plus `plus_one`, `result`. `completed` is False when
    the T664 election was not filed, and then `result` is 0.
    """

    output: Money
    position: int
    completed: bool
    line_3: int
    plus_one: int
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The property's worksheet line 23."""
        return self.result


@dataclass(frozen=True)
class PrincipalResidenceWorksheetLine24(TraceLine):
    """Form T2091(IND)-WS line 24 "Multiply line 22 by line 23." of the property at `position`
    (from 1), for `output`: line 22 (`line_22`) times line 23 (`line_23`), `result`. `completed` is
    False when the T664 election was not filed, and then `result` is 0.
    """

    output: Money
    position: int
    completed: bool
    line_22: Decimal
    line_23: int
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The property's worksheet line 24."""
        return self.result


@dataclass(frozen=True)
class PrincipalResidenceWorksheetLine26(TraceLine):
    """Form T2091(IND)-WS line 26 "Divide line 24 by line 25." of the property at `position` (from
    1), for `output`: line 24 (`line_24`) divided by line 25 (`line_25`), rounded with `rounding`,
    `result`. `completed` is False when the T664 election was not filed, and then `result` is 0.
    """

    output: Money
    position: int
    completed: bool
    line_24: Decimal
    line_25: int
    rounding: RoundingRule
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The property's worksheet line 26."""
        return self.result


@dataclass(frozen=True)
class PrincipalResidenceWorksheetLine27(TraceLine):
    """Form T2091(IND)-WS line 27 "Line 21 minus line 26" of the property at `position` (from 1),
    for `output`: line 21 (`line_21`) less line 26 (`line_26`), not floored, `result`.
    `completed` is False when the T664 election was not filed, and then `result` is 0.
    """

    output: Money
    position: int
    completed: bool
    line_21: Decimal
    line_26: Decimal
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The property's worksheet line 27, the net adjusted gain."""
        return self.result


@dataclass(frozen=True)
class PrincipalResidenceWorksheetLine59(TraceLine):
    """Form T2091(IND)-WS line 59 "Enter the amount from line 27" (Part 2 not built) of the property
    at `position` (from 1), for `output`: line 27 (`line_27`), `result`. `completed` is False when
    the T664 election was not filed, and then `result` is 0.
    """

    output: Money
    position: int
    completed: bool
    line_27: Decimal
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The property's worksheet line 59."""
        return self.result


@dataclass(frozen=True)
class PrincipalResidenceWorksheetLine61(TraceLine):
    """Form T2091(IND)-WS line 61 "Multiply line 59 by line 60." of the property at `position` (from
    1), for `output`: line 59 (`line_59`) times line 60 (`line_60`), `result`. `completed` is False
    when the T664 election was not filed, and then `result` is 0.
    """

    output: Money
    position: int
    completed: bool
    line_59: Decimal
    line_60: int
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The property's worksheet line 61."""
        return self.result


@dataclass(frozen=True)
class PrincipalResidenceWorksheetLine63(TraceLine):
    """Form T2091(IND)-WS line 63 "Divide line 61 by line 62." of the property at `position` (from
    1), for `output`: line 61 (`line_61`) divided by line 62 (`line_62`), rounded with `rounding`,
    `result`. `completed` is False when the T664 election was not filed, and then `result` is 0.
    """

    output: Money
    position: int
    completed: bool
    line_61: Decimal
    line_62: int
    rounding: RoundingRule
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The property's worksheet line 63."""
        return self.result


@dataclass(frozen=True)
class PrincipalResidenceWorksheetLine64(TraceLine):
    """Form T2091(IND)-WS line 64 "Line 59 minus line 63" of the property at `position` (from 1),
    for `output`: line 59 (`line_59`) less line 63 (`line_63`), not floored, `result`.
    `completed` is False when the T664 election was not filed, and then `result` is 0.
    """

    output: Money
    position: int
    completed: bool
    line_59: Decimal
    line_63: Decimal
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The property's worksheet line 64, the total adjusted gain."""
        return self.result


@dataclass(frozen=True)
class PrincipalResidenceWorksheetLine66(TraceLine):
    """Form T2091(IND)-WS line 66 "Enter whichever amount is less: line 64 or line 65." of the
    property at `position` (from 1), for `output`: the lesser of line 64 (`line_64`) and line 65
    (`line_65`, the elected capital gain), `result`. `completed` is False when the T664 election was
    not filed, and then `result` is 0.
    """

    output: Money
    position: int
    completed: bool
    line_64: Decimal
    line_65: Decimal
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The property's worksheet line 66, the reduction as a result of the election."""
        return self.result


@dataclass(frozen=True)
class PrincipalResidenceLine56(TraceLine):
    """Form T2091(IND) Part 4 line 56 "Reduction as a result of the capital gains election (line 66
    of Form T2091(IND)-WS)" of the property at `position` (from 1), for `output`: worksheet line 66
    (`line_66`), `result`. `completed` is False when the T664 election was not filed, and then
    `result` is 0.
    """

    output: Money
    position: int
    completed: bool
    line_66: Decimal
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The property's line 56."""
        return self.result


@dataclass(frozen=True)
class PrincipalResidenceLine57(TraceLine):
    """Form T2091(IND) Part 4 line 57 "Line 55 minus line 56 (if negative, enter "0")" of the
    property at `position` (from 1), for `output`: line 55 (`line_55`, the total capital gain before
    the reduction) less line 56 (`line_56`), not below 0, `result`. It has no `completed` flag, as
    the form has none for it.
    """

    output: Money
    position: int
    line_55: Decimal
    line_56: Decimal
    result: Decimal

    @property
    def amount(self) -> Decimal:
        """The property's line 57, the total capital gain after the election."""
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


@dataclass(frozen=True)
class NetCapitalLossesRowLine(TraceLine):
    """One year row of Form T657 Chart 1, "Calculate your net capital losses of other years (line 14
    of Step 2)", by `position` (from 1), for `output`: the columns A to D the filer enters, column E
    (C minus D, not below 0), column F (B plus E) and column G (A minus F, not below 0), which is
    the amount added to line 14 of Step 2 for the row."""

    output: Money
    position: int
    column_a: Decimal
    column_b: Decimal
    column_c: Decimal
    column_d: Decimal
    column_e: Decimal
    column_f: Decimal
    column_g: Decimal

    @property
    def amount(self) -> Decimal:
        """Column G."""
        return self.column_g
