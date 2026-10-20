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
    CPP_ENHANCED_CONTRIBUTIONS,
    CPP_FIRST_ADDITIONAL_CONTRIBUTIONS,
    CPP_SECOND_ADDITIONAL_CONTRIBUTIONS,
    DEDUCTIONS_FROM_TOTAL_INCOME,
    ELECTED_SPLIT_PENSION_DEDUCTION,
    EXPLORATION_AND_DEVELOPMENT_EXPENSES,
    NET_INCOME,
    NET_INCOME_BEFORE_ADJUSTMENTS,
    NET_INCOME_LESS_UCCB_AND_RDSP_INCOME,
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
    RDSP_INCOME_REPAYMENT,
    SECURITY_OPTIONS_DEDUCTIONS,
    SUPPORT_PAYMENTS_DEDUCTION,
    TOTAL_CARRYING_CHARGES,
    TOTAL_INTEREST_EXPENSES,
    TOTAL_OTHER_EXPENSES,
    UCCB_AND_RDSP_INCOME,
    UCCB_AND_RDSP_INCOME_REPAYMENTS,
    UCCB_REPAYMENT,
    UNION_DUES,
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
    assert registry.get("ca/elected_split_pension_deduction") is ELECTED_SPLIT_PENSION_DEDUCTION
    assert registry.get("ca/union_dues") is UNION_DUES
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
    ):
        assert kind.value_type is Decimal, kind.identifier
