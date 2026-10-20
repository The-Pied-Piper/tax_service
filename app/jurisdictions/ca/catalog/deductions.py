"""The federal catalog: deductions from total income.

The split pension, union dues, child care, capital gains deduction, business investment loss,
support, carrying charges, CPP and other deduction lines, down to net income and the repayment lines
that follow it, and the lines of Form T2222 (northern residents deductions) with Chart A and Chart B
of its Step 3, which are record lists.
"""

from __future__ import annotations

from decimal import Decimal

from app.domain.record_list import RecordListKind
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

ZONE_A_DAYS_LIVED = CATALOG.declare("zone_a_days_lived", int, non_negative=True)
"""Zone A days lived, Form T2222 Step 2 line 1 "Enter the number of days you lived in a prescribed
northern zone in 2025.": a starting count of days."""

ZONE_A_ADDITIONAL_RESIDENCY_DAYS = CATALOG.declare(
    "zone_a_additional_residency_days", int, non_negative=True
)
"""Zone A days for the additional residency amount, Form T2222 Step 2 line 2 "Enter the number of
days you qualify for the additional residency amount in 2025.": a starting count of days."""

ZONE_A_BASIC_RESIDENCY_AMOUNT = CATALOG.declare(
    "zone_a_basic_residency_amount", Decimal, non_negative=True
)
"""Zone A basic residency amount, Form T2222 Step 2 line 1 "Enter the number of days you lived in
a prescribed northern zone in 2025. multiplied by $11.00 =": the days of line 1 times $11.00."""

ZONE_A_ADDITIONAL_RESIDENCY_AMOUNT = CATALOG.declare(
    "zone_a_additional_residency_amount", Decimal, non_negative=True
)
"""Zone A additional residency amount, Form T2222 Step 2 line 2 "Enter the number of days you
qualify for the additional residency amount in 2025. multiplied by $11.00 =": the days of line 2
times $11.00."""

ZONE_A_RESIDENCY_AMOUNT = CATALOG.declare("zone_a_residency_amount", Decimal, non_negative=True)
"""Zone A residency amount, Form T2222 Step 2 line 3 and line 67490 "Line 1 plus line 2 =": the
basic and the additional residency amounts of Zone A."""

ZONE_A_SPECIAL_WORK_SITE_BENEFITS = CATALOG.declare(
    "zone_a_special_work_site_benefits", Decimal, non_negative=True
)
"""Zone A special work site benefits, Form T2222 Step 2 line 4 and line 67507 "If you worked at a
special work site, enter the amount from box 31 of your T4 slip or box 124 of your T4A slip that
represents the non-taxable benefits for board and lodging at the special work site.": a starting
amount. The site's location within 30 kilometres of a population centre is the filer's to apply."""

ZONE_A_RESIDENCY_AFTER_WORK_SITE = CATALOG.declare(
    "zone_a_residency_after_work_site", Decimal, non_negative=True
)
"""Zone A residency amount after the work site benefits, Form T2222 Step 2 line 5 "Line 3 minus
line 4 (if negative, enter "0") =": line 3 less line 4, not below zero."""

ZONE_B_DAYS_LIVED = CATALOG.declare("zone_b_days_lived", int, non_negative=True)
"""Zone B days lived, Form T2222 Step 2 line 6 "Enter the number of days you lived in an
intermediate zone in 2025.": a starting count of days."""

ZONE_B_ADDITIONAL_RESIDENCY_DAYS = CATALOG.declare(
    "zone_b_additional_residency_days", int, non_negative=True
)
"""Zone B days for the additional residency amount, Form T2222 Step 2 line 7 "Enter the number of
days you qualify for the additional residency amount in 2025.": a starting count of days."""

ZONE_B_BASIC_RESIDENCY_AMOUNT = CATALOG.declare(
    "zone_b_basic_residency_amount", Decimal, non_negative=True
)
"""Zone B basic residency amount, Form T2222 Step 2 line 6 "Enter the number of days you lived in
an intermediate zone in 2025. multiplied by $5.50 =": the days of line 6 times $5.50."""

ZONE_B_ADDITIONAL_RESIDENCY_AMOUNT = CATALOG.declare(
    "zone_b_additional_residency_amount", Decimal, non_negative=True
)
"""Zone B additional residency amount, Form T2222 Step 2 line 7 "Enter the number of days you
qualify for the additional residency amount in 2025. multiplied by $5.50 =": the days of line 7
times $5.50."""

ZONE_B_RESIDENCY_AMOUNT = CATALOG.declare("zone_b_residency_amount", Decimal, non_negative=True)
"""Zone B residency amount, Form T2222 Step 2 line 8 and line 67520 "Line 6 plus line 7 =": the
basic and the additional residency amounts of Zone B."""

ZONE_B_SPECIAL_WORK_SITE_BENEFITS = CATALOG.declare(
    "zone_b_special_work_site_benefits", Decimal, non_negative=True
)
"""Zone B special work site benefits, Form T2222 Step 2 line 9 and line 67529 "If you worked at a
special work site, enter the amount from box 31 of your T4 slip or box 124 of your T4A slip that
represents the non-taxable benefits for board and lodging at the special work site.": a starting
amount. The site's location within 30 kilometres of a population centre is the filer's to apply."""

ZONE_B_RESIDENCY_AFTER_WORK_SITE = CATALOG.declare(
    "zone_b_residency_after_work_site", Decimal, non_negative=True
)
"""Zone B residency amount after the work site benefits, Form T2222 Step 2 line 10 "Line 8 minus
line 9 (if negative, enter "0") =": line 8 less line 9, not below zero."""

RESIDENCY_AMOUNT = CATALOG.declare("residency_amount", Decimal, non_negative=True)
"""Residency amount, Form T2222 Step 2 line 11 "Line 5 plus line 10 =": the Zone A and Zone B
amounts after the work site benefits."""

RESIDENCY_NET_INCOME_LIMIT = CATALOG.declare(
    "residency_net_income_limit", Decimal, non_negative=True
)
"""Residency limit on net income, Form T2222 Step 2 line 12 "Enter your net income from line 23600
of your return. multiplied by 20%  =": the net income times 20%."""

RESIDENCY_DEDUCTION = CATALOG.declare("residency_deduction", Decimal, non_negative=True)
"""Residency deduction, Form T2222 Step 2 line 13 "Enter whichever is less: amount from line 11 or
line 12. Residency deduction": the lesser of lines 11 and 12; line 17 of Step 4 is this amount."""

TRAVEL_INDIVIDUAL = CATALOG.declare("travel_individual", int, non_negative=True)
"""Individual, Form T2222 Step 3 Chart A "Row A: Enter the name of each individual, including
yourself, whose travel you are claiming." and Chart B "Column 1: Enter the name of the person who
took the trip.": a count, the number the filer gives each individual, which only names the
individual and which no capability reads."""

TRIP_ZONE = CATALOG.declare("trip_zone", int, non_negative=True)
"""Zone of a trip, Form T2222 Step 3 Chart B "Enter the lowest amount from column 3, 4, or 5 in the
column for the prescribed zone(s) you resided in at the time of the trip.": a count, 1 for Zone A
(column 6) and 2 for Zone B (column 7)."""

TRIP_BENEFIT_OR_STANDARD_AMOUNT = CATALOG.declare(
    "trip_benefit_or_standard_amount", Decimal, non_negative=True
)
"""Benefit or standard amount of a trip, Form T2222 Step 3 Chart B "Column 3: Enter either the
taxable travel benefit or the portion of the individual's $1,200 standard amount for the trip.":
an input for each trip."""

TRIP_TRAVEL_EXPENSES = CATALOG.declare("trip_travel_expenses", Decimal, non_negative=True)
"""Travel expenses of a trip, Form T2222 Step 3 Chart B "Column 4: Enter the amount of travel
expenses for each trip taken.": an input for each trip."""

TRIP_LOWEST_RETURN_AIRFARE = CATALOG.declare(
    "trip_lowest_return_airfare", Decimal, non_negative=True
)
"""Lowest return airfare of a trip, Form T2222 Step 3 Chart B "Column 5: Enter the cost of the
lowest return airfare.": an input for each trip."""

TRAVEL_TRIPS = RecordListKind.declare(
    CATALOG,
    "travel_trips",
    fields=(
        TRAVEL_INDIVIDUAL,
        TRIP_ZONE,
        TRIP_BENEFIT_OR_STANDARD_AMOUNT,
        TRIP_TRAVEL_EXPENSES,
        TRIP_LOWEST_RETURN_AIRFARE,
    ),
)
"""Trips, Form T2222 Step 3 Chart B, one record for each trip: the individual who took it ("Column
1"), the zone whose column the amount goes in, and "Column 3", "Column 4" and "Column 5". A starting
list, possibly empty."""

STANDARD_AMOUNT_ALLOCATED_1 = CATALOG.declare(
    "standard_amount_allocated_1", Decimal, non_negative=True
)
"""First allocation of the standard amount, Form T2222 Step 3 Chart A "Row B: Enter the name of
everyone (including yourself) who is claiming a deduction for trips taken by the individual in row
A and the total portion of the $1,200 standard amount allocated by each claimant for all trips
taken by that individual.": the first claimant's portion, an input."""

STANDARD_AMOUNT_ALLOCATED_2 = CATALOG.declare(
    "standard_amount_allocated_2", Decimal, non_negative=True
)
"""Second allocation of the standard amount, Form T2222 Step 3 Chart A row B: the second
claimant's portion, an input."""

STANDARD_AMOUNT_ALLOCATED_3 = CATALOG.declare(
    "standard_amount_allocated_3", Decimal, non_negative=True
)
"""Third allocation of the standard amount, Form T2222 Step 3 Chart A row B: the third claimant's
portion, an input."""

TRAVEL_INDIVIDUALS = RecordListKind.declare(
    CATALOG,
    "travel_individuals",
    fields=(
        TRAVEL_INDIVIDUAL,
        STANDARD_AMOUNT_ALLOCATED_1,
        STANDARD_AMOUNT_ALLOCATED_2,
        STANDARD_AMOUNT_ALLOCATED_3,
    ),
)
"""Individuals, Form T2222 Step 3 Chart A "Row A: Enter the name of each individual, including
yourself, whose travel you are claiming.", one record for each individual with the three amounts of
"Row B". A starting list, possibly empty."""

STANDARD_AMOUNT_ALLOCATED = CATALOG.declare("standard_amount_allocated", Decimal, non_negative=True)
"""Standard amount allocated, Form T2222 Step 3 Chart A "Row C: Enter the total of all amounts in
row B. This total cannot be more than $1,200.": row C added over the individuals. No line of the
form reads it, so the manifest returns it."""

TRAVEL_TOTAL_ZONE_A = CATALOG.declare("travel_total_zone_a", Decimal, non_negative=True)
"""Zone A total of the trips, Form T2222 Step 3 Chart B "(A) Total (add all the amounts under
Column 6) =", line 14 and line 67540 "Amount A of Chart B"."""

TRAVEL_TOTAL_ZONE_B = CATALOG.declare("travel_total_zone_b", Decimal, non_negative=True)
"""Zone B total of the trips, Form T2222 Step 3 Chart B "(B) Total (add all the amounts under
Column 7) =", read by line 15 "Enter the total from box B. Line 67560"."""

TRAVEL_ZONE_B_DEDUCTION = CATALOG.declare("travel_zone_b_deduction", Decimal, non_negative=True)
"""Zone B travel amount, Form T2222 Step 3 line 15 "Enter the total from box B. Line 67560
multiplied by 50% =": the Zone B total times 50%."""

TRAVEL_DEDUCTION = CATALOG.declare("travel_deduction", Decimal, non_negative=True)
"""Travel deduction, Form T2222 Step 3 line 16 "Line 14 plus line 15 Travel deduction =": the Zone
A total (line 14) and line 15; line 18 of Step 4 is this amount."""

NORTHERN_RESIDENTS_DEDUCTIONS = CATALOG.declare(
    "northern_residents_deductions", Decimal, non_negative=True
)
"""Northern residents deductions, Form T2222 Step 4 line 19 "Line 17 plus line 18 Enter this amount
on line 25500 of your return. Northern residents deductions =" and T1 line 66 and line 25500
"Northern residents deductions (complete Form T2222)": the residency deduction (line 17) and the
travel deduction (line 18)."""
