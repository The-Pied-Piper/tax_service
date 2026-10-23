"""Jurisdiction manifest: which capabilities run for a jurisdiction, and from which tax year.

A manifest selects capabilities and fills their slots (design.md §4): parameter slots with
families, artifact slots with artifact identifiers. The slots themselves are declared in code.
A manifest is a flat set of forms, peers that together are the return (a form is a named group of
selections with the artifacts it exports), and the identifiers of the artifacts the computation
starts from.
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
    """A named group of selections run once, or once per instance, with the artifacts it exports.

    A form is a peer of the others, not a capability: `instances` is the identifier of the
    record-list kind the caller supplies, one record per instance, or `None` for a form that runs
    once; `exports` are the identifiers of the artifacts the form produces, each readable by every
    form (itself aside) as `<name>.<local id of the export>`. All are plain identifiers
    `<namespace>/<snake_case>`: the dotted identifier is built by the engine, never written.
    `exports` and `capabilities` (the form's selections) are kept as tuples copied from what was
    given. The inputs of a form are not declared: they are derived from its selections.
    """

    name: str
    instances: str | None
    exports: tuple[str, ...]
    capabilities: tuple[CapabilitySelection, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "exports", tuple(self.exports))
        object.__setattr__(self, "capabilities", tuple(self.capabilities))
        self.check_identifier("name", self.name)
        if self.instances is not None:
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

    `forms` are the peers that together are the return, in a tuple of at least one form with
    distinct names. `inputs` are the identifiers of the artifacts a computation starts from: a
    non-empty set, among them the instances kind of each form, which the caller supplies with the
    rest. Each form's own inputs are derived from its selections.
    """

    jurisdiction: JurisdictionCode
    version: int
    valid_from_tax_year: int
    inputs: frozenset[str]
    forms: tuple[Form, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "forms", tuple(self.forms))
        if not self.forms:
            raise InvalidManifestError("forms must name at least one form")
        names = [found.name for found in self.forms]
        for name in names:
            if names.count(name) > 1:
                raise InvalidManifestError(f"form {name!r} is listed more than once")
        if not self.inputs:
            raise InvalidManifestError("inputs must name at least one artifact")
