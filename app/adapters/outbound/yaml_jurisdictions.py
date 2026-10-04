"""Reads jurisdictions from YAML manifest files. Implements JurisdictionSource.

Every `*.yaml` / `*.yml` file under the directory (recursively) is one manifest;
a jurisdiction is every manifest whose `jurisdiction` field names it.
Parsing is strict because a manifest must stay selection plus parameters
(design.md §4): unknown keys, duplicate keys and wrongly typed values are
rejected with the offending file named, never coerced or ignored.
"""

from __future__ import annotations

from pathlib import Path

import yaml

from app.adapters.outbound import yaml_support as y
from app.adapters.outbound.yaml_support import YamlShapeError
from app.domain.errors import (
    InvalidJurisdictionCodeError,
    InvalidManifestError,
    NotFoundError,
)
from app.domain.jurisdiction import Jurisdiction
from app.domain.jurisdiction_code import JurisdictionCode
from app.domain.manifest import CapabilitySelection, Manifest

_MANIFEST_KEYS = frozenset({"jurisdiction", "version", "valid_from_tax_year", "capabilities"})
_CAPABILITY_KEYS = frozenset({"name", "params_family"})


class YamlJurisdictionSource:
    def __init__(self, directory: Path) -> None:
        self._directory = directory

    def get_jurisdiction(self, code: JurisdictionCode) -> Jurisdiction:
        manifests = tuple(m for m in self.load_all() if m.jurisdiction == code)
        if not manifests:
            raise NotFoundError(f"no manifests for jurisdiction {code} in {self._directory}")
        return Jurisdiction(code=code, manifests=manifests)

    def load_all(self) -> list[Manifest]:
        if not self._directory.is_dir():
            raise InvalidManifestError(f"manifest directory not found: {self._directory}")
        paths = sorted(p for pattern in ("*.yaml", "*.yml") for p in self._directory.rglob(pattern))
        return [self.load(path) for path in paths]

    @staticmethod
    def load(path: Path) -> Manifest:
        try:
            document = y.load(path)
        except (OSError, yaml.YAMLError) as exc:
            raise InvalidManifestError(f"{path}: {exc}") from exc
        try:
            return _to_manifest(document)
        except (InvalidManifestError, YamlShapeError) as exc:
            raise InvalidManifestError(f"{path}: {exc}") from exc


def _to_manifest(document: object) -> Manifest:
    doc = y.mapping(document, "manifest", _MANIFEST_KEYS)
    entries = y.sequence(doc["capabilities"], "capabilities")
    return Manifest(
        jurisdiction=_code(doc["jurisdiction"], "jurisdiction"),
        version=y.integer(doc["version"], "version"),
        valid_from_tax_year=y.integer(doc["valid_from_tax_year"], "valid_from_tax_year"),
        capabilities=tuple(
            _to_selection(entry, f"capabilities[{i}]") for i, entry in enumerate(entries)
        ),
    )


def _to_selection(entry: object, where: str) -> CapabilitySelection:
    fields = y.mapping(entry, where, _CAPABILITY_KEYS)
    return CapabilitySelection(
        name=y.string(fields["name"], f"{where}.name"),
        params_family=y.string(fields["params_family"], f"{where}.params_family"),
    )


def _code(value: object, where: str) -> JurisdictionCode:
    try:
        return JurisdictionCode(y.string(value, where))
    except InvalidJurisdictionCodeError as exc:
        raise InvalidManifestError(f"{where}: {exc}") from exc
