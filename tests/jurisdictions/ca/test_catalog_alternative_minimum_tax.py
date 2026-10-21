"""Registered and money kinds of the federal catalog family `alternative_minimum_tax`."""

from __future__ import annotations

from decimal import Decimal

from app.domain.artifact import ArtifactKind, ArtifactRegistry
from app.jurisdictions.ca.catalog import (
    AMT_ADJUSTMENTS_BEFORE_RATE_TOTAL,
    AMT_APPLICABLE_RATE_AMOUNT,
    AMT_CAPITAL_GAINS_ADJUSTMENTS,
    AMT_CLASS_43_1_INCOME,
    AMT_COMMISSION_EMPLOYMENT_EXPENSES,
    AMT_DEDUCTIONS_TOTAL,
    AMT_DEFERRED_PROFIT_SHARING_PLAN_DEDUCTION,
    AMT_EXCESS_EPSP_AMOUNTS,
    AMT_FILM_PROPERTY_ADJUSTMENT,
    AMT_FILM_PROPERTY_CCA_AND_CARRYING_CHARGES,
    AMT_FILM_PROPERTY_INCOME_BEFORE_CCA,
    AMT_FINANCING_EXPENSES,
    AMT_FORFEITED_SALARY_DEFERRAL_AMOUNTS,
    AMT_GRADUATED_RATE_ESTATE_CAPITAL_GAINS,
    AMT_INVESTMENT_COUNSEL_FEES,
    AMT_LEGAL_AND_ACCOUNTING_EXPENSES,
    AMT_LIFE_INSURANCE_PREMIUMS_AS_COLLATERAL,
    AMT_LIMITED_PARTNER_CARRYING_CHARGES,
    AMT_LIMITED_PARTNERSHIP_DIFFERENCE_APPLIED,
    AMT_LIMITED_PARTNERSHIP_DIFFERENCE_ELECTION,
    AMT_LIMITED_PARTNERSHIP_DIFFERENCE_NO_ELECTION,
    AMT_LIMITED_PARTNERSHIP_LOSSES_ADJUSTMENT,
    AMT_LOSSES_AND_DEDUCTIONS_SUBTOTAL,
    AMT_MORTGAGE_FORECLOSURE_CAPITAL_GAINS,
    AMT_MOVING_EXPENSES_DEDUCTION,
    AMT_NET_CAPITAL_GAINS_AFTER_ADJUSTMENTS,
    AMT_NET_CAPITAL_LOSSES_DIFFERENCE,
    AMT_NON_CAPITAL_LOSSES_ADJUSTMENT,
    AMT_NON_CAPITAL_LOSSES_DIFFERENCE,
    AMT_NON_DEDUCTIBLE_INTEREST,
    AMT_NON_DEDUCTIBLE_OFFICE_EXPENSES,
    AMT_NON_DEDUCTIBLE_PROPERTY_EXPENSES,
    AMT_OFFICE_EXPENSES_ADJUSTMENT,
    AMT_OTHER_YEARS_LOSSES_TOTAL,
    AMT_PART_1_SUBTOTAL,
    AMT_PPIP_PREMIUMS_DEDUCTION,
    AMT_PROSPECTOR_OR_GRUBSTAKER_DEDUCTION,
    AMT_PUBLICLY_LISTED_GIFTS_ADJUSTMENT,
    AMT_PUBLICLY_LISTED_GIFTS_NET,
    AMT_PUBLICLY_LISTED_GIFTS_T1170_LINE_68231,
    AMT_PUBLICLY_LISTED_GIFTS_TOTAL,
    AMT_RENTAL_PROPERTY_ADJUSTMENT,
    AMT_RENTAL_PROPERTY_CCA_AND_CARRYING_CHARGES,
    AMT_RENTAL_PROPERTY_INCOME_BEFORE_CCA,
    AMT_REPAYMENT_OF_SALARY_AND_WAGES,
    AMT_REPAYMENT_OF_WAGE_LOSS_REPLACEMENT,
    AMT_RESOURCE_EXPENDITURES,
    AMT_RESOURCE_FOREIGN_PROPERTY_INCOME,
    AMT_RESOURCE_INCOME_TOTAL,
    AMT_RESOURCE_PRODUCTION_INCOME,
    AMT_RESOURCE_PROPERTY_AND_FLOW_THROUGH_SHARES,
    AMT_SECURITY_OPTION_GIFTS_DEDUCTION,
    AMT_SECURITY_OPTION_PUBLICLY_LISTED_GIFTS,
    AMT_SECURITY_OPTIONS_D1_TOTAL,
    AMT_SECURITY_OPTIONS_D_TOTAL,
    AMT_SECURITY_OPTIONS_NET,
    AMT_T4_SECURITY_OPTIONS_BOXES_39_AND_91,
    AMT_T4_SECURITY_OPTIONS_BOXES_41_AND_92,
    AMT_T1212_LINE_2_DEFERRED_SECURITY_OPTIONS,
    AMT_TAX_SHELTER_ADJUSTMENTS,
    AMT_TAX_SHELTER_DEDUCTIBLE_AMOUNTS,
    AMT_TAX_SHELTER_LOSSES,
    AMT_TREATY_EXEMPT_CAPITAL_GAINS,
)
from tests.jurisdictions.ca.catalog_snapshot import SIGNED

PART_1_KINDS: tuple[ArtifactKind[Decimal], ...] = (
    AMT_FILM_PROPERTY_CCA_AND_CARRYING_CHARGES,
    AMT_FILM_PROPERTY_INCOME_BEFORE_CCA,
    AMT_FILM_PROPERTY_ADJUSTMENT,
    AMT_RENTAL_PROPERTY_CCA_AND_CARRYING_CHARGES,
    AMT_RENTAL_PROPERTY_INCOME_BEFORE_CCA,
    AMT_RENTAL_PROPERTY_ADJUSTMENT,
    AMT_TAX_SHELTER_LOSSES,
    AMT_TAX_SHELTER_DEDUCTIBLE_AMOUNTS,
    AMT_LIMITED_PARTNER_CARRYING_CHARGES,
    AMT_TAX_SHELTER_ADJUSTMENTS,
    AMT_PART_1_SUBTOTAL,
    AMT_MORTGAGE_FORECLOSURE_CAPITAL_GAINS,
    AMT_TREATY_EXEMPT_CAPITAL_GAINS,
    AMT_GRADUATED_RATE_ESTATE_CAPITAL_GAINS,
    AMT_CAPITAL_GAINS_ADJUSTMENTS,
    AMT_NET_CAPITAL_GAINS_AFTER_ADJUSTMENTS,
    AMT_PUBLICLY_LISTED_GIFTS_TOTAL,
    AMT_PUBLICLY_LISTED_GIFTS_T1170_LINE_68231,
    AMT_PUBLICLY_LISTED_GIFTS_NET,
    AMT_PUBLICLY_LISTED_GIFTS_ADJUSTMENT,
)

PART_9_KINDS: tuple[ArtifactKind[Decimal], ...] = (
    AMT_RESOURCE_EXPENDITURES,
    AMT_RESOURCE_PRODUCTION_INCOME,
    AMT_RESOURCE_FOREIGN_PROPERTY_INCOME,
    AMT_CLASS_43_1_INCOME,
    AMT_RESOURCE_INCOME_TOTAL,
    AMT_RESOURCE_PROPERTY_AND_FLOW_THROUGH_SHARES,
)

# Part 1 lines 28 to 32 and 35 to 38: the security options deductions.
SECURITY_OPTIONS_KINDS: tuple[ArtifactKind[Decimal], ...] = (
    AMT_T4_SECURITY_OPTIONS_BOXES_39_AND_91,
    AMT_T1212_LINE_2_DEFERRED_SECURITY_OPTIONS,
    AMT_SECURITY_OPTIONS_D_TOTAL,
    AMT_SECURITY_OPTION_PUBLICLY_LISTED_GIFTS,
    AMT_SECURITY_OPTION_GIFTS_DEDUCTION,
    AMT_SECURITY_OPTIONS_NET,
    AMT_T4_SECURITY_OPTIONS_BOXES_41_AND_92,
    AMT_PROSPECTOR_OR_GRUBSTAKER_DEDUCTION,
    AMT_DEFERRED_PROFIT_SHARING_PLAN_DEDUCTION,
    AMT_SECURITY_OPTIONS_D1_TOTAL,
)

# Part 1 lines 39 to 63: the losses of other years, the deductions of lines 54 to 62 and line 63.
LOSSES_AND_DEDUCTIONS_KINDS: tuple[ArtifactKind[Decimal], ...] = (
    AMT_LIMITED_PARTNERSHIP_DIFFERENCE_NO_ELECTION,
    AMT_LIMITED_PARTNERSHIP_DIFFERENCE_ELECTION,
    AMT_NON_CAPITAL_LOSSES_DIFFERENCE,
    AMT_NET_CAPITAL_LOSSES_DIFFERENCE,
    AMT_OTHER_YEARS_LOSSES_TOTAL,
    AMT_LIMITED_PARTNERSHIP_DIFFERENCE_APPLIED,
    AMT_LIMITED_PARTNERSHIP_LOSSES_ADJUSTMENT,
    AMT_NON_CAPITAL_LOSSES_ADJUSTMENT,
    AMT_LOSSES_AND_DEDUCTIONS_SUBTOTAL,
    AMT_MOVING_EXPENSES_DEDUCTION,
    AMT_PPIP_PREMIUMS_DEDUCTION,
    AMT_DEDUCTIONS_TOTAL,
)

# Part 1 lines 64 to 80: the non-deductible expenses and the applicable rate.
NON_DEDUCTIBLE_AND_RATE_KINDS: tuple[ArtifactKind[Decimal], ...] = (
    AMT_NON_DEDUCTIBLE_INTEREST,
    AMT_LIFE_INSURANCE_PREMIUMS_AS_COLLATERAL,
    AMT_FINANCING_EXPENSES,
    AMT_INVESTMENT_COUNSEL_FEES,
    AMT_NON_DEDUCTIBLE_PROPERTY_EXPENSES,
    AMT_COMMISSION_EMPLOYMENT_EXPENSES,
    AMT_LEGAL_AND_ACCOUNTING_EXPENSES,
    AMT_REPAYMENT_OF_SALARY_AND_WAGES,
    AMT_EXCESS_EPSP_AMOUNTS,
    AMT_FORFEITED_SALARY_DEFERRAL_AMOUNTS,
    AMT_REPAYMENT_OF_WAGE_LOSS_REPLACEMENT,
    AMT_NON_DEDUCTIBLE_OFFICE_EXPENSES,
    AMT_OFFICE_EXPENSES_ADJUSTMENT,
    AMT_ADJUSTMENTS_BEFORE_RATE_TOTAL,
    AMT_APPLICABLE_RATE_AMOUNT,
)


def test_the_alternative_minimum_tax_kinds_are_the_registered_ones(
    registry: ArtifactRegistry,
) -> None:
    assert (
        registry.get("ca/amt_film_property_cca_and_carrying_charges")
        is AMT_FILM_PROPERTY_CCA_AND_CARRYING_CHARGES
    )
    assert (
        registry.get("ca/amt_film_property_income_before_cca")
        is AMT_FILM_PROPERTY_INCOME_BEFORE_CCA
    )
    assert registry.get("ca/amt_film_property_adjustment") is AMT_FILM_PROPERTY_ADJUSTMENT
    assert (
        registry.get("ca/amt_rental_property_cca_and_carrying_charges")
        is AMT_RENTAL_PROPERTY_CCA_AND_CARRYING_CHARGES
    )
    assert (
        registry.get("ca/amt_rental_property_income_before_cca")
        is AMT_RENTAL_PROPERTY_INCOME_BEFORE_CCA
    )
    assert registry.get("ca/amt_rental_property_adjustment") is AMT_RENTAL_PROPERTY_ADJUSTMENT
    assert registry.get("ca/amt_tax_shelter_losses") is AMT_TAX_SHELTER_LOSSES
    assert (
        registry.get("ca/amt_tax_shelter_deductible_amounts") is AMT_TAX_SHELTER_DEDUCTIBLE_AMOUNTS
    )
    assert (
        registry.get("ca/amt_limited_partner_carrying_charges")
        is AMT_LIMITED_PARTNER_CARRYING_CHARGES
    )
    assert registry.get("ca/amt_tax_shelter_adjustments") is AMT_TAX_SHELTER_ADJUSTMENTS
    assert registry.get("ca/amt_part_1_subtotal") is AMT_PART_1_SUBTOTAL


def test_the_part_9_kinds_are_the_registered_ones(registry: ArtifactRegistry) -> None:
    assert registry.get("ca/amt_resource_expenditures") is AMT_RESOURCE_EXPENDITURES
    assert registry.get("ca/amt_resource_production_income") is AMT_RESOURCE_PRODUCTION_INCOME
    assert (
        registry.get("ca/amt_resource_foreign_property_income")
        is AMT_RESOURCE_FOREIGN_PROPERTY_INCOME
    )
    assert registry.get("ca/amt_class_43_1_income") is AMT_CLASS_43_1_INCOME
    assert registry.get("ca/amt_resource_income_total") is AMT_RESOURCE_INCOME_TOTAL
    assert (
        registry.get("ca/amt_resource_property_and_flow_through_shares")
        is AMT_RESOURCE_PROPERTY_AND_FLOW_THROUGH_SHARES
    )


def test_the_part_1_capital_gains_and_gifts_kinds_are_the_registered_ones(
    registry: ArtifactRegistry,
) -> None:
    assert (
        registry.get("ca/amt_mortgage_foreclosure_capital_gains")
        is AMT_MORTGAGE_FORECLOSURE_CAPITAL_GAINS
    )
    assert registry.get("ca/amt_treaty_exempt_capital_gains") is AMT_TREATY_EXEMPT_CAPITAL_GAINS
    assert (
        registry.get("ca/amt_graduated_rate_estate_capital_gains")
        is AMT_GRADUATED_RATE_ESTATE_CAPITAL_GAINS
    )
    assert registry.get("ca/amt_capital_gains_adjustments") is AMT_CAPITAL_GAINS_ADJUSTMENTS
    assert (
        registry.get("ca/amt_net_capital_gains_after_adjustments")
        is AMT_NET_CAPITAL_GAINS_AFTER_ADJUSTMENTS
    )
    assert registry.get("ca/amt_publicly_listed_gifts_total") is AMT_PUBLICLY_LISTED_GIFTS_TOTAL
    assert (
        registry.get("ca/amt_publicly_listed_gifts_t1170_line_68231")
        is AMT_PUBLICLY_LISTED_GIFTS_T1170_LINE_68231
    )
    assert registry.get("ca/amt_publicly_listed_gifts_net") is AMT_PUBLICLY_LISTED_GIFTS_NET
    assert (
        registry.get("ca/amt_publicly_listed_gifts_adjustment")
        is AMT_PUBLICLY_LISTED_GIFTS_ADJUSTMENT
    )


def test_the_security_options_kinds_are_the_registered_ones(registry: ArtifactRegistry) -> None:
    assert (
        registry.get("ca/amt_t4_security_options_boxes_39_and_91")
        is AMT_T4_SECURITY_OPTIONS_BOXES_39_AND_91
    )
    assert (
        registry.get("ca/amt_t1212_line_2_deferred_security_options")
        is AMT_T1212_LINE_2_DEFERRED_SECURITY_OPTIONS
    )
    assert registry.get("ca/amt_security_options_d_total") is AMT_SECURITY_OPTIONS_D_TOTAL
    assert (
        registry.get("ca/amt_security_option_publicly_listed_gifts")
        is AMT_SECURITY_OPTION_PUBLICLY_LISTED_GIFTS
    )
    assert (
        registry.get("ca/amt_security_option_gifts_deduction")
        is AMT_SECURITY_OPTION_GIFTS_DEDUCTION
    )
    assert registry.get("ca/amt_security_options_net") is AMT_SECURITY_OPTIONS_NET
    assert (
        registry.get("ca/amt_t4_security_options_boxes_41_and_92")
        is AMT_T4_SECURITY_OPTIONS_BOXES_41_AND_92
    )
    assert (
        registry.get("ca/amt_prospector_or_grubstaker_deduction")
        is AMT_PROSPECTOR_OR_GRUBSTAKER_DEDUCTION
    )
    assert (
        registry.get("ca/amt_deferred_profit_sharing_plan_deduction")
        is AMT_DEFERRED_PROFIT_SHARING_PLAN_DEDUCTION
    )
    assert registry.get("ca/amt_security_options_d1_total") is AMT_SECURITY_OPTIONS_D1_TOTAL


def test_the_losses_and_deductions_kinds_are_the_registered_ones(
    registry: ArtifactRegistry,
) -> None:
    assert (
        registry.get("ca/amt_limited_partnership_difference_no_election")
        is AMT_LIMITED_PARTNERSHIP_DIFFERENCE_NO_ELECTION
    )
    assert (
        registry.get("ca/amt_limited_partnership_difference_election")
        is AMT_LIMITED_PARTNERSHIP_DIFFERENCE_ELECTION
    )
    assert registry.get("ca/amt_non_capital_losses_difference") is AMT_NON_CAPITAL_LOSSES_DIFFERENCE
    assert registry.get("ca/amt_net_capital_losses_difference") is AMT_NET_CAPITAL_LOSSES_DIFFERENCE
    assert registry.get("ca/amt_other_years_losses_total") is AMT_OTHER_YEARS_LOSSES_TOTAL
    assert (
        registry.get("ca/amt_limited_partnership_difference_applied")
        is AMT_LIMITED_PARTNERSHIP_DIFFERENCE_APPLIED
    )
    assert (
        registry.get("ca/amt_limited_partnership_losses_adjustment")
        is AMT_LIMITED_PARTNERSHIP_LOSSES_ADJUSTMENT
    )
    assert registry.get("ca/amt_non_capital_losses_adjustment") is AMT_NON_CAPITAL_LOSSES_ADJUSTMENT
    assert (
        registry.get("ca/amt_losses_and_deductions_subtotal") is AMT_LOSSES_AND_DEDUCTIONS_SUBTOTAL
    )
    assert registry.get("ca/amt_moving_expenses_deduction") is AMT_MOVING_EXPENSES_DEDUCTION
    assert registry.get("ca/amt_ppip_premiums_deduction") is AMT_PPIP_PREMIUMS_DEDUCTION
    assert registry.get("ca/amt_deductions_total") is AMT_DEDUCTIONS_TOTAL


def test_the_non_deductible_expenses_and_applicable_rate_kinds_are_the_registered_ones(
    registry: ArtifactRegistry,
) -> None:
    assert registry.get("ca/amt_non_deductible_interest") is AMT_NON_DEDUCTIBLE_INTEREST
    assert (
        registry.get("ca/amt_life_insurance_premiums_as_collateral")
        is AMT_LIFE_INSURANCE_PREMIUMS_AS_COLLATERAL
    )
    assert registry.get("ca/amt_financing_expenses") is AMT_FINANCING_EXPENSES
    assert registry.get("ca/amt_investment_counsel_fees") is AMT_INVESTMENT_COUNSEL_FEES
    assert (
        registry.get("ca/amt_non_deductible_property_expenses")
        is AMT_NON_DEDUCTIBLE_PROPERTY_EXPENSES
    )
    assert (
        registry.get("ca/amt_commission_employment_expenses") is AMT_COMMISSION_EMPLOYMENT_EXPENSES
    )
    assert registry.get("ca/amt_legal_and_accounting_expenses") is AMT_LEGAL_AND_ACCOUNTING_EXPENSES
    assert registry.get("ca/amt_repayment_of_salary_and_wages") is AMT_REPAYMENT_OF_SALARY_AND_WAGES
    assert registry.get("ca/amt_excess_epsp_amounts") is AMT_EXCESS_EPSP_AMOUNTS
    assert (
        registry.get("ca/amt_forfeited_salary_deferral_amounts")
        is AMT_FORFEITED_SALARY_DEFERRAL_AMOUNTS
    )
    assert (
        registry.get("ca/amt_repayment_of_wage_loss_replacement")
        is AMT_REPAYMENT_OF_WAGE_LOSS_REPLACEMENT
    )
    assert (
        registry.get("ca/amt_non_deductible_office_expenses") is AMT_NON_DEDUCTIBLE_OFFICE_EXPENSES
    )
    assert registry.get("ca/amt_office_expenses_adjustment") is AMT_OFFICE_EXPENSES_ADJUSTMENT
    assert registry.get("ca/amt_adjustments_before_rate_total") is AMT_ADJUSTMENTS_BEFORE_RATE_TOTAL
    assert registry.get("ca/amt_applicable_rate_amount") is AMT_APPLICABLE_RATE_AMOUNT


def test_the_alternative_minimum_tax_kinds_are_money() -> None:
    for kind in (
        PART_1_KINDS
        + PART_9_KINDS
        + SECURITY_OPTIONS_KINDS
        + LOSSES_AND_DEDUCTIONS_KINDS
        + NON_DEDUCTIBLE_AND_RATE_KINDS
    ):
        assert kind.value_type is Decimal, kind.identifier


def test_the_bracketed_lines_are_signed_and_the_rest_are_not_below_zero() -> None:
    for kind in (
        PART_1_KINDS
        + PART_9_KINDS
        + SECURITY_OPTIONS_KINDS
        + LOSSES_AND_DEDUCTIONS_KINDS
        + NON_DEDUCTIBLE_AND_RATE_KINDS
    ):
        assert kind.non_negative is (kind.identifier not in SIGNED), kind.identifier
