"""Registered and money kinds of the federal catalog family `deductions`."""

from __future__ import annotations

from decimal import Decimal

import pytest

from app.domain.artifact import ArtifactRegistry
from app.domain.errors import InvalidRecordError
from app.domain.record_list import RecordList, RecordListKind
from app.jurisdictions.ca.catalog import (
    ALLOWABLE_BUSINESS_INVESTMENT_LOSS,
    BUSINESS_INVESTMENT_LOSS,
    BUSINESS_INVESTMENT_LOSS_AFTER_REDUCTION,
    BUSINESS_INVESTMENT_LOSS_REDUCTION,
    BUSINESS_INVESTMENT_LOSS_REDUCTION_AVAILABLE,
    CANADIAN_ARMED_FORCES_AND_POLICE_DEDUCTION,
    CAPITAL_GAINS_DEDUCTIONS_1985_TO_1987,
    CAPITAL_GAINS_DEDUCTIONS_1988_AND_1989_ELIGIBLE_CAPITAL_PROPERTY,
    CAPITAL_GAINS_DEDUCTIONS_1988_AND_1989_OTHER_THAN_ELIGIBLE_CAPITAL_PROPERTY,
    CAPITAL_GAINS_DEDUCTIONS_1990_TO_1999,
    CAPITAL_GAINS_DEDUCTIONS_2000,
    CAPITAL_GAINS_DEDUCTIONS_2001_TO_2024,
    CAPITAL_GAINS_DEDUCTIONS_CLAIMED_1985_TO_2024,
    CARRYING_CHARGES_INTEREST_EXPENSES_AND_OTHER_EXPENSES,
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
    CPP_ACTUAL_BASE_CONTRIBUTIONS,
    CPP_ADDITIONAL_MAXIMUM_PENSIONABLE_EARNINGS,
    CPP_BASIC_EXEMPTION,
    CPP_CONTRIBUTIONS_DIFFERENCE,
    CPP_DEDUCTION_ON_SELF_EMPLOYMENT,
    CPP_EARNINGS_SUBJECT_TO_BASE_AND_FIRST_ADDITIONAL,
    CPP_EARNINGS_SUBJECT_TO_SECOND_ADDITIONAL,
    CPP_EARNINGS_UP_TO_MAXIMUM,
    CPP_ENHANCED_CONTRIBUTIONS,
    CPP_FIRST_ADDITIONAL_CONTRIBUTIONS,
    CPP_MAXIMUM_PENSIONABLE_EARNINGS,
    CPP_MONTHS,
    CPP_PART_4_COMPLETED,
    CPP_PENSIONABLE_EARNINGS,
    CPP_PENSIONABLE_EARNINGS_UP_TO_ADDITIONAL_MAXIMUM,
    CPP_SECOND_ADDITIONAL_CONTRIBUTIONS,
    CPP_SECOND_ADDITIONAL_EARNINGS_MAXIMUM,
    CPP_T4_BASE_AND_FIRST_ADDITIONAL_CONTRIBUTIONS,
    CPP_T4_SECOND_ADDITIONAL_CONTRIBUTIONS,
    CPT20_EARNINGS,
    DEDUCTIONS_FROM_TOTAL_INCOME,
    EI_BENEFITS_REPAYMENT,
    EI_CONTROLLED_CORPORATION_EARNINGS,
    EI_EARNINGS_SUBJECT_TO_PREMIUM,
    EI_EXCLUDED_SLIP_NET_INCOME,
    EI_EXCLUDED_SLIPS,
    EI_EXCLUDED_SLIPS_NET_INCOME,
    EI_EXEMPT_SELF_EMPLOYMENT_INCOME,
    EI_INSURABLE_EARNINGS,
    EI_INSURABLE_EARNINGS_REMAINING,
    EI_MAXIMUM_INSURABLE_EARNINGS,
    EI_NET_SELF_EMPLOYMENT_INCOME,
    EI_SELF_EMPLOYMENT_BEFORE_SLIPS,
    EI_SELF_EMPLOYMENT_EARNINGS,
    EI_SPECIAL_BENEFITS_AGREEMENT,
    ELECTED_SPLIT_PENSION_DEDUCTION,
    EXPLORATION_AND_DEVELOPMENT_EXPENSES,
    NET_INCOME,
    NET_INCOME_BEFORE_ADJUSTMENTS,
    NET_INCOME_BEFORE_ADJUSTMENTS_NOT_BELOW_ZERO,
    NET_INCOME_LESS_UCCB_AND_RDSP_INCOME,
    NORTHERN_RESIDENTS_DEDUCTIONS,
    OAS_AND_FEDERAL_SUPPLEMENTS,
    OAS_BENEFITS_BASE_AMOUNT,
    OAS_OVERPAYMENT_RECOVERED,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_1994,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_2024,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1994_TO_1996,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1997_TO_1999,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2000,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2001_TO_2023,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2024,
    OTHER_DEDUCTIONS,
    OTHER_PAYMENTS_DEDUCTION,
    OTHER_PAYMENTS_DEDUCTION_ABOVE_LIMIT,
    OTHER_PAYMENTS_DEDUCTION_AFTER_LIMIT,
    OTHER_PAYMENTS_LIMIT_INCOME,
    OTHER_PAYMENTS_WORKSHEET_LINE_9_OVER_LIMIT,
    OTHER_PAYMENTS_WORKSHEET_REQUIRED,
    OTHER_SPLIT_INCOME,
    PENSIONABLE_NET_SELF_EMPLOYMENT_EARNINGS,
    RDSP_INCOME_REPAYMENT,
    RESIDENCY_AMOUNT,
    RESIDENCY_DEDUCTION,
    RESIDENCY_NET_INCOME_LIMIT,
    SECURITY_OPTIONS_DEDUCTIONS,
    SELF_EMPLOYED_CPP_BASE_CONTRIBUTIONS,
    SELF_EMPLOYED_CPP_BASE_CREDIT,
    SELF_EMPLOYED_CPP_CONTRIBUTIONS_PAYABLE,
    SELF_EMPLOYED_CPP_DEDUCTION,
    SELF_EMPLOYED_CPP_ENHANCED_CONTRIBUTIONS,
    SELF_EMPLOYED_CPP_FIRST_ADDITIONAL_CONTRIBUTIONS,
    SELF_EMPLOYED_CPP_SECOND_ADDITIONAL_CONTRIBUTIONS,
    SELF_EMPLOYED_EI_PREMIUMS,
    SOCIAL_BENEFITS_LINE_5,
    SOCIAL_BENEFITS_LINE_6,
    SOCIAL_BENEFITS_LINE_10,
    SOCIAL_BENEFITS_LINE_11,
    SOCIAL_BENEFITS_LINE_14,
    SOCIAL_BENEFITS_LINE_15,
    SOCIAL_BENEFITS_LINE_17,
    SOCIAL_BENEFITS_LINE_18,
    SOCIAL_BENEFITS_LINE_19,
    SOCIAL_BENEFITS_LINE_21,
    SOCIAL_BENEFITS_REPAYMENT,
    SOCIAL_BENEFITS_REPAYMENT_APPLIES,
    SPLIT_INCOME_DIVIDENDS,
    SPLIT_INCOME_DIVIDENDS_OTHER_THAN_ELIGIBLE,
    STANDARD_AMOUNT_ALLOCATED,
    STANDARD_AMOUNT_ALLOCATED_1,
    STANDARD_AMOUNT_ALLOCATED_2,
    STANDARD_AMOUNT_ALLOCATED_3,
    SUPPORT_PAYMENTS_DEDUCTION,
    TOSI_ADJUSTED_NET_INCOME,
    TOSI_ADJUSTED_NET_INCOME_NOT_BELOW_ZERO,
    TOTAL_CARRYING_CHARGES,
    TOTAL_INTEREST_EXPENSES,
    TOTAL_OTHER_EXPENSES,
    TOTAL_SPLIT_INCOME,
    TRAVEL_DEDUCTION,
    TRAVEL_INDIVIDUAL,
    TRAVEL_INDIVIDUALS,
    TRAVEL_TOTAL_ZONE_A,
    TRAVEL_TOTAL_ZONE_B,
    TRAVEL_TRIPS,
    TRAVEL_ZONE_B_DEDUCTION,
    TRIP_BENEFIT_OR_STANDARD_AMOUNT,
    TRIP_LOWEST_RETURN_AIRFARE,
    TRIP_TRAVEL_EXPENSES,
    TRIP_ZONE,
    UCCB_AND_RDSP_INCOME,
    UCCB_AND_RDSP_INCOME_REPAYMENTS,
    UCCB_REPAYMENT,
    UNION_DUES,
    ZONE_A_ADDITIONAL_RESIDENCY_AMOUNT,
    ZONE_A_ADDITIONAL_RESIDENCY_DAYS,
    ZONE_A_BASIC_RESIDENCY_AMOUNT,
    ZONE_A_DAYS_LIVED,
    ZONE_A_RESIDENCY_AFTER_WORK_SITE,
    ZONE_A_RESIDENCY_AMOUNT,
    ZONE_A_SPECIAL_WORK_SITE_BENEFITS,
    ZONE_B_ADDITIONAL_RESIDENCY_AMOUNT,
    ZONE_B_ADDITIONAL_RESIDENCY_DAYS,
    ZONE_B_BASIC_RESIDENCY_AMOUNT,
    ZONE_B_DAYS_LIVED,
    ZONE_B_RESIDENCY_AFTER_WORK_SITE,
    ZONE_B_RESIDENCY_AMOUNT,
    ZONE_B_SPECIAL_WORK_SITE_BENEFITS,
)
from tests.jurisdictions.ca.catalog_snapshot import COUNTS, RECORD_LISTS, REGISTERED, SIGNED


def test_the_deductions_kinds_are_the_registered_ones(registry: ArtifactRegistry) -> None:
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
    assert registry.get("ca/zone_a_days_lived") is ZONE_A_DAYS_LIVED
    assert registry.get("ca/zone_a_additional_residency_days") is ZONE_A_ADDITIONAL_RESIDENCY_DAYS
    assert registry.get("ca/zone_a_basic_residency_amount") is ZONE_A_BASIC_RESIDENCY_AMOUNT
    assert (
        registry.get("ca/zone_a_additional_residency_amount") is ZONE_A_ADDITIONAL_RESIDENCY_AMOUNT
    )
    assert registry.get("ca/zone_a_residency_amount") is ZONE_A_RESIDENCY_AMOUNT
    assert registry.get("ca/zone_a_special_work_site_benefits") is ZONE_A_SPECIAL_WORK_SITE_BENEFITS
    assert registry.get("ca/zone_a_residency_after_work_site") is ZONE_A_RESIDENCY_AFTER_WORK_SITE
    assert registry.get("ca/zone_b_days_lived") is ZONE_B_DAYS_LIVED
    assert registry.get("ca/zone_b_additional_residency_days") is ZONE_B_ADDITIONAL_RESIDENCY_DAYS
    assert registry.get("ca/zone_b_basic_residency_amount") is ZONE_B_BASIC_RESIDENCY_AMOUNT
    assert (
        registry.get("ca/zone_b_additional_residency_amount") is ZONE_B_ADDITIONAL_RESIDENCY_AMOUNT
    )
    assert registry.get("ca/zone_b_residency_amount") is ZONE_B_RESIDENCY_AMOUNT
    assert registry.get("ca/zone_b_special_work_site_benefits") is ZONE_B_SPECIAL_WORK_SITE_BENEFITS
    assert registry.get("ca/zone_b_residency_after_work_site") is ZONE_B_RESIDENCY_AFTER_WORK_SITE
    assert registry.get("ca/residency_amount") is RESIDENCY_AMOUNT
    assert registry.get("ca/residency_net_income_limit") is RESIDENCY_NET_INCOME_LIMIT
    assert registry.get("ca/residency_deduction") is RESIDENCY_DEDUCTION
    assert registry.get("ca/travel_individual") is TRAVEL_INDIVIDUAL
    assert registry.get("ca/trip_zone") is TRIP_ZONE
    assert registry.get("ca/trip_benefit_or_standard_amount") is TRIP_BENEFIT_OR_STANDARD_AMOUNT
    assert registry.get("ca/trip_travel_expenses") is TRIP_TRAVEL_EXPENSES
    assert registry.get("ca/trip_lowest_return_airfare") is TRIP_LOWEST_RETURN_AIRFARE
    assert registry.get("ca/travel_trips") is TRAVEL_TRIPS
    assert registry.get("ca/standard_amount_allocated_1") is STANDARD_AMOUNT_ALLOCATED_1
    assert registry.get("ca/standard_amount_allocated_2") is STANDARD_AMOUNT_ALLOCATED_2
    assert registry.get("ca/standard_amount_allocated_3") is STANDARD_AMOUNT_ALLOCATED_3
    assert registry.get("ca/travel_individuals") is TRAVEL_INDIVIDUALS
    assert registry.get("ca/standard_amount_allocated") is STANDARD_AMOUNT_ALLOCATED
    assert registry.get("ca/travel_total_zone_a") is TRAVEL_TOTAL_ZONE_A
    assert registry.get("ca/travel_total_zone_b") is TRAVEL_TOTAL_ZONE_B
    assert registry.get("ca/travel_zone_b_deduction") is TRAVEL_ZONE_B_DEDUCTION
    assert registry.get("ca/travel_deduction") is TRAVEL_DEDUCTION
    assert registry.get("ca/northern_residents_deductions") is NORTHERN_RESIDENTS_DEDUCTIONS
    assert registry.get("ca/elected_split_pension_deduction") is ELECTED_SPLIT_PENSION_DEDUCTION
    assert registry.get("ca/union_dues") is UNION_DUES
    assert registry.get("ca/cpp_months") is CPP_MONTHS
    assert registry.get("ca/cpt20_earnings") is CPT20_EARNINGS
    assert registry.get("ca/cpp_part_4_completed") is CPP_PART_4_COMPLETED
    assert (
        registry.get("ca/ei_controlled_corporation_earnings") is EI_CONTROLLED_CORPORATION_EARNINGS
    )
    assert registry.get("ca/ei_exempt_self_employment_income") is EI_EXEMPT_SELF_EMPLOYMENT_INCOME
    assert registry.get("ca/ei_insurable_earnings") is EI_INSURABLE_EARNINGS
    assert registry.get("ca/ei_special_benefits_agreement") is EI_SPECIAL_BENEFITS_AGREEMENT
    assert registry.get("ca/cpp_enhanced_contributions") is CPP_ENHANCED_CONTRIBUTIONS
    assert (
        registry.get("ca/exploration_and_development_expenses")
        is EXPLORATION_AND_DEVELOPMENT_EXPENSES
    )
    assert registry.get("ca/other_deductions") is OTHER_DEDUCTIONS
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
    assert (
        registry.get("ca/capital_gains_deductions_1985_to_1987")
        is CAPITAL_GAINS_DEDUCTIONS_1985_TO_1987
    )
    assert (
        registry.get(
            "ca/capital_gains_deductions_1988_and_1989_other_than_eligible_capital_property"
        )
        is CAPITAL_GAINS_DEDUCTIONS_1988_AND_1989_OTHER_THAN_ELIGIBLE_CAPITAL_PROPERTY
    )
    assert (
        registry.get("ca/capital_gains_deductions_1988_and_1989_eligible_capital_property")
        is CAPITAL_GAINS_DEDUCTIONS_1988_AND_1989_ELIGIBLE_CAPITAL_PROPERTY
    )
    assert (
        registry.get("ca/capital_gains_deductions_1990_to_1999")
        is CAPITAL_GAINS_DEDUCTIONS_1990_TO_1999
    )
    assert registry.get("ca/capital_gains_deductions_2000") is CAPITAL_GAINS_DEDUCTIONS_2000
    assert (
        registry.get("ca/capital_gains_deductions_2001_to_2024")
        is CAPITAL_GAINS_DEDUCTIONS_2001_TO_2024
    )
    assert (
        registry.get("ca/capital_gains_deductions_claimed_1985_to_2024")
        is CAPITAL_GAINS_DEDUCTIONS_CLAIMED_1985_TO_2024
    )
    assert (
        registry.get("ca/other_business_investment_loss_reductions_1986_to_1994")
        is OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_1994
    )
    assert (
        registry.get("ca/other_business_investment_loss_reductions_1994_to_1996")
        is OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1994_TO_1996
    )
    assert (
        registry.get("ca/other_business_investment_loss_reductions_1997_to_1999")
        is OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1997_TO_1999
    )
    assert (
        registry.get("ca/other_business_investment_loss_reductions_2000")
        is OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2000
    )
    assert (
        registry.get("ca/other_business_investment_loss_reductions_2001_to_2023")
        is OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2001_TO_2023
    )
    assert (
        registry.get("ca/other_business_investment_loss_reductions_2024")
        is OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2024
    )
    assert (
        registry.get("ca/other_business_investment_loss_reductions_1986_to_2024")
        is OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_2024
    )
    assert (
        registry.get("ca/business_investment_loss_reduction_available")
        is BUSINESS_INVESTMENT_LOSS_REDUCTION_AVAILABLE
    )
    assert registry.get("ca/business_investment_loss") is BUSINESS_INVESTMENT_LOSS
    assert (
        registry.get("ca/business_investment_loss_reduction") is BUSINESS_INVESTMENT_LOSS_REDUCTION
    )
    assert (
        registry.get("ca/business_investment_loss_after_reduction")
        is BUSINESS_INVESTMENT_LOSS_AFTER_REDUCTION
    )
    assert (
        registry.get("ca/allowable_business_investment_loss") is ALLOWABLE_BUSINESS_INVESTMENT_LOSS
    )
    assert registry.get("ca/support_payments_deduction") is SUPPORT_PAYMENTS_DEDUCTION
    assert registry.get("ca/total_carrying_charges") is TOTAL_CARRYING_CHARGES
    assert registry.get("ca/total_interest_expenses") is TOTAL_INTEREST_EXPENSES
    assert registry.get("ca/total_other_expenses") is TOTAL_OTHER_EXPENSES
    assert (
        registry.get("ca/carrying_charges_interest_expenses_and_other_expenses")
        is CARRYING_CHARGES_INTEREST_EXPENSES_AND_OTHER_EXPENSES
    )
    assert registry.get("ca/cpp_maximum_pensionable_earnings") is CPP_MAXIMUM_PENSIONABLE_EARNINGS
    assert (
        registry.get("ca/cpp_second_additional_earnings_maximum")
        is CPP_SECOND_ADDITIONAL_EARNINGS_MAXIMUM
    )
    assert (
        registry.get("ca/cpp_additional_maximum_pensionable_earnings")
        is CPP_ADDITIONAL_MAXIMUM_PENSIONABLE_EARNINGS
    )
    assert registry.get("ca/cpp_basic_exemption") is CPP_BASIC_EXEMPTION
    assert (
        registry.get("ca/pensionable_net_self_employment_earnings")
        is PENSIONABLE_NET_SELF_EMPLOYMENT_EARNINGS
    )
    assert registry.get("ca/cpp_pensionable_earnings") is CPP_PENSIONABLE_EARNINGS
    assert (
        registry.get("ca/cpp_pensionable_earnings_up_to_additional_maximum")
        is CPP_PENSIONABLE_EARNINGS_UP_TO_ADDITIONAL_MAXIMUM
    )
    assert (
        registry.get("ca/cpp_earnings_subject_to_second_additional")
        is CPP_EARNINGS_SUBJECT_TO_SECOND_ADDITIONAL
    )
    assert registry.get("ca/cpp_earnings_up_to_maximum") is CPP_EARNINGS_UP_TO_MAXIMUM
    assert (
        registry.get("ca/cpp_earnings_subject_to_base_and_first_additional")
        is CPP_EARNINGS_SUBJECT_TO_BASE_AND_FIRST_ADDITIONAL
    )
    assert (
        registry.get("ca/self_employed_cpp_base_contributions")
        is SELF_EMPLOYED_CPP_BASE_CONTRIBUTIONS
    )
    assert (
        registry.get("ca/self_employed_cpp_first_additional_contributions")
        is SELF_EMPLOYED_CPP_FIRST_ADDITIONAL_CONTRIBUTIONS
    )
    assert (
        registry.get("ca/self_employed_cpp_second_additional_contributions")
        is SELF_EMPLOYED_CPP_SECOND_ADDITIONAL_CONTRIBUTIONS
    )
    assert (
        registry.get("ca/self_employed_cpp_enhanced_contributions")
        is SELF_EMPLOYED_CPP_ENHANCED_CONTRIBUTIONS
    )
    assert (
        registry.get("ca/self_employed_cpp_contributions_payable")
        is SELF_EMPLOYED_CPP_CONTRIBUTIONS_PAYABLE
    )
    assert registry.get("ca/self_employed_cpp_base_credit") is SELF_EMPLOYED_CPP_BASE_CREDIT
    assert registry.get("ca/self_employed_cpp_deduction") is SELF_EMPLOYED_CPP_DEDUCTION
    assert registry.get("ca/cpp_deduction_on_self_employment") is CPP_DEDUCTION_ON_SELF_EMPLOYMENT
    assert registry.get("ca/ei_self_employment_earnings") is EI_SELF_EMPLOYMENT_EARNINGS
    assert registry.get("ca/ei_net_self_employment_income") is EI_NET_SELF_EMPLOYMENT_INCOME
    assert registry.get("ca/ei_maximum_insurable_earnings") is EI_MAXIMUM_INSURABLE_EARNINGS
    assert registry.get("ca/ei_insurable_earnings_remaining") is EI_INSURABLE_EARNINGS_REMAINING
    assert registry.get("ca/ei_earnings_subject_to_premium") is EI_EARNINGS_SUBJECT_TO_PREMIUM
    assert registry.get("ca/self_employed_ei_premiums") is SELF_EMPLOYED_EI_PREMIUMS
    assert registry.get("ca/deductions_from_total_income") is DEDUCTIONS_FROM_TOTAL_INCOME
    assert registry.get("ca/net_income_before_adjustments") is NET_INCOME_BEFORE_ADJUSTMENTS
    assert registry.get("ca/net_income") is NET_INCOME
    assert registry.get("ca/oas_overpayment_recovered") is OAS_OVERPAYMENT_RECOVERED
    assert registry.get("ca/ei_benefits_repayment") is EI_BENEFITS_REPAYMENT
    assert (
        registry.get("ca/net_income_before_adjustments_not_below_zero")
        is NET_INCOME_BEFORE_ADJUSTMENTS_NOT_BELOW_ZERO
    )
    assert registry.get("ca/social_benefits_repayment_applies") is SOCIAL_BENEFITS_REPAYMENT_APPLIES
    assert registry.get("ca/oas_and_federal_supplements") is OAS_AND_FEDERAL_SUPPLEMENTS
    assert registry.get("ca/social_benefits_line_5") is SOCIAL_BENEFITS_LINE_5
    assert registry.get("ca/social_benefits_line_6") is SOCIAL_BENEFITS_LINE_6
    assert registry.get("ca/social_benefits_line_10") is SOCIAL_BENEFITS_LINE_10
    assert registry.get("ca/social_benefits_line_11") is SOCIAL_BENEFITS_LINE_11
    assert registry.get("ca/social_benefits_line_14") is SOCIAL_BENEFITS_LINE_14
    assert registry.get("ca/social_benefits_line_15") is SOCIAL_BENEFITS_LINE_15
    assert registry.get("ca/oas_benefits_base_amount") is OAS_BENEFITS_BASE_AMOUNT
    assert registry.get("ca/social_benefits_line_17") is SOCIAL_BENEFITS_LINE_17
    assert registry.get("ca/social_benefits_line_18") is SOCIAL_BENEFITS_LINE_18
    assert registry.get("ca/social_benefits_line_19") is SOCIAL_BENEFITS_LINE_19
    assert registry.get("ca/social_benefits_line_21") is SOCIAL_BENEFITS_LINE_21
    assert registry.get("ca/social_benefits_repayment") is SOCIAL_BENEFITS_REPAYMENT
    assert registry.get("ca/split_income_dividends") is SPLIT_INCOME_DIVIDENDS
    assert (
        registry.get("ca/split_income_dividends_other_than_eligible")
        is SPLIT_INCOME_DIVIDENDS_OTHER_THAN_ELIGIBLE
    )
    assert registry.get("ca/other_split_income") is OTHER_SPLIT_INCOME
    assert registry.get("ca/total_split_income") is TOTAL_SPLIT_INCOME
    assert registry.get("ca/tosi_adjusted_net_income") is TOSI_ADJUSTED_NET_INCOME
    assert (
        registry.get("ca/tosi_adjusted_net_income_not_below_zero")
        is TOSI_ADJUSTED_NET_INCOME_NOT_BELOW_ZERO
    )


def test_the_deductions_kinds_are_money() -> None:
    for kind in (
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
        ZONE_A_BASIC_RESIDENCY_AMOUNT,
        ZONE_A_ADDITIONAL_RESIDENCY_AMOUNT,
        ZONE_A_RESIDENCY_AMOUNT,
        ZONE_A_SPECIAL_WORK_SITE_BENEFITS,
        ZONE_A_RESIDENCY_AFTER_WORK_SITE,
        ZONE_B_BASIC_RESIDENCY_AMOUNT,
        ZONE_B_ADDITIONAL_RESIDENCY_AMOUNT,
        ZONE_B_RESIDENCY_AMOUNT,
        ZONE_B_SPECIAL_WORK_SITE_BENEFITS,
        ZONE_B_RESIDENCY_AFTER_WORK_SITE,
        RESIDENCY_AMOUNT,
        RESIDENCY_NET_INCOME_LIMIT,
        RESIDENCY_DEDUCTION,
        TRIP_BENEFIT_OR_STANDARD_AMOUNT,
        TRIP_TRAVEL_EXPENSES,
        TRIP_LOWEST_RETURN_AIRFARE,
        STANDARD_AMOUNT_ALLOCATED_1,
        STANDARD_AMOUNT_ALLOCATED_2,
        STANDARD_AMOUNT_ALLOCATED_3,
        STANDARD_AMOUNT_ALLOCATED,
        TRAVEL_TOTAL_ZONE_A,
        TRAVEL_TOTAL_ZONE_B,
        TRAVEL_ZONE_B_DEDUCTION,
        TRAVEL_DEDUCTION,
        NORTHERN_RESIDENTS_DEDUCTIONS,
        UNION_DUES,
        CPT20_EARNINGS,
        EI_CONTROLLED_CORPORATION_EARNINGS,
        EI_EXEMPT_SELF_EMPLOYMENT_INCOME,
        EI_INSURABLE_EARNINGS,
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
        CPP_MAXIMUM_PENSIONABLE_EARNINGS,
        CPP_SECOND_ADDITIONAL_EARNINGS_MAXIMUM,
        CPP_ADDITIONAL_MAXIMUM_PENSIONABLE_EARNINGS,
        CPP_BASIC_EXEMPTION,
        PENSIONABLE_NET_SELF_EMPLOYMENT_EARNINGS,
        CPP_PENSIONABLE_EARNINGS,
        CPP_PENSIONABLE_EARNINGS_UP_TO_ADDITIONAL_MAXIMUM,
        CPP_EARNINGS_SUBJECT_TO_SECOND_ADDITIONAL,
        CPP_EARNINGS_UP_TO_MAXIMUM,
        CPP_EARNINGS_SUBJECT_TO_BASE_AND_FIRST_ADDITIONAL,
        SELF_EMPLOYED_CPP_BASE_CONTRIBUTIONS,
        SELF_EMPLOYED_CPP_FIRST_ADDITIONAL_CONTRIBUTIONS,
        SELF_EMPLOYED_CPP_SECOND_ADDITIONAL_CONTRIBUTIONS,
        SELF_EMPLOYED_CPP_ENHANCED_CONTRIBUTIONS,
        SELF_EMPLOYED_CPP_CONTRIBUTIONS_PAYABLE,
        SELF_EMPLOYED_CPP_BASE_CREDIT,
        SELF_EMPLOYED_CPP_DEDUCTION,
        CPP_DEDUCTION_ON_SELF_EMPLOYMENT,
        EI_SELF_EMPLOYMENT_EARNINGS,
        EI_NET_SELF_EMPLOYMENT_INCOME,
        EI_MAXIMUM_INSURABLE_EARNINGS,
        EI_INSURABLE_EARNINGS_REMAINING,
        EI_EARNINGS_SUBJECT_TO_PREMIUM,
        SELF_EMPLOYED_EI_PREMIUMS,
        DEDUCTIONS_FROM_TOTAL_INCOME,
        NET_INCOME,
        SPLIT_INCOME_DIVIDENDS,
        SPLIT_INCOME_DIVIDENDS_OTHER_THAN_ELIGIBLE,
        OTHER_SPLIT_INCOME,
        TOTAL_SPLIT_INCOME,
        TOSI_ADJUSTED_NET_INCOME,
        TOSI_ADJUSTED_NET_INCOME_NOT_BELOW_ZERO,
        EI_BENEFITS_REPAYMENT,
        NET_INCOME_BEFORE_ADJUSTMENTS_NOT_BELOW_ZERO,
        OAS_AND_FEDERAL_SUPPLEMENTS,
        OAS_BENEFITS_BASE_AMOUNT,
        OAS_OVERPAYMENT_RECOVERED,
        SOCIAL_BENEFITS_LINE_5,
        SOCIAL_BENEFITS_LINE_6,
        SOCIAL_BENEFITS_LINE_10,
        SOCIAL_BENEFITS_LINE_11,
        SOCIAL_BENEFITS_LINE_14,
        SOCIAL_BENEFITS_LINE_15,
        SOCIAL_BENEFITS_LINE_17,
        SOCIAL_BENEFITS_LINE_18,
        SOCIAL_BENEFITS_LINE_19,
        SOCIAL_BENEFITS_LINE_21,
        SOCIAL_BENEFITS_REPAYMENT,
    ):
        assert kind.value_type is Decimal, kind.identifier


def test_the_tosi_adjusted_net_income_is_signed(registry: ArtifactRegistry) -> None:
    # Form T1206 Part 1 line 6 "TOSI-adjusted net income: line 4 plus line 5 If negative, enter
    # the result in brackets" (line 5 may itself be in brackets) prints no "(if negative, enter
    # "0")", so it is signed.
    assert TOSI_ADJUSTED_NET_INCOME.non_negative is False
    assert registry.kind("ca/tosi_adjusted_net_income") is TOSI_ADJUSTED_NET_INCOME
    assert "ca/tosi_adjusted_net_income" in SIGNED


def test_the_tosi_adjusted_net_income_not_below_zero_is_its_non_negative_twin(
    registry: ArtifactRegistry,
) -> None:
    # "(If the TOSI-adjusted net income at line 6 is negative, use the negative value when it is
    # part of an adjusted net income calculation, otherwise use zero.)": the signed line 6 and a
    # second kind for "otherwise use zero", which the basic personal amount, the age amount and
    # Schedule 6 line 7 read.
    assert TOSI_ADJUSTED_NET_INCOME_NOT_BELOW_ZERO is not TOSI_ADJUSTED_NET_INCOME
    assert TOSI_ADJUSTED_NET_INCOME_NOT_BELOW_ZERO.non_negative is True
    assert registry.kind("ca/tosi_adjusted_net_income_not_below_zero").non_negative is True
    assert "ca/tosi_adjusted_net_income_not_below_zero" not in SIGNED


def test_the_t1206_part_1_amounts_are_non_negative_decimals(registry: ArtifactRegistry) -> None:
    # Lines 1 to 3 are the caller's amounts of split income, and line 4 adds them.
    for kind in (
        SPLIT_INCOME_DIVIDENDS,
        SPLIT_INCOME_DIVIDENDS_OTHER_THAN_ELIGIBLE,
        OTHER_SPLIT_INCOME,
        TOTAL_SPLIT_INCOME,
    ):
        assert kind.identifier not in SIGNED, kind.identifier
        assert kind.value_type is Decimal, kind.identifier
        assert kind.non_negative is True, kind.identifier
        assert registry.kind(kind.identifier) is kind


def test_the_net_income_before_adjustments_not_below_zero_is_its_non_negative_twin(
    registry: ArtifactRegistry,
) -> None:
    # Federal Worksheet "Line 25000 - Other payments deduction" line 1 "Amount from line 23400 of
    # your return (if negative, enter "0")": line 23400 stays signed ("show in brackets") and,
    # once line 23500 reduces the net income of line 23600, this line needs its own floored kind.
    assert NET_INCOME_BEFORE_ADJUSTMENTS_NOT_BELOW_ZERO is not NET_INCOME_BEFORE_ADJUSTMENTS
    assert NET_INCOME_BEFORE_ADJUSTMENTS_NOT_BELOW_ZERO is not NET_INCOME
    assert NET_INCOME_BEFORE_ADJUSTMENTS_NOT_BELOW_ZERO.non_negative is True
    assert registry.kind("ca/net_income_before_adjustments_not_below_zero").non_negative is True
    assert "ca/net_income_before_adjustments_not_below_zero" not in SIGNED


def test_the_social_benefits_chart_lines_that_print_no_floor_are_signed(
    registry: ArtifactRegistry,
) -> None:
    # Federal Worksheet "Line 23500 - Social benefits repayment": line 6 "Net income before
    # adjustments from line 23400 of your return" (line 23400 may be negative, and the T1206 line
    # 4 is added), line 11 "Line 6 minus line 10 =" and line 15 "Line 11 plus line 14 Adjusted net
    # income" print no "(if negative, enter "0")".
    for kind in (SOCIAL_BENEFITS_LINE_6, SOCIAL_BENEFITS_LINE_11, SOCIAL_BENEFITS_LINE_15):
        assert kind.value_type is Decimal, kind.identifier
        assert kind.non_negative is False, kind.identifier
        assert registry.kind(kind.identifier) is kind
        assert kind.identifier in SIGNED


def test_the_other_social_benefits_chart_lines_are_non_negative(
    registry: ArtifactRegistry,
) -> None:
    # Lines 5 and 17 print "(if negative, enter "0")"; the others add, take 15% of, or compare
    # non-negative figures. The two caller inputs are slip boxes.
    for kind in (
        OAS_OVERPAYMENT_RECOVERED,
        EI_BENEFITS_REPAYMENT,
        OAS_AND_FEDERAL_SUPPLEMENTS,
        SOCIAL_BENEFITS_LINE_5,
        SOCIAL_BENEFITS_LINE_10,
        SOCIAL_BENEFITS_LINE_14,
        OAS_BENEFITS_BASE_AMOUNT,
        SOCIAL_BENEFITS_LINE_17,
        SOCIAL_BENEFITS_LINE_18,
        SOCIAL_BENEFITS_LINE_19,
        SOCIAL_BENEFITS_LINE_21,
        SOCIAL_BENEFITS_REPAYMENT,
    ):
        assert kind.identifier not in SIGNED, kind.identifier
        assert kind.non_negative is True, kind.identifier
        assert registry.kind(kind.identifier) is kind


def test_the_social_benefits_chart_applies_count_is_an_int_kind(registry: ArtifactRegistry) -> None:
    # The entry conditions of the chart ("Complete the chart below if one or both of the following
    # applies:") give a count, 1 when the chart applies and 0 otherwise.
    assert SOCIAL_BENEFITS_REPAYMENT_APPLIES.value_type is int
    assert registry.kind("ca/social_benefits_repayment_applies").value_type is int
    assert "ca/social_benefits_repayment_applies" in COUNTS


def test_the_ei_excluded_slips_are_a_record_list_of_the_net_income_of_each_slip(
    registry: ArtifactRegistry,
) -> None:
    # Schedule 13 line 1: "If you received a T4 slip for self-employment income with EI premiums
    # in box 18, do not include any net income (or net loss) reported on lines 13500, 13700,
    # 13900, 14100, and 14300 of your return for that slip": one record per such slip, whose one
    # field is the net income (or net loss) reported for it.
    assert isinstance(EI_EXCLUDED_SLIPS, RecordListKind)
    assert EI_EXCLUDED_SLIPS.identifier == "ca/ei_excluded_slips"
    assert EI_EXCLUDED_SLIPS.value_type is RecordList
    assert EI_EXCLUDED_SLIPS.non_negative is False
    assert EI_EXCLUDED_SLIPS.fields == (EI_EXCLUDED_SLIP_NET_INCOME,)
    assert registry.get("ca/ei_excluded_slips") is EI_EXCLUDED_SLIPS
    assert "ca/ei_excluded_slips" in RECORD_LISTS
    assert "ca/ei_excluded_slips" in REGISTERED


def test_the_net_income_of_an_excluded_slip_is_a_signed_decimal(
    registry: ArtifactRegistry,
) -> None:
    # "(or net loss)": a slip may report a loss, so the field is not declared non-negative.
    assert EI_EXCLUDED_SLIP_NET_INCOME.identifier == "ca/ei_excluded_slip_net_income"
    assert EI_EXCLUDED_SLIP_NET_INCOME.value_type is Decimal
    assert EI_EXCLUDED_SLIP_NET_INCOME.non_negative is False
    assert registry.kind("ca/ei_excluded_slip_net_income") is EI_EXCLUDED_SLIP_NET_INCOME
    assert "ca/ei_excluded_slip_net_income" in SIGNED


def test_the_ei_excluded_slips_hold_a_loss_and_may_be_empty() -> None:
    rows = RecordList(
        EI_EXCLUDED_SLIPS.fields,
        [
            {EI_EXCLUDED_SLIP_NET_INCOME: Decimal("20000")},
            {EI_EXCLUDED_SLIP_NET_INCOME: Decimal("-1500")},
        ],
    )

    assert [record[EI_EXCLUDED_SLIP_NET_INCOME] for record in rows.records] == [
        Decimal("20000"),
        Decimal("-1500"),
    ]
    assert RecordList(EI_EXCLUDED_SLIPS.fields, []).records == ()


def test_an_excluded_slip_missing_its_net_income_is_refused_naming_the_row() -> None:
    with pytest.raises(InvalidRecordError, match="item 1.*ei_excluded_slip_net_income"):
        RecordList(EI_EXCLUDED_SLIPS.fields, [{}])


def test_schedule_13_line_1_before_the_slips_is_signed(registry: ArtifactRegistry) -> None:
    # Line 1 is "the total amount from line 12200 plus line 27": before the slips and the "(if
    # negative, enter "0")" floor of the finished line 1, so it is not declared non-negative.
    assert EI_SELF_EMPLOYMENT_BEFORE_SLIPS.identifier == "ca/ei_self_employment_before_slips"
    assert EI_SELF_EMPLOYMENT_BEFORE_SLIPS.value_type is Decimal
    assert EI_SELF_EMPLOYMENT_BEFORE_SLIPS.non_negative is False
    assert registry.kind("ca/ei_self_employment_before_slips") is EI_SELF_EMPLOYMENT_BEFORE_SLIPS
    assert "ca/ei_self_employment_before_slips" in SIGNED


def test_the_net_income_of_all_the_excluded_slips_is_signed(registry: ArtifactRegistry) -> None:
    # The total of the slips' net income (or net loss) may be a loss.
    assert EI_EXCLUDED_SLIPS_NET_INCOME.identifier == "ca/ei_excluded_slips_net_income"
    assert EI_EXCLUDED_SLIPS_NET_INCOME.value_type is Decimal
    assert EI_EXCLUDED_SLIPS_NET_INCOME.non_negative is False
    assert registry.kind("ca/ei_excluded_slips_net_income") is EI_EXCLUDED_SLIPS_NET_INCOME
    assert "ca/ei_excluded_slips_net_income" in SIGNED


def test_schedule_13_line_1_stays_non_negative_after_the_slips(registry: ArtifactRegistry) -> None:
    # "(if negative, enter "0")" is on the finished line 1, ca/ei_self_employment_earnings.
    assert EI_SELF_EMPLOYMENT_EARNINGS is not EI_SELF_EMPLOYMENT_BEFORE_SLIPS
    assert EI_SELF_EMPLOYMENT_EARNINGS.non_negative is True
    assert "ca/ei_self_employment_earnings" not in SIGNED


# Schedule 8 Part 3 the box 16 and 16A totals the filer enters, and the lines
# that compare them with the required contributions. The kinds are reached through the module
# so that the rest of this file runs before they are declared.
def test_the_cpp_t4_box_totals_are_non_negative_money_the_filer_enters(
    registry: ArtifactRegistry,
) -> None:
    # Schedule 8 Part 3 line 8 and line 50340 "Total actual base and first additional
    # contributions on CPP pensionable earnings from box 16 of all of your T4 slips", and line 21
    # and line 50341 "Total actual second additional contributions on CPP pensionable earnings
    # from box 16A of all of your T4 slips": amounts the filer enters, never below zero.
    for identifier in (
        "ca/cpp_t4_base_and_first_additional_contributions",
        "ca/cpp_t4_second_additional_contributions",
    ):
        kind = registry.kind(identifier)
        assert kind.value_type is Decimal, identifier
        assert kind.non_negative is True, identifier
        assert identifier not in SIGNED, identifier
    assert (
        registry.kind("ca/cpp_t4_base_and_first_additional_contributions")
        is CPP_T4_BASE_AND_FIRST_ADDITIONAL_CONTRIBUTIONS
    )
    assert (
        registry.kind("ca/cpp_t4_second_additional_contributions")
        is CPP_T4_SECOND_ADDITIONAL_CONTRIBUTIONS
    )


def test_the_cpp_part_3_lines_that_print_no_brackets_are_non_negative(
    registry: ArtifactRegistry,
) -> None:
    # Line 9 is "amount from line 8 multiplied by 83.1933%", line 10 is "Line 8 minus line 9" (the
    # factor is below 100%, so it is never below zero) and line 13 is "Line 11 plus line 12": none
    # can be negative, and none prints "(if negative, show in brackets)".
    for identifier in (
        "ca/cpp_actual_base_contributions",
        "ca/cpp_actual_first_additional_contributions",
        "ca/cpp_required_base_and_first_additional_contributions",
    ):
        kind = registry.kind(identifier)
        assert kind.value_type is Decimal, identifier
        assert kind.non_negative is True, identifier
        assert identifier not in SIGNED, identifier
    assert registry.kind("ca/cpp_actual_base_contributions") is CPP_ACTUAL_BASE_CONTRIBUTIONS


def test_the_cpp_part_3_difference_lines_are_signed_as_their_brackets_say(
    registry: ArtifactRegistry,
) -> None:
    # Lines 16, 19, 20, 23 and 24 each print "(if negative, show in brackets)", so each is a
    # signed Decimal, a loss of contributions over the required ones included.
    for identifier in (
        "ca/cpp_base_contributions_difference",
        "ca/cpp_first_additional_contributions_difference",
        "ca/cpp_base_and_first_additional_contributions_difference",
        "ca/cpp_second_additional_contributions_difference",
        "ca/cpp_contributions_difference",
    ):
        kind = registry.kind(identifier)
        assert kind.value_type is Decimal, identifier
        assert kind.non_negative is False, identifier
        assert identifier in SIGNED, identifier
    assert registry.kind("ca/cpp_contributions_difference") is CPP_CONTRIBUTIONS_DIFFERENCE


# Schedule 8 Part 3a and Part 3b: the counts that carry the form's "if ... If not, enter "0""
# instructions, the lines of Part 3b and the three return lines they route. The kinds are reached
# through the registry so that the rest of this file runs before they are declared.
def test_the_cpp_part_3_routing_counts_are_non_negative_int_kinds(
    registry: ArtifactRegistry,
) -> None:
    # Each count is 1 when the form's condition holds and 0 otherwise: line 24 positive (the
    # Part 3a / Part 3b choice), lines 16, 19 and 23 positive or "0", and the "both positive" or
    # "negative and positive" conditions of lines 32, 35, 39, 42 and 46.
    for identifier in (
        "ca/cpp_line_24_positive",
        "ca/cpp_line_16_not_negative",
        "ca/cpp_line_19_not_negative",
        "ca/cpp_line_23_not_negative",
        "ca/cpp_line_16_negative_line_19_positive",
        "ca/cpp_line_23_and_line_33_positive",
        "ca/cpp_line_16_positive",
        "ca/cpp_line_23_and_line_40_positive",
        "ca/cpp_line_20_positive",
    ):
        kind = registry.kind(identifier)
        assert kind.value_type is int, identifier
        assert kind.non_negative is True, identifier
        assert identifier in COUNTS, identifier
        assert identifier not in SIGNED, identifier


def test_the_cpp_part_3b_whichever_is_less_candidates_are_signed(
    registry: ArtifactRegistry,
) -> None:
    # The lesser of two amounts of which one may be negative (lines 19, 23, 16 and 20 print "(if
    # negative, show in brackets)") is only used when its count says both are positive, but the
    # step that computes it runs for every return, so its kind is signed. "The result of line 23
    # minus line 35" (line 42) is negative when line 35 is more than line 23.
    for identifier in (
        "ca/cpp_part_3b_line_32_lesser",
        "ca/cpp_part_3b_line_35_lesser",
        "ca/cpp_part_3b_line_39_lesser",
        "ca/cpp_part_3b_line_23_less_line_35",
        "ca/cpp_part_3b_line_42_lesser",
        "ca/cpp_part_3b_line_46_lesser",
    ):
        kind = registry.kind(identifier)
        assert kind.value_type is Decimal, identifier
        assert kind.non_negative is False, identifier
        assert identifier in SIGNED, identifier


def test_the_cpp_part_3b_lines_and_the_three_return_lines_are_non_negative_money(
    registry: ArtifactRegistry,
) -> None:
    # The zero of "enter "0"", lines 30 to 48 of Part 3b (each is a chosen non-negative amount, a
    # sum of them, or a difference that cannot go below zero) and T1 line 30800, line 22215 and
    # line 44800 as the form routes them: none prints brackets.
    for identifier in (
        "ca/cpp_zero",
        "ca/cpp_part_3b_line_30",
        "ca/cpp_part_3b_line_31",
        "ca/cpp_part_3b_line_32",
        "ca/cpp_part_3b_line_33",
        "ca/cpp_part_3b_line_34",
        "ca/cpp_part_3b_line_35",
        "ca/cpp_part_3b_line_36",
        "ca/cpp_part_3b_line_37",
        "ca/cpp_part_3b_line_38",
        "ca/cpp_part_3b_line_39",
        "ca/cpp_part_3b_line_40",
        "ca/cpp_part_3b_line_41",
        "ca/cpp_part_3b_line_42",
        "ca/cpp_part_3b_line_43",
        "ca/cpp_part_3b_line_44",
        "ca/cpp_part_3b_line_45",
        "ca/cpp_part_3b_line_46",
        "ca/cpp_part_3b_line_47",
        "ca/cpp_part_3b_line_48",
        "ca/cpp_base_contributions_on_return",
        "ca/cpp_enhanced_contributions_on_return",
        "ca/cpp_overpayment",
    ):
        kind = registry.kind(identifier)
        assert kind.value_type is Decimal, identifier
        assert kind.non_negative is True, identifier
        assert identifier not in SIGNED, identifier
        assert identifier in REGISTERED, identifier


# Schedule 8 Part 5 lines 1 to 42 (self-employment income and other earnings when the filer also
# has employment income): the T4 CPT20 input, Part 3 line 2 and the lines of Part 5. The kinds are
# reached through the registry so that the rest of this file runs before they are declared.
def test_the_cpt20_earnings_shown_on_a_t4_slip_are_a_non_negative_input(
    registry: ArtifactRegistry,
) -> None:
    # Part 5 line 3 and line 50399 "Employment earnings shown on a T4 slip that you are electing
    # to pay additional CPP contributions on (complete Form CPT20)": an amount the filer enters,
    # never below zero, like line 2 (CPT20 earnings not shown on a T4 slip).
    kind = registry.kind("ca/cpt20_t4_earnings")
    assert kind.value_type is Decimal
    assert kind.non_negative is True
    assert "ca/cpt20_t4_earnings" not in SIGNED
    assert "ca/cpt20_t4_earnings" in REGISTERED
    assert kind is not CPT20_EARNINGS


def test_part_3_line_2_is_a_non_negative_amount_of_employment_earnings(
    registry: ArtifactRegistry,
) -> None:
    # Part 3 line 2 "Enter whichever is less: amount from line D of Part 2 or line 1": the lesser
    # of two non-negative amounts, read by Part 5 line 32 ("Amount from line 2 of Part 3").
    kind = registry.kind("ca/cpp_part_3_line_2")
    assert kind.value_type is Decimal
    assert kind.non_negative is True
    assert "ca/cpp_part_3_line_2" not in SIGNED
    assert "ca/cpp_part_3_line_2" in REGISTERED


def test_the_cpp_part_5_conditions_are_non_negative_int_counts(
    registry: ArtifactRegistry,
) -> None:
    # Each count is 1 when the form's condition holds and 0 otherwise: line 9's "If the amount
    # from line 20 of Part 3 is negative and line 23 of Part 3 is positive", line 15's "If the
    # amount from line 20 of Part 3 is positive and line 23 of Part 3 is negative" and the "If the
    # amount from line 33 is more than line 17" of lines 34 to 42.
    for identifier in (
        "ca/cpp_part_5_line_20_negative_line_23_positive",
        "ca/cpp_part_5_line_20_positive_line_23_negative",
        "ca/cpp_part_5_line_33_more_than_line_17",
    ):
        kind = registry.kind(identifier)
        assert kind.value_type is int, identifier
        assert kind.non_negative is True, identifier
        assert identifier in COUNTS, identifier
        assert identifier not in SIGNED, identifier


def test_the_cpp_part_5_lines_that_cannot_be_negative_are_non_negative_money(
    registry: ArtifactRegistry,
) -> None:
    # Lines 6, 12, 8 and 14 are "if positive. If not, enter "0"" or "as a positive amount"; lines
    # 9 and 15 are the lesser of two positive amounts or "0"; lines 19, 21, 28, 29 and 30 print
    # "(if negative, enter "0")" and line 25 enters "0" when it is negative.
    for number in (6, 8, 9, 12, 14, 15, 19, 21, 25, 28, 29, 30):
        identifier = f"ca/cpp_part_5_line_{number}"
        kind = registry.kind(identifier)
        assert kind.value_type is Decimal, identifier
        assert kind.non_negative is True, identifier
        assert identifier not in SIGNED, identifier
        assert identifier in REGISTERED, identifier


def test_the_cpp_part_5_lines_that_print_no_floor_are_signed(
    registry: ArtifactRegistry,
) -> None:
    # Line 4 "Add lines 1 to 3" (line 1 is a loss when line 27 is), lines 7, 13, 36, 39 and 41 are
    # plain "minus" lines, line 10 and line 16 add a plain "minus" line, line 20 multiplies line 10,
    # line 22 is the lesser of line 4 and line 21, line 33 adds line 4 and line 35 divides line
    # 16; none prints "(if negative, enter "0")". Line 42 is the lesser of lines 36 and 41, so it
    # is negative when line 41 is (a loss with employment income above $71,300): the form gives no
    # floor, so it is signed. The candidates of lines 9, 15 and 42 are signed as in Part 3b.
    for identifier in (
        "ca/cpp_part_5_line_4",
        "ca/cpp_part_5_line_7",
        "ca/cpp_part_5_line_9_lesser",
        "ca/cpp_part_5_line_10",
        "ca/cpp_part_5_line_13",
        "ca/cpp_part_5_line_15_lesser",
        "ca/cpp_part_5_line_16",
        "ca/cpp_part_5_line_20",
        "ca/cpp_part_5_line_22",
        "ca/cpp_part_5_line_33",
        "ca/cpp_part_5_line_35",
        "ca/cpp_part_5_line_36",
        "ca/cpp_part_5_line_39",
        "ca/cpp_part_5_line_41",
        "ca/cpp_part_5_line_42_lesser",
        "ca/cpp_part_5_line_42",
    ):
        kind = registry.kind(identifier)
        assert kind.value_type is Decimal, identifier
        assert kind.non_negative is False, identifier
        assert identifier in SIGNED, identifier
        assert identifier in REGISTERED, identifier
