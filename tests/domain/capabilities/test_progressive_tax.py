"""Unit tests for the ProgressiveTax capability, with made-up brackets.

Its slots: parameter `schedule` (a brackets dataset, whose rounding rule it applies to the total),
consumed `base` and produced `output`.
"""

from __future__ import annotations

from collections.abc import Mapping
from decimal import Decimal
from types import MappingProxyType
from typing import Any, assert_type, cast

import pytest

from app.domain.artifact import Artifact, ArtifactKind
from app.domain.capabilities.progressive_tax import ProgressiveTax
from app.domain.capability import TraceLine
from app.domain.parameters.brackets import BRACKETS, Bracket, BracketSchedule
from app.domain.parameters.credit import CREDIT, Credit
from app.domain.parameters.datasets import ParameterDataset
from app.domain.parameters.kind import ParameterKind
from app.domain.parameters.rounding import NO_ROUNDING, RoundingMode, RoundingRule, RoundTo

D = Decimal


TAXABLE_BASE = ArtifactKind("ex/taxable_base", Decimal)
BASIC_TAX = ArtifactKind("ex/basic_tax", Decimal)
OTHER_BASE = ArtifactKind("ex/other_base", Decimal)
OTHER_TAX = ArtifactKind("ex/other_tax", Decimal)


SCHEDULE = BracketSchedule(
    (Bracket(D(0), D("0.10")), Bracket(D(100), D("0.20")), Bracket(D(300), D("0.30")))
)


def schedule(rounding: RoundingRule = NO_ROUNDING) -> ParameterDataset[BracketSchedule]:
    return ParameterDataset(
        "ex/brackets", 2025, BRACKETS, SCHEDULE, rounding, ("https://example.org/rates",)
    )


def capability(rounding: RoundingRule = NO_ROUNDING) -> ProgressiveTax:
    return ProgressiveTax(TAXABLE_BASE, BASIC_TAX, schedule(rounding))


def test_declares_its_contract() -> None:
    assert capability().consumes == frozenset({TAXABLE_BASE})
    assert capability().produces == frozenset({BASIC_TAX})


def test_produces_tax_on_the_base() -> None:
    result = capability().compute((Artifact(TAXABLE_BASE, D(250)),))

    assert result.outputs == (Artifact(BASIC_TAX, D("40.0")),)


def test_the_same_capability_serves_different_wiring() -> None:
    wired = ProgressiveTax(OTHER_BASE, OTHER_TAX, schedule())

    result = wired.compute((Artifact(OTHER_BASE, D(50)),))

    assert result.outputs == (Artifact(OTHER_TAX, D("5.0")),)


def test_rounds_once_at_the_end_with_the_schedules_rule() -> None:
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


def test_declares_its_slots() -> None:
    assert ProgressiveTax.PARAMETERS == {"schedule": BRACKETS}
    assert ProgressiveTax.PARAMETERS["schedule"] is BRACKETS
    assert ProgressiveTax.CONSUMES == {"base": Decimal}
    assert ProgressiveTax.PRODUCES == {"output": Decimal}


def test_its_slots_are_read_only() -> None:
    for slots in (ProgressiveTax.PARAMETERS, ProgressiveTax.CONSUMES, ProgressiveTax.PRODUCES):
        assert isinstance(slots, MappingProxyType)


def test_its_slots_are_typed_as_read_only_mappings() -> None:
    assert_type(ProgressiveTax.PARAMETERS, Mapping[str, ParameterKind[BracketSchedule]])
    assert_type(ProgressiveTax.CONSUMES, Mapping[str, type])
    assert_type(ProgressiveTax.PRODUCES, Mapping[str, type])


def test_its_slots_cannot_be_changed() -> None:
    for slots in (ProgressiveTax.PARAMETERS, ProgressiveTax.CONSUMES, ProgressiveTax.PRODUCES):
        with pytest.raises(TypeError):
            cast(Any, slots)["extra"] = Decimal


def test_is_built_from_its_slot_names_as_keywords() -> None:
    wired = ProgressiveTax(base=TAXABLE_BASE, output=BASIC_TAX, schedule=schedule())

    result = wired.compute((Artifact(TAXABLE_BASE, D(250)),))

    assert result.outputs == (Artifact(BASIC_TAX, D("40.0")),)


def test_takes_no_separate_rounding_argument() -> None:
    with pytest.raises(TypeError):
        ProgressiveTax(TAXABLE_BASE, BASIC_TAX, schedule(), NO_ROUNDING)  # type: ignore[call-arg]


def test_is_not_generic_over_artifacts() -> None:
    assert not getattr(ProgressiveTax, "__type_params__", ())
    assert not getattr(ProgressiveTax, "__parameters__", ())


def test_mypy_rejects_wiring_an_artifact_kind_of_another_value_type() -> None:
    count = ArtifactKind("ex/count", int)
    # An ArtifactKind[int] is not Money; the ignore fails under mypy (warn_unused_ignores) if
    # wiring an artifact kind of another value type is ever accepted.
    ProgressiveTax(count, BASIC_TAX, schedule())  # type: ignore[arg-type]


class Cents(Decimal):
    """A made-up Decimal subtype, to probe ArtifactKind's variance."""


CENTS = ArtifactKind("ex/cents", Cents)  # bound to a name: built inline it would infer Decimal


def test_mypy_rejects_wiring_an_artifact_kind_of_a_value_subtype() -> None:
    # `ArtifactKind` is invariant, so an ArtifactKind[Cents] is not Money; if `ArtifactKind` ever
    # became covariant this ignore would be unused and mypy (strict) would fail.
    ProgressiveTax(CENTS, BASIC_TAX, schedule())  # type: ignore[arg-type]


def test_mypy_rejects_a_dataset_of_another_kind_for_the_schedule() -> None:
    credit = ParameterDataset("ex/credit", 2025, CREDIT, Credit(D(1)), NO_ROUNDING, ("src",))

    def wire() -> None:  # type-checked, never run
        # A credit dataset is not a ParameterDataset[BracketSchedule]; the ignore fails under
        # mypy (warn_unused_ignores) if it is ever accepted.
        ProgressiveTax(TAXABLE_BASE, BASIC_TAX, credit)  # type: ignore[arg-type]

    assert callable(wire)


def test_mypy_rejects_a_bare_schedule_without_its_dataset() -> None:
    def wire() -> None:  # type-checked, never run
        # Parameter slots take the dataset, which carries the rounding rule; never bare values.
        ProgressiveTax(TAXABLE_BASE, BASIC_TAX, SCHEDULE)  # type: ignore[arg-type]

    assert callable(wire)
