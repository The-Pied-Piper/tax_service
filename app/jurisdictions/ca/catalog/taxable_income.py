"""The federal catalog: losses of other years and taxable income.

The non-capital and net capital losses of other years, the deductions from net income, taxable
income and the federal basic tax.
"""

from __future__ import annotations

from decimal import Decimal

from app.jurisdictions.ca.catalog.base import CATALOG

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

UNAPPLIED_NET_CAPITAL_LOSSES_1985_TO_1987 = CATALOG.declare(
    "unapplied_net_capital_losses_1985_to_1987", Decimal, non_negative=True
)
"""Unapplied net capital losses, Form T1436 "Line 25300 - Net capital loss of other years (if you
have pre-1986 capital loss balance)", Chart A column (A) "Amount of your unapplied net capital
losses", row "After May 22, 1985, and before 1988": a starting amount."""

UNAPPLIED_NET_CAPITAL_LOSSES_1988_AND_1989 = CATALOG.declare(
    "unapplied_net_capital_losses_1988_and_1989", Decimal, non_negative=True
)
"""Unapplied net capital losses, Form T1436 "Line 25300 - Net capital loss of other years (if you
have pre-1986 capital loss balance)", Chart A column (A) "Amount of your unapplied net capital
losses", row "In 1988 and 1989": a starting amount."""

UNAPPLIED_NET_CAPITAL_LOSSES_1990_TO_1999 = CATALOG.declare(
    "unapplied_net_capital_losses_1990_to_1999", Decimal, non_negative=True
)
"""Unapplied net capital losses, Form T1436 "Line 25300 - Net capital loss of other years (if you
have pre-1986 capital loss balance)", Chart A column (A) "Amount of your unapplied net capital
losses", row "After 1989 and before 2000": a starting amount."""

UNAPPLIED_NET_CAPITAL_LOSSES_2001_TO_2024 = CATALOG.declare(
    "unapplied_net_capital_losses_2001_to_2024", Decimal, non_negative=True
)
"""Unapplied net capital losses, Form T1436 "Line 25300 - Net capital loss of other years (if you
have pre-1986 capital loss balance)", Chart A column (A) "Amount of your unapplied net capital
losses", row "After 2000 and before 2025": a starting amount."""

NET_CAPITAL_LOSSES_CLAIMED = CATALOG.declare(
    "net_capital_losses_claimed", Decimal, non_negative=True
)
"""Net capital losses claimed, Form T1436 line 7 "Enter the amount of losses you want to claim
(3).": the amount the filer chooses to claim, a starting amount, refused when above line 6."""

ADJUSTED_GROSS_CAPITAL_LOSSES_1985_TO_1987 = CATALOG.declare(
    "adjusted_gross_capital_losses_1985_to_1987", Decimal, non_negative=True
)
"""Adjusted gross capital losses, Form T1436 Chart A column (C) "Adjusted gross capital losses
(column A multiplied by column B)", row "After May 22, 1985, and before 1988": column A times the
exact fraction of column B, rounded half-up to the cent, once."""

ADJUSTED_GROSS_CAPITAL_LOSSES_1988_AND_1989 = CATALOG.declare(
    "adjusted_gross_capital_losses_1988_and_1989", Decimal, non_negative=True
)
"""Adjusted gross capital losses, Form T1436 Chart A column (C) "Adjusted gross capital losses
(column A multiplied by column B)", row "In 1988 and 1989": column A times the exact fraction of
column B, rounded half-up to the cent, once."""

ADJUSTED_GROSS_CAPITAL_LOSSES_1990_TO_1999 = CATALOG.declare(
    "adjusted_gross_capital_losses_1990_to_1999", Decimal, non_negative=True
)
"""Adjusted gross capital losses, Form T1436 Chart A column (C) "Adjusted gross capital losses
(column A multiplied by column B)", row "After 1989 and before 2000": column A times the exact
fraction of column B, rounded half-up to the cent, once."""

ADJUSTED_GROSS_CAPITAL_LOSSES_2001_TO_2024 = CATALOG.declare(
    "adjusted_gross_capital_losses_2001_to_2024", Decimal, non_negative=True
)
"""Adjusted gross capital losses, Form T1436 Chart A column (C) "Adjusted gross capital losses
(column A multiplied by column B)", row "After 2000 and before 2025": column A times the exact
fraction of column B, rounded half-up to the cent, once."""

TOTAL_ADJUSTED_NET_CAPITAL_LOSSES = CATALOG.declare(
    "total_adjusted_net_capital_losses", Decimal, non_negative=True
)
"""Total adjusted net capital losses, Form T1436 line 4 "Total of column C from Chart A": the sum of
column C over the rows wired."""

NET_CAPITAL_LOSSES_AVAILABLE_TO_CLAIM = CATALOG.declare(
    "net_capital_losses_available_to_claim", Decimal, non_negative=True
)
"""Net capital losses available to claim, Form T1436 line 6 "Enter whichever is less: amount from
line 4 or line 5.": the lesser of line 4 and line 5, the taxable capital gains (T1 line 12700)."""

NET_CAPITAL_LOSSES_OF_OTHER_YEARS = CATALOG.declare(
    "net_capital_losses_of_other_years", Decimal, non_negative=True
)
"""Net capital losses of other years, T1 line 63 and line 25300 "Net capital losses of other years":
Form T1436 line 7, the amount claimed, at most line 6; with lines 1 to 3 not completed it is also
line 13, the amount applied by column D, and a deduction from net income."""

ADJUSTED_LOSSES_APPLIED_1985_TO_1987 = CATALOG.declare(
    "adjusted_losses_applied_1985_to_1987", Decimal, non_negative=True
)
"""Adjusted losses applied, Form T1436 Chart A column (D) "Total adjusted net capital losses applied
against taxable capital gains in 2025", row "After May 22, 1985, and before 1988": the lesser of
column C and what is left of line 13 after the older rows, as Guide T4037 applies the earlier years
first."""

ADJUSTED_LOSSES_LEFT_AFTER_1985_TO_1987 = CATALOG.declare(
    "adjusted_losses_left_after_1985_to_1987", Decimal, non_negative=True
)
"""Adjusted losses left after the row "After May 22, 1985, and before 1988": what is left of line
13, the amount claimed, once the row's column D is taken off, for the next row's column D."""

REMAINING_ADJUSTED_LOSSES_1985_TO_1987 = CATALOG.declare(
    "remaining_adjusted_losses_1985_to_1987", Decimal, non_negative=True
)
"""Remaining adjusted losses, Form T1436 Chart A column (E) "Remaining adjusted net capital losses
(column C minus column D)", row "After May 22, 1985, and before 1988": column C less column D."""

NET_CAPITAL_LOSS_BALANCE_1985_TO_1987 = CATALOG.declare(
    "net_capital_loss_balance_1985_to_1987", Decimal, non_negative=True
)
"""Net capital loss balance, Form T1436 Chart A column (G) "Net capital loss balance available to
carry forward (column E multiplied by column F)", row "After May 22, 1985, and before 1988": column
E times the exact fraction of column F, rounded half-up to the cent, once; what the return produces
for next year's column A."""

ADJUSTED_LOSSES_APPLIED_1988_AND_1989 = CATALOG.declare(
    "adjusted_losses_applied_1988_and_1989", Decimal, non_negative=True
)
"""Adjusted losses applied, Form T1436 Chart A column (D) "Total adjusted net capital losses applied
against taxable capital gains in 2025", row "In 1988 and 1989": the lesser of column C and what is
left of line 13 after the older rows, as Guide T4037 applies the earlier years first."""

ADJUSTED_LOSSES_LEFT_AFTER_1988_AND_1989 = CATALOG.declare(
    "adjusted_losses_left_after_1988_and_1989", Decimal, non_negative=True
)
"""Adjusted losses left after the row "In 1988 and 1989": what is left of line 13, the amount
claimed, once the row's column D is taken off, for the next row's column D."""

REMAINING_ADJUSTED_LOSSES_1988_AND_1989 = CATALOG.declare(
    "remaining_adjusted_losses_1988_and_1989", Decimal, non_negative=True
)
"""Remaining adjusted losses, Form T1436 Chart A column (E) "Remaining adjusted net capital losses
(column C minus column D)", row "In 1988 and 1989": column C less column D."""

NET_CAPITAL_LOSS_BALANCE_1988_AND_1989 = CATALOG.declare(
    "net_capital_loss_balance_1988_and_1989", Decimal, non_negative=True
)
"""Net capital loss balance, Form T1436 Chart A column (G) "Net capital loss balance available to
carry forward (column E multiplied by column F)", row "In 1988 and 1989": column E times the exact
fraction of column F, rounded half-up to the cent, once; what the return produces for next year's
column A."""

ADJUSTED_LOSSES_APPLIED_1990_TO_1999 = CATALOG.declare(
    "adjusted_losses_applied_1990_to_1999", Decimal, non_negative=True
)
"""Adjusted losses applied, Form T1436 Chart A column (D) "Total adjusted net capital losses applied
against taxable capital gains in 2025", row "After 1989 and before 2000": the lesser of column C and
what is left of line 13 after the older rows, as Guide T4037 applies the earlier years first."""

ADJUSTED_LOSSES_LEFT_AFTER_1990_TO_1999 = CATALOG.declare(
    "adjusted_losses_left_after_1990_to_1999", Decimal, non_negative=True
)
"""Adjusted losses left after the row "After 1989 and before 2000": what is left of line 13, the
amount claimed, once the row's column D is taken off, for the next row's column D."""

REMAINING_ADJUSTED_LOSSES_1990_TO_1999 = CATALOG.declare(
    "remaining_adjusted_losses_1990_to_1999", Decimal, non_negative=True
)
"""Remaining adjusted losses, Form T1436 Chart A column (E) "Remaining adjusted net capital losses
(column C minus column D)", row "After 1989 and before 2000": column C less column D."""

NET_CAPITAL_LOSS_BALANCE_1990_TO_1999 = CATALOG.declare(
    "net_capital_loss_balance_1990_to_1999", Decimal, non_negative=True
)
"""Net capital loss balance, Form T1436 Chart A column (G) "Net capital loss balance available to
carry forward (column E multiplied by column F)", row "After 1989 and before 2000": column E times
the exact fraction of column F, rounded half-up to the cent, once; what the return produces for next
year's column A."""

ADJUSTED_LOSSES_APPLIED_2001_TO_2024 = CATALOG.declare(
    "adjusted_losses_applied_2001_to_2024", Decimal, non_negative=True
)
"""Adjusted losses applied, Form T1436 Chart A column (D) "Total adjusted net capital losses applied
against taxable capital gains in 2025", row "After 2000 and before 2025": the lesser of column C and
what is left of line 13 after the older rows, as Guide T4037 applies the earlier years first."""

REMAINING_ADJUSTED_LOSSES_2001_TO_2024 = CATALOG.declare(
    "remaining_adjusted_losses_2001_to_2024", Decimal, non_negative=True
)
"""Remaining adjusted losses, Form T1436 Chart A column (E) "Remaining adjusted net capital losses
(column C minus column D)", row "After 2000 and before 2025": column C less column D."""

NET_CAPITAL_LOSS_BALANCE_2001_TO_2024 = CATALOG.declare(
    "net_capital_loss_balance_2001_to_2024", Decimal, non_negative=True
)
"""Net capital loss balance, Form T1436 Chart A column (G) "Net capital loss balance available to
carry forward (column E multiplied by column F)", row "After 2000 and before 2025": column E times
the exact fraction of column F, rounded half-up to the cent, once; what the return produces for next
year's column A."""

ADDITIONAL_DEDUCTIONS = CATALOG.declare("additional_deductions", Decimal, non_negative=True)
"""Additional deductions, T1 line 67 and line 25600 "Additional deductions": a starting amount."""

DEDUCTIONS_FROM_NET_INCOME = CATALOG.declare(
    "deductions_from_net_income", Decimal, non_negative=True
)
"""Deductions from net income, T1 line 68 and line 25700 "Add lines 58 to 67.": the sum of the
deductions from net income, here, in line order, lines 58, 59, 60, 61, 62, 63, 66 and 67 (lines
24400, 24900, 25000, 25100, 25200, 25300, 25500 and 25600); lines 64 and 65 (25395 and 25400) are
not wired yet.
"""

TAXABLE_INCOME = CATALOG.declare("taxable_income", Decimal, non_negative=True)
"""Taxable income, T1 line 69 "Line 57 minus line 68 (if negative, enter "0") Taxable income"
(line 26000, as Step 5 refers to it): net income less the deductions from net income, not below
zero; the base the federal and Ontario brackets apply to.

Line 57 is "Enter the amount from line 56 of the previous page" (net income); line 68 (25700) is
"Add lines 58 to 67".
"""

QBT_ELECTION_ELIGIBLE_AMOUNT = CATALOG.declare(
    "qbt_election_eligible_amount", Decimal, non_negative=True
)
"""Total eligible amount for the joint election, Form T2048 line 1 "Total eligible amount for the
joint election (maximum of $10 million per election)": a starting amount; the $10 million
per-election maximum is not enforced here."""

QBT_PERCENTAGE_ALLOCATED = CATALOG.declare("qbt_percentage_allocated", Decimal, non_negative=True)
"""Percentage allocated to you, Form T2048 line 2 "Percentage allocated to you": a starting amount
entered as a percentage (50 means 50%)."""

QBT_AMOUNT_ALLOCATED = CATALOG.declare("qbt_amount_allocated", Decimal, non_negative=True)
"""Amount allocated, Form T2048 line 3 "Line 1 multiplied by the percentage from line 2": line 1
times line 2 divided by 100, rounded half-up to the cent, once."""

QBT_TAXABLE_AMOUNT_ALLOCATED = CATALOG.declare(
    "qbt_taxable_amount_allocated", Decimal, non_negative=True
)
"""Taxable amount allocated, Form T2048 line 5 "Line 3 multiplied by the percentage from line 4":
line 3 multiplied by the inclusion rate on line 4 (50%)."""

QBT_PRIOR_YEARS_CLAIMS = CATALOG.declare("qbt_prior_years_claims", Decimal, non_negative=True)
"""Capital gains deduction claimed in prior years, Form T2048 line 6 "Capital gains deduction
claimed in prior years at line 25395 of your return for this disposition, if any": a starting
amount."""

QBT_DEDUCTION_AVAILABLE = CATALOG.declare("qbt_deduction_available", Decimal, non_negative=True)
"""Capital gains deduction available from your election, Form T2048 line 7 "Capital gains deduction
available from your election: line 5 minus line 6": line 5 minus line 6, floored at zero (the
form prints no floor)."""

QBT_CAPITAL_GAINS = CATALOG.declare("qbt_capital_gains", Decimal, non_negative=True)
"""Capital gains for the QBT or QCC in the current year, Form T2048 line 9 "Capital gains for the
QBT or QCC that occurred in the current year reported on Schedule 3": a starting amount."""

QBT_2024_RESERVE = CATALOG.declare("qbt_2024_reserve", Decimal, non_negative=True)
"""Amount of 2024 reserve, Form T2048 line 10 "Amount of 2024 reserve claimed for the QBT or QCC, if
any": a starting amount."""

QBT_CAPITAL_GAINS_WITH_2024_RESERVE = CATALOG.declare(
    "qbt_capital_gains_with_2024_reserve", Decimal, non_negative=True
)
"""Capital gains with the 2024 reserve, Form T2048 line 11 "Line 9 plus line 10": the sum of line 9
and line 10."""

QBT_2025_RESERVE = CATALOG.declare("qbt_2025_reserve", Decimal, non_negative=True)
"""Amount of 2025 reserve, Form T2048 line 13 "Amount of 2025 reserve claimed for the QBT or QCC, if
any": a starting amount."""

QBT_TOTAL_CAPITAL_GAINS = CATALOG.declare("qbt_total_capital_gains", Decimal, non_negative=True)
"""Total capital gains for the QBT or QCC, Form T2048 line 14 "Total capital gains for the QBT or
QCC: line 12 minus line 13": line 12 minus line 13, floored at zero (the form prints no floor)."""

QBT_TAXABLE_CAPITAL_GAINS = CATALOG.declare("qbt_taxable_capital_gains", Decimal, non_negative=True)
"""Taxable capital gains for the QBT or QCC only, Form T2048 line 16 "Taxable capital gains for the
QBT or QCC only: line 14 multiplied by the inclusion rate on line 15": line 14 multiplied by the
50% inclusion rate, rounded half-up to the cent."""

QBT_TAXABLE_GAINS_LIMIT = CATALOG.declare("qbt_taxable_gains_limit", Decimal, non_negative=True)
"""Taxable gains limit, Form T2048 line 17 "Enter whichever is less: amount from line 8 or line
16.": the lesser of line 8 and line 16."""

QBT_TAXABLE_GAINS_NOT_LIMITED = CATALOG.declare(
    "qbt_taxable_gains_not_limited", Decimal, non_negative=True
)
"""Taxable capital gains not limited by the QBT or QCC, Form T2048 line 21 "Line 19 minus line 20
(if negative enter "0")": line 8 minus line 17, floored at zero; Chart A line 18 is the same
figure."""

QBT_NET_CAPITAL_LOSSES_REMAINING = CATALOG.declare(
    "qbt_net_capital_losses_remaining", Decimal, non_negative=True
)
"""Net capital losses remaining, Form T2048 line 22 "Line 18 minus line 21 (if negative enter "0")":
line 18 minus line 21, floored at zero."""

QBT_HAS_INVESTMENT_EXPENSES = CATALOG.declare("qbt_has_investment_expenses", int, non_negative=True)
"""Has investment expenses in 2025, Form T2048 line 24 "If you have investment expenses in 2025,
complete Chart A on page 4 and enter the amount from line 20 of Chart A. Otherwise, enter "0".":
a starting count, 1 when there are investment expenses in 2025 and 0 otherwise."""

QBT_NET_INVESTMENT_LOSS = CATALOG.declare("qbt_net_investment_loss", Decimal, non_negative=True)
"""Net investment loss for the year, Form T2048 line 24 "Net investment loss for the year": Chart A
line 20 multiplied by the 0 or 1 count of investment expenses in 2025, so 0 when there are none."""

QBT_REDUCTIONS_FROM_LOSSES = CATALOG.declare(
    "qbt_reductions_from_losses", Decimal, non_negative=True
)
"""Reductions from losses, Form T2048 line 25 "Add lines 22, 23, and 24": the sum of lines 22, 23
and 24."""

QBT_DEDUCTION_LIMIT = CATALOG.declare("qbt_deduction_limit", Decimal, non_negative=True)
"""Deduction limit, Form T2048 line 26 "Line 17 minus line 25": line 17 minus line 25, floored at
zero (the form prints no floor)."""

QBT_MAXIMUM_DEDUCTION = CATALOG.declare("qbt_maximum_deduction", Decimal, non_negative=True)
"""Maximum deduction, Form T2048 line 27 "Enter whichever is less: amount from line 7 or line 26.":
the lesser of line 7 and line 26."""

QBT_DEDUCTION_CLAIMED = CATALOG.declare("qbt_deduction_claimed", Decimal, non_negative=True)
"""Deduction claimed, Form T2048 line 27 "Enter all or part of the amount you want to claim on line
25395 of your return": a starting amount, which the claim cannot exceed."""

QBT_CAPITAL_GAINS_DEDUCTION = CATALOG.declare(
    "qbt_capital_gains_deduction", Decimal, non_negative=True
)
"""Eligible capital gains deduction for QBT or QCC, Form T2048 line 27 "Eligible capital gains
deduction for QBT or QCC": the amount claimed, at most the maximum deduction."""

QBT_DEDUCTION_BASE = CATALOG.declare("qbt_deduction_base", Decimal, non_negative=True)
"""Deduction base, Form T2048 line 28 "Enter whichever is less: amount from line 7 or line 17.": the
lesser of line 7 and line 17."""

QBT_REDUCTION_AMOUNT = CATALOG.declare("qbt_reduction_amount", Decimal, non_negative=True)
"""Reduction amount, Form T2048 line 30 "Line 28 minus line 29" "Reduction amount": line 28 minus
line 29."""

QBT_ALLOCATION_TOTAL = CATALOG.declare("qbt_allocation_total", Decimal, non_negative=True)
"""Allocation total, Form T2048 line 32 "Line 30 plus line 31": line 30 plus line 31."""

QBT_ABIL_AND_NET_INVESTMENT_LOSS = CATALOG.declare(
    "qbt_abil_and_net_investment_loss", Decimal, non_negative=True
)
"""ABIL and net investment loss, Form T2048 line 35 "Line 33 plus line 34": line 33 plus line 34."""

QBT_ALLOCATION_LIMIT = CATALOG.declare("qbt_allocation_limit", Decimal, non_negative=True)
"""Allocation limit, Form T2048 line 36 "Enter whichever is less: amount from line 30 or line 35.":
the lesser of line 30 and line 35."""

QBT_ABIL_REDUCTION = CATALOG.declare("qbt_abil_reduction", Decimal, non_negative=True)
"""ABIL reduction, Form T2048 line 41 "Line 39 multiplied by line 40" "ABIL reduction": line 33
times line 36 divided by line 35, rounded half-up to the cent, once; 0 when line 35 is zero."""

QBT_NET_INVESTMENT_LOSS_REDUCTION = CATALOG.declare(
    "qbt_net_investment_loss_reduction", Decimal, non_negative=True
)
"""Net investment loss reduction, Form T2048 line 42 "Line 36 minus line 41" "Net investment loss
reduction": line 36 minus line 41."""

QBT_ELECTION_IS_QBT = CATALOG.declare("qbt_election_is_qbt", int, non_negative=True)
"""Election is for a QBT, Form T2048 Part 5 B "Amount from line 7 if the election is for a QBT": a
starting count, 1 when the election is for a QBT and 0 otherwise."""

QBT_GAINS_ARE_QSBCS_OR_QFFP = CATALOG.declare("qbt_gains_are_qsbcs_or_qffp", int, non_negative=True)
"""Gains are from QSBCS or QFFP, Form T2048 Part 5 E "Amounts from line 31 and 36 if gains are from
a qualified small business corporation shares (QSBCS) or qualified farm or fishing property
(QFFP)": a starting count, 1 when the gains are from QSBCS or QFFP and 0 otherwise."""

QCC_ELECTION_DEDUCTION = CATALOG.declare("qcc_election_deduction", Decimal, non_negative=True)
"""Deduction available from QCC election, Form T2048 Part 5 A "Amount from line 7 if the election is
for a QCC": line 7 minus the QBT election deduction, the part of line 7 that the QBT election
does not take."""

QBT_ELECTION_DEDUCTION = CATALOG.declare("qbt_election_deduction", Decimal, non_negative=True)
"""Deduction available from QBT election, Form T2048 Part 5 B "Amount from line 7 if the election is
for a QBT": line 7 multiplied by the 0 or 1 QBT election count."""

QBT_TAXABLE_GAINS_RELATED_TO_DEDUCTION = CATALOG.declare(
    "qbt_taxable_gains_related_to_deduction", Decimal, non_negative=True
)
"""Taxable gains related to the deduction, Form T2048 Part 5 D "Amount from lines 31 and 36": line
31 plus line 36."""

QSBCS_QFFP_TAXABLE_GAINS_RELATED_TO_DEDUCTION = CATALOG.declare(
    "qsbcs_qffp_taxable_gains_related_to_deduction", Decimal, non_negative=True
)
"""QSBCS or QFFP taxable gains related to the deduction, Form T2048 Part 5 E "Portion of QSBCS or
QFFP taxable capital gains related to a capital gain deduction for QBT or QCC claimed": the Part
5 D amount multiplied by the 0 or 1 QSBCS or QFFP count."""

QBT_NET_RENTAL_INCOME = CATALOG.declare("qbt_net_rental_income", Decimal, non_negative=True)
"""Net rental income, Form T2048 Chart A line 12 "Net rental income, including recaptured capital
cost allowance (line 12600)": the positive part of the net rental income, floored at zero (the
form prints no floor)."""

QBT_NET_RENTAL_LOSS = CATALOG.declare("qbt_net_rental_loss", Decimal, non_negative=True)
"""Net rental losses, Form T2048 Chart A line 2 "Net rental losses (line 12600)": the net rental
loss as a positive amount, zero when the net rental income is positive."""

QBT_PARTNERSHIP_LOSSES = CATALOG.declare("qbt_partnership_losses", Decimal, non_negative=True)
"""Limited or non-active partnership losses, Form T2048 Chart A line 3 "Limited or non-active
partnership losses (line 12200) other than allowable capital losses": a starting amount."""

QBT_EXPLORATION_EXPENSES_AT_HALF = CATALOG.declare(
    "qbt_exploration_expenses_at_half", Decimal, non_negative=True
)
"""Exploration and development expenses at 50%, Form T2048 Chart A line 5 "50% of exploration and
development expenses (line 22400)": 50% of the exploration and development expenses."""

QBT_OTHER_INVESTMENT_EXPENSES = CATALOG.declare(
    "qbt_other_investment_expenses", Decimal, non_negative=True
)
"""Other investment expenses, Form T2048 Chart A line 6 "Any other investment expenses claimed in
2025 to earn property income (see the list of "other investment expenses" on the next page)": a
starting amount."""

QBT_CHART_A_NET_CAPITAL_LOSSES_USED = CATALOG.declare(
    "qbt_chart_a_net_capital_losses_used", Decimal, non_negative=True
)
"""Net capital losses used in Chart A, Form T2048 Chart A line 9 "Line 7 minus line 8 (if negative
enter "0")": line 7 minus line 8, floored at zero."""

QBT_INVESTMENT_EXPENSES = CATALOG.declare("qbt_investment_expenses", Decimal, non_negative=True)
"""Investment expenses, Form T2048 Chart A line 10 "Investment expenses: add lines 1 to 6, and line
9": the sum of lines 1 to 6 and line 9."""

QBT_DIVIDENDS_AND_INVESTMENT_INCOME = CATALOG.declare(
    "qbt_dividends_and_investment_income", Decimal, non_negative=True
)
"""Investment income, Form T2048 Chart A line 11 "Investment income (lines 12000 and 12100)": the
sum of the taxable dividends and the interest and other investment income."""

QBT_OTHER_PROPERTY_INCOME = CATALOG.declare("qbt_other_property_income", Decimal, non_negative=True)
"""Other property income, Form T2048 Chart A line 14 "Any other property income reported in 2025
(see the list of "other property income" on the next page) including annuity payments taxable
under paragraph 56(1)(d) minus the capital portion deducted under paragraph 60(a)": a starting
amount."""

QBT_RECOVERY_OF_EXPLORATION_EXPENSES = CATALOG.declare(
    "qbt_recovery_of_exploration_expenses", Decimal, non_negative=True
)
"""Recovery of exploration and development expenses at 50%, Form T2048 Chart A line 15 "50% of
income from the recovery of exploration and development expenses (line 13000)": 50% of other
income."""

QBT_INVESTMENT_INCOME = CATALOG.declare("qbt_investment_income", Decimal, non_negative=True)
"""Investment income, Form T2048 Chart A line 19 "Investment income: add lines 11 to 15, and line
18": the sum of lines 11 to 15 and line 18."""

QBT_CHART_A_NET_INVESTMENT_LOSS = CATALOG.declare(
    "qbt_chart_a_net_investment_loss", Decimal, non_negative=True
)
"""Net investment losses for the year, Form T2048 Chart A line 20 "Line 10 minus line 19 (if
negative enter "0")": line 10 minus line 19, floored at zero."""
