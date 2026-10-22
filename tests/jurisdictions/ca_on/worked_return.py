"""Worked returns: human-reviewed YAML files of a return's inputs and expected lines.

A file under `returns/` names its `jurisdiction` and `tax_year`, describes the taxpayer, lists
the `sources` its figures were checked against, and maps artifact identifiers to figures under
`inputs` and `expected`. Every figure is a quoted string, so YAML never reads it as a number: an
amount is a decimal string, and a count (an `int` kind, under `inputs` or `expected`) is a string
of decimal digits with no sign and no leading zero, such as "0" or "3". A record list (under
`inputs`, or under `expected` for a line the return produces as a list, such as T776 Area A's
closing UCC) is a list of mappings, one per record in order, each keyed by its fields'
identifiers with figures spelled as above; `[]` is no records. A rate (a `Rate` kind, only under
`expected`) is a quoted decimal from 0 to 1, such as "0.55". Digits (a digits kind, under
`inputs` or `expected`, as a carried entry is listed under both) are quoted text kept as
entered, such as "012345678", or `""` for a box left blank. `WorkedReturn.load` checks that
shape and resolves each identifier through an artifact registry; every failure is a
WorkedReturnError naming the file and the key, except a value its kind refuses, such as a
negative amount, a rate above 1 or digits of the wrong length, which is the kind's own error.
A line or input the file leaves out is blank: `with_blanks` fills it in against the manifest's
declared inputs and outputs (a record list left out is no records, as an input and as an
expected line).
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, replace
from decimal import Decimal
from pathlib import Path
from typing import Any

import yaml

from app.adapters.outbound.yaml_support import YamlNode, YamlShapeError
from app.domain.artifact import Artifact, ArtifactKind, ArtifactRegistry
from app.domain.digits import DigitsKind
from app.domain.errors import (
    InvalidJurisdictionCodeError,
    InvalidRegistrationError,
    UnknownRegistrationError,
)
from app.domain.jurisdiction_code import JurisdictionCode
from app.domain.manifest import Form
from app.domain.parameters.rate import Rate
from app.domain.record_list import RecordList, RecordListKind

_SECTIONS = frozenset({"jurisdiction", "tax_year", "description", "sources", "inputs", "expected"})


class WorkedReturnError(ValueError):
    """A worked-return file is malformed or names something its manifest cannot leave blank."""


@dataclass(frozen=True)
class WorkedReturn:
    """One worked return read from `path`: its starting artifacts and the lines it expects."""

    path: Path
    jurisdiction: JurisdictionCode
    tax_year: int
    description: str
    sources: tuple[str, ...]
    inputs: tuple[Artifact[Any], ...]
    expected: tuple[Artifact[Any], ...]

    @classmethod
    def discover(cls, directory: Path) -> tuple[Path, ...]:
        """Every `*.yaml` file directly in `directory`, in name order."""
        return tuple(sorted(directory.glob("*.yaml")))

    @classmethod
    def load(cls, path: Path, artifacts: ArtifactRegistry) -> WorkedReturn:
        """Read the worked return at `path`, resolving its identifiers through `artifacts`.

        Raises WorkedReturnError naming the file and the offending key.
        """
        try:
            root = YamlNode.load(path, path.name).require_mapping(_SECTIONS)
            return cls(
                path=path,
                jurisdiction=cls._jurisdiction(root.field("jurisdiction")),
                tax_year=root.field("tax_year").require_integer(),
                description=root.field("description").require_non_empty_string(),
                sources=cls._sources(root.field("sources")),
                inputs=cls._artifacts(root.field("inputs"), artifacts, inputs=True),
                expected=cls._artifacts(root.field("expected"), artifacts, inputs=False),
            )
        except (YamlShapeError, yaml.YAMLError) as exc:
            raise WorkedReturnError(f"{path}: {exc}") from None

    def with_blanks(
        self, inputs: frozenset[str], outputs: frozenset[str], artifacts: ArtifactRegistry
    ) -> WorkedReturn:
        """This return with every blank line of the form filled in, as the filer left it blank.

        `inputs` and `outputs` are the identifiers the manifest declares. A declared input the
        file leaves out is entered as blank: 0 for an amount or a count, no records for a record
        list, the empty text for digits. A declared output the file leaves out is expected to be
        0, or the empty text for digits, so a line that fires on a return not meant to trigger it
        still fails. Raises WorkedReturnError naming the file and the identifier for one
        `artifacts` does not know or that holds no blank.
        """
        given = {artifact.kind.identifier for artifact in self.inputs}
        listed = {artifact.kind.identifier for artifact in self.expected}
        return replace(
            self,
            inputs=self.inputs + self._blanks(sorted(inputs - given), "inputs", artifacts),
            expected=self.expected + self._blanks(sorted(outputs - listed), "expected", artifacts),
        )

    def with_forms(self, forms: Iterable[Form], artifacts: ArtifactRegistry) -> WorkedReturn:
        """This return with the flat inputs of each form turned into its instances artifact.

        Temporary test support: a worked return gives a form's instance inputs flat at the top
        level of `inputs:`, while the engine takes only the instances shape. The flat inputs that
        are fields of the form's instances kind become the one record of that artifact, the fields
        the file leaves out blank as in `with_blanks`; with none of them in the file the artifact
        is an empty list. An instances artifact the file already gives is kept as it is. Raises
        WorkedReturnError naming the file for an instances identifier that is not a record list.
        """
        inputs = self.inputs
        for form in forms:
            kind = self._instances_kind(form, artifacts)
            if any(artifact.kind == kind for artifact in inputs):
                continue
            flat = [artifact for artifact in inputs if artifact.kind in kind.fields]
            inputs = tuple(artifact for artifact in inputs if artifact not in flat)
            record: dict[ArtifactKind[Any], object] = {a.kind: a.value for a in flat}
            if flat:
                missing = [field.identifier for field in kind.fields if field not in record]
                record.update({a.kind: a.value for a in self._blanks(missing, "inputs", artifacts)})
            instances = RecordList(kind.fields, [record] if flat else [])
            inputs += (Artifact(kind, instances),)
        return replace(self, inputs=inputs)

    def _instances_kind(self, form: Form, artifacts: ArtifactRegistry) -> RecordListKind:
        try:
            kind = artifacts.kind(form.instances)
        except (UnknownRegistrationError, InvalidRegistrationError) as exc:
            raise WorkedReturnError(
                f"{self.path}: form {form.name!r}: unknown instances {form.instances!r} ({exc})"
            ) from None
        if not isinstance(kind, RecordListKind):
            raise WorkedReturnError(
                f"{self.path}: form {form.name!r}: instances {form.instances!r} "
                "is not a record list"
            )
        return kind

    def _blanks(
        self, identifiers: list[str], section: str, artifacts: ArtifactRegistry
    ) -> tuple[Artifact[Any], ...]:
        result: list[Artifact[Any]] = []
        for identifier in identifiers:
            try:
                kind = artifacts.kind(identifier)
            except (UnknownRegistrationError, InvalidRegistrationError) as exc:
                raise WorkedReturnError(
                    f"{self.path}: {section}: unknown artifact identifier {identifier!r} ({exc})"
                ) from None
            if kind.value_type is Decimal:
                result.append(Artifact(kind, Decimal(0)))
            elif kind.value_type is int:
                result.append(Artifact(kind, 0))
            elif isinstance(kind, RecordListKind):
                result.append(Artifact(kind, RecordList(kind.fields, [])))
            elif isinstance(kind, DigitsKind):
                result.append(Artifact(kind, ""))
            else:
                raise WorkedReturnError(
                    f"{self.path}: {section}: {identifier!r} holds a "
                    f"{kind.value_type.__name__}, which has no blank"
                )
        return tuple(result)

    @staticmethod
    def _jurisdiction(node: YamlNode) -> JurisdictionCode:
        try:
            return JurisdictionCode(node.require_non_empty_string())
        except InvalidJurisdictionCodeError as exc:
            raise YamlShapeError(f"{node.where}: {exc}") from None

    @staticmethod
    def _sources(node: YamlNode) -> tuple[str, ...]:
        sources = tuple(item.require_non_empty_string() for item in node.items())
        if not sources:
            raise YamlShapeError(f"{node.where} must not be empty")
        return sources

    @staticmethod
    def _count(node: YamlNode) -> int:
        text = node.require_string()
        try:
            return node.parse_whole_number()
        except YamlShapeError:
            raise YamlShapeError(f"{node.where} is not a count: {text!r}") from None

    @staticmethod
    def _records(node: YamlNode, kind: RecordListKind) -> RecordList:
        """`node` read as a list of records of `kind`'s fields; a nested list reads the same."""
        keys = frozenset(field.identifier for field in kind.fields)
        records: list[dict[ArtifactKind[Any], Decimal | int | RecordList]] = []
        for item in node.items():
            item.require_mapping(keys)
            record: dict[ArtifactKind[Any], Decimal | int | RecordList] = {}
            for field in kind.fields:
                value = item.field(field.identifier)
                if isinstance(field, RecordListKind):
                    record[field] = WorkedReturn._records(value, field)
                elif field.value_type is int:
                    record[field] = WorkedReturn._count(value)
                else:
                    record[field] = value.parse_decimal()
            records.append(record)
        return RecordList(kind.fields, records)

    @staticmethod
    def _artifacts(
        node: YamlNode, artifacts: ArtifactRegistry, *, inputs: bool
    ) -> tuple[Artifact[Any], ...]:
        fields = node.fields()
        if not fields:
            raise YamlShapeError(f"{node.where} must not be empty")
        result: list[Artifact[Any]] = []
        for identifier, value in fields:
            try:
                kind = artifacts.kind(identifier)
            except (UnknownRegistrationError, InvalidRegistrationError) as exc:
                raise YamlShapeError(
                    f"{value.where}: unknown artifact identifier {identifier!r} ({exc})"
                ) from None
            if kind.value_type is Decimal:
                result.append(Artifact(kind, value.parse_decimal()))
            elif kind.value_type is int:
                result.append(Artifact(kind, WorkedReturn._count(value)))
            elif isinstance(kind, RecordListKind):
                result.append(Artifact(kind, WorkedReturn._records(value, kind)))
            elif isinstance(kind, DigitsKind):
                result.append(Artifact(kind, value.require_string()))
            elif not inputs and kind.value_type is Rate:
                result.append(Artifact(kind, Rate(value.parse_decimal())))
            else:
                accepted = (
                    "an amount, a count, a record list or digits"
                    if inputs
                    else "an amount, a count, a record list, a rate or digits"
                )
                raise YamlShapeError(
                    f"{value.where}: {identifier!r} holds a {kind.value_type.__name__}, "
                    f"not {accepted}"
                )
        return tuple(result)
