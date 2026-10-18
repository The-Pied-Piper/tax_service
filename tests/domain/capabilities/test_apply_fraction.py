"""Unit tests for the ApplyFraction capability (`core/apply_fraction`), made-up kinds and values.

Its slots: one parameter slot `fraction` (a `fraction` dataset), one consumed slot `base` and one
produced slot `output`. The output is `rounding.apply(base × numerator / denominator)`, multiplied
before it divides, so the one division is the only inexact step and the quotient is carried
unrounded (the Decimal context's precision is its only limit), rounded only with the `fraction`
dataset's rule (which defaults to no rounding); it records one `FractionAppliedLine`.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import fields
from decimal import Decimal
from types import MappingProxyType
from typing import Any, assert_type, cast

import pytest

import app.domain.capabilities as core
from app.domain.artifact import Artifact, ArtifactKind
from app.domain.capabilities.apply_fraction import ApplyFraction
from app.domain.capability import CapabilityRegistry
from app.domain.errors import InvalidCapabilityError, MissingArtifactError
from app.domain.parameters.datasets import ParameterDataset
from app.domain.parameters.fraction import FRACTION, Fraction
from app.domain.parameters.kind import ParameterKind
from app.domain.parameters.rate import RATE, Rate
from app.domain.parameters.rounding import NO_ROUNDING, RoundingMode, RoundingRule, RoundTo
from app.domain.trace import FractionAppliedLine

D = Decimal
CENT = RoundTo(D("0.01"), RoundingMode.HALF_UP)


EARNED = ArtifactKind("ex/earned_income", Decimal)
PORTION = ArtifactKind("ex/earned_portion", Decimal)


def fraction(
    numerator: int = 2, denominator: int = 3, rounding: RoundingRule = NO_ROUNDING
) -> ParameterDataset[Fraction]:
    """By default two-thirds, exact."""
    return ParameterDataset(
        "ex/portion_fraction",
        2025,
        FRACTION,
        Fraction(numerator, denominator),
        rounding,
        ("https://example.org/f",),
    )


def capability(fraction_data: ParameterDataset[Fraction] | None = None) -> ApplyFraction:
    """By default two-thirds of the made-up earned income, exact."""
    return ApplyFraction(fraction_data or fraction(), EARNED, PORTION)


def compute(wired: ApplyFraction, base: str) -> Artifact[Any]:
    (output,) = wired.compute((Artifact(EARNED, D(base)),)).outputs
    return output


def test_is_registered_as_core_apply_fraction() -> None:
    assert CapabilityRegistry.shared().get("core/apply_fraction") is ApplyFraction


def test_is_exported_from_the_capabilities_package() -> None:
    assert "apply_fraction" in core.__all__
    assert core.apply_fraction.ApplyFraction is ApplyFraction


def test_declares_its_contract() -> None:
    assert capability().consumes == frozenset({EARNED})
    assert capability().produces == frozenset({PORTION})


def test_leaves_its_contract_to_the_base() -> None:
    assert "consumes" not in vars(ApplyFraction)
    assert "produces" not in vars(ApplyFraction)


def test_declares_its_slots() -> None:
    assert ApplyFraction.PARAMETERS == {"fraction": FRACTION}
    assert ApplyFraction.PARAMETERS["fraction"] is FRACTION
    assert ApplyFraction.CONSUMES == {"base": Decimal}
    assert ApplyFraction.PRODUCES == {"output": Decimal}
    assert not ApplyFraction.is_list_slot("base")


def test_its_slots_are_read_only() -> None:
    for slots in (ApplyFraction.PARAMETERS, ApplyFraction.CONSUMES, ApplyFraction.PRODUCES):
        assert isinstance(slots, MappingProxyType)


def test_its_slots_are_typed_as_read_only_mappings() -> None:
    assert_type(ApplyFraction.PARAMETERS, Mapping[str, ParameterKind[Fraction]])
    assert_type(ApplyFraction.CONSUMES, Mapping[str, type])
    assert_type(ApplyFraction.PRODUCES, Mapping[str, type])


def test_its_slots_cannot_be_changed() -> None:
    for slots in (ApplyFraction.PARAMETERS, ApplyFraction.CONSUMES, ApplyFraction.PRODUCES):
        with pytest.raises(TypeError):
            cast(Any, slots)["extra"] = Decimal


def test_is_built_from_its_slot_names_as_keywords() -> None:
    wired = ApplyFraction(fraction=fraction(), base=EARNED, output=PORTION)

    assert compute(wired, "60000") == Artifact(PORTION, D("40000"))


def test_takes_no_separate_rounding_argument() -> None:
    with pytest.raises(TypeError):
        ApplyFraction(fraction(), EARNED, PORTION, NO_ROUNDING)  # type: ignore[call-arg]


def test_rejects_one_kind_as_both_base_and_output() -> None:
    with pytest.raises(InvalidCapabilityError, match="ApplyFraction") as raised:
        ApplyFraction(fraction(), EARNED, EARNED)

    message = str(raised.value)
    assert "'base'" in message
    assert "'output'" in message


def test_rejects_a_list_of_kinds_for_its_base() -> None:
    with pytest.raises(InvalidCapabilityError, match="ApplyFraction.*'base'"):
        ApplyFraction(fraction(), (EARNED,), PORTION)  # type: ignore[arg-type]


def test_mypy_rejects_wiring_an_artifact_kind_of_another_value_type() -> None:
    count = ArtifactKind("ex/count", int)
    # An ArtifactKind[int] is not Money; the ignore fails under mypy (warn_unused_ignores) if
    # wiring an artifact kind of another value type is ever accepted. At run time, building it
    # fails too.
    with pytest.raises(InvalidCapabilityError, match="ApplyFraction.*'base'"):
        ApplyFraction(fraction(), count, PORTION)  # type: ignore[arg-type]


def test_mypy_rejects_a_dataset_of_another_parameter_kind() -> None:
    def wire() -> None:  # type-checked, never run
        # A rate dataset is not a ParameterDataset[Fraction]; the ignore fails under mypy
        # (warn_unused_ignores) if it is ever accepted.
        rate = ParameterDataset(
            "ex/some_rate", 2025, RATE, Rate(D("0.5")), NO_ROUNDING, ("https://example.org/r",)
        )
        ApplyFraction(rate, EARNED, PORTION)  # type: ignore[arg-type]

    assert callable(wire)


def test_is_not_generic_over_artifacts() -> None:
    assert not getattr(ApplyFraction, "__type_params__", ())
    assert not getattr(ApplyFraction, "__parameters__", ())


# --- computing --------------------------------------------------------------------------------


def test_produces_the_base_times_the_fraction() -> None:
    # 60000 × 2 / 3 = 40000, exactly.
    output = compute(capability(), "60000")

    assert output == Artifact(PORTION, D("40000"))
    assert str(output.value) == "40000"
    assert type(output.value) is Decimal


def test_carries_an_inexact_quotient_unrounded_to_the_contexts_precision() -> None:
    # 50000 × 2 / 3 = 33333.333... has no finite expansion: the quotient is carried to the Decimal
    # context's 28 significant digits, unrounded by any rule. Dividing first (50000 / 3 × 2) or
    # multiplying by a quotient (50000 × (2 / 3)) would end in ...334 instead.
    output = compute(capability(), "50000")

    assert output == Artifact(PORTION, D("33333.33333333333333333333333"))
    assert str(output.value) == "33333.33333333333333333333333"


def test_multiplies_before_it_divides_so_an_even_quotient_stays_exact() -> None:
    # 3 × 1 / 3 = 1 exactly; dividing first (3 × (1 / 3)) would give 0.9999999999999999999999999999.
    output = compute(capability(fraction(1, 3)), "3")

    assert output == Artifact(PORTION, D("1"))
    assert str(output.value) == "1"


def test_keeps_the_product_exact_without_rounding() -> None:
    # 1000.05 × 2 / 3 = 666.7, exact, not rounded.
    assert compute(capability(), "1000.05") == Artifact(PORTION, D("666.7"))


def test_rounds_with_the_fraction_datasets_rule() -> None:
    wired = capability(fraction(rounding=CENT))

    # 33333.33333333333333333333333 half-up to 33333.33.
    assert compute(wired, "50000") == Artifact(PORTION, D("33333.33"))


def test_rounds_with_another_rule_of_the_fraction_dataset() -> None:
    wired = capability(fraction(rounding=RoundTo(D("1"), RoundingMode.CEILING)))

    # 33333.333... up to 33334.
    assert compute(wired, "50000") == Artifact(PORTION, D("33334"))


def test_a_rounded_output_carries_the_increments_scale() -> None:
    wired = capability(fraction(rounding=CENT))

    assert str(compute(wired, "60000").value) == "40000.00"


def test_a_fraction_of_one_produces_the_base() -> None:
    assert compute(capability(fraction(3, 3)), "1234.56") == Artifact(PORTION, D("1234.56"))


def test_a_fraction_above_one_multiplies_up() -> None:
    assert compute(capability(fraction(3, 2)), "1000") == Artifact(PORTION, D("1500"))


def test_four_sixths_and_two_thirds_give_equal_results() -> None:
    # 4/6 is two-thirds; 1000 × 4 / 6 is the same quotient as 1000 × 2 / 3.
    assert compute(capability(fraction(4, 6)), "1000") == compute(capability(), "1000")


def test_a_zero_base_produces_zero() -> None:
    output = compute(capability(), "0")

    assert output == Artifact(PORTION, D("0"))
    assert type(output.value) is Decimal


def test_the_fraction_dataset_supplies_the_fraction() -> None:
    assert compute(capability(fraction(1, 4)), "1000") == Artifact(PORTION, D("250"))


def test_ignores_artifacts_it_does_not_consume() -> None:
    other = ArtifactKind("ex/other", Decimal)

    result = capability().compute((Artifact(other, D("9")), Artifact(EARNED, D("60000"))))

    assert result.outputs == (Artifact(PORTION, D("40000")),)


def test_a_missing_base_is_a_missing_artifact() -> None:
    with pytest.raises(MissingArtifactError, match="earned_income"):
        capability().compute(())


# --- trace ------------------------------------------------------------------------------------


def test_traces_one_fraction_applied_line() -> None:
    trace = capability().compute((Artifact(EARNED, D("60000")),)).trace

    assert trace == (
        FractionAppliedLine(
            output=PORTION,
            base=EARNED,
            base_amount=D("60000"),
            fraction=Fraction(2, 3),
            rounding=NO_ROUNDING,
            result=D("40000"),
        ),
    )


def test_traces_the_fraction_datasets_rounding_rule_and_the_rounded_result() -> None:
    trace = capability(fraction(rounding=CENT)).compute((Artifact(EARNED, D("50000")),)).trace

    assert trace == (
        FractionAppliedLine(PORTION, EARNED, D("50000"), Fraction(2, 3), CENT, D("33333.33")),
    )


def test_trace_amount_is_the_result() -> None:
    trace = capability(fraction(rounding=CENT)).compute((Artifact(EARNED, D("50000")),)).trace

    assert [line.amount for line in trace] == [D("33333.33")]


def test_trace_holds_no_text() -> None:
    trace = capability().compute((Artifact(EARNED, D("60000")),)).trace

    for line in trace:
        assert not any(isinstance(getattr(line, f.name), str) for f in fields(line))
