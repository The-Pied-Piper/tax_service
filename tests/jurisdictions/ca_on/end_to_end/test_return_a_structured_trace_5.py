"""CA-ON 2025 end to end, Return A: return a structured trace 5."""

from __future__ import annotations

from app.domain.trace import (
    BracketColumnLine,
    ChosenByRangeLine,
    ItemsTotalLine,
    OtherDependantMedicalLine,
    RoundedTotalLine,
)
from app.jurisdictions.ca.catalog import (
    FEDERAL_BASIC_TAX,
    OTHER_DEPENDANTS_MEDICAL,
    POLITICAL_CONTRIBUTIONS,
    POLITICAL_CREDIT_BEFORE_MAXIMUM,
    POLITICAL_CREDIT_CHOSEN_COLUMN,
    POLITICAL_CREDIT_COLUMN_1_LINE_7,
    POLITICAL_CREDIT_SHORTCUT_THRESHOLD,
    TAXABLE_INCOME,
)
from app.jurisdictions.ca_on import catalog as ontario
from app.jurisdictions.ca_on.catalog import (
    ONTARIO_BASIC_TAX,
)
from tests.jurisdictions.ca_on.end_to_end.support import D, return_a


def test_the_trace_records_each_total_as_a_structured_line() -> None:
    trace = return_a().trace
    totals = {line.output: line for line in trace if isinstance(line, RoundedTotalLine)}
    ranged = {line.output: line for line in trace if isinstance(line, ChosenByRangeLine)}
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
