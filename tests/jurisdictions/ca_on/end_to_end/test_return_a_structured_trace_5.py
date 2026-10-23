"""CA-ON 2025 end to end, Return A: return a structured trace 5."""

from __future__ import annotations

from app.domain.parameters.rate import Rate
from app.domain.parameters.rate_table import RateTableRow
from app.domain.trace import (
    BracketColumnLine,
    ChosenByRangeLine,
    ChosenBySignLine,
    ChosenRateAppliedLine,
    ItemsTotalLine,
    RateByIncomeBandLine,
    RoundedTotalLine,
)
from app.jurisdictions.ca.catalog import (
    CHILD_CARE_EXPENSES,
    FEDERAL_BASIC_TAX,
    OTHER_DEPENDANTS_MEDICAL,
    POLITICAL_CONTRIBUTIONS,
    POLITICAL_CREDIT_BEFORE_MAXIMUM,
    POLITICAL_CREDIT_CHOSEN_COLUMN,
    POLITICAL_CREDIT_COLUMN_1_LINE_7,
    POLITICAL_CREDIT_SHORTCUT_THRESHOLD,
    RENTAL_EPOP_PERCENTAGE_ROOM,
    RENTAL_IMMEDIATE_EXPENSING_ALLOCATED,
    RENTAL_IMMEDIATE_EXPENSING_SHARE,
    RENTAL_NON_COMPLIANT_EXPENSES,
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
from tests.jurisdictions.ca_on.end_to_end.support import CENT, D, run_a


def test_the_trace_records_each_total_as_a_structured_line() -> None:
    # The lines of the one T2125, T2042, T2121 and T776 statement of Return A, then those
    # of the return form.
    result = run_a()
    trace = (
        *result["ca/t2125"][0].trace,
        *result["ca/t2042"][0].trace,
        *result["ca/t2121"][0].trace,
        *result["ca/t776"][0].trace,
        *result["ca-on/return"][0].trace,
    )
    totals = {line.output: line for line in trace if isinstance(line, RoundedTotalLine)}
    chosen_by_sign = {line.output: line for line in trace if isinstance(line, ChosenBySignLine)}
    ranged = {line.output: line for line in trace if isinstance(line, ChosenByRangeLine)}
    bands = {line.output: line for line in trace if isinstance(line, RateByIncomeBandLine)}
    chosen_rates = {
        line.output: line
        for line in trace
        if isinstance(line, ChosenRateAppliedLine) and line.output is CARE_CREDIT
    }
    # Form T776 Area G Note 11 "If the total of column 3 is more than 100%, enter "0."": 100% less
    # the total of column 3 is 100.00 for Return A, not below zero, so line iii is the $1.5 million
    # times the percentage assigned to you, 0.00 for Return A.
    assert chosen_by_sign == {
        RENTAL_IMMEDIATE_EXPENSING_ALLOCATED: ChosenBySignLine(
            output=RENTAL_IMMEDIATE_EXPENSING_ALLOCATED,
            sign_kind=RENTAL_EPOP_PERCENTAGE_ROOM,
            sign=D("100.00"),
            chosen_kind=RENTAL_IMMEDIATE_EXPENSING_SHARE,
            chosen_value=D("0.00"),
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
