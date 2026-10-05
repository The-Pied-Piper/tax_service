"""The worksheet: every value of one computation.

It starts with the computation's starting values and records each capability's
outputs as the capability is applied, holding it to its contract (design.md §3).
It never decides what runs next; ordering belongs to the composition (§5).
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import cast

from app.domain.artifact import Artifact
from app.domain.capability import Capability, TraceLine
from app.domain.errors import CapabilityContractError, DuplicateArtifactError, MissingArtifactError


class Worksheet:
    """The values of one computation, who produced each, and the trace of how."""

    def __init__(self, *values: Artifact) -> None:
        self._check_artifacts(values)
        self._values: dict[type[Artifact], Artifact] = {}
        self._producers: dict[type[Artifact], Capability] = {}
        self._trace: list[TraceLine] = []
        for value in values:
            if type(value) in self._values:
                raise DuplicateArtifactError(f"two starting values for {value.label()!r}")
            self._values[type(value)] = value

    @property
    def trace(self) -> tuple[TraceLine, ...]:
        """Every applied capability's trace lines, in the order they were applied."""
        return tuple(self._trace)

    def get[A: Artifact](self, artifact: type[A]) -> A:
        """The value recorded for `artifact`."""
        if artifact not in self._values:
            raise MissingArtifactError(f"no value for {artifact.label()!r}")
        return cast(A, self._values[artifact])  # each value is keyed by its own class

    def producer_of(self, artifact: type[Artifact]) -> Capability | None:
        """The capability that produced `artifact`'s value; `None` for a starting value."""
        if artifact not in self._values:
            raise MissingArtifactError(f"no value for {artifact.label()!r}")
        return self._producers.get(artifact)

    def apply(self, capability: Capability) -> None:
        """Compute `capability` from this worksheet and record its outputs.

        Nothing is recorded unless the capability keeps its contract.
        """
        name = type(capability).__name__
        missing = capability.consumes - self._values.keys()
        if missing:
            raise MissingArtifactError(f"{name} needs {self._labels(missing)}")
        result = capability.compute(tuple(self._values[a] for a in capability.consumes))
        self._check_artifacts(result.outputs)
        produced = [type(value) for value in result.outputs]
        if frozenset(produced) != capability.produces:
            raise CapabilityContractError(
                f"{name} declares {self._labels(capability.produces)} "
                f"but produced {self._labels(set(produced))}"
            )
        repeated = {a for a in produced if produced.count(a) > 1}
        if repeated:
            raise DuplicateArtifactError(f"{name} produced {self._labels(repeated)} more than once")
        recorded = capability.produces & self._values.keys()
        if recorded:
            raise DuplicateArtifactError(
                f"{name} produced {self._labels(recorded)}, already recorded"
            )
        for value in result.outputs:
            self._values[type(value)] = value
            self._producers[type(value)] = capability
        self._trace.extend(result.trace)

    @staticmethod
    def _labels(artifacts: Iterable[type[Artifact]]) -> str:
        return ", ".join(repr(label) for label in sorted(a.label() for a in artifacts))

    @staticmethod
    def _check_artifacts(values: Iterable[object]) -> None:
        for value in values:
            if not isinstance(value, Artifact):
                raise TypeError(f"a value must be an artifact, got {type(value).__name__}")
