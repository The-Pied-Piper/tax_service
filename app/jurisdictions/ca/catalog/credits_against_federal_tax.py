"""The federal catalog: credits against federal tax.

The political contribution credit, the labour-sponsored funds credit, the countries of the foreign
tax credit and the federal tax less credits.
"""

from __future__ import annotations

from decimal import Decimal

from app.domain.record_list import RecordListKind
from app.jurisdictions.ca.catalog.base import CATALOG

POLITICAL_CREDIT_COLUMN_1_LINE_2 = CATALOG.declare(
    "political_credit_column_1_line_2", Decimal, non_negative=True
)
"""Federal political contribution credit column 1 line 2, Federal Worksheet "Column 1: Line 40900 is
$400 or less", line 2 "0.00": a printed constant."""

POLITICAL_CREDIT_COLUMN_1_LINE_3 = CATALOG.declare(
    "political_credit_column_1_line_3", Decimal, non_negative=True
)
"""Federal political contribution credit column 1 line 3, Federal Worksheet "Column 1: Line 40900 is
$400 or less", line 3 "Line 1 minus line 2 (if negative, enter "0") =": the contributions less line
2, not below zero."""

POLITICAL_CREDIT_COLUMN_1_LINE_5 = CATALOG.declare(
    "political_credit_column_1_line_5", Decimal, non_negative=True
)
"""Federal political contribution credit column 1 line 5, Federal Worksheet "Column 1: Line 40900 is
$400 or less", line 5 "Line 3 multiplied by the percentage from line 4 =": line 3 at the line 4 rate
of 75%."""

POLITICAL_CREDIT_COLUMN_1_LINE_6 = CATALOG.declare(
    "political_credit_column_1_line_6", Decimal, non_negative=True
)
"""Federal political contribution credit column 1 line 6, Federal Worksheet "Column 1: Line 40900 is
$400 or less", line 6 "0.00": a printed constant."""

POLITICAL_CREDIT_COLUMN_1_LINE_7 = CATALOG.declare(
    "political_credit_column_1_line_7", Decimal, non_negative=True
)
"""Federal political contribution credit column 1 line 7, Federal Worksheet "Column 1: Line 40900 is
$400 or less", line 7 "Line 5 plus line 6 Enter this amount on line 41000 of your return. =": line 5
plus line 6."""

POLITICAL_CREDIT_COLUMN_2_LINE_2 = CATALOG.declare(
    "political_credit_column_2_line_2", Decimal, non_negative=True
)
"""Federal political contribution credit column 2 line 2, Federal Worksheet "Column 2: Line 40900 is
more than $400 but not more than $750", line 2 "400.00": a printed constant."""

POLITICAL_CREDIT_COLUMN_2_LINE_3 = CATALOG.declare(
    "political_credit_column_2_line_3", Decimal, non_negative=True
)
"""Federal political contribution credit column 2 line 3, Federal Worksheet "Column 2: Line 40900 is
more than $400 but not more than $750", line 3 "Line 1 minus line 2 (if negative, enter "0") =": the
contributions less line 2, not below zero."""

POLITICAL_CREDIT_COLUMN_2_LINE_5 = CATALOG.declare(
    "political_credit_column_2_line_5", Decimal, non_negative=True
)
"""Federal political contribution credit column 2 line 5, Federal Worksheet "Column 2: Line 40900 is
more than $400 but not more than $750", line 5 "Line 3 multiplied by the percentage from line 4 =":
line 3 at the line 4 rate of 50%."""

POLITICAL_CREDIT_COLUMN_2_LINE_6 = CATALOG.declare(
    "political_credit_column_2_line_6", Decimal, non_negative=True
)
"""Federal political contribution credit column 2 line 6, Federal Worksheet "Column 2: Line 40900 is
more than $400 but not more than $750", line 6 "300.00": a printed constant."""

POLITICAL_CREDIT_COLUMN_2_LINE_7 = CATALOG.declare(
    "political_credit_column_2_line_7", Decimal, non_negative=True
)
"""Federal political contribution credit column 2 line 7, Federal Worksheet "Column 2: Line 40900 is
more than $400 but not more than $750", line 7 "Line 5 plus line 6 Enter this amount on line 41000
of your return. =": line 5 plus line 6."""

POLITICAL_CREDIT_COLUMN_3_LINE_2 = CATALOG.declare(
    "political_credit_column_3_line_2", Decimal, non_negative=True
)
"""Federal political contribution credit column 3 line 2, Federal Worksheet "Column 3: Line 40900 is
more than more than $750", line 2 "750.00": a printed constant."""

POLITICAL_CREDIT_COLUMN_3_LINE_3 = CATALOG.declare(
    "political_credit_column_3_line_3", Decimal, non_negative=True
)
"""Federal political contribution credit column 3 line 3, Federal Worksheet "Column 3: Line 40900 is
more than more than $750", line 3 "Line 1 minus line 2 (if negative, enter "0") =": the
contributions less line 2, not below zero."""

POLITICAL_CREDIT_COLUMN_3_LINE_5 = CATALOG.declare(
    "political_credit_column_3_line_5", Decimal, non_negative=True
)
"""Federal political contribution credit column 3 line 5, Federal Worksheet "Column 3: Line 40900 is
more than more than $750", line 5 "Line 3 multiplied by the percentage from line 4 =": line 3 at the
line 4 rate of 33.33%."""

POLITICAL_CREDIT_COLUMN_3_LINE_6 = CATALOG.declare(
    "political_credit_column_3_line_6", Decimal, non_negative=True
)
"""Federal political contribution credit column 3 line 6, Federal Worksheet "Column 3: Line 40900 is
more than more than $750", line 6 "475.00": a printed constant."""

POLITICAL_CREDIT_COLUMN_3_LINE_7 = CATALOG.declare(
    "political_credit_column_3_line_7", Decimal, non_negative=True
)
"""Federal political contribution credit column 3 line 7, Federal Worksheet "Column 3: Line 40900 is
more than more than $750", line 7 "Line 5 plus line 6 Enter this amount on line 41000 of your
return. =": line 5 plus line 6."""

POLITICAL_CREDIT_CHOSEN_COLUMN = CATALOG.declare(
    "political_credit_chosen_column", Decimal, non_negative=True
)
"""Federal political contribution credit, the column that applies, Federal Worksheet "Line 41000 -
Federal political contribution tax credit": the line 7 of column 1 if line 40900 is $400 or less,
of column 2 if it is more than $400 but not more than $750, of column 3 if it is more than $750."""

POLITICAL_CREDIT_SHORTCUT_THRESHOLD = CATALOG.declare(
    "political_credit_shortcut_threshold", Decimal, non_negative=True
)
"""Federal political contribution credit shortcut threshold, Federal Worksheet "Line 41000 -
Federal political contribution tax credit": "If your total federal political contributions from
line 40900 of your return were" "$1,275 or more, enter $650 on line 41000 of your return.": the
printed $1,275, a constant."""

POLITICAL_CREDIT_SHORTCUT_AMOUNT = CATALOG.declare(
    "political_credit_shortcut_amount", Decimal, non_negative=True
)
"""Federal political contribution credit shortcut amount, Federal Worksheet "Line 41000 - Federal
political contribution tax credit": "$1,275 or more, enter $650 on line 41000 of your return.": the
printed $650, a constant."""

POLITICAL_CREDIT_BEFORE_MAXIMUM = CATALOG.declare(
    "political_credit_before_maximum", Decimal, non_negative=True
)
"""Federal political contribution credit before its maximum, Federal Worksheet "Line 41000 -
Federal political contribution tax credit": the printed $650 when line 40900 is $1,275 or more,
otherwise the line 7 of the column that applies."""

POLITICAL_CREDIT = CATALOG.declare("political_credit", Decimal, non_negative=True)
"""Federal political contribution tax credit, T1 line 135 and line 41000 "Total federal political
contributions (attach receipts) Line 40900 (maximum $650)": the worksheet's result, at most
$650."""

LABOUR_SPONSORED_FUNDS_NET_COST = CATALOG.declare(
    "labour_sponsored_funds_net_cost", Decimal, non_negative=True
)
"""Net cost of shares of a provincially registered fund, T1 line 137, line 41300 "Net cost of shares
of a provincially registered fund": the caller's net cost, as entered."""

LABOUR_SPONSORED_FUNDS_CREDIT_BEFORE_MAXIMUM = CATALOG.declare(
    "labour_sponsored_funds_credit_before_maximum", Decimal, non_negative=True
)
"""Labour-sponsored funds credit before the maximum, T1 line 137 (line 41400): the guide's "equal to
15% of the net cost reported on line 41300 of your return", before its "to a maximum of $750"."""

LABOUR_SPONSORED_FUNDS_CREDIT = CATALOG.declare(
    "labour_sponsored_funds_credit", Decimal, non_negative=True
)
"""Labour-sponsored funds tax credit, T1 line 137 and line 41400 "Labour-sponsored funds tax credit
Line 41300: Net cost of shares of a provincially registered fund Line 41300: Allowable credit": the
guide's "allowable credit on line 41400 of your return that is equal to 15% of the net cost
reported on line 41300 of your return, to a maximum of $750."."""

CREDITS_AGAINST_FEDERAL_TAX = CATALOG.declare(
    "credits_against_federal_tax", Decimal, non_negative=True
)
"""Credits against federal tax, T1 line 138 (line 41600) "Add lines 135 to 137.": here line 135
(`political_credit`, 41000) and line 137 (`labour_sponsored_funds_credit`), in line order, as line
136 (41200) is not wired."""

FEDERAL_TAX_LESS_CREDITS = CATALOG.declare("federal_tax_less_credits", Decimal, non_negative=True)
"""Federal tax less credits, T1 line 139 (line 41700) "Line 134 minus line 138 (if negative, enter
"0")": line 134 (40600) "Line 132 minus line 133 (if negative, enter "0") Federal tax", here line
132 (`federal_tax_with_itc_recapture`) as line 133 is not wired, less line 138, not below zero."""

FEDERAL_TAX_LINE_41700 = CATALOG.declare("federal_tax_line_41700", Decimal, non_negative=True)
"""Federal tax, T1 line 139 and line 41700 "Line 134 minus line 138 (if negative, enter "0")", or,
when Part 5 line 11 of Form T691 is positive, Part 6 line 14 "Enter this amount on line 41700 of
your return.": the figure entered on line 41700, the federal tax less credits when the count of
"line 11 is positive" is 0, else the Part 6 line 14 amount, never below zero."""

FOREIGN_NON_BUSINESS_TAX_PAID = CATALOG.declare(
    "foreign_non_business_tax_paid", Decimal, non_negative=True
)
"""Non-business income tax paid to a foreign country, Form T2209 line 1 "Non-business income tax
paid to a foreign country (1) 43100": the total of the non-business income or profits tax paid to
that country for the year, minus the part deductible under subsection 20(11) or deducted under
subsection 20(12) of the ITA, as the caller enters it; a field of each record of the foreign tax
countries, not an artifact of its own."""

NET_FOREIGN_NON_BUSINESS_INCOME = CATALOG.declare(
    "net_foreign_non_business_income", Decimal, non_negative=True
)
"""Net foreign non-business income, Form T2209 line 2 "Net foreign non-business income (2) 43300":
the net income from that country; a field of each record of the foreign tax countries, not an
artifact of its own."""

FOREIGN_TAX_COUNTRIES = RecordListKind.declare(
    CATALOG,
    "foreign_tax_countries",
    fields=(FOREIGN_NON_BUSINESS_TAX_PAID, NET_FOREIGN_NON_BUSINESS_INCOME),
)
"""Foreign tax countries, Form T2209 "do the applicable calculation shown on this form for
non-business and business taxes paid to each country on a separate sheet": a starting list with one
record for each country, holding line 1 (43100) and line 2 (43300). The list may be empty."""

FOREIGN_TAX_CREDIT_SHEET_LINE_3 = CATALOG.declare(
    "foreign_tax_credit_sheet_line_3", Decimal, non_negative=True
)
"""Federal non-business foreign tax credit of a sheet, Form T2209 line 3 "Enter whichever is less:
the amount from line 1 or line 2.": the lesser of the tax paid and the rounded line 2 of that sheet;
a field of each record of the foreign tax credit sheets, not an artifact of its own."""

FOREIGN_TAX_CREDIT_SHEETS = RecordListKind.declare(
    CATALOG,
    "foreign_tax_credit_sheets",
    fields=(
        FOREIGN_NON_BUSINESS_TAX_PAID,
        NET_FOREIGN_NON_BUSINESS_INCOME,
        FOREIGN_TAX_CREDIT_SHEET_LINE_3,
    ),
)
"""Foreign tax credit sheets, Form T2209 "on a separate sheet": one record for each sheet worked, in
order, holding line 1 (43100), the net foreign income used on line 2 (43300, after the cap at net
income) and line 3. The list may be empty."""

ITC_APPRENTICE_SALARY_AND_WAGES = CATALOG.declare(
    "itc_apprentice_salary_and_wages", Decimal, non_negative=True
)
"""Apprentice's eligible salary and wages, Form T2038(IND) Part B Table 1 "The lesser of eligible
salary and wages** payable in the year or $20,000.": each apprentice's eligible salary and wages
payable in the year, net of any assistance; a field of each record of the apprentices, not an
artifact of its own."""

ITC_APPRENTICES = RecordListKind.declare(
    CATALOG, "itc_apprentices", fields=(ITC_APPRENTICE_SALARY_AND_WAGES,)
)
"""Apprentices, Form T2038(IND) Part B Table 1 "Calculation of total Apprenticeship job creation tax
credit": a starting list with one record for each apprentice, holding the eligible salary and wages
(column 3). The list may be empty."""

ITC_APPRENTICESHIP_WAGES_TOTAL = CATALOG.declare(
    "itc_apprenticeship_wages_total", Decimal, non_negative=True
)
"""Apprenticeship wages total, Form T2038(IND) Part B Table 1 "Total apprenticeship job creation tax
credit (Total of amounts in column 3 plus applicable amount from box 40* of your T3 slip)": the
total of the column 3 amounts, before the 10% and before the box 40 amount, which are not part of
this figure."""
