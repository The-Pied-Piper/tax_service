"""Snapshot of the registered artifact identifiers.

Identifiers are stored with results and exposed by the API, so changing or removing one is a
breaking change: update this snapshot only on purpose. Adding an artifact adds it here.
"""

from __future__ import annotations

from decimal import Decimal

from app.domain.artifact import ArtifactRegistry
from tests.pilot.ca_on.catalog import FEDERAL_BASIC_TAX, TAXABLE_INCOME

REGISTERED = frozenset({"ca/taxable_income", "ca/federal_basic_tax"})


def test_registered_identifiers_snapshot() -> None:
    assert ArtifactRegistry.shared().identifiers() == REGISTERED


def test_catalog_artifacts_are_the_registered_ones() -> None:
    registry = ArtifactRegistry.shared()

    assert registry.get("ca/taxable_income") == TAXABLE_INCOME
    assert registry.get("ca/federal_basic_tax") == FEDERAL_BASIC_TAX


def test_catalog_artifacts_are_money() -> None:
    assert TAXABLE_INCOME.value_type is Decimal
    assert FEDERAL_BASIC_TAX.value_type is Decimal
