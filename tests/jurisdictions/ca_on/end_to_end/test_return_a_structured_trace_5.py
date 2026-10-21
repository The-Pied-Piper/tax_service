"""CA-ON 2025 end to end, Return A: return a structured trace 5."""

from __future__ import annotations

from app.domain.parameters.rate import Rate
from app.domain.parameters.rate_table import RateTableRow
from app.domain.parameters.rounding import RoundingMode, RoundTo
from app.domain.trace import (
    AmountWhenMoreLine,
    BracketColumnLine,
    ChosenByRangeLine,
    ChosenBySignLine,
    ChosenRateAppliedLine,
    CountAtLeastLine,
    DividedByRateLine,
    ItemsTotalLine,
    LesserOfWhenPositiveLine,
    PositivePartOfNegationLine,
    RateByIncomeBandLine,
    RatioTruncatedLine,
    RoundedTotalLine,
)
from app.jurisdictions.ca.catalog import (
    CHILD_CARE_EXPENSES,
    CPP_MAXIMUM_PENSIONABLE_EARNINGS,
    CPP_MONTHS,
    FEDERAL_BASIC_TAX,
    OTHER_DEPENDANTS_MEDICAL,
    POLITICAL_CONTRIBUTIONS,
    POLITICAL_CREDIT_BEFORE_MAXIMUM,
    POLITICAL_CREDIT_CHOSEN_COLUMN,
    POLITICAL_CREDIT_COLUMN_1_LINE_7,
    POLITICAL_CREDIT_SHORTCUT_THRESHOLD,
    QPP_MONTHS,
    RC381_EMPLOYMENT_CPP_BASE_CONTRIBUTIONS,
    RC381_EMPLOYMENT_CPP_ENHANCED_CONTRIBUTIONS,
    RC381_PART_2_LINE_B,
    RC381_PART_2_LINE_G,
    RC381_PART_3_LINE_3,
    RC381_PART_3_LINE_6,
    RC381_PART_3_LINE_15,
    RC381_PART_3_LINE_15_LESSER,
    RC381_PART_3_LINE_35,
    RC381_PART_3_LINE_35_LESSER,
    RC381_PART_3_LINE_52,
    RC381_PART_3_LINE_53,
    RC381_PART_3_LINE_59,
    RC381_PART_3_LINE_60,
    RC381_PART_3_LINE_61,
    RC381_PART_3_LINE_67,
    RC381_PART_3_LINE_68,
    RC381_PART_3_LINE_69,
    RC381_PART_3_LINE_75,
    RC381_PART_3_LINE_76,
    RC381_PART_3_LINE_77,
    RC381_PART_3_LINE_78,
    RC381_PART_3_LINE_80,
    RC381_PART_3_LINE_81,
    RC381_PART_3_LINE_82,
    RC381_PART_3_LINE_83,
    RC381_PART_3_LINE_84,
    RC381_PART_3_LINE_85,
    RC381_PART_3_LINE_87,
    RC381_PART_3_LINE_87_DIFFERENCE,
    RC381_PART_3_LINE_89,
    RC381_PART_3_LINE_90,
    RC381_PART_3_LINE_91,
    RC381_PART_3_LINE_93,
    RC381_PART_4_LINE_13,
    RC381_PART_4_LINE_14,
    RC381_PART_4_LINE_17,
    RC381_PART_4_LINE_17A,
    RC381_PART_4_LINE_20,
    RC381_PART_4_LINE_21,
    RC381_PART_4_LINE_21_FROM_LINE_17,
    RC381_PART_4_LINE_21_LESSER,
    RC381_PART_4_LINE_22,
    RC381_PART_4_LINE_23,
    RC381_PART_4_LINE_23_LESSER,
    RC381_PART_4_LINE_24,
    RC381_PART_4_LINE_25A,
    RC381_PART_4_LINE_31,
    RC381_PART_4_LINE_33,
    RC381_PART_4_LINE_34,
    RC381_PART_4_LINE_35,
    RC381_PART_4_LINE_35AA,
    RC381_PART_4_LINE_35AA_FROM_LINE_17,
    RC381_PART_4_LINE_35AB,
    RC381_PART_4_LINE_35AB_FROM_LINE_20,
    RC381_PART_4_LINE_35AB_WHEN_LINE_35_ZERO,
    RC381_PART_4_LINE_46,
    RC381_PART_4_LINE_51,
    RC381_PART_4_LINE_54,
    RC381_PART_4_LINE_55,
    RC381_PART_4_LINE_56,
    RC381_PART_4_LINE_74,
    RC381_PART_4_LINE_76,
    RC381_PART_4_LINE_83,
    RC381_PART_4_LINE_83_LESSER,
    RC381_PART_4_LINE_90,
    RC381_PART_4_LINE_91_FROM_LINE_90,
    RENTAL_NON_COMPLIANT_EXPENSES,
    T4_CPP_CONTRIBUTIONS_BOX_16,
    T4_CPP_PENSIONABLE_EARNINGS_OUTSIDE_QUEBEC,
    TAXABLE_INCOME,
)
from app.jurisdictions.ca.trace import OtherDependantMedicalLine, ShortTermRentalNonCompliantLine
from app.jurisdictions.ca_on import catalog as ontario
from app.jurisdictions.ca_on.catalog import (
    CARE_CREDIT,
    CARE_CREDIT_PERCENTAGE,
    CARE_FAMILY_ADJUSTED_INCOME,
    ONTARIO_BASIC_TAX,
)
from tests.jurisdictions.ca_on.end_to_end.support import CENT, D, return_a


def test_the_trace_records_each_total_as_a_structured_line() -> None:
    trace = return_a().trace
    totals = {line.output: line for line in trace if isinstance(line, RoundedTotalLine)}
    ranged = {line.output: line for line in trace if isinstance(line, ChosenByRangeLine)}
    bands = {line.output: line for line in trace if isinstance(line, RateByIncomeBandLine)}
    chosen_rates = {
        line.output: line
        for line in trace
        if isinstance(line, ChosenRateAppliedLine) and line.output is CARE_CREDIT
    }
    counts_at_least = {line.output: line for line in trace if isinstance(line, CountAtLeastLine)}
    truncated = {line.output: line for line in trace if isinstance(line, RatioTruncatedLine)}
    when_more = {line.output: line for line in trace if isinstance(line, AmountWhenMoreLine)}
    chosen_by_sign = {line.output: line for line in trace if isinstance(line, ChosenBySignLine)}
    positive_parts = {
        line.output: line for line in trace if isinstance(line, PositivePartOfNegationLine)
    }
    lesser_when_positive = {
        line.output: line for line in trace if isinstance(line, LesserOfWhenPositiveLine)
    }
    # Form RC381 Part 3b lines 75 "If line 53 is positive or "0", enter the amount from line 52",
    # 82 "If line 60 is positive or "0", enter the amount from line 59" and 89 "If line 68 is
    # positive or "0", enter the amount from line 67", and the three results of Part 3a and Part
    # 3b, chosen by the sign of line 69: Return A's lines 53, 60, 68 and 69 are all 0, so each is
    # in the "positive or 0" branch (or, for the two results, the "0 or negative" branch of Part
    # 3b). The overpayment of line 44800 is line 69 not below zero, a floored sum of line 69.
    assert chosen_by_sign == {
        # Form RC381 Part 4 line 31 (the difference "Line 29 minus line 30" when line 61 of Part 3
        # is positive), line 35A's two sentences (line 35A takes line 17 when line 35 is positive,
        # and line 20 in brackets when line 35 is "0" and then only when line 61 is negative) and
        # lines 46 and 51 (the differences, when line 68 of Part 3 is positive): Return A's lines
        # 61, 35 and 68 are all 0, so line 31, line 35aa, line 35ab, line 46 and line 51 have no
        # candidate for "0", and line 35ab's choice for line 35 at "0" takes the amount from line
        # 20 in brackets (0).
        RC381_PART_4_LINE_31: ChosenBySignLine(
            output=RC381_PART_4_LINE_31,
            sign_kind=RC381_PART_3_LINE_61,
            sign=D("0"),
            chosen_kind=None,
            chosen_value=D("0"),
        ),
        RC381_PART_4_LINE_35AA: ChosenBySignLine(
            output=RC381_PART_4_LINE_35AA,
            sign_kind=RC381_PART_4_LINE_35,
            sign=D("0"),
            chosen_kind=None,
            chosen_value=D("0"),
        ),
        RC381_PART_4_LINE_35AB_WHEN_LINE_35_ZERO: ChosenBySignLine(
            output=RC381_PART_4_LINE_35AB_WHEN_LINE_35_ZERO,
            sign_kind=RC381_PART_4_LINE_35,
            sign=D("0"),
            chosen_kind=RC381_PART_4_LINE_35AB_FROM_LINE_20,
            chosen_value=D("0"),
        ),
        RC381_PART_4_LINE_35AB: ChosenBySignLine(
            output=RC381_PART_4_LINE_35AB,
            sign_kind=RC381_PART_3_LINE_61,
            sign=D("0"),
            chosen_kind=None,
            chosen_value=D("0"),
        ),
        RC381_PART_4_LINE_46: ChosenBySignLine(
            output=RC381_PART_4_LINE_46,
            sign_kind=RC381_PART_3_LINE_68,
            sign=D("0"),
            chosen_kind=None,
            chosen_value=D("0"),
        ),
        RC381_PART_4_LINE_51: ChosenBySignLine(
            output=RC381_PART_4_LINE_51,
            sign_kind=RC381_PART_3_LINE_68,
            sign=D("0"),
            chosen_kind=None,
            chosen_value=D("0"),
        ),
        # Form RC381 Part 4 line 13 "Line 5 minus line 12" (line 61 of Part 3 positive; else line
        # 5), line 21 (by the sign of line 20), line 23 (by the sign of line 69 of Part 3), line
        # 24 and line 25A (line 61 negative): Return A's lines 61, 20 and 69 are all 0, so line 13
        # takes line 5 ("0" or negative), line 21 has no candidate for "0", line 23 takes the
        # lesser ("positive or 0"), and lines 24 and 25A have none for "0".
        RC381_PART_4_LINE_13: ChosenBySignLine(
            output=RC381_PART_4_LINE_13,
            sign_kind=RC381_PART_3_LINE_61,
            sign=D("0"),
            chosen_kind=T4_CPP_CONTRIBUTIONS_BOX_16,
            chosen_value=D("0"),
        ),
        RC381_PART_4_LINE_21: ChosenBySignLine(
            output=RC381_PART_4_LINE_21,
            sign_kind=RC381_PART_4_LINE_20,
            sign=D("0"),
            chosen_kind=None,
            chosen_value=D("0"),
        ),
        RC381_PART_4_LINE_23: ChosenBySignLine(
            output=RC381_PART_4_LINE_23,
            sign_kind=RC381_PART_3_LINE_69,
            sign=D("0"),
            chosen_kind=RC381_PART_4_LINE_23_LESSER,
            chosen_value=D("0"),
        ),
        RC381_PART_4_LINE_24: ChosenBySignLine(
            output=RC381_PART_4_LINE_24,
            sign_kind=RC381_PART_3_LINE_61,
            sign=D("0"),
            chosen_kind=None,
            chosen_value=D("0"),
        ),
        RC381_PART_4_LINE_25A: ChosenBySignLine(
            output=RC381_PART_4_LINE_25A,
            sign_kind=RC381_PART_3_LINE_61,
            sign=D("0"),
            chosen_kind=None,
            chosen_value=D("0"),
        ),
        RC381_PART_3_LINE_75: ChosenBySignLine(
            output=RC381_PART_3_LINE_75,
            sign_kind=RC381_PART_3_LINE_53,
            sign=D("0"),
            chosen_kind=RC381_PART_3_LINE_52,
            chosen_value=D("0"),
        ),
        RC381_PART_3_LINE_82: ChosenBySignLine(
            output=RC381_PART_3_LINE_82,
            sign_kind=RC381_PART_3_LINE_60,
            sign=D("0"),
            chosen_kind=RC381_PART_3_LINE_59,
            chosen_value=D("0"),
        ),
        RC381_PART_3_LINE_89: ChosenBySignLine(
            output=RC381_PART_3_LINE_89,
            sign_kind=RC381_PART_3_LINE_68,
            sign=D("0"),
            chosen_kind=RC381_PART_3_LINE_67,
            chosen_value=D("0"),
        ),
        RC381_EMPLOYMENT_CPP_BASE_CONTRIBUTIONS: ChosenBySignLine(
            output=RC381_EMPLOYMENT_CPP_BASE_CONTRIBUTIONS,
            sign_kind=RC381_PART_3_LINE_69,
            sign=D("0"),
            chosen_kind=RC381_PART_3_LINE_81,
            chosen_value=D("0"),
        ),
        RC381_EMPLOYMENT_CPP_ENHANCED_CONTRIBUTIONS: ChosenBySignLine(
            output=RC381_EMPLOYMENT_CPP_ENHANCED_CONTRIBUTIONS,
            sign_kind=RC381_PART_3_LINE_69,
            sign=D("0"),
            chosen_kind=RC381_PART_3_LINE_93,
            chosen_value=D("0"),
        ),
    }
    # Form RC381 Part 3b lines 76, 83 and 90 "Enter the amount from line 53 (60, 68) as a positive
    # amount": none is negative for Return A.
    assert positive_parts == {
        # Form RC381 Part 4 line 91 "amount from line 90 entered as a positive amount": Return A's
        # line 90 is not negative.
        RC381_PART_4_LINE_91_FROM_LINE_90: PositivePartOfNegationLine(
            output=RC381_PART_4_LINE_91_FROM_LINE_90,
            amount_kind=RC381_PART_4_LINE_90,
            amount_value=D("0.00"),
            result=D("0"),
        ),
        # Form RC381 Part 4 line 33 "Enter the amount from line 61 of Part 3 as a positive amount."
        # and line 54 "Enter the amount from line 68 of Part 3 as a positive amount.": neither is
        # negative for Return A.
        RC381_PART_4_LINE_33: PositivePartOfNegationLine(
            output=RC381_PART_4_LINE_33,
            amount_kind=RC381_PART_3_LINE_61,
            amount_value=D("0"),
            result=D("0"),
        ),
        RC381_PART_4_LINE_54: PositivePartOfNegationLine(
            output=RC381_PART_4_LINE_54,
            amount_kind=RC381_PART_3_LINE_68,
            amount_value=D("0"),
            result=D("0"),
        ),
        # Form RC381 Part 4 line 14 "Enter the amount from line 61 of Part 3 as a positive
        # amount." and line 17A "If line 17 is negative, enter it as a positive amount.": neither
        # is negative for Return A.
        RC381_PART_4_LINE_14: PositivePartOfNegationLine(
            output=RC381_PART_4_LINE_14,
            amount_kind=RC381_PART_3_LINE_61,
            amount_value=D("0"),
            result=D("0"),
        ),
        RC381_PART_4_LINE_17A: PositivePartOfNegationLine(
            output=RC381_PART_4_LINE_17A,
            amount_kind=RC381_PART_4_LINE_17,
            amount_value=D("0"),
            result=D("0"),
        ),
        RC381_PART_3_LINE_76: PositivePartOfNegationLine(
            output=RC381_PART_3_LINE_76,
            amount_kind=RC381_PART_3_LINE_53,
            amount_value=D("0"),
            result=D("0"),
        ),
        RC381_PART_3_LINE_83: PositivePartOfNegationLine(
            output=RC381_PART_3_LINE_83,
            amount_kind=RC381_PART_3_LINE_60,
            amount_value=D("0"),
            result=D("0"),
        ),
        RC381_PART_3_LINE_90: PositivePartOfNegationLine(
            output=RC381_PART_3_LINE_90,
            amount_kind=RC381_PART_3_LINE_68,
            amount_value=D("0"),
            result=D("0"),
        ),
    }
    # Form RC381 Part 3b lines 77, 80, 84, 87 and 91, "whichever is less" when the lines are
    # positive: none is positive for Return A, so each is "0".
    assert lesser_when_positive == {
        # Form RC381 Part 4 line 34 "If line 17A is positive, enter whichever is less: amount from
        # line 17A or line 33.", line 35A's amounts from line 17 and (in brackets) from line 20 and
        # line 55 "If line 61 of Part 3 is positive, enter whichever is less: amount from line 61
        # of Part 3 or line 54.": none is positive for Return A, so each is "0".
        RC381_PART_4_LINE_34: LesserOfWhenPositiveLine(
            output=RC381_PART_4_LINE_34,
            parts=((RC381_PART_4_LINE_17A, D("0")), (RC381_PART_4_LINE_33, D("0"))),
            all_positive=False,
            bracket=False,
            result=D("0"),
        ),
        RC381_PART_4_LINE_35AA_FROM_LINE_17: LesserOfWhenPositiveLine(
            output=RC381_PART_4_LINE_35AA_FROM_LINE_17,
            parts=((RC381_PART_4_LINE_17, D("0")),),
            all_positive=False,
            bracket=False,
            result=D("0"),
        ),
        RC381_PART_4_LINE_35AB_FROM_LINE_20: LesserOfWhenPositiveLine(
            output=RC381_PART_4_LINE_35AB_FROM_LINE_20,
            parts=((RC381_PART_4_LINE_20, D("0")),),
            all_positive=False,
            bracket=True,
            result=D("0"),
        ),
        RC381_PART_4_LINE_55: LesserOfWhenPositiveLine(
            output=RC381_PART_4_LINE_55,
            parts=((RC381_PART_3_LINE_61, D("0")), (RC381_PART_4_LINE_54, D("0"))),
            all_positive=False,
            bracket=False,
            result=D("0"),
        ),
        # Form RC381 Part 4 line 21, "If line 17 is positive, enter the amount from line 17 (show
        # in brackets)" and "If line 20 is positive, enter whichever is less: amount from line 20
        # or line 17A": none is positive for Return A, so each is "0".
        RC381_PART_4_LINE_21_FROM_LINE_17: LesserOfWhenPositiveLine(
            output=RC381_PART_4_LINE_21_FROM_LINE_17,
            parts=((RC381_PART_4_LINE_17, D("0")),),
            all_positive=False,
            bracket=True,
            result=D("0"),
        ),
        RC381_PART_4_LINE_21_LESSER: LesserOfWhenPositiveLine(
            output=RC381_PART_4_LINE_21_LESSER,
            parts=((RC381_PART_4_LINE_20, D("0")), (RC381_PART_4_LINE_17A, D("0"))),
            all_positive=False,
            bracket=False,
            result=D("0"),
        ),
        RC381_PART_3_LINE_77: LesserOfWhenPositiveLine(
            output=RC381_PART_3_LINE_77,
            parts=((RC381_PART_3_LINE_60, D("0")), (RC381_PART_3_LINE_76, D("0"))),
            all_positive=False,
            bracket=False,
            result=D("0"),
        ),
        RC381_PART_3_LINE_80: LesserOfWhenPositiveLine(
            output=RC381_PART_3_LINE_80,
            parts=((RC381_PART_3_LINE_68, D("0")), (RC381_PART_3_LINE_78, D("0"))),
            all_positive=False,
            bracket=False,
            result=D("0"),
        ),
        RC381_PART_3_LINE_84: LesserOfWhenPositiveLine(
            output=RC381_PART_3_LINE_84,
            parts=((RC381_PART_3_LINE_53, D("0")), (RC381_PART_3_LINE_83, D("0"))),
            all_positive=False,
            bracket=False,
            result=D("0"),
        ),
        RC381_PART_3_LINE_87: LesserOfWhenPositiveLine(
            output=RC381_PART_3_LINE_87,
            parts=((RC381_PART_3_LINE_85, D("0")), (RC381_PART_3_LINE_87_DIFFERENCE, D("0"))),
            all_positive=False,
            bracket=False,
            result=D("0"),
        ),
        RC381_PART_3_LINE_91: LesserOfWhenPositiveLine(
            output=RC381_PART_3_LINE_91,
            parts=((RC381_PART_3_LINE_61, D("0")), (RC381_PART_3_LINE_90, D("0"))),
            all_positive=False,
            bracket=False,
            result=D("0"),
        ),
    }
    # Form RC381 Part 2 "The number you enter on line A cannot be more than the number you enter on
    # line B.": Return A's lines A and B are both 12.
    assert counts_at_least == {
        RC381_PART_2_LINE_B: CountAtLeastLine(
            output=RC381_PART_2_LINE_B,
            count_kind=QPP_MONTHS,
            count=12,
            minimum_kind=CPP_MONTHS,
            minimum=12,
        )
    }
    # Form RC381 Part 3 line 6 "Line 4 divided by line 5 (calculated to the fifth decimal place
    # without rounding)": Return A has no T4 pensionable earnings, so line 3 is 0 and line 6 is 0.
    assert truncated == {
        # Form RC381 Part 4 line 22 "If line 17A is more than line 14, enter "1". If not, enter
        # the result of line 17A divided by line 14 (calculated to the fifth decimal place
        # without rounding).": lines 17A and 14 are both 0, so line 17A is not more and line 22 is
        # 0 (a zero divisor gives 0).
        RC381_PART_4_LINE_22: RatioTruncatedLine(
            output=RC381_PART_4_LINE_22,
            dividend=RC381_PART_4_LINE_17A,
            dividend_amount=D("0"),
            divisor=RC381_PART_4_LINE_14,
            divisor_amount=D("0"),
            rounding=RoundTo(D("0.00001"), RoundingMode.DOWN),
            cap_at_one=True,
            result=D("0"),
        ),
        RC381_PART_3_LINE_6: RatioTruncatedLine(
            output=RC381_PART_3_LINE_6,
            dividend=T4_CPP_PENSIONABLE_EARNINGS_OUTSIDE_QUEBEC,
            dividend_amount=D("0"),
            divisor=RC381_PART_3_LINE_3,
            divisor_amount=D("0"),
            rounding=RoundTo(D("0.00001"), RoundingMode.DOWN),
            cap_at_one=False,
            result=D("0"),
        ),
    }
    # Form RC381 Part 3 line 15, when "the amount from line 3 is more than the amount from line C
    # of Part 2": line 3 is 0, not more than line C (71,300.00), so line 15 is 0.
    assert when_more == {
        # Form RC381 Part 4 line 83, "If line 74 is more than line 57, complete lines 75 to 83. If
        # not, enter "0" on line 83": Return A's line 74 is 0, not more than line C (71,300.00).
        RC381_PART_4_LINE_83: AmountWhenMoreLine(
            output=RC381_PART_4_LINE_83,
            amount_kind=RC381_PART_4_LINE_83_LESSER,
            amount_value=D("0.00"),
            more_kind=RC381_PART_4_LINE_74,
            more_value=D("0.00"),
            than_kind=CPP_MAXIMUM_PENSIONABLE_EARNINGS,
            than_value=D("71300.00"),
            result=D("0"),
        ),
        # Form RC381 Part 3 line 35, when "the amount from line 3 is more than the amount from line
        # G of Part 2": line 3 is 0, not more than line G (71,300.00), so line 35 is 0.
        RC381_PART_3_LINE_35: AmountWhenMoreLine(
            output=RC381_PART_3_LINE_35,
            amount_kind=RC381_PART_3_LINE_35_LESSER,
            amount_value=D("0"),
            more_kind=RC381_PART_3_LINE_3,
            more_value=D("0"),
            than_kind=RC381_PART_2_LINE_G,
            than_value=D("71300.00"),
            result=D("0"),
        ),
        RC381_PART_3_LINE_15: AmountWhenMoreLine(
            output=RC381_PART_3_LINE_15,
            amount_kind=RC381_PART_3_LINE_15_LESSER,
            amount_value=D("0.00"),
            more_kind=RC381_PART_3_LINE_3,
            more_value=D("0"),
            than_kind=CPP_MAXIMUM_PENSIONABLE_EARNINGS,
            than_value=D("71300.00"),
            result=D("0"),
        ),
    }
    # Schedule ON479-A line 7: 115,000 is "more than $114,000 but not more than $117,600: 19%".
    assert bands == {
        CARE_CREDIT_PERCENTAGE: RateByIncomeBandLine(
            output=CARE_CREDIT_PERCENTAGE,
            income=CARE_FAMILY_ADJUSTED_INCOME,
            income_amount=D("115000"),
            row=RateTableRow(D("114000"), D("117600"), Rate(D("0.19"))),
            rate=Rate(D("0.19")),
        )
    }
    # Schedule ON479-A line 8 "Line 6 multiplied by the percentage from line 7": line 6 is 0.
    assert chosen_rates == {
        CARE_CREDIT: ChosenRateAppliedLine(
            output=CARE_CREDIT,
            base=CHILD_CARE_EXPENSES,
            base_amount=D("0"),
            rate_kind=CARE_CREDIT_PERCENTAGE,
            rate=Rate(D("0.19")),
            rounding=CENT,
            result=D("0.00"),
        )
    }
    assert ranged == {
        ontario.POLITICAL_CREDIT_BEFORE_MAXIMUM: ChosenByRangeLine(
            output=ontario.POLITICAL_CREDIT_BEFORE_MAXIMUM,
            tested_kind=ontario.POLITICAL_CONTRIBUTIONS,
            tested_value=D("0"),
            chosen_kind=ontario.POLITICAL_CREDIT_COLUMN_1_LINE_7,
            chosen_value=D("0.00"),
        ),
        POLITICAL_CREDIT_CHOSEN_COLUMN: ChosenByRangeLine(
            output=POLITICAL_CREDIT_CHOSEN_COLUMN,
            tested_kind=POLITICAL_CONTRIBUTIONS,
            tested_value=D("0"),
            chosen_kind=POLITICAL_CREDIT_COLUMN_1_LINE_7,
            chosen_value=D("0.00"),
        ),
        POLITICAL_CREDIT_BEFORE_MAXIMUM: ChosenByRangeLine(
            output=POLITICAL_CREDIT_BEFORE_MAXIMUM,
            tested_kind=POLITICAL_CREDIT_SHORTCUT_THRESHOLD,
            tested_value=D("1275"),
            chosen_kind=POLITICAL_CREDIT_CHOSEN_COLUMN,
            chosen_value=D("0.00"),
        ),
    }
    assert totals[FEDERAL_BASIC_TAX].base == TAXABLE_INCOME
    assert totals[FEDERAL_BASIC_TAX].base_amount == D("115000")
    assert totals[FEDERAL_BASIC_TAX].amount == D("20146.25")
    assert totals[ONTARIO_BASIC_TAX].base == TAXABLE_INCOME
    assert totals[ONTARIO_BASIC_TAX].amount == D("8539.60")
    columns = [line for line in trace if isinstance(line, BracketColumnLine)]
    assert len(columns) == 2
    assert set(columns) == {
        BracketColumnLine(
            lower=D("114750"),
            rate=D("0.26"),
            excess=D("250"),
            tax_at_start=D("20081.25"),
            tax=D("20146.25"),
        ),
        BracketColumnLine(
            lower=D("105775"),
            rate=D("0.1116"),
            excess=D("9225"),
            tax_at_start=D("7510.09"),
            tax=D("8539.60"),
        ),
    }
    assert [
        line
        for line in trace
        if isinstance(line, OtherDependantMedicalLine | ItemsTotalLine)
        and line.output == OTHER_DEPENDANTS_MEDICAL
    ] == [ItemsTotalLine(output=OTHER_DEPENDANTS_MEDICAL, items=(), total=D("0"))]
    # T776 line 9366 (Chart A line B): Return A has no short-term rental rows, so no per-row
    # lines and a total of 0.
    assert [
        line
        for line in trace
        if isinstance(line, ShortTermRentalNonCompliantLine | ItemsTotalLine)
        and line.output == RENTAL_NON_COMPLIANT_EXPENSES
    ] == [ItemsTotalLine(output=RENTAL_NON_COMPLIANT_EXPENSES, items=(), total=D("0"))]
    # Form RC381 Part 4 line 76 "Amount from line 56 ÷ 4% =": Return A's line 56 is 0, so the
    # quotient is 0.00.
    assert [
        line
        for line in trace
        if isinstance(line, DividedByRateLine) and line.output == RC381_PART_4_LINE_76
    ] == [
        DividedByRateLine(
            RC381_PART_4_LINE_76,
            RC381_PART_4_LINE_56,
            D("0"),
            Rate(D("0.04")),
            CENT,
            D("0.00"),
        )
    ]
