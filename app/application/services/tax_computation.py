"""Tax computation: a jurisdiction's manifest for a tax year built into a composition, and run.

The service does the I/O only: it reads the jurisdiction through its port, asks it for the
manifest of the tax year, resolves each selection's capability class and datasets and the
manifest's input and output kinds through the ports and registries it was given, and hands them
with the artifact registry to the domain (`CapabilityBuilder`, which resolves the selection's
artifact kinds, and `FormSet`, which wires every form), which decides. Resolution errors
propagate unchanged. Built on demand per call.

A manifest's own selections are the return form's; its `forms` are peers that run once per
instance and export `<form>.<export>` kinds that every form reads. Those kinds are registered
into the artifact registry before any selection is built. `compute` returns the return form's
worksheet, as it does for a manifest without forms; `run` returns every form's worksheets.
"""

from __future__ import annotations

from typing import Any

from app.application.ports.jurisdiction_source import JurisdictionSource
from app.application.ports.parameter_source import ParameterSource
from app.domain.artifact import Artifact, ArtifactRegistry
from app.domain.capability import Capability, CapabilityRegistry
from app.domain.capability_builder import CapabilityBuilder
from app.domain.composition import Composition
from app.domain.errors import InvalidCompositionError
from app.domain.form import FormComposition, FormSet, FormWorksheets
from app.domain.jurisdiction_code import JurisdictionCode
from app.domain.manifest import CapabilitySelection, Form
from app.domain.parameters.datasets import ParameterDataset
from app.domain.record_list import RecordListKind
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
        """The composition of the return form of the manifest that applies to `tax_year` in `code`.

        For a manifest without forms, the whole computation. With forms, the return form's: its
        inputs are the manifest's without the forms' instances kinds, plus the `<form>.<export>`
        kinds it reads; `form_set` and `run` are the whole computation.
        """
        return self.form_set(code, tax_year).return_form.composition

    def form_set(self, code: JurisdictionCode, tax_year: int) -> FormSet:
        """The return form and the forms of the manifest of `tax_year` in `code`, wired."""
        manifest = self._jurisdictions.get_jurisdiction(code).manifest_for(tax_year)
        instances = {form.name: self._instances(form) for form in manifest.forms}
        exports = {
            form.name: [self._artifacts.kind(identifier) for identifier in form.exports]
            for form in manifest.forms
        }
        for form in manifest.forms:
            self._register_derived(FormComposition.derive(form.name, exports[form.name]))
        return FormSet(
            manifest.return_form_name,
            [self._capability(selection, tax_year) for selection in manifest.capabilities],
            inputs=frozenset(self._artifacts.kind(identifier) for identifier in manifest.inputs),
            outputs=frozenset(self._artifacts.kind(identifier) for identifier in manifest.outputs),
            forms=[
                FormComposition(
                    form.name,
                    [self._capability(selection, tax_year) for selection in form.capabilities],
                    instances=instances[form.name],
                    exports=exports[form.name],
                )
                for form in manifest.forms
            ],
        )

    def compute(
        self, code: JurisdictionCode, tax_year: int, *artifacts: Artifact[Any]
    ) -> Worksheet:
        """The return form's worksheet of `run(code, tax_year, *artifacts)`."""
        return self.run(code, tax_year, *artifacts).return_worksheet

    def run(
        self, code: JurisdictionCode, tax_year: int, *artifacts: Artifact[Any]
    ) -> FormWorksheets:
        """The worksheets of every form's every instance, and the return form's, from `artifacts`.

        `artifacts` are the starting artifacts of the manifest: one of each declared input kind,
        among them each form's instances.
        """
        return self.form_set(code, tax_year).compute(*artifacts)

    def _instances(self, form: Form) -> RecordListKind:
        """The record-list kind the caller supplies for `form`, one record per instance."""
        kind = self._artifacts.kind(form.instances)
        if not isinstance(kind, RecordListKind):
            raise InvalidCompositionError(
                f"form {form.name!r}: instances {form.instances!r} is not a record list"
            )
        return kind

    def _register_derived(self, kinds: tuple[RecordListKind, ...]) -> None:
        """Register each derived `<form>.<export>` kind; the same kind again is skipped.

        Another kind under a derived identifier is the registry's DuplicateRegistrationError.
        """
        for kind in kinds:
            taken = kind.identifier in self._artifacts.identifiers()
            if not taken or self._artifacts.kind(kind.identifier) != kind:
                self._artifacts.register(kind.identifier, kind)

    def _capability(self, selection: CapabilitySelection, tax_year: int) -> Capability:
        cls = self._capabilities.get(selection.name)
        # Only slots the class declares are fetched; the builder reports any other key.
        datasets: dict[str, ParameterDataset[Any]] = {
            slot: self._parameters.get(family, tax_year, cls.PARAMETERS[slot])
            for slot, family in selection.params.items()
            if slot in cls.PARAMETERS
        }
        return self._builder.build(selection, cls, datasets, self._artifacts)
