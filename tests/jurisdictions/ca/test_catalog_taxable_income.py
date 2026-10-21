"""Registered and money kinds of the federal catalog family `taxable_income`."""

from __future__ import annotations

from decimal import Decimal

from app.domain.artifact import ArtifactRegistry
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
    CAPITAL_GAINS_DEDUCTION,
    DEDUCTIONS_FROM_NET_INCOME,
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
    TAXABLE_INCOME,
    TOTAL_ADJUSTED_NET_CAPITAL_LOSSES,
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
