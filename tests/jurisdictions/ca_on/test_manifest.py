"""The CA-ON manifest: what it selects, and that production code builds it into a composition.

Building it through `TaxComputationService.compose` resolves every slot: each capability name to a
registered class, each parameter slot's family to a dataset of the slot's kind for the tax year,
and each artifact identifier to a registered kind of the slot's value type.
"""

from __future__ import annotations

import app.registrations  # lists the packages; build_tax_computation registers their catalogs
from app.adapters.outbound.yaml_jurisdictions import YamlJurisdictionSource
from app.application.services.tax_computation import TaxComputationService
from app.domain.capabilities.apply_fraction import ApplyFraction
from app.domain.capabilities.apply_rate import ApplyRate
from app.domain.capabilities.at_most import AtMost
from app.domain.capabilities.capped_amount import CappedAmount
from app.domain.capabilities.choose_by_count import ChooseByCount
from app.domain.capabilities.contribution_tier import TieredContribution
from app.domain.capabilities.credit_amount import CreditAmount
from app.domain.capabilities.lesser_of import LesserOf
from app.domain.capabilities.multiple_over import MultipleOver
from app.domain.capabilities.per_unit_amount import PerUnitAmount
from app.domain.capabilities.progressive_tax import ProgressiveTax
from app.domain.capabilities.subtract import Subtract
from app.domain.capabilities.subtract_not_below_zero import SubtractNotBelowZero
from app.domain.capabilities.sum import Sum
from app.domain.capabilities.tapered_amount import TaperedAmount
from app.domain.capabilities.tiered_surcharge import TieredSurcharge
from app.domain.capabilities.times_count import TimesCount
from app.domain.jurisdiction_code import JurisdictionCode
from app.domain.manifest import CapabilitySelection, Manifest
from app.jurisdictions.ca.capabilities.caregiver_amount import CaregiverAmount
from app.jurisdictions.ca.capabilities.disability_transfer_amount import DisabilityTransferAmount
from app.jurisdictions.ca.capabilities.other_dependants_medical import OtherDependantsMedical
from app.jurisdictions.ca.catalog import (
    ADDITIONAL_DEDUCTIONS,
    ADJUSTED_FAMILY_NET_INCOME,
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
    DEPENDANT_NET_INCOME,
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
    FEDERAL_TAX_AFTER_CREDITS,
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
    PROVINCIAL_CREDITS,
    RDSP_INCOME,
    RDSP_INCOME_REPAYMENT,
    REFUND,
    REFUND_OR_BALANCE_OWING,
    REGULAR_RATE_DONATION_CREDIT,
    REGULAR_RATE_DONATIONS,
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
    UNION_DUES,
    UNIVERSAL_CHILD_CARE_BENEFIT,
    UNIVERSITY_DONATIONS_OUTSIDE_CANADA,
    UNUSED_RRSP_CONTRIBUTIONS,
    UNUSED_RRSP_CONTRIBUTIONS_CARRIED_FORWARD,
    WORKERS_COMPENSATION_BENEFITS,
    WORKING_INCOME,
)
from app.jurisdictions.ca_on import catalog as ontario
from app.jurisdictions.ca_on.capabilities.caregiver_amount import OntarioCaregiverAmount
from app.jurisdictions.ca_on.capabilities.choose_by_range import ChooseByRange
from app.jurisdictions.ca_on.capabilities.coop_education_credit import CoopEducationCredit
from app.jurisdictions.ca_on.capabilities.flow_through_share_expenses import (
    FlowThroughShareExpenses,
)
from app.jurisdictions.ca_on.capabilities.quotient import Quotient
from app.jurisdictions.ca_on.capabilities.record_count import RecordCount
from app.jurisdictions.ca_on.catalog import (
    CAREGIVER_DEPENDANTS,
    COMMUNITY_FOOD_PROGRAM_CREDIT,
    COMMUNITY_FOOD_PROGRAM_DONATIONS,
    COOP_EDUCATION_CREDIT,
    COOP_EDUCATION_FULL_SHARE,
    COOP_EDUCATION_PAYROLL,
    COOP_EDUCATION_PAYROLL_OVER_THRESHOLD,
    COOP_EDUCATION_PAYROLL_RANGE,
    COOP_EDUCATION_PAYROLL_THRESHOLD,
    COOP_EDUCATION_PHASE_OUT_SHARE,
    COOP_EDUCATION_PLACEMENT_COUNT,
    COOP_EDUCATION_PLACEMENTS,
    COOP_EDUCATION_REMAINING_SHARE,
    DEPENDANTS,
    DEPENDENT_CHILDREN,
    ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_MAXIMUM,
    ELIGIBLE_DEPENDANT_BASE,
    FERTILITY_CREDIT,
    FERTILITY_CREDIT_BEFORE_MAXIMUM,
    FERTILITY_EXPENSES,
    FLOW_THROUGH_SHARE_CREDIT,
    FLOW_THROUGH_SHARE_EXPENSES,
    FLOW_THROUGH_SHARE_SLIPS,
    LIFT_CREDIT,
    LIFT_CREDIT_BEFORE_MAXIMUM,
    LIFT_MAXIMUM_CREDIT,
    LIFT_REDUCTION,
    ONTARIO_BASIC_TAX,
    ONTARIO_CREDITS,
    ONTARIO_CREDITS_SUBTOTAL,
    ONTARIO_HEALTH_PREMIUM,
    ONTARIO_SURTAX,
    ONTARIO_TAX,
    ONTARIO_TAX_AFTER_CREDITS,
    ONTARIO_TAX_AFTER_DIVIDEND_CREDIT,
    ONTARIO_TAX_AFTER_FOOD_CREDIT,
    ONTARIO_TAX_AFTER_LIFT_CREDIT,
    ONTARIO_TAX_AFTER_REDUCTION,
    ONTARIO_TAX_BEFORE_DIVIDEND_CREDIT,
    ONTARIO_TAX_LESS_DIVIDEND_CREDIT,
    ONTARIO_TAX_REDUCTION,
    ONTARIO_TAX_WITH_SURTAX,
    SENIORS_TRANSIT_AMOUNT_PAID_AT_MOST_MAXIMUM,
    SENIORS_TRANSIT_CREDIT,
    SENIORS_TRANSIT_PAID,
    TAX_REDUCTION_AMOUNTS,
    TAX_REDUCTION_BASIC,
    TAX_REDUCTION_FOR_CHILDREN,
    TAX_REDUCTION_FOR_DEPENDANTS,
)
from app.main import build_tax_computation

ROOTS = app.registrations.JURISDICTIONS.roots()
CA_ON = JurisdictionCode("CA-ON")


def manifest() -> Manifest:
    (only,) = YamlJurisdictionSource(ROOTS).get_jurisdiction(CA_ON).manifests
    return only


def service() -> TaxComputationService:
    return build_tax_computation()


def test_ca_on_has_one_manifest_from_2025() -> None:
    found = manifest()

    assert found.jurisdiction == CA_ON
    assert found.version == 1
    assert found.valid_from_tax_year == 2025
    assert found.inputs == frozenset(
        {
            "ca/employment_income",
            "ca/capital_gain",
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
            "ca/t3_investment_income",
            "ca/t5_investment_income",
            "ca/t5013_investment_income",
            "ca/investment_income_credited_not_received",
            "ca/tax_refund_interest",
            "ca/foreign_investment_income",
            "ca/investment_income_without_a_slip",
            "ca/investment_royalties",
            "ca/investment_income_reported_in_previous_years",
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
            "ca/uccb_repayment",
            "ca/rdsp_income_repayment",
            "ca/canadian_armed_forces_and_police_deduction",
            "ca/security_options_deductions",
            "ca/limited_partnership_losses_of_other_years",
            "ca/non_capital_losses_of_other_years",
            "ca/additional_deductions",
            "ca/other_payments_deduction_above_limit",
            "ca/other_payments_worksheet_required",
            "ca/other_payments_worksheet_line_9_over_limit",
            "ca/unused_rrsp_contributions",
            "ca/rrsp_contributions",
            "ca/rrsp_deduction_limit",
            "ca/rrsp_amount_deducted",
            "ca/union_dues",
            "ca/rpp_deduction",
            "ca/elected_split_pension_deduction",
            "ca/support_payments_deduction",
            "ca/exploration_and_development_expenses",
            "ca/other_deductions",
            "ca/total_carrying_charges",
            "ca/total_interest_expenses",
            "ca/total_other_expenses",
            "ca/capital_gains_deductions_1985_to_1987",
            "ca/capital_gains_deductions_1988_and_1989_other_than_eligible_capital_property",
            "ca/capital_gains_deductions_1988_and_1989_eligible_capital_property",
            "ca/capital_gains_deductions_1990_to_1999",
            "ca/capital_gains_deductions_2000",
            "ca/capital_gains_deductions_2001_to_2024",
            "ca/other_business_investment_loss_reductions_1986_to_1994",
            "ca/other_business_investment_loss_reductions_1994_to_1996",
            "ca/other_business_investment_loss_reductions_1997_to_1999",
            "ca/other_business_investment_loss_reductions_2000",
            "ca/other_business_investment_loss_reductions_2001_to_2023",
            "ca/other_business_investment_loss_reductions_2024",
            "ca/business_investment_loss",
            "ca/fhsa_contributions_in_2025",
            "ca/fhsa_contributions_in_2025_after_first_qualifying_withdrawal",
            "ca/fhsa_variable_b_amount",
            "ca/fhsa_designated_withdrawals_in_2025",
            "ca/fhsa_contributions_in_2024",
            "ca/fhsa_contributions_in_2024_before_first_qualifying_withdrawal",
            "ca/fhsa_carryforward_for_2025",
            "ca/fhsa_rrsp_transfers_in_2024_and_prior_years",
            "ca/fhsa_rrsp_transfers_in_2025",
            "ca/fhsa_designated_transfers_in_2024_and_prior_years",
            "ca/fhsa_designated_transfers_in_2025",
            "ca/fhsa_variable_h_amount",
            "ca/fhsa_carryforward_for_2024",
            "ca/fhsa_variable_f_amount",
            "ca/fhsa_annual_limits_for_2024_and_prior_years",
            "ca/fhsa_deductions_for_2024_and_prior_years",
            "ca/fhsa_unused_contributions_brought_forward",
            "ca/fhsa_contributions_deducted",
            "ca/fhsa_maximum_participation_period_ended",
            "ca-on/dependent_children",
            "ca-on/dependants",
            "ca/eligible_dependants",
            "ca/dependant_net_income",
            "ca/infirm_dependants",
            "ca/medical_expenses",
            "ca/other_dependants",
            "ca-on/caregiver_dependants",
            "ca/disability_dependants",
            "ca/infirm_children",
            "ca/born_in_1960_or_earlier",
            "ca/spouse_net_income",
            "ca/spouses_claimed",
            "ca/spouse_caregiver_eligible",
            "ca/child_care_expenses_paid",
            "ca/children_under_seven",
            "ca/children_with_disability",
            "ca/children_seven_to_sixteen",
            "ca/cwb_eligible_dependants",
            "ca/income_tax_deducted",
            "ca/part_xii_2_tax_credit",
            "ca/employee_and_partner_gst_hst_rebate",
            "ca/educator_supplies_expenses",
            "ca/journalism_labour_tax_credit",
            "ca/tax_paid_by_instalments",
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
            "ca-on/opportunities_fund_donation",
            "ca-on/fertility_expenses",
            "ca-on/seniors_transit_paid",
            "ca-on/flow_through_share_slips",
            "ca-on/coop_education_payroll",
            "ca-on/coop_education_placements",
            "ca-on/community_food_program_donations",
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
            "ca-on/political_contributions",
        }
    )
    # T1 line 167, the refund or balance owing, Schedule 7 line 23, what the return produces for
    # the next year's line 1, line 12010, the amount of dividends other than eligible, which
    # nothing else on the return reads; the Federal Worksheet's "Line 25000 - Other payments
    # deduction" line 9 "Line 5 plus line 8 =", which nothing consumes while the count of line 9
    # over $93,454 is a starting count; and ON428 line 58, the Ontario tax less the dividend tax
    # credit, which nothing else on the return reads (the surtax and line 69 read line 53; line
    # 60, the minimum tax carryover, is not modelled); T1 line 54 (line 23400) "Net income before
    # adjustments", which nothing reads while line 23500 is not wired (the floored net income of
    # line 56 is the next line of the chain); Schedule 15 line 58, what the return produces
    # for the next year's line 52; the Ontario opportunities fund's line 3 (line 46600) "Net
    # refund (line 1 minus line 2)", which nothing reads (line 48400, the refund, is read by that
    # page's line 1, so it is not a line the computation returns); and ON479 line 63260, the
    # number of eligible work placements, which nothing else reads: the lines the computation
    # returns.
    assert found.outputs == frozenset(
        {
            "ca/refund_or_balance_owing",
            "ca-on/net_refund",
            "ca/unused_rrsp_contributions_carried_forward",
            "ca/net_income_before_adjustments",
            "ca/fhsa_unused_contributions_carried_forward",
            "ca/taxable_dividends_other_than_eligible",
            "ca/other_payments_limit_income",
            "ca-on/ontario_tax_less_dividend_credit",
            "ca-on/coop_education_placement_count",
        }
    )
    # List order carries no meaning: the composition derives the run order from the contracts.
    assert set(found.capabilities) == {
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca/capital_gains_inclusion_rate"},
            consumes={"base": "ca/capital_gain"},
            produces={"output": "ca/taxable_capital_gains"},
        ),
        # T1 line 9 (12000) "Amount of dividends (eligible and other than eligible)" and line
        # 12010 "Amount of dividends (other than eligible)" (use Federal Worksheet): the Federal
        # Worksheet's "Lines 12000 and 12010 - Taxable amount of dividends from taxable Canadian
        # corporations", line 5 "Add lines 1 to 4. Enter this amount on line 12010 of your
        # return." (the T3, T4PS, T5 and T5013 slip boxes of lines 1 to 4) and line 10 "Add lines
        # 6 to 9. Enter this amount on line 12000 of your return." (lines 6 to 9). For dividends
        # with no information slip, line 11 "Actual amount of eligible dividends received" and
        # line 12 "Applicable rate 138%" give line 13 "Line 11 multiplied by the percentage from
        # line 12"; line 14 "Actual amount of dividends other than eligible dividends received"
        # and line 15 "Applicable rate 115%" give line 16 "Line 14 multiplied by the percentage
        # from line 15 Include this amount on line 12010 of your return."; line 17 "Line 13 plus
        # line 16. Include this amount on line 12000 of your return." The rates are above one, so
        # they are fractions, not rates. Line 12010 is line 5 plus line 16 and line 12000 is line
        # 10 plus line 17.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/t3_taxable_dividends_other_than_eligible",
                    "ca/t4ps_taxable_dividends_other_than_eligible",
                    "ca/t5_taxable_dividends_other_than_eligible",
                    "ca/t5013_taxable_dividends_other_than_eligible",
                )
            },
            produces={"output": "ca/slip_taxable_dividends_other_than_eligible"},
        ),
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/t3_taxable_dividends",
                    "ca/t4ps_taxable_dividends",
                    "ca/t5_taxable_dividends",
                    "ca/t5013_taxable_dividends",
                )
            },
            produces={"output": "ca/slip_taxable_dividends"},
        ),
        CapabilitySelection(
            name="core/apply_fraction",
            params={"fraction": "ca/eligible_dividend_gross_up"},
            consumes={"base": "ca/eligible_dividends_received_without_a_slip"},
            produces={"output": "ca/eligible_dividends_grossed_up"},
        ),
        CapabilitySelection(
            name="core/apply_fraction",
            params={"fraction": "ca/other_dividend_gross_up"},
            consumes={"base": "ca/other_dividends_received_without_a_slip"},
            produces={"output": "ca/other_dividends_grossed_up"},
        ),
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": ("ca/eligible_dividends_grossed_up", "ca/other_dividends_grossed_up")
            },
            produces={"output": "ca/dividends_without_a_slip_grossed_up"},
        ),
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/slip_taxable_dividends_other_than_eligible",
                    "ca/other_dividends_grossed_up",
                )
            },
            produces={"output": "ca/taxable_dividends_other_than_eligible"},
        ),
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": ("ca/slip_taxable_dividends", "ca/dividends_without_a_slip_grossed_up")
            },
            produces={"output": "ca/taxable_dividends"},
        ),
        # T1 Step 2 line 10 (12100) "Interest and other investment income (use Federal
        # Worksheet)": the Federal Worksheet's "Line 12100 - Interest and other investment
        # income" line 9 "Add lines 1 to 8.", in line order, then line 11 "Line 9 minus line
        # 10. Enter this amount on line 12100 of your return." with line 10 "Interest and other
        # investment income, included on line 9, received and reported in previous years".
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/t3_investment_income",
                    "ca/t5_investment_income",
                    "ca/t5013_investment_income",
                    "ca/investment_income_credited_not_received",
                    "ca/tax_refund_interest",
                    "ca/foreign_investment_income",
                    "ca/investment_income_without_a_slip",
                    "ca/investment_royalties",
                )
            },
            produces={"output": "ca/investment_income_before_prior_years"},
        ),
        CapabilitySelection(
            name="core/subtract",
            params={},
            consumes={
                "amount": "ca/investment_income_before_prior_years",
                "less": "ca/investment_income_reported_in_previous_years",
            },
            produces={"output": "ca/interest_and_other_investment_income"},
        ),
        # T1 line 32 and line 14700 "Add lines 29 to 31 (see line 25000 in Step 4).": workers'
        # compensation benefits (14400), social assistance payments (14500) and net federal
        # supplements paid (14600), in line order.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/workers_compensation_benefits",
                    "ca/social_assistance_payments",
                    "ca/net_federal_supplements",
                )
            },
            produces={"output": "ca/income_support_benefits"},
        ),
        # T1 line 33 and line 15000 "Line 28 plus line 32 Total income": every income line the
        # return lists, in line order (lines 1 to 20, here with the amount of dividends of line
        # 9 (12000), the taxable capital gains of line 14 and the taxable support payments of
        # line 15, then line 32); rental income (line 13) and self-employment income (lines 22
        # to 26) are not wired yet.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/employment_income",
                    "ca/other_employment_income",
                    "ca/old_age_security",
                    "ca/cpp_or_qpp_benefits",
                    "ca/other_pensions_and_superannuation",
                    "ca/elected_split_pension_amount",
                    "ca/universal_child_care_benefit",
                    "ca/ei_and_other_benefits",
                    "ca/taxable_dividends",
                    "ca/interest_and_other_investment_income",
                    "ca/net_partnership_income",
                    "ca/rdsp_income",
                    "ca/taxable_capital_gains",
                    "ca/taxable_support_payments",
                    "ca/rrsp_income",
                    "ca/fhsa_income",
                    "ca/other_fhsa_income",
                    "ca/other_income",
                    "ca/taxable_scholarships",
                    "ca/income_support_benefits",
                )
            },
            produces={"output": "ca/total_income"},
        ),
        # Schedule 8 Part 3, each contribution on employment income: line 11 (base, 4.95% of the
        # earnings between the $3,500 exemption and the $71,300 ceiling, lines 2 to 7), line 12
        # (first additional, 1% of the same band) and line 22 (second additional, 4% of the
        # earnings between the $71,300 and $81,200 ceilings, lines 2 to 4).
        CapabilitySelection(
            name="core/contribution_tier",
            params={"tier": "ca/cpp_base_contribution"},
            consumes={"earnings": "ca/employment_income"},
            produces={"output": "ca/cpp_base_contributions"},
        ),
        CapabilitySelection(
            name="core/contribution_tier",
            params={"tier": "ca/cpp_first_additional_contribution"},
            consumes={"earnings": "ca/employment_income"},
            produces={"output": "ca/cpp_first_additional_contributions"},
        ),
        CapabilitySelection(
            name="core/contribution_tier",
            params={"tier": "ca/cpp_second_additional_contribution"},
            consumes={"earnings": "ca/employment_income"},
            produces={"output": "ca/cpp_second_additional_contributions"},
        ),
        # T1 line 31200 "through employment (boxes 18 and 55 of all T4 slips) (maximum
        # $1,077.48)": the EI premiums, 1.64% of the employment income up to the $65,700
        # maximum insurable earnings, with no exemption (the EI premium rates and maximums,
        # 2025 federal row).
        CapabilitySelection(
            name="core/contribution_tier",
            params={"tier": "ca/ei_premium"},
            consumes={"earnings": "ca/employment_income"},
            produces={"output": "ca/ei_premiums"},
        ),
        # Schedule 8 Part 3a line 28 "Line 26 plus line 27": the first and second additional
        # contributions together, the T1 line 22215 deduction.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/cpp_first_additional_contributions",
                    "ca/cpp_second_additional_contributions",
                )
            },
            produces={"output": "ca/cpp_enhanced_contributions"},
        ),
        # Schedule 7 line 5 "Line 1 plus line 4 ... Total contributions", line 6 "Total
        # contributions from line 5" and line 10 "Line 6 minus line 9 Contributions available to
        # deduct": with no HBP or LLP repayments (line 9), line 10 is line 5. In line 5's order:
        # the unused contributions (line 1), then the contributions (line 4).
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca/unused_rrsp_contributions", "ca/rrsp_contributions")},
            produces={"output": "ca/rrsp_contributions_available"},
        ),
        # Schedule 7 line 17 "Enter whichever is less: amount from line 13 or line 16.": with no
        # employer PRPP contributions (line 12) and no transfers (line 15), line 13 is the limit
        # and line 16 the contributions available to deduct. The parts keep line 20's order (line
        # 10, then the limit).
        CapabilitySelection(
            name="core/lesser_of",
            params={},
            consumes={"amounts": ("ca/rrsp_contributions_available", "ca/rrsp_deduction_limit")},
            produces={"output": "ca/rrsp_deduction_maximum"},
        ),
        # Schedule 7 line 18 "Enter your RRSP, PRPP, or SPP contributions you are deducting for
        # 2025 (cannot be more than the amount on line 17).", line 19 "Line 15 plus line 18" and
        # line 20 "Enter whichever is less: amount from line 10 or line 19. Enter this amount on
        # line 20800 of your return. RRSP deduction": with no transfers (line 15), line 19 is
        # line 18, at most line 17 and so at most line 10, and line 20 is line 18 itself. A
        # claim above line 17 is refused, not capped.
        CapabilitySelection(
            name="core/at_most",
            params={},
            consumes={"amount": "ca/rrsp_amount_deducted", "bound": "ca/rrsp_deduction_maximum"},
            produces={"output": "ca/rrsp_deduction"},
        ),
        # Schedule 7 line 23 "Line 21 minus line 22 Your unused contributions available to carry
        # forward to a future year": line 21 "Enter your contributions available to deduct from
        # line 10 of the previous page." less line 22 "Enter your RRSP deduction from line 20 of
        # the previous page."; never negative, as line 20 is at most line 10.
        CapabilitySelection(
            name="core/subtract",
            params={},
            consumes={"amount": "ca/rrsp_contributions_available", "less": "ca/rrsp_deduction"},
            produces={"output": "ca/unused_rrsp_contributions_carried_forward"},
        ),
        # Form T778 Part B line 1 "Number of eligible children born in 2019 or later whom the
        # disability amount cannot be claimed for" "multiplied by $8,000", line 2 (line 67960)
        # "Number of eligible children born in 2025 or earlier whom the disability amount can be
        # claimed for" "multiplied by $11,000" and line 3 "Number of eligible children born in
        # 2009 to 2018 (and born in 2008 or earlier with a mental or physical infirmity whom the
        # disability amount cannot be claimed for)" "multiplied by $5,000".
        CapabilitySelection(
            name="core/per_unit_amount",
            params={"amount": "ca/child_care_limit_under_seven"},
            consumes={"count": "ca/children_under_seven"},
            produces={"output": "ca/child_care_limit_for_children_under_seven"},
        ),
        CapabilitySelection(
            name="core/per_unit_amount",
            params={"amount": "ca/child_care_limit_disability"},
            consumes={"count": "ca/children_with_disability"},
            produces={"output": "ca/child_care_limit_for_children_with_disability"},
        ),
        CapabilitySelection(
            name="core/per_unit_amount",
            params={"amount": "ca/child_care_limit_seven_to_sixteen"},
            consumes={"count": "ca/children_seven_to_sixteen"},
            produces={"output": "ca/child_care_limit_for_children_seven_to_sixteen"},
        ),
        # T778 line 4 "Add lines 1 to 3.", in line order.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/child_care_limit_for_children_under_seven",
                    "ca/child_care_limit_for_children_with_disability",
                    "ca/child_care_limit_for_children_seven_to_sixteen",
                )
            },
            produces={"output": "ca/child_care_basic_limit"},
        ),
        # T778 line 6 "Enter your earned income.", "the total of the following: employment
        # income (including tips and gratuities, and the non-taxable part of an allowance
        # received as an emergency volunteer) ...": the employment income, the other earned
        # income lines not triggered; then "multiplied by two-thirds": one part.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca/employment_income",)},
            produces={"output": "ca/child_care_earned_income"},
        ),
        CapabilitySelection(
            name="core/apply_fraction",
            params={"fraction": "ca/child_care_earned_income_fraction"},
            consumes={"base": "ca/child_care_earned_income"},
            produces={"output": "ca/child_care_earned_income_limit"},
        ),
        # T778 line 7 "Enter whichever amount is the least: line 4, line 5 or line 6.", in that
        # order, line 5 "Enter the amount from line 67950." being the expenses paid; with line 8
        # (the other person with the higher net income) not triggered, line 9 "Line 7 minus line
        # 8. ... enter this amount on line 21400 of your return. Allowable deduction" is line 7.
        CapabilitySelection(
            name="core/lesser_of",
            params={},
            consumes={
                "amounts": (
                    "ca/child_care_basic_limit",
                    "ca/child_care_expenses_paid",
                    "ca/child_care_earned_income_limit",
                )
            },
            produces={"output": "ca/child_care_expenses"},
        ),
        # Federal Worksheet "Line 22100 - Carrying charges, interest expenses, and other expenses":
        # line 1 "Total carrying charges", line 2 "Total interest expenses" and line 3 "Total other
        # expenses" (starting amounts), and line 4 "Add lines 1 to 3. Enter this amount on line
        # 22100 of your return.", in line order.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/total_carrying_charges",
                    "ca/total_interest_expenses",
                    "ca/total_other_expenses",
                )
            },
            produces={"output": "ca/carrying_charges_interest_expenses_and_other_expenses"},
        ),
        # Form T1436 (Capital Gains Worksheet), "Line 21700 – Allowable business investment loss",
        # "Calculating your business investment loss reduction, if any": lines 1 to 6 (the capital
        # gains deductions claimed for 1985 to 1987, for 1988 and 1989 other than for eligible
        # capital property, for 1988 and 1989 for eligible capital property, for 1990 to 1999, for
        # 2000 and for 2001 to 2024) are starting amounts, each as its line prints it after its
        # multiplier (the figures come from the returns of 1985 to 2024); line 7 "Add lines 1 to 6."
        # Total of all capital gains deductions claimed from 1985 to 2024.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/capital_gains_deductions_1985_to_1987",
                    "ca/capital_gains_deductions_1988_and_1989_other_than_eligible_capital_property",
                    "ca/capital_gains_deductions_1988_and_1989_eligible_capital_property",
                    "ca/capital_gains_deductions_1990_to_1999",
                    "ca/capital_gains_deductions_2000",
                    "ca/capital_gains_deductions_2001_to_2024",
                )
            },
            produces={"output": "ca/capital_gains_deductions_claimed_1985_to_2024"},
        ),
        # Lines 8 to 13 (the amounts of Schedule 3 for 1986 to 1994, 1994 to 1996, 1997 to 1999,
        # 2000, 2001 to 2023 and 2024) are starting amounts; line 14 "Add lines 8 to 13." Total of
        # all other business investment loss reductions for 1986 to 2024.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/other_business_investment_loss_reductions_1986_to_1994",
                    "ca/other_business_investment_loss_reductions_1994_to_1996",
                    "ca/other_business_investment_loss_reductions_1997_to_1999",
                    "ca/other_business_investment_loss_reductions_2000",
                    "ca/other_business_investment_loss_reductions_2001_to_2023",
                    "ca/other_business_investment_loss_reductions_2024",
                )
            },
            produces={"output": "ca/other_business_investment_loss_reductions_1986_to_2024"},
        ),
        # Line 15 "Line 7 minus line 14" prints no "(if negative, enter "0")", so it may be
        # negative.
        CapabilitySelection(
            name="core/subtract",
            params={},
            consumes={
                "amount": "ca/capital_gains_deductions_claimed_1985_to_2024",
                "less": "ca/other_business_investment_loss_reductions_1986_to_2024",
            },
            produces={"output": "ca/business_investment_loss_reduction_available"},
        ),
        # Line 16 "Business investment loss in 2025 Enter this amount on line 21699 of your return."
        # is a starting amount, the gross of line 21699; line 17 "Enter whichever is less: amount
        # from line 15 or line 16. Enter this amount on line 17800 of Schedule 3." prints no "(if
        # negative, enter "0")" either, so it may be negative with line 15.
        CapabilitySelection(
            name="core/lesser_of",
            params={},
            consumes={
                "amounts": (
                    "ca/business_investment_loss_reduction_available",
                    "ca/business_investment_loss",
                )
            },
            produces={"output": "ca/business_investment_loss_reduction"},
        ),
        # Line 18 "Line 16 minus line 17 Business investment loss reduction": never negative, as
        # line 17 is at most line 16.
        CapabilitySelection(
            name="core/subtract",
            params={},
            consumes={
                "amount": "ca/business_investment_loss",
                "less": "ca/business_investment_loss_reduction",
            },
            produces={"output": "ca/business_investment_loss_after_reduction"},
        ),
        # Line 19 "Inclusion rate for 2025 × 50 %", the rate dataset, and line 20 "Line 18
        # multiplied by the percentage on line 19 Enter this amount on line 21700 of your return.
        # Allowable business investment loss".
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca/business_investment_loss_inclusion_rate"},
            consumes={"base": "ca/business_investment_loss_after_reduction"},
            produces={"output": "ca/allowable_business_investment_loss"},
        ),
        # Schedule 15 (form 5000-S15) Step 2 "Calculate your annual FHSA limit for 2025": line 1 and
        # line 68935 "Total contributions made to your FHSAs in 2025 (box 18 of your 2025 T4FHSA
        # slips)" and line 2 and line 68940 "Total contributions made to your FHSAs in 2025 after
        # your first qualifying withdrawal" are starting amounts; line 3 "Line 1 minus line 2 ="
        # prints no "(if negative, enter "0")", so it may be negative.
        CapabilitySelection(
            name="core/subtract",
            params={},
            consumes={
                "amount": "ca/fhsa_contributions_in_2025",
                "less": "ca/fhsa_contributions_in_2025_after_first_qualifying_withdrawal",
            },
            produces={"output": "ca/fhsa_contributions_in_2025_before_first_qualifying_withdrawal"},
        ),
        # Line 4 "Variable "B" amount of your annual FHSA limit for 2024 (from your 2025 FHSA
        # participation room statement)" is a starting amount; line 5 "Line 3 plus line 4 =".
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/fhsa_contributions_in_2025_before_first_qualifying_withdrawal",
                    "ca/fhsa_variable_b_amount",
                )
            },
            produces={"output": "ca/fhsa_contributions_plus_variable_b_amount"},
        ),
        # Line 6 and line 68945 "Total designated withdrawals from your FHSAs in 2025 (box 38 of
        # your 2025 T4FHSA slips)", line 7 "Total contributions made to your FHSAs in 2024 (from
        # your 2025 FHSA participation room statement)" and line 8 "Contributions to your FHSAs in
        # 2024 before your first qualifying withdrawal (from your 2025 FHSA participation room
        # statement)" are starting amounts; line 9 "Line 7 minus line 8 =" prints no floor.
        CapabilitySelection(
            name="core/subtract",
            params={},
            consumes={
                "amount": "ca/fhsa_contributions_in_2024",
                "less": "ca/fhsa_contributions_in_2024_before_first_qualifying_withdrawal",
            },
            produces={"output": "ca/fhsa_contributions_in_2024_after_first_qualifying_withdrawal"},
        ),
        # Line 10 "Amount from line 2" is the same artifact as line 2; line 11 "Line 9 plus line 10
        # =".
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/fhsa_contributions_in_2024_after_first_qualifying_withdrawal",
                    "ca/fhsa_contributions_in_2025_after_first_qualifying_withdrawal",
                )
            },
            produces={"output": "ca/fhsa_contributions_after_first_qualifying_withdrawal"},
        ),
        # Line 12 "Line 6 minus line 11 (if negative, enter "0") =".
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={
                "amount": "ca/fhsa_designated_withdrawals_in_2025",
                "less": "ca/fhsa_contributions_after_first_qualifying_withdrawal",
            },
            produces={"output": "ca/fhsa_excess_designated_withdrawals"},
        ),
        # Line 13 "Line 5 minus line 12 (if negative, enter "0") =".
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={
                "amount": "ca/fhsa_contributions_plus_variable_b_amount",
                "less": "ca/fhsa_excess_designated_withdrawals",
            },
            produces={"output": "ca/fhsa_contributions_limit"},
        ),
        # Line 14 "8,000.00", the dataset as an artifact of the same name; line 30 "8,000.00" is the
        # same figure, read again below.
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca/fhsa_annual_amount"},
            consumes={},
            produces={"output": "ca/fhsa_annual_amount"},
        ),
        # Line 15 "Your FHSA carryforward for 2025 (from your 2025 FHSA participation room
        # statement)" is a starting amount; line 16 "Line 14 plus line 15 =".
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca/fhsa_annual_amount", "ca/fhsa_carryforward_for_2025")},
            produces={"output": "ca/fhsa_annual_amount_with_carryforward"},
        ),
        # Line 17 "Total transfers from your RRSPs to your FHSAs in 2024 and prior years (from your
        # 2025 FHSA participation room statement)" and line 18 and line 68950 "Total transfers from
        # your RRSPs to your FHSAs in 2025 (boxes 32 and 34 of your 2025 T4FHSA slips)" are starting
        # amounts; line 19 "Line 17 plus line 18 =".
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/fhsa_rrsp_transfers_in_2024_and_prior_years",
                    "ca/fhsa_rrsp_transfers_in_2025",
                )
            },
            produces={"output": "ca/fhsa_total_rrsp_transfers"},
        ),
        # Line 20 "Total designated transfers from your FHSAs to your RRSPs or RRIFs in 2024 and
        # prior years (from your 2025 FHSA participation room statement)" and line 21 and line 68955
        # "Total designated transfers from your FHSAs to your RRSPs or RRIFs in 2025 (box 36 of your
        # 2025 T4FHSA slips)" are starting amounts; line 22 "Line 20 plus line 21 =".
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/fhsa_designated_transfers_in_2024_and_prior_years",
                    "ca/fhsa_designated_transfers_in_2025",
                )
            },
            produces={"output": "ca/fhsa_total_designated_transfers"},
        ),
        # Line 23 "Line 19 minus line 22 Net RRSP-to-FHSA transfer amount =" prints no floor. Line
        # 24 "Amount from line 23 of the previous page" is the same artifact.
        CapabilitySelection(
            name="core/subtract",
            params={},
            consumes={
                "amount": "ca/fhsa_total_rrsp_transfers",
                "less": "ca/fhsa_total_designated_transfers",
            },
            produces={"output": "ca/fhsa_net_rrsp_transfer_amount"},
        ),
        # Step 2 (continued): line 25 "Amount from line 17 of the previous page" and line 26 "Amount
        # from line 20 of the previous page" are the same artifacts; line 27 "Net RRSP-to-FHSA
        # transfer amount for 2024 and prior years: Line 25 minus line 26 =" prints no floor.
        CapabilitySelection(
            name="core/subtract",
            params={},
            consumes={
                "amount": "ca/fhsa_rrsp_transfers_in_2024_and_prior_years",
                "less": "ca/fhsa_designated_transfers_in_2024_and_prior_years",
            },
            produces={"output": "ca/fhsa_net_rrsp_transfer_amount_for_2024_and_prior_years"},
        ),
        # Line 28 "Variable "H" amount of your annual FHSA limit for 2024 (from your 2025 FHSA
        # participation room statement)" is a starting amount; line 29 "Line 27 minus line 28 (if
        # negative, enter "0") =".
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={
                "amount": "ca/fhsa_net_rrsp_transfer_amount_for_2024_and_prior_years",
                "less": "ca/fhsa_variable_h_amount",
            },
            produces={"output": "ca/fhsa_net_transfer_amount_less_variable_h_amount"},
        ),
        # Line 30 "8,000.00", the same dataset as line 14, read by its own step.
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca/fhsa_annual_amount"},
            consumes={},
            produces={"output": "ca/fhsa_annual_amount_for_2024"},
        ),
        # Line 31 "Your FHSA carryforward for 2024 (from your 2024 FHSA participation room
        # statement)" is a starting amount; line 32 "Line 30 plus line 31 =".
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca/fhsa_annual_amount_for_2024", "ca/fhsa_carryforward_for_2024")},
            produces={"output": "ca/fhsa_annual_amount_for_2024_with_carryforward"},
        ),
        # Line 33 "Enter whichever is less: amount from line 29 or line 32.", in that order.
        CapabilitySelection(
            name="core/lesser_of",
            params={},
            consumes={
                "amounts": (
                    "ca/fhsa_net_transfer_amount_less_variable_h_amount",
                    "ca/fhsa_annual_amount_for_2024_with_carryforward",
                )
            },
            produces={"output": "ca/fhsa_transfer_amount_at_most_limit"},
        ),
        # Line 34 "Variable "F" amount of your annual FHSA limit for 2024 (from your 2025 FHSA
        # participation room statement)" is a starting amount; line 35 "Line 33 plus line 34 =".
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": ("ca/fhsa_transfer_amount_at_most_limit", "ca/fhsa_variable_f_amount")
            },
            produces={"output": "ca/fhsa_transfer_amount_plus_variable_f_amount"},
        ),
        # Line 36 "Line 24 minus line 35 =" (line 24 "Amount from line 23 of the previous page")
        # prints no floor.
        CapabilitySelection(
            name="core/subtract",
            params={},
            consumes={
                "amount": "ca/fhsa_net_rrsp_transfer_amount",
                "less": "ca/fhsa_transfer_amount_plus_variable_f_amount",
            },
            produces={"output": "ca/fhsa_net_transfer_amount_after_prior_years"},
        ),
        # Line 37 "Amount from line 16 of the previous page" and line 38 "Amount from line 36" are
        # the same artifacts; line 39 "Line 37 minus line 38 (if negative, enter "0") =".
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={
                "amount": "ca/fhsa_annual_amount_with_carryforward",
                "less": "ca/fhsa_net_transfer_amount_after_prior_years",
            },
            produces={"output": "ca/fhsa_annual_amount_after_transfers"},
        ),
        # Line 40 "Enter whichever is less: amount from line 13 of the previous page or line 39.
        # Annual FHSA limit for 2025", in that order, when the maximum participation period has not
        # ended.
        CapabilitySelection(
            name="core/lesser_of",
            params={},
            consumes={
                "amounts": ("ca/fhsa_contributions_limit", "ca/fhsa_annual_amount_after_transfers")
            },
            produces={"output": "ca/fhsa_annual_limit_from_step_2"},
        ),
        # "If your maximum participation period (MPP) ended in a prior year, do not complete this
        # step. Your 2025 annual FHSA limit is "0". Enter "0" on line 40 and continue at Step 3.":
        # the printed 0, the dataset as an artifact of the same name.
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca/fhsa_annual_limit_after_maximum_participation_period"},
            consumes={},
            produces={"output": "ca/fhsa_annual_limit_after_maximum_participation_period"},
        ),
        # A count of 1 when the maximum participation period ended in a prior year (a caller's 0 or
        # 1) chooses the printed 0 over the result of Step 2 for line 40 (and so for line 41 "Annual
        # FHSA limit from line 40").
        CapabilitySelection(
            name="core/choose_by_count",
            params={},
            consumes={
                "count": "ca/fhsa_maximum_participation_period_ended",
                "when_none": "ca/fhsa_annual_limit_from_step_2",
                "when_any": "ca/fhsa_annual_limit_after_maximum_participation_period",
            },
            produces={"output": "ca/fhsa_annual_limit"},
        ),
        # Step 3 "Calculate your FHSA deduction and unused FHSA contributions available to deduct in
        # future years": line 42 "Your total annual FHSA limits for 2024 and prior years (from your
        # 2025 FHSA participation room statement)" is a starting amount; line 43 "Line 41 plus line
        # 42 =".
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": ("ca/fhsa_annual_limit", "ca/fhsa_annual_limits_for_2024_and_prior_years")
            },
            produces={"output": "ca/fhsa_total_annual_limits"},
        ),
        # Line 44 "Your total FHSA deductions for 2024 and prior years (from your 2025 FHSA
        # participation room statement)" is a starting amount; line 45 "Line 43 minus line 44 ="
        # prints no floor.
        CapabilitySelection(
            name="core/subtract",
            params={},
            consumes={
                "amount": "ca/fhsa_total_annual_limits",
                "less": "ca/fhsa_deductions_for_2024_and_prior_years",
            },
            produces={"output": "ca/fhsa_annual_limits_less_deductions"},
        ),
        # Line 46 "Lifetime FHSA limit 40,000.00", the dataset as an artifact of the same name.
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca/fhsa_lifetime_limit"},
            consumes={},
            produces={"output": "ca/fhsa_lifetime_limit"},
        ),
        # Line 47 "Your FHSA deduction from line 44" is the same artifact as line 44; line 48 "Line
        # 46 minus line 47 =" prints no floor.
        CapabilitySelection(
            name="core/subtract",
            params={},
            consumes={
                "amount": "ca/fhsa_lifetime_limit",
                "less": "ca/fhsa_deductions_for_2024_and_prior_years",
            },
            produces={"output": "ca/fhsa_lifetime_limit_less_deductions"},
        ),
        # Line 49 "Net RRSP-to-FHSA transfer amount from line 24" is the same artifact as line 23;
        # line 50 "Line 48 minus line 49 (if negative, enter "0") =".
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={
                "amount": "ca/fhsa_lifetime_limit_less_deductions",
                "less": "ca/fhsa_net_rrsp_transfer_amount",
            },
            produces={"output": "ca/fhsa_lifetime_limit_less_deductions_and_transfers"},
        ),
        # Line 51 "Enter whichever is less: amount from line 45 or line 50. Maximum FHSA deduction
        # available for 2025", in that order.
        CapabilitySelection(
            name="core/lesser_of",
            params={},
            consumes={
                "amounts": (
                    "ca/fhsa_annual_limits_less_deductions",
                    "ca/fhsa_lifetime_limit_less_deductions_and_transfers",
                )
            },
            produces={"output": "ca/fhsa_maximum_deduction"},
        ),
        # Line 52 "Your unused FHSA contributions available to deduct in future years (from your
        # 2025 FHSA participation room statement)" is a starting amount; line 53 "Amount from line 3
        # of page 2" is the same artifact as line 3; line 54 "Line 52 plus line 53 =".
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/fhsa_unused_contributions_brought_forward",
                    "ca/fhsa_contributions_in_2025_before_first_qualifying_withdrawal",
                )
            },
            produces={"output": "ca/fhsa_unused_contributions_plus_contributions"},
        ),
        # Line 55 "Amount from line 12 of page 2" is the same artifact as line 12; line 56 "Line 54
        # minus line 55 =" prints no floor.
        CapabilitySelection(
            name="core/subtract",
            params={},
            consumes={
                "amount": "ca/fhsa_unused_contributions_plus_contributions",
                "less": "ca/fhsa_excess_designated_withdrawals",
            },
            produces={"output": "ca/fhsa_contributions_available"},
        ),
        # Line 57 "Enter the FHSA contributions you are deducting for 2025 (cannot be more than the
        # amount on line 51 of the previous page). Enter this amount on line 20805 of your return.
        # FHSA deduction for 2025": the amount the filer chooses to deduct, a starting amount,
        # refused when above line 51, not capped (as Schedule 7 line 18 is refused above line 17);
        # T1 line 37 and line 20805 is that amount.
        CapabilitySelection(
            name="core/at_most",
            params={},
            consumes={
                "amount": "ca/fhsa_contributions_deducted",
                "bound": "ca/fhsa_maximum_deduction",
            },
            produces={"output": "ca/fhsa_deduction"},
        ),
        # Line 58 "Line 56 minus line 57 Your unused FHSA contributions available to deduct in
        # future years =", a product of the return for the next year's line 52; it prints no floor.
        CapabilitySelection(
            name="core/subtract",
            params={},
            consumes={"amount": "ca/fhsa_contributions_available", "less": "ca/fhsa_deduction"},
            produces={"output": "ca/fhsa_unused_contributions_carried_forward"},
        ),
        # T1 line 53 and line 23300 "Add lines 35 to 52.": the deductions wired so far in the form's
        # line order (20700, 20800, 20805, 21000, 21200, 21300, 21400, 21700, 22000, 22100, 22215,
        # 22400, 23200). Not wired yet: 21500, 21900, 22200, 22900 and 23100; lines 20810 and 21999
        # have no line among lines 35 to 52 and nothing on this return reads them.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/rpp_deduction",
                    "ca/rrsp_deduction",
                    "ca/fhsa_deduction",
                    "ca/elected_split_pension_deduction",
                    "ca/union_dues",
                    "ca/uccb_repayment",
                    "ca/child_care_expenses",
                    "ca/allowable_business_investment_loss",
                    "ca/support_payments_deduction",
                    "ca/carrying_charges_interest_expenses_and_other_expenses",
                    "ca/cpp_enhanced_contributions",
                    "ca/exploration_and_development_expenses",
                    "ca/other_deductions",
                )
            },
            produces={"output": "ca/deductions_from_total_income"},
        ),
        # T1 line 54 and line 23400 "Line 34 minus line 53 (if negative, show in brackets) Net
        # income before adjustments": total income less total deductions, not floored, so a negative
        # result is shown in brackets. The net income of line 56 (line 23600) stays the floored
        # result until line 23500 is wired.
        CapabilitySelection(
            name="core/subtract",
            params={},
            consumes={"amount": "ca/total_income", "less": "ca/deductions_from_total_income"},
            produces={"output": "ca/net_income_before_adjustments"},
        ),
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={"amount": "ca/total_income", "less": "ca/deductions_from_total_income"},
            produces={"output": "ca/net_income"},
        ),
        # Federal Worksheet "Line 25000 - Other payments deduction", "Complete the following
        # calculation if you reported net federal supplements on line 14600 of your return.":
        # line 1 "Amount from line 23400 of your return (if negative, enter "0")" is the net
        # income artifact (line 23400 floored at 0, as line 23500 is not wired yet); line 4 "Line
        # 2 plus line 3 =" adds line 2 "Amount from line 11700 of your return" (the universal
        # child care benefit) and line 3 "Amount from line 12500 of your return" (the RDSP
        # income), in line order.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca/universal_child_care_benefit", "ca/rdsp_income")},
            produces={"output": "ca/uccb_and_rdsp_income"},
        ),
        # Line 5 "Line 1 minus line 4 =" prints no "(if negative, enter "0")", unlike line 1, so
        # it may be negative.
        CapabilitySelection(
            name="core/subtract",
            params={},
            consumes={"amount": "ca/net_income", "less": "ca/uccb_and_rdsp_income"},
            produces={"output": "ca/net_income_less_uccb_and_rdsp_income"},
        ),
        # Line 8 "Line 6 plus line 7 =": line 6 "Amount from line 21300 of your return" (the UCCB
        # repayment, a starting amount, also a part of line 23300) and line 7 "RDSP income
        # repayment (included in the amount on line 23200 of your return)", a starting amount of
        # its own that the caller also includes in line 23200, in line order.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca/uccb_repayment", "ca/rdsp_income_repayment")},
            produces={"output": "ca/uccb_and_rdsp_income_repayments"},
        ),
        # Line 9 "Line 5 plus line 8 =", the amount the worksheet compares with $93,454.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/net_income_less_uccb_and_rdsp_income",
                    "ca/uccb_and_rdsp_income_repayments",
                )
            },
            produces={"output": "ca/other_payments_limit_income"},
        ),
        # "If the amount on line 9 is more than $93,454, go to canada.ca/line-25000 to find out
        # how much you can deduct. Otherwise, enter the amount from line 14700 of your return on
        # line 25000 of your return.": a count of 1 when line 9 is more than $93,454 (a starting
        # count, 0 or 1, until a comparison capability derives it) chooses the amount that chart
        # gives (a starting amount) over line 14700.
        CapabilitySelection(
            name="core/choose_by_count",
            params={},
            consumes={
                "count": "ca/other_payments_worksheet_line_9_over_limit",
                "when_none": "ca/income_support_benefits",
                "when_any": "ca/other_payments_deduction_above_limit",
            },
            produces={"output": "ca/other_payments_deduction_after_limit"},
        ),
        # T1 line 60 and line 25000 "Other payments deduction (enter the amount from line 14700
        # if you did not enter an amount on line 14600; otherwise, use Federal Worksheet)": a
        # count of 1 when an amount was entered on line 14600 (a starting count, 0 or 1, until a
        # comparison capability derives it) chooses the worksheet's result over line 14700.
        CapabilitySelection(
            name="core/choose_by_count",
            params={},
            consumes={
                "count": "ca/other_payments_worksheet_required",
                "when_none": "ca/income_support_benefits",
                "when_any": "ca/other_payments_deduction_after_limit",
            },
            produces={"output": "ca/other_payments_deduction"},
        ),
        # T1 line 68 and line 25700 "Add lines 58 to 67.": lines 58, 59, 60, 61, 62 and 67 (lines
        # 24400, 24900, 25000, 25100, 25200 and 25600), in line order; lines 63 to 66 (25300,
        # 25395, 25400 and 25500) are not wired yet.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/canadian_armed_forces_and_police_deduction",
                    "ca/security_options_deductions",
                    "ca/other_payments_deduction",
                    "ca/limited_partnership_losses_of_other_years",
                    "ca/non_capital_losses_of_other_years",
                    "ca/additional_deductions",
                )
            },
            produces={"output": "ca/deductions_from_net_income"},
        ),
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={"amount": "ca/net_income", "less": "ca/deductions_from_net_income"},
            produces={"output": "ca/taxable_income"},
        ),
        CapabilitySelection(
            name="core/progressive_tax",
            params={"schedule": "ca/brackets"},
            consumes={"base": "ca/taxable_income"},
            produces={"output": "ca/federal_basic_tax"},
        ),
        CapabilitySelection(
            name="core/progressive_tax",
            params={"schedule": "ca-on/brackets"},
            consumes={"base": "ca/taxable_income"},
            produces={"output": "ca-on/ontario_basic_tax"},
        ),
        # T1 line 30000 "If the amount on line 23600 is $177,882 or less, enter $16,129. If the
        # amount on line 23600 is $253,414 or more, enter $14,538. Otherwise, use the Federal
        # Worksheet to calculate the amount to enter. (maximum $16,129)": the federal basic
        # personal amount is the worksheet's taper on net income (line 23600), the first part of
        # the T1's total of credit amounts.
        CapabilitySelection(
            name="core/tapered_amount",
            params={"taper": "ca/basic_personal_amount"},
            consumes={"base": "ca/net_income"},
            produces={"output": "ca/basic_personal_amount"},
        ),
        # ON428 line 58040 has no reduction: the Ontario basic personal amount dataset becomes an
        # artifact of the same name, the first part of ON428's total of credit amounts.
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca-on/basic_personal_amount"},
            consumes={},
            produces={"output": "ca-on/basic_personal_amount"},
        ),
        # The Canada employment amount: the lesser of the T1's cap and employment income.
        CapabilitySelection(
            name="core/capped_amount",
            params={"cap": "ca/canada_employment_amount"},
            consumes={"base": "ca/employment_income"},
            produces={"output": "ca/canada_employment_amount"},
        ),
        # T1 line 100 (line 31800) "Disability amount transferred from a dependant (use Federal
        # Worksheet)", Federal Worksheet "Line 31800 - Disability amount transferred from a
        # dependant": for each dependant who is eligible for the disability tax credit, line 1
        # "Base amount 10,138.00", line 2 "Maximum supplement 5,914.00", line 4 "Threshold for
        # child care and attendant care expenses 3,464.00", line 8 "Line 1 plus line 7 (maximum
        # $16,052)", line 13 "Enter whichever is less: amount from line 8 or line 12. Allowable
        # amount for this dependant", and "the total of allowable amounts claimed for all
        # dependants who qualify for the disability tax credit".
        CapabilitySelection(
            name="ca/disability_transfer_amount",
            params={
                "base": "ca/disability_transfer_base_amount",
                "supplement": "ca/disability_transfer_supplement_maximum",
                "threshold": "ca/disability_transfer_care_threshold",
                "maximum": "ca/disability_transfer_maximum",
            },
            consumes={"dependants": "ca/disability_dependants"},
            produces={"output": "ca/disability_transferred_amount"},
        ),
        # Federal Worksheet, "Line 30100 - Age amount": line 1 "Maximum amount 9,028.00", the
        # dataset as an artifact of the same name.
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca/age_maximum"},
            consumes={},
            produces={"output": "ca/age_maximum"},
        ),
        # Line 3 "Income threshold 45,522.00", the dataset as an artifact of the same name.
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca/age_income_threshold"},
            consumes={},
            produces={"output": "ca/age_income_threshold"},
        ),
        # Line 2 "Amount from line 23600 of your return", the net income, and line 4 "Line 2 minus
        # line 3 (if negative, enter "0")".
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={"amount": "ca/net_income", "less": "ca/age_income_threshold"},
            produces={"output": "ca/age_income_over_threshold"},
        ),
        # Line 5 "Applicable rate 15%" and line 6 "Line 4 multiplied by the percentage from line
        # 5".
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca/age_rate"},
            consumes={"base": "ca/age_income_over_threshold"},
            produces={"output": "ca/age_reduction"},
        ),
        # Line 7 "Line 1 minus line 6 (if negative, enter "0") Enter this amount on line 30100 of
        # your return."
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={"amount": "ca/age_maximum", "less": "ca/age_reduction"},
            produces={"output": "ca/age_amount_before_count"},
        ),
        # T1 line 78 (line 30100) "Age amount (if you were born in 1960 or earlier) (use Federal
        # Worksheet) (maximum $9,028)": line 7 once if born in 1960 or earlier, else 0.
        CapabilitySelection(
            name="core/times_count",
            params={},
            consumes={
                "amount": "ca/age_amount_before_count",
                "count": "ca/born_in_1960_or_earlier",
            },
            produces={"output": "ca/age_amount"},
        ),
        # Schedule 5, "Line 30300 - Spouse or common-law partner amount": line 2 and line 51090
        # "If you are eligible for the Canada caregiver amount for your spouse or common-law
        # partner, enter $2,687", for each spouse eligible for it, at most one.
        CapabilitySelection(
            name="core/per_unit_amount",
            params={"amount": "ca/spouse_infirmity_amount"},
            consumes={"count": "ca/spouse_caregiver_eligible"},
            produces={"output": "ca/spouse_infirmity_supplement"},
        ),
        # Line 3 "Line 1 plus line 2", line 1 "Basic personal amount from line 30000 of your
        # return".
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca/basic_personal_amount", "ca/spouse_infirmity_supplement")},
            produces={"output": "ca/spouse_amount_basis"},
        ),
        # Line 4 "Your spouse's or common-law partner's net income from line 23600 of their
        # return (Note 1)" and line 5 "Line 3 minus line 4 (if negative, enter "0") Enter this
        # amount on line 30300 of your return."
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={"amount": "ca/spouse_amount_basis", "less": "ca/spouse_net_income"},
            produces={"output": "ca/spouse_amount_before_count"},
        ),
        # T1 line 79 (line 30300) "Spouse or common-law partner amount (complete Schedule 5)":
        # line 5 once if the filer claims it ("Only one spouse or common-law partner can claim
        # the amount on line 30300 for each other for the same year"), else 0.
        CapabilitySelection(
            name="core/times_count",
            params={},
            consumes={
                "amount": "ca/spouse_amount_before_count",
                "count": "ca/spouses_claimed",
            },
            produces={"output": "ca/spouse_amount"},
        ),
        # Schedule 5, "Line 30400 - Amount for an eligible dependant": line 1 "Basic personal
        # amount from line 30000 of your return", line 3 "Line 1 plus line 2" with line 2 (an
        # infirm eligible dependant 18 or older) not triggered, line 4 (51106) "Dependant's net
        # income from line 23600 of their return" and line 5 "Line 3 minus line 4 (if negative,
        # enter "0") Enter this amount on line 30400 of your return.".
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={"amount": "ca/basic_personal_amount", "less": "ca/dependant_net_income"},
            produces={"output": "ca/eligible_dependant_amount_before_count"},
        ),
        # T1 line 80 (line 30400) "Amount for an eligible dependant (complete Schedule 5)": line
        # 5 for each eligible dependant claimed, at most one ("Each household is allowed only one
        # claim for this amount").
        CapabilitySelection(
            name="core/times_count",
            params={},
            consumes={
                "amount": "ca/eligible_dependant_amount_before_count",
                "count": "ca/eligible_dependants",
            },
            produces={"output": "ca/eligible_dependant_amount"},
        ),
        # Schedule 5, "Line 30425 - Canada caregiver amount for spouse or common-law partner,
        # or eligible dependant age 18 or older": line 1 "Base amount 28,798.00", the dataset as
        # an artifact of the same name.
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca/spouse_caregiver_base"},
            consumes={},
            produces={"output": "ca/spouse_caregiver_base"},
        ),
        # Line 2 "Net income for this person from line 23600 of their return", the spouse's
        # net income, and line 3 "Line 1 minus line 2 (if negative, enter "0") (maximum
        # $8,601)", before its maximum, then at most it.
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={"amount": "ca/spouse_caregiver_base", "less": "ca/spouse_net_income"},
            produces={"output": "ca/spouse_caregiver_before_maximum"},
        ),
        CapabilitySelection(
            name="core/capped_amount",
            params={"cap": "ca/spouse_caregiver_maximum"},
            consumes={"base": "ca/spouse_caregiver_before_maximum"},
            produces={"output": "ca/spouse_caregiver_limit"},
        ),
        # Line 4 "Amount claimed on line 30300 or line 30400 of your return, if applicable", the
        # spouse amount, and line 5 "Line 3 minus line 4 (if negative, enter "0") Enter this
        # amount on line 30425 of your return."
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={"amount": "ca/spouse_caregiver_limit", "less": "ca/spouse_amount"},
            produces={"output": "ca/spouse_caregiver_amount_before_count"},
        ),
        # T1 line 81 (line 30425) "Canada caregiver amount for spouse or common-law partner,
        # or eligible dependant age 18 or older (complete Schedule 5)": line 5 once if the
        # spouse is eligible for the Canada caregiver amount (line 51090), else 0. The eligible
        # dependant 18 or older (line 30400) is not wired here.
        CapabilitySelection(
            name="core/times_count",
            params={},
            consumes={
                "amount": "ca/spouse_caregiver_amount_before_count",
                "count": "ca/spouse_caregiver_eligible",
            },
            produces={"output": "ca/spouse_caregiver_amount"},
        ),
        # T1 line 82 (line 30450) "Canada caregiver amount for other infirm dependants age 18 or
        # older (complete Schedule 5)", Schedule 5 "Line 30450 - Canada caregiver amount for other
        # infirm dependants age 18 or older": for each dependant, line 1 "Base amount 28,798.00"
        # less line 2 "Infirm dependant's net income from line 23600 of their return", line 3
        # "Line 1 minus line 2 (if negative, enter "0") (maximum $8,601)", and "the total of
        # allowable amounts claimed for all dependants".
        CapabilitySelection(
            name="ca/caregiver_amount",
            params={"base": "ca/caregiver_base_amount", "maximum": "ca/caregiver_maximum_amount"},
            consumes={"dependants": "ca/infirm_dependants"},
            produces={"output": "ca/caregiver_amount"},
        ),
        # T1 line 83 (line 30500) "Canada caregiver amount for infirm children under 18 years of
        # age (see Schedule 5) Number of children you are claiming this amount for Line 30499"
        # "multiplied by $2,687".
        CapabilitySelection(
            name="core/per_unit_amount",
            params={"amount": "ca/infirm_child_amount"},
            consumes={"count": "ca/infirm_children"},
            produces={"output": "ca/infirm_children_amount"},
        ),
        # Worksheet ON428, "Line 58080 - Age amount": line 1 "Maximum amount 6,223.00", the
        # dataset as an artifact of the same name.
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca-on/age_maximum"},
            consumes={},
            produces={"output": "ca-on/age_maximum"},
        ),
        # Line 3 "Income threshold 46,330.00", the dataset as an artifact of the same name.
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca-on/age_income_threshold"},
            consumes={},
            produces={"output": "ca-on/age_income_threshold"},
        ),
        # Line 2 "Amount from line 23600 of your return", the net income, and line 4 "Line 2
        # minus line 3 (if negative, enter "0")".
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={"amount": "ca/net_income", "less": "ca-on/age_income_threshold"},
            produces={"output": "ca-on/age_income_over_threshold"},
        ),
        # Line 5 "Applicable rate 15%" and line 6 "Line 4 multiplied by the percentage from line
        # 5".
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca-on/age_rate"},
            consumes={"base": "ca-on/age_income_over_threshold"},
            produces={"output": "ca-on/age_reduction"},
        ),
        # Line 7 "Line 1 minus line 6 (if negative, enter "0") Enter this amount on line 58080 of
        # your Form ON428."
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={"amount": "ca-on/age_maximum", "less": "ca-on/age_reduction"},
            produces={"output": "ca-on/age_amount_before_count"},
        ),
        # ON428 line 10 and line 58080 "Age amount (if you were born in 1960 or earlier) (use
        # Worksheet ON428) (maximum $6,223)": line 7 once if born in 1960 or earlier, else 0.
        CapabilitySelection(
            name="core/times_count",
            params={},
            consumes={
                "amount": "ca-on/age_amount_before_count",
                "count": "ca/born_in_1960_or_earlier",
            },
            produces={"output": "ca-on/age_amount"},
        ),
        # ON428 line 11 "Base amount 11,905.00": the dataset becomes an artifact of the same name.
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca-on/spouse_base"},
            consumes={},
            produces={"output": "ca-on/spouse_base"},
        ),
        # Line 12 "Your spouse's or common-law partner's net income from line 23600 of their
        # return", and line 13 (line 58120) "Line 11 minus line 12 (if negative, enter "0")
        # (maximum $10,823)", before its maximum, then at most it.
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={"amount": "ca-on/spouse_base", "less": "ca/spouse_net_income"},
            produces={"output": "ca-on/spouse_amount_before_maximum"},
        ),
        CapabilitySelection(
            name="core/capped_amount",
            params={"cap": "ca-on/spouse_maximum"},
            consumes={"base": "ca-on/spouse_amount_before_maximum"},
            produces={"output": "ca-on/spouse_amount_before_count"},
        ),
        # Line 58120 for each spouse or common-law partner amount claimed, the T1 line 30300
        # count.
        CapabilitySelection(
            name="core/times_count",
            params={},
            consumes={
                "amount": "ca-on/spouse_amount_before_count",
                "count": "ca/spouses_claimed",
            },
            produces={"output": "ca-on/spouse_amount"},
        ),
        # ON428 line 14 "Base amount 11,905.00": the dataset becomes an artifact of the same name.
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca-on/eligible_dependant_base"},
            consumes={},
            produces={"output": "ca-on/eligible_dependant_base"},
        ),
        # ON428 line 15 "Your eligible dependant's net income from line 23600 of their return",
        # the federal Schedule 5 line 4 figure, and line 16 (line 58160) "Line 14 minus line 15
        # (if negative, enter "0") (maximum $10,823)", before its maximum, then at most it.
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={
                "amount": "ca-on/eligible_dependant_base",
                "less": "ca/dependant_net_income",
            },
            produces={"output": "ca-on/eligible_dependant_amount_before_maximum"},
        ),
        CapabilitySelection(
            name="core/capped_amount",
            params={"cap": "ca-on/eligible_dependant_maximum"},
            consumes={"base": "ca-on/eligible_dependant_amount_before_maximum"},
            produces={"output": "ca-on/eligible_dependant_amount_before_count"},
        ),
        # Line 58160 for each eligible dependant claimed, the T1 line 30400 count.
        CapabilitySelection(
            name="core/times_count",
            params={},
            consumes={
                "amount": "ca-on/eligible_dependant_amount_before_count",
                "count": "ca/eligible_dependants",
            },
            produces={"output": "ca-on/eligible_dependant_amount"},
        ),
        # ON428 line 39 "Line 37 multiplied by the percentage from line 38" (line 37 "Amount from
        # line 23600 of your return", line 38 "Applicable rate 3%"): 3% of the net income.
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca-on/medical_net_income_rate"},
            consumes={"base": "ca/net_income"},
            produces={"output": "ca-on/medical_net_income_share"},
        ),
        # ON428 line 40 "Enter whichever is less: $2,885 or the amount on line 39."
        CapabilitySelection(
            name="core/capped_amount",
            params={"cap": "ca-on/medical_threshold_ceiling"},
            consumes={"base": "ca-on/medical_net_income_share"},
            produces={"output": "ca-on/medical_threshold"},
        ),
        # ON428 line 41 "Line 36 minus line 40 (if negative, enter "0")": line 36 is the filer's
        # medical expenses, the caller input of T1 line 107 (line 33099), shared with the T1.
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={"amount": "ca/medical_expenses", "less": "ca-on/medical_threshold"},
            produces={"output": "ca-on/medical_expenses_over_threshold"},
        ),
        # ON428 line 42 and line 58729 "Allowable amount of medical expenses for other dependants
        # (use Worksheet ON428)"; Worksheet ON428, line 58729, for each dependant: line 1 "Medical
        # expenses for other dependant", line 2 "Enter the amount from line 40 of the dependant's
        # Form ON428.", line 3 "Line 1 minus line 2 (if negative, enter "0") (maximum $15,551 per
        # dependant)", and line 4 "Add the amounts from line 3 of columns 1, 2, and 3 (and others,
        # if any). Enter this amount on line 58729 of your Form ON428." The same people as T1 line
        # 33199, so the same record list.
        CapabilitySelection(
            name="ca/other_dependants_medical",
            params={"reduction": "ca-on/other_dependants_medical_reduction"},
            consumes={"dependants": "ca/other_dependants"},
            produces={"output": "ca-on/other_dependants_medical"},
        ),
        # ON428 line 43 and line 58769 "Line 41 plus line 42".
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": ("ca-on/medical_expenses_over_threshold", "ca-on/other_dependants_medical")
            },
            produces={"output": "ca-on/medical_claim"},
        ),
        # ON428 line 17 and line 58185 "Ontario caregiver amount (use Worksheet ON428)", Worksheet
        # ON428 "Line 58185 - Ontario caregiver amount": for each dependant, line 1 "Base amount
        # 26,562.00" less line 2 "Dependant's net income from line 23600 of their return", line 3
        # "Line 1 minus line 2 (if negative, enter "0") (maximum $6,008 per dependant)", line 4
        # "Amount claimed for this dependant on line 58160 of your Form ON428, if any", line 5
        # "Allowable amount for this dependant: line 3 minus line 4 (if negative, enter "0")" and
        # line 6 "Add the amounts from line 5 of columns 1, 2, and 3 (and others, if any). Enter
        # this amount on line 58185 of your Form ON428."
        CapabilitySelection(
            name="ca-on/caregiver_amount",
            params={
                "base": "ca-on/caregiver_base_amount",
                "maximum": "ca-on/caregiver_maximum_amount",
            },
            consumes={
                "dependants": "ca-on/caregiver_dependants",
                "eligible_dependant_amount": "ca-on/eligible_dependant_amount",
            },
            produces={"output": "ca-on/caregiver_amount"},
        ),
        # T1 line 108 "Amount from line 23600" "multiplied by 3%": 3% of the net income.
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca/medical_net_income_rate"},
            consumes={"base": "ca/net_income"},
            produces={"output": "ca/medical_net_income_share"},
        ),
        # T1 line 109 "Enter whichever is less: $2,834 or the amount from line 108."
        CapabilitySelection(
            name="core/capped_amount",
            params={"cap": "ca/medical_threshold_ceiling"},
            consumes={"base": "ca/medical_net_income_share"},
            produces={"output": "ca/medical_threshold"},
        ),
        # T1 line 107 and line 33099 "Medical expenses for self, spouse or common-law partner and
        # your dependent children under 18 years of age", a caller input, and line 110 "Line 107
        # minus line 109 (if negative, enter "0")".
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={"amount": "ca/medical_expenses", "less": "ca/medical_threshold"},
            produces={"output": "ca/medical_expenses_over_threshold"},
        ),
        # T1 line 111 and line 33199 "Allowable amount of medical expenses for other dependants
        # (use Federal Worksheet)"; Federal Worksheet, line 33199, for each dependant: line 1
        # "Medical expenses for other dependant", line 2 "For provinces and territories other
        # than Quebec: amount from line 109 of the dependant's return.", line 3 "Line 1 minus
        # line 2 (if negative, enter "0")", and line 4 "Add the amounts from line 3 of columns 1,
        # 2, and 3 (and others, if any). Enter this amount on line 33199 of your return."
        CapabilitySelection(
            name="ca/other_dependants_medical",
            params={"reduction": "ca/other_dependants_medical_reduction"},
            consumes={"dependants": "ca/other_dependants"},
            produces={"output": "ca/other_dependants_medical"},
        ),
        # T1 line 112 and line 33200 "Line 110 plus line 111".
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": ("ca/medical_expenses_over_threshold", "ca/other_dependants_medical")
            },
            produces={"output": "ca/medical_claim"},
        ),
        # T1 line 33500 (lines 30000, 30100, 30300, 30400, 30425, 30450, 30500, 30800, 31200, 31260,
        # 31800, 33200) and ON428 line 58800 (lines 58040, 58080, 58120, 58160, 58185, 58240,
        # 58300, 58769), in the forms' line order. T1 line 113 and line 33500 is "Line 106 plus
        # line 112", and line 112 (line 33200) follows the lines that line 106 adds; ON428 line 44
        # and line 58800 is "Line 35 plus line 43", and line 43 (line 58769) follows the lines
        # that line 35 adds. ON428 lines 58240 and 58300 are "Amount from line 30800 / 31200 of
        # your return", so the Ontario sum reads the federal kinds; it has no Canada employment
        # amount.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/basic_personal_amount",
                    "ca/age_amount",
                    "ca/spouse_amount",
                    "ca/eligible_dependant_amount",
                    "ca/spouse_caregiver_amount",
                    "ca/caregiver_amount",
                    "ca/infirm_children_amount",
                    "ca/cpp_base_contributions",
                    "ca/ei_premiums",
                    "ca/canada_employment_amount",
                    "ca/disability_transferred_amount",
                    "ca/medical_claim",
                )
            },
            produces={"output": "ca/non_refundable_credit_amounts"},
        ),
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca-on/basic_personal_amount",
                    "ca-on/age_amount",
                    "ca-on/spouse_amount",
                    "ca-on/eligible_dependant_amount",
                    "ca-on/caregiver_amount",
                    "ca/cpp_base_contributions",
                    "ca/ei_premiums",
                    "ca-on/medical_claim",
                )
            },
            produces={"output": "ca-on/non_refundable_credit_amounts"},
        ),
        # Schedule 9 chart for line 33700 "Gifts of capital property that is depreciable property",
        # line 4 "Enter whichever is less: amount from line 2 or line 3.": the net proceeds of
        # disposition of the property donated in 2025 (line 2) and its capital cost (line 3), caller
        # inputs for the one class and property the return claims.
        CapabilitySelection(
            name="core/lesser_of",
            params={},
            consumes={
                "amounts": ("ca/depreciable_gift_net_proceeds", "ca/depreciable_gift_capital_cost")
            },
            produces={"output": "ca/depreciable_gift_proceeds_or_cost"},
        ),
        # Schedule 9 chart for line 33700, line 5 "Enter whichever is less: amount from line 1 or
        # line 4. Enter this amount on line 33700 of the previous page.": line 1 "Amount of
        # recaptured depreciation included on your 2025 return" is a caller input. This is the
        # previous page's line B, "Gifts of capital property that are depreciable property".
        CapabilitySelection(
            name="core/lesser_of",
            params={},
            consumes={
                "amounts": (
                    "ca/depreciable_gift_recaptured_depreciation",
                    "ca/depreciable_gift_proceeds_or_cost",
                )
            },
            produces={"output": "ca/depreciable_gifts"},
        ),
        # Schedule 9 chart for line 33900 "Gifts of capital property", line 3 "Line 1 minus Line 2
        # Enter this amount on line 33900 on the previous page.": line 1 "Amount of current-year
        # taxable capital gains from capital property donated in 2025" and line 2 "Amount of
        # current-year capital gains deduction from capital property donated in 2025" are caller
        # inputs. This is the previous page's line C, "Gifts of capital property".
        CapabilitySelection(
            name="core/subtract",
            params={},
            consumes={
                "amount": "ca/capital_gift_taxable_gains",
                "less": "ca/capital_gift_gains_deduction",
            },
            produces={"output": "ca/capital_property_gifts"},
        ),
        # Schedule 9 line 5 "Add lines 1 to 4. Total eligible amount of charitable donations": line
        # 1 donations to registered charities and similar organizations, line 2 (line 32900)
        # donations to the Government of Canada, a province or territory and similar bodies, line 3
        # (line 33300) donations to registered universities outside Canada and line 4 (line 33400)
        # donations to the United Nations and its agencies and registered foreign charities, caller
        # inputs taken as the receipts state them, with any unused donations of the previous five
        # years that the filer chooses to claim.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/charitable_donations",
                    "ca/government_donations",
                    "ca/university_donations_outside_canada",
                    "ca/foreign_charity_donations",
                )
            },
            produces={"output": "ca/total_charitable_donations"},
        ),
        # Schedule 9 line 6 "Enter your net income from line 23600 of your return. Line A"
        # "multiplied by 75%": 75% of the net income.
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca/donation_net_income_rate"},
            consumes={"base": "ca/net_income"},
            produces={"output": "ca/donation_limit_on_net_income"},
        ),
        # Schedule 9 line 7 "Amount B plus amount C Line D" "multiplied by 25%": line D is the gifts
        # of capital property that are depreciable property (line B, line 33700) plus the gifts of
        # capital property (line C, line 33900), and line 7 is 25% of it.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca/depreciable_gifts", "ca/capital_property_gifts")},
            produces={"output": "ca/capital_gifts_total"},
        ),
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca/capital_gifts_limit_rate"},
            consumes={"base": "ca/capital_gifts_total"},
            produces={"output": "ca/capital_gifts_limit_addition"},
        ),
        # Schedule 9 line 8 "Line 6 plus line 7".
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": ("ca/donation_limit_on_net_income", "ca/capital_gifts_limit_addition")
            },
            produces={"output": "ca/donation_limit_with_capital_gifts"},
        ),
        # Schedule 9 line 9 "Enter whichever is less: amount A or line 8. Total charitable donations
        # limit": amount A is the net income of line 6, so the 25% of the gifts of capital property
        # can raise the limit above 75% of the net income, but not above the net income itself.
        CapabilitySelection(
            name="core/lesser_of",
            params={},
            consumes={"amounts": ("ca/net_income", "ca/donation_limit_with_capital_gifts")},
            produces={"output": "ca/charitable_donations_limit"},
        ),
        # Schedule 9 line 10 and line 34000 "Enter whichever is less: amount from line 5 or line 9."
        CapabilitySelection(
            name="core/lesser_of",
            params={},
            consumes={
                "amounts": ("ca/total_charitable_donations", "ca/charitable_donations_limit")
            },
            produces={"output": "ca/charitable_donations_claimed"},
        ),
        # Schedule 9 line 11 and line 34200 "Eligible amount of ecological gifts and cultural gifts
        # (see Guide P113)", a caller input, and line 12 "Line 10 plus line 11".
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": ("ca/charitable_donations_claimed", "ca/ecological_and_cultural_gifts")
            },
            produces={"output": "ca/donations_and_gifts_total"},
        ),
        # Schedule 9 line 13 "Enter whichever is less: amount from line 12 or $200.": the $200 is a
        # dataset, claimed whole.
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca/donation_first_tier_maximum"},
            consumes={},
            produces={"output": "ca/donation_first_tier_maximum"},
        ),
        CapabilitySelection(
            name="core/lesser_of",
            params={},
            consumes={
                "amounts": ("ca/donations_and_gifts_total", "ca/donation_first_tier_maximum")
            },
            produces={"output": "ca/donations_first_tier"},
        ),
        # Schedule 9 line 14 "Line 12 minus line 13".
        CapabilitySelection(
            name="core/subtract",
            params={},
            consumes={"amount": "ca/donations_and_gifts_total", "less": "ca/donations_first_tier"},
            produces={"output": "ca/donations_over_first_tier"},
        ),
        # Schedule 9 line 15 and line 34210 "Total ecological gifts made after February 10, 2014,
        # and before 2016 included in the amount on line 11", a caller input, and line 16 "Line 14
        # minus line 15 (if negative, enter "0")".
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={
                "amount": "ca/donations_over_first_tier",
                "less": "ca/ecological_gifts_before_2016",
            },
            produces={"output": "ca/donations_over_first_tier_after_2016_gifts"},
        ),
        # Schedule 9 line 18 "Income threshold 253,414.00": the dataset becomes an artifact of the
        # same name.
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca/donation_high_income_threshold"},
            consumes={},
            produces={"output": "ca/donation_high_income_threshold"},
        ),
        # Schedule 9 line 17 "Enter your taxable income from line 26000 of your return." and line 19
        # "Line 17 minus line 18 (if negative, enter "0")".
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={"amount": "ca/taxable_income", "less": "ca/donation_high_income_threshold"},
            produces={"output": "ca/taxable_income_over_donation_threshold"},
        ),
        # Schedule 9 line 20 "Enter whichever is less: amount from line 16 or line 19. Line F"
        # "multiplied by 33%": line F, then 33% of it.
        CapabilitySelection(
            name="core/lesser_of",
            params={},
            consumes={
                "amounts": (
                    "ca/donations_over_first_tier_after_2016_gifts",
                    "ca/taxable_income_over_donation_threshold",
                )
            },
            produces={"output": "ca/high_income_donations"},
        ),
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca/donation_high_income_rate"},
            consumes={"base": "ca/high_income_donations"},
            produces={"output": "ca/high_income_donation_credit"},
        ),
        # Schedule 9 line 21 "Amount E minus amount F Line G" "multiplied by 29%": amount E is the
        # amount from line 14 of the previous page and amount F is line F; line G, then 29% of it.
        CapabilitySelection(
            name="core/subtract",
            params={},
            consumes={"amount": "ca/donations_over_first_tier", "less": "ca/high_income_donations"},
            produces={"output": "ca/regular_rate_donations"},
        ),
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca/donation_regular_rate"},
            consumes={"base": "ca/regular_rate_donations"},
            produces={"output": "ca/regular_rate_donation_credit"},
        ),
        # Schedule 9 line 22 "Amount from line 13 of the previous page Line H" "multiplied by
        # 14.5%".
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca/donation_first_tier_rate"},
            consumes={"base": "ca/donations_first_tier"},
            produces={"output": "ca/first_tier_donation_credit"},
        ),
        # Schedule 9 line 23 "Add lines 20 to 22. Enter this amount on line 34900 of your return.
        # Allowable donations for 2025", T1 line 116 (line 34900) "Donations and gifts (complete
        # Schedule 9)".
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/high_income_donation_credit",
                    "ca/regular_rate_donation_credit",
                    "ca/first_tier_donation_credit",
                )
            },
            produces={"output": "ca/donations_and_gifts_credit"},
        ),
        # T1 line 115 (line 33800) "Line 113 multiplied by the percentage from line 114": the
        # federal credit rate is applied once, to the total of credit amounts. It is the first of
        # the three lines that line 35000 adds, and the base of the top-up tax credit.
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca/credit_rate"},
            consumes={"base": "ca/non_refundable_credit_amounts"},
            produces={"output": "ca/credit_amounts_at_credit_rate"},
        ),
        # ON428 line 46 (line 58840) "Line 44 multiplied by the percentage from line 45": the
        # Ontario credit rate is applied once, to the total of credit amounts. It is the first of
        # the two lines that line 50 adds.
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca-on/credit_rate"},
            consumes={"base": "ca-on/non_refundable_credit_amounts"},
            produces={"output": "ca-on/credit_amounts_at_credit_rate"},
        ),
        # ON428 line 47 "Amount from line 13 of your federal Schedule 9" "multiplied by 5.05%":
        # 5.05% of the first $200 of the donations and gifts, the federal Schedule 9 line 13.
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca-on/donation_first_tier_rate"},
            consumes={"base": "ca/donations_first_tier"},
            produces={"output": "ca-on/donations_first_tier_credit"},
        ),
        # ON428 line 48 "Amount from line 14 of your federal Schedule 9" "multiplied by 11.16%":
        # 11.16% of the rest of the donations and gifts, the federal Schedule 9 line 14.
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca-on/donation_over_first_tier_rate"},
            consumes={"base": "ca/donations_over_first_tier"},
            produces={"output": "ca-on/donations_over_first_tier_credit"},
        ),
        # ON428 line 49 and line 58969 "Line 47 plus line 48".
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca-on/donations_first_tier_credit",
                    "ca-on/donations_over_first_tier_credit",
                )
            },
            produces={"output": "ca-on/donations_and_gifts_credit"},
        ),
        # ON428 line 50 and line 61500 "Line 46 plus line 49 Enter this amount on line 52.
        # Ontario non-refundable tax credits": line 46 (line 58840) and line 49 (line 58969), in
        # line order.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": ("ca-on/credit_amounts_at_credit_rate", "ca-on/donations_and_gifts_credit")
            },
            produces={"output": "ca-on/non_refundable_tax_credits"},
        ),
        # Federal Worksheet 5000-D1, "Line 34990 - Top-up tax credit": line 1 "Amount from line
        # 33800 of your return", line 2 "Amount from line 22 of your Schedule 9" and line 3 "Line 1
        # plus line 2".
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": ("ca/credit_amounts_at_credit_rate", "ca/first_tier_donation_credit")
            },
            produces={"output": "ca/top_up_credits_base"},
        ),
        # Federal Worksheet 5000-D1, "Line 34990 - Top-up tax credit", line 4 "8,319.38": the
        # dataset becomes an artifact of the same name; line 5 "Line 3 minus line 4 (if negative,
        # enter "0")".
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca/top_up_threshold"},
            consumes={},
            produces={"output": "ca/top_up_threshold"},
        ),
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={"amount": "ca/top_up_credits_base", "less": "ca/top_up_threshold"},
            produces={"output": "ca/top_up_excess"},
        ),
        # Federal Worksheet 5000-D1, "Line 34990 - Top-up tax credit", line 6 "Applicable rate
        # 3.45%" and line 7 "Line 5 multiplied by the percentage from line 6 Enter this amount on
        # line 34990 of your return.", T1 line 117 (line 34990) "Top-up tax credit (use Federal
        # Worksheet)".
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca/top_up_rate"},
            consumes={"base": "ca/top_up_excess"},
            produces={"output": "ca/top_up_tax_credit"},
        ),
        # T1 line 118 (line 35000) "Add lines 115 to 117. Total federal non-refundable tax credits":
        # line 115 (line 33800), line 116 (line 34900) and line 117 (line 34990), in line order.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/credit_amounts_at_credit_rate",
                    "ca/donations_and_gifts_credit",
                    "ca/top_up_tax_credit",
                )
            },
            produces={"output": "ca/non_refundable_tax_credits"},
        ),
        # T1 line 123 (40425) "Federal dividend tax credit (use Federal Worksheet)": the Federal
        # Worksheet's "Line 40425 - Federal dividend tax credit", line 5 "Add lines 1 to 4." of
        # the credits shown on the T3, T4PS, T5 and T5013 slips. For dividends with no
        # information slip, line A "Amount from line 12000 of your return (Note 1)" and line B
        # "Amount from line 12010 of your return (Note 1)", Note 1 being "Enter only the amount
        # of dividends that were not shown on an information slip.", so line A is the
        # Worksheet's line 17 and line B its line 16, each its own step; line 6 is "Line B,
        # multiplied by 9.0301%"; line C is "Amount A minus amount B", and line 7 (printed
        # "Line 2") is line C "multiplied by 15.0198%"; line 8 is "Line 6 plus line 7" and
        # line 9 "Line 5 plus line 8 Enter this amount on line 40425 of your return."
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/t3_dividend_tax_credit",
                    "ca/t4ps_dividend_tax_credit",
                    "ca/t5_dividend_tax_credit",
                    "ca/t5013_dividend_tax_credit",
                )
            },
            produces={"output": "ca/slip_dividend_tax_credit"},
        ),
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca/dividends_without_a_slip_grossed_up",)},
            produces={"output": "ca/dividends_amount_a"},
        ),
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca/other_dividends_grossed_up",)},
            produces={"output": "ca/dividends_amount_b"},
        ),
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca/dividend_credit_rate_other_than_eligible"},
            consumes={"base": "ca/dividends_amount_b"},
            produces={"output": "ca/other_dividends_credit"},
        ),
        CapabilitySelection(
            name="core/subtract",
            params={},
            consumes={"amount": "ca/dividends_amount_a", "less": "ca/dividends_amount_b"},
            produces={"output": "ca/dividends_amount_a_less_b"},
        ),
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca/dividend_credit_rate_eligible"},
            consumes={"base": "ca/dividends_amount_a_less_b"},
            produces={"output": "ca/eligible_dividends_credit"},
        ),
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca/other_dividends_credit", "ca/eligible_dividends_credit")},
            produces={"output": "ca/no_slip_dividend_tax_credit"},
        ),
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca/slip_dividend_tax_credit", "ca/no_slip_dividend_tax_credit")},
            produces={"output": "ca/dividend_tax_credit"},
        ),
        # T1 line 125 "Add lines 122 to 124.": line 122 "Amount from line 35000" and line 123
        # (40425), in line order; line 124 (40427, minimum tax carryover) is not triggered.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca/non_refundable_tax_credits", "ca/dividend_tax_credit")},
            produces={"output": "ca/credits_against_basic_federal_tax"},
        ),
        # Each form's credits come off its basic tax, not below zero: the unused part is lost.
        # Federally the credits are line 125 (T1 line 126 "Line 121 minus line 125 (if negative,
        # enter "0")").
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={
                "amount": "ca/federal_basic_tax",
                "less": "ca/credits_against_basic_federal_tax",
            },
            produces={"output": "ca/federal_tax_after_credits"},
        ),
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={
                "amount": "ca-on/ontario_basic_tax",
                "less": "ca-on/non_refundable_tax_credits",
            },
            produces={"output": "ca-on/ontario_tax_after_credits"},
        ),
        # ON428 lines 66 to 68: the surtax on line 65, which is the Ontario tax after credits
        # while line 64 (tax on split income) is not modelled.
        CapabilitySelection(
            name="core/tiered_surcharge",
            params={"tiers": "ca-on/surtax"},
            consumes={"base": "ca-on/ontario_tax_after_credits"},
            produces={"output": "ca-on/ontario_surtax"},
        ),
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca-on/ontario_tax_after_credits", "ca-on/ontario_surtax")},
            produces={"output": "ca-on/ontario_tax_with_surtax"},
        ),
        # ON428 line 56 "Enter the amount from line 53 above.", line 57 (printed "Line 57 and
        # line and line 61520") "Ontario dividend tax credit (use Worksheet ON428)" and line 58
        # "Line 56 minus line 57 (if negative, enter "0")". Worksheet ON428's "Line 61520 -
        # Ontario dividend tax credit": line A "Amount from line 12000 of your return" and line
        # 1 "Amount from line 12010 of your return Line B" "multiplied by 2.9863%", with no Note
        # 1, so A and B are the whole lines 12000 and 12010, each its own step; line 2 "Amount
        # A minus amount B Line C" "multiplied by 10%"; line 3 "Line 1 plus line 2 Enter this
        # amount on line 61520 of your Form ON428.", which is line 57.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca-on/ontario_tax_after_credits",)},
            produces={"output": "ca-on/ontario_tax_before_dividend_credit"},
        ),
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca/taxable_dividends",)},
            produces={"output": "ca-on/dividends_amount_a"},
        ),
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca/taxable_dividends_other_than_eligible",)},
            produces={"output": "ca-on/dividends_amount_b"},
        ),
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca-on/dividend_credit_rate_other_than_eligible"},
            consumes={"base": "ca-on/dividends_amount_b"},
            produces={"output": "ca-on/other_dividends_credit"},
        ),
        CapabilitySelection(
            name="core/subtract",
            params={},
            consumes={"amount": "ca-on/dividends_amount_a", "less": "ca-on/dividends_amount_b"},
            produces={"output": "ca-on/dividends_amount_a_less_b"},
        ),
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca-on/dividend_credit_rate_eligible"},
            consumes={"base": "ca-on/dividends_amount_a_less_b"},
            produces={"output": "ca-on/eligible_dividends_credit"},
        ),
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca-on/other_dividends_credit", "ca-on/eligible_dividends_credit")},
            produces={"output": "ca-on/dividend_tax_credit"},
        ),
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={
                "amount": "ca-on/ontario_tax_before_dividend_credit",
                "less": "ca-on/dividend_tax_credit",
            },
            produces={"output": "ca-on/ontario_tax_less_dividend_credit"},
        ),
        # ON428 line 70 "Ontario dividend tax credit from line 57" and line 71 "Line 69 minus
        # line 70 (if negative, enter "0")": line 71 is line 73, as line 72 (the additional tax
        # for minimum tax purposes) is not triggered.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca-on/dividend_tax_credit",)},
            produces={"output": "ca-on/dividend_credit_from_line_57"},
        ),
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={
                "amount": "ca-on/ontario_tax_with_surtax",
                "less": "ca-on/dividend_credit_from_line_57",
            },
            produces={"output": "ca-on/ontario_tax_after_dividend_credit"},
        ),
        # ON428 line 74 "Basic reduction 294.00": the dataset becomes an artifact of the same
        # name, the first part of line 77.
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca-on/tax_reduction_basic"},
            consumes={},
            produces={"output": "ca-on/tax_reduction_basic"},
        ),
        # ON428 line 75 (line 60969) "Number of dependent children multiplied by $544" and line
        # 76 (line 60970) "Number of dependants multiplied by $544".
        CapabilitySelection(
            name="core/per_unit_amount",
            params={"amount": "ca-on/tax_reduction_per_dependant"},
            consumes={"count": "ca-on/dependent_children"},
            produces={"output": "ca-on/tax_reduction_for_children"},
        ),
        CapabilitySelection(
            name="core/per_unit_amount",
            params={"amount": "ca-on/tax_reduction_per_dependant"},
            consumes={"count": "ca-on/dependants"},
            produces={"output": "ca-on/tax_reduction_for_dependants"},
        ),
        # ON428 line 77 "Add lines 74 to 76.", in line order.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca-on/tax_reduction_basic",
                    "ca-on/tax_reduction_for_children",
                    "ca-on/tax_reduction_for_dependants",
                )
            },
            produces={"output": "ca-on/tax_reduction_amounts"},
        ),
        # ON428 line 78 "Amount from line 77 above multiplied by 2", line 79 "Amount from line 73
        # above" and line 80 "Line 78 minus line 79 (if negative, enter "0") Ontario tax
        # reduction": line 73 is line 71, the Ontario tax after the dividend credit, while the
        # minimum tax (line 72) is not triggered.
        CapabilitySelection(
            name="core/multiple_over",
            params={"factor": "ca-on/tax_reduction_factor"},
            consumes={
                "amount": "ca-on/tax_reduction_amounts",
                "less": "ca-on/ontario_tax_after_dividend_credit",
            },
            produces={"output": "ca-on/ontario_tax_reduction"},
        ),
        # ON428 line 81 "Line 73 minus line 80 (if negative, enter "0")".
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={
                "amount": "ca-on/ontario_tax_after_dividend_credit",
                "less": "ca-on/ontario_tax_reduction",
            },
            produces={"output": "ca-on/ontario_tax_after_reduction"},
        ),
        # Schedule ON428-A line 3 "Line 1 plus line 2", line 1 "Amount from line 10100 of your
        # return" (line 2, line 10400, not triggered), and line 5 "Line 3 multiplied by the
        # percentage from line 4 (maximum $875)", line 4 "Applicable rate 5.05%": the rate on
        # employment income, before its maximum.
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca-on/lift_rate"},
            consumes={"base": "ca/employment_income"},
            produces={"output": "ca-on/lift_credit_before_maximum"},
        ),
        # Line 5's "(maximum $875)" and Part A line 14 "Amount from line 5 above (maximum
        # $875)".
        CapabilitySelection(
            name="core/capped_amount",
            params={"cap": "ca-on/lift_maximum"},
            consumes={"base": "ca-on/lift_credit_before_maximum"},
            produces={"output": "ca-on/lift_maximum_credit"},
        ),
        # Lines 15 to 19: line 15 "Amount from line 13 above", the adjusted net income, which is
        # net income (line 23600) while lines 7, 8, 10 and 11 are not triggered; line 16
        # "Individual income threshold 32,500.00"; line 17 "Line 15 minus line 16 (if negative,
        # enter "0")"; line 18 "Applicable rate 5%"; line 19 "Line 17 multiplied by the
        # percentage from line 18".
        CapabilitySelection(
            name="core/tiered_surcharge",
            params={"tiers": "ca-on/lift_reduction"},
            consumes={"base": "ca/net_income"},
            produces={"output": "ca-on/lift_reduction"},
        ),
        # Line 20 "Line 14 minus line 19 (if negative, enter "0") Enter this amount on line 62140
        # of your Form ON428.", ON428 line 85.
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={"amount": "ca-on/lift_maximum_credit", "less": "ca-on/lift_reduction"},
            produces={"output": "ca-on/lift_credit"},
        ),
        # ON428 line 86 "Line 84 minus line 85 (if negative, enter "0")": line 84 "Amount from line
        # 83 of the previous page" carries line 83 "Line 81 minus line 82 (if negative, enter "0")",
        # which is line 81 while line 82 (the provincial foreign tax credit) is not triggered.
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={"amount": "ca-on/ontario_tax_after_reduction", "less": "ca-on/lift_credit"},
            produces={"output": "ca-on/ontario_tax_after_lift_credit"},
        ),
        # ON428 line 87 and line 62150 "Enter the amount of qualifying donations that have also
        # been claimed as a charitable donation." "multiplied by 25%", under "Community food
        # program donation tax credit for farmers:": the donations are a caller input, taken as
        # entered.
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca-on/community_food_program_rate"},
            consumes={"base": "ca-on/community_food_program_donations"},
            produces={"output": "ca-on/community_food_program_credit"},
        ),
        # ON428 line 88 "Line 86 minus line 87 (if negative, enter "0")".
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={
                "amount": "ca-on/ontario_tax_after_lift_credit",
                "less": "ca-on/community_food_program_credit",
            },
            produces={"output": "ca-on/ontario_tax_after_food_credit"},
        ),
        # ON428 line 89 "Ontario health premium (complete the chart below)": the chart's tiers on
        # line 1 "Enter your taxable income from line 26000 of your return", each the previous
        # plateau plus a rate on the income over its threshold, at most the next plateau.
        CapabilitySelection(
            name="core/tiered_surcharge",
            params={"tiers": "ca-on/health_premium"},
            consumes={"base": "ca/taxable_income"},
            produces={"output": "ca-on/ontario_health_premium"},
        ),
        # ON428 line 90 "Line 88 plus line 89 Enter this amount on line 42800 of your return.
        # Ontario tax".
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": ("ca-on/ontario_tax_after_food_credit", "ca-on/ontario_health_premium")
            },
            produces={"output": "ca-on/ontario_tax"},
        ),
        # T2038(IND) Part C "Recapture", "Amount of expenditure on which ITC earned at 15% (after
        # 2013) is recaptured. Do not enter more than the amount of the original expenditure" (line
        # 67193), times 0.15, amount 1: the caller's line 67193 at 15%.
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca/itc_recapture_rate_after_2013"},
            consumes={"base": "ca/itc_recapture_expenditure_at_15_percent"},
            produces={"output": "ca/itc_recapture_at_15_percent"},
        ),
        # Line 67195 "Amount of expenditure on which ITC earned at 20% (before 2014) is recaptured.
        # Do not enter more than the amount of the original expenditure", times 0.20, amount 2: the
        # caller's line 67195 at 20%.
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca/itc_recapture_rate_before_2014"},
            consumes={"base": "ca/itc_recapture_expenditure_at_20_percent"},
            produces={"output": "ca/itc_recapture_at_20_percent"},
        ),
        # "Total recapture of investment tax credit on SR&ED expenditures (add amounts 1 and 2)
        # Enter this amount on the Recapture of investment tax credit line of your income tax and
        # benefit return" (amount 3), T1 line 131 "Recapture of investment tax credit (complete Form
        # T2038(IND))": amounts 1 and 2 added.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": ("ca/itc_recapture_at_15_percent", "ca/itc_recapture_at_20_percent")
            },
            produces={"output": "ca/itc_recapture"},
        ),
        # T1 line 132 "Line 130 plus line 131 =": line 126 (42900) "Basic federal tax" and line 131.
        # Line 127 "Federal surtax on income earned outside Canada (complete Form T2203)" is not
        # triggered on a return whose income is all allocated to Ontario and line 129 (40500) is not
        # yet wired, so lines 128 and 130 carry line 126 unchanged.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca/federal_tax_after_credits", "ca/itc_recapture")},
            produces={"output": "ca/federal_tax_with_itc_recapture"},
        ),
        # T1 line 135 and line 41000 "Total federal political contributions (attach receipts) Line
        # 40900" is a caller input, ca/political_contributions, taken as the T1 takes it; the
        # Federal Worksheet "Line 41000 - Federal political contribution tax credit" reads it as
        # line 40900 and builds each of its three columns as printed, then the one that applies is
        # picked.
        # Federal Worksheet "Column 1: Line 40900 is $400 or less".
        # Line 2: 0.00, a printed constant.
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca/political_credit_column_1_line_2"},
            consumes={},
            produces={"output": "ca/political_credit_column_1_line_2"},
        ),
        # Column 1 line 3 "Line 1 minus line 2 (if negative, enter "0") =", line 1 being the
        # contributions.
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={
                "amount": "ca/political_contributions",
                "less": "ca/political_credit_column_1_line_2",
            },
            produces={"output": "ca/political_credit_column_1_line_3"},
        ),
        # Column 1 line 4 "Rate 75%" and line 5 "Line 3 multiplied by the percentage from line 4 =".
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca/political_credit_column_1_line_4"},
            consumes={"base": "ca/political_credit_column_1_line_3"},
            produces={"output": "ca/political_credit_column_1_line_5"},
        ),
        # Column 1 line 6: 0.00, a printed constant.
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca/political_credit_column_1_line_6"},
            consumes={},
            produces={"output": "ca/political_credit_column_1_line_6"},
        ),
        # Column 1 line 7 "Line 5 plus line 6 Enter this amount on line 41000 of your return. =".
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/political_credit_column_1_line_5",
                    "ca/political_credit_column_1_line_6",
                ),
            },
            produces={"output": "ca/political_credit_column_1_line_7"},
        ),
        # Federal Worksheet "Column 2: Line 40900 is more than $400 but not more than $750".
        # Line 2: 400.00, a printed constant.
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca/political_credit_column_2_line_2"},
            consumes={},
            produces={"output": "ca/political_credit_column_2_line_2"},
        ),
        # Column 2 line 3 "Line 1 minus line 2 (if negative, enter "0") =", line 1 being the
        # contributions.
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={
                "amount": "ca/political_contributions",
                "less": "ca/political_credit_column_2_line_2",
            },
            produces={"output": "ca/political_credit_column_2_line_3"},
        ),
        # Column 2 line 4 "Rate 50%" and line 5 "Line 3 multiplied by the percentage from line 4 =".
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca/political_credit_column_2_line_4"},
            consumes={"base": "ca/political_credit_column_2_line_3"},
            produces={"output": "ca/political_credit_column_2_line_5"},
        ),
        # Column 2 line 6: 300.00, a printed constant.
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca/political_credit_column_2_line_6"},
            consumes={},
            produces={"output": "ca/political_credit_column_2_line_6"},
        ),
        # Column 2 line 7 "Line 5 plus line 6 Enter this amount on line 41000 of your return. =".
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/political_credit_column_2_line_5",
                    "ca/political_credit_column_2_line_6",
                ),
            },
            produces={"output": "ca/political_credit_column_2_line_7"},
        ),
        # Federal Worksheet "Column 3: Line 40900 is more than more than $750".
        # Line 2: 750.00, a printed constant.
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca/political_credit_column_3_line_2"},
            consumes={},
            produces={"output": "ca/political_credit_column_3_line_2"},
        ),
        # Column 3 line 3 "Line 1 minus line 2 (if negative, enter "0") =", line 1 being the
        # contributions.
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={
                "amount": "ca/political_contributions",
                "less": "ca/political_credit_column_3_line_2",
            },
            produces={"output": "ca/political_credit_column_3_line_3"},
        ),
        # Column 3 line 4 "Rate 33.33%" and line 5 "Line 3 multiplied by the percentage from line 4
        # =".
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca/political_credit_column_3_line_4"},
            consumes={"base": "ca/political_credit_column_3_line_3"},
            produces={"output": "ca/political_credit_column_3_line_5"},
        ),
        # Column 3 line 6: 475.00, a printed constant.
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca/political_credit_column_3_line_6"},
            consumes={},
            produces={"output": "ca/political_credit_column_3_line_6"},
        ),
        # Column 3 line 7 "Line 5 plus line 6 Enter this amount on line 41000 of your return. =".
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/political_credit_column_3_line_5",
                    "ca/political_credit_column_3_line_6",
                ),
            },
            produces={"output": "ca/political_credit_column_3_line_7"},
        ),
        # The column that applies, "Use column 1 if the amount from line 40900 is $400 or less. Use
        # column 2 if the amount from line 40900 is more than $400 but not more than $750. Use
        # column 3 if the amount from line 40900 is more than $750.": the limits are the columns'
        # own line 2 constants, which their headings print again.
        CapabilitySelection(
            name="ca-on/choose_by_range",
            params={},
            consumes={
                "amount": "ca/political_contributions",
                "first_limit": "ca/political_credit_column_2_line_2",
                "second_limit": "ca/political_credit_column_3_line_2",
                "first": "ca/political_credit_column_1_line_7",
                "second": "ca/political_credit_column_2_line_7",
                "third": "ca/political_credit_column_3_line_7",
            },
            produces={"output": "ca/political_credit_chosen_column"},
        ),
        # The shortcut, "If your total federal political contributions from line 40900 of your
        # return were" "$1,275 or more, enter $650 on line 41000 of your return. If not, use the
        # amount from line 40900 of your return to decide which column to complete.": the printed
        # 1,275 and 650 are datasets. Nothing compares two amounts yet, so the same chooser tests
        # the 1,275 against the contributions: when it is at most the contributions it chooses the
        # 650, otherwise the chosen column's line 7. A chooser's six artifact slots must be six
        # different artifacts, so the middle range is given column 3's line 2 (750) as its limit
        # and column 3's line 7 as its value: 1,275 is never at most 750, so it is never chosen.
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca/political_credit_shortcut_threshold"},
            consumes={},
            produces={"output": "ca/political_credit_shortcut_threshold"},
        ),
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca/political_credit_shortcut_amount"},
            consumes={},
            produces={"output": "ca/political_credit_shortcut_amount"},
        ),
        CapabilitySelection(
            name="ca-on/choose_by_range",
            params={},
            consumes={
                "amount": "ca/political_credit_shortcut_threshold",
                "first_limit": "ca/political_contributions",
                "second_limit": "ca/political_credit_column_3_line_2",
                "first": "ca/political_credit_shortcut_amount",
                "second": "ca/political_credit_column_3_line_7",
                "third": "ca/political_credit_chosen_column",
            },
            produces={"output": "ca/political_credit_before_maximum"},
        ),
        # T1 line 135 and line 41000 "(maximum $650)", after the worksheet's line 7 or the
        # shortcut's $650.
        CapabilitySelection(
            name="core/capped_amount",
            params={"cap": "ca/political_credit_maximum"},
            consumes={"base": "ca/political_credit_before_maximum"},
            produces={"output": "ca/political_credit"},
        ),
        # T1 line 137 and line 41400 "Labour-sponsored funds tax credit Line 41300: Net cost of
        # shares of a provincially registered fund Line 41300: Allowable credit": the guide's "Claim
        # the amount of your allowable credit on line 41400 of your return that is equal to 15% of
        # the net cost reported on line 41300 of your return, to a maximum of $750." is 15% of line
        # 41300, the caller's net cost.
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca/labour_sponsored_funds_rate"},
            consumes={"base": "ca/labour_sponsored_funds_net_cost"},
            produces={"output": "ca/labour_sponsored_funds_credit_before_maximum"},
        ),
        # The guide's "to a maximum of $750" comes after the percentage, so it caps the credit.
        CapabilitySelection(
            name="core/capped_amount",
            params={"cap": "ca/labour_sponsored_funds_maximum"},
            consumes={"base": "ca/labour_sponsored_funds_credit_before_maximum"},
            produces={"output": "ca/labour_sponsored_funds_credit"},
        ),
        # T1 line 138 (line 41600) "Add lines 135 to 137.": line 135 (41000, the federal political
        # contribution tax credit) and line 137 (41400), in line order, as line 136 (41200, the
        # investment tax credit) is not yet wired.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": ("ca/political_credit", "ca/labour_sponsored_funds_credit"),
            },
            produces={"output": "ca/credits_against_federal_tax"},
        ),
        # T1 line 139 (line 41700) "Line 134 minus line 138 (if negative, enter "0")": line 134
        # (40600) "Line 132 minus line 133 (if negative, enter "0") Federal tax" carries line 132,
        # as line 133 (the federal logging tax credit) is not yet wired.
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={
                "amount": "ca/federal_tax_with_itc_recapture",
                "less": "ca/credits_against_federal_tax",
            },
            produces={"output": "ca/federal_tax_less_credits"},
        ),
        # Form T1172 Part A, line 3 "Amount from line 1 or 2, whichever is less": line 1 (68270)
        # "Total of all AIPs you received or the promoter had transferred to an RRSP, PRPP or SPP on
        # your behalf, during the year." and line 2 "Total amounts you or your promoter contributed
        # on your behalf to your RRSP, PRPP, or SPP, or the RRSP or SPP of your spouse or common-law
        # partner, in the year you received the AIPs or the first 60 days of the following year,
        # that you deducted on line 20800 of your income tax and benefit return for the year you
        # received the AIPs.", both the caller's.
        CapabilitySelection(
            name="core/lesser_of",
            params={},
            consumes={
                "amounts": ("ca/resp_aips_received_part_a", "ca/resp_aips_rrsp_contributions")
            },
            produces={"output": "ca/resp_aips_contributions_counted"},
        ),
        # Line 4 "Maximum lifetime RRSP contribution limit that can be used to reduce or eliminate
        # the amount of AIPs subject to the additional tax $ 50,000.00", the dataset as an artifact
        # of the same name.
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca/resp_aips_lifetime_limit"},
            consumes={},
            produces={"output": "ca/resp_aips_lifetime_limit"},
        ),
        # Line 6 "Line 4 minus line 5": line 5 "Total of all amounts used to reduce the amount of
        # additional tax payable on AIPs received in previous years (if applicable). This amount is
        # the total of the amount entered at line 5 of all T1172 forms you filed for 1998 and at
        # line 7 of all T1172 forms you filed for 1999 and later", the caller's, with no floor on
        # the line.
        CapabilitySelection(
            name="core/subtract",
            params={},
            consumes={
                "amount": "ca/resp_aips_lifetime_limit",
                "less": "ca/resp_aips_reduction_used_in_previous_years",
            },
            produces={"output": "ca/resp_aips_limit_remaining"},
        ),
        # Line 7 "Amount from line 3 or 6, whichever is less".
        CapabilitySelection(
            name="core/lesser_of",
            params={},
            consumes={
                "amounts": ("ca/resp_aips_contributions_counted", "ca/resp_aips_limit_remaining")
            },
            produces={"output": "ca/resp_aips_reduction"},
        ),
        # Line 8 "Amount of AIPs subject to the additional tax: line 1 minus line 7".
        CapabilitySelection(
            name="core/subtract",
            params={},
            consumes={"amount": "ca/resp_aips_received_part_a", "less": "ca/resp_aips_reduction"},
            produces={"output": "ca/resp_aips_subject_to_tax"},
        ),
        # Line 9 "Rate of the additional tax on AIPs" (20%) and line 10 "Additional tax on AIPs:
        # line 8 multiplied by line 9." (Part C, for a resident of Quebec on December 31, is not
        # triggered on an Ontario resident's return).
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca/resp_aips_part_a_rate"},
            consumes={"base": "ca/resp_aips_subject_to_tax"},
            produces={"output": "ca/resp_aips_part_a_tax"},
        ),
        # Part B "Fill out this part only if Part A does not apply to you.": line 11 (68280) "Total
        # of all AIPs you received from RESPs during the year.", the caller's, line 12 "Rate of the
        # additional tax on AIPs" (20%) and line 13 "Additional tax on AIPs: line 11 multiplied by
        # line 12.".
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca/resp_aips_part_b_rate"},
            consumes={"base": "ca/resp_aips_received_part_b"},
            produces={"output": "ca/resp_aips_part_b_tax"},
        ),
        # A count of 1 when Part A applies (a caller's 0 or 1, as the form takes the original
        # subscriber and the other listed cases) chooses line 10 over line 13, the amount the form
        # says to enter on line 41800; a count of 0 is Part B.
        CapabilitySelection(
            name="core/choose_by_count",
            params={},
            consumes={
                "count": "ca/resp_aips_part_a_applies",
                "when_none": "ca/resp_aips_part_b_tax",
                "when_any": "ca/resp_aips_part_a_tax",
            },
            produces={"output": "ca/resp_aips_additional_tax"},
        ),
        # T1 line 141 and line 41800 "Special taxes": the amount of Form T1172 (line 10 or 13) and
        # the RL-10 amount, the guide's "Report, on line 41800 of your return, the result of the
        # following calculation using your RL-10 slip: Tax Credit for a Labour-Sponsored Fund" whose
        # list the guide's .txt cuts off after "75% of box", so the amount is the caller's until the
        # rest is quoted (to be confirmed). The tax on excess EPSP amounts (Form RC359 line 9, per
        # employer) is not yet wired.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": ("ca/resp_aips_additional_tax", "ca/rl_10_labour_sponsored_fund_amount")
            },
            produces={"output": "ca/special_taxes"},
        ),
        # T1 line 142 (line 42000) "Add lines 139 to 141. Net federal tax": line 139 (41700), line
        # 140 (41500) "Advanced Canada workers benefit (ACWB) (complete Schedule 6)", the RC210 box
        # 10 amount the guide says to report, the caller's, and line 141 (41800), in line order.
        # Lines 120 and 124 (tax on split income, minimum tax carryover) are not modelled.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/federal_tax_less_credits",
                    "ca/advanced_canada_workers_benefit",
                    "ca/special_taxes",
                )
            },
            produces={"output": "ca/net_federal_tax"},
        ),
        # T1 line 148 (line 43500) "Add lines 143 to 147. Total payable": line 143 "Amount from
        # line 42000" and line 147 (42800), the Ontario tax, in line order; lines 144 to 146 are
        # not triggered.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca/net_federal_tax", "ca-on/ontario_tax")},
            produces={"output": "ca/total_payable"},
        ),
        # Schedule 6 line 5 "Add lines 1 to 4. Enter the result, even if it is "0". Working
        # income", line 1 "Employment income and other employment income from line 10100 and line
        # 10400 of the return" (line 10400 and lines 2 to 4 not triggered), carried by line 6
        # "Add the amounts from line 5 in columns 1 and 2. Enter this amount on line 16. Family
        # working income" with no eligible spouse: one part.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca/employment_income",)},
            produces={"output": "ca/working_income"},
        ),
        # Schedule 6 line 15 "Line 13 minus line 14 Enter this amount on line 23 and line 35.
        # Adjusted family net income": line 7 "Net income from line 23600 of the return", through
        # lines 10, 12 and 13 with lines 8, 9 and 11 not triggered and no eligible spouse (line
        # 14 not triggered): one part.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca/net_income",)},
            produces={"output": "ca/adjusted_family_net_income"},
        ),
        # Schedule 6 lines 16 to 22: line 16 "Family working income from line 6"; line 17 "Base
        # amount 3,000.00"; line 18 "Line 16 minus line 17 (if negative, enter "0")"; line 19
        # "Rate 27%"; line 20 "Line 18 multiplied by the percentage from line 19"; line 21 "If
        # you had an eligible spouse or an eligible dependant, enter $2,813. If not, enter
        # $1,633."; line 22 "Enter whichever is less: amount from line 20 or line 21.": one tier
        # with a maximum, with no eligible spouse or dependant.
        CapabilitySelection(
            name="core/tiered_surcharge",
            params={"tiers": "ca/cwb_basic"},
            consumes={"base": "ca/working_income"},
            produces={"output": "ca/cwb_before_reduction_without_dependant"},
        ),
        # The same lines with an eligible dependant: line 21's $2,813 as the tier's maximum.
        CapabilitySelection(
            name="core/tiered_surcharge",
            params={"tiers": "ca/cwb_basic_with_dependant"},
            consumes={"base": "ca/working_income"},
            produces={"output": "ca/cwb_before_reduction_with_dependant"},
        ),
        # Schedule 6 lines 23 to 27: line 23 "Adjusted family net income from line 15"; line 24
        # "If you had an eligible spouse or an eligible dependant, enter $30,639. If not, enter
        # $26,855."; line 25 "Line 23 minus line 24 (if negative, enter "0")"; line 26 "Rate
        # 15%"; line 27 "Line 25 multiplied by the percentage from line 26": one tier, with no
        # eligible spouse or dependant.
        CapabilitySelection(
            name="core/tiered_surcharge",
            params={"tiers": "ca/cwb_reduction"},
            consumes={"base": "ca/adjusted_family_net_income"},
            produces={"output": "ca/cwb_reduction_without_dependant"},
        ),
        # The same lines with an eligible dependant: line 24's $30,639 as the tier's threshold.
        CapabilitySelection(
            name="core/tiered_surcharge",
            params={"tiers": "ca/cwb_reduction_with_dependant"},
            consumes={"base": "ca/adjusted_family_net_income"},
            produces={"output": "ca/cwb_reduction_with_dependant"},
        ),
        # Schedule 6 line 28 "Line 22 minus line 27 (if negative, enter "0") If you are not
        # completing Step 3, enter this amount on line 45300 of your return.", with no eligible
        # spouse or dependant: Step 3 (the disability supplement) is not triggered.
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={
                "amount": "ca/cwb_before_reduction_without_dependant",
                "less": "ca/cwb_reduction_without_dependant",
            },
            produces={"output": "ca/canada_workers_benefit_without_dependant"},
        ),
        # Line 28 with an eligible dependant.
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={
                "amount": "ca/cwb_before_reduction_with_dependant",
                "less": "ca/cwb_reduction_with_dependant",
            },
            produces={"output": "ca/canada_workers_benefit_with_dependant"},
        ),
        # Line 28 for the filer's family status, which lines 21 and 24 read ("If you had an
        # eligible spouse or an eligible dependant ... If not ..."): the line with no eligible
        # spouse or dependant when the number of Schedule 6 eligible dependants (line 38100) is
        # 0, else the line with one; an eligible spouse is not modelled.
        CapabilitySelection(
            name="core/choose_by_count",
            params={},
            consumes={
                "count": "ca/cwb_eligible_dependants",
                "when_none": "ca/canada_workers_benefit_without_dependant",
                "when_any": "ca/canada_workers_benefit_with_dependant",
            },
            produces={"output": "ca/canada_workers_benefit"},
        ),
        # Form ON479 line 1 and line 61268 "Eligible medical expenses for fertility treatment
        # multiplied by 25% (maximum $5,000) =": the rate on the expenses, before its maximum.
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca-on/fertility_credit_rate"},
            consumes={"base": "ca-on/fertility_expenses"},
            produces={"output": "ca-on/fertility_credit_before_maximum"},
        ),
        # Line 1's "(maximum $5,000)", printed after the percentage, so it caps the credit.
        CapabilitySelection(
            name="core/capped_amount",
            params={"cap": "ca-on/fertility_credit_maximum"},
            consumes={"base": "ca-on/fertility_credit_before_maximum"},
            produces={"output": "ca-on/fertility_credit"},
        ),
        # Line 14 "Amount paid in the year for eligible seniors' use of Ontario public transit
        # services (maximum $3,000) Line 63100 multiplied by 15% =": the "(maximum $3,000)" is
        # printed before the percentage, so it caps the amount paid.
        CapabilitySelection(
            name="core/capped_amount",
            params={"cap": "ca-on/seniors_transit_maximum"},
            consumes={"base": "ca-on/seniors_transit_paid"},
            produces={"output": "ca-on/seniors_transit_amount_paid_at_most_maximum"},
        ),
        # Line 14's "multiplied by 15% =", on the capped amount.
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca-on/seniors_transit_rate"},
            consumes={"base": "ca-on/seniors_transit_amount_paid_at_most_maximum"},
            produces={"output": "ca-on/seniors_transit_credit"},
        ),
        # Form ON479 line 15 and line 63100 "Ontario political contributions made in 2025" is a
        # caller input, ca-on/political_contributions, taken as the form takes it; Worksheet ON479
        # "Line 16 - Ontario political contribution tax credit" reads it as line 63110 and builds
        # each of its three columns as printed, then the one that applies is picked.
        # Worksheet ON479 "Column 1: Line 63110 is $500.05 or less".
        # Line 2: 0.00, a printed constant.
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca-on/political_credit_column_1_line_2"},
            consumes={},
            produces={"output": "ca-on/political_credit_column_1_line_2"},
        ),
        # Column 1 line 3 "Line 1 minus line 2 (cannot be negative)", line 1 being the
        # contributions.
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={
                "amount": "ca-on/political_contributions",
                "less": "ca-on/political_credit_column_1_line_2",
            },
            produces={"output": "ca-on/political_credit_column_1_line_3"},
        ),
        # Column 1 line 4 "Rate 75%" and line 5 "Line 3 multiplied by the percentage from line 4".
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca-on/political_credit_column_1_line_4"},
            consumes={"base": "ca-on/political_credit_column_1_line_3"},
            produces={"output": "ca-on/political_credit_column_1_line_5"},
        ),
        # Column 1 line 6: 0.00, a printed constant.
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca-on/political_credit_column_1_line_6"},
            consumes={},
            produces={"output": "ca-on/political_credit_column_1_line_6"},
        ),
        # Column 1 line 7 "Line 5 plus line 6 Enter this amount on line 16 of your Form ON479.".
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca-on/political_credit_column_1_line_5",
                    "ca-on/political_credit_column_1_line_6",
                )
            },
            produces={"output": "ca-on/political_credit_column_1_line_7"},
        ),
        # Worksheet ON479 "Column 2: Line 63110 is more than $500.05 but not more than $1,666.82".
        # Line 2: 500.05, a printed constant.
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca-on/political_credit_column_2_line_2"},
            consumes={},
            produces={"output": "ca-on/political_credit_column_2_line_2"},
        ),
        # Column 2 line 3 "Line 1 minus line 2 (cannot be negative)", line 1 being the
        # contributions.
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={
                "amount": "ca-on/political_contributions",
                "less": "ca-on/political_credit_column_2_line_2",
            },
            produces={"output": "ca-on/political_credit_column_2_line_3"},
        ),
        # Column 2 line 4 "Rate 50%" and line 5 "Line 3 multiplied by the percentage from line 4".
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca-on/political_credit_column_2_line_4"},
            consumes={"base": "ca-on/political_credit_column_2_line_3"},
            produces={"output": "ca-on/political_credit_column_2_line_5"},
        ),
        # Column 2 line 6: 375.03, a printed constant.
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca-on/political_credit_column_2_line_6"},
            consumes={},
            produces={"output": "ca-on/political_credit_column_2_line_6"},
        ),
        # Column 2 line 7 "Line 5 plus line 6 Enter this amount on line 16 of your Form ON479.".
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca-on/political_credit_column_2_line_5",
                    "ca-on/political_credit_column_2_line_6",
                )
            },
            produces={"output": "ca-on/political_credit_column_2_line_7"},
        ),
        # Worksheet ON479 "Column 3: Line 63110 is more than $1,666.82".
        # Line 2: 1,666.82, a printed constant.
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca-on/political_credit_column_3_line_2"},
            consumes={},
            produces={"output": "ca-on/political_credit_column_3_line_2"},
        ),
        # Column 3 line 3 "Line 1 minus line 2 (cannot be negative)", line 1 being the
        # contributions.
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={
                "amount": "ca-on/political_contributions",
                "less": "ca-on/political_credit_column_3_line_2",
            },
            produces={"output": "ca-on/political_credit_column_3_line_3"},
        ),
        # Column 3 line 4 "Rate 33.33%" and line 5 "Line 3 multiplied by the percentage from line
        # 4".
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca-on/political_credit_column_3_line_4"},
            consumes={"base": "ca-on/political_credit_column_3_line_3"},
            produces={"output": "ca-on/political_credit_column_3_line_5"},
        ),
        # Column 3 line 6: 958.41, a printed constant.
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca-on/political_credit_column_3_line_6"},
            consumes={},
            produces={"output": "ca-on/political_credit_column_3_line_6"},
        ),
        # Column 3 line 7 "Line 5 plus line 6 Enter this amount on line 16 of your Form ON479.".
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca-on/political_credit_column_3_line_5",
                    "ca-on/political_credit_column_3_line_6",
                )
            },
            produces={"output": "ca-on/political_credit_column_3_line_7"},
        ),
        # The column that applies: column 1 if line 63110 is $500.05 or less, column 2 if it is more
        # than $500.05 but not more than $1,666.82, column 3 if it is more than $1,666.82. The
        # limits are the columns' own line 2 constants, which their headings print again.
        CapabilitySelection(
            name="ca-on/choose_by_range",
            params={},
            consumes={
                "amount": "ca-on/political_contributions",
                "first_limit": "ca-on/political_credit_column_2_line_2",
                "second_limit": "ca-on/political_credit_column_3_line_2",
                "first": "ca-on/political_credit_column_1_line_7",
                "second": "ca-on/political_credit_column_2_line_7",
                "third": "ca-on/political_credit_column_3_line_7",
            },
            produces={"output": "ca-on/political_credit_before_maximum"},
        ),
        # ON479 line 16 "(maximum $1,666.82)", after the chosen column's line 7.
        CapabilitySelection(
            name="core/capped_amount",
            params={"cap": "ca-on/political_credit_maximum"},
            consumes={"base": "ca-on/political_credit_before_maximum"},
            produces={"output": "ca-on/political_credit"},
        ),
        # Form T1221 lines 1 to 3 "Enter the amount of qualifying expenses." (one line for each
        # corporation or slip) and line 4 "Add lines 1 to 3. Enter this amount on line 63220 of
        # your Form ON479.": the expenses of every slip in the list, added.
        CapabilitySelection(
            name="ca-on/flow_through_share_expenses",
            params={},
            consumes={"slips": "ca-on/flow_through_share_slips"},
            produces={"output": "ca-on/flow_through_share_expenses"},
        ),
        # Form ON479 line 17 and line 63220 "Enter your total expenses from your Form T1221.
        # multiplied by 5% =": the 5% on T1221 line 4.
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca-on/flow_through_share_rate"},
            consumes={"base": "ca-on/flow_through_share_expenses"},
            produces={"output": "ca-on/flow_through_share_credit"},
        ),
        # Line 18 "Add lines 1, 2, 13, 14, 16, and 17. =": lines 1, 14, 16 and 17, in line order, as
        # lines 2 and 13 are not triggered.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca-on/fertility_credit",
                    "ca-on/seniors_transit_credit",
                    "ca-on/political_credit",
                    "ca-on/flow_through_share_credit",
                )
            },
            produces={"output": "ca-on/ontario_credits_subtotal"},
        ),
        # Worksheet ON479, "Line 20 - Ontario co-operative education tax credit", line 5
        # "400,000.00", the dataset as an artifact of the same name.
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca-on/coop_education_payroll_threshold"},
            consumes={},
            produces={"output": "ca-on/coop_education_payroll_threshold"},
        ),
        # Line 6 "Line 4 minus line 5 (if negative, enter "0")": line 4 "Total salaries and wages
        # paid in the 2024 taxation year" less the threshold.
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={
                "amount": "ca-on/coop_education_payroll",
                "less": "ca-on/coop_education_payroll_threshold",
            },
            produces={"output": "ca-on/coop_education_payroll_over_threshold"},
        ),
        # Line 7 "200,000.00", the dataset as an artifact of the same name.
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca-on/coop_education_payroll_range"},
            consumes={},
            produces={"output": "ca-on/coop_education_payroll_range"},
        ),
        # Line 8 "Line 6 divided by line 7".
        CapabilitySelection(
            name="ca-on/quotient",
            params={},
            consumes={
                "dividend": "ca-on/coop_education_payroll_over_threshold",
                "divisor": "ca-on/coop_education_payroll_range",
            },
            produces={"output": "ca-on/coop_education_phase_out_share"},
        ),
        # Line 9 "1.00", the dataset as an artifact of the same name.
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca-on/coop_education_full_share"},
            consumes={},
            produces={"output": "ca-on/coop_education_full_share"},
        ),
        # Line 11 "Line 9 minus line 10 (if negative, enter "0")": line 10 is "Amount from line 8
        # above", so line 8 itself is taken off line 9.
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={
                "amount": "ca-on/coop_education_full_share",
                "less": "ca-on/coop_education_phase_out_share",
            },
            produces={"output": "ca-on/coop_education_remaining_share"},
        ),
        # Lines 1, 3, 12 and 13 for each qualifying work placement, and ON479 line 20 and line
        # 63300 "Enter the total amount claimed for all qualifying work placements. (maximum
        # $3,000 per student)": the total of the placements' line 13.
        CapabilitySelection(
            name="ca-on/coop_education_credit",
            params={
                "expenditure_rate": "ca-on/coop_education_expenditure_rate",
                "supplement_rate": "ca-on/coop_education_supplement_rate",
                "maximum": "ca-on/coop_education_maximum",
            },
            consumes={
                "placements": "ca-on/coop_education_placements",
                "remaining_share": "ca-on/coop_education_remaining_share",
            },
            produces={"output": "ca-on/coop_education_credit"},
        ),
        # ON479 line 63260 "Number of eligible work placements your business or partnership is
        # claiming under the Ontario co-operative education tax credit program": the number of
        # placements in the list.
        CapabilitySelection(
            name="ca-on/record_count",
            params={},
            consumes={"records": "ca-on/coop_education_placements"},
            produces={"output": "ca-on/coop_education_placement_count"},
        ),
        # Line 21 "Line 19 plus line 20 Enter this amount online 47900 of your return. Ontario
        # credits =": line 19 "Amount from line 18 of the previous page" carries line 18, and
        # line 20 is the co-operative education credit.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca-on/ontario_credits_subtotal", "ca-on/coop_education_credit")},
            produces={"output": "ca-on/ontario_credits"},
        ),
        # T1 line 165 and line 47900 "Provincial or territorial credits (complete Form 479, if it
        # applies)": ON479 line 21, the Ontario credits.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca-on/ontario_credits",)},
            produces={"output": "ca/provincial_credits"},
        ),
        # T1 "Eligible educator school supply tax credit" line 161 and line 46900: "Supplies
        # expenses (maximum $1,000) Line 46800 multiplied by 25% =": the "(maximum $1,000)" is
        # printed before the percentage, so it caps the supplies expenses (line 46800).
        CapabilitySelection(
            name="core/capped_amount",
            params={"cap": "ca/educator_supplies_maximum"},
            consumes={"base": "ca/educator_supplies_expenses"},
            produces={"output": "ca/educator_supplies_expenses_at_most_maximum"},
        ),
        # Line 161's "multiplied by 25% =", on the capped supplies expenses.
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca/educator_supplies_rate"},
            consumes={"base": "ca/educator_supplies_expenses_at_most_maximum"},
            produces={"output": "ca/educator_school_supply_credit"},
        ),
        # T1 line 166 (line 48200) "Add lines 150 to 165. Total credits": line 150 (43700), line
        # 155 (45300) "Canada workers benefit (CWB) (complete Schedule 6)", line 159 (45600) "Part
        # XII.2 tax credit (box 38 of all T3 slips and box 209 of all T5013 slips)", line 160
        # (45700) "Employee and partner GST/HST rebate (complete Form GST370)", line 161 (46900),
        # line 162 (47555) "Canadian journalism labour tax credit (box 236 of all T5013 slips)",
        # line 164 (47600) "Tax paid by instalments" and line 165 (47900), in line order, as the
        # other lines are not triggered or not yet wired.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/income_tax_deducted",
                    "ca/canada_workers_benefit",
                    "ca/part_xii_2_tax_credit",
                    "ca/employee_and_partner_gst_hst_rebate",
                    "ca/educator_school_supply_credit",
                    "ca/journalism_labour_tax_credit",
                    "ca/tax_paid_by_instalments",
                    "ca/provincial_credits",
                )
            },
            produces={"output": "ca/total_credits"},
        ),
        # T1 line 167 "Line 149 minus line 166 If the amount is negative, enter it on line
        # 48400 below. If the amount is positive, enter it on line 48500 below. Refund or
        # balance owing": not floored, so a negative result is a refund and a positive one a
        # balance owing.
        CapabilitySelection(
            name="core/subtract",
            params={},
            consumes={"amount": "ca/total_payable", "less": "ca/total_credits"},
            produces={"output": "ca/refund_or_balance_owing"},
        ),
        # T1 line 48400 "Refund": line 167 is entered on line 48400 "If the amount is negative", so
        # the total credits less the total payable, not below zero, a refund and never a negative.
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={"amount": "ca/total_credits", "less": "ca/total_payable"},
            produces={"output": "ca/refund"},
        ),
        # The Ontario opportunities fund, on the T1 provincial pages, line 1 "Amount from line 48400
        # above": the refund.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca/refund",)},
            produces={"output": "ca-on/refund_before_donation"},
        ),
        # Line 3 and line 46600 "Net refund (line 1 minus line 2) =": line 1 less line 2 and line
        # 46500 "Your donation to the Ontario opportunities fund".
        CapabilitySelection(
            name="core/subtract",
            params={},
            consumes={
                "amount": "ca-on/refund_before_donation",
                "less": "ca-on/opportunities_fund_donation",
            },
            produces={"output": "ca-on/net_refund"},
        ),
    }
    assert len(found.capabilities) == 291


def test_its_first_tax_year_composes_every_selection() -> None:
    composition = service().compose(CA_ON, 2025)

    wiring = {
        (type(capability), capability.consumes, capability.produces)
        for capability in composition.order
    }
    assert len(composition.order) == 291
    assert wiring == {
        (ApplyRate, frozenset({CAPITAL_GAIN}), frozenset({TAXABLE_CAPITAL_GAINS})),
        (
            TieredContribution,
            frozenset({EMPLOYMENT_INCOME}),
            frozenset({CPP_BASE_CONTRIBUTIONS}),
        ),
        (
            TieredContribution,
            frozenset({EMPLOYMENT_INCOME}),
            frozenset({CPP_FIRST_ADDITIONAL_CONTRIBUTIONS}),
        ),
        (
            TieredContribution,
            frozenset({EMPLOYMENT_INCOME}),
            frozenset({CPP_SECOND_ADDITIONAL_CONTRIBUTIONS}),
        ),
        (TieredContribution, frozenset({EMPLOYMENT_INCOME}), frozenset({EI_PREMIUMS})),
        (
            Sum,
            frozenset({CPP_FIRST_ADDITIONAL_CONTRIBUTIONS, CPP_SECOND_ADDITIONAL_CONTRIBUTIONS}),
            frozenset({CPP_ENHANCED_CONTRIBUTIONS}),
        ),
        (
            Sum,
            frozenset(
                {
                    T3_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
                    T4PS_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
                    T5_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
                    T5013_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
                }
            ),
            frozenset({SLIP_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE}),
        ),
        (
            Sum,
            frozenset(
                {
                    T3_TAXABLE_DIVIDENDS,
                    T4PS_TAXABLE_DIVIDENDS,
                    T5_TAXABLE_DIVIDENDS,
                    T5013_TAXABLE_DIVIDENDS,
                }
            ),
            frozenset({SLIP_TAXABLE_DIVIDENDS}),
        ),
        (
            ApplyFraction,
            frozenset({ELIGIBLE_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP}),
            frozenset({ELIGIBLE_DIVIDENDS_GROSSED_UP}),
        ),
        (
            ApplyFraction,
            frozenset({OTHER_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP}),
            frozenset({OTHER_DIVIDENDS_GROSSED_UP}),
        ),
        (
            Sum,
            frozenset({ELIGIBLE_DIVIDENDS_GROSSED_UP, OTHER_DIVIDENDS_GROSSED_UP}),
            frozenset({DIVIDENDS_WITHOUT_A_SLIP_GROSSED_UP}),
        ),
        (
            Sum,
            frozenset({SLIP_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE, OTHER_DIVIDENDS_GROSSED_UP}),
            frozenset({TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE}),
        ),
        (
            Sum,
            frozenset({SLIP_TAXABLE_DIVIDENDS, DIVIDENDS_WITHOUT_A_SLIP_GROSSED_UP}),
            frozenset({TAXABLE_DIVIDENDS}),
        ),
        (
            Sum,
            frozenset(
                {
                    T3_INVESTMENT_INCOME,
                    T5_INVESTMENT_INCOME,
                    T5013_INVESTMENT_INCOME,
                    INVESTMENT_INCOME_CREDITED_NOT_RECEIVED,
                    TAX_REFUND_INTEREST,
                    FOREIGN_INVESTMENT_INCOME,
                    INVESTMENT_INCOME_WITHOUT_A_SLIP,
                    INVESTMENT_ROYALTIES,
                }
            ),
            frozenset({INVESTMENT_INCOME_BEFORE_PRIOR_YEARS}),
        ),
        (
            Subtract,
            frozenset(
                {INVESTMENT_INCOME_BEFORE_PRIOR_YEARS, INVESTMENT_INCOME_REPORTED_IN_PREVIOUS_YEARS}
            ),
            frozenset({INTEREST_AND_OTHER_INVESTMENT_INCOME}),
        ),
        (
            Sum,
            frozenset(
                {WORKERS_COMPENSATION_BENEFITS, SOCIAL_ASSISTANCE_PAYMENTS, NET_FEDERAL_SUPPLEMENTS}
            ),
            frozenset({INCOME_SUPPORT_BENEFITS}),
        ),
        (
            Sum,
            frozenset(
                {
                    EMPLOYMENT_INCOME,
                    OTHER_EMPLOYMENT_INCOME,
                    OLD_AGE_SECURITY,
                    CPP_OR_QPP_BENEFITS,
                    OTHER_PENSIONS_AND_SUPERANNUATION,
                    ELECTED_SPLIT_PENSION_AMOUNT,
                    UNIVERSAL_CHILD_CARE_BENEFIT,
                    EI_AND_OTHER_BENEFITS,
                    TAXABLE_DIVIDENDS,
                    INTEREST_AND_OTHER_INVESTMENT_INCOME,
                    NET_PARTNERSHIP_INCOME,
                    RDSP_INCOME,
                    TAXABLE_CAPITAL_GAINS,
                    TAXABLE_SUPPORT_PAYMENTS,
                    RRSP_INCOME,
                    FHSA_INCOME,
                    OTHER_FHSA_INCOME,
                    OTHER_INCOME,
                    TAXABLE_SCHOLARSHIPS,
                    INCOME_SUPPORT_BENEFITS,
                }
            ),
            frozenset({TOTAL_INCOME}),
        ),
        (
            Sum,
            frozenset({UNUSED_RRSP_CONTRIBUTIONS, RRSP_CONTRIBUTIONS}),
            frozenset({RRSP_CONTRIBUTIONS_AVAILABLE}),
        ),
        (
            LesserOf,
            frozenset({RRSP_CONTRIBUTIONS_AVAILABLE, RRSP_DEDUCTION_LIMIT}),
            frozenset({RRSP_DEDUCTION_MAXIMUM}),
        ),
        (
            AtMost,
            frozenset({RRSP_AMOUNT_DEDUCTED, RRSP_DEDUCTION_MAXIMUM}),
            frozenset({RRSP_DEDUCTION}),
        ),
        (
            Subtract,
            frozenset({RRSP_CONTRIBUTIONS_AVAILABLE, RRSP_DEDUCTION}),
            frozenset({UNUSED_RRSP_CONTRIBUTIONS_CARRIED_FORWARD}),
        ),
        (
            PerUnitAmount,
            frozenset({CHILDREN_UNDER_SEVEN}),
            frozenset({CHILD_CARE_LIMIT_FOR_CHILDREN_UNDER_SEVEN}),
        ),
        (
            PerUnitAmount,
            frozenset({CHILDREN_WITH_DISABILITY}),
            frozenset({CHILD_CARE_LIMIT_FOR_CHILDREN_WITH_DISABILITY}),
        ),
        (
            PerUnitAmount,
            frozenset({CHILDREN_SEVEN_TO_SIXTEEN}),
            frozenset({CHILD_CARE_LIMIT_FOR_CHILDREN_SEVEN_TO_SIXTEEN}),
        ),
        (
            Sum,
            frozenset(
                {
                    CHILD_CARE_LIMIT_FOR_CHILDREN_UNDER_SEVEN,
                    CHILD_CARE_LIMIT_FOR_CHILDREN_WITH_DISABILITY,
                    CHILD_CARE_LIMIT_FOR_CHILDREN_SEVEN_TO_SIXTEEN,
                }
            ),
            frozenset({CHILD_CARE_BASIC_LIMIT}),
        ),
        (Sum, frozenset({EMPLOYMENT_INCOME}), frozenset({CHILD_CARE_EARNED_INCOME})),
        (
            ApplyFraction,
            frozenset({CHILD_CARE_EARNED_INCOME}),
            frozenset({CHILD_CARE_EARNED_INCOME_LIMIT}),
        ),
        (
            LesserOf,
            frozenset(
                {CHILD_CARE_BASIC_LIMIT, CHILD_CARE_EXPENSES_PAID, CHILD_CARE_EARNED_INCOME_LIMIT}
            ),
            frozenset({CHILD_CARE_EXPENSES}),
        ),
        (
            Sum,
            frozenset({TOTAL_CARRYING_CHARGES, TOTAL_INTEREST_EXPENSES, TOTAL_OTHER_EXPENSES}),
            frozenset({CARRYING_CHARGES_INTEREST_EXPENSES_AND_OTHER_EXPENSES}),
        ),
        (
            Sum,
            frozenset(
                {
                    CAPITAL_GAINS_DEDUCTIONS_1985_TO_1987,
                    CAPITAL_GAINS_DEDUCTIONS_1988_AND_1989_OTHER_THAN_ELIGIBLE_CAPITAL_PROPERTY,
                    CAPITAL_GAINS_DEDUCTIONS_1988_AND_1989_ELIGIBLE_CAPITAL_PROPERTY,
                    CAPITAL_GAINS_DEDUCTIONS_1990_TO_1999,
                    CAPITAL_GAINS_DEDUCTIONS_2000,
                    CAPITAL_GAINS_DEDUCTIONS_2001_TO_2024,
                }
            ),
            frozenset({CAPITAL_GAINS_DEDUCTIONS_CLAIMED_1985_TO_2024}),
        ),
        (
            Sum,
            frozenset(
                {
                    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_1994,
                    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1994_TO_1996,
                    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1997_TO_1999,
                    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2000,
                    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2001_TO_2023,
                    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2024,
                }
            ),
            frozenset({OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_2024}),
        ),
        (
            Subtract,
            frozenset(
                {
                    CAPITAL_GAINS_DEDUCTIONS_CLAIMED_1985_TO_2024,
                    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_2024,
                }
            ),
            frozenset({BUSINESS_INVESTMENT_LOSS_REDUCTION_AVAILABLE}),
        ),
        (
            LesserOf,
            frozenset({BUSINESS_INVESTMENT_LOSS_REDUCTION_AVAILABLE, BUSINESS_INVESTMENT_LOSS}),
            frozenset({BUSINESS_INVESTMENT_LOSS_REDUCTION}),
        ),
        (
            Subtract,
            frozenset({BUSINESS_INVESTMENT_LOSS, BUSINESS_INVESTMENT_LOSS_REDUCTION}),
            frozenset({BUSINESS_INVESTMENT_LOSS_AFTER_REDUCTION}),
        ),
        (
            ApplyRate,
            frozenset({BUSINESS_INVESTMENT_LOSS_AFTER_REDUCTION}),
            frozenset({ALLOWABLE_BUSINESS_INVESTMENT_LOSS}),
        ),
        (
            Subtract,
            frozenset(
                {
                    FHSA_CONTRIBUTIONS_IN_2025,
                    FHSA_CONTRIBUTIONS_IN_2025_AFTER_FIRST_QUALIFYING_WITHDRAWAL,
                }
            ),
            frozenset({FHSA_CONTRIBUTIONS_IN_2025_BEFORE_FIRST_QUALIFYING_WITHDRAWAL}),
        ),
        (
            Sum,
            frozenset(
                {
                    FHSA_CONTRIBUTIONS_IN_2025_BEFORE_FIRST_QUALIFYING_WITHDRAWAL,
                    FHSA_VARIABLE_B_AMOUNT,
                }
            ),
            frozenset({FHSA_CONTRIBUTIONS_PLUS_VARIABLE_B_AMOUNT}),
        ),
        (
            Subtract,
            frozenset(
                {
                    FHSA_CONTRIBUTIONS_IN_2024,
                    FHSA_CONTRIBUTIONS_IN_2024_BEFORE_FIRST_QUALIFYING_WITHDRAWAL,
                }
            ),
            frozenset({FHSA_CONTRIBUTIONS_IN_2024_AFTER_FIRST_QUALIFYING_WITHDRAWAL}),
        ),
        (
            Sum,
            frozenset(
                {
                    FHSA_CONTRIBUTIONS_IN_2024_AFTER_FIRST_QUALIFYING_WITHDRAWAL,
                    FHSA_CONTRIBUTIONS_IN_2025_AFTER_FIRST_QUALIFYING_WITHDRAWAL,
                }
            ),
            frozenset({FHSA_CONTRIBUTIONS_AFTER_FIRST_QUALIFYING_WITHDRAWAL}),
        ),
        (
            SubtractNotBelowZero,
            frozenset(
                {
                    FHSA_DESIGNATED_WITHDRAWALS_IN_2025,
                    FHSA_CONTRIBUTIONS_AFTER_FIRST_QUALIFYING_WITHDRAWAL,
                }
            ),
            frozenset({FHSA_EXCESS_DESIGNATED_WITHDRAWALS}),
        ),
        (
            SubtractNotBelowZero,
            frozenset(
                {FHSA_CONTRIBUTIONS_PLUS_VARIABLE_B_AMOUNT, FHSA_EXCESS_DESIGNATED_WITHDRAWALS}
            ),
            frozenset({FHSA_CONTRIBUTIONS_LIMIT}),
        ),
        (CreditAmount, frozenset(), frozenset({FHSA_ANNUAL_AMOUNT})),
        (
            Sum,
            frozenset({FHSA_ANNUAL_AMOUNT, FHSA_CARRYFORWARD_FOR_2025}),
            frozenset({FHSA_ANNUAL_AMOUNT_WITH_CARRYFORWARD}),
        ),
        (
            Sum,
            frozenset({FHSA_RRSP_TRANSFERS_IN_2024_AND_PRIOR_YEARS, FHSA_RRSP_TRANSFERS_IN_2025}),
            frozenset({FHSA_TOTAL_RRSP_TRANSFERS}),
        ),
        (
            Sum,
            frozenset(
                {
                    FHSA_DESIGNATED_TRANSFERS_IN_2024_AND_PRIOR_YEARS,
                    FHSA_DESIGNATED_TRANSFERS_IN_2025,
                }
            ),
            frozenset({FHSA_TOTAL_DESIGNATED_TRANSFERS}),
        ),
        (
            Subtract,
            frozenset({FHSA_TOTAL_RRSP_TRANSFERS, FHSA_TOTAL_DESIGNATED_TRANSFERS}),
            frozenset({FHSA_NET_RRSP_TRANSFER_AMOUNT}),
        ),
        (
            Subtract,
            frozenset(
                {
                    FHSA_RRSP_TRANSFERS_IN_2024_AND_PRIOR_YEARS,
                    FHSA_DESIGNATED_TRANSFERS_IN_2024_AND_PRIOR_YEARS,
                }
            ),
            frozenset({FHSA_NET_RRSP_TRANSFER_AMOUNT_FOR_2024_AND_PRIOR_YEARS}),
        ),
        (
            SubtractNotBelowZero,
            frozenset(
                {FHSA_NET_RRSP_TRANSFER_AMOUNT_FOR_2024_AND_PRIOR_YEARS, FHSA_VARIABLE_H_AMOUNT}
            ),
            frozenset({FHSA_NET_TRANSFER_AMOUNT_LESS_VARIABLE_H_AMOUNT}),
        ),
        (CreditAmount, frozenset(), frozenset({FHSA_ANNUAL_AMOUNT_FOR_2024})),
        (
            Sum,
            frozenset({FHSA_ANNUAL_AMOUNT_FOR_2024, FHSA_CARRYFORWARD_FOR_2024}),
            frozenset({FHSA_ANNUAL_AMOUNT_FOR_2024_WITH_CARRYFORWARD}),
        ),
        (
            LesserOf,
            frozenset(
                {
                    FHSA_NET_TRANSFER_AMOUNT_LESS_VARIABLE_H_AMOUNT,
                    FHSA_ANNUAL_AMOUNT_FOR_2024_WITH_CARRYFORWARD,
                }
            ),
            frozenset({FHSA_TRANSFER_AMOUNT_AT_MOST_LIMIT}),
        ),
        (
            Sum,
            frozenset({FHSA_TRANSFER_AMOUNT_AT_MOST_LIMIT, FHSA_VARIABLE_F_AMOUNT}),
            frozenset({FHSA_TRANSFER_AMOUNT_PLUS_VARIABLE_F_AMOUNT}),
        ),
        (
            Subtract,
            frozenset({FHSA_NET_RRSP_TRANSFER_AMOUNT, FHSA_TRANSFER_AMOUNT_PLUS_VARIABLE_F_AMOUNT}),
            frozenset({FHSA_NET_TRANSFER_AMOUNT_AFTER_PRIOR_YEARS}),
        ),
        (
            SubtractNotBelowZero,
            frozenset(
                {FHSA_ANNUAL_AMOUNT_WITH_CARRYFORWARD, FHSA_NET_TRANSFER_AMOUNT_AFTER_PRIOR_YEARS}
            ),
            frozenset({FHSA_ANNUAL_AMOUNT_AFTER_TRANSFERS}),
        ),
        (
            LesserOf,
            frozenset({FHSA_CONTRIBUTIONS_LIMIT, FHSA_ANNUAL_AMOUNT_AFTER_TRANSFERS}),
            frozenset({FHSA_ANNUAL_LIMIT_FROM_STEP_2}),
        ),
        (
            CreditAmount,
            frozenset(),
            frozenset({FHSA_ANNUAL_LIMIT_AFTER_MAXIMUM_PARTICIPATION_PERIOD}),
        ),
        (
            ChooseByCount,
            frozenset(
                {
                    FHSA_MAXIMUM_PARTICIPATION_PERIOD_ENDED,
                    FHSA_ANNUAL_LIMIT_FROM_STEP_2,
                    FHSA_ANNUAL_LIMIT_AFTER_MAXIMUM_PARTICIPATION_PERIOD,
                }
            ),
            frozenset({FHSA_ANNUAL_LIMIT}),
        ),
        (
            Sum,
            frozenset({FHSA_ANNUAL_LIMIT, FHSA_ANNUAL_LIMITS_FOR_2024_AND_PRIOR_YEARS}),
            frozenset({FHSA_TOTAL_ANNUAL_LIMITS}),
        ),
        (
            Subtract,
            frozenset({FHSA_TOTAL_ANNUAL_LIMITS, FHSA_DEDUCTIONS_FOR_2024_AND_PRIOR_YEARS}),
            frozenset({FHSA_ANNUAL_LIMITS_LESS_DEDUCTIONS}),
        ),
        (CreditAmount, frozenset(), frozenset({FHSA_LIFETIME_LIMIT})),
        (
            Subtract,
            frozenset({FHSA_LIFETIME_LIMIT, FHSA_DEDUCTIONS_FOR_2024_AND_PRIOR_YEARS}),
            frozenset({FHSA_LIFETIME_LIMIT_LESS_DEDUCTIONS}),
        ),
        (
            SubtractNotBelowZero,
            frozenset({FHSA_LIFETIME_LIMIT_LESS_DEDUCTIONS, FHSA_NET_RRSP_TRANSFER_AMOUNT}),
            frozenset({FHSA_LIFETIME_LIMIT_LESS_DEDUCTIONS_AND_TRANSFERS}),
        ),
        (
            LesserOf,
            frozenset(
                {
                    FHSA_ANNUAL_LIMITS_LESS_DEDUCTIONS,
                    FHSA_LIFETIME_LIMIT_LESS_DEDUCTIONS_AND_TRANSFERS,
                }
            ),
            frozenset({FHSA_MAXIMUM_DEDUCTION}),
        ),
        (
            Sum,
            frozenset(
                {
                    FHSA_UNUSED_CONTRIBUTIONS_BROUGHT_FORWARD,
                    FHSA_CONTRIBUTIONS_IN_2025_BEFORE_FIRST_QUALIFYING_WITHDRAWAL,
                }
            ),
            frozenset({FHSA_UNUSED_CONTRIBUTIONS_PLUS_CONTRIBUTIONS}),
        ),
        (
            Subtract,
            frozenset(
                {FHSA_UNUSED_CONTRIBUTIONS_PLUS_CONTRIBUTIONS, FHSA_EXCESS_DESIGNATED_WITHDRAWALS}
            ),
            frozenset({FHSA_CONTRIBUTIONS_AVAILABLE}),
        ),
        (
            AtMost,
            frozenset({FHSA_CONTRIBUTIONS_DEDUCTED, FHSA_MAXIMUM_DEDUCTION}),
            frozenset({FHSA_DEDUCTION}),
        ),
        (
            Subtract,
            frozenset({FHSA_CONTRIBUTIONS_AVAILABLE, FHSA_DEDUCTION}),
            frozenset({FHSA_UNUSED_CONTRIBUTIONS_CARRIED_FORWARD}),
        ),
        (
            Sum,
            frozenset(
                {
                    RPP_DEDUCTION,
                    RRSP_DEDUCTION,
                    FHSA_DEDUCTION,
                    ELECTED_SPLIT_PENSION_DEDUCTION,
                    UNION_DUES,
                    UCCB_REPAYMENT,
                    CHILD_CARE_EXPENSES,
                    ALLOWABLE_BUSINESS_INVESTMENT_LOSS,
                    SUPPORT_PAYMENTS_DEDUCTION,
                    CARRYING_CHARGES_INTEREST_EXPENSES_AND_OTHER_EXPENSES,
                    CPP_ENHANCED_CONTRIBUTIONS,
                    EXPLORATION_AND_DEVELOPMENT_EXPENSES,
                    OTHER_DEDUCTIONS,
                }
            ),
            frozenset({DEDUCTIONS_FROM_TOTAL_INCOME}),
        ),
        (
            Subtract,
            frozenset({TOTAL_INCOME, DEDUCTIONS_FROM_TOTAL_INCOME}),
            frozenset({NET_INCOME_BEFORE_ADJUSTMENTS}),
        ),
        (
            SubtractNotBelowZero,
            frozenset({TOTAL_INCOME, DEDUCTIONS_FROM_TOTAL_INCOME}),
            frozenset({NET_INCOME}),
        ),
        (
            Sum,
            frozenset({UNIVERSAL_CHILD_CARE_BENEFIT, RDSP_INCOME}),
            frozenset({UCCB_AND_RDSP_INCOME}),
        ),
        (
            Subtract,
            frozenset({NET_INCOME, UCCB_AND_RDSP_INCOME}),
            frozenset({NET_INCOME_LESS_UCCB_AND_RDSP_INCOME}),
        ),
        (
            Sum,
            frozenset({UCCB_REPAYMENT, RDSP_INCOME_REPAYMENT}),
            frozenset({UCCB_AND_RDSP_INCOME_REPAYMENTS}),
        ),
        (
            Sum,
            frozenset({NET_INCOME_LESS_UCCB_AND_RDSP_INCOME, UCCB_AND_RDSP_INCOME_REPAYMENTS}),
            frozenset({OTHER_PAYMENTS_LIMIT_INCOME}),
        ),
        (
            ChooseByCount,
            frozenset(
                {
                    OTHER_PAYMENTS_WORKSHEET_LINE_9_OVER_LIMIT,
                    INCOME_SUPPORT_BENEFITS,
                    OTHER_PAYMENTS_DEDUCTION_ABOVE_LIMIT,
                }
            ),
            frozenset({OTHER_PAYMENTS_DEDUCTION_AFTER_LIMIT}),
        ),
        (
            ChooseByCount,
            frozenset(
                {
                    OTHER_PAYMENTS_WORKSHEET_REQUIRED,
                    INCOME_SUPPORT_BENEFITS,
                    OTHER_PAYMENTS_DEDUCTION_AFTER_LIMIT,
                }
            ),
            frozenset({OTHER_PAYMENTS_DEDUCTION}),
        ),
        (
            Sum,
            frozenset(
                {
                    CANADIAN_ARMED_FORCES_AND_POLICE_DEDUCTION,
                    SECURITY_OPTIONS_DEDUCTIONS,
                    OTHER_PAYMENTS_DEDUCTION,
                    LIMITED_PARTNERSHIP_LOSSES_OF_OTHER_YEARS,
                    NON_CAPITAL_LOSSES_OF_OTHER_YEARS,
                    ADDITIONAL_DEDUCTIONS,
                }
            ),
            frozenset({DEDUCTIONS_FROM_NET_INCOME}),
        ),
        (
            SubtractNotBelowZero,
            frozenset({NET_INCOME, DEDUCTIONS_FROM_NET_INCOME}),
            frozenset({TAXABLE_INCOME}),
        ),
        (ProgressiveTax, frozenset({TAXABLE_INCOME}), frozenset({FEDERAL_BASIC_TAX})),
        (ProgressiveTax, frozenset({TAXABLE_INCOME}), frozenset({ONTARIO_BASIC_TAX})),
        (TaperedAmount, frozenset({NET_INCOME}), frozenset({BASIC_PERSONAL_AMOUNT})),
        (CreditAmount, frozenset(), frozenset({ontario.BASIC_PERSONAL_AMOUNT})),
        (CappedAmount, frozenset({EMPLOYMENT_INCOME}), frozenset({CANADA_EMPLOYMENT_AMOUNT})),
        (CreditAmount, frozenset(), frozenset({AGE_MAXIMUM})),
        (CreditAmount, frozenset(), frozenset({AGE_INCOME_THRESHOLD})),
        (
            SubtractNotBelowZero,
            frozenset({NET_INCOME, AGE_INCOME_THRESHOLD}),
            frozenset({AGE_INCOME_OVER_THRESHOLD}),
        ),
        (ApplyRate, frozenset({AGE_INCOME_OVER_THRESHOLD}), frozenset({AGE_REDUCTION})),
        (
            SubtractNotBelowZero,
            frozenset({AGE_MAXIMUM, AGE_REDUCTION}),
            frozenset({AGE_AMOUNT_BEFORE_COUNT}),
        ),
        (
            TimesCount,
            frozenset({AGE_AMOUNT_BEFORE_COUNT, BORN_IN_1960_OR_EARLIER}),
            frozenset({AGE_AMOUNT}),
        ),
        (
            PerUnitAmount,
            frozenset({SPOUSE_CAREGIVER_ELIGIBLE}),
            frozenset({SPOUSE_INFIRMITY_SUPPLEMENT}),
        ),
        (
            Sum,
            frozenset({BASIC_PERSONAL_AMOUNT, SPOUSE_INFIRMITY_SUPPLEMENT}),
            frozenset({SPOUSE_AMOUNT_BASIS}),
        ),
        (
            SubtractNotBelowZero,
            frozenset({SPOUSE_AMOUNT_BASIS, SPOUSE_NET_INCOME}),
            frozenset({SPOUSE_AMOUNT_BEFORE_COUNT}),
        ),
        (
            TimesCount,
            frozenset({SPOUSE_AMOUNT_BEFORE_COUNT, SPOUSES_CLAIMED}),
            frozenset({SPOUSE_AMOUNT}),
        ),
        (
            SubtractNotBelowZero,
            frozenset({BASIC_PERSONAL_AMOUNT, DEPENDANT_NET_INCOME}),
            frozenset({ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT}),
        ),
        (
            TimesCount,
            frozenset({ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT, ELIGIBLE_DEPENDANTS}),
            frozenset({ELIGIBLE_DEPENDANT_AMOUNT}),
        ),
        (CreditAmount, frozenset(), frozenset({SPOUSE_CAREGIVER_BASE})),
        (
            SubtractNotBelowZero,
            frozenset({SPOUSE_CAREGIVER_BASE, SPOUSE_NET_INCOME}),
            frozenset({SPOUSE_CAREGIVER_BEFORE_MAXIMUM}),
        ),
        (
            CappedAmount,
            frozenset({SPOUSE_CAREGIVER_BEFORE_MAXIMUM}),
            frozenset({SPOUSE_CAREGIVER_LIMIT}),
        ),
        (
            SubtractNotBelowZero,
            frozenset({SPOUSE_CAREGIVER_LIMIT, SPOUSE_AMOUNT}),
            frozenset({SPOUSE_CAREGIVER_AMOUNT_BEFORE_COUNT}),
        ),
        (
            TimesCount,
            frozenset({SPOUSE_CAREGIVER_AMOUNT_BEFORE_COUNT, SPOUSE_CAREGIVER_ELIGIBLE}),
            frozenset({SPOUSE_CAREGIVER_AMOUNT}),
        ),
        (CaregiverAmount, frozenset({INFIRM_DEPENDANTS}), frozenset({CAREGIVER_AMOUNT})),
        (ApplyRate, frozenset({NET_INCOME}), frozenset({MEDICAL_NET_INCOME_SHARE})),
        (CappedAmount, frozenset({MEDICAL_NET_INCOME_SHARE}), frozenset({MEDICAL_THRESHOLD})),
        (
            SubtractNotBelowZero,
            frozenset({MEDICAL_EXPENSES, MEDICAL_THRESHOLD}),
            frozenset({MEDICAL_EXPENSES_OVER_THRESHOLD}),
        ),
        (
            OtherDependantsMedical,
            frozenset({OTHER_DEPENDANTS}),
            frozenset({OTHER_DEPENDANTS_MEDICAL}),
        ),
        (
            Sum,
            frozenset({MEDICAL_EXPENSES_OVER_THRESHOLD, OTHER_DEPENDANTS_MEDICAL}),
            frozenset({MEDICAL_CLAIM}),
        ),
        (ApplyRate, frozenset({NET_INCOME}), frozenset({ontario.MEDICAL_NET_INCOME_SHARE})),
        (
            CappedAmount,
            frozenset({ontario.MEDICAL_NET_INCOME_SHARE}),
            frozenset({ontario.MEDICAL_THRESHOLD}),
        ),
        (
            SubtractNotBelowZero,
            frozenset({MEDICAL_EXPENSES, ontario.MEDICAL_THRESHOLD}),
            frozenset({ontario.MEDICAL_EXPENSES_OVER_THRESHOLD}),
        ),
        (
            OtherDependantsMedical,
            frozenset({OTHER_DEPENDANTS}),
            frozenset({ontario.OTHER_DEPENDANTS_MEDICAL}),
        ),
        (
            Sum,
            frozenset({ontario.MEDICAL_EXPENSES_OVER_THRESHOLD, ontario.OTHER_DEPENDANTS_MEDICAL}),
            frozenset({ontario.MEDICAL_CLAIM}),
        ),
        (
            DisabilityTransferAmount,
            frozenset({DISABILITY_DEPENDANTS}),
            frozenset({DISABILITY_TRANSFERRED_AMOUNT}),
        ),
        (PerUnitAmount, frozenset({INFIRM_CHILDREN}), frozenset({INFIRM_CHILDREN_AMOUNT})),
        (CreditAmount, frozenset(), frozenset({ontario.AGE_MAXIMUM})),
        (CreditAmount, frozenset(), frozenset({ontario.AGE_INCOME_THRESHOLD})),
        (
            SubtractNotBelowZero,
            frozenset({NET_INCOME, ontario.AGE_INCOME_THRESHOLD}),
            frozenset({ontario.AGE_INCOME_OVER_THRESHOLD}),
        ),
        (
            ApplyRate,
            frozenset({ontario.AGE_INCOME_OVER_THRESHOLD}),
            frozenset({ontario.AGE_REDUCTION}),
        ),
        (
            SubtractNotBelowZero,
            frozenset({ontario.AGE_MAXIMUM, ontario.AGE_REDUCTION}),
            frozenset({ontario.AGE_AMOUNT_BEFORE_COUNT}),
        ),
        (
            TimesCount,
            frozenset({ontario.AGE_AMOUNT_BEFORE_COUNT, BORN_IN_1960_OR_EARLIER}),
            frozenset({ontario.AGE_AMOUNT}),
        ),
        (CreditAmount, frozenset(), frozenset({ontario.SPOUSE_BASE})),
        (
            SubtractNotBelowZero,
            frozenset({ontario.SPOUSE_BASE, SPOUSE_NET_INCOME}),
            frozenset({ontario.SPOUSE_AMOUNT_BEFORE_MAXIMUM}),
        ),
        (
            CappedAmount,
            frozenset({ontario.SPOUSE_AMOUNT_BEFORE_MAXIMUM}),
            frozenset({ontario.SPOUSE_AMOUNT_BEFORE_COUNT}),
        ),
        (
            TimesCount,
            frozenset({ontario.SPOUSE_AMOUNT_BEFORE_COUNT, SPOUSES_CLAIMED}),
            frozenset({ontario.SPOUSE_AMOUNT}),
        ),
        (CreditAmount, frozenset(), frozenset({ELIGIBLE_DEPENDANT_BASE})),
        (
            SubtractNotBelowZero,
            frozenset({ELIGIBLE_DEPENDANT_BASE, DEPENDANT_NET_INCOME}),
            frozenset({ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_MAXIMUM}),
        ),
        (
            CappedAmount,
            frozenset({ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_MAXIMUM}),
            frozenset({ontario.ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT}),
        ),
        (
            TimesCount,
            frozenset({ontario.ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT, ELIGIBLE_DEPENDANTS}),
            frozenset({ontario.ELIGIBLE_DEPENDANT_AMOUNT}),
        ),
        (
            OntarioCaregiverAmount,
            frozenset({CAREGIVER_DEPENDANTS, ontario.ELIGIBLE_DEPENDANT_AMOUNT}),
            frozenset({ontario.CAREGIVER_AMOUNT}),
        ),
        (
            Sum,
            frozenset(
                {
                    BASIC_PERSONAL_AMOUNT,
                    AGE_AMOUNT,
                    SPOUSE_AMOUNT,
                    ELIGIBLE_DEPENDANT_AMOUNT,
                    SPOUSE_CAREGIVER_AMOUNT,
                    CAREGIVER_AMOUNT,
                    INFIRM_CHILDREN_AMOUNT,
                    CPP_BASE_CONTRIBUTIONS,
                    EI_PREMIUMS,
                    CANADA_EMPLOYMENT_AMOUNT,
                    MEDICAL_CLAIM,
                    DISABILITY_TRANSFERRED_AMOUNT,
                }
            ),
            frozenset({NON_REFUNDABLE_CREDIT_AMOUNTS}),
        ),
        (
            Sum,
            frozenset(
                {
                    ontario.BASIC_PERSONAL_AMOUNT,
                    ontario.AGE_AMOUNT,
                    ontario.SPOUSE_AMOUNT,
                    ontario.ELIGIBLE_DEPENDANT_AMOUNT,
                    ontario.CAREGIVER_AMOUNT,
                    CPP_BASE_CONTRIBUTIONS,
                    EI_PREMIUMS,
                    ontario.MEDICAL_CLAIM,
                }
            ),
            frozenset({ontario.NON_REFUNDABLE_CREDIT_AMOUNTS}),
        ),
        (
            ApplyRate,
            frozenset({NON_REFUNDABLE_CREDIT_AMOUNTS}),
            frozenset({CREDIT_AMOUNTS_AT_CREDIT_RATE}),
        ),
        (
            LesserOf,
            frozenset({DEPRECIABLE_GIFT_NET_PROCEEDS, DEPRECIABLE_GIFT_CAPITAL_COST}),
            frozenset({DEPRECIABLE_GIFT_PROCEEDS_OR_COST}),
        ),
        (
            LesserOf,
            frozenset(
                {DEPRECIABLE_GIFT_RECAPTURED_DEPRECIATION, DEPRECIABLE_GIFT_PROCEEDS_OR_COST}
            ),
            frozenset({DEPRECIABLE_GIFTS}),
        ),
        (
            Subtract,
            frozenset({CAPITAL_GIFT_TAXABLE_GAINS, CAPITAL_GIFT_GAINS_DEDUCTION}),
            frozenset({CAPITAL_PROPERTY_GIFTS}),
        ),
        (
            Sum,
            frozenset(
                {
                    CHARITABLE_DONATIONS,
                    GOVERNMENT_DONATIONS,
                    UNIVERSITY_DONATIONS_OUTSIDE_CANADA,
                    FOREIGN_CHARITY_DONATIONS,
                }
            ),
            frozenset({TOTAL_CHARITABLE_DONATIONS}),
        ),
        (ApplyRate, frozenset({NET_INCOME}), frozenset({DONATION_LIMIT_ON_NET_INCOME})),
        (
            Sum,
            frozenset({DEPRECIABLE_GIFTS, CAPITAL_PROPERTY_GIFTS}),
            frozenset({CAPITAL_GIFTS_TOTAL}),
        ),
        (ApplyRate, frozenset({CAPITAL_GIFTS_TOTAL}), frozenset({CAPITAL_GIFTS_LIMIT_ADDITION})),
        (
            Sum,
            frozenset({DONATION_LIMIT_ON_NET_INCOME, CAPITAL_GIFTS_LIMIT_ADDITION}),
            frozenset({DONATION_LIMIT_WITH_CAPITAL_GIFTS}),
        ),
        (
            LesserOf,
            frozenset({NET_INCOME, DONATION_LIMIT_WITH_CAPITAL_GIFTS}),
            frozenset({CHARITABLE_DONATIONS_LIMIT}),
        ),
        (
            LesserOf,
            frozenset({TOTAL_CHARITABLE_DONATIONS, CHARITABLE_DONATIONS_LIMIT}),
            frozenset({CHARITABLE_DONATIONS_CLAIMED}),
        ),
        (
            Sum,
            frozenset({CHARITABLE_DONATIONS_CLAIMED, ECOLOGICAL_AND_CULTURAL_GIFTS}),
            frozenset({DONATIONS_AND_GIFTS_TOTAL}),
        ),
        (CreditAmount, frozenset(), frozenset({DONATION_FIRST_TIER_MAXIMUM})),
        (
            LesserOf,
            frozenset({DONATIONS_AND_GIFTS_TOTAL, DONATION_FIRST_TIER_MAXIMUM}),
            frozenset({DONATIONS_FIRST_TIER}),
        ),
        (
            Subtract,
            frozenset({DONATIONS_AND_GIFTS_TOTAL, DONATIONS_FIRST_TIER}),
            frozenset({DONATIONS_OVER_FIRST_TIER}),
        ),
        (
            SubtractNotBelowZero,
            frozenset({DONATIONS_OVER_FIRST_TIER, ECOLOGICAL_GIFTS_BEFORE_2016}),
            frozenset({DONATIONS_OVER_FIRST_TIER_AFTER_2016_GIFTS}),
        ),
        (CreditAmount, frozenset(), frozenset({DONATION_HIGH_INCOME_THRESHOLD})),
        (
            SubtractNotBelowZero,
            frozenset({TAXABLE_INCOME, DONATION_HIGH_INCOME_THRESHOLD}),
            frozenset({TAXABLE_INCOME_OVER_DONATION_THRESHOLD}),
        ),
        (
            LesserOf,
            frozenset(
                {DONATIONS_OVER_FIRST_TIER_AFTER_2016_GIFTS, TAXABLE_INCOME_OVER_DONATION_THRESHOLD}
            ),
            frozenset({HIGH_INCOME_DONATIONS}),
        ),
        (ApplyRate, frozenset({HIGH_INCOME_DONATIONS}), frozenset({HIGH_INCOME_DONATION_CREDIT})),
        (
            Subtract,
            frozenset({DONATIONS_OVER_FIRST_TIER, HIGH_INCOME_DONATIONS}),
            frozenset({REGULAR_RATE_DONATIONS}),
        ),
        (ApplyRate, frozenset({REGULAR_RATE_DONATIONS}), frozenset({REGULAR_RATE_DONATION_CREDIT})),
        (ApplyRate, frozenset({DONATIONS_FIRST_TIER}), frozenset({FIRST_TIER_DONATION_CREDIT})),
        (
            Sum,
            frozenset(
                {
                    HIGH_INCOME_DONATION_CREDIT,
                    REGULAR_RATE_DONATION_CREDIT,
                    FIRST_TIER_DONATION_CREDIT,
                }
            ),
            frozenset({DONATIONS_AND_GIFTS_CREDIT}),
        ),
        (
            Sum,
            frozenset({CREDIT_AMOUNTS_AT_CREDIT_RATE, FIRST_TIER_DONATION_CREDIT}),
            frozenset({TOP_UP_CREDITS_BASE}),
        ),
        (CreditAmount, frozenset(), frozenset({TOP_UP_THRESHOLD})),
        (
            SubtractNotBelowZero,
            frozenset({TOP_UP_CREDITS_BASE, TOP_UP_THRESHOLD}),
            frozenset({TOP_UP_EXCESS}),
        ),
        (ApplyRate, frozenset({TOP_UP_EXCESS}), frozenset({TOP_UP_TAX_CREDIT})),
        (
            Sum,
            frozenset(
                {CREDIT_AMOUNTS_AT_CREDIT_RATE, DONATIONS_AND_GIFTS_CREDIT, TOP_UP_TAX_CREDIT}
            ),
            frozenset({NON_REFUNDABLE_TAX_CREDITS}),
        ),
        (
            ApplyRate,
            frozenset({ontario.NON_REFUNDABLE_CREDIT_AMOUNTS}),
            frozenset({ontario.CREDIT_AMOUNTS_AT_CREDIT_RATE}),
        ),
        (
            ApplyRate,
            frozenset({DONATIONS_FIRST_TIER}),
            frozenset({ontario.DONATIONS_FIRST_TIER_CREDIT}),
        ),
        (
            ApplyRate,
            frozenset({DONATIONS_OVER_FIRST_TIER}),
            frozenset({ontario.DONATIONS_OVER_FIRST_TIER_CREDIT}),
        ),
        (
            Sum,
            frozenset(
                {ontario.DONATIONS_FIRST_TIER_CREDIT, ontario.DONATIONS_OVER_FIRST_TIER_CREDIT}
            ),
            frozenset({ontario.DONATIONS_AND_GIFTS_CREDIT}),
        ),
        (
            Sum,
            frozenset({ontario.CREDIT_AMOUNTS_AT_CREDIT_RATE, ontario.DONATIONS_AND_GIFTS_CREDIT}),
            frozenset({ontario.NON_REFUNDABLE_TAX_CREDITS}),
        ),
        (
            Sum,
            frozenset(
                {
                    T3_DIVIDEND_TAX_CREDIT,
                    T4PS_DIVIDEND_TAX_CREDIT,
                    T5_DIVIDEND_TAX_CREDIT,
                    T5013_DIVIDEND_TAX_CREDIT,
                }
            ),
            frozenset({SLIP_DIVIDEND_TAX_CREDIT}),
        ),
        (
            Sum,
            frozenset({DIVIDENDS_WITHOUT_A_SLIP_GROSSED_UP}),
            frozenset({DIVIDENDS_AMOUNT_A}),
        ),
        (Sum, frozenset({OTHER_DIVIDENDS_GROSSED_UP}), frozenset({DIVIDENDS_AMOUNT_B})),
        (ApplyRate, frozenset({DIVIDENDS_AMOUNT_B}), frozenset({OTHER_DIVIDENDS_CREDIT})),
        (
            Subtract,
            frozenset({DIVIDENDS_AMOUNT_A, DIVIDENDS_AMOUNT_B}),
            frozenset({DIVIDENDS_AMOUNT_A_LESS_B}),
        ),
        (
            ApplyRate,
            frozenset({DIVIDENDS_AMOUNT_A_LESS_B}),
            frozenset({ELIGIBLE_DIVIDENDS_CREDIT}),
        ),
        (
            Sum,
            frozenset({OTHER_DIVIDENDS_CREDIT, ELIGIBLE_DIVIDENDS_CREDIT}),
            frozenset({NO_SLIP_DIVIDEND_TAX_CREDIT}),
        ),
        (
            Sum,
            frozenset({SLIP_DIVIDEND_TAX_CREDIT, NO_SLIP_DIVIDEND_TAX_CREDIT}),
            frozenset({DIVIDEND_TAX_CREDIT}),
        ),
        (
            Sum,
            frozenset({NON_REFUNDABLE_TAX_CREDITS, DIVIDEND_TAX_CREDIT}),
            frozenset({CREDITS_AGAINST_BASIC_FEDERAL_TAX}),
        ),
        (
            SubtractNotBelowZero,
            frozenset({FEDERAL_BASIC_TAX, CREDITS_AGAINST_BASIC_FEDERAL_TAX}),
            frozenset({FEDERAL_TAX_AFTER_CREDITS}),
        ),
        (
            SubtractNotBelowZero,
            frozenset({ONTARIO_BASIC_TAX, ontario.NON_REFUNDABLE_TAX_CREDITS}),
            frozenset({ONTARIO_TAX_AFTER_CREDITS}),
        ),
        (TieredSurcharge, frozenset({ONTARIO_TAX_AFTER_CREDITS}), frozenset({ONTARIO_SURTAX})),
        (
            Sum,
            frozenset({ONTARIO_TAX_AFTER_CREDITS, ONTARIO_SURTAX}),
            frozenset({ONTARIO_TAX_WITH_SURTAX}),
        ),
        (
            Sum,
            frozenset({ONTARIO_TAX_AFTER_CREDITS}),
            frozenset({ONTARIO_TAX_BEFORE_DIVIDEND_CREDIT}),
        ),
        (Sum, frozenset({TAXABLE_DIVIDENDS}), frozenset({ontario.DIVIDENDS_AMOUNT_A})),
        (
            Sum,
            frozenset({TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE}),
            frozenset({ontario.DIVIDENDS_AMOUNT_B}),
        ),
        (
            ApplyRate,
            frozenset({ontario.DIVIDENDS_AMOUNT_B}),
            frozenset({ontario.OTHER_DIVIDENDS_CREDIT}),
        ),
        (
            Subtract,
            frozenset({ontario.DIVIDENDS_AMOUNT_A, ontario.DIVIDENDS_AMOUNT_B}),
            frozenset({ontario.DIVIDENDS_AMOUNT_A_LESS_B}),
        ),
        (
            ApplyRate,
            frozenset({ontario.DIVIDENDS_AMOUNT_A_LESS_B}),
            frozenset({ontario.ELIGIBLE_DIVIDENDS_CREDIT}),
        ),
        (
            Sum,
            frozenset({ontario.OTHER_DIVIDENDS_CREDIT, ontario.ELIGIBLE_DIVIDENDS_CREDIT}),
            frozenset({ontario.DIVIDEND_TAX_CREDIT}),
        ),
        (
            SubtractNotBelowZero,
            frozenset({ONTARIO_TAX_BEFORE_DIVIDEND_CREDIT, ontario.DIVIDEND_TAX_CREDIT}),
            frozenset({ONTARIO_TAX_LESS_DIVIDEND_CREDIT}),
        ),
        (
            Sum,
            frozenset({ontario.DIVIDEND_TAX_CREDIT}),
            frozenset({ontario.DIVIDEND_CREDIT_FROM_LINE_57}),
        ),
        (
            SubtractNotBelowZero,
            frozenset({ONTARIO_TAX_WITH_SURTAX, ontario.DIVIDEND_CREDIT_FROM_LINE_57}),
            frozenset({ONTARIO_TAX_AFTER_DIVIDEND_CREDIT}),
        ),
        (CreditAmount, frozenset(), frozenset({TAX_REDUCTION_BASIC})),
        (PerUnitAmount, frozenset({DEPENDENT_CHILDREN}), frozenset({TAX_REDUCTION_FOR_CHILDREN})),
        (PerUnitAmount, frozenset({DEPENDANTS}), frozenset({TAX_REDUCTION_FOR_DEPENDANTS})),
        (
            Sum,
            frozenset(
                {TAX_REDUCTION_BASIC, TAX_REDUCTION_FOR_CHILDREN, TAX_REDUCTION_FOR_DEPENDANTS}
            ),
            frozenset({TAX_REDUCTION_AMOUNTS}),
        ),
        (
            MultipleOver,
            frozenset({TAX_REDUCTION_AMOUNTS, ONTARIO_TAX_AFTER_DIVIDEND_CREDIT}),
            frozenset({ONTARIO_TAX_REDUCTION}),
        ),
        (
            SubtractNotBelowZero,
            frozenset({ONTARIO_TAX_AFTER_DIVIDEND_CREDIT, ONTARIO_TAX_REDUCTION}),
            frozenset({ONTARIO_TAX_AFTER_REDUCTION}),
        ),
        (ApplyRate, frozenset({EMPLOYMENT_INCOME}), frozenset({LIFT_CREDIT_BEFORE_MAXIMUM})),
        (CappedAmount, frozenset({LIFT_CREDIT_BEFORE_MAXIMUM}), frozenset({LIFT_MAXIMUM_CREDIT})),
        (TieredSurcharge, frozenset({NET_INCOME}), frozenset({LIFT_REDUCTION})),
        (
            SubtractNotBelowZero,
            frozenset({LIFT_MAXIMUM_CREDIT, LIFT_REDUCTION}),
            frozenset({LIFT_CREDIT}),
        ),
        (
            SubtractNotBelowZero,
            frozenset({ONTARIO_TAX_AFTER_REDUCTION, LIFT_CREDIT}),
            frozenset({ONTARIO_TAX_AFTER_LIFT_CREDIT}),
        ),
        (
            ApplyRate,
            frozenset({COMMUNITY_FOOD_PROGRAM_DONATIONS}),
            frozenset({COMMUNITY_FOOD_PROGRAM_CREDIT}),
        ),
        (
            SubtractNotBelowZero,
            frozenset({ONTARIO_TAX_AFTER_LIFT_CREDIT, COMMUNITY_FOOD_PROGRAM_CREDIT}),
            frozenset({ONTARIO_TAX_AFTER_FOOD_CREDIT}),
        ),
        (TieredSurcharge, frozenset({TAXABLE_INCOME}), frozenset({ONTARIO_HEALTH_PREMIUM})),
        (
            Sum,
            frozenset({ONTARIO_TAX_AFTER_FOOD_CREDIT, ONTARIO_HEALTH_PREMIUM}),
            frozenset({ONTARIO_TAX}),
        ),
        (
            ApplyRate,
            frozenset({ITC_RECAPTURE_EXPENDITURE_AT_15_PERCENT}),
            frozenset({ITC_RECAPTURE_AT_15_PERCENT}),
        ),
        (
            ApplyRate,
            frozenset({ITC_RECAPTURE_EXPENDITURE_AT_20_PERCENT}),
            frozenset({ITC_RECAPTURE_AT_20_PERCENT}),
        ),
        (
            Sum,
            frozenset({ITC_RECAPTURE_AT_15_PERCENT, ITC_RECAPTURE_AT_20_PERCENT}),
            frozenset({ITC_RECAPTURE}),
        ),
        (
            Sum,
            frozenset({FEDERAL_TAX_AFTER_CREDITS, ITC_RECAPTURE}),
            frozenset({FEDERAL_TAX_WITH_ITC_RECAPTURE}),
        ),
        (CreditAmount, frozenset(), frozenset({POLITICAL_CREDIT_COLUMN_1_LINE_2})),
        (
            SubtractNotBelowZero,
            frozenset({POLITICAL_CONTRIBUTIONS, POLITICAL_CREDIT_COLUMN_1_LINE_2}),
            frozenset({POLITICAL_CREDIT_COLUMN_1_LINE_3}),
        ),
        (
            ApplyRate,
            frozenset({POLITICAL_CREDIT_COLUMN_1_LINE_3}),
            frozenset({POLITICAL_CREDIT_COLUMN_1_LINE_5}),
        ),
        (CreditAmount, frozenset(), frozenset({POLITICAL_CREDIT_COLUMN_1_LINE_6})),
        (
            Sum,
            frozenset({POLITICAL_CREDIT_COLUMN_1_LINE_5, POLITICAL_CREDIT_COLUMN_1_LINE_6}),
            frozenset({POLITICAL_CREDIT_COLUMN_1_LINE_7}),
        ),
        (CreditAmount, frozenset(), frozenset({POLITICAL_CREDIT_COLUMN_2_LINE_2})),
        (
            SubtractNotBelowZero,
            frozenset({POLITICAL_CONTRIBUTIONS, POLITICAL_CREDIT_COLUMN_2_LINE_2}),
            frozenset({POLITICAL_CREDIT_COLUMN_2_LINE_3}),
        ),
        (
            ApplyRate,
            frozenset({POLITICAL_CREDIT_COLUMN_2_LINE_3}),
            frozenset({POLITICAL_CREDIT_COLUMN_2_LINE_5}),
        ),
        (CreditAmount, frozenset(), frozenset({POLITICAL_CREDIT_COLUMN_2_LINE_6})),
        (
            Sum,
            frozenset({POLITICAL_CREDIT_COLUMN_2_LINE_5, POLITICAL_CREDIT_COLUMN_2_LINE_6}),
            frozenset({POLITICAL_CREDIT_COLUMN_2_LINE_7}),
        ),
        (CreditAmount, frozenset(), frozenset({POLITICAL_CREDIT_COLUMN_3_LINE_2})),
        (
            SubtractNotBelowZero,
            frozenset({POLITICAL_CONTRIBUTIONS, POLITICAL_CREDIT_COLUMN_3_LINE_2}),
            frozenset({POLITICAL_CREDIT_COLUMN_3_LINE_3}),
        ),
        (
            ApplyRate,
            frozenset({POLITICAL_CREDIT_COLUMN_3_LINE_3}),
            frozenset({POLITICAL_CREDIT_COLUMN_3_LINE_5}),
        ),
        (CreditAmount, frozenset(), frozenset({POLITICAL_CREDIT_COLUMN_3_LINE_6})),
        (
            Sum,
            frozenset({POLITICAL_CREDIT_COLUMN_3_LINE_5, POLITICAL_CREDIT_COLUMN_3_LINE_6}),
            frozenset({POLITICAL_CREDIT_COLUMN_3_LINE_7}),
        ),
        (
            ChooseByRange,
            frozenset(
                {
                    POLITICAL_CONTRIBUTIONS,
                    POLITICAL_CREDIT_COLUMN_2_LINE_2,
                    POLITICAL_CREDIT_COLUMN_3_LINE_2,
                    POLITICAL_CREDIT_COLUMN_1_LINE_7,
                    POLITICAL_CREDIT_COLUMN_2_LINE_7,
                    POLITICAL_CREDIT_COLUMN_3_LINE_7,
                }
            ),
            frozenset({POLITICAL_CREDIT_CHOSEN_COLUMN}),
        ),
        (CreditAmount, frozenset(), frozenset({POLITICAL_CREDIT_SHORTCUT_THRESHOLD})),
        (CreditAmount, frozenset(), frozenset({POLITICAL_CREDIT_SHORTCUT_AMOUNT})),
        (
            ChooseByRange,
            frozenset(
                {
                    POLITICAL_CREDIT_SHORTCUT_THRESHOLD,
                    POLITICAL_CONTRIBUTIONS,
                    POLITICAL_CREDIT_COLUMN_3_LINE_2,
                    POLITICAL_CREDIT_SHORTCUT_AMOUNT,
                    POLITICAL_CREDIT_COLUMN_3_LINE_7,
                    POLITICAL_CREDIT_CHOSEN_COLUMN,
                }
            ),
            frozenset({POLITICAL_CREDIT_BEFORE_MAXIMUM}),
        ),
        (CappedAmount, frozenset({POLITICAL_CREDIT_BEFORE_MAXIMUM}), frozenset({POLITICAL_CREDIT})),
        (
            ApplyRate,
            frozenset({LABOUR_SPONSORED_FUNDS_NET_COST}),
            frozenset({LABOUR_SPONSORED_FUNDS_CREDIT_BEFORE_MAXIMUM}),
        ),
        (
            CappedAmount,
            frozenset({LABOUR_SPONSORED_FUNDS_CREDIT_BEFORE_MAXIMUM}),
            frozenset({LABOUR_SPONSORED_FUNDS_CREDIT}),
        ),
        (
            Sum,
            frozenset({POLITICAL_CREDIT, LABOUR_SPONSORED_FUNDS_CREDIT}),
            frozenset({CREDITS_AGAINST_FEDERAL_TAX}),
        ),
        (
            SubtractNotBelowZero,
            frozenset({FEDERAL_TAX_WITH_ITC_RECAPTURE, CREDITS_AGAINST_FEDERAL_TAX}),
            frozenset({FEDERAL_TAX_LESS_CREDITS}),
        ),
        (
            LesserOf,
            frozenset({RESP_AIPS_RECEIVED_PART_A, RESP_AIPS_RRSP_CONTRIBUTIONS}),
            frozenset({RESP_AIPS_CONTRIBUTIONS_COUNTED}),
        ),
        (CreditAmount, frozenset({}), frozenset({RESP_AIPS_LIFETIME_LIMIT})),
        (
            Subtract,
            frozenset({RESP_AIPS_LIFETIME_LIMIT, RESP_AIPS_REDUCTION_USED_IN_PREVIOUS_YEARS}),
            frozenset({RESP_AIPS_LIMIT_REMAINING}),
        ),
        (
            LesserOf,
            frozenset({RESP_AIPS_CONTRIBUTIONS_COUNTED, RESP_AIPS_LIMIT_REMAINING}),
            frozenset({RESP_AIPS_REDUCTION}),
        ),
        (
            Subtract,
            frozenset({RESP_AIPS_RECEIVED_PART_A, RESP_AIPS_REDUCTION}),
            frozenset({RESP_AIPS_SUBJECT_TO_TAX}),
        ),
        (ApplyRate, frozenset({RESP_AIPS_SUBJECT_TO_TAX}), frozenset({RESP_AIPS_PART_A_TAX})),
        (ApplyRate, frozenset({RESP_AIPS_RECEIVED_PART_B}), frozenset({RESP_AIPS_PART_B_TAX})),
        (
            ChooseByCount,
            frozenset({RESP_AIPS_PART_A_APPLIES, RESP_AIPS_PART_B_TAX, RESP_AIPS_PART_A_TAX}),
            frozenset({RESP_AIPS_ADDITIONAL_TAX}),
        ),
        (
            Sum,
            frozenset({RESP_AIPS_ADDITIONAL_TAX, RL_10_LABOUR_SPONSORED_FUND_AMOUNT}),
            frozenset({SPECIAL_TAXES}),
        ),
        (
            Sum,
            frozenset({FEDERAL_TAX_LESS_CREDITS, ADVANCED_CANADA_WORKERS_BENEFIT, SPECIAL_TAXES}),
            frozenset({NET_FEDERAL_TAX}),
        ),
        (Sum, frozenset({NET_FEDERAL_TAX, ONTARIO_TAX}), frozenset({TOTAL_PAYABLE})),
        (Sum, frozenset({EMPLOYMENT_INCOME}), frozenset({WORKING_INCOME})),
        (Sum, frozenset({NET_INCOME}), frozenset({ADJUSTED_FAMILY_NET_INCOME})),
        (
            TieredSurcharge,
            frozenset({WORKING_INCOME}),
            frozenset({CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT}),
        ),
        (
            TieredSurcharge,
            frozenset({WORKING_INCOME}),
            frozenset({CWB_BEFORE_REDUCTION_WITH_DEPENDANT}),
        ),
        (
            TieredSurcharge,
            frozenset({ADJUSTED_FAMILY_NET_INCOME}),
            frozenset({CWB_REDUCTION_WITHOUT_DEPENDANT}),
        ),
        (
            TieredSurcharge,
            frozenset({ADJUSTED_FAMILY_NET_INCOME}),
            frozenset({CWB_REDUCTION_WITH_DEPENDANT}),
        ),
        (
            SubtractNotBelowZero,
            frozenset({CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT, CWB_REDUCTION_WITHOUT_DEPENDANT}),
            frozenset({CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT}),
        ),
        (
            SubtractNotBelowZero,
            frozenset({CWB_BEFORE_REDUCTION_WITH_DEPENDANT, CWB_REDUCTION_WITH_DEPENDANT}),
            frozenset({CANADA_WORKERS_BENEFIT_WITH_DEPENDANT}),
        ),
        (
            ChooseByCount,
            frozenset(
                {
                    CWB_ELIGIBLE_DEPENDANTS,
                    CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT,
                    CANADA_WORKERS_BENEFIT_WITH_DEPENDANT,
                }
            ),
            frozenset({CANADA_WORKERS_BENEFIT}),
        ),
        (ApplyRate, frozenset({FERTILITY_EXPENSES}), frozenset({FERTILITY_CREDIT_BEFORE_MAXIMUM})),
        (CappedAmount, frozenset({FERTILITY_CREDIT_BEFORE_MAXIMUM}), frozenset({FERTILITY_CREDIT})),
        (
            CappedAmount,
            frozenset({SENIORS_TRANSIT_PAID}),
            frozenset({SENIORS_TRANSIT_AMOUNT_PAID_AT_MOST_MAXIMUM}),
        ),
        (
            ApplyRate,
            frozenset({SENIORS_TRANSIT_AMOUNT_PAID_AT_MOST_MAXIMUM}),
            frozenset({SENIORS_TRANSIT_CREDIT}),
        ),
        (CreditAmount, frozenset(), frozenset({ontario.POLITICAL_CREDIT_COLUMN_1_LINE_2})),
        (
            SubtractNotBelowZero,
            frozenset({ontario.POLITICAL_CONTRIBUTIONS, ontario.POLITICAL_CREDIT_COLUMN_1_LINE_2}),
            frozenset({ontario.POLITICAL_CREDIT_COLUMN_1_LINE_3}),
        ),
        (
            ApplyRate,
            frozenset({ontario.POLITICAL_CREDIT_COLUMN_1_LINE_3}),
            frozenset({ontario.POLITICAL_CREDIT_COLUMN_1_LINE_5}),
        ),
        (CreditAmount, frozenset(), frozenset({ontario.POLITICAL_CREDIT_COLUMN_1_LINE_6})),
        (
            FlowThroughShareExpenses,
            frozenset({FLOW_THROUGH_SHARE_SLIPS}),
            frozenset({FLOW_THROUGH_SHARE_EXPENSES}),
        ),
        (
            ApplyRate,
            frozenset({FLOW_THROUGH_SHARE_EXPENSES}),
            frozenset({FLOW_THROUGH_SHARE_CREDIT}),
        ),
        (
            Sum,
            frozenset(
                {ontario.POLITICAL_CREDIT_COLUMN_1_LINE_5, ontario.POLITICAL_CREDIT_COLUMN_1_LINE_6}
            ),
            frozenset({ontario.POLITICAL_CREDIT_COLUMN_1_LINE_7}),
        ),
        (CreditAmount, frozenset(), frozenset({ontario.POLITICAL_CREDIT_COLUMN_2_LINE_2})),
        (
            SubtractNotBelowZero,
            frozenset({ontario.POLITICAL_CONTRIBUTIONS, ontario.POLITICAL_CREDIT_COLUMN_2_LINE_2}),
            frozenset({ontario.POLITICAL_CREDIT_COLUMN_2_LINE_3}),
        ),
        (
            ApplyRate,
            frozenset({ontario.POLITICAL_CREDIT_COLUMN_2_LINE_3}),
            frozenset({ontario.POLITICAL_CREDIT_COLUMN_2_LINE_5}),
        ),
        (CreditAmount, frozenset(), frozenset({ontario.POLITICAL_CREDIT_COLUMN_2_LINE_6})),
        (
            Sum,
            frozenset(
                {ontario.POLITICAL_CREDIT_COLUMN_2_LINE_5, ontario.POLITICAL_CREDIT_COLUMN_2_LINE_6}
            ),
            frozenset({ontario.POLITICAL_CREDIT_COLUMN_2_LINE_7}),
        ),
        (CreditAmount, frozenset(), frozenset({ontario.POLITICAL_CREDIT_COLUMN_3_LINE_2})),
        (
            SubtractNotBelowZero,
            frozenset({ontario.POLITICAL_CONTRIBUTIONS, ontario.POLITICAL_CREDIT_COLUMN_3_LINE_2}),
            frozenset({ontario.POLITICAL_CREDIT_COLUMN_3_LINE_3}),
        ),
        (
            ApplyRate,
            frozenset({ontario.POLITICAL_CREDIT_COLUMN_3_LINE_3}),
            frozenset({ontario.POLITICAL_CREDIT_COLUMN_3_LINE_5}),
        ),
        (CreditAmount, frozenset(), frozenset({ontario.POLITICAL_CREDIT_COLUMN_3_LINE_6})),
        (
            Sum,
            frozenset(
                {ontario.POLITICAL_CREDIT_COLUMN_3_LINE_5, ontario.POLITICAL_CREDIT_COLUMN_3_LINE_6}
            ),
            frozenset({ontario.POLITICAL_CREDIT_COLUMN_3_LINE_7}),
        ),
        (
            ChooseByRange,
            frozenset(
                {
                    ontario.POLITICAL_CONTRIBUTIONS,
                    ontario.POLITICAL_CREDIT_COLUMN_2_LINE_2,
                    ontario.POLITICAL_CREDIT_COLUMN_3_LINE_2,
                    ontario.POLITICAL_CREDIT_COLUMN_1_LINE_7,
                    ontario.POLITICAL_CREDIT_COLUMN_2_LINE_7,
                    ontario.POLITICAL_CREDIT_COLUMN_3_LINE_7,
                }
            ),
            frozenset({ontario.POLITICAL_CREDIT_BEFORE_MAXIMUM}),
        ),
        (
            CappedAmount,
            frozenset({ontario.POLITICAL_CREDIT_BEFORE_MAXIMUM}),
            frozenset({ontario.POLITICAL_CREDIT}),
        ),
        (
            Sum,
            frozenset(
                {
                    FERTILITY_CREDIT,
                    SENIORS_TRANSIT_CREDIT,
                    ontario.POLITICAL_CREDIT,
                    FLOW_THROUGH_SHARE_CREDIT,
                }
            ),
            frozenset({ONTARIO_CREDITS_SUBTOTAL}),
        ),
        (CreditAmount, frozenset(), frozenset({COOP_EDUCATION_PAYROLL_THRESHOLD})),
        (
            SubtractNotBelowZero,
            frozenset({COOP_EDUCATION_PAYROLL, COOP_EDUCATION_PAYROLL_THRESHOLD}),
            frozenset({COOP_EDUCATION_PAYROLL_OVER_THRESHOLD}),
        ),
        (CreditAmount, frozenset(), frozenset({COOP_EDUCATION_PAYROLL_RANGE})),
        (
            Quotient,
            frozenset({COOP_EDUCATION_PAYROLL_OVER_THRESHOLD, COOP_EDUCATION_PAYROLL_RANGE}),
            frozenset({COOP_EDUCATION_PHASE_OUT_SHARE}),
        ),
        (CreditAmount, frozenset(), frozenset({COOP_EDUCATION_FULL_SHARE})),
        (
            SubtractNotBelowZero,
            frozenset({COOP_EDUCATION_FULL_SHARE, COOP_EDUCATION_PHASE_OUT_SHARE}),
            frozenset({COOP_EDUCATION_REMAINING_SHARE}),
        ),
        (
            CoopEducationCredit,
            frozenset({COOP_EDUCATION_PLACEMENTS, COOP_EDUCATION_REMAINING_SHARE}),
            frozenset({COOP_EDUCATION_CREDIT}),
        ),
        (
            RecordCount,
            frozenset({COOP_EDUCATION_PLACEMENTS}),
            frozenset({COOP_EDUCATION_PLACEMENT_COUNT}),
        ),
        (
            Sum,
            frozenset({ONTARIO_CREDITS_SUBTOTAL, COOP_EDUCATION_CREDIT}),
            frozenset({ONTARIO_CREDITS}),
        ),
        (Sum, frozenset({ONTARIO_CREDITS}), frozenset({PROVINCIAL_CREDITS})),
        (
            CappedAmount,
            frozenset({EDUCATOR_SUPPLIES_EXPENSES}),
            frozenset({EDUCATOR_SUPPLIES_EXPENSES_AT_MOST_MAXIMUM}),
        ),
        (
            ApplyRate,
            frozenset({EDUCATOR_SUPPLIES_EXPENSES_AT_MOST_MAXIMUM}),
            frozenset({EDUCATOR_SCHOOL_SUPPLY_CREDIT}),
        ),
        (
            Sum,
            frozenset(
                {
                    INCOME_TAX_DEDUCTED,
                    CANADA_WORKERS_BENEFIT,
                    PART_XII_2_TAX_CREDIT,
                    EMPLOYEE_AND_PARTNER_GST_HST_REBATE,
                    EDUCATOR_SCHOOL_SUPPLY_CREDIT,
                    JOURNALISM_LABOUR_TAX_CREDIT,
                    TAX_PAID_BY_INSTALMENTS,
                    PROVINCIAL_CREDITS,
                }
            ),
            frozenset({TOTAL_CREDITS}),
        ),
        (
            Subtract,
            frozenset({TOTAL_PAYABLE, TOTAL_CREDITS}),
            frozenset({REFUND_OR_BALANCE_OWING}),
        ),
        (SubtractNotBelowZero, frozenset({TOTAL_CREDITS, TOTAL_PAYABLE}), frozenset({REFUND})),
        (Sum, frozenset({REFUND}), frozenset({ontario.REFUND_BEFORE_DONATION})),
        (
            Subtract,
            frozenset({ontario.REFUND_BEFORE_DONATION, ontario.OPPORTUNITIES_FUND_DONATION}),
            frozenset({ontario.NET_REFUND}),
        ),
    }
