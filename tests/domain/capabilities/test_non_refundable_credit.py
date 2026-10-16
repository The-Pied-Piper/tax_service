"""Unit tests for the NonRefundableCredit capability, with made-up values.

Its slots: parameters `amount` (a `credit` dataset holding the credit amount) and `rate` (a `rate`
dataset), consumed `tax` and produced `output`. The credit is amount × rate, rounded with the
`amount` dataset's rule; the rate dataset's rule is never applied.
"""

from __future__ import annotations

from collections.abc import Mapping
from decimal import Decimal
from types import MappingProxyType
from typing import Any, assert_type, cast

import pytest

from app.domain.artifact import Artifact, ArtifactKind
from app.domain.capabilities.non_refundable_credit import NonRefundableCredit
from app.domain.capability import TraceLine
from app.domain.errors import InvalidCapabilityError
from app.domain.parameters.credit import CREDIT, Credit
from app.domain.parameters.datasets import ParameterDataset
from app.domain.parameters.kind import ParameterKind
from app.domain.parameters.rate import RATE, Rate
from app.domain.parameters.rounding import NO_ROUNDING, RoundingMode, RoundingRule, RoundTo

D = Decimal
CENT = RoundTo(D("0.01"), RoundingMode.HALF_UP)


BASIC_TAX = ArtifactKind("ex/basic_tax", Decimal)
TAX_AFTER_CREDIT = ArtifactKind("ex/tax_after_credit", Decimal)


def amount(value: str = "1000", rounding: RoundingRule = NO_ROUNDING) -> ParameterDataset[Credit]:
    return ParameterDataset(
        "ex/personal_credit", 2025, CREDIT, Credit(D(value)), rounding, ("https://example.org/c",)
    )


def rate(value: str = "0.125", rounding: RoundingRule = NO_ROUNDING) -> ParameterDataset[Rate]:
    return ParameterDataset(
        "ex/credit_rate", 2025, RATE, Rate(D(value)), rounding, ("https://example.org/r",)
    )


def capability(
    amount_data: ParameterDataset[Credit] | None = None,
    rate_data: ParameterDataset[Rate] | None = None,
) -> NonRefundableCredit:
    """By default 12.5% of 1000: a credit worth 125."""
    return NonRefundableCredit(
        BASIC_TAX, TAX_AFTER_CREDIT, amount_data or amount(), rate_data or rate()
    )


def test_declares_its_contract() -> None:
    assert capability().consumes == frozenset({BASIC_TAX})
    assert capability().produces == frozenset({TAX_AFTER_CREDIT})


def test_leaves_its_contract_to_the_base() -> None:
    assert "consumes" not in vars(NonRefundableCredit)
    assert "produces" not in vars(NonRefundableCredit)


def test_rejects_one_kind_as_both_tax_and_output() -> None:
    with pytest.raises(InvalidCapabilityError, match="NonRefundableCredit") as raised:
        NonRefundableCredit(BASIC_TAX, BASIC_TAX, amount(), rate())

    message = str(raised.value)
    assert "'tax'" in message
    assert "'output'" in message


def test_subtracts_the_credit_from_tax() -> None:
    assert capability().compute((Artifact(BASIC_TAX, D("500")),)).outputs == (
        Artifact(TAX_AFTER_CREDIT, D("375.000")),
    )


def test_never_reduces_tax_below_zero() -> None:
    assert capability().compute((Artifact(BASIC_TAX, D("100")),)).outputs == (
        Artifact(TAX_AFTER_CREDIT, D("0")),
    )


def test_zero_tax_stays_zero() -> None:
    assert capability().compute((Artifact(BASIC_TAX, D("0")),)).outputs == (
        Artifact(TAX_AFTER_CREDIT, D("0")),
    )


def test_rounds_the_credit_with_the_amount_datasets_rule() -> None:
    wired = capability(amount("1000.05", CENT), rate("0.1"))  # 100.005

    result = wired.compute((Artifact(BASIC_TAX, D("500")),))

    assert result.outputs == (Artifact(TAX_AFTER_CREDIT, D("399.99")),)


def test_ignores_the_rate_datasets_rounding_rule() -> None:
    wired = capability(amount("1000.05"), rate("0.1", CENT))  # 100.005, kept exact

    result = wired.compute((Artifact(BASIC_TAX, D("500")),))

    assert result.outputs == (Artifact(TAX_AFTER_CREDIT, D("399.995")),)


def test_traces_the_credit_and_the_result() -> None:
    trace = capability().compute((Artifact(BASIC_TAX, D("500")),)).trace

    assert trace == (
        TraceLine("credit: 12.5% of 1000 (no rounding)", D("125.000")),
        TraceLine("tax_after_credit: basic_tax 500 less credit, not below 0", D("375.000")),
    )


def test_traces_the_amount_datasets_rounding_rule() -> None:
    trace = (
        capability(amount("1000.05", CENT), rate("0.1"))
        .compute((Artifact(BASIC_TAX, D("500")),))
        .trace
    )

    assert trace[0] == TraceLine("credit: 10% of 1000.05 (half-up to 0.01)", D("100.01"))


def test_traces_the_unused_part_when_the_credit_exceeds_tax() -> None:
    trace = capability().compute((Artifact(BASIC_TAX, D("100")),)).trace

    assert trace[-1] == TraceLine("unused credit, not refunded", D("25.000"))


def test_rejects_negative_tax() -> None:
    with pytest.raises(ValueError, match="basic_tax must not be negative"):
        capability().compute((Artifact(BASIC_TAX, D("-1")),))


def test_declares_its_slots() -> None:
    assert NonRefundableCredit.PARAMETERS == {"amount": CREDIT, "rate": RATE}
    assert NonRefundableCredit.PARAMETERS["amount"] is CREDIT
    assert NonRefundableCredit.PARAMETERS["rate"] is RATE
    assert NonRefundableCredit.CONSUMES == {"tax": Decimal}
    assert NonRefundableCredit.PRODUCES == {"output": Decimal}


def test_its_slots_are_read_only() -> None:
    for slots in (
        NonRefundableCredit.PARAMETERS,
        NonRefundableCredit.CONSUMES,
        NonRefundableCredit.PRODUCES,
    ):
        assert isinstance(slots, MappingProxyType)


def test_its_slots_are_typed_as_read_only_mappings() -> None:
    assert_type(NonRefundableCredit.PARAMETERS, Mapping[str, ParameterKind[Any]])
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


def test_is_built_from_its_slot_names_as_keywords() -> None:
    wired = NonRefundableCredit(
        tax=BASIC_TAX, output=TAX_AFTER_CREDIT, amount=amount(), rate=rate()
    )

    result = wired.compute((Artifact(BASIC_TAX, D("500")),))

    assert result.outputs == (Artifact(TAX_AFTER_CREDIT, D("375.000")),)


def test_takes_no_separate_rounding_argument() -> None:
    with pytest.raises(TypeError):
        NonRefundableCredit(  # type: ignore[call-arg]
            BASIC_TAX, TAX_AFTER_CREDIT, amount(), rate(), NO_ROUNDING
        )


def test_is_not_generic_over_artifacts() -> None:
    assert not getattr(NonRefundableCredit, "__type_params__", ())
    assert not getattr(NonRefundableCredit, "__parameters__", ())


def test_mypy_rejects_wiring_an_artifact_kind_of_another_value_type() -> None:
    count = ArtifactKind("ex/count", int)
    # An ArtifactKind[int] is not Money; the ignore fails under mypy (warn_unused_ignores) if
    # wiring an artifact kind of another value type is ever accepted. At run time, building it
    # fails too.
    with pytest.raises(InvalidCapabilityError, match="NonRefundableCredit.*'tax'"):
        NonRefundableCredit(count, TAX_AFTER_CREDIT, amount(), rate())  # type: ignore[arg-type]


class Cents(Decimal):
    """A made-up Decimal subtype, to probe ArtifactKind's variance."""


CENTS = ArtifactKind("ex/cents", Cents)  # bound to a name: built inline it would infer Decimal


def test_mypy_rejects_wiring_an_artifact_kind_of_a_value_subtype() -> None:
    # `ArtifactKind` is invariant, so an ArtifactKind[Cents] is not Money; if `ArtifactKind` ever
    # became covariant this ignore would be unused and mypy (strict) would fail. At run time,
    # building it fails too: the value type must match the slot's exactly.
    with pytest.raises(InvalidCapabilityError, match="NonRefundableCredit.*'tax'"):
        NonRefundableCredit(CENTS, TAX_AFTER_CREDIT, amount(), rate())  # type: ignore[arg-type]


def test_mypy_rejects_swapping_the_amount_and_rate_datasets() -> None:
    def wire() -> None:  # type-checked, never run
        # A rate dataset is not a ParameterDataset[Credit], nor the reverse; each ignore fails
        # under mypy (warn_unused_ignores) if the swap is ever accepted.
        NonRefundableCredit(
            BASIC_TAX,
            TAX_AFTER_CREDIT,
            rate(),  # type: ignore[arg-type]
            amount(),  # type: ignore[arg-type]
        )

    assert callable(wire)
