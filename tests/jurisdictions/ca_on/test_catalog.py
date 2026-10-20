"""Snapshot of the `ca-on/` artifact kind identifiers, as the application registers them.

Identifiers are stored with results and exposed by the API, so changing or removing one is a
breaking change: update this snapshot only on purpose. Declaring a kind in this package's catalog
adds it here; federal kinds are snapshotted in `tests/jurisdictions/ca/`. The kinds are
registered explicitly, as the composition root does, into a fresh registry.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Any

import pytest

import app.jurisdictions.ca_on
import app.jurisdictions.ca_on.catalog
from app.domain.artifact import ArtifactCatalog, ArtifactKind, ArtifactRegistry
from app.domain.digits import DigitsKind
from app.domain.errors import InvalidRecordError, NegativeArtifactError
from app.domain.record_list import RecordList, RecordListKind
from app.jurisdictions.ca.catalog import (
    DEPENDANT_CARE_EXPENSES,
    DEPENDANT_NET_INCOME,
    DEPENDANT_TAXABLE_INCOME,
    DEPENDANT_UNDER_18,
    INFIRM_DEPENDANTS,
)
from app.jurisdictions.ca.catalog import (
    DISABILITY_DEPENDANTS as FEDERAL_DISABILITY_DEPENDANTS,
)
from app.jurisdictions.ca_on.catalog import (
    AGE_AMOUNT,
    AGE_AMOUNT_BEFORE_COUNT,
    AGE_INCOME_OVER_THRESHOLD,
    AGE_INCOME_THRESHOLD,
    AGE_MAXIMUM,
    AGE_REDUCTION,
    APPLIES_FOR_ENERGY_AND_PROPERTY_TAX_CREDIT,
    APPLIES_FOR_NORTHERN_ENERGY_CREDIT,
    APPLIES_FOR_SENIOR_HOMEOWNERS_GRANT,
    BANKRUPT_IN_YEAR,
    BASIC_PERSONAL_AMOUNT,
    CAREGIVER_AMOUNT,
    CAREGIVER_DEPENDANTS,
    CATALOG,
    CHOOSES_SINGLE_BENEFIT_PAYMENT,
    CLAIMED_AS_ELIGIBLE_DEPENDANT,
    CLAIMS_SENIORS_CARE_CREDIT,
    CLAIMS_TAX_REDUCTION_AMOUNTS_AT_EQUAL_NET_INCOME,
    COMMUNITY_FOOD_PROGRAM_CREDIT,
    COMMUNITY_FOOD_PROGRAM_DONATIONS,
    COOP_CLAIMED_AS_PARTNERSHIP_MEMBER,
    COOP_EDUCATION_CREDIT,
    COOP_EDUCATION_FULL_SHARE,
    COOP_EDUCATION_PAYROLL,
    COOP_EDUCATION_PAYROLL_OVER_THRESHOLD,
    COOP_EDUCATION_PAYROLL_RANGE,
    COOP_EDUCATION_PAYROLL_THRESHOLD,
    COOP_EDUCATION_PHASE_OUT_SHARE,
    COOP_EDUCATION_PLACEMENT_COUNT,
    COOP_EDUCATION_PLACEMENT_EXPENDITURES,
    COOP_EDUCATION_PLACEMENTS,
    COOP_EDUCATION_REMAINING_SHARE,
    COOP_PARTNERSHIP_BUSINESS_NUMBER,
    CREDIT_AMOUNTS_AT_CREDIT_RATE,
    DEPENDANT_ON428_LINE_28,
    DEPENDANTS,
    DEPENDENT_CHILDREN,
    DISABILITY_DEPENDANTS,
    DISABILITY_TRANSFERRED_AMOUNT,
    DIVIDEND_CREDIT_FROM_LINE_57,
    DIVIDEND_TAX_CREDIT,
    DIVIDENDS_AMOUNT_A,
    DIVIDENDS_AMOUNT_A_LESS_B,
    DIVIDENDS_AMOUNT_B,
    DONATIONS_AND_GIFTS_CREDIT,
    DONATIONS_FIRST_TIER_CREDIT,
    DONATIONS_OVER_FIRST_TIER_CREDIT,
    ELIGIBLE_DEPENDANT_AMOUNT,
    ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT,
    ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_MAXIMUM,
    ELIGIBLE_DEPENDANT_BASE,
    ELIGIBLE_DIVIDENDS_CREDIT,
    FERTILITY_CREDIT,
    FERTILITY_CREDIT_BEFORE_MAXIMUM,
    FERTILITY_EXPENSES,
    FLOW_THROUGH_SHARE_CREDIT,
    FLOW_THROUGH_SHARE_EXPENSES,
    FLOW_THROUGH_SHARE_SLIP_EXPENSES,
    FLOW_THROUGH_SHARE_SLIPS,
    LIFT_ADJUSTED_NET_INCOME,
    LIFT_CREDIT,
    LIFT_CREDIT_BEFORE_MAXIMUM,
    LIFT_CREDIT_SINGLE,
    LIFT_CREDIT_WITH_SPOUSE,
    LIFT_EXCESS_OVER_FAMILY_THRESHOLD,
    LIFT_EXCESS_OVER_INDIVIDUAL_THRESHOLD,
    LIFT_FAMILY_INCOME_THRESHOLD,
    LIFT_FAMILY_NET_INCOME,
    LIFT_FAMILY_REDUCTION,
    LIFT_GREATER_EXCESS,
    LIFT_INDIVIDUAL_INCOME_THRESHOLD,
    LIFT_MAXIMUM_CREDIT,
    LIFT_NET_INCOME_AND_REPAYMENTS,
    LIFT_REDUCTION,
    LIFT_SPOUSE_ADJUSTED_NET_INCOME,
    LIFT_SPOUSE_AT_YEAR_END,
    LIFT_SPOUSE_NET_INCOME_AND_REPAYMENTS,
    LIFT_SPOUSE_UCCB_AND_RDSP_INCOME,
    LIFT_UCCB_AND_RDSP_INCOME,
    LIVED_IN_STUDENT_RESIDENCE,
    MEDICAL_CLAIM,
    MEDICAL_EXPENSES_OVER_THRESHOLD,
    MEDICAL_NET_INCOME_SHARE,
    MEDICAL_THRESHOLD,
    NET_REFUND,
    NON_REFUNDABLE_CREDIT_AMOUNTS,
    NON_REFUNDABLE_TAX_CREDITS,
    NOT_CLAIMING_ONTARIO_TAX_REDUCTION,
    NOT_RESIDENT_OF_CANADA_AT_START_OF_YEAR,
    NOT_RESIDENT_OF_ONTARIO_AT_YEAR_END,
    ONTARIO_BASIC_TAX,
    ONTARIO_CREDITS,
    ONTARIO_CREDITS_SUBTOTAL,
    ONTARIO_HEALTH_PREMIUM,
    ONTARIO_MINIMUM_TAX,
    ONTARIO_SURTAX,
    ONTARIO_TAX,
    ONTARIO_TAX_AFTER_CREDITS,
    ONTARIO_TAX_AFTER_DIVIDEND_CREDIT,
    ONTARIO_TAX_AFTER_FOOD_CREDIT,
    ONTARIO_TAX_AFTER_LIFT_CREDIT,
    ONTARIO_TAX_AFTER_REDUCTION,
    ONTARIO_TAX_BEFORE_DIVIDEND_CREDIT,
    ONTARIO_TAX_BEFORE_REDUCTION,
    ONTARIO_TAX_LESS_DIVIDEND_CREDIT,
    ONTARIO_TAX_REDUCTION,
    ONTARIO_TAX_REDUCTION_BEFORE_CONDITIONS,
    ONTARIO_TAX_WITH_SURTAX,
    OPPORTUNITIES_FUND_DONATION,
    OTHER_DEPENDANTS_MEDICAL,
    OTHER_DIVIDENDS_CREDIT,
    POLITICAL_CONTRIBUTIONS,
    POLITICAL_CREDIT,
    POLITICAL_CREDIT_BEFORE_MAXIMUM,
    POLITICAL_CREDIT_COLUMN_1_LINE_2,
    POLITICAL_CREDIT_COLUMN_1_LINE_3,
    POLITICAL_CREDIT_COLUMN_1_LINE_5,
    POLITICAL_CREDIT_COLUMN_1_LINE_6,
    POLITICAL_CREDIT_COLUMN_1_LINE_7,
    POLITICAL_CREDIT_COLUMN_2_LINE_2,
    POLITICAL_CREDIT_COLUMN_2_LINE_3,
    POLITICAL_CREDIT_COLUMN_2_LINE_5,
    POLITICAL_CREDIT_COLUMN_2_LINE_6,
    POLITICAL_CREDIT_COLUMN_2_LINE_7,
    POLITICAL_CREDIT_COLUMN_3_LINE_2,
    POLITICAL_CREDIT_COLUMN_3_LINE_3,
    POLITICAL_CREDIT_COLUMN_3_LINE_5,
    POLITICAL_CREDIT_COLUMN_3_LINE_6,
    POLITICAL_CREDIT_COLUMN_3_LINE_7,
    PROPERTY_TAX_PAID,
    PUBLIC_LONG_TERM_CARE_PAID,
    REFUND_BEFORE_DONATION,
    RENT_PAID,
    RESERVE_HOME_ENERGY_COSTS,
    RETURN_FILED_BY_TRUSTEE_IN_BANKRUPTCY,
    SENIORS_CARE_AMOUNT,
    SENIORS_CARE_BASE_AMOUNT,
    SENIORS_CARE_BEFORE_CLAIM,
    SENIORS_CARE_BEFORE_MAXIMUM,
    SENIORS_CARE_CREDIT,
    SENIORS_CARE_FAMILY_NET_INCOME,
    SENIORS_CARE_INCOME_OVER_BASE,
    SENIORS_CARE_REDUCTION,
    SENIORS_TRANSIT_AMOUNT_PAID_AT_MOST_MAXIMUM,
    SENIORS_TRANSIT_CREDIT,
    SENIORS_TRANSIT_PAID,
    SEPARATE_RESIDENCES_FOR_MEDICAL_REASONS,
    SPOUSE_AMOUNT,
    SPOUSE_AMOUNT_BEFORE_COUNT,
    SPOUSE_AMOUNT_BEFORE_MAXIMUM,
    SPOUSE_BASE,
    TAX_REDUCTION_AMOUNTS,
    TAX_REDUCTION_AMOUNTS_CLAIMABLE,
    TAX_REDUCTION_BASIC,
    TAX_REDUCTION_CLAIMABLE,
    TAX_REDUCTION_FOR_CHILDREN,
    TAX_REDUCTION_FOR_CHILDREN_BEFORE_SPOUSE_RULE,
    TAX_REDUCTION_FOR_DEPENDANTS,
    TAX_REDUCTION_FOR_DEPENDANTS_BEFORE_SPOUSE_RULE,
)
from app.registrations import JURISDICTIONS

REGISTERED = frozenset(
    {
        "ca-on/ontario_basic_tax",
        "ca-on/basic_personal_amount",
        "ca-on/age_maximum",
        "ca-on/age_income_threshold",
        "ca-on/age_income_over_threshold",
        "ca-on/age_reduction",
        "ca-on/age_amount_before_count",
        "ca-on/age_amount",
        "ca-on/spouse_base",
        "ca-on/spouse_amount_before_maximum",
        "ca-on/spouse_amount_before_count",
        "ca-on/spouse_amount",
        "ca-on/eligible_dependant_base",
        "ca-on/eligible_dependant_amount_before_maximum",
        "ca-on/eligible_dependant_amount_before_count",
        "ca-on/eligible_dependant_amount",
        "ca-on/medical_net_income_share",
        "ca-on/medical_threshold",
        "ca-on/medical_expenses_over_threshold",
        "ca-on/other_dependants_medical",
        "ca-on/medical_claim",
        "ca-on/claimed_as_eligible_dependant",
        "ca-on/caregiver_dependants",
        "ca-on/caregiver_amount",
        "ca-on/dependant_on428_line_28",
        "ca-on/disability_dependants",
        "ca-on/disability_transferred_amount",
        "ca-on/non_refundable_credit_amounts",
        "ca-on/credit_amounts_at_credit_rate",
        "ca-on/donations_first_tier_credit",
        "ca-on/donations_over_first_tier_credit",
        "ca-on/donations_and_gifts_credit",
        "ca-on/non_refundable_tax_credits",
        "ca-on/ontario_tax_after_credits",
        "ca-on/ontario_surtax",
        "ca-on/ontario_tax_with_surtax",
        "ca-on/dividends_amount_a",
        "ca-on/dividends_amount_b",
        "ca-on/other_dividends_credit",
        "ca-on/dividends_amount_a_less_b",
        "ca-on/eligible_dividends_credit",
        "ca-on/dividend_tax_credit",
        "ca-on/ontario_tax_before_dividend_credit",
        "ca-on/ontario_tax_less_dividend_credit",
        "ca-on/dividend_credit_from_line_57",
        "ca-on/ontario_tax_after_dividend_credit",
        "ca-on/tax_reduction_basic",
        "ca-on/dependent_children",
        "ca-on/tax_reduction_for_children",
        "ca-on/dependants",
        "ca-on/tax_reduction_for_dependants",
        "ca-on/tax_reduction_amounts",
        "ca-on/ontario_tax_reduction",
        "ca-on/ontario_minimum_tax",
        "ca-on/ontario_tax_before_reduction",
        "ca-on/not_resident_of_canada_at_start_of_year",
        "ca-on/not_resident_of_ontario_at_year_end",
        "ca-on/bankrupt_in_year",
        "ca-on/return_filed_by_trustee_in_bankruptcy",
        "ca-on/not_claiming_ontario_tax_reduction",
        "ca-on/tax_reduction_claimable",
        "ca-on/claims_tax_reduction_amounts_at_equal_net_income",
        "ca-on/tax_reduction_amounts_claimable",
        "ca-on/tax_reduction_for_children_before_spouse_rule",
        "ca-on/tax_reduction_for_dependants_before_spouse_rule",
        "ca-on/ontario_tax_reduction_before_conditions",
        "ca-on/ontario_tax_after_reduction",
        "ca-on/lift_credit_before_maximum",
        "ca-on/lift_maximum_credit",
        "ca-on/lift_reduction",
        "ca-on/lift_spouse_at_year_end",
        "ca-on/lift_net_income_and_repayments",
        "ca-on/lift_uccb_and_rdsp_income",
        "ca-on/lift_adjusted_net_income",
        "ca-on/lift_credit_single",
        "ca-on/lift_spouse_net_income_and_repayments",
        "ca-on/lift_spouse_uccb_and_rdsp_income",
        "ca-on/lift_spouse_adjusted_net_income",
        "ca-on/lift_individual_income_threshold",
        "ca-on/lift_excess_over_individual_threshold",
        "ca-on/lift_family_net_income",
        "ca-on/lift_family_income_threshold",
        "ca-on/lift_excess_over_family_threshold",
        "ca-on/lift_greater_excess",
        "ca-on/lift_family_reduction",
        "ca-on/lift_credit_with_spouse",
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
        "ca-on/claims_seniors_care_credit",
        "ca-on/seniors_care_before_maximum",
        "ca-on/seniors_care_amount",
        "ca-on/seniors_care_family_net_income",
        "ca-on/seniors_care_base_amount",
        "ca-on/seniors_care_income_over_base",
        "ca-on/seniors_care_reduction",
        "ca-on/seniors_care_before_claim",
        "ca-on/seniors_care_credit",
        "ca-on/seniors_transit_paid",
        "ca-on/seniors_transit_amount_paid_at_most_maximum",
        "ca-on/seniors_transit_credit",
        "ca-on/political_contributions",
        "ca-on/political_credit_column_1_line_2",
        "ca-on/political_credit_column_1_line_3",
        "ca-on/political_credit_column_1_line_5",
        "ca-on/political_credit_column_1_line_6",
        "ca-on/political_credit_column_1_line_7",
        "ca-on/political_credit_column_2_line_2",
        "ca-on/political_credit_column_2_line_3",
        "ca-on/political_credit_column_2_line_5",
        "ca-on/political_credit_column_2_line_6",
        "ca-on/political_credit_column_2_line_7",
        "ca-on/political_credit_column_3_line_2",
        "ca-on/political_credit_column_3_line_3",
        "ca-on/political_credit_column_3_line_5",
        "ca-on/political_credit_column_3_line_6",
        "ca-on/political_credit_column_3_line_7",
        "ca-on/political_credit_before_maximum",
        "ca-on/political_credit",
        "ca-on/flow_through_share_slip_expenses",
        "ca-on/flow_through_share_slips",
        "ca-on/flow_through_share_expenses",
        "ca-on/flow_through_share_credit",
        "ca-on/coop_education_payroll",
        "ca-on/coop_education_payroll_threshold",
        "ca-on/coop_education_payroll_over_threshold",
        "ca-on/coop_education_payroll_range",
        "ca-on/coop_education_phase_out_share",
        "ca-on/coop_education_full_share",
        "ca-on/coop_education_remaining_share",
        "ca-on/coop_education_placement_expenditures",
        "ca-on/coop_education_placements",
        "ca-on/coop_education_placement_count",
        "ca-on/coop_education_credit",
        "ca-on/ontario_credits_subtotal",
        "ca-on/ontario_credits",
        "ca-on/refund_before_donation",
        "ca-on/opportunities_fund_donation",
        "ca-on/net_refund",
        "ca-on/applies_for_energy_and_property_tax_credit",
        "ca-on/applies_for_northern_energy_credit",
        "ca-on/chooses_single_benefit_payment",
        "ca-on/applies_for_senior_homeowners_grant",
        "ca-on/separate_residences_for_medical_reasons",
        "ca-on/lived_in_student_residence",
        "ca-on/rent_paid",
        "ca-on/property_tax_paid",
        "ca-on/reserve_home_energy_costs",
        "ca-on/public_long_term_care_paid",
        "ca-on/coop_claimed_as_partnership_member",
        "ca-on/coop_partnership_business_number",
    }
)
# ON428 lines 75 (line 60969) and 76 (line 60970): the numbers of dependent children and of
# dependants, counted, not money; Worksheet ON428's "Line 58185 - Ontario caregiver amount"
# line 4, whether a dependant is the one claimed on line 58160 (0 or 1), a field of each record;
# ON479 line 63260, the number of eligible work placements; and Schedule ON428-A's choice of
# Part A or Part B, whether there was a spouse or common-law partner at the end of the year
# (0 or 1).
# line 4, whether a dependant is the one claimed on line 58160 (0 or 1), a field of each record; and
# ON479 line 63260, the number of eligible work placements; Form ON-BEN's six tick boxes
# (lines 61020, 61040, 61060, 61070, 61080 and 61140), each 0 or 1; and ON479 line 63265, the
# answer on a partnership claim, 0 or 1.
COUNTS = frozenset(
    {
        "ca-on/dependent_children",
        "ca-on/dependants",
        "ca-on/claimed_as_eligible_dependant",
        "ca-on/coop_education_placement_count",
        "ca-on/claims_seniors_care_credit",
        "ca-on/lift_spouse_at_year_end",
        "ca-on/not_resident_of_canada_at_start_of_year",
        "ca-on/not_resident_of_ontario_at_year_end",
        "ca-on/bankrupt_in_year",
        "ca-on/return_filed_by_trustee_in_bankruptcy",
        "ca-on/not_claiming_ontario_tax_reduction",
        "ca-on/tax_reduction_claimable",
        "ca-on/claims_tax_reduction_amounts_at_equal_net_income",
        "ca-on/tax_reduction_amounts_claimable",
        "ca-on/applies_for_energy_and_property_tax_credit",
        "ca-on/applies_for_northern_energy_credit",
        "ca-on/chooses_single_benefit_payment",
        "ca-on/applies_for_senior_homeowners_grant",
        "ca-on/separate_residences_for_medical_reasons",
        "ca-on/lived_in_student_residence",
        "ca-on/coop_claimed_as_partnership_member",
    }
)
# ON479 line 63270, the business number, "(enter 9 digits)": a digits kind of nine digits.
DIGITS = frozenset({"ca-on/coop_partnership_business_number"})
# Form T1221 lines 1 to 3, one line per corporation or slip: the record list of the slips;
# Worksheet ON428's "Line 58185 - Ontario caregiver amount", "Complete one column for each
# dependant": the record list of its dependants; and Worksheet ON428's "Line 58480 - Disability
# amount transferred from a dependant", "Complete this calculation for each dependant": the
# record list of its dependants; and Worksheet ON479's chart for each qualifying work placement:
# the record list of the placements.
RECORD_LISTS = frozenset(
    {
        "ca-on/flow_through_share_slips",
        "ca-on/caregiver_dependants",
        "ca-on/coop_education_placements",
        "ca-on/disability_dependants",
    }
)
# Schedule ON428-A lines 9, 21 and 24 print no "(if negative, enter "0")", and line 6 and line 21
# take the net income "or the amount you would have entered if the instructions on line 23600
# said "if negative, show in brackets"": signed kinds.
SIGNED = frozenset(
    {
        "ca-on/lift_net_income_and_repayments",
        "ca-on/lift_spouse_net_income_and_repayments",
    }
)


@pytest.fixture
def registry() -> ArtifactRegistry:
    registry = ArtifactRegistry()
    JURISDICTIONS.register(registry)
    return registry


def test_registered_identifiers_snapshot(registry: ArtifactRegistry) -> None:
    identifiers = registry.identifiers()

    assert {i for i in identifiers if i.startswith("ca-on/")} == REGISTERED


def test_the_package_exposes_its_catalog() -> None:
    assert isinstance(app.jurisdictions.ca_on.catalog.CATALOG, ArtifactCatalog)
    assert app.jurisdictions.ca_on.catalog.CATALOG is CATALOG
    assert {kind.identifier for kind in CATALOG.kinds} == REGISTERED


def test_catalog_kinds_are_the_registered_ones(registry: ArtifactRegistry) -> None:
    assert registry.get("ca-on/ontario_basic_tax") is ONTARIO_BASIC_TAX
    assert registry.get("ca-on/ontario_tax_after_credits") is ONTARIO_TAX_AFTER_CREDITS
    assert registry.get("ca-on/basic_personal_amount") is BASIC_PERSONAL_AMOUNT
    assert registry.get("ca-on/age_maximum") is AGE_MAXIMUM
    assert registry.get("ca-on/age_income_threshold") is AGE_INCOME_THRESHOLD
    assert registry.get("ca-on/age_income_over_threshold") is AGE_INCOME_OVER_THRESHOLD
    assert registry.get("ca-on/age_reduction") is AGE_REDUCTION
    assert registry.get("ca-on/age_amount_before_count") is AGE_AMOUNT_BEFORE_COUNT
    assert registry.get("ca-on/age_amount") is AGE_AMOUNT
    assert registry.get("ca-on/spouse_base") is SPOUSE_BASE
    assert registry.get("ca-on/spouse_amount_before_maximum") is SPOUSE_AMOUNT_BEFORE_MAXIMUM
    assert registry.get("ca-on/spouse_amount_before_count") is SPOUSE_AMOUNT_BEFORE_COUNT
    assert registry.get("ca-on/spouse_amount") is SPOUSE_AMOUNT
    assert registry.get("ca-on/eligible_dependant_base") is ELIGIBLE_DEPENDANT_BASE
    assert (
        registry.get("ca-on/eligible_dependant_amount_before_maximum")
        is ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_MAXIMUM
    )
    assert (
        registry.get("ca-on/eligible_dependant_amount_before_count")
        is ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT
    )
    assert registry.get("ca-on/eligible_dependant_amount") is ELIGIBLE_DEPENDANT_AMOUNT
    assert registry.get("ca-on/medical_net_income_share") is MEDICAL_NET_INCOME_SHARE
    assert registry.get("ca-on/medical_threshold") is MEDICAL_THRESHOLD
    assert registry.get("ca-on/medical_expenses_over_threshold") is MEDICAL_EXPENSES_OVER_THRESHOLD
    assert registry.get("ca-on/other_dependants_medical") is OTHER_DEPENDANTS_MEDICAL
    assert registry.get("ca-on/medical_claim") is MEDICAL_CLAIM
    assert registry.get("ca-on/claimed_as_eligible_dependant") is CLAIMED_AS_ELIGIBLE_DEPENDANT
    assert registry.get("ca-on/caregiver_dependants") is CAREGIVER_DEPENDANTS
    assert registry.get("ca-on/caregiver_amount") is CAREGIVER_AMOUNT
    assert registry.get("ca-on/dependant_on428_line_28") is DEPENDANT_ON428_LINE_28
    assert registry.get("ca-on/disability_dependants") is DISABILITY_DEPENDANTS
    assert registry.get("ca-on/disability_transferred_amount") is DISABILITY_TRANSFERRED_AMOUNT
    assert registry.get("ca-on/non_refundable_credit_amounts") is NON_REFUNDABLE_CREDIT_AMOUNTS
    assert registry.get("ca-on/credit_amounts_at_credit_rate") is CREDIT_AMOUNTS_AT_CREDIT_RATE
    assert registry.get("ca-on/donations_first_tier_credit") is DONATIONS_FIRST_TIER_CREDIT
    assert (
        registry.get("ca-on/donations_over_first_tier_credit") is DONATIONS_OVER_FIRST_TIER_CREDIT
    )
    assert registry.get("ca-on/donations_and_gifts_credit") is DONATIONS_AND_GIFTS_CREDIT
    assert registry.get("ca-on/non_refundable_tax_credits") is NON_REFUNDABLE_TAX_CREDITS
    assert registry.get("ca-on/ontario_surtax") is ONTARIO_SURTAX
    assert registry.get("ca-on/ontario_tax_with_surtax") is ONTARIO_TAX_WITH_SURTAX
    assert registry.get("ca-on/dividends_amount_a") is DIVIDENDS_AMOUNT_A
    assert registry.get("ca-on/dividends_amount_b") is DIVIDENDS_AMOUNT_B
    assert registry.get("ca-on/other_dividends_credit") is OTHER_DIVIDENDS_CREDIT
    assert registry.get("ca-on/dividends_amount_a_less_b") is DIVIDENDS_AMOUNT_A_LESS_B
    assert registry.get("ca-on/eligible_dividends_credit") is ELIGIBLE_DIVIDENDS_CREDIT
    assert registry.get("ca-on/dividend_tax_credit") is DIVIDEND_TAX_CREDIT
    assert (
        registry.get("ca-on/ontario_tax_before_dividend_credit")
        is ONTARIO_TAX_BEFORE_DIVIDEND_CREDIT
    )
    assert (
        registry.get("ca-on/ontario_tax_less_dividend_credit") is ONTARIO_TAX_LESS_DIVIDEND_CREDIT
    )
    assert registry.get("ca-on/dividend_credit_from_line_57") is DIVIDEND_CREDIT_FROM_LINE_57
    assert (
        registry.get("ca-on/ontario_tax_after_dividend_credit") is ONTARIO_TAX_AFTER_DIVIDEND_CREDIT
    )
    assert registry.get("ca-on/tax_reduction_basic") is TAX_REDUCTION_BASIC
    assert registry.get("ca-on/dependent_children") is DEPENDENT_CHILDREN
    assert registry.get("ca-on/tax_reduction_for_children") is TAX_REDUCTION_FOR_CHILDREN
    assert registry.get("ca-on/dependants") is DEPENDANTS
    assert registry.get("ca-on/tax_reduction_for_dependants") is TAX_REDUCTION_FOR_DEPENDANTS
    assert registry.get("ca-on/tax_reduction_amounts") is TAX_REDUCTION_AMOUNTS
    assert registry.get("ca-on/ontario_tax_reduction") is ONTARIO_TAX_REDUCTION
    assert registry.get("ca-on/ontario_minimum_tax") is ONTARIO_MINIMUM_TAX
    assert registry.get("ca-on/ontario_tax_before_reduction") is ONTARIO_TAX_BEFORE_REDUCTION
    assert (
        registry.get("ca-on/not_resident_of_canada_at_start_of_year")
        is NOT_RESIDENT_OF_CANADA_AT_START_OF_YEAR
    )
    assert (
        registry.get("ca-on/not_resident_of_ontario_at_year_end")
        is NOT_RESIDENT_OF_ONTARIO_AT_YEAR_END
    )
    assert registry.get("ca-on/bankrupt_in_year") is BANKRUPT_IN_YEAR
    assert (
        registry.get("ca-on/return_filed_by_trustee_in_bankruptcy")
        is RETURN_FILED_BY_TRUSTEE_IN_BANKRUPTCY
    )
    assert (
        registry.get("ca-on/not_claiming_ontario_tax_reduction")
        is NOT_CLAIMING_ONTARIO_TAX_REDUCTION
    )
    assert registry.get("ca-on/tax_reduction_claimable") is TAX_REDUCTION_CLAIMABLE
    assert (
        registry.get("ca-on/claims_tax_reduction_amounts_at_equal_net_income")
        is CLAIMS_TAX_REDUCTION_AMOUNTS_AT_EQUAL_NET_INCOME
    )
    assert registry.get("ca-on/tax_reduction_amounts_claimable") is TAX_REDUCTION_AMOUNTS_CLAIMABLE
    assert (
        registry.get("ca-on/tax_reduction_for_children_before_spouse_rule")
        is TAX_REDUCTION_FOR_CHILDREN_BEFORE_SPOUSE_RULE
    )
    assert (
        registry.get("ca-on/tax_reduction_for_dependants_before_spouse_rule")
        is TAX_REDUCTION_FOR_DEPENDANTS_BEFORE_SPOUSE_RULE
    )
    assert (
        registry.get("ca-on/ontario_tax_reduction_before_conditions")
        is ONTARIO_TAX_REDUCTION_BEFORE_CONDITIONS
    )
    assert registry.get("ca-on/ontario_tax_after_reduction") is ONTARIO_TAX_AFTER_REDUCTION
    assert registry.get("ca-on/lift_credit_before_maximum") is LIFT_CREDIT_BEFORE_MAXIMUM
    assert registry.get("ca-on/lift_maximum_credit") is LIFT_MAXIMUM_CREDIT
    assert registry.get("ca-on/lift_reduction") is LIFT_REDUCTION
    assert registry.get("ca-on/lift_spouse_at_year_end") is LIFT_SPOUSE_AT_YEAR_END
    assert registry.get("ca-on/lift_net_income_and_repayments") is LIFT_NET_INCOME_AND_REPAYMENTS
    assert registry.get("ca-on/lift_uccb_and_rdsp_income") is LIFT_UCCB_AND_RDSP_INCOME
    assert registry.get("ca-on/lift_adjusted_net_income") is LIFT_ADJUSTED_NET_INCOME
    assert registry.get("ca-on/lift_credit_single") is LIFT_CREDIT_SINGLE
    assert (
        registry.get("ca-on/lift_spouse_net_income_and_repayments")
        is LIFT_SPOUSE_NET_INCOME_AND_REPAYMENTS
    )
    assert (
        registry.get("ca-on/lift_spouse_uccb_and_rdsp_income") is LIFT_SPOUSE_UCCB_AND_RDSP_INCOME
    )
    assert registry.get("ca-on/lift_spouse_adjusted_net_income") is LIFT_SPOUSE_ADJUSTED_NET_INCOME
    assert (
        registry.get("ca-on/lift_individual_income_threshold") is LIFT_INDIVIDUAL_INCOME_THRESHOLD
    )
    assert (
        registry.get("ca-on/lift_excess_over_individual_threshold")
        is LIFT_EXCESS_OVER_INDIVIDUAL_THRESHOLD
    )
    assert registry.get("ca-on/lift_family_net_income") is LIFT_FAMILY_NET_INCOME
    assert registry.get("ca-on/lift_family_income_threshold") is LIFT_FAMILY_INCOME_THRESHOLD
    assert (
        registry.get("ca-on/lift_excess_over_family_threshold") is LIFT_EXCESS_OVER_FAMILY_THRESHOLD
    )
    assert registry.get("ca-on/lift_greater_excess") is LIFT_GREATER_EXCESS
    assert registry.get("ca-on/lift_family_reduction") is LIFT_FAMILY_REDUCTION
    assert registry.get("ca-on/lift_credit_with_spouse") is LIFT_CREDIT_WITH_SPOUSE
    assert registry.get("ca-on/lift_credit") is LIFT_CREDIT
    assert registry.get("ca-on/ontario_tax_after_lift_credit") is ONTARIO_TAX_AFTER_LIFT_CREDIT
    assert (
        registry.get("ca-on/community_food_program_donations") is COMMUNITY_FOOD_PROGRAM_DONATIONS
    )
    assert registry.get("ca-on/community_food_program_credit") is COMMUNITY_FOOD_PROGRAM_CREDIT
    assert registry.get("ca-on/ontario_tax_after_food_credit") is ONTARIO_TAX_AFTER_FOOD_CREDIT
    assert registry.get("ca-on/ontario_health_premium") is ONTARIO_HEALTH_PREMIUM
    assert registry.get("ca-on/ontario_tax") is ONTARIO_TAX
    assert registry.get("ca-on/fertility_expenses") is FERTILITY_EXPENSES
    assert registry.get("ca-on/fertility_credit_before_maximum") is FERTILITY_CREDIT_BEFORE_MAXIMUM
    assert registry.get("ca-on/fertility_credit") is FERTILITY_CREDIT
    assert registry.get("ca-on/claims_seniors_care_credit") is CLAIMS_SENIORS_CARE_CREDIT
    assert registry.get("ca-on/seniors_care_before_maximum") is SENIORS_CARE_BEFORE_MAXIMUM
    assert registry.get("ca-on/seniors_care_amount") is SENIORS_CARE_AMOUNT
    assert registry.get("ca-on/seniors_care_family_net_income") is SENIORS_CARE_FAMILY_NET_INCOME
    assert registry.get("ca-on/seniors_care_base_amount") is SENIORS_CARE_BASE_AMOUNT
    assert registry.get("ca-on/seniors_care_income_over_base") is SENIORS_CARE_INCOME_OVER_BASE
    assert registry.get("ca-on/seniors_care_reduction") is SENIORS_CARE_REDUCTION
    assert registry.get("ca-on/seniors_care_before_claim") is SENIORS_CARE_BEFORE_CLAIM
    assert registry.get("ca-on/seniors_care_credit") is SENIORS_CARE_CREDIT
    assert registry.get("ca-on/seniors_transit_paid") is SENIORS_TRANSIT_PAID
    assert (
        registry.get("ca-on/seniors_transit_amount_paid_at_most_maximum")
        is SENIORS_TRANSIT_AMOUNT_PAID_AT_MOST_MAXIMUM
    )
    assert registry.get("ca-on/seniors_transit_credit") is SENIORS_TRANSIT_CREDIT
    assert registry.get("ca-on/political_contributions") is POLITICAL_CONTRIBUTIONS
    assert (
        registry.get("ca-on/political_credit_column_1_line_2") is POLITICAL_CREDIT_COLUMN_1_LINE_2
    )
    assert (
        registry.get("ca-on/political_credit_column_1_line_3") is POLITICAL_CREDIT_COLUMN_1_LINE_3
    )
    assert (
        registry.get("ca-on/political_credit_column_1_line_5") is POLITICAL_CREDIT_COLUMN_1_LINE_5
    )
    assert (
        registry.get("ca-on/political_credit_column_1_line_6") is POLITICAL_CREDIT_COLUMN_1_LINE_6
    )
    assert (
        registry.get("ca-on/political_credit_column_1_line_7") is POLITICAL_CREDIT_COLUMN_1_LINE_7
    )
    assert (
        registry.get("ca-on/political_credit_column_2_line_2") is POLITICAL_CREDIT_COLUMN_2_LINE_2
    )
    assert (
        registry.get("ca-on/political_credit_column_2_line_3") is POLITICAL_CREDIT_COLUMN_2_LINE_3
    )
    assert (
        registry.get("ca-on/political_credit_column_2_line_5") is POLITICAL_CREDIT_COLUMN_2_LINE_5
    )
    assert (
        registry.get("ca-on/political_credit_column_2_line_6") is POLITICAL_CREDIT_COLUMN_2_LINE_6
    )
    assert (
        registry.get("ca-on/political_credit_column_2_line_7") is POLITICAL_CREDIT_COLUMN_2_LINE_7
    )
    assert (
        registry.get("ca-on/political_credit_column_3_line_2") is POLITICAL_CREDIT_COLUMN_3_LINE_2
    )
    assert (
        registry.get("ca-on/political_credit_column_3_line_3") is POLITICAL_CREDIT_COLUMN_3_LINE_3
    )
    assert (
        registry.get("ca-on/political_credit_column_3_line_5") is POLITICAL_CREDIT_COLUMN_3_LINE_5
    )
    assert (
        registry.get("ca-on/political_credit_column_3_line_6") is POLITICAL_CREDIT_COLUMN_3_LINE_6
    )
    assert (
        registry.get("ca-on/political_credit_column_3_line_7") is POLITICAL_CREDIT_COLUMN_3_LINE_7
    )
    assert registry.get("ca-on/political_credit_before_maximum") is POLITICAL_CREDIT_BEFORE_MAXIMUM
    assert registry.get("ca-on/political_credit") is POLITICAL_CREDIT
    assert (
        registry.get("ca-on/flow_through_share_slip_expenses") is FLOW_THROUGH_SHARE_SLIP_EXPENSES
    )
    assert registry.get("ca-on/flow_through_share_slips") is FLOW_THROUGH_SHARE_SLIPS
    assert registry.get("ca-on/flow_through_share_expenses") is FLOW_THROUGH_SHARE_EXPENSES
    assert registry.get("ca-on/flow_through_share_credit") is FLOW_THROUGH_SHARE_CREDIT
    assert registry.get("ca-on/coop_education_payroll") is COOP_EDUCATION_PAYROLL
    assert (
        registry.get("ca-on/coop_education_payroll_threshold") is COOP_EDUCATION_PAYROLL_THRESHOLD
    )
    assert (
        registry.get("ca-on/coop_education_payroll_over_threshold")
        is COOP_EDUCATION_PAYROLL_OVER_THRESHOLD
    )
    assert registry.get("ca-on/coop_education_payroll_range") is COOP_EDUCATION_PAYROLL_RANGE
    assert registry.get("ca-on/coop_education_phase_out_share") is COOP_EDUCATION_PHASE_OUT_SHARE
    assert registry.get("ca-on/coop_education_full_share") is COOP_EDUCATION_FULL_SHARE
    assert registry.get("ca-on/coop_education_remaining_share") is COOP_EDUCATION_REMAINING_SHARE
    assert (
        registry.get("ca-on/coop_education_placement_expenditures")
        is COOP_EDUCATION_PLACEMENT_EXPENDITURES
    )
    assert registry.get("ca-on/coop_education_placements") is COOP_EDUCATION_PLACEMENTS
    assert registry.get("ca-on/coop_education_placement_count") is COOP_EDUCATION_PLACEMENT_COUNT
    assert registry.get("ca-on/coop_education_credit") is COOP_EDUCATION_CREDIT
    assert registry.get("ca-on/ontario_credits_subtotal") is ONTARIO_CREDITS_SUBTOTAL
    assert registry.get("ca-on/ontario_credits") is ONTARIO_CREDITS
    assert registry.get("ca-on/refund_before_donation") is REFUND_BEFORE_DONATION
    assert registry.get("ca-on/opportunities_fund_donation") is OPPORTUNITIES_FUND_DONATION
    assert registry.get("ca-on/net_refund") is NET_REFUND
    assert (
        registry.get("ca-on/applies_for_energy_and_property_tax_credit")
        is APPLIES_FOR_ENERGY_AND_PROPERTY_TAX_CREDIT
    )
    assert (
        registry.get("ca-on/applies_for_northern_energy_credit")
        is APPLIES_FOR_NORTHERN_ENERGY_CREDIT
    )
    assert registry.get("ca-on/chooses_single_benefit_payment") is CHOOSES_SINGLE_BENEFIT_PAYMENT
    assert (
        registry.get("ca-on/applies_for_senior_homeowners_grant")
        is APPLIES_FOR_SENIOR_HOMEOWNERS_GRANT
    )
    assert (
        registry.get("ca-on/separate_residences_for_medical_reasons")
        is SEPARATE_RESIDENCES_FOR_MEDICAL_REASONS
    )
    assert registry.get("ca-on/lived_in_student_residence") is LIVED_IN_STUDENT_RESIDENCE
    assert registry.get("ca-on/rent_paid") is RENT_PAID
    assert registry.get("ca-on/property_tax_paid") is PROPERTY_TAX_PAID
    assert registry.get("ca-on/reserve_home_energy_costs") is RESERVE_HOME_ENERGY_COSTS
    assert registry.get("ca-on/public_long_term_care_paid") is PUBLIC_LONG_TERM_CARE_PAID
    assert (
        registry.get("ca-on/coop_claimed_as_partnership_member")
        is COOP_CLAIMED_AS_PARTNERSHIP_MEMBER
    )
    assert (
        registry.get("ca-on/coop_partnership_business_number") is COOP_PARTNERSHIP_BUSINESS_NUMBER
    )


def test_every_registered_kind_but_the_counts_lists_and_digits_is_money_in_the_package_namespace(
    registry: ArtifactRegistry,
) -> None:
    for identifier in REGISTERED - COUNTS - RECORD_LISTS - DIGITS:
        kind = registry.get(identifier)
        assert isinstance(kind, ArtifactKind)
        assert kind.identifier.startswith(f"{app.jurisdictions.ca_on.NAMESPACE}/")
        assert kind.value_type is Decimal, identifier


def test_the_counts_are_int_kinds_in_the_package_namespace(registry: ArtifactRegistry) -> None:
    assert COUNTS <= REGISTERED
    for identifier in COUNTS:
        kind = registry.get(identifier)
        assert isinstance(kind, ArtifactKind)
        assert kind.identifier.startswith(f"{app.jurisdictions.ca_on.NAMESPACE}/")
        assert kind.value_type is int, identifier


def test_the_flow_through_share_slips_are_a_record_list_of_the_slip_expenses(
    registry: ArtifactRegistry,
) -> None:
    assert RECORD_LISTS <= REGISTERED
    for identifier in RECORD_LISTS:
        kind = registry.get(identifier)
        assert isinstance(kind, RecordListKind)
        assert kind.identifier.startswith(f"{app.jurisdictions.ca_on.NAMESPACE}/")
    assert FLOW_THROUGH_SHARE_SLIPS.fields == (FLOW_THROUGH_SHARE_SLIP_EXPENSES,)
    assert FLOW_THROUGH_SHARE_SLIP_EXPENSES.value_type is Decimal


def test_the_caregiver_dependants_are_a_record_list_of_net_income_and_whether_claimed_on_58160(
    registry: ArtifactRegistry,
) -> None:
    # Worksheet ON428 "Line 58185 - Ontario caregiver amount": per dependant, line 2 "Dependant's
    # net income from line 23600 of their return" and line 4 "Amount claimed for this dependant
    # on line 58160 of your Form ON428, if any", which the record holds as whether this is the
    # dependant claimed there (0 or 1). Its own list: the Ontario sets differ from line 30450's.
    assert "ca-on/caregiver_dependants" in RECORD_LISTS
    assert isinstance(CAREGIVER_DEPENDANTS, RecordListKind)
    assert CAREGIVER_DEPENDANTS.identifier == "ca-on/caregiver_dependants"
    assert CAREGIVER_DEPENDANTS.value_type is RecordList
    assert CAREGIVER_DEPENDANTS.fields == (DEPENDANT_NET_INCOME, CLAIMED_AS_ELIGIBLE_DEPENDANT)
    assert registry.get("ca-on/caregiver_dependants") is CAREGIVER_DEPENDANTS
    assert CAREGIVER_DEPENDANTS is not INFIRM_DEPENDANTS
    assert CAREGIVER_DEPENDANTS.fields[0] is DEPENDANT_NET_INCOME
    assert CLAIMED_AS_ELIGIBLE_DEPENDANT.identifier == "ca-on/claimed_as_eligible_dependant"
    assert CLAIMED_AS_ELIGIBLE_DEPENDANT.value_type is int
    assert CLAIMED_AS_ELIGIBLE_DEPENDANT.non_negative is True


def test_the_caregiver_amount_is_a_non_negative_decimal(registry: ArtifactRegistry) -> None:
    # ON428 line 17 and line 58185 "Ontario caregiver amount (use Worksheet ON428)": the total of
    # the worksheet's line 5, each "if negative, enter "0"".
    assert CAREGIVER_AMOUNT.identifier == "ca-on/caregiver_amount"
    assert CAREGIVER_AMOUNT.value_type is Decimal
    assert CAREGIVER_AMOUNT.non_negative is True
    assert registry.kind("ca-on/caregiver_amount") is CAREGIVER_AMOUNT


def test_the_co_operative_education_placements_are_a_record_list_of_the_expenditures(
    registry: ArtifactRegistry,
) -> None:
    kind = registry.get("ca-on/coop_education_placements")

    assert isinstance(kind, RecordListKind)
    assert kind is COOP_EDUCATION_PLACEMENTS
    assert COOP_EDUCATION_PLACEMENTS.fields == (COOP_EDUCATION_PLACEMENT_EXPENDITURES,)
    assert COOP_EDUCATION_PLACEMENT_EXPENDITURES.value_type is Decimal
    assert COOP_EDUCATION_PLACEMENT_EXPENDITURES.non_negative is True


def test_the_co_operative_education_placement_count_is_a_non_negative_int_kind() -> None:
    assert COOP_EDUCATION_PLACEMENT_COUNT.identifier == "ca-on/coop_education_placement_count"
    assert COOP_EDUCATION_PLACEMENT_COUNT.value_type is int
    assert COOP_EDUCATION_PLACEMENT_COUNT.non_negative is True


def test_the_co_operative_education_payroll_and_credit_are_non_negative_amounts() -> None:
    for kind in (COOP_EDUCATION_PAYROLL, COOP_EDUCATION_CREDIT):
        assert kind.value_type is Decimal
        assert kind.non_negative is True


def test_the_disability_dependants_are_a_record_list_of_the_ontario_worksheets_figures(
    registry: ArtifactRegistry,
) -> None:
    # Worksheet ON428 "Line 58480 - Disability amount transferred from a dependant", per
    # dependant: whether they were "under 18 years of age on December 31, 2025", line 3 "Total
    # child care and attendant care expenses for this dependant claimed by you or another
    # person", line 8 "Enter the amount from line 28 of the dependant's Form ON428." and line 10
    # "Dependant's taxable income from line 26000 of their return": the four fields a record
    # holds, in the worksheet's line order (the caller lists only the dependants who qualify).
    assert "ca-on/disability_dependants" in RECORD_LISTS
    assert isinstance(DISABILITY_DEPENDANTS, RecordListKind)
    assert DISABILITY_DEPENDANTS.identifier == "ca-on/disability_dependants"
    assert DISABILITY_DEPENDANTS.value_type is RecordList
    assert DISABILITY_DEPENDANTS.non_negative is False
    assert DISABILITY_DEPENDANTS.fields == (
        DEPENDANT_UNDER_18,
        DEPENDANT_CARE_EXPENSES,
        DEPENDANT_ON428_LINE_28,
        DEPENDANT_TAXABLE_INCOME,
    )
    assert registry.get("ca-on/disability_dependants") is DISABILITY_DEPENDANTS


def test_the_ontario_disability_dependants_are_a_list_of_their_own() -> None:
    # Its own list, as the Ontario caregiver dependants are: the third figure is the dependant's
    # ON428 line 28, not line 98 of their federal return.
    assert DISABILITY_DEPENDANTS is not FEDERAL_DISABILITY_DEPENDANTS
    assert DISABILITY_DEPENDANTS.fields != FEDERAL_DISABILITY_DEPENDANTS.fields
    assert DISABILITY_DEPENDANTS.fields[:2] == FEDERAL_DISABILITY_DEPENDANTS.fields[:2]
    assert DISABILITY_DEPENDANTS.fields[3] is FEDERAL_DISABILITY_DEPENDANTS.fields[3]
    assert DEPENDANT_NET_INCOME not in DISABILITY_DEPENDANTS.fields


def test_the_dependant_on428_line_28_is_a_non_negative_decimal(registry: ArtifactRegistry) -> None:
    # Worksheet ON428 for line 58480, line 8 "Enter the amount from line 28 of the dependant's
    # Form ON428.": a starting amount from another person's return, a field of each record.
    assert DEPENDANT_ON428_LINE_28.identifier == "ca-on/dependant_on428_line_28"
    assert DEPENDANT_ON428_LINE_28.value_type is Decimal
    assert DEPENDANT_ON428_LINE_28.non_negative is True
    assert registry.kind("ca-on/dependant_on428_line_28") is DEPENDANT_ON428_LINE_28
    assert DEPENDANT_ON428_LINE_28 in CATALOG.kinds


def disability_record(**changes: object) -> dict[ArtifactKind[Any], object]:
    """One dependant aged 20 with a chosen ON428 line 28, with `changes` by field name."""
    record: dict[ArtifactKind[Any], object] = {
        DEPENDANT_UNDER_18: 0,
        DEPENDANT_CARE_EXPENSES: Decimal("0"),
        DEPENDANT_ON428_LINE_28: Decimal("15000"),
        DEPENDANT_TAXABLE_INCOME: Decimal("20000"),
    }
    names: dict[str, ArtifactKind[Any]] = {
        "under_18": DEPENDANT_UNDER_18,
        "care_expenses": DEPENDANT_CARE_EXPENSES,
        "on428_line_28": DEPENDANT_ON428_LINE_28,
        "taxable_income": DEPENDANT_TAXABLE_INCOME,
    }
    for name, value in changes.items():
        record[names[name]] = value
    return record


def test_the_disability_dependants_hold_the_four_figures_each_in_the_callers_order() -> None:
    dependants = RecordList(
        DISABILITY_DEPENDANTS.fields,
        [
            disability_record(),
            disability_record(under_18=1, care_expenses=Decimal("5000"), on428_line_28=Decimal(0)),
        ],
    )

    assert [record[DEPENDANT_UNDER_18] for record in dependants.records] == [0, 1]
    assert [record[DEPENDANT_CARE_EXPENSES] for record in dependants.records] == [
        Decimal("0"),
        Decimal("5000"),
    ]
    assert [record[DEPENDANT_ON428_LINE_28] for record in dependants.records] == [
        Decimal("15000"),
        Decimal("0"),
    ]
    assert [record[DEPENDANT_TAXABLE_INCOME] for record in dependants.records] == [
        Decimal("20000"),
        Decimal("20000"),
    ]


def test_there_may_be_no_disability_dependants() -> None:
    assert RecordList(DISABILITY_DEPENDANTS.fields, []).records == ()


@pytest.mark.parametrize(
    "missing",
    [
        DEPENDANT_UNDER_18,
        DEPENDANT_CARE_EXPENSES,
        DEPENDANT_ON428_LINE_28,
        DEPENDANT_TAXABLE_INCOME,
    ],
)
def test_a_disability_dependant_missing_a_figure_is_an_invalid_record(
    missing: ArtifactKind[Any],
) -> None:
    record = disability_record()
    del record[missing]

    with pytest.raises(InvalidRecordError, match=f"item 1: missing field {missing.identifier}"):
        RecordList(DISABILITY_DEPENDANTS.fields, [record])


def test_the_second_disability_dependant_is_named_by_its_position() -> None:
    record = disability_record()
    del record[DEPENDANT_ON428_LINE_28]

    with pytest.raises(
        InvalidRecordError, match="item 2: missing field ca-on/dependant_on428_line_28"
    ):
        RecordList(DISABILITY_DEPENDANTS.fields, [disability_record(), record])


def test_a_disability_dependant_with_another_figure_is_an_invalid_record() -> None:
    record = disability_record()
    record[DEPENDANT_NET_INCOME] = Decimal("5000")

    with pytest.raises(InvalidRecordError, match="item 1: unknown field ca/dependant_net_income"):
        RecordList(DISABILITY_DEPENDANTS.fields, [record])


@pytest.mark.parametrize(
    ("change", "identifier"),
    [
        ({"under_18": -1}, "ca/dependant_under_18"),
        ({"care_expenses": Decimal("-0.01")}, "ca/dependant_care_expenses"),
        ({"on428_line_28": Decimal("-1")}, "ca-on/dependant_on428_line_28"),
        ({"taxable_income": Decimal("-1")}, "ca/dependant_taxable_income"),
    ],
)
def test_a_negative_disability_dependant_figure_is_refused(
    change: dict[str, object], identifier: str
) -> None:
    with pytest.raises(NegativeArtifactError, match=f"item 1: {identifier} cannot be negative"):
        RecordList(DISABILITY_DEPENDANTS.fields, [disability_record(**change)])


@pytest.mark.parametrize(
    "change",
    [
        {"under_18": Decimal("1")},
        {"under_18": True},
        {"care_expenses": 5000},
        {"on428_line_28": "15000"},
        {"taxable_income": 20000.0},
    ],
)
def test_a_disability_dependant_figure_of_the_wrong_type_is_refused(
    change: dict[str, object],
) -> None:
    with pytest.raises(TypeError):
        RecordList(DISABILITY_DEPENDANTS.fields, [disability_record(**change)])


def test_the_disability_transferred_amount_is_a_non_negative_decimal(
    registry: ArtifactRegistry,
) -> None:
    # ON428 line 30 and line 58480 "Disability amount transferred from a dependant (use Worksheet
    # ON428)": the total of the worksheet's line 12 amounts, each the lesser of two amounts that
    # are at least "0".
    assert DISABILITY_TRANSFERRED_AMOUNT.identifier == "ca-on/disability_transferred_amount"
    assert DISABILITY_TRANSFERRED_AMOUNT.value_type is Decimal
    assert DISABILITY_TRANSFERRED_AMOUNT.non_negative is True
    assert registry.kind("ca-on/disability_transferred_amount") is DISABILITY_TRANSFERRED_AMOUNT


def test_the_lift_lines_that_print_no_floor_are_signed(registry: ArtifactRegistry) -> None:
    # Schedule ON428-A line 9 "Add lines 6 to 8." and line 24 "Add lines 21 to 23." print no floor
    # and add a figure that may be negative (line 21 is the caller's existing spouse net income,
    # `ca/spouse_net_income_before_adjustments`, which is signed). Lines 13 and 28 are floored.
    assert SIGNED <= REGISTERED
    for kind in (
        LIFT_NET_INCOME_AND_REPAYMENTS,
        LIFT_SPOUSE_NET_INCOME_AND_REPAYMENTS,
    ):
        assert kind.value_type is Decimal
        assert kind.non_negative is False, kind.identifier
        assert registry.kind(kind.identifier) is kind
    assert LIFT_ADJUSTED_NET_INCOME.non_negative is True
    assert LIFT_SPOUSE_ADJUSTED_NET_INCOME.non_negative is True


def test_the_lift_spouse_at_year_end_is_a_non_negative_count(registry: ArtifactRegistry) -> None:
    # Schedule ON428-A: "If you had a spouse or common-law partner at the end of the year,
    # complete Part B"; "If your spouse or common-law partner died at any time during the year,
    # complete Part A as if you were single", so the caller enters 0 then.
    assert LIFT_SPOUSE_AT_YEAR_END.identifier == "ca-on/lift_spouse_at_year_end"
    assert LIFT_SPOUSE_AT_YEAR_END.value_type is int
    assert LIFT_SPOUSE_AT_YEAR_END.non_negative is True
    assert registry.kind("ca-on/lift_spouse_at_year_end") is LIFT_SPOUSE_AT_YEAR_END


def test_every_kind_but_the_record_lists_the_signed_lines_and_digits_is_declared_non_negative(
    registry: ArtifactRegistry,
) -> None:
    for kind in CATALOG.kinds:
        if kind.identifier not in RECORD_LISTS | SIGNED | DIGITS:
            assert kind.non_negative is True, kind.identifier
    for identifier in REGISTERED - RECORD_LISTS - SIGNED - DIGITS:
        assert registry.kind(identifier).non_negative is True, identifier


def test_the_seniors_care_at_home_kinds_are_non_negative_amounts_and_a_claim_count() -> None:
    # Form ON479 lines 3 to 13 (line 63095): line 5 before and after its maximum, line 8 (family
    # net income), line 9 (the printed base amount), lines 10 and 12, line 13 before the claim and
    # as claimed, and the caller's 0/1 count "claims the Ontario seniors care at home tax credit".
    for kind in (
        SENIORS_CARE_BEFORE_MAXIMUM,
        SENIORS_CARE_AMOUNT,
        SENIORS_CARE_FAMILY_NET_INCOME,
        SENIORS_CARE_BASE_AMOUNT,
        SENIORS_CARE_INCOME_OVER_BASE,
        SENIORS_CARE_REDUCTION,
        SENIORS_CARE_BEFORE_CLAIM,
        SENIORS_CARE_CREDIT,
    ):
        assert kind.value_type is Decimal
        assert kind.non_negative is True
    assert CLAIMS_SENIORS_CARE_CREDIT.identifier == "ca-on/claims_seniors_care_credit"
    assert CLAIMS_SENIORS_CARE_CREDIT.value_type is int
    assert CLAIMS_SENIORS_CARE_CREDIT.non_negative is True


def test_the_on_ben_tick_boxes_are_counts_and_its_part_a_lines_amounts() -> None:
    # Form ON-BEN "Line 61020: If you met any of these conditions and are applying for the 2026
    # OEPTC, tick this box", lines 61040, 61060, 61070, 61080 and 61140: tick boxes, taken from
    # the caller as 0 or 1.
    for kind, identifier in (
        (APPLIES_FOR_ENERGY_AND_PROPERTY_TAX_CREDIT, "applies_for_energy_and_property_tax_credit"),
        (APPLIES_FOR_NORTHERN_ENERGY_CREDIT, "applies_for_northern_energy_credit"),
        (CHOOSES_SINGLE_BENEFIT_PAYMENT, "chooses_single_benefit_payment"),
        (APPLIES_FOR_SENIOR_HOMEOWNERS_GRANT, "applies_for_senior_homeowners_grant"),
        (SEPARATE_RESIDENCES_FOR_MEDICAL_REASONS, "separate_residences_for_medical_reasons"),
        (LIVED_IN_STUDENT_RESIDENCE, "lived_in_student_residence"),
    ):
        assert kind.identifier == f"ca-on/{identifier}"
        assert kind.value_type is int
        assert kind.non_negative is True
    # Part A "Line 61100: Enter the total amount of rent paid for your principal residence",
    # "Line 61120: Enter the total amount of property tax paid for your principal residence",
    # "Line 61210: ... enter the total amount of home energy costs (like electricity and heat)
    # paid for your principal residence" and "Line 61230: Enter the total amount paid for your
    # accommodation in a public long-term care home or non-profit long-term care home".
    for amount_kind, identifier in (
        (RENT_PAID, "rent_paid"),
        (PROPERTY_TAX_PAID, "property_tax_paid"),
        (RESERVE_HOME_ENERGY_COSTS, "reserve_home_energy_costs"),
        (PUBLIC_LONG_TERM_CARE_PAID, "public_long_term_care_paid"),
    ):
        assert amount_kind.identifier == f"ca-on/{identifier}"
        assert amount_kind.value_type is Decimal
        assert amount_kind.non_negative is True


def test_the_tax_reduction_conditions_are_non_negative_counts() -> None:
    # ON428 "Enter "0" on line 80 if any of the following applies to you": the five conditions
    # other than line 72 are the caller's 0 or 1, and the two counts the conditions give, whether
    # line 80 and lines 75 and 76 are completed, are 0 or 1; the caller's yes or no at a tie in
    # the net incomes is a count too.
    for kind in (
        NOT_RESIDENT_OF_CANADA_AT_START_OF_YEAR,
        NOT_RESIDENT_OF_ONTARIO_AT_YEAR_END,
        BANKRUPT_IN_YEAR,
        RETURN_FILED_BY_TRUSTEE_IN_BANKRUPTCY,
        NOT_CLAIMING_ONTARIO_TAX_REDUCTION,
        TAX_REDUCTION_CLAIMABLE,
        CLAIMS_TAX_REDUCTION_AMOUNTS_AT_EQUAL_NET_INCOME,
        TAX_REDUCTION_AMOUNTS_CLAIMABLE,
    ):
        assert kind.value_type is int, kind.identifier
        assert kind.non_negative is True, kind.identifier


def test_line_72_and_line_73_are_non_negative_amounts() -> None:
    # ON428 line 72 (additional tax for minimum tax purposes, as entered) and line 73 "Line 71
    # plus line 72 =".
    for kind in (ONTARIO_MINIMUM_TAX, ONTARIO_TAX_BEFORE_REDUCTION):
        assert kind.value_type is Decimal, kind.identifier
        assert kind.non_negative is True, kind.identifier


def test_the_co_operative_education_partnership_lines_are_a_yes_no_count_and_nine_digits(
    registry: ArtifactRegistry,
) -> None:
    # ON479 "Line 63265: Are you claiming this credit as a member of a partnership? 1 Yes or 2
    # No", taken as a count, 0 for no and 1 for yes, as the other yes/no answers are; and "Line
    # 63270: If yes, enter your nine-digit business number. (enter 9 digits)", a digits kind of
    # nine digits.
    assert COOP_CLAIMED_AS_PARTNERSHIP_MEMBER.identifier == (
        "ca-on/coop_claimed_as_partnership_member"
    )
    assert COOP_CLAIMED_AS_PARTNERSHIP_MEMBER.value_type is int
    assert COOP_CLAIMED_AS_PARTNERSHIP_MEMBER.non_negative is True
    assert COOP_PARTNERSHIP_BUSINESS_NUMBER.identifier == ("ca-on/coop_partnership_business_number")
    assert isinstance(COOP_PARTNERSHIP_BUSINESS_NUMBER, DigitsKind)
    assert COOP_PARTNERSHIP_BUSINESS_NUMBER.digits == 9
    assert COOP_PARTNERSHIP_BUSINESS_NUMBER.value_type is str
    assert registry.kind("ca-on/coop_partnership_business_number") == DigitsKind(
        "ca-on/coop_partnership_business_number", digits=9
    )
    assert DIGITS <= REGISTERED
    for identifier in DIGITS:
        assert isinstance(registry.kind(identifier), DigitsKind), identifier
