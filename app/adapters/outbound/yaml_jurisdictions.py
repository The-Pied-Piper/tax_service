"""Reads jurisdictions from YAML manifest files. Implements JurisdictionSource.

The source takes a mapping of namespace -> jurisdiction package directory. A jurisdiction's
namespace is its code lower-cased (`EX-ON` -> `ex-on`). Each `*.yaml` / `*.yml` file directly in
`<roots[ex-on]>/manifests/` is one whole manifest, and each subfolder there is one manifest too,
merged from its parts: every `*.yaml` / `*.yml` file inside it (recursively), read in sorted path
order. A part may carry any of the six manifest keys; the scalar keys (`jurisdiction`, `version`,
`valid_from_tax_year`) must each be in exactly one part, and the lists (`inputs`, `outputs`,
`capabilities`) are concatenated in part order, an identifier listed in two parts of `inputs` or of
`outputs` being rejected. The merged mapping then goes through the same parse as a whole file. A
manifest naming another jurisdiction is rejected.
Each selection names a capability and fills its slots: `params` (slot -> family, optional),
`consumes` (slot -> artifact identifier, or a list of them kept in order as a tuple, optional)
and `produces` (slot -> artifact identifier, required, at least one). Slot names, and whether a
slot takes one identifier or a list, are not checked against capability classes here.
The top-level `inputs` and `outputs` list the computation's artifact identifiers: both required,
non-empty lists of non-empty strings without duplicates, and no identifier in both.
Parsing is strict because a manifest must stay selection plus slot bindings
(design.md §4): unknown keys, duplicate keys and wrongly typed values are
rejected with the offending file (for a folder, the offending part) named, never coerced or
ignored.
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

_MANIFEST_KEYS = frozenset(
    {"jurisdiction", "version", "valid_from_tax_year", "inputs", "outputs", "capabilities"}
)
_CAPABILITY_KEYS = frozenset({"name", "produces"})
_OPTIONAL_CAPABILITY_KEYS = frozenset({"params", "consumes"})
_SCALAR_KEYS = ("jurisdiction", "version", "valid_from_tax_year")
_IDENTIFIER_LISTS = ("inputs", "outputs")
_PATTERNS = ("*.yaml", "*.yml")
_SUFFIXES = frozenset({".yaml", ".yml"})


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
        paths = sorted(
            p
            for p in manifests.iterdir()
            if (p.is_dir() and self._parts(p)) or (p.is_file() and p.suffix in _SUFFIXES)
        )
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
        """The manifest in the file `path`, or merged from the parts in the folder `path`."""
        if path.is_dir():
            return cls._load_folder(path)
        try:
            document = YamlNode.load(path, "manifest")
        except (OSError, yaml.YAMLError) as exc:
            raise InvalidManifestError(f"{path}: {exc}") from exc
        try:
            return cls._manifest(document)
        except (InvalidManifestError, YamlShapeError) as exc:
            raise InvalidManifestError(f"{path}: {exc}") from exc

    @staticmethod
    def _parts(folder: Path) -> list[Path]:
        """The `*.yaml` / `*.yml` files under `folder`, in sorted path order."""
        return sorted(p for pattern in _PATTERNS for p in folder.rglob(pattern) if p.is_file())

    @classmethod
    def _load_folder(cls, folder: Path) -> Manifest:
        parts = cls._parts(folder)
        merged: dict[str, object] = {}
        scalar_owners: dict[str, Path] = {}
        lists: dict[str, list[object]] = {}
        identifier_owners: dict[str, dict[str, Path]] = {key: {} for key in _IDENTIFIER_LISTS}
        for part in parts:
            for key, node in cls._part(part).items():
                if key in _SCALAR_KEYS:
                    if key in scalar_owners:
                        raise InvalidManifestError(
                            f"{part}: key {key!r} is already set in {scalar_owners[key]}"
                        )
                    scalar_owners[key] = part
                    merged[key] = node.value
                else:
                    cls._claim_identifiers(key, node, part, identifier_owners.get(key, {}))
                    lists.setdefault(key, []).extend(item.value for item in node.items())
        try:
            return cls._manifest(YamlNode.root({**merged, **lists}, "manifest"))
        except (InvalidManifestError, YamlShapeError) as exc:
            raise InvalidManifestError(f"{folder}: {exc}") from exc

    @classmethod
    def _part(cls, part: Path) -> dict[str, YamlNode]:
        """The keys a part carries, each checked on its own; errors name the part."""
        try:
            doc = YamlNode.load(part, "manifest").require_mapping(
                frozenset(), optional=_MANIFEST_KEYS
            )
            contents = dict(doc.fields())
            if "jurisdiction" in contents:
                cls._code(contents["jurisdiction"])
            for key in ("version", "valid_from_tax_year"):
                if key in contents:
                    contents[key].require_integer()
            for key in _IDENTIFIER_LISTS:
                if key in contents:
                    cls._identifiers(contents[key])
            if "capabilities" in contents:
                for entry in contents["capabilities"].items():
                    cls._selection(entry)
        except (OSError, yaml.YAMLError, InvalidManifestError, YamlShapeError) as exc:
            raise InvalidManifestError(f"{part}: {exc}") from exc
        return contents

    @staticmethod
    def _claim_identifiers(key: str, node: YamlNode, part: Path, owners: dict[str, Path]) -> None:
        """Record the part's identifiers under `key`, refusing one an earlier part listed."""
        if key not in _IDENTIFIER_LISTS:
            return
        for index, item in enumerate(node.items()):
            identifier = item.require_string()
            if identifier in owners:
                raise InvalidManifestError(
                    f"{part}: {key}[{index}]: {identifier!r} is already listed in "
                    f"{owners[identifier]}"
                )
            owners[identifier] = part

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
            inputs=cls._identifiers(doc.field("inputs")),
            outputs=cls._identifiers(doc.field("outputs")),
        )

    @staticmethod
    def _identifiers(node: YamlNode) -> frozenset[str]:
        """A list of non-empty identifiers, none repeated; an empty list is Manifest's check."""
        identifiers: set[str] = set()
        for item in node.items():
            identifier = item.require_string()
            if not identifier:
                raise YamlShapeError(f"{item.where} must not be empty")
            if identifier in identifiers:
                raise YamlShapeError(f"{item.where}: {identifier!r} is listed more than once")
            identifiers.add(identifier)
        return frozenset(identifiers)

    @classmethod
    def _selection(cls, entry: YamlNode) -> CapabilitySelection:
        fields = entry.require_mapping(_CAPABILITY_KEYS, optional=_OPTIONAL_CAPABILITY_KEYS)
        return CapabilitySelection(
            name=fields.field("name").require_string(),
            params=cls._bindings(fields.optional_field("params")),
            consumes=cls._consumed(fields.optional_field("consumes")),
            produces=cls._produced(fields.field("produces")),
        )

    @classmethod
    def _produced(cls, node: YamlNode) -> dict[str, str]:
        bindings = cls._bindings(node)
        if not bindings:
            raise YamlShapeError(f"{node.where} must name at least one slot")
        return bindings

    @staticmethod
    def _bindings(node: YamlNode | None) -> dict[str, str]:
        return {} if node is None else node.string_mapping()

    @classmethod
    def _consumed(cls, node: YamlNode | None) -> dict[str, str | tuple[str, ...]]:
        """Consumed slots, each bound to one identifier or to a list of them, in order."""
        if node is None:
            return {}
        return {slot: cls._identifier_or_list(value) for slot, value in node.fields()}

    @staticmethod
    def _identifier_or_list(node: YamlNode) -> str | tuple[str, ...]:
        """A non-empty identifier, or a list of them as a tuple; repeats are the builder's check."""
        if node.is_list():
            return tuple(item.require_non_empty_string() for item in node.items())
        if not isinstance(node.value, str):
            raise YamlShapeError(
                f"{node.where} must be a string or a list of strings, "
                f"got {type(node.value).__name__}"
            )
        return node.require_non_empty_string()

    @staticmethod
    def _code(node: YamlNode) -> JurisdictionCode:
        try:
            return JurisdictionCode(node.require_string())
        except InvalidJurisdictionCodeError as exc:
            raise InvalidManifestError(f"{node.where}: {exc}") from exc
