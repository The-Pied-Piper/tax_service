"""The federal catalog: the refund or balance owing.

Total credits, the balance owing and the refund.
"""

from __future__ import annotations

from decimal import Decimal

from app.jurisdictions.ca.catalog.base import CATALOG

TOTAL_CREDITS = CATALOG.declare("total_credits", Decimal, non_negative=True)
"""Total credits, T1 line 166 (line 48200) "Add lines 150 to 165. Total credits": here line 150
(43700), line 153 (45000, the EI overpayment), line 154 (45200), line 155 (45300), line 159
(45600), line 160 (45700), line 161 (46900), line 162 (47555), line 164 (47600) and line 165
(47900), in line order.

Not triggered by the returns modelled, or left to later work: the other lines from 151 to 163
(lines 44000 to 47556, among them 44800 CPP overpayment).
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

T2204_INSURABLE_EARNINGS = CATALOG.declare("t2204_insurable_earnings", Decimal, non_negative=True)
"""Total EI insurable earnings, Form T2204 line 1 "Total EI insurable earnings (box 24 or, if
blank, box 14 of your T4 slips) (1)": a starting amount, before note (1) "If you have no
self-employment earnings and your total EI insurable earnings on your T4 slips are less than
$2,000, enter "0"."
"""

T2204_SELF_EMPLOYMENT_EARNINGS = CATALOG.declare(
    "t2204_self_employment_earnings", Decimal, non_negative=True
)
"""Self-employment and other earnings eligible under the EI agreement, Form T2204 line 2 "Total
self-employment and other earnings eligible for the EI program for access to EI special benefits":
a starting amount, nil when there is no agreement with the Canada Employment Insurance
Commission."""

T2204_PREMIUMS_DEDUCTED = CATALOG.declare("t2204_premiums_deducted", Decimal, non_negative=True)
"""Total premiums deducted, Form T2204 line 4 "Total premiums deducted: Residents of other than
Quebec (box 18 and box 55 of your T4 slips)": a starting amount."""

T2204_LINE_1_COUNT = CATALOG.declare("t2204_line_1_count", int, non_negative=True)
"""Count of the note (1) on Form T2204 line 1 "If you have no self-employment earnings and your
total EI insurable earnings on your T4 slips are less than $2,000, enter "0"": 0 when the note
applies and 1 otherwise, the factor of line 1."""

T2204_LINE_1 = CATALOG.declare("t2204_line_1", Decimal, non_negative=True)
"""Total EI insurable earnings, Form T2204 line 1 "Total EI insurable earnings (box 24 or, if
blank, box 14 of your T4 slips) (1)", after note (1): the insurable earnings, or "0" when the note
applies."""

T2204_LINE_1_PLUS_2 = CATALOG.declare("t2204_line_1_plus_2", Decimal, non_negative=True)
"""Line 1 plus line 2 of Form T2204 before the maximum of line 3: the insurable earnings after note
(1) plus the self-employment earnings eligible under the agreement, not yet capped."""

T2204_LINE_3 = CATALOG.declare("t2204_line_3", Decimal, non_negative=True)
"""Line 3 of Form T2204, "Line 1 plus line 2 (maximum $65,700)": the sum of lines 1 and 2, capped at
the maximum insurable earnings of $65,700."""

T2204_EXEMPTION = CATALOG.declare("t2204_exemption", Decimal, non_negative=True)
"""Exemption of Form T2204 line 7 "Amount from line 3 – $2,000 = (if negative, enter "0")": the
$2,000 taken from line 3, claimed whole, a dataset figure."""

T2204_LINE_6 = CATALOG.declare("t2204_line_6", Decimal, non_negative=True)
"""Line 6 of Form T2204, "Line 4 plus line 5": the premiums deducted (line 4) plus the Schedule 13
premiums payable on self-employment and other earnings (line 5), for each agreement."""

T2204_LINE_7 = CATALOG.declare("t2204_line_7", Decimal, non_negative=True)
"""Line 7 of Form T2204, "Amount from line 3 – $2,000 = (if negative, enter "0")": line 3 less the
$2,000 exemption, not below zero."""

T2204_LINE_8 = CATALOG.declare("t2204_line_8", Decimal, non_negative=True)
"""Line 8 of Form T2204, "Line 6 minus line 7 (if negative, enter "0")": line 6 less line 7, not
below zero."""

T2204_LINE_9 = CATALOG.declare("t2204_line_9", Decimal, non_negative=True)
"""Line 9 of Form T2204, "Total premiums deducted from line 4 above": line 4 carried over."""

T2204_LINE_10 = CATALOG.declare("t2204_line_10", Decimal, non_negative=True)
"""Line 10 of Form T2204, "Residents of other than Quebec Amount from line 1 × 1.64% = (maximum
$1,077.48)": line 1 times the EI premium rate, capped at the maximum premium. The Quebec variant
(line 11) is not modelled."""

T2204_LINE_12 = CATALOG.declare("t2204_line_12", Decimal, non_negative=True)
"""Line 12 of Form T2204, "Enter the amount from line 10 or line 11, whichever applies.": line 10,
as the Quebec variant of line 11 is not modelled."""

T2204_LINE_13 = CATALOG.declare("t2204_line_13", Decimal, non_negative=True)
"""Line 13 of Form T2204, "Line 9 minus line 12 (if negative, enter "0")": the premiums deducted
less the premiums payable, not below zero."""

T2204_LINE_14 = CATALOG.declare("t2204_line_14", Decimal, non_negative=True)
"""Line 14 of Form T2204, "Enter whichever is more: amount from line 8 or line 13.": the greater of
line 8 and line 13."""

T2204_LINE_15 = CATALOG.declare("t2204_line_15", Decimal, non_negative=True)
"""Line 15 of Form T2204, "Enter whichever is less: amount from line 9 or line 14.": the lesser of
line 9 and line 14."""

T2204_LINE_15_COUNT = CATALOG.declare("t2204_line_15_count", int, non_negative=True)
"""Count of Form T2204 line 15, "If this amount is more than $1, enter it on line 45000 of your
return.": 1 when line 15 is more than $1 and 0 otherwise, the factor of line 45000."""

T2204_LINE_16 = CATALOG.declare("t2204_line_16", Decimal, non_negative=True)
"""Line 16 of Form T2204, "Enter whichever amount is the least: line 7, line 9 or line 12.": the
least of lines 7, 9 and 12. It is entered on line 31200 of the return (`ca/ei_premiums`)."""

EI_OVERPAYMENT = CATALOG.declare("ei_overpayment", Decimal, non_negative=True)
"""Employment insurance (EI) overpayment, T1 line 45000 "Employment insurance (EI) overpayment":
line 15 of Form T2204 when it is more than $1 ("If this amount is more than $1, enter it on line
45000 of your return"), else 0. Total credits (line 48200) read it at line 153."""
