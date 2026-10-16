"""The CA-ON manifest: what it selects, and that every slot it fills resolves.

Each parameter slot's family has a dataset of the slot's kind for the manifest's first tax year,
and each artifact slot's identifier is a registered kind of the slot's value type.
"""

from __future__ import annotations

import app.registrations  # fills the shared registries and lists the packages, as the app does
from app.adapters.outbound.yaml_jurisdictions import YamlJurisdictionSource
from app.adapters.outbound.yaml_parameters import YamlParameterSource
from app.domain.artifact import ArtifactKind, ArtifactRegistry
from app.domain.capability import CapabilityRegistry
from app.domain.jurisdiction_code import JurisdictionCode
from app.domain.manifest import CapabilitySelection, Manifest

ROOTS = app.registrations.JURISDICTIONS.roots()
CA_ON = JurisdictionCode("CA-ON")


def manifest() -> Manifest:
    (only,) = YamlJurisdictionSource(ROOTS).get_jurisdiction(CA_ON).manifests
    return only


def test_ca_on_has_one_manifest_from_2025() -> None:
    found = manifest()

    assert found.jurisdiction == CA_ON
    assert found.version == 1
    assert found.valid_from_tax_year == 2025
    assert found.capabilities == (
        CapabilitySelection(
            name="core/progressive_tax",
            params={"schedule": "ca/brackets"},
            consumes={"base": "ca/taxable_income"},
            produces={"output": "ca/federal_basic_tax"},
        ),
        CapabilitySelection(
            name="core/progressive_tax",
            params={"schedule": "ca-on/brackets"},
            consumes={"base": "ca/taxable_income"},
            produces={"output": "ca-on/ontario_basic_tax"},
        ),
        CapabilitySelection(
            name="core/non_refundable_credit",
            params={"amount": "ca/basic_personal_amount", "rate": "ca/credit_rate"},
            consumes={"tax": "ca/federal_basic_tax"},
            produces={"output": "ca/federal_tax_after_credits"},
        ),
        CapabilitySelection(
            name="core/non_refundable_credit",
            params={"amount": "ca-on/basic_personal_amount", "rate": "ca-on/credit_rate"},
            consumes={"tax": "ca-on/ontario_basic_tax"},
            produces={"output": "ca-on/ontario_tax_after_credits"},
        ),
    )


def test_every_selection_fills_exactly_its_capabilitys_slots() -> None:
    capabilities = CapabilityRegistry.shared()

    for selection in manifest().capabilities:
        cls = capabilities.get(selection.name)
        assert set(selection.params) == set(cls.PARAMETERS), selection.name
        assert set(selection.consumes) == set(cls.CONSUMES), selection.name
        assert set(selection.produces) == set(cls.PRODUCES), selection.name


def test_every_parameter_slot_has_a_dataset_of_its_kind_for_the_first_tax_year() -> None:
    found = manifest()
    parameters = YamlParameterSource(ROOTS)
    capabilities = CapabilityRegistry.shared()

    for selection in found.capabilities:
        slots = capabilities.get(selection.name).PARAMETERS  # each capability declares its kinds
        for slot, family in selection.params.items():
            kind = slots[slot]
            dataset = parameters.get(family, found.valid_from_tax_year, kind)
            assert dataset.kind is kind, (selection.name, slot)


def test_every_artifact_slot_names_a_registered_kind_of_its_value_type() -> None:
    artifacts = ArtifactRegistry.shared()
    capabilities = CapabilityRegistry.shared()

    for selection in manifest().capabilities:
        cls = capabilities.get(selection.name)
        for bindings, slots in (
            (selection.consumes, cls.CONSUMES),
            (selection.produces, cls.PRODUCES),
        ):
            for slot, identifier in bindings.items():
                kind = artifacts.get(identifier)
                assert isinstance(kind, ArtifactKind), identifier
                assert kind.identifier == identifier
                assert kind.value_type is slots[slot], (selection.name, slot)
