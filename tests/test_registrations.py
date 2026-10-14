"""The composition root's explicit list of jurisdiction packages and the data roots it yields.

Checked generically, so a package added under `app/jurisdictions/` but not registered fails here.
"""

from __future__ import annotations

import importlib
from pathlib import Path

import app.jurisdictions
import app.registrations
from app.adapters.outbound.jurisdiction_packages import JurisdictionPackages

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
