"""The CA-ON manifest entries of one family of lines (see `test_manifest.py`)."""

from __future__ import annotations

from app.domain.capabilities.apply_fraction import ApplyFraction
from app.domain.capabilities.apply_rate import ApplyRate
from app.domain.capabilities.choose_by_count import ChooseByCount
from app.domain.capabilities.contribution_tier import TieredContribution
from app.domain.capabilities.lesser_of import LesserOf
from app.domain.capabilities.per_unit_amount import PerUnitAmount
from app.domain.capabilities.subtract import Subtract
from app.domain.capabilities.subtract_not_below_zero import SubtractNotBelowZero
from app.domain.capabilities.sum import Sum
from app.domain.manifest import CapabilitySelection
from app.jurisdictions.ca.catalog import (
    ALLOWABLE_BUSINESS_INVESTMENT_LOSS,
    BUSINESS_INVESTMENT_LOSS,
    BUSINESS_INVESTMENT_LOSS_AFTER_REDUCTION,
    BUSINESS_INVESTMENT_LOSS_REDUCTION,
    BUSINESS_INVESTMENT_LOSS_REDUCTION_AVAILABLE,
    CAPITAL_GAINS_DEDUCTIONS_1985_TO_1987,
    CAPITAL_GAINS_DEDUCTIONS_1988_AND_1989_ELIGIBLE_CAPITAL_PROPERTY,
    CAPITAL_GAINS_DEDUCTIONS_1988_AND_1989_OTHER_THAN_ELIGIBLE_CAPITAL_PROPERTY,
    CAPITAL_GAINS_DEDUCTIONS_1990_TO_1999,
    CAPITAL_GAINS_DEDUCTIONS_2000,
    CAPITAL_GAINS_DEDUCTIONS_2001_TO_2024,
    CAPITAL_GAINS_DEDUCTIONS_CLAIMED_1985_TO_2024,
    CARRYING_CHARGES_INTEREST_EXPENSES_AND_OTHER_EXPENSES,
    CHILD_CARE_BASIC_LIMIT,
    CHILD_CARE_EARNED_INCOME,
    CHILD_CARE_EARNED_INCOME_LIMIT,
    CHILD_CARE_EXPENSES,
    CHILD_CARE_EXPENSES_PAID,
    CHILD_CARE_LIMIT_FOR_CHILDREN_SEVEN_TO_SIXTEEN,
    CHILD_CARE_LIMIT_FOR_CHILDREN_UNDER_SEVEN,
    CHILD_CARE_LIMIT_FOR_CHILDREN_WITH_DISABILITY,
    CHILDREN_SEVEN_TO_SIXTEEN,
    CHILDREN_UNDER_SEVEN,
    CHILDREN_WITH_DISABILITY,
    CPP_ENHANCED_CONTRIBUTIONS,
    CPP_FIRST_ADDITIONAL_CONTRIBUTIONS,
    CPP_SECOND_ADDITIONAL_CONTRIBUTIONS,
    DEDUCTIONS_FROM_TOTAL_INCOME,
    ELECTED_SPLIT_PENSION_DEDUCTION,
    EMPLOYMENT_INCOME,
    EXPLORATION_AND_DEVELOPMENT_EXPENSES,
    FHSA_DEDUCTION,
    INCOME_SUPPORT_BENEFITS,
    NET_INCOME,
    NET_INCOME_BEFORE_ADJUSTMENTS,
    NET_INCOME_LESS_UCCB_AND_RDSP_INCOME,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_1994,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_2024,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1994_TO_1996,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1997_TO_1999,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2000,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2001_TO_2023,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2024,
    OTHER_DEDUCTIONS,
    OTHER_PAYMENTS_DEDUCTION,
    OTHER_PAYMENTS_DEDUCTION_ABOVE_LIMIT,
    OTHER_PAYMENTS_DEDUCTION_AFTER_LIMIT,
    OTHER_PAYMENTS_LIMIT_INCOME,
    OTHER_PAYMENTS_WORKSHEET_LINE_9_OVER_LIMIT,
    OTHER_PAYMENTS_WORKSHEET_REQUIRED,
    RDSP_INCOME,
    RDSP_INCOME_REPAYMENT,
    RPP_DEDUCTION,
    RRSP_DEDUCTION,
    SUPPORT_PAYMENTS_DEDUCTION,
    TOTAL_CARRYING_CHARGES,
    TOTAL_INCOME,
    TOTAL_INTEREST_EXPENSES,
    TOTAL_OTHER_EXPENSES,
    UCCB_AND_RDSP_INCOME,
    UCCB_AND_RDSP_INCOME_REPAYMENTS,
    UCCB_REPAYMENT,
    UNION_DUES,
    UNIVERSAL_CHILD_CARE_BENEFIT,
)

INPUTS = frozenset(
    {
        "ca/uccb_repayment",
        "ca/rdsp_income_repayment",
        "ca/canadian_armed_forces_and_police_deduction",
        "ca/security_options_deductions",
        "ca/other_payments_deduction_above_limit",
        "ca/other_payments_worksheet_required",
        "ca/other_payments_worksheet_line_9_over_limit",
        "ca/union_dues",
        "ca/elected_split_pension_deduction",
        "ca/support_payments_deduction",
        "ca/exploration_and_development_expenses",
        "ca/other_deductions",
        "ca/total_carrying_charges",
        "ca/total_interest_expenses",
        "ca/total_other_expenses",
        "ca/capital_gains_deductions_1985_to_1987",
        "ca/capital_gains_deductions_1988_and_1989_other_than_eligible_capital_property",
        "ca/capital_gains_deductions_1988_and_1989_eligible_capital_property",
        "ca/capital_gains_deductions_1990_to_1999",
        "ca/capital_gains_deductions_2000",
        "ca/capital_gains_deductions_2001_to_2024",
        "ca/other_business_investment_loss_reductions_1986_to_1994",
        "ca/other_business_investment_loss_reductions_1994_to_1996",
        "ca/other_business_investment_loss_reductions_1997_to_1999",
        "ca/other_business_investment_loss_reductions_2000",
        "ca/other_business_investment_loss_reductions_2001_to_2023",
        "ca/other_business_investment_loss_reductions_2024",
        "ca/business_investment_loss",
        "ca/child_care_expenses_paid",
        "ca/children_under_seven",
        "ca/children_with_disability",
        "ca/children_seven_to_sixteen",
    }
)

OUTPUTS = frozenset(
    {
        "ca/net_income_before_adjustments",
        "ca/other_payments_limit_income",
    }
)

STEPS = {
    CapabilitySelection(
        name="core/contribution_tier",
        params={"tier": "ca/cpp_first_additional_contribution"},
        consumes={"earnings": "ca/employment_income"},
        produces={"output": "ca/cpp_first_additional_contributions"},
    ),
    CapabilitySelection(
        name="core/contribution_tier",
        params={"tier": "ca/cpp_second_additional_contribution"},
        consumes={"earnings": "ca/employment_income"},
        produces={"output": "ca/cpp_second_additional_contributions"},
    ),
    # Schedule 8 Part 3a line 28 "Line 26 plus line 27": the first and second additional
    # contributions together, the T1 line 22215 deduction.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/cpp_first_additional_contributions",
                "ca/cpp_second_additional_contributions",
            )
        },
        produces={"output": "ca/cpp_enhanced_contributions"},
    ),
    # Form T778 Part B line 1 "Number of eligible children born in 2019 or later whom the
    # disability amount cannot be claimed for" "multiplied by $8,000", line 2 (line 67960)
    # "Number of eligible children born in 2025 or earlier whom the disability amount can be
    # claimed for" "multiplied by $11,000" and line 3 "Number of eligible children born in
    # 2009 to 2018 (and born in 2008 or earlier with a mental or physical infirmity whom the
    # disability amount cannot be claimed for)" "multiplied by $5,000".
    CapabilitySelection(
        name="core/per_unit_amount",
        params={"amount": "ca/child_care_limit_under_seven"},
        consumes={"count": "ca/children_under_seven"},
        produces={"output": "ca/child_care_limit_for_children_under_seven"},
    ),
    CapabilitySelection(
        name="core/per_unit_amount",
        params={"amount": "ca/child_care_limit_disability"},
        consumes={"count": "ca/children_with_disability"},
        produces={"output": "ca/child_care_limit_for_children_with_disability"},
    ),
    CapabilitySelection(
        name="core/per_unit_amount",
        params={"amount": "ca/child_care_limit_seven_to_sixteen"},
        consumes={"count": "ca/children_seven_to_sixteen"},
        produces={"output": "ca/child_care_limit_for_children_seven_to_sixteen"},
    ),
    # T778 line 4 "Add lines 1 to 3.", in line order.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/child_care_limit_for_children_under_seven",
                "ca/child_care_limit_for_children_with_disability",
                "ca/child_care_limit_for_children_seven_to_sixteen",
            )
        },
        produces={"output": "ca/child_care_basic_limit"},
    ),
    # T778 line 6 "Enter your earned income.", "the total of the following: employment
    # income (including tips and gratuities, and the non-taxable part of an allowance
    # received as an emergency volunteer) ...": the employment income, the other earned
    # income lines not triggered; then "multiplied by two-thirds": one part.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/employment_income",)},
        produces={"output": "ca/child_care_earned_income"},
    ),
    CapabilitySelection(
        name="core/apply_fraction",
        params={"fraction": "ca/child_care_earned_income_fraction"},
        consumes={"base": "ca/child_care_earned_income"},
        produces={"output": "ca/child_care_earned_income_limit"},
    ),
    # T778 line 7 "Enter whichever amount is the least: line 4, line 5 or line 6.", in that
    # order, line 5 "Enter the amount from line 67950." being the expenses paid; with line 8
    # (the other person with the higher net income) not triggered, line 9 "Line 7 minus line
    # 8. ... enter this amount on line 21400 of your return. Allowable deduction" is line 7.
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={
            "amounts": (
                "ca/child_care_basic_limit",
                "ca/child_care_expenses_paid",
                "ca/child_care_earned_income_limit",
            )
        },
        produces={"output": "ca/child_care_expenses"},
    ),
    # Federal Worksheet "Line 22100 - Carrying charges, interest expenses, and other expenses":
    # line 1 "Total carrying charges", line 2 "Total interest expenses" and line 3 "Total other
    # expenses" (starting amounts), and line 4 "Add lines 1 to 3. Enter this amount on line
    # 22100 of your return.", in line order.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/total_carrying_charges",
                "ca/total_interest_expenses",
                "ca/total_other_expenses",
            )
        },
        produces={"output": "ca/carrying_charges_interest_expenses_and_other_expenses"},
    ),
    # Form T1436 (Capital Gains Worksheet), "Line 21700 – Allowable business investment loss",
    # "Calculating your business investment loss reduction, if any": lines 1 to 6 (the capital
    # gains deductions claimed for 1985 to 1987, for 1988 and 1989 other than for eligible
    # capital property, for 1988 and 1989 for eligible capital property, for 1990 to 1999, for
    # 2000 and for 2001 to 2024) are starting amounts, each as its line prints it after its
    # multiplier (the figures come from the returns of 1985 to 2024); line 7 "Add lines 1 to 6."
    # Total of all capital gains deductions claimed from 1985 to 2024.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/capital_gains_deductions_1985_to_1987",
                "ca/capital_gains_deductions_1988_and_1989_other_than_eligible_capital_property",
                "ca/capital_gains_deductions_1988_and_1989_eligible_capital_property",
                "ca/capital_gains_deductions_1990_to_1999",
                "ca/capital_gains_deductions_2000",
                "ca/capital_gains_deductions_2001_to_2024",
            )
        },
        produces={"output": "ca/capital_gains_deductions_claimed_1985_to_2024"},
    ),
    # Lines 8 to 13 (the amounts of Schedule 3 for 1986 to 1994, 1994 to 1996, 1997 to 1999,
    # 2000, 2001 to 2023 and 2024) are starting amounts; line 14 "Add lines 8 to 13." Total of
    # all other business investment loss reductions for 1986 to 2024.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/other_business_investment_loss_reductions_1986_to_1994",
                "ca/other_business_investment_loss_reductions_1994_to_1996",
                "ca/other_business_investment_loss_reductions_1997_to_1999",
                "ca/other_business_investment_loss_reductions_2000",
                "ca/other_business_investment_loss_reductions_2001_to_2023",
                "ca/other_business_investment_loss_reductions_2024",
            )
        },
        produces={"output": "ca/other_business_investment_loss_reductions_1986_to_2024"},
    ),
    # Line 15 "Line 7 minus line 14" prints no "(if negative, enter "0")", so it may be
    # negative.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/capital_gains_deductions_claimed_1985_to_2024",
            "less": "ca/other_business_investment_loss_reductions_1986_to_2024",
        },
        produces={"output": "ca/business_investment_loss_reduction_available"},
    ),
    # Line 16 "Business investment loss in 2025 Enter this amount on line 21699 of your return."
    # is a starting amount, the gross of line 21699; line 17 "Enter whichever is less: amount
    # from line 15 or line 16. Enter this amount on line 17800 of Schedule 3." prints no "(if
    # negative, enter "0")" either, so it may be negative with line 15.
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={
            "amounts": (
                "ca/business_investment_loss_reduction_available",
                "ca/business_investment_loss",
            )
        },
        produces={"output": "ca/business_investment_loss_reduction"},
    ),
    # Line 18 "Line 16 minus line 17 Business investment loss reduction": never negative, as
    # line 17 is at most line 16.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/business_investment_loss",
            "less": "ca/business_investment_loss_reduction",
        },
        produces={"output": "ca/business_investment_loss_after_reduction"},
    ),
    # Line 19 "Inclusion rate for 2025 × 50 %", the rate dataset, and line 20 "Line 18
    # multiplied by the percentage on line 19 Enter this amount on line 21700 of your return.
    # Allowable business investment loss".
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/business_investment_loss_inclusion_rate"},
        consumes={"base": "ca/business_investment_loss_after_reduction"},
        produces={"output": "ca/allowable_business_investment_loss"},
    ),
    # T1 line 53 and line 23300 "Add lines 35 to 52.": the deductions wired so far in the form's
    # line order (20700, 20800, 20805, 21000, 21200, 21300, 21400, 21700, 22000, 22100, 22215,
    # 22400, 23200). Not wired yet: 21500, 21900, 22200, 22900 and 23100; lines 20810 and 21999
    # have no line among lines 35 to 52 and nothing on this return reads them.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/rpp_deduction",
                "ca/rrsp_deduction",
                "ca/fhsa_deduction",
                "ca/elected_split_pension_deduction",
                "ca/union_dues",
                "ca/uccb_repayment",
                "ca/child_care_expenses",
                "ca/allowable_business_investment_loss",
                "ca/support_payments_deduction",
                "ca/carrying_charges_interest_expenses_and_other_expenses",
                "ca/cpp_enhanced_contributions",
                "ca/exploration_and_development_expenses",
                "ca/other_deductions",
            )
        },
        produces={"output": "ca/deductions_from_total_income"},
    ),
    # T1 line 54 and line 23400 "Line 34 minus line 53 (if negative, show in brackets) Net
    # income before adjustments": total income less total deductions, not floored, so a negative
    # result is shown in brackets. The net income of line 56 (line 23600) stays the floored
    # result until line 23500 is wired.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ca/total_income", "less": "ca/deductions_from_total_income"},
        produces={"output": "ca/net_income_before_adjustments"},
    ),
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={"amount": "ca/total_income", "less": "ca/deductions_from_total_income"},
        produces={"output": "ca/net_income"},
    ),
    # Federal Worksheet "Line 25000 - Other payments deduction", "Complete the following
    # calculation if you reported net federal supplements on line 14600 of your return.":
    # line 1 "Amount from line 23400 of your return (if negative, enter "0")" is the net
    # income artifact (line 23400 floored at 0, as line 23500 is not wired yet); line 4 "Line
    # 2 plus line 3 =" adds line 2 "Amount from line 11700 of your return" (the universal
    # child care benefit) and line 3 "Amount from line 12500 of your return" (the RDSP
    # income), in line order.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/universal_child_care_benefit", "ca/rdsp_income")},
        produces={"output": "ca/uccb_and_rdsp_income"},
    ),
    # Line 5 "Line 1 minus line 4 =" prints no "(if negative, enter "0")", unlike line 1, so
    # it may be negative.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ca/net_income", "less": "ca/uccb_and_rdsp_income"},
        produces={"output": "ca/net_income_less_uccb_and_rdsp_income"},
    ),
    # Line 8 "Line 6 plus line 7 =": line 6 "Amount from line 21300 of your return" (the UCCB
    # repayment, a starting amount, also a part of line 23300) and line 7 "RDSP income
    # repayment (included in the amount on line 23200 of your return)", a starting amount of
    # its own that the caller also includes in line 23200, in line order.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/uccb_repayment", "ca/rdsp_income_repayment")},
        produces={"output": "ca/uccb_and_rdsp_income_repayments"},
    ),
    # Line 9 "Line 5 plus line 8 =", the amount the worksheet compares with $93,454.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/net_income_less_uccb_and_rdsp_income",
                "ca/uccb_and_rdsp_income_repayments",
            )
        },
        produces={"output": "ca/other_payments_limit_income"},
    ),
    # "If the amount on line 9 is more than $93,454, go to canada.ca/line-25000 to find out
    # how much you can deduct. Otherwise, enter the amount from line 14700 of your return on
    # line 25000 of your return.": a count of 1 when line 9 is more than $93,454 (a starting
    # count, 0 or 1, until a comparison capability derives it) chooses the amount that chart
    # gives (a starting amount) over line 14700.
    CapabilitySelection(
        name="core/choose_by_count",
        params={},
        consumes={
            "count": "ca/other_payments_worksheet_line_9_over_limit",
            "when_none": "ca/income_support_benefits",
            "when_any": "ca/other_payments_deduction_above_limit",
        },
        produces={"output": "ca/other_payments_deduction_after_limit"},
    ),
    # T1 line 60 and line 25000 "Other payments deduction (enter the amount from line 14700
    # if you did not enter an amount on line 14600; otherwise, use Federal Worksheet)": a
    # count of 1 when an amount was entered on line 14600 (a starting count, 0 or 1, until a
    # comparison capability derives it) chooses the worksheet's result over line 14700.
    CapabilitySelection(
        name="core/choose_by_count",
        params={},
        consumes={
            "count": "ca/other_payments_worksheet_required",
            "when_none": "ca/income_support_benefits",
            "when_any": "ca/other_payments_deduction_after_limit",
        },
        produces={"output": "ca/other_payments_deduction"},
    ),
}

WIRING = {
    (
        TieredContribution,
        frozenset({EMPLOYMENT_INCOME}),
        frozenset({CPP_FIRST_ADDITIONAL_CONTRIBUTIONS}),
    ),
    (
        TieredContribution,
        frozenset({EMPLOYMENT_INCOME}),
        frozenset({CPP_SECOND_ADDITIONAL_CONTRIBUTIONS}),
    ),
    (
        Sum,
        frozenset({CPP_FIRST_ADDITIONAL_CONTRIBUTIONS, CPP_SECOND_ADDITIONAL_CONTRIBUTIONS}),
        frozenset({CPP_ENHANCED_CONTRIBUTIONS}),
    ),
    (
        PerUnitAmount,
        frozenset({CHILDREN_UNDER_SEVEN}),
        frozenset({CHILD_CARE_LIMIT_FOR_CHILDREN_UNDER_SEVEN}),
    ),
    (
        PerUnitAmount,
        frozenset({CHILDREN_WITH_DISABILITY}),
        frozenset({CHILD_CARE_LIMIT_FOR_CHILDREN_WITH_DISABILITY}),
    ),
    (
        PerUnitAmount,
        frozenset({CHILDREN_SEVEN_TO_SIXTEEN}),
        frozenset({CHILD_CARE_LIMIT_FOR_CHILDREN_SEVEN_TO_SIXTEEN}),
    ),
    (
        Sum,
        frozenset(
            {
                CHILD_CARE_LIMIT_FOR_CHILDREN_UNDER_SEVEN,
                CHILD_CARE_LIMIT_FOR_CHILDREN_WITH_DISABILITY,
                CHILD_CARE_LIMIT_FOR_CHILDREN_SEVEN_TO_SIXTEEN,
            }
        ),
        frozenset({CHILD_CARE_BASIC_LIMIT}),
    ),
    (Sum, frozenset({EMPLOYMENT_INCOME}), frozenset({CHILD_CARE_EARNED_INCOME})),
    (
        ApplyFraction,
        frozenset({CHILD_CARE_EARNED_INCOME}),
        frozenset({CHILD_CARE_EARNED_INCOME_LIMIT}),
    ),
    (
        LesserOf,
        frozenset(
            {CHILD_CARE_BASIC_LIMIT, CHILD_CARE_EXPENSES_PAID, CHILD_CARE_EARNED_INCOME_LIMIT}
        ),
        frozenset({CHILD_CARE_EXPENSES}),
    ),
    (
        Sum,
        frozenset({TOTAL_CARRYING_CHARGES, TOTAL_INTEREST_EXPENSES, TOTAL_OTHER_EXPENSES}),
        frozenset({CARRYING_CHARGES_INTEREST_EXPENSES_AND_OTHER_EXPENSES}),
    ),
    (
        Sum,
        frozenset(
            {
                CAPITAL_GAINS_DEDUCTIONS_1985_TO_1987,
                CAPITAL_GAINS_DEDUCTIONS_1988_AND_1989_OTHER_THAN_ELIGIBLE_CAPITAL_PROPERTY,
                CAPITAL_GAINS_DEDUCTIONS_1988_AND_1989_ELIGIBLE_CAPITAL_PROPERTY,
                CAPITAL_GAINS_DEDUCTIONS_1990_TO_1999,
                CAPITAL_GAINS_DEDUCTIONS_2000,
                CAPITAL_GAINS_DEDUCTIONS_2001_TO_2024,
            }
        ),
        frozenset({CAPITAL_GAINS_DEDUCTIONS_CLAIMED_1985_TO_2024}),
    ),
    (
        Sum,
        frozenset(
            {
                OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_1994,
                OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1994_TO_1996,
                OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1997_TO_1999,
                OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2000,
                OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2001_TO_2023,
                OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2024,
            }
        ),
        frozenset({OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_2024}),
    ),
    (
        Subtract,
        frozenset(
            {
                CAPITAL_GAINS_DEDUCTIONS_CLAIMED_1985_TO_2024,
                OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_2024,
            }
        ),
        frozenset({BUSINESS_INVESTMENT_LOSS_REDUCTION_AVAILABLE}),
    ),
    (
        LesserOf,
        frozenset({BUSINESS_INVESTMENT_LOSS_REDUCTION_AVAILABLE, BUSINESS_INVESTMENT_LOSS}),
        frozenset({BUSINESS_INVESTMENT_LOSS_REDUCTION}),
    ),
    (
        Subtract,
        frozenset({BUSINESS_INVESTMENT_LOSS, BUSINESS_INVESTMENT_LOSS_REDUCTION}),
        frozenset({BUSINESS_INVESTMENT_LOSS_AFTER_REDUCTION}),
    ),
    (
        ApplyRate,
        frozenset({BUSINESS_INVESTMENT_LOSS_AFTER_REDUCTION}),
        frozenset({ALLOWABLE_BUSINESS_INVESTMENT_LOSS}),
    ),
    (
        Sum,
        frozenset(
            {
                RPP_DEDUCTION,
                RRSP_DEDUCTION,
                FHSA_DEDUCTION,
                ELECTED_SPLIT_PENSION_DEDUCTION,
                UNION_DUES,
                UCCB_REPAYMENT,
                CHILD_CARE_EXPENSES,
                ALLOWABLE_BUSINESS_INVESTMENT_LOSS,
                SUPPORT_PAYMENTS_DEDUCTION,
                CARRYING_CHARGES_INTEREST_EXPENSES_AND_OTHER_EXPENSES,
                CPP_ENHANCED_CONTRIBUTIONS,
                EXPLORATION_AND_DEVELOPMENT_EXPENSES,
                OTHER_DEDUCTIONS,
            }
        ),
        frozenset({DEDUCTIONS_FROM_TOTAL_INCOME}),
    ),
    (
        Subtract,
        frozenset({TOTAL_INCOME, DEDUCTIONS_FROM_TOTAL_INCOME}),
        frozenset({NET_INCOME_BEFORE_ADJUSTMENTS}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({TOTAL_INCOME, DEDUCTIONS_FROM_TOTAL_INCOME}),
        frozenset({NET_INCOME}),
    ),
    (
        Sum,
        frozenset({UNIVERSAL_CHILD_CARE_BENEFIT, RDSP_INCOME}),
        frozenset({UCCB_AND_RDSP_INCOME}),
    ),
    (
        Subtract,
        frozenset({NET_INCOME, UCCB_AND_RDSP_INCOME}),
        frozenset({NET_INCOME_LESS_UCCB_AND_RDSP_INCOME}),
    ),
    (
        Sum,
        frozenset({UCCB_REPAYMENT, RDSP_INCOME_REPAYMENT}),
        frozenset({UCCB_AND_RDSP_INCOME_REPAYMENTS}),
    ),
    (
        Sum,
        frozenset({NET_INCOME_LESS_UCCB_AND_RDSP_INCOME, UCCB_AND_RDSP_INCOME_REPAYMENTS}),
        frozenset({OTHER_PAYMENTS_LIMIT_INCOME}),
    ),
    (
        ChooseByCount,
        frozenset(
            {
                OTHER_PAYMENTS_WORKSHEET_LINE_9_OVER_LIMIT,
                INCOME_SUPPORT_BENEFITS,
                OTHER_PAYMENTS_DEDUCTION_ABOVE_LIMIT,
            }
        ),
        frozenset({OTHER_PAYMENTS_DEDUCTION_AFTER_LIMIT}),
    ),
    (
        ChooseByCount,
        frozenset(
            {
                OTHER_PAYMENTS_WORKSHEET_REQUIRED,
                INCOME_SUPPORT_BENEFITS,
                OTHER_PAYMENTS_DEDUCTION_AFTER_LIMIT,
            }
        ),
        frozenset({OTHER_PAYMENTS_DEDUCTION}),
    ),
}
