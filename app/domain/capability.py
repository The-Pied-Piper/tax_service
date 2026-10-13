"""The capability contract (design.md §3).

A capability is pure mechanism. It declares, in code, the artifact kinds it consumes
and produces; the worksheet holds it to that declaration when applying it. The
vocabulary is consume / produce only: there is no "modify". Fold contributions
come later.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, ClassVar, cast

from app.domain.artifact import Artifact, ArtifactKind
from app.domain.errors import CapabilityContractError, DuplicateArtifactError, MissingArtifactError
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


class Capability(ABC):
    PARAMETERS: ClassVar[ParameterKind[Any]]
    """The kind of parameter dataset this capability is built from."""

    @property
    @abstractmethod
    def consumes(self) -> frozenset[ArtifactKind[Any]]: ...

    @property
    @abstractmethod
    def produces(self) -> frozenset[ArtifactKind[Any]]: ...

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
