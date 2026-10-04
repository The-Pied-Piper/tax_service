"""Unit tests for the NonRefundableCredit capability, with made-up values."""

from __future__ import annotations

from decimal import Decimal

import pytest

from app.domain.artifact import Artifact
from app.domain.capabilities.non_refundable_credit import NonRefundableCredit
from app.domain.capability import TraceLine
from app.domain.parameters.credit import CREDIT as CREDIT_KIND
from app.domain.parameters.credit import Credit
from app.domain.parameters.rounding import NO_ROUNDING, RoundingMode, RoundingRule, RoundTo

D = Decimal
TAX, AFTER = Artifact("basic_tax"), Artifact("tax_after_credit")
CREDIT = Credit(amount=D("1000"), rate=D("0.125"))  # worth 125


def capability(
    credit: Credit = CREDIT, rounding: RoundingRule = NO_ROUNDING
) -> NonRefundableCredit:
    return NonRefundableCredit(TAX, AFTER, credit, rounding)


def test_declares_its_contract() -> None:
    assert capability().consumes == frozenset({TAX})
    assert capability().produces == frozenset({AFTER})


def test_subtracts_the_credit_from_tax() -> None:
    assert capability().run({TAX: D("500")}).outputs == {AFTER: D("375.000")}


def test_never_reduces_tax_below_zero() -> None:
    assert capability().run({TAX: D("100")}).outputs == {AFTER: D("0")}


def test_zero_tax_stays_zero() -> None:
    assert capability().run({TAX: D("0")}).outputs == {AFTER: D("0")}


def test_rounds_the_credit_with_the_given_rule() -> None:
    credit = Credit(amount=D("1000.05"), rate=D("0.1"))  # 100.005
    cent = RoundTo(D("0.01"), RoundingMode.HALF_UP)

    assert capability(credit, cent).run({TAX: D("500")}).outputs == {AFTER: D("399.99")}


def test_traces_the_credit_and_the_result() -> None:
    trace = capability().run({TAX: D("500")}).trace

    assert trace == (
        TraceLine("credit: 12.5% of 1000 (no rounding)", D("125.000")),
        TraceLine("tax_after_credit: basic_tax 500 less credit, not below 0", D("375.000")),
    )


def test_traces_the_unused_part_when_the_credit_exceeds_tax() -> None:
    trace = capability().run({TAX: D("100")}).trace

    assert trace[-1] == TraceLine("unused credit, not refunded", D("25.000"))


def test_rejects_negative_tax() -> None:
    with pytest.raises(ValueError, match="must not be negative"):
        capability().run({TAX: D("-1")})


def test_tax_and_output_must_differ() -> None:
    with pytest.raises(ValueError, match="must differ"):
        NonRefundableCredit(TAX, TAX, CREDIT, NO_ROUNDING)


def test_declares_the_parameter_kind_it_needs() -> None:
    assert NonRefundableCredit.PARAMETERS is CREDIT_KIND
