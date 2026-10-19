"""The 2025 Ontario fertility and seniors' transit credit figures, checked against CRA's ON479.

2025 Form ON479 (form 5006-TC), "Ontario fertility treatment tax credit": "Line 1 and line 61268:
Eligible medical expenses for fertility treatment multiplied by 25% (maximum $5,000) ="; "Ontario
seniors' public transit tax credit": "Line 14: Amount paid in the year for eligible seniors' use
of Ontario public transit services (maximum $3,000) Line 63100 multiplied by 15% =". The form
prints the fertility maximum after the rate, so it caps the credit; it prints the transit maximum
before the rate, so it caps the amount paid. Each percentage is a rate (the `rate` kind) and each
maximum a plain cap (the `amount` kind). Lines 1 and 14 are dollars-and-cents boxes, so each is
rounded half-up to the cent.
"""

from __future__ import annotations

from decimal import Decimal

import pytest

import app.registrations
from app.adapters.outbound.yaml_parameters import YamlParameterSource
from app.domain.artifact import Artifact, ArtifactKind
from app.domain.capabilities.apply_rate import ApplyRate
from app.domain.capabilities.capped_amount import CappedAmount
from app.domain.parameters.amount import AMOUNT, Amount
from app.domain.parameters.rate import RATE, Rate
from app.domain.parameters.rounding import RoundingMode, RoundTo

D = Decimal
SOURCE = YamlParameterSource(app.registrations.JURISDICTIONS.roots())
FERTILITY_RATE = "ca-on/fertility_credit_rate"
FERTILITY_MAXIMUM = "ca-on/fertility_credit_maximum"
TRANSIT_MAXIMUM = "ca-on/seniors_transit_maximum"
TRANSIT_RATE = "ca-on/seniors_transit_rate"
ON479_TEXT = "https://www.canada.ca/content/dam/cra-arc/formspubs/pbg/5006-tc/5006-tc-25e.txt"

# Made up for this test and not registered: the amounts the rates and maximums are applied to
# and the results.
EXPENSES = ArtifactKind("ex/expenses", Decimal)
BEFORE_MAXIMUM = ArtifactKind("ex/before_maximum", Decimal)
CAPPED = ArtifactKind("ex/capped", Decimal)
PAID = ArtifactKind("ex/paid", Decimal)
CREDIT = ArtifactKind("ex/credit", Decimal)
CENT = RoundTo(D("0.01"), RoundingMode.HALF_UP)


def test_2025_fertility_rate_is_25_percent() -> None:
    data = SOURCE.get(FERTILITY_RATE, 2025, RATE)

    assert data.values == Rate(D("0.25"))
    # ON479 line 1, a dollars-and-cents box: half-up to the cent.
    assert data.rounding == CENT


def test_2025_fertility_maximum_is_5000() -> None:
    data = SOURCE.get(FERTILITY_MAXIMUM, 2025, AMOUNT)

    assert data.values == Amount(D("5000"))
    # ON479 line 1, a dollars-and-cents box: half-up to the cent.
    assert data.rounding == CENT


def test_2025_transit_maximum_is_3000() -> None:
    data = SOURCE.get(TRANSIT_MAXIMUM, 2025, AMOUNT)

    assert data.values == Amount(D("3000"))
    # ON479 line 14, a dollars-and-cents box: half-up to the cent.
    assert data.rounding == CENT


def test_2025_transit_rate_is_15_percent() -> None:
    data = SOURCE.get(TRANSIT_RATE, 2025, RATE)

    assert data.values == Rate(D("0.15"))
    # ON479 line 14, a dollars-and-cents box: half-up to the cent.
    assert data.rounding == CENT


def test_2025_datasets_cite_only_the_on479_text() -> None:
    assert SOURCE.get(FERTILITY_RATE, 2025, RATE).sources == (ON479_TEXT,)
    assert SOURCE.get(FERTILITY_MAXIMUM, 2025, AMOUNT).sources == (ON479_TEXT,)
    assert SOURCE.get(TRANSIT_MAXIMUM, 2025, AMOUNT).sources == (ON479_TEXT,)
    assert SOURCE.get(TRANSIT_RATE, 2025, RATE).sources == (ON479_TEXT,)


@pytest.mark.parametrize(
    ("expenses", "credit"),
    [
        # Return G: 24000 x 25% = 6000, before the maximum.
        ("24000", "6000.00"),
        # Below the maximum: 12000 x 25% = 3000.
        ("12000", "3000.00"),
        # Returns A to G's other cases and the edges.
        ("0", "0"),
        ("20000", "5000.00"),
        # 1000.01 x 25% = 250.0025, rounded half-up to 250.00; 1000.02 x 25% = 250.005, a tie,
        # up to 250.01.
        ("1000.01", "250.00"),
        ("1000.02", "250.01"),
    ],
)
def test_25_percent_of_the_fertility_expenses(expenses: str, credit: str) -> None:
    capability = ApplyRate(SOURCE.get(FERTILITY_RATE, 2025, RATE), EXPENSES, BEFORE_MAXIMUM)

    result = capability.compute((Artifact(EXPENSES, D(expenses)),))

    assert result.outputs == (Artifact(BEFORE_MAXIMUM, D(credit)),)


@pytest.mark.parametrize(
    ("credit", "capped"),
    [
        # Return G: 6000.00 is above the maximum.
        ("6000.00", "5000"),
        # At the maximum, and a cent above it.
        ("5000", "5000"),
        ("5000.01", "5000"),
        # Below it, the credit itself.
        ("3000.00", "3000.00"),
        ("0", "0"),
    ],
)
def test_the_fertility_credit_is_at_most_5000(credit: str, capped: str) -> None:
    capability = CappedAmount(SOURCE.get(FERTILITY_MAXIMUM, 2025, AMOUNT), BEFORE_MAXIMUM, CAPPED)

    result = capability.compute((Artifact(BEFORE_MAXIMUM, D(credit)),))

    assert result.outputs == (Artifact(CAPPED, D(capped)),)


@pytest.mark.parametrize(
    ("paid", "capped"),
    [
        # Return G: 1200 is below the maximum.
        ("1200", "1200"),
        # At the maximum, and a cent above it.
        ("3000", "3000"),
        ("3000.01", "3000"),
        # Paid above the maximum: 3500 counts as 3000.
        ("3500", "3000"),
        ("0", "0"),
    ],
)
def test_the_transit_amount_paid_is_at_most_3000(paid: str, capped: str) -> None:
    capability = CappedAmount(SOURCE.get(TRANSIT_MAXIMUM, 2025, AMOUNT), PAID, CAPPED)

    result = capability.compute((Artifact(PAID, D(paid)),))

    assert result.outputs == (Artifact(CAPPED, D(capped)),)


@pytest.mark.parametrize(
    ("amount", "credit"),
    [
        # Return G: 1200 x 15% = 180.
        ("1200", "180.00"),
        # 3500 paid is capped at 3000 first: 3000 x 15% = 450.
        ("3000", "450.00"),
        ("0", "0"),
        # 0.03 x 15% = 0.0045, rounded half-up to 0.00; 0.10 x 15% = 0.015, a tie, up to 0.02.
        ("0.03", "0.00"),
        ("0.10", "0.02"),
    ],
)
def test_15_percent_of_the_transit_amount(amount: str, credit: str) -> None:
    capability = ApplyRate(SOURCE.get(TRANSIT_RATE, 2025, RATE), CAPPED, CREDIT)

    result = capability.compute((Artifact(CAPPED, D(amount)),))

    assert result.outputs == (Artifact(CREDIT, D(credit)),)


def test_transit_paid_3500_gives_450_through_the_cap_then_the_rate() -> None:
    cap = CappedAmount(SOURCE.get(TRANSIT_MAXIMUM, 2025, AMOUNT), PAID, CAPPED)
    rate = ApplyRate(SOURCE.get(TRANSIT_RATE, 2025, RATE), CAPPED, CREDIT)

    capped = cap.compute((Artifact(PAID, D("3500")),))
    result = rate.compute(capped.outputs)

    assert result.outputs == (Artifact(CREDIT, D("450.00")),)
