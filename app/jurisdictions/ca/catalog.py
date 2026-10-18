"""The federal Canada artifact catalog: artifact kinds named from Canada's own return (§2, §7).

Only the kinds in use are declared. Identifiers are stable: `tests/jurisdictions/ca/test_catalog.py`
snapshots them.
"""

from __future__ import annotations

from decimal import Decimal

from app.domain.artifact import ArtifactCatalog
from app.domain.registry import Namespace
from app.jurisdictions.ca import NAMESPACE

CATALOG = ArtifactCatalog(Namespace(NAMESPACE))

EMPLOYMENT_INCOME = CATALOG.declare("employment_income", Decimal)
"""Employment income, T1 line 10100: a starting amount that total income sums directly."""

CAPITAL_GAIN = CATALOG.declare("capital_gain", Decimal)
"""The claimed capital gain before inclusion, mirroring Schedule 3 line 21 (total capital gains
or losses).

Losses, and netting gains against them, are not modelled yet.
"""

TAXABLE_CAPITAL_GAINS = CATALOG.declare("taxable_capital_gains", Decimal)
"""Taxable capital gains, T1 line 12700: the capital gain times the inclusion rate (Schedule 3
lines 23 to 26)."""

TOTAL_INCOME = CATALOG.declare("total_income", Decimal)
"""Total income, T1 line 15000: the sum of the income lines, here employment income and taxable
capital gains."""

RRSP_DEDUCTION = CATALOG.declare("rrsp_deduction", Decimal)
"""RRSP deduction, T1 line 20800 "RRSP deduction (complete Schedule 7 and attach receipts)": the
amount claimed, a starting amount.

The contribution limit is not modelled, so the claimed amount is an input.
"""

UNION_DUES = CATALOG.declare("union_dues", Decimal)
"""Union dues, T1 line 21200 "Annual union, professional, or like dues (receipts and box 44 of all
T4 slips)": the amount claimed, a starting amount."""

DEDUCTIONS_FROM_TOTAL_INCOME = CATALOG.declare("deductions_from_total_income", Decimal)
"""Total deductions, T1 line 23300 "Add lines 35 to 52": the sum of the deductions from total
income, here the RRSP deduction and union dues."""

NET_INCOME = CATALOG.declare("net_income", Decimal)
"""Net income, T1 line 23600 "Line 54 minus line 55 (if negative, enter "0") Net income": total
income less total deductions, not below zero.

Line 54 (23400) is "Line 34 minus line 53 (if negative, show in brackets) Net income before
adjustments"; line 55 (23500, social benefits repayment) is not modelled.
"""

DEDUCTIONS_FROM_NET_INCOME = CATALOG.declare("deductions_from_net_income", Decimal)
"""Deductions from net income, T1 line 25700 "Add lines 58 to 67": the sum of the deductions
from net income, lines 58 to 67 (lines 24400 to 25600).

None of those deductions is modelled yet, so the sum has no parts.
"""

TAXABLE_INCOME = CATALOG.declare("taxable_income", Decimal)
"""Taxable income, T1 line 69 "Line 57 minus line 68 (if negative, enter "0") Taxable income"
(line 26000, as Step 5 refers to it): net income less the deductions from net income, not below
zero; the base the federal and Ontario brackets apply to.

Line 57 is "Enter the amount from line 56 of the previous page" (net income); line 68 (25700) is
"Add lines 58 to 67".
"""

FEDERAL_BASIC_TAX = CATALOG.declare("federal_basic_tax", Decimal)
"""Federal tax on taxable income from the bracket schedule, before non-refundable credits.

Its T1 line reference is still to be confirmed: design.md §2 marks federal line semantics
UNVERIFIED.
"""

BASIC_PERSONAL_AMOUNT = CATALOG.declare("basic_personal_amount", Decimal)
"""Basic personal amount, T1 line 30000 "If the amount on line 23600 is $177,882 or less, enter
$16,129. Otherwise, use the Federal Worksheet to calculate the amount to enter. (maximum
$16,129)": the amount claimed, the first part of the total of the credit amounts.

The reduction for net income above $177,882 is not modelled, so the claimed amount is the full
amount.
"""

NON_REFUNDABLE_CREDIT_AMOUNTS = CATALOG.declare("non_refundable_credit_amounts", Decimal)
"""Total of the non-refundable credit amounts, T1 line 33500 "Line 106 plus line 112": the sum
of the credit amounts the rate is applied to once, here the basic personal amount alone."""

FEDERAL_TAX_AFTER_CREDITS = CATALOG.declare("federal_tax_after_credits", Decimal)
"""Federal basic tax less federal non-refundable tax credits, not below zero.

Its T1 line reference is still to be confirmed: design.md §2 marks federal line semantics
UNVERIFIED.
"""
