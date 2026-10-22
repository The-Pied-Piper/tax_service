"""The run of a form: its capabilities computed once per instance, as one node of a composition.

A `Form` (manifest.py) is manifest data. `FormRun` is what lets the return's `Composition` carry
it: the one adapter between a form and the capability contract `Worksheet.apply` takes. It
consumes the form's instances kind (a record list, one record per instance) and produces, for each
export `X` of the form `B`, the derived kind `B.X`: a record list of one field, `X`, with a record
per instance, in instance order. The form's own capabilities are wired once into an inner
`Composition`, whose inputs are the fields of the instances kind and whose outputs are the exports;
each instance is computed on its own `Worksheet`, so instances never meet.
"""

from __future__ import annotations

from collections.abc import Iterable
from decimal import Decimal
from typing import Any

from app.domain.artifact import Artifact, ArtifactKind
from app.domain.capability import Capability, CapabilityResult
from app.domain.composition import Composition
from app.domain.errors import DomainError, InvalidCompositionError
from app.domain.record_list import RecordList, RecordListKind
from app.domain.trace import FormInstanceLine, TraceLine


class FormRun(Capability):
    """The form `name` run on each record of its `instances` list; see the module docstring.

    A capability only so that `Worksheet.apply` accepts it: it declares no slots, calls
    `Capability.__init__()` with none and overrides `consumes`, `produces` and `compute`. Raises
    InvalidCompositionError naming the form if `instances` is not a record-list kind, an export
    is neither a `Decimal` or `int` kind nor a record-list kind, or the inner wiring breaks a rule
    of `Composition`.
    """

    def __init__(
        self,
        name: str,
        instances: ArtifactKind[Any],
        exports: Iterable[ArtifactKind[Any]],
        capabilities: Iterable[Capability],
    ) -> None:
        """Wire `capabilities` into form `name`, consuming `instances` and exporting `exports`."""
        super().__init__()
        if not isinstance(instances, RecordListKind):
            raise InvalidCompositionError(
                f"form {name!r}: instances {instances.identifier!r} is not a record list"
            )
        self._name = name
        self._instances = instances
        self._exports = tuple(exports)
        namespace, _, form_id = name.partition("/")
        self._derived = tuple(
            RecordListKind(f"{namespace}/{form_id}.{export.label}", fields=(self._checked(export),))
            for export in self._exports
        )
        try:
            self._composition = Composition(
                capabilities,
                inputs=frozenset(instances.fields),
                outputs=frozenset(self._exports),
            )
        except InvalidCompositionError as exc:
            raise InvalidCompositionError(f"form {name!r}: {exc}") from exc

    @property
    def derived(self) -> tuple[RecordListKind, ...]:
        """The kind `<form>.<export>` of each export, in the order of the exports."""
        return self._derived

    @property
    def consumes(self) -> frozenset[ArtifactKind[Any]]:
        """The form's instances kind."""
        return frozenset({self._instances})

    @property
    def produces(self) -> frozenset[ArtifactKind[Any]]:
        """The derived kind of each export."""
        return frozenset(self._derived)

    def compute(self, inputs: tuple[Artifact[Any], ...]) -> CapabilityResult:
        """Run the form on each instance, in order; a failure names the form and the position."""
        records = self._input(inputs, self._instances).value.records
        exported: list[list[dict[ArtifactKind[Any], object]]] = [[] for _ in self._exports]
        trace: list[TraceLine] = []
        for position, record in enumerate(records, start=1):
            starting = (Artifact(kind, record[kind]) for kind in self._instances.fields)
            try:
                worksheet = self._composition.compute(*starting)
            except DomainError as exc:
                exc.args = (f"{self._name}, instance {position}: {exc}",)
                raise
            for export, listed in zip(self._exports, exported, strict=True):
                listed.append({export: worksheet.get(export).value})
            trace.append(FormInstanceLine(self._name, position, worksheet.trace))
        outputs = tuple(
            Artifact(kind, RecordList(kind.fields, listed))
            for kind, listed in zip(self._derived, exported, strict=True)
        )
        return CapabilityResult(outputs=outputs, trace=tuple(trace))

    def _checked(self, export: ArtifactKind[Any]) -> ArtifactKind[Any]:
        """`export` if a record can hold it: a `Decimal` or `int` kind or a record-list kind."""
        if not (
            issubclass(export.value_type, Decimal)
            or export.value_type is int
            or isinstance(export, RecordListKind)
        ):
            raise InvalidCompositionError(
                f"form {self._name!r}: export {export.identifier!r} is a "
                f"{export.value_type.__name__}, not an amount, a count or a record list"
            )
        return export
