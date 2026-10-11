"""Unit tests for the Capability base: how a capability reads its inputs (design.md §3)."""

from __future__ import annotations

from decimal import Decimal
from typing import Any, assert_type

import pytest

from app.domain.artifact import Artifact, Value
from app.domain.capability import Capability, CapabilityResult
from app.domain.errors import CapabilityContractError, DuplicateArtifactError, MissingArtifactError

D = Decimal
IN = Artifact("ex/in", Decimal)
OTHER = Artifact("ex/other", Decimal)
OUT = Artifact("ex/out", Decimal)


class Reader(Capability):
    """Consumes `IN` and `OTHER`; `read` returns what `_input` finds for an artifact."""

    @property
    def consumes(self) -> frozenset[Artifact[Any]]:
        return frozenset({IN, OTHER})

    @property
    def produces(self) -> frozenset[Artifact[Any]]:
        return frozenset({OUT})

    def compute(self, inputs: tuple[Value[Any], ...]) -> CapabilityResult:
        return CapabilityResult(outputs=(Value(OUT, self._input(inputs, IN).value),), trace=())

    def read[V](self, inputs: tuple[Value[Any], ...], artifact: Artifact[V]) -> Value[V]:
        return self._input(inputs, artifact)


def test_input_finds_the_value_of_the_artifact() -> None:
    inputs = (Value(OTHER, D(2)), Value(IN, D(1)))

    found = Reader().read(inputs, IN)

    assert_type(found, Value[Decimal])
    assert found == Value(IN, D(1))


def test_input_matches_by_artifact_equality_not_identity() -> None:
    inputs = (Value(Artifact("ex/in", Decimal), D(1)),)

    assert Reader().read(inputs, IN) == Value(IN, D(1))


def test_input_rejects_a_missing_artifact() -> None:
    with pytest.raises(MissingArtifactError, match="Reader needs 'in'"):
        Reader().read((Value(OTHER, D(2)),), IN)


def test_input_rejects_two_values_for_one_artifact() -> None:
    with pytest.raises(DuplicateArtifactError, match="Reader got 2 values for 'in'"):
        Reader().read((Value(IN, D(1)), Value(IN, D(2))), IN)


def test_input_refuses_an_artifact_the_capability_does_not_consume() -> None:
    with pytest.raises(CapabilityContractError, match="Reader does not consume 'out'"):
        Reader().read((Value(OUT, D(1)),), OUT)


def test_compute_returns_values() -> None:
    result = Reader().compute((Value(IN, D(3)), Value(OTHER, D(4))))

    assert result.outputs == (Value(OUT, D(3)),)
