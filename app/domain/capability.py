"""The capability contract (design.md §3).

A capability is pure mechanism. It declares, in code, the artifacts it consumes
and produces; the worksheet holds it to that declaration when applying it. The
vocabulary is consume / produce only: there is no "modify". Fold contributions
come later.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, ClassVar

from app.domain.artifact import Artifact
from app.domain.errors import CapabilityContractError, DuplicateArtifactError, MissingArtifactError
from app.domain.parameters.kind import ParameterKind
from app.domain.registry import NamespacedRegistry


@dataclass(frozen=True)
class TraceLine:
    """One labelled line of a capability's explanation of its result."""

    description: str
    amount: Decimal


@dataclass(frozen=True)
class CapabilityResult:
    outputs: tuple[Artifact, ...]
    trace: tuple[TraceLine, ...]


class Capability(ABC):
    PARAMETERS: ClassVar[ParameterKind[Any]]
    """The kind of parameter dataset this capability is built from."""

    @property
    @abstractmethod
    def consumes(self) -> frozenset[type[Artifact]]: ...

    @property
    @abstractmethod
    def produces(self) -> frozenset[type[Artifact]]: ...

    @abstractmethod
    def compute(self, inputs: tuple[Artifact, ...]) -> CapabilityResult:
        """Compute this capability's outputs from the artifacts it consumes.

        Only `Worksheet.apply` calls this in a real computation, checking the contract.
        """

    def _input[A: Artifact](self, inputs: tuple[Artifact, ...], artifact: type[A]) -> A:
        """The one value of `artifact` in `inputs`; `artifact` must be one this consumes."""
        name = type(self).__name__
        if artifact not in self.consumes:
            raise CapabilityContractError(f"{name} does not consume {artifact.label()!r}")
        found = [value for value in inputs if type(value) is artifact]
        if not found:
            raise MissingArtifactError(f"{name} needs {artifact.label()!r}")
        if len(found) > 1:
            raise DuplicateArtifactError(f"{name} got {len(found)} values for {artifact.label()!r}")
        return found[0]


class CapabilityRegistry(NamespacedRegistry[type[Capability]]):
    """The capability classes packages contribute, by full identifier (`core/progressive_tax`)."""

    def register_class[C: Capability](self, local_id: str, cls: type[C]) -> type[C]:
        """Register `cls` under `local_id` in its package's namespace and return it unchanged."""
        self.register(local_id, cls)
        return cls


def capability[C: Capability](*, identifier: str) -> Callable[[type[C]], type[C]]:
    """Class decorator registering a capability in the shared CapabilityRegistry under `identifier`.

    `identifier` is the local id; the namespace comes from the package declaring `NAMESPACE`.
    """
    return lambda cls: CapabilityRegistry.shared().register_class(identifier, cls)
