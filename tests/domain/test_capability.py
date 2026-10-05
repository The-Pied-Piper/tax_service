"""Unit tests for the Capability base: how a capability reads its inputs (design.md §3)."""

from __future__ import annotations

from decimal import Decimal

import pytest

from app.domain.artifact import Amount, Artifact
from app.domain.capability import Capability, CapabilityResult
from app.domain.errors import CapabilityContractError, DuplicateArtifactError, MissingArtifactError


class In(Amount):
    """Made-up artifact for these tests."""


class Other(Amount):
    """Made-up artifact for these tests."""


class Out(Amount):
    """Made-up artifact for these tests."""


class Reader(Capability):
    """Consumes `In` and `Other`; `read` returns what `_input` finds for an artifact."""

    @property
    def consumes(self) -> frozenset[type[Artifact]]:
        return frozenset({In, Other})

    @property
    def produces(self) -> frozenset[type[Artifact]]:
        return frozenset({Out})

    def compute(self, inputs: tuple[Artifact, ...]) -> CapabilityResult:
        return CapabilityResult(outputs=(Out(self._input(inputs, In).value),), trace=())

    def read[A: Artifact](self, inputs: tuple[Artifact, ...], artifact: type[A]) -> A:
        return self._input(inputs, artifact)


def test_input_finds_the_instance_of_the_artifact() -> None:
    inputs = (Other(Decimal(2)), In(Decimal(1)))

    assert Reader().read(inputs, In) == In(Decimal(1))


def test_input_rejects_a_missing_artifact() -> None:
    with pytest.raises(MissingArtifactError, match="Reader needs 'in'"):
        Reader().read((Other(Decimal(2)),), In)


def test_input_rejects_two_values_for_one_artifact() -> None:
    with pytest.raises(DuplicateArtifactError, match="Reader got 2 values for 'in'"):
        Reader().read((In(Decimal(1)), In(Decimal(2))), In)


def test_input_refuses_an_artifact_the_capability_does_not_consume() -> None:
    with pytest.raises(CapabilityContractError, match="Reader does not consume 'out'"):
        Reader().read((Out(Decimal(1)),), Out)
