"""The 2025 entry conditions of Form T657 Chart 2021, 2022 and 2023 Part 2, checked against the
form.

Form T657 (2025), Chart Y Part 1: "If you are reporting a reserve in 2025 from a disposition of QFFP
in Y and amount E above is equal to or less than the amounts on line 21 of Step 1, line 19 of Step 2,
and amount M above, and you want to claim the additional deduction, complete Part 2 of Chart Y on
the next page." Each dataset `ca/t657_chart_Y_part_2_conditions` lists, in that order, the
conditions under which Part 2 is not completed: the filer does not want the additional deduction
(a 0/1 count), and Part 1 amount E is more than line 21, more than line 19 or more than Part 1
amount M (amounts read in the order amount E, line 21, line 19, amount M). The count is 0 when any
applies and 1 when none does, and is not rounded.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Any

import pytest

import app.registrations
from app.adapters.outbound.yaml_parameters import YamlParameterSource
from app.domain.parameters.conditions import (
    CONDITIONS,
    Condition,
    ConditionList,
    ConditionPart,
    ConditionTest,
)
from app.domain.parameters.rounding import NO_ROUNDING

SOURCE = YamlParameterSource(app.registrations.JURISDICTIONS.roots())
T657_PDF = "https://www.canada.ca/content/dam/cra-arc/formspubs/pbg/t657/t657-25e.pdf"
YEARS = (2021, 2022, 2023)


def conditions_dataset(year: int) -> Any:
    return SOURCE.get(f"ca/t657_chart_{year}_part_2_conditions", 2025, CONDITIONS)


@pytest.mark.parametrize("year", YEARS)
def test_2025_part_2_is_skipped_when_any_of_four_conditions_applies(year: int) -> None:
    data = conditions_dataset(year)

    assert data.values == ConditionList(
        0,
        (
            Condition(
                "You do not want to claim the additional deduction",
                (ConditionPart((ConditionTest("count", 1, "equal_to", Decimal(0), None),)),),
            ),
            Condition(
                "Amount E in Part 1 is more than your annual gains limit for 2025 from line 21 "
                "in Step 1",
                (ConditionPart((ConditionTest("amount", 1, "more_than", None, 2),)),),
            ),
            Condition(
                "Amount E in Part 1 is more than your cumulative gains limit for 2025 from line "
                "19 in Step 2",
                (ConditionPart((ConditionTest("amount", 1, "more_than", None, 3),)),),
            ),
            Condition(
                "Amount E in Part 1 is more than the total amount of capital gains included in "
                "your 2025 income that is eligible for the capital gains deduction from amount "
                "M in Part 1",
                (ConditionPart((ConditionTest("amount", 1, "more_than", None, 4),)),),
            ),
        ),
    )


@pytest.mark.parametrize("year", YEARS)
def test_2025_the_conditions_are_a_count_so_nothing_is_rounded_and_cite_the_pdf(year: int) -> None:
    data = conditions_dataset(year)

    assert data.rounding == NO_ROUNDING
    assert data.sources == (T657_PDF,)
