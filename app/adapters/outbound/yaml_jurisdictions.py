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

from app.adapters.outbound.yaml_support import YamlNode, YamlShapeError
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

    @classmethod
    def load(cls, path: Path) -> Manifest:
        try:
            document = YamlNode.load(path, "manifest")
        except (OSError, yaml.YAMLError) as exc:
            raise InvalidManifestError(f"{path}: {exc}") from exc
        try:
            return cls._manifest(document)
        except (InvalidManifestError, YamlShapeError) as exc:
            raise InvalidManifestError(f"{path}: {exc}") from exc

    @classmethod
    def _manifest(cls, document: YamlNode) -> Manifest:
        doc = document.require_mapping(_MANIFEST_KEYS)
        return Manifest(
            jurisdiction=cls._code(doc.field("jurisdiction")),
            version=doc.field("version").require_integer(),
            valid_from_tax_year=doc.field("valid_from_tax_year").require_integer(),
            capabilities=tuple(
                cls._selection(entry) for entry in doc.field("capabilities").items()
            ),
        )

    @staticmethod
    def _selection(entry: YamlNode) -> CapabilitySelection:
        fields = entry.require_mapping(_CAPABILITY_KEYS)
        return CapabilitySelection(
            name=fields.field("name").require_string(),
            params_family=fields.field("params_family").require_string(),
        )

    @staticmethod
    def _code(node: YamlNode) -> JurisdictionCode:
        try:
            return JurisdictionCode(node.require_string())
        except InvalidJurisdictionCodeError as exc:
            raise InvalidManifestError(f"{node.where}: {exc}") from exc
