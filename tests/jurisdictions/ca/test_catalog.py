"""Snapshot of the `ca/` artifact kind identifiers, as the application registers them.

Identifiers are stored with results and exposed by the API, so changing or removing one is a
breaking change: update this snapshot only on purpose. Each package snapshots its own namespace;
declaring a kind in this package's catalog adds it here. The kinds are registered explicitly,
as the composition root does, into a fresh registry.
"""

from __future__ import annotations

from decimal import Decimal

import pytest

import app.jurisdictions.ca
import app.jurisdictions.ca.catalog
from app.domain.artifact import ArtifactCatalog, ArtifactKind, ArtifactRegistry
from app.jurisdictions.ca.catalog import (
    ADJUSTED_FAMILY_NET_INCOME,
    BASIC_PERSONAL_AMOUNT,
    CANADA_EMPLOYMENT_AMOUNT,
    CANADA_WORKERS_BENEFIT,
    CANADA_WORKERS_BENEFIT_WITH_DEPENDANT,
    CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT,
    CAPITAL_GAIN,
    CATALOG,
    CHILD_CARE_BASIC_LIMIT,
    CHILD_CARE_EARNED_INCOME,
    CHILD_CARE_EARNED_INCOME_LIMIT,
    CHILD_CARE_EXPENSES,
    CHILD_CARE_EXPENSES_PAID,
    CHILD_CARE_LIMIT_FOR_CHILDREN_SEVEN_TO_SIXTEEN,
    CHILD_CARE_LIMIT_FOR_CHILDREN_UNDER_SEVEN,
    CHILD_CARE_LIMIT_FOR_CHILDREN_WITH_DISABILITY,
    CHILDREN_SEVEN_TO_SIXTEEN,
    CHILDREN_UNDER_SEVEN,
    CHILDREN_WITH_DISABILITY,
    CPP_BASE_CONTRIBUTIONS,
    CPP_ENHANCED_CONTRIBUTIONS,
    CPP_FIRST_ADDITIONAL_CONTRIBUTIONS,
    CPP_SECOND_ADDITIONAL_CONTRIBUTIONS,
    CWB_BEFORE_REDUCTION_WITH_DEPENDANT,
    CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT,
    CWB_ELIGIBLE_DEPENDANTS,
    CWB_REDUCTION_WITH_DEPENDANT,
    CWB_REDUCTION_WITHOUT_DEPENDANT,
    DEDUCTIONS_FROM_NET_INCOME,
    DEDUCTIONS_FROM_TOTAL_INCOME,
    DEPENDANT_NET_INCOME,
    EI_PREMIUMS,
    ELIGIBLE_DEPENDANT_AMOUNT,
    ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT,
    ELIGIBLE_DEPENDANTS,
    EMPLOYMENT_INCOME,
    FEDERAL_BASIC_TAX,
    INCOME_TAX_DEDUCTED,
    INFIRM_CHILDREN,
    INFIRM_CHILDREN_AMOUNT,
    NET_FEDERAL_TAX,
    NET_INCOME,
    NON_REFUNDABLE_CREDIT_AMOUNTS,
    NON_REFUNDABLE_TAX_CREDITS,
    REFUND_OR_BALANCE_OWING,
    RRSP_AMOUNT_DEDUCTED,
    RRSP_CONTRIBUTIONS,
    RRSP_CONTRIBUTIONS_AVAILABLE,
    RRSP_DEDUCTION,
    RRSP_DEDUCTION_LIMIT,
    RRSP_DEDUCTION_MAXIMUM,
    TAXABLE_CAPITAL_GAINS,
    TAXABLE_INCOME,
    TOTAL_CREDITS,
    TOTAL_INCOME,
    TOTAL_PAYABLE,
    UNION_DUES,
    UNUSED_RRSP_CONTRIBUTIONS,
    UNUSED_RRSP_CONTRIBUTIONS_CARRIED_FORWARD,
    WORKING_INCOME,
)
from app.registrations import JURISDICTIONS

REGISTERED = frozenset(
    {
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
        "ca/eligible_dependants",
        "ca/dependant_net_income",
        "ca/eligible_dependant_amount_before_count",
        "ca/eligible_dependant_amount",
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
        "ca/total_credits",
        "ca/refund_or_balance_owing",
    }
)
# T1 line 167 (line 48400 or 48500): the balance, negative for a refund, the one `ca/` kind that
# may be below zero.
SIGNED = frozenset({"ca/refund_or_balance_owing"})
# T1 line 30400 (Schedule 5, "Each household is allowed only one claim for this amount") and line
# 30499 ("Number of children you are claiming this amount for"): the numbers of eligible
# dependants and of infirm children; and Form T778 Part B lines 1 to 3 ("Number of eligible
# children born in 2019 or later whom the disability amount cannot be claimed for", "... born in
# 2025 or earlier whom the disability amount can be claimed for", "... born in 2009 to 2018"):
# the numbers of eligible children for the child care expenses deduction; and Schedule 6 line 38100
# ("Do you have an eligible dependant? 1 Yes or 2 No"), whose eligible dependant is "your or your
# spouse's or common-law partner's child", "under 19 years of age" and "not eligible for the CWB for
# 2025": the number of eligible dependants for the Canada workers benefit; counted, not money.
COUNTS = frozenset(
    {
        "ca/eligible_dependants",
        "ca/infirm_children",
        "ca/children_under_seven",
        "ca/children_with_disability",
        "ca/children_seven_to_sixteen",
        "ca/cwb_eligible_dependants",
    }
)


@pytest.fixture
def registry() -> ArtifactRegistry:
    registry = ArtifactRegistry()
    JURISDICTIONS.register(registry)
    return registry


def test_registered_identifiers_snapshot(registry: ArtifactRegistry) -> None:
    identifiers = registry.identifiers()

    assert {i for i in identifiers if i.startswith("ca/")} == REGISTERED


def test_the_package_exposes_its_catalog() -> None:
    assert isinstance(app.jurisdictions.ca.catalog.CATALOG, ArtifactCatalog)
    assert app.jurisdictions.ca.catalog.CATALOG is CATALOG
    assert {kind.identifier for kind in CATALOG.kinds} == REGISTERED


def test_catalog_kinds_are_the_registered_ones(registry: ArtifactRegistry) -> None:
    assert registry.get("ca/taxable_income") is TAXABLE_INCOME
    assert registry.get("ca/federal_basic_tax") is FEDERAL_BASIC_TAX
    assert registry.get("ca/employment_income") is EMPLOYMENT_INCOME
    assert registry.get("ca/capital_gain") is CAPITAL_GAIN
    assert registry.get("ca/taxable_capital_gains") is TAXABLE_CAPITAL_GAINS
    assert registry.get("ca/total_income") is TOTAL_INCOME
    assert registry.get("ca/unused_rrsp_contributions") is UNUSED_RRSP_CONTRIBUTIONS
    assert registry.get("ca/rrsp_contributions") is RRSP_CONTRIBUTIONS
    assert registry.get("ca/rrsp_contributions_available") is RRSP_CONTRIBUTIONS_AVAILABLE
    assert registry.get("ca/rrsp_deduction_limit") is RRSP_DEDUCTION_LIMIT
    assert registry.get("ca/rrsp_deduction_maximum") is RRSP_DEDUCTION_MAXIMUM
    assert registry.get("ca/rrsp_amount_deducted") is RRSP_AMOUNT_DEDUCTED
    assert registry.get("ca/rrsp_deduction") is RRSP_DEDUCTION
    assert (
        registry.get("ca/unused_rrsp_contributions_carried_forward")
        is UNUSED_RRSP_CONTRIBUTIONS_CARRIED_FORWARD
    )
    assert registry.get("ca/union_dues") is UNION_DUES
    assert registry.get("ca/cpp_enhanced_contributions") is CPP_ENHANCED_CONTRIBUTIONS
    assert (
        registry.get("ca/cpp_first_additional_contributions") is CPP_FIRST_ADDITIONAL_CONTRIBUTIONS
    )
    assert (
        registry.get("ca/cpp_second_additional_contributions")
        is CPP_SECOND_ADDITIONAL_CONTRIBUTIONS
    )
    assert registry.get("ca/child_care_expenses_paid") is CHILD_CARE_EXPENSES_PAID
    assert registry.get("ca/children_under_seven") is CHILDREN_UNDER_SEVEN
    assert registry.get("ca/children_with_disability") is CHILDREN_WITH_DISABILITY
    assert registry.get("ca/children_seven_to_sixteen") is CHILDREN_SEVEN_TO_SIXTEEN
    assert (
        registry.get("ca/child_care_limit_for_children_under_seven")
        is CHILD_CARE_LIMIT_FOR_CHILDREN_UNDER_SEVEN
    )
    assert (
        registry.get("ca/child_care_limit_for_children_with_disability")
        is CHILD_CARE_LIMIT_FOR_CHILDREN_WITH_DISABILITY
    )
    assert (
        registry.get("ca/child_care_limit_for_children_seven_to_sixteen")
        is CHILD_CARE_LIMIT_FOR_CHILDREN_SEVEN_TO_SIXTEEN
    )
    assert registry.get("ca/child_care_basic_limit") is CHILD_CARE_BASIC_LIMIT
    assert registry.get("ca/child_care_earned_income") is CHILD_CARE_EARNED_INCOME
    assert registry.get("ca/child_care_earned_income_limit") is CHILD_CARE_EARNED_INCOME_LIMIT
    assert registry.get("ca/child_care_expenses") is CHILD_CARE_EXPENSES
    assert registry.get("ca/deductions_from_total_income") is DEDUCTIONS_FROM_TOTAL_INCOME
    assert registry.get("ca/net_income") is NET_INCOME
    assert registry.get("ca/deductions_from_net_income") is DEDUCTIONS_FROM_NET_INCOME
    assert registry.get("ca/basic_personal_amount") is BASIC_PERSONAL_AMOUNT
    assert registry.get("ca/eligible_dependants") is ELIGIBLE_DEPENDANTS
    assert registry.get("ca/dependant_net_income") is DEPENDANT_NET_INCOME
    assert (
        registry.get("ca/eligible_dependant_amount_before_count")
        is ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT
    )
    assert registry.get("ca/eligible_dependant_amount") is ELIGIBLE_DEPENDANT_AMOUNT
    assert registry.get("ca/infirm_children") is INFIRM_CHILDREN
    assert registry.get("ca/infirm_children_amount") is INFIRM_CHILDREN_AMOUNT
    assert registry.get("ca/non_refundable_credit_amounts") is NON_REFUNDABLE_CREDIT_AMOUNTS
    assert registry.get("ca/cpp_base_contributions") is CPP_BASE_CONTRIBUTIONS
    assert registry.get("ca/ei_premiums") is EI_PREMIUMS
    assert registry.get("ca/canada_employment_amount") is CANADA_EMPLOYMENT_AMOUNT
    assert registry.get("ca/non_refundable_tax_credits") is NON_REFUNDABLE_TAX_CREDITS
    assert registry.get("ca/net_federal_tax") is NET_FEDERAL_TAX
    assert registry.get("ca/total_payable") is TOTAL_PAYABLE
    assert registry.get("ca/income_tax_deducted") is INCOME_TAX_DEDUCTED
    assert registry.get("ca/cwb_eligible_dependants") is CWB_ELIGIBLE_DEPENDANTS
    assert registry.get("ca/working_income") is WORKING_INCOME
    assert registry.get("ca/adjusted_family_net_income") is ADJUSTED_FAMILY_NET_INCOME
    assert (
        registry.get("ca/cwb_before_reduction_without_dependant")
        is CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT
    )
    assert registry.get("ca/cwb_reduction_without_dependant") is CWB_REDUCTION_WITHOUT_DEPENDANT
    assert (
        registry.get("ca/canada_workers_benefit_without_dependant")
        is CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT
    )
    assert (
        registry.get("ca/cwb_before_reduction_with_dependant")
        is CWB_BEFORE_REDUCTION_WITH_DEPENDANT
    )
    assert registry.get("ca/cwb_reduction_with_dependant") is CWB_REDUCTION_WITH_DEPENDANT
    assert (
        registry.get("ca/canada_workers_benefit_with_dependant")
        is CANADA_WORKERS_BENEFIT_WITH_DEPENDANT
    )
    assert registry.get("ca/canada_workers_benefit") is CANADA_WORKERS_BENEFIT
    assert registry.get("ca/total_credits") is TOTAL_CREDITS
    assert registry.get("ca/refund_or_balance_owing") is REFUND_OR_BALANCE_OWING


def test_catalog_kinds_are_in_the_package_namespace() -> None:
    for kind in CATALOG.kinds:
        assert kind.identifier.startswith(f"{app.jurisdictions.ca.NAMESPACE}/")


def test_catalog_kinds_are_money() -> None:
    assert TAXABLE_INCOME.value_type is Decimal
    assert FEDERAL_BASIC_TAX.value_type is Decimal
    for kind in (
        EMPLOYMENT_INCOME,
        CAPITAL_GAIN,
        TAXABLE_CAPITAL_GAINS,
        TOTAL_INCOME,
        UNUSED_RRSP_CONTRIBUTIONS,
        RRSP_CONTRIBUTIONS,
        RRSP_CONTRIBUTIONS_AVAILABLE,
        RRSP_DEDUCTION_LIMIT,
        RRSP_DEDUCTION_MAXIMUM,
        RRSP_AMOUNT_DEDUCTED,
        RRSP_DEDUCTION,
        UNUSED_RRSP_CONTRIBUTIONS_CARRIED_FORWARD,
        UNION_DUES,
        CHILD_CARE_EXPENSES_PAID,
        CHILD_CARE_LIMIT_FOR_CHILDREN_UNDER_SEVEN,
        CHILD_CARE_LIMIT_FOR_CHILDREN_WITH_DISABILITY,
        CHILD_CARE_LIMIT_FOR_CHILDREN_SEVEN_TO_SIXTEEN,
        CHILD_CARE_BASIC_LIMIT,
        CHILD_CARE_EARNED_INCOME,
        CHILD_CARE_EARNED_INCOME_LIMIT,
        CHILD_CARE_EXPENSES,
        CPP_FIRST_ADDITIONAL_CONTRIBUTIONS,
        CPP_SECOND_ADDITIONAL_CONTRIBUTIONS,
        CPP_ENHANCED_CONTRIBUTIONS,
        DEDUCTIONS_FROM_TOTAL_INCOME,
        NET_INCOME,
        DEDUCTIONS_FROM_NET_INCOME,
        BASIC_PERSONAL_AMOUNT,
        DEPENDANT_NET_INCOME,
        ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT,
        ELIGIBLE_DEPENDANT_AMOUNT,
        INFIRM_CHILDREN_AMOUNT,
        NON_REFUNDABLE_CREDIT_AMOUNTS,
        CPP_BASE_CONTRIBUTIONS,
        EI_PREMIUMS,
        CANADA_EMPLOYMENT_AMOUNT,
        NON_REFUNDABLE_TAX_CREDITS,
        NET_FEDERAL_TAX,
        TOTAL_PAYABLE,
        INCOME_TAX_DEDUCTED,
        WORKING_INCOME,
        ADJUSTED_FAMILY_NET_INCOME,
        CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT,
        CWB_REDUCTION_WITHOUT_DEPENDANT,
        CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT,
        CWB_BEFORE_REDUCTION_WITH_DEPENDANT,
        CWB_REDUCTION_WITH_DEPENDANT,
        CANADA_WORKERS_BENEFIT_WITH_DEPENDANT,
        CANADA_WORKERS_BENEFIT,
        TOTAL_CREDITS,
        REFUND_OR_BALANCE_OWING,
    ):
        assert kind.value_type is Decimal, kind.identifier


def test_every_registered_kind_but_the_counts_is_money(registry: ArtifactRegistry) -> None:
    for identifier in REGISTERED - COUNTS:
        kind = registry.get(identifier)
        assert isinstance(kind, ArtifactKind)
        assert kind.value_type is Decimal, identifier


def test_the_counts_are_int_kinds_in_the_package_namespace(registry: ArtifactRegistry) -> None:
    assert COUNTS <= REGISTERED
    for identifier in COUNTS:
        kind = registry.get(identifier)
        assert isinstance(kind, ArtifactKind)
        assert kind.identifier.startswith(f"{app.jurisdictions.ca.NAMESPACE}/")
        assert kind.value_type is int, identifier


def test_every_kind_but_the_balance_is_declared_non_negative(registry: ArtifactRegistry) -> None:
    # No other `ca/` line can be negative on the forms as modelled.
    for kind in CATALOG.kinds:
        if kind.identifier not in SIGNED:
            assert kind.non_negative is True, kind.identifier
    for identifier in REGISTERED - SIGNED:
        assert registry.kind(identifier).non_negative is True, identifier


def test_the_refund_or_balance_owing_is_signed(registry: ArtifactRegistry) -> None:
    # T1 line 167 "Line 149 minus line 166 If the amount is negative, enter it on line 48400
    # below. If the amount is positive, enter it on line 48500 below. Refund or balance owing":
    # negative is a refund, so the kind is not declared non-negative.
    assert REFUND_OR_BALANCE_OWING.non_negative is False
    assert registry.kind("ca/refund_or_balance_owing").non_negative is False
    assert SIGNED <= REGISTERED


def test_the_income_tax_deducted_is_non_negative() -> None:
    # T1 line 150 (line 43700) "Total income tax deducted (amounts from all Canadian slips)".
    assert INCOME_TAX_DEDUCTED.non_negative is True


def test_the_rrsp_amount_deducted_is_non_negative() -> None:
    # Schedule 7 line 18 "Enter your RRSP, PRPP, or SPP contributions you are deducting for 2025
    # (cannot be more than the amount on line 17).": an amount the filer states.
    assert RRSP_AMOUNT_DEDUCTED.non_negative is True


def test_capital_gain_is_non_negative_while_losses_are_not_modelled() -> None:
    assert CAPITAL_GAIN.non_negative is True
