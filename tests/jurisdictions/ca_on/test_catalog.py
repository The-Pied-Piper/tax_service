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
    DEPENDANTS,
    DEPENDENT_CHILDREN,
    NON_REFUNDABLE_CREDIT_AMOUNTS,
    NON_REFUNDABLE_TAX_CREDITS,
    ONTARIO_BASIC_TAX,
    ONTARIO_HEALTH_PREMIUM,
    ONTARIO_SURTAX,
    ONTARIO_TAX,
    ONTARIO_TAX_AFTER_CREDITS,
    ONTARIO_TAX_AFTER_REDUCTION,
    ONTARIO_TAX_REDUCTION,
    ONTARIO_TAX_WITH_SURTAX,
    TAX_REDUCTION_AMOUNTS,
    TAX_REDUCTION_BASIC,
    TAX_REDUCTION_FOR_CHILDREN,
    TAX_REDUCTION_FOR_DEPENDANTS,
)
from app.registrations import JURISDICTIONS

REGISTERED = frozenset(
    {
        "ca-on/ontario_basic_tax",
        "ca-on/basic_personal_amount",
        "ca-on/non_refundable_credit_amounts",
        "ca-on/non_refundable_tax_credits",
        "ca-on/ontario_tax_after_credits",
        "ca-on/ontario_surtax",
        "ca-on/ontario_tax_with_surtax",
        "ca-on/tax_reduction_basic",
        "ca-on/dependent_children",
        "ca-on/tax_reduction_for_children",
        "ca-on/dependants",
        "ca-on/tax_reduction_for_dependants",
        "ca-on/tax_reduction_amounts",
        "ca-on/ontario_tax_reduction",
        "ca-on/ontario_tax_after_reduction",
        "ca-on/ontario_health_premium",
        "ca-on/ontario_tax",
    }
)
# ON428 lines 75 (line 60969) and 76 (line 60970): the numbers of dependent children and of
# dependants, counted, not money.
COUNTS = frozenset({"ca-on/dependent_children", "ca-on/dependants"})


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
    assert registry.get("ca-on/non_refundable_tax_credits") is NON_REFUNDABLE_TAX_CREDITS
    assert registry.get("ca-on/ontario_surtax") is ONTARIO_SURTAX
    assert registry.get("ca-on/ontario_tax_with_surtax") is ONTARIO_TAX_WITH_SURTAX
    assert registry.get("ca-on/tax_reduction_basic") is TAX_REDUCTION_BASIC
    assert registry.get("ca-on/dependent_children") is DEPENDENT_CHILDREN
    assert registry.get("ca-on/tax_reduction_for_children") is TAX_REDUCTION_FOR_CHILDREN
    assert registry.get("ca-on/dependants") is DEPENDANTS
    assert registry.get("ca-on/tax_reduction_for_dependants") is TAX_REDUCTION_FOR_DEPENDANTS
    assert registry.get("ca-on/tax_reduction_amounts") is TAX_REDUCTION_AMOUNTS
    assert registry.get("ca-on/ontario_tax_reduction") is ONTARIO_TAX_REDUCTION
    assert registry.get("ca-on/ontario_tax_after_reduction") is ONTARIO_TAX_AFTER_REDUCTION
    assert registry.get("ca-on/ontario_health_premium") is ONTARIO_HEALTH_PREMIUM
    assert registry.get("ca-on/ontario_tax") is ONTARIO_TAX


def test_every_registered_kind_but_the_counts_is_money_in_the_package_namespace(
    registry: ArtifactRegistry,
) -> None:
    for identifier in REGISTERED - COUNTS:
        kind = registry.get(identifier)
        assert isinstance(kind, ArtifactKind)
        assert kind.identifier.startswith(f"{app.jurisdictions.ca_on.NAMESPACE}/")
        assert kind.value_type is Decimal, identifier


def test_the_counts_are_int_kinds_in_the_package_namespace(registry: ArtifactRegistry) -> None:
    assert COUNTS <= REGISTERED
    for identifier in COUNTS:
        kind = registry.get(identifier)
        assert isinstance(kind, ArtifactKind)
        assert kind.identifier.startswith(f"{app.jurisdictions.ca_on.NAMESPACE}/")
        assert kind.value_type is int, identifier


def test_every_kind_is_declared_non_negative(registry: ArtifactRegistry) -> None:
    for kind in CATALOG.kinds:
        assert kind.non_negative is True, kind.identifier
    for identifier in REGISTERED:
        assert registry.kind(identifier).non_negative is True, identifier
