"""CA-ON 2025, end to end: CRA's worked example computed from the manifest through the service.

The service is the one the composition root builds (`build_tax_computation`): the real YAML
sources over the jurisdiction packages and the shared registries. Taxable income of 115000
gives federal basic tax 20146.25, 17807.545 after the basic personal amount credit; Ontario
basic tax 8539.5965, 7895.873 after its credit. No rounding is configured for these lines, so
amounts stay exact.
"""

from __future__ import annotations

from decimal import Decimal
from typing import assert_type

from app.application.services.tax_computation import TaxComputationService
from app.domain.artifact import Artifact
from app.domain.capabilities.non_refundable_credit import NonRefundableCredit
from app.domain.capabilities.progressive_tax import ProgressiveTax
from app.domain.jurisdiction_code import JurisdictionCode
from app.domain.worksheet import Worksheet
from app.jurisdictions.ca.catalog import (
    FEDERAL_BASIC_TAX,
    FEDERAL_TAX_AFTER_CREDITS,
    TAXABLE_INCOME,
)
from app.jurisdictions.ca_on.catalog import ONTARIO_BASIC_TAX, ONTARIO_TAX_AFTER_CREDITS
from app.main import build_tax_computation

D = Decimal
CA_ON = JurisdictionCode("CA-ON")


def service() -> TaxComputationService:
    return build_tax_computation()


def compute(taxable_income: str) -> Worksheet:
    return service().compute(CA_ON, 2025, Artifact(TAXABLE_INCOME, D(taxable_income)))


def test_cra_worked_example_115000() -> None:
    worksheet = compute("115000")

    assert_type(worksheet, Worksheet)
    assert worksheet.get(FEDERAL_BASIC_TAX).value == D("20146.25")
    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("17807.545")
    assert worksheet.get(ONTARIO_BASIC_TAX).value == D("8539.5965")
    assert worksheet.get(ONTARIO_TAX_AFTER_CREDITS).value == D("7895.873")


def test_each_amount_is_produced_by_its_capability() -> None:
    worksheet = compute("115000")

    assert worksheet.producer_of(TAXABLE_INCOME) is None
    assert isinstance(worksheet.producer_of(FEDERAL_BASIC_TAX), ProgressiveTax)
    assert isinstance(worksheet.producer_of(ONTARIO_BASIC_TAX), ProgressiveTax)
    assert isinstance(worksheet.producer_of(FEDERAL_TAX_AFTER_CREDITS), NonRefundableCredit)
    assert isinstance(worksheet.producer_of(ONTARIO_TAX_AFTER_CREDITS), NonRefundableCredit)
    assert worksheet.producer_of(FEDERAL_BASIC_TAX) is not worksheet.producer_of(ONTARIO_BASIC_TAX)


def test_the_trace_explains_the_computation() -> None:
    worksheet = compute("115000")

    def position(label: str, amount: str) -> int:
        """The index of the one trace line starting with `label` that carries `amount`."""
        (found,) = [
            i
            for i, line in enumerate(worksheet.trace)
            if line.description.startswith(label) and line.amount == D(amount)
        ]
        return found

    federal_basic = position("federal_basic_tax", "20146.25")
    federal_after = position("federal_tax_after_credits", "17807.545")
    ontario_basic = position("ontario_basic_tax", "8539.5965")
    ontario_after = position("ontario_tax_after_credits", "7895.873")
    assert federal_basic < federal_after
    assert ontario_basic < ontario_after


def test_each_progressive_tax_runs_before_its_credit() -> None:
    order = service().compose(CA_ON, 2025).order

    assert len(order) == 4
    position = {kind: i for i, capability in enumerate(order) for kind in capability.produces}
    assert position[FEDERAL_BASIC_TAX] < position[FEDERAL_TAX_AFTER_CREDITS]
    assert position[ONTARIO_BASIC_TAX] < position[ONTARIO_TAX_AFTER_CREDITS]


def test_a_credit_larger_than_the_tax_leaves_zero_not_a_refund() -> None:
    worksheet = compute("10000")

    assert worksheet.get(FEDERAL_BASIC_TAX).value == D("1450")
    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("0")
    assert worksheet.get(ONTARIO_TAX_AFTER_CREDITS).value == D("0")
