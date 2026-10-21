"""CA-ON 2025 end to end: return bg."""

from __future__ import annotations

from app.domain.worksheet import Worksheet
from app.jurisdictions.ca.catalog import (
    AMT_CAPITAL_GAINS_ADJUSTMENTS,
    AMT_FILM_PROPERTY_ADJUSTMENT,
    AMT_MORTGAGE_FORECLOSURE_CAPITAL_GAINS,
    AMT_NET_CAPITAL_GAINS_AFTER_ADJUSTMENTS,
    AMT_PART_1_SUBTOTAL,
    AMT_PUBLICLY_LISTED_GIFTS_ADJUSTMENT,
    AMT_PUBLICLY_LISTED_GIFTS_NET,
    AMT_RENTAL_PROPERTY_ADJUSTMENT,
    AMT_RESOURCE_INCOME_TOTAL,
    AMT_RESOURCE_PROPERTY_AND_FLOW_THROUGH_SHARES,
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
