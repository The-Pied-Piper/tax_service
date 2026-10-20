"""CA-ON 2025 end to end: return ab."""

from __future__ import annotations

from typing import Any

from app.adapters.inbound.trace_english import EnglishTraceRenderer
from app.domain.parameters.amount import Amount
from app.domain.record_list import RecordList
from app.domain.trace import (
    DisabilityTransferLine,
    ItemsTotalLine,
)
from app.domain.worksheet import Worksheet
from app.jurisdictions.ca.capabilities.disability_transfer_amount import DisabilityTransferAmount
from app.jurisdictions.ca.catalog import (
    CANADA_WORKERS_BENEFIT,
    CAREGIVER_AMOUNT,
    DEPENDANT_CARE_EXPENSES,
    DEPENDANT_CREDIT_AMOUNTS,
    DEPENDANT_TAXABLE_INCOME,
    DEPENDANT_UNDER_18,
    DISABILITY_DEPENDANTS,
    DISABILITY_TRANSFERRED_AMOUNT,
    FEDERAL_TAX_AFTER_CREDITS,
    MEDICAL_CLAIM,
    MEDICAL_EXPENSES_OVER_THRESHOLD,
    MEDICAL_THRESHOLD,
    NET_INCOME,
    NON_REFUNDABLE_CREDIT_AMOUNTS,
    NON_REFUNDABLE_TAX_CREDITS,
    OTHER_DEPENDANTS_MEDICAL,
    REFUND_OR_BALANCE_OWING,
    TOTAL_PAYABLE,
)
from app.jurisdictions.ca_on import catalog as ontario
from app.jurisdictions.ca_on.catalog import (
    ONTARIO_TAX,
)
from tests.jurisdictions.ca_on.end_to_end.support import CENT, D, compute, return_w


def return_ab(**overrides: Any) -> Worksheet:
    """Return AB's inputs (`returns/2025_return_ab.yaml`): Return W's and a dependant aged 20.

    `overrides` replace any keyword of `return_w`, for the variants below.
    """
    given: dict[str, Any] = {"disability_dependants": ((0, "0", "16129", "20000"),)}
    return return_w(**{**given, **overrides})


def test_return_abs_dependant_with_a_disability_transfers_6267_on_line_31800() -> None:
    # Return AB is Return W (employment income of 48000, taxable income 47555.00, federal tax on
    # it 6895.48, the Ontario figures of Return W, the Canada caregiver amount for two infirm
    # dependants 12399.00) with one dependant with a disability, aged 20 (so worksheet line 7 is
    # "0"), no care expenses, line 98 of their return 16129 and their taxable income 20000, all
    # chosen figures. Federal Worksheet line 31800: line 8 = 10138.00 + 0; line 10 = 10138.00 +
    # 16129 = 26267.00; line 12 = 26267.00 - 20000 = 6267.00; line 13 = lesser(10138.00,
    # 6267.00) = 6267.00, the total of the allowable amounts. The federal credit amounts are
    # 16129 + 0 + 0 + 0 + 0 + 12399.00 + 0 + 2202.75 + 787.20 + 1471 + 6267.00 = 39255.95; 14.5%
    # of it is 5692.11275, rounded half-up to the cent: 5692.11, so the federal tax after
    # credits is 6895.48 - 5692.11 = 1203.37. The Ontario total of credit amounts is Return W's,
    # 23306.95 (the Ontario disability amount, ON428 line 58480, is not yet computed), so the
    # Ontario tax is 1302.28. The total payable is 1203.37 + 1302.28 = 2505.65, and with the
    # chosen tax deducted of 4800 and no Canada workers benefit, line 167 is 2505.65 - 4800 =
    # -2294.35, a refund.
    worksheet = return_ab()

    assert worksheet.get(DISABILITY_DEPENDANTS).value == RecordList(
        DISABILITY_DEPENDANTS.fields,
        [
            {
                DEPENDANT_UNDER_18: 0,
                DEPENDANT_CARE_EXPENSES: D("0"),
                DEPENDANT_CREDIT_AMOUNTS: D("16129"),
                DEPENDANT_TAXABLE_INCOME: D("20000"),
            }
        ],
    )
    assert worksheet.producer_of(DISABILITY_DEPENDANTS) is None
    assert isinstance(
        worksheet.producer_of(DISABILITY_TRANSFERRED_AMOUNT), DisabilityTransferAmount
    )
    assert worksheet.get(DISABILITY_TRANSFERRED_AMOUNT).value == D("6267.00")
    assert worksheet.get(CAREGIVER_AMOUNT).value == D("12399.00")
    assert worksheet.get(NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("39255.95")
    assert worksheet.get(NON_REFUNDABLE_TAX_CREDITS).value == D("5692.11")
    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("1203.37")
    assert worksheet.get(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("23306.95")
    assert worksheet.get(ONTARIO_TAX).value == D("1302.28")
    assert worksheet.get(TOTAL_PAYABLE).value == D("2505.65")
    assert worksheet.get(CANADA_WORKERS_BENEFIT).value == D("0")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-2294.35")


def test_return_abs_trace_names_the_dependant_and_totals_the_credit_amounts() -> None:
    worksheet = return_ab()

    lines = [
        line
        for line in worksheet.trace
        if isinstance(line, DisabilityTransferLine | ItemsTotalLine)
        and line.output == DISABILITY_TRANSFERRED_AMOUNT
    ]
    assert lines == [
        DisabilityTransferLine(
            output=DISABILITY_TRANSFERRED_AMOUNT,
            position=1,
            base=Amount(D("10138.00")),
            supplement=Amount(D("5914.00")),
            threshold=Amount(D("3464.00")),
            maximum=Amount(D("16052")),
            under_18=0,
            care_expenses=D("0"),
            line_5=D("0"),
            line_6=D("5914.00"),
            line_7=D("0"),
            line_8=D("10138.00"),
            credit_amounts=D("16129"),
            line_10=D("26267.00"),
            taxable_income=D("20000"),
            line_12=D("6267.00"),
            rounding=CENT,
            result=D("6267.00"),
        ),
        ItemsTotalLine(
            output=DISABILITY_TRANSFERRED_AMOUNT,
            items=((1, D("6267.00")),),
            total=D("6267.00"),
        ),
    ]
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    first = rendered.index(
        "disability_transferred_amount: dependant 1: 18 or older: base 10138 + 0, at most 16052 "
        "= 10138; 10138 + credit amounts 16129 less taxable income 20000 = 6267; "
        "the lesser of 10138 and 6267 = 6267 (half-up to 0.01)"
    )
    assert rendered[first : first + 2] == (
        "disability_transferred_amount: dependant 1: 18 or older: base 10138 + 0, at most 16052 "
        "= 10138; 10138 + credit amounts 16129 less taxable income 20000 = 6267; "
        "the lesser of 10138 and 6267 = 6267 (half-up to 0.01)",
        "disability_transferred_amount: item 1 6267 = 6267",
    )
    assert (
        "non_refundable_credit_amounts: basic_personal_amount 16129 + age_amount 0 "
        "+ spouse_amount 0 + eligible_dependant_amount 0 + spouse_caregiver_amount 0 "
        "+ caregiver_amount 12399 + infirm_children_amount 0 + cpp_base_contributions 2202.75 "
        "+ ei_premiums 787.2 + canada_employment_amount 1471 + disability_transferred_amount 6267 "
        "+ medical_claim 0 "
        "= 39255.95"
    ) in rendered


def test_a_dependant_under_18_with_care_expenses_transfers_the_reduced_supplement() -> None:
    # Care expenses of 5000: line 5 = 5000 - 3464.00 = 1536.00; line 6 = 5914.00 - 1536.00 =
    # 4378.00; line 7 = line 6; line 8 = 10138.00 + 4378.00 = 14516.00; with no credit amounts
    # and no taxable income line 12 = 14516.00, and line 13 is 14516.00.
    worksheet = compute(
        "48000", "0", "0", "0", "8640", "0", "0", disability_dependants=((1, "5000", "0", "0"),)
    )

    assert worksheet.get(DISABILITY_TRANSFERRED_AMOUNT).value == D("14516.00")
    assert worksheet.get(NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("35105.95")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "disability_transferred_amount: dependant 1: under 18: care expenses 5000 less threshold "
        "3464 = 1536; supplement 5914 less 1536 = 4378; base 10138 + 4378, at most 16052 = 14516; "
        "14516 + credit amounts 0 less taxable income 0 = 14516; "
        "the lesser of 14516 and 14516 = 14516 (half-up to 0.01)"
    ) in rendered


def test_two_dependants_with_a_disability_are_transferred_one_by_one_on_line_31800() -> None:
    worksheet = compute(
        "48000",
        "0",
        "0",
        "0",
        "8640",
        "0",
        "0",
        disability_dependants=((0, "0", "16129", "20000"), (1, "5000", "0", "0")),
    )

    # 6267.00 + 14516.00 = 20783.00.
    assert worksheet.get(DISABILITY_TRANSFERRED_AMOUNT).value == D("20783.00")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert "disability_transferred_amount: item 1 6267 + item 2 14516 = 20783" in rendered


def test_a_dependants_taxable_income_above_their_credits_transfers_nothing() -> None:
    # Line 10 = 10138.00 + 0; line 12 = 10138.00 - 20000 is negative, "0".
    worksheet = compute(
        "48000", "0", "0", "0", "8640", "0", "0", disability_dependants=((0, "0", "0", "20000"),)
    )

    assert worksheet.get(DISABILITY_TRANSFERRED_AMOUNT).value == D("0")
    assert worksheet.get(NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("20589.95")


def test_no_dependants_with_a_disability_transfer_nothing_on_line_31800() -> None:
    worksheet = compute("48000", "0", "0", "0", "8640", "0", "0")

    assert worksheet.get(DISABILITY_TRANSFERRED_AMOUNT).value == D("0")
    assert worksheet.get(NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("20589.95")


def test_dependants_with_a_disability_do_not_change_the_ontario_credits() -> None:
    # ON428 line 58480 (the Ontario disability amount transferred from a dependant) is not yet
    # computed.
    without = return_w()
    with_dependants = return_ab()

    assert with_dependants.get(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS) == (
        without.get(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS)
    )
    assert with_dependants.get(ONTARIO_TAX) == without.get(ONTARIO_TAX)


def test_ontarios_ceiling_is_2885_not_the_federal_2834() -> None:
    # Employment income of 96000 gives a net income of 94926.00, and 3% of it is 2847.78: above
    # the federal ceiling of 2834 and below Ontario's 2885, so line 109 is 2834 and ON428 line
    # 40 is 2847.78.
    worksheet = compute("96000", "0", "0", "0", "0", "0", "0", medical_expenses="5000")

    assert worksheet.get(NET_INCOME).value == D("94926.00")
    assert worksheet.get(MEDICAL_THRESHOLD).value == D("2834")
    assert worksheet.get(ontario.MEDICAL_THRESHOLD).value == D("2847.78")
    assert worksheet.get(MEDICAL_EXPENSES_OVER_THRESHOLD).value == D("2166")
    assert worksheet.get(ontario.MEDICAL_EXPENSES_OVER_THRESHOLD).value == D("2152.22")


def test_ontarios_threshold_on_line_40_stops_at_2885() -> None:
    worksheet = compute("115000", "0", "0", "0", "0", "0", "0", medical_expenses="5000")

    assert worksheet.get(ontario.MEDICAL_NET_INCOME_SHARE).value > D("2885")
    assert worksheet.get(ontario.MEDICAL_THRESHOLD).value == D("2885")
    assert worksheet.get(ontario.MEDICAL_EXPENSES_OVER_THRESHOLD).value == D("2115")


def test_ontario_caps_each_dependants_claim_at_15551_and_the_t1_does_not() -> None:
    # A dependant with no net income and expenses of 20000: the Federal Worksheet's line 3 is the
    # whole 20000, Worksheet ON428's line 3 is at most 15551.
    worksheet = compute(
        "48000", "0", "0", "0", "8640", "0", "0", other_dependants=(("20000", "0"),)
    )

    assert worksheet.get(OTHER_DEPENDANTS_MEDICAL).value == D("20000.00")
    assert worksheet.get(ontario.OTHER_DEPENDANTS_MEDICAL).value == D("15551.00")
    assert worksheet.get(ontario.MEDICAL_CLAIM).value == D("15551.00")
    assert worksheet.get(MEDICAL_CLAIM).value == D("20000.00")


def test_ontario_pooled_dependants_would_give_the_wrong_line_58729() -> None:
    separate = compute(
        "48000",
        "0",
        "0",
        "0",
        "8640",
        "0",
        "0",
        other_dependants=(("3000", "10000"), ("1000", "40000")),
    )
    pooled = compute(
        "48000", "0", "0", "0", "8640", "0", "0", other_dependants=(("4000", "50000"),)
    )

    assert separate.get(ontario.OTHER_DEPENDANTS_MEDICAL).value == D("2700.00")
    # 4000 - lesser(1500.00, 2885) = 2500.00, not 2700.00.
    assert pooled.get(ontario.OTHER_DEPENDANTS_MEDICAL).value == D("2500.00")


def test_no_medical_expenses_claim_nothing_on_line_58769() -> None:
    worksheet = compute("48000", "0", "0", "0", "8640", "0", "0")

    assert worksheet.get(ontario.MEDICAL_EXPENSES_OVER_THRESHOLD).value == D("0")
    assert worksheet.get(ontario.OTHER_DEPENDANTS_MEDICAL).value == D("0")
    assert worksheet.get(ontario.MEDICAL_CLAIM).value == D("0")
    assert worksheet.get(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("15736.95")
