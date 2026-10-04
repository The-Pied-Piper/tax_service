"""2025 federal and Ontario bracket data, checked against CRA's published figures.

Sources are listed in each dataset file. The fixed-tax amounts are the constants
printed on the 2025 T1 return (lines 71-75) and Form ON428 (Part A, lines 3-7),
which CRA shows rounded to the cent.
"""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

import pytest

from app.adapters.outbound.yaml_parameters import YamlParameterSource
from app.domain.artifact import Artifact
from app.domain.capabilities.progressive_tax import ProgressiveTax
from app.domain.rounding import NO_ROUNDING, RoundingMode, RoundTo

D = Decimal
PARAMETERS = Path(__file__).resolve().parents[3] / "data" / "parameters"
SOURCE = YamlParameterSource(PARAMETERS)
TO_CENT = RoundTo(D("0.01"), RoundingMode.HALF_UP)

FEDERAL_FIXED_TAX = {  # 2025 T1, line 71 threshold -> line 75 fixed tax
    "57375": "8319.38",
    "114750": "20081.25",
    "177882": "36495.57",
    "253414": "58399.85",
}
ONTARIO_FIXED_TAX = {  # 2025 ON428 Part A, line 3 threshold -> line 7 fixed tax
    "52886": "2670.74",
    "105775": "7510.09",
    "150000": "12445.60",
    "220000": "20957.60",
}


def test_federal_2025_brackets() -> None:
    data = SOURCE.get_brackets("ca/brackets", 2025)

    assert [(b.lower, b.rate) for b in data.schedule.brackets] == [
        (D("0"), D("0.145")),
        (D("57375"), D("0.205")),
        (D("114750"), D("0.26")),
        (D("177882"), D("0.29")),
        (D("253414"), D("0.33")),
    ]
    assert data.rounding == NO_ROUNDING  # CRA states no rounding rule for these lines
    assert data.sources


def test_ontario_2025_brackets() -> None:
    data = SOURCE.get_brackets("ca-on/brackets", 2025)

    assert [(b.lower, b.rate) for b in data.schedule.brackets] == [
        (D("0"), D("0.0505")),
        (D("52886"), D("0.0915")),
        (D("105775"), D("0.1116")),
        (D("150000"), D("0.1216")),
        (D("220000"), D("0.1316")),
    ]
    assert data.rounding == NO_ROUNDING
    assert data.sources


@pytest.mark.parametrize(
    ("family", "threshold", "fixed_tax"),
    [("ca/brackets", t, f) for t, f in FEDERAL_FIXED_TAX.items()]
    + [("ca-on/brackets", t, f) for t, f in ONTARIO_FIXED_TAX.items()],
)
def test_reproduces_the_fixed_tax_printed_on_the_form(
    family: str, threshold: str, fixed_tax: str
) -> None:
    schedule = SOURCE.get_brackets(family, 2025).schedule

    assert TO_CENT.apply(schedule.tax_on(D(threshold))) == D(fixed_tax)


@pytest.mark.parametrize(
    ("taxable_income", "federal_basic_tax"),
    [
        ("10000", "1450"),  # CRA "Completing a basic tax return": Giovanni
        ("115000", "20146.25"),  # same page, Maria: 8,319 + 11,762 + 65 rounded per line
    ],
)
def test_matches_cra_worked_examples(taxable_income: str, federal_basic_tax: str) -> None:
    data = SOURCE.get_brackets("ca/brackets", 2025)
    base, tax = Artifact("taxable_income"), Artifact("federal_basic_tax")

    result = ProgressiveTax(base, tax, data.schedule, data.rounding).run({base: D(taxable_income)})

    assert result.outputs[tax] == D(federal_basic_tax)
