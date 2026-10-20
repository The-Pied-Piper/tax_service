"""The federal catalog: the remaining T1 inputs.

The labour-sponsored fund amount, political contributions, disability supports and employment
expense deductions, business income lines, residence and spouse figures.
"""

from __future__ import annotations

from decimal import Decimal

from app.jurisdictions.ca.catalog.base import CATALOG

RL_10_LABOUR_SPONSORED_FUND_AMOUNT = CATALOG.declare(
    "rl_10_labour_sponsored_fund_amount", Decimal, non_negative=True
)
"""Tax Credit for a Labour-Sponsored Fund (Revenu Québec), the guide's "Line 41800 - Special taxes":
"Report, on line 41800 of your return, the result of the following calculation using your RL-10
slip: Tax Credit for a Labour-Sponsored Fund (Revenu Québec)", the tax for not purchasing
replacement shares in a Quebec labour-sponsored fund. The caller's result, as entered: the guide's
text ends the list at "75% of box"."""

POLITICAL_CONTRIBUTIONS = CATALOG.declare("political_contributions", Decimal, non_negative=True)
"""Total federal political contributions, T1 line 135 and line 41000 "Total federal political
contributions (attach receipts) Line 40900": a starting amount, taken as the T1 takes it. The
Federal Worksheet "Line 41000 - Federal political contribution tax credit" line 1 of each column
"Total federal political contributions from line 40900 of your return" reads it.

The worksheet's eligibility text ("contributions that you or your spouse or common-law partner made
in the year to a registered federal political party, a registered association, or a candidate in a
federal election", less any advantage received) is the caller's to apply."""

DISABILITY_SUPPORTS_DEDUCTION = CATALOG.declare(
    "disability_supports_deduction", Decimal, non_negative=True
)
"""Disability supports deduction, T1 line 42 and line 21500 "Disability supports deduction (complete
Form T929)": a starting amount, taken as entered. The Federal Worksheet "Line 45200 - Refundable
medical expense supplement" line 9 "Amount from line 21500 of your return" reads it. Only line 45200
reads it until the deductions from total income compute it; it does not yet enter net income."""

OTHER_EMPLOYMENT_EXPENSES = CATALOG.declare("other_employment_expenses", Decimal, non_negative=True)
"""Other employment expenses, T1 line 50 and line 22900 "Other employment expenses (see Guide
T4044)": a starting amount, taken as entered. The Federal Worksheet "Line 45200 - Refundable medical
expense supplement" takes it off the employment income ("minus the amounts from lines 20700, 21200,
22900, and 23100 of your return"). Only line 45200 reads it until the deductions from total income
compute it; it does not yet enter net income."""

CLERGY_RESIDENCE_DEDUCTION = CATALOG.declare(
    "clergy_residence_deduction", Decimal, non_negative=True
)
"""Clergy residence deduction, T1 line 51 and line 23100 "Clergy residence deduction (complete Form
T1223)": a starting amount, taken as entered. The Federal Worksheet "Line 45200 - Refundable medical
expense supplement" takes it off the employment income, as line 22900. Only line 45200 reads it
until the deductions from total income compute it; it does not yet enter net income."""

NET_BUSINESS_INCOME = CATALOG.declare("net_business_income", Decimal, non_negative=True)
"""Net business income, T1 line 22 and line 13500 "Business income" "Net": a starting amount. The
Federal Worksheet "Line 45200 - Refundable medical expense supplement" counts "your net
self-employment income (not including losses)" and notes that where one line reports a profit from
one business and a loss from another, "use only the profit amounts", and that a loss from only one
business is not included, so the amount is the line's profits only, the caller's to apply. Only line
45200 reads it until the self-employment income is computed; it does not yet enter total income."""

NET_PROFESSIONAL_INCOME = CATALOG.declare("net_professional_income", Decimal, non_negative=True)
"""Net professional income, T1 line 23 and line 13700 "Professional income" "Net": a starting
amount, the profits only as for `net_business_income`, and read only by line 45200 for now."""

NET_COMMISSION_INCOME = CATALOG.declare("net_commission_income", Decimal, non_negative=True)
"""Net commission income, T1 line 24 and line 13900 "Commission income" "Net": a starting amount,
the profits only as for `net_business_income`, and read only by line 45200 for now."""

NET_FARMING_INCOME = CATALOG.declare("net_farming_income", Decimal, non_negative=True)
"""Net farming income, T1 line 25 and line 14100 "Farming income" "Net": a starting amount, the
profits only as for `net_business_income`, and read only by line 45200 for now."""

NET_FISHING_INCOME = CATALOG.declare("net_fishing_income", Decimal, non_negative=True)
"""Net fishing income, T1 line 26 and line 14300 "Fishing income" "Net": a starting amount, the
profits only as for `net_business_income`, and read only by line 45200 for now."""

WAGE_LOSS_REPLACEMENT_PLAN_INCOME = CATALOG.declare(
    "wage_loss_replacement_plan_income", Decimal, non_negative=True
)
"""Wage-loss replacement plan income, Federal Worksheet "Line 45200 - Refundable medical expense
supplement" "your employment income from lines 10100 and 10400 of your return (other than amounts
received from a wage-loss replacement plan)": the amounts received from such a plan that lines 10100
and 10400 include, the caller's, as entered."""

RESIDENT_IN_CANADA_THROUGHOUT_2025 = CATALOG.declare(
    "resident_in_canada_throughout_2025", int, non_negative=True
)
"""Resident in Canada throughout 2025, Federal Worksheet "Line 45200 - Refundable medical expense
supplement" "You were resident in Canada throughout 2025": the caller's count, 1 when it applies and
0 when it does not."""

AGED_18_OR_OLDER_AT_END_OF_2025 = CATALOG.declare(
    "aged_18_or_older_at_end_of_2025", int, non_negative=True
)
"""18 years of age or older at the end of 2025, Federal Worksheet "Line 45200 - Refundable medical
expense supplement" "You were 18 years of age or older at the end of 2025": the caller's count, 1
when it applies and 0 when it does not."""

SPOUSE_NET_INCOME_BEFORE_ADJUSTMENTS = CATALOG.declare(
    "spouse_net_income_before_adjustments", Decimal
)
"""Spouse's net income amount, Federal Worksheet "Line 45200 - Refundable medical expense
supplement" line 1, column 2 "Net income amount from line 23600 of the return (or the amount you
would have entered if the instructions on line 23600 said "if negative, show in brackets")": the
caller's amount for the spouse or common-law partner, signed as the worksheet allows brackets. 0
when there is no spouse or common-law partner, and when "you were separated because of a breakdown
in your relationship for a period of 90 days or more that included December 31, 2025" or "your
spouse or common-law partner died on or before December 31, 2025", as the worksheet says "do not
include their income"."""

SPOUSE_UCCB_REPAYMENT = CATALOG.declare("spouse_uccb_repayment", Decimal, non_negative=True)
"""Spouse's UCCB repayment, Federal Worksheet "Line 45200 - Refundable medical expense supplement"
line 2, column 2 "Total of the universal child care benefit (UCCB) repayment (line 21300 of the
return)": the caller's amount for the spouse or common-law partner, 0 where their income is not
included."""

SPOUSE_RDSP_INCOME_REPAYMENT = CATALOG.declare(
    "spouse_rdsp_income_repayment", Decimal, non_negative=True
)
"""Spouse's RDSP income repayment, Federal Worksheet "Line 45200 - Refundable medical expense
supplement" line 2, column 2 "the registered disability savings plan (RDSP) income repayment
(included in the amount on line 23200 of the return)": the caller's amount for the spouse or
common-law partner, 0 where their income is not included."""

SPOUSE_UNIVERSAL_CHILD_CARE_BENEFIT = CATALOG.declare(
    "spouse_universal_child_care_benefit", Decimal, non_negative=True
)
"""Spouse's UCCB income, Federal Worksheet "Line 45200 - Refundable medical expense supplement" line
4, column 2 "Total of the UCCB income (line 11700 of the return)": the caller's amount for the
spouse or common-law partner, 0 where their income is not included."""

SPOUSE_RDSP_INCOME = CATALOG.declare("spouse_rdsp_income", Decimal, non_negative=True)
"""Spouse's RDSP income, Federal Worksheet "Line 45200 - Refundable medical expense supplement" line
4, column 2 "the RDSP income (line 12500 of the return)": the caller's amount for the spouse or
common-law partner, 0 where their income is not included."""

SPOUSE_OR_COMMON_LAW_PARTNER_ON_DECEMBER_31 = CATALOG.declare(
    "spouse_or_common_law_partner_on_december_31", int, non_negative=True
)
"""Spouse or common-law partner on December 31, 2025, T1 "Marital status on December 31, 2025" Box 1
Married, Box 2 Living common-law: the caller's count, 1 for box 1 or box 2 and 0 for any other."""
