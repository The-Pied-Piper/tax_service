"""Reads jurisdictions from YAML manifest files. Implements JurisdictionSource.

The source takes a mapping of namespace -> jurisdiction package directory. A jurisdiction's
namespace is its code lower-cased (`EX-ON` -> `ex-on`), and every `*.yaml` / `*.yml` file under
`<roots[ex-on]>/manifests/` (recursively) is one of its manifests; a manifest there naming
another jurisdiction is rejected.
Parsing is strict because a manifest must stay selection plus parameters
(design.md §4): unknown keys, duplicate keys and wrongly typed values are
rejected with the offending file named, never coerced or ignored.
"""

from __future__ import annotations

from collections.abc import Mapping
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
from app.domain.registry import Namespace

_MANIFEST_KEYS = frozenset({"jurisdiction", "version", "valid_from_tax_year", "capabilities"})
_CAPABILITY_KEYS = frozenset({"name", "params_family"})


class YamlJurisdictionSource:
    """Jurisdictions read from the `manifests/` directory of each jurisdiction package."""

    def __init__(self, roots: Mapping[Namespace, Path]) -> None:
        """Read manifests under each namespace's package directory in `roots`."""
        self._roots = dict(roots)

    def get_jurisdiction(self, code: JurisdictionCode) -> Jurisdiction:
        """The jurisdiction with every manifest in its package; see JurisdictionSource."""
        manifests = tuple(self._load_all(code))
        if not manifests:
            raise NotFoundError(f"no manifests for jurisdiction {code} in {self._manifests(code)}")
        return Jurisdiction(code=code, manifests=manifests)

    def _load_all(self, code: JurisdictionCode) -> list[Manifest]:
        manifests = self._manifests(code)
        if not manifests.parent.is_dir():
            raise InvalidManifestError(f"package directory not found: {manifests.parent}")
        if not manifests.is_dir():
            return []
        paths = sorted(p for pattern in ("*.yaml", "*.yml") for p in manifests.rglob(pattern))
        return [self._load_for(code, path) for path in paths]

    def _manifests(self, code: JurisdictionCode) -> Path:
        namespace = code.namespace
        if namespace not in self._roots:
            raise NotFoundError(
                f"no jurisdiction {code}: no jurisdiction package declares namespace "
                f"{namespace.name!r}"
            )
        return self._roots[namespace] / "manifests"

    @classmethod
    def _load_for(cls, code: JurisdictionCode, path: Path) -> Manifest:
        manifest = cls.load(path)
        if manifest.jurisdiction != code:
            raise InvalidManifestError(
                f"{path}: manifest is for {manifest.jurisdiction}, but its package is {code}'s"
            )
        return manifest

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
