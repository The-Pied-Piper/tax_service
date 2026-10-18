"""The 2025 amounts for an eligible dependant and for infirm children, checked against CRA's forms.

Federal: 2025 T1 (form 5000-R) line 80 (line 30400) "Amount for an eligible dependant (complete
Schedule 5)" and line 83 (line 30500) "Canada caregiver amount for infirm children under 18
years of age (see Schedule 5) Number of children you are claiming this amount for Line 30499"
"multiplied by $2,687". Schedule 5 (form 5000-S5), "Line 30400 - Amount for an eligible
dependant": line 1 "Basic personal amount from line 30000 of your return"; line 2 "If you are
eligible for the Canada caregiver amount for your dependant (other than your infirm child under 18
years of age), enter $2,687"; line 3 "Line 1 plus line 2"; line 4 (51106) "Dependant's net
income from line 23600 of their return"; line 5 "Line 3 minus line 4 (if negative, enter "0")
Enter this amount on line 30400 of your return.". Line 30400 has no dataset of its own: it is the
filer's line 30000 amount less the dependant's net income (line 2 not triggered), for each
eligible dependant ("Each household is allowed only one claim for this amount"). The $2,687 of
line 30500 is a per-unit amount (the `amount` kind).

Ontario: 2025 ON428 (form 5006-C) line 14 "Base amount 11,905.00"; line 15 "Your eligible
dependant's net income from line 23600 of their return"; line 16 (line 58160) "Line 14 minus line
15 (if negative, enter "0") (maximum $10,823)". The base is a claimed amount (the `credit` kind,
as the basic reduction), the maximum a plain cap (the `amount` kind). The forms state no rounding
on any of these lines.
"""

from __future__ import annotations

from decimal import Decimal

import pytest

import app.registrations
from app.adapters.outbound.yaml_parameters import YamlParameterSource
from app.domain.artifact import Artifact, ArtifactKind
from app.domain.capabilities.capped_amount import CappedAmount
from app.domain.capabilities.credit_amount import CreditAmount
from app.domain.capabilities.per_unit_amount import PerUnitAmount
from app.domain.parameters.amount import AMOUNT, Amount
from app.domain.parameters.credit import CREDIT, Credit
from app.domain.parameters.rounding import NO_ROUNDING

D = Decimal
SOURCE = YamlParameterSource(app.registrations.JURISDICTIONS.roots())
INFIRM_CHILD = "ca/infirm_child_amount"
ONTARIO_BASE = "ca-on/eligible_dependant_base"
ONTARIO_MAXIMUM = "ca-on/eligible_dependant_maximum"
T1_TEXT = "https://www.canada.ca/content/dam/cra-arc/formspubs/pbg/5000-r/5000-r-25e.txt"
ON428_TEXT = "https://www.canada.ca/content/dam/cra-arc/formspubs/pbg/5006-c/5006-c-25e.txt"

# Made up for this test and not registered: the number of infirm children and their amount (line
# 30500), the Ontario base as an artifact (line 14), and the Ontario amount before its maximum
# and after it (line 16).
INFIRM_CHILDREN = ArtifactKind("ex/infirm_children", int)
INFIRM_AMOUNT = ArtifactKind("ex/infirm_children_amount", Decimal)
BASE = ArtifactKind("ex/base", Decimal)
BEFORE_MAXIMUM = ArtifactKind("ex/before_maximum", Decimal)
BEFORE_COUNT = ArtifactKind("ex/before_count", Decimal)


def test_2025_amount_per_infirm_child_is_2687() -> None:
    data = SOURCE.get(INFIRM_CHILD, 2025, AMOUNT)

    assert data.values == Amount(D("2687"))
    assert data.rounding == NO_ROUNDING  # the T1 states no rounding on line 30500


def test_2025_ontario_base_is_11905() -> None:
    data = SOURCE.get(ONTARIO_BASE, 2025, CREDIT)

    assert data.values == Credit(amount=D("11905.00"))
    assert data.rounding == NO_ROUNDING  # ON428 states no rounding on line 14


def test_2025_ontario_maximum_is_10823() -> None:
    data = SOURCE.get(ONTARIO_MAXIMUM, 2025, AMOUNT)

    assert data.values == Amount(D("10823"))
    assert data.rounding == NO_ROUNDING  # ON428 states no rounding on line 16


def test_2025_datasets_cite_only_their_form_text() -> None:
    assert SOURCE.get(INFIRM_CHILD, 2025, AMOUNT).sources == (T1_TEXT,)
    assert SOURCE.get(ONTARIO_BASE, 2025, CREDIT).sources == (ON428_TEXT,)
    assert SOURCE.get(ONTARIO_MAXIMUM, 2025, AMOUNT).sources == (ON428_TEXT,)


@pytest.mark.parametrize(
    ("count", "amount"),
    [
        # Returns A to F: no infirm children.
        (0, "0"),
        (1, "2687"),
        (2, "5374"),
        (3, "8061"),
    ],
)
def test_2687_for_each_infirm_child(count: int, amount: str) -> None:
    capability = PerUnitAmount(
        SOURCE.get(INFIRM_CHILD, 2025, AMOUNT), INFIRM_CHILDREN, INFIRM_AMOUNT
    )

    result = capability.compute((Artifact(INFIRM_CHILDREN, count),))

    assert result.outputs == (Artifact(INFIRM_AMOUNT, D(amount)),)


def test_the_ontario_base_is_claimed_whole() -> None:
    capability = CreditAmount(SOURCE.get(ONTARIO_BASE, 2025, CREDIT), BASE)

    result = capability.compute(())

    assert result.outputs == (Artifact(BASE, D("11905.00")),)


@pytest.mark.parametrize(
    ("amount", "capped"),
    [
        # Return F: 11905.00 is above the maximum.
        ("11905.00", "10823"),
        # At the maximum, and a cent above it.
        ("10823", "10823"),
        ("10823.01", "10823"),
        # Below it, the amount itself, as for a dependant with 1500 of net income.
        ("10405.00", "10405.00"),
        ("0", "0"),
    ],
)
def test_the_ontario_amount_is_at_most_10823(amount: str, capped: str) -> None:
    capability = CappedAmount(
        SOURCE.get(ONTARIO_MAXIMUM, 2025, AMOUNT), BEFORE_MAXIMUM, BEFORE_COUNT
    )

    result = capability.compute((Artifact(BEFORE_MAXIMUM, D(amount)),))

    assert result.outputs == (Artifact(BEFORE_COUNT, D(capped)),)
