"""CA-ON 2025 end to end: return bd."""

from __future__ import annotations

from app.adapters.inbound.trace_english import EnglishTraceRenderer
from app.domain.worksheet import Worksheet
from app.jurisdictions.ca.catalog import (
    FEDERAL_BASIC_TAX,
    FISH_CCA_CLAIM,
    FISH_CCA_CLAIM_LESS_PERSONAL_PART,
    FISH_EXPENSES_SUBTOTAL,
    FISH_GROSS_INCOME,
    FISH_GROSS_INCOME_BEFORE_EXPENSES,
    FISH_HOME_ALLOWABLE_CLAIM,
    FISH_HOME_CARRY_FORWARD,
    FISH_HOME_EXPENSES,
    FISH_HOME_EXPENSES_AVAILABLE,
    FISH_HOME_INCOME_LIMIT,
    FISH_MOTOR_VEHICLE_EXPENSES,
    FISH_NET_INCOME_AFTER_ADJUSTMENTS,
    FISH_NET_INCOME_BEFORE_ADJUSTMENTS,
    FISH_OTHER_EXPENSES_WITH_TERMINAL_LOSS,
    FISH_PARTNER_OTHER_AMOUNTS,
    FISH_PARTNERSHIP_TOTAL,
    FISH_RECAPTURED_CCA,
    FISH_SHARE_OF_NET_INCOME,
    FISH_TERMINAL_LOSS,
    FISH_TOTAL_EXPENSES,
    FISH_VEHICLE_AVAILABLE_INTEREST,
    FISH_VEHICLE_BUSINESS_USE_PART,
    FISH_VEHICLE_INTEREST_FOR_PERIOD,
    FISH_VEHICLE_LEASE_CHARGE_PORTION,
    FISH_VEHICLE_LEASE_COST_PORTION,
    FISH_VEHICLE_LEASE_PRICE_85_PERCENT,
    FISH_VEHICLE_LEASE_PRICE_BASE,
    FISH_VEHICLE_LEASING_COST,
    FISH_VEHICLE_LIST_PRICE_LIMIT_WITH_TAX,
    FISH_VEHICLE_TOTAL_EXPENSES,
    FISHING_INCOME,
    NET_INCOME,
    NET_SELF_EMPLOYMENT_INCOME,
    REFUND_OR_BALANCE_OWING,
    TAXABLE_INCOME,
    TOTAL_INCOME,
    TOTAL_PAYABLE,
)
from app.jurisdictions.ca_on.catalog import ONTARIO_BASIC_TAX
from tests.jurisdictions.ca_on.end_to_end.support import D, compute

# Return BD's T2121: fish products of 40000 (amount 3A), expenses of 25000 (salt, bait and ice 10000
# on line 9138, and fishing gear 15000 on line 9136), with no capital cost allowance, repairs,
# partner
# or business-use-of-home amounts.
FISH = {
    "fish_products": "40000",
    "salt_bait_and_ice": "10000",
    "fishing_gear": "15000",
    # Charts A to C for one leased passenger vehicle that is used for no fishing: business
    # kilometres 0 (amount 1), so line 9281 (amount 16 of Chart A) is 0, the same as before the
    # charts; every Chart B and C line is still computed as printed.
    "vehicle_business_kilometres": "0",
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


def return_bd() -> Worksheet:
    """Return BD's inputs, as in `returns/2025_return_bd.yaml`: a sole proprietor whose only
    activity is a fishing business, one T2121 for it: income of 40000 (line 8299 and T1 line 14299),
    expenses of 25000 (4Q), so line 9369 is 15000, which is line 9946 and T1 line 14300.
    """
    return compute("0", (), "0", "0", "0", "0", "0", fish=FISH)


def test_return_bds_gross_fishing_income_is_40000_on_line_8299_and_t1_line_14299() -> None:
    # Part 3: the income lines 3A to 3F and line 9600 "Other income (specify)" add to 40000 with no
    # recapture (no Area A rows) and line 9600 0, so line 8299, "Gross income", is 40000, which is
    # T1 line 14299 and amount 4A.
    worksheet = return_bd()

    assert worksheet.get(FISH_RECAPTURED_CCA).value == D("0")
    assert worksheet.get(FISH_GROSS_INCOME).value == D("40000")
    assert worksheet.get(FISH_GROSS_INCOME_BEFORE_EXPENSES).value == D("40000")


def test_return_bds_expenses_are_25000_and_net_income_before_adjustments_15000() -> None:
    # Part 4: amount 4Q is the expense lines (10000 + 15000) with no repairs, 0 terminal loss and 0
    # other expenses, so 25000; line 9368 is 4Q plus line 9936, 25000 + 0; line 9369 is
    # 40000 - 25000 = 15000.
    worksheet = return_bd()

    assert worksheet.get(FISH_EXPENSES_SUBTOTAL).value == D("25000")
    assert worksheet.get(FISH_TOTAL_EXPENSES).value == D("25000")
    assert worksheet.get(FISH_NET_INCOME_BEFORE_ADJUSTMENTS).value == D("15000")


def test_return_bds_has_no_cca_terminal_loss_or_recapture() -> None:
    # No Area A rows: the CCA claim (line 9936), the terminal loss (line 9270) and the recapture
    # (line 9600) are all 0, so none of them changes the figures above.
    worksheet = return_bd()

    assert worksheet.get(FISH_CCA_CLAIM_LESS_PERSONAL_PART).value == D("0")
    assert worksheet.get(FISH_CCA_CLAIM).value == D("0")
    assert worksheet.get(FISH_TERMINAL_LOSS).value == D("0")
    assert worksheet.get(FISH_OTHER_EXPENSES_WITH_TERMINAL_LOSS).value == D("0")


def test_return_bds_sole_proprietor_has_no_partnership_amounts() -> None:
    # No partner (count 0): amount 5A is line 9369, 15000, whatever the T5013 amount; line 9974 and
    # amounts 6A to 6E are 0, so amount 5B is 15000, line 9943 is 0 and amount 5C is 15000.
    worksheet = return_bd()

    assert worksheet.get(FISH_SHARE_OF_NET_INCOME).value == D("15000")
    assert worksheet.get(FISH_PARTNER_OTHER_AMOUNTS).value == D("0")
    assert worksheet.get(FISH_PARTNERSHIP_TOTAL).value == D("15000")
    assert worksheet.get(FISH_NET_INCOME_AFTER_ADJUSTMENTS).value == D("15000")


def test_return_bds_business_use_of_home_is_nil() -> None:
    # Part 7: every amount 7A to 7L is 0, so amounts 7H, 7J, 7M and line 9945 are 0; amount 7N is
    # amount 5C, 15000, and amount 7O is 0, so amount 7P is 0.
    worksheet = return_bd()

    assert worksheet.get(FISH_HOME_EXPENSES_AVAILABLE).value == D("0")
    assert worksheet.get(FISH_HOME_INCOME_LIMIT).value == D("15000")
    assert worksheet.get(FISH_HOME_CARRY_FORWARD).value == D("0")
    assert worksheet.get(FISH_HOME_ALLOWABLE_CLAIM).value == D("0")
    assert worksheet.get(FISH_HOME_EXPENSES).value == D("0")


def test_return_bds_net_fishing_income_is_15000_on_line_9946_and_t1_line_14300() -> None:
    # Line 9946 is amount 5C minus line 9945: 15000 - 0 = 15000, T1 line 26 and line 14300; the net
    # self-employment income (line 27) is 0 + 0 + 0 + 0 + 15000.
    worksheet = return_bd()

    assert worksheet.get(FISHING_INCOME).value == D("15000")
    assert worksheet.get(NET_SELF_EMPLOYMENT_INCOME).value == D("15000")


def test_return_bds_line_27_is_in_total_income_and_flows_down() -> None:
    # Line 27 (15000) is in total income (line 15000) and there is no other income, so total
    # income, net income and taxable income are 15000, and the tax is on the same figure: federal
    # basic tax 2175.00 (before the credits of 2338.71, which take the tax to 0), Ontario basic tax
    # 757.50, the Ontario tax reduction takes the Ontario tax to 0, and no balance is owing.
    worksheet = return_bd()

    assert worksheet.get(TOTAL_INCOME).value == D("15000.00")
    assert worksheet.get(NET_INCOME).value == D("15000.00")
    assert worksheet.get(TAXABLE_INCOME).value == D("15000.00")
    assert worksheet.get(FEDERAL_BASIC_TAX).value == D("2175.00")
    assert worksheet.get(ONTARIO_BASIC_TAX).value == D("757.50")
    assert worksheet.get(TOTAL_PAYABLE).value == D("0.00")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("0.00")


def test_return_bds_trace_names_each_line_of_the_fish_statement() -> None:
    rendered = EnglishTraceRenderer().render_all(return_bd().trace)

    for rendered_line in (
        "fish_gross_income_before_expenses: fish_gross_income 40000 = 40000",
        "fish_total_expenses: fish_expenses_subtotal 25000 + fish_cca_claim 0 = 25000",
        "fish_net_income_before_adjustments: fish_gross_income_before_expenses 40000 "
        "less fish_total_expenses 25000 = 15000",
        "fish_share_of_net_income: fish_net_income_before_adjustments 15000, "
        "chosen as fish_partner is 0",
        "fish_partnership_total: fish_share_of_net_income 15000 "
        "+ fish_partner_gst_hst_rebate 0 = 15000",
        "fish_net_income_after_adjustments: fish_partnership_total 15000 "
        "less fish_partner_other_amounts 0 = 15000",
        "fish_home_expenses_available: fish_home_expenses_business_part 0 "
        "+ fish_home_cca 0 + fish_home_carried_forward 0 = 0",
        "fish_home_income_limit: fish_net_income_after_adjustments 15000, not below 0 = 15000",
        "fish_home_carry_forward: fish_home_expenses_available 0 "
        "less fish_home_income_limit 15000, not below 0 = 0",
        "fish_home_allowable_claim: lesser of fish_home_expenses_available 0 "
        "and fish_home_income_limit 15000 = 0",
        "fish_home_expenses: fish_home_allowable_claim 0 = 0",
        "fishing_income: fish_net_income_after_adjustments 15000 less fish_home_expenses 0 = 15000",
        "net_self_employment_income: business_income 0 + professional_income 0 "
        "+ commission_income 0 + farming_income 0 + fishing_income 15000 = 15000",
    ):
        assert rendered_line in rendered, rendered_line


def test_return_bds_motor_vehicle_line_9281_is_0_from_charts_a_to_c() -> None:
    # Chart B: 350 ÷ 30 × 183 days = 2135.00, and the lesser of that and the 400 payable is 400.
    # Chart C: 44706 plus 13% is 50517.78, 1100 plus 13% is 1243.00 and 38000 plus 13% is 42940.00;
    # 60000 is the greater of 60000 and 50517.78, 85% of it is 51000.00, 1243.00 x 183 ÷ 30 is
    # 7582.30 and 42940.00 x 2550 ÷ 51000.00 is 2147.00, so the leasing cost is 2147.00. Chart A:
    # 1000 + 400 + 600 + 200 + 2147 + 653 = 5000, and 0 kilometres for fishing give a business use
    # part of 0 x 5000 ÷ 10000 = 0, so line 9281 is 0 and the fishing expenses are still 25000.
    worksheet = return_bd()

    assert worksheet.get(FISH_VEHICLE_INTEREST_FOR_PERIOD).value == D("2135.00")
    assert worksheet.get(FISH_VEHICLE_AVAILABLE_INTEREST).value == D("400.00")
    assert worksheet.get(FISH_VEHICLE_LIST_PRICE_LIMIT_WITH_TAX).value == D("50517.78")
    assert worksheet.get(FISH_VEHICLE_LEASE_PRICE_BASE).value == D("60000.00")
    assert worksheet.get(FISH_VEHICLE_LEASE_PRICE_85_PERCENT).value == D("51000.00")
    assert worksheet.get(FISH_VEHICLE_LEASE_CHARGE_PORTION).value == D("7582.30")
    assert worksheet.get(FISH_VEHICLE_LEASE_COST_PORTION).value == D("2147.00")
    assert worksheet.get(FISH_VEHICLE_LEASING_COST).value == D("2147.00")
    assert worksheet.get(FISH_VEHICLE_TOTAL_EXPENSES).value == D("5000.00")
    assert worksheet.get(FISH_VEHICLE_BUSINESS_USE_PART).value == D("0.00")
    assert worksheet.get(FISH_MOTOR_VEHICLE_EXPENSES).value == D("0.00")
    assert worksheet.get(FISH_EXPENSES_SUBTOTAL).value == D("25000")
