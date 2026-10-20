"""CA-ON 2025 end to end: return ao."""

from __future__ import annotations

from typing import Any

import pytest

from app.domain.trace import ConditionsCountLine
from app.domain.worksheet import Worksheet
from app.jurisdictions.ca.catalog import NET_INCOME
from app.jurisdictions.ca_on.catalog import (
    ONTARIO_MINIMUM_TAX,
    ONTARIO_TAX_AFTER_DIVIDEND_CREDIT,
    ONTARIO_TAX_AFTER_REDUCTION,
    ONTARIO_TAX_BEFORE_REDUCTION,
    ONTARIO_TAX_REDUCTION,
    ONTARIO_TAX_REDUCTION_BEFORE_CONDITIONS,
    TAX_REDUCTION_AMOUNTS,
    TAX_REDUCTION_AMOUNTS_CLAIMABLE,
    TAX_REDUCTION_BASIC,
    TAX_REDUCTION_CLAIMABLE,
    TAX_REDUCTION_FOR_CHILDREN,
    TAX_REDUCTION_FOR_CHILDREN_BEFORE_SPOUSE_RULE,
    TAX_REDUCTION_FOR_DEPENDANTS,
    TAX_REDUCTION_FOR_DEPENDANTS_BEFORE_SPOUSE_RULE,
)
from tests.jurisdictions.ca_on.end_to_end.support import D, compute


def return_ao(**overrides: Any) -> Worksheet:
    """Return AO's inputs, as in `returns/2025_return_ao.yaml`: the higher-income spouse.

    Employment income of 22139.77 (a chosen figure) makes net income 21953.37 and the Ontario tax
    after the dividend credit (ON428 line 71) exactly 400.00, which is line 73 with no line 72.
    The filer has a spouse or common-law partner on December 31 whose net income is 15000 (a
    chosen figure), and two dependent children born in 2007 or later; none of the six conditions
    on which the form enters "0" on line 80 applies.
    """
    inputs: dict[str, Any] = {
        "dependent_children": 2,
        "spouse_or_common_law_partner_on_december_31": 1,
        "spouse_net_income": "15000",
    }
    return compute("22139.77", (), "0", "0", "0", "0", "0", **{**inputs, **overrides})


def counted(worksheet: Worksheet, kind: Any) -> ConditionsCountLine:
    (line,) = (
        line
        for line in worksheet.trace
        if isinstance(line, ConditionsCountLine) and line.output == kind
    )
    return line


def test_the_higher_income_spouse_claims_lines_75_and_76_and_line_80_is_2364() -> None:
    # ON428: line 73 "Line 71 plus line 72 =" is 400.00 + 0 = 400.00. "If you had a spouse or
    # common-law partner on December 31, 2025, only the individual with the higher net income can
    # claim the amounts on lines 75 and 76": net income 21953.37 is more than the spouse's
    # 15000, so the filer claims. Line 74 "Basic reduction 294.00"; line 75 "Number of dependent
    # children multiplied by $544" is 2 x 544 = 1088.00; line 76 is 0 x 544 = 0; line 77 "Add
    # lines 74 to 76." is 294.00 + 1088.00 + 0 = 1382.00; line 78 "Amount from line 77 above
    # multiplied by 2" is 2764.00; line 80 "Line 78 minus line 79 (if negative, enter "0")" is
    # 2764.00 - 400.00 = 2364.00 and line 81 "Line 73 minus line 80 (if negative, enter "0")" is
    # 0, as 400.00 - 2364.00 is negative.
    worksheet = return_ao()

    assert worksheet.get(NET_INCOME).value == D("21953.37")
    assert worksheet.get(ONTARIO_TAX_AFTER_DIVIDEND_CREDIT).value == D("400.00")
    assert worksheet.get(ONTARIO_MINIMUM_TAX).value == D("0")
    assert worksheet.get(ONTARIO_TAX_BEFORE_REDUCTION).value == D("400.00")
    assert worksheet.get(TAX_REDUCTION_AMOUNTS_CLAIMABLE).value == 1
    assert worksheet.get(TAX_REDUCTION_BASIC).value == D("294.00")
    assert worksheet.get(TAX_REDUCTION_FOR_CHILDREN_BEFORE_SPOUSE_RULE).value == D("1088.00")
    assert worksheet.get(TAX_REDUCTION_FOR_DEPENDANTS_BEFORE_SPOUSE_RULE).value == D("0")
    assert worksheet.get(TAX_REDUCTION_FOR_CHILDREN).value == D("1088.00")
    assert worksheet.get(TAX_REDUCTION_FOR_DEPENDANTS).value == D("0")
    assert worksheet.get(TAX_REDUCTION_AMOUNTS).value == D("1382.00")
    assert worksheet.get(ONTARIO_TAX_REDUCTION_BEFORE_CONDITIONS).value == D("2364.00")
    assert worksheet.get(TAX_REDUCTION_CLAIMABLE).value == 1
    assert worksheet.get(ONTARIO_TAX_REDUCTION).value == D("2364.00")
    assert worksheet.get(ONTARIO_TAX_AFTER_REDUCTION).value == D("0")


def test_the_lower_income_spouse_claims_neither_line_and_line_80_is_188() -> None:
    # The spouse's net income, 48000, is more than the filer's 21953.37, so the filer does not
    # claim lines 75 and 76: both are 0 whatever the counts, line 77 is the basic 294.00, line 78
    # is 588.00, line 80 is 588.00 - 400.00 = 188.00 and line 81 is 400.00 - 188.00 = 212.00.
    worksheet = return_ao(spouse_net_income="48000")

    assert worksheet.get(TAX_REDUCTION_AMOUNTS_CLAIMABLE).value == 0
    assert worksheet.get(TAX_REDUCTION_FOR_CHILDREN_BEFORE_SPOUSE_RULE).value == D("1088.00")
    assert worksheet.get(TAX_REDUCTION_FOR_CHILDREN).value == D("0")
    assert worksheet.get(TAX_REDUCTION_FOR_DEPENDANTS).value == D("0")
    assert worksheet.get(TAX_REDUCTION_AMOUNTS).value == D("294.00")
    assert worksheet.get(ONTARIO_TAX_REDUCTION_BEFORE_CONDITIONS).value == D("188.00")
    assert worksheet.get(TAX_REDUCTION_CLAIMABLE).value == 1
    assert worksheet.get(ONTARIO_TAX_REDUCTION).value == D("188.00")
    assert worksheet.get(ONTARIO_TAX_AFTER_REDUCTION).value == D("212.00")


def test_an_amount_on_line_72_makes_line_80_zero_and_is_part_of_line_73() -> None:
    # "There is an amount on line 72" is one of the six conditions: line 72 of 120.00 makes line
    # 73 400.00 + 120.00 = 520.00, and line 80 "0" however large twice lines 74 to 76 are (here
    # 2764.00 - 520.00 = 2244.00 before the conditions), so line 81 is line 73, 520.00.
    worksheet = return_ao(ontario_minimum_tax="120.00")

    assert worksheet.get(ONTARIO_MINIMUM_TAX).value == D("120.00")
    assert worksheet.get(ONTARIO_TAX_AFTER_DIVIDEND_CREDIT).value == D("400.00")
    assert worksheet.get(ONTARIO_TAX_BEFORE_REDUCTION).value == D("520.00")
    assert worksheet.get(ONTARIO_TAX_REDUCTION_BEFORE_CONDITIONS).value == D("2244.00")
    assert worksheet.get(TAX_REDUCTION_CLAIMABLE).value == 0
    assert worksheet.get(ONTARIO_TAX_REDUCTION).value == D("0")
    assert worksheet.get(ONTARIO_TAX_AFTER_REDUCTION).value == D("520.00")


def test_a_line_72_of_zero_is_not_an_amount_on_line_72() -> None:
    worksheet = return_ao(ontario_minimum_tax="0.00")

    assert worksheet.get(TAX_REDUCTION_CLAIMABLE).value == 1
    assert worksheet.get(ONTARIO_TAX_REDUCTION).value == D("2364.00")


def test_bankruptcy_in_2025_makes_line_80_zero() -> None:
    # "You were bankrupt at any time in 2025": line 80 is "0", so line 81 is line 73, 400.00.
    worksheet = return_ao(bankrupt_in_year=1)

    assert worksheet.get(TAX_REDUCTION_CLAIMABLE).value == 0
    assert worksheet.get(ONTARIO_TAX_REDUCTION_BEFORE_CONDITIONS).value == D("2364.00")
    assert worksheet.get(ONTARIO_TAX_REDUCTION).value == D("0")
    assert worksheet.get(ONTARIO_TAX_AFTER_REDUCTION).value == D("400.00")


@pytest.mark.parametrize(
    "condition",
    [
        "not_resident_of_canada_at_start_of_year",
        "not_resident_of_ontario_at_year_end",
        "bankrupt_in_year",
        "return_filed_by_trustee_in_bankruptcy",
        "not_claiming_ontario_tax_reduction",
    ],
)
def test_each_of_the_five_counts_alone_makes_line_80_zero(condition: str) -> None:
    worksheet = return_ao(**{condition: 1})

    assert worksheet.get(TAX_REDUCTION_CLAIMABLE).value == 0
    assert worksheet.get(ONTARIO_TAX_REDUCTION).value == D("0")
    assert worksheet.get(ONTARIO_TAX_AFTER_REDUCTION).value == D("400.00")


def test_the_trace_names_the_conditions_that_apply_by_position_in_the_form_s_order() -> None:
    # "You were bankrupt at any time in 2025" is the fourth of the six printed conditions, and
    # "There is an amount on line 72" the third.
    bankrupt = return_ao(bankrupt_in_year=1)
    minimum_tax = return_ao(ontario_minimum_tax="120.00")
    neither = return_ao()

    assert counted(bankrupt, TAX_REDUCTION_CLAIMABLE) == ConditionsCountLine(
        TAX_REDUCTION_CLAIMABLE, (4,), 0
    )
    assert counted(minimum_tax, TAX_REDUCTION_CLAIMABLE) == ConditionsCountLine(
        TAX_REDUCTION_CLAIMABLE, (3,), 0
    )
    assert counted(neither, TAX_REDUCTION_CLAIMABLE) == ConditionsCountLine(
        TAX_REDUCTION_CLAIMABLE, (), 1
    )


def test_equal_net_incomes_leave_the_claim_to_the_caller() -> None:
    # The form names no claimant when the two net incomes are equal (to be confirmed): the
    # caller says, yes or no, whether this return claims lines 75 and 76. Net income 21953.37.
    claims = return_ao(
        spouse_net_income="21953.37", claims_tax_reduction_amounts_at_equal_net_income=1
    )
    does_not = return_ao(spouse_net_income="21953.37")

    assert claims.get(TAX_REDUCTION_AMOUNTS_CLAIMABLE).value == 1
    assert claims.get(ONTARIO_TAX_REDUCTION).value == D("2364.00")
    assert does_not.get(TAX_REDUCTION_AMOUNTS_CLAIMABLE).value == 0
    assert does_not.get(ONTARIO_TAX_REDUCTION).value == D("188.00")


def test_the_claim_at_a_tie_changes_nothing_when_the_net_incomes_differ() -> None:
    higher = return_ao(claims_tax_reduction_amounts_at_equal_net_income=1)
    lower = return_ao(spouse_net_income="48000", claims_tax_reduction_amounts_at_equal_net_income=1)

    assert higher.get(ONTARIO_TAX_REDUCTION).value == D("2364.00")
    assert lower.get(ONTARIO_TAX_REDUCTION).value == D("188.00")


def test_with_no_spouse_or_common_law_partner_the_filer_claims_whatever_the_spouse_figure() -> None:
    # "If you had a spouse or common-law partner on December 31, 2025, ...": with none (the T1's
    # marital status is not Box 1 or Box 2) the rule does not apply, so the filer claims lines 75
    # and 76 even with a spouse net income of 48000 entered.
    worksheet = return_ao(spouse_or_common_law_partner_on_december_31=0, spouse_net_income="48000")

    assert worksheet.get(TAX_REDUCTION_AMOUNTS_CLAIMABLE).value == 1
    assert worksheet.get(TAX_REDUCTION_FOR_CHILDREN).value == D("1088.00")
    assert worksheet.get(ONTARIO_TAX_REDUCTION).value == D("2364.00")


def test_a_dependant_with_an_impairment_adds_544_to_the_amounts_the_filer_claims() -> None:
    # Line 76 (line 60970) "Number of dependants multiplied by $544" is 1 x 544 = 544.00; line
    # 77 is 294.00 + 1088.00 + 544.00 = 1926.00, line 78 is 3852.00 and line 80 is 3852.00 -
    # 400.00 = 3452.00.
    worksheet = return_ao(dependants=1)

    assert worksheet.get(TAX_REDUCTION_FOR_DEPENDANTS).value == D("544.00")
    assert worksheet.get(TAX_REDUCTION_AMOUNTS).value == D("1926.00")
    assert worksheet.get(ONTARIO_TAX_REDUCTION).value == D("3452.00")
    assert worksheet.get(ONTARIO_TAX_AFTER_REDUCTION).value == D("0")


def test_the_lower_income_spouse_claims_neither_dependants_line() -> None:
    worksheet = return_ao(dependants=1, spouse_net_income="48000")

    assert worksheet.get(TAX_REDUCTION_FOR_DEPENDANTS_BEFORE_SPOUSE_RULE).value == D("544.00")
    assert worksheet.get(TAX_REDUCTION_FOR_DEPENDANTS).value == D("0")
    assert worksheet.get(TAX_REDUCTION_AMOUNTS).value == D("294.00")
