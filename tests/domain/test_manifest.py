"""Unit tests for CapabilitySelection and Manifest.

A selection is one capability chosen by a manifest, with its slots filled: `params` maps parameter
slots to families; `consumes` and `produces` map artifact slots to artifact identifiers. All are
kept as strings (the registries resolve them later) in read-only mappings. A manifest declares the
computation's `inputs` and `outputs` as frozensets of artifact identifiers: each non-empty. An
identifier in both is carried onto the return as entered. Names are made up.
"""

from __future__ import annotations

import dataclasses
from types import MappingProxyType
from typing import Any, cast

import pytest

from app.domain.errors import InvalidManifestError
from app.domain.jurisdiction_code import JurisdictionCode
from app.domain.manifest import CapabilitySelection, Form, Manifest


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
        "forms",
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


def test_manifest_accepts_an_identifier_that_is_both_input_and_output() -> None:
    found = manifest(
        inputs=frozenset({"ex/taxable_base", "ex/levy"}),
        outputs=frozenset({"ex/levy"}),
    )

    assert found.inputs == frozenset({"ex/taxable_base", "ex/levy"})
    assert found.outputs == frozenset({"ex/levy"})


def test_manifest_accepts_inputs_and_outputs_that_are_all_the_same() -> None:
    found = manifest(inputs=frozenset({"ex/levy"}), outputs=frozenset({"ex/levy"}))

    assert found.inputs == found.outputs == frozenset({"ex/levy"})


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


# --- forms: a named group of selections with its instances kind and its exports ---------------
#
# A `Form` is manifest data beside `CapabilitySelection`, not a capability: its `name`, the
# `instances` identifier of the record-list kind the caller supplies (one record per instance),
# the `exports` it produces as `<form>.<export>` artifacts, and its `capabilities`. All of them
# are plain identifiers `<namespace>/<snake_case>`: the dotted `<form>.<export>` is built by the
# engine, never written in a manifest.


def form(
    name: str = "ex/rental",
    instances: str = "ex/rentals",
    exports: Any = ("ex/net_income", "ex/unit_list"),
    capabilities: Any = None,
) -> Form:
    return Form(
        name=name,
        instances=instances,
        exports=exports,
        capabilities=(selection(),) if capabilities is None else capabilities,
    )


def test_a_form_holds_its_name_instances_exports_and_selections() -> None:
    found = form()

    assert found.name == "ex/rental"
    assert found.instances == "ex/rentals"
    assert found.exports == ("ex/net_income", "ex/unit_list")
    assert found.capabilities == (selection(),)


def test_form_fields_in_order() -> None:
    assert [field.name for field in dataclasses.fields(Form)] == [
        "name",
        "instances",
        "exports",
        "capabilities",
    ]


def test_a_form_is_not_a_capability_selection() -> None:
    assert not issubclass(Form, CapabilitySelection)


def test_exports_and_capabilities_are_kept_as_tuples_copied_from_what_was_given() -> None:
    exports = ["ex/net_income"]
    chosen = [selection()]
    found = form(exports=exports, capabilities=chosen)

    exports.append("ex/other")
    chosen.clear()

    assert found.exports == ("ex/net_income",)
    assert found.capabilities == (selection(),)
    assert isinstance(found.exports, tuple)
    assert isinstance(found.capabilities, tuple)


def test_a_form_is_frozen() -> None:
    with pytest.raises(dataclasses.FrozenInstanceError):
        cast(Any, form()).name = "ex/other"


def test_equal_forms_are_equal_and_hash_alike() -> None:
    assert form() == form()
    assert hash(form()) == hash(form())
    assert len({form(), form()}) == 1
    assert form() != form(exports=("ex/net_income",))
    assert form() != form(instances="ex/other")


@pytest.mark.parametrize("field", ["name", "instances"])
@pytest.mark.parametrize(
    "bad", ["", "rental", "ex/Rental", "ex/rental.net_income", "ex/a/b", "ex/", "/rental"]
)
def test_a_form_name_and_instances_are_plain_namespaced_identifiers(field: str, bad: str) -> None:
    with pytest.raises(InvalidManifestError, match=field):
        form(**{field: bad})


@pytest.mark.parametrize(
    "bad", ["", "net_income", "ex/NetIncome", "ex/rental.net_income", "ex/a/b"]
)
def test_an_export_is_a_plain_namespaced_identifier(bad: str) -> None:
    with pytest.raises(InvalidManifestError, match="exports"):
        form(exports=("ex/net_income", bad))


def test_a_form_must_export_something() -> None:
    with pytest.raises(InvalidManifestError, match="exports must name at least one artifact"):
        form(exports=())


@pytest.mark.parametrize(
    "exports", [("ex/net_income", "ex/net_income"), ("ex/net_income", "ca/net_income")]
)
def test_two_exports_with_the_same_local_id_are_refused(exports: tuple[str, ...]) -> None:
    # Both would be produced as `ex/rental.net_income`.
    with pytest.raises(InvalidManifestError, match=r"net_income.*more than once"):
        form(exports=exports)


def test_a_manifest_has_no_forms_by_default() -> None:
    assert manifest().forms == ()


def test_manifest_fields_end_with_forms() -> None:
    assert [field.name for field in dataclasses.fields(Manifest)][-1] == "forms"


def test_a_manifest_holds_its_forms_as_a_tuple_in_order() -> None:
    other = form(name="ex/business", instances="ex/businesses", exports=("ex/profit",))
    found = dataclasses.replace(manifest(), forms=cast(Any, [form(), other]))

    assert found.forms == (form(), other)
    assert isinstance(found.forms, tuple)


def test_manifests_with_other_forms_differ_and_equal_ones_hash_alike() -> None:
    with_form = dataclasses.replace(manifest(), forms=(form(),))

    assert with_form != manifest()
    assert with_form == dataclasses.replace(manifest(), forms=(form(),))
    assert hash(with_form) == hash(dataclasses.replace(manifest(), forms=(form(),)))


def test_a_manifest_refuses_two_forms_of_one_name() -> None:
    again = form(instances="ex/others", exports=("ex/profit",))

    with pytest.raises(InvalidManifestError, match="ex/rental.*more than once"):
        dataclasses.replace(manifest(), forms=(form(), again))


# --- the return form: the form of every selection of `capabilities` -----------------------------
#
# `Manifest.capabilities`, `inputs` and `outputs` are the selections and the starting and ending
# artifacts of the RETURN form, named `<jurisdiction namespace>/return`; `forms` holds only the
# other forms. A form of the return's name would be a second return, so it is refused.


def test_the_return_form_is_named_return_in_the_namespace_of_the_jurisdiction() -> None:
    assert manifest().return_form_name == "ex-on/return"


def test_a_manifest_refuses_a_form_named_like_its_return_form() -> None:
    clash = form(name="ex-on/return", instances="ex/rentals", exports=("ex/profit",))

    with pytest.raises(InvalidManifestError, match="ex-on/return.*return form"):
        dataclasses.replace(manifest(), forms=(clash,))


def test_a_form_named_return_in_another_namespace_is_allowed() -> None:
    other = form(name="ex/return", instances="ex/rentals", exports=("ex/profit",))

    assert dataclasses.replace(manifest(), forms=(other,)).forms == (other,)
