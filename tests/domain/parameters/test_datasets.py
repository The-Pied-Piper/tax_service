"""Unit tests for ParameterDataset: one family's values of one kind for one tax year."""

from __future__ import annotations

from decimal import Decimal

import pytest

from app.domain.parameters.credit import CREDIT, Credit
from app.domain.parameters.datasets import ParameterDataset
from app.domain.parameters.kind import ParameterKind
from app.domain.parameters.rounding import NO_ROUNDING


def test_holds_values_of_its_kind() -> None:
    credit = Credit(amount=Decimal(1), rate=Decimal("0.1"))

    dataset = ParameterDataset("ex/credit", 2025, CREDIT, credit, NO_ROUNDING, ("src",))

    assert dataset.values is credit


def test_rejects_values_of_another_type() -> None:
    with pytest.raises(TypeError, match="credit dataset values must be a Credit, got Decimal"):
        ParameterDataset(
            "ex/credit",
            2025,
            CREDIT,
            Decimal(1),
            NO_ROUNDING,
            ("src",),
        )


def test_works_for_any_kind() -> None:
    rate = ParameterKind("flat_rate", Decimal)

    dataset = ParameterDataset("ex/rate", 2025, rate, Decimal("0.2"), NO_ROUNDING, ("src",))

    assert dataset.values == Decimal("0.2")
