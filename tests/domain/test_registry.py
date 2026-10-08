"""Unit tests for Registry and NamespacedRegistry: namespaced registration and typed lookup.

A registration gives only a local id; the namespace comes from the nearest package above
the registered object's module that declares `NAMESPACE`. Names are made up; the made-up
packages live in `registration_fixtures`.
"""

from __future__ import annotations

import importlib
import sys
from collections.abc import Iterator

import pytest

from app.domain.errors import (
    DomainError,
    DuplicateRegistrationError,
    InvalidRegistrationError,
    UnknownRegistrationError,
)
from app.domain.registry import NamespacedRegistry, Registry
from tests.domain.registration_fixtures.bad_namespace.oddities import Oddity
from tests.domain.registration_fixtures.with_namespace.gadgets import Gadget, Sprocket
from tests.domain.registration_fixtures.with_namespace.inner import gadgets as inner
from tests.domain.registration_fixtures.with_namespace.plain.widgets import Widget
from tests.domain.registration_fixtures.without_namespace.orphans import Orphan


def make_registry() -> NamespacedRegistry[type[object]]:
    return NamespacedRegistry[type[object]]()


# --- registering and looking up -----------------------------------------------------------


def test_register_returns_the_full_namespaced_identifier() -> None:
    assert make_registry().register("gadget", Gadget) == "ex/gadget"


def test_get_returns_the_exact_registered_object() -> None:
    registry = make_registry()
    registry.register("gadget", Gadget)
    registry.register("sprocket", Sprocket)

    found: type[object] = registry.get("ex/gadget")

    assert found is Gadget
    assert registry.get("ex/sprocket") is Sprocket


def test_get_needs_the_full_identifier_not_the_local_id() -> None:
    registry = make_registry()
    registry.register("gadget", Gadget)

    with pytest.raises(UnknownRegistrationError, match="'gadget'"):
        registry.get("gadget")


def test_get_of_an_unknown_identifier_fails() -> None:
    registry = make_registry()
    registry.register("gadget", Gadget)

    with pytest.raises(UnknownRegistrationError, match="'ex/missing'"):
        registry.get("ex/missing")


def test_registries_do_not_share_registrations() -> None:
    first = make_registry()
    first.register("gadget", Gadget)

    with pytest.raises(UnknownRegistrationError):
        make_registry().get("ex/gadget")


# --- uniqueness ---------------------------------------------------------------------------


def test_registering_an_identifier_twice_fails() -> None:
    registry = make_registry()
    registry.register("gadget", Gadget)

    with pytest.raises(DuplicateRegistrationError, match="'ex/gadget'"):
        registry.register("gadget", Sprocket)

    assert registry.get("ex/gadget") is Gadget  # never silently overridden


def test_registering_the_same_object_twice_under_one_identifier_fails() -> None:
    registry = make_registry()
    registry.register("gadget", Gadget)

    with pytest.raises(DuplicateRegistrationError, match="'ex/gadget'"):
        registry.register("gadget", Gadget)


def test_the_same_local_id_in_different_namespaces_is_allowed() -> None:
    registry = make_registry()

    assert registry.register("gadget", Gadget) == "ex/gadget"
    assert registry.register("gadget", inner.Gadget) == "ex-inner/gadget"
    assert registry.get("ex/gadget") is Gadget
    assert registry.get("ex-inner/gadget") is inner.Gadget


# --- namespaces ---------------------------------------------------------------------------


def test_namespace_is_inherited_from_an_enclosing_package() -> None:
    # `plain` declares no NAMESPACE; its parent package declares "ex".
    assert make_registry().register("widget", Widget) == "ex/widget"


def test_nearest_package_declaring_a_namespace_wins() -> None:
    # `inner` declares "ex-inner" below a package declaring "ex".
    assert make_registry().register("gadget", inner.Gadget) == "ex-inner/gadget"


def test_registering_from_a_module_without_a_namespace_fails_naming_the_module() -> None:
    module = "tests.domain.registration_fixtures.without_namespace.orphans"

    with pytest.raises(InvalidRegistrationError, match="NAMESPACE") as excinfo:
        make_registry().register("orphan", Orphan)

    assert module in str(excinfo.value)


FIXTURES = "tests.domain.registration_fixtures.with_namespace"
LATE = f"{FIXTURES}.late_namespace"
REEXPORTING = f"{FIXTURES}.reexporting"
STILL_IMPORTING = (
    r"is still being imported and has no NAMESPACE: declare NAMESPACE at the top of its "
    r"__init__\.py \(repeat the parent's to inherit it\), or do not import registering modules "
    r"from that __init__\.py"
)


@pytest.fixture
def forget_half_imported() -> Iterator[None]:
    """Drop the half-imported fixture modules afterwards, so the import fails again next time."""
    yield
    for package in (LATE, REEXPORTING):
        for name in [n for n in sys.modules if n == package or n.startswith(f"{package}.")]:
            del sys.modules[name]


@pytest.mark.usefixtures("forget_half_imported")
def test_registering_before_the_package_declares_its_namespace_fails() -> None:
    # The package imports a registering module above its NAMESPACE line; falling back to the
    # enclosing package's namespace would register the item under the wrong identifier.
    with pytest.raises(InvalidRegistrationError, match=STILL_IMPORTING) as excinfo:
        importlib.import_module(LATE)

    assert LATE in str(excinfo.value)


@pytest.mark.usefixtures("forget_half_imported")
def test_registering_from_the_init_of_a_package_inheriting_its_namespace_fails() -> None:
    # Strict on purpose: while the package initialises, a missing NAMESPACE cannot be told apart
    # from one not declared yet, so inheriting packages must not import registering modules.
    with pytest.raises(InvalidRegistrationError, match=STILL_IMPORTING) as excinfo:
        importlib.import_module(REEXPORTING)

    assert REEXPORTING in str(excinfo.value)


def test_a_malformed_namespace_is_rejected() -> None:
    with pytest.raises(InvalidRegistrationError, match="'Ex_Bad'"):
        make_registry().register("oddity", Oddity)


@pytest.mark.parametrize(
    "local_id",
    [
        "",
        "Gadget",
        "gadget-x",
        "gadget x",
        "_gadget",
        "gadget_",
        "gadget__x",
        "1gadget",
        "ex/gadget",
    ],
)
def test_a_local_id_that_is_not_snake_case_is_rejected(local_id: str) -> None:
    registry = make_registry()

    with pytest.raises(InvalidRegistrationError, match="snake_case"):
        registry.register(local_id, Gadget)


@pytest.mark.parametrize("local_id", ["gadget", "gadget_2", "big_gadget", "g"])
def test_snake_case_local_ids_are_accepted(local_id: str) -> None:
    assert make_registry().register(local_id, Gadget) == f"ex/{local_id}"


# --- one shared instance per registry subclass ---------------------------------------------


class ExampleRegistry(Registry[type[object]]):
    """A made-up registry subclass, so these tests never touch a real shared registry."""


class OtherExampleRegistry(Registry[type[object]]):
    """A second made-up registry subclass."""


def test_shared_returns_the_same_instance_every_time() -> None:
    shared = ExampleRegistry.shared()

    assert isinstance(shared, ExampleRegistry)
    assert ExampleRegistry.shared() is shared


def test_each_registry_subclass_has_its_own_shared_instance() -> None:
    assert id(OtherExampleRegistry.shared()) != id(ExampleRegistry.shared())
    assert isinstance(OtherExampleRegistry.shared(), OtherExampleRegistry)


def test_a_plain_registry_can_be_constructed_directly() -> None:
    assert isinstance(Registry[type[object]](), Registry)


def test_a_namespaced_registry_is_a_registry() -> None:
    assert issubclass(NamespacedRegistry, Registry)


def test_a_directly_constructed_registry_is_not_the_shared_one() -> None:
    assert ExampleRegistry() is not ExampleRegistry.shared()


# --- errors -------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "error", [DuplicateRegistrationError, UnknownRegistrationError, InvalidRegistrationError]
)
def test_registration_errors_are_domain_errors(error: type[Exception]) -> None:
    assert issubclass(error, DomainError)
