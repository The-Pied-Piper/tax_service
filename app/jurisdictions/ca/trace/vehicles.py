"""Trace lines for the motor vehicle expenses of Form T2125 Charts A to C: the lines worked for
one vehicle.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from app.domain.artifact import Money
from app.domain.trace.base import TraceLine

__all__ = ["BusinessVehicleLine"]


@dataclass(frozen=True)
class BusinessVehicleLine(TraceLine):
    """The allowable motor vehicle expenses `line_16` of one vehicle, by `position` (from 1), for
    `output`.

    It follows Charts A to C for the vehicle: `line_12` Chart A "Total motor vehicle expenses: Add
    amounts 3 to 11.", `line_13` "Business use part: amount 1 ÷ amount 2 × amount 12 = 13" (0 with
    no total kilometres), `line_19` Chart B "Available interest expense: Amount 17 or 18,
    whichever is less", `line_28` Chart C "Eligible leasing cost: Amount 26 or 27, whichever is
    less" and `line_16` Chart A "Allowable motor vehicle expenses: Add amounts 13 to 15".
    """

    output: Money
    position: int
    line_12: Decimal
    line_13: Decimal
    line_19: Decimal
    line_28: Decimal
    line_16: Decimal

    @property
    def amount(self) -> Decimal:
        """The vehicle's allowable motor vehicle expenses."""
        return self.line_16
