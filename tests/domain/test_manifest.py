"""Unit tests for CapabilitySelection: one capability chosen by a manifest, with its slots filled.

`params` maps parameter slots to families; `consumes` and `produces` map artifact slots to artifact
identifiers. All are kept as strings (the registries resolve them later) in read-only mappings.
Names are made up.
"""

from __future__ import annotations

import dataclasses
from types import MappingProxyType
from typing import Any, cast

import pytest

from app.domain.manifest import CapabilitySelection


def selection() -> CapabilitySelection:
    return CapabilitySelection(
        name="ex/progressive_tax",
        params={"schedule": "ex/brackets"},
        consumes={"base": "ex/taxable_base"},
        produces={"output": "ex/levy"},
    )


def test_holds_its_name_and_slot_bindings() -> None:
    chosen = selection()

    assert chosen.name == "ex/progressive_tax"
    assert chosen.params == {"schedule": "ex/brackets"}
    assert chosen.consumes == {"base": "ex/taxable_base"}
    assert chosen.produces == {"output": "ex/levy"}


def test_has_no_params_family() -> None:
    assert [field.name for field in dataclasses.fields(CapabilitySelection)] == [
        "name",
        "params",
        "consumes",
        "produces",
    ]


def test_slot_bindings_are_read_only() -> None:
    chosen = selection()

    for bindings in (chosen.params, chosen.consumes, chosen.produces):
        assert isinstance(bindings, MappingProxyType)
        with pytest.raises(TypeError):
            cast(Any, bindings)["extra"] = "ex/other"


def test_slot_bindings_are_copied_from_what_it_was_given() -> None:
    params = {"schedule": "ex/brackets"}
    chosen = CapabilitySelection(
        name="ex/progressive_tax", params=params, consumes={}, produces={"output": "ex/levy"}
    )

    params["schedule"] = "ex/other"

    assert chosen.params == {"schedule": "ex/brackets"}


def test_is_frozen() -> None:
    with pytest.raises(dataclasses.FrozenInstanceError):
        cast(Any, selection()).name = "ex/other"


def test_selections_with_the_same_bindings_are_equal() -> None:
    assert selection() == selection()
    assert selection() != dataclasses.replace(selection(), produces={"output": "ex/other"})


def test_a_selection_may_bind_no_parameters_and_consume_nothing() -> None:
    chosen = CapabilitySelection(
        name="ex/flat_grant", params={}, consumes={}, produces={"output": "ex/grant"}
    )

    assert chosen.params == {}
    assert chosen.consumes == {}


def test_equal_selections_hash_alike() -> None:
    assert hash(selection()) == hash(selection())
    assert len({selection(), selection()}) == 1
