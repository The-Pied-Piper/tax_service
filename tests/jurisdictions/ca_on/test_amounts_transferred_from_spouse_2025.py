"""The 2025 Schedule 2 dataset (federal amounts transferred from a spouse), checked against CRA.

Form 5000-S2 (T1-2025), "Spouse's or common-law partner's taxable income": line 7 "Enter the
amount from line 26000 of their return on line 7 if it is $57,375 or less. If it is more than
$57,375, enter the result of the following calculation: amount from line 76 of their return
divided by 14.5% =".

One dataset, the `threshold_rate` kind: $57,375 and 14.5%. It is Schedule 11 line 11's figures
again, but a dataset of its own because it is another form's line, rounded by its own rule:
Schedule 2 line 7 is a dollars-and-cents box and states no rounding rule, so it rounds half-up to
the cent, the owner's decision (#143).
"""

from __future__ import annotations

from decimal import Decimal

import pytest

import app.registrations
from app.adapters.outbound.yaml_parameters import YamlParameterSource
from app.domain.artifact import Artifact, ArtifactKind
from app.domain.parameters.rate import Rate
from app.domain.parameters.rounding import RoundingMode, RoundTo
from app.domain.parameters.threshold_rate import THRESHOLD_RATE, ThresholdRate
from app.jurisdictions.ca.capabilities.amount_or_divided_by_rate import AmountOrDividedByRate

D = Decimal
SOURCE = YamlParameterSource(app.registrations.JURISDICTIONS.roots())
INCOME_LIMIT = "ca/spouse_transfer_income_limit"

# Made up for these tests and not registered.
INCOME = ArtifactKind("ex/income", Decimal)
TAX = ArtifactKind("ex/tax", Decimal)
OUTPUT = ArtifactKind("ex/out", Decimal)


def test_2025_line_7_threshold_is_57375_and_rate_14_5_percent_to_the_cent() -> None:
    data = SOURCE.get(INCOME_LIMIT, 2025, THRESHOLD_RATE)

    assert data.values == ThresholdRate(Rate(D("0.145")), D("57375"))
    assert data.rounding == RoundTo(D("0.01"), RoundingMode.HALF_UP)


def test_2025_line_7_cites_schedule_2() -> None:
    data = SOURCE.get(INCOME_LIMIT, 2025, THRESHOLD_RATE)

    assert (
        "https://www.canada.ca/content/dam/cra-arc/formspubs/pbg/5000-s2/5000-s2-25e.txt"
        in data.sources
    )


@pytest.mark.parametrize(
    ("income", "tax", "line_7"),
    [
        # Schedule 2 worked example: their taxable income 20,000 is at or below $57,375.
        ("20000", "2900", "20000"),
        ("57375", "8319.38", "57375"),
        # Over it: their line 76 divided by 14.5%, half-up to the cent: 11000 / 0.145 =
        # 75862.0689..., 75862.07.
        ("70000", "11000", "75862.07"),
    ],
)
def test_line_7_is_their_taxable_income_or_their_tax_divided_by_14_5_percent(
    income: str, tax: str, line_7: str
) -> None:
    capability = AmountOrDividedByRate(
        SOURCE.get(INCOME_LIMIT, 2025, THRESHOLD_RATE), INCOME, TAX, OUTPUT
    )

    result = capability.compute((Artifact(INCOME, D(income)), Artifact(TAX, D(tax))))

    assert result.outputs == (Artifact(OUTPUT, D(line_7)),)
