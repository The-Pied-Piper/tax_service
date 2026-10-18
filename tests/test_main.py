"""Unit tests for the composition root: wiring of services that have no HTTP route yet, and the
explicit registration of jurisdiction catalogs it performs (by `build_tax_computation` and at app
startup)."""

from __future__ import annotations

import pytest

import app.registrations
from app.application.services.tax_computation import TaxComputationService
from app.domain.artifact import ArtifactRegistry
from app.domain.jurisdiction_code import JurisdictionCode
from app.jurisdictions.ca.catalog import FEDERAL_BASIC_TAX, TAXABLE_INCOME
from app.main import build_tax_computation, create_app
from app.settings import Settings


@pytest.fixture
def shared(monkeypatch: pytest.MonkeyPatch) -> ArtifactRegistry:
    """A fresh registry standing in for the shared one, so each test registers from scratch."""
    registry = ArtifactRegistry()
    monkeypatch.setattr(ArtifactRegistry, "shared", classmethod(lambda cls: registry))
    return registry


def test_builds_a_tax_computation_over_the_jurisdiction_packages_and_shared_registries() -> None:
    computation = build_tax_computation()

    assert isinstance(computation, TaxComputationService)
    assert len(computation.compose(JurisdictionCode("CA-ON"), 2025).order) == 40


def test_building_it_registers_the_jurisdiction_catalogs(shared: ArtifactRegistry) -> None:
    assert shared.identifiers() == frozenset()

    build_tax_computation()

    assert {i for i in shared.identifiers() if i.startswith("ca/")} == {
        "ca/employment_income",
        "ca/capital_gain",
        "ca/taxable_capital_gains",
        "ca/total_income",
        "ca/unused_rrsp_contributions",
        "ca/rrsp_contributions",
        "ca/rrsp_contributions_available",
        "ca/rrsp_deduction_limit",
        "ca/rrsp_deduction_maximum",
        "ca/rrsp_amount_deducted",
        "ca/rrsp_deduction",
        "ca/unused_rrsp_contributions_carried_forward",
        "ca/union_dues",
        "ca/cpp_first_additional_contributions",
        "ca/cpp_second_additional_contributions",
        "ca/cpp_enhanced_contributions",
        "ca/deductions_from_total_income",
        "ca/net_income",
        "ca/deductions_from_net_income",
        "ca/taxable_income",
        "ca/federal_basic_tax",
        "ca/basic_personal_amount",
        "ca/cpp_base_contributions",
        "ca/ei_premiums",
        "ca/canada_employment_amount",
        "ca/non_refundable_credit_amounts",
        "ca/non_refundable_tax_credits",
        "ca/federal_tax_after_credits",
        "ca/net_federal_tax",
        "ca/total_payable",
        "ca/income_tax_deducted",
        "ca/total_credits",
        "ca/refund_or_balance_owing",
    }
    assert {i for i in shared.identifiers() if i.startswith("ca-on/")} == {
        "ca-on/ontario_basic_tax",
        "ca-on/basic_personal_amount",
        "ca-on/non_refundable_credit_amounts",
        "ca-on/non_refundable_tax_credits",
        "ca-on/ontario_tax_after_credits",
        "ca-on/ontario_surtax",
        "ca-on/ontario_tax_with_surtax",
        "ca-on/tax_reduction_basic",
        "ca-on/dependent_children",
        "ca-on/tax_reduction_for_children",
        "ca-on/dependants",
        "ca-on/tax_reduction_for_dependants",
        "ca-on/tax_reduction_amounts",
        "ca-on/ontario_tax_reduction",
        "ca-on/ontario_tax_after_reduction",
        "ca-on/ontario_health_premium",
        "ca-on/ontario_tax",
    }
    assert shared.get("ca/taxable_income") is TAXABLE_INCOME
    assert shared.get("ca/federal_basic_tax") is FEDERAL_BASIC_TAX


def test_building_it_registers_every_listed_catalog(shared: ArtifactRegistry) -> None:
    expected = ArtifactRegistry()
    app.registrations.JURISDICTIONS.register(expected)

    build_tax_computation()

    assert shared.identifiers() == expected.identifiers()


def test_building_it_twice_is_fine(shared: ArtifactRegistry) -> None:
    build_tax_computation()
    first = shared.identifiers()

    computation = build_tax_computation()

    assert shared.identifiers() == first
    assert len(computation.compose(JurisdictionCode("CA-ON"), 2025).order) == 40


def test_a_fresh_shared_registry_composes_after_building(shared: ArtifactRegistry) -> None:
    computation = build_tax_computation()

    assert len(computation.compose(JurisdictionCode("CA-ON"), 2025).order) == 40


def test_app_startup_registers_the_jurisdiction_catalogs(shared: ArtifactRegistry) -> None:
    application = create_app(Settings())

    with application.test_client():
        assert shared.get("ca/taxable_income") is TAXABLE_INCOME
        assert shared.get("ca/federal_basic_tax") is FEDERAL_BASIC_TAX
