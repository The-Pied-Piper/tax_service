"""CA-ON 2025 end to end: return ci."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import pytest

from app.adapters.inbound.trace_english import EnglishTraceRenderer
from app.domain.errors import InputAboveBoundError, InvalidRecordError
from app.domain.worksheet import Worksheet
from app.jurisdictions.ca.catalog import (
    CCA_CLASS_NUMBER,
    CCA_UCC_AT_END,
    FEDERAL_BASIC_TAX,
    NET_INCOME,
    NET_RENTAL_INCOME,
    REFUND_OR_BALANCE_OWING,
    RENTAL_CCA_CLAIM,
    RENTAL_CCA_LIMIT,
    RENTAL_CCA_TABLE_CLAIM,
    RENTAL_CLOSING_UCC,
    RENTAL_NET_INCOME_AFTER_CCA,
    RENTAL_NET_INCOME_AFTER_TERMINAL_LOSS,
    RENTAL_RECAPTURED_CCA,
    RENTAL_TERMINAL_LOSS,
    TAXABLE_INCOME,
    TOTAL_INCOME,
    TOTAL_PAYABLE,
)
from app.jurisdictions.ca_on.catalog import ONTARIO_BASIC_TAX
from tests.jurisdictions.ca_on.end_to_end.support import D, rental_return

# Area A rows as (column 1, column 2, column 3, column 5, column 11, column 12, the claim, no
# property left, column 4, column 6, column 9, Note 9's remaining personal part): class 1 with a
# UCC of 100000.00 and proceeds of 40000.00 with property left, so column 7 is 60000.00 and the
# maximum 60000.00 x 4% = 2400.00, claimed in full; the remaining personal part of the property's
# cost is 5000.00, so column 24 is 60000.00 - 2400.00 - 5000.00 = 52600.00.
CLASS_1_ROW = ("1", "100000.00", "0", "40000.00", "0", "0", "2400.00", 0, "0", "0", "0", "5000.00")

RETURN_CI_STATEMENT: dict[str, Any] = {
    "rental_properties": ((2, "0", "24000"),),
    "rental_expenses": {
        "insurance": ("1200", "0", "0"),
        "interest_and_bank_charges": ("6000", "0", "0"),
        "repairs_and_maintenance": ("2900", "0", "0"),
        "property_taxes": ("3500", "0", "0"),
    },
    "rental_cca_classes_rows": (CLASS_1_ROW,),
}


def return_ci(
    changes: Mapping[str, Any] | None = None, **overrides: Any
) -> dict[str, tuple[Worksheet, ...]]:
    """Return CI's inputs, as in `returns/2025_return_ci.yaml`: Return BS's landlord with one
    Area A class whose property was partly disposed of and had a personal part (Note 9), and no
    immediate expensing.

    Gross rents of 24000 (one property, two units) are the only income; the expenses are the
    insurance 1200, the interest 6000, the property taxes 3500 and the repairs 2900, 13600 in all.
    The claim is 2400.00, so line 9936 is 2400.00 and line 9946 and T1 line 12600 are
    24000 - 13600 - 2400.00 = 8000.00, the net rental income of Return BS.
    """
    return rental_return(RETURN_CI_STATEMENT, changes, **overrides)


def class_1_row(
    claim: str = "2400.00", personal_part: str = "5000.00"
) -> tuple[str, str, str, str, str, str, str, int, str, str, str, str]:
    """Class 1 of Return CI with the given claim (column 23) and remaining personal part."""
    return ("1", "100000.00", "0", "40000.00", "0", "0", claim, 0, "0", "0", "0", personal_part)


def test_return_cis_class_1_closes_at_52600_after_the_remaining_personal_part() -> None:
    # Area A, class 1: column 7 is 100000.00 + 0 - 40000.00 = 60000.00; the maximum is 4% of
    # column 19, 60000.00, so 2400.00, claimed (column 23). Column 24 is column 7 minus column 23
    # (Note 9), less the remaining personal part of the property's cost: 60000.00 - 2400.00 -
    # 5000.00 = 52600.00.
    result = return_ci()
    statement = result["ca/t776"][0]

    records = statement.get(RENTAL_CLOSING_UCC).value.records
    assert [(record[CCA_CLASS_NUMBER], record[CCA_UCC_AT_END]) for record in records] == [
        (D("1"), D("52600.00")),
    ]


def test_return_cis_trace_names_the_remaining_personal_part() -> None:
    result = return_ci()
    rendered = EnglishTraceRenderer().render_all(result["ca/t776"][0].trace)

    for line in (
        "rental_cca_table_claim: item 1 class 1: column 7 60000, column 14 40000, column 15 0, "
        "column 16 40000, column 17 0, column 18 0, column 19 60000, "
        "maximum 4% of column 19 = 2400 (half-up to 0.01), claim 2400",
        "rental_closing_ucc: item 1 class 1: column 7 60000 less claim 2400 "
        "less personal part 5000 = 52600",
    ):
        assert line in rendered, line


def test_return_cis_personal_part_does_not_change_the_claim_or_the_recapture() -> None:
    # Note 9 changes only column 24: column 23 is still 2400.00 (line ii and line 9936), and
    # column 7 (60000.00) is positive with property left, so there is no recapture and no
    # terminal loss.
    result = return_ci()
    statement = result["ca/t776"][0]

    assert statement.get(RENTAL_CCA_TABLE_CLAIM).value == D("2400.00")
    assert statement.get(RENTAL_CCA_LIMIT).value == D("10400")
    assert statement.get(RENTAL_CCA_CLAIM).value == D("2400.00")
    assert statement.get(RENTAL_RECAPTURED_CCA).value == D("0")
    assert statement.get(RENTAL_TERMINAL_LOSS).value == D("0")


def test_return_cis_net_rental_income_is_8000_on_line_12600() -> None:
    # Amount 5 is 24000 - 13600 = 10400; amount 6 is 10400 - 2400.00 = 8000.00, which is line
    # 9946 and T1 line 12600. It is the whole of total income.
    result = return_ci()
    worksheet = result["ca-on/return"][0]
    statement = result["ca/t776"][0]

    assert statement.get(RENTAL_NET_INCOME_AFTER_TERMINAL_LOSS).value == D("10400")
    assert statement.get(RENTAL_NET_INCOME_AFTER_CCA).value == D("8000.00")
    assert worksheet.get(NET_RENTAL_INCOME).value == D("8000.00")
    assert worksheet.get(TOTAL_INCOME).value == D("8000.00")


def test_return_cis_tax_lines_are_return_bss() -> None:
    # Net income and taxable income are 8000.00 (no deductions), as in Return BS: the federal tax
    # on it is 8000.00 x 14.5% = 1160.00 and the Ontario tax 8000.00 x 5.05% = 404.00, each below
    # its non-refundable credits, so there is no tax payable.
    result = return_ci()
    worksheet = result["ca-on/return"][0]

    assert worksheet.get(NET_INCOME).value == D("8000.00")
    assert worksheet.get(TAXABLE_INCOME).value == D("8000.00")
    assert worksheet.get(FEDERAL_BASIC_TAX).value == D("1160.00")
    assert worksheet.get(ONTARIO_BASIC_TAX).value == D("404.00")
    assert worksheet.get(TOTAL_PAYABLE).value == D("0")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("0")


def test_a_personal_part_of_0_closes_the_class_at_column_7_less_the_claim() -> None:
    # 60000.00 - 2400.00 = 57600.00, and the line reads as one without a personal part.
    result = return_ci({"rental_cca_classes_rows": (class_1_row(personal_part="0"),)})
    statement = result["ca/t776"][0]

    (record,) = statement.get(RENTAL_CLOSING_UCC).value.records
    assert record[CCA_UCC_AT_END] == D("57600.00")
    rendered = EnglishTraceRenderer().render_all(statement.trace)
    assert "rental_closing_ucc: item 1 class 1: column 7 60000 less claim 2400 = 57600" in rendered
    assert statement.get(RENTAL_CCA_CLAIM).value == D("2400.00")


def test_a_personal_part_of_column_7_less_the_claim_closes_the_class_at_zero() -> None:
    # The part may be all that is left: 60000.00 - 2400.00 - 57600.00 = 0.00.
    result = return_ci({"rental_cca_classes_rows": (class_1_row(personal_part="57600.00"),)})

    (record,) = result["ca/t776"][0].get(RENTAL_CLOSING_UCC).value.records
    assert record[CCA_UCC_AT_END] == D("0")


def test_a_personal_part_above_column_7_less_the_claim_is_refused() -> None:
    # 57600.00 + 0.01 is more than the 57600.00 left after the claim.
    with pytest.raises(InvalidRecordError) as raised:
        return_ci({"rental_cca_classes_rows": (class_1_row(personal_part="57600.01"),)})

    assert str(raised.value) == (
        "ca/t776, instance 1: item 1: personal part (57600.01) is above column 7 less the claim "
        "(57600.00)"
    )


def test_a_smaller_claim_leaves_room_for_a_larger_personal_part() -> None:
    # With no claim, column 7 less the claim is 60000.00: a part of 60000.00 is allowed, and
    # 60000.01 is refused. The claim is not the personal part's to change: no CCA, line 9946 is
    # 10400 - 0 = 10400.00.
    result = return_ci({"rental_cca_classes_rows": (class_1_row("0", "60000.00"),)})

    (record,) = result["ca/t776"][0].get(RENTAL_CLOSING_UCC).value.records
    assert record[CCA_UCC_AT_END] == D("0")
    assert result["ca/t776"][0].get(RENTAL_CCA_CLAIM).value == D("0")
    with pytest.raises(InvalidRecordError) as raised:
        return_ci({"rental_cca_classes_rows": (class_1_row("0", "60000.01"),)})

    assert str(raised.value) == (
        "ca/t776, instance 1: item 1: personal part (60000.01) is above column 7 less the claim "
        "(60000.00)"
    )


def test_a_claim_above_the_maximum_is_still_refused_with_a_personal_part() -> None:
    with pytest.raises(InputAboveBoundError) as raised:
        return_ci({"rental_cca_classes_rows": (class_1_row("2400.01"),)})

    assert str(raised.value) == (
        "ca/t776, instance 1: item 1: ca/cca_claimed 2400.01 is above the maximum 2400.00"
    )
