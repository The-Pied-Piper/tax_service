"""Form T1-M in the CA-ON manifest: any number of moves, and what the return reads.

T1-M is the form `ca/t1_m`, one instance for each move (each eligible move gets its own form). Its
selections live in the part `05k_t1_m.yaml` under the `form:` key; the caller supplies the moves as
the record list `ca/t1_m_moves`, whose fields are the caller's inputs of one move; and the form
exports its line 29, "Enter this amount on line 21900 of your return", which T1 line 21900 totals
over the moves, and its line 30, which nothing on the return reads. The entries of the form are
listed in `manifest_families/t1_m.py`.
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
from app.jurisdictions.ca.catalog import (
    MOVING_EXPENSES_CLAIM,
    MOVING_EXPENSES_DEDUCTION,
    T1_M_MOVES,
)
from app.main import build_tax_computation
from tests.jurisdictions.ca_on.manifest_families import t1_m

CA_ON = JurisdictionCode("CA-ON")
PART = Path(app.jurisdictions.ca_on.__file__).parent / "manifests" / "v1" / "05k_t1_m.yaml"
INCOME_PART = PART.with_name("01_inputs.yaml")
DEDUCTIONS_PART = PART.with_name("05_deductions.yaml")
AMT_PART = PART.with_name("20_alternative_minimum_tax.yaml")


def manifest() -> Manifest:
    (only,) = (
        YamlJurisdictionSource(app.registrations.JURISDICTIONS.roots())
        .get_jurisdiction(CA_ON)
        .manifests
    )
    return only


def form() -> Form:
    (found,) = (each for each in manifest().forms if each.name == "ca/t1_m")
    return found


def composed() -> FormComposition:
    return build_tax_computation().compose(CA_ON, 2025).form("ca/t1_m")


# --- the part and the form -----------------------------------------------------------------------


def test_the_t1_m_part_declares_the_form_ca_t1_m_with_its_instances_and_exports() -> None:
    declared = yaml.safe_load(PART.read_text())["form"]

    assert declared == {
        "name": "ca/t1_m",
        "instances": "ca/t1_m_moves",
        "exports": list(t1_m.FORM_EXPORTS),
    }


def test_the_manifest_has_the_form_t1_m_beside_the_other_forms() -> None:
    found = form()

    assert found.name == "ca/t1_m"
    assert found.instances == "ca/t1_m_moves"
    assert found.exports == t1_m.FORM_EXPORTS


def test_the_form_holds_the_14_t1_m_selections() -> None:
    found = form()

    assert len(found.capabilities) == 14
    assert set(found.capabilities) == t1_m.FORM_STEPS


def test_the_return_selects_only_the_total_of_line_21900_and_none_of_the_form_steps() -> None:
    (default, *_) = manifest().forms
    selected = set(default.capabilities)

    assert t1_m.STEPS <= selected
    assert not selected & t1_m.FORM_STEPS
    produced = set(chain.from_iterable(step.produces.values() for step in selected))
    assert "ca/moving_expenses_deduction" in produced


def test_the_form_selects_the_40_kilometre_test_and_the_5000_maximum_from_their_datasets() -> None:
    by_name = {step.name: step for step in form().capabilities}

    assert by_name["ca/threshold_gate"].params == {"threshold": "ca/moving_distance_threshold"}
    assert by_name["core/capped_amount"].params == {"cap": "ca/moving_old_home_maintenance_cap"}


def test_the_t1_m_part_is_not_over_30_kb_and_the_other_parts_hold_no_t1_m_input() -> None:
    assert PART.stat().st_size <= 30 * 1024
    for other in (INCOME_PART, DEDUCTIONS_PART, AMT_PART):
        text = other.read_text()
        for identifier in t1_m.FORM_INPUTS:
            assert f"- {identifier}\n" not in text, (other.name, identifier)


# --- the instances input -------------------------------------------------------------------------


def test_the_instances_are_the_one_input_of_the_manifest_in_place_of_the_t1_m_inputs() -> None:
    inputs = manifest().inputs

    assert t1_m.INPUTS <= inputs
    assert inputs.isdisjoint(t1_m.FORM_INPUTS)


def test_the_moves_kind_is_a_record_list_of_every_t1_m_input_in_line_order() -> None:
    assert isinstance(T1_M_MOVES, RecordListKind)
    assert T1_M_MOVES.identifier == "ca/t1_m_moves"
    assert frozenset(field.identifier for field in T1_M_MOVES.fields) == t1_m.FORM_INPUTS
    assert len(T1_M_MOVES.fields) == len(t1_m.FORM_INPUTS) == 19


def test_the_catalog_registers_the_moves_kind_beside_the_other_record_lists() -> None:
    build_tax_computation()

    assert ArtifactRegistry.shared().kind("ca/t1_m_moves") is T1_M_MOVES


# --- the outputs and the node --------------------------------------------------------------------


def test_the_return_declares_no_output_for_line_30_which_nothing_reads() -> None:
    (default, *_) = manifest().forms
    exports = set(default.exports)

    assert t1_m.OUTPUTS <= exports
    assert "ca/moving_unused_expenses" not in exports
    assert not {export for export in exports if "." in export}


def test_the_form_set_runs_the_form_once_for_each_move_and_derives_its_two_kinds() -> None:
    found = composed()

    assert found.instances == T1_M_MOVES
    assert found.imports == frozenset()
    assert found.derived == (
        t1_m.MOVING_EXPENSES_CLAIM_PER_MOVE,
        t1_m.MOVING_UNUSED_EXPENSES_PER_MOVE,
    )


def test_the_claim_export_is_a_record_list_of_the_line_29_amount() -> None:
    (claim,) = (
        kind for kind in composed().derived if kind.identifier == "ca/t1_m.moving_expenses_claim"
    )

    assert claim == t1_m.MOVING_EXPENSES_CLAIM_PER_MOVE
    assert claim.fields == (MOVING_EXPENSES_CLAIM,)


def test_the_return_total_adds_the_claim_of_every_move_into_line_21900() -> None:
    # T1 line 21900 "Moving expenses (complete Form T1-M)": line 29 of each move, added.
    (step,) = t1_m.STEPS
    assert step.name == "core/record_total"
    assert step.consumes == {"records": "ca/t1_m.moving_expenses_claim"}
    assert step.produces == {"output": "ca/moving_expenses_deduction"}
    assert MOVING_EXPENSES_DEDUCTION.identifier == "ca/moving_expenses_deduction"


def test_the_selections_inside_the_form_are_wired_as_the_family_says() -> None:
    inner = {
        (type(capability), capability.consumes, capability.produces)
        for capability in composed().composition.order
    }

    assert inner == t1_m.FORM_WIRING
