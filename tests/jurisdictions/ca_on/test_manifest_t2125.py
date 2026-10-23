"""Form T2125 in the CA-ON manifest: any number of statements, and what the return reads.

T2125 is the form `ca/t2125`, one instance for each statement (one for each business). Its
selections live in the part `03b_t2125.yaml` under the `form:` key; the caller supplies the
statements as the record list `ca/t2125_statements`, whose fields are the T2125 inputs; and the form
exports its line 9946, "Your net income (loss)", which T1 line 13500 "Net" totals over the
statements. The entries of the form are listed in `manifest_families/t2125.py`. The five printed
constants of Charts B and C are the form's own copies; the return selects none of them.
"""

from __future__ import annotations

from itertools import chain
from pathlib import Path

import yaml

import app.jurisdictions.ca_on
import app.registrations  # lists the packages; build_tax_computation registers their catalogs
from app.adapters.outbound.yaml_jurisdictions import YamlJurisdictionSource
from app.domain.artifact import ArtifactRegistry
from app.domain.form import FormComposition
from app.domain.jurisdiction_code import JurisdictionCode
from app.domain.manifest import Form, Manifest
from app.domain.record_list import RecordListKind
from app.jurisdictions.ca.catalog import BUSINESS_INCOME, T2125_STATEMENTS
from app.main import build_tax_computation
from tests.jurisdictions.ca_on.manifest_families import t2125

CA_ON = JurisdictionCode("CA-ON")
PART = Path(app.jurisdictions.ca_on.__file__).parent / "manifests" / "v1" / "03b_t2125.yaml"
INCOME_PART = PART.with_name("03_income.yaml")
INPUTS_PART = PART.with_name("01_inputs.yaml")
VEHICLE_CONSTANTS = frozenset(
    {
        "ca/business_vehicle_interest_limit",
        "ca/business_vehicle_days_divisor",
        "ca/business_vehicle_list_price_limit",
        "ca/business_vehicle_lease_charge_limit",
        "ca/business_vehicle_lease_cost_limit",
    }
)


def manifest() -> Manifest:
    (only,) = (
        YamlJurisdictionSource(app.registrations.JURISDICTIONS.roots())
        .get_jurisdiction(CA_ON)
        .manifests
    )
    return only


def form() -> Form:
    (found,) = (each for each in manifest().forms if each.name == "ca/t2125")
    return found


def composed() -> FormComposition:
    return build_tax_computation().compose(CA_ON, 2025).form("ca/t2125")


# --- the part and the form -----------------------------------------------------------------------


def test_the_t2125_part_declares_the_form_ca_t2125_with_its_instances_and_exports() -> None:
    declared = yaml.safe_load(PART.read_text())["form"]

    assert declared == {
        "name": "ca/t2125",
        "instances": "ca/t2125_statements",
        "exports": list(t2125.FORM_EXPORTS),
    }


def test_the_manifest_has_the_form_t2125_beside_the_other_forms() -> None:
    found = form()

    assert found.name == "ca/t2125"
    assert found.instances == "ca/t2125_statements"
    assert found.exports == t2125.FORM_EXPORTS


def test_the_form_holds_the_55_t2125_selections_unchanged() -> None:
    found = form()

    assert len(found.capabilities) == 55
    assert set(found.capabilities) == t2125.FORM_STEPS


def test_the_return_selects_only_the_total_of_line_9946_and_none_of_the_form_steps() -> None:
    (default, *_) = manifest().forms
    selected = set(default.capabilities)

    assert t2125.STEPS <= selected
    # What the form holds, the return holds not at all: the five printed constants of Charts B and C
    # are the form's own copies, and no part of the return selects them.
    assert not selected & t2125.FORM_STEPS
    produced = set(chain.from_iterable(step.produces.values() for step in selected))
    assert not produced & VEHICLE_CONSTANTS


def test_the_form_has_its_own_copy_of_the_five_constants() -> None:
    own = [step for step in form().capabilities if step.produces["output"] in VEHICLE_CONSTANTS]

    assert [step.name for step in own] == ["core/credit_amount"] * 5
    assert {step.produces["output"] for step in own} == VEHICLE_CONSTANTS
    assert not PART.with_name("03f_t2125_vehicle_limits.yaml").exists()


def test_the_t2125_part_is_not_over_30_kb_and_the_other_parts_hold_no_t2125_input() -> None:
    assert PART.stat().st_size <= 30 * 1024
    for other in (INCOME_PART, INPUTS_PART):
        text = other.read_text()
        for identifier in t2125.FORM_INPUTS:
            assert f"- {identifier}\n" not in text, (other.name, identifier)


# --- the instances input -------------------------------------------------------------------------


def test_the_instances_are_the_one_input_of_the_manifest_in_place_of_the_t2125_inputs() -> None:
    inputs = manifest().inputs

    assert t2125.INPUTS <= inputs
    assert inputs.isdisjoint(t2125.FORM_INPUTS)


def test_the_statements_kind_is_a_record_list_of_every_t2125_input_in_order() -> None:
    assert isinstance(T2125_STATEMENTS, RecordListKind)
    assert T2125_STATEMENTS.identifier == "ca/t2125_statements"
    assert frozenset(field.identifier for field in T2125_STATEMENTS.fields) == t2125.FORM_INPUTS
    assert len(T2125_STATEMENTS.fields) == len(t2125.FORM_INPUTS) == 70


def test_the_area_a_list_of_a_statement_is_a_nested_record_list() -> None:
    nested = {
        field.identifier for field in T2125_STATEMENTS.fields if isinstance(field, RecordListKind)
    }

    assert nested == {"ca/business_cca_classes"}


def test_the_catalog_registers_the_statements_kind_beside_the_other_record_lists() -> None:
    build_tax_computation()

    assert ArtifactRegistry.shared().kind("ca/t2125_statements") is T2125_STATEMENTS


# --- the outputs and the node --------------------------------------------------------------------


def test_the_return_declares_no_output_for_the_exports_nothing_reads() -> None:
    (default, *_) = manifest().forms
    exports = set(default.exports)

    assert t2125.OUTPUTS <= exports
    assert not {"ca/business_closing_ucc", "ca/business_home_carry_forward"} & exports
    assert not {export for export in exports if "." in export}


def test_the_form_set_runs_the_form_on_the_statements_and_derives_its_three_kinds() -> None:
    found = composed()

    assert found.instances == T2125_STATEMENTS
    assert found.imports == frozenset()
    assert found.derived == (
        t2125.NET_INCOME_PER_STATEMENT,
        t2125.BUSINESS_CLOSING_UCC_PER_STATEMENT,
        t2125.BUSINESS_HOME_CARRY_FORWARD_PER_STATEMENT,
    )


def test_the_net_income_export_is_a_record_list_of_the_signed_business_income() -> None:
    (net,) = (kind for kind in composed().derived if kind.identifier == "ca/t2125.business_income")

    assert net == t2125.NET_INCOME_PER_STATEMENT
    assert net.fields == (BUSINESS_INCOME,)


def test_the_selections_inside_the_form_are_wired_as_they_were_on_the_return() -> None:
    inner = {
        (type(capability), capability.consumes, capability.produces)
        for capability in composed().composition.order
    }

    assert inner == t2125.FORM_WIRING
