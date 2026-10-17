"""Unit tests for artifact kinds and artifacts (design.md §2).

An `ArtifactKind[V]` names a kind of artifact by a namespaced identifier and states the type of
its values; an `Artifact[V]` is one value of a kind in one computation. `ArtifactCatalog` only
records the kinds a package declares; `ArtifactRegistry.register_catalog` registers them. Names are
made up; the catalog tests point `ArtifactRegistry.shared` at a fresh registry with monkeypatch,
so the shared registry stays clean and declaring can be seen to register nothing.
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


def test_declaring_registers_nothing(fresh: ArtifactRegistry) -> None:
    catalog = ArtifactCatalog(Namespace("ex"))
    catalog.declare("taxable_base", Decimal)
    catalog.declare("person_count", int)

    assert fresh.identifiers() == frozenset()
    with pytest.raises(UnknownRegistrationError):
        fresh.get("ex/taxable_base")


def test_catalog_kinds_are_the_declared_kinds_in_declaration_order(fresh: ArtifactRegistry) -> None:
    catalog = ArtifactCatalog(Namespace("ex"))
    base = catalog.declare("taxable_base", Decimal)
    count = catalog.declare("person_count", int)
    tax = catalog.declare("basic_tax", Decimal)

    kinds = catalog.kinds

    assert_type(kinds, tuple[ArtifactKind[Any], ...])
    assert isinstance(kinds, tuple)
    assert len(kinds) == 3
    assert kinds[0] is base
    assert kinds[1] is count
    assert kinds[2] is tax


def test_a_catalog_has_its_namespace() -> None:
    assert ArtifactCatalog(Namespace("ex-on")).namespace == Namespace("ex-on")


def test_a_new_catalog_has_no_kinds(fresh: ArtifactRegistry) -> None:
    assert ArtifactCatalog(Namespace("ex")).kinds == ()


def test_catalog_rejects_a_duplicate_local_id_at_declare(fresh: ArtifactRegistry) -> None:
    catalog = ArtifactCatalog(Namespace("ex"))
    first = catalog.declare("taxable_base", Decimal)

    with pytest.raises(DuplicateRegistrationError, match="'ex/taxable_base'"):
        catalog.declare("taxable_base", int)

    assert catalog.kinds == (first,)
    assert fresh.identifiers() == frozenset()


def test_separate_catalogs_may_declare_the_same_identifier_until_registered(
    fresh: ArtifactRegistry,
) -> None:
    first = ArtifactCatalog(Namespace("ex")).declare("taxable_base", Decimal)
    second = ArtifactCatalog(Namespace("ex")).declare("taxable_base", int)

    assert first.identifier == second.identifier == "ex/taxable_base"


@pytest.mark.parametrize("local_id", ["", "TaxableBase", "taxable-base", "ex/taxable_base"])
def test_catalog_rejects_a_local_id_that_is_not_snake_case(
    fresh: ArtifactRegistry, local_id: str
) -> None:
    catalog = ArtifactCatalog(Namespace("ex"))

    with pytest.raises(InvalidRegistrationError, match="invalid local id"):
        catalog.declare(local_id, Decimal)

    assert catalog.kinds == ()
    assert fresh.identifiers() == frozenset()


# --- ArtifactRegistry.register_catalog ------------------------------------------------------


def test_register_catalog_registers_every_declared_kind_under_its_identifier(
    fresh: ArtifactRegistry,
) -> None:
    catalog = ArtifactCatalog(Namespace("ex"))
    base = catalog.declare("taxable_base", Decimal)
    count = catalog.declare("person_count", int)
    registry = ArtifactRegistry()

    registry.register_catalog(catalog)

    assert registry.get("ex/taxable_base") is base
    assert registry.get("ex/person_count") is count


def test_identifiers_lists_every_registered_identifier(fresh: ArtifactRegistry) -> None:
    catalog = ArtifactCatalog(Namespace("ex"))
    catalog.declare("taxable_base", Decimal)
    catalog.declare("person_count", int)
    registry = ArtifactRegistry()
    registry.register_catalog(catalog)

    identifiers = registry.identifiers()

    assert_type(identifiers, frozenset[str])
    assert identifiers == frozenset({"ex/taxable_base", "ex/person_count"})


def test_register_catalog_registers_into_that_registry_only(fresh: ArtifactRegistry) -> None:
    catalog = ArtifactCatalog(Namespace("ex"))
    catalog.declare("taxable_base", Decimal)

    ArtifactRegistry().register_catalog(catalog)

    assert fresh.identifiers() == frozenset()


def test_registering_an_empty_catalog_registers_nothing(fresh: ArtifactRegistry) -> None:
    registry = ArtifactRegistry()

    registry.register_catalog(ArtifactCatalog(Namespace("ex")))

    assert registry.identifiers() == frozenset()


def test_registering_the_same_catalog_twice_is_idempotent(fresh: ArtifactRegistry) -> None:
    catalog = ArtifactCatalog(Namespace("ex"))
    base = catalog.declare("taxable_base", Decimal)
    registry = ArtifactRegistry()
    registry.register_catalog(catalog)

    registry.register_catalog(catalog)

    assert registry.identifiers() == {"ex/taxable_base"}
    assert registry.get("ex/taxable_base") is base


def test_a_different_catalog_with_a_clashing_identifier_is_rejected(
    fresh: ArtifactRegistry,
) -> None:
    first = ArtifactCatalog(Namespace("ex"))
    base = first.declare("taxable_base", Decimal)
    second = ArtifactCatalog(Namespace("ex"))
    second.declare("taxable_base", Decimal)
    registry = ArtifactRegistry()
    registry.register_catalog(first)

    with pytest.raises(DuplicateRegistrationError, match="'ex/taxable_base'"):
        registry.register_catalog(second)

    assert registry.get("ex/taxable_base") is base


def test_a_catalog_clashing_with_a_directly_registered_kind_is_rejected(
    fresh: ArtifactRegistry,
) -> None:
    catalog = ArtifactCatalog(Namespace("ex"))
    catalog.declare("taxable_base", Decimal)
    registry = ArtifactRegistry()
    registry.register("ex/taxable_base", ArtifactKind("ex/taxable_base", Decimal))

    with pytest.raises(DuplicateRegistrationError, match="'ex/taxable_base'"):
        registry.register_catalog(catalog)


def test_the_same_local_id_may_appear_in_different_namespaces(fresh: ArtifactRegistry) -> None:
    first = ArtifactCatalog(Namespace("ex"))
    first.declare("basic_tax", Decimal)
    second = ArtifactCatalog(Namespace("ex-sub"))
    second.declare("basic_tax", Decimal)
    registry = ArtifactRegistry()

    registry.register_catalog(first)
    registry.register_catalog(second)

    assert registry.identifiers() == {"ex/basic_tax", "ex-sub/basic_tax"}


def test_a_directly_built_artifact_kind_is_not_registered(fresh: ArtifactRegistry) -> None:
    ArtifactKind("ex/taxable_base", Decimal)

    with pytest.raises(UnknownRegistrationError):
        fresh.get("ex/taxable_base")
    assert fresh.identifiers() == frozenset()
