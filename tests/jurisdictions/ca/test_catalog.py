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
from app.jurisdictions.ca.catalog import (
    BASIC_PERSONAL_AMOUNT,
    CAPITAL_GAIN,
    CATALOG,
    CPP_BASE_CONTRIBUTIONS,
    CPP_ENHANCED_CONTRIBUTIONS,
    DEDUCTIONS_FROM_NET_INCOME,
    DEDUCTIONS_FROM_TOTAL_INCOME,
    EI_PREMIUMS,
    EMPLOYMENT_INCOME,
    FEDERAL_BASIC_TAX,
    NET_INCOME,
    NON_REFUNDABLE_CREDIT_AMOUNTS,
    RRSP_DEDUCTION,
    TAXABLE_CAPITAL_GAINS,
    TAXABLE_INCOME,
    TOTAL_INCOME,
    UNION_DUES,
)
from app.registrations import JURISDICTIONS

REGISTERED = frozenset(
    {
        "ca/employment_income",
        "ca/capital_gain",
        "ca/taxable_capital_gains",
        "ca/total_income",
        "ca/rrsp_deduction",
        "ca/union_dues",
        "ca/cpp_enhanced_contributions",
        "ca/deductions_from_total_income",
        "ca/net_income",
        "ca/deductions_from_net_income",
        "ca/taxable_income",
        "ca/federal_basic_tax",
        "ca/basic_personal_amount",
        "ca/cpp_base_contributions",
        "ca/ei_premiums",
        "ca/non_refundable_credit_amounts",
        "ca/federal_tax_after_credits",
    }
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
    assert registry.get("ca/employment_income") is EMPLOYMENT_INCOME
    assert registry.get("ca/capital_gain") is CAPITAL_GAIN
    assert registry.get("ca/taxable_capital_gains") is TAXABLE_CAPITAL_GAINS
    assert registry.get("ca/total_income") is TOTAL_INCOME
    assert registry.get("ca/rrsp_deduction") is RRSP_DEDUCTION
    assert registry.get("ca/union_dues") is UNION_DUES
    assert registry.get("ca/deductions_from_total_income") is DEDUCTIONS_FROM_TOTAL_INCOME
    assert registry.get("ca/net_income") is NET_INCOME
    assert registry.get("ca/deductions_from_net_income") is DEDUCTIONS_FROM_NET_INCOME
    assert registry.get("ca/basic_personal_amount") is BASIC_PERSONAL_AMOUNT
    assert registry.get("ca/non_refundable_credit_amounts") is NON_REFUNDABLE_CREDIT_AMOUNTS
    assert registry.get("ca/cpp_base_contributions") is CPP_BASE_CONTRIBUTIONS
    assert registry.get("ca/cpp_enhanced_contributions") is CPP_ENHANCED_CONTRIBUTIONS
    assert registry.get("ca/ei_premiums") is EI_PREMIUMS


def test_catalog_kinds_are_in_the_package_namespace() -> None:
    for kind in CATALOG.kinds:
        assert kind.identifier.startswith(f"{app.jurisdictions.ca.NAMESPACE}/")


def test_catalog_kinds_are_money() -> None:
    assert TAXABLE_INCOME.value_type is Decimal
    assert FEDERAL_BASIC_TAX.value_type is Decimal
    for kind in (
        EMPLOYMENT_INCOME,
        CAPITAL_GAIN,
        TAXABLE_CAPITAL_GAINS,
        TOTAL_INCOME,
        RRSP_DEDUCTION,
        UNION_DUES,
        DEDUCTIONS_FROM_TOTAL_INCOME,
        NET_INCOME,
        DEDUCTIONS_FROM_NET_INCOME,
        BASIC_PERSONAL_AMOUNT,
        NON_REFUNDABLE_CREDIT_AMOUNTS,
        CPP_BASE_CONTRIBUTIONS,
        CPP_ENHANCED_CONTRIBUTIONS,
        EI_PREMIUMS,
    ):
        assert kind.value_type is Decimal, kind.identifier


def test_every_registered_kind_is_money(registry: ArtifactRegistry) -> None:
    for identifier in REGISTERED:
        kind = registry.get(identifier)
        assert isinstance(kind, ArtifactKind)
        assert kind.value_type is Decimal, identifier
