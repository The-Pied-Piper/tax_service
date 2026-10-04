"""Reads parameter datasets from YAML files. Implements ParameterSource.

A dataset for family `ca-on/brackets` and tax year 2025 lives at
`<directory>/ca-on/brackets/2025.yaml`. Every file has the same envelope
(family, tax_year, kind, sources, rounding) plus keys specific to its kind,
which that kind's parser reads. The file must declare the family, year and kind
that were asked for. An absent file is NotFoundError: a year is never carried
forward. Decimals are YAML strings ("0.145") so they never pass through float.
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import yaml

from app.adapters.outbound.parameter_parsers import DEFAULT_PARSERS, ParameterParser
from app.adapters.outbound.yaml_support import YamlNode, YamlShapeError
from app.domain.errors import DomainError, InvalidParameterDataError, NotFoundError
from app.domain.parameters.datasets import ParameterDataset
from app.domain.parameters.kind import ParameterKind
from app.domain.parameters.rounding import NO_ROUNDING, RoundingMode, RoundingRule, RoundTo

_FAMILY = re.compile(r"[a-z0-9]+([_-][a-z0-9]+)*(/[a-z0-9]+([_-][a-z0-9]+)*)+")
_ENVELOPE_KEYS = frozenset({"family", "tax_year", "kind", "sources", "rounding"})
_ROUNDING_KEYS = frozenset({"increment", "mode"})


class YamlParameterSource:
    def __init__(
        self, directory: Path, parsers: Sequence[ParameterParser[Any]] = DEFAULT_PARSERS
    ) -> None:
        self._directory = directory
        self._parsers: dict[str, ParameterParser[Any]] = {}
        for parser in parsers:
            if parser.kind.name in self._parsers:
                raise ValueError(f"two parsers for parameter kind {parser.kind.name!r}")
            self._parsers[parser.kind.name] = parser

    def get[T](self, family: str, tax_year: int, kind: ParameterKind[T]) -> ParameterDataset[T]:
        """Read `<directory>/<family>/<tax_year>.yaml` and parse it with the parser for `kind`.

        The file must declare the same family, year and kind; see ParameterSource.get for errors.
        """
        parser = self._parsers.get(kind.name)
        if parser is None or parser.kind != kind:
            raise LookupError(f"no parser for parameter kind {kind.name!r}")
        path = self._path(family, tax_year)
        try:
            document = YamlNode.load(path, "dataset")
            declared_kind = document.field("kind").require_string()
        except (OSError, yaml.YAMLError, YamlShapeError) as exc:
            raise InvalidParameterDataError(f"{path}: {exc}") from exc
        if declared_kind != kind.name:
            raise InvalidParameterDataError(
                f"{path}: kind {declared_kind!r} does not match the requested {kind.name!r}"
            )
        try:
            doc = document.require_mapping(_ENVELOPE_KEYS | parser.body_keys)
            self._check_identity(doc, family, tax_year)
            return ParameterDataset(
                family=family,
                tax_year=tax_year,
                kind=kind,
                values=parser.parse(doc),
                rounding=self._rounding(doc.field("rounding")),
                sources=self._sources(doc.field("sources")),
            )
        except (YamlShapeError, DomainError) as exc:
            raise InvalidParameterDataError(f"{path}: {exc}") from exc

    def _path(self, family: str, tax_year: int) -> Path:
        if not _FAMILY.fullmatch(family):
            raise ValueError(f"invalid parameter family {family!r}: expected e.g. 'ca-on/brackets'")
        path = self._directory / family / f"{tax_year}.yaml"
        if not path.is_file():
            raise NotFoundError(
                f"no {family} dataset for tax year {tax_year} (expected {path}); "
                "an absent year is never carried forward"
            )
        return path

    @staticmethod
    def _check_identity(doc: YamlNode, family: str, tax_year: int) -> None:
        declared_family = doc.field("family").require_string()
        if declared_family != family:
            raise YamlShapeError(f"family {declared_family!r} does not match {family!r}")
        declared_year = doc.field("tax_year").require_integer()
        if declared_year != tax_year:
            raise YamlShapeError(f"tax_year {declared_year} does not match {tax_year}")

    @staticmethod
    def _rounding(node: YamlNode) -> RoundingRule:
        if node.value == "none":
            return NO_ROUNDING
        if not isinstance(node.value, dict):
            raise YamlShapeError("rounding must be 'none' or a mapping of increment and mode")
        fields = node.require_mapping(_ROUNDING_KEYS)
        mode_name = fields.field("mode").require_string()
        modes = {mode.value: mode for mode in RoundingMode}
        if mode_name not in modes:
            raise YamlShapeError(f"rounding.mode {mode_name!r} is not one of {sorted(modes)}")
        return RoundTo(increment=fields.field("increment").parse_decimal(), mode=modes[mode_name])

    @staticmethod
    def _sources(node: YamlNode) -> tuple[str, ...]:
        entries = node.items()
        if not entries:
            raise YamlShapeError("sources must list at least one source")
        return tuple(entry.require_string() for entry in entries)
