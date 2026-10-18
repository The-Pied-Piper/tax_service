"""The 2025 Ontario health premium tiers, checked against CRA's ON428.

2025 ON428 (form 5006-C), line 89 "Ontario health premium (complete the chart below)"; the chart's
line 1 is "Enter your taxable income from line 26000 of your return", and by taxable income:
$20,000 or less: $0; more than $20,000 but not more than $25,000: (taxable income − $20,000) × 6%;
more than $25,000 but not more than $36,000: $300; more than $36,000 but not more than $38,500:
(taxable income − $36,000) × 6% + $300; more than $38,500 but not more than $48,000: $450; more
than $48,000 but not more than $48,600: (taxable income − $48,000) × 25% + $450; more than $48,600
but not more than $72,000: $600; more than $72,000 but not more than $72,600: (taxable income −
$72,000) × 25% + $600; more than $72,600 but not more than $200,000: $750; more than $200,000 but
not more than $200,600: (taxable income − $200,000) × 25% + $750; more than $200,600: $900. Each
row is the previous plateau plus a rate on the income over the row's threshold, capped at the
next plateau, so each sloped row is a tier with its own maximum: the plateaus' differences. The
chart states no rounding.
"""

from __future__ import annotations

from decimal import Decimal

import pytest

import app.registrations
from app.adapters.outbound.yaml_parameters import YamlParameterSource
from app.domain.artifact import Artifact, ArtifactKind
from app.domain.capabilities.tiered_surcharge import TieredSurcharge
from app.domain.parameters.rate import Rate
from app.domain.parameters.rounding import NO_ROUNDING
from app.domain.parameters.surcharge_tiers import SURCHARGE_TIERS, SurchargeTier, SurchargeTiers

D = Decimal
SOURCE = YamlParameterSource(app.registrations.JURISDICTIONS.roots())
FAMILY = "ca-on/health_premium"
ON428_TEXT = "https://www.canada.ca/content/dam/cra-arc/formspubs/pbg/5006-c/5006-c-25e.txt"

# Made up for this test and not registered: the income the premium is on, and the premium.
INCOME = ArtifactKind("ex/income", Decimal)
PREMIUM = ArtifactKind("ex/premium", Decimal)


def test_2025_tiers_are_the_chart_rows_each_capped_at_the_next_plateau() -> None:
    data = SOURCE.get(FAMILY, 2025, SURCHARGE_TIERS)

    assert data.values == SurchargeTiers(
        (
            SurchargeTier(D("20000"), Rate(D("0.06")), D("300")),
            SurchargeTier(D("36000"), Rate(D("0.06")), D("150")),
            SurchargeTier(D("48000"), Rate(D("0.25")), D("150")),
            SurchargeTier(D("72000"), Rate(D("0.25")), D("150")),
            SurchargeTier(D("200000"), Rate(D("0.25")), D("150")),
        )
    )
    assert data.rounding == NO_ROUNDING  # the chart states no rounding


def test_2025_tiers_cite_only_the_on428_text() -> None:
    data = SOURCE.get(FAMILY, 2025, SURCHARGE_TIERS)

    assert data.sources == (ON428_TEXT,)


@pytest.mark.parametrize(
    ("income", "premium"),
    [
        # Return A (115000), D (74174.00) and E (198926.00): "more than $72,600 but not more than
        # $200,000", $750.
        ("115000", "750"),
        ("74174.00", "750"),
        ("198926.00", "750"),
        # Return C (49535.00): "more than $48,600 but not more than $72,000", $600.
        ("49535.00", "600"),
        # "$20,000 or less": $0, at the threshold and below it.
        ("0", "0"),
        ("20000", "0"),
        # A cent over: (20000.01 - 20000) x 6%, unrounded.
        ("20000.01", "0.0006"),
        # Inside the first sloped row: (22000 - 20000) x 6% = 120.
        ("22000", "120"),
        # At the row's top, (25000 - 20000) x 6% = 300, the plateau itself; above it, $300.
        ("25000", "300"),
        ("30000", "300"),
        ("36000", "300"),
        # (37000 - 36000) x 6% + 300 = 360; at 38500, 150 + 300 = 450.
        ("37000", "360"),
        ("38500", "450"),
        ("40000", "450"),
        # (48300 - 48000) x 25% + 450 = 525; at 48600, 150 + 450 = 600.
        ("48300", "525"),
        ("48600", "600"),
        # (72300 - 72000) x 25% + 600 = 675; at 72600, 750.
        ("72300", "675"),
        ("72600", "750"),
        ("200000", "750"),
        # (200300 - 200000) x 25% + 750 = 825; at 200600 and above, $900.
        ("200300", "825"),
        ("200600", "900"),
        ("1000000", "900"),
    ],
)
def test_charges_the_chart_premium_on_taxable_income(income: str, premium: str) -> None:
    capability = TieredSurcharge(SOURCE.get(FAMILY, 2025, SURCHARGE_TIERS), INCOME, PREMIUM)

    result = capability.compute((Artifact(INCOME, D(income)),))

    assert result.outputs == (Artifact(PREMIUM, D(premium)),)
