"""The Ontario artifact catalog: Ontario's own kinds, named from Forms ON428 (§2, §7), ON479, T1221.

Only the kinds in use are declared, each non-negative, as no ON428 or ON479 line here can be
negative: amounts are Decimal, the counts of dependent children and dependants int, and the T1221
slips a record list. Federal kinds come from `app.jurisdictions.ca.catalog`. Identifiers are
stable: `tests/jurisdictions/ca_on/test_catalog.py` snapshots them.
"""

from __future__ import annotations

from decimal import Decimal

from app.domain.artifact import ArtifactCatalog
from app.domain.record_list import RecordListKind
from app.domain.registry import Namespace
from app.jurisdictions.ca.catalog import DEPENDANT_NET_INCOME
from app.jurisdictions.ca_on import NAMESPACE

CATALOG = ArtifactCatalog(Namespace(NAMESPACE))

ONTARIO_BASIC_TAX = CATALOG.declare("ontario_basic_tax", Decimal, non_negative=True)
"""Ontario tax on taxable income, 2025 ON428 line 8 (Part A), before non-refundable credits."""

BASIC_PERSONAL_AMOUNT = CATALOG.declare("basic_personal_amount", Decimal, non_negative=True)
"""Basic personal amount, ON428 line 9 (line 58040) "Basic personal amount Claim $12,747": the
amount claimed, the first part of the total of the Ontario credit amounts."""

AGE_MAXIMUM = CATALOG.declare("age_maximum", Decimal, non_negative=True)
"""Maximum Ontario age amount, Worksheet ON428 (form 5006-D), "Line 58080 - Age amount", line 1
"Maximum amount 6,223.00": the dataset as an artifact."""

AGE_INCOME_THRESHOLD = CATALOG.declare("age_income_threshold", Decimal, non_negative=True)
"""Income threshold of the Ontario age amount, Worksheet ON428 (form 5006-D), "Line 58080 - Age
amount", line 3 "Income threshold 46,330.00": the dataset as an artifact."""

AGE_INCOME_OVER_THRESHOLD = CATALOG.declare("age_income_over_threshold", Decimal, non_negative=True)
"""Net income over the income threshold, Worksheet ON428 (form 5006-D), "Line 58080 - Age amount",
line 4 "Line 2 minus line 3 (if negative, enter "0")": line 2 "Amount from line 23600 of your
return" less the income threshold of line 3, not below zero."""

AGE_REDUCTION = CATALOG.declare("age_reduction", Decimal, non_negative=True)
"""Reduction of the Ontario age amount, Worksheet ON428 (form 5006-D), "Line 58080 - Age amount",
line 6 "Line 4 multiplied by the percentage from line 5": line 4 at the applicable rate of line 5
"15%"."""

AGE_AMOUNT_BEFORE_COUNT = CATALOG.declare("age_amount_before_count", Decimal, non_negative=True)
"""Ontario age amount before it is claimed, Worksheet ON428 (form 5006-D), "Line 58080 - Age
amount", line 7 "Line 1 minus line 6 (if negative, enter "0") Enter this amount on line 58080 of
your Form ON428.": the maximum amount less the reduction, not below zero."""

AGE_AMOUNT = CATALOG.declare("age_amount", Decimal, non_negative=True)
"""Age amount, ON428 line 10 (line 58080) "Age amount (if you were born in 1960 or earlier) (use
Worksheet ON428) (maximum $6,223)": the worksheet's line 7 once if the filer was born in 1960 or
earlier, else 0, the T1 line 30100 count; a part of the total of the Ontario credit amounts."""

SPOUSE_BASE = CATALOG.declare("spouse_base", Decimal, non_negative=True)
"""Base amount for a spouse or common-law partner, ON428 line 11 "Base amount 11,905.00": the
amount claimed, before the spouse's net income comes off it."""

SPOUSE_AMOUNT_BEFORE_MAXIMUM = CATALOG.declare(
    "spouse_amount_before_maximum", Decimal, non_negative=True
)
"""Spouse or common-law partner amount before its maximum, ON428 line 13 "Line 11 minus line 12 (if
negative, enter "0")": the base amount less line 12 "Your spouse's or common-law partner's net
income from line 23600 of their return", the federal Schedule 5 line 4 figure, not below zero."""

SPOUSE_AMOUNT_BEFORE_COUNT = CATALOG.declare(
    "spouse_amount_before_count", Decimal, non_negative=True
)
"""Spouse or common-law partner amount before it is claimed, ON428 line 13's "(maximum $10,823)":
the amount before its maximum, at most it."""

SPOUSE_AMOUNT = CATALOG.declare("spouse_amount", Decimal, non_negative=True)
"""Spouse or common-law partner amount, ON428 line 13 (line 58120) "Line 11 minus line 12 (if
negative, enter "0") (maximum $10,823)": the capped amount once if the filer claims it, else 0,
the T1 line 30300 count; a part of the total of the Ontario credit amounts."""

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

CLAIMED_AS_ELIGIBLE_DEPENDANT = CATALOG.declare(
    "claimed_as_eligible_dependant", int, non_negative=True
)
"""Whether a dependant is the one claimed on line 58160, Worksheet ON428 "Line 58185 - Ontario
caregiver amount" line 4 "Amount claimed for this dependant on line 58160 of your Form ON428, if
any": 1 for the dependant claimed there, 0 for any other (any other count is read as claimed), a field of each record of the caregiver
dependants."""

CAREGIVER_DEPENDANTS = RecordListKind.declare(
    CATALOG, "caregiver_dependants", fields=(DEPENDANT_NET_INCOME, CLAIMED_AS_ELIGIBLE_DEPENDANT)
)
"""Dependants for the Ontario caregiver amount, Worksheet ON428 "Line 58185 - Ontario caregiver
amount" "Complete one column for each dependant": a starting list with one record for each
dependant, holding line 2 "Dependant's net income from line 23600 of their return" and whether it
is the dependant claimed on line 58160 (line 4). The caller lists only the dependants who
qualify."""

CAREGIVER_AMOUNT = CATALOG.declare("caregiver_amount", Decimal, non_negative=True)
"""Ontario caregiver amount, ON428 line 17 and line 58185 "Ontario caregiver amount (use Worksheet
ON428)": Worksheet ON428 line 6 "Add the amounts from line 5 of columns 1, 2, and 3 (and others, if
any)", each line 5 "Allowable amount for this dependant: line 3 minus line 4 (if negative, enter
"0")", a part of the total of the Ontario credit amounts."""

NON_REFUNDABLE_CREDIT_AMOUNTS = CATALOG.declare(
    "non_refundable_credit_amounts", Decimal, non_negative=True
)
"""Total of the Ontario non-refundable credit amounts, ON428 line 44 (line 58800) "Line 35 plus
line 43": the sum of the credit amounts the rate is applied to once, here, in line order, the
basic personal amount (line 58040), the age amount (line 58080), the spouse or common-law
partner amount (line 58120), the amount for an eligible dependant (line 58160), the Ontario
caregiver amount (line 58185), the base CPP contributions (line 58240) and the EI premiums
(line 58300)."""

CREDIT_AMOUNTS_AT_CREDIT_RATE = CATALOG.declare(
    "credit_amounts_at_credit_rate", Decimal, non_negative=True
)
"""Ontario credit amounts at the credit rate, ON428 line 46 (line 58840) "Line 44 multiplied by the
percentage from line 45": the total of the credit amounts times the credit rate, the first of the
two lines that line 50 adds."""

DONATIONS_FIRST_TIER_CREDIT = CATALOG.declare(
    "donations_first_tier_credit", Decimal, non_negative=True
)
"""Ontario donations credit at the first tier, ON428 line 47 "Amount from line 13 of your federal
Schedule 9" "multiplied by 5.05%": 5.05% of Schedule 9 line 13."""

DONATIONS_OVER_FIRST_TIER_CREDIT = CATALOG.declare(
    "donations_over_first_tier_credit", Decimal, non_negative=True
)
"""Ontario donations credit over the first tier, ON428 line 48 "Amount from line 14 of your federal
Schedule 9" "multiplied by 11.16%": 11.16% of Schedule 9 line 14."""

DONATIONS_AND_GIFTS_CREDIT = CATALOG.declare(
    "donations_and_gifts_credit", Decimal, non_negative=True
)
"""Ontario donations and gifts credit, ON428 line 49 (line 58969) "Line 47 plus line 48": the sum of
the two tiers."""

NON_REFUNDABLE_TAX_CREDITS = CATALOG.declare(
    "non_refundable_tax_credits", Decimal, non_negative=True
)
"""Ontario non-refundable tax credits, ON428 line 50 (line 61500) "Line 46 plus line 49 Enter this
amount on line 52. Ontario non-refundable tax credits": line 46 (line 58840), the total of the
Ontario credit amounts times the credit rate, plus line 49 (line 58969), the donations and gifts
credit."""

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

DIVIDENDS_AMOUNT_A = CATALOG.declare("dividends_amount_a", Decimal, non_negative=True)
"""Dividends amount A, Worksheet ON428 line 61520 line A "Amount from line 12000 of your
return": the whole line 12000, as the worksheet has no Note 1."""

DIVIDENDS_AMOUNT_B = CATALOG.declare("dividends_amount_b", Decimal, non_negative=True)
"""Dividends amount B, Worksheet ON428 line 61520 line 1 "Amount from line 12010 of your return Line
B": the whole line 12010."""

OTHER_DIVIDENDS_CREDIT = CATALOG.declare("other_dividends_credit", Decimal, non_negative=True)
"""Ontario credit on dividends other than eligible, Worksheet ON428 line 61520 line 1 "multiplied by
2.9863%": amount B times the rate."""

DIVIDENDS_AMOUNT_A_LESS_B = CATALOG.declare("dividends_amount_a_less_b", Decimal, non_negative=True)
"""Dividends amount A less amount B, Worksheet ON428 line 61520 line 2 "Amount A minus amount B Line
C": the eligible dividends."""

ELIGIBLE_DIVIDENDS_CREDIT = CATALOG.declare("eligible_dividends_credit", Decimal, non_negative=True)
"""Ontario credit on eligible dividends, Worksheet ON428 line 61520 line 2 "multiplied by 10%": line
C times the rate."""

DIVIDEND_TAX_CREDIT = CATALOG.declare("dividend_tax_credit", Decimal, non_negative=True)
"""Ontario dividend tax credit, Worksheet ON428 line 61520 line 3 "Line 1 plus line 2 Enter this
amount on line 61520 of your Form ON428.": the credit on dividends other than eligible plus the
credit on eligible dividends, which is ON428 line 57."""

ONTARIO_TAX_BEFORE_DIVIDEND_CREDIT = CATALOG.declare(
    "ontario_tax_before_dividend_credit", Decimal, non_negative=True
)
"""Ontario tax before the dividend tax credit, ON428 line 56 "Enter the amount from line 53 above.":
the Ontario tax after non-refundable tax credits."""

ONTARIO_TAX_LESS_DIVIDEND_CREDIT = CATALOG.declare(
    "ontario_tax_less_dividend_credit", Decimal, non_negative=True
)
"""Ontario tax less the dividend tax credit, ON428 line 58 "Line 56 minus line 57 (if negative,
enter "0")": the Ontario tax after credits less the Ontario dividend tax credit (line 57), not
below zero. Nothing else on the return reads it, as the surtax and line 69 read line 53, so the
manifest returns it."""

DIVIDEND_CREDIT_FROM_LINE_57 = CATALOG.declare(
    "dividend_credit_from_line_57", Decimal, non_negative=True
)
"""Ontario dividend tax credit from line 57, ON428 line 70 "Ontario dividend tax credit from line
57": the credit of line 57 again."""

ONTARIO_TAX_AFTER_DIVIDEND_CREDIT = CATALOG.declare(
    "ontario_tax_after_dividend_credit", Decimal, non_negative=True
)
"""Ontario tax after the dividend tax credit, ON428 line 71 "Line 69 minus line 70 (if negative,
enter "0")": the Ontario tax with surtax less the dividend tax credit, not below zero. It is line
73, as line 72 (the additional tax for minimum tax purposes) is not triggered."""

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
The minimum tax (line 72) is not triggered, so line 73 is line 71, the Ontario tax after the
dividend tax credit. The conditions under which the form enters "0" on line 80, and
the rule that only the spouse or common-law partner with the higher net income claims lines 75
and 76, are not modelled.
"""

ONTARIO_TAX_AFTER_REDUCTION = CATALOG.declare(
    "ontario_tax_after_reduction", Decimal, non_negative=True
)
"""Ontario tax after the Ontario tax reduction, ON428 line 81 "Line 73 minus line 80 (if negative,
enter "0")": the Ontario tax after the dividend tax credit (line 73) less the Ontario tax
reduction."""

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

COMMUNITY_FOOD_PROGRAM_DONATIONS = CATALOG.declare(
    "community_food_program_donations", Decimal, non_negative=True
)
"""Qualifying community food program donations, ON428 line 87 and line 62150 "Enter the amount of
qualifying donations that have also been claimed as a charitable donation.": a starting amount,
taken as entered, as nothing here checks it against Schedule 9."""

COMMUNITY_FOOD_PROGRAM_CREDIT = CATALOG.declare(
    "community_food_program_credit", Decimal, non_negative=True
)
"""Community food program donation tax credit for farmers, ON428 line 87 "multiplied by 25%": the
qualifying donations (line 62150) at the rate."""

ONTARIO_TAX_AFTER_FOOD_CREDIT = CATALOG.declare(
    "ontario_tax_after_food_credit", Decimal, non_negative=True
)
"""Ontario tax after the community food program donation tax credit for farmers, ON428 line 88
"Line 86 minus line 87 (if negative, enter "0")": the Ontario tax after the LIFT credit less the
credit."""

ONTARIO_HEALTH_PREMIUM = CATALOG.declare("ontario_health_premium", Decimal, non_negative=True)
"""Ontario health premium, ON428 line 89 "Ontario health premium (complete the chart below)": the
chart on taxable income (its line 1 "Enter your taxable income from line 26000 of your return"),
each sloped row the previous plateau plus a rate on the income over the row's threshold, at most
the next plateau."""

ONTARIO_TAX = CATALOG.declare("ontario_tax", Decimal, non_negative=True)
"""Ontario tax, ON428 line 90 "Line 88 plus line 89 Enter this amount on line 42800 of your
return. Ontario tax": the Ontario tax after the community food program donation tax credit for
farmers plus the Ontario health premium."""

FERTILITY_EXPENSES = CATALOG.declare("fertility_expenses", Decimal, non_negative=True)
"""Eligible medical expenses for fertility treatment, Form ON479 line 1 and line 61268 "Eligible
medical expenses for fertility treatment": a starting amount, from the receipts the form asks for.

The form prints no eligibility rules for the line; eligibility is to be confirmed."""

FERTILITY_CREDIT_BEFORE_MAXIMUM = CATALOG.declare(
    "fertility_credit_before_maximum", Decimal, non_negative=True
)
"""Fertility treatment credit before its maximum, Form ON479 line 1 "Eligible medical expenses for
fertility treatment multiplied by 25% (maximum $5,000) =" before the maximum: the 25% on the
expenses."""

FERTILITY_CREDIT = CATALOG.declare("fertility_credit", Decimal, non_negative=True)
"""Fertility treatment credit, Form ON479 line 1 and line 61268 "Eligible medical expenses for
fertility treatment multiplied by 25% (maximum $5,000) =": the 25% on the expenses, at most
$5,000, the maximum being printed after the percentage."""

SENIORS_TRANSIT_PAID = CATALOG.declare("seniors_transit_paid", Decimal, non_negative=True)
"""Amount paid for eligible seniors' use of Ontario public transit services, Form ON479 line 14
"Amount paid in the year for eligible seniors' use of Ontario public transit services (maximum
$3,000) Line 63100": a starting amount, from the receipts the form asks for.

The form prints no eligibility rules for the line; eligibility is to be confirmed."""

SENIORS_TRANSIT_AMOUNT_PAID_AT_MOST_MAXIMUM = CATALOG.declare(
    "seniors_transit_amount_paid_at_most_maximum", Decimal, non_negative=True
)
"""Amount paid for seniors' transit at most its maximum, Form ON479 line 14 "Amount paid in the year
for eligible seniors' use of Ontario public transit services (maximum $3,000)": the amount paid, at
most $3,000, the maximum being printed before the percentage."""

SENIORS_TRANSIT_CREDIT = CATALOG.declare("seniors_transit_credit", Decimal, non_negative=True)
"""Seniors' public transit credit, Form ON479 line 14 "Amount paid in the year for eligible
seniors' use of Ontario public transit services (maximum $3,000) Line 63100 multiplied by 15% =":
15% of the amount paid, at most $3,000."""

POLITICAL_CONTRIBUTIONS = CATALOG.declare("political_contributions", Decimal, non_negative=True)
"""Ontario political contributions, Form ON479 line 15 and line 63100 "Ontario political
contributions made in 2025": a starting amount, taken as the form takes it. Worksheet ON479 line 1
of each column "Enter your total political contributions from line 63110 of your Form ON479." reads
it.

The form gives no eligibility conditions beyond "Ontario political contributions"."""

POLITICAL_CREDIT_COLUMN_1_LINE_2 = CATALOG.declare(
    "political_credit_column_1_line_2", Decimal, non_negative=True
)
"""Political contribution credit column 1 line 2, Worksheet ON479 "Column 1: Line 63110 is $500.05
or less", line 2 "0.00": a printed constant."""

POLITICAL_CREDIT_COLUMN_1_LINE_3 = CATALOG.declare(
    "political_credit_column_1_line_3", Decimal, non_negative=True
)
"""Political contribution credit column 1 line 3, Worksheet ON479 "Column 1: Line 63110 is $500.05
or less", line 3 "Line 1 minus line 2 (cannot be negative)": the contributions less line 2, not
below zero."""

POLITICAL_CREDIT_COLUMN_1_LINE_5 = CATALOG.declare(
    "political_credit_column_1_line_5", Decimal, non_negative=True
)
"""Political contribution credit column 1 line 5, Worksheet ON479 "Column 1: Line 63110 is $500.05
or less", line 5 "Line 3 multiplied by the percentage from line 4": line 3 at the line 4 rate of
75%."""

POLITICAL_CREDIT_COLUMN_1_LINE_6 = CATALOG.declare(
    "political_credit_column_1_line_6", Decimal, non_negative=True
)
"""Political contribution credit column 1 line 6, Worksheet ON479 "Column 1: Line 63110 is $500.05
or less", line 6 "0.00": a printed constant."""

POLITICAL_CREDIT_COLUMN_1_LINE_7 = CATALOG.declare(
    "political_credit_column_1_line_7", Decimal, non_negative=True
)
"""Political contribution credit column 1 line 7, Worksheet ON479 "Column 1: Line 63110 is $500.05
or less", line 7 "Line 5 plus line 6 Enter this amount on line 16 of your Form ON479.": line 5
plus line 6."""

POLITICAL_CREDIT_COLUMN_2_LINE_2 = CATALOG.declare(
    "political_credit_column_2_line_2", Decimal, non_negative=True
)
"""Political contribution credit column 2 line 2, Worksheet ON479 "Column 2: Line 63110 is more than
$500.05 but not more than $1,666.82", line 2 "500.05": a printed constant."""

POLITICAL_CREDIT_COLUMN_2_LINE_3 = CATALOG.declare(
    "political_credit_column_2_line_3", Decimal, non_negative=True
)
"""Political contribution credit column 2 line 3, Worksheet ON479 "Column 2: Line 63110 is more than
$500.05 but not more than $1,666.82", line 3 "Line 1 minus line 2 (cannot be negative)": the
contributions less line 2, not below zero."""

POLITICAL_CREDIT_COLUMN_2_LINE_5 = CATALOG.declare(
    "political_credit_column_2_line_5", Decimal, non_negative=True
)
"""Political contribution credit column 2 line 5, Worksheet ON479 "Column 2: Line 63110 is more than
$500.05 but not more than $1,666.82", line 5 "Line 3 multiplied by the percentage from line 4":
line 3 at the line 4 rate of 50%."""

POLITICAL_CREDIT_COLUMN_2_LINE_6 = CATALOG.declare(
    "political_credit_column_2_line_6", Decimal, non_negative=True
)
"""Political contribution credit column 2 line 6, Worksheet ON479 "Column 2: Line 63110 is more than
$500.05 but not more than $1,666.82", line 6 "375.03": a printed constant."""

POLITICAL_CREDIT_COLUMN_2_LINE_7 = CATALOG.declare(
    "political_credit_column_2_line_7", Decimal, non_negative=True
)
"""Political contribution credit column 2 line 7, Worksheet ON479 "Column 2: Line 63110 is more than
$500.05 but not more than $1,666.82", line 7 "Line 5 plus line 6 Enter this amount on line 16 of
your Form ON479.": line 5 plus line 6."""

POLITICAL_CREDIT_COLUMN_3_LINE_2 = CATALOG.declare(
    "political_credit_column_3_line_2", Decimal, non_negative=True
)
"""Political contribution credit column 3 line 2, Worksheet ON479 "Column 3: Line 63110 is more than
$1,666.82", line 2 "1,666.82": a printed constant."""

POLITICAL_CREDIT_COLUMN_3_LINE_3 = CATALOG.declare(
    "political_credit_column_3_line_3", Decimal, non_negative=True
)
"""Political contribution credit column 3 line 3, Worksheet ON479 "Column 3: Line 63110 is more than
$1,666.82", line 3 "Line 1 minus line 2 (cannot be negative)": the contributions less line 2, not
below zero."""

POLITICAL_CREDIT_COLUMN_3_LINE_5 = CATALOG.declare(
    "political_credit_column_3_line_5", Decimal, non_negative=True
)
"""Political contribution credit column 3 line 5, Worksheet ON479 "Column 3: Line 63110 is more than
$1,666.82", line 5 "Line 3 multiplied by the percentage from line 4": line 3 at the line 4 rate
of 33.33%."""

POLITICAL_CREDIT_COLUMN_3_LINE_6 = CATALOG.declare(
    "political_credit_column_3_line_6", Decimal, non_negative=True
)
"""Political contribution credit column 3 line 6, Worksheet ON479 "Column 3: Line 63110 is more than
$1,666.82", line 6 "958.41": a printed constant."""

POLITICAL_CREDIT_COLUMN_3_LINE_7 = CATALOG.declare(
    "political_credit_column_3_line_7", Decimal, non_negative=True
)
"""Political contribution credit column 3 line 7, Worksheet ON479 "Column 3: Line 63110 is more than
$1,666.82", line 7 "Line 5 plus line 6 Enter this amount on line 16 of your Form ON479.": line 5
plus line 6."""

POLITICAL_CREDIT_BEFORE_MAXIMUM = CATALOG.declare(
    "political_credit_before_maximum", Decimal, non_negative=True
)
"""Political contribution credit before its maximum, Worksheet ON479 "Line 16 - Ontario political
contribution tax credit" line 7 "Enter this amount on line 16 of your Form ON479.": the line 7 of
the column that applies, column 1 if line 63110 is $500.05 or less, column 2 if it is more than
$500.05 but not more than $1,666.82, column 3 if it is more than $1,666.82."""

POLITICAL_CREDIT = CATALOG.declare("political_credit", Decimal, non_negative=True)
"""Ontario political contribution tax credit, Form ON479 line 16 "Enter $1,666.82 if your total
contributions are $3,793 or more. If not, use Worksheet ON479. (maximum $1,666.82)": the worksheet's
line 7, at most $1,666.82."""

FLOW_THROUGH_SHARE_SLIP_EXPENSES = CATALOG.declare(
    "flow_through_share_slip_expenses", Decimal, non_negative=True
)
"""Qualifying expenses of one slip, Form T1221 lines 1 to 3 "Enter the amount of qualifying
expenses.": the amounts from boxes 145 and 155 of a T101 slip or boxes 200 and 244 of a T5013 slip,
one line for each corporation or slip, taken as entered. The identification number the form asks
for beside it is not a field, as it feeds no calculation."""

FLOW_THROUGH_SHARE_SLIPS = RecordListKind.declare(
    CATALOG, "flow_through_share_slips", fields=(FLOW_THROUGH_SHARE_SLIP_EXPENSES,)
)
"""Slips for the focused flow-through share credit, Form T1221 lines 1 to 3 "Use a separate line to
enter the identification number for each corporation ... and the amounts from boxes 145 and 155 of
your T101 slips, or boxes 200 and 244 of your T5013 slips": one record for each slip, in the order
entered. A list may be empty."""

FLOW_THROUGH_SHARE_EXPENSES = CATALOG.declare(
    "flow_through_share_expenses", Decimal, non_negative=True
)
"""Total expenses of the flow-through share slips, Form T1221 line 4 "Add lines 1 to 3. Enter this
amount on line 63220 of your Form ON479.": the qualifying expenses of every slip, added."""

FLOW_THROUGH_SHARE_CREDIT = CATALOG.declare("flow_through_share_credit", Decimal, non_negative=True)
"""Focused flow-through share credit, Form ON479 line 17 and line 63220 "Enter your total expenses
from your Form T1221. multiplied by 5% =": the 5% on the total expenses of the slips."""

ONTARIO_CREDITS_SUBTOTAL = CATALOG.declare("ontario_credits_subtotal", Decimal, non_negative=True)
"""Ontario credits subtotal, Form ON479 line 18 "Add lines 1, 2, 13, 14, 16, and 17. =": here
lines 1, 14, 16 and 17, in line order. Line 19 "Amount from line 18 of the previous page" carries
it.

Not triggered by the returns modelled, or left to later work: lines 2 and 13."""

ONTARIO_CREDITS = CATALOG.declare("ontario_credits", Decimal, non_negative=True)
"""Ontario credits, Form ON479 line 21 "Line 19 plus line 20 Enter this amount online 47900 of
your return. Ontario credits =": line 19 "Amount from line 18 of the previous page", which carries
line 18.

Line 20 (the co-operative education credit) is not triggered by the returns modelled."""

REFUND_BEFORE_DONATION = CATALOG.declare("refund_before_donation", Decimal, non_negative=True)
"""Refund before the donation, Ontario opportunities fund line 1 "Amount from line 48400 above":
the refund."""

OPPORTUNITIES_FUND_DONATION = CATALOG.declare(
    "opportunities_fund_donation", Decimal, non_negative=True
)
"""Donation to the Ontario opportunities fund, line 2 and line 46500 "Your donation to the Ontario
opportunities fund": the part of the refund the filer gives, as entered."""

NET_REFUND = CATALOG.declare("net_refund", Decimal, non_negative=True)
"""Net refund, Ontario opportunities fund line 3 and line 46600 "Net refund (line 1 minus line
2) =": line 1 less line 2."""
