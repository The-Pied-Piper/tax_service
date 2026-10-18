"""The federal Canada artifact catalog: artifact kinds named from Canada's own return (§2, §7).

Only the kinds in use are declared, each non-negative: none of these lines can be negative on the
return as modelled (the balance owing, where negative means a refund, will be unconstrained).
Identifiers are stable: `tests/jurisdictions/ca/test_catalog.py` snapshots them.
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

RRSP_DEDUCTION = CATALOG.declare("rrsp_deduction", Decimal, non_negative=True)
"""RRSP deduction, Schedule 7 line 20 "Enter whichever is less: amount from line 10 or line 19.
Enter this amount on line 20800 of your return. RRSP deduction": the lesser of the contributions
available to deduct and the deduction limit, the T1 line 20800 deduction from total income.

Line 10 is "Line 6 minus line 9 Contributions available to deduct"; line 17 "Enter whichever is
less: amount from line 13 or line 16."; line 18 "Enter your RRSP, PRPP, or SPP contributions you
are deducting for 2025 (cannot be more than the amount on line 17)."; line 19 "Line 15 plus line
18". With lines 12 and 15 at 0 and line 18 the full line 17, line 19 is the lesser of the
contributions available to deduct and the limit. Not triggered by the returns modelled: HBP and
LLP repayments (lines 7 to 9), employer PRPP contributions (line 12), transfers (line 15) and
deducting less than line 17 (line 18).
"""

UNION_DUES = CATALOG.declare("union_dues", Decimal, non_negative=True)
"""Union dues, T1 line 21200 "Annual union, professional, or like dues (receipts and box 44 of all
T4 slips)": the amount claimed, a starting amount."""

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
income, here the RRSP deduction, union dues and the enhanced CPP contributions."""

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
$16,129. Otherwise, use the Federal Worksheet to calculate the amount to enter. (maximum
$16,129)": the amount claimed, the first part of the total of the credit amounts.

The reduction for net income above $177,882 is not modelled, so the claimed amount is the full
amount.
"""

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
of the credit amounts the rate is applied to once, here the basic personal amount, the base CPP
contributions, the EI premiums and the Canada employment amount."""

NON_REFUNDABLE_TAX_CREDITS = CATALOG.declare(
    "non_refundable_tax_credits", Decimal, non_negative=True
)
"""Federal non-refundable tax credits, T1 line 118 (line 35000) "Add lines 115 to 117. Total
federal non-refundable tax credits": the total of the credit amounts times the credit rate, here
line 115 (line 33800) alone, since lines 116 and 117 are not triggered."""

FEDERAL_TAX_AFTER_CREDITS = CATALOG.declare("federal_tax_after_credits", Decimal, non_negative=True)
"""Federal basic tax less federal non-refundable tax credits, not below zero.

Its T1 line reference is still to be confirmed: design.md §2 marks federal line semantics
UNVERIFIED.
"""
