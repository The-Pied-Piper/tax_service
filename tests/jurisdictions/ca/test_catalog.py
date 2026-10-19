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
    ADDITIONAL_DEDUCTIONS,
    ADJUSTED_FAMILY_NET_INCOME,
    AGE_AMOUNT,
    AGE_AMOUNT_BEFORE_COUNT,
    AGE_INCOME_OVER_THRESHOLD,
    AGE_INCOME_THRESHOLD,
    AGE_MAXIMUM,
    AGE_REDUCTION,
    BASIC_PERSONAL_AMOUNT,
    BORN_IN_1960_OR_EARLIER,
    CANADA_EMPLOYMENT_AMOUNT,
    CANADA_WORKERS_BENEFIT,
    CANADA_WORKERS_BENEFIT_WITH_DEPENDANT,
    CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT,
    CANADIAN_ARMED_FORCES_AND_POLICE_DEDUCTION,
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
    CPP_OR_QPP_BENEFITS,
    CPP_SECOND_ADDITIONAL_CONTRIBUTIONS,
    CREDITS_AGAINST_BASIC_FEDERAL_TAX,
    CWB_BEFORE_REDUCTION_WITH_DEPENDANT,
    CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT,
    CWB_ELIGIBLE_DEPENDANTS,
    CWB_REDUCTION_WITH_DEPENDANT,
    CWB_REDUCTION_WITHOUT_DEPENDANT,
    DEDUCTIONS_FROM_NET_INCOME,
    DEDUCTIONS_FROM_TOTAL_INCOME,
    DEPENDANT_NET_INCOME,
    DIVIDEND_TAX_CREDIT,
    DIVIDENDS_AMOUNT_A,
    DIVIDENDS_AMOUNT_A_LESS_B,
    DIVIDENDS_AMOUNT_B,
    DIVIDENDS_WITHOUT_A_SLIP_GROSSED_UP,
    EI_AND_OTHER_BENEFITS,
    EI_PREMIUMS,
    ELECTED_SPLIT_PENSION_AMOUNT,
    ELIGIBLE_DEPENDANT_AMOUNT,
    ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT,
    ELIGIBLE_DEPENDANTS,
    ELIGIBLE_DIVIDENDS_CREDIT,
    ELIGIBLE_DIVIDENDS_GROSSED_UP,
    ELIGIBLE_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP,
    EMPLOYMENT_INCOME,
    FEDERAL_BASIC_TAX,
    FHSA_INCOME,
    FOREIGN_INVESTMENT_INCOME,
    INCOME_SUPPORT_BENEFITS,
    INCOME_TAX_DEDUCTED,
    INFIRM_CHILDREN,
    INFIRM_CHILDREN_AMOUNT,
    INTEREST_AND_OTHER_INVESTMENT_INCOME,
    INVESTMENT_INCOME_BEFORE_PRIOR_YEARS,
    INVESTMENT_INCOME_CREDITED_NOT_RECEIVED,
    INVESTMENT_INCOME_REPORTED_IN_PREVIOUS_YEARS,
    INVESTMENT_INCOME_WITHOUT_A_SLIP,
    INVESTMENT_ROYALTIES,
    LIMITED_PARTNERSHIP_LOSSES_OF_OTHER_YEARS,
    NET_FEDERAL_SUPPLEMENTS,
    NET_FEDERAL_TAX,
    NET_INCOME,
    NET_INCOME_LESS_UCCB_AND_RDSP_INCOME,
    NET_PARTNERSHIP_INCOME,
    NO_SLIP_DIVIDEND_TAX_CREDIT,
    NON_CAPITAL_LOSSES_OF_OTHER_YEARS,
    NON_REFUNDABLE_CREDIT_AMOUNTS,
    NON_REFUNDABLE_TAX_CREDITS,
    OLD_AGE_SECURITY,
    OTHER_DIVIDENDS_CREDIT,
    OTHER_DIVIDENDS_GROSSED_UP,
    OTHER_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP,
    OTHER_EMPLOYMENT_INCOME,
    OTHER_FHSA_INCOME,
    OTHER_INCOME,
    OTHER_PAYMENTS_DEDUCTION,
    OTHER_PAYMENTS_DEDUCTION_ABOVE_LIMIT,
    OTHER_PAYMENTS_DEDUCTION_AFTER_LIMIT,
    OTHER_PAYMENTS_LIMIT_INCOME,
    OTHER_PAYMENTS_WORKSHEET_LINE_9_OVER_LIMIT,
    OTHER_PAYMENTS_WORKSHEET_REQUIRED,
    OTHER_PENSIONS_AND_SUPERANNUATION,
    PROVINCIAL_CREDITS,
    RDSP_INCOME,
    RDSP_INCOME_REPAYMENT,
    REFUND_OR_BALANCE_OWING,
    RRSP_AMOUNT_DEDUCTED,
    RRSP_CONTRIBUTIONS,
    RRSP_CONTRIBUTIONS_AVAILABLE,
    RRSP_DEDUCTION,
    RRSP_DEDUCTION_LIMIT,
    RRSP_DEDUCTION_MAXIMUM,
    RRSP_INCOME,
    SECURITY_OPTIONS_DEDUCTIONS,
    SLIP_DIVIDEND_TAX_CREDIT,
    SLIP_TAXABLE_DIVIDENDS,
    SLIP_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
    SOCIAL_ASSISTANCE_PAYMENTS,
    SPOUSE_AMOUNT,
    SPOUSE_AMOUNT_BASIS,
    SPOUSE_AMOUNT_BEFORE_COUNT,
    SPOUSE_CAREGIVER_AMOUNT,
    SPOUSE_CAREGIVER_AMOUNT_BEFORE_COUNT,
    SPOUSE_CAREGIVER_BASE,
    SPOUSE_CAREGIVER_BEFORE_MAXIMUM,
    SPOUSE_CAREGIVER_ELIGIBLE,
    SPOUSE_CAREGIVER_LIMIT,
    SPOUSE_INFIRMITY_SUPPLEMENT,
    SPOUSE_NET_INCOME,
    SPOUSES_CLAIMED,
    T3_DIVIDEND_TAX_CREDIT,
    T3_INVESTMENT_INCOME,
    T3_TAXABLE_DIVIDENDS,
    T3_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
    T4PS_DIVIDEND_TAX_CREDIT,
    T4PS_TAXABLE_DIVIDENDS,
    T4PS_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
    T5_DIVIDEND_TAX_CREDIT,
    T5_INVESTMENT_INCOME,
    T5_TAXABLE_DIVIDENDS,
    T5_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
    T5013_DIVIDEND_TAX_CREDIT,
    T5013_INVESTMENT_INCOME,
    T5013_TAXABLE_DIVIDENDS,
    T5013_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
    TAX_REFUND_INTEREST,
    TAXABLE_CAPITAL_GAINS,
    TAXABLE_DIVIDENDS,
    TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
    TAXABLE_INCOME,
    TAXABLE_SCHOLARSHIPS,
    TAXABLE_SUPPORT_PAYMENTS,
    TOTAL_CREDITS,
    TOTAL_INCOME,
    TOTAL_PAYABLE,
    UCCB_AND_RDSP_INCOME,
    UCCB_AND_RDSP_INCOME_REPAYMENTS,
    UCCB_REPAYMENT,
    UNION_DUES,
    UNIVERSAL_CHILD_CARE_BENEFIT,
    UNUSED_RRSP_CONTRIBUTIONS,
    UNUSED_RRSP_CONTRIBUTIONS_CARRIED_FORWARD,
    WORKERS_COMPENSATION_BENEFITS,
    WORKING_INCOME,
)
from app.registrations import JURISDICTIONS

REGISTERED = frozenset(
    {
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
)
# T1 line 167 (line 48400 or 48500): the balance, negative for a refund; and the Federal
# Worksheet's "Line 25000 - Other payments deduction" line 5 "Line 1 minus line 4 =" and line 9
# "Line 5 plus line 8 =", which print no "(if negative, enter "0")" and so may be below zero: the
# `ca/` kinds that may be below zero.
SIGNED = frozenset(
    {
        "ca/refund_or_balance_owing",
        "ca/net_income_less_uccb_and_rdsp_income",
        "ca/other_payments_limit_income",
    }
)
# T1 line 30400 (Schedule 5, "Each household is allowed only one claim for this amount") and line
# 30499 ("Number of children you are claiming this amount for"): the numbers of eligible
# dependants and of infirm children; and Form T778 Part B lines 1 to 3 ("Number of eligible
# children born in 2019 or later whom the disability amount cannot be claimed for", "... born in
# 2025 or earlier whom the disability amount can be claimed for", "... born in 2009 to 2018"):
# the numbers of eligible children for the child care expenses deduction; and Schedule 6 line 38100
# ("Do you have an eligible dependant? 1 Yes or 2 No"), whose eligible dependant is "your or your
# spouse's or common-law partner's child", "under 19 years of age" and "not eligible for the CWB for
# 2025": the number of eligible dependants for the Canada workers benefit; T1 line 30100 ("if
# you were born in 1960 or earlier"), Schedule 5 line 30300 (the spouse amount claimed) and line
# 51090 (eligible for the Canada caregiver amount for the spouse), each a 0 or 1 count as the forms
# take it; and the Federal Worksheet's "Line 25000 - Other payments deduction": 1 if an amount was
# entered on line 14600 ("enter the amount from line 14700 if you did not enter an amount on line
# 14600; otherwise, use Federal Worksheet") and 1 if "the amount on line 9 is more than $93,454",
# each 0 or 1 until a comparison capability derives them; counted, not money.
COUNTS = frozenset(
    {
        "ca/eligible_dependants",
        "ca/infirm_children",
        "ca/born_in_1960_or_earlier",
        "ca/spouses_claimed",
        "ca/spouse_caregiver_eligible",
        "ca/children_under_seven",
        "ca/children_with_disability",
        "ca/children_seven_to_sixteen",
        "ca/cwb_eligible_dependants",
        "ca/other_payments_worksheet_required",
        "ca/other_payments_worksheet_line_9_over_limit",
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
    assert registry.get("ca/other_employment_income") is OTHER_EMPLOYMENT_INCOME
    assert registry.get("ca/old_age_security") is OLD_AGE_SECURITY
    assert registry.get("ca/cpp_or_qpp_benefits") is CPP_OR_QPP_BENEFITS
    assert registry.get("ca/other_pensions_and_superannuation") is OTHER_PENSIONS_AND_SUPERANNUATION
    assert registry.get("ca/elected_split_pension_amount") is ELECTED_SPLIT_PENSION_AMOUNT
    assert registry.get("ca/universal_child_care_benefit") is UNIVERSAL_CHILD_CARE_BENEFIT
    assert registry.get("ca/ei_and_other_benefits") is EI_AND_OTHER_BENEFITS
    assert (
        registry.get("ca/t3_taxable_dividends_other_than_eligible")
        is T3_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE
    )
    assert (
        registry.get("ca/t4ps_taxable_dividends_other_than_eligible")
        is T4PS_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE
    )
    assert (
        registry.get("ca/t5_taxable_dividends_other_than_eligible")
        is T5_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE
    )
    assert (
        registry.get("ca/t5013_taxable_dividends_other_than_eligible")
        is T5013_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE
    )
    assert registry.get("ca/t3_taxable_dividends") is T3_TAXABLE_DIVIDENDS
    assert registry.get("ca/t4ps_taxable_dividends") is T4PS_TAXABLE_DIVIDENDS
    assert registry.get("ca/t5_taxable_dividends") is T5_TAXABLE_DIVIDENDS
    assert registry.get("ca/t5013_taxable_dividends") is T5013_TAXABLE_DIVIDENDS
    assert (
        registry.get("ca/eligible_dividends_received_without_a_slip")
        is ELIGIBLE_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP
    )
    assert (
        registry.get("ca/other_dividends_received_without_a_slip")
        is OTHER_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP
    )
    assert registry.get("ca/t3_dividend_tax_credit") is T3_DIVIDEND_TAX_CREDIT
    assert registry.get("ca/t4ps_dividend_tax_credit") is T4PS_DIVIDEND_TAX_CREDIT
    assert registry.get("ca/t5_dividend_tax_credit") is T5_DIVIDEND_TAX_CREDIT
    assert registry.get("ca/t5013_dividend_tax_credit") is T5013_DIVIDEND_TAX_CREDIT
    assert (
        registry.get("ca/slip_taxable_dividends_other_than_eligible")
        is SLIP_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE
    )
    assert registry.get("ca/slip_taxable_dividends") is SLIP_TAXABLE_DIVIDENDS
    assert registry.get("ca/eligible_dividends_grossed_up") is ELIGIBLE_DIVIDENDS_GROSSED_UP
    assert registry.get("ca/other_dividends_grossed_up") is OTHER_DIVIDENDS_GROSSED_UP
    assert (
        registry.get("ca/dividends_without_a_slip_grossed_up")
        is DIVIDENDS_WITHOUT_A_SLIP_GROSSED_UP
    )
    assert (
        registry.get("ca/taxable_dividends_other_than_eligible")
        is TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE
    )
    assert registry.get("ca/taxable_dividends") is TAXABLE_DIVIDENDS
    assert registry.get("ca/slip_dividend_tax_credit") is SLIP_DIVIDEND_TAX_CREDIT
    assert registry.get("ca/dividends_amount_a") is DIVIDENDS_AMOUNT_A
    assert registry.get("ca/dividends_amount_b") is DIVIDENDS_AMOUNT_B
    assert registry.get("ca/other_dividends_credit") is OTHER_DIVIDENDS_CREDIT
    assert registry.get("ca/dividends_amount_a_less_b") is DIVIDENDS_AMOUNT_A_LESS_B
    assert registry.get("ca/eligible_dividends_credit") is ELIGIBLE_DIVIDENDS_CREDIT
    assert registry.get("ca/no_slip_dividend_tax_credit") is NO_SLIP_DIVIDEND_TAX_CREDIT
    assert registry.get("ca/dividend_tax_credit") is DIVIDEND_TAX_CREDIT
    assert registry.get("ca/credits_against_basic_federal_tax") is CREDITS_AGAINST_BASIC_FEDERAL_TAX
    assert registry.get("ca/t3_investment_income") is T3_INVESTMENT_INCOME
    assert registry.get("ca/t5_investment_income") is T5_INVESTMENT_INCOME
    assert registry.get("ca/t5013_investment_income") is T5013_INVESTMENT_INCOME
    assert (
        registry.get("ca/investment_income_credited_not_received")
        is INVESTMENT_INCOME_CREDITED_NOT_RECEIVED
    )
    assert registry.get("ca/tax_refund_interest") is TAX_REFUND_INTEREST
    assert registry.get("ca/foreign_investment_income") is FOREIGN_INVESTMENT_INCOME
    assert registry.get("ca/investment_income_without_a_slip") is INVESTMENT_INCOME_WITHOUT_A_SLIP
    assert registry.get("ca/investment_royalties") is INVESTMENT_ROYALTIES
    assert (
        registry.get("ca/investment_income_before_prior_years")
        is INVESTMENT_INCOME_BEFORE_PRIOR_YEARS
    )
    assert (
        registry.get("ca/investment_income_reported_in_previous_years")
        is INVESTMENT_INCOME_REPORTED_IN_PREVIOUS_YEARS
    )
    assert (
        registry.get("ca/interest_and_other_investment_income")
        is INTEREST_AND_OTHER_INVESTMENT_INCOME
    )
    assert registry.get("ca/net_partnership_income") is NET_PARTNERSHIP_INCOME
    assert registry.get("ca/rdsp_income") is RDSP_INCOME
    assert registry.get("ca/taxable_support_payments") is TAXABLE_SUPPORT_PAYMENTS
    assert registry.get("ca/rrsp_income") is RRSP_INCOME
    assert registry.get("ca/fhsa_income") is FHSA_INCOME
    assert registry.get("ca/other_fhsa_income") is OTHER_FHSA_INCOME
    assert registry.get("ca/other_income") is OTHER_INCOME
    assert registry.get("ca/taxable_scholarships") is TAXABLE_SCHOLARSHIPS
    assert registry.get("ca/workers_compensation_benefits") is WORKERS_COMPENSATION_BENEFITS
    assert registry.get("ca/social_assistance_payments") is SOCIAL_ASSISTANCE_PAYMENTS
    assert registry.get("ca/net_federal_supplements") is NET_FEDERAL_SUPPLEMENTS
    assert registry.get("ca/income_support_benefits") is INCOME_SUPPORT_BENEFITS
    assert (
        registry.get("ca/canadian_armed_forces_and_police_deduction")
        is CANADIAN_ARMED_FORCES_AND_POLICE_DEDUCTION
    )
    assert registry.get("ca/security_options_deductions") is SECURITY_OPTIONS_DEDUCTIONS
    assert registry.get("ca/uccb_repayment") is UCCB_REPAYMENT
    assert registry.get("ca/rdsp_income_repayment") is RDSP_INCOME_REPAYMENT
    assert registry.get("ca/uccb_and_rdsp_income") is UCCB_AND_RDSP_INCOME
    assert (
        registry.get("ca/net_income_less_uccb_and_rdsp_income")
        is NET_INCOME_LESS_UCCB_AND_RDSP_INCOME
    )
    assert registry.get("ca/uccb_and_rdsp_income_repayments") is UCCB_AND_RDSP_INCOME_REPAYMENTS
    assert registry.get("ca/other_payments_limit_income") is OTHER_PAYMENTS_LIMIT_INCOME
    assert registry.get("ca/other_payments_worksheet_required") is OTHER_PAYMENTS_WORKSHEET_REQUIRED
    assert (
        registry.get("ca/other_payments_worksheet_line_9_over_limit")
        is OTHER_PAYMENTS_WORKSHEET_LINE_9_OVER_LIMIT
    )
    assert (
        registry.get("ca/other_payments_deduction_above_limit")
        is OTHER_PAYMENTS_DEDUCTION_ABOVE_LIMIT
    )
    assert (
        registry.get("ca/other_payments_deduction_after_limit")
        is OTHER_PAYMENTS_DEDUCTION_AFTER_LIMIT
    )
    assert registry.get("ca/other_payments_deduction") is OTHER_PAYMENTS_DEDUCTION
    assert (
        registry.get("ca/limited_partnership_losses_of_other_years")
        is LIMITED_PARTNERSHIP_LOSSES_OF_OTHER_YEARS
    )
    assert registry.get("ca/non_capital_losses_of_other_years") is NON_CAPITAL_LOSSES_OF_OTHER_YEARS
    assert registry.get("ca/additional_deductions") is ADDITIONAL_DEDUCTIONS
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
    assert registry.get("ca/born_in_1960_or_earlier") is BORN_IN_1960_OR_EARLIER
    assert registry.get("ca/age_maximum") is AGE_MAXIMUM
    assert registry.get("ca/age_income_threshold") is AGE_INCOME_THRESHOLD
    assert registry.get("ca/age_income_over_threshold") is AGE_INCOME_OVER_THRESHOLD
    assert registry.get("ca/age_reduction") is AGE_REDUCTION
    assert registry.get("ca/age_amount_before_count") is AGE_AMOUNT_BEFORE_COUNT
    assert registry.get("ca/age_amount") is AGE_AMOUNT
    assert registry.get("ca/spouses_claimed") is SPOUSES_CLAIMED
    assert registry.get("ca/spouse_caregiver_eligible") is SPOUSE_CAREGIVER_ELIGIBLE
    assert registry.get("ca/spouse_net_income") is SPOUSE_NET_INCOME
    assert registry.get("ca/spouse_infirmity_supplement") is SPOUSE_INFIRMITY_SUPPLEMENT
    assert registry.get("ca/spouse_amount_basis") is SPOUSE_AMOUNT_BASIS
    assert registry.get("ca/spouse_amount_before_count") is SPOUSE_AMOUNT_BEFORE_COUNT
    assert registry.get("ca/spouse_amount") is SPOUSE_AMOUNT
    assert registry.get("ca/eligible_dependants") is ELIGIBLE_DEPENDANTS
    assert registry.get("ca/dependant_net_income") is DEPENDANT_NET_INCOME
    assert (
        registry.get("ca/eligible_dependant_amount_before_count")
        is ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT
    )
    assert registry.get("ca/eligible_dependant_amount") is ELIGIBLE_DEPENDANT_AMOUNT
    assert registry.get("ca/spouse_caregiver_base") is SPOUSE_CAREGIVER_BASE
    assert registry.get("ca/spouse_caregiver_before_maximum") is SPOUSE_CAREGIVER_BEFORE_MAXIMUM
    assert registry.get("ca/spouse_caregiver_limit") is SPOUSE_CAREGIVER_LIMIT
    assert (
        registry.get("ca/spouse_caregiver_amount_before_count")
        is SPOUSE_CAREGIVER_AMOUNT_BEFORE_COUNT
    )
    assert registry.get("ca/spouse_caregiver_amount") is SPOUSE_CAREGIVER_AMOUNT
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
    assert registry.get("ca/provincial_credits") is PROVINCIAL_CREDITS
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
        OTHER_EMPLOYMENT_INCOME,
        OLD_AGE_SECURITY,
        CPP_OR_QPP_BENEFITS,
        OTHER_PENSIONS_AND_SUPERANNUATION,
        ELECTED_SPLIT_PENSION_AMOUNT,
        UNIVERSAL_CHILD_CARE_BENEFIT,
        EI_AND_OTHER_BENEFITS,
        T3_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
        T4PS_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
        T5_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
        T5013_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
        T3_TAXABLE_DIVIDENDS,
        T4PS_TAXABLE_DIVIDENDS,
        T5_TAXABLE_DIVIDENDS,
        T5013_TAXABLE_DIVIDENDS,
        ELIGIBLE_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP,
        OTHER_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP,
        T3_DIVIDEND_TAX_CREDIT,
        T4PS_DIVIDEND_TAX_CREDIT,
        T5_DIVIDEND_TAX_CREDIT,
        T5013_DIVIDEND_TAX_CREDIT,
        SLIP_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
        SLIP_TAXABLE_DIVIDENDS,
        ELIGIBLE_DIVIDENDS_GROSSED_UP,
        OTHER_DIVIDENDS_GROSSED_UP,
        DIVIDENDS_WITHOUT_A_SLIP_GROSSED_UP,
        TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
        TAXABLE_DIVIDENDS,
        SLIP_DIVIDEND_TAX_CREDIT,
        DIVIDENDS_AMOUNT_A,
        DIVIDENDS_AMOUNT_B,
        OTHER_DIVIDENDS_CREDIT,
        DIVIDENDS_AMOUNT_A_LESS_B,
        ELIGIBLE_DIVIDENDS_CREDIT,
        NO_SLIP_DIVIDEND_TAX_CREDIT,
        DIVIDEND_TAX_CREDIT,
        CREDITS_AGAINST_BASIC_FEDERAL_TAX,
        T3_INVESTMENT_INCOME,
        T5_INVESTMENT_INCOME,
        T5013_INVESTMENT_INCOME,
        INVESTMENT_INCOME_CREDITED_NOT_RECEIVED,
        TAX_REFUND_INTEREST,
        FOREIGN_INVESTMENT_INCOME,
        INVESTMENT_INCOME_WITHOUT_A_SLIP,
        INVESTMENT_ROYALTIES,
        INVESTMENT_INCOME_BEFORE_PRIOR_YEARS,
        INVESTMENT_INCOME_REPORTED_IN_PREVIOUS_YEARS,
        INTEREST_AND_OTHER_INVESTMENT_INCOME,
        NET_PARTNERSHIP_INCOME,
        RDSP_INCOME,
        TAXABLE_SUPPORT_PAYMENTS,
        RRSP_INCOME,
        FHSA_INCOME,
        OTHER_FHSA_INCOME,
        OTHER_INCOME,
        TAXABLE_SCHOLARSHIPS,
        WORKERS_COMPENSATION_BENEFITS,
        SOCIAL_ASSISTANCE_PAYMENTS,
        NET_FEDERAL_SUPPLEMENTS,
        INCOME_SUPPORT_BENEFITS,
        CANADIAN_ARMED_FORCES_AND_POLICE_DEDUCTION,
        SECURITY_OPTIONS_DEDUCTIONS,
        UCCB_REPAYMENT,
        RDSP_INCOME_REPAYMENT,
        UCCB_AND_RDSP_INCOME,
        NET_INCOME_LESS_UCCB_AND_RDSP_INCOME,
        UCCB_AND_RDSP_INCOME_REPAYMENTS,
        OTHER_PAYMENTS_LIMIT_INCOME,
        OTHER_PAYMENTS_DEDUCTION_ABOVE_LIMIT,
        OTHER_PAYMENTS_DEDUCTION_AFTER_LIMIT,
        OTHER_PAYMENTS_DEDUCTION,
        LIMITED_PARTNERSHIP_LOSSES_OF_OTHER_YEARS,
        NON_CAPITAL_LOSSES_OF_OTHER_YEARS,
        ADDITIONAL_DEDUCTIONS,
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
        AGE_MAXIMUM,
        AGE_INCOME_THRESHOLD,
        AGE_INCOME_OVER_THRESHOLD,
        AGE_REDUCTION,
        AGE_AMOUNT_BEFORE_COUNT,
        AGE_AMOUNT,
        SPOUSE_NET_INCOME,
        SPOUSE_INFIRMITY_SUPPLEMENT,
        SPOUSE_AMOUNT_BASIS,
        SPOUSE_AMOUNT_BEFORE_COUNT,
        SPOUSE_AMOUNT,
        DEPENDANT_NET_INCOME,
        ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT,
        ELIGIBLE_DEPENDANT_AMOUNT,
        SPOUSE_CAREGIVER_BASE,
        SPOUSE_CAREGIVER_BEFORE_MAXIMUM,
        SPOUSE_CAREGIVER_LIMIT,
        SPOUSE_CAREGIVER_AMOUNT_BEFORE_COUNT,
        SPOUSE_CAREGIVER_AMOUNT,
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
        PROVINCIAL_CREDITS,
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


def test_the_other_payments_worksheets_lines_5_and_9_are_signed(registry: ArtifactRegistry) -> None:
    # Federal Worksheet "Line 25000 - Other payments deduction": line 5 "Line 1 minus line 4 =" and
    # line 9 "Line 5 plus line 8 =" print no floor, unlike line 1 ("if negative, enter "0"").
    assert NET_INCOME_LESS_UCCB_AND_RDSP_INCOME.non_negative is False
    assert OTHER_PAYMENTS_LIMIT_INCOME.non_negative is False
    assert registry.kind("ca/net_income_less_uccb_and_rdsp_income").non_negative is False
    assert registry.kind("ca/other_payments_limit_income").non_negative is False
    assert UCCB_AND_RDSP_INCOME.non_negative is True
    assert UCCB_AND_RDSP_INCOME_REPAYMENTS.non_negative is True
    assert OTHER_PAYMENTS_DEDUCTION.non_negative is True


def test_the_income_tax_deducted_is_non_negative() -> None:
    # T1 line 150 (line 43700) "Total income tax deducted (amounts from all Canadian slips)".
    assert INCOME_TAX_DEDUCTED.non_negative is True


def test_the_rrsp_amount_deducted_is_non_negative() -> None:
    # Schedule 7 line 18 "Enter your RRSP, PRPP, or SPP contributions you are deducting for 2025
    # (cannot be more than the amount on line 17).": an amount the filer states.
    assert RRSP_AMOUNT_DEDUCTED.non_negative is True


def test_capital_gain_is_non_negative_while_losses_are_not_modelled() -> None:
    assert CAPITAL_GAIN.non_negative is True
