"""Registered and money kinds of the federal catalog family `taxable_income`."""

from __future__ import annotations

from decimal import Decimal

from app.domain.artifact import ArtifactRegistry
from app.domain.record_list import RecordListKind
from app.jurisdictions.ca.catalog import (
    ABIL_AFTER_QBT_REDUCTION,
    ABIL_CLAIMED_AFTER_1984_AND_BEFORE_2025,
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
    ADJUSTED_NET_CAPITAL_LOSSES_OF_OTHER_YEARS,
    ANNUAL_GAINS_LIMIT_2025,
    ANNUAL_GAINS_LINE_3,
    ANNUAL_GAINS_LINE_3_AT_INCLUSION_RATE,
    ANNUAL_GAINS_LINE_5,
    ANNUAL_GAINS_LINE_7,
    ANNUAL_GAINS_LINE_9,
    ANNUAL_GAINS_LINE_10,
    ANNUAL_GAINS_LINE_12,
    ANNUAL_GAINS_SCHEDULE_3_TOTAL,
    CAPITAL_GAINS_DEDUCTION,
    CAPITAL_GAINS_DEDUCTION_CLAIMED,
    CHART_1_COLUMN_G_TOTAL,
    CHART_2_LINE_3,
    CHART_2_LINE_4,
    CHART_2_LINE_5,
    CHART_2_LINE_7,
    CHART_2_LINE_8,
    CHART_2_LINE_9,
    CHART_2_LINE_11,
    CHART_2_LINE_12,
    CHART_2_LINE_13,
    CHART_2_LINE_14_OVER_TWICE_IR,
    CHART_2_LINE_15,
    CHART_2_LINE_16,
    CHART_2_LINE_17,
    CHART_2_LINE_19,
    CHART_2_NUMERATOR_ONE,
    CHART_2_TWICE_IR,
    CHART_2025_PART_1_AMOUNT_A,
    CHART_2025_PART_1_AMOUNT_C,
    CHART_2025_PART_1_AMOUNT_E,
    CHART_2025_PART_1_AMOUNT_K,
    CHART_2025_PART_1_AMOUNT_M,
    CHART_2025_PART_1_AMOUNT_N,
    CHART_2025_PART_1_AMOUNT_P,
    CHART_2025_PART_1_AMOUNT_Q,
    CHART_2025_PART_1_AMOUNTS_F_TO_J,
    CHART_2025_PART_2_AMOUNT_A,
    CHART_2025_PART_2_AMOUNT_C,
    CHART_2025_PART_2_AMOUNT_E,
    CHART_2025_PART_2_AMOUNT_F,
    CHART_2025_PART_2_AMOUNT_G,
    CHART_2025_PART_2_AMOUNT_H,
    CHART_2025_PART_2_AMOUNT_K,
    CHART_2025_PART_2_AMOUNT_M,
    CHART_2025_PART_2_AMOUNT_N,
    CHART_2025_PART_2_AMOUNT_P,
    CHART_2025_PART_2_AMOUNT_Q,
    CHART_2025_PART_2_AMOUNTS_F_TO_J,
    CUMULATIVE_ELIGIBLE_TAXABLE_CAPITAL_GAINS,
    CUMULATIVE_GAINS_LIMIT_2025,
    CUMULATIVE_LOSSES_AND_DEDUCTIONS,
    DEDUCTIONS_FROM_NET_INCOME,
    ELIGIBLE_TAXABLE_CAPITAL_GAINS_2002_TO_2025,
    ELIGIBLE_TAXABLE_CAPITAL_GAINS_2025,
    EXEMPT_INCOME_DEDUCTIONS,
    LIMITED_PARTNERSHIP_LOSSES_OF_OTHER_YEARS,
    NET_CAPITAL_LOSS_BALANCE_1985_TO_1987,
    NET_CAPITAL_LOSS_BALANCE_1988_AND_1989,
    NET_CAPITAL_LOSS_BALANCE_1990_TO_1999,
    NET_CAPITAL_LOSS_BALANCE_2001_TO_2024,
    NET_CAPITAL_LOSSES_AVAILABLE_TO_CLAIM,
    NET_CAPITAL_LOSSES_CLAIMED,
    NET_CAPITAL_LOSSES_OF_OTHER_YEARS,
    NON_CAPITAL_LOSSES_OF_OTHER_YEARS,
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
    REMAINING_ADJUSTED_LOSSES_1985_TO_1987,
    REMAINING_ADJUSTED_LOSSES_1988_AND_1989,
    REMAINING_ADJUSTED_LOSSES_1990_TO_1999,
    REMAINING_ADJUSTED_LOSSES_2001_TO_2024,
    SCHEDULE_3_LINE_17600_NOT_BELOW_ZERO,
    SCHEDULE_3_LINE_19900,
    T657_ABIL_CLAIMED_1985_TO_2024,
    T657_CAPITAL_LOSSES_CLAIMED_1985,
    T657_CHART_1_COLUMN_A,
    T657_CHART_1_COLUMN_B,
    T657_CHART_1_COLUMN_C,
    T657_CHART_1_COLUMN_D,
    T657_CHART_1_ROWS,
    T657_CHART_2_LINE_1,
    T657_CHART_2_LINE_2,
    T657_CHART_2_LINE_6,
    T657_CHART_2_LINE_10,
    T657_CHART_2_LINE_14,
    T657_CHART_2_LINE_18,
    T657_CUMULATIVE_NET_INVESTMENT_LOSS,
    T657_DEDUCTIONS_CLAIMED_1985_TO_2024,
    T657_GAINS_1985_TO_1991,
    T657_GAINS_1992_AND_1993,
    T657_GAINS_1994,
    T657_GAINS_1995,
    T657_GAINS_1996_TO_1999,
    T657_GAINS_2000,
    T657_GAINS_2001,
    T657_GAINS_2002_TO_2024,
    T657_INCLUSION_RATE_2000,
    T657_NET_NON_ELIGIBLE_TAXABLE_CAPITAL_GAINS,
    T657_PART_1_AMOUNT_B,
    T657_PART_1_AMOUNT_F,
    T657_PART_1_AMOUNT_G,
    T657_PART_1_AMOUNT_H,
    T657_PART_1_AMOUNT_I,
    T657_PART_1_AMOUNT_J,
    T657_PART_1_AMOUNT_L,
    T657_PART_2_AMOUNT_I,
    T657_PART_2_AMOUNT_J,
    T657_PART_2_AMOUNT_L,
    T657_PART_2_EXCLUDED_F,
    T657_PART_2_EXCLUDED_G,
    T657_PART_2_EXCLUDED_H,
    T657_T2017_LINE_13,
    T657_T2048_LINE_17217_FOR_2024,
    TAXABLE_INCOME,
    TOTAL_ADJUSTED_NET_CAPITAL_LOSSES,
    TOTAL_LOSSES_FOR_ANNUAL_GAINS_LIMIT,
    UNAPPLIED_NET_CAPITAL_LOSSES_1985_TO_1987,
    UNAPPLIED_NET_CAPITAL_LOSSES_1988_AND_1989,
    UNAPPLIED_NET_CAPITAL_LOSSES_1990_TO_1999,
    UNAPPLIED_NET_CAPITAL_LOSSES_2001_TO_2024,
)


def test_the_taxable_income_kinds_are_the_registered_ones(registry: ArtifactRegistry) -> None:
    assert registry.get("ca/taxable_income") is TAXABLE_INCOME
    assert (
        registry.get("ca/limited_partnership_losses_of_other_years")
        is LIMITED_PARTNERSHIP_LOSSES_OF_OTHER_YEARS
    )
    assert registry.get("ca/non_capital_losses_of_other_years") is NON_CAPITAL_LOSSES_OF_OTHER_YEARS
    assert (
        registry.get("ca/unapplied_net_capital_losses_1985_to_1987")
        is UNAPPLIED_NET_CAPITAL_LOSSES_1985_TO_1987
    )
    assert (
        registry.get("ca/unapplied_net_capital_losses_1988_and_1989")
        is UNAPPLIED_NET_CAPITAL_LOSSES_1988_AND_1989
    )
    assert (
        registry.get("ca/unapplied_net_capital_losses_1990_to_1999")
        is UNAPPLIED_NET_CAPITAL_LOSSES_1990_TO_1999
    )
    assert (
        registry.get("ca/unapplied_net_capital_losses_2001_to_2024")
        is UNAPPLIED_NET_CAPITAL_LOSSES_2001_TO_2024
    )
    assert registry.get("ca/net_capital_losses_claimed") is NET_CAPITAL_LOSSES_CLAIMED
    assert (
        registry.get("ca/adjusted_gross_capital_losses_1985_to_1987")
        is ADJUSTED_GROSS_CAPITAL_LOSSES_1985_TO_1987
    )
    assert (
        registry.get("ca/adjusted_gross_capital_losses_1988_and_1989")
        is ADJUSTED_GROSS_CAPITAL_LOSSES_1988_AND_1989
    )
    assert (
        registry.get("ca/adjusted_gross_capital_losses_1990_to_1999")
        is ADJUSTED_GROSS_CAPITAL_LOSSES_1990_TO_1999
    )
    assert (
        registry.get("ca/adjusted_gross_capital_losses_2001_to_2024")
        is ADJUSTED_GROSS_CAPITAL_LOSSES_2001_TO_2024
    )
    assert registry.get("ca/total_adjusted_net_capital_losses") is TOTAL_ADJUSTED_NET_CAPITAL_LOSSES
    assert (
        registry.get("ca/net_capital_losses_available_to_claim")
        is NET_CAPITAL_LOSSES_AVAILABLE_TO_CLAIM
    )
    assert registry.get("ca/net_capital_losses_of_other_years") is NET_CAPITAL_LOSSES_OF_OTHER_YEARS
    assert (
        registry.get("ca/adjusted_losses_applied_1985_to_1987")
        is ADJUSTED_LOSSES_APPLIED_1985_TO_1987
    )
    assert (
        registry.get("ca/adjusted_losses_left_after_1985_to_1987")
        is ADJUSTED_LOSSES_LEFT_AFTER_1985_TO_1987
    )
    assert (
        registry.get("ca/remaining_adjusted_losses_1985_to_1987")
        is REMAINING_ADJUSTED_LOSSES_1985_TO_1987
    )
    assert (
        registry.get("ca/net_capital_loss_balance_1985_to_1987")
        is NET_CAPITAL_LOSS_BALANCE_1985_TO_1987
    )
    assert (
        registry.get("ca/adjusted_losses_applied_1988_and_1989")
        is ADJUSTED_LOSSES_APPLIED_1988_AND_1989
    )
    assert (
        registry.get("ca/adjusted_losses_left_after_1988_and_1989")
        is ADJUSTED_LOSSES_LEFT_AFTER_1988_AND_1989
    )
    assert (
        registry.get("ca/remaining_adjusted_losses_1988_and_1989")
        is REMAINING_ADJUSTED_LOSSES_1988_AND_1989
    )
    assert (
        registry.get("ca/net_capital_loss_balance_1988_and_1989")
        is NET_CAPITAL_LOSS_BALANCE_1988_AND_1989
    )
    assert (
        registry.get("ca/adjusted_losses_applied_1990_to_1999")
        is ADJUSTED_LOSSES_APPLIED_1990_TO_1999
    )
    assert (
        registry.get("ca/adjusted_losses_left_after_1990_to_1999")
        is ADJUSTED_LOSSES_LEFT_AFTER_1990_TO_1999
    )
    assert (
        registry.get("ca/remaining_adjusted_losses_1990_to_1999")
        is REMAINING_ADJUSTED_LOSSES_1990_TO_1999
    )
    assert (
        registry.get("ca/net_capital_loss_balance_1990_to_1999")
        is NET_CAPITAL_LOSS_BALANCE_1990_TO_1999
    )
    assert (
        registry.get("ca/adjusted_losses_applied_2001_to_2024")
        is ADJUSTED_LOSSES_APPLIED_2001_TO_2024
    )
    assert (
        registry.get("ca/remaining_adjusted_losses_2001_to_2024")
        is REMAINING_ADJUSTED_LOSSES_2001_TO_2024
    )
    assert (
        registry.get("ca/net_capital_loss_balance_2001_to_2024")
        is NET_CAPITAL_LOSS_BALANCE_2001_TO_2024
    )
    assert registry.get("ca/additional_deductions") is ADDITIONAL_DEDUCTIONS
    assert registry.get("ca/deductions_from_net_income") is DEDUCTIONS_FROM_NET_INCOME


def test_the_taxable_income_kinds_are_money() -> None:
    for kind in (
        LIMITED_PARTNERSHIP_LOSSES_OF_OTHER_YEARS,
        NON_CAPITAL_LOSSES_OF_OTHER_YEARS,
        UNAPPLIED_NET_CAPITAL_LOSSES_1985_TO_1987,
        UNAPPLIED_NET_CAPITAL_LOSSES_1988_AND_1989,
        UNAPPLIED_NET_CAPITAL_LOSSES_1990_TO_1999,
        UNAPPLIED_NET_CAPITAL_LOSSES_2001_TO_2024,
        NET_CAPITAL_LOSSES_CLAIMED,
        ADJUSTED_GROSS_CAPITAL_LOSSES_1985_TO_1987,
        ADJUSTED_GROSS_CAPITAL_LOSSES_1988_AND_1989,
        ADJUSTED_GROSS_CAPITAL_LOSSES_1990_TO_1999,
        ADJUSTED_GROSS_CAPITAL_LOSSES_2001_TO_2024,
        TOTAL_ADJUSTED_NET_CAPITAL_LOSSES,
        NET_CAPITAL_LOSSES_AVAILABLE_TO_CLAIM,
        NET_CAPITAL_LOSSES_OF_OTHER_YEARS,
        ADJUSTED_LOSSES_APPLIED_1985_TO_1987,
        ADJUSTED_LOSSES_LEFT_AFTER_1985_TO_1987,
        REMAINING_ADJUSTED_LOSSES_1985_TO_1987,
        NET_CAPITAL_LOSS_BALANCE_1985_TO_1987,
        ADJUSTED_LOSSES_APPLIED_1988_AND_1989,
        ADJUSTED_LOSSES_LEFT_AFTER_1988_AND_1989,
        REMAINING_ADJUSTED_LOSSES_1988_AND_1989,
        NET_CAPITAL_LOSS_BALANCE_1988_AND_1989,
        ADJUSTED_LOSSES_APPLIED_1990_TO_1999,
        ADJUSTED_LOSSES_LEFT_AFTER_1990_TO_1999,
        REMAINING_ADJUSTED_LOSSES_1990_TO_1999,
        NET_CAPITAL_LOSS_BALANCE_1990_TO_1999,
        ADJUSTED_LOSSES_APPLIED_2001_TO_2024,
        REMAINING_ADJUSTED_LOSSES_2001_TO_2024,
        NET_CAPITAL_LOSS_BALANCE_2001_TO_2024,
        ADDITIONAL_DEDUCTIONS,
        DEDUCTIONS_FROM_NET_INCOME,
    ):
        assert kind.value_type is Decimal, kind.identifier


def test_the_deductions_the_foreign_tax_credit_subtracts_are_the_registered_ones(
    registry: ArtifactRegistry,
) -> None:
    # Form T2209 note (3), net income, "minus any:" "capital gains deduction for qualifying
    # business transfer or qualifying cooperative conversion you claimed (line 25395 of your
    # return)", "capital gains deduction you claimed (line 25400 of your return)" and "amounts
    # deductible as net employment income from a prescribed international organization, as
    # foreign income exempt under a tax treaty, or as adult basic education tuition assistance
    # (included on line 25600 of your return)". T1 lines 64 and 65 are not wired into line 68.
    assert registry.get("ca/capital_gains_deduction") is CAPITAL_GAINS_DEDUCTION
    assert registry.get("ca/exempt_income_deductions") is EXEMPT_INCOME_DEDUCTIONS


def test_the_deductions_the_foreign_tax_credit_subtracts_are_non_negative_money(
    registry: ArtifactRegistry,
) -> None:
    for kind in (
        CAPITAL_GAINS_DEDUCTION,
        EXEMPT_INCOME_DEDUCTIONS,
    ):
        assert kind.value_type is Decimal, kind.identifier
        assert kind.non_negative is True, kind.identifier
        assert registry.kind(kind.identifier) is kind


def test_the_form_t2048_kinds_are_the_registered_ones(registry: ArtifactRegistry) -> None:
    # Form T2048 (Capital Gains Deduction for Qualifying Business Transfers or Qualifying
    # Cooperative Conversions) Parts 2 to 5 and Chart A, and line 25395 (T1 line 64).
    for identifier, kind in (
        ("ca/qbt_election_eligible_amount", QBT_ELECTION_ELIGIBLE_AMOUNT),
        ("ca/qbt_percentage_allocated", QBT_PERCENTAGE_ALLOCATED),
        ("ca/qbt_amount_allocated", QBT_AMOUNT_ALLOCATED),
        ("ca/qbt_taxable_amount_allocated", QBT_TAXABLE_AMOUNT_ALLOCATED),
        ("ca/qbt_prior_years_claims", QBT_PRIOR_YEARS_CLAIMS),
        ("ca/qbt_deduction_available", QBT_DEDUCTION_AVAILABLE),
        ("ca/qbt_capital_gains", QBT_CAPITAL_GAINS),
        ("ca/qbt_2024_reserve", QBT_2024_RESERVE),
        ("ca/qbt_capital_gains_with_2024_reserve", QBT_CAPITAL_GAINS_WITH_2024_RESERVE),
        ("ca/qbt_2025_reserve", QBT_2025_RESERVE),
        ("ca/qbt_total_capital_gains", QBT_TOTAL_CAPITAL_GAINS),
        ("ca/qbt_taxable_capital_gains", QBT_TAXABLE_CAPITAL_GAINS),
        ("ca/qbt_taxable_gains_limit", QBT_TAXABLE_GAINS_LIMIT),
        ("ca/qbt_taxable_gains_not_limited", QBT_TAXABLE_GAINS_NOT_LIMITED),
        ("ca/qbt_net_capital_losses_remaining", QBT_NET_CAPITAL_LOSSES_REMAINING),
        ("ca/qbt_has_investment_expenses", QBT_HAS_INVESTMENT_EXPENSES),
        ("ca/qbt_net_investment_loss", QBT_NET_INVESTMENT_LOSS),
        ("ca/qbt_reductions_from_losses", QBT_REDUCTIONS_FROM_LOSSES),
        ("ca/qbt_deduction_limit", QBT_DEDUCTION_LIMIT),
        ("ca/qbt_maximum_deduction", QBT_MAXIMUM_DEDUCTION),
        ("ca/qbt_deduction_claimed", QBT_DEDUCTION_CLAIMED),
        ("ca/qbt_capital_gains_deduction", QBT_CAPITAL_GAINS_DEDUCTION),
        ("ca/qbt_deduction_base", QBT_DEDUCTION_BASE),
        ("ca/qbt_reduction_amount", QBT_REDUCTION_AMOUNT),
        ("ca/qbt_allocation_total", QBT_ALLOCATION_TOTAL),
        ("ca/qbt_abil_and_net_investment_loss", QBT_ABIL_AND_NET_INVESTMENT_LOSS),
        ("ca/qbt_allocation_limit", QBT_ALLOCATION_LIMIT),
        ("ca/qbt_abil_reduction", QBT_ABIL_REDUCTION),
        ("ca/qbt_net_investment_loss_reduction", QBT_NET_INVESTMENT_LOSS_REDUCTION),
        ("ca/qbt_election_is_qbt", QBT_ELECTION_IS_QBT),
        ("ca/qbt_gains_are_qsbcs_or_qffp", QBT_GAINS_ARE_QSBCS_OR_QFFP),
        ("ca/qcc_election_deduction", QCC_ELECTION_DEDUCTION),
        ("ca/qbt_election_deduction", QBT_ELECTION_DEDUCTION),
        ("ca/qbt_taxable_gains_related_to_deduction", QBT_TAXABLE_GAINS_RELATED_TO_DEDUCTION),
        (
            "ca/qsbcs_qffp_taxable_gains_related_to_deduction",
            QSBCS_QFFP_TAXABLE_GAINS_RELATED_TO_DEDUCTION,
        ),
        ("ca/qbt_net_rental_income", QBT_NET_RENTAL_INCOME),
        ("ca/qbt_net_rental_loss", QBT_NET_RENTAL_LOSS),
        ("ca/qbt_partnership_losses", QBT_PARTNERSHIP_LOSSES),
        ("ca/qbt_exploration_expenses_at_half", QBT_EXPLORATION_EXPENSES_AT_HALF),
        ("ca/qbt_other_investment_expenses", QBT_OTHER_INVESTMENT_EXPENSES),
        ("ca/qbt_chart_a_net_capital_losses_used", QBT_CHART_A_NET_CAPITAL_LOSSES_USED),
        ("ca/qbt_investment_expenses", QBT_INVESTMENT_EXPENSES),
        ("ca/qbt_dividends_and_investment_income", QBT_DIVIDENDS_AND_INVESTMENT_INCOME),
        ("ca/qbt_other_property_income", QBT_OTHER_PROPERTY_INCOME),
        ("ca/qbt_recovery_of_exploration_expenses", QBT_RECOVERY_OF_EXPLORATION_EXPENSES),
        ("ca/qbt_investment_income", QBT_INVESTMENT_INCOME),
        ("ca/qbt_chart_a_net_investment_loss", QBT_CHART_A_NET_INVESTMENT_LOSS),
    ):
        assert registry.get(identifier) is kind, identifier


def test_the_form_t2048_kinds_are_money_and_counts() -> None:
    # Line 2 "Percentage allocated to you" is a number entered as printed (50 for 50%), so money.
    for kind in (
        QBT_PERCENTAGE_ALLOCATED,
        QBT_ELECTION_ELIGIBLE_AMOUNT,
        QBT_AMOUNT_ALLOCATED,
        QBT_TAXABLE_AMOUNT_ALLOCATED,
        QBT_PRIOR_YEARS_CLAIMS,
        QBT_DEDUCTION_AVAILABLE,
        QBT_CAPITAL_GAINS,
        QBT_2024_RESERVE,
        QBT_CAPITAL_GAINS_WITH_2024_RESERVE,
        QBT_2025_RESERVE,
        QBT_TOTAL_CAPITAL_GAINS,
        QBT_TAXABLE_CAPITAL_GAINS,
        QBT_TAXABLE_GAINS_LIMIT,
        QBT_TAXABLE_GAINS_NOT_LIMITED,
        QBT_NET_CAPITAL_LOSSES_REMAINING,
        QBT_NET_INVESTMENT_LOSS,
        QBT_REDUCTIONS_FROM_LOSSES,
        QBT_DEDUCTION_LIMIT,
        QBT_MAXIMUM_DEDUCTION,
        QBT_DEDUCTION_CLAIMED,
        QBT_CAPITAL_GAINS_DEDUCTION,
        QBT_DEDUCTION_BASE,
        QBT_REDUCTION_AMOUNT,
        QBT_ALLOCATION_TOTAL,
        QBT_ABIL_AND_NET_INVESTMENT_LOSS,
        QBT_ALLOCATION_LIMIT,
        QBT_ABIL_REDUCTION,
        QBT_NET_INVESTMENT_LOSS_REDUCTION,
        QCC_ELECTION_DEDUCTION,
        QBT_ELECTION_DEDUCTION,
        QBT_TAXABLE_GAINS_RELATED_TO_DEDUCTION,
        QSBCS_QFFP_TAXABLE_GAINS_RELATED_TO_DEDUCTION,
        QBT_NET_RENTAL_INCOME,
        QBT_NET_RENTAL_LOSS,
        QBT_PARTNERSHIP_LOSSES,
        QBT_EXPLORATION_EXPENSES_AT_HALF,
        QBT_OTHER_INVESTMENT_EXPENSES,
        QBT_CHART_A_NET_CAPITAL_LOSSES_USED,
        QBT_INVESTMENT_EXPENSES,
        QBT_DIVIDENDS_AND_INVESTMENT_INCOME,
        QBT_OTHER_PROPERTY_INCOME,
        QBT_RECOVERY_OF_EXPLORATION_EXPENSES,
        QBT_INVESTMENT_INCOME,
        QBT_CHART_A_NET_INVESTMENT_LOSS,
    ):
        assert kind.value_type is Decimal, kind.identifier
        assert kind.non_negative is True, kind.identifier
    # "election is for a QBT", "gains are QSBCS/QFFP" and "you have investment expenses in 2025"
    # are 0 or 1, the pattern of the other yes/no inputs.
    for count in (
        QBT_HAS_INVESTMENT_EXPENSES,
        QBT_ELECTION_IS_QBT,
        QBT_GAINS_ARE_QSBCS_OR_QFFP,
    ):
        assert count.value_type is int, count.identifier


def test_the_form_t657_kinds_are_the_registered_ones(registry: ArtifactRegistry) -> None:
    # Form T657 (Calculation of Capital Gains Deduction) Steps 1 and 2, Charts 1, 2 and 2025, and
    # line 25400 (T1 line 65).
    for identifier, kind in (
        ("ca/t657_t2017_line_13", T657_T2017_LINE_13),
        (
            "ca/t657_net_non_eligible_taxable_capital_gains",
            T657_NET_NON_ELIGIBLE_TAXABLE_CAPITAL_GAINS,
        ),
        ("ca/t657_gains_1985_to_1991", T657_GAINS_1985_TO_1991),
        ("ca/t657_gains_1992_and_1993", T657_GAINS_1992_AND_1993),
        ("ca/t657_gains_1994", T657_GAINS_1994),
        ("ca/t657_gains_1995", T657_GAINS_1995),
        ("ca/t657_gains_1996_to_1999", T657_GAINS_1996_TO_1999),
        ("ca/t657_gains_2000", T657_GAINS_2000),
        ("ca/t657_gains_2001", T657_GAINS_2001),
        ("ca/t657_gains_2002_to_2024", T657_GAINS_2002_TO_2024),
        ("ca/t657_capital_losses_claimed_1985", T657_CAPITAL_LOSSES_CLAIMED_1985),
        ("ca/t657_abil_claimed_1985_to_2024", T657_ABIL_CLAIMED_1985_TO_2024),
        ("ca/t657_t2048_line_17217_for_2024", T657_T2048_LINE_17217_FOR_2024),
        ("ca/t657_cumulative_net_investment_loss", T657_CUMULATIVE_NET_INVESTMENT_LOSS),
        ("ca/t657_deductions_claimed_1985_to_2024", T657_DEDUCTIONS_CLAIMED_1985_TO_2024),
        ("ca/t657_chart_2_line_1", T657_CHART_2_LINE_1),
        ("ca/t657_chart_2_line_2", T657_CHART_2_LINE_2),
        ("ca/t657_chart_2_line_6", T657_CHART_2_LINE_6),
        ("ca/t657_chart_2_line_10", T657_CHART_2_LINE_10),
        ("ca/t657_chart_2_line_14", T657_CHART_2_LINE_14),
        ("ca/t657_inclusion_rate_2000", T657_INCLUSION_RATE_2000),
        ("ca/t657_chart_2_line_18", T657_CHART_2_LINE_18),
        ("ca/t657_part_1_amount_b", T657_PART_1_AMOUNT_B),
        ("ca/t657_part_1_amount_f", T657_PART_1_AMOUNT_F),
        ("ca/t657_part_1_amount_g", T657_PART_1_AMOUNT_G),
        ("ca/t657_part_1_amount_h", T657_PART_1_AMOUNT_H),
        ("ca/t657_part_1_amount_i", T657_PART_1_AMOUNT_I),
        ("ca/t657_part_1_amount_j", T657_PART_1_AMOUNT_J),
        ("ca/t657_part_1_amount_l", T657_PART_1_AMOUNT_L),
        ("ca/t657_part_2_excluded_f", T657_PART_2_EXCLUDED_F),
        ("ca/t657_part_2_excluded_g", T657_PART_2_EXCLUDED_G),
        ("ca/t657_part_2_excluded_h", T657_PART_2_EXCLUDED_H),
        ("ca/t657_part_2_amount_i", T657_PART_2_AMOUNT_I),
        ("ca/t657_part_2_amount_j", T657_PART_2_AMOUNT_J),
        ("ca/t657_part_2_amount_l", T657_PART_2_AMOUNT_L),
        ("ca/capital_gains_deduction_claimed", CAPITAL_GAINS_DEDUCTION_CLAIMED),
        ("ca/annual_gains_schedule_3_total", ANNUAL_GAINS_SCHEDULE_3_TOTAL),
        ("ca/annual_gains_line_3", ANNUAL_GAINS_LINE_3),
        ("ca/annual_gains_line_3_at_inclusion_rate", ANNUAL_GAINS_LINE_3_AT_INCLUSION_RATE),
        ("ca/annual_gains_line_5", ANNUAL_GAINS_LINE_5),
        ("ca/annual_gains_line_7", ANNUAL_GAINS_LINE_7),
        ("ca/schedule_3_line_19900", SCHEDULE_3_LINE_19900),
        ("ca/schedule_3_line_17600_not_below_zero", SCHEDULE_3_LINE_17600_NOT_BELOW_ZERO),
        ("ca/annual_gains_line_9", ANNUAL_GAINS_LINE_9),
        ("ca/annual_gains_line_10", ANNUAL_GAINS_LINE_10),
        ("ca/annual_gains_line_12", ANNUAL_GAINS_LINE_12),
        ("ca/eligible_taxable_capital_gains_2025", ELIGIBLE_TAXABLE_CAPITAL_GAINS_2025),
        (
            "ca/adjusted_net_capital_losses_of_other_years",
            ADJUSTED_NET_CAPITAL_LOSSES_OF_OTHER_YEARS,
        ),
        ("ca/abil_after_qbt_reduction", ABIL_AFTER_QBT_REDUCTION),
        ("ca/total_losses_for_annual_gains_limit", TOTAL_LOSSES_FOR_ANNUAL_GAINS_LIMIT),
        ("ca/annual_gains_limit_2025", ANNUAL_GAINS_LIMIT_2025),
        (
            "ca/eligible_taxable_capital_gains_2002_to_2025",
            ELIGIBLE_TAXABLE_CAPITAL_GAINS_2002_TO_2025,
        ),
        ("ca/cumulative_eligible_taxable_capital_gains", CUMULATIVE_ELIGIBLE_TAXABLE_CAPITAL_GAINS),
        ("ca/abil_claimed_after_1984_and_before_2025", ABIL_CLAIMED_AFTER_1984_AND_BEFORE_2025),
        ("ca/chart_1_column_g_total", CHART_1_COLUMN_G_TOTAL),
        ("ca/cumulative_losses_and_deductions", CUMULATIVE_LOSSES_AND_DEDUCTIONS),
        ("ca/cumulative_gains_limit_2025", CUMULATIVE_GAINS_LIMIT_2025),
        ("ca/chart_2_line_3", CHART_2_LINE_3),
        ("ca/chart_2_line_4", CHART_2_LINE_4),
        ("ca/chart_2_line_5", CHART_2_LINE_5),
        ("ca/chart_2_line_7", CHART_2_LINE_7),
        ("ca/chart_2_line_8", CHART_2_LINE_8),
        ("ca/chart_2_line_9", CHART_2_LINE_9),
        ("ca/chart_2_line_11", CHART_2_LINE_11),
        ("ca/chart_2_line_12", CHART_2_LINE_12),
        ("ca/chart_2_line_13", CHART_2_LINE_13),
        ("ca/chart_2_line_15", CHART_2_LINE_15),
        ("ca/chart_2_twice_ir", CHART_2_TWICE_IR),
        ("ca/chart_2_line_14_over_twice_ir", CHART_2_LINE_14_OVER_TWICE_IR),
        ("ca/chart_2_line_16", CHART_2_LINE_16),
        ("ca/chart_2_line_17", CHART_2_LINE_17),
        ("ca/chart_2_line_19", CHART_2_LINE_19),
        ("ca/chart_2_numerator_one", CHART_2_NUMERATOR_ONE),
        ("ca/chart_2025_part_1_amount_a", CHART_2025_PART_1_AMOUNT_A),
        ("ca/chart_2025_part_1_amount_c", CHART_2025_PART_1_AMOUNT_C),
        ("ca/chart_2025_part_1_amount_e", CHART_2025_PART_1_AMOUNT_E),
        ("ca/chart_2025_part_1_amounts_f_to_j", CHART_2025_PART_1_AMOUNTS_F_TO_J),
        ("ca/chart_2025_part_1_amount_k", CHART_2025_PART_1_AMOUNT_K),
        ("ca/chart_2025_part_1_amount_m", CHART_2025_PART_1_AMOUNT_M),
        ("ca/chart_2025_part_1_amount_n", CHART_2025_PART_1_AMOUNT_N),
        ("ca/chart_2025_part_1_amount_p", CHART_2025_PART_1_AMOUNT_P),
        ("ca/chart_2025_part_1_amount_q", CHART_2025_PART_1_AMOUNT_Q),
        ("ca/chart_2025_part_2_amount_a", CHART_2025_PART_2_AMOUNT_A),
        ("ca/chart_2025_part_2_amount_c", CHART_2025_PART_2_AMOUNT_C),
        ("ca/chart_2025_part_2_amount_e", CHART_2025_PART_2_AMOUNT_E),
        ("ca/chart_2025_part_2_amount_f", CHART_2025_PART_2_AMOUNT_F),
        ("ca/chart_2025_part_2_amount_g", CHART_2025_PART_2_AMOUNT_G),
        ("ca/chart_2025_part_2_amount_h", CHART_2025_PART_2_AMOUNT_H),
        ("ca/chart_2025_part_2_amounts_f_to_j", CHART_2025_PART_2_AMOUNTS_F_TO_J),
        ("ca/chart_2025_part_2_amount_k", CHART_2025_PART_2_AMOUNT_K),
        ("ca/chart_2025_part_2_amount_m", CHART_2025_PART_2_AMOUNT_M),
        ("ca/chart_2025_part_2_amount_n", CHART_2025_PART_2_AMOUNT_N),
        ("ca/chart_2025_part_2_amount_p", CHART_2025_PART_2_AMOUNT_P),
        ("ca/chart_2025_part_2_amount_q", CHART_2025_PART_2_AMOUNT_Q),
        ("ca/capital_gains_deduction", CAPITAL_GAINS_DEDUCTION),
        ("ca/t657_chart_1_column_a", T657_CHART_1_COLUMN_A),
        ("ca/t657_chart_1_column_b", T657_CHART_1_COLUMN_B),
        ("ca/t657_chart_1_column_c", T657_CHART_1_COLUMN_C),
        ("ca/t657_chart_1_column_d", T657_CHART_1_COLUMN_D),
        ("ca/t657_chart_1_rows", T657_CHART_1_ROWS),
    ):
        assert registry.get(identifier) is kind, identifier


def test_the_form_t657_amounts_are_money_non_negative_except_the_signed_lines() -> None:
    # The lines that print "if negative, show in brackets", or no floor on a gain or loss, are
    # signed; every other amount, starting or computed, is non-negative.
    signed = (
        T657_T2017_LINE_13,
        T657_PART_1_AMOUNT_I,
        T657_PART_1_AMOUNT_J,
        T657_PART_2_AMOUNT_I,
        T657_PART_2_AMOUNT_J,
        ANNUAL_GAINS_SCHEDULE_3_TOTAL,
        ANNUAL_GAINS_LINE_3,
        ANNUAL_GAINS_LINE_3_AT_INCLUSION_RATE,
        ANNUAL_GAINS_LINE_7,
        SCHEDULE_3_LINE_19900,
        ANNUAL_GAINS_LINE_10,
        ANNUAL_GAINS_LINE_12,
        ELIGIBLE_TAXABLE_CAPITAL_GAINS_2025,
        ELIGIBLE_TAXABLE_CAPITAL_GAINS_2002_TO_2025,
        CUMULATIVE_ELIGIBLE_TAXABLE_CAPITAL_GAINS,
        CHART_2025_PART_2_AMOUNT_F,
        CHART_2025_PART_2_AMOUNT_G,
        CHART_2025_PART_2_AMOUNT_H,
    )
    for kind in signed:
        assert kind.value_type is Decimal, kind.identifier
        assert kind.non_negative is False, kind.identifier
    for kind in (
        T657_NET_NON_ELIGIBLE_TAXABLE_CAPITAL_GAINS,
        T657_GAINS_1985_TO_1991,
        T657_GAINS_1992_AND_1993,
        T657_GAINS_1994,
        T657_GAINS_1995,
        T657_GAINS_1996_TO_1999,
        T657_GAINS_2000,
        T657_GAINS_2001,
        T657_GAINS_2002_TO_2024,
        T657_CAPITAL_LOSSES_CLAIMED_1985,
        T657_ABIL_CLAIMED_1985_TO_2024,
        T657_T2048_LINE_17217_FOR_2024,
        T657_CUMULATIVE_NET_INVESTMENT_LOSS,
        T657_DEDUCTIONS_CLAIMED_1985_TO_2024,
        T657_CHART_2_LINE_1,
        T657_CHART_2_LINE_2,
        T657_CHART_2_LINE_6,
        T657_CHART_2_LINE_10,
        T657_CHART_2_LINE_14,
        T657_INCLUSION_RATE_2000,
        T657_CHART_2_LINE_18,
        T657_PART_1_AMOUNT_B,
        T657_PART_1_AMOUNT_F,
        T657_PART_1_AMOUNT_G,
        T657_PART_1_AMOUNT_H,
        T657_PART_1_AMOUNT_L,
        T657_PART_2_EXCLUDED_F,
        T657_PART_2_EXCLUDED_G,
        T657_PART_2_EXCLUDED_H,
        T657_PART_2_AMOUNT_L,
        CAPITAL_GAINS_DEDUCTION_CLAIMED,
        ANNUAL_GAINS_LINE_5,
        SCHEDULE_3_LINE_17600_NOT_BELOW_ZERO,
        ANNUAL_GAINS_LINE_9,
        ADJUSTED_NET_CAPITAL_LOSSES_OF_OTHER_YEARS,
        ABIL_AFTER_QBT_REDUCTION,
        TOTAL_LOSSES_FOR_ANNUAL_GAINS_LIMIT,
        ANNUAL_GAINS_LIMIT_2025,
        ABIL_CLAIMED_AFTER_1984_AND_BEFORE_2025,
        CHART_1_COLUMN_G_TOTAL,
        CUMULATIVE_LOSSES_AND_DEDUCTIONS,
        CUMULATIVE_GAINS_LIMIT_2025,
        CHART_2_LINE_3,
        CHART_2_LINE_4,
        CHART_2_LINE_5,
        CHART_2_LINE_7,
        CHART_2_LINE_8,
        CHART_2_LINE_9,
        CHART_2_LINE_11,
        CHART_2_LINE_12,
        CHART_2_LINE_13,
        CHART_2_LINE_15,
        CHART_2_TWICE_IR,
        CHART_2_LINE_14_OVER_TWICE_IR,
        CHART_2_LINE_16,
        CHART_2_LINE_17,
        CHART_2_LINE_19,
        CHART_2_NUMERATOR_ONE,
        CHART_2025_PART_1_AMOUNT_A,
        CHART_2025_PART_1_AMOUNT_C,
        CHART_2025_PART_1_AMOUNT_E,
        CHART_2025_PART_1_AMOUNTS_F_TO_J,
        CHART_2025_PART_1_AMOUNT_K,
        CHART_2025_PART_1_AMOUNT_M,
        CHART_2025_PART_1_AMOUNT_N,
        CHART_2025_PART_1_AMOUNT_P,
        CHART_2025_PART_1_AMOUNT_Q,
        CHART_2025_PART_2_AMOUNT_A,
        CHART_2025_PART_2_AMOUNT_C,
        CHART_2025_PART_2_AMOUNT_E,
        CHART_2025_PART_2_AMOUNTS_F_TO_J,
        CHART_2025_PART_2_AMOUNT_K,
        CHART_2025_PART_2_AMOUNT_M,
        CHART_2025_PART_2_AMOUNT_N,
        CHART_2025_PART_2_AMOUNT_P,
        CHART_2025_PART_2_AMOUNT_Q,
        CAPITAL_GAINS_DEDUCTION,
        T657_CHART_1_COLUMN_A,
        T657_CHART_1_COLUMN_B,
        T657_CHART_1_COLUMN_C,
        T657_CHART_1_COLUMN_D,
    ):
        assert kind.value_type is Decimal, kind.identifier
        assert kind.non_negative is True, kind.identifier


def test_chart_1_is_a_record_list_of_one_record_for_each_year_row(
    registry: ArtifactRegistry,
) -> None:
    # Chart 1 "Calculate your net capital losses of other years (line 14 of Step 2)": columns A to
    # D of each printed year row; a cell the form prints N/A is left 0 by the filer.
    assert registry.get("ca/t657_chart_1_rows") is T657_CHART_1_ROWS
    assert isinstance(T657_CHART_1_ROWS, RecordListKind)
    assert T657_CHART_1_ROWS.fields == (
        T657_CHART_1_COLUMN_A,
        T657_CHART_1_COLUMN_B,
        T657_CHART_1_COLUMN_C,
        T657_CHART_1_COLUMN_D,
    )
