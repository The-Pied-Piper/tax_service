"""Unit tests for the Capability base: its slots and how it reads its inputs (design.md §3).

A capability class declares three read-only slot mappings: `PARAMETERS` (slot -> parameter kind),
`CONSUMES` and `PRODUCES` (slot -> artifact value type). Subclasses may assign plain dicts; the
base exposes every mapping as a `MappingProxyType`, empty when nothing is declared. When a subclass
is defined, the base checks that every slot name is snake_case, unique across the three mappings,
and a keyword parameter of the constructor; otherwise it raises `InvalidCapabilityError` naming
the class and the slot. Names and values are made up.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from decimal import Decimal
from types import MappingProxyType
from typing import Any, assert_type, cast

import pytest

from app.domain.artifact import Artifact, ArtifactKind, Money
from app.domain.capability import Capability, CapabilityResult
from app.domain.errors import (
    CapabilityContractError,
    DomainError,
    DuplicateArtifactError,
    InvalidCapabilityError,
    MissingArtifactError,
)
from app.domain.parameters.datasets import ParameterDataset
from app.domain.parameters.kind import ParameterKind
from app.domain.parameters.rounding import NO_ROUNDING

D = Decimal
IN = ArtifactKind("ex/in", Decimal)
OTHER = ArtifactKind("ex/other", Decimal)
OUT = ArtifactKind("ex/out", Decimal)
FACTOR = ParameterKind("factor", Decimal)
OFFSET = ParameterKind("offset", Decimal)


class Reader(Capability):
    """Consumes `IN` and `OTHER`; `read` returns what `_input` finds for a kind. Has no slots."""

    @property
    def consumes(self) -> frozenset[ArtifactKind[Any]]:
        return frozenset({IN, OTHER})

    @property
    def produces(self) -> frozenset[ArtifactKind[Any]]:
        return frozenset({OUT})

    def compute(self, inputs: tuple[Artifact[Any], ...]) -> CapabilityResult:
        return CapabilityResult(outputs=(Artifact(OUT, self._input(inputs, IN).value),), trace=())

    def read[V](self, inputs: tuple[Artifact[Any], ...], kind: ArtifactKind[V]) -> Artifact[V]:
        return self._input(inputs, kind)


class Scale(Capability):
    """Produces `target` = `source` × `factor` + `offset`; declares every kind of slot."""

    PARAMETERS = {"factor": FACTOR, "offset": OFFSET}
    CONSUMES = {"source": Decimal}
    PRODUCES = {"target": Decimal}

    def __init__(
        self,
        source: Money,
        target: Money,
        factor: ParameterDataset[Decimal],
        *,
        offset: ParameterDataset[Decimal],
    ) -> None:
        self._source, self._target = source, target
        self._factor, self._offset = factor, offset

    @property
    def consumes(self) -> frozenset[ArtifactKind[Any]]:
        return frozenset({self._source})

    @property
    def produces(self) -> frozenset[ArtifactKind[Any]]:
        return frozenset({self._target})

    def compute(self, inputs: tuple[Artifact[Any], ...]) -> CapabilityResult:
        value = self._input(inputs, self._source).value * self._factor.values + self._offset.values
        return CapabilityResult(outputs=(Artifact(self._target, value),), trace=())


# --- reading inputs -------------------------------------------------------------------------


def test_input_finds_the_artifact_of_the_kind() -> None:
    inputs = (Artifact(OTHER, D(2)), Artifact(IN, D(1)))

    found = Reader().read(inputs, IN)

    assert_type(found, Artifact[Decimal])
    assert found == Artifact(IN, D(1))


def test_input_matches_by_kind_equality_not_identity() -> None:
    inputs = (Artifact(ArtifactKind("ex/in", Decimal), D(1)),)

    assert Reader().read(inputs, IN) == Artifact(IN, D(1))


def test_input_rejects_a_missing_artifact() -> None:
    with pytest.raises(MissingArtifactError, match="Reader needs 'in'"):
        Reader().read((Artifact(OTHER, D(2)),), IN)


def test_input_rejects_two_artifacts_of_one_kind() -> None:
    with pytest.raises(DuplicateArtifactError, match="Reader got 2 values for 'in'"):
        Reader().read((Artifact(IN, D(1)), Artifact(IN, D(2))), IN)


def test_input_refuses_a_kind_the_capability_does_not_consume() -> None:
    with pytest.raises(CapabilityContractError, match="Reader does not consume 'out'"):
        Reader().read((Artifact(OUT, D(1)),), OUT)


def test_compute_returns_artifacts() -> None:
    result = Reader().compute((Artifact(IN, D(3)), Artifact(OTHER, D(4))))

    assert result.outputs == (Artifact(OUT, D(3)),)


# --- declared slots -------------------------------------------------------------------------


def test_the_base_declares_no_slots() -> None:
    for slots in (Capability.PARAMETERS, Capability.CONSUMES, Capability.PRODUCES):
        assert isinstance(slots, MappingProxyType)
        assert slots == {}


def test_a_capability_declaring_nothing_has_empty_slots() -> None:
    assert Reader.PARAMETERS == {}
    assert Reader.CONSUMES == {}
    assert Reader.PRODUCES == {}


def test_slot_mappings_are_typed() -> None:
    assert_type(Capability.PARAMETERS, Mapping[str, ParameterKind[Any]])
    assert_type(Capability.CONSUMES, Mapping[str, type])
    assert_type(Capability.PRODUCES, Mapping[str, type])


def test_declared_slots_are_exposed() -> None:
    assert Scale.PARAMETERS == {"factor": FACTOR, "offset": OFFSET}
    assert Scale.CONSUMES == {"source": Decimal}
    assert Scale.PRODUCES == {"target": Decimal}


def test_declared_slots_are_read_only() -> None:
    for slots in (Scale.PARAMETERS, Scale.CONSUMES, Scale.PRODUCES):
        assert isinstance(slots, MappingProxyType)
        with pytest.raises(TypeError):
            cast(Any, slots)["extra"] = Decimal


def test_a_capability_is_built_from_its_slot_names_as_keywords() -> None:
    arguments: dict[str, Any] = {
        "source": IN,
        "target": OUT,
        "factor": ParameterDataset("ex/factor", 2025, FACTOR, D(2), NO_ROUNDING, ("src",)),
        "offset": ParameterDataset("ex/offset", 2025, OFFSET, D(1), NO_ROUNDING, ("src",)),
    }

    scale = Scale(**arguments)

    assert set(arguments) == set(Scale.PARAMETERS) | set(Scale.CONSUMES) | set(Scale.PRODUCES)
    assert scale.compute((Artifact(IN, D(3)),)).outputs == (Artifact(OUT, D(7)),)


def test_a_subclass_inherits_its_parents_slots() -> None:
    class Child(Scale):
        pass

    assert Child.PARAMETERS == Scale.PARAMETERS
    assert Child.CONSUMES == Scale.CONSUMES
    assert Child.PRODUCES == Scale.PRODUCES


# --- slots are checked when a class is defined ----------------------------------------------


def test_rejects_a_parameter_slot_the_constructor_does_not_take() -> None:
    with pytest.raises(InvalidCapabilityError, match="Typo.*'facter'"):

        class Typo(Reader):
            PARAMETERS = {"facter": FACTOR}

            def __init__(self, factor: ParameterDataset[Decimal]) -> None:
                self.factor = factor


def test_rejects_a_consumed_slot_the_constructor_does_not_take() -> None:
    with pytest.raises(InvalidCapabilityError, match="Typo.*'base'"):

        class Typo(Reader):
            CONSUMES = {"base": Decimal}

            def __init__(self, source: Money) -> None:
                self.source = source


def test_rejects_a_produced_slot_the_constructor_does_not_take() -> None:
    with pytest.raises(InvalidCapabilityError, match="Typo.*'output'"):

        class Typo(Reader):
            PRODUCES = {"output": Decimal}


def test_rejects_a_slot_that_is_a_positional_only_parameter() -> None:
    with pytest.raises(InvalidCapabilityError, match="Positional.*'source'"):

        class Positional(Reader):
            CONSUMES = {"source": Decimal}

            def __init__(self, source: Money, /) -> None:
                self.source = source


def test_rejects_an_inherited_slot_a_new_constructor_drops() -> None:
    with pytest.raises(InvalidCapabilityError, match="Narrower.*'offset'"):

        class Narrower(Scale):
            def __init__(
                self, source: Money, target: Money, factor: ParameterDataset[Decimal]
            ) -> None:
                super().__init__(source, target, factor, offset=factor)


def test_accepts_keyword_only_slots() -> None:
    class KeywordOnly(Reader):
        CONSUMES = {"source": Decimal}

        def __init__(self, *, source: Money) -> None:
            self.source = source

    assert KeywordOnly.CONSUMES == {"source": Decimal}


def _takes_upper(self: Capability, *, Source: Money) -> None:
    pass


def _takes_double_underscore(self: Capability, *, two__parts: Money) -> None:
    pass


def _takes_trailing_underscore(self: Capability, *, trailing_: Money) -> None:
    pass


def _takes_leading_underscore(self: Capability, *, _hidden: Money) -> None:
    pass


@pytest.mark.parametrize(
    ("slot", "init"),
    [
        ("Source", _takes_upper),
        ("two__parts", _takes_double_underscore),
        ("trailing_", _takes_trailing_underscore),
        ("_hidden", _takes_leading_underscore),
    ],
)
def test_rejects_a_slot_name_that_is_not_snake_case(slot: str, init: Callable[..., None]) -> None:
    # The constructor does take the slot, so only its name is wrong.
    with pytest.raises(InvalidCapabilityError, match=f"Odd.*{slot!r}.*snake_case"):
        type("Odd", (Reader,), {"CONSUMES": {slot: Decimal}, "__init__": init})


def test_a_constructor_beside_a_custom_new_is_still_checked() -> None:
    class WithNew(Reader):
        CONSUMES = {"base": Decimal}

        def __new__(cls, *args: object, **kwargs: object) -> WithNew:
            return super().__new__(cls)

        def __init__(self, base: Money) -> None:
            self.base = base

    assert WithNew.CONSUMES == {"base": Decimal}
    assert WithNew(IN).base == IN


def test_rejects_self_as_a_slot() -> None:
    with pytest.raises(InvalidCapabilityError, match="Selfish.*'self'"):

        class Selfish(Reader):
            CONSUMES = {"self": Decimal}

            def __init__(self, source: Money) -> None:
                self.source = source


def test_rejects_slots_a_constructor_takes_only_through_var_keywords() -> None:
    with pytest.raises(InvalidCapabilityError, match="Loose.*'source'"):

        class Loose(Reader):
            CONSUMES = {"source": Decimal}

            def __init__(self, **slots: Money) -> None:
                self.slots = slots


@pytest.mark.parametrize(
    ("mapping", "slots", "message"),
    [
        ("CONSUMES", {7: Decimal}, "Bad.*CONSUMES slot 7.*must be a string"),
        ("PARAMETERS", {"factor": Decimal}, "Bad.*PARAMETERS slot 'factor'.*ParameterKind"),
        ("CONSUMES", {"source": IN}, "Bad.*CONSUMES slot 'source'.*must be a type"),
        ("PRODUCES", {"target": "Decimal"}, "Bad.*PRODUCES slot 'target'.*must be a type"),
        ("PRODUCES", [("target", Decimal)], "Bad.*PRODUCES must be a mapping"),
    ],
)
def test_rejects_malformed_slot_declarations(mapping: str, slots: object, message: str) -> None:
    def init(self: Capability, factor: object, source: object, target: object) -> None:
        pass

    with pytest.raises(InvalidCapabilityError, match=message):
        type("Bad", (Reader,), {mapping: slots, "__init__": init})


@pytest.mark.parametrize(
    ("first", "second"),
    [("PARAMETERS", "CONSUMES"), ("PARAMETERS", "PRODUCES"), ("CONSUMES", "PRODUCES")],
)
def test_rejects_a_slot_name_used_in_two_mappings(first: str, second: str) -> None:
    slots: dict[str, Mapping[str, Any]] = {
        "PARAMETERS": {"value": FACTOR},
        "CONSUMES": {"value": Decimal},
        "PRODUCES": {"value": Decimal},
    }

    def init(self: Capability, value: object) -> None:
        pass

    namespace = {first: slots[first], second: slots[second], "__init__": init}
    with pytest.raises(InvalidCapabilityError, match="Twice.*'value'"):
        type("Twice", (Reader,), namespace)


def test_invalid_capability_is_a_domain_error() -> None:
    assert issubclass(InvalidCapabilityError, DomainError)
