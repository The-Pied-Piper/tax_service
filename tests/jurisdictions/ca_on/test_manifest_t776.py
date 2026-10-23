"""Form T776 in the CA-ON manifest: a form with any number of statements, and what the return reads.

T776 is the form `ca/t776`, one instance for each statement (one for each rental operation). Its
selections live in the part `03e_t776.yaml` under the `form:` key; the caller supplies the
statements as the record list `ca/t776_statements`, whose fields are the T776 inputs; and the form
exports its line 9946, "Your net income (loss)", which T1 line 12600 "Net" totals over the
statements. The entries of the form are listed in `manifest_families/t776.py`.
"""

from __future__ import annotations

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
from app.jurisdictions.ca.catalog import NET_RENTAL_INCOME, T776_STATEMENTS
from app.main import build_tax_computation
from tests.jurisdictions.ca_on.manifest_families import t776

CA_ON = JurisdictionCode("CA-ON")
PART = Path(app.jurisdictions.ca_on.__file__).parent / "manifests" / "v1" / "03e_t776.yaml"
INCOME_PART = PART.with_name("03_income.yaml")
INPUTS_PART = PART.with_name("01_inputs.yaml")


def manifest() -> Manifest:
    (only,) = (
        YamlJurisdictionSource(app.registrations.JURISDICTIONS.roots())
        .get_jurisdiction(CA_ON)
        .manifests
    )
    return only


def form() -> Form:
    (found,) = (found for found in manifest().forms if found.name == "ca/t776")
    return found


def composed() -> FormComposition:
    found = build_tax_computation().compose(CA_ON, 2025).form("ca/t776")
    return found


# --- the part and the form -----------------------------------------------------------------------


def test_the_t776_part_declares_the_form_ca_t776_with_its_instances_and_exports() -> None:
    declared = yaml.safe_load(PART.read_text())["form"]

    assert declared == {
        "name": "ca/t776",
        "instances": "ca/t776_statements",
        "exports": list(t776.FORM_EXPORTS),
    }


def test_the_manifest_has_the_form_t776_beside_the_other_forms() -> None:
    found = form()

    assert found.name == "ca/t776"
    assert found.instances == "ca/t776_statements"
    assert found.exports == t776.FORM_EXPORTS


def test_the_form_holds_the_31_t776_selections_unchanged() -> None:
    found = form()

    assert len(found.capabilities) == 31
    assert set(found.capabilities) == t776.FORM_STEPS


def test_the_return_selects_no_t776_step_of_its_own_but_the_total_of_line_9946() -> None:
    (default, *_) = manifest().forms
    selected = set(default.capabilities)

    assert t776.STEPS <= selected
    assert selected.isdisjoint(t776.FORM_STEPS)


def test_the_t776_part_is_not_over_30_kb_and_the_other_parts_hold_no_t776_step() -> None:
    assert PART.stat().st_size <= 30 * 1024
    for other in (INCOME_PART, INPUTS_PART):
        text = other.read_text()
        assert "ca/rental_" not in text, other.name
        assert "ca/short_term_rental" not in text, other.name


# --- the instances input -------------------------------------------------------------------------


def test_the_instances_are_the_one_input_of_the_manifest_in_place_of_the_t776_inputs() -> None:
    inputs = manifest().inputs

    assert t776.INPUTS <= inputs
    assert inputs.isdisjoint(t776.FORM_INPUTS)


def test_the_statements_kind_is_a_record_list_of_every_t776_input_in_order() -> None:
    assert isinstance(T776_STATEMENTS, RecordListKind)
    assert T776_STATEMENTS.identifier == "ca/t776_statements"
    assert frozenset(field.identifier for field in T776_STATEMENTS.fields) == t776.FORM_INPUTS
    assert len(T776_STATEMENTS.fields) == len(t776.FORM_INPUTS) == 56


def test_the_lists_of_a_statement_are_nested_record_lists() -> None:
    nested = {
        field.identifier for field in T776_STATEMENTS.fields if isinstance(field, RecordListKind)
    }

    assert nested == {
        "ca/rental_properties",
        "ca/short_term_rental_units",
        "ca/short_term_rental_cca_units",
        "ca/rental_cca_classes",
    }


def test_the_catalog_registers_the_statements_kind_beside_the_other_record_lists() -> None:
    build_tax_computation()

    assert ArtifactRegistry.shared().kind("ca/t776_statements") is T776_STATEMENTS


# --- the outputs and the node --------------------------------------------------------------------


def test_the_return_declares_no_output_for_the_exports_nothing_reads() -> None:
    (default, *_) = manifest().forms
    exports = set(default.exports)

    assert t776.OUTPUTS <= exports
    assert (
        not {
            "ca/short_term_rental_gross_rents",
            "ca/rental_short_term_portion",
            "ca/rental_closing_ucc",
            "ca/rental_non_compliant_cca",
            "ca/short_term_rental_non_compliant_cca_by_class",
        }
        & exports
    )
    assert not {export for export in exports if "." in export}


def test_the_form_set_runs_the_form_on_the_statements_and_derives_its_six_kinds() -> None:
    found = composed()

    assert found.instances == T776_STATEMENTS
    assert found.imports == frozenset()
    assert found.derived == (
        t776.NET_RENTAL_INCOME_PER_STATEMENT,
        t776.SHORT_TERM_RENTAL_GROSS_RENTS_PER_STATEMENT,
        t776.RENTAL_SHORT_TERM_PORTION_PER_STATEMENT,
        t776.RENTAL_CLOSING_UCC_PER_STATEMENT,
        t776.RENTAL_NON_COMPLIANT_CCA_PER_STATEMENT,
        t776.SHORT_TERM_RENTAL_NON_COMPLIANT_CCA_BY_CLASS_PER_STATEMENT,
    )


def test_the_net_income_export_is_a_record_list_of_the_signed_net_rental_income() -> None:
    (net,) = (kind for kind in composed().derived if kind.identifier == "ca/t776.net_rental_income")

    assert net == t776.NET_RENTAL_INCOME_PER_STATEMENT
    assert net.fields == (NET_RENTAL_INCOME,)


def test_the_selections_inside_the_form_are_wired_as_they_were_on_the_return() -> None:
    inner = {
        (type(capability), capability.consumes, capability.produces)
        for capability in composed().composition.order
    }

    assert inner == t776.FORM_WIRING
