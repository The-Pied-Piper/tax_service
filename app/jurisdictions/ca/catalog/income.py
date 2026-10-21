"""The federal catalog: income.

The T1 income lines, total income, the dividend and investment income lines that feed them, and
the short-term rental rows of Form T776 Chart A.
"""

from __future__ import annotations

from decimal import Decimal

from app.domain.record_list import RecordListKind
from app.jurisdictions.ca.catalog.base import CATALOG
from app.jurisdictions.ca.catalog.personal_amounts import (
    CCA_ADDITIONS,
    CCA_AIIP_ADDITIONS,
    CCA_CLAIMED,
    CCA_CLASS_NUMBER,
    CCA_NO_PROPERTY_LEFT,
    CCA_PROCEEDS,
    CCA_RIIP_ADDITIONS,
    CCA_UCC_AT_END,
    CCA_UCC_AT_START,
)

EMPLOYMENT_INCOME = CATALOG.declare("employment_income", Decimal, non_negative=True)
"""Employment income, T1 line 10100: a starting amount that total income sums directly."""

CAPITAL_GAIN = CATALOG.declare("capital_gain", Decimal)
"""Total capital gains or losses, Schedule 3 line 21 and line 19700 "Line 19 plus line 20 Total
capital gains or losses =": line 19 plus the reserves of line 20, worked out from Part 3 and Part 4.
Signed, as the form reports "all negative amounts (losses) using brackets"; line 22 is the same
figure and the inclusion rate applies to it."""

DISPOSITION_PROCEEDS = CATALOG.declare("disposition_proceeds", Decimal, non_negative=True)
"""Proceeds of a disposition, Schedule 3 Part 3 "(Column 2): Proceeds of disposition": a field of
each record of the property lists, not an artifact of its own."""

DISPOSITION_ADJUSTED_COST_BASE = CATALOG.declare(
    "disposition_adjusted_cost_base", Decimal, non_negative=True
)
"""Adjusted cost base of a disposition, Schedule 3 Part 3 "(Column 3): Adjusted cost base": a field
of each record of the property lists, not an artifact of its own."""

DISPOSITION_OUTLAYS = CATALOG.declare("disposition_outlays", Decimal, non_negative=True)
"""Outlays and expenses of a disposition, Schedule 3 Part 3 "(Column 4): Outlays and expenses": a
field of each record of the property lists, not an artifact of its own."""

QSBCS_DISPOSITIONS = RecordListKind.declare(
    CATALOG,
    "qsbcs_dispositions",
    fields=(DISPOSITION_PROCEEDS, DISPOSITION_ADJUSTED_COST_BASE, DISPOSITION_OUTLAYS),
)
"""Qualified small business corporation shares (QSBCS) dispositions, Schedule 3 Part 3 "Qualified
small business corporation shares (QSBCS)" "For each Gain or loss enter as many lines as
necessary.": a starting list with one record for each disposition, holding "(Column 2): Proceeds of
disposition", "(Column 3): Adjusted cost base" and "(Column 4): Outlays and expenses" (column 1 and
the narrative columns feed no line)."""

QSBCS_GAIN_OR_LOSS = CATALOG.declare("qsbcs_gain_or_loss", Decimal)
"""Qualified small business corporation shares (QSBCS) gain or loss, Schedule 3 line 1 and line
10700 "Total gain or loss (add all the amounts under column 5)": the rows' column 5 "Gain or loss
(column 2 minus columns 3 and 4)" added, a loss in brackets."""

QFFP_DISPOSITIONS = RecordListKind.declare(
    CATALOG,
    "qffp_dispositions",
    fields=(DISPOSITION_PROCEEDS, DISPOSITION_ADJUSTED_COST_BASE, DISPOSITION_OUTLAYS),
)
"""Qualified farm or fishing property (QFFP) dispositions, Schedule 3 Part 3 "Qualified farm or
fishing property (QFFP)" "For each Gain or loss enter as many lines as necessary.": a starting list
with one record for each disposition, holding "(Column 2): Proceeds of disposition", "(Column 3):
Adjusted cost base" and "(Column 4): Outlays and expenses" (column 1 and the narrative columns feed
no line)."""

QFFP_GAIN_OR_LOSS = CATALOG.declare("qffp_gain_or_loss", Decimal)
"""Qualified farm or fishing property (QFFP) gain or loss, Schedule 3 line 2 and line 11000 "Total
gain or loss (add all the amounts under column 5)": the rows' column 5 "Gain or loss (column 2 minus
columns 3 and 4)" added, a loss in brackets."""

QFFP_FORECLOSURE_DISPOSITIONS = RecordListKind.declare(
    CATALOG,
    "qffp_foreclosure_dispositions",
    fields=(DISPOSITION_PROCEEDS, DISPOSITION_ADJUSTED_COST_BASE, DISPOSITION_OUTLAYS),
)
"""QFFP: Mortgage foreclosures and conditional sales repossessions dispositions, Schedule 3 Part 3
"QFFP: Mortgage foreclosures and conditional sales repossessions" "For each Gain or loss enter as
many lines as necessary.": a starting list with one record for each disposition, holding "(Column
2): Proceeds of disposition", "(Column 3): Adjusted cost base" and "(Column 4): Outlays and
expenses" (column 1 and the narrative columns feed no line)."""

QFFP_FORECLOSURE_GAIN_OR_LOSS = CATALOG.declare("qffp_foreclosure_gain_or_loss", Decimal)
"""QFFP: Mortgage foreclosures and conditional sales repossessions gain or loss, Schedule 3 line 3
and line 12400 "Total gain or loss (add all the amounts under column 5)": the rows' column 5 "Gain
or loss (column 2 minus columns 3 and 4)" added, a loss in brackets."""

SHARE_DISPOSITIONS = RecordListKind.declare(
    CATALOG,
    "share_dispositions",
    fields=(DISPOSITION_PROCEEDS, DISPOSITION_ADJUSTED_COST_BASE, DISPOSITION_OUTLAYS),
)
"""Publicly traded shares, mutual fund units, deferral of eligible small business corporation shares
and other shares dispositions, Schedule 3 Part 3 "Publicly traded shares, mutual fund units,
deferral of eligible small business corporation shares and other shares" "For each Gain or loss
enter as many lines as necessary.": a starting list with one record for each disposition, holding
"(Column 2): Proceeds of disposition", "(Column 3): Adjusted cost base" and "(Column 4): Outlays and
expenses" (column 1 and the narrative columns feed no line)."""

SHARE_GAIN_OR_LOSS = CATALOG.declare("share_gain_or_loss", Decimal)
"""Publicly traded shares, mutual fund units, deferral of eligible small business corporation shares
and other shares gain or loss, Schedule 3 line 4 and line 13200 "Total gain or loss (add all the
amounts under column 5)": the rows' column 5 "Gain or loss (column 2 minus columns 3 and 4)" added,
a loss in brackets."""

REAL_ESTATE_DISPOSITIONS = RecordListKind.declare(
    CATALOG,
    "real_estate_dispositions",
    fields=(DISPOSITION_PROCEEDS, DISPOSITION_ADJUSTED_COST_BASE, DISPOSITION_OUTLAYS),
)
"""Real estate, depreciable property, and other properties (see parts 1 and 2) dispositions,
Schedule 3 Part 3 "Real estate, depreciable property, and other properties (see parts 1 and 2)" "For
each Gain or loss enter as many lines as necessary.": a starting list with one record for each
disposition, holding "(Column 2): Proceeds of disposition", "(Column 3): Adjusted cost base" and
"(Column 4): Outlays and expenses" (column 1 and the narrative columns feed no line)."""

REAL_ESTATE_GAIN_OR_LOSS = CATALOG.declare("real_estate_gain_or_loss", Decimal)
"""Real estate, depreciable property, and other properties (see parts 1 and 2) gain or loss,
Schedule 3 line 5 and line 13800 "Total gain or loss (add all the amounts under column 5)": the
rows' column 5 "Gain or loss (column 2 minus columns 3 and 4)" added, a loss in brackets."""

BOND_DISPOSITIONS = RecordListKind.declare(
    CATALOG,
    "bond_dispositions",
    fields=(DISPOSITION_PROCEEDS, DISPOSITION_ADJUSTED_COST_BASE, DISPOSITION_OUTLAYS),
)
"""Bonds, debentures, promissory notes, and other similar properties dispositions, Schedule 3 Part 3
"Bonds, debentures, promissory notes, and other similar properties" "For each Gain or loss enter as
many lines as necessary.": a starting list with one record for each disposition, holding "(Column
2): Proceeds of disposition", "(Column 3): Adjusted cost base" and "(Column 4): Outlays and
expenses" (column 1 and the narrative columns feed no line)."""

BOND_GAIN_OR_LOSS = CATALOG.declare("bond_gain_or_loss", Decimal)
"""Bonds, debentures, promissory notes, and other similar properties gain or loss, Schedule 3 line 6
and line 15300 "Total gain or loss (add all the amounts under column 5)": the rows' column 5 "Gain
or loss (column 2 minus columns 3 and 4)" added, a loss in brackets."""

CRYPTO_ASSET_DISPOSITIONS = RecordListKind.declare(
    CATALOG,
    "crypto_asset_dispositions",
    fields=(DISPOSITION_PROCEEDS, DISPOSITION_ADJUSTED_COST_BASE, DISPOSITION_OUTLAYS),
)
"""Crypto-assets dispositions, Schedule 3 Part 3 "Crypto-assets" "For each Gain or loss enter as
many lines as necessary.": a starting list with one record for each disposition, holding "(Column
2): Proceeds of disposition", "(Column 3): Adjusted cost base" and "(Column 4): Outlays and
expenses" (column 1 and the narrative columns feed no line)."""

CRYPTO_ASSET_GAIN_OR_LOSS = CATALOG.declare("crypto_asset_gain_or_loss", Decimal)
"""Crypto-assets gain or loss, Schedule 3 line 7 and line 15301 "Total gain or loss (add all the
amounts under column 5)": the rows' column 5 "Gain or loss (column 2 minus columns 3 and 4)" added,
a loss in brackets."""

OTHER_FORECLOSURE_DISPOSITIONS = RecordListKind.declare(
    CATALOG,
    "other_foreclosure_dispositions",
    fields=(DISPOSITION_PROCEEDS, DISPOSITION_ADJUSTED_COST_BASE, DISPOSITION_OUTLAYS),
)
"""Other mortgage foreclosures and conditional sales repossessions dispositions, Schedule 3 Part 3
"Other mortgage foreclosures and conditional sales repossessions" "For each Gain or loss enter as
many lines as necessary.": a starting list with one record for each disposition, holding "(Column
2): Proceeds of disposition", "(Column 3): Adjusted cost base" and "(Column 4): Outlays and
expenses" (column 1 and the narrative columns feed no line)."""

OTHER_FORECLOSURE_GAIN_OR_LOSS = CATALOG.declare("other_foreclosure_gain_or_loss", Decimal)
"""Other mortgage foreclosures and conditional sales repossessions gain or loss, Schedule 3 line 8
and line 15500 "Total gain (or loss) (add all the amounts under column 5)": the rows' column 5 "Gain
or loss (column 2 minus columns 3 and 4)" added, a loss in brackets."""

PERSONAL_USE_PROPERTY_DISPOSITIONS = RecordListKind.declare(
    CATALOG,
    "personal_use_property_dispositions",
    fields=(DISPOSITION_PROCEEDS, DISPOSITION_ADJUSTED_COST_BASE, DISPOSITION_OUTLAYS),
)
"""Personal-use property dispositions, Schedule 3 Part 3 "Personal-use property (see parts 1 and 2)"
"(provide a full description)": a starting list with one record for each disposition, holding
"(Column 2): Proceeds of disposition", "(Column 3): Adjusted cost base" and "(Column 4): Outlays and
expenses". The principal residence rows come from Form T2091(IND), not from this list."""

PERSONAL_USE_PROPERTY_GAIN_ROWS = CATALOG.declare(
    "personal_use_property_gain_rows", Decimal, non_negative=True
)
"""Gain on the personal-use property rows, Schedule 3 "Line 9 and line 15800: Total gain only (add
all the amounts under column 5)": the rows' column 5 added, a row with a loss counting 0. A part of
line 9."""

PERSONAL_USE_PROPERTY_GAIN = CATALOG.declare(
    "personal_use_property_gain", Decimal, non_negative=True
)
"""Personal-use property gain, Schedule 3 "Line 9 and line 15800: Total gain only (add all the
amounts under column 5)": the sum of its parts, today only the rows listed on the form."""

LISTED_PERSONAL_PROPERTY_DISPOSITIONS = RecordListKind.declare(
    CATALOG,
    "listed_personal_property_dispositions",
    fields=(DISPOSITION_PROCEEDS, DISPOSITION_ADJUSTED_COST_BASE, DISPOSITION_OUTLAYS),
)
"""Listed personal property dispositions, Schedule 3 Part 3 "Listed personal property (LPP) (LPP
losses can only be applied against LPP gains)" "(provide a full description)": a starting list with
one record for each disposition, holding "(Column 2): Proceeds of disposition", "(Column 3):
Adjusted cost base" and "(Column 4): Outlays and expenses"."""

LISTED_PERSONAL_PROPERTY_GAIN_OR_LOSS = CATALOG.declare(
    "listed_personal_property_gain_or_loss", Decimal
)
"""Listed personal property gain or loss, Schedule 3 Part 3 "Listed personal property (LPP) (LPP
losses can only be applied against LPP gains)": the rows' column 5 "Gain or loss (column 2 minus
columns 3 and 4)" added, a loss in brackets, before "Subtract: unapplied LPP losses from other
years"."""

UNAPPLIED_LISTED_PERSONAL_PROPERTY_LOSSES = CATALOG.declare(
    "unapplied_listed_personal_property_losses", Decimal, non_negative=True
)
"""Unapplied listed personal property losses, Schedule 3 Part 3 "Subtract: unapplied LPP losses from
other years": a starting amount."""

LISTED_PERSONAL_PROPERTY_NET_GAIN = CATALOG.declare(
    "listed_personal_property_net_gain", Decimal, non_negative=True
)
"""Listed personal property net gain, Schedule 3 "Line 10 and line 15900: Net gain only": the rows'
gain or loss less the unapplied LPP losses from other years, not below 0."""

CAPITAL_GAINS_OF_QUALIFIED_AND_OTHER_PROPERTIES = CATALOG.declare(
    "capital_gains_of_qualified_and_other_properties", Decimal
)
"""Total gains or losses of qualified properties and other properties, Schedule 3 "Line 11: Add
lines 1 to 10. Total gains or losses of qualified properties and other properties =", also Part 4
"Line 12: Amount from line 11 of the previous page"."""

CAPITAL_GAINS_DEFERRAL = CATALOG.declare("capital_gains_deferral", Decimal, non_negative=True)
"""Capital gains deferral, Schedule 3 "Line 13 and line 16100: Capital gains deferral from
qualifying dispositions of eligible small business corporation shares included on line 4": a
starting amount."""

CAPITAL_GAINS_AFTER_DEFERRAL = CATALOG.declare("capital_gains_after_deferral", Decimal)
"""Gains or losses after the deferral, Schedule 3 "Line 14: Line 12 minus line 13 =", a loss in
brackets."""

SLIP_CAPITAL_GAINS_OR_LOSSES = CATALOG.declare("slip_capital_gains_or_losses", Decimal)
"""Capital gains or losses from slips, Schedule 3 "Line 15 and line 17400: Capital gains or losses
from your T5, T5013, and T4PS slips": a starting amount, a loss in brackets."""

T3_CAPITAL_GAINS_OR_LOSSES = CATALOG.declare("t3_capital_gains_or_losses", Decimal)
"""Capital gains or losses from T3 slips, Schedule 3 "Line 16 and line 17600: Capital gains or
losses from your T3 slips": a starting amount, a loss in brackets."""

CAPITAL_GAINS_BEFORE_INVESTMENT_LOSS_REDUCTION = CATALOG.declare(
    "capital_gains_before_investment_loss_reduction", Decimal
)
"""Gains or losses before the business investment loss reduction, Schedule 3 "Line 17: Add lines 14
to 16. =", a loss in brackets."""

CAPITAL_GAINS_BEFORE_RESERVES = CATALOG.declare("capital_gains_before_reserves", Decimal)
"""Gains or losses before reserves, Schedule 3 "Line 19 and line 19100: Total gains or losses before
reserves: line 17 minus line 18 =", a loss in brackets."""

CAPITAL_GAINS_RESERVES = CATALOG.declare("capital_gains_reserves", Decimal)
"""Reserves, Schedule 3 "Line 20 and line 19200: Reserves to be included in (or deducted from)
income from Form T2017": a starting amount, a deduction in brackets."""

INCLUDED_CAPITAL_GAIN = CATALOG.declare("included_capital_gain", Decimal)
"""Included capital gain, Schedule 3 "Line 24: Line 22 multiplied by the percentage from line 23
=", a net capital loss in brackets."""

PARTNERSHIP_GAINS_AT_FULL_INCLUSION = CATALOG.declare(
    "partnership_gains_at_full_inclusion", Decimal, non_negative=True
)
"""Partnership gains at full inclusion, Schedule 3 line 25 "Line 25 and line 19890: Capital gains
from certain dispositions of an interest in a partnership subject to 100% inclusion rate (if
negative, enter "0")": a starting amount, added to the included capital gain (line 24)."""

TAXABLE_CAPITAL_GAINS = CATALOG.declare("taxable_capital_gains", Decimal, non_negative=True)
"""Taxable capital gains, T1 line 12700: Schedule 3 line 26 "If positive, enter the result on line
12700 of your return", line 24 plus line 25, or 0 when that is negative (a net capital loss)."""

TOTAL_INCOME = CATALOG.declare("total_income", Decimal)
"""Total income, T1 line 15000 "Line 28 plus line 32 Total income": the sum of the income lines
wired so far, in line order, with the taxable dividends (line 12000), the taxable capital gains
and the taxable support payments. Not floored, so a loss larger than the other income is shown in
brackets as the form prints it (T1 line 33 prints no floor; the General Guide says "If you have a
loss, show it on the applicable line using brackets").

Not wired yet: rental income (line 13) and the net self-employment income (line 27), which is
computed but not yet part of line 28 or line 15000.
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

BUSINESS_INCOME = CATALOG.declare("business_income", Decimal)
"""Business income, T1 line 22 "Business income", line 13500 "Net": the net business income, a
starting amount. Negative when the expenses are larger (a loss), as the form prints no floor."""

PROFESSIONAL_INCOME = CATALOG.declare("professional_income", Decimal)
"""Professional income, T1 line 23 "Professional income", line 13700 "Net": the net professional
income, a starting amount. Negative when the expenses are larger (a loss), as the form prints no
floor."""

COMMISSION_INCOME = CATALOG.declare("commission_income", Decimal)
"""Commission income, T1 line 24 "Commission income", line 13900 "Net": the net commission income,
a starting amount. Negative when the expenses are larger (a loss), as the form prints no floor."""

FARMING_INCOME = CATALOG.declare("farming_income", Decimal)
"""Farming income, T1 line 25 "Farming income", line 14100 "Net": the net farming income, a
starting amount. Negative when the expenses are larger (a loss), as the form prints no floor."""

FISHING_INCOME = CATALOG.declare("fishing_income", Decimal)
"""Fishing income, T1 line 26 "Fishing income", line 14300 "Net": the net fishing income, a
starting amount. Negative when the expenses are larger (a loss), as the form prints no floor."""

NET_SELF_EMPLOYMENT_INCOME = CATALOG.declare("net_self_employment_income", Decimal)
"""Net self-employment income, T1 line 27 "Add lines 22 to 26. Net self-employment income": the net
business, professional, commission, farming and fishing income, in line order. Negative when the
losses exceed the income, as the form prints no floor.

Not yet part of line 28 "Line 21 plus line 27", of total income (line 15000) or of the working
income of Schedule 6, which still read the other income lines alone. Schedule 8 and Schedule 13
read it.
"""

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

SHORT_TERM_RENTAL_RELATED_CCA = CATALOG.declare(
    "short_term_rental_related_cca", Decimal, non_negative=True
)
"""Related CCA of a short-term rental, Form T776 Chart B, column 4 "Related portion of the
available CCA from column 21 in Area A": a field of each record of the short-term rental CCA
units, not an artifact of its own."""

SHORT_TERM_RENTAL_CCA_UNITS = RecordListKind.declare(
    CATALOG,
    "short_term_rental_cca_units",
    fields=(
        CCA_CLASS_NUMBER,
        SHORT_TERM_RENTAL_RELATED_CCA,
        SHORT_TERM_RENTAL_NON_COMPLIANT_DAYS,
        SHORT_TERM_RENTAL_DAYS,
    ),
)
"""Short-term rental CCA units, Form T776 Chart B "Enter each short-term rental or mixed rental
property on a separate row": a starting list with one record for each row, holding column 1 "Class
number", column 4 "Related portion of the available CCA from column 21 in Area A", column 5
"Number of days the residential property was a non-compliant short-term rental" and column 6
"Number of days the residential property was a short-term rental" (columns 2 and 3, the address
and the unit number, are labels the engine does not use)."""

NON_COMPLIANT_CCA = CATALOG.declare("non_compliant_cca", Decimal, non_negative=True)
"""Non-compliant amount of CCA of a class, Form T776 Area A "Column 22: Non-compliant amount of CCA
(see Chart B below)": a field of each record of the non-compliant CCA by class, not an artifact of
its own."""

SHORT_TERM_RENTAL_NON_COMPLIANT_CCA_BY_CLASS = RecordListKind.declare(
    CATALOG,
    "short_term_rental_non_compliant_cca_by_class",
    fields=(CCA_CLASS_NUMBER, NON_COMPLIANT_CCA),
)
"""Non-compliant CCA by class, Form T776 Chart B "*** For each class, add the amounts from column 7
of Chart B and enter each total in column 22 of Area A, in the respective row.": one record for
each class of the short-term rental CCA units, holding its class number and column 22."""


RENTAL_PROPERTY_UNITS = CATALOG.declare("rental_property_units", int, non_negative=True)
"""Number of units of a rental property, Form T776 Part 3 "Number of units": a field of each
record of the rental properties, not an artifact of its own."""

RENTAL_PROPERTY_SHORT_TERM_RENTS = CATALOG.declare(
    "rental_property_short_term_rents", Decimal, non_negative=True
)
"""Gross rents for short-term rentals of a rental property, Form T776 Part 3 "Gross rents for
short-term rentals": a field of each record of the rental properties, not an artifact of its
own."""

RENTAL_PROPERTY_GROSS_RENTS = CATALOG.declare(
    "rental_property_gross_rents", Decimal, non_negative=True
)
"""Gross rents for all units of a rental property, Form T776 Part 3 "Gross rents for all units": a
field of each record of the rental properties, not an artifact of its own."""

RENTAL_PROPERTIES = RecordListKind.declare(
    CATALOG,
    "rental_properties",
    fields=(
        RENTAL_PROPERTY_UNITS,
        RENTAL_PROPERTY_SHORT_TERM_RENTS,
        RENTAL_PROPERTY_GROSS_RENTS,
    ),
)
"""Rental properties, Form T776 Part 3 "List the addresses of your rental properties." with the
columns "Number of units", "Gross rents for short-term rentals" and "Gross rents for all units": a
starting list with one record for each property, holding those three columns (the address is a
label the engine does not use)."""

SHORT_TERM_RENTAL_GROSS_RENTS = CATALOG.declare(
    "short_term_rental_gross_rents", Decimal, non_negative=True
)
"""Total gross rents for short-term rentals, Form T776 line 8140 "Total of your gross rents for
short-term rentals in the year you receive them (add amounts under "Gross rents for short-term
rentals")": the column of the rental properties, added."""

RENTAL_GROSS_RENTS = CATALOG.declare("rental_gross_rents", Decimal, non_negative=True)
"""Total of all gross rents, Form T776 line 8141 "Total of all your gross rents in the year you
receive them (add lines under "Gross rents for all units")": the column of the rental
properties, added."""

RENTAL_OTHER_INCOME = CATALOG.declare("rental_other_income", Decimal, non_negative=True)
"""Other rental income, Form T776 line 8230 "Other income (for example, premiums and leases,
sharecropping)": a starting amount."""

GROSS_RENTAL_INCOME = CATALOG.declare("gross_rental_income", Decimal, non_negative=True)
"""Gross rental income, Form T776 line 8299 "Total gross rental income: Enter this amount on your
income tax and benefit return on line 12599 (line 8141 plus line 8230)", T1 line 13 and line
12599 "Gross": line 8141 plus line 8230."""

RENTAL_ADVERTISING = CATALOG.declare("rental_advertising", Decimal, non_negative=True)
"""Rental advertising, Form T776 line 8521 "Advertising", "Total expenses": a starting amount."""

RENTAL_ADVERTISING_PERSONAL_PORTION = CATALOG.declare(
    "rental_advertising_personal_portion", Decimal, non_negative=True
)
"""Personal portion of the rental advertising, Form T776 line 8521 "Advertising", "Personal
portion of total expenses": a starting amount."""

RENTAL_ADVERTISING_SHORT_TERM_PORTION = CATALOG.declare(
    "rental_advertising_short_term_portion", Decimal, non_negative=True
)
"""Short-term rental portion of the rental advertising, Form T776 line 8521 "Advertising",
"Short-term rental portion of total expenses": a starting amount."""

RENTAL_INSURANCE = CATALOG.declare("rental_insurance", Decimal, non_negative=True)
"""Rental insurance, Form T776 line 8690 "Insurance", "Total expenses": a starting amount."""

RENTAL_INSURANCE_PERSONAL_PORTION = CATALOG.declare(
    "rental_insurance_personal_portion", Decimal, non_negative=True
)
"""Personal portion of the rental insurance, Form T776 line 8690 "Insurance", "Personal portion of
total expenses": a starting amount."""

RENTAL_INSURANCE_SHORT_TERM_PORTION = CATALOG.declare(
    "rental_insurance_short_term_portion", Decimal, non_negative=True
)
"""Short-term rental portion of the rental insurance, Form T776 line 8690 "Insurance", "Short-term
rental portion of total expenses": a starting amount."""

RENTAL_INTEREST_AND_BANK_CHARGES = CATALOG.declare(
    "rental_interest_and_bank_charges", Decimal, non_negative=True
)
"""Rental interest and bank charges, Form T776 line 8710 "Interest and bank charges", "Total
expenses": a starting amount."""

RENTAL_INTEREST_AND_BANK_CHARGES_PERSONAL_PORTION = CATALOG.declare(
    "rental_interest_and_bank_charges_personal_portion", Decimal, non_negative=True
)
"""Personal portion of the rental interest and bank charges, Form T776 line 8710 "Interest and
bank charges", "Personal portion of total expenses": a starting amount."""

RENTAL_INTEREST_AND_BANK_CHARGES_SHORT_TERM_PORTION = CATALOG.declare(
    "rental_interest_and_bank_charges_short_term_portion", Decimal, non_negative=True
)
"""Short-term rental portion of the rental interest and bank charges, Form T776 line 8710
"Interest and bank charges", "Short-term rental portion of total expenses": a starting amount."""

RENTAL_OFFICE_EXPENSES = CATALOG.declare("rental_office_expenses", Decimal, non_negative=True)
"""Rental office expenses, Form T776 line 8810 "Office expenses", "Total expenses": a starting
amount."""

RENTAL_OFFICE_EXPENSES_PERSONAL_PORTION = CATALOG.declare(
    "rental_office_expenses_personal_portion", Decimal, non_negative=True
)
"""Personal portion of the rental office expenses, Form T776 line 8810 "Office expenses",
"Personal portion of total expenses": a starting amount."""

RENTAL_OFFICE_EXPENSES_SHORT_TERM_PORTION = CATALOG.declare(
    "rental_office_expenses_short_term_portion", Decimal, non_negative=True
)
"""Short-term rental portion of the rental office expenses, Form T776 line 8810 "Office expenses",
"Short-term rental portion of total expenses": a starting amount."""

RENTAL_PROFESSIONAL_FEES = CATALOG.declare("rental_professional_fees", Decimal, non_negative=True)
"""Rental professional fees, Form T776 line 8860 "Professional fees (including legal and
accounting fees)", "Total expenses": a starting amount."""

RENTAL_PROFESSIONAL_FEES_PERSONAL_PORTION = CATALOG.declare(
    "rental_professional_fees_personal_portion", Decimal, non_negative=True
)
"""Personal portion of the rental professional fees, Form T776 line 8860 "Professional fees
(including legal and accounting fees)", "Personal portion of total expenses": a starting
amount."""

RENTAL_PROFESSIONAL_FEES_SHORT_TERM_PORTION = CATALOG.declare(
    "rental_professional_fees_short_term_portion", Decimal, non_negative=True
)
"""Short-term rental portion of the rental professional fees, Form T776 line 8860 "Professional
fees (including legal and accounting fees)", "Short-term rental portion of total expenses": a
starting amount."""

RENTAL_MANAGEMENT_AND_ADMINISTRATION_FEES = CATALOG.declare(
    "rental_management_and_administration_fees", Decimal, non_negative=True
)
"""Rental management and administration fees, Form T776 line 8871 "Management and administration
fees", "Total expenses": a starting amount."""

RENTAL_MANAGEMENT_AND_ADMINISTRATION_FEES_PERSONAL_PORTION = CATALOG.declare(
    "rental_management_and_administration_fees_personal_portion", Decimal, non_negative=True
)
"""Personal portion of the rental management and administration fees, Form T776 line 8871
"Management and administration fees", "Personal portion of total expenses": a starting amount."""

RENTAL_MANAGEMENT_AND_ADMINISTRATION_FEES_SHORT_TERM_PORTION = CATALOG.declare(
    "rental_management_and_administration_fees_short_term_portion", Decimal, non_negative=True
)
"""Short-term rental portion of the rental management and administration fees, Form T776 line 8871
"Management and administration fees", "Short-term rental portion of total expenses": a starting
amount."""

RENTAL_REPAIRS_AND_MAINTENANCE = CATALOG.declare(
    "rental_repairs_and_maintenance", Decimal, non_negative=True
)
"""Rental repairs and maintenance, Form T776 line 8960 "Repairs and maintenance", "Total
expenses": a starting amount."""

RENTAL_REPAIRS_AND_MAINTENANCE_PERSONAL_PORTION = CATALOG.declare(
    "rental_repairs_and_maintenance_personal_portion", Decimal, non_negative=True
)
"""Personal portion of the rental repairs and maintenance, Form T776 line 8960 "Repairs and
maintenance", "Personal portion of total expenses": a starting amount."""

RENTAL_REPAIRS_AND_MAINTENANCE_SHORT_TERM_PORTION = CATALOG.declare(
    "rental_repairs_and_maintenance_short_term_portion", Decimal, non_negative=True
)
"""Short-term rental portion of the rental repairs and maintenance, Form T776 line 8960 "Repairs
and maintenance", "Short-term rental portion of total expenses": a starting amount."""

RENTAL_SALARIES_WAGES_AND_BENEFITS = CATALOG.declare(
    "rental_salaries_wages_and_benefits", Decimal, non_negative=True
)
"""Rental salaries, wages and benefits, Form T776 line 9060 "Salaries, wages and benefits
(including employer's contributions)", "Total expenses": a starting amount."""

RENTAL_SALARIES_WAGES_AND_BENEFITS_PERSONAL_PORTION = CATALOG.declare(
    "rental_salaries_wages_and_benefits_personal_portion", Decimal, non_negative=True
)
"""Personal portion of the rental salaries, wages and benefits, Form T776 line 9060 "Salaries,
wages and benefits (including employer's contributions)", "Personal portion of total expenses":
a starting amount."""

RENTAL_SALARIES_WAGES_AND_BENEFITS_SHORT_TERM_PORTION = CATALOG.declare(
    "rental_salaries_wages_and_benefits_short_term_portion", Decimal, non_negative=True
)
"""Short-term rental portion of the rental salaries, wages and benefits, Form T776 line 9060
"Salaries, wages and benefits (including employer's contributions)", "Short-term rental portion
of total expenses": a starting amount."""

RENTAL_PROPERTY_TAXES = CATALOG.declare("rental_property_taxes", Decimal, non_negative=True)
"""Rental property taxes, Form T776 line 9180 "Property taxes", "Total expenses": a starting
amount."""

RENTAL_PROPERTY_TAXES_PERSONAL_PORTION = CATALOG.declare(
    "rental_property_taxes_personal_portion", Decimal, non_negative=True
)
"""Personal portion of the rental property taxes, Form T776 line 9180 "Property taxes", "Personal
portion of total expenses": a starting amount."""

RENTAL_PROPERTY_TAXES_SHORT_TERM_PORTION = CATALOG.declare(
    "rental_property_taxes_short_term_portion", Decimal, non_negative=True
)
"""Short-term rental portion of the rental property taxes, Form T776 line 9180 "Property taxes",
"Short-term rental portion of total expenses": a starting amount."""

RENTAL_TRAVEL = CATALOG.declare("rental_travel", Decimal, non_negative=True)
"""Rental travel, Form T776 line 9200 "Travel", "Total expenses": a starting amount."""

RENTAL_TRAVEL_PERSONAL_PORTION = CATALOG.declare(
    "rental_travel_personal_portion", Decimal, non_negative=True
)
"""Personal portion of the rental travel, Form T776 line 9200 "Travel", "Personal portion of total
expenses": a starting amount."""

RENTAL_TRAVEL_SHORT_TERM_PORTION = CATALOG.declare(
    "rental_travel_short_term_portion", Decimal, non_negative=True
)
"""Short-term rental portion of the rental travel, Form T776 line 9200 "Travel", "Short-term
rental portion of total expenses": a starting amount."""

RENTAL_UTILITIES = CATALOG.declare("rental_utilities", Decimal, non_negative=True)
"""Rental utilities, Form T776 line 9220 "Utilities", "Total expenses": a starting amount."""

RENTAL_UTILITIES_PERSONAL_PORTION = CATALOG.declare(
    "rental_utilities_personal_portion", Decimal, non_negative=True
)
"""Personal portion of the rental utilities, Form T776 line 9220 "Utilities", "Personal portion of
total expenses": a starting amount."""

RENTAL_UTILITIES_SHORT_TERM_PORTION = CATALOG.declare(
    "rental_utilities_short_term_portion", Decimal, non_negative=True
)
"""Short-term rental portion of the rental utilities, Form T776 line 9220 "Utilities", "Short-term
rental portion of total expenses": a starting amount."""

RENTAL_MOTOR_VEHICLE_EXPENSES = CATALOG.declare(
    "rental_motor_vehicle_expenses", Decimal, non_negative=True
)
"""Rental motor vehicle expenses, Form T776 line 9281 "Motor vehicle expenses (not including
capital cost allowance)", "Total expenses": a starting amount."""

RENTAL_MOTOR_VEHICLE_EXPENSES_PERSONAL_PORTION = CATALOG.declare(
    "rental_motor_vehicle_expenses_personal_portion", Decimal, non_negative=True
)
"""Personal portion of the rental motor vehicle expenses, Form T776 line 9281 "Motor vehicle
expenses (not including capital cost allowance)", "Personal portion of total expenses": a
starting amount."""

RENTAL_MOTOR_VEHICLE_EXPENSES_SHORT_TERM_PORTION = CATALOG.declare(
    "rental_motor_vehicle_expenses_short_term_portion", Decimal, non_negative=True
)
"""Short-term rental portion of the rental motor vehicle expenses, Form T776 line 9281 "Motor
vehicle expenses (not including capital cost allowance)", "Short-term rental portion of total
expenses": a starting amount."""

RENTAL_OTHER_EXPENSES = CATALOG.declare("rental_other_expenses", Decimal, non_negative=True)
"""Rental other expenses, Form T776 line 9270 "Other expenses", "Total expenses": a starting
amount."""

RENTAL_OTHER_EXPENSES_PERSONAL_PORTION = CATALOG.declare(
    "rental_other_expenses_personal_portion", Decimal, non_negative=True
)
"""Personal portion of the rental other expenses, Form T776 line 9270 "Other expenses", "Personal
portion of total expenses": a starting amount."""

RENTAL_OTHER_EXPENSES_SHORT_TERM_PORTION = CATALOG.declare(
    "rental_other_expenses_short_term_portion", Decimal, non_negative=True
)
"""Short-term rental portion of the rental other expenses, Form T776 line 9270 "Other expenses",
"Short-term rental portion of total expenses": a starting amount."""

RENTAL_TOTAL_EXPENSES = CATALOG.declare("rental_total_expenses", Decimal, non_negative=True)
"""Total rental expenses, Form T776 line A "Total expenses (add amounts listed under "Total
expenses")": the 13 expense lines (8521 to 9270), in line order."""

RENTAL_PERSONAL_PORTION = CATALOG.declare("rental_personal_portion", Decimal, non_negative=True)
"""Personal portion of the rental expenses, Form T776 line 9949 "Total for personal portion (add
amounts listed under "Personal portion of total expenses")": the 13 expense lines, in line
order."""

RENTAL_SHORT_TERM_PORTION = CATALOG.declare("rental_short_term_portion", Decimal, non_negative=True)
"""Short-term rental portion of the rental expenses, Form T776 line 9365 "Total for short-term
rental portion (add amounts listed under "Short-term rental portion of total expenses")": the
13 expense lines, in line order."""

RENTAL_NON_COMPLIANT_EXPENSES = CATALOG.declare(
    "rental_non_compliant_expenses", Decimal, non_negative=True
)
"""Non-compliant amount of the short-term rental expenses, Form T776 line 9366 "Non-compliant
amount for short-term rentals (amount B from Chart A)": Chart A line B, the total of column 6
over the short-term rental units."""

RENTAL_NON_COMPLIANT_CCA = CATALOG.declare("rental_non_compliant_cca", Decimal, non_negative=True)
"""Non-compliant amount of the short-term rental CCA, Form T776 Chart B "Line C: Total
non-compliant amount of CCA for short-term rentals: Total of column 7 (enter on line 9367 of Part
4)": the total of column 7 over the short-term rental CCA units."""

RENTAL_EXPENSES_LESS_PERSONAL_PORTION = CATALOG.declare(
    "rental_expenses_less_personal_portion", Decimal, non_negative=True
)
"""Rental expenses less the personal portion, the first step of Form T776 line 1 "Deductible
expenses (amount A minus line 9949 minus line 9366)": amount A minus line 9949, which the form
prints as one line with no figure of its own."""

RENTAL_DEDUCTIBLE_EXPENSES = CATALOG.declare(
    "rental_deductible_expenses", Decimal, non_negative=True
)
"""Deductible rental expenses, Form T776 line 1 "Deductible expenses (amount A minus line 9949
minus line 9366)": amount A minus line 9949, less line 9366."""

RENTAL_NET_INCOME_BEFORE_ADJUSTMENTS = CATALOG.declare(
    "rental_net_income_before_adjustments", Decimal
)
"""Rental net income (loss) before adjustments, Form T776 line 9369 "Net income (loss) before
adjustments (total gross rental income from line 8299 minus deductible expenses from amount
1)": signed, a loss is negative."""

RENTAL_COOWNER = CATALOG.declare("rental_coowner", int, non_negative=True)
"""Whether the filer is a co-owner of the rental, Form T776 line 2 "Co-owners: calculate your
share of net income from line 9369. Enter your result on amount 2": 1 for a co-owner, 0 for a
sole proprietor or a partner, a starting count."""

RENTAL_COOWNER_SHARE = CATALOG.declare("rental_coowner_share", Decimal)
"""Co-owner's share of the rental net income, Form T776 line 2 "Co-owners: calculate your share of
net income from line 9369. Enter your result on amount 2": a starting amount, signed."""

RENTAL_NET_INCOME_SHARE = CATALOG.declare("rental_net_income_share", Decimal)
"""Rental net income share, Form T776 amount 2 "Co-owners: calculate your share of net income from
line 9369. Enter your result on amount 2": the co-owner's share (line 2, as entered) when the
filer is a co-owner; otherwise line 9369, which is how this wiring reads a sole proprietor's
amount 2 (the form prints no instruction for one)."""

RENTAL_COOWNER_OTHER_EXPENSES = CATALOG.declare(
    "rental_coowner_other_expenses", Decimal, non_negative=True
)
"""Other expenses of the rental co-owner, Form T776 line 9945 "Other expenses of the co-owner:
other deductible expenses you have as a co-owner which you did not deduct elsewhere": a
starting amount."""

RENTAL_NET_INCOME_AFTER_COOWNER_EXPENSES = CATALOG.declare(
    "rental_net_income_after_coowner_expenses", Decimal
)
"""Rental subtotal after the co-owner's other expenses, Form T776 line 3 "Subtotal (amount 2 minus
line 9945)": signed."""

RENTAL_RECAPTURED_CCA = CATALOG.declare("rental_recaptured_cca", Decimal, non_negative=True)
"""Recaptured capital cost allowance on the rental, Form T776 line 9947 "Recaptured capital cost
allowance (co-owners: enter your share of the amount)": a starting amount, as entered."""

RENTAL_NET_INCOME_WITH_RECAPTURE = CATALOG.declare("rental_net_income_with_recapture", Decimal)
"""Rental subtotal with recaptured capital cost allowance, Form T776 line 4 "Subtotal (amount 3
plus line 9947)": signed."""

RENTAL_TERMINAL_LOSS = CATALOG.declare("rental_terminal_loss", Decimal, non_negative=True)
"""Terminal loss on the rental, Form T776 line 9948 "Terminal loss (co-owners: enter your share of
the amount)": a starting amount, as entered."""

RENTAL_NET_INCOME_AFTER_TERMINAL_LOSS = CATALOG.declare(
    "rental_net_income_after_terminal_loss", Decimal
)
"""Rental subtotal after the terminal loss, Form T776 line 5 "Subtotal (amount 4 minus line
9948)": signed."""

RENTAL_CCA_CLAIM = CATALOG.declare("rental_cca_claim", Decimal, non_negative=True)
"""Capital cost allowance claimed on the rental, Form T776 line 9936 "Total CCA claim for the year
(amount ii from Area A minus any personal part of CCA, and any CCA for business-use-of home
expenses)": a starting amount, as entered."""

RENTAL_NET_INCOME_AFTER_CCA = CATALOG.declare("rental_net_income_after_cca", Decimal)
"""Rental net income (loss) of a sole proprietor or a co-owner, Form T776 line 6 "Net income
(loss) (amount 5 minus line 9936)": signed, a loss is negative."""

RENTAL_PARTNER = CATALOG.declare("rental_partner", int, non_negative=True)
"""Whether the filer is a partner in the rental, Form T776 line 7 "Partners: your share of amount
6, or the amount from your T5013 slip, Statement of Partnership Income": 1 for a partner, 0
otherwise, a starting count."""

RENTAL_PARTNER_SHARE = CATALOG.declare("rental_partner_share", Decimal)
"""Partner's share of the rental net income, Form T776 line 7 "Partners: your share of amount 6,
or the amount from your T5013 slip, Statement of Partnership Income": a starting amount,
signed."""

RENTAL_PARTNER_GST_HST_REBATE = CATALOG.declare(
    "rental_partner_gst_hst_rebate", Decimal, non_negative=True
)
"""GST/HST rebate of the rental partner, Form T776 line 9974 "Partners: GST/HST rebate for
partners received in the year": a starting amount."""

RENTAL_PARTNER_OTHER_EXPENSES = CATALOG.declare(
    "rental_partner_other_expenses", Decimal, non_negative=True
)
"""Other expenses of the rental partner, Form T776 line 9943 "Partners: other expenses of the
partner": a starting amount."""

RENTAL_PARTNER_SHARE_WITH_REBATE = CATALOG.declare("rental_partner_share_with_rebate", Decimal)
"""Rental partner's share with the GST/HST rebate, the first step of Form T776 line 9946 "For
partnerships, enter the result from amount 7 plus line 9974 minus line 9943": amount 7 plus
line 9974."""

RENTAL_PARTNERSHIP_NET_INCOME = CATALOG.declare("rental_partnership_net_income", Decimal)
"""Rental net income (loss) of a partner, Form T776 line 9946 "For partnerships, enter the result
from amount 7 plus line 9974 minus line 9943": amount 7 plus line 9974, less line 9943, signed."""

NET_RENTAL_INCOME = CATALOG.declare("net_rental_income", Decimal)
"""Net rental income, Form T776 line 9946 "Your net income (loss): For sole proprietors or
co-owners, enter the result from amount 6. For partnerships, enter the result from amount 7
plus line 9974 minus line 9943. Enter this amount on line 12600 of your income tax and benefit
return", T1 line 13 and line 12600 "Net": amount 6, or for a partner the partnership figure;
signed, a loss is negative."""

RENTAL_CCA_CLASSES = RecordListKind.declare(
    CATALOG,
    "rental_cca_classes",
    fields=(
        CCA_CLASS_NUMBER,
        CCA_UCC_AT_START,
        CCA_ADDITIONS,
        CCA_PROCEEDS,
        CCA_AIIP_ADDITIONS,
        CCA_RIIP_ADDITIONS,
        CCA_CLAIMED,
        CCA_NO_PROPERTY_LEFT,
    ),
)
"""Rental classes, Form T776 Area A "Calculation of capital cost allowance (CCA) claim": a
starting list with one record for each class, holding the columns the filer enters (class
number, UCC at the start of the year, additions, proceeds, the AIIP and RIIP parts of the
additions, the CCA claimed) and whether any property is left in the class."""

RENTAL_CLOSING_UCC = RecordListKind.declare(
    CATALOG, "rental_closing_ucc", fields=(CCA_CLASS_NUMBER, CCA_UCC_AT_END)
)
"""Rental closing UCC, Form T776 Area A "Column 24: UCC at the end of the year (column 7 minus
column 23)": one record for each class of the rental classes, holding its class number and
column 24."""

RENTAL_CCA_TABLE_RECAPTURE = CATALOG.declare(
    "rental_cca_table_recapture", Decimal, non_negative=True
)
"""Recapture of the rental classes, Form T776 Area A Note 3 "If you have a negative amount in
column 7, add it to income as a recapture under "Recaptured capital cost allowance" on line
9947": the recapture of each class, totalled."""

RENTAL_CCA_TABLE_TERMINAL_LOSS = CATALOG.declare(
    "rental_cca_table_terminal_loss", Decimal, non_negative=True
)
"""Terminal loss of the rental classes, Form T776 Area A Note 3 "If no property is left in the
class and there is a positive amount in this column, deduct the amount from your income as a
terminal loss under "Terminal loss" on line 9948": the terminal loss of each class, totalled."""

RENTAL_CCA_TABLE_CLAIM = CATALOG.declare("rental_cca_table_claim", Decimal, non_negative=True)
"""Total CCA claim of the rental classes, Form T776 Area A "Line ii: Total CCA claim for the year
*: Total of column 23": the CCA claimed on each class, at most its maximum, totalled."""

RENTAL_COOWNER_RECAPTURED_CCA = CATALOG.declare(
    "rental_coowner_recaptured_cca", Decimal, non_negative=True
)
"""Co-owner's share of the recapture, Form T776 line 9947 "Recaptured capital cost allowance
(co-owners: enter your share of the amount)": a starting amount, used for a co-owner."""

RENTAL_COOWNER_TERMINAL_LOSS = CATALOG.declare(
    "rental_coowner_terminal_loss", Decimal, non_negative=True
)
"""Co-owner's share of the terminal loss, Form T776 line 9948 "Terminal loss (co-owners: enter
your share of the amount)": a starting amount, used for a co-owner."""

RENTAL_COOWNER_CCA_CLAIM = CATALOG.declare("rental_coowner_cca_claim", Decimal, non_negative=True)
"""Co-owner's share of the CCA claim, Form T776 Area A "Co-owners: Enter only your share of the
total CCA claim for the year from amount ii on line 9936": a starting amount, used for a
co-owner."""

RENTAL_CCA_CLAIM_SHARE = CATALOG.declare("rental_cca_claim_share", Decimal, non_negative=True)
"""Rental CCA claim before deductions, Form T776 Area A amount ii: the co-owner's share for a
co-owner, otherwise the total CCA claim of the rental classes."""

RENTAL_CCA_PERSONAL_PART = CATALOG.declare("rental_cca_personal_part", Decimal, non_negative=True)
"""Personal part of the rental CCA, Form T776 line 9936 "amount ii from Area A minus any personal
part of CCA": a starting amount."""

RENTAL_CCA_BUSINESS_USE_OF_HOME = CATALOG.declare(
    "rental_cca_business_use_of_home", Decimal, non_negative=True
)
"""CCA for business-use-of-home expenses, Form T776 line 9936 "and any CCA for business-use-of
home expenses": a starting amount."""

RENTAL_CCA_CLAIM_LESS_PERSONAL_PART = CATALOG.declare(
    "rental_cca_claim_less_personal_part", Decimal, non_negative=True
)
"""Rental CCA claim less the personal part, the first step of Form T776 line 9936: amount ii
minus the personal part of CCA."""

RENTAL_CCA_CLAIM_BEFORE_LIMIT = CATALOG.declare(
    "rental_cca_claim_before_limit", Decimal, non_negative=True
)
"""Rental CCA claim before the loss limit, the second step of Form T776 line 9936: the first step
minus the CCA for business-use-of-home expenses."""

RENTAL_CCA_LIMIT = CATALOG.declare("rental_cca_limit", Decimal, non_negative=True)
"""Most the rental CCA claim may be, Guide T4036 "You cannot use CCA to create or increase a
rental loss": Form T776 amount 5, or 0 when amount 5 is negative."""
