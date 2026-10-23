"""CA-ON 2025 end to end, Return A: return a structured trace 3."""

from __future__ import annotations

from fractions import Fraction as ExactFraction

from app.domain.parameters.amount import Amount
from app.domain.parameters.credit import Credit
from app.domain.parameters.factor import Factor
from app.domain.parameters.fraction import Fraction
from app.domain.parameters.rate import Rate
from app.domain.parameters.rounding import NO_ROUNDING
from app.domain.parameters.taper import Taper
from app.domain.trace import (
    CappedAmountLine,
    CreditAmountLine,
    DividedByRateLine,
    FractionAppliedLine,
    MultipleOverLine,
    PerUnitAmountLine,
    SignChosenDifferenceLine,
    SubtractedLine,
    TaperedAmountLine,
    ThresholdGateLine,
    TimesCountLine,
)
from app.jurisdictions.ca.catalog import (
    ADJUSTED_GROSS_CAPITAL_LOSSES_1985_TO_1987,
    ADJUSTED_GROSS_CAPITAL_LOSSES_1988_AND_1989,
    ADJUSTED_GROSS_CAPITAL_LOSSES_1990_TO_1999,
    ADJUSTED_GROSS_CAPITAL_LOSSES_2000,
    ADJUSTED_GROSS_CAPITAL_LOSSES_2001_TO_2024,
    ADJUSTED_GROSS_CAPITAL_LOSSES_BEFORE_MAY_23_1985,
    ADJUSTED_LOSSES_APPLIED_1985_TO_1987,
    ADJUSTED_LOSSES_APPLIED_1988_AND_1989,
    ADJUSTED_LOSSES_APPLIED_1990_TO_1999,
    ADJUSTED_LOSSES_APPLIED_2000,
    ADJUSTED_LOSSES_APPLIED_2001_TO_2024,
    ADJUSTED_LOSSES_APPLIED_BEFORE_MAY_23_1985,
    ADJUSTED_LOSSES_LEFT_AFTER_1985_TO_1987,
    ADJUSTED_LOSSES_LEFT_AFTER_1988_AND_1989,
    ADJUSTED_LOSSES_LEFT_AFTER_1990_TO_1999,
    ADJUSTED_LOSSES_LEFT_AFTER_2000,
    ADJUSTED_LOSSES_LEFT_AFTER_BEFORE_MAY_23_1985,
    ADJUSTED_NET_CAPITAL_LOSSES_APPLIED,
    AGE_AMOUNT,
    AGE_AMOUNT_BEFORE_COUNT,
    AGE_INCOME_THRESHOLD,
    AGE_MAXIMUM,
    AGED_18_OR_OLDER_AT_END_OF_2025,
    AMOUNTS_TRANSFERRED_FROM_SPOUSE,
    AMT_AMOUNT_A_MINUS_AMOUNT_B,
    AMT_BASIC_EXEMPTION,
    AMT_BASIC_FEDERAL_TAX,
    AMT_CAPITAL_GAINS_ADDED,
    AMT_CAPITAL_GAINS_ADJUSTMENTS,
    AMT_CAPITAL_GAINS_DIFFERENCE,
    AMT_CARRYOVER_AVAILABLE_FOR_2026,
    AMT_CARRYOVER_BALANCE,
    AMT_CARRYOVER_BALANCE_WITH_ADDITIONAL_TAXES,
    AMT_CREDITS_TOTAL,
    AMT_FEDERAL_SURTAX_AT_48_PERCENT,
    AMT_FEDERAL_SURTAX_IF_NON_RESIDENT,
    AMT_LIMITED_PARTNERSHIP_DIFFERENCE_APPLIED,
    AMT_LIMITED_PARTNERSHIP_LOSSES_ADJUSTMENT,
    AMT_MINIMUM_TAX_CARRYOVER_APPLIED,
    AMT_MINIMUM_TAX_CARRYOVER_FROM_PREVIOUS_YEARS,
    AMT_NET_CAPITAL_GAINS_AFTER_ADJUSTMENTS,
    AMT_NON_CAPITAL_LOSSES_ADJUSTMENT,
    AMT_NON_CAPITAL_LOSSES_DIFFERENCE,
    AMT_NON_DEDUCTIBLE_OFFICE_EXPENSES,
    AMT_NON_RESIDENT_OR_DEEMED_RESIDENT,
    AMT_OFFICE_EXPENSES_ADJUSTMENT,
    AMT_PART_6_SURTAX_AT_48_PERCENT,
    AMT_PART_6_SURTAX_IF_NON_RESIDENT,
    AMT_PART_7_BASIC_TAX_WITH_RECAPTURE,
    AMT_PART_7_CREDITS_TOTAL,
    AMT_PART_7_TAX_LESS_CREDITS,
    AMT_PUBLICLY_LISTED_GIFTS_NET,
    AMT_PUBLICLY_LISTED_GIFTS_T1170_LINE_68231,
    AMT_PUBLICLY_LISTED_GIFTS_TOTAL,
    AMT_QBT_CAPITAL_GAINS_DEDUCTION_DIFFERENCE,
    AMT_QBT_CAPITAL_GAINS_DEDUCTION_DOUBLED,
    AMT_SPLIT_INCOME_AND_CREDITS_TOTAL,
    AMT_TAX_PAYABLE_AFTER_CREDITS,
    AMT_TAX_PAYABLE_BEFORE_MINIMUM_TAX_CARRYOVER,
    AMT_TAX_PAYABLE_WITH_ITC_RECAPTURE,
    AMT_UNAPPLIED_2018_CARRYOVER,
    ANNUAL_GAINS_LINE_3,
    ANNUAL_GAINS_LINE_3_AT_INCLUSION_RATE,
    ANNUAL_GAINS_LINE_5,
    ANNUAL_GAINS_LINE_7,
    ANNUAL_GAINS_LINE_9,
    ANNUAL_GAINS_LINE_10,
    ANNUAL_GAINS_LINE_12,
    BASIC_FEDERAL_TAX_WITH_DIVIDEND_CREDIT,
    BASIC_PERSONAL_AMOUNT,
    BORN_IN_1960_OR_EARLIER,
    BUSINESS_CCA_CLAIM,
    BUSINESS_CCA_CLAIM_LESS_PERSONAL_PART,
    BUSINESS_CCA_PERSONAL_PART,
    BUSINESS_CCA_TABLE_CLAIM,
    BUSINESS_CLOSING_INVENTORY,
    BUSINESS_COST_OF_GOODS_SOLD,
    BUSINESS_COST_OF_GOODS_SUBTOTAL,
    BUSINESS_GROSS_INCOME_BEFORE_EXPENSES,
    BUSINESS_GROSS_INCOME_FOR_GROSS_PROFIT,
    BUSINESS_GROSS_PROFIT,
    BUSINESS_GROSS_SALES,
    BUSINESS_HOME_CCA,
    BUSINESS_HOME_EXPENSES,
    BUSINESS_HOME_EXPENSES_BUSINESS_PART,
    BUSINESS_HOME_EXPENSES_SUBTOTAL,
    BUSINESS_HOME_PERSONAL_USE_PART,
    BUSINESS_INCOME,
    BUSINESS_INVESTMENT_LOSS,
    BUSINESS_INVESTMENT_LOSS_AFTER_REDUCTION,
    BUSINESS_INVESTMENT_LOSS_REDUCTION,
    BUSINESS_INVESTMENT_LOSS_REDUCTION_AVAILABLE,
    BUSINESS_NET_INCOME_AFTER_ADJUSTMENTS,
    BUSINESS_NET_INCOME_BEFORE_ADJUSTMENTS,
    BUSINESS_PARTNER_OTHER_AMOUNTS,
    BUSINESS_PARTNERSHIP_TOTAL,
    BUSINESS_QUICK_METHOD_ASSISTANCE,
    BUSINESS_QUICK_METHOD_GST_HST,
    BUSINESS_QUICK_METHOD_REMITTED,
    BUSINESS_SALES_ADJUSTMENTS,
    BUSINESS_SALES_SUBTOTAL,
    BUSINESS_TOTAL_EXPENSES,
    BUSINESS_VEHICLE_DAYS_DIVISOR,
    BUSINESS_VEHICLE_INTEREST_LIMIT,
    BUSINESS_VEHICLE_LEASE_CHARGE_LIMIT,
    BUSINESS_VEHICLE_LEASE_CHARGE_PORTION,
    BUSINESS_VEHICLE_LEASE_CHARGES_NET,
    BUSINESS_VEHICLE_LEASE_COST_LIMIT,
    BUSINESS_VEHICLE_LEASE_PAYMENTS_BEFORE,
    BUSINESS_VEHICLE_LIST_PRICE_LIMIT,
    CANADA_EMPLOYMENT_AMOUNT,
    CANADA_TRAINING_CREDIT,
    CANADIAN_TUITION_AVAILABLE,
    CANADIAN_TUITION_FEES,
    CAPITAL_GAIN,
    CAPITAL_GAINS_AFTER_DEFERRAL,
    CAPITAL_GAINS_BEFORE_INVESTMENT_LOSS_REDUCTION,
    CAPITAL_GAINS_BEFORE_RESERVES,
    CAPITAL_GAINS_DEDUCTIONS_CLAIMED_1985_TO_2024,
    CAPITAL_GAINS_DEFERRAL,
    CAPITAL_GAINS_OF_QUALIFIED_AND_OTHER_PROPERTIES,
    CAPITAL_GIFT_GAINS_DEDUCTION,
    CAPITAL_GIFT_TAXABLE_GAINS,
    CAPITAL_PROPERTY_GIFTS,
    CHART_2_LINE_4,
    CHART_2_LINE_8,
    CHART_2_LINE_12,
    CHART_2_LINE_14_OVER_TWICE_IR,
    CHART_2_LINE_16,
    CHART_2_NUMERATOR_ONE,
    CHART_2_TWICE_IR,
    CHART_2016_PART_1_AMOUNT_A,
    CHART_2016_PART_1_AMOUNT_F,
    CHART_2016_PART_1_AMOUNTS_D_AND_E,
    CHART_2016_PART_2_AMOUNT_A,
    CHART_2016_PART_2_AMOUNT_F,
    CHART_2017_PART_1_AMOUNT_A,
    CHART_2017_PART_1_AMOUNT_H,
    CHART_2017_PART_1_AMOUNTS_F_AND_G,
    CHART_2017_PART_2_AMOUNT_A,
    CHART_2017_PART_2_AMOUNT_F,
    CHART_2018_PART_1_AMOUNT_A,
    CHART_2018_PART_1_AMOUNT_H,
    CHART_2018_PART_1_AMOUNTS_F_AND_G,
    CHART_2018_PART_2_AMOUNT_A,
    CHART_2018_PART_2_AMOUNT_F,
    CHART_2019_PART_1_AMOUNT_A,
    CHART_2019_PART_1_AMOUNT_H,
    CHART_2019_PART_1_AMOUNTS_F_AND_G,
    CHART_2019_PART_2_AMOUNT_A,
    CHART_2019_PART_2_AMOUNT_F,
    CHART_2020_PART_1_AMOUNT_A,
    CHART_2020_PART_1_AMOUNT_H,
    CHART_2020_PART_1_AMOUNTS_F_AND_G,
    CHART_2020_PART_2_AMOUNT_A,
    CHART_2020_PART_2_AMOUNT_F,
    CHART_2021_PART_1_AMOUNT_A,
    CHART_2021_PART_1_AMOUNT_H,
    CHART_2021_PART_1_AMOUNT_I,
    CHART_2021_PART_1_AMOUNTS_F_AND_G,
    CHART_2021_PART_2_AMOUNT_A,
    CHART_2021_PART_2_AMOUNT_F,
    CHART_2021_PART_2_AMOUNT_G,
    CHART_2022_PART_1_AMOUNT_A,
    CHART_2022_PART_1_AMOUNT_H,
    CHART_2022_PART_1_AMOUNT_I,
    CHART_2022_PART_1_AMOUNTS_F_AND_G,
    CHART_2022_PART_2_AMOUNT_A,
    CHART_2022_PART_2_AMOUNT_F,
    CHART_2022_PART_2_AMOUNT_G,
    CHART_2023_PART_1_AMOUNT_A,
    CHART_2023_PART_1_AMOUNT_H,
    CHART_2023_PART_1_AMOUNT_I,
    CHART_2023_PART_1_AMOUNTS_F_AND_G,
    CHART_2023_PART_2_AMOUNT_A,
    CHART_2023_PART_2_AMOUNT_F,
    CHART_2023_PART_2_AMOUNT_G,
    CHART_2024_PERIOD_1_AMOUNT_A,
    CHART_2024_PERIOD_1_AMOUNT_I,
    CHART_2024_PERIOD_1_AMOUNTS_F_TO_H,
    CHART_2024_PERIOD_2_AMOUNT_A,
    CHART_2024_PERIOD_2_AMOUNT_I,
    CHART_2024_PERIOD_2_AMOUNTS_F_TO_H,
    CHART_2025_PART_1_AMOUNT_A,
    CHART_2025_PART_1_AMOUNT_K,
    CHART_2025_PART_1_AMOUNTS_F_TO_J,
    CHART_2025_PART_2_AMOUNT_A,
    CHART_2025_PART_2_AMOUNT_F,
    CHART_2025_PART_2_AMOUNT_G,
    CHART_2025_PART_2_AMOUNT_H,
    CHART_2025_PART_2_AMOUNT_K,
    CHART_2025_PART_2_AMOUNTS_F_TO_J,
    CHILD_CARE_EARNED_INCOME,
    CHILD_CARE_EARNED_INCOME_LIMIT,
    CHILD_CARE_LIMIT_FOR_CHILDREN_SEVEN_TO_SIXTEEN,
    CHILD_CARE_LIMIT_FOR_CHILDREN_UNDER_SEVEN,
    CHILD_CARE_LIMIT_FOR_CHILDREN_WITH_DISABILITY,
    CHILDREN_SEVEN_TO_SIXTEEN,
    CHILDREN_UNDER_SEVEN,
    CHILDREN_WITH_DISABILITY,
    CPP_ACTUAL_BASE_CONTRIBUTIONS,
    CPP_ACTUAL_FIRST_ADDITIONAL_CONTRIBUTIONS,
    CPP_BASE_CONTRIBUTIONS,
    CPP_BASE_CONTRIBUTIONS_DIFFERENCE,
    CPP_BASE_CONTRIBUTIONS_ON_SELF_EMPLOYMENT,
    CPP_DEDUCTION_ON_SELF_EMPLOYMENT,
    CPP_FIRST_ADDITIONAL_CONTRIBUTIONS,
    CPP_FIRST_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE,
    CPP_PART_3B_LINE_23_LESS_LINE_35,
    CPP_PART_3B_LINE_31,
    CPP_PART_3B_LINE_32,
    CPP_PART_3B_LINE_33,
    CPP_PART_3B_LINE_35,
    CPP_PART_3B_LINE_38,
    CPP_PART_3B_LINE_39,
    CPP_PART_3B_LINE_40,
    CPP_PART_4_COMPLETED,
    CPP_PART_5_BASE_CONTRIBUTIONS_ON_SELF_EMPLOYMENT,
    CPP_PART_5_COMPLETED,
    CPP_PART_5_DEDUCTION_ON_SELF_EMPLOYMENT,
    CPP_PART_5_LINE_4,
    CPP_PART_5_LINE_6,
    CPP_PART_5_LINE_7,
    CPP_PART_5_LINE_10,
    CPP_PART_5_LINE_12,
    CPP_PART_5_LINE_13,
    CPP_PART_5_LINE_16,
    CPP_PART_5_LINE_20,
    CPP_PART_5_LINE_23_LESS_LINE_56,
    CPP_PART_5_LINE_25,
    CPP_PART_5_LINE_30,
    CPP_PART_5_LINE_35,
    CPP_PART_5_LINE_36,
    CPP_PART_5_LINE_39,
    CPP_PART_5_LINE_41,
    CPP_PART_5_LINE_47,
    CPP_PART_5_LINE_48,
    CPP_PART_5_LINE_48_LINE_24_IF_POSITIVE,
    CPP_PART_5_LINE_49,
    CPP_PART_5_LINE_49_IF_POSITIVE,
    CPP_PART_5_LINE_52,
    CPP_PART_5_LINE_53,
    CPP_PART_5_LINE_54,
    CPP_PART_5_LINE_56,
    CPP_PART_5_LINE_59,
    CPP_PART_5_LINE_60,
    CPP_PART_5_LINE_61,
    CPP_PART_5_LINE_70,
    CPP_PART_5_LINE_71,
    CPP_PART_5_LINE_72,
    CPP_PART_5_LINE_73,
    CPP_PART_5_LINE_74,
    CPP_PART_5_LINE_75,
    CPP_PART_5_LINE_75_BASE,
    CPP_PART_5_LINE_77,
    CPP_PART_5_LINE_80,
    CPP_PART_5_LINE_83,
    CPP_PART_5_LINE_88,
    CPP_PART_5_PAYABLE_ON_SELF_EMPLOYMENT,
    CPP_PAYABLE_ON_SELF_EMPLOYMENT,
    CPP_SECOND_ADDITIONAL_CONTRIBUTIONS,
    CPP_SECOND_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE,
    CPP_SECOND_ADDITIONAL_EARNINGS_MAXIMUM,
    CPP_T4_BASE_AND_FIRST_ADDITIONAL_CONTRIBUTIONS,
    CPP_T4_SECOND_ADDITIONAL_CONTRIBUTIONS,
    CPP_ZERO,
    CURRENT_YEAR_TUITION_AVAILABLE,
    DEDUCTIONS_FROM_TOTAL_INCOME,
    DISABILITY_AMOUNT_FOR_SELF,
    DISABILITY_AMOUNT_FOR_SELF_IF_ELIGIBLE,
    DISABILITY_SELF_BASE_AMOUNT,
    DISABILITY_SELF_CARE_THRESHOLD,
    DISABILITY_SELF_SUPPLEMENT_MAXIMUM,
    DIVIDENDS_AMOUNT_A,
    DIVIDENDS_AMOUNT_A_LESS_B,
    DIVIDENDS_AMOUNT_B,
    DONATION_FIRST_TIER_MAXIMUM,
    DONATION_HIGH_INCOME_THRESHOLD,
    DONATIONS_AND_GIFTS_TOTAL,
    DONATIONS_FIRST_TIER,
    DONATIONS_OVER_FIRST_TIER,
    EDUCATOR_SUPPLIES_EXPENSES,
    EDUCATOR_SUPPLIES_EXPENSES_AT_MOST_MAXIMUM,
    EI_MAXIMUM_INSURABLE_EARNINGS,
    EI_PAYABLE_ON_SELF_EMPLOYMENT,
    EI_PREMIUMS_ON_SELF_EMPLOYMENT,
    EI_SPECIAL_BENEFITS_AGREEMENT,
    ELIGIBLE_DEPENDANT_AMOUNT,
    ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT,
    ELIGIBLE_DEPENDANTS,
    ELIGIBLE_DIVIDENDS_GROSSED_UP,
    ELIGIBLE_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP,
    ELIGIBLE_FOR_DISABILITY_AMOUNT,
    EMPLOYMENT_INCOME,
    FARM_CCA_CLAIM,
    FARM_CCA_CLAIM_LESS_PERSONAL_PART,
    FARM_CCA_PERSONAL_PART,
    FARM_CCA_TABLE_CLAIM,
    FARM_GROSS_INCOME_BEFORE_EXPENSES,
    FARM_HOME_CCA,
    FARM_HOME_EXPENSES,
    FARM_HOME_EXPENSES_BUSINESS_PART,
    FARM_HOME_EXPENSES_SUBTOTAL,
    FARM_HOME_PERSONAL_USE_PART,
    FARM_NET_INCOME_AFTER_ADJUSTMENTS,
    FARM_NET_INCOME_BEFORE_ADJUSTMENTS,
    FARM_PARTNER_OTHER_AMOUNTS,
    FARM_PARTNERSHIP_TOTAL,
    FARM_TOTAL_EXPENSES,
    FARM_VEHICLE_LEASE_CHARGE_PORTION,
    FARM_VEHICLE_LEASE_CHARGES_NET,
    FARM_VEHICLE_LEASE_PAYMENTS_BEFORE,
    FARMING_INCOME,
    FEDERAL_TAX_WITH_SPLIT_INCOME,
    FEDERAL_TUITION_AMOUNT,
    FHSA_ANNUAL_AMOUNT,
    FHSA_ANNUAL_AMOUNT_FOR_2024,
    FHSA_ANNUAL_LIMIT_AFTER_MAXIMUM_PARTICIPATION_PERIOD,
    FHSA_ANNUAL_LIMITS_LESS_DEDUCTIONS,
    FHSA_CONTRIBUTIONS_AVAILABLE,
    FHSA_CONTRIBUTIONS_IN_2024,
    FHSA_CONTRIBUTIONS_IN_2024_AFTER_FIRST_QUALIFYING_WITHDRAWAL,
    FHSA_CONTRIBUTIONS_IN_2024_BEFORE_FIRST_QUALIFYING_WITHDRAWAL,
    FHSA_CONTRIBUTIONS_IN_2025,
    FHSA_CONTRIBUTIONS_IN_2025_AFTER_FIRST_QUALIFYING_WITHDRAWAL,
    FHSA_CONTRIBUTIONS_IN_2025_BEFORE_FIRST_QUALIFYING_WITHDRAWAL,
    FHSA_DEDUCTION,
    FHSA_DEDUCTIONS_FOR_2024_AND_PRIOR_YEARS,
    FHSA_DESIGNATED_TRANSFERS_IN_2024_AND_PRIOR_YEARS,
    FHSA_EXCESS_DESIGNATED_WITHDRAWALS,
    FHSA_LIFETIME_LIMIT,
    FHSA_LIFETIME_LIMIT_LESS_DEDUCTIONS,
    FHSA_NET_RRSP_TRANSFER_AMOUNT,
    FHSA_NET_RRSP_TRANSFER_AMOUNT_FOR_2024_AND_PRIOR_YEARS,
    FHSA_NET_TRANSFER_AMOUNT_AFTER_PRIOR_YEARS,
    FHSA_RRSP_TRANSFERS_IN_2024_AND_PRIOR_YEARS,
    FHSA_TOTAL_ANNUAL_LIMITS,
    FHSA_TOTAL_DESIGNATED_TRANSFERS,
    FHSA_TOTAL_RRSP_TRANSFERS,
    FHSA_TRANSFER_AMOUNT_PLUS_VARIABLE_F_AMOUNT,
    FHSA_UNUSED_CONTRIBUTIONS_CARRIED_FORWARD,
    FHSA_UNUSED_CONTRIBUTIONS_PLUS_CONTRIBUTIONS,
    FIRST_NATIONS_ABATEMENT,
    FISH_CCA_CLAIM,
    FISH_CCA_CLAIM_LESS_PERSONAL_PART,
    FISH_CCA_PERSONAL_PART,
    FISH_CCA_TABLE_CLAIM,
    FISH_GROSS_INCOME_BEFORE_EXPENSES,
    FISH_HOME_CCA,
    FISH_HOME_EXPENSES,
    FISH_HOME_EXPENSES_BUSINESS_PART,
    FISH_HOME_EXPENSES_SUBTOTAL,
    FISH_HOME_PERSONAL_USE_PART,
    FISH_INSURANCE_RECOVERY,
    FISH_NET_INCOME_AFTER_ADJUSTMENTS,
    FISH_NET_INCOME_BEFORE_ADJUSTMENTS,
    FISH_PARTNER_OTHER_AMOUNTS,
    FISH_PARTNERSHIP_TOTAL,
    FISH_REPAIRS_TOTAL,
    FISH_REPAIRS_YOUR_COST,
    FISH_TOTAL_EXPENSES,
    FISH_VEHICLE_LEASE_CHARGE_PORTION,
    FISH_VEHICLE_LEASE_CHARGES_NET,
    FISH_VEHICLE_LEASE_PAYMENTS_BEFORE,
    FISHING_INCOME,
    FOREIGN_TAX_CREDIT_BASIC_FEDERAL_TAX,
    FOREIGN_TAX_CREDIT_NET_INCOME,
    FOREIGN_TAX_CREDIT_NET_INCOME_BEFORE_SPLIT_INCOME,
    FOREIGN_TAX_CREDIT_NET_INCOME_DEDUCTIONS,
    FOREIGN_TAX_CREDIT_NET_INCOME_WITH_SPLIT_INCOME,
    GROSS_RENTAL_INCOME,
    HIGH_INCOME_DONATIONS,
    INFIRM_CHILDREN,
    INFIRM_CHILDREN_AMOUNT,
    INTEREST_AND_OTHER_INVESTMENT_INCOME,
    INVESTMENT_INCOME_BEFORE_PRIOR_YEARS,
    INVESTMENT_INCOME_REPORTED_IN_PREVIOUS_YEARS,
    LABOUR_SPONSORED_FUNDS_CREDIT,
    LABOUR_SPONSORED_FUNDS_CREDIT_BEFORE_MAXIMUM,
    LIMITED_PARTNERSHIP_LOSSES_OF_OTHER_YEARS,
    MEDICAL_NET_INCOME_SHARE,
    MEDICAL_SUPPLEMENT_EMPLOYMENT_INCOME,
    MEDICAL_SUPPLEMENT_EMPLOYMENT_INCOME_LESS_WAGE_LOSS,
    MEDICAL_SUPPLEMENT_IF_RESIDENT,
    MEDICAL_SUPPLEMENT_IF_WORKING_INCOME_MET,
    MEDICAL_SUPPLEMENT_INCOME_THRESHOLD,
    MEDICAL_SUPPLEMENT_LINE_13,
    MEDICAL_SUPPLEMENT_LINE_14,
    MEDICAL_SUPPLEMENT_LINE_16,
    MEDICAL_SUPPLEMENT_WORKING_INCOME,
    MEDICAL_THRESHOLD,
    NET_CAPITAL_LOSS_BALANCE_1985_TO_1987,
    NET_CAPITAL_LOSS_BALANCE_1988_AND_1989,
    NET_CAPITAL_LOSS_BALANCE_1990_TO_1999,
    NET_CAPITAL_LOSS_BALANCE_2001_TO_2024,
    NET_CAPITAL_LOSS_BALANCE_BEFORE_MAY_23_1985,
    NET_CAPITAL_LOSS_NUMERATOR_ONE_2000,
    NET_CAPITAL_LOSS_TWICE_IR_2000,
    NET_CAPITAL_LOSSES_BEFORE_MAY_23_1985,
    NET_INCOME_BEFORE_ADJUSTMENTS,
    NET_INCOME_BEFORE_ADJUSTMENTS_NOT_BELOW_ZERO,
    NET_INCOME_LESS_UCCB_AND_RDSP_INCOME,
    NET_INCOME_SIGNED,
    NET_RENTAL_INCOME,
    NON_CAPITAL_LOSSES_OF_OTHER_YEARS,
    OAS_BENEFITS_BASE_AMOUNT,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_2024,
    OTHER_DIVIDENDS_GROSSED_UP,
    OTHER_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP,
    OTHER_EMPLOYMENT_EXPENSES,
    POLITICAL_CREDIT,
    POLITICAL_CREDIT_BEFORE_MAXIMUM,
    POLITICAL_CREDIT_COLUMN_1_LINE_2,
    POLITICAL_CREDIT_COLUMN_1_LINE_6,
    POLITICAL_CREDIT_COLUMN_2_LINE_2,
    POLITICAL_CREDIT_COLUMN_2_LINE_6,
    POLITICAL_CREDIT_COLUMN_3_LINE_2,
    POLITICAL_CREDIT_COLUMN_3_LINE_6,
    POLITICAL_CREDIT_SHORTCUT_AMOUNT,
    POLITICAL_CREDIT_SHORTCUT_THRESHOLD,
    PRE_1986_CAPITAL_LOSS_BALANCE,
    PRE_1986_DEDUCTIONS_1988_AND_1989,
    PRE_1986_DEDUCTIONS_1990_TO_1999,
    PRE_1986_DEDUCTIONS_ADJUSTED_1988_AND_1989,
    PRE_1986_DEDUCTIONS_ADJUSTED_1990_TO_1999,
    PRE_1986_DEDUCTIONS_TOTAL,
    QBT_ABIL_REDUCTION,
    QBT_ALLOCATION_LIMIT,
    QBT_CAPITAL_GAINS_DEDUCTION,
    QBT_CHART_A_NET_INVESTMENT_LOSS,
    QBT_DEDUCTION_AVAILABLE,
    QBT_DEDUCTION_BASE,
    QBT_ELECTION_DEDUCTION,
    QBT_ELECTION_IS_QBT,
    QBT_GAINS_ARE_QSBCS_OR_QFFP,
    QBT_HAS_INVESTMENT_EXPENSES,
    QBT_NET_INVESTMENT_LOSS,
    QBT_NET_INVESTMENT_LOSS_REDUCTION,
    QBT_NET_RENTAL_INCOME,
    QBT_NET_RENTAL_LOSS,
    QBT_REDUCTION_AMOUNT,
    QBT_TAXABLE_GAINS_RELATED_TO_DEDUCTION,
    QCC_ELECTION_DEDUCTION,
    QFFP_FORECLOSURE_GAIN_OR_LOSS,
    QFFP_GAIN_OR_LOSS,
    QSBCS_GAIN_OR_LOSS,
    QSBCS_QFFP_TAXABLE_GAINS_RELATED_TO_DEDUCTION,
    RC381_PART_3_LINE_11,
    RC381_PART_3_LINE_15,
    RC381_PART_3_LINE_16,
    RC381_PART_3_LINE_20,
    RC381_PART_3_LINE_21,
    REFUND_OR_BALANCE_OWING,
    REFUNDABLE_MEDICAL_EXPENSE_SUPPLEMENT,
    REGULAR_RATE_DONATIONS,
    REMAINING_ADJUSTED_LOSSES_1985_TO_1987,
    REMAINING_ADJUSTED_LOSSES_1988_AND_1989,
    REMAINING_ADJUSTED_LOSSES_1990_TO_1999,
    REMAINING_ADJUSTED_LOSSES_2000,
    REMAINING_ADJUSTED_LOSSES_2001_TO_2024,
    REMAINING_ADJUSTED_LOSSES_BEFORE_MAY_23_1985,
    RENTAL_CCA_BUSINESS_USE_OF_HOME,
    RENTAL_CCA_CLAIM,
    RENTAL_CCA_CLAIM_BEFORE_LIMIT,
    RENTAL_CCA_CLAIM_LESS_PERSONAL_PART,
    RENTAL_CCA_CLAIM_SHARE,
    RENTAL_CCA_PERSONAL_PART,
    RENTAL_COOWNER_OTHER_EXPENSES,
    RENTAL_DEDUCTIBLE_EXPENSES,
    RENTAL_EXPENSES_LESS_PERSONAL_PORTION,
    RENTAL_NET_INCOME_AFTER_CCA,
    RENTAL_NET_INCOME_AFTER_COOWNER_EXPENSES,
    RENTAL_NET_INCOME_AFTER_TERMINAL_LOSS,
    RENTAL_NET_INCOME_BEFORE_ADJUSTMENTS,
    RENTAL_NET_INCOME_SHARE,
    RENTAL_NET_INCOME_WITH_RECAPTURE,
    RENTAL_NON_COMPLIANT_EXPENSES,
    RENTAL_PARTNER_OTHER_EXPENSES,
    RENTAL_PARTNER_SHARE_WITH_REBATE,
    RENTAL_PARTNERSHIP_NET_INCOME,
    RENTAL_PERSONAL_PORTION,
    RENTAL_TERMINAL_LOSS,
    RENTAL_TOTAL_EXPENSES,
    RESIDENT_IN_CANADA_THROUGHOUT_2025,
    RESP_AIPS_LIFETIME_LIMIT,
    RESP_AIPS_LIMIT_REMAINING,
    RESP_AIPS_RECEIVED_PART_A,
    RESP_AIPS_REDUCTION,
    RESP_AIPS_REDUCTION_USED_IN_PREVIOUS_YEARS,
    RESP_AIPS_SUBJECT_TO_TAX,
    RRSP_CONTRIBUTIONS_AVAILABLE,
    RRSP_DEDUCTION,
    SCHEDULE_3_LINE_17600_NOT_BELOW_ZERO,
    SCHEDULE_3_LINE_19900,
    SELF_EMPLOYED_CPP_BASE_CREDIT,
    SELF_EMPLOYED_CPP_CONTRIBUTIONS_PAYABLE,
    SELF_EMPLOYED_CPP_DEDUCTION,
    SELF_EMPLOYED_EI_PREMIUMS,
    SOCIAL_BENEFITS_LINE_6,
    SOCIAL_BENEFITS_LINE_10,
    SOCIAL_BENEFITS_LINE_11,
    SOCIAL_BENEFITS_LINE_21,
    SOCIAL_BENEFITS_REPAYMENT,
    SOCIAL_BENEFITS_REPAYMENT_APPLIES,
    SPLIT_INCOME_LINE_10,
    SPLIT_INCOME_LINE_14,
    SPLIT_INCOME_LINE_15,
    SPLIT_INCOME_LINE_21,
    SPLIT_INCOME_LINE_22,
    SPOUSE_AMOUNT,
    SPOUSE_AMOUNT_BEFORE_COUNT,
    SPOUSE_CAREGIVER_AMOUNT,
    SPOUSE_CAREGIVER_AMOUNT_BEFORE_COUNT,
    SPOUSE_CAREGIVER_BASE,
    SPOUSE_CAREGIVER_BEFORE_MAXIMUM,
    SPOUSE_CAREGIVER_ELIGIBLE,
    SPOUSE_CAREGIVER_LIMIT,
    SPOUSE_INFIRMITY_SUPPLEMENT,
    SPOUSE_NOT_SEPARATED_90_DAYS,
    SPOUSE_UNUSED_AMOUNTS,
    SPOUSES_CLAIMED,
    T657_CHART_2_LINE_2,
    T657_CHART_2_LINE_6,
    T657_CHART_2_LINE_10,
    T657_CHART_2_LINE_14,
    T657_CHART_2016_AMOUNT_D,
    T657_CHART_2017_AMOUNT_F,
    T657_CHART_2018_AMOUNT_F,
    T657_CHART_2019_AMOUNT_F,
    T657_CHART_2020_AMOUNT_F,
    T657_CHART_2021_AMOUNT_F,
    T657_CHART_2021_AMOUNT_I,
    T657_CHART_2021_PART_2_AMOUNT_G,
    T657_CHART_2022_AMOUNT_F,
    T657_CHART_2022_AMOUNT_I,
    T657_CHART_2022_PART_2_AMOUNT_G,
    T657_CHART_2023_AMOUNT_F,
    T657_CHART_2023_AMOUNT_I,
    T657_CHART_2023_PART_2_AMOUNT_G,
    T657_INCLUSION_RATE_2000,
    T657_PART_2_EXCLUDED_F,
    T657_PART_2_EXCLUDED_G,
    T657_PART_2_EXCLUDED_H,
    TAXABLE_CAPITAL_GAINS,
    TAXABLE_DIVIDENDS,
    TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
    TOP_UP_THRESHOLD,
    TOSI_ADJUSTED_NET_INCOME_NOT_BELOW_ZERO,
    TOTAL_ADJUSTED_NET_CAPITAL_LOSSES,
    TOTAL_ADJUSTED_NET_CAPITAL_LOSSES_APPLIED,
    TOTAL_CREDITS,
    TOTAL_INCOME,
    TOTAL_PAYABLE,
    TOTAL_TUITION_AVAILABLE,
    TUITION_CARRIED_FORWARD,
    TUITION_INCOME_LESS_CREDITS,
    TUITION_INCOME_REMAINING,
    TUITION_TRANSFER_LIMIT,
    TUITION_TRANSFERRED,
    UCCB_AND_RDSP_INCOME,
    UNAPPLIED_ADJUSTED_NET_CAPITAL_LOSSES,
    UNAPPLIED_NET_CAPITAL_LOSSES_1985_TO_1987,
    UNAPPLIED_NET_CAPITAL_LOSSES_1988_AND_1989,
    UNAPPLIED_NET_CAPITAL_LOSSES_1990_TO_1999,
    UNAPPLIED_NET_CAPITAL_LOSSES_2001_TO_2024,
    UNUSED_FEDERAL_TUITION,
    UNUSED_RRSP_CONTRIBUTIONS_CARRIED_FORWARD,
    UNUSED_TUITION_CLAIMED,
    WAGE_LOSS_REPLACEMENT_PLAN_INCOME,
    ZONE_A_ADDITIONAL_RESIDENCY_AMOUNT,
    ZONE_A_ADDITIONAL_RESIDENCY_DAYS,
    ZONE_A_BASIC_RESIDENCY_AMOUNT,
    ZONE_A_DAYS_LIVED,
    ZONE_B_ADDITIONAL_RESIDENCY_AMOUNT,
    ZONE_B_ADDITIONAL_RESIDENCY_DAYS,
    ZONE_B_BASIC_RESIDENCY_AMOUNT,
    ZONE_B_DAYS_LIVED,
)
from app.jurisdictions.ca_on import catalog as ontario
from app.jurisdictions.ca_on.catalog import (
    CLAIMS_SENIORS_CARE_CREDIT,
    COOP_EDUCATION_FULL_SHARE,
    COOP_EDUCATION_PAYROLL_RANGE,
    COOP_EDUCATION_PAYROLL_THRESHOLD,
    DEPENDANTS,
    DEPENDENT_CHILDREN,
    ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_MAXIMUM,
    ELIGIBLE_DEPENDANT_BASE,
    FERTILITY_CREDIT,
    FERTILITY_CREDIT_BEFORE_MAXIMUM,
    LIFT_CREDIT_BEFORE_MAXIMUM,
    LIFT_MAXIMUM_CREDIT,
    ONTARIO_TAX_BEFORE_REDUCTION,
    ONTARIO_TAX_REDUCTION,
    ONTARIO_TAX_REDUCTION_BEFORE_CONDITIONS,
    SENIORS_CARE_AMOUNT,
    SENIORS_CARE_BASE_AMOUNT,
    SENIORS_CARE_BEFORE_CLAIM,
    SENIORS_CARE_BEFORE_MAXIMUM,
    SENIORS_CARE_CREDIT,
    SENIORS_TRANSIT_AMOUNT_PAID_AT_MOST_MAXIMUM,
    SENIORS_TRANSIT_PAID,
    TAX_REDUCTION_AMOUNTS,
    TAX_REDUCTION_AMOUNTS_CLAIMABLE,
    TAX_REDUCTION_BASIC,
    TAX_REDUCTION_CLAIMABLE,
    TAX_REDUCTION_FOR_CHILDREN,
    TAX_REDUCTION_FOR_CHILDREN_BEFORE_SPOUSE_RULE,
    TAX_REDUCTION_FOR_DEPENDANTS,
    TAX_REDUCTION_FOR_DEPENDANTS_BEFORE_SPOUSE_RULE,
)
from tests.jurisdictions.ca_on.end_to_end.support import CENT, D, run_a


def test_the_trace_records_each_total_as_a_structured_line() -> None:
    # The lines of the one T2125, the one T2042 and the one T776 statement of Return A, then those
    # of the return form.
    result = run_a()
    trace = (
        *result["ca/t2125"][0].trace,
        *result["ca/t2042"][0].trace,
        *result["ca/t776"][0].trace,
        *result["ca-on/return"][0].trace,
    )
    subtracted = {line.output: line for line in trace if isinstance(line, SubtractedLine)}
    amounts = {line.output: line for line in trace if isinstance(line, CreditAmountLine)}
    tapered = {line.output: line for line in trace if isinstance(line, TaperedAmountLine)}
    capped = {line.output: line for line in trace if isinstance(line, CappedAmountLine)}
    per_unit = {line.output: line for line in trace if isinstance(line, PerUnitAmountLine)}
    multiples = {line.output: line for line in trace if isinstance(line, MultipleOverLine)}
    times = {line.output: line for line in trace if isinstance(line, TimesCountLine)}
    gated = {line.output: line for line in trace if isinstance(line, ThresholdGateLine)}
    fractions = {line.output: line for line in trace if isinstance(line, FractionAppliedLine)}
    divided = {
        line.output: line
        for line in trace
        if isinstance(line, DividedByRateLine) and line.output == CPP_PART_5_LINE_35
    }
    # Schedule 8 Part 5 line 35 "Amount from line 16 divided by 4%": 396.00 / 4% = 9,900.00 for
    # Return A (the second additional contribution required on 110,000).
    assert divided == {
        CPP_PART_5_LINE_35: DividedByRateLine(
            output=CPP_PART_5_LINE_35,
            dividend=CPP_PART_5_LINE_16,
            dividend_amount=D("396.00"),
            rate=Rate(D("0.04")),
            rounding=CENT,
            result=D("9900.00"),
        ),
    }
    assert subtracted == {
        # Form T691 Part 7 line 8 "Line 4 minus line 7": line 4, 16951.38, less line 7, 0.00:
        # 16951.38.
        AMT_PART_7_TAX_LESS_CREDITS: SubtractedLine(
            output=AMT_PART_7_TAX_LESS_CREDITS,
            minuend=AMT_PART_7_BASIC_TAX_WITH_RECAPTURE,
            minuend_amount=D("16951.38"),
            subtrahend=AMT_PART_7_CREDITS_TOTAL,
            subtrahend_amount=D("0.00"),
            result=D("16951.38"),
        ),
        # Worksheet ON428 line 8 "Line 6 minus line 7": line 6, the surtax on line 3 (523.79), less
        # line 7, the surtax on line 65 of the form (523.79): 0.
        ontario.WORKSHEET_ON428_LINE_8: SubtractedLine(
            output=ontario.WORKSHEET_ON428_LINE_8,
            minuend=ontario.WORKSHEET_ON428_LINE_6,
            minuend_amount=D("523.79"),
            subtrahend=ontario.WORKSHEET_ON428_LINE_7,
            subtrahend_amount=D("523.79"),
            result=D("0"),
        ),
        # Form T691 Part 8 line 13 "Balance of minimum tax carryover available for later years, if
        # any: line 1 minus line 12": line 1 (0) less line 12 (0): 0.
        AMT_CARRYOVER_BALANCE: SubtractedLine(
            output=AMT_CARRYOVER_BALANCE,
            minuend=AMT_MINIMUM_TAX_CARRYOVER_FROM_PREVIOUS_YEARS,
            minuend_amount=D("0"),
            subtrahend=AMT_MINIMUM_TAX_CARRYOVER_APPLIED,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Form T691 Part 8 line 17 "Total minimum tax carryover available for 2026: line 15 minus
        # line 16": line 15 (0) less line 16, the unapplied 2018 carryover (0): 0.
        AMT_CARRYOVER_AVAILABLE_FOR_2026: SubtractedLine(
            output=AMT_CARRYOVER_AVAILABLE_FOR_2026,
            minuend=AMT_CARRYOVER_BALANCE_WITH_ADDITIONAL_TAXES,
            minuend_amount=D("0"),
            subtrahend=AMT_UNAPPLIED_2018_CARRYOVER,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Form RC381 Part 3 line 16 "Line 11 minus line 15": both are 0.
        RC381_PART_3_LINE_16: SubtractedLine(
            output=RC381_PART_3_LINE_16,
            minuend=RC381_PART_3_LINE_11,
            minuend_amount=D("0"),
            subtrahend=RC381_PART_3_LINE_15,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Form RC381 Part 3 line 21 "Line 19 minus line 20": the T4 box 16 total of 4034.10 less
        # line 20, 3356.10, 678.00.
        RC381_PART_3_LINE_21: SubtractedLine(
            output=RC381_PART_3_LINE_21,
            minuend=CPP_T4_BASE_AND_FIRST_ADDITIONAL_CONTRIBUTIONS,
            minuend_amount=D("4034.10"),
            subtrahend=RC381_PART_3_LINE_20,
            subtrahend_amount=D("3356.10"),
            result=D("678.00"),
        ),
        # Form T691 Part 2 line 5 "Line 1 minus line 4" "Tax payable before minimum tax carryover":
        # 20146.25 less 3194.87, 16951.38.
        AMT_TAX_PAYABLE_BEFORE_MINIMUM_TAX_CARRYOVER: SubtractedLine(
            output=AMT_TAX_PAYABLE_BEFORE_MINIMUM_TAX_CARRYOVER,
            minuend=FEDERAL_TAX_WITH_SPLIT_INCOME,
            minuend_amount=D("20146.25"),
            subtrahend=AMT_CREDITS_TOTAL,
            subtrahend_amount=D("3194.87"),
            result=D("16951.38"),
        ),
        # Form T691 Part 2 line 7 "Line 5 minus line 6" "Basic federal tax": 16951.38 less 0 (line
        # 6, the carryover applied, is 0 for Return A), 16951.38.
        AMT_BASIC_FEDERAL_TAX: SubtractedLine(
            output=AMT_BASIC_FEDERAL_TAX,
            minuend=AMT_TAX_PAYABLE_BEFORE_MINIMUM_TAX_CARRYOVER,
            minuend_amount=D("16951.38"),
            subtrahend=AMT_MINIMUM_TAX_CARRYOVER_APPLIED,
            subtrahend_amount=D("0"),
            result=D("16951.38"),
        ),
        # Form T691 Part 8 line 9 "Line 4 minus line 8": 16951.38 less 0, 16951.38.
        AMT_TAX_PAYABLE_AFTER_CREDITS: SubtractedLine(
            output=AMT_TAX_PAYABLE_AFTER_CREDITS,
            minuend=AMT_TAX_PAYABLE_WITH_ITC_RECAPTURE,
            minuend_amount=D("16951.38"),
            subtrahend=AMT_SPLIT_INCOME_AND_CREDITS_TOTAL,
            subtrahend_amount=D("0"),
            result=D("16951.38"),
        ),
        # Form T2209 note (3), net income: line 23400 less line 23500 (the line 23600 amount, here
        # not floored), none repaid on Return A; then the deductions it lists, none on Return A,
        # come off that amount plus line 68360 of Form T1206.
        FOREIGN_TAX_CREDIT_NET_INCOME_BEFORE_SPLIT_INCOME: SubtractedLine(
            output=FOREIGN_TAX_CREDIT_NET_INCOME_BEFORE_SPLIT_INCOME,
            minuend=NET_INCOME_BEFORE_ADJUSTMENTS,
            minuend_amount=D("115000"),
            subtrahend=SOCIAL_BENEFITS_REPAYMENT,
            subtrahend_amount=D("0"),
            result=D("115000"),
        ),
        FOREIGN_TAX_CREDIT_NET_INCOME: SubtractedLine(
            output=FOREIGN_TAX_CREDIT_NET_INCOME,
            minuend=FOREIGN_TAX_CREDIT_NET_INCOME_WITH_SPLIT_INCOME,
            minuend_amount=D("115000"),
            subtrahend=FOREIGN_TAX_CREDIT_NET_INCOME_DEDUCTIONS,
            subtrahend_amount=D("0"),
            result=D("115000"),
        ),
        # Note (4), basic federal tax: line 42900 plus the dividend tax credit, less the federal
        # refundable First Nations abatement (line 44100), none on Return A.
        FOREIGN_TAX_CREDIT_BASIC_FEDERAL_TAX: SubtractedLine(
            output=FOREIGN_TAX_CREDIT_BASIC_FEDERAL_TAX,
            minuend=BASIC_FEDERAL_TAX_WITH_DIVIDEND_CREDIT,
            minuend_amount=D("16951.38"),
            subtrahend=FIRST_NATIONS_ABATEMENT,
            subtrahend_amount=D("0"),
            result=D("16951.38"),
        ),
        # Schedule 8 Part 5 line 74 "Line 72 minus line 73": 0.00 and line 73 ("0", line 24 of
        # Part 3 is 0) for Return A.
        CPP_PART_5_LINE_74: SubtractedLine(
            output=CPP_PART_5_LINE_74,
            minuend=CPP_PART_5_LINE_72,
            minuend_amount=D("0.00"),
            subtrahend=CPP_PART_5_LINE_73,
            subtrahend_amount=D("0"),
            result=D("0.00"),
        ),
        # Schedule 8 Part 5 line 77 "Amount A minus line 76": line A and line 75 (line 76 is the
        # amount from line 75) are both 0.00 for Return A.
        CPP_PART_5_LINE_77: SubtractedLine(
            output=CPP_PART_5_LINE_77,
            minuend=CPP_PART_5_LINE_75_BASE,
            minuend_amount=D("0.00"),
            subtrahend=CPP_PART_5_LINE_75,
            subtrahend_amount=D("0.00"),
            result=D("0.00"),
        ),
        # Schedule 8 Part 5 line 80 "Line 78 minus line 79": line 78 is the amount from line 70
        # and line 79 the amount from line 75, both 0.00 for Return A.
        CPP_PART_5_LINE_80: SubtractedLine(
            output=CPP_PART_5_LINE_80,
            minuend=CPP_PART_5_LINE_70,
            minuend_amount=D("0.00"),
            subtrahend=CPP_PART_5_LINE_75,
            subtrahend_amount=D("0.00"),
            result=D("0.00"),
        ),
        # Schedule 8 Part 5 line 83 "Line 81 minus line 82": line 81 is the amount from line 71
        # and line 82 the amount from line 77, both 0.00 for Return A.
        CPP_PART_5_LINE_83: SubtractedLine(
            output=CPP_PART_5_LINE_83,
            minuend=CPP_PART_5_LINE_71,
            minuend_amount=D("0.00"),
            subtrahend=CPP_PART_5_LINE_77,
            subtrahend_amount=D("0.00"),
            result=D("0.00"),
        ),
        # Schedule 8 Part 5 line 54 "Line 52 minus line 53": line 52 and line 53 are both 0
        # for Return A.
        CPP_PART_5_LINE_54: SubtractedLine(
            output=CPP_PART_5_LINE_54,
            minuend=CPP_PART_5_LINE_52,
            minuend_amount=D("0"),
            subtrahend=CPP_PART_5_LINE_53,
            subtrahend_amount=D("0.00"),
            result=D("0.00"),
        ),
        # Schedule 8 Part 5 line 63 "the result of line 23 of Part 3 minus line 56": line 23
        # of Part 3 and line 56 are both 0 for Return A.
        CPP_PART_5_LINE_23_LESS_LINE_56: SubtractedLine(
            output=CPP_PART_5_LINE_23_LESS_LINE_56,
            minuend=CPP_SECOND_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE,
            minuend_amount=D("0.00"),
            subtrahend=CPP_PART_5_LINE_56,
            subtrahend_amount=D("0.00"),
            result=D("0.00"),
        ),
        # Schedule 8 Part 5 line 61 "Line 59 minus line 60": line 59 and line 60 are both 0
        # for Return A.
        CPP_PART_5_LINE_61: SubtractedLine(
            output=CPP_PART_5_LINE_61,
            minuend=CPP_PART_5_LINE_59,
            minuend_amount=D("0"),
            subtrahend=CPP_PART_5_LINE_60,
            subtrahend_amount=D("0.00"),
            result=D("0.00"),
        ),
        # Schedule 8 Part 5 line 49 "Line 47 minus line 48": both are 0.00 for Return A.
        CPP_PART_5_LINE_49: SubtractedLine(
            output=CPP_PART_5_LINE_49,
            minuend=CPP_PART_5_LINE_47,
            minuend_amount=D("0.00"),
            subtrahend=CPP_PART_5_LINE_48,
            subtrahend_amount=D("0.00"),
            result=D("0.00"),
        ),
        # Schedule 8 Part 5 line 7 "Line 5 minus line 6": line 5 is the T4 box 16 total and line 6
        # is "0" for Return A.
        CPP_PART_5_LINE_7: SubtractedLine(
            CPP_PART_5_LINE_7,
            CPP_T4_BASE_AND_FIRST_ADDITIONAL_CONTRIBUTIONS,
            D("4034.10"),
            CPP_PART_5_LINE_6,
            D("0"),
            D("4034.10"),
        ),
        # Schedule 8 Part 5 line 13 "Line 11 minus line 12": line 11 is the T4 box 16A total and
        # line 12 is "0" for Return A.
        CPP_PART_5_LINE_13: SubtractedLine(
            CPP_PART_5_LINE_13,
            CPP_T4_SECOND_ADDITIONAL_CONTRIBUTIONS,
            D("396.00"),
            CPP_PART_5_LINE_12,
            D("0"),
            D("396.00"),
        ),
        # Schedule 8 Part 5 line 36 "Line 34 minus line 35": line C of Part 2 (9,900) less
        # 396.00 / 4% (9,900.00) for Return A.
        CPP_PART_5_LINE_36: SubtractedLine(
            CPP_PART_5_LINE_36,
            CPP_SECOND_ADDITIONAL_EARNINGS_MAXIMUM,
            D("9900.00"),
            CPP_PART_5_LINE_35,
            D("9900.00"),
            D("0.00"),
        ),
        # Schedule 8 Part 5 line 39 "Line 37 minus line 38": line 4 and line 25 are both "0" for
        # Return A.
        CPP_PART_5_LINE_39: SubtractedLine(
            CPP_PART_5_LINE_39,
            CPP_PART_5_LINE_4,
            D("0.00"),
            CPP_PART_5_LINE_25,
            D("0"),
            D("0.00"),
        ),
        # Schedule 8 Part 5 line 41 "Line 39 minus line 40": line 39 and line 30 are both "0" for
        # Return A.
        CPP_PART_5_LINE_41: SubtractedLine(
            CPP_PART_5_LINE_41,
            CPP_PART_5_LINE_39,
            D("0.00"),
            CPP_PART_5_LINE_30,
            D("0"),
            D("0.00"),
        ),
        # Schedule 8 Part 3b line 33 "Line 31 minus line 32": both are "0" for Return A.
        CPP_PART_3B_LINE_33: SubtractedLine(
            CPP_PART_3B_LINE_33,
            CPP_PART_3B_LINE_31,
            D("0"),
            CPP_PART_3B_LINE_32,
            D("0"),
            D("0"),
        ),
        # Schedule 8 Part 3b line 40 "Line 38 minus line 39": both are "0" for Return A.
        CPP_PART_3B_LINE_40: SubtractedLine(
            CPP_PART_3B_LINE_40,
            CPP_PART_3B_LINE_38,
            D("0"),
            CPP_PART_3B_LINE_39,
            D("0"),
            D("0"),
        ),
        # Schedule 8 Part 3b line 42 "the result of line 23 minus line 35": line 23 and line 35 are
        # "0" for Return A.
        CPP_PART_3B_LINE_23_LESS_LINE_35: SubtractedLine(
            CPP_PART_3B_LINE_23_LESS_LINE_35,
            CPP_SECOND_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE,
            D("0.00"),
            CPP_PART_3B_LINE_35,
            D("0"),
            D("0.00"),
        ),
        # Schedule 8 Part 3 line 10 "Line 8 minus line 9".
        CPP_ACTUAL_FIRST_ADDITIONAL_CONTRIBUTIONS: SubtractedLine(
            CPP_ACTUAL_FIRST_ADDITIONAL_CONTRIBUTIONS,
            CPP_T4_BASE_AND_FIRST_ADDITIONAL_CONTRIBUTIONS,
            D("4034.10"),
            CPP_ACTUAL_BASE_CONTRIBUTIONS,
            D("3356.10"),
            D("678.00"),
        ),
        # Schedule 8 Part 3 line 16 "Line 14 minus line 15".
        CPP_BASE_CONTRIBUTIONS_DIFFERENCE: SubtractedLine(
            CPP_BASE_CONTRIBUTIONS_DIFFERENCE,
            CPP_ACTUAL_BASE_CONTRIBUTIONS,
            D("3356.10"),
            CPP_BASE_CONTRIBUTIONS,
            D("3356.10"),
            D("0.00"),
        ),
        # Schedule 8 Part 3 line 19 "Line 17 minus line 18".
        CPP_FIRST_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE: SubtractedLine(
            CPP_FIRST_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE,
            CPP_ACTUAL_FIRST_ADDITIONAL_CONTRIBUTIONS,
            D("678.00"),
            CPP_FIRST_ADDITIONAL_CONTRIBUTIONS,
            D("678.00"),
            D("0.00"),
        ),
        # Schedule 8 Part 3 line 23 "Line 21 minus line 22".
        CPP_SECOND_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE: SubtractedLine(
            CPP_SECOND_ADDITIONAL_CONTRIBUTIONS_DIFFERENCE,
            CPP_T4_SECOND_ADDITIONAL_CONTRIBUTIONS,
            D("396.00"),
            CPP_SECOND_ADDITIONAL_CONTRIBUTIONS,
            D("396.00"),
            D("0.00"),
        ),
        # Form T2125 Chart C line 26 "Amount 25: amount 21" (printed with a subtraction sign): line
        # 25 is 0 for Return A (no leased vehicle), and amount 21 is 0.
        BUSINESS_VEHICLE_LEASE_CHARGES_NET: SubtractedLine(
            output=BUSINESS_VEHICLE_LEASE_CHARGES_NET,
            minuend=BUSINESS_VEHICLE_LEASE_CHARGE_PORTION,
            minuend_amount=D("0"),
            subtrahend=BUSINESS_VEHICLE_LEASE_PAYMENTS_BEFORE,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Form T2042 Chart C line 26 "Amount 25: amount 21" (printed with a subtraction sign): line
        # 25 is 0 for Return A (no leased vehicle), and amount 21 is 0.
        FARM_VEHICLE_LEASE_CHARGES_NET: SubtractedLine(
            output=FARM_VEHICLE_LEASE_CHARGES_NET,
            minuend=FARM_VEHICLE_LEASE_CHARGE_PORTION,
            minuend_amount=D("0"),
            subtrahend=FARM_VEHICLE_LEASE_PAYMENTS_BEFORE,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Form T2121 Chart C line 26 "Amount 25: amount 21" (printed with a subtraction sign): line
        # 25 is 0 for Return A (no leased vehicle), and amount 21 is 0.
        FISH_VEHICLE_LEASE_CHARGES_NET: SubtractedLine(
            output=FISH_VEHICLE_LEASE_CHARGES_NET,
            minuend=FISH_VEHICLE_LEASE_CHARGE_PORTION,
            minuend_amount=D("0"),
            subtrahend=FISH_VEHICLE_LEASE_PAYMENTS_BEFORE,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Form T691 Part 1 line 20 "Line 15 minus line 19 (if negative, show in brackets)": line 15
        # is Return A's 20000 of capital gains (line 19700) and line 19 is 0.
        AMT_NET_CAPITAL_GAINS_AFTER_ADJUSTMENTS: SubtractedLine(
            output=AMT_NET_CAPITAL_GAINS_AFTER_ADJUSTMENTS,
            minuend=CAPITAL_GAIN,
            minuend_amount=D("20000"),
            subtrahend=AMT_CAPITAL_GAINS_ADJUSTMENTS,
            subtrahend_amount=D("0"),
            result=D("20000"),
        ),
        # Form T691 Part 1 line 22 "Line 20 minus line 21": line 20 is 20000 and line 21 is the
        # taxable capital gains of line 12700, 10000.
        AMT_CAPITAL_GAINS_DIFFERENCE: SubtractedLine(
            output=AMT_CAPITAL_GAINS_DIFFERENCE,
            minuend=AMT_NET_CAPITAL_GAINS_AFTER_ADJUSTMENTS,
            minuend_amount=D("20000"),
            subtrahend=TAXABLE_CAPITAL_GAINS,
            subtrahend_amount=D("10000"),
            result=D("10000"),
        ),
        # Form T691 Part 1 line 26 "Line 24 minus line 25": Return A has no gifts of publicly
        # listed securities.
        AMT_PUBLICLY_LISTED_GIFTS_NET: SubtractedLine(
            output=AMT_PUBLICLY_LISTED_GIFTS_NET,
            minuend=AMT_PUBLICLY_LISTED_GIFTS_TOTAL,
            minuend_amount=D("0"),
            subtrahend=AMT_PUBLICLY_LISTED_GIFTS_T1170_LINE_68231,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Form T691 Part 1 line 47 "Line 45 minus line 46": Return A has no limited partnership
        # losses of other years, so line 45 and line 46 are 0.
        AMT_LIMITED_PARTNERSHIP_LOSSES_ADJUSTMENT: SubtractedLine(
            output=AMT_LIMITED_PARTNERSHIP_LOSSES_ADJUSTMENT,
            minuend=LIMITED_PARTNERSHIP_LOSSES_OF_OTHER_YEARS,
            minuend_amount=D("0"),
            subtrahend=AMT_LIMITED_PARTNERSHIP_DIFFERENCE_APPLIED,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Form T691 Part 1 line 50 "Line 48 minus line 49": Return A has no non-capital losses of
        # other years, so line 48 and line 49 are 0.
        AMT_NON_CAPITAL_LOSSES_ADJUSTMENT: SubtractedLine(
            output=AMT_NON_CAPITAL_LOSSES_ADJUSTMENT,
            minuend=NON_CAPITAL_LOSSES_OF_OTHER_YEARS,
            minuend_amount=D("0"),
            subtrahend=AMT_NON_CAPITAL_LOSSES_DIFFERENCE,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Form T691 Part 1 line 77 "Line 69 minus line 76": Return A has no other employment
        # expenses for this purpose, so line 69 and line 76 are 0.
        AMT_OFFICE_EXPENSES_ADJUSTMENT: SubtractedLine(
            output=AMT_OFFICE_EXPENSES_ADJUSTMENT,
            minuend=OTHER_EMPLOYMENT_EXPENSES,
            minuend_amount=D("0"),
            subtrahend=AMT_NON_DEDUCTIBLE_OFFICE_EXPENSES,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Schedule ON(S11) line 8 "Line 6 minus line 7": the unused balance, 0 on the return
        # with nothing brought forward, less the claim of line 5, 0.
        ontario.UNUSED_TUITION_CARRIED_FORWARD: SubtractedLine(
            output=ontario.UNUSED_TUITION_CARRIED_FORWARD,
            minuend=ontario.UNUSED_TUITION_AMOUNTS_BROUGHT_FORWARD,
            minuend_amount=D("0"),
            subtrahend=ontario.UNUSED_TUITION_CLAIMED,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Federal Worksheet "Line 23500" line 11 "Line 6 minus line 10": no floor is printed.
        SOCIAL_BENEFITS_LINE_11: SubtractedLine(
            output=SOCIAL_BENEFITS_LINE_11,
            minuend=SOCIAL_BENEFITS_LINE_6,
            minuend_amount=D("115000"),
            subtrahend=SOCIAL_BENEFITS_LINE_10,
            subtrahend_amount=D("0"),
            result=D("115000"),
        ),
        # Schedule 3 line 14 "Line 12 minus line 13" and line 19 "Line 17 minus line 18": Return A
        # has no deferral and no business investment loss, so line 18 is 0.
        CAPITAL_GAINS_AFTER_DEFERRAL: SubtractedLine(
            output=CAPITAL_GAINS_AFTER_DEFERRAL,
            minuend=CAPITAL_GAINS_OF_QUALIFIED_AND_OTHER_PROPERTIES,
            minuend_amount=D("20000"),
            subtrahend=CAPITAL_GAINS_DEFERRAL,
            subtrahend_amount=D("0"),
            result=D("20000"),
        ),
        CAPITAL_GAINS_BEFORE_RESERVES: SubtractedLine(
            output=CAPITAL_GAINS_BEFORE_RESERVES,
            minuend=CAPITAL_GAINS_BEFORE_INVESTMENT_LOSS_REDUCTION,
            minuend_amount=D("20000"),
            subtrahend=BUSINESS_INVESTMENT_LOSS_REDUCTION,
            subtrahend_amount=D("0"),
            result=D("20000"),
        ),
        # T776 Part 4 line 1 (amount A less line 9949, then less line 9366), line 9369, amounts 3,
        # 5 and 6 and the partnership's amount: Return A has none of these figures, so each is 0.
        RENTAL_EXPENSES_LESS_PERSONAL_PORTION: SubtractedLine(
            output=RENTAL_EXPENSES_LESS_PERSONAL_PORTION,
            minuend=RENTAL_TOTAL_EXPENSES,
            minuend_amount=D("0"),
            subtrahend=RENTAL_PERSONAL_PORTION,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        RENTAL_DEDUCTIBLE_EXPENSES: SubtractedLine(
            output=RENTAL_DEDUCTIBLE_EXPENSES,
            minuend=RENTAL_EXPENSES_LESS_PERSONAL_PORTION,
            minuend_amount=D("0"),
            subtrahend=RENTAL_NON_COMPLIANT_EXPENSES,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        RENTAL_NET_INCOME_BEFORE_ADJUSTMENTS: SubtractedLine(
            output=RENTAL_NET_INCOME_BEFORE_ADJUSTMENTS,
            minuend=GROSS_RENTAL_INCOME,
            minuend_amount=D("0"),
            subtrahend=RENTAL_DEDUCTIBLE_EXPENSES,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        RENTAL_NET_INCOME_AFTER_COOWNER_EXPENSES: SubtractedLine(
            output=RENTAL_NET_INCOME_AFTER_COOWNER_EXPENSES,
            minuend=RENTAL_NET_INCOME_SHARE,
            minuend_amount=D("0"),
            subtrahend=RENTAL_COOWNER_OTHER_EXPENSES,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        RENTAL_NET_INCOME_AFTER_TERMINAL_LOSS: SubtractedLine(
            output=RENTAL_NET_INCOME_AFTER_TERMINAL_LOSS,
            minuend=RENTAL_NET_INCOME_WITH_RECAPTURE,
            minuend_amount=D("0"),
            subtrahend=RENTAL_TERMINAL_LOSS,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # T776 line 9936: amount ii less the personal part of CCA, then less the CCA for
        # business-use-of-home expenses; with no classes each is 0.
        RENTAL_CCA_CLAIM_LESS_PERSONAL_PART: SubtractedLine(
            output=RENTAL_CCA_CLAIM_LESS_PERSONAL_PART,
            minuend=RENTAL_CCA_CLAIM_SHARE,
            minuend_amount=D("0"),
            subtrahend=RENTAL_CCA_PERSONAL_PART,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        RENTAL_CCA_CLAIM_BEFORE_LIMIT: SubtractedLine(
            output=RENTAL_CCA_CLAIM_BEFORE_LIMIT,
            minuend=RENTAL_CCA_CLAIM_LESS_PERSONAL_PART,
            minuend_amount=D("0"),
            subtrahend=RENTAL_CCA_BUSINESS_USE_OF_HOME,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        RENTAL_NET_INCOME_AFTER_CCA: SubtractedLine(
            output=RENTAL_NET_INCOME_AFTER_CCA,
            minuend=RENTAL_NET_INCOME_AFTER_TERMINAL_LOSS,
            minuend_amount=D("0"),
            subtrahend=RENTAL_CCA_CLAIM,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        RENTAL_PARTNERSHIP_NET_INCOME: SubtractedLine(
            output=RENTAL_PARTNERSHIP_NET_INCOME,
            minuend=RENTAL_PARTNER_SHARE_WITH_REBATE,
            minuend_amount=D("0"),
            subtrahend=RENTAL_PARTNER_OTHER_EXPENSES,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Form T1172 line 6 "Line 4 minus line 5" and line 8 "line 1 minus line 7", with no
        # floor on either.
        RESP_AIPS_LIMIT_REMAINING: SubtractedLine(
            output=RESP_AIPS_LIMIT_REMAINING,
            minuend=RESP_AIPS_LIFETIME_LIMIT,
            minuend_amount=D("50000.00"),
            subtrahend=RESP_AIPS_REDUCTION_USED_IN_PREVIOUS_YEARS,
            subtrahend_amount=D("0"),
            result=D("50000.00"),
        ),
        RESP_AIPS_SUBJECT_TO_TAX: SubtractedLine(
            output=RESP_AIPS_SUBJECT_TO_TAX,
            minuend=RESP_AIPS_RECEIVED_PART_A,
            minuend_amount=D("0"),
            subtrahend=RESP_AIPS_REDUCTION,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Worksheet ON428's line C "Amount A minus amount B": no dividends.
        ontario.DIVIDENDS_AMOUNT_A_LESS_B: SubtractedLine(
            output=ontario.DIVIDENDS_AMOUNT_A_LESS_B,
            minuend=ontario.DIVIDENDS_AMOUNT_A,
            minuend_amount=D("0"),
            subtrahend=ontario.DIVIDENDS_AMOUNT_B,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # The Federal Worksheet's line C "Amount A minus amount B": no dividends with no slip.
        DIVIDENDS_AMOUNT_A_LESS_B: SubtractedLine(
            output=DIVIDENDS_AMOUNT_A_LESS_B,
            minuend=DIVIDENDS_AMOUNT_A,
            minuend_amount=D("0"),
            subtrahend=DIVIDENDS_AMOUNT_B,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # The Federal Worksheet's line 5 "Line 1 minus line 4 =": no floor is printed.
        NET_INCOME_LESS_UCCB_AND_RDSP_INCOME: SubtractedLine(
            output=NET_INCOME_LESS_UCCB_AND_RDSP_INCOME,
            minuend=NET_INCOME_BEFORE_ADJUSTMENTS_NOT_BELOW_ZERO,
            minuend_amount=D("115000"),
            subtrahend=UCCB_AND_RDSP_INCOME,
            subtrahend_amount=D("0"),
            result=D("115000"),
        ),
        # Schedule 9 chart for line 33900 line 3 "Line 1 minus Line 2", line 14 "Line 12 minus line
        # 13" and line 21's amount G, "Amount E minus amount F": all 0 for donations of 0.
        CAPITAL_PROPERTY_GIFTS: SubtractedLine(
            output=CAPITAL_PROPERTY_GIFTS,
            minuend=CAPITAL_GIFT_TAXABLE_GAINS,
            minuend_amount=D("0"),
            subtrahend=CAPITAL_GIFT_GAINS_DEDUCTION,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        DONATIONS_OVER_FIRST_TIER: SubtractedLine(
            output=DONATIONS_OVER_FIRST_TIER,
            minuend=DONATIONS_AND_GIFTS_TOTAL,
            minuend_amount=D("0"),
            subtrahend=DONATIONS_FIRST_TIER,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        REGULAR_RATE_DONATIONS: SubtractedLine(
            output=REGULAR_RATE_DONATIONS,
            minuend=DONATIONS_OVER_FIRST_TIER,
            minuend_amount=D("0"),
            subtrahend=HIGH_INCOME_DONATIONS,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # The Federal Worksheet's line 11 "Line 9 minus line 10. Enter this amount on line 12100
        # of your return.": nothing reported in previous years comes off nothing.
        INTEREST_AND_OTHER_INVESTMENT_INCOME: SubtractedLine(
            output=INTEREST_AND_OTHER_INVESTMENT_INCOME,
            minuend=INVESTMENT_INCOME_BEFORE_PRIOR_YEARS,
            minuend_amount=D("0"),
            subtrahend=INVESTMENT_INCOME_REPORTED_IN_PREVIOUS_YEARS,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Schedule 7 line 23 "Line 21 minus line 22 Your unused contributions available to carry
        # forward to a future year": all of the 1926 available is deducted, so nothing is left.
        UNUSED_RRSP_CONTRIBUTIONS_CARRIED_FORWARD: SubtractedLine(
            output=UNUSED_RRSP_CONTRIBUTIONS_CARRIED_FORWARD,
            minuend=RRSP_CONTRIBUTIONS_AVAILABLE,
            minuend_amount=D("1926"),
            subtrahend=RRSP_DEDUCTION,
            subtrahend_amount=D("1926"),
            result=D("0"),
        ),
        # T1 line 167 "Line 149 minus line 166 ... Refund or balance owing": it takes amounts
        # already in cents, is not floored, and is positive here, so a balance owing (line 48500).
        REFUND_OR_BALANCE_OWING: SubtractedLine(
            output=REFUND_OR_BALANCE_OWING,
            minuend=TOTAL_PAYABLE,
            minuend_amount=D("25897.15"),
            subtrahend=TOTAL_CREDITS,
            subtrahend_amount=D("25000"),
            result=D("897.15"),
        ),
        # The Ontario opportunities fund, line 3 and line 46600 "Net refund (line 1 minus line 2)".
        ontario.NET_REFUND: SubtractedLine(
            output=ontario.NET_REFUND,
            minuend=ontario.REFUND_BEFORE_DONATION,
            minuend_amount=D("0"),
            subtrahend=ontario.OPPORTUNITIES_FUND_DONATION,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Form T1436 line 15.
        BUSINESS_INVESTMENT_LOSS_REDUCTION_AVAILABLE: SubtractedLine(
            output=BUSINESS_INVESTMENT_LOSS_REDUCTION_AVAILABLE,
            minuend=CAPITAL_GAINS_DEDUCTIONS_CLAIMED_1985_TO_2024,
            minuend_amount=D("0"),
            subtrahend=OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_2024,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Form T1436 line 18.
        BUSINESS_INVESTMENT_LOSS_AFTER_REDUCTION: SubtractedLine(
            output=BUSINESS_INVESTMENT_LOSS_AFTER_REDUCTION,
            minuend=BUSINESS_INVESTMENT_LOSS,
            minuend_amount=D("0"),
            subtrahend=BUSINESS_INVESTMENT_LOSS_REDUCTION,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Schedule 15 line 3.
        FHSA_CONTRIBUTIONS_IN_2025_BEFORE_FIRST_QUALIFYING_WITHDRAWAL: SubtractedLine(
            output=FHSA_CONTRIBUTIONS_IN_2025_BEFORE_FIRST_QUALIFYING_WITHDRAWAL,
            minuend=FHSA_CONTRIBUTIONS_IN_2025,
            minuend_amount=D("0"),
            subtrahend=FHSA_CONTRIBUTIONS_IN_2025_AFTER_FIRST_QUALIFYING_WITHDRAWAL,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Schedule 15 line 9.
        FHSA_CONTRIBUTIONS_IN_2024_AFTER_FIRST_QUALIFYING_WITHDRAWAL: SubtractedLine(
            output=FHSA_CONTRIBUTIONS_IN_2024_AFTER_FIRST_QUALIFYING_WITHDRAWAL,
            minuend=FHSA_CONTRIBUTIONS_IN_2024,
            minuend_amount=D("0"),
            subtrahend=FHSA_CONTRIBUTIONS_IN_2024_BEFORE_FIRST_QUALIFYING_WITHDRAWAL,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Schedule 15 line 23.
        FHSA_NET_RRSP_TRANSFER_AMOUNT: SubtractedLine(
            output=FHSA_NET_RRSP_TRANSFER_AMOUNT,
            minuend=FHSA_TOTAL_RRSP_TRANSFERS,
            minuend_amount=D("0"),
            subtrahend=FHSA_TOTAL_DESIGNATED_TRANSFERS,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Schedule 15 line 27.
        FHSA_NET_RRSP_TRANSFER_AMOUNT_FOR_2024_AND_PRIOR_YEARS: SubtractedLine(
            output=FHSA_NET_RRSP_TRANSFER_AMOUNT_FOR_2024_AND_PRIOR_YEARS,
            minuend=FHSA_RRSP_TRANSFERS_IN_2024_AND_PRIOR_YEARS,
            minuend_amount=D("0"),
            subtrahend=FHSA_DESIGNATED_TRANSFERS_IN_2024_AND_PRIOR_YEARS,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Schedule 15 line 36.
        FHSA_NET_TRANSFER_AMOUNT_AFTER_PRIOR_YEARS: SubtractedLine(
            output=FHSA_NET_TRANSFER_AMOUNT_AFTER_PRIOR_YEARS,
            minuend=FHSA_NET_RRSP_TRANSFER_AMOUNT,
            minuend_amount=D("0"),
            subtrahend=FHSA_TRANSFER_AMOUNT_PLUS_VARIABLE_F_AMOUNT,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Schedule 15 line 45.
        FHSA_ANNUAL_LIMITS_LESS_DEDUCTIONS: SubtractedLine(
            output=FHSA_ANNUAL_LIMITS_LESS_DEDUCTIONS,
            minuend=FHSA_TOTAL_ANNUAL_LIMITS,
            minuend_amount=D("0"),
            subtrahend=FHSA_DEDUCTIONS_FOR_2024_AND_PRIOR_YEARS,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Schedule 15 line 48.
        FHSA_LIFETIME_LIMIT_LESS_DEDUCTIONS: SubtractedLine(
            output=FHSA_LIFETIME_LIMIT_LESS_DEDUCTIONS,
            minuend=FHSA_LIFETIME_LIMIT,
            minuend_amount=D("40000.00"),
            subtrahend=FHSA_DEDUCTIONS_FOR_2024_AND_PRIOR_YEARS,
            subtrahend_amount=D("0"),
            result=D("40000.00"),
        ),
        # Schedule 15 line 56.
        FHSA_CONTRIBUTIONS_AVAILABLE: SubtractedLine(
            output=FHSA_CONTRIBUTIONS_AVAILABLE,
            minuend=FHSA_UNUSED_CONTRIBUTIONS_PLUS_CONTRIBUTIONS,
            minuend_amount=D("0"),
            subtrahend=FHSA_EXCESS_DESIGNATED_WITHDRAWALS,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Schedule 15 line 58.
        FHSA_UNUSED_CONTRIBUTIONS_CARRIED_FORWARD: SubtractedLine(
            output=FHSA_UNUSED_CONTRIBUTIONS_CARRIED_FORWARD,
            minuend=FHSA_CONTRIBUTIONS_AVAILABLE,
            minuend_amount=D("0"),
            subtrahend=FHSA_DEDUCTION,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Form T1206 Part 2 line 15 "Line 10 minus line 14" and line 22 "Line 15 minus line 21",
        # with no floor printed on either: all 0 for Return A.
        # Form T1206 Part 3 line 39 "Line 33 minus line 38" and line 47 "Line 39 minus line 46",
        # exact and signed: Return A has no split income, so each is 0.
        ontario.SPLIT_INCOME_LINE_39: SubtractedLine(
            output=ontario.SPLIT_INCOME_LINE_39,
            minuend=ontario.ONTARIO_TAX_ON_SPLIT_INCOME,
            minuend_amount=D("0"),
            subtrahend=ontario.SPLIT_INCOME_LINE_38,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        ontario.SPLIT_INCOME_LINE_47: SubtractedLine(
            output=ontario.SPLIT_INCOME_LINE_47,
            minuend=ontario.SPLIT_INCOME_LINE_39,
            minuend_amount=D("0"),
            subtrahend=ontario.SPLIT_INCOME_LINE_46,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        SPLIT_INCOME_LINE_15: SubtractedLine(
            output=SPLIT_INCOME_LINE_15,
            minuend=SPLIT_INCOME_LINE_10,
            minuend_amount=D("0"),
            subtrahend=SPLIT_INCOME_LINE_14,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        SPLIT_INCOME_LINE_22: SubtractedLine(
            output=SPLIT_INCOME_LINE_22,
            minuend=SPLIT_INCOME_LINE_15,
            minuend_amount=D("0"),
            subtrahend=SPLIT_INCOME_LINE_21,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # T1 line 23400.
        NET_INCOME_BEFORE_ADJUSTMENTS: SubtractedLine(
            output=NET_INCOME_BEFORE_ADJUSTMENTS,
            minuend=TOTAL_INCOME,
            minuend_amount=D("120000"),
            subtrahend=DEDUCTIONS_FROM_TOTAL_INCOME,
            subtrahend_amount=D("5000"),
            result=D("115000"),
        ),
        # Line 23600 before its floor, which Form T1206 Part 1 line 5 and Schedule ON479-A column 1
        # line 1 read: line 23400 less line 23500, which is 0 for Return A.
        NET_INCOME_SIGNED: SubtractedLine(
            output=NET_INCOME_SIGNED,
            minuend=NET_INCOME_BEFORE_ADJUSTMENTS,
            minuend_amount=D("115000"),
            subtrahend=SOCIAL_BENEFITS_REPAYMENT,
            subtrahend_amount=D("0"),
            result=D("115000"),
        ),
        # Form T1436 line 3 "Pre-1986 capital loss balance available for 2025: line 1 minus line
        # 2" and line 8 "Balance of unapplied adjusted net capital losses of other years not used
        # to reduce taxable capital gains: line 4 minus line 7", for no losses and no claim.
        PRE_1986_CAPITAL_LOSS_BALANCE: SubtractedLine(
            output=PRE_1986_CAPITAL_LOSS_BALANCE,
            minuend=NET_CAPITAL_LOSSES_BEFORE_MAY_23_1985,
            minuend_amount=D("0"),
            subtrahend=PRE_1986_DEDUCTIONS_TOTAL,
            subtrahend_amount=D("0.00"),
            result=D("0.00"),
        ),
        UNAPPLIED_ADJUSTED_NET_CAPITAL_LOSSES: SubtractedLine(
            output=UNAPPLIED_ADJUSTED_NET_CAPITAL_LOSSES,
            minuend=TOTAL_ADJUSTED_NET_CAPITAL_LOSSES,
            minuend_amount=D("0.00"),
            subtrahend=ADJUSTED_NET_CAPITAL_LOSSES_APPLIED,
            subtrahend_amount=D("0"),
            result=D("0.00"),
        ),
        # Form T1436 Chart A: what is left of line 13 (the amount claimed, 0) after each row,
        # oldest first, and column E "Remaining adjusted net capital losses (column C minus column
        # D)".
        ADJUSTED_LOSSES_LEFT_AFTER_BEFORE_MAY_23_1985: SubtractedLine(
            output=ADJUSTED_LOSSES_LEFT_AFTER_BEFORE_MAY_23_1985,
            minuend=TOTAL_ADJUSTED_NET_CAPITAL_LOSSES_APPLIED,
            minuend_amount=D("0.00"),
            subtrahend=ADJUSTED_LOSSES_APPLIED_BEFORE_MAY_23_1985,
            subtrahend_amount=D("0.00"),
            result=D("0.00"),
        ),
        REMAINING_ADJUSTED_LOSSES_BEFORE_MAY_23_1985: SubtractedLine(
            output=REMAINING_ADJUSTED_LOSSES_BEFORE_MAY_23_1985,
            minuend=ADJUSTED_GROSS_CAPITAL_LOSSES_BEFORE_MAY_23_1985,
            minuend_amount=D("0.00"),
            subtrahend=ADJUSTED_LOSSES_APPLIED_BEFORE_MAY_23_1985,
            subtrahend_amount=D("0.00"),
            result=D("0.00"),
        ),
        ADJUSTED_LOSSES_LEFT_AFTER_1985_TO_1987: SubtractedLine(
            output=ADJUSTED_LOSSES_LEFT_AFTER_1985_TO_1987,
            minuend=ADJUSTED_LOSSES_LEFT_AFTER_BEFORE_MAY_23_1985,
            minuend_amount=D("0.00"),
            subtrahend=ADJUSTED_LOSSES_APPLIED_1985_TO_1987,
            subtrahend_amount=D("0.00"),
            result=D("0.00"),
        ),
        REMAINING_ADJUSTED_LOSSES_1985_TO_1987: SubtractedLine(
            output=REMAINING_ADJUSTED_LOSSES_1985_TO_1987,
            minuend=ADJUSTED_GROSS_CAPITAL_LOSSES_1985_TO_1987,
            minuend_amount=D("0.00"),
            subtrahend=ADJUSTED_LOSSES_APPLIED_1985_TO_1987,
            subtrahend_amount=D("0.00"),
            result=D("0.00"),
        ),
        ADJUSTED_LOSSES_LEFT_AFTER_1988_AND_1989: SubtractedLine(
            output=ADJUSTED_LOSSES_LEFT_AFTER_1988_AND_1989,
            minuend=ADJUSTED_LOSSES_LEFT_AFTER_1985_TO_1987,
            minuend_amount=D("0.00"),
            subtrahend=ADJUSTED_LOSSES_APPLIED_1988_AND_1989,
            subtrahend_amount=D("0.00"),
            result=D("0.00"),
        ),
        REMAINING_ADJUSTED_LOSSES_1988_AND_1989: SubtractedLine(
            output=REMAINING_ADJUSTED_LOSSES_1988_AND_1989,
            minuend=ADJUSTED_GROSS_CAPITAL_LOSSES_1988_AND_1989,
            minuend_amount=D("0.00"),
            subtrahend=ADJUSTED_LOSSES_APPLIED_1988_AND_1989,
            subtrahend_amount=D("0.00"),
            result=D("0.00"),
        ),
        ADJUSTED_LOSSES_LEFT_AFTER_1990_TO_1999: SubtractedLine(
            output=ADJUSTED_LOSSES_LEFT_AFTER_1990_TO_1999,
            minuend=ADJUSTED_LOSSES_LEFT_AFTER_1988_AND_1989,
            minuend_amount=D("0.00"),
            subtrahend=ADJUSTED_LOSSES_APPLIED_1990_TO_1999,
            subtrahend_amount=D("0.00"),
            result=D("0.00"),
        ),
        REMAINING_ADJUSTED_LOSSES_1990_TO_1999: SubtractedLine(
            output=REMAINING_ADJUSTED_LOSSES_1990_TO_1999,
            minuend=ADJUSTED_GROSS_CAPITAL_LOSSES_1990_TO_1999,
            minuend_amount=D("0.00"),
            subtrahend=ADJUSTED_LOSSES_APPLIED_1990_TO_1999,
            subtrahend_amount=D("0.00"),
            result=D("0.00"),
        ),
        ADJUSTED_LOSSES_LEFT_AFTER_2000: SubtractedLine(
            output=ADJUSTED_LOSSES_LEFT_AFTER_2000,
            minuend=ADJUSTED_LOSSES_LEFT_AFTER_1990_TO_1999,
            minuend_amount=D("0.00"),
            subtrahend=ADJUSTED_LOSSES_APPLIED_2000,
            subtrahend_amount=D("0.00"),
            result=D("0.00"),
        ),
        REMAINING_ADJUSTED_LOSSES_2000: SubtractedLine(
            output=REMAINING_ADJUSTED_LOSSES_2000,
            minuend=ADJUSTED_GROSS_CAPITAL_LOSSES_2000,
            minuend_amount=D("0.00"),
            subtrahend=ADJUSTED_LOSSES_APPLIED_2000,
            subtrahend_amount=D("0.00"),
            result=D("0.00"),
        ),
        REMAINING_ADJUSTED_LOSSES_2001_TO_2024: SubtractedLine(
            output=REMAINING_ADJUSTED_LOSSES_2001_TO_2024,
            minuend=ADJUSTED_GROSS_CAPITAL_LOSSES_2001_TO_2024,
            minuend_amount=D("0.00"),
            subtrahend=ADJUSTED_LOSSES_APPLIED_2001_TO_2024,
            subtrahend_amount=D("0.00"),
            result=D("0.00"),
        ),
        # Federal Worksheet "Line 45200 - Refundable medical expense supplement" (T1 line 154),
        # Return A: line 21500 and line 33200 are 0, so line 11 and line 13 are 0.
        MEDICAL_SUPPLEMENT_EMPLOYMENT_INCOME_LESS_WAGE_LOSS: SubtractedLine(
            output=MEDICAL_SUPPLEMENT_EMPLOYMENT_INCOME_LESS_WAGE_LOSS,
            minuend=MEDICAL_SUPPLEMENT_EMPLOYMENT_INCOME,
            minuend_amount=D("110000"),
            subtrahend=WAGE_LOSS_REPLACEMENT_PLAN_INCOME,
            subtrahend_amount=D("0"),
            result=D("110000"),
        ),
        # Schedule 11, Schedule 2 and line 45350 (Return A claims none: every figure is 0).
        CANADIAN_TUITION_AVAILABLE: SubtractedLine(
            output=CANADIAN_TUITION_AVAILABLE,
            minuend=CANADIAN_TUITION_FEES,
            minuend_amount=D("0"),
            subtrahend=CANADA_TRAINING_CREDIT,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        TUITION_INCOME_REMAINING: SubtractedLine(
            output=TUITION_INCOME_REMAINING,
            minuend=TUITION_INCOME_LESS_CREDITS,
            minuend_amount=D("116906.08"),
            subtrahend=UNUSED_TUITION_CLAIMED,
            subtrahend_amount=D("0"),
            result=D("116906.08"),
        ),
        UNUSED_FEDERAL_TUITION: SubtractedLine(
            output=UNUSED_FEDERAL_TUITION,
            minuend=TOTAL_TUITION_AVAILABLE,
            minuend_amount=D("0"),
            subtrahend=FEDERAL_TUITION_AMOUNT,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        TUITION_CARRIED_FORWARD: SubtractedLine(
            output=TUITION_CARRIED_FORWARD,
            minuend=UNUSED_FEDERAL_TUITION,
            minuend_amount=D("0"),
            subtrahend=TUITION_TRANSFERRED,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Form T2048 (line 25395) and Chart A: Return A enters nothing on the form, so its lines
        # are 0 (or, where they read another line, that line's figure).
        QBT_NET_RENTAL_LOSS: SubtractedLine(
            QBT_NET_RENTAL_LOSS, QBT_NET_RENTAL_INCOME, D("0"), NET_RENTAL_INCOME, D("0"), D("0")
        ),
        QCC_ELECTION_DEDUCTION: SubtractedLine(
            QCC_ELECTION_DEDUCTION,
            QBT_DEDUCTION_AVAILABLE,
            D("0"),
            QBT_ELECTION_DEDUCTION,
            D("0"),
            D("0"),
        ),
        QBT_REDUCTION_AMOUNT: SubtractedLine(
            QBT_REDUCTION_AMOUNT,
            QBT_DEDUCTION_BASE,
            D("0"),
            QBT_CAPITAL_GAINS_DEDUCTION,
            D("0"),
            D("0"),
        ),
        QBT_NET_INVESTMENT_LOSS_REDUCTION: SubtractedLine(
            QBT_NET_INVESTMENT_LOSS_REDUCTION,
            QBT_ALLOCATION_LIMIT,
            D("0"),
            QBT_ABIL_REDUCTION,
            D("0"),
            D("0"),
        ),
        # T2125 amounts 3C, 3F, 5D, 7J and 9369, lines 8518, 8519, 9936 (two steps) and 9946
        # (T1 line 13500): Return A has none of these figures, so each is 0.
        BUSINESS_SALES_SUBTOTAL: SubtractedLine(
            output=BUSINESS_SALES_SUBTOTAL,
            minuend=BUSINESS_GROSS_SALES,
            minuend_amount=D("0"),
            subtrahend=BUSINESS_SALES_ADJUSTMENTS,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        BUSINESS_QUICK_METHOD_ASSISTANCE: SubtractedLine(
            output=BUSINESS_QUICK_METHOD_ASSISTANCE,
            minuend=BUSINESS_QUICK_METHOD_GST_HST,
            minuend_amount=D("0"),
            subtrahend=BUSINESS_QUICK_METHOD_REMITTED,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        BUSINESS_COST_OF_GOODS_SOLD: SubtractedLine(
            output=BUSINESS_COST_OF_GOODS_SOLD,
            minuend=BUSINESS_COST_OF_GOODS_SUBTOTAL,
            minuend_amount=D("0"),
            subtrahend=BUSINESS_CLOSING_INVENTORY,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        BUSINESS_GROSS_PROFIT: SubtractedLine(
            output=BUSINESS_GROSS_PROFIT,
            minuend=BUSINESS_GROSS_INCOME_FOR_GROSS_PROFIT,
            minuend_amount=D("0"),
            subtrahend=BUSINESS_COST_OF_GOODS_SOLD,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        BUSINESS_CCA_CLAIM_LESS_PERSONAL_PART: SubtractedLine(
            output=BUSINESS_CCA_CLAIM_LESS_PERSONAL_PART,
            minuend=BUSINESS_CCA_TABLE_CLAIM,
            minuend_amount=D("0"),
            subtrahend=BUSINESS_CCA_PERSONAL_PART,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        BUSINESS_CCA_CLAIM: SubtractedLine(
            output=BUSINESS_CCA_CLAIM,
            minuend=BUSINESS_CCA_CLAIM_LESS_PERSONAL_PART,
            minuend_amount=D("0"),
            subtrahend=BUSINESS_HOME_CCA,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        BUSINESS_NET_INCOME_BEFORE_ADJUSTMENTS: SubtractedLine(
            output=BUSINESS_NET_INCOME_BEFORE_ADJUSTMENTS,
            minuend=BUSINESS_GROSS_INCOME_BEFORE_EXPENSES,
            minuend_amount=D("0"),
            subtrahend=BUSINESS_TOTAL_EXPENSES,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        BUSINESS_NET_INCOME_AFTER_ADJUSTMENTS: SubtractedLine(
            output=BUSINESS_NET_INCOME_AFTER_ADJUSTMENTS,
            minuend=BUSINESS_PARTNERSHIP_TOTAL,
            minuend_amount=D("0"),
            subtrahend=BUSINESS_PARTNER_OTHER_AMOUNTS,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        BUSINESS_HOME_EXPENSES_BUSINESS_PART: SubtractedLine(
            output=BUSINESS_HOME_EXPENSES_BUSINESS_PART,
            minuend=BUSINESS_HOME_EXPENSES_SUBTOTAL,
            minuend_amount=D("0"),
            subtrahend=BUSINESS_HOME_PERSONAL_USE_PART,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        BUSINESS_INCOME: SubtractedLine(
            output=BUSINESS_INCOME,
            minuend=BUSINESS_NET_INCOME_AFTER_ADJUSTMENTS,
            minuend_amount=D("0"),
            subtrahend=BUSINESS_HOME_EXPENSES,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # T2042 Part 4, Part 5, Part 7 and T1 line 25 subtractions: Return A has no farming
        # statement, so each is 0.
        FARM_CCA_CLAIM_LESS_PERSONAL_PART: SubtractedLine(
            output=FARM_CCA_CLAIM_LESS_PERSONAL_PART,
            minuend=FARM_CCA_TABLE_CLAIM,
            minuend_amount=D("0"),
            subtrahend=FARM_CCA_PERSONAL_PART,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        FARM_CCA_CLAIM: SubtractedLine(
            output=FARM_CCA_CLAIM,
            minuend=FARM_CCA_CLAIM_LESS_PERSONAL_PART,
            minuend_amount=D("0"),
            subtrahend=FARM_HOME_CCA,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        FARM_NET_INCOME_BEFORE_ADJUSTMENTS: SubtractedLine(
            output=FARM_NET_INCOME_BEFORE_ADJUSTMENTS,
            minuend=FARM_GROSS_INCOME_BEFORE_EXPENSES,
            minuend_amount=D("0"),
            subtrahend=FARM_TOTAL_EXPENSES,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        FARM_NET_INCOME_AFTER_ADJUSTMENTS: SubtractedLine(
            output=FARM_NET_INCOME_AFTER_ADJUSTMENTS,
            minuend=FARM_PARTNERSHIP_TOTAL,
            minuend_amount=D("0"),
            subtrahend=FARM_PARTNER_OTHER_AMOUNTS,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        FARM_HOME_EXPENSES_BUSINESS_PART: SubtractedLine(
            output=FARM_HOME_EXPENSES_BUSINESS_PART,
            minuend=FARM_HOME_EXPENSES_SUBTOTAL,
            minuend_amount=D("0"),
            subtrahend=FARM_HOME_PERSONAL_USE_PART,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        FARMING_INCOME: SubtractedLine(
            output=FARMING_INCOME,
            minuend=FARM_NET_INCOME_AFTER_ADJUSTMENTS,
            minuend_amount=D("0"),
            subtrahend=FARM_HOME_EXPENSES,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Form T657 (line 25400): Return A enters nothing on it, so its lines are 0 (or,
        # where they read another line, that line's figure).
        CHART_2025_PART_2_AMOUNT_F: SubtractedLine(
            output=CHART_2025_PART_2_AMOUNT_F,
            minuend=QSBCS_GAIN_OR_LOSS,
            minuend_amount=D("0"),
            subtrahend=T657_PART_2_EXCLUDED_F,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        CHART_2025_PART_2_AMOUNT_G: SubtractedLine(
            output=CHART_2025_PART_2_AMOUNT_G,
            minuend=QFFP_GAIN_OR_LOSS,
            minuend_amount=D("0"),
            subtrahend=T657_PART_2_EXCLUDED_G,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        CHART_2025_PART_2_AMOUNT_H: SubtractedLine(
            output=CHART_2025_PART_2_AMOUNT_H,
            minuend=QFFP_FORECLOSURE_GAIN_OR_LOSS,
            minuend_amount=D("0"),
            subtrahend=T657_PART_2_EXCLUDED_H,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        CHART_2_LINE_16: SubtractedLine(
            output=CHART_2_LINE_16,
            minuend=T657_CHART_2_LINE_14,
            minuend_amount=D("0"),
            subtrahend=CHART_2_LINE_14_OVER_TWICE_IR,
            subtrahend_amount=D("0.00"),
            result=D("0.00"),
        ),
        ANNUAL_GAINS_LINE_10: SubtractedLine(
            output=ANNUAL_GAINS_LINE_10,
            minuend=SCHEDULE_3_LINE_19900,
            minuend_amount=D("10000.00"),
            subtrahend=ANNUAL_GAINS_LINE_9,
            subtrahend_amount=D("0.00"),
            result=D("10000.00"),
        ),
        ANNUAL_GAINS_LINE_12: SubtractedLine(
            output=ANNUAL_GAINS_LINE_12,
            minuend=ANNUAL_GAINS_LINE_10,
            minuend_amount=D("10000.00"),
            subtrahend=QBT_TAXABLE_GAINS_RELATED_TO_DEDUCTION,
            subtrahend_amount=D("0"),
            result=D("10000.00"),
        ),
        ANNUAL_GAINS_LINE_7: SubtractedLine(
            output=ANNUAL_GAINS_LINE_7,
            minuend=ANNUAL_GAINS_LINE_5,
            minuend_amount=D("0"),
            subtrahend=QSBCS_QFFP_TAXABLE_GAINS_RELATED_TO_DEDUCTION,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # T2121 Part 4, Part 5, Part 7 and T1 line 26 subtractions: Return A has no fishing
        # statement,
        # so each is 0.
        FISH_REPAIRS_YOUR_COST: SubtractedLine(
            output=FISH_REPAIRS_YOUR_COST,
            minuend=FISH_REPAIRS_TOTAL,
            minuend_amount=D("0"),
            subtrahend=FISH_INSURANCE_RECOVERY,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        FISH_CCA_CLAIM_LESS_PERSONAL_PART: SubtractedLine(
            output=FISH_CCA_CLAIM_LESS_PERSONAL_PART,
            minuend=FISH_CCA_TABLE_CLAIM,
            minuend_amount=D("0"),
            subtrahend=FISH_CCA_PERSONAL_PART,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        FISH_CCA_CLAIM: SubtractedLine(
            output=FISH_CCA_CLAIM,
            minuend=FISH_CCA_CLAIM_LESS_PERSONAL_PART,
            minuend_amount=D("0"),
            subtrahend=FISH_HOME_CCA,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        FISH_NET_INCOME_BEFORE_ADJUSTMENTS: SubtractedLine(
            output=FISH_NET_INCOME_BEFORE_ADJUSTMENTS,
            minuend=FISH_GROSS_INCOME_BEFORE_EXPENSES,
            minuend_amount=D("0"),
            subtrahend=FISH_TOTAL_EXPENSES,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        FISH_NET_INCOME_AFTER_ADJUSTMENTS: SubtractedLine(
            output=FISH_NET_INCOME_AFTER_ADJUSTMENTS,
            minuend=FISH_PARTNERSHIP_TOTAL,
            minuend_amount=D("0"),
            subtrahend=FISH_PARTNER_OTHER_AMOUNTS,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        FISH_HOME_EXPENSES_BUSINESS_PART: SubtractedLine(
            output=FISH_HOME_EXPENSES_BUSINESS_PART,
            minuend=FISH_HOME_EXPENSES_SUBTOTAL,
            minuend_amount=D("0"),
            subtrahend=FISH_HOME_PERSONAL_USE_PART,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        FISHING_INCOME: SubtractedLine(
            output=FISHING_INCOME,
            minuend=FISH_NET_INCOME_AFTER_ADJUSTMENTS,
            minuend_amount=D("0"),
            subtrahend=FISH_HOME_EXPENSES,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Form T691 Part 1 "Amount A minus Amount B": A is line 12000 of the return, 0, and B is
        # line 12010 of the return, 0.
        AMT_AMOUNT_A_MINUS_AMOUNT_B: SubtractedLine(
            output=AMT_AMOUNT_A_MINUS_AMOUNT_B,
            minuend=TAXABLE_DIVIDENDS,
            minuend_amount=D("0"),
            subtrahend=TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Form T691 Part 1 line 91 "line 89 minus line 90": 0 less the amount from line 25395, 0.
        AMT_QBT_CAPITAL_GAINS_DEDUCTION_DIFFERENCE: SubtractedLine(
            output=AMT_QBT_CAPITAL_GAINS_DEDUCTION_DIFFERENCE,
            minuend=AMT_QBT_CAPITAL_GAINS_DEDUCTION_DOUBLED,
            minuend_amount=D("0"),
            subtrahend=QBT_CAPITAL_GAINS_DEDUCTION,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
    }
    assert tapered == {
        BASIC_PERSONAL_AMOUNT: TaperedAmountLine(
            output=BASIC_PERSONAL_AMOUNT,
            base=TOSI_ADJUSTED_NET_INCOME_NOT_BELOW_ZERO,
            base_amount=D("115000"),
            taper=Taper(
                base=D("14538"), supplement=D("1591"), threshold=D("177882"), range=D("75532")
            ),
            rounding=CENT,
            reduction=ExactFraction(0),
            result=D("16129.00"),
        )
    }
    assert gated == {
        # Federal Worksheet "Line 45200 - Refundable medical expense supplement" (T1 line 154),
        # Return A: line 21500 and line 33200 are 0, so line 11 and line 13 are 0.
        MEDICAL_SUPPLEMENT_IF_WORKING_INCOME_MET: ThresholdGateLine(
            output=MEDICAL_SUPPLEMENT_IF_WORKING_INCOME_MET,
            amount_kind=MEDICAL_SUPPLEMENT_LINE_16,
            amount_value=D("0"),
            gate_kind=MEDICAL_SUPPLEMENT_WORKING_INCOME,
            gate_value=D("108000"),
            threshold=Amount(D("4390")),
            rounding=CENT,
            result=D("0.00"),
        ),
    }
    assert amounts == {
        # Form T657 Chart 2016 Part 1 amount A: "Maximum capital gains deduction for QFFP and/or
        # QSBCS
        # disposed of in 2016" 412,088.00.
        CHART_2016_PART_1_AMOUNT_A: CreditAmountLine(
            output=CHART_2016_PART_1_AMOUNT_A,
            basis=Credit(amount=D("412088")),
            rounding=CENT,
            value=D("412088.00"),
        ),
        # Form T657 Chart 2016 Part 2 amount A: "Maximum capital gains deduction for QFFP disposed
        # of in
        # 2016" 500,000.00.
        CHART_2016_PART_2_AMOUNT_A: CreditAmountLine(
            output=CHART_2016_PART_2_AMOUNT_A,
            basis=Credit(amount=D("500000")),
            rounding=CENT,
            value=D("500000.00"),
        ),
        # Form T657 Chart 2017 Part 1 amount A: "Maximum capital gains deduction for QFFP and/or
        # QSBCS
        # disposed of in 2017" 417,858.00.
        CHART_2017_PART_1_AMOUNT_A: CreditAmountLine(
            output=CHART_2017_PART_1_AMOUNT_A,
            basis=Credit(amount=D("417858")),
            rounding=CENT,
            value=D("417858.00"),
        ),
        # Form T657 Chart 2017 Part 2 amount A: "Maximum capital gains deduction for QFFP disposed
        # of in
        # 2017" 500,000.00.
        CHART_2017_PART_2_AMOUNT_A: CreditAmountLine(
            output=CHART_2017_PART_2_AMOUNT_A,
            basis=Credit(amount=D("500000")),
            rounding=CENT,
            value=D("500000.00"),
        ),
        # Form T657 Chart 2018 Part 1 amount A: "Maximum capital gains deduction for QFFP and/or
        # QSBCS
        # disposed of in 2018" 424,126.00.
        CHART_2018_PART_1_AMOUNT_A: CreditAmountLine(
            output=CHART_2018_PART_1_AMOUNT_A,
            basis=Credit(amount=D("424126")),
            rounding=CENT,
            value=D("424126.00"),
        ),
        # Form T657 Chart 2018 Part 2 amount A: "Maximum capital gains deduction for QFFP disposed
        # of in
        # 2018" 500,000.00.
        CHART_2018_PART_2_AMOUNT_A: CreditAmountLine(
            output=CHART_2018_PART_2_AMOUNT_A,
            basis=Credit(amount=D("500000")),
            rounding=CENT,
            value=D("500000.00"),
        ),
        # Form T657 Chart 2019 Part 1 amount A: "Maximum capital gains deduction for QFFP and/or
        # QSBCS
        # disposed of in 2019" 433,456.00.
        CHART_2019_PART_1_AMOUNT_A: CreditAmountLine(
            output=CHART_2019_PART_1_AMOUNT_A,
            basis=Credit(amount=D("433456")),
            rounding=CENT,
            value=D("433456.00"),
        ),
        # Form T657 Chart 2019 Part 2 amount A: "Maximum capital gains deduction for QFFP disposed
        # of in
        # 2019" 500,000.00.
        CHART_2019_PART_2_AMOUNT_A: CreditAmountLine(
            output=CHART_2019_PART_2_AMOUNT_A,
            basis=Credit(amount=D("500000")),
            rounding=CENT,
            value=D("500000.00"),
        ),
        # Form T657 Chart 2020 Part 1 amount A: "Maximum capital gains deduction for QFFP and/or
        # QSBCS
        # disposed of in 2020" 441,692.00.
        CHART_2020_PART_1_AMOUNT_A: CreditAmountLine(
            output=CHART_2020_PART_1_AMOUNT_A,
            basis=Credit(amount=D("441692")),
            rounding=CENT,
            value=D("441692.00"),
        ),
        # Form T657 Chart 2020 Part 2 amount A: "Maximum capital gains deduction for QFFP disposed
        # of in
        # 2020" 500,000.00.
        CHART_2020_PART_2_AMOUNT_A: CreditAmountLine(
            output=CHART_2020_PART_2_AMOUNT_A,
            basis=Credit(amount=D("500000")),
            rounding=CENT,
            value=D("500000.00"),
        ),
        # Schedule 8 Part 3b line 32 "enter "0"": the form's "0", claimed whole.
        CPP_ZERO: CreditAmountLine(CPP_ZERO, Credit(amount=D("0")), CENT, D("0")),
        # Form T2125 Chart B line 18 and Chart C line 25 "÷ 30": the printed constants, each a
        # dataset of the same name, claimed whole to the cent.
        BUSINESS_VEHICLE_INTEREST_LIMIT: CreditAmountLine(
            BUSINESS_VEHICLE_INTEREST_LIMIT, Credit(amount=D("350.00")), CENT, D("350.00")
        ),
        BUSINESS_VEHICLE_DAYS_DIVISOR: CreditAmountLine(
            BUSINESS_VEHICLE_DAYS_DIVISOR, Credit(amount=D("30.00")), CENT, D("30.00")
        ),
        BUSINESS_VEHICLE_LIST_PRICE_LIMIT: CreditAmountLine(
            BUSINESS_VEHICLE_LIST_PRICE_LIMIT, Credit(amount=D("44706.00")), CENT, D("44706.00")
        ),
        BUSINESS_VEHICLE_LEASE_CHARGE_LIMIT: CreditAmountLine(
            BUSINESS_VEHICLE_LEASE_CHARGE_LIMIT, Credit(amount=D("1100.00")), CENT, D("1100.00")
        ),
        BUSINESS_VEHICLE_LEASE_COST_LIMIT: CreditAmountLine(
            BUSINESS_VEHICLE_LEASE_COST_LIMIT, Credit(amount=D("38000.00")), CENT, D("38000.00")
        ),
        # Form T657 Chart 2021 Part 1 amount A: "Maximum capital gains deduction for QFFP and/or
        # QSBCS disposed of in 2021" 446,109.00.
        CHART_2021_PART_1_AMOUNT_A: CreditAmountLine(
            output=CHART_2021_PART_1_AMOUNT_A,
            basis=Credit(amount=D("446109")),
            rounding=CENT,
            value=D("446109.00"),
        ),
        # Form T657 Chart 2021 Part 2 amount A: "Maximum capital gains deduction for QFFP
        # disposed of in 2021" 500,000.00.
        CHART_2021_PART_2_AMOUNT_A: CreditAmountLine(
            output=CHART_2021_PART_2_AMOUNT_A,
            basis=Credit(amount=D("500000")),
            rounding=CENT,
            value=D("500000.00"),
        ),
        # Form T657 Chart 2022 Part 1 amount A: "Maximum capital gains deduction for QFFP and/or
        # QSBCS disposed of in 2022" 456,815.00.
        CHART_2022_PART_1_AMOUNT_A: CreditAmountLine(
            output=CHART_2022_PART_1_AMOUNT_A,
            basis=Credit(amount=D("456815")),
            rounding=CENT,
            value=D("456815.00"),
        ),
        # Form T657 Chart 2022 Part 2 amount A: "Maximum capital gains deduction for QFFP
        # disposed of in 2022" 500,000.00.
        CHART_2022_PART_2_AMOUNT_A: CreditAmountLine(
            output=CHART_2022_PART_2_AMOUNT_A,
            basis=Credit(amount=D("500000")),
            rounding=CENT,
            value=D("500000.00"),
        ),
        # Form T657 Chart 2023 Part 1 amount A: "Maximum capital gains deduction for QFFP and/or
        # QSBCS disposed of in 2023" 485,595.00.
        CHART_2023_PART_1_AMOUNT_A: CreditAmountLine(
            output=CHART_2023_PART_1_AMOUNT_A,
            basis=Credit(amount=D("485595")),
            rounding=CENT,
            value=D("485595.00"),
        ),
        # Form T657 Chart 2023 Part 2 amount A: "Maximum capital gains deduction for QFFP
        # disposed of in 2023" 500,000.00.
        CHART_2023_PART_2_AMOUNT_A: CreditAmountLine(
            output=CHART_2023_PART_2_AMOUNT_A,
            basis=Credit(amount=D("500000")),
            rounding=CENT,
            value=D("500000.00"),
        ),
        # Form T657 Chart 2024 Period 1 amount A: "Maximum capital gains deduction for QFFP and/or
        # QSBCS disposed of in 2024 for Period 1" 508,418.00.
        CHART_2024_PERIOD_1_AMOUNT_A: CreditAmountLine(
            output=CHART_2024_PERIOD_1_AMOUNT_A,
            basis=Credit(amount=D("508418")),
            rounding=CENT,
            value=D("508418.00"),
        ),
        # Form T657 Chart 2024 Period 2 amount A: "Maximum capital gains deduction for QFFP and/or
        # QSBCS disposed of in 2024 for Period 2" 625,000.00.
        CHART_2024_PERIOD_2_AMOUNT_A: CreditAmountLine(
            output=CHART_2024_PERIOD_2_AMOUNT_A,
            basis=Credit(amount=D("625000")),
            rounding=CENT,
            value=D("625000.00"),
        ),
        ontario.DISABILITY_SELF_BASE_AMOUNT: CreditAmountLine(
            ontario.DISABILITY_SELF_BASE_AMOUNT, Credit(amount=D("10298.00")), CENT, D("10298.00")
        ),
        ontario.DISABILITY_SELF_CARE_THRESHOLD: CreditAmountLine(
            ontario.DISABILITY_SELF_CARE_THRESHOLD, Credit(amount=D("3518.00")), CENT, D("3518.00")
        ),
        ontario.DISABILITY_SELF_SUPPLEMENT_MAXIMUM: CreditAmountLine(
            ontario.DISABILITY_SELF_SUPPLEMENT_MAXIMUM,
            Credit(amount=D("6007.00")),
            CENT,
            D("6007.00"),
        ),
        DISABILITY_SELF_BASE_AMOUNT: CreditAmountLine(
            DISABILITY_SELF_BASE_AMOUNT, Credit(amount=D("10138.00")), CENT, D("10138.00")
        ),
        DISABILITY_SELF_CARE_THRESHOLD: CreditAmountLine(
            DISABILITY_SELF_CARE_THRESHOLD, Credit(amount=D("3464.00")), CENT, D("3464.00")
        ),
        DISABILITY_SELF_SUPPLEMENT_MAXIMUM: CreditAmountLine(
            DISABILITY_SELF_SUPPLEMENT_MAXIMUM, Credit(amount=D("5914.00")), CENT, D("5914.00")
        ),
        # Federal Worksheet "Line 23500" line 16 "OAS benefits base amount 93,343.00".
        OAS_BENEFITS_BASE_AMOUNT: CreditAmountLine(
            OAS_BENEFITS_BASE_AMOUNT, Credit(amount=D("93343.00")), CENT, D("93343.00")
        ),
        # Form T1172 line 4 "Maximum lifetime RRSP contribution limit ... $ 50,000.00".
        RESP_AIPS_LIFETIME_LIMIT: CreditAmountLine(
            RESP_AIPS_LIFETIME_LIMIT, Credit(amount=D("50000.00")), CENT, D("50000.00")
        ),
        ontario.BASIC_PERSONAL_AMOUNT: CreditAmountLine(
            ontario.BASIC_PERSONAL_AMOUNT, Credit(amount=D("12747")), CENT, D("12747")
        ),
        TAX_REDUCTION_BASIC: CreditAmountLine(
            TAX_REDUCTION_BASIC, Credit(amount=D("294.00")), CENT, D("294.00")
        ),
        # Federal Worksheet line 1 "Maximum amount 9,028.00" and Schedule 5 line 1 of the line
        # 30425 part "Base amount 28,798.00".
        AGE_MAXIMUM: CreditAmountLine(AGE_MAXIMUM, Credit(amount=D("9028.00")), CENT, D("9028.00")),
        # Federal Worksheet line 3 "Income threshold 45,522.00".
        AGE_INCOME_THRESHOLD: CreditAmountLine(
            AGE_INCOME_THRESHOLD, Credit(amount=D("45522.00")), CENT, D("45522.00")
        ),
        SPOUSE_CAREGIVER_BASE: CreditAmountLine(
            SPOUSE_CAREGIVER_BASE, Credit(amount=D("28798.00")), CENT, D("28798.00")
        ),
        # Worksheet ON428 line 1 "Maximum amount 6,223.00" and line 3 "Income threshold
        # 46,330.00".
        ontario.AGE_MAXIMUM: CreditAmountLine(
            ontario.AGE_MAXIMUM, Credit(amount=D("6223.00")), CENT, D("6223.00")
        ),
        ontario.AGE_INCOME_THRESHOLD: CreditAmountLine(
            ontario.AGE_INCOME_THRESHOLD, Credit(amount=D("46330.00")), CENT, D("46330.00")
        ),
        # ON428 line 11 "Base amount 11,905.00".
        ontario.SPOUSE_BASE: CreditAmountLine(
            ontario.SPOUSE_BASE, Credit(amount=D("11905.00")), CENT, D("11905.00")
        ),
        # Schedule ON428-A line 31 "Individual income threshold 32,500.00" and line 36 "Family
        # income threshold 65,0000.00", a typo for 65,000.00.
        ontario.LIFT_INDIVIDUAL_INCOME_THRESHOLD: CreditAmountLine(
            ontario.LIFT_INDIVIDUAL_INCOME_THRESHOLD,
            Credit(amount=D("32500.00")),
            CENT,
            D("32500.00"),
        ),
        ontario.LIFT_FAMILY_INCOME_THRESHOLD: CreditAmountLine(
            ontario.LIFT_FAMILY_INCOME_THRESHOLD,
            Credit(amount=D("65000.00")),
            CENT,
            D("65000.00"),
        ),
        # ON428 line 14 "Base amount 11,905.00".
        ELIGIBLE_DEPENDANT_BASE: CreditAmountLine(
            ELIGIBLE_DEPENDANT_BASE, Credit(amount=D("11905.00")), CENT, D("11905.00")
        ),
        # Schedule 9 line 13 "$200" and line 18 "Income threshold 253,414.00"; Federal Worksheet
        # line 4 "8,319.38": each claimed whole.
        DONATION_FIRST_TIER_MAXIMUM: CreditAmountLine(
            DONATION_FIRST_TIER_MAXIMUM, Credit(amount=D("200")), CENT, D("200.00")
        ),
        DONATION_HIGH_INCOME_THRESHOLD: CreditAmountLine(
            DONATION_HIGH_INCOME_THRESHOLD, Credit(amount=D("253414.00")), CENT, D("253414.00")
        ),
        TOP_UP_THRESHOLD: CreditAmountLine(
            TOP_UP_THRESHOLD, Credit(amount=D("8319.38")), CENT, D("8319.38")
        ),
        # Schedule 15 line 14.
        FHSA_ANNUAL_AMOUNT: CreditAmountLine(
            FHSA_ANNUAL_AMOUNT, Credit(amount=D("8000.00")), CENT, D("8000.00")
        ),
        # Schedule 15 line 30.
        FHSA_ANNUAL_AMOUNT_FOR_2024: CreditAmountLine(
            FHSA_ANNUAL_AMOUNT_FOR_2024, Credit(amount=D("8000.00")), CENT, D("8000.00")
        ),
        # Schedule 15 Step 2's printed "0".
        FHSA_ANNUAL_LIMIT_AFTER_MAXIMUM_PARTICIPATION_PERIOD: CreditAmountLine(
            FHSA_ANNUAL_LIMIT_AFTER_MAXIMUM_PARTICIPATION_PERIOD,
            Credit(amount=D("0")),
            CENT,
            D("0.00"),
        ),
        # Schedule 15 line 46.
        FHSA_LIFETIME_LIMIT: CreditAmountLine(
            FHSA_LIFETIME_LIMIT, Credit(amount=D("40000.00")), CENT, D("40000.00")
        ),
        # Worksheet ON479 column 1 line 2: 0.00, a printed constant.
        ontario.POLITICAL_CREDIT_COLUMN_1_LINE_2: CreditAmountLine(
            ontario.POLITICAL_CREDIT_COLUMN_1_LINE_2, Credit(amount=D("0.00")), CENT, D("0.00")
        ),
        # Worksheet ON479 column 1 line 6: 0.00, a printed constant.
        ontario.POLITICAL_CREDIT_COLUMN_1_LINE_6: CreditAmountLine(
            ontario.POLITICAL_CREDIT_COLUMN_1_LINE_6, Credit(amount=D("0.00")), CENT, D("0.00")
        ),
        # Worksheet ON479 column 2 line 2: 500.05, a printed constant.
        ontario.POLITICAL_CREDIT_COLUMN_2_LINE_2: CreditAmountLine(
            ontario.POLITICAL_CREDIT_COLUMN_2_LINE_2, Credit(amount=D("500.05")), CENT, D("500.05")
        ),
        # Worksheet ON479 column 2 line 6: 375.03, a printed constant.
        ontario.POLITICAL_CREDIT_COLUMN_2_LINE_6: CreditAmountLine(
            ontario.POLITICAL_CREDIT_COLUMN_2_LINE_6, Credit(amount=D("375.03")), CENT, D("375.03")
        ),
        # Worksheet ON479 column 3 line 2: 1666.82, a printed constant.
        ontario.POLITICAL_CREDIT_COLUMN_3_LINE_2: CreditAmountLine(
            ontario.POLITICAL_CREDIT_COLUMN_3_LINE_2,
            Credit(amount=D("1666.82")),
            CENT,
            D("1666.82"),
        ),
        # Worksheet ON479 column 3 line 6: 958.41, a printed constant.
        ontario.POLITICAL_CREDIT_COLUMN_3_LINE_6: CreditAmountLine(
            ontario.POLITICAL_CREDIT_COLUMN_3_LINE_6, Credit(amount=D("958.41")), CENT, D("958.41")
        ),
        # Federal Worksheet column 1 line 2: 0.00, a printed constant.
        POLITICAL_CREDIT_COLUMN_1_LINE_2: CreditAmountLine(
            POLITICAL_CREDIT_COLUMN_1_LINE_2, Credit(amount=D("0.00")), CENT, D("0.00")
        ),
        # Federal Worksheet column 1 line 6: 0.00, a printed constant.
        POLITICAL_CREDIT_COLUMN_1_LINE_6: CreditAmountLine(
            POLITICAL_CREDIT_COLUMN_1_LINE_6, Credit(amount=D("0.00")), CENT, D("0.00")
        ),
        # Federal Worksheet column 2 line 2: 400.00, a printed constant.
        POLITICAL_CREDIT_COLUMN_2_LINE_2: CreditAmountLine(
            POLITICAL_CREDIT_COLUMN_2_LINE_2, Credit(amount=D("400.00")), CENT, D("400.00")
        ),
        # Federal Worksheet column 2 line 6: 300.00, a printed constant.
        POLITICAL_CREDIT_COLUMN_2_LINE_6: CreditAmountLine(
            POLITICAL_CREDIT_COLUMN_2_LINE_6, Credit(amount=D("300.00")), CENT, D("300.00")
        ),
        # Federal Worksheet column 3 line 2: 750.00, a printed constant.
        POLITICAL_CREDIT_COLUMN_3_LINE_2: CreditAmountLine(
            POLITICAL_CREDIT_COLUMN_3_LINE_2, Credit(amount=D("750.00")), CENT, D("750.00")
        ),
        # Federal Worksheet column 3 line 6: 475.00, a printed constant.
        POLITICAL_CREDIT_COLUMN_3_LINE_6: CreditAmountLine(
            POLITICAL_CREDIT_COLUMN_3_LINE_6, Credit(amount=D("475.00")), CENT, D("475.00")
        ),
        # Federal Worksheet shortcut "$1,275 or more": the printed threshold.
        POLITICAL_CREDIT_SHORTCUT_THRESHOLD: CreditAmountLine(
            POLITICAL_CREDIT_SHORTCUT_THRESHOLD, Credit(amount=D("1275")), CENT, D("1275")
        ),
        # Federal Worksheet shortcut "enter $650 on line 41000": the printed amount.
        POLITICAL_CREDIT_SHORTCUT_AMOUNT: CreditAmountLine(
            POLITICAL_CREDIT_SHORTCUT_AMOUNT, Credit(amount=D("650")), CENT, D("650")
        ),
        # ON479 line 9 "Base amount 35,000.00".
        SENIORS_CARE_BASE_AMOUNT: CreditAmountLine(
            SENIORS_CARE_BASE_AMOUNT, Credit(amount=D("35000.00")), CENT, D("35000.00")
        ),
        # Worksheet ON479 "Line 20" line 5 "400,000.00", line 7 "200,000.00" and line 9 "1.00".
        COOP_EDUCATION_PAYROLL_THRESHOLD: CreditAmountLine(
            COOP_EDUCATION_PAYROLL_THRESHOLD, Credit(amount=D("400000.00")), CENT, D("400000.00")
        ),
        COOP_EDUCATION_PAYROLL_RANGE: CreditAmountLine(
            COOP_EDUCATION_PAYROLL_RANGE, Credit(amount=D("200000.00")), CENT, D("200000.00")
        ),
        COOP_EDUCATION_FULL_SHARE: CreditAmountLine(
            COOP_EDUCATION_FULL_SHARE, Credit(amount=D("1.00")), CENT, D("1.00")
        ),
        # Federal Worksheet "Line 45200 - Refundable medical expense supplement" (T1 line 154),
        # Return A: line 21500 and line 33200 are 0, so line 11 and line 13 are 0.
        MEDICAL_SUPPLEMENT_INCOME_THRESHOLD: CreditAmountLine(
            output=MEDICAL_SUPPLEMENT_INCOME_THRESHOLD,
            basis=Credit(amount=D("33294.00")),
            rounding=CENT,
            value=D("33294.00"),
        ),
        # Schedule 13 line 5 "Maximum insurable earnings 65,700.00".
        EI_MAXIMUM_INSURABLE_EARNINGS: CreditAmountLine(
            EI_MAXIMUM_INSURABLE_EARNINGS, Credit(amount=D("65700.00")), CENT, D("65700.00")
        ),
        # Form T657 (line 25400): Return A enters nothing on it, so its lines are 0 (or,
        # where they read another line, that line's figure).
        CHART_2025_PART_1_AMOUNT_A: CreditAmountLine(
            output=CHART_2025_PART_1_AMOUNT_A,
            basis=Credit(amount=D("522145")),
            rounding=CENT,
            value=D("522145.00"),
        ),
        CHART_2025_PART_2_AMOUNT_A: CreditAmountLine(
            output=CHART_2025_PART_2_AMOUNT_A,
            basis=Credit(amount=D("625000")),
            rounding=CENT,
            value=D("625000.00"),
        ),
        NET_CAPITAL_LOSS_NUMERATOR_ONE_2000: CreditAmountLine(
            output=NET_CAPITAL_LOSS_NUMERATOR_ONE_2000,
            basis=Credit(amount=D("1")),
            rounding=CENT,
            value=D("1.00"),
        ),
        CHART_2_NUMERATOR_ONE: CreditAmountLine(
            output=CHART_2_NUMERATOR_ONE,
            basis=Credit(amount=D("1")),
            rounding=CENT,
            value=D("1.00"),
        ),
        # Form T691 Part 1 line 94 "Basic exemption" 177,882.00, a printed amount.
        AMT_BASIC_EXEMPTION: CreditAmountLine(
            AMT_BASIC_EXEMPTION, Credit(amount=D("177882.00")), CENT, D("177882.00")
        ),
    }
    assert per_unit == {
        # Form T2222 lines 1, 2, 6 and 7 "multiplied by $11.00" and "multiplied by $5.50": Return A
        # has no days.
        ZONE_A_BASIC_RESIDENCY_AMOUNT: PerUnitAmountLine(
            output=ZONE_A_BASIC_RESIDENCY_AMOUNT,
            count_kind=ZONE_A_DAYS_LIVED,
            count=0,
            per_unit=Amount(D("11.00")),
            rounding=CENT,
            result=D("0"),
        ),
        ZONE_A_ADDITIONAL_RESIDENCY_AMOUNT: PerUnitAmountLine(
            output=ZONE_A_ADDITIONAL_RESIDENCY_AMOUNT,
            count_kind=ZONE_A_ADDITIONAL_RESIDENCY_DAYS,
            count=0,
            per_unit=Amount(D("11.00")),
            rounding=CENT,
            result=D("0"),
        ),
        ZONE_B_BASIC_RESIDENCY_AMOUNT: PerUnitAmountLine(
            output=ZONE_B_BASIC_RESIDENCY_AMOUNT,
            count_kind=ZONE_B_DAYS_LIVED,
            count=0,
            per_unit=Amount(D("5.50")),
            rounding=CENT,
            result=D("0"),
        ),
        ZONE_B_ADDITIONAL_RESIDENCY_AMOUNT: PerUnitAmountLine(
            output=ZONE_B_ADDITIONAL_RESIDENCY_AMOUNT,
            count_kind=ZONE_B_ADDITIONAL_RESIDENCY_DAYS,
            count=0,
            per_unit=Amount(D("5.50")),
            rounding=CENT,
            result=D("0"),
        ),
        TAX_REDUCTION_FOR_CHILDREN_BEFORE_SPOUSE_RULE: PerUnitAmountLine(
            output=TAX_REDUCTION_FOR_CHILDREN_BEFORE_SPOUSE_RULE,
            count_kind=DEPENDENT_CHILDREN,
            count=0,
            per_unit=Amount(D("544")),
            rounding=CENT,
            result=D("0"),
        ),
        TAX_REDUCTION_FOR_DEPENDANTS_BEFORE_SPOUSE_RULE: PerUnitAmountLine(
            output=TAX_REDUCTION_FOR_DEPENDANTS_BEFORE_SPOUSE_RULE,
            count_kind=DEPENDANTS,
            count=0,
            per_unit=Amount(D("544")),
            rounding=CENT,
            result=D("0"),
        ),
        # Schedule 5 line 2 (line 51090) "enter $2,687" for each spouse eligible for the Canada
        # caregiver amount: Return A has none.
        SPOUSE_INFIRMITY_SUPPLEMENT: PerUnitAmountLine(
            output=SPOUSE_INFIRMITY_SUPPLEMENT,
            count_kind=SPOUSE_CAREGIVER_ELIGIBLE,
            count=0,
            per_unit=Amount(D("2687")),
            rounding=CENT,
            result=D("0"),
        ),
        # T1 line 30500 "Number of children you are claiming this amount for Line 30499"
        # "multiplied by $2,687": Return A has no infirm child.
        INFIRM_CHILDREN_AMOUNT: PerUnitAmountLine(
            output=INFIRM_CHILDREN_AMOUNT,
            count_kind=INFIRM_CHILDREN,
            count=0,
            per_unit=Amount(D("2687")),
            rounding=CENT,
            result=D("0"),
        ),
        # Form T778 Part B lines 1 to 3, "multiplied by $8,000", "$11,000" and "$5,000": Return A
        # has no eligible child.
        CHILD_CARE_LIMIT_FOR_CHILDREN_UNDER_SEVEN: PerUnitAmountLine(
            output=CHILD_CARE_LIMIT_FOR_CHILDREN_UNDER_SEVEN,
            count_kind=CHILDREN_UNDER_SEVEN,
            count=0,
            per_unit=Amount(D("8000")),
            rounding=CENT,
            result=D("0"),
        ),
        CHILD_CARE_LIMIT_FOR_CHILDREN_WITH_DISABILITY: PerUnitAmountLine(
            output=CHILD_CARE_LIMIT_FOR_CHILDREN_WITH_DISABILITY,
            count_kind=CHILDREN_WITH_DISABILITY,
            count=0,
            per_unit=Amount(D("11000")),
            rounding=CENT,
            result=D("0"),
        ),
        CHILD_CARE_LIMIT_FOR_CHILDREN_SEVEN_TO_SIXTEEN: PerUnitAmountLine(
            output=CHILD_CARE_LIMIT_FOR_CHILDREN_SEVEN_TO_SIXTEEN,
            count_kind=CHILDREN_SEVEN_TO_SIXTEEN,
            count=0,
            per_unit=Amount(D("5000")),
            rounding=CENT,
            result=D("0"),
        ),
    }
    assert fractions == {
        # Schedule 8 Part 5 line 48 "multiplied by 2": 0 x 2 for Return A.
        CPP_PART_5_LINE_48: FractionAppliedLine(
            output=CPP_PART_5_LINE_48,
            base=CPP_PART_5_LINE_48_LINE_24_IF_POSITIVE,
            base_amount=D("0"),
            fraction=Fraction(2, 1),
            rounding=CENT,
            result=D("0.00"),
        ),
        # Schedule 8 Part 5 line 20 "Amount from line 10 multiplied by 16.80672": 4,034.10 x
        # 16.80672 = 67,799.989152, to the cent 67,799.99 for Return A.
        CPP_PART_5_LINE_20: FractionAppliedLine(
            output=CPP_PART_5_LINE_20,
            base=CPP_PART_5_LINE_10,
            base_amount=D("4034.10"),
            fraction=Fraction(1680672, 100000),
            rounding=CENT,
            result=D("67799.99"),
        ),
        # Form T657 Chart 2016 Part 1 "× 1/2 = F": amounts D and E of 0, times 1/2.
        CHART_2016_PART_1_AMOUNT_F: FractionAppliedLine(
            output=CHART_2016_PART_1_AMOUNT_F,
            base=CHART_2016_PART_1_AMOUNTS_D_AND_E,
            base_amount=D("0"),
            fraction=Fraction(1, 2),
            rounding=CENT,
            result=D("0"),
        ),
        # Form T657 Chart 2016 Part 2 "× 1/2 = F": the T2017 line 6 amount of 0, times 1/2.
        CHART_2016_PART_2_AMOUNT_F: FractionAppliedLine(
            output=CHART_2016_PART_2_AMOUNT_F,
            base=T657_CHART_2016_AMOUNT_D,
            base_amount=D("0"),
            fraction=Fraction(1, 2),
            rounding=CENT,
            result=D("0"),
        ),
        # Form T657 Chart 2017 Part 1 "× 1/2 = H": amounts F and G of 0, times 1/2.
        CHART_2017_PART_1_AMOUNT_H: FractionAppliedLine(
            output=CHART_2017_PART_1_AMOUNT_H,
            base=CHART_2017_PART_1_AMOUNTS_F_AND_G,
            base_amount=D("0"),
            fraction=Fraction(1, 2),
            rounding=CENT,
            result=D("0"),
        ),
        # Form T657 Chart 2017 Part 2 "× 1/2 = F": the T2017 line 6 amount of 0, times 1/2.
        CHART_2017_PART_2_AMOUNT_F: FractionAppliedLine(
            output=CHART_2017_PART_2_AMOUNT_F,
            base=T657_CHART_2017_AMOUNT_F,
            base_amount=D("0"),
            fraction=Fraction(1, 2),
            rounding=CENT,
            result=D("0"),
        ),
        # Form T657 Chart 2018 Part 1 "× 1/2 = H": amounts F and G of 0, times 1/2.
        CHART_2018_PART_1_AMOUNT_H: FractionAppliedLine(
            output=CHART_2018_PART_1_AMOUNT_H,
            base=CHART_2018_PART_1_AMOUNTS_F_AND_G,
            base_amount=D("0"),
            fraction=Fraction(1, 2),
            rounding=CENT,
            result=D("0"),
        ),
        # Form T657 Chart 2018 Part 2 "× 1/2 = F": the T2017 line 6 amount of 0, times 1/2.
        CHART_2018_PART_2_AMOUNT_F: FractionAppliedLine(
            output=CHART_2018_PART_2_AMOUNT_F,
            base=T657_CHART_2018_AMOUNT_F,
            base_amount=D("0"),
            fraction=Fraction(1, 2),
            rounding=CENT,
            result=D("0"),
        ),
        # Form T657 Chart 2019 Part 1 "× 1/2 = H": amounts F and G of 0, times 1/2.
        CHART_2019_PART_1_AMOUNT_H: FractionAppliedLine(
            output=CHART_2019_PART_1_AMOUNT_H,
            base=CHART_2019_PART_1_AMOUNTS_F_AND_G,
            base_amount=D("0"),
            fraction=Fraction(1, 2),
            rounding=CENT,
            result=D("0"),
        ),
        # Form T657 Chart 2019 Part 2 "× 1/2 = F": the T2017 line 6 amount of 0, times 1/2.
        CHART_2019_PART_2_AMOUNT_F: FractionAppliedLine(
            output=CHART_2019_PART_2_AMOUNT_F,
            base=T657_CHART_2019_AMOUNT_F,
            base_amount=D("0"),
            fraction=Fraction(1, 2),
            rounding=CENT,
            result=D("0"),
        ),
        # Form T657 Chart 2020 Part 1 "× 1/2 = H": amounts F and G of 0, times 1/2.
        CHART_2020_PART_1_AMOUNT_H: FractionAppliedLine(
            output=CHART_2020_PART_1_AMOUNT_H,
            base=CHART_2020_PART_1_AMOUNTS_F_AND_G,
            base_amount=D("0"),
            fraction=Fraction(1, 2),
            rounding=CENT,
            result=D("0"),
        ),
        # Form T657 Chart 2020 Part 2 "× 1/2 = F": the T2017 line 6 amount of 0, times 1/2.
        CHART_2020_PART_2_AMOUNT_F: FractionAppliedLine(
            output=CHART_2020_PART_2_AMOUNT_F,
            base=T657_CHART_2020_AMOUNT_F,
            base_amount=D("0"),
            fraction=Fraction(1, 2),
            rounding=CENT,
            result=D("0"),
        ),
        # Form T657 Chart 2021 Part 1 "× 1/2 = H": amounts F and G of 0, times 1/2.
        CHART_2021_PART_1_AMOUNT_H: FractionAppliedLine(
            output=CHART_2021_PART_1_AMOUNT_H,
            base=CHART_2021_PART_1_AMOUNTS_F_AND_G,
            base_amount=D("0"),
            fraction=Fraction(1, 2),
            rounding=CENT,
            result=D("0.00"),
        ),
        # Form T657 Chart 2021 Part 1 box 30 "× 1/2 = +" I: the amount of 0, times 1/2.
        CHART_2021_PART_1_AMOUNT_I: FractionAppliedLine(
            output=CHART_2021_PART_1_AMOUNT_I,
            base=T657_CHART_2021_AMOUNT_I,
            base_amount=D("0"),
            fraction=Fraction(1, 2),
            rounding=CENT,
            result=D("0.00"),
        ),
        # Form T657 Chart 2021 Part 2 "× 1/2 = F": the T2017 amount of 0, times 1/2.
        CHART_2021_PART_2_AMOUNT_F: FractionAppliedLine(
            output=CHART_2021_PART_2_AMOUNT_F,
            base=T657_CHART_2021_AMOUNT_F,
            base_amount=D("0"),
            fraction=Fraction(1, 2),
            rounding=CENT,
            result=D("0.00"),
        ),
        # Form T657 Chart 2021 Part 2 box 30 QFFP "× 1/2 = G": the amount of 0, times 1/2.
        CHART_2021_PART_2_AMOUNT_G: FractionAppliedLine(
            output=CHART_2021_PART_2_AMOUNT_G,
            base=T657_CHART_2021_PART_2_AMOUNT_G,
            base_amount=D("0"),
            fraction=Fraction(1, 2),
            rounding=CENT,
            result=D("0.00"),
        ),
        # Form T657 Chart 2022 Part 1 "× 1/2 = H": amounts F and G of 0, times 1/2.
        CHART_2022_PART_1_AMOUNT_H: FractionAppliedLine(
            output=CHART_2022_PART_1_AMOUNT_H,
            base=CHART_2022_PART_1_AMOUNTS_F_AND_G,
            base_amount=D("0"),
            fraction=Fraction(1, 2),
            rounding=CENT,
            result=D("0.00"),
        ),
        # Form T657 Chart 2022 Part 1 box 30 "× 1/2 = +" I: the amount of 0, times 1/2.
        CHART_2022_PART_1_AMOUNT_I: FractionAppliedLine(
            output=CHART_2022_PART_1_AMOUNT_I,
            base=T657_CHART_2022_AMOUNT_I,
            base_amount=D("0"),
            fraction=Fraction(1, 2),
            rounding=CENT,
            result=D("0.00"),
        ),
        # Form T657 Chart 2022 Part 2 "× 1/2 = F": the T2017 amount of 0, times 1/2.
        CHART_2022_PART_2_AMOUNT_F: FractionAppliedLine(
            output=CHART_2022_PART_2_AMOUNT_F,
            base=T657_CHART_2022_AMOUNT_F,
            base_amount=D("0"),
            fraction=Fraction(1, 2),
            rounding=CENT,
            result=D("0.00"),
        ),
        # Form T657 Chart 2022 Part 2 box 30 QFFP "× 1/2 = G": the amount of 0, times 1/2.
        CHART_2022_PART_2_AMOUNT_G: FractionAppliedLine(
            output=CHART_2022_PART_2_AMOUNT_G,
            base=T657_CHART_2022_PART_2_AMOUNT_G,
            base_amount=D("0"),
            fraction=Fraction(1, 2),
            rounding=CENT,
            result=D("0.00"),
        ),
        # Form T657 Chart 2023 Part 1 "× 1/2 = H": amounts F and G of 0, times 1/2.
        CHART_2023_PART_1_AMOUNT_H: FractionAppliedLine(
            output=CHART_2023_PART_1_AMOUNT_H,
            base=CHART_2023_PART_1_AMOUNTS_F_AND_G,
            base_amount=D("0"),
            fraction=Fraction(1, 2),
            rounding=CENT,
            result=D("0.00"),
        ),
        # Form T657 Chart 2023 Part 1 box 30 "× 1/2 = +" I: the amount of 0, times 1/2.
        CHART_2023_PART_1_AMOUNT_I: FractionAppliedLine(
            output=CHART_2023_PART_1_AMOUNT_I,
            base=T657_CHART_2023_AMOUNT_I,
            base_amount=D("0"),
            fraction=Fraction(1, 2),
            rounding=CENT,
            result=D("0.00"),
        ),
        # Form T657 Chart 2023 Part 2 "× 1/2 = F": the T2017 amount of 0, times 1/2.
        CHART_2023_PART_2_AMOUNT_F: FractionAppliedLine(
            output=CHART_2023_PART_2_AMOUNT_F,
            base=T657_CHART_2023_AMOUNT_F,
            base_amount=D("0"),
            fraction=Fraction(1, 2),
            rounding=CENT,
            result=D("0.00"),
        ),
        # Form T657 Chart 2023 Part 2 box 30 QFFP "× 1/2 = G": the amount of 0, times 1/2.
        CHART_2023_PART_2_AMOUNT_G: FractionAppliedLine(
            output=CHART_2023_PART_2_AMOUNT_G,
            base=T657_CHART_2023_PART_2_AMOUNT_G,
            base_amount=D("0"),
            fraction=Fraction(1, 2),
            rounding=CENT,
            result=D("0.00"),
        ),
        # Form T657 Chart 2024 Period 1 "× 1/2 = I": the amounts F to H of 0, times 1/2.
        CHART_2024_PERIOD_1_AMOUNT_I: FractionAppliedLine(
            output=CHART_2024_PERIOD_1_AMOUNT_I,
            base=CHART_2024_PERIOD_1_AMOUNTS_F_TO_H,
            base_amount=D("0"),
            fraction=Fraction(1, 2),
            rounding=CENT,
            result=D("0.00"),
        ),
        # Form T657 Chart 2024 Period 2 "× 1/2 = I": the amounts F to H of 0, times 1/2.
        CHART_2024_PERIOD_2_AMOUNT_I: FractionAppliedLine(
            output=CHART_2024_PERIOD_2_AMOUNT_I,
            base=CHART_2024_PERIOD_2_AMOUNTS_F_TO_H,
            base_amount=D("0"),
            fraction=Fraction(1, 2),
            rounding=CENT,
            result=D("0.00"),
        ),
        # The Federal Worksheet's lines 13 and 16: 138% and 115% of no dividends with no slip.
        ELIGIBLE_DIVIDENDS_GROSSED_UP: FractionAppliedLine(
            output=ELIGIBLE_DIVIDENDS_GROSSED_UP,
            base=ELIGIBLE_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP,
            base_amount=D("0"),
            fraction=Fraction(138, 100),
            rounding=CENT,
            result=D("0"),
        ),
        OTHER_DIVIDENDS_GROSSED_UP: FractionAppliedLine(
            output=OTHER_DIVIDENDS_GROSSED_UP,
            base=OTHER_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP,
            base_amount=D("0"),
            fraction=Fraction(115, 100),
            rounding=CENT,
            result=D("0"),
        ),
        # Form T691 Part 1 line 89 "× 2" of the amount from line 25395 of the return, 0.
        AMT_QBT_CAPITAL_GAINS_DEDUCTION_DOUBLED: FractionAppliedLine(
            output=AMT_QBT_CAPITAL_GAINS_DEDUCTION_DOUBLED,
            base=QBT_CAPITAL_GAINS_DEDUCTION,
            base_amount=D("0"),
            fraction=Fraction(2, 1),
            rounding=CENT,
            result=D("0"),
        ),
        CHILD_CARE_EARNED_INCOME_LIMIT: FractionAppliedLine(
            output=CHILD_CARE_EARNED_INCOME_LIMIT,
            base=CHILD_CARE_EARNED_INCOME,
            base_amount=D("110000"),
            fraction=Fraction(2, 3),
            rounding=CENT,
            result=D("73333.33"),
        ),
        # Form T1436 Chart A column C "Adjusted gross capital losses (column A multiplied by column
        # B)" for no unapplied losses, and column G "Net capital loss balance available to carry
        # forward (column E multiplied by column F)" for none remaining, each a fraction of 0.
        # Form T1436 lines 2: "In 1988 and 1989" (B) x 0.75 and "From 1990 to 1999" (C) x 0.6667,
        # each of 0, as exact fractions; column C of the row "Before May 23, 1985" (column A is
        # line 3) and its column G, each factor 1.
        PRE_1986_DEDUCTIONS_ADJUSTED_1988_AND_1989: FractionAppliedLine(
            output=PRE_1986_DEDUCTIONS_ADJUSTED_1988_AND_1989,
            base=PRE_1986_DEDUCTIONS_1988_AND_1989,
            base_amount=D("0"),
            fraction=Fraction(3, 4),
            rounding=CENT,
            result=D("0.00"),
        ),
        PRE_1986_DEDUCTIONS_ADJUSTED_1990_TO_1999: FractionAppliedLine(
            output=PRE_1986_DEDUCTIONS_ADJUSTED_1990_TO_1999,
            base=PRE_1986_DEDUCTIONS_1990_TO_1999,
            base_amount=D("0"),
            fraction=Fraction(2, 3),
            rounding=CENT,
            result=D("0.00"),
        ),
        ADJUSTED_GROSS_CAPITAL_LOSSES_BEFORE_MAY_23_1985: FractionAppliedLine(
            output=ADJUSTED_GROSS_CAPITAL_LOSSES_BEFORE_MAY_23_1985,
            base=PRE_1986_CAPITAL_LOSS_BALANCE,
            base_amount=D("0.00"),
            fraction=Fraction(1, 1),
            rounding=CENT,
            result=D("0.00"),
        ),
        NET_CAPITAL_LOSS_BALANCE_BEFORE_MAY_23_1985: FractionAppliedLine(
            output=NET_CAPITAL_LOSS_BALANCE_BEFORE_MAY_23_1985,
            base=REMAINING_ADJUSTED_LOSSES_BEFORE_MAY_23_1985,
            base_amount=D("0.00"),
            fraction=Fraction(1, 1),
            rounding=CENT,
            result=D("0.00"),
        ),
        ADJUSTED_GROSS_CAPITAL_LOSSES_1985_TO_1987: FractionAppliedLine(
            output=ADJUSTED_GROSS_CAPITAL_LOSSES_1985_TO_1987,
            base=UNAPPLIED_NET_CAPITAL_LOSSES_1985_TO_1987,
            base_amount=D("0"),
            fraction=Fraction(1, 1),
            rounding=CENT,
            result=D("0.00"),
        ),
        ADJUSTED_GROSS_CAPITAL_LOSSES_1988_AND_1989: FractionAppliedLine(
            output=ADJUSTED_GROSS_CAPITAL_LOSSES_1988_AND_1989,
            base=UNAPPLIED_NET_CAPITAL_LOSSES_1988_AND_1989,
            base_amount=D("0"),
            fraction=Fraction(3, 4),
            rounding=CENT,
            result=D("0.00"),
        ),
        ADJUSTED_GROSS_CAPITAL_LOSSES_1990_TO_1999: FractionAppliedLine(
            output=ADJUSTED_GROSS_CAPITAL_LOSSES_1990_TO_1999,
            base=UNAPPLIED_NET_CAPITAL_LOSSES_1990_TO_1999,
            base_amount=D("0"),
            fraction=Fraction(2, 3),
            rounding=CENT,
            result=D("0.00"),
        ),
        ADJUSTED_GROSS_CAPITAL_LOSSES_2001_TO_2024: FractionAppliedLine(
            output=ADJUSTED_GROSS_CAPITAL_LOSSES_2001_TO_2024,
            base=UNAPPLIED_NET_CAPITAL_LOSSES_2001_TO_2024,
            base_amount=D("0"),
            fraction=Fraction(1, 1),
            rounding=CENT,
            result=D("0.00"),
        ),
        NET_CAPITAL_LOSS_BALANCE_1985_TO_1987: FractionAppliedLine(
            output=NET_CAPITAL_LOSS_BALANCE_1985_TO_1987,
            base=REMAINING_ADJUSTED_LOSSES_1985_TO_1987,
            base_amount=D("0.00"),
            fraction=Fraction(1, 1),
            rounding=CENT,
            result=D("0.00"),
        ),
        NET_CAPITAL_LOSS_BALANCE_1988_AND_1989: FractionAppliedLine(
            output=NET_CAPITAL_LOSS_BALANCE_1988_AND_1989,
            base=REMAINING_ADJUSTED_LOSSES_1988_AND_1989,
            base_amount=D("0.00"),
            fraction=Fraction(4, 3),
            rounding=CENT,
            result=D("0.00"),
        ),
        NET_CAPITAL_LOSS_BALANCE_1990_TO_1999: FractionAppliedLine(
            output=NET_CAPITAL_LOSS_BALANCE_1990_TO_1999,
            base=REMAINING_ADJUSTED_LOSSES_1990_TO_1999,
            base_amount=D("0.00"),
            fraction=Fraction(3, 2),
            rounding=CENT,
            result=D("0.00"),
        ),
        NET_CAPITAL_LOSS_BALANCE_2001_TO_2024: FractionAppliedLine(
            output=NET_CAPITAL_LOSS_BALANCE_2001_TO_2024,
            base=REMAINING_ADJUSTED_LOSSES_2001_TO_2024,
            base_amount=D("0.00"),
            fraction=Fraction(1, 1),
            rounding=CENT,
            result=D("0.00"),
        ),
        # Form T657 (line 25400): Return A enters nothing on it, so its lines are 0 (or,
        # where they read another line, that line's figure).
        CHART_2_LINE_12: FractionAppliedLine(
            output=CHART_2_LINE_12,
            base=T657_CHART_2_LINE_10,
            base_amount=D("0"),
            fraction=Fraction(1, 3),
            rounding=CENT,
            result=D("0.00"),
        ),
        NET_CAPITAL_LOSS_TWICE_IR_2000: FractionAppliedLine(
            output=NET_CAPITAL_LOSS_TWICE_IR_2000,
            base=T657_INCLUSION_RATE_2000,
            base_amount=D("0"),
            fraction=Fraction(2, 1),
            rounding=NO_ROUNDING,
            result=D("0"),
        ),
        CHART_2_TWICE_IR: FractionAppliedLine(
            output=CHART_2_TWICE_IR,
            base=T657_INCLUSION_RATE_2000,
            base_amount=D("0"),
            fraction=Fraction(2, 1),
            rounding=NO_ROUNDING,
            result=D("0"),
        ),
        CHART_2_LINE_4: FractionAppliedLine(
            output=CHART_2_LINE_4,
            base=T657_CHART_2_LINE_2,
            base_amount=D("0"),
            fraction=Fraction(1, 4),
            rounding=CENT,
            result=D("0.00"),
        ),
        CHART_2_LINE_8: FractionAppliedLine(
            output=CHART_2_LINE_8,
            base=T657_CHART_2_LINE_6,
            base_amount=D("0"),
            fraction=Fraction(1, 3),
            rounding=CENT,
            result=D("0.00"),
        ),
        ANNUAL_GAINS_LINE_3_AT_INCLUSION_RATE: FractionAppliedLine(
            output=ANNUAL_GAINS_LINE_3_AT_INCLUSION_RATE,
            base=ANNUAL_GAINS_LINE_3,
            base_amount=D("0"),
            fraction=Fraction(1, 2),
            rounding=CENT,
            result=D("0.00"),
        ),
        CHART_2025_PART_1_AMOUNT_K: FractionAppliedLine(
            output=CHART_2025_PART_1_AMOUNT_K,
            base=CHART_2025_PART_1_AMOUNTS_F_TO_J,
            base_amount=D("0"),
            fraction=Fraction(1, 2),
            rounding=CENT,
            result=D("0.00"),
        ),
        CHART_2025_PART_2_AMOUNT_K: FractionAppliedLine(
            output=CHART_2025_PART_2_AMOUNT_K,
            base=CHART_2025_PART_2_AMOUNTS_F_TO_J,
            base_amount=D("0"),
            fraction=Fraction(1, 2),
            rounding=CENT,
            result=D("0.00"),
        ),
        ANNUAL_GAINS_LINE_9: FractionAppliedLine(
            output=ANNUAL_GAINS_LINE_9,
            base=SCHEDULE_3_LINE_17600_NOT_BELOW_ZERO,
            base_amount=D("0"),
            fraction=Fraction(1, 2),
            rounding=CENT,
            result=D("0.00"),
        ),
    }
    assert times == {
        # Form T691 Part 6 line 11, the second branch, "enter the amount from line 9" when "you are
        # a non-resident or deemed resident": line 9, 8136.66, times a count of 0 (Return A is not a
        # non-resident), a plain 0.
        AMT_PART_6_SURTAX_IF_NON_RESIDENT: TimesCountLine(
            output=AMT_PART_6_SURTAX_IF_NON_RESIDENT,
            amount_kind=AMT_PART_6_SURTAX_AT_48_PERCENT,
            amount_value=D("8136.66"),
            count_kind=AMT_NON_RESIDENT_OR_DEEMED_RESIDENT,
            count=0,
            result=D("0"),
        ),
        # Form T691 Part 3 line 4, the second branch, "enter the amount from line 2" when "you are a
        # non-resident or deemed resident": line 2, 8136.66, times a count of 0 (Return A is not a
        # non-resident), a plain 0.
        AMT_FEDERAL_SURTAX_IF_NON_RESIDENT: TimesCountLine(
            output=AMT_FEDERAL_SURTAX_IF_NON_RESIDENT,
            amount_kind=AMT_FEDERAL_SURTAX_AT_48_PERCENT,
            amount_value=D("8136.66"),
            count_kind=AMT_NON_RESIDENT_OR_DEEMED_RESIDENT,
            count=0,
            result=D("0"),
        ),
        # T1 line 31000 from Schedule 8 Part 5 line 70, once for each Part 5 completed: 0 for
        # Return A.
        CPP_PART_5_BASE_CONTRIBUTIONS_ON_SELF_EMPLOYMENT: TimesCountLine(
            output=CPP_PART_5_BASE_CONTRIBUTIONS_ON_SELF_EMPLOYMENT,
            amount_kind=CPP_PART_5_LINE_70,
            amount_value=D("0.00"),
            count_kind=CPP_PART_5_COMPLETED,
            count=0,
            result=D("0"),
        ),
        # T1 line 22200 from Schedule 8 Part 5 line 88, once for each Part 5 completed: 0 for
        # Return A.
        CPP_PART_5_DEDUCTION_ON_SELF_EMPLOYMENT: TimesCountLine(
            output=CPP_PART_5_DEDUCTION_ON_SELF_EMPLOYMENT,
            amount_kind=CPP_PART_5_LINE_88,
            amount_value=D("0.00"),
            count_kind=CPP_PART_5_COMPLETED,
            count=0,
            result=D("0"),
        ),
        # T1 line 42100 from Schedule 8 Part 5 line 49 if positive, once for each Part 5
        # completed: 0 for Return A.
        CPP_PART_5_PAYABLE_ON_SELF_EMPLOYMENT: TimesCountLine(
            output=CPP_PART_5_PAYABLE_ON_SELF_EMPLOYMENT,
            amount_kind=CPP_PART_5_LINE_49_IF_POSITIVE,
            amount_value=D("0"),
            count_kind=CPP_PART_5_COMPLETED,
            count=0,
            result=D("0"),
        ),
        ontario.DISABILITY_AMOUNT_FOR_SELF: TimesCountLine(
            output=ontario.DISABILITY_AMOUNT_FOR_SELF,
            amount_kind=ontario.DISABILITY_AMOUNT_FOR_SELF_IF_ELIGIBLE,
            amount_value=D("10298.00"),
            count_kind=ELIGIBLE_FOR_DISABILITY_AMOUNT,
            count=0,
            result=D("0"),
        ),
        DISABILITY_AMOUNT_FOR_SELF: TimesCountLine(
            output=DISABILITY_AMOUNT_FOR_SELF,
            amount_kind=DISABILITY_AMOUNT_FOR_SELF_IF_ELIGIBLE,
            amount_value=D("10138.00"),
            count_kind=ELIGIBLE_FOR_DISABILITY_AMOUNT,
            count=0,
            result=D("0"),
        ),
        # T1 line 55 (line 23500): the chart's line 21 once if the chart applies, else 0; it does
        # not apply to Return A (no OAS, no net federal supplements and no EI benefits).
        SOCIAL_BENEFITS_REPAYMENT: TimesCountLine(
            output=SOCIAL_BENEFITS_REPAYMENT,
            amount_kind=SOCIAL_BENEFITS_LINE_21,
            amount_value=D("0"),
            count_kind=SOCIAL_BENEFITS_REPAYMENT_APPLIES,
            count=0,
            result=D("0"),
        ),
        # ON428 line 75 and line 76: the amounts of the filer's dependent children and dependants,
        # claimed once as the rule on lines 75 and 76 lets Return A's filer (no spouse or
        # common-law partner), and line 80 once as none of the six conditions applies.
        TAX_REDUCTION_FOR_CHILDREN: TimesCountLine(
            output=TAX_REDUCTION_FOR_CHILDREN,
            amount_kind=TAX_REDUCTION_FOR_CHILDREN_BEFORE_SPOUSE_RULE,
            amount_value=D("0"),
            count_kind=TAX_REDUCTION_AMOUNTS_CLAIMABLE,
            count=1,
            result=D("0"),
        ),
        TAX_REDUCTION_FOR_DEPENDANTS: TimesCountLine(
            output=TAX_REDUCTION_FOR_DEPENDANTS,
            amount_kind=TAX_REDUCTION_FOR_DEPENDANTS_BEFORE_SPOUSE_RULE,
            amount_value=D("0"),
            count_kind=TAX_REDUCTION_AMOUNTS_CLAIMABLE,
            count=1,
            result=D("0"),
        ),
        ONTARIO_TAX_REDUCTION: TimesCountLine(
            output=ONTARIO_TAX_REDUCTION,
            amount_kind=ONTARIO_TAX_REDUCTION_BEFORE_CONDITIONS,
            amount_value=D("0"),
            count_kind=TAX_REDUCTION_CLAIMABLE,
            count=1,
            result=D("0"),
        ),
        ontario.TAX_OTHERWISE_PAYABLE_REDUCTION: TimesCountLine(
            output=ontario.TAX_OTHERWISE_PAYABLE_REDUCTION,
            amount_kind=ontario.TAX_OTHERWISE_PAYABLE_REDUCTION_BEFORE_CONDITIONS,
            amount_value=D("0"),
            count_kind=ontario.TAX_OTHERWISE_PAYABLE_REDUCTION_CLAIMABLE,
            count=1,
            result=D("0"),
        ),
        ELIGIBLE_DEPENDANT_AMOUNT: TimesCountLine(
            output=ELIGIBLE_DEPENDANT_AMOUNT,
            amount_kind=ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT,
            amount_value=D("16129.00"),
            count_kind=ELIGIBLE_DEPENDANTS,
            count=0,
            result=D("0"),
        ),
        # T1 line 30100, line 30300 and line 30425, each line 7 or 5 claimed for the 0 filers
        # born in 1960 or earlier, 0 spouse amounts and 0 spouses eligible for the Canada
        # caregiver amount of Return A, a plain 0.
        AGE_AMOUNT: TimesCountLine(
            output=AGE_AMOUNT,
            amount_kind=AGE_AMOUNT_BEFORE_COUNT,
            amount_value=D("0"),
            count_kind=BORN_IN_1960_OR_EARLIER,
            count=0,
            result=D("0"),
        ),
        SPOUSE_AMOUNT: TimesCountLine(
            output=SPOUSE_AMOUNT,
            amount_kind=SPOUSE_AMOUNT_BEFORE_COUNT,
            amount_value=D("16129.00"),
            count_kind=SPOUSES_CLAIMED,
            count=0,
            result=D("0"),
        ),
        SPOUSE_CAREGIVER_AMOUNT: TimesCountLine(
            output=SPOUSE_CAREGIVER_AMOUNT,
            amount_kind=SPOUSE_CAREGIVER_AMOUNT_BEFORE_COUNT,
            amount_value=D("8601.00"),
            count_kind=SPOUSE_CAREGIVER_ELIGIBLE,
            count=0,
            result=D("0"),
        ),
        # The caller's count "claims the Ontario seniors care at home tax credit" times ON479 line
        # 13: Return A claims none, so a plain 0.
        SENIORS_CARE_CREDIT: TimesCountLine(
            output=SENIORS_CARE_CREDIT,
            amount_kind=SENIORS_CARE_BEFORE_CLAIM,
            amount_value=D("0"),
            count_kind=CLAIMS_SENIORS_CARE_CREDIT,
            count=0,
            result=D("0"),
        ),
        # ON428 line 10 (line 58080) and lines 11 to 13 (line 58120), each claimed for the 0
        # filers born in 1960 or earlier and 0 spouse amounts of Return A, a plain 0.
        ontario.AGE_AMOUNT: TimesCountLine(
            output=ontario.AGE_AMOUNT,
            amount_kind=ontario.AGE_AMOUNT_BEFORE_COUNT,
            amount_value=D("0"),
            count_kind=BORN_IN_1960_OR_EARLIER,
            count=0,
            result=D("0"),
        ),
        ontario.SPOUSE_AMOUNT: TimesCountLine(
            output=ontario.SPOUSE_AMOUNT,
            amount_kind=ontario.SPOUSE_AMOUNT_BEFORE_COUNT,
            amount_value=D("10823"),
            count_kind=SPOUSES_CLAIMED,
            count=0,
            result=D("0"),
        ),
        ontario.ELIGIBLE_DEPENDANT_AMOUNT: TimesCountLine(
            output=ontario.ELIGIBLE_DEPENDANT_AMOUNT,
            amount_kind=ontario.ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT,
            amount_value=D("10823"),
            count_kind=ELIGIBLE_DEPENDANTS,
            count=0,
            result=D("0"),
        ),
        # Federal Worksheet "Line 45200 - Refundable medical expense supplement" (T1 line 154),
        # Return A: line 21500 and line 33200 are 0, so line 11 and line 13 are 0.
        MEDICAL_SUPPLEMENT_IF_RESIDENT: TimesCountLine(
            output=MEDICAL_SUPPLEMENT_IF_RESIDENT,
            amount_kind=MEDICAL_SUPPLEMENT_IF_WORKING_INCOME_MET,
            amount_value=D("0.00"),
            count_kind=RESIDENT_IN_CANADA_THROUGHOUT_2025,
            count=1,
            result=D("0.00"),
        ),
        REFUNDABLE_MEDICAL_EXPENSE_SUPPLEMENT: TimesCountLine(
            output=REFUNDABLE_MEDICAL_EXPENSE_SUPPLEMENT,
            amount_kind=MEDICAL_SUPPLEMENT_IF_RESIDENT,
            amount_value=D("0.00"),
            count_kind=AGED_18_OR_OLDER_AT_END_OF_2025,
            count=1,
            result=D("0.00"),
        ),
        # T1 lines 42100, 31000 and 22200: Schedule 8 Part 4 lines 14, 15 and 17, each for the 0
        # "Part 4 completed" of Return A, a plain 0.
        CPP_PAYABLE_ON_SELF_EMPLOYMENT: TimesCountLine(
            output=CPP_PAYABLE_ON_SELF_EMPLOYMENT,
            amount_kind=SELF_EMPLOYED_CPP_CONTRIBUTIONS_PAYABLE,
            amount_value=D("0"),
            count_kind=CPP_PART_4_COMPLETED,
            count=0,
            result=D("0"),
        ),
        CPP_BASE_CONTRIBUTIONS_ON_SELF_EMPLOYMENT: TimesCountLine(
            output=CPP_BASE_CONTRIBUTIONS_ON_SELF_EMPLOYMENT,
            amount_kind=SELF_EMPLOYED_CPP_BASE_CREDIT,
            amount_value=D("0"),
            count_kind=CPP_PART_4_COMPLETED,
            count=0,
            result=D("0"),
        ),
        CPP_DEDUCTION_ON_SELF_EMPLOYMENT: TimesCountLine(
            output=CPP_DEDUCTION_ON_SELF_EMPLOYMENT,
            amount_kind=SELF_EMPLOYED_CPP_DEDUCTION,
            amount_value=D("0"),
            count_kind=CPP_PART_4_COMPLETED,
            count=0,
            result=D("0"),
        ),
        # T1 lines 31217 and 42120: Schedule 13 line 9, each for the 0 agreements with the
        # Canada Employment Insurance Commission of Return A, a plain 0.
        EI_PREMIUMS_ON_SELF_EMPLOYMENT: TimesCountLine(
            output=EI_PREMIUMS_ON_SELF_EMPLOYMENT,
            amount_kind=SELF_EMPLOYED_EI_PREMIUMS,
            amount_value=D("0"),
            count_kind=EI_SPECIAL_BENEFITS_AGREEMENT,
            count=0,
            result=D("0"),
        ),
        EI_PAYABLE_ON_SELF_EMPLOYMENT: TimesCountLine(
            output=EI_PAYABLE_ON_SELF_EMPLOYMENT,
            amount_kind=SELF_EMPLOYED_EI_PREMIUMS,
            amount_value=D("0"),
            count_kind=EI_SPECIAL_BENEFITS_AGREEMENT,
            count=0,
            result=D("0"),
        ),
        # Schedule 11, Schedule 2 and line 45350 (Return A claims none: every figure is 0).
        AMOUNTS_TRANSFERRED_FROM_SPOUSE: TimesCountLine(
            output=AMOUNTS_TRANSFERRED_FROM_SPOUSE,
            amount_kind=SPOUSE_UNUSED_AMOUNTS,
            amount_value=D("0"),
            count_kind=SPOUSE_NOT_SEPARATED_90_DAYS,
            count=0,
            result=D("0"),
        ),
        # Schedule ON(S2) line 11 and ON428 line 34 (line 58640), the same count (Return A claims
        # none: every figure is 0).
        ontario.AMOUNTS_TRANSFERRED_FROM_SPOUSE: TimesCountLine(
            output=ontario.AMOUNTS_TRANSFERRED_FROM_SPOUSE,
            amount_kind=ontario.SPOUSE_UNUSED_AMOUNTS,
            amount_value=D("0"),
            count_kind=SPOUSE_NOT_SEPARATED_90_DAYS,
            count=0,
            result=D("0"),
        ),
        # Form T2048 (line 25395) and Chart A: Return A enters nothing on the form, so its lines
        # are 0 (or, where they read another line, that line's figure).
        QBT_ELECTION_DEDUCTION: TimesCountLine(
            QBT_ELECTION_DEDUCTION, QBT_DEDUCTION_AVAILABLE, D("0"), QBT_ELECTION_IS_QBT, 0, D("0")
        ),
        QBT_NET_INVESTMENT_LOSS: TimesCountLine(
            QBT_NET_INVESTMENT_LOSS,
            QBT_CHART_A_NET_INVESTMENT_LOSS,
            D("0"),
            QBT_HAS_INVESTMENT_EXPENSES,
            0,
            D("0"),
        ),
        QSBCS_QFFP_TAXABLE_GAINS_RELATED_TO_DEDUCTION: TimesCountLine(
            QSBCS_QFFP_TAXABLE_GAINS_RELATED_TO_DEDUCTION,
            QBT_TAXABLE_GAINS_RELATED_TO_DEDUCTION,
            D("0"),
            QBT_GAINS_ARE_QSBCS_OR_QFFP,
            0,
            D("0"),
        ),
    }
    assert multiples == {
        ONTARIO_TAX_REDUCTION_BEFORE_CONDITIONS: MultipleOverLine(
            output=ONTARIO_TAX_REDUCTION_BEFORE_CONDITIONS,
            base=TAX_REDUCTION_AMOUNTS,
            base_amount=D("294.00"),
            factor=Factor(D("2")),
            less=ONTARIO_TAX_BEFORE_REDUCTION,
            less_amount=D("8195.77"),
            rounding=CENT,
            result=D("0"),
        ),
        ontario.TAX_OTHERWISE_PAYABLE_REDUCTION_BEFORE_CONDITIONS: MultipleOverLine(
            output=ontario.TAX_OTHERWISE_PAYABLE_REDUCTION_BEFORE_CONDITIONS,
            base=TAX_REDUCTION_AMOUNTS,
            base_amount=D("294.00"),
            factor=Factor(D("2")),
            less=ontario.TAX_OTHERWISE_PAYABLE_LINE_73,
            less_amount=D("8195.77"),
            rounding=CENT,
            result=D("0"),
        ),
    }
    assert capped == {
        # The guide's line 41400 "to a maximum of $750", after the 15%: 0 is below it.
        LABOUR_SPONSORED_FUNDS_CREDIT: CappedAmountLine(
            LABOUR_SPONSORED_FUNDS_CREDIT,
            LABOUR_SPONSORED_FUNDS_CREDIT_BEFORE_MAXIMUM,
            D("0"),
            Amount(D("750")),
            CENT,
            D("0"),
        ),
        CANADA_EMPLOYMENT_AMOUNT: CappedAmountLine(
            CANADA_EMPLOYMENT_AMOUNT,
            EMPLOYMENT_INCOME,
            D("110000"),
            Amount(D("1471")),
            CENT,
            D("1471"),
        ),
        # T1 line 109 "Enter whichever is less: $2,834 or the amount from line 108.": 3450.00 is
        # above it.
        MEDICAL_THRESHOLD: CappedAmountLine(
            MEDICAL_THRESHOLD,
            MEDICAL_NET_INCOME_SHARE,
            D("3450.00"),
            Amount(D("2834")),
            CENT,
            D("2834"),
        ),
        # ON428 line 40 "Enter whichever is less: $2,885 or the amount on line 39."
        ontario.MEDICAL_THRESHOLD: CappedAmountLine(
            ontario.MEDICAL_THRESHOLD,
            ontario.MEDICAL_NET_INCOME_SHARE,
            D("3450.00"),
            Amount(D("2885")),
            CENT,
            D("2885"),
        ),
        # Schedule ON428-A line 5's "(maximum $875)" and line 14 "Amount from line 5 above
        # (maximum $875)": 5555.00 is above it.
        LIFT_MAXIMUM_CREDIT: CappedAmountLine(
            LIFT_MAXIMUM_CREDIT,
            LIFT_CREDIT_BEFORE_MAXIMUM,
            D("5555.00"),
            Amount(D("875")),
            CENT,
            D("875"),
        ),
        # ON479 line 1's "(maximum $5,000)", printed after the percentage: it caps the credit.
        FERTILITY_CREDIT: CappedAmountLine(
            FERTILITY_CREDIT,
            FERTILITY_CREDIT_BEFORE_MAXIMUM,
            D("0"),
            Amount(D("5000")),
            CENT,
            D("0"),
        ),
        # ON479 line 5's "(maximum $1,500)", printed after the percentage: it caps the result.
        SENIORS_CARE_AMOUNT: CappedAmountLine(
            SENIORS_CARE_AMOUNT,
            SENIORS_CARE_BEFORE_MAXIMUM,
            D("0"),
            Amount(D("1500")),
            CENT,
            D("0"),
        ),
        # T1 line 161's "(maximum $1,000)", printed before the percentage: it caps the supplies
        # expenses (line 46800).
        EDUCATOR_SUPPLIES_EXPENSES_AT_MOST_MAXIMUM: CappedAmountLine(
            EDUCATOR_SUPPLIES_EXPENSES_AT_MOST_MAXIMUM,
            EDUCATOR_SUPPLIES_EXPENSES,
            D("0"),
            Amount(D("1000")),
            CENT,
            D("0"),
        ),
        # ON479 line 14's "(maximum $3,000)", printed before the percentage: it caps the amount
        # paid.
        SENIORS_TRANSIT_AMOUNT_PAID_AT_MOST_MAXIMUM: CappedAmountLine(
            SENIORS_TRANSIT_AMOUNT_PAID_AT_MOST_MAXIMUM,
            SENIORS_TRANSIT_PAID,
            D("0"),
            Amount(D("3000")),
            CENT,
            D("0"),
        ),
        # Schedule 5 line 3 of the line 30425 part "(maximum $8,601)": 28798.00 is above it.
        SPOUSE_CAREGIVER_LIMIT: CappedAmountLine(
            SPOUSE_CAREGIVER_LIMIT,
            SPOUSE_CAREGIVER_BEFORE_MAXIMUM,
            D("28798.00"),
            Amount(D("8601")),
            CENT,
            D("8601"),
        ),
        # ON428 line 13's "(maximum $10,823)": 11905.00 is above it.
        ontario.SPOUSE_AMOUNT_BEFORE_COUNT: CappedAmountLine(
            ontario.SPOUSE_AMOUNT_BEFORE_COUNT,
            ontario.SPOUSE_AMOUNT_BEFORE_MAXIMUM,
            D("11905.00"),
            Amount(D("10823")),
            CENT,
            D("10823"),
        ),
        # ON479 line 16's "(maximum $1,666.82)": the pick for contributions of 0 is 0.
        ontario.POLITICAL_CREDIT: CappedAmountLine(
            ontario.POLITICAL_CREDIT,
            ontario.POLITICAL_CREDIT_BEFORE_MAXIMUM,
            D("0.00"),
            Amount(D("1666.82")),
            CENT,
            D("0.00"),
        ),
        # T1 line 135 and line 41000 "(maximum $650)": the pick for contributions of 0 is 0.
        POLITICAL_CREDIT: CappedAmountLine(
            POLITICAL_CREDIT,
            POLITICAL_CREDIT_BEFORE_MAXIMUM,
            D("0.00"),
            Amount(D("650")),
            CENT,
            D("0.00"),
        ),
        # ON428 line 16's "(maximum $10,823)": 11905.00 is above it.
        ontario.ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT: CappedAmountLine(
            ontario.ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT,
            ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_MAXIMUM,
            D("11905.00"),
            Amount(D("10823")),
            CENT,
            D("10823"),
        ),
        # Federal Worksheet "Line 45200 - Refundable medical expense supplement" (T1 line 154),
        # Return A: line 21500 and line 33200 are 0, so line 11 and line 13 are 0.
        MEDICAL_SUPPLEMENT_LINE_14: CappedAmountLine(
            output=MEDICAL_SUPPLEMENT_LINE_14,
            base=MEDICAL_SUPPLEMENT_LINE_13,
            base_amount=D("0.00"),
            cap=Amount(D("1504")),
            rounding=CENT,
            result=D("0.00"),
        ),
        # Schedule 11, Schedule 2 and line 45350 (Return A claims none: every figure is 0).
        TUITION_TRANSFER_LIMIT: CappedAmountLine(
            output=TUITION_TRANSFER_LIMIT,
            base=CURRENT_YEAR_TUITION_AVAILABLE,
            base_amount=D("0"),
            cap=Amount(D("5000")),
            rounding=CENT,
            result=D("0.00"),
        ),
    }


def test_the_trace_records_the_capital_gains_picked_by_the_sign_of_line_20() -> None:
    result = run_a()
    trace = (
        *result["ca/t2125"][0].trace,
        *result["ca/t2042"][0].trace,
        *result["ca-on/return"][0].trace,
    )
    chosen = [line for line in trace if isinstance(line, SignChosenDifferenceLine)]
    # Form T691 Part 1 line 23 "If line 20 is positive, enter the amount from line 22.": Return
    # A's line 20 is 20000 (positive), so line 23 is line 22, 10000.
    assert chosen == [
        SignChosenDifferenceLine(
            output=AMT_CAPITAL_GAINS_ADDED,
            sign=AMT_NET_CAPITAL_GAINS_AFTER_ADJUSTMENTS,
            sign_amount=D("20000"),
            reference=TAXABLE_CAPITAL_GAINS,
            reference_amount=D("10000"),
            difference=AMT_CAPITAL_GAINS_DIFFERENCE,
            difference_amount=D("10000"),
            result=D("10000"),
        )
    ]
