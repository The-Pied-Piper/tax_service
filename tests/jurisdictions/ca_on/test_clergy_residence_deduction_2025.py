"""The 2025 figures of the clergy residence deduction, checked against Form T1223 Part C.

T1 2025 (form 5006-R) line 51 and line 23100 "Clergy residence deduction (complete Form T1223)"
and Form T1223 (2025) Part C, line 2 "Amount from line 1 multiplied by 1/3", line 4 "Line 3
multiplied by $1,000 (maximum $10,000)" and the maximum of $10,000 on the same line. The one-third
is not a finite decimal, so it is a `fraction`; the $1,000 per month and the $10,000 maximum are
dollars-and-cents `amount`s, taken as printed. Line 2 and line 4 are dollars-and-cents boxes, so
the fraction and the per-month amount round half-up to the cent, the owner's decision, as the form
states no rounding rule.
"""

from __future__ import annotations

from decimal import Decimal

import pytest

import app.registrations
from app.adapters.outbound.yaml_parameters import YamlParameterSource
from app.domain.artifact import Artifact, ArtifactKind
from app.domain.capabilities.apply_fraction import ApplyFraction
from app.domain.capabilities.capped_amount import CappedAmount
from app.domain.capabilities.per_unit_amount import PerUnitAmount
from app.domain.parameters.amount import AMOUNT, Amount
from app.domain.parameters.fraction import FRACTION, Fraction
from app.domain.parameters.rounding import RoundingMode, RoundTo

D = Decimal
SOURCE = YamlParameterSource(app.registrations.JURISDICTIONS.roots())
ONE_THIRD = "ca/clergy_residence_fraction"
PER_MONTH = "ca/clergy_residence_per_month"
MONTHS_MAXIMUM = "ca/clergy_residence_months_maximum"
T1223_PDF = "https://www.canada.ca/content/dam/cra-arc/formspubs/pbg/t1223/t1223-25e.pdf"

# Made up for this test and not registered: the income, the months and the amounts they give.
INCOME = ArtifactKind("ex/qualifying_income", Decimal)
LINE_2 = ArtifactKind("ex/line_2", Decimal)
MONTHS = ArtifactKind("ex/months", int)
MONTHS_AMOUNT = ArtifactKind("ex/months_amount", Decimal)
LINE_4 = ArtifactKind("ex/line_4", Decimal)


def test_2025_the_one_third_fraction_is_one_over_three() -> None:
    data = SOURCE.get(ONE_THIRD, 2025, FRACTION)

    # Line 2 "Amount from line 1 multiplied by 1/3".
    assert data.values == Fraction(1, 3)
    # Line 2, a dollars-and-cents box: half-up to the cent.
    assert data.rounding == RoundTo(D("0.01"), RoundingMode.HALF_UP)


def test_2025_the_per_month_amount_is_1000() -> None:
    data = SOURCE.get(PER_MONTH, 2025, AMOUNT)

    # Line 4 "Line 3 multiplied by $1,000".
    assert data.values == Amount(D("1000"))
    assert data.rounding == RoundTo(D("0.01"), RoundingMode.HALF_UP)


def test_2025_the_months_maximum_is_10000() -> None:
    data = SOURCE.get(MONTHS_MAXIMUM, 2025, AMOUNT)

    # Line 4 "(maximum $10,000)".
    assert data.values == Amount(D("10000"))
    assert data.rounding == RoundTo(D("0.01"), RoundingMode.HALF_UP)


def test_2025_the_datasets_cite_only_the_t1223_form() -> None:
    assert SOURCE.get(ONE_THIRD, 2025, FRACTION).sources == (T1223_PDF,)
    assert SOURCE.get(PER_MONTH, 2025, AMOUNT).sources == (T1223_PDF,)
    assert SOURCE.get(MONTHS_MAXIMUM, 2025, AMOUNT).sources == (T1223_PDF,)


@pytest.mark.parametrize(
    ("income", "line_2"),
    [
        # Line 1 45000 (the worked example): 45000 / 3 = 15000.
        ("45000", "15000.00"),
        # Line 1 8000: 8000 / 3 = 2666.666..., rounded half-up to the cent.
        ("8000", "2666.67"),
        ("30000", "10000.00"),
        ("0", "0"),
    ],
)
def test_line_2_is_one_third_of_the_income_from_qualifying_employment(
    income: str, line_2: str
) -> None:
    capability = ApplyFraction(SOURCE.get(ONE_THIRD, 2025, FRACTION), INCOME, LINE_2)

    result = capability.compute((Artifact(INCOME, D(income)),))

    assert result.outputs == (Artifact(LINE_2, D(line_2)),)


@pytest.mark.parametrize(
    ("months", "amount"),
    [(12, "12000"), (3, "3000"), (1, "1000"), (0, "0")],
)
def test_line_4_is_1000_for_each_month_of_qualifying_employment(months: int, amount: str) -> None:
    capability = PerUnitAmount(SOURCE.get(PER_MONTH, 2025, AMOUNT), MONTHS, MONTHS_AMOUNT)

    result = capability.compute((Artifact(MONTHS, months),))

    assert result.outputs == (Artifact(MONTHS_AMOUNT, D(amount)),)


@pytest.mark.parametrize(
    ("base", "capped"),
    [
        # Twelve months is 12000, capped at 10000 (line 4 of the worked example).
        ("12000", "10000.00"),
        ("10000", "10000.00"),
        ("9000", "9000"),
        ("0", "0"),
    ],
)
def test_line_4_is_capped_at_the_maximum(base: str, capped: str) -> None:
    capability = CappedAmount(SOURCE.get(MONTHS_MAXIMUM, 2025, AMOUNT), MONTHS_AMOUNT, LINE_4)

    result = capability.compute((Artifact(MONTHS_AMOUNT, D(base)),))

    assert result.outputs == (Artifact(LINE_4, D(capped)),)
