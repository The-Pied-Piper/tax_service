"""The capability contract (design.md §3).

A capability is pure mechanism. It declares, in code, the artifacts it consumes
and produces; the worksheet holds it to that declaration when applying it. The
vocabulary is consume / produce only: there is no "modify". Fold contributions
come later.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping
from dataclasses import dataclass
from decimal import Decimal
from typing import TYPE_CHECKING, Any, ClassVar

from app.domain.artifact import Artifact
from app.domain.parameters.kind import ParameterKind

if TYPE_CHECKING:
    from app.domain.worksheet import WorksheetView


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
    PARAMETERS: ClassVar[ParameterKind[Any]]
    """The kind of parameter dataset this capability is built from."""

    @property
    @abstractmethod
    def consumes(self) -> frozenset[Artifact]: ...

    @property
    @abstractmethod
    def produces(self) -> frozenset[Artifact]: ...

    @abstractmethod
    def compute(self, worksheet: WorksheetView) -> CapabilityResult:
        """Compute this capability's outputs from the artifacts it consumes.

        Only `Worksheet.apply` calls this in a real computation, checking the contract.
        """
