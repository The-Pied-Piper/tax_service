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

NET_FEDERAL_TAX = CATALOG.declare("net_federal_tax", Decimal, non_negative=True)
"""Net federal tax, T1 line 142 (line 42000) "Add lines 139 to 141. Net federal tax": the federal
tax less the credits against it (`federal_tax_less_credits`, line 139), the advanced Canada workers
benefit (`advanced_canada_workers_benefit`, line 140) and the special taxes (`special_taxes`, line
141), in line order.

Line 126 (42900) is "Line 121 minus line 125 (if negative, enter "0") Basic federal tax", line 121
(40400) "Line 119 plus line 120" and line 125 "Add lines 122 to 124.", line 122 being "Amount from
line 35000" and line 123 the federal dividend tax credit: the federal tax after credits. Line 131
(`itc_recapture`) is added to it (line 132) and line 134 (40600) "Line 132 minus line 133 (if
negative, enter "0") Federal tax" carries line 132, as line 133 is not wired. Not modelled: line 120
(40424, tax on split income), line 124 (minimum tax carryover), line 127 (foreign surtax, not
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
