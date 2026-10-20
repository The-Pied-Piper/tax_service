"""The composition root's explicit list of jurisdiction packages and the data roots it yields.

Checked generically, so a package added under `app/jurisdictions/` but not registered fails here.
Catalogs register only when `JURISDICTIONS.register()` is called; importing registers no kind.
"""

from __future__ import annotations

import importlib
import inspect
import subprocess
import sys
from pathlib import Path

import app
import app.adapters.outbound.parameter_parsers
import app.domain.capabilities
import app.jurisdictions
import app.registrations
from app.adapters.outbound.jurisdiction_packages import JurisdictionPackages
from app.domain.artifact import ArtifactCatalog, ArtifactRegistry
from app.domain.capability import CapabilityRegistry

JURISDICTIONS_DIRECTORY = Path(app.jurisdictions.__file__).parent


def test_lists_the_jurisdiction_packages() -> None:
    assert isinstance(app.registrations.JURISDICTIONS, JurisdictionPackages)


def test_every_jurisdiction_package_is_registered() -> None:
    packages = {init.parent for init in JURISDICTIONS_DIRECTORY.glob("*/__init__.py")}

    assert packages
    assert packages <= set(app.registrations.JURISDICTIONS.roots().values())


def test_each_root_is_the_directory_of_the_package_declaring_its_namespace() -> None:
    for namespace, directory in app.registrations.JURISDICTIONS.roots().items():
        package = importlib.import_module(f"app.jurisdictions.{directory.name}")

        assert Path(package.__file__ or "").parent == directory
        assert package.NAMESPACE == namespace.name


def test_lists_the_core_packages() -> None:
    assert app.registrations.CORE_PACKAGES == (
        app.domain.capabilities,
        app.adapters.outbound.parameter_parsers,
    )


def test_importing_a_jurisdiction_package_registers_its_capabilities() -> None:
    registered = CapabilityRegistry.shared().get("ca-on/flow_through_share_expenses")

    assert (
        registered.__module__ == "app.jurisdictions.ca_on.capabilities.flow_through_share_expenses"
    )


def test_each_core_package_imports_every_module_in_its_directory() -> None:
    for package in app.registrations.CORE_PACKAGES:
        directory = Path(package.__file__ or "").parent
        modules = {path.stem for path in directory.glob("*.py")} - {"__init__"}

        assert modules, package.__name__
        assert modules <= set(package.__all__), package.__name__
        for name in modules:
            assert getattr(package, name) is sys.modules[f"{package.__name__}.{name}"], name


def test_has_no_side_effect_only_imports() -> None:
    source = inspect.getsource(app.registrations)

    assert "noqa" not in source


def test_every_listed_package_exposes_its_catalog() -> None:
    for directory in app.registrations.JURISDICTIONS.roots().values():
        catalog = importlib.import_module(f"app.jurisdictions.{directory.name}.catalog")

        assert isinstance(getattr(catalog, "CATALOG", None), ArtifactCatalog), catalog.__name__


def test_register_fills_a_fresh_registry_with_every_listed_catalog() -> None:
    registry = ArtifactRegistry()

    app.registrations.JURISDICTIONS.register(registry)

    expected = set()
    for directory in app.registrations.JURISDICTIONS.roots().values():
        catalog = importlib.import_module(f"app.jurisdictions.{directory.name}.catalog").CATALOG
        expected |= {kind.identifier for kind in catalog.kinds}
        for kind in catalog.kinds:
            assert registry.get(kind.identifier) is kind
    assert expected
    assert registry.identifiers() == expected


def test_registering_twice_is_idempotent() -> None:
    registry = ArtifactRegistry()
    app.registrations.JURISDICTIONS.register(registry)
    first = registry.identifiers()

    app.registrations.JURISDICTIONS.register(registry)

    assert registry.identifiers() == first


_IMPORT_EVERYTHING = """
import pkgutil, importlib
import app
import app.adapters.outbound.parameter_parsers
import app.domain.capabilities
import app.jurisdictions
import app.registrations
from app.domain.artifact import ArtifactRegistry
for info in pkgutil.walk_packages(app.jurisdictions.__path__, "app.jurisdictions."):
    importlib.import_module(info.name)
print(sorted(ArtifactRegistry.shared().identifiers()))
"""


def test_importing_the_packages_and_registrations_registers_no_artifact_kind() -> None:
    # A fresh interpreter, so modules this test session already imported are imported again.
    result = subprocess.run(
        [sys.executable, "-c", _IMPORT_EVERYTHING],
        cwd=Path(app.__file__).parent.parent,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "[]"
