"""Registered and money kinds of the federal catalog family `income`."""

from __future__ import annotations

from decimal import Decimal
from typing import Any

import pytest

from app.domain.artifact import ArtifactKind, ArtifactRegistry
from app.domain.record_list import RecordList, RecordListKind
from app.jurisdictions.ca.catalog import (
    BOND_DISPOSITIONS,
    BOND_GAIN_OR_LOSS,
    BOND_PROCEEDS,
    BUSINESS_EPOP_AGREEMENT_FILED,
    BUSINESS_EPOP_AGREEMENT_FILED_CHECKED,
    BUSINESS_EPOP_ASSOCIATED,
    BUSINESS_EPOP_ASSOCIATED_CHECKED,
    BUSINESS_EPOP_PERCENTAGE,
    BUSINESS_EPOP_PERCENTAGE_CHECKED,
    BUSINESS_EPOP_PERCENTAGE_MAXIMUM,
    BUSINESS_EPOP_PERCENTAGE_ROOM,
    BUSINESS_EPOP_PERCENTAGE_TOTAL,
    BUSINESS_FISCAL_PERIOD_DAYS,
    BUSINESS_FISCAL_PERIOD_DAYS_ENTERED,
    BUSINESS_IMMEDIATE_EXPENSING_ALLOCATED,
    BUSINESS_IMMEDIATE_EXPENSING_ASSOCIATED_LIMIT,
    BUSINESS_IMMEDIATE_EXPENSING_CAP,
    BUSINESS_IMMEDIATE_EXPENSING_CLAIM,
    BUSINESS_IMMEDIATE_EXPENSING_LIMIT,
    BUSINESS_IMMEDIATE_EXPENSING_LIMIT_BEFORE_MINISTER,
    BUSINESS_IMMEDIATE_EXPENSING_SHARE,
    BUSINESS_INCOME,
    BUSINESS_INCOME_BEFORE_CCA,
    BUSINESS_MINISTER_ALLOCATION,
    BUSINESS_MINISTER_ALLOCATION_GIVEN,
    BUSINESS_MINISTER_ALLOCATION_GIVEN_CHECKED,
    BUSINESS_VEHICLE_DAYS_DIVISOR,
    BUSINESS_VEHICLE_LIST_PRICE,
    BUSINESS_VEHICLE_SALES_TAX_RATE,
    BUSINESS_VEHICLES,
    CAPITAL_GAIN,
    CAPITAL_GAINS_AFTER_DEFERRAL,
    CAPITAL_GAINS_BEFORE_INVESTMENT_LOSS_REDUCTION,
    CAPITAL_GAINS_BEFORE_RESERVES,
    CAPITAL_GAINS_DEFERRAL,
    CAPITAL_GAINS_OF_QUALIFIED_AND_OTHER_PROPERTIES,
    CAPITAL_GAINS_RESERVES,
    COMMISSION_INCOME,
    CPP_OR_QPP_BENEFITS,
    CREDITS_AGAINST_BASIC_FEDERAL_TAX,
    CRYPTO_ASSET_DISPOSITIONS,
    CRYPTO_ASSET_GAIN_OR_LOSS,
    CRYPTO_ASSET_PROCEEDS,
    DISPOSITION_ADJUSTED_COST_BASE,
    DISPOSITION_OUTLAYS,
    DISPOSITION_PROCEEDS,
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
    FARM_EPOP_AGREEMENT_FILED,
    FARM_EPOP_AGREEMENT_FILED_CHECKED,
    FARM_EPOP_ASSOCIATED,
    FARM_EPOP_ASSOCIATED_CHECKED,
    FARM_EPOP_PERCENTAGE,
    FARM_EPOP_PERCENTAGE_CHECKED,
    FARM_EPOP_PERCENTAGE_MAXIMUM,
    FARM_EPOP_PERCENTAGE_ROOM,
    FARM_EPOP_PERCENTAGE_TOTAL,
    FARM_FISCAL_PERIOD_DAYS,
    FARM_FISCAL_PERIOD_DAYS_ENTERED,
    FARM_IMMEDIATE_EXPENSING_ALLOCATED,
    FARM_IMMEDIATE_EXPENSING_ASSOCIATED_LIMIT,
    FARM_IMMEDIATE_EXPENSING_CAP,
    FARM_IMMEDIATE_EXPENSING_CLAIM,
    FARM_IMMEDIATE_EXPENSING_LIMIT,
    FARM_IMMEDIATE_EXPENSING_LIMIT_BEFORE_MINISTER,
    FARM_IMMEDIATE_EXPENSING_SHARE,
    FARM_INCOME_BEFORE_CCA,
    FARM_MINISTER_ALLOCATION,
    FARM_MINISTER_ALLOCATION_GIVEN,
    FARM_MINISTER_ALLOCATION_GIVEN_CHECKED,
    FARM_MOTOR_VEHICLE_EXPENSES,
    FARM_VEHICLE_SALES_TAX_RATE,
    FARMING_INCOME,
    FHSA_INCOME,
    FISH_EPOP_AGREEMENT_FILED,
    FISH_EPOP_AGREEMENT_FILED_CHECKED,
    FISH_EPOP_ASSOCIATED,
    FISH_EPOP_ASSOCIATED_CHECKED,
    FISH_EPOP_PERCENTAGE,
    FISH_EPOP_PERCENTAGE_CHECKED,
    FISH_EPOP_PERCENTAGE_MAXIMUM,
    FISH_EPOP_PERCENTAGE_ROOM,
    FISH_EPOP_PERCENTAGE_TOTAL,
    FISH_FISCAL_PERIOD_DAYS,
    FISH_FISCAL_PERIOD_DAYS_ENTERED,
    FISH_IMMEDIATE_EXPENSING_ALLOCATED,
    FISH_IMMEDIATE_EXPENSING_ASSOCIATED_LIMIT,
    FISH_IMMEDIATE_EXPENSING_CAP,
    FISH_IMMEDIATE_EXPENSING_CLAIM,
    FISH_IMMEDIATE_EXPENSING_LIMIT,
    FISH_IMMEDIATE_EXPENSING_LIMIT_BEFORE_MINISTER,
    FISH_IMMEDIATE_EXPENSING_SHARE,
    FISH_INCOME_BEFORE_CCA,
    FISH_MINISTER_ALLOCATION,
    FISH_MINISTER_ALLOCATION_GIVEN,
    FISH_MINISTER_ALLOCATION_GIVEN_CHECKED,
    FISH_MOTOR_VEHICLE_EXPENSES,
    FISH_VEHICLE_SALES_TAX_RATE,
    FISHING_INCOME,
    FOREIGN_INVESTMENT_INCOME,
    GROSS_RENTAL_INCOME,
    INCLUDED_CAPITAL_GAIN,
    INCOME_SUPPORT_BENEFITS,
    INTEREST_AND_OTHER_INVESTMENT_INCOME,
    INVESTMENT_INCOME_BEFORE_PRIOR_YEARS,
    INVESTMENT_INCOME_CREDITED_NOT_RECEIVED,
    INVESTMENT_INCOME_REPORTED_IN_PREVIOUS_YEARS,
    INVESTMENT_INCOME_WITHOUT_A_SLIP,
    INVESTMENT_ROYALTIES,
    LISTED_PERSONAL_PROPERTY_DISPOSITIONS,
    LISTED_PERSONAL_PROPERTY_GAIN_OR_LOSS,
    LISTED_PERSONAL_PROPERTY_NET_GAIN,
    NET_FEDERAL_SUPPLEMENTS,
    NET_PARTNERSHIP_INCOME,
    NET_RENTAL_INCOME,
    NET_SELF_EMPLOYMENT_INCOME,
    NO_SLIP_DIVIDEND_TAX_CREDIT,
    NON_COMPLIANT_CCA,
    OLD_AGE_SECURITY,
    OTHER_DIVIDENDS_CREDIT,
    OTHER_DIVIDENDS_GROSSED_UP,
    OTHER_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP,
    OTHER_EMPLOYMENT_INCOME,
    OTHER_FHSA_INCOME,
    OTHER_FORECLOSURE_DISPOSITIONS,
    OTHER_FORECLOSURE_GAIN_OR_LOSS,
    OTHER_FORECLOSURE_PROCEEDS,
    OTHER_INCOME,
    OTHER_PENSIONS_AND_SUPERANNUATION,
    PARTNERSHIP_GAINS_AT_FULL_INCLUSION,
    PERSONAL_USE_PROPERTY_DISPOSITIONS,
    PERSONAL_USE_PROPERTY_GAIN,
    PERSONAL_USE_PROPERTY_GAIN_ROWS,
    PROFESSIONAL_INCOME,
    QFFP_DISPOSITIONS,
    QFFP_FORECLOSURE_DISPOSITIONS,
    QFFP_FORECLOSURE_GAIN_OR_LOSS,
    QFFP_FORECLOSURE_PROCEEDS,
    QFFP_GAIN_OR_LOSS,
    QFFP_PROCEEDS,
    QSBCS_DISPOSITIONS,
    QSBCS_GAIN_OR_LOSS,
    QSBCS_PROCEEDS,
    RDSP_INCOME,
    REAL_ESTATE_DISPOSITIONS,
    REAL_ESTATE_GAIN_OR_LOSS,
    REAL_ESTATE_PROCEEDS,
    RENTAL_ADVERTISING,
    RENTAL_ADVERTISING_PERSONAL_PORTION,
    RENTAL_ADVERTISING_SHORT_TERM_PORTION,
    RENTAL_CCA_BUSINESS_USE_OF_HOME,
    RENTAL_CCA_CLAIM,
    RENTAL_CCA_CLAIM_BEFORE_LIMIT,
    RENTAL_CCA_CLAIM_LESS_PERSONAL_PART,
    RENTAL_CCA_CLAIM_SHARE,
    RENTAL_CCA_CLASSES,
    RENTAL_CCA_LIMIT,
    RENTAL_CCA_PERSONAL_PART,
    RENTAL_CCA_TABLE_CLAIM,
    RENTAL_CCA_TABLE_RECAPTURE,
    RENTAL_CCA_TABLE_TERMINAL_LOSS,
    RENTAL_CLOSING_UCC,
    RENTAL_COOWNER,
    RENTAL_COOWNER_CCA_CLAIM,
    RENTAL_COOWNER_OTHER_EXPENSES,
    RENTAL_COOWNER_RECAPTURED_CCA,
    RENTAL_COOWNER_SHARE,
    RENTAL_COOWNER_TERMINAL_LOSS,
    RENTAL_DEDUCTIBLE_EXPENSES,
    RENTAL_EPOP_AGREEMENT_FILED,
    RENTAL_EPOP_AGREEMENT_FILED_CHECKED,
    RENTAL_EPOP_ASSOCIATED,
    RENTAL_EPOP_ASSOCIATED_CHECKED,
    RENTAL_EPOP_PERCENTAGE,
    RENTAL_EPOP_PERCENTAGE_CHECKED,
    RENTAL_EPOP_PERCENTAGE_MAXIMUM,
    RENTAL_EPOP_PERCENTAGE_ROOM,
    RENTAL_EPOP_PERCENTAGE_TOTAL,
    RENTAL_EXPENSES_LESS_PERSONAL_PORTION,
    RENTAL_FISCAL_PERIOD_DAYS,
    RENTAL_FISCAL_PERIOD_DAYS_ENTERED,
    RENTAL_GROSS_RENTS,
    RENTAL_IMMEDIATE_EXPENSING_ALLOCATED,
    RENTAL_IMMEDIATE_EXPENSING_ASSOCIATED_LIMIT,
    RENTAL_IMMEDIATE_EXPENSING_CAP,
    RENTAL_IMMEDIATE_EXPENSING_CLAIM,
    RENTAL_IMMEDIATE_EXPENSING_LIMIT,
    RENTAL_IMMEDIATE_EXPENSING_LIMIT_BEFORE_MINISTER,
    RENTAL_IMMEDIATE_EXPENSING_SHARE,
    RENTAL_INSURANCE,
    RENTAL_INSURANCE_PERSONAL_PORTION,
    RENTAL_INSURANCE_SHORT_TERM_PORTION,
    RENTAL_INTEREST_AND_BANK_CHARGES,
    RENTAL_INTEREST_AND_BANK_CHARGES_PERSONAL_PORTION,
    RENTAL_INTEREST_AND_BANK_CHARGES_SHORT_TERM_PORTION,
    RENTAL_MANAGEMENT_AND_ADMINISTRATION_FEES,
    RENTAL_MANAGEMENT_AND_ADMINISTRATION_FEES_PERSONAL_PORTION,
    RENTAL_MANAGEMENT_AND_ADMINISTRATION_FEES_SHORT_TERM_PORTION,
    RENTAL_MINISTER_ALLOCATION,
    RENTAL_MINISTER_ALLOCATION_GIVEN,
    RENTAL_MINISTER_ALLOCATION_GIVEN_CHECKED,
    RENTAL_MOTOR_VEHICLE_EXPENSES,
    RENTAL_MOTOR_VEHICLE_EXPENSES_PERSONAL_PORTION,
    RENTAL_MOTOR_VEHICLE_EXPENSES_SHORT_TERM_PORTION,
    RENTAL_NET_INCOME_AFTER_CCA,
    RENTAL_NET_INCOME_AFTER_COOWNER_EXPENSES,
    RENTAL_NET_INCOME_AFTER_TERMINAL_LOSS,
    RENTAL_NET_INCOME_BEFORE_ADJUSTMENTS,
    RENTAL_NET_INCOME_SHARE,
    RENTAL_NET_INCOME_WITH_RECAPTURE,
    RENTAL_NON_COMPLIANT_CCA,
    RENTAL_NON_COMPLIANT_EXPENSES,
    RENTAL_OFFICE_EXPENSES,
    RENTAL_OFFICE_EXPENSES_PERSONAL_PORTION,
    RENTAL_OFFICE_EXPENSES_SHORT_TERM_PORTION,
    RENTAL_OTHER_EXPENSES,
    RENTAL_OTHER_EXPENSES_PERSONAL_PORTION,
    RENTAL_OTHER_EXPENSES_SHORT_TERM_PORTION,
    RENTAL_OTHER_INCOME,
    RENTAL_PARTNER,
    RENTAL_PARTNER_GST_HST_REBATE,
    RENTAL_PARTNER_OTHER_EXPENSES,
    RENTAL_PARTNER_SHARE,
    RENTAL_PARTNER_SHARE_WITH_REBATE,
    RENTAL_PARTNERSHIP_NET_INCOME,
    RENTAL_PERSONAL_PORTION,
    RENTAL_PROFESSIONAL_FEES,
    RENTAL_PROFESSIONAL_FEES_PERSONAL_PORTION,
    RENTAL_PROFESSIONAL_FEES_SHORT_TERM_PORTION,
    RENTAL_PROPERTIES,
    RENTAL_PROPERTY_GROSS_RENTS,
    RENTAL_PROPERTY_SHORT_TERM_RENTS,
    RENTAL_PROPERTY_TAXES,
    RENTAL_PROPERTY_TAXES_PERSONAL_PORTION,
    RENTAL_PROPERTY_TAXES_SHORT_TERM_PORTION,
    RENTAL_PROPERTY_UNITS,
    RENTAL_RECAPTURED_CCA,
    RENTAL_REPAIRS_AND_MAINTENANCE,
    RENTAL_REPAIRS_AND_MAINTENANCE_PERSONAL_PORTION,
    RENTAL_REPAIRS_AND_MAINTENANCE_SHORT_TERM_PORTION,
    RENTAL_SALARIES_WAGES_AND_BENEFITS,
    RENTAL_SALARIES_WAGES_AND_BENEFITS_PERSONAL_PORTION,
    RENTAL_SALARIES_WAGES_AND_BENEFITS_SHORT_TERM_PORTION,
    RENTAL_SHORT_TERM_PORTION,
    RENTAL_TERMINAL_LOSS,
    RENTAL_TOTAL_EXPENSES,
    RENTAL_TRAVEL,
    RENTAL_TRAVEL_PERSONAL_PORTION,
    RENTAL_TRAVEL_SHORT_TERM_PORTION,
    RENTAL_UTILITIES,
    RENTAL_UTILITIES_PERSONAL_PORTION,
    RENTAL_UTILITIES_SHORT_TERM_PORTION,
    RRSP_INCOME,
    SHARE_DISPOSITIONS,
    SHARE_GAIN_OR_LOSS,
    SHARE_PROCEEDS,
    SHORT_TERM_RENTAL_CCA_UNITS,
    SHORT_TERM_RENTAL_DAYS,
    SHORT_TERM_RENTAL_GROSS_RENTS,
    SHORT_TERM_RENTAL_NON_COMPLIANT_CCA_BY_CLASS,
    SHORT_TERM_RENTAL_NON_COMPLIANT_DAYS,
    SHORT_TERM_RENTAL_RELATED_CCA,
    SHORT_TERM_RENTAL_RELATED_EXPENSES,
    SHORT_TERM_RENTAL_UNITS,
    SLIP_CAPITAL_GAINS_OR_LOSSES,
    SLIP_DIVIDEND_TAX_CREDIT,
    SLIP_TAXABLE_DIVIDENDS,
    SLIP_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
    SOCIAL_ASSISTANCE_PAYMENTS,
    T3_CAPITAL_GAINS_OR_LOSSES,
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
    T776_STATEMENTS,
    T2042_STATEMENTS,
    T2121_STATEMENTS,
    T2125_STATEMENTS,
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
    UNAPPLIED_LISTED_PERSONAL_PROPERTY_LOSSES,
    UNIVERSAL_CHILD_CARE_BENEFIT,
    WORKERS_COMPENSATION_BENEFITS,
)
from tests.jurisdictions.ca.catalog_snapshot import (
    RECORD_LISTS,
    REGISTERED,
    SIGNED,
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
    assert registry.get("ca/business_income") is BUSINESS_INCOME
    assert registry.get("ca/business_epop_associated") is BUSINESS_EPOP_ASSOCIATED
    assert registry.get("ca/business_epop_agreement_filed") is BUSINESS_EPOP_AGREEMENT_FILED
    assert registry.get("ca/business_epop_percentage") is BUSINESS_EPOP_PERCENTAGE
    assert registry.get("ca/business_epop_percentage_total") is BUSINESS_EPOP_PERCENTAGE_TOTAL
    assert (
        registry.get("ca/business_minister_allocation_given") is BUSINESS_MINISTER_ALLOCATION_GIVEN
    )
    assert registry.get("ca/business_minister_allocation") is BUSINESS_MINISTER_ALLOCATION
    assert registry.get("ca/business_immediate_expensing_cap") is BUSINESS_IMMEDIATE_EXPENSING_CAP
    assert registry.get("ca/business_epop_percentage_maximum") is BUSINESS_EPOP_PERCENTAGE_MAXIMUM
    assert (
        registry.get("ca/business_immediate_expensing_share") is BUSINESS_IMMEDIATE_EXPENSING_SHARE
    )
    assert registry.get("ca/business_epop_percentage_room") is BUSINESS_EPOP_PERCENTAGE_ROOM
    assert (
        registry.get("ca/business_immediate_expensing_allocated")
        is BUSINESS_IMMEDIATE_EXPENSING_ALLOCATED
    )
    assert (
        registry.get("ca/business_immediate_expensing_associated_limit")
        is BUSINESS_IMMEDIATE_EXPENSING_ASSOCIATED_LIMIT
    )
    assert (
        registry.get("ca/business_immediate_expensing_limit_before_minister")
        is BUSINESS_IMMEDIATE_EXPENSING_LIMIT_BEFORE_MINISTER
    )
    assert (
        registry.get("ca/business_immediate_expensing_limit") is BUSINESS_IMMEDIATE_EXPENSING_LIMIT
    )
    assert (
        registry.get("ca/business_immediate_expensing_claim") is BUSINESS_IMMEDIATE_EXPENSING_CLAIM
    )
    assert registry.get("ca/business_income_before_cca") is BUSINESS_INCOME_BEFORE_CCA
    assert (
        registry.get("ca/business_fiscal_period_days_entered")
        is BUSINESS_FISCAL_PERIOD_DAYS_ENTERED
    )
    assert registry.get("ca/business_fiscal_period_days") is BUSINESS_FISCAL_PERIOD_DAYS
    assert registry.get("ca/farm_fiscal_period_days_entered") is FARM_FISCAL_PERIOD_DAYS_ENTERED
    assert registry.get("ca/farm_fiscal_period_days") is FARM_FISCAL_PERIOD_DAYS
    assert registry.get("ca/fish_fiscal_period_days_entered") is FISH_FISCAL_PERIOD_DAYS_ENTERED
    assert registry.get("ca/fish_fiscal_period_days") is FISH_FISCAL_PERIOD_DAYS
    assert registry.get("ca/professional_income") is PROFESSIONAL_INCOME
    assert registry.get("ca/commission_income") is COMMISSION_INCOME
    assert registry.get("ca/farming_income") is FARMING_INCOME
    assert registry.get("ca/farm_epop_associated") is FARM_EPOP_ASSOCIATED
    assert registry.get("ca/farm_epop_agreement_filed") is FARM_EPOP_AGREEMENT_FILED
    assert registry.get("ca/farm_epop_percentage") is FARM_EPOP_PERCENTAGE
    assert registry.get("ca/farm_epop_percentage_total") is FARM_EPOP_PERCENTAGE_TOTAL
    assert registry.get("ca/farm_minister_allocation_given") is FARM_MINISTER_ALLOCATION_GIVEN
    assert registry.get("ca/farm_minister_allocation") is FARM_MINISTER_ALLOCATION
    assert registry.get("ca/farm_immediate_expensing_cap") is FARM_IMMEDIATE_EXPENSING_CAP
    assert registry.get("ca/farm_epop_percentage_maximum") is FARM_EPOP_PERCENTAGE_MAXIMUM
    assert registry.get("ca/farm_immediate_expensing_share") is FARM_IMMEDIATE_EXPENSING_SHARE
    assert registry.get("ca/farm_epop_percentage_room") is FARM_EPOP_PERCENTAGE_ROOM
    assert (
        registry.get("ca/farm_immediate_expensing_allocated") is FARM_IMMEDIATE_EXPENSING_ALLOCATED
    )
    assert (
        registry.get("ca/farm_immediate_expensing_associated_limit")
        is FARM_IMMEDIATE_EXPENSING_ASSOCIATED_LIMIT
    )
    assert (
        registry.get("ca/farm_immediate_expensing_limit_before_minister")
        is FARM_IMMEDIATE_EXPENSING_LIMIT_BEFORE_MINISTER
    )
    assert registry.get("ca/farm_immediate_expensing_limit") is FARM_IMMEDIATE_EXPENSING_LIMIT
    assert registry.get("ca/farm_immediate_expensing_claim") is FARM_IMMEDIATE_EXPENSING_CLAIM
    assert registry.get("ca/farm_income_before_cca") is FARM_INCOME_BEFORE_CCA
    assert registry.get("ca/fish_epop_associated") is FISH_EPOP_ASSOCIATED
    assert registry.get("ca/fish_epop_agreement_filed") is FISH_EPOP_AGREEMENT_FILED
    assert registry.get("ca/fish_epop_percentage") is FISH_EPOP_PERCENTAGE
    assert registry.get("ca/fish_epop_percentage_total") is FISH_EPOP_PERCENTAGE_TOTAL
    assert registry.get("ca/fish_minister_allocation_given") is FISH_MINISTER_ALLOCATION_GIVEN
    assert registry.get("ca/fish_minister_allocation") is FISH_MINISTER_ALLOCATION
    assert registry.get("ca/fish_immediate_expensing_cap") is FISH_IMMEDIATE_EXPENSING_CAP
    assert registry.get("ca/fish_epop_percentage_maximum") is FISH_EPOP_PERCENTAGE_MAXIMUM
    assert registry.get("ca/fish_immediate_expensing_share") is FISH_IMMEDIATE_EXPENSING_SHARE
    assert registry.get("ca/fish_epop_percentage_room") is FISH_EPOP_PERCENTAGE_ROOM
    assert (
        registry.get("ca/fish_immediate_expensing_allocated") is FISH_IMMEDIATE_EXPENSING_ALLOCATED
    )
    assert (
        registry.get("ca/fish_immediate_expensing_associated_limit")
        is FISH_IMMEDIATE_EXPENSING_ASSOCIATED_LIMIT
    )
    assert (
        registry.get("ca/fish_immediate_expensing_limit_before_minister")
        is FISH_IMMEDIATE_EXPENSING_LIMIT_BEFORE_MINISTER
    )
    assert registry.get("ca/fish_immediate_expensing_limit") is FISH_IMMEDIATE_EXPENSING_LIMIT
    assert registry.get("ca/fish_immediate_expensing_claim") is FISH_IMMEDIATE_EXPENSING_CLAIM
    assert registry.get("ca/fish_income_before_cca") is FISH_INCOME_BEFORE_CCA
    assert registry.get("ca/fishing_income") is FISHING_INCOME
    assert registry.get("ca/workers_compensation_benefits") is WORKERS_COMPENSATION_BENEFITS
    assert registry.get("ca/social_assistance_payments") is SOCIAL_ASSISTANCE_PAYMENTS
    assert registry.get("ca/net_federal_supplements") is NET_FEDERAL_SUPPLEMENTS
    assert registry.get("ca/income_support_benefits") is INCOME_SUPPORT_BENEFITS
    assert registry.get("ca/net_self_employment_income") is NET_SELF_EMPLOYMENT_INCOME
    assert (
        registry.get("ca/short_term_rental_related_expenses") is SHORT_TERM_RENTAL_RELATED_EXPENSES
    )
    assert (
        registry.get("ca/short_term_rental_non_compliant_days")
        is SHORT_TERM_RENTAL_NON_COMPLIANT_DAYS
    )
    assert registry.get("ca/short_term_rental_days") is SHORT_TERM_RENTAL_DAYS
    assert registry.get("ca/short_term_rental_units") is SHORT_TERM_RENTAL_UNITS
    assert registry.get("ca/short_term_rental_related_cca") is SHORT_TERM_RENTAL_RELATED_CCA
    assert registry.get("ca/short_term_rental_cca_units") is SHORT_TERM_RENTAL_CCA_UNITS
    assert registry.get("ca/non_compliant_cca") is NON_COMPLIANT_CCA
    assert (
        registry.get("ca/short_term_rental_non_compliant_cca_by_class")
        is SHORT_TERM_RENTAL_NON_COMPLIANT_CCA_BY_CLASS
    )
    assert registry.get("ca/rental_property_units") is RENTAL_PROPERTY_UNITS
    assert registry.get("ca/rental_property_short_term_rents") is RENTAL_PROPERTY_SHORT_TERM_RENTS
    assert registry.get("ca/rental_property_gross_rents") is RENTAL_PROPERTY_GROSS_RENTS
    assert registry.get("ca/rental_properties") is RENTAL_PROPERTIES
    assert registry.get("ca/short_term_rental_gross_rents") is SHORT_TERM_RENTAL_GROSS_RENTS
    assert registry.get("ca/rental_gross_rents") is RENTAL_GROSS_RENTS
    assert registry.get("ca/rental_other_income") is RENTAL_OTHER_INCOME
    assert registry.get("ca/gross_rental_income") is GROSS_RENTAL_INCOME
    assert registry.get("ca/rental_advertising") is RENTAL_ADVERTISING
    assert (
        registry.get("ca/rental_advertising_personal_portion")
        is RENTAL_ADVERTISING_PERSONAL_PORTION
    )
    assert (
        registry.get("ca/rental_advertising_short_term_portion")
        is RENTAL_ADVERTISING_SHORT_TERM_PORTION
    )
    assert registry.get("ca/rental_insurance") is RENTAL_INSURANCE
    assert registry.get("ca/rental_insurance_personal_portion") is RENTAL_INSURANCE_PERSONAL_PORTION
    assert (
        registry.get("ca/rental_insurance_short_term_portion")
        is RENTAL_INSURANCE_SHORT_TERM_PORTION
    )
    assert registry.get("ca/rental_interest_and_bank_charges") is RENTAL_INTEREST_AND_BANK_CHARGES
    assert (
        registry.get("ca/rental_interest_and_bank_charges_personal_portion")
        is RENTAL_INTEREST_AND_BANK_CHARGES_PERSONAL_PORTION
    )
    assert (
        registry.get("ca/rental_interest_and_bank_charges_short_term_portion")
        is RENTAL_INTEREST_AND_BANK_CHARGES_SHORT_TERM_PORTION
    )
    assert registry.get("ca/rental_office_expenses") is RENTAL_OFFICE_EXPENSES
    assert (
        registry.get("ca/rental_office_expenses_personal_portion")
        is RENTAL_OFFICE_EXPENSES_PERSONAL_PORTION
    )
    assert (
        registry.get("ca/rental_office_expenses_short_term_portion")
        is RENTAL_OFFICE_EXPENSES_SHORT_TERM_PORTION
    )
    assert registry.get("ca/rental_professional_fees") is RENTAL_PROFESSIONAL_FEES
    assert (
        registry.get("ca/rental_professional_fees_personal_portion")
        is RENTAL_PROFESSIONAL_FEES_PERSONAL_PORTION
    )
    assert (
        registry.get("ca/rental_professional_fees_short_term_portion")
        is RENTAL_PROFESSIONAL_FEES_SHORT_TERM_PORTION
    )
    assert (
        registry.get("ca/rental_management_and_administration_fees")
        is RENTAL_MANAGEMENT_AND_ADMINISTRATION_FEES
    )
    assert (
        registry.get("ca/rental_management_and_administration_fees_personal_portion")
        is RENTAL_MANAGEMENT_AND_ADMINISTRATION_FEES_PERSONAL_PORTION
    )
    assert (
        registry.get("ca/rental_management_and_administration_fees_short_term_portion")
        is RENTAL_MANAGEMENT_AND_ADMINISTRATION_FEES_SHORT_TERM_PORTION
    )
    assert registry.get("ca/rental_repairs_and_maintenance") is RENTAL_REPAIRS_AND_MAINTENANCE
    assert (
        registry.get("ca/rental_repairs_and_maintenance_personal_portion")
        is RENTAL_REPAIRS_AND_MAINTENANCE_PERSONAL_PORTION
    )
    assert (
        registry.get("ca/rental_repairs_and_maintenance_short_term_portion")
        is RENTAL_REPAIRS_AND_MAINTENANCE_SHORT_TERM_PORTION
    )
    assert (
        registry.get("ca/rental_salaries_wages_and_benefits") is RENTAL_SALARIES_WAGES_AND_BENEFITS
    )
    assert (
        registry.get("ca/rental_salaries_wages_and_benefits_personal_portion")
        is RENTAL_SALARIES_WAGES_AND_BENEFITS_PERSONAL_PORTION
    )
    assert (
        registry.get("ca/rental_salaries_wages_and_benefits_short_term_portion")
        is RENTAL_SALARIES_WAGES_AND_BENEFITS_SHORT_TERM_PORTION
    )
    assert registry.get("ca/rental_property_taxes") is RENTAL_PROPERTY_TAXES
    assert (
        registry.get("ca/rental_property_taxes_personal_portion")
        is RENTAL_PROPERTY_TAXES_PERSONAL_PORTION
    )
    assert (
        registry.get("ca/rental_property_taxes_short_term_portion")
        is RENTAL_PROPERTY_TAXES_SHORT_TERM_PORTION
    )
    assert registry.get("ca/rental_travel") is RENTAL_TRAVEL
    assert registry.get("ca/rental_travel_personal_portion") is RENTAL_TRAVEL_PERSONAL_PORTION
    assert registry.get("ca/rental_travel_short_term_portion") is RENTAL_TRAVEL_SHORT_TERM_PORTION
    assert registry.get("ca/rental_utilities") is RENTAL_UTILITIES
    assert registry.get("ca/rental_utilities_personal_portion") is RENTAL_UTILITIES_PERSONAL_PORTION
    assert (
        registry.get("ca/rental_utilities_short_term_portion")
        is RENTAL_UTILITIES_SHORT_TERM_PORTION
    )
    assert registry.get("ca/rental_motor_vehicle_expenses") is RENTAL_MOTOR_VEHICLE_EXPENSES
    assert (
        registry.get("ca/rental_motor_vehicle_expenses_personal_portion")
        is RENTAL_MOTOR_VEHICLE_EXPENSES_PERSONAL_PORTION
    )
    assert (
        registry.get("ca/rental_motor_vehicle_expenses_short_term_portion")
        is RENTAL_MOTOR_VEHICLE_EXPENSES_SHORT_TERM_PORTION
    )
    assert registry.get("ca/rental_other_expenses") is RENTAL_OTHER_EXPENSES
    assert (
        registry.get("ca/rental_other_expenses_personal_portion")
        is RENTAL_OTHER_EXPENSES_PERSONAL_PORTION
    )
    assert (
        registry.get("ca/rental_other_expenses_short_term_portion")
        is RENTAL_OTHER_EXPENSES_SHORT_TERM_PORTION
    )
    assert registry.get("ca/rental_total_expenses") is RENTAL_TOTAL_EXPENSES
    assert registry.get("ca/rental_personal_portion") is RENTAL_PERSONAL_PORTION
    assert registry.get("ca/rental_short_term_portion") is RENTAL_SHORT_TERM_PORTION
    assert registry.get("ca/rental_non_compliant_expenses") is RENTAL_NON_COMPLIANT_EXPENSES
    assert registry.get("ca/rental_non_compliant_cca") is RENTAL_NON_COMPLIANT_CCA
    assert (
        registry.get("ca/rental_expenses_less_personal_portion")
        is RENTAL_EXPENSES_LESS_PERSONAL_PORTION
    )
    assert registry.get("ca/rental_deductible_expenses") is RENTAL_DEDUCTIBLE_EXPENSES
    assert (
        registry.get("ca/rental_net_income_before_adjustments")
        is RENTAL_NET_INCOME_BEFORE_ADJUSTMENTS
    )
    assert registry.get("ca/rental_coowner") is RENTAL_COOWNER
    assert registry.get("ca/rental_coowner_share") is RENTAL_COOWNER_SHARE
    assert registry.get("ca/rental_net_income_share") is RENTAL_NET_INCOME_SHARE
    assert registry.get("ca/rental_coowner_other_expenses") is RENTAL_COOWNER_OTHER_EXPENSES
    assert (
        registry.get("ca/rental_net_income_after_coowner_expenses")
        is RENTAL_NET_INCOME_AFTER_COOWNER_EXPENSES
    )
    assert registry.get("ca/rental_recaptured_cca") is RENTAL_RECAPTURED_CCA
    assert registry.get("ca/rental_net_income_with_recapture") is RENTAL_NET_INCOME_WITH_RECAPTURE
    assert registry.get("ca/rental_terminal_loss") is RENTAL_TERMINAL_LOSS
    assert (
        registry.get("ca/rental_net_income_after_terminal_loss")
        is RENTAL_NET_INCOME_AFTER_TERMINAL_LOSS
    )
    assert registry.get("ca/rental_cca_claim") is RENTAL_CCA_CLAIM
    assert registry.get("ca/rental_cca_classes") is RENTAL_CCA_CLASSES
    assert registry.get("ca/rental_cca_table_recapture") is RENTAL_CCA_TABLE_RECAPTURE
    assert registry.get("ca/rental_cca_table_terminal_loss") is RENTAL_CCA_TABLE_TERMINAL_LOSS
    assert registry.get("ca/rental_cca_table_claim") is RENTAL_CCA_TABLE_CLAIM
    assert registry.get("ca/rental_coowner_recaptured_cca") is RENTAL_COOWNER_RECAPTURED_CCA
    assert registry.get("ca/rental_coowner_terminal_loss") is RENTAL_COOWNER_TERMINAL_LOSS
    assert registry.get("ca/rental_coowner_cca_claim") is RENTAL_COOWNER_CCA_CLAIM
    assert registry.get("ca/rental_cca_claim_share") is RENTAL_CCA_CLAIM_SHARE
    assert registry.get("ca/rental_cca_personal_part") is RENTAL_CCA_PERSONAL_PART
    assert registry.get("ca/rental_cca_business_use_of_home") is RENTAL_CCA_BUSINESS_USE_OF_HOME
    assert (
        registry.get("ca/rental_cca_claim_less_personal_part")
        is RENTAL_CCA_CLAIM_LESS_PERSONAL_PART
    )
    assert registry.get("ca/rental_cca_claim_before_limit") is RENTAL_CCA_CLAIM_BEFORE_LIMIT
    assert registry.get("ca/rental_cca_limit") is RENTAL_CCA_LIMIT
    assert registry.get("ca/rental_closing_ucc") is RENTAL_CLOSING_UCC
    assert registry.get("ca/rental_net_income_after_cca") is RENTAL_NET_INCOME_AFTER_CCA
    assert registry.get("ca/rental_epop_associated") is RENTAL_EPOP_ASSOCIATED
    assert registry.get("ca/rental_epop_agreement_filed") is RENTAL_EPOP_AGREEMENT_FILED
    assert registry.get("ca/rental_epop_percentage") is RENTAL_EPOP_PERCENTAGE
    assert registry.get("ca/rental_epop_percentage_total") is RENTAL_EPOP_PERCENTAGE_TOTAL
    assert registry.get("ca/rental_minister_allocation_given") is RENTAL_MINISTER_ALLOCATION_GIVEN
    assert registry.get("ca/rental_minister_allocation") is RENTAL_MINISTER_ALLOCATION
    assert registry.get("ca/rental_immediate_expensing_cap") is RENTAL_IMMEDIATE_EXPENSING_CAP
    assert registry.get("ca/rental_epop_percentage_maximum") is RENTAL_EPOP_PERCENTAGE_MAXIMUM
    assert registry.get("ca/rental_immediate_expensing_share") is RENTAL_IMMEDIATE_EXPENSING_SHARE
    assert registry.get("ca/rental_epop_percentage_room") is RENTAL_EPOP_PERCENTAGE_ROOM
    assert (
        registry.get("ca/rental_immediate_expensing_allocated")
        is RENTAL_IMMEDIATE_EXPENSING_ALLOCATED
    )
    assert (
        registry.get("ca/rental_immediate_expensing_associated_limit")
        is RENTAL_IMMEDIATE_EXPENSING_ASSOCIATED_LIMIT
    )
    assert (
        registry.get("ca/rental_immediate_expensing_limit_before_minister")
        is RENTAL_IMMEDIATE_EXPENSING_LIMIT_BEFORE_MINISTER
    )
    assert registry.get("ca/rental_immediate_expensing_limit") is RENTAL_IMMEDIATE_EXPENSING_LIMIT
    assert registry.get("ca/rental_immediate_expensing_claim") is RENTAL_IMMEDIATE_EXPENSING_CLAIM
    assert registry.get("ca/rental_fiscal_period_days_entered") is RENTAL_FISCAL_PERIOD_DAYS_ENTERED
    assert registry.get("ca/rental_fiscal_period_days") is RENTAL_FISCAL_PERIOD_DAYS
    assert registry.get("ca/rental_partner") is RENTAL_PARTNER
    assert registry.get("ca/rental_partner_share") is RENTAL_PARTNER_SHARE
    assert registry.get("ca/rental_partner_gst_hst_rebate") is RENTAL_PARTNER_GST_HST_REBATE
    assert registry.get("ca/rental_partner_other_expenses") is RENTAL_PARTNER_OTHER_EXPENSES
    assert registry.get("ca/rental_partner_share_with_rebate") is RENTAL_PARTNER_SHARE_WITH_REBATE
    assert registry.get("ca/rental_partnership_net_income") is RENTAL_PARTNERSHIP_NET_INCOME
    assert registry.get("ca/net_rental_income") is NET_RENTAL_INCOME
    assert registry.get("ca/t776_statements") is T776_STATEMENTS
    assert registry.get("ca/t2125_statements") is T2125_STATEMENTS
    assert registry.get("ca/t2042_statements") is T2042_STATEMENTS
    assert registry.get("ca/t2121_statements") is T2121_STATEMENTS


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
        BUSINESS_INCOME,
        PROFESSIONAL_INCOME,
        COMMISSION_INCOME,
        FARMING_INCOME,
        FISHING_INCOME,
        NET_SELF_EMPLOYMENT_INCOME,
        WORKERS_COMPENSATION_BENEFITS,
        SOCIAL_ASSISTANCE_PAYMENTS,
        NET_FEDERAL_SUPPLEMENTS,
        INCOME_SUPPORT_BENEFITS,
        SHORT_TERM_RENTAL_RELATED_CCA,
        NON_COMPLIANT_CCA,
        RENTAL_NON_COMPLIANT_CCA,
    ):
        assert kind.value_type is Decimal, kind.identifier


# --- Schedule 3 (form 5000-S3) Parts 3 and 4 --------------------------------------------------

DISPOSITION_LISTS: list[tuple[str, RecordListKind]] = [
    ("ca/qsbcs_dispositions", QSBCS_DISPOSITIONS),
    ("ca/qffp_dispositions", QFFP_DISPOSITIONS),
    ("ca/qffp_foreclosure_dispositions", QFFP_FORECLOSURE_DISPOSITIONS),
    ("ca/share_dispositions", SHARE_DISPOSITIONS),
    ("ca/real_estate_dispositions", REAL_ESTATE_DISPOSITIONS),
    ("ca/bond_dispositions", BOND_DISPOSITIONS),
    ("ca/crypto_asset_dispositions", CRYPTO_ASSET_DISPOSITIONS),
    ("ca/other_foreclosure_dispositions", OTHER_FORECLOSURE_DISPOSITIONS),
    ("ca/personal_use_property_dispositions", PERSONAL_USE_PROPERTY_DISPOSITIONS),
    ("ca/listed_personal_property_dispositions", LISTED_PERSONAL_PROPERTY_DISPOSITIONS),
]

SIGNED_LINES: list[tuple[str, ArtifactKind[Any]]] = [
    ("ca/qsbcs_gain_or_loss", QSBCS_GAIN_OR_LOSS),
    ("ca/qffp_gain_or_loss", QFFP_GAIN_OR_LOSS),
    ("ca/qffp_foreclosure_gain_or_loss", QFFP_FORECLOSURE_GAIN_OR_LOSS),
    ("ca/share_gain_or_loss", SHARE_GAIN_OR_LOSS),
    ("ca/real_estate_gain_or_loss", REAL_ESTATE_GAIN_OR_LOSS),
    ("ca/bond_gain_or_loss", BOND_GAIN_OR_LOSS),
    ("ca/crypto_asset_gain_or_loss", CRYPTO_ASSET_GAIN_OR_LOSS),
    ("ca/other_foreclosure_gain_or_loss", OTHER_FORECLOSURE_GAIN_OR_LOSS),
    ("ca/listed_personal_property_gain_or_loss", LISTED_PERSONAL_PROPERTY_GAIN_OR_LOSS),
    (
        "ca/capital_gains_of_qualified_and_other_properties",
        CAPITAL_GAINS_OF_QUALIFIED_AND_OTHER_PROPERTIES,
    ),
    ("ca/capital_gains_after_deferral", CAPITAL_GAINS_AFTER_DEFERRAL),
    ("ca/slip_capital_gains_or_losses", SLIP_CAPITAL_GAINS_OR_LOSSES),
    ("ca/t3_capital_gains_or_losses", T3_CAPITAL_GAINS_OR_LOSSES),
    (
        "ca/capital_gains_before_investment_loss_reduction",
        CAPITAL_GAINS_BEFORE_INVESTMENT_LOSS_REDUCTION,
    ),
    ("ca/capital_gains_before_reserves", CAPITAL_GAINS_BEFORE_RESERVES),
    ("ca/capital_gains_reserves", CAPITAL_GAINS_RESERVES),
    ("ca/capital_gain", CAPITAL_GAIN),
    ("ca/included_capital_gain", INCLUDED_CAPITAL_GAIN),
]

NON_NEGATIVE_LINES: list[tuple[str, ArtifactKind[Any]]] = [
    ("ca/personal_use_property_gain_rows", PERSONAL_USE_PROPERTY_GAIN_ROWS),
    ("ca/personal_use_property_gain", PERSONAL_USE_PROPERTY_GAIN),
    ("ca/unapplied_listed_personal_property_losses", UNAPPLIED_LISTED_PERSONAL_PROPERTY_LOSSES),
    ("ca/listed_personal_property_net_gain", LISTED_PERSONAL_PROPERTY_NET_GAIN),
    ("ca/capital_gains_deferral", CAPITAL_GAINS_DEFERRAL),
    ("ca/partnership_gains_at_full_inclusion", PARTNERSHIP_GAINS_AT_FULL_INCLUSION),
    ("ca/disposition_proceeds", DISPOSITION_PROCEEDS),
    ("ca/disposition_adjusted_cost_base", DISPOSITION_ADJUSTED_COST_BASE),
    ("ca/disposition_outlays", DISPOSITION_OUTLAYS),
    ("ca/qsbcs_proceeds", QSBCS_PROCEEDS),
    ("ca/qffp_proceeds", QFFP_PROCEEDS),
    ("ca/qffp_foreclosure_proceeds", QFFP_FORECLOSURE_PROCEEDS),
    ("ca/share_proceeds", SHARE_PROCEEDS),
    ("ca/real_estate_proceeds", REAL_ESTATE_PROCEEDS),
    ("ca/bond_proceeds", BOND_PROCEEDS),
    ("ca/crypto_asset_proceeds", CRYPTO_ASSET_PROCEEDS),
    ("ca/other_foreclosure_proceeds", OTHER_FORECLOSURE_PROCEEDS),
]


def test_the_schedule_3_kinds_are_the_registered_ones(registry: ArtifactRegistry) -> None:
    for identifier, kind in [*DISPOSITION_LISTS, *SIGNED_LINES, *NON_NEGATIVE_LINES]:
        assert registry.get(identifier) is kind, identifier
        assert kind.identifier == identifier
        assert identifier in REGISTERED


def test_the_ten_property_lists_are_record_lists_of_columns_2_to_4() -> None:
    # Schedule 3 Part 3: "(Column 2): Proceeds of disposition", "(Column 3): Adjusted cost base",
    # "(Column 4): Outlays and expenses"; column 1 (year acquired) feeds no line, column 5 is
    # worked out. One kind of each field, shared by all ten lists, in the form's column order.
    for identifier, kind in DISPOSITION_LISTS:
        assert isinstance(kind, RecordListKind), identifier
        assert kind.value_type is RecordList
        assert kind.fields == (
            DISPOSITION_PROCEEDS,
            DISPOSITION_ADJUSTED_COST_BASE,
            DISPOSITION_OUTLAYS,
        ), identifier
        assert identifier in RECORD_LISTS


def test_the_disposition_fields_are_non_negative_decimals() -> None:
    for kind in (DISPOSITION_PROCEEDS, DISPOSITION_ADJUSTED_COST_BASE, DISPOSITION_OUTLAYS):
        assert kind.value_type is Decimal
        assert kind.non_negative is True


def test_the_part_3_and_part_4_lines_that_print_losses_in_brackets_are_signed_decimals() -> None:
    # "Report all negative amounts (losses) using brackets."
    for identifier, kind in SIGNED_LINES:
        assert kind.value_type is Decimal, identifier
        assert kind.non_negative is False, identifier
        assert identifier in SIGNED


def test_the_gain_only_lines_the_deferral_and_the_unapplied_losses_are_non_negative() -> None:
    # Line 9 and line 10 are "gain only"; line 13 and the unapplied listed personal property
    # losses are amounts the filer states.
    for identifier, kind in NON_NEGATIVE_LINES:
        assert kind.value_type is Decimal, identifier
        assert kind.non_negative is True, identifier
        assert identifier not in SIGNED


def test_the_taxable_capital_gains_stay_non_negative() -> None:
    # T1 line 12700 takes line 26 only "If positive".
    assert TAXABLE_CAPITAL_GAINS.non_negative is True
    assert "ca/taxable_capital_gains" not in SIGNED


def test_every_disposition_list_is_a_kind_of_its_own() -> None:
    assert len({id(kind) for _, kind in DISPOSITION_LISTS}) == 10


def test_the_t2125_chart_kinds_are_registered_under_their_names(registry: ArtifactRegistry) -> None:
    # Form T2125 Charts A to C: the vehicles list, the caller's sales tax rate and the printed
    # constants (each a dataset of the same name, which T2042 and T2121 still produce as kinds); the
    # lines the charts compute are in the trace of `ca/business_vehicle_expenses`, not artifacts.
    assert registry.get("ca/business_vehicle_days_divisor") is BUSINESS_VEHICLE_DAYS_DIVISOR
    assert registry.get("ca/business_vehicle_list_price") is BUSINESS_VEHICLE_LIST_PRICE
    assert registry.get("ca/business_vehicle_sales_tax_rate") is BUSINESS_VEHICLE_SALES_TAX_RATE
    assert registry.get("ca/business_vehicles") is BUSINESS_VEHICLES
    assert BUSINESS_VEHICLE_DAYS_DIVISOR.non_negative is True
    for kind in (
        BUSINESS_VEHICLE_DAYS_DIVISOR,
        BUSINESS_VEHICLE_LIST_PRICE,
        BUSINESS_VEHICLE_SALES_TAX_RATE,
    ):
        assert kind.value_type is Decimal, kind.identifier


def test_the_t2125_chart_lines_are_no_longer_artifacts(registry: ArtifactRegistry) -> None:
    # Each vehicle's lines 12, 13, 19, 26, 28 and the rest are worked inside the capability.
    for name in (
        "list_price_limit_tax",
        "lease_charge_limit_tax",
        "lease_cost_limit_tax",
        "list_price_limit_with_tax",
        "lease_charge_limit_with_tax",
        "lease_cost_limit_with_tax",
        "total_expenses",
        "business_use_part",
        "interest_for_period",
        "available_interest",
        "lease_price_base",
        "lease_price_85_percent",
        "lease_charge_portion",
        "lease_charges_net",
        "lease_cost_portion",
        "leasing_cost",
    ):
        assert f"ca/business_vehicle_{name}" not in registry.identifiers(), name


def test_the_t2042_chart_kinds_are_registered_under_their_names(registry: ArtifactRegistry) -> None:
    # Form T2042 Charts A to C: each vehicle is a record of the shared `ca/business_vehicles`, the
    # sales tax rate of the province is the statement's input, and the line 9819 kind is
    # the capability's output over the vehicles.
    assert BUSINESS_VEHICLES in T2042_STATEMENTS.fields
    assert registry.get("ca/business_vehicles") is BUSINESS_VEHICLES
    assert registry.get("ca/farm_vehicle_sales_tax_rate") is FARM_VEHICLE_SALES_TAX_RATE
    assert registry.get("ca/farm_motor_vehicle_expenses") is FARM_MOTOR_VEHICLE_EXPENSES
    assert registry.get("ca/business_vehicle_days_divisor") is BUSINESS_VEHICLE_DAYS_DIVISOR


def test_the_t2042_chart_lines_are_no_longer_artifacts(registry: ArtifactRegistry) -> None:
    # Each vehicle's lines of Charts A to C are worked inside the capability, as on T2125.
    for name in (
        "list_price_limit_tax",
        "lease_charge_limit_tax",
        "lease_cost_limit_tax",
        "list_price_limit_with_tax",
        "lease_charge_limit_with_tax",
        "lease_cost_limit_with_tax",
        "total_expenses",
        "business_use_part",
        "interest_for_period",
        "available_interest",
        "lease_price_base",
        "lease_price_85_percent",
        "lease_charge_portion",
        "lease_charges_net",
        "lease_cost_portion",
        "leasing_cost",
    ):
        assert f"ca/farm_vehicle_{name}" not in registry.identifiers(), name


def test_the_t2121_chart_kinds_are_registered_under_their_names(registry: ArtifactRegistry) -> None:
    # Form T2121 Charts A to C: each vehicle is a record of the shared `ca/business_vehicles`, the
    # sales tax rate of the province is the statement's input, and the line 9281 kind is
    # the capability's output over the vehicles.
    assert BUSINESS_VEHICLES in T2121_STATEMENTS.fields
    assert registry.get("ca/business_vehicles") is BUSINESS_VEHICLES
    assert registry.get("ca/fish_vehicle_sales_tax_rate") is FISH_VEHICLE_SALES_TAX_RATE
    assert registry.get("ca/fish_motor_vehicle_expenses") is FISH_MOTOR_VEHICLE_EXPENSES
    assert registry.get("ca/business_vehicle_days_divisor") is BUSINESS_VEHICLE_DAYS_DIVISOR


def test_the_t2121_chart_lines_are_no_longer_artifacts(registry: ArtifactRegistry) -> None:
    # Each vehicle's lines of Charts A to C are worked inside the capability, as on T2125.
    for name in (
        "list_price_limit_tax",
        "lease_charge_limit_tax",
        "lease_cost_limit_tax",
        "list_price_limit_with_tax",
        "lease_charge_limit_with_tax",
        "lease_cost_limit_with_tax",
        "total_expenses",
        "business_use_part",
        "interest_for_period",
        "available_interest",
        "lease_price_base",
        "lease_price_85_percent",
        "lease_charge_portion",
        "lease_charges_net",
        "lease_cost_portion",
        "leasing_cost",
    ):
        assert f"ca/fish_vehicle_{name}" not in registry.identifiers(), name


# --- the immediate expensing limit checks: a yes or no answer checked to be 0 or 1, and a
# business's own percentage checked against the total of column 3 (the forms are silent on both).

CHECKED_KINDS = (
    (
        "ca/rental_epop_associated",
        "ca/rental_epop_associated_checked",
        RENTAL_EPOP_ASSOCIATED_CHECKED,
        int,
    ),
    (
        "ca/rental_epop_agreement_filed",
        "ca/rental_epop_agreement_filed_checked",
        RENTAL_EPOP_AGREEMENT_FILED_CHECKED,
        int,
    ),
    (
        "ca/rental_minister_allocation_given",
        "ca/rental_minister_allocation_given_checked",
        RENTAL_MINISTER_ALLOCATION_GIVEN_CHECKED,
        int,
    ),
    (
        "ca/rental_epop_percentage",
        "ca/rental_epop_percentage_checked",
        RENTAL_EPOP_PERCENTAGE_CHECKED,
        Decimal,
    ),
    (
        "ca/business_epop_associated",
        "ca/business_epop_associated_checked",
        BUSINESS_EPOP_ASSOCIATED_CHECKED,
        int,
    ),
    (
        "ca/business_epop_agreement_filed",
        "ca/business_epop_agreement_filed_checked",
        BUSINESS_EPOP_AGREEMENT_FILED_CHECKED,
        int,
    ),
    (
        "ca/business_minister_allocation_given",
        "ca/business_minister_allocation_given_checked",
        BUSINESS_MINISTER_ALLOCATION_GIVEN_CHECKED,
        int,
    ),
    (
        "ca/business_epop_percentage",
        "ca/business_epop_percentage_checked",
        BUSINESS_EPOP_PERCENTAGE_CHECKED,
        Decimal,
    ),
    (
        "ca/farm_epop_associated",
        "ca/farm_epop_associated_checked",
        FARM_EPOP_ASSOCIATED_CHECKED,
        int,
    ),
    (
        "ca/farm_epop_agreement_filed",
        "ca/farm_epop_agreement_filed_checked",
        FARM_EPOP_AGREEMENT_FILED_CHECKED,
        int,
    ),
    (
        "ca/farm_minister_allocation_given",
        "ca/farm_minister_allocation_given_checked",
        FARM_MINISTER_ALLOCATION_GIVEN_CHECKED,
        int,
    ),
    (
        "ca/farm_epop_percentage",
        "ca/farm_epop_percentage_checked",
        FARM_EPOP_PERCENTAGE_CHECKED,
        Decimal,
    ),
    (
        "ca/fish_epop_associated",
        "ca/fish_epop_associated_checked",
        FISH_EPOP_ASSOCIATED_CHECKED,
        int,
    ),
    (
        "ca/fish_epop_agreement_filed",
        "ca/fish_epop_agreement_filed_checked",
        FISH_EPOP_AGREEMENT_FILED_CHECKED,
        int,
    ),
    (
        "ca/fish_minister_allocation_given",
        "ca/fish_minister_allocation_given_checked",
        FISH_MINISTER_ALLOCATION_GIVEN_CHECKED,
        int,
    ),
    (
        "ca/fish_epop_percentage",
        "ca/fish_epop_percentage_checked",
        FISH_EPOP_PERCENTAGE_CHECKED,
        Decimal,
    ),
)


@pytest.mark.parametrize(("input_id", "identifier", "constant", "value_type"), CHECKED_KINDS)
def test_each_checked_kind_is_registered_and_is_the_output_of_its_check(
    input_id: str,
    identifier: str,
    constant: ArtifactKind[Any],
    value_type: type,
    registry: ArtifactRegistry,
) -> None:
    # The endnote 5 answers are yes or no questions, taken as a count and checked to be 0 or 1
    # (`ca/yes_or_no_count`); the percentage is checked not to exceed the total of column 3
    # (`core/at_most`, a choice, not a form rule). The checked kind is new, beside the input.
    kind = registry.kind(identifier)
    assert kind is constant
    assert kind.identifier == identifier
    assert kind.value_type is value_type
    assert kind.non_negative is True
    assert registry.kind(input_id) is not kind
    assert registry.kind(input_id).value_type is value_type
