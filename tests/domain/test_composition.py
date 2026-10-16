"""Unit tests for the Composition: wired capabilities, checked and ordered (design.md §5).

A composition is built from capabilities and the kinds a computation takes and returns. It
rejects bad wiring when built, derives a deterministic execution order from the capabilities'
contracts, and computes by applying each capability, in that order, to a fresh worksheet.
Generic tests use made-up kinds and the small `Link` capability below.
"""

from __future__ import annotations

from collections.abc import Iterable
from decimal import Decimal
from itertools import permutations
from typing import Any, assert_type, cast

import pytest

from app.domain.artifact import Artifact, ArtifactKind
from app.domain.capabilities.non_refundable_credit import NonRefundableCredit
from app.domain.capabilities.progressive_tax import ProgressiveTax
from app.domain.capability import Capability, CapabilityRegistry, CapabilityResult, TraceLine
from app.domain.composition import Composition
from app.domain.errors import (
    DomainError,
    DuplicateArtifactError,
    InvalidCompositionError,
)
from app.domain.parameters.brackets import BRACKETS, Bracket, BracketSchedule
from app.domain.parameters.credit import CREDIT, Credit
from app.domain.parameters.datasets import ParameterDataset
from app.domain.parameters.rate import RATE, Rate
from app.domain.parameters.rounding import NO_ROUNDING
from app.domain.worksheet import Worksheet

D = Decimal
A = ArtifactKind("ex/a", Decimal)
B = ArtifactKind("ex/b", Decimal)
C = ArtifactKind("ex/c", Decimal)
E = ArtifactKind("ex/e", Decimal)
F = ArtifactKind("ex/f", Decimal)
ZERO = D(0)


class Link(Capability):
    """Consumes `consumes`, and produces each kind of `produces` as the sum of its inputs + `add`.

    Its one trace line is labelled `tag`, so tests can see the order capabilities ran in. It takes
    any number of kinds, so it declares no slots.
    """

    def __init__(
        self,
        consumes: Iterable[ArtifactKind[Any]],
        produces: Iterable[ArtifactKind[Any]],
        add: Decimal = ZERO,
        tag: str = "link",
    ) -> None:
        self._consumes = frozenset(consumes)
        self._produces = frozenset(produces)
        self._add = add
        self.tag = tag

    @property
    def consumes(self) -> frozenset[ArtifactKind[Any]]:
        return self._consumes

    @property
    def produces(self) -> frozenset[ArtifactKind[Any]]:
        return self._produces

    def compute(self, inputs: tuple[Artifact[Any], ...]) -> CapabilityResult:
        total = sum((self._input(inputs, kind).value for kind in self._consumes), ZERO) + self._add
        outputs = tuple(Artifact(kind, total) for kind in self._produces)
        return CapabilityResult(outputs=outputs, trace=(TraceLine(self.tag, total),))

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.tag})"


class Left(Link):
    """A `Link` whose class name sorts before `Right`'s."""


class Right(Link):
    """A `Link` whose class name sorts after `Left`'s."""


class Apple(Link):
    """A `Link` whose class name sorts before `Zebra`'s."""


class Zebra(Link):
    """A `Link` whose class name sorts after `Apple`'s."""


def kinds(*members: ArtifactKind[Any]) -> frozenset[ArtifactKind[Any]]:
    return frozenset(members)


# --- construction and build-time checks ---------------------------------------------------------


def test_a_well_wired_composition_builds() -> None:
    first, second = Link([A], [B]), Link([B], [C])

    composition = Composition([first, second], inputs=kinds(A), outputs=kinds(C))

    assert composition.order == (first, second)


def test_accepts_any_iterable_of_capabilities() -> None:
    first, second = Link([A], [B]), Link([B], [C])

    composition = Composition(iter([second, first]), inputs=kinds(A), outputs=kinds(C))

    assert composition.order == (first, second)


def test_wires_by_kind_equality_not_identity() -> None:
    first = Link([A], [ArtifactKind("ex/b", Decimal)])
    second = Link([ArtifactKind("ex/b", Decimal)], [C])

    composition = Composition([second, first], inputs=kinds(A), outputs=kinds(C))

    assert composition.order == (first, second)


def test_rejects_a_consumed_kind_nothing_produces() -> None:
    with pytest.raises(InvalidCompositionError, match="no producer for 'b'"):
        Composition([Link([A, B], [C])], inputs=kinds(A), outputs=kinds(C))


def test_rejects_a_consumed_kind_produced_only_with_another_value_type() -> None:
    b_as_int = ArtifactKind("ex/b", int)
    producer = Link([A], [b_as_int])
    consumer = Link([B], [C])

    with pytest.raises(InvalidCompositionError, match="no producer for 'b'") as raised:
        Composition([producer, consumer], inputs=kinds(A), outputs=kinds(b_as_int, C))

    message = str(raised.value)
    assert "int" in message
    assert "Decimal" in message


def test_rejects_a_cycle_and_names_its_kinds() -> None:
    to_b = Link([A, C], [B])
    to_c = Link([B], [C])
    to_e = Link([B], [E])

    with pytest.raises(InvalidCompositionError, match="cycle") as raised:
        Composition([to_b, to_c, to_e], inputs=kinds(A), outputs=kinds(E))

    message = str(raised.value)
    assert "cycle involving" in message
    assert "'b'" in message
    assert "'c'" in message
    assert "'e'" not in message  # strictly downstream of the cycle


def test_rejects_a_capability_that_consumes_what_it_produces() -> None:
    with pytest.raises(InvalidCompositionError, match="cycle.*'b'"):
        Composition([Link([A, B], [B])], inputs=kinds(A), outputs=kinds(B))


def test_rejects_an_orphan_output() -> None:
    with pytest.raises(InvalidCompositionError, match="orphan") as raised:
        Composition([Link([A], [B]), Link([A], [C])], inputs=kinds(A), outputs=kinds(B))

    assert "'c'" in str(raised.value)


def test_rejects_a_declared_output_nothing_produces() -> None:
    with pytest.raises(InvalidCompositionError, match="output 'c'"):
        Composition([Link([A], [B])], inputs=kinds(A), outputs=kinds(B, C))


def test_rejects_two_capabilities_producing_one_kind() -> None:
    with pytest.raises(InvalidCompositionError, match="more than one") as raised:
        Composition(
            [Link([A], [B], tag="one"), Link([A], [B], tag="two")],
            inputs=kinds(A),
            outputs=kinds(B),
        )

    assert "'b'" in str(raised.value)


def test_rejects_a_declared_input_a_capability_also_produces() -> None:
    with pytest.raises(InvalidCompositionError, match="input 'b'") as raised:
        Composition([Link([A], [B])], inputs=kinds(A, B), outputs=kinds(B))

    assert "produce" in str(raised.value)


def test_rejects_a_declared_input_nothing_consumes() -> None:
    with pytest.raises(InvalidCompositionError, match="input 'c' is consumed by nothing"):
        Composition([Link([A], [B])], inputs=kinds(A, C), outputs=kinds(B))


def test_rejects_a_capability_that_produces_nothing() -> None:
    with pytest.raises(InvalidCompositionError, match="Link produces nothing"):
        Composition([Link([A], [B]), Link([A], [])], inputs=kinds(A), outputs=kinds(B))


def test_naming_duplicate_producers_does_not_depend_on_the_order_given() -> None:
    left, right = Left([A], [B]), Right([A], [B])
    messages = set()

    for given in ([left, right], [right, left]):
        with pytest.raises(InvalidCompositionError, match="more than one") as raised:
            Composition(given, inputs=kinds(A), outputs=kinds(B))
        messages.add(str(raised.value))

    assert len(messages) == 1


def test_naming_an_unsatisfied_consume_does_not_depend_on_the_order_given() -> None:
    needs_e, needs_f = Left([A, E], [B]), Right([A, F], [C])
    messages = set()

    for given in ([needs_e, needs_f], [needs_f, needs_e]):
        with pytest.raises(InvalidCompositionError, match="no producer") as raised:
            Composition(given, inputs=kinds(A), outputs=kinds(B, C))
        messages.add(str(raised.value))

    assert len(messages) == 1


def test_invalid_composition_is_a_domain_error() -> None:
    assert issubclass(InvalidCompositionError, DomainError)


# --- derived order -------------------------------------------------------------------------------


def test_order_is_derived_from_contracts_whatever_order_capabilities_are_given_in() -> None:
    chain: tuple[Capability, ...] = (
        Link([A], [B], tag="1"),
        Link([B], [C], tag="2"),
        Link([C], [E], tag="3"),
        Link([E], [F], tag="4"),
    )

    for given in permutations(chain):
        composition = Composition(given, inputs=kinds(A), outputs=kinds(F))

        assert composition.order == chain


def test_order_of_a_diamond_is_the_same_for_every_input_order() -> None:
    left, right, join = Left([A], [B]), Right([A], [C]), Link([B, C], [E])

    for given in permutations((left, right, join)):
        composition = Composition(given, inputs=kinds(A), outputs=kinds(E))

        assert composition.order == (left, right, join)


def test_ties_are_broken_by_class_name_when_unregistered() -> None:
    apple, zebra = Apple([A], [C]), Zebra([A], [B])

    for given in ([apple, zebra], [zebra, apple]):
        composition = Composition(given, inputs=kinds(A), outputs=kinds(B, C))

        assert composition.order == (apple, zebra)


def test_ties_are_broken_by_registered_identifier(monkeypatch: pytest.MonkeyPatch) -> None:
    registry = CapabilityRegistry()
    registry.register("ex/first", Zebra)
    registry.register("ex/second", Apple)
    monkeypatch.setattr(CapabilityRegistry, "shared", classmethod(lambda cls: registry))
    apple, zebra = Apple([A], [C]), Zebra([A], [B])

    for given in ([apple, zebra], [zebra, apple]):
        composition = Composition(given, inputs=kinds(A), outputs=kinds(B, C))

        assert composition.order == (zebra, apple)


def test_ties_between_instances_of_one_class_are_broken_by_what_they_produce() -> None:
    to_c, to_b = Link([A], [C]), Link([A], [B])

    for given in ([to_c, to_b], [to_b, to_c]):
        composition = Composition(given, inputs=kinds(A), outputs=kinds(B, C))

        assert composition.order == (to_b, to_c)


def test_ties_between_kinds_sharing_an_identifier_are_broken_by_value_type() -> None:
    b_as_int = ArtifactKind("ex/b", int)
    to_decimal, to_int = Link([A], [B]), Link([A], [b_as_int])

    for given in ([to_decimal, to_int], [to_int, to_decimal]):
        composition = Composition(given, inputs=kinds(A), outputs=kinds(B, b_as_int))

        assert composition.order == (to_decimal, to_int)


def test_order_is_a_read_only_tuple() -> None:
    composition = Composition([Link([A], [B])], inputs=kinds(A), outputs=kinds(B))

    assert_type(composition.order, tuple[Capability, ...])
    assert isinstance(composition.order, tuple)
    with pytest.raises(AttributeError):
        cast(Any, composition).order = ()


# --- compute -------------------------------------------------------------------------------------


def chain_composition() -> tuple[Composition, Link, Link]:
    first, second = Link([A], [B], D(1), "first"), Link([B], [C], D(10), "second")
    return Composition([second, first], inputs=kinds(A), outputs=kinds(C)), first, second


def test_compute_runs_the_capabilities_in_order_and_returns_the_worksheet() -> None:
    composition, first, second = chain_composition()

    worksheet = composition.compute(Artifact(A, D(2)))

    assert_type(worksheet, Worksheet)
    assert worksheet.get(C) == Artifact(C, D(13))
    assert worksheet.get(A) == Artifact(A, D(2))
    assert worksheet.producer_of(A) is None
    assert worksheet.producer_of(B) is first
    assert worksheet.producer_of(C) is second
    assert worksheet.trace == (TraceLine("first", D(3)), TraceLine("second", D(13)))


def test_compute_follows_a_diamond() -> None:
    left, right = Left([A], [B], D(1), "left"), Right([A], [C], D(2), "right")
    join = Link([B, C], [E], tag="join")
    composition = Composition([join, right, left], inputs=kinds(A), outputs=kinds(E))

    worksheet = composition.compute(Artifact(A, D(5)))

    assert worksheet.get(E) == Artifact(E, D(13))
    assert [line.description for line in worksheet.trace] == ["left", "right", "join"]


def test_each_compute_gets_a_fresh_worksheet() -> None:
    composition, _, _ = chain_composition()

    once = composition.compute(Artifact(A, D(2)))
    again = composition.compute(Artifact(A, D(5)))

    assert once is not again
    assert once.get(C) == Artifact(C, D(13))
    assert again.get(C) == Artifact(C, D(16))
    assert len(once.trace) == 2


def test_compute_takes_several_inputs() -> None:
    composition = Composition([Link([A, B], [C])], inputs=kinds(A, B), outputs=kinds(C))

    worksheet = composition.compute(Artifact(B, D(4)), Artifact(A, D(3)))

    assert worksheet.get(C) == Artifact(C, D(7))


def test_compute_rejects_a_missing_input() -> None:
    composition = Composition([Link([A, B], [C])], inputs=kinds(A, B), outputs=kinds(C))

    with pytest.raises(InvalidCompositionError, match="'b'"):
        composition.compute(Artifact(A, D(3)))


def test_compute_rejects_an_extra_starting_artifact() -> None:
    composition, _, _ = chain_composition()

    with pytest.raises(InvalidCompositionError, match="'e'"):
        composition.compute(Artifact(A, D(2)), Artifact(E, D(1)))


def test_compute_names_several_extra_starting_artifacts_grammatically() -> None:
    composition, _, _ = chain_composition()

    with pytest.raises(InvalidCompositionError, match="'c', 'e' are not inputs"):
        composition.compute(Artifact(A, D(2)), Artifact(E, D(1)), Artifact(C, D(1)))


def test_compute_names_the_value_type_of_a_starting_artifact_of_the_wrong_type() -> None:
    composition, _, _ = chain_composition()

    with pytest.raises(InvalidCompositionError, match="'a'") as raised:
        composition.compute(Artifact(ArtifactKind("ex/a", int), 2))

    message = str(raised.value)
    assert "int" in message
    assert "Decimal" in message


def test_compute_rejects_a_starting_artifact_the_composition_produces() -> None:
    composition, _, _ = chain_composition()

    with pytest.raises(InvalidCompositionError, match="'b'"):
        composition.compute(Artifact(A, D(2)), Artifact(B, D(1)))


def test_compute_rejects_two_values_for_one_input() -> None:
    composition, _, _ = chain_composition()

    with pytest.raises(DuplicateArtifactError, match="'a'"):
        composition.compute(Artifact(A, D(2)), Artifact(A, D(3)))


# --- end to end, with made-up data ---------------------------------------------------------------

TAXABLE_BASE = ArtifactKind("ex/taxable_base", Decimal)
BASIC_TAX = ArtifactKind("ex/basic_tax", Decimal)
TAX_AFTER_CREDIT = ArtifactKind("ex/tax_after_credit", Decimal)

SOURCES = ("https://example.org/2025",)
SCHEDULE = ParameterDataset(
    "ex/brackets",
    2025,
    BRACKETS,
    BracketSchedule(
        (Bracket(D(0), D("0.10")), Bracket(D(100), D("0.20")), Bracket(D(300), D("0.30")))
    ),
    NO_ROUNDING,
    SOURCES,
)
CREDIT_AMOUNT = ParameterDataset("ex/credit", 2025, CREDIT, Credit(D(400)), NO_ROUNDING, SOURCES)
CREDIT_RATE = ParameterDataset("ex/credit_rate", 2025, RATE, Rate(D("0.15")), NO_ROUNDING, SOURCES)


def test_end_to_end_two_real_capabilities_given_in_the_wrong_order() -> None:
    tax = ProgressiveTax(TAXABLE_BASE, BASIC_TAX, SCHEDULE)
    credit = NonRefundableCredit(BASIC_TAX, TAX_AFTER_CREDIT, CREDIT_AMOUNT, CREDIT_RATE)  # 60
    composition = Composition(
        [credit, tax], inputs=kinds(TAXABLE_BASE), outputs=kinds(TAX_AFTER_CREDIT)
    )

    worksheet = composition.compute(Artifact(TAXABLE_BASE, D(500)))

    # 10% of 100 + 20% of 200 + 30% of 200 = 110; less a credit of 15% of 400 = 60.
    assert composition.order == (tax, credit)
    assert worksheet.get(BASIC_TAX) == Artifact(BASIC_TAX, D(110))
    assert worksheet.get(TAX_AFTER_CREDIT) == Artifact(TAX_AFTER_CREDIT, D(50))
    assert worksheet.producer_of(TAX_AFTER_CREDIT) is credit
    assert worksheet.trace[-1].amount == D(50)
    assert worksheet.trace[3].amount == D(110)
