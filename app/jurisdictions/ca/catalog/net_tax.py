"""The federal catalog: federal tax payable.

Special taxes, net federal tax, total payable and income tax deducted.
"""

from __future__ import annotations

from decimal import Decimal

from app.jurisdictions.ca.catalog.base import CATALOG

SPECIAL_TAXES = CATALOG.declare("special_taxes", Decimal, non_negative=True)
"""Special taxes, T1 line 141 (line 41800) "Special taxes": the additional tax on RESP accumulated
income payments (`resp_aips_additional_tax`, Form T1172) and the tax for not purchasing replacement
shares in a Quebec labour-sponsored fund (`rl_10_labour_sponsored_fund_amount`). Not wired: the tax
on excess employees profit sharing plan amounts (Form RC359)."""

SPLIT_INCOME_LINE_10 = CATALOG.declare("split_income_line_10", Decimal, non_negative=True)
"""Tax on split income with the advanced Canada workers benefit, Form T1206 Part 2 line 10 "Line 8
plus line 9", line 9 being "Amount from line 41500 of your return": the federal tax on split income
plus the advanced Canada workers benefit."""

SPLIT_INCOME_LINE_13 = CATALOG.declare("split_income_line_13", Decimal, non_negative=True)
"""Disability amounts on split income, Form T1206 Part 2 line 13 "Line 11 plus line 12", line 11
being "Amount from line 31600 of your return" and line 12 "Amount from line 31800 of your return":
the disability amount for self plus the disability amount transferred from a dependant, under
"Federal disability tax credit"."""

SPLIT_INCOME_LINE_14 = CATALOG.declare("split_income_line_14", Decimal, non_negative=True)
"""Disability tax credit on split income, Form T1206 Part 2 line 14, line 13 "× 14.5%": the
disability amounts at the credit rate."""

SPLIT_INCOME_LINE_15 = CATALOG.declare("split_income_line_15", Decimal)
"""Tax on split income less the disability credit, Form T1206 Part 2 line 15 "Line 10 minus line
14": line 10 less the disability credit.

The form prints no "(if negative, enter "0")", so the kind is signed.
"""

SPLIT_INCOME_LINE_18 = CATALOG.declare("split_income_line_18", Decimal, non_negative=True)
"""Eligible dividends on split income, Form T1206 Part 2 line 18 "Line 16 minus line 17 (if
negative, enter "0")": line 16 (the dividends of line 1 of Part 1) less line 17 (the dividends other
than eligible of line 2), not below zero, under "Federal dividend tax credit on split income"."""

SPLIT_INCOME_LINE_19 = CATALOG.declare("split_income_line_19", Decimal, non_negative=True)
"""Dividend tax credit on split income, other than eligible, Form T1206 Part 2 line 19, line 17 "×
9.0301%": line 17 at the dividend tax credit rate for dividends other than eligible."""

SPLIT_INCOME_LINE_20 = CATALOG.declare("split_income_line_20", Decimal, non_negative=True)
"""Dividend tax credit on split income, eligible, Form T1206 Part 2 line 20, line 18 "× 15.0198%":
line 18 at the dividend tax credit rate for eligible dividends."""

SPLIT_INCOME_LINE_21 = CATALOG.declare("split_income_line_21", Decimal, non_negative=True)
"""Dividend tax credit on split income, Form T1206 Part 2 line 21 "Line 19 plus line 20": the
federal dividend tax credit on split income."""

SPLIT_INCOME_LINE_22 = CATALOG.declare("split_income_line_22", Decimal)
"""Tax on split income after the credits, Form T1206 Part 2 line 22 "Line 15 minus line 21": line 15
less the dividend tax credit.

The form prints no "(if negative, enter "0")", so the kind is signed.
"""

SPLIT_INCOME_LINE_24 = CATALOG.declare("split_income_line_24", Decimal, non_negative=True)
"""Tax on split income after the credits, not below zero, Form T1206 Part 2 line 24 "Line 22 minus
line 23 (if negative, enter "0")": line 22 not below zero, line 23 (the federal foreign tax credit
on split income) not being wired."""

SPLIT_INCOME_LINE_29 = CATALOG.declare("split_income_line_29", Decimal, non_negative=True)
"""Federal tax less credits with the advanced Canada workers benefit, Form T1206 Part 2 line 29
"Line 27 plus line 28": the federal tax less credits (lines 25 to 27, the T1 line 139) plus the
advanced Canada workers benefit of line 28."""

SPLIT_INCOME_LINE_30 = CATALOG.declare("split_income_line_30", Decimal, non_negative=True)
"""Federal tax on split income floor, Form T1206 Part 2 line 30 "Enter whichever is more: the amount
from line 24 or line 29.": the greater of line 24 and line 29, the floor under the federal tax on
split income."""

NET_FEDERAL_TAX = CATALOG.declare("net_federal_tax", Decimal, non_negative=True)
"""Net federal tax, T1 line 142 (line 42000) "Add lines 139 to 141. Net federal tax": by Form T1206
Part 2 "Add the amount from line 30 to the amount from line 41800 of your return, and enter the
result on line 42000 of your return.", line 30 (`split_income_line_30`, the more of line 24 and line
29, line 29 being line 139, `federal_tax_less_credits`, plus line 140, the advanced Canada workers
benefit) plus the special taxes (`special_taxes`, line 141), in line order. With no split income,
line 24 is 0 and the sum is lines 139 to 141.

Line 126 (42900) is "Line 121 minus line 125 (if negative, enter "0") Basic federal tax", line 121
(40400) "Line 119 plus line 120" and line 125 "Add lines 122 to 124.", line 122 being "Amount from
line 35000" and line 123 the federal dividend tax credit: the federal tax after credits. Line 131
(`itc_recapture`) is added to it (line 132) and line 134 (40600) "Line 132 minus line 133 (if
negative, enter "0") Federal tax" carries line 132, as line 133 is not wired. Not modelled: line 124
(minimum tax carryover), line 127 (foreign surtax, not
triggered on a return whose income is all allocated to Ontario), line 129 (foreign tax credit),
line 133 (logging tax credit) and line 136 (investment tax credit).
"""

CPP_PAYABLE_ON_SELF_EMPLOYMENT = CATALOG.declare(
    "cpp_payable_on_self_employment", Decimal, non_negative=True
)
"""CPP contributions payable on self-employment income and other earnings, T1 line 144 and line
42100 "CPP contributions payable on self-employment income and other earnings (complete Schedule 8
or Form RC381, whichever applies)": Schedule 8 Part 4 line 14, entered once for each Part 4
completed (1 or 0). Part 5 and Form RC381 are not wired."""

EI_PAYABLE_ON_SELF_EMPLOYMENT = CATALOG.declare(
    "ei_payable_on_self_employment", Decimal, non_negative=True
)
"""EI premiums payable on self-employment and other eligible earnings, T1 line 145 and line 42120
"Employment insurance premiums payable on self-employment and other eligible earnings (complete
Schedule 13)": Schedule 13 line 9, entered once for each agreement with the Commission (1 or 0)."""

TOTAL_PAYABLE = CATALOG.declare("total_payable", Decimal, non_negative=True)
"""Total payable, T1 line 148 (line 43500) "Add lines 143 to 147. Total payable": the net federal
tax, the CPP contributions and EI premiums payable on self-employment income and the provincial
tax, in line order.

Line 143 is "Amount from line 42000"; line 144 (42100) and line 145 (42120) are the Schedule 8
Part 4 and Schedule 13 amounts; line 147 (42800) "Provincial or territorial tax (complete and
attach your provincial or territorial Form 428, even if the result is "0")". Not computed: line 146
(42200), the social benefits repayment.
"""

INCOME_TAX_DEDUCTED = CATALOG.declare("income_tax_deducted", Decimal, non_negative=True)
"""Income tax deducted, T1 line 150 (line 43700) "Total income tax deducted (amounts from all
Canadian slips)": a starting amount."""
