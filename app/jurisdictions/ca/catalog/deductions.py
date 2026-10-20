"""The federal catalog: deductions from total income.

The split pension, union dues, child care, capital gains deduction, business investment loss,
support, carrying charges, CPP and other deduction lines, down to net income and the repayment lines
that follow it.
"""

from __future__ import annotations

from decimal import Decimal

from app.jurisdictions.ca.catalog.base import CATALOG

ELECTED_SPLIT_PENSION_DEDUCTION = CATALOG.declare(
    "elected_split_pension_deduction", Decimal, non_negative=True
)
"""Deduction for elected split-pension amount, T1 line 38 and line 21000 "Deduction for elected
split-pension amount (complete Form T1032)": the amount claimed, a starting amount; the election
is the filer's, from the spouse-coupled Form T1032."""

UNION_DUES = CATALOG.declare("union_dues", Decimal, non_negative=True)
"""Union dues, T1 line 21200 "Annual union, professional, or like dues (receipts and box 44 of all
T4 slips)": the amount claimed, a starting amount."""

CHILD_CARE_EXPENSES_PAID = CATALOG.declare("child_care_expenses_paid", Decimal, non_negative=True)
"""Child care expenses paid, Form T778 Part A line 67950 "Total (add all entries for Child care
expenses paid)": a starting amount, also Part B line 5 "Enter the amount from line 67950."."""

CHILDREN_UNDER_SEVEN = CATALOG.declare("children_under_seven", int, non_negative=True)
"""Number of eligible children born in 2019 or later, Form T778 Part B line 1 "Number of eligible
children born in 2019 or later whom the disability amount cannot be claimed for": a starting
count."""

CHILDREN_WITH_DISABILITY = CATALOG.declare("children_with_disability", int, non_negative=True)
"""Number of eligible children with the disability amount, Form T778 Part B line 2 (line 67960)
"Number of eligible children born in 2025 or earlier whom the disability amount can be claimed
for": a starting count."""

CHILDREN_SEVEN_TO_SIXTEEN = CATALOG.declare("children_seven_to_sixteen", int, non_negative=True)
"""Number of eligible children born in 2009 to 2018, Form T778 Part B line 3 "Number of eligible
children born in 2009 to 2018 (and born in 2008 or earlier with a mental or physical infirmity
whom the disability amount cannot be claimed for)": a starting count."""

CHILD_CARE_LIMIT_FOR_CHILDREN_UNDER_SEVEN = CATALOG.declare(
    "child_care_limit_for_children_under_seven", Decimal, non_negative=True
)
"""Child care limit for the children born in 2019 or later, Form T778 Part B line 1 "multiplied by
$8,000": the line 1 count times $8,000, a part of line 4."""

CHILD_CARE_LIMIT_FOR_CHILDREN_WITH_DISABILITY = CATALOG.declare(
    "child_care_limit_for_children_with_disability", Decimal, non_negative=True
)
"""Child care limit for the children with the disability amount, Form T778 Part B line 2 (line
67960) "multiplied by $11,000": the line 2 count times $11,000, a part of line 4."""

CHILD_CARE_LIMIT_FOR_CHILDREN_SEVEN_TO_SIXTEEN = CATALOG.declare(
    "child_care_limit_for_children_seven_to_sixteen", Decimal, non_negative=True
)
"""Child care limit for the children born in 2009 to 2018, Form T778 Part B line 3 "multiplied by
$5,000": the line 3 count times $5,000, a part of line 4."""

CHILD_CARE_BASIC_LIMIT = CATALOG.declare("child_care_basic_limit", Decimal, non_negative=True)
"""Child care basic limit, Form T778 Part B line 4 "Add lines 1 to 3.": the limits for each group
of eligible children, in line order."""

CHILD_CARE_EARNED_INCOME = CATALOG.declare("child_care_earned_income", Decimal, non_negative=True)
"""Earned income for child care, Form T778 Part B line 6 "Enter your earned income.": "Your earned
income of line 6 is the total of the following: employment income (including tips and gratuities,
and the non-taxable part of an allowance received as an emergency volunteer) ...", here employment
income alone.

The other parts of earned income the form's "Earned income" definition lists are not triggered by
the returns modelled.
"""

CHILD_CARE_EARNED_INCOME_LIMIT = CATALOG.declare(
    "child_care_earned_income_limit", Decimal, non_negative=True
)
"""Earned income limit for child care, Form T778 Part B line 6 "multiplied by two-thirds": the
earned income times two-thirds, rounded half-up to the cent, once, as line 6 is a dollars-and-cents
box."""

CHILD_CARE_EXPENSES = CATALOG.declare("child_care_expenses", Decimal, non_negative=True)
"""Child care expenses deduction, T1 line 41 (line 21400) "Child care expenses (complete Form
T778)": Form T778 Part B line 7 "Enter whichever amount is the least: line 4, line 5 or line 6.",
carried by line 9 "Line 7 minus line 8. ... enter this amount on line 21400 of your return.
Allowable deduction", a deduction from total income.

Line 8 (the other person with the higher net income) is not triggered, so line 9 is line 7; nor
are Parts C and D (the higher-income claimant, school attendance). Eligibility is the return's to
state, not computed here.
"""

CAPITAL_GAINS_DEDUCTIONS_1985_TO_1987 = CATALOG.declare(
    "capital_gains_deductions_1985_to_1987", Decimal, non_negative=True
)
"""Capital gains deductions claimed for 1985 to 1987, Form T1436 (Capital Gains Worksheet) line
1, as the line prints it after its multiplier: a starting amount, a figure from the returns of
1985 to 2024."""

CAPITAL_GAINS_DEDUCTIONS_1988_AND_1989_OTHER_THAN_ELIGIBLE_CAPITAL_PROPERTY = CATALOG.declare(
    "capital_gains_deductions_1988_and_1989_other_than_eligible_capital_property",
    Decimal,
    non_negative=True,
)
"""Capital gains deductions claimed for 1988 and 1989 other than for eligible capital property,
Form T1436 (Capital Gains Worksheet) line 2, as the line prints it after its multiplier: a
starting amount, a figure from the returns of 1985 to 2024."""

CAPITAL_GAINS_DEDUCTIONS_1988_AND_1989_ELIGIBLE_CAPITAL_PROPERTY = CATALOG.declare(
    "capital_gains_deductions_1988_and_1989_eligible_capital_property", Decimal, non_negative=True
)
"""Capital gains deductions claimed for 1988 and 1989 for eligible capital property, Form T1436
(Capital Gains Worksheet) line 3, as the line prints it after its multiplier: a starting amount,
a figure from the returns of 1985 to 2024."""

CAPITAL_GAINS_DEDUCTIONS_1990_TO_1999 = CATALOG.declare(
    "capital_gains_deductions_1990_to_1999", Decimal, non_negative=True
)
"""Capital gains deductions claimed for 1990 to 1999, Form T1436 (Capital Gains Worksheet) line
4, as the line prints it after its multiplier: a starting amount, a figure from the returns of
1985 to 2024."""

CAPITAL_GAINS_DEDUCTIONS_2000 = CATALOG.declare(
    "capital_gains_deductions_2000", Decimal, non_negative=True
)
"""Capital gains deductions claimed for 2000, Form T1436 (Capital Gains Worksheet) line 5, as
the line prints it after its multiplier: a starting amount, a figure from the returns of 1985 to
2024."""

CAPITAL_GAINS_DEDUCTIONS_2001_TO_2024 = CATALOG.declare(
    "capital_gains_deductions_2001_to_2024", Decimal, non_negative=True
)
"""Capital gains deductions claimed for 2001 to 2024, Form T1436 (Capital Gains Worksheet) line
6, as the line prints it after its multiplier: a starting amount, a figure from the returns of
1985 to 2024."""

CAPITAL_GAINS_DEDUCTIONS_CLAIMED_1985_TO_2024 = CATALOG.declare(
    "capital_gains_deductions_claimed_1985_to_2024", Decimal, non_negative=True
)
"""Total capital gains deductions claimed from 1985 to 2024, Form T1436 (Capital Gains Worksheet)
line 7 "Add lines 1 to 6.": the sum of the six deductions claimed in earlier years."""

OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_1994 = CATALOG.declare(
    "other_business_investment_loss_reductions_1986_to_1994", Decimal, non_negative=True
)
"""Other business investment loss reductions for 1986 to 1994, Form T1436 (Capital Gains
Worksheet) line 8: a starting amount, a figure from the returns of 1986 to 2024."""

OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1994_TO_1996 = CATALOG.declare(
    "other_business_investment_loss_reductions_1994_to_1996", Decimal, non_negative=True
)
"""Other business investment loss reductions for 1994 to 1996, Form T1436 (Capital Gains
Worksheet) line 9: a starting amount, a figure from the returns of 1986 to 2024."""

OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1997_TO_1999 = CATALOG.declare(
    "other_business_investment_loss_reductions_1997_to_1999", Decimal, non_negative=True
)
"""Other business investment loss reductions for 1997 to 1999, Form T1436 (Capital Gains
Worksheet) line 10: a starting amount, a figure from the returns of 1986 to 2024."""

OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2000 = CATALOG.declare(
    "other_business_investment_loss_reductions_2000", Decimal, non_negative=True
)
"""Other business investment loss reductions for 2000, Form T1436 (Capital Gains Worksheet) line
11: a starting amount, a figure from the returns of 1986 to 2024."""

OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2001_TO_2023 = CATALOG.declare(
    "other_business_investment_loss_reductions_2001_to_2023", Decimal, non_negative=True
)
"""Other business investment loss reductions for 2001 to 2023, Form T1436 (Capital Gains
Worksheet) line 12: a starting amount, a figure from the returns of 1986 to 2024."""

OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2024 = CATALOG.declare(
    "other_business_investment_loss_reductions_2024", Decimal, non_negative=True
)
"""Other business investment loss reductions for 2024, Form T1436 (Capital Gains Worksheet) line
13: a starting amount, a figure from the returns of 1986 to 2024."""

OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_2024 = CATALOG.declare(
    "other_business_investment_loss_reductions_1986_to_2024", Decimal, non_negative=True
)
"""Total other business investment loss reductions for 1986 to 2024, Form T1436 (Capital Gains
Worksheet) line 14 "Add lines 8 to 13.": the sum of the six reductions of earlier years."""

BUSINESS_INVESTMENT_LOSS_REDUCTION_AVAILABLE = CATALOG.declare(
    "business_investment_loss_reduction_available", Decimal
)
"""Business investment loss reduction available, Form T1436 (Capital Gains Worksheet) line 15 "Line
7 minus line 14": the capital gains deductions claimed less the other reductions. The line prints no
"(if negative, enter "0")", so the kind is signed."""

BUSINESS_INVESTMENT_LOSS = CATALOG.declare("business_investment_loss", Decimal, non_negative=True)
"""Business investment loss in 2025, Form T1436 line 16 and T1 line 43 gross, line 21699 "Enter
this amount on line 21699 of your return.": a starting amount."""

BUSINESS_INVESTMENT_LOSS_REDUCTION = CATALOG.declare("business_investment_loss_reduction", Decimal)
"""Business investment loss reduction, Form T1436 (Capital Gains Worksheet) line 17 "Enter whichever
is less: amount from line 15 or line 16. Enter this amount on line 17800 of Schedule 3.": the lesser
of the reduction available and the loss. The line prints no floor, so the kind is signed (negative
with line 15)."""

BUSINESS_INVESTMENT_LOSS_AFTER_REDUCTION = CATALOG.declare(
    "business_investment_loss_after_reduction", Decimal, non_negative=True
)
"""Business investment loss after the reduction, Form T1436 (Capital Gains Worksheet) line 18 "Line
16 minus line 17 Business investment loss reduction": never negative, as line 17 is at most line
16."""

ALLOWABLE_BUSINESS_INVESTMENT_LOSS = CATALOG.declare(
    "allowable_business_investment_loss", Decimal, non_negative=True
)
"""Allowable business investment loss, T1 line 43 and line 21700, Form T1436 line 20 "Line 18
multiplied by the percentage on line 19 Enter this amount on line 21700 of your return.": half
the loss after the reduction, a deduction from total income."""

SUPPORT_PAYMENTS_DEDUCTION = CATALOG.declare(
    "support_payments_deduction", Decimal, non_negative=True
)
"""Support payments made, T1 line 45 and line 22000 "Enter on line 22000 of your return the
deductible part of the support payments that you made.": the deductible part, a starting amount
as the return asks for it. The total of line 21999 informs it and nothing on this return reads
it."""

TOTAL_CARRYING_CHARGES = CATALOG.declare("total_carrying_charges", Decimal, non_negative=True)
"""Total carrying charges, Federal Worksheet "Line 22100 - Carrying charges, interest expenses,
and other expenses" line 1: a starting amount."""

TOTAL_INTEREST_EXPENSES = CATALOG.declare("total_interest_expenses", Decimal, non_negative=True)
"""Total interest expenses, Federal Worksheet "Line 22100 - Carrying charges, interest expenses,
and other expenses" line 2: a starting amount."""

TOTAL_OTHER_EXPENSES = CATALOG.declare("total_other_expenses", Decimal, non_negative=True)
"""Total other expenses, Federal Worksheet "Line 22100 - Carrying charges, interest expenses,
and other expenses" line 3: a starting amount."""

CARRYING_CHARGES_INTEREST_EXPENSES_AND_OTHER_EXPENSES = CATALOG.declare(
    "carrying_charges_interest_expenses_and_other_expenses", Decimal, non_negative=True
)
"""Carrying charges, interest expenses, and other expenses, T1 line 46 and line 22100: Federal
Worksheet "Line 22100 - Carrying charges, interest expenses, and other expenses" line 4 "Add
lines 1 to 3. Enter this amount on line 22100 of your return.", a deduction from total income."""

CPP_FIRST_ADDITIONAL_CONTRIBUTIONS = CATALOG.declare(
    "cpp_first_additional_contributions", Decimal, non_negative=True
)
"""First additional CPP contributions, Schedule 8 Part 3 line 12 "amount from line 7 multiplied
by 1% (maximum $678.00)": the required contributions on the employment income between the basic
exemption and the maximum pensionable earnings. Line 18 is "Amount from line 12"; Part 3b line 37
"If line 19 is positive or "0", enter the amount from line 18 at line 37 and line 43, and continue
at line 44." carries it into line 48 (Part 3a line 26 into line 28 when line 24 is positive).

Line 7 is "Line 5 minus line 6 (if negative, enter "0") (maximum $67,800)", the same earnings
as the base contributions'.
"""

CPP_SECOND_ADDITIONAL_CONTRIBUTIONS = CATALOG.declare(
    "cpp_second_additional_contributions", Decimal, non_negative=True
)
"""Second additional CPP contributions, Schedule 8 Part 3 line 22 "amount from line 4 multiplied
by 4% (maximum $396.00)": the required contributions on the employment income between the
maximum and the additional maximum pensionable earnings. Part 3b line 44 "If line 23 is positive
or "0", enter the amount from line 22 on line 44 and line 47, and continue at line 48." carries it
into line 48 (Part 3a line 27 "Amount from line 22 (if any)" into line 28 when line 24 is
positive).

Line 4 is "Line 2 minus line 3 (if negative, enter "0")": the earnings, at most the additional
maximum (line 2), less the maximum pensionable earnings (line 3).
"""

CPP_ENHANCED_CONTRIBUTIONS = CATALOG.declare(
    "cpp_enhanced_contributions", Decimal, non_negative=True
)
"""Enhanced CPP contributions, Schedule 8 Part 3b line 48 "Line 43 plus line 47 Enter this amount
(in dollars and cents) on line 22215 of your return.": the first and second additional
contributions together, the T1 line 22215 deduction from total income (not a credit).

When line 24 is positive, Part 3a line 28 "Line 26 plus line 27 Enter this amount (in dollars and
cents) on line 22215 of your return." carries the same sum.
"""

EXPLORATION_AND_DEVELOPMENT_EXPENSES = CATALOG.declare(
    "exploration_and_development_expenses", Decimal, non_negative=True
)
"""Exploration and development expenses, T1 line 49 and line 22400 "Exploration and development
expenses (complete Form T1229)": a starting amount until CRA publishes a 2025 edition of Form
T1229 (the latest is 2023)."""

OTHER_DEDUCTIONS = CATALOG.declare("other_deductions", Decimal, non_negative=True)
"""Other deductions, T1 line 52 and line 23200 "Other deductions": a starting amount, which
includes the RDSP income repayment (a starting amount of its own, Federal Worksheet for line
25000 line 7)."""

DEDUCTIONS_FROM_TOTAL_INCOME = CATALOG.declare(
    "deductions_from_total_income", Decimal, non_negative=True
)
"""Total deductions, T1 line 23300 "Add lines 35 to 52": the sum of the deductions from total
income, here, in line order, the RPP deduction (line 20700), the RRSP deduction (line 20800), the
FHSA deduction (line 20805), the elected split-pension deduction (line 21000), union dues (line
21200), the UCCB repayment (line 21300), the child care expenses (line 21400), the allowable
business investment loss (line 21700), the deductible support payments (line 22000), carrying
charges, interest expenses and other expenses (line 22100), the enhanced CPP contributions (line
22215), exploration and development expenses (line 22400) and other deductions (line 23200).

Not wired yet: lines 21500, 21900, 22200, 22900 and 23100."""

NET_INCOME_BEFORE_ADJUSTMENTS = CATALOG.declare("net_income_before_adjustments", Decimal)
"""Net income before adjustments, T1 line 54 and line 23400 "Line 34 minus line 53 (if negative,
show in brackets)": total income less total deductions, not floored, so the kind is signed."""

NET_INCOME = CATALOG.declare("net_income", Decimal, non_negative=True)
"""Net income, T1 line 23600 "Line 54 minus line 55 (if negative, enter "0") Net income": total
income less total deductions, not below zero.

Line 54 (23400, net income before adjustments) is its own kind, not floored; line 55 (23500,
social benefits repayment) is not modelled.
"""

CANADIAN_ARMED_FORCES_AND_POLICE_DEDUCTION = CATALOG.declare(
    "canadian_armed_forces_and_police_deduction", Decimal, non_negative=True
)
"""Canadian Armed Forces personnel and police deduction, T1 line 58 and line 24400 "Canadian Armed
Forces personnel and police deduction (box 43 of all T4 slips)": a starting amount."""

SECURITY_OPTIONS_DEDUCTIONS = CATALOG.declare(
    "security_options_deductions", Decimal, non_negative=True
)
"""Security options deductions, T1 line 59 and line 24900 "Security options deductions (boxes 39,
41, 91 and 92 of all T4 slips or see Form T1212)": a starting amount."""

UCCB_REPAYMENT = CATALOG.declare("uccb_repayment", Decimal, non_negative=True)
"""UCCB repayment, T1 line 40 and line 21300 "Universal child care benefit (UCCB) repayment (box 12
of all RC62 slips)", also Federal Worksheet "Line 25000 - Other payments deduction" line 6 "Amount
from line 21300 of your return": a starting amount, a deduction from total income."""

RDSP_INCOME_REPAYMENT = CATALOG.declare("rdsp_income_repayment", Decimal, non_negative=True)
"""RDSP income repayment, Federal Worksheet "Line 25000 - Other payments deduction" line 7 "RDSP
income repayment (included in the amount on line 23200 of your return)": a starting amount."""

UCCB_AND_RDSP_INCOME = CATALOG.declare("uccb_and_rdsp_income", Decimal, non_negative=True)
"""UCCB and RDSP income, Federal Worksheet "Line 25000 - Other payments deduction" line 4 "Line 2
plus line 3 =": the amount from line 11700 of the return (line 2) and the amount from line 12500
(line 3)."""

NET_INCOME_LESS_UCCB_AND_RDSP_INCOME = CATALOG.declare(
    "net_income_less_uccb_and_rdsp_income", Decimal
)
"""Net income less the UCCB and RDSP income, Federal Worksheet "Line 25000 - Other payments
deduction" line 5 "Line 1 minus line 4 =": the net income (line 1, "Amount from line 23400 of your
return (if negative, enter "0")") less line 4.

The form prints no "(if negative, enter "0")" on line 5, so the kind is signed.
"""

UCCB_AND_RDSP_INCOME_REPAYMENTS = CATALOG.declare(
    "uccb_and_rdsp_income_repayments", Decimal, non_negative=True
)
"""UCCB and RDSP income repayments, Federal Worksheet "Line 25000 - Other payments deduction" line
8 "Line 6 plus line 7 =": the UCCB repayment (line 6) and the RDSP income repayment (line 7)."""

OTHER_PAYMENTS_LIMIT_INCOME = CATALOG.declare("other_payments_limit_income", Decimal)
"""Income for the limit, Federal Worksheet "Line 25000 - Other payments deduction" line 9 "Line 5
plus line 8 =": the amount the worksheet compares with $93,454 ("If the amount on line 9 is more
than $93,454, go to canada.ca/line-25000 to find out how much you can deduct.").

The form prints no "(if negative, enter "0")" on line 9, so the kind is signed. The count of line 9
over $93,454 is a starting count, so nothing consumes this line and the manifest returns it.
"""

OTHER_PAYMENTS_WORKSHEET_LINE_9_OVER_LIMIT = CATALOG.declare(
    "other_payments_worksheet_line_9_over_limit", int, non_negative=True
)
"""Line 9 over the limit, Federal Worksheet "Line 25000 - Other payments deduction" "If the amount
on line 9 is more than $93,454, go to canada.ca/line-25000 to find out how much you can deduct.":
a starting count, 1 when line 9 is more than $93,454 and 0 otherwise, until a comparison
capability derives it."""

OTHER_PAYMENTS_DEDUCTION_ABOVE_LIMIT = CATALOG.declare(
    "other_payments_deduction_above_limit", Decimal, non_negative=True
)
"""Other payments deduction above the limit, Federal Worksheet "Line 25000 - Other payments
deduction" "go to canada.ca/line-25000 to find out how much you can deduct": the amount that
chart gives when line 9 is more than $93,454, a starting amount."""

OTHER_PAYMENTS_DEDUCTION_AFTER_LIMIT = CATALOG.declare(
    "other_payments_deduction_after_limit", Decimal, non_negative=True
)
"""Other payments deduction after the limit, Federal Worksheet "Line 25000 - Other payments
deduction" "Otherwise, enter the amount from line 14700 of your return on line 25000 of your
return.": line 14700 when line 9 is not more than $93,454, else the amount the canada.ca/line-25000
chart gives."""

OTHER_PAYMENTS_WORKSHEET_REQUIRED = CATALOG.declare(
    "other_payments_worksheet_required", int, non_negative=True
)
"""Worksheet required, T1 line 60 and line 25000 "Other payments deduction (enter the amount from
line 14700 if you did not enter an amount on line 14600; otherwise, use Federal Worksheet)": a
starting count, 1 when an amount was entered on line 14600 and 0 otherwise, until a comparison
capability derives it."""

OTHER_PAYMENTS_DEDUCTION = CATALOG.declare("other_payments_deduction", Decimal, non_negative=True)
"""Other payments deduction, T1 line 60 and line 25000 "Other payments deduction (enter the amount
from line 14700 if you did not enter an amount on line 14600; otherwise, use Federal Worksheet)":
line 14700 when no amount was entered on line 14600, else the Federal Worksheet's result."""
