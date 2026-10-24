"""Registered and money kinds of the federal catalog family `other_inputs`."""

from __future__ import annotations

from decimal import Decimal

from app.domain.artifact import ArtifactRegistry
from app.jurisdictions.ca.catalog import (
    AGED_18_OR_OLDER_AT_END_OF_2025,
    DISABILITY_SUPPORTS_DEDUCTION,
    NET_BUSINESS_INCOME,
    NET_COMMISSION_INCOME,
    NET_FARMING_INCOME,
    NET_FISHING_INCOME,
    NET_PROFESSIONAL_INCOME,
    OTHER_EMPLOYMENT_EXPENSES,
    POLITICAL_CONTRIBUTIONS,
    RESIDENT_IN_CANADA_THROUGHOUT_2025,
    RL_10_LABOUR_SPONSORED_FUND_AMOUNT,
    SPOUSE_NET_INCOME_BEFORE_ADJUSTMENTS,
    SPOUSE_OR_COMMON_LAW_PARTNER_ON_DECEMBER_31,
    SPOUSE_RDSP_INCOME,
    SPOUSE_RDSP_INCOME_REPAYMENT,
    SPOUSE_UCCB_REPAYMENT,
    SPOUSE_UNIVERSAL_CHILD_CARE_BENEFIT,
    WAGE_LOSS_REPLACEMENT_PLAN_INCOME,
)


def test_the_other_inputs_kinds_are_the_registered_ones(registry: ArtifactRegistry) -> None:
    assert (
        registry.get("ca/rl_10_labour_sponsored_fund_amount") is RL_10_LABOUR_SPONSORED_FUND_AMOUNT
    )
    assert registry.get("ca/political_contributions") is POLITICAL_CONTRIBUTIONS
    assert registry.get("ca/disability_supports_deduction") is DISABILITY_SUPPORTS_DEDUCTION
    assert registry.get("ca/other_employment_expenses") is OTHER_EMPLOYMENT_EXPENSES
    assert registry.get("ca/net_business_income") is NET_BUSINESS_INCOME
    assert registry.get("ca/net_professional_income") is NET_PROFESSIONAL_INCOME
    assert registry.get("ca/net_commission_income") is NET_COMMISSION_INCOME
    assert registry.get("ca/net_farming_income") is NET_FARMING_INCOME
    assert registry.get("ca/net_fishing_income") is NET_FISHING_INCOME
    assert registry.get("ca/wage_loss_replacement_plan_income") is WAGE_LOSS_REPLACEMENT_PLAN_INCOME
    assert (
        registry.get("ca/resident_in_canada_throughout_2025") is RESIDENT_IN_CANADA_THROUGHOUT_2025
    )
    assert registry.get("ca/aged_18_or_older_at_end_of_2025") is AGED_18_OR_OLDER_AT_END_OF_2025
    assert (
        registry.get("ca/spouse_net_income_before_adjustments")
        is SPOUSE_NET_INCOME_BEFORE_ADJUSTMENTS
    )
    assert registry.get("ca/spouse_uccb_repayment") is SPOUSE_UCCB_REPAYMENT
    assert registry.get("ca/spouse_rdsp_income_repayment") is SPOUSE_RDSP_INCOME_REPAYMENT
    assert (
        registry.get("ca/spouse_universal_child_care_benefit")
        is SPOUSE_UNIVERSAL_CHILD_CARE_BENEFIT
    )
    assert registry.get("ca/spouse_rdsp_income") is SPOUSE_RDSP_INCOME
    assert (
        registry.get("ca/spouse_or_common_law_partner_on_december_31")
        is SPOUSE_OR_COMMON_LAW_PARTNER_ON_DECEMBER_31
    )


def test_the_other_inputs_kinds_are_money() -> None:
    for kind in (
        RL_10_LABOUR_SPONSORED_FUND_AMOUNT,
        POLITICAL_CONTRIBUTIONS,
        DISABILITY_SUPPORTS_DEDUCTION,
        OTHER_EMPLOYMENT_EXPENSES,
        NET_BUSINESS_INCOME,
        NET_PROFESSIONAL_INCOME,
        NET_COMMISSION_INCOME,
        NET_FARMING_INCOME,
        NET_FISHING_INCOME,
        WAGE_LOSS_REPLACEMENT_PLAN_INCOME,
        SPOUSE_NET_INCOME_BEFORE_ADJUSTMENTS,
        SPOUSE_UCCB_REPAYMENT,
        SPOUSE_RDSP_INCOME_REPAYMENT,
        SPOUSE_UNIVERSAL_CHILD_CARE_BENEFIT,
        SPOUSE_RDSP_INCOME,
    ):
        assert kind.value_type is Decimal, kind.identifier


def test_the_spouse_or_common_law_partner_on_december_31_is_a_non_negative_count() -> None:
    assert SPOUSE_OR_COMMON_LAW_PARTNER_ON_DECEMBER_31.value_type is int
    assert SPOUSE_OR_COMMON_LAW_PARTNER_ON_DECEMBER_31.non_negative is True
