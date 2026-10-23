"""BusinessVehicleExpenses: the motor vehicle expenses of Form T2125 Charts A to C, line 9281.

T2125 Part 4 line 9281 "Motor vehicle expenses (not including CCA) (amount 16 of Chart A)", where
Chart A line 16 reads "Allowable motor vehicle expenses: Add amounts 13 to 15 (enter this total on
line 9281 of Part 4)". The charts are filled in for each vehicle, so each record of the consumed
`vehicles` list is one vehicle, worked on its own, and the output is the total of their line 16
amounts, 0 when there are no vehicles. A vehicle works these lines, in this order:

- Chart B line 18 "($350*** ÷ 30) × the number of days in the fiscal period for which interest was
  payable (accrual method) or paid (cash method)" and line 19 "Available interest expense: Amount
  17 or 18, whichever is less (include this in amount 4 of Chart A above)".
- Chart C line 23 "Amount 23 or ($44,706 + GST and PST, or $44,706 + HST), whichever is more",
  where the tax is the printed amount times the `sales_tax_rate` (the caller's GST or HST rate, in
  percent), rounded; line 24 "× 85%"; line 25 "[($1,100 + GST and PST, or $1,100 + HST) × amount
  22] ÷ 30"; line 26 "Amount 25: amount 21"; line 27 "[($38,000 + GST and PST, or $38,000 + HST)
  × amount 20] ÷ amount 24"; and line 28 "Eligible leasing cost: Amount 26 or 27, whichever is less
  (enter in amount 8 of Chart A above)". The form prints no floor on line 26, but line 28 is not
  negative, so a vehicle whose line 26 is below 0 is refused (`CapabilityContractError`).
- Chart A line 12 "Total motor vehicle expenses: Add amounts 3 to 11.", amounts 4 and 8 being
  lines 19 and 28; line 13 "Business use part: amount 1 ÷ amount 2 × amount 12 = 13", 0 when
  amount 2 is 0; and line 16, line 13 plus amount 14 (parking fees) and amount 15 (supplementary
  business insurance).

The printed $350, 30, $44,706, $1,100, $38,000 and 85% are the datasets `interest_limit`,
`days_divisor`, `list_price_limit`, `lease_charge_limit`, `lease_cost_limit` and
`lease_price_rate`. The form states no rounding rule, but each line is a dollars-and-cents box, so
each quotient or product (lines 13, 18, 24, 25 and 27 and the tax on a printed amount) is worked as
an exact fraction and rounded once with the `rounding` dataset's rule. It records one
`BusinessVehicleLine` for each vehicle, by position from 1, then an `ItemsTotalLine`.
"""

from __future__ import annotations

from collections.abc import Mapping
from decimal import Decimal
from fractions import Fraction as ExactFraction
from typing import Any, ClassVar

from app.domain.artifact import Artifact, ArtifactKind, Money
from app.domain.capability import Capability, CapabilityResult, capability
from app.domain.errors import CapabilityContractError, ValidationError
from app.domain.parameters.credit import CREDIT, Credit
from app.domain.parameters.datasets import ParameterDataset
from app.domain.parameters.kind import ParameterKind
from app.domain.parameters.rate import RATE, Rate
from app.domain.parameters.rounding import RoundingRule
from app.domain.parameters.rounding_only import ROUNDING_ONLY, RoundingOnly
from app.domain.record_list import Record, RecordList
from app.domain.trace import ItemsTotalLine
from app.jurisdictions.ca.catalog import (
    BUSINESS_VEHICLE_BUSINESS_KILOMETRES,
    BUSINESS_VEHICLE_ELECTRICITY_ZEV,
    BUSINESS_VEHICLE_FUEL_AND_OIL,
    BUSINESS_VEHICLE_INSURANCE,
    BUSINESS_VEHICLE_INTEREST_DAYS,
    BUSINESS_VEHICLE_INTEREST_PAYABLE,
    BUSINESS_VEHICLE_LEASE_CHARGES,
    BUSINESS_VEHICLE_LEASE_DAYS,
    BUSINESS_VEHICLE_LEASE_PAYMENTS_BEFORE,
    BUSINESS_VEHICLE_LICENCE_AND_REGISTRATION,
    BUSINESS_VEHICLE_LIST_PRICE,
    BUSINESS_VEHICLE_MAINTENANCE_AND_REPAIRS,
    BUSINESS_VEHICLE_OTHER_EXPENSES_10,
    BUSINESS_VEHICLE_OTHER_EXPENSES_11,
    BUSINESS_VEHICLE_PARKING_FEES,
    BUSINESS_VEHICLE_SUPPLEMENTARY_INSURANCE,
    BUSINESS_VEHICLE_TOTAL_KILOMETRES,
)
from app.jurisdictions.ca.trace import BusinessVehicleLine


@capability(identifier="business_vehicle_expenses")
class BusinessVehicleExpenses(Capability):
    """Produces `output`: the total, over the consumed `vehicles`, of each vehicle's allowable
    motor vehicle expenses (Chart A line 16), at the consumed `sales_tax_rate`."""

    PARAMETERS: ClassVar[Mapping[str, ParameterKind[Any]]] = {
        "interest_limit": CREDIT,
        "days_divisor": CREDIT,
        "list_price_limit": CREDIT,
        "lease_charge_limit": CREDIT,
        "lease_cost_limit": CREDIT,
        "lease_price_rate": RATE,
        "rounding": ROUNDING_ONLY,
    }
    CONSUMES: ClassVar[Mapping[str, type]] = {"vehicles": RecordList, "sales_tax_rate": Decimal}
    PRODUCES: ClassVar[Mapping[str, type]] = {"output": Decimal}

    def __init__(
        self,
        interest_limit: ParameterDataset[Credit],
        days_divisor: ParameterDataset[Credit],
        list_price_limit: ParameterDataset[Credit],
        lease_charge_limit: ParameterDataset[Credit],
        lease_cost_limit: ParameterDataset[Credit],
        lease_price_rate: ParameterDataset[Rate],
        rounding: ParameterDataset[RoundingOnly],
        vehicles: ArtifactKind[RecordList],
        sales_tax_rate: Money,
        output: Money,
    ) -> None:
        """Wire the capability: its seven datasets, the record list of vehicles and the sales tax
        rate it reads, the kind produced."""
        super().__init__(vehicles=vehicles, sales_tax_rate=sales_tax_rate, output=output)
        self._interest_limit = interest_limit.values.amount
        self._days_divisor = days_divisor.values.amount
        self._list_price_limit = list_price_limit.values.amount
        self._lease_charge_limit = lease_charge_limit.values.amount
        self._lease_cost_limit = lease_cost_limit.values.amount
        self._lease_price_rate = lease_price_rate.values.value
        self._rate_rounding: RoundingRule = lease_price_rate.rounding
        self._rounding: RoundingRule = rounding.rounding
        self._vehicles = vehicles
        self._sales_tax_rate = sales_tax_rate
        self._output = output

    def compute(self, inputs: tuple[Artifact[Any], ...]) -> CapabilityResult:
        records = self._input(inputs, self._vehicles).value.records
        rate = self._input(inputs, self._sales_tax_rate).value
        lines = tuple(
            self._vehicle(position, record, rate) for position, record in enumerate(records, 1)
        )
        items = tuple((line.position, line.line_16) for line in lines)
        total = sum((amount for _position, amount in items), Decimal(0))
        return CapabilityResult(
            outputs=(Artifact(self._output, total),),
            trace=(*lines, ItemsTotalLine(self._output, items, total)),
        )

    def _vehicle(self, position: int, record: Record, rate: Decimal) -> BusinessVehicleLine:
        """The lines of one vehicle's Charts A to C."""
        # Chart B.
        line_18 = self._quotient(
            self._interest_limit, record[BUSINESS_VEHICLE_INTEREST_DAYS], self._days_divisor
        )
        line_19 = min(Decimal(record[BUSINESS_VEHICLE_INTEREST_PAYABLE]), line_18)
        # Chart C.
        price_with_tax = self._list_price_limit + self._tax(self._list_price_limit, rate)
        line_23 = max(Decimal(record[BUSINESS_VEHICLE_LIST_PRICE]), price_with_tax)
        line_24 = self._rate_rounding.apply(
            ExactFraction(line_23) * ExactFraction(self._lease_price_rate)
        )
        charge_with_tax = self._lease_charge_limit + self._tax(self._lease_charge_limit, rate)
        line_25 = self._quotient(
            charge_with_tax, record[BUSINESS_VEHICLE_LEASE_DAYS], self._days_divisor
        )
        line_26 = line_25 - Decimal(record[BUSINESS_VEHICLE_LEASE_PAYMENTS_BEFORE])
        if line_26 < 0:
            raise CapabilityContractError(f"item {position}: line 26 ({line_26}) is below 0")
        cost_with_tax = self._lease_cost_limit + self._tax(self._lease_cost_limit, rate)
        line_27 = self._quotient(cost_with_tax, record[BUSINESS_VEHICLE_LEASE_CHARGES], line_24)
        line_28 = min(line_26, line_27)
        # Chart A.
        line_12 = (
            Decimal(record[BUSINESS_VEHICLE_FUEL_AND_OIL])
            + line_19
            + Decimal(record[BUSINESS_VEHICLE_INSURANCE])
            + Decimal(record[BUSINESS_VEHICLE_LICENCE_AND_REGISTRATION])
            + Decimal(record[BUSINESS_VEHICLE_MAINTENANCE_AND_REPAIRS])
            + line_28
            + Decimal(record[BUSINESS_VEHICLE_ELECTRICITY_ZEV])
            + Decimal(record[BUSINESS_VEHICLE_OTHER_EXPENSES_10])
            + Decimal(record[BUSINESS_VEHICLE_OTHER_EXPENSES_11])
        )
        total_kilometres = Decimal(record[BUSINESS_VEHICLE_TOTAL_KILOMETRES])
        line_13 = (
            self._quotient(line_12, record[BUSINESS_VEHICLE_BUSINESS_KILOMETRES], total_kilometres)
            if total_kilometres != 0
            else self._rounding.apply(ExactFraction(0))
        )
        line_16 = (
            line_13
            + Decimal(record[BUSINESS_VEHICLE_PARKING_FEES])
            + Decimal(record[BUSINESS_VEHICLE_SUPPLEMENTARY_INSURANCE])
        )
        return BusinessVehicleLine(
            self._output, position, line_12, line_13, line_19, line_28, line_16
        )

    def _tax(self, printed: Decimal, rate: Decimal) -> Decimal:
        """The GST and PST, or HST, on `printed` at `rate` percent, rounded once."""
        return self._rounding.apply(ExactFraction(printed) * ExactFraction(rate) / 100)

    def _quotient(self, amount: Decimal, factor: Decimal, divisor: Decimal) -> Decimal:
        """`amount` × `factor` ÷ `divisor` as an exact fraction, rounded once; a zero divisor is
        refused."""
        if divisor == 0:
            raise ValidationError(f"{amount * factor} cannot be divided by {divisor}")
        return self._rounding.apply(
            ExactFraction(amount) * ExactFraction(factor) / ExactFraction(divisor)
        )
