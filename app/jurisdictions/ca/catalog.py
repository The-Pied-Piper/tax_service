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

TAXABLE_INCOME = CATALOG.declare("taxable_income", Decimal)
"""Taxable income, T1 line 26000: the base the federal and Ontario brackets apply to."""

FEDERAL_BASIC_TAX = CATALOG.declare("federal_basic_tax", Decimal)
"""Federal tax on taxable income from the bracket schedule, before non-refundable credits.

Its T1 line reference is still to be confirmed: design.md §2 marks federal line semantics
UNVERIFIED.
"""

FEDERAL_TAX_AFTER_CREDITS = CATALOG.declare("federal_tax_after_credits", Decimal)
"""Federal basic tax less federal non-refundable tax credits, not below zero.

Its T1 line reference is still to be confirmed: design.md §2 marks federal line semantics
UNVERIFIED.
"""
