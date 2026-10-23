"""Form T2048 in the CA-ON manifest: one instance for each disposition, and what the return reads.

T2048 is the form `ca/t2048`, run once for each disposition of the record list
`ca/t2048_dispositions`, whose fields are the 13 T2048 inputs (`FORM_INPUTS`). Its limits are
`min_instances` 0 and `max_instances` 1 (more are not accepted yet). The form's selections are
`FORM_STEPS`: its
34 own (`OWN_STEPS`) and 54 copies of the return's steps that compute the 11 figures it reads
(`COPIED_STEPS`; the return keeps the originals). The form exports the nine artifacts of
`FORM_EXPORTS`; the return re-produces each of them with `core/record_total` over the form's derived
kind `ca/t2048.<name>` (`STEPS`), so every consumer keeps its name and its figure, and with no
disposition every one of them is 0. The form reads the manifest inputs, its record fields and the
other form's export `IMPORTS`. The entries are listed in `manifest_families/t2048.py`.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

import app.jurisdictions.ca_on
import app.registrations  # lists the packages; build_tax_computation registers their catalogs
from app.adapters.inbound.trace_english import EnglishTraceRenderer
from app.adapters.outbound.yaml_jurisdictions import YamlJurisdictionSource
from app.domain.artifact import ArtifactRegistry
from app.domain.errors import ValidationError
from app.domain.form import FormComposition
from app.domain.jurisdiction_code import JurisdictionCode
from app.domain.manifest import Form, Manifest
from app.domain.record_list import RecordListKind
from app.domain.trace.forms import FormInstanceLine
from app.jurisdictions.ca.catalog import (
    QBT_ABIL_REDUCTION,
    QBT_ALLOCATION_TOTAL,
    QBT_CAPITAL_GAINS_DEDUCTION,
    QBT_ELECTION_DEDUCTION,
    QBT_NET_INVESTMENT_LOSS_REDUCTION,
    QBT_TAXABLE_CAPITAL_GAINS,
    QBT_TAXABLE_GAINS_RELATED_TO_DEDUCTION,
    QCC_ELECTION_DEDUCTION,
    QSBCS_QFFP_TAXABLE_GAINS_RELATED_TO_DEDUCTION,
    T2048_DISPOSITIONS,
)
from app.main import build_tax_computation
from tests.jurisdictions.ca_on.end_to_end.support import D, run, service
from tests.jurisdictions.ca_on.manifest_families import t2048

CA_ON = JurisdictionCode("CA-ON")
ROOTS = app.registrations.JURISDICTIONS.roots()
PART = (
    Path(app.jurisdictions.ca_on.__file__).parent
    / "manifests"
    / "v1"
    / "06a_capital_gains_deduction_qbt.yaml"
)
COPIES_PART = PART.with_name("06a_capital_gains_deduction_qbt_copies.yaml")
INCOME_PART = PART.with_name("06_taxable_income.yaml")
INPUTS_PART = PART.with_name("01_inputs.yaml")
VALUED_EXPORTS = (
    QBT_ALLOCATION_TOTAL,
    QCC_ELECTION_DEDUCTION,
    QBT_ELECTION_DEDUCTION,
    QBT_TAXABLE_CAPITAL_GAINS,
    QBT_TAXABLE_GAINS_RELATED_TO_DEDUCTION,
    QSBCS_QFFP_TAXABLE_GAINS_RELATED_TO_DEDUCTION,
    QBT_ABIL_REDUCTION,
    QBT_NET_INVESTMENT_LOSS_REDUCTION,
    QBT_CAPITAL_GAINS_DEDUCTION,
)


def manifest() -> Manifest:
    (only,) = YamlJurisdictionSource(ROOTS).get_jurisdiction(CA_ON).manifests
    return only


def form() -> Form:
    (found,) = (each for each in manifest().forms if each.name == "ca/t2048")
    return found


def composed() -> FormComposition:
    return build_tax_computation().compose(CA_ON, 2025).form("ca/t2048")


# --- the parts and the form ----------------------------------------------------------------------


def test_the_t2048_part_declares_the_form_ca_t2048_with_its_instances_limits_and_exports() -> None:
    declared = yaml.safe_load(PART.read_text())["form"]

    assert declared == {
        "name": "ca/t2048",
        "instances": "ca/t2048_dispositions",
        "min_instances": 0,
        "max_instances": 1,
        "exports": list(t2048.FORM_EXPORTS),
    }


def test_the_t2048_copies_part_declares_only_the_form_ca_t2048() -> None:
    assert yaml.safe_load(COPIES_PART.read_text())["form"] == {"name": "ca/t2048"}


def test_the_t2048_parts_are_not_over_30_kb() -> None:
    assert PART.stat().st_size <= 30 * 1024
    assert COPIES_PART.stat().st_size <= 30 * 1024


def test_the_other_parts_hold_no_t2048_input_and_the_dispositions_input_is_declared() -> None:
    inputs_text = INPUTS_PART.read_text()

    for identifier in t2048.INPUTS:
        assert f"- {identifier}\n" in inputs_text, identifier
    for identifier in t2048.FORM_INPUTS:
        assert f"- {identifier}\n" not in inputs_text, identifier
        assert f"- {identifier}\n" not in INCOME_PART.read_text(), identifier


def test_the_return_part_holds_the_nine_record_totals_of_the_form_exports() -> None:
    steps = yaml.safe_load(INCOME_PART.read_text())["capabilities"]
    totals = {
        (step["consumes"]["records"], step["produces"]["output"])
        for step in steps
        if step["name"] == "core/record_total"
        and step["consumes"]["records"].startswith("ca/t2048.")
    }

    assert totals == {(step.consumes["records"], step.produces["output"]) for step in t2048.STEPS}
    assert len(totals) == len(t2048.FORM_EXPORTS) == 9


# --- the form and the return ---------------------------------------------------------------------


def test_the_manifest_has_the_form_t2048_for_each_disposition_with_at_most_one() -> None:
    found = form()

    assert found.name == "ca/t2048"
    assert found.instances == "ca/t2048_dispositions"
    assert found.exports == t2048.FORM_EXPORTS
    assert found.min_instances == 0
    assert found.max_instances == 1
    assert found.exclusive_group is None


def test_the_form_holds_the_34_own_selections_and_54_copies_of_the_return_steps() -> None:
    found = form()

    assert len(found.capabilities) == 88
    assert set(found.capabilities) == t2048.FORM_STEPS
    assert len(t2048.OWN_STEPS) == 34
    assert len(t2048.COPIED_STEPS) == 54
    assert t2048.FORM_STEPS == t2048.OWN_STEPS | t2048.COPIED_STEPS


def test_the_return_selects_one_record_total_for_each_export_and_none_of_the_form_steps() -> None:
    (default, *_) = manifest().forms
    selected = set(default.capabilities)

    assert t2048.STEPS <= selected
    # The return keeps the 54 steps the form copies (its own originals), and none of its 34 own.
    assert t2048.COPIED_STEPS <= selected
    assert not selected & t2048.OWN_STEPS
    assert {step.name for step in t2048.STEPS} == {"core/record_total"}
    assert len(t2048.STEPS) == len(t2048.FORM_EXPORTS) == 9


def test_the_return_declares_the_outputs_it_reads_or_outputs_and_not_the_claim() -> None:
    (default, *_) = manifest().forms

    assert t2048.OUTPUTS <= set(default.exports)
    assert len(t2048.OUTPUTS) == 8
    # Line 25395 is read by the return (taxable income, the foreign tax credit and the AMT) but is
    # no output of it: the return re-produces it, and declares no export for it.
    assert QBT_CAPITAL_GAINS_DEDUCTION.identifier not in default.exports


# --- the instances input -------------------------------------------------------------------------


def test_the_dispositions_are_the_one_input_of_the_manifest_in_place_of_the_t2048_inputs() -> None:
    inputs = manifest().inputs

    assert t2048.INPUTS <= inputs
    assert inputs.isdisjoint(t2048.FORM_INPUTS)


def test_the_dispositions_kind_is_registered_beside_the_other_record_lists() -> None:
    build_tax_computation()

    assert isinstance(T2048_DISPOSITIONS, RecordListKind)
    assert ArtifactRegistry.shared().kind("ca/t2048_dispositions") is T2048_DISPOSITIONS


def test_the_dispositions_kind_has_the_thirteen_inputs_and_no_nested_list() -> None:
    identifiers = [field.identifier for field in T2048_DISPOSITIONS.fields]

    assert frozenset(identifiers) == t2048.FORM_INPUTS
    assert len(identifiers) == len(t2048.FORM_INPUTS) == 13
    assert not [field for field in T2048_DISPOSITIONS.fields if isinstance(field, RecordListKind)]


# --- the form's run ------------------------------------------------------------------------------


def test_the_form_runs_once_per_disposition_on_its_selections_and_derives_its_nine_kinds() -> None:
    found = composed()

    assert found.instances == T2048_DISPOSITIONS
    assert {kind.identifier for kind in found.imports} == t2048.IMPORTS
    assert len(found.derived) == 9
    assert {kind.identifier for kind in found.derived} == {
        "ca/t2048." + export.split("/", 1)[1] for export in t2048.FORM_EXPORTS
    }


def test_each_derived_kind_is_a_record_list_of_the_export_it_names() -> None:
    by_name = {kind.identifier: kind for kind in composed().derived}

    for export in t2048.FORM_EXPORTS:
        derived = by_name["ca/t2048." + export.split("/", 1)[1]]
        assert isinstance(derived, RecordListKind)
        assert len(derived.fields) == 1
        assert derived.fields[0].identifier == export


def test_the_form_selections_are_wired_as_they_were_on_the_return() -> None:
    inner = {
        (type(capability), capability.consumes, capability.produces)
        for capability in composed().composition.order
    }

    assert inner == t2048.FORM_WIRING
    assert len(composed().composition.order) == 88
    assert len(t2048.FORM_WIRING) == 88


def test_the_form_reads_its_fields_the_other_export_and_shared_manifest_inputs_only() -> None:
    produced = {str(k) for step in t2048.FORM_STEPS for k in step.produces.values()}
    read: set[str] = set()
    for step in t2048.FORM_STEPS:
        for value in step.consumes.values():
            read |= set(value) if isinstance(value, (tuple, list)) else {value}
    external = read - produced
    # The copies read the return's shared inputs (manifest inputs), the 13 fields and the one
    # export of another form; nothing else comes from outside the form.
    assert t2048.FORM_INPUTS <= external
    assert t2048.IMPORTS <= external
    assert external - t2048.FORM_INPUTS - t2048.IMPORTS <= manifest().inputs


def test_the_return_wiring_is_nine_record_totals_over_the_form_derived_kinds() -> None:
    assert len(t2048.WIRING) == 9
    assert {wiring[0].__name__ for wiring in t2048.WIRING} == {"RecordTotal"}


# --- the limits and the figures ------------------------------------------------------------------


def test_two_dispositions_are_refused_naming_the_form() -> None:
    with pytest.raises(ValidationError) as raised:
        run("0", (), "0", "0", "0", "0", "0", t2048_dispositions_rows=({}, {}))

    assert str(raised.value).startswith("form 'ca/t2048' allows at most 1 instance(s), got 2")


def test_with_zero_dispositions_every_exported_total_is_zero() -> None:
    runs = run("0", (), "0", "0", "0", "0", "0", t2048_dispositions_rows=())
    worksheet = runs["ca-on/return"][0]

    assert runs.get("ca/t2048", ()) == ()
    for kind in VALUED_EXPORTS:
        assert worksheet.get(kind).value == D("0"), kind.identifier


def test_the_form_run_is_a_form_instance_line_whose_lines_read_ca_t2048_instance_1() -> None:
    runs = run(
        "0", (), "0", "0", "0", "0", "0", t2048_dispositions_rows=({"qbt_capital_gains": "100000"},)
    )
    (line,) = [
        each
        for each in service().compose(CA_ON, 2025).trace(runs)
        if isinstance(each, FormInstanceLine) and each.form == "ca/t2048"
    ]

    assert line.position == 1
    assert line.lines == runs["ca/t2048"][0].trace
    (text,) = EnglishTraceRenderer().render_all((line,))
    assert text.split("\n")
    assert all(sentence.startswith("ca/t2048, instance 1: ") for sentence in text.split("\n"))
