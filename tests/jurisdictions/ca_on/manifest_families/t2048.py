"""The CA-ON manifest entries of Form T2048 (line 25395), Parts 2 to 5 and Chart A (see
`test_manifest.py` and `test_manifest_t2048.py`).

T2048 is the form `ca/t2048`, run once for each disposition of `ca/t2048_dispositions`, whose fields
are the T2048 inputs (`FORM_INPUTS`). Its selections are `FORM_STEPS`: the 34 of Parts 2 to 5 and
Chart A, and 54 copies of the return's steps that compute the 11 figures the form reads (the
return keeps its own). The form exports the nine artifacts the return reads or outputs
(`FORM_EXPORTS`), and the return re-produces each of them with `core/record_total` over the form's
derived kind `ca/t2048.<name>` (`STEPS`). `IMPORTS` are the other forms' exports the copies read.
Line 25395 is added to line 25700 in the `taxable_income` family.
"""

from __future__ import annotations

from app.domain.capabilities.apply_fraction import ApplyFraction
from app.domain.capabilities.apply_rate import ApplyRate
from app.domain.capabilities.at_most import AtMost
from app.domain.capabilities.credit_amount import CreditAmount
from app.domain.capabilities.lesser_of import LesserOf
from app.domain.capabilities.record_total import RecordTotal
from app.domain.capabilities.subtract import Subtract
from app.domain.capabilities.subtract_not_below_zero import SubtractNotBelowZero
from app.domain.capabilities.sum import Sum
from app.domain.capabilities.sum_not_below_zero import SumNotBelowZero
from app.domain.capabilities.times_count import TimesCount
from app.domain.manifest import CapabilitySelection
from app.domain.record_list import RecordListKind
from app.jurisdictions.ca.capabilities.apply_percentage import ApplyPercentage
from app.jurisdictions.ca.capabilities.apply_ratio_or_zero import ApplyRatioOrZero
from app.jurisdictions.ca.capabilities.disposition_gains import DispositionGains
from app.jurisdictions.ca.capabilities.disposition_gains_only import DispositionGainsOnly
from app.jurisdictions.ca.capabilities.lesser_of_with_maximum import LesserOfWithMaximum
from app.jurisdictions.ca.capabilities.principal_residence_gain import PrincipalResidenceGain
from app.jurisdictions.ca.catalog import (
    ADJUSTED_GROSS_CAPITAL_LOSSES_1985_TO_1987,
    ADJUSTED_GROSS_CAPITAL_LOSSES_1988_AND_1989,
    ADJUSTED_GROSS_CAPITAL_LOSSES_1990_TO_1999,
    ADJUSTED_GROSS_CAPITAL_LOSSES_2000,
    ADJUSTED_GROSS_CAPITAL_LOSSES_2001_TO_2024,
    ADJUSTED_GROSS_CAPITAL_LOSSES_BEFORE_MAY_23_1985,
    ADJUSTED_NET_CAPITAL_LOSSES_APPLIED,
    ALLOWABLE_BUSINESS_INVESTMENT_LOSS,
    BOND_DISPOSITIONS,
    BOND_GAIN_OR_LOSS,
    BUSINESS_INVESTMENT_LOSS,
    BUSINESS_INVESTMENT_LOSS_AFTER_REDUCTION,
    BUSINESS_INVESTMENT_LOSS_REDUCTION,
    BUSINESS_INVESTMENT_LOSS_REDUCTION_AVAILABLE,
    CAPITAL_GAIN,
    CAPITAL_GAINS_AFTER_DEFERRAL,
    CAPITAL_GAINS_BEFORE_INVESTMENT_LOSS_REDUCTION,
    CAPITAL_GAINS_BEFORE_RESERVES,
    CAPITAL_GAINS_DEDUCTIONS_1985_TO_1987,
    CAPITAL_GAINS_DEDUCTIONS_1988_AND_1989_ELIGIBLE_CAPITAL_PROPERTY,
    CAPITAL_GAINS_DEDUCTIONS_1988_AND_1989_OTHER_THAN_ELIGIBLE_CAPITAL_PROPERTY,
    CAPITAL_GAINS_DEDUCTIONS_1990_TO_1999,
    CAPITAL_GAINS_DEDUCTIONS_2000,
    CAPITAL_GAINS_DEDUCTIONS_2001_TO_2024,
    CAPITAL_GAINS_DEDUCTIONS_CLAIMED_1985_TO_2024,
    CAPITAL_GAINS_DEFERRAL,
    CAPITAL_GAINS_OF_QUALIFIED_AND_OTHER_PROPERTIES,
    CAPITAL_GAINS_RESERVES,
    CARRYING_CHARGES_INTEREST_EXPENSES_AND_OTHER_EXPENSES,
    CRYPTO_ASSET_DISPOSITIONS,
    CRYPTO_ASSET_GAIN_OR_LOSS,
    DIVIDENDS_WITHOUT_A_SLIP_GROSSED_UP,
    ELIGIBLE_DIVIDENDS_GROSSED_UP,
    ELIGIBLE_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP,
    EXPLORATION_AND_DEVELOPMENT_EXPENSES,
    FOREIGN_INVESTMENT_INCOME,
    INCLUDED_CAPITAL_GAIN,
    INTEREST_AND_OTHER_INVESTMENT_INCOME,
    INVESTMENT_INCOME_BEFORE_PRIOR_YEARS,
    INVESTMENT_INCOME_CREDITED_NOT_RECEIVED,
    INVESTMENT_INCOME_REPORTED_IN_PREVIOUS_YEARS,
    INVESTMENT_INCOME_WITHOUT_A_SLIP,
    INVESTMENT_ROYALTIES,
    LIMITED_PARTNERSHIP_LOSSES_OF_OTHER_YEARS,
    LISTED_PERSONAL_PROPERTY_DISPOSITIONS,
    LISTED_PERSONAL_PROPERTY_GAIN_OR_LOSS,
    LISTED_PERSONAL_PROPERTY_NET_GAIN,
    NET_CAPITAL_LOSS_NUMERATOR_ONE_2000,
    NET_CAPITAL_LOSS_TWICE_IR_2000,
    NET_CAPITAL_LOSSES_ADDITIONAL_DEDUCTION,
    NET_CAPITAL_LOSSES_AVAILABLE_TO_CLAIM,
    NET_CAPITAL_LOSSES_BEFORE_MAY_23_1985,
    NET_CAPITAL_LOSSES_CLAIMED,
    NET_CAPITAL_LOSSES_OF_OTHER_YEARS,
    NET_PARTNERSHIP_INCOME,
    NET_RENTAL_INCOME,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_1994,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_2024,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1994_TO_1996,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1997_TO_1999,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2000,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2001_TO_2023,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2024,
    OTHER_DIVIDENDS_GROSSED_UP,
    OTHER_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP,
    OTHER_FORECLOSURE_DISPOSITIONS,
    OTHER_FORECLOSURE_GAIN_OR_LOSS,
    OTHER_INCOME,
    PARTNERSHIP_GAINS_AT_FULL_INCLUSION,
    PERSONAL_USE_PROPERTY_DISPOSITIONS,
    PERSONAL_USE_PROPERTY_GAIN,
    PERSONAL_USE_PROPERTY_GAIN_ROWS,
    PRE_1986_CAPITAL_LOSS_BALANCE,
    PRE_1986_DEDUCTIONS_1988_AND_1989,
    PRE_1986_DEDUCTIONS_1990_TO_1999,
    PRE_1986_DEDUCTIONS_2000,
    PRE_1986_DEDUCTIONS_2001_TO_2024,
    PRE_1986_DEDUCTIONS_ADJUSTED_1988_AND_1989,
    PRE_1986_DEDUCTIONS_ADJUSTED_1990_TO_1999,
    PRE_1986_DEDUCTIONS_ADJUSTED_2000,
    PRE_1986_DEDUCTIONS_BEFORE_1988,
    PRE_1986_DEDUCTIONS_TOTAL,
    PRINCIPAL_RESIDENCE_GAIN,
    PRINCIPAL_RESIDENCE_PROPERTIES,
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
    QFFP_DISPOSITIONS,
    QFFP_FORECLOSURE_DISPOSITIONS,
    QFFP_FORECLOSURE_GAIN_OR_LOSS,
    QFFP_GAIN_OR_LOSS,
    QSBCS_DISPOSITIONS,
    QSBCS_GAIN_OR_LOSS,
    QSBCS_QFFP_TAXABLE_GAINS_RELATED_TO_DEDUCTION,
    REAL_ESTATE_DISPOSITIONS,
    REAL_ESTATE_GAIN_OR_LOSS,
    SHARE_DISPOSITIONS,
    SHARE_GAIN_OR_LOSS,
    SLIP_CAPITAL_GAINS_OR_LOSSES,
    SLIP_TAXABLE_DIVIDENDS,
    T3_CAPITAL_GAINS_OR_LOSSES,
    T3_INVESTMENT_INCOME,
    T3_TAXABLE_DIVIDENDS,
    T4PS_TAXABLE_DIVIDENDS,
    T5_INVESTMENT_INCOME,
    T5_TAXABLE_DIVIDENDS,
    T657_INCLUSION_RATE_2000,
    T5013_INVESTMENT_INCOME,
    T5013_TAXABLE_DIVIDENDS,
    TAX_REFUND_INTEREST,
    TAXABLE_CAPITAL_GAINS,
    TAXABLE_DIVIDENDS,
    TOTAL_ADJUSTED_NET_CAPITAL_LOSSES,
    TOTAL_CARRYING_CHARGES,
    TOTAL_INTEREST_EXPENSES,
    TOTAL_OTHER_EXPENSES,
    UNAPPLIED_ADJUSTED_NET_CAPITAL_LOSSES,
    UNAPPLIED_LISTED_PERSONAL_PROPERTY_LOSSES,
    UNAPPLIED_NET_CAPITAL_LOSSES_1985_TO_1987,
    UNAPPLIED_NET_CAPITAL_LOSSES_1988_AND_1989,
    UNAPPLIED_NET_CAPITAL_LOSSES_1990_TO_1999,
    UNAPPLIED_NET_CAPITAL_LOSSES_2000,
    UNAPPLIED_NET_CAPITAL_LOSSES_2001_TO_2024,
)
from tests.jurisdictions.ca_on.manifest_families.t776 import NET_RENTAL_INCOME_PER_STATEMENT

# Each export of the form totals over the dispositions: one record of the form's per-disposition
# list for each, read by the return as `ca/t2048.<name>`.
ALLOCATION_TOTAL_PER_DISPOSITION = RecordListKind(
    "ca/t2048.qbt_allocation_total", fields=(QBT_ALLOCATION_TOTAL,)
)
QCC_ELECTION_DEDUCTION_PER_DISPOSITION = RecordListKind(
    "ca/t2048.qcc_election_deduction", fields=(QCC_ELECTION_DEDUCTION,)
)
QBT_ELECTION_DEDUCTION_PER_DISPOSITION = RecordListKind(
    "ca/t2048.qbt_election_deduction", fields=(QBT_ELECTION_DEDUCTION,)
)
TAXABLE_CAPITAL_GAINS_PER_DISPOSITION = RecordListKind(
    "ca/t2048.qbt_taxable_capital_gains", fields=(QBT_TAXABLE_CAPITAL_GAINS,)
)
TAXABLE_GAINS_RELATED_PER_DISPOSITION = RecordListKind(
    "ca/t2048.qbt_taxable_gains_related_to_deduction",
    fields=(QBT_TAXABLE_GAINS_RELATED_TO_DEDUCTION,),
)
QSBCS_QFFP_GAINS_RELATED_PER_DISPOSITION = RecordListKind(
    "ca/t2048.qsbcs_qffp_taxable_gains_related_to_deduction",
    fields=(QSBCS_QFFP_TAXABLE_GAINS_RELATED_TO_DEDUCTION,),
)
ABIL_REDUCTION_PER_DISPOSITION = RecordListKind(
    "ca/t2048.qbt_abil_reduction", fields=(QBT_ABIL_REDUCTION,)
)
NET_INVESTMENT_LOSS_REDUCTION_PER_DISPOSITION = RecordListKind(
    "ca/t2048.qbt_net_investment_loss_reduction", fields=(QBT_NET_INVESTMENT_LOSS_REDUCTION,)
)
CAPITAL_GAINS_DEDUCTION_PER_DISPOSITION = RecordListKind(
    "ca/t2048.qbt_capital_gains_deduction", fields=(QBT_CAPITAL_GAINS_DEDUCTION,)
)

FORM_INPUTS = frozenset(
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


OWN_STEPS = {
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

# Copies of the 54 return steps
COPIED_STEPS = {
    # Copies of the 54 return steps the form's 11 figures need (Umar's rule: a form carries its own
    # copies and reads manifest inputs and other forms' exports, never the return). The return keeps
    # its originals.
    CapabilitySelection(
        name="ca/disposition_gains",
        params={},
        consumes={"dispositions": "ca/qsbcs_dispositions"},
        produces={"output": "ca/qsbcs_gain_or_loss"},
    ),
    CapabilitySelection(
        name="ca/disposition_gains",
        params={},
        consumes={"dispositions": "ca/qffp_dispositions"},
        produces={"output": "ca/qffp_gain_or_loss"},
    ),
    CapabilitySelection(
        name="ca/disposition_gains",
        params={},
        consumes={"dispositions": "ca/qffp_foreclosure_dispositions"},
        produces={"output": "ca/qffp_foreclosure_gain_or_loss"},
    ),
    CapabilitySelection(
        name="ca/disposition_gains",
        params={},
        consumes={"dispositions": "ca/share_dispositions"},
        produces={"output": "ca/share_gain_or_loss"},
    ),
    CapabilitySelection(
        name="ca/disposition_gains",
        params={},
        consumes={"dispositions": "ca/real_estate_dispositions"},
        produces={"output": "ca/real_estate_gain_or_loss"},
    ),
    CapabilitySelection(
        name="ca/disposition_gains",
        params={},
        consumes={"dispositions": "ca/bond_dispositions"},
        produces={"output": "ca/bond_gain_or_loss"},
    ),
    CapabilitySelection(
        name="ca/disposition_gains",
        params={},
        consumes={"dispositions": "ca/crypto_asset_dispositions"},
        produces={"output": "ca/crypto_asset_gain_or_loss"},
    ),
    CapabilitySelection(
        name="ca/disposition_gains",
        params={},
        consumes={"dispositions": "ca/other_foreclosure_dispositions"},
        produces={"output": "ca/other_foreclosure_gain_or_loss"},
    ),
    CapabilitySelection(
        name="ca/disposition_gains_only",
        params={},
        consumes={"dispositions": "ca/personal_use_property_dispositions"},
        produces={"output": "ca/personal_use_property_gain_rows"},
    ),
    CapabilitySelection(
        name="ca/principal_residence_gain",
        params={"rounding": "ca/principal_residence_gain_rounding"},
        consumes={"properties": "ca/principal_residence_properties"},
        produces={"output": "ca/principal_residence_gain"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/personal_use_property_gain_rows",
                "ca/principal_residence_gain",
            )
        },
        produces={"output": "ca/personal_use_property_gain"},
    ),
    CapabilitySelection(
        name="ca/disposition_gains",
        params={},
        consumes={"dispositions": "ca/listed_personal_property_dispositions"},
        produces={"output": "ca/listed_personal_property_gain_or_loss"},
    ),
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/listed_personal_property_gain_or_loss",
            "less": "ca/unapplied_listed_personal_property_losses",
        },
        produces={"output": "ca/listed_personal_property_net_gain"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/qsbcs_gain_or_loss",
                "ca/qffp_gain_or_loss",
                "ca/qffp_foreclosure_gain_or_loss",
                "ca/share_gain_or_loss",
                "ca/real_estate_gain_or_loss",
                "ca/bond_gain_or_loss",
                "ca/crypto_asset_gain_or_loss",
                "ca/other_foreclosure_gain_or_loss",
                "ca/personal_use_property_gain",
                "ca/listed_personal_property_net_gain",
            )
        },
        produces={"output": "ca/capital_gains_of_qualified_and_other_properties"},
    ),
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/capital_gains_of_qualified_and_other_properties",
            "less": "ca/capital_gains_deferral",
        },
        produces={"output": "ca/capital_gains_after_deferral"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/capital_gains_after_deferral",
                "ca/slip_capital_gains_or_losses",
                "ca/t3_capital_gains_or_losses",
            )
        },
        produces={"output": "ca/capital_gains_before_investment_loss_reduction"},
    ),
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/capital_gains_before_investment_loss_reduction",
            "less": "ca/business_investment_loss_reduction",
        },
        produces={"output": "ca/capital_gains_before_reserves"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/capital_gains_before_reserves",
                "ca/capital_gains_reserves",
            )
        },
        produces={"output": "ca/capital_gain"},
    ),
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/capital_gains_inclusion_rate"},
        consumes={"base": "ca/capital_gain"},
        produces={"output": "ca/included_capital_gain"},
    ),
    CapabilitySelection(
        name="core/sum_not_below_zero",
        params={},
        consumes={
            "parts": (
                "ca/included_capital_gain",
                "ca/partnership_gains_at_full_inclusion",
            )
        },
        produces={"output": "ca/taxable_capital_gains"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/t3_taxable_dividends",
                "ca/t4ps_taxable_dividends",
                "ca/t5_taxable_dividends",
                "ca/t5013_taxable_dividends",
            )
        },
        produces={"output": "ca/slip_taxable_dividends"},
    ),
    CapabilitySelection(
        name="core/apply_fraction",
        params={"fraction": "ca/eligible_dividend_gross_up"},
        consumes={"base": "ca/eligible_dividends_received_without_a_slip"},
        produces={"output": "ca/eligible_dividends_grossed_up"},
    ),
    CapabilitySelection(
        name="core/apply_fraction",
        params={"fraction": "ca/other_dividend_gross_up"},
        consumes={"base": "ca/other_dividends_received_without_a_slip"},
        produces={"output": "ca/other_dividends_grossed_up"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/eligible_dividends_grossed_up",
                "ca/other_dividends_grossed_up",
            )
        },
        produces={"output": "ca/dividends_without_a_slip_grossed_up"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/slip_taxable_dividends",
                "ca/dividends_without_a_slip_grossed_up",
            )
        },
        produces={"output": "ca/taxable_dividends"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/t3_investment_income",
                "ca/t5_investment_income",
                "ca/t5013_investment_income",
                "ca/investment_income_credited_not_received",
                "ca/tax_refund_interest",
                "ca/foreign_investment_income",
                "ca/investment_income_without_a_slip",
                "ca/investment_royalties",
            )
        },
        produces={"output": "ca/investment_income_before_prior_years"},
    ),
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/investment_income_before_prior_years",
            "less": "ca/investment_income_reported_in_previous_years",
        },
        produces={"output": "ca/interest_and_other_investment_income"},
    ),
    CapabilitySelection(
        name="core/record_total",
        params={},
        consumes={"records": "ca/t776.net_rental_income"},
        produces={"output": "ca/net_rental_income"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/total_carrying_charges",
                "ca/total_interest_expenses",
                "ca/total_other_expenses",
            )
        },
        produces={"output": "ca/carrying_charges_interest_expenses_and_other_expenses"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/capital_gains_deductions_1985_to_1987",
                "ca/capital_gains_deductions_1988_and_1989_other_than_eligible_capital_property",
                "ca/capital_gains_deductions_1988_and_1989_eligible_capital_property",
                "ca/capital_gains_deductions_1990_to_1999",
                "ca/capital_gains_deductions_2000",
                "ca/capital_gains_deductions_2001_to_2024",
            )
        },
        produces={"output": "ca/capital_gains_deductions_claimed_1985_to_2024"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/other_business_investment_loss_reductions_1986_to_1994",
                "ca/other_business_investment_loss_reductions_1994_to_1996",
                "ca/other_business_investment_loss_reductions_1997_to_1999",
                "ca/other_business_investment_loss_reductions_2000",
                "ca/other_business_investment_loss_reductions_2001_to_2023",
                "ca/other_business_investment_loss_reductions_2024",
            )
        },
        produces={"output": "ca/other_business_investment_loss_reductions_1986_to_2024"},
    ),
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/capital_gains_deductions_claimed_1985_to_2024",
            "less": "ca/other_business_investment_loss_reductions_1986_to_2024",
        },
        produces={"output": "ca/business_investment_loss_reduction_available"},
    ),
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={
            "amounts": (
                "ca/business_investment_loss_reduction_available",
                "ca/business_investment_loss",
            )
        },
        produces={"output": "ca/business_investment_loss_reduction"},
    ),
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/business_investment_loss",
            "less": "ca/business_investment_loss_reduction",
        },
        produces={"output": "ca/business_investment_loss_after_reduction"},
    ),
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/business_investment_loss_inclusion_rate"},
        consumes={"base": "ca/business_investment_loss_after_reduction"},
        produces={"output": "ca/allowable_business_investment_loss"},
    ),
    CapabilitySelection(
        name="core/apply_fraction",
        params={"fraction": "ca/pre_1986_deductions_factor_1988_and_1989"},
        consumes={"base": "ca/pre_1986_deductions_1988_and_1989"},
        produces={"output": "ca/pre_1986_deductions_adjusted_1988_and_1989"},
    ),
    CapabilitySelection(
        name="core/apply_fraction",
        params={"fraction": "ca/pre_1986_deductions_factor_1990_to_1999"},
        consumes={"base": "ca/pre_1986_deductions_1990_to_1999"},
        produces={"output": "ca/pre_1986_deductions_adjusted_1990_to_1999"},
    ),
    CapabilitySelection(
        name="ca/apply_ratio_or_zero",
        params={"rounding": "ca/pre_1986_deductions_adjusted_2000_rounding"},
        consumes={
            "amount": "ca/pre_1986_deductions_2000",
            "numerator": "ca/net_capital_loss_numerator_one_2000",
            "denominator": "ca/net_capital_loss_twice_ir_2000",
        },
        produces={"output": "ca/pre_1986_deductions_adjusted_2000"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/pre_1986_deductions_before_1988",
                "ca/pre_1986_deductions_adjusted_1988_and_1989",
                "ca/pre_1986_deductions_adjusted_1990_to_1999",
                "ca/pre_1986_deductions_adjusted_2000",
                "ca/pre_1986_deductions_2001_to_2024",
            )
        },
        produces={"output": "ca/pre_1986_deductions_total"},
    ),
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/net_capital_losses_before_may_23_1985",
            "less": "ca/pre_1986_deductions_total",
        },
        produces={"output": "ca/pre_1986_capital_loss_balance"},
    ),
    CapabilitySelection(
        name="core/apply_fraction",
        params={"fraction": "ca/net_capital_loss_inclusion_rate_factor_before_may_23_1985"},
        consumes={"base": "ca/pre_1986_capital_loss_balance"},
        produces={"output": "ca/adjusted_gross_capital_losses_before_may_23_1985"},
    ),
    CapabilitySelection(
        name="core/apply_fraction",
        params={"fraction": "ca/net_capital_loss_inclusion_rate_factor_1985_to_1987"},
        consumes={"base": "ca/unapplied_net_capital_losses_1985_to_1987"},
        produces={"output": "ca/adjusted_gross_capital_losses_1985_to_1987"},
    ),
    CapabilitySelection(
        name="core/apply_fraction",
        params={"fraction": "ca/net_capital_loss_inclusion_rate_factor_1988_and_1989"},
        consumes={"base": "ca/unapplied_net_capital_losses_1988_and_1989"},
        produces={"output": "ca/adjusted_gross_capital_losses_1988_and_1989"},
    ),
    CapabilitySelection(
        name="core/apply_fraction",
        params={"fraction": "ca/net_capital_loss_inclusion_rate_factor_1990_to_1999"},
        consumes={"base": "ca/unapplied_net_capital_losses_1990_to_1999"},
        produces={"output": "ca/adjusted_gross_capital_losses_1990_to_1999"},
    ),
    CapabilitySelection(
        name="core/apply_fraction",
        params={"fraction": "ca/net_capital_loss_inclusion_rate_factor_2001_to_2024"},
        consumes={"base": "ca/unapplied_net_capital_losses_2001_to_2024"},
        produces={"output": "ca/adjusted_gross_capital_losses_2001_to_2024"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/adjusted_gross_capital_losses_before_may_23_1985",
                "ca/adjusted_gross_capital_losses_1985_to_1987",
                "ca/adjusted_gross_capital_losses_1988_and_1989",
                "ca/adjusted_gross_capital_losses_1990_to_1999",
                "ca/adjusted_gross_capital_losses_2000",
                "ca/adjusted_gross_capital_losses_2001_to_2024",
            )
        },
        produces={"output": "ca/total_adjusted_net_capital_losses"},
    ),
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={
            "amounts": (
                "ca/total_adjusted_net_capital_losses",
                "ca/taxable_capital_gains",
            )
        },
        produces={"output": "ca/net_capital_losses_available_to_claim"},
    ),
    CapabilitySelection(
        name="core/at_most",
        params={},
        consumes={
            "amount": "ca/net_capital_losses_claimed",
            "bound": "ca/net_capital_losses_available_to_claim",
        },
        produces={"output": "ca/adjusted_net_capital_losses_applied"},
    ),
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/total_adjusted_net_capital_losses",
            "less": "ca/adjusted_net_capital_losses_applied",
        },
        produces={"output": "ca/unapplied_adjusted_net_capital_losses"},
    ),
    CapabilitySelection(
        name="ca/lesser_of_with_maximum",
        params={"maximum": "ca/net_capital_losses_additional_deduction_maximum"},
        consumes={
            "amounts": (
                "ca/pre_1986_capital_loss_balance",
                "ca/unapplied_adjusted_net_capital_losses",
            )
        },
        produces={"output": "ca/net_capital_losses_additional_deduction"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/adjusted_net_capital_losses_applied",
                "ca/net_capital_losses_additional_deduction",
            )
        },
        produces={"output": "ca/net_capital_losses_of_other_years"},
    ),
    CapabilitySelection(
        name="core/apply_fraction",
        params={"fraction": "ca/net_capital_loss_twice_ir_fraction_2000"},
        consumes={"base": "ca/t657_inclusion_rate_2000"},
        produces={"output": "ca/net_capital_loss_twice_ir_2000"},
    ),
    CapabilitySelection(
        name="core/credit_amount",
        params={"amount": "ca/net_capital_loss_numerator_one_2000"},
        consumes={},
        produces={"output": "ca/net_capital_loss_numerator_one_2000"},
    ),
    CapabilitySelection(
        name="ca/apply_ratio_or_zero",
        params={"rounding": "ca/adjusted_gross_capital_losses_2000_rounding"},
        consumes={
            "amount": "ca/unapplied_net_capital_losses_2000",
            "numerator": "ca/net_capital_loss_numerator_one_2000",
            "denominator": "ca/net_capital_loss_twice_ir_2000",
        },
        produces={"output": "ca/adjusted_gross_capital_losses_2000"},
    ),
}

FORM_STEPS = OWN_STEPS | COPIED_STEPS


# The form exports the eight artifacts of the 02_outputs block and line 25395's claim, which the
# return reads (06_taxable_income, 08a_foreign_tax_credit and 20_alternative_minimum_tax).
FORM_EXPORTS = (
    "ca/qbt_allocation_total",
    "ca/qcc_election_deduction",
    "ca/qbt_election_deduction",
    "ca/qbt_taxable_capital_gains",
    "ca/qbt_taxable_gains_related_to_deduction",
    "ca/qsbcs_qffp_taxable_gains_related_to_deduction",
    "ca/qbt_abil_reduction",
    "ca/qbt_net_investment_loss_reduction",
    "ca/qbt_capital_gains_deduction",
)

# The return's own artifacts that the form's selections read (the form starts from them, as the
# other forms do); none of them is produced on the form.
IMPORTS = frozenset({"ca/t776.net_rental_income"})

INPUTS = frozenset({"ca/t2048_dispositions"})

# Part 5's totals (A 17211, B 17212, C 17213, D 17215, E 17216, F 17217, G 17218; C, F and G are
# lines 16, 41 and 42) and Part 4 line 32: the return's own outputs, read by no other line of it
# (or, where a line is read, by the return's record totals of the form's exports).
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


# The return totals each export over the dispositions, `core/record_total`.
STEPS = {
    CapabilitySelection(
        name="core/record_total",
        params={},
        consumes={"records": "ca/t2048.qbt_allocation_total"},
        produces={"output": "ca/qbt_allocation_total"},
    ),
    CapabilitySelection(
        name="core/record_total",
        params={},
        consumes={"records": "ca/t2048.qcc_election_deduction"},
        produces={"output": "ca/qcc_election_deduction"},
    ),
    CapabilitySelection(
        name="core/record_total",
        params={},
        consumes={"records": "ca/t2048.qbt_election_deduction"},
        produces={"output": "ca/qbt_election_deduction"},
    ),
    CapabilitySelection(
        name="core/record_total",
        params={},
        consumes={"records": "ca/t2048.qbt_taxable_capital_gains"},
        produces={"output": "ca/qbt_taxable_capital_gains"},
    ),
    CapabilitySelection(
        name="core/record_total",
        params={},
        consumes={"records": "ca/t2048.qbt_taxable_gains_related_to_deduction"},
        produces={"output": "ca/qbt_taxable_gains_related_to_deduction"},
    ),
    CapabilitySelection(
        name="core/record_total",
        params={},
        consumes={"records": "ca/t2048.qsbcs_qffp_taxable_gains_related_to_deduction"},
        produces={"output": "ca/qsbcs_qffp_taxable_gains_related_to_deduction"},
    ),
    CapabilitySelection(
        name="core/record_total",
        params={},
        consumes={"records": "ca/t2048.qbt_abil_reduction"},
        produces={"output": "ca/qbt_abil_reduction"},
    ),
    CapabilitySelection(
        name="core/record_total",
        params={},
        consumes={"records": "ca/t2048.qbt_net_investment_loss_reduction"},
        produces={"output": "ca/qbt_net_investment_loss_reduction"},
    ),
    CapabilitySelection(
        name="core/record_total",
        params={},
        consumes={"records": "ca/t2048.qbt_capital_gains_deduction"},
        produces={"output": "ca/qbt_capital_gains_deduction"},
    ),
}

FORM_WIRING = {
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
    (DispositionGains, frozenset({QSBCS_DISPOSITIONS}), frozenset({QSBCS_GAIN_OR_LOSS})),
    (DispositionGains, frozenset({QFFP_DISPOSITIONS}), frozenset({QFFP_GAIN_OR_LOSS})),
    (
        DispositionGains,
        frozenset({QFFP_FORECLOSURE_DISPOSITIONS}),
        frozenset({QFFP_FORECLOSURE_GAIN_OR_LOSS}),
    ),
    (DispositionGains, frozenset({SHARE_DISPOSITIONS}), frozenset({SHARE_GAIN_OR_LOSS})),
    (
        DispositionGains,
        frozenset({REAL_ESTATE_DISPOSITIONS}),
        frozenset({REAL_ESTATE_GAIN_OR_LOSS}),
    ),
    (DispositionGains, frozenset({BOND_DISPOSITIONS}), frozenset({BOND_GAIN_OR_LOSS})),
    (
        DispositionGains,
        frozenset({CRYPTO_ASSET_DISPOSITIONS}),
        frozenset({CRYPTO_ASSET_GAIN_OR_LOSS}),
    ),
    (
        DispositionGains,
        frozenset({OTHER_FORECLOSURE_DISPOSITIONS}),
        frozenset({OTHER_FORECLOSURE_GAIN_OR_LOSS}),
    ),
    (
        DispositionGainsOnly,
        frozenset({PERSONAL_USE_PROPERTY_DISPOSITIONS}),
        frozenset({PERSONAL_USE_PROPERTY_GAIN_ROWS}),
    ),
    (
        PrincipalResidenceGain,
        frozenset({PRINCIPAL_RESIDENCE_PROPERTIES}),
        frozenset({PRINCIPAL_RESIDENCE_GAIN}),
    ),
    (
        Sum,
        frozenset({PERSONAL_USE_PROPERTY_GAIN_ROWS, PRINCIPAL_RESIDENCE_GAIN}),
        frozenset({PERSONAL_USE_PROPERTY_GAIN}),
    ),
    (
        DispositionGains,
        frozenset({LISTED_PERSONAL_PROPERTY_DISPOSITIONS}),
        frozenset({LISTED_PERSONAL_PROPERTY_GAIN_OR_LOSS}),
    ),
    (
        SubtractNotBelowZero,
        frozenset(
            {LISTED_PERSONAL_PROPERTY_GAIN_OR_LOSS, UNAPPLIED_LISTED_PERSONAL_PROPERTY_LOSSES}
        ),
        frozenset({LISTED_PERSONAL_PROPERTY_NET_GAIN}),
    ),
    (
        Sum,
        frozenset(
            {
                BOND_GAIN_OR_LOSS,
                CRYPTO_ASSET_GAIN_OR_LOSS,
                LISTED_PERSONAL_PROPERTY_NET_GAIN,
                OTHER_FORECLOSURE_GAIN_OR_LOSS,
                PERSONAL_USE_PROPERTY_GAIN,
                QFFP_FORECLOSURE_GAIN_OR_LOSS,
                QFFP_GAIN_OR_LOSS,
                QSBCS_GAIN_OR_LOSS,
                REAL_ESTATE_GAIN_OR_LOSS,
                SHARE_GAIN_OR_LOSS,
            }
        ),
        frozenset({CAPITAL_GAINS_OF_QUALIFIED_AND_OTHER_PROPERTIES}),
    ),
    (
        Subtract,
        frozenset({CAPITAL_GAINS_DEFERRAL, CAPITAL_GAINS_OF_QUALIFIED_AND_OTHER_PROPERTIES}),
        frozenset({CAPITAL_GAINS_AFTER_DEFERRAL}),
    ),
    (
        Sum,
        frozenset(
            {CAPITAL_GAINS_AFTER_DEFERRAL, SLIP_CAPITAL_GAINS_OR_LOSSES, T3_CAPITAL_GAINS_OR_LOSSES}
        ),
        frozenset({CAPITAL_GAINS_BEFORE_INVESTMENT_LOSS_REDUCTION}),
    ),
    (
        Subtract,
        frozenset(
            {BUSINESS_INVESTMENT_LOSS_REDUCTION, CAPITAL_GAINS_BEFORE_INVESTMENT_LOSS_REDUCTION}
        ),
        frozenset({CAPITAL_GAINS_BEFORE_RESERVES}),
    ),
    (
        Sum,
        frozenset({CAPITAL_GAINS_BEFORE_RESERVES, CAPITAL_GAINS_RESERVES}),
        frozenset({CAPITAL_GAIN}),
    ),
    (ApplyRate, frozenset({CAPITAL_GAIN}), frozenset({INCLUDED_CAPITAL_GAIN})),
    (
        SumNotBelowZero,
        frozenset({INCLUDED_CAPITAL_GAIN, PARTNERSHIP_GAINS_AT_FULL_INCLUSION}),
        frozenset({TAXABLE_CAPITAL_GAINS}),
    ),
    (
        Sum,
        frozenset(
            {
                T3_TAXABLE_DIVIDENDS,
                T4PS_TAXABLE_DIVIDENDS,
                T5013_TAXABLE_DIVIDENDS,
                T5_TAXABLE_DIVIDENDS,
            }
        ),
        frozenset({SLIP_TAXABLE_DIVIDENDS}),
    ),
    (
        ApplyFraction,
        frozenset({ELIGIBLE_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP}),
        frozenset({ELIGIBLE_DIVIDENDS_GROSSED_UP}),
    ),
    (
        ApplyFraction,
        frozenset({OTHER_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP}),
        frozenset({OTHER_DIVIDENDS_GROSSED_UP}),
    ),
    (
        Sum,
        frozenset({ELIGIBLE_DIVIDENDS_GROSSED_UP, OTHER_DIVIDENDS_GROSSED_UP}),
        frozenset({DIVIDENDS_WITHOUT_A_SLIP_GROSSED_UP}),
    ),
    (
        Sum,
        frozenset({DIVIDENDS_WITHOUT_A_SLIP_GROSSED_UP, SLIP_TAXABLE_DIVIDENDS}),
        frozenset({TAXABLE_DIVIDENDS}),
    ),
    (
        Sum,
        frozenset(
            {
                FOREIGN_INVESTMENT_INCOME,
                INVESTMENT_INCOME_CREDITED_NOT_RECEIVED,
                INVESTMENT_INCOME_WITHOUT_A_SLIP,
                INVESTMENT_ROYALTIES,
                T3_INVESTMENT_INCOME,
                T5013_INVESTMENT_INCOME,
                T5_INVESTMENT_INCOME,
                TAX_REFUND_INTEREST,
            }
        ),
        frozenset({INVESTMENT_INCOME_BEFORE_PRIOR_YEARS}),
    ),
    (
        Subtract,
        frozenset(
            {INVESTMENT_INCOME_BEFORE_PRIOR_YEARS, INVESTMENT_INCOME_REPORTED_IN_PREVIOUS_YEARS}
        ),
        frozenset({INTEREST_AND_OTHER_INVESTMENT_INCOME}),
    ),
    (RecordTotal, frozenset({NET_RENTAL_INCOME_PER_STATEMENT}), frozenset({NET_RENTAL_INCOME})),
    (
        Sum,
        frozenset({TOTAL_CARRYING_CHARGES, TOTAL_INTEREST_EXPENSES, TOTAL_OTHER_EXPENSES}),
        frozenset({CARRYING_CHARGES_INTEREST_EXPENSES_AND_OTHER_EXPENSES}),
    ),
    (
        Sum,
        frozenset(
            {
                CAPITAL_GAINS_DEDUCTIONS_1985_TO_1987,
                CAPITAL_GAINS_DEDUCTIONS_1988_AND_1989_ELIGIBLE_CAPITAL_PROPERTY,
                CAPITAL_GAINS_DEDUCTIONS_1988_AND_1989_OTHER_THAN_ELIGIBLE_CAPITAL_PROPERTY,
                CAPITAL_GAINS_DEDUCTIONS_1990_TO_1999,
                CAPITAL_GAINS_DEDUCTIONS_2000,
                CAPITAL_GAINS_DEDUCTIONS_2001_TO_2024,
            }
        ),
        frozenset({CAPITAL_GAINS_DEDUCTIONS_CLAIMED_1985_TO_2024}),
    ),
    (
        Sum,
        frozenset(
            {
                OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_1994,
                OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1994_TO_1996,
                OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1997_TO_1999,
                OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2000,
                OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2001_TO_2023,
                OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2024,
            }
        ),
        frozenset({OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_2024}),
    ),
    (
        Subtract,
        frozenset(
            {
                CAPITAL_GAINS_DEDUCTIONS_CLAIMED_1985_TO_2024,
                OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_2024,
            }
        ),
        frozenset({BUSINESS_INVESTMENT_LOSS_REDUCTION_AVAILABLE}),
    ),
    (
        LesserOf,
        frozenset({BUSINESS_INVESTMENT_LOSS, BUSINESS_INVESTMENT_LOSS_REDUCTION_AVAILABLE}),
        frozenset({BUSINESS_INVESTMENT_LOSS_REDUCTION}),
    ),
    (
        Subtract,
        frozenset({BUSINESS_INVESTMENT_LOSS, BUSINESS_INVESTMENT_LOSS_REDUCTION}),
        frozenset({BUSINESS_INVESTMENT_LOSS_AFTER_REDUCTION}),
    ),
    (
        ApplyRate,
        frozenset({BUSINESS_INVESTMENT_LOSS_AFTER_REDUCTION}),
        frozenset({ALLOWABLE_BUSINESS_INVESTMENT_LOSS}),
    ),
    (
        ApplyFraction,
        frozenset({PRE_1986_DEDUCTIONS_1988_AND_1989}),
        frozenset({PRE_1986_DEDUCTIONS_ADJUSTED_1988_AND_1989}),
    ),
    (
        ApplyFraction,
        frozenset({PRE_1986_DEDUCTIONS_1990_TO_1999}),
        frozenset({PRE_1986_DEDUCTIONS_ADJUSTED_1990_TO_1999}),
    ),
    (
        ApplyRatioOrZero,
        frozenset(
            {
                NET_CAPITAL_LOSS_NUMERATOR_ONE_2000,
                NET_CAPITAL_LOSS_TWICE_IR_2000,
                PRE_1986_DEDUCTIONS_2000,
            }
        ),
        frozenset({PRE_1986_DEDUCTIONS_ADJUSTED_2000}),
    ),
    (
        Sum,
        frozenset(
            {
                PRE_1986_DEDUCTIONS_2001_TO_2024,
                PRE_1986_DEDUCTIONS_ADJUSTED_1988_AND_1989,
                PRE_1986_DEDUCTIONS_ADJUSTED_1990_TO_1999,
                PRE_1986_DEDUCTIONS_ADJUSTED_2000,
                PRE_1986_DEDUCTIONS_BEFORE_1988,
            }
        ),
        frozenset({PRE_1986_DEDUCTIONS_TOTAL}),
    ),
    (
        Subtract,
        frozenset({NET_CAPITAL_LOSSES_BEFORE_MAY_23_1985, PRE_1986_DEDUCTIONS_TOTAL}),
        frozenset({PRE_1986_CAPITAL_LOSS_BALANCE}),
    ),
    (
        ApplyFraction,
        frozenset({PRE_1986_CAPITAL_LOSS_BALANCE}),
        frozenset({ADJUSTED_GROSS_CAPITAL_LOSSES_BEFORE_MAY_23_1985}),
    ),
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
                ADJUSTED_GROSS_CAPITAL_LOSSES_2000,
                ADJUSTED_GROSS_CAPITAL_LOSSES_2001_TO_2024,
                ADJUSTED_GROSS_CAPITAL_LOSSES_BEFORE_MAY_23_1985,
            }
        ),
        frozenset({TOTAL_ADJUSTED_NET_CAPITAL_LOSSES}),
    ),
    (
        LesserOf,
        frozenset({TAXABLE_CAPITAL_GAINS, TOTAL_ADJUSTED_NET_CAPITAL_LOSSES}),
        frozenset({NET_CAPITAL_LOSSES_AVAILABLE_TO_CLAIM}),
    ),
    (
        AtMost,
        frozenset({NET_CAPITAL_LOSSES_AVAILABLE_TO_CLAIM, NET_CAPITAL_LOSSES_CLAIMED}),
        frozenset({ADJUSTED_NET_CAPITAL_LOSSES_APPLIED}),
    ),
    (
        Subtract,
        frozenset({ADJUSTED_NET_CAPITAL_LOSSES_APPLIED, TOTAL_ADJUSTED_NET_CAPITAL_LOSSES}),
        frozenset({UNAPPLIED_ADJUSTED_NET_CAPITAL_LOSSES}),
    ),
    (
        LesserOfWithMaximum,
        frozenset({PRE_1986_CAPITAL_LOSS_BALANCE, UNAPPLIED_ADJUSTED_NET_CAPITAL_LOSSES}),
        frozenset({NET_CAPITAL_LOSSES_ADDITIONAL_DEDUCTION}),
    ),
    (
        Sum,
        frozenset({ADJUSTED_NET_CAPITAL_LOSSES_APPLIED, NET_CAPITAL_LOSSES_ADDITIONAL_DEDUCTION}),
        frozenset({NET_CAPITAL_LOSSES_OF_OTHER_YEARS}),
    ),
    (
        ApplyFraction,
        frozenset({T657_INCLUSION_RATE_2000}),
        frozenset({NET_CAPITAL_LOSS_TWICE_IR_2000}),
    ),
    (CreditAmount, frozenset({}), frozenset({NET_CAPITAL_LOSS_NUMERATOR_ONE_2000})),
    (
        ApplyRatioOrZero,
        frozenset(
            {
                NET_CAPITAL_LOSS_NUMERATOR_ONE_2000,
                NET_CAPITAL_LOSS_TWICE_IR_2000,
                UNAPPLIED_NET_CAPITAL_LOSSES_2000,
            }
        ),
        frozenset({ADJUSTED_GROSS_CAPITAL_LOSSES_2000}),
    ),
}


WIRING = {
    (RecordTotal, frozenset({ALLOCATION_TOTAL_PER_DISPOSITION}), frozenset({QBT_ALLOCATION_TOTAL})),
    (
        RecordTotal,
        frozenset({QCC_ELECTION_DEDUCTION_PER_DISPOSITION}),
        frozenset({QCC_ELECTION_DEDUCTION}),
    ),
    (
        RecordTotal,
        frozenset({QBT_ELECTION_DEDUCTION_PER_DISPOSITION}),
        frozenset({QBT_ELECTION_DEDUCTION}),
    ),
    (
        RecordTotal,
        frozenset({TAXABLE_CAPITAL_GAINS_PER_DISPOSITION}),
        frozenset({QBT_TAXABLE_CAPITAL_GAINS}),
    ),
    (
        RecordTotal,
        frozenset({TAXABLE_GAINS_RELATED_PER_DISPOSITION}),
        frozenset({QBT_TAXABLE_GAINS_RELATED_TO_DEDUCTION}),
    ),
    (
        RecordTotal,
        frozenset({QSBCS_QFFP_GAINS_RELATED_PER_DISPOSITION}),
        frozenset({QSBCS_QFFP_TAXABLE_GAINS_RELATED_TO_DEDUCTION}),
    ),
    (RecordTotal, frozenset({ABIL_REDUCTION_PER_DISPOSITION}), frozenset({QBT_ABIL_REDUCTION})),
    (
        RecordTotal,
        frozenset({NET_INVESTMENT_LOSS_REDUCTION_PER_DISPOSITION}),
        frozenset({QBT_NET_INVESTMENT_LOSS_REDUCTION}),
    ),
    (
        RecordTotal,
        frozenset({CAPITAL_GAINS_DEDUCTION_PER_DISPOSITION}),
        frozenset({QBT_CAPITAL_GAINS_DEDUCTION}),
    ),
}
