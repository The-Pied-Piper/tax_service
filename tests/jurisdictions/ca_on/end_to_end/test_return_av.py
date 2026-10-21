"""CA-ON 2025 end to end: return av."""

from __future__ import annotations

from typing import Any

import pytest

from app.adapters.inbound.trace_english import EnglishTraceRenderer
from app.domain.errors import ValidationError
from app.domain.worksheet import Worksheet
from app.jurisdictions.ca.capabilities.short_term_rental_non_compliant_cca import (
    ShortTermRentalNonCompliantCca,
)
from app.jurisdictions.ca.capabilities.short_term_rental_non_compliant_cca_by_class import (
    ShortTermRentalNonCompliantCcaByClass,
)
from app.jurisdictions.ca.catalog import (
    CCA_CLASS_NUMBER,
    NET_RENTAL_INCOME,
    NON_COMPLIANT_CCA,
    RENTAL_NON_COMPLIANT_CCA,
    RENTAL_NON_COMPLIANT_EXPENSES,
    SHORT_TERM_RENTAL_NON_COMPLIANT_CCA_BY_CLASS,
    TOTAL_INCOME,
)
from tests.jurisdictions.ca_on.end_to_end.support import D, compute

# Chart B rows as (column 1, column 4, column 5, column 6): class 1 with 900 and 30 days of 90,
# class 1 with 100 and 1 day of 3, class 8 with 500 and 45 days of 90.
ROWS: tuple[tuple[str, str, int, int], ...] = (
    ("1", "900", 30, 90),
    ("1", "100", 1, 3),
    ("8", "500", 45, 90),
)


def return_av(**overrides: Any) -> Worksheet:
    """Return AV's inputs, as in `returns/2025_return_av.yaml`: Return AD's landlord with three
    Chart B rows.

    Gross rents of 24000 (one property, two units) are the only income; the expenses are the
    insurance 1200, the interest 6000, the property taxes 3500 and the repairs 1300, 12000 in all.
    """
    inputs: dict[str, Any] = {
        "employment_income": "0",
        "share_dispositions": (),
        "unused_rrsp_contributions": "0",
        "rrsp_contributions": "0",
        "rrsp_deduction_limit": "0",
        "rrsp_amount_deducted": "0",
        "union_dues": "0",
        "rental_properties": ((2, "0", "24000"),),
        "rental_expenses": {
            "insurance": ("1200", "0", "0"),
            "interest_and_bank_charges": ("6000", "0", "0"),
            "repairs_and_maintenance": ("1300", "0", "0"),
            "property_taxes": ("3500", "0", "0"),
        },
        "short_term_rental_cca_units_rows": ROWS,
    }
    return compute(**{**inputs, **overrides})


def test_return_avs_line_9367_is_583_33_from_three_chart_b_rows() -> None:
    # Chart B column 7 is column 4 x column 5 / column 6, each row rounded half-up to the cent:
    # 900 x 30 / 90 = 300.00, 100 x 1 / 3 = 33.33 and 500 x 45 / 90 = 250.00; line C, and so
    # line 9367, is 300.00 + 33.33 + 250.00 = 583.33.
    worksheet = return_av()

    assert worksheet.get(RENTAL_NON_COMPLIANT_CCA).value == D("583.33")
    assert isinstance(
        worksheet.producer_of(RENTAL_NON_COMPLIANT_CCA), ShortTermRentalNonCompliantCca
    )


def test_return_avs_column_22_is_333_33_for_class_1_and_250_for_class_8() -> None:
    # "For each class, add the amounts from column 7 of Chart B and enter each total in column
    # 22 of Area A": class 1 is 300.00 + 33.33, class 8 is 250.00, in the order the classes appear.
    worksheet = return_av()

    records = worksheet.get(SHORT_TERM_RENTAL_NON_COMPLIANT_CCA_BY_CLASS).value.records
    assert [(record[CCA_CLASS_NUMBER], record[NON_COMPLIANT_CCA]) for record in records] == [
        (D("1"), D("333.33")),
        (D("8"), D("250.00")),
    ]
    assert isinstance(
        worksheet.producer_of(SHORT_TERM_RENTAL_NON_COMPLIANT_CCA_BY_CLASS),
        ShortTermRentalNonCompliantCcaByClass,
    )


def test_return_avs_chart_b_does_not_change_the_rental_income() -> None:
    # Nothing reads line 9367 or column 22 yet: Chart A's line 9366 is 0 and net rental income is
    # Return AD's 12000.
    worksheet = return_av()

    assert worksheet.get(RENTAL_NON_COMPLIANT_EXPENSES).value == D("0")
    assert worksheet.get(NET_RENTAL_INCOME).value == D("12000")
    assert worksheet.get(TOTAL_INCOME).value == D("12000")


def test_return_avs_trace_shows_each_chart_b_row_and_class() -> None:
    rendered = EnglishTraceRenderer().render_all(return_av().trace)

    for line in (
        "rental_non_compliant_cca: row 1: class 1 CCA 900 for 30 non-compliant days of 90 "
        "short-term days = 300 (half-up to 0.01)",
        "rental_non_compliant_cca: row 2: class 1 CCA 100 for 1 non-compliant days of 3 "
        "short-term days = 33.33 (half-up to 0.01)",
        "rental_non_compliant_cca: row 3: class 8 CCA 500 for 45 non-compliant days of 90 "
        "short-term days = 250 (half-up to 0.01)",
        "rental_non_compliant_cca: item 1 300 + item 2 33.33 + item 3 250 = 583.33",
        "short_term_rental_non_compliant_cca_by_class: item 1 class 1: column 7 300 + 33.33 "
        "= 333.33",
        "short_term_rental_non_compliant_cca_by_class: item 2 class 8: column 7 250 = 250",
    ):
        assert line in rendered, line


def test_no_chart_b_rows_give_zero_and_an_empty_list() -> None:
    worksheet = return_av(short_term_rental_cca_units_rows=())

    assert worksheet.get(RENTAL_NON_COMPLIANT_CCA).value == D("0")
    assert worksheet.get(SHORT_TERM_RENTAL_NON_COMPLIANT_CCA_BY_CLASS).value.records == ()
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert "rental_non_compliant_cca: no items = 0" in rendered


def test_a_row_with_900_of_cca_and_30_of_90_days_is_300_on_line_9367() -> None:
    worksheet = return_av(short_term_rental_cca_units_rows=(("1", "900", 30, 90),))

    assert worksheet.get(RENTAL_NON_COMPLIANT_CCA).value == D("300.00")


def test_a_chart_b_row_with_no_short_term_days_is_refused_naming_the_row() -> None:
    with pytest.raises(ValidationError, match="row 1: ca/short_term_rental_days cannot be 0"):
        return_av(short_term_rental_cca_units_rows=(("1", "900", 0, 0),))


def test_a_chart_b_row_with_more_non_compliant_days_than_days_is_refused() -> None:
    with pytest.raises(ValidationError, match="row 2.*short_term_rental_non_compliant_days"):
        return_av(short_term_rental_cca_units_rows=(ROWS[0], ("1", "900", 91, 90)))
