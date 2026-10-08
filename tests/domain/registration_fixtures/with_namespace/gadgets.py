"""Made-up things registered under the `ex` namespace of the enclosing package."""

from __future__ import annotations

from app.domain.artifact import Artifact
from app.domain.capability import Capability, CapabilityResult


class Gadget:
    """A made-up thing to register."""


class Sprocket:
    """Another made-up thing to register."""


class GadgetLevy(Capability):
    """A made-up capability; deliberately not decorated, so importing it registers nothing."""

    @property
    def consumes(self) -> frozenset[type[Artifact]]:
        return frozenset()

    @property
    def produces(self) -> frozenset[type[Artifact]]:
        return frozenset()

    def compute(self, inputs: tuple[Artifact, ...]) -> CapabilityResult:
        return CapabilityResult(outputs=(), trace=())
