"""Unit tests for JurisdictionPackages: jurisdiction packages -> namespace -> package directory.

A package's directory is `Path(package.__file__).parent` and its namespace is its `NAMESPACE`;
packages declare nothing else. Packages here are made-up module objects.
"""

from __future__ import annotations

from pathlib import Path
from types import ModuleType

import pytest

from app.adapters.outbound.jurisdiction_packages import JurisdictionPackages
from app.domain.errors import DuplicateRegistrationError, InvalidRegistrationError
from app.domain.registry import Namespace


def package(directory: Path, name: str, namespace: object = None) -> ModuleType:
    module = ModuleType(name)
    module.__file__ = str(directory / name / "__init__.py")
    module.__path__ = [str(directory / name)]
    if namespace is not None:
        module.NAMESPACE = namespace  # type: ignore[attr-defined]
    return module


def test_maps_each_namespace_to_its_package_directory(tmp_path: Path) -> None:
    packages = JurisdictionPackages(
        (package(tmp_path, "ex", "ex"), package(tmp_path, "ex_on", "ex-on"))
    )

    assert packages.roots() == {
        Namespace("ex"): tmp_path / "ex",
        Namespace("ex-on"): tmp_path / "ex_on",
    }


def test_no_packages_give_no_roots() -> None:
    assert JurisdictionPackages(()).roots() == {}


def test_a_package_without_namespace_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(InvalidRegistrationError, match="ex_on"):
        JurisdictionPackages((package(tmp_path, "ex_on"),))


def test_an_invalid_namespace_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(InvalidRegistrationError, match="ex_on"):
        JurisdictionPackages((package(tmp_path, "ex_on", "Ex_On"),))


def test_two_packages_with_one_namespace_are_rejected(tmp_path: Path) -> None:
    with pytest.raises(DuplicateRegistrationError, match="'ex'"):
        JurisdictionPackages((package(tmp_path, "one", "ex"), package(tmp_path, "two", "ex")))


def test_a_package_without_a_file_is_rejected() -> None:
    module = ModuleType("ex_pkg")
    module.NAMESPACE = "ex"  # type: ignore[attr-defined]

    with pytest.raises(InvalidRegistrationError, match="ex_pkg"):
        JurisdictionPackages((module,))
