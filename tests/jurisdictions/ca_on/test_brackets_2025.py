"""2025 federal and Ontario bracket data, checked against CRA's published figures.

Sources are listed in each dataset file. Each bracket carries the form's printed column: its lower
bound, its rate and the constant printed for it, the tax at the bracket's start in dollars and
cents (2025 T1, Step 5, Part A, lines 71, 73 and 75; Form ON428, Part A, lines 3, 5 and 7). The
tax on taxable income is "Line 72 multiplied by the percentage from line 73" plus line 75 (T1),
or line 6 plus line 7 (ON428), for the column the income falls in; an income exactly at a column's
upper bound falls in that column ("more than ... but not more than ...").
"""

from __future__ import annotations

from decimal import Decimal

import pytest

import app.registrations
from app.adapters.outbound.yaml_parameters import YamlParameterSource
from app.domain.artifact import Artifact
from app.domain.capabilities.progressive_tax import ProgressiveTax
from app.domain.parameters.brackets import BRACKETS
from app.domain.parameters.rounding import NO_ROUNDING
from app.jurisdictions.ca.catalog import FEDERAL_BASIC_TAX, TAXABLE_INCOME

D = Decimal
SOURCE = YamlParameterSource(app.registrations.JURISDICTIONS.roots())

FEDERAL_SOURCES = (
    "https://www.canada.ca/en/revenue-agency/services/tax/individuals/tax-rates-brackets/last-year.html",
    "https://www.canada.ca/content/dam/cra-arc/formspubs/pbg/5000-r/5000-r-25e.txt",
    "https://www.canada.ca/en/department-finance/news/2025/05/delivering-a-middle-class-tax-cut.html",
)
ONTARIO_SOURCES = (
    "https://www.canada.ca/en/revenue-agency/services/tax/individuals/tax-rates-brackets/last-year.html",
    "https://www.canada.ca/content/dam/cra-arc/formspubs/pbg/5006-c/5006-c-25e.txt",
    "https://data.ontario.ca/en/dataset/personal-income-tax-rates-and-credits/resource/60f84727-7e12-4fd4-ba06-30955d31b2ae",
)


def test_federal_2025_brackets() -> None:
    data = SOURCE.get("ca/brackets", 2025, BRACKETS)

    # 2025 T1, Step 5, Part A: line 71 lower bound, line 73 rate, line 75 printed constant.
    assert [(b.lower, b.rate, b.tax_at_start) for b in data.values.brackets] == [
        (D("0"), D("0.145"), D("0.00")),
        (D("57375"), D("0.205"), D("8319.38")),
        (D("114750"), D("0.26"), D("20081.25")),
        (D("177882"), D("0.29"), D("36495.57")),
        (D("253414"), D("0.33"), D("58399.85")),
    ]
    assert data.rounding == NO_ROUNDING  # CRA states no rounding rule for lines 74 or 76
    assert data.sources == FEDERAL_SOURCES


def test_ontario_2025_brackets() -> None:
    data = SOURCE.get("ca-on/brackets", 2025, BRACKETS)

    # 2025 ON428, Part A: line 3 lower bound, line 5 rate, line 7 printed constant.
    assert [(b.lower, b.rate, b.tax_at_start) for b in data.values.brackets] == [
        (D("0"), D("0.0505"), D("0.00")),
        (D("52886"), D("0.0915"), D("2670.74")),
        (D("105775"), D("0.1116"), D("7510.09")),
        (D("150000"), D("0.1216"), D("12445.60")),
        (D("220000"), D("0.1316"), D("20957.60")),
    ]
    assert data.rounding == NO_ROUNDING  # CRA states no rounding rule for lines 6 or 8
    assert data.sources == ONTARIO_SOURCES


def test_the_printed_constants_are_held_to_the_cent() -> None:
    for family in ("ca/brackets", "ca-on/brackets"):
        brackets = SOURCE.get(family, 2025, BRACKETS).values.brackets
        assert all(b.tax_at_start.as_tuple().exponent == -2 for b in brackets)


@pytest.mark.parametrize(
    ("family", "income", "tax"),
    [
        # An income at a column's upper bound falls in that column: its rate on the excess
        # over the column's lower bound, plus the column's printed constant.
        ("ca/brackets", "57375", "8319.375"),  # 14.5% x 57,375 + 0.00
        ("ca/brackets", "114750", "20081.255"),  # 20.5% x 57,375 + 8,319.38
        ("ca/brackets", "177882", "36495.57"),  # 26% x 63,132 + 20,081.25
        ("ca/brackets", "253414", "58399.85"),  # 29% x 75,532 + 36,495.57
        ("ca-on/brackets", "52886", "2670.743"),  # 5.05% x 52,886 + 0.00
        ("ca-on/brackets", "105775", "7510.0835"),  # 9.15% x 52,889 + 2,670.74
        ("ca-on/brackets", "150000", "12445.60"),  # 11.16% x 44,225 + 7,510.09
        ("ca-on/brackets", "220000", "20957.60"),  # 12.16% x 70,000 + 12,445.60
    ],
)
def test_an_income_at_a_threshold_is_taxed_in_the_lower_column(
    family: str, income: str, tax: str
) -> None:
    schedule = SOURCE.get(family, 2025, BRACKETS).values

    assert schedule.tax_on(D(income)) == D(tax)


@pytest.mark.parametrize(
    ("family", "income", "tax"),
    [
        # Just above a threshold: the next column's printed constant, plus its rate on a cent.
        ("ca/brackets", "57375.01", "8319.38205"),  # 20.5% x 0.01 + 8,319.38
        ("ca-on/brackets", "105775.01", "7510.091116"),  # 11.16% x 0.01 + 7,510.09
    ],
)
def test_an_income_above_a_threshold_starts_from_the_next_columns_constant(
    family: str, income: str, tax: str
) -> None:
    schedule = SOURCE.get(family, 2025, BRACKETS).values

    assert schedule.tax_on(D(income)) == D(tax)


@pytest.mark.parametrize(
    ("taxable_income", "federal_basic_tax"),
    [
        ("10000", "1450"),  # CRA "Completing a basic tax return": Giovanni
        ("115000", "20146.25"),  # same page, Maria: 26% x 250 + 20,081.25
    ],
)
def test_matches_cra_worked_examples(taxable_income: str, federal_basic_tax: str) -> None:
    schedule = SOURCE.get("ca/brackets", 2025, BRACKETS)
    capability = ProgressiveTax(TAXABLE_INCOME, FEDERAL_BASIC_TAX, schedule)

    result = capability.compute((Artifact(TAXABLE_INCOME, D(taxable_income)),))

    assert result.outputs == (Artifact(FEDERAL_BASIC_TAX, D(federal_basic_tax)),)
