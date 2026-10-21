"""CA-ON 2025 end to end: return bb."""

from __future__ import annotations

from typing import Any

from app.adapters.inbound.trace_english import EnglishTraceRenderer
from app.domain.artifact import ArtifactKind
from app.domain.worksheet import Worksheet
from app.jurisdictions.ca.catalog import (
    BUSINESS_ADJUSTED_GROSS_SALES,
    BUSINESS_CCA_CLAIM,
    BUSINESS_CCA_CLAIM_LESS_PERSONAL_PART,
    BUSINESS_CCA_TABLE_CLAIM,
    BUSINESS_CLOSING_UCC,
    BUSINESS_COST_OF_GOODS_SOLD,
    BUSINESS_COST_OF_GOODS_SUBTOTAL,
    BUSINESS_GROSS_INCOME,
    BUSINESS_GROSS_INCOME_BEFORE_EXPENSES,
    BUSINESS_GROSS_INCOME_FOR_GROSS_PROFIT,
    BUSINESS_GROSS_PROFIT,
    BUSINESS_HOME_ALLOWABLE_CLAIM,
    BUSINESS_HOME_CARRY_FORWARD,
    BUSINESS_HOME_EXPENSES,
    BUSINESS_HOME_EXPENSES_AVAILABLE,
    BUSINESS_HOME_EXPENSES_BUSINESS_PART,
    BUSINESS_HOME_EXPENSES_SUBTOTAL,
    BUSINESS_HOME_INCOME_LIMIT,
    BUSINESS_INCOME,
    BUSINESS_NET_INCOME_AFTER_ADJUSTMENTS,
    BUSINESS_NET_INCOME_BEFORE_ADJUSTMENTS,
    BUSINESS_OTHER_EXPENSES_WITH_TERMINAL_LOSS,
    BUSINESS_OTHER_INCOME_WITH_RECAPTURE,
    BUSINESS_PARTNER_OTHER_AMOUNTS,
    BUSINESS_PARTNER_OTHER_AMOUNTS_TOTAL,
    BUSINESS_PARTNERSHIP_TOTAL,
    BUSINESS_QUICK_METHOD_ASSISTANCE,
    BUSINESS_RECAPTURED_CCA,
    BUSINESS_RESERVES_AND_OTHER_INCOME,
    BUSINESS_SALES_SUBTOTAL,
    BUSINESS_SHARE_OF_NET_INCOME,
    BUSINESS_TERMINAL_LOSS,
    BUSINESS_TOTAL_EXPENSES,
    FEDERAL_BASIC_TAX,
    NET_INCOME,
    NET_SELF_EMPLOYMENT_INCOME,
    REFUND_OR_BALANCE_OWING,
    TAXABLE_INCOME,
    TOTAL_INCOME,
    TOTAL_PAYABLE,
)
from app.jurisdictions.ca_on.catalog import ONTARIO_BASIC_TAX
from tests.jurisdictions.ca_on.end_to_end.support import D, compute

# Return BB's T2125: gross sales 50000, the seven expense lines 1500 + 1200 + 800 + 2500 + 6000 +
# 1500 + 2500 = 16000, and the business-use-of-home expenses 600 + 500 + 300 + 200 + 400 = 2000.
BUSINESS = {
    "gross_sales": "50000",
    "advertising": "1500",
    "insurance": "1200",
    "office_expenses": "800",
    "professional_fees": "2500",
    "rent": "6000",
    "utilities": "1500",
    "motor_vehicle_expenses": "2500",
    "home_heat": "600",
    "home_electricity": "500",
    "home_insurance": "300",
    "home_maintenance": "200",
    "home_property_taxes": "400",
}
FURNITURE = ("8", "10000", "0", "0", "0", "0", "2000", 0)


def line(worksheet: Worksheet, kind: ArtifactKind[Any]) -> Any:
    """The value of the T2125 kind `kind` on `worksheet`."""
    return worksheet.get(kind).value


def return_bb(**overrides: Any) -> Worksheet:
    """Return BB's inputs, as in `returns/2025_return_bb.yaml`: a sole proprietor whose only
    activity is a business.

    One T2125 for the business: gross sales of 50000 (amount 3A, and so line 8299 and T1 line
    13499), expenses of 16000 on seven lines and 2000 of capital cost allowance (Class 8, opening
    UCC 10000, claim 2000), 18000 in all (line 9368), so line 9369 is 32000; business-use-of-home
    expenses of 2000, so line 9945 is 2000 and line 9946 and T1 line 13500 are 30000.
    """
    inputs: dict[str, Any] = {
        "business": BUSINESS,
        "business_cca_classes_rows": (FURNITURE,),
    }
    return compute("0", (), "0", "0", "0", "0", "0", **{**inputs, **overrides})


def test_return_bbs_gross_business_income_is_50000_on_line_8299_and_t1_line_13499() -> None:
    # Part 3A: amount 3A 50000 less amount 3B 0 is amount 3C 50000; the quick method is not used
    # (amounts 3D and 3E 0), so amount 3F is 0 and amount 3G, which is line 8000, is 50000 + 0.
    # Line 8290 and line 8230 are 0 (no reserves, other income or recapture), so amount 3O is 0
    # and line 8299, "Line 8000 plus amount 3O", is 50000. T1 line 13499 is line 8299.
    worksheet = return_bb()

    assert line(worksheet, BUSINESS_SALES_SUBTOTAL) == D("50000")
    assert line(worksheet, BUSINESS_QUICK_METHOD_ASSISTANCE) == D("0")
    assert line(worksheet, BUSINESS_ADJUSTED_GROSS_SALES) == D("50000")
    assert line(worksheet, BUSINESS_RECAPTURED_CCA) == D("0")
    assert line(worksheet, BUSINESS_OTHER_INCOME_WITH_RECAPTURE) == D("0")
    assert line(worksheet, BUSINESS_RESERVES_AND_OTHER_INCOME) == D("0")
    assert line(worksheet, BUSINESS_GROSS_INCOME) == D("50000")


def test_return_bbs_gross_profit_is_the_gross_income_with_no_cost_of_goods_sold() -> None:
    # Part 3D: amount 3P is line 8299, 50000; amounts 3Q to 3U and line 8500 are 0, so amount 3V
    # and line 8518 are 0 and line 8519 is 50000 - 0, which is amount 4A.
    worksheet = return_bb()

    assert line(worksheet, BUSINESS_GROSS_INCOME_FOR_GROSS_PROFIT) == D("50000")
    assert line(worksheet, BUSINESS_COST_OF_GOODS_SUBTOTAL) == D("0")
    assert line(worksheet, BUSINESS_COST_OF_GOODS_SOLD) == D("0")
    assert line(worksheet, BUSINESS_GROSS_PROFIT) == D("50000")
    assert line(worksheet, BUSINESS_GROSS_INCOME_BEFORE_EXPENSES) == D("50000")


def test_return_bbs_area_a_claims_2000_on_line_9936() -> None:
    # Area A, Class 8: column 7 is 10000 + 0 - 0 = 10000; with no additions column 18 is 0,
    # column 19 is 10000 and the maximum is 10000 x 20% = 2000.00; 2000 is claimed. Amount ii
    # is 2000; with no personal part or business-use-of-home CCA (amount 7K), line 9936 is 2000.
    # No class has a negative column 7 or is empty, so there is no recapture and no terminal loss.
    worksheet = return_bb()

    assert line(worksheet, BUSINESS_CCA_TABLE_CLAIM) == D("2000")
    assert line(worksheet, BUSINESS_CCA_CLAIM_LESS_PERSONAL_PART) == D("2000")
    assert line(worksheet, BUSINESS_CCA_CLAIM) == D("2000")
    assert line(worksheet, BUSINESS_RECAPTURED_CCA) == D("0")
    assert line(worksheet, BUSINESS_TERMINAL_LOSS) == D("0")
    assert line(worksheet, BUSINESS_OTHER_EXPENSES_WITH_TERMINAL_LOSS) == D("0")


def test_return_bbs_closing_ucc_is_8000_for_class_8() -> None:
    # Column 22 is column 7 less column 21: 10000 - 2000 = 8000, next year's column 2.
    worksheet = return_bb()

    closing = line(worksheet, BUSINESS_CLOSING_UCC)
    assert [list(record.values()) for record in closing.records] == [[D("8"), D("8000")]]


def test_return_bbs_total_expenses_are_18000_and_net_income_before_adjustments_32000() -> None:
    # Amounts 4B to 4T add to 16000 (the seven lines entered), amount 4U (line 9936) is 2000 and
    # amount 4V (line 9270) is 0: line 9368 is 18000. Line 9369 is 50000 - 18000 = 32000.
    worksheet = return_bb()

    assert line(worksheet, BUSINESS_TOTAL_EXPENSES) == D("18000")
    assert line(worksheet, BUSINESS_NET_INCOME_BEFORE_ADJUSTMENTS) == D("32000")


def test_return_bbs_sole_proprietor_has_no_partnership_amounts() -> None:
    # No partner (count 0): amount 5A is line 9369, 32000; amounts 5B and 9974 and 6A to 6E are 0,
    # so amount 5C is 32000, line 9943 is 0 and amount 5D is 32000.
    worksheet = return_bb()

    assert line(worksheet, BUSINESS_SHARE_OF_NET_INCOME) == D("32000")
    assert line(worksheet, BUSINESS_PARTNER_OTHER_AMOUNTS_TOTAL) == D("0")
    assert line(worksheet, BUSINESS_PARTNER_OTHER_AMOUNTS) == D("0")
    assert line(worksheet, BUSINESS_PARTNERSHIP_TOTAL) == D("32000")
    assert line(worksheet, BUSINESS_NET_INCOME_AFTER_ADJUSTMENTS) == D("32000")


def test_return_bbs_business_use_of_home_claim_is_2000() -> None:
    # Part 7: amount 7H is 600 + 500 + 300 + 200 + 0 + 400 + 0 = 2000, amount 7I is 0, so amount
    # 7J is 2000; amounts 7K and 7L are 0, so amount 7M is 2000. Amount 7N is amount 5D, 32000.
    # Amount 7O is 2000 - 32000, negative, so 0. Amount 7P, the lesser of 2000 and 32000, is 2000,
    # which is line 9945.
    worksheet = return_bb()

    assert line(worksheet, BUSINESS_HOME_EXPENSES_SUBTOTAL) == D("2000")
    assert line(worksheet, BUSINESS_HOME_EXPENSES_BUSINESS_PART) == D("2000")
    assert line(worksheet, BUSINESS_HOME_EXPENSES_AVAILABLE) == D("2000")
    assert line(worksheet, BUSINESS_HOME_INCOME_LIMIT) == D("32000")
    assert line(worksheet, BUSINESS_HOME_CARRY_FORWARD) == D("0")
    assert line(worksheet, BUSINESS_HOME_ALLOWABLE_CLAIM) == D("2000")
    assert line(worksheet, BUSINESS_HOME_EXPENSES) == D("2000")


def test_return_bbs_net_business_income_is_30000_on_line_9946_and_t1_line_13500() -> None:
    # Line 9946 is amount 5D less line 9945: 32000 - 2000 = 30000, T1 line 22 and line 13500; the
    # net self-employment income (line 27) is 30000 + 0 + 0 + 0 + 0.
    worksheet = return_bb()

    assert worksheet.get(BUSINESS_INCOME).value == D("30000")
    assert worksheet.get(NET_SELF_EMPLOYMENT_INCOME).value == D("30000")


def test_return_bbs_line_27_is_in_total_income_and_flows_down() -> None:
    # Line 27 (30000) is in total income (line 15000) and there is no other income, so total
    # income, net income and taxable income are 30000. With no employment income and Schedule 8
    # Part 4 not completed, no CPP or EI is computed.
    worksheet = return_bb()

    assert worksheet.get(TOTAL_INCOME).value == D("30000.00")
    assert worksheet.get(NET_INCOME).value == D("30000.00")
    assert worksheet.get(TAXABLE_INCOME).value == D("30000.00")
    assert worksheet.get(FEDERAL_BASIC_TAX).value == D("4350.00")
    assert worksheet.get(ONTARIO_BASIC_TAX).value == D("1515.00")
    assert worksheet.get(TOTAL_PAYABLE).value == D("3182.57")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("3182.57")


def test_return_bbs_trace_names_each_line_of_the_business_statement() -> None:
    rendered = EnglishTraceRenderer().render_all(return_bb().trace)

    for rendered_line in (
        "business_sales_subtotal: business_gross_sales 50000 less business_sales_adjustments 0 "
        "= 50000",
        "business_quick_method_assistance: business_quick_method_gst_hst 0 "
        "less business_quick_method_remitted 0 = 0",
        "business_adjusted_gross_sales: business_sales_subtotal 50000 "
        "+ business_quick_method_assistance 0 = 50000",
        "business_recaptured_cca: item 1 class 8: column 7 10000 is not negative: recapture 0",
        "business_other_income_with_recapture: business_other_income 0 "
        "+ business_recaptured_cca 0 = 0",
        "business_reserves_and_other_income: business_reserves_deducted_last_year 0 "
        "+ business_other_income_with_recapture 0 = 0",
        "business_gross_income: business_adjusted_gross_sales 50000 "
        "+ business_reserves_and_other_income 0 = 50000",
        "business_gross_income_for_gross_profit: business_gross_income 50000 = 50000",
        "business_cost_of_goods_sold: business_cost_of_goods_subtotal 0 "
        "less business_closing_inventory 0 = 0",
        "business_gross_profit: business_gross_income_for_gross_profit 50000 "
        "less business_cost_of_goods_sold 0 = 50000",
        "business_gross_income_before_expenses: business_gross_profit 50000 = 50000",
        "business_cca_table_claim: item 1 class 8: column 7 10000, column 14 0, column 15 0, "
        "column 16 0, column 17 0, column 18 0, column 19 10000, "
        "maximum 20% of column 19 = 2000 (half-up to 0.01), claim 2000",
        "business_cca_claim_less_personal_part: business_cca_table_claim 2000 "
        "less business_cca_personal_part 0 = 2000",
        "business_cca_claim: business_cca_claim_less_personal_part 2000 "
        "less business_home_cca 0 = 2000",
        "business_terminal_loss: item 1 class 8: column 7 10000 with property left: "
        "terminal loss 0",
        "business_other_expenses_with_terminal_loss: business_other_expenses 0 "
        "+ business_terminal_loss 0 = 0",
        "business_closing_ucc: item 1 class 8: column 7 10000 less claim 2000 = 8000",
        "business_net_income_before_adjustments: business_gross_income_before_expenses 50000 "
        "less business_total_expenses 18000 = 32000",
        "business_share_of_net_income: business_net_income_before_adjustments 32000, "
        "chosen as business_partner is 0",
        "business_partnership_total: business_share_of_net_income 32000 "
        "+ business_journalism_labour_tax_credit 0 + business_partner_gst_hst_rebate 0 = 32000",
        "business_net_income_after_adjustments: business_partnership_total 32000 "
        "less business_partner_other_amounts 0 = 32000",
        "business_home_expenses_available: business_home_expenses_business_part 2000 "
        "+ business_home_cca 0 + business_home_carried_forward 0 = 2000",
        "business_home_income_limit: business_net_income_after_adjustments 32000, "
        "not below 0 = 32000",
        "business_home_carry_forward: business_home_expenses_available 2000 "
        "less business_home_income_limit 32000, not below 0 = 0",
        "business_home_allowable_claim: lesser of business_home_expenses_available 2000 "
        "and business_home_income_limit 32000 = 2000",
        "business_home_expenses: business_home_allowable_claim 2000 = 2000",
        "business_income: business_net_income_after_adjustments 32000 "
        "less business_home_expenses 2000 = 30000",
        "net_self_employment_income: business_income 30000 + professional_income 0 "
        "+ commission_income 0 + farming_income 0 + fishing_income 0 = 30000",
    ):
        assert rendered_line in rendered, rendered_line
