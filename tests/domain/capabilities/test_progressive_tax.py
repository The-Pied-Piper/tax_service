"""Unit tests for the ProgressiveTax capability, with made-up brackets."""

from __future__ import annotations

from decimal import Decimal

import pytest

from app.domain.artifact import Amount
from app.domain.capabilities.progressive_tax import ProgressiveTax
from app.domain.capability import TraceLine
from app.domain.parameters.brackets import BRACKETS, Bracket, BracketSchedule
from app.domain.parameters.rounding import NO_ROUNDING, RoundingMode, RoundingRule, RoundTo

D = Decimal


class TaxableBase(Amount):
    """Made-up artifact for these tests."""


class BasicTax(Amount):
    """Made-up artifact for these tests."""


class OtherBase(Amount):
    """Made-up artifact for these tests."""


class OtherTax(Amount):
    """Made-up artifact for these tests."""


SCHEDULE = BracketSchedule(
    (Bracket(D(0), D("0.10")), Bracket(D(100), D("0.20")), Bracket(D(300), D("0.30")))
)


def capability(rounding: RoundingRule = NO_ROUNDING) -> ProgressiveTax[TaxableBase, BasicTax]:
    return ProgressiveTax(TaxableBase, BasicTax, SCHEDULE, rounding)


def test_declares_its_contract() -> None:
    assert capability().consumes == frozenset({TaxableBase})
    assert capability().produces == frozenset({BasicTax})


def test_produces_tax_on_the_base() -> None:
    result = capability().compute((TaxableBase(D(250)),))

    assert result.outputs == (BasicTax(D("40.0")),)


def test_the_same_capability_serves_different_wiring() -> None:
    wired = ProgressiveTax(OtherBase, OtherTax, SCHEDULE, NO_ROUNDING)

    result = wired.compute((OtherBase(D(50)),))

    assert result.outputs == (OtherTax(D("5.0")),)


def test_rounds_once_at_the_end_with_the_given_rule() -> None:
    cent = RoundTo(D("0.01"), RoundingMode.HALF_UP)
    # 10% of 100 + 20% of 0.025 = 10.005 -> 10.01; per-slice rounding would give 10.00 + 0.01.
    result = capability(cent).compute((TaxableBase(D("100.025")),))

    assert result.outputs == (BasicTax(D("10.01")),)


def test_without_a_rule_the_tax_stays_exact() -> None:
    result = capability().compute((TaxableBase(D("100.025")),))

    assert result.outputs == (BasicTax(D("10.0050")),)


def test_traces_each_slice_and_the_total() -> None:
    cent = RoundTo(D("0.01"), RoundingMode.HALF_UP)

    trace = capability(cent).compute((TaxableBase(D(250)),)).trace

    assert trace == (
        TraceLine("10% on 100 (0 to 100)", D("10.0")),
        TraceLine("20% on 150 (100 to 300)", D("30.0")),
        TraceLine("basic_tax on taxable_base 250 (half-up to 0.01)", D("40.00")),
    )


def test_trace_describes_the_open_top_slice() -> None:
    trace = capability().compute((TaxableBase(D(400)),)).trace

    assert trace[-2] == TraceLine("30% on 100 (over 300)", D("30.0"))
    assert trace[-1] == TraceLine("basic_tax on taxable_base 400 (no rounding)", D("80.0"))


def test_rejects_negative_base() -> None:
    with pytest.raises(ValueError, match="must not be negative"):
        capability().compute((TaxableBase(D(-1)),))


def test_declares_the_parameter_kind_it_needs() -> None:
    assert ProgressiveTax.PARAMETERS is BRACKETS
