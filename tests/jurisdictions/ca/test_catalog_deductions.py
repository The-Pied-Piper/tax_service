"""Registered and money kinds of the federal catalog family `deductions`."""

from __future__ import annotations

from decimal import Decimal

from app.domain.artifact import ArtifactRegistry
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
    CPP_ADDITIONAL_MAXIMUM_PENSIONABLE_EARNINGS,
    CPP_BASIC_EXEMPTION,
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
    CPT20_EARNINGS,
    DEDUCTIONS_FROM_TOTAL_INCOME,
    EI_CONTROLLED_CORPORATION_EARNINGS,
    EI_EARNINGS_SUBJECT_TO_PREMIUM,
    EI_EXEMPT_SELF_EMPLOYMENT_INCOME,
    EI_INSURABLE_EARNINGS,
    EI_INSURABLE_EARNINGS_REMAINING,
    EI_MAXIMUM_INSURABLE_EARNINGS,
    EI_NET_SELF_EMPLOYMENT_INCOME,
    EI_SELF_EMPLOYMENT_EARNINGS,
    EI_SPECIAL_BENEFITS_AGREEMENT,
    ELECTED_SPLIT_PENSION_DEDUCTION,
    EXPLORATION_AND_DEVELOPMENT_EXPENSES,
    NET_INCOME,
    NET_INCOME_BEFORE_ADJUSTMENTS,
    NET_INCOME_LESS_UCCB_AND_RDSP_INCOME,
    NORTHERN_RESIDENTS_DEDUCTIONS,
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
    STANDARD_AMOUNT_ALLOCATED,
    STANDARD_AMOUNT_ALLOCATED_1,
    STANDARD_AMOUNT_ALLOCATED_2,
    STANDARD_AMOUNT_ALLOCATED_3,
    SUPPORT_PAYMENTS_DEDUCTION,
    TOTAL_CARRYING_CHARGES,
    TOTAL_INTEREST_EXPENSES,
    TOTAL_OTHER_EXPENSES,
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
    ):
        assert kind.value_type is Decimal, kind.identifier
