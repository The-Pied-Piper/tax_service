"""Registered and money kinds of the federal catalog family `investment_tax_credit`.

Form T2038(IND) Parts A and B: the caller's lines (67120, 67130, 67135, 67140, 67170, 67175, the
T3 box 40 amount of line 67180, and 67184 and 67185), the credit each one produces, and the two
declared outputs, amount A and amount F. The apprentices and their total are the kinds of
`credits_against_federal_tax`, which the family reads.
"""

from __future__ import annotations

from decimal import Decimal

import pytest

from app.domain.artifact import Artifact, ArtifactKind, ArtifactRegistry
from app.domain.errors import NegativeArtifactError
from app.jurisdictions.ca.catalog import (
    ITC_AGRICULTURAL_SRED_CONTRIBUTIONS,
    ITC_AGRICULTURAL_SRED_CREDIT,
    ITC_APPRENTICESHIP_CREDIT,
    ITC_APPRENTICESHIP_T3_BOX_40,
    ITC_APPRENTICESHIP_WAGES_WITH_T3,
    ITC_CRITICAL_MINERAL_CREDIT,
    ITC_CRITICAL_MINERAL_EXPENDITURES,
    ITC_MINERAL_EXPLORATION_CREDIT,
    ITC_MINERAL_EXPLORATION_EXPENDITURES,
    ITC_NONREFUNDABLE_CREDITS,
    ITC_QUALIFIED_PROPERTY,
    ITC_QUALIFIED_PROPERTY_CREDIT,
    ITC_REFUNDABLE_CREDITS,
    ITC_SRED_CREDIT,
    ITC_SRED_EXPENDITURES,
    ITC_SRED_PARTNERSHIP_ALLOCATION,
    ITC_SRED_REPAYMENT_2014_AND_PRIOR,
    ITC_SRED_REPAYMENT_2015_AND_AFTER,
    ITC_SRED_REPAYMENT_CREDIT,
    ITC_SRED_REPAYMENT_CREDIT_2014_AND_PRIOR,
    ITC_SRED_REPAYMENT_CREDIT_2015_AND_AFTER,
)

# The caller's lines, as the form takes them: line 67120 (Part A, amount 1), 67130 (amount 2),
# 67135 (amount 3), 67140 (amount 4), 67170 (Part B, amount B), 67175 (amount C), the T3 box 40
# amount of line 67180 (amount D), and lines 67184 and 67185 (Part B repayments 1 and 2).
CALLER_LINES: tuple[tuple[str, ArtifactKind[Decimal]], ...] = (
    ("ca/itc_sred_expenditures", ITC_SRED_EXPENDITURES),
    ("ca/itc_agricultural_sred_contributions", ITC_AGRICULTURAL_SRED_CONTRIBUTIONS),
    ("ca/itc_sred_partnership_allocation", ITC_SRED_PARTNERSHIP_ALLOCATION),
    ("ca/itc_qualified_property", ITC_QUALIFIED_PROPERTY),
    ("ca/itc_mineral_exploration_expenditures", ITC_MINERAL_EXPLORATION_EXPENDITURES),
    ("ca/itc_critical_mineral_expenditures", ITC_CRITICAL_MINERAL_EXPENDITURES),
    ("ca/itc_apprenticeship_t3_box_40", ITC_APPRENTICESHIP_T3_BOX_40),
    ("ca/itc_sred_repayment_2014_and_prior", ITC_SRED_REPAYMENT_2014_AND_PRIOR),
    ("ca/itc_sred_repayment_2015_and_after", ITC_SRED_REPAYMENT_2015_AND_AFTER),
)

# The credits each line produces at its rate (amounts 1, 2, 4, B, C, D, the two repayments and
# E), the sums that are not outputs (the total of line 67180 with the T3 box 40 amount, and E),
# and the credits that go into the two declared outputs.
CREDITS: tuple[tuple[str, ArtifactKind[Decimal]], ...] = (
    ("ca/itc_sred_credit", ITC_SRED_CREDIT),
    ("ca/itc_agricultural_sred_credit", ITC_AGRICULTURAL_SRED_CREDIT),
    ("ca/itc_qualified_property_credit", ITC_QUALIFIED_PROPERTY_CREDIT),
    ("ca/itc_mineral_exploration_credit", ITC_MINERAL_EXPLORATION_CREDIT),
    ("ca/itc_critical_mineral_credit", ITC_CRITICAL_MINERAL_CREDIT),
    ("ca/itc_apprenticeship_wages_with_t3", ITC_APPRENTICESHIP_WAGES_WITH_T3),
    ("ca/itc_apprenticeship_credit", ITC_APPRENTICESHIP_CREDIT),
    ("ca/itc_sred_repayment_credit_2014_and_prior", ITC_SRED_REPAYMENT_CREDIT_2014_AND_PRIOR),
    ("ca/itc_sred_repayment_credit_2015_and_after", ITC_SRED_REPAYMENT_CREDIT_2015_AND_AFTER),
    ("ca/itc_sred_repayment_credit", ITC_SRED_REPAYMENT_CREDIT),
)

# The two declared outputs: Part A amount A "Total current-year refundable credits (add amounts 1
# to 4)" and Part B amount F "Total current-year non-refundable tax credits (add amounts B, C, D
# and E)".
DECLARED_OUTPUTS: tuple[tuple[str, ArtifactKind[Decimal]], ...] = (
    ("ca/itc_refundable_credits", ITC_REFUNDABLE_CREDITS),
    ("ca/itc_nonrefundable_credits", ITC_NONREFUNDABLE_CREDITS),
)


def test_the_caller_lines_are_the_registered_kinds(registry: ArtifactRegistry) -> None:
    for identifier, kind in CALLER_LINES:
        assert registry.get(identifier) is kind, identifier


def test_the_credits_are_the_registered_kinds(registry: ArtifactRegistry) -> None:
    for identifier, kind in CREDITS:
        assert registry.get(identifier) is kind, identifier


def test_the_declared_outputs_are_the_registered_kinds(registry: ArtifactRegistry) -> None:
    for identifier, kind in DECLARED_OUTPUTS:
        assert registry.get(identifier) is kind, identifier


@pytest.mark.parametrize(
    ("identifier", "kind"),
    CALLER_LINES + CREDITS + DECLARED_OUTPUTS,
    ids=[identifier for identifier, _ in CALLER_LINES + CREDITS + DECLARED_OUTPUTS],
)
def test_every_kind_is_a_non_negative_money_kind(
    identifier: str, kind: ArtifactKind[Decimal]
) -> None:
    # No line of Part A or Part B can be negative on the form as modelled: each is an amount
    # the caller enters or a credit at a rate, and the form prints no floor to subtract from.
    assert kind.identifier == identifier
    assert kind.value_type is Decimal
    assert kind.non_negative is True


def test_a_negative_caller_line_is_refused() -> None:
    # Line 67120 "ITC for qualified expenditures for SR&ED": an amount, never negative.
    with pytest.raises(NegativeArtifactError):
        Artifact(ITC_SRED_EXPENDITURES, Decimal("-1"))


def test_a_credit_holds_its_amount_to_the_cent() -> None:
    # Amount 4 of Part A, "ITC for total investments in qualified property" at 10%: 10,000.00 x
    # 0.10 is 1,000.00, and the credit holds that amount.
    assert Artifact(ITC_QUALIFIED_PROPERTY_CREDIT, Decimal("1000.00")).value == Decimal("1000.00")
