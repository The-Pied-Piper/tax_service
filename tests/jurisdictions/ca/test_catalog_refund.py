"""Registered and money kinds of the federal catalog family `refund`."""

from __future__ import annotations

from decimal import Decimal

from app.domain.artifact import ArtifactRegistry
from app.jurisdictions.ca.catalog import REFUND, REFUND_OR_BALANCE_OWING, TOTAL_CREDITS


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
