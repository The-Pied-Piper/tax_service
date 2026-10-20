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

from app.domain.errors import InvalidManifestError
from app.domain.jurisdiction_code import JurisdictionCode


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
class Manifest:
    """One structural version of a jurisdiction's composition.

    `capabilities` keeps the authored order, which is advisory only. `inputs` and `outputs` are
    the identifiers of the artifacts a computation starts from and returns: each non-empty. An
    identifier in both is an input carried onto the return as entered.
    """

    jurisdiction: JurisdictionCode
    version: int
    valid_from_tax_year: int
    capabilities: tuple[CapabilitySelection, ...]
    inputs: frozenset[str]
    outputs: frozenset[str]

    def __post_init__(self) -> None:
        for field in ("inputs", "outputs"):
            if not getattr(self, field):
                raise InvalidManifestError(f"{field} must name at least one artifact")
