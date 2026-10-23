"""CA-ON 2025 end to end, Return A: return a structured trace 1."""

from __future__ import annotations

from app.domain.parameters.rate import Rate
from app.domain.trace import (
    AtMostLine,
    CappedAmountLine,
    ChosenByCountLine,
    ChosenByRangeLine,
    ContributionTierLine,
    CreditAmountLine,
    FractionAppliedLine,
    ItemsTotalLine,
    LesserOfLine,
    MultipleOverLine,
    PercentageAppliedLine,
    PerUnitAmountLine,
    QuotientLine,
    RateAppliedLine,
    RecordCountLine,
    RecordTotalLine,
    RoundedTotalLine,
    SubtractedLine,
    SubtractedNotBelowZeroLine,
    SumLine,
    SurchargeTierLine,
    TaperedAmountLine,
    ThresholdGateLine,
    TimesCountLine,
)
from app.jurisdictions.ca.catalog import (
    AGE_INCOME_OVER_THRESHOLD,
    AGE_REDUCTION,
    ALLOWABLE_BUSINESS_INVESTMENT_LOSS,
    AMT_ADJUSTMENTS_BEFORE_RATE_TOTAL,
    AMT_AMOUNT_A_MINUS_AMOUNT_B,
    AMT_APPLICABLE_RATE_AMOUNT,
    AMT_BASIC_FEDERAL_TAX,
    AMT_DIVIDENDS_DIFFERENCE_ADJUSTMENT,
    AMT_DIVIDENDS_OTHER_THAN_ELIGIBLE_ADJUSTMENT,
    AMT_DONATIONS_AND_GIFTS_ADJUSTMENT,
    AMT_FEDERAL_SURTAX_AT_48_PERCENT,
    AMT_FEDERAL_SURTAX_MULTIPLE_JURISDICTIONS,
    AMT_FEDERAL_TAX_UNDER_MINIMUM_TAX,
    AMT_FOREIGN_INCOME_LIMIT,
    AMT_FOREIGN_NON_BUSINESS_TAX_PAID,
    AMT_FOREIGN_NON_BUSINESS_TAX_TWO_THIRDS,
    AMT_GROSS_MINIMUM_AMOUNT,
    AMT_LIFETIME_EXEMPTION_ADJUSTMENT,
    AMT_NET_ADJUSTED_TAXABLE_INCOME,
    AMT_NON_REFUNDABLE_CREDITS_ADJUSTMENT,
    AMT_PART_6_SURTAX_AT_48_PERCENT,
    AMT_PART_6_SURTAX_MULTIPLE_JURISDICTIONS,
    AMT_PUBLICLY_LISTED_GIFTS_ADJUSTMENT,
    AMT_PUBLICLY_LISTED_GIFTS_NET,
    AMT_SECURITY_OPTION_GIFTS_DEDUCTION,
    AMT_SECURITY_OPTION_PUBLICLY_LISTED_GIFTS,
    AMT_T2203_COLUMN_5_PERCENTAGE,
    AMT_TOTAL_FOREIGN_INCOME,
    BUSINESS_INVESTMENT_LOSS_AFTER_REDUCTION,
    BUSINESS_VEHICLE_LEASE_PRICE_85_PERCENT,
    BUSINESS_VEHICLE_LEASE_PRICE_BASE,
    CANADA_TRAINING_CREDIT_BASIS,
    CANADIAN_TUITION_FEES,
    CAPITAL_GAIN,
    CAPITAL_GAINS_DEDUCTION,
    CAPITAL_GIFTS_LIMIT_ADDITION,
    CAPITAL_GIFTS_TOTAL,
    CPP_ACTUAL_BASE_CONTRIBUTIONS,
    CPP_PART_5_LINE_43,
    CPP_PART_5_LINE_44,
    CPP_PART_5_LINE_45,
    CPP_PART_5_LINE_50,
    CPP_PART_5_LINE_50_LINE_49_POSITIVE,
    CPP_PART_5_LINE_70,
    CPP_PART_5_LINE_71,
    CPP_PART_5_LINE_75,
    CPP_PART_5_LINE_75_BASE,
    CPP_PART_5_LINE_84,
    CPP_T4_BASE_AND_FIRST_ADDITIONAL_CONTRIBUTIONS,
    CREDIT_AMOUNTS_AT_CREDIT_RATE,
    CWB_BEFORE_REDUCTION_WITH_DEPENDANT,
    CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT,
    CWB_REDUCTION_WITH_DEPENDANT,
    CWB_REDUCTION_WITHOUT_DEPENDANT,
    DIVIDENDS_AMOUNT_A_LESS_B,
    DIVIDENDS_AMOUNT_B,
    DONATION_LIMIT_ON_NET_INCOME,
    DONATIONS_AND_GIFTS_CREDIT,
    DONATIONS_FIRST_TIER,
    DONATIONS_OVER_FIRST_TIER,
    EDUCATOR_SCHOOL_SUPPLY_CREDIT,
    EDUCATOR_SUPPLIES_EXPENSES_AT_MOST_MAXIMUM,
    ELIGIBLE_DIVIDENDS_CREDIT,
    EMPLOYMENT_INCOME,
    EXPLORATION_AND_DEVELOPMENT_EXPENSES,
    FARM_VEHICLE_LEASE_PRICE_85_PERCENT,
    FARM_VEHICLE_LEASE_PRICE_BASE,
    FEDERAL_TAX_ON_SPLIT_INCOME,
    FIRST_TIER_DONATION_CREDIT,
    FISH_VEHICLE_LEASE_PRICE_85_PERCENT,
    FISH_VEHICLE_LEASE_PRICE_BASE,
    HIGH_INCOME_DONATION_CREDIT,
    HIGH_INCOME_DONATIONS,
    INCLUDED_CAPITAL_GAIN,
    ITC_RECAPTURE_AT_15_PERCENT,
    ITC_RECAPTURE_AT_20_PERCENT,
    ITC_RECAPTURE_EXPENDITURE_AT_15_PERCENT,
    ITC_RECAPTURE_EXPENDITURE_AT_20_PERCENT,
    LABOUR_SPONSORED_FUNDS_CREDIT_BEFORE_MAXIMUM,
    LABOUR_SPONSORED_FUNDS_NET_COST,
    MEDICAL_NET_INCOME_SHARE,
    MEDICAL_SUPPLEMENT_LINE_8,
    MEDICAL_SUPPLEMENT_LINE_11,
    MEDICAL_SUPPLEMENT_LINE_13,
    MEDICAL_SUPPLEMENT_LINE_15,
    NET_INCOME,
    NON_REFUNDABLE_CREDIT_AMOUNTS,
    OTHER_DIVIDENDS_CREDIT,
    OTHER_INCOME,
    POLITICAL_CREDIT_COLUMN_1_LINE_3,
    POLITICAL_CREDIT_COLUMN_1_LINE_5,
    POLITICAL_CREDIT_COLUMN_2_LINE_3,
    POLITICAL_CREDIT_COLUMN_2_LINE_5,
    POLITICAL_CREDIT_COLUMN_3_LINE_3,
    POLITICAL_CREDIT_COLUMN_3_LINE_5,
    QBT_AMOUNT_ALLOCATED,
    QBT_EXPLORATION_EXPENSES_AT_HALF,
    QBT_RECOVERY_OF_EXPLORATION_EXPENSES,
    QBT_TAXABLE_AMOUNT_ALLOCATED,
    QBT_TAXABLE_CAPITAL_GAINS,
    QBT_TOTAL_CAPITAL_GAINS,
    RC381_PART_3_LINE_20,
    REGULAR_RATE_DONATION_CREDIT,
    REGULAR_RATE_DONATIONS,
    RESIDENCY_NET_INCOME_LIMIT,
    RESP_AIPS_PART_A_TAX,
    RESP_AIPS_PART_B_TAX,
    RESP_AIPS_RECEIVED_PART_B,
    RESP_AIPS_SUBJECT_TO_TAX,
    SELF_EMPLOYED_CPP_BASE_CONTRIBUTIONS,
    SELF_EMPLOYED_CPP_BASE_CREDIT,
    SOCIAL_BENEFITS_LINE_17,
    SOCIAL_BENEFITS_LINE_18,
    SPLIT_INCOME_DIVIDENDS_OTHER_THAN_ELIGIBLE,
    SPLIT_INCOME_LINE_13,
    SPLIT_INCOME_LINE_14,
    SPLIT_INCOME_LINE_18,
    SPLIT_INCOME_LINE_19,
    SPLIT_INCOME_LINE_20,
    TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
    TOP_UP_EXCESS,
    TOP_UP_TAX_CREDIT,
    TOTAL_SPLIT_INCOME,
    TRAVEL_TOTAL_ZONE_B,
    TRAVEL_ZONE_B_DEDUCTION,
)
from app.jurisdictions.ca_on import catalog as ontario
from app.jurisdictions.ca_on.catalog import (
    COMMUNITY_FOOD_PROGRAM_CREDIT,
    COMMUNITY_FOOD_PROGRAM_DONATIONS,
    COOP_EDUCATION_CREDIT,
    FERTILITY_CREDIT_BEFORE_MAXIMUM,
    FERTILITY_EXPENSES,
    FLOW_THROUGH_SHARE_CREDIT,
    FLOW_THROUGH_SHARE_EXPENSES,
    LIFT_CREDIT_BEFORE_MAXIMUM,
    LIFT_REDUCTION,
    ONTARIO_HEALTH_PREMIUM,
    ONTARIO_SURTAX,
    SENIORS_CARE_BEFORE_MAXIMUM,
    SENIORS_CARE_INCOME_OVER_BASE,
    SENIORS_CARE_REDUCTION,
    SENIORS_TRANSIT_AMOUNT_PAID_AT_MOST_MAXIMUM,
    SENIORS_TRANSIT_CREDIT,
)
from app.jurisdictions.ca_on.trace import PlacementCreditLine
from tests.jurisdictions.ca_on.end_to_end.support import CENT, D, return_a


def test_the_trace_records_each_total_as_a_structured_line() -> None:
    trace = return_a().trace
    rated = {line.output: line for line in trace if isinstance(line, RateAppliedLine)}
    {line.output: line for line in trace if isinstance(line, SumLine)}
    {line.output: line for line in trace if isinstance(line, SubtractedNotBelowZeroLine)}
    {line.output: line for line in trace if isinstance(line, SubtractedLine)}
    {line.output: line for line in trace if isinstance(line, RoundedTotalLine)}
    {line.output: line for line in trace if isinstance(line, CreditAmountLine)}
    {line.output: line for line in trace if isinstance(line, TaperedAmountLine)}
    {line.output: line for line in trace if isinstance(line, CappedAmountLine)}
    {line.output: line for line in trace if isinstance(line, ContributionTierLine)}
    {line.output: line for line in trace if isinstance(line, LesserOfLine)}
    {line.output: line for line in trace if isinstance(line, AtMostLine)}
    [
        line
        for line in trace
        if isinstance(line, SurchargeTierLine) and line.output == ONTARIO_SURTAX
    ]
    [
        line
        for line in trace
        if isinstance(line, SurchargeTierLine) and line.output == LIFT_REDUCTION
    ]
    [
        line
        for line in trace
        if isinstance(line, SurchargeTierLine) and line.output == ONTARIO_HEALTH_PREMIUM
    ]
    [
        line
        for line in trace
        if isinstance(line, SurchargeTierLine)
        and line.output
        in (CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT, CWB_BEFORE_REDUCTION_WITH_DEPENDANT)
    ]
    [
        line
        for line in trace
        if isinstance(line, SurchargeTierLine)
        and line.output in (CWB_REDUCTION_WITHOUT_DEPENDANT, CWB_REDUCTION_WITH_DEPENDANT)
    ]
    {line.output: line for line in trace if isinstance(line, PerUnitAmountLine)}
    {line.output: line for line in trace if isinstance(line, MultipleOverLine)}
    {line.output: line for line in trace if isinstance(line, TimesCountLine)}
    {line.output: line for line in trace if isinstance(line, ThresholdGateLine)}
    {line.output: line for line in trace if isinstance(line, FractionAppliedLine)}
    {line.output: line for line in trace if isinstance(line, ChosenByCountLine)}
    {line.output: line for line in trace if isinstance(line, RecordTotalLine)}
    {line.output: line for line in trace if isinstance(line, ChosenByRangeLine)}
    {line.output: line for line in trace if isinstance(line, QuotientLine)}
    {line.output: line for line in trace if isinstance(line, RecordCountLine)}
    [line for line in trace if isinstance(line, PlacementCreditLine)]
    {
        line.output: line
        for line in trace
        if isinstance(line, ItemsTotalLine) and line.output is COOP_EDUCATION_CREDIT
    }
    percentages = {
        line.output: line
        for line in trace
        if isinstance(line, PercentageAppliedLine)
        and line.output is AMT_FEDERAL_SURTAX_MULTIPLE_JURISDICTIONS
    }
    part_6_percentages = {
        line.output: line
        for line in trace
        if isinstance(line, PercentageAppliedLine)
        and line.output is AMT_PART_6_SURTAX_MULTIPLE_JURISDICTIONS
    }
    assert part_6_percentages == {
        # Form T691 Part 6 line 10 "If you have to pay tax to multiple jurisdictions, multiply the
        # amount from line 9 by the percentage in Column 5 of line 52220 on Form T2203.": line 9,
        # 8136.66, at the percentage "0" a caller gives for Return A, 8136.66 x 0 / 100, 0.00.
        AMT_PART_6_SURTAX_MULTIPLE_JURISDICTIONS: PercentageAppliedLine(
            output=AMT_PART_6_SURTAX_MULTIPLE_JURISDICTIONS,
            amount_kind=AMT_PART_6_SURTAX_AT_48_PERCENT,
            amount_value=D("8136.66"),
            percentage_kind=AMT_T2203_COLUMN_5_PERCENTAGE,
            percentage_value=D("0"),
            rounding=CENT,
            result=D("0"),
        ),
    }
    assert percentages == {
        # Form T691 Part 3 line 3 "If you have to pay tax to multiple jurisdictions, multiply the
        # amount from line 2 by the percentage in Column 5 of line 52220 on Form T2203.": line 2,
        # 8136.66, at the percentage "0" a caller gives for Return A (no multiple jurisdictions),
        # 8136.66 x 0 / 100, 0.00.
        AMT_FEDERAL_SURTAX_MULTIPLE_JURISDICTIONS: PercentageAppliedLine(
            output=AMT_FEDERAL_SURTAX_MULTIPLE_JURISDICTIONS,
            amount_kind=AMT_FEDERAL_SURTAX_AT_48_PERCENT,
            amount_value=D("8136.66"),
            percentage_kind=AMT_T2203_COLUMN_5_PERCENTAGE,
            percentage_value=D("0"),
            rounding=CENT,
            result=D("0"),
        ),
    }
    assert rated == {
        # Form RC381 Part 3 line 20 "amount from line 19 x 83.1933%": line 19 is the T4 box 16 total
        # of 4034.10 that Return A enters, 4034.10 x 0.831933 = 3356.1000..., 3356.10.
        RC381_PART_3_LINE_20: RateAppliedLine(
            RC381_PART_3_LINE_20,
            CPP_T4_BASE_AND_FIRST_ADDITIONAL_CONTRIBUTIONS,
            D("4034.10"),
            Rate(D("0.831933")),
            CENT,
            D("3356.10"),
        ),
        # Form T691 Part 4 line 6 "Foreign income limit for special foreign tax credit: line 4
        # multiplied by the percentage on line 5 (if negative, enter "0")", with line 5 "Applicable
        # rate" "× 20.5%": line 4, 0.00 for Return A, at 20.5%, 0 times 0.205, 0.00.
        AMT_FOREIGN_INCOME_LIMIT: RateAppliedLine(
            output=AMT_FOREIGN_INCOME_LIMIT,
            base=AMT_TOTAL_FOREIGN_INCOME,
            base_amount=D("0"),
            rate=Rate(D("0.205")),
            rounding=CENT,
            result=D("0"),
        ),
        # Form T691 Part 4 line 7 "Total non-business income tax paid to a foreign country (12)"
        # "× 66.6666%": the caller's tax paid, 0 for Return A, at 66.6666%, 0 times 0.666666, 0.00.
        AMT_FOREIGN_NON_BUSINESS_TAX_TWO_THIRDS: RateAppliedLine(
            output=AMT_FOREIGN_NON_BUSINESS_TAX_TWO_THIRDS,
            base=AMT_FOREIGN_NON_BUSINESS_TAX_PAID,
            base_amount=D("0"),
            rate=Rate(D("0.666666")),
            rounding=CENT,
            result=D("0"),
        ),
        # Form T691 Part 3 line 2 "Federal surtax on business income earned outside Canada"
        # "Multiply the amount from line 1 by 48%.": line 1, the basic federal tax of 16951.38, at
        # 48%, 16951.38 x 0.48 = 8136.6624, rounded half-up to 8136.66.
        AMT_FEDERAL_SURTAX_AT_48_PERCENT: RateAppliedLine(
            output=AMT_FEDERAL_SURTAX_AT_48_PERCENT,
            base=AMT_BASIC_FEDERAL_TAX,
            base_amount=D("16951.38"),
            rate=Rate(D("0.48")),
            rounding=CENT,
            result=D("8136.66"),
        ),
        # Form T691 Part 6 line 9 "Federal surtax on business income earned outside Canada"
        # "Multiply the amount from line 7 by 48%.": line 7, the federal tax under the minimum tax
        # of 16951.38, at 48%, 16951.38 x 0.48 = 8136.6624, rounded half-up to 8136.66.
        AMT_PART_6_SURTAX_AT_48_PERCENT: RateAppliedLine(
            output=AMT_PART_6_SURTAX_AT_48_PERCENT,
            base=AMT_FEDERAL_TAX_UNDER_MINIMUM_TAX,
            base_amount=D("16951.38"),
            rate=Rate(D("0.48")),
            rounding=CENT,
            result=D("8136.66"),
        ),
        # Schedule 8 Part 5 line 70 "amount from line 43 multiplied by 50%": 0.00 x 50% for
        # Return A (no self-employment income, so line 43 is 0.00).
        CPP_PART_5_LINE_70: RateAppliedLine(
            output=CPP_PART_5_LINE_70,
            base=CPP_PART_5_LINE_43,
            base_amount=D("0.00"),
            rate=Rate(D("0.5")),
            rounding=CENT,
            result=D("0.00"),
        ),
        # Schedule 8 Part 5 line 71 "Amount from line 44 multiplied by 50%": 0.00 x 50% for
        # Return A.
        CPP_PART_5_LINE_71: RateAppliedLine(
            output=CPP_PART_5_LINE_71,
            base=CPP_PART_5_LINE_44,
            base_amount=D("0.00"),
            rate=Rate(D("0.5")),
            rounding=CENT,
            result=D("0.00"),
        ),
        # Schedule 8 Part 5 line 84 "Amount from line 45 multiplied by 50%": 0.00 x 50% for
        # Return A.
        CPP_PART_5_LINE_84: RateAppliedLine(
            output=CPP_PART_5_LINE_84,
            base=CPP_PART_5_LINE_45,
            base_amount=D("0.00"),
            rate=Rate(D("0.5")),
            rounding=CENT,
            result=D("0.00"),
        ),
        # Schedule 8 Part 5 line 75 "Line A multiply by 83.1933": 0.00 x 83.1933% for Return A.
        CPP_PART_5_LINE_75: RateAppliedLine(
            output=CPP_PART_5_LINE_75,
            base=CPP_PART_5_LINE_75_BASE,
            base_amount=D("0.00"),
            rate=Rate(D("0.831933")),
            rounding=CENT,
            result=D("0.00"),
        ),
        # Schedule 8 Part 5 line 50 "multiplied by 50%": 0 x 50% for Return A.
        CPP_PART_5_LINE_50: RateAppliedLine(
            output=CPP_PART_5_LINE_50,
            base=CPP_PART_5_LINE_50_LINE_49_POSITIVE,
            base_amount=D("0"),
            rate=Rate(D("0.5")),
            rounding=CENT,
            result=D("0.00"),
        ),
        # Schedule 8 Part 3 line 9 "amount from line 8 multiplied by 83.1933%": Return A's T4 box 16
        # equals the required contributions (line 13), so the base share is line 11.
        CPP_ACTUAL_BASE_CONTRIBUTIONS: RateAppliedLine(
            CPP_ACTUAL_BASE_CONTRIBUTIONS,
            CPP_T4_BASE_AND_FIRST_ADDITIONAL_CONTRIBUTIONS,
            D("4034.10"),
            Rate(D("0.831933")),
            CENT,
            D("3356.10"),
        ),
        # Form T691 Part 1 line 31 "× 40%" of the gifts under a security option plan (67914): Return
        # A has none, so the base and the 40% are 0.
        AMT_SECURITY_OPTION_GIFTS_DEDUCTION: RateAppliedLine(
            AMT_SECURITY_OPTION_GIFTS_DEDUCTION,
            AMT_SECURITY_OPTION_PUBLICLY_LISTED_GIFTS,
            D("0"),
            Rate(D("0.4")),
            CENT,
            D("0"),
        ),
        # Form T2125 Chart C line 24 "× 85%" of amount 23 or the list price limit with tax: Return A
        # has no leased vehicle, so the base is 44706.00 and the 85% is 38000.10.
        BUSINESS_VEHICLE_LEASE_PRICE_85_PERCENT: RateAppliedLine(
            BUSINESS_VEHICLE_LEASE_PRICE_85_PERCENT,
            BUSINESS_VEHICLE_LEASE_PRICE_BASE,
            D("44706.00"),
            Rate(D("0.85")),
            CENT,
            D("38000.10"),
        ),
        # Form T2042 Chart C line 24 "× 85%" of amount 23 or the list price limit with tax: Return A
        # has no leased vehicle, so the base is 44706.00 and the 85% is 38000.10.
        FARM_VEHICLE_LEASE_PRICE_85_PERCENT: RateAppliedLine(
            FARM_VEHICLE_LEASE_PRICE_85_PERCENT,
            FARM_VEHICLE_LEASE_PRICE_BASE,
            D("44706.00"),
            Rate(D("0.85")),
            CENT,
            D("38000.10"),
        ),
        # Form T2121 Chart C line 24 "× 85%" of amount 23 or the list price limit with tax: Return A
        # has no leased vehicle, so the base is 44706.00 and the 85% is 38000.10.
        FISH_VEHICLE_LEASE_PRICE_85_PERCENT: RateAppliedLine(
            FISH_VEHICLE_LEASE_PRICE_85_PERCENT,
            FISH_VEHICLE_LEASE_PRICE_BASE,
            D("44706.00"),
            Rate(D("0.85")),
            CENT,
            D("38000.10"),
        ),
        # Form T691 Part 1 line 80 "Line 78 multiply by the percentage from line 79": line 78 is
        # 3074.00 (line 63: the union dues of line 21200, 2000.00, and the enhanced CPP
        # contributions of line 22215, 1074.00), and 50% of it is 1537.00.
        AMT_APPLICABLE_RATE_AMOUNT: RateAppliedLine(
            AMT_APPLICABLE_RATE_AMOUNT,
            AMT_ADJUSTMENTS_BEFORE_RATE_TOTAL,
            D("3074.00"),
            Rate(D("0.5")),
            CENT,
            D("1537.00"),
        ),
        # Form T691 Part 1 line 26 "× 30%" applied to "Line 24 minus line 25": Return A has no
        # gifts of publicly listed securities, so the net is 0 and so is the 30%.
        AMT_PUBLICLY_LISTED_GIFTS_ADJUSTMENT: RateAppliedLine(
            AMT_PUBLICLY_LISTED_GIFTS_ADJUSTMENT,
            AMT_PUBLICLY_LISTED_GIFTS_NET,
            D("0"),
            Rate(D("0.3")),
            CENT,
            D("0"),
        ),
        # Federal Worksheet "Line 23500" line 18 "Amount from line 17 multiplied by 15%": Return A's
        # line 17 is 115000 - 93343.00 = 21657.00 (the chart does not apply, line 23500 is 0).
        SOCIAL_BENEFITS_LINE_18: RateAppliedLine(
            SOCIAL_BENEFITS_LINE_18,
            SOCIAL_BENEFITS_LINE_17,
            D("21657.00"),
            Rate(D("0.15")),
            CENT,
            D("3248.55"),
        ),
        # T2038(IND) Part C amounts 1 and 2: the expenditures on lines 67193 and 67195 at 15% and
        # 20%, here 0.
        ITC_RECAPTURE_AT_15_PERCENT: RateAppliedLine(
            ITC_RECAPTURE_AT_15_PERCENT,
            ITC_RECAPTURE_EXPENDITURE_AT_15_PERCENT,
            D("0"),
            Rate(D("0.15")),
            CENT,
            D("0"),
        ),
        ITC_RECAPTURE_AT_20_PERCENT: RateAppliedLine(
            ITC_RECAPTURE_AT_20_PERCENT,
            ITC_RECAPTURE_EXPENDITURE_AT_20_PERCENT,
            D("0"),
            Rate(D("0.20")),
            CENT,
            D("0"),
        ),
        # Line 41400's "15% of the net cost reported on line 41300", before the maximum of $750.
        LABOUR_SPONSORED_FUNDS_CREDIT_BEFORE_MAXIMUM: RateAppliedLine(
            LABOUR_SPONSORED_FUNDS_CREDIT_BEFORE_MAXIMUM,
            LABOUR_SPONSORED_FUNDS_NET_COST,
            D("0"),
            Rate(D("0.15")),
            CENT,
            D("0"),
        ),
        # Form T1172 line 10 (line 8 x 20%, Part A) and line 13 (line 11 x 20%, Part B).
        RESP_AIPS_PART_A_TAX: RateAppliedLine(
            RESP_AIPS_PART_A_TAX,
            RESP_AIPS_SUBJECT_TO_TAX,
            D("0"),
            Rate(D("0.20")),
            CENT,
            D("0"),
        ),
        RESP_AIPS_PART_B_TAX: RateAppliedLine(
            RESP_AIPS_PART_B_TAX,
            RESP_AIPS_RECEIVED_PART_B,
            D("0"),
            Rate(D("0.20")),
            CENT,
            D("0"),
        ),
        # Form T2222 line 12 "Enter your net income from line 23600 of your return. multiplied by
        # 20%" and line 15 "Enter the total from box B. multiplied by 50%".
        RESIDENCY_NET_INCOME_LIMIT: RateAppliedLine(
            RESIDENCY_NET_INCOME_LIMIT,
            NET_INCOME,
            D("115000"),
            Rate(D("0.20")),
            CENT,
            D("23000.00"),
        ),
        TRAVEL_ZONE_B_DEDUCTION: RateAppliedLine(
            TRAVEL_ZONE_B_DEDUCTION, TRAVEL_TOTAL_ZONE_B, D("0"), Rate(D("0.50")), CENT, D("0")
        ),
        # The Federal Worksheet's "Line 40425" line 6 (line B x 9.0301%) and line 7 (line C x
        # 15.0198%), on no dividends with no slip.
        OTHER_DIVIDENDS_CREDIT: RateAppliedLine(
            OTHER_DIVIDENDS_CREDIT,
            DIVIDENDS_AMOUNT_B,
            D("0"),
            Rate(D("0.090301")),
            CENT,
            D("0"),
        ),
        ELIGIBLE_DIVIDENDS_CREDIT: RateAppliedLine(
            ELIGIBLE_DIVIDENDS_CREDIT,
            DIVIDENDS_AMOUNT_A_LESS_B,
            D("0"),
            Rate(D("0.150198")),
            CENT,
            D("0"),
        ),
        # Worksheet ON428's "Line 61520" line 1 (line B x 2.9863%) and line 2 (line C x 10%), on
        # no dividends.
        ontario.OTHER_DIVIDENDS_CREDIT: RateAppliedLine(
            ontario.OTHER_DIVIDENDS_CREDIT,
            ontario.DIVIDENDS_AMOUNT_B,
            D("0"),
            Rate(D("0.029863")),
            CENT,
            D("0"),
        ),
        ontario.ELIGIBLE_DIVIDENDS_CREDIT: RateAppliedLine(
            ontario.ELIGIBLE_DIVIDENDS_CREDIT,
            ontario.DIVIDENDS_AMOUNT_A_LESS_B,
            D("0"),
            Rate(D("0.1")),
            CENT,
            D("0"),
        ),
        # Form T1206 Part 3 lines 33 (20.53% of the total split income), 38 (5.05% of line 36),
        # 42 (10% of the line 18 amount) and 45 (2.9863% of the line 2 amount), on no split income.
        ontario.ONTARIO_TAX_ON_SPLIT_INCOME: RateAppliedLine(
            ontario.ONTARIO_TAX_ON_SPLIT_INCOME,
            TOTAL_SPLIT_INCOME,
            D("0"),
            Rate(D("0.2053")),
            CENT,
            D("0"),
        ),
        ontario.SPLIT_INCOME_LINE_38: RateAppliedLine(
            ontario.SPLIT_INCOME_LINE_38,
            ontario.SPLIT_INCOME_LINE_36,
            D("0"),
            Rate(D("0.0505")),
            CENT,
            D("0"),
        ),
        ontario.SPLIT_INCOME_LINE_42: RateAppliedLine(
            ontario.SPLIT_INCOME_LINE_42,
            SPLIT_INCOME_LINE_18,
            D("0"),
            Rate(D("0.1")),
            CENT,
            D("0"),
        ),
        ontario.SPLIT_INCOME_LINE_45: RateAppliedLine(
            ontario.SPLIT_INCOME_LINE_45,
            SPLIT_INCOME_DIVIDENDS_OTHER_THAN_ELIGIBLE,
            D("0"),
            Rate(D("0.029863")),
            CENT,
            D("0"),
        ),
        # Schedule 3 Part 5 line 24 "Line 22 multiplied by the percentage on line 23": Return A's
        # line 22 (line 21, 19700) is the 20000 of its one share row.
        INCLUDED_CAPITAL_GAIN: RateAppliedLine(
            INCLUDED_CAPITAL_GAIN,
            CAPITAL_GAIN,
            D("20000"),
            Rate(D("0.5")),
            CENT,
            D("10000"),
        ),
        CREDIT_AMOUNTS_AT_CREDIT_RATE: RateAppliedLine(
            CREDIT_AMOUNTS_AT_CREDIT_RATE,
            NON_REFUNDABLE_CREDIT_AMOUNTS,
            D("22033.58"),
            Rate(D("0.145")),
            CENT,
            D("3194.87"),
        ),
        # Schedule 9 line 6 "Enter your net income from line 23600 of your return. Line A"
        # "multiplied by 75%", line 7 "Amount B plus amount C Line D" "multiplied by 25%", line 20
        # "Line F" "multiplied by 33%", line 21 "Line G" "multiplied by 29%" and line 22 "Line H"
        # "multiplied by 14.5%": Return A has donations of 0, so every line but line 6 is 0.
        DONATION_LIMIT_ON_NET_INCOME: RateAppliedLine(
            DONATION_LIMIT_ON_NET_INCOME, NET_INCOME, D("115000"), Rate(D("0.75")), CENT, D("86250")
        ),
        # Form T1206 Part 2 line 8 "Amount from line 7 multiplied by 33%" (line 7 being line 4),
        # line 14 "Line 13" "× 14.5%", line 19 "Line 17" "× 9.0301%" and line 20 "Line 18"
        # "× 15.0198%": all 0 for Return A, which has no split income.
        FEDERAL_TAX_ON_SPLIT_INCOME: RateAppliedLine(
            FEDERAL_TAX_ON_SPLIT_INCOME, TOTAL_SPLIT_INCOME, D("0"), Rate(D("0.33")), CENT, D("0")
        ),
        SPLIT_INCOME_LINE_14: RateAppliedLine(
            SPLIT_INCOME_LINE_14, SPLIT_INCOME_LINE_13, D("0"), Rate(D("0.145")), CENT, D("0")
        ),
        SPLIT_INCOME_LINE_19: RateAppliedLine(
            SPLIT_INCOME_LINE_19,
            SPLIT_INCOME_DIVIDENDS_OTHER_THAN_ELIGIBLE,
            D("0"),
            Rate(D("0.090301")),
            CENT,
            D("0"),
        ),
        SPLIT_INCOME_LINE_20: RateAppliedLine(
            SPLIT_INCOME_LINE_20, SPLIT_INCOME_LINE_18, D("0"), Rate(D("0.150198")), CENT, D("0")
        ),
        # T1 line 108 "Amount from line 23600 multiplied by 3%".
        MEDICAL_NET_INCOME_SHARE: RateAppliedLine(
            MEDICAL_NET_INCOME_SHARE, NET_INCOME, D("115000"), Rate(D("0.03")), CENT, D("3450.00")
        ),
        # ON428 line 39 "Line 37 multiplied by the percentage from line 38".
        ontario.MEDICAL_NET_INCOME_SHARE: RateAppliedLine(
            ontario.MEDICAL_NET_INCOME_SHARE,
            NET_INCOME,
            D("115000"),
            Rate(D("0.03")),
            CENT,
            D("3450.00"),
        ),
        CAPITAL_GIFTS_LIMIT_ADDITION: RateAppliedLine(
            CAPITAL_GIFTS_LIMIT_ADDITION,
            CAPITAL_GIFTS_TOTAL,
            D("0"),
            Rate(D("0.25")),
            CENT,
            D("0.00"),
        ),
        HIGH_INCOME_DONATION_CREDIT: RateAppliedLine(
            HIGH_INCOME_DONATION_CREDIT,
            HIGH_INCOME_DONATIONS,
            D("0"),
            Rate(D("0.33")),
            CENT,
            D("0.00"),
        ),
        REGULAR_RATE_DONATION_CREDIT: RateAppliedLine(
            REGULAR_RATE_DONATION_CREDIT,
            REGULAR_RATE_DONATIONS,
            D("0"),
            Rate(D("0.29")),
            CENT,
            D("0.00"),
        ),
        FIRST_TIER_DONATION_CREDIT: RateAppliedLine(
            FIRST_TIER_DONATION_CREDIT,
            DONATIONS_FIRST_TIER,
            D("0"),
            Rate(D("0.145")),
            CENT,
            D("0.00"),
        ),
        # Federal Worksheet line 6 "Applicable rate 3.45%" and line 7 "Line 5 multiplied by the
        # percentage from line 6": line 5 is 0.
        TOP_UP_TAX_CREDIT: RateAppliedLine(
            TOP_UP_TAX_CREDIT, TOP_UP_EXCESS, D("0"), Rate(D("0.0345")), CENT, D("0.00")
        ),
        ontario.CREDIT_AMOUNTS_AT_CREDIT_RATE: RateAppliedLine(
            ontario.CREDIT_AMOUNTS_AT_CREDIT_RATE,
            ontario.NON_REFUNDABLE_CREDIT_AMOUNTS,
            D("17180.58"),
            Rate(D("0.0505")),
            CENT,
            D("867.62"),
        ),
        # ON428 line 47 "Amount from line 13 of your federal Schedule 9" "multiplied by 5.05%" and
        # line 48 "Amount from line 14 of your federal Schedule 9" "multiplied by 11.16%": lines
        # 13 and 14 are 0.
        ontario.DONATIONS_FIRST_TIER_CREDIT: RateAppliedLine(
            ontario.DONATIONS_FIRST_TIER_CREDIT,
            DONATIONS_FIRST_TIER,
            D("0"),
            Rate(D("0.0505")),
            CENT,
            D("0.00"),
        ),
        ontario.DONATIONS_OVER_FIRST_TIER_CREDIT: RateAppliedLine(
            ontario.DONATIONS_OVER_FIRST_TIER_CREDIT,
            DONATIONS_OVER_FIRST_TIER,
            D("0"),
            Rate(D("0.1116")),
            CENT,
            D("0.00"),
        ),
        # ON479 line 1 "Eligible medical expenses for fertility treatment multiplied by 25%
        # (maximum $5,000)", before its maximum: no expenses.
        FERTILITY_CREDIT_BEFORE_MAXIMUM: RateAppliedLine(
            FERTILITY_CREDIT_BEFORE_MAXIMUM,
            FERTILITY_EXPENSES,
            D("0"),
            Rate(D("0.25")),
            CENT,
            D("0"),
        ),
        # ON479 line 4 "Allowable percentage 25%" and line 5 "Line 3 multiplied by the percentage
        # from line 4", before its maximum: line 3 is ON428 line 58769, 0 for Return A.
        SENIORS_CARE_BEFORE_MAXIMUM: RateAppliedLine(
            SENIORS_CARE_BEFORE_MAXIMUM,
            ontario.MEDICAL_CLAIM,
            D("0"),
            Rate(D("0.25")),
            CENT,
            D("0"),
        ),
        # ON479 line 11 "Applicable rate 5%" and line 12 "Line 10 multiplied by the percentage from
        # line 11": 5% of 115000.00 - 35000.00 = 80000.00.
        SENIORS_CARE_REDUCTION: RateAppliedLine(
            SENIORS_CARE_REDUCTION,
            SENIORS_CARE_INCOME_OVER_BASE,
            D("80000.00"),
            Rate(D("0.05")),
            CENT,
            D("4000.00"),
        ),
        # T1 line 161 (line 46900) "multiplied by 25%", on the supplies expenses after their
        # maximum of $1,000.
        EDUCATOR_SCHOOL_SUPPLY_CREDIT: RateAppliedLine(
            EDUCATOR_SCHOOL_SUPPLY_CREDIT,
            EDUCATOR_SUPPLIES_EXPENSES_AT_MOST_MAXIMUM,
            D("0"),
            Rate(D("0.25")),
            CENT,
            D("0"),
        ),
        # ON479 line 14 "multiplied by 15%", on the amount paid after its maximum of $3,000.
        SENIORS_TRANSIT_CREDIT: RateAppliedLine(
            SENIORS_TRANSIT_CREDIT,
            SENIORS_TRANSIT_AMOUNT_PAID_AT_MOST_MAXIMUM,
            D("0"),
            Rate(D("0.15")),
            CENT,
            D("0"),
        ),
        # Federal Worksheet line 5 "Applicable rate 15%" and line 6 "Line 4 multiplied by the
        # percentage from line 5": line 4 is the net income 115000 over the income threshold.
        AGE_REDUCTION: RateAppliedLine(
            AGE_REDUCTION,
            AGE_INCOME_OVER_THRESHOLD,
            D("69478.00"),
            Rate(D("0.15")),
            CENT,
            D("10421.70"),
        ),
        # Worksheet ON479 column 1 line 5 "Line 3 multiplied by the percentage from line 4":
        # line 3 is 0.
        ontario.POLITICAL_CREDIT_COLUMN_1_LINE_5: RateAppliedLine(
            ontario.POLITICAL_CREDIT_COLUMN_1_LINE_5,
            ontario.POLITICAL_CREDIT_COLUMN_1_LINE_3,
            D("0"),
            Rate(D("0.75")),
            CENT,
            D("0.00"),
        ),
        # Worksheet ON479 column 2 line 5 "Line 3 multiplied by the percentage from line 4":
        # line 3 is 0.
        ontario.POLITICAL_CREDIT_COLUMN_2_LINE_5: RateAppliedLine(
            ontario.POLITICAL_CREDIT_COLUMN_2_LINE_5,
            ontario.POLITICAL_CREDIT_COLUMN_2_LINE_3,
            D("0"),
            Rate(D("0.5")),
            CENT,
            D("0.00"),
        ),
        # Worksheet ON479 column 3 line 5 "Line 3 multiplied by the percentage from line 4":
        # line 3 is 0.
        ontario.POLITICAL_CREDIT_COLUMN_3_LINE_5: RateAppliedLine(
            ontario.POLITICAL_CREDIT_COLUMN_3_LINE_5,
            ontario.POLITICAL_CREDIT_COLUMN_3_LINE_3,
            D("0"),
            Rate(D("0.3333")),
            CENT,
            D("0.00"),
        ),
        # Federal Worksheet column 1 line 5 "Line 3 multiplied by the percentage from line 4 =":
        # line 3 is 0.
        POLITICAL_CREDIT_COLUMN_1_LINE_5: RateAppliedLine(
            POLITICAL_CREDIT_COLUMN_1_LINE_5,
            POLITICAL_CREDIT_COLUMN_1_LINE_3,
            D("0"),
            Rate(D("0.75")),
            CENT,
            D("0.00"),
        ),
        # Federal Worksheet column 2 line 5 "Line 3 multiplied by the percentage from line 4 =":
        # line 3 is 0.
        POLITICAL_CREDIT_COLUMN_2_LINE_5: RateAppliedLine(
            POLITICAL_CREDIT_COLUMN_2_LINE_5,
            POLITICAL_CREDIT_COLUMN_2_LINE_3,
            D("0"),
            Rate(D("0.5")),
            CENT,
            D("0.00"),
        ),
        # Federal Worksheet column 3 line 5 "Line 3 multiplied by the percentage from line 4 =":
        # line 3 is 0.
        POLITICAL_CREDIT_COLUMN_3_LINE_5: RateAppliedLine(
            POLITICAL_CREDIT_COLUMN_3_LINE_5,
            POLITICAL_CREDIT_COLUMN_3_LINE_3,
            D("0"),
            Rate(D("0.3333")),
            CENT,
            D("0.00"),
        ),
        # ON479 line 17 and line 63220 "multiplied by 5%", on Form T1221 line 4: no slips, 0.
        FLOW_THROUGH_SHARE_CREDIT: RateAppliedLine(
            FLOW_THROUGH_SHARE_CREDIT,
            FLOW_THROUGH_SHARE_EXPENSES,
            D("0"),
            Rate(D("0.05")),
            CENT,
            D("0"),
        ),
        # Worksheet ON428 line 5 "Applicable rate 15%" and line 6 "Line 4 multiplied by the
        # percentage from line 5": line 4 is the net income 115000 over the income threshold.
        ontario.AGE_REDUCTION: RateAppliedLine(
            ontario.AGE_REDUCTION,
            ontario.AGE_INCOME_OVER_THRESHOLD,
            D("68670.00"),
            Rate(D("0.15")),
            CENT,
            D("10300.50"),
        ),
        # ON428 line 87 and line 62150 "multiplied by 25%": the qualifying donations of 0.
        COMMUNITY_FOOD_PROGRAM_CREDIT: RateAppliedLine(
            COMMUNITY_FOOD_PROGRAM_CREDIT,
            COMMUNITY_FOOD_PROGRAM_DONATIONS,
            D("0"),
            Rate(D("0.25")),
            CENT,
            D("0.00"),
        ),
        # Schedule ON428-A line 5 "Line 3 multiplied by the percentage from line 4 (maximum
        # $875)", before its maximum: line 3 is employment income (line 10100), as line 2 (line
        # 10400) is not triggered.
        LIFT_CREDIT_BEFORE_MAXIMUM: RateAppliedLine(
            LIFT_CREDIT_BEFORE_MAXIMUM,
            EMPLOYMENT_INCOME,
            D("110000"),
            Rate(D("0.0505")),
            CENT,
            D("5555.00"),
        ),
        # Schedule ON428-A line 40 "Line 38 multiplied by the percentage from line 39": line 38,
        # the greater of lines 32 and 37 (82500 and 50000), at 5% (line 39).
        ontario.LIFT_FAMILY_REDUCTION: RateAppliedLine(
            ontario.LIFT_FAMILY_REDUCTION,
            ontario.LIFT_GREATER_EXCESS,
            D("82500"),
            Rate(D("0.05")),
            CENT,
            D("4125.00"),
        ),
        # Form T1436 line 20 (T1 line 21700).
        ALLOWABLE_BUSINESS_INVESTMENT_LOSS: RateAppliedLine(
            ALLOWABLE_BUSINESS_INVESTMENT_LOSS,
            BUSINESS_INVESTMENT_LOSS_AFTER_REDUCTION,
            D("0"),
            Rate(D("0.5")),
            CENT,
            D("0.00"),
        ),
        # Federal Worksheet "Line 45200 - Refundable medical expense supplement" (T1 line 154),
        # Return A: line 21500 and line 33200 are 0, so line 11 and line 13 are 0.
        MEDICAL_SUPPLEMENT_LINE_13: RateAppliedLine(
            output=MEDICAL_SUPPLEMENT_LINE_13,
            base=MEDICAL_SUPPLEMENT_LINE_11,
            base_amount=D("0"),
            rate=Rate(D("0.25")),
            rounding=CENT,
            result=D("0.00"),
        ),
        MEDICAL_SUPPLEMENT_LINE_15: RateAppliedLine(
            output=MEDICAL_SUPPLEMENT_LINE_15,
            base=MEDICAL_SUPPLEMENT_LINE_8,
            base_amount=D("81706.00"),
            rate=Rate(D("0.05")),
            rounding=CENT,
            result=D("4085.30"),
        ),
        # Schedule 8 Part 4 line 15 "amount from line 10 multiplied by 50%": no self-employment
        # income, so line 10 is 0.
        SELF_EMPLOYED_CPP_BASE_CREDIT: RateAppliedLine(
            SELF_EMPLOYED_CPP_BASE_CREDIT,
            SELF_EMPLOYED_CPP_BASE_CONTRIBUTIONS,
            D("0"),
            Rate(D("0.5")),
            CENT,
            D("0"),
        ),
        # Schedule 11, Schedule 2 and line 45350 (Return A claims none: every figure is 0).
        CANADA_TRAINING_CREDIT_BASIS: RateAppliedLine(
            output=CANADA_TRAINING_CREDIT_BASIS,
            base=CANADIAN_TUITION_FEES,
            base_amount=D("0"),
            rate=Rate(D("0.5")),
            rounding=CENT,
            result=D("0.00"),
        ),
        # Form T2048 (line 25395) and Chart A: Return A enters nothing on the form, so its lines
        # are 0 (or, where they read another line, that line's figure).
        QBT_EXPLORATION_EXPENSES_AT_HALF: RateAppliedLine(
            QBT_EXPLORATION_EXPENSES_AT_HALF,
            EXPLORATION_AND_DEVELOPMENT_EXPENSES,
            D("0"),
            Rate(D("0.5")),
            CENT,
            D("0.00"),
        ),
        QBT_RECOVERY_OF_EXPLORATION_EXPENSES: RateAppliedLine(
            QBT_RECOVERY_OF_EXPLORATION_EXPENSES,
            OTHER_INCOME,
            D("0"),
            Rate(D("0.5")),
            CENT,
            D("0.00"),
        ),
        QBT_TAXABLE_AMOUNT_ALLOCATED: RateAppliedLine(
            QBT_TAXABLE_AMOUNT_ALLOCATED,
            QBT_AMOUNT_ALLOCATED,
            D("0.00"),
            Rate(D("0.5")),
            CENT,
            D("0.00"),
        ),
        QBT_TAXABLE_CAPITAL_GAINS: RateAppliedLine(
            QBT_TAXABLE_CAPITAL_GAINS,
            QBT_TOTAL_CAPITAL_GAINS,
            D("0"),
            Rate(D("0.5")),
            CENT,
            D("0.00"),
        ),
        # Form T691 Part 1 line 84 "B × 13.0435%": B is the amount of line 12010 of the return, 0.
        AMT_DIVIDENDS_OTHER_THAN_ELIGIBLE_ADJUSTMENT: RateAppliedLine(
            AMT_DIVIDENDS_OTHER_THAN_ELIGIBLE_ADJUSTMENT,
            TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
            D("0"),
            Rate(D("0.130435")),
            CENT,
            D("0"),
        ),
        # Form T691 Part 1 line 85 "C × 27.5362%": C is amount A minus amount B, 0.
        AMT_DIVIDENDS_DIFFERENCE_ADJUSTMENT: RateAppliedLine(
            AMT_DIVIDENDS_DIFFERENCE_ADJUSTMENT,
            AMT_AMOUNT_A_MINUS_AMOUNT_B,
            D("0"),
            Rate(D("0.275362")),
            CENT,
            D("0"),
        ),
        # Form T691 Part 1 line 87 "× 40%" of the amount from line 25400 of the return, 0.
        AMT_LIFETIME_EXEMPTION_ADJUSTMENT: RateAppliedLine(
            AMT_LIFETIME_EXEMPTION_ADJUSTMENT,
            CAPITAL_GAINS_DEDUCTION,
            D("0"),
            Rate(D("0.40")),
            CENT,
            D("0"),
        ),
        # Form T691 Part 1 line 97 "Gross minimum amount": line 95 multiplied by 20.5%. Return A's
        # line 95 is 0, as line 93 (126537.00) is under the basic exemption.
        AMT_GROSS_MINIMUM_AMOUNT: RateAppliedLine(
            AMT_GROSS_MINIMUM_AMOUNT,
            AMT_NET_ADJUSTED_TAXABLE_INCOME,
            D("0"),
            Rate(D("0.205")),
            CENT,
            D("0"),
        ),
        # Form T691 Part 1 line 98 "× 50%" of line 33800 of the return, 3194.87: 1597.435, a tie,
        # rounded half-up to 1597.44.
        AMT_NON_REFUNDABLE_CREDITS_ADJUSTMENT: RateAppliedLine(
            AMT_NON_REFUNDABLE_CREDITS_ADJUSTMENT,
            CREDIT_AMOUNTS_AT_CREDIT_RATE,
            D("3194.87"),
            Rate(D("0.5")),
            CENT,
            D("1597.44"),
        ),
        # Form T691 Part 1 line 99 "× 80%" of line 34900 of the return, 0.
        AMT_DONATIONS_AND_GIFTS_ADJUSTMENT: RateAppliedLine(
            AMT_DONATIONS_AND_GIFTS_ADJUSTMENT,
            DONATIONS_AND_GIFTS_CREDIT,
            D("0"),
            Rate(D("0.8")),
            CENT,
            D("0"),
        ),
    }
