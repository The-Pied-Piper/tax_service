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
from typing import Any, ClassVar, cast

from app.domain.artifact import Artifact, Value
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
    """What a capability computed: one value per artifact it produces, and how."""

    outputs: tuple[Value[Any], ...]
    trace: tuple[TraceLine, ...]


class Capability(ABC):
    PARAMETERS: ClassVar[ParameterKind[Any]]
    """The kind of parameter dataset this capability is built from."""

    @property
    @abstractmethod
    def consumes(self) -> frozenset[Artifact[Any]]: ...

    @property
    @abstractmethod
    def produces(self) -> frozenset[Artifact[Any]]: ...

    @abstractmethod
    def compute(self, inputs: tuple[Value[Any], ...]) -> CapabilityResult:
        """Compute this capability's outputs from the values of the artifacts it consumes.

        Only `Worksheet.apply` calls this in a real computation, checking the contract.
        """

    def _input[V](self, inputs: tuple[Value[Any], ...], artifact: Artifact[V]) -> Value[V]:
        """The one value of `artifact` in `inputs`; `artifact` must be one this consumes."""
        name = type(self).__name__
        if artifact not in self.consumes:
            raise CapabilityContractError(f"{name} does not consume {artifact.label!r}")
        found = [value for value in inputs if value.artifact == artifact]
        if not found:
            raise MissingArtifactError(f"{name} needs {artifact.label!r}")
        if len(found) > 1:
            raise DuplicateArtifactError(f"{name} got {len(found)} values for {artifact.label!r}")
        # Safe: the value's artifact equals `artifact`, and a Value is checked against its type.
        return cast(Value[V], found[0])


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
