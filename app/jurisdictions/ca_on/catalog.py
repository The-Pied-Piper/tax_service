"""The Ontario artifact catalog: Ontario's own kinds, named from Forms ON428 (§2, §7), ON479, T1221.

Only the kinds in use are declared, each non-negative, as no ON428 or ON479 line here can be
negative: amounts are Decimal, the counts of dependent children and dependants int, and the T1221
slips and the co-operative education work placements record lists. Federal kinds come from
`app.jurisdictions.ca.catalog`. Identifiers are stable: `tests/jurisdictions/ca_on/test_catalog.py`
snapshots them.
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

MEDICAL_NET_INCOME_SHARE = CATALOG.declare("medical_net_income_share", Decimal, non_negative=True)
"""Share of the net income for medical expenses, ON428 line 39 "Line 37 multiplied by the percentage
from line 38" (line 37 "Amount from line 23600 of your return", line 38 "Applicable rate 3%"): 3%
of the net income."""

MEDICAL_THRESHOLD = CATALOG.declare("medical_threshold", Decimal, non_negative=True)
"""Threshold for medical expenses, ON428 line 40 "Enter whichever is less: $2,885 or the amount on
line 39.": the lesser of the ceiling and the share of the net income."""

MEDICAL_EXPENSES_OVER_THRESHOLD = CATALOG.declare(
    "medical_expenses_over_threshold", Decimal, non_negative=True
)
"""Medical expenses over the threshold, ON428 line 41 "Line 36 minus line 40 (if negative, enter
"0")": the filer's own group, not below zero."""

OTHER_DEPENDANTS_MEDICAL = CATALOG.declare("other_dependants_medical", Decimal, non_negative=True)
"""Allowable medical expenses for other dependants, ON428 line 42 and line 58729 "Allowable amount
of medical expenses for other dependants (use Worksheet ON428)": line 4 "Add the amounts from
line 3 of columns 1, 2, and 3 (and others, if any)", each line 3 being "Line 1 minus line 2 (if
negative, enter "0") (maximum $15,551 per dependant)"."""

MEDICAL_CLAIM = CATALOG.declare("medical_claim", Decimal, non_negative=True)
"""Allowable medical expenses, ON428 line 43 and line 58769 "Line 41 plus line 42": the filer's own
group plus the allowable amount for other dependants, a part of the total of the Ontario credit
amounts (line 58800)."""

CLAIMED_AS_ELIGIBLE_DEPENDANT = CATALOG.declare(
    "claimed_as_eligible_dependant", int, non_negative=True
)
"""Whether a dependant is the one claimed on line 58160, Worksheet ON428 "Line 58185 - Ontario
caregiver amount" line 4 "Amount claimed for this dependant on line 58160 of your Form ON428, if
any": 1 for the dependant claimed there, 0 for any other (any other count is read as claimed), a
field of each record of the caregiver dependants."""

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
caregiver amount (line 58185), the base CPP contributions (line 58240), the EI premiums
(line 58300) and the allowable medical expenses (line 58769)."""

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
"""LIFT credit at most its maximum, Schedule ON428-A line 5's "(maximum $875)", Part A line 14
"Amount from line 5 above (maximum $875)" and Part B line 29 "Amount from line 5 of the previous
page (maximum $875)"."""

LIFT_NET_INCOME_AND_REPAYMENTS = CATALOG.declare(
    "lift_net_income_and_repayments", Decimal, non_negative=False
)
"""Net income and repayments, Schedule ON428-A line 9 "Add lines 6 to 8.": line 6 "Net income from
line 23600 of your return (or the amount you would have entered if the instructions on line 23600
said "if negative, show in brackets")", line 7 "Amount from line 21300 of your return" and line 8
"Amount of registered disability savings plan (RDSP) income repayment included on line 23200 of
your return". Line 9 prints no floor and line 6 may be negative, so the kind is signed."""

LIFT_UCCB_AND_RDSP_INCOME = CATALOG.declare("lift_uccb_and_rdsp_income", Decimal, non_negative=True)
"""UCCB and RDSP income, Schedule ON428-A line 12 "Line 10 plus line 11": line 10 "Amount from line
11700 of your return" and line 11 "Amount of RDSP income included on line 12500 of your return"."""

LIFT_ADJUSTED_NET_INCOME = CATALOG.declare("lift_adjusted_net_income", Decimal, non_negative=True)
"""Adjusted net income, Schedule ON428-A line 13 "Line 9 minus line 12 (if negative, enter "0")
Your adjusted net income", which Part A line 15 "Amount from line 13 above" and Part B line 30
"Amount from line 13 of the previous page" take."""

LIFT_REDUCTION = CATALOG.declare("lift_reduction", Decimal, non_negative=True)
"""LIFT credit reduction, Schedule ON428-A Part A line 19 "Line 17 multiplied by the percentage
from line 18": line 18 "Applicable rate 5%" on line 17 "Line 15 minus line 16 (if negative, enter
"0")", line 16 "Individual income threshold 32,500.00".

Line 15 is "Amount from line 13 above", the adjusted net income (line 13). The schedule states no
eligibility rules of its own ("To find out if you are eligible for the low-income individuals and
families tax (LIFT) credit, go to canada.ca/on-tax-info.").
"""

LIFT_CREDIT_SINGLE = CATALOG.declare("lift_credit_single", Decimal, non_negative=True)
"""LIFT credit for a single individual, Schedule ON428-A Part A line 20 "Line 14 minus line 19 (if
negative, enter "0") Enter this amount on line 62140 of your Form ON428.": the maximum credit less
the reduction."""

LIFT_SPOUSE_AT_YEAR_END = CATALOG.declare("lift_spouse_at_year_end", int, non_negative=True)
"""Spouse or common-law partner at the end of the year, Schedule ON428-A "If you had a spouse or
common-law partner at the end of the year, complete Part B on the next page" (and "If you were
single at the end of the year, complete Part A"): a starting count, 0 or 1. The note "If your
spouse or common-law partner died at any time during the year, complete Part A as if you were
single" means the caller enters 0 then."""

LIFT_SPOUSE_NET_INCOME_AND_REPAYMENTS = CATALOG.declare(
    "lift_spouse_net_income_and_repayments", Decimal, non_negative=False
)
"""Spouse's net income and repayments, Schedule ON428-A Part B line 24 "Add lines 21 to 23.", the
sum of the caller's existing spouse inputs (`ca/spouse_net_income_before_adjustments`,
`ca/spouse_uccb_repayment`, `ca/spouse_rdsp_income_repayment`). Line 24 prints no floor and line 21
may be negative, so the kind is signed."""

LIFT_SPOUSE_UCCB_AND_RDSP_INCOME = CATALOG.declare(
    "lift_spouse_uccb_and_rdsp_income", Decimal, non_negative=True
)
"""Spouse's UCCB and RDSP income, Schedule ON428-A Part B line 27 "Line 25 plus line 26", the sum of
the caller's existing spouse inputs (`ca/spouse_universal_child_care_benefit`,
`ca/spouse_rdsp_income`)."""

LIFT_SPOUSE_ADJUSTED_NET_INCOME = CATALOG.declare(
    "lift_spouse_adjusted_net_income", Decimal, non_negative=True
)
"""Spouse's adjusted net income, Schedule ON428-A Part B line 28 "Line 24 minus line 27 (if
negative, enter "0") Your spouse's or common-law partner's adjusted net income"."""

LIFT_INDIVIDUAL_INCOME_THRESHOLD = CATALOG.declare(
    "lift_individual_income_threshold", Decimal, non_negative=True
)
"""Individual income threshold, Schedule ON428-A Part B line 31 "Individual income threshold
32,500.00": a printed amount, taken whole."""

LIFT_EXCESS_OVER_INDIVIDUAL_THRESHOLD = CATALOG.declare(
    "lift_excess_over_individual_threshold", Decimal, non_negative=True
)
"""Excess over the individual threshold, Schedule ON428-A Part B line 32 "Line 30 minus line 31 (if
negative, enter "0")", line 30 being "Amount from line 13 of the previous page"."""

LIFT_FAMILY_NET_INCOME = CATALOG.declare("lift_family_net_income", Decimal, non_negative=True)
"""Adjusted family net income, Schedule ON428-A Part B line 35 "Line 33 plus line 34 Adjusted
family net income": line 33 "Amount from line 30 above" and line 34 "Amount from line 28 above"."""

LIFT_FAMILY_INCOME_THRESHOLD = CATALOG.declare(
    "lift_family_income_threshold", Decimal, non_negative=True
)
"""Family income threshold, Schedule ON428-A Part B line 36 "Family income threshold 65,0000.00":
a printed amount, taken whole. The text prints a typo; the threshold is 65,000.00."""

LIFT_EXCESS_OVER_FAMILY_THRESHOLD = CATALOG.declare(
    "lift_excess_over_family_threshold", Decimal, non_negative=True
)
"""Excess over the family threshold, Schedule ON428-A Part B line 37 "Line 35 minus line 36 (if
negative, enter "0")"."""

LIFT_GREATER_EXCESS = CATALOG.declare("lift_greater_excess", Decimal, non_negative=True)
"""Greater excess, Schedule ON428-A Part B line 38 "Enter whichever is more: amount from line 32 or
line 37."."""

LIFT_FAMILY_REDUCTION = CATALOG.declare("lift_family_reduction", Decimal, non_negative=True)
"""LIFT credit reduction for a family, Schedule ON428-A Part B line 40 "Line 38 multiplied by the
percentage from line 39", line 39 being "Applicable rate 5%"."""

LIFT_CREDIT_WITH_SPOUSE = CATALOG.declare("lift_credit_with_spouse", Decimal, non_negative=True)
"""LIFT credit for an individual with a spouse or common-law partner, Schedule ON428-A Part B line
41 "Line 29 minus line 40 (if negative, enter "0") Enter this amount on line 62140 of your Form
ON428.": line 29 "Amount from line 5 of the previous page (maximum $875)" less the reduction."""

LIFT_CREDIT = CATALOG.declare("lift_credit", Decimal, non_negative=True)
"""LIFT credit, ON428 line 85 (62140) "Low-income individuals and families tax (LIFT) credit
(complete Schedule ON428-A)": Part A line 20 for a single individual, or Part B line 41 when there
was a spouse or common-law partner at the end of the year."""

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

CLAIMS_SENIORS_CARE_CREDIT = CATALOG.declare("claims_seniors_care_credit", int, non_negative=True)
"""Whether the filer claims the Ontario seniors care at home tax credit, Form ON479 line 13 and line
63095: a starting count, 0 or 1, that multiplies line 13, so 1 if the filer claims it, else 0.

The form prints no eligibility rules for the credit; the caller claims it only for a filer who
qualifies."""

SENIORS_CARE_BEFORE_MAXIMUM = CATALOG.declare(
    "seniors_care_before_maximum", Decimal, non_negative=True
)
"""Seniors care at home credit before its maximum, Form ON479 line 5 "Line 3 multiplied by the
percentage from line 4 (maximum $1,500) =" before the maximum: line 4 "Allowable percentage 25%" on
line 3 "Medical expenses from line 58769 of your Form ON428"."""

SENIORS_CARE_AMOUNT = CATALOG.declare("seniors_care_amount", Decimal, non_negative=True)
"""Seniors care at home credit amount, Form ON479 line 5 "Line 3 multiplied by the percentage from
line 4 (maximum $1,500) =": the 25% on the medical expenses, at most $1,500, the maximum being
printed after the percentage."""

SENIORS_CARE_FAMILY_NET_INCOME = CATALOG.declare(
    "seniors_care_family_net_income", Decimal, non_negative=True
)
"""Family net income, Form ON479 line 8 "Line 6 plus line 7 Family net income =": line 6 "Your net
income from line 23600 of your return" plus line 7 "Your spouse's or common-law partner's net
income from line 23600 of their return (if applicable)", 0 with no spouse."""

SENIORS_CARE_BASE_AMOUNT = CATALOG.declare("seniors_care_base_amount", Decimal, non_negative=True)
"""Form ON479 line 9 "Base amount 35,000.00": the dataset's amount as an artifact."""

SENIORS_CARE_INCOME_OVER_BASE = CATALOG.declare(
    "seniors_care_income_over_base", Decimal, non_negative=True
)
"""Family net income over the base amount, Form ON479 line 10 "Line 8 minus line 9 (if negative,
enter "0") =": not below zero."""

SENIORS_CARE_REDUCTION = CATALOG.declare("seniors_care_reduction", Decimal, non_negative=True)
"""Seniors care at home credit reduction, Form ON479 line 12 "Line 10 multiplied by the percentage
from line 11 =": line 11 "Applicable rate 5%" on the family net income over the base amount."""

SENIORS_CARE_BEFORE_CLAIM = CATALOG.declare("seniors_care_before_claim", Decimal, non_negative=True)
"""Seniors care at home credit before the claim, Form ON479 line 13 "Line 5 minus line 12 (if
negative, enter "0") =": the amount less the reduction, not below zero. The form's rules for a
family net income of $35,000 or less and of more than $65,000 follow from lines 9 to 12."""

SENIORS_CARE_CREDIT = CATALOG.declare("seniors_care_credit", Decimal, non_negative=True)
"""Ontario seniors care at home tax credit, Form ON479 line 13 and line 63095 "Line 5 minus line 12
(if negative, enter "0") =": line 13 once if the filer claims the credit, else 0."""

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

COOP_EDUCATION_PAYROLL = CATALOG.declare("coop_education_payroll", Decimal, non_negative=True)
"""Total salaries and wages paid in the 2024 taxation year, Worksheet ON479 "Line 20 - Ontario
co-operative education tax credit" line 4: a starting amount, taken as entered."""

COOP_EDUCATION_PAYROLL_THRESHOLD = CATALOG.declare(
    "coop_education_payroll_threshold", Decimal, non_negative=True
)
"""Worksheet ON479 "Line 20" line 5 "400,000.00": the dataset's amount as an artifact."""

COOP_EDUCATION_PAYROLL_OVER_THRESHOLD = CATALOG.declare(
    "coop_education_payroll_over_threshold", Decimal, non_negative=True
)
"""Worksheet ON479 "Line 20" line 6 "Line 4 minus line 5 (if negative, enter "0") =": the payroll
over $400,000, not below zero."""

COOP_EDUCATION_PAYROLL_RANGE = CATALOG.declare(
    "coop_education_payroll_range", Decimal, non_negative=True
)
"""Worksheet ON479 "Line 20" line 7 "200,000.00": the dataset's amount as an artifact."""

COOP_EDUCATION_PHASE_OUT_SHARE = CATALOG.declare(
    "coop_education_phase_out_share", Decimal, non_negative=True
)
"""Worksheet ON479 "Line 20" line 8 "Line 6 divided by line 7 =", which line 10 "Amount from line 8
above" repeats: an exact fraction, never rounded."""

COOP_EDUCATION_FULL_SHARE = CATALOG.declare("coop_education_full_share", Decimal, non_negative=True)
"""Worksheet ON479 "Line 20" line 9 "1.00": the dataset's amount as an artifact."""

COOP_EDUCATION_REMAINING_SHARE = CATALOG.declare(
    "coop_education_remaining_share", Decimal, non_negative=True
)
"""Worksheet ON479 "Line 20" line 11 "Line 9 minus line 10 (if negative, enter "0") =": the share
of the 5% that remains."""

COOP_EDUCATION_PLACEMENT_EXPENDITURES = CATALOG.declare(
    "coop_education_placement_expenditures", Decimal, non_negative=True
)
"""Eligible expenditures of one work placement, Worksheet ON479 "Line 20" line 1 "Amount of
eligible expenditures (Note 1) incurred in 2025 Line A": already reduced by government assistance
as Note 1 asks, taken as entered."""

COOP_EDUCATION_PLACEMENTS = RecordListKind.declare(
    CATALOG, "coop_education_placements", fields=(COOP_EDUCATION_PLACEMENT_EXPENDITURES,)
)
"""Qualifying work placements, Worksheet ON479 "Line 20" "complete this chart for each qualifying
work placement": one record for each placement, in the order entered. A list may be empty."""

COOP_EDUCATION_PLACEMENT_COUNT = CATALOG.declare(
    "coop_education_placement_count", int, non_negative=True
)
"""Number of work placements, Form ON479 line 63260 "Number of eligible work placements your
business or partnership is claiming under the Ontario co-operative education tax credit program":
the placements in the list."""

COOP_EDUCATION_CREDIT = CATALOG.declare("coop_education_credit", Decimal, non_negative=True)
"""Co-operative education credit, Form ON479 line 20 and line 63300 "Enter the total amount claimed
for all qualifying work placements. (maximum $3,000 per student)": the total of the placements'
Worksheet ON479 line 13, each at most $3,000."""

ONTARIO_CREDITS_SUBTOTAL = CATALOG.declare("ontario_credits_subtotal", Decimal, non_negative=True)
"""Ontario credits subtotal, Form ON479 line 18 "Add lines 1, 2, 13, 14, 16, and 17. =": here
lines 1, 14, 16 and 17, in line order. Line 19 "Amount from line 18 of the previous page" carries
it.

Not triggered by the returns modelled, or left to later work: lines 2 and 13."""

ONTARIO_CREDITS = CATALOG.declare("ontario_credits", Decimal, non_negative=True)
"""Ontario credits, Form ON479 line 21 "Line 19 plus line 20 Enter this amount online 47900 of
your return. Ontario credits =": line 19 "Amount from line 18 of the previous page", which carries
line 18.

Line 20 is the co-operative education credit."""

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
