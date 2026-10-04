"""Unit tests for the ProgressiveTax capability, with made-up brackets."""

from __future__ import annotations

from decimal import Decimal

import pytest

from app.domain.artifact import Artifact
from app.domain.capabilities.progressive_tax import ProgressiveTax
from app.domain.capability import TraceLine
from app.domain.parameters.brackets import Bracket, BracketSchedule
from app.domain.parameters.rounding import NO_ROUNDING, RoundingMode, RoundTo

D = Decimal
BASE, TAX = Artifact("taxable_base"), Artifact("basic_tax")
SCHEDULE = BracketSchedule(
    (Bracket(D(0), D("0.10")), Bracket(D(100), D("0.20")), Bracket(D(300), D("0.30")))
)


def test_declares_its_contract() -> None:
    capability = ProgressiveTax(BASE, TAX, SCHEDULE, NO_ROUNDING)

    assert capability.consumes == frozenset({BASE})
    assert capability.produces == frozenset({TAX})


def test_produces_tax_on_the_base() -> None:
    result = ProgressiveTax(BASE, TAX, SCHEDULE, NO_ROUNDING).run({BASE: D(250)})

    assert result.outputs == {TAX: D("40.0")}


def test_the_same_capability_serves_different_wiring() -> None:
    other_base, other_tax = Artifact("other_base"), Artifact("other_tax")

    result = ProgressiveTax(other_base, other_tax, SCHEDULE, NO_ROUNDING).run({other_base: D(50)})

    assert result.outputs == {other_tax: D("5.0")}


def test_rounds_once_at_the_end_with_the_given_rule() -> None:
    cent = RoundTo(D("0.01"), RoundingMode.HALF_UP)
    # 10% of 100 + 20% of 0.025 = 10.005 -> 10.01; per-slice rounding would give 10.00 + 0.01.
    result = ProgressiveTax(BASE, TAX, SCHEDULE, cent).run({BASE: D("100.025")})

    assert result.outputs == {TAX: D("10.01")}


def test_without_a_rule_the_tax_stays_exact() -> None:
    result = ProgressiveTax(BASE, TAX, SCHEDULE, NO_ROUNDING).run({BASE: D("100.025")})

    assert result.outputs == {TAX: D("10.0050")}


def test_traces_each_slice_and_the_total() -> None:
    cent = RoundTo(D("0.01"), RoundingMode.HALF_UP)

    trace = ProgressiveTax(BASE, TAX, SCHEDULE, cent).run({BASE: D(250)}).trace

    assert trace == (
        TraceLine("10% on 100 (0 to 100)", D("10.0")),
        TraceLine("20% on 150 (100 to 300)", D("30.0")),
        TraceLine("basic_tax on taxable_base 250 (half-up to 0.01)", D("40.00")),
    )


def test_trace_describes_the_open_top_slice() -> None:
    trace = ProgressiveTax(BASE, TAX, SCHEDULE, NO_ROUNDING).run({BASE: D(400)}).trace

    assert trace[-2] == TraceLine("30% on 100 (over 300)", D("30.0"))
    assert trace[-1] == TraceLine("basic_tax on taxable_base 400 (no rounding)", D("80.0"))


def test_rejects_negative_base() -> None:
    with pytest.raises(ValueError, match="must not be negative"):
        ProgressiveTax(BASE, TAX, SCHEDULE, NO_ROUNDING).run({BASE: D(-1)})


def test_base_and_output_must_differ() -> None:
    with pytest.raises(ValueError, match="must differ"):
        ProgressiveTax(BASE, BASE, SCHEDULE, NO_ROUNDING)
