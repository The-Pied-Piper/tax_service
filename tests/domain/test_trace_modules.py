"""Unit tests for the layout of the `app.domain.trace` package: each line class's home module.

The line classes live in one module per feature group, each with an `__all__`; the package
`__init__` re-exports every module's `__all__`, so `from app.domain.trace import SumLine` keeps
working. Every exported line class appears in `HOMES`, so a new one is placed deliberately.
"""

from __future__ import annotations

import importlib
import inspect

import pytest

import app.domain.trace
from app.domain.trace import TraceLine

HOMES: dict[str, tuple[str, ...]] = {
    "base": ("TraceLine",),
    "arithmetic": (
        "RoundedTotalLine",
        "SumLine",
        "SumNotBelowZeroLine",
        "RateAppliedLine",
        "SubtractedLine",
        "SubtractedNotBelowZeroLine",
        "CreditAmountLine",
        "CappedAmountLine",
        "LesserOfLine",
        "GreaterOfLine",
        "PerUnitAmountLine",
        "MultipleOverLine",
        "AtMostLine",
        "FractionAppliedLine",
        "RatioAppliedLine",
        "TimesCountLine",
        "QuotientLine",
        "ThresholdGateLine",
        "AmountOrDividedByRateLine",
    ),
    "rate_tables": (
        "BracketColumnLine",
        "ContributionTierLine",
        "SurchargeTierLine",
        "TaperedAmountLine",
        "RateByIncomeBandLine",
        "ChosenRateAppliedLine",
        "AmountByCountLine",
    ),
    "choices": ("ChosenByCountLine", "ChosenByRangeLine", "ConditionLine", "ConditionsCountLine"),
    "record_lists": (
        "RecordTotalLine",
        "RecordCountLine",
        "ItemsTotalLine",
        "ItemSumLine",
        "ItemLesserOfLine",
    ),
    "dependants": (
        "CaregiverClaimLine",
        "CaregiverClaimLessClaimedLine",
        "OtherDependantMedicalLine",
        "DisabilityTransferLine",
    ),
    "placement_credit": ("PlacementCreditLine",),
    "rentals": ("ShortTermRentalNonCompliantLine",),
    "gains": ("PrincipalResidenceGainLine", "DispositionGainLine", "DispositionGainOnlyLine"),
    "capital_cost": (
        "CcaZeroReason",
        "CcaClaimLine",
        "RecapturedCcaLine",
        "TerminalLossLine",
        "ClosingUccLine",
    ),
}

PLACED = [(module, name) for module, names in HOMES.items() for name in names]


def test_trace_is_a_package() -> None:
    assert hasattr(app.domain.trace, "__path__")


@pytest.mark.parametrize(("module", "name"), PLACED, ids=[name for _, name in PLACED])
def test_each_class_lives_in_its_feature_module(module: str, name: str) -> None:
    home = importlib.import_module(f"app.domain.trace.{module}")

    assert getattr(home, name).__module__ == f"app.domain.trace.{module}"
    assert name in home.__all__


@pytest.mark.parametrize(("module", "name"), PLACED, ids=[name for _, name in PLACED])
def test_the_package_re_exports_each_class(module: str, name: str) -> None:
    home = importlib.import_module(f"app.domain.trace.{module}")

    assert getattr(app.domain.trace, name) is getattr(home, name)


@pytest.mark.parametrize("module", list(HOMES))
def test_each_feature_module_exports_exactly_its_classes(module: str) -> None:
    home = importlib.import_module(f"app.domain.trace.{module}")

    assert set(home.__all__) == set(HOMES[module])


def test_every_exported_line_class_is_placed() -> None:
    exported = {
        name
        for name, found in vars(app.domain.trace).items()
        if inspect.isclass(found) and issubclass(found, TraceLine)
    }

    assert exported == {name for _, name in PLACED if name != "CcaZeroReason"}


def test_the_package_exports_every_placed_name() -> None:
    assert set(app.domain.trace.__all__) == {name for _, name in PLACED}
