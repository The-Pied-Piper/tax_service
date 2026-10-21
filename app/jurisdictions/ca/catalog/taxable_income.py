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
"""x."""

QBT_PERCENTAGE_ALLOCATED = CATALOG.declare("qbt_percentage_allocated", Decimal, non_negative=True)
"""x."""

QBT_AMOUNT_ALLOCATED = CATALOG.declare("qbt_amount_allocated", Decimal, non_negative=True)
"""x."""

QBT_TAXABLE_AMOUNT_ALLOCATED = CATALOG.declare(
    "qbt_taxable_amount_allocated", Decimal, non_negative=True
)
"""x."""

QBT_PRIOR_YEARS_CLAIMS = CATALOG.declare("qbt_prior_years_claims", Decimal, non_negative=True)
"""x."""

QBT_DEDUCTION_AVAILABLE = CATALOG.declare("qbt_deduction_available", Decimal, non_negative=True)
"""x."""

QBT_CAPITAL_GAINS = CATALOG.declare("qbt_capital_gains", Decimal, non_negative=True)
"""x."""

QBT_2024_RESERVE = CATALOG.declare("qbt_2024_reserve", Decimal, non_negative=True)
"""x."""

QBT_CAPITAL_GAINS_WITH_2024_RESERVE = CATALOG.declare(
    "qbt_capital_gains_with_2024_reserve", Decimal, non_negative=True
)
"""x."""

QBT_2025_RESERVE = CATALOG.declare("qbt_2025_reserve", Decimal, non_negative=True)
"""x."""

QBT_TOTAL_CAPITAL_GAINS = CATALOG.declare("qbt_total_capital_gains", Decimal, non_negative=True)
"""x."""

QBT_TAXABLE_CAPITAL_GAINS = CATALOG.declare("qbt_taxable_capital_gains", Decimal, non_negative=True)
"""x."""

QBT_TAXABLE_GAINS_LIMIT = CATALOG.declare("qbt_taxable_gains_limit", Decimal, non_negative=True)
"""x."""

QBT_TAXABLE_GAINS_NOT_LIMITED = CATALOG.declare(
    "qbt_taxable_gains_not_limited", Decimal, non_negative=True
)
"""x."""

QBT_NET_CAPITAL_LOSSES_REMAINING = CATALOG.declare(
    "qbt_net_capital_losses_remaining", Decimal, non_negative=True
)
"""x."""

QBT_HAS_INVESTMENT_EXPENSES = CATALOG.declare("qbt_has_investment_expenses", int, non_negative=True)
"""x."""

QBT_NET_INVESTMENT_LOSS = CATALOG.declare("qbt_net_investment_loss", Decimal, non_negative=True)
"""x."""

QBT_REDUCTIONS_FROM_LOSSES = CATALOG.declare(
    "qbt_reductions_from_losses", Decimal, non_negative=True
)
"""x."""

QBT_DEDUCTION_LIMIT = CATALOG.declare("qbt_deduction_limit", Decimal, non_negative=True)
"""x."""

QBT_MAXIMUM_DEDUCTION = CATALOG.declare("qbt_maximum_deduction", Decimal, non_negative=True)
"""x."""

QBT_DEDUCTION_CLAIMED = CATALOG.declare("qbt_deduction_claimed", Decimal, non_negative=True)
"""x."""

QBT_CAPITAL_GAINS_DEDUCTION = CATALOG.declare(
    "qbt_capital_gains_deduction", Decimal, non_negative=True
)
"""x."""

QBT_DEDUCTION_BASE = CATALOG.declare("qbt_deduction_base", Decimal, non_negative=True)
"""x."""

QBT_REDUCTION_AMOUNT = CATALOG.declare("qbt_reduction_amount", Decimal, non_negative=True)
"""x."""

QBT_ALLOCATION_TOTAL = CATALOG.declare("qbt_allocation_total", Decimal, non_negative=True)
"""x."""

QBT_ABIL_AND_NET_INVESTMENT_LOSS = CATALOG.declare(
    "qbt_abil_and_net_investment_loss", Decimal, non_negative=True
)
"""x."""

QBT_ALLOCATION_LIMIT = CATALOG.declare("qbt_allocation_limit", Decimal, non_negative=True)
"""x."""

QBT_ABIL_REDUCTION = CATALOG.declare("qbt_abil_reduction", Decimal, non_negative=True)
"""x."""

QBT_NET_INVESTMENT_LOSS_REDUCTION = CATALOG.declare(
    "qbt_net_investment_loss_reduction", Decimal, non_negative=True
)
"""x."""

QBT_ELECTION_IS_QBT = CATALOG.declare("qbt_election_is_qbt", int, non_negative=True)
"""x."""

QBT_GAINS_ARE_QSBCS_OR_QFFP = CATALOG.declare("qbt_gains_are_qsbcs_or_qffp", int, non_negative=True)
"""x."""

QCC_ELECTION_DEDUCTION = CATALOG.declare("qcc_election_deduction", Decimal, non_negative=True)
"""x."""

QBT_ELECTION_DEDUCTION = CATALOG.declare("qbt_election_deduction", Decimal, non_negative=True)
"""x."""

QBT_TAXABLE_GAINS_RELATED_TO_DEDUCTION = CATALOG.declare(
    "qbt_taxable_gains_related_to_deduction", Decimal, non_negative=True
)
"""x."""

QSBCS_QFFP_TAXABLE_GAINS_RELATED_TO_DEDUCTION = CATALOG.declare(
    "qsbcs_qffp_taxable_gains_related_to_deduction", Decimal, non_negative=True
)
"""x."""

QBT_NET_RENTAL_INCOME = CATALOG.declare("qbt_net_rental_income", Decimal, non_negative=True)
"""x."""

QBT_NET_RENTAL_LOSS = CATALOG.declare("qbt_net_rental_loss", Decimal, non_negative=True)
"""x."""

QBT_PARTNERSHIP_LOSSES = CATALOG.declare("qbt_partnership_losses", Decimal, non_negative=True)
"""x."""

QBT_EXPLORATION_EXPENSES_AT_HALF = CATALOG.declare(
    "qbt_exploration_expenses_at_half", Decimal, non_negative=True
)
"""x."""

QBT_OTHER_INVESTMENT_EXPENSES = CATALOG.declare(
    "qbt_other_investment_expenses", Decimal, non_negative=True
)
"""x."""

QBT_CHART_A_NET_CAPITAL_LOSSES_USED = CATALOG.declare(
    "qbt_chart_a_net_capital_losses_used", Decimal, non_negative=True
)
"""x."""

QBT_INVESTMENT_EXPENSES = CATALOG.declare("qbt_investment_expenses", Decimal, non_negative=True)
"""x."""

QBT_DIVIDENDS_AND_INVESTMENT_INCOME = CATALOG.declare(
    "qbt_dividends_and_investment_income", Decimal, non_negative=True
)
"""x."""

QBT_OTHER_PROPERTY_INCOME = CATALOG.declare("qbt_other_property_income", Decimal, non_negative=True)
"""x."""

QBT_RECOVERY_OF_EXPLORATION_EXPENSES = CATALOG.declare(
    "qbt_recovery_of_exploration_expenses", Decimal, non_negative=True
)
"""x."""

QBT_INVESTMENT_INCOME = CATALOG.declare("qbt_investment_income", Decimal, non_negative=True)
"""x."""

QBT_CHART_A_NET_INVESTMENT_LOSS = CATALOG.declare(
    "qbt_chart_a_net_investment_loss", Decimal, non_negative=True
)
"""x."""
