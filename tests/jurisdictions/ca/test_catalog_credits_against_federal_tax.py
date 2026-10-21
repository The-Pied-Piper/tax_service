"""Registered and money kinds of the federal catalog family `credits_against_federal_tax`."""

from __future__ import annotations

from decimal import Decimal
from typing import Any

import pytest

from app.domain.artifact import ArtifactKind, ArtifactRegistry
from app.domain.errors import InvalidRecordError, NegativeArtifactError
from app.domain.record_list import RecordList, RecordListKind
from app.jurisdictions.ca.catalog import (
    CREDITS_AGAINST_FEDERAL_TAX,
    FEDERAL_TAX_LESS_CREDITS,
    FOREIGN_NON_BUSINESS_TAX_PAID,
    FOREIGN_TAX_COUNTRIES,
    FOREIGN_TAX_CREDIT_SHEET_LINE_3,
    FOREIGN_TAX_CREDIT_SHEETS,
    LABOUR_SPONSORED_FUNDS_CREDIT,
    LABOUR_SPONSORED_FUNDS_CREDIT_BEFORE_MAXIMUM,
    LABOUR_SPONSORED_FUNDS_NET_COST,
    NET_FOREIGN_NON_BUSINESS_INCOME,
    POLITICAL_CREDIT,
    POLITICAL_CREDIT_BEFORE_MAXIMUM,
    POLITICAL_CREDIT_CHOSEN_COLUMN,
    POLITICAL_CREDIT_COLUMN_1_LINE_2,
    POLITICAL_CREDIT_COLUMN_1_LINE_3,
    POLITICAL_CREDIT_COLUMN_1_LINE_5,
    POLITICAL_CREDIT_COLUMN_1_LINE_6,
    POLITICAL_CREDIT_COLUMN_1_LINE_7,
    POLITICAL_CREDIT_COLUMN_2_LINE_2,
    POLITICAL_CREDIT_COLUMN_2_LINE_3,
    POLITICAL_CREDIT_COLUMN_2_LINE_5,
    POLITICAL_CREDIT_COLUMN_2_LINE_6,
    POLITICAL_CREDIT_COLUMN_2_LINE_7,
    POLITICAL_CREDIT_COLUMN_3_LINE_2,
    POLITICAL_CREDIT_COLUMN_3_LINE_3,
    POLITICAL_CREDIT_COLUMN_3_LINE_5,
    POLITICAL_CREDIT_COLUMN_3_LINE_6,
    POLITICAL_CREDIT_COLUMN_3_LINE_7,
    POLITICAL_CREDIT_SHORTCUT_AMOUNT,
    POLITICAL_CREDIT_SHORTCUT_THRESHOLD,
)


def test_the_credits_against_federal_tax_kinds_are_the_registered_ones(
    registry: ArtifactRegistry,
) -> None:
    assert registry.get("ca/labour_sponsored_funds_net_cost") is LABOUR_SPONSORED_FUNDS_NET_COST
    assert registry.get("ca/political_credit_column_1_line_2") is POLITICAL_CREDIT_COLUMN_1_LINE_2
    assert registry.get("ca/political_credit_column_1_line_3") is POLITICAL_CREDIT_COLUMN_1_LINE_3
    assert registry.get("ca/political_credit_column_1_line_5") is POLITICAL_CREDIT_COLUMN_1_LINE_5
    assert registry.get("ca/political_credit_column_1_line_6") is POLITICAL_CREDIT_COLUMN_1_LINE_6
    assert registry.get("ca/political_credit_column_1_line_7") is POLITICAL_CREDIT_COLUMN_1_LINE_7
    assert registry.get("ca/political_credit_column_2_line_2") is POLITICAL_CREDIT_COLUMN_2_LINE_2
    assert registry.get("ca/political_credit_column_2_line_3") is POLITICAL_CREDIT_COLUMN_2_LINE_3
    assert registry.get("ca/political_credit_column_2_line_5") is POLITICAL_CREDIT_COLUMN_2_LINE_5
    assert registry.get("ca/political_credit_column_2_line_6") is POLITICAL_CREDIT_COLUMN_2_LINE_6
    assert registry.get("ca/political_credit_column_2_line_7") is POLITICAL_CREDIT_COLUMN_2_LINE_7
    assert registry.get("ca/political_credit_column_3_line_2") is POLITICAL_CREDIT_COLUMN_3_LINE_2
    assert registry.get("ca/political_credit_column_3_line_3") is POLITICAL_CREDIT_COLUMN_3_LINE_3
    assert registry.get("ca/political_credit_column_3_line_5") is POLITICAL_CREDIT_COLUMN_3_LINE_5
    assert registry.get("ca/political_credit_column_3_line_6") is POLITICAL_CREDIT_COLUMN_3_LINE_6
    assert registry.get("ca/political_credit_column_3_line_7") is POLITICAL_CREDIT_COLUMN_3_LINE_7
    assert registry.get("ca/political_credit_chosen_column") is POLITICAL_CREDIT_CHOSEN_COLUMN
    assert (
        registry.get("ca/political_credit_shortcut_threshold")
        is POLITICAL_CREDIT_SHORTCUT_THRESHOLD
    )
    assert registry.get("ca/political_credit_shortcut_amount") is POLITICAL_CREDIT_SHORTCUT_AMOUNT
    assert registry.get("ca/political_credit_before_maximum") is POLITICAL_CREDIT_BEFORE_MAXIMUM
    assert registry.get("ca/political_credit") is POLITICAL_CREDIT
    assert (
        registry.get("ca/labour_sponsored_funds_credit_before_maximum")
        is LABOUR_SPONSORED_FUNDS_CREDIT_BEFORE_MAXIMUM
    )
    assert registry.get("ca/labour_sponsored_funds_credit") is LABOUR_SPONSORED_FUNDS_CREDIT
    assert registry.get("ca/credits_against_federal_tax") is CREDITS_AGAINST_FEDERAL_TAX
    assert registry.get("ca/federal_tax_less_credits") is FEDERAL_TAX_LESS_CREDITS


def test_the_credits_against_federal_tax_kinds_are_money() -> None:
    for kind in (
        LABOUR_SPONSORED_FUNDS_NET_COST,
        POLITICAL_CREDIT_COLUMN_1_LINE_2,
        POLITICAL_CREDIT_COLUMN_1_LINE_3,
        POLITICAL_CREDIT_COLUMN_1_LINE_5,
        POLITICAL_CREDIT_COLUMN_1_LINE_6,
        POLITICAL_CREDIT_COLUMN_1_LINE_7,
        POLITICAL_CREDIT_COLUMN_2_LINE_2,
        POLITICAL_CREDIT_COLUMN_2_LINE_3,
        POLITICAL_CREDIT_COLUMN_2_LINE_5,
        POLITICAL_CREDIT_COLUMN_2_LINE_6,
        POLITICAL_CREDIT_COLUMN_2_LINE_7,
        POLITICAL_CREDIT_COLUMN_3_LINE_2,
        POLITICAL_CREDIT_COLUMN_3_LINE_3,
        POLITICAL_CREDIT_COLUMN_3_LINE_5,
        POLITICAL_CREDIT_COLUMN_3_LINE_6,
        POLITICAL_CREDIT_COLUMN_3_LINE_7,
        POLITICAL_CREDIT_CHOSEN_COLUMN,
        POLITICAL_CREDIT_SHORTCUT_THRESHOLD,
        POLITICAL_CREDIT_SHORTCUT_AMOUNT,
        POLITICAL_CREDIT_BEFORE_MAXIMUM,
        POLITICAL_CREDIT,
        LABOUR_SPONSORED_FUNDS_CREDIT_BEFORE_MAXIMUM,
        LABOUR_SPONSORED_FUNDS_CREDIT,
        CREDITS_AGAINST_FEDERAL_TAX,
        FEDERAL_TAX_LESS_CREDITS,
    ):
        assert kind.value_type is Decimal, kind.identifier


# --- Form T2209: the countries of the foreign tax credit ----------------------------------------


def test_the_foreign_non_business_tax_paid_is_a_non_negative_decimal(
    registry: ArtifactRegistry,
) -> None:
    # T2209 line 1 "Non-business income tax paid to a foreign country (1) 43100"; note (1) is
    # the tax paid minus the part deductible under subsection 20(11) or deducted under 20(12).
    assert FOREIGN_NON_BUSINESS_TAX_PAID.identifier == "ca/foreign_non_business_tax_paid"
    assert FOREIGN_NON_BUSINESS_TAX_PAID.value_type is Decimal
    assert FOREIGN_NON_BUSINESS_TAX_PAID.non_negative is True
    assert registry.kind("ca/foreign_non_business_tax_paid") is FOREIGN_NON_BUSINESS_TAX_PAID


def test_the_net_foreign_non_business_income_is_a_non_negative_decimal(
    registry: ArtifactRegistry,
) -> None:
    # T2209 line 2 "Net foreign non-business income (2) 43300".
    assert NET_FOREIGN_NON_BUSINESS_INCOME.identifier == "ca/net_foreign_non_business_income"
    assert NET_FOREIGN_NON_BUSINESS_INCOME.value_type is Decimal
    assert NET_FOREIGN_NON_BUSINESS_INCOME.non_negative is True
    assert registry.kind("ca/net_foreign_non_business_income") is NET_FOREIGN_NON_BUSINESS_INCOME


def test_the_foreign_tax_countries_are_a_record_list_of_lines_43100_and_43300(
    registry: ArtifactRegistry,
) -> None:
    # T2209: "do the applicable calculation ... for each country on a separate sheet"; each
    # record holds one country's two figures.
    assert isinstance(FOREIGN_TAX_COUNTRIES, RecordListKind)
    assert FOREIGN_TAX_COUNTRIES.identifier == "ca/foreign_tax_countries"
    assert FOREIGN_TAX_COUNTRIES.value_type is RecordList
    assert FOREIGN_TAX_COUNTRIES.fields == (
        FOREIGN_NON_BUSINESS_TAX_PAID,
        NET_FOREIGN_NON_BUSINESS_INCOME,
    )
    assert registry.get("ca/foreign_tax_countries") is FOREIGN_TAX_COUNTRIES


def foreign_country_record(**changes: object) -> dict[ArtifactKind[Any], object]:
    names: dict[str, ArtifactKind[Any]] = {
        "tax_paid": FOREIGN_NON_BUSINESS_TAX_PAID,
        "income": NET_FOREIGN_NON_BUSINESS_INCOME,
    }
    record: dict[ArtifactKind[Any], object] = {
        FOREIGN_NON_BUSINESS_TAX_PAID: Decimal("1500"),
        NET_FOREIGN_NON_BUSINESS_INCOME: Decimal("10000"),
    }
    for name, value in changes.items():
        record[names[name]] = value
    return record


def test_the_foreign_tax_countries_hold_each_countrys_figures_in_the_callers_order() -> None:
    rows = RecordList(
        FOREIGN_TAX_COUNTRIES.fields,
        [foreign_country_record(), foreign_country_record(tax_paid=Decimal("100"))],
    )

    assert [record[FOREIGN_NON_BUSINESS_TAX_PAID] for record in rows.records] == [
        Decimal("1500"),
        Decimal("100"),
    ]
    assert rows.records[0][NET_FOREIGN_NON_BUSINESS_INCOME] == Decimal("10000")


def test_the_foreign_tax_countries_may_be_empty() -> None:
    assert RecordList(FOREIGN_TAX_COUNTRIES.fields, []).records == ()


@pytest.mark.parametrize("field", ["tax_paid", "income"])
def test_a_foreign_country_refuses_a_negative_figure(field: str) -> None:
    with pytest.raises(NegativeArtifactError, match="item 1"):
        RecordList(FOREIGN_TAX_COUNTRIES.fields, [foreign_country_record(**{field: Decimal("-1")})])


def test_a_foreign_country_missing_a_figure_is_refused_naming_the_row() -> None:
    record = foreign_country_record()
    del record[NET_FOREIGN_NON_BUSINESS_INCOME]

    with pytest.raises(InvalidRecordError, match="item 1.*net_foreign_non_business_income"):
        RecordList(FOREIGN_TAX_COUNTRIES.fields, [record])


# --- Form T2209: the sheets of the foreign tax credit -------------------------------------------


def test_the_sheet_line_3_is_a_non_negative_decimal(registry: ArtifactRegistry) -> None:
    # T2209 line 3 "Enter whichever is less: the amount from line 1 or line 2."
    assert FOREIGN_TAX_CREDIT_SHEET_LINE_3.identifier == "ca/foreign_tax_credit_sheet_line_3"
    assert FOREIGN_TAX_CREDIT_SHEET_LINE_3.value_type is Decimal
    assert FOREIGN_TAX_CREDIT_SHEET_LINE_3.non_negative is True
    assert registry.kind("ca/foreign_tax_credit_sheet_line_3") is FOREIGN_TAX_CREDIT_SHEET_LINE_3


def test_the_foreign_tax_credit_sheets_are_a_record_list_of_lines_1_2_and_3() -> None:
    assert isinstance(FOREIGN_TAX_CREDIT_SHEETS, RecordListKind)
    assert FOREIGN_TAX_CREDIT_SHEETS.identifier == "ca/foreign_tax_credit_sheets"
    assert FOREIGN_TAX_CREDIT_SHEETS.value_type is RecordList
    assert FOREIGN_TAX_CREDIT_SHEETS.fields == (
        FOREIGN_NON_BUSINESS_TAX_PAID,
        NET_FOREIGN_NON_BUSINESS_INCOME,
        FOREIGN_TAX_CREDIT_SHEET_LINE_3,
    )


def foreign_sheet_record(**changes: object) -> dict[ArtifactKind[Any], object]:
    names = {
        "tax_paid": FOREIGN_NON_BUSINESS_TAX_PAID,
        "income": NET_FOREIGN_NON_BUSINESS_INCOME,
        "line_3": FOREIGN_TAX_CREDIT_SHEET_LINE_3,
    }
    record: dict[ArtifactKind[Any], object] = {
        FOREIGN_NON_BUSINESS_TAX_PAID: Decimal("1500"),
        NET_FOREIGN_NON_BUSINESS_INCOME: Decimal("10000"),
        FOREIGN_TAX_CREDIT_SHEET_LINE_3: Decimal("1400"),
    }
    for name, value in changes.items():
        record[names[name]] = value
    return record


def test_the_foreign_tax_credit_sheets_hold_each_sheet_in_order() -> None:
    rows = RecordList(
        FOREIGN_TAX_CREDIT_SHEETS.fields,
        [foreign_sheet_record(), foreign_sheet_record(line_3=Decimal("100"))],
    )

    assert [record[FOREIGN_TAX_CREDIT_SHEET_LINE_3] for record in rows.records] == [
        Decimal("1400"),
        Decimal("100"),
    ]


def test_the_foreign_tax_credit_sheets_may_be_empty() -> None:
    assert RecordList(FOREIGN_TAX_CREDIT_SHEETS.fields, []).records == ()


def test_a_foreign_tax_credit_sheet_refuses_a_negative_line_3() -> None:
    with pytest.raises(NegativeArtifactError):
        RecordList(FOREIGN_TAX_CREDIT_SHEETS.fields, [foreign_sheet_record(line_3=Decimal("-1"))])
