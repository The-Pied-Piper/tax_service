"""Form T2121 in the CA-ON manifest: any number of statements, and what the return reads.

T2121 is the form `ca/t2121`, one instance for each statement (one for each fishing business). Its
selections live in the part `03d_t2121.yaml` under the `form:` key; the caller supplies the
statements as the record list `ca/t2121_statements`, whose fields are the T2121 inputs; and the form
exports its line 9946, "Your net income (loss)", which T1 line 14300 "Net" totals over the
statements. The entries of the form are listed in `manifest_families/t2121.py`. The printed
constants of Charts B and C are the datasets of the form's one motor vehicle step; the return
selects none of them.
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
from app.jurisdictions.ca.catalog import FISHING_INCOME, T2121_STATEMENTS
from app.main import build_tax_computation
from tests.jurisdictions.ca_on.manifest_families import t2121

CA_ON = JurisdictionCode("CA-ON")
PART = Path(app.jurisdictions.ca_on.__file__).parent / "manifests" / "v1" / "03d_t2121.yaml"
INCOME_PART = PART.with_name("03_income.yaml")
INPUTS_PART = PART.with_name("01_inputs.yaml")
VEHICLE_CONSTANTS = frozenset(
    {
        "ca/business_vehicle_days_divisor",
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
    (found,) = (each for each in manifest().forms if each.name == "ca/t2121")
    return found


def composed() -> FormComposition:
    return build_tax_computation().compose(CA_ON, 2025).form("ca/t2121")


# --- the part and the form -----------------------------------------------------------------------


def test_the_t2121_part_declares_the_form_ca_t2121_with_its_instances_and_exports() -> None:
    declared = yaml.safe_load(PART.read_text())["form"]

    assert declared == {
        "name": "ca/t2121",
        "instances": "ca/t2121_statements",
        "exports": list(t2121.FORM_EXPORTS),
    }


def test_the_manifest_has_the_form_t2121_beside_the_other_forms() -> None:
    found = form()

    assert found.name == "ca/t2121"
    assert found.instances == "ca/t2121_statements"
    assert found.exports == t2121.FORM_EXPORTS


def test_the_form_holds_the_46_t2121_selections() -> None:
    # The selections of Charts A to C of one vehicle and the five printed constants are now one
    # step over the statement's vehicles, the form's only selection for them.
    found = form()

    assert len(found.capabilities) == 46
    assert set(found.capabilities) == t2121.FORM_STEPS


def test_the_return_selects_only_the_total_of_line_9946_and_none_of_the_form_steps() -> None:
    (default, *_) = manifest().forms
    selected = set(default.capabilities)

    assert t2121.STEPS <= selected
    # What the form holds, the return holds not at all: the printed constants of Charts B and C
    # are datasets of the form's vehicle step, and no part of the return selects them.
    assert not selected & t2121.FORM_STEPS
    produced = set(chain.from_iterable(step.produces.values() for step in selected))
    assert not produced & VEHICLE_CONSTANTS


def test_the_form_selects_one_vehicles_step_over_the_printed_constants_datasets() -> None:
    (own,) = [step for step in form().capabilities if step.name == "ca/business_vehicle_expenses"]

    assert own.params == {
        "interest_limits": "ca/business_vehicle_interest_limits",
        "lease_limits": "ca/business_vehicle_lease_limits",
        "days_divisor": "ca/business_vehicle_days_divisor",
        "lease_price_rate": "ca/business_vehicle_lease_price_rate",
        "rounding": "ca/business_vehicle_rounding",
    }
    assert own.consumes == {
        "vehicles": "ca/business_vehicles",
        "sales_tax_rate": "ca/fish_vehicle_sales_tax_rate",
    }
    assert own.produces == {"output": "ca/fish_motor_vehicle_expenses"}


def test_the_form_has_no_step_of_its_own_for_the_chart_lines_or_the_constants() -> None:
    produced = {step.produces["output"] for step in form().capabilities}

    assert not produced & VEHICLE_CONSTANTS
    assert not any(identifier.startswith("ca/fish_vehicle_") for identifier in produced)


def test_the_t2121_part_is_not_over_30_kb_and_the_other_parts_hold_no_t2121_input() -> None:
    assert PART.stat().st_size <= 30 * 1024
    for other in (INCOME_PART, INPUTS_PART):
        text = other.read_text()
        for identifier in t2121.FORM_INPUTS:
            assert f"- {identifier}\n" not in text, (other.name, identifier)


# --- the instances input -------------------------------------------------------------------------


def test_the_instances_are_the_one_input_of_the_manifest_in_place_of_the_t2121_inputs() -> None:
    inputs = manifest().inputs

    assert t2121.INPUTS <= inputs
    assert inputs.isdisjoint(t2121.FORM_INPUTS)


def test_the_statements_kind_is_a_record_list_of_every_t2121_input_in_order() -> None:
    assert isinstance(T2121_STATEMENTS, RecordListKind)
    assert T2121_STATEMENTS.identifier == "ca/t2121_statements"
    assert frozenset(field.identifier for field in T2121_STATEMENTS.fields) == t2121.FORM_INPUTS
    assert len(T2121_STATEMENTS.fields) == len(t2121.FORM_INPUTS) == 53


def test_the_area_a_list_and_the_vehicles_of_a_statement_are_nested_record_lists() -> None:
    nested = {
        field.identifier for field in T2121_STATEMENTS.fields if isinstance(field, RecordListKind)
    }

    assert nested == {"ca/business_vehicles", "ca/fish_cca_classes"}


def test_the_catalog_registers_the_statements_kind_beside_the_other_record_lists() -> None:
    build_tax_computation()

    assert ArtifactRegistry.shared().kind("ca/t2121_statements") is T2121_STATEMENTS


# --- the outputs and the node --------------------------------------------------------------------


def test_the_return_declares_no_output_for_the_exports_nothing_reads() -> None:
    (default, *_) = manifest().forms
    exports = set(default.exports)

    assert t2121.OUTPUTS <= exports
    assert (
        not {
            "ca/fish_closing_ucc",
            "ca/fish_home_carry_forward",
            "ca/fish_immediate_expensing_claim",
            "ca/fish_immediate_expensing_limit_unprorated",
        }
        & exports
    )
    assert not {export for export in exports if "." in export}


def test_the_form_set_runs_the_form_on_the_statements_and_derives_its_five_kinds() -> None:
    found = composed()

    assert found.instances == T2121_STATEMENTS
    assert found.imports == frozenset()
    assert found.derived == (
        t2121.NET_INCOME_PER_STATEMENT,
        t2121.FISH_CLOSING_UCC_PER_STATEMENT,
        t2121.FISH_HOME_CARRY_FORWARD_PER_STATEMENT,
        t2121.FISH_IMMEDIATE_EXPENSING_CLAIM_PER_STATEMENT,
        t2121.FISH_IMMEDIATE_EXPENSING_LIMIT_UNPRORATED_PER_STATEMENT,
    )


def test_the_net_income_export_is_a_record_list_of_the_signed_fishing_income() -> None:
    (net,) = (kind for kind in composed().derived if kind.identifier == "ca/t2121.fishing_income")

    assert net == t2121.NET_INCOME_PER_STATEMENT
    assert net.fields == (FISHING_INCOME,)


def test_the_selections_inside_the_form_are_wired_as_they_were_on_the_return() -> None:
    inner = {
        (type(capability), capability.consumes, capability.produces)
        for capability in composed().composition.order
    }

    assert inner == t2121.FORM_WIRING
