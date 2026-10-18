"""Snapshot of the `ca-on/` artifact kind identifiers, as the application registers them.

Identifiers are stored with results and exposed by the API, so changing or removing one is a
breaking change: update this snapshot only on purpose. Declaring a kind in this package's catalog
adds it here; federal kinds are snapshotted in `tests/jurisdictions/ca/`. The kinds are
registered explicitly, as the composition root does, into a fresh registry.
"""

from __future__ import annotations

from decimal import Decimal

import pytest

import app.jurisdictions.ca_on
import app.jurisdictions.ca_on.catalog
from app.domain.artifact import ArtifactCatalog, ArtifactKind, ArtifactRegistry
from app.jurisdictions.ca_on.catalog import (
    BASIC_PERSONAL_AMOUNT,
    CATALOG,
    NON_REFUNDABLE_CREDIT_AMOUNTS,
    ONTARIO_BASIC_TAX,
    ONTARIO_TAX_AFTER_CREDITS,
)
from app.registrations import JURISDICTIONS

REGISTERED = frozenset(
    {
        "ca-on/ontario_basic_tax",
        "ca-on/basic_personal_amount",
        "ca-on/non_refundable_credit_amounts",
        "ca-on/ontario_tax_after_credits",
    }
)


@pytest.fixture
def registry() -> ArtifactRegistry:
    registry = ArtifactRegistry()
    JURISDICTIONS.register(registry)
    return registry


def test_registered_identifiers_snapshot(registry: ArtifactRegistry) -> None:
    identifiers = registry.identifiers()

    assert {i for i in identifiers if i.startswith("ca-on/")} == REGISTERED


def test_the_package_exposes_its_catalog() -> None:
    assert isinstance(app.jurisdictions.ca_on.catalog.CATALOG, ArtifactCatalog)
    assert app.jurisdictions.ca_on.catalog.CATALOG is CATALOG
    assert {kind.identifier for kind in CATALOG.kinds} == REGISTERED


def test_catalog_kinds_are_the_registered_ones(registry: ArtifactRegistry) -> None:
    assert registry.get("ca-on/ontario_basic_tax") is ONTARIO_BASIC_TAX
    assert registry.get("ca-on/ontario_tax_after_credits") is ONTARIO_TAX_AFTER_CREDITS
    assert registry.get("ca-on/basic_personal_amount") is BASIC_PERSONAL_AMOUNT
    assert registry.get("ca-on/non_refundable_credit_amounts") is NON_REFUNDABLE_CREDIT_AMOUNTS


def test_every_registered_kind_is_money_in_the_package_namespace(
    registry: ArtifactRegistry,
) -> None:
    for identifier in REGISTERED:
        kind = registry.get(identifier)
        assert isinstance(kind, ArtifactKind)
        assert kind.identifier.startswith(f"{app.jurisdictions.ca_on.NAMESPACE}/")
        assert kind.value_type is Decimal, identifier
