"""Unit tests for artifacts and values (design.md §2).

An `Artifact[V]` names an artifact by a namespaced identifier and states the type of its values;
a `Value[V]` is one value of it in one computation. `ArtifactCatalog` is the only way an artifact
gets registered. Names are made up; the catalog tests point `ArtifactRegistry.shared` at a fresh
registry with monkeypatch, so the shared registry stays clean.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from decimal import Decimal
from typing import Any, assert_type, cast

import pytest

from app.domain.artifact import Artifact, ArtifactCatalog, ArtifactRegistry, Money, Value
from app.domain.errors import (
    DuplicateRegistrationError,
    InvalidRegistrationError,
    UnknownRegistrationError,
)
from app.domain.registry import Namespace, Registry

D = Decimal
BASE = Artifact("ex/taxable_base", Decimal)
TAX = Artifact("ex/basic_tax", Decimal)


@pytest.fixture
def fresh(monkeypatch: pytest.MonkeyPatch) -> ArtifactRegistry:
    """A fresh registry that catalogs register into for the duration of one test."""
    registry = ArtifactRegistry()
    monkeypatch.setattr(ArtifactRegistry, "shared", classmethod(lambda cls: registry))
    return registry


# --- Artifact -------------------------------------------------------------------------------


def test_an_artifact_has_an_identifier_and_a_value_type() -> None:
    assert BASE.identifier == "ex/taxable_base"
    assert BASE.value_type is Decimal


def test_the_value_type_is_known_statically() -> None:
    assert_type(BASE, Artifact[Decimal])
    assert_type(Artifact("ex/count", int), Artifact[int])


def test_money_is_an_alias_for_decimal_artifacts() -> None:
    money: Money = BASE

    assert_type(money, Artifact[Decimal])


def test_artifacts_are_equal_by_identifier_and_value_type() -> None:
    assert Artifact("ex/taxable_base", Decimal) == BASE
    assert BASE != TAX
    other_type: Artifact[Any] = Artifact("ex/taxable_base", int)
    assert other_type != BASE
    assert len({BASE, Artifact("ex/taxable_base", Decimal)}) == 1


def test_artifacts_are_immutable() -> None:
    with pytest.raises(FrozenInstanceError):
        BASE.identifier = "ex/other"  # type: ignore[misc]


def test_label_is_the_local_part_of_the_identifier() -> None:
    assert BASE.label == "taxable_base"
    assert Artifact("ca-on/basic_tax", Decimal).label == "basic_tax"
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
    with pytest.raises(InvalidRegistrationError, match="invalid artifact identifier"):
        Artifact(identifier, Decimal)


@pytest.mark.parametrize("identifier", ["ex/a", "ca-on/basic_tax", "x1/line_26000", "a-b-c/x2"])
def test_accepts_namespaced_snake_case_identifiers(identifier: str) -> None:
    assert Artifact(identifier, Decimal).identifier == identifier


def test_an_invalid_identifier_fails_like_an_invalid_catalog_declaration(
    fresh: ArtifactRegistry,
) -> None:
    with pytest.raises(InvalidRegistrationError) as direct:
        Artifact("ex/Bad", Decimal)
    with pytest.raises(InvalidRegistrationError) as declared:
        ArtifactCatalog(Namespace("ex")).artifact("Bad", Decimal)

    assert type(direct.value) is type(declared.value)


def test_value_type_must_be_a_type() -> None:
    with pytest.raises(TypeError, match="value_type must be a type"):
        Artifact("ex/a", cast(Any, "Decimal"))


def test_artifact_is_invariant_in_its_value_type() -> None:
    # Covariance would let mypy accept an Artifact[int] where an Artifact[Decimal] is wired.
    (value_type,) = vars(Artifact)["__parameters__"]
    assert not (
        value_type.__covariant__
        or value_type.__contravariant__
        or getattr(value_type, "__infer_variance__", False)
    )


# --- Value ----------------------------------------------------------------------------------


def test_a_value_carries_its_artifact_and_value() -> None:
    value = Value(BASE, D("2.5"))

    assert value.artifact == BASE
    assert value.value == D("2.5")
    assert_type(value, Value[Decimal])


def test_a_value_must_be_of_its_artifacts_value_type() -> None:
    with pytest.raises(TypeError, match="taxable_base must be a Decimal, got float"):
        Value(BASE, cast(Any, 2.5))


def test_values_are_equal_by_artifact_and_value() -> None:
    assert Value(BASE, D(1)) == Value(BASE, D(1))
    assert Value(BASE, D(1)) != Value(BASE, D(2))
    assert Value(BASE, D(1)) != Value(TAX, D(1))
    assert len({Value(BASE, D(1)), Value(BASE, D(1))}) == 1


def test_values_are_immutable() -> None:
    value = Value(BASE, D(1))

    with pytest.raises(FrozenInstanceError):
        value.value = D(2)  # type: ignore[misc]


# --- ArtifactRegistry and ArtifactCatalog ---------------------------------------------------


def test_artifact_registry_is_a_registry() -> None:
    assert issubclass(ArtifactRegistry, Registry)


def test_shared_returns_the_same_instance_every_time() -> None:
    assert ArtifactRegistry.shared() is ArtifactRegistry.shared()
    assert isinstance(ArtifactRegistry.shared(), ArtifactRegistry)


def test_catalog_builds_the_namespaced_artifact(fresh: ArtifactRegistry) -> None:
    artifact = ArtifactCatalog(Namespace("ex")).artifact("taxable_base", Decimal)

    assert_type(artifact, Artifact[Decimal])
    assert artifact == Artifact("ex/taxable_base", Decimal)


def test_catalog_registers_the_artifact_under_its_identifier(fresh: ArtifactRegistry) -> None:
    artifact = ArtifactCatalog(Namespace("ex")).artifact("taxable_base", Decimal)

    assert fresh.get("ex/taxable_base") == artifact
    assert fresh.identifiers() == {"ex/taxable_base"}


def test_identifiers_lists_every_registered_identifier(fresh: ArtifactRegistry) -> None:
    catalog = ArtifactCatalog(Namespace("ex"))
    catalog.artifact("taxable_base", Decimal)
    catalog.artifact("person_count", int)

    identifiers = fresh.identifiers()

    assert_type(identifiers, frozenset[str])
    assert identifiers == frozenset({"ex/taxable_base", "ex/person_count"})


def test_catalog_rejects_a_duplicate_identifier(fresh: ArtifactRegistry) -> None:
    ArtifactCatalog(Namespace("ex")).artifact("taxable_base", Decimal)

    with pytest.raises(DuplicateRegistrationError, match="'ex/taxable_base'"):
        ArtifactCatalog(Namespace("ex")).artifact("taxable_base", int)


def test_the_same_local_id_may_appear_in_different_namespaces(fresh: ArtifactRegistry) -> None:
    ArtifactCatalog(Namespace("ex")).artifact("basic_tax", Decimal)
    ArtifactCatalog(Namespace("ex-sub")).artifact("basic_tax", Decimal)

    assert fresh.identifiers() == {"ex/basic_tax", "ex-sub/basic_tax"}


@pytest.mark.parametrize("local_id", ["", "TaxableBase", "taxable-base", "ex/taxable_base"])
def test_catalog_rejects_a_local_id_that_is_not_snake_case(
    fresh: ArtifactRegistry, local_id: str
) -> None:
    with pytest.raises(InvalidRegistrationError, match="invalid local id"):
        ArtifactCatalog(Namespace("ex")).artifact(local_id, Decimal)

    assert fresh.identifiers() == frozenset()


def test_a_directly_built_artifact_is_not_registered(fresh: ArtifactRegistry) -> None:
    Artifact("ex/taxable_base", Decimal)

    with pytest.raises(UnknownRegistrationError):
        fresh.get("ex/taxable_base")
    assert fresh.identifiers() == frozenset()
