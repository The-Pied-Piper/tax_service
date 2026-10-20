"""CA-ON 2025 end to end, Return A: return a structured trace 4."""

from __future__ import annotations

from app.domain.parameters.contribution_tier import ContributionTier
from app.domain.parameters.rate import Rate
from app.domain.trace import (
    AtMostLine,
    ChosenByCountLine,
    ContributionTierLine,
    GreaterOfLine,
    ItemsTotalLine,
    LesserOfLine,
    PlacementCreditLine,
    QuotientLine,
    RecordCountLine,
    RecordTotalLine,
    SubtractedNotBelowZeroLine,
    SurchargeTierLine,
)
from app.jurisdictions.ca.catalog import (
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
    AGE_AMOUNT_BEFORE_COUNT,
    AGE_INCOME_OVER_THRESHOLD,
    AGE_INCOME_THRESHOLD,
    AGE_MAXIMUM,
    AGE_REDUCTION,
    BASIC_PERSONAL_AMOUNT,
    BUSINESS_INVESTMENT_LOSS,
    BUSINESS_INVESTMENT_LOSS_REDUCTION,
    BUSINESS_INVESTMENT_LOSS_REDUCTION_AVAILABLE,
    CANADA_WORKERS_BENEFIT,
    CANADA_WORKERS_BENEFIT_WITH_DEPENDANT,
    CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT,
    CHARITABLE_DONATIONS_CLAIMED,
    CHARITABLE_DONATIONS_LIMIT,
    CHILD_CARE_BASIC_LIMIT,
    CHILD_CARE_EARNED_INCOME_LIMIT,
    CHILD_CARE_EXPENSES,
    CHILD_CARE_EXPENSES_PAID,
    CPP_BASE_CONTRIBUTIONS,
    CPP_FIRST_ADDITIONAL_CONTRIBUTIONS,
    CPP_SECOND_ADDITIONAL_CONTRIBUTIONS,
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
    DONATION_FIRST_TIER_MAXIMUM,
    DONATION_HIGH_INCOME_THRESHOLD,
    DONATION_LIMIT_WITH_CAPITAL_GIFTS,
    DONATIONS_AND_GIFTS_TOTAL,
    DONATIONS_FIRST_TIER,
    DONATIONS_OVER_FIRST_TIER,
    DONATIONS_OVER_FIRST_TIER_AFTER_2016_GIFTS,
    ECOLOGICAL_GIFTS_BEFORE_2016,
    EI_PREMIUMS,
    ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT,
    EMPLOYMENT_INCOME,
    FEDERAL_BASIC_TAX,
    FEDERAL_TAX_AFTER_CREDITS,
    FEDERAL_TAX_LESS_CREDITS,
    FEDERAL_TAX_WITH_ITC_RECAPTURE,
    FHSA_ANNUAL_AMOUNT_AFTER_TRANSFERS,
    FHSA_ANNUAL_AMOUNT_FOR_2024_WITH_CARRYFORWARD,
    FHSA_ANNUAL_AMOUNT_WITH_CARRYFORWARD,
    FHSA_ANNUAL_LIMIT,
    FHSA_ANNUAL_LIMIT_FROM_STEP_2,
    FHSA_ANNUAL_LIMITS_LESS_DEDUCTIONS,
    FHSA_CONTRIBUTIONS_AFTER_FIRST_QUALIFYING_WITHDRAWAL,
    FHSA_CONTRIBUTIONS_DEDUCTED,
    FHSA_CONTRIBUTIONS_LIMIT,
    FHSA_CONTRIBUTIONS_PLUS_VARIABLE_B_AMOUNT,
    FHSA_DEDUCTION,
    FHSA_DESIGNATED_WITHDRAWALS_IN_2025,
    FHSA_EXCESS_DESIGNATED_WITHDRAWALS,
    FHSA_LIFETIME_LIMIT_LESS_DEDUCTIONS,
    FHSA_LIFETIME_LIMIT_LESS_DEDUCTIONS_AND_TRANSFERS,
    FHSA_MAXIMUM_DEDUCTION,
    FHSA_MAXIMUM_PARTICIPATION_PERIOD_ENDED,
    FHSA_NET_RRSP_TRANSFER_AMOUNT,
    FHSA_NET_RRSP_TRANSFER_AMOUNT_FOR_2024_AND_PRIOR_YEARS,
    FHSA_NET_TRANSFER_AMOUNT_AFTER_PRIOR_YEARS,
    FHSA_NET_TRANSFER_AMOUNT_LESS_VARIABLE_H_AMOUNT,
    FHSA_TRANSFER_AMOUNT_AT_MOST_LIMIT,
    FHSA_VARIABLE_H_AMOUNT,
    HIGH_INCOME_DONATIONS,
    INCOME_SUPPORT_BENEFITS,
    MEDICAL_EXPENSES,
    MEDICAL_EXPENSES_OVER_THRESHOLD,
    MEDICAL_SUPPLEMENT_COLUMN_1_LINE_3,
    MEDICAL_SUPPLEMENT_COLUMN_1_LINE_5,
    MEDICAL_SUPPLEMENT_COLUMN_2_LINE_3,
    MEDICAL_SUPPLEMENT_COLUMN_2_LINE_4,
    MEDICAL_SUPPLEMENT_COLUMN_2_LINE_5,
    MEDICAL_SUPPLEMENT_EMPLOYMENT_DEDUCTIONS,
    MEDICAL_SUPPLEMENT_EMPLOYMENT_INCOME_LESS_WAGE_LOSS,
    MEDICAL_SUPPLEMENT_EMPLOYMENT_WORKING_INCOME,
    MEDICAL_SUPPLEMENT_INCOME_THRESHOLD,
    MEDICAL_SUPPLEMENT_LINE_6,
    MEDICAL_SUPPLEMENT_LINE_8,
    MEDICAL_SUPPLEMENT_LINE_14,
    MEDICAL_SUPPLEMENT_LINE_15,
    MEDICAL_SUPPLEMENT_LINE_16,
    MEDICAL_THRESHOLD,
    NET_CAPITAL_LOSSES_AVAILABLE_TO_CLAIM,
    NET_CAPITAL_LOSSES_CLAIMED,
    NET_CAPITAL_LOSSES_OF_OTHER_YEARS,
    NET_INCOME,
    OTHER_PAYMENTS_DEDUCTION,
    OTHER_PAYMENTS_DEDUCTION_AFTER_LIMIT,
    OTHER_PAYMENTS_WORKSHEET_LINE_9_OVER_LIMIT,
    OTHER_PAYMENTS_WORKSHEET_REQUIRED,
    POLITICAL_CONTRIBUTIONS,
    POLITICAL_CREDIT_COLUMN_1_LINE_2,
    POLITICAL_CREDIT_COLUMN_1_LINE_3,
    POLITICAL_CREDIT_COLUMN_2_LINE_2,
    POLITICAL_CREDIT_COLUMN_2_LINE_3,
    POLITICAL_CREDIT_COLUMN_3_LINE_2,
    POLITICAL_CREDIT_COLUMN_3_LINE_3,
    REFUND,
    RESP_AIPS_ADDITIONAL_TAX,
    RESP_AIPS_CONTRIBUTIONS_COUNTED,
    RESP_AIPS_LIMIT_REMAINING,
    RESP_AIPS_PART_A_APPLIES,
    RESP_AIPS_PART_B_TAX,
    RESP_AIPS_RECEIVED_PART_A,
    RESP_AIPS_REDUCTION,
    RESP_AIPS_RRSP_CONTRIBUTIONS,
    RRSP_AMOUNT_DEDUCTED,
    RRSP_CONTRIBUTIONS_AVAILABLE,
    RRSP_DEDUCTION,
    RRSP_DEDUCTION_LIMIT,
    RRSP_DEDUCTION_MAXIMUM,
    SPOUSE_AMOUNT,
    SPOUSE_AMOUNT_BASIS,
    SPOUSE_AMOUNT_BEFORE_COUNT,
    SPOUSE_CAREGIVER_AMOUNT_BEFORE_COUNT,
    SPOUSE_CAREGIVER_BASE,
    SPOUSE_CAREGIVER_BEFORE_MAXIMUM,
    SPOUSE_CAREGIVER_LIMIT,
    SPOUSE_NET_INCOME,
    TAXABLE_CAPITAL_GAINS,
    TAXABLE_INCOME,
    TAXABLE_INCOME_OVER_DONATION_THRESHOLD,
    TOP_UP_CREDITS_BASE,
    TOP_UP_EXCESS,
    TOP_UP_THRESHOLD,
    TOTAL_ADJUSTED_NET_CAPITAL_LOSSES,
    TOTAL_CHARITABLE_DONATIONS,
    TOTAL_CREDITS,
    TOTAL_INCOME,
    TOTAL_PAYABLE,
    UCCB_AND_RDSP_INCOME,
    WORKING_INCOME,
)
from app.jurisdictions.ca_on import catalog as ontario
from app.jurisdictions.ca_on.catalog import (
    COMMUNITY_FOOD_PROGRAM_CREDIT,
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
    ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_MAXIMUM,
    ELIGIBLE_DEPENDANT_BASE,
    FLOW_THROUGH_SHARE_EXPENSES,
    FLOW_THROUGH_SHARE_SLIP_EXPENSES,
    LIFT_CREDIT,
    LIFT_MAXIMUM_CREDIT,
    LIFT_REDUCTION,
    ONTARIO_BASIC_TAX,
    ONTARIO_HEALTH_PREMIUM,
    ONTARIO_SURTAX,
    ONTARIO_TAX_AFTER_CREDITS,
    ONTARIO_TAX_AFTER_FOOD_CREDIT,
    ONTARIO_TAX_AFTER_LIFT_CREDIT,
    ONTARIO_TAX_AFTER_REDUCTION,
    ONTARIO_TAX_REDUCTION,
    ONTARIO_TAX_WITH_SURTAX,
    SENIORS_CARE_AMOUNT,
    SENIORS_CARE_BASE_AMOUNT,
    SENIORS_CARE_BEFORE_CLAIM,
    SENIORS_CARE_FAMILY_NET_INCOME,
    SENIORS_CARE_INCOME_OVER_BASE,
    SENIORS_CARE_REDUCTION,
)
from tests.jurisdictions.ca_on.end_to_end.support import CENT, D, return_a


def test_the_trace_records_each_total_as_a_structured_line() -> None:
    trace = return_a().trace
    floored = {line.output: line for line in trace if isinstance(line, SubtractedNotBelowZeroLine)}
    tiers = {line.output: line for line in trace if isinstance(line, ContributionTierLine)}
    lesser = {line.output: line for line in trace if isinstance(line, LesserOfLine)}
    at_most = {line.output: line for line in trace if isinstance(line, AtMostLine)}
    surcharged = [
        line
        for line in trace
        if isinstance(line, SurchargeTierLine) and line.output == ONTARIO_SURTAX
    ]
    lift_tiers = [
        line
        for line in trace
        if isinstance(line, SurchargeTierLine) and line.output == LIFT_REDUCTION
    ]
    premium_tiers = [
        line
        for line in trace
        if isinstance(line, SurchargeTierLine) and line.output == ONTARIO_HEALTH_PREMIUM
    ]
    cwb_basic_tiers = [
        line
        for line in trace
        if isinstance(line, SurchargeTierLine)
        and line.output
        in (CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT, CWB_BEFORE_REDUCTION_WITH_DEPENDANT)
    ]
    cwb_reduction_tiers = [
        line
        for line in trace
        if isinstance(line, SurchargeTierLine)
        and line.output in (CWB_REDUCTION_WITHOUT_DEPENDANT, CWB_REDUCTION_WITH_DEPENDANT)
    ]
    chosen = {line.output: line for line in trace if isinstance(line, ChosenByCountLine)}
    record_totals = {line.output: line for line in trace if isinstance(line, RecordTotalLine)}
    quotients = {line.output: line for line in trace if isinstance(line, QuotientLine)}
    record_counts = {line.output: line for line in trace if isinstance(line, RecordCountLine)}
    placement_credits = [line for line in trace if isinstance(line, PlacementCreditLine)]
    items_totals = {
        line.output: line
        for line in trace
        if isinstance(line, ItemsTotalLine) and line.output is COOP_EDUCATION_CREDIT
    }
    assert lesser == {
        # Form T1172 line 3 "Amount from line 1 or 2, whichever is less" and line 7 "Amount from
        # line 3 or 6, whichever is less", for no AIPs.
        RESP_AIPS_CONTRIBUTIONS_COUNTED: LesserOfLine(
            RESP_AIPS_CONTRIBUTIONS_COUNTED,
            ((RESP_AIPS_RECEIVED_PART_A, D("0")), (RESP_AIPS_RRSP_CONTRIBUTIONS, D("0"))),
            D("0"),
        ),
        RESP_AIPS_REDUCTION: LesserOfLine(
            RESP_AIPS_REDUCTION,
            (
                (RESP_AIPS_CONTRIBUTIONS_COUNTED, D("0")),
                (RESP_AIPS_LIMIT_REMAINING, D("50000.00")),
            ),
            D("0"),
        ),
        # Schedule 9 chart for line 33700, line 4 "Enter whichever is less: amount from line 2 or
        # line 3." and line 5 "amount from line 1 or line 4", both 0.
        DEPRECIABLE_GIFT_PROCEEDS_OR_COST: LesserOfLine(
            DEPRECIABLE_GIFT_PROCEEDS_OR_COST,
            ((DEPRECIABLE_GIFT_NET_PROCEEDS, D("0")), (DEPRECIABLE_GIFT_CAPITAL_COST, D("0"))),
            D("0"),
        ),
        DEPRECIABLE_GIFTS: LesserOfLine(
            DEPRECIABLE_GIFTS,
            (
                (DEPRECIABLE_GIFT_RECAPTURED_DEPRECIATION, D("0")),
                (DEPRECIABLE_GIFT_PROCEEDS_OR_COST, D("0")),
            ),
            D("0"),
        ),
        # Schedule 9 line 9 "Enter whichever is less: amount A or line 8.": amount A is the net
        # income, 115000, above line 8 (75% of it), so line 9 is line 8 when line 7 is 0. Line 10
        # "amount from line 5 or line 9", line 13 "amount from line 12 or $200." and line 20 "amount
        # from line 16 or line 19".
        CHARITABLE_DONATIONS_LIMIT: LesserOfLine(
            CHARITABLE_DONATIONS_LIMIT,
            ((NET_INCOME, D("115000")), (DONATION_LIMIT_WITH_CAPITAL_GIFTS, D("86250"))),
            D("86250"),
        ),
        CHARITABLE_DONATIONS_CLAIMED: LesserOfLine(
            CHARITABLE_DONATIONS_CLAIMED,
            ((TOTAL_CHARITABLE_DONATIONS, D("0")), (CHARITABLE_DONATIONS_LIMIT, D("86250"))),
            D("0"),
        ),
        DONATIONS_FIRST_TIER: LesserOfLine(
            DONATIONS_FIRST_TIER,
            ((DONATIONS_AND_GIFTS_TOTAL, D("0")), (DONATION_FIRST_TIER_MAXIMUM, D("200.00"))),
            D("0"),
        ),
        HIGH_INCOME_DONATIONS: LesserOfLine(
            HIGH_INCOME_DONATIONS,
            (
                (DONATIONS_OVER_FIRST_TIER_AFTER_2016_GIFTS, D("0")),
                (TAXABLE_INCOME_OVER_DONATION_THRESHOLD, D("0")),
            ),
            D("0"),
        ),
        RRSP_DEDUCTION_MAXIMUM: LesserOfLine(
            RRSP_DEDUCTION_MAXIMUM,
            ((RRSP_CONTRIBUTIONS_AVAILABLE, D("1926")), (RRSP_DEDUCTION_LIMIT, D("19800"))),
            D("1926"),
        ),
        # Form T778 line 7 "Enter whichever amount is the least: line 4, line 5 or line 6.", in
        # that order: lines 4 and 5 are both 0, and the first listed is produced.
        CHILD_CARE_EXPENSES: LesserOfLine(
            CHILD_CARE_EXPENSES,
            (
                (CHILD_CARE_BASIC_LIMIT, D("0")),
                (CHILD_CARE_EXPENSES_PAID, D("0")),
                (CHILD_CARE_EARNED_INCOME_LIMIT, D("73333.33")),
            ),
            D("0"),
        ),
        # Form T1436 line 17.
        BUSINESS_INVESTMENT_LOSS_REDUCTION: LesserOfLine(
            BUSINESS_INVESTMENT_LOSS_REDUCTION,
            (
                (BUSINESS_INVESTMENT_LOSS_REDUCTION_AVAILABLE, D("0")),
                (BUSINESS_INVESTMENT_LOSS, D("0")),
            ),
            D("0"),
        ),
        # Schedule 15 line 33.
        FHSA_TRANSFER_AMOUNT_AT_MOST_LIMIT: LesserOfLine(
            FHSA_TRANSFER_AMOUNT_AT_MOST_LIMIT,
            (
                (FHSA_NET_TRANSFER_AMOUNT_LESS_VARIABLE_H_AMOUNT, D("0")),
                (FHSA_ANNUAL_AMOUNT_FOR_2024_WITH_CARRYFORWARD, D("8000.00")),
            ),
            D("0"),
        ),
        # Schedule 15 line 40, Step 2's result.
        FHSA_ANNUAL_LIMIT_FROM_STEP_2: LesserOfLine(
            FHSA_ANNUAL_LIMIT_FROM_STEP_2,
            (
                (FHSA_CONTRIBUTIONS_LIMIT, D("0")),
                (FHSA_ANNUAL_AMOUNT_AFTER_TRANSFERS, D("8000.00")),
            ),
            D("0"),
        ),
        # Schedule 15 line 51.
        FHSA_MAXIMUM_DEDUCTION: LesserOfLine(
            FHSA_MAXIMUM_DEDUCTION,
            (
                (FHSA_ANNUAL_LIMITS_LESS_DEDUCTIONS, D("0")),
                (FHSA_LIFETIME_LIMIT_LESS_DEDUCTIONS_AND_TRANSFERS, D("40000.00")),
            ),
            D("0"),
        ),
        # Form T1436 line 6 "Enter whichever is less: amount from line 4 or line 5.": the total of
        # column C, 0.00, is below the taxable capital gains of 10000.00 (half of the 20000 gain).
        NET_CAPITAL_LOSSES_AVAILABLE_TO_CLAIM: LesserOfLine(
            NET_CAPITAL_LOSSES_AVAILABLE_TO_CLAIM,
            (
                (TOTAL_ADJUSTED_NET_CAPITAL_LOSSES, D("0.00")),
                (TAXABLE_CAPITAL_GAINS, D("10000.00")),
            ),
            D("0.00"),
        ),
        # Form T1436 Chart A column D "Total adjusted net capital losses applied against taxable
        # capital gains in 2025": the lesser of column C and what is left of line 13, 0 for no
        # claim.
        ADJUSTED_LOSSES_APPLIED_1985_TO_1987: LesserOfLine(
            ADJUSTED_LOSSES_APPLIED_1985_TO_1987,
            (
                (ADJUSTED_GROSS_CAPITAL_LOSSES_1985_TO_1987, D("0.00")),
                (NET_CAPITAL_LOSSES_OF_OTHER_YEARS, D("0")),
            ),
            D("0.00"),
        ),
        ADJUSTED_LOSSES_APPLIED_1988_AND_1989: LesserOfLine(
            ADJUSTED_LOSSES_APPLIED_1988_AND_1989,
            (
                (ADJUSTED_GROSS_CAPITAL_LOSSES_1988_AND_1989, D("0.00")),
                (ADJUSTED_LOSSES_LEFT_AFTER_1985_TO_1987, D("0.00")),
            ),
            D("0.00"),
        ),
        ADJUSTED_LOSSES_APPLIED_1990_TO_1999: LesserOfLine(
            ADJUSTED_LOSSES_APPLIED_1990_TO_1999,
            (
                (ADJUSTED_GROSS_CAPITAL_LOSSES_1990_TO_1999, D("0.00")),
                (ADJUSTED_LOSSES_LEFT_AFTER_1988_AND_1989, D("0.00")),
            ),
            D("0.00"),
        ),
        ADJUSTED_LOSSES_APPLIED_2001_TO_2024: LesserOfLine(
            ADJUSTED_LOSSES_APPLIED_2001_TO_2024,
            (
                (ADJUSTED_GROSS_CAPITAL_LOSSES_2001_TO_2024, D("0.00")),
                (ADJUSTED_LOSSES_LEFT_AFTER_1990_TO_1999, D("0.00")),
            ),
            D("0.00"),
        ),
    }
    assert at_most == {
        RRSP_DEDUCTION: AtMostLine(
            output=RRSP_DEDUCTION,
            amount_kind=RRSP_AMOUNT_DEDUCTED,
            amount_value=D("1926"),
            bound=RRSP_DEDUCTION_MAXIMUM,
            bound_value=D("1926"),
        ),
        # Schedule 15 line 57 (T1 line 20805).
        FHSA_DEDUCTION: AtMostLine(
            output=FHSA_DEDUCTION,
            amount_kind=FHSA_CONTRIBUTIONS_DEDUCTED,
            amount_value=D("0"),
            bound=FHSA_MAXIMUM_DEDUCTION,
            bound_value=D("0"),
        ),
        # Form T1436 line 7 "Enter the amount of losses you want to claim (3).", which is T1 line
        # 25300 and line 13: a claim of 0 against a line 6 of 0.00.
        NET_CAPITAL_LOSSES_OF_OTHER_YEARS: AtMostLine(
            output=NET_CAPITAL_LOSSES_OF_OTHER_YEARS,
            amount_kind=NET_CAPITAL_LOSSES_CLAIMED,
            amount_value=D("0"),
            bound=NET_CAPITAL_LOSSES_AVAILABLE_TO_CLAIM,
            bound_value=D("0.00"),
        ),
    }
    assert tiers == {
        CPP_BASE_CONTRIBUTIONS: ContributionTierLine(
            CPP_BASE_CONTRIBUTIONS,
            EMPLOYMENT_INCOME,
            D("110000"),
            ContributionTier(Rate(D("0.0495")), D("3500"), D("71300"), D("3356.10")),
            CENT,
            D("67800"),
            D("3356.10"),
        ),
        CPP_FIRST_ADDITIONAL_CONTRIBUTIONS: ContributionTierLine(
            CPP_FIRST_ADDITIONAL_CONTRIBUTIONS,
            EMPLOYMENT_INCOME,
            D("110000"),
            ContributionTier(Rate(D("0.01")), D("3500"), D("71300"), D("678.00")),
            CENT,
            D("67800"),
            D("678.00"),
        ),
        CPP_SECOND_ADDITIONAL_CONTRIBUTIONS: ContributionTierLine(
            CPP_SECOND_ADDITIONAL_CONTRIBUTIONS,
            EMPLOYMENT_INCOME,
            D("110000"),
            ContributionTier(Rate(D("0.04")), D("71300"), D("81200"), D("396.00")),
            CENT,
            D("9900"),
            D("396.00"),
        ),
        EI_PREMIUMS: ContributionTierLine(
            EI_PREMIUMS,
            EMPLOYMENT_INCOME,
            D("110000"),
            ContributionTier(Rate(D("0.0164")), D("0"), D("65700"), D("1077.48")),
            CENT,
            D("65700"),
            D("1077.48"),
        ),
    }
    assert surcharged == [
        SurchargeTierLine(
            output=ONTARIO_SURTAX,
            base=ONTARIO_TAX_AFTER_CREDITS,
            base_amount=D("7671.98"),
            threshold=D("5710"),
            rate=Rate(D("0.20")),
            rounding=CENT,
            part=D("392.40"),
        ),
        SurchargeTierLine(
            output=ONTARIO_SURTAX,
            base=ONTARIO_TAX_AFTER_CREDITS,
            base_amount=D("7671.98"),
            threshold=D("7307"),
            rate=Rate(D("0.36")),
            rounding=CENT,
            part=D("131.39"),
        ),
    ]
    assert premium_tiers == [
        SurchargeTierLine(
            output=ONTARIO_HEALTH_PREMIUM,
            base=TAXABLE_INCOME,
            base_amount=D("115000"),
            threshold=D("20000"),
            rate=Rate(D("0.06")),
            rounding=CENT,
            part=D("300"),
            maximum=D("300"),
        ),
        SurchargeTierLine(
            output=ONTARIO_HEALTH_PREMIUM,
            base=TAXABLE_INCOME,
            base_amount=D("115000"),
            threshold=D("36000"),
            rate=Rate(D("0.06")),
            rounding=CENT,
            part=D("150"),
            maximum=D("150"),
        ),
        SurchargeTierLine(
            output=ONTARIO_HEALTH_PREMIUM,
            base=TAXABLE_INCOME,
            base_amount=D("115000"),
            threshold=D("48000"),
            rate=Rate(D("0.25")),
            rounding=CENT,
            part=D("150"),
            maximum=D("150"),
        ),
        SurchargeTierLine(
            output=ONTARIO_HEALTH_PREMIUM,
            base=TAXABLE_INCOME,
            base_amount=D("115000"),
            threshold=D("72000"),
            rate=Rate(D("0.25")),
            rounding=CENT,
            part=D("150"),
            maximum=D("150"),
        ),
        SurchargeTierLine(
            output=ONTARIO_HEALTH_PREMIUM,
            base=TAXABLE_INCOME,
            base_amount=D("115000"),
            threshold=D("200000"),
            rate=Rate(D("0.25")),
            rounding=CENT,
            part=D("0"),
            maximum=D("150"),
        ),
    ]
    assert lift_tiers == [
        SurchargeTierLine(
            output=LIFT_REDUCTION,
            base=ontario.LIFT_ADJUSTED_NET_INCOME,
            base_amount=D("115000"),
            threshold=D("32500"),
            rate=Rate(D("0.05")),
            rounding=CENT,
            part=D("4125.00"),
        )
    ]
    assert set(cwb_basic_tiers) == {
        SurchargeTierLine(
            output=CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT,
            base=WORKING_INCOME,
            base_amount=D("110000"),
            threshold=D("3000"),
            rate=Rate(D("0.27")),
            rounding=CENT,
            part=D("1633"),
            maximum=D("1633"),
        ),
        SurchargeTierLine(
            output=CWB_BEFORE_REDUCTION_WITH_DEPENDANT,
            base=WORKING_INCOME,
            base_amount=D("110000"),
            threshold=D("3000"),
            rate=Rate(D("0.27")),
            rounding=CENT,
            part=D("2813"),
            maximum=D("2813"),
        ),
    }
    assert len(cwb_basic_tiers) == 2
    assert set(cwb_reduction_tiers) == {
        SurchargeTierLine(
            output=CWB_REDUCTION_WITHOUT_DEPENDANT,
            base=ADJUSTED_FAMILY_NET_INCOME,
            base_amount=D("115000"),
            threshold=D("26855"),
            rate=Rate(D("0.15")),
            rounding=CENT,
            part=D("13221.75"),
        ),
        SurchargeTierLine(
            output=CWB_REDUCTION_WITH_DEPENDANT,
            base=ADJUSTED_FAMILY_NET_INCOME,
            base_amount=D("115000"),
            threshold=D("30639"),
            rate=Rate(D("0.15")),
            rounding=CENT,
            part=D("12654.15"),
        ),
    }
    assert len(cwb_reduction_tiers) == 2
    assert floored == {
        # T1 line 110 "Line 107 minus line 109 (if negative, enter "0")": no medical expenses.
        MEDICAL_EXPENSES_OVER_THRESHOLD: SubtractedNotBelowZeroLine(
            output=MEDICAL_EXPENSES_OVER_THRESHOLD,
            minuend=MEDICAL_EXPENSES,
            minuend_amount=D("0"),
            subtrahend=MEDICAL_THRESHOLD,
            subtrahend_amount=D("2834"),
            result=D("0"),
        ),
        # ON428 line 41 "Line 36 minus line 40 (if negative, enter "0")".
        ontario.MEDICAL_EXPENSES_OVER_THRESHOLD: SubtractedNotBelowZeroLine(
            output=ontario.MEDICAL_EXPENSES_OVER_THRESHOLD,
            minuend=MEDICAL_EXPENSES,
            minuend_amount=D("0"),
            subtrahend=ontario.MEDICAL_THRESHOLD,
            subtrahend_amount=D("2885"),
            result=D("0"),
        ),
        # T1 line 139 (line 41700) "Line 134 minus line 138 (if negative, enter "0")", with line
        # 134 carrying line 132: no credit against a federal tax of 16951.38.
        FEDERAL_TAX_LESS_CREDITS: SubtractedNotBelowZeroLine(
            output=FEDERAL_TAX_LESS_CREDITS,
            minuend=FEDERAL_TAX_WITH_ITC_RECAPTURE,
            minuend_amount=D("16951.38"),
            subtrahend=CREDITS_AGAINST_FEDERAL_TAX,
            subtrahend_amount=D("0"),
            result=D("16951.38"),
        ),
        # ON479 line 10 "Line 8 minus line 9 (if negative, enter "0")" and line 13 "Line 5 minus
        # line 12 (if negative, enter "0")": Return A's family net income is its own 115000.00
        # (line 7 is 0), 80000.00 over the base, so line 12 is 4000.00 and line 13 is 0 - 4000.00,
        # negative, so 0.
        SENIORS_CARE_INCOME_OVER_BASE: SubtractedNotBelowZeroLine(
            output=SENIORS_CARE_INCOME_OVER_BASE,
            minuend=SENIORS_CARE_FAMILY_NET_INCOME,
            minuend_amount=D("115000.00"),
            subtrahend=SENIORS_CARE_BASE_AMOUNT,
            subtrahend_amount=D("35000.00"),
            result=D("80000.00"),
        ),
        SENIORS_CARE_BEFORE_CLAIM: SubtractedNotBelowZeroLine(
            output=SENIORS_CARE_BEFORE_CLAIM,
            minuend=SENIORS_CARE_AMOUNT,
            minuend_amount=D("0"),
            subtrahend=SENIORS_CARE_REDUCTION,
            subtrahend_amount=D("4000.00"),
            result=D("0"),
        ),
        # Worksheet ON479 "Line 20" line 6 "Line 4 minus line 5 (if negative, enter "0")" and line
        # 11 "Line 9 minus line 10 (if negative, enter "0")": Return A has no payroll entered (0),
        # so line 6 is 0, line 8 is 0 and line 11 is the whole 1.00.
        COOP_EDUCATION_PAYROLL_OVER_THRESHOLD: SubtractedNotBelowZeroLine(
            output=COOP_EDUCATION_PAYROLL_OVER_THRESHOLD,
            minuend=COOP_EDUCATION_PAYROLL,
            minuend_amount=D("0"),
            subtrahend=COOP_EDUCATION_PAYROLL_THRESHOLD,
            subtrahend_amount=D("400000.00"),
            result=D("0"),
        ),
        COOP_EDUCATION_REMAINING_SHARE: SubtractedNotBelowZeroLine(
            output=COOP_EDUCATION_REMAINING_SHARE,
            minuend=COOP_EDUCATION_FULL_SHARE,
            minuend_amount=D("1.00"),
            subtrahend=COOP_EDUCATION_PHASE_OUT_SHARE,
            subtrahend_amount=D("0"),
            result=D("1.00"),
        ),
        # Schedule 9 line 16 "Line 14 minus line 15 (if negative, enter "0")" and line 19 "Line 17
        # minus line 18 (if negative, enter "0")": the taxable income of 115000 is below the
        # threshold of 253414.00. Federal Worksheet line 5 "Line 3 minus line 4 (if negative,
        # enter "0")": 3194.87 is below 8319.38.
        DONATIONS_OVER_FIRST_TIER_AFTER_2016_GIFTS: SubtractedNotBelowZeroLine(
            output=DONATIONS_OVER_FIRST_TIER_AFTER_2016_GIFTS,
            minuend=DONATIONS_OVER_FIRST_TIER,
            minuend_amount=D("0"),
            subtrahend=ECOLOGICAL_GIFTS_BEFORE_2016,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        TAXABLE_INCOME_OVER_DONATION_THRESHOLD: SubtractedNotBelowZeroLine(
            output=TAXABLE_INCOME_OVER_DONATION_THRESHOLD,
            minuend=TAXABLE_INCOME,
            minuend_amount=D("115000"),
            subtrahend=DONATION_HIGH_INCOME_THRESHOLD,
            subtrahend_amount=D("253414.00"),
            result=D("0"),
        ),
        TOP_UP_EXCESS: SubtractedNotBelowZeroLine(
            output=TOP_UP_EXCESS,
            minuend=TOP_UP_CREDITS_BASE,
            minuend_amount=D("3194.87"),
            subtrahend=TOP_UP_THRESHOLD,
            subtrahend_amount=D("8319.38"),
            result=D("0"),
        ),
        # Worksheet ON479 column 1 line 3 "Line 1 minus line 2 (cannot be negative)": line 1 is 0.
        ontario.POLITICAL_CREDIT_COLUMN_1_LINE_3: SubtractedNotBelowZeroLine(
            output=ontario.POLITICAL_CREDIT_COLUMN_1_LINE_3,
            minuend=ontario.POLITICAL_CONTRIBUTIONS,
            minuend_amount=D("0"),
            subtrahend=ontario.POLITICAL_CREDIT_COLUMN_1_LINE_2,
            subtrahend_amount=D("0.00"),
            result=D("0"),
        ),
        # Worksheet ON479 column 2 line 3 "Line 1 minus line 2 (cannot be negative)": line 1 is 0.
        ontario.POLITICAL_CREDIT_COLUMN_2_LINE_3: SubtractedNotBelowZeroLine(
            output=ontario.POLITICAL_CREDIT_COLUMN_2_LINE_3,
            minuend=ontario.POLITICAL_CONTRIBUTIONS,
            minuend_amount=D("0"),
            subtrahend=ontario.POLITICAL_CREDIT_COLUMN_2_LINE_2,
            subtrahend_amount=D("500.05"),
            result=D("0"),
        ),
        # Worksheet ON479 column 3 line 3 "Line 1 minus line 2 (cannot be negative)": line 1 is 0.
        ontario.POLITICAL_CREDIT_COLUMN_3_LINE_3: SubtractedNotBelowZeroLine(
            output=ontario.POLITICAL_CREDIT_COLUMN_3_LINE_3,
            minuend=ontario.POLITICAL_CONTRIBUTIONS,
            minuend_amount=D("0"),
            subtrahend=ontario.POLITICAL_CREDIT_COLUMN_3_LINE_2,
            subtrahend_amount=D("1666.82"),
            result=D("0"),
        ),
        # Federal Worksheet column 1 line 3 "Line 1 minus line 2 (if negative, enter "0") =": line 1
        # is 0.
        POLITICAL_CREDIT_COLUMN_1_LINE_3: SubtractedNotBelowZeroLine(
            output=POLITICAL_CREDIT_COLUMN_1_LINE_3,
            minuend=POLITICAL_CONTRIBUTIONS,
            minuend_amount=D("0"),
            subtrahend=POLITICAL_CREDIT_COLUMN_1_LINE_2,
            subtrahend_amount=D("0.00"),
            result=D("0"),
        ),
        # Federal Worksheet column 2 line 3 "Line 1 minus line 2 (if negative, enter "0") =": line 1
        # is 0.
        POLITICAL_CREDIT_COLUMN_2_LINE_3: SubtractedNotBelowZeroLine(
            output=POLITICAL_CREDIT_COLUMN_2_LINE_3,
            minuend=POLITICAL_CONTRIBUTIONS,
            minuend_amount=D("0"),
            subtrahend=POLITICAL_CREDIT_COLUMN_2_LINE_2,
            subtrahend_amount=D("400.00"),
            result=D("0"),
        ),
        # Federal Worksheet column 3 line 3 "Line 1 minus line 2 (if negative, enter "0") =": line 1
        # is 0.
        POLITICAL_CREDIT_COLUMN_3_LINE_3: SubtractedNotBelowZeroLine(
            output=POLITICAL_CREDIT_COLUMN_3_LINE_3,
            minuend=POLITICAL_CONTRIBUTIONS,
            minuend_amount=D("0"),
            subtrahend=POLITICAL_CREDIT_COLUMN_3_LINE_2,
            subtrahend_amount=D("750.00"),
            result=D("0"),
        ),
        NET_INCOME: SubtractedNotBelowZeroLine(
            output=NET_INCOME,
            minuend=TOTAL_INCOME,
            minuend_amount=D("120000"),
            subtrahend=DEDUCTIONS_FROM_TOTAL_INCOME,
            subtrahend_amount=D("5000"),
            result=D("115000"),
        ),
        TAXABLE_INCOME: SubtractedNotBelowZeroLine(
            output=TAXABLE_INCOME,
            minuend=NET_INCOME,
            minuend_amount=D("115000"),
            subtrahend=DEDUCTIONS_FROM_NET_INCOME,
            subtrahend_amount=D("0"),
            result=D("115000"),
        ),
        # Each form's credits come off its basic tax, not below zero; here both taxes exceed
        # their credits.
        FEDERAL_TAX_AFTER_CREDITS: SubtractedNotBelowZeroLine(
            output=FEDERAL_TAX_AFTER_CREDITS,
            minuend=FEDERAL_BASIC_TAX,
            minuend_amount=D("20146.25"),
            subtrahend=CREDITS_AGAINST_BASIC_FEDERAL_TAX,
            subtrahend_amount=D("3194.87"),
            result=D("16951.38"),
        ),
        ONTARIO_TAX_AFTER_CREDITS: SubtractedNotBelowZeroLine(
            output=ONTARIO_TAX_AFTER_CREDITS,
            minuend=ONTARIO_BASIC_TAX,
            minuend_amount=D("8539.60"),
            subtrahend=ontario.NON_REFUNDABLE_TAX_CREDITS,
            subtrahend_amount=D("867.62"),
            result=D("7671.98"),
        ),
        # Schedule 5 line 5 "Line 3 minus line 4 (if negative, enter "0")": line 3 is line 1,
        # the basic personal amount, as line 2 is not triggered; line 4 the dependant's net
        # income, entered as 0.
        ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT: SubtractedNotBelowZeroLine(
            output=ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT,
            minuend=BASIC_PERSONAL_AMOUNT,
            minuend_amount=D("16129.00"),
            subtrahend=DEPENDANT_NET_INCOME,
            subtrahend_amount=D("0"),
            result=D("16129.00"),
        ),
        # Federal Worksheet line 4 "Line 2 minus line 3 (if negative, enter "0")": the net income
        # 115000 less the income threshold 45522.00.
        AGE_INCOME_OVER_THRESHOLD: SubtractedNotBelowZeroLine(
            output=AGE_INCOME_OVER_THRESHOLD,
            minuend=NET_INCOME,
            minuend_amount=D("115000"),
            subtrahend=AGE_INCOME_THRESHOLD,
            subtrahend_amount=D("45522.00"),
            result=D("69478.00"),
        ),
        # Federal Worksheet line 7 "Line 1 minus line 6 (if negative, enter "0")": 9028.00 less
        # 10421.70 is negative, so 0.
        AGE_AMOUNT_BEFORE_COUNT: SubtractedNotBelowZeroLine(
            output=AGE_AMOUNT_BEFORE_COUNT,
            minuend=AGE_MAXIMUM,
            minuend_amount=D("9028.00"),
            subtrahend=AGE_REDUCTION,
            subtrahend_amount=D("10421.70"),
            result=D("0"),
        ),
        # Schedule 5 line 5 of the line 30300 part "Line 3 minus line 4 (if negative, enter "0")",
        # with the spouse's net income entered as 0.
        SPOUSE_AMOUNT_BEFORE_COUNT: SubtractedNotBelowZeroLine(
            output=SPOUSE_AMOUNT_BEFORE_COUNT,
            minuend=SPOUSE_AMOUNT_BASIS,
            minuend_amount=D("16129.00"),
            subtrahend=SPOUSE_NET_INCOME,
            subtrahend_amount=D("0"),
            result=D("16129.00"),
        ),
        # Schedule 5 line 3 and line 5 of the line 30425 part, "Line 1 minus line 2" and "Line 3
        # minus line 4", each "(if negative, enter "0")".
        SPOUSE_CAREGIVER_BEFORE_MAXIMUM: SubtractedNotBelowZeroLine(
            output=SPOUSE_CAREGIVER_BEFORE_MAXIMUM,
            minuend=SPOUSE_CAREGIVER_BASE,
            minuend_amount=D("28798.00"),
            subtrahend=SPOUSE_NET_INCOME,
            subtrahend_amount=D("0"),
            result=D("28798.00"),
        ),
        SPOUSE_CAREGIVER_AMOUNT_BEFORE_COUNT: SubtractedNotBelowZeroLine(
            output=SPOUSE_CAREGIVER_AMOUNT_BEFORE_COUNT,
            minuend=SPOUSE_CAREGIVER_LIMIT,
            minuend_amount=D("8601"),
            subtrahend=SPOUSE_AMOUNT,
            subtrahend_amount=D("0"),
            result=D("8601"),
        ),
        # Worksheet ON428 line 4 "Line 2 minus line 3 (if negative, enter "0")": the net income
        # 115000 less the income threshold 46330.00.
        ontario.AGE_INCOME_OVER_THRESHOLD: SubtractedNotBelowZeroLine(
            output=ontario.AGE_INCOME_OVER_THRESHOLD,
            minuend=NET_INCOME,
            minuend_amount=D("115000"),
            subtrahend=ontario.AGE_INCOME_THRESHOLD,
            subtrahend_amount=D("46330.00"),
            result=D("68670.00"),
        ),
        # Worksheet ON428 line 7 "Line 1 minus line 6 (if negative, enter "0")": 6223.00 less
        # 10300.50 is negative, so 0.
        ontario.AGE_AMOUNT_BEFORE_COUNT: SubtractedNotBelowZeroLine(
            output=ontario.AGE_AMOUNT_BEFORE_COUNT,
            minuend=ontario.AGE_MAXIMUM,
            minuend_amount=D("6223.00"),
            subtrahend=ontario.AGE_REDUCTION,
            subtrahend_amount=D("10300.50"),
            result=D("0"),
        ),
        # ON428 line 13 "Line 11 minus line 12 (if negative, enter "0")", before its maximum,
        # with the spouse's net income entered as 0.
        ontario.SPOUSE_AMOUNT_BEFORE_MAXIMUM: SubtractedNotBelowZeroLine(
            output=ontario.SPOUSE_AMOUNT_BEFORE_MAXIMUM,
            minuend=ontario.SPOUSE_BASE,
            minuend_amount=D("11905.00"),
            subtrahend=SPOUSE_NET_INCOME,
            subtrahend_amount=D("0"),
            result=D("11905.00"),
        ),
        # ON428 line 16 "Line 14 minus line 15 (if negative, enter "0")", before its maximum.
        ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_MAXIMUM: SubtractedNotBelowZeroLine(
            output=ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_MAXIMUM,
            minuend=ELIGIBLE_DEPENDANT_BASE,
            minuend_amount=D("11905.00"),
            subtrahend=DEPENDANT_NET_INCOME,
            subtrahend_amount=D("0"),
            result=D("11905.00"),
        ),
        # ON428 line 58 "Line 56 minus line 57 (if negative, enter "0")" and line 71 "Line 69
        # minus line 70 (if negative, enter "0")": the credit is 0.
        ontario.ONTARIO_TAX_LESS_DIVIDEND_CREDIT: SubtractedNotBelowZeroLine(
            output=ontario.ONTARIO_TAX_LESS_DIVIDEND_CREDIT,
            minuend=ontario.ONTARIO_TAX_BEFORE_DIVIDEND_CREDIT,
            minuend_amount=D("7671.98"),
            subtrahend=ontario.DIVIDEND_TAX_CREDIT,
            subtrahend_amount=D("0"),
            result=D("7671.98"),
        ),
        ontario.ONTARIO_TAX_AFTER_DIVIDEND_CREDIT: SubtractedNotBelowZeroLine(
            output=ontario.ONTARIO_TAX_AFTER_DIVIDEND_CREDIT,
            minuend=ONTARIO_TAX_WITH_SURTAX,
            minuend_amount=D("8195.77"),
            subtrahend=ontario.DIVIDEND_CREDIT_FROM_LINE_57,
            subtrahend_amount=D("0"),
            result=D("8195.77"),
        ),
        # ON428 line 81 "Line 73 minus line 80 (if negative, enter "0")".
        ONTARIO_TAX_AFTER_REDUCTION: SubtractedNotBelowZeroLine(
            output=ONTARIO_TAX_AFTER_REDUCTION,
            minuend=ontario.ONTARIO_TAX_AFTER_DIVIDEND_CREDIT,
            minuend_amount=D("8195.77"),
            subtrahend=ONTARIO_TAX_REDUCTION,
            subtrahend_amount=D("0"),
            result=D("8195.77"),
        ),
        # Schedule ON428-A line 20 "Line 14 minus line 19 (if negative, enter "0")": the
        # reduction of 4125.00 exceeds the 875, so the credit for a single individual is 0.
        ontario.LIFT_CREDIT_SINGLE: SubtractedNotBelowZeroLine(
            output=ontario.LIFT_CREDIT_SINGLE,
            minuend=LIFT_MAXIMUM_CREDIT,
            minuend_amount=D("875"),
            subtrahend=LIFT_REDUCTION,
            subtrahend_amount=D("4125.00"),
            result=D("0"),
        ),
        # Schedule ON428-A line 13 "Line 9 minus line 12 (if negative, enter "0")" and line 28
        # "Line 24 minus line 27 (if negative, enter "0")", then lines 32 "Line 30 minus line 31"
        # and 37 "Line 35 minus line 36", each "(if negative, enter "0")", and line 41 "Line 29
        # minus line 40 (if negative, enter "0")": the family reduction of 4125.00 exceeds the 875.
        ontario.LIFT_ADJUSTED_NET_INCOME: SubtractedNotBelowZeroLine(
            output=ontario.LIFT_ADJUSTED_NET_INCOME,
            minuend=ontario.LIFT_NET_INCOME_AND_REPAYMENTS,
            minuend_amount=D("115000"),
            subtrahend=ontario.LIFT_UCCB_AND_RDSP_INCOME,
            subtrahend_amount=D("0"),
            result=D("115000"),
        ),
        ontario.LIFT_SPOUSE_ADJUSTED_NET_INCOME: SubtractedNotBelowZeroLine(
            output=ontario.LIFT_SPOUSE_ADJUSTED_NET_INCOME,
            minuend=ontario.LIFT_SPOUSE_NET_INCOME_AND_REPAYMENTS,
            minuend_amount=D("0"),
            subtrahend=ontario.LIFT_SPOUSE_UCCB_AND_RDSP_INCOME,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        ontario.LIFT_EXCESS_OVER_INDIVIDUAL_THRESHOLD: SubtractedNotBelowZeroLine(
            output=ontario.LIFT_EXCESS_OVER_INDIVIDUAL_THRESHOLD,
            minuend=ontario.LIFT_ADJUSTED_NET_INCOME,
            minuend_amount=D("115000"),
            subtrahend=ontario.LIFT_INDIVIDUAL_INCOME_THRESHOLD,
            subtrahend_amount=D("32500.00"),
            result=D("82500.00"),
        ),
        ontario.LIFT_EXCESS_OVER_FAMILY_THRESHOLD: SubtractedNotBelowZeroLine(
            output=ontario.LIFT_EXCESS_OVER_FAMILY_THRESHOLD,
            minuend=ontario.LIFT_FAMILY_NET_INCOME,
            minuend_amount=D("115000"),
            subtrahend=ontario.LIFT_FAMILY_INCOME_THRESHOLD,
            subtrahend_amount=D("65000.00"),
            result=D("50000.00"),
        ),
        ontario.LIFT_CREDIT_WITH_SPOUSE: SubtractedNotBelowZeroLine(
            output=ontario.LIFT_CREDIT_WITH_SPOUSE,
            minuend=LIFT_MAXIMUM_CREDIT,
            minuend_amount=D("875"),
            subtrahend=ontario.LIFT_FAMILY_REDUCTION,
            subtrahend_amount=D("4125.00"),
            result=D("0"),
        ),
        # T1 line 48400 "Refund": the total credits of 25000 less the total payable of 25897.15 is
        # not above zero, so the refund is 0 (the balance owing of 897.15 is line 48500).
        REFUND: SubtractedNotBelowZeroLine(
            output=REFUND,
            minuend=TOTAL_CREDITS,
            minuend_amount=D("25000"),
            subtrahend=TOTAL_PAYABLE,
            subtrahend_amount=D("25897.15"),
            result=D("0"),
        ),
        # ON428 line 86 "Line 84 minus line 85 (if negative, enter "0")".
        ONTARIO_TAX_AFTER_LIFT_CREDIT: SubtractedNotBelowZeroLine(
            output=ONTARIO_TAX_AFTER_LIFT_CREDIT,
            minuend=ONTARIO_TAX_AFTER_REDUCTION,
            minuend_amount=D("8195.77"),
            subtrahend=LIFT_CREDIT,
            subtrahend_amount=D("0"),
            result=D("8195.77"),
        ),
        # ON428 line 88 "Line 86 minus line 87 (if negative, enter "0")": line 87 is 0.
        ONTARIO_TAX_AFTER_FOOD_CREDIT: SubtractedNotBelowZeroLine(
            output=ONTARIO_TAX_AFTER_FOOD_CREDIT,
            minuend=ONTARIO_TAX_AFTER_LIFT_CREDIT,
            minuend_amount=D("8195.77"),
            subtrahend=COMMUNITY_FOOD_PROGRAM_CREDIT,
            subtrahend_amount=D("0.00"),
            result=D("8195.77"),
        ),
        # Schedule 6 line 28 "Line 22 minus line 27 (if negative, enter "0")": the reduction of
        # 13221.75 exceeds the 1633, and that of 12654.15 the 2813, so the benefit is 0 with or
        # without an eligible dependant.
        CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT: SubtractedNotBelowZeroLine(
            output=CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT,
            minuend=CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT,
            minuend_amount=D("1633"),
            subtrahend=CWB_REDUCTION_WITHOUT_DEPENDANT,
            subtrahend_amount=D("13221.75"),
            result=D("0"),
        ),
        CANADA_WORKERS_BENEFIT_WITH_DEPENDANT: SubtractedNotBelowZeroLine(
            output=CANADA_WORKERS_BENEFIT_WITH_DEPENDANT,
            minuend=CWB_BEFORE_REDUCTION_WITH_DEPENDANT,
            minuend_amount=D("2813"),
            subtrahend=CWB_REDUCTION_WITH_DEPENDANT,
            subtrahend_amount=D("12654.15"),
            result=D("0"),
        ),
        # Schedule 15 line 12.
        FHSA_EXCESS_DESIGNATED_WITHDRAWALS: SubtractedNotBelowZeroLine(
            output=FHSA_EXCESS_DESIGNATED_WITHDRAWALS,
            minuend=FHSA_DESIGNATED_WITHDRAWALS_IN_2025,
            minuend_amount=D("0"),
            subtrahend=FHSA_CONTRIBUTIONS_AFTER_FIRST_QUALIFYING_WITHDRAWAL,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Schedule 15 line 13.
        FHSA_CONTRIBUTIONS_LIMIT: SubtractedNotBelowZeroLine(
            output=FHSA_CONTRIBUTIONS_LIMIT,
            minuend=FHSA_CONTRIBUTIONS_PLUS_VARIABLE_B_AMOUNT,
            minuend_amount=D("0"),
            subtrahend=FHSA_EXCESS_DESIGNATED_WITHDRAWALS,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Schedule 15 line 29.
        FHSA_NET_TRANSFER_AMOUNT_LESS_VARIABLE_H_AMOUNT: SubtractedNotBelowZeroLine(
            output=FHSA_NET_TRANSFER_AMOUNT_LESS_VARIABLE_H_AMOUNT,
            minuend=FHSA_NET_RRSP_TRANSFER_AMOUNT_FOR_2024_AND_PRIOR_YEARS,
            minuend_amount=D("0"),
            subtrahend=FHSA_VARIABLE_H_AMOUNT,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Schedule 15 line 39.
        FHSA_ANNUAL_AMOUNT_AFTER_TRANSFERS: SubtractedNotBelowZeroLine(
            output=FHSA_ANNUAL_AMOUNT_AFTER_TRANSFERS,
            minuend=FHSA_ANNUAL_AMOUNT_WITH_CARRYFORWARD,
            minuend_amount=D("8000.00"),
            subtrahend=FHSA_NET_TRANSFER_AMOUNT_AFTER_PRIOR_YEARS,
            subtrahend_amount=D("0"),
            result=D("8000.00"),
        ),
        # Schedule 15 line 50.
        FHSA_LIFETIME_LIMIT_LESS_DEDUCTIONS_AND_TRANSFERS: SubtractedNotBelowZeroLine(
            output=FHSA_LIFETIME_LIMIT_LESS_DEDUCTIONS_AND_TRANSFERS,
            minuend=FHSA_LIFETIME_LIMIT_LESS_DEDUCTIONS,
            minuend_amount=D("40000.00"),
            subtrahend=FHSA_NET_RRSP_TRANSFER_AMOUNT,
            subtrahend_amount=D("0"),
            result=D("40000.00"),
        ),
        # Federal Worksheet "Line 45200 - Refundable medical expense supplement" (T1 line 154),
        # Return A: line 21500 and line 33200 are 0, so line 11 and line 13 are 0.
        MEDICAL_SUPPLEMENT_COLUMN_2_LINE_5: SubtractedNotBelowZeroLine(
            output=MEDICAL_SUPPLEMENT_COLUMN_2_LINE_5,
            minuend=MEDICAL_SUPPLEMENT_COLUMN_2_LINE_3,
            minuend_amount=D("0"),
            subtrahend=MEDICAL_SUPPLEMENT_COLUMN_2_LINE_4,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        MEDICAL_SUPPLEMENT_EMPLOYMENT_WORKING_INCOME: SubtractedNotBelowZeroLine(
            output=MEDICAL_SUPPLEMENT_EMPLOYMENT_WORKING_INCOME,
            minuend=MEDICAL_SUPPLEMENT_EMPLOYMENT_INCOME_LESS_WAGE_LOSS,
            minuend_amount=D("110000"),
            subtrahend=MEDICAL_SUPPLEMENT_EMPLOYMENT_DEDUCTIONS,
            subtrahend_amount=D("2000"),
            result=D("108000"),
        ),
        MEDICAL_SUPPLEMENT_COLUMN_1_LINE_5: SubtractedNotBelowZeroLine(
            output=MEDICAL_SUPPLEMENT_COLUMN_1_LINE_5,
            minuend=MEDICAL_SUPPLEMENT_COLUMN_1_LINE_3,
            minuend_amount=D("115000.00"),
            subtrahend=UCCB_AND_RDSP_INCOME,
            subtrahend_amount=D("0"),
            result=D("115000.00"),
        ),
        MEDICAL_SUPPLEMENT_LINE_8: SubtractedNotBelowZeroLine(
            output=MEDICAL_SUPPLEMENT_LINE_8,
            minuend=MEDICAL_SUPPLEMENT_LINE_6,
            minuend_amount=D("115000.00"),
            subtrahend=MEDICAL_SUPPLEMENT_INCOME_THRESHOLD,
            subtrahend_amount=D("33294.00"),
            result=D("81706.00"),
        ),
        MEDICAL_SUPPLEMENT_LINE_16: SubtractedNotBelowZeroLine(
            output=MEDICAL_SUPPLEMENT_LINE_16,
            minuend=MEDICAL_SUPPLEMENT_LINE_14,
            minuend_amount=D("0.00"),
            subtrahend=MEDICAL_SUPPLEMENT_LINE_15,
            subtrahend_amount=D("4085.30"),
            result=D("0"),
        ),
    }
    assert record_totals == {
        FLOW_THROUGH_SHARE_EXPENSES: RecordTotalLine(
            FLOW_THROUGH_SHARE_EXPENSES, FLOW_THROUGH_SHARE_SLIP_EXPENSES, (), D("0")
        ),
    }
    assert quotients == {
        COOP_EDUCATION_PHASE_OUT_SHARE: QuotientLine(
            output=COOP_EDUCATION_PHASE_OUT_SHARE,
            dividend=COOP_EDUCATION_PAYROLL_OVER_THRESHOLD,
            dividend_amount=D("0"),
            divisor=COOP_EDUCATION_PAYROLL_RANGE,
            divisor_amount=D("200000.00"),
            result=D("0"),
        ),
    }
    assert record_counts == {
        COOP_EDUCATION_PLACEMENT_COUNT: RecordCountLine(
            COOP_EDUCATION_PLACEMENT_COUNT, COOP_EDUCATION_PLACEMENTS, 0
        ),
    }
    assert placement_credits == []
    assert items_totals == {
        COOP_EDUCATION_CREDIT: ItemsTotalLine(COOP_EDUCATION_CREDIT, (), D("0"))
    }
    assert {line.output: line for line in trace if isinstance(line, GreaterOfLine)} == {
        ontario.LIFT_GREATER_EXCESS: GreaterOfLine(
            ontario.LIFT_GREATER_EXCESS,
            (
                (ontario.LIFT_EXCESS_OVER_INDIVIDUAL_THRESHOLD, D("82500.00")),
                (ontario.LIFT_EXCESS_OVER_FAMILY_THRESHOLD, D("50000.00")),
            ),
            D("82500.00"),
        )
    }
    assert chosen == {
        # Form T1172: a count of 0 (Part A does not apply) chooses Part B's line 13.
        RESP_AIPS_ADDITIONAL_TAX: ChosenByCountLine(
            output=RESP_AIPS_ADDITIONAL_TAX,
            count_kind=RESP_AIPS_PART_A_APPLIES,
            count=0,
            chosen_kind=RESP_AIPS_PART_B_TAX,
            chosen_value=D("0"),
        ),
        # Line 25000: line 9 is not over $93,454 and no amount was entered on line 14600, so
        # line 14700 (0 here) twice.
        OTHER_PAYMENTS_DEDUCTION_AFTER_LIMIT: ChosenByCountLine(
            output=OTHER_PAYMENTS_DEDUCTION_AFTER_LIMIT,
            count_kind=OTHER_PAYMENTS_WORKSHEET_LINE_9_OVER_LIMIT,
            count=0,
            chosen_kind=INCOME_SUPPORT_BENEFITS,
            chosen_value=D("0"),
        ),
        OTHER_PAYMENTS_DEDUCTION: ChosenByCountLine(
            output=OTHER_PAYMENTS_DEDUCTION,
            count_kind=OTHER_PAYMENTS_WORKSHEET_REQUIRED,
            count=0,
            chosen_kind=INCOME_SUPPORT_BENEFITS,
            chosen_value=D("0"),
        ),
        # ON428 line 85, from Schedule ON428-A: Part A (line 20) with no spouse or common-law
        # partner at the end of the year.
        LIFT_CREDIT: ChosenByCountLine(
            output=LIFT_CREDIT,
            count_kind=ontario.LIFT_SPOUSE_AT_YEAR_END,
            count=0,
            chosen_kind=ontario.LIFT_CREDIT_SINGLE,
            chosen_value=D("0"),
        ),
        CANADA_WORKERS_BENEFIT: ChosenByCountLine(
            output=CANADA_WORKERS_BENEFIT,
            count_kind=CWB_ELIGIBLE_DEPENDANTS,
            count=0,
            chosen_kind=CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT,
            chosen_value=D("0"),
        ),
        # Schedule 15 line 40.
        FHSA_ANNUAL_LIMIT: ChosenByCountLine(
            output=FHSA_ANNUAL_LIMIT,
            count_kind=FHSA_MAXIMUM_PARTICIPATION_PERIOD_ENDED,
            count=0,
            chosen_kind=FHSA_ANNUAL_LIMIT_FROM_STEP_2,
            chosen_value=D("0"),
        ),
    }
