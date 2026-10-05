"""The worksheet: every value of one computation.

It starts with the computation's starting values and records each capability's
outputs as the capability is applied, holding it to its contract (design.md §3).
It never decides what runs next; ordering belongs to the composition (§5).
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from decimal import Decimal

from app.domain.artifact import Artifact
from app.domain.capability import Capability, TraceLine
from app.domain.errors import CapabilityContractError, DuplicateArtifactError, MissingArtifactError


class Worksheet:
    """The values of one computation, and the trace of how they were produced."""

    def __init__(self, values: Mapping[Artifact, Decimal]) -> None:
        self._check_decimals(values)
        self._values = dict(values)
        self._trace: list[TraceLine] = []

    @property
    def trace(self) -> tuple[TraceLine, ...]:
        """Every applied capability's trace lines, in the order they were applied."""
        return tuple(self._trace)

    def get(self, artifact: Artifact) -> Decimal:
        """The value recorded for `artifact`."""
        if artifact not in self._values:
            raise MissingArtifactError(f"no value for {artifact.name!r}")
        return self._values[artifact]

    def view_for(self, capability: Capability) -> WorksheetView:
        """A read-only view limited to the artifacts `capability` consumes."""
        return WorksheetView(self, capability)

    def apply(self, capability: Capability) -> None:
        """Compute `capability` from this worksheet and record its outputs.

        Nothing is recorded unless the capability keeps its contract.
        """
        name = type(capability).__name__
        missing = capability.consumes - self._values.keys()
        if missing:
            raise MissingArtifactError(f"{name} needs {self._names(missing)}")
        result = capability.compute(self.view_for(capability))
        produced = frozenset(result.outputs)
        if produced != capability.produces:
            raise CapabilityContractError(
                f"{name} declares {self._names(capability.produces)} "
                f"but produced {self._names(produced)}"
            )
        self._check_decimals(result.outputs)
        recorded = produced & self._values.keys()
        if recorded:
            raise DuplicateArtifactError(
                f"{name} produced {self._names(recorded)}, already recorded"
            )
        self._values.update(result.outputs)
        self._trace.extend(result.trace)

    @staticmethod
    def _names(artifacts: Iterable[Artifact]) -> str:
        return ", ".join(repr(a.name) for a in sorted(artifacts, key=lambda a: a.name))

    @staticmethod
    def _check_decimals(values: Mapping[Artifact, Decimal]) -> None:
        for artifact, value in values.items():
            if not isinstance(value, Decimal):
                raise TypeError(
                    f"artifact {artifact.name!r} must be a Decimal, got {type(value).__name__}"
                )


class WorksheetView:
    """What a capability may read while computing: only the artifacts it consumes."""

    def __init__(self, worksheet: Worksheet, capability: Capability) -> None:
        self._worksheet = worksheet
        self._capability = capability

    def get(self, artifact: Artifact) -> Decimal:
        """The value of `artifact`, which the capability must consume."""
        if artifact not in self._capability.consumes:
            raise CapabilityContractError(
                f"{type(self._capability).__name__} does not consume {artifact.name!r}"
            )
        return self._worksheet.get(artifact)
