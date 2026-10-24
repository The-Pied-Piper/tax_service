"""Registered and money kinds of the federal catalog family `net_tax`."""

from __future__ import annotations

from decimal import Decimal

from app.domain.artifact import ArtifactRegistry
from app.jurisdictions.ca.catalog import (
    CPP_PAYABLE_ON_SELF_EMPLOYMENT,
    EI_PAYABLE_ON_SELF_EMPLOYMENT,
    INCOME_TAX_DEDUCTED,
    NET_FEDERAL_TAX,
    SOCIAL_BENEFITS_REPAYMENT_PAYABLE,
    SPECIAL_TAXES,
    SPLIT_INCOME_LINE_10,
    SPLIT_INCOME_LINE_13,
    SPLIT_INCOME_LINE_14,
    SPLIT_INCOME_LINE_15,
    SPLIT_INCOME_LINE_18,
    SPLIT_INCOME_LINE_19,
    SPLIT_INCOME_LINE_20,
    SPLIT_INCOME_LINE_21,
    SPLIT_INCOME_LINE_22,
    SPLIT_INCOME_LINE_23,
    SPLIT_INCOME_LINE_24,
    SPLIT_INCOME_LINE_29,
    SPLIT_INCOME_LINE_30,
    TOTAL_PAYABLE,
)
from tests.jurisdictions.ca.catalog_snapshot import SIGNED


def test_the_net_tax_kinds_are_the_registered_ones(registry: ArtifactRegistry) -> None:
    assert registry.get("ca/special_taxes") is SPECIAL_TAXES
    assert registry.get("ca/net_federal_tax") is NET_FEDERAL_TAX
    assert registry.get("ca/cpp_payable_on_self_employment") is CPP_PAYABLE_ON_SELF_EMPLOYMENT
    assert registry.get("ca/ei_payable_on_self_employment") is EI_PAYABLE_ON_SELF_EMPLOYMENT
    assert registry.get("ca/social_benefits_repayment_payable") is SOCIAL_BENEFITS_REPAYMENT_PAYABLE
    assert registry.get("ca/total_payable") is TOTAL_PAYABLE
    assert registry.get("ca/income_tax_deducted") is INCOME_TAX_DEDUCTED
    assert registry.get("ca/split_income_line_10") is SPLIT_INCOME_LINE_10
    assert registry.get("ca/split_income_line_13") is SPLIT_INCOME_LINE_13
    assert registry.get("ca/split_income_line_14") is SPLIT_INCOME_LINE_14
    assert registry.get("ca/split_income_line_15") is SPLIT_INCOME_LINE_15
    assert registry.get("ca/split_income_line_18") is SPLIT_INCOME_LINE_18
    assert registry.get("ca/split_income_line_19") is SPLIT_INCOME_LINE_19
    assert registry.get("ca/split_income_line_20") is SPLIT_INCOME_LINE_20
    assert registry.get("ca/split_income_line_21") is SPLIT_INCOME_LINE_21
    assert registry.get("ca/split_income_line_22") is SPLIT_INCOME_LINE_22
    assert registry.get("ca/split_income_line_23") is SPLIT_INCOME_LINE_23
    assert registry.get("ca/split_income_line_24") is SPLIT_INCOME_LINE_24
    assert registry.get("ca/split_income_line_29") is SPLIT_INCOME_LINE_29
    assert registry.get("ca/split_income_line_30") is SPLIT_INCOME_LINE_30


def test_the_net_tax_kinds_are_money() -> None:
    for kind in (
        SPECIAL_TAXES,
        NET_FEDERAL_TAX,
        CPP_PAYABLE_ON_SELF_EMPLOYMENT,
        EI_PAYABLE_ON_SELF_EMPLOYMENT,
        SOCIAL_BENEFITS_REPAYMENT_PAYABLE,
        TOTAL_PAYABLE,
        INCOME_TAX_DEDUCTED,
        SPLIT_INCOME_LINE_10,
        SPLIT_INCOME_LINE_13,
        SPLIT_INCOME_LINE_14,
        SPLIT_INCOME_LINE_15,
        SPLIT_INCOME_LINE_18,
        SPLIT_INCOME_LINE_19,
        SPLIT_INCOME_LINE_20,
        SPLIT_INCOME_LINE_21,
        SPLIT_INCOME_LINE_22,
        SPLIT_INCOME_LINE_23,
        SPLIT_INCOME_LINE_24,
        SPLIT_INCOME_LINE_29,
        SPLIT_INCOME_LINE_30,
    ):
        assert kind.value_type is Decimal, kind.identifier


def test_the_t1206_part_2_lines_that_print_no_floor_are_signed(registry: ArtifactRegistry) -> None:
    # Form T1206 Part 2 line 15 "Line 10 minus line 14" and line 22 "Line 15 minus line 21" print no
    # "(if negative, enter "0")", so each is signed; line 24 "Line 22 minus line 23 (if negative,
    # enter "0")" is the floored line, and line 23 multiplies the non-negative federal foreign tax
    # credit by a share.
    for kind in (SPLIT_INCOME_LINE_15, SPLIT_INCOME_LINE_22):
        assert kind.non_negative is False, kind.identifier
        assert registry.kind(kind.identifier) is kind
        assert kind.identifier in SIGNED
    assert SPLIT_INCOME_LINE_23.non_negative is True
    assert SPLIT_INCOME_LINE_24.non_negative is True


def test_the_other_t1206_part_2_lines_are_non_negative(registry: ArtifactRegistry) -> None:
    # Lines 10, 13, 14, 19, 20, 21, 23, 29 and 30 add, take a rate or a share of, or compare
    # non-negative figures, and lines 18 and 24 print "(if negative, enter "0")".
    for kind in (
        SPLIT_INCOME_LINE_10,
        SPLIT_INCOME_LINE_13,
        SPLIT_INCOME_LINE_14,
        SPLIT_INCOME_LINE_18,
        SPLIT_INCOME_LINE_19,
        SPLIT_INCOME_LINE_20,
        SPLIT_INCOME_LINE_21,
        SPLIT_INCOME_LINE_23,
        SPLIT_INCOME_LINE_24,
        SPLIT_INCOME_LINE_29,
        SPLIT_INCOME_LINE_30,
    ):
        assert kind.identifier not in SIGNED, kind.identifier
        assert kind.non_negative is True, kind.identifier
        assert registry.kind(kind.identifier) is kind


def test_the_social_benefits_repayment_payable_is_a_non_negative_decimal(
    registry: ArtifactRegistry,
) -> None:
    # T1 line 146 and line 42200 "Social benefits repayment (amount from line 23500)" carries the
    # non-negative line 23500.
    assert SOCIAL_BENEFITS_REPAYMENT_PAYABLE.value_type is Decimal
    assert SOCIAL_BENEFITS_REPAYMENT_PAYABLE.non_negative is True
    assert registry.kind("ca/social_benefits_repayment_payable").non_negative is True
    assert "ca/social_benefits_repayment_payable" not in SIGNED
