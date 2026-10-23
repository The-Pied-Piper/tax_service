"""Reads jurisdictions from YAML manifest files. Implements JurisdictionSource.

The source takes a mapping of namespace -> jurisdiction package directory. A jurisdiction's
namespace is its code lower-cased (`EX-ON` -> `ex-on`). Each `*.yaml` / `*.yml` file directly in
`<roots[ex-on]>/manifests/` is one whole manifest, and each subfolder there is one manifest too,
merged from its parts: every `*.yaml` / `*.yml` file inside it (recursively), read in sorted path
order. A part may carry any of the six manifest keys or a `form:` key; the scalar keys
(`jurisdiction`, `version`, `valid_from_tax_year`) must each be in exactly one part, and the lists
(`inputs`, `outputs`, `capabilities`) are concatenated in part order, an identifier listed in two
parts of `inputs` or of `outputs` being rejected. The merged mapping then goes through the same
parse as a whole file. A manifest naming another jurisdiction is rejected.
A manifest is a flat set of forms. A part with a `form:` key (`name`, and `exports` with an optional
`instances`, all identifiers `<namespace>/<snake_case>`) gives all its `capabilities` to that
form; without `instances` the form has one instance. A part without one joins the default
form, named `<namespace>/return` and otherwise an ordinary form: its exports are the
manifest's `outputs`. A form may span parts that carry the same `form.name`, in part order:
exactly one of them declares `exports` (with its `instances`), and a second that does is rejected.
A part with a `form:` key takes no `inputs` or `outputs`: inputs are derived, exports are declared
in the `form:` block. The default form's name is reserved for the parts without a `form:` key; a
`form:` part naming it is rejected, naming the part. The default form's `outputs` are its exports,
so two with one local id (`ex/x` and `ca/x`, both `<ns>/return.x`) are rejected as "outputs".
A single manifest file is not a part and takes no `form:` key: all of it is the default form.
Each selection names a capability and fills its slots: `params` (slot -> family, optional),
`consumes` (slot -> artifact identifier, or a list of them kept in order as a tuple, optional)
and `produces` (slot -> artifact identifier, required, at least one). Slot names, and whether a
slot takes one identifier or a list, are not checked against capability classes here.
The top-level `inputs` and `outputs` list the computation's starting artifacts and the default
form's exports: both required, non-empty lists of non-empty strings without duplicates (an
identifier in both is an input carried onto the return as entered).
Parsing is strict because a manifest must stay selection plus slot bindings
(design.md §4): unknown keys, duplicate keys and wrongly typed values are
rejected with the offending file (for a folder, the offending part) named, never coerced or
ignored.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
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
from app.domain.manifest import CapabilitySelection, Form, Manifest
from app.domain.registry import Namespace

_MANIFEST_KEYS = frozenset(
    {"jurisdiction", "version", "valid_from_tax_year", "inputs", "outputs", "capabilities"}
)
_PART_KEYS = _MANIFEST_KEYS | {"form"}
_FORM_KEYS = frozenset({"name"})
_OPTIONAL_FORM_KEYS = frozenset({"instances", "exports"})
_DEFAULT_FORM = "return"
_CAPABILITY_KEYS = frozenset({"name", "produces"})
_OPTIONAL_CAPABILITY_KEYS = frozenset({"params", "consumes"})
_SCALAR_KEYS = ("jurisdiction", "version", "valid_from_tax_year")
_IDENTIFIER_LISTS = ("inputs", "outputs")
_PATTERNS = ("*.yaml", "*.yml")


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
            if (p.is_dir() and self._parts(p))
            or (p.is_file() and any(p.match(pattern) for pattern in _PATTERNS))
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
        form_selections: dict[str, list[CapabilitySelection]] = {}
        declarations: dict[str, tuple[Path, str | None, tuple[str, ...]]] = {}
        identifier_owners: dict[str, dict[str, Path]] = {key: {} for key in _IDENTIFIER_LISTS}
        for part in parts:
            contents = cls._part(part)
            if "form" in contents:
                cls._join_form(part, contents, form_selections, declarations)
            for key, node in contents.items():
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
        if form_selections:
            lists.setdefault("capabilities", [])  # the default form may have none beside the others
        try:
            return cls._manifest(
                YamlNode.root({**merged, **lists}, "manifest"),
                lambda default: tuple(
                    cls._form(name, selections, declarations, default)
                    for name, selections in form_selections.items()
                ),
            )
        except (InvalidManifestError, YamlShapeError) as exc:
            raise InvalidManifestError(f"{folder}: {exc}") from exc

    @classmethod
    def _join_form(
        cls,
        part: Path,
        contents: dict[str, YamlNode],
        form_selections: dict[str, list[CapabilitySelection]],
        declarations: dict[str, tuple[Path, str | None, tuple[str, ...]]],
    ) -> None:
        """Give the `capabilities` of a part with a `form:` key to its form, noting its declaration.

        Takes `form` and `capabilities` out of `contents`; a second part declaring the exports of
        a form is rejected, naming the part that did.
        """
        name, declared = cls._form_header(contents.pop("form"))
        if contents.keys() & set(_IDENTIFIER_LISTS):
            raise InvalidManifestError(
                f"{part}: form {name!r}: inputs are derived and exports are declared in the "
                "form: block, so the part takes no `inputs` or `outputs`"
            )
        chosen = form_selections.setdefault(name, [])
        if declared is not None:
            if name in declarations:
                raise InvalidManifestError(
                    f"{part}: form {name!r}: exports are already declared in "
                    f"{declarations[name][0]}"
                )
            declarations[name] = (part, *declared)
        if "capabilities" in contents:
            chosen.extend(cls._selection(entry) for entry in contents.pop("capabilities").items())

    @staticmethod
    def _form(
        name: str,
        selections: list[CapabilitySelection],
        declarations: dict[str, tuple[Path, str | None, tuple[str, ...]]],
        default: str,
    ) -> Form:
        """The form `name` of the selections of all its parts and its one declaration."""
        if name not in declarations:
            raise InvalidManifestError(f"form {name!r}: no part declares its exports")
        part, instances, exports = declarations[name]
        if name == default:
            raise InvalidManifestError(
                f"{part}: form {name!r}: the name is reserved for the parts without a `form:` key"
            )
        return Form(name=name, instances=instances, exports=exports, capabilities=tuple(selections))

    @classmethod
    def _form_header(cls, node: YamlNode) -> tuple[str, tuple[str | None, tuple[str, ...]] | None]:
        """The name of a part's form and, if it declares them, its instances and exports."""
        node.require_mapping(_FORM_KEYS, optional=_OPTIONAL_FORM_KEYS)
        name = node.field("name").require_non_empty_string()
        Form.check_identifier("name", name)
        instances = node.optional_field("instances")
        exports = node.optional_field("exports")
        if exports is None:
            if instances is not None:
                raise InvalidManifestError(
                    f"form {name!r}: instances must be declared with exports"
                )
            return name, None
        cls._identifiers(exports)
        listed = tuple(item.require_string() for item in exports.items())
        declared = None if instances is None else instances.require_non_empty_string()
        # Built to check the declaration; the form's selections are added when the parts merge.
        Form(name=name, instances=declared, exports=listed, capabilities=())
        return name, (declared, listed)

    @classmethod
    def _part(cls, part: Path) -> dict[str, YamlNode]:
        """The keys a part carries, each checked on its own; errors name the part."""
        try:
            doc = YamlNode.load(part, "manifest").require_mapping(frozenset(), optional=_PART_KEYS)
            contents = dict(doc.fields())
            if "form" in contents:
                cls._form_header(contents["form"])
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
    def _manifest(
        cls,
        document: YamlNode,
        forms_beside: Callable[[str], tuple[Form, ...]] = lambda _: (),
    ) -> Manifest:
        """The manifest of `document`, whose selections and `outputs` are the default form's.

        `forms_beside` gives the other forms, from the name the default form takes.
        """
        doc = document.require_mapping(_MANIFEST_KEYS)
        code = cls._code(doc.field("jurisdiction"))
        outputs = cls._identifiers(doc.field("outputs"))
        if not outputs:
            raise InvalidManifestError("outputs must name at least one artifact")
        Form.check_exports("outputs", sorted(outputs))
        default = code.namespace.identifier(_DEFAULT_FORM)
        return Manifest(
            jurisdiction=code,
            version=doc.field("version").require_integer(),
            valid_from_tax_year=doc.field("valid_from_tax_year").require_integer(),
            inputs=cls._identifiers(doc.field("inputs")),
            forms=(
                Form(
                    name=default,
                    instances=None,
                    exports=tuple(sorted(outputs)),
                    capabilities=tuple(
                        cls._selection(entry) for entry in doc.field("capabilities").items()
                    ),
                ),
                *forms_beside(default),
            ),
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
