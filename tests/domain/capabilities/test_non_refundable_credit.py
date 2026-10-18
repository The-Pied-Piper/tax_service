"""Unit tests for the NonRefundableCredit capability (`core/non_refundable_credit`), made up.

Its slots: one parameter slot `rate` (a `rate` dataset), consumed `amounts` (the summed
credit amounts, an artifact) and `tax`, produced `output`. The credit is amounts × rate, applied
once and rounded with the `rate` dataset's rule; the output is tax less the credit, not below zero,
and the part of the credit the tax cannot absorb is lost, not refunded.
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
from app.domain.capabilities.non_refundable_credit import NonRefundableCredit
from app.domain.capability import CapabilityRegistry
from app.domain.errors import InvalidCapabilityError, MissingArtifactError
from app.domain.parameters.credit import CREDIT, Credit
from app.domain.parameters.datasets import ParameterDataset
from app.domain.parameters.kind import ParameterKind
from app.domain.parameters.rate import RATE, Rate
from app.domain.parameters.rounding import NO_ROUNDING, RoundingMode, RoundingRule, RoundTo
from app.domain.trace import CreditAppliedLine, CreditLine, UnusedCreditLine

D = Decimal
CENT = RoundTo(D("0.01"), RoundingMode.HALF_UP)


CREDIT_AMOUNTS = ArtifactKind("ex/credit_amounts", Decimal)
BASIC_TAX = ArtifactKind("ex/basic_tax", Decimal)
TAX_AFTER_CREDIT = ArtifactKind("ex/tax_after_credit", Decimal)


def rate(value: str = "0.125", rounding: RoundingRule = NO_ROUNDING) -> ParameterDataset[Rate]:
    return ParameterDataset(
        "ex/credit_rate", 2025, RATE, Rate(D(value)), rounding, ("https://example.org/r",)
    )


def capability(rate_data: ParameterDataset[Rate] | None = None) -> NonRefundableCredit:
    """By default 12.5% of the summed credit amounts, exact."""
    return NonRefundableCredit(rate_data or rate(), CREDIT_AMOUNTS, BASIC_TAX, TAX_AFTER_CREDIT)


def inputs(amounts: str, tax: str) -> tuple[Artifact[Decimal], ...]:
    return (Artifact(CREDIT_AMOUNTS, D(amounts)), Artifact(BASIC_TAX, D(tax)))


def compute(amounts: str, tax: str, wired: NonRefundableCredit | None = None) -> Artifact[Any]:
    (output,) = (wired or capability()).compute(inputs(amounts, tax)).outputs
    return output


# --- registration and contract ----------------------------------------------------------------


def test_is_registered_as_core_non_refundable_credit() -> None:
    assert CapabilityRegistry.shared().get("core/non_refundable_credit") is NonRefundableCredit


def test_is_exported_from_the_capabilities_package() -> None:
    assert "non_refundable_credit" in core.__all__
    assert core.non_refundable_credit.NonRefundableCredit is NonRefundableCredit


def test_declares_its_contract() -> None:
    assert capability().consumes == frozenset({CREDIT_AMOUNTS, BASIC_TAX})
    assert capability().produces == frozenset({TAX_AFTER_CREDIT})


def test_leaves_its_contract_to_the_base() -> None:
    assert "consumes" not in vars(NonRefundableCredit)
    assert "produces" not in vars(NonRefundableCredit)


def test_declares_its_slots() -> None:
    assert NonRefundableCredit.PARAMETERS == {"rate": RATE}
    assert NonRefundableCredit.PARAMETERS["rate"] is RATE
    assert NonRefundableCredit.CONSUMES == {"amounts": Decimal, "tax": Decimal}
    assert NonRefundableCredit.PRODUCES == {"output": Decimal}
    assert not NonRefundableCredit.is_list_slot("amounts")
    assert not NonRefundableCredit.is_list_slot("tax")


def test_has_no_credit_amount_parameter_slot() -> None:
    # The amounts arrive summed, as an artifact; no `credit` dataset reaches this capability.
    assert "amount" not in NonRefundableCredit.PARAMETERS
    assert CREDIT not in cast(Any, NonRefundableCredit.PARAMETERS).values()


def test_its_slots_are_read_only() -> None:
    for slots in (
        NonRefundableCredit.PARAMETERS,
        NonRefundableCredit.CONSUMES,
        NonRefundableCredit.PRODUCES,
    ):
        assert isinstance(slots, MappingProxyType)


def test_its_slots_are_typed_as_read_only_mappings() -> None:
    assert_type(NonRefundableCredit.PARAMETERS, Mapping[str, ParameterKind[Rate]])
    assert_type(NonRefundableCredit.CONSUMES, Mapping[str, type])
    assert_type(NonRefundableCredit.PRODUCES, Mapping[str, type])


def test_its_slots_cannot_be_changed() -> None:
    for slots in (
        NonRefundableCredit.PARAMETERS,
        NonRefundableCredit.CONSUMES,
        NonRefundableCredit.PRODUCES,
    ):
        with pytest.raises(TypeError):
            cast(Any, slots)["extra"] = Decimal


# --- building ---------------------------------------------------------------------------------


def test_is_built_from_its_slot_names_as_keywords() -> None:
    wired = NonRefundableCredit(
        rate=rate(), amounts=CREDIT_AMOUNTS, tax=BASIC_TAX, output=TAX_AFTER_CREDIT
    )

    assert compute("1000", "500", wired) == Artifact(TAX_AFTER_CREDIT, D("375.000"))


def test_is_built_positionally_as_rate_amounts_tax_output() -> None:
    wired = NonRefundableCredit(rate(), CREDIT_AMOUNTS, BASIC_TAX, TAX_AFTER_CREDIT)

    assert wired.consumes == frozenset({CREDIT_AMOUNTS, BASIC_TAX})
    assert wired.produces == frozenset({TAX_AFTER_CREDIT})


def test_takes_no_credit_amount_dataset() -> None:
    amount = ParameterDataset(
        "ex/personal_credit", 2025, CREDIT, Credit(D("1000")), NO_ROUNDING, ("https://example.org",)
    )
    with pytest.raises(TypeError):
        NonRefundableCredit(  # type: ignore[call-arg]
            rate=rate(),
            amounts=CREDIT_AMOUNTS,
            tax=BASIC_TAX,
            output=TAX_AFTER_CREDIT,
            amount=amount,
        )


def test_takes_no_separate_rounding_argument() -> None:
    with pytest.raises(TypeError):
        NonRefundableCredit(  # type: ignore[call-arg]
            rate(), CREDIT_AMOUNTS, BASIC_TAX, TAX_AFTER_CREDIT, NO_ROUNDING
        )


def test_rejects_one_kind_as_both_tax_and_output() -> None:
    with pytest.raises(InvalidCapabilityError, match="NonRefundableCredit") as raised:
        NonRefundableCredit(rate(), CREDIT_AMOUNTS, BASIC_TAX, BASIC_TAX)

    message = str(raised.value)
    assert "'tax'" in message
    assert "'output'" in message


def test_rejects_one_kind_as_both_amounts_and_tax() -> None:
    with pytest.raises(InvalidCapabilityError, match="NonRefundableCredit") as raised:
        NonRefundableCredit(rate(), BASIC_TAX, BASIC_TAX, TAX_AFTER_CREDIT)

    message = str(raised.value)
    assert "'amounts'" in message
    assert "'tax'" in message


def test_rejects_one_kind_as_both_amounts_and_output() -> None:
    with pytest.raises(InvalidCapabilityError, match="NonRefundableCredit") as raised:
        NonRefundableCredit(rate(), CREDIT_AMOUNTS, BASIC_TAX, CREDIT_AMOUNTS)

    message = str(raised.value)
    assert "'amounts'" in message
    assert "'output'" in message


def test_rejects_a_list_of_kinds_for_its_amounts() -> None:
    with pytest.raises(InvalidCapabilityError, match="NonRefundableCredit.*'amounts'"):
        NonRefundableCredit(
            rate(),
            (CREDIT_AMOUNTS,),  # type: ignore[arg-type]
            BASIC_TAX,
            TAX_AFTER_CREDIT,
        )


def test_is_not_generic_over_artifacts() -> None:
    assert not getattr(NonRefundableCredit, "__type_params__", ())
    assert not getattr(NonRefundableCredit, "__parameters__", ())


def test_mypy_rejects_wiring_an_artifact_kind_of_another_value_type() -> None:
    count = ArtifactKind("ex/count", int)
    # An ArtifactKind[int] is not Money; the ignore fails under mypy (warn_unused_ignores) if
    # wiring an artifact kind of another value type is ever accepted. At run time, building it
    # fails too.
    with pytest.raises(InvalidCapabilityError, match="NonRefundableCredit.*'amounts'"):
        NonRefundableCredit(rate(), count, BASIC_TAX, TAX_AFTER_CREDIT)  # type: ignore[arg-type]
    with pytest.raises(InvalidCapabilityError, match="NonRefundableCredit.*'tax'"):
        NonRefundableCredit(rate(), CREDIT_AMOUNTS, count, TAX_AFTER_CREDIT)  # type: ignore[arg-type]


class Cents(Decimal):
    """A made-up Decimal subtype, to probe ArtifactKind's variance."""


CENTS = ArtifactKind("ex/cents", Cents)  # bound to a name: built inline it would infer Decimal


def test_mypy_rejects_wiring_an_artifact_kind_of_a_value_subtype() -> None:
    # `ArtifactKind` is invariant, so an ArtifactKind[Cents] is not Money; if `ArtifactKind` ever
    # became covariant this ignore would be unused and mypy (strict) would fail. At run time,
    # building it fails too: the value type must match the slot's exactly.
    with pytest.raises(InvalidCapabilityError, match="NonRefundableCredit.*'tax'"):
        NonRefundableCredit(rate(), CREDIT_AMOUNTS, CENTS, TAX_AFTER_CREDIT)  # type: ignore[arg-type]


def test_mypy_rejects_a_dataset_of_another_parameter_kind() -> None:
    def wire() -> None:  # type-checked, never run
        # A credit dataset is not a ParameterDataset[Rate]; the ignore fails under mypy
        # (warn_unused_ignores) if it is ever accepted.
        credit = ParameterDataset(
            "ex/some_credit", 2025, CREDIT, Credit(D("1")), NO_ROUNDING, ("https://example.org/c",)
        )
        NonRefundableCredit(credit, CREDIT_AMOUNTS, BASIC_TAX, TAX_AFTER_CREDIT)  # type: ignore[arg-type]

    assert callable(wire)


# --- computing --------------------------------------------------------------------------------


def test_subtracts_the_amounts_times_the_rate_from_tax() -> None:
    assert compute("1000", "500") == Artifact(TAX_AFTER_CREDIT, D("375.000"))


def test_applies_the_rate_once_to_the_summed_amounts() -> None:
    # 12.5% of 2345.67 = 293.20875, exact without rounding.
    assert compute("2345.67", "1000") == Artifact(TAX_AFTER_CREDIT, D("706.79125"))


def test_the_rate_dataset_supplies_the_rate() -> None:
    wired = capability(rate("0.05"))

    assert compute("1000", "500", wired) == Artifact(TAX_AFTER_CREDIT, D("450.00"))


def test_never_reduces_tax_below_zero() -> None:
    assert compute("1000", "100") == Artifact(TAX_AFTER_CREDIT, D("0"))


def test_a_credit_equal_to_the_tax_leaves_zero() -> None:
    assert compute("1000", "125") == Artifact(TAX_AFTER_CREDIT, D("0"))


def test_zero_tax_stays_zero() -> None:
    assert compute("1000", "0") == Artifact(TAX_AFTER_CREDIT, D("0"))


def test_zero_amounts_leave_the_tax_unchanged() -> None:
    output = compute("0", "500")

    assert output == Artifact(TAX_AFTER_CREDIT, D("500"))
    assert type(output.value) is Decimal


def test_rounds_the_credit_with_the_rate_datasets_rule() -> None:
    wired = capability(rate("0.1", CENT))  # 10% of 1000.05 = 100.005, half-up to 100.01

    assert compute("1000.05", "500", wired) == Artifact(TAX_AFTER_CREDIT, D("399.99"))


def test_rounds_the_credit_with_another_rule_of_the_rate_dataset() -> None:
    wired = capability(rate("0.1", RoundTo(D("1"), RoundingMode.FLOOR)))  # 100.995, floor to 100

    assert compute("1009.95", "500", wired) == Artifact(TAX_AFTER_CREDIT, D("400"))


def test_keeps_the_credit_exact_without_rounding() -> None:
    assert compute("1000.05", "500", capability(rate("0.1"))) == Artifact(
        TAX_AFTER_CREDIT, D("399.995")
    )


def test_rounds_the_credit_not_the_tax() -> None:
    # The credit rounds to 100.01; the tax, 500.333, is not rounded, so neither is the result.
    wired = capability(rate("0.1", CENT))

    assert compute("1000.05", "500.333", wired) == Artifact(TAX_AFTER_CREDIT, D("400.323"))


def test_floors_against_the_rounded_credit() -> None:
    # 10% of 1000.05 = 100.005, rounded to 100.01: more than a tax of 100.006, so 0.
    wired = capability(rate("0.1", CENT))

    assert compute("1000.05", "100.006", wired) == Artifact(TAX_AFTER_CREDIT, D("0"))


def test_multiplies_decimals_float_would_not() -> None:
    assert compute("0.3", "1", capability(rate("0.1"))) == Artifact(TAX_AFTER_CREDIT, D("0.97"))


def test_ignores_artifacts_it_does_not_consume() -> None:
    other = ArtifactKind("ex/other", Decimal)

    result = capability().compute((Artifact(other, D("9")), *inputs("1000", "500")))

    assert result.outputs == (Artifact(TAX_AFTER_CREDIT, D("375.000")),)


def test_a_missing_amounts_artifact_is_a_missing_artifact() -> None:
    with pytest.raises(MissingArtifactError, match="credit_amounts"):
        capability().compute((Artifact(BASIC_TAX, D("500")),))


def test_a_missing_tax_artifact_is_a_missing_artifact() -> None:
    with pytest.raises(MissingArtifactError, match="basic_tax"):
        capability().compute((Artifact(CREDIT_AMOUNTS, D("1000")),))


def test_rejects_negative_tax() -> None:
    with pytest.raises(ValueError, match="basic_tax must not be negative"):
        capability().compute(inputs("1000", "-1"))


def test_rejects_negative_amounts() -> None:
    # A negative sum of credit amounts would raise the tax; it is rejected like a negative tax.
    with pytest.raises(ValueError, match="credit_amounts must not be negative"):
        capability().compute(inputs("-1", "500"))


# --- trace ------------------------------------------------------------------------------------


def test_traces_the_credit_and_the_result() -> None:
    trace = capability().compute(inputs("1000", "500")).trace

    assert trace == (
        CreditLine(
            amounts=CREDIT_AMOUNTS,
            amounts_value=D("1000"),
            rate=Rate(D("0.125")),
            rounding=NO_ROUNDING,
            credit=D("125.000"),
        ),
        CreditAppliedLine(
            output=TAX_AFTER_CREDIT, tax=BASIC_TAX, tax_amount=D("500"), after=D("375.000")
        ),
    )


def test_traces_the_rate_datasets_rounding_rule_and_the_rounded_credit() -> None:
    trace = capability(rate("0.1", CENT)).compute(inputs("1000.05", "500")).trace

    assert trace[0] == CreditLine(CREDIT_AMOUNTS, D("1000.05"), Rate(D("0.1")), CENT, D("100.01"))


def test_traces_the_three_lines_when_the_credit_exceeds_tax() -> None:
    trace = capability().compute(inputs("1000", "100")).trace

    assert trace == (
        CreditLine(CREDIT_AMOUNTS, D("1000"), Rate(D("0.125")), NO_ROUNDING, D("125.000")),
        CreditAppliedLine(TAX_AFTER_CREDIT, BASIC_TAX, D("100"), D("0")),
        UnusedCreditLine(unused=D("25.000")),
    )


def test_traces_the_unused_part_of_the_rounded_credit() -> None:
    trace = capability(rate("0.1", CENT)).compute(inputs("1000.05", "100")).trace

    assert trace[-1] == UnusedCreditLine(D("0.01"))


def test_traces_no_unused_part_when_the_credit_fits() -> None:
    trace = capability().compute(inputs("1000", "125")).trace

    assert not any(isinstance(line, UnusedCreditLine) for line in trace)


def test_trace_amounts_of_its_lines() -> None:
    trace = capability().compute(inputs("1000", "100")).trace

    assert [line.amount for line in trace] == [D("125.000"), D("0"), D("25.000")]


def test_trace_holds_no_text() -> None:
    trace = capability().compute(inputs("1000", "100")).trace

    for line in trace:
        assert not any(isinstance(getattr(line, f.name), str) for f in fields(line))
