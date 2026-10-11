"""Unit tests for ParameterParserRegistry and `@parameter_parser`.

Parsers are keyed by their kind's plain name (`brackets`, `credit`), not namespaced yet.
Lookups are typed: `for_kind(kind)` for a `ParameterKind[T]` gives a `ParameterParser[T]`; the
`assert_type` checks below make `mypy .` fail if a lookup returned `Any` or another type.
Made-up kinds and parsers are never registered in the shared registry: the decorator test
points `ParameterParserRegistry.shared` at a fresh registry with monkeypatch.
"""

from __future__ import annotations

from decimal import Decimal
from typing import assert_type

import pytest

from app.adapters.outbound.parameter_parsers import ParameterParser
from app.adapters.outbound.parameter_parsers.brackets import BracketsParser
from app.adapters.outbound.parameter_parsers.credit import CreditParser
from app.adapters.outbound.parameter_parsers.registry import (
    ParameterParserRegistry,
    parameter_parser,
)
from app.adapters.outbound.yaml_support import YamlNode
from app.domain.capability import CapabilityRegistry
from app.domain.errors import DuplicateRegistrationError, UnknownRegistrationError
from app.domain.parameters.brackets import BRACKETS, Bracket, BracketSchedule
from app.domain.parameters.credit import CREDIT, Credit
from app.domain.parameters.kind import ParameterKind
from app.domain.registry import Registry

D = Decimal

FLAT_RATE = ParameterKind("flat_rate", Decimal)


class FlatRateParser:
    """A made-up kind's parser, registered only in registries the tests create."""

    kind = FLAT_RATE
    body_keys = frozenset({"rate"})

    def parse(self, document: YamlNode) -> Decimal:
        return document.field("rate").parse_decimal()


class OtherFlatRateParser(FlatRateParser):
    """A second parser for the same made-up kind."""


@pytest.fixture
def fresh(monkeypatch: pytest.MonkeyPatch) -> ParameterParserRegistry:
    """A fresh registry that `@parameter_parser` registers into for the duration of one test."""
    registry = ParameterParserRegistry()
    monkeypatch.setattr(ParameterParserRegistry, "shared", classmethod(lambda cls: registry))
    return registry


# --- typed registration and lookup ------------------------------------------------------------


def test_parameter_parser_registry_is_a_registry() -> None:
    assert issubclass(ParameterParserRegistry, Registry)


def test_register_parser_returns_the_parser_itself() -> None:
    parser = FlatRateParser()

    registered = ParameterParserRegistry().register_parser(parser)

    assert_type(registered, ParameterParser[Decimal])

    assert registered is parser


def test_for_kind_returns_the_parser_registered_for_the_kind() -> None:
    registry = ParameterParserRegistry()
    brackets = BracketsParser()
    registry.register_parser(brackets)
    registry.register_parser(CreditParser())

    found = registry.for_kind(BRACKETS)

    assert_type(found, ParameterParser[BracketSchedule])
    assert found is brackets
    assert found.kind is BRACKETS


def test_for_kind_is_typed_by_the_kind() -> None:
    registry = ParameterParserRegistry()
    registry.register_parser(BracketsParser())
    registry.register_parser(CreditParser())
    registry.register_parser(FlatRateParser())

    schedule = registry.for_kind(BRACKETS).parse(
        YamlNode.root({"brackets": [{"from": "0", "rate": "0.1"}]}, "dataset")
    )
    credit = registry.for_kind(CREDIT).parse(
        YamlNode.root({"amount": "100", "rate": "0.5"}, "dataset")
    )
    rate = registry.for_kind(FLAT_RATE).parse(YamlNode.root({"rate": "0.2"}, "dataset"))

    assert_type(schedule, BracketSchedule)
    assert_type(credit, Credit)
    assert_type(rate, Decimal)

    assert schedule == BracketSchedule((Bracket(D("0"), D("0.1")),))
    assert credit == Credit(amount=D("100"), rate=D("0.5"))
    assert rate == D("0.2")


def test_parsers_are_keyed_by_their_kind_name() -> None:
    registry = ParameterParserRegistry()
    parser = FlatRateParser()
    registry.register_parser(parser)

    assert registry.get("flat_rate") is parser  # the inherited string-keyed lookup


def test_registering_two_parsers_for_one_kind_fails() -> None:
    registry = ParameterParserRegistry()
    first = FlatRateParser()
    registry.register_parser(first)

    with pytest.raises(DuplicateRegistrationError, match="'flat_rate'"):
        registry.register_parser(OtherFlatRateParser())

    assert registry.for_kind(FLAT_RATE) is first  # never silently overridden


def test_getting_a_kind_without_a_parser_fails() -> None:
    registry = ParameterParserRegistry()
    registry.register_parser(BracketsParser())

    with pytest.raises(UnknownRegistrationError, match="'flat_rate'"):
        registry.for_kind(FLAT_RATE)


def test_a_kind_with_a_registered_name_but_another_value_type_is_unknown() -> None:
    registry = ParameterParserRegistry()
    registry.register_parser(BracketsParser())
    impostor = ParameterKind("brackets", Decimal)

    with pytest.raises(UnknownRegistrationError, match="'brackets'"):
        registry.for_kind(impostor)


def test_a_non_parser_stored_under_a_kind_name_is_unknown() -> None:
    # The inherited string-keyed `register` bypasses `register_parser`; `for_kind` must not
    # trust what it finds there.
    registry = ParameterParserRegistry()
    registry.register("brackets", 42)

    with pytest.raises(UnknownRegistrationError, match="'brackets'"):
        registry.for_kind(BRACKETS)


# --- the shared registry ----------------------------------------------------------------------


def test_shared_returns_the_same_instance_every_time() -> None:
    assert ParameterParserRegistry.shared() is ParameterParserRegistry.shared()
    assert isinstance(ParameterParserRegistry.shared(), ParameterParserRegistry)


def test_a_directly_constructed_registry_is_separate_and_empty() -> None:
    registry = ParameterParserRegistry()

    assert registry is not ParameterParserRegistry.shared()
    with pytest.raises(UnknownRegistrationError):
        registry.for_kind(BRACKETS)


def test_shared_parser_registry_is_not_the_shared_capability_registry() -> None:
    assert id(ParameterParserRegistry.shared()) != id(CapabilityRegistry.shared())


# --- the decorator ----------------------------------------------------------------------------


def test_decorator_registers_an_instance_under_its_kind(fresh: ParameterParserRegistry) -> None:
    parameter_parser(FlatRateParser)

    found = fresh.for_kind(FLAT_RATE)

    assert_type(found, ParameterParser[Decimal])
    assert isinstance(found, FlatRateParser)


def test_decorator_returns_the_class_unchanged(fresh: ParameterParserRegistry) -> None:
    decorated = parameter_parser(FlatRateParser)

    assert_type(decorated, type[FlatRateParser])

    assert decorated is FlatRateParser


def test_decorating_a_second_parser_for_one_kind_fails(fresh: ParameterParserRegistry) -> None:
    parameter_parser(FlatRateParser)

    with pytest.raises(DuplicateRegistrationError, match="'flat_rate'"):
        parameter_parser(OtherFlatRateParser)


@pytest.mark.parametrize(
    ("kind", "parser_class"),
    [(BRACKETS, BracketsParser), (CREDIT, CreditParser)],
)
def test_built_in_parsers_are_registered_in_the_shared_registry(
    kind: ParameterKind[object], parser_class: type[object]
) -> None:
    parser = ParameterParserRegistry.shared().for_kind(kind)

    assert isinstance(parser, parser_class)
    assert parser.kind is kind
