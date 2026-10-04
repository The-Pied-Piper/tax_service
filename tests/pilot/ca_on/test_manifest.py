"""The CA-ON manifest: what it selects, and that every selection's data exists."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from app.adapters.outbound.yaml_jurisdictions import YamlJurisdictionSource
from app.adapters.outbound.yaml_parameters import YamlParameterSource
from app.domain.jurisdiction_code import JurisdictionCode
from app.domain.manifest import CapabilitySelection

DATA = Path(__file__).resolve().parents[3] / "data"
CA_ON = JurisdictionCode("CA-ON")


def test_ca_on_has_one_manifest_from_2025() -> None:
    (manifest,) = YamlJurisdictionSource(DATA / "manifests").get_jurisdiction(CA_ON).manifests

    assert manifest.jurisdiction == CA_ON
    assert manifest.version == 1
    assert manifest.valid_from_tax_year == 2025
    assert manifest.capabilities == (
        CapabilitySelection(name="progressive_tax", params_family="ca/brackets"),
        CapabilitySelection(name="progressive_tax", params_family="ca-on/brackets"),
        CapabilitySelection(name="non_refundable_credit", params_family="ca/basic_personal_amount"),
        CapabilitySelection(
            name="non_refundable_credit", params_family="ca-on/basic_personal_amount"
        ),
    )


def test_every_selection_has_a_dataset_for_its_first_tax_year() -> None:
    (manifest,) = YamlJurisdictionSource(DATA / "manifests").get_jurisdiction(CA_ON).manifests
    parameters = YamlParameterSource(DATA / "parameters")
    readers: dict[str, Callable[[str, int], object]] = {
        "progressive_tax": parameters.get_brackets,
        "non_refundable_credit": parameters.get_credit,
    }

    for selection in manifest.capabilities:
        read = readers[selection.name]  # KeyError: a capability with no known dataset type
        read(selection.params_family, manifest.valid_from_tax_year)  # raises if absent
