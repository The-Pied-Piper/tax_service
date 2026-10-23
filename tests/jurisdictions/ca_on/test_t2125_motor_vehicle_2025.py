"""The 2025 datasets of Form T2125 Charts A to C (motor vehicle expenses, line 9281), checked
against CRA's form, and the charts worked for one leased passenger vehicle.

Form T2125 (Statement of Business or Professional Activities, 2025 edition, confirmed 2026-10-19
from the PDF; no .txt is published, https://www.canada.ca/content/dam/cra-arc/formspubs/pbg/t2125/
t2125-25e.pdf):

- Chart A line 16 "Allowable motor vehicle expenses: Add amounts 13 to 15 (enter this total on line
  9281 of Part 4)", line 13 "Business use part: amount 1 ÷ amount 2 × amount 12 = 13" and line 12
  "Total motor vehicle expenses: Add amounts 3 to 11.";
- Chart B line 18 "($350*** ÷ 30) × the number of days in the fiscal period for which interest was
  payable (accrual method) or paid (cash method)", and line 19 "Available interest expense: Amount
  17 or 18, whichever is less (include this in amount 4 of Chart A above)";
- Chart C line 23 "Amount 23 or ($44,706 + GST and PST, or $44,706 + HST), whichever is
  more", line 24 "× 85%", line 25 "[($1,100 + GST and PST, or $1,100 + HST) × amount 22] ÷ 30",
  line 27 "[($38,000 + GST and PST, or $38,000 + HST) × amount 20] ÷ amount 24" and line 28
  "Eligible leasing cost: Amount 26 or 27, whichever is less (enter in amount 8 of Chart A
  above)"; the sales tax rate is "Use a GST rate of 5% or HST rate applicable to your province."

The printed constants are the 2025 figures in the chart body; the endnotes give the figures of
leases entered into in earlier years, which are not modelled. Every product and quotient is a
dollars-and-cents box and rounds half-up to the cent, the owner's decision, as the form states no
rounding rule. Amount 26 is a subtraction the form prints without a floor, so it is signed.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Any

import pytest

import app.registrations
from app.adapters.outbound.yaml_parameters import YamlParameterSource
from app.domain.errors import CapabilityContractError
from app.domain.parameters.credit import CREDIT, Credit
from app.domain.parameters.rate import RATE, Rate
from app.domain.parameters.rounding import RoundingMode, RoundTo
from app.domain.parameters.rounding_only import ROUNDING_ONLY, RoundingOnly
from app.domain.worksheet import Worksheet
from app.jurisdictions.ca.catalog import (
    BUSINESS_MOTOR_VEHICLE_EXPENSES,
    BUSINESS_TOTAL_EXPENSES,
    BUSINESS_VEHICLE_AVAILABLE_INTEREST,
    BUSINESS_VEHICLE_BUSINESS_USE_PART,
    BUSINESS_VEHICLE_DAYS_DIVISOR,
    BUSINESS_VEHICLE_INTEREST_FOR_PERIOD,
    BUSINESS_VEHICLE_INTEREST_LIMIT,
    BUSINESS_VEHICLE_LEASE_CHARGE_LIMIT,
    BUSINESS_VEHICLE_LEASE_CHARGE_PORTION,
    BUSINESS_VEHICLE_LEASE_CHARGES_NET,
    BUSINESS_VEHICLE_LEASE_COST_LIMIT,
    BUSINESS_VEHICLE_LEASE_COST_PORTION,
    BUSINESS_VEHICLE_LEASE_PRICE_85_PERCENT,
    BUSINESS_VEHICLE_LEASE_PRICE_BASE,
    BUSINESS_VEHICLE_LEASING_COST,
    BUSINESS_VEHICLE_LIST_PRICE_LIMIT,
    BUSINESS_VEHICLE_TOTAL_EXPENSES,
)
from tests.jurisdictions.ca_on.end_to_end.support import D, run

SOURCE = YamlParameterSource(app.registrations.JURISDICTIONS.roots())
CENT = RoundTo(D("0.01"), RoundingMode.HALF_UP)
T2125_PDF = "https://www.canada.ca/content/dam/cra-arc/formspubs/pbg/t2125/t2125-25e.pdf"

# The printed constants, each a dataset of the same name (the charts' "$350***", "÷ 30",
# "$44,706", "$1,100" and "$38,000").
CONSTANTS = {
    "ca/business_vehicle_interest_limit": D("350"),
    "ca/business_vehicle_days_divisor": D("30"),
    "ca/business_vehicle_list_price_limit": D("44706"),
    "ca/business_vehicle_lease_charge_limit": D("1100"),
    "ca/business_vehicle_lease_cost_limit": D("38000"),
}
ROUNDING_FAMILIES = (
    "ca/business_vehicle_business_use_rounding",
    "ca/business_vehicle_interest_rounding",
    "ca/business_vehicle_sales_tax_rounding",
    "ca/business_vehicle_lease_charge_rounding",
    "ca/business_vehicle_lease_cost_rounding",
)


@pytest.mark.parametrize(("family", "amount"), CONSTANTS.items())
def test_2025_each_chart_constant_is_the_printed_figure(family: str, amount: Decimal) -> None:
    data = SOURCE.get(family, 2025, CREDIT)

    assert data.values == Credit(amount=amount)
    assert data.rounding == CENT


@pytest.mark.parametrize("family", (*CONSTANTS, "ca/business_vehicle_lease_price_rate"))
def test_2025_each_chart_figure_cites_the_form(family: str) -> None:
    if family.endswith("_rate"):
        assert T2125_PDF in SOURCE.get(family, 2025, RATE).sources
    else:
        assert T2125_PDF in SOURCE.get(family, 2025, CREDIT).sources


def test_2025_the_leasing_price_rate_is_85_percent() -> None:
    # Chart C line 24: "Amount 23 or ($44,706 + GST and PST, or $44,706 + HST), whichever is more ×
    # 85%".
    data = SOURCE.get("ca/business_vehicle_lease_price_rate", 2025, RATE)

    assert data.values == Rate(D("0.85"))
    assert data.rounding == CENT


@pytest.mark.parametrize("family", ROUNDING_FAMILIES)
def test_2025_each_chart_rounding_is_half_up_to_the_cent_with_no_values(family: str) -> None:
    data = SOURCE.get(family, 2025, ROUNDING_ONLY)

    assert data.values == RoundingOnly()
    assert data.rounding == CENT


# A leased passenger vehicle used half for business, the figures of Return BB (see
# returns/2025_return_bb.yaml): Chart B interest 400 on 183 days, Chart C lease charges 2550 over
# 183 days at a list price of 60000 and a 13% HST rate, and the other Chart A lines.
LEASED: dict[str, str] = {
    "vehicle_business_kilometres": "5000",
    "vehicle_total_kilometres": "10000",
    "vehicle_fuel_and_oil": "1000",
    "vehicle_insurance": "600",
    "vehicle_maintenance_and_repairs": "200",
    "vehicle_other_expenses_10": "653",
    "vehicle_interest_payable": "400",
    "vehicle_interest_days": "183",
    "vehicle_lease_charges": "2550",
    "vehicle_lease_days": "183",
    "vehicle_list_price": "60000",
    "vehicle_sales_tax_rate": "13",
}


def statement(vehicle: dict[str, str]) -> Worksheet:
    """A T2125 of gross sales of 50000 and office expenses of 20000, with the Chart A to C amounts
    in `vehicle` (the others 0)."""
    amounts = {"gross_sales": "50000", "office_expenses": "20000", **vehicle}
    result = run("0", (), "0", "0", "0", "0", "0", business_statements=({"business": amounts},))
    return result["ca/t2125"][0]


def line(worksheet: Worksheet, kind: Any) -> Any:
    return worksheet.get(kind).value


def test_a_leased_vehicle_gives_line_9281_of_2500_and_the_expenses_of_22500() -> None:
    # Chart A: line 12 is 1000 (3) + 400 (4, line 19) + 600 (5) + 200 (7) + 2147 (8, line 28)
    # + 653 (10) = 5000; line 13 is 5000 x 5000 / 10000 = 2500; line 16 is 2500 + 0 + 0 = 2500,
    # line 9281. Line 9368 is 20000 + 2500 = 22500 and line 9369 is 50000 - 22500 = 27500.
    worksheet = statement(LEASED)

    assert line(worksheet, BUSINESS_VEHICLE_TOTAL_EXPENSES) == D("5000")
    assert line(worksheet, BUSINESS_VEHICLE_BUSINESS_USE_PART) == D("2500")
    assert line(worksheet, BUSINESS_MOTOR_VEHICLE_EXPENSES) == D("2500")
    assert line(worksheet, BUSINESS_TOTAL_EXPENSES) == D("22500")


def test_chart_b_interest_is_the_amount_payable_when_that_is_the_lesser() -> None:
    # Chart B line 18: 350 ÷ 30 × 183 days = 64050 ÷ 30 = 2135.00; line 17 is 400, the lesser,
    # so line 19, the available interest expense, is 400.
    worksheet = statement(LEASED)

    assert line(worksheet, BUSINESS_VEHICLE_INTEREST_FOR_PERIOD) == D("2135.00")
    assert line(worksheet, BUSINESS_VEHICLE_AVAILABLE_INTEREST) == D("400.00")


def test_chart_b_interest_is_capped_at_the_350_over_30_a_day_amount() -> None:
    # Line 17 is 3000, more than line 18 of 2135.00 (350 ÷ 30 × 183), so line 19 is 2135.00.
    worksheet = statement({**LEASED, "vehicle_interest_payable": "3000"})

    assert line(worksheet, BUSINESS_VEHICLE_AVAILABLE_INTEREST) == D("2135.00")


def test_chart_c_takes_the_price_plus_tax_when_it_is_more_than_the_list_price() -> None:
    # Line 23 is 40000; 44706 plus 13% (5811.78) is 50517.78, the greater, and 85% of it is
    # 42940.113, which rounds to 42940.11 (line 24).
    worksheet = statement({**LEASED, "vehicle_list_price": "40000"})

    assert line(worksheet, BUSINESS_VEHICLE_LEASE_PRICE_BASE) == D("50517.78")
    assert line(worksheet, BUSINESS_VEHICLE_LEASE_PRICE_85_PERCENT) == D("42940.11")


def test_chart_c_takes_the_list_price_when_it_is_more_than_the_price_plus_tax() -> None:
    # Line 23 is 60000, more than 50517.78, so line 24 is 60000 x 85% = 51000.00.
    worksheet = statement(LEASED)

    assert line(worksheet, BUSINESS_VEHICLE_LEASE_PRICE_BASE) == D("60000")
    assert line(worksheet, BUSINESS_VEHICLE_LEASE_PRICE_85_PERCENT) == D("51000.00")


def test_chart_c_line_25_is_the_1100_plus_tax_times_the_days_over_30() -> None:
    # (1100 + 13% of 1100 = 1243.00) x 183 days = 227469.00 ÷ 30 = 7582.30.
    worksheet = statement(LEASED)

    assert line(worksheet, BUSINESS_VEHICLE_LEASE_CHARGE_LIMIT) == D("1100.00")
    assert line(worksheet, BUSINESS_VEHICLE_LEASE_CHARGE_PORTION) == D("7582.30")


def test_chart_c_line_27_is_the_38000_plus_tax_times_the_charges_over_line_24() -> None:
    # (38000 + 13% = 42940.00) x 2550 lease charges = 109497000 ÷ 51000.00 = 2147.00.
    worksheet = statement(LEASED)

    assert line(worksheet, BUSINESS_VEHICLE_LEASE_COST_LIMIT) == D("38000.00")
    assert line(worksheet, BUSINESS_VEHICLE_LEASE_COST_PORTION) == D("2147.00")


def test_chart_c_leasing_cost_is_the_lesser_of_line_26_and_line_27() -> None:
    # Line 26 is 7582.30 - 0 = 7582.30 and line 27 is 2147.00, so line 28, the leasing cost, is
    # 2147.00.
    worksheet = statement(LEASED)

    assert line(worksheet, BUSINESS_VEHICLE_LEASE_CHARGES_NET) == D("7582.30")
    assert line(worksheet, BUSINESS_VEHICLE_LEASING_COST) == D("2147.00")


def test_chart_c_leasing_cost_is_line_26_when_the_payments_before_make_it_the_lesser() -> None:
    # Line 25 is 7582.30 and line 21 is 7000, so line 26 is 582.30, less than line 27 (2147.00):
    # line 28 is 582.30, line 12 is 1000 + 400 + 600 + 200 + 582.30 + 653 = 3435.30 and line 13 is
    # 3435.30 x 5000 / 10000 = 1717.65, line 9281.
    worksheet = statement({**LEASED, "vehicle_lease_payments_before": "7000"})

    assert line(worksheet, BUSINESS_VEHICLE_LEASE_CHARGES_NET) == D("582.30")
    assert line(worksheet, BUSINESS_VEHICLE_LEASING_COST) == D("582.30")
    assert line(worksheet, BUSINESS_VEHICLE_TOTAL_EXPENSES) == D("3435.30")
    assert line(worksheet, BUSINESS_MOTOR_VEHICLE_EXPENSES) == D("1717.65")


def test_chart_c_line_28_below_zero_is_refused() -> None:
    # Line 25 is 7582.30 and line 21 (payments before the year) is 9000, so line 26 is
    # 7582.30 - 9000 = -1417.70. The form prints no floor, but the eligible leasing cost (line 28)
    # is a non-negative amount, so the computation refuses it rather than inventing a floor.
    with pytest.raises(CapabilityContractError):
        statement({**LEASED, "vehicle_lease_payments_before": "9000"})


def test_chart_a_business_use_part_is_rounded_half_up_to_the_cent() -> None:
    # Amount 1 of 1 and amount 2 of 3: 100 x 1 ÷ 3 = 33.333..., which rounds to 33.33 (line 13),
    # and line 16 is 33.33 + 0 + 0.
    worksheet = statement(
        {
            "vehicle_business_kilometres": "1",
            "vehicle_total_kilometres": "3",
            "vehicle_fuel_and_oil": "100",
        }
    )

    assert line(worksheet, BUSINESS_VEHICLE_BUSINESS_USE_PART) == D("33.33")
    assert line(worksheet, BUSINESS_MOTOR_VEHICLE_EXPENSES) == D("33.33")


def test_chart_a_business_use_part_is_0_when_there_are_no_total_kilometres() -> None:
    # A total of 0 kilometres gives a business use part of 0 (no division), so line 16 is only
    # the parking fees of 300.
    worksheet = statement(
        {
            "vehicle_business_kilometres": "5000",
            "vehicle_total_kilometres": "0",
            "vehicle_parking_fees": "300",
        }
    )

    assert line(worksheet, BUSINESS_VEHICLE_BUSINESS_USE_PART) == D("0")
    assert line(worksheet, BUSINESS_MOTOR_VEHICLE_EXPENSES) == D("300")


def test_the_chart_constant_for_the_days_divides_by_30_in_both_charts() -> None:
    worksheet = statement(LEASED)

    assert line(worksheet, BUSINESS_VEHICLE_DAYS_DIVISOR) == D("30.00")
    assert line(worksheet, BUSINESS_VEHICLE_INTEREST_LIMIT) == D("350.00")
    assert line(worksheet, BUSINESS_VEHICLE_LIST_PRICE_LIMIT) == D("44706.00")
