"""The federal catalog: losses of other years and taxable income.

The non-capital and net capital losses of other years, the deductions from net income, taxable
income and the federal basic tax.
"""

from __future__ import annotations

from decimal import Decimal

from app.domain.record_list import RecordListKind
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

UNAPPLIED_NET_CAPITAL_LOSSES_2000 = CATALOG.declare(
    "unapplied_net_capital_losses_2000", Decimal, non_negative=True
)
"""Unapplied net capital losses, Form T1436 "Line 25300 - Net capital loss of other years (if you
have pre-1986 capital loss balance)", Chart A column (A) "Amount of your unapplied net capital
losses", row "In 2000": a starting amount. The 2000 inclusion rate (ca/t657_inclusion_rate_2000)
must be entered when this is not 0; with that rate at 0 the row's adjusted amount is 0."""

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

ADJUSTED_GROSS_CAPITAL_LOSSES_2000 = CATALOG.declare(
    "adjusted_gross_capital_losses_2000", Decimal, non_negative=True
)
"""Adjusted gross capital losses, Form T1436 Chart A column (C) "Adjusted gross capital losses
(column A multiplied by column B)", row "In 2000": column A times the exact fraction of column B,
rounded half-up to the cent, once; 0 when IR is 0."""

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

ADJUSTED_LOSSES_APPLIED_2000 = CATALOG.declare(
    "adjusted_losses_applied_2000", Decimal, non_negative=True
)
"""Adjusted losses applied, Form T1436 Chart A column (D) "Total adjusted net capital losses applied
against taxable capital gains in 2025", row "In 2000": the lesser of column C and what is left of
line 13 after the older rows, as Guide T4037 applies the earlier years first."""

ADJUSTED_LOSSES_LEFT_AFTER_2000 = CATALOG.declare(
    "adjusted_losses_left_after_2000", Decimal, non_negative=True
)
"""Adjusted losses left after the row "In 2000": what is left of line 13, the amount claimed, once
the row's column D is taken off, for the next row's column D."""

REMAINING_ADJUSTED_LOSSES_2000 = CATALOG.declare(
    "remaining_adjusted_losses_2000", Decimal, non_negative=True
)
"""Remaining adjusted losses, Form T1436 Chart A column (E) "Remaining adjusted net capital losses
(column C minus column D)", row "In 2000": column C less column D."""

NET_CAPITAL_LOSS_BALANCE_2000 = CATALOG.declare(
    "net_capital_loss_balance_2000", Decimal, non_negative=True
)
"""Net capital loss balance, Form T1436 Chart A column (G) "Net capital loss balance available to
carry forward (column E multiplied by column F)", row "In 2000": column E times the exact fraction
of column F, rounded half-up to the cent, once; what the return produces for next year's
column A."""

NET_CAPITAL_LOSS_TWICE_IR_2000 = CATALOG.declare(
    "net_capital_loss_twice_ir_2000", Decimal, non_negative=True
)
"""Twice IR, Form T1436 Chart A column (F) "2 × IR", row "In 2000" (footnote (2): "IR" is the
inclusion rate for 2000): IR multiplied by 2, exact and not rounded."""

NET_CAPITAL_LOSS_NUMERATOR_ONE_2000 = CATALOG.declare(
    "net_capital_loss_numerator_one_2000", Decimal, non_negative=True
)
"""The 1 of the Chart A column (B) factor, Form T1436 Chart A column (B) "1/(IR × 2)", row
"In 2000": the 1 printed in the factor, a credit of 1."""

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

NET_CAPITAL_LOSSES_BEFORE_MAY_23_1985 = CATALOG.declare(
    "net_capital_losses_before_may_23_1985", Decimal, non_negative=True
)
"""Net capital losses before May 23, 1985, Form T1436 "Calculating your pre-1986 capital loss
balance available for 2025, if any" line 1 "Balance of unapplied net capital losses you had before
May 23, 1985": a starting amount."""

PRE_1986_DEDUCTIONS_BEFORE_1988 = CATALOG.declare(
    "pre_1986_deductions_before_1988", Decimal, non_negative=True
)
"""Capital gains deductions claimed, Form T1436 "Calculating your pre-1986 capital loss balance
available for 2025, if any", "Capital gains deductions you claimed:", row "Before 1988" (A): a
starting amount."""

PRE_1986_DEDUCTIONS_1988_AND_1989 = CATALOG.declare(
    "pre_1986_deductions_1988_and_1989", Decimal, non_negative=True
)
"""Capital gains deductions claimed, Form T1436 "Calculating your pre-1986 capital loss balance
available for 2025, if any", "Capital gains deductions you claimed:", row "In 1988 and 1989" (B): a
starting amount, before the printed "x 0.75"."""

PRE_1986_DEDUCTIONS_1990_TO_1999 = CATALOG.declare(
    "pre_1986_deductions_1990_to_1999", Decimal, non_negative=True
)
"""Capital gains deductions claimed, Form T1436 "Calculating your pre-1986 capital loss balance
available for 2025, if any", "Capital gains deductions you claimed:", row "From 1990 to 1999" (C): a
starting amount, before the printed "x 0.6667"."""

PRE_1986_DEDUCTIONS_2000 = CATALOG.declare("pre_1986_deductions_2000", Decimal, non_negative=True)
"""Capital gains deductions claimed, Form T1436 "Calculating your pre-1986 capital loss balance
available for 2025, if any", "Capital gains deductions you claimed:", row "In 2000" (D): a starting
amount, before the printed "x 1/(IR x 2)". The 2000 inclusion rate (ca/t657_inclusion_rate_2000)
must be entered when this is not 0; with that rate at 0 the row's adjusted amount is 0."""

PRE_1986_DEDUCTIONS_2001_TO_2024 = CATALOG.declare(
    "pre_1986_deductions_2001_to_2024", Decimal, non_negative=True
)
"""Capital gains deductions claimed, Form T1436 "Calculating your pre-1986 capital loss balance
available for 2025, if any", "Capital gains deductions you claimed:", row "From 2001 to 2024" (E): a
starting amount."""

PRE_1986_DEDUCTIONS_ADJUSTED_1988_AND_1989 = CATALOG.declare(
    "pre_1986_deductions_adjusted_1988_and_1989", Decimal, non_negative=True
)
"""Capital gains deductions claimed after adjustment, Form T1436 "Calculating your pre-1986 capital
loss balance available for 2025, if any", row "In 1988 and 1989" (B): the amount times the exact
fraction 3/4 (printed 0.75), rounded half-up to the cent, once."""

PRE_1986_DEDUCTIONS_ADJUSTED_1990_TO_1999 = CATALOG.declare(
    "pre_1986_deductions_adjusted_1990_to_1999", Decimal, non_negative=True
)
"""Capital gains deductions claimed after adjustment, Form T1436 "Calculating your pre-1986 capital
loss balance available for 2025, if any", row "From 1990 to 1999" (C): the amount times the exact
fraction 2/3 (printed 0.6667), rounded half-up to the cent, once."""

PRE_1986_DEDUCTIONS_ADJUSTED_2000 = CATALOG.declare(
    "pre_1986_deductions_adjusted_2000", Decimal, non_negative=True
)
"""Capital gains deductions claimed after adjustment, Form T1436 "Calculating your pre-1986 capital
loss balance available for 2025, if any", row "In 2000" (D): the amount times 1/(IR x 2), the amount
divided by 2 x IR, rounded half-up to the cent, once; 0 when IR is 0."""

PRE_1986_DEDUCTIONS_TOTAL = CATALOG.declare("pre_1986_deductions_total", Decimal, non_negative=True)
"""Total capital gains deductions after adjustment, Form T1436 "Calculating your pre-1986 capital
loss balance available for 2025, if any" line 2 "Total capital gains deductions after adjustment:
add amounts A to E.": the sum of the rows A to E."""

PRE_1986_CAPITAL_LOSS_BALANCE = CATALOG.declare("pre_1986_capital_loss_balance", Decimal)
"""Pre-1986 capital loss balance, Form T1436 "Calculating your pre-1986 capital loss balance
available for 2025, if any" line 3 "Pre-1986 capital loss balance available for 2025: line 1 minus
line 2". The line prints no "(if negative, enter "0")", so the kind is signed."""

ADJUSTED_GROSS_CAPITAL_LOSSES_BEFORE_MAY_23_1985 = CATALOG.declare(
    "adjusted_gross_capital_losses_before_may_23_1985", Decimal, non_negative=True
)
"""Adjusted gross capital losses, Form T1436 Chart A column (C) "Adjusted gross capital losses
(column A multiplied by column B)", row "Before May 23, 1985": column A (line 3) times the exact
fraction of column B, rounded half-up to the cent, once."""

ADJUSTED_LOSSES_APPLIED_BEFORE_MAY_23_1985 = CATALOG.declare(
    "adjusted_losses_applied_before_may_23_1985", Decimal, non_negative=True
)
"""Adjusted losses applied, Form T1436 Chart A column (D) "Total adjusted net capital losses applied
against taxable capital gains in 2025", row "Before May 23, 1985": the lesser of column C and line
13, the oldest row first."""

ADJUSTED_LOSSES_LEFT_AFTER_BEFORE_MAY_23_1985 = CATALOG.declare(
    "adjusted_losses_left_after_before_may_23_1985", Decimal, non_negative=True
)
"""Adjusted losses left after the row "Before May 23, 1985" of Form T1436 Chart A: line 13 less its
column (D), what the next row may take."""

REMAINING_ADJUSTED_LOSSES_BEFORE_MAY_23_1985 = CATALOG.declare(
    "remaining_adjusted_losses_before_may_23_1985", Decimal, non_negative=True
)
"""Remaining adjusted losses, Form T1436 Chart A column (E) "Remaining adjusted net capital losses
(column C minus column D)", row "Before May 23, 1985": column C less column D."""

NET_CAPITAL_LOSS_BALANCE_BEFORE_MAY_23_1985 = CATALOG.declare(
    "net_capital_loss_balance_before_may_23_1985", Decimal, non_negative=True
)
"""Net capital loss balance, Form T1436 Chart A column (G) "Net capital loss balance available to
carry forward (column E multiplied by column F)", row "Before May 23, 1985": column E times the
exact fraction of column F, rounded half-up to the cent, once; what the return produces for next
year."""

ADJUSTED_NET_CAPITAL_LOSSES_APPLIED = CATALOG.declare(
    "adjusted_net_capital_losses_applied", Decimal, non_negative=True
)
"""Adjusted net capital losses applied, Form T1436 line 7 "Enter the amount of losses you want to
claim (3).": the amount claimed, not above line 6."""

UNAPPLIED_ADJUSTED_NET_CAPITAL_LOSSES = CATALOG.declare(
    "unapplied_adjusted_net_capital_losses", Decimal, non_negative=True
)
"""Unapplied adjusted net capital losses, Form T1436 line 8 "Balance of unapplied adjusted net
capital losses of other years not used to reduce taxable capital gains: line 4 minus line 7"."""

NET_CAPITAL_LOSSES_ADDITIONAL_DEDUCTION = CATALOG.declare(
    "net_capital_losses_additional_deduction", Decimal, non_negative=True
)
"""Additional deduction for net capital losses, Form T1436 line 9 "Enter whichever is less: amount
from line 3, line 8, or $2,000": the least of the three."""

TOTAL_ADJUSTED_NET_CAPITAL_LOSSES_APPLIED = CATALOG.declare(
    "total_adjusted_net_capital_losses_applied", Decimal, non_negative=True
)
"""Total adjusted net capital losses of other years applied in 2025, Form T1436 line 13 "Line 11
plus line 12": line 7 plus line 9, the total of Chart A column (D)."""

ADDITIONAL_DEDUCTIONS = CATALOG.declare("additional_deductions", Decimal, non_negative=True)
"""Additional deductions, T1 line 67 and line 25600 "Additional deductions": a starting amount."""

EXEMPT_INCOME_DEDUCTIONS = CATALOG.declare("exempt_income_deductions", Decimal, non_negative=True)
"""Exempt income deductions, Form T2209 note (3) "amounts deductible as net employment income from a
prescribed international organization, as foreign income exempt under a tax treaty, or as adult
basic education tuition assistance (included on line 25600 of your return)": a starting amount, the
part of T1 line 67 and line 25600 "Additional deductions" that the note names. It is already inside
`additional_deductions`; only the foreign tax credit's net income reads it on its own."""

DEDUCTIONS_FROM_NET_INCOME = CATALOG.declare(
    "deductions_from_net_income", Decimal, non_negative=True
)
"""Deductions from net income, T1 line 68 and line 25700 "Add lines 58 to 67.": the sum of the
deductions from net income, here, in line order, lines 58, 59, 60, 61, 62, 63, 64, 65, 66 and 67
(lines 24400, 24900, 25000, 25100, 25200, 25300, 25395, 25400, 25500 and 25600).
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

T2048_DISPOSITIONS = RecordListKind.declare(
    CATALOG,
    "t2048_dispositions",
    fields=(
        QBT_ELECTION_ELIGIBLE_AMOUNT,
        QBT_PERCENTAGE_ALLOCATED,
        QBT_PRIOR_YEARS_CLAIMS,
        QBT_CAPITAL_GAINS,
        QBT_2024_RESERVE,
        QBT_2025_RESERVE,
        QBT_HAS_INVESTMENT_EXPENSES,
        QBT_DEDUCTION_CLAIMED,
        QBT_ELECTION_IS_QBT,
        QBT_GAINS_ARE_QSBCS_OR_QFFP,
        QBT_PARTNERSHIP_LOSSES,
        QBT_OTHER_INVESTMENT_EXPENSES,
        QBT_OTHER_PROPERTY_INCOME,
    ),
)
"""Qualifying dispositions, Form T2048 "If you have more than one qualifying disposition, use a
separate form to complete parts 1 to 4 for each qualifying disposition. You should designate the
order in which the deductions are claimed": one record for each qualifying disposition, in the
order the filer designates, holding the starting inputs of Parts 2 to 5 and Chart A in the form's
order. The form `ca/t2048` runs once for each record; a field is not an artifact of the return."""

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

T657_T2017_LINE_13 = CATALOG.declare("t657_t2017_line_13", Decimal)
"""Amount from Form T2017 line 13, Form T657 Step 1 line 2 "Total amount from line 13 of Form T2017
(if negative, show in brackets)": a starting amount, a loss in brackets."""

T657_NET_NON_ELIGIBLE_TAXABLE_CAPITAL_GAINS = CATALOG.declare(
    "t657_net_non_eligible_taxable_capital_gains", Decimal, non_negative=True
)
"""Net non-eligible taxable capital gains in 2025, Form T657 Step 1 line 15 "Net non-eligible
taxable capital gains in 2025 (line 14 of Chart A of Form T936 for 2025)": a starting amount."""

T657_GAINS_1985_TO_1991 = CATALOG.declare("t657_gains_1985_to_1991", Decimal, non_negative=True)
"""Taxable capital gains reported after 1984 and before 1992, Form T657 Step 2 line 1 "Total taxable
capital gains reported after 1984 and before 1992: Total amount from line 127 of your returns for
these years": a starting amount."""

T657_GAINS_1992_AND_1993 = CATALOG.declare("t657_gains_1992_and_1993", Decimal, non_negative=True)
"""1992 and 1993 eligible taxable capital gains, Form T657 Step 2 line 2 "1992 and 1993 eligible
taxable capital gains": a starting amount."""

T657_GAINS_1994 = CATALOG.declare("t657_gains_1994", Decimal, non_negative=True)
"""1994 eligible taxable capital gains, Form T657 Step 2 line 3 "1994 eligible taxable capital
gains": a starting amount."""

T657_GAINS_1995 = CATALOG.declare("t657_gains_1995", Decimal, non_negative=True)
"""1995 eligible taxable capital gains, Form T657 Step 2 line 4 "1995 eligible taxable capital
gains": a starting amount."""

T657_GAINS_1996_TO_1999 = CATALOG.declare("t657_gains_1996_to_1999", Decimal, non_negative=True)
"""1996 to 1999 eligible taxable capital gains, Form T657 Step 2 line 5 "1996 to 1999 eligible
taxable capital gains": a starting amount."""

T657_GAINS_2000 = CATALOG.declare("t657_gains_2000", Decimal, non_negative=True)
"""2000 eligible taxable capital gains, Form T657 Step 2 line 6 "2000 eligible taxable capital
gains": a starting amount."""

T657_GAINS_2001 = CATALOG.declare("t657_gains_2001", Decimal, non_negative=True)
"""2001 eligible taxable capital gains, Form T657 Step 2 line 7 "2001 eligible taxable capital
gains": a starting amount."""

T657_GAINS_2002_TO_2024 = CATALOG.declare("t657_gains_2002_to_2024", Decimal, non_negative=True)
"""2002 to 2024 eligible taxable capital gains, Form T657 Step 2 line 8 "2002 to 2025 eligible
taxable capital gains", the part for 2002 to 2024: a starting amount; 2025 is Step 1 line 13."""

T657_CAPITAL_LOSSES_CLAIMED_1985 = CATALOG.declare(
    "t657_capital_losses_claimed_1985", Decimal, non_negative=True
)
"""Allowable capital losses claimed in 1985, Form T657 Step 2 line 10 "Allowable capital losses
claimed in 1985 shown in brackets on line 127 of your 1985 return (maximum $2,000)": a starting
amount."""

T657_ABIL_CLAIMED_1985_TO_2024 = CATALOG.declare(
    "t657_abil_claimed_1985_to_2024", Decimal, non_negative=True
)
"""Allowable business investment losses claimed 1985 to 2024, Form T657 Step 2 line 11 "Total amount
from line 217 of your returns for 1985 to 2018 and line 21700 of your returns for 2019 to 2024": a
starting amount."""

T657_T2048_LINE_17217_FOR_2024 = CATALOG.declare(
    "t657_t2048_line_17217_for_2024", Decimal, non_negative=True
)
"""Form T2048 line 17217 for 2024, Form T657 Step 2 line 12 "Amount from line 17217 of Form T2048
for 2024": a starting amount."""

T657_CUMULATIVE_NET_INVESTMENT_LOSS = CATALOG.declare(
    "t657_cumulative_net_investment_loss", Decimal, non_negative=True
)
"""Cumulative net investment loss to December 31, 2025, Form T657 Step 2 line 16 "Cumulative net
investment loss to December 31, 2025: Amount from line C in Part 3 of Form T936 for 2025": a
starting amount."""

T657_DEDUCTIONS_CLAIMED_1985_TO_2024 = CATALOG.declare(
    "t657_deductions_claimed_1985_to_2024", Decimal, non_negative=True
)
"""Total capital gains deductions claimed after 1984 and before 2025, Form T657 Step 2 line 17
"Total capital gains deductions claimed after 1984 and before 2025": a starting amount."""

T657_CHART_2_LINE_1 = CATALOG.declare("t657_chart_2_line_1", Decimal, non_negative=True)
"""Amount from line 254 of your 1985 to 1987 returns, Form T657 Chart 2 line 1 "Amount from line 254
of your 1985 to 1987 returns": a starting amount."""

T657_CHART_2_LINE_2 = CATALOG.declare("t657_chart_2_line_2", Decimal, non_negative=True)
"""Capital gains deductions claimed in 1988 and 1989, excluding eligible capital property, Form T657
Chart 2 line 2 "Capital gains deductions claimed in 1988 and 1989 (excluding eligible capital
property)": a starting amount."""

T657_CHART_2_LINE_6 = CATALOG.declare("t657_chart_2_line_6", Decimal, non_negative=True)
"""Capital gains deductions claimed in 1988 and 1989 for eligible capital property, Form T657 Chart
2 line 6 "Capital gains deductions claimed in 1988 and 1989 for eligible capital property": a
starting amount."""

T657_CHART_2_LINE_10 = CATALOG.declare("t657_chart_2_line_10", Decimal, non_negative=True)
"""Capital gains deductions claimed in 1990 to 1999, Form T657 Chart 2 line 10 "Total capital gains
deductions claimed in 1990 to 1999: Amount from line 254 of your returns for 1990 to 1999": a
starting amount."""

T657_CHART_2_LINE_14 = CATALOG.declare("t657_chart_2_line_14", Decimal, non_negative=True)
"""Capital gains deduction claimed in 2000, Form T657 Chart 2 line 14 "Total capital gains deduction
claimed in 2000: Amount from line 254 of your 2000 return": a starting amount."""

T657_INCLUSION_RATE_2000 = CATALOG.declare("t657_inclusion_rate_2000", Decimal, non_negative=True)
"""Inclusion rate for 2000 (IR), Form T657 Chart 2 footnote (2) "Your "IR" is your inclusion rate
for 2000": a starting rate, entered as a decimal. IR is the 2000 inclusion rate from line 16 of the
filer's 2000 Schedule 3 Part 4. It must be entered when Chart 2 line 14 is not 0; 0 means not
entered, and then the line 16 adjustment is 0 (line 16 equals line 14). Form T1436 Chart A row
"In 2000" reads the same figure, for its column (B) "1/(IR × 2)" and column (F) "2 × IR"."""

T657_CHART_2_LINE_18 = CATALOG.declare("t657_chart_2_line_18", Decimal, non_negative=True)
"""Capital gains deduction claimed in 2001 to 2024, Form T657 Chart 2 line 18 "Total capital gains
deduction claimed in 2001 to 2024: Amount from line 254 of your 2001 to 2018 returns and line 25400
of your 2019 and later returns": a starting amount."""

T657_PART_1_AMOUNT_F = CATALOG.declare("t657_part_1_amount_f", Decimal, non_negative=True)
"""Chart 2025 Part 1 amount F, Form T657 Chart 2025 Part 1 "Add amounts F to J (if negative, enter
"0")": the amount from box 57 of a T3 slip or box 153 of a T5013 slip, a starting amount."""

T657_PART_1_AMOUNT_G = CATALOG.declare("t657_part_1_amount_g", Decimal, non_negative=True)
"""Chart 2025 Part 1 amount G, Form T657 Chart 2025 Part 1 "Add amounts F to J (if negative, enter
"0")": the amount from box 55 of a T3 slip or box 154 of a T5013 slip, a starting amount."""

T657_PART_1_AMOUNT_H = CATALOG.declare("t657_part_1_amount_h", Decimal, non_negative=True)
"""Chart 2025 Part 1 amount H, Form T657 Chart 2025 Part 1 "Add amounts F to J (if negative, enter
"0")": the amount from box 155 of a T5013 slip, a starting amount."""

T657_PART_1_AMOUNT_I = CATALOG.declare("t657_part_1_amount_i", Decimal)
"""Chart 2025 Part 1 amount I, Form T657 Chart 2025 Part 1 "Add amounts F to J (if negative, enter
"0")": "Amount from line 6 of Form T2017", a starting amount, a loss in brackets."""

T657_PART_1_AMOUNT_J = CATALOG.declare("t657_part_1_amount_j", Decimal)
"""Chart 2025 Part 1 amount J, Form T657 Chart 2025 Part 1 "Add amounts F to J (if negative, enter
"0")": "Amount from line 12 of Form T2017", a starting amount, a loss in brackets."""

T657_PART_1_AMOUNT_L = CATALOG.declare("t657_part_1_amount_l", Decimal, non_negative=True)
"""Chart 2025 Part 1 amount L, Form T657 Chart 2025 Part 1 "Amount K minus amount L": the portion of
the amount from line 17216 of Form T2048 for a QFFP or QSBCS disposed of in Period 1 of 2024, a
starting amount."""

T657_PART_2_EXCLUDED_F = CATALOG.declare("t657_part_2_excluded_f", Decimal, non_negative=True)
"""Chart 2025 Part 2 amount F, Form T657 Chart 2025 Part 2 amount F "Amount from line 10700 of
Schedule 3 (do not include ...)": the amount the filer enters as not to be included, a starting
amount."""

T657_PART_2_EXCLUDED_G = CATALOG.declare("t657_part_2_excluded_g", Decimal, non_negative=True)
"""Chart 2025 Part 2 amount G, Form T657 Chart 2025 Part 2 amount G "Amount from line 11000 of
Schedule 3 (do not include ...)": the amount the filer enters as not to be included, a starting
amount."""

T657_PART_2_EXCLUDED_H = CATALOG.declare("t657_part_2_excluded_h", Decimal, non_negative=True)
"""Chart 2025 Part 2 amount H, Form T657 Chart 2025 Part 2 amount H "Amount from line 12400 of
Schedule 3 (do not include ...)": the amount the filer enters as not to be included, a starting
amount."""

T657_PART_2_AMOUNT_I = CATALOG.declare("t657_part_2_amount_i", Decimal)
"""Chart 2025 Part 2 amount I, Form T657 Chart 2025 Part 2 "Add amounts F to J (if negative, enter
"0")": "Amount from line 6 of Form T2017 (do not include ...)", a starting amount, a loss in
brackets."""

T657_PART_2_AMOUNT_J = CATALOG.declare("t657_part_2_amount_j", Decimal)
"""Chart 2025 Part 2 amount J, Form T657 Chart 2025 Part 2 "Add amounts F to J (if negative, enter
"0")": "Amount from line 12 of Form T2017 (...)", a starting amount, a loss in brackets."""

T657_PART_2_AMOUNT_L = CATALOG.declare("t657_part_2_amount_l", Decimal, non_negative=True)
"""Chart 2025 Part 2 amount L, Form T657 Chart 2025 Part 2 "Amount K minus amount L": the portion of
the amount from line 17216 of Form T2048 for a QFFP or QSBCS disposed of in 2025 or after June 24,
2024, a starting amount."""

CAPITAL_GAINS_DEDUCTION_CLAIMED = CATALOG.declare(
    "capital_gains_deduction_claimed", Decimal, non_negative=True
)
"""Capital gains deduction the filer chooses to claim, T1 line 25400 "Capital gains deduction
(complete Form T657)": a starting amount, which may not exceed Part 2 amount Q ("However, you can
choose to claim less.")."""

ANNUAL_GAINS_SCHEDULE_3_TOTAL = CATALOG.declare("annual_gains_schedule_3_total", Decimal)
"""Total of Schedule 3 lines 10700, 11000 and 12400, Form T657 Step 1 line 1 "Total of lines 10700,
11000, and 12400 of Schedule 3 (if negative, show in brackets)": the signed sum."""

ANNUAL_GAINS_LINE_3 = CATALOG.declare("annual_gains_line_3", Decimal)
"""Step 1 line 3, Form T657 Step 1 line 3 "Add lines 1 and 2 (if negative, show in brackets).": line
1 plus line 2, signed."""

ANNUAL_GAINS_LINE_3_AT_INCLUSION_RATE = CATALOG.declare(
    "annual_gains_line_3_at_inclusion_rate", Decimal
)
"""Step 1 line 3 at the inclusion rate, Form T657 Step 1 line 4 "Inclusion rate × 1/2": line 3
multiplied by 1/2, rounded half-up to the cent, before line 5 floors it at 0."""

ANNUAL_GAINS_LINE_5 = CATALOG.declare("annual_gains_line_5", Decimal, non_negative=True)
"""Step 1 line 5, Form T657 Step 1 line 5 "Line 3 multiplied by the inclusion rate on line 4 (if
negative, enter "0")": line 4 floored at 0."""

ANNUAL_GAINS_LINE_7 = CATALOG.declare("annual_gains_line_7", Decimal)
"""Total taxable capital gains or losses for 2025 for qualifying property, Form T657 Step 1 line 7
"Line 5 minus line 6": line 5 minus line 6, signed, not floored."""

SCHEDULE_3_LINE_19900 = CATALOG.declare("schedule_3_line_19900", Decimal)
"""Total taxable capital gains (or net capital losses) from Schedule 3 line 19900, Form T657 Step 1
line 8 "Total taxable capital gains (or net capital losses) from line 19900 of Schedule 3 (if
negative, show in brackets)": Schedule 3 line 24 plus line 25, signed."""

SCHEDULE_3_LINE_17600_NOT_BELOW_ZERO = CATALOG.declare(
    "schedule_3_line_17600_not_below_zero", Decimal, non_negative=True
)
"""Amount from Schedule 3 line 17600, Form T657 Step 1 line 9 "Amount from line 17600 of Schedule 3
(if negative, enter "0")": the amount, floored at 0."""

ANNUAL_GAINS_LINE_9 = CATALOG.declare("annual_gains_line_9", Decimal, non_negative=True)
"""Step 1 line 9 at 1/2, Form T657 Step 1 line 9 "× 1/2 =": the line 17600 amount multiplied by 1/2,
rounded half-up to the cent."""

ANNUAL_GAINS_LINE_10 = CATALOG.declare("annual_gains_line_10", Decimal)
"""Step 1 line 10, Form T657 Step 1 line 10 "Line 8 minus line 9": line 8 minus line 9, signed."""

ANNUAL_GAINS_LINE_12 = CATALOG.declare("annual_gains_line_12", Decimal)
"""Step 1 line 12, Form T657 Step 1 line 12 "Line 10 minus line 11": line 10 minus line 11,
signed."""

ELIGIBLE_TAXABLE_CAPITAL_GAINS_2025 = CATALOG.declare(
    "eligible_taxable_capital_gains_2025", Decimal
)
"""Eligible taxable capital gains for 2025, Form T657 Step 1 line 13 "Enter whichever is less:
amount from line 7 or line 12." "Eligible taxable capital gains for 2025": the lesser of line 7 and
line 12."""

ADJUSTED_NET_CAPITAL_LOSSES_OF_OTHER_YEARS = CATALOG.declare(
    "adjusted_net_capital_losses_of_other_years", Decimal, non_negative=True
)
"""Adjusted net capital losses of other years, Form T657 Step 1 line 16 "Adjusted net capital losses
of other years: Line 14 minus line 15 (if negative, enter "0")": line 14 minus line 15, not below
0."""

ABIL_AFTER_QBT_REDUCTION = CATALOG.declare("abil_after_qbt_reduction", Decimal, non_negative=True)
"""Allowable business investment loss after the QBT reduction, Form T657 Step 1 line 19 "Line 17
minus line 18": line 17 minus line 18, floored at 0 (the form prints no floor)."""

TOTAL_LOSSES_FOR_ANNUAL_GAINS_LIMIT = CATALOG.declare(
    "total_losses_for_annual_gains_limit", Decimal, non_negative=True
)
"""Total losses for annual gains limit, Form T657 Step 1 line 20 "Line 16 plus line 19" "Total
losses for annual gains limit": line 16 plus line 19."""

ANNUAL_GAINS_LIMIT_2025 = CATALOG.declare("annual_gains_limit_2025", Decimal, non_negative=True)
"""Annual gains limit for 2025, Form T657 Step 1 line 21 "Line 13 minus line 20 (if negative, enter
"0")" "Annual gains limit for 2025": line 13 minus line 20, not below 0."""

ELIGIBLE_TAXABLE_CAPITAL_GAINS_2002_TO_2025 = CATALOG.declare(
    "eligible_taxable_capital_gains_2002_to_2025", Decimal
)
"""Eligible taxable capital gains for 2002 to 2025, Form T657 Step 2 line 8 "2002 to 2025 eligible
taxable capital gains": the 2002 to 2024 amount plus Step 1 line 13 for 2025."""

CUMULATIVE_ELIGIBLE_TAXABLE_CAPITAL_GAINS = CATALOG.declare(
    "cumulative_eligible_taxable_capital_gains", Decimal
)
"""Cumulative eligible taxable capital gains, Form T657 Step 2 line 9 "Add lines 1 to 8."
"Cumulative eligible taxable capital gains": the sum of Step 2 lines 1 to 8."""

ABIL_CLAIMED_AFTER_1984_AND_BEFORE_2025 = CATALOG.declare(
    "abil_claimed_after_1984_and_before_2025", Decimal, non_negative=True
)
"""Total allowable business investment losses claimed after 1984 and before 2025, Form T657 Step 2
line 13 "Total allowable business investment losses claimed after 1984 and before 2025: Line 11
minus line 12": line 11 minus line 12, floored at 0 (the form prints no floor)."""

CHART_1_COLUMN_G_TOTAL = CATALOG.declare("chart_1_column_g_total", Decimal, non_negative=True)
"""Total of Chart 1 column G, Form T657 Step 2 line 14 "Total of amounts in column G in Chart 1":
the sum of column G over every year row."""

CUMULATIVE_LOSSES_AND_DEDUCTIONS = CATALOG.declare(
    "cumulative_losses_and_deductions", Decimal, non_negative=True
)
"""Cumulative losses and deductions, Form T657 Step 2 line 18 "Add lines 10 and 13 to 17.": the sum
of lines 10, 13 to 17."""

CUMULATIVE_GAINS_LIMIT_2025 = CATALOG.declare(
    "cumulative_gains_limit_2025", Decimal, non_negative=True
)
"""Cumulative gains limit for 2025, Form T657 Step 2 line 19 "Line 9 minus line 18 (if negative,
enter "0")" "Cumulative gains limit for 2025": line 9 minus line 18, not below 0."""

CHART_2_LINE_3 = CATALOG.declare("chart_2_line_3", Decimal, non_negative=True)
"""Chart 2 line 3, Form T657 Chart 2 line 3 "Line 1 plus line 2": line 1 plus line 2."""

CHART_2_LINE_4 = CATALOG.declare("chart_2_line_4", Decimal, non_negative=True)
"""Adjustment of 1988 and 1989 capital gains deductions excluding eligible capital property, Form
T657 Chart 2 line 4 "Amount from line 2 × 1/4": line 2 multiplied by 1/4, rounded half-up to the
cent."""

CHART_2_LINE_5 = CATALOG.declare("chart_2_line_5", Decimal, non_negative=True)
"""Chart 2 line 5, Form T657 Chart 2 line 5 "Line 3 minus line 4 (if negative, enter "0")": line 3
minus line 4, not below 0."""

CHART_2_LINE_7 = CATALOG.declare("chart_2_line_7", Decimal, non_negative=True)
"""Chart 2 line 7, Form T657 Chart 2 line 7 "Line 5 plus line 6": line 5 plus line 6."""

CHART_2_LINE_8 = CATALOG.declare("chart_2_line_8", Decimal, non_negative=True)
"""Adjustment of 1988 and 1989 capital gains deductions for eligible capital property, Form T657
Chart 2 line 8 "Amount from line 6 × 1/3": line 6 multiplied by 1/3, rounded half-up to the cent."""

CHART_2_LINE_9 = CATALOG.declare("chart_2_line_9", Decimal, non_negative=True)
"""Chart 2 line 9, Form T657 Chart 2 line 9 "Line 7 minus line 8 (if negative, enter "0")": line 7
minus line 8, not below 0."""

CHART_2_LINE_11 = CATALOG.declare("chart_2_line_11", Decimal, non_negative=True)
"""Chart 2 line 11, Form T657 Chart 2 line 11 "Line 9 plus line 10": line 9 plus line 10."""

CHART_2_LINE_12 = CATALOG.declare("chart_2_line_12", Decimal, non_negative=True)
"""Adjustment of 1990 to 1999 capital gains deductions, Form T657 Chart 2 line 12 "Amount from line
10 × 1/3": line 10 multiplied by 1/3, rounded half-up to the cent."""

CHART_2_LINE_13 = CATALOG.declare("chart_2_line_13", Decimal, non_negative=True)
"""Chart 2 line 13, Form T657 Chart 2 line 13 "Line 11 minus line 12 (if negative, enter "0")": line
11 minus line 12, not below 0."""

CHART_2_LINE_15 = CATALOG.declare("chart_2_line_15", Decimal, non_negative=True)
"""Chart 2 line 15, Form T657 Chart 2 line 15 "Line 13 plus line 14": line 13 plus line 14."""

CHART_2_TWICE_IR = CATALOG.declare("chart_2_twice_ir", Decimal, non_negative=True)
"""Twice IR, Form T657 Chart 2 line 16 "Adjustment of 2000 capital gains deduction: Amount from line
14 × [ 1 – ( 2 × IR )]", the "2 × IR": IR multiplied by 2, exact and not rounded."""

CHART_2_LINE_14_OVER_TWICE_IR = CATALOG.declare(
    "chart_2_line_14_over_twice_ir", Decimal, non_negative=True
)
"""Line 14 over twice IR, Form T657 Chart 2 line 16 "Adjustment of 2000 capital gains deduction:
Amount from line 14 × [ 1 – ( 2 × IR )]", line 14 × 1 over ( 2 × IR ): line 14 divided by twice IR,
rounded half-up to the cent once, the only rounding of the line; 0 when IR is 0."""

CHART_2_LINE_16 = CATALOG.declare("chart_2_line_16", Decimal, non_negative=True)
"""Adjustment of 2000 capital gains deduction, Form T657 Chart 2 line 16 "Adjustment of 2000 capital
gains deduction: Amount from line 14 × [ 1 – ( 2 × IR )] = (2)": line 14 minus line 14 multiplied by
1 over ( 2 × IR ), which is line 14 minus the quotient."""

CHART_2_LINE_17 = CATALOG.declare("chart_2_line_17", Decimal, non_negative=True)
"""Chart 2 line 17, Form T657 Chart 2 line 17 "Line 15 minus line 16 (if negative, enter "0")": line
15 minus line 16, not below 0."""

CHART_2_LINE_19 = CATALOG.declare("chart_2_line_19", Decimal, non_negative=True)
"""Capital gains deductions from previous years, Form T657 Chart 2 line 19 "Capital gains deductions
from previous years: Line 17 plus line 18 (if negative, enter 0)": line 17 plus line 18, not below
0."""

CHART_2_NUMERATOR_ONE = CATALOG.declare("chart_2_numerator_one", Decimal, non_negative=True)
"""The 1 of the Chart 2 line 16 quotient, Form T657 Chart 2 line 16 "Adjustment of 2000 capital
gains deduction: Amount from line 14 × [ 1 – ( 2 × IR )]": the 1 printed in the bracket, a credit of
1."""

CHART_2025_PART_1_AMOUNT_A = CATALOG.declare(
    "chart_2025_part_1_amount_a", Decimal, non_negative=True
)
"""Maximum capital gains deduction for QFFP and/or QSBCS reported in 2025 but disposed of in period
1 of 2024, Form T657 Chart 2025 Part 1 amount A: 522,145.00, a dataset."""

CHART_2025_PART_1_AMOUNT_C = CATALOG.declare(
    "chart_2025_part_1_amount_c", Decimal, non_negative=True
)
"""Chart 2025 Part 1 amount C, Form T657 Chart 2025 Part 1 "Amount A minus amount B": amount A minus
amount B, floored at 0 (the form prints no floor)."""

CHART_2025_PART_1_AMOUNT_E = CATALOG.declare(
    "chart_2025_part_1_amount_e", Decimal, non_negative=True
)
"""Chart 2025 Part 1 amount E, Form T657 Chart 2025 Part 1 amount E "amount C minus amount D (if
negative, enter "0")": amount C minus amount D, not below 0."""

CHART_2025_PART_1_AMOUNTS_F_TO_J = CATALOG.declare(
    "chart_2025_part_1_amounts_f_to_j", Decimal, non_negative=True
)
"""Chart 2025 Part 1 amounts F to J, Form T657 Chart 2025 Part 1 "Add amounts F to J (if negative,
enter "0")": the sum of amounts F to J, not below 0."""

CHART_2025_PART_1_AMOUNT_K = CATALOG.declare(
    "chart_2025_part_1_amount_k", Decimal, non_negative=True
)
"""Chart 2025 Part 1 amount K, Form T657 Chart 2025 Part 1 "= × 1/2 = K": amounts F to J multiplied
by 1/2, rounded half-up to the cent."""

CHART_2025_PART_1_AMOUNT_M = CATALOG.declare(
    "chart_2025_part_1_amount_m", Decimal, non_negative=True
)
"""Chart 2025 Part 1 amount M, Form T657 Chart 2025 Part 1 "Amount K minus amount L": amount K minus
amount L, floored at 0 (the form prints no floor)."""

CHART_2025_PART_1_AMOUNT_N = CATALOG.declare(
    "chart_2025_part_1_amount_n", Decimal, non_negative=True
)
"""Chart 2025 Part 1 amount N, Form T657 Chart 2025 Part 1 "Enter whichever is less: amount E or
amount M.": the lesser of amount E and amount M."""

CHART_2025_PART_1_AMOUNT_P = CATALOG.declare(
    "chart_2025_part_1_amount_p", Decimal, non_negative=True
)
"""Chart 2025 Part 1 amount P, Form T657 Chart 2025 Part 1 "Amount N plus amount O": amount N plus
amount B, where O is amount B."""

CHART_2025_PART_1_AMOUNT_Q = CATALOG.declare(
    "chart_2025_part_1_amount_q", Decimal, non_negative=True
)
"""Chart 2025 Part 1 amount Q, Form T657 Chart 2025 Part 1 "Enter whichever is less: line 21 of Step
1, line 19 of Step 2 or amount P above.": the lesser of the annual gains limit, the cumulative gains
limit and amount P."""

CHART_2025_PART_2_AMOUNT_A = CATALOG.declare(
    "chart_2025_part_2_amount_a", Decimal, non_negative=True
)
"""Maximum capital gains deduction for QFFP and/or QSBCS disposed of in 2025 or disposed of after
June 24, 2024 and reported in 2025, Form T657 Chart 2025 Part 2 amount A: 625,000.00, a dataset."""

CHART_2025_PART_2_AMOUNT_C = CATALOG.declare(
    "chart_2025_part_2_amount_c", Decimal, non_negative=True
)
"""Chart 2025 Part 2 amount C, Form T657 Chart 2025 Part 2 "Amount A minus amount B": amount A minus
amount B, floored at 0 (the form prints no floor)."""

CHART_2025_PART_2_AMOUNT_E = CATALOG.declare(
    "chart_2025_part_2_amount_e", Decimal, non_negative=True
)
"""Chart 2025 Part 2 amount E, Form T657 Chart 2025 Part 2 amount E "amount C minus amount D (if
negative, enter "0")": amount C minus amount D, not below 0."""

CHART_2025_PART_2_AMOUNT_F = CATALOG.declare("chart_2025_part_2_amount_f", Decimal)
"""Chart 2025 Part 2 amount F, Form T657 Chart 2025 Part 2 amount F "Amount from line 10700 of
Schedule 3 (do not include ...)": line 10700 of Schedule 3 less the excluded amount F."""

CHART_2025_PART_2_AMOUNT_G = CATALOG.declare("chart_2025_part_2_amount_g", Decimal)
"""Chart 2025 Part 2 amount G, Form T657 Chart 2025 Part 2 amount G "Amount from line 11000 of
Schedule 3 (do not include ...)": line 11000 of Schedule 3 less the excluded amount G."""

CHART_2025_PART_2_AMOUNT_H = CATALOG.declare("chart_2025_part_2_amount_h", Decimal)
"""Chart 2025 Part 2 amount H, Form T657 Chart 2025 Part 2 amount H "Amount from line 12400 of
Schedule 3 (do not include ...)": line 12400 of Schedule 3 less the excluded amount H."""

CHART_2025_PART_2_AMOUNTS_F_TO_J = CATALOG.declare(
    "chart_2025_part_2_amounts_f_to_j", Decimal, non_negative=True
)
"""Chart 2025 Part 2 amounts F to J, Form T657 Chart 2025 Part 2 "Add amounts F to J (if negative,
enter "0")": the sum of amounts F to J, not below 0."""

CHART_2025_PART_2_AMOUNT_K = CATALOG.declare(
    "chart_2025_part_2_amount_k", Decimal, non_negative=True
)
"""Chart 2025 Part 2 amount K, Form T657 Chart 2025 Part 2 "= × 1/2 = K": amounts F to J multiplied
by 1/2, rounded half-up to the cent."""

CHART_2025_PART_2_AMOUNT_M = CATALOG.declare(
    "chart_2025_part_2_amount_m", Decimal, non_negative=True
)
"""Chart 2025 Part 2 amount M, Form T657 Chart 2025 Part 2 "Amount K minus amount L": amount K minus
amount L, floored at 0 (the form prints no floor)."""

CHART_2025_PART_2_AMOUNT_N = CATALOG.declare(
    "chart_2025_part_2_amount_n", Decimal, non_negative=True
)
"""Chart 2025 Part 2 amount N, Form T657 Chart 2025 Part 2 "Enter whichever is less: amount E or
amount M.": the lesser of amount E and amount M."""

CHART_2025_PART_2_AMOUNT_P = CATALOG.declare(
    "chart_2025_part_2_amount_p", Decimal, non_negative=True
)
"""Chart 2025 Part 2 amount P, Form T657 Chart 2025 Part 2 "Amount N plus amount O": amount N plus
amount B, where B is Part 1 amount P."""

CHART_2025_PART_2_AMOUNT_Q = CATALOG.declare(
    "chart_2025_part_2_amount_q", Decimal, non_negative=True
)
"""Chart 2025 Part 2 amount Q, Form T657 Chart 2025 Part 2 "Enter whichever is less: line 21 of Step
1, line 19 of Step 2 or amount P above.": the maximum amount you can claim on line 25400 of your
2025 return."""

CAPITAL_GAINS_DEDUCTION = CATALOG.declare("capital_gains_deduction", Decimal, non_negative=True)
"""Capital gains deduction, T1 line 25400 "Capital gains deduction (complete Form T657)": the amount
claimed, at most Part 2 amount Q."""

T657_CHART_1_COLUMN_A = CATALOG.declare("t657_chart_1_column_a", Decimal, non_negative=True)
"""Net capital losses of other years claimed for the year, Form T657 Chart 1 column A "Enter the
total amount of net capital losses of other years claimed for each year indicated from line 253 or
25300 of each return": a starting amount per year row."""

T657_CHART_1_COLUMN_B = CATALOG.declare("t657_chart_1_column_b", Decimal, non_negative=True)
"""Reserves included in capital gains for property disposed of before 1985, Form T657 Chart 1 column
B "For 1985, 1986, and 1987, enter 1/2 of the total reserves included in capital gains for capital
property disposed of before 1985": a starting amount per year row."""

T657_CHART_1_COLUMN_C = CATALOG.declare("t657_chart_1_column_c", Decimal, non_negative=True)
"""Amount from the Form T936 line named for the year, Form T657 Chart 1 column C "For 1992, enter
whichever amount is less: line 127 of your 1992 return or line (f) in Part A of Form T936 for 1992":
a starting amount per year row."""

T657_CHART_1_COLUMN_D = CATALOG.declare("t657_chart_1_column_d", Decimal, non_negative=True)
"""Amount from the Form T936 line named for the year, Form T657 Chart 1 column D "For 1992, enter
the amount from line (k) in Part B of Form T936 for 1992": a starting amount per year row."""

T657_CHART_1_ROWS = RecordListKind.declare(
    CATALOG,
    "t657_chart_1_rows",
    fields=(
        T657_CHART_1_COLUMN_A,
        T657_CHART_1_COLUMN_B,
        T657_CHART_1_COLUMN_C,
        T657_CHART_1_COLUMN_D,
    ),
)
"""Chart 1 year rows, Form T657 Chart 1 "Chart 1 – Calculate your net capital losses of other years
(line 14 of Step 2)": one record for each YEAR, with columns A to D (the form's own Note:
"complete a separate calculation for each year that applies to you"; the printed rows combine years
only for space). A single-year filer enters one record."""
