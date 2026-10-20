"""CA-ON 2025 end to end, Return A: return a producers 1."""

from __future__ import annotations

from typing import Any

from app.domain.capabilities.apply_fraction import ApplyFraction
from app.domain.capabilities.apply_rate import ApplyRate
from app.domain.capabilities.at_most import AtMost
from app.domain.capabilities.capped_amount import CappedAmount
from app.domain.capabilities.choose_by_count import ChooseByCount
from app.domain.capabilities.contribution_tier import TieredContribution
from app.domain.capabilities.credit_amount import CreditAmount
from app.domain.capabilities.greater_of import GreaterOf
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
from app.jurisdictions.ca.capabilities.caregiver_amount import CaregiverAmount
from app.jurisdictions.ca.capabilities.chart_a_row_c_total import ChartARowCTotal
from app.jurisdictions.ca.capabilities.chart_b_zone_a_total import ChartBZoneATotal
from app.jurisdictions.ca.capabilities.chart_b_zone_b_total import ChartBZoneBTotal
from app.jurisdictions.ca.capabilities.disability_transfer_amount import DisabilityTransferAmount
from app.jurisdictions.ca.capabilities.other_dependants_medical import OtherDependantsMedical
from app.jurisdictions.ca.capabilities.rental_gross_rents import RentalGrossRents
from app.jurisdictions.ca.capabilities.short_term_rental_gross_rents import (
    ShortTermRentalGrossRents,
)
from app.jurisdictions.ca.capabilities.short_term_rental_non_compliant_expenses import (
    ShortTermRentalNonCompliantExpenses,
)
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
    AGE_AMOUNT,
    AGE_AMOUNT_BEFORE_COUNT,
    AGE_INCOME_OVER_THRESHOLD,
    AGE_INCOME_THRESHOLD,
    AGE_MAXIMUM,
    AGE_REDUCTION,
    AGED_18_OR_OLDER_AT_END_OF_2025,
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
    CLERGY_RESIDENCE_DEDUCTION,
    CPP_BASE_CONTRIBUTIONS,
    CPP_ENHANCED_CONTRIBUTIONS,
    CPP_FIRST_ADDITIONAL_CONTRIBUTIONS,
    CPP_OR_QPP_BENEFITS,
    CPP_SECOND_ADDITIONAL_CONTRIBUTIONS,
    CREDIT_AMOUNTS_AT_CREDIT_RATE,
    CREDITS_AGAINST_BASIC_FEDERAL_TAX,
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
    DISABILITY_SUPPORTS_DEDUCTION,
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
    EMPLOYMENT_INCOME,
    EXPLORATION_AND_DEVELOPMENT_EXPENSES,
    FEDERAL_BASIC_TAX,
    FEDERAL_TAX_AFTER_CREDITS,
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
    GROSS_RENTAL_INCOME,
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
    LIMITED_PARTNERSHIP_LOSSES_OF_OTHER_YEARS,
    MEDICAL_CLAIM,
    MEDICAL_EXPENSES,
    MEDICAL_EXPENSES_OVER_THRESHOLD,
    MEDICAL_NET_INCOME_SHARE,
    MEDICAL_THRESHOLD,
    NET_BUSINESS_INCOME,
    NET_CAPITAL_LOSS_BALANCE_1985_TO_1987,
    NET_CAPITAL_LOSS_BALANCE_1988_AND_1989,
    NET_CAPITAL_LOSS_BALANCE_1990_TO_1999,
    NET_CAPITAL_LOSS_BALANCE_2001_TO_2024,
    NET_CAPITAL_LOSSES_AVAILABLE_TO_CLAIM,
    NET_CAPITAL_LOSSES_CLAIMED,
    NET_CAPITAL_LOSSES_OF_OTHER_YEARS,
    NET_COMMISSION_INCOME,
    NET_FARMING_INCOME,
    NET_FEDERAL_SUPPLEMENTS,
    NET_FEDERAL_TAX,
    NET_FISHING_INCOME,
    NET_INCOME,
    NET_INCOME_BEFORE_ADJUSTMENTS,
    NET_INCOME_LESS_UCCB_AND_RDSP_INCOME,
    NET_PARTNERSHIP_INCOME,
    NET_PROFESSIONAL_INCOME,
    NET_RENTAL_INCOME,
    NO_SLIP_DIVIDEND_TAX_CREDIT,
    NON_CAPITAL_LOSSES_OF_OTHER_YEARS,
    NON_REFUNDABLE_CREDIT_AMOUNTS,
    NON_REFUNDABLE_TAX_CREDITS,
    NORTHERN_RESIDENTS_DEDUCTIONS,
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
    OTHER_EMPLOYMENT_EXPENSES,
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
    POLITICAL_CONTRIBUTIONS,
    RDSP_INCOME,
    RDSP_INCOME_REPAYMENT,
    REFUND_OR_BALANCE_OWING,
    REGULAR_RATE_DONATION_CREDIT,
    REGULAR_RATE_DONATIONS,
    REMAINING_ADJUSTED_LOSSES_1985_TO_1987,
    REMAINING_ADJUSTED_LOSSES_1988_AND_1989,
    REMAINING_ADJUSTED_LOSSES_1990_TO_1999,
    REMAINING_ADJUSTED_LOSSES_2001_TO_2024,
    RENTAL_ADVERTISING,
    RENTAL_ADVERTISING_PERSONAL_PORTION,
    RENTAL_ADVERTISING_SHORT_TERM_PORTION,
    RENTAL_CCA_CLAIM,
    RENTAL_COOWNER,
    RENTAL_COOWNER_OTHER_EXPENSES,
    RENTAL_COOWNER_SHARE,
    RENTAL_DEDUCTIBLE_EXPENSES,
    RENTAL_EXPENSES_LESS_PERSONAL_PORTION,
    RENTAL_GROSS_RENTS,
    RENTAL_INSURANCE,
    RENTAL_INSURANCE_PERSONAL_PORTION,
    RENTAL_INSURANCE_SHORT_TERM_PORTION,
    RENTAL_INTEREST_AND_BANK_CHARGES,
    RENTAL_INTEREST_AND_BANK_CHARGES_PERSONAL_PORTION,
    RENTAL_INTEREST_AND_BANK_CHARGES_SHORT_TERM_PORTION,
    RENTAL_MANAGEMENT_AND_ADMINISTRATION_FEES,
    RENTAL_MANAGEMENT_AND_ADMINISTRATION_FEES_PERSONAL_PORTION,
    RENTAL_MANAGEMENT_AND_ADMINISTRATION_FEES_SHORT_TERM_PORTION,
    RENTAL_MOTOR_VEHICLE_EXPENSES,
    RENTAL_MOTOR_VEHICLE_EXPENSES_PERSONAL_PORTION,
    RENTAL_MOTOR_VEHICLE_EXPENSES_SHORT_TERM_PORTION,
    RENTAL_NET_INCOME_AFTER_CCA,
    RENTAL_NET_INCOME_AFTER_COOWNER_EXPENSES,
    RENTAL_NET_INCOME_AFTER_TERMINAL_LOSS,
    RENTAL_NET_INCOME_BEFORE_ADJUSTMENTS,
    RENTAL_NET_INCOME_SHARE,
    RENTAL_NET_INCOME_WITH_RECAPTURE,
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
    RENTAL_PROPERTY_TAXES,
    RENTAL_PROPERTY_TAXES_PERSONAL_PORTION,
    RENTAL_PROPERTY_TAXES_SHORT_TERM_PORTION,
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
    RESIDENCY_AMOUNT,
    RESIDENCY_DEDUCTION,
    RESIDENCY_NET_INCOME_LIMIT,
    RESIDENT_IN_CANADA_THROUGHOUT_2025,
    RPP_DEDUCTION,
    RRSP_AMOUNT_DEDUCTED,
    RRSP_CONTRIBUTIONS,
    RRSP_CONTRIBUTIONS_AVAILABLE,
    RRSP_DEDUCTION,
    RRSP_DEDUCTION_LIMIT,
    RRSP_DEDUCTION_MAXIMUM,
    RRSP_INCOME,
    SECURITY_OPTIONS_DEDUCTIONS,
    SHORT_TERM_RENTAL_GROSS_RENTS,
    SHORT_TERM_RENTAL_UNITS,
    SLIP_DIVIDEND_TAX_CREDIT,
    SLIP_TAXABLE_DIVIDENDS,
    SLIP_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
    SOCIAL_ASSISTANCE_PAYMENTS,
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
    SPOUSE_NET_INCOME_BEFORE_ADJUSTMENTS,
    SPOUSE_RDSP_INCOME,
    SPOUSE_RDSP_INCOME_REPAYMENT,
    SPOUSE_UCCB_REPAYMENT,
    SPOUSE_UNIVERSAL_CHILD_CARE_BENEFIT,
    SPOUSES_CLAIMED,
    STANDARD_AMOUNT_ALLOCATED,
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
    TOTAL_INCOME,
    TOTAL_INTEREST_EXPENSES,
    TOTAL_OTHER_EXPENSES,
    TOTAL_PAYABLE,
    TRAVEL_DEDUCTION,
    TRAVEL_INDIVIDUALS,
    TRAVEL_TOTAL_ZONE_A,
    TRAVEL_TOTAL_ZONE_B,
    TRAVEL_TRIPS,
    TRAVEL_ZONE_B_DEDUCTION,
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
    WAGE_LOSS_REPLACEMENT_PLAN_INCOME,
    WORKERS_COMPENSATION_BENEFITS,
    WORKING_INCOME,
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
from app.jurisdictions.ca_on import catalog as ontario
from app.jurisdictions.ca_on.capabilities.caregiver_amount import OntarioCaregiverAmount
from app.jurisdictions.ca_on.catalog import (
    COMMUNITY_FOOD_PROGRAM_CREDIT,
    COMMUNITY_FOOD_PROGRAM_DONATIONS,
    COOP_EDUCATION_PAYROLL,
    COOP_EDUCATION_PLACEMENTS,
    DEPENDANTS,
    DEPENDENT_CHILDREN,
    ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_MAXIMUM,
    ELIGIBLE_DEPENDANT_BASE,
    FERTILITY_CREDIT,
    FERTILITY_CREDIT_BEFORE_MAXIMUM,
    FERTILITY_EXPENSES,
    FLOW_THROUGH_SHARE_SLIPS,
    LIFT_CREDIT,
    LIFT_CREDIT_BEFORE_MAXIMUM,
    LIFT_MAXIMUM_CREDIT,
    LIFT_REDUCTION,
    ONTARIO_BASIC_TAX,
    ONTARIO_HEALTH_PREMIUM,
    ONTARIO_SURTAX,
    ONTARIO_TAX,
    ONTARIO_TAX_AFTER_CREDITS,
    ONTARIO_TAX_AFTER_FOOD_CREDIT,
    ONTARIO_TAX_AFTER_LIFT_CREDIT,
    ONTARIO_TAX_AFTER_REDUCTION,
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
from tests.jurisdictions.ca_on.end_to_end.support import return_a


def test_each_amount_is_produced_by_its_capability() -> None:
    worksheet = return_a()
    assert worksheet.producer_of(EMPLOYMENT_INCOME) is None
    assert worksheet.producer_of(CAPITAL_GAIN) is None
    assert worksheet.producer_of(UNUSED_RRSP_CONTRIBUTIONS) is None
    assert worksheet.producer_of(RRSP_CONTRIBUTIONS) is None
    assert worksheet.producer_of(RRSP_DEDUCTION_LIMIT) is None
    assert worksheet.producer_of(RRSP_AMOUNT_DEDUCTED) is None
    assert worksheet.producer_of(UNION_DUES) is None
    assert worksheet.producer_of(DEPENDENT_CHILDREN) is None
    assert worksheet.producer_of(DEPENDANTS) is None
    assert worksheet.producer_of(ELIGIBLE_DEPENDANTS) is None
    assert worksheet.producer_of(DEPENDANT_NET_INCOME) is None
    assert worksheet.producer_of(INFIRM_DEPENDANTS) is None
    assert worksheet.producer_of(MEDICAL_EXPENSES) is None
    assert worksheet.producer_of(OTHER_DEPENDANTS) is None
    assert worksheet.producer_of(ontario.CAREGIVER_DEPENDANTS) is None
    assert worksheet.producer_of(DISABILITY_DEPENDANTS) is None
    assert worksheet.producer_of(INFIRM_CHILDREN) is None
    assert worksheet.producer_of(BORN_IN_1960_OR_EARLIER) is None
    assert worksheet.producer_of(SPOUSE_NET_INCOME) is None
    assert worksheet.producer_of(SPOUSES_CLAIMED) is None
    assert worksheet.producer_of(SPOUSE_CAREGIVER_ELIGIBLE) is None
    assert worksheet.producer_of(CHILD_CARE_EXPENSES_PAID) is None
    assert worksheet.producer_of(CHILDREN_UNDER_SEVEN) is None
    assert worksheet.producer_of(CHILDREN_WITH_DISABILITY) is None
    assert worksheet.producer_of(CHILDREN_SEVEN_TO_SIXTEEN) is None
    assert worksheet.producer_of(CWB_ELIGIBLE_DEPENDANTS) is None
    assert worksheet.producer_of(INCOME_TAX_DEDUCTED) is None
    assert worksheet.producer_of(FERTILITY_EXPENSES) is None
    assert worksheet.producer_of(SENIORS_TRANSIT_PAID) is None
    assert worksheet.producer_of(FLOW_THROUGH_SHARE_SLIPS) is None
    assert worksheet.producer_of(COOP_EDUCATION_PAYROLL) is None
    assert worksheet.producer_of(COOP_EDUCATION_PLACEMENTS) is None
    assert worksheet.producer_of(COMMUNITY_FOOD_PROGRAM_DONATIONS) is None
    assert worksheet.producer_of(CHARITABLE_DONATIONS) is None
    assert worksheet.producer_of(GOVERNMENT_DONATIONS) is None
    assert worksheet.producer_of(UNIVERSITY_DONATIONS_OUTSIDE_CANADA) is None
    assert worksheet.producer_of(FOREIGN_CHARITY_DONATIONS) is None
    assert worksheet.producer_of(ECOLOGICAL_AND_CULTURAL_GIFTS) is None
    assert worksheet.producer_of(ECOLOGICAL_GIFTS_BEFORE_2016) is None
    assert worksheet.producer_of(DEPRECIABLE_GIFT_RECAPTURED_DEPRECIATION) is None
    assert worksheet.producer_of(DEPRECIABLE_GIFT_NET_PROCEEDS) is None
    assert worksheet.producer_of(DEPRECIABLE_GIFT_CAPITAL_COST) is None
    assert worksheet.producer_of(CAPITAL_GIFT_TAXABLE_GAINS) is None
    assert worksheet.producer_of(CAPITAL_GIFT_GAINS_DEDUCTION) is None
    assert worksheet.producer_of(ontario.POLITICAL_CONTRIBUTIONS) is None
    assert worksheet.producer_of(POLITICAL_CONTRIBUTIONS) is None
    assert worksheet.producer_of(DISABILITY_SUPPORTS_DEDUCTION) is None
    assert worksheet.producer_of(OTHER_EMPLOYMENT_EXPENSES) is None
    assert worksheet.producer_of(CLERGY_RESIDENCE_DEDUCTION) is None
    assert worksheet.producer_of(NET_BUSINESS_INCOME) is None
    assert worksheet.producer_of(NET_PROFESSIONAL_INCOME) is None
    assert worksheet.producer_of(NET_COMMISSION_INCOME) is None
    assert worksheet.producer_of(NET_FARMING_INCOME) is None
    assert worksheet.producer_of(NET_FISHING_INCOME) is None
    assert worksheet.producer_of(WAGE_LOSS_REPLACEMENT_PLAN_INCOME) is None
    assert worksheet.producer_of(RESIDENT_IN_CANADA_THROUGHOUT_2025) is None
    assert worksheet.producer_of(AGED_18_OR_OLDER_AT_END_OF_2025) is None
    assert worksheet.producer_of(SPOUSE_NET_INCOME_BEFORE_ADJUSTMENTS) is None
    assert worksheet.producer_of(SPOUSE_UCCB_REPAYMENT) is None
    assert worksheet.producer_of(SPOUSE_RDSP_INCOME_REPAYMENT) is None
    assert worksheet.producer_of(SPOUSE_UNIVERSAL_CHILD_CARE_BENEFIT) is None
    assert worksheet.producer_of(SPOUSE_RDSP_INCOME) is None
    assert worksheet.producer_of(ontario.LIFT_SPOUSE_AT_YEAR_END) is None
    assert worksheet.producer_of(OTHER_EMPLOYMENT_INCOME) is None
    assert worksheet.producer_of(OLD_AGE_SECURITY) is None
    assert worksheet.producer_of(CPP_OR_QPP_BENEFITS) is None
    assert worksheet.producer_of(OTHER_PENSIONS_AND_SUPERANNUATION) is None
    assert worksheet.producer_of(ELECTED_SPLIT_PENSION_AMOUNT) is None
    assert worksheet.producer_of(UNIVERSAL_CHILD_CARE_BENEFIT) is None
    assert worksheet.producer_of(EI_AND_OTHER_BENEFITS) is None
    assert worksheet.producer_of(T3_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE) is None
    assert worksheet.producer_of(T4PS_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE) is None
    assert worksheet.producer_of(T5_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE) is None
    assert worksheet.producer_of(T5013_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE) is None
    assert worksheet.producer_of(T3_TAXABLE_DIVIDENDS) is None
    assert worksheet.producer_of(T4PS_TAXABLE_DIVIDENDS) is None
    assert worksheet.producer_of(T5_TAXABLE_DIVIDENDS) is None
    assert worksheet.producer_of(T5013_TAXABLE_DIVIDENDS) is None
    assert worksheet.producer_of(ELIGIBLE_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP) is None
    assert worksheet.producer_of(OTHER_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP) is None
    assert worksheet.producer_of(T3_DIVIDEND_TAX_CREDIT) is None
    assert worksheet.producer_of(T4PS_DIVIDEND_TAX_CREDIT) is None
    assert worksheet.producer_of(T5_DIVIDEND_TAX_CREDIT) is None
    assert worksheet.producer_of(T5013_DIVIDEND_TAX_CREDIT) is None
    assert worksheet.producer_of(T3_INVESTMENT_INCOME) is None
    assert worksheet.producer_of(T5_INVESTMENT_INCOME) is None
    assert worksheet.producer_of(T5013_INVESTMENT_INCOME) is None
    assert worksheet.producer_of(INVESTMENT_INCOME_CREDITED_NOT_RECEIVED) is None
    assert worksheet.producer_of(TAX_REFUND_INTEREST) is None
    assert worksheet.producer_of(FOREIGN_INVESTMENT_INCOME) is None
    assert worksheet.producer_of(INVESTMENT_INCOME_WITHOUT_A_SLIP) is None
    assert worksheet.producer_of(INVESTMENT_ROYALTIES) is None
    assert worksheet.producer_of(INVESTMENT_INCOME_REPORTED_IN_PREVIOUS_YEARS) is None
    assert worksheet.producer_of(NET_PARTNERSHIP_INCOME) is None
    assert worksheet.producer_of(RDSP_INCOME) is None
    # T776 Parts 3 and 4 and T1 lines 12599 and 12600: the caller's rows, expense boxes and the
    # co-owner's and partner's figures are starting inputs; every other line has a producer.
    assert worksheet.producer_of(RENTAL_PROPERTIES) is None
    assert worksheet.producer_of(RENTAL_OTHER_INCOME) is None
    assert worksheet.producer_of(RENTAL_ADVERTISING) is None
    assert worksheet.producer_of(RENTAL_ADVERTISING_PERSONAL_PORTION) is None
    assert worksheet.producer_of(RENTAL_ADVERTISING_SHORT_TERM_PORTION) is None
    assert worksheet.producer_of(RENTAL_INSURANCE) is None
    assert worksheet.producer_of(RENTAL_INSURANCE_PERSONAL_PORTION) is None
    assert worksheet.producer_of(RENTAL_INSURANCE_SHORT_TERM_PORTION) is None
    assert worksheet.producer_of(RENTAL_INTEREST_AND_BANK_CHARGES) is None
    assert worksheet.producer_of(RENTAL_INTEREST_AND_BANK_CHARGES_PERSONAL_PORTION) is None
    assert worksheet.producer_of(RENTAL_INTEREST_AND_BANK_CHARGES_SHORT_TERM_PORTION) is None
    assert worksheet.producer_of(RENTAL_OFFICE_EXPENSES) is None
    assert worksheet.producer_of(RENTAL_OFFICE_EXPENSES_PERSONAL_PORTION) is None
    assert worksheet.producer_of(RENTAL_OFFICE_EXPENSES_SHORT_TERM_PORTION) is None
    assert worksheet.producer_of(RENTAL_PROFESSIONAL_FEES) is None
    assert worksheet.producer_of(RENTAL_PROFESSIONAL_FEES_PERSONAL_PORTION) is None
    assert worksheet.producer_of(RENTAL_PROFESSIONAL_FEES_SHORT_TERM_PORTION) is None
    assert worksheet.producer_of(RENTAL_MANAGEMENT_AND_ADMINISTRATION_FEES) is None
    assert worksheet.producer_of(RENTAL_MANAGEMENT_AND_ADMINISTRATION_FEES_PERSONAL_PORTION) is None
    assert (
        worksheet.producer_of(RENTAL_MANAGEMENT_AND_ADMINISTRATION_FEES_SHORT_TERM_PORTION) is None
    )
    assert worksheet.producer_of(RENTAL_REPAIRS_AND_MAINTENANCE) is None
    assert worksheet.producer_of(RENTAL_REPAIRS_AND_MAINTENANCE_PERSONAL_PORTION) is None
    assert worksheet.producer_of(RENTAL_REPAIRS_AND_MAINTENANCE_SHORT_TERM_PORTION) is None
    assert worksheet.producer_of(RENTAL_SALARIES_WAGES_AND_BENEFITS) is None
    assert worksheet.producer_of(RENTAL_SALARIES_WAGES_AND_BENEFITS_PERSONAL_PORTION) is None
    assert worksheet.producer_of(RENTAL_SALARIES_WAGES_AND_BENEFITS_SHORT_TERM_PORTION) is None
    assert worksheet.producer_of(RENTAL_PROPERTY_TAXES) is None
    assert worksheet.producer_of(RENTAL_PROPERTY_TAXES_PERSONAL_PORTION) is None
    assert worksheet.producer_of(RENTAL_PROPERTY_TAXES_SHORT_TERM_PORTION) is None
    assert worksheet.producer_of(RENTAL_TRAVEL) is None
    assert worksheet.producer_of(RENTAL_TRAVEL_PERSONAL_PORTION) is None
    assert worksheet.producer_of(RENTAL_TRAVEL_SHORT_TERM_PORTION) is None
    assert worksheet.producer_of(RENTAL_UTILITIES) is None
    assert worksheet.producer_of(RENTAL_UTILITIES_PERSONAL_PORTION) is None
    assert worksheet.producer_of(RENTAL_UTILITIES_SHORT_TERM_PORTION) is None
    assert worksheet.producer_of(RENTAL_MOTOR_VEHICLE_EXPENSES) is None
    assert worksheet.producer_of(RENTAL_MOTOR_VEHICLE_EXPENSES_PERSONAL_PORTION) is None
    assert worksheet.producer_of(RENTAL_MOTOR_VEHICLE_EXPENSES_SHORT_TERM_PORTION) is None
    assert worksheet.producer_of(RENTAL_OTHER_EXPENSES) is None
    assert worksheet.producer_of(RENTAL_OTHER_EXPENSES_PERSONAL_PORTION) is None
    assert worksheet.producer_of(RENTAL_OTHER_EXPENSES_SHORT_TERM_PORTION) is None
    assert worksheet.producer_of(RENTAL_COOWNER) is None
    assert worksheet.producer_of(RENTAL_COOWNER_SHARE) is None
    assert worksheet.producer_of(RENTAL_COOWNER_OTHER_EXPENSES) is None
    assert worksheet.producer_of(RENTAL_RECAPTURED_CCA) is None
    assert worksheet.producer_of(RENTAL_TERMINAL_LOSS) is None
    assert worksheet.producer_of(RENTAL_CCA_CLAIM) is None
    assert worksheet.producer_of(RENTAL_PARTNER) is None
    assert worksheet.producer_of(RENTAL_PARTNER_SHARE) is None
    assert worksheet.producer_of(RENTAL_PARTNER_GST_HST_REBATE) is None
    assert worksheet.producer_of(RENTAL_PARTNER_OTHER_EXPENSES) is None
    assert worksheet.producer_of(SHORT_TERM_RENTAL_UNITS) is None
    assert isinstance(
        worksheet.producer_of(SHORT_TERM_RENTAL_GROSS_RENTS), ShortTermRentalGrossRents
    )
    assert isinstance(worksheet.producer_of(RENTAL_GROSS_RENTS), RentalGrossRents)
    assert isinstance(worksheet.producer_of(GROSS_RENTAL_INCOME), Sum)
    assert isinstance(worksheet.producer_of(RENTAL_TOTAL_EXPENSES), Sum)
    assert isinstance(worksheet.producer_of(RENTAL_PERSONAL_PORTION), Sum)
    assert isinstance(worksheet.producer_of(RENTAL_SHORT_TERM_PORTION), Sum)
    assert isinstance(
        worksheet.producer_of(RENTAL_NON_COMPLIANT_EXPENSES), ShortTermRentalNonCompliantExpenses
    )
    assert isinstance(worksheet.producer_of(RENTAL_EXPENSES_LESS_PERSONAL_PORTION), Subtract)
    assert isinstance(worksheet.producer_of(RENTAL_DEDUCTIBLE_EXPENSES), Subtract)
    assert isinstance(worksheet.producer_of(RENTAL_NET_INCOME_BEFORE_ADJUSTMENTS), Subtract)
    assert isinstance(worksheet.producer_of(RENTAL_NET_INCOME_SHARE), ChooseByCount)
    assert isinstance(worksheet.producer_of(RENTAL_NET_INCOME_AFTER_COOWNER_EXPENSES), Subtract)
    assert isinstance(worksheet.producer_of(RENTAL_NET_INCOME_WITH_RECAPTURE), Sum)
    assert isinstance(worksheet.producer_of(RENTAL_NET_INCOME_AFTER_TERMINAL_LOSS), Subtract)
    assert isinstance(worksheet.producer_of(RENTAL_NET_INCOME_AFTER_CCA), Subtract)
    assert isinstance(worksheet.producer_of(RENTAL_PARTNER_SHARE_WITH_REBATE), Sum)
    assert isinstance(worksheet.producer_of(RENTAL_PARTNERSHIP_NET_INCOME), Subtract)
    assert isinstance(worksheet.producer_of(NET_RENTAL_INCOME), ChooseByCount)
    assert worksheet.producer_of(RENTAL_GROSS_RENTS) is not worksheet.producer_of(
        SHORT_TERM_RENTAL_GROSS_RENTS
    )
    assert worksheet.producer_of(RENTAL_NET_INCOME_SHARE) is not worksheet.producer_of(
        NET_RENTAL_INCOME
    )
    assert worksheet.producer_of(TAXABLE_SUPPORT_PAYMENTS) is None
    assert worksheet.producer_of(RRSP_INCOME) is None
    assert worksheet.producer_of(FHSA_INCOME) is None
    assert worksheet.producer_of(OTHER_FHSA_INCOME) is None
    assert worksheet.producer_of(OTHER_INCOME) is None
    assert worksheet.producer_of(TAXABLE_SCHOLARSHIPS) is None
    assert worksheet.producer_of(WORKERS_COMPENSATION_BENEFITS) is None
    assert worksheet.producer_of(SOCIAL_ASSISTANCE_PAYMENTS) is None
    assert worksheet.producer_of(NET_FEDERAL_SUPPLEMENTS) is None
    for starting_kind in (
        UCCB_REPAYMENT,
        RDSP_INCOME_REPAYMENT,
        CANADIAN_ARMED_FORCES_AND_POLICE_DEDUCTION,
        SECURITY_OPTIONS_DEDUCTIONS,
        LIMITED_PARTNERSHIP_LOSSES_OF_OTHER_YEARS,
        NON_CAPITAL_LOSSES_OF_OTHER_YEARS,
        UNAPPLIED_NET_CAPITAL_LOSSES_1985_TO_1987,
        UNAPPLIED_NET_CAPITAL_LOSSES_1988_AND_1989,
        UNAPPLIED_NET_CAPITAL_LOSSES_1990_TO_1999,
        UNAPPLIED_NET_CAPITAL_LOSSES_2001_TO_2024,
        NET_CAPITAL_LOSSES_CLAIMED,
        ADDITIONAL_DEDUCTIONS,
        OTHER_PAYMENTS_DEDUCTION_ABOVE_LIMIT,
        OTHER_PAYMENTS_WORKSHEET_REQUIRED,
        OTHER_PAYMENTS_WORKSHEET_LINE_9_OVER_LIMIT,
    ):
        assert worksheet.producer_of(starting_kind) is None, starting_kind.identifier
    assert isinstance(worksheet.producer_of(UCCB_AND_RDSP_INCOME), Sum)
    assert isinstance(worksheet.producer_of(NET_INCOME_LESS_UCCB_AND_RDSP_INCOME), Subtract)
    assert isinstance(worksheet.producer_of(UCCB_AND_RDSP_INCOME_REPAYMENTS), Sum)
    assert isinstance(worksheet.producer_of(OTHER_PAYMENTS_LIMIT_INCOME), Sum)
    assert isinstance(worksheet.producer_of(OTHER_PAYMENTS_DEDUCTION_AFTER_LIMIT), ChooseByCount)
    assert isinstance(worksheet.producer_of(OTHER_PAYMENTS_DEDUCTION), ChooseByCount)
    assert worksheet.producer_of(OTHER_PAYMENTS_DEDUCTION_AFTER_LIMIT) is not (
        worksheet.producer_of(OTHER_PAYMENTS_DEDUCTION)
    )
    assert worksheet.producer_of(OTHER_PAYMENTS_DEDUCTION) is not (
        worksheet.producer_of(CANADA_WORKERS_BENEFIT)
    )
    # Form T2222: the days, the special work site benefits and the two record lists are starting
    # artifacts; every line of Steps 2 to 4 has a producer of its own.
    t2222_start: Any
    for t2222_start in (
        ZONE_A_DAYS_LIVED,
        ZONE_A_ADDITIONAL_RESIDENCY_DAYS,
        ZONE_A_SPECIAL_WORK_SITE_BENEFITS,
        ZONE_B_DAYS_LIVED,
        ZONE_B_ADDITIONAL_RESIDENCY_DAYS,
        ZONE_B_SPECIAL_WORK_SITE_BENEFITS,
        TRAVEL_TRIPS,
        TRAVEL_INDIVIDUALS,
    ):
        assert worksheet.producer_of(t2222_start) is None, t2222_start.identifier
    for kind in (
        ZONE_A_BASIC_RESIDENCY_AMOUNT,
        ZONE_A_ADDITIONAL_RESIDENCY_AMOUNT,
        ZONE_B_BASIC_RESIDENCY_AMOUNT,
        ZONE_B_ADDITIONAL_RESIDENCY_AMOUNT,
    ):
        assert isinstance(worksheet.producer_of(kind), PerUnitAmount), kind
    for kind in (
        ZONE_A_RESIDENCY_AMOUNT,
        ZONE_B_RESIDENCY_AMOUNT,
        RESIDENCY_AMOUNT,
        TRAVEL_DEDUCTION,
        NORTHERN_RESIDENTS_DEDUCTIONS,
    ):
        assert isinstance(worksheet.producer_of(kind), Sum), kind
    assert isinstance(worksheet.producer_of(ZONE_A_RESIDENCY_AFTER_WORK_SITE), SubtractNotBelowZero)
    assert isinstance(worksheet.producer_of(ZONE_B_RESIDENCY_AFTER_WORK_SITE), SubtractNotBelowZero)
    assert isinstance(worksheet.producer_of(RESIDENCY_NET_INCOME_LIMIT), ApplyRate)
    assert isinstance(worksheet.producer_of(TRAVEL_ZONE_B_DEDUCTION), ApplyRate)
    assert isinstance(worksheet.producer_of(RESIDENCY_DEDUCTION), LesserOf)
    assert isinstance(worksheet.producer_of(TRAVEL_TOTAL_ZONE_A), ChartBZoneATotal)
    assert isinstance(worksheet.producer_of(TRAVEL_TOTAL_ZONE_B), ChartBZoneBTotal)
    assert isinstance(worksheet.producer_of(STANDARD_AMOUNT_ALLOCATED), ChartARowCTotal)
    # One capability for each line: no two of these lines share one.
    producers = [
        worksheet.producer_of(kind)
        for kind in (
            ZONE_A_BASIC_RESIDENCY_AMOUNT,
            ZONE_A_ADDITIONAL_RESIDENCY_AMOUNT,
            ZONE_B_BASIC_RESIDENCY_AMOUNT,
            ZONE_B_ADDITIONAL_RESIDENCY_AMOUNT,
            ZONE_A_RESIDENCY_AMOUNT,
            ZONE_B_RESIDENCY_AMOUNT,
            ZONE_A_RESIDENCY_AFTER_WORK_SITE,
            ZONE_B_RESIDENCY_AFTER_WORK_SITE,
            RESIDENCY_AMOUNT,
            RESIDENCY_NET_INCOME_LIMIT,
            RESIDENCY_DEDUCTION,
            TRAVEL_TOTAL_ZONE_A,
            TRAVEL_TOTAL_ZONE_B,
            STANDARD_AMOUNT_ALLOCATED,
            TRAVEL_ZONE_B_DEDUCTION,
            TRAVEL_DEDUCTION,
            NORTHERN_RESIDENTS_DEDUCTIONS,
        )
    ]
    assert len({id(producer) for producer in producers}) == len(producers)
    assert isinstance(worksheet.producer_of(INVESTMENT_INCOME_BEFORE_PRIOR_YEARS), Sum)
    assert isinstance(worksheet.producer_of(INTEREST_AND_OTHER_INVESTMENT_INCOME), Subtract)
    assert isinstance(worksheet.producer_of(INCOME_SUPPORT_BENEFITS), Sum)
    for kind in (
        SLIP_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
        SLIP_TAXABLE_DIVIDENDS,
        DIVIDENDS_WITHOUT_A_SLIP_GROSSED_UP,
        TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
        TAXABLE_DIVIDENDS,
        SLIP_DIVIDEND_TAX_CREDIT,
        DIVIDENDS_AMOUNT_A,
        DIVIDENDS_AMOUNT_B,
        NO_SLIP_DIVIDEND_TAX_CREDIT,
        DIVIDEND_TAX_CREDIT,
        CREDITS_AGAINST_BASIC_FEDERAL_TAX,
    ):
        assert isinstance(worksheet.producer_of(kind), Sum), kind
    assert isinstance(worksheet.producer_of(ELIGIBLE_DIVIDENDS_GROSSED_UP), ApplyFraction)
    assert isinstance(worksheet.producer_of(OTHER_DIVIDENDS_GROSSED_UP), ApplyFraction)
    assert isinstance(worksheet.producer_of(OTHER_DIVIDENDS_CREDIT), ApplyRate)
    assert isinstance(worksheet.producer_of(ELIGIBLE_DIVIDENDS_CREDIT), ApplyRate)
    assert isinstance(worksheet.producer_of(DIVIDENDS_AMOUNT_A_LESS_B), Subtract)
    assert worksheet.producer_of(ELIGIBLE_DIVIDENDS_GROSSED_UP) is not (
        worksheet.producer_of(OTHER_DIVIDENDS_GROSSED_UP)
    )
    assert worksheet.producer_of(OTHER_DIVIDENDS_CREDIT) is not (
        worksheet.producer_of(ELIGIBLE_DIVIDENDS_CREDIT)
    )
    assert worksheet.producer_of(INTEREST_AND_OTHER_INVESTMENT_INCOME) is not (
        worksheet.producer_of(REFUND_OR_BALANCE_OWING)
    )
    assert worksheet.producer_of(INVESTMENT_INCOME_BEFORE_PRIOR_YEARS) is not (
        worksheet.producer_of(INCOME_SUPPORT_BENEFITS)
    )
    assert isinstance(worksheet.producer_of(RRSP_CONTRIBUTIONS_AVAILABLE), Sum)
    assert isinstance(worksheet.producer_of(RRSP_DEDUCTION_MAXIMUM), LesserOf)
    assert isinstance(worksheet.producer_of(RRSP_DEDUCTION), AtMost)
    assert isinstance(worksheet.producer_of(UNUSED_RRSP_CONTRIBUTIONS_CARRIED_FORWARD), Subtract)
    assert worksheet.producer_of(UNUSED_RRSP_CONTRIBUTIONS_CARRIED_FORWARD) is not (
        worksheet.producer_of(REFUND_OR_BALANCE_OWING)
    )
    assert isinstance(worksheet.producer_of(CPP_BASE_CONTRIBUTIONS), TieredContribution)
    assert isinstance(worksheet.producer_of(CPP_FIRST_ADDITIONAL_CONTRIBUTIONS), TieredContribution)
    assert isinstance(
        worksheet.producer_of(CPP_SECOND_ADDITIONAL_CONTRIBUTIONS), TieredContribution
    )
    tiers = {
        worksheet.producer_of(kind)
        for kind in (
            CPP_BASE_CONTRIBUTIONS,
            CPP_FIRST_ADDITIONAL_CONTRIBUTIONS,
            CPP_SECOND_ADDITIONAL_CONTRIBUTIONS,
        )
    }
    assert len(tiers) == 3
    assert isinstance(worksheet.producer_of(EI_PREMIUMS), TieredContribution)
    assert worksheet.producer_of(EI_PREMIUMS) not in tiers
    assert isinstance(worksheet.producer_of(CPP_ENHANCED_CONTRIBUTIONS), Sum)
    assert isinstance(worksheet.producer_of(TAXABLE_CAPITAL_GAINS), ApplyRate)
    assert isinstance(worksheet.producer_of(TOTAL_INCOME), Sum)
    child_care_limits = {
        worksheet.producer_of(kind)
        for kind in (
            CHILD_CARE_LIMIT_FOR_CHILDREN_UNDER_SEVEN,
            CHILD_CARE_LIMIT_FOR_CHILDREN_WITH_DISABILITY,
            CHILD_CARE_LIMIT_FOR_CHILDREN_SEVEN_TO_SIXTEEN,
        )
    }
    assert len(child_care_limits) == 3
    assert all(isinstance(producer, PerUnitAmount) for producer in child_care_limits)
    assert isinstance(worksheet.producer_of(CHILD_CARE_BASIC_LIMIT), Sum)
    assert isinstance(worksheet.producer_of(CHILD_CARE_EARNED_INCOME), Sum)
    assert worksheet.producer_of(CHILD_CARE_EARNED_INCOME) is not worksheet.producer_of(
        WORKING_INCOME
    )
    assert isinstance(worksheet.producer_of(CHILD_CARE_EARNED_INCOME_LIMIT), ApplyFraction)
    assert isinstance(worksheet.producer_of(CHILD_CARE_EXPENSES), LesserOf)
    assert worksheet.producer_of(CHILD_CARE_EXPENSES) is not worksheet.producer_of(
        RRSP_DEDUCTION_MAXIMUM
    )
    assert isinstance(worksheet.producer_of(DEDUCTIONS_FROM_TOTAL_INCOME), Sum)
    assert isinstance(worksheet.producer_of(NET_INCOME), SubtractNotBelowZero)
    for starting_kind in (
        RPP_DEDUCTION,
        ELECTED_SPLIT_PENSION_DEDUCTION,
        SUPPORT_PAYMENTS_DEDUCTION,
        EXPLORATION_AND_DEVELOPMENT_EXPENSES,
        OTHER_DEDUCTIONS,
        TOTAL_CARRYING_CHARGES,
        TOTAL_INTEREST_EXPENSES,
        TOTAL_OTHER_EXPENSES,
        CAPITAL_GAINS_DEDUCTIONS_1985_TO_1987,
        CAPITAL_GAINS_DEDUCTIONS_1988_AND_1989_OTHER_THAN_ELIGIBLE_CAPITAL_PROPERTY,
        CAPITAL_GAINS_DEDUCTIONS_1988_AND_1989_ELIGIBLE_CAPITAL_PROPERTY,
        CAPITAL_GAINS_DEDUCTIONS_1990_TO_1999,
        CAPITAL_GAINS_DEDUCTIONS_2000,
        CAPITAL_GAINS_DEDUCTIONS_2001_TO_2024,
        OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_1994,
        OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1994_TO_1996,
        OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1997_TO_1999,
        OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2000,
        OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2001_TO_2023,
        OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2024,
        BUSINESS_INVESTMENT_LOSS,
        FHSA_CONTRIBUTIONS_IN_2025,
        FHSA_CONTRIBUTIONS_IN_2025_AFTER_FIRST_QUALIFYING_WITHDRAWAL,
        FHSA_VARIABLE_B_AMOUNT,
        FHSA_DESIGNATED_WITHDRAWALS_IN_2025,
        FHSA_CONTRIBUTIONS_IN_2024,
        FHSA_CONTRIBUTIONS_IN_2024_BEFORE_FIRST_QUALIFYING_WITHDRAWAL,
        FHSA_CARRYFORWARD_FOR_2025,
        FHSA_RRSP_TRANSFERS_IN_2024_AND_PRIOR_YEARS,
        FHSA_RRSP_TRANSFERS_IN_2025,
        FHSA_DESIGNATED_TRANSFERS_IN_2024_AND_PRIOR_YEARS,
        FHSA_DESIGNATED_TRANSFERS_IN_2025,
        FHSA_VARIABLE_H_AMOUNT,
        FHSA_CARRYFORWARD_FOR_2024,
        FHSA_VARIABLE_F_AMOUNT,
        FHSA_ANNUAL_LIMITS_FOR_2024_AND_PRIOR_YEARS,
        FHSA_DEDUCTIONS_FOR_2024_AND_PRIOR_YEARS,
        FHSA_UNUSED_CONTRIBUTIONS_BROUGHT_FORWARD,
        FHSA_CONTRIBUTIONS_DEDUCTED,
        FHSA_MAXIMUM_PARTICIPATION_PERIOD_ENDED,
    ):
        assert worksheet.producer_of(starting_kind) is None, starting_kind.identifier
    for kind in (
        CARRYING_CHARGES_INTEREST_EXPENSES_AND_OTHER_EXPENSES,
        CAPITAL_GAINS_DEDUCTIONS_CLAIMED_1985_TO_2024,
        OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_2024,
        FHSA_CONTRIBUTIONS_PLUS_VARIABLE_B_AMOUNT,
        FHSA_CONTRIBUTIONS_AFTER_FIRST_QUALIFYING_WITHDRAWAL,
        FHSA_ANNUAL_AMOUNT_WITH_CARRYFORWARD,
        FHSA_TOTAL_RRSP_TRANSFERS,
        FHSA_TOTAL_DESIGNATED_TRANSFERS,
        FHSA_ANNUAL_AMOUNT_FOR_2024_WITH_CARRYFORWARD,
        FHSA_TRANSFER_AMOUNT_PLUS_VARIABLE_F_AMOUNT,
        FHSA_TOTAL_ANNUAL_LIMITS,
        FHSA_UNUSED_CONTRIBUTIONS_PLUS_CONTRIBUTIONS,
    ):
        assert isinstance(worksheet.producer_of(kind), Sum), kind.identifier
    for kind in (
        BUSINESS_INVESTMENT_LOSS_REDUCTION_AVAILABLE,
        BUSINESS_INVESTMENT_LOSS_AFTER_REDUCTION,
        FHSA_CONTRIBUTIONS_IN_2025_BEFORE_FIRST_QUALIFYING_WITHDRAWAL,
        FHSA_CONTRIBUTIONS_IN_2024_AFTER_FIRST_QUALIFYING_WITHDRAWAL,
        FHSA_NET_RRSP_TRANSFER_AMOUNT,
        FHSA_NET_RRSP_TRANSFER_AMOUNT_FOR_2024_AND_PRIOR_YEARS,
        FHSA_NET_TRANSFER_AMOUNT_AFTER_PRIOR_YEARS,
        FHSA_ANNUAL_LIMITS_LESS_DEDUCTIONS,
        FHSA_LIFETIME_LIMIT_LESS_DEDUCTIONS,
        FHSA_CONTRIBUTIONS_AVAILABLE,
        FHSA_UNUSED_CONTRIBUTIONS_CARRIED_FORWARD,
        NET_INCOME_BEFORE_ADJUSTMENTS,
    ):
        assert isinstance(worksheet.producer_of(kind), Subtract), kind.identifier
    for kind in (
        FHSA_EXCESS_DESIGNATED_WITHDRAWALS,
        FHSA_CONTRIBUTIONS_LIMIT,
        FHSA_NET_TRANSFER_AMOUNT_LESS_VARIABLE_H_AMOUNT,
        FHSA_ANNUAL_AMOUNT_AFTER_TRANSFERS,
        FHSA_LIFETIME_LIMIT_LESS_DEDUCTIONS_AND_TRANSFERS,
    ):
        assert isinstance(worksheet.producer_of(kind), SubtractNotBelowZero), kind.identifier
    for kind in (
        BUSINESS_INVESTMENT_LOSS_REDUCTION,
        FHSA_TRANSFER_AMOUNT_AT_MOST_LIMIT,
        FHSA_ANNUAL_LIMIT_FROM_STEP_2,
        FHSA_MAXIMUM_DEDUCTION,
    ):
        assert isinstance(worksheet.producer_of(kind), LesserOf), kind.identifier
    for kind in (ALLOWABLE_BUSINESS_INVESTMENT_LOSS,):
        assert isinstance(worksheet.producer_of(kind), ApplyRate), kind.identifier
    for kind in (
        FHSA_ANNUAL_AMOUNT,
        FHSA_ANNUAL_AMOUNT_FOR_2024,
        FHSA_ANNUAL_LIMIT_AFTER_MAXIMUM_PARTICIPATION_PERIOD,
        FHSA_LIFETIME_LIMIT,
    ):
        assert isinstance(worksheet.producer_of(kind), CreditAmount), kind.identifier
    for kind in (FHSA_ANNUAL_LIMIT,):
        assert isinstance(worksheet.producer_of(kind), ChooseByCount), kind.identifier
    for kind in (FHSA_DEDUCTION,):
        assert isinstance(worksheet.producer_of(kind), AtMost), kind.identifier
    assert worksheet.producer_of(FHSA_ANNUAL_AMOUNT) is not (
        worksheet.producer_of(FHSA_ANNUAL_AMOUNT_FOR_2024)
    )
    assert worksheet.producer_of(FHSA_ANNUAL_LIMIT) is not (
        worksheet.producer_of(FHSA_ANNUAL_LIMIT_FROM_STEP_2)
    )
    assert worksheet.producer_of(NET_INCOME_BEFORE_ADJUSTMENTS) is not (
        worksheet.producer_of(NET_INCOME)
    )
    assert worksheet.producer_of(TOTAL_INCOME) is not worksheet.producer_of(
        DEDUCTIONS_FROM_TOTAL_INCOME
    )
    assert isinstance(worksheet.producer_of(DEDUCTIONS_FROM_NET_INCOME), Sum)
    assert isinstance(
        worksheet.producer_of(ADJUSTED_GROSS_CAPITAL_LOSSES_1985_TO_1987), ApplyFraction
    )
    assert isinstance(
        worksheet.producer_of(ADJUSTED_GROSS_CAPITAL_LOSSES_1988_AND_1989), ApplyFraction
    )
    assert isinstance(
        worksheet.producer_of(ADJUSTED_GROSS_CAPITAL_LOSSES_1990_TO_1999), ApplyFraction
    )
    assert isinstance(
        worksheet.producer_of(ADJUSTED_GROSS_CAPITAL_LOSSES_2001_TO_2024), ApplyFraction
    )
    assert isinstance(worksheet.producer_of(TOTAL_ADJUSTED_NET_CAPITAL_LOSSES), Sum)
    assert isinstance(worksheet.producer_of(NET_CAPITAL_LOSSES_AVAILABLE_TO_CLAIM), LesserOf)
    assert isinstance(worksheet.producer_of(NET_CAPITAL_LOSSES_OF_OTHER_YEARS), AtMost)
    assert isinstance(worksheet.producer_of(ADJUSTED_LOSSES_APPLIED_1985_TO_1987), LesserOf)
    assert isinstance(worksheet.producer_of(ADJUSTED_LOSSES_LEFT_AFTER_1985_TO_1987), Subtract)
    assert isinstance(worksheet.producer_of(REMAINING_ADJUSTED_LOSSES_1985_TO_1987), Subtract)
    assert isinstance(worksheet.producer_of(NET_CAPITAL_LOSS_BALANCE_1985_TO_1987), ApplyFraction)
    assert isinstance(worksheet.producer_of(ADJUSTED_LOSSES_APPLIED_1988_AND_1989), LesserOf)
    assert isinstance(worksheet.producer_of(ADJUSTED_LOSSES_LEFT_AFTER_1988_AND_1989), Subtract)
    assert isinstance(worksheet.producer_of(REMAINING_ADJUSTED_LOSSES_1988_AND_1989), Subtract)
    assert isinstance(worksheet.producer_of(NET_CAPITAL_LOSS_BALANCE_1988_AND_1989), ApplyFraction)
    assert isinstance(worksheet.producer_of(ADJUSTED_LOSSES_APPLIED_1990_TO_1999), LesserOf)
    assert isinstance(worksheet.producer_of(ADJUSTED_LOSSES_LEFT_AFTER_1990_TO_1999), Subtract)
    assert isinstance(worksheet.producer_of(REMAINING_ADJUSTED_LOSSES_1990_TO_1999), Subtract)
    assert isinstance(worksheet.producer_of(NET_CAPITAL_LOSS_BALANCE_1990_TO_1999), ApplyFraction)
    assert isinstance(worksheet.producer_of(ADJUSTED_LOSSES_APPLIED_2001_TO_2024), LesserOf)
    assert isinstance(worksheet.producer_of(REMAINING_ADJUSTED_LOSSES_2001_TO_2024), Subtract)
    assert isinstance(worksheet.producer_of(NET_CAPITAL_LOSS_BALANCE_2001_TO_2024), ApplyFraction)
    assert worksheet.producer_of(NET_CAPITAL_LOSSES_OF_OTHER_YEARS) is not worksheet.producer_of(
        NET_CAPITAL_LOSSES_AVAILABLE_TO_CLAIM
    )
    assert isinstance(worksheet.producer_of(TAXABLE_INCOME), SubtractNotBelowZero)
    assert worksheet.producer_of(TAXABLE_INCOME) is not worksheet.producer_of(NET_INCOME)
    assert worksheet.producer_of(DEDUCTIONS_FROM_NET_INCOME) is not worksheet.producer_of(
        TOTAL_INCOME
    )
    assert worksheet.producer_of(DEDUCTIONS_FROM_NET_INCOME) is not worksheet.producer_of(
        DEDUCTIONS_FROM_TOTAL_INCOME
    )
    assert isinstance(worksheet.producer_of(FEDERAL_BASIC_TAX), ProgressiveTax)
    assert isinstance(worksheet.producer_of(ONTARIO_BASIC_TAX), ProgressiveTax)
    assert worksheet.producer_of(FEDERAL_BASIC_TAX) is not worksheet.producer_of(ONTARIO_BASIC_TAX)
    assert isinstance(worksheet.producer_of(BASIC_PERSONAL_AMOUNT), TaperedAmount)
    assert isinstance(worksheet.producer_of(ontario.BASIC_PERSONAL_AMOUNT), CreditAmount)
    assert worksheet.producer_of(BASIC_PERSONAL_AMOUNT) is not worksheet.producer_of(
        ontario.BASIC_PERSONAL_AMOUNT
    )
    assert isinstance(worksheet.producer_of(CANADA_EMPLOYMENT_AMOUNT), CappedAmount)
    assert isinstance(
        worksheet.producer_of(ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT), SubtractNotBelowZero
    )
    assert isinstance(worksheet.producer_of(ELIGIBLE_DEPENDANT_AMOUNT), TimesCount)
    assert isinstance(worksheet.producer_of(AGE_MAXIMUM), CreditAmount)
    assert isinstance(worksheet.producer_of(AGE_INCOME_THRESHOLD), CreditAmount)
    assert isinstance(worksheet.producer_of(AGE_INCOME_OVER_THRESHOLD), SubtractNotBelowZero)
    assert isinstance(worksheet.producer_of(AGE_REDUCTION), ApplyRate)
    assert isinstance(worksheet.producer_of(AGE_AMOUNT_BEFORE_COUNT), SubtractNotBelowZero)
    assert isinstance(worksheet.producer_of(AGE_AMOUNT), TimesCount)
    assert isinstance(worksheet.producer_of(SPOUSE_INFIRMITY_SUPPLEMENT), PerUnitAmount)
    assert isinstance(worksheet.producer_of(SPOUSE_AMOUNT_BASIS), Sum)
    assert isinstance(worksheet.producer_of(SPOUSE_AMOUNT_BEFORE_COUNT), SubtractNotBelowZero)
    assert isinstance(worksheet.producer_of(SPOUSE_AMOUNT), TimesCount)
    assert isinstance(worksheet.producer_of(SPOUSE_CAREGIVER_BASE), CreditAmount)
    assert isinstance(worksheet.producer_of(SPOUSE_CAREGIVER_BEFORE_MAXIMUM), SubtractNotBelowZero)
    assert isinstance(worksheet.producer_of(SPOUSE_CAREGIVER_LIMIT), CappedAmount)
    assert isinstance(
        worksheet.producer_of(SPOUSE_CAREGIVER_AMOUNT_BEFORE_COUNT), SubtractNotBelowZero
    )
    assert isinstance(worksheet.producer_of(SPOUSE_CAREGIVER_AMOUNT), TimesCount)
    assert worksheet.producer_of(AGE_AMOUNT) is not worksheet.producer_of(SPOUSE_AMOUNT)
    assert worksheet.producer_of(SPOUSE_AMOUNT) is not worksheet.producer_of(
        SPOUSE_CAREGIVER_AMOUNT
    )
    assert worksheet.producer_of(SPOUSE_AMOUNT) is not worksheet.producer_of(
        ELIGIBLE_DEPENDANT_AMOUNT
    )
    assert worksheet.producer_of(AGE_MAXIMUM) is not worksheet.producer_of(SPOUSE_CAREGIVER_BASE)
    assert worksheet.producer_of(SPOUSE_INFIRMITY_SUPPLEMENT) is not (
        worksheet.producer_of(INFIRM_CHILDREN_AMOUNT)
    )
    assert isinstance(worksheet.producer_of(INFIRM_CHILDREN_AMOUNT), PerUnitAmount)
    assert isinstance(worksheet.producer_of(CAREGIVER_AMOUNT), CaregiverAmount)
    assert isinstance(worksheet.producer_of(MEDICAL_NET_INCOME_SHARE), ApplyRate)
    assert isinstance(worksheet.producer_of(MEDICAL_THRESHOLD), CappedAmount)
    assert isinstance(worksheet.producer_of(MEDICAL_EXPENSES_OVER_THRESHOLD), SubtractNotBelowZero)
    assert isinstance(worksheet.producer_of(OTHER_DEPENDANTS_MEDICAL), OtherDependantsMedical)
    assert isinstance(worksheet.producer_of(MEDICAL_CLAIM), Sum)
    assert isinstance(
        worksheet.producer_of(DISABILITY_TRANSFERRED_AMOUNT), DisabilityTransferAmount
    )
    assert worksheet.producer_of(INFIRM_CHILDREN_AMOUNT) is not worksheet.producer_of(
        TAX_REDUCTION_FOR_CHILDREN
    )
    assert isinstance(worksheet.producer_of(ELIGIBLE_DEPENDANT_BASE), CreditAmount)
    assert worksheet.producer_of(ELIGIBLE_DEPENDANT_BASE) is not worksheet.producer_of(
        ontario.BASIC_PERSONAL_AMOUNT
    )
    assert isinstance(
        worksheet.producer_of(ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_MAXIMUM), SubtractNotBelowZero
    )
    assert worksheet.producer_of(ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_MAXIMUM) is not (
        worksheet.producer_of(ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT)
    )
    assert isinstance(
        worksheet.producer_of(ontario.ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT), CappedAmount
    )
    assert isinstance(worksheet.producer_of(ontario.ELIGIBLE_DEPENDANT_AMOUNT), TimesCount)
    assert worksheet.producer_of(ontario.ELIGIBLE_DEPENDANT_AMOUNT) is not (
        worksheet.producer_of(ELIGIBLE_DEPENDANT_AMOUNT)
    )
    assert isinstance(worksheet.producer_of(ontario.CAREGIVER_AMOUNT), OntarioCaregiverAmount)
    assert worksheet.producer_of(ontario.CAREGIVER_AMOUNT) is not (
        worksheet.producer_of(CAREGIVER_AMOUNT)
    )
    assert isinstance(worksheet.producer_of(ontario.AGE_MAXIMUM), CreditAmount)
    assert isinstance(worksheet.producer_of(ontario.AGE_INCOME_THRESHOLD), CreditAmount)
    assert isinstance(
        worksheet.producer_of(ontario.AGE_INCOME_OVER_THRESHOLD), SubtractNotBelowZero
    )
    assert isinstance(worksheet.producer_of(ontario.AGE_REDUCTION), ApplyRate)
    assert isinstance(worksheet.producer_of(ontario.AGE_AMOUNT_BEFORE_COUNT), SubtractNotBelowZero)
    assert isinstance(worksheet.producer_of(ontario.AGE_AMOUNT), TimesCount)
    assert worksheet.producer_of(ontario.AGE_AMOUNT) is not worksheet.producer_of(AGE_AMOUNT)
    assert isinstance(worksheet.producer_of(ontario.SPOUSE_BASE), CreditAmount)
    assert isinstance(
        worksheet.producer_of(ontario.SPOUSE_AMOUNT_BEFORE_MAXIMUM), SubtractNotBelowZero
    )
    assert isinstance(worksheet.producer_of(ontario.SPOUSE_AMOUNT_BEFORE_COUNT), CappedAmount)
    assert isinstance(worksheet.producer_of(ontario.SPOUSE_AMOUNT), TimesCount)
    assert worksheet.producer_of(ontario.SPOUSE_AMOUNT) is not worksheet.producer_of(SPOUSE_AMOUNT)
    assert isinstance(worksheet.producer_of(NON_REFUNDABLE_CREDIT_AMOUNTS), Sum)
    assert isinstance(worksheet.producer_of(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS), Sum)
    assert worksheet.producer_of(NON_REFUNDABLE_CREDIT_AMOUNTS) is not worksheet.producer_of(
        ontario.NON_REFUNDABLE_CREDIT_AMOUNTS
    )
    assert isinstance(worksheet.producer_of(CREDIT_AMOUNTS_AT_CREDIT_RATE), ApplyRate)
    assert isinstance(worksheet.producer_of(NON_REFUNDABLE_TAX_CREDITS), Sum)
    assert isinstance(worksheet.producer_of(ontario.CREDIT_AMOUNTS_AT_CREDIT_RATE), ApplyRate)
    assert isinstance(worksheet.producer_of(ontario.DONATIONS_FIRST_TIER_CREDIT), ApplyRate)
    assert isinstance(worksheet.producer_of(ontario.DONATIONS_OVER_FIRST_TIER_CREDIT), ApplyRate)
    assert isinstance(worksheet.producer_of(ontario.DONATIONS_AND_GIFTS_CREDIT), Sum)
    assert isinstance(worksheet.producer_of(ontario.NON_REFUNDABLE_TAX_CREDITS), Sum)
    assert worksheet.producer_of(ontario.CREDIT_AMOUNTS_AT_CREDIT_RATE) is not (
        worksheet.producer_of(CREDIT_AMOUNTS_AT_CREDIT_RATE)
    )
    assert worksheet.producer_of(ontario.DONATIONS_AND_GIFTS_CREDIT) is not (
        worksheet.producer_of(DONATIONS_AND_GIFTS_CREDIT)
    )
    assert worksheet.producer_of(ontario.DONATIONS_FIRST_TIER_CREDIT) is not (
        worksheet.producer_of(ontario.DONATIONS_OVER_FIRST_TIER_CREDIT)
    )
    assert worksheet.producer_of(CREDIT_AMOUNTS_AT_CREDIT_RATE) is not worksheet.producer_of(
        ontario.NON_REFUNDABLE_TAX_CREDITS
    )
    assert worksheet.producer_of(CREDIT_AMOUNTS_AT_CREDIT_RATE) is not worksheet.producer_of(
        NON_REFUNDABLE_TAX_CREDITS
    )
    assert worksheet.producer_of(NON_REFUNDABLE_TAX_CREDITS) is not worksheet.producer_of(
        ontario.NON_REFUNDABLE_TAX_CREDITS
    )
    assert worksheet.producer_of(NON_REFUNDABLE_TAX_CREDITS) is not worksheet.producer_of(
        TAXABLE_CAPITAL_GAINS
    )
    assert isinstance(worksheet.producer_of(FEDERAL_TAX_AFTER_CREDITS), SubtractNotBelowZero)
    assert isinstance(worksheet.producer_of(DEPRECIABLE_GIFT_PROCEEDS_OR_COST), LesserOf)
    assert isinstance(worksheet.producer_of(DEPRECIABLE_GIFTS), LesserOf)
    assert isinstance(worksheet.producer_of(CAPITAL_PROPERTY_GIFTS), Subtract)
    assert isinstance(worksheet.producer_of(TOTAL_CHARITABLE_DONATIONS), Sum)
    assert isinstance(worksheet.producer_of(DONATION_LIMIT_ON_NET_INCOME), ApplyRate)
    assert isinstance(worksheet.producer_of(CAPITAL_GIFTS_TOTAL), Sum)
    assert isinstance(worksheet.producer_of(CAPITAL_GIFTS_LIMIT_ADDITION), ApplyRate)
    assert isinstance(worksheet.producer_of(DONATION_LIMIT_WITH_CAPITAL_GIFTS), Sum)
    assert isinstance(worksheet.producer_of(CHARITABLE_DONATIONS_LIMIT), LesserOf)
    assert isinstance(worksheet.producer_of(CHARITABLE_DONATIONS_CLAIMED), LesserOf)
    assert isinstance(worksheet.producer_of(DONATIONS_AND_GIFTS_TOTAL), Sum)
    assert isinstance(worksheet.producer_of(DONATION_FIRST_TIER_MAXIMUM), CreditAmount)
    assert isinstance(worksheet.producer_of(DONATIONS_FIRST_TIER), LesserOf)
    assert isinstance(worksheet.producer_of(DONATIONS_OVER_FIRST_TIER), Subtract)
    assert isinstance(
        worksheet.producer_of(DONATIONS_OVER_FIRST_TIER_AFTER_2016_GIFTS), SubtractNotBelowZero
    )
    assert isinstance(worksheet.producer_of(DONATION_HIGH_INCOME_THRESHOLD), CreditAmount)
    assert isinstance(
        worksheet.producer_of(TAXABLE_INCOME_OVER_DONATION_THRESHOLD), SubtractNotBelowZero
    )
    assert isinstance(worksheet.producer_of(HIGH_INCOME_DONATIONS), LesserOf)
    assert isinstance(worksheet.producer_of(HIGH_INCOME_DONATION_CREDIT), ApplyRate)
    assert isinstance(worksheet.producer_of(REGULAR_RATE_DONATIONS), Subtract)
    assert isinstance(worksheet.producer_of(REGULAR_RATE_DONATION_CREDIT), ApplyRate)
    assert isinstance(worksheet.producer_of(FIRST_TIER_DONATION_CREDIT), ApplyRate)
    assert isinstance(worksheet.producer_of(DONATIONS_AND_GIFTS_CREDIT), Sum)
    assert isinstance(worksheet.producer_of(TOP_UP_CREDITS_BASE), Sum)
    assert isinstance(worksheet.producer_of(TOP_UP_THRESHOLD), CreditAmount)
    assert isinstance(worksheet.producer_of(TOP_UP_EXCESS), SubtractNotBelowZero)
    assert isinstance(worksheet.producer_of(TOP_UP_TAX_CREDIT), ApplyRate)
    schedule_9 = (
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
        TOP_UP_CREDITS_BASE,
        TOP_UP_THRESHOLD,
        TOP_UP_EXCESS,
        TOP_UP_TAX_CREDIT,
    )
    assert len({id(worksheet.producer_of(kind)) for kind in schedule_9}) == len(schedule_9)
    assert isinstance(worksheet.producer_of(ONTARIO_TAX_AFTER_CREDITS), SubtractNotBelowZero)
    assert worksheet.producer_of(FEDERAL_TAX_AFTER_CREDITS) is not worksheet.producer_of(
        ONTARIO_TAX_AFTER_CREDITS
    )
    assert isinstance(worksheet.producer_of(ONTARIO_SURTAX), TieredSurcharge)
    assert isinstance(worksheet.producer_of(ONTARIO_TAX_WITH_SURTAX), Sum)
    assert worksheet.producer_of(ONTARIO_TAX_WITH_SURTAX) is not worksheet.producer_of(TOTAL_INCOME)
    for kind in (
        ontario.DIVIDENDS_AMOUNT_A,
        ontario.DIVIDENDS_AMOUNT_B,
        ontario.DIVIDEND_TAX_CREDIT,
        ontario.ONTARIO_TAX_BEFORE_DIVIDEND_CREDIT,
        ontario.DIVIDEND_CREDIT_FROM_LINE_57,
    ):
        assert isinstance(worksheet.producer_of(kind), Sum), kind
    assert isinstance(worksheet.producer_of(ontario.OTHER_DIVIDENDS_CREDIT), ApplyRate)
    assert isinstance(worksheet.producer_of(ontario.ELIGIBLE_DIVIDENDS_CREDIT), ApplyRate)
    assert isinstance(worksheet.producer_of(ontario.DIVIDENDS_AMOUNT_A_LESS_B), Subtract)
    assert isinstance(
        worksheet.producer_of(ontario.ONTARIO_TAX_LESS_DIVIDEND_CREDIT), SubtractNotBelowZero
    )
    assert isinstance(
        worksheet.producer_of(ontario.ONTARIO_TAX_AFTER_DIVIDEND_CREDIT), SubtractNotBelowZero
    )
    assert worksheet.producer_of(ontario.DIVIDENDS_AMOUNT_A) is not (
        worksheet.producer_of(DIVIDENDS_AMOUNT_A)
    )
    assert worksheet.producer_of(ontario.OTHER_DIVIDENDS_CREDIT) is not (
        worksheet.producer_of(OTHER_DIVIDENDS_CREDIT)
    )
    assert worksheet.producer_of(ontario.ELIGIBLE_DIVIDENDS_CREDIT) is not (
        worksheet.producer_of(ELIGIBLE_DIVIDENDS_CREDIT)
    )
    assert worksheet.producer_of(ontario.DIVIDENDS_AMOUNT_A_LESS_B) is not (
        worksheet.producer_of(DIVIDENDS_AMOUNT_A_LESS_B)
    )
    assert worksheet.producer_of(ontario.DIVIDEND_TAX_CREDIT) is not (
        worksheet.producer_of(DIVIDEND_TAX_CREDIT)
    )
    assert worksheet.producer_of(ontario.ONTARIO_TAX_AFTER_DIVIDEND_CREDIT) is not (
        worksheet.producer_of(ONTARIO_TAX_WITH_SURTAX)
    )
    assert isinstance(worksheet.producer_of(TAX_REDUCTION_BASIC), CreditAmount)
    assert worksheet.producer_of(TAX_REDUCTION_BASIC) is not worksheet.producer_of(
        ontario.BASIC_PERSONAL_AMOUNT
    )
    assert isinstance(worksheet.producer_of(TAX_REDUCTION_FOR_CHILDREN), PerUnitAmount)
    assert isinstance(worksheet.producer_of(TAX_REDUCTION_FOR_DEPENDANTS), PerUnitAmount)
    assert worksheet.producer_of(TAX_REDUCTION_FOR_CHILDREN) is not worksheet.producer_of(
        TAX_REDUCTION_FOR_DEPENDANTS
    )
    assert isinstance(worksheet.producer_of(TAX_REDUCTION_AMOUNTS), Sum)
    assert isinstance(worksheet.producer_of(ONTARIO_TAX_REDUCTION), MultipleOver)
    assert isinstance(worksheet.producer_of(ONTARIO_TAX_AFTER_REDUCTION), SubtractNotBelowZero)
    assert worksheet.producer_of(ONTARIO_TAX_AFTER_REDUCTION) is not worksheet.producer_of(
        ONTARIO_TAX_AFTER_CREDITS
    )
    assert isinstance(worksheet.producer_of(LIFT_CREDIT_BEFORE_MAXIMUM), ApplyRate)
    assert worksheet.producer_of(LIFT_CREDIT_BEFORE_MAXIMUM) is not worksheet.producer_of(
        TAXABLE_CAPITAL_GAINS
    )
    assert isinstance(worksheet.producer_of(LIFT_MAXIMUM_CREDIT), CappedAmount)
    assert worksheet.producer_of(LIFT_MAXIMUM_CREDIT) is not worksheet.producer_of(
        CANADA_EMPLOYMENT_AMOUNT
    )
    assert isinstance(worksheet.producer_of(LIFT_REDUCTION), TieredSurcharge)
    assert worksheet.producer_of(LIFT_REDUCTION) is not worksheet.producer_of(ONTARIO_SURTAX)
    assert isinstance(worksheet.producer_of(LIFT_CREDIT), ChooseByCount)
    assert isinstance(worksheet.producer_of(ontario.LIFT_CREDIT_SINGLE), SubtractNotBelowZero)
    assert isinstance(worksheet.producer_of(ontario.LIFT_CREDIT_WITH_SPOUSE), SubtractNotBelowZero)
    assert worksheet.producer_of(ontario.LIFT_CREDIT_SINGLE) is not worksheet.producer_of(
        ontario.LIFT_CREDIT_WITH_SPOUSE
    )
    for kind in (
        ontario.LIFT_NET_INCOME_AND_REPAYMENTS,
        ontario.LIFT_UCCB_AND_RDSP_INCOME,
        ontario.LIFT_SPOUSE_NET_INCOME_AND_REPAYMENTS,
        ontario.LIFT_SPOUSE_UCCB_AND_RDSP_INCOME,
        ontario.LIFT_FAMILY_NET_INCOME,
    ):
        assert isinstance(worksheet.producer_of(kind), Sum), kind.identifier
    for kind in (
        ontario.LIFT_ADJUSTED_NET_INCOME,
        ontario.LIFT_SPOUSE_ADJUSTED_NET_INCOME,
        ontario.LIFT_EXCESS_OVER_INDIVIDUAL_THRESHOLD,
        ontario.LIFT_EXCESS_OVER_FAMILY_THRESHOLD,
    ):
        assert isinstance(worksheet.producer_of(kind), SubtractNotBelowZero), kind.identifier
    assert isinstance(worksheet.producer_of(ontario.LIFT_INDIVIDUAL_INCOME_THRESHOLD), CreditAmount)
    assert isinstance(worksheet.producer_of(ontario.LIFT_FAMILY_INCOME_THRESHOLD), CreditAmount)
    assert isinstance(worksheet.producer_of(ontario.LIFT_GREATER_EXCESS), GreaterOf)
    assert isinstance(worksheet.producer_of(ontario.LIFT_FAMILY_REDUCTION), ApplyRate)
    assert isinstance(worksheet.producer_of(ONTARIO_TAX_AFTER_LIFT_CREDIT), SubtractNotBelowZero)
    assert worksheet.producer_of(LIFT_CREDIT) is not worksheet.producer_of(
        ONTARIO_TAX_AFTER_LIFT_CREDIT
    )
    assert worksheet.producer_of(ONTARIO_TAX_AFTER_LIFT_CREDIT) is not worksheet.producer_of(
        ONTARIO_TAX_AFTER_REDUCTION
    )
    assert isinstance(worksheet.producer_of(COMMUNITY_FOOD_PROGRAM_CREDIT), ApplyRate)
    assert worksheet.producer_of(COMMUNITY_FOOD_PROGRAM_CREDIT) is not worksheet.producer_of(
        LIFT_CREDIT_BEFORE_MAXIMUM
    )
    assert isinstance(worksheet.producer_of(ONTARIO_TAX_AFTER_FOOD_CREDIT), SubtractNotBelowZero)
    assert worksheet.producer_of(ONTARIO_TAX_AFTER_FOOD_CREDIT) is not worksheet.producer_of(
        ONTARIO_TAX_AFTER_LIFT_CREDIT
    )
    assert isinstance(worksheet.producer_of(ONTARIO_HEALTH_PREMIUM), TieredSurcharge)
    assert worksheet.producer_of(ONTARIO_HEALTH_PREMIUM) is not worksheet.producer_of(
        ONTARIO_SURTAX
    )
    assert worksheet.producer_of(ONTARIO_HEALTH_PREMIUM) is not worksheet.producer_of(
        LIFT_REDUCTION
    )
    assert isinstance(worksheet.producer_of(ONTARIO_TAX), Sum)
    assert worksheet.producer_of(ONTARIO_TAX) is not worksheet.producer_of(ONTARIO_TAX_WITH_SURTAX)
    assert isinstance(worksheet.producer_of(NET_FEDERAL_TAX), Sum)
    assert isinstance(worksheet.producer_of(TOTAL_PAYABLE), Sum)
    assert isinstance(worksheet.producer_of(WORKING_INCOME), Sum)
    assert isinstance(worksheet.producer_of(ADJUSTED_FAMILY_NET_INCOME), Sum)
    assert worksheet.producer_of(WORKING_INCOME) is not worksheet.producer_of(
        ADJUSTED_FAMILY_NET_INCOME
    )
    assert worksheet.producer_of(WORKING_INCOME) is not worksheet.producer_of(TOTAL_INCOME)
    cwb_lines = (
        CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT,
        CWB_BEFORE_REDUCTION_WITH_DEPENDANT,
        CWB_REDUCTION_WITHOUT_DEPENDANT,
        CWB_REDUCTION_WITH_DEPENDANT,
    )
    for kind in cwb_lines:
        assert isinstance(worksheet.producer_of(kind), TieredSurcharge)
    assert len({id(worksheet.producer_of(kind)) for kind in cwb_lines}) == 4
    assert worksheet.producer_of(CWB_REDUCTION_WITHOUT_DEPENDANT) is not worksheet.producer_of(
        LIFT_REDUCTION
    )
    for kind in (CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT, CANADA_WORKERS_BENEFIT_WITH_DEPENDANT):
        assert isinstance(worksheet.producer_of(kind), SubtractNotBelowZero)
        assert worksheet.producer_of(kind) is not worksheet.producer_of(LIFT_CREDIT)
    assert worksheet.producer_of(
        CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT
    ) is not worksheet.producer_of(CANADA_WORKERS_BENEFIT_WITH_DEPENDANT)
    assert isinstance(worksheet.producer_of(CANADA_WORKERS_BENEFIT), ChooseByCount)
    assert isinstance(worksheet.producer_of(FERTILITY_CREDIT_BEFORE_MAXIMUM), ApplyRate)
    assert isinstance(worksheet.producer_of(FERTILITY_CREDIT), CappedAmount)
    assert isinstance(
        worksheet.producer_of(SENIORS_TRANSIT_AMOUNT_PAID_AT_MOST_MAXIMUM), CappedAmount
    )
    assert isinstance(worksheet.producer_of(SENIORS_TRANSIT_CREDIT), ApplyRate)
    assert worksheet.producer_of(FERTILITY_CREDIT_BEFORE_MAXIMUM) is not worksheet.producer_of(
        SENIORS_TRANSIT_CREDIT
    )
    assert worksheet.producer_of(FERTILITY_CREDIT) is not worksheet.producer_of(
        SENIORS_TRANSIT_AMOUNT_PAID_AT_MOST_MAXIMUM
    )
