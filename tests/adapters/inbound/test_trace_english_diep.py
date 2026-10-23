"""Unit tests for the English text of the DIEP columns in the CCA table's trace lines.

T776 Area A "Column 9: Immediate expensing amount for DIEPs (Note 5)". `CcaClaimLine` and
`ClosingUccLine` gain a field `column_9` (the immediate expensing amount of the class, 0 by
default); their English wording is unchanged when it is 0 and mentions it when it is above 0: the
claim line lists "column 9" after "column 7" in its columns, and the closing line reads "less claim
C (including column 9 N)". `ImmediateExpensingLine` (line i's one line per class) reads "column 4 A
less column 6 B, column 7 C: column 8 D, column 9 E".

Worked row, Class 8 (20%): column 7 6,000, column 9 3,000, column 18 1,000, column 19 2,000,
maximum 400.00, claim 3,400, column 24 6,000 - 3,400 = 2,600.
"""

from __future__ import annotations

from dataclasses import fields
from decimal import Decimal

from app.adapters.inbound.trace_english import EnglishTraceRenderer
from app.domain.artifact import ArtifactKind
from app.domain.record_list import RecordListKind
from app.domain.trace import TraceLine
from app.jurisdictions.ca.catalog import CCA_UCC_AT_END
from app.jurisdictions.ca.trace import (
    CcaClaimLine,
    CcaZeroReason,
    ClosingUccLine,
    ImmediateExpensingLine,
)
from tests.jurisdictions.ca.capabilities.cca_table import CENT, CLASS_8

D = Decimal
CCA_CLAIM = ArtifactKind("ex/cca_claim", Decimal)
CLOSING_UCC = RecordListKind("ex/closing_ucc", fields=(CCA_UCC_AT_END,))
IMMEDIATE_EXPENSING = ArtifactKind("ex/immediate_expensing_claim", Decimal)


def render(line: TraceLine) -> str:
    return EnglishTraceRenderer().render(line)


def claim_line(column_9: str) -> CcaClaimLine:
    return CcaClaimLine(
        output=CCA_CLAIM,
        position=1,
        class_rate=CLASS_8,
        no_property_left=0,
        column_7=D("6000"),
        column_14=D("0"),
        column_15=D("0"),
        column_16=D("0"),
        column_17=D("0"),
        column_18=D("1000"),
        column_19=D("2000"),
        zero_reason=CcaZeroReason.NONE,
        maximum=D("400.00"),
        rounding=CENT,
        claim=D("3400"),
        column_9=D(column_9),
    )


def closing_line(column_9: str, claim: str, result: str) -> ClosingUccLine:
    return ClosingUccLine(
        CLOSING_UCC,
        1,
        CLASS_8,
        0,
        D("6000"),
        CcaZeroReason.NONE,
        D(claim),
        D(result),
        column_9=D(column_9),
    )


def test_the_claim_line_lists_column_9_after_column_7() -> None:
    assert render(claim_line("3000")) == (
        "cca_claim: item 1 class 8: column 7 6000, column 9 3000, column 14 0, column 15 0, "
        "column 16 0, column 17 0, column 18 1000, column 19 2000, "
        "maximum 20% of column 19 = 400 (half-up to 0.01), claim 3400"
    )


def test_the_claim_line_is_unchanged_when_column_9_is_0() -> None:
    assert render(claim_line("0")) == (
        "cca_claim: item 1 class 8: column 7 6000, column 14 0, column 15 0, "
        "column 16 0, column 17 0, column 18 1000, column 19 2000, "
        "maximum 20% of column 19 = 400 (half-up to 0.01), claim 3400"
    )


def test_the_claim_line_without_a_column_9_reads_as_one_with_0() -> None:
    without = CcaClaimLine(
        output=CCA_CLAIM,
        position=1,
        class_rate=CLASS_8,
        no_property_left=0,
        column_7=D("6000"),
        column_14=D("0"),
        column_15=D("0"),
        column_16=D("0"),
        column_17=D("0"),
        column_18=D("1000"),
        column_19=D("2000"),
        zero_reason=CcaZeroReason.NONE,
        maximum=D("400.00"),
        rounding=CENT,
        claim=D("3400"),
    )

    assert without == claim_line("0")
    assert without.column_9 == D("0")


def test_the_closing_line_names_the_column_9_in_the_claim() -> None:
    assert render(closing_line("3000", "3400", "2600")) == (
        "closing_ucc: item 1 class 8: column 7 6000 less claim 3400 (including column 9 3000) "
        "= 2600"
    )


def test_the_closing_line_is_unchanged_when_column_9_is_0() -> None:
    assert render(closing_line("0", "2000", "4000")) == (
        "closing_ucc: item 1 class 8: column 7 6000 less claim 2000 = 4000"
    )


def test_column_9_is_the_last_field_of_the_claim_and_closing_lines() -> None:
    assert [f.name for f in fields(CcaClaimLine)][-1] == "column_9"
    assert [f.name for f in fields(ClosingUccLine)][-1] == "column_9"


def test_the_immediate_expensing_line_fields_in_order() -> None:
    assert [f.name for f in fields(ImmediateExpensingLine)] == [
        "output",
        "position",
        "class_rate",
        "column_4",
        "column_6",
        "column_7",
        "column_8",
        "column_9",
    ]


def test_the_immediate_expensing_line_amount_is_column_9() -> None:
    line = ImmediateExpensingLine(
        IMMEDIATE_EXPENSING, 1, CLASS_8, D("4000"), D("0"), D("6000"), D("4000"), D("3000")
    )

    assert line.amount == D("3000")
    assert "amount" not in [f.name for f in fields(line)]


def test_renders_the_immediate_expensing_of_a_class() -> None:
    line = ImmediateExpensingLine(
        IMMEDIATE_EXPENSING, 1, CLASS_8, D("4000.00"), D("0"), D("6000.00"), D("4000.00"), D("3000")
    )

    assert render(line) == (
        "immediate_expensing_claim: item 1 class 8: column 4 4000 less column 6 0, "
        "column 7 6000: column 8 4000, column 9 3000"
    )


def test_renders_a_column_8_cut_by_column_7() -> None:
    line = ImmediateExpensingLine(
        IMMEDIATE_EXPENSING, 2, CLASS_8, D("5000"), D("0"), D("3000"), D("3000"), D("3000")
    )

    assert render(line) == (
        "immediate_expensing_claim: item 2 class 8: column 4 5000 less column 6 0, "
        "column 7 3000: column 8 3000, column 9 3000"
    )


def test_renders_a_column_8_of_0_when_column_6_is_above_column_4() -> None:
    line = ImmediateExpensingLine(
        IMMEDIATE_EXPENSING, 1, CLASS_8, D("1000"), D("1500"), D("1500"), D("0"), D("0")
    )

    assert render(line) == (
        "immediate_expensing_claim: item 1 class 8: column 4 1000 less column 6 1500, "
        "column 7 1500: column 8 0, column 9 0"
    )
