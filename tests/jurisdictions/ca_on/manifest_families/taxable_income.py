"""The CA-ON manifest entries of one family of lines (see `test_manifest.py`)."""

from __future__ import annotations

from app.domain.capabilities.apply_fraction import ApplyFraction
from app.domain.capabilities.at_most import AtMost
from app.domain.capabilities.lesser_of import LesserOf
from app.domain.capabilities.subtract import Subtract
from app.domain.capabilities.subtract_not_below_zero import SubtractNotBelowZero
from app.domain.capabilities.sum import Sum
from app.domain.manifest import CapabilitySelection
from app.jurisdictions.ca.catalog import (
    ADDITIONAL_DEDUCTIONS,
    ADJUSTED_GROSS_CAPITAL_LOSSES_1985_TO_1987,
    ADJUSTED_GROSS_CAPITAL_LOSSES_1988_AND_1989,
    ADJUSTED_GROSS_CAPITAL_LOSSES_1990_TO_1999,
    ADJUSTED_GROSS_CAPITAL_LOSSES_2001_TO_2024,
    ADJUSTED_LOSSES_APPLIED_1985_TO_1987,
    ADJUSTED_LOSSES_APPLIED_1988_AND_1989,
    ADJUSTED_LOSSES_APPLIED_1990_TO_1999,
    ADJUSTED_LOSSES_APPLIED_2001_TO_2024,
    ADJUSTED_LOSSES_LEFT_AFTER_1985_TO_1987,
    ADJUSTED_LOSSES_LEFT_AFTER_1988_AND_1989,
    ADJUSTED_LOSSES_LEFT_AFTER_1990_TO_1999,
    CANADIAN_ARMED_FORCES_AND_POLICE_DEDUCTION,
    DEDUCTIONS_FROM_NET_INCOME,
    LIMITED_PARTNERSHIP_LOSSES_OF_OTHER_YEARS,
    NET_CAPITAL_LOSS_BALANCE_1985_TO_1987,
    NET_CAPITAL_LOSS_BALANCE_1988_AND_1989,
    NET_CAPITAL_LOSS_BALANCE_1990_TO_1999,
    NET_CAPITAL_LOSS_BALANCE_2001_TO_2024,
    NET_CAPITAL_LOSSES_AVAILABLE_TO_CLAIM,
    NET_CAPITAL_LOSSES_CLAIMED,
    NET_CAPITAL_LOSSES_OF_OTHER_YEARS,
    NET_INCOME,
    NON_CAPITAL_LOSSES_OF_OTHER_YEARS,
    NORTHERN_RESIDENTS_DEDUCTIONS,
    OTHER_PAYMENTS_DEDUCTION,
    REMAINING_ADJUSTED_LOSSES_1985_TO_1987,
    REMAINING_ADJUSTED_LOSSES_1988_AND_1989,
    REMAINING_ADJUSTED_LOSSES_1990_TO_1999,
    REMAINING_ADJUSTED_LOSSES_2001_TO_2024,
    SECURITY_OPTIONS_DEDUCTIONS,
    TAXABLE_CAPITAL_GAINS,
    TAXABLE_INCOME,
    TOTAL_ADJUSTED_NET_CAPITAL_LOSSES,
    UNAPPLIED_NET_CAPITAL_LOSSES_1985_TO_1987,
    UNAPPLIED_NET_CAPITAL_LOSSES_1988_AND_1989,
    UNAPPLIED_NET_CAPITAL_LOSSES_1990_TO_1999,
    UNAPPLIED_NET_CAPITAL_LOSSES_2001_TO_2024,
)

INPUTS = frozenset(
    {
        "ca/limited_partnership_losses_of_other_years",
        "ca/non_capital_losses_of_other_years",
        "ca/unapplied_net_capital_losses_1985_to_1987",
        "ca/unapplied_net_capital_losses_1988_and_1989",
        "ca/unapplied_net_capital_losses_1990_to_1999",
        "ca/unapplied_net_capital_losses_2001_to_2024",
        "ca/net_capital_losses_claimed",
        "ca/additional_deductions",
    }
)

OUTPUTS = frozenset(
    {
        "ca/net_capital_loss_balance_1985_to_1987",
        "ca/net_capital_loss_balance_1988_and_1989",
        "ca/net_capital_loss_balance_1990_to_1999",
        "ca/net_capital_loss_balance_2001_to_2024",
    }
)

STEPS = {
    # Form T1436 (Capital Gains Worksheet), "Line 25300 - Net capital loss of other years (if
    # you have pre-1986 capital loss balance)" and its "Chart A - Adjustment calculation for
    # carry-forward losses": each cell of the printed rows "After May 22, 1985, and before
    # 1988", "In 1988 and 1989", "After 1989 and before 2000" and "After 2000 and before 2025"
    # is its own step. Column (A) "Amount of your unapplied net capital losses" is a starting
    # amount per row, as the form takes it; the rows "Before May 23, 1985" and "In 2000" are not
    # wired yet.
    # Row "After May 22, 1985, and before 1988", column (C) "Adjusted gross capital losses
    # (column A multiplied by column B)", column (B) "Adjustment factor (for the inclusion
    # rate)" being 1.
    CapabilitySelection(
        name="core/apply_fraction",
        params={"fraction": "ca/net_capital_loss_inclusion_rate_factor_1985_to_1987"},
        consumes={"base": "ca/unapplied_net_capital_losses_1985_to_1987"},
        produces={"output": "ca/adjusted_gross_capital_losses_1985_to_1987"},
    ),
    # Row "In 1988 and 1989", column (C) "Adjusted gross capital losses (column A multiplied by
    # column B)", column (B) "Adjustment factor (for the inclusion rate)" being 3/4 (printed
    # 0.75).
    CapabilitySelection(
        name="core/apply_fraction",
        params={"fraction": "ca/net_capital_loss_inclusion_rate_factor_1988_and_1989"},
        consumes={"base": "ca/unapplied_net_capital_losses_1988_and_1989"},
        produces={"output": "ca/adjusted_gross_capital_losses_1988_and_1989"},
    ),
    # Row "After 1989 and before 2000", column (C) "Adjusted gross capital losses (column A
    # multiplied by column B)", column (B) "Adjustment factor (for the inclusion rate)" being
    # 2/3 (printed 0.6667).
    CapabilitySelection(
        name="core/apply_fraction",
        params={"fraction": "ca/net_capital_loss_inclusion_rate_factor_1990_to_1999"},
        consumes={"base": "ca/unapplied_net_capital_losses_1990_to_1999"},
        produces={"output": "ca/adjusted_gross_capital_losses_1990_to_1999"},
    ),
    # Row "After 2000 and before 2025", column (C) "Adjusted gross capital losses (column A
    # multiplied by column B)", column (B) "Adjustment factor (for the inclusion rate)" being 1.
    CapabilitySelection(
        name="core/apply_fraction",
        params={"fraction": "ca/net_capital_loss_inclusion_rate_factor_2001_to_2024"},
        consumes={"base": "ca/unapplied_net_capital_losses_2001_to_2024"},
        produces={"output": "ca/adjusted_gross_capital_losses_2001_to_2024"},
    ),
    # Line 4 "Total of column C from Chart A".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/adjusted_gross_capital_losses_1985_to_1987",
                "ca/adjusted_gross_capital_losses_1988_and_1989",
                "ca/adjusted_gross_capital_losses_1990_to_1999",
                "ca/adjusted_gross_capital_losses_2001_to_2024",
            ),
        },
        produces={"output": "ca/total_adjusted_net_capital_losses"},
    ),
    # Line 5 "Taxable capital gains from line 12700 of your 2025 return", then line 6 "Enter
    # whichever is less: amount from line 4 or line 5.", in that order.
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={
            "amounts": (
                "ca/total_adjusted_net_capital_losses",
                "ca/taxable_capital_gains",
            ),
        },
        produces={"output": "ca/net_capital_losses_available_to_claim"},
    ),
    # Line 7 "Enter the amount of losses you want to claim (3).", note (3) "You can apply all or
    # part of the amount from line 6 against your taxable capital gains in 2025.": the amount
    # the filer chooses to claim, a starting amount, refused when above line 6, not capped.
    # Lines 1 to 3 are not completed, so "enter the amount from line 7 on line 25300 of your
    # 2025 return" and "enter the amount from line 7 on line 13": line 7 is T1 line 63 and line
    # 25300 "Net capital losses of other years" and Form T1436 line 13.
    CapabilitySelection(
        name="core/at_most",
        params={},
        consumes={
            "amount": "ca/net_capital_losses_claimed",
            "bound": "ca/net_capital_losses_available_to_claim",
        },
        produces={"output": "ca/net_capital_losses_of_other_years"},
    ),
    # Row "After May 22, 1985, and before 1988", column (D) "Total adjusted net capital losses
    # applied against taxable capital gains in 2025": the lesser of column C and line 13, the
    # amount claimed, as "You have to apply net capital losses of earlier years before you apply
    # net capital losses of later years." (Guide T4037) puts the oldest row first.
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={
            "amounts": (
                "ca/adjusted_gross_capital_losses_1985_to_1987",
                "ca/net_capital_losses_of_other_years",
            ),
        },
        produces={"output": "ca/adjusted_losses_applied_1985_to_1987"},
    ),
    # What is left of line 13 after the row "After May 22, 1985, and before 1988": the amount
    # before it less its column D.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/net_capital_losses_of_other_years",
            "less": "ca/adjusted_losses_applied_1985_to_1987",
        },
        produces={"output": "ca/adjusted_losses_left_after_1985_to_1987"},
    ),
    # Row "After May 22, 1985, and before 1988", column (E) "Remaining adjusted net capital
    # losses (column C minus column D)".
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/adjusted_gross_capital_losses_1985_to_1987",
            "less": "ca/adjusted_losses_applied_1985_to_1987",
        },
        produces={"output": "ca/remaining_adjusted_losses_1985_to_1987"},
    ),
    # Row "After May 22, 1985, and before 1988", column (G) "Net capital loss balance available
    # to carry forward (column E multiplied by column F)", column (F) "Adjustment factor (for
    # carry-forward losses)" being 1.
    CapabilitySelection(
        name="core/apply_fraction",
        params={"fraction": "ca/net_capital_loss_carry_forward_factor_1985_to_1987"},
        consumes={"base": "ca/remaining_adjusted_losses_1985_to_1987"},
        produces={"output": "ca/net_capital_loss_balance_1985_to_1987"},
    ),
    # Row "In 1988 and 1989", column (D): the lesser of column C and what is left of line 13
    # after the older rows.
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={
            "amounts": (
                "ca/adjusted_gross_capital_losses_1988_and_1989",
                "ca/adjusted_losses_left_after_1985_to_1987",
            ),
        },
        produces={"output": "ca/adjusted_losses_applied_1988_and_1989"},
    ),
    # What is left of line 13 after the row "In 1988 and 1989": the amount before it less its
    # column D.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/adjusted_losses_left_after_1985_to_1987",
            "less": "ca/adjusted_losses_applied_1988_and_1989",
        },
        produces={"output": "ca/adjusted_losses_left_after_1988_and_1989"},
    ),
    # Row "In 1988 and 1989", column (E) "Remaining adjusted net capital losses (column C minus
    # column D)".
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/adjusted_gross_capital_losses_1988_and_1989",
            "less": "ca/adjusted_losses_applied_1988_and_1989",
        },
        produces={"output": "ca/remaining_adjusted_losses_1988_and_1989"},
    ),
    # Row "In 1988 and 1989", column (G) "Net capital loss balance available to carry forward
    # (column E multiplied by column F)", column (F) "Adjustment factor (for carry-forward
    # losses)" being 4/3 (printed 1.33).
    CapabilitySelection(
        name="core/apply_fraction",
        params={"fraction": "ca/net_capital_loss_carry_forward_factor_1988_and_1989"},
        consumes={"base": "ca/remaining_adjusted_losses_1988_and_1989"},
        produces={"output": "ca/net_capital_loss_balance_1988_and_1989"},
    ),
    # Row "After 1989 and before 2000", column (D): the lesser of column C and what is left of
    # line 13 after the older rows.
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={
            "amounts": (
                "ca/adjusted_gross_capital_losses_1990_to_1999",
                "ca/adjusted_losses_left_after_1988_and_1989",
            ),
        },
        produces={"output": "ca/adjusted_losses_applied_1990_to_1999"},
    ),
    # What is left of line 13 after the row "After 1989 and before 2000": the amount before it
    # less its column D.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/adjusted_losses_left_after_1988_and_1989",
            "less": "ca/adjusted_losses_applied_1990_to_1999",
        },
        produces={"output": "ca/adjusted_losses_left_after_1990_to_1999"},
    ),
    # Row "After 1989 and before 2000", column (E) "Remaining adjusted net capital losses
    # (column C minus column D)".
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/adjusted_gross_capital_losses_1990_to_1999",
            "less": "ca/adjusted_losses_applied_1990_to_1999",
        },
        produces={"output": "ca/remaining_adjusted_losses_1990_to_1999"},
    ),
    # Row "After 1989 and before 2000", column (G) "Net capital loss balance available to carry
    # forward (column E multiplied by column F)", column (F) "Adjustment factor (for
    # carry-forward losses)" being 3/2 (printed 1.5).
    CapabilitySelection(
        name="core/apply_fraction",
        params={"fraction": "ca/net_capital_loss_carry_forward_factor_1990_to_1999"},
        consumes={"base": "ca/remaining_adjusted_losses_1990_to_1999"},
        produces={"output": "ca/net_capital_loss_balance_1990_to_1999"},
    ),
    # Row "After 2000 and before 2025", column (D): the lesser of column C and what is left of
    # line 13 after the older rows.
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={
            "amounts": (
                "ca/adjusted_gross_capital_losses_2001_to_2024",
                "ca/adjusted_losses_left_after_1990_to_1999",
            ),
        },
        produces={"output": "ca/adjusted_losses_applied_2001_to_2024"},
    ),
    # Row "After 2000 and before 2025", column (E) "Remaining adjusted net capital losses
    # (column C minus column D)".
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/adjusted_gross_capital_losses_2001_to_2024",
            "less": "ca/adjusted_losses_applied_2001_to_2024",
        },
        produces={"output": "ca/remaining_adjusted_losses_2001_to_2024"},
    ),
    # Row "After 2000 and before 2025", column (G) "Net capital loss balance available to carry
    # forward (column E multiplied by column F)", column (F) "Adjustment factor (for
    # carry-forward losses)" being 1.
    CapabilitySelection(
        name="core/apply_fraction",
        params={"fraction": "ca/net_capital_loss_carry_forward_factor_2001_to_2024"},
        consumes={"base": "ca/remaining_adjusted_losses_2001_to_2024"},
        produces={"output": "ca/net_capital_loss_balance_2001_to_2024"},
    ),
    # T1 line 68 and line 25700 "Add lines 58 to 67.": lines 58, 59, 60, 61, 62, 63, 66 and 67
    # (lines 24400, 24900, 25000, 25100, 25200, 25300, 25500 and 25600), in line order; lines 64
    # and 65 (25395 and 25400) are not wired yet.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/canadian_armed_forces_and_police_deduction",
                "ca/security_options_deductions",
                "ca/other_payments_deduction",
                "ca/limited_partnership_losses_of_other_years",
                "ca/non_capital_losses_of_other_years",
                "ca/net_capital_losses_of_other_years",
                "ca/northern_residents_deductions",
                "ca/additional_deductions",
            )
        },
        produces={"output": "ca/deductions_from_net_income"},
    ),
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={"amount": "ca/net_income", "less": "ca/deductions_from_net_income"},
        produces={"output": "ca/taxable_income"},
    ),
}

WIRING = {
    (
        ApplyFraction,
        frozenset({UNAPPLIED_NET_CAPITAL_LOSSES_1985_TO_1987}),
        frozenset({ADJUSTED_GROSS_CAPITAL_LOSSES_1985_TO_1987}),
    ),
    (
        ApplyFraction,
        frozenset({UNAPPLIED_NET_CAPITAL_LOSSES_1988_AND_1989}),
        frozenset({ADJUSTED_GROSS_CAPITAL_LOSSES_1988_AND_1989}),
    ),
    (
        ApplyFraction,
        frozenset({UNAPPLIED_NET_CAPITAL_LOSSES_1990_TO_1999}),
        frozenset({ADJUSTED_GROSS_CAPITAL_LOSSES_1990_TO_1999}),
    ),
    (
        ApplyFraction,
        frozenset({UNAPPLIED_NET_CAPITAL_LOSSES_2001_TO_2024}),
        frozenset({ADJUSTED_GROSS_CAPITAL_LOSSES_2001_TO_2024}),
    ),
    (
        Sum,
        frozenset(
            {
                ADJUSTED_GROSS_CAPITAL_LOSSES_1985_TO_1987,
                ADJUSTED_GROSS_CAPITAL_LOSSES_1988_AND_1989,
                ADJUSTED_GROSS_CAPITAL_LOSSES_1990_TO_1999,
                ADJUSTED_GROSS_CAPITAL_LOSSES_2001_TO_2024,
            }
        ),
        frozenset({TOTAL_ADJUSTED_NET_CAPITAL_LOSSES}),
    ),
    (
        LesserOf,
        frozenset({TOTAL_ADJUSTED_NET_CAPITAL_LOSSES, TAXABLE_CAPITAL_GAINS}),
        frozenset({NET_CAPITAL_LOSSES_AVAILABLE_TO_CLAIM}),
    ),
    (
        AtMost,
        frozenset({NET_CAPITAL_LOSSES_CLAIMED, NET_CAPITAL_LOSSES_AVAILABLE_TO_CLAIM}),
        frozenset({NET_CAPITAL_LOSSES_OF_OTHER_YEARS}),
    ),
    (
        LesserOf,
        frozenset({ADJUSTED_GROSS_CAPITAL_LOSSES_1985_TO_1987, NET_CAPITAL_LOSSES_OF_OTHER_YEARS}),
        frozenset({ADJUSTED_LOSSES_APPLIED_1985_TO_1987}),
    ),
    (
        Subtract,
        frozenset({NET_CAPITAL_LOSSES_OF_OTHER_YEARS, ADJUSTED_LOSSES_APPLIED_1985_TO_1987}),
        frozenset({ADJUSTED_LOSSES_LEFT_AFTER_1985_TO_1987}),
    ),
    (
        Subtract,
        frozenset(
            {ADJUSTED_GROSS_CAPITAL_LOSSES_1985_TO_1987, ADJUSTED_LOSSES_APPLIED_1985_TO_1987}
        ),
        frozenset({REMAINING_ADJUSTED_LOSSES_1985_TO_1987}),
    ),
    (
        ApplyFraction,
        frozenset({REMAINING_ADJUSTED_LOSSES_1985_TO_1987}),
        frozenset({NET_CAPITAL_LOSS_BALANCE_1985_TO_1987}),
    ),
    (
        LesserOf,
        frozenset(
            {
                ADJUSTED_GROSS_CAPITAL_LOSSES_1988_AND_1989,
                ADJUSTED_LOSSES_LEFT_AFTER_1985_TO_1987,
            }
        ),
        frozenset({ADJUSTED_LOSSES_APPLIED_1988_AND_1989}),
    ),
    (
        Subtract,
        frozenset({ADJUSTED_LOSSES_LEFT_AFTER_1985_TO_1987, ADJUSTED_LOSSES_APPLIED_1988_AND_1989}),
        frozenset({ADJUSTED_LOSSES_LEFT_AFTER_1988_AND_1989}),
    ),
    (
        Subtract,
        frozenset(
            {ADJUSTED_GROSS_CAPITAL_LOSSES_1988_AND_1989, ADJUSTED_LOSSES_APPLIED_1988_AND_1989}
        ),
        frozenset({REMAINING_ADJUSTED_LOSSES_1988_AND_1989}),
    ),
    (
        ApplyFraction,
        frozenset({REMAINING_ADJUSTED_LOSSES_1988_AND_1989}),
        frozenset({NET_CAPITAL_LOSS_BALANCE_1988_AND_1989}),
    ),
    (
        LesserOf,
        frozenset(
            {
                ADJUSTED_GROSS_CAPITAL_LOSSES_1990_TO_1999,
                ADJUSTED_LOSSES_LEFT_AFTER_1988_AND_1989,
            }
        ),
        frozenset({ADJUSTED_LOSSES_APPLIED_1990_TO_1999}),
    ),
    (
        Subtract,
        frozenset({ADJUSTED_LOSSES_LEFT_AFTER_1988_AND_1989, ADJUSTED_LOSSES_APPLIED_1990_TO_1999}),
        frozenset({ADJUSTED_LOSSES_LEFT_AFTER_1990_TO_1999}),
    ),
    (
        Subtract,
        frozenset(
            {ADJUSTED_GROSS_CAPITAL_LOSSES_1990_TO_1999, ADJUSTED_LOSSES_APPLIED_1990_TO_1999}
        ),
        frozenset({REMAINING_ADJUSTED_LOSSES_1990_TO_1999}),
    ),
    (
        ApplyFraction,
        frozenset({REMAINING_ADJUSTED_LOSSES_1990_TO_1999}),
        frozenset({NET_CAPITAL_LOSS_BALANCE_1990_TO_1999}),
    ),
    (
        LesserOf,
        frozenset(
            {
                ADJUSTED_GROSS_CAPITAL_LOSSES_2001_TO_2024,
                ADJUSTED_LOSSES_LEFT_AFTER_1990_TO_1999,
            }
        ),
        frozenset({ADJUSTED_LOSSES_APPLIED_2001_TO_2024}),
    ),
    (
        Subtract,
        frozenset(
            {ADJUSTED_GROSS_CAPITAL_LOSSES_2001_TO_2024, ADJUSTED_LOSSES_APPLIED_2001_TO_2024}
        ),
        frozenset({REMAINING_ADJUSTED_LOSSES_2001_TO_2024}),
    ),
    (
        ApplyFraction,
        frozenset({REMAINING_ADJUSTED_LOSSES_2001_TO_2024}),
        frozenset({NET_CAPITAL_LOSS_BALANCE_2001_TO_2024}),
    ),
    (
        Sum,
        frozenset(
            {
                CANADIAN_ARMED_FORCES_AND_POLICE_DEDUCTION,
                SECURITY_OPTIONS_DEDUCTIONS,
                OTHER_PAYMENTS_DEDUCTION,
                LIMITED_PARTNERSHIP_LOSSES_OF_OTHER_YEARS,
                NON_CAPITAL_LOSSES_OF_OTHER_YEARS,
                NET_CAPITAL_LOSSES_OF_OTHER_YEARS,
                NORTHERN_RESIDENTS_DEDUCTIONS,
                ADDITIONAL_DEDUCTIONS,
            }
        ),
        frozenset({DEDUCTIONS_FROM_NET_INCOME}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({NET_INCOME, DEDUCTIONS_FROM_NET_INCOME}),
        frozenset({TAXABLE_INCOME}),
    ),
}
