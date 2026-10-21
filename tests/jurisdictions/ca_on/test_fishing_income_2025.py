"""The 2025 fishing income lines (T2121 Parts 3 to 7 and Area A, T1 lines 14299 and 14300), checked
against CRA's form.

2025 Form T2121 (Statement of Fishing Activities), Part 3 "Gross income: Total of amounts 3A to 3F
and line 9600 (enter this amount on line 14299 of your income tax and benefit return)"; Part 4
"Gross income (line 8299 of Part 3)" (4A), "Subtotal: Add amounts 4B to 4P." (4Q), "Total expenses:
Amount 4Q plus line 9936" (9368) and "Net income (loss) before adjustments: Amount 4A minus line
9368"
(9369); "Your cost (amount 4 minus amount 5)" (line 8963, amount 4O); Part 5 "Your share of line
9369
or the amount from your T5013 slip, Statement of Partnership Income" (5A), "Total: Amount 5A plus
line 9974" (5B) and "Your net income (loss): Amount 5C minus line 9945 (enter this amount on line
14300
of your income tax and benefit return)" (9946); Part 7 "Net income (loss) after adjustments (amount
5C) (if negative, enter "0")." and "Allowable claim: Amount 7M or 7N above, whichever is less (enter
your share of this amount on line 9945 of Part 5)"; Area A endnote 3: "If you have a negative amount
in column 7, add it to income as a recapture in Part 3 on line 9600. If no property is left in the
class and there is a positive amount in this column, deduct the amount from income as a terminal
loss
in Part 4 on line 9270. Recapture and terminal loss do not apply to a Class 10.1 property unless it
is
a DIEP." Every amount of the form is a dollars-and-cents box, and these lines only add and subtract
amounts already in cents (the capital cost allowance columns round with the `ca/cca_class_rates`
dataset, tested in test_rental_cca_2025.py), so the lines have no dataset of their own.

The lines are tested here one rule at a time on the registered kinds; the lines together, from the
income lines to T1 lines 14299 and 14300, are in `end_to_end/test_return_bd.py` and
`returns/2025_return_bd.yaml`.
"""

from __future__ import annotations

from typing import Any

from app.domain.artifact import ArtifactKind
from app.domain.worksheet import Worksheet
from app.jurisdictions.ca.catalog import (
    FISH_CCA_CLAIM,
    FISH_CCA_CLAIM_LESS_PERSONAL_PART,
    FISH_CCA_TABLE_CLAIM,
    FISH_EXPENSES_SUBTOTAL,
    FISH_GROSS_INCOME,
    FISH_GROSS_INCOME_BEFORE_EXPENSES,
    FISH_HOME_ALLOWABLE_CLAIM,
    FISH_HOME_CARRY_FORWARD,
    FISH_HOME_EXPENSES,
    FISH_HOME_EXPENSES_AVAILABLE,
    FISH_HOME_INCOME_LIMIT,
    FISH_NET_INCOME_AFTER_ADJUSTMENTS,
    FISH_NET_INCOME_BEFORE_ADJUSTMENTS,
    FISH_OTHER_EXPENSES_WITH_TERMINAL_LOSS,
    FISH_OTHER_INCOME_WITH_RECAPTURE,
    FISH_PARTNER_OTHER_AMOUNTS,
    FISH_PARTNER_OTHER_AMOUNTS_TOTAL,
    FISH_PARTNERSHIP_TOTAL,
    FISH_RECAPTURED_CCA,
    FISH_REPAIRS_TOTAL,
    FISH_REPAIRS_YOUR_COST,
    FISH_SHARE_OF_NET_INCOME,
    FISH_TERMINAL_LOSS,
    FISH_TOTAL_EXPENSES,
    FISHING_INCOME,
)
from tests.jurisdictions.ca_on.end_to_end.support import D, compute

# Return BD's statement, the default of these tests: one fish products amount of 40000 (amount 3A),
# expenses of 25000 (salt, bait and ice 10000 on line 9138, fishing gear 15000 on line 9136), so
# line
# 9369 is 15000, and no CCA, repairs, partner or business-use-of-home amounts.
DEFAULT_FISH = {"fish_products": "40000", "salt_bait_and_ice": "10000", "fishing_gear": "15000"}

# The 14 expense amounts of Part 4 that are entered directly, in the form's order: lines 4B to 4N
# and the other expenses of line 9270 (4P).
EXPENSE_NAMES = (
    "salt_bait_and_ice",
    "crew_shares",
    "fuel_costs",
    "fishing_gear",
    "insurance",
    "interest_and_bank_charges",
    "meals_and_entertainment",
    "business_taxes_licences_and_memberships",
    "motor_vehicle_expenses",
    "office_expenses",
    "nets_and_traps",
    "professional_fees",
    "salaries_wages_and_benefits",
    "other_expenses",
)

CcaRow = tuple[str, str, str, str, str, str, str, int]


def statement(
    fish: dict[str, str] | None = None,
    partner: int = 0,
    cca_classes: tuple[CcaRow, ...] = (),
    **overrides: Any,
) -> Worksheet:
    """Return BD's statement with `fish` changing or adding its amounts, `partner` the partner
    count (amount 5A) and `cca_classes` the Area A rows."""
    amounts = {**DEFAULT_FISH, **(fish or {})}
    return compute(
        "0",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
        fish=amounts,
        fish_partner=partner,
        fish_cca_classes_rows=cca_classes,
        **overrides,
    )


def line(worksheet: Worksheet, kind: ArtifactKind[Any]) -> Any:
    return worksheet.get(kind).value


def test_the_income_lines_3a_to_3f_and_line_9600_add_to_line_8299() -> None:
    # Amounts 3B "Other marine products" 1000, 3C "Grants, credits, and rebates" 2000 and 3D
    # "Subsidies" 4000 are entry lines, so line 8299 is 40000 + 1000 + 2000 + 4000 = 47000, and
    # amount
    # 4A is the same.
    worksheet = statement(
        {
            "other_marine_products": "1000",
            "grants_credits_and_rebates": "2000",
            "subsidies": "4000",
        }
    )

    assert line(worksheet, FISH_GROSS_INCOME) == D("47000")
    assert line(worksheet, FISH_GROSS_INCOME_BEFORE_EXPENSES) == D("47000")


def test_a_statement_with_no_other_amounts_is_the_income_less_the_expenses() -> None:
    # Income 40000 (line 8299 and T1 line 14299); expenses 25000 (4B and 4E), no CCA, so line 9368
    # is
    # 25000 and line 9369 is 40000 - 25000 = 15000, which is line 9946 and T1 line 14300.
    worksheet = statement()

    assert line(worksheet, FISH_GROSS_INCOME_BEFORE_EXPENSES) == D("40000")
    assert line(worksheet, FISH_EXPENSES_SUBTOTAL) == D("25000")
    assert line(worksheet, FISH_TOTAL_EXPENSES) == D("25000")
    assert line(worksheet, FISH_NET_INCOME_BEFORE_ADJUSTMENTS) == D("15000")
    assert line(worksheet, FISHING_INCOME) == D("15000")


def test_a_recapture_row_adds_the_negative_column_7_to_line_9600() -> None:
    # Class 8: UCC at the start 1000, proceeds of dispositions 4000, so column 7 is
    # 1000 + 0 - 4000 = -3000, "a negative amount in column 7", added to income as a recapture on
    # line 9600: 3000. Other income of 500 makes line 9600 3500 (500 + 3000), so line 8299 is
    # 40000 + 3500 = 43500 and line 9369 is 43500 - 25000 = 18500. No claim is allowed on a
    # negative column 7.
    worksheet = statement(
        {"other_income": "500"},
        cca_classes=(("8", "1000", "0", "4000", "0", "0", "0", 0),),
    )

    assert line(worksheet, FISH_RECAPTURED_CCA) == D("3000")
    assert line(worksheet, FISH_OTHER_INCOME_WITH_RECAPTURE) == D("3500")
    assert line(worksheet, FISH_GROSS_INCOME_BEFORE_EXPENSES) == D("43500")
    assert line(worksheet, FISH_CCA_CLAIM) == D("0")
    assert line(worksheet, FISH_NET_INCOME_BEFORE_ADJUSTMENTS) == D("18500")


def test_a_terminal_loss_row_takes_the_positive_column_7_off_on_line_9270() -> None:
    # Class 8 with no property left: column 7 is 1000 + 0 - 0 = 1000, positive, so it is deducted
    # from income as a terminal loss in Part 4 on line 9270 (4P), with no CCA claimed on the class.
    # Line 9270 is 0 + 1000 = 1000, so 4Q is 25000 + 1000 = 26000 and line 9369 is
    # 40000 - 26000 = 14000.
    worksheet = statement(
        cca_classes=(("8", "1000", "0", "0", "0", "0", "0", 1),),
    )

    assert line(worksheet, FISH_TERMINAL_LOSS) == D("1000")
    assert line(worksheet, FISH_OTHER_EXPENSES_WITH_TERMINAL_LOSS) == D("1000")
    assert line(worksheet, FISH_EXPENSES_SUBTOTAL) == D("26000")
    assert line(worksheet, FISH_CCA_CLAIM) == D("0")
    assert line(worksheet, FISH_NET_INCOME_BEFORE_ADJUSTMENTS) == D("14000")


def test_a_class_with_property_left_has_no_terminal_loss() -> None:
    # Column 7 is positive but property is left in the class, so no terminal loss: line 9270 is 0.
    worksheet = statement(cca_classes=(("8", "1000", "0", "0", "0", "0", "0", 0),))

    assert line(worksheet, FISH_TERMINAL_LOSS) == D("0")
    assert line(worksheet, FISH_OTHER_EXPENSES_WITH_TERMINAL_LOSS) == D("0")
    assert line(worksheet, FISH_EXPENSES_SUBTOTAL) == D("25000")


def test_class_10_1_has_no_recapture_or_terminal_loss() -> None:
    # Class 10.1, column 7 is 1000 + 0 - 4000 = -3000 and no property is left: "Recapture and
    # terminal loss do not apply to a Class 10.1 property unless it is a DIEP", so both are 0.
    worksheet = statement(cca_classes=(("10.1", "1000", "0", "4000", "0", "0", "0", 1),))

    assert line(worksheet, FISH_RECAPTURED_CCA) == D("0")
    assert line(worksheet, FISH_TERMINAL_LOSS) == D("0")
    assert line(worksheet, FISH_NET_INCOME_BEFORE_ADJUSTMENTS) == D("15000")


def test_one_class_list_gives_a_claim_a_recapture_and_a_terminal_loss_together() -> None:
    # Class 8: UCC 10000, a claim of 2000 (the maximum, 10000 x 20%); class 10: column 7 of
    # -3000, a recapture of 3000 on line 9600; class 6: column 7 of 500 with no property left, a
    # terminal loss of 500 on line 9270. Line 9936 is 2000; line 9270 is 500; 4Q is 25000 + 500 =
    # 25500; line 9368 is 25500 + 2000 = 27500; line 8299 is 40000 + 3000 = 43000, so line 9369 is
    # 43000 - 27500 = 15500.
    worksheet = statement(
        cca_classes=(
            ("8", "10000", "0", "0", "0", "0", "2000", 0),
            ("10", "1000", "0", "4000", "0", "0", "0", 0),
            ("6", "500", "0", "0", "0", "0", "0", 1),
        ),
    )

    assert line(worksheet, FISH_CCA_TABLE_CLAIM) == D("2000")
    assert line(worksheet, FISH_CCA_CLAIM) == D("2000")
    assert line(worksheet, FISH_RECAPTURED_CCA) == D("3000")
    assert line(worksheet, FISH_TERMINAL_LOSS) == D("500")
    assert line(worksheet, FISH_EXPENSES_SUBTOTAL) == D("25500")
    assert line(worksheet, FISH_TOTAL_EXPENSES) == D("27500")
    assert line(worksheet, FISH_NET_INCOME_BEFORE_ADJUSTMENTS) == D("15500")


def test_the_personal_part_and_the_business_use_of_home_cca_come_off_line_9936() -> None:
    # Amount ii is 2000; the personal part (a caller's 500) comes off to give 1500, and the CCA for
    # business-use-of-home expenses (amount 7K, a caller's 300) comes off to give line 9936, 1200.
    # Line 9368 is 25000 + 1200 = 26200, so line 9369 is 40000 - 26200 = 13800. Amount 7M is
    # 0 + 300 + 0 = 300 and line 9945 is 300, so line 9946 is 13800 - 300 = 13500.
    worksheet = statement(
        {"cca_personal_part": "500", "home_cca": "300"},
        cca_classes=(("8", "10000", "0", "0", "0", "0", "2000", 0),),
    )

    assert line(worksheet, FISH_CCA_CLAIM_LESS_PERSONAL_PART) == D("1500")
    assert line(worksheet, FISH_CCA_CLAIM) == D("1200")
    assert line(worksheet, FISH_TOTAL_EXPENSES) == D("26200")
    assert line(worksheet, FISH_NET_INCOME_BEFORE_ADJUSTMENTS) == D("13800")
    assert line(worksheet, FISH_HOME_EXPENSES_AVAILABLE) == D("300")
    assert line(worksheet, FISH_HOME_EXPENSES) == D("300")
    assert line(worksheet, FISHING_INCOME) == D("13500")


def test_every_expense_line_and_other_expenses_add_to_4q() -> None:
    # Each of the 14 amounts of Part 4 that is entered (lines 4B to 4N and the other expenses of
    # line 9270, 4P) is 100: 4Q is 1400, and with the income of 40000, line 9369 is 40000 - 1400 =
    # 38600.
    worksheet = statement({name: "100" for name in EXPENSE_NAMES})

    assert line(worksheet, FISH_EXPENSES_SUBTOTAL) == D("1400")
    assert line(worksheet, FISH_NET_INCOME_BEFORE_ADJUSTMENTS) == D("38600")


def test_the_repairs_total_less_the_insurance_recovery_is_line_8963_and_adds_to_4q() -> None:
    # Repairs of the fishing boat 1000, engine 2000 and electrical equipment 500 are amount 4, 3500;
    # with an insurance recovery of 800 (amount 5), "Your cost" (amount 4O, line 8963) is 2700,
    # which
    # adds to 4Q: 25000 + 2700 = 27700, so line 9369 is 40000 - 27700 = 12300.
    worksheet = statement(
        {
            "repairs_fishing_boat": "1000",
            "repairs_engine": "2000",
            "repairs_electrical_equipment": "500",
            "insurance_recovery": "800",
        }
    )

    assert line(worksheet, FISH_REPAIRS_TOTAL) == D("3500")
    assert line(worksheet, FISH_REPAIRS_YOUR_COST) == D("2700")
    assert line(worksheet, FISH_EXPENSES_SUBTOTAL) == D("27700")
    assert line(worksheet, FISH_NET_INCOME_BEFORE_ADJUSTMENTS) == D("12300")


def test_an_insurance_recovery_above_the_repairs_is_a_negative_line_8963_with_no_floor() -> None:
    # Amount 4 is 3500 and amount 5 is 4000, so "Your cost (amount 4 minus amount 5)" is -500: the
    # form prints no floor, so line 8963 is -500 and 4Q is 25000 - 500 = 24500.
    worksheet = statement(
        {
            "repairs_fishing_boat": "1000",
            "repairs_engine": "2000",
            "repairs_electrical_equipment": "500",
            "insurance_recovery": "4000",
        }
    )

    assert line(worksheet, FISH_REPAIRS_YOUR_COST) == D("-500")
    assert line(worksheet, FISH_EXPENSES_SUBTOTAL) == D("24500")


def test_a_recovery_above_the_repairs_with_no_other_expenses_is_a_negative_4q_and_9368() -> None:
    # Repairs of 100 (amount 4) and an insurance recovery of 300 (amount 5) give "Your cost" of
    # -200 (amount 4O). With no other expenses (the default salt, bait and ice and fishing gear
    # are zeroed) amount 4Q is -200 and line 9368 is -200 + 0 = -200, with no error. Income 3A of
    # 40000 is amount 4A, so line 9369 is 40000 - (-200) = 40200.
    worksheet = statement(
        {
            "salt_bait_and_ice": "0",
            "fishing_gear": "0",
            "repairs_fishing_boat": "100",
            "insurance_recovery": "300",
        }
    )

    assert line(worksheet, FISH_REPAIRS_YOUR_COST) == D("-200")
    assert line(worksheet, FISH_EXPENSES_SUBTOTAL) == D("-200")
    assert line(worksheet, FISH_TOTAL_EXPENSES) == D("-200")
    assert line(worksheet, FISH_NET_INCOME_BEFORE_ADJUSTMENTS) == D("40200")
    assert line(worksheet, FISHING_INCOME) == D("40200")


def test_a_partner_takes_the_t5013_amount_for_amount_5a() -> None:
    # One partner (count 1): amount 5A is the T5013 amount, 12000, as entered; line 9946 is then
    # 12000 - 0 = 12000.
    worksheet = statement({"partner_share": "12000"}, partner=1)

    assert line(worksheet, FISH_SHARE_OF_NET_INCOME) == D("12000")
    assert line(worksheet, FISH_PARTNERSHIP_TOTAL) == D("12000")
    assert line(worksheet, FISH_NET_INCOME_AFTER_ADJUSTMENTS) == D("12000")
    assert line(worksheet, FISHING_INCOME) == D("12000")


def test_a_sole_proprietor_ignores_the_t5013_amount() -> None:
    # No partner (count 0): amount 5A is line 9369, 15000, whatever the T5013 amount entered.
    worksheet = statement({"partner_share": "12000"})

    assert line(worksheet, FISH_SHARE_OF_NET_INCOME) == D("15000")
    assert line(worksheet, FISHING_INCOME) == D("15000")


def test_the_gst_hst_rebate_for_partners_comes_into_amount_5b() -> None:
    # Amount 5B is amount 5A (15000) plus line 9974 (GST/HST rebate for partners, 200): 15200, and
    # with no partner amounts it is line 9946.
    worksheet = statement({"partner_gst_hst_rebate": "200"})

    assert line(worksheet, FISH_PARTNERSHIP_TOTAL) == D("15200")
    assert line(worksheet, FISHING_INCOME) == D("15200")


def test_a_loss_is_line_9369_below_zero_and_line_14300_in_brackets() -> None:
    # Income of 10000 (fish products) against expenses of 25000: line 9369 is -15000, and so are
    # amount 5A and line 9946, which is T1 line 14300 "(loss)"; the form prints no floor.
    worksheet = statement({"fish_products": "10000"})

    assert line(worksheet, FISH_NET_INCOME_BEFORE_ADJUSTMENTS) == D("-15000")
    assert line(worksheet, FISH_SHARE_OF_NET_INCOME) == D("-15000")
    assert line(worksheet, FISH_NET_INCOME_AFTER_ADJUSTMENTS) == D("-15000")
    assert line(worksheet, FISHING_INCOME) == D("-15000")


def test_amount_7o_carries_the_whole_claim_forward_when_amount_5c_is_negative() -> None:
    # A loss of 15000 (amount 5C is -15000): business-use-of-home expenses of 2000 (amount 7A, heat)
    # give 7M of 2000. Amount 7N is 0 (not negative) "if negative, enter "0"", so amount 7P is the
    # lesser of 2000 and 0, 0, line 9945 is 0 and amount 7O carries the whole 2000 forward.
    worksheet = statement({"fish_products": "10000", "home_heat": "2000"})

    assert line(worksheet, FISH_HOME_EXPENSES_AVAILABLE) == D("2000")
    assert line(worksheet, FISH_HOME_INCOME_LIMIT) == D("0")
    assert line(worksheet, FISH_HOME_CARRY_FORWARD) == D("2000")
    assert line(worksheet, FISH_HOME_ALLOWABLE_CLAIM) == D("0")
    assert line(worksheet, FISH_HOME_EXPENSES) == D("0")
    assert line(worksheet, FISHING_INCOME) == D("-15000")


def test_amount_7o_is_0_when_amount_7n_is_larger_and_amount_7p_is_amount_7m() -> None:
    # Amount 7M is 2000 and amount 7N is amount 5C, 15000, so amount 7O is 0 and amount 7P, the
    # allowable claim, is 2000, which is line 9945; line 9946 is 15000 - 2000 = 13000.
    worksheet = statement({"home_heat": "2000"})

    assert line(worksheet, FISH_HOME_CARRY_FORWARD) == D("0")
    assert line(worksheet, FISH_HOME_ALLOWABLE_CLAIM) == D("2000")
    assert line(worksheet, FISH_HOME_EXPENSES) == D("2000")
    assert line(worksheet, FISHING_INCOME) == D("13000")


def test_amount_7p_is_amount_7n_when_the_home_expenses_exceed_the_net_income() -> None:
    # Net income of 1000 (amount 5C), amount 7M 3000 (heat): amount 7N is 1000, amount 7O is
    # 3000 - 1000 = 2000 carried forward and amount 7P, the lesser, is 1000, which is line 9945, so
    # line 9946 is 1000 - 1000 = 0.
    worksheet = statement({"fish_products": "26000", "home_heat": "3000"})

    assert line(worksheet, FISH_NET_INCOME_AFTER_ADJUSTMENTS) == D("1000")
    assert line(worksheet, FISH_HOME_CARRY_FORWARD) == D("2000")
    assert line(worksheet, FISH_HOME_ALLOWABLE_CLAIM) == D("1000")
    assert line(worksheet, FISHING_INCOME) == D("0")


def test_the_partner_other_amounts_come_off_at_line_9943() -> None:
    # Amounts 6A and 6B (100 and 200) make amount 6F and line 9943, 300; amount 5C is 15000 - 300.
    worksheet = statement({"partner_other_amount_a": "100", "partner_other_amount_b": "200"})

    assert line(worksheet, FISH_PARTNER_OTHER_AMOUNTS_TOTAL) == D("300")
    assert line(worksheet, FISH_PARTNER_OTHER_AMOUNTS) == D("300")
    assert line(worksheet, FISH_NET_INCOME_AFTER_ADJUSTMENTS) == D("14700")
    assert line(worksheet, FISHING_INCOME) == D("14700")
