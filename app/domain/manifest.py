"""Jurisdiction manifest: which capabilities run for a jurisdiction, and from which tax year.

A manifest selects capabilities and fills their slots (design.md §4): parameter slots with
families, artifact slots with artifact identifiers. The slots themselves are declared in code.
A manifest also declares the computation's inputs and outputs by artifact identifier; an
identifier in both is carried onto the return as entered.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType

from app.domain.errors import InvalidManifestError, InvalidRegistrationError
from app.domain.jurisdiction_code import JurisdictionCode
from app.domain.registry import Namespace


@dataclass(frozen=True, slots=True)
class CapabilitySelection:
    """One capability chosen by a manifest, with its slots filled by identifier.

    `params` maps parameter slots to families; `consumes` and `produces` map artifact slots to
    artifact identifiers, and a consumed slot may instead map to a list of identifiers, kept in
    order as a tuple. Each is kept as a read-only copy of what it was given.
    """

    name: str
    params: Mapping[str, str]
    consumes: Mapping[str, str | tuple[str, ...]]
    produces: Mapping[str, str]

    def __post_init__(self) -> None:
        for field in ("params", "produces"):
            object.__setattr__(self, field, MappingProxyType(dict(getattr(self, field))))
        # A list of identifiers becomes a tuple, so the selection stays frozen and hashable.
        consumes = {
            slot: named if isinstance(named, str) else tuple(named)
            for slot, named in self.consumes.items()
        }
        object.__setattr__(self, "consumes", MappingProxyType(consumes))

    def __hash__(self) -> int:
        """Hash by value, like the frozen dataclass it is; the read-only mappings are unhashable."""
        bindings = (self.params, self.consumes, self.produces)
        return hash((self.name, *(frozenset(mapping.items()) for mapping in bindings)))


@dataclass(frozen=True, slots=True)
class Form:
    """A named group of selections run once per instance, with the artifacts it exports.

    A form is a peer of the others, not a capability: `instances` is the identifier of the
    record-list kind the caller supplies, one record per instance; `exports` are the identifiers
    of the artifacts the form produces, each readable by every other form and by the return form as
    `<name>.<local id of the export>`. All are plain identifiers `<namespace>/<snake_case>`: the
    dotted identifier is built by the engine, never written. `exports` and `capabilities` (the
    form's selections) are kept as tuples copied from what was given.
    """

    name: str
    instances: str
    exports: tuple[str, ...]
    capabilities: tuple[CapabilitySelection, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "exports", tuple(self.exports))
        object.__setattr__(self, "capabilities", tuple(self.capabilities))
        self.check_identifier("name", self.name)
        self.check_identifier("instances", self.instances)
        if not self.exports:
            raise InvalidManifestError("exports must name at least one artifact")
        local_ids: set[str] = set()
        for export in self.exports:
            self.check_identifier("exports", export)
            local_id = export.partition("/")[2]
            if local_id in local_ids:
                raise InvalidManifestError(
                    f"exports: local id {local_id!r} is listed more than once"
                )
            local_ids.add(local_id)

    @staticmethod
    def check_identifier(field: str, identifier: str) -> None:
        """Refuse an identifier that is not `<namespace>/<snake_case>`, naming `field`."""
        namespace, _, local_id = identifier.partition("/")
        try:
            Namespace(namespace).identifier(local_id)
        except InvalidRegistrationError as exc:
            raise InvalidManifestError(f"{field} {identifier!r}: {exc}") from None


@dataclass(frozen=True, slots=True)
class Manifest:
    """One structural version of a jurisdiction's composition.

    `capabilities` keeps the authored order, which is advisory only. `inputs` and `outputs` are
    the identifiers of the artifacts a computation starts from and returns: each non-empty. An
    identifier in both is an input carried onto the return as entered. `forms` are the manifest's
    forms other than the return form, each with its own selections, in a tuple of distinct names.
    `capabilities`, `inputs` and `outputs` are those of the return form, named `return_form_name`;
    a form of that name would be a second return and is refused. The instances kind of each form
    is among `inputs`: the caller supplies it with the rest.
    """

    jurisdiction: JurisdictionCode
    version: int
    valid_from_tax_year: int
    capabilities: tuple[CapabilitySelection, ...]
    inputs: frozenset[str]
    outputs: frozenset[str]
    forms: tuple[Form, ...] = ()

    @property
    def return_form_name(self) -> str:
        """The name of the return form: `return` in the namespace of the jurisdiction."""
        return self.jurisdiction.namespace.identifier("return")

    def __post_init__(self) -> None:
        object.__setattr__(self, "forms", tuple(self.forms))
        names = [found.name for found in self.forms]
        if self.return_form_name in names:
            raise InvalidManifestError(
                f"form {self.return_form_name!r} is the return form: the selections of the "
                "manifest, not a form of `forms`"
            )
        for name in names:
            if names.count(name) > 1:
                raise InvalidManifestError(f"form {name!r} is listed more than once")
        for field in ("inputs", "outputs"):
            if not getattr(self, field):
                raise InvalidManifestError(f"{field} must name at least one artifact")
