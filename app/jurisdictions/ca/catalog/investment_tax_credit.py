"""The federal catalog: investment tax credit, Form T2038(IND) Parts A and B.

The caller's lines of Parts A and B (the SR&ED, agricultural, partnership, qualified property,
mineral exploration, critical mineral, apprenticeship T3 box 40 and repayment figures), the credit
each one produces at its rate, the sums that are not outputs, and the two declared outputs, amount
A and amount F. The apprentices and their total are the kinds of `credits_against_federal_tax`.
"""

from __future__ import annotations

from decimal import Decimal

from app.jurisdictions.ca.catalog.base import CATALOG

ITC_SRED_EXPENDITURES = CATALOG.declare("itc_sred_expenditures", Decimal, non_negative=True)
"""SR&ED expenditures, Form T2038(IND) Part A line 67120 "ITC for qualified expenditures for SR&ED
(amount from line 559 of Form T661 plus applicable amount from box 40* of your T3 slip, minus
amounts from lines 67130 and 67135)": the caller's amount, as entered."""

ITC_AGRICULTURAL_SRED_CONTRIBUTIONS = CATALOG.declare(
    "itc_agricultural_sred_contributions", Decimal, non_negative=True
)
"""Agricultural SR&ED contributions, Form T2038(IND) Part A line 67130 "80% of total contributions
made to agricultural organizations for SR&ED": the caller's amount, as entered."""

ITC_SRED_PARTNERSHIP_ALLOCATION = CATALOG.declare(
    "itc_sred_partnership_allocation", Decimal, non_negative=True
)
"""ITC allocated from a partnership for SR&ED, Form T2038(IND) Part A line 67135 "ITC allocated
from a partnership for SR&ED (see boxes 186, 187, and 189 of your T5013 slips)": amount 3, read as
it is, the caller's amount from the T5013 slips."""

ITC_QUALIFIED_PROPERTY = CATALOG.declare("itc_qualified_property", Decimal, non_negative=True)
"""Qualified property, Form T2038(IND) Part A line 67140 "ITC for total investments in qualified
property (include applicable amount from box 40* of your T3 slip)": the caller's amount, as
entered."""

ITC_MINERAL_EXPLORATION_EXPENDITURES = CATALOG.declare(
    "itc_mineral_exploration_expenditures", Decimal, non_negative=True
)
"""Flow-through mining expenditures, Form T2038(IND) Part B line 67170 "Total of your flow-through
mining expenditures related to mineral exploration tax credit": the caller's amount from the
appropriate line in Part IV of Form T1229, as entered."""

ITC_CRITICAL_MINERAL_EXPENDITURES = CATALOG.declare(
    "itc_critical_mineral_expenditures", Decimal, non_negative=True
)
"""Flow-through critical mineral mining expenditures, Form T2038(IND) Part B line 67175 "Total of
your flow-through critical mineral mining expenditures related to critical mineral exploration tax
credit": the caller's amount from the appropriate line in Part IV of Form T1229, as entered."""

ITC_APPRENTICESHIP_T3_BOX_40 = CATALOG.declare(
    "itc_apprenticeship_t3_box_40", Decimal, non_negative=True
)
"""Apprenticeship T3 box 40 amount, Form T2038(IND) Part B line 67180 "Total apprenticeship job
creation tax credit (Total of amounts in column 3 plus applicable amount from box 40* of your T3
slip)": the caller's amount from box 40 of the T3 slip, as entered, added to column 3."""

ITC_SRED_REPAYMENT_2014_AND_PRIOR = CATALOG.declare(
    "itc_sred_repayment_2014_and_prior", Decimal, non_negative=True
)
"""Repayment for SR&ED expenditures of 2014 and prior years, Form T2038(IND) Part B line 67184
"Repayment of assistance that reduced qualified SR&ED expenditures incurred in 2014 and prior
years (amount from line 560 of Form T661)": the caller's amount, as entered."""

ITC_SRED_REPAYMENT_2015_AND_AFTER = CATALOG.declare(
    "itc_sred_repayment_2015_and_after", Decimal, non_negative=True
)
"""Repayment for SR&ED expenditures of 2015 and subsequent years, Form T2038(IND) Part B line 67185
"Repayment of assistance that reduced qualified SR&ED expenditures incurred in 2015 and subsequent
years (amount from line 560 of Form T661)": the caller's amount, as entered."""

ITC_SRED_CREDIT = CATALOG.declare("itc_sred_credit", Decimal, non_negative=True)
"""SR&ED credit, Form T2038(IND) Part A, amount 1: line 67120 "× 0.15 =", the caller's expenditures
times 0.15."""

ITC_AGRICULTURAL_SRED_CREDIT = CATALOG.declare(
    "itc_agricultural_sred_credit", Decimal, non_negative=True
)
"""Agricultural SR&ED credit, Form T2038(IND) Part A, amount 2: line 67130 "× 0.15 =", the caller's
contributions times 0.15."""

ITC_QUALIFIED_PROPERTY_CREDIT = CATALOG.declare(
    "itc_qualified_property_credit", Decimal, non_negative=True
)
"""Qualified property credit, Form T2038(IND) Part A, amount 4: line 67140 "× 0.10 =", the caller's
investments times 0.10."""

ITC_MINERAL_EXPLORATION_CREDIT = CATALOG.declare(
    "itc_mineral_exploration_credit", Decimal, non_negative=True
)
"""Mineral exploration tax credit, Form T2038(IND) Part B, amount B: line 67170 "× 0.15 =", the
caller's flow-through mining expenditures times 0.15."""

ITC_CRITICAL_MINERAL_CREDIT = CATALOG.declare(
    "itc_critical_mineral_credit", Decimal, non_negative=True
)
"""Critical mineral exploration tax credit, Form T2038(IND) Part B, amount C: line 67175 "× 0.30 =",
the caller's flow-through critical mineral expenditures times 0.30."""

ITC_APPRENTICESHIP_WAGES_WITH_T3 = CATALOG.declare(
    "itc_apprenticeship_wages_with_t3", Decimal, non_negative=True
)
"""Apprenticeship total for the credit, Form T2038(IND) Part B line 67180 "Total apprenticeship job
creation tax credit (Total of amounts in column 3 plus applicable amount from box 40* of your T3
slip)": the total of column 3, plus the caller's T3 box 40 amount."""

ITC_APPRENTICESHIP_CREDIT = CATALOG.declare("itc_apprenticeship_credit", Decimal, non_negative=True)
"""Apprenticeship job creation tax credit, Form T2038(IND) Part B, amount D: line 67180 "× 0.10 =",
the total of line 67180 times 0.10."""

ITC_SRED_REPAYMENT_CREDIT_2014_AND_PRIOR = CATALOG.declare(
    "itc_sred_repayment_credit_2014_and_prior", Decimal, non_negative=True
)
"""Repayment credit for 2014 and prior years, Form T2038(IND) Part B, amount 1: line 67184
"× 0.20 =", the caller's repayment times 0.20."""

ITC_SRED_REPAYMENT_CREDIT_2015_AND_AFTER = CATALOG.declare(
    "itc_sred_repayment_credit_2015_and_after", Decimal, non_negative=True
)
"""Repayment credit for 2015 and subsequent years, Form T2038(IND) Part B, amount 2: line 67185
"× 0.15 =", the caller's repayment times 0.15."""

ITC_SRED_REPAYMENT_CREDIT = CATALOG.declare("itc_sred_repayment_credit", Decimal, non_negative=True)
"""Total repayment of assistance for SR&ED, Form T2038(IND) Part B, amount E: "Total repayment of
assistance for SR&ED (add amounts 1 and 2)", the two repayment credits."""

ITC_REFUNDABLE_CREDITS = CATALOG.declare("itc_refundable_credits", Decimal, non_negative=True)
"""Total current-year refundable credits, Form T2038(IND) Part A, amount A: "Total current-year
refundable credits (add amounts 1 to 4)", the four credits of Part A, in line order. Part D reads
it as "Enter amount A at amount 2 in Part D"."""

ITC_NONREFUNDABLE_CREDITS = CATALOG.declare("itc_nonrefundable_credits", Decimal, non_negative=True)
"""Total current-year non-refundable tax credits, Form T2038(IND) Part B, amount F: "Total
current-year non-refundable tax credits (add amounts B, C, D and E)", the credits B, C, D and E.
Part D reads it as "Enter amount F at amount 3 in Part D"."""
