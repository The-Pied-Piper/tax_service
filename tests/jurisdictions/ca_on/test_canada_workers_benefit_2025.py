"""The 2025 Canada workers benefit basic amount and reduction, checked against CRA's Schedule 6.

2025 Schedule 6 (form 5000-S6), Step 2, for a filer with no eligible spouse and no eligible
dependant: line 16 "Family working income from line 6"; line 17 "Base amount 3,000.00"; line 18
"Line 16 minus line 17 (if negative, enter "0")"; line 19 "Rate 27%"; line 20 "Line 18 multiplied
by the percentage from line 19"; line 21 "If you had an eligible spouse or an eligible dependant,
enter $2,813. If not, enter $1,633."; line 22 "Enter whichever is less: amount from line 20 or
line 21."; line 23 "Adjusted family net income from line 15"; line 24 "If you had an eligible
spouse or an eligible dependant, enter $30,639. If not, enter $26,855."; line 25 "Line 23 minus
line 24 (if negative, enter "0")"; line 26 "Rate 15%"; line 27 "Line 25 multiplied by the
percentage from line 26"; line 28 "Line 22 minus line 27 (if negative, enter "0")". Lines 17 to 22
are one tier over the base amount with a maximum, and lines 24 to 27 one tier over the threshold
with none (the `surcharge_tiers` kind). The chart's "Basic CWB: $37,742" limit is not a dataset:
it follows from the arithmetic, as 1,633 less 15% of (37,742 - 26,855) is below zero. The form
states no rounding.
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
BASIC_FAMILY = "ca/cwb_basic"
REDUCTION_FAMILY = "ca/cwb_reduction"
SCHEDULE_6_TEXT = "https://www.canada.ca/content/dam/cra-arc/formspubs/pbg/5000-s6/5000-s6-25e.txt"

# Made up for this test and not registered: the working income the basic amount is on (line 16),
# the basic amount (line 22), the adjusted family net income the reduction is on (line 23) and the
# reduction (line 27).
WORKING_INCOME = ArtifactKind("ex/working_income", Decimal)
BASIC = ArtifactKind("ex/basic", Decimal)
NET_INCOME = ArtifactKind("ex/net_income", Decimal)
REDUCTION = ArtifactKind("ex/reduction", Decimal)


def test_2025_basic_amount_is_27_percent_over_3000_at_most_1633() -> None:
    data = SOURCE.get(BASIC_FAMILY, 2025, SURCHARGE_TIERS)

    assert data.values == SurchargeTiers((SurchargeTier(D("3000"), Rate(D("0.27")), D("1633")),))
    assert data.rounding == NO_ROUNDING  # Schedule 6 states no rounding on lines 18 to 22


def test_2025_reduction_is_15_percent_over_26855() -> None:
    data = SOURCE.get(REDUCTION_FAMILY, 2025, SURCHARGE_TIERS)

    assert data.values == SurchargeTiers((SurchargeTier(D("26855"), Rate(D("0.15"))),))
    assert data.rounding == NO_ROUNDING  # Schedule 6 states no rounding on lines 25 and 27


def test_2025_datasets_cite_only_the_schedule_6_text() -> None:
    assert SOURCE.get(BASIC_FAMILY, 2025, SURCHARGE_TIERS).sources == (SCHEDULE_6_TEXT,)
    assert SOURCE.get(REDUCTION_FAMILY, 2025, SURCHARGE_TIERS).sources == (SCHEDULE_6_TEXT,)


@pytest.mark.parametrize(
    ("working_income", "basic"),
    [
        # Return B: (30000 - 3000) x 27% = 7290.00, more than 1633.
        ("30000", "1633"),
        # The low-income return of the worked-return tests: (10000 - 3000) x 27% = 1890.00,
        # more than 1633.
        ("10000", "1633"),
        # Below the maximum: (8000 - 3000) x 27%, unrounded.
        ("8000", "1350.00"),
        # Returns C and A, far above it.
        ("50000", "1633"),
        ("110000", "1633"),
        # At the base amount nothing is over it; a cent above, 27% of the cent, unrounded.
        ("3000", "0"),
        ("3000.01", "0.0027"),
        ("0", "0"),
    ],
)
def test_27_percent_of_working_income_over_3000_at_most_1633(
    working_income: str, basic: str
) -> None:
    capability = TieredSurcharge(
        SOURCE.get(BASIC_FAMILY, 2025, SURCHARGE_TIERS), WORKING_INCOME, BASIC
    )

    result = capability.compute((Artifact(WORKING_INCOME, D(working_income)),))

    assert result.outputs == (Artifact(BASIC, D(basic)),)


@pytest.mark.parametrize(
    ("net_income", "reduction"),
    [
        # Return B: (29735.00 - 26855) x 15% = 2880.00 x 15%.
        ("29735.00", "432.0000"),
        # Return C: (49535.00 - 26855) x 15% = 22680.00 x 15%, more than 1633.
        ("49535.00", "3402.0000"),
        # The low-income return: 9935.00 is below the threshold, so line 25 is 0.
        ("9935.00", "0"),
        # Return A: (115000 - 26855) x 15%.
        ("115000", "13221.75"),
        # The chart's limit: (37742 - 26855) x 15% = 1633.05, more than the 1633 maximum.
        ("37742", "1633.05"),
        # At the threshold nothing is over it; a cent above, 15% of the cent, unrounded.
        ("26855", "0"),
        ("26855.01", "0.0015"),
        ("0", "0"),
    ],
)
def test_15_percent_of_net_income_over_26855(net_income: str, reduction: str) -> None:
    capability = TieredSurcharge(
        SOURCE.get(REDUCTION_FAMILY, 2025, SURCHARGE_TIERS), NET_INCOME, REDUCTION
    )

    result = capability.compute((Artifact(NET_INCOME, D(net_income)),))

    assert result.outputs == (Artifact(REDUCTION, D(reduction)),)
