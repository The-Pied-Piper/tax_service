"""The federal catalog: the Canada workers benefit.

The Canada workers benefit lines.
"""

from __future__ import annotations

from decimal import Decimal

from app.jurisdictions.ca.catalog.base import CATALOG

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
