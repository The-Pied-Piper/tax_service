"""Unit tests for TaxComputationService with forms: a form run once per instance, end to end.

A manifest's `forms` are groups of selections with an instances kind (a record list, one record per
instance) and `exports`. The service builds one inner `Composition` per form, once, with the same
`CapabilityBuilder`, datasets and registries as the return's; the form takes part in the return's
composition as one node (`FormRun`) that consumes the instances kind and produces, for each export
`X` of form `B`, the derived artifact `B.X`: a record list of ONE field (X's kind) with a record per
instance, in instance order. `B.X` kinds are built by the engine and registered into the artifact
registry at compose time, idempotently, so the return's selections consume them by identifier. With
no instances, each `B.X` is an empty record list. Everything here is made up (`ex/` names).
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import replace
from decimal import Decimal
from typing import Any, ClassVar

import pytest

from app.application.services.tax_computation import TaxComputationService
from app.domain.artifact import Artifact, ArtifactKind, ArtifactRegistry
from app.domain.capabilities.record_total import RecordTotal
from app.domain.capabilities.subtract import Subtract
from app.domain.capability import Capability, CapabilityRegistry, CapabilityResult
from app.domain.errors import (
    CapabilityContractError,
    DuplicateRegistrationError,
    InvalidCompositionError,
    MissingArtifactError,
    NotFoundError,
    UnknownRegistrationError,
)
from app.domain.form import FormRun
from app.domain.jurisdiction import Jurisdiction
from app.domain.jurisdiction_code import JurisdictionCode
from app.domain.manifest import CapabilitySelection, Form, Manifest
from app.domain.record_list import RecordList, RecordListKind
from app.domain.trace import FormInstanceLine, RecordTotalLine, SubtractedLine
from tests.application.services.test_tax_computation import (
    BASE,
    FACTOR,
    FakeJurisdictions,
    FakeParameters,
    Scale,
    StepLine,
    factor_data,
)

D = Decimal
EX_ON = JurisdictionCode("EX-ON")

# --- the made-up rental form: two amounts and a nested list of unit rents per instance ---------

GROSS_RENT = ArtifactKind("ex/gross_rent", Decimal)
EXPENSES = ArtifactKind("ex/expenses", Decimal)
NET_INCOME = ArtifactKind("ex/net_income", Decimal, non_negative=True)
UNIT_AMOUNT = ArtifactKind("ex/unit_amount", Decimal)
UNITS = RecordListKind("ex/units", fields=(UNIT_AMOUNT,))
UNITS_DOUBLED = RecordListKind("ex/units_doubled", fields=(UNIT_AMOUNT,))
RENTALS = RecordListKind("ex/rentals", fields=(GROSS_RENT, EXPENSES, UNITS))
TOTAL_NET_INCOME = ArtifactKind("ex/total_net_income", Decimal)
OTHER_AMOUNT = ArtifactKind("ex/other_amount", Decimal)
SPARE = ArtifactKind("ex/spare", Decimal)
NOTES = ArtifactKind("ex/notes", Decimal)
NOTE = ArtifactKind("ex/note", str)

# The kinds the engine derives for the rental form's two exports: one field, a record per instance.
NET_INCOME_PER_RENTAL = RecordListKind("ex/rental.net_income", fields=(NET_INCOME,))
UNITS_DOUBLED_PER_RENTAL = RecordListKind("ex/rental.units_doubled", fields=(UNITS_DOUBLED,))

# The made-up scaling form: `ex/bases` instances, each scaled by the `ex/factor` dataset.
BASES = RecordListKind("ex/bases", fields=(BASE,))
SCALED = ArtifactKind("ex/scaled", Decimal)
SCALED_TOTAL = ArtifactKind("ex/scaled_total", Decimal)
SCALED_PER_BASE = RecordListKind("ex/scaling.scaled", fields=(SCALED,))


class DoubleUnits(Capability):
    """Produces `doubled`: the consumed `units` list with every amount doubled, same order."""

    CONSUMES: ClassVar[Mapping[str, type]] = {"units": RecordList}
    PRODUCES: ClassVar[Mapping[str, type]] = {"doubled": RecordList}

    def __init__(self, units: RecordListKind, doubled: RecordListKind) -> None:
        super().__init__(units=units, doubled=doubled)
        self._units, self._doubled = units, doubled

    def compute(self, inputs: tuple[Artifact[Any], ...]) -> CapabilityResult:
        records = self._input(inputs, self._units).value.records
        value = RecordList(
            self._doubled.fields, [{UNIT_AMOUNT: record[UNIT_AMOUNT] * 2} for record in records]
        )
        return CapabilityResult(
            outputs=(Artifact(self._doubled, value),), trace=(StepLine("doubled", D(len(records))),)
        )


class Describe(Capability):
    """Produces `note`, a text: not a kind a form may export."""

    CONSUMES: ClassVar[Mapping[str, type]] = {"source": Decimal}
    PRODUCES: ClassVar[Mapping[str, type]] = {"note": str}

    def __init__(self, source: ArtifactKind[Decimal], note: ArtifactKind[str]) -> None:
        super().__init__(source=source, note=note)
        self._note = note

    def compute(self, inputs: tuple[Artifact[Any], ...]) -> CapabilityResult:
        return CapabilityResult(outputs=(Artifact(self._note, "x"),), trace=())


NET = CapabilitySelection(
    name="core/subtract",
    params={},
    consumes={"amount": "ex/gross_rent", "less": "ex/expenses"},
    produces={"output": "ex/net_income"},
)
DOUBLE = CapabilitySelection(
    name="ex/double_units",
    params={},
    consumes={"units": "ex/units"},
    produces={"doubled": "ex/units_doubled"},
)
RENTAL = Form(
    name="ex/rental",
    instances="ex/rentals",
    exports=("ex/net_income", "ex/units_doubled"),
    capabilities=(NET, DOUBLE),
)
TOTAL = CapabilitySelection(
    name="core/record_total",
    params={},
    consumes={"records": "ex/rental.net_income"},
    produces={"output": "ex/total_net_income"},
)
SCALE = CapabilitySelection(
    name="ex/scale",
    params={"factor": "ex/factor"},
    consumes={"source": "ex/base"},
    produces={"target": "ex/scaled"},
)
SCALING = Form(
    name="ex/scaling", instances="ex/bases", exports=("ex/scaled",), capabilities=(SCALE,)
)
SCALED_SUM = CapabilitySelection(
    name="core/record_total",
    params={},
    consumes={"records": "ex/scaling.scaled"},
    produces={"output": "ex/scaled_total"},
)


def rental_manifest(
    form: Form = RENTAL,
    inputs: frozenset[str] = frozenset({"ex/rentals"}),
) -> Manifest:
    return Manifest(
        jurisdiction=EX_ON,
        version=1,
        valid_from_tax_year=2025,
        capabilities=(TOTAL,),
        inputs=inputs,
        outputs=frozenset({"ex/total_net_income", "ex/rental.units_doubled"}),
        forms=(form,),
    )


def scaling_manifest() -> Manifest:
    return Manifest(
        jurisdiction=EX_ON,
        version=1,
        valid_from_tax_year=2025,
        capabilities=(SCALED_SUM,),
        inputs=frozenset({"ex/bases"}),
        outputs=frozenset({"ex/scaled_total"}),
        forms=(SCALING,),
    )


def both_manifest() -> Manifest:
    return Manifest(
        jurisdiction=EX_ON,
        version=1,
        valid_from_tax_year=2025,
        capabilities=(TOTAL, SCALED_SUM),
        inputs=frozenset({"ex/rentals", "ex/bases"}),
        outputs=frozenset({"ex/total_net_income", "ex/rental.units_doubled", "ex/scaled_total"}),
        forms=(RENTAL, SCALING),
    )


def artifact_registry(
    *extra: ArtifactKind[Any], rentals_kind: RecordListKind = RENTALS
) -> ArtifactRegistry:
    registry = ArtifactRegistry()
    kinds: tuple[ArtifactKind[Any], ...] = (
        GROSS_RENT,
        EXPENSES,
        NET_INCOME,
        UNIT_AMOUNT,
        UNITS,
        UNITS_DOUBLED,
        rentals_kind,
        TOTAL_NET_INCOME,
        OTHER_AMOUNT,
        SPARE,
        NOTES,
        NOTE,
        BASE,
        SCALED,
        BASES,
        SCALED_TOTAL,
    )
    for kind in (*kinds, *extra):
        registry.register(kind.identifier, kind)
    return registry


def capability_registry() -> CapabilityRegistry:
    registry = CapabilityRegistry()
    registry.register("core/subtract", Subtract)
    registry.register("core/record_total", RecordTotal)
    registry.register("ex/double_units", DoubleUnits)
    registry.register("ex/describe", Describe)
    registry.register("ex/scale", Scale)
    return registry


def service(
    manifest: Manifest,
    artifacts: ArtifactRegistry | None = None,
    parameters: FakeParameters | None = None,
) -> TaxComputationService:
    return TaxComputationService(
        FakeJurisdictions(Jurisdiction(code=EX_ON, manifests=(manifest,))),
        parameters if parameters is not None else FakeParameters(factor_data()),
        capability_registry(),
        artifacts if artifacts is not None else artifact_registry(),
    )


def units(*amounts: str) -> RecordList:
    return RecordList(UNITS.fields, [{UNIT_AMOUNT: D(amount)} for amount in amounts])


def rentals(*instances: tuple[str, str, RecordList]) -> Artifact[Any]:
    records: list[dict[ArtifactKind[Any], object]] = [
        {GROSS_RENT: D(gross), EXPENSES: D(expenses), UNITS: listed}
        for gross, expenses, listed in instances
    ]
    return Artifact(RENTALS, RecordList(RENTALS.fields, records))


TWO_RENTALS = rentals(
    ("12000", "2000", units("100", "250.50")),
    ("5000", "1000", units()),
)


# --- two instances, end to end ---------------------------------------------------------------


def test_two_instances_are_run_each_on_its_own_and_totalled_by_the_return() -> None:
    worksheet = service(rental_manifest()).compute(EX_ON, 2025, TWO_RENTALS)

    assert worksheet.get(TOTAL_NET_INCOME).value == D("14000")


def test_an_export_is_a_record_list_of_one_field_with_a_record_per_instance() -> None:
    artifacts = artifact_registry()
    worksheet = service(rental_manifest(), artifacts).compute(EX_ON, 2025, TWO_RENTALS)

    net = artifacts.kind("ex/rental.net_income")
    assert net == NET_INCOME_PER_RENTAL
    assert worksheet.get(net).value == RecordList(
        (NET_INCOME,), [{NET_INCOME: D("10000")}, {NET_INCOME: D("4000")}]
    )


def test_instance_order_is_the_order_of_the_records_given() -> None:
    swapped = rentals(
        ("5000", "1000", units()),
        ("12000", "2000", units("100")),
    )
    artifacts = artifact_registry()

    worksheet = service(rental_manifest(), artifacts).compute(EX_ON, 2025, swapped)

    net = worksheet.get(artifacts.kind("ex/rental.net_income")).value
    assert [record[NET_INCOME] for record in net.records] == [D("4000"), D("10000")]


def test_a_list_valued_export_is_a_record_list_of_nested_record_lists() -> None:
    artifacts = artifact_registry()
    worksheet = service(rental_manifest(), artifacts).compute(EX_ON, 2025, TWO_RENTALS)

    doubled = artifacts.kind("ex/rental.units_doubled")

    assert doubled == UNITS_DOUBLED_PER_RENTAL
    assert worksheet.get(doubled).value == RecordList(
        (UNITS_DOUBLED,),
        [
            {
                UNITS_DOUBLED: RecordList(
                    UNITS_DOUBLED.fields,
                    [{UNIT_AMOUNT: D("200")}, {UNIT_AMOUNT: D("501.00")}],
                )
            },
            {UNITS_DOUBLED: RecordList(UNITS_DOUBLED.fields, [])},
        ],
    )


def test_an_instance_holds_a_nested_record_list_the_form_reads() -> None:
    # The first instance's class table (`ex/units`) reaches the form's capability whole.
    artifacts = artifact_registry()
    one = rentals(("100", "0", units("1", "2", "3")))

    worksheet = service(rental_manifest(), artifacts).compute(EX_ON, 2025, one)

    (record,) = worksheet.get(artifacts.kind("ex/rental.units_doubled")).value.records
    assert [each[UNIT_AMOUNT] for each in record[UNITS_DOUBLED].records] == [D(2), D(4), D(6)]


def test_the_export_artifacts_are_produced_by_the_form_node() -> None:
    artifacts = artifact_registry()
    worksheet = service(rental_manifest(), artifacts).compute(EX_ON, 2025, TWO_RENTALS)

    for identifier in ("ex/rental.net_income", "ex/rental.units_doubled"):
        assert isinstance(worksheet.producer_of(artifacts.kind(identifier)), FormRun)
    assert isinstance(worksheet.producer_of(TOTAL_NET_INCOME), RecordTotal)
    assert worksheet.producer_of(RENTALS) is None


def test_an_inner_artifact_that_is_not_an_export_never_reaches_the_returns_worksheet() -> None:
    worksheet = service(rental_manifest()).compute(EX_ON, 2025, TWO_RENTALS)

    inner: tuple[ArtifactKind[Any], ...] = (GROSS_RENT, EXPENSES, NET_INCOME, UNITS, UNITS_DOUBLED)
    for kind in inner:
        with pytest.raises(MissingArtifactError, match="no value"):
            worksheet.get(kind)


# --- zero instances --------------------------------------------------------------------------


def test_no_instances_still_produces_every_export_as_an_empty_record_list() -> None:
    artifacts = artifact_registry()

    worksheet = service(rental_manifest(), artifacts).compute(EX_ON, 2025, rentals())

    assert worksheet.get(artifacts.kind("ex/rental.net_income")).value == RecordList(
        (NET_INCOME,), []
    )
    assert worksheet.get(artifacts.kind("ex/rental.units_doubled")).value == RecordList(
        (UNITS_DOUBLED,), []
    )
    assert worksheet.get(TOTAL_NET_INCOME).value == D(0)


def test_no_instances_leaves_only_the_returns_own_trace() -> None:
    worksheet = service(rental_manifest()).compute(EX_ON, 2025, rentals())

    assert worksheet.trace == (RecordTotalLine(TOTAL_NET_INCOME, NET_INCOME, (), D(0)),)


# --- the trace: one line per instance, then the returns own lines -----------------------------


def test_each_instances_trace_is_grouped_in_one_line_named_by_form_and_position() -> None:
    worksheet = service(rental_manifest()).compute(EX_ON, 2025, TWO_RENTALS)

    first, second, total = worksheet.trace

    assert isinstance(first, FormInstanceLine) and isinstance(second, FormInstanceLine)
    assert (first.form, first.position) == ("ex/rental", 1)
    assert (second.form, second.position) == ("ex/rental", 2)
    assert total == RecordTotalLine(
        TOTAL_NET_INCOME, NET_INCOME, (D("10000"), D("4000")), D("14000")
    )


def test_an_instances_lines_are_those_of_its_own_run() -> None:
    worksheet = service(rental_manifest()).compute(EX_ON, 2025, TWO_RENTALS)

    first, second, _total = worksheet.trace
    assert isinstance(first, FormInstanceLine) and isinstance(second, FormInstanceLine)

    def results(line: FormInstanceLine) -> list[Decimal]:
        return [inner.result for inner in line.lines if isinstance(inner, SubtractedLine)]

    assert results(first) == [D("10000")]
    assert results(second) == [D("4000")]
    assert StepLine("doubled", D(2)) in first.lines
    assert StepLine("doubled", D(0)) in second.lines
    assert len(first.lines) == len(second.lines) == 2


# --- compose: the form is one node of the returns composition -------------------------------


def test_compose_has_one_form_node_that_consumes_the_instances_and_produces_the_exports() -> None:
    artifacts = artifact_registry()

    composition = service(rental_manifest(), artifacts).compose(EX_ON, 2025)

    (node,) = [c for c in composition.order if isinstance(c, FormRun)]
    assert isinstance(node, Capability)
    assert node.consumes == frozenset({RENTALS})
    assert node.produces == frozenset({NET_INCOME_PER_RENTAL, UNITS_DOUBLED_PER_RENTAL})
    assert [type(c) for c in composition.order] == [FormRun, RecordTotal]


def test_two_forms_are_peers_each_with_its_own_node_and_exports() -> None:
    artifacts = artifact_registry()
    manifest = both_manifest()
    bases = Artifact(BASES, RecordList(BASES.fields, [{BASE: D("2")}, {BASE: D("5")}]))

    worksheet = service(manifest, artifacts).compute(EX_ON, 2025, TWO_RENTALS, bases)

    assert worksheet.get(TOTAL_NET_INCOME).value == D("14000")
    assert worksheet.get(SCALED_TOTAL).value == D("21")
    assert worksheet.get(artifacts.kind("ex/scaling.scaled")).value.records[1][SCALED] == D("15")


def test_the_instances_kind_must_be_one_of_the_manifests_inputs() -> None:
    # The return reads two other amounts, so its inputs are used; the form's `ex/rentals` is not
    # among them and nothing produces it.
    reads_others = CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ex/other_amount", "less": "ex/notes"},
        produces={"output": "ex/spare"},
    )
    manifest = replace(
        rental_manifest(),
        capabilities=(TOTAL, reads_others),
        inputs=frozenset({"ex/other_amount", "ex/notes"}),
        outputs=frozenset({"ex/total_net_income", "ex/rental.units_doubled", "ex/spare"}),
    )

    with pytest.raises(
        InvalidCompositionError, match="no producer for 'rentals', consumed by FormRun"
    ):
        service(manifest).compose(EX_ON, 2025)


def test_the_computation_takes_the_instances_and_nothing_else_of_the_form() -> None:
    composition = service(rental_manifest()).compose(EX_ON, 2025)

    with pytest.raises(InvalidCompositionError, match="missing input 'rentals'"):
        composition.compute()
    with pytest.raises(InvalidCompositionError, match="'gross_rent' is not an input"):
        composition.compute(TWO_RENTALS, Artifact(GROSS_RENT, D(1)))


# --- the derived kinds are registered at compose time, idempotently ---------------------------


def test_compose_registers_the_derived_kinds_by_their_dotted_identifiers() -> None:
    artifacts = artifact_registry()
    assert "ex/rental.net_income" not in artifacts.identifiers()

    service(rental_manifest(), artifacts).compose(EX_ON, 2025)

    assert artifacts.kind("ex/rental.net_income") == NET_INCOME_PER_RENTAL
    assert artifacts.kind("ex/rental.units_doubled") == UNITS_DOUBLED_PER_RENTAL


def test_composing_twice_registers_the_derived_kinds_once_and_keeps_the_first() -> None:
    artifacts = artifact_registry()
    computation = service(rental_manifest(), artifacts)

    first = computation.compose(EX_ON, 2025)
    registered = artifacts.kind("ex/rental.net_income")
    second = computation.compose(EX_ON, 2025)

    assert artifacts.kind("ex/rental.net_income") is registered
    (node,) = [c for c in second.order if isinstance(c, FormRun)]
    assert node.produces == frozenset({NET_INCOME_PER_RENTAL, UNITS_DOUBLED_PER_RENTAL})
    assert [type(c) for c in first.order] == [type(c) for c in second.order]


def test_each_compose_computes_the_same_figures() -> None:
    computation = service(rental_manifest())

    totals = [
        computation.compute(EX_ON, 2025, TWO_RENTALS).get(TOTAL_NET_INCOME).value for _ in range(3)
    ]

    assert totals == [D("14000")] * 3


def test_two_services_on_one_registry_agree_on_the_derived_kinds() -> None:
    artifacts = artifact_registry()

    service(rental_manifest(), artifacts).compose(EX_ON, 2025)
    service(rental_manifest(), artifacts).compose(EX_ON, 2025)

    assert artifacts.kind("ex/rental.net_income") == NET_INCOME_PER_RENTAL


@pytest.mark.parametrize(
    "other",
    [
        ArtifactKind("ex/rental.net_income", Decimal),
        RecordListKind("ex/rental.net_income", fields=(GROSS_RENT,)),
    ],
    ids=["a-plain-amount", "a-list-of-another-field"],
)
def test_another_kind_under_a_derived_identifier_is_an_error(other: ArtifactKind[Any]) -> None:
    artifacts = artifact_registry(other)

    with pytest.raises(DuplicateRegistrationError, match=r"ex/rental\.net_income"):
        service(rental_manifest(), artifacts).compose(EX_ON, 2025)


# --- the form's selections are built like the returns: datasets, once per form ---------------


def test_the_forms_datasets_are_fetched_once_for_the_tax_year_not_once_per_instance() -> None:
    parameters = FakeParameters(factor_data())
    bases = Artifact(
        BASES, RecordList(BASES.fields, [{BASE: D("2")}, {BASE: D("5")}, {BASE: D("7")}])
    )

    worksheet = service(scaling_manifest(), parameters=parameters).compute(EX_ON, 2025, bases)

    assert worksheet.get(SCALED_TOTAL).value == D("42")
    assert parameters.requests.count(("ex/factor", 2025, FACTOR)) == 1


def test_a_forms_dataset_of_another_tax_year_is_not_used() -> None:
    parameters = FakeParameters(factor_data(2024))

    with pytest.raises(NotFoundError, match="ex/factor"):
        service(scaling_manifest(), parameters=parameters).compose(EX_ON, 2025)


def test_the_scaling_forms_trace_has_one_line_per_instance() -> None:
    bases = Artifact(BASES, RecordList(BASES.fields, [{BASE: D("2")}, {BASE: D("5")}]))

    worksheet = service(scaling_manifest()).compute(EX_ON, 2025, bases)

    assert worksheet.trace[:2] == (
        FormInstanceLine("ex/scaling", 1, (StepLine("scaled", D("6")),)),
        FormInstanceLine("ex/scaling", 2, (StepLine("scaled", D("15")),)),
    )


# --- errors name the form and the instance position -------------------------------------------


@pytest.mark.parametrize("position", [1, 2])
def test_a_failure_inside_an_instance_names_the_form_and_the_instance(position: int) -> None:
    # `ex/net_income` is non-negative, so a loss in one instance breaks the Subtract contract.
    instances = [("1000", "100", units()), ("1000", "100", units())]
    instances[position - 1] = ("100", "500", units())

    with pytest.raises(
        CapabilityContractError, match=rf"ex/rental, instance {position}\b"
    ) as caught:
        service(rental_manifest()).compute(EX_ON, 2025, rentals(*instances))

    assert "net_income" in str(caught.value)


def test_an_inner_input_nothing_reads_is_refused_naming_the_form() -> None:
    wider = RecordListKind("ex/rentals", fields=(GROSS_RENT, EXPENSES, UNITS, NOTES))
    artifacts = artifact_registry(rentals_kind=wider)

    with pytest.raises(InvalidCompositionError, match="ex/rental") as caught:
        service(rental_manifest(), artifacts).compose(EX_ON, 2025)

    assert "'notes' is consumed by nothing" in str(caught.value)


def test_an_inner_selection_with_no_producer_is_refused_naming_the_form() -> None:
    lost = CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ex/net_income", "less": "ex/other_amount"},
        produces={"output": "ex/spare"},
    )
    form = replace(RENTAL, capabilities=(NET, DOUBLE, lost))

    with pytest.raises(InvalidCompositionError, match="ex/rental") as caught:
        service(rental_manifest(form)).compose(EX_ON, 2025)

    assert "no producer for 'other_amount', consumed by Subtract" in str(caught.value)


def test_an_inner_output_nothing_reads_or_exports_is_refused_naming_the_form() -> None:
    stray = CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ex/net_income", "less": "ex/expenses"},
        produces={"output": "ex/spare"},
    )
    form = replace(RENTAL, capabilities=(NET, DOUBLE, stray))

    with pytest.raises(InvalidCompositionError, match="ex/rental") as caught:
        service(rental_manifest(form)).compose(EX_ON, 2025)

    assert "orphan output 'spare'" in str(caught.value)


def test_an_export_nothing_in_the_form_produces_is_refused_naming_the_form() -> None:
    form = replace(RENTAL, exports=("ex/net_income", "ex/units_doubled", "ex/spare"))

    with pytest.raises(InvalidCompositionError, match="ex/rental") as caught:
        service(rental_manifest(form)).compose(EX_ON, 2025)

    assert "declared output 'spare' is produced by nothing" in str(caught.value)


def test_an_export_that_is_neither_an_amount_a_count_nor_a_record_list_is_refused() -> None:
    describe = CapabilitySelection(
        name="ex/describe",
        params={},
        consumes={"source": "ex/base"},
        produces={"note": "ex/note"},
    )
    form = Form(
        name="ex/labelled", instances="ex/bases", exports=("ex/note",), capabilities=(describe,)
    )
    manifest = Manifest(
        jurisdiction=EX_ON,
        version=1,
        valid_from_tax_year=2025,
        capabilities=(),
        inputs=frozenset({"ex/bases"}),
        outputs=frozenset({"ex/bases"}),
        forms=(form,),
    )

    with pytest.raises(InvalidCompositionError) as caught:
        service(manifest).compose(EX_ON, 2025)

    assert "ex/labelled" in str(caught.value)
    assert "ex/note" in str(caught.value)


def test_instances_that_are_not_a_registered_kind_are_unknown() -> None:
    form = replace(RENTAL, instances="ex/nowhere")

    with pytest.raises(UnknownRegistrationError, match="ex/nowhere"):
        service(rental_manifest(form, inputs=frozenset({"ex/nowhere"}))).compose(EX_ON, 2025)


def test_instances_that_are_not_a_record_list_kind_are_refused_naming_the_form() -> None:
    form = replace(RENTAL, instances="ex/gross_rent")

    with pytest.raises(InvalidCompositionError) as caught:
        service(rental_manifest(form, inputs=frozenset({"ex/gross_rent"}))).compose(EX_ON, 2025)

    assert "ex/rental" in str(caught.value)
    assert "ex/gross_rent" in str(caught.value)
