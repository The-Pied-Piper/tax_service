"""CA-ON 2025 end to end, Return A: return a structured trace 5."""

from __future__ import annotations

from app.domain.parameters.rate import Rate
from app.domain.parameters.rate_table import RateTableRow
from app.domain.parameters.rounding import RoundingMode, RoundTo
from app.domain.trace import (
    AmountWhenMoreLine,
    BracketColumnLine,
    ChosenByRangeLine,
    ChosenRateAppliedLine,
    CountAtLeastLine,
    ItemsTotalLine,
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
    RC381_PART_2_LINE_B,
    RC381_PART_3_LINE_3,
    RC381_PART_3_LINE_6,
    RC381_PART_3_LINE_15,
    RC381_PART_3_LINE_15_LESSER,
    RENTAL_NON_COMPLIANT_EXPENSES,
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
        RC381_PART_3_LINE_6: RatioTruncatedLine(
            output=RC381_PART_3_LINE_6,
            dividend=T4_CPP_PENSIONABLE_EARNINGS_OUTSIDE_QUEBEC,
            dividend_amount=D("0"),
            divisor=RC381_PART_3_LINE_3,
            divisor_amount=D("0"),
            rounding=RoundTo(D("0.00001"), RoundingMode.DOWN),
            cap_at_one=False,
            result=D("0"),
        )
    }
    # Form RC381 Part 3 line 15, when "the amount from line 3 is more than the amount from line C
    # of Part 2": line 3 is 0, not more than line C (71,300.00), so line 15 is 0.
    assert when_more == {
        RC381_PART_3_LINE_15: AmountWhenMoreLine(
            output=RC381_PART_3_LINE_15,
            amount_kind=RC381_PART_3_LINE_15_LESSER,
            amount_value=D("0.00"),
            more_kind=RC381_PART_3_LINE_3,
            more_value=D("0"),
            than_kind=CPP_MAXIMUM_PENSIONABLE_EARNINGS,
            than_value=D("71300.00"),
            result=D("0"),
        )
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
