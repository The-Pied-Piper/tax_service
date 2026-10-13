"""Unit tests for the Capability base: how a capability reads its inputs (design.md §3)."""

from __future__ import annotations

from decimal import Decimal
from typing import Any, assert_type

import pytest

from app.domain.artifact import Artifact, ArtifactKind
from app.domain.capability import Capability, CapabilityResult
from app.domain.errors import CapabilityContractError, DuplicateArtifactError, MissingArtifactError

D = Decimal
IN = ArtifactKind("ex/in", Decimal)
OTHER = ArtifactKind("ex/other", Decimal)
OUT = ArtifactKind("ex/out", Decimal)


class Reader(Capability):
    """Consumes `IN` and `OTHER`; `read` returns what `_input` finds for a kind."""

    @property
    def consumes(self) -> frozenset[ArtifactKind[Any]]:
        return frozenset({IN, OTHER})

    @property
    def produces(self) -> frozenset[ArtifactKind[Any]]:
        return frozenset({OUT})

    def compute(self, inputs: tuple[Artifact[Any], ...]) -> CapabilityResult:
        return CapabilityResult(outputs=(Artifact(OUT, self._input(inputs, IN).value),), trace=())

    def read[V](self, inputs: tuple[Artifact[Any], ...], kind: ArtifactKind[V]) -> Artifact[V]:
        return self._input(inputs, kind)


def test_input_finds_the_artifact_of_the_kind() -> None:
    inputs = (Artifact(OTHER, D(2)), Artifact(IN, D(1)))

    found = Reader().read(inputs, IN)

    assert_type(found, Artifact[Decimal])
    assert found == Artifact(IN, D(1))


def test_input_matches_by_kind_equality_not_identity() -> None:
    inputs = (Artifact(ArtifactKind("ex/in", Decimal), D(1)),)

    assert Reader().read(inputs, IN) == Artifact(IN, D(1))


def test_input_rejects_a_missing_artifact() -> None:
    with pytest.raises(MissingArtifactError, match="Reader needs 'in'"):
        Reader().read((Artifact(OTHER, D(2)),), IN)


def test_input_rejects_two_artifacts_of_one_kind() -> None:
    with pytest.raises(DuplicateArtifactError, match="Reader got 2 values for 'in'"):
        Reader().read((Artifact(IN, D(1)), Artifact(IN, D(2))), IN)


def test_input_refuses_a_kind_the_capability_does_not_consume() -> None:
    with pytest.raises(CapabilityContractError, match="Reader does not consume 'out'"):
        Reader().read((Artifact(OUT, D(1)),), OUT)


def test_compute_returns_artifacts() -> None:
    result = Reader().compute((Artifact(IN, D(3)), Artifact(OTHER, D(4))))

    assert result.outputs == (Artifact(OUT, D(3)),)
