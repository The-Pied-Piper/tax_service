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
    DEDUCTIONS_FROM_NET_INCOME,
    LIMITED_PARTNERSHIP_LOSSES_OF_OTHER_YEARS,
    NET_CAPITAL_LOSS_BALANCE_1985_TO_1987,
    NET_CAPITAL_LOSS_BALANCE_1988_AND_1989,
    NET_CAPITAL_LOSS_BALANCE_1990_TO_1999,
    NET_CAPITAL_LOSS_BALANCE_2001_TO_2024,
    NET_CAPITAL_LOSSES_AVAILABLE_TO_CLAIM,
    NET_CAPITAL_LOSSES_CLAIMED,
    NET_CAPITAL_LOSSES_OF_OTHER_YEARS,
    NON_CAPITAL_LOSSES_OF_OTHER_YEARS,
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
