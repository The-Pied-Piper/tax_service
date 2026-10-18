"""Unit tests for TaxComputationService: a jurisdiction's manifest built into a composition, run.

The service does the I/O only: it reads the jurisdiction, takes the manifest for the tax year,
resolves each selection's class and datasets from the ports and registries it was given, has
`CapabilityBuilder` build each capability from them and the artifact registry (the builder resolves
artifact kinds), and builds the `Composition`. Resolution errors
propagate unchanged. The ports are small in-memory fakes and the registries private ones; every
code, capability, kind and dataset is made up.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from decimal import Decimal
from functools import cache
from typing import Any, ClassVar, assert_type

import pytest

from app.application.ports.jurisdiction_source import JurisdictionSource
from app.application.ports.parameter_source import ParameterSource
from app.application.services.tax_computation import TaxComputationService
from app.domain.artifact import Artifact, ArtifactKind, ArtifactRegistry, Money
from app.domain.capability import Capability, CapabilityRegistry, CapabilityResult
from app.domain.composition import Composition
from app.domain.errors import (
    InvalidCompositionError,
    InvalidParameterDataError,
    InvalidRegistrationError,
    InvalidSelectionError,
    NotFoundError,
    UnknownRegistrationError,
)
from app.domain.jurisdiction import Jurisdiction
from app.domain.jurisdiction_code import JurisdictionCode
from app.domain.manifest import CapabilitySelection, Manifest
from app.domain.parameters.datasets import ParameterDataset
from app.domain.parameters.kind import ParameterKind
from app.domain.parameters.rounding import NO_ROUNDING
from app.domain.trace import TraceLine
from app.domain.worksheet import Worksheet

D = Decimal
EX_ON = JurisdictionCode("EX-ON")


@dataclass(frozen=True)
class Factor:
    """A made-up parameter: a multiplier."""

    value: Decimal


@dataclass(frozen=True)
class Offset:
    """A made-up parameter: an amount added."""

    value: Decimal


FACTOR = ParameterKind("factor", Factor)
OFFSET = ParameterKind("offset", Offset)

BASE = ArtifactKind("ex/base", Decimal)
SCALED = ArtifactKind("ex/scaled", Decimal)
RESULT = ArtifactKind("ex-on/result", Decimal)
EXTRA = ArtifactKind("ex/extra", Decimal)


@dataclass(frozen=True)
class StepLine(TraceLine):
    """A made-up trace line: which step ran and the value it produced."""

    step: str
    value: Decimal

    @property
    def amount(self) -> Decimal:
        return self.value


class Scale(Capability):
    """Produces `target` = `source` × the `factor` dataset's value."""

    PARAMETERS: ClassVar[Mapping[str, ParameterKind[Any]]] = {"factor": FACTOR}
    CONSUMES: ClassVar[Mapping[str, type]] = {"source": Decimal}
    PRODUCES: ClassVar[Mapping[str, type]] = {"target": Decimal}

    def __init__(self, source: Money, target: Money, factor: ParameterDataset[Factor]) -> None:
        super().__init__(source=source, target=target)
        self._source, self._target, self._factor = source, target, factor

    def compute(self, inputs: tuple[Artifact[Any], ...]) -> CapabilityResult:
        value = self._input(inputs, self._source).value * self._factor.values.value
        return CapabilityResult(
            outputs=(Artifact(self._target, value),), trace=(StepLine("scaled", value),)
        )


class Shift(Capability):
    """Produces `target` = `source` + the `offset` dataset's value."""

    PARAMETERS: ClassVar[Mapping[str, ParameterKind[Any]]] = {"offset": OFFSET}
    CONSUMES: ClassVar[Mapping[str, type]] = {"source": Decimal}
    PRODUCES: ClassVar[Mapping[str, type]] = {"target": Decimal}

    def __init__(self, source: Money, target: Money, offset: ParameterDataset[Offset]) -> None:
        super().__init__(source=source, target=target)
        self._source, self._target, self._offset = source, target, offset

    def compute(self, inputs: tuple[Artifact[Any], ...]) -> CapabilityResult:
        value = self._input(inputs, self._source).value + self._offset.values.value
        return CapabilityResult(
            outputs=(Artifact(self._target, value),), trace=(StepLine("shifted", value),)
        )


class FakeJurisdictions:
    """An in-memory JurisdictionSource holding the given jurisdictions."""

    def __init__(self, *jurisdictions: Jurisdiction) -> None:
        self._by_code = {jurisdiction.code: jurisdiction for jurisdiction in jurisdictions}

    def get_jurisdiction(self, code: JurisdictionCode) -> Jurisdiction:
        if code not in self._by_code:
            raise NotFoundError(f"no jurisdiction {code}")
        return self._by_code[code]


class FakeParameters:
    """An in-memory ParameterSource holding datasets by (family, tax year); records each request.

    Like the port's contract asks, a dataset of another kind than the one asked for is an error.
    """

    def __init__(self, *datasets: ParameterDataset[Any]) -> None:
        self._by_key = {(dataset.family, dataset.tax_year): dataset for dataset in datasets}
        self.requests: list[tuple[str, int, ParameterKind[Any]]] = []

    def get[T](self, family: str, tax_year: int, kind: ParameterKind[T]) -> ParameterDataset[T]:
        self.requests.append((family, tax_year, kind))
        if (family, tax_year) not in self._by_key:
            raise NotFoundError(f"no {family} dataset for tax year {tax_year}")
        found: ParameterDataset[Any] = self._by_key[(family, tax_year)]
        if found.kind != kind:
            raise InvalidParameterDataError(
                f"{family} for tax year {tax_year} is a {found.kind.name} dataset, not {kind.name}"
            )
        return found


def dataset[T](
    family: str, kind: ParameterKind[T], values: T, tax_year: int = 2025
) -> ParameterDataset[T]:
    return ParameterDataset(
        family=family,
        tax_year=tax_year,
        kind=kind,
        values=values,
        rounding=NO_ROUNDING,
        sources=(f"https://example.org/{family}",),
    )


def factor_data(tax_year: int = 2025) -> ParameterDataset[Factor]:
    return dataset("ex/factor", FACTOR, Factor(D("3")), tax_year)


def offset_data(tax_year: int = 2025) -> ParameterDataset[Offset]:
    return dataset("ex-on/offset", OFFSET, Offset(D("1")), tax_year)


SCALE = CapabilitySelection(
    name="ex/scale",
    params={"factor": "ex/factor"},
    consumes={"source": "ex/base"},
    produces={"target": "ex/scaled"},
)
SHIFT = CapabilitySelection(
    name="ex/shift",
    params={"offset": "ex-on/offset"},
    consumes={"source": "ex/scaled"},
    produces={"target": "ex-on/result"},
)


def manifest(
    *selections: CapabilitySelection,
    inputs: frozenset[str] = frozenset({"ex/base"}),
    outputs: frozenset[str] = frozenset({"ex-on/result"}),
    version: int = 1,
    valid_from_tax_year: int = 2025,
) -> Manifest:
    return Manifest(
        jurisdiction=EX_ON,
        version=version,
        valid_from_tax_year=valid_from_tax_year,
        capabilities=selections or (SHIFT, SCALE),  # authored out of order on purpose
        inputs=inputs,
        outputs=outputs,
    )


def capability_registry() -> CapabilityRegistry:
    registry = CapabilityRegistry()
    registry.register("ex/scale", Scale)
    registry.register("ex/shift", Shift)
    return registry


def artifact_registry() -> ArtifactRegistry:
    registry = ArtifactRegistry()
    for kind in (BASE, SCALED, RESULT, EXTRA):
        registry.register(kind.identifier, kind)
    return registry


def service(
    *manifests: Manifest,
    parameters: ParameterSource | None = None,
    capabilities: CapabilityRegistry | None = None,
    artifacts: ArtifactRegistry | None = None,
) -> TaxComputationService:
    jurisdictions: JurisdictionSource = FakeJurisdictions(
        Jurisdiction(code=EX_ON, manifests=manifests or (manifest(),))
    )
    return TaxComputationService(
        jurisdictions,
        parameters if parameters is not None else FakeParameters(factor_data(), offset_data()),
        capabilities if capabilities is not None else capability_registry(),
        artifacts if artifacts is not None else artifact_registry(),
    )


def test_computes_a_manifest_end_to_end() -> None:
    worksheet = service().compute(EX_ON, 2025, Artifact(BASE, D("5")))

    assert_type(worksheet, Worksheet)
    assert worksheet.get(SCALED).value == D("15")
    assert worksheet.get(RESULT).value == D("16")
    assert isinstance(worksheet.producer_of(SCALED), Scale)
    assert isinstance(worksheet.producer_of(RESULT), Shift)
    assert worksheet.producer_of(BASE) is None
    assert worksheet.trace == (StepLine("scaled", D("15")), StepLine("shifted", D("16")))


def test_composes_the_manifests_selections_in_contract_order() -> None:
    composition = service().compose(EX_ON, 2025)

    assert_type(composition, Composition)
    assert [type(capability) for capability in composition.order] == [Scale, Shift]
    scale, shift = composition.order
    assert scale.consumes == frozenset({BASE}) and scale.produces == frozenset({SCALED})
    assert shift.consumes == frozenset({SCALED}) and shift.produces == frozenset({RESULT})


def test_compose_is_deterministic() -> None:
    computation = service()

    first = computation.compose(EX_ON, 2025).order
    second = computation.compose(EX_ON, 2025).order

    def shape(order: tuple[Capability, ...]) -> list[tuple[type, frozenset[Any], frozenset[Any]]]:
        return [(type(c), c.consumes, c.produces) for c in order]

    assert shape(first) == shape(second)


def test_the_composition_takes_and_returns_the_manifests_inputs_and_outputs() -> None:
    composition = service().compose(EX_ON, 2025)

    with pytest.raises(InvalidCompositionError, match="missing input 'base'"):
        composition.compute()
    with pytest.raises(InvalidCompositionError, match="'scaled' is not an input"):
        composition.compute(Artifact(BASE, D("5")), Artifact(SCALED, D("1")))


def test_uses_the_manifest_for_the_tax_year_and_that_years_datasets() -> None:
    later = manifest(SCALE, outputs=frozenset({"ex/scaled"}), version=2, valid_from_tax_year=2027)
    parameters = FakeParameters(factor_data(2026), offset_data(2026), factor_data(2027))

    computation = service(manifest(), later, parameters=parameters)

    assert [type(c) for c in computation.compose(EX_ON, 2026).order] == [Scale, Shift]
    assert [type(c) for c in computation.compose(EX_ON, 2027).order] == [Scale]
    assert ("ex/factor", 2026, FACTOR) in parameters.requests
    assert ("ex-on/offset", 2026, OFFSET) in parameters.requests
    assert all(year != 2025 for _family, year, _kind in parameters.requests)


def test_asks_for_each_dataset_with_its_slots_kind() -> None:
    parameters = FakeParameters(factor_data(), offset_data())

    service(parameters=parameters).compose(EX_ON, 2025)

    assert sorted(parameters.requests, key=lambda request: request[0]) == [
        ("ex-on/offset", 2025, OFFSET),
        ("ex/factor", 2025, FACTOR),
    ]


def test_resolves_through_the_registries_it_was_given_not_the_shared_ones() -> None:
    assert "ex/scale" not in CapabilityRegistry.shared().identifiers()
    assert "ex/base" not in ArtifactRegistry.shared().identifiers()

    assert len(service().compose(EX_ON, 2025).order) == 2


def test_an_unknown_jurisdiction_is_not_found() -> None:
    with pytest.raises(NotFoundError, match="EX-ZZ"):
        service().compose(JurisdictionCode("EX-ZZ"), 2025)


def test_a_tax_year_before_every_manifest_is_not_found() -> None:
    with pytest.raises(NotFoundError, match="2024"):
        service().compose(EX_ON, 2024)


def test_an_unknown_capability_name_is_an_unknown_registration() -> None:
    unknown = CapabilitySelection(
        name="ex/nowhere",
        params={},
        consumes={"source": "ex/base"},
        produces={"target": "ex/scaled"},
    )

    with pytest.raises(UnknownRegistrationError, match="'ex/nowhere'"):
        service(manifest(unknown, SHIFT)).compose(EX_ON, 2025)


@pytest.mark.parametrize(
    "selections",
    [
        pytest.param(
            (
                CapabilitySelection(
                    name="ex/scale",
                    params={"factor": "ex/factor"},
                    consumes={"source": "ex/nowhere"},
                    produces={"target": "ex/scaled"},
                ),
                SHIFT,
            ),
            id="consumed",
        ),
        pytest.param(
            (
                SCALE,
                CapabilitySelection(
                    name="ex/shift",
                    params={"offset": "ex-on/offset"},
                    consumes={"source": "ex/scaled"},
                    produces={"target": "ex/nowhere"},
                ),
            ),
            id="produced",
        ),
    ],
)
def test_an_unknown_artifact_identifier_in_a_selection_is_an_unknown_registration(
    selections: tuple[CapabilitySelection, ...],
) -> None:
    with pytest.raises(UnknownRegistrationError, match="'ex/nowhere'"):
        service(manifest(*selections)).compose(EX_ON, 2025)


@pytest.mark.parametrize(
    ("inputs", "outputs"),
    [
        pytest.param(frozenset({"ex/nowhere"}), frozenset({"ex-on/result"}), id="input"),
        pytest.param(frozenset({"ex/base"}), frozenset({"ex/nowhere"}), id="output"),
    ],
)
def test_an_unknown_input_or_output_identifier_is_an_unknown_registration(
    inputs: frozenset[str], outputs: frozenset[str]
) -> None:
    with pytest.raises(UnknownRegistrationError, match="'ex/nowhere'"):
        service(manifest(inputs=inputs, outputs=outputs)).compose(EX_ON, 2025)


def test_a_missing_dataset_is_not_found() -> None:
    parameters = FakeParameters(factor_data())

    with pytest.raises(NotFoundError, match="ex-on/offset"):
        service(parameters=parameters).compose(EX_ON, 2025)


def test_a_dataset_of_the_wrong_kind_is_the_parameter_sources_error() -> None:
    wrong = dataset("ex/factor", OFFSET, Offset(D("3")))
    parameters = FakeParameters(wrong, offset_data())

    with pytest.raises(InvalidParameterDataError, match="ex/factor"):
        service(parameters=parameters).compose(EX_ON, 2025)


@pytest.mark.parametrize(
    ("params", "slot"),
    [
        pytest.param({"factor": "ex/factor", "bonus": "ex/bonus"}, "bonus", id="undeclared-key"),
        pytest.param({"factor": "ex/factor", "source": "ex/base"}, "source", id="artifact-slot"),
    ],
)
def test_a_params_key_that_is_not_a_parameter_slot_is_an_invalid_selection(
    params: dict[str, str], slot: str
) -> None:
    misfilled = CapabilitySelection(
        name="ex/scale",
        params=params,
        consumes={"source": "ex/base"},
        produces={"target": "ex/scaled"},
    )
    parameters = FakeParameters(factor_data(), offset_data())

    with pytest.raises(InvalidSelectionError, match=repr(slot)):
        service(manifest(misfilled, SHIFT), parameters=parameters).compose(EX_ON, 2025)
    assert all(family != params[slot] for family, _year, _kind in parameters.requests)


def test_a_selection_filling_the_wrong_slots_is_an_invalid_selection() -> None:
    misfilled = CapabilitySelection(
        name="ex/scale",
        params={"factor": "ex/factor"},
        consumes={"input": "ex/base"},
        produces={"target": "ex/scaled"},
    )

    with pytest.raises(InvalidSelectionError, match="'input'"):
        service(manifest(misfilled, SHIFT)).compose(EX_ON, 2025)


@pytest.mark.parametrize(
    ("inputs", "outputs", "message"),
    [
        pytest.param(
            frozenset({"ex/base", "ex/scaled"}),
            frozenset({"ex-on/result"}),
            "input 'scaled' is also produced by Scale",
            id="input-also-produced",
        ),
        pytest.param(
            frozenset({"ex/base"}),
            frozenset({"ex/scaled"}),
            "orphan output 'result'",
            id="undeclared-output",
        ),
        pytest.param(
            frozenset({"ex/base", "ex/extra"}),
            frozenset({"ex-on/result"}),
            "input 'extra' is consumed by nothing",
            id="unused-input",
        ),
        pytest.param(
            frozenset({"ex/base"}),
            frozenset({"ex-on/result", "ex/extra"}),
            "declared output 'extra' is produced by nothing",
            id="unproduced-output",
        ),
    ],
)
def test_inputs_or_outputs_the_composition_rejects_are_an_invalid_composition(
    inputs: frozenset[str], outputs: frozenset[str], message: str
) -> None:
    with pytest.raises(InvalidCompositionError, match=message):
        service(manifest(inputs=inputs, outputs=outputs)).compose(EX_ON, 2025)


def test_an_identifier_registered_as_something_other_than_a_kind_is_an_invalid_registration() -> (
    None
):
    artifacts = artifact_registry()
    artifacts.register("ex/stray", object())

    with pytest.raises(InvalidRegistrationError, match="'ex/stray'.*not as an artifact kind"):
        service(
            manifest(outputs=frozenset({"ex-on/result", "ex/stray"})), artifacts=artifacts
        ).compose(EX_ON, 2025)


def test_an_identifier_in_a_selection_registered_as_something_other_than_a_kind_is_invalid() -> (
    None
):
    artifacts = artifact_registry()
    artifacts.register("ex/stray", object())
    stray = CapabilitySelection(
        name="ex/scale",
        params={"factor": "ex/factor"},
        consumes={"source": "ex/stray"},
        produces={"target": "ex/scaled"},
    )

    with pytest.raises(InvalidRegistrationError, match="'ex/stray'.*not as an artifact kind"):
        service(manifest(stray, SHIFT), artifacts=artifacts).compose(EX_ON, 2025)


# --- list slots: a consumed slot filled with a list of identifiers ------------------------------
#
# The list-slot class is defined inside a cached factory, so a class definition the base rejects
# fails the tests that use it rather than the collection of this whole module.

PART_ONE = ArtifactKind("ex/part_one", Decimal)
PART_TWO = ArtifactKind("ex/part_two", Decimal)
PART_THREE = ArtifactKind("ex/part_three", Decimal)


@dataclass(frozen=True)
class PartsLine(TraceLine):
    """A made-up trace line: the identifiers of the parts added, in order, and their total."""

    parts: tuple[str, ...]
    total: Decimal

    @property
    def amount(self) -> Decimal:
        return self.total


@cache
def total_class() -> Any:
    class Total(Capability):
        """Produces `total` = the sum of its `parts`, each read with `_input`, in their order."""

        CONSUMES = {"parts": list[Decimal]}
        PRODUCES = {"total": Decimal}

        def __init__(self, parts: tuple[Money, ...], total: Money) -> None:
            super().__init__(parts=parts, total=total)
            self.parts, self.total = parts, total

        def compute(self, inputs: tuple[Artifact[Any], ...]) -> CapabilityResult:
            values = [self._input(inputs, kind).value for kind in self.parts]
            value = sum(values, D(0))
            line = PartsLine(tuple(kind.identifier for kind in self.parts), value)
            return CapabilityResult(outputs=(Artifact(self.total, value),), trace=(line,))

    return Total


def list_slot_manifest(parts: Any, *producers: CapabilitySelection) -> Manifest:
    """Three made-up producers of parts and a Total over `parts` producing `ex-on/result`."""
    to_one = CapabilitySelection(
        name="ex/scale",
        params={"factor": "ex/factor"},
        consumes={"source": "ex/base"},
        produces={"target": "ex/part_one"},
    )
    to_two = CapabilitySelection(
        name="ex/shift",
        params={"offset": "ex-on/offset"},
        consumes={"source": "ex/base"},
        produces={"target": "ex/part_two"},
    )
    to_three = CapabilitySelection(  # chained after to_one, so the total waits for a chain
        name="ex/shift",
        params={"offset": "ex-on/offset"},
        consumes={"source": "ex/part_one"},
        produces={"target": "ex/part_three"},
    )
    total = CapabilitySelection(
        name="ex/total_up",
        params={},
        consumes={"parts": parts},
        produces={"total": "ex-on/result"},
    )
    return manifest(total, *(producers or (to_three, to_two, to_one)))


def list_slot_service(*manifests: Manifest) -> TaxComputationService:
    capabilities = capability_registry()
    capabilities.register("ex/total_up", total_class())
    artifacts = artifact_registry()
    for kind in (PART_ONE, PART_TWO, PART_THREE):
        artifacts.register(kind.identifier, kind)
    return service(*manifests, capabilities=capabilities, artifacts=artifacts)


def test_a_list_slot_receives_its_kinds_in_manifest_order() -> None:
    parts = ("ex/part_two", "ex/part_three", "ex/part_one")
    total_cls = total_class()

    composition = list_slot_service(list_slot_manifest(parts)).compose(EX_ON, 2025)

    total = composition.order[-1]
    assert isinstance(total, total_cls)
    assert total.parts == (PART_TWO, PART_THREE, PART_ONE)
    assert total.consumes == frozenset({PART_ONE, PART_TWO, PART_THREE})
    assert total.produces == frozenset({RESULT})


def test_the_list_slot_capability_runs_after_all_three_producers() -> None:
    parts = ("ex/part_two", "ex/part_three", "ex/part_one")

    composition = list_slot_service(list_slot_manifest(parts)).compose(EX_ON, 2025)

    assert [type(capability) for capability in composition.order] == [
        Scale,
        Shift,
        Shift,
        total_class(),
    ]


def test_computes_a_list_slot_end_to_end() -> None:
    parts = ("ex/part_two", "ex/part_three", "ex/part_one")

    worksheet = list_slot_service(list_slot_manifest(parts)).compute(
        EX_ON, 2025, Artifact(BASE, D("5"))
    )

    # part_one = 5 × 3 = 15; part_two = 5 + 1 = 6; part_three = 15 + 1 = 16.
    assert worksheet.get(PART_ONE).value == D("15")
    assert worksheet.get(PART_TWO).value == D("6")
    assert worksheet.get(PART_THREE).value == D("16")
    assert worksheet.get(RESULT).value == D("37")
    assert isinstance(worksheet.producer_of(RESULT), total_class())
    assert worksheet.trace[-1] == PartsLine(parts, D("37"))


def test_an_unknown_identifier_in_a_list_is_an_unknown_registration() -> None:
    parts = ("ex/part_two", "ex/nowhere", "ex/part_one")

    with pytest.raises(UnknownRegistrationError, match="'ex/nowhere'"):
        list_slot_service(list_slot_manifest(parts)).compose(EX_ON, 2025)


def test_a_listed_kind_nothing_produces_is_an_invalid_composition() -> None:
    parts = ("ex/part_two", "ex/extra", "ex/part_one")

    with pytest.raises(InvalidCompositionError, match="no producer for 'extra'"):
        list_slot_service(list_slot_manifest(parts)).compose(EX_ON, 2025)


def test_a_kind_listed_twice_is_an_invalid_selection() -> None:
    parts = ("ex/part_two", "ex/part_three", "ex/part_one", "ex/part_two")

    with pytest.raises(InvalidSelectionError, match="'parts'"):
        list_slot_service(list_slot_manifest(parts)).compose(EX_ON, 2025)


def test_a_single_identifier_for_a_list_slot_is_an_invalid_selection() -> None:
    to_one = CapabilitySelection(
        name="ex/scale",
        params={"factor": "ex/factor"},
        consumes={"source": "ex/base"},
        produces={"target": "ex/part_one"},
    )

    with pytest.raises(InvalidSelectionError, match="'parts'"):
        list_slot_service(list_slot_manifest("ex/part_one", to_one)).compose(EX_ON, 2025)


def test_a_list_for_a_single_slot_is_an_invalid_selection() -> None:
    to_one = CapabilitySelection(
        name="ex/scale",
        params={"factor": "ex/factor"},
        consumes={"source": ("ex/base",)},
        produces={"target": "ex/part_one"},
    )

    with pytest.raises(InvalidSelectionError, match="'source'"):
        list_slot_service(list_slot_manifest(("ex/part_one",), to_one)).compose(EX_ON, 2025)


# --- core/sum: the generic sum over a list slot, wired by a made-up manifest -------------------
#
# `Sum` is imported inside a cached factory, so its absence fails the tests that use it rather
# than the collection of this whole module. It is registered in a private registry under its
# shared identifier, `core/sum`.


@cache
def sum_class() -> Any:
    from app.domain.capabilities.sum import Sum

    return Sum


def sum_manifest(parts: tuple[str, ...]) -> Manifest:
    """The three made-up producers of parts and `core/sum` over `parts` producing `ex-on/result`."""
    to_one = CapabilitySelection(
        name="ex/scale",
        params={"factor": "ex/factor"},
        consumes={"source": "ex/base"},
        produces={"target": "ex/part_one"},
    )
    to_two = CapabilitySelection(
        name="ex/shift",
        params={"offset": "ex-on/offset"},
        consumes={"source": "ex/base"},
        produces={"target": "ex/part_two"},
    )
    to_three = CapabilitySelection(
        name="ex/shift",
        params={"offset": "ex-on/offset"},
        consumes={"source": "ex/part_one"},
        produces={"target": "ex/part_three"},
    )
    total = CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": parts},
        produces={"output": "ex-on/result"},
    )
    return manifest(total, to_three, to_two, to_one)


def sum_service(*manifests: Manifest) -> TaxComputationService:
    capabilities = capability_registry()
    capabilities.register("core/sum", sum_class())
    artifacts = artifact_registry()
    for kind in (PART_ONE, PART_TWO, PART_THREE):
        artifacts.register(kind.identifier, kind)
    return service(*manifests, capabilities=capabilities, artifacts=artifacts)


def test_computes_core_sum_end_to_end() -> None:
    from app.domain.trace import SumLine

    parts = ("ex/part_two", "ex/part_three", "ex/part_one")

    worksheet = sum_service(sum_manifest(parts)).compute(EX_ON, 2025, Artifact(BASE, D("5")))

    # part_one = 5 × 3 = 15; part_two = 5 + 1 = 6; part_three = 15 + 1 = 16.
    assert worksheet.get(RESULT).value == D("37")
    assert isinstance(worksheet.producer_of(RESULT), sum_class())
    assert worksheet.trace[-1] == SumLine(
        RESULT, ((PART_TWO, D("6")), (PART_THREE, D("16")), (PART_ONE, D("15"))), D("37")
    )
    assert [type(line) for line in worksheet.trace].count(SumLine) == 1


def test_core_sum_runs_after_all_its_parts() -> None:
    parts = ("ex/part_two", "ex/part_three", "ex/part_one")

    composition = sum_service(sum_manifest(parts)).compose(EX_ON, 2025)

    assert type(composition.order[-1]) is sum_class()
    assert composition.order[-1].consumes == frozenset({PART_ONE, PART_TWO, PART_THREE})


# --- core/apply_rate: base × a rate dataset's rate, wired by a made-up manifest ----------------
#
# `ApplyRate` is imported inside a cached factory, like `Sum` above, so its absence fails only
# the tests that use it. It is registered in a private registry under its shared identifier,
# `core/apply_rate`, and reads a made-up `rate` dataset that rounds half-up to the cent.


@cache
def apply_rate_class() -> Any:
    from app.domain.capabilities.apply_rate import ApplyRate

    return ApplyRate


def portion_rate_data(tax_year: int = 2025) -> ParameterDataset[Any]:
    from app.domain.parameters.rate import RATE, Rate
    from app.domain.parameters.rounding import RoundingMode, RoundTo

    return ParameterDataset(
        family="ex/portion_rate",
        tax_year=tax_year,
        kind=RATE,
        values=Rate(D("0.5")),
        rounding=RoundTo(D("0.01"), RoundingMode.HALF_UP),
        sources=("https://example.org/ex/portion_rate",),
    )


APPLY_RATE = CapabilitySelection(
    name="core/apply_rate",
    params={"rate": "ex/portion_rate"},
    consumes={"base": "ex/scaled"},
    produces={"output": "ex-on/result"},
)


def apply_rate_service() -> tuple[TaxComputationService, FakeParameters]:
    capabilities = capability_registry()
    capabilities.register("core/apply_rate", apply_rate_class())
    parameters = FakeParameters(factor_data(), offset_data(), portion_rate_data())
    built = service(
        manifest(APPLY_RATE, SCALE),  # authored out of order on purpose
        parameters=parameters,
        capabilities=capabilities,
    )
    return built, parameters


def test_computes_core_apply_rate_end_to_end() -> None:
    from app.domain.parameters.rate import Rate
    from app.domain.parameters.rounding import RoundingMode, RoundTo
    from app.domain.trace import RateAppliedLine

    built, _parameters = apply_rate_service()

    worksheet = built.compute(EX_ON, 2025, Artifact(BASE, D("5.01")))

    # scaled = 5.01 × 3 = 15.03; result = 15.03 × 0.5 = 7.515, rounded half-up to 7.52.
    assert worksheet.get(SCALED).value == D("15.03")
    assert worksheet.get(RESULT).value == D("7.52")
    assert isinstance(worksheet.producer_of(RESULT), apply_rate_class())
    assert worksheet.trace[-1] == RateAppliedLine(
        RESULT,
        SCALED,
        D("15.03"),
        Rate(D("0.5")),
        RoundTo(D("0.01"), RoundingMode.HALF_UP),
        D("7.52"),
    )
    assert [type(line) for line in worksheet.trace].count(RateAppliedLine) == 1


def test_core_apply_rate_runs_after_its_base_is_produced() -> None:
    built, _parameters = apply_rate_service()

    composition = built.compose(EX_ON, 2025)

    assert type(composition.order[-1]) is apply_rate_class()
    assert composition.order[-1].consumes == frozenset({SCALED})


def test_core_apply_rate_asks_for_its_dataset_as_a_rate() -> None:
    from app.domain.parameters.rate import RATE

    built, parameters = apply_rate_service()

    built.compose(EX_ON, 2025)

    assert ("ex/portion_rate", 2025, RATE) in parameters.requests


# --- core/subtract: amount less another artifact, wired by a made-up manifest -----------------
#
# `Subtract` is imported inside a cached factory, like `Sum` above, so its absence fails only the
# tests that use it. It is registered in a private registry under its shared identifier,
# `core/subtract`, and takes one of the manifest's inputs and one produced artifact.


@cache
def subtract_class() -> Any:
    from app.domain.capabilities.subtract import Subtract

    return Subtract


def subtract_service(amount: str, less: str) -> TaxComputationService:
    """`ex/scale` (base × 3) and `core/subtract` producing `ex-on/result` = amount − less."""
    subtract = CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": amount, "less": less},
        produces={"output": "ex-on/result"},
    )
    capabilities = capability_registry()
    capabilities.register("core/subtract", subtract_class())
    return service(manifest(subtract, SCALE), capabilities=capabilities)  # out of order on purpose


def test_computes_core_subtract_end_to_end() -> None:
    from app.domain.trace import SubtractedLine

    worksheet = subtract_service("ex/scaled", "ex/base").compute(
        EX_ON, 2025, Artifact(BASE, D("5.01"))
    )

    # scaled = 5.01 × 3 = 15.03; result = 15.03 − 5.01 = 10.02.
    assert worksheet.get(RESULT).value == D("10.02")
    assert isinstance(worksheet.producer_of(RESULT), subtract_class())
    assert worksheet.trace[-1] == SubtractedLine(
        RESULT, SCALED, D("15.03"), BASE, D("5.01"), D("10.02")
    )
    assert [type(line) for line in worksheet.trace].count(SubtractedLine) == 1


def test_core_subtract_produces_a_negative_result_end_to_end() -> None:
    from app.domain.trace import SubtractedLine

    worksheet = subtract_service("ex/base", "ex/scaled").compute(
        EX_ON, 2025, Artifact(BASE, D("5.01"))
    )

    # result = 5.01 − 15.03 = −10.02, not floored at zero.
    assert worksheet.get(RESULT).value == D("-10.02")
    assert worksheet.trace[-1] == SubtractedLine(
        RESULT, BASE, D("5.01"), SCALED, D("15.03"), D("-10.02")
    )


def test_core_subtract_runs_after_what_it_consumes_is_produced() -> None:
    composition = subtract_service("ex/scaled", "ex/base").compose(EX_ON, 2025)

    assert type(composition.order[-1]) is subtract_class()
    assert composition.order[-1].consumes == frozenset({SCALED, BASE})


# --- core/subtract_not_below_zero: amount less another, floored at zero, by a made-up manifest -
#
# Like `Subtract` above, `SubtractNotBelowZero` is imported inside a cached factory so its absence
# fails only the tests that use it, and is registered in a private registry under its shared
# identifier, `core/subtract_not_below_zero`.


@cache
def subtract_not_below_zero_class() -> Any:
    from app.domain.capabilities.subtract_not_below_zero import SubtractNotBelowZero

    return SubtractNotBelowZero


def subtract_not_below_zero_service(amount: str, less: str) -> TaxComputationService:
    """`ex/scale` (base × 3) and `core/subtract_not_below_zero` producing `ex-on/result`."""
    subtract = CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={"amount": amount, "less": less},
        produces={"output": "ex-on/result"},
    )
    capabilities = capability_registry()
    capabilities.register("core/subtract_not_below_zero", subtract_not_below_zero_class())
    return service(manifest(subtract, SCALE), capabilities=capabilities)  # out of order on purpose


def test_computes_core_subtract_not_below_zero_end_to_end() -> None:
    from app.domain.trace import SubtractedNotBelowZeroLine

    worksheet = subtract_not_below_zero_service("ex/scaled", "ex/base").compute(
        EX_ON, 2025, Artifact(BASE, D("5.01"))
    )

    # scaled = 5.01 × 3 = 15.03; result = 15.03 − 5.01 = 10.02, above zero so unchanged.
    assert worksheet.get(RESULT).value == D("10.02")
    assert isinstance(worksheet.producer_of(RESULT), subtract_not_below_zero_class())
    assert worksheet.trace[-1] == SubtractedNotBelowZeroLine(
        RESULT, SCALED, D("15.03"), BASE, D("5.01"), D("10.02")
    )
    assert [type(line) for line in worksheet.trace].count(SubtractedNotBelowZeroLine) == 1


def test_core_subtract_not_below_zero_floors_a_negative_difference_end_to_end() -> None:
    from app.domain.trace import SubtractedNotBelowZeroLine

    worksheet = subtract_not_below_zero_service("ex/base", "ex/scaled").compute(
        EX_ON, 2025, Artifact(BASE, D("5.01"))
    )

    # 5.01 − 15.03 = −10.02, floored: result = 0.
    assert worksheet.get(RESULT).value == D("0")
    assert worksheet.trace[-1] == SubtractedNotBelowZeroLine(
        RESULT, BASE, D("5.01"), SCALED, D("15.03"), D("0")
    )
    assert [type(line) for line in worksheet.trace].count(SubtractedNotBelowZeroLine) == 1


def test_core_subtract_not_below_zero_runs_after_what_it_consumes_is_produced() -> None:
    composition = subtract_not_below_zero_service("ex/scaled", "ex/base").compose(EX_ON, 2025)

    assert type(composition.order[-1]) is subtract_not_below_zero_class()
    assert composition.order[-1].consumes == frozenset({SCALED, BASE})


# --- core/credit_amount: a credit dataset's amount as a part of core/sum, by a made-up manifest -
#
# `CreditAmount` is imported inside a cached factory, like `Sum` above, so its absence fails only
# the tests that use it. It is registered in a private registry under its shared identifier,
# `core/credit_amount`; its selection fills no consumed slot, and it reads a made-up `credit`
# dataset that rounds half-up to the cent.


@cache
def credit_amount_class() -> Any:
    from app.domain.capabilities.credit_amount import CreditAmount

    return CreditAmount


def personal_credit_data(tax_year: int = 2025) -> ParameterDataset[Any]:
    from app.domain.parameters.credit import CREDIT, Credit
    from app.domain.parameters.rounding import RoundingMode, RoundTo

    return ParameterDataset(
        family="ex/personal_credit",
        tax_year=tax_year,
        kind=CREDIT,
        values=Credit(D("1000.005")),
        rounding=RoundTo(D("0.01"), RoundingMode.HALF_UP),
        sources=("https://example.org/ex/personal_credit",),
    )


CREDIT_AMOUNT = CapabilitySelection(
    name="core/credit_amount",
    params={"amount": "ex/personal_credit"},
    consumes={},
    produces={"output": "ex/part_two"},
)


def credit_amount_service() -> tuple[TaxComputationService, FakeParameters]:
    """`ex/scale` (base × 3) and `core/credit_amount` summed by `core/sum` into `ex-on/result`."""
    to_one = CapabilitySelection(
        name="ex/scale",
        params={"factor": "ex/factor"},
        consumes={"source": "ex/base"},
        produces={"target": "ex/part_one"},
    )
    total = CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ex/part_one", "ex/part_two")},
        produces={"output": "ex-on/result"},
    )
    capabilities = capability_registry()
    capabilities.register("core/sum", sum_class())
    capabilities.register("core/credit_amount", credit_amount_class())
    artifacts = artifact_registry()
    for kind in (PART_ONE, PART_TWO):
        artifacts.register(kind.identifier, kind)
    parameters = FakeParameters(factor_data(), offset_data(), personal_credit_data())
    built = service(
        manifest(total, CREDIT_AMOUNT, to_one),  # authored out of order on purpose
        parameters=parameters,
        capabilities=capabilities,
        artifacts=artifacts,
    )
    return built, parameters


def test_computes_core_credit_amount_as_a_part_of_core_sum_end_to_end() -> None:
    from app.domain.parameters.credit import Credit
    from app.domain.parameters.rounding import RoundingMode, RoundTo
    from app.domain.trace import CreditAmountLine, SumLine

    built, _parameters = credit_amount_service()

    worksheet = built.compute(EX_ON, 2025, Artifact(BASE, D("5")))

    # part_one = 5 × 3 = 15; part_two = 1000.005, rounded half-up to 1000.01; result = 1015.01.
    assert worksheet.get(PART_TWO).value == D("1000.01")
    assert isinstance(worksheet.producer_of(PART_TWO), credit_amount_class())
    assert worksheet.get(RESULT).value == D("1015.01")
    assert (
        CreditAmountLine(
            PART_TWO, Credit(D("1000.005")), RoundTo(D("0.01"), RoundingMode.HALF_UP), D("1000.01")
        )
        in worksheet.trace
    )
    assert [type(line) for line in worksheet.trace].count(CreditAmountLine) == 1
    assert worksheet.trace[-1] == SumLine(
        RESULT, ((PART_ONE, D("15")), (PART_TWO, D("1000.01"))), D("1015.01")
    )


def test_the_composition_accepts_a_selection_without_consumes() -> None:
    built, _parameters = credit_amount_service()

    composition = built.compose(EX_ON, 2025)

    (credit,) = [c for c in composition.order if type(c) is credit_amount_class()]
    assert credit.consumes == frozenset()
    assert credit.produces == frozenset({PART_TWO})
    assert type(composition.order[-1]) is sum_class()


def test_core_credit_amount_asks_for_its_dataset_as_a_credit() -> None:
    from app.domain.parameters.credit import CREDIT

    built, parameters = credit_amount_service()

    built.compose(EX_ON, 2025)

    assert ("ex/personal_credit", 2025, CREDIT) in parameters.requests


# --- core/capped_amount: the lesser of base and an amount dataset's cap, by a made-up manifest --
#
# `CappedAmount` is imported inside a cached factory, like `Sum` above, so its absence fails only
# the tests that use it. It is registered in a private registry under its shared identifier,
# `core/capped_amount`, and reads a made-up `amount` dataset that rounds half-up to the cent.


@cache
def capped_amount_class() -> Any:
    from app.domain.capabilities.capped_amount import CappedAmount

    return CappedAmount


def some_cap_data(tax_year: int = 2025) -> ParameterDataset[Any]:
    from app.domain.parameters.amount import AMOUNT, Amount
    from app.domain.parameters.rounding import RoundingMode, RoundTo

    return ParameterDataset(
        family="ex/some_cap",
        tax_year=tax_year,
        kind=AMOUNT,
        values=Amount(D("20")),
        rounding=RoundTo(D("0.01"), RoundingMode.HALF_UP),
        sources=("https://example.org/ex/some_cap",),
    )


CAPPED_AMOUNT = CapabilitySelection(
    name="core/capped_amount",
    params={"cap": "ex/some_cap"},
    consumes={"base": "ex/scaled"},
    produces={"output": "ex-on/result"},
)


def capped_amount_service() -> tuple[TaxComputationService, FakeParameters]:
    capabilities = capability_registry()
    capabilities.register("core/capped_amount", capped_amount_class())
    parameters = FakeParameters(factor_data(), offset_data(), some_cap_data())
    built = service(
        manifest(CAPPED_AMOUNT, SCALE),  # authored out of order on purpose
        parameters=parameters,
        capabilities=capabilities,
    )
    return built, parameters


def test_computes_core_capped_amount_below_the_cap_end_to_end() -> None:
    from app.domain.parameters.amount import Amount
    from app.domain.parameters.rounding import RoundingMode, RoundTo
    from app.domain.trace import CappedAmountLine

    built, _parameters = capped_amount_service()

    worksheet = built.compute(EX_ON, 2025, Artifact(BASE, D("5.005")))

    # scaled = 5.005 × 3 = 15.015; below the cap of 20, rounded half-up: result = 15.02.
    assert worksheet.get(SCALED).value == D("15.015")
    assert worksheet.get(RESULT).value == D("15.02")
    assert isinstance(worksheet.producer_of(RESULT), capped_amount_class())
    assert worksheet.trace[-1] == CappedAmountLine(
        RESULT,
        SCALED,
        D("15.015"),
        Amount(D("20")),
        RoundTo(D("0.01"), RoundingMode.HALF_UP),
        D("15.02"),
    )
    assert [type(line) for line in worksheet.trace].count(CappedAmountLine) == 1


def test_computes_core_capped_amount_above_the_cap_end_to_end() -> None:
    from app.domain.parameters.amount import Amount
    from app.domain.parameters.rounding import RoundingMode, RoundTo
    from app.domain.trace import CappedAmountLine

    built, _parameters = capped_amount_service()

    worksheet = built.compute(EX_ON, 2025, Artifact(BASE, D("10")))

    # scaled = 10 × 3 = 30; above the cap: result = 20, rounded half-up to 20.00.
    assert worksheet.get(RESULT).value == D("20")
    assert str(worksheet.get(RESULT).value) == "20.00"
    assert worksheet.trace[-1] == CappedAmountLine(
        RESULT,
        SCALED,
        D("30"),
        Amount(D("20")),
        RoundTo(D("0.01"), RoundingMode.HALF_UP),
        D("20.00"),
    )


def test_core_capped_amount_runs_after_its_base_is_produced() -> None:
    built, _parameters = capped_amount_service()

    composition = built.compose(EX_ON, 2025)

    assert type(composition.order[-1]) is capped_amount_class()
    assert composition.order[-1].consumes == frozenset({SCALED})


def test_core_capped_amount_asks_for_its_dataset_as_an_amount() -> None:
    from app.domain.parameters.amount import AMOUNT

    built, parameters = capped_amount_service()

    built.compose(EX_ON, 2025)

    assert ("ex/some_cap", 2025, AMOUNT) in parameters.requests
