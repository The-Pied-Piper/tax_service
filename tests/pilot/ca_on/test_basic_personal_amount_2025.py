"""2025 federal and Ontario basic personal amounts, checked against CRA's forms.

Federal: 2025 T1 line 30000 ($16,129 at net income of $177,882 or less) and the
non-refundable credit rate on line 114 (14.5%). Ontario: 2025 ON428 line 58040
($12,747) and the credit rate on line 45 (5.05%). The federal amount's reduction
at higher net incomes is not modelled yet. Sources are listed in each dataset.
"""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

import pytest

from app.adapters.outbound.yaml_parameters import YamlParameterSource
from app.domain.artifact import Artifact
from app.domain.capabilities.non_refundable_credit import NonRefundableCredit
from app.domain.capability import CapabilityResult
from app.domain.parameters.credit import CREDIT, Credit
from app.domain.parameters.rounding import NO_ROUNDING
from app.domain.worksheet import Worksheet

D = Decimal
SOURCE = YamlParameterSource(Path(__file__).resolve().parents[3] / "data" / "parameters")
TAX, AFTER = Artifact("basic_tax"), Artifact("tax_after_credits")


def compute(capability: NonRefundableCredit, values: dict[Artifact, Decimal]) -> CapabilityResult:
    return capability.compute(Worksheet(values).view_for(capability))


@pytest.mark.parametrize(
    ("family", "amount", "rate"),
    [
        ("ca/basic_personal_amount", "16129", "0.145"),
        ("ca-on/basic_personal_amount", "12747", "0.0505"),
    ],
)
def test_2025_amounts_and_rates(family: str, amount: str, rate: str) -> None:
    data = SOURCE.get(family, 2025, CREDIT)

    assert data.values == Credit(amount=D(amount), rate=D(rate))
    assert data.rounding == NO_ROUNDING  # CRA states no rounding rule for amount × rate
    assert data.sources


@pytest.mark.parametrize(
    ("family", "basic_tax", "after"),
    [
        # $115,000 of taxable income: federal basic tax 20,146.25 less 16,129 × 14.5%.
        ("ca/basic_personal_amount", "20146.25", "17807.545"),
        # $10,000 of taxable income: federal basic tax 1,450 is fully offset.
        ("ca/basic_personal_amount", "1450", "0"),
        # Ontario basic tax on $115,000 (ON428 formula: 8,539.5965) less 12,747 × 5.05%.
        ("ca-on/basic_personal_amount", "8539.5965", "7895.873"),
    ],
)
def test_applies_to_basic_tax(family: str, basic_tax: str, after: str) -> None:
    data = SOURCE.get(family, 2025, CREDIT)

    capability = NonRefundableCredit(TAX, AFTER, data.values, data.rounding)

    result = compute(capability, {TAX: D(basic_tax)})

    assert result.outputs[AFTER] == D(after)
