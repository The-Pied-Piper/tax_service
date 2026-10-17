"""Tax computation: a jurisdiction's manifest for a tax year built into a composition, and run.

The service does the I/O only: it reads the jurisdiction through its port, asks it for the
manifest of the tax year, resolves each selection's capability class, datasets and artifact kinds
through the ports and registries it was given, and hands them to the domain (`CapabilityBuilder`,
`Composition`), which decides. Resolution errors propagate unchanged. Built on demand per call.
"""

from __future__ import annotations

from typing import Any

from app.application.ports.jurisdiction_source import JurisdictionSource
from app.application.ports.parameter_source import ParameterSource
from app.domain.artifact import Artifact, ArtifactKind, ArtifactRegistry
from app.domain.capability import Capability, CapabilityRegistry
from app.domain.capability_builder import CapabilityBuilder
from app.domain.composition import Composition
from app.domain.errors import InvalidRegistrationError
from app.domain.jurisdiction_code import JurisdictionCode
from app.domain.manifest import CapabilitySelection
from app.domain.parameters.datasets import ParameterDataset
from app.domain.worksheet import Worksheet


class TaxComputationService:
    """Builds and runs the composition a jurisdiction's manifest describes for a tax year."""

    def __init__(
        self,
        jurisdictions: JurisdictionSource,
        parameters: ParameterSource,
        capabilities: CapabilityRegistry,
        artifacts: ArtifactRegistry,
    ) -> None:
        """Resolve manifests, datasets, capability classes and artifact kinds through these."""
        self._jurisdictions = jurisdictions
        self._parameters = parameters
        self._capabilities = capabilities
        self._artifacts = artifacts
        self._builder = CapabilityBuilder()

    def compose(self, code: JurisdictionCode, tax_year: int) -> Composition:
        """The composition of the manifest that applies to `tax_year` in jurisdiction `code`."""
        manifest = self._jurisdictions.get_jurisdiction(code).manifest_for(tax_year)
        return Composition(
            (self._capability(selection, tax_year) for selection in manifest.capabilities),
            inputs=frozenset(self._kind(identifier) for identifier in manifest.inputs),
            outputs=frozenset(self._kind(identifier) for identifier in manifest.outputs),
        )

    def compute(
        self, code: JurisdictionCode, tax_year: int, *artifacts: Artifact[Any]
    ) -> Worksheet:
        """The worksheet of `compose(code, tax_year)` computed from the starting `artifacts`."""
        return self.compose(code, tax_year).compute(*artifacts)

    def _capability(self, selection: CapabilitySelection, tax_year: int) -> Capability:
        cls = self._capabilities.get(selection.name)
        # Only slots the class declares are fetched; the builder reports any other key.
        datasets: dict[str, ParameterDataset[Any]] = {
            slot: self._parameters.get(family, tax_year, cls.PARAMETERS[slot])
            for slot, family in selection.params.items()
            if slot in cls.PARAMETERS
        }
        kinds = {
            slot: self._kind(identifier)
            for bindings in (selection.consumes, selection.produces)
            for slot, identifier in bindings.items()
        }
        return self._builder.build(selection, cls, datasets, kinds)

    def _kind(self, identifier: str) -> ArtifactKind[Any]:
        """The kind registered as `identifier`; the registry stores kinds as `object`."""
        kind = self._artifacts.get(identifier)
        if not isinstance(kind, ArtifactKind):
            raise InvalidRegistrationError(
                f"{identifier!r} is registered as {kind!r}, not as an artifact kind"
            )
        return kind
