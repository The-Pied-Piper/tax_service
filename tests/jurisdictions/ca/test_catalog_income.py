"""Registered and money kinds of the federal catalog family `income`."""

from __future__ import annotations

from decimal import Decimal

from app.domain.artifact import ArtifactRegistry
from app.jurisdictions.ca.catalog import (
    CAPITAL_GAIN,
    CPP_OR_QPP_BENEFITS,
    CREDITS_AGAINST_BASIC_FEDERAL_TAX,
    DIVIDEND_TAX_CREDIT,
    DIVIDENDS_AMOUNT_A,
    DIVIDENDS_AMOUNT_A_LESS_B,
    DIVIDENDS_AMOUNT_B,
    DIVIDENDS_WITHOUT_A_SLIP_GROSSED_UP,
    EI_AND_OTHER_BENEFITS,
    ELECTED_SPLIT_PENSION_AMOUNT,
    ELIGIBLE_DIVIDENDS_CREDIT,
    ELIGIBLE_DIVIDENDS_GROSSED_UP,
    ELIGIBLE_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP,
    EMPLOYMENT_INCOME,
    FHSA_INCOME,
    FOREIGN_INVESTMENT_INCOME,
    INCOME_SUPPORT_BENEFITS,
    INTEREST_AND_OTHER_INVESTMENT_INCOME,
    INVESTMENT_INCOME_BEFORE_PRIOR_YEARS,
    INVESTMENT_INCOME_CREDITED_NOT_RECEIVED,
    INVESTMENT_INCOME_REPORTED_IN_PREVIOUS_YEARS,
    INVESTMENT_INCOME_WITHOUT_A_SLIP,
    INVESTMENT_ROYALTIES,
    NET_FEDERAL_SUPPLEMENTS,
    NET_PARTNERSHIP_INCOME,
    NO_SLIP_DIVIDEND_TAX_CREDIT,
    OLD_AGE_SECURITY,
    OTHER_DIVIDENDS_CREDIT,
    OTHER_DIVIDENDS_GROSSED_UP,
    OTHER_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP,
    OTHER_EMPLOYMENT_INCOME,
    OTHER_FHSA_INCOME,
    OTHER_INCOME,
    OTHER_PENSIONS_AND_SUPERANNUATION,
    RDSP_INCOME,
    RRSP_INCOME,
    SLIP_DIVIDEND_TAX_CREDIT,
    SLIP_TAXABLE_DIVIDENDS,
    SLIP_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
    SOCIAL_ASSISTANCE_PAYMENTS,
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
    TAXABLE_SCHOLARSHIPS,
    TAXABLE_SUPPORT_PAYMENTS,
    TOTAL_INCOME,
    UNIVERSAL_CHILD_CARE_BENEFIT,
    WORKERS_COMPENSATION_BENEFITS,
)


def test_the_income_kinds_are_the_registered_ones(registry: ArtifactRegistry) -> None:
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


def test_the_income_kinds_are_money() -> None:
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
    ):
        assert kind.value_type is Decimal, kind.identifier
