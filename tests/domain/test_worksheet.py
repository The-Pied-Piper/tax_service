"""Unit tests for the Worksheet: every value of one computation (design.md §3).

The worksheet holds each capability to its contract when applying it: consumed
inputs must be present, outputs must match `produces`, and no value is overwritten.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Any, assert_type, cast

import pytest

from app.domain.artifact import Artifact, Money, Value
from app.domain.capability import Capability, CapabilityResult, TraceLine
from app.domain.errors import (
    CapabilityContractError,
    DomainError,
    DuplicateArtifactError,
    MissingArtifactError,
)
from app.domain.worksheet import Worksheet

D = Decimal
A = Artifact("ex/a", Decimal)
B = Artifact("ex/b", Decimal)
C = Artifact("ex/c", Decimal)


class Double(Capability):
    """Produces `out` = 2 × `inp`; `extra`, `skip` and `peek` let a test break the contract."""

    def __init__(
        self,
        inp: Money,
        out: Money,
        extra: Money | None = None,
        skip: bool = False,
        peek: Money | None = None,
    ) -> None:
        self._inp, self._out, self._extra, self._skip, self._peek = inp, out, extra, skip, peek
        self.received: tuple[Value[Any], ...] = ()

    @property
    def consumes(self) -> frozenset[Artifact[Any]]:
        return frozenset({self._inp})

    @property
    def produces(self) -> frozenset[Artifact[Any]]:
        return frozenset({self._out})

    def compute(self, inputs: tuple[Value[Any], ...]) -> CapabilityResult:
        self.received = inputs
        if self._peek is not None:
            self._input(inputs, self._peek)
        value = self._input(inputs, self._inp).value * 2
        outputs: tuple[Value[Any], ...] = () if self._skip else (Value(self._out, value),)
        if self._extra is not None:
            outputs += (Value(self._extra, value),)
        return CapabilityResult(outputs=outputs, trace=(TraceLine("doubled", value),))


def test_holds_its_starting_values() -> None:
    found = Worksheet(Value(A, D("2.5"))).get(A)

    assert_type(found, Value[Decimal])
    assert found == Value(A, D("2.5"))


def test_get_matches_by_artifact_equality_not_identity() -> None:
    worksheet = Worksheet(Value(Artifact("ex/a", Decimal), D(1)))

    assert worksheet.get(A) == Value(A, D(1))


def test_get_rejects_a_value_it_does_not_hold() -> None:
    with pytest.raises(MissingArtifactError, match="'b'"):
        Worksheet(Value(A, D(1))).get(B)


def test_rejects_a_starting_value_that_is_not_a_value() -> None:
    with pytest.raises(TypeError, match="must be a Value, got Decimal"):
        Worksheet(cast(Any, D(1)))


def test_rejects_an_artifact_given_as_a_starting_value() -> None:
    with pytest.raises(TypeError, match="must be a Value, got Artifact"):
        Worksheet(cast(Any, A))


def test_rejects_two_starting_values_for_one_artifact() -> None:
    with pytest.raises(DuplicateArtifactError, match="'a'"):
        Worksheet(Value(A, D(1)), Value(A, D(2)))


def test_apply_records_the_outputs() -> None:
    worksheet = Worksheet(Value(A, D("2.5")))

    worksheet.apply(Double(A, B))

    assert worksheet.get(B) == Value(B, D("5.0"))


def test_apply_feeds_one_capability_into_the_next() -> None:
    worksheet = Worksheet(Value(A, D(1)))

    worksheet.apply(Double(A, B))
    worksheet.apply(Double(B, C))

    assert worksheet.get(C) == Value(C, D(4))


def test_apply_passes_only_what_the_capability_consumes() -> None:
    capability = Double(A, B)

    Worksheet(Value(A, D(1)), Value(C, D(9))).apply(capability)

    assert capability.received == (Value(A, D(1)),)


def test_apply_collects_the_trace_in_order() -> None:
    worksheet = Worksheet(Value(A, D(1)))

    worksheet.apply(Double(A, B))
    worksheet.apply(Double(B, C))

    assert worksheet.trace == (TraceLine("doubled", D(2)), TraceLine("doubled", D(4)))


def test_a_new_worksheet_has_no_trace() -> None:
    assert Worksheet(Value(A, D(1))).trace == ()


def test_records_the_producer_of_each_value() -> None:
    worksheet = Worksheet(Value(A, D(1)))
    capability = Double(A, B)

    worksheet.apply(capability)

    assert worksheet.producer_of(B) is capability


def test_starting_values_have_no_producer() -> None:
    assert Worksheet(Value(A, D(1))).producer_of(A) is None


def test_producer_of_rejects_a_value_it_does_not_hold() -> None:
    with pytest.raises(MissingArtifactError, match="'b'"):
        Worksheet(Value(A, D(1))).producer_of(B)


def test_apply_rejects_missing_input() -> None:
    with pytest.raises(MissingArtifactError, match="Double needs 'a'"):
        Worksheet(Value(C, D(1))).apply(Double(A, B))


def test_apply_rejects_outputs_beyond_the_contract() -> None:
    with pytest.raises(CapabilityContractError, match="'c'"):
        Worksheet(Value(A, D(1))).apply(Double(A, B, extra=C))


def test_apply_rejects_outputs_short_of_the_contract() -> None:
    with pytest.raises(CapabilityContractError, match="'b'"):
        Worksheet(Value(A, D(1))).apply(Double(A, B, skip=True))


def test_apply_rejects_two_outputs_for_one_artifact() -> None:
    with pytest.raises(DuplicateArtifactError, match="Double produced 'b' more than once"):
        Worksheet(Value(A, D(1))).apply(Double(A, B, extra=B))


def test_apply_records_nothing_when_the_contract_is_broken() -> None:
    worksheet = Worksheet(Value(A, D(1)))

    with pytest.raises(CapabilityContractError):
        worksheet.apply(Double(A, B, extra=C))

    with pytest.raises(MissingArtifactError):
        worksheet.get(B)
    assert worksheet.trace == ()


def test_apply_refuses_to_overwrite_a_value() -> None:
    worksheet = Worksheet(Value(A, D(1)), Value(B, D(7)))

    with pytest.raises(DuplicateArtifactError, match="'b'"):
        worksheet.apply(Double(A, B))

    assert worksheet.get(B) == Value(B, D(7))
    assert worksheet.producer_of(B) is None


def test_apply_rejects_an_output_that_is_not_a_value() -> None:
    class Plain(Double):
        def compute(self, inputs: tuple[Value[Any], ...]) -> CapabilityResult:
            return CapabilityResult(outputs=cast(Any, (D(2),)), trace=())

    with pytest.raises(TypeError, match="must be a Value, got Decimal"):
        Worksheet(Value(A, D(1))).apply(Plain(A, B))


def test_a_capability_cannot_read_what_it_does_not_consume() -> None:
    worksheet = Worksheet(Value(A, D(1)), Value(C, D(9)))

    with pytest.raises(CapabilityContractError, match="Double does not consume 'c'"):
        worksheet.apply(Double(A, B, peek=C))


def test_errors_are_domain_errors() -> None:
    assert issubclass(MissingArtifactError, DomainError)
    assert issubclass(CapabilityContractError, DomainError)
    assert issubclass(DuplicateArtifactError, DomainError)
