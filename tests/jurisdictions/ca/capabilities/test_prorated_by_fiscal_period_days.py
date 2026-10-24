"""Unit tests for the ProratedByFiscalPeriodDays capability (`ca/prorated_by_fiscal_period_days`),
an amount prorated by the days of the fiscal period, made-up kinds.

Guide T4002 2025 and Guide T4036 2025, "Immediate expensing incentive": "The deduction is limited
to $1.5 million per tax year: ... The limit is also prorated for tax years shorter than 365 days".
Neither guide prints the arithmetic, so the proration is taken as the guides' CCA example does
("base your CCA claim on the number of days in your fiscal period compared to 365 days"): the
amount times the days of the fiscal period over the days of a full year.

Its slots: two parameter slots, `rounding` (a `rounding_only` dataset) and `class_rates` (a
`class_rates` dataset, read only for its `full_year_days`, the 365); two consumed slots, the
`Decimal` `amount` and the int `fiscal_period_days`; and one produced `Decimal` slot `output`. The
output is `rounding.apply(amount x fiscal_period_days / full_year_days)`, formed as one exact
fraction and rounded once by the dataset's rule. Days below 1 are refused
(`InputBelowBoundError`, "<kind> 0 is below the minimum 1") and days above `full_year_days` are
refused (`InputAboveBoundError`, "<kind> 366 is above the maximum 365"), as the CCA table words
them. It records one `ProratedByDaysLine` (in `app.jurisdictions.ca.trace`, next to
`FiscalPeriodDaysLine`) with the output, the amount's kind and value, the days' kind and value, the
dataset's `full_year_days` and the result, in that order.

Worked values, each worked out as an exact fraction and rounded half-up to the cent:
1500000 x 153 / 365 = 229500000 / 365 = 628767.1232..., so 628767.12 (365 x 628767 = 229499955,
remainder 45, and 45 / 365 = 0.1232...); 600000 x 153 / 365 = 91800000 / 365 = 251506.8493..., so
251506.85; 1500000 x 214 / 365 = 321000000 / 365 = 879452.0547..., so 879452.05; 1500000 x 365 /
365 = 1500000.00; 1500000 x 1 / 365 = 4109.5890..., so 4109.59; 1500000 x 153 / 366 =
229500000 / 366 = 627049.1803..., so 627049.18. Rounding once matters: rounding 1500000 / 365 to
4109.59 first and multiplying by 153 would give 628766.27.
"""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping
from decimal import Decimal
from types import MappingProxyType
from typing import assert_type, cast

import pytest

import app.jurisdictions.ca.capabilities as ca_capabilities
from app.domain.artifact import Artifact, ArtifactKind, Money
from app.domain.capability import CapabilityRegistry
from app.domain.errors import (
    InputAboveBoundError,
    InputBelowBoundError,
    InvalidCapabilityError,
    MissingArtifactError,
)
from app.domain.parameters.class_rates import CLASS_RATES
from app.domain.parameters.datasets import ParameterDataset
from app.domain.parameters.rounding import NO_ROUNDING, RoundingMode, RoundingRule, RoundTo
from app.domain.parameters.rounding_only import ROUNDING_ONLY, RoundingOnly
from app.jurisdictions.ca.capabilities.prorated_by_fiscal_period_days import (
    ProratedByFiscalPeriodDays,
)
from app.jurisdictions.ca.trace import ProratedByDaysLine
from tests.jurisdictions.ca.capabilities.cca_table import class_rates

D = Decimal
CENT = RoundTo(D("0.01"), RoundingMode.HALF_UP)
DOLLAR = RoundTo(D("1"), RoundingMode.HALF_UP)

LIMIT = ArtifactKind("ex/limit", Decimal)
DAYS = ArtifactKind("ex/fiscal_period_days", int)
PRORATED = ArtifactKind("ex/limit_prorated", Decimal)


def rounding(rule: RoundingRule = CENT) -> ParameterDataset[RoundingOnly]:
    """By default half-up to the cent."""
    return ParameterDataset(
        "ex/limit_rounding",
        2025,
        ROUNDING_ONLY,
        RoundingOnly(),
        rule,
        ("https://example.org/rounding",),
    )


def capability(rule: RoundingRule = CENT, full_year_days: int = 365) -> ProratedByFiscalPeriodDays:
    return ProratedByFiscalPeriodDays(
        rounding(rule), class_rates(full_year_days=full_year_days), LIMIT, DAYS, PRORATED
    )


def inputs(amount: str, days: int) -> tuple[Artifact[Decimal] | Artifact[int], ...]:
    return (Artifact(LIMIT, D(amount)), Artifact(DAYS, days))


def prorated(
    amount: str, days: int, rule: RoundingRule = CENT, full_year_days: int = 365
) -> Decimal:
    (output,) = capability(rule, full_year_days).compute(inputs(amount, days)).outputs
    assert isinstance(output.value, Decimal)
    return output.value


def test_is_registered_as_ca_prorated_by_fiscal_period_days() -> None:
    registered = CapabilityRegistry.shared().get("ca/prorated_by_fiscal_period_days")

    assert registered is ProratedByFiscalPeriodDays


def test_is_exported_from_the_ca_capabilities_package() -> None:
    assert "prorated_by_fiscal_period_days" in ca_capabilities.__all__
    assert (
        ca_capabilities.prorated_by_fiscal_period_days.ProratedByFiscalPeriodDays
        is ProratedByFiscalPeriodDays
    )


def test_declares_its_contract() -> None:
    assert capability().consumes == frozenset({LIMIT, DAYS})
    assert capability().produces == frozenset({PRORATED})


def test_leaves_its_contract_to_the_base() -> None:
    assert "consumes" not in vars(ProratedByFiscalPeriodDays)
    assert "produces" not in vars(ProratedByFiscalPeriodDays)


def test_declares_its_slots() -> None:
    assert ProratedByFiscalPeriodDays.PARAMETERS == {
        "rounding": ROUNDING_ONLY,
        "class_rates": CLASS_RATES,
    }
    assert ProratedByFiscalPeriodDays.CONSUMES == {"amount": Decimal, "fiscal_period_days": int}
    assert ProratedByFiscalPeriodDays.PRODUCES == {"output": Decimal}


def test_its_slots_are_read_only() -> None:
    for each in (
        ProratedByFiscalPeriodDays.PARAMETERS,
        ProratedByFiscalPeriodDays.CONSUMES,
        ProratedByFiscalPeriodDays.PRODUCES,
    ):
        assert isinstance(each, MappingProxyType)
        with pytest.raises(TypeError):
            cast("MutableMapping[str, object]", each)["extra"] = int


def test_its_consumed_and_produced_slots_are_typed_as_read_only_mappings() -> None:
    assert_type(ProratedByFiscalPeriodDays.CONSUMES, Mapping[str, type])
    assert_type(ProratedByFiscalPeriodDays.PRODUCES, Mapping[str, type])


def test_is_built_from_its_slot_names_as_keywords() -> None:
    wired = ProratedByFiscalPeriodDays(
        rounding=rounding(),
        class_rates=class_rates(),
        amount=LIMIT,
        fiscal_period_days=DAYS,
        output=PRORATED,
    )

    (output,) = wired.compute(inputs("1500000", 153)).outputs
    assert output == Artifact(PRORATED, D("628767.12"))


def test_rejects_an_int_kind_for_the_amount() -> None:
    int_kind = cast("Money", ArtifactKind("ex/count", int))

    with pytest.raises(InvalidCapabilityError, match="ProratedByFiscalPeriodDays.*'amount'"):
        ProratedByFiscalPeriodDays(rounding(), class_rates(), int_kind, DAYS, PRORATED)


def test_rejects_a_money_kind_for_the_days() -> None:
    money_kind = cast("ArtifactKind[int]", ArtifactKind("ex/money", Decimal))

    with pytest.raises(
        InvalidCapabilityError, match="ProratedByFiscalPeriodDays.*'fiscal_period_days'"
    ):
        ProratedByFiscalPeriodDays(rounding(), class_rates(), LIMIT, money_kind, PRORATED)


def test_rejects_one_kind_as_both_amount_and_output() -> None:
    with pytest.raises(InvalidCapabilityError, match="ProratedByFiscalPeriodDays") as raised:
        ProratedByFiscalPeriodDays(rounding(), class_rates(), LIMIT, DAYS, LIMIT)

    assert "'amount'" in str(raised.value)
    assert "'output'" in str(raised.value)


@pytest.mark.parametrize(
    ("amount", "days", "expected"),
    [
        # A 153-day fiscal period of the $1.5 million.
        ("1500000", 153, "628767.12"),
        # The same period of a 40% share of the $1.5 million.
        ("600000", 153, "251506.85"),
        # June 1 to December 31, 2025 is 214 days.
        ("1500000", 214, "879452.05"),
        # A full year is not prorated.
        ("1500000", 365, "1500000.00"),
        ("600000", 365, "600000.00"),
        ("1500000", 1, "4109.59"),
        ("0", 153, "0.00"),
        # An amount of 0 stays 0 for the days of a full year.
        ("0", 365, "0.00"),
        # 1.825 x 1 / 365 = 0.005, a tie, rounds up to 0.01.
        ("1.825", 1, "0.01"),
    ],
)
def test_multiplies_by_the_days_over_a_full_year_and_rounds_once(
    amount: str, days: int, expected: str
) -> None:
    assert prorated(amount, days) == D(expected)


def test_rounds_once_not_the_daily_amount_first() -> None:
    # 1500000 / 365 = 4109.59 to the cent, and 4109.59 x 153 = 628766.27, which is not the answer.
    assert prorated("1500000", 153) == D("628767.12")
    assert prorated("1500000", 153) != D("628766.27")


def test_the_dataset_decides_the_rounding() -> None:
    assert prorated("1500000", 153, DOLLAR) == D("628767")


def test_under_no_rounding_a_product_that_is_exact_stays_exact() -> None:
    # 36500 x 73 / 365 = 7300, exact, with no rounding rule to apply.
    assert prorated("36500", 73, NO_ROUNDING) == D("7300")


def test_a_dataset_of_366_days_prorates_by_366() -> None:
    assert prorated("1500000", 153, full_year_days=366) == D("627049.18")
    assert prorated("1500000", 366, full_year_days=366) == D("1500000.00")


def test_the_output_is_a_decimal_of_the_produced_kind() -> None:
    (output,) = capability().compute(inputs("1500000", 153)).outputs

    assert output.kind == PRORATED
    assert type(output.value) is Decimal


def test_zero_days_are_refused_naming_the_kind_and_the_minimum() -> None:
    with pytest.raises(InputBelowBoundError) as raised:
        prorated("1500000", 0)

    assert str(raised.value) == "ex/fiscal_period_days 0 is below the minimum 1"


def test_negative_days_are_refused() -> None:
    with pytest.raises(InputBelowBoundError) as raised:
        prorated("1500000", -1)

    assert str(raised.value) == "ex/fiscal_period_days -1 is below the minimum 1"


def test_366_days_are_refused_naming_the_kind_and_the_maximum() -> None:
    with pytest.raises(InputAboveBoundError) as raised:
        prorated("1500000", 366)

    assert str(raised.value) == "ex/fiscal_period_days 366 is above the maximum 365"


def test_a_dataset_of_366_days_refuses_367_days() -> None:
    with pytest.raises(InputAboveBoundError) as raised:
        prorated("1500000", 367, full_year_days=366)

    assert str(raised.value) == "ex/fiscal_period_days 367 is above the maximum 366"


@pytest.mark.parametrize("days", [1, 365])
def test_the_days_at_the_bounds_are_allowed(days: int) -> None:
    assert prorated("365", days) == D(days)


@pytest.mark.parametrize("missing", [0, 1])
def test_a_missing_consumed_artifact_is_a_missing_artifact(missing: int) -> None:
    given = tuple(a for i, a in enumerate(inputs("1500000", 153)) if i != missing)

    with pytest.raises(MissingArtifactError):
        capability().compute(given)


def test_traces_one_prorated_by_days_line() -> None:
    result = capability().compute(inputs("1500000", 153))

    assert result.trace == (
        ProratedByDaysLine(PRORATED, LIMIT, D("1500000"), DAYS, 153, 365, D("628767.12")),
    )


def test_the_line_carries_the_full_year_of_the_dataset() -> None:
    result = capability(full_year_days=366).compute(inputs("1500000", 153))

    assert result.trace == (
        ProratedByDaysLine(PRORATED, LIMIT, D("1500000"), DAYS, 153, 366, D("627049.18")),
    )
