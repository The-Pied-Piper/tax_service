"""Registered and money kinds of the federal catalog family `net_tax`."""

from __future__ import annotations

from decimal import Decimal

from app.domain.artifact import ArtifactRegistry
from app.jurisdictions.ca.catalog import (
    INCOME_TAX_DEDUCTED,
    NET_FEDERAL_TAX,
    SPECIAL_TAXES,
    TOTAL_PAYABLE,
)


def test_the_net_tax_kinds_are_the_registered_ones(registry: ArtifactRegistry) -> None:
    assert registry.get("ca/special_taxes") is SPECIAL_TAXES
    assert registry.get("ca/net_federal_tax") is NET_FEDERAL_TAX
    assert registry.get("ca/total_payable") is TOTAL_PAYABLE
    assert registry.get("ca/income_tax_deducted") is INCOME_TAX_DEDUCTED


def test_the_net_tax_kinds_are_money() -> None:
    for kind in (
        SPECIAL_TAXES,
        NET_FEDERAL_TAX,
        TOTAL_PAYABLE,
        INCOME_TAX_DEDUCTED,
    ):
        assert kind.value_type is Decimal, kind.identifier
