"""Registered and money kinds of the federal catalog family `non_refundable_credits`."""

from __future__ import annotations

from decimal import Decimal

from app.domain.artifact import ArtifactRegistry
from app.jurisdictions.ca.catalog import (
    CANADA_EMPLOYMENT_AMOUNT,
    CAPITAL_GIFT_GAINS_DEDUCTION,
    CAPITAL_GIFT_TAXABLE_GAINS,
    CAPITAL_GIFTS_LIMIT_ADDITION,
    CAPITAL_GIFTS_TOTAL,
    CAPITAL_PROPERTY_GIFTS,
    CHARITABLE_DONATIONS,
    CHARITABLE_DONATIONS_CLAIMED,
    CHARITABLE_DONATIONS_LIMIT,
    CPP_BASE_CONTRIBUTIONS,
    CREDIT_AMOUNTS_AT_CREDIT_RATE,
    DEPRECIABLE_GIFT_CAPITAL_COST,
    DEPRECIABLE_GIFT_NET_PROCEEDS,
    DEPRECIABLE_GIFT_PROCEEDS_OR_COST,
    DEPRECIABLE_GIFT_RECAPTURED_DEPRECIATION,
    DEPRECIABLE_GIFTS,
    DONATION_FIRST_TIER_MAXIMUM,
    DONATION_HIGH_INCOME_THRESHOLD,
    DONATION_LIMIT_ON_NET_INCOME,
    DONATION_LIMIT_WITH_CAPITAL_GIFTS,
    DONATIONS_AND_GIFTS_CREDIT,
    DONATIONS_AND_GIFTS_TOTAL,
    DONATIONS_FIRST_TIER,
    DONATIONS_OVER_FIRST_TIER,
    DONATIONS_OVER_FIRST_TIER_AFTER_2016_GIFTS,
    ECOLOGICAL_AND_CULTURAL_GIFTS,
    ECOLOGICAL_GIFTS_BEFORE_2016,
    EI_PREMIUMS,
    FEDERAL_TAX_WITH_ITC_RECAPTURE,
    FIRST_TIER_DONATION_CREDIT,
    FOREIGN_CHARITY_DONATIONS,
    GOVERNMENT_DONATIONS,
    HIGH_INCOME_DONATION_CREDIT,
    HIGH_INCOME_DONATIONS,
    ITC_RECAPTURE,
    ITC_RECAPTURE_AT_15_PERCENT,
    ITC_RECAPTURE_AT_20_PERCENT,
    ITC_RECAPTURE_EXPENDITURE_AT_15_PERCENT,
    ITC_RECAPTURE_EXPENDITURE_AT_20_PERCENT,
    NON_REFUNDABLE_CREDIT_AMOUNTS,
    NON_REFUNDABLE_TAX_CREDITS,
    REGULAR_RATE_DONATION_CREDIT,
    REGULAR_RATE_DONATIONS,
    TAXABLE_INCOME_OVER_DONATION_THRESHOLD,
    TOP_UP_CREDITS_BASE,
    TOP_UP_EXCESS,
    TOP_UP_TAX_CREDIT,
    TOP_UP_THRESHOLD,
    TOTAL_CHARITABLE_DONATIONS,
    UNIVERSITY_DONATIONS_OUTSIDE_CANADA,
)


def test_the_non_refundable_credits_kinds_are_the_registered_ones(
    registry: ArtifactRegistry,
) -> None:
    assert registry.get("ca/non_refundable_credit_amounts") is NON_REFUNDABLE_CREDIT_AMOUNTS
    assert registry.get("ca/cpp_base_contributions") is CPP_BASE_CONTRIBUTIONS
    assert registry.get("ca/ei_premiums") is EI_PREMIUMS
    assert registry.get("ca/canada_employment_amount") is CANADA_EMPLOYMENT_AMOUNT
    assert registry.get("ca/non_refundable_tax_credits") is NON_REFUNDABLE_TAX_CREDITS
    assert (
        registry.get("ca/itc_recapture_expenditure_at_15_percent")
        is ITC_RECAPTURE_EXPENDITURE_AT_15_PERCENT
    )
    assert (
        registry.get("ca/itc_recapture_expenditure_at_20_percent")
        is ITC_RECAPTURE_EXPENDITURE_AT_20_PERCENT
    )
    assert registry.get("ca/itc_recapture_at_15_percent") is ITC_RECAPTURE_AT_15_PERCENT
    assert registry.get("ca/itc_recapture_at_20_percent") is ITC_RECAPTURE_AT_20_PERCENT
    assert registry.get("ca/itc_recapture") is ITC_RECAPTURE
    assert registry.get("ca/federal_tax_with_itc_recapture") is FEDERAL_TAX_WITH_ITC_RECAPTURE
    assert registry.get("ca/charitable_donations") is CHARITABLE_DONATIONS
    assert registry.get("ca/government_donations") is GOVERNMENT_DONATIONS
    assert (
        registry.get("ca/university_donations_outside_canada")
        is UNIVERSITY_DONATIONS_OUTSIDE_CANADA
    )
    assert registry.get("ca/foreign_charity_donations") is FOREIGN_CHARITY_DONATIONS
    assert registry.get("ca/ecological_and_cultural_gifts") is ECOLOGICAL_AND_CULTURAL_GIFTS
    assert registry.get("ca/ecological_gifts_before_2016") is ECOLOGICAL_GIFTS_BEFORE_2016
    assert (
        registry.get("ca/depreciable_gift_recaptured_depreciation")
        is DEPRECIABLE_GIFT_RECAPTURED_DEPRECIATION
    )
    assert registry.get("ca/depreciable_gift_net_proceeds") is DEPRECIABLE_GIFT_NET_PROCEEDS
    assert registry.get("ca/depreciable_gift_capital_cost") is DEPRECIABLE_GIFT_CAPITAL_COST
    assert registry.get("ca/capital_gift_taxable_gains") is CAPITAL_GIFT_TAXABLE_GAINS
    assert registry.get("ca/capital_gift_gains_deduction") is CAPITAL_GIFT_GAINS_DEDUCTION
    assert registry.get("ca/depreciable_gift_proceeds_or_cost") is DEPRECIABLE_GIFT_PROCEEDS_OR_COST
    assert registry.get("ca/depreciable_gifts") is DEPRECIABLE_GIFTS
    assert registry.get("ca/capital_property_gifts") is CAPITAL_PROPERTY_GIFTS
    assert registry.get("ca/total_charitable_donations") is TOTAL_CHARITABLE_DONATIONS
    assert registry.get("ca/donation_limit_on_net_income") is DONATION_LIMIT_ON_NET_INCOME
    assert registry.get("ca/capital_gifts_total") is CAPITAL_GIFTS_TOTAL
    assert registry.get("ca/capital_gifts_limit_addition") is CAPITAL_GIFTS_LIMIT_ADDITION
    assert registry.get("ca/donation_limit_with_capital_gifts") is DONATION_LIMIT_WITH_CAPITAL_GIFTS
    assert registry.get("ca/charitable_donations_limit") is CHARITABLE_DONATIONS_LIMIT
    assert registry.get("ca/charitable_donations_claimed") is CHARITABLE_DONATIONS_CLAIMED
    assert registry.get("ca/donations_and_gifts_total") is DONATIONS_AND_GIFTS_TOTAL
    assert registry.get("ca/donation_first_tier_maximum") is DONATION_FIRST_TIER_MAXIMUM
    assert registry.get("ca/donations_first_tier") is DONATIONS_FIRST_TIER
    assert registry.get("ca/donations_over_first_tier") is DONATIONS_OVER_FIRST_TIER
    assert (
        registry.get("ca/donations_over_first_tier_after_2016_gifts")
        is DONATIONS_OVER_FIRST_TIER_AFTER_2016_GIFTS
    )
    assert registry.get("ca/donation_high_income_threshold") is DONATION_HIGH_INCOME_THRESHOLD
    assert (
        registry.get("ca/taxable_income_over_donation_threshold")
        is TAXABLE_INCOME_OVER_DONATION_THRESHOLD
    )
    assert registry.get("ca/high_income_donations") is HIGH_INCOME_DONATIONS
    assert registry.get("ca/high_income_donation_credit") is HIGH_INCOME_DONATION_CREDIT
    assert registry.get("ca/regular_rate_donations") is REGULAR_RATE_DONATIONS
    assert registry.get("ca/regular_rate_donation_credit") is REGULAR_RATE_DONATION_CREDIT
    assert registry.get("ca/first_tier_donation_credit") is FIRST_TIER_DONATION_CREDIT
    assert registry.get("ca/donations_and_gifts_credit") is DONATIONS_AND_GIFTS_CREDIT
    assert registry.get("ca/credit_amounts_at_credit_rate") is CREDIT_AMOUNTS_AT_CREDIT_RATE
    assert registry.get("ca/top_up_credits_base") is TOP_UP_CREDITS_BASE
    assert registry.get("ca/top_up_threshold") is TOP_UP_THRESHOLD
    assert registry.get("ca/top_up_excess") is TOP_UP_EXCESS
    assert registry.get("ca/top_up_tax_credit") is TOP_UP_TAX_CREDIT


def test_the_non_refundable_credits_kinds_are_money() -> None:
    for kind in (
        NON_REFUNDABLE_CREDIT_AMOUNTS,
        CPP_BASE_CONTRIBUTIONS,
        EI_PREMIUMS,
        CANADA_EMPLOYMENT_AMOUNT,
        NON_REFUNDABLE_TAX_CREDITS,
        ITC_RECAPTURE_EXPENDITURE_AT_15_PERCENT,
        ITC_RECAPTURE_EXPENDITURE_AT_20_PERCENT,
        ITC_RECAPTURE_AT_15_PERCENT,
        ITC_RECAPTURE_AT_20_PERCENT,
        ITC_RECAPTURE,
        FEDERAL_TAX_WITH_ITC_RECAPTURE,
        CHARITABLE_DONATIONS,
        GOVERNMENT_DONATIONS,
        UNIVERSITY_DONATIONS_OUTSIDE_CANADA,
        FOREIGN_CHARITY_DONATIONS,
        ECOLOGICAL_AND_CULTURAL_GIFTS,
        ECOLOGICAL_GIFTS_BEFORE_2016,
        DEPRECIABLE_GIFT_RECAPTURED_DEPRECIATION,
        DEPRECIABLE_GIFT_NET_PROCEEDS,
        DEPRECIABLE_GIFT_CAPITAL_COST,
        CAPITAL_GIFT_TAXABLE_GAINS,
        CAPITAL_GIFT_GAINS_DEDUCTION,
        DEPRECIABLE_GIFT_PROCEEDS_OR_COST,
        DEPRECIABLE_GIFTS,
        CAPITAL_PROPERTY_GIFTS,
        TOTAL_CHARITABLE_DONATIONS,
        DONATION_LIMIT_ON_NET_INCOME,
        CAPITAL_GIFTS_TOTAL,
        CAPITAL_GIFTS_LIMIT_ADDITION,
        DONATION_LIMIT_WITH_CAPITAL_GIFTS,
        CHARITABLE_DONATIONS_LIMIT,
        CHARITABLE_DONATIONS_CLAIMED,
        DONATIONS_AND_GIFTS_TOTAL,
        DONATION_FIRST_TIER_MAXIMUM,
        DONATIONS_FIRST_TIER,
        DONATIONS_OVER_FIRST_TIER,
        DONATIONS_OVER_FIRST_TIER_AFTER_2016_GIFTS,
        DONATION_HIGH_INCOME_THRESHOLD,
        TAXABLE_INCOME_OVER_DONATION_THRESHOLD,
        HIGH_INCOME_DONATIONS,
        HIGH_INCOME_DONATION_CREDIT,
        REGULAR_RATE_DONATIONS,
        REGULAR_RATE_DONATION_CREDIT,
        FIRST_TIER_DONATION_CREDIT,
        DONATIONS_AND_GIFTS_CREDIT,
        CREDIT_AMOUNTS_AT_CREDIT_RATE,
        TOP_UP_CREDITS_BASE,
        TOP_UP_THRESHOLD,
        TOP_UP_EXCESS,
        TOP_UP_TAX_CREDIT,
    ):
        assert kind.value_type is Decimal, kind.identifier
