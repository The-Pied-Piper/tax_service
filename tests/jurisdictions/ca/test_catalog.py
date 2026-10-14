"""Snapshot of the registered `ca/` artifact kind identifiers, as the application registers them.

Identifiers are stored with results and exposed by the API, so changing or removing one is a
breaking change: update this snapshot only on purpose. Each package snapshots its own namespace;
declaring a kind in this package's catalog adds it here.
"""

from __future__ import annotations

from decimal import Decimal

import app.jurisdictions.ca
import app.registrations  # noqa: F401  (fills the shared registries, as the app does)
from app.domain.artifact import ArtifactRegistry
from app.jurisdictions.ca.catalog import FEDERAL_BASIC_TAX, TAXABLE_INCOME

REGISTERED = frozenset({"ca/taxable_income", "ca/federal_basic_tax"})


def test_registered_identifiers_snapshot() -> None:
    identifiers = ArtifactRegistry.shared().identifiers()

    assert {i for i in identifiers if i.startswith("ca/")} == REGISTERED


def test_catalog_kinds_are_the_registered_ones() -> None:
    registry = ArtifactRegistry.shared()

    assert registry.get("ca/taxable_income") is TAXABLE_INCOME
    assert registry.get("ca/federal_basic_tax") is FEDERAL_BASIC_TAX


def test_catalog_kinds_are_in_the_package_namespace() -> None:
    for kind in (TAXABLE_INCOME, FEDERAL_BASIC_TAX):
        assert kind.identifier.startswith(f"{app.jurisdictions.ca.NAMESPACE}/")


def test_catalog_kinds_are_money() -> None:
    assert TAXABLE_INCOME.value_type is Decimal
    assert FEDERAL_BASIC_TAX.value_type is Decimal
