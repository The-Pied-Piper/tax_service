"""Unit tests for ParameterKind: names a kind of parameter and the type it produces."""

from __future__ import annotations

from decimal import Decimal

import pytest

from app.domain.parameters.brackets import BRACKETS, BracketSchedule
from app.domain.parameters.credit import CREDIT, Credit
from app.domain.parameters.kind import ParameterKind


def test_built_in_kinds() -> None:
    assert BRACKETS == ParameterKind("brackets", BracketSchedule)
    assert CREDIT == ParameterKind("credit", Credit)


@pytest.mark.parametrize("name", ["", "Brackets", "flat-rate", "2x", "_x"])
def test_rejects_names_that_are_not_snake_case(name: str) -> None:
    with pytest.raises(ValueError, match="parameter kind name"):
        ParameterKind(name, Decimal)


def test_value_type_must_be_a_type() -> None:
    with pytest.raises(TypeError, match="value_type must be a type"):
        ParameterKind("x", "Decimal")  # type: ignore[arg-type]


def test_kind_is_invariant_in_its_value_type() -> None:
    # Covariance would let mypy widen T and accept a parser whose values do not match its kind.
    (value_type,) = vars(ParameterKind)["__parameters__"]
    assert not (
        value_type.__covariant__
        or value_type.__contravariant__
        or getattr(value_type, "__infer_variance__", False)
    )
