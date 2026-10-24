"""Shared test data for the CcaVehicleProceeds capability, Form T2125 Area A endnote 2.

T2125 (2025), Area A endnote 2: "The proceeds of disposition of a zero-emission passenger vehicle
(ZEPV) that has been included in Class 54, or a passenger vehicle bought after April 18, 2021, that
has been included in Class 10.1, and whose cost is more than the prescribed amount will be adjusted
based on a factor equal to its prescribed amount as a proportion of the actual cost of the vehicle.
For dispositions after July 29, 2019, you will have to adjust the actual cost of the vehicle for
any payments or repayments of government assistance that you may have received or repaid for the
vehicle. If the passenger vehicle in Class 10.1 is not designated for immediate expensing
treatment, this special rule does not apply."

Guide T4002 2025, "Class 10.1 (30%)": "The capital cost limits of a Class 10.1 passenger vehicle
are the following prescribed amounts: $30,000 for vehicles acquired before 2022, plus the GST/HST
or PST; $34,000 for vehicles acquired in 2022, plus the GST/HST or PST; $36,000 for vehicles
acquired in 2023, plus the GST/HST or PST; $37,000 for vehicles acquired in 2024, plus the GST/HST
or PST; $38,000 for vehicles acquired in 2025, plus the GST/HST or PST".

The dataset is a made-up `example.org` dataset of those five prescribed amounts, a `year_amounts`
table with the amount `prescribed_amount` and a half-up rounding to the cent. The list of classes
and the produced list are the catalog's own `ca/business_cca_classes` and
`ca/business_cca_classes_adjusted`; each record of the classes holds the Area A row's columns and
the three fields of the adjustment (the year the vehicle was acquired, 0 when the rule does not
apply to the row, its actual cost and the government assistance received less repaid). The sales
tax rate is the caller's, in percent, the catalog's `ca/business_vehicle_sales_tax_rate`.
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
from app.domain.parameters.datasets import ParameterDataset
from app.domain.parameters.kind import ParameterKind
from app.domain.parameters.rounding import RoundingMode, RoundingRule, RoundTo
from app.domain.parameters.year_amounts import YEAR_AMOUNTS, YearAmounts, YearAmountsRow
from app.domain.record_list import RecordList, RecordListKind
from app.jurisdictions.ca.capabilities.cca_vehicle_proceeds import CcaVehicleProceeds
from app.jurisdictions.ca.catalog import (
    BUSINESS_CCA_CLASSES,
    BUSINESS_CCA_CLASSES_ADJUSTED,
    BUSINESS_VEHICLE_SALES_TAX_RATE,
    CCA_ADDITIONS,
    CCA_AIIP_ADDITIONS,
    CCA_CLAIMED,
    CCA_CLASS_NUMBER,
    CCA_DIEP_ADDITIONS,
    CCA_DIEP_PROCEEDS,
    CCA_HALF_YEAR_RULE_DIFFERS,
    CCA_IMMEDIATE_EXPENSING,
    CCA_NO_PROPERTY_LEFT,
    CCA_PERSONAL_PART_REMAINING,
    CCA_PROCEEDS,
    CCA_RATE_ELECTION,
    CCA_RIIP_ADDITIONS,
    CCA_UCC_AT_START,
    CCA_VEHICLE_ACQUIRED_YEAR,
    CCA_VEHICLE_COST,
    CCA_VEHICLE_GOVERNMENT_ASSISTANCE,
)
from app.jurisdictions.ca.trace import CcaVehicleProceedsLine

D = Decimal
CENT = RoundTo(D("0.01"), RoundingMode.HALF_UP)
SOURCES = ("https://example.org/t4002",)
FAMILY = "ca/cca_vehicle_prescribed_amounts"

CLASSES = BUSINESS_CCA_CLASSES
ADJUSTED = BUSINESS_CCA_CLASSES_ADJUSTED
SALES_TAX_RATE = BUSINESS_VEHICLE_SALES_TAX_RATE

# The three fields of the adjustment, the last of the classes and not in the adjusted list.
VEHICLE_FIELDS = (CCA_VEHICLE_ACQUIRED_YEAR, CCA_VEHICLE_COST, CCA_VEHICLE_GOVERNMENT_ASSISTANCE)

# Guide T4002 "Class 10.1 (30%)": 38,000 for 2025, 37,000 for 2024, 36,000 for 2023, 34,000 for
# 2022 and 30,000 for a vehicle acquired before 2022 (the open-ended row), each plus the tax.
PRESCRIBED = (
    (2025, "38000"),
    (2024, "37000"),
    (2023, "36000"),
    (2022, "34000"),
    (None, "30000"),
)


def prescribed_amounts(
    rounding: RoundingRule = CENT,
    rows: tuple[tuple[int | None, str], ...] = PRESCRIBED,
) -> ParameterDataset[YearAmounts]:
    """The prescribed amounts by year acquired, newest first: (from_year or None, the
    `prescribed_amount`)."""
    table = YearAmounts(
        tuple(YearAmountsRow(year, {"prescribed_amount": D(amount)}) for year, amount in rows)
    )
    return ParameterDataset(FAMILY, 2025, YEAR_AMOUNTS, table, rounding, SOURCES)


def capability(dataset: ParameterDataset[YearAmounts] | None = None) -> CcaVehicleProceeds:
    return CcaVehicleProceeds(dataset or prescribed_amounts(), CLASSES, SALES_TAX_RATE, ADJUSTED)


def row(
    number: str = "10.1",
    ucc_at_start: str = "0",
    additions: str = "0",
    proceeds: str = "0",
    diep_proceeds: str = "0",
    *,
    year: int = 0,
    cost: str = "0",
    assistance: str = "0",
    diep_additions: str = "0",
    immediate_expensing: str = "0",
    claimed: str = "0",
    no_property_left: int = 0,
    personal_part_remaining: str = "0",
    half_year_rule_differs: int = 0,
    rate_election: int = 0,
    aiip_additions: str = "0",
    riip_additions: str = "0",
) -> dict[ArtifactKind[Any], Decimal | int]:
    """One Area A row of the T2125 list: columns 1, 2, 3, 4, 5, 6, 9, 11, 12 and the claim, the
    other flags, and the year, actual cost and government assistance of the adjustment."""
    return {
        CCA_CLASS_NUMBER: D(number),
        CCA_UCC_AT_START: D(ucc_at_start),
        CCA_ADDITIONS: D(additions),
        CCA_DIEP_ADDITIONS: D(diep_additions),
        CCA_PROCEEDS: D(proceeds),
        CCA_DIEP_PROCEEDS: D(diep_proceeds),
        CCA_IMMEDIATE_EXPENSING: D(immediate_expensing),
        CCA_AIIP_ADDITIONS: D(aiip_additions),
        CCA_RIIP_ADDITIONS: D(riip_additions),
        CCA_CLAIMED: D(claimed),
        CCA_NO_PROPERTY_LEFT: no_property_left,
        CCA_PERSONAL_PART_REMAINING: D(personal_part_remaining),
        CCA_HALF_YEAR_RULE_DIFFERS: half_year_rule_differs,
        CCA_RATE_ELECTION: rate_election,
        CCA_VEHICLE_ACQUIRED_YEAR: year,
        CCA_VEHICLE_COST: D(cost),
        CCA_VEHICLE_GOVERNMENT_ASSISTANCE: D(assistance),
    }


def classes(*rows: dict[ArtifactKind[Any], Decimal | int]) -> Artifact[Any]:
    """A `ca/business_cca_classes` artifact of one record per row, in order."""
    assert isinstance(CLASSES, RecordListKind)
    return Artifact(CLASSES, RecordList(CLASSES.fields, rows))


def sales_tax_rate(percent: str = "13") -> Artifact[Any]:
    """The GST or HST rate of the caller's province, in percent."""
    return Artifact(SALES_TAX_RATE, D(percent))


def trace_line(
    position: int,
    applied: bool,
    prescribed_amount: str,
    actual_cost: str,
    proceeds: str,
    adjusted_proceeds: str,
    diep_proceeds: str = "0",
    adjusted_diep_proceeds: str = "0",
) -> CcaVehicleProceedsLine:
    return CcaVehicleProceedsLine(
        ADJUSTED,
        position,
        applied,
        D(prescribed_amount),
        D(actual_cost),
        D(proceeds),
        D(adjusted_proceeds),
        D(diep_proceeds),
        D(adjusted_diep_proceeds),
    )


# Return CV's vehicle (see returns/2025_return_cv.yaml): a Class 10.1 passenger vehicle bought in
# 2025 for 50,000 plus the 13% HST (56,500.00) and sold for 40,000, all of it a DIEP's: the
# prescribed amount with tax is 38,000 + 4,940 = 42,940 and the factor 42,940 / 56,500 = 0.76, so
# the proceeds become 40,000 x 0.76 = 30,400.00.
SOLD = row(
    "10.1",
    additions="42940",
    proceeds="40000",
    diep_proceeds="40000",
    diep_additions="42940",
    year=2025,
    cost="56500.00",
)


class _Jurisdictions:
    def __init__(self, jurisdiction: Jurisdiction) -> None:
        self._jurisdiction = jurisdiction

    def get_jurisdiction(self, code: JurisdictionCode) -> Jurisdiction:
        return self._jurisdiction


class _Parameters:
    def __init__(self, dataset: ParameterDataset[YearAmounts]) -> None:
        self._dataset = dataset

    def get[T](self, family: str, tax_year: int, kind: ParameterKind[T]) -> ParameterDataset[T]:
        if (family, tax_year, kind) != (self._dataset.family, 2025, YEAR_AMOUNTS):
            raise NotFoundError(f"no {family} dataset for tax year {tax_year}")
        return cast(ParameterDataset[T], self._dataset)


def service() -> TaxComputationService:
    """A computation of `ca/cca_vehicle_proceeds` over `ca/business_cca_classes` and the sales
    tax rate, producing `ca/business_cca_classes_adjusted`, wired as the T2125 manifest does."""
    code = JurisdictionCode("CA-ON")
    dataset = prescribed_amounts()
    selection = CapabilitySelection(
        name="ca/cca_vehicle_proceeds",
        params={"prescribed_amounts": dataset.family},
        consumes={"classes": CLASSES.identifier, "sales_tax_rate": SALES_TAX_RATE.identifier},
        produces={"output": ADJUSTED.identifier},
    )
    manifest = Manifest(
        jurisdiction=code,
        version=1,
        valid_from_tax_year=2025,
        inputs=frozenset({CLASSES.identifier, SALES_TAX_RATE.identifier}),
        forms=(
            Form(
                name=code.namespace.identifier("return"),
                instances=None,
                exports=(ADJUSTED.identifier,),
                capabilities=(selection,),
            ),
        ),
    )
    artifacts = ArtifactRegistry()
    for kind in (CLASSES, SALES_TAX_RATE, ADJUSTED):
        artifacts.register(kind.identifier, kind)
    return TaxComputationService(
        _Jurisdictions(Jurisdiction(code=code, manifests=(manifest,))),
        _Parameters(dataset),
        CapabilityRegistry.shared(),
        artifacts,
    )
