"""Unit tests for Artifact: a named intermediate value in a computation (design.md §2)."""

from __future__ import annotations

import pytest

from app.domain.artifact import Artifact


@pytest.mark.parametrize("name", ["taxable_base", "x", "tax_after_credit_2"])
def test_accepts_snake_case_names(name: str) -> None:
    artifact = Artifact(name)

    assert artifact.name == name
    assert str(artifact) == name


@pytest.mark.parametrize("name", ["", "Taxable", "2x", "taxable-base", "taxable base", "_x", "x_"])
def test_rejects_names_that_are_not_snake_case(name: str) -> None:
    with pytest.raises(ValueError, match="artifact name"):
        Artifact(name)


def test_rejects_non_string_name() -> None:
    with pytest.raises(TypeError, match="must be a str"):
        Artifact(1)  # type: ignore[arg-type]


def test_artifacts_are_equal_by_name_and_hashable() -> None:
    assert Artifact("a") == Artifact("a")
    assert Artifact("a") != Artifact("b")
    assert len({Artifact("a"), Artifact("a")}) == 1
