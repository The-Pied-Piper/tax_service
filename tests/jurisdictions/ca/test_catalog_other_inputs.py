"""Registered and money kinds of the federal catalog family `other_inputs`, and the T929 inputs."""

from __future__ import annotations

from decimal import Decimal

from app.domain.artifact import ArtifactRegistry
from app.jurisdictions.ca.catalog import (
    AGED_18_OR_OLDER_AT_END_OF_2025,
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
    T929_COVID_19_PAYMENTS,
    T929_EARNINGS_SUPPLEMENTS,
    T929_EMPLOYMENT_INSURANCE_PART_2_SUPPORT,
    T929_EXPENSES_PAID,
    T929_EXPENSES_REIMBURSED,
    T929_INCOME_REPLACEMENT_SUPPORT,
    T929_NET_RESEARCH_GRANTS,
    T929_WAGE_EARNER_PROTECTION_AMOUNTS,
    T929_WEEKS_ATTENDED,
    WAGE_LOSS_REPLACEMENT_PLAN_INCOME,
)


def test_the_other_inputs_kinds_are_the_registered_ones(registry: ArtifactRegistry) -> None:
    assert (
        registry.get("ca/rl_10_labour_sponsored_fund_amount") is RL_10_LABOUR_SPONSORED_FUND_AMOUNT
    )
    assert registry.get("ca/political_contributions") is POLITICAL_CONTRIBUTIONS
    assert registry.get("ca/other_employment_expenses") is OTHER_EMPLOYMENT_EXPENSES
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
        OTHER_EMPLOYMENT_EXPENSES,
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


T929_MONEY_INPUTS = (
    T929_EXPENSES_PAID,
    T929_EXPENSES_REIMBURSED,
    T929_NET_RESEARCH_GRANTS,
    T929_EARNINGS_SUPPLEMENTS,
    T929_EMPLOYMENT_INSURANCE_PART_2_SUPPORT,
    T929_INCOME_REPLACEMENT_SUPPORT,
    T929_WAGE_EARNER_PROTECTION_AMOUNTS,
    T929_COVID_19_PAYMENTS,
)


def test_the_t929_inputs_are_the_registered_ones(registry: ArtifactRegistry) -> None:
    assert registry.get("ca/t929_expenses_paid") is T929_EXPENSES_PAID
    assert registry.get("ca/t929_expenses_reimbursed") is T929_EXPENSES_REIMBURSED
    assert registry.get("ca/t929_weeks_attended") is T929_WEEKS_ATTENDED
    assert registry.get("ca/t929_net_research_grants") is T929_NET_RESEARCH_GRANTS
    assert registry.get("ca/t929_earnings_supplements") is T929_EARNINGS_SUPPLEMENTS
    assert (
        registry.get("ca/t929_employment_insurance_part_2_support")
        is T929_EMPLOYMENT_INSURANCE_PART_2_SUPPORT
    )
    assert registry.get("ca/t929_income_replacement_support") is T929_INCOME_REPLACEMENT_SUPPORT
    assert (
        registry.get("ca/t929_wage_earner_protection_amounts")
        is T929_WAGE_EARNER_PROTECTION_AMOUNTS
    )
    assert registry.get("ca/t929_covid_19_payments") is T929_COVID_19_PAYMENTS


def test_the_t929_money_inputs_are_non_negative_decimals() -> None:
    for kind in T929_MONEY_INPUTS:
        assert kind.value_type is Decimal, kind.identifier
        assert kind.non_negative is True, kind.identifier


def test_the_t929_weeks_attended_is_a_non_negative_int_count() -> None:
    assert T929_WEEKS_ATTENDED.value_type is int
    assert T929_WEEKS_ATTENDED.non_negative is True
