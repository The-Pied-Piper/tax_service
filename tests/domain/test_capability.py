"""Unit tests for the Capability contract (design.md §3).

A capability declares what it consumes and produces, and `run` holds it to that
contract: required inputs must be present and outputs must match `produces`.
"""

from __future__ import annotations

from collections.abc import Mapping
from decimal import Decimal

import pytest

from app.domain.artifact import Artifact
from app.domain.capability import Capability, CapabilityResult, TraceLine
from app.domain.errors import CapabilityContractError, DomainError, MissingArtifactError

A, B, C = Artifact("a"), Artifact("b"), Artifact("c")


class Double(Capability):
    """Produces `out` = 2 × `inp`; `extra` lets a test break the contract."""

    def __init__(self, inp: Artifact, out: Artifact, extra: Artifact | None = None) -> None:
        self._inp, self._out, self._extra = inp, out, extra

    @property
    def consumes(self) -> frozenset[Artifact]:
        return frozenset({self._inp})

    @property
    def produces(self) -> frozenset[Artifact]:
        return frozenset({self._out})

    def _compute(self, inputs: Mapping[Artifact, Decimal]) -> CapabilityResult:
        value = inputs[self._inp] * 2
        outputs = {self._out: value}
        if self._extra is not None:
            outputs[self._extra] = value
        return CapabilityResult(outputs=outputs, trace=(TraceLine("doubled", value),))


def test_run_returns_outputs_and_trace() -> None:
    result = Double(A, B).run({A: Decimal("2.5")})

    assert result.outputs == {B: Decimal("5.0")}
    assert result.trace == (TraceLine("doubled", Decimal("5.0")),)


def test_run_ignores_inputs_it_does_not_consume() -> None:
    assert Double(A, B).run({A: Decimal(1), C: Decimal(9)}).outputs == {B: Decimal(2)}


def test_run_rejects_missing_input() -> None:
    with pytest.raises(MissingArtifactError, match="'a'"):
        Double(A, B).run({C: Decimal(1)})


def test_run_rejects_outputs_beyond_the_contract() -> None:
    with pytest.raises(CapabilityContractError, match="'c'"):
        Double(A, B, extra=C).run({A: Decimal(1)})


def test_errors_are_domain_errors() -> None:
    assert issubclass(MissingArtifactError, DomainError)
    assert issubclass(CapabilityContractError, DomainError)


def test_run_rejects_non_decimal_input() -> None:
    with pytest.raises(TypeError, match="must be a Decimal"):
        Double(A, B).run({A: 1.5})  # type: ignore[dict-item]
