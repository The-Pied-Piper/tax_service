"""Unit tests for artifact kinds and artifacts (design.md §2).

An `ArtifactKind[V]` names a kind of artifact by a namespaced identifier and states the type of
its values; an `Artifact[V]` is one value of a kind in one computation. `ArtifactCatalog` is the
only way a kind gets registered. Names are made up; the catalog tests point
`ArtifactRegistry.shared` at a fresh registry with monkeypatch, so the shared registry stays clean.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from decimal import Decimal
from typing import Any, assert_type, cast

import pytest

from app.domain.artifact import Artifact, ArtifactCatalog, ArtifactKind, ArtifactRegistry, Money
from app.domain.errors import (
    DuplicateRegistrationError,
    InvalidRegistrationError,
    UnknownRegistrationError,
)
from app.domain.registry import Namespace, Registry

D = Decimal
BASE = ArtifactKind("ex/taxable_base", Decimal)
TAX = ArtifactKind("ex/basic_tax", Decimal)


@pytest.fixture
def fresh(monkeypatch: pytest.MonkeyPatch) -> ArtifactRegistry:
    """A fresh registry that catalogs register into for the duration of one test."""
    registry = ArtifactRegistry()
    monkeypatch.setattr(ArtifactRegistry, "shared", classmethod(lambda cls: registry))
    return registry


# --- ArtifactKind ---------------------------------------------------------------------------


def test_an_artifact_kind_has_an_identifier_and_a_value_type() -> None:
    assert BASE.identifier == "ex/taxable_base"
    assert BASE.value_type is Decimal


def test_the_value_type_is_known_statically() -> None:
    assert_type(BASE, ArtifactKind[Decimal])
    assert_type(ArtifactKind("ex/count", int), ArtifactKind[int])


def test_money_is_an_alias_for_decimal_artifact_kinds() -> None:
    money: Money = BASE

    assert_type(money, ArtifactKind[Decimal])


def test_artifact_kinds_are_equal_by_identifier_and_value_type() -> None:
    assert ArtifactKind("ex/taxable_base", Decimal) == BASE
    assert BASE != TAX
    other_type: ArtifactKind[Any] = ArtifactKind("ex/taxable_base", int)
    assert other_type != BASE
    assert len({BASE, ArtifactKind("ex/taxable_base", Decimal)}) == 1


def test_artifact_kinds_are_immutable() -> None:
    with pytest.raises(FrozenInstanceError):
        BASE.identifier = "ex/other"  # type: ignore[misc]


def test_label_is_the_local_part_of_the_identifier() -> None:
    assert BASE.label == "taxable_base"
    assert ArtifactKind("ca-on/basic_tax", Decimal).label == "basic_tax"
    assert_type(BASE.label, str)


@pytest.mark.parametrize(
    "identifier",
    [
        "",
        "taxable_base",  # no namespace
        "/taxable_base",
        "ex/",
        "Ex/taxable_base",
        "ex-/taxable_base",
        "e--x/taxable_base",
        "e_x/taxable_base",
        "ex/TaxableBase",
        "ex/taxable-base",
        "ex/_taxable",
        "ex/2x",
        "ex/a/b",
        " ex/a",
    ],
)
def test_rejects_an_identifier_not_namespace_slash_snake_case(identifier: str) -> None:
    with pytest.raises(InvalidRegistrationError, match="invalid artifact kind identifier"):
        ArtifactKind(identifier, Decimal)


@pytest.mark.parametrize("identifier", ["ex/a", "ca-on/basic_tax", "x1/line_26000", "a-b-c/x2"])
def test_accepts_namespaced_snake_case_identifiers(identifier: str) -> None:
    assert ArtifactKind(identifier, Decimal).identifier == identifier


def test_an_invalid_identifier_fails_like_an_invalid_catalog_declaration(
    fresh: ArtifactRegistry,
) -> None:
    with pytest.raises(InvalidRegistrationError) as direct:
        ArtifactKind("ex/Bad", Decimal)
    with pytest.raises(InvalidRegistrationError) as declared:
        ArtifactCatalog(Namespace("ex")).declare("Bad", Decimal)

    assert type(direct.value) is type(declared.value)


def test_value_type_must_be_a_type() -> None:
    with pytest.raises(TypeError, match="value_type must be a type"):
        ArtifactKind("ex/a", cast(Any, "Decimal"))


def test_an_artifact_kind_is_invariant_in_its_value_type() -> None:
    # Covariance would let mypy accept an ArtifactKind[int] wired where an
    # ArtifactKind[Decimal] is expected.
    (value_type,) = vars(ArtifactKind)["__parameters__"]
    assert not (
        value_type.__covariant__
        or value_type.__contravariant__
        or getattr(value_type, "__infer_variance__", False)
    )


# --- Artifact -------------------------------------------------------------------------------


def test_an_artifact_carries_its_kind_and_value() -> None:
    artifact = Artifact(kind=BASE, value=D("2.5"))

    assert artifact.kind == BASE
    assert artifact.value == D("2.5")
    assert_type(artifact, Artifact[Decimal])


def test_an_artifact_value_must_be_of_its_kinds_value_type() -> None:
    with pytest.raises(TypeError, match="taxable_base must be a Decimal, got float"):
        Artifact(BASE, cast(Any, 2.5))


def test_artifacts_are_equal_by_kind_and_value() -> None:
    assert Artifact(BASE, D(1)) == Artifact(BASE, D(1))
    assert Artifact(BASE, D(1)) != Artifact(BASE, D(2))
    assert Artifact(BASE, D(1)) != Artifact(TAX, D(1))
    assert len({Artifact(BASE, D(1)), Artifact(BASE, D(1))}) == 1


def test_artifacts_are_immutable() -> None:
    artifact = Artifact(BASE, D(1))

    with pytest.raises(FrozenInstanceError):
        artifact.value = D(2)  # type: ignore[misc]


# --- ArtifactRegistry and ArtifactCatalog ---------------------------------------------------


def test_artifact_registry_is_a_registry() -> None:
    assert issubclass(ArtifactRegistry, Registry)


def test_shared_returns_the_same_instance_every_time() -> None:
    assert ArtifactRegistry.shared() is ArtifactRegistry.shared()
    assert isinstance(ArtifactRegistry.shared(), ArtifactRegistry)


def test_catalog_declares_the_namespaced_kind(fresh: ArtifactRegistry) -> None:
    kind = ArtifactCatalog(Namespace("ex")).declare("taxable_base", Decimal)

    assert_type(kind, ArtifactKind[Decimal])
    assert kind == ArtifactKind("ex/taxable_base", Decimal)


def test_catalog_registers_the_kind_under_its_identifier(fresh: ArtifactRegistry) -> None:
    kind = ArtifactCatalog(Namespace("ex")).declare("taxable_base", Decimal)

    assert fresh.get("ex/taxable_base") == kind
    assert fresh.identifiers() == {"ex/taxable_base"}


def test_identifiers_lists_every_registered_identifier(fresh: ArtifactRegistry) -> None:
    catalog = ArtifactCatalog(Namespace("ex"))
    catalog.declare("taxable_base", Decimal)
    catalog.declare("person_count", int)

    identifiers = fresh.identifiers()

    assert_type(identifiers, frozenset[str])
    assert identifiers == frozenset({"ex/taxable_base", "ex/person_count"})


def test_catalog_rejects_a_duplicate_identifier(fresh: ArtifactRegistry) -> None:
    ArtifactCatalog(Namespace("ex")).declare("taxable_base", Decimal)

    with pytest.raises(DuplicateRegistrationError, match="'ex/taxable_base'"):
        ArtifactCatalog(Namespace("ex")).declare("taxable_base", int)


def test_the_same_local_id_may_appear_in_different_namespaces(fresh: ArtifactRegistry) -> None:
    ArtifactCatalog(Namespace("ex")).declare("basic_tax", Decimal)
    ArtifactCatalog(Namespace("ex-sub")).declare("basic_tax", Decimal)

    assert fresh.identifiers() == {"ex/basic_tax", "ex-sub/basic_tax"}


@pytest.mark.parametrize("local_id", ["", "TaxableBase", "taxable-base", "ex/taxable_base"])
def test_catalog_rejects_a_local_id_that_is_not_snake_case(
    fresh: ArtifactRegistry, local_id: str
) -> None:
    with pytest.raises(InvalidRegistrationError, match="invalid local id"):
        ArtifactCatalog(Namespace("ex")).declare(local_id, Decimal)

    assert fresh.identifiers() == frozenset()


def test_a_directly_built_artifact_kind_is_not_registered(fresh: ArtifactRegistry) -> None:
    ArtifactKind("ex/taxable_base", Decimal)

    with pytest.raises(UnknownRegistrationError):
        fresh.get("ex/taxable_base")
    assert fresh.identifiers() == frozenset()
