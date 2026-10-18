"""The 2025 Ontario surtax tiers, checked against CRA's ON428.

2025 ON428 (form 5006-C): line 65 "Line 63 minus line 64 (if negative, enter "0")" is the surtax
base; line 66 "(Line 65 minus $5,710) multiplied by 20% (if negative, enter "0")"; line 67 "(Line
65 minus $7,307) multiplied by 36% (if negative, enter "0")"; line 68 "Line 66 plus line 67" is
the surtax. Each tier is a separate line, so each is its own part; the form states no rounding on
lines 66 and 67.
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
FAMILY = "ca-on/surtax"
ON428_TEXT = "https://www.canada.ca/content/dam/cra-arc/formspubs/pbg/5006-c/5006-c-25e.txt"

# Made up for this test and not registered: the tax the surtax is on, and the surtax.
TAX = ArtifactKind("ex/tax", Decimal)
SURTAX = ArtifactKind("ex/surtax", Decimal)


def test_2025_tiers_are_20_percent_over_5710_and_36_percent_over_7307() -> None:
    data = SOURCE.get(FAMILY, 2025, SURCHARGE_TIERS)

    assert data.values == SurchargeTiers(
        (
            SurchargeTier(D("5710"), Rate(D("0.20"))),
            SurchargeTier(D("7307"), Rate(D("0.36"))),
        )
    )
    assert data.rounding == NO_ROUNDING  # ON428 states no rounding on lines 66 and 67


def test_2025_tiers_cite_only_the_on428_text() -> None:
    data = SOURCE.get(FAMILY, 2025, SURCHARGE_TIERS)

    assert data.sources == (ON428_TEXT,)


@pytest.mark.parametrize(
    ("tax", "surtax"),
    [
        # Return A: Ontario tax after credits of 7671.98071, above both thresholds:
        # (7671.98071 - 5710) x 20% = 392.396142 plus (7671.98071 - 7307) x 36% = 131.3930556.
        ("7671.98071", "523.7891976"),
        # Returns C and D: below the first threshold, so no surtax.
        ("1700.145625", "0"),
        ("3750.97271", "0"),
        # At the first threshold nothing is over it; a cent above, 20% of the cent, unrounded.
        ("5710", "0"),
        ("5710.01", "0.002"),
        # At the second threshold only the first tier charges: 1597 x 20%.
        ("7307", "319.40"),
        # A cent above it: 1597.01 x 20% plus 0.01 x 36%.
        ("7307.01", "319.4056"),
        ("0", "0"),
    ],
)
def test_surcharges_the_ontario_tax(tax: str, surtax: str) -> None:
    capability = TieredSurcharge(SOURCE.get(FAMILY, 2025, SURCHARGE_TIERS), TAX, SURTAX)

    result = capability.compute((Artifact(TAX, D(tax)),))

    assert result.outputs == (Artifact(SURTAX, D(surtax)),)
