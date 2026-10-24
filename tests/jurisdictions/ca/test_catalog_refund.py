"""Registered and money kinds of the federal catalog family `refund`."""

from __future__ import annotations

from decimal import Decimal

from app.domain.artifact import ArtifactRegistry
from app.jurisdictions.ca.catalog import (
    EI_OVERPAYMENT,
    REFUND,
    REFUND_OR_BALANCE_OWING,
    T2204_EXEMPTION,
    T2204_INSURABLE_EARNINGS,
    T2204_LINE_1,
    T2204_LINE_1_COUNT,
    T2204_LINE_1_PLUS_2,
    T2204_LINE_3,
    T2204_LINE_6,
    T2204_LINE_7,
    T2204_LINE_8,
    T2204_LINE_9,
    T2204_LINE_10,
    T2204_LINE_12,
    T2204_LINE_13,
    T2204_LINE_14,
    T2204_LINE_15,
    T2204_LINE_15_COUNT,
    T2204_LINE_16,
    T2204_PREMIUMS_DEDUCTED,
    T2204_SELF_EMPLOYMENT_EARNINGS,
    TOTAL_CREDITS,
)

T2204_MONEY = (
    T2204_INSURABLE_EARNINGS,
    T2204_SELF_EMPLOYMENT_EARNINGS,
    T2204_PREMIUMS_DEDUCTED,
    T2204_LINE_1,
    T2204_LINE_1_PLUS_2,
    T2204_LINE_3,
    T2204_EXEMPTION,
    T2204_LINE_6,
    T2204_LINE_7,
    T2204_LINE_8,
    T2204_LINE_9,
    T2204_LINE_10,
    T2204_LINE_12,
    T2204_LINE_13,
    T2204_LINE_14,
    T2204_LINE_15,
    T2204_LINE_16,
    EI_OVERPAYMENT,
)
T2204_COUNTS = (T2204_LINE_1_COUNT, T2204_LINE_15_COUNT)


def test_the_refund_kinds_are_the_registered_ones(registry: ArtifactRegistry) -> None:
    assert registry.get("ca/total_credits") is TOTAL_CREDITS
    assert registry.get("ca/refund_or_balance_owing") is REFUND_OR_BALANCE_OWING
    assert registry.get("ca/refund") is REFUND


def test_the_refund_kinds_are_money() -> None:
    for kind in (
        TOTAL_CREDITS,
        REFUND_OR_BALANCE_OWING,
        REFUND,
    ):
        assert kind.value_type is Decimal, kind.identifier


def test_the_t2204_kinds_are_the_registered_ones(registry: ArtifactRegistry) -> None:
    # T2204 (Employee Overpayment of Employment Insurance Premiums): the caller's three inputs,
    # the lines 1 to 16 that are computed, and the overpayment on T1 line 45000.
    for kind in T2204_MONEY + T2204_COUNTS:
        assert registry.get(kind.identifier) is kind, kind.identifier


def test_the_t2204_kinds_are_money() -> None:
    for kind in T2204_MONEY:
        assert kind.value_type is Decimal, kind.identifier


def test_the_t2204_counts_are_int_kinds() -> None:
    # The count of note (1) and the count of line 45000, each 0 or 1.
    for kind in T2204_COUNTS:
        assert kind.value_type is int, kind.identifier
