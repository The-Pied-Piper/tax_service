"""The federal Canada artifact catalog: artifact kinds named from Canada's own return (§2, §7).

Only the kinds in use are declared, each non-negative but one: none of these lines can be negative
on the return as modelled except the refund or balance owing, where negative means a refund.
Amounts are Decimal; the counts of eligible dependants, of infirm children, of the eligible
children for child care (Form T778 Part B lines 1 to 3) and of the Schedule 6 eligible dependants
(line 38100) int. Identifiers are stable: `tests/jurisdictions/ca/test_catalog.py` snapshots them.
"""

from __future__ import annotations

from decimal import Decimal

from app.domain.artifact import ArtifactCatalog
from app.domain.registry import Namespace
from app.jurisdictions.ca import NAMESPACE

CATALOG = ArtifactCatalog(Namespace(NAMESPACE))

EMPLOYMENT_INCOME = CATALOG.declare("employment_income", Decimal, non_negative=True)
"""Employment income, T1 line 10100: a starting amount that total income sums directly."""

CAPITAL_GAIN = CATALOG.declare("capital_gain", Decimal, non_negative=True)
"""The claimed capital gain before inclusion, mirroring Schedule 3 line 21 (total capital gains
or losses).

Losses, and netting gains against them, are not modelled yet, so the kind is declared
non-negative; net gains or losses, when modelled, will be a different kind.
"""

TAXABLE_CAPITAL_GAINS = CATALOG.declare("taxable_capital_gains", Decimal, non_negative=True)
"""Taxable capital gains, T1 line 12700: the capital gain times the inclusion rate (Schedule 3
lines 23 to 26)."""

TOTAL_INCOME = CATALOG.declare("total_income", Decimal, non_negative=True)
"""Total income, T1 line 15000: the sum of the income lines, here employment income and taxable
capital gains."""

UNUSED_RRSP_CONTRIBUTIONS = CATALOG.declare("unused_rrsp_contributions", Decimal, non_negative=True)
"""Unused RRSP contributions, Schedule 7 line 1 "Enter your unused RRSP contributions previously
reported and available to deduct for 2025 as shown on your latest notice of assessment or
reassessment, or Form T1028 for 2025": the contributions previously reported and not yet
deducted, a starting amount."""

RRSP_CONTRIBUTIONS = CATALOG.declare("rrsp_contributions", Decimal, non_negative=True)
"""RRSP contributions, Schedule 7 line 4 (line 24500) "Line 2 plus line 3": the contributions made
from March 4, 2025, to March 2, 2026, a starting amount.

Line 2 is "Enter contributions made to your RRSP, SPP or PRPP, or to your spouse's or common-law
partner's RRSP or SPP from March 4, 2025, to December 31, 2025 (attach all receipts)."; line 3 is
the same contributions "from January 1, 2026, to March 2, 2026".
"""

RRSP_CONTRIBUTIONS_AVAILABLE = CATALOG.declare(
    "rrsp_contributions_available", Decimal, non_negative=True
)
"""RRSP contributions available to deduct, Schedule 7 line 10 "Line 6 minus line 9 Contributions
available to deduct": the unused contributions plus the contributions.

Line 5 is "Line 1 plus line 4 ... Total contributions"; line 6 "Total contributions from line 5".
With line 9 at 0, line 10 is line 5. Not triggered by the returns modelled: HBP and LLP repayments
(lines 7 to 9).
"""

RRSP_DEDUCTION_LIMIT = CATALOG.declare("rrsp_deduction_limit", Decimal, non_negative=True)
"""RRSP deduction limit, Schedule 7 line 11 "Enter your RRSP deduction limit for 2025 as shown on
your latest notice of assessment or reassessment, or Form T1028 for 2025.": a starting amount."""

RRSP_DEDUCTION_MAXIMUM = CATALOG.declare("rrsp_deduction_maximum", Decimal, non_negative=True)
"""RRSP deduction maximum, Schedule 7 line 17 "Enter whichever is less: amount from line 13 or line
16.": the lesser of the contributions available to deduct and the deduction limit, the most that
may be deducted.

Line 13 is "Line 11 minus line 12"; line 16 "Line 14 minus line 15". With lines 12 and 15 at 0,
line 13 is the limit and line 16 the contributions available to deduct. Not triggered by the
returns modelled: employer PRPP contributions (line 12) and transfers (line 15).
"""

RRSP_AMOUNT_DEDUCTED = CATALOG.declare("rrsp_amount_deducted", Decimal, non_negative=True)
"""RRSP amount deducted, Schedule 7 line 18 "Enter your RRSP, PRPP, or SPP contributions you are
deducting for 2025 (cannot be more than the amount on line 17).": the amount the filer chooses to
deduct, a starting amount, refused when above line 17."""

RRSP_DEDUCTION = CATALOG.declare("rrsp_deduction", Decimal, non_negative=True)
"""RRSP deduction, Schedule 7 line 20 "Enter whichever is less: amount from line 10 or line 19.
Enter this amount on line 20800 of your return. RRSP deduction": the amount deducted, at most the
deduction maximum, the T1 line 20800 deduction from total income.

Line 19 is "Line 15 plus line 18". With line 15 at 0, line 19 is line 18, at most line 17 and so
at most line 10, and line 20 is line 18 itself. Not triggered by the returns modelled: transfers
(line 15).
"""

UNUSED_RRSP_CONTRIBUTIONS_CARRIED_FORWARD = CATALOG.declare(
    "unused_rrsp_contributions_carried_forward", Decimal, non_negative=True
)
"""Unused RRSP contributions carried forward, Schedule 7 line 23 "Line 21 minus line 22 Your unused
contributions available to carry forward to a future year": the contributions available to deduct
less the RRSP deduction, a product of the return for the next year's line 1.

Line 21 is "Enter your contributions available to deduct from line 10 of the previous page."; line
22 "Enter your RRSP deduction from line 20 of the previous page.". Never negative, as line 20 is
at most line 10.
"""

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

DEDUCTIONS_FROM_TOTAL_INCOME = CATALOG.declare(
    "deductions_from_total_income", Decimal, non_negative=True
)
"""Total deductions, T1 line 23300 "Add lines 35 to 52": the sum of the deductions from total
income, here, in line order, the RRSP deduction (line 20800), union dues (line 21200), the child
care expenses (line 21400) and the enhanced CPP contributions (line 22215)."""

NET_INCOME = CATALOG.declare("net_income", Decimal, non_negative=True)
"""Net income, T1 line 23600 "Line 54 minus line 55 (if negative, enter "0") Net income": total
income less total deductions, not below zero.

Line 54 (23400) is "Line 34 minus line 53 (if negative, show in brackets) Net income before
adjustments"; line 55 (23500, social benefits repayment) is not modelled.
"""

DEDUCTIONS_FROM_NET_INCOME = CATALOG.declare(
    "deductions_from_net_income", Decimal, non_negative=True
)
"""Deductions from net income, T1 line 25700 "Add lines 58 to 67": the sum of the deductions
from net income, lines 58 to 67 (lines 24400 to 25600).

None of those deductions is modelled yet, so the sum has no parts.
"""

TAXABLE_INCOME = CATALOG.declare("taxable_income", Decimal, non_negative=True)
"""Taxable income, T1 line 69 "Line 57 minus line 68 (if negative, enter "0") Taxable income"
(line 26000, as Step 5 refers to it): net income less the deductions from net income, not below
zero; the base the federal and Ontario brackets apply to.

Line 57 is "Enter the amount from line 56 of the previous page" (net income); line 68 (25700) is
"Add lines 58 to 67".
"""

FEDERAL_BASIC_TAX = CATALOG.declare("federal_basic_tax", Decimal, non_negative=True)
"""Federal tax on taxable income from the bracket schedule, before non-refundable credits.

Its T1 line reference is still to be confirmed: design.md §2 marks federal line semantics
UNVERIFIED.
"""

BASIC_PERSONAL_AMOUNT = CATALOG.declare("basic_personal_amount", Decimal, non_negative=True)
"""Basic personal amount, T1 line 30000 "If the amount on line 23600 is $177,882 or less, enter
$16,129. If the amount on line 23600 is $253,414 or more, enter $14,538. Otherwise, use the
Federal Worksheet to calculate the amount to enter. (maximum $16,129)": the first part of the
total of the credit amounts.

It is computed from net income (line 23600) by the Federal Worksheet (form 5000-D1), line 30000:
line 11 "Line 1 plus line 10 Enter this amount on line 30000 of your return. (maximum $16,129)",
the base amount of line 1 plus the supplement amount of line 2 less its reduction for net income
over the income threshold of line 4 (line 10 "Line 2 minus line 9 (if negative, enter "0")").
"""

ELIGIBLE_DEPENDANTS = CATALOG.declare("eligible_dependants", int, non_negative=True)
"""Number of eligible dependants claimed for, T1 line 80 (line 30400) "Amount for an eligible
dependant (complete Schedule 5)": a starting count, 0 or 1.

Schedule 5 states "Each household is allowed only one claim for this amount"; a count is only
declared non-negative, so that rule is the return's to keep, as are the conditions: "You did not
have a spouse or common-law partner or, if you did, you were not living with them, supporting them,
or being supported by them"; "You supported the dependant in 2025"; "You lived with the dependant
(in most cases in Canada) in a home ... you maintained"; the dependant is "your child, grandchild,
brother or sister under 18 years of age" (or "your parent or grandparent", or "your child,
grandchild, brother or sister 18 years of age or older with a mental or physical infirmity"); and
"You had to pay child support in 2025 for the eligible dependant" bars the claim, with exceptions.
Eligibility is not computed here.
"""

DEPENDANT_NET_INCOME = CATALOG.declare("dependant_net_income", Decimal, non_negative=True)
"""Dependant's net income, Schedule 5 line 4 (line 51106) "Dependant's net income from line 23600
of their return": a starting amount, also ON428 line 15 "Your eligible dependant's net income from
line 23600 of their return"."""

ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT = CATALOG.declare(
    "eligible_dependant_amount_before_count", Decimal, non_negative=True
)
"""Amount for an eligible dependant before it is claimed, Schedule 5 line 5 "Line 3 minus line 4
(if negative, enter "0") Enter this amount on line 30400 of your return.": the basic personal
amount (line 1 "Basic personal amount from line 30000 of your return") less the dependant's net
income (line 4), not below zero.

Line 3 is "Line 1 plus line 2"; line 2 "If you are eligible for the Canada caregiver amount for
your dependant (other than your infirm child under 18 years of age), enter $2,687" is not
triggered, so line 3 is line 1.
"""

ELIGIBLE_DEPENDANT_AMOUNT = CATALOG.declare("eligible_dependant_amount", Decimal, non_negative=True)
"""Amount for an eligible dependant, T1 line 80 (line 30400) "Amount for an eligible dependant
(complete Schedule 5)": Schedule 5 line 5 for each eligible dependant claimed for, a part of the
total of the credit amounts."""

INFIRM_CHILDREN = CATALOG.declare("infirm_children", int, non_negative=True)
"""Number of infirm children, T1 line 83 "Number of children you are claiming this amount for Line
30499": a starting count."""

INFIRM_CHILDREN_AMOUNT = CATALOG.declare("infirm_children_amount", Decimal, non_negative=True)
"""Canada caregiver amount for infirm children, T1 line 83 (line 30500) "Canada caregiver amount
for infirm children under 18 years of age (see Schedule 5) Number of children you are claiming
this amount for Line 30499" "multiplied by $2,687", a part of the total of the credit amounts on
the T1 alone (the ON428 caregiver amount, line 58185, is not triggered)."""

CPP_BASE_CONTRIBUTIONS = CATALOG.declare("cpp_base_contributions", Decimal, non_negative=True)
"""Base CPP contributions, Schedule 8 Part 3 line 11 "amount from line 7 multiplied by 4.95%
(maximum $3,356.10)": the required contributions on the employment income between the basic
exemption and the maximum pensionable earnings, a part of the total of the credit amounts on the
T1 and, as ON428 line 19 (line 58240) "Amount from line 30800 of your return", on ON428.

Line 15 is "Amount from line 11"; Part 3b line 30 "If line 16 is positive or "0", enter the amount
from line 15 at line 30 and line 36, and continue at line 37." and line 36 "Line 34 plus line 35.
Enter this amount (in dollars and cents) on line 30800 of your return and line 58240 of your Form
428." carry it to T1 line 30800 and ON428 line 58240, lines 32 and 35 being 0. When line 24 is
positive, Part 3a line 25 "Enter the amount from line 15." carries the same amount.

Line 1 (50339) is "Total CPP pensionable earnings from box 26 of all of your T4 slips (if box 26
is blank, enter the amount from box 14)", so the three contributions read employment income.
Not triggered by the returns modelled: Part 2's proration for fewer than 12 months, box 26
differing from box 14, and the slips' deducted contributions differing from the required ones
(so no overpayment on T1 line 44800).
"""

EI_PREMIUMS = CATALOG.declare("ei_premiums", Decimal, non_negative=True)
"""EI premiums, T1 line 31200 "through employment (boxes 18 and 55 of all T4 slips) (maximum
$1,077.48)": the rate on employment income up to the maximum insurable earnings, a part of the
total of the credit amounts on the T1 and, as ON428 line 21 (line 58300) "Amount from line 31200
of your return", on ON428.

Employment income is taken as the insurable earnings: boxes 18 and 55 of the slip are not
modelled. Not triggered by the returns modelled: the EI overpayment (T1 line 45000).
"""

CANADA_EMPLOYMENT_AMOUNT = CATALOG.declare("canada_employment_amount", Decimal, non_negative=True)
"""Canada employment amount, T1 line 31260 "Enter whichever is less: $1,471 or line 1 plus line
2.": the lesser of the cap and employment income, the fourth part of the total of the credit
amounts on the T1 alone (ON428 has no such line).

Line 1 (10100) is "Employment income (box 14 of all T4 slips)" and line 2 (10400) is "Other
employment income". The returns have no other employment income, so the cap applies to
employment income alone.
"""

NON_REFUNDABLE_CREDIT_AMOUNTS = CATALOG.declare(
    "non_refundable_credit_amounts", Decimal, non_negative=True
)
"""Total of the non-refundable credit amounts, T1 line 33500 "Line 106 plus line 112": the sum
of the credit amounts the rate is applied to once, here, in line order, the basic personal amount
(line 30000), the amount for an eligible dependant (line 30400), the Canada caregiver amount for
infirm children (line 30500), the base CPP contributions (line 30800), the EI premiums (line
31200) and the Canada employment amount (line 31260)."""

NON_REFUNDABLE_TAX_CREDITS = CATALOG.declare(
    "non_refundable_tax_credits", Decimal, non_negative=True
)
"""Federal non-refundable tax credits, T1 line 118 (line 35000) "Add lines 115 to 117. Total
federal non-refundable tax credits": the total of the credit amounts times the credit rate, here
line 115 (line 33800) alone, since lines 116 and 117 are not triggered."""

FEDERAL_TAX_AFTER_CREDITS = CATALOG.declare("federal_tax_after_credits", Decimal, non_negative=True)
"""Basic federal tax, T1 line 126 (line 42900) "Line 121 minus line 125 (if negative, enter "0")
Basic federal tax": the federal basic tax less the federal non-refundable tax credits, not below
zero.

Line 121 (40400) is "Line 119 plus line 120", line 119 "Enter the amount from line 76."; line 125
is "Add lines 122 to 124.", line 122 "Amount from line 35000". Not modelled: line 120 (40424, tax
on split income) and lines 123 and 124 (dividend tax credit, minimum tax carryover).
"""

NET_FEDERAL_TAX = CATALOG.declare("net_federal_tax", Decimal, non_negative=True)
"""Net federal tax, T1 line 142 (line 42000) "Add lines 139 to 141. Net federal tax": the federal
tax after credits carried through the lines between, as nothing else on them is modelled.

Line 126 (42900) is "Line 121 minus line 125 (if negative, enter "0") Basic federal tax", line 121
(40400) "Line 119 plus line 120" and line 125 "Add lines 122 to 124.", line 122 being "Amount from
line 35000": the federal tax after credits. Line 134 (40600) "Line 132 minus line 133 (if
negative, enter "0") Federal tax" and line 139 (41700) "Line 134 minus line 138 (if negative,
enter "0")" carry it to line 142. Not modelled: line 120 (40424, tax on split income), lines 123
and 124 (dividend tax credit, minimum tax carryover), lines 127 to 133 (foreign surtax, foreign
tax credit, investment tax credit recapture, logging tax credit), lines 135 to 138 (political,
investment and labour-sponsored credits, 41600) and lines 140 (41500, advanced Canada workers
benefit) and 141 (41800, special taxes).
"""

TOTAL_PAYABLE = CATALOG.declare("total_payable", Decimal, non_negative=True)
"""Total payable, T1 line 148 (line 43500) "Add lines 143 to 147. Total payable": the net federal
tax plus the provincial tax, in line order.

Line 143 is "Amount from line 42000"; line 147 (42800) "Provincial or territorial tax (complete
and attach your provincial or territorial Form 428, even if the result is "0")". Not triggered by
the returns modelled: lines 144 (42100), 145 (42120) and 146 (42200).
"""

INCOME_TAX_DEDUCTED = CATALOG.declare("income_tax_deducted", Decimal, non_negative=True)
"""Income tax deducted, T1 line 150 (line 43700) "Total income tax deducted (amounts from all
Canadian slips)": a starting amount."""

CWB_ELIGIBLE_DEPENDANTS = CATALOG.declare("cwb_eligible_dependants", int, non_negative=True)
"""Number of eligible dependants for the Canada workers benefit, Schedule 6 Step 1 "Line 38100: Do
you have an eligible dependant? 1 Yes or 2 No": a starting count, 0 or 1, the count of 0 answering
no and of 1 yes.

Schedule 6 defines the eligible dependant by its own conditions: "They were your or your spouse's or
common-law partner's child"; "They were under 19 years of age and lived with you on December 31,
2025 ..."; "They were not eligible for the CWB for 2025". They differ from the eligible dependant
claimed for on T1 line 30400, so a dependant can be one and not the other. A count is only declared
non-negative, so the conditions are the return's to check against its facts; eligibility is not
computed here. Line 38101 "Do you have an eligible spouse? 1 Yes or 2 No" is not modelled.
"""

WORKING_INCOME = CATALOG.declare("working_income", Decimal, non_negative=True)
"""Working income, Schedule 6 line 5 "Add lines 1 to 4. Enter the result, even if it is "0".
Working income": line 1 "Employment income and other employment income from line 10100 and line
10400 of the return", here employment income alone, as line 10400 and lines 2 to 4 (scholarships,
self-employment, exempt income) are not triggered.

With no eligible spouse it is also line 6 "Add the amounts from line 5 in columns 1 and 2. Enter
this amount on line 16. Family working income"."""

ADJUSTED_FAMILY_NET_INCOME = CATALOG.declare(
    "adjusted_family_net_income", Decimal, non_negative=True
)
"""Adjusted family net income, Schedule 6 line 15 "Line 13 minus line 14 Enter this amount on line
23 and line 35. Adjusted family net income": line 7 "Net income from line 23600 of the return",
carried through line 10 "Add lines 7 to 9.", line 12 "Line 10 minus line 11 (if negative, enter
"0")" and line 13 "Add the amounts from line 12 in columns 1 and 2.", as lines 8, 9 and 11 are not
triggered and, with no eligible spouse, neither is line 14 (the secondary earner exemption)."""

CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT = CATALOG.declare(
    "cwb_before_reduction_without_dependant", Decimal, non_negative=True
)
"""Canada workers benefit before its reduction with no eligible spouse and no eligible dependant,
Schedule 6 line 22 "Enter whichever is less: amount from line 20 or line 21.": line 20 "Line 18
multiplied by the percentage from line 19", line 19 "Rate 27%", on line 18 "Line 16 minus line 17
(if negative, enter "0")", the family working income (line 16) over line 17 "Base amount
3,000.00"; line 21 "If you had an eligible spouse or an eligible dependant, enter $2,813. If not,
enter $1,633.", here $1,633.

Schedule 6 states its conditions: "Complete this schedule if you met all of the following
conditions in 2025: You were a resident of Canada throughout the year; You earned working income
(see Part A); You were, at the end of the year, 19 years of age or older, or you resided with your
spouse or common-law partner or your child"; "You cannot claim the CWB for 2025 if any of the
following conditions apply to you: You were enrolled as a full-time student at a designated
educational institution for a total of more than 13 weeks in the year, unless you had an eligible
dependant at the end of the year; You were confined to a prison or similar institution for a period
of at least 90 days during the year; You were exempt from income tax in Canada for a period in the
year when you were an officer or a servant of another country (such as a diplomat) residing in
Canada or you were a family member who resided with such a person or an employee of such a person,
at any time in the year"; and, under line 6, "You can claim the basic CWB in Step 2 if the family
working income on line 6 is more than $3,000." Eligibility is the return's to state, not computed
here. The basic amount only: the disability supplement (Step 3) and advance payments (Step 4) are
not triggered."""

CWB_REDUCTION_WITHOUT_DEPENDANT = CATALOG.declare(
    "cwb_reduction_without_dependant", Decimal, non_negative=True
)
"""Canada workers benefit reduction with no eligible spouse and no eligible dependant, Schedule 6
line 27 "Line 25 multiplied by the percentage from line 26": line 26 "Rate 15%" on line 25 "Line
23 minus line 24 (if negative, enter "0")", line 23 "Adjusted family net income from line 15" over
line 24 "If you had an eligible spouse or an eligible dependant, enter $30,639. If not, enter
$26,855.", here $26,855.

The chart's "Basic CWB: $37,742" limit is not wired: it follows from the arithmetic, as 1,633 less
15% of (37,742 - 26,855) is below zero."""

CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT = CATALOG.declare(
    "canada_workers_benefit_without_dependant", Decimal, non_negative=True
)
"""Canada workers benefit with no eligible spouse and no eligible dependant, Schedule 6 line 28
"Line 22 minus line 27 (if negative, enter "0")": line 22 with $1,633 on line 21, less line 27
with $26,855 on line 24.

Step 3 (the disability supplement) is not triggered."""

CWB_BEFORE_REDUCTION_WITH_DEPENDANT = CATALOG.declare(
    "cwb_before_reduction_with_dependant", Decimal, non_negative=True
)
"""Canada workers benefit before its reduction with an eligible dependant, Schedule 6 line 22
"Enter whichever is less: amount from line 20 or line 21.": line 20 "Line 18 multiplied by the
percentage from line 19", line 19 "Rate 27%", on line 18 "Line 16 minus line 17 (if negative,
enter "0")", the family working income (line 16) over line 17 "Base amount 3,000.00"; line 21 "If
you had an eligible spouse or an eligible dependant, enter $2,813. If not, enter $1,633.", here
$2,813.

An eligible spouse is not modelled; the conditions are Schedule 6's, as for the amount with no
eligible spouse and no eligible dependant."""

CWB_REDUCTION_WITH_DEPENDANT = CATALOG.declare(
    "cwb_reduction_with_dependant", Decimal, non_negative=True
)
"""Canada workers benefit reduction with an eligible dependant, Schedule 6 line 27 "Line 25
multiplied by the percentage from line 26": line 26 "Rate 15%" on line 25 "Line 23 minus line 24
(if negative, enter "0")", line 23 "Adjusted family net income from line 15" over line 24 "If you
had an eligible spouse or an eligible dependant, enter $30,639. If not, enter $26,855.", here
$30,639.

The chart's "You had an eligible spouse or an eligible dependant Basic CWB: $49,393" limit is not
wired: it follows from the arithmetic, as 2,813 less 15% of (49,393 - 30,639) is below zero."""

CANADA_WORKERS_BENEFIT_WITH_DEPENDANT = CATALOG.declare(
    "canada_workers_benefit_with_dependant", Decimal, non_negative=True
)
"""Canada workers benefit with an eligible dependant, Schedule 6 line 28 "Line 22 minus line 27
(if negative, enter "0")": line 22 with $2,813 on line 21, less line 27 with $30,639 on line 24.

Step 3 (the disability supplement) is not triggered."""

CANADA_WORKERS_BENEFIT = CATALOG.declare("canada_workers_benefit", Decimal, non_negative=True)
"""Canada workers benefit, Schedule 6 line 28 "Line 22 minus line 27 (if negative, enter "0") If you
are not completing Step 3, enter this amount on line 45300 of your return.", T1 line 155 (45300)
"Canada workers benefit (CWB) (complete Schedule 6)": line 28 for the filer's family status, which
lines 21 and 24 read ("If you had an eligible spouse or an eligible dependant ... If not ..."),
chosen by the number of Schedule 6 eligible dependants (line 38100): with none, the benefit with no
eligible spouse and no eligible dependant, else the benefit with one. The eligible dependants
claimed for on T1 line 30400 do not choose it, as Schedule 6 defines its eligible dependant by its
own conditions.

An eligible spouse is not modelled: a filer with one and no eligible dependant is computed with the
amounts for no eligible spouse and no eligible dependant, which the form does not give them."""

TOTAL_CREDITS = CATALOG.declare("total_credits", Decimal, non_negative=True)
"""Total credits, T1 line 166 (line 48200) "Add lines 150 to 165. Total credits": here line 150
(43700) and line 155 (45300), in line order.

Not triggered by the returns modelled, or left to later work: the other lines from 151 to 165
(lines 44000 to 47900, among them 44800 CPP overpayment and 45000 EI overpayment).
"""

REFUND_OR_BALANCE_OWING = CATALOG.declare("refund_or_balance_owing", Decimal)
"""Refund or balance owing, T1 line 167 "Line 149 minus line 166 If the amount is negative, enter
it on line 48400 below. If the amount is positive, enter it on line 48500 below. Refund or balance
owing": the total payable less the total credits, both already in cents.

Line 149 is "Enter the amount from line 148 of the previous page.", the total payable. The one
kind not declared non-negative: a negative amount is a refund (line 48400 "Refund"), a positive
one a balance owing (line 48500 "Balance owing"). The line takes amounts already in cents, so it
is in cents without a rounding of its own.
"""
