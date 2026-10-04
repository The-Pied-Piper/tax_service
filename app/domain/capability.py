"""The capability contract (design.md §3).

A capability is pure mechanism. It declares, in code, the artifacts it consumes
and produces; `run` holds it to that declaration. The vocabulary is consume /
produce only: there is no "modify". Fold contributions come later.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping
from dataclasses import dataclass
from decimal import Decimal

from app.domain.artifact import Artifact
from app.domain.errors import CapabilityContractError, MissingArtifactError


@dataclass(frozen=True)
class TraceLine:
    """One labelled line of a capability's explanation of its result."""

    description: str
    amount: Decimal


@dataclass(frozen=True)
class CapabilityResult:
    outputs: Mapping[Artifact, Decimal]
    trace: tuple[TraceLine, ...]


class Capability(ABC):
    @property
    @abstractmethod
    def consumes(self) -> frozenset[Artifact]: ...

    @property
    @abstractmethod
    def produces(self) -> frozenset[Artifact]: ...

    def run(self, inputs: Mapping[Artifact, Decimal]) -> CapabilityResult:
        """Compute this capability's outputs from the artifacts it consumes."""
        missing = self.consumes - inputs.keys()
        if missing:
            raise MissingArtifactError(f"{type(self).__name__} needs {self._names(missing)}")
        consumed = {artifact: inputs[artifact] for artifact in self.consumes}
        for artifact, value in consumed.items():
            if not isinstance(value, Decimal):
                raise TypeError(
                    f"artifact {artifact.name!r} must be a Decimal, got {type(value).__name__}"
                )
        result = self._compute(consumed)
        produced = frozenset(result.outputs)
        if produced != self.produces:
            raise CapabilityContractError(
                f"{type(self).__name__} declares {self._names(self.produces)} "
                f"but produced {self._names(produced)}"
            )
        return result

    @abstractmethod
    def _compute(self, inputs: Mapping[Artifact, Decimal]) -> CapabilityResult:
        """The mechanism itself; receives exactly the consumed artifacts."""

    @staticmethod
    def _names(artifacts: frozenset[Artifact]) -> str:
        return ", ".join(repr(a.name) for a in sorted(artifacts, key=lambda a: a.name))
