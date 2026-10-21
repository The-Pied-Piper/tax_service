"""The 2025 Part 1 line 96 federal tax rate of Form T691: 20.5% of line 95, checked against Form
T691. Form T691 (2025) Part 1 line 96: "Federal tax rate" "× 20.5%" (line 96), read by line 97
"Gross minimum amount: line 95 multiplied by the percentage on line 96.". The 20.5% is the printed
percentage of the form, a rate of 0.205, applied to a dollars-and-cents product, so it is rounded
half-up to the cent, the owner's decision, as the form states no rounding rule.
"""

from __future__ import annotations

from decimal import Decimal

import pytest

import app.registrations
from app.adapters.outbound.yaml_parameters import YamlParameterSource
from app.domain.artifact import Artifact, ArtifactKind
from app.domain.capabilities.apply_rate import ApplyRate
from app.domain.parameters.rate import RATE, Rate
from app.domain.parameters.rounding import RoundingMode, RoundTo

D = Decimal
SOURCE = YamlParameterSource(app.registrations.JURISDICTIONS.roots())
T691_PDF = "https://www.canada.ca/content/dam/cra-arc/formspubs/pbg/t691/t691-25e.pdf"
CENT = RoundTo(D("0.01"), RoundingMode.HALF_UP)

FAMILY = "ca/amt_federal_tax_rate"

# Made up for this test and not registered: the amount the rate is applied to, and the product.
BASE = ArtifactKind("ex/amt_line_95", Decimal)
AMOUNT = ArtifactKind("ex/amt_line_97", Decimal)


def test_2025_amt_federal_tax_rate_is_20_5_percent() -> None:
    data = SOURCE.get(FAMILY, 2025, RATE)

    assert data.values == Rate(D("0.205"))
    # Part 1 line 96, a dollars-and-cents line: half-up to the cent.
    assert data.rounding == CENT


def test_2025_amt_federal_tax_rate_cites_the_form_it_is_printed_on() -> None:
    data = SOURCE.get(FAMILY, 2025, RATE)

    assert T691_PDF in data.sources


@pytest.mark.parametrize(
    ("base", "result"),
    [
        ("34176.50", "7006.18"),
        ("100", "20.50"),
    ],
)
def test_applies_to_the_base(base: str, result: str) -> None:
    capability = ApplyRate(SOURCE.get(FAMILY, 2025, RATE), BASE, AMOUNT)

    result_outputs = capability.compute((Artifact(BASE, D(base)),)).outputs

    assert result_outputs == (Artifact(AMOUNT, D(result)),)
