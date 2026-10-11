"""Unit tests for the NonRefundableCredit capability, with made-up values."""

from __future__ import annotations

from decimal import Decimal

import pytest

from app.domain.artifact import Artifact, Value
from app.domain.capabilities.non_refundable_credit import NonRefundableCredit
from app.domain.capability import TraceLine
from app.domain.parameters.credit import CREDIT as CREDIT_KIND
from app.domain.parameters.credit import Credit
from app.domain.parameters.rounding import NO_ROUNDING, RoundingMode, RoundingRule, RoundTo

D = Decimal


BASIC_TAX = Artifact("ex/basic_tax", Decimal)
TAX_AFTER_CREDIT = Artifact("ex/tax_after_credit", Decimal)


CREDIT = Credit(amount=D("1000"), rate=D("0.125"))  # worth 125


def capability(
    credit: Credit = CREDIT, rounding: RoundingRule = NO_ROUNDING
) -> NonRefundableCredit:
    return NonRefundableCredit(BASIC_TAX, TAX_AFTER_CREDIT, credit, rounding)


def test_declares_its_contract() -> None:
    assert capability().consumes == frozenset({BASIC_TAX})
    assert capability().produces == frozenset({TAX_AFTER_CREDIT})


def test_subtracts_the_credit_from_tax() -> None:
    assert capability().compute((Value(BASIC_TAX, D("500")),)).outputs == (
        Value(TAX_AFTER_CREDIT, D("375.000")),
    )


def test_never_reduces_tax_below_zero() -> None:
    assert capability().compute((Value(BASIC_TAX, D("100")),)).outputs == (
        Value(TAX_AFTER_CREDIT, D("0")),
    )


def test_zero_tax_stays_zero() -> None:
    assert capability().compute((Value(BASIC_TAX, D("0")),)).outputs == (
        Value(TAX_AFTER_CREDIT, D("0")),
    )


def test_rounds_the_credit_with_the_given_rule() -> None:
    credit = Credit(amount=D("1000.05"), rate=D("0.1"))  # 100.005
    cent = RoundTo(D("0.01"), RoundingMode.HALF_UP)

    result = capability(credit, cent).compute((Value(BASIC_TAX, D("500")),))

    assert result.outputs == (Value(TAX_AFTER_CREDIT, D("399.99")),)


def test_traces_the_credit_and_the_result() -> None:
    trace = capability().compute((Value(BASIC_TAX, D("500")),)).trace

    assert trace == (
        TraceLine("credit: 12.5% of 1000 (no rounding)", D("125.000")),
        TraceLine("tax_after_credit: basic_tax 500 less credit, not below 0", D("375.000")),
    )


def test_traces_the_unused_part_when_the_credit_exceeds_tax() -> None:
    trace = capability().compute((Value(BASIC_TAX, D("100")),)).trace

    assert trace[-1] == TraceLine("unused credit, not refunded", D("25.000"))


def test_rejects_negative_tax() -> None:
    with pytest.raises(ValueError, match="basic_tax must not be negative"):
        capability().compute((Value(BASIC_TAX, D("-1")),))


def test_declares_the_parameter_kind_it_needs() -> None:
    assert NonRefundableCredit.PARAMETERS is CREDIT_KIND


def test_is_not_generic_over_artifacts() -> None:
    assert not getattr(NonRefundableCredit, "__type_params__", ())
    assert not getattr(NonRefundableCredit, "__parameters__", ())


def test_mypy_rejects_wiring_an_artifact_of_another_value_type() -> None:
    count = Artifact("ex/count", int)
    # An Artifact[int] is not Money; the ignore fails under mypy (warn_unused_ignores) if wiring
    # an artifact of another value type is ever accepted.
    NonRefundableCredit(count, TAX_AFTER_CREDIT, CREDIT, NO_ROUNDING)  # type: ignore[arg-type]


class Cents(Decimal):
    """A made-up Decimal subtype, to probe Artifact's variance."""


CENTS = Artifact("ex/cents", Cents)  # bound to a name: built inline it would infer Decimal


def test_mypy_rejects_wiring_an_artifact_of_a_value_subtype() -> None:
    # `Artifact` is invariant, so an Artifact[Cents] is not Money; if `Artifact` ever became
    # covariant this ignore would be unused and mypy (strict) would fail.
    NonRefundableCredit(CENTS, TAX_AFTER_CREDIT, CREDIT, NO_ROUNDING)  # type: ignore[arg-type]
