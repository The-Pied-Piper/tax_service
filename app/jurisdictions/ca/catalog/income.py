"""The federal catalog: income.

The T1 income lines, total income, the dividend and investment income lines that feed them, and
the short-term rental rows of Form T776 Chart A.
"""

from __future__ import annotations

from decimal import Decimal

from app.domain.record_list import RecordListKind
from app.jurisdictions.ca.catalog.base import CATALOG

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

TOTAL_INCOME = CATALOG.declare("total_income", Decimal)
"""Total income, T1 line 15000 "Line 28 plus line 32 Total income": the sum of the income lines
wired so far, in line order, with the taxable dividends (line 12000), the taxable capital gains
and the taxable support payments. Not floored, so a loss larger than the other income is shown in
brackets as the form prints it (T1 line 33 prints no floor; the General Guide says "If you have a
loss, show it on the applicable line using brackets").

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
