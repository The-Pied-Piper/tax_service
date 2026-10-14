"""2025 federal and Ontario basic personal amounts and credit rates, checked against CRA's forms.

Federal: 2025 T1 line 30000 ($16,129 at net income of $177,882 or less) and the
non-refundable credit rate on line 114 (14.5%). Ontario: 2025 ON428 line 58040
($12,747) and the credit rate on line 45 (5.05%). Each rate is its own dataset
(`credit_rate`), stated once. The federal amount's reduction at higher net incomes
is not modelled yet. Sources are listed in each dataset.
"""

from __future__ import annotations

from decimal import Decimal

import pytest

import app.registrations
from app.adapters.outbound.yaml_parameters import YamlParameterSource
from app.domain.artifact import Artifact, ArtifactKind
from app.domain.capabilities.non_refundable_credit import NonRefundableCredit
from app.domain.parameters.brackets import BRACKETS
from app.domain.parameters.credit import CREDIT, Credit
from app.domain.parameters.rate import RATE, Rate
from app.domain.parameters.rounding import NO_ROUNDING

D = Decimal
SOURCE = YamlParameterSource(app.registrations.JURISDICTIONS.roots())


# Made up for this test and not registered: whichever basic tax the credit applies to, and
# that tax less the credit.
BASIC_TAX = ArtifactKind("ex/basic_tax", Decimal)
TAX_AFTER_CREDITS = ArtifactKind("ex/tax_after_credits", Decimal)


@pytest.mark.parametrize(
    ("family", "amount"),
    [("ca/basic_personal_amount", "16129"), ("ca-on/basic_personal_amount", "12747")],
)
def test_2025_amounts(family: str, amount: str) -> None:
    data = SOURCE.get(family, 2025, CREDIT)

    assert data.values == Credit(amount=D(amount))
    assert data.rounding == NO_ROUNDING  # CRA states no rounding rule for amount × rate
    assert data.sources


@pytest.mark.parametrize(
    ("family", "rate"),
    [("ca/credit_rate", "0.145"), ("ca-on/credit_rate", "0.0505")],
)
def test_2025_credit_rates(family: str, rate: str) -> None:
    data = SOURCE.get(family, 2025, RATE)

    assert data.values == Rate(D(rate))
    assert data.sources


@pytest.mark.parametrize(
    ("rate_family", "brackets_family"),
    [("ca/credit_rate", "ca/brackets"), ("ca-on/credit_rate", "ca-on/brackets")],
)
def test_2025_credit_rate_is_the_lowest_bracket_rate(
    rate_family: str, brackets_family: str
) -> None:
    rate = SOURCE.get(rate_family, 2025, RATE).values.value
    lowest = SOURCE.get(brackets_family, 2025, BRACKETS).values.brackets[0].rate

    assert rate == lowest


@pytest.mark.parametrize(
    ("prefix", "basic_tax", "after"),
    [
        # $115,000 of taxable income: federal basic tax 20,146.25 less 16,129 × 14.5%.
        ("ca", "20146.25", "17807.545"),
        # $10,000 of taxable income: federal basic tax 1,450 is fully offset.
        ("ca", "1450", "0"),
        # Ontario basic tax on $115,000 (ON428 formula: 8,539.5965) less 12,747 × 5.05%.
        ("ca-on", "8539.5965", "7895.873"),
    ],
)
def test_applies_to_basic_tax(prefix: str, basic_tax: str, after: str) -> None:
    amount = SOURCE.get(f"{prefix}/basic_personal_amount", 2025, CREDIT)
    rate = SOURCE.get(f"{prefix}/credit_rate", 2025, RATE)

    capability = NonRefundableCredit(BASIC_TAX, TAX_AFTER_CREDITS, amount, rate)

    result = capability.compute((Artifact(BASIC_TAX, D(basic_tax)),))

    assert result.outputs == (Artifact(TAX_AFTER_CREDITS, D(after)),)
