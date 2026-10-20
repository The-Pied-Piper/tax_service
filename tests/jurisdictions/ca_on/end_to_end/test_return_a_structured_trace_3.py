"""CA-ON 2025 end to end, Return A: return a structured trace 3."""

from __future__ import annotations

from fractions import Fraction as ExactFraction

from app.domain.parameters.amount import Amount
from app.domain.parameters.credit import Credit
from app.domain.parameters.factor import Factor
from app.domain.parameters.fraction import Fraction
from app.domain.parameters.taper import Taper
from app.domain.trace import (
    CappedAmountLine,
    CreditAmountLine,
    FractionAppliedLine,
    MultipleOverLine,
    PerUnitAmountLine,
    SubtractedLine,
    TaperedAmountLine,
    ThresholdGateLine,
    TimesCountLine,
)
from app.jurisdictions.ca.catalog import (
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
    AGE_INCOME_THRESHOLD,
    AGE_MAXIMUM,
    AGED_18_OR_OLDER_AT_END_OF_2025,
    BASIC_PERSONAL_AMOUNT,
    BORN_IN_1960_OR_EARLIER,
    BUSINESS_INVESTMENT_LOSS,
    BUSINESS_INVESTMENT_LOSS_AFTER_REDUCTION,
    BUSINESS_INVESTMENT_LOSS_REDUCTION,
    BUSINESS_INVESTMENT_LOSS_REDUCTION_AVAILABLE,
    CANADA_EMPLOYMENT_AMOUNT,
    CAPITAL_GAINS_DEDUCTIONS_CLAIMED_1985_TO_2024,
    CAPITAL_GIFT_GAINS_DEDUCTION,
    CAPITAL_GIFT_TAXABLE_GAINS,
    CAPITAL_PROPERTY_GIFTS,
    CHILD_CARE_EARNED_INCOME,
    CHILD_CARE_EARNED_INCOME_LIMIT,
    CHILD_CARE_LIMIT_FOR_CHILDREN_SEVEN_TO_SIXTEEN,
    CHILD_CARE_LIMIT_FOR_CHILDREN_UNDER_SEVEN,
    CHILD_CARE_LIMIT_FOR_CHILDREN_WITH_DISABILITY,
    CHILDREN_SEVEN_TO_SIXTEEN,
    CHILDREN_UNDER_SEVEN,
    CHILDREN_WITH_DISABILITY,
    CPP_BASE_CONTRIBUTIONS_ON_SELF_EMPLOYMENT,
    CPP_DEDUCTION_ON_SELF_EMPLOYMENT,
    CPP_PART_4_COMPLETED,
    CPP_PAYABLE_ON_SELF_EMPLOYMENT,
    DEDUCTIONS_FROM_TOTAL_INCOME,
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
    EMPLOYMENT_INCOME,
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
    GROSS_RENTAL_INCOME,
    HIGH_INCOME_DONATIONS,
    INFIRM_CHILDREN,
    INFIRM_CHILDREN_AMOUNT,
    INTEREST_AND_OTHER_INVESTMENT_INCOME,
    INVESTMENT_INCOME_BEFORE_PRIOR_YEARS,
    INVESTMENT_INCOME_REPORTED_IN_PREVIOUS_YEARS,
    LABOUR_SPONSORED_FUNDS_CREDIT,
    LABOUR_SPONSORED_FUNDS_CREDIT_BEFORE_MAXIMUM,
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
    NET_CAPITAL_LOSSES_OF_OTHER_YEARS,
    NET_INCOME,
    NET_INCOME_BEFORE_ADJUSTMENTS,
    NET_INCOME_LESS_UCCB_AND_RDSP_INCOME,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_2024,
    OTHER_DIVIDENDS_GROSSED_UP,
    OTHER_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP,
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
    REFUND_OR_BALANCE_OWING,
    REFUNDABLE_MEDICAL_EXPENSE_SUPPLEMENT,
    REGULAR_RATE_DONATIONS,
    REMAINING_ADJUSTED_LOSSES_1985_TO_1987,
    REMAINING_ADJUSTED_LOSSES_1988_AND_1989,
    REMAINING_ADJUSTED_LOSSES_1990_TO_1999,
    REMAINING_ADJUSTED_LOSSES_2001_TO_2024,
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
    SELF_EMPLOYED_CPP_BASE_CREDIT,
    SELF_EMPLOYED_CPP_CONTRIBUTIONS_PAYABLE,
    SELF_EMPLOYED_CPP_DEDUCTION,
    SELF_EMPLOYED_EI_PREMIUMS,
    SPOUSE_AMOUNT,
    SPOUSE_AMOUNT_BEFORE_COUNT,
    SPOUSE_CAREGIVER_AMOUNT,
    SPOUSE_CAREGIVER_AMOUNT_BEFORE_COUNT,
    SPOUSE_CAREGIVER_BASE,
    SPOUSE_CAREGIVER_BEFORE_MAXIMUM,
    SPOUSE_CAREGIVER_ELIGIBLE,
    SPOUSE_CAREGIVER_LIMIT,
    SPOUSE_INFIRMITY_SUPPLEMENT,
    SPOUSES_CLAIMED,
    TOP_UP_THRESHOLD,
    TOTAL_CREDITS,
    TOTAL_INCOME,
    TOTAL_PAYABLE,
    UCCB_AND_RDSP_INCOME,
    UNAPPLIED_NET_CAPITAL_LOSSES_1985_TO_1987,
    UNAPPLIED_NET_CAPITAL_LOSSES_1988_AND_1989,
    UNAPPLIED_NET_CAPITAL_LOSSES_1990_TO_1999,
    UNAPPLIED_NET_CAPITAL_LOSSES_2001_TO_2024,
    UNUSED_RRSP_CONTRIBUTIONS_CARRIED_FORWARD,
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
from tests.jurisdictions.ca_on.end_to_end.support import CENT, D, return_a


def test_the_trace_records_each_total_as_a_structured_line() -> None:
    trace = return_a().trace
    subtracted = {line.output: line for line in trace if isinstance(line, SubtractedLine)}
    amounts = {line.output: line for line in trace if isinstance(line, CreditAmountLine)}
    tapered = {line.output: line for line in trace if isinstance(line, TaperedAmountLine)}
    capped = {line.output: line for line in trace if isinstance(line, CappedAmountLine)}
    per_unit = {line.output: line for line in trace if isinstance(line, PerUnitAmountLine)}
    multiples = {line.output: line for line in trace if isinstance(line, MultipleOverLine)}
    times = {line.output: line for line in trace if isinstance(line, TimesCountLine)}
    gated = {line.output: line for line in trace if isinstance(line, ThresholdGateLine)}
    fractions = {line.output: line for line in trace if isinstance(line, FractionAppliedLine)}
    assert subtracted == {
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
            minuend=NET_INCOME,
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
        # T1 line 23400.
        NET_INCOME_BEFORE_ADJUSTMENTS: SubtractedLine(
            output=NET_INCOME_BEFORE_ADJUSTMENTS,
            minuend=TOTAL_INCOME,
            minuend_amount=D("120000"),
            subtrahend=DEDUCTIONS_FROM_TOTAL_INCOME,
            subtrahend_amount=D("5000"),
            result=D("115000"),
        ),
        # Form T1436 Chart A: what is left of line 13 (the amount claimed, 0) after each of the
        # older rows, and column E "Remaining adjusted net capital losses (column C minus column
        # D)".
        ADJUSTED_LOSSES_LEFT_AFTER_1985_TO_1987: SubtractedLine(
            output=ADJUSTED_LOSSES_LEFT_AFTER_1985_TO_1987,
            minuend=NET_CAPITAL_LOSSES_OF_OTHER_YEARS,
            minuend_amount=D("0"),
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
    }
    assert tapered == {
        BASIC_PERSONAL_AMOUNT: TaperedAmountLine(
            output=BASIC_PERSONAL_AMOUNT,
            base=NET_INCOME,
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
    }
    assert times == {
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
        )
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
    }
