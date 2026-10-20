"""Snapshot of the `ca/` artifact kind identifiers, as the application registers them.

Identifiers are stored with results and exposed by the API, so changing or removing one is a
breaking change: update this snapshot only on purpose. Each package snapshots its own namespace;
declaring a kind in this package's catalog adds it here. The kinds are registered explicitly,
as the composition root does, into a fresh registry.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Any

import pytest

import app.jurisdictions.ca
import app.jurisdictions.ca.catalog
from app.domain.artifact import ArtifactCatalog, ArtifactKind, ArtifactRegistry
from app.domain.errors import InvalidRecordError, NegativeArtifactError
from app.domain.record_list import RecordList, RecordListKind
from app.jurisdictions.ca.catalog import (
    ADDITIONAL_DEDUCTIONS,
    ADJUSTED_FAMILY_NET_INCOME,
    ADJUSTED_GROSS_CAPITAL_LOSSES_1985_TO_1987,
    ADJUSTED_GROSS_CAPITAL_LOSSES_1988_AND_1989,
    ADJUSTED_GROSS_CAPITAL_LOSSES_1990_TO_1999,
    ADJUSTED_GROSS_CAPITAL_LOSSES_2001_TO_2024,
    ADJUSTED_LOSSES_APPLIED_1985_TO_1987,
    ADJUSTED_LOSSES_APPLIED_1988_AND_1989,
    ADJUSTED_LOSSES_APPLIED_1990_TO_1999,
    ADJUSTED_LOSSES_APPLIED_2001_TO_2024,
    ADJUSTED_LOSSES_LEFT_AFTER_1985_TO_1987,
    ADJUSTED_LOSSES_LEFT_AFTER_1988_AND_1989,
    ADJUSTED_LOSSES_LEFT_AFTER_1990_TO_1999,
    ADVANCED_CANADA_WORKERS_BENEFIT,
    AGE_AMOUNT,
    AGE_AMOUNT_BEFORE_COUNT,
    AGE_INCOME_OVER_THRESHOLD,
    AGE_INCOME_THRESHOLD,
    AGE_MAXIMUM,
    AGE_REDUCTION,
    ALLOWABLE_BUSINESS_INVESTMENT_LOSS,
    BASIC_PERSONAL_AMOUNT,
    BORN_IN_1960_OR_EARLIER,
    BUSINESS_INVESTMENT_LOSS,
    BUSINESS_INVESTMENT_LOSS_AFTER_REDUCTION,
    BUSINESS_INVESTMENT_LOSS_REDUCTION,
    BUSINESS_INVESTMENT_LOSS_REDUCTION_AVAILABLE,
    CANADA_EMPLOYMENT_AMOUNT,
    CANADA_WORKERS_BENEFIT,
    CANADA_WORKERS_BENEFIT_WITH_DEPENDANT,
    CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT,
    CANADIAN_ARMED_FORCES_AND_POLICE_DEDUCTION,
    CAPITAL_GAIN,
    CAPITAL_GAINS_DEDUCTIONS_1985_TO_1987,
    CAPITAL_GAINS_DEDUCTIONS_1988_AND_1989_ELIGIBLE_CAPITAL_PROPERTY,
    CAPITAL_GAINS_DEDUCTIONS_1988_AND_1989_OTHER_THAN_ELIGIBLE_CAPITAL_PROPERTY,
    CAPITAL_GAINS_DEDUCTIONS_1990_TO_1999,
    CAPITAL_GAINS_DEDUCTIONS_2000,
    CAPITAL_GAINS_DEDUCTIONS_2001_TO_2024,
    CAPITAL_GAINS_DEDUCTIONS_CLAIMED_1985_TO_2024,
    CAPITAL_GIFT_GAINS_DEDUCTION,
    CAPITAL_GIFT_TAXABLE_GAINS,
    CAPITAL_GIFTS_LIMIT_ADDITION,
    CAPITAL_GIFTS_TOTAL,
    CAPITAL_PROPERTY_GIFTS,
    CAREGIVER_AMOUNT,
    CARRYING_CHARGES_INTEREST_EXPENSES_AND_OTHER_EXPENSES,
    CATALOG,
    CHARITABLE_DONATIONS,
    CHARITABLE_DONATIONS_CLAIMED,
    CHARITABLE_DONATIONS_LIMIT,
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
    CPP_BASE_CONTRIBUTIONS,
    CPP_ENHANCED_CONTRIBUTIONS,
    CPP_FIRST_ADDITIONAL_CONTRIBUTIONS,
    CPP_OR_QPP_BENEFITS,
    CPP_SECOND_ADDITIONAL_CONTRIBUTIONS,
    CREDIT_AMOUNTS_AT_CREDIT_RATE,
    CREDITS_AGAINST_BASIC_FEDERAL_TAX,
    CREDITS_AGAINST_FEDERAL_TAX,
    CWB_BEFORE_REDUCTION_WITH_DEPENDANT,
    CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT,
    CWB_ELIGIBLE_DEPENDANTS,
    CWB_REDUCTION_WITH_DEPENDANT,
    CWB_REDUCTION_WITHOUT_DEPENDANT,
    DEDUCTIONS_FROM_NET_INCOME,
    DEDUCTIONS_FROM_TOTAL_INCOME,
    DEPENDANT_CARE_EXPENSES,
    DEPENDANT_CREDIT_AMOUNTS,
    DEPENDANT_NET_INCOME,
    DEPENDANT_TAXABLE_INCOME,
    DEPENDANT_UNDER_18,
    DEPRECIABLE_GIFT_CAPITAL_COST,
    DEPRECIABLE_GIFT_NET_PROCEEDS,
    DEPRECIABLE_GIFT_PROCEEDS_OR_COST,
    DEPRECIABLE_GIFT_RECAPTURED_DEPRECIATION,
    DEPRECIABLE_GIFTS,
    DISABILITY_DEPENDANTS,
    DISABILITY_TRANSFERRED_AMOUNT,
    DIVIDEND_TAX_CREDIT,
    DIVIDENDS_AMOUNT_A,
    DIVIDENDS_AMOUNT_A_LESS_B,
    DIVIDENDS_AMOUNT_B,
    DIVIDENDS_WITHOUT_A_SLIP_GROSSED_UP,
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
    EDUCATOR_SCHOOL_SUPPLY_CREDIT,
    EDUCATOR_SUPPLIES_EXPENSES,
    EDUCATOR_SUPPLIES_EXPENSES_AT_MOST_MAXIMUM,
    EI_AND_OTHER_BENEFITS,
    EI_PREMIUMS,
    ELECTED_SPLIT_PENSION_AMOUNT,
    ELECTED_SPLIT_PENSION_DEDUCTION,
    ELIGIBLE_DEPENDANT_AMOUNT,
    ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT,
    ELIGIBLE_DEPENDANTS,
    ELIGIBLE_DIVIDENDS_CREDIT,
    ELIGIBLE_DIVIDENDS_GROSSED_UP,
    ELIGIBLE_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP,
    EMPLOYEE_AND_PARTNER_GST_HST_REBATE,
    EMPLOYMENT_INCOME,
    EXPLORATION_AND_DEVELOPMENT_EXPENSES,
    FEDERAL_BASIC_TAX,
    FEDERAL_TAX_LESS_CREDITS,
    FEDERAL_TAX_WITH_ITC_RECAPTURE,
    FHSA_ANNUAL_AMOUNT,
    FHSA_ANNUAL_AMOUNT_AFTER_TRANSFERS,
    FHSA_ANNUAL_AMOUNT_FOR_2024,
    FHSA_ANNUAL_AMOUNT_FOR_2024_WITH_CARRYFORWARD,
    FHSA_ANNUAL_AMOUNT_WITH_CARRYFORWARD,
    FHSA_ANNUAL_LIMIT,
    FHSA_ANNUAL_LIMIT_AFTER_MAXIMUM_PARTICIPATION_PERIOD,
    FHSA_ANNUAL_LIMIT_FROM_STEP_2,
    FHSA_ANNUAL_LIMITS_FOR_2024_AND_PRIOR_YEARS,
    FHSA_ANNUAL_LIMITS_LESS_DEDUCTIONS,
    FHSA_CARRYFORWARD_FOR_2024,
    FHSA_CARRYFORWARD_FOR_2025,
    FHSA_CONTRIBUTIONS_AFTER_FIRST_QUALIFYING_WITHDRAWAL,
    FHSA_CONTRIBUTIONS_AVAILABLE,
    FHSA_CONTRIBUTIONS_DEDUCTED,
    FHSA_CONTRIBUTIONS_IN_2024,
    FHSA_CONTRIBUTIONS_IN_2024_AFTER_FIRST_QUALIFYING_WITHDRAWAL,
    FHSA_CONTRIBUTIONS_IN_2024_BEFORE_FIRST_QUALIFYING_WITHDRAWAL,
    FHSA_CONTRIBUTIONS_IN_2025,
    FHSA_CONTRIBUTIONS_IN_2025_AFTER_FIRST_QUALIFYING_WITHDRAWAL,
    FHSA_CONTRIBUTIONS_IN_2025_BEFORE_FIRST_QUALIFYING_WITHDRAWAL,
    FHSA_CONTRIBUTIONS_LIMIT,
    FHSA_CONTRIBUTIONS_PLUS_VARIABLE_B_AMOUNT,
    FHSA_DEDUCTION,
    FHSA_DEDUCTIONS_FOR_2024_AND_PRIOR_YEARS,
    FHSA_DESIGNATED_TRANSFERS_IN_2024_AND_PRIOR_YEARS,
    FHSA_DESIGNATED_TRANSFERS_IN_2025,
    FHSA_DESIGNATED_WITHDRAWALS_IN_2025,
    FHSA_EXCESS_DESIGNATED_WITHDRAWALS,
    FHSA_INCOME,
    FHSA_LIFETIME_LIMIT,
    FHSA_LIFETIME_LIMIT_LESS_DEDUCTIONS,
    FHSA_LIFETIME_LIMIT_LESS_DEDUCTIONS_AND_TRANSFERS,
    FHSA_MAXIMUM_DEDUCTION,
    FHSA_MAXIMUM_PARTICIPATION_PERIOD_ENDED,
    FHSA_NET_RRSP_TRANSFER_AMOUNT,
    FHSA_NET_RRSP_TRANSFER_AMOUNT_FOR_2024_AND_PRIOR_YEARS,
    FHSA_NET_TRANSFER_AMOUNT_AFTER_PRIOR_YEARS,
    FHSA_NET_TRANSFER_AMOUNT_LESS_VARIABLE_H_AMOUNT,
    FHSA_RRSP_TRANSFERS_IN_2024_AND_PRIOR_YEARS,
    FHSA_RRSP_TRANSFERS_IN_2025,
    FHSA_TOTAL_ANNUAL_LIMITS,
    FHSA_TOTAL_DESIGNATED_TRANSFERS,
    FHSA_TOTAL_RRSP_TRANSFERS,
    FHSA_TRANSFER_AMOUNT_AT_MOST_LIMIT,
    FHSA_TRANSFER_AMOUNT_PLUS_VARIABLE_F_AMOUNT,
    FHSA_UNUSED_CONTRIBUTIONS_BROUGHT_FORWARD,
    FHSA_UNUSED_CONTRIBUTIONS_CARRIED_FORWARD,
    FHSA_UNUSED_CONTRIBUTIONS_PLUS_CONTRIBUTIONS,
    FHSA_VARIABLE_B_AMOUNT,
    FHSA_VARIABLE_F_AMOUNT,
    FHSA_VARIABLE_H_AMOUNT,
    FIRST_TIER_DONATION_CREDIT,
    FOREIGN_CHARITY_DONATIONS,
    FOREIGN_INVESTMENT_INCOME,
    GOVERNMENT_DONATIONS,
    HIGH_INCOME_DONATION_CREDIT,
    HIGH_INCOME_DONATIONS,
    INCOME_SUPPORT_BENEFITS,
    INCOME_TAX_DEDUCTED,
    INFIRM_CHILDREN,
    INFIRM_CHILDREN_AMOUNT,
    INFIRM_DEPENDANTS,
    INTEREST_AND_OTHER_INVESTMENT_INCOME,
    INVESTMENT_INCOME_BEFORE_PRIOR_YEARS,
    INVESTMENT_INCOME_CREDITED_NOT_RECEIVED,
    INVESTMENT_INCOME_REPORTED_IN_PREVIOUS_YEARS,
    INVESTMENT_INCOME_WITHOUT_A_SLIP,
    INVESTMENT_ROYALTIES,
    ITC_RECAPTURE,
    ITC_RECAPTURE_AT_15_PERCENT,
    ITC_RECAPTURE_AT_20_PERCENT,
    ITC_RECAPTURE_EXPENDITURE_AT_15_PERCENT,
    ITC_RECAPTURE_EXPENDITURE_AT_20_PERCENT,
    JOURNALISM_LABOUR_TAX_CREDIT,
    LABOUR_SPONSORED_FUNDS_CREDIT,
    LABOUR_SPONSORED_FUNDS_CREDIT_BEFORE_MAXIMUM,
    LABOUR_SPONSORED_FUNDS_NET_COST,
    LIMITED_PARTNERSHIP_LOSSES_OF_OTHER_YEARS,
    MEDICAL_CLAIM,
    MEDICAL_EXPENSES,
    MEDICAL_EXPENSES_OVER_THRESHOLD,
    MEDICAL_NET_INCOME_SHARE,
    MEDICAL_THRESHOLD,
    NET_CAPITAL_LOSS_BALANCE_1985_TO_1987,
    NET_CAPITAL_LOSS_BALANCE_1988_AND_1989,
    NET_CAPITAL_LOSS_BALANCE_1990_TO_1999,
    NET_CAPITAL_LOSS_BALANCE_2001_TO_2024,
    NET_CAPITAL_LOSSES_AVAILABLE_TO_CLAIM,
    NET_CAPITAL_LOSSES_CLAIMED,
    NET_CAPITAL_LOSSES_OF_OTHER_YEARS,
    NET_FEDERAL_SUPPLEMENTS,
    NET_FEDERAL_TAX,
    NET_INCOME,
    NET_INCOME_BEFORE_ADJUSTMENTS,
    NET_INCOME_LESS_UCCB_AND_RDSP_INCOME,
    NET_PARTNERSHIP_INCOME,
    NO_SLIP_DIVIDEND_TAX_CREDIT,
    NON_CAPITAL_LOSSES_OF_OTHER_YEARS,
    NON_REFUNDABLE_CREDIT_AMOUNTS,
    NON_REFUNDABLE_TAX_CREDITS,
    OLD_AGE_SECURITY,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_1994,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_2024,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1994_TO_1996,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1997_TO_1999,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2000,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2001_TO_2023,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2024,
    OTHER_DEDUCTIONS,
    OTHER_DEPENDANT_MEDICAL_EXPENSES,
    OTHER_DEPENDANTS,
    OTHER_DEPENDANTS_MEDICAL,
    OTHER_DIVIDENDS_CREDIT,
    OTHER_DIVIDENDS_GROSSED_UP,
    OTHER_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP,
    OTHER_EMPLOYMENT_INCOME,
    OTHER_FHSA_INCOME,
    OTHER_INCOME,
    OTHER_PAYMENTS_DEDUCTION,
    OTHER_PAYMENTS_DEDUCTION_ABOVE_LIMIT,
    OTHER_PAYMENTS_DEDUCTION_AFTER_LIMIT,
    OTHER_PAYMENTS_LIMIT_INCOME,
    OTHER_PAYMENTS_WORKSHEET_LINE_9_OVER_LIMIT,
    OTHER_PAYMENTS_WORKSHEET_REQUIRED,
    OTHER_PENSIONS_AND_SUPERANNUATION,
    PART_XII_2_TAX_CREDIT,
    POLITICAL_CONTRIBUTIONS,
    POLITICAL_CREDIT,
    POLITICAL_CREDIT_BEFORE_MAXIMUM,
    POLITICAL_CREDIT_CHOSEN_COLUMN,
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
    POLITICAL_CREDIT_SHORTCUT_AMOUNT,
    POLITICAL_CREDIT_SHORTCUT_THRESHOLD,
    PRINCIPAL_RESIDENCE_GAIN,
    PRINCIPAL_RESIDENCE_PROPERTIES,
    PROVINCIAL_CREDITS,
    RDSP_INCOME,
    RDSP_INCOME_REPAYMENT,
    REFUND,
    REFUND_OR_BALANCE_OWING,
    REGULAR_RATE_DONATION_CREDIT,
    REGULAR_RATE_DONATIONS,
    REMAINING_ADJUSTED_LOSSES_1985_TO_1987,
    REMAINING_ADJUSTED_LOSSES_1988_AND_1989,
    REMAINING_ADJUSTED_LOSSES_1990_TO_1999,
    REMAINING_ADJUSTED_LOSSES_2001_TO_2024,
    RESIDENCE_ADJUSTED_COST_BASE,
    RESIDENCE_OUTLAYS,
    RESIDENCE_PLUS_ONE_YEAR,
    RESIDENCE_PROCEEDS,
    RESIDENCE_YEARS_DESIGNATED_1972_TO_1981,
    RESIDENCE_YEARS_DESIGNATED_AFTER_1981,
    RESIDENCE_YEARS_OWNED_1972_TO_1981,
    RESIDENCE_YEARS_OWNED_AFTER_1981,
    RESP_AIPS_ADDITIONAL_TAX,
    RESP_AIPS_CONTRIBUTIONS_COUNTED,
    RESP_AIPS_LIFETIME_LIMIT,
    RESP_AIPS_LIMIT_REMAINING,
    RESP_AIPS_PART_A_APPLIES,
    RESP_AIPS_PART_A_TAX,
    RESP_AIPS_PART_B_TAX,
    RESP_AIPS_RECEIVED_PART_A,
    RESP_AIPS_RECEIVED_PART_B,
    RESP_AIPS_REDUCTION,
    RESP_AIPS_REDUCTION_USED_IN_PREVIOUS_YEARS,
    RESP_AIPS_RRSP_CONTRIBUTIONS,
    RESP_AIPS_SUBJECT_TO_TAX,
    RL_10_LABOUR_SPONSORED_FUND_AMOUNT,
    RPP_DEDUCTION,
    RRSP_AMOUNT_DEDUCTED,
    RRSP_CONTRIBUTIONS,
    RRSP_CONTRIBUTIONS_AVAILABLE,
    RRSP_DEDUCTION,
    RRSP_DEDUCTION_LIMIT,
    RRSP_DEDUCTION_MAXIMUM,
    RRSP_INCOME,
    SECURITY_OPTIONS_DEDUCTIONS,
    SLIP_DIVIDEND_TAX_CREDIT,
    SLIP_TAXABLE_DIVIDENDS,
    SLIP_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
    SOCIAL_ASSISTANCE_PAYMENTS,
    SPECIAL_TAXES,
    SPOUSE_AMOUNT,
    SPOUSE_AMOUNT_BASIS,
    SPOUSE_AMOUNT_BEFORE_COUNT,
    SPOUSE_CAREGIVER_AMOUNT,
    SPOUSE_CAREGIVER_AMOUNT_BEFORE_COUNT,
    SPOUSE_CAREGIVER_BASE,
    SPOUSE_CAREGIVER_BEFORE_MAXIMUM,
    SPOUSE_CAREGIVER_ELIGIBLE,
    SPOUSE_CAREGIVER_LIMIT,
    SPOUSE_INFIRMITY_SUPPLEMENT,
    SPOUSE_NET_INCOME,
    SPOUSES_CLAIMED,
    SUPPORT_PAYMENTS_DEDUCTION,
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
    TAX_PAID_BY_INSTALMENTS,
    TAX_REFUND_INTEREST,
    TAXABLE_CAPITAL_GAINS,
    TAXABLE_DIVIDENDS,
    TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
    TAXABLE_INCOME,
    TAXABLE_INCOME_OVER_DONATION_THRESHOLD,
    TAXABLE_SCHOLARSHIPS,
    TAXABLE_SUPPORT_PAYMENTS,
    TOP_UP_CREDITS_BASE,
    TOP_UP_EXCESS,
    TOP_UP_TAX_CREDIT,
    TOP_UP_THRESHOLD,
    TOTAL_ADJUSTED_NET_CAPITAL_LOSSES,
    TOTAL_CARRYING_CHARGES,
    TOTAL_CHARITABLE_DONATIONS,
    TOTAL_CREDITS,
    TOTAL_INCOME,
    TOTAL_INTEREST_EXPENSES,
    TOTAL_OTHER_EXPENSES,
    TOTAL_PAYABLE,
    UCCB_AND_RDSP_INCOME,
    UCCB_AND_RDSP_INCOME_REPAYMENTS,
    UCCB_REPAYMENT,
    UNAPPLIED_NET_CAPITAL_LOSSES_1985_TO_1987,
    UNAPPLIED_NET_CAPITAL_LOSSES_1988_AND_1989,
    UNAPPLIED_NET_CAPITAL_LOSSES_1990_TO_1999,
    UNAPPLIED_NET_CAPITAL_LOSSES_2001_TO_2024,
    UNION_DUES,
    UNIVERSAL_CHILD_CARE_BENEFIT,
    UNIVERSITY_DONATIONS_OUTSIDE_CANADA,
    UNUSED_RRSP_CONTRIBUTIONS,
    UNUSED_RRSP_CONTRIBUTIONS_CARRIED_FORWARD,
    WORKERS_COMPENSATION_BENEFITS,
    WORKING_INCOME,
)
from app.registrations import JURISDICTIONS

REGISTERED = frozenset(
    {
        "ca/employment_income",
        "ca/capital_gain",
        "ca/taxable_capital_gains",
        "ca/total_income",
        "ca/other_employment_income",
        "ca/old_age_security",
        "ca/cpp_or_qpp_benefits",
        "ca/other_pensions_and_superannuation",
        "ca/elected_split_pension_amount",
        "ca/universal_child_care_benefit",
        "ca/ei_and_other_benefits",
        "ca/t3_taxable_dividends_other_than_eligible",
        "ca/t4ps_taxable_dividends_other_than_eligible",
        "ca/t5_taxable_dividends_other_than_eligible",
        "ca/t5013_taxable_dividends_other_than_eligible",
        "ca/t3_taxable_dividends",
        "ca/t4ps_taxable_dividends",
        "ca/t5_taxable_dividends",
        "ca/t5013_taxable_dividends",
        "ca/eligible_dividends_received_without_a_slip",
        "ca/other_dividends_received_without_a_slip",
        "ca/t3_dividend_tax_credit",
        "ca/t4ps_dividend_tax_credit",
        "ca/t5_dividend_tax_credit",
        "ca/t5013_dividend_tax_credit",
        "ca/slip_taxable_dividends_other_than_eligible",
        "ca/slip_taxable_dividends",
        "ca/eligible_dividends_grossed_up",
        "ca/other_dividends_grossed_up",
        "ca/dividends_without_a_slip_grossed_up",
        "ca/taxable_dividends_other_than_eligible",
        "ca/taxable_dividends",
        "ca/slip_dividend_tax_credit",
        "ca/dividends_amount_a",
        "ca/dividends_amount_b",
        "ca/other_dividends_credit",
        "ca/dividends_amount_a_less_b",
        "ca/eligible_dividends_credit",
        "ca/no_slip_dividend_tax_credit",
        "ca/dividend_tax_credit",
        "ca/credits_against_basic_federal_tax",
        "ca/t3_investment_income",
        "ca/t5_investment_income",
        "ca/t5013_investment_income",
        "ca/investment_income_credited_not_received",
        "ca/tax_refund_interest",
        "ca/foreign_investment_income",
        "ca/investment_income_without_a_slip",
        "ca/investment_royalties",
        "ca/investment_income_before_prior_years",
        "ca/investment_income_reported_in_previous_years",
        "ca/interest_and_other_investment_income",
        "ca/net_partnership_income",
        "ca/rdsp_income",
        "ca/taxable_support_payments",
        "ca/rrsp_income",
        "ca/fhsa_income",
        "ca/other_fhsa_income",
        "ca/other_income",
        "ca/taxable_scholarships",
        "ca/workers_compensation_benefits",
        "ca/social_assistance_payments",
        "ca/net_federal_supplements",
        "ca/income_support_benefits",
        "ca/rpp_deduction",
        "ca/canadian_armed_forces_and_police_deduction",
        "ca/security_options_deductions",
        "ca/uccb_repayment",
        "ca/rdsp_income_repayment",
        "ca/uccb_and_rdsp_income",
        "ca/net_income_less_uccb_and_rdsp_income",
        "ca/uccb_and_rdsp_income_repayments",
        "ca/other_payments_limit_income",
        "ca/other_payments_worksheet_required",
        "ca/other_payments_worksheet_line_9_over_limit",
        "ca/other_payments_deduction_above_limit",
        "ca/other_payments_deduction_after_limit",
        "ca/other_payments_deduction",
        "ca/limited_partnership_losses_of_other_years",
        "ca/non_capital_losses_of_other_years",
        "ca/unapplied_net_capital_losses_1985_to_1987",
        "ca/unapplied_net_capital_losses_1988_and_1989",
        "ca/unapplied_net_capital_losses_1990_to_1999",
        "ca/unapplied_net_capital_losses_2001_to_2024",
        "ca/net_capital_losses_claimed",
        "ca/adjusted_gross_capital_losses_1985_to_1987",
        "ca/adjusted_gross_capital_losses_1988_and_1989",
        "ca/adjusted_gross_capital_losses_1990_to_1999",
        "ca/adjusted_gross_capital_losses_2001_to_2024",
        "ca/total_adjusted_net_capital_losses",
        "ca/net_capital_losses_available_to_claim",
        "ca/net_capital_losses_of_other_years",
        "ca/adjusted_losses_applied_1985_to_1987",
        "ca/adjusted_losses_left_after_1985_to_1987",
        "ca/remaining_adjusted_losses_1985_to_1987",
        "ca/net_capital_loss_balance_1985_to_1987",
        "ca/adjusted_losses_applied_1988_and_1989",
        "ca/adjusted_losses_left_after_1988_and_1989",
        "ca/remaining_adjusted_losses_1988_and_1989",
        "ca/net_capital_loss_balance_1988_and_1989",
        "ca/adjusted_losses_applied_1990_to_1999",
        "ca/adjusted_losses_left_after_1990_to_1999",
        "ca/remaining_adjusted_losses_1990_to_1999",
        "ca/net_capital_loss_balance_1990_to_1999",
        "ca/adjusted_losses_applied_2001_to_2024",
        "ca/remaining_adjusted_losses_2001_to_2024",
        "ca/net_capital_loss_balance_2001_to_2024",
        "ca/additional_deductions",
        "ca/unused_rrsp_contributions",
        "ca/rrsp_contributions",
        "ca/rrsp_contributions_available",
        "ca/rrsp_deduction_limit",
        "ca/rrsp_deduction_maximum",
        "ca/rrsp_amount_deducted",
        "ca/rrsp_deduction",
        "ca/unused_rrsp_contributions_carried_forward",
        "ca/fhsa_contributions_in_2025",
        "ca/fhsa_contributions_in_2025_after_first_qualifying_withdrawal",
        "ca/fhsa_contributions_in_2025_before_first_qualifying_withdrawal",
        "ca/fhsa_variable_b_amount",
        "ca/fhsa_contributions_plus_variable_b_amount",
        "ca/fhsa_designated_withdrawals_in_2025",
        "ca/fhsa_contributions_in_2024",
        "ca/fhsa_contributions_in_2024_before_first_qualifying_withdrawal",
        "ca/fhsa_contributions_in_2024_after_first_qualifying_withdrawal",
        "ca/fhsa_contributions_after_first_qualifying_withdrawal",
        "ca/fhsa_excess_designated_withdrawals",
        "ca/fhsa_contributions_limit",
        "ca/fhsa_annual_amount",
        "ca/fhsa_carryforward_for_2025",
        "ca/fhsa_annual_amount_with_carryforward",
        "ca/fhsa_rrsp_transfers_in_2024_and_prior_years",
        "ca/fhsa_rrsp_transfers_in_2025",
        "ca/fhsa_total_rrsp_transfers",
        "ca/fhsa_designated_transfers_in_2024_and_prior_years",
        "ca/fhsa_designated_transfers_in_2025",
        "ca/fhsa_total_designated_transfers",
        "ca/fhsa_net_rrsp_transfer_amount",
        "ca/fhsa_net_rrsp_transfer_amount_for_2024_and_prior_years",
        "ca/fhsa_variable_h_amount",
        "ca/fhsa_net_transfer_amount_less_variable_h_amount",
        "ca/fhsa_annual_amount_for_2024",
        "ca/fhsa_carryforward_for_2024",
        "ca/fhsa_annual_amount_for_2024_with_carryforward",
        "ca/fhsa_transfer_amount_at_most_limit",
        "ca/fhsa_variable_f_amount",
        "ca/fhsa_transfer_amount_plus_variable_f_amount",
        "ca/fhsa_net_transfer_amount_after_prior_years",
        "ca/fhsa_annual_amount_after_transfers",
        "ca/fhsa_maximum_participation_period_ended",
        "ca/fhsa_annual_limit_from_step_2",
        "ca/fhsa_annual_limit_after_maximum_participation_period",
        "ca/fhsa_annual_limit",
        "ca/fhsa_annual_limits_for_2024_and_prior_years",
        "ca/fhsa_total_annual_limits",
        "ca/fhsa_deductions_for_2024_and_prior_years",
        "ca/fhsa_annual_limits_less_deductions",
        "ca/fhsa_lifetime_limit",
        "ca/fhsa_lifetime_limit_less_deductions",
        "ca/fhsa_lifetime_limit_less_deductions_and_transfers",
        "ca/fhsa_maximum_deduction",
        "ca/fhsa_unused_contributions_brought_forward",
        "ca/fhsa_unused_contributions_plus_contributions",
        "ca/fhsa_contributions_available",
        "ca/fhsa_contributions_deducted",
        "ca/fhsa_deduction",
        "ca/fhsa_unused_contributions_carried_forward",
        "ca/elected_split_pension_deduction",
        "ca/union_dues",
        "ca/child_care_expenses_paid",
        "ca/children_under_seven",
        "ca/children_with_disability",
        "ca/children_seven_to_sixteen",
        "ca/child_care_limit_for_children_under_seven",
        "ca/child_care_limit_for_children_with_disability",
        "ca/child_care_limit_for_children_seven_to_sixteen",
        "ca/child_care_basic_limit",
        "ca/child_care_earned_income",
        "ca/child_care_earned_income_limit",
        "ca/child_care_expenses",
        "ca/capital_gains_deductions_1985_to_1987",
        "ca/capital_gains_deductions_1988_and_1989_other_than_eligible_capital_property",
        "ca/capital_gains_deductions_1988_and_1989_eligible_capital_property",
        "ca/capital_gains_deductions_1990_to_1999",
        "ca/capital_gains_deductions_2000",
        "ca/capital_gains_deductions_2001_to_2024",
        "ca/capital_gains_deductions_claimed_1985_to_2024",
        "ca/other_business_investment_loss_reductions_1986_to_1994",
        "ca/other_business_investment_loss_reductions_1994_to_1996",
        "ca/other_business_investment_loss_reductions_1997_to_1999",
        "ca/other_business_investment_loss_reductions_2000",
        "ca/other_business_investment_loss_reductions_2001_to_2023",
        "ca/other_business_investment_loss_reductions_2024",
        "ca/other_business_investment_loss_reductions_1986_to_2024",
        "ca/business_investment_loss_reduction_available",
        "ca/business_investment_loss",
        "ca/business_investment_loss_reduction",
        "ca/business_investment_loss_after_reduction",
        "ca/allowable_business_investment_loss",
        "ca/support_payments_deduction",
        "ca/total_carrying_charges",
        "ca/total_interest_expenses",
        "ca/total_other_expenses",
        "ca/carrying_charges_interest_expenses_and_other_expenses",
        "ca/cpp_first_additional_contributions",
        "ca/cpp_second_additional_contributions",
        "ca/cpp_enhanced_contributions",
        "ca/exploration_and_development_expenses",
        "ca/other_deductions",
        "ca/deductions_from_total_income",
        "ca/net_income_before_adjustments",
        "ca/net_income",
        "ca/deductions_from_net_income",
        "ca/taxable_income",
        "ca/federal_basic_tax",
        "ca/basic_personal_amount",
        "ca/born_in_1960_or_earlier",
        "ca/age_maximum",
        "ca/age_income_threshold",
        "ca/age_income_over_threshold",
        "ca/age_reduction",
        "ca/age_amount_before_count",
        "ca/age_amount",
        "ca/spouses_claimed",
        "ca/spouse_caregiver_eligible",
        "ca/spouse_net_income",
        "ca/spouse_infirmity_supplement",
        "ca/spouse_amount_basis",
        "ca/spouse_amount_before_count",
        "ca/spouse_amount",
        "ca/eligible_dependants",
        "ca/dependant_net_income",
        "ca/eligible_dependant_amount_before_count",
        "ca/eligible_dependant_amount",
        "ca/spouse_caregiver_base",
        "ca/spouse_caregiver_before_maximum",
        "ca/spouse_caregiver_limit",
        "ca/spouse_caregiver_amount_before_count",
        "ca/spouse_caregiver_amount",
        "ca/infirm_dependants",
        "ca/caregiver_amount",
        "ca/other_dependant_medical_expenses",
        "ca/other_dependants",
        "ca/other_dependants_medical",
        "ca/medical_expenses",
        "ca/medical_net_income_share",
        "ca/medical_threshold",
        "ca/medical_expenses_over_threshold",
        "ca/medical_claim",
        "ca/infirm_children",
        "ca/infirm_children_amount",
        "ca/dependant_under_18",
        "ca/dependant_care_expenses",
        "ca/dependant_credit_amounts",
        "ca/dependant_taxable_income",
        "ca/disability_dependants",
        "ca/disability_transferred_amount",
        "ca/residence_years_designated_after_1981",
        "ca/residence_years_designated_1972_to_1981",
        "ca/residence_years_owned_after_1981",
        "ca/residence_years_owned_1972_to_1981",
        "ca/residence_proceeds",
        "ca/residence_outlays",
        "ca/residence_adjusted_cost_base",
        "ca/residence_plus_one_year",
        "ca/principal_residence_properties",
        "ca/principal_residence_gain",
        "ca/cpp_base_contributions",
        "ca/ei_premiums",
        "ca/canada_employment_amount",
        "ca/non_refundable_credit_amounts",
        "ca/non_refundable_tax_credits",
        "ca/federal_tax_after_credits",
        "ca/itc_recapture_expenditure_at_15_percent",
        "ca/itc_recapture_expenditure_at_20_percent",
        "ca/labour_sponsored_funds_net_cost",
        "ca/advanced_canada_workers_benefit",
        "ca/resp_aips_received_part_a",
        "ca/resp_aips_rrsp_contributions",
        "ca/resp_aips_reduction_used_in_previous_years",
        "ca/resp_aips_received_part_b",
        "ca/resp_aips_part_a_applies",
        "ca/rl_10_labour_sponsored_fund_amount",
        "ca/political_contributions",
        "ca/itc_recapture_at_15_percent",
        "ca/itc_recapture_at_20_percent",
        "ca/itc_recapture",
        "ca/federal_tax_with_itc_recapture",
        "ca/political_credit_column_1_line_2",
        "ca/political_credit_column_1_line_3",
        "ca/political_credit_column_1_line_5",
        "ca/political_credit_column_1_line_6",
        "ca/political_credit_column_1_line_7",
        "ca/political_credit_column_2_line_2",
        "ca/political_credit_column_2_line_3",
        "ca/political_credit_column_2_line_5",
        "ca/political_credit_column_2_line_6",
        "ca/political_credit_column_2_line_7",
        "ca/political_credit_column_3_line_2",
        "ca/political_credit_column_3_line_3",
        "ca/political_credit_column_3_line_5",
        "ca/political_credit_column_3_line_6",
        "ca/political_credit_column_3_line_7",
        "ca/political_credit_chosen_column",
        "ca/political_credit_shortcut_threshold",
        "ca/political_credit_shortcut_amount",
        "ca/political_credit_before_maximum",
        "ca/political_credit",
        "ca/labour_sponsored_funds_credit_before_maximum",
        "ca/labour_sponsored_funds_credit",
        "ca/credits_against_federal_tax",
        "ca/federal_tax_less_credits",
        "ca/resp_aips_contributions_counted",
        "ca/resp_aips_lifetime_limit",
        "ca/resp_aips_limit_remaining",
        "ca/resp_aips_reduction",
        "ca/resp_aips_subject_to_tax",
        "ca/resp_aips_part_a_tax",
        "ca/resp_aips_part_b_tax",
        "ca/resp_aips_additional_tax",
        "ca/special_taxes",
        "ca/net_federal_tax",
        "ca/total_payable",
        "ca/income_tax_deducted",
        "ca/cwb_eligible_dependants",
        "ca/working_income",
        "ca/adjusted_family_net_income",
        "ca/cwb_before_reduction_without_dependant",
        "ca/cwb_reduction_without_dependant",
        "ca/canada_workers_benefit_without_dependant",
        "ca/cwb_before_reduction_with_dependant",
        "ca/cwb_reduction_with_dependant",
        "ca/canada_workers_benefit_with_dependant",
        "ca/canada_workers_benefit",
        "ca/provincial_credits",
        "ca/part_xii_2_tax_credit",
        "ca/employee_and_partner_gst_hst_rebate",
        "ca/educator_supplies_expenses",
        "ca/educator_supplies_expenses_at_most_maximum",
        "ca/educator_school_supply_credit",
        "ca/journalism_labour_tax_credit",
        "ca/tax_paid_by_instalments",
        "ca/total_credits",
        "ca/refund_or_balance_owing",
        "ca/refund",
        "ca/charitable_donations",
        "ca/government_donations",
        "ca/university_donations_outside_canada",
        "ca/foreign_charity_donations",
        "ca/ecological_and_cultural_gifts",
        "ca/ecological_gifts_before_2016",
        "ca/depreciable_gift_recaptured_depreciation",
        "ca/depreciable_gift_net_proceeds",
        "ca/depreciable_gift_capital_cost",
        "ca/capital_gift_taxable_gains",
        "ca/capital_gift_gains_deduction",
        "ca/depreciable_gift_proceeds_or_cost",
        "ca/depreciable_gifts",
        "ca/capital_property_gifts",
        "ca/total_charitable_donations",
        "ca/donation_limit_on_net_income",
        "ca/capital_gifts_total",
        "ca/capital_gifts_limit_addition",
        "ca/donation_limit_with_capital_gifts",
        "ca/charitable_donations_limit",
        "ca/charitable_donations_claimed",
        "ca/donations_and_gifts_total",
        "ca/donation_first_tier_maximum",
        "ca/donations_first_tier",
        "ca/donations_over_first_tier",
        "ca/donations_over_first_tier_after_2016_gifts",
        "ca/donation_high_income_threshold",
        "ca/taxable_income_over_donation_threshold",
        "ca/high_income_donations",
        "ca/high_income_donation_credit",
        "ca/regular_rate_donations",
        "ca/regular_rate_donation_credit",
        "ca/first_tier_donation_credit",
        "ca/donations_and_gifts_credit",
        "ca/credit_amounts_at_credit_rate",
        "ca/top_up_credits_base",
        "ca/top_up_threshold",
        "ca/top_up_excess",
        "ca/top_up_tax_credit",
    }
)
# T1 line 167 (line 48400 or 48500): the balance, negative for a refund; and the Federal
# Worksheet's "Line 25000 - Other payments deduction" line 5 "Line 1 minus line 4 =" and line 9
# "Line 5 plus line 8 =", which print no "(if negative, enter "0")" and so may be below zero: the
# `ca/` kinds that may be below zero. So are the lines of the T1 Step 3 chain that print no "(if
# negative, enter "0")": T1 line 54 (line 23400) "Line 34 minus line 53 (if negative, show in
# brackets)", the lines of Form T1436 (Capital Gains Worksheet) line 21700 that subtract with no
# floor or take the lesser of such a line (lines 15 and 17), and the lines of Schedule 15 (FHSA)
# Steps 2 and 3 that subtract or add such a line with no floor (lines 3, 5, 9, 11, 23, 27, 36, 45,
# 48, 51, 54, 56 and 58); and Form T1172 (RESP additional tax) Part A line 6 "Line 4 minus line
# 5" and line 7 "Amount from line 3 or 6, whichever is less", which print no "(if negative, enter
# "0")".
SIGNED = frozenset(
    {
        "ca/refund_or_balance_owing",
        "ca/net_income_less_uccb_and_rdsp_income",
        "ca/other_payments_limit_income",
        "ca/fhsa_contributions_in_2025_before_first_qualifying_withdrawal",
        "ca/fhsa_contributions_plus_variable_b_amount",
        "ca/fhsa_contributions_in_2024_after_first_qualifying_withdrawal",
        "ca/fhsa_contributions_after_first_qualifying_withdrawal",
        "ca/fhsa_net_rrsp_transfer_amount",
        "ca/fhsa_net_rrsp_transfer_amount_for_2024_and_prior_years",
        "ca/fhsa_net_transfer_amount_after_prior_years",
        "ca/fhsa_annual_limits_less_deductions",
        "ca/fhsa_lifetime_limit_less_deductions",
        "ca/fhsa_maximum_deduction",
        "ca/fhsa_unused_contributions_plus_contributions",
        "ca/fhsa_contributions_available",
        "ca/fhsa_unused_contributions_carried_forward",
        "ca/business_investment_loss_reduction_available",
        "ca/business_investment_loss_reduction",
        "ca/net_income_before_adjustments",
        "ca/resp_aips_limit_remaining",
        "ca/resp_aips_reduction",
    }
)
# T1 line 30400 (Schedule 5, "Each household is allowed only one claim for this amount") and line
# 30499 ("Number of children you are claiming this amount for"): the numbers of eligible
# dependants and of infirm children; and Form T778 Part B lines 1 to 3 ("Number of eligible
# children born in 2019 or later whom the disability amount cannot be claimed for", "... born in
# 2025 or earlier whom the disability amount can be claimed for", "... born in 2009 to 2018"):
# the numbers of eligible children for the child care expenses deduction; and Schedule 6 line 38100
# ("Do you have an eligible dependant? 1 Yes or 2 No"), whose eligible dependant is "your or your
# spouse's or common-law partner's child", "under 19 years of age" and "not eligible for the CWB for
# 2025": the number of eligible dependants for the Canada workers benefit; T1 line 30100 ("if
# you were born in 1960 or earlier"), Schedule 5 line 30300 (the spouse amount claimed) and line
# 51090 (eligible for the Canada caregiver amount for the spouse), each a 0 or 1 count as the forms
# take it; and the Federal Worksheet's "Line 25000 - Other payments deduction": 1 if an amount was
# entered on line 14600 ("enter the amount from line 14700 if you did not enter an amount on line
# 14600; otherwise, use Federal Worksheet") and 1 if "the amount on line 9 is more than $93,454",
# each 0 or 1 until a comparison capability derives them; and Schedule 15 Step 2 "If your maximum
# participation period (MPP) ended in a prior year, do not complete this step. Your 2025 annual FHSA
# limit is "0".": 1 if it ended in a prior year and 0 otherwise; and Form T1172 "Part B - Fill out
# this part only if Part A does not apply to you": 1 if Part A applies and 0 otherwise; counted, not
# money.
COUNTS = frozenset(
    {
        "ca/eligible_dependants",
        "ca/infirm_children",
        "ca/dependant_under_18",
        "ca/residence_years_designated_after_1981",
        "ca/residence_years_designated_1972_to_1981",
        "ca/residence_years_owned_after_1981",
        "ca/residence_years_owned_1972_to_1981",
        "ca/residence_plus_one_year",
        "ca/born_in_1960_or_earlier",
        "ca/spouses_claimed",
        "ca/spouse_caregiver_eligible",
        "ca/children_under_seven",
        "ca/children_with_disability",
        "ca/children_seven_to_sixteen",
        "ca/cwb_eligible_dependants",
        "ca/other_payments_worksheet_required",
        "ca/other_payments_worksheet_line_9_over_limit",
        "ca/fhsa_maximum_participation_period_ended",
        "ca/resp_aips_part_a_applies",
    }
)
# T1 line 82 (line 30450) and Schedule 5 "Line 30450 - Canada caregiver amount for other infirm
# dependants age 18 or older": "Complete the chart below for each dependant who meets the
# conditions above", so the infirm dependants are a list of records, not a number.
# Federal Worksheet "Line 31800 - Disability amount transferred from a dependant": "Complete the
# following calculation fore ach dependant who is eligible for the disability tax credit in 2025",
# so the dependants who qualify are a list of records too.
# Form T2091(IND): "Complete a separate form for each property you sold.", so the properties sold
# are a list of records as well.
RECORD_LISTS = frozenset(
    {
        "ca/infirm_dependants",
        "ca/disability_dependants",
        "ca/other_dependants",
        "ca/principal_residence_properties",
    }
)


@pytest.fixture
def registry() -> ArtifactRegistry:
    registry = ArtifactRegistry()
    JURISDICTIONS.register(registry)
    return registry


def test_registered_identifiers_snapshot(registry: ArtifactRegistry) -> None:
    identifiers = registry.identifiers()

    assert {i for i in identifiers if i.startswith("ca/")} == REGISTERED


def test_the_package_exposes_its_catalog() -> None:
    assert isinstance(app.jurisdictions.ca.catalog.CATALOG, ArtifactCatalog)
    assert app.jurisdictions.ca.catalog.CATALOG is CATALOG
    assert {kind.identifier for kind in CATALOG.kinds} == REGISTERED


def test_catalog_kinds_are_the_registered_ones(registry: ArtifactRegistry) -> None:
    assert registry.get("ca/taxable_income") is TAXABLE_INCOME
    assert registry.get("ca/federal_basic_tax") is FEDERAL_BASIC_TAX
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
    assert registry.get("ca/rpp_deduction") is RPP_DEDUCTION
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
    assert (
        registry.get("ca/limited_partnership_losses_of_other_years")
        is LIMITED_PARTNERSHIP_LOSSES_OF_OTHER_YEARS
    )
    assert registry.get("ca/non_capital_losses_of_other_years") is NON_CAPITAL_LOSSES_OF_OTHER_YEARS
    assert (
        registry.get("ca/unapplied_net_capital_losses_1985_to_1987")
        is UNAPPLIED_NET_CAPITAL_LOSSES_1985_TO_1987
    )
    assert (
        registry.get("ca/unapplied_net_capital_losses_1988_and_1989")
        is UNAPPLIED_NET_CAPITAL_LOSSES_1988_AND_1989
    )
    assert (
        registry.get("ca/unapplied_net_capital_losses_1990_to_1999")
        is UNAPPLIED_NET_CAPITAL_LOSSES_1990_TO_1999
    )
    assert (
        registry.get("ca/unapplied_net_capital_losses_2001_to_2024")
        is UNAPPLIED_NET_CAPITAL_LOSSES_2001_TO_2024
    )
    assert registry.get("ca/net_capital_losses_claimed") is NET_CAPITAL_LOSSES_CLAIMED
    assert (
        registry.get("ca/adjusted_gross_capital_losses_1985_to_1987")
        is ADJUSTED_GROSS_CAPITAL_LOSSES_1985_TO_1987
    )
    assert (
        registry.get("ca/adjusted_gross_capital_losses_1988_and_1989")
        is ADJUSTED_GROSS_CAPITAL_LOSSES_1988_AND_1989
    )
    assert (
        registry.get("ca/adjusted_gross_capital_losses_1990_to_1999")
        is ADJUSTED_GROSS_CAPITAL_LOSSES_1990_TO_1999
    )
    assert (
        registry.get("ca/adjusted_gross_capital_losses_2001_to_2024")
        is ADJUSTED_GROSS_CAPITAL_LOSSES_2001_TO_2024
    )
    assert registry.get("ca/total_adjusted_net_capital_losses") is TOTAL_ADJUSTED_NET_CAPITAL_LOSSES
    assert (
        registry.get("ca/net_capital_losses_available_to_claim")
        is NET_CAPITAL_LOSSES_AVAILABLE_TO_CLAIM
    )
    assert registry.get("ca/net_capital_losses_of_other_years") is NET_CAPITAL_LOSSES_OF_OTHER_YEARS
    assert (
        registry.get("ca/adjusted_losses_applied_1985_to_1987")
        is ADJUSTED_LOSSES_APPLIED_1985_TO_1987
    )
    assert (
        registry.get("ca/adjusted_losses_left_after_1985_to_1987")
        is ADJUSTED_LOSSES_LEFT_AFTER_1985_TO_1987
    )
    assert (
        registry.get("ca/remaining_adjusted_losses_1985_to_1987")
        is REMAINING_ADJUSTED_LOSSES_1985_TO_1987
    )
    assert (
        registry.get("ca/net_capital_loss_balance_1985_to_1987")
        is NET_CAPITAL_LOSS_BALANCE_1985_TO_1987
    )
    assert (
        registry.get("ca/adjusted_losses_applied_1988_and_1989")
        is ADJUSTED_LOSSES_APPLIED_1988_AND_1989
    )
    assert (
        registry.get("ca/adjusted_losses_left_after_1988_and_1989")
        is ADJUSTED_LOSSES_LEFT_AFTER_1988_AND_1989
    )
    assert (
        registry.get("ca/remaining_adjusted_losses_1988_and_1989")
        is REMAINING_ADJUSTED_LOSSES_1988_AND_1989
    )
    assert (
        registry.get("ca/net_capital_loss_balance_1988_and_1989")
        is NET_CAPITAL_LOSS_BALANCE_1988_AND_1989
    )
    assert (
        registry.get("ca/adjusted_losses_applied_1990_to_1999")
        is ADJUSTED_LOSSES_APPLIED_1990_TO_1999
    )
    assert (
        registry.get("ca/adjusted_losses_left_after_1990_to_1999")
        is ADJUSTED_LOSSES_LEFT_AFTER_1990_TO_1999
    )
    assert (
        registry.get("ca/remaining_adjusted_losses_1990_to_1999")
        is REMAINING_ADJUSTED_LOSSES_1990_TO_1999
    )
    assert (
        registry.get("ca/net_capital_loss_balance_1990_to_1999")
        is NET_CAPITAL_LOSS_BALANCE_1990_TO_1999
    )
    assert (
        registry.get("ca/adjusted_losses_applied_2001_to_2024")
        is ADJUSTED_LOSSES_APPLIED_2001_TO_2024
    )
    assert (
        registry.get("ca/remaining_adjusted_losses_2001_to_2024")
        is REMAINING_ADJUSTED_LOSSES_2001_TO_2024
    )
    assert (
        registry.get("ca/net_capital_loss_balance_2001_to_2024")
        is NET_CAPITAL_LOSS_BALANCE_2001_TO_2024
    )
    assert registry.get("ca/additional_deductions") is ADDITIONAL_DEDUCTIONS
    assert registry.get("ca/unused_rrsp_contributions") is UNUSED_RRSP_CONTRIBUTIONS
    assert registry.get("ca/rrsp_contributions") is RRSP_CONTRIBUTIONS
    assert registry.get("ca/rrsp_contributions_available") is RRSP_CONTRIBUTIONS_AVAILABLE
    assert registry.get("ca/rrsp_deduction_limit") is RRSP_DEDUCTION_LIMIT
    assert registry.get("ca/rrsp_deduction_maximum") is RRSP_DEDUCTION_MAXIMUM
    assert registry.get("ca/rrsp_amount_deducted") is RRSP_AMOUNT_DEDUCTED
    assert registry.get("ca/rrsp_deduction") is RRSP_DEDUCTION
    assert (
        registry.get("ca/unused_rrsp_contributions_carried_forward")
        is UNUSED_RRSP_CONTRIBUTIONS_CARRIED_FORWARD
    )
    assert registry.get("ca/fhsa_contributions_in_2025") is FHSA_CONTRIBUTIONS_IN_2025
    assert (
        registry.get("ca/fhsa_contributions_in_2025_after_first_qualifying_withdrawal")
        is FHSA_CONTRIBUTIONS_IN_2025_AFTER_FIRST_QUALIFYING_WITHDRAWAL
    )
    assert (
        registry.get("ca/fhsa_contributions_in_2025_before_first_qualifying_withdrawal")
        is FHSA_CONTRIBUTIONS_IN_2025_BEFORE_FIRST_QUALIFYING_WITHDRAWAL
    )
    assert registry.get("ca/fhsa_variable_b_amount") is FHSA_VARIABLE_B_AMOUNT
    assert (
        registry.get("ca/fhsa_contributions_plus_variable_b_amount")
        is FHSA_CONTRIBUTIONS_PLUS_VARIABLE_B_AMOUNT
    )
    assert (
        registry.get("ca/fhsa_designated_withdrawals_in_2025")
        is FHSA_DESIGNATED_WITHDRAWALS_IN_2025
    )
    assert registry.get("ca/fhsa_contributions_in_2024") is FHSA_CONTRIBUTIONS_IN_2024
    assert (
        registry.get("ca/fhsa_contributions_in_2024_before_first_qualifying_withdrawal")
        is FHSA_CONTRIBUTIONS_IN_2024_BEFORE_FIRST_QUALIFYING_WITHDRAWAL
    )
    assert (
        registry.get("ca/fhsa_contributions_in_2024_after_first_qualifying_withdrawal")
        is FHSA_CONTRIBUTIONS_IN_2024_AFTER_FIRST_QUALIFYING_WITHDRAWAL
    )
    assert (
        registry.get("ca/fhsa_contributions_after_first_qualifying_withdrawal")
        is FHSA_CONTRIBUTIONS_AFTER_FIRST_QUALIFYING_WITHDRAWAL
    )
    assert (
        registry.get("ca/fhsa_excess_designated_withdrawals") is FHSA_EXCESS_DESIGNATED_WITHDRAWALS
    )
    assert registry.get("ca/fhsa_contributions_limit") is FHSA_CONTRIBUTIONS_LIMIT
    assert registry.get("ca/fhsa_annual_amount") is FHSA_ANNUAL_AMOUNT
    assert registry.get("ca/fhsa_carryforward_for_2025") is FHSA_CARRYFORWARD_FOR_2025
    assert (
        registry.get("ca/fhsa_annual_amount_with_carryforward")
        is FHSA_ANNUAL_AMOUNT_WITH_CARRYFORWARD
    )
    assert (
        registry.get("ca/fhsa_rrsp_transfers_in_2024_and_prior_years")
        is FHSA_RRSP_TRANSFERS_IN_2024_AND_PRIOR_YEARS
    )
    assert registry.get("ca/fhsa_rrsp_transfers_in_2025") is FHSA_RRSP_TRANSFERS_IN_2025
    assert registry.get("ca/fhsa_total_rrsp_transfers") is FHSA_TOTAL_RRSP_TRANSFERS
    assert (
        registry.get("ca/fhsa_designated_transfers_in_2024_and_prior_years")
        is FHSA_DESIGNATED_TRANSFERS_IN_2024_AND_PRIOR_YEARS
    )
    assert registry.get("ca/fhsa_designated_transfers_in_2025") is FHSA_DESIGNATED_TRANSFERS_IN_2025
    assert registry.get("ca/fhsa_total_designated_transfers") is FHSA_TOTAL_DESIGNATED_TRANSFERS
    assert registry.get("ca/fhsa_net_rrsp_transfer_amount") is FHSA_NET_RRSP_TRANSFER_AMOUNT
    assert (
        registry.get("ca/fhsa_net_rrsp_transfer_amount_for_2024_and_prior_years")
        is FHSA_NET_RRSP_TRANSFER_AMOUNT_FOR_2024_AND_PRIOR_YEARS
    )
    assert registry.get("ca/fhsa_variable_h_amount") is FHSA_VARIABLE_H_AMOUNT
    assert (
        registry.get("ca/fhsa_net_transfer_amount_less_variable_h_amount")
        is FHSA_NET_TRANSFER_AMOUNT_LESS_VARIABLE_H_AMOUNT
    )
    assert registry.get("ca/fhsa_annual_amount_for_2024") is FHSA_ANNUAL_AMOUNT_FOR_2024
    assert registry.get("ca/fhsa_carryforward_for_2024") is FHSA_CARRYFORWARD_FOR_2024
    assert (
        registry.get("ca/fhsa_annual_amount_for_2024_with_carryforward")
        is FHSA_ANNUAL_AMOUNT_FOR_2024_WITH_CARRYFORWARD
    )
    assert (
        registry.get("ca/fhsa_transfer_amount_at_most_limit") is FHSA_TRANSFER_AMOUNT_AT_MOST_LIMIT
    )
    assert registry.get("ca/fhsa_variable_f_amount") is FHSA_VARIABLE_F_AMOUNT
    assert (
        registry.get("ca/fhsa_transfer_amount_plus_variable_f_amount")
        is FHSA_TRANSFER_AMOUNT_PLUS_VARIABLE_F_AMOUNT
    )
    assert (
        registry.get("ca/fhsa_net_transfer_amount_after_prior_years")
        is FHSA_NET_TRANSFER_AMOUNT_AFTER_PRIOR_YEARS
    )
    assert (
        registry.get("ca/fhsa_annual_amount_after_transfers") is FHSA_ANNUAL_AMOUNT_AFTER_TRANSFERS
    )
    assert (
        registry.get("ca/fhsa_maximum_participation_period_ended")
        is FHSA_MAXIMUM_PARTICIPATION_PERIOD_ENDED
    )
    assert registry.get("ca/fhsa_annual_limit_from_step_2") is FHSA_ANNUAL_LIMIT_FROM_STEP_2
    assert (
        registry.get("ca/fhsa_annual_limit_after_maximum_participation_period")
        is FHSA_ANNUAL_LIMIT_AFTER_MAXIMUM_PARTICIPATION_PERIOD
    )
    assert registry.get("ca/fhsa_annual_limit") is FHSA_ANNUAL_LIMIT
    assert (
        registry.get("ca/fhsa_annual_limits_for_2024_and_prior_years")
        is FHSA_ANNUAL_LIMITS_FOR_2024_AND_PRIOR_YEARS
    )
    assert registry.get("ca/fhsa_total_annual_limits") is FHSA_TOTAL_ANNUAL_LIMITS
    assert (
        registry.get("ca/fhsa_deductions_for_2024_and_prior_years")
        is FHSA_DEDUCTIONS_FOR_2024_AND_PRIOR_YEARS
    )
    assert (
        registry.get("ca/fhsa_annual_limits_less_deductions") is FHSA_ANNUAL_LIMITS_LESS_DEDUCTIONS
    )
    assert registry.get("ca/fhsa_lifetime_limit") is FHSA_LIFETIME_LIMIT
    assert (
        registry.get("ca/fhsa_lifetime_limit_less_deductions")
        is FHSA_LIFETIME_LIMIT_LESS_DEDUCTIONS
    )
    assert (
        registry.get("ca/fhsa_lifetime_limit_less_deductions_and_transfers")
        is FHSA_LIFETIME_LIMIT_LESS_DEDUCTIONS_AND_TRANSFERS
    )
    assert registry.get("ca/fhsa_maximum_deduction") is FHSA_MAXIMUM_DEDUCTION
    assert (
        registry.get("ca/fhsa_unused_contributions_brought_forward")
        is FHSA_UNUSED_CONTRIBUTIONS_BROUGHT_FORWARD
    )
    assert (
        registry.get("ca/fhsa_unused_contributions_plus_contributions")
        is FHSA_UNUSED_CONTRIBUTIONS_PLUS_CONTRIBUTIONS
    )
    assert registry.get("ca/fhsa_contributions_available") is FHSA_CONTRIBUTIONS_AVAILABLE
    assert registry.get("ca/fhsa_contributions_deducted") is FHSA_CONTRIBUTIONS_DEDUCTED
    assert registry.get("ca/fhsa_deduction") is FHSA_DEDUCTION
    assert (
        registry.get("ca/fhsa_unused_contributions_carried_forward")
        is FHSA_UNUSED_CONTRIBUTIONS_CARRIED_FORWARD
    )
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
    assert registry.get("ca/deductions_from_net_income") is DEDUCTIONS_FROM_NET_INCOME
    assert registry.get("ca/basic_personal_amount") is BASIC_PERSONAL_AMOUNT
    assert registry.get("ca/born_in_1960_or_earlier") is BORN_IN_1960_OR_EARLIER
    assert registry.get("ca/age_maximum") is AGE_MAXIMUM
    assert registry.get("ca/age_income_threshold") is AGE_INCOME_THRESHOLD
    assert registry.get("ca/age_income_over_threshold") is AGE_INCOME_OVER_THRESHOLD
    assert registry.get("ca/age_reduction") is AGE_REDUCTION
    assert registry.get("ca/age_amount_before_count") is AGE_AMOUNT_BEFORE_COUNT
    assert registry.get("ca/age_amount") is AGE_AMOUNT
    assert registry.get("ca/spouses_claimed") is SPOUSES_CLAIMED
    assert registry.get("ca/spouse_caregiver_eligible") is SPOUSE_CAREGIVER_ELIGIBLE
    assert registry.get("ca/spouse_net_income") is SPOUSE_NET_INCOME
    assert registry.get("ca/spouse_infirmity_supplement") is SPOUSE_INFIRMITY_SUPPLEMENT
    assert registry.get("ca/spouse_amount_basis") is SPOUSE_AMOUNT_BASIS
    assert registry.get("ca/spouse_amount_before_count") is SPOUSE_AMOUNT_BEFORE_COUNT
    assert registry.get("ca/spouse_amount") is SPOUSE_AMOUNT
    assert registry.get("ca/eligible_dependants") is ELIGIBLE_DEPENDANTS
    assert registry.get("ca/dependant_net_income") is DEPENDANT_NET_INCOME
    assert (
        registry.get("ca/eligible_dependant_amount_before_count")
        is ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT
    )
    assert registry.get("ca/eligible_dependant_amount") is ELIGIBLE_DEPENDANT_AMOUNT
    assert registry.get("ca/spouse_caregiver_base") is SPOUSE_CAREGIVER_BASE
    assert registry.get("ca/spouse_caregiver_before_maximum") is SPOUSE_CAREGIVER_BEFORE_MAXIMUM
    assert registry.get("ca/spouse_caregiver_limit") is SPOUSE_CAREGIVER_LIMIT
    assert (
        registry.get("ca/spouse_caregiver_amount_before_count")
        is SPOUSE_CAREGIVER_AMOUNT_BEFORE_COUNT
    )
    assert registry.get("ca/spouse_caregiver_amount") is SPOUSE_CAREGIVER_AMOUNT
    assert registry.get("ca/infirm_dependants") is INFIRM_DEPENDANTS
    assert registry.get("ca/caregiver_amount") is CAREGIVER_AMOUNT
    assert registry.get("ca/other_dependant_medical_expenses") is OTHER_DEPENDANT_MEDICAL_EXPENSES
    assert registry.get("ca/other_dependants") is OTHER_DEPENDANTS
    assert registry.get("ca/other_dependants_medical") is OTHER_DEPENDANTS_MEDICAL
    assert registry.get("ca/medical_expenses") is MEDICAL_EXPENSES
    assert registry.get("ca/medical_net_income_share") is MEDICAL_NET_INCOME_SHARE
    assert registry.get("ca/medical_threshold") is MEDICAL_THRESHOLD
    assert registry.get("ca/medical_expenses_over_threshold") is MEDICAL_EXPENSES_OVER_THRESHOLD
    assert registry.get("ca/medical_claim") is MEDICAL_CLAIM
    assert registry.get("ca/dependant_under_18") is DEPENDANT_UNDER_18
    assert registry.get("ca/dependant_care_expenses") is DEPENDANT_CARE_EXPENSES
    assert registry.get("ca/dependant_credit_amounts") is DEPENDANT_CREDIT_AMOUNTS
    assert registry.get("ca/dependant_taxable_income") is DEPENDANT_TAXABLE_INCOME
    assert registry.get("ca/disability_dependants") is DISABILITY_DEPENDANTS
    assert registry.get("ca/disability_transferred_amount") is DISABILITY_TRANSFERRED_AMOUNT
    assert (
        registry.get("ca/residence_years_designated_after_1981")
        is RESIDENCE_YEARS_DESIGNATED_AFTER_1981
    )
    assert (
        registry.get("ca/residence_years_designated_1972_to_1981")
        is RESIDENCE_YEARS_DESIGNATED_1972_TO_1981
    )
    assert registry.get("ca/residence_years_owned_after_1981") is RESIDENCE_YEARS_OWNED_AFTER_1981
    assert (
        registry.get("ca/residence_years_owned_1972_to_1981") is RESIDENCE_YEARS_OWNED_1972_TO_1981
    )
    assert registry.get("ca/residence_proceeds") is RESIDENCE_PROCEEDS
    assert registry.get("ca/residence_outlays") is RESIDENCE_OUTLAYS
    assert registry.get("ca/residence_adjusted_cost_base") is RESIDENCE_ADJUSTED_COST_BASE
    assert registry.get("ca/residence_plus_one_year") is RESIDENCE_PLUS_ONE_YEAR
    assert registry.get("ca/principal_residence_properties") is PRINCIPAL_RESIDENCE_PROPERTIES
    assert registry.get("ca/principal_residence_gain") is PRINCIPAL_RESIDENCE_GAIN
    assert registry.get("ca/infirm_children") is INFIRM_CHILDREN
    assert registry.get("ca/infirm_children_amount") is INFIRM_CHILDREN_AMOUNT
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
    assert registry.get("ca/labour_sponsored_funds_net_cost") is LABOUR_SPONSORED_FUNDS_NET_COST
    assert registry.get("ca/advanced_canada_workers_benefit") is ADVANCED_CANADA_WORKERS_BENEFIT
    assert registry.get("ca/resp_aips_received_part_a") is RESP_AIPS_RECEIVED_PART_A
    assert registry.get("ca/resp_aips_rrsp_contributions") is RESP_AIPS_RRSP_CONTRIBUTIONS
    assert (
        registry.get("ca/resp_aips_reduction_used_in_previous_years")
        is RESP_AIPS_REDUCTION_USED_IN_PREVIOUS_YEARS
    )
    assert registry.get("ca/resp_aips_received_part_b") is RESP_AIPS_RECEIVED_PART_B
    assert registry.get("ca/resp_aips_part_a_applies") is RESP_AIPS_PART_A_APPLIES
    assert (
        registry.get("ca/rl_10_labour_sponsored_fund_amount") is RL_10_LABOUR_SPONSORED_FUND_AMOUNT
    )
    assert registry.get("ca/political_contributions") is POLITICAL_CONTRIBUTIONS
    assert registry.get("ca/itc_recapture_at_15_percent") is ITC_RECAPTURE_AT_15_PERCENT
    assert registry.get("ca/itc_recapture_at_20_percent") is ITC_RECAPTURE_AT_20_PERCENT
    assert registry.get("ca/itc_recapture") is ITC_RECAPTURE
    assert registry.get("ca/federal_tax_with_itc_recapture") is FEDERAL_TAX_WITH_ITC_RECAPTURE
    assert registry.get("ca/political_credit_column_1_line_2") is POLITICAL_CREDIT_COLUMN_1_LINE_2
    assert registry.get("ca/political_credit_column_1_line_3") is POLITICAL_CREDIT_COLUMN_1_LINE_3
    assert registry.get("ca/political_credit_column_1_line_5") is POLITICAL_CREDIT_COLUMN_1_LINE_5
    assert registry.get("ca/political_credit_column_1_line_6") is POLITICAL_CREDIT_COLUMN_1_LINE_6
    assert registry.get("ca/political_credit_column_1_line_7") is POLITICAL_CREDIT_COLUMN_1_LINE_7
    assert registry.get("ca/political_credit_column_2_line_2") is POLITICAL_CREDIT_COLUMN_2_LINE_2
    assert registry.get("ca/political_credit_column_2_line_3") is POLITICAL_CREDIT_COLUMN_2_LINE_3
    assert registry.get("ca/political_credit_column_2_line_5") is POLITICAL_CREDIT_COLUMN_2_LINE_5
    assert registry.get("ca/political_credit_column_2_line_6") is POLITICAL_CREDIT_COLUMN_2_LINE_6
    assert registry.get("ca/political_credit_column_2_line_7") is POLITICAL_CREDIT_COLUMN_2_LINE_7
    assert registry.get("ca/political_credit_column_3_line_2") is POLITICAL_CREDIT_COLUMN_3_LINE_2
    assert registry.get("ca/political_credit_column_3_line_3") is POLITICAL_CREDIT_COLUMN_3_LINE_3
    assert registry.get("ca/political_credit_column_3_line_5") is POLITICAL_CREDIT_COLUMN_3_LINE_5
    assert registry.get("ca/political_credit_column_3_line_6") is POLITICAL_CREDIT_COLUMN_3_LINE_6
    assert registry.get("ca/political_credit_column_3_line_7") is POLITICAL_CREDIT_COLUMN_3_LINE_7
    assert registry.get("ca/political_credit_chosen_column") is POLITICAL_CREDIT_CHOSEN_COLUMN
    assert (
        registry.get("ca/political_credit_shortcut_threshold")
        is POLITICAL_CREDIT_SHORTCUT_THRESHOLD
    )
    assert registry.get("ca/political_credit_shortcut_amount") is POLITICAL_CREDIT_SHORTCUT_AMOUNT
    assert registry.get("ca/political_credit_before_maximum") is POLITICAL_CREDIT_BEFORE_MAXIMUM
    assert registry.get("ca/political_credit") is POLITICAL_CREDIT
    assert (
        registry.get("ca/labour_sponsored_funds_credit_before_maximum")
        is LABOUR_SPONSORED_FUNDS_CREDIT_BEFORE_MAXIMUM
    )
    assert registry.get("ca/labour_sponsored_funds_credit") is LABOUR_SPONSORED_FUNDS_CREDIT
    assert registry.get("ca/credits_against_federal_tax") is CREDITS_AGAINST_FEDERAL_TAX
    assert registry.get("ca/federal_tax_less_credits") is FEDERAL_TAX_LESS_CREDITS
    assert registry.get("ca/resp_aips_contributions_counted") is RESP_AIPS_CONTRIBUTIONS_COUNTED
    assert registry.get("ca/resp_aips_lifetime_limit") is RESP_AIPS_LIFETIME_LIMIT
    assert registry.get("ca/resp_aips_limit_remaining") is RESP_AIPS_LIMIT_REMAINING
    assert registry.get("ca/resp_aips_reduction") is RESP_AIPS_REDUCTION
    assert registry.get("ca/resp_aips_subject_to_tax") is RESP_AIPS_SUBJECT_TO_TAX
    assert registry.get("ca/resp_aips_part_a_tax") is RESP_AIPS_PART_A_TAX
    assert registry.get("ca/resp_aips_part_b_tax") is RESP_AIPS_PART_B_TAX
    assert registry.get("ca/resp_aips_additional_tax") is RESP_AIPS_ADDITIONAL_TAX
    assert registry.get("ca/special_taxes") is SPECIAL_TAXES
    assert registry.get("ca/net_federal_tax") is NET_FEDERAL_TAX
    assert registry.get("ca/total_payable") is TOTAL_PAYABLE
    assert registry.get("ca/income_tax_deducted") is INCOME_TAX_DEDUCTED
    assert registry.get("ca/cwb_eligible_dependants") is CWB_ELIGIBLE_DEPENDANTS
    assert registry.get("ca/working_income") is WORKING_INCOME
    assert registry.get("ca/adjusted_family_net_income") is ADJUSTED_FAMILY_NET_INCOME
    assert (
        registry.get("ca/cwb_before_reduction_without_dependant")
        is CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT
    )
    assert registry.get("ca/cwb_reduction_without_dependant") is CWB_REDUCTION_WITHOUT_DEPENDANT
    assert (
        registry.get("ca/canada_workers_benefit_without_dependant")
        is CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT
    )
    assert (
        registry.get("ca/cwb_before_reduction_with_dependant")
        is CWB_BEFORE_REDUCTION_WITH_DEPENDANT
    )
    assert registry.get("ca/cwb_reduction_with_dependant") is CWB_REDUCTION_WITH_DEPENDANT
    assert (
        registry.get("ca/canada_workers_benefit_with_dependant")
        is CANADA_WORKERS_BENEFIT_WITH_DEPENDANT
    )
    assert registry.get("ca/canada_workers_benefit") is CANADA_WORKERS_BENEFIT
    assert registry.get("ca/provincial_credits") is PROVINCIAL_CREDITS
    assert registry.get("ca/part_xii_2_tax_credit") is PART_XII_2_TAX_CREDIT
    assert (
        registry.get("ca/employee_and_partner_gst_hst_rebate")
        is EMPLOYEE_AND_PARTNER_GST_HST_REBATE
    )
    assert registry.get("ca/educator_supplies_expenses") is EDUCATOR_SUPPLIES_EXPENSES
    assert (
        registry.get("ca/educator_supplies_expenses_at_most_maximum")
        is EDUCATOR_SUPPLIES_EXPENSES_AT_MOST_MAXIMUM
    )
    assert registry.get("ca/educator_school_supply_credit") is EDUCATOR_SCHOOL_SUPPLY_CREDIT
    assert registry.get("ca/journalism_labour_tax_credit") is JOURNALISM_LABOUR_TAX_CREDIT
    assert registry.get("ca/tax_paid_by_instalments") is TAX_PAID_BY_INSTALMENTS
    assert registry.get("ca/total_credits") is TOTAL_CREDITS
    assert registry.get("ca/refund_or_balance_owing") is REFUND_OR_BALANCE_OWING
    assert registry.get("ca/refund") is REFUND
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


def test_catalog_kinds_are_in_the_package_namespace() -> None:
    for kind in CATALOG.kinds:
        assert kind.identifier.startswith(f"{app.jurisdictions.ca.NAMESPACE}/")


def test_catalog_kinds_are_money() -> None:
    assert TAXABLE_INCOME.value_type is Decimal
    assert FEDERAL_BASIC_TAX.value_type is Decimal
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
        LIMITED_PARTNERSHIP_LOSSES_OF_OTHER_YEARS,
        NON_CAPITAL_LOSSES_OF_OTHER_YEARS,
        UNAPPLIED_NET_CAPITAL_LOSSES_1985_TO_1987,
        UNAPPLIED_NET_CAPITAL_LOSSES_1988_AND_1989,
        UNAPPLIED_NET_CAPITAL_LOSSES_1990_TO_1999,
        UNAPPLIED_NET_CAPITAL_LOSSES_2001_TO_2024,
        NET_CAPITAL_LOSSES_CLAIMED,
        ADJUSTED_GROSS_CAPITAL_LOSSES_1985_TO_1987,
        ADJUSTED_GROSS_CAPITAL_LOSSES_1988_AND_1989,
        ADJUSTED_GROSS_CAPITAL_LOSSES_1990_TO_1999,
        ADJUSTED_GROSS_CAPITAL_LOSSES_2001_TO_2024,
        TOTAL_ADJUSTED_NET_CAPITAL_LOSSES,
        NET_CAPITAL_LOSSES_AVAILABLE_TO_CLAIM,
        NET_CAPITAL_LOSSES_OF_OTHER_YEARS,
        ADJUSTED_LOSSES_APPLIED_1985_TO_1987,
        ADJUSTED_LOSSES_LEFT_AFTER_1985_TO_1987,
        REMAINING_ADJUSTED_LOSSES_1985_TO_1987,
        NET_CAPITAL_LOSS_BALANCE_1985_TO_1987,
        ADJUSTED_LOSSES_APPLIED_1988_AND_1989,
        ADJUSTED_LOSSES_LEFT_AFTER_1988_AND_1989,
        REMAINING_ADJUSTED_LOSSES_1988_AND_1989,
        NET_CAPITAL_LOSS_BALANCE_1988_AND_1989,
        ADJUSTED_LOSSES_APPLIED_1990_TO_1999,
        ADJUSTED_LOSSES_LEFT_AFTER_1990_TO_1999,
        REMAINING_ADJUSTED_LOSSES_1990_TO_1999,
        NET_CAPITAL_LOSS_BALANCE_1990_TO_1999,
        ADJUSTED_LOSSES_APPLIED_2001_TO_2024,
        REMAINING_ADJUSTED_LOSSES_2001_TO_2024,
        NET_CAPITAL_LOSS_BALANCE_2001_TO_2024,
        ADDITIONAL_DEDUCTIONS,
        UNUSED_RRSP_CONTRIBUTIONS,
        RRSP_CONTRIBUTIONS,
        RRSP_CONTRIBUTIONS_AVAILABLE,
        RRSP_DEDUCTION_LIMIT,
        RRSP_DEDUCTION_MAXIMUM,
        RRSP_AMOUNT_DEDUCTED,
        RRSP_DEDUCTION,
        UNUSED_RRSP_CONTRIBUTIONS_CARRIED_FORWARD,
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
        DEDUCTIONS_FROM_NET_INCOME,
        BASIC_PERSONAL_AMOUNT,
        AGE_MAXIMUM,
        AGE_INCOME_THRESHOLD,
        AGE_INCOME_OVER_THRESHOLD,
        AGE_REDUCTION,
        AGE_AMOUNT_BEFORE_COUNT,
        AGE_AMOUNT,
        SPOUSE_NET_INCOME,
        SPOUSE_INFIRMITY_SUPPLEMENT,
        SPOUSE_AMOUNT_BASIS,
        SPOUSE_AMOUNT_BEFORE_COUNT,
        SPOUSE_AMOUNT,
        DEPENDANT_NET_INCOME,
        ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT,
        ELIGIBLE_DEPENDANT_AMOUNT,
        SPOUSE_CAREGIVER_BASE,
        SPOUSE_CAREGIVER_BEFORE_MAXIMUM,
        SPOUSE_CAREGIVER_LIMIT,
        SPOUSE_CAREGIVER_AMOUNT_BEFORE_COUNT,
        SPOUSE_CAREGIVER_AMOUNT,
        CAREGIVER_AMOUNT,
        OTHER_DEPENDANT_MEDICAL_EXPENSES,
        OTHER_DEPENDANTS_MEDICAL,
        MEDICAL_EXPENSES,
        MEDICAL_NET_INCOME_SHARE,
        MEDICAL_THRESHOLD,
        MEDICAL_EXPENSES_OVER_THRESHOLD,
        MEDICAL_CLAIM,
        DEPENDANT_CARE_EXPENSES,
        DEPENDANT_CREDIT_AMOUNTS,
        DEPENDANT_TAXABLE_INCOME,
        DISABILITY_TRANSFERRED_AMOUNT,
        RESIDENCE_PROCEEDS,
        RESIDENCE_OUTLAYS,
        RESIDENCE_ADJUSTED_COST_BASE,
        PRINCIPAL_RESIDENCE_GAIN,
        INFIRM_CHILDREN_AMOUNT,
        NON_REFUNDABLE_CREDIT_AMOUNTS,
        CPP_BASE_CONTRIBUTIONS,
        EI_PREMIUMS,
        CANADA_EMPLOYMENT_AMOUNT,
        NON_REFUNDABLE_TAX_CREDITS,
        ITC_RECAPTURE_EXPENDITURE_AT_15_PERCENT,
        ITC_RECAPTURE_EXPENDITURE_AT_20_PERCENT,
        LABOUR_SPONSORED_FUNDS_NET_COST,
        ADVANCED_CANADA_WORKERS_BENEFIT,
        RESP_AIPS_RECEIVED_PART_A,
        RESP_AIPS_RRSP_CONTRIBUTIONS,
        RESP_AIPS_REDUCTION_USED_IN_PREVIOUS_YEARS,
        RESP_AIPS_RECEIVED_PART_B,
        RL_10_LABOUR_SPONSORED_FUND_AMOUNT,
        POLITICAL_CONTRIBUTIONS,
        ITC_RECAPTURE_AT_15_PERCENT,
        ITC_RECAPTURE_AT_20_PERCENT,
        ITC_RECAPTURE,
        FEDERAL_TAX_WITH_ITC_RECAPTURE,
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
        POLITICAL_CREDIT_CHOSEN_COLUMN,
        POLITICAL_CREDIT_SHORTCUT_THRESHOLD,
        POLITICAL_CREDIT_SHORTCUT_AMOUNT,
        POLITICAL_CREDIT_BEFORE_MAXIMUM,
        POLITICAL_CREDIT,
        LABOUR_SPONSORED_FUNDS_CREDIT_BEFORE_MAXIMUM,
        LABOUR_SPONSORED_FUNDS_CREDIT,
        CREDITS_AGAINST_FEDERAL_TAX,
        FEDERAL_TAX_LESS_CREDITS,
        RESP_AIPS_CONTRIBUTIONS_COUNTED,
        RESP_AIPS_LIFETIME_LIMIT,
        RESP_AIPS_LIMIT_REMAINING,
        RESP_AIPS_REDUCTION,
        RESP_AIPS_SUBJECT_TO_TAX,
        RESP_AIPS_PART_A_TAX,
        RESP_AIPS_PART_B_TAX,
        RESP_AIPS_ADDITIONAL_TAX,
        SPECIAL_TAXES,
        NET_FEDERAL_TAX,
        TOTAL_PAYABLE,
        INCOME_TAX_DEDUCTED,
        WORKING_INCOME,
        ADJUSTED_FAMILY_NET_INCOME,
        CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT,
        CWB_REDUCTION_WITHOUT_DEPENDANT,
        CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT,
        CWB_BEFORE_REDUCTION_WITH_DEPENDANT,
        CWB_REDUCTION_WITH_DEPENDANT,
        CANADA_WORKERS_BENEFIT_WITH_DEPENDANT,
        CANADA_WORKERS_BENEFIT,
        PROVINCIAL_CREDITS,
        PART_XII_2_TAX_CREDIT,
        EMPLOYEE_AND_PARTNER_GST_HST_REBATE,
        EDUCATOR_SUPPLIES_EXPENSES,
        EDUCATOR_SUPPLIES_EXPENSES_AT_MOST_MAXIMUM,
        EDUCATOR_SCHOOL_SUPPLY_CREDIT,
        JOURNALISM_LABOUR_TAX_CREDIT,
        TAX_PAID_BY_INSTALMENTS,
        TOTAL_CREDITS,
        REFUND_OR_BALANCE_OWING,
        REFUND,
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


def test_every_registered_kind_but_the_counts_and_record_lists_is_money(
    registry: ArtifactRegistry,
) -> None:
    for identifier in REGISTERED - COUNTS - RECORD_LISTS:
        kind = registry.get(identifier)
        assert isinstance(kind, ArtifactKind)
        assert kind.value_type is Decimal, identifier


def test_the_counts_are_int_kinds_in_the_package_namespace(registry: ArtifactRegistry) -> None:
    assert COUNTS <= REGISTERED
    for identifier in COUNTS:
        kind = registry.get(identifier)
        assert isinstance(kind, ArtifactKind)
        assert kind.identifier.startswith(f"{app.jurisdictions.ca.NAMESPACE}/")
        assert kind.value_type is int, identifier


def test_every_kind_but_the_balance_is_declared_non_negative(registry: ArtifactRegistry) -> None:
    # No other `ca/` line can be negative on the forms as modelled.
    # A record list is not an amount: it is never declared non-negative, its fields are.
    for kind in CATALOG.kinds:
        if kind.identifier not in SIGNED | RECORD_LISTS:
            assert kind.non_negative is True, kind.identifier
    for identifier in REGISTERED - SIGNED - RECORD_LISTS:
        assert registry.kind(identifier).non_negative is True, identifier


def test_the_refund_or_balance_owing_is_signed(registry: ArtifactRegistry) -> None:
    # T1 line 167 "Line 149 minus line 166 If the amount is negative, enter it on line 48400
    # below. If the amount is positive, enter it on line 48500 below. Refund or balance owing":
    # negative is a refund, so the kind is not declared non-negative.
    assert REFUND_OR_BALANCE_OWING.non_negative is False
    assert registry.kind("ca/refund_or_balance_owing").non_negative is False
    assert SIGNED <= REGISTERED


def test_the_other_payments_worksheets_lines_5_and_9_are_signed(registry: ArtifactRegistry) -> None:
    # Federal Worksheet "Line 25000 - Other payments deduction": line 5 "Line 1 minus line 4 =" and
    # line 9 "Line 5 plus line 8 =" print no floor, unlike line 1 ("if negative, enter "0"").
    assert NET_INCOME_LESS_UCCB_AND_RDSP_INCOME.non_negative is False
    assert OTHER_PAYMENTS_LIMIT_INCOME.non_negative is False
    assert registry.kind("ca/net_income_less_uccb_and_rdsp_income").non_negative is False
    assert registry.kind("ca/other_payments_limit_income").non_negative is False
    assert UCCB_AND_RDSP_INCOME.non_negative is True
    assert UCCB_AND_RDSP_INCOME_REPAYMENTS.non_negative is True
    assert OTHER_PAYMENTS_DEDUCTION.non_negative is True


def test_the_net_income_before_adjustments_is_signed(registry: ArtifactRegistry) -> None:
    # T1 line 54 and line 23400 "Line 34 minus line 53 (if negative, show in brackets) Net income
    # before adjustments": the brackets are a negative figure, unlike line 56 (line 23600) "Line 54
    # minus line 55 (if negative, enter "0")", which stays the non-negative `ca/net_income`.
    assert NET_INCOME_BEFORE_ADJUSTMENTS.non_negative is False
    assert registry.kind("ca/net_income_before_adjustments").non_negative is False
    assert NET_INCOME.non_negative is True
    assert DEDUCTIONS_FROM_TOTAL_INCOME.non_negative is True


def test_the_t1436_lines_that_print_no_floor_are_signed(registry: ArtifactRegistry) -> None:
    # Form T1436 line 21700: line 15 "Line 7 minus line 14" and line 17 "Enter whichever is less:
    # amount from line 15 or line 16." print no "(if negative, enter "0")".
    assert BUSINESS_INVESTMENT_LOSS_REDUCTION_AVAILABLE.non_negative is False
    assert BUSINESS_INVESTMENT_LOSS_REDUCTION.non_negative is False
    assert registry.kind("ca/business_investment_loss_reduction_available").non_negative is False
    assert registry.kind("ca/business_investment_loss_reduction").non_negative is False


def test_the_other_t1436_lines_are_non_negative(registry: ArtifactRegistry) -> None:
    # Lines 7 and 14 add non-negative figures; line 18 "Line 16 minus line 17" is never negative as
    # line 17 is at most line 16; line 20 "Line 18 multiplied by the percentage on line 19".
    for kind in (
        CAPITAL_GAINS_DEDUCTIONS_CLAIMED_1985_TO_2024,
        OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_2024,
        BUSINESS_INVESTMENT_LOSS,
        BUSINESS_INVESTMENT_LOSS_AFTER_REDUCTION,
        ALLOWABLE_BUSINESS_INVESTMENT_LOSS,
    ):
        assert kind.non_negative is True, kind.identifier
        assert registry.kind(kind.identifier).non_negative is True, kind.identifier


def test_the_schedule_15_lines_that_print_no_floor_are_signed(registry: ArtifactRegistry) -> None:
    # Schedule 15 (FHSA) Steps 2 and 3: lines 3, 5, 9, 11, 23, 27, 36, 45, 48, 51, 54, 56 and 58
    # subtract (or add a line that subtracts, or take the lesser of such a line) with no "(if
    # negative, enter "0")".
    for kind in (
        FHSA_CONTRIBUTIONS_IN_2025_BEFORE_FIRST_QUALIFYING_WITHDRAWAL,
        FHSA_CONTRIBUTIONS_PLUS_VARIABLE_B_AMOUNT,
        FHSA_CONTRIBUTIONS_IN_2024_AFTER_FIRST_QUALIFYING_WITHDRAWAL,
        FHSA_CONTRIBUTIONS_AFTER_FIRST_QUALIFYING_WITHDRAWAL,
        FHSA_NET_RRSP_TRANSFER_AMOUNT,
        FHSA_NET_RRSP_TRANSFER_AMOUNT_FOR_2024_AND_PRIOR_YEARS,
        FHSA_NET_TRANSFER_AMOUNT_AFTER_PRIOR_YEARS,
        FHSA_ANNUAL_LIMITS_LESS_DEDUCTIONS,
        FHSA_LIFETIME_LIMIT_LESS_DEDUCTIONS,
        FHSA_MAXIMUM_DEDUCTION,
        FHSA_UNUSED_CONTRIBUTIONS_PLUS_CONTRIBUTIONS,
        FHSA_CONTRIBUTIONS_AVAILABLE,
        FHSA_UNUSED_CONTRIBUTIONS_CARRIED_FORWARD,
    ):
        assert kind.non_negative is False, kind.identifier
        assert registry.kind(kind.identifier).non_negative is False, kind.identifier


def test_the_schedule_15_lines_that_print_a_floor_or_add_non_negative_figures_are_non_negative(
    registry: ArtifactRegistry,
) -> None:
    # Lines 12, 13, 29, 39 and 50 print "(if negative, enter "0")"; lines 16, 19, 22, 32, 33, 35,
    # 40 and 43 and the deduction (line 57, at most line 51) add or take the lesser of
    # non-negative lines.
    for kind in (
        FHSA_EXCESS_DESIGNATED_WITHDRAWALS,
        FHSA_CONTRIBUTIONS_LIMIT,
        FHSA_ANNUAL_AMOUNT_WITH_CARRYFORWARD,
        FHSA_TOTAL_RRSP_TRANSFERS,
        FHSA_TOTAL_DESIGNATED_TRANSFERS,
        FHSA_NET_TRANSFER_AMOUNT_LESS_VARIABLE_H_AMOUNT,
        FHSA_ANNUAL_AMOUNT_FOR_2024_WITH_CARRYFORWARD,
        FHSA_TRANSFER_AMOUNT_AT_MOST_LIMIT,
        FHSA_TRANSFER_AMOUNT_PLUS_VARIABLE_F_AMOUNT,
        FHSA_ANNUAL_AMOUNT_AFTER_TRANSFERS,
        FHSA_ANNUAL_LIMIT_FROM_STEP_2,
        FHSA_ANNUAL_LIMIT,
        FHSA_TOTAL_ANNUAL_LIMITS,
        FHSA_LIFETIME_LIMIT_LESS_DEDUCTIONS_AND_TRANSFERS,
        FHSA_DEDUCTION,
    ):
        assert kind.non_negative is True, kind.identifier
        assert registry.kind(kind.identifier).non_negative is True, kind.identifier


def test_the_fhsa_maximum_participation_period_count_is_a_non_negative_int() -> None:
    # Schedule 15 Step 2: "If your maximum participation period (MPP) ended in a prior year, ...
    # Enter "0" on line 40": a caller's 0 or 1 count.
    assert FHSA_MAXIMUM_PARTICIPATION_PERIOD_ENDED.value_type is int
    assert FHSA_MAXIMUM_PARTICIPATION_PERIOD_ENDED.non_negative is True


def test_the_income_tax_deducted_is_non_negative() -> None:
    # T1 line 150 (line 43700) "Total income tax deducted (amounts from all Canadian slips)".
    assert INCOME_TAX_DEDUCTED.non_negative is True


def test_the_rrsp_amount_deducted_is_non_negative() -> None:
    # Schedule 7 line 18 "Enter your RRSP, PRPP, or SPP contributions you are deducting for 2025
    # (cannot be more than the amount on line 17).": an amount the filer states.
    assert RRSP_AMOUNT_DEDUCTED.non_negative is True


def test_capital_gain_is_non_negative_while_losses_are_not_modelled() -> None:
    assert CAPITAL_GAIN.non_negative is True


def test_the_step_6_credit_lines_are_non_negative(registry: ArtifactRegistry) -> None:
    # T1 lines 45600, 45700, 46800, 46900, 47555 and 47600 are slip, receipt or form amounts of
    # money paid or credited to the filer, none of which prints a negative figure; line 48400
    # "Refund" is the negative of line 167 and is entered only when line 167 is negative, so it is
    # never below zero, unlike line 167 (`ca/refund_or_balance_owing`), which stays signed.
    for kind in (
        PART_XII_2_TAX_CREDIT,
        EMPLOYEE_AND_PARTNER_GST_HST_REBATE,
        EDUCATOR_SUPPLIES_EXPENSES,
        EDUCATOR_SUPPLIES_EXPENSES_AT_MOST_MAXIMUM,
        EDUCATOR_SCHOOL_SUPPLY_CREDIT,
        JOURNALISM_LABOUR_TAX_CREDIT,
        TAX_PAID_BY_INSTALMENTS,
        REFUND,
    ):
        assert kind.value_type is Decimal, kind.identifier
        assert kind.non_negative is True, kind.identifier
        assert registry.kind(kind.identifier).non_negative is True, kind.identifier
    assert REFUND_OR_BALANCE_OWING.non_negative is False


def test_the_infirm_dependants_are_a_record_list_of_their_net_incomes(
    registry: ArtifactRegistry,
) -> None:
    # Schedule 5 line 30450's chart, per dependant: line 2 "Infirm dependant's net income from
    # line 23600 of their return", the one field a record holds (the caller lists only the
    # dependants who are eligible, so there are no eligibility fields).
    assert RECORD_LISTS <= REGISTERED
    assert isinstance(INFIRM_DEPENDANTS, RecordListKind)
    assert INFIRM_DEPENDANTS.identifier == "ca/infirm_dependants"
    assert INFIRM_DEPENDANTS.value_type is RecordList
    assert INFIRM_DEPENDANTS.fields == (DEPENDANT_NET_INCOME,)
    assert registry.get("ca/infirm_dependants") is INFIRM_DEPENDANTS


def test_the_record_list_reuses_the_dependants_net_income_kind() -> None:
    # Schedule 5 line 4 and ON428 line 15 read the same kind; here it is the field of a record.
    assert INFIRM_DEPENDANTS.fields[0] is DEPENDANT_NET_INCOME
    assert DEPENDANT_NET_INCOME.identifier == "ca/dependant_net_income"
    assert DEPENDANT_NET_INCOME.non_negative is True


def test_the_infirm_dependants_hold_a_net_income_each_in_the_callers_order() -> None:
    dependants = RecordList(
        INFIRM_DEPENDANTS.fields,
        [{DEPENDANT_NET_INCOME: Decimal("5000")}, {DEPENDANT_NET_INCOME: Decimal("25000")}],
    )

    assert [record[DEPENDANT_NET_INCOME] for record in dependants.records] == [
        Decimal("5000"),
        Decimal("25000"),
    ]


def test_the_caregiver_amount_is_a_non_negative_decimal(registry: ArtifactRegistry) -> None:
    # T1 line 82 (line 30450) "Canada caregiver amount for other infirm dependants age 18 or
    # older (complete Schedule 5)": the total of the allowable amounts, each at least "0".
    assert CAREGIVER_AMOUNT.identifier == "ca/caregiver_amount"
    assert CAREGIVER_AMOUNT.value_type is Decimal
    assert CAREGIVER_AMOUNT.non_negative is True
    assert registry.kind("ca/caregiver_amount") is CAREGIVER_AMOUNT


def test_the_other_dependants_are_a_record_list_of_expenses_and_net_income(
    registry: ArtifactRegistry,
) -> None:
    # Federal Worksheet, line 33199, "Complete one column for each dependant": line 1 "Medical
    # expenses for other dependant" and, for line 2, the dependant's net income. A list of its own:
    # the infirm dependants of line 30450 are a different set of people.
    assert isinstance(OTHER_DEPENDANTS, RecordListKind)
    assert OTHER_DEPENDANTS.identifier == "ca/other_dependants"
    assert OTHER_DEPENDANTS.value_type is RecordList
    assert OTHER_DEPENDANTS.fields == (OTHER_DEPENDANT_MEDICAL_EXPENSES, DEPENDANT_NET_INCOME)
    assert OTHER_DEPENDANTS is not INFIRM_DEPENDANTS
    assert registry.get("ca/other_dependants") is OTHER_DEPENDANTS


def test_the_other_dependants_list_reuses_the_dependants_net_income_kind() -> None:
    assert OTHER_DEPENDANTS.fields[1] is DEPENDANT_NET_INCOME


def test_the_other_dependants_hold_expenses_and_net_income_each_in_the_callers_order() -> None:
    dependants = RecordList(
        OTHER_DEPENDANTS.fields,
        [
            {
                OTHER_DEPENDANT_MEDICAL_EXPENSES: Decimal("3000"),
                DEPENDANT_NET_INCOME: Decimal("10000"),
            },
            {
                OTHER_DEPENDANT_MEDICAL_EXPENSES: Decimal("1000"),
                DEPENDANT_NET_INCOME: Decimal("40000"),
            },
        ],
    )

    assert [record[OTHER_DEPENDANT_MEDICAL_EXPENSES] for record in dependants.records] == [
        Decimal("3000"),
        Decimal("1000"),
    ]


def test_the_other_dependant_medical_expenses_are_a_non_negative_decimal(
    registry: ArtifactRegistry,
) -> None:
    # Federal Worksheet, line 33199, line 1 "Medical expenses for other dependant".
    assert OTHER_DEPENDANT_MEDICAL_EXPENSES.identifier == "ca/other_dependant_medical_expenses"
    assert OTHER_DEPENDANT_MEDICAL_EXPENSES.value_type is Decimal
    assert OTHER_DEPENDANT_MEDICAL_EXPENSES.non_negative is True
    assert registry.kind("ca/other_dependant_medical_expenses") is OTHER_DEPENDANT_MEDICAL_EXPENSES


def test_the_other_dependants_medical_is_a_non_negative_decimal(registry: ArtifactRegistry) -> None:
    # T1 line 33199 "Allowable amount of medical expenses for other dependants": the total of
    # each dependant's line 3, which is "0" when negative.
    assert OTHER_DEPENDANTS_MEDICAL.identifier == "ca/other_dependants_medical"
    assert OTHER_DEPENDANTS_MEDICAL.value_type is Decimal
    assert OTHER_DEPENDANTS_MEDICAL.non_negative is True
    assert registry.kind("ca/other_dependants_medical") is OTHER_DEPENDANTS_MEDICAL


def test_medical_expenses_is_a_non_negative_decimal(registry: ArtifactRegistry) -> None:
    # T1 line 107 and line 33099 "Medical expenses for self, spouse or common-law partner and
    # your dependent children under 18 years of age": a starting amount.
    assert MEDICAL_EXPENSES.identifier == "ca/medical_expenses"
    assert MEDICAL_EXPENSES.value_type is Decimal
    assert MEDICAL_EXPENSES.non_negative is True
    assert registry.kind("ca/medical_expenses") is MEDICAL_EXPENSES


def test_medical_net_income_share_is_a_non_negative_decimal(registry: ArtifactRegistry) -> None:
    # T1 line 108 "Amount from line 23600" "multiplied by 3%".
    assert MEDICAL_NET_INCOME_SHARE.identifier == "ca/medical_net_income_share"
    assert MEDICAL_NET_INCOME_SHARE.value_type is Decimal
    assert MEDICAL_NET_INCOME_SHARE.non_negative is True
    assert registry.kind("ca/medical_net_income_share") is MEDICAL_NET_INCOME_SHARE


def test_medical_threshold_is_a_non_negative_decimal(registry: ArtifactRegistry) -> None:
    # T1 line 109 "Enter whichever is less: $2,834 or the amount from line 108."
    assert MEDICAL_THRESHOLD.identifier == "ca/medical_threshold"
    assert MEDICAL_THRESHOLD.value_type is Decimal
    assert MEDICAL_THRESHOLD.non_negative is True
    assert registry.kind("ca/medical_threshold") is MEDICAL_THRESHOLD


def test_medical_expenses_over_threshold_is_a_non_negative_decimal(
    registry: ArtifactRegistry,
) -> None:
    # T1 line 110 "Line 107 minus line 109 (if negative, enter "0")".
    assert MEDICAL_EXPENSES_OVER_THRESHOLD.identifier == "ca/medical_expenses_over_threshold"
    assert MEDICAL_EXPENSES_OVER_THRESHOLD.value_type is Decimal
    assert MEDICAL_EXPENSES_OVER_THRESHOLD.non_negative is True
    assert registry.kind("ca/medical_expenses_over_threshold") is MEDICAL_EXPENSES_OVER_THRESHOLD


def test_medical_claim_is_a_non_negative_decimal(registry: ArtifactRegistry) -> None:
    # T1 line 112 and line 33200 "Line 110 plus line 111".
    assert MEDICAL_CLAIM.identifier == "ca/medical_claim"
    assert MEDICAL_CLAIM.value_type is Decimal
    assert MEDICAL_CLAIM.non_negative is True
    assert registry.kind("ca/medical_claim") is MEDICAL_CLAIM


def test_the_disability_dependants_are_a_record_list_of_the_worksheets_figures(
    registry: ArtifactRegistry,
) -> None:
    # Federal Worksheet "Line 31800", per dependant: whether they were "under 18 years of age on
    # December 31, 2025", line 3 "Total of child care and attendant care expenses for your
    # dependant that you or another person claimed", line 9 "amount from line 98 of your
    # dependant's return" and line 11 "Dependant's taxable income from line 26000 of their
    # return": the four fields a record holds, in the worksheet's line order (the caller lists
    # only the dependants who qualify, so there are no eligibility fields).
    assert RECORD_LISTS <= REGISTERED
    assert isinstance(DISABILITY_DEPENDANTS, RecordListKind)
    assert DISABILITY_DEPENDANTS.identifier == "ca/disability_dependants"
    assert DISABILITY_DEPENDANTS.value_type is RecordList
    assert DISABILITY_DEPENDANTS.non_negative is False
    assert DISABILITY_DEPENDANTS.fields == (
        DEPENDANT_UNDER_18,
        DEPENDANT_CARE_EXPENSES,
        DEPENDANT_CREDIT_AMOUNTS,
        DEPENDANT_TAXABLE_INCOME,
    )
    assert registry.get("ca/disability_dependants") is DISABILITY_DEPENDANTS


def test_the_disability_dependants_fields_are_kinds_of_their_own() -> None:
    assert DEPENDANT_UNDER_18.identifier == "ca/dependant_under_18"
    assert DEPENDANT_CARE_EXPENSES.identifier == "ca/dependant_care_expenses"
    assert DEPENDANT_CREDIT_AMOUNTS.identifier == "ca/dependant_credit_amounts"
    assert DEPENDANT_TAXABLE_INCOME.identifier == "ca/dependant_taxable_income"
    # Not the net income of line 30400's dependant: another figure of another return.
    assert DEPENDANT_NET_INCOME not in DISABILITY_DEPENDANTS.fields
    for kind in DISABILITY_DEPENDANTS.fields:
        assert kind.non_negative is True, kind.identifier


def test_the_dependant_under_18_is_a_non_negative_int_count(registry: ArtifactRegistry) -> None:
    # "If the dependant was under 18 years of age on December 31, 2025, ...": a yes or no, taken
    # as a count of 0 or 1 like the forms' other yes or no questions.
    assert DEPENDANT_UNDER_18.value_type is int
    assert DEPENDANT_UNDER_18.non_negative is True
    assert registry.kind("ca/dependant_under_18") is DEPENDANT_UNDER_18


@pytest.mark.parametrize(
    "kind", [DEPENDANT_CARE_EXPENSES, DEPENDANT_CREDIT_AMOUNTS, DEPENDANT_TAXABLE_INCOME]
)
def test_the_disability_dependants_amounts_are_non_negative_decimals(
    kind: ArtifactKind[Decimal], registry: ArtifactRegistry
) -> None:
    assert kind.value_type is Decimal
    assert kind.non_negative is True
    assert registry.kind(kind.identifier) is kind


def disability_record(**changes: object) -> dict[ArtifactKind[Any], object]:
    """One dependant aged 20 with the ticket's chosen figures, with `changes` by field name."""
    record: dict[ArtifactKind[Any], object] = {
        DEPENDANT_UNDER_18: 0,
        DEPENDANT_CARE_EXPENSES: Decimal("0"),
        DEPENDANT_CREDIT_AMOUNTS: Decimal("16129"),
        DEPENDANT_TAXABLE_INCOME: Decimal("20000"),
    }
    names: dict[str, ArtifactKind[Any]] = {
        "under_18": DEPENDANT_UNDER_18,
        "care_expenses": DEPENDANT_CARE_EXPENSES,
        "credit_amounts": DEPENDANT_CREDIT_AMOUNTS,
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
            disability_record(under_18=1, care_expenses=Decimal("5000"), credit_amounts=Decimal(0)),
        ],
    )

    assert [record[DEPENDANT_UNDER_18] for record in dependants.records] == [0, 1]
    assert [record[DEPENDANT_CARE_EXPENSES] for record in dependants.records] == [
        Decimal("0"),
        Decimal("5000"),
    ]
    assert [record[DEPENDANT_CREDIT_AMOUNTS] for record in dependants.records] == [
        Decimal("16129"),
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
        DEPENDANT_CREDIT_AMOUNTS,
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
    del record[DEPENDANT_TAXABLE_INCOME]

    with pytest.raises(
        InvalidRecordError, match="item 2: missing field ca/dependant_taxable_income"
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
        ({"credit_amounts": Decimal("-1")}, "ca/dependant_credit_amounts"),
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
        {"credit_amounts": "16129"},
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
    # T1 line 100 (line 31800) "Disability amount transferred from a dependant (use Federal
    # Worksheet)": the total of the worksheet's line 13 amounts, each the lesser of two amounts
    # that are at least "0".
    assert DISABILITY_TRANSFERRED_AMOUNT.identifier == "ca/disability_transferred_amount"
    assert DISABILITY_TRANSFERRED_AMOUNT.value_type is Decimal
    assert DISABILITY_TRANSFERRED_AMOUNT.non_negative is True
    assert registry.kind("ca/disability_transferred_amount") is DISABILITY_TRANSFERRED_AMOUNT


def test_the_principal_residence_properties_are_a_record_list_of_the_forms_input_lines(
    registry: ArtifactRegistry,
) -> None:
    # Form T2091(IND), per property ("Complete a separate form for each property you sold."):
    # line 1 and line 2 the years designated "After 1981" and "After 1971 and before 1982", line 5
    # and line 6 the years owned in the same periods, line 8 "Proceeds of disposition or deemed
    # disposition", line 9 "Outlays and expenses made or incurred related to the disposition",
    # line 10 "Adjusted cost base at the time of disposition", and whether the "plus one" rule
    # applies: the fields a record holds, in the form's line order (lines 3, 4, 7 and 14 onward
    # are worked out).
    assert RECORD_LISTS <= REGISTERED
    assert isinstance(PRINCIPAL_RESIDENCE_PROPERTIES, RecordListKind)
    assert PRINCIPAL_RESIDENCE_PROPERTIES.identifier == "ca/principal_residence_properties"
    assert PRINCIPAL_RESIDENCE_PROPERTIES.value_type is RecordList
    assert PRINCIPAL_RESIDENCE_PROPERTIES.non_negative is False
    assert PRINCIPAL_RESIDENCE_PROPERTIES.fields == (
        RESIDENCE_YEARS_DESIGNATED_AFTER_1981,
        RESIDENCE_YEARS_DESIGNATED_1972_TO_1981,
        RESIDENCE_YEARS_OWNED_AFTER_1981,
        RESIDENCE_YEARS_OWNED_1972_TO_1981,
        RESIDENCE_PROCEEDS,
        RESIDENCE_OUTLAYS,
        RESIDENCE_ADJUSTED_COST_BASE,
        RESIDENCE_PLUS_ONE_YEAR,
    )
    assert registry.get("ca/principal_residence_properties") is PRINCIPAL_RESIDENCE_PROPERTIES


def test_the_principal_residence_properties_fields_are_kinds_of_their_own() -> None:
    assert RESIDENCE_YEARS_DESIGNATED_AFTER_1981.identifier == (
        "ca/residence_years_designated_after_1981"
    )
    assert RESIDENCE_YEARS_DESIGNATED_1972_TO_1981.identifier == (
        "ca/residence_years_designated_1972_to_1981"
    )
    assert RESIDENCE_YEARS_OWNED_AFTER_1981.identifier == "ca/residence_years_owned_after_1981"
    assert RESIDENCE_YEARS_OWNED_1972_TO_1981.identifier == (
        "ca/residence_years_owned_1972_to_1981"
    )
    assert RESIDENCE_PROCEEDS.identifier == "ca/residence_proceeds"
    assert RESIDENCE_OUTLAYS.identifier == "ca/residence_outlays"
    assert RESIDENCE_ADJUSTED_COST_BASE.identifier == "ca/residence_adjusted_cost_base"
    assert RESIDENCE_PLUS_ONE_YEAR.identifier == "ca/residence_plus_one_year"
    for kind in PRINCIPAL_RESIDENCE_PROPERTIES.fields:
        assert kind.non_negative is True, kind.identifier


@pytest.mark.parametrize(
    "kind",
    [
        RESIDENCE_YEARS_DESIGNATED_AFTER_1981,
        RESIDENCE_YEARS_DESIGNATED_1972_TO_1981,
        RESIDENCE_YEARS_OWNED_AFTER_1981,
        RESIDENCE_YEARS_OWNED_1972_TO_1981,
        RESIDENCE_PLUS_ONE_YEAR,
    ],
)
def test_the_residence_years_and_the_plus_one_are_non_negative_int_counts(
    kind: ArtifactKind[int], registry: ArtifactRegistry
) -> None:
    # Lines 1, 2, 5 and 6 are numbers of tax years; the "plus one" is a yes or no, taken as a count
    # of 0 or 1 like the forms' other yes or no questions.
    assert kind.value_type is int
    assert kind.non_negative is True
    assert registry.kind(kind.identifier) is kind


@pytest.mark.parametrize(
    "kind", [RESIDENCE_PROCEEDS, RESIDENCE_OUTLAYS, RESIDENCE_ADJUSTED_COST_BASE]
)
def test_the_residence_amounts_are_non_negative_decimals(
    kind: ArtifactKind[Decimal], registry: ArtifactRegistry
) -> None:
    assert kind.value_type is Decimal
    assert kind.non_negative is True
    assert registry.kind(kind.identifier) is kind


def residence_record(**changes: object) -> dict[ArtifactKind[Any], object]:
    """One property with the ticket's example figures, with `changes` by field name."""
    record: dict[ArtifactKind[Any], object] = {
        RESIDENCE_YEARS_DESIGNATED_AFTER_1981: 6,
        RESIDENCE_YEARS_DESIGNATED_1972_TO_1981: 0,
        RESIDENCE_YEARS_OWNED_AFTER_1981: 10,
        RESIDENCE_YEARS_OWNED_1972_TO_1981: 0,
        RESIDENCE_PROCEEDS: Decimal("400000"),
        RESIDENCE_OUTLAYS: Decimal("5000"),
        RESIDENCE_ADJUSTED_COST_BASE: Decimal("95000"),
        RESIDENCE_PLUS_ONE_YEAR: 1,
    }
    names: dict[str, ArtifactKind[Any]] = {
        "designated_after_1981": RESIDENCE_YEARS_DESIGNATED_AFTER_1981,
        "designated_1972_to_1981": RESIDENCE_YEARS_DESIGNATED_1972_TO_1981,
        "owned_after_1981": RESIDENCE_YEARS_OWNED_AFTER_1981,
        "owned_1972_to_1981": RESIDENCE_YEARS_OWNED_1972_TO_1981,
        "proceeds": RESIDENCE_PROCEEDS,
        "outlays": RESIDENCE_OUTLAYS,
        "adjusted_cost_base": RESIDENCE_ADJUSTED_COST_BASE,
        "plus_one": RESIDENCE_PLUS_ONE_YEAR,
    }
    for name, value in changes.items():
        record[names[name]] = value
    return record


def test_the_principal_residence_properties_hold_the_eight_figures_each_in_the_callers_order() -> (
    None
):
    properties = RecordList(
        PRINCIPAL_RESIDENCE_PROPERTIES.fields,
        [
            residence_record(),
            residence_record(
                designated_after_1981=2,
                designated_1972_to_1981=3,
                owned_after_1981=6,
                owned_1972_to_1981=4,
                proceeds=Decimal("500000"),
                outlays=Decimal("0"),
                plus_one=0,
            ),
        ],
    )

    assert [record[RESIDENCE_YEARS_DESIGNATED_AFTER_1981] for record in properties.records] == [
        6,
        2,
    ]
    assert [record[RESIDENCE_YEARS_DESIGNATED_1972_TO_1981] for record in properties.records] == [
        0,
        3,
    ]
    assert [record[RESIDENCE_YEARS_OWNED_AFTER_1981] for record in properties.records] == [10, 6]
    assert [record[RESIDENCE_YEARS_OWNED_1972_TO_1981] for record in properties.records] == [0, 4]
    assert [record[RESIDENCE_PROCEEDS] for record in properties.records] == [
        Decimal("400000"),
        Decimal("500000"),
    ]
    assert [record[RESIDENCE_OUTLAYS] for record in properties.records] == [
        Decimal("5000"),
        Decimal("0"),
    ]
    assert [record[RESIDENCE_ADJUSTED_COST_BASE] for record in properties.records] == [
        Decimal("95000"),
        Decimal("95000"),
    ]
    assert [record[RESIDENCE_PLUS_ONE_YEAR] for record in properties.records] == [1, 0]


def test_there_may_be_no_principal_residence_properties() -> None:
    assert RecordList(PRINCIPAL_RESIDENCE_PROPERTIES.fields, []).records == ()


@pytest.mark.parametrize("missing", PRINCIPAL_RESIDENCE_PROPERTIES.fields)
def test_a_property_missing_a_figure_is_an_invalid_record(missing: ArtifactKind[Any]) -> None:
    record = residence_record()
    del record[missing]

    with pytest.raises(InvalidRecordError, match=f"item 1: missing field {missing.identifier}"):
        RecordList(PRINCIPAL_RESIDENCE_PROPERTIES.fields, [record])


def test_the_second_property_is_named_by_its_position() -> None:
    record = residence_record()
    del record[RESIDENCE_PROCEEDS]

    with pytest.raises(InvalidRecordError, match="item 2: missing field ca/residence_proceeds"):
        RecordList(PRINCIPAL_RESIDENCE_PROPERTIES.fields, [residence_record(), record])


def test_a_property_with_another_figure_is_an_invalid_record() -> None:
    record = residence_record()
    record[CAPITAL_GAIN] = Decimal("300000")

    with pytest.raises(InvalidRecordError, match="item 1: unknown field ca/capital_gain"):
        RecordList(PRINCIPAL_RESIDENCE_PROPERTIES.fields, [record])


@pytest.mark.parametrize(
    ("change", "identifier"),
    [
        ({"designated_after_1981": -1}, "ca/residence_years_designated_after_1981"),
        ({"designated_1972_to_1981": -1}, "ca/residence_years_designated_1972_to_1981"),
        ({"owned_after_1981": -1}, "ca/residence_years_owned_after_1981"),
        ({"owned_1972_to_1981": -1}, "ca/residence_years_owned_1972_to_1981"),
        ({"proceeds": Decimal("-0.01")}, "ca/residence_proceeds"),
        ({"outlays": Decimal("-1")}, "ca/residence_outlays"),
        ({"adjusted_cost_base": Decimal("-1")}, "ca/residence_adjusted_cost_base"),
        ({"plus_one": -1}, "ca/residence_plus_one_year"),
    ],
)
def test_a_negative_property_figure_is_refused(change: dict[str, object], identifier: str) -> None:
    with pytest.raises(NegativeArtifactError, match=f"item 1: {identifier} cannot be negative"):
        RecordList(PRINCIPAL_RESIDENCE_PROPERTIES.fields, [residence_record(**change)])


@pytest.mark.parametrize(
    "change",
    [
        {"designated_after_1981": Decimal("6")},
        {"owned_after_1981": True},
        {"owned_1972_to_1981": 1.0},
        {"plus_one": Decimal("1")},
        {"proceeds": 400000},
        {"outlays": "5000"},
        {"adjusted_cost_base": 95000.0},
    ],
)
def test_a_property_figure_of_the_wrong_type_is_refused(change: dict[str, object]) -> None:
    with pytest.raises(TypeError):
        RecordList(PRINCIPAL_RESIDENCE_PROPERTIES.fields, [residence_record(**change)])


def test_the_principal_residence_gain_is_a_non_negative_decimal(registry: ArtifactRegistry) -> None:
    # Form T2091(IND) Part 3 line 54 "Total capital gain": line 24 "Line 18 minus line 23 (if
    # negative, enter "0")" for each property, totalled here.
    assert PRINCIPAL_RESIDENCE_GAIN.identifier == "ca/principal_residence_gain"
    assert PRINCIPAL_RESIDENCE_GAIN.value_type is Decimal
    assert PRINCIPAL_RESIDENCE_GAIN.non_negative is True
    assert registry.kind("ca/principal_residence_gain") is PRINCIPAL_RESIDENCE_GAIN


def test_the_special_tax_and_credit_lines_are_non_negative(registry: ArtifactRegistry) -> None:
    # T1 lines 131, 41300, 41400, 41500 and 41800 and the forms behind them (T2038(IND) Part C,
    # T1172 Parts A and B, the RC210 box 10 and the RL-10 slip) print amounts of tax, credit or
    # expenditure with no negative figure; the lines that carry or subtract them print a floor
    # or cannot be negative: line 132 adds line 131 to line 126, line 139 is "if negative, enter
    # "0"" and T1172's line 3 is the lesser of two such amounts, line 8 is line 1 less a line 7
    # that is at most line 1.
    for kind in (
        ITC_RECAPTURE_EXPENDITURE_AT_15_PERCENT,
        ITC_RECAPTURE_EXPENDITURE_AT_20_PERCENT,
        LABOUR_SPONSORED_FUNDS_NET_COST,
        ADVANCED_CANADA_WORKERS_BENEFIT,
        RESP_AIPS_RECEIVED_PART_A,
        RESP_AIPS_RRSP_CONTRIBUTIONS,
        RESP_AIPS_REDUCTION_USED_IN_PREVIOUS_YEARS,
        RESP_AIPS_RECEIVED_PART_B,
        RL_10_LABOUR_SPONSORED_FUND_AMOUNT,
        POLITICAL_CONTRIBUTIONS,
        ITC_RECAPTURE_AT_15_PERCENT,
        ITC_RECAPTURE_AT_20_PERCENT,
        ITC_RECAPTURE,
        FEDERAL_TAX_WITH_ITC_RECAPTURE,
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
        POLITICAL_CREDIT_CHOSEN_COLUMN,
        POLITICAL_CREDIT_SHORTCUT_THRESHOLD,
        POLITICAL_CREDIT_SHORTCUT_AMOUNT,
        POLITICAL_CREDIT_BEFORE_MAXIMUM,
        POLITICAL_CREDIT,
        LABOUR_SPONSORED_FUNDS_CREDIT_BEFORE_MAXIMUM,
        LABOUR_SPONSORED_FUNDS_CREDIT,
        CREDITS_AGAINST_FEDERAL_TAX,
        FEDERAL_TAX_LESS_CREDITS,
        RESP_AIPS_CONTRIBUTIONS_COUNTED,
        RESP_AIPS_LIFETIME_LIMIT,
        RESP_AIPS_SUBJECT_TO_TAX,
        RESP_AIPS_PART_A_TAX,
        RESP_AIPS_PART_B_TAX,
        RESP_AIPS_ADDITIONAL_TAX,
        SPECIAL_TAXES,
    ):
        assert kind.value_type is Decimal, kind.identifier
        assert kind.non_negative is True, kind.identifier
        assert registry.kind(kind.identifier).non_negative is True, kind.identifier


def test_the_t1172_lines_that_print_no_floor_are_signed(registry: ArtifactRegistry) -> None:
    # Form T1172 Part A: line 6 "Line 4 minus line 5" and line 7 "Amount from line 3 or 6, whichever
    # is less" print no "(if negative, enter "0")", so line 5 above 50,000.00 would make them
    # negative, as the form prints; line 8 "line 1 minus line 7" is never negative as line 7 is at
    # most line 3, which is at most line 1.
    assert RESP_AIPS_LIMIT_REMAINING.non_negative is False
    assert RESP_AIPS_REDUCTION.non_negative is False
    assert registry.kind("ca/resp_aips_limit_remaining").non_negative is False
    assert registry.kind("ca/resp_aips_reduction").non_negative is False
    assert RESP_AIPS_CONTRIBUTIONS_COUNTED.non_negative is True
    assert RESP_AIPS_SUBJECT_TO_TAX.non_negative is True


def test_the_t1172_part_a_count_is_a_non_negative_int() -> None:
    # Form T1172 "Part B - Fill out this part only if Part A does not apply to you": a caller's 0
    # (Part B) or 1 (Part A) count, as the other 0 or 1 counts of the forms.
    assert RESP_AIPS_PART_A_APPLIES.value_type is int
    assert RESP_AIPS_PART_A_APPLIES.non_negative is True
