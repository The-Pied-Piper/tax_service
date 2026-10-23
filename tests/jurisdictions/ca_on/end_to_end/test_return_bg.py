"""CA-ON 2025 end to end: return bg."""

from __future__ import annotations

import pytest

from app.domain.errors import InputAboveBoundError
from app.domain.worksheet import Worksheet
from app.jurisdictions.ca.catalog import (
    AMT_ADJUSTED_INCOME_WITH_GAINS,
    AMT_ADJUSTED_INCOME_WITH_SECURITY_OPTIONS,
    AMT_ADJUSTED_TAXABLE_INCOME,
    AMT_ADJUSTMENTS_AFTER_RATE_TOTAL,
    AMT_ADJUSTMENTS_BEFORE_RATE_TOTAL,
    AMT_ADJUSTMENTS_WITH_LIFETIME_EXEMPTION_TOTAL,
    AMT_ALTERNATIVE_MINIMUM_TAX_PAYABLE,
    AMT_AMOUNT_A_MINUS_AMOUNT_B,
    AMT_APPLICABLE_RATE_AMOUNT,
    AMT_BASIC_EXEMPTION,
    AMT_BASIC_FEDERAL_TAX,
    AMT_BASIC_FEDERAL_TAX_LESS_SPLIT_INCOME_TAX,
    AMT_CAPITAL_GAINS_ADDED,
    AMT_CAPITAL_GAINS_ADJUSTMENTS,
    AMT_CAPITAL_GAINS_DEDUCTIONS_TOTAL,
    AMT_CAPITAL_GAINS_DIFFERENCE,
    AMT_CREDITS_ADJUSTMENTS_TOTAL,
    AMT_CREDITS_TOTAL,
    AMT_DEDUCTIONS_TOTAL,
    AMT_DIVIDENDS_ADJUSTMENTS_TOTAL,
    AMT_DIVIDENDS_DIFFERENCE_ADJUSTMENT,
    AMT_DIVIDENDS_OTHER_THAN_ELIGIBLE_ADJUSTMENT,
    AMT_DONATIONS_AND_GIFTS_ADJUSTMENT,
    AMT_FEDERAL_SURTAX,
    AMT_FEDERAL_SURTAX_AT_48_PERCENT,
    AMT_FEDERAL_SURTAX_MULTIPLE_JURISDICTIONS,
    AMT_FEDERAL_TAX_PAYABLE_UNDER_MINIMUM_TAX,
    AMT_FEDERAL_TAX_UNDER_MINIMUM_TAX,
    AMT_FEDERAL_TAX_WITH_SURTAX_AND_RECAPTURE,
    AMT_FILM_PROPERTY_ADJUSTMENT,
    AMT_FOREIGN_CAPITAL_GAINS_NON_TAXABLE,
    AMT_FOREIGN_INCOME_LIMIT,
    AMT_FOREIGN_NON_BUSINESS_TAX_TWO_THIRDS,
    AMT_FOREIGN_TAX_CREDIT_LESSER,
    AMT_FOREIGN_TAXES_PAID,
    AMT_GREATER_OF_BASIC_TAX_AND_MINIMUM_AMOUNT,
    AMT_GROSS_MINIMUM_AMOUNT,
    AMT_INVESTMENT_TAX_CREDIT,
    AMT_INVESTMENT_TAX_CREDIT_LESS_PART_D,
    AMT_LIFETIME_EXEMPTION_ADJUSTMENT,
    AMT_LIMITED_PARTNERSHIP_DIFFERENCE_APPLIED,
    AMT_LIMITED_PARTNERSHIP_LOSSES_ADJUSTMENT,
    AMT_LINE_3_HAS_AMOUNT,
    AMT_LOSSES_AND_DEDUCTIONS_SUBTOTAL,
    AMT_MAXIMUM_CARRYOVER_APPLIED,
    AMT_MAXIMUM_CARRYOVER_CLAIM,
    AMT_MINIMUM_AMOUNT,
    AMT_MINIMUM_TAX_AFTER_REGULAR_TAX,
    AMT_MINIMUM_TAX_CARRYOVER_APPLIED,
    AMT_MORTGAGE_FORECLOSURE_CAPITAL_GAINS,
    AMT_NET_ADJUSTED_TAXABLE_INCOME,
    AMT_NET_CAPITAL_GAINS_AFTER_ADJUSTMENTS,
    AMT_NET_MINIMUM_TAX_PAYABLE,
    AMT_NON_CAPITAL_LOSSES_ADJUSTMENT,
    AMT_NON_DEDUCTIBLE_OFFICE_EXPENSES,
    AMT_NON_DEDUCTIBLE_PROPERTY_EXPENSES,
    AMT_NON_REFUNDABLE_CREDITS_ADJUSTMENT,
    AMT_OFFICE_EXPENSES_ADJUSTMENT,
    AMT_OTHER_YEARS_LOSSES_TOTAL,
    AMT_PART_1_SUBTOTAL,
    AMT_PART_5_LINE_11_IS_POSITIVE,
    AMT_PART_6_FEDERAL_SURTAX,
    AMT_PART_6_HAS_AMOUNT_ON_LINE_10,
    AMT_PART_6_SURTAX_AT_48_PERCENT,
    AMT_PART_6_SURTAX_IF_NON_RESIDENT,
    AMT_PART_6_SURTAX_MULTIPLE_JURISDICTIONS,
    AMT_PART_6_TAX_WITH_SURTAX,
    AMT_PUBLICLY_LISTED_GIFTS_ADJUSTMENT,
    AMT_PUBLICLY_LISTED_GIFTS_NET,
    AMT_QBT_CAPITAL_GAINS_DEDUCTION_DIFFERENCE,
    AMT_QBT_CAPITAL_GAINS_DEDUCTION_DOUBLED,
    AMT_REGULAR_NET_FEDERAL_TAX_PAYABLE,
    AMT_REGULAR_NET_TAX_LESS_SURTAX,
    AMT_REGULAR_TAX_CREDITS_TOTAL,
    AMT_RENTAL_PROPERTY_ADJUSTMENT,
    AMT_RESOURCE_INCOME_TOTAL,
    AMT_RESOURCE_PROPERTY_AND_FLOW_THROUGH_SHARES,
    AMT_SECURITY_OPTION_GIFTS_DEDUCTION,
    AMT_SECURITY_OPTIONS_AND_LOSSES_TOTAL,
    AMT_SECURITY_OPTIONS_D1_TOTAL,
    AMT_SECURITY_OPTIONS_D_TOTAL,
    AMT_SECURITY_OPTIONS_NET,
    AMT_SPECIAL_FOREIGN_TAX_CREDIT,
    AMT_SPLIT_INCOME_AND_CREDITS_TOTAL,
    AMT_TAX_PAYABLE_AFTER_CREDITS,
    AMT_TAX_PAYABLE_BEFORE_MINIMUM_TAX_CARRYOVER,
    AMT_TAX_PAYABLE_WITH_ITC_RECAPTURE,
    AMT_TAX_SHELTER_ADJUSTMENTS,
    AMT_TOTAL_FOREIGN_INCOME,
    CAPITAL_GAIN,
    CREDITS_AGAINST_BASIC_FEDERAL_TAX,
    FEDERAL_FOREIGN_TAX_CREDIT,
    FEDERAL_TAX_AFTER_CREDITS,
    FEDERAL_TAX_LESS_CREDITS,
    FEDERAL_TAX_LINE_41700,
    NET_FEDERAL_TAX,
    REFUND_OR_BALANCE_OWING,
    SPLIT_INCOME_LINE_22,
    SPLIT_INCOME_LINE_24,
    SPLIT_INCOME_LINE_29,
    SPLIT_INCOME_LINE_30,
    TAXABLE_CAPITAL_GAINS,
    TAXABLE_INCOME,
)
from tests.jurisdictions.ca_on.end_to_end.support import D, Disposition, compute


def return_bg(
    film_cca: str = "9000.00",
    film_income: str = "4000.00",
    rental_cca: str = "7000.00",
    rental_income: str = "9000.00",
    shelter_losses: str = "1000.00",
    shelter_deductible: str = "500.00",
    limited_partner_carrying: str = "250.00",
    *,
    share_dispositions: tuple[Disposition, ...] = (("5000", "3000", "0"),),
    qffp_foreclosure_dispositions: tuple[Disposition, ...] = (),
    resource_expenditures: str = "5000.00",
    resource_production: str = "2000.00",
    resource_foreign: str = "1000.00",
    class_43_1: str = "500.00",
    treaty_exempt: str = "200.00",
    graduated_rate_estate: str = "100.00",
    gifts_total: str = "3000.00",
    gifts_line_68231: str = "1000.00",
    security_t4_39_and_91: str = "1000.00",
    security_t1212: str = "400.00",
    security_gifts: str = "500.00",
    security_t4_41_and_92: str = "300.00",
    prospector: str = "100.00",
    deferred_profit_sharing: str = "50.00",
    limited_partnership_no_election: str = "600.00",
    non_capital_difference: str = "100.00",
    net_capital_difference: str = "50.00",
    moving_expenses: str = "200.00",
    non_deductible_interest: str = "300.00",
    life_insurance_premiums: str = "100.00",
    investment_counsel_fees: str = "50.00",
    commission_employment: str = "150.00",
    employment_income: str = "60000",
    carryover_from_previous_years: str = "0",
    carryover_claim: str = "0",
    t2203_percentage: str = "0",
    non_resident: int = 0,
    itc_claim: str = "0",
    amount_i: str = "0",
    foreign_business_income: str = "0",
    foreign_non_business_income: str = "0",
    foreign_capital_gains_claim: str = "0",
    foreign_non_business_tax: str = "0",
    foreign_business_tax: str = "0",
    foreign_tax_countries: tuple[tuple[str, str], ...] = (),
    part_d_amount_15: str = "0",
    split_income_dividends: str = "0",
    split_income_dividends_other_than_eligible: str = "0",
) -> Worksheet:
    """Return BG's inputs (`returns/2025_return_bg.yaml`), with the Part 1 amounts given."""
    return compute(
        employment_income,
        share_dispositions,
        "0",
        "0",
        "0",
        "0",
        "0",
        qffp_foreclosure_dispositions=qffp_foreclosure_dispositions,
        amt_film_property_cca_and_carrying_charges=film_cca,
        amt_film_property_income_before_cca=film_income,
        amt_rental_property_cca_and_carrying_charges=rental_cca,
        amt_rental_property_income_before_cca=rental_income,
        amt_tax_shelter_losses=shelter_losses,
        amt_tax_shelter_deductible_amounts=shelter_deductible,
        amt_limited_partner_carrying_charges=limited_partner_carrying,
        amt_resource_expenditures=resource_expenditures,
        amt_resource_production_income=resource_production,
        amt_resource_foreign_property_income=resource_foreign,
        amt_class_43_1_income=class_43_1,
        amt_treaty_exempt_capital_gains=treaty_exempt,
        amt_graduated_rate_estate_capital_gains=graduated_rate_estate,
        amt_publicly_listed_gifts_total=gifts_total,
        amt_publicly_listed_gifts_t1170_line_68231=gifts_line_68231,
        amt_t4_security_options_boxes_39_and_91=security_t4_39_and_91,
        amt_t1212_line_2_deferred_security_options=security_t1212,
        amt_security_option_publicly_listed_gifts=security_gifts,
        amt_t4_security_options_boxes_41_and_92=security_t4_41_and_92,
        amt_prospector_or_grubstaker_deduction=prospector,
        amt_deferred_profit_sharing_plan_deduction=deferred_profit_sharing,
        amt_limited_partnership_difference_no_election=limited_partnership_no_election,
        amt_non_capital_losses_difference=non_capital_difference,
        amt_net_capital_losses_difference=net_capital_difference,
        amt_moving_expenses_deduction=moving_expenses,
        amt_non_deductible_interest=non_deductible_interest,
        amt_life_insurance_premiums_as_collateral=life_insurance_premiums,
        amt_investment_counsel_fees=investment_counsel_fees,
        amt_commission_employment_expenses=commission_employment,
        amt_minimum_tax_carryover_from_previous_years=carryover_from_previous_years,
        amt_minimum_tax_carryover_claim=carryover_claim,
        amt_t2203_column_5_percentage=t2203_percentage,
        amt_non_resident_or_deemed_resident=non_resident,
        amt_investment_tax_credit_claim=itc_claim,
        amt_t2038_amount_i=amount_i,
        amt_t2038_part_d_amount_15=part_d_amount_15,
        amt_foreign_business_income=foreign_business_income,
        amt_foreign_non_business_income=foreign_non_business_income,
        amt_foreign_capital_gains_non_taxable_claim=foreign_capital_gains_claim,
        amt_foreign_non_business_tax_paid=foreign_non_business_tax,
        amt_foreign_business_tax_paid=foreign_business_tax,
        foreign_tax_countries_rows=foreign_tax_countries,
        split_income_dividends=split_income_dividends,
        split_income_dividends_other_than_eligible=split_income_dividends_other_than_eligible,
    )


def test_return_bg_line_1_is_the_taxable_income_with_the_cpp_deduction_and_the_gain() -> None:
    # Return BG: 60000.00 less the CPP enhanced contribution of 565.00 (line 22215) is 59435.00;
    # the taxable capital gains of 1000.00 (half the 2000.00 gain) make 60435.00.
    worksheet = return_bg()

    assert worksheet.get(TAXABLE_INCOME).value == D("60435.00")


def test_return_bg_line_21_is_the_taxable_capital_gains_of_half_the_gain() -> None:
    # Return BG's share gain of 5000.00 less 3000.00 is 2000.00; at the 50% inclusion rate, 1000.00.
    worksheet = return_bg()

    assert worksheet.get(TAXABLE_CAPITAL_GAINS).value == D("1000.00")


def test_return_bg_line_4_is_the_film_cca_less_the_film_income() -> None:
    # Line 2 9000.00 minus line 3 4000.00 is 5000.00, not below zero.
    worksheet = return_bg()

    assert worksheet.get(AMT_FILM_PROPERTY_ADJUSTMENT).value == D("5000.00")


def test_return_bg_line_4_is_zero_when_the_film_income_is_more_than_the_cca() -> None:
    # Line 2 2000.00 minus line 3 4000.00 is -2000.00, which is entered as "0".
    worksheet = return_bg(film_cca="2000.00", film_income="4000.00")

    assert worksheet.get(AMT_FILM_PROPERTY_ADJUSTMENT).value == D("0")


def test_return_bg_line_7_is_zero_when_the_rental_income_is_more_than_the_cca() -> None:
    # Line 5 7000.00 minus line 6 9000.00 is -2000.00, which is entered as "0".
    worksheet = return_bg()

    assert worksheet.get(AMT_RENTAL_PROPERTY_ADJUSTMENT).value == D("0")


def test_return_bg_line_7_is_the_rental_cca_less_the_rental_income_when_it_is_positive() -> None:
    # Line 5 9000.00 minus line 6 7000.00 is 2000.00.
    worksheet = return_bg(rental_cca="9000.00", rental_income="7000.00")

    assert worksheet.get(AMT_RENTAL_PROPERTY_ADJUSTMENT).value == D("2000.00")


def test_return_bg_line_11_adds_lines_8_to_10() -> None:
    # Lines 8, 9 and 10 of 1000.00, 500.00 and 250.00 are 1750.00.
    worksheet = return_bg()

    assert worksheet.get(AMT_TAX_SHELTER_ADJUSTMENTS).value == D("1750.00")


def test_return_bg_line_12_adds_lines_1_4_7_and_11() -> None:
    # Line 1 60435.00 plus line 4 5000.00, line 7 0 and line 11 1750.00 is 67185.00.
    worksheet = return_bg()

    assert worksheet.get(AMT_PART_1_SUBTOTAL).value == D("67185.00")


def test_return_bg_line_12_with_no_film_rental_or_tax_shelter_amounts_is_line_1() -> None:
    # With every amount of lines 2, 3, 5, 6, 8, 9 and 10 at 0, line 12 is the taxable income.
    worksheet = return_bg(
        film_cca="0.00",
        film_income="0.00",
        rental_cca="0.00",
        rental_income="0.00",
        shelter_losses="0.00",
        shelter_deductible="0.00",
        limited_partner_carrying="0.00",
    )

    assert worksheet.get(AMT_PART_1_SUBTOTAL).value == D("60435.00")


def test_return_bg_part_9_line_5_adds_lines_2_to_4() -> None:
    # Part 9 line 2 2000.00, line 3 1000.00 and line 4 500.00 are 3500.00.
    worksheet = return_bg()

    assert worksheet.get(AMT_RESOURCE_INCOME_TOTAL).value == D("3500.00")


def test_return_bg_part_9_line_6_is_line_1_less_line_5() -> None:
    # Part 9 line 1 5000.00 less line 5 3500.00 is 1500.00, not below zero.
    worksheet = return_bg()

    assert worksheet.get(AMT_RESOURCE_PROPERTY_AND_FLOW_THROUGH_SHARES).value == D("1500.00")


def test_return_bg_part_9_line_6_is_zero_when_the_income_is_more_than_the_expenditures() -> None:
    # Part 9 line 1 2000.00 less line 5 3500.00 is -1500.00, which is entered as "0".
    worksheet = return_bg(resource_expenditures="2000.00")

    assert worksheet.get(AMT_RESOURCE_PROPERTY_AND_FLOW_THROUGH_SHARES).value == D("0")


def test_return_bg_line_16_adds_the_foreclosure_gains_and_losses() -> None:
    # A foreclosure of proceeds 1000.00 with an adjusted cost base of 1500.00 is a loss of
    # 500.00, so line 16 is -500.00 (a loss in brackets) and the other foreclosure amount is 0.
    worksheet = return_bg(qffp_foreclosure_dispositions=(("1000", "1500", "0"),))

    assert worksheet.get(AMT_MORTGAGE_FORECLOSURE_CAPITAL_GAINS).value == D("-500.00")


def test_return_bg_line_19_adds_lines_16_to_18() -> None:
    # Line 16 0 plus line 17 200.00 plus line 18 100.00 is 300.00.
    worksheet = return_bg()

    assert worksheet.get(AMT_CAPITAL_GAINS_ADJUSTMENTS).value == D("300.00")


def test_return_bg_line_15_is_the_capital_gain_of_the_share_disposition() -> None:
    # The share disposition's gain of 5000.00 less 3000.00 is line 19700 and line 15, 2000.00.
    worksheet = return_bg()

    assert worksheet.get(CAPITAL_GAIN).value == D("2000.00")


def test_return_bg_line_20_is_the_capital_gain_less_line_19() -> None:
    # Line 15 2000.00 minus line 19 300.00 is 1700.00.
    worksheet = return_bg()

    assert worksheet.get(AMT_NET_CAPITAL_GAINS_AFTER_ADJUSTMENTS).value == D("1700.00")


def test_return_bg_line_20_nets_the_foreclosure_loss_through_lines_15_and_19() -> None:
    # The capital gain of 2000.00 less the 500.00 foreclosure loss is 1500.00, and line 19 is
    # -500.00 + 300.00 = -200.00, so line 20 is 1500.00 minus -200.00, which is 1700.00.
    worksheet = return_bg(qffp_foreclosure_dispositions=(("1000", "1500", "0"),))

    assert worksheet.get(CAPITAL_GAIN).value == D("1500.00")
    assert worksheet.get(AMT_NET_CAPITAL_GAINS_AFTER_ADJUSTMENTS).value == D("1700.00")


def test_return_bg_line_20_shows_a_loss_in_brackets() -> None:
    # A share disposition of proceeds 1000.00 with an adjusted cost base of 3000.00 is a loss of
    # 2000.00, so line 15 is -2000.00 and line 20 is -2000.00 minus 300.00, which is -2300.00.
    worksheet = return_bg(share_dispositions=(("1000", "3000", "0"),))

    assert worksheet.get(AMT_NET_CAPITAL_GAINS_AFTER_ADJUSTMENTS).value == D("-2300.00")


def test_return_bg_line_22_is_line_20_less_line_21() -> None:
    # Line 20 1700.00 minus line 21 1000.00 (the taxable capital gains, line 12700) is 700.00.
    worksheet = return_bg()

    assert worksheet.get(AMT_CAPITAL_GAINS_DIFFERENCE).value == D("700.00")


def test_return_bg_line_23_is_line_22_when_line_20_is_positive() -> None:
    # Line 20 is 1700.00, positive, so line 23 is the amount from line 22, 700.00.
    worksheet = return_bg()

    assert worksheet.get(AMT_CAPITAL_GAINS_ADDED).value == D("700.00")


def test_return_bg_line_23_is_the_lesser_figure_in_brackets_when_line_20_is_negative() -> None:
    # Lines 17 and 18 of 200.00 and 3000.00 make line 19 3200.00, so line 20 is 2000.00 minus
    # 3200.00 = -1200.00; line 21 is 1000.00 and line 22 is -1200.00 minus 1000.00 = -2200.00
    # (2200.00 without brackets); the lesser of 1000.00 and 2200.00 is 1000.00, in brackets.
    worksheet = return_bg(graduated_rate_estate="3000.00")

    assert worksheet.get(AMT_NET_CAPITAL_GAINS_AFTER_ADJUSTMENTS).value == D("-1200.00")
    assert worksheet.get(AMT_CAPITAL_GAINS_DIFFERENCE).value == D("-2200.00")
    assert worksheet.get(AMT_CAPITAL_GAINS_ADDED).value == D("-1000.00")


def test_return_bg_line_23_is_zero_when_line_20_and_line_21_are_zero() -> None:
    # With no share disposition and lines 17 and 18 at 0, lines 15, 19, 20 and 21 are 0, and so
    # are lines 22 and 23.
    worksheet = return_bg(share_dispositions=(), treaty_exempt="0.00", graduated_rate_estate="0.00")

    assert worksheet.get(AMT_NET_CAPITAL_GAINS_AFTER_ADJUSTMENTS).value == D("0")
    assert worksheet.get(TAXABLE_CAPITAL_GAINS).value == D("0")
    assert worksheet.get(AMT_CAPITAL_GAINS_DIFFERENCE).value == D("0")
    assert worksheet.get(AMT_CAPITAL_GAINS_ADDED).value == D("0")


def test_return_bg_line_27_adds_lines_13_14_23_and_26() -> None:
    # Line 13 67185.00 (line 12) plus line 14 1500.00 plus line 23 700.00 plus line 26 600.00.
    worksheet = return_bg()

    assert worksheet.get(AMT_ADJUSTED_INCOME_WITH_GAINS).value == D("69985.00")


def test_return_bg_line_27_takes_line_23_in_brackets_when_line_20_is_negative() -> None:
    # 67185.00 plus 1500.00 plus -1000.00 plus 600.00 is 68285.00.
    worksheet = return_bg(graduated_rate_estate="3000.00")

    assert worksheet.get(AMT_ADJUSTED_INCOME_WITH_GAINS).value == D("68285.00")


def test_return_bg_line_27_with_no_capital_gain() -> None:
    # Taxable income is 59435.00 with no gain, so line 12 is 59435.00 + 5000.00 + 0.00 + 1750.00 =
    # 66185.00; plus line 14 1500.00, line 23 0 and line 26 600.00 is 68285.00.
    worksheet = return_bg(share_dispositions=(), treaty_exempt="0.00", graduated_rate_estate="0.00")

    assert worksheet.get(AMT_PART_1_SUBTOTAL).value == D("66185.00")
    assert worksheet.get(AMT_ADJUSTED_INCOME_WITH_GAINS).value == D("68285.00")


def test_return_bg_line_24_less_line_25_is_the_gifts_net() -> None:
    # Line 24 3000.00 minus line 25 1000.00 is 2000.00.
    worksheet = return_bg()

    assert worksheet.get(AMT_PUBLICLY_LISTED_GIFTS_NET).value == D("2000.00")


def test_return_bg_line_26_is_30_percent_of_line_24_less_line_25() -> None:
    # 30% of 2000.00 is 600.00.
    worksheet = return_bg()

    assert worksheet.get(AMT_PUBLICLY_LISTED_GIFTS_ADJUSTMENT).value == D("600.00")


def test_return_bg_line_26_is_negative_when_line_25_is_more_than_line_24() -> None:
    # Line 24 500.00 minus line 25 1000.00 is -500.00, and 30% of it is -150.00 (not floored).
    worksheet = return_bg(gifts_total="500.00", gifts_line_68231="1000.00")

    assert worksheet.get(AMT_PUBLICLY_LISTED_GIFTS_ADJUSTMENT).value == D("-150.00")


def test_return_bg_line_30_adds_lines_28_and_29() -> None:
    # The T4 slips' boxes 39 and 91 of 1000.00 plus the Form T1212 amount of 400.00 are 1400.00.
    worksheet = return_bg()

    assert worksheet.get(AMT_SECURITY_OPTIONS_D_TOTAL).value == D("1400.00")


def test_return_bg_line_31_is_40_percent_of_the_security_option_gifts() -> None:
    # 40% of the gifts of 500.00 under a security option plan is 200.00.
    worksheet = return_bg()

    assert worksheet.get(AMT_SECURITY_OPTION_GIFTS_DEDUCTION).value == D("200.00")


def test_return_bg_line_32_is_line_30_less_line_31() -> None:
    # Line 30 1400.00 minus line 31 200.00 is 1200.00, not below zero.
    worksheet = return_bg()

    assert worksheet.get(AMT_SECURITY_OPTIONS_NET).value == D("1200.00")


def test_return_bg_line_32_is_zero_when_the_gifts_are_more_than_line_30() -> None:
    # 40% of the gifts of 4000.00 is 1600.00; line 30 of 1400.00 less 1600.00 is -200.00: "0".
    worksheet = return_bg(security_gifts="4000.00")

    assert worksheet.get(AMT_SECURITY_OPTIONS_NET).value == D("0")


def test_return_bg_line_38_adds_lines_35_to_37() -> None:
    # Lines 35, 36 and 37 of 300.00, 100.00 and 50.00 are 450.00.
    worksheet = return_bg()

    assert worksheet.get(AMT_SECURITY_OPTIONS_D1_TOTAL).value == D("450.00")


def test_return_bg_line_43_adds_line_39_or_40_and_lines_41_and_42() -> None:
    # Line 39 600.00 (line 40 not applicable), plus line 41 100.00 and line 42 50.00, is 750.00.
    worksheet = return_bg()

    assert worksheet.get(AMT_OTHER_YEARS_LOSSES_TOTAL).value == D("750.00")


def test_return_bg_line_46_is_the_line_39_amount_as_applicable() -> None:
    # Line 39 is 600.00 and line 40 is not applicable, so line 46 is 600.00.
    worksheet = return_bg()

    assert worksheet.get(AMT_LIMITED_PARTNERSHIP_DIFFERENCE_APPLIED).value == D("600.00")


def test_return_bg_line_47_is_line_45_less_line_46_and_shows_a_loss_in_brackets() -> None:
    # Line 45, the limited partnership losses of other years, is 0 as none are claimed; 0 minus
    # line 46 of 600.00 is -600.00.
    worksheet = return_bg()

    assert worksheet.get(AMT_LIMITED_PARTNERSHIP_LOSSES_ADJUSTMENT).value == D("-600.00")


def test_return_bg_line_50_is_line_48_less_line_49_and_shows_a_loss_in_brackets() -> None:
    # Line 48 is 0 as none are claimed; 0 minus line 49 of 100.00 is -100.00.
    worksheet = return_bg()

    assert worksheet.get(AMT_NON_CAPITAL_LOSSES_ADJUSTMENT).value == D("-100.00")


def test_return_bg_line_53_adds_lines_47_50_51_and_52() -> None:
    # Lines 47 and 50 of -600.00 and -100.00, and lines 51 and 52 of 0, are -700.00.
    worksheet = return_bg()

    assert worksheet.get(AMT_LOSSES_AND_DEDUCTIONS_SUBTOTAL).value == D("-700.00")


def test_return_bg_line_63_adds_line_53_and_lines_55_to_62() -> None:
    # Line 53 of -700.00, the moving expenses of 200.00 (line 56) and the enhanced CPP
    # contributions of 565.00 (line 58) are 65.00; the other lines are 0.
    worksheet = return_bg()

    assert worksheet.get(AMT_DEDUCTIONS_TOTAL).value == D("65.00")


def test_return_bg_line_68_adds_lines_64_to_67() -> None:
    # Lines 64 to 67 of 300.00, 100.00, 0 and 50.00 are 450.00.
    worksheet = return_bg()

    assert worksheet.get(AMT_NON_DEDUCTIBLE_PROPERTY_EXPENSES).value == D("450.00")


def test_return_bg_line_76_adds_lines_70_to_75() -> None:
    # Line 70 of 150.00, and lines 71 to 75 not applicable, are 150.00.
    worksheet = return_bg()

    assert worksheet.get(AMT_NON_DEDUCTIBLE_OFFICE_EXPENSES).value == D("150.00")


def test_return_bg_line_77_is_line_69_less_line_76_and_shows_a_loss_in_brackets() -> None:
    # Line 69 is 0 as none is claimed; 0 minus line 76 of 150.00 is -150.00.
    worksheet = return_bg()

    assert worksheet.get(AMT_OFFICE_EXPENSES_ADJUSTMENT).value == D("-150.00")


def test_return_bg_line_78_adds_lines_63_68_and_77() -> None:
    # Lines 63, 68 and 77 of 65.00, 450.00 and -150.00 are 365.00.
    worksheet = return_bg()

    assert worksheet.get(AMT_ADJUSTMENTS_BEFORE_RATE_TOTAL).value == D("365.00")


def test_return_bg_line_80_is_50_percent_of_line_78() -> None:
    # 50% of line 78 of 365.00 is 182.50.
    worksheet = return_bg()

    assert worksheet.get(AMT_APPLICABLE_RATE_AMOUNT).value == D("182.50")


def test_return_bg_line_80_is_negative_when_line_78_is_negative() -> None:
    # Line 76 of 1000.00 makes line 77 -1000.00, so line 78 is 65.00 plus 450.00 less 1000.00,
    # -485.00, and 50% of it is -242.50 (not floored).
    worksheet = return_bg(commission_employment="1000.00")

    assert worksheet.get(AMT_APPLICABLE_RATE_AMOUNT).value == D("-242.50")


def test_return_bg_line_33_adds_line_27_and_line_32() -> None:
    # Line 27 of 69985.00 and line 32 of 1200.00 are 71185.00.
    worksheet = return_bg()

    assert worksheet.get(AMT_ADJUSTED_INCOME_WITH_SECURITY_OPTIONS).value == D("71185.00")


def test_return_bg_line_44_adds_lines_34_38_and_43() -> None:
    # Line 34, the amount from line 33 of 71185.00, line 38 of 450.00 and line 43 of 750.00 are
    # 72385.00.
    worksheet = return_bg()

    assert worksheet.get(AMT_SECURITY_OPTIONS_AND_LOSSES_TOTAL).value == D("72385.00")


def test_return_bg_line_82_adds_line_80_and_line_44() -> None:
    # Line 80 of 182.50 and line 81, the amount from line 44 of 72385.00, are 72567.50.
    worksheet = return_bg()

    assert worksheet.get(AMT_ADJUSTMENTS_AFTER_RATE_TOTAL).value == D("72567.50")


def test_return_bg_lines_84_to_92_are_zero_with_no_dividends_or_capital_gains_deduction() -> None:
    # Return BG claims no dividends, so lines 12000 and 12010 are 0 and lines 84 to 86 are 0; it
    # claims no capital gains deduction (lines 25400 and 25395), so lines 87 to 92 are 0 too.
    worksheet = return_bg()

    for kind in (
        AMT_DIVIDENDS_OTHER_THAN_ELIGIBLE_ADJUSTMENT,
        AMT_AMOUNT_A_MINUS_AMOUNT_B,
        AMT_DIVIDENDS_DIFFERENCE_ADJUSTMENT,
        AMT_DIVIDENDS_ADJUSTMENTS_TOTAL,
        AMT_LIFETIME_EXEMPTION_ADJUSTMENT,
        AMT_ADJUSTMENTS_WITH_LIFETIME_EXEMPTION_TOTAL,
        AMT_QBT_CAPITAL_GAINS_DEDUCTION_DOUBLED,
        AMT_QBT_CAPITAL_GAINS_DEDUCTION_DIFFERENCE,
        AMT_CAPITAL_GAINS_DEDUCTIONS_TOTAL,
    ):
        assert worksheet.get(kind).value == D("0"), kind.identifier


def test_return_bg_line_93_is_line_83_less_line_92() -> None:
    # Line 83, the amount from line 82 of 72567.50, less line 92 of 0, is 72567.50.
    worksheet = return_bg()

    assert worksheet.get(AMT_ADJUSTED_TAXABLE_INCOME).value == D("72567.50")


def test_return_bg_line_94_is_the_basic_exemption_of_177882() -> None:
    worksheet = return_bg()

    assert worksheet.get(AMT_BASIC_EXEMPTION).value == D("177882.00")


def test_return_bg_line_95_is_zero_when_line_93_is_under_the_basic_exemption() -> None:
    # Line 93 of 72567.50 less 177882.00 is below zero, so line 95 is 0 and the filer is not
    # subject to alternative minimum tax.
    worksheet = return_bg()

    assert worksheet.get(AMT_NET_ADJUSTED_TAXABLE_INCOME).value == D("0")


def test_return_bg_line_97_is_zero_when_line_95_is_zero() -> None:
    worksheet = return_bg()

    assert worksheet.get(AMT_GROSS_MINIMUM_AMOUNT).value == D("0")


def test_return_bg_line_98_is_50_percent_of_line_33800_rounded_half_up() -> None:
    # Line 33800 of 3100.21, the credit amounts at the credit rate, times 50% is 1550.105, a tie,
    # rounded half-up to 1550.11.
    worksheet = return_bg()

    assert worksheet.get(AMT_NON_REFUNDABLE_CREDITS_ADJUSTMENT).value == D("1550.11")


def test_return_bg_line_99_is_zero_with_no_donations_and_gifts() -> None:
    worksheet = return_bg()

    assert worksheet.get(AMT_DONATIONS_AND_GIFTS_ADJUSTMENT).value == D("0")


def test_return_bg_line_102_adds_lines_98_to_101() -> None:
    # Line 98 of 1550.11, line 99 of 0, and the caller's lines 100 and 101 not given (0), are
    # 1550.11.
    worksheet = return_bg()

    assert worksheet.get(AMT_CREDITS_ADJUSTMENTS_TOTAL).value == D("1550.11")


def test_return_bg_line_103_is_zero_when_line_97_is_less_than_line_102() -> None:
    # Line 97 of 0 less line 102 of 1550.11 is below zero, so the minimum amount is 0.
    worksheet = return_bg()

    assert worksheet.get(AMT_MINIMUM_AMOUNT).value == D("0")


def test_return_bg_with_200000_employment_income_line_1_is_the_taxable_income() -> None:
    # 200000.00 less the enhanced CPP contributions of 1074.00 (678.00 first additional, the
    # maximum, and 396.00 second additional, the maximum) is 198926.00; plus the 1000.00 taxable
    # capital gains is 199926.00.
    worksheet = return_bg(employment_income="200000")

    assert worksheet.get(TAXABLE_INCOME).value == D("199926.00")


def test_return_bg_with_200000_employment_income_line_63_adds_the_enhanced_cpp() -> None:
    # Line 53 of -700.00, the moving expenses of 200.00 and the enhanced CPP contributions of
    # 1074.00 are 574.00.
    worksheet = return_bg(employment_income="200000")

    assert worksheet.get(AMT_DEDUCTIONS_TOTAL).value == D("574.00")


def test_return_bg_with_200000_employment_income_line_80_is_50_percent_of_line_78() -> None:
    # Line 78 of 874.00 (574.00 plus 450.00 less 150.00) at 50% is 437.00.
    worksheet = return_bg(employment_income="200000")

    assert worksheet.get(AMT_APPLICABLE_RATE_AMOUNT).value == D("437.00")


def test_return_bg_with_200000_employment_income_line_82_adds_lines_80_and_81() -> None:
    # Line 80 of 437.00 and line 81, the amount from line 44 of 211876.00, are 212313.00.
    worksheet = return_bg(employment_income="200000")

    assert worksheet.get(AMT_ADJUSTMENTS_AFTER_RATE_TOTAL).value == D("212313.00")


def test_return_bg_with_200000_employment_income_line_95_is_over_the_basic_exemption() -> None:
    # Line 93 of 212313.00 less the basic exemption of 177882.00 is 34431.00.
    worksheet = return_bg(employment_income="200000")

    assert worksheet.get(AMT_NET_ADJUSTED_TAXABLE_INCOME).value == D("34431.00")


def test_return_bg_with_200000_employment_income_line_97_is_20_5_percent_of_line_95() -> None:
    # 20.5% of 34431.00 is 7058.355, a tie, rounded half-up to 7058.36.
    worksheet = return_bg(employment_income="200000")

    assert worksheet.get(AMT_GROSS_MINIMUM_AMOUNT).value == D("7058.36")


def test_return_bg_with_200000_employment_income_line_103_is_line_97_less_line_102() -> None:
    # Line 97 of 7058.36 less line 102 of 1563.77 (line 98, 50% of line 33800 of 3127.54, and lines
    # 99 to 101 of 0) is 5494.59.
    worksheet = return_bg(employment_income="200000")

    assert worksheet.get(AMT_CREDITS_ADJUSTMENTS_TOTAL).value == D("1563.77")
    assert worksheet.get(AMT_MINIMUM_AMOUNT).value == D("5494.59")


def test_return_bg_part_2_line_4_adds_the_credits_of_lines_35000_and_40425() -> None:
    # Line 2, the total non-refundable tax credits of line 35000, is 3100.21 (21380.75 at the credit
    # rate, rounded half-up); line 3, the dividend tax credit of line 40425, is 0.00. Line 4 is
    # 3100.21 plus 0.00, 3100.21.
    worksheet = return_bg()

    assert worksheet.get(AMT_CREDITS_TOTAL).value == D("3100.21")


def test_return_bg_part_2_line_5_is_the_federal_tax_less_line_4() -> None:
    # Line 1, the federal tax of line 40400, is 8946.68 on taxable income of 60435.00; line 4 is
    # 3100.21, so line 5 is 8946.68 minus 3100.21, 5846.47.
    worksheet = return_bg()

    assert worksheet.get(AMT_TAX_PAYABLE_BEFORE_MINIMUM_TAX_CARRYOVER).value == D("5846.47")


def test_return_bg_part_2_line_7_is_the_basic_federal_tax() -> None:
    # Line 5 of 5846.47 less line 6, the minimum tax carryover applied of 0.00, is 5846.47.
    worksheet = return_bg()

    assert worksheet.get(AMT_BASIC_FEDERAL_TAX).value == D("5846.47")


def test_return_bg_part_8_lines_4_and_8_add_their_lines() -> None:
    # Line 4 is line 2, the tax payable of 5846.47, plus line 3, the recapture of 0.00: 5846.47.
    # Line 8 adds lines 5 to 7, the split income tax, the logging tax credit and line 41600, all 0:
    # 0.00.
    worksheet = return_bg()

    assert worksheet.get(AMT_TAX_PAYABLE_WITH_ITC_RECAPTURE).value == D("5846.47")
    assert worksheet.get(AMT_SPLIT_INCOME_AND_CREDITS_TOTAL).value == D("0")


def test_return_bg_part_8_line_9_is_line_4_less_line_8_and_line_11_is_line_9_less_line_10() -> None:
    # Line 9 is 5846.47 minus 0.00, 5846.47. Line 10 is the minimum amount of line 103 of Part 1,
    # 0.00, so line 11 is 5846.47 minus 0.00, 5846.47, not below zero.
    worksheet = return_bg()

    assert worksheet.get(AMT_TAX_PAYABLE_AFTER_CREDITS).value == D("5846.47")
    assert worksheet.get(AMT_MAXIMUM_CARRYOVER_APPLIED).value == D("5846.47")


def test_return_bg_part_8_line_12_claims_nothing_when_no_carryover_is_entered() -> None:
    # The cap is the lesser of line 1, 0.00, and line 11, 5846.47: 0.00. The claim is 0.00, so
    # nothing is applied on line 40427 and basic federal tax is unchanged.
    worksheet = return_bg()

    assert worksheet.get(AMT_MAXIMUM_CARRYOVER_CLAIM).value == D("0")
    assert worksheet.get(AMT_MINIMUM_TAX_CARRYOVER_APPLIED).value == D("0")
    assert worksheet.get(CREDITS_AGAINST_BASIC_FEDERAL_TAX).value == D("3100.21")
    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("5846.47")


def test_return_bg_with_200000_part_2_line_5_is_the_federal_tax_less_line_4() -> None:
    # Line 1, the federal tax of line 40400 on taxable income of 199926.00, is 42888.33; line 4 is
    # 3127.54 (21569.25 at the credit rate), so line 5 is 42888.33 minus 3127.54, 39760.79.
    worksheet = return_bg(employment_income="200000")

    assert worksheet.get(AMT_TAX_PAYABLE_BEFORE_MINIMUM_TAX_CARRYOVER).value == D("39760.79")


def test_return_bg_with_200000_part_8_line_11_is_line_9_less_the_minimum() -> None:
    # Line 9, line 4 of 39760.79 less line 8 of 0.00, is 39760.79; line 10, the minimum amount of
    # 5494.59, leaves line 11 at 39760.79 minus 5494.59, 34266.20.
    worksheet = return_bg(employment_income="200000")

    assert worksheet.get(AMT_MAXIMUM_CARRYOVER_APPLIED).value == D("34266.20")


def test_return_bg_with_a_carryover_and_a_claim_within_the_cap_applies_the_claim() -> None:
    # Line 1 is the carryover from 2018 to 2024 of 1000.00; line 11 is 34266.20. The cap is the
    # lesser of them, 1000.00, and the claim of 400.00 is within it, so 400.00 is applied on line 12
    # (line 40427).
    worksheet = return_bg(
        employment_income="200000",
        carryover_from_previous_years="1000",
        carryover_claim="400",
    )

    assert worksheet.get(AMT_MAXIMUM_CARRYOVER_CLAIM).value == D("1000")
    assert worksheet.get(AMT_MINIMUM_TAX_CARRYOVER_APPLIED).value == D("400")


def test_return_bg_with_a_carryover_claim_lowers_basic_federal_tax_and_the_t1_line_126() -> None:
    # Part 2 line 7 is line 5 of 39760.79 less line 6 of 400.00: 39360.79. T1 line 124 is 400.00, so
    # line 125 is 3127.54 plus 0.00 plus 400.00, 3527.54, and line 126 is 42888.33 minus 3527.54,
    # 39360.79.
    worksheet = return_bg(
        employment_income="200000",
        carryover_from_previous_years="1000",
        carryover_claim="400",
    )

    assert worksheet.get(AMT_BASIC_FEDERAL_TAX).value == D("39360.79")
    assert worksheet.get(CREDITS_AGAINST_BASIC_FEDERAL_TAX).value == D("3527.54")
    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("39360.79")


def test_return_bg_with_a_claim_at_the_cap_is_applied_in_full() -> None:
    # The claim of 34266.20 is the line 11 cap when line 1 is larger, so it is applied in full.
    worksheet = return_bg(
        employment_income="200000",
        carryover_from_previous_years="50000",
        carryover_claim="34266.20",
    )

    assert worksheet.get(AMT_MINIMUM_TAX_CARRYOVER_APPLIED).value == D("34266.20")


def test_a_carryover_claim_above_line_1_is_refused_naming_both_kinds() -> None:
    # Line 12 "not more than line 1 or 11, whichever is less": the cap is the carryover of 1000.00,
    # and 1000.01 is above it, an input error, not capped.
    with pytest.raises(InputAboveBoundError) as raised:
        return_bg(
            employment_income="200000",
            carryover_from_previous_years="1000",
            carryover_claim="1000.01",
        )

    assert str(raised.value).startswith(
        "ca/amt_minimum_tax_carryover_claim 1000.01 is above ca/amt_maximum_carryover_claim 1000"
    )


def test_a_carryover_claim_above_line_11_is_refused_when_line_11_is_the_lesser() -> None:
    # Line 1 of 50000.00 is more than line 11 of 34266.20, so the cap is line 11: 34266.21 is
    # above it.
    with pytest.raises(InputAboveBoundError) as raised:
        return_bg(
            employment_income="200000",
            carryover_from_previous_years="50000",
            carryover_claim="34266.21",
        )

    assert str(raised.value).startswith(
        "ca/amt_minimum_tax_carryover_claim 34266.21 is above "
        "ca/amt_maximum_carryover_claim 34266.2"
    )


def test_a_claim_is_refused_when_no_carryover_is_available() -> None:
    # With no carryover from earlier years, line 1 is 0.00 and so is the cap: a claim of 0.01 is
    # above it.
    with pytest.raises(InputAboveBoundError) as raised:
        return_bg(carryover_claim="0.01")

    assert str(raised.value).startswith(
        "ca/amt_minimum_tax_carryover_claim 0.01 is above ca/amt_maximum_carryover_claim 0"
    )


def test_return_bg_line_2_is_48_percent_of_the_basic_federal_tax() -> None:
    # Line 2 is 48% of the basic federal tax of 5846.47 (Part 2 line 7): 5846.47 x 0.48 is
    # 2806.3056, rounded to 2806.31.
    worksheet = return_bg()

    assert worksheet.get(AMT_FEDERAL_SURTAX_AT_48_PERCENT).value == D("2806.31")


def test_return_bg_line_3_and_line_4_are_zero_by_default() -> None:
    # No T2203 percentage (line 3 is 0.00), so line 3 has no amount; the filer is not
    # non-resident, so line 4 is the surtax if non-resident, 0.00.
    worksheet = return_bg()

    assert worksheet.get(AMT_FEDERAL_SURTAX_MULTIPLE_JURISDICTIONS).value == D("0.00")
    assert worksheet.get(AMT_LINE_3_HAS_AMOUNT).value == D("0")
    assert worksheet.get(AMT_FEDERAL_SURTAX).value == D("0.00")


def test_return_bg_line_4_is_line_2_for_a_non_resident_with_no_line_3_amount() -> None:
    # No line 3 amount, so line 4 is the surtax if non-resident: line 2 of 2806.31 for a
    # non-resident. Line 15 is line 1 of 5846.47 plus 2806.31, which is 8652.78.
    worksheet = return_bg(non_resident=1)

    assert worksheet.get(AMT_FEDERAL_SURTAX).value == D("2806.31")
    assert worksheet.get(AMT_REGULAR_NET_FEDERAL_TAX_PAYABLE).value == D("8652.78")


def test_return_bg_line_3_is_half_of_line_2_when_the_t2203_percentage_is_50() -> None:
    # Line 2 of 2806.31 at 50% is 1403.155, a tie, rounded half-up to 1403.16. Line 3 has an
    # amount, so line 4 is line 3, 1403.16. Line 15 is 5846.47 plus 1403.16, 7249.63.
    worksheet = return_bg(t2203_percentage="50")

    assert worksheet.get(AMT_FEDERAL_SURTAX_MULTIPLE_JURISDICTIONS).value == D("1403.16")
    assert worksheet.get(AMT_LINE_3_HAS_AMOUNT).value == D("1")
    assert worksheet.get(AMT_FEDERAL_SURTAX).value == D("1403.16")
    assert worksheet.get(AMT_REGULAR_NET_FEDERAL_TAX_PAYABLE).value == D("7249.63")


def test_return_bg_line_4_takes_line_3_over_the_non_resident_surtax() -> None:
    # A non-resident who also has a line 3 amount: line 3 has an amount, so line 4 is line 3,
    # 1403.16, not line 2 of 2806.31. Line 15 is 5846.47 plus 1403.16, 7249.63.
    worksheet = return_bg(t2203_percentage="50", non_resident=1)

    assert worksheet.get(AMT_FEDERAL_SURTAX).value == D("1403.16")
    assert worksheet.get(AMT_REGULAR_NET_FEDERAL_TAX_PAYABLE).value == D("7249.63")


def test_return_bg_line_6_is_the_basic_federal_tax_with_no_surtax() -> None:
    # Line 6 is the basic federal tax (Part 2 line 7) of 5846.47 plus line 4 of 0.00 and the
    # recapture of 0.00: 5846.47.
    worksheet = return_bg()

    assert worksheet.get(AMT_FEDERAL_TAX_WITH_SURTAX_AND_RECAPTURE).value == D("5846.47")


def test_return_bg_line_15_is_line_6_with_no_regular_tax_credits() -> None:
    # Line 15 is line 1 of 5846.47 less line 14, the regular tax credits total of 0.00: 5846.47.
    worksheet = return_bg()

    assert worksheet.get(AMT_REGULAR_NET_FEDERAL_TAX_PAYABLE).value == D("5846.47")


def test_return_bg_line_12_is_the_investment_tax_credit_claim_when_it_is_within_line_i() -> None:
    # The investment tax credit claim of 100.00 is within the T2038 amount I of 150.00, so line 12
    # is 100.00. Line 14 is line 12 of 100.00 plus line 13 of 0.00, 100.00. Line 15 is line 6 of
    # 5846.47 less 100.00, 5746.47.
    worksheet = return_bg(itc_claim="100", amount_i="150")

    assert worksheet.get(AMT_INVESTMENT_TAX_CREDIT).value == D("100")
    assert worksheet.get(AMT_REGULAR_TAX_CREDITS_TOTAL).value == D("100")
    assert worksheet.get(AMT_REGULAR_NET_FEDERAL_TAX_PAYABLE).value == D("5746.47")


def test_an_investment_tax_credit_claim_above_t2038_amount_i_is_refused() -> None:
    # The claim of 200.00 is above the T2038 amount I of 150.00, an input error, not capped.
    with pytest.raises(InputAboveBoundError) as raised:
        return_bg(itc_claim="200", amount_i="150")

    assert str(raised.value).startswith(
        "ca/amt_investment_tax_credit_claim 200 is above ca/amt_t2038_amount_i 150"
    )


def test_return_bg_part_4_is_zero_by_default() -> None:
    # No foreign income, tax or claim, and no T2209 credit: lines 3, 4, 6, 7, 9, 10 and 11 are 0.
    worksheet = return_bg()

    assert worksheet.get(AMT_FOREIGN_CAPITAL_GAINS_NON_TAXABLE).value == D("0")
    assert worksheet.get(AMT_TOTAL_FOREIGN_INCOME).value == D("0")
    assert worksheet.get(AMT_FOREIGN_INCOME_LIMIT).value == D("0")
    assert worksheet.get(AMT_FOREIGN_NON_BUSINESS_TAX_TWO_THIRDS).value == D("0")
    assert worksheet.get(AMT_FOREIGN_TAXES_PAID).value == D("0")
    assert worksheet.get(AMT_FOREIGN_TAX_CREDIT_LESSER).value == D("0")
    assert worksheet.get(AMT_SPECIAL_FOREIGN_TAX_CREDIT).value == D("0")


def test_return_bg_part_4_worked_case_is_line_by_line() -> None:
    # Line 1 1500.00 and line 2 500.00; line 3 is a claim of 300.00, at most line 23 of Part 1
    # (700.00). Line 4 is 1500.00 + 500.00 + 300.00 = 2300.00, and line 6 is 2300.00 times 20.5%,
    # 471.50. Line 7 is 600.00 times 66.6666%, 399.9996, rounded to 400.00; line 8 is 100.00, so
    # line 9 is 500.00. Line 10 is the lesser of 471.50 and 500.00, 471.50. Line 11 is the greater
    # of the federal foreign tax credit, 0.00, and 471.50: 471.50.
    worksheet = return_bg(
        foreign_business_income="1500",
        foreign_non_business_income="500",
        foreign_capital_gains_claim="300",
        foreign_non_business_tax="600",
        foreign_business_tax="100",
    )

    assert worksheet.get(AMT_FOREIGN_CAPITAL_GAINS_NON_TAXABLE).value == D("300.00")
    assert worksheet.get(AMT_TOTAL_FOREIGN_INCOME).value == D("2300.00")
    assert worksheet.get(AMT_FOREIGN_INCOME_LIMIT).value == D("471.50")
    assert worksheet.get(AMT_FOREIGN_NON_BUSINESS_TAX_TWO_THIRDS).value == D("400.00")
    assert worksheet.get(AMT_FOREIGN_TAXES_PAID).value == D("500.00")
    assert worksheet.get(AMT_FOREIGN_TAX_CREDIT_LESSER).value == D("471.50")
    assert worksheet.get(AMT_SPECIAL_FOREIGN_TAX_CREDIT).value == D("471.50")


def test_return_bg_line_3_accepts_a_claim_equal_to_line_23() -> None:
    # A claim of 700.00 is equal to line 23 of Part 1 (700.00), so it is not above it: line 3 is
    # 700.00, line 4 is 700.00 and line 6 is 700.00 times 20.5%, 143.50.
    worksheet = return_bg(foreign_capital_gains_claim="700")

    assert worksheet.get(AMT_FOREIGN_CAPITAL_GAINS_NON_TAXABLE).value == D("700")
    assert worksheet.get(AMT_TOTAL_FOREIGN_INCOME).value == D("700")
    assert worksheet.get(AMT_FOREIGN_INCOME_LIMIT).value == D("143.50")


def test_return_bg_line_3_refuses_a_claim_above_line_23_and_does_not_cap_it() -> None:
    # A claim of 800.00 is above line 23 of Part 1 (700.00): an input error, not capped to 700.00.
    with pytest.raises(InputAboveBoundError) as raised:
        return_bg(foreign_capital_gains_claim="800")

    assert str(raised.value).startswith(
        "ca/amt_foreign_capital_gains_non_taxable_claim 800 is above "
        "ca/amt_capital_gains_added_not_below_zero 700.00"
    )


def test_return_bg_line_3_refuses_a_claim_when_line_23_is_negative() -> None:
    # With graduated rate estate amounts of 3000.00, line 23 of Part 1 is -1000.00 (see the test
    # above it). The most line 3 may claim is line 23 taken as 0, so a claim of 100.00 is above it
    # and is refused, not capped.
    with pytest.raises(InputAboveBoundError) as raised:
        return_bg(graduated_rate_estate="3000.00", foreign_capital_gains_claim="100")

    assert str(raised.value).startswith(
        "ca/amt_foreign_capital_gains_non_taxable_claim 100 is above "
        "ca/amt_capital_gains_added_not_below_zero 0"
    )


def test_return_bg_line_3_accepts_a_zero_claim_when_line_23_is_negative() -> None:
    # Line 23 of Part 1 is -1000.00, so the bound of line 3 is 0: a claim of 0.00 is not above it,
    # and line 3 is 0.00, so line 4 and line 6 are 0.00 as well.
    worksheet = return_bg(graduated_rate_estate="3000.00", foreign_capital_gains_claim="0")

    assert worksheet.get(AMT_FOREIGN_CAPITAL_GAINS_NON_TAXABLE).value == D("0")
    assert worksheet.get(AMT_TOTAL_FOREIGN_INCOME).value == D("0")
    assert worksheet.get(AMT_FOREIGN_INCOME_LIMIT).value == D("0")


def test_return_bg_line_4_takes_a_negative_business_income_into_account() -> None:
    # Foreign business income of -300.00 (a loss, net of expenses) and 500.00 of non-business
    # income: line 4 is 200.00, and line 6 is 200.00 times 20.5%, 41.00.
    worksheet = return_bg(foreign_business_income="-300", foreign_non_business_income="500")

    assert worksheet.get(AMT_TOTAL_FOREIGN_INCOME).value == D("200.00")
    assert worksheet.get(AMT_FOREIGN_INCOME_LIMIT).value == D("41.00")


def test_return_bg_line_4_is_zero_when_the_total_of_the_foreign_income_is_below_zero() -> None:
    # Line 1 of -2500.00 and line 2 of 500.00 add to -2000.00, which is not above zero: line 4 is
    # 0, and line 6 is 0 times 20.5%, 0.00.
    worksheet = return_bg(foreign_business_income="-2500", foreign_non_business_income="500")

    assert worksheet.get(AMT_TOTAL_FOREIGN_INCOME).value == D("0")
    assert worksheet.get(AMT_FOREIGN_INCOME_LIMIT).value == D("0")


def test_return_bg_line_10_is_line_9_when_the_taxes_paid_are_lower() -> None:
    # Non-business tax of 30.00 is line 7, 30.00 times 66.6666%, 19.99998, rounded to 20.00; with no
    # business tax, line 8 is 0.00, so line 9 is 20.00. Line 6 is 471.50 (for 2300.00 of line 4),
    # so line 10 is the lesser, 20.00, and line 11 is the greater of 0.00 and 20.00: 20.00.
    worksheet = return_bg(
        foreign_business_income="1500",
        foreign_non_business_income="500",
        foreign_capital_gains_claim="300",
        foreign_non_business_tax="30",
    )

    assert worksheet.get(AMT_FOREIGN_NON_BUSINESS_TAX_TWO_THIRDS).value == D("20.00")
    assert worksheet.get(AMT_FOREIGN_TAXES_PAID).value == D("20.00")
    assert worksheet.get(AMT_FOREIGN_TAX_CREDIT_LESSER).value == D("20.00")
    assert worksheet.get(AMT_SPECIAL_FOREIGN_TAX_CREDIT).value == D("20.00")


def test_return_bg_line_11_is_the_t2209_credit_when_it_is_more_than_line_10() -> None:
    # One country paying 500.00 tax on 1000.00 of foreign non-business income: the Form T2209 line 2
    # is 1000.00 times the basic federal tax of 5846.47 over the net income of 60435.00, 96.74, and
    # line 3 is the lesser of 500.00 and 96.74, 96.74: the federal foreign tax credit. Line 10 is
    # the lesser of line 6 (471.50) and line 9 (20.00), 20.00, so line 11 is 96.74, the greater.
    worksheet = return_bg(
        foreign_business_income="1500",
        foreign_non_business_income="500",
        foreign_capital_gains_claim="300",
        foreign_non_business_tax="30",
        foreign_tax_countries=(("500", "1000"),),
    )

    assert worksheet.get(FEDERAL_FOREIGN_TAX_CREDIT).value == D("96.74")
    assert worksheet.get(AMT_FOREIGN_TAX_CREDIT_LESSER).value == D("20.00")
    assert worksheet.get(AMT_SPECIAL_FOREIGN_TAX_CREDIT).value == D("96.74")


def test_return_bg_part_5_is_zero_by_default() -> None:
    # Line 1 is 0.00 (line 103 of Part 1) and line 2 is 0.00, so line 3 is 0.00. Line 4 is the
    # regular net federal tax payable of 5846.47 and line 5 is the surtax of 0.00, so line 6 is
    # 5846.47. Line 7 is 0.00 less 5846.47, below zero, so 0.00. Lines 8 to 11 are 0.00: the filer
    # is not subject to alternative minimum tax.
    worksheet = return_bg()

    assert worksheet.get(AMT_NET_MINIMUM_TAX_PAYABLE).value == D("0")
    assert worksheet.get(AMT_REGULAR_NET_TAX_LESS_SURTAX).value == D("5846.47")
    assert worksheet.get(AMT_MINIMUM_TAX_AFTER_REGULAR_TAX).value == D("0")
    assert worksheet.get(AMT_INVESTMENT_TAX_CREDIT_LESS_PART_D).value == D("0")
    assert worksheet.get(AMT_ALTERNATIVE_MINIMUM_TAX_PAYABLE).value == D("0")


def test_return_bg_part_5_line_3_is_line_1_less_the_special_foreign_tax_credit() -> None:
    # The security options of boxes 39 and 91 at 150000.00 (in place of 1000.00) add 149000.00 to
    # line 93 of Part 1, to 221567.50, so line 95 is 43685.50 and line 97 is 20.5% of it, 8955.5275,
    # rounded to 8955.53; less line 102 of 1550.11, line 103 (line 1 of Part 5) is 7405.42. The
    # foreign figures of the Part 4 case above give line 2, the special foreign tax credit, of
    # 471.50, so line 3 is 7405.42 less 471.50, 6933.92. Line 6 is 5846.47 and line 7 is 6933.92
    # less 5846.47, 1087.45, which is then line 11 as no investment tax credit is claimed.
    worksheet = return_bg(
        security_t4_39_and_91="150000",
        foreign_business_income="1500",
        foreign_non_business_income="500",
        foreign_capital_gains_claim="300",
        foreign_non_business_tax="600",
        foreign_business_tax="100",
    )

    assert worksheet.get(AMT_MINIMUM_AMOUNT).value == D("7405.42")
    assert worksheet.get(AMT_SPECIAL_FOREIGN_TAX_CREDIT).value == D("471.50")
    assert worksheet.get(AMT_NET_MINIMUM_TAX_PAYABLE).value == D("6933.92")
    assert worksheet.get(AMT_MINIMUM_TAX_AFTER_REGULAR_TAX).value == D("1087.45")
    assert worksheet.get(AMT_ALTERNATIVE_MINIMUM_TAX_PAYABLE).value == D("1087.45")


def test_return_bg_part_5_line_7_is_line_3_less_line_6_when_it_is_positive() -> None:
    # With the security options at 150000.00, line 1 of Part 5 is 7405.42 and line 3 is the same,
    # with no foreign tax credit. Line 6 is the regular net federal tax payable of 5846.47 less a
    # surtax of 0.00, 5846.47, so line 7 is 7405.42 less 5846.47, 1558.95, and line 11 is the same.
    worksheet = return_bg(security_t4_39_and_91="150000")

    assert worksheet.get(AMT_NET_MINIMUM_TAX_PAYABLE).value == D("7405.42")
    assert worksheet.get(AMT_REGULAR_NET_TAX_LESS_SURTAX).value == D("5846.47")
    assert worksheet.get(AMT_MINIMUM_TAX_AFTER_REGULAR_TAX).value == D("1558.95")
    assert worksheet.get(AMT_ALTERNATIVE_MINIMUM_TAX_PAYABLE).value == D("1558.95")


def test_return_bg_part_5_line_7_is_zero_when_the_regular_net_tax_is_more() -> None:
    # With employment income of 200000.00, line 1 of Part 5 is the minimum amount of 5494.59 and
    # line 6 is the regular net federal tax payable of 39760.79 (line 5, the surtax, is 0.00). Line
    # 7 is 5494.59 less 39760.79, below zero, so 0.00, and line 11 is 0.00.
    worksheet = return_bg(employment_income="200000")

    assert worksheet.get(AMT_NET_MINIMUM_TAX_PAYABLE).value == D("5494.59")
    assert worksheet.get(AMT_REGULAR_NET_TAX_LESS_SURTAX).value == D("39760.79")
    assert worksheet.get(AMT_MINIMUM_TAX_AFTER_REGULAR_TAX).value == D("0")
    assert worksheet.get(AMT_ALTERNATIVE_MINIMUM_TAX_PAYABLE).value == D("0")


def test_return_bg_part_5_line_6_adds_back_a_negative_surtax() -> None:
    # A non-resident with employment income of 8000.00: taxable income is 8955.00 (8000.00, plus the
    # taxable capital gain of 1000.00, less the enhanced CPP contributions of 45.00, 1% of 4500.00).
    # The federal tax at 14.5% is 1298.48, rounded half-up from 1298.475. The credit amounts are
    # 17953.95 (the basic personal amount of 16129.00, the CPP base contributions of 222.75, the EI
    # premiums of 131.20 and the Canada employment amount of 1471.00), at 14.5% 2603.32, so the
    # basic federal tax is 1298.48 less 2603.32, -1304.84. Line 5, the surtax, is 48% of that,
    # -626.32, a negative amount. Line 4 is floored at 0.00 because the federal tax with the
    # surtax is negative, so line 6 is 0.00 less -626.32, 626.32, and line 7 is 0.00 with no
    # minimum amount.
    worksheet = return_bg(employment_income="8000", non_resident=1)

    assert worksheet.get(AMT_FEDERAL_SURTAX).value == D("-626.32")
    assert worksheet.get(AMT_REGULAR_NET_TAX_LESS_SURTAX).value == D("626.32")
    assert worksheet.get(AMT_MINIMUM_TAX_AFTER_REGULAR_TAX).value == D("0")


def test_return_bg_part_5_line_10_is_line_8_less_amount_15_of_part_d() -> None:
    # With the security options at 150000.00 and an investment tax credit claim of 100.00 (within
    # amount I of 150.00), the claim is line 12 of Part 3 and reduces line 15 to 5746.47, so line 6
    # is 5746.47 and line 7 is 7405.42 less 5746.47, 1658.95. Line 8 is the claim, 100.00, and line
    # 9, amount 15 of Part D of Form T2038(IND), is 60.00: line 10 is 40.00 and line 11 is 1658.95
    # less 40.00, 1618.95.
    worksheet = return_bg(
        security_t4_39_and_91="150000",
        itc_claim="100",
        amount_i="150",
        part_d_amount_15="60",
    )

    assert worksheet.get(AMT_REGULAR_NET_FEDERAL_TAX_PAYABLE).value == D("5746.47")
    assert worksheet.get(AMT_MINIMUM_TAX_AFTER_REGULAR_TAX).value == D("1658.95")
    assert worksheet.get(AMT_INVESTMENT_TAX_CREDIT_LESS_PART_D).value == D("40.00")
    assert worksheet.get(AMT_ALTERNATIVE_MINIMUM_TAX_PAYABLE).value == D("1618.95")


def test_return_bg_part_5_line_10_is_zero_when_amount_15_of_part_d_is_more_than_the_claim() -> None:
    # The same return with amount 15 of Part D at 150.00, above the claim of 100.00: line 10 is
    # 0.00, and line 11 is line 7, 1658.95.
    worksheet = return_bg(
        security_t4_39_and_91="150000",
        itc_claim="100",
        amount_i="150",
        part_d_amount_15="150",
    )

    assert worksheet.get(AMT_INVESTMENT_TAX_CREDIT_LESS_PART_D).value == D("0")
    assert worksheet.get(AMT_ALTERNATIVE_MINIMUM_TAX_PAYABLE).value == D("1658.95")


def test_return_bg_part_6_line_9_is_the_surtax_on_line_7_and_line_14_is_zero_by_default() -> None:
    # Line 1 is the basic federal tax of 5846.47 and line 2 is 0.00 (no split income), so line 3 is
    # 5846.47. Line 4 is 0.00, so line 5 is 5846.47, and line 7 is 5846.47 plus 0.00. Line 8 is
    # 0.00. Line 9 is 48% of line 7: 5846.47 times 0.48 is 2806.3056, rounded half-up to 2806.31.
    # Line 10 is 0.00 (a chosen percentage of 0, as no tax is payable to multiple jurisdictions).
    # Line 11 is 0.00: no amount is on line 10, and the filer is not a non-resident. Line 12 is 0.00
    # and line 13 is 0.00, so line 14 is 0.00.
    worksheet = return_bg()

    assert worksheet.get(AMT_BASIC_FEDERAL_TAX_LESS_SPLIT_INCOME_TAX).value == D("5846.47")
    assert worksheet.get(AMT_GREATER_OF_BASIC_TAX_AND_MINIMUM_AMOUNT).value == D("5846.47")
    assert worksheet.get(AMT_FEDERAL_TAX_UNDER_MINIMUM_TAX).value == D("5846.47")
    assert worksheet.get(AMT_PART_6_SURTAX_AT_48_PERCENT).value == D("2806.31")
    assert worksheet.get(AMT_PART_6_SURTAX_MULTIPLE_JURISDICTIONS).value == D("0")
    assert worksheet.get(AMT_PART_6_HAS_AMOUNT_ON_LINE_10).value == 0
    assert worksheet.get(AMT_PART_6_FEDERAL_SURTAX).value == D("0")
    assert worksheet.get(AMT_PART_6_TAX_WITH_SURTAX).value == D("0")
    assert worksheet.get(AMT_FEDERAL_TAX_PAYABLE_UNDER_MINIMUM_TAX).value == D("0")


def test_return_bg_part_6_line_5_is_the_minimum_amount_when_it_is_more_than_line_3() -> None:
    # With the security options of boxes 39 and 91 at 150000.00 and no foreign figures, line 3 is
    # 5846.47 less 0.00, and line 4, the minimum amount, is 7405.42, so line 5 is 7405.42 and line 7
    # is 7405.42 plus 0.00. Line 9 is 48% of 7405.42, 3554.6016, rounded to 3554.60. Line 8 is
    # 7405.42 (no special foreign tax credit), so line 12 is 7405.42 with no amount on line 11, and
    # line 14 is 7405.42.
    worksheet = return_bg(security_t4_39_and_91="150000")

    assert worksheet.get(AMT_BASIC_FEDERAL_TAX_LESS_SPLIT_INCOME_TAX).value == D("5846.47")
    assert worksheet.get(AMT_GREATER_OF_BASIC_TAX_AND_MINIMUM_AMOUNT).value == D("7405.42")
    assert worksheet.get(AMT_FEDERAL_TAX_UNDER_MINIMUM_TAX).value == D("7405.42")
    assert worksheet.get(AMT_PART_6_SURTAX_AT_48_PERCENT).value == D("3554.60")
    assert worksheet.get(AMT_NET_MINIMUM_TAX_PAYABLE).value == D("7405.42")
    assert worksheet.get(AMT_PART_6_TAX_WITH_SURTAX).value == D("7405.42")
    assert worksheet.get(AMT_FEDERAL_TAX_PAYABLE_UNDER_MINIMUM_TAX).value == D("7405.42")


def test_return_bg_part_6_line_12_is_line_8_when_line_11_is_zero() -> None:
    # The security options of 150000.00 with the foreign figures of the Part 5 case above: line 5 is
    # the minimum amount of 7405.42 and line 7 is the same. Line 8 is the net minimum tax payable of
    # 6933.92 (7405.42 less the special foreign tax credit of 471.50), line 9 is 3554.60, and line
    # 10 and line 11 are 0.00, so line 12 is 6933.92 and line 14 is 6933.92.
    worksheet = return_bg(
        security_t4_39_and_91="150000",
        foreign_business_income="1500",
        foreign_non_business_income="500",
        foreign_capital_gains_claim="300",
        foreign_non_business_tax="600",
        foreign_business_tax="100",
    )

    assert worksheet.get(AMT_FEDERAL_TAX_UNDER_MINIMUM_TAX).value == D("7405.42")
    assert worksheet.get(AMT_NET_MINIMUM_TAX_PAYABLE).value == D("6933.92")
    assert worksheet.get(AMT_PART_6_SURTAX_MULTIPLE_JURISDICTIONS).value == D("0")
    assert worksheet.get(AMT_PART_6_FEDERAL_SURTAX).value == D("0")
    assert worksheet.get(AMT_PART_6_TAX_WITH_SURTAX).value == D("6933.92")
    assert worksheet.get(AMT_FEDERAL_TAX_PAYABLE_UNDER_MINIMUM_TAX).value == D("6933.92")


def test_return_bg_part_6_line_11_is_line_9_for_a_non_resident_with_no_amount_on_line_10() -> None:
    # With the security options at 150000.00 and a non-resident (a count of 1), line 10 is 0.00, so
    # the condition on line 10 does not apply, and line 11 is line 9, 3554.60, times the count. Line
    # 12 is 7405.42 plus 3554.60, 10960.02, and line 14 is the same. Line 9 is the surtax on line 7
    # of Part 6, 3554.60, not the surtax on line 2 of Part 3 (2806.31) that Part 3 takes for a
    # non-resident.
    worksheet = return_bg(security_t4_39_and_91="150000", non_resident=1)

    assert worksheet.get(AMT_PART_6_SURTAX_AT_48_PERCENT).value == D("3554.60")
    assert worksheet.get(AMT_PART_6_HAS_AMOUNT_ON_LINE_10).value == 0
    assert worksheet.get(AMT_PART_6_SURTAX_IF_NON_RESIDENT).value == D("3554.60")
    assert worksheet.get(AMT_PART_6_FEDERAL_SURTAX).value == D("3554.60")
    assert worksheet.get(AMT_PART_6_TAX_WITH_SURTAX).value == D("10960.02")
    assert worksheet.get(AMT_FEDERAL_TAX_PAYABLE_UNDER_MINIMUM_TAX).value == D("10960.02")


def test_return_bg_part_6_line_11_is_line_10_when_line_10_has_an_amount() -> None:
    # With the security options at 150000.00 and 50 as the percentage of Column 5 of line 52220 on
    # Form T2203 (a figure the caller gives), line 10 is 3554.60 times 50%, 1777.30, which is an
    # amount, so line 11 is line 10, 1777.30. Line 12 is 7405.42 plus 1777.30, 9182.72, and line 14
    # is the same.
    worksheet = return_bg(security_t4_39_and_91="150000", t2203_percentage="50")

    assert worksheet.get(AMT_PART_6_SURTAX_MULTIPLE_JURISDICTIONS).value == D("1777.30")
    assert worksheet.get(AMT_PART_6_HAS_AMOUNT_ON_LINE_10).value == 1
    assert worksheet.get(AMT_PART_6_FEDERAL_SURTAX).value == D("1777.30")
    assert worksheet.get(AMT_PART_6_TAX_WITH_SURTAX).value == D("9182.72")
    assert worksheet.get(AMT_FEDERAL_TAX_PAYABLE_UNDER_MINIMUM_TAX).value == D("9182.72")


def test_return_bg_part_6_line_14_is_line_13_when_the_split_income_tax_is_more_than_line_12() -> (
    None
):
    # Split dividends of 11500.00, as on Return AL: Form T1206 line 22 is 2756.54 (3795.00 less
    # 1038.46) and line 24 is the same. Line 3 is the basic federal tax of line 1 less 2756.54, and
    # line 5 is line 3, as the minimum amount is 0.00, and line 7 is line 5 plus line 6, the basic
    # federal tax again. Line 8 is 0.00 and line 11
    # is 0.00 (a resident, with no tax to multiple jurisdictions), so line 12 is 0.00 and line 14
    # is line 13, 2756.54.
    worksheet = return_bg(
        split_income_dividends="11500",
        split_income_dividends_other_than_eligible="11500",
    )
    basic = worksheet.get(AMT_BASIC_FEDERAL_TAX).value

    assert worksheet.get(SPLIT_INCOME_LINE_22).value == D("2756.54")
    assert worksheet.get(AMT_BASIC_FEDERAL_TAX_LESS_SPLIT_INCOME_TAX).value == basic - D("2756.54")
    assert worksheet.get(AMT_FEDERAL_TAX_UNDER_MINIMUM_TAX).value == basic
    assert worksheet.get(SPLIT_INCOME_LINE_24).value == D("2756.54")
    assert worksheet.get(AMT_PART_6_TAX_WITH_SURTAX).value == D("0")
    assert worksheet.get(AMT_FEDERAL_TAX_PAYABLE_UNDER_MINIMUM_TAX).value == D("2756.54")


def test_return_bg_part_6_line_3_is_floored_for_a_non_resident_with_negative_basic_tax() -> None:
    # A non-resident with employment income of 8000.00, whose basic federal tax is -1304.84 (as the
    # Part 5 case above): line 3 is -1304.84 less 0.00, not below zero, so 0.00, and line 5 is 0.00.
    # Line 7 is 0.00 plus 0.00, so line 9 is 0.00 and line 11, the non-resident's amount, is 0.00
    # too. Part 3 line 2 is -626.32 for this return, but Part 6 does not take that: line 5, the
    # greater of line 3 and the minimum amount, is 0.00.
    worksheet = return_bg(employment_income="8000", non_resident=1)

    assert worksheet.get(AMT_BASIC_FEDERAL_TAX_LESS_SPLIT_INCOME_TAX).value == D("0")
    assert worksheet.get(AMT_FEDERAL_TAX_UNDER_MINIMUM_TAX).value == D("0")
    assert worksheet.get(AMT_PART_6_SURTAX_AT_48_PERCENT).value == D("0")
    assert worksheet.get(AMT_PART_6_FEDERAL_SURTAX).value == D("0")
    assert worksheet.get(AMT_FEDERAL_TAX_PAYABLE_UNDER_MINIMUM_TAX).value == D("0")


def test_return_bg_line_41700_is_the_line_139_figure_when_part_5_line_11_is_zero() -> None:
    # Part 5 line 11 is 0.00 (the Part 5 case above), so the condition "line 11 is positive" counts
    # 0 and T1 line 41700 is the line 139 figure: line 132 (the federal tax with the ITC recapture,
    # 5846.47) less line 138 (0.00), 5846.47. Part 6 line 14, 0.00, is not entered on the return.
    # Line 29 of Form T1206 Part 2 is then 5846.47 plus 0.00, and the net federal tax is the same.
    worksheet = return_bg()

    assert worksheet.get(AMT_PART_5_LINE_11_IS_POSITIVE).value == 0
    assert worksheet.get(FEDERAL_TAX_LESS_CREDITS).value == D("5846.47")
    assert worksheet.get(FEDERAL_TAX_LINE_41700).value == D("5846.47")
    assert worksheet.get(SPLIT_INCOME_LINE_29).value == D("5846.47")
    assert worksheet.get(NET_FEDERAL_TAX).value == D("5846.47")


def test_return_bg_line_41700_is_part_6_line_14_when_part_5_line_11_is_positive() -> None:
    # The security options of boxes 39 and 91 at 150000.00 and a non-resident (a count of 1): Part 5
    # line 11 is 1558.95 (line 7, 7405.42 less 5846.47 of line 6, with line 10 at 0.00), which is
    # positive, so the condition "line 11 is positive" counts 1 and T1 line 41700 takes Part 6 line
    # 14 of 10960.02 (the Part 6 case above) in place of the line 139 figure of 5846.47. Line 29 of
    # Form T1206 Part 2 is 10960.02 plus 0.00, and line 30 is the greater of line 24 (0.00) and line
    # 29, 10960.02, so the net federal tax is 10960.02 plus the special taxes of 0.00. The balance
    # owing rises by the change in the net federal tax, 10960.02 less 5846.47, 5113.55: from 8973.29
    # to 14086.84, as nothing else in the total payable or the credits changes.
    worksheet = return_bg(security_t4_39_and_91="150000", non_resident=1)

    assert worksheet.get(AMT_ALTERNATIVE_MINIMUM_TAX_PAYABLE).value == D("1558.95")
    assert worksheet.get(AMT_PART_5_LINE_11_IS_POSITIVE).value == 1
    assert worksheet.get(AMT_FEDERAL_TAX_PAYABLE_UNDER_MINIMUM_TAX).value == D("10960.02")
    assert worksheet.get(FEDERAL_TAX_LESS_CREDITS).value == D("5846.47")
    assert worksheet.get(FEDERAL_TAX_LINE_41700).value == D("10960.02")
    assert worksheet.get(SPLIT_INCOME_LINE_29).value == D("10960.02")
    assert worksheet.get(SPLIT_INCOME_LINE_30).value == D("10960.02")
    assert worksheet.get(NET_FEDERAL_TAX).value == D("10960.02")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("14086.84")


def test_return_bg_line_41700_keeps_line_139_when_regular_tax_is_more_than_minimum() -> None:
    # Employment income of 200000.00: the minimum amount on line 103 of Part 1 is 5494.59, but the
    # regular net federal tax less the surtax, line 6 of Part 5, is 39760.79, more than the minimum,
    # so line 7 and line 11 are 0.00 and the condition "line 11 is positive" counts 0. Part 6 line
    # 14 is still computed, 5494.59 (line 12 is the net minimum tax of 5494.59, with no amount on
    # line 11), but it is not entered on line 41700: the line 139 figure, 39760.79, is.
    worksheet = return_bg(employment_income="200000")

    assert worksheet.get(AMT_MINIMUM_AMOUNT).value == D("5494.59")
    assert worksheet.get(AMT_ALTERNATIVE_MINIMUM_TAX_PAYABLE).value == D("0")
    assert worksheet.get(AMT_PART_5_LINE_11_IS_POSITIVE).value == 0
    assert worksheet.get(AMT_FEDERAL_TAX_PAYABLE_UNDER_MINIMUM_TAX).value == D("5494.59")
    assert worksheet.get(FEDERAL_TAX_LINE_41700).value == D("39760.79")
    assert worksheet.get(NET_FEDERAL_TAX).value == D("39760.79")
