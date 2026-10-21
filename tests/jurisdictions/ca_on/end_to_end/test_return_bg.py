"""CA-ON 2025 end to end: return bg."""

from __future__ import annotations

from app.domain.worksheet import Worksheet
from app.jurisdictions.ca.catalog import (
    AMT_FILM_PROPERTY_ADJUSTMENT,
    AMT_PART_1_SUBTOTAL,
    AMT_RENTAL_PROPERTY_ADJUSTMENT,
    AMT_TAX_SHELTER_ADJUSTMENTS,
    TAXABLE_INCOME,
)
from tests.jurisdictions.ca_on.end_to_end.support import D, compute


def return_bg(
    film_cca: str = "9000.00",
    film_income: str = "4000.00",
    rental_cca: str = "7000.00",
    rental_income: str = "9000.00",
    shelter_losses: str = "1000.00",
    shelter_deductible: str = "500.00",
    limited_partner_carrying: str = "250.00",
) -> Worksheet:
    """Return BG's inputs (`returns/2025_return_bg.yaml`), with the Part 1 amounts given."""
    return compute(
        "60000",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
        amt_film_property_cca_and_carrying_charges=film_cca,
        amt_film_property_income_before_cca=film_income,
        amt_rental_property_cca_and_carrying_charges=rental_cca,
        amt_rental_property_income_before_cca=rental_income,
        amt_tax_shelter_losses=shelter_losses,
        amt_tax_shelter_deductible_amounts=shelter_deductible,
        amt_limited_partner_carrying_charges=limited_partner_carrying,
    )


def test_return_bg_line_1_is_the_taxable_income_after_the_cpp_enhanced_deduction() -> None:
    # Return BG: 60000.00 less the CPP enhanced contribution of 565.00 (line 22215) is 59435.00.
    worksheet = return_bg()

    assert worksheet.get(TAXABLE_INCOME).value == D("59435.00")


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
    # Line 1 59435.00 plus line 4 5000.00, line 7 0 and line 11 1750.00 is 66185.00.
    worksheet = return_bg()

    assert worksheet.get(AMT_PART_1_SUBTOTAL).value == D("66185.00")


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

    assert worksheet.get(AMT_PART_1_SUBTOTAL).value == D("59435.00")
