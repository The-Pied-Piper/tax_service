"""Unit tests for CapabilityBuilder: one capability built from a manifest selection.

The builder is given the selection, the capability class, the resolved datasets (parameter slot ->
dataset) and the resolved kinds (artifact slot -> kind). It checks the selection fills exactly the
class's slots, each in its own section, with datasets of the slots' kinds, then calls the
constructor by keyword. Value types of kinds are the constructor's check. Names are made up.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, ClassVar, assert_type

import pytest

from app.domain.artifact import Artifact, ArtifactKind, Money
from app.domain.capability import Capability, CapabilityResult
from app.domain.capability_builder import CapabilityBuilder
from app.domain.errors import DomainError, InvalidCapabilityError, InvalidSelectionError
from app.domain.manifest import CapabilitySelection
from app.domain.parameters.datasets import ParameterDataset
from app.domain.parameters.kind import ParameterKind
from app.domain.parameters.rounding import NO_ROUNDING
from app.domain.trace import TraceLine

D = Decimal


@dataclass(frozen=True)
class Factor:
    """A made-up parameter: a multiplier."""

    value: Decimal


@dataclass(frozen=True)
class Offset:
    """Another made-up parameter, of another kind."""

    value: Decimal


FACTOR = ParameterKind("factor", Factor)
OFFSET = ParameterKind("offset", Offset)

SOURCE = ArtifactKind("ex/source", Decimal)
TARGET = ArtifactKind("ex/target", Decimal)


@dataclass(frozen=True)
class ScaledLine(TraceLine):
    """A made-up trace line: the scaled value."""

    scaled: Decimal

    @property
    def amount(self) -> Decimal:
        return self.scaled


class Scale(Capability):
    """Produces `target` = `source` × the `factor` dataset's value."""

    PARAMETERS: ClassVar[Mapping[str, ParameterKind[Any]]] = {"factor": FACTOR}
    CONSUMES: ClassVar[Mapping[str, type]] = {"source": Decimal}
    PRODUCES: ClassVar[Mapping[str, type]] = {"target": Decimal}

    def __init__(self, *, source: Money, target: Money, factor: ParameterDataset[Factor]) -> None:
        super().__init__(source=source, target=target)
        self.source = source
        self.target = target
        self.factor = factor

    def compute(self, inputs: tuple[Artifact[Any], ...]) -> CapabilityResult:
        value = self._input(inputs, self.source).value * self.factor.values.value
        return CapabilityResult(outputs=(Artifact(self.target, value),), trace=(ScaledLine(value),))


FACTOR_DATA = ParameterDataset(
    family="ex/factor",
    tax_year=2025,
    kind=FACTOR,
    values=Factor(D("3")),
    rounding=NO_ROUNDING,
    sources=("https://example.org/ex/factor",),
)
OFFSET_DATA = ParameterDataset(
    family="ex/offset",
    tax_year=2025,
    kind=OFFSET,
    values=Offset(D("1")),
    rounding=NO_ROUNDING,
    sources=("https://example.org/ex/offset",),
)


def selection(
    params: Mapping[str, str] | None = None,
    consumes: Mapping[str, str] | None = None,
    produces: Mapping[str, str] | None = None,
) -> CapabilitySelection:
    return CapabilitySelection(
        name="ex/scale",
        params={"factor": "ex/factor"} if params is None else params,
        consumes={"source": "ex/source"} if consumes is None else consumes,
        produces={"target": "ex/target"} if produces is None else produces,
    )


def datasets(**overrides: ParameterDataset[Any]) -> dict[str, ParameterDataset[Any]]:
    return {"factor": FACTOR_DATA, **overrides}


def kinds(**overrides: ArtifactKind[Any]) -> dict[str, ArtifactKind[Any]]:
    return {"source": SOURCE, "target": TARGET, **overrides}


def build(
    chosen: CapabilitySelection,
    given_datasets: Mapping[str, ParameterDataset[Any]] | None = None,
    given_kinds: Mapping[str, ArtifactKind[Any]] | None = None,
) -> Capability:
    return CapabilityBuilder().build(
        chosen,
        Scale,
        datasets() if given_datasets is None else given_datasets,
        kinds() if given_kinds is None else given_kinds,
    )


def assert_names(excinfo: pytest.ExceptionInfo[InvalidSelectionError], slot: str) -> None:
    message = str(excinfo.value)
    assert "ex/scale (produces " in message, message
    assert repr(slot) in message, message


def test_builds_an_instance_of_the_class_wired_with_the_given_kinds() -> None:
    built = CapabilityBuilder().build(selection(), Scale, datasets(), kinds())

    assert_type(built, Capability)
    assert isinstance(built, Scale)
    assert built.consumes == frozenset({SOURCE})
    assert built.produces == frozenset({TARGET})
    assert built.factor is FACTOR_DATA


def test_the_built_capability_computes_with_its_dataset() -> None:
    built = build(selection())

    result = built.compute((Artifact(SOURCE, D("5")),))

    assert result.outputs == (Artifact(TARGET, D("15")),)


def test_invalid_selection_error_is_a_domain_error() -> None:
    assert issubclass(InvalidSelectionError, DomainError)


def test_rejects_a_params_key_that_is_not_a_parameter_slot() -> None:
    with pytest.raises(InvalidSelectionError) as excinfo:
        build(selection(params={"factor": "ex/factor", "bonus": "ex/bonus"}))

    assert_names(excinfo, "bonus")


def test_rejects_an_artifact_slot_given_as_a_parameter() -> None:
    with pytest.raises(InvalidSelectionError) as excinfo:
        build(selection(params={"factor": "ex/factor", "source": "ex/source"}))

    assert_names(excinfo, "source")


def test_rejects_a_parameter_slot_the_selection_does_not_fill() -> None:
    with pytest.raises(InvalidSelectionError) as excinfo:
        build(selection(params={}), given_datasets={})

    assert_names(excinfo, "factor")


def test_rejects_a_dataset_of_another_kind_than_the_slots() -> None:
    with pytest.raises(InvalidSelectionError) as excinfo:
        build(selection(), given_datasets=datasets(factor=OFFSET_DATA))

    assert_names(excinfo, "factor")
    assert "offset" in str(excinfo.value)


def test_rejects_a_consumes_key_that_is_not_a_consumed_slot() -> None:
    with pytest.raises(InvalidSelectionError) as excinfo:
        build(
            selection(consumes={"source": "ex/source", "extra": "ex/extra"}),
            given_kinds=kinds(extra=ArtifactKind("ex/extra", Decimal)),
        )

    assert_names(excinfo, "extra")


def test_rejects_a_produces_key_that_is_not_a_produced_slot() -> None:
    with pytest.raises(InvalidSelectionError) as excinfo:
        build(
            selection(produces={"target": "ex/target", "extra": "ex/extra"}),
            given_kinds=kinds(extra=ArtifactKind("ex/extra", Decimal)),
        )

    assert_names(excinfo, "extra")


def test_rejects_a_produced_slot_given_under_consumes() -> None:
    with pytest.raises(InvalidSelectionError) as excinfo:
        build(selection(consumes={"source": "ex/source", "target": "ex/target"}, produces={}))

    assert_names(excinfo, "target")


def test_rejects_a_consumed_slot_given_under_produces() -> None:
    with pytest.raises(InvalidSelectionError) as excinfo:
        build(selection(consumes={}, produces={"source": "ex/source", "target": "ex/target"}))

    assert_names(excinfo, "source")


def test_rejects_a_parameter_slot_given_as_an_artifact_slot() -> None:
    with pytest.raises(InvalidSelectionError) as excinfo:
        build(
            selection(consumes={"source": "ex/source", "factor": "ex/factor"}),
            given_kinds=kinds(factor=ArtifactKind("ex/factor", Decimal)),
        )

    assert_names(excinfo, "factor")


@pytest.mark.parametrize(
    ("consumes", "produces", "slot"),
    [
        pytest.param({}, {"target": "ex/target"}, "source", id="consumed-slot-missing"),
        pytest.param({"source": "ex/source"}, {}, "target", id="produced-slot-missing"),
    ],
)
def test_rejects_an_artifact_slot_the_selection_does_not_fill(
    consumes: dict[str, str], produces: dict[str, str], slot: str
) -> None:
    with pytest.raises(InvalidSelectionError) as excinfo:
        build(selection(consumes=consumes, produces=produces))

    assert_names(excinfo, slot)


def test_rejects_a_parameter_slot_without_a_resolved_dataset() -> None:
    with pytest.raises(InvalidSelectionError) as excinfo:
        build(selection(), given_datasets={})

    assert_names(excinfo, "factor")


@pytest.mark.parametrize("slot", ["source", "target"])
def test_rejects_an_artifact_slot_without_a_resolved_kind(slot: str) -> None:
    resolved = {k: v for k, v in kinds().items() if k != slot}

    with pytest.raises(InvalidSelectionError) as excinfo:
        build(selection(), given_kinds=resolved)

    assert_names(excinfo, slot)


def test_a_kind_of_the_wrong_value_type_is_the_constructors_error() -> None:
    wrong = ArtifactKind("ex/target", int)

    with pytest.raises(InvalidCapabilityError, match=re.escape("'target'")):
        build(selection(), given_kinds=kinds(target=wrong))


def test_a_class_without_parameter_slots_builds_from_an_empty_params() -> None:
    class Copy(Capability):
        CONSUMES: ClassVar[Mapping[str, type]] = {"source": Decimal}
        PRODUCES: ClassVar[Mapping[str, type]] = {"target": Decimal}

        def __init__(self, source: Money, target: Money) -> None:
            super().__init__(source=source, target=target)

        def compute(self, inputs: tuple[Artifact[Any], ...]) -> CapabilityResult:
            raise NotImplementedError

    chosen = CapabilitySelection(
        name="ex/copy",
        params={},
        consumes={"source": "ex/source"},
        produces={"target": "ex/target"},
    )

    built = CapabilityBuilder().build(chosen, Copy, {}, kinds())

    assert isinstance(built, Copy)
    assert built.produces == frozenset({TARGET})


def test_identifies_the_selection_by_name_and_produced_identifiers() -> None:
    with pytest.raises(InvalidSelectionError, match=re.escape("ex/scale (produces ex/target)")):
        build(selection(params={}), given_datasets={})


def test_rejects_a_dataset_of_another_family_than_the_selection_names() -> None:
    other = ParameterDataset(
        family="ex/other_factor",
        tax_year=2025,
        kind=FACTOR,
        values=Factor(D("2")),
        rounding=NO_ROUNDING,
        sources=("https://example.org/ex/other_factor",),
    )

    with pytest.raises(InvalidSelectionError) as excinfo:
        build(selection(), given_datasets=datasets(factor=other))

    assert_names(excinfo, "factor")
    assert "ex/other_factor" in str(excinfo.value)


def test_rejects_a_kind_of_another_identifier_than_the_selection_names() -> None:
    with pytest.raises(InvalidSelectionError) as excinfo:
        build(selection(), given_kinds=kinds(source=ArtifactKind("ex/elsewhere", Decimal)))

    assert_names(excinfo, "source")
    assert "ex/elsewhere" in str(excinfo.value)


def test_rejects_a_resolved_dataset_for_a_key_that_is_not_a_parameter_slot() -> None:
    with pytest.raises(InvalidSelectionError) as excinfo:
        build(selection(), given_datasets=datasets(bonus=FACTOR_DATA))

    assert_names(excinfo, "bonus")


def test_rejects_a_resolved_kind_for_a_key_that_is_not_an_artifact_slot() -> None:
    with pytest.raises(InvalidSelectionError) as excinfo:
        build(selection(), given_kinds=kinds(extra=ArtifactKind("ex/extra", Decimal)))

    assert_names(excinfo, "extra")
