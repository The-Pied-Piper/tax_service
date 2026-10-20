"""The federal catalog: personal amounts.

The basic personal, age, spouse, eligible dependant, caregiver, medical and disability amounts, the
principal residence gain lines, the fields of the capital cost allowance table and the infirm
children amount.
"""

from __future__ import annotations

from decimal import Decimal

from app.domain.record_list import RecordListKind
from app.jurisdictions.ca.catalog.base import CATALOG

FEDERAL_BASIC_TAX = CATALOG.declare("federal_basic_tax", Decimal, non_negative=True)
"""Federal tax on taxable income from the bracket schedule, before non-refundable credits.

Its T1 line reference is still to be confirmed: design.md §2 marks federal line semantics
UNVERIFIED.
"""

BASIC_PERSONAL_AMOUNT = CATALOG.declare("basic_personal_amount", Decimal, non_negative=True)
"""Basic personal amount, T1 line 30000 "If the amount on line 23600 is $177,882 or less, enter
$16,129. If the amount on line 23600 is $253,414 or more, enter $14,538. Otherwise, use the
Federal Worksheet to calculate the amount to enter. (maximum $16,129)": the first part of the
total of the credit amounts.

It is computed from net income (line 23600) by the Federal Worksheet (form 5000-D1), line 30000:
line 11 "Line 1 plus line 10 Enter this amount on line 30000 of your return. (maximum $16,129)",
the base amount of line 1 plus the supplement amount of line 2 less its reduction for net income
over the income threshold of line 4 (line 10 "Line 2 minus line 9 (if negative, enter "0")").
"""

BORN_IN_1960_OR_EARLIER = CATALOG.declare("born_in_1960_or_earlier", int, non_negative=True)
"""Born in 1960 or earlier, T1 line 78 (line 30100) "Age amount (if you were born in 1960 or
earlier) (use Federal Worksheet) (maximum $9,028)": a starting count, 0 or 1, from the date of birth
the return asks for.

The age amount is claimed only if the filer was born in 1960 or earlier; a count is only declared
non-negative, so that condition is the return's to keep. It multiplies the age amount, as the form
takes it.
"""

AGE_MAXIMUM = CATALOG.declare("age_maximum", Decimal, non_negative=True)
"""Maximum age amount, Federal Worksheet (form 5000-D1), "Line 30100 - Age amount", line 1 "Maximum
amount 9,028.00": the dataset as an artifact."""

AGE_INCOME_THRESHOLD = CATALOG.declare("age_income_threshold", Decimal, non_negative=True)
"""Income threshold of the age amount, Federal Worksheet (form 5000-D1), "Line 30100 - Age amount",
line 3 "Income threshold 45,522.00": the dataset as an artifact."""

AGE_INCOME_OVER_THRESHOLD = CATALOG.declare("age_income_over_threshold", Decimal, non_negative=True)
"""Net income over the income threshold, Federal Worksheet (form 5000-D1), "Line 30100 - Age
amount", line 4 "Line 2 minus line 3 (if negative, enter "0")": line 2 "Amount from line 23600 of
your return" less the income threshold of line 3, not below zero."""

AGE_REDUCTION = CATALOG.declare("age_reduction", Decimal, non_negative=True)
"""Reduction of the age amount, Federal Worksheet (form 5000-D1), "Line 30100 - Age amount", line 6
"Line 4 multiplied by the percentage from line 5": line 4 at the applicable rate of line 5 "15%"."""

AGE_AMOUNT_BEFORE_COUNT = CATALOG.declare("age_amount_before_count", Decimal, non_negative=True)
"""Age amount before it is claimed, Federal Worksheet (form 5000-D1), "Line 30100 - Age amount",
line 7 "Line 1 minus line 6 (if negative, enter "0") Enter this amount on line 30100 of your
return.": the maximum amount less the reduction, not below zero."""

AGE_AMOUNT = CATALOG.declare("age_amount", Decimal, non_negative=True)
"""Age amount, T1 line 78 (line 30100) "Age amount (if you were born in 1960 or earlier) (use
Federal Worksheet) (maximum $9,028)": the worksheet's line 7 once if the filer was born in 1960 or
earlier, else 0; a part of the total of the credit amounts."""

SPOUSE_NET_INCOME = CATALOG.declare("spouse_net_income", Decimal, non_negative=True)
"""Spouse's net income, Schedule 5 line 4 "Your spouse's or common-law partner's net income from
line 23600 of their return (Note 1)": a starting amount, also line 2 "Net income for this person
from line 23600 of their return" of the Canada caregiver calculation for line 30425, and ON428
line 12 "Your spouse's or common-law partner's net income from line 23600 of their return".
"""

SPOUSES_CLAIMED = CATALOG.declare("spouses_claimed", int, non_negative=True)
"""Number of spouse or common-law partner amounts claimed, T1 line 79 (line 30300) "Spouse or
common-law partner amount (complete Schedule 5)": a starting count, 0 or 1.

Schedule 5 states "Claim this amount if, at any time in the year, you supported your spouse or
common-law partner" and "Only one spouse or common-law partner can claim the amount on line 30300
for each other for the same year"; a count is only declared non-negative, so that rule is the
return's to keep. The claim is the filer's statement; without it a return with no spouse would claim
the whole basic personal amount.
"""

SPOUSE_CAREGIVER_ELIGIBLE = CATALOG.declare("spouse_caregiver_eligible", int, non_negative=True)
"""Eligible for the Canada caregiver amount for the spouse, Schedule 5 line 2 and line 51090 "If you
are eligible for the Canada caregiver amount for your spouse or common-law partner, enter $2,687
(see line 30425 on page 4)": a starting count, 0 or 1.

Eligibility is the filer's statement, as the schedule takes it, and is not computed here. It adds
the $2,687 at line 2 of line 30300 and triggers line 30425, which the schedule asks for only if
"you entered $2,687 on line 51090 or line 51100".
"""

SPOUSE_INFIRMITY_SUPPLEMENT = CATALOG.declare(
    "spouse_infirmity_supplement", Decimal, non_negative=True
)
"""Supplement for a spouse with an infirmity, Schedule 5, "Line 30300 - Spouse or common-law partner
amount", line 2 and line 51090 "If you are eligible for the Canada caregiver amount for your spouse
or common-law partner, enter $2,687": the dataset once if eligible, else 0."""

SPOUSE_AMOUNT_BASIS = CATALOG.declare("spouse_amount_basis", Decimal, non_negative=True)
"""Basis of the spouse or common-law partner amount, Schedule 5, "Line 30300 - Spouse or common-law
partner amount", line 3 "Line 1 plus line 2": line 1 "Basic personal amount from line 30000 of your
return" plus the supplement of line 2."""

SPOUSE_AMOUNT_BEFORE_COUNT = CATALOG.declare(
    "spouse_amount_before_count", Decimal, non_negative=True
)
"""Spouse or common-law partner amount before it is claimed, Schedule 5, "Line 30300 - Spouse or
common-law partner amount", line 5 "Line 3 minus line 4 (if negative, enter "0") Enter this amount
on line 30300 of your return.": line 3 less line 4, the spouse's net income, not below zero."""

SPOUSE_AMOUNT = CATALOG.declare("spouse_amount", Decimal, non_negative=True)
"""Spouse or common-law partner amount, T1 line 79 (line 30300) "Spouse or common-law partner amount
(complete Schedule 5)": Schedule 5 line 5 once if the filer claims it, else 0; a part of the total
of the credit amounts."""

ELIGIBLE_DEPENDANTS = CATALOG.declare("eligible_dependants", int, non_negative=True)
"""Number of eligible dependants claimed for, T1 line 80 (line 30400) "Amount for an eligible
dependant (complete Schedule 5)": a starting count, 0 or 1.

Schedule 5 states "Each household is allowed only one claim for this amount"; a count is only
declared non-negative, so that rule is the return's to keep, as are the conditions: "You did not
have a spouse or common-law partner or, if you did, you were not living with them, supporting them,
or being supported by them"; "You supported the dependant in 2025"; "You lived with the dependant
(in most cases in Canada) in a home ... you maintained"; the dependant is "your child, grandchild,
brother or sister under 18 years of age" (or "your parent or grandparent", or "your child,
grandchild, brother or sister 18 years of age or older with a mental or physical infirmity"); and
"You had to pay child support in 2025 for the eligible dependant" bars the claim, with exceptions.
Eligibility is not computed here.
"""

DEPENDANT_NET_INCOME = CATALOG.declare("dependant_net_income", Decimal, non_negative=True)
"""Dependant's net income, Schedule 5 line 4 (line 51106) "Dependant's net income from line 23600
of their return": a starting amount, also ON428 line 15 "Your eligible dependant's net income from
line 23600 of their return"."""

ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT = CATALOG.declare(
    "eligible_dependant_amount_before_count", Decimal, non_negative=True
)
"""Amount for an eligible dependant before it is claimed, Schedule 5 line 5 "Line 3 minus line 4
(if negative, enter "0") Enter this amount on line 30400 of your return.": the basic personal
amount (line 1 "Basic personal amount from line 30000 of your return") less the dependant's net
income (line 4), not below zero.

Line 3 is "Line 1 plus line 2"; line 2 "If you are eligible for the Canada caregiver amount for
your dependant (other than your infirm child under 18 years of age), enter $2,687" is not
triggered, so line 3 is line 1.
"""

ELIGIBLE_DEPENDANT_AMOUNT = CATALOG.declare("eligible_dependant_amount", Decimal, non_negative=True)
"""Amount for an eligible dependant, T1 line 80 (line 30400) "Amount for an eligible dependant
(complete Schedule 5)": Schedule 5 line 5 for each eligible dependant claimed for, a part of the
total of the credit amounts."""

SPOUSE_CAREGIVER_BASE = CATALOG.declare("spouse_caregiver_base", Decimal, non_negative=True)
"""Base amount for the Canada caregiver amount for a spouse, Schedule 5, "Line 30425 - Canada
caregiver amount for spouse or common-law partner, or eligible dependant age 18 or older", line 1
"Base amount 28,798.00": the dataset as an artifact."""

SPOUSE_CAREGIVER_BEFORE_MAXIMUM = CATALOG.declare(
    "spouse_caregiver_before_maximum", Decimal, non_negative=True
)
"""Canada caregiver amount for a spouse before its maximum, Schedule 5 (form 5000-S5), "Line 30425",
line 3 "Line 1 minus line 2 (if negative, enter "0") (maximum $8,601)": line 1 "Base amount
28,798.00" less line 2 "Net income for this person from line 23600 of their return", not below
zero, before the "(maximum $8,601)" is applied."""

SPOUSE_CAREGIVER_LIMIT = CATALOG.declare("spouse_caregiver_limit", Decimal, non_negative=True)
"""Canada caregiver amount for a spouse at most its maximum, Schedule 5 (form 5000-S5), "Line
30425", line 3 "Line 1 minus line 2 (if negative, enter "0") (maximum $8,601)": the amount before
its maximum, at most $8,601.

It is not named `..._before_count`, as the eligible dependant's capped amount is, because that name
is the line 5 result's (`spouse_caregiver_amount_before_count`), which line 4 comes off first.
"""

SPOUSE_CAREGIVER_AMOUNT_BEFORE_COUNT = CATALOG.declare(
    "spouse_caregiver_amount_before_count", Decimal, non_negative=True
)
"""Canada caregiver amount for a spouse before it is claimed, Schedule 5, "Line 30425", line 5 "Line
3 minus line 4 (if negative, enter "0") Enter this amount on line 30425 of your return. Allowable
amount for this person": line 3 less line 4 "Amount claimed on line 30300 or line 30400 of your
return, if applicable", here the spouse amount, not below zero.

The condition "a person whose net income is between $8,624 and $28,798" needs no gate: below $8,624
line 4 is already more than $8,601, so line 5 is 0. The eligible dependant 18 or older (line 30400)
is not wired here.
"""

SPOUSE_CAREGIVER_AMOUNT = CATALOG.declare("spouse_caregiver_amount", Decimal, non_negative=True)
"""Canada caregiver amount for a spouse, T1 line 81 (line 30425) "Canada caregiver amount for spouse
or common-law partner, or eligible dependant age 18 or older (complete Schedule 5)": Schedule 5 line
5 once if the spouse is eligible for it (line 51090), else 0; a part of the total of the credit
amounts."""

INFIRM_DEPENDANTS = RecordListKind.declare(
    CATALOG, "infirm_dependants", fields=(DEPENDANT_NET_INCOME,)
)
"""Infirm dependants, Schedule 5 "Line 30450 - Canada caregiver amount for other infirm dependants
age 18 or older" "Complete the chart below for each dependant who meets the conditions above": a
starting list with one record for each such dependant, holding line 2 "Infirm dependant's net
income from line 23600 of their return". The caller lists only the dependants who meet the
conditions."""

CAREGIVER_AMOUNT = CATALOG.declare("caregiver_amount", Decimal, non_negative=True)
"""Canada caregiver amount for other infirm dependants, T1 line 82 (line 30450) "Canada caregiver
amount for other infirm dependants age 18 or older (complete Schedule 5)": "the total of allowable
amounts claimed for all dependants", each line 3 "Line 1 minus line 2 (if negative, enter "0")
(maximum $8,601)", a part of the total of the credit amounts."""

OTHER_DEPENDANT_MEDICAL_EXPENSES = CATALOG.declare(
    "other_dependant_medical_expenses", Decimal, non_negative=True
)
"""Medical expenses for an other dependant, Federal Worksheet for line 33199, line 1 "Medical
expenses for other dependant": a field of each record of the other dependants, not an artifact of
its own."""

OTHER_DEPENDANTS = RecordListKind.declare(
    CATALOG,
    "other_dependants",
    fields=(OTHER_DEPENDANT_MEDICAL_EXPENSES, DEPENDANT_NET_INCOME),
)
"""Other dependants, Federal Worksheet for line 33199 "Complete one column for each dependant": a
starting list with one record for each dependant whose medical expenses are claimed, holding line 1
"Medical expenses for other dependant" and the dependant's net income from line 23600 of their
return, from which line 2 "amount from line 109 of the dependant's return" is worked out. A list
of its own: the infirm dependants of line 30450 are a different set of people."""

OTHER_DEPENDANTS_MEDICAL = CATALOG.declare("other_dependants_medical", Decimal, non_negative=True)
"""Allowable amount of medical expenses for other dependants, T1 line 111 (line 33199) "Allowable
amount of medical expenses for other dependants (use Federal Worksheet)": line 4 "Add the amounts
from line 3 of columns 1, 2, and 3 (and others, if any)", each line 3 being "Line 1 minus line 2
(if negative, enter "0")"."""

SHORT_TERM_RENTAL_RELATED_EXPENSES = CATALOG.declare(
    "short_term_rental_related_expenses", Decimal, non_negative=True
)
"""Related expenses of a short-term rental, Form T776 Chart A, column 3 "Related portion of the
total from line 9365 of Part 4": a field of each record of the short-term rental units, not an
artifact of its own."""

SHORT_TERM_RENTAL_NON_COMPLIANT_DAYS = CATALOG.declare(
    "short_term_rental_non_compliant_days", int, non_negative=True
)
"""Non-compliant days of a short-term rental, Form T776 Chart A, column 4 "Number of days the
residential property was a non compliant short-term rental": a field of each record of the
short-term rental units, not an artifact of its own."""

SHORT_TERM_RENTAL_DAYS = CATALOG.declare("short_term_rental_days", int, non_negative=True)
"""Days of a short-term rental, Form T776 Chart A, column 5 "Number of days the residential
property was a short-term rental": a field of each record of the short-term rental units, not an
artifact of its own."""

SHORT_TERM_RENTAL_UNITS = RecordListKind.declare(
    CATALOG,
    "short_term_rental_units",
    fields=(
        SHORT_TERM_RENTAL_RELATED_EXPENSES,
        SHORT_TERM_RENTAL_NON_COMPLIANT_DAYS,
        SHORT_TERM_RENTAL_DAYS,
    ),
)
"""Short-term rental units, Form T776 Chart A "Enter each short-term rental or mixed rental
property on a separate row": a starting list with one record for each row, holding column 3
"Related portion of the total from line 9365 of Part 4", column 4 "Number of days the residential
property was a non compliant short-term rental" and column 5 "Number of days the residential
property was a short-term rental" (columns 1 and 2, the address and the unit number, are labels
the engine does not use)."""

MEDICAL_EXPENSES = CATALOG.declare("medical_expenses", Decimal, non_negative=True)
"""Medical expenses, T1 line 107 and line 33099 "Medical expenses for self, spouse or common-law
partner and your dependent children under 18 years of age": a starting amount."""

MEDICAL_NET_INCOME_SHARE = CATALOG.declare("medical_net_income_share", Decimal, non_negative=True)
"""Share of the net income for medical expenses, T1 line 108 "Amount from line 23600" "multiplied by
3%": 3% of the net income."""

MEDICAL_THRESHOLD = CATALOG.declare("medical_threshold", Decimal, non_negative=True)
"""Threshold for medical expenses, T1 line 109 "Enter whichever is less: $2,834 or the amount from
line 108.": the lesser of the ceiling and the share of the net income."""

MEDICAL_EXPENSES_OVER_THRESHOLD = CATALOG.declare(
    "medical_expenses_over_threshold", Decimal, non_negative=True
)
"""Medical expenses over the threshold, T1 line 110 "Line 107 minus line 109 (if negative, enter
"0")": the filer's own group, not below zero."""

MEDICAL_CLAIM = CATALOG.declare("medical_claim", Decimal, non_negative=True)
"""Allowable medical expenses, T1 line 112 and line 33200 "Line 110 plus line 111": the filer's own
group plus the allowable amount for other dependants, a part of the total of the credit amounts
(line 33500)."""

DEPENDANT_UNDER_18 = CATALOG.declare("dependant_under_18", int, non_negative=True)
"""Dependant under 18, Federal Worksheet "Line 31800 - Disability amount transferred from a
dependant" "If the dependant was under 18 years of age on December 31, 2025, complete lines 2 to
13. If the dependant was 18 years of age or older, complete lines 7 to 13.": 1 if the dependant was
under 18 on December 31, 2025, else 0, taken as a count like the forms' other yes or no questions;
a starting count, a field of each record of the dependants with a disability."""

DEPENDANT_CARE_EXPENSES = CATALOG.declare("dependant_care_expenses", Decimal, non_negative=True)
"""Dependant's care expenses, Federal Worksheet for line 31800, line 3 "Total of child care and
attendant care expenses for your dependant that you or another person claimed": a starting amount,
a field of each record of the dependants with a disability. It matters only for a dependant under
18."""

DEPENDANT_CREDIT_AMOUNTS = CATALOG.declare("dependant_credit_amounts", Decimal, non_negative=True)
"""Dependant's credit amounts, Federal Worksheet for line 31800, line 9 "For provinces and
territories other than Quebec: amount from line 98 of your dependant's return", where 5000-R line
98 is "Add lines 85, 96, and 97.": a starting amount from another person's return, a field of each
record of the dependants with a disability."""

DEPENDANT_TAXABLE_INCOME = CATALOG.declare("dependant_taxable_income", Decimal, non_negative=True)
"""Dependant's taxable income, Federal Worksheet for line 31800, line 11 "Dependant's taxable
income from line 26000 of their return": a starting amount from another person's return, a field
of each record of the dependants with a disability."""

DISABILITY_DEPENDANTS = RecordListKind.declare(
    CATALOG,
    "disability_dependants",
    fields=(
        DEPENDANT_UNDER_18,
        DEPENDANT_CARE_EXPENSES,
        DEPENDANT_CREDIT_AMOUNTS,
        DEPENDANT_TAXABLE_INCOME,
    ),
)
"""Dependants with a disability, Federal Worksheet "Line 31800 - Disability amount transferred from
a dependant" "Complete the following calculation fore ach dependant who is eligible for the
disability tax credit in 2025": a starting list with one record for each such dependant, holding
whether they were under 18 on December 31, 2025, line 3 the child care and attendant care
expenses, line 9 line 98 of their return and line 11 their taxable income. The caller lists only
the dependants who meet the conditions."""

DISABILITY_TRANSFERRED_AMOUNT = CATALOG.declare(
    "disability_transferred_amount", Decimal, non_negative=True
)
"""Disability amount transferred from a dependant, T1 line 100 (line 31800) "Disability amount
transferred from a dependant (use Federal Worksheet)": "the total of allowable amounts claimed for
all dependants who qualify for the disability tax credit", each line 13 "Enter whichever is less:
amount from line 8 or line 12. Allowable amount for this dependant", a part of the total of the
credit amounts."""

RESIDENCE_YEARS_DESIGNATED_AFTER_1981 = CATALOG.declare(
    "residence_years_designated_after_1981", int, non_negative=True
)
"""Years designated after 1981, Form T2091(IND) line 1 "Designation" "After 1981": the number of
tax years after 1981 for which the property is designated as the principal residence; a starting
count, a field of each record of the properties sold."""

RESIDENCE_YEARS_DESIGNATED_1972_TO_1981 = CATALOG.declare(
    "residence_years_designated_1972_to_1981", int, non_negative=True
)
"""Years designated from 1972 to 1981, Form T2091(IND) line 2 "Designation" "After 1971 and before
1982": the number of tax years in that period for which the property is designated as the
principal residence; a starting count, a field of each record of the properties sold."""

RESIDENCE_YEARS_OWNED_AFTER_1981 = CATALOG.declare(
    "residence_years_owned_after_1981", int, non_negative=True
)
"""Years owned after 1981, Form T2091(IND) line 5 "Number of tax years ending after the acquisition
date in which you owned the property" "After 1981": a starting count, a field of each record of
the properties sold."""

RESIDENCE_YEARS_OWNED_1972_TO_1981 = CATALOG.declare(
    "residence_years_owned_1972_to_1981", int, non_negative=True
)
"""Years owned from 1972 to 1981, Form T2091(IND) line 6 "Number of tax years ending after the
acquisition date in which you owned the property" "After 1971 and before 1982": a starting count,
a field of each record of the properties sold."""

RESIDENCE_PROCEEDS = CATALOG.declare("residence_proceeds", Decimal, non_negative=True)
"""Proceeds of disposition, Form T2091(IND) line 8 "Proceeds of disposition or deemed disposition"
(carried to line 14): a starting amount, a field of each record of the properties sold."""

RESIDENCE_OUTLAYS = CATALOG.declare("residence_outlays", Decimal, non_negative=True)
"""Outlays and expenses, Form T2091(IND) line 9 "Outlays and expenses made or incurred related to
the disposition" (carried to line 16): a starting amount, a field of each record of the properties
sold."""

RESIDENCE_ADJUSTED_COST_BASE = CATALOG.declare(
    "residence_adjusted_cost_base", Decimal, non_negative=True
)
"""Adjusted cost base, Form T2091(IND) line 10 "Adjusted cost base at the time of disposition"
(carried to line 15): a starting amount, a field of each record of the properties sold."""

RESIDENCE_PLUS_ONE_YEAR = CATALOG.declare("residence_plus_one_year", int, non_negative=True)
"""The "plus one" year, Form T2091(IND) line 20 "Line 4 plus 1 (see note on page 4)" with the note
"One year is granted by law. If you disposed of your principal residence after October 2, 2016,
and were a non-resident throughout the year of acquisition of the property, you are not eligible
to use the "plus one" rule in this calculation.": 1 if the property may use it, else 0, taken as a
count like the forms' other yes or no questions; a starting count, a field of each record of the
properties sold."""

PRINCIPAL_RESIDENCE_PROPERTIES = RecordListKind.declare(
    CATALOG,
    "principal_residence_properties",
    fields=(
        RESIDENCE_YEARS_DESIGNATED_AFTER_1981,
        RESIDENCE_YEARS_DESIGNATED_1972_TO_1981,
        RESIDENCE_YEARS_OWNED_AFTER_1981,
        RESIDENCE_YEARS_OWNED_1972_TO_1981,
        RESIDENCE_PROCEEDS,
        RESIDENCE_OUTLAYS,
        RESIDENCE_ADJUSTED_COST_BASE,
        RESIDENCE_PLUS_ONE_YEAR,
    ),
)
"""Properties sold and designated as a principal residence, Form T2091(IND) "Complete a separate
form for each property you sold.": a starting list with one record for each such property, holding
the form's input lines 1, 2, 5, 6, 8, 9 and 10 and whether the "plus one" applies (lines 3, 4, 7
and 14 onward are worked out). The caller lists only the properties the form sends to Section 2
(Schedule 3 box 2 or 3) that are not flipped properties."""

PRINCIPAL_RESIDENCE_GAIN = CATALOG.declare("principal_residence_gain", Decimal, non_negative=True)
"""Capital gain left after the principal residence exemption, Form T2091(IND) Part 3 line 54 "Total
capital gain": "Otherwise, enter the amount from line 24", each line 24 being "Line 18 minus line
23 (if negative, enter "0")", totalled over the properties sold."""

CCA_CLASS_NUMBER = CATALOG.declare("cca_class_number", Decimal, non_negative=True)
"""Class number, T776 and T2125 Area A "Column 1: Class number": a number such as 8, 10.1 or 43.1,
kept exact, a field of each record of a list of capital cost allowance classes."""

CCA_UCC_AT_START = CATALOG.declare("cca_ucc_at_start", Decimal, non_negative=True)
"""UCC at the start of the year, Area A "Column 2: Undepreciated capital cost (UCC) at the start of
the year": a starting amount, a field of each record of a list of capital cost allowance
classes."""

CCA_ADDITIONS = CATALOG.declare("cca_additions", Decimal, non_negative=True)
"""Cost of additions, Area A "Column 3: Cost of additions in the year (see Areas B and C below)": a
starting amount, a field of each record of a list of capital cost allowance classes."""

CCA_PROCEEDS = CATALOG.declare("cca_proceeds", Decimal, non_negative=True)
"""Proceeds of dispositions, Area A "Column 5: Proceeds of dispositions in the year (see Areas D and
E below)": a starting amount, a field of each record of a list of capital cost allowance
classes."""

CCA_AIIP_ADDITIONS = CATALOG.declare("cca_aiip_additions", Decimal, non_negative=True)
"""AIIP additions, Area A "Column 11: Cost of remaining additions from column 10 that are AIIPs or
ZEVs acquired before 2025": a starting amount, a field of each record of a list of capital cost
allowance classes."""

CCA_RIIP_ADDITIONS = CATALOG.declare("cca_riip_additions", Decimal, non_negative=True)
"""RIIP additions, Area A "Column 12: Cost of remaining additions from column 10 that are RIIPs or
ZEVs acquired after 2024": a starting amount, a field of each record of a list of capital cost
allowance classes."""

CCA_CLAIMED = CATALOG.declare("cca_claimed", Decimal, non_negative=True)
"""CCA claimed, T776 Area A "Column 23: CCA claim for the year" (T2125 column 21): the caller's
election, "any amount you like, from zero to the maximum allowed for the year" (Guide T4036), a
field of each record of a list of capital cost allowance classes."""

CCA_NO_PROPERTY_LEFT = CATALOG.declare("cca_no_property_left", int, non_negative=True)
"""No property left in the class, Area A Note 3 "If no property is left in the class and there is a
positive amount in this column, deduct the amount from your income as a terminal loss": 1 if no
property is left in the class at the end of the year, else 0, taken as a count like the forms'
other yes or no questions; a field of each record of a list of capital cost allowance classes."""

CCA_UCC_AT_END = CATALOG.declare("cca_ucc_at_end", Decimal, non_negative=True)
"""UCC at the end of the year, T776 Area A "Column 24: UCC at the end of the year (column 7 minus
column 23)" (T2125 column 22): a field of each record of the closing list of capital cost
allowance classes, for next year."""

INFIRM_CHILDREN = CATALOG.declare("infirm_children", int, non_negative=True)
"""Number of infirm children, T1 line 83 "Number of children you are claiming this amount for Line
30499": a starting count."""

INFIRM_CHILDREN_AMOUNT = CATALOG.declare("infirm_children_amount", Decimal, non_negative=True)
"""Canada caregiver amount for infirm children, T1 line 83 (line 30500) "Canada caregiver amount
for infirm children under 18 years of age (see Schedule 5) Number of children you are claiming
this amount for Line 30499" "multiplied by $2,687", a part of the total of the credit amounts on
the T1 alone (the ON428 caregiver amount, line 58185, is not triggered)."""
