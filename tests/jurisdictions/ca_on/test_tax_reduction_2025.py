"""The 2025 Ontario tax reduction amounts and factor, checked against CRA's ON428.

2025 ON428 (form 5006-C), Ontario tax reduction: line 74 "Basic reduction 294.00"; line 75 (line
60969) "Number of dependent children multiplied by $544"; line 76 (line 60970) "Number of
dependants multiplied by $544"; line 77 "Add lines 74 to 76."; line 78 "Amount from line 77 above
multiplied by 2"; line 79 "Amount from line 73 above"; line 80 "Line 78 minus line 79 (if negative,
enter "0") Ontario tax reduction". The basic reduction is a claimed amount (the `credit` kind, as
the basic personal amount), the $544 a per-unit amount (the `amount` kind) for both lines 75 and
76, and the 2 a factor (the `factor` kind), since a `rate` is at most 1. The form states no
rounding on lines 74 to 80.
"""

from __future__ import annotations

from decimal import Decimal

import pytest

import app.registrations
from app.adapters.outbound.yaml_parameters import YamlParameterSource
from app.domain.artifact import Artifact, ArtifactKind
from app.domain.capabilities.credit_amount import CreditAmount
from app.domain.capabilities.multiple_over import MultipleOver
from app.domain.capabilities.per_unit_amount import PerUnitAmount
from app.domain.parameters.amount import AMOUNT, Amount
from app.domain.parameters.credit import CREDIT, Credit
from app.domain.parameters.factor import FACTOR, Factor
from app.domain.parameters.rounding import NO_ROUNDING

D = Decimal
SOURCE = YamlParameterSource(app.registrations.JURISDICTIONS.roots())
BASIC = "ca-on/tax_reduction_basic"
PER_DEPENDANT = "ca-on/tax_reduction_per_dependant"
FACTOR_FAMILY = "ca-on/tax_reduction_factor"
ON428_TEXT = "https://www.canada.ca/content/dam/cra-arc/formspubs/pbg/5006-c/5006-c-25e.txt"

# Made up for this test and not registered: the basic reduction as an artifact, a count and its
# per-unit amount, the reduction amounts (line 77), the tax they are set against (line 73) and the
# reduction (line 80).
BASIC_REDUCTION = ArtifactKind("ex/basic_reduction", Decimal)
COUNT = ArtifactKind("ex/count", int)
COUNT_AMOUNT = ArtifactKind("ex/count_amount", Decimal)
AMOUNTS = ArtifactKind("ex/reduction_amounts", Decimal)
TAX = ArtifactKind("ex/tax", Decimal)
REDUCTION = ArtifactKind("ex/reduction", Decimal)


def test_2025_basic_reduction_is_294() -> None:
    data = SOURCE.get(BASIC, 2025, CREDIT)

    assert data.values == Credit(amount=D("294.00"))
    assert data.rounding == NO_ROUNDING  # ON428 states no rounding on line 74


def test_2025_amount_per_dependant_is_544() -> None:
    data = SOURCE.get(PER_DEPENDANT, 2025, AMOUNT)

    assert data.values == Amount(D("544"))
    assert data.rounding == NO_ROUNDING  # ON428 states no rounding on lines 75 and 76


def test_2025_factor_is_2() -> None:
    data = SOURCE.get(FACTOR_FAMILY, 2025, FACTOR)

    assert data.values == Factor(D("2"))
    assert data.rounding == NO_ROUNDING  # ON428 states no rounding on lines 78 and 80


def test_2025_datasets_cite_only_the_on428_text() -> None:
    assert SOURCE.get(BASIC, 2025, CREDIT).sources == (ON428_TEXT,)
    assert SOURCE.get(PER_DEPENDANT, 2025, AMOUNT).sources == (ON428_TEXT,)
    assert SOURCE.get(FACTOR_FAMILY, 2025, FACTOR).sources == (ON428_TEXT,)


def test_the_basic_reduction_is_claimed_whole() -> None:
    capability = CreditAmount(SOURCE.get(BASIC, 2025, CREDIT), BASIC_REDUCTION)

    result = capability.compute(())

    assert result.outputs == (Artifact(BASIC_REDUCTION, D("294.00")),)


@pytest.mark.parametrize(
    ("count", "amount"),
    [
        # Returns A, C, D and E: no dependent children and no dependants.
        (0, "0"),
        (1, "544"),
        (2, "1088"),
        (3, "1632"),
        (5, "2720"),
    ],
)
def test_544_for_each_dependent_child_or_dependant(count: int, amount: str) -> None:
    capability = PerUnitAmount(SOURCE.get(PER_DEPENDANT, 2025, AMOUNT), COUNT, COUNT_AMOUNT)

    result = capability.compute((Artifact(COUNT, count),))

    assert result.outputs == (Artifact(COUNT_AMOUNT, D(amount)),)


@pytest.mark.parametrize(
    ("amounts", "tax", "reduction"),
    [
        # Returns A, C, D and E: line 77 is the basic reduction alone, 294.00, so line 78 is
        # 588.00; each line 73 exceeds it, so line 80 is 0.
        ("294.00", "8195.7699076", "0"),
        ("294.00", "1700.145625", "0"),
        ("294.00", "3750.97271", "0"),
        ("294.00", "23570.1964036", "0"),
        # A tax below 588.00: the reduction is the difference, unrounded.
        ("294.00", "486.802325", "101.197675"),
        # At 588.00 nothing is left; with no tax the whole 588.00.
        ("294.00", "588.00", "0"),
        ("294.00", "0", "588.00"),
        # Five dependent children and three dependants: 294.00 + 2720 + 1632 = 4646.00, so line
        # 78 is 9292.00, above Return A's line 73.
        ("4646.00", "8195.7699076", "1096.2300924"),
    ],
)
def test_twice_the_reduction_amounts_over_the_tax(amounts: str, tax: str, reduction: str) -> None:
    capability = MultipleOver(SOURCE.get(FACTOR_FAMILY, 2025, FACTOR), AMOUNTS, TAX, REDUCTION)

    result = capability.compute((Artifact(AMOUNTS, D(amounts)), Artifact(TAX, D(tax))))

    assert result.outputs == (Artifact(REDUCTION, D(reduction)),)
