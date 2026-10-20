"""CA-ON 2025 end to end, Return A: return a structured trace 2."""

from __future__ import annotations

from app.domain.trace import (
    SumLine,
)
from app.jurisdictions.ca.catalog import (
    ADDITIONAL_DEDUCTIONS,
    ADJUSTED_FAMILY_NET_INCOME,
    ADJUSTED_GROSS_CAPITAL_LOSSES_1985_TO_1987,
    ADJUSTED_GROSS_CAPITAL_LOSSES_1988_AND_1989,
    ADJUSTED_GROSS_CAPITAL_LOSSES_1990_TO_1999,
    ADJUSTED_GROSS_CAPITAL_LOSSES_2001_TO_2024,
    ADVANCED_CANADA_WORKERS_BENEFIT,
    AGE_AMOUNT,
    ALLOWABLE_BUSINESS_INVESTMENT_LOSS,
    BASIC_PERSONAL_AMOUNT,
    CANADA_EMPLOYMENT_AMOUNT,
    CANADA_WORKERS_BENEFIT,
    CANADIAN_ARMED_FORCES_AND_POLICE_DEDUCTION,
    CAPITAL_GAINS_DEDUCTIONS_1985_TO_1987,
    CAPITAL_GAINS_DEDUCTIONS_1988_AND_1989_ELIGIBLE_CAPITAL_PROPERTY,
    CAPITAL_GAINS_DEDUCTIONS_1988_AND_1989_OTHER_THAN_ELIGIBLE_CAPITAL_PROPERTY,
    CAPITAL_GAINS_DEDUCTIONS_1990_TO_1999,
    CAPITAL_GAINS_DEDUCTIONS_2000,
    CAPITAL_GAINS_DEDUCTIONS_2001_TO_2024,
    CAPITAL_GAINS_DEDUCTIONS_CLAIMED_1985_TO_2024,
    CAPITAL_GIFTS_LIMIT_ADDITION,
    CAPITAL_GIFTS_TOTAL,
    CAPITAL_PROPERTY_GIFTS,
    CAREGIVER_AMOUNT,
    CARRYING_CHARGES_INTEREST_EXPENSES_AND_OTHER_EXPENSES,
    CHARITABLE_DONATIONS,
    CHARITABLE_DONATIONS_CLAIMED,
    CHILD_CARE_BASIC_LIMIT,
    CHILD_CARE_EARNED_INCOME,
    CHILD_CARE_EXPENSES,
    CHILD_CARE_LIMIT_FOR_CHILDREN_SEVEN_TO_SIXTEEN,
    CHILD_CARE_LIMIT_FOR_CHILDREN_UNDER_SEVEN,
    CHILD_CARE_LIMIT_FOR_CHILDREN_WITH_DISABILITY,
    CLERGY_RESIDENCE_DEDUCTION,
    CPP_BASE_CONTRIBUTIONS,
    CPP_ENHANCED_CONTRIBUTIONS,
    CPP_FIRST_ADDITIONAL_CONTRIBUTIONS,
    CPP_OR_QPP_BENEFITS,
    CPP_SECOND_ADDITIONAL_CONTRIBUTIONS,
    CREDIT_AMOUNTS_AT_CREDIT_RATE,
    CREDITS_AGAINST_BASIC_FEDERAL_TAX,
    CREDITS_AGAINST_FEDERAL_TAX,
    DEDUCTIONS_FROM_NET_INCOME,
    DEDUCTIONS_FROM_TOTAL_INCOME,
    DEPRECIABLE_GIFTS,
    DISABILITY_SUPPORTS_DEDUCTION,
    DISABILITY_TRANSFERRED_AMOUNT,
    DIVIDEND_TAX_CREDIT,
    DIVIDENDS_AMOUNT_A,
    DIVIDENDS_AMOUNT_B,
    DIVIDENDS_WITHOUT_A_SLIP_GROSSED_UP,
    DONATION_LIMIT_ON_NET_INCOME,
    DONATION_LIMIT_WITH_CAPITAL_GIFTS,
    DONATIONS_AND_GIFTS_CREDIT,
    DONATIONS_AND_GIFTS_TOTAL,
    ECOLOGICAL_AND_CULTURAL_GIFTS,
    EDUCATOR_SCHOOL_SUPPLY_CREDIT,
    EI_AND_OTHER_BENEFITS,
    EI_PREMIUMS,
    ELECTED_SPLIT_PENSION_AMOUNT,
    ELECTED_SPLIT_PENSION_DEDUCTION,
    ELIGIBLE_DEPENDANT_AMOUNT,
    ELIGIBLE_DIVIDENDS_CREDIT,
    ELIGIBLE_DIVIDENDS_GROSSED_UP,
    EMPLOYEE_AND_PARTNER_GST_HST_REBATE,
    EMPLOYMENT_INCOME,
    EXPLORATION_AND_DEVELOPMENT_EXPENSES,
    FEDERAL_TAX_AFTER_CREDITS,
    FEDERAL_TAX_LESS_CREDITS,
    FEDERAL_TAX_WITH_ITC_RECAPTURE,
    FHSA_ANNUAL_AMOUNT,
    FHSA_ANNUAL_AMOUNT_FOR_2024,
    FHSA_ANNUAL_AMOUNT_FOR_2024_WITH_CARRYFORWARD,
    FHSA_ANNUAL_AMOUNT_WITH_CARRYFORWARD,
    FHSA_ANNUAL_LIMIT,
    FHSA_ANNUAL_LIMITS_FOR_2024_AND_PRIOR_YEARS,
    FHSA_CARRYFORWARD_FOR_2024,
    FHSA_CARRYFORWARD_FOR_2025,
    FHSA_CONTRIBUTIONS_AFTER_FIRST_QUALIFYING_WITHDRAWAL,
    FHSA_CONTRIBUTIONS_IN_2024_AFTER_FIRST_QUALIFYING_WITHDRAWAL,
    FHSA_CONTRIBUTIONS_IN_2025_AFTER_FIRST_QUALIFYING_WITHDRAWAL,
    FHSA_CONTRIBUTIONS_IN_2025_BEFORE_FIRST_QUALIFYING_WITHDRAWAL,
    FHSA_CONTRIBUTIONS_PLUS_VARIABLE_B_AMOUNT,
    FHSA_DEDUCTION,
    FHSA_DESIGNATED_TRANSFERS_IN_2024_AND_PRIOR_YEARS,
    FHSA_DESIGNATED_TRANSFERS_IN_2025,
    FHSA_INCOME,
    FHSA_RRSP_TRANSFERS_IN_2024_AND_PRIOR_YEARS,
    FHSA_RRSP_TRANSFERS_IN_2025,
    FHSA_TOTAL_ANNUAL_LIMITS,
    FHSA_TOTAL_DESIGNATED_TRANSFERS,
    FHSA_TOTAL_RRSP_TRANSFERS,
    FHSA_TRANSFER_AMOUNT_AT_MOST_LIMIT,
    FHSA_TRANSFER_AMOUNT_PLUS_VARIABLE_F_AMOUNT,
    FHSA_UNUSED_CONTRIBUTIONS_BROUGHT_FORWARD,
    FHSA_UNUSED_CONTRIBUTIONS_PLUS_CONTRIBUTIONS,
    FHSA_VARIABLE_B_AMOUNT,
    FHSA_VARIABLE_F_AMOUNT,
    FIRST_TIER_DONATION_CREDIT,
    FOREIGN_CHARITY_DONATIONS,
    FOREIGN_INVESTMENT_INCOME,
    GOVERNMENT_DONATIONS,
    GROSS_RENTAL_INCOME,
    HIGH_INCOME_DONATION_CREDIT,
    INCOME_SUPPORT_BENEFITS,
    INCOME_TAX_DEDUCTED,
    INFIRM_CHILDREN_AMOUNT,
    INTEREST_AND_OTHER_INVESTMENT_INCOME,
    INVESTMENT_INCOME_BEFORE_PRIOR_YEARS,
    INVESTMENT_INCOME_CREDITED_NOT_RECEIVED,
    INVESTMENT_INCOME_WITHOUT_A_SLIP,
    INVESTMENT_ROYALTIES,
    ITC_RECAPTURE,
    ITC_RECAPTURE_AT_15_PERCENT,
    ITC_RECAPTURE_AT_20_PERCENT,
    JOURNALISM_LABOUR_TAX_CREDIT,
    LABOUR_SPONSORED_FUNDS_CREDIT,
    LIMITED_PARTNERSHIP_LOSSES_OF_OTHER_YEARS,
    MEDICAL_CLAIM,
    MEDICAL_EXPENSES_OVER_THRESHOLD,
    MEDICAL_SUPPLEMENT_COLUMN_1_LINE_3,
    MEDICAL_SUPPLEMENT_COLUMN_1_LINE_5,
    MEDICAL_SUPPLEMENT_COLUMN_2_LINE_2,
    MEDICAL_SUPPLEMENT_COLUMN_2_LINE_3,
    MEDICAL_SUPPLEMENT_COLUMN_2_LINE_4,
    MEDICAL_SUPPLEMENT_COLUMN_2_LINE_5,
    MEDICAL_SUPPLEMENT_EMPLOYMENT_DEDUCTIONS,
    MEDICAL_SUPPLEMENT_EMPLOYMENT_INCOME,
    MEDICAL_SUPPLEMENT_EMPLOYMENT_WORKING_INCOME,
    MEDICAL_SUPPLEMENT_LINE_6,
    MEDICAL_SUPPLEMENT_LINE_11,
    MEDICAL_SUPPLEMENT_SELF_EMPLOYMENT_INCOME,
    MEDICAL_SUPPLEMENT_WORKING_INCOME,
    NET_BUSINESS_INCOME,
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
    OLD_AGE_SECURITY,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_1994,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_2024,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1994_TO_1996,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1997_TO_1999,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2000,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2001_TO_2023,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2024,
    OTHER_DEDUCTIONS,
    OTHER_DEPENDANTS_MEDICAL,
    OTHER_DIVIDENDS_CREDIT,
    OTHER_DIVIDENDS_GROSSED_UP,
    OTHER_EMPLOYMENT_EXPENSES,
    OTHER_EMPLOYMENT_INCOME,
    OTHER_FHSA_INCOME,
    OTHER_INCOME,
    OTHER_PAYMENTS_DEDUCTION,
    OTHER_PAYMENTS_LIMIT_INCOME,
    OTHER_PENSIONS_AND_SUPERANNUATION,
    PART_XII_2_TAX_CREDIT,
    POLITICAL_CREDIT,
    POLITICAL_CREDIT_COLUMN_1_LINE_5,
    POLITICAL_CREDIT_COLUMN_1_LINE_6,
    POLITICAL_CREDIT_COLUMN_1_LINE_7,
    POLITICAL_CREDIT_COLUMN_2_LINE_5,
    POLITICAL_CREDIT_COLUMN_2_LINE_6,
    POLITICAL_CREDIT_COLUMN_2_LINE_7,
    POLITICAL_CREDIT_COLUMN_3_LINE_5,
    POLITICAL_CREDIT_COLUMN_3_LINE_6,
    POLITICAL_CREDIT_COLUMN_3_LINE_7,
    PROVINCIAL_CREDITS,
    RDSP_INCOME,
    RDSP_INCOME_REPAYMENT,
    REFUND,
    REFUNDABLE_MEDICAL_EXPENSE_SUPPLEMENT,
    REGULAR_RATE_DONATION_CREDIT,
    RENTAL_ADVERTISING,
    RENTAL_ADVERTISING_PERSONAL_PORTION,
    RENTAL_ADVERTISING_SHORT_TERM_PORTION,
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
    RENTAL_NET_INCOME_AFTER_COOWNER_EXPENSES,
    RENTAL_NET_INCOME_WITH_RECAPTURE,
    RENTAL_OFFICE_EXPENSES,
    RENTAL_OFFICE_EXPENSES_PERSONAL_PORTION,
    RENTAL_OFFICE_EXPENSES_SHORT_TERM_PORTION,
    RENTAL_OTHER_EXPENSES,
    RENTAL_OTHER_EXPENSES_PERSONAL_PORTION,
    RENTAL_OTHER_EXPENSES_SHORT_TERM_PORTION,
    RENTAL_OTHER_INCOME,
    RENTAL_PARTNER_GST_HST_REBATE,
    RENTAL_PARTNER_SHARE,
    RENTAL_PARTNER_SHARE_WITH_REBATE,
    RENTAL_PERSONAL_PORTION,
    RENTAL_PROFESSIONAL_FEES,
    RENTAL_PROFESSIONAL_FEES_PERSONAL_PORTION,
    RENTAL_PROFESSIONAL_FEES_SHORT_TERM_PORTION,
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
    RENTAL_TOTAL_EXPENSES,
    RENTAL_TRAVEL,
    RENTAL_TRAVEL_PERSONAL_PORTION,
    RENTAL_TRAVEL_SHORT_TERM_PORTION,
    RENTAL_UTILITIES,
    RENTAL_UTILITIES_PERSONAL_PORTION,
    RENTAL_UTILITIES_SHORT_TERM_PORTION,
    RESP_AIPS_ADDITIONAL_TAX,
    RL_10_LABOUR_SPONSORED_FUND_AMOUNT,
    RPP_DEDUCTION,
    RRSP_CONTRIBUTIONS,
    RRSP_CONTRIBUTIONS_AVAILABLE,
    RRSP_DEDUCTION,
    RRSP_INCOME,
    SECURITY_OPTIONS_DEDUCTIONS,
    SLIP_DIVIDEND_TAX_CREDIT,
    SLIP_TAXABLE_DIVIDENDS,
    SLIP_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
    SOCIAL_ASSISTANCE_PAYMENTS,
    SPECIAL_TAXES,
    SPOUSE_AMOUNT,
    SPOUSE_AMOUNT_BASIS,
    SPOUSE_CAREGIVER_AMOUNT,
    SPOUSE_INFIRMITY_SUPPLEMENT,
    SPOUSE_NET_INCOME,
    SPOUSE_NET_INCOME_BEFORE_ADJUSTMENTS,
    SPOUSE_RDSP_INCOME,
    SPOUSE_RDSP_INCOME_REPAYMENT,
    SPOUSE_UCCB_REPAYMENT,
    SPOUSE_UNIVERSAL_CHILD_CARE_BENEFIT,
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
    TAXABLE_SCHOLARSHIPS,
    TAXABLE_SUPPORT_PAYMENTS,
    TOP_UP_CREDITS_BASE,
    TOP_UP_TAX_CREDIT,
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
    UNION_DUES,
    UNIVERSAL_CHILD_CARE_BENEFIT,
    UNIVERSITY_DONATIONS_OUTSIDE_CANADA,
    UNUSED_RRSP_CONTRIBUTIONS,
    WORKERS_COMPENSATION_BENEFITS,
    WORKING_INCOME,
)
from app.jurisdictions.ca_on import catalog as ontario
from app.jurisdictions.ca_on.catalog import (
    COOP_EDUCATION_CREDIT,
    FERTILITY_CREDIT,
    FLOW_THROUGH_SHARE_CREDIT,
    ONTARIO_CREDITS,
    ONTARIO_CREDITS_SUBTOTAL,
    ONTARIO_HEALTH_PREMIUM,
    ONTARIO_SURTAX,
    ONTARIO_TAX,
    ONTARIO_TAX_AFTER_CREDITS,
    ONTARIO_TAX_AFTER_FOOD_CREDIT,
    ONTARIO_TAX_WITH_SURTAX,
    SENIORS_CARE_CREDIT,
    SENIORS_CARE_FAMILY_NET_INCOME,
    SENIORS_TRANSIT_CREDIT,
    TAX_REDUCTION_AMOUNTS,
    TAX_REDUCTION_BASIC,
    TAX_REDUCTION_FOR_CHILDREN,
    TAX_REDUCTION_FOR_DEPENDANTS,
)
from tests.jurisdictions.ca_on.end_to_end.support import D, return_a


def test_the_trace_records_each_total_as_a_structured_line() -> None:
    trace = return_a().trace
    sums = {line.output: line for line in trace if isinstance(line, SumLine)}
    assert sums == {
        # T776 Part 3 line 8299 and Part 4 lines A, 9949 and 9365, amount 4 and amount 7 plus line
        # 9974: Return A has no rental figures, so each is a sum of zeros.
        GROSS_RENTAL_INCOME: SumLine(
            GROSS_RENTAL_INCOME,
            (
                (RENTAL_GROSS_RENTS, D("0")),
                (RENTAL_OTHER_INCOME, D("0")),
            ),
            D("0"),
        ),
        RENTAL_TOTAL_EXPENSES: SumLine(
            RENTAL_TOTAL_EXPENSES,
            (
                (RENTAL_ADVERTISING, D("0")),
                (RENTAL_INSURANCE, D("0")),
                (RENTAL_INTEREST_AND_BANK_CHARGES, D("0")),
                (RENTAL_OFFICE_EXPENSES, D("0")),
                (RENTAL_PROFESSIONAL_FEES, D("0")),
                (RENTAL_MANAGEMENT_AND_ADMINISTRATION_FEES, D("0")),
                (RENTAL_REPAIRS_AND_MAINTENANCE, D("0")),
                (RENTAL_SALARIES_WAGES_AND_BENEFITS, D("0")),
                (RENTAL_PROPERTY_TAXES, D("0")),
                (RENTAL_TRAVEL, D("0")),
                (RENTAL_UTILITIES, D("0")),
                (RENTAL_MOTOR_VEHICLE_EXPENSES, D("0")),
                (RENTAL_OTHER_EXPENSES, D("0")),
            ),
            D("0"),
        ),
        RENTAL_PERSONAL_PORTION: SumLine(
            RENTAL_PERSONAL_PORTION,
            (
                (RENTAL_ADVERTISING_PERSONAL_PORTION, D("0")),
                (RENTAL_INSURANCE_PERSONAL_PORTION, D("0")),
                (RENTAL_INTEREST_AND_BANK_CHARGES_PERSONAL_PORTION, D("0")),
                (RENTAL_OFFICE_EXPENSES_PERSONAL_PORTION, D("0")),
                (RENTAL_PROFESSIONAL_FEES_PERSONAL_PORTION, D("0")),
                (RENTAL_MANAGEMENT_AND_ADMINISTRATION_FEES_PERSONAL_PORTION, D("0")),
                (RENTAL_REPAIRS_AND_MAINTENANCE_PERSONAL_PORTION, D("0")),
                (RENTAL_SALARIES_WAGES_AND_BENEFITS_PERSONAL_PORTION, D("0")),
                (RENTAL_PROPERTY_TAXES_PERSONAL_PORTION, D("0")),
                (RENTAL_TRAVEL_PERSONAL_PORTION, D("0")),
                (RENTAL_UTILITIES_PERSONAL_PORTION, D("0")),
                (RENTAL_MOTOR_VEHICLE_EXPENSES_PERSONAL_PORTION, D("0")),
                (RENTAL_OTHER_EXPENSES_PERSONAL_PORTION, D("0")),
            ),
            D("0"),
        ),
        RENTAL_SHORT_TERM_PORTION: SumLine(
            RENTAL_SHORT_TERM_PORTION,
            (
                (RENTAL_ADVERTISING_SHORT_TERM_PORTION, D("0")),
                (RENTAL_INSURANCE_SHORT_TERM_PORTION, D("0")),
                (RENTAL_INTEREST_AND_BANK_CHARGES_SHORT_TERM_PORTION, D("0")),
                (RENTAL_OFFICE_EXPENSES_SHORT_TERM_PORTION, D("0")),
                (RENTAL_PROFESSIONAL_FEES_SHORT_TERM_PORTION, D("0")),
                (RENTAL_MANAGEMENT_AND_ADMINISTRATION_FEES_SHORT_TERM_PORTION, D("0")),
                (RENTAL_REPAIRS_AND_MAINTENANCE_SHORT_TERM_PORTION, D("0")),
                (RENTAL_SALARIES_WAGES_AND_BENEFITS_SHORT_TERM_PORTION, D("0")),
                (RENTAL_PROPERTY_TAXES_SHORT_TERM_PORTION, D("0")),
                (RENTAL_TRAVEL_SHORT_TERM_PORTION, D("0")),
                (RENTAL_UTILITIES_SHORT_TERM_PORTION, D("0")),
                (RENTAL_MOTOR_VEHICLE_EXPENSES_SHORT_TERM_PORTION, D("0")),
                (RENTAL_OTHER_EXPENSES_SHORT_TERM_PORTION, D("0")),
            ),
            D("0"),
        ),
        RENTAL_NET_INCOME_WITH_RECAPTURE: SumLine(
            RENTAL_NET_INCOME_WITH_RECAPTURE,
            (
                (RENTAL_NET_INCOME_AFTER_COOWNER_EXPENSES, D("0")),
                (RENTAL_RECAPTURED_CCA, D("0")),
            ),
            D("0"),
        ),
        RENTAL_PARTNER_SHARE_WITH_REBATE: SumLine(
            RENTAL_PARTNER_SHARE_WITH_REBATE,
            (
                (RENTAL_PARTNER_SHARE, D("0")),
                (RENTAL_PARTNER_GST_HST_REBATE, D("0")),
            ),
            D("0"),
        ),
        # The Federal Worksheet's "Lines 12000 and 12010" lines 5 and 10, line 17 and, with the
        # slip amounts, lines 12010 and 12000: no dividends, so every line is 0.
        SLIP_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE: SumLine(
            SLIP_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
            (
                (T3_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE, D("0")),
                (T4PS_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE, D("0")),
                (T5_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE, D("0")),
                (T5013_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE, D("0")),
            ),
            D("0"),
        ),
        SLIP_TAXABLE_DIVIDENDS: SumLine(
            SLIP_TAXABLE_DIVIDENDS,
            (
                (T3_TAXABLE_DIVIDENDS, D("0")),
                (T4PS_TAXABLE_DIVIDENDS, D("0")),
                (T5_TAXABLE_DIVIDENDS, D("0")),
                (T5013_TAXABLE_DIVIDENDS, D("0")),
            ),
            D("0"),
        ),
        DIVIDENDS_WITHOUT_A_SLIP_GROSSED_UP: SumLine(
            DIVIDENDS_WITHOUT_A_SLIP_GROSSED_UP,
            (
                (ELIGIBLE_DIVIDENDS_GROSSED_UP, D("0")),
                (OTHER_DIVIDENDS_GROSSED_UP, D("0")),
            ),
            D("0"),
        ),
        TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE: SumLine(
            TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
            (
                (SLIP_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE, D("0")),
                (OTHER_DIVIDENDS_GROSSED_UP, D("0")),
            ),
            D("0"),
        ),
        TAXABLE_DIVIDENDS: SumLine(
            TAXABLE_DIVIDENDS,
            (
                (SLIP_TAXABLE_DIVIDENDS, D("0")),
                (DIVIDENDS_WITHOUT_A_SLIP_GROSSED_UP, D("0")),
            ),
            D("0"),
        ),
        # The Federal Worksheet's "Line 40425 - Federal dividend tax credit" lines 5, A, B, 8 and
        # 9 and T1 line 125 "Add lines 122 to 124.": lines A and B are each one part.
        SLIP_DIVIDEND_TAX_CREDIT: SumLine(
            SLIP_DIVIDEND_TAX_CREDIT,
            (
                (T3_DIVIDEND_TAX_CREDIT, D("0")),
                (T4PS_DIVIDEND_TAX_CREDIT, D("0")),
                (T5_DIVIDEND_TAX_CREDIT, D("0")),
                (T5013_DIVIDEND_TAX_CREDIT, D("0")),
            ),
            D("0"),
        ),
        DIVIDENDS_AMOUNT_A: SumLine(
            DIVIDENDS_AMOUNT_A,
            ((DIVIDENDS_WITHOUT_A_SLIP_GROSSED_UP, D("0")),),
            D("0"),
        ),
        DIVIDENDS_AMOUNT_B: SumLine(
            DIVIDENDS_AMOUNT_B,
            ((OTHER_DIVIDENDS_GROSSED_UP, D("0")),),
            D("0"),
        ),
        NO_SLIP_DIVIDEND_TAX_CREDIT: SumLine(
            NO_SLIP_DIVIDEND_TAX_CREDIT,
            (
                (OTHER_DIVIDENDS_CREDIT, D("0")),
                (ELIGIBLE_DIVIDENDS_CREDIT, D("0")),
            ),
            D("0"),
        ),
        DIVIDEND_TAX_CREDIT: SumLine(
            DIVIDEND_TAX_CREDIT,
            (
                (SLIP_DIVIDEND_TAX_CREDIT, D("0")),
                (NO_SLIP_DIVIDEND_TAX_CREDIT, D("0")),
            ),
            D("0"),
        ),
        CREDITS_AGAINST_BASIC_FEDERAL_TAX: SumLine(
            CREDITS_AGAINST_BASIC_FEDERAL_TAX,
            ((NON_REFUNDABLE_TAX_CREDITS, D("3194.87")), (DIVIDEND_TAX_CREDIT, D("0"))),
            D("3194.87"),
        ),
        # T1 line 15000 "Line 28 plus line 32 Total income": the income lines, in line order.
        TOTAL_INCOME: SumLine(
            TOTAL_INCOME,
            (
                (EMPLOYMENT_INCOME, D("110000")),
                (OTHER_EMPLOYMENT_INCOME, D("0")),
                (OLD_AGE_SECURITY, D("0")),
                (CPP_OR_QPP_BENEFITS, D("0")),
                (OTHER_PENSIONS_AND_SUPERANNUATION, D("0")),
                (ELECTED_SPLIT_PENSION_AMOUNT, D("0")),
                (UNIVERSAL_CHILD_CARE_BENEFIT, D("0")),
                (EI_AND_OTHER_BENEFITS, D("0")),
                (TAXABLE_DIVIDENDS, D("0")),
                (INTEREST_AND_OTHER_INVESTMENT_INCOME, D("0")),
                (NET_PARTNERSHIP_INCOME, D("0")),
                (RDSP_INCOME, D("0")),
                (NET_RENTAL_INCOME, D("0")),
                (TAXABLE_CAPITAL_GAINS, D("10000")),
                (TAXABLE_SUPPORT_PAYMENTS, D("0")),
                (RRSP_INCOME, D("0")),
                (FHSA_INCOME, D("0")),
                (OTHER_FHSA_INCOME, D("0")),
                (OTHER_INCOME, D("0")),
                (TAXABLE_SCHOLARSHIPS, D("0")),
                (INCOME_SUPPORT_BENEFITS, D("0")),
            ),
            D("120000"),
        ),
        # The Federal Worksheet's "Line 12100 - Interest and other investment income" line 9
        # "Add lines 1 to 8.", and T1 line 14700 "Add lines 29 to 31", each in line order.
        INVESTMENT_INCOME_BEFORE_PRIOR_YEARS: SumLine(
            INVESTMENT_INCOME_BEFORE_PRIOR_YEARS,
            (
                (T3_INVESTMENT_INCOME, D("0")),
                (T5_INVESTMENT_INCOME, D("0")),
                (T5013_INVESTMENT_INCOME, D("0")),
                (INVESTMENT_INCOME_CREDITED_NOT_RECEIVED, D("0")),
                (TAX_REFUND_INTEREST, D("0")),
                (FOREIGN_INVESTMENT_INCOME, D("0")),
                (INVESTMENT_INCOME_WITHOUT_A_SLIP, D("0")),
                (INVESTMENT_ROYALTIES, D("0")),
            ),
            D("0"),
        ),
        INCOME_SUPPORT_BENEFITS: SumLine(
            INCOME_SUPPORT_BENEFITS,
            (
                (WORKERS_COMPENSATION_BENEFITS, D("0")),
                (SOCIAL_ASSISTANCE_PAYMENTS, D("0")),
                (NET_FEDERAL_SUPPLEMENTS, D("0")),
            ),
            D("0"),
        ),
        # Schedule 8 Part 3a line 28 "Line 26 plus line 27", to T1 line 22215.
        CPP_ENHANCED_CONTRIBUTIONS: SumLine(
            CPP_ENHANCED_CONTRIBUTIONS,
            (
                (CPP_FIRST_ADDITIONAL_CONTRIBUTIONS, D("678.00")),
                (CPP_SECOND_ADDITIONAL_CONTRIBUTIONS, D("396.00")),
            ),
            D("1074.00"),
        ),
        # Schedule 7 line 5 "Line 1 plus line 4 ... Total contributions", to line 10
        # "Contributions available to deduct" with no HBP or LLP repayments (line 9).
        RRSP_CONTRIBUTIONS_AVAILABLE: SumLine(
            RRSP_CONTRIBUTIONS_AVAILABLE,
            ((UNUSED_RRSP_CONTRIBUTIONS, D("0")), (RRSP_CONTRIBUTIONS, D("1926"))),
            D("1926"),
        ),
        # Form T778 line 4 "Add lines 1 to 3.", and line 6's earned income, the employment
        # income.
        CHILD_CARE_BASIC_LIMIT: SumLine(
            CHILD_CARE_BASIC_LIMIT,
            (
                (CHILD_CARE_LIMIT_FOR_CHILDREN_UNDER_SEVEN, D("0")),
                (CHILD_CARE_LIMIT_FOR_CHILDREN_WITH_DISABILITY, D("0")),
                (CHILD_CARE_LIMIT_FOR_CHILDREN_SEVEN_TO_SIXTEEN, D("0")),
            ),
            D("0"),
        ),
        CHILD_CARE_EARNED_INCOME: SumLine(
            CHILD_CARE_EARNED_INCOME, ((EMPLOYMENT_INCOME, D("110000")),), D("110000")
        ),
        # T1 line 23300, in line order: 20700, 20800, 20805, 21000, 21200, 21300, 21400, 21700,
        # 22000, 22100, 22215, 22400, 23200.
        DEDUCTIONS_FROM_TOTAL_INCOME: SumLine(
            DEDUCTIONS_FROM_TOTAL_INCOME,
            (
                (RPP_DEDUCTION, D("0")),
                (RRSP_DEDUCTION, D("1926")),
                (FHSA_DEDUCTION, D("0")),
                (ELECTED_SPLIT_PENSION_DEDUCTION, D("0")),
                (UNION_DUES, D("2000")),
                (UCCB_REPAYMENT, D("0")),
                (CHILD_CARE_EXPENSES, D("0")),
                (ALLOWABLE_BUSINESS_INVESTMENT_LOSS, D("0")),
                (SUPPORT_PAYMENTS_DEDUCTION, D("0")),
                (CARRYING_CHARGES_INTEREST_EXPENSES_AND_OTHER_EXPENSES, D("0")),
                (CPP_ENHANCED_CONTRIBUTIONS, D("1074.00")),
                (EXPLORATION_AND_DEVELOPMENT_EXPENSES, D("0")),
                (OTHER_DEDUCTIONS, D("0")),
            ),
            D("5000"),
        ),
        # The Federal Worksheet's "Line 25000 - Other payments deduction" lines 4, 8 and 9, each
        # in line order.
        UCCB_AND_RDSP_INCOME: SumLine(
            UCCB_AND_RDSP_INCOME,
            ((UNIVERSAL_CHILD_CARE_BENEFIT, D("0")), (RDSP_INCOME, D("0"))),
            D("0"),
        ),
        UCCB_AND_RDSP_INCOME_REPAYMENTS: SumLine(
            UCCB_AND_RDSP_INCOME_REPAYMENTS,
            ((UCCB_REPAYMENT, D("0")), (RDSP_INCOME_REPAYMENT, D("0"))),
            D("0"),
        ),
        # Schedule ON428-A lines 9 "Add lines 6 to 8.", 12 "Line 10 plus line 11", 24 "Add lines
        # 21 to 23.", 27 "Line 25 plus line 26" and 35 "Line 33 plus line 34 Adjusted family net
        # income", each in line order; the spouse's lines are 0 for a filer with no spouse.
        ontario.LIFT_NET_INCOME_AND_REPAYMENTS: SumLine(
            ontario.LIFT_NET_INCOME_AND_REPAYMENTS,
            (
                (NET_INCOME_BEFORE_ADJUSTMENTS, D("115000")),
                (UCCB_REPAYMENT, D("0")),
                (RDSP_INCOME_REPAYMENT, D("0")),
            ),
            D("115000"),
        ),
        ontario.LIFT_UCCB_AND_RDSP_INCOME: SumLine(
            ontario.LIFT_UCCB_AND_RDSP_INCOME,
            ((UNIVERSAL_CHILD_CARE_BENEFIT, D("0")), (RDSP_INCOME, D("0"))),
            D("0"),
        ),
        ontario.LIFT_SPOUSE_NET_INCOME_AND_REPAYMENTS: SumLine(
            ontario.LIFT_SPOUSE_NET_INCOME_AND_REPAYMENTS,
            (
                (SPOUSE_NET_INCOME_BEFORE_ADJUSTMENTS, D("0")),
                (SPOUSE_UCCB_REPAYMENT, D("0")),
                (SPOUSE_RDSP_INCOME_REPAYMENT, D("0")),
            ),
            D("0"),
        ),
        ontario.LIFT_SPOUSE_UCCB_AND_RDSP_INCOME: SumLine(
            ontario.LIFT_SPOUSE_UCCB_AND_RDSP_INCOME,
            (
                (SPOUSE_UNIVERSAL_CHILD_CARE_BENEFIT, D("0")),
                (SPOUSE_RDSP_INCOME, D("0")),
            ),
            D("0"),
        ),
        ontario.LIFT_FAMILY_NET_INCOME: SumLine(
            ontario.LIFT_FAMILY_NET_INCOME,
            (
                (ontario.LIFT_ADJUSTED_NET_INCOME, D("115000")),
                (ontario.LIFT_SPOUSE_ADJUSTED_NET_INCOME, D("0")),
            ),
            D("115000"),
        ),
        OTHER_PAYMENTS_LIMIT_INCOME: SumLine(
            OTHER_PAYMENTS_LIMIT_INCOME,
            (
                (NET_INCOME_LESS_UCCB_AND_RDSP_INCOME, D("115000")),
                (UCCB_AND_RDSP_INCOME_REPAYMENTS, D("0")),
            ),
            D("115000"),
        ),
        # T1 line 68 and line 25700 "Add lines 58 to 67.", in line order, line 63 (25300) included.
        DEDUCTIONS_FROM_NET_INCOME: SumLine(
            DEDUCTIONS_FROM_NET_INCOME,
            (
                (CANADIAN_ARMED_FORCES_AND_POLICE_DEDUCTION, D("0")),
                (SECURITY_OPTIONS_DEDUCTIONS, D("0")),
                (OTHER_PAYMENTS_DEDUCTION, D("0")),
                (LIMITED_PARTNERSHIP_LOSSES_OF_OTHER_YEARS, D("0")),
                (NON_CAPITAL_LOSSES_OF_OTHER_YEARS, D("0")),
                (NET_CAPITAL_LOSSES_OF_OTHER_YEARS, D("0")),
                (ADDITIONAL_DEDUCTIONS, D("0")),
            ),
            D("0"),
        ),
        # T1 line 118 (line 35000) "Add lines 115 to 117. Total federal non-refundable tax credits":
        # line 115 (line 33800), line 116 (line 34900) and line 117 (line 34990), in line order.
        NON_REFUNDABLE_TAX_CREDITS: SumLine(
            NON_REFUNDABLE_TAX_CREDITS,
            (
                (CREDIT_AMOUNTS_AT_CREDIT_RATE, D("3194.87")),
                (DONATIONS_AND_GIFTS_CREDIT, D("0.00")),
                (TOP_UP_TAX_CREDIT, D("0.00")),
            ),
            D("3194.87"),
        ),
        # ON428 line 49 and line 58969 "Line 47 plus line 48", and line 50 and line 61500 "Line 46
        # plus line 49 Enter this amount on line 52. Ontario non-refundable tax credits".
        ontario.DONATIONS_AND_GIFTS_CREDIT: SumLine(
            ontario.DONATIONS_AND_GIFTS_CREDIT,
            (
                (ontario.DONATIONS_FIRST_TIER_CREDIT, D("0.00")),
                (ontario.DONATIONS_OVER_FIRST_TIER_CREDIT, D("0.00")),
            ),
            D("0.00"),
        ),
        ontario.NON_REFUNDABLE_TAX_CREDITS: SumLine(
            ontario.NON_REFUNDABLE_TAX_CREDITS,
            (
                (ontario.CREDIT_AMOUNTS_AT_CREDIT_RATE, D("867.62")),
                (ontario.DONATIONS_AND_GIFTS_CREDIT, D("0.00")),
            ),
            D("867.62"),
        ),
        # Schedule 9 line 5 "Add lines 1 to 4.", line 7 "Amount B plus amount C Line D", line 8
        # "Line 6 plus line 7", line 12 "Line 10 plus line 11" and line 23 "Add lines 20 to 22.".
        TOTAL_CHARITABLE_DONATIONS: SumLine(
            TOTAL_CHARITABLE_DONATIONS,
            (
                (CHARITABLE_DONATIONS, D("0")),
                (GOVERNMENT_DONATIONS, D("0")),
                (UNIVERSITY_DONATIONS_OUTSIDE_CANADA, D("0")),
                (FOREIGN_CHARITY_DONATIONS, D("0")),
            ),
            D("0"),
        ),
        CAPITAL_GIFTS_TOTAL: SumLine(
            CAPITAL_GIFTS_TOTAL,
            ((DEPRECIABLE_GIFTS, D("0")), (CAPITAL_PROPERTY_GIFTS, D("0"))),
            D("0"),
        ),
        # T1 line 112 "Line 110 plus line 111".
        MEDICAL_CLAIM: SumLine(
            MEDICAL_CLAIM,
            (
                (MEDICAL_EXPENSES_OVER_THRESHOLD, D("0")),
                (OTHER_DEPENDANTS_MEDICAL, D("0")),
            ),
            D("0"),
        ),
        # ON428 line 43 and line 58769 "Line 41 plus line 42".
        ontario.MEDICAL_CLAIM: SumLine(
            ontario.MEDICAL_CLAIM,
            (
                (ontario.MEDICAL_EXPENSES_OVER_THRESHOLD, D("0")),
                (ontario.OTHER_DEPENDANTS_MEDICAL, D("0")),
            ),
            D("0"),
        ),
        DONATION_LIMIT_WITH_CAPITAL_GIFTS: SumLine(
            DONATION_LIMIT_WITH_CAPITAL_GIFTS,
            (
                (DONATION_LIMIT_ON_NET_INCOME, D("86250")),
                (CAPITAL_GIFTS_LIMIT_ADDITION, D("0.00")),
            ),
            D("86250"),
        ),
        DONATIONS_AND_GIFTS_TOTAL: SumLine(
            DONATIONS_AND_GIFTS_TOTAL,
            ((CHARITABLE_DONATIONS_CLAIMED, D("0")), (ECOLOGICAL_AND_CULTURAL_GIFTS, D("0"))),
            D("0"),
        ),
        DONATIONS_AND_GIFTS_CREDIT: SumLine(
            DONATIONS_AND_GIFTS_CREDIT,
            (
                (HIGH_INCOME_DONATION_CREDIT, D("0.00")),
                (REGULAR_RATE_DONATION_CREDIT, D("0.00")),
                (FIRST_TIER_DONATION_CREDIT, D("0.00")),
            ),
            D("0.00"),
        ),
        # Federal Worksheet line 3 "Line 1 plus line 2": line 33800 and Schedule 9 line 22.
        TOP_UP_CREDITS_BASE: SumLine(
            TOP_UP_CREDITS_BASE,
            (
                (CREDIT_AMOUNTS_AT_CREDIT_RATE, D("3194.87")),
                (FIRST_TIER_DONATION_CREDIT, D("0.00")),
            ),
            D("3194.87"),
        ),
        NON_REFUNDABLE_CREDIT_AMOUNTS: SumLine(
            NON_REFUNDABLE_CREDIT_AMOUNTS,
            (
                (BASIC_PERSONAL_AMOUNT, D("16129")),
                (AGE_AMOUNT, D("0")),
                (SPOUSE_AMOUNT, D("0")),
                (ELIGIBLE_DEPENDANT_AMOUNT, D("0")),
                (SPOUSE_CAREGIVER_AMOUNT, D("0")),
                (CAREGIVER_AMOUNT, D("0")),
                (INFIRM_CHILDREN_AMOUNT, D("0")),
                (CPP_BASE_CONTRIBUTIONS, D("3356.10")),
                (EI_PREMIUMS, D("1077.48")),
                (CANADA_EMPLOYMENT_AMOUNT, D("1471")),
                (DISABILITY_TRANSFERRED_AMOUNT, D("0")),
                (MEDICAL_CLAIM, D("0")),
            ),
            D("22033.58"),
        ),
        # Schedule 5 (5000-S5) line 3 "Line 1 plus line 2": the basic personal amount plus the
        # amount for a spouse eligible for the Canada caregiver amount, here none.
        SPOUSE_AMOUNT_BASIS: SumLine(
            SPOUSE_AMOUNT_BASIS,
            (
                (BASIC_PERSONAL_AMOUNT, D("16129.00")),
                (SPOUSE_INFIRMITY_SUPPLEMENT, D("0")),
            ),
            D("16129.00"),
        ),
        # ON428 has no Canada employment amount; its lines 58240 and 58300 read the federal
        # amounts (lines 30800 and 31200).
        ontario.NON_REFUNDABLE_CREDIT_AMOUNTS: SumLine(
            ontario.NON_REFUNDABLE_CREDIT_AMOUNTS,
            (
                (ontario.BASIC_PERSONAL_AMOUNT, D("12747")),
                (ontario.AGE_AMOUNT, D("0")),
                (ontario.SPOUSE_AMOUNT, D("0")),
                (ontario.ELIGIBLE_DEPENDANT_AMOUNT, D("0")),
                (ontario.CAREGIVER_AMOUNT, D("0")),
                (CPP_BASE_CONTRIBUTIONS, D("3356.10")),
                (EI_PREMIUMS, D("1077.48")),
                (ontario.MEDICAL_CLAIM, D("0")),
            ),
            D("17180.58"),
        ),
        # Worksheet ON428's "Line 61520" lines A and B (whole lines 12000 and 12010) and line 3
        # "Line 1 plus line 2", and ON428 lines 56 "Enter the amount from line 53 above." and 70
        # "Ontario dividend tax credit from line 57": each of A, B, 56 and 70 is one part.
        ontario.DIVIDENDS_AMOUNT_A: SumLine(
            ontario.DIVIDENDS_AMOUNT_A, ((TAXABLE_DIVIDENDS, D("0")),), D("0")
        ),
        ontario.DIVIDENDS_AMOUNT_B: SumLine(
            ontario.DIVIDENDS_AMOUNT_B,
            ((TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE, D("0")),),
            D("0"),
        ),
        ontario.DIVIDEND_TAX_CREDIT: SumLine(
            ontario.DIVIDEND_TAX_CREDIT,
            ((ontario.OTHER_DIVIDENDS_CREDIT, D("0")), (ontario.ELIGIBLE_DIVIDENDS_CREDIT, D("0"))),
            D("0"),
        ),
        ontario.ONTARIO_TAX_BEFORE_DIVIDEND_CREDIT: SumLine(
            ontario.ONTARIO_TAX_BEFORE_DIVIDEND_CREDIT,
            ((ONTARIO_TAX_AFTER_CREDITS, D("7671.98")),),
            D("7671.98"),
        ),
        ontario.DIVIDEND_CREDIT_FROM_LINE_57: SumLine(
            ontario.DIVIDEND_CREDIT_FROM_LINE_57,
            ((ontario.DIVIDEND_TAX_CREDIT, D("0")),),
            D("0"),
        ),
        # ON428 line 69 "Line 62 plus line 68": the Ontario tax after credits plus the surtax.
        ONTARIO_TAX_WITH_SURTAX: SumLine(
            ONTARIO_TAX_WITH_SURTAX,
            ((ONTARIO_TAX_AFTER_CREDITS, D("7671.98")), (ONTARIO_SURTAX, D("523.79"))),
            D("8195.77"),
        ),
        # ON428 line 77 "Add lines 74 to 76.", in line order.
        TAX_REDUCTION_AMOUNTS: SumLine(
            TAX_REDUCTION_AMOUNTS,
            (
                (TAX_REDUCTION_BASIC, D("294.00")),
                (TAX_REDUCTION_FOR_CHILDREN, D("0")),
                (TAX_REDUCTION_FOR_DEPENDANTS, D("0")),
            ),
            D("294.00"),
        ),
        # ON428 line 90 "Line 88 plus line 89 Enter this amount on line 42800 of your return.
        # Ontario tax": line 88 is line 86, as line 87 is 0.
        ONTARIO_TAX: SumLine(
            ONTARIO_TAX,
            (
                (ONTARIO_TAX_AFTER_FOOD_CREDIT, D("8195.77")),
                (ONTARIO_HEALTH_PREMIUM, D("750")),
            ),
            D("8945.77"),
        ),
        # T1 line 142 (line 42000) "Add lines 139 to 141. Net federal tax", in line order: line
        # 139 (41700), line 140 (41500, the advanced Canada workers benefit) and line 141 (41800,
        # special taxes), the last two 0 here.
        NET_FEDERAL_TAX: SumLine(
            NET_FEDERAL_TAX,
            (
                (FEDERAL_TAX_LESS_CREDITS, D("16951.38")),
                (ADVANCED_CANADA_WORKERS_BENEFIT, D("0")),
                (SPECIAL_TAXES, D("0")),
            ),
            D("16951.38"),
        ),
        # T2038(IND) Part C amount 3 "Total recapture of investment tax credit on SR&ED
        # expenditures (add amounts 1 and 2)", T1 line 131, and line 132 "Line 130 plus line 131"
        # with line 130 carrying line 126.
        ITC_RECAPTURE: SumLine(
            ITC_RECAPTURE,
            ((ITC_RECAPTURE_AT_15_PERCENT, D("0")), (ITC_RECAPTURE_AT_20_PERCENT, D("0"))),
            D("0"),
        ),
        FEDERAL_TAX_WITH_ITC_RECAPTURE: SumLine(
            FEDERAL_TAX_WITH_ITC_RECAPTURE,
            ((FEDERAL_TAX_AFTER_CREDITS, D("16951.38")), (ITC_RECAPTURE, D("0"))),
            D("16951.38"),
        ),
        # T1 line 138 (line 41600) "Add lines 135 to 137.": lines 135 and 137, in line order.
        CREDITS_AGAINST_FEDERAL_TAX: SumLine(
            CREDITS_AGAINST_FEDERAL_TAX,
            ((POLITICAL_CREDIT, D("0.00")), (LABOUR_SPONSORED_FUNDS_CREDIT, D("0"))),
            D("0.00"),
        ),
        # Federal Worksheet column 1 line 7 "Line 5 plus line 6 =": line 5 is 0.
        POLITICAL_CREDIT_COLUMN_1_LINE_7: SumLine(
            POLITICAL_CREDIT_COLUMN_1_LINE_7,
            (
                (POLITICAL_CREDIT_COLUMN_1_LINE_5, D("0.00")),
                (POLITICAL_CREDIT_COLUMN_1_LINE_6, D("0.00")),
            ),
            D("0.00"),
        ),
        # Federal Worksheet column 2 line 7 "Line 5 plus line 6 =": line 5 is 0.
        POLITICAL_CREDIT_COLUMN_2_LINE_7: SumLine(
            POLITICAL_CREDIT_COLUMN_2_LINE_7,
            (
                (POLITICAL_CREDIT_COLUMN_2_LINE_5, D("0.00")),
                (POLITICAL_CREDIT_COLUMN_2_LINE_6, D("300.00")),
            ),
            D("300.00"),
        ),
        # Federal Worksheet column 3 line 7 "Line 5 plus line 6 =": line 5 is 0.
        POLITICAL_CREDIT_COLUMN_3_LINE_7: SumLine(
            POLITICAL_CREDIT_COLUMN_3_LINE_7,
            (
                (POLITICAL_CREDIT_COLUMN_3_LINE_5, D("0.00")),
                (POLITICAL_CREDIT_COLUMN_3_LINE_6, D("475.00")),
            ),
            D("475.00"),
        ),
        # T1 line 141 (line 41800) "Special taxes": Form T1172's line 10 or 13 and the RL-10 amount.
        SPECIAL_TAXES: SumLine(
            SPECIAL_TAXES,
            ((RESP_AIPS_ADDITIONAL_TAX, D("0")), (RL_10_LABOUR_SPONSORED_FUND_AMOUNT, D("0"))),
            D("0"),
        ),
        # T1 line 148 (line 43500) "Add lines 143 to 147. Total payable", in line order: line
        # 143 "Amount from line 42000" and line 147 (42800), the Ontario tax.
        TOTAL_PAYABLE: SumLine(
            TOTAL_PAYABLE,
            ((NET_FEDERAL_TAX, D("16951.38")), (ONTARIO_TAX, D("8945.77"))),
            D("25897.15"),
        ),
        # Schedule 6 line 5 "Add lines 1 to 4. Enter the result, even if it is "0". Working
        # income": line 1 "Employment income and other employment income from line 10100 and line
        # 10400 of the return" alone, as lines 2 to 4 are not triggered.
        WORKING_INCOME: SumLine(WORKING_INCOME, ((EMPLOYMENT_INCOME, D("110000")),), D("110000")),
        # Schedule 6 line 15 "Line 13 minus line 14 Enter this amount on line 23 and line 35.
        # Adjusted family net income": line 7, net income (line 23600), carried unchanged.
        ADJUSTED_FAMILY_NET_INCOME: SumLine(
            ADJUSTED_FAMILY_NET_INCOME, ((NET_INCOME, D("115000")),), D("115000")
        ),
        # Worksheet ON479 column 1 line 7 "Line 5 plus line 6": line 5 is 0.
        ontario.POLITICAL_CREDIT_COLUMN_1_LINE_7: SumLine(
            ontario.POLITICAL_CREDIT_COLUMN_1_LINE_7,
            (
                (ontario.POLITICAL_CREDIT_COLUMN_1_LINE_5, D("0.00")),
                (ontario.POLITICAL_CREDIT_COLUMN_1_LINE_6, D("0.00")),
            ),
            D("0.00"),
        ),
        # Worksheet ON479 column 2 line 7 "Line 5 plus line 6": line 5 is 0.
        ontario.POLITICAL_CREDIT_COLUMN_2_LINE_7: SumLine(
            ontario.POLITICAL_CREDIT_COLUMN_2_LINE_7,
            (
                (ontario.POLITICAL_CREDIT_COLUMN_2_LINE_5, D("0.00")),
                (ontario.POLITICAL_CREDIT_COLUMN_2_LINE_6, D("375.03")),
            ),
            D("375.03"),
        ),
        # Worksheet ON479 column 3 line 7 "Line 5 plus line 6": line 5 is 0.
        ontario.POLITICAL_CREDIT_COLUMN_3_LINE_7: SumLine(
            ontario.POLITICAL_CREDIT_COLUMN_3_LINE_7,
            (
                (ontario.POLITICAL_CREDIT_COLUMN_3_LINE_5, D("0.00")),
                (ontario.POLITICAL_CREDIT_COLUMN_3_LINE_6, D("958.41")),
            ),
            D("958.41"),
        ),
        # ON479 line 8 "Line 6 plus line 7 Family net income": the net income (line 6) and the
        # spouse's (line 7, 0 with no spouse).
        SENIORS_CARE_FAMILY_NET_INCOME: SumLine(
            SENIORS_CARE_FAMILY_NET_INCOME,
            ((NET_INCOME, D("115000.00")), (SPOUSE_NET_INCOME, D("0"))),
            D("115000.00"),
        ),
        # ON479 line 18 "Add lines 1, 2, 13, 14, 16, and 17.": lines 1, 13, 14, 16 and 17, in order.
        ONTARIO_CREDITS_SUBTOTAL: SumLine(
            ONTARIO_CREDITS_SUBTOTAL,
            (
                (FERTILITY_CREDIT, D("0")),
                (SENIORS_CARE_CREDIT, D("0")),
                (SENIORS_TRANSIT_CREDIT, D("0")),
                (ontario.POLITICAL_CREDIT, D("0.00")),
                (FLOW_THROUGH_SHARE_CREDIT, D("0")),
            ),
            D("0"),
        ),
        # ON479 line 21 "Line 19 plus line 20": line 19 carries line 18, and line 20 is the
        # co-operative education credit, 0 for no work placements.
        ONTARIO_CREDITS: SumLine(
            ONTARIO_CREDITS,
            ((ONTARIO_CREDITS_SUBTOTAL, D("0")), (COOP_EDUCATION_CREDIT, D("0"))),
            D("0"),
        ),
        # T1 line 165 (line 47900) "Provincial or territorial credits": ON479 line 21.
        PROVINCIAL_CREDITS: SumLine(PROVINCIAL_CREDITS, ((ONTARIO_CREDITS, D("0")),), D("0")),
        # T1 line 166 (line 48200) "Add lines 150 to 165. Total credits": line 150 (43700), line
        # 155 (45300), the Canada workers benefit, and line 165 (47900), in line order.
        TOTAL_CREDITS: SumLine(
            TOTAL_CREDITS,
            (
                (INCOME_TAX_DEDUCTED, D("25000")),
                (REFUNDABLE_MEDICAL_EXPENSE_SUPPLEMENT, D("0.00")),
                (CANADA_WORKERS_BENEFIT, D("0")),
                (PART_XII_2_TAX_CREDIT, D("0")),
                (EMPLOYEE_AND_PARTNER_GST_HST_REBATE, D("0")),
                (EDUCATOR_SCHOOL_SUPPLY_CREDIT, D("0")),
                (JOURNALISM_LABOUR_TAX_CREDIT, D("0")),
                (TAX_PAID_BY_INSTALMENTS, D("0")),
                (PROVINCIAL_CREDITS, D("0")),
            ),
            D("25000"),
        ),
        # The Ontario opportunities fund, line 1 "Amount from line 48400 above".
        ontario.REFUND_BEFORE_DONATION: SumLine(
            ontario.REFUND_BEFORE_DONATION, ((REFUND, D("0")),), D("0")
        ),
        # Federal Worksheet line 22100, line 4.
        CARRYING_CHARGES_INTEREST_EXPENSES_AND_OTHER_EXPENSES: SumLine(
            CARRYING_CHARGES_INTEREST_EXPENSES_AND_OTHER_EXPENSES,
            (
                (TOTAL_CARRYING_CHARGES, D("0")),
                (TOTAL_INTEREST_EXPENSES, D("0")),
                (TOTAL_OTHER_EXPENSES, D("0")),
            ),
            D("0"),
        ),
        # Form T1436 line 7.
        CAPITAL_GAINS_DEDUCTIONS_CLAIMED_1985_TO_2024: SumLine(
            CAPITAL_GAINS_DEDUCTIONS_CLAIMED_1985_TO_2024,
            (
                (CAPITAL_GAINS_DEDUCTIONS_1985_TO_1987, D("0")),
                (
                    CAPITAL_GAINS_DEDUCTIONS_1988_AND_1989_OTHER_THAN_ELIGIBLE_CAPITAL_PROPERTY,
                    D("0"),
                ),
                (CAPITAL_GAINS_DEDUCTIONS_1988_AND_1989_ELIGIBLE_CAPITAL_PROPERTY, D("0")),
                (CAPITAL_GAINS_DEDUCTIONS_1990_TO_1999, D("0")),
                (CAPITAL_GAINS_DEDUCTIONS_2000, D("0")),
                (CAPITAL_GAINS_DEDUCTIONS_2001_TO_2024, D("0")),
            ),
            D("0"),
        ),
        # Form T1436 line 14.
        OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_2024: SumLine(
            OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_2024,
            (
                (OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_1994, D("0")),
                (OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1994_TO_1996, D("0")),
                (OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1997_TO_1999, D("0")),
                (OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2000, D("0")),
                (OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2001_TO_2023, D("0")),
                (OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2024, D("0")),
            ),
            D("0"),
        ),
        # Schedule 15 line 5.
        FHSA_CONTRIBUTIONS_PLUS_VARIABLE_B_AMOUNT: SumLine(
            FHSA_CONTRIBUTIONS_PLUS_VARIABLE_B_AMOUNT,
            (
                (FHSA_CONTRIBUTIONS_IN_2025_BEFORE_FIRST_QUALIFYING_WITHDRAWAL, D("0")),
                (FHSA_VARIABLE_B_AMOUNT, D("0")),
            ),
            D("0"),
        ),
        # Schedule 15 line 11.
        FHSA_CONTRIBUTIONS_AFTER_FIRST_QUALIFYING_WITHDRAWAL: SumLine(
            FHSA_CONTRIBUTIONS_AFTER_FIRST_QUALIFYING_WITHDRAWAL,
            (
                (FHSA_CONTRIBUTIONS_IN_2024_AFTER_FIRST_QUALIFYING_WITHDRAWAL, D("0")),
                (FHSA_CONTRIBUTIONS_IN_2025_AFTER_FIRST_QUALIFYING_WITHDRAWAL, D("0")),
            ),
            D("0"),
        ),
        # Schedule 15 line 16.
        FHSA_ANNUAL_AMOUNT_WITH_CARRYFORWARD: SumLine(
            FHSA_ANNUAL_AMOUNT_WITH_CARRYFORWARD,
            ((FHSA_ANNUAL_AMOUNT, D("8000.00")), (FHSA_CARRYFORWARD_FOR_2025, D("0"))),
            D("8000.00"),
        ),
        # Schedule 15 line 19.
        FHSA_TOTAL_RRSP_TRANSFERS: SumLine(
            FHSA_TOTAL_RRSP_TRANSFERS,
            (
                (FHSA_RRSP_TRANSFERS_IN_2024_AND_PRIOR_YEARS, D("0")),
                (FHSA_RRSP_TRANSFERS_IN_2025, D("0")),
            ),
            D("0"),
        ),
        # Schedule 15 line 22.
        FHSA_TOTAL_DESIGNATED_TRANSFERS: SumLine(
            FHSA_TOTAL_DESIGNATED_TRANSFERS,
            (
                (FHSA_DESIGNATED_TRANSFERS_IN_2024_AND_PRIOR_YEARS, D("0")),
                (FHSA_DESIGNATED_TRANSFERS_IN_2025, D("0")),
            ),
            D("0"),
        ),
        # Schedule 15 line 32.
        FHSA_ANNUAL_AMOUNT_FOR_2024_WITH_CARRYFORWARD: SumLine(
            FHSA_ANNUAL_AMOUNT_FOR_2024_WITH_CARRYFORWARD,
            ((FHSA_ANNUAL_AMOUNT_FOR_2024, D("8000.00")), (FHSA_CARRYFORWARD_FOR_2024, D("0"))),
            D("8000.00"),
        ),
        # Schedule 15 line 35.
        FHSA_TRANSFER_AMOUNT_PLUS_VARIABLE_F_AMOUNT: SumLine(
            FHSA_TRANSFER_AMOUNT_PLUS_VARIABLE_F_AMOUNT,
            ((FHSA_TRANSFER_AMOUNT_AT_MOST_LIMIT, D("0")), (FHSA_VARIABLE_F_AMOUNT, D("0"))),
            D("0"),
        ),
        # Schedule 15 line 43.
        FHSA_TOTAL_ANNUAL_LIMITS: SumLine(
            FHSA_TOTAL_ANNUAL_LIMITS,
            ((FHSA_ANNUAL_LIMIT, D("0")), (FHSA_ANNUAL_LIMITS_FOR_2024_AND_PRIOR_YEARS, D("0"))),
            D("0"),
        ),
        # Schedule 15 line 54.
        FHSA_UNUSED_CONTRIBUTIONS_PLUS_CONTRIBUTIONS: SumLine(
            FHSA_UNUSED_CONTRIBUTIONS_PLUS_CONTRIBUTIONS,
            (
                (FHSA_UNUSED_CONTRIBUTIONS_BROUGHT_FORWARD, D("0")),
                (FHSA_CONTRIBUTIONS_IN_2025_BEFORE_FIRST_QUALIFYING_WITHDRAWAL, D("0")),
            ),
            D("0"),
        ),
        # Form T1436 line 4 "Total of column C from Chart A", for no unapplied losses.
        TOTAL_ADJUSTED_NET_CAPITAL_LOSSES: SumLine(
            TOTAL_ADJUSTED_NET_CAPITAL_LOSSES,
            (
                (ADJUSTED_GROSS_CAPITAL_LOSSES_1985_TO_1987, D("0.00")),
                (ADJUSTED_GROSS_CAPITAL_LOSSES_1988_AND_1989, D("0.00")),
                (ADJUSTED_GROSS_CAPITAL_LOSSES_1990_TO_1999, D("0.00")),
                (ADJUSTED_GROSS_CAPITAL_LOSSES_2001_TO_2024, D("0.00")),
            ),
            D("0.00"),
        ),
        # Federal Worksheet "Line 45200 - Refundable medical expense supplement" (T1 line 154),
        # Return A: line 21500 and line 33200 are 0, so line 11 and line 13 are 0.
        MEDICAL_SUPPLEMENT_COLUMN_2_LINE_2: SumLine(
            output=MEDICAL_SUPPLEMENT_COLUMN_2_LINE_2,
            parts=(
                (
                    SPOUSE_UCCB_REPAYMENT,
                    D("0"),
                ),
                (
                    SPOUSE_RDSP_INCOME_REPAYMENT,
                    D("0"),
                ),
            ),
            total=D("0"),
        ),
        MEDICAL_SUPPLEMENT_COLUMN_2_LINE_3: SumLine(
            output=MEDICAL_SUPPLEMENT_COLUMN_2_LINE_3,
            parts=(
                (
                    SPOUSE_NET_INCOME_BEFORE_ADJUSTMENTS,
                    D("0"),
                ),
                (
                    MEDICAL_SUPPLEMENT_COLUMN_2_LINE_2,
                    D("0"),
                ),
            ),
            total=D("0"),
        ),
        MEDICAL_SUPPLEMENT_COLUMN_2_LINE_4: SumLine(
            output=MEDICAL_SUPPLEMENT_COLUMN_2_LINE_4,
            parts=(
                (
                    SPOUSE_UNIVERSAL_CHILD_CARE_BENEFIT,
                    D("0"),
                ),
                (
                    SPOUSE_RDSP_INCOME,
                    D("0"),
                ),
            ),
            total=D("0"),
        ),
        MEDICAL_SUPPLEMENT_EMPLOYMENT_DEDUCTIONS: SumLine(
            output=MEDICAL_SUPPLEMENT_EMPLOYMENT_DEDUCTIONS,
            parts=(
                (
                    RPP_DEDUCTION,
                    D("0"),
                ),
                (
                    UNION_DUES,
                    D("2000"),
                ),
                (
                    OTHER_EMPLOYMENT_EXPENSES,
                    D("0"),
                ),
                (
                    CLERGY_RESIDENCE_DEDUCTION,
                    D("0"),
                ),
            ),
            total=D("2000"),
        ),
        MEDICAL_SUPPLEMENT_EMPLOYMENT_INCOME: SumLine(
            output=MEDICAL_SUPPLEMENT_EMPLOYMENT_INCOME,
            parts=(
                (
                    EMPLOYMENT_INCOME,
                    D("110000"),
                ),
                (
                    OTHER_EMPLOYMENT_INCOME,
                    D("0"),
                ),
            ),
            total=D("110000"),
        ),
        MEDICAL_SUPPLEMENT_SELF_EMPLOYMENT_INCOME: SumLine(
            output=MEDICAL_SUPPLEMENT_SELF_EMPLOYMENT_INCOME,
            parts=(
                (
                    NET_BUSINESS_INCOME,
                    D("0"),
                ),
                (
                    NET_PROFESSIONAL_INCOME,
                    D("0"),
                ),
                (
                    NET_COMMISSION_INCOME,
                    D("0"),
                ),
                (
                    NET_FARMING_INCOME,
                    D("0"),
                ),
                (
                    NET_FISHING_INCOME,
                    D("0"),
                ),
            ),
            total=D("0"),
        ),
        MEDICAL_SUPPLEMENT_WORKING_INCOME: SumLine(
            output=MEDICAL_SUPPLEMENT_WORKING_INCOME,
            parts=(
                (
                    MEDICAL_SUPPLEMENT_EMPLOYMENT_WORKING_INCOME,
                    D("108000"),
                ),
                (
                    MEDICAL_SUPPLEMENT_SELF_EMPLOYMENT_INCOME,
                    D("0"),
                ),
            ),
            total=D("108000"),
        ),
        MEDICAL_SUPPLEMENT_LINE_11: SumLine(
            output=MEDICAL_SUPPLEMENT_LINE_11,
            parts=(
                (
                    DISABILITY_SUPPORTS_DEDUCTION,
                    D("0"),
                ),
                (
                    MEDICAL_CLAIM,
                    D("0"),
                ),
            ),
            total=D("0"),
        ),
        MEDICAL_SUPPLEMENT_COLUMN_1_LINE_3: SumLine(
            output=MEDICAL_SUPPLEMENT_COLUMN_1_LINE_3,
            parts=(
                (
                    NET_INCOME_BEFORE_ADJUSTMENTS,
                    D("115000.00"),
                ),
                (
                    UCCB_AND_RDSP_INCOME_REPAYMENTS,
                    D("0"),
                ),
            ),
            total=D("115000.00"),
        ),
        MEDICAL_SUPPLEMENT_LINE_6: SumLine(
            output=MEDICAL_SUPPLEMENT_LINE_6,
            parts=(
                (
                    MEDICAL_SUPPLEMENT_COLUMN_1_LINE_5,
                    D("115000.00"),
                ),
                (
                    MEDICAL_SUPPLEMENT_COLUMN_2_LINE_5,
                    D("0"),
                ),
            ),
            total=D("115000.00"),
        ),
    }
