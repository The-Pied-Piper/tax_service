"""The 2025 Schedule ON(S2) dataset (Ontario amounts from a spouse), checked against CRA.

Form 5006-S2 (Schedule ON(S2), 2025), "Spouse's or common-law partner's taxable income": line 5
"Enter the amount from line 26000 of their return on line 5 if it is $52,886 or less. If it is more
than $52,886, enter the result of the following calculation: Amount from line 8 of their Form
ON428" "divided by 5.05% =".

One dataset, the `threshold_rate` kind: $52,886 and 5.05%. They are Schedule ON(S11) line 2's
figures again, but a dataset of its own because it is another form's line, rounded by its own rule:
line 5 is a dollars-and-cents box and states no rounding rule, so it rounds half-up to the cent, as
every dollars-and-cents line does.
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
INCOME_LIMIT = "ca-on/spouse_transfer_income_limit"
S2_TEXT = "https://www.canada.ca/content/dam/cra-arc/formspubs/pbg/5006-s2/5006-s2-25e.txt"

# Made up for these tests and not registered.
INCOME = ArtifactKind("ex/income", Decimal)
TAX = ArtifactKind("ex/tax", Decimal)
OUTPUT = ArtifactKind("ex/out", Decimal)


def test_2025_line_5_threshold_is_52886_and_rate_5_05_percent_to_the_cent() -> None:
    data = SOURCE.get(INCOME_LIMIT, 2025, THRESHOLD_RATE)

    assert data.values == ThresholdRate(Rate(D("0.0505")), D("52886"))
    assert data.rounding == RoundTo(D("0.01"), RoundingMode.HALF_UP)


def test_2025_line_5_cites_only_schedule_on_s2() -> None:
    data = SOURCE.get(INCOME_LIMIT, 2025, THRESHOLD_RATE)

    assert data.sources == (S2_TEXT,)


@pytest.mark.parametrize(
    ("income", "tax", "line_5"),
    [
        # Return AT's example: their taxable income 20,000 is at or below $52,886.
        ("20000", "1010.00", "20000"),
        # At the threshold, the amount passes through ("or less").
        ("52886", "2670.74", "52886"),
        # A cent over, their tax is divided by 5.05%: 2670.74 x 2000 / 101 = 52885.9406, half-up
        # to 52885.94.
        ("52886.01", "2670.74", "52885.94"),
        # 3269.97 x 2000 / 101 = 64751.8812, half-up to 64751.88; their taxable income is unused.
        ("59435", "3269.97", "64751.88"),
    ],
)
def test_line_5_is_their_taxable_income_or_their_ontario_tax_divided_by_5_05_percent(
    income: str, tax: str, line_5: str
) -> None:
    capability = AmountOrDividedByRate(
        SOURCE.get(INCOME_LIMIT, 2025, THRESHOLD_RATE), INCOME, TAX, OUTPUT
    )

    result = capability.compute((Artifact(INCOME, D(income)), Artifact(TAX, D(tax))))

    assert result.outputs == (Artifact(OUTPUT, D(line_5)),)
