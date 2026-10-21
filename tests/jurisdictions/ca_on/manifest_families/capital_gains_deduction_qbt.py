"""The CA-ON manifest entries of Form T2048 (line 25395), Parts 2 to 5 and Chart A (see
`test_manifest.py`).

The steps are in the manifest part `06a_capital_gains_deduction_qbt.yaml`; line 25395 is added to
line 25700 in the `taxable_income` family.
"""

from __future__ import annotations

from app.domain.capabilities.apply_rate import ApplyRate
from app.domain.capabilities.at_most import AtMost
from app.domain.capabilities.lesser_of import LesserOf
from app.domain.capabilities.subtract import Subtract
from app.domain.capabilities.subtract_not_below_zero import SubtractNotBelowZero
from app.domain.capabilities.sum import Sum
from app.domain.capabilities.sum_not_below_zero import SumNotBelowZero
from app.domain.capabilities.times_count import TimesCount
from app.domain.manifest import CapabilitySelection
from app.jurisdictions.ca.capabilities.apply_percentage import ApplyPercentage
from app.jurisdictions.ca.capabilities.apply_ratio_or_zero import ApplyRatioOrZero
from app.jurisdictions.ca.catalog import (
    ALLOWABLE_BUSINESS_INVESTMENT_LOSS,
    CARRYING_CHARGES_INTEREST_EXPENSES_AND_OTHER_EXPENSES,
    EXPLORATION_AND_DEVELOPMENT_EXPENSES,
    INTEREST_AND_OTHER_INVESTMENT_INCOME,
    LIMITED_PARTNERSHIP_LOSSES_OF_OTHER_YEARS,
    NET_CAPITAL_LOSSES_OF_OTHER_YEARS,
    NET_PARTNERSHIP_INCOME,
    NET_RENTAL_INCOME,
    OTHER_INCOME,
    QBT_2024_RESERVE,
    QBT_2025_RESERVE,
    QBT_ABIL_AND_NET_INVESTMENT_LOSS,
    QBT_ABIL_REDUCTION,
    QBT_ALLOCATION_LIMIT,
    QBT_ALLOCATION_TOTAL,
    QBT_AMOUNT_ALLOCATED,
    QBT_CAPITAL_GAINS,
    QBT_CAPITAL_GAINS_DEDUCTION,
    QBT_CAPITAL_GAINS_WITH_2024_RESERVE,
    QBT_CHART_A_NET_CAPITAL_LOSSES_USED,
    QBT_CHART_A_NET_INVESTMENT_LOSS,
    QBT_DEDUCTION_AVAILABLE,
    QBT_DEDUCTION_BASE,
    QBT_DEDUCTION_CLAIMED,
    QBT_DEDUCTION_LIMIT,
    QBT_DIVIDENDS_AND_INVESTMENT_INCOME,
    QBT_ELECTION_DEDUCTION,
    QBT_ELECTION_ELIGIBLE_AMOUNT,
    QBT_ELECTION_IS_QBT,
    QBT_EXPLORATION_EXPENSES_AT_HALF,
    QBT_GAINS_ARE_QSBCS_OR_QFFP,
    QBT_HAS_INVESTMENT_EXPENSES,
    QBT_INVESTMENT_EXPENSES,
    QBT_INVESTMENT_INCOME,
    QBT_MAXIMUM_DEDUCTION,
    QBT_NET_CAPITAL_LOSSES_REMAINING,
    QBT_NET_INVESTMENT_LOSS,
    QBT_NET_INVESTMENT_LOSS_REDUCTION,
    QBT_NET_RENTAL_INCOME,
    QBT_NET_RENTAL_LOSS,
    QBT_OTHER_INVESTMENT_EXPENSES,
    QBT_OTHER_PROPERTY_INCOME,
    QBT_PARTNERSHIP_LOSSES,
    QBT_PERCENTAGE_ALLOCATED,
    QBT_PRIOR_YEARS_CLAIMS,
    QBT_RECOVERY_OF_EXPLORATION_EXPENSES,
    QBT_REDUCTION_AMOUNT,
    QBT_REDUCTIONS_FROM_LOSSES,
    QBT_TAXABLE_AMOUNT_ALLOCATED,
    QBT_TAXABLE_CAPITAL_GAINS,
    QBT_TAXABLE_GAINS_LIMIT,
    QBT_TAXABLE_GAINS_NOT_LIMITED,
    QBT_TAXABLE_GAINS_RELATED_TO_DEDUCTION,
    QBT_TOTAL_CAPITAL_GAINS,
    QCC_ELECTION_DEDUCTION,
    QSBCS_QFFP_TAXABLE_GAINS_RELATED_TO_DEDUCTION,
    TAXABLE_CAPITAL_GAINS,
    TAXABLE_DIVIDENDS,
)

INPUTS = frozenset(
    {
        "ca/qbt_election_eligible_amount",
        "ca/qbt_percentage_allocated",
        "ca/qbt_prior_years_claims",
        "ca/qbt_capital_gains",
        "ca/qbt_2024_reserve",
        "ca/qbt_2025_reserve",
        "ca/qbt_has_investment_expenses",
        "ca/qbt_deduction_claimed",
        "ca/qbt_election_is_qbt",
        "ca/qbt_gains_are_qsbcs_or_qffp",
        "ca/qbt_partnership_losses",
        "ca/qbt_other_investment_expenses",
        "ca/qbt_other_property_income",
    }
)

# Part 5's totals (A 17211, B 17212, C 17213, D 17215, E 17216, F 17217, G 17218; C, F and G are
# lines 16, 41 and 42) and Part 4 line 32, which nothing else on the return reads.
OUTPUTS = frozenset(
    {
        "ca/qbt_allocation_total",
        "ca/qcc_election_deduction",
        "ca/qbt_election_deduction",
        "ca/qbt_taxable_capital_gains",
        "ca/qbt_taxable_gains_related_to_deduction",
        "ca/qsbcs_qffp_taxable_gains_related_to_deduction",
        "ca/qbt_abil_reduction",
        "ca/qbt_net_investment_loss_reduction",
    }
)

STEPS = {
    # Form T2048 Part 2 line 3 "Line 1 multiplied by the percentage from line 2" (line 1 "Total
    # eligible amount for the joint election (maximum of $10 million per election)", line 2
    # "Percentage allocated to you"): the percentage is entered as printed (50 for 50%), so the
    # product is `ca/apply_percentage`.
    CapabilitySelection(
        name="ca/apply_percentage",
        params={"rounding": "ca/qbt_amount_allocated_rounding"},
        consumes={
            "amount": "ca/qbt_election_eligible_amount",
            "percentage": "ca/qbt_percentage_allocated",
        },
        produces={"output": "ca/qbt_amount_allocated"},
    ),
    # Part 2 line 4 "Inclusion rate × 50%" and line 5 "Line 3 multiplied by the percentage from line
    # 4".
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/qbt_election_inclusion_rate"},
        consumes={
            "base": "ca/qbt_amount_allocated",
        },
        produces={"output": "ca/qbt_taxable_amount_allocated"},
    ),
    # Part 2 line 7 "Capital gains deduction available from your election: line 5 minus line 6"
    # (line 6 "Capital gains deduction claimed in prior years at line 25395 of your return for this
    # disposition, if any"). The form prints no floor; a line 6 above line 5 is floored at 0 here,
    # an assumption to be confirmed.
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/qbt_taxable_amount_allocated",
            "less": "ca/qbt_prior_years_claims",
        },
        produces={"output": "ca/qbt_deduction_available"},
    ),
    # Part 3 line 11 "Line 9 plus line 10" (line 9 "Capital gains for the QBT or QCC that occurred
    # in the current year reported on Schedule 3", line 10 "Amount of 2024 reserve claimed for the
    # QBT or QCC, if any"). Line 8 "Taxable capital gains from line 12700 of your return" is the
    # artifact ca/taxable_capital_gains, read directly; line 12 "Amount from line 11 of the previous
    # page" is line 11.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/qbt_capital_gains",
                "ca/qbt_2024_reserve",
            ),
        },
        produces={"output": "ca/qbt_capital_gains_with_2024_reserve"},
    ),
    # Part 3 line 14 "Total capital gains for the QBT or QCC: line 12 minus line 13" (line 13
    # "Amount of 2025 reserve claimed for the QBT or QCC, if any"). The form prints no floor; a line
    # 13 above line 12 is floored at 0 here, an assumption to be confirmed.
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/qbt_capital_gains_with_2024_reserve",
            "less": "ca/qbt_2025_reserve",
        },
        produces={"output": "ca/qbt_total_capital_gains"},
    ),
    # Part 3 line 15 "Inclusion rate × 50%" and line 16 "Taxable capital gains for the QBT or QCC
    # only: line 14 multiplied by the inclusion rate on line 15" (also Part 5 C, total 17213).
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/qbt_gains_inclusion_rate"},
        consumes={
            "base": "ca/qbt_total_capital_gains",
        },
        produces={"output": "ca/qbt_taxable_capital_gains"},
    ),
    # Part 3 line 17 "Enter whichever is less: amount from line 8 or line 16."
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={
            "amounts": (
                "ca/taxable_capital_gains",
                "ca/qbt_taxable_capital_gains",
            ),
        },
        produces={"output": "ca/qbt_taxable_gains_limit"},
    ),
    # Part 3 line 21 "Line 19 minus line 20 (if negative enter "0")" (line 19 "Amount from line 8",
    # line 20 "Amount from line 17"). Chart A line 18 "Line 16 minus line 17" (line 16 "Line 8 of
    # Part 3", line 17 "Line 17 of Part 3") is the same figure, so Chart A reads this artifact.
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/taxable_capital_gains",
            "less": "ca/qbt_taxable_gains_limit",
        },
        produces={"output": "ca/qbt_taxable_gains_not_limited"},
    ),
    # Part 3 line 22 "Line 18 minus line 21 (if negative enter "0")" (line 18 "Net capital losses of
    # other years (line 25300 of your return)").
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/net_capital_losses_of_other_years",
            "less": "ca/qbt_taxable_gains_not_limited",
        },
        produces={"output": "ca/qbt_net_capital_losses_remaining"},
    ),
    # Part 3 line 24 "Net investment loss for the year: If you have investment expenses in 2025,
    # complete Chart A on page 4 and enter the amount from line 20 of Chart A. Otherwise, enter
    # "0"." The yes/no answer is a 0 or 1 input; the loss times that count is the loss or 0. Line 23
    # "Allowable business investment loss (ABIL) for the year (line 21700 of your return)" is the
    # artifact ca/allowable_business_investment_loss, read directly.
    CapabilitySelection(
        name="core/times_count",
        params={},
        consumes={
            "amount": "ca/qbt_chart_a_net_investment_loss",
            "count": "ca/qbt_has_investment_expenses",
        },
        produces={"output": "ca/qbt_net_investment_loss"},
    ),
    # Part 3 line 25 "Add lines 22, 23, and 24".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/qbt_net_capital_losses_remaining",
                "ca/allowable_business_investment_loss",
                "ca/qbt_net_investment_loss",
            ),
        },
        produces={"output": "ca/qbt_reductions_from_losses"},
    ),
    # Part 3 line 26 "Line 17 minus line 25". The form prints no floor; a result below 0 is floored
    # at 0 here (nothing can be claimed), an assumption to be confirmed.
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/qbt_taxable_gains_limit",
            "less": "ca/qbt_reductions_from_losses",
        },
        produces={"output": "ca/qbt_deduction_limit"},
    ),
    # Part 3 line 27 "Enter whichever is less: amount from line 7 or line 26." (the most that can be
    # claimed).
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={
            "amounts": (
                "ca/qbt_deduction_available",
                "ca/qbt_deduction_limit",
            ),
        },
        produces={"output": "ca/qbt_maximum_deduction"},
    ),
    # Part 3 line 27 "Enter all or part of the amount you want to claim on line 25395 of your
    # return. Eligible capital gains deduction for QBT or QCC" and T1 line 64 and line 25395: the
    # amount the filer chooses, an input, which may not exceed the line above.
    CapabilitySelection(
        name="core/at_most",
        params={},
        consumes={
            "amount": "ca/qbt_deduction_claimed",
            "bound": "ca/qbt_maximum_deduction",
        },
        produces={"output": "ca/qbt_capital_gains_deduction"},
    ),
    # Part 4 line 28 "Enter whichever is less: amount from line 7 or line 17."
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={
            "amounts": (
                "ca/qbt_deduction_available",
                "ca/qbt_taxable_gains_limit",
            ),
        },
        produces={"output": "ca/qbt_deduction_base"},
    ),
    # Part 4 line 30 "Line 28 minus line 29" (line 29 "Amount from line 27") "Reduction amount".
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/qbt_deduction_base",
            "less": "ca/qbt_capital_gains_deduction",
        },
        produces={"output": "ca/qbt_reduction_amount"},
    ),
    # Part 4 line 32 "Line 30 plus line 31" (line 31 "Amount claimed on line 25395 of your return
    # for this QBT or QCC").
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/qbt_reduction_amount",
                "ca/qbt_capital_gains_deduction",
            ),
        },
        produces={"output": "ca/qbt_allocation_total"},
    ),
    # Part 4 line 35 "Line 33 plus line 34" (line 33 "Amount from line 23", line 34 "Amount from
    # line 24").
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/allowable_business_investment_loss",
                "ca/qbt_net_investment_loss",
            ),
        },
        produces={"output": "ca/qbt_abil_and_net_investment_loss"},
    ),
    # Part 4 line 36 "Enter whichever is less: amount from line 30 or line 35. (if the result is
    # "0", enter "0" on lines 41 and 42 and continue to Part 5)".
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={
            "amounts": (
                "ca/qbt_reduction_amount",
                "ca/qbt_abil_and_net_investment_loss",
            ),
        },
        produces={"output": "ca/qbt_allocation_limit"},
    ),
    # Part 4 line 41 "Line 39 multiplied by line 40" "ABIL reduction" (line 37 "Amount from line
    # 36", line 38 "Amount from line 35", line 39 "Line 37 divided by line 38", line 40 "Amount from
    # line 33"): line 40 times line 37 over line 38, 0 when line 38 is 0 ("if the result is "0",
    # enter "0" on lines 41 and 42").
    CapabilitySelection(
        name="ca/apply_ratio_or_zero",
        params={"rounding": "ca/qbt_abil_reduction_rounding"},
        consumes={
            "amount": "ca/allowable_business_investment_loss",
            "numerator": "ca/qbt_allocation_limit",
            "denominator": "ca/qbt_abil_and_net_investment_loss",
        },
        produces={"output": "ca/qbt_abil_reduction"},
    ),
    # Part 4 line 42 "Line 36 minus line 41" "Net investment loss reduction".
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/qbt_allocation_limit",
            "less": "ca/qbt_abil_reduction",
        },
        produces={"output": "ca/qbt_net_investment_loss_reduction"},
    ),
    # Part 5 B "Deduction available from QBT election: Amount from line 7 if the election is for a
    # QBT" (Total 17212): line 7 times the 0 or 1 answer.
    CapabilitySelection(
        name="core/times_count",
        params={},
        consumes={
            "amount": "ca/qbt_deduction_available",
            "count": "ca/qbt_election_is_qbt",
        },
        produces={"output": "ca/qbt_election_deduction"},
    ),
    # Part 5 A "Deduction available from QCC election: Amount from line 7 if the election is for a
    # QCC" (Total 17211): the part of line 7 that B did not take.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/qbt_deduction_available",
            "less": "ca/qbt_election_deduction",
        },
        produces={"output": "ca/qcc_election_deduction"},
    ),
    # Part 5 D "Portion of the taxable capital gains related to a capital gain deduction for QBT or
    # QCC claimed: Amount from lines 31 and 36" (Total 17215). C "Taxable capital gains for QBT or
    # QCC: Amount from line 16" (Total 17213) is the artifact of line 16; F (17217) is line 41 and G
    # (17218) is line 42.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/qbt_capital_gains_deduction",
                "ca/qbt_allocation_limit",
            ),
        },
        produces={"output": "ca/qbt_taxable_gains_related_to_deduction"},
    ),
    # Part 5 E "Portion of QSBCS or QFFP taxable capital gains related to a capital gain deduction
    # for QBT or QCC claimed: Amounts from line 31 and 36 if gains are from a qualified small
    # business corporation shares (QSBCS) or qualified farm or fishing property (QFFP)" (Total
    # 17216): D times the 0 or 1 answer.
    CapabilitySelection(
        name="core/times_count",
        params={},
        consumes={
            "amount": "ca/qbt_taxable_gains_related_to_deduction",
            "count": "ca/qbt_gains_are_qsbcs_or_qffp",
        },
        produces={"output": "ca/qsbcs_qffp_taxable_gains_related_to_deduction"},
    ),
    # Chart A line 12 "Net rental income, including recaptured capital cost allowance (line 12600)":
    # the positive part of the signed net rental income.
    CapabilitySelection(
        name="core/sum_not_below_zero",
        params={},
        consumes={
            "parts": ("ca/net_rental_income",),
        },
        produces={"output": "ca/qbt_net_rental_income"},
    ),
    # Chart A line 2 "Net rental losses (line 12600)": the negative part of the signed net rental
    # income, as a positive amount.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/qbt_net_rental_income",
            "less": "ca/net_rental_income",
        },
        produces={"output": "ca/qbt_net_rental_loss"},
    ),
    # Chart A line 5 "50% of exploration and development expenses (line 22400)". Line 1 "Carrying
    # charges and interest expenses (line 22100)" and line 4 "Limited partnership losses of other
    # years after 1985 (line 25100)" are read from their artifacts; line 3 "Limited or non-active
    # partnership losses (line 12200) other than allowable capital losses" and line 6 "Any other
    # investment expenses claimed in 2025 to earn property income" are inputs.
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/qbt_exploration_expenses_rate"},
        consumes={
            "base": "ca/exploration_and_development_expenses",
        },
        produces={"output": "ca/qbt_exploration_expenses_at_half"},
    ),
    # Chart A line 9 "Line 7 minus line 8 (if negative enter "0")" (line 7 "Line 18 of Part 3", line
    # 8 "Line 22 of Part 3").
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/net_capital_losses_of_other_years",
            "less": "ca/qbt_net_capital_losses_remaining",
        },
        produces={"output": "ca/qbt_chart_a_net_capital_losses_used"},
    ),
    # Chart A line 10 "Investment expenses: add lines 1 to 6, and line 9".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/carrying_charges_interest_expenses_and_other_expenses",
                "ca/qbt_net_rental_loss",
                "ca/qbt_partnership_losses",
                "ca/limited_partnership_losses_of_other_years",
                "ca/qbt_exploration_expenses_at_half",
                "ca/qbt_other_investment_expenses",
                "ca/qbt_chart_a_net_capital_losses_used",
            ),
        },
        produces={"output": "ca/qbt_investment_expenses"},
    ),
    # Chart A line 11 "Investment income (lines 12000 and 12100)".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/taxable_dividends",
                "ca/interest_and_other_investment_income",
            ),
        },
        produces={"output": "ca/qbt_dividends_and_investment_income"},
    ),
    # Chart A line 15 "50% of income from the recovery of exploration and development expenses (line
    # 13000)".
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/qbt_exploration_recovery_rate"},
        consumes={
            "base": "ca/other_income",
        },
        produces={"output": "ca/qbt_recovery_of_exploration_expenses"},
    ),
    # Chart A line 19 "Investment income: add lines 11 to 15, and line 18" (line 13 "Net income from
    # limited or non-active partnership (line 12200) other than taxable capital gains"; line 14 "Any
    # other property income reported in 2025" is an input).
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/qbt_dividends_and_investment_income",
                "ca/qbt_net_rental_income",
                "ca/net_partnership_income",
                "ca/qbt_other_property_income",
                "ca/qbt_recovery_of_exploration_expenses",
                "ca/qbt_taxable_gains_not_limited",
            ),
        },
        produces={"output": "ca/qbt_investment_income"},
    ),
    # Chart A line 20 "Line 10 minus line 19 (if negative enter "0")" "Net investment losses for the
    # year".
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/qbt_investment_expenses",
            "less": "ca/qbt_investment_income",
        },
        produces={"output": "ca/qbt_chart_a_net_investment_loss"},
    ),
}

WIRING = {
    (
        ApplyPercentage,
        frozenset({QBT_ELECTION_ELIGIBLE_AMOUNT, QBT_PERCENTAGE_ALLOCATED}),
        frozenset({QBT_AMOUNT_ALLOCATED}),
    ),
    (
        ApplyRate,
        frozenset({QBT_AMOUNT_ALLOCATED}),
        frozenset({QBT_TAXABLE_AMOUNT_ALLOCATED}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({QBT_TAXABLE_AMOUNT_ALLOCATED, QBT_PRIOR_YEARS_CLAIMS}),
        frozenset({QBT_DEDUCTION_AVAILABLE}),
    ),
    (
        Sum,
        frozenset({QBT_CAPITAL_GAINS, QBT_2024_RESERVE}),
        frozenset({QBT_CAPITAL_GAINS_WITH_2024_RESERVE}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({QBT_CAPITAL_GAINS_WITH_2024_RESERVE, QBT_2025_RESERVE}),
        frozenset({QBT_TOTAL_CAPITAL_GAINS}),
    ),
    (
        ApplyRate,
        frozenset({QBT_TOTAL_CAPITAL_GAINS}),
        frozenset({QBT_TAXABLE_CAPITAL_GAINS}),
    ),
    (
        LesserOf,
        frozenset({TAXABLE_CAPITAL_GAINS, QBT_TAXABLE_CAPITAL_GAINS}),
        frozenset({QBT_TAXABLE_GAINS_LIMIT}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({TAXABLE_CAPITAL_GAINS, QBT_TAXABLE_GAINS_LIMIT}),
        frozenset({QBT_TAXABLE_GAINS_NOT_LIMITED}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({NET_CAPITAL_LOSSES_OF_OTHER_YEARS, QBT_TAXABLE_GAINS_NOT_LIMITED}),
        frozenset({QBT_NET_CAPITAL_LOSSES_REMAINING}),
    ),
    (
        TimesCount,
        frozenset({QBT_CHART_A_NET_INVESTMENT_LOSS, QBT_HAS_INVESTMENT_EXPENSES}),
        frozenset({QBT_NET_INVESTMENT_LOSS}),
    ),
    (
        Sum,
        frozenset(
            {
                QBT_NET_CAPITAL_LOSSES_REMAINING,
                ALLOWABLE_BUSINESS_INVESTMENT_LOSS,
                QBT_NET_INVESTMENT_LOSS,
            }
        ),
        frozenset({QBT_REDUCTIONS_FROM_LOSSES}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({QBT_TAXABLE_GAINS_LIMIT, QBT_REDUCTIONS_FROM_LOSSES}),
        frozenset({QBT_DEDUCTION_LIMIT}),
    ),
    (
        LesserOf,
        frozenset({QBT_DEDUCTION_AVAILABLE, QBT_DEDUCTION_LIMIT}),
        frozenset({QBT_MAXIMUM_DEDUCTION}),
    ),
    (
        AtMost,
        frozenset({QBT_DEDUCTION_CLAIMED, QBT_MAXIMUM_DEDUCTION}),
        frozenset({QBT_CAPITAL_GAINS_DEDUCTION}),
    ),
    (
        LesserOf,
        frozenset({QBT_DEDUCTION_AVAILABLE, QBT_TAXABLE_GAINS_LIMIT}),
        frozenset({QBT_DEDUCTION_BASE}),
    ),
    (
        Subtract,
        frozenset({QBT_DEDUCTION_BASE, QBT_CAPITAL_GAINS_DEDUCTION}),
        frozenset({QBT_REDUCTION_AMOUNT}),
    ),
    (
        Sum,
        frozenset({QBT_REDUCTION_AMOUNT, QBT_CAPITAL_GAINS_DEDUCTION}),
        frozenset({QBT_ALLOCATION_TOTAL}),
    ),
    (
        Sum,
        frozenset({ALLOWABLE_BUSINESS_INVESTMENT_LOSS, QBT_NET_INVESTMENT_LOSS}),
        frozenset({QBT_ABIL_AND_NET_INVESTMENT_LOSS}),
    ),
    (
        LesserOf,
        frozenset({QBT_REDUCTION_AMOUNT, QBT_ABIL_AND_NET_INVESTMENT_LOSS}),
        frozenset({QBT_ALLOCATION_LIMIT}),
    ),
    (
        ApplyRatioOrZero,
        frozenset(
            {
                ALLOWABLE_BUSINESS_INVESTMENT_LOSS,
                QBT_ALLOCATION_LIMIT,
                QBT_ABIL_AND_NET_INVESTMENT_LOSS,
            }
        ),
        frozenset({QBT_ABIL_REDUCTION}),
    ),
    (
        Subtract,
        frozenset({QBT_ALLOCATION_LIMIT, QBT_ABIL_REDUCTION}),
        frozenset({QBT_NET_INVESTMENT_LOSS_REDUCTION}),
    ),
    (
        TimesCount,
        frozenset({QBT_DEDUCTION_AVAILABLE, QBT_ELECTION_IS_QBT}),
        frozenset({QBT_ELECTION_DEDUCTION}),
    ),
    (
        Subtract,
        frozenset({QBT_DEDUCTION_AVAILABLE, QBT_ELECTION_DEDUCTION}),
        frozenset({QCC_ELECTION_DEDUCTION}),
    ),
    (
        Sum,
        frozenset({QBT_CAPITAL_GAINS_DEDUCTION, QBT_ALLOCATION_LIMIT}),
        frozenset({QBT_TAXABLE_GAINS_RELATED_TO_DEDUCTION}),
    ),
    (
        TimesCount,
        frozenset({QBT_TAXABLE_GAINS_RELATED_TO_DEDUCTION, QBT_GAINS_ARE_QSBCS_OR_QFFP}),
        frozenset({QSBCS_QFFP_TAXABLE_GAINS_RELATED_TO_DEDUCTION}),
    ),
    (
        SumNotBelowZero,
        frozenset({NET_RENTAL_INCOME}),
        frozenset({QBT_NET_RENTAL_INCOME}),
    ),
    (
        Subtract,
        frozenset({QBT_NET_RENTAL_INCOME, NET_RENTAL_INCOME}),
        frozenset({QBT_NET_RENTAL_LOSS}),
    ),
    (
        ApplyRate,
        frozenset({EXPLORATION_AND_DEVELOPMENT_EXPENSES}),
        frozenset({QBT_EXPLORATION_EXPENSES_AT_HALF}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({NET_CAPITAL_LOSSES_OF_OTHER_YEARS, QBT_NET_CAPITAL_LOSSES_REMAINING}),
        frozenset({QBT_CHART_A_NET_CAPITAL_LOSSES_USED}),
    ),
    (
        Sum,
        frozenset(
            {
                CARRYING_CHARGES_INTEREST_EXPENSES_AND_OTHER_EXPENSES,
                QBT_NET_RENTAL_LOSS,
                QBT_PARTNERSHIP_LOSSES,
                LIMITED_PARTNERSHIP_LOSSES_OF_OTHER_YEARS,
                QBT_EXPLORATION_EXPENSES_AT_HALF,
                QBT_OTHER_INVESTMENT_EXPENSES,
                QBT_CHART_A_NET_CAPITAL_LOSSES_USED,
            }
        ),
        frozenset({QBT_INVESTMENT_EXPENSES}),
    ),
    (
        Sum,
        frozenset({TAXABLE_DIVIDENDS, INTEREST_AND_OTHER_INVESTMENT_INCOME}),
        frozenset({QBT_DIVIDENDS_AND_INVESTMENT_INCOME}),
    ),
    (
        ApplyRate,
        frozenset({OTHER_INCOME}),
        frozenset({QBT_RECOVERY_OF_EXPLORATION_EXPENSES}),
    ),
    (
        Sum,
        frozenset(
            {
                QBT_DIVIDENDS_AND_INVESTMENT_INCOME,
                QBT_NET_RENTAL_INCOME,
                NET_PARTNERSHIP_INCOME,
                QBT_OTHER_PROPERTY_INCOME,
                QBT_RECOVERY_OF_EXPLORATION_EXPENSES,
                QBT_TAXABLE_GAINS_NOT_LIMITED,
            }
        ),
        frozenset({QBT_INVESTMENT_INCOME}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({QBT_INVESTMENT_EXPENSES, QBT_INVESTMENT_INCOME}),
        frozenset({QBT_CHART_A_NET_INVESTMENT_LOSS}),
    ),
}
