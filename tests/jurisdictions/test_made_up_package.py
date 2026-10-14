"""A made-up jurisdiction needs only a package directory: NAMESPACE, a catalog, manifests and
parameters, read through the real sources. Names and values are made up."""

from __future__ import annotations

import importlib
import sys
from decimal import Decimal
from pathlib import Path

import pytest

import app.registrations  # noqa: F401  (fills the shared registries, as the app does)
from app.adapters.outbound.jurisdiction_packages import JurisdictionPackages
from app.adapters.outbound.yaml_jurisdictions import YamlJurisdictionSource
from app.adapters.outbound.yaml_parameters import YamlParameterSource
from app.domain.artifact import ArtifactRegistry
from app.domain.capability import CapabilityRegistry
from app.domain.jurisdiction_code import JurisdictionCode
from app.domain.manifest import CapabilitySelection
from app.domain.parameters.brackets import BRACKETS, Bracket, BracketSchedule
from app.domain.registry import Namespace
from tests.jurisdictions.registration_fixtures import ex_on

D = Decimal
EX_ON = JurisdictionCode("EX-ON")
PACKAGES = JurisdictionPackages((ex_on,))


def test_the_package_directory_is_its_root() -> None:
    assert PACKAGES.roots() == {Namespace("ex-on"): Path(ex_on.__file__).parent}


def test_its_manifest_is_read_from_the_package() -> None:
    (manifest,) = YamlJurisdictionSource(PACKAGES.roots()).get_jurisdiction(EX_ON).manifests

    assert manifest.capabilities == (
        CapabilitySelection(
            name="core/progressive_tax",
            params={"schedule": "ex-on/brackets"},
            consumes={"base": "ex-on/levy_base"},
            produces={"output": "ex-on/levy"},
        ),
    )


def test_its_datasets_are_read_from_the_package() -> None:
    dataset = YamlParameterSource(PACKAGES.roots()).get("ex-on/brackets", 2025, BRACKETS)

    assert dataset.values == BracketSchedule(
        (Bracket(D("0"), D("0.10")), Bracket(D("100"), D("0.20")))
    )


def test_every_parameter_slot_has_a_dataset() -> None:
    (manifest,) = YamlJurisdictionSource(PACKAGES.roots()).get_jurisdiction(EX_ON).manifests
    parameters = YamlParameterSource(PACKAGES.roots())

    for selection in manifest.capabilities:
        slots = CapabilityRegistry.shared().get(selection.name).PARAMETERS
        assert set(selection.params) == set(slots)
        for slot, family in selection.params.items():
            kind = slots[slot]
            assert parameters.get(family, manifest.valid_from_tax_year, kind).kind is kind


def test_every_artifact_slot_names_a_kind_of_its_catalog() -> None:
    (manifest,) = YamlJurisdictionSource(PACKAGES.roots()).get_jurisdiction(EX_ON).manifests
    declared = {"ex-on/levy_base", "ex-on/levy"}  # see the catalog test below

    for selection in manifest.capabilities:
        assert set(selection.consumes.values()) | set(selection.produces.values()) <= declared


def test_its_catalog_registers_kinds_in_its_namespace(monkeypatch: pytest.MonkeyPatch) -> None:
    # A fresh registry and a fresh import, so the shared registry never sees made-up kinds.
    registry = ArtifactRegistry()
    monkeypatch.setattr(ArtifactRegistry, "shared", classmethod(lambda cls: registry))
    name = "tests.jurisdictions.registration_fixtures.ex_on.catalog"
    monkeypatch.delitem(sys.modules, name, raising=False)

    catalog = importlib.import_module(name)

    assert registry.identifiers() == {"ex-on/levy_base", "ex-on/levy"}
    assert registry.get("ex-on/levy") is catalog.LEVY
