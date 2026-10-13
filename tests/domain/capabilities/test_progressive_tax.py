"""Unit tests for the ProgressiveTax capability, with made-up brackets."""

from __future__ import annotations

from decimal import Decimal

import pytest

from app.domain.artifact import Artifact, ArtifactKind
from app.domain.capabilities.progressive_tax import ProgressiveTax
from app.domain.capability import TraceLine
from app.domain.parameters.brackets import BRACKETS, Bracket, BracketSchedule
from app.domain.parameters.rounding import NO_ROUNDING, RoundingMode, RoundingRule, RoundTo

D = Decimal


TAXABLE_BASE = ArtifactKind("ex/taxable_base", Decimal)
BASIC_TAX = ArtifactKind("ex/basic_tax", Decimal)
OTHER_BASE = ArtifactKind("ex/other_base", Decimal)
OTHER_TAX = ArtifactKind("ex/other_tax", Decimal)


SCHEDULE = BracketSchedule(
    (Bracket(D(0), D("0.10")), Bracket(D(100), D("0.20")), Bracket(D(300), D("0.30")))
)


def capability(rounding: RoundingRule = NO_ROUNDING) -> ProgressiveTax:
    return ProgressiveTax(TAXABLE_BASE, BASIC_TAX, SCHEDULE, rounding)


def test_declares_its_contract() -> None:
    assert capability().consumes == frozenset({TAXABLE_BASE})
    assert capability().produces == frozenset({BASIC_TAX})


def test_produces_tax_on_the_base() -> None:
    result = capability().compute((Artifact(TAXABLE_BASE, D(250)),))

    assert result.outputs == (Artifact(BASIC_TAX, D("40.0")),)


def test_the_same_capability_serves_different_wiring() -> None:
    wired = ProgressiveTax(OTHER_BASE, OTHER_TAX, SCHEDULE, NO_ROUNDING)

    result = wired.compute((Artifact(OTHER_BASE, D(50)),))

    assert result.outputs == (Artifact(OTHER_TAX, D("5.0")),)


def test_rounds_once_at_the_end_with_the_given_rule() -> None:
    cent = RoundTo(D("0.01"), RoundingMode.HALF_UP)
    # 10% of 100 + 20% of 0.025 = 10.005 -> 10.01; per-slice rounding would give 10.00 + 0.01.
    result = capability(cent).compute((Artifact(TAXABLE_BASE, D("100.025")),))

    assert result.outputs == (Artifact(BASIC_TAX, D("10.01")),)


def test_without_a_rule_the_tax_stays_exact() -> None:
    result = capability().compute((Artifact(TAXABLE_BASE, D("100.025")),))

    assert result.outputs == (Artifact(BASIC_TAX, D("10.0050")),)


def test_traces_each_slice_and_the_total() -> None:
    cent = RoundTo(D("0.01"), RoundingMode.HALF_UP)

    trace = capability(cent).compute((Artifact(TAXABLE_BASE, D(250)),)).trace

    assert trace == (
        TraceLine("10% on 100 (0 to 100)", D("10.0")),
        TraceLine("20% on 150 (100 to 300)", D("30.0")),
        TraceLine("basic_tax on taxable_base 250 (half-up to 0.01)", D("40.00")),
    )


def test_trace_describes_the_open_top_slice() -> None:
    trace = capability().compute((Artifact(TAXABLE_BASE, D(400)),)).trace

    assert trace[-2] == TraceLine("30% on 100 (over 300)", D("30.0"))
    assert trace[-1] == TraceLine("basic_tax on taxable_base 400 (no rounding)", D("80.0"))


def test_rejects_negative_base() -> None:
    with pytest.raises(ValueError, match="must not be negative"):
        capability().compute((Artifact(TAXABLE_BASE, D(-1)),))


def test_declares_the_parameter_kind_it_needs() -> None:
    assert ProgressiveTax.PARAMETERS is BRACKETS


def test_is_not_generic_over_artifacts() -> None:
    assert not getattr(ProgressiveTax, "__type_params__", ())
    assert not getattr(ProgressiveTax, "__parameters__", ())


def test_mypy_rejects_wiring_an_artifact_kind_of_another_value_type() -> None:
    count = ArtifactKind("ex/count", int)
    # An ArtifactKind[int] is not Money; the ignore fails under mypy (warn_unused_ignores) if
    # wiring an artifact kind of another value type is ever accepted.
    ProgressiveTax(count, BASIC_TAX, SCHEDULE, NO_ROUNDING)  # type: ignore[arg-type]


class Cents(Decimal):
    """A made-up Decimal subtype, to probe ArtifactKind's variance."""


CENTS = ArtifactKind("ex/cents", Cents)  # bound to a name: built inline it would infer Decimal


def test_mypy_rejects_wiring_an_artifact_kind_of_a_value_subtype() -> None:
    # `ArtifactKind` is invariant, so an ArtifactKind[Cents] is not Money; if `ArtifactKind` ever
    # became covariant this ignore would be unused and mypy (strict) would fail.
    ProgressiveTax(CENTS, BASIC_TAX, SCHEDULE, NO_ROUNDING)  # type: ignore[arg-type]
