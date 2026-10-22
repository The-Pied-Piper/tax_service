"""CA-ON 2025 end to end: return ad."""

from __future__ import annotations

from typing import Any

import pytest

from app.domain.errors import NegativeArtifactError, ValidationError
from app.domain.worksheet import Worksheet
from app.jurisdictions.ca.catalog import (
    GROSS_RENTAL_INCOME,
    NET_INCOME,
    NET_RENTAL_INCOME,
    REFUND_OR_BALANCE_OWING,
    RENTAL_CCA_CLAIM,
    RENTAL_DEDUCTIBLE_EXPENSES,
    RENTAL_EXPENSES_LESS_PERSONAL_PORTION,
    RENTAL_GROSS_RENTS,
    RENTAL_NET_INCOME_AFTER_CCA,
    RENTAL_NET_INCOME_AFTER_COOWNER_EXPENSES,
    RENTAL_NET_INCOME_AFTER_TERMINAL_LOSS,
    RENTAL_NET_INCOME_BEFORE_ADJUSTMENTS,
    RENTAL_NET_INCOME_SHARE,
    RENTAL_NET_INCOME_WITH_RECAPTURE,
    RENTAL_NON_COMPLIANT_EXPENSES,
    RENTAL_PARTNER_SHARE_WITH_REBATE,
    RENTAL_PARTNERSHIP_NET_INCOME,
    RENTAL_PERSONAL_PORTION,
    RENTAL_RECAPTURED_CCA,
    RENTAL_SHORT_TERM_PORTION,
    RENTAL_TERMINAL_LOSS,
    RENTAL_TOTAL_EXPENSES,
    SHORT_TERM_RENTAL_GROSS_RENTS,
    TAXABLE_INCOME,
    TOTAL_INCOME,
    TOTAL_PAYABLE,
)
from tests.jurisdictions.ca_on.end_to_end.support import (
    D,
    compute,
    render_flat,
    t776_line,
)


def return_ad(**overrides: Any) -> Worksheet:
    """Return AD's inputs, as in `returns/2025_return_ad.yaml`: a landlord with two rental units.

    Gross rents of 24000 (one property, two units) are the only income; the expenses are the
    insurance 1200, the interest 6000, the property taxes 3500 and the repairs 1300, 12000 in all,
    with no personal or short-term portion, so line 9946 and T1 line 12600 are 12000.
    """
    inputs: dict[str, Any] = {
        "employment_income": "0",
        "share_dispositions": (),
        "unused_rrsp_contributions": "0",
        "rrsp_contributions": "0",
        "rrsp_deduction_limit": "0",
        "rrsp_amount_deducted": "0",
        "union_dues": "0",
        "rental_properties": ((2, "0", "24000"),),
        "rental_expenses": {
            "insurance": ("1200", "0", "0"),
            "interest_and_bank_charges": ("6000", "0", "0"),
            "repairs_and_maintenance": ("1300", "0", "0"),
            "property_taxes": ("3500", "0", "0"),
        },
    }
    return compute(**{**inputs, **overrides})


def test_return_ads_gross_rents_are_24000_on_line_12599() -> None:
    # Form T776 Part 3: one property of two units, gross rents for all units 24000 and none for
    # short-term rentals, so line 8140 is 0 and line 8141 is 24000; with no other income (line
    # 8230) line 8299, and so T1 line 12599, is 24000.
    worksheet = return_ad()

    assert t776_line(worksheet, SHORT_TERM_RENTAL_GROSS_RENTS) == D("0")
    assert t776_line(worksheet, RENTAL_GROSS_RENTS) == D("24000")
    assert t776_line(worksheet, GROSS_RENTAL_INCOME) == D("24000")


def test_return_ads_net_rental_income_is_12000_on_line_12600() -> None:
    # Part 4: the expenses total 1200 + 6000 + 3500 + 1300 = 12000 (line A), with no personal
    # portion (line 9949), no short-term portion (line 9365) and no Chart A rows (line 9366 is 0),
    # so line 1 is 12000 and line 9369 is 24000 - 12000 = 12000. Sole proprietor, so amount 2 is
    # line 9369; with no co-owner expenses, recapture, terminal loss or CCA, amounts 3 to 6 are
    # 12000 too, and line 9946, T1 line 12600, is amount 6.
    worksheet = return_ad()

    assert t776_line(worksheet, RENTAL_TOTAL_EXPENSES) == D("12000")
    assert t776_line(worksheet, RENTAL_PERSONAL_PORTION) == D("0")
    assert t776_line(worksheet, RENTAL_SHORT_TERM_PORTION) == D("0")
    assert t776_line(worksheet, RENTAL_NON_COMPLIANT_EXPENSES) == D("0")
    assert t776_line(worksheet, RENTAL_EXPENSES_LESS_PERSONAL_PORTION) == D("12000")
    assert t776_line(worksheet, RENTAL_DEDUCTIBLE_EXPENSES) == D("12000")
    assert t776_line(worksheet, RENTAL_NET_INCOME_BEFORE_ADJUSTMENTS) == D("12000")
    assert t776_line(worksheet, RENTAL_NET_INCOME_SHARE) == D("12000")
    assert t776_line(worksheet, RENTAL_NET_INCOME_AFTER_COOWNER_EXPENSES) == D("12000")
    assert t776_line(worksheet, RENTAL_NET_INCOME_WITH_RECAPTURE) == D("12000")
    assert t776_line(worksheet, RENTAL_NET_INCOME_AFTER_TERMINAL_LOSS) == D("12000")
    assert t776_line(worksheet, RENTAL_NET_INCOME_AFTER_CCA) == D("12000")
    assert t776_line(worksheet, RENTAL_PARTNERSHIP_NET_INCOME) == D("0")
    assert worksheet.get(NET_RENTAL_INCOME).value == D("12000")


def test_return_ads_net_rental_income_is_the_only_income_on_line_15000() -> None:
    # T1 line 13 "Rental income" is line 12600 (net), not line 12599 (gross): total income is the
    # 12000, and so are net income and taxable income, below every tax threshold.
    worksheet = return_ad()

    assert worksheet.get(TOTAL_INCOME).value == D("12000")
    assert worksheet.get(NET_INCOME).value == D("12000.00")
    assert worksheet.get(TAXABLE_INCOME).value == D("12000.00")
    assert worksheet.get(TOTAL_PAYABLE).value == D("0")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("0")


def test_return_ads_trace_names_each_line_of_the_rental_income() -> None:
    rendered = render_flat(return_ad().trace)

    for line in (
        "short_term_rental_gross_rents: item 1 rental_property_short_term_rents 0 = 0",
        "rental_gross_rents: item 1 rental_property_gross_rents 24000 = 24000",
        "gross_rental_income: rental_gross_rents 24000 + rental_other_income 0 = 24000",
        "rental_total_expenses: rental_advertising 0 + rental_insurance 1200 "
        "+ rental_interest_and_bank_charges 6000 + rental_office_expenses 0 "
        "+ rental_professional_fees 0 + rental_management_and_administration_fees 0 "
        "+ rental_repairs_and_maintenance 1300 + rental_salaries_wages_and_benefits 0 "
        "+ rental_property_taxes 3500 + rental_travel 0 + rental_utilities 0 "
        "+ rental_motor_vehicle_expenses 0 + rental_other_expenses 0 = 12000",
        "rental_non_compliant_expenses: no items = 0",
        "rental_expenses_less_personal_portion: rental_total_expenses 12000 "
        "less rental_personal_portion 0 = 12000",
        "rental_deductible_expenses: rental_expenses_less_personal_portion 12000 "
        "less rental_non_compliant_expenses 0 = 12000",
        "rental_net_income_before_adjustments: gross_rental_income 24000 "
        "less rental_deductible_expenses 12000 = 12000",
        "rental_net_income_share: rental_net_income_before_adjustments 12000, "
        "chosen as rental_coowner is 0",
        "rental_net_income_after_coowner_expenses: rental_net_income_share 12000 "
        "less rental_coowner_other_expenses 0 = 12000",
        "rental_net_income_with_recapture: rental_net_income_after_coowner_expenses 12000 "
        "+ rental_recaptured_cca 0 = 12000",
        "rental_net_income_after_terminal_loss: rental_net_income_with_recapture 12000 "
        "less rental_terminal_loss 0 = 12000",
        "rental_net_income_after_cca: rental_net_income_after_terminal_loss 12000 "
        "less rental_cca_claim 0 = 12000",
        "net_rental_income: rental_net_income_after_cca 12000, chosen as rental_partner is 0",
    ):
        assert line in rendered, line
    total_income = [text for text in rendered if text.startswith("total_income: ")]
    assert len(total_income) == 1
    assert "+ rdsp_income 0 + net_rental_income 12000 + taxable_capital_gains 0 " in total_income[0]
    assert total_income[0].endswith("= 12000")


def test_a_short_term_rental_of_900_with_30_of_90_days_non_compliant_is_300_on_line_9366() -> None:
    # Chart A: one row of related expenses 900, 30 non-compliant days of 90 short-term days:
    # 900 x 30 / 90 = 300.00. The insurance's short-term portion of 900 (line 9365) is the row's
    # column 3; line 1 is the total expenses of 1200 less line 9949 (0) less line 9366 (300.00),
    # 900.00, so line 9369 is 24000 - 900.00 = 23100.00.
    worksheet = return_ad(
        rental_expenses={"insurance": ("1200", "0", "900")},
        short_term_rental_units_rows=(("900", 30, 90),),
    )

    assert t776_line(worksheet, RENTAL_SHORT_TERM_PORTION) == D("900")
    assert t776_line(worksheet, RENTAL_NON_COMPLIANT_EXPENSES) == D("300.00")
    assert t776_line(worksheet, RENTAL_DEDUCTIBLE_EXPENSES) == D("900.00")
    assert t776_line(worksheet, RENTAL_NET_INCOME_BEFORE_ADJUSTMENTS) == D("23100.00")
    assert worksheet.get(NET_RENTAL_INCOME).value == D("23100.00")
    rendered = render_flat(worksheet.trace)
    assert (
        "rental_non_compliant_expenses: row 1: expenses 900 for 30 non-compliant days of 90 "
        "short-term days = 300 (half-up to 0.01)"
    ) in rendered
    assert "rental_non_compliant_expenses: item 1 300 = 300" in rendered


def test_each_chart_a_row_is_worked_on_its_own_and_added_into_line_9366() -> None:
    worksheet = return_ad(
        rental_expenses={"insurance": ("1200", "0", "1000")},
        short_term_rental_units_rows=(("900", 30, 90), ("100", 2, 3)),
    )

    # 300.00 + 66.67, each row rounded half-up to the cent before the total.
    assert t776_line(worksheet, RENTAL_NON_COMPLIANT_EXPENSES) == D("366.67")
    rendered = render_flat(worksheet.trace)
    assert "rental_non_compliant_expenses: item 1 300 + item 2 66.67 = 366.67" in rendered


def test_a_personal_portion_comes_off_the_expenses_before_line_9366() -> None:
    # Line 1 is amount A minus line 9949 minus line 9366: 1200 - 200 = 1000, then 1000 - 0.
    worksheet = return_ad(rental_expenses={"insurance": ("1200", "200", "0")})

    assert t776_line(worksheet, RENTAL_PERSONAL_PORTION) == D("200")
    assert t776_line(worksheet, RENTAL_EXPENSES_LESS_PERSONAL_PORTION) == D("1000")
    assert t776_line(worksheet, RENTAL_DEDUCTIBLE_EXPENSES) == D("1000")


def test_other_income_on_line_8230_adds_to_line_8299_but_not_to_line_8141() -> None:
    worksheet = return_ad(rental_other_income="500")

    assert t776_line(worksheet, RENTAL_GROSS_RENTS) == D("24000")
    assert t776_line(worksheet, GROSS_RENTAL_INCOME) == D("24500")
    assert t776_line(worksheet, RENTAL_NET_INCOME_BEFORE_ADJUSTMENTS) == D("12500")
    assert worksheet.get(NET_RENTAL_INCOME).value == D("12500")


def test_short_term_rents_are_not_added_to_line_8141() -> None:
    # Line 8141 adds the "Gross rents for all units" column; line 8140 the short-term column.
    worksheet = return_ad(rental_properties=((2, "8000", "24000"), (1, "0", "6000")))

    assert t776_line(worksheet, SHORT_TERM_RENTAL_GROSS_RENTS) == D("8000")
    assert t776_line(worksheet, RENTAL_GROSS_RENTS) == D("30000")
    assert t776_line(worksheet, GROSS_RENTAL_INCOME) == D("30000")


def test_a_rental_loss_of_2000_is_line_12600_of_minus_2000_and_lowers_total_income() -> None:
    # Gross rents of 10000 and expenses of 12000: line 9369 is a loss of 2000.00, kept with its
    # sign through amounts 2 to 6 and line 9946 (T1 line 12600), and added to the 50000 of
    # employment income on line 15000.
    worksheet = return_ad(
        employment_income="50000",
        rental_properties=((1, "0", "10000"),),
        rental_expenses={"insurance": ("12000", "0", "0")},
    )

    assert t776_line(worksheet, GROSS_RENTAL_INCOME) == D("10000")
    assert t776_line(worksheet, RENTAL_NET_INCOME_BEFORE_ADJUSTMENTS) == D("-2000")
    assert t776_line(worksheet, RENTAL_NET_INCOME_AFTER_CCA) == D("-2000")
    assert worksheet.get(NET_RENTAL_INCOME).value == D("-2000.00")
    assert worksheet.get(TOTAL_INCOME).value == D("48000")
    rendered = render_flat(worksheet.trace)
    assert (
        "net_rental_income: rental_net_income_after_cca -2000, chosen as rental_partner is 0"
    ) in rendered


def test_a_rental_loss_with_no_other_income_is_a_negative_total_income() -> None:
    # Total income (line 15000) is not floored, as the form prints it: with no other income the
    # loss of 10000 - 12000 = -2000 on line 12600 is the whole of total income.
    worksheet = return_ad(
        rental_properties=((1, "0", "10000"),),
        rental_expenses={"insurance": ("12000", "0", "0")},
    )

    assert worksheet.get(NET_RENTAL_INCOME).value == D("-2000")
    assert worksheet.get(TOTAL_INCOME).value == D("-2000")


def test_a_co_owners_share_replaces_line_9369_on_amount_2_and_runs_through_amounts_3_to_6() -> None:
    # Line 2 is the co-owner's own 6000 of the 12000 (count 1); line 9945 takes 500 off (amount
    # 3 is 5500), line 9947 adds 200 (amount 4, 5700), line 9948 takes 100 off (amount 5, 5600)
    # and line 9936 takes 300 off (amount 6, 5300): line 9946 and T1 line 12600 are 5300.
    worksheet = return_ad(
        rental_coowner=1,
        rental_coowner_share="6000",
        rental_coowner_other_expenses="500",
        rental_coowner_recaptured_cca="200",
        rental_coowner_terminal_loss="100",
        rental_coowner_cca_claim="300",
    )

    assert t776_line(worksheet, RENTAL_NET_INCOME_BEFORE_ADJUSTMENTS) == D("12000")
    assert t776_line(worksheet, RENTAL_NET_INCOME_SHARE) == D("6000")
    assert t776_line(worksheet, RENTAL_NET_INCOME_AFTER_COOWNER_EXPENSES) == D("5500")
    assert t776_line(worksheet, RENTAL_NET_INCOME_WITH_RECAPTURE) == D("5700")
    assert t776_line(worksheet, RENTAL_NET_INCOME_AFTER_TERMINAL_LOSS) == D("5600")
    assert t776_line(worksheet, RENTAL_RECAPTURED_CCA) == D("200")
    assert t776_line(worksheet, RENTAL_TERMINAL_LOSS) == D("100")
    assert t776_line(worksheet, RENTAL_CCA_CLAIM) == D("300")
    assert t776_line(worksheet, RENTAL_NET_INCOME_AFTER_CCA) == D("5300")
    assert worksheet.get(NET_RENTAL_INCOME).value == D("5300")
    assert worksheet.get(TOTAL_INCOME).value == D("5300")
    rendered = render_flat(worksheet.trace)
    assert (
        "rental_net_income_share: rental_coowner_share 6000, chosen as rental_coowner is 1"
    ) in rendered


def test_a_sole_proprietor_ignores_the_co_owners_share_and_carries_line_9369() -> None:
    # The same figures with a count of 0: amount 2 is line 9369 (12000), so amount 3 is
    # 12000 - 500 = 11500; the entered share of 6000 and the co-owner's shares of lines 9947,
    # 9948 and 9936 (200, 100 and 300) are not used, and with no Area A classes those three lines
    # are 0, so amount 6 is 11500.
    worksheet = return_ad(
        rental_coowner=0,
        rental_coowner_share="6000",
        rental_coowner_other_expenses="500",
        rental_coowner_recaptured_cca="200",
        rental_coowner_terminal_loss="100",
        rental_coowner_cca_claim="300",
    )

    assert t776_line(worksheet, RENTAL_NET_INCOME_SHARE) == D("12000")
    assert t776_line(worksheet, RENTAL_RECAPTURED_CCA) == D("0")
    assert t776_line(worksheet, RENTAL_TERMINAL_LOSS) == D("0")
    assert t776_line(worksheet, RENTAL_CCA_CLAIM) == D("0")
    assert t776_line(worksheet, RENTAL_NET_INCOME_AFTER_CCA) == D("11500")
    assert worksheet.get(NET_RENTAL_INCOME).value == D("11500")


def test_a_partners_line_9946_is_amount_7_plus_line_9974_minus_line_9943() -> None:
    # Amount 7 is 4000 (the T5013 amount), line 9974 adds 50 and line 9943 takes 30 off:
    # 4000 + 50 - 30 = 4020, which replaces amount 6 (12000) on line 9946.
    worksheet = return_ad(
        rental_partner=1,
        rental_partner_share="4000",
        rental_partner_gst_hst_rebate="50",
        rental_partner_other_expenses="30",
    )

    assert t776_line(worksheet, RENTAL_NET_INCOME_AFTER_CCA) == D("12000")
    assert t776_line(worksheet, RENTAL_PARTNER_SHARE_WITH_REBATE) == D("4050")
    assert t776_line(worksheet, RENTAL_PARTNERSHIP_NET_INCOME) == D("4020")
    assert worksheet.get(NET_RENTAL_INCOME).value == D("4020")
    assert worksheet.get(TOTAL_INCOME).value == D("4020")
    rendered = render_flat(worksheet.trace)
    assert (
        "net_rental_income: rental_partnership_net_income 4020, chosen as rental_partner is 1"
    ) in rendered


def test_a_sole_proprietor_ignores_the_partners_figures() -> None:
    worksheet = return_ad(
        rental_partner=0,
        rental_partner_share="4000",
        rental_partner_gst_hst_rebate="50",
        rental_partner_other_expenses="30",
    )

    assert t776_line(worksheet, RENTAL_PARTNERSHIP_NET_INCOME) == D("4020")
    assert worksheet.get(NET_RENTAL_INCOME).value == D("12000")


def test_a_partners_loss_is_negative_on_line_9946() -> None:
    worksheet = return_ad(
        employment_income="50000",
        rental_partner=1,
        rental_partner_share="-1000",
        rental_partner_other_expenses="20",
    )

    assert t776_line(worksheet, RENTAL_PARTNERSHIP_NET_INCOME) == D("-1020")
    assert worksheet.get(NET_RENTAL_INCOME).value == D("-1020")
    assert worksheet.get(TOTAL_INCOME).value == D("48980")


def test_a_co_owners_loss_is_negative_on_amount_2() -> None:
    worksheet = return_ad(employment_income="50000", rental_coowner=1, rental_coowner_share="-3000")

    assert t776_line(worksheet, RENTAL_NET_INCOME_SHARE) == D("-3000")
    assert t776_line(worksheet, RENTAL_NET_INCOME_AFTER_CCA) == D("-3000")
    assert worksheet.get(NET_RENTAL_INCOME).value == D("-3000")


def test_a_chart_a_row_with_no_short_term_days_is_refused_naming_the_row() -> None:
    with pytest.raises(ValidationError, match="row 1: ca/short_term_rental_days cannot be 0"):
        return_ad(short_term_rental_units_rows=(("900", 0, 0),))


def test_a_negative_expense_box_is_refused() -> None:
    with pytest.raises(NegativeArtifactError):
        return_ad(rental_expenses={"insurance": ("-1", "0", "0")})
