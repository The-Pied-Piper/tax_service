"""Forms: peers that run once per instance and read each other's exports.

A computation is a flat set of forms that together are the return; none is special. A form is a
group of capabilities with the artifacts it exports, never a capability itself. A `FormComposition`
is one form wired: an inner `Composition` whose outputs are the form's exports and whose inputs are
derived. The inputs of a form with `instances` (a record-list kind, one record per instance) are
the fields of that kind; a form without an `instances` list has exactly one implicit instance,
fed from the starting artifacts it reads. The kinds a form reads that other forms export are its
imports and are inputs too.

For each export `X` of the form `B` the engine derives the kind `B.X`: a record list of one field,
`X`, with a record per instance in instance order (one record for a form without an instances list).
Every form reads any such kind by its identifier; an export nobody reads is fine.

A `FormSet` holds the forms of one computation. It orders them by their imports, runs each once
per instance record (a form without an instances list has one) on its own `Worksheet`, keeps
every form's exports in one store and hands each run its imports as starting artifacts. It
returns a plain mapping: form name to one `Worksheet` per instance, in instance order.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from decimal import Decimal
from typing import Any

from app.domain.artifact import Artifact, ArtifactKind
from app.domain.capability import Capability
from app.domain.composition import Composition
from app.domain.errors import (
    DomainError,
    DuplicateArtifactError,
    InvalidCompositionError,
    NotFoundError,
)
from app.domain.record_list import RecordList, RecordListKind
from app.domain.trace import FormInstanceLine, TraceLine
from app.domain.worksheet import Worksheet


class FormComposition:
    """One form wired: the capabilities of form `name` as an inner `Composition`.

    Built with `exports` and, optionally, the `instances` kind (a record list, else an
    InvalidCompositionError). The inner composition returns the exports. Its inputs are the fields
    of `instances`; without instances they are the kinds of `starting` (the starting artifacts of
    the computation) that the form's capabilities consume or export, plus, always, its imports. An
    export of a `Decimal` or `int` kind or a record-list kind is also readable by every form as
    `<form>.<export>`; one of another kind (a rate, digits) is only on the form's worksheets.
    Any breach of the rules of `Composition`, or an empty `exports` or an export that is another
    form's, is an InvalidCompositionError. The form is always named in the message
    (`form 'x': ...`), whether or not it has an instances list: a form without one has one instance.
    """

    def __init__(
        self,
        name: str,
        capabilities: Iterable[Capability],
        *,
        exports: Iterable[ArtifactKind[Any]],
        instances: ArtifactKind[Any] | None = None,
        starting: frozenset[ArtifactKind[Any]] = frozenset(),
    ) -> None:
        """Wire `capabilities` as the form `name`, exporting `exports`, over `instances` if any."""
        if instances is not None and not isinstance(instances, RecordListKind):
            raise InvalidCompositionError(
                f"form {name!r}: instances {instances.identifier!r} is not a record list"
            )
        listed = tuple(exports)
        if not listed:
            raise InvalidCompositionError(f"form {name!r}: exports must name at least one artifact")
        for export in listed:
            if export.is_form_export:
                raise InvalidCompositionError(
                    f"form {name!r}: export {export.identifier!r} is another form's export"
                )
        wired = tuple(capabilities)
        produced = {kind for capability in wired for kind in capability.produces}
        read = {kind for capability in wired for kind in capability.consumes} | set(listed)
        self._name = name
        self._instances = instances
        self._exports = listed
        self._derived = self.derive(name, listed)
        self._imports = frozenset(kind for kind in read - produced if kind.is_form_export)
        self._inputs = (
            frozenset(instances.fields) if instances is not None else frozenset(read & starting)
        )
        try:
            self._composition = Composition(
                wired, inputs=self._inputs | self._imports, outputs=frozenset(listed)
            )
        except InvalidCompositionError as exc:
            raise InvalidCompositionError(f"form {name!r}: {exc}") from exc

    @staticmethod
    def derive(name: str, exports: Iterable[ArtifactKind[Any]]) -> tuple[RecordListKind, ...]:
        """The kind `<form>.<export>` of each of the form `name`'s `exports` a record can hold.

        Each is a record list of the export's one field, in the order of the exports. An export
        that is not an amount, a count or a record list (a rate, say, or digits) has none: no
        other form reads it.
        """
        namespace, _, form_id = name.partition("/")
        return tuple(
            RecordListKind(f"{namespace}/{form_id}.{export.label}", fields=(export,))
            for export in exports
            if issubclass(export.value_type, Decimal)
            or export.value_type is int
            or isinstance(export, RecordListKind)
        )

    @property
    def name(self) -> str:
        """The form's name, `<namespace>/<snake_case>`."""
        return self._name

    @property
    def instances(self) -> RecordListKind | None:
        """The record-list kind with a record per instance; `None` without an instances list."""
        return self._instances

    @property
    def exports(self) -> tuple[ArtifactKind[Any], ...]:
        """The kinds the form exports, in order."""
        return self._exports

    @property
    def derived(self) -> tuple[RecordListKind, ...]:
        """The kind `<form>.<export>` of each export a record can hold, in export order."""
        return self._derived

    @property
    def inputs(self) -> frozenset[ArtifactKind[Any]]:
        """The kinds the form starts from, imports aside: instance fields or starting artifacts."""
        return self._inputs

    @property
    def imports(self) -> frozenset[ArtifactKind[Any]]:
        """The kinds of other forms' exports that this form reads."""
        return self._imports

    @property
    def composition(self) -> Composition:
        """The inner composition, computed once per instance (one without an instances list)."""
        return self._composition


class FormSet:
    """The forms of a computation, run in the order of their imports.

    Construction fails with InvalidCompositionError naming the forms for a form listed twice, an
    instances kind that is not among `inputs`, an input that is a form's derived `<form>.<export>`
    kind, an import that no form exports, a cycle of imports, or an input that no form reads (an
    instances kind is read by its form).
    """

    def __init__(
        self, forms: Iterable[FormComposition], *, inputs: frozenset[ArtifactKind[Any]]
    ) -> None:
        """Wire `forms` into a computation that starts from the artifacts of the kinds `inputs`."""
        listed = tuple(forms)
        self._check_names(listed)
        self._check_instances(listed, inputs)
        self._producers: dict[ArtifactKind[Any], str] = {
            kind: form.name for form in listed for kind in form.derived
        }
        self._check_not_derived(inputs)
        self._check_imports(listed)
        self._check_inputs_are_read(listed, inputs)
        self._inputs = inputs
        self._forms = self._order(listed)

    @property
    def forms(self) -> tuple[FormComposition, ...]:
        """The forms in the order they run."""
        return self._forms

    def form(self, name: str) -> FormComposition:
        """The form `name`, else a NotFoundError."""
        for form in self._forms:
            if form.name == name:
                return form
        raise NotFoundError(f"no form {name!r}")

    def compute(self, *artifacts: Artifact[Any]) -> dict[str, tuple[Worksheet, ...]]:
        """Run every form on `artifacts`: one of each input kind, instances kinds among them.

        Each form runs once per record of its instances (a form without an instances list has one
        instance), in `forms` order, on a worksheet of its inputs and its imports. The result maps
        each form's name to its worksheets in instance order, none if its instances list is empty.
        A DomainError from a run is raised as itself; its message starts with the form and the
        instance position (`<form>, instance N: ...`, N being 1 for a form without an instances
        list). A kind given that is a form's export is refused: the forms derive it,
        and two values for one kind are a DuplicateArtifactError, as in a `Worksheet`.
        """
        kinds = [artifact.kind for artifact in artifacts]
        for kind in kinds:
            if kinds.count(kind) > 1:
                raise DuplicateArtifactError(f"two starting values for {kind.label!r}")
        given = {artifact.kind: artifact for artifact in artifacts}
        self._check_given(given)
        store: dict[ArtifactKind[Any], Artifact[Any]] = {}
        worksheets: dict[str, tuple[Worksheet, ...]] = {}
        for form in self._forms:
            ran = tuple(self._runs(form, given, store))
            worksheets[form.name] = ran
            for derived in form.derived:
                (export,) = derived.fields
                listed = [{export: worksheet.get(export).value} for worksheet in ran]
                store[derived] = Artifact(derived, RecordList(derived.fields, listed))
        return worksheets

    def trace(self, worksheets: Mapping[str, Sequence[Worksheet]]) -> tuple[TraceLine, ...]:
        """A `FormInstanceLine` per worksheet of `worksheets`, in the order the forms run.

        The position is from 1; a form without an instances list has one instance, 1.
        """
        return tuple(
            FormInstanceLine(form.name, position, worksheet.trace)
            for form in self._forms
            for position, worksheet in enumerate(worksheets.get(form.name, ()), start=1)
        )

    def _runs(
        self,
        form: FormComposition,
        given: Mapping[ArtifactKind[Any], Artifact[Any]],
        store: Mapping[ArtifactKind[Any], Artifact[Any]],
    ) -> Iterable[Worksheet]:
        imported = [store[kind] for kind in sorted(form.imports, key=Composition.sort_key)]
        instances = form.instances
        if instances is None:
            starting = [given[kind] for kind in sorted(form.inputs, key=Composition.sort_key)]
            yield self._run(form, 1, [*starting, *imported])
            return
        for position, record in enumerate(given[instances].value.records, start=1):
            starting = [Artifact(kind, record[kind]) for kind in instances.fields]
            yield self._run(form, position, [*starting, *imported])

    @staticmethod
    def _run(form: FormComposition, position: int, starting: list[Artifact[Any]]) -> Worksheet:
        try:
            return form.composition.compute(*starting)
        except DomainError as exc:
            exc.args = (f"{form.name}, instance {position}: {exc}",)
            raise

    def _check_given(self, given: Mapping[ArtifactKind[Any], Artifact[Any]]) -> None:
        self._check_not_derived(given.keys())
        Composition.check_starting_kinds(given.keys(), self._inputs)

    def _check_not_derived(self, kinds: Iterable[ArtifactKind[Any]]) -> None:
        derived = set(kinds) & self._producers.keys()
        if derived:
            verb = "is" if len(derived) == 1 else "are"
            raise InvalidCompositionError(
                f"{Composition.labels(derived)} {verb} exported by a form, not an input"
            )

    @staticmethod
    def _check_names(forms: tuple[FormComposition, ...]) -> None:
        names = [form.name for form in forms]
        for each in names:
            if names.count(each) > 1:
                raise InvalidCompositionError(f"form {each!r} is listed more than once")

    @staticmethod
    def _check_instances(
        forms: tuple[FormComposition, ...], inputs: frozenset[ArtifactKind[Any]]
    ) -> None:
        for form in forms:
            if form.instances is not None and form.instances not in inputs:
                raise InvalidCompositionError(
                    f"form {form.name!r}: instances {form.instances.identifier!r} "
                    "is not an input of the computation"
                )

    def _check_imports(self, forms: tuple[FormComposition, ...]) -> None:
        for form in forms:
            for kind in sorted(form.imports, key=Composition.sort_key):
                if kind not in self._producers:
                    raise InvalidCompositionError(
                        f"form {form.name!r}: no form exports {kind.label!r}, which it imports"
                    )

    def _check_inputs_are_read(
        self, forms: tuple[FormComposition, ...], inputs: frozenset[ArtifactKind[Any]]
    ) -> None:
        read = {kind for form in forms for kind in form.inputs}
        read |= {form.instances for form in forms if form.instances is not None}
        unread = inputs - read
        if unread:
            kind = min(unread, key=Composition.sort_key)
            raise InvalidCompositionError(f"input {kind.label!r} is consumed by nothing")

    def _order(self, forms: tuple[FormComposition, ...]) -> tuple[FormComposition, ...]:
        """The forms so that each runs after every form it imports from; ties by name."""
        needs = {form.name: {self._producers[kind] for kind in form.imports} for form in forms}
        pending = sorted(forms, key=lambda form: form.name)
        done: set[str] = set()
        order: list[FormComposition] = []
        while pending:
            chosen = next((form for form in pending if needs[form.name] <= done), None)
            if chosen is None:
                cycle = self._on_cycle({form.name: needs[form.name] for form in pending})
                names = ", ".join(repr(each) for each in sorted(cycle))
                raise InvalidCompositionError(f"cycle involving forms {names}")
            pending.remove(chosen)
            order.append(chosen)
            done.add(chosen.name)
        return tuple(order)

    @staticmethod
    def _on_cycle(stuck: Mapping[str, set[str]]) -> set[str]:
        """The stuck forms that import from each other, without those only downstream of them."""
        remaining = set(stuck)
        while True:
            sinks = {
                form for form in remaining if not any(form in stuck[other] for other in remaining)
            }
            if not sinks:
                return remaining
            remaining -= sinks
