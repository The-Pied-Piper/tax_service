"""The federal Canada artifact catalog: artifact kinds named from Canada's own return (§2, §7).

Only the kinds in use are declared, each non-negative but three: none of these lines can be negative
on the return as modelled except the refund or balance owing, where negative means a refund, and
lines 5 and 9 of the Federal Worksheet for line 25000, which print no floor. Amounts are Decimal;
the counts of eligible dependants, of infirm children, of the eligible children for child care
(Form T778 Part B lines 1 to 3), of the Schedule 6 eligible dependants (line 38100) and the two
starting counts of the Federal Worksheet for line 25000 int. Identifiers are stable:
`tests/jurisdictions/ca/test_catalog.py` snapshots them.
"""

from __future__ import annotations

from decimal import Decimal

from app.domain.artifact import ArtifactCatalog
from app.domain.registry import Namespace
from app.jurisdictions.ca import NAMESPACE

CATALOG = ArtifactCatalog(Namespace(NAMESPACE))

EMPLOYMENT_INCOME = CATALOG.declare("employment_income", Decimal, non_negative=True)
"""Employment income, T1 line 10100: a starting amount that total income sums directly."""

CAPITAL_GAIN = CATALOG.declare("capital_gain", Decimal, non_negative=True)
"""The claimed capital gain before inclusion, mirroring Schedule 3 line 21 (total capital gains
or losses).

Losses, and netting gains against them, are not modelled yet, so the kind is declared
non-negative; net gains or losses, when modelled, will be a different kind.
"""

TAXABLE_CAPITAL_GAINS = CATALOG.declare("taxable_capital_gains", Decimal, non_negative=True)
"""Taxable capital gains, T1 line 12700: the capital gain times the inclusion rate (Schedule 3
lines 23 to 26)."""

TOTAL_INCOME = CATALOG.declare("total_income", Decimal, non_negative=True)
"""Total income, T1 line 15000 "Line 28 plus line 32 Total income": the sum of the income lines
wired so far, in line order, with the taxable dividends (line 12000), the taxable capital gains
and the taxable support payments.

Not wired yet: rental income (line 13) and self-employment income (lines 22 to 26).
"""

OTHER_EMPLOYMENT_INCOME = CATALOG.declare("other_employment_income", Decimal, non_negative=True)
"""Other employment income, T1 line 10400 "Other employment income": a starting amount."""

OLD_AGE_SECURITY = CATALOG.declare("old_age_security", Decimal, non_negative=True)
"""Old age security pension, T1 line 11300 "Old age security (OAS) pension (box 18 of the T4A(OAS)
slip)": a starting amount."""

CPP_OR_QPP_BENEFITS = CATALOG.declare("cpp_or_qpp_benefits", Decimal, non_negative=True)
"""CPP or QPP benefits, T1 line 11400 "CPP or QPP benefits (box 20 of the T4A(P) slip)": a starting
amount."""

OTHER_PENSIONS_AND_SUPERANNUATION = CATALOG.declare(
    "other_pensions_and_superannuation", Decimal, non_negative=True
)
"""Other pensions and superannuation, T1 line 11500 "Other pensions and superannuation": a starting
amount."""

ELECTED_SPLIT_PENSION_AMOUNT = CATALOG.declare(
    "elected_split_pension_amount", Decimal, non_negative=True
)
"""Elected split-pension amount, T1 line 11600 "Elected split-pension amount (complete Form T1032)":
the election made with the spouse or common-law partner, a starting amount."""

UNIVERSAL_CHILD_CARE_BENEFIT = CATALOG.declare(
    "universal_child_care_benefit", Decimal, non_negative=True
)
"""Universal child care benefit, T1 line 11700 "Universal child care benefit (UCCB) (see the RC62
slip)": a starting amount."""

EI_AND_OTHER_BENEFITS = CATALOG.declare("ei_and_other_benefits", Decimal, non_negative=True)
"""Employment insurance and other benefits, T1 line 11900 "Employment insurance (EI) and other
benefits (box 14 of the T4E slip)": a starting amount."""

T3_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE = CATALOG.declare(
    "t3_taxable_dividends_other_than_eligible", Decimal, non_negative=True
)
"""T3 taxable dividends other than eligible, Federal Worksheet for lines 12000 and 12010 line 1 "Box
32 of all T3 slips": a starting amount."""

T4PS_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE = CATALOG.declare(
    "t4ps_taxable_dividends_other_than_eligible", Decimal, non_negative=True
)
"""T4PS taxable dividends other than eligible, Federal Worksheet for lines 12000 and 12010 line 2
"Box 25 of all T4PS slips": a starting amount."""

T5_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE = CATALOG.declare(
    "t5_taxable_dividends_other_than_eligible", Decimal, non_negative=True
)
"""T5 taxable dividends other than eligible, Federal Worksheet for lines 12000 and 12010 line 3 "Box
11 of all T5 slips": a starting amount."""

T5013_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE = CATALOG.declare(
    "t5013_taxable_dividends_other_than_eligible", Decimal, non_negative=True
)
"""T5013 taxable dividends other than eligible, Federal Worksheet for lines 12000 and 12010 line 4
"Box 130 of all T5013 slips": a starting amount."""

T3_TAXABLE_DIVIDENDS = CATALOG.declare("t3_taxable_dividends", Decimal, non_negative=True)
"""T3 taxable dividends, Federal Worksheet for lines 12000 and 12010 line 6 "Boxes 32 and 50 of all
T3 slips": a starting amount."""

T4PS_TAXABLE_DIVIDENDS = CATALOG.declare("t4ps_taxable_dividends", Decimal, non_negative=True)
"""T4PS taxable dividends, Federal Worksheet for lines 12000 and 12010 line 7 "Boxes 25 and 31 of
all T4PS slips": a starting amount."""

T5_TAXABLE_DIVIDENDS = CATALOG.declare("t5_taxable_dividends", Decimal, non_negative=True)
"""T5 taxable dividends, Federal Worksheet for lines 12000 and 12010 line 8 "Boxes 11 and 25 of all
T5 slips": a starting amount."""

T5013_TAXABLE_DIVIDENDS = CATALOG.declare("t5013_taxable_dividends", Decimal, non_negative=True)
"""T5013 taxable dividends, Federal Worksheet for lines 12000 and 12010 line 9 "Boxes 130 and 133 of
all T5013 slips": a starting amount."""

ELIGIBLE_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP = CATALOG.declare(
    "eligible_dividends_received_without_a_slip", Decimal, non_negative=True
)
"""Eligible dividends received with no slip, Federal Worksheet for lines 12000 and 12010 line 11
"Actual amount of eligible dividends received", under "Taxable amount of dividends if you did not
receive an information slip": a starting amount."""

OTHER_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP = CATALOG.declare(
    "other_dividends_received_without_a_slip", Decimal, non_negative=True
)
"""Other dividends received with no slip, Federal Worksheet for lines 12000 and 12010 line 14
"Actual amount of dividends other than eligible dividends received", under "Taxable amount of
dividends if you did not receive an information slip": a starting amount."""

T3_DIVIDEND_TAX_CREDIT = CATALOG.declare("t3_dividend_tax_credit", Decimal, non_negative=True)
"""T3 dividend tax credit, Federal Worksheet for line 40425 line 1 "Boxes 39 and 51 of all T3
slips": a starting amount."""

T4PS_DIVIDEND_TAX_CREDIT = CATALOG.declare("t4ps_dividend_tax_credit", Decimal, non_negative=True)
"""T4PS dividend tax credit, Federal Worksheet for line 40425 line 2 "Boxes 26 and 32 of all T4PS
slips": a starting amount."""

T5_DIVIDEND_TAX_CREDIT = CATALOG.declare("t5_dividend_tax_credit", Decimal, non_negative=True)
"""T5 dividend tax credit, Federal Worksheet for line 40425 line 3 "Boxes 12 and 26 of all T5
slips": a starting amount."""

T5013_DIVIDEND_TAX_CREDIT = CATALOG.declare("t5013_dividend_tax_credit", Decimal, non_negative=True)
"""T5013 dividend tax credit, Federal Worksheet for line 40425 line 4 "Boxes 131 and 134 of all
T5013 slips": a starting amount."""

SLIP_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE = CATALOG.declare(
    "slip_taxable_dividends_other_than_eligible", Decimal, non_negative=True
)
"""Slip taxable dividends other than eligible, Federal Worksheet for lines 12000 and 12010 line 5
"Add lines 1 to 4. Enter this amount on line 12010 of your return.": the four slip boxes of lines 1
to 4."""

SLIP_TAXABLE_DIVIDENDS = CATALOG.declare("slip_taxable_dividends", Decimal, non_negative=True)
"""Slip taxable dividends, Federal Worksheet for lines 12000 and 12010 line 10 "Add lines 6 to 9.
Enter this amount on line 12000 of your return.": the four slip boxes of lines 6 to 9."""

ELIGIBLE_DIVIDENDS_GROSSED_UP = CATALOG.declare(
    "eligible_dividends_grossed_up", Decimal, non_negative=True
)
"""Eligible dividends grossed up, Federal Worksheet for lines 12000 and 12010 line 13 "Line 11
multiplied by the percentage from line 12": line 12 "Applicable rate 138%" on the eligible dividends
received with no slip."""

OTHER_DIVIDENDS_GROSSED_UP = CATALOG.declare(
    "other_dividends_grossed_up", Decimal, non_negative=True
)
"""Other dividends grossed up, Federal Worksheet for lines 12000 and 12010 line 16 "Line 14
multiplied by the percentage from line 15 Include this amount on line 12010 of your return.": line
15 "Applicable rate 115%" on the dividends other than eligible received with no slip."""

DIVIDENDS_WITHOUT_A_SLIP_GROSSED_UP = CATALOG.declare(
    "dividends_without_a_slip_grossed_up", Decimal, non_negative=True
)
"""Dividends with no slip, grossed up, Federal Worksheet for lines 12000 and 12010 line 17 "Line 13
plus line 16. Include this amount on line 12000 of your return.": the grossed-up eligible dividends
and the grossed-up other dividends."""

TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE = CATALOG.declare(
    "taxable_dividends_other_than_eligible", Decimal, non_negative=True
)
"""Taxable dividends other than eligible, T1 line 12010 "Amount of dividends (other than
eligible)" (use Federal Worksheet): the slip amount (line 5) plus the amount with no slip (line 16).

No federal line reads it, so the manifest returns it as a return line."""

TAXABLE_DIVIDENDS = CATALOG.declare("taxable_dividends", Decimal, non_negative=True)
"""Taxable dividends, T1 line 12000 "Amount of dividends (eligible and other than eligible)"
(use Federal Worksheet): the slip amount (line 10) plus the amount with no slip (line 17); total
income sums it."""

SLIP_DIVIDEND_TAX_CREDIT = CATALOG.declare("slip_dividend_tax_credit", Decimal, non_negative=True)
"""Slip dividend tax credit, Federal Worksheet for line 40425 line 5 "Add lines 1 to 4.": the
credits shown on the T3, T4PS, T5 and T5013 slips, which the worksheet enters on line 40425 as they
are."""

DIVIDENDS_AMOUNT_A = CATALOG.declare("dividends_amount_a", Decimal, non_negative=True)
"""Dividends amount A, Federal Worksheet for line 40425 line A "Amount from line 12000 of your
return (Note 1)", Note 1 being "Enter only the amount of dividends that were not shown on an
information slip.": the worksheet's line 17 for lines 12000 and 12010, the grossed-up dividends with
no slip."""

DIVIDENDS_AMOUNT_B = CATALOG.declare("dividends_amount_b", Decimal, non_negative=True)
"""Dividends amount B, Federal Worksheet for line 40425 line B "Amount from line 12010 of your
return (Note 1)", Note 1 being "Enter only the amount of dividends that were not shown on an
information slip.": the worksheet's line 16 for lines 12000 and 12010, the grossed-up other
dividends with no slip."""

OTHER_DIVIDENDS_CREDIT = CATALOG.declare("other_dividends_credit", Decimal, non_negative=True)
"""Credit on other dividends, Federal Worksheet for line 40425 line 6 "Line B multiplied by
9.0301%": the amount B times the credit rate for dividends other than eligible."""

DIVIDENDS_AMOUNT_A_LESS_B = CATALOG.declare("dividends_amount_a_less_b", Decimal, non_negative=True)
"""Dividends amount A less amount B, Federal Worksheet for line 40425 line C "Amount A minus amount
B": the grossed-up eligible dividends with no slip."""

ELIGIBLE_DIVIDENDS_CREDIT = CATALOG.declare("eligible_dividends_credit", Decimal, non_negative=True)
"""Credit on eligible dividends, Federal Worksheet for line 40425 line 7 (printed "Line 2") "Line C
multiplied by 15.0198%": the amount A less amount B times the credit rate for eligible dividends."""

NO_SLIP_DIVIDEND_TAX_CREDIT = CATALOG.declare(
    "no_slip_dividend_tax_credit", Decimal, non_negative=True
)
"""Dividend tax credit with no slip, Federal Worksheet for line 40425 line 8 "Line 6 plus line 7":
the credit on other dividends and the credit on eligible dividends."""

DIVIDEND_TAX_CREDIT = CATALOG.declare("dividend_tax_credit", Decimal, non_negative=True)
"""Federal dividend tax credit, T1 line 123 (line 40425) "Federal dividend tax credit (use Federal
Worksheet)": Federal Worksheet line 9 "Line 5 plus line 8 Enter this amount on line 40425 of your
return.", the slip credits and the credit with no slip."""

CREDITS_AGAINST_BASIC_FEDERAL_TAX = CATALOG.declare(
    "credits_against_basic_federal_tax", Decimal, non_negative=True
)
"""Credits against the basic federal tax, T1 line 125 "Add lines 122 to 124.": line 122 "Amount from
line 35000" and line 123 (40425), the federal dividend tax credit, in line order.

Line 124 (40427, minimum tax carryover) is not modelled."""

T3_INVESTMENT_INCOME = CATALOG.declare("t3_investment_income", Decimal, non_negative=True)
"""T3 investment income, Federal Worksheet for line 12100 line 1 "Box 25 of all T3 slips": a
starting amount."""

T5_INVESTMENT_INCOME = CATALOG.declare("t5_investment_income", Decimal, non_negative=True)
"""T5 investment income, Federal Worksheet for line 12100 line 2 "Boxes 13, 14, 15, and 30 of all T5
slips": a starting amount."""

T5013_INVESTMENT_INCOME = CATALOG.declare("t5013_investment_income", Decimal, non_negative=True)
"""T5013 investment income, Federal Worksheet for line 12100 line 3 "Boxes 128, 135, and 146 of all
T5013 slips": a starting amount."""

INVESTMENT_INCOME_CREDITED_NOT_RECEIVED = CATALOG.declare(
    "investment_income_credited_not_received", Decimal, non_negative=True
)
"""Investment income credited and not received, Federal Worksheet for line 12100 line 4 "Amounts
credited to you that you did not receive (such as reinvestments)": a starting amount."""

TAX_REFUND_INTEREST = CATALOG.declare("tax_refund_interest", Decimal, non_negative=True)
"""Interest on a tax refund, Federal Worksheet for line 12100 line 5 "Interest on any tax refund you
received in 2025 as shown on your notice of assessment or reassessment": a starting amount."""

FOREIGN_INVESTMENT_INCOME = CATALOG.declare("foreign_investment_income", Decimal, non_negative=True)
"""Foreign investment income, Federal Worksheet for line 12100 line 6 "Income from foreign sources,
including foreign dividends, in Canadian dollars": a starting amount."""

INVESTMENT_INCOME_WITHOUT_A_SLIP = CATALOG.declare(
    "investment_income_without_a_slip", Decimal, non_negative=True
)
"""Investment income with no slip, Federal Worksheet for line 12100 line 7 "Interest or income
earned from bank accounts, term deposits, guaranteed investment certificates (GICs), and other
similar investments, treasury bills or life insurance policies not reported on any information
slip": a starting amount."""

INVESTMENT_ROYALTIES = CATALOG.declare("investment_royalties", Decimal, non_negative=True)
"""Investment royalties, Federal Worksheet for line 12100 line 8 "Royalties not included on line
10400 or line 13500 of your return": a starting amount."""

INVESTMENT_INCOME_BEFORE_PRIOR_YEARS = CATALOG.declare(
    "investment_income_before_prior_years", Decimal, non_negative=True
)
"""Investment income before the part reported in previous years, Federal Worksheet for line 12100
line 9 "Add lines 1 to 8.": the sum of the eight sources."""

INVESTMENT_INCOME_REPORTED_IN_PREVIOUS_YEARS = CATALOG.declare(
    "investment_income_reported_in_previous_years", Decimal, non_negative=True
)
"""Investment income reported in previous years, Federal Worksheet for line 12100 line 10 "Interest
and other investment income, included on line 9, received and reported in previous years": a
starting amount."""

INTEREST_AND_OTHER_INVESTMENT_INCOME = CATALOG.declare(
    "interest_and_other_investment_income", Decimal, non_negative=True
)
"""Interest and other investment income, T1 line 12100 "Interest and other investment income (use
Federal Worksheet)": Federal Worksheet line 11 "Line 9 minus line 10. Enter this amount on line
12100 of your return.", the investment income less the part reported in previous years."""

NET_PARTNERSHIP_INCOME = CATALOG.declare("net_partnership_income", Decimal, non_negative=True)
"""Net partnership income, T1 line 12200 "Net partnership income (limited or non-active partners
only)": a starting amount."""

RDSP_INCOME = CATALOG.declare("rdsp_income", Decimal, non_negative=True)
"""Registered disability savings plan income, T1 line 12500 "Registered disability savings plan
(RDSP) income (box 131 of the T4A slip)": a starting amount."""

TAXABLE_SUPPORT_PAYMENTS = CATALOG.declare("taxable_support_payments", Decimal, non_negative=True)
"""Taxable support payments, T1 line 12800 "Taxable amount": a starting amount."""

RRSP_INCOME = CATALOG.declare("rrsp_income", Decimal, non_negative=True)
"""RRSP income, T1 line 12900 "Registered retirement savings plan (RRSP) income (from all T4RSP
slips)": a starting amount."""

FHSA_INCOME = CATALOG.declare("fhsa_income", Decimal, non_negative=True)
"""Taxable FHSA income, T1 line 12905 "Taxable first home savings account (FHSA) income (see the
T4FHSA slip)": a starting amount."""

OTHER_FHSA_INCOME = CATALOG.declare("other_fhsa_income", Decimal, non_negative=True)
"""Taxable FHSA income - other, T1 line 12906 "Taxable FHSA income - other (see the T4FHSA slip)": a
starting amount."""

OTHER_INCOME = CATALOG.declare("other_income", Decimal, non_negative=True)
"""Other income, T1 line 13000 "Other income": a starting amount."""

TAXABLE_SCHOLARSHIPS = CATALOG.declare("taxable_scholarships", Decimal, non_negative=True)
"""Taxable scholarships, T1 line 13010 "Taxable scholarships, fellowships, bursaries and artists'
project grants": a starting amount."""

WORKERS_COMPENSATION_BENEFITS = CATALOG.declare(
    "workers_compensation_benefits", Decimal, non_negative=True
)
"""Workers' compensation benefits, T1 line 14400 "Workers' compensation benefits (box 10 of the
T5007 slip)": a starting amount."""

SOCIAL_ASSISTANCE_PAYMENTS = CATALOG.declare(
    "social_assistance_payments", Decimal, non_negative=True
)
"""Social assistance payments, T1 line 14500 "Social assistance payments": a starting amount."""

NET_FEDERAL_SUPPLEMENTS = CATALOG.declare("net_federal_supplements", Decimal, non_negative=True)
"""Net federal supplements paid, T1 line 14600 "Net federal supplements paid (box 21 of the T4A(OAS)
slip)": a starting amount."""

INCOME_SUPPORT_BENEFITS = CATALOG.declare("income_support_benefits", Decimal, non_negative=True)
"""Income support benefits, T1 line 14700 "Add lines 29 to 31 (see line 25000 in Step 4).": the
workers' compensation benefits, social assistance payments and net federal supplements."""

UNUSED_RRSP_CONTRIBUTIONS = CATALOG.declare("unused_rrsp_contributions", Decimal, non_negative=True)
"""Unused RRSP contributions, Schedule 7 line 1 "Enter your unused RRSP contributions previously
reported and available to deduct for 2025 as shown on your latest notice of assessment or
reassessment, or Form T1028 for 2025": the contributions previously reported and not yet
deducted, a starting amount."""

RRSP_CONTRIBUTIONS = CATALOG.declare("rrsp_contributions", Decimal, non_negative=True)
"""RRSP contributions, Schedule 7 line 4 (line 24500) "Line 2 plus line 3": the contributions made
from March 4, 2025, to March 2, 2026, a starting amount.

Line 2 is "Enter contributions made to your RRSP, SPP or PRPP, or to your spouse's or common-law
partner's RRSP or SPP from March 4, 2025, to December 31, 2025 (attach all receipts)."; line 3 is
the same contributions "from January 1, 2026, to March 2, 2026".
"""

RRSP_CONTRIBUTIONS_AVAILABLE = CATALOG.declare(
    "rrsp_contributions_available", Decimal, non_negative=True
)
"""RRSP contributions available to deduct, Schedule 7 line 10 "Line 6 minus line 9 Contributions
available to deduct": the unused contributions plus the contributions.

Line 5 is "Line 1 plus line 4 ... Total contributions"; line 6 "Total contributions from line 5".
With line 9 at 0, line 10 is line 5. Not triggered by the returns modelled: HBP and LLP repayments
(lines 7 to 9).
"""

RRSP_DEDUCTION_LIMIT = CATALOG.declare("rrsp_deduction_limit", Decimal, non_negative=True)
"""RRSP deduction limit, Schedule 7 line 11 "Enter your RRSP deduction limit for 2025 as shown on
your latest notice of assessment or reassessment, or Form T1028 for 2025.": a starting amount."""

RRSP_DEDUCTION_MAXIMUM = CATALOG.declare("rrsp_deduction_maximum", Decimal, non_negative=True)
"""RRSP deduction maximum, Schedule 7 line 17 "Enter whichever is less: amount from line 13 or line
16.": the lesser of the contributions available to deduct and the deduction limit, the most that
may be deducted.

Line 13 is "Line 11 minus line 12"; line 16 "Line 14 minus line 15". With lines 12 and 15 at 0,
line 13 is the limit and line 16 the contributions available to deduct. Not triggered by the
returns modelled: employer PRPP contributions (line 12) and transfers (line 15).
"""

RRSP_AMOUNT_DEDUCTED = CATALOG.declare("rrsp_amount_deducted", Decimal, non_negative=True)
"""RRSP amount deducted, Schedule 7 line 18 "Enter your RRSP, PRPP, or SPP contributions you are
deducting for 2025 (cannot be more than the amount on line 17).": the amount the filer chooses to
deduct, a starting amount, refused when above line 17."""

RRSP_DEDUCTION = CATALOG.declare("rrsp_deduction", Decimal, non_negative=True)
"""RRSP deduction, Schedule 7 line 20 "Enter whichever is less: amount from line 10 or line 19.
Enter this amount on line 20800 of your return. RRSP deduction": the amount deducted, at most the
deduction maximum, the T1 line 20800 deduction from total income.

Line 19 is "Line 15 plus line 18". With line 15 at 0, line 19 is line 18, at most line 17 and so
at most line 10, and line 20 is line 18 itself. Not triggered by the returns modelled: transfers
(line 15).
"""

UNUSED_RRSP_CONTRIBUTIONS_CARRIED_FORWARD = CATALOG.declare(
    "unused_rrsp_contributions_carried_forward", Decimal, non_negative=True
)
"""Unused RRSP contributions carried forward, Schedule 7 line 23 "Line 21 minus line 22 Your unused
contributions available to carry forward to a future year": the contributions available to deduct
less the RRSP deduction, a product of the return for the next year's line 1.

Line 21 is "Enter your contributions available to deduct from line 10 of the previous page."; line
22 "Enter your RRSP deduction from line 20 of the previous page.". Never negative, as line 20 is
at most line 10.
"""

UNION_DUES = CATALOG.declare("union_dues", Decimal, non_negative=True)
"""Union dues, T1 line 21200 "Annual union, professional, or like dues (receipts and box 44 of all
T4 slips)": the amount claimed, a starting amount."""

CHILD_CARE_EXPENSES_PAID = CATALOG.declare("child_care_expenses_paid", Decimal, non_negative=True)
"""Child care expenses paid, Form T778 Part A line 67950 "Total (add all entries for Child care
expenses paid)": a starting amount, also Part B line 5 "Enter the amount from line 67950."."""

CHILDREN_UNDER_SEVEN = CATALOG.declare("children_under_seven", int, non_negative=True)
"""Number of eligible children born in 2019 or later, Form T778 Part B line 1 "Number of eligible
children born in 2019 or later whom the disability amount cannot be claimed for": a starting
count."""

CHILDREN_WITH_DISABILITY = CATALOG.declare("children_with_disability", int, non_negative=True)
"""Number of eligible children with the disability amount, Form T778 Part B line 2 (line 67960)
"Number of eligible children born in 2025 or earlier whom the disability amount can be claimed
for": a starting count."""

CHILDREN_SEVEN_TO_SIXTEEN = CATALOG.declare("children_seven_to_sixteen", int, non_negative=True)
"""Number of eligible children born in 2009 to 2018, Form T778 Part B line 3 "Number of eligible
children born in 2009 to 2018 (and born in 2008 or earlier with a mental or physical infirmity
whom the disability amount cannot be claimed for)": a starting count."""

CHILD_CARE_LIMIT_FOR_CHILDREN_UNDER_SEVEN = CATALOG.declare(
    "child_care_limit_for_children_under_seven", Decimal, non_negative=True
)
"""Child care limit for the children born in 2019 or later, Form T778 Part B line 1 "multiplied by
$8,000": the line 1 count times $8,000, a part of line 4."""

CHILD_CARE_LIMIT_FOR_CHILDREN_WITH_DISABILITY = CATALOG.declare(
    "child_care_limit_for_children_with_disability", Decimal, non_negative=True
)
"""Child care limit for the children with the disability amount, Form T778 Part B line 2 (line
67960) "multiplied by $11,000": the line 2 count times $11,000, a part of line 4."""

CHILD_CARE_LIMIT_FOR_CHILDREN_SEVEN_TO_SIXTEEN = CATALOG.declare(
    "child_care_limit_for_children_seven_to_sixteen", Decimal, non_negative=True
)
"""Child care limit for the children born in 2009 to 2018, Form T778 Part B line 3 "multiplied by
$5,000": the line 3 count times $5,000, a part of line 4."""

CHILD_CARE_BASIC_LIMIT = CATALOG.declare("child_care_basic_limit", Decimal, non_negative=True)
"""Child care basic limit, Form T778 Part B line 4 "Add lines 1 to 3.": the limits for each group
of eligible children, in line order."""

CHILD_CARE_EARNED_INCOME = CATALOG.declare("child_care_earned_income", Decimal, non_negative=True)
"""Earned income for child care, Form T778 Part B line 6 "Enter your earned income.": "Your earned
income of line 6 is the total of the following: employment income (including tips and gratuities,
and the non-taxable part of an allowance received as an emergency volunteer) ...", here employment
income alone.

The other parts of earned income the form's "Earned income" definition lists are not triggered by
the returns modelled.
"""

CHILD_CARE_EARNED_INCOME_LIMIT = CATALOG.declare(
    "child_care_earned_income_limit", Decimal, non_negative=True
)
"""Earned income limit for child care, Form T778 Part B line 6 "multiplied by two-thirds": the
earned income times two-thirds, rounded half-up to the cent, once, as line 6 is a dollars-and-cents
box."""

CHILD_CARE_EXPENSES = CATALOG.declare("child_care_expenses", Decimal, non_negative=True)
"""Child care expenses deduction, T1 line 41 (line 21400) "Child care expenses (complete Form
T778)": Form T778 Part B line 7 "Enter whichever amount is the least: line 4, line 5 or line 6.",
carried by line 9 "Line 7 minus line 8. ... enter this amount on line 21400 of your return.
Allowable deduction", a deduction from total income.

Line 8 (the other person with the higher net income) is not triggered, so line 9 is line 7; nor
are Parts C and D (the higher-income claimant, school attendance). Eligibility is the return's to
state, not computed here.
"""

CPP_FIRST_ADDITIONAL_CONTRIBUTIONS = CATALOG.declare(
    "cpp_first_additional_contributions", Decimal, non_negative=True
)
"""First additional CPP contributions, Schedule 8 Part 3 line 12 "amount from line 7 multiplied
by 1% (maximum $678.00)": the required contributions on the employment income between the basic
exemption and the maximum pensionable earnings. Line 18 is "Amount from line 12"; Part 3b line 37
"If line 19 is positive or "0", enter the amount from line 18 at line 37 and line 43, and continue
at line 44." carries it into line 48 (Part 3a line 26 into line 28 when line 24 is positive).

Line 7 is "Line 5 minus line 6 (if negative, enter "0") (maximum $67,800)", the same earnings
as the base contributions'.
"""

CPP_SECOND_ADDITIONAL_CONTRIBUTIONS = CATALOG.declare(
    "cpp_second_additional_contributions", Decimal, non_negative=True
)
"""Second additional CPP contributions, Schedule 8 Part 3 line 22 "amount from line 4 multiplied
by 4% (maximum $396.00)": the required contributions on the employment income between the
maximum and the additional maximum pensionable earnings. Part 3b line 44 "If line 23 is positive
or "0", enter the amount from line 22 on line 44 and line 47, and continue at line 48." carries it
into line 48 (Part 3a line 27 "Amount from line 22 (if any)" into line 28 when line 24 is
positive).

Line 4 is "Line 2 minus line 3 (if negative, enter "0")": the earnings, at most the additional
maximum (line 2), less the maximum pensionable earnings (line 3).
"""

CPP_ENHANCED_CONTRIBUTIONS = CATALOG.declare(
    "cpp_enhanced_contributions", Decimal, non_negative=True
)
"""Enhanced CPP contributions, Schedule 8 Part 3b line 48 "Line 43 plus line 47 Enter this amount
(in dollars and cents) on line 22215 of your return.": the first and second additional
contributions together, the T1 line 22215 deduction from total income (not a credit).

When line 24 is positive, Part 3a line 28 "Line 26 plus line 27 Enter this amount (in dollars and
cents) on line 22215 of your return." carries the same sum.
"""

DEDUCTIONS_FROM_TOTAL_INCOME = CATALOG.declare(
    "deductions_from_total_income", Decimal, non_negative=True
)
"""Total deductions, T1 line 23300 "Add lines 35 to 52": the sum of the deductions from total
income, here, in line order, the RRSP deduction (line 20800), union dues (line 21200), the child
care expenses (line 21400) and the enhanced CPP contributions (line 22215)."""

NET_INCOME = CATALOG.declare("net_income", Decimal, non_negative=True)
"""Net income, T1 line 23600 "Line 54 minus line 55 (if negative, enter "0") Net income": total
income less total deductions, not below zero.

Line 54 (23400) is "Line 34 minus line 53 (if negative, show in brackets) Net income before
adjustments"; line 55 (23500, social benefits repayment) is not modelled.
"""

CANADIAN_ARMED_FORCES_AND_POLICE_DEDUCTION = CATALOG.declare(
    "canadian_armed_forces_and_police_deduction", Decimal, non_negative=True
)
"""Canadian Armed Forces personnel and police deduction, T1 line 58 and line 24400 "Canadian Armed
Forces personnel and police deduction (box 43 of all T4 slips)": a starting amount."""

SECURITY_OPTIONS_DEDUCTIONS = CATALOG.declare(
    "security_options_deductions", Decimal, non_negative=True
)
"""Security options deductions, T1 line 59 and line 24900 "Security options deductions (boxes 39,
41, 91 and 92 of all T4 slips or see Form T1212)": a starting amount."""

UCCB_REPAYMENT = CATALOG.declare("uccb_repayment", Decimal, non_negative=True)
"""UCCB repayment, Federal Worksheet "Line 25000 - Other payments deduction" line 6 "Amount from
line 21300 of your return": a starting amount, as line 21300 is not wired yet."""

RDSP_INCOME_REPAYMENT = CATALOG.declare("rdsp_income_repayment", Decimal, non_negative=True)
"""RDSP income repayment, Federal Worksheet "Line 25000 - Other payments deduction" line 7 "RDSP
income repayment (included in the amount on line 23200 of your return)": a starting amount."""

UCCB_AND_RDSP_INCOME = CATALOG.declare("uccb_and_rdsp_income", Decimal, non_negative=True)
"""UCCB and RDSP income, Federal Worksheet "Line 25000 - Other payments deduction" line 4 "Line 2
plus line 3 =": the amount from line 11700 of the return (line 2) and the amount from line 12500
(line 3)."""

NET_INCOME_LESS_UCCB_AND_RDSP_INCOME = CATALOG.declare(
    "net_income_less_uccb_and_rdsp_income", Decimal
)
"""Net income less the UCCB and RDSP income, Federal Worksheet "Line 25000 - Other payments
deduction" line 5 "Line 1 minus line 4 =": the net income (line 1, "Amount from line 23400 of your
return (if negative, enter "0")") less line 4.

The form prints no "(if negative, enter "0")" on line 5, so the kind is signed.
"""

UCCB_AND_RDSP_INCOME_REPAYMENTS = CATALOG.declare(
    "uccb_and_rdsp_income_repayments", Decimal, non_negative=True
)
"""UCCB and RDSP income repayments, Federal Worksheet "Line 25000 - Other payments deduction" line
8 "Line 6 plus line 7 =": the UCCB repayment (line 6) and the RDSP income repayment (line 7)."""

OTHER_PAYMENTS_LIMIT_INCOME = CATALOG.declare("other_payments_limit_income", Decimal)
"""Income for the limit, Federal Worksheet "Line 25000 - Other payments deduction" line 9 "Line 5
plus line 8 =": the amount the worksheet compares with $93,454 ("If the amount on line 9 is more
than $93,454, go to canada.ca/line-25000 to find out how much you can deduct.").

The form prints no "(if negative, enter "0")" on line 9, so the kind is signed. The count of line 9
over $93,454 is a starting count, so nothing consumes this line and the manifest returns it.
"""

OTHER_PAYMENTS_WORKSHEET_LINE_9_OVER_LIMIT = CATALOG.declare(
    "other_payments_worksheet_line_9_over_limit", int, non_negative=True
)
"""Line 9 over the limit, Federal Worksheet "Line 25000 - Other payments deduction" "If the amount
on line 9 is more than $93,454, go to canada.ca/line-25000 to find out how much you can deduct.":
a starting count, 1 when line 9 is more than $93,454 and 0 otherwise, until a comparison
capability derives it."""

OTHER_PAYMENTS_DEDUCTION_ABOVE_LIMIT = CATALOG.declare(
    "other_payments_deduction_above_limit", Decimal, non_negative=True
)
"""Other payments deduction above the limit, Federal Worksheet "Line 25000 - Other payments
deduction" "go to canada.ca/line-25000 to find out how much you can deduct": the amount that
chart gives when line 9 is more than $93,454, a starting amount."""

OTHER_PAYMENTS_DEDUCTION_AFTER_LIMIT = CATALOG.declare(
    "other_payments_deduction_after_limit", Decimal, non_negative=True
)
"""Other payments deduction after the limit, Federal Worksheet "Line 25000 - Other payments
deduction" "Otherwise, enter the amount from line 14700 of your return on line 25000 of your
return.": line 14700 when line 9 is not more than $93,454, else the amount the canada.ca/line-25000
chart gives."""

OTHER_PAYMENTS_WORKSHEET_REQUIRED = CATALOG.declare(
    "other_payments_worksheet_required", int, non_negative=True
)
"""Worksheet required, T1 line 60 and line 25000 "Other payments deduction (enter the amount from
line 14700 if you did not enter an amount on line 14600; otherwise, use Federal Worksheet)": a
starting count, 1 when an amount was entered on line 14600 and 0 otherwise, until a comparison
capability derives it."""

OTHER_PAYMENTS_DEDUCTION = CATALOG.declare("other_payments_deduction", Decimal, non_negative=True)
"""Other payments deduction, T1 line 60 and line 25000 "Other payments deduction (enter the amount
from line 14700 if you did not enter an amount on line 14600; otherwise, use Federal Worksheet)":
line 14700 when no amount was entered on line 14600, else the Federal Worksheet's result."""

LIMITED_PARTNERSHIP_LOSSES_OF_OTHER_YEARS = CATALOG.declare(
    "limited_partnership_losses_of_other_years", Decimal, non_negative=True
)
"""Limited partnership losses of other years, T1 line 61 and line 25100 "Limited partnership losses
of other years": the amount the filer chooses to claim, a starting amount."""

NON_CAPITAL_LOSSES_OF_OTHER_YEARS = CATALOG.declare(
    "non_capital_losses_of_other_years", Decimal, non_negative=True
)
"""Non-capital losses of other years, T1 line 62 and line 25200 "Non-capital losses of other
years": the amount the filer chooses to claim, a starting amount."""

ADDITIONAL_DEDUCTIONS = CATALOG.declare("additional_deductions", Decimal, non_negative=True)
"""Additional deductions, T1 line 67 and line 25600 "Additional deductions": a starting amount."""

DEDUCTIONS_FROM_NET_INCOME = CATALOG.declare(
    "deductions_from_net_income", Decimal, non_negative=True
)
"""Deductions from net income, T1 line 68 and line 25700 "Add lines 58 to 67.": the sum of the
deductions from net income, here, in line order, lines 58, 59, 60, 61, 62 and 67 (lines 24400,
24900, 25000, 25100, 25200 and 25600); lines 63 to 66 (25300, 25395, 25400 and 25500) are not
wired yet.
"""

TAXABLE_INCOME = CATALOG.declare("taxable_income", Decimal, non_negative=True)
"""Taxable income, T1 line 69 "Line 57 minus line 68 (if negative, enter "0") Taxable income"
(line 26000, as Step 5 refers to it): net income less the deductions from net income, not below
zero; the base the federal and Ontario brackets apply to.

Line 57 is "Enter the amount from line 56 of the previous page" (net income); line 68 (25700) is
"Add lines 58 to 67".
"""

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

INFIRM_CHILDREN = CATALOG.declare("infirm_children", int, non_negative=True)
"""Number of infirm children, T1 line 83 "Number of children you are claiming this amount for Line
30499": a starting count."""

INFIRM_CHILDREN_AMOUNT = CATALOG.declare("infirm_children_amount", Decimal, non_negative=True)
"""Canada caregiver amount for infirm children, T1 line 83 (line 30500) "Canada caregiver amount
for infirm children under 18 years of age (see Schedule 5) Number of children you are claiming
this amount for Line 30499" "multiplied by $2,687", a part of the total of the credit amounts on
the T1 alone (the ON428 caregiver amount, line 58185, is not triggered)."""

CPP_BASE_CONTRIBUTIONS = CATALOG.declare("cpp_base_contributions", Decimal, non_negative=True)
"""Base CPP contributions, Schedule 8 Part 3 line 11 "amount from line 7 multiplied by 4.95%
(maximum $3,356.10)": the required contributions on the employment income between the basic
exemption and the maximum pensionable earnings, a part of the total of the credit amounts on the
T1 and, as ON428 line 19 (line 58240) "Amount from line 30800 of your return", on ON428.

Line 15 is "Amount from line 11"; Part 3b line 30 "If line 16 is positive or "0", enter the amount
from line 15 at line 30 and line 36, and continue at line 37." and line 36 "Line 34 plus line 35.
Enter this amount (in dollars and cents) on line 30800 of your return and line 58240 of your Form
428." carry it to T1 line 30800 and ON428 line 58240, lines 32 and 35 being 0. When line 24 is
positive, Part 3a line 25 "Enter the amount from line 15." carries the same amount.

Line 1 (50339) is "Total CPP pensionable earnings from box 26 of all of your T4 slips (if box 26
is blank, enter the amount from box 14)", so the three contributions read employment income.
Not triggered by the returns modelled: Part 2's proration for fewer than 12 months, box 26
differing from box 14, and the slips' deducted contributions differing from the required ones
(so no overpayment on T1 line 44800).
"""

EI_PREMIUMS = CATALOG.declare("ei_premiums", Decimal, non_negative=True)
"""EI premiums, T1 line 31200 "through employment (boxes 18 and 55 of all T4 slips) (maximum
$1,077.48)": the rate on employment income up to the maximum insurable earnings, a part of the
total of the credit amounts on the T1 and, as ON428 line 21 (line 58300) "Amount from line 31200
of your return", on ON428.

Employment income is taken as the insurable earnings: boxes 18 and 55 of the slip are not
modelled. Not triggered by the returns modelled: the EI overpayment (T1 line 45000).
"""

CANADA_EMPLOYMENT_AMOUNT = CATALOG.declare("canada_employment_amount", Decimal, non_negative=True)
"""Canada employment amount, T1 line 31260 "Enter whichever is less: $1,471 or line 1 plus line
2.": the lesser of the cap and employment income, the fourth part of the total of the credit
amounts on the T1 alone (ON428 has no such line).

Line 1 (10100) is "Employment income (box 14 of all T4 slips)" and line 2 (10400) is "Other
employment income". The returns have no other employment income, so the cap applies to
employment income alone.
"""

NON_REFUNDABLE_CREDIT_AMOUNTS = CATALOG.declare(
    "non_refundable_credit_amounts", Decimal, non_negative=True
)
"""Total of the non-refundable credit amounts, T1 line 33500 "Line 106 plus line 112": the sum
of the credit amounts the rate is applied to once, here, in line order, the basic personal amount
(line 30000), the age amount (line 78, 30100), the spouse or common-law partner amount (line 79,
30300), the amount for an eligible dependant (line 80, 30400), the Canada caregiver amount for a
spouse or common-law partner (line 81, 30425), the Canada caregiver amount for infirm children
(line 83, 30500), the base CPP contributions (line 30800), the EI premiums (line 31200) and the
Canada employment amount (line 31260)."""

CHARITABLE_DONATIONS = CATALOG.declare("charitable_donations", Decimal, non_negative=True)
"""Charitable donations, Schedule 9 line 1 "Donations to registered charities and similar
organizations": the eligible amount on the receipts, with any unused donations of the previous five
years that the filer chooses to claim, a starting amount."""

GOVERNMENT_DONATIONS = CATALOG.declare("government_donations", Decimal, non_negative=True)
"""Government donations, Schedule 9 line 2 (line 32900) "Donations to the Government of Canada, a
province or territory and similar bodies": the eligible amount on the receipts, a starting amount.
"""

UNIVERSITY_DONATIONS_OUTSIDE_CANADA = CATALOG.declare(
    "university_donations_outside_canada", Decimal, non_negative=True
)
"""University donations outside Canada, Schedule 9 line 3 (line 33300) "Donations to registered
universities outside Canada": the eligible amount on the receipts, a starting amount."""

FOREIGN_CHARITY_DONATIONS = CATALOG.declare("foreign_charity_donations", Decimal, non_negative=True)
"""Foreign charity donations, Schedule 9 line 4 (line 33400) "Donations to the United Nations and
its agencies and registered foreign charities": the eligible amount on the receipts, a starting
amount."""

ECOLOGICAL_AND_CULTURAL_GIFTS = CATALOG.declare(
    "ecological_and_cultural_gifts", Decimal, non_negative=True
)
"""Ecological and cultural gifts, Schedule 9 line 11 (line 34200) "Eligible amount of ecological
gifts and cultural gifts (see Guide P113)": a starting amount."""

ECOLOGICAL_GIFTS_BEFORE_2016 = CATALOG.declare(
    "ecological_gifts_before_2016", Decimal, non_negative=True
)
"""Ecological gifts before 2016, Schedule 9 line 15 (line 34210) "Total ecological gifts made after
February 10, 2014, and before 2016 included in the amount on line 11": a starting amount."""

DEPRECIABLE_GIFT_RECAPTURED_DEPRECIATION = CATALOG.declare(
    "depreciable_gift_recaptured_depreciation", Decimal, non_negative=True
)
"""Recaptured depreciation on the depreciable property donated, Schedule 9 chart for line 33700,
line 1 "Amount of recaptured depreciation included on your 2025 return": a starting amount."""

DEPRECIABLE_GIFT_NET_PROCEEDS = CATALOG.declare(
    "depreciable_gift_net_proceeds", Decimal, non_negative=True
)
"""Net proceeds of disposition of the depreciable property donated, Schedule 9 chart for line 33700,
line 2: the net proceeds of disposition of the property donated in 2025, a starting amount for the
one class and property the return claims."""

DEPRECIABLE_GIFT_CAPITAL_COST = CATALOG.declare(
    "depreciable_gift_capital_cost", Decimal, non_negative=True
)
"""Capital cost of the depreciable property donated, Schedule 9 chart for line 33700, line 3: the
capital cost of the property donated in 2025, a starting amount for the one class and property the
return claims."""

CAPITAL_GIFT_TAXABLE_GAINS = CATALOG.declare(
    "capital_gift_taxable_gains", Decimal, non_negative=True
)
"""Taxable capital gains on the capital property donated, Schedule 9 chart for line 33900, line 1
"Amount of current-year taxable capital gains from capital property donated in 2025": a starting
amount."""

CAPITAL_GIFT_GAINS_DEDUCTION = CATALOG.declare(
    "capital_gift_gains_deduction", Decimal, non_negative=True
)
"""Capital gains deduction on the capital property donated, Schedule 9 chart for line 33900, line 2
"Amount of current-year capital gains deduction from capital property donated in 2025": a starting
amount."""

DEPRECIABLE_GIFT_PROCEEDS_OR_COST = CATALOG.declare(
    "depreciable_gift_proceeds_or_cost", Decimal, non_negative=True
)
"""Lesser of the proceeds and the cost of the depreciable property donated, Schedule 9 chart for
line 33700, line 4 "Enter whichever is less: amount from line 2 or line 3.": the lesser of the net
proceeds of disposition and the capital cost."""

DEPRECIABLE_GIFTS = CATALOG.declare("depreciable_gifts", Decimal, non_negative=True)
"""Gifts of capital property that are depreciable property, Schedule 9 line B and line 33700, chart
line 5 "Enter whichever is less: amount from line 1 or line 4. Enter this amount on line 33700 of
the previous page.": the lesser of the recaptured depreciation and line 4."""

CAPITAL_PROPERTY_GIFTS = CATALOG.declare("capital_property_gifts", Decimal, non_negative=True)
"""Gifts of capital property, Schedule 9 line C and line 33900, chart line 3 "Line 1 minus Line 2
Enter this amount on line 33900 on the previous page.": the taxable capital gains less the capital
gains deduction."""

TOTAL_CHARITABLE_DONATIONS = CATALOG.declare(
    "total_charitable_donations", Decimal, non_negative=True
)
"""Total eligible amount of charitable donations, Schedule 9 line 5 "Add lines 1 to 4. Total
eligible amount of charitable donations": the sum of the four kinds of donations."""

DONATION_LIMIT_ON_NET_INCOME = CATALOG.declare(
    "donation_limit_on_net_income", Decimal, non_negative=True
)
"""Donation limit on the net income, Schedule 9 line 6 "Enter your net income from line 23600 of
your return. Line A multiplied by 75%": 75% of the net income."""

CAPITAL_GIFTS_TOTAL = CATALOG.declare("capital_gifts_total", Decimal, non_negative=True)
"""Gifts of capital property, Schedule 9 line 7 "Amount B plus amount C Line D": the gifts of
capital property that are depreciable property (line B) plus the gifts of capital property (line C).
"""

CAPITAL_GIFTS_LIMIT_ADDITION = CATALOG.declare(
    "capital_gifts_limit_addition", Decimal, non_negative=True
)
"""Donation limit addition for gifts of capital property, Schedule 9 line 7 "multiplied by 25%": 25%
of line D."""

DONATION_LIMIT_WITH_CAPITAL_GIFTS = CATALOG.declare(
    "donation_limit_with_capital_gifts", Decimal, non_negative=True
)
"""Donation limit with the gifts of capital property, Schedule 9 line 8 "Line 6 plus line 7": line 6
plus line 7."""

CHARITABLE_DONATIONS_LIMIT = CATALOG.declare(
    "charitable_donations_limit", Decimal, non_negative=True
)
"""Total charitable donations limit, Schedule 9 line 9 "Enter whichever is less: amount A or line 8.
Total charitable donations limit": the lesser of the net income (amount A) and line 8."""

CHARITABLE_DONATIONS_CLAIMED = CATALOG.declare(
    "charitable_donations_claimed", Decimal, non_negative=True
)
"""Charitable donations claimed, Schedule 9 line 10 and line 34000 "Enter whichever is less: amount
from line 5 or line 9.": the lesser of the total eligible amount of charitable donations and the
limit."""

DONATIONS_AND_GIFTS_TOTAL = CATALOG.declare("donations_and_gifts_total", Decimal, non_negative=True)
"""Donations and gifts, Schedule 9 line 12 "Line 10 plus line 11": the charitable donations claimed
plus the ecological and cultural gifts."""

DONATION_FIRST_TIER_MAXIMUM = CATALOG.declare(
    "donation_first_tier_maximum", Decimal, non_negative=True
)
"""Donations first tier maximum, Schedule 9 line 13 "Enter whichever is less: amount from line 12 or
$200.": the $200, claimed whole."""

DONATIONS_FIRST_TIER = CATALOG.declare("donations_first_tier", Decimal, non_negative=True)
"""Donations at the first tier, Schedule 9 line 13 "Enter whichever is less: amount from line 12 or
$200." (line H): the lesser of line 12 and $200."""

DONATIONS_OVER_FIRST_TIER = CATALOG.declare("donations_over_first_tier", Decimal, non_negative=True)
"""Donations over the first tier, Schedule 9 line 14 "Line 12 minus line 13" (amount E): line 12
less line 13."""

DONATIONS_OVER_FIRST_TIER_AFTER_2016_GIFTS = CATALOG.declare(
    "donations_over_first_tier_after_2016_gifts", Decimal, non_negative=True
)
"""Donations over the first tier less the ecological gifts before 2016, Schedule 9 line 16 "Line 14
minus line 15 (if negative, enter "0")": line 14 less line 15, not below zero."""

DONATION_HIGH_INCOME_THRESHOLD = CATALOG.declare(
    "donation_high_income_threshold", Decimal, non_negative=True
)
"""Donations high income threshold, Schedule 9 line 18 "Income threshold 253,414.00": the threshold,
claimed whole."""

TAXABLE_INCOME_OVER_DONATION_THRESHOLD = CATALOG.declare(
    "taxable_income_over_donation_threshold", Decimal, non_negative=True
)
"""Taxable income over the donations threshold, Schedule 9 line 19 "Line 17 minus line 18 (if
negative, enter "0")": the taxable income of line 17 (line 26000) less the threshold, not below
zero."""

HIGH_INCOME_DONATIONS = CATALOG.declare("high_income_donations", Decimal, non_negative=True)
"""Donations at the high income rate, Schedule 9 line 20 "Enter whichever is less: amount from line
16 or line 19. Line F": the lesser of line 16 and line 19."""

HIGH_INCOME_DONATION_CREDIT = CATALOG.declare(
    "high_income_donation_credit", Decimal, non_negative=True
)
"""Donations credit at the high income rate, Schedule 9 line 20 "multiplied by 33%": 33% of line F.
"""

REGULAR_RATE_DONATIONS = CATALOG.declare("regular_rate_donations", Decimal, non_negative=True)
"""Donations at the regular rate, Schedule 9 line 21 "Amount E minus amount F Line G": the donations
over the first tier (amount E) less line F."""

REGULAR_RATE_DONATION_CREDIT = CATALOG.declare(
    "regular_rate_donation_credit", Decimal, non_negative=True
)
"""Donations credit at the regular rate, Schedule 9 line 21 "multiplied by 29%": 29% of line G."""

FIRST_TIER_DONATION_CREDIT = CATALOG.declare(
    "first_tier_donation_credit", Decimal, non_negative=True
)
"""Donations credit at the first tier, Schedule 9 line 22 "Amount from line 13 of the previous page
Line H multiplied by 14.5%": 14.5% of line 13."""

DONATIONS_AND_GIFTS_CREDIT = CATALOG.declare(
    "donations_and_gifts_credit", Decimal, non_negative=True
)
"""Donations and gifts credit, Schedule 9 line 23 "Add lines 20 to 22. Enter this amount on line
34900 of your return. Allowable donations for 2025", T1 line 116 (line 34900) "Donations and gifts
(complete Schedule 9)": lines 20, 21 and 22 added."""

CREDIT_AMOUNTS_AT_CREDIT_RATE = CATALOG.declare(
    "credit_amounts_at_credit_rate", Decimal, non_negative=True
)
"""Federal credit amounts at the credit rate, T1 line 115 (line 33800) "Line 113 multiplied by the
percentage from line 114": the total of the credit amounts times the credit rate, the first of the
three lines that line 35000 adds and line 1 of the top-up tax credit worksheet."""

TOP_UP_CREDITS_BASE = CATALOG.declare("top_up_credits_base", Decimal, non_negative=True)
"""Credits for the top-up tax credit, Federal Worksheet "Line 34990 - Top-up tax credit", line 3
"Line 1 plus line 2": line 1 "Amount from line 33800 of your return" plus line 2 "Amount from line
22 of your Schedule 9"."""

TOP_UP_THRESHOLD = CATALOG.declare("top_up_threshold", Decimal, non_negative=True)
"""Top-up tax credit threshold, Federal Worksheet "Line 34990 - Top-up tax credit", line 4
"8,319.38": the threshold, claimed whole."""

TOP_UP_EXCESS = CATALOG.declare("top_up_excess", Decimal, non_negative=True)
"""Credits over the top-up threshold, Federal Worksheet "Line 34990 - Top-up tax credit", line 5
"Line 3 minus line 4 (if negative, enter "0")": line 3 less line 4, not below zero."""

TOP_UP_TAX_CREDIT = CATALOG.declare("top_up_tax_credit", Decimal, non_negative=True)
"""Top-up tax credit, Federal Worksheet "Line 34990 - Top-up tax credit", line 7 "Line 5 multiplied
by the percentage from line 6 Enter this amount on line 34990 of your return.", T1 line 117 (line
34990) "Top-up tax credit (use Federal Worksheet)": line 5 times the 3.45% of line 6."""

NON_REFUNDABLE_TAX_CREDITS = CATALOG.declare(
    "non_refundable_tax_credits", Decimal, non_negative=True
)
"""Federal non-refundable tax credits, T1 line 118 (line 35000) "Add lines 115 to 117. Total
federal non-refundable tax credits": line 115 (line 33800, the total of the credit amounts times the
credit rate), line 116 (line 34900, the donations and gifts credit) and line 117 (line 34990, the
top-up tax credit), in line order."""

FEDERAL_TAX_AFTER_CREDITS = CATALOG.declare("federal_tax_after_credits", Decimal, non_negative=True)
"""Basic federal tax, T1 line 126 (line 42900) "Line 121 minus line 125 (if negative, enter "0")
Basic federal tax": the federal basic tax less the credits against it, not below zero.

Line 121 (40400) is "Line 119 plus line 120", line 119 "Enter the amount from line 76."; line 125
is "Add lines 122 to 124.", line 122 "Amount from line 35000" and line 123 "Federal dividend tax
credit". Not modelled: line 120 (40424, tax on split income) and line 124 (minimum tax
carryover).
"""

NET_FEDERAL_TAX = CATALOG.declare("net_federal_tax", Decimal, non_negative=True)
"""Net federal tax, T1 line 142 (line 42000) "Add lines 139 to 141. Net federal tax": the federal
tax after credits carried through the lines between, as nothing else on them is modelled.

Line 126 (42900) is "Line 121 minus line 125 (if negative, enter "0") Basic federal tax", line 121
(40400) "Line 119 plus line 120" and line 125 "Add lines 122 to 124.", line 122 being "Amount from
line 35000" and line 123 the federal dividend tax credit: the federal tax after credits. Line 134
(40600) "Line 132 minus line 133 (if negative, enter "0") Federal tax" and line 139 (41700) "Line
134 minus line 138 (if negative, enter "0")" carry it to line 142. Not modelled: line 120 (40424,
tax on split income), line 124 (minimum tax carryover), lines 127 to 133 (foreign surtax, foreign
tax credit, investment tax credit recapture, logging tax credit), lines 135 to 138 (political,
investment and labour-sponsored credits, 41600) and lines 140 (41500, advanced Canada workers
benefit) and 141 (41800, special taxes).
"""

TOTAL_PAYABLE = CATALOG.declare("total_payable", Decimal, non_negative=True)
"""Total payable, T1 line 148 (line 43500) "Add lines 143 to 147. Total payable": the net federal
tax plus the provincial tax, in line order.

Line 143 is "Amount from line 42000"; line 147 (42800) "Provincial or territorial tax (complete
and attach your provincial or territorial Form 428, even if the result is "0")". Not triggered by
the returns modelled: lines 144 (42100), 145 (42120) and 146 (42200).
"""

INCOME_TAX_DEDUCTED = CATALOG.declare("income_tax_deducted", Decimal, non_negative=True)
"""Income tax deducted, T1 line 150 (line 43700) "Total income tax deducted (amounts from all
Canadian slips)": a starting amount."""

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

PROVINCIAL_CREDITS = CATALOG.declare("provincial_credits", Decimal, non_negative=True)
"""Provincial or territorial credits, T1 line 165 and line 47900 "Provincial or territorial credits
(complete Form 479, if it applies)": the Ontario credits, Form ON479 line 21."""

TOTAL_CREDITS = CATALOG.declare("total_credits", Decimal, non_negative=True)
"""Total credits, T1 line 166 (line 48200) "Add lines 150 to 165. Total credits": here line 150
(43700), line 155 (45300) and line 165 (47900), in line order.

Not triggered by the returns modelled, or left to later work: the other lines from 151 to 164
(lines 44000 to 47600, among them 44800 CPP overpayment and 45000 EI overpayment).
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
