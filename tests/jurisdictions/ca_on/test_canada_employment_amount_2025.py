"""The 2025 Canada employment amount cap, checked against CRA's T1.

2025 T1 (form 5000-R) line 92 (line 31260): "Enter whichever is less: $1,471 or line 1 plus
line 2.", where line 1 (line 10100) is "Employment income (box 14 of all T4 slips)" and line 2
(line 10400) is "Other employment income". Other employment income is not modelled, so the cap
applies to employment income alone. The $1,471 is a plain amount (the `amount` kind), not a
credit: the rate is applied once to the total of the credit amounts (line 33500), of which the
capped amount is one part. The form states no rounding.
"""

from __future__ import annotations

from decimal import Decimal

import pytest

import app.registrations
from app.adapters.outbound.yaml_parameters import YamlParameterSource
from app.domain.artifact import Artifact, ArtifactKind
from app.domain.capabilities.capped_amount import CappedAmount
from app.domain.errors import InvalidParameterDataError
from app.domain.parameters.amount import AMOUNT, Amount
from app.domain.parameters.credit import CREDIT
from app.domain.parameters.rounding import NO_ROUNDING

D = Decimal
SOURCE = YamlParameterSource(app.registrations.JURISDICTIONS.roots())
FAMILY = "ca/canada_employment_amount"

# Made up for this test and not registered: the income the cap applies to, and its capped amount.
INCOME = ArtifactKind("ex/income", Decimal)
CAPPED = ArtifactKind("ex/capped", Decimal)


def test_2025_cap_is_1471() -> None:
    data = SOURCE.get(FAMILY, 2025, AMOUNT)

    assert data.values == Amount(D("1471"))
    assert data.rounding == NO_ROUNDING  # the T1 states no rounding on line 92


def test_2025_cap_is_an_amount_not_a_credit() -> None:
    with pytest.raises(InvalidParameterDataError, match=r"kind 'amount'"):
        SOURCE.get(FAMILY, 2025, CREDIT)


@pytest.mark.parametrize(
    "source",
    [
        "https://www.canada.ca/content/dam/cra-arc/formspubs/pbg/5000-r/5000-r-25e.txt",
        "https://www.canada.ca/content/dam/cra-arc/formspubs/pbg/5000-r/5000-r-25e.pdf",
    ],
)
def test_2025_cap_cites_its_sources(source: str) -> None:
    data = SOURCE.get(FAMILY, 2025, AMOUNT)

    assert source in data.sources


@pytest.mark.parametrize(
    ("income", "capped"),
    [
        # Returns A, C and D: employment income well above the cap.
        ("110000", "1471"),
        ("50000", "1471"),
        ("75000", "1471"),
        # At the cap, and a cent above it.
        ("1471", "1471"),
        ("1471.01", "1471"),
        # Below the cap the income itself is the lesser, cents and all.
        ("1000.50", "1000.50"),
        ("0", "0"),
    ],
)
def test_caps_employment_income(income: str, capped: str) -> None:
    capability = CappedAmount(SOURCE.get(FAMILY, 2025, AMOUNT), INCOME, CAPPED)

    result = capability.compute((Artifact(INCOME, D(income)),))

    assert result.outputs == (Artifact(CAPPED, D(capped)),)
