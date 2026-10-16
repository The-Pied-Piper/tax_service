"""The capability contract (design.md §3).

A capability is pure mechanism. Its class declares, in code, named slots: parameter slots
(`PARAMETERS`, slot -> parameter kind) and artifact slots (`CONSUMES` / `PRODUCES`, slot -> value
type), each a keyword parameter of its constructor; a manifest fills them. An instance consumes
and produces the artifact kinds it was built with, and the worksheet holds it to that. The
vocabulary is consume / produce only: there is no "modify". Fold contributions come later.
"""

from __future__ import annotations

import inspect
import re
from abc import ABC, abstractmethod
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from decimal import Decimal
from types import MappingProxyType
from typing import Any, ClassVar, cast

from app.domain.artifact import Artifact, ArtifactKind
from app.domain.errors import (
    CapabilityContractError,
    DuplicateArtifactError,
    InvalidCapabilityError,
    MissingArtifactError,
)
from app.domain.parameters.kind import ParameterKind
from app.domain.registry import Namespace, Registry


@dataclass(frozen=True)
class TraceLine:
    """One labelled line of a capability's explanation of its result."""

    description: str
    amount: Decimal


@dataclass(frozen=True)
class CapabilityResult:
    """What a capability computed: one artifact per kind it produces, and how."""

    outputs: tuple[Artifact[Any], ...]
    trace: tuple[TraceLine, ...]


_SLOT_NAME = re.compile(r"[a-z][a-z0-9]*(_[a-z0-9]+)*")
_SLOT_MAPPINGS = ("PARAMETERS", "CONSUMES", "PRODUCES")
_KEYWORD_CAPABLE = frozenset(
    {inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.KEYWORD_ONLY}
)


class Capability(ABC):
    """A mechanism, built from named slots, that computes what it produces from what it consumes.

    Subclasses may assign plain dicts to the slot mappings; each is exposed read-only, and every
    slot is checked against the constructor when the subclass is defined. The constructor must be
    written in the class body (a dataclass-generated `__init__` is not there yet when the check
    runs), and each slot must be a named keyword parameter of it: `**kwargs` does not count. The
    constructor passes its artifact slots, by name, to `super().__init__`, which checks them and
    derives `consumes` and `produces`; parameter datasets stay on the subclass.
    """

    PARAMETERS: ClassVar[Mapping[str, ParameterKind[Any]]] = MappingProxyType({})
    """Parameter slots: slot name -> the kind of dataset the constructor takes under that name."""

    CONSUMES: ClassVar[Mapping[str, type]] = MappingProxyType({})
    """Consumed artifact slots: slot name -> the value type of the artifact kind it takes."""

    PRODUCES: ClassVar[Mapping[str, type]] = MappingProxyType({})
    """Produced artifact slots: slot name -> the value type of the artifact kind it takes."""

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Freeze the slot mappings `cls` declares and check every slot it has against `__init__`.

        Raises InvalidCapabilityError naming the class and the slot.
        """
        super().__init_subclass__(**kwargs)
        for mapping in _SLOT_MAPPINGS:
            if mapping in vars(cls):
                declared = getattr(cls, mapping)
                if not isinstance(declared, Mapping):
                    raise InvalidCapabilityError(
                        f"{cls.__name__}: {mapping} must be a mapping of slot names, "
                        f"got {type(declared).__name__}"
                    )
                setattr(cls, mapping, MappingProxyType(dict(declared)))
        cls._check_slots()

    @classmethod
    def _check_slots(cls) -> None:
        name = cls.__name__
        declared_in: dict[str, str] = {}
        for mapping in _SLOT_MAPPINGS:
            for slot, filler in getattr(cls, mapping).items():
                cls._check_slot(mapping, slot, filler)
                if slot in declared_in:
                    raise InvalidCapabilityError(
                        f"{name}: slot {slot!r} is declared in both {declared_in[slot]} "
                        f"and {mapping}"
                    )
                declared_in[slot] = mapping
        # `__init__`'s own signature, not the class's, so a custom `__new__` cannot hide it; its
        # first parameter (`self`) is skipped, so `self` can never fill a slot.
        _self, *parameters = inspect.signature(cls.__init__).parameters.values()
        keywords = {p.name for p in parameters if p.kind in _KEYWORD_CAPABLE}
        for slot, mapping in declared_in.items():
            if slot not in keywords:
                raise InvalidCapabilityError(
                    f"{name}: {mapping} slot {slot!r} is not a keyword parameter of {name}.__init__"
                )

    @classmethod
    def _check_slot(cls, mapping: str, slot: object, filler: object) -> None:
        name = cls.__name__
        if not isinstance(slot, str):
            raise InvalidCapabilityError(
                f"{name}: {mapping} slot {slot!r} must be a string, got {type(slot).__name__}"
            )
        if not _SLOT_NAME.fullmatch(slot):
            raise InvalidCapabilityError(f"{name}: {mapping} slot {slot!r} must be snake_case")
        if mapping == "PARAMETERS":
            if not isinstance(filler, ParameterKind):
                raise InvalidCapabilityError(
                    f"{name}: PARAMETERS slot {slot!r} must map to a ParameterKind, got {filler!r}"
                )
        elif not isinstance(filler, type):
            raise InvalidCapabilityError(
                f"{name}: {mapping} slot {slot!r} must be a type, got {filler!r}"
            )

    def __init__(self, **slots: ArtifactKind[Any]) -> None:
        """Wire the artifact slots declared in `CONSUMES` / `PRODUCES` with the kinds given by name.

        Raises InvalidCapabilityError naming the class and the slot if one is missing, unknown,
        not filled with a kind of exactly its value type, or filled with a kind another slot has.
        """
        name = type(self).__name__
        declared = {**self.CONSUMES, **self.PRODUCES}
        for slot in slots:
            if slot not in declared:
                hint = " (it is a parameter slot)" if slot in self.PARAMETERS else ""
                raise InvalidCapabilityError(f"{name}: {slot!r} is not an artifact slot{hint}")
        filled_by: dict[ArtifactKind[Any], str] = {}
        for slot, value_type in declared.items():
            if slot not in slots:
                raise InvalidCapabilityError(f"{name}: artifact slot {slot!r} is not given")
            kind: object = slots[slot]
            if not isinstance(kind, ArtifactKind):
                raise InvalidCapabilityError(
                    f"{name}: artifact slot {slot!r} must be an ArtifactKind, got {kind!r}"
                )
            if kind.value_type is not value_type:
                raise InvalidCapabilityError(
                    f"{name}: artifact slot {slot!r} takes a kind of {value_type.__name__}, "
                    f"got {kind.identifier!r} of {kind.value_type.__name__}"
                )
            if kind in filled_by:
                raise InvalidCapabilityError(
                    f"{name}: artifact slots {filled_by[kind]!r} and {slot!r} are both given "
                    f"{kind.identifier!r}"
                )
            filled_by[kind] = slot
        self._consumes = frozenset(slots[slot] for slot in self.CONSUMES)
        self._produces = frozenset(slots[slot] for slot in self.PRODUCES)

    @property
    def consumes(self) -> frozenset[ArtifactKind[Any]]:
        """The artifact kinds this capability was built to consume."""
        return self._wired("_consumes")

    @property
    def produces(self) -> frozenset[ArtifactKind[Any]]:
        """The artifact kinds this capability was built to produce."""
        return self._wired("_produces")

    def _wired(self, attribute: str) -> frozenset[ArtifactKind[Any]]:
        """The kinds stored under `attribute` by `Capability.__init__`, which must have run."""
        try:
            kinds: frozenset[ArtifactKind[Any]] = getattr(self, attribute)
        except AttributeError:
            raise InvalidCapabilityError(
                f"{type(self).__name__}: __init__ must pass its artifact slots to super().__init__"
            ) from None
        return kinds

    @abstractmethod
    def compute(self, inputs: tuple[Artifact[Any], ...]) -> CapabilityResult:
        """Compute this capability's output artifacts from the artifacts of the kinds it consumes.

        Only `Worksheet.apply` calls this in a real computation, checking the contract.
        """

    def _input[V](self, inputs: tuple[Artifact[Any], ...], kind: ArtifactKind[V]) -> Artifact[V]:
        """The one artifact of `kind` in `inputs`; `kind` must be one this consumes."""
        name = type(self).__name__
        if kind not in self.consumes:
            raise CapabilityContractError(f"{name} does not consume {kind.label!r}")
        found = [artifact for artifact in inputs if artifact.kind == kind]
        if not found:
            raise MissingArtifactError(f"{name} needs {kind.label!r}")
        if len(found) > 1:
            raise DuplicateArtifactError(f"{name} got {len(found)} values for {kind.label!r}")
        # Safe: the artifact's kind equals `kind`, and an Artifact is checked against its kind.
        return cast(Artifact[V], found[0])


class CapabilityRegistry(Registry[type[Capability]]):
    """The capability classes packages contribute, by full identifier (`core/progressive_tax`).

    Register through `register_class` or `@capability`; the inherited `register` takes the key
    as given and skips namespace validation.
    """

    def register_class[C: Capability](self, local_id: str, cls: type[C]) -> type[C]:
        """Register `cls` under `local_id` in its package's namespace and return it unchanged."""
        self.register(Namespace.of(cls).identifier(local_id), cls)
        return cls


def capability[C: Capability](*, identifier: str) -> Callable[[type[C]], type[C]]:
    """Class decorator registering a capability in the shared CapabilityRegistry under `identifier`.

    `identifier` is the local id; the namespace comes from the package declaring `NAMESPACE`.
    """
    return lambda cls: CapabilityRegistry.shared().register_class(identifier, cls)
