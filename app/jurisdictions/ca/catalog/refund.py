"""The federal catalog: the refund or balance owing.

Total credits, the balance owing and the refund.
"""

from __future__ import annotations

from decimal import Decimal

from app.jurisdictions.ca.catalog.base import CATALOG

TOTAL_CREDITS = CATALOG.declare("total_credits", Decimal, non_negative=True)
"""Total credits, T1 line 166 (line 48200) "Add lines 150 to 165. Total credits": here line 150
(43700), line 154 (45200), line 155 (45300), line 159 (45600), line 160 (45700), line 161 (46900),
line 162 (47555), line 164 (47600) and line 165 (47900), in line order.

Not triggered by the returns modelled, or left to later work: the other lines from 151 to 163
(lines 44000 to 47556, among them 44800 CPP overpayment and 45000 EI overpayment).
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

REFUND = CATALOG.declare("refund", Decimal, non_negative=True)
"""Refund, T1 line 48400 "Refund": line 167 "If the amount is negative, enter it on line 48400
below", so the total credits less the total payable, not below zero. A refund is never negative,
unlike line 167 (`refund_or_balance_owing`), which stays signed."""
