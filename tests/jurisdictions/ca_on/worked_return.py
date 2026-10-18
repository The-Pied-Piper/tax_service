"""Worked returns: human-reviewed YAML files of a return's inputs and expected lines.

A file under `returns/` names its `jurisdiction` and `tax_year`, describes the taxpayer, lists
the `sources` its figures were checked against, and maps artifact identifiers to amounts (quoted
decimal strings) under `inputs` and `expected`; a count (an `int` kind) is a plain YAML integer
and appears only under `inputs`. `WorkedReturn.load` checks that shape and
resolves each identifier through an artifact registry; every failure is a WorkedReturnError
naming the file and the key.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any

import yaml

from app.adapters.outbound.yaml_support import YamlNode, YamlShapeError
from app.domain.artifact import Artifact, ArtifactRegistry
from app.domain.errors import (
    InvalidJurisdictionCodeError,
    InvalidRegistrationError,
    UnknownRegistrationError,
)
from app.domain.jurisdiction_code import JurisdictionCode

_SECTIONS = frozenset({"jurisdiction", "tax_year", "description", "sources", "inputs", "expected"})


class WorkedReturnError(ValueError):
    """A worked-return file is malformed or does not cover what its manifest declares."""


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
                inputs=cls._artifacts(root.field("inputs"), artifacts, counts=True),
                expected=cls._artifacts(root.field("expected"), artifacts, counts=False),
            )
        except (YamlShapeError, yaml.YAMLError) as exc:
            raise WorkedReturnError(f"{path}: {exc}") from None

    def require_outputs(self, outputs: frozenset[str]) -> None:
        """Check `expected` lists every one of `outputs`, the identifiers the manifest declares.

        Raises WorkedReturnError naming the file and the missing outputs.
        """
        missing = outputs - {artifact.kind.identifier for artifact in self.expected}
        if missing:
            raise WorkedReturnError(
                f"{self.path}: expected: missing declared outputs {sorted(missing)}"
            )

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
    def _artifacts(
        node: YamlNode, artifacts: ArtifactRegistry, *, counts: bool
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
            elif counts and kind.value_type is int:
                result.append(Artifact(kind, value.require_integer()))
            else:
                accepted = "an amount or a count" if counts else "an amount"
                raise YamlShapeError(
                    f"{value.where}: {identifier!r} holds a {kind.value_type.__name__}, "
                    f"not {accepted}"
                )
        return tuple(result)
