"""Reads jurisdictions from YAML manifest files. Implements JurisdictionSource.

Every `*.yaml` / `*.yml` file under the directory (recursively) is one manifest;
a jurisdiction is every manifest whose `jurisdiction` field names it.
Parsing is strict because a manifest must stay selection plus parameters
(design.md §4): unknown keys, duplicate keys and wrongly typed values are
rejected with the offending file named, never coerced or ignored.
"""

from __future__ import annotations

from collections.abc import Hashable
from pathlib import Path
from typing import Any

import yaml
from yaml.constructor import ConstructorError
from yaml.nodes import MappingNode

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


class _StrictLoader(yaml.SafeLoader):
    """SafeLoader that rejects duplicate mapping keys instead of keeping the last one."""

    def construct_mapping(self, node: MappingNode, deep: bool = False) -> dict[Hashable, Any]:
        seen: set[Any] = set()
        for key_node, _ in node.value:
            key = self.construct_object(key_node, deep=deep)
            if key in seen:
                raise ConstructorError(None, None, f"duplicate key {key!r}", key_node.start_mark)
            seen.add(key)
        return super().construct_mapping(node, deep=deep)


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
            document = yaml.load(path.read_text(encoding="utf-8"), Loader=_StrictLoader)
        except (OSError, yaml.YAMLError) as exc:
            raise InvalidManifestError(f"{path}: {exc}") from exc
        try:
            return _to_manifest(document)
        except InvalidManifestError as exc:
            raise InvalidManifestError(f"{path}: {exc}") from exc


def _to_manifest(document: object) -> Manifest:
    doc = _mapping(document, "manifest", _MANIFEST_KEYS)
    entries = doc["capabilities"]
    if not isinstance(entries, list):
        raise InvalidManifestError("capabilities must be a list")
    return Manifest(
        jurisdiction=_code(doc["jurisdiction"], "jurisdiction"),
        version=_int(doc["version"], "version"),
        valid_from_tax_year=_int(doc["valid_from_tax_year"], "valid_from_tax_year"),
        capabilities=tuple(
            _to_selection(entry, f"capabilities[{i}]") for i, entry in enumerate(entries)
        ),
    )


def _to_selection(entry: object, where: str) -> CapabilitySelection:
    fields = _mapping(entry, where, _CAPABILITY_KEYS)
    return CapabilitySelection(
        name=_str(fields["name"], f"{where}.name"),
        params_family=_str(fields["params_family"], f"{where}.params_family"),
    )


def _mapping(value: object, where: str, keys: frozenset[str]) -> dict[str, object]:
    if not isinstance(value, dict):
        raise InvalidManifestError(f"{where} must be a mapping")
    unknown = set(value) - keys
    if unknown:
        raise InvalidManifestError(f"{where}: unknown keys {sorted(map(str, unknown))}")
    missing = keys - set(value)
    if missing:
        raise InvalidManifestError(f"{where}: missing keys {sorted(missing)}")
    return value


def _str(value: object, where: str) -> str:
    if not isinstance(value, str):
        raise InvalidManifestError(f"{where} must be a string, got {type(value).__name__}")
    return value


def _code(value: object, where: str) -> JurisdictionCode:
    try:
        return JurisdictionCode(_str(value, where))
    except InvalidJurisdictionCodeError as exc:
        raise InvalidManifestError(f"{where}: {exc}") from exc


def _int(value: object, where: str) -> int:
    # bool is an int subclass; `version: yes` must not become 1.
    if not isinstance(value, int) or isinstance(value, bool):
        raise InvalidManifestError(f"{where} must be an integer, got {type(value).__name__}")
    return value
