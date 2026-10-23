"""Shared test data for the BusinessVehicleExpenses capability, Form T2125 Charts A to C.

The six printed figures and the rounding are made-up `example.org` datasets with the 2025 figures
of the chart lines: "($350*** ÷ 30)" (Chart B line 18), "$44,706" (Chart C line 23), "$1,100"
(line 25) and "$38,000" (line 27), the 85% of line 24 and a half-up rounding to the cent. The
sales tax rate is the artifact of the caller's province, "Use a GST rate of 5% or HST rate
applicable to your province.", given in percent. The record list of vehicles and the produced kind
are the catalog's own `ca/business_vehicles` and `ca/business_motor_vehicle_expenses`; each record
of the vehicles holds the amounts of one vehicle's Charts A to C that the caller enters.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Any, cast

from app.application.services.tax_computation import TaxComputationService
from app.domain.artifact import Artifact, ArtifactKind, ArtifactRegistry
from app.domain.capability import CapabilityRegistry
from app.domain.errors import NotFoundError
from app.domain.jurisdiction import Jurisdiction
from app.domain.jurisdiction_code import JurisdictionCode
from app.domain.manifest import CapabilitySelection, Form, Manifest
from app.domain.parameters.credit import CREDIT, Credit
from app.domain.parameters.datasets import ParameterDataset
from app.domain.parameters.kind import ParameterKind
from app.domain.parameters.rate import RATE, Rate
from app.domain.parameters.rounding import RoundingMode, RoundTo
from app.domain.parameters.rounding_only import ROUNDING_ONLY, RoundingOnly
from app.domain.record_list import RecordList, RecordListKind
from app.jurisdictions.ca.capabilities.business_vehicle_expenses import BusinessVehicleExpenses
from app.jurisdictions.ca.catalog import (
    BUSINESS_MOTOR_VEHICLE_EXPENSES,
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
    BUSINESS_VEHICLE_SALES_TAX_RATE,
    BUSINESS_VEHICLE_SUPPLEMENTARY_INSURANCE,
    BUSINESS_VEHICLE_TOTAL_KILOMETRES,
    BUSINESS_VEHICLES,
)

D = Decimal
CENT = RoundTo(D("0.01"), RoundingMode.HALF_UP)
SOURCES = ("https://example.org/t2125",)

VEHICLES = BUSINESS_VEHICLES
SALES_TAX_RATE = BUSINESS_VEHICLE_SALES_TAX_RATE
MOTOR_VEHICLE_EXPENSES = BUSINESS_MOTOR_VEHICLE_EXPENSES

# The slot names and the dataset families they are wired to, in the capability's slot order.
FAMILIES = {
    "interest_limit": "ca/business_vehicle_interest_limit",
    "days_divisor": "ca/business_vehicle_days_divisor",
    "list_price_limit": "ca/business_vehicle_list_price_limit",
    "lease_charge_limit": "ca/business_vehicle_lease_charge_limit",
    "lease_cost_limit": "ca/business_vehicle_lease_cost_limit",
    "lease_price_rate": "ca/business_vehicle_lease_price_rate",
    "rounding": "ca/business_vehicle_rounding",
}


def credit(family: str, amount: str) -> ParameterDataset[Credit]:
    return ParameterDataset(family, 2025, CREDIT, Credit(amount=D(amount)), CENT, SOURCES)


def datasets() -> dict[str, ParameterDataset[Any]]:
    """The seven datasets, by slot name: the five printed amounts, the 85% and the rounding."""
    return {
        "interest_limit": credit(FAMILIES["interest_limit"], "350"),
        "days_divisor": credit(FAMILIES["days_divisor"], "30"),
        "list_price_limit": credit(FAMILIES["list_price_limit"], "44706"),
        "lease_charge_limit": credit(FAMILIES["lease_charge_limit"], "1100"),
        "lease_cost_limit": credit(FAMILIES["lease_cost_limit"], "38000"),
        "lease_price_rate": ParameterDataset(
            FAMILIES["lease_price_rate"], 2025, RATE, Rate(D("0.85")), CENT, SOURCES
        ),
        "rounding": ParameterDataset(
            FAMILIES["rounding"], 2025, ROUNDING_ONLY, RoundingOnly(), CENT, SOURCES
        ),
    }


def capability(**replaced: ParameterDataset[Any]) -> BusinessVehicleExpenses:
    """The capability over the datasets above (any slot may be replaced by name)."""
    return BusinessVehicleExpenses(
        **{**datasets(), **replaced},
        vehicles=VEHICLES,
        sales_tax_rate=SALES_TAX_RATE,
        output=MOTOR_VEHICLE_EXPENSES,
    )


def vehicle(
    business_kilometres: str = "0",
    total_kilometres: str = "0",
    fuel_and_oil: str = "0",
    insurance: str = "0",
    licence_and_registration: str = "0",
    maintenance_and_repairs: str = "0",
    electricity_zev: str = "0",
    other_expenses_10: str = "0",
    other_expenses_11: str = "0",
    parking_fees: str = "0",
    supplementary_insurance: str = "0",
    interest_payable: str = "0",
    interest_days: str = "0",
    lease_charges: str = "0",
    lease_payments_before: str = "0",
    lease_days: str = "0",
    list_price: str = "0",
) -> dict[ArtifactKind[Any], Decimal]:
    """One vehicle: Chart A amounts 1, 2, 3, 5, 6, 7, 9, 10, 11, 14 and 15, Chart B amount 17 and
    its days, and Chart C amounts 20, 21, 22 and 23."""
    return {
        BUSINESS_VEHICLE_BUSINESS_KILOMETRES: D(business_kilometres),
        BUSINESS_VEHICLE_TOTAL_KILOMETRES: D(total_kilometres),
        BUSINESS_VEHICLE_FUEL_AND_OIL: D(fuel_and_oil),
        BUSINESS_VEHICLE_INSURANCE: D(insurance),
        BUSINESS_VEHICLE_LICENCE_AND_REGISTRATION: D(licence_and_registration),
        BUSINESS_VEHICLE_MAINTENANCE_AND_REPAIRS: D(maintenance_and_repairs),
        BUSINESS_VEHICLE_ELECTRICITY_ZEV: D(electricity_zev),
        BUSINESS_VEHICLE_OTHER_EXPENSES_10: D(other_expenses_10),
        BUSINESS_VEHICLE_OTHER_EXPENSES_11: D(other_expenses_11),
        BUSINESS_VEHICLE_PARKING_FEES: D(parking_fees),
        BUSINESS_VEHICLE_SUPPLEMENTARY_INSURANCE: D(supplementary_insurance),
        BUSINESS_VEHICLE_INTEREST_PAYABLE: D(interest_payable),
        BUSINESS_VEHICLE_INTEREST_DAYS: D(interest_days),
        BUSINESS_VEHICLE_LEASE_CHARGES: D(lease_charges),
        BUSINESS_VEHICLE_LEASE_PAYMENTS_BEFORE: D(lease_payments_before),
        BUSINESS_VEHICLE_LEASE_DAYS: D(lease_days),
        BUSINESS_VEHICLE_LIST_PRICE: D(list_price),
    }


def vehicles(*records: dict[ArtifactKind[Any], Decimal]) -> Artifact[Any]:
    """A `ca/business_vehicles` artifact of one record per vehicle, in order."""
    assert isinstance(VEHICLES, RecordListKind)
    return Artifact(VEHICLES, RecordList(VEHICLES.fields, records))


def sales_tax_rate(percent: str = "13") -> Artifact[Any]:
    """The GST or HST rate of the caller's province, in percent."""
    return Artifact(SALES_TAX_RATE, D(percent))


# Return BB's leased passenger vehicle used half for business (see returns/2025_return_bb.yaml):
# Chart B interest 400 on 183 days, Chart C lease charges 2550 over 183 days at a list price of
# 60000, and a 13% HST rate: line 19 is 400, line 28 is 2147.00, line 12 is 5000 and lines 13 and
# 16 are 2500.
LEASED = vehicle(
    business_kilometres="5000",
    total_kilometres="10000",
    fuel_and_oil="1000",
    insurance="600",
    maintenance_and_repairs="200",
    other_expenses_10="653",
    interest_payable="400",
    interest_days="183",
    lease_charges="2550",
    lease_days="183",
    list_price="60000",
)


class _Jurisdictions:
    def __init__(self, jurisdiction: Jurisdiction) -> None:
        self._jurisdiction = jurisdiction

    def get_jurisdiction(self, code: JurisdictionCode) -> Jurisdiction:
        return self._jurisdiction


class _Parameters:
    def __init__(self, found: dict[str, ParameterDataset[Any]]) -> None:
        self._found = found

    def get[T](self, family: str, tax_year: int, kind: ParameterKind[T]) -> ParameterDataset[T]:
        dataset = self._found.get(family)
        if dataset is None or (tax_year, kind) != (dataset.tax_year, dataset.kind):
            raise NotFoundError(f"no {family} dataset for tax year {tax_year}")
        return cast(ParameterDataset[T], dataset)


def service() -> TaxComputationService:
    """A computation of `ca/business_vehicle_expenses` over `ca/business_vehicles` and the sales
    tax rate, producing `ca/business_motor_vehicle_expenses`, wired as the T2125 manifest does."""
    code = JurisdictionCode("CA-ON")
    found = datasets()
    selection = CapabilitySelection(
        name="ca/business_vehicle_expenses",
        params={slot: dataset.family for slot, dataset in found.items()},
        consumes={"vehicles": VEHICLES.identifier, "sales_tax_rate": SALES_TAX_RATE.identifier},
        produces={"output": MOTOR_VEHICLE_EXPENSES.identifier},
    )
    manifest = Manifest(
        jurisdiction=code,
        version=1,
        valid_from_tax_year=2025,
        inputs=frozenset({VEHICLES.identifier, SALES_TAX_RATE.identifier}),
        forms=(
            Form(
                name=code.namespace.identifier("return"),
                instances=None,
                exports=(MOTOR_VEHICLE_EXPENSES.identifier,),
                capabilities=(selection,),
            ),
        ),
    )
    artifacts = ArtifactRegistry()
    for kind in (VEHICLES, SALES_TAX_RATE, MOTOR_VEHICLE_EXPENSES):
        artifacts.register(kind.identifier, kind)
    return TaxComputationService(
        _Jurisdictions(Jurisdiction(code=code, manifests=(manifest,))),
        _Parameters({dataset.family: dataset for dataset in found.values()}),
        CapabilityRegistry.shared(),
        artifacts,
    )
