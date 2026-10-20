"""Registered and money kinds of the federal catalog family `credits_against_federal_tax`."""

from __future__ import annotations

from decimal import Decimal

from app.domain.artifact import ArtifactRegistry
from app.jurisdictions.ca.catalog import (
    CREDITS_AGAINST_FEDERAL_TAX,
    FEDERAL_TAX_LESS_CREDITS,
    LABOUR_SPONSORED_FUNDS_CREDIT,
    LABOUR_SPONSORED_FUNDS_CREDIT_BEFORE_MAXIMUM,
    LABOUR_SPONSORED_FUNDS_NET_COST,
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
