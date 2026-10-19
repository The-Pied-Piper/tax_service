"""Unit tests for the composition root: wiring of services that have no HTTP route yet, the
explicit registration of jurisdiction catalogs it performs (by `build_tax_computation` and at app
startup), and the problem responses it maps domain errors onto."""

from __future__ import annotations

from typing import Any

import pytest

import app.registrations
from app.application.services.tax_computation import TaxComputationService
from app.application.services.widgets_service import WidgetsService
from app.domain.artifact import ArtifactRegistry
from app.domain.errors import (
    CapabilityContractError,
    ConflictError,
    DomainError,
    InputAboveBoundError,
    InvalidCompositionError,
    NegativeArtifactError,
    NotFoundError,
    ValidationError,
)
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
    assert len(computation.compose(JurisdictionCode("CA-ON"), 2025).order) == 117


def test_building_it_registers_the_jurisdiction_catalogs(shared: ArtifactRegistry) -> None:
    assert shared.identifiers() == frozenset()

    build_tax_computation()

    assert {i for i in shared.identifiers() if i.startswith("ca/")} == {
        "ca/employment_income",
        "ca/capital_gain",
        "ca/taxable_capital_gains",
        "ca/total_income",
        "ca/other_employment_income",
        "ca/old_age_security",
        "ca/cpp_or_qpp_benefits",
        "ca/other_pensions_and_superannuation",
        "ca/elected_split_pension_amount",
        "ca/universal_child_care_benefit",
        "ca/ei_and_other_benefits",
        "ca/t3_taxable_dividends_other_than_eligible",
        "ca/t4ps_taxable_dividends_other_than_eligible",
        "ca/t5_taxable_dividends_other_than_eligible",
        "ca/t5013_taxable_dividends_other_than_eligible",
        "ca/t3_taxable_dividends",
        "ca/t4ps_taxable_dividends",
        "ca/t5_taxable_dividends",
        "ca/t5013_taxable_dividends",
        "ca/eligible_dividends_received_without_a_slip",
        "ca/other_dividends_received_without_a_slip",
        "ca/t3_dividend_tax_credit",
        "ca/t4ps_dividend_tax_credit",
        "ca/t5_dividend_tax_credit",
        "ca/t5013_dividend_tax_credit",
        "ca/slip_taxable_dividends_other_than_eligible",
        "ca/slip_taxable_dividends",
        "ca/eligible_dividends_grossed_up",
        "ca/other_dividends_grossed_up",
        "ca/dividends_without_a_slip_grossed_up",
        "ca/taxable_dividends_other_than_eligible",
        "ca/taxable_dividends",
        "ca/slip_dividend_tax_credit",
        "ca/dividends_amount_a",
        "ca/dividends_amount_b",
        "ca/other_dividends_credit",
        "ca/dividends_amount_a_less_b",
        "ca/eligible_dividends_credit",
        "ca/no_slip_dividend_tax_credit",
        "ca/dividend_tax_credit",
        "ca/credits_against_basic_federal_tax",
        "ca/t3_investment_income",
        "ca/t5_investment_income",
        "ca/t5013_investment_income",
        "ca/investment_income_credited_not_received",
        "ca/tax_refund_interest",
        "ca/foreign_investment_income",
        "ca/investment_income_without_a_slip",
        "ca/investment_royalties",
        "ca/investment_income_before_prior_years",
        "ca/investment_income_reported_in_previous_years",
        "ca/interest_and_other_investment_income",
        "ca/net_partnership_income",
        "ca/rdsp_income",
        "ca/taxable_support_payments",
        "ca/rrsp_income",
        "ca/fhsa_income",
        "ca/other_fhsa_income",
        "ca/other_income",
        "ca/taxable_scholarships",
        "ca/workers_compensation_benefits",
        "ca/social_assistance_payments",
        "ca/net_federal_supplements",
        "ca/income_support_benefits",
        "ca/canadian_armed_forces_and_police_deduction",
        "ca/security_options_deductions",
        "ca/uccb_repayment",
        "ca/rdsp_income_repayment",
        "ca/uccb_and_rdsp_income",
        "ca/net_income_less_uccb_and_rdsp_income",
        "ca/uccb_and_rdsp_income_repayments",
        "ca/other_payments_limit_income",
        "ca/other_payments_worksheet_required",
        "ca/other_payments_worksheet_line_9_over_limit",
        "ca/other_payments_deduction_above_limit",
        "ca/other_payments_deduction_after_limit",
        "ca/other_payments_deduction",
        "ca/limited_partnership_losses_of_other_years",
        "ca/non_capital_losses_of_other_years",
        "ca/additional_deductions",
        "ca/unused_rrsp_contributions",
        "ca/rrsp_contributions",
        "ca/rrsp_contributions_available",
        "ca/rrsp_deduction_limit",
        "ca/rrsp_deduction_maximum",
        "ca/rrsp_amount_deducted",
        "ca/rrsp_deduction",
        "ca/unused_rrsp_contributions_carried_forward",
        "ca/union_dues",
        "ca/child_care_expenses_paid",
        "ca/children_under_seven",
        "ca/children_with_disability",
        "ca/children_seven_to_sixteen",
        "ca/child_care_limit_for_children_under_seven",
        "ca/child_care_limit_for_children_with_disability",
        "ca/child_care_limit_for_children_seven_to_sixteen",
        "ca/child_care_basic_limit",
        "ca/child_care_earned_income",
        "ca/child_care_earned_income_limit",
        "ca/child_care_expenses",
        "ca/cpp_first_additional_contributions",
        "ca/cpp_second_additional_contributions",
        "ca/cpp_enhanced_contributions",
        "ca/deductions_from_total_income",
        "ca/net_income",
        "ca/deductions_from_net_income",
        "ca/taxable_income",
        "ca/federal_basic_tax",
        "ca/basic_personal_amount",
        "ca/born_in_1960_or_earlier",
        "ca/age_maximum",
        "ca/age_income_threshold",
        "ca/age_income_over_threshold",
        "ca/age_reduction",
        "ca/age_amount_before_count",
        "ca/age_amount",
        "ca/spouses_claimed",
        "ca/spouse_caregiver_eligible",
        "ca/spouse_net_income",
        "ca/spouse_infirmity_supplement",
        "ca/spouse_amount_basis",
        "ca/spouse_amount_before_count",
        "ca/spouse_amount",
        "ca/eligible_dependants",
        "ca/dependant_net_income",
        "ca/eligible_dependant_amount_before_count",
        "ca/eligible_dependant_amount",
        "ca/spouse_caregiver_base",
        "ca/spouse_caregiver_before_maximum",
        "ca/spouse_caregiver_limit",
        "ca/spouse_caregiver_amount_before_count",
        "ca/spouse_caregiver_amount",
        "ca/infirm_children",
        "ca/infirm_children_amount",
        "ca/cpp_base_contributions",
        "ca/ei_premiums",
        "ca/canada_employment_amount",
        "ca/non_refundable_credit_amounts",
        "ca/non_refundable_tax_credits",
        "ca/federal_tax_after_credits",
        "ca/net_federal_tax",
        "ca/total_payable",
        "ca/income_tax_deducted",
        "ca/cwb_eligible_dependants",
        "ca/working_income",
        "ca/adjusted_family_net_income",
        "ca/cwb_before_reduction_without_dependant",
        "ca/cwb_reduction_without_dependant",
        "ca/canada_workers_benefit_without_dependant",
        "ca/cwb_before_reduction_with_dependant",
        "ca/cwb_reduction_with_dependant",
        "ca/canada_workers_benefit_with_dependant",
        "ca/canada_workers_benefit",
        "ca/provincial_credits",
        "ca/total_credits",
        "ca/refund_or_balance_owing",
    }
    assert {i for i in shared.identifiers() if i.startswith("ca-on/")} == {
        "ca-on/ontario_basic_tax",
        "ca-on/basic_personal_amount",
        "ca-on/eligible_dependant_base",
        "ca-on/eligible_dependant_amount_before_maximum",
        "ca-on/eligible_dependant_amount_before_count",
        "ca-on/eligible_dependant_amount",
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
        "ca-on/lift_credit_before_maximum",
        "ca-on/lift_maximum_credit",
        "ca-on/lift_reduction",
        "ca-on/lift_credit",
        "ca-on/ontario_tax_after_lift_credit",
        "ca-on/community_food_program_donations",
        "ca-on/community_food_program_credit",
        "ca-on/ontario_tax_after_food_credit",
        "ca-on/ontario_health_premium",
        "ca-on/ontario_tax",
        "ca-on/fertility_expenses",
        "ca-on/fertility_credit_before_maximum",
        "ca-on/fertility_credit",
        "ca-on/seniors_transit_paid",
        "ca-on/seniors_transit_amount_paid_at_most_maximum",
        "ca-on/seniors_transit_credit",
        "ca-on/ontario_credits_subtotal",
        "ca-on/ontario_credits",
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
    assert len(computation.compose(JurisdictionCode("CA-ON"), 2025).order) == 117


def test_a_fresh_shared_registry_composes_after_building(shared: ArtifactRegistry) -> None:
    computation = build_tax_computation()

    assert len(computation.compose(JurisdictionCode("CA-ON"), 2025).order) == 117


def test_app_startup_registers_the_jurisdiction_catalogs(shared: ArtifactRegistry) -> None:
    application = create_app(Settings())

    with application.test_client():
        assert shared.get("ca/taxable_income") is TAXABLE_INCOME
        assert shared.get("ca/federal_basic_tax") is FEDERAL_BASIC_TAX


# --- domain errors as problem responses ----------------------------------------------------------


@pytest.mark.parametrize(
    ("error", "status"),
    [
        (NotFoundError, 404),
        (ConflictError, 409),
        (ValidationError, 422),
        (NegativeArtifactError, 422),
        (InputAboveBoundError, 422),
        (CapabilityContractError, 500),
        (InvalidCompositionError, 400),
        (DomainError, 400),
    ],
)
def test_a_domain_error_is_a_problem_response_with_its_status(
    monkeypatch: pytest.MonkeyPatch, error: type[DomainError], status: int
) -> None:
    async def raising(self: WidgetsService, **_: Any) -> Any:
        raise error("ex/made_up went wrong")

    monkeypatch.setattr(WidgetsService, "list_widgets", raising)
    client = create_app(Settings()).test_client()

    response = client.get("/api/v1/widgets")

    assert response.status_code == status
    assert response.headers["content-type"] == "application/problem+json"
    assert response.json()["status"] == status
    assert response.json()["title"] == error.__name__
    assert response.json()["detail"] == "ex/made_up went wrong"
