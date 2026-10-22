"""Tax computation: a jurisdiction's manifest for a tax year built into a composition, and run.

The service does the I/O only: it reads the jurisdiction through its port, asks it for the
manifest of the tax year, resolves each selection's capability class and datasets and the
manifest's input and output kinds through the ports and registries it was given, and hands them
with the artifact registry to the domain (`CapabilityBuilder`, which resolves the selection's
artifact kinds, and `Composition`), which decides. Resolution errors propagate unchanged. Built
on demand per call.
"""

from __future__ import annotations

from typing import Any

from app.application.ports.jurisdiction_source import JurisdictionSource
from app.application.ports.parameter_source import ParameterSource
from app.domain.artifact import Artifact, ArtifactRegistry
from app.domain.capability import Capability, CapabilityRegistry
from app.domain.capability_builder import CapabilityBuilder
from app.domain.composition import Composition
from app.domain.form import FormRun
from app.domain.jurisdiction_code import JurisdictionCode
from app.domain.manifest import CapabilitySelection, Form
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
        runs = [self._form_run(form, tax_year) for form in manifest.forms]
        return Composition(
            [
                *runs,
                *(self._capability(selection, tax_year) for selection in manifest.capabilities),
            ],
            inputs=frozenset(self._artifacts.kind(identifier) for identifier in manifest.inputs),
            outputs=frozenset(self._artifacts.kind(identifier) for identifier in manifest.outputs),
        )

    def compute(
        self, code: JurisdictionCode, tax_year: int, *artifacts: Artifact[Any]
    ) -> Worksheet:
        """The worksheet of `compose(code, tax_year)` computed from the starting `artifacts`."""
        return self.compose(code, tax_year).compute(*artifacts)

    def _form_run(self, form: Form, tax_year: int) -> FormRun:
        """The node for `form`, its derived export kinds registered so selections can read them."""
        run = FormRun(
            form.name,
            self._artifacts.kind(form.instances),
            [self._artifacts.kind(identifier) for identifier in form.exports],
            [self._capability(selection, tax_year) for selection in form.capabilities],
        )
        for kind in run.derived:
            # Idempotent: the same kind again is skipped, another kind under it is refused.
            taken = kind.identifier in self._artifacts.identifiers()
            if not taken or self._artifacts.kind(kind.identifier) != kind:
                self._artifacts.register(kind.identifier, kind)
        return run

    def _capability(self, selection: CapabilitySelection, tax_year: int) -> Capability:
        cls = self._capabilities.get(selection.name)
        # Only slots the class declares are fetched; the builder reports any other key.
        datasets: dict[str, ParameterDataset[Any]] = {
            slot: self._parameters.get(family, tax_year, cls.PARAMETERS[slot])
            for slot, family in selection.params.items()
            if slot in cls.PARAMETERS
        }
        return self._builder.build(selection, cls, datasets, self._artifacts)
