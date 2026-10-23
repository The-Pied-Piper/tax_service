"""Registered and money kinds of the federal catalog family `non_refundable_credits`."""

from __future__ import annotations

from decimal import Decimal

from app.domain.artifact import ArtifactRegistry
from app.jurisdictions.ca.catalog import (
    AMOUNTS_TRANSFERRED_FROM_SPOUSE,
    BASIC_FEDERAL_TAX_WITH_DIVIDEND_CREDIT,
    CANADA_EMPLOYMENT_AMOUNT,
    CANADA_TRAINING_CREDIT_BASIS,
    CANADA_TRAINING_CREDIT_CLAIMED,
    CANADA_TRAINING_CREDIT_LIMIT,
    CANADA_TRAINING_CREDIT_MAXIMUM,
    CANADIAN_TUITION_AVAILABLE,
    CANADIAN_TUITION_FEES,
    CAPITAL_GIFT_GAINS_DEDUCTION,
    CAPITAL_GIFT_TAXABLE_GAINS,
    CAPITAL_GIFTS_LIMIT_ADDITION,
    CAPITAL_GIFTS_TOTAL,
    CAPITAL_PROPERTY_GIFTS,
    CHARITABLE_DONATIONS,
    CHARITABLE_DONATIONS_CLAIMED,
    CHARITABLE_DONATIONS_LIMIT,
    CPP_BASE_CONTRIBUTIONS,
    CPP_BASE_CONTRIBUTIONS_ON_SELF_EMPLOYMENT,
    CREDIT_AMOUNTS_AT_CREDIT_RATE,
    CREDIT_AMOUNTS_SUBTOTAL,
    CURRENT_YEAR_TUITION_AVAILABLE,
    CURRENT_YEAR_TUITION_CLAIMED,
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
    EI_PREMIUMS_ON_SELF_EMPLOYMENT,
    FEDERAL_FOREIGN_TAX_CREDIT,
    FEDERAL_NON_BUSINESS_FOREIGN_TAX_CREDIT,
    FEDERAL_TAX_LESS_FOREIGN_TAX_CREDIT,
    FEDERAL_TAX_ON_SPLIT_INCOME,
    FEDERAL_TAX_WITH_ITC_RECAPTURE,
    FEDERAL_TAX_WITH_SPLIT_INCOME,
    FEDERAL_TUITION_AMOUNT,
    FIRST_NATIONS_ABATEMENT,
    FIRST_TIER_DONATION_CREDIT,
    FOREIGN_CHARITY_DONATIONS,
    FOREIGN_TAX_CREDIT_BASIC_FEDERAL_TAX,
    FOREIGN_TAX_CREDIT_NET_INCOME,
    FOREIGN_TAX_CREDIT_NET_INCOME_BEFORE_SPLIT_INCOME,
    FOREIGN_TAX_CREDIT_NET_INCOME_DEDUCTIONS,
    FOREIGN_TAX_CREDIT_NET_INCOME_WITH_SPLIT_INCOME,
    FOREIGN_TUITION_FEES,
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
    SPOUSE_ADJUSTED_TAXABLE_INCOME,
    SPOUSE_CREDITS_USED,
    SPOUSE_DESIGNATED_TUITION,
    SPOUSE_INCOME_FOR_TRANSFER,
    SPOUSE_NOT_SEPARATED_90_DAYS,
    SPOUSE_RETURN_AGE_AMOUNT,
    SPOUSE_RETURN_BASIC_PERSONAL_AMOUNT,
    SPOUSE_RETURN_DISABILITY_AMOUNT,
    SPOUSE_RETURN_FEDERAL_BASIC_TAX,
    SPOUSE_RETURN_FEDERAL_TUITION_AMOUNT,
    SPOUSE_RETURN_INFIRM_CHILDREN_AMOUNT,
    SPOUSE_RETURN_LINE_96,
    SPOUSE_RETURN_PENSION_INCOME_AMOUNT,
    SPOUSE_RETURN_TAXABLE_INCOME,
    SPOUSE_TRANSFERABLE_AMOUNTS,
    SPOUSE_UNUSED_AMOUNTS,
    TAXABLE_INCOME_OVER_DONATION_THRESHOLD,
    TOP_UP_CREDITS_BASE,
    TOP_UP_EXCESS,
    TOP_UP_TAX_CREDIT,
    TOP_UP_THRESHOLD,
    TOSI_ADJUSTED_TAXABLE_INCOME,
    TOTAL_CHARITABLE_DONATIONS,
    TOTAL_TUITION_AVAILABLE,
    TUITION_AVAILABLE_TO_TRANSFER,
    TUITION_CARRIED_FORWARD,
    TUITION_INCOME_BASE,
    TUITION_INCOME_LESS_CREDITS,
    TUITION_INCOME_REMAINING,
    TUITION_INCOME_WITH_TOSI,
    TUITION_TRANSFER_ELECTED,
    TUITION_TRANSFER_LIMIT,
    TUITION_TRANSFERRED,
    TUITION_TRANSFERRED_FROM_CHILD,
    UNIVERSITY_DONATIONS_OUTSIDE_CANADA,
    UNUSED_FEDERAL_TUITION,
    UNUSED_TUITION_CLAIMED,
    UNUSED_TUITION_FROM_2024,
)
from tests.jurisdictions.ca.catalog_snapshot import SIGNED


def test_the_non_refundable_credits_kinds_are_the_registered_ones(
    registry: ArtifactRegistry,
) -> None:
    assert registry.get("ca/non_refundable_credit_amounts") is NON_REFUNDABLE_CREDIT_AMOUNTS
    assert registry.get("ca/cpp_base_contributions") is CPP_BASE_CONTRIBUTIONS
    assert (
        registry.get("ca/cpp_base_contributions_on_self_employment")
        is CPP_BASE_CONTRIBUTIONS_ON_SELF_EMPLOYMENT
    )
    assert registry.get("ca/ei_premiums") is EI_PREMIUMS
    assert registry.get("ca/ei_premiums_on_self_employment") is EI_PREMIUMS_ON_SELF_EMPLOYMENT
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
    assert registry.get("ca/federal_tax_on_split_income") is FEDERAL_TAX_ON_SPLIT_INCOME
    assert registry.get("ca/federal_tax_with_split_income") is FEDERAL_TAX_WITH_SPLIT_INCOME
    assert registry.get("ca/tosi_adjusted_taxable_income") is TOSI_ADJUSTED_TAXABLE_INCOME
    assert registry.get("ca/canadian_tuition_fees") is CANADIAN_TUITION_FEES
    assert registry.get("ca/canada_training_credit_limit") is CANADA_TRAINING_CREDIT_LIMIT
    assert registry.get("ca/canada_training_credit_claimed") is CANADA_TRAINING_CREDIT_CLAIMED
    assert registry.get("ca/foreign_tuition_fees") is FOREIGN_TUITION_FEES
    assert registry.get("ca/unused_tuition_from_2024") is UNUSED_TUITION_FROM_2024
    assert registry.get("ca/tuition_transfer_elected") is TUITION_TRANSFER_ELECTED
    assert registry.get("ca/tuition_transferred_from_child") is TUITION_TRANSFERRED_FROM_CHILD
    assert registry.get("ca/canada_training_credit_basis") is CANADA_TRAINING_CREDIT_BASIS
    assert registry.get("ca/canada_training_credit_maximum") is CANADA_TRAINING_CREDIT_MAXIMUM
    assert registry.get("ca/canadian_tuition_available") is CANADIAN_TUITION_AVAILABLE
    assert registry.get("ca/current_year_tuition_available") is CURRENT_YEAR_TUITION_AVAILABLE
    assert registry.get("ca/total_tuition_available") is TOTAL_TUITION_AVAILABLE
    assert registry.get("ca/tuition_income_base") is TUITION_INCOME_BASE
    assert registry.get("ca/tuition_income_with_tosi") is TUITION_INCOME_WITH_TOSI
    assert registry.get("ca/credit_amounts_subtotal") is CREDIT_AMOUNTS_SUBTOTAL
    assert registry.get("ca/tuition_income_less_credits") is TUITION_INCOME_LESS_CREDITS
    assert registry.get("ca/unused_tuition_claimed") is UNUSED_TUITION_CLAIMED
    assert registry.get("ca/tuition_income_remaining") is TUITION_INCOME_REMAINING
    assert registry.get("ca/current_year_tuition_claimed") is CURRENT_YEAR_TUITION_CLAIMED
    assert registry.get("ca/federal_tuition_amount") is FEDERAL_TUITION_AMOUNT
    assert registry.get("ca/unused_federal_tuition") is UNUSED_FEDERAL_TUITION
    assert registry.get("ca/tuition_transfer_limit") is TUITION_TRANSFER_LIMIT
    assert registry.get("ca/tuition_available_to_transfer") is TUITION_AVAILABLE_TO_TRANSFER
    assert registry.get("ca/tuition_transferred") is TUITION_TRANSFERRED
    assert registry.get("ca/tuition_carried_forward") is TUITION_CARRIED_FORWARD
    assert registry.get("ca/spouse_return_age_amount") is SPOUSE_RETURN_AGE_AMOUNT
    assert (
        registry.get("ca/spouse_return_infirm_children_amount")
        is SPOUSE_RETURN_INFIRM_CHILDREN_AMOUNT
    )
    assert (
        registry.get("ca/spouse_return_pension_income_amount")
        is SPOUSE_RETURN_PENSION_INCOME_AMOUNT
    )
    assert registry.get("ca/spouse_return_disability_amount") is SPOUSE_RETURN_DISABILITY_AMOUNT
    assert registry.get("ca/spouse_designated_tuition") is SPOUSE_DESIGNATED_TUITION
    assert registry.get("ca/spouse_return_taxable_income") is SPOUSE_RETURN_TAXABLE_INCOME
    assert registry.get("ca/spouse_return_federal_basic_tax") is SPOUSE_RETURN_FEDERAL_BASIC_TAX
    assert (
        registry.get("ca/spouse_return_basic_personal_amount")
        is SPOUSE_RETURN_BASIC_PERSONAL_AMOUNT
    )
    assert registry.get("ca/spouse_return_line_96") is SPOUSE_RETURN_LINE_96
    assert (
        registry.get("ca/spouse_return_federal_tuition_amount")
        is SPOUSE_RETURN_FEDERAL_TUITION_AMOUNT
    )
    assert registry.get("ca/spouse_transferable_amounts") is SPOUSE_TRANSFERABLE_AMOUNTS
    assert registry.get("ca/spouse_income_for_transfer") is SPOUSE_INCOME_FOR_TRANSFER
    assert registry.get("ca/spouse_credits_used") is SPOUSE_CREDITS_USED
    assert registry.get("ca/spouse_adjusted_taxable_income") is SPOUSE_ADJUSTED_TAXABLE_INCOME
    assert registry.get("ca/spouse_unused_amounts") is SPOUSE_UNUSED_AMOUNTS
    assert registry.get("ca/amounts_transferred_from_spouse") is AMOUNTS_TRANSFERRED_FROM_SPOUSE
    assert registry.get("ca/spouse_not_separated_90_days") is SPOUSE_NOT_SEPARATED_90_DAYS


def test_the_non_refundable_credits_kinds_are_money() -> None:
    for kind in (
        NON_REFUNDABLE_CREDIT_AMOUNTS,
        CPP_BASE_CONTRIBUTIONS,
        CPP_BASE_CONTRIBUTIONS_ON_SELF_EMPLOYMENT,
        EI_PREMIUMS,
        EI_PREMIUMS_ON_SELF_EMPLOYMENT,
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
        FEDERAL_TAX_ON_SPLIT_INCOME,
        FEDERAL_TAX_WITH_SPLIT_INCOME,
        CANADIAN_TUITION_FEES,
        CANADA_TRAINING_CREDIT_LIMIT,
        CANADA_TRAINING_CREDIT_CLAIMED,
        FOREIGN_TUITION_FEES,
        UNUSED_TUITION_FROM_2024,
        TUITION_TRANSFER_ELECTED,
        TUITION_TRANSFERRED_FROM_CHILD,
        CANADA_TRAINING_CREDIT_BASIS,
        CANADA_TRAINING_CREDIT_MAXIMUM,
        CANADIAN_TUITION_AVAILABLE,
        CURRENT_YEAR_TUITION_AVAILABLE,
        TOTAL_TUITION_AVAILABLE,
        TUITION_INCOME_BASE,
        TOSI_ADJUSTED_TAXABLE_INCOME,
        TUITION_INCOME_WITH_TOSI,
        CREDIT_AMOUNTS_SUBTOTAL,
        TUITION_INCOME_LESS_CREDITS,
        UNUSED_TUITION_CLAIMED,
        TUITION_INCOME_REMAINING,
        CURRENT_YEAR_TUITION_CLAIMED,
        FEDERAL_TUITION_AMOUNT,
        UNUSED_FEDERAL_TUITION,
        TUITION_TRANSFER_LIMIT,
        TUITION_AVAILABLE_TO_TRANSFER,
        TUITION_TRANSFERRED,
        TUITION_CARRIED_FORWARD,
        SPOUSE_RETURN_AGE_AMOUNT,
        SPOUSE_RETURN_INFIRM_CHILDREN_AMOUNT,
        SPOUSE_RETURN_PENSION_INCOME_AMOUNT,
        SPOUSE_RETURN_DISABILITY_AMOUNT,
        SPOUSE_DESIGNATED_TUITION,
        SPOUSE_RETURN_TAXABLE_INCOME,
        SPOUSE_RETURN_FEDERAL_BASIC_TAX,
        SPOUSE_RETURN_BASIC_PERSONAL_AMOUNT,
        SPOUSE_RETURN_LINE_96,
        SPOUSE_RETURN_FEDERAL_TUITION_AMOUNT,
        SPOUSE_TRANSFERABLE_AMOUNTS,
        SPOUSE_INCOME_FOR_TRANSFER,
        SPOUSE_CREDITS_USED,
        SPOUSE_ADJUSTED_TAXABLE_INCOME,
        SPOUSE_UNUSED_AMOUNTS,
        AMOUNTS_TRANSFERRED_FROM_SPOUSE,
    ):
        assert kind.value_type is Decimal, kind.identifier


def test_the_federal_tax_on_split_income_lines_are_non_negative(registry: ArtifactRegistry) -> None:
    # T1 line 120 is 33% of a non-negative amount and line 121 "Line 119 plus line 120 =" adds two
    # non-negative taxes.
    for kind in (FEDERAL_TAX_ON_SPLIT_INCOME, FEDERAL_TAX_WITH_SPLIT_INCOME):
        assert kind.non_negative is True, kind.identifier
        assert registry.kind(kind.identifier) is kind


def test_the_tuition_and_transfer_kinds_are_non_negative(registry: ArtifactRegistry) -> None:
    # Schedule 11 and Schedule 2 take amounts the forms never show below zero: the lines that
    # subtract say "(if negative, enter "0")" or are bounded by the line they come off.
    for kind in (
        CANADIAN_TUITION_FEES,
        CANADA_TRAINING_CREDIT_LIMIT,
        CANADA_TRAINING_CREDIT_CLAIMED,
        FOREIGN_TUITION_FEES,
        UNUSED_TUITION_FROM_2024,
        TUITION_TRANSFER_ELECTED,
        TUITION_TRANSFERRED_FROM_CHILD,
        CANADA_TRAINING_CREDIT_BASIS,
        CANADA_TRAINING_CREDIT_MAXIMUM,
        CANADIAN_TUITION_AVAILABLE,
        CURRENT_YEAR_TUITION_AVAILABLE,
        TOTAL_TUITION_AVAILABLE,
        TUITION_INCOME_BASE,
        TOSI_ADJUSTED_TAXABLE_INCOME,
        TUITION_INCOME_WITH_TOSI,
        CREDIT_AMOUNTS_SUBTOTAL,
        TUITION_INCOME_LESS_CREDITS,
        UNUSED_TUITION_CLAIMED,
        TUITION_INCOME_REMAINING,
        CURRENT_YEAR_TUITION_CLAIMED,
        FEDERAL_TUITION_AMOUNT,
        UNUSED_FEDERAL_TUITION,
        TUITION_TRANSFER_LIMIT,
        TUITION_AVAILABLE_TO_TRANSFER,
        TUITION_TRANSFERRED,
        TUITION_CARRIED_FORWARD,
        SPOUSE_RETURN_AGE_AMOUNT,
        SPOUSE_RETURN_INFIRM_CHILDREN_AMOUNT,
        SPOUSE_RETURN_PENSION_INCOME_AMOUNT,
        SPOUSE_RETURN_DISABILITY_AMOUNT,
        SPOUSE_DESIGNATED_TUITION,
        SPOUSE_RETURN_TAXABLE_INCOME,
        SPOUSE_RETURN_FEDERAL_BASIC_TAX,
        SPOUSE_RETURN_BASIC_PERSONAL_AMOUNT,
        SPOUSE_RETURN_LINE_96,
        SPOUSE_RETURN_FEDERAL_TUITION_AMOUNT,
        SPOUSE_TRANSFERABLE_AMOUNTS,
        SPOUSE_INCOME_FOR_TRANSFER,
        SPOUSE_CREDITS_USED,
        SPOUSE_ADJUSTED_TAXABLE_INCOME,
        SPOUSE_UNUSED_AMOUNTS,
        AMOUNTS_TRANSFERRED_FROM_SPOUSE,
    ):
        assert kind.non_negative is True, kind.identifier
        assert registry.kind(kind.identifier) is kind


def test_the_separation_count_is_a_non_negative_int(registry: ArtifactRegistry) -> None:
    # Schedule 2: "If you were separated because of a breakdown in your relationship for a period
    # of 90 days or more including December 31, 2025, your spouse or common-law partner cannot
    # transfer any unused amounts to you.": a caller's count, 1 when not separated and 0 when
    # separated (to be confirmed on the ticket).
    assert SPOUSE_NOT_SEPARATED_90_DAYS.value_type is int
    assert SPOUSE_NOT_SEPARATED_90_DAYS.non_negative is True
    assert registry.kind("ca/spouse_not_separated_90_days") is SPOUSE_NOT_SEPARATED_90_DAYS


# --- Form T2209 and T1 lines 128 to 130: the federal foreign tax credit ---------------------------


def test_the_federal_foreign_tax_credit_kinds_are_the_registered_ones(
    registry: ArtifactRegistry,
) -> None:
    assert registry.get("ca/first_nations_abatement") is FIRST_NATIONS_ABATEMENT
    assert (
        registry.get("ca/foreign_tax_credit_net_income_deductions")
        is FOREIGN_TAX_CREDIT_NET_INCOME_DEDUCTIONS
    )
    assert (
        registry.get("ca/foreign_tax_credit_net_income_before_split_income")
        is FOREIGN_TAX_CREDIT_NET_INCOME_BEFORE_SPLIT_INCOME
    )
    assert (
        registry.get("ca/foreign_tax_credit_net_income_with_split_income")
        is FOREIGN_TAX_CREDIT_NET_INCOME_WITH_SPLIT_INCOME
    )
    assert registry.get("ca/foreign_tax_credit_net_income") is FOREIGN_TAX_CREDIT_NET_INCOME
    assert (
        registry.get("ca/basic_federal_tax_with_dividend_credit")
        is BASIC_FEDERAL_TAX_WITH_DIVIDEND_CREDIT
    )
    assert (
        registry.get("ca/foreign_tax_credit_basic_federal_tax")
        is FOREIGN_TAX_CREDIT_BASIC_FEDERAL_TAX
    )
    assert (
        registry.get("ca/federal_non_business_foreign_tax_credit")
        is FEDERAL_NON_BUSINESS_FOREIGN_TAX_CREDIT
    )
    assert registry.get("ca/federal_foreign_tax_credit") is FEDERAL_FOREIGN_TAX_CREDIT
    assert (
        registry.get("ca/federal_tax_less_foreign_tax_credit")
        is FEDERAL_TAX_LESS_FOREIGN_TAX_CREDIT
    )


def test_the_federal_foreign_tax_credit_kinds_are_money() -> None:
    for kind in (
        FIRST_NATIONS_ABATEMENT,
        FOREIGN_TAX_CREDIT_NET_INCOME_DEDUCTIONS,
        FOREIGN_TAX_CREDIT_NET_INCOME_BEFORE_SPLIT_INCOME,
        FOREIGN_TAX_CREDIT_NET_INCOME_WITH_SPLIT_INCOME,
        FOREIGN_TAX_CREDIT_NET_INCOME,
        BASIC_FEDERAL_TAX_WITH_DIVIDEND_CREDIT,
        FOREIGN_TAX_CREDIT_BASIC_FEDERAL_TAX,
        FEDERAL_NON_BUSINESS_FOREIGN_TAX_CREDIT,
        FEDERAL_FOREIGN_TAX_CREDIT,
        FEDERAL_TAX_LESS_FOREIGN_TAX_CREDIT,
    ):
        assert kind.value_type is Decimal, kind.identifier


def test_the_foreign_tax_credit_net_income_kinds_are_signed(registry: ArtifactRegistry) -> None:
    # Form T2209 note (3), net income: "Amount from line 23600 of your return (or the amount you
    # would have entered if the instructions said "if negative, show in brackets") plus the amount
    # on line 68360 of Form T1206, Total split income, minus any:" the listed deductions. The
    # note prints no "(if negative, enter "0")", and line 23600 in brackets is signed, so the
    # amount before the split income, the amount with it and the result may each be negative.
    for kind in (
        FOREIGN_TAX_CREDIT_NET_INCOME_BEFORE_SPLIT_INCOME,
        FOREIGN_TAX_CREDIT_NET_INCOME_WITH_SPLIT_INCOME,
        FOREIGN_TAX_CREDIT_NET_INCOME,
    ):
        assert kind.non_negative is False, kind.identifier
        assert registry.kind(kind.identifier) is kind
        assert kind.identifier in SIGNED


def test_the_other_federal_foreign_tax_credit_kinds_are_non_negative(
    registry: ArtifactRegistry,
) -> None:
    # Note (4), basic federal tax: line 42900 plus the federal dividend tax credit, minus the
    # First Nations abatement; line 3 is the lesser of two non-negative amounts, line 13 "should
    # not be more than" line 42900, and T1 line 130 comes off line 128 within the limit.
    for kind in (
        FIRST_NATIONS_ABATEMENT,
        FOREIGN_TAX_CREDIT_NET_INCOME_DEDUCTIONS,
        BASIC_FEDERAL_TAX_WITH_DIVIDEND_CREDIT,
        FOREIGN_TAX_CREDIT_BASIC_FEDERAL_TAX,
        FEDERAL_NON_BUSINESS_FOREIGN_TAX_CREDIT,
        FEDERAL_FOREIGN_TAX_CREDIT,
        FEDERAL_TAX_LESS_FOREIGN_TAX_CREDIT,
    ):
        assert kind.non_negative is True, kind.identifier
        assert registry.kind(kind.identifier) is kind
