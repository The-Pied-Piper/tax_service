"""Registered and money kinds of the federal catalog family `alternative_minimum_tax`."""

from __future__ import annotations

from decimal import Decimal

from app.domain.artifact import Artifact, ArtifactKind, ArtifactRegistry
from app.jurisdictions.ca.catalog import (
    AMT_ADJUSTED_INCOME_WITH_GAINS,
    AMT_ADJUSTED_INCOME_WITH_SECURITY_OPTIONS,
    AMT_ADJUSTED_TAXABLE_INCOME,
    AMT_ADJUSTMENTS_AFTER_RATE_TOTAL,
    AMT_ADJUSTMENTS_BEFORE_RATE_TOTAL,
    AMT_ADJUSTMENTS_WITH_LIFETIME_EXEMPTION_TOTAL,
    AMT_AMOUNT_A_MINUS_AMOUNT_B,
    AMT_APPLICABLE_RATE_AMOUNT,
    AMT_BASIC_EXEMPTION,
    AMT_BASIC_FEDERAL_TAX,
    AMT_CAPITAL_GAINS_ADDED,
    AMT_CAPITAL_GAINS_ADJUSTMENTS,
    AMT_CAPITAL_GAINS_DEDUCTIONS_TOTAL,
    AMT_CAPITAL_GAINS_DIFFERENCE,
    AMT_CLASS_43_1_INCOME,
    AMT_COMMISSION_EMPLOYMENT_EXPENSES,
    AMT_CREDITS_ADJUSTMENTS_TOTAL,
    AMT_CREDITS_TOTAL,
    AMT_DEDUCTIONS_TOTAL,
    AMT_DEFERRED_PROFIT_SHARING_PLAN_DEDUCTION,
    AMT_DIVIDENDS_ADJUSTMENTS_TOTAL,
    AMT_DIVIDENDS_DIFFERENCE_ADJUSTMENT,
    AMT_DIVIDENDS_OTHER_THAN_ELIGIBLE_ADJUSTMENT,
    AMT_DONATIONS_AND_GIFTS_ADJUSTMENT,
    AMT_EXCESS_EPSP_AMOUNTS,
    AMT_FEDERAL_LOGGING_TAX_CREDIT,
    AMT_FEDERAL_SURTAX,
    AMT_FEDERAL_SURTAX_AT_48_PERCENT,
    AMT_FEDERAL_SURTAX_IF_NON_RESIDENT,
    AMT_FEDERAL_SURTAX_MULTIPLE_JURISDICTIONS,
    AMT_FEDERAL_TAX_PAYABLE,
    AMT_FEDERAL_TAX_WITH_SURTAX_AND_RECAPTURE,
    AMT_FILM_PROPERTY_ADJUSTMENT,
    AMT_FILM_PROPERTY_CCA_AND_CARRYING_CHARGES,
    AMT_FILM_PROPERTY_INCOME_BEFORE_CCA,
    AMT_FINANCING_EXPENSES,
    AMT_FOREIGN_AND_LOGGING_CREDITS_TOTAL,
    AMT_FORFEITED_SALARY_DEFERRAL_AMOUNTS,
    AMT_GRADUATED_RATE_ESTATE_CAPITAL_GAINS,
    AMT_GROSS_MINIMUM_AMOUNT,
    AMT_INVESTMENT_COUNSEL_FEES,
    AMT_INVESTMENT_TAX_CREDIT,
    AMT_INVESTMENT_TAX_CREDIT_CLAIM,
    AMT_LEGAL_AND_ACCOUNTING_EXPENSES,
    AMT_LIFE_INSURANCE_PREMIUMS_AS_COLLATERAL,
    AMT_LIFETIME_EXEMPTION_ADJUSTMENT,
    AMT_LIMITED_PARTNER_CARRYING_CHARGES,
    AMT_LIMITED_PARTNERSHIP_DIFFERENCE_APPLIED,
    AMT_LIMITED_PARTNERSHIP_DIFFERENCE_ELECTION,
    AMT_LIMITED_PARTNERSHIP_DIFFERENCE_NO_ELECTION,
    AMT_LIMITED_PARTNERSHIP_LOSSES_ADJUSTMENT,
    AMT_LINE_3_HAS_AMOUNT,
    AMT_LOSSES_AND_DEDUCTIONS_SUBTOTAL,
    AMT_MAXIMUM_CARRYOVER_APPLIED,
    AMT_MAXIMUM_CARRYOVER_CLAIM,
    AMT_MINIMUM_AMOUNT,
    AMT_MINIMUM_TAX_CARRYOVER_APPLIED,
    AMT_MINIMUM_TAX_CARRYOVER_CLAIM,
    AMT_MINIMUM_TAX_CARRYOVER_FROM_PREVIOUS_YEARS,
    AMT_MORTGAGE_FORECLOSURE_CAPITAL_GAINS,
    AMT_MOVING_EXPENSES_DEDUCTION,
    AMT_NET_ADJUSTED_TAXABLE_INCOME,
    AMT_NET_CAPITAL_GAINS_AFTER_ADJUSTMENTS,
    AMT_NET_CAPITAL_LOSSES_DIFFERENCE,
    AMT_NON_CAPITAL_LOSSES_ADJUSTMENT,
    AMT_NON_CAPITAL_LOSSES_DIFFERENCE,
    AMT_NON_DEDUCTIBLE_INTEREST,
    AMT_NON_DEDUCTIBLE_OFFICE_EXPENSES,
    AMT_NON_DEDUCTIBLE_PROPERTY_EXPENSES,
    AMT_NON_REFUNDABLE_CREDITS_ADJUSTMENT,
    AMT_NON_RESIDENT_OR_DEEMED_RESIDENT,
    AMT_OFFICE_EXPENSES_ADJUSTMENT,
    AMT_OTHER_YEARS_LOSSES_TOTAL,
    AMT_PART_1_SUBTOTAL,
    AMT_PPIP_PREMIUMS_DEDUCTION,
    AMT_PROSPECTOR_OR_GRUBSTAKER_DEDUCTION,
    AMT_PUBLICLY_LISTED_GIFTS_ADJUSTMENT,
    AMT_PUBLICLY_LISTED_GIFTS_NET,
    AMT_PUBLICLY_LISTED_GIFTS_T1170_LINE_68231,
    AMT_PUBLICLY_LISTED_GIFTS_TOTAL,
    AMT_QBT_CAPITAL_GAINS_DEDUCTION_DIFFERENCE,
    AMT_QBT_CAPITAL_GAINS_DEDUCTION_DOUBLED,
    AMT_REGULAR_NET_FEDERAL_TAX_PAYABLE,
    AMT_REGULAR_TAX_CREDITS_TOTAL,
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
    AMT_SECTION_119_FORMER_RESIDENT_CREDIT,
    AMT_SECURITY_OPTION_GIFTS_DEDUCTION,
    AMT_SECURITY_OPTION_PUBLICLY_LISTED_GIFTS,
    AMT_SECURITY_OPTIONS_AND_LOSSES_TOTAL,
    AMT_SECURITY_OPTIONS_D1_TOTAL,
    AMT_SECURITY_OPTIONS_D_TOTAL,
    AMT_SECURITY_OPTIONS_NET,
    AMT_SPLIT_INCOME_AND_CREDITS_TOTAL,
    AMT_T4_SECURITY_OPTIONS_BOXES_39_AND_91,
    AMT_T4_SECURITY_OPTIONS_BOXES_41_AND_92,
    AMT_T1212_LINE_2_DEFERRED_SECURITY_OPTIONS,
    AMT_T2038_AMOUNT_I,
    AMT_T2203_COLUMN_5_PERCENTAGE,
    AMT_TAX_PAYABLE_AFTER_CREDITS,
    AMT_TAX_PAYABLE_BEFORE_MINIMUM_TAX_CARRYOVER,
    AMT_TAX_PAYABLE_WITH_ITC_RECAPTURE,
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
    AMT_CAPITAL_GAINS_DIFFERENCE,
    AMT_CAPITAL_GAINS_ADDED,
    AMT_ADJUSTED_INCOME_WITH_GAINS,
    AMT_ADJUSTED_INCOME_WITH_SECURITY_OPTIONS,
    AMT_SECURITY_OPTIONS_AND_LOSSES_TOTAL,
    AMT_ADJUSTMENTS_AFTER_RATE_TOTAL,
    AMT_DIVIDENDS_OTHER_THAN_ELIGIBLE_ADJUSTMENT,
    AMT_AMOUNT_A_MINUS_AMOUNT_B,
    AMT_DIVIDENDS_DIFFERENCE_ADJUSTMENT,
    AMT_DIVIDENDS_ADJUSTMENTS_TOTAL,
    AMT_LIFETIME_EXEMPTION_ADJUSTMENT,
    AMT_ADJUSTMENTS_WITH_LIFETIME_EXEMPTION_TOTAL,
    AMT_QBT_CAPITAL_GAINS_DEDUCTION_DOUBLED,
    AMT_QBT_CAPITAL_GAINS_DEDUCTION_DIFFERENCE,
    AMT_CAPITAL_GAINS_DEDUCTIONS_TOTAL,
    AMT_ADJUSTED_TAXABLE_INCOME,
    AMT_BASIC_EXEMPTION,
    AMT_NET_ADJUSTED_TAXABLE_INCOME,
    AMT_GROSS_MINIMUM_AMOUNT,
    AMT_NON_REFUNDABLE_CREDITS_ADJUSTMENT,
    AMT_DONATIONS_AND_GIFTS_ADJUSTMENT,
    AMT_FEDERAL_LOGGING_TAX_CREDIT,
    AMT_SECTION_119_FORMER_RESIDENT_CREDIT,
    AMT_CREDITS_ADJUSTMENTS_TOTAL,
    AMT_MINIMUM_AMOUNT,
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

# Part 3 lines 1 to 15: the federal surtax, the credits and the regular net federal tax payable,
# with the T2203 percentage and the two counts that choose the surtax line 4 takes.
PART_3_KINDS: tuple[ArtifactKind[Decimal], ...] = (
    AMT_FEDERAL_SURTAX_AT_48_PERCENT,
    AMT_FEDERAL_SURTAX_MULTIPLE_JURISDICTIONS,
    AMT_FEDERAL_SURTAX_IF_NON_RESIDENT,
    AMT_FEDERAL_SURTAX,
    AMT_FEDERAL_TAX_WITH_SURTAX_AND_RECAPTURE,
    AMT_T2203_COLUMN_5_PERCENTAGE,
    AMT_FOREIGN_AND_LOGGING_CREDITS_TOTAL,
    AMT_FEDERAL_TAX_PAYABLE,
    AMT_INVESTMENT_TAX_CREDIT_CLAIM,
    AMT_T2038_AMOUNT_I,
    AMT_INVESTMENT_TAX_CREDIT,
    AMT_REGULAR_TAX_CREDITS_TOTAL,
    AMT_REGULAR_NET_FEDERAL_TAX_PAYABLE,
)
PART_3_COUNTS: tuple[ArtifactKind[int], ...] = (
    AMT_NON_RESIDENT_OR_DEEMED_RESIDENT,
    AMT_LINE_3_HAS_AMOUNT,
)


# Part 2 lines 1 to 7 and Part 8 lines 1 to 12: the basic federal tax and the minimum tax
# carryover, with the carryover claim (line 12) and the cap on it.
PART_2_AND_8_KINDS: tuple[ArtifactKind[Decimal], ...] = (
    AMT_CREDITS_TOTAL,
    AMT_TAX_PAYABLE_BEFORE_MINIMUM_TAX_CARRYOVER,
    AMT_BASIC_FEDERAL_TAX,
    AMT_MINIMUM_TAX_CARRYOVER_FROM_PREVIOUS_YEARS,
    AMT_TAX_PAYABLE_WITH_ITC_RECAPTURE,
    AMT_SPLIT_INCOME_AND_CREDITS_TOTAL,
    AMT_TAX_PAYABLE_AFTER_CREDITS,
    AMT_MAXIMUM_CARRYOVER_APPLIED,
    AMT_MAXIMUM_CARRYOVER_CLAIM,
    AMT_MINIMUM_TAX_CARRYOVER_CLAIM,
    AMT_MINIMUM_TAX_CARRYOVER_APPLIED,
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


def test_the_part_1_lines_22_23_and_27_kinds_are_the_registered_ones(
    registry: ArtifactRegistry,
) -> None:
    assert registry.get("ca/amt_capital_gains_difference") is AMT_CAPITAL_GAINS_DIFFERENCE
    assert registry.get("ca/amt_capital_gains_added") is AMT_CAPITAL_GAINS_ADDED
    assert registry.get("ca/amt_adjusted_income_with_gains") is AMT_ADJUSTED_INCOME_WITH_GAINS


def test_the_part_1_lines_33_44_and_82_kinds_are_the_registered_ones(
    registry: ArtifactRegistry,
) -> None:
    assert (
        registry.get("ca/amt_adjusted_income_with_security_options")
        is AMT_ADJUSTED_INCOME_WITH_SECURITY_OPTIONS
    )
    assert (
        registry.get("ca/amt_security_options_and_losses_total")
        is AMT_SECURITY_OPTIONS_AND_LOSSES_TOTAL
    )
    assert registry.get("ca/amt_adjustments_after_rate_total") is AMT_ADJUSTMENTS_AFTER_RATE_TOTAL


def test_the_part_1_lines_84_to_89_kinds_are_the_registered_ones(
    registry: ArtifactRegistry,
) -> None:
    assert (
        registry.get("ca/amt_dividends_other_than_eligible_adjustment")
        is AMT_DIVIDENDS_OTHER_THAN_ELIGIBLE_ADJUSTMENT
    )
    assert registry.get("ca/amt_amount_a_minus_amount_b") is AMT_AMOUNT_A_MINUS_AMOUNT_B
    assert (
        registry.get("ca/amt_dividends_difference_adjustment")
        is AMT_DIVIDENDS_DIFFERENCE_ADJUSTMENT
    )
    assert registry.get("ca/amt_dividends_adjustments_total") is AMT_DIVIDENDS_ADJUSTMENTS_TOTAL
    assert registry.get("ca/amt_lifetime_exemption_adjustment") is AMT_LIFETIME_EXEMPTION_ADJUSTMENT
    assert (
        registry.get("ca/amt_adjustments_with_lifetime_exemption_total")
        is AMT_ADJUSTMENTS_WITH_LIFETIME_EXEMPTION_TOTAL
    )
    assert (
        registry.get("ca/amt_qbt_capital_gains_deduction_doubled")
        is AMT_QBT_CAPITAL_GAINS_DEDUCTION_DOUBLED
    )


def test_the_part_1_lines_91_to_103_kinds_are_the_registered_ones(
    registry: ArtifactRegistry,
) -> None:
    assert (
        registry.get("ca/amt_qbt_capital_gains_deduction_difference")
        is AMT_QBT_CAPITAL_GAINS_DEDUCTION_DIFFERENCE
    )
    assert (
        registry.get("ca/amt_capital_gains_deductions_total") is AMT_CAPITAL_GAINS_DEDUCTIONS_TOTAL
    )
    assert registry.get("ca/amt_adjusted_taxable_income") is AMT_ADJUSTED_TAXABLE_INCOME
    assert registry.get("ca/amt_basic_exemption") is AMT_BASIC_EXEMPTION
    assert registry.get("ca/amt_net_adjusted_taxable_income") is AMT_NET_ADJUSTED_TAXABLE_INCOME
    assert registry.get("ca/amt_gross_minimum_amount") is AMT_GROSS_MINIMUM_AMOUNT
    assert (
        registry.get("ca/amt_non_refundable_credits_adjustment")
        is AMT_NON_REFUNDABLE_CREDITS_ADJUSTMENT
    )
    assert (
        registry.get("ca/amt_donations_and_gifts_adjustment") is AMT_DONATIONS_AND_GIFTS_ADJUSTMENT
    )
    assert registry.get("ca/amt_federal_logging_tax_credit") is AMT_FEDERAL_LOGGING_TAX_CREDIT
    assert (
        registry.get("ca/amt_section_119_former_resident_credit")
        is AMT_SECTION_119_FORMER_RESIDENT_CREDIT
    )
    assert registry.get("ca/amt_credits_adjustments_total") is AMT_CREDITS_ADJUSTMENTS_TOTAL
    assert registry.get("ca/amt_minimum_amount") is AMT_MINIMUM_AMOUNT


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


def test_the_part_2_and_part_8_kinds_are_the_registered_ones(
    registry: ArtifactRegistry,
) -> None:
    assert registry.get("ca/amt_credits_total") is AMT_CREDITS_TOTAL
    assert (
        registry.get("ca/amt_tax_payable_before_minimum_tax_carryover")
        is AMT_TAX_PAYABLE_BEFORE_MINIMUM_TAX_CARRYOVER
    )
    assert registry.get("ca/amt_basic_federal_tax") is AMT_BASIC_FEDERAL_TAX
    assert (
        registry.get("ca/amt_minimum_tax_carryover_from_previous_years")
        is AMT_MINIMUM_TAX_CARRYOVER_FROM_PREVIOUS_YEARS
    )
    assert (
        registry.get("ca/amt_tax_payable_with_itc_recapture") is AMT_TAX_PAYABLE_WITH_ITC_RECAPTURE
    )
    assert (
        registry.get("ca/amt_split_income_and_credits_total") is AMT_SPLIT_INCOME_AND_CREDITS_TOTAL
    )
    assert registry.get("ca/amt_tax_payable_after_credits") is AMT_TAX_PAYABLE_AFTER_CREDITS
    assert registry.get("ca/amt_maximum_carryover_applied") is AMT_MAXIMUM_CARRYOVER_APPLIED
    assert registry.get("ca/amt_maximum_carryover_claim") is AMT_MAXIMUM_CARRYOVER_CLAIM
    assert registry.get("ca/amt_minimum_tax_carryover_claim") is AMT_MINIMUM_TAX_CARRYOVER_CLAIM
    assert registry.get("ca/amt_minimum_tax_carryover_applied") is AMT_MINIMUM_TAX_CARRYOVER_APPLIED


def test_the_part_3_kinds_are_the_registered_ones(registry: ArtifactRegistry) -> None:
    assert registry.get("ca/amt_federal_surtax_at_48_percent") is AMT_FEDERAL_SURTAX_AT_48_PERCENT
    assert registry.get("ca/amt_t2203_column_5_percentage") is AMT_T2203_COLUMN_5_PERCENTAGE
    assert (
        registry.get("ca/amt_federal_surtax_multiple_jurisdictions")
        is AMT_FEDERAL_SURTAX_MULTIPLE_JURISDICTIONS
    )
    assert (
        registry.get("ca/amt_federal_surtax_if_non_resident") is AMT_FEDERAL_SURTAX_IF_NON_RESIDENT
    )
    assert registry.get("ca/amt_federal_surtax") is AMT_FEDERAL_SURTAX
    assert (
        registry.get("ca/amt_federal_tax_with_surtax_and_recapture")
        is AMT_FEDERAL_TAX_WITH_SURTAX_AND_RECAPTURE
    )
    assert (
        registry.get("ca/amt_foreign_and_logging_credits_total")
        is AMT_FOREIGN_AND_LOGGING_CREDITS_TOTAL
    )
    assert registry.get("ca/amt_federal_tax_payable") is AMT_FEDERAL_TAX_PAYABLE
    assert registry.get("ca/amt_investment_tax_credit_claim") is AMT_INVESTMENT_TAX_CREDIT_CLAIM
    assert registry.get("ca/amt_t2038_amount_i") is AMT_T2038_AMOUNT_I
    assert registry.get("ca/amt_investment_tax_credit") is AMT_INVESTMENT_TAX_CREDIT
    assert registry.get("ca/amt_regular_tax_credits_total") is AMT_REGULAR_TAX_CREDITS_TOTAL
    assert (
        registry.get("ca/amt_regular_net_federal_tax_payable")
        is AMT_REGULAR_NET_FEDERAL_TAX_PAYABLE
    )


def test_the_part_3_counts_are_the_registered_ones(registry: ArtifactRegistry) -> None:
    for kind in PART_3_COUNTS:
        assert registry.get(kind.identifier) is kind


def test_the_alternative_minimum_tax_kinds_are_money() -> None:
    for kind in (
        PART_1_KINDS
        + PART_9_KINDS
        + SECURITY_OPTIONS_KINDS
        + LOSSES_AND_DEDUCTIONS_KINDS
        + NON_DEDUCTIBLE_AND_RATE_KINDS
        + PART_2_AND_8_KINDS
        + PART_3_KINDS
    ):
        assert kind.value_type is Decimal, kind.identifier


def test_the_bracketed_lines_are_signed_and_the_rest_are_not_below_zero() -> None:
    for kind in (
        PART_1_KINDS
        + PART_9_KINDS
        + SECURITY_OPTIONS_KINDS
        + LOSSES_AND_DEDUCTIONS_KINDS
        + NON_DEDUCTIBLE_AND_RATE_KINDS
        + PART_2_AND_8_KINDS
        + PART_3_KINDS
    ):
        assert kind.non_negative is (kind.identifier not in SIGNED), kind.identifier


def test_the_federal_surtax_at_48_percent_holds_a_negative_base() -> None:
    # Part 3 line 2, "Multiply the amount from line 1 by 48%.", with line 1 the basic federal tax,
    # which is negative when the credits exceed the tax: 48% of a negative amount is negative,
    # and the kind holds it, as the form prints no floor.
    assert Artifact(AMT_FEDERAL_SURTAX_AT_48_PERCENT, Decimal("-567.29")).value == Decimal(
        "-567.29"
    )
