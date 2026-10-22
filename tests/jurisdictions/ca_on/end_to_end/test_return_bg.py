"""CA-ON 2025 end to end: return bg."""

from __future__ import annotations

from app.domain.worksheet import Worksheet
from app.jurisdictions.ca.catalog import (
    AMT_ADJUSTED_INCOME_WITH_GAINS,
    AMT_ADJUSTMENTS_BEFORE_RATE_TOTAL,
    AMT_APPLICABLE_RATE_AMOUNT,
    AMT_CAPITAL_GAINS_ADDED,
    AMT_CAPITAL_GAINS_ADJUSTMENTS,
    AMT_CAPITAL_GAINS_DIFFERENCE,
    AMT_DEDUCTIONS_TOTAL,
    AMT_FILM_PROPERTY_ADJUSTMENT,
    AMT_LIMITED_PARTNERSHIP_DIFFERENCE_APPLIED,
    AMT_LIMITED_PARTNERSHIP_LOSSES_ADJUSTMENT,
    AMT_LOSSES_AND_DEDUCTIONS_SUBTOTAL,
    AMT_MORTGAGE_FORECLOSURE_CAPITAL_GAINS,
    AMT_NET_CAPITAL_GAINS_AFTER_ADJUSTMENTS,
    AMT_NON_CAPITAL_LOSSES_ADJUSTMENT,
    AMT_NON_DEDUCTIBLE_OFFICE_EXPENSES,
    AMT_NON_DEDUCTIBLE_PROPERTY_EXPENSES,
    AMT_OFFICE_EXPENSES_ADJUSTMENT,
    AMT_OTHER_YEARS_LOSSES_TOTAL,
    AMT_PART_1_SUBTOTAL,
    AMT_PUBLICLY_LISTED_GIFTS_ADJUSTMENT,
    AMT_PUBLICLY_LISTED_GIFTS_NET,
    AMT_RENTAL_PROPERTY_ADJUSTMENT,
    AMT_RESOURCE_INCOME_TOTAL,
    AMT_RESOURCE_PROPERTY_AND_FLOW_THROUGH_SHARES,
    AMT_SECURITY_OPTION_GIFTS_DEDUCTION,
    AMT_SECURITY_OPTIONS_D1_TOTAL,
    AMT_SECURITY_OPTIONS_D_TOTAL,
    AMT_SECURITY_OPTIONS_NET,
    AMT_TAX_SHELTER_ADJUSTMENTS,
    CAPITAL_GAIN,
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
) -> Worksheet:
    """Return BG's inputs (`returns/2025_return_bg.yaml`), with the Part 1 amounts given."""
    return compute(
        "60000",
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
