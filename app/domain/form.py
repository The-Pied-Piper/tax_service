"""Forms: peers that run once per instance and read each other's exports.

A form is a group of capabilities with the artifacts it exports, never a capability itself. A
`FormComposition` is one form wired: an inner `Composition` whose inputs are the fields of its
instances kind (a record list, one record per instance) and its imports, and whose outputs are its
exports. For each export `X` of the form `B` the engine derives the kind `B.X`: a record list of
one field, `X`, with a record per instance in instance order. Every form reads any such kind by its
identifier; the dotted kinds a form consumes (or, for the return form, declares as outputs) and
nothing in it produces are its imports.

The return form is the form of the manifest's own selections, with no instances and exactly one
run. It is not special otherwise: it reads imports like any other form, and its outputs are the
computation's outputs.

A `FormSet` holds the return form and the others. It orders the forms by their imports, runs each
once per instance on its own `Worksheet`, keeps every form's exports in one store and hands each
run the imports as starting artifacts. It returns `FormWorksheets`: every worksheet of every run,
by form name and instance position, and the return form's worksheet.
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

    Built with the form's `instances` kind (a record list, else an InvalidCompositionError) and
    `exports`, the inner composition takes the
    instances' fields and the imports, and returns the exports. An export is a `Decimal` or `int`
    kind or a record-list kind, else a record could not hold it. Any breach of the rules of
    `Composition`, or an empty `exports`, is an InvalidCompositionError naming the form. The
    return form is built with `for_return` and has no instances.
    """

    def __init__(
        self,
        name: str,
        capabilities: Iterable[Capability],
        *,
        instances: ArtifactKind[Any],
        exports: Iterable[ArtifactKind[Any]],
    ) -> None:
        """Wire `capabilities` as the form `name` of `instances`, exporting `exports`."""
        if not isinstance(instances, RecordListKind):
            raise InvalidCompositionError(
                f"form {name!r}: instances {instances.identifier!r} is not a record list"
            )
        listed = tuple(exports)
        if not listed:
            raise InvalidCompositionError(f"form {name!r}: exports must name at least one artifact")
        self._instances: RecordListKind | None = instances
        self._exports = listed
        self._derived = self.derive(name, listed)
        self._wire(name, capabilities, frozenset(instances.fields), frozenset(listed))

    @classmethod
    def for_return(
        cls,
        name: str,
        capabilities: Iterable[Capability],
        *,
        inputs: frozenset[ArtifactKind[Any]],
        outputs: frozenset[ArtifactKind[Any]],
    ) -> FormComposition:
        """The return form `name`: no instances, no exports; `inputs` and `outputs` as given.

        Its wiring errors are those of `Composition`, unprefixed, as for a manifest with no
        forms other than the return form.
        """
        form = cls.__new__(cls)
        form._instances = None
        form._exports = ()
        form._derived = ()
        form._wire(name, capabilities, inputs, outputs)
        return form

    @staticmethod
    def derive(name: str, exports: Iterable[ArtifactKind[Any]]) -> tuple[RecordListKind, ...]:
        """The kind `<form>.<export>` of each of the form `name`'s `exports`, in order.

        Each is a record list of the export's one field. An export that is not an amount, a count
        or a record list is an InvalidCompositionError naming the form.
        """
        namespace, _, form_id = name.partition("/")
        kinds: list[RecordListKind] = []
        for export in exports:
            if not (
                issubclass(export.value_type, Decimal)
                or export.value_type is int
                or isinstance(export, RecordListKind)
            ):
                raise InvalidCompositionError(
                    f"form {name!r}: export {export.identifier!r} is a "
                    f"{export.value_type.__name__}, not an amount, a count or a record list"
                )
            kinds.append(RecordListKind(f"{namespace}/{form_id}.{export.label}", fields=(export,)))
        return tuple(kinds)

    @property
    def name(self) -> str:
        """The form's name, `<namespace>/<snake_case>`."""
        return self._name

    @property
    def instances(self) -> RecordListKind | None:
        """The record-list kind with a record per instance; `None` for the return form."""
        return self._instances

    @property
    def exports(self) -> tuple[ArtifactKind[Any], ...]:
        """The kinds the form exports, in order; none for the return form."""
        return self._exports

    @property
    def derived(self) -> tuple[RecordListKind, ...]:
        """The kind `<form>.<export>` of each export, in the order of the exports."""
        return self._derived

    @property
    def imports(self) -> frozenset[ArtifactKind[Any]]:
        """The kinds of other forms' exports that this form reads."""
        return self._imports

    @property
    def composition(self) -> Composition:
        """The inner composition, computed once per instance (once for the return form)."""
        return self._composition

    def _wire(
        self,
        name: str,
        capabilities: Iterable[Capability],
        inputs: frozenset[ArtifactKind[Any]],
        outputs: frozenset[ArtifactKind[Any]],
    ) -> None:
        wired = tuple(capabilities)
        produced = {kind for capability in wired for kind in capability.produces}
        read = {kind for capability in wired for kind in capability.consumes} | outputs
        self._name = name
        self._imports = frozenset(kind for kind in read - produced if kind.is_form_export)
        try:
            self._composition = Composition(wired, inputs=inputs | self._imports, outputs=outputs)
        except InvalidCompositionError as exc:
            if self._instances is None:
                raise
            raise InvalidCompositionError(f"form {name!r}: {exc}") from exc


class FormWorksheets:
    """What a `FormSet` run kept: every form's worksheet per instance, and the return's.

    The worksheets of a form are in instance order, reached by the form's name and the instance's
    position from 1. The return form is reached the same way, with the one position 1.
    """

    def __init__(
        self,
        return_form: str,
        worksheets: Mapping[str, Sequence[Worksheet]],
        return_worksheet: Worksheet,
    ) -> None:
        """Keep `worksheets` (in the order the forms ran) and the return form's worksheet."""
        self._return_form = return_form
        self._worksheets = {form: tuple(found) for form, found in worksheets.items()}
        self._worksheets[return_form] = (return_worksheet,)
        self._return_worksheet = return_worksheet

    @property
    def return_worksheet(self) -> Worksheet:
        """The return form's worksheet: its inputs, its imports and everything it computed."""
        return self._return_worksheet

    @property
    def forms(self) -> tuple[str, ...]:
        """The names of the forms in the order they ran, the return form last."""
        return tuple(self._worksheets)

    @property
    def trace(self) -> tuple[TraceLine, ...]:
        """A `FormInstanceLine` per instance of each form in run order, then the return's lines."""
        lines: list[TraceLine] = []
        for form, found in self._worksheets.items():
            if form != self._return_form:
                lines.extend(
                    FormInstanceLine(form, position, worksheet.trace)
                    for position, worksheet in enumerate(found, start=1)
                )
        return (*lines, *self._return_worksheet.trace)

    def worksheets(self, form: str) -> tuple[Worksheet, ...]:
        """Every instance's worksheet of `form`, in instance order; none for no instances."""
        if form not in self._worksheets:
            raise NotFoundError(f"no form {form!r} was run")
        return self._worksheets[form]

    def worksheet(self, form: str, position: int) -> Worksheet:
        """The worksheet of the instance of `form` at `position`, counted from 1."""
        found = self.worksheets(form)
        if not 1 <= position <= len(found):
            raise NotFoundError(
                f"form {form!r} has no instance {position}: it ran {len(found)} instance(s)"
            )
        return found[position - 1]


class FormSet:
    """The return form and the other forms of a computation, run in the order of their imports.

    Construction fails with InvalidCompositionError naming the forms for a form listed twice or
    named like the return form, an instances kind that is not among `inputs`, an import that no
    form exports, or a cycle of imports. The return form's inputs are `inputs` without the forms'
    instances kinds; its outputs are `outputs`. Without forms the set computes what the return
    form's `Composition` does, with the same errors.
    """

    def __init__(
        self,
        name: str,
        capabilities: Iterable[Capability],
        *,
        inputs: frozenset[ArtifactKind[Any]],
        outputs: frozenset[ArtifactKind[Any]],
        forms: Iterable[FormComposition] = (),
    ) -> None:
        """Wire the return form `name` of `capabilities` and `forms` into a computation."""
        others = tuple(forms)
        self._check_names(name, others)
        self._check_instances(others, inputs)
        instance_kinds = frozenset(kind for form in others if (kind := form.instances) is not None)
        self._return_form = FormComposition.for_return(
            name, capabilities, inputs=inputs - instance_kinds, outputs=outputs
        )
        self._producers: dict[ArtifactKind[Any], str] = {
            kind: form.name for form in others for kind in form.derived
        }
        self._check_imports((*others, self._return_form))
        self._forms = self._order(others)
        self._instance_kinds = instance_kinds

    @property
    def return_form(self) -> FormComposition:
        """The form of the manifest's own selections."""
        return self._return_form

    @property
    def forms(self) -> tuple[FormComposition, ...]:
        """The forms other than the return form, in the order they run."""
        return self._forms

    def compute(self, *artifacts: Artifact[Any]) -> FormWorksheets:
        """Run every form on `artifacts`: the instances of each form and the return's inputs.

        Each form runs once per record of its instances, in `forms` order, on a worksheet of the
        record's fields and the form's imports; the return form runs last, once, on `artifacts`
        other than the instances and its imports. A DomainError from an instance is raised as
        itself with the form and the instance position at the front of its message. A kind given
        that is a form's export is refused: the forms derive it, and two values for one kind are a
        DuplicateArtifactError, as in a `Worksheet`.
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
            instances = form.instances
            assert instances is not None  # only the return form has none
            records = given[instances].value.records
            ran = tuple(
                self._run(form, position, record, store)
                for position, record in enumerate(records, start=1)
            )
            worksheets[form.name] = ran
            for export, derived in zip(form.exports, form.derived, strict=True):
                listed = [{export: worksheet.get(export).value} for worksheet in ran]
                store[derived] = Artifact(derived, RecordList(derived.fields, listed))
        rest = (artifact for kind, artifact in given.items() if kind not in self._instance_kinds)
        imported = (store[kind] for kind in self._sorted(self._return_form.imports))
        returned = self._return_form.composition.compute(*rest, *imported)
        return FormWorksheets(self._return_form.name, worksheets, returned)

    def _run(
        self,
        form: FormComposition,
        position: int,
        record: Mapping[ArtifactKind[Any], object],
        store: Mapping[ArtifactKind[Any], Artifact[Any]],
    ) -> Worksheet:
        instances = form.instances
        assert instances is not None  # only the return form has none
        starting = [Artifact(kind, record[kind]) for kind in instances.fields]
        starting += (store[kind] for kind in self._sorted(form.imports))
        try:
            return form.composition.compute(*starting)
        except DomainError as exc:
            exc.args = (f"{form.name}, instance {position}: {exc}",)
            raise

    def _check_given(self, given: Mapping[ArtifactKind[Any], Artifact[Any]]) -> None:
        derived = given.keys() & self._producers.keys()
        if derived:
            labels = self._labels(derived)
            verb = "is" if len(derived) == 1 else "are"
            raise InvalidCompositionError(f"{labels} {verb} exported by a form, not an input")
        missing = self._instance_kinds - given.keys()
        if missing:
            noun = "input" if len(missing) == 1 else "inputs"
            raise InvalidCompositionError(f"missing {noun} {self._labels(missing)}")

    @staticmethod
    def _check_names(name: str, forms: tuple[FormComposition, ...]) -> None:
        names = [name, *(form.name for form in forms)]
        for each in names:
            if names.count(each) > 1:
                raise InvalidCompositionError(f"form {each!r} is listed more than once")

    @staticmethod
    def _check_instances(
        forms: tuple[FormComposition, ...], inputs: frozenset[ArtifactKind[Any]]
    ) -> None:
        for form in forms:
            if form.instances is None:
                raise InvalidCompositionError(
                    f"form {form.name!r} is a return form, not one of the other forms"
                )
            if form.instances not in inputs:
                raise InvalidCompositionError(
                    f"form {form.name!r}: instances {form.instances.identifier!r} "
                    "is not an input of the computation"
                )

    def _check_imports(self, forms: tuple[FormComposition, ...]) -> None:
        for form in forms:
            for kind in self._sorted(form.imports):
                if kind not in self._producers:
                    raise InvalidCompositionError(
                        f"form {form.name!r}: no form exports {kind.label!r}, which it imports"
                    )

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

    @staticmethod
    def _sorted(kinds: Iterable[ArtifactKind[Any]]) -> list[ArtifactKind[Any]]:
        return sorted(kinds, key=lambda kind: kind.identifier)

    @staticmethod
    def _labels(kinds: Iterable[ArtifactKind[Any]]) -> str:
        return ", ".join(repr(label) for label in sorted({kind.label for kind in kinds}))
