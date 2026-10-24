"""Form T2048 in the CA-ON manifest: one instance for each disposition, and what the return reads.

T2048 is the form `ca/t2048`, run once for each disposition of the record list
`ca/t2048_dispositions`, whose fields are the 13 T2048 inputs (`FORM_INPUTS`). Its limit is
`min_instances` 0 and no maximum: any number of dispositions is accepted. The form's selections are
`FORM_STEPS`: its 41 own (`OWN_STEPS`) and 54 copies of the return's steps that compute the 11
figures it reads (`COPIED_STEPS`; the return keeps the originals). The form exports the nine
artifacts of `TOTALED_EXPORTS` and a tenth, the order check's; the return re-produces each of the
nine with `core/record_total` over the form's derived kind `ca/t2048.<name>` (`STEPS`), so every
consumer keeps its name and its figure, and with no disposition every one of them is 0. The form
reads the manifest inputs, its record fields, the other form's export `IMPORTS` and its own earlier
runs (`EARLIER`): notes (1) to (3) subtract the sum of the earlier runs' lines 32, 41 and 42 from
lines 8, 23 and Chart A line 20, and a QBT listed after a QCC is an input error. The entries are
listed in `manifest_families/t2048.py`.
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
from app.domain.worksheet import Worksheet
from app.jurisdictions.ca.catalog import (
    ALLOWABLE_BUSINESS_INVESTMENT_LOSS,
    QBT_ABIL_REDUCTION,
    QBT_ALLOCATION_TOTAL,
    QBT_ALLOWABLE_BUSINESS_INVESTMENT_LOSS_AFTER_EARLIER,
    QBT_CAPITAL_GAINS_DEDUCTION,
    QBT_CHART_A_NET_INVESTMENT_LOSS,
    QBT_CHART_A_NET_INVESTMENT_LOSS_AFTER_EARLIER,
    QBT_EARLIER_ABIL_REDUCTION_TOTAL,
    QBT_EARLIER_ALLOCATION_TOTAL,
    QBT_EARLIER_NET_INVESTMENT_LOSS_REDUCTION_TOTAL,
    QBT_ELECTION_DEDUCTION,
    QBT_ELECTION_IS_QBT_IN_ORDER,
    QBT_MAXIMUM_DEDUCTION,
    QBT_NET_INVESTMENT_LOSS_REDUCTION,
    QBT_TAXABLE_CAPITAL_GAINS,
    QBT_TAXABLE_CAPITAL_GAINS_AFTER_EARLIER,
    QBT_TAXABLE_GAINS_LIMIT,
    QBT_TAXABLE_GAINS_NOT_LIMITED,
    QBT_TAXABLE_GAINS_RELATED_TO_DEDUCTION,
    QCC_ELECTION_DEDUCTION,
    QSBCS_QFFP_TAXABLE_GAINS_RELATED_TO_DEDUCTION,
    T2048_DISPOSITIONS,
    TAXABLE_CAPITAL_GAINS,
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


def test_the_t2048_part_declares_the_form_ca_t2048_with_its_instances_minimum_and_exports() -> None:
    declared = yaml.safe_load(PART.read_text())["form"]

    # No `max_instances`: any number of dispositions is accepted.
    assert declared == {
        "name": "ca/t2048",
        "instances": "ca/t2048_dispositions",
        "min_instances": 0,
        "exports": list(t2048.FORM_EXPORTS),
    }
    assert len(t2048.FORM_EXPORTS) == 10


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
    assert len(totals) == len(t2048.TOTALED_EXPORTS) == 9


# --- the form and the return ---------------------------------------------------------------------


def test_the_manifest_has_the_form_t2048_for_each_disposition_with_no_maximum() -> None:
    found = form()

    assert found.name == "ca/t2048"
    assert found.instances == "ca/t2048_dispositions"
    assert found.exports == t2048.FORM_EXPORTS
    assert found.min_instances == 0
    assert found.max_instances is None
    assert found.exclusive_group is None


def test_the_form_holds_the_41_own_selections_and_54_copies_of_the_return_steps() -> None:
    found = form()

    assert len(found.capabilities) == 95
    assert set(found.capabilities) == t2048.FORM_STEPS
    assert len(t2048.OWN_STEPS) == 41
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
    assert len(t2048.STEPS) == len(t2048.TOTALED_EXPORTS) == 9


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


def test_the_form_runs_once_per_disposition_on_its_selections_and_derives_its_ten_kinds() -> None:
    found = composed()

    assert found.instances == T2048_DISPOSITIONS
    assert {kind.identifier for kind in found.imports} == t2048.IMPORTS
    assert len(found.derived) == 10
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
    assert len(composed().composition.order) == 95
    assert len(t2048.FORM_WIRING) == 95


def test_the_form_reads_four_of_its_own_derived_kinds_the_earlier_runs() -> None:
    # Line 32, line 41 and line 42 (notes (1) to (3)) and the election answers (the order check).
    assert {kind.identifier for kind in composed().earlier} == t2048.EARLIER
    assert len(t2048.EARLIER) == 4


def test_the_form_reads_its_fields_the_other_export_its_earlier_runs_and_shared_inputs_only() -> (
    None
):
    produced = {str(k) for step in t2048.FORM_STEPS for k in step.produces.values()}
    read: set[str] = set()
    for step in t2048.FORM_STEPS:
        for value in step.consumes.values():
            read |= set(value) if isinstance(value, (tuple, list)) else {value}
    external = read - produced
    # The copies read the return's shared inputs (manifest inputs), the 13 fields and the one
    # export of another form; the notes and the order check read the form's own earlier runs;
    # nothing else comes from outside the form.
    assert t2048.FORM_INPUTS <= external
    assert t2048.IMPORTS <= external
    assert t2048.EARLIER <= external
    assert external - t2048.FORM_INPUTS - t2048.IMPORTS - t2048.EARLIER <= manifest().inputs


def test_the_return_wiring_is_nine_record_totals_over_the_form_derived_kinds() -> None:
    assert len(t2048.WIRING) == 9
    assert {wiring[0].__name__ for wiring in t2048.WIRING} == {"RecordTotal"}


# --- the limits and the figures ------------------------------------------------------------------


def test_two_dispositions_are_accepted_and_the_form_runs_once_for_each() -> None:
    runs = run("0", (), "0", "0", "0", "0", "0", t2048_dispositions_rows=({}, {}))

    assert len(runs["ca/t2048"]) == 2


def test_any_number_of_dispositions_is_accepted() -> None:
    runs = run("0", (), "0", "0", "0", "0", "0", t2048_dispositions_rows=({},) * 5)

    assert len(runs["ca/t2048"]) == 5


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


# --- notes (1) to (3): the earlier runs' lines 32, 41 and 42 ----------------------------------

# A return with taxable capital gains (line 12700) of 100,000.00, a business investment loss of
# 8,000 (ABIL 4,000.00, line 21700) and carrying charges of 5,000. Each disposition is a QBT:
# line 1 600,000 at 50% (line 7 is 150,000.00), gains of 160,000 (line 16 is 80,000.00) and 30,000
# of other investment expenses (Chart A line 6), with investment expenses in 2025. The first claims
# 40,000; the others claim 0.
QBT: dict[str, str | int] = {
    "qbt_election_eligible_amount": "600000",
    "qbt_percentage_allocated": "50",
    "qbt_capital_gains": "160000",
    "qbt_election_is_qbt": 1,
    "qbt_has_investment_expenses": 1,
    "qbt_other_investment_expenses": "30000",
}


def scenario(rows: tuple[dict[str, str | int], ...]) -> dict[str, tuple[Worksheet, ...]]:
    return run(
        "0",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
        slip_capital_gains_or_losses="200000",
        business_investment_loss="8000",
        total_carrying_charges="5000",
        t2048_dispositions_rows=rows,
    )


def qbts(*claims: str) -> list[Worksheet]:
    rows = tuple({**QBT, "qbt_deduction_claimed": claim} for claim in claims)
    return list(scenario(rows)["ca/t2048"])


def test_the_first_run_has_no_earlier_amount_so_its_lines_are_the_returns() -> None:
    # No earlier run: the sums of all previous amounts are 0, line 8 is line 12700 (100,000.00),
    # line 23 is the ABIL (4,000.00) and Chart A line 20 is 15,000.00: line 10 is 5,000 + 30,000 =
    # 35,000.00 and line 19 is line 18 (100,000.00 - 80,000.00 = 20,000.00), 35,000.00 - 20,000.00.
    (first,) = qbts("40000")

    assert first.get(QBT_EARLIER_ALLOCATION_TOTAL).value == D("0")
    assert first.get(QBT_EARLIER_ABIL_REDUCTION_TOTAL).value == D("0")
    assert first.get(QBT_EARLIER_NET_INVESTMENT_LOSS_REDUCTION_TOTAL).value == D("0")
    assert first.get(QBT_TAXABLE_CAPITAL_GAINS_AFTER_EARLIER).value == D("100000.00")
    assert first.get(QBT_ALLOWABLE_BUSINESS_INVESTMENT_LOSS_AFTER_EARLIER).value == D("4000.00")
    assert first.get(QBT_CHART_A_NET_INVESTMENT_LOSS_AFTER_EARLIER).value == D("15000.00")
    assert first.get(QBT_CHART_A_NET_INVESTMENT_LOSS).value == D("15000.00")


def test_the_first_run_of_several_is_as_it_would_be_alone() -> None:
    # Line 17 is 80,000.00; line 25 is 0 + 4,000.00 + 15,000.00 = 19,000.00; line 26 is 61,000.00;
    # 40,000 is claimed. Line 30 is 80,000.00 - 40,000 = 40,000.00 and line 32 is 80,000.00. Line
    # 35 is 19,000.00; line 36 is the lesser of 40,000.00 and 19,000.00; line 41 is 4,000.00 and
    # line 42 is 15,000.00.
    first, *_ = qbts("40000", "0")

    assert first.get(QBT_ALLOCATION_TOTAL).value == D("80000.00")
    assert first.get(QBT_ABIL_REDUCTION).value == D("4000.00")
    assert first.get(QBT_NET_INVESTMENT_LOSS_REDUCTION).value == D("15000.00")


def test_note_1_takes_the_earlier_line_32_from_line_8() -> None:
    # Note (1): line 8 of the next form is 100,000.00 - 80,000.00 (the first form's line 32) =
    # 20,000.00, so its line 17 is the lesser of that and its line 16 (80,000.00): 20,000.00.
    first, second = qbts("40000", "0")

    assert second.get(QBT_EARLIER_ALLOCATION_TOTAL).value == first.get(QBT_ALLOCATION_TOTAL).value
    assert second.get(QBT_EARLIER_ALLOCATION_TOTAL).value == D("80000.00")
    assert second.get(QBT_TAXABLE_CAPITAL_GAINS_AFTER_EARLIER).value == D("20000.00")
    assert second.get(TAXABLE_CAPITAL_GAINS).value == D("100000.00")
    assert second.get(QBT_TAXABLE_GAINS_LIMIT).value == D("20000.00")
    assert second.get(QBT_TAXABLE_GAINS_NOT_LIMITED).value == D("0")


def test_note_2_takes_the_earlier_line_41_from_line_23() -> None:
    # Note (2): line 23 of the next form is 4,000.00 - 4,000.00 (the first form's line 41) = 0.00.
    first, second = qbts("40000", "0")

    assert second.get(QBT_EARLIER_ABIL_REDUCTION_TOTAL).value == first.get(QBT_ABIL_REDUCTION).value
    assert second.get(QBT_EARLIER_ABIL_REDUCTION_TOTAL).value == D("4000.00")
    assert second.get(ALLOWABLE_BUSINESS_INVESTMENT_LOSS).value == D("4000.00")
    assert second.get(QBT_ALLOWABLE_BUSINESS_INVESTMENT_LOSS_AFTER_EARLIER).value == D("0.00")


def test_note_3_takes_the_earlier_line_42_from_chart_a_line_20() -> None:
    # Note (3): the next form's Chart A line 20 is 35,000.00 (line 10, with line 18 at 0 and
    # nothing else on line 19) - 15,000.00 (the first form's line 42) = 20,000.00, line 24.
    first, second = qbts("40000", "0")

    assert second.get(QBT_EARLIER_NET_INVESTMENT_LOSS_REDUCTION_TOTAL).value == (
        first.get(QBT_NET_INVESTMENT_LOSS_REDUCTION).value
    )
    assert second.get(QBT_CHART_A_NET_INVESTMENT_LOSS).value == D("35000.00")
    assert second.get(QBT_CHART_A_NET_INVESTMENT_LOSS_AFTER_EARLIER).value == D("20000.00")


def test_the_second_run_works_from_the_corrected_lines() -> None:
    # Line 25 is 0 + 0.00 + 20,000.00 = 20,000.00 and line 26 is 20,000.00 - 20,000.00 = 0, so
    # nothing can be claimed (0). Line 28 is 20,000.00, line 30 is 20,000.00 and line 32 is
    # 20,000.00; line 35 is 0.00 + 20,000.00; line 36 is 20,000.00; line 41 is 0.00 x 20,000.00 /
    # 20,000.00 = 0.00 and line 42 is 20,000.00.
    _, second = qbts("40000", "0")

    assert second.get(QBT_MAXIMUM_DEDUCTION).value == D("0")
    assert second.get(QBT_CAPITAL_GAINS_DEDUCTION).value == D("0")
    assert second.get(QBT_ALLOCATION_TOTAL).value == D("20000.00")
    assert second.get(QBT_ABIL_REDUCTION).value == D("0.00")
    assert second.get(QBT_NET_INVESTMENT_LOSS_REDUCTION).value == D("20000.00")


def test_a_third_run_subtracts_the_sum_of_both_earlier_runs() -> None:
    # Line 32: 80,000.00 + 20,000.00 = 100,000.00, so line 8 is 0.00; line 41: 4,000.00 + 0.00, so
    # line 23 is 0.00; line 42: 15,000.00 + 20,000.00 = 35,000.00, so Chart A line 20 is 0.00.
    *_, third = qbts("40000", "0", "0")

    assert third.get(QBT_EARLIER_ALLOCATION_TOTAL).value == D("100000.00")
    assert third.get(QBT_EARLIER_ABIL_REDUCTION_TOTAL).value == D("4000.00")
    assert third.get(QBT_EARLIER_NET_INVESTMENT_LOSS_REDUCTION_TOTAL).value == D("35000.00")
    assert third.get(QBT_TAXABLE_CAPITAL_GAINS_AFTER_EARLIER).value == D("0.00")
    assert third.get(QBT_ALLOWABLE_BUSINESS_INVESTMENT_LOSS_AFTER_EARLIER).value == D("0.00")
    assert third.get(QBT_CHART_A_NET_INVESTMENT_LOSS_AFTER_EARLIER).value == D("0.00")


def test_the_return_totals_each_line_over_the_dispositions() -> None:
    # Line 32: 80,000.00 + 20,000.00; line 41: 4,000.00 + 0.00; line 42: 15,000.00 + 20,000.00;
    # line 25395: 40,000 + 0; Part 5 B (17212) is line 7 of each, 150,000.00 + 150,000.00.
    runs = scenario(tuple({**QBT, "qbt_deduction_claimed": c} for c in ("40000", "0")))
    worksheet = runs["ca-on/return"][0]

    assert worksheet.get(QBT_ALLOCATION_TOTAL).value == D("100000.00")
    assert worksheet.get(QBT_ABIL_REDUCTION).value == D("4000.00")
    assert worksheet.get(QBT_NET_INVESTMENT_LOSS_REDUCTION).value == D("35000.00")
    assert worksheet.get(QBT_CAPITAL_GAINS_DEDUCTION).value == D("40000")
    assert worksheet.get(QBT_ELECTION_DEDUCTION).value == D("300000.00")


# --- "You must claim any deduction under a QBT before any deduction under a QCC." ----------------


def listed(*kinds: str) -> list[Worksheet]:
    """The runs for dispositions that are QBTs ("qbt") or QCCs ("qcc"), in this order."""
    rows = tuple({"qbt_election_is_qbt": 1 if kind == "qbt" else 0} for kind in kinds)
    return list(run("0", (), "0", "0", "0", "0", "0", t2048_dispositions_rows=rows)["ca/t2048"])


@pytest.mark.parametrize(
    "order",
    [
        ("qbt",),
        ("qcc",),
        ("qbt", "qbt"),
        ("qbt", "qcc"),
        ("qcc", "qcc"),
        ("qbt", "qbt", "qcc", "qcc"),
    ],
)
def test_a_qbt_before_any_qcc_is_in_order(order: tuple[str, ...]) -> None:
    runs = listed(*order)

    assert [w.get(QBT_ELECTION_IS_QBT_IN_ORDER).value for w in runs] == [
        1 if kind == "qbt" else 0 for kind in order
    ]


def test_a_qcc_listed_before_a_qbt_is_an_input_error_at_the_qbt() -> None:
    with pytest.raises(ValidationError) as raised:
        listed("qcc", "qbt")

    assert str(raised.value) == (
        "ca/t2048, instance 2: ca/qbt_election_is_qbt is 1 but disposition 1 before it is a QCC: "
        "the QBT must come before the QCC"
    )


def test_the_error_names_the_later_qbt_s_position_and_the_first_qcc_before_it() -> None:
    with pytest.raises(ValidationError) as raised:
        listed("qbt", "qcc", "qcc", "qbt")

    assert str(raised.value).startswith("ca/t2048, instance 4: ")
    assert "disposition 2 before it is a QCC" in str(raised.value)
    assert "the QBT must come before the QCC" in str(raised.value)


def test_a_qbt_listed_after_a_qcc_is_refused_even_with_no_figures() -> None:
    # The order is the filer's designation; the check reads the answers only, not the amounts.
    with pytest.raises(ValidationError, match="QBT must come before the QCC"):
        run(
            "0",
            (),
            "0",
            "0",
            "0",
            "0",
            "0",
            t2048_dispositions_rows=({"qbt_election_is_qbt": 0}, {"qbt_election_is_qbt": 1}),
        )
