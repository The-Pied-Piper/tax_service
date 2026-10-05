"""Unit tests for artifacts: a class is an identity, an instance a value (design.md §2)."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from decimal import Decimal

import pytest

from app.domain.artifact import Amount, Artifact


class TaxableBase(Amount):
    """Made-up artifact for these tests."""


class BasicTax(Amount):
    """Made-up artifact for these tests."""


class RRSPLikeDeduction(Amount):
    """Made-up artifact whose name starts with an acronym."""


def test_an_instance_carries_its_value() -> None:
    assert TaxableBase(Decimal("2.5")).value == Decimal("2.5")


def test_an_amount_must_be_a_decimal() -> None:
    with pytest.raises(TypeError, match="TaxableBase must be a Decimal, got float"):
        TaxableBase(2.5)  # type: ignore[arg-type]


def test_values_are_equal_by_artifact_and_value() -> None:
    assert TaxableBase(Decimal(1)) == TaxableBase(Decimal(1))
    assert TaxableBase(Decimal(1)) != TaxableBase(Decimal(2))
    other_artifact: Artifact = BasicTax(Decimal(1))  # mypy already rejects comparing the two
    assert TaxableBase(Decimal(1)) != other_artifact
    assert len({TaxableBase(Decimal(1)), TaxableBase(Decimal(1))}) == 1


def test_values_are_immutable() -> None:
    value = TaxableBase(Decimal(1))

    with pytest.raises(FrozenInstanceError):
        value.value = Decimal(2)  # type: ignore[misc]


@pytest.mark.parametrize("value_type", [Artifact, Amount])
def test_value_types_hold_no_value_themselves(value_type: type[Artifact]) -> None:
    with pytest.raises(TypeError, match="not an artifact"):
        value_type(Decimal(1))


def test_an_artifact_cannot_subclass_another_artifact() -> None:
    with pytest.raises(TypeError, match="must subclass a value type"):

        class NarrowerBase(TaxableBase):
            pass


@pytest.mark.parametrize(
    ("artifact", "label"),
    [
        (TaxableBase, "taxable_base"),
        (BasicTax, "basic_tax"),
        (RRSPLikeDeduction, "rrsp_like_deduction"),
    ],
)
def test_label_is_the_class_name_in_snake_case(artifact: type[Artifact], label: str) -> None:
    assert artifact.label() == label
