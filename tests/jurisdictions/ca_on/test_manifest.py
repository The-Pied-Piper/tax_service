"""The CA-ON manifest: what it selects, and that every selection's data exists."""

from __future__ import annotations

import app.registrations  # fills the shared registries and lists the packages, as the app does
from app.adapters.outbound.yaml_jurisdictions import YamlJurisdictionSource
from app.adapters.outbound.yaml_parameters import YamlParameterSource
from app.domain.capability import CapabilityRegistry
from app.domain.jurisdiction_code import JurisdictionCode
from app.domain.manifest import CapabilitySelection

ROOTS = app.registrations.JURISDICTIONS.roots()
CA_ON = JurisdictionCode("CA-ON")


def test_ca_on_has_one_manifest_from_2025() -> None:
    (manifest,) = YamlJurisdictionSource(ROOTS).get_jurisdiction(CA_ON).manifests

    assert manifest.jurisdiction == CA_ON
    assert manifest.version == 1
    assert manifest.valid_from_tax_year == 2025
    assert manifest.capabilities == (
        CapabilitySelection(name="core/progressive_tax", params_family="ca/brackets"),
        CapabilitySelection(name="core/progressive_tax", params_family="ca-on/brackets"),
        CapabilitySelection(
            name="core/non_refundable_credit", params_family="ca/basic_personal_amount"
        ),
        CapabilitySelection(
            name="core/non_refundable_credit", params_family="ca-on/basic_personal_amount"
        ),
    )


def test_every_selection_has_a_dataset_for_its_first_tax_year() -> None:
    (manifest,) = YamlJurisdictionSource(ROOTS).get_jurisdiction(CA_ON).manifests
    parameters = YamlParameterSource(ROOTS)
    capabilities = CapabilityRegistry.shared()

    for selection in manifest.capabilities:
        kind = capabilities.get(selection.name).PARAMETERS  # each capability declares its kind
        dataset = parameters.get(selection.params_family, manifest.valid_from_tax_year, kind)
        assert dataset.kind is kind
