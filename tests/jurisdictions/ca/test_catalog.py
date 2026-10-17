"""Snapshot of the `ca/` artifact kind identifiers, as the application registers them.

Identifiers are stored with results and exposed by the API, so changing or removing one is a
breaking change: update this snapshot only on purpose. Each package snapshots its own namespace;
declaring a kind in this package's catalog adds it here. The kinds are registered explicitly,
as the composition root does, into a fresh registry.
"""

from __future__ import annotations

from decimal import Decimal

import pytest

import app.jurisdictions.ca
import app.jurisdictions.ca.catalog
from app.domain.artifact import ArtifactCatalog, ArtifactKind, ArtifactRegistry
from app.jurisdictions.ca.catalog import CATALOG, FEDERAL_BASIC_TAX, TAXABLE_INCOME
from app.registrations import JURISDICTIONS

REGISTERED = frozenset(
    {"ca/taxable_income", "ca/federal_basic_tax", "ca/federal_tax_after_credits"}
)


@pytest.fixture
def registry() -> ArtifactRegistry:
    registry = ArtifactRegistry()
    JURISDICTIONS.register(registry)
    return registry


def test_registered_identifiers_snapshot(registry: ArtifactRegistry) -> None:
    identifiers = registry.identifiers()

    assert {i for i in identifiers if i.startswith("ca/")} == REGISTERED


def test_the_package_exposes_its_catalog() -> None:
    assert isinstance(app.jurisdictions.ca.catalog.CATALOG, ArtifactCatalog)
    assert app.jurisdictions.ca.catalog.CATALOG is CATALOG
    assert {kind.identifier for kind in CATALOG.kinds} == REGISTERED


def test_catalog_kinds_are_the_registered_ones(registry: ArtifactRegistry) -> None:
    assert registry.get("ca/taxable_income") is TAXABLE_INCOME
    assert registry.get("ca/federal_basic_tax") is FEDERAL_BASIC_TAX


def test_catalog_kinds_are_in_the_package_namespace() -> None:
    for kind in CATALOG.kinds:
        assert kind.identifier.startswith(f"{app.jurisdictions.ca.NAMESPACE}/")


def test_catalog_kinds_are_money() -> None:
    assert TAXABLE_INCOME.value_type is Decimal
    assert FEDERAL_BASIC_TAX.value_type is Decimal


def test_every_registered_kind_is_money(registry: ArtifactRegistry) -> None:
    for identifier in REGISTERED:
        kind = registry.get(identifier)
        assert isinstance(kind, ArtifactKind)
        assert kind.value_type is Decimal, identifier
