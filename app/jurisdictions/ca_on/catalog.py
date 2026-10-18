"""The Ontario artifact catalog: Ontario's own kinds, named from Form ON428 (§2, §7).

Only the kinds in use are declared, each non-negative, as no ON428 line here can be negative:
amounts are Decimal, the counts of dependent children and dependants int. Federal kinds come
from `app.jurisdictions.ca.catalog`. Identifiers are stable:
`tests/jurisdictions/ca_on/test_catalog.py` snapshots them.
"""

from __future__ import annotations

from decimal import Decimal

from app.domain.artifact import ArtifactCatalog
from app.domain.registry import Namespace
from app.jurisdictions.ca_on import NAMESPACE

CATALOG = ArtifactCatalog(Namespace(NAMESPACE))

ONTARIO_BASIC_TAX = CATALOG.declare("ontario_basic_tax", Decimal, non_negative=True)
"""Ontario tax on taxable income, 2025 ON428 line 8 (Part A), before non-refundable credits."""

BASIC_PERSONAL_AMOUNT = CATALOG.declare("basic_personal_amount", Decimal, non_negative=True)
"""Basic personal amount, ON428 line 9 (line 58040) "Basic personal amount Claim $12,747": the
amount claimed, the first part of the total of the Ontario credit amounts."""

ELIGIBLE_DEPENDANT_BASE = CATALOG.declare("eligible_dependant_base", Decimal, non_negative=True)
"""Base amount for an eligible dependant, ON428 line 14 "Base amount 11,905.00": the amount
claimed, before the dependant's net income comes off it."""

ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_MAXIMUM = CATALOG.declare(
    "eligible_dependant_amount_before_maximum", Decimal, non_negative=True
)
"""Amount for an eligible dependant before its maximum, ON428 line 16 "Line 14 minus line 15 (if
negative, enter "0")": the base amount less line 15 "Your eligible dependant's net income from
line 23600 of their return", the federal Schedule 5 line 4 figure, not below zero."""

ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT = CATALOG.declare(
    "eligible_dependant_amount_before_count", Decimal, non_negative=True
)
"""Amount for an eligible dependant before it is claimed, ON428 line 16's "(maximum $10,823)": the
amount before its maximum, at most it."""

ELIGIBLE_DEPENDANT_AMOUNT = CATALOG.declare("eligible_dependant_amount", Decimal, non_negative=True)
"""Amount for an eligible dependant, ON428 line 16 (line 58160): the capped amount for each
eligible dependant claimed for, the T1 line 30400 count, a part of the total of the Ontario credit
amounts."""

NON_REFUNDABLE_CREDIT_AMOUNTS = CATALOG.declare(
    "non_refundable_credit_amounts", Decimal, non_negative=True
)
"""Total of the Ontario non-refundable credit amounts, ON428 line 44 (line 58800) "Line 35 plus
line 43": the sum of the credit amounts the rate is applied to once, here, in line order, the
basic personal amount (line 58040), the amount for an eligible dependant (line 58160), the base
CPP contributions (line 58240) and the EI premiums (line 58300)."""

NON_REFUNDABLE_TAX_CREDITS = CATALOG.declare(
    "non_refundable_tax_credits", Decimal, non_negative=True
)
"""Ontario non-refundable tax credits, ON428 line 50 (line 61500) "Line 46 plus line 49 Enter this
amount on line 52. Ontario non-refundable tax credits": the total of the Ontario credit amounts
times the credit rate, here line 46 (line 58840) alone."""

ONTARIO_TAX_AFTER_CREDITS = CATALOG.declare("ontario_tax_after_credits", Decimal, non_negative=True)
"""Ontario tax after non-refundable tax credits, not below zero: 2025 ON428 line 53."""

ONTARIO_SURTAX = CATALOG.declare("ontario_surtax", Decimal, non_negative=True)
"""Ontario surtax, 2025 ON428 line 68 "Line 66 plus line 67": the 20% tier over $5,710 (line 66)
plus the 36% tier over $7,307 (line 67), each on line 65, the surtax base.

Line 65 is "Line 63 minus line 64 (if negative, enter "0")", with line 64 the Ontario tax on split
income. Neither that tax (line 54) nor the minimum tax carryover (line 60) is modelled, so lines
55, 61, 62 and 63 carry line 53 unchanged and line 65 is the Ontario tax after credits itself.
"""

ONTARIO_TAX_WITH_SURTAX = CATALOG.declare("ontario_tax_with_surtax", Decimal, non_negative=True)
"""Ontario tax with surtax, 2025 ON428 line 69 "Line 62 plus line 68": the Ontario tax after
credits (line 62, which carries line 53 while neither the tax on split income nor the minimum tax
carryover is modelled) plus the Ontario surtax."""

TAX_REDUCTION_BASIC = CATALOG.declare("tax_reduction_basic", Decimal, non_negative=True)
"""Basic reduction, ON428 line 74 "Basic reduction 294.00": the amount claimed, the first part of
the Ontario tax reduction amounts."""

DEPENDENT_CHILDREN = CATALOG.declare("dependent_children", int, non_negative=True)
"""Number of dependent children, ON428 line 75 (line 60969) "Number of dependent children
multiplied by $544", the children "born in 2007 or later": a starting count."""

TAX_REDUCTION_FOR_CHILDREN = CATALOG.declare(
    "tax_reduction_for_children", Decimal, non_negative=True
)
"""Reduction for dependent children, ON428 line 75 (line 60969) "Number of dependent children
multiplied by $544"."""

DEPENDANTS = CATALOG.declare("dependants", int, non_negative=True)
"""Number of dependants, ON428 line 76 (line 60970) "Number of dependants multiplied by $544", the
dependants "with a mental or physical impairment": a starting count."""

TAX_REDUCTION_FOR_DEPENDANTS = CATALOG.declare(
    "tax_reduction_for_dependants", Decimal, non_negative=True
)
"""Reduction for dependants, ON428 line 76 (line 60970) "Number of dependants multiplied by
$544"."""

TAX_REDUCTION_AMOUNTS = CATALOG.declare("tax_reduction_amounts", Decimal, non_negative=True)
"""Ontario tax reduction amounts, ON428 line 77 "Add lines 74 to 76.": the basic reduction plus
the reductions for dependent children and for dependants."""

ONTARIO_TAX_REDUCTION = CATALOG.declare("ontario_tax_reduction", Decimal, non_negative=True)
"""Ontario tax reduction, ON428 line 80 "Line 78 minus line 79 (if negative, enter "0") Ontario
tax reduction": line 78 "Amount from line 77 above multiplied by 2", less line 79 "Amount from
line 73 above".

Line 73 is "Line 71 plus line 72" and line 71 "Line 69 minus line 70 (if negative, enter "0")".
Neither the dividend tax credit (line 70) nor the minimum tax (line 72) is modelled, so line 73 is
the Ontario tax with surtax itself. The conditions under which the form enters "0" on line 80, and
the rule that only the spouse or common-law partner with the higher net income claims lines 75
and 76, are not modelled.
"""

ONTARIO_TAX_AFTER_REDUCTION = CATALOG.declare(
    "ontario_tax_after_reduction", Decimal, non_negative=True
)
"""Ontario tax after the Ontario tax reduction, ON428 line 81 "Line 73 minus line 80 (if negative,
enter "0")": the Ontario tax with surtax (line 73) less the Ontario tax reduction."""

LIFT_CREDIT_BEFORE_MAXIMUM = CATALOG.declare(
    "lift_credit_before_maximum", Decimal, non_negative=True
)
"""LIFT credit before its maximum, Schedule ON428-A line 5 "Line 3 multiplied by the percentage
from line 4 (maximum $875)" before the maximum: line 4 "Applicable rate 5.05%" on line 3 "Line 1
plus line 2", which is employment income (line 1 "Amount from line 10100 of your return") while
line 2 "Amount from line 10400 of your return" is not triggered."""

LIFT_MAXIMUM_CREDIT = CATALOG.declare("lift_maximum_credit", Decimal, non_negative=True)
"""LIFT credit at most its maximum, Schedule ON428-A line 5's "(maximum $875)" and Part A line 14
"Amount from line 5 above (maximum $875)"."""

LIFT_REDUCTION = CATALOG.declare("lift_reduction", Decimal, non_negative=True)
"""LIFT credit reduction, Schedule ON428-A Part A line 19 "Line 17 multiplied by the percentage
from line 18": line 18 "Applicable rate 5%" on line 17 "Line 15 minus line 16 (if negative, enter
"0")", line 16 "Individual income threshold 32,500.00".

Line 15 is "Amount from line 13 above", the adjusted net income, which is net income (line 6,
from line 23600 of the return) while lines 7, 8, 10 and 11 are not triggered. Each taxpayer is
taken to be single at the end of the year, so Part A applies and Part B (a spouse) is not
modelled; the schedule states no eligibility rules of its own ("To find out if you are eligible
for the low-income individuals and families tax (LIFT) credit, go to canada.ca/on-tax-info.").
"""

LIFT_CREDIT = CATALOG.declare("lift_credit", Decimal, non_negative=True)
"""LIFT credit, Schedule ON428-A line 20 "Line 14 minus line 19 (if negative, enter "0") Enter
this amount on line 62140 of your Form ON428.", ON428 line 85 (62140) "Low-income individuals and
families tax (LIFT) credit (complete Schedule ON428-A)"."""

ONTARIO_TAX_AFTER_LIFT_CREDIT = CATALOG.declare(
    "ontario_tax_after_lift_credit", Decimal, non_negative=True
)
"""Ontario tax after the LIFT credit, ON428 line 86 "Line 84 minus line 85 (if negative, enter
"0")": the Ontario tax after the reduction less the LIFT credit, as line 84 "Amount from line 83
of the previous page" carries line 83 "Line 81 minus line 82 (if negative, enter "0")", which is
line 81 while the provincial foreign tax credit (line 82) is not triggered."""

ONTARIO_HEALTH_PREMIUM = CATALOG.declare("ontario_health_premium", Decimal, non_negative=True)
"""Ontario health premium, ON428 line 89 "Ontario health premium (complete the chart below)": the
chart on taxable income (its line 1 "Enter your taxable income from line 26000 of your return"),
each sloped row the previous plateau plus a rate on the income over the row's threshold, at most
the next plateau."""

ONTARIO_TAX = CATALOG.declare("ontario_tax", Decimal, non_negative=True)
"""Ontario tax, ON428 line 90 "Line 88 plus line 89 Enter this amount on line 42800 of your
return. Ontario tax": the Ontario tax after the LIFT credit plus the Ontario health premium.

Line 88 "Line 86 minus line 87 (if negative, enter "0")" carries line 86, as the community food
program donation tax credit for farmers (line 87) is not triggered by the returns computed so far.
"""
