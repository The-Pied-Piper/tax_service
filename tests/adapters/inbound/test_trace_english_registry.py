"""Unit tests for EnglishRendererRegistry, `@english_renderer` and EnglishTraceRenderer's lookup.

A line class's English text is a renderer class registered beside it (`line_class = <the line
class>`, `render(self, line) -> str`), keyed by the line class itself; EnglishTraceRenderer looks
the renderer up by `type(line)`, in the registry it is given or by default the shared one. Made-up
lines and renderers are never registered in the shared registry: the decorator tests point
`EnglishRendererRegistry.shared` at a fresh registry with monkeypatch, and the made-up package in
`rendering_fixtures` is imported only while it does, then forgotten.
"""

from __future__ import annotations

import importlib
import inspect
import sys
from collections.abc import Iterator
from dataclasses import dataclass
from decimal import Decimal
from types import ModuleType
from typing import assert_type

import pytest

# Imported first, so the core and jurisdiction renderers fill the real shared registry before any
# test points `shared` at a fresh one.
import app.adapters.inbound.trace_english
import app.domain.trace
import app.jurisdictions.ca.trace
import app.jurisdictions.ca_on.trace
from app.adapters.inbound.trace_english import EnglishTraceRenderer
from app.adapters.inbound.trace_english.registry import (
    EnglishRendererRegistry,
    english_renderer,
)
from app.adapters.outbound.parameter_parsers.registry import ParameterParserRegistry
from app.domain.artifact import ArtifactKind
from app.domain.errors import DuplicateRegistrationError, UnknownRegistrationError
from app.domain.registry import Registry
from app.domain.trace import SumLine, TraceLine

D = Decimal

EX_TOTAL = ArtifactKind("ex/total", Decimal)

REAL_SHARED = EnglishRendererRegistry.shared()  # before any test points `shared` elsewhere


@dataclass(frozen=True)
class ExampleLine(TraceLine):
    """A made-up line class, registered only in registries the tests create."""

    figure: Decimal

    @property
    def amount(self) -> Decimal:
        return self.figure


@dataclass(frozen=True)
class ExampleSubLine(ExampleLine):
    """A subclass of the made-up line class, with no renderer of its own."""


class ExampleRenderer:
    """The made-up line's English text."""

    line_class = ExampleLine

    def render(self, line: ExampleLine) -> str:
        return f"example of {line.figure}"


class OtherExampleRenderer(ExampleRenderer):
    """A second renderer for the same made-up line class."""


@pytest.fixture
def fresh(monkeypatch: pytest.MonkeyPatch) -> EnglishRendererRegistry:
    """A fresh registry that `@english_renderer` registers into for the duration of one test."""
    registry = EnglishRendererRegistry()
    monkeypatch.setattr(EnglishRendererRegistry, "shared", classmethod(lambda cls: registry))
    return registry


# --- registration and lookup by line class -----------------------------------------------------


def test_english_renderer_registry_is_a_registry() -> None:
    assert issubclass(EnglishRendererRegistry, Registry)


def test_register_class_returns_the_class_unchanged() -> None:
    registered = EnglishRendererRegistry().register_class(ExampleRenderer)

    assert_type(registered, type[ExampleRenderer])

    assert registered is ExampleRenderer


def test_for_line_class_returns_the_renderer_registered_for_the_class() -> None:
    registry = EnglishRendererRegistry()
    registry.register_class(ExampleRenderer)

    found = registry.for_line_class(ExampleLine)

    assert isinstance(found, ExampleRenderer)
    assert found.line_class is ExampleLine
    assert found.render(ExampleLine(D("2.5"))) == "example of 2.5"


def test_registering_two_renderers_for_one_line_class_fails() -> None:
    registry = EnglishRendererRegistry()
    registry.register_class(ExampleRenderer)
    first = registry.for_line_class(ExampleLine)

    with pytest.raises(DuplicateRegistrationError, match="ExampleLine"):
        registry.register_class(OtherExampleRenderer)

    assert registry.for_line_class(ExampleLine) is first  # never silently overridden


def test_looking_up_a_line_class_without_a_renderer_fails_naming_it() -> None:
    registry = EnglishRendererRegistry()

    with pytest.raises(UnknownRegistrationError, match="ExampleLine"):
        registry.for_line_class(ExampleLine)


def test_a_subclass_of_a_registered_line_class_has_no_renderer() -> None:
    # Keyed by the exact class, as EnglishTraceRenderer looks up `type(line)`.
    registry = EnglishRendererRegistry()
    registry.register_class(ExampleRenderer)

    with pytest.raises(UnknownRegistrationError, match="ExampleSubLine"):
        registry.for_line_class(ExampleSubLine)


def test_a_non_renderer_stored_under_a_line_class_key_is_unknown() -> None:
    # The inherited string-keyed `register` bypasses `register_class`; `for_line_class` must not
    # trust what it finds there.
    registry = EnglishRendererRegistry()
    registry.register(f"{ExampleLine.__module__}.{ExampleLine.__qualname__}", 42)

    with pytest.raises(UnknownRegistrationError, match="ExampleLine"):
        registry.for_line_class(ExampleLine)


# --- the shared registry ---------------------------------------------------------------------


def test_shared_returns_the_same_instance_every_time() -> None:
    assert EnglishRendererRegistry.shared() is EnglishRendererRegistry.shared()
    assert isinstance(EnglishRendererRegistry.shared(), EnglishRendererRegistry)


def test_a_directly_constructed_registry_is_separate_and_empty() -> None:
    registry = EnglishRendererRegistry()

    assert registry is not EnglishRendererRegistry.shared()
    with pytest.raises(UnknownRegistrationError):
        registry.for_line_class(SumLine)


def test_shared_renderer_registry_is_not_the_shared_parser_registry() -> None:
    assert id(EnglishRendererRegistry.shared()) != id(ParameterParserRegistry.shared())


def test_the_shared_registry_holds_exactly_the_built_in_renderers() -> None:
    assert REAL_SHARED.identifiers() == {
        "app.domain.trace.arithmetic.AmountOrDividedByRateLine",
        "app.domain.trace.arithmetic.AtMostLine",
        "app.domain.trace.arithmetic.CappedAmountLine",
        "app.domain.trace.arithmetic.CreditAmountLine",
        "app.domain.trace.arithmetic.DividedByRateLine",
        "app.domain.trace.arithmetic.FractionAppliedLine",
        "app.domain.trace.arithmetic.GreaterOfLine",
        "app.domain.trace.arithmetic.LesserOfLine",
        "app.domain.trace.arithmetic.MultipleOverLine",
        "app.domain.trace.arithmetic.PerUnitAmountLine",
        "app.domain.trace.arithmetic.QuotientLine",
        "app.domain.trace.arithmetic.RateAppliedLine",
        "app.domain.trace.arithmetic.RatioAppliedLine",
        "app.domain.trace.arithmetic.RoundedTotalLine",
        "app.domain.trace.arithmetic.SubtractedLine",
        "app.domain.trace.arithmetic.SubtractedNotBelowZeroLine",
        "app.domain.trace.arithmetic.SumLine",
        "app.domain.trace.arithmetic.SumNotBelowZeroLine",
        "app.domain.trace.arithmetic.ThresholdGateLine",
        "app.domain.trace.arithmetic.TimesCountLine",
        "app.domain.trace.choices.ChosenByCountLine",
        "app.domain.trace.choices.ChosenByRangeLine",
        "app.domain.trace.choices.ConditionLine",
        "app.domain.trace.choices.ConditionsCountLine",
        "app.domain.trace.rate_tables.AmountByCountLine",
        "app.domain.trace.rate_tables.BracketColumnLine",
        "app.domain.trace.rate_tables.ChosenRateAppliedLine",
        "app.domain.trace.rate_tables.ContributionTierLine",
        "app.domain.trace.rate_tables.RateByIncomeBandLine",
        "app.domain.trace.rate_tables.SurchargeTierLine",
        "app.domain.trace.rate_tables.TaperedAmountLine",
        "app.domain.trace.record_lists.ItemLesserOfLine",
        "app.domain.trace.record_lists.ItemSumLine",
        "app.domain.trace.record_lists.ItemsTotalLine",
        "app.domain.trace.record_lists.RecordCountLine",
        "app.domain.trace.record_lists.RecordTotalLine",
        "app.jurisdictions.ca.trace.capital_cost.CcaClaimLine",
        "app.jurisdictions.ca.trace.capital_cost.ClosingUccLine",
        "app.jurisdictions.ca.trace.capital_cost.RecapturedCcaLine",
        "app.jurisdictions.ca.trace.capital_cost.TerminalLossLine",
        "app.jurisdictions.ca.trace.dependants.CaregiverClaimLine",
        "app.jurisdictions.ca.trace.dependants.DisabilityTransferLine",
        "app.jurisdictions.ca.trace.dependants.OtherDependantMedicalLine",
        "app.jurisdictions.ca.trace.gains.DispositionGainLine",
        "app.jurisdictions.ca.trace.gains.DispositionGainOnlyLine",
        "app.jurisdictions.ca.trace.gains.DispositionProceedsLine",
        "app.jurisdictions.ca.trace.gains.PrincipalResidenceGainLine",
        "app.jurisdictions.ca.trace.percentages.PercentageAppliedLine",
        "app.jurisdictions.ca.trace.rentals.ShortTermRentalNonCompliantCcaByClassLine",
        "app.jurisdictions.ca.trace.rentals.ShortTermRentalNonCompliantCcaLine",
        "app.jurisdictions.ca.trace.rentals.ShortTermRentalNonCompliantLine",
        "app.jurisdictions.ca_on.trace.dependants.CaregiverClaimLessClaimedLine",
        "app.jurisdictions.ca_on.trace.placement_credit.PlacementCreditLine",
    }


# --- the decorator ---------------------------------------------------------------------------


def test_decorator_registers_an_instance_under_its_line_class(
    fresh: EnglishRendererRegistry,
) -> None:
    english_renderer(ExampleRenderer)

    assert isinstance(fresh.for_line_class(ExampleLine), ExampleRenderer)


def test_decorator_returns_the_class_unchanged(fresh: EnglishRendererRegistry) -> None:
    decorated = english_renderer(ExampleRenderer)

    assert_type(decorated, type[ExampleRenderer])

    assert decorated is ExampleRenderer


def test_decorating_a_second_renderer_for_one_line_class_fails(
    fresh: EnglishRendererRegistry,
) -> None:
    english_renderer(ExampleRenderer)

    with pytest.raises(DuplicateRegistrationError, match="ExampleLine"):
        english_renderer(OtherExampleRenderer)


# --- EnglishTraceRenderer looks renderers up -------------------------------------------------


def test_the_renderer_renders_a_line_with_the_renderer_registered_for_its_class() -> None:
    registry = EnglishRendererRegistry()
    registry.register_class(ExampleRenderer)

    renderer = EnglishTraceRenderer(registry)

    assert renderer.render(ExampleLine(D("3.50"))) == "example of 3.50"
    assert renderer.render_all((ExampleLine(D(1)), ExampleLine(D(2)))) == (
        "example of 1",
        "example of 2",
    )


def test_an_unregistered_line_class_fails_naming_it_and_the_language() -> None:
    renderer = EnglishTraceRenderer(EnglishRendererRegistry())

    with pytest.raises(TypeError, match=r"^no English rendering for trace line ExampleLine$"):
        renderer.render(ExampleLine(D(1)))


def test_a_renderer_given_a_private_registry_does_not_use_the_shared_one() -> None:
    renderer = EnglishTraceRenderer(EnglishRendererRegistry())

    with pytest.raises(TypeError, match=r"^no English rendering for trace line SumLine$"):
        renderer.render(SumLine(EX_TOTAL, (), D(1)))


def test_a_renderer_registered_in_a_private_registry_is_unknown_to_the_default_renderer() -> None:
    EnglishRendererRegistry().register_class(ExampleRenderer)

    with pytest.raises(TypeError, match=r"^no English rendering for trace line ExampleLine$"):
        EnglishTraceRenderer().render(ExampleLine(D(1)))


def test_the_default_renderer_uses_the_shared_registry(fresh: EnglishRendererRegistry) -> None:
    english_renderer(ExampleRenderer)

    assert EnglishTraceRenderer().render(ExampleLine(D(4))) == "example of 4"


# --- every core and jurisdiction line class has English text; core's sits beside its module ----

# The core and jurisdiction trace packages, imported above so that all their renderers are
# registered; where each jurisdiction's renderers live is checked under tests/jurisdictions.
TRACE_PACKAGES: tuple[ModuleType, ...] = (
    app.domain.trace,
    app.jurisdictions.ca.trace,
    app.jurisdictions.ca_on.trace,
)


def exported_line_classes() -> list[type[TraceLine]]:
    """Every TraceLine subclass the core and jurisdiction trace packages export, by name."""
    return sorted(
        {
            found
            for package in TRACE_PACKAGES
            for found in vars(package).values()
            if inspect.isclass(found) and issubclass(found, TraceLine) and found is not TraceLine
        },
        key=lambda cls: cls.__name__,
    )


@pytest.mark.parametrize("line_class", exported_line_classes(), ids=lambda cls: cls.__name__)
def test_every_exported_line_class_has_a_shared_english_renderer(
    line_class: type[TraceLine],
) -> None:
    found = EnglishRendererRegistry.shared().for_line_class(line_class)

    assert getattr(found, "line_class") is line_class  # noqa: B009
    assert callable(getattr(found, "render", None))


def core_line_classes() -> list[type[TraceLine]]:
    """Every TraceLine subclass the core trace package exports, by name."""
    return [
        cls for cls in exported_line_classes() if cls.__module__.startswith("app.domain.trace.")
    ]


@pytest.mark.parametrize("line_class", core_line_classes(), ids=lambda cls: cls.__name__)
def test_each_core_renderer_lives_in_the_adapter_module_matching_its_line_classs_module(
    line_class: type[TraceLine],
) -> None:
    # SumLine in app.domain.trace.arithmetic -> its renderer in trace_english.arithmetic.
    feature = line_class.__module__.rsplit(".", 1)[1]
    found = EnglishRendererRegistry.shared().for_line_class(line_class)

    assert type(found).__module__ == f"app.adapters.inbound.trace_english.{feature}"


def test_the_adapter_is_a_package_with_registry_and_renderer_modules() -> None:
    assert hasattr(app.adapters.inbound.trace_english, "__path__")
    assert EnglishRendererRegistry.__module__ == "app.adapters.inbound.trace_english.registry"
    assert english_renderer.__module__ == "app.adapters.inbound.trace_english.registry"
    assert EnglishTraceRenderer.__module__ == "app.adapters.inbound.trace_english.renderer"


# --- a made-up package adds a line class and its English text --------------------------------

LEVIES = "tests.adapters.inbound.rendering_fixtures.levies"


@pytest.fixture
def levies(fresh: EnglishRendererRegistry) -> Iterator[ModuleType]:
    """The made-up package's module, imported (so registered) into the fresh registry only.

    Forgotten afterwards, so the next test importing it registers it again into its own registry
    and the shared registry never holds it.
    """
    sys.modules.pop(LEVIES, None)
    yield importlib.import_module(LEVIES)
    sys.modules.pop(LEVIES, None)


def test_a_made_up_packages_line_is_rendered_with_its_own_text(
    levies: ModuleType, fresh: EnglishRendererRegistry
) -> None:
    line = levies.ExLevyLine(ArtifactKind("ex/levy", Decimal), D("12.5"))

    assert EnglishTraceRenderer(fresh).render(line) == "levy: levy of 12.5"


def test_importing_the_made_up_package_registers_its_renderer(
    levies: ModuleType, fresh: EnglishRendererRegistry
) -> None:
    found = fresh.for_line_class(levies.ExLevyLine)

    assert isinstance(found, levies.ExLevyRenderer)


def test_the_made_up_line_is_not_in_the_real_shared_registry(levies: ModuleType) -> None:
    # `fresh` stands in for `shared` here; the real shared registry was kept at import.
    with pytest.raises(UnknownRegistrationError, match="ExLevyLine"):
        REAL_SHARED.for_line_class(levies.ExLevyLine)
