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
    BUSINESS_INVESTMENT_LOSS_AFTER_REDUCTION,
    CANADA_TRAINING_CREDIT_BASIS,
    CANADIAN_TUITION_FEES,
    CAPITAL_GAIN,
    CAPITAL_GIFTS_LIMIT_ADDITION,
    CAPITAL_GIFTS_TOTAL,
    CREDIT_AMOUNTS_AT_CREDIT_RATE,
    CWB_BEFORE_REDUCTION_WITH_DEPENDANT,
    CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT,
    CWB_REDUCTION_WITH_DEPENDANT,
    CWB_REDUCTION_WITHOUT_DEPENDANT,
    DIVIDENDS_AMOUNT_A_LESS_B,
    DIVIDENDS_AMOUNT_B,
    DONATION_LIMIT_ON_NET_INCOME,
    DONATIONS_FIRST_TIER,
    DONATIONS_OVER_FIRST_TIER,
    EDUCATOR_SCHOOL_SUPPLY_CREDIT,
    EDUCATOR_SUPPLIES_EXPENSES_AT_MOST_MAXIMUM,
    ELIGIBLE_DIVIDENDS_CREDIT,
    EMPLOYMENT_INCOME,
    FEDERAL_TAX_ON_SPLIT_INCOME,
    FIRST_TIER_DONATION_CREDIT,
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
    POLITICAL_CREDIT_COLUMN_1_LINE_3,
    POLITICAL_CREDIT_COLUMN_1_LINE_5,
    POLITICAL_CREDIT_COLUMN_2_LINE_3,
    POLITICAL_CREDIT_COLUMN_2_LINE_5,
    POLITICAL_CREDIT_COLUMN_3_LINE_3,
    POLITICAL_CREDIT_COLUMN_3_LINE_5,
    REGULAR_RATE_DONATION_CREDIT,
    REGULAR_RATE_DONATIONS,
    RESIDENCY_NET_INCOME_LIMIT,
    RESP_AIPS_PART_A_TAX,
    RESP_AIPS_PART_B_TAX,
    RESP_AIPS_RECEIVED_PART_B,
    RESP_AIPS_SUBJECT_TO_TAX,
    SELF_EMPLOYED_CPP_BASE_CONTRIBUTIONS,
    SELF_EMPLOYED_CPP_BASE_CREDIT,
    SPLIT_INCOME_DIVIDENDS_OTHER_THAN_ELIGIBLE,
    SPLIT_INCOME_LINE_13,
    SPLIT_INCOME_LINE_14,
    SPLIT_INCOME_LINE_18,
    SPLIT_INCOME_LINE_19,
    SPLIT_INCOME_LINE_20,
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
    assert rated == {
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
    }
