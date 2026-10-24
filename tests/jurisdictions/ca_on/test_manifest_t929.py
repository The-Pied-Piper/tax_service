"""Form T929 in the CA-ON manifest: one copy at most, the copies of the return's steps, and the line
21500 the return reads.

Form T929 (the disability supports deduction, T1 line 21500) is the form `ca/t929`, run once for
the one copy of the form the return carries (none, with an empty `ca/t929_instances`; at most one).
Its selections are in the parts `05k_t929.yaml` (the form's header and its 12 own steps,
`OWN_STEPS`) and `05l_t929_copies_1.yaml` and `05m_t929_copies_2.yaml` (the form only, with 131
copies of the return's steps that compute net income, `COPIED_STEPS`). The return keeps the
originals, and a guard checks that each copy is its original on the return, except the line 23300
sum, which the return adds the deduction to. The return re-produces the deduction with one
`core/record_total` over the form's derived kind, placed before that sum in `05_deductions.yaml`.
The entries are listed in `manifest_families/t929.py`.
"""

from __future__ import annotations

from pathlib import Path

import yaml

import app.jurisdictions.ca_on
import app.registrations  # lists the packages; build_tax_computation registers their catalogs
from app.adapters.outbound.yaml_jurisdictions import YamlJurisdictionSource
from app.domain.artifact import ArtifactRegistry
from app.domain.capabilities.sum import Sum
from app.domain.form import FormComposition
from app.domain.jurisdiction_code import JurisdictionCode
from app.domain.manifest import CapabilitySelection, Form, Manifest
from app.domain.record_list import RecordListKind
from app.jurisdictions.ca.catalog import (
    DEDUCTIONS_FROM_TOTAL_INCOME,
    DISABILITY_SUPPORTS_DEDUCTION,
    T929_INSTANCES,
)
from app.main import build_tax_computation
from tests.jurisdictions.ca_on.manifest_families import t929

CA_ON = JurisdictionCode("CA-ON")
PARTS = Path(app.jurisdictions.ca_on.__file__).parent / "manifests" / "v1"
FORM_PARTS = ("05k_t929.yaml", "05l_t929_copies_1.yaml", "05m_t929_copies_2.yaml")
COPIES_PARTS = FORM_PARTS[1:]
INPUTS_PART = PARTS / "01_inputs.yaml"
DEDUCTIONS_PART = PARTS / "05_deductions.yaml"
DEDUCTIONS_SUM = "ca/deductions_from_total_income"
DEDUCTION_PRODUCER = "ca/disability_supports_deduction"


def manifest() -> Manifest:
    (only,) = (
        YamlJurisdictionSource(app.registrations.JURISDICTIONS.roots())
        .get_jurisdiction(CA_ON)
        .manifests
    )
    return only


def form() -> Form:
    (found,) = (found for found in manifest().forms if found.name == "ca/t929")
    return found


def composed() -> FormComposition:
    return build_tax_computation().compose(CA_ON, 2025).form("ca/t929")


def return_wiring() -> set[tuple[type, frozenset[object], frozenset[object]]]:
    composition = build_tax_computation().compose(CA_ON, 2025).form("ca-on/return").composition
    return {
        (type(capability), capability.consumes, capability.produces)
        for capability in composition.order
    }


def produced_by(selections: set[CapabilitySelection], name: str) -> CapabilitySelection:
    (found,) = (selection for selection in selections if name in selection.produces.values())
    return found


# --- the parts and the form ----------------------------------------------------------------------


def test_the_first_part_declares_the_form_t929_with_its_instances_limits_and_exports() -> None:
    declared = yaml.safe_load((PARTS / FORM_PARTS[0]).read_text())["form"]

    assert declared == {
        "name": "ca/t929",
        "instances": "ca/t929_instances",
        "max_instances": 1,
        "min_instances": 0,
        "exports": list(t929.FORM_EXPORTS),
    }
    assert len(t929.FORM_EXPORTS) == 7


def test_the_copies_parts_declare_only_the_form_ca_t929() -> None:
    for name in COPIES_PARTS:
        assert yaml.safe_load((PARTS / name).read_text())["form"] == {"name": "ca/t929"}, name


def test_each_t929_part_is_not_over_30_kb() -> None:
    for name in FORM_PARTS:
        assert (PARTS / name).stat().st_size <= 30 * 1024, name


def test_the_manifest_has_the_form_t929_with_at_most_one_instance() -> None:
    found = form()

    assert found.name == "ca/t929"
    assert found.instances == "ca/t929_instances"
    assert found.exports == t929.FORM_EXPORTS
    assert (found.min_instances, found.max_instances) == (0, 1)
    assert found.exclusive_group is None


def test_the_form_holds_the_12_own_and_131_copied_selections() -> None:
    found = form()

    assert len(t929.OWN_STEPS) == 12
    assert len(t929.COPIED_STEPS) == 131
    assert t929.FORM_STEPS == t929.OWN_STEPS | t929.COPIED_STEPS
    assert len(found.capabilities) == 143
    assert set(found.capabilities) == t929.FORM_STEPS


def test_the_return_totals_the_deduction_with_one_record_total_and_no_form_step() -> None:
    (default, *_) = manifest().forms
    selected = set(default.capabilities)

    assert t929.STEPS <= selected
    assert not selected & t929.OWN_STEPS
    assert {step.name for step in t929.STEPS} == {"core/record_total"}
    assert len(t929.STEPS) == 1


# --- the guard: each copy is its original on the return ------------------------------------------


def test_guard_every_copied_step_is_its_original_on_the_return_except_the_line_23300_sum() -> None:
    (default, *_) = manifest().forms
    selected = set(default.capabilities)
    copied_sum = produced_by(t929.COPIED_STEPS, DEDUCTIONS_SUM)

    assert t929.COPIED_STEPS - {copied_sum} <= selected
    original_sum = produced_by(selected, DEDUCTIONS_SUM)
    assert original_sum.name == copied_sum.name == "core/sum"
    assert original_sum.params == copied_sum.params
    # The return's sum is the copy's with the deduction added after child care expenses.
    original_parts = original_sum.consumes["parts"]
    copied_parts = copied_sum.consumes["parts"]
    assert set(original_parts) == set(copied_parts) | {DEDUCTION_PRODUCER}
    assert (
        original_parts.index(DEDUCTION_PRODUCER)
        == original_parts.index("ca/child_care_expenses") + 1
    )
    assert original_sum.produces == copied_sum.produces


def test_guard_each_copied_step_is_wired_as_its_original_on_the_return() -> None:
    own_outputs = {output for step in t929.OWN_STEPS for output in step.produces.values()}
    form_wiring = {
        (type(capability), capability.consumes, capability.produces)
        for capability in composed().composition.order
    }
    copied_wiring = {
        wiring
        for wiring in form_wiring
        if not {kind.identifier for kind in wiring[2]} & own_outputs
    }

    assert len(copied_wiring) == 131
    missing = copied_wiring - return_wiring()
    # Only the line 23300 sum differs: the return adds the deduction to it.
    (only,) = missing
    assert only[0] is Sum
    assert only[2] == frozenset({DEDUCTIONS_FROM_TOTAL_INCOME})
    assert only[1] | {DISABILITY_SUPPORTS_DEDUCTION} in {
        wiring[1]
        for wiring in return_wiring()
        if wiring[0] is Sum and wiring[2] == frozenset({DEDUCTIONS_FROM_TOTAL_INCOME})
    }


# --- the return's deduction and the line 23300 sum -----------------------------------------------


def test_the_return_totals_the_deduction_before_the_line_23300_sum_in_05_deductions() -> None:
    steps = yaml.safe_load(DEDUCTIONS_PART.read_text())["capabilities"]
    totals = [
        index
        for index, step in enumerate(steps)
        if step["name"] == "core/record_total" and step["produces"]["output"] == DEDUCTION_PRODUCER
    ]
    sums = [
        index
        for index, step in enumerate(steps)
        if step["name"] == "core/sum" and step["produces"]["output"] == DEDUCTIONS_SUM
    ]

    (total,) = totals
    (summed,) = sums
    assert steps[total]["consumes"] == {"records": "ca/t929.disability_supports_deduction"}
    assert total < summed
    parts = steps[summed]["consumes"]["parts"]
    assert parts.index(DEDUCTION_PRODUCER) == parts.index("ca/child_care_expenses") + 1


def test_the_other_parts_hold_no_t929_input() -> None:
    inputs_text = INPUTS_PART.read_text()

    for identifier in t929.INPUTS:
        assert f"- {identifier}\n" in inputs_text, identifier
    for name in sorted(path.name for path in PARTS.glob("*.yaml")):
        if name in (*FORM_PARTS, "01_inputs.yaml"):
            continue
        text = (PARTS / name).read_text()
        for identifier in t929.INPUTS:
            assert f"- {identifier}\n" not in text, (name, identifier)


def test_the_disability_supports_deduction_is_no_longer_a_manifest_input() -> None:
    assert DISABILITY_SUPPORTS_DEDUCTION.identifier not in manifest().inputs
    assert f"  - {DEDUCTION_PRODUCER}\n" not in INPUTS_PART.read_text()


# --- the instances and the inputs -----------------------------------------------------------------


def test_the_instances_are_an_input_of_the_manifest() -> None:
    assert t929.INPUTS <= manifest().inputs
    assert "ca/t929_instances" in manifest().inputs


def test_the_instances_kind_is_a_record_list_with_no_fields() -> None:
    assert isinstance(T929_INSTANCES, RecordListKind)
    assert T929_INSTANCES.identifier == "ca/t929_instances"
    assert T929_INSTANCES.fields == ()


def test_the_catalog_registers_the_instances_kind_beside_the_other_record_lists() -> None:
    build_tax_computation()

    assert ArtifactRegistry.shared().kind("ca/t929_instances") is T929_INSTANCES


# --- the form and the return ----------------------------------------------------------------------


def test_the_form_runs_once_per_instance_and_derives_its_seven_kinds() -> None:
    found = composed()

    assert found.instances == T929_INSTANCES
    assert {kind.identifier for kind in found.imports} == t929.IMPORTS
    assert [kind.identifier for kind in found.derived] == [
        f"ca/t929.{export.removeprefix('ca/')}" for export in t929.FORM_EXPORTS
    ]
    assert (found.min_instances, found.max_instances) == (0, 1)


def test_the_form_own_selections_are_wired_as_declared() -> None:
    inner = {
        (type(capability), capability.consumes, capability.produces)
        for capability in composed().composition.order
    }

    assert len(composed().composition.order) == 143
    assert t929.FORM_WIRING <= inner
    assert len(t929.FORM_WIRING) == 12


def test_the_return_wiring_is_one_record_total_over_the_form_derived_kind() -> None:
    assert len(t929.WIRING) == 1
    assert {wiring[0].__name__ for wiring in t929.WIRING} == {"RecordTotal"}
    assert t929.WIRING <= return_wiring()


def test_the_return_declares_no_output_for_the_form_lines() -> None:
    (default, *_) = manifest().forms

    assert not {export for export in default.exports if export.startswith("ca/t929")}
    assert DEDUCTION_PRODUCER not in default.exports
