"""Unit tests for CapabilitySelection and Manifest.

A selection is one capability chosen by a manifest, with its slots filled: `params` maps parameter
slots to families; `consumes` and `produces` map artifact slots to artifact identifiers. All are
kept as strings (the registries resolve them later) in read-only mappings. A manifest declares the
computation's `inputs` and `outputs` as frozensets of artifact identifiers: each non-empty, and
no identifier in both. Names are made up.
"""

from __future__ import annotations

import dataclasses
from types import MappingProxyType
from typing import Any, cast

import pytest

from app.domain.errors import InvalidManifestError
from app.domain.jurisdiction_code import JurisdictionCode
from app.domain.manifest import CapabilitySelection, Manifest


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


def manifest(
    inputs: frozenset[str] = frozenset({"ex/taxable_base"}),
    outputs: frozenset[str] = frozenset({"ex/levy"}),
) -> Manifest:
    return Manifest(
        jurisdiction=JurisdictionCode("EX-ON"),
        version=1,
        valid_from_tax_year=2025,
        capabilities=(selection(),),
        inputs=inputs,
        outputs=outputs,
    )


def test_manifest_holds_its_inputs_and_outputs() -> None:
    found = manifest(
        inputs=frozenset({"ex/taxable_base", "ex/gross_income"}),
        outputs=frozenset({"ex/levy"}),
    )

    assert found.inputs == frozenset({"ex/taxable_base", "ex/gross_income"})
    assert found.outputs == frozenset({"ex/levy"})


def test_manifest_fields_in_order() -> None:
    assert [field.name for field in dataclasses.fields(Manifest)] == [
        "jurisdiction",
        "version",
        "valid_from_tax_year",
        "capabilities",
        "inputs",
        "outputs",
    ]


def test_equal_manifests_are_equal_and_hash_alike() -> None:
    assert manifest() == manifest()
    assert hash(manifest()) == hash(manifest())
    assert manifest() != manifest(outputs=frozenset({"ex/other"}))


@pytest.mark.parametrize("field", ["inputs", "outputs"])
def test_manifest_rejects_empty_inputs_or_outputs(field: str) -> None:
    empty: dict[str, frozenset[str]] = {field: frozenset()}

    with pytest.raises(InvalidManifestError, match=f"{field} must name at least one artifact"):
        manifest(**empty)


def test_manifest_rejects_an_identifier_that_is_both_input_and_output() -> None:
    with pytest.raises(InvalidManifestError, match="'ex/levy' is both an input and an output"):
        manifest(
            inputs=frozenset({"ex/taxable_base", "ex/levy"}),
            outputs=frozenset({"ex/levy"}),
        )


# --- list slots: a consumed slot filled with a list of identifiers ------------------------------


def listing(parts: Any) -> CapabilitySelection:
    return CapabilitySelection(
        name="ex/total_up",
        params={},
        consumes={"base": "ex/taxable_base", "parts": parts},
        produces={"total": "ex/total"},
    )


def test_a_consumed_slot_may_hold_a_list_of_identifiers_kept_as_a_tuple() -> None:
    chosen = listing(["ex/a", "ex/b", "ex/c"])

    assert chosen.consumes == {"base": "ex/taxable_base", "parts": ("ex/a", "ex/b", "ex/c")}
    assert isinstance(chosen.consumes["parts"], tuple)
    assert isinstance(chosen.consumes["base"], str)


def test_a_list_of_identifiers_keeps_its_order() -> None:
    assert listing(["ex/c", "ex/a", "ex/b"]).consumes["parts"] == ("ex/c", "ex/a", "ex/b")


def test_a_list_of_identifiers_may_be_empty() -> None:
    assert listing([]).consumes["parts"] == ()


def test_a_list_of_identifiers_is_copied_from_what_it_was_given() -> None:
    parts = ["ex/a", "ex/b"]
    chosen = listing(parts)

    parts.append("ex/c")

    assert chosen.consumes["parts"] == ("ex/a", "ex/b")


def test_selections_with_list_slots_compare_and_hash_by_value() -> None:
    assert listing(["ex/a", "ex/b"]) == listing(("ex/a", "ex/b"))
    assert listing(["ex/a", "ex/b"]) != listing(["ex/b", "ex/a"])
    assert hash(listing(["ex/a", "ex/b"])) == hash(listing(("ex/a", "ex/b")))
    assert len({listing(["ex/a", "ex/b"]), listing(("ex/a", "ex/b"))}) == 1
