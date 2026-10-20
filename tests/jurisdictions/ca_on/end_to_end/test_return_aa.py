"""CA-ON 2025 end to end: return aa."""

from __future__ import annotations

from typing import Any

from app.domain.worksheet import Worksheet
from app.jurisdictions.ca.catalog import (
    NET_INCOME,
    REFUND_OR_BALANCE_OWING,
    TOTAL_CREDITS,
    TOTAL_PAYABLE,
)
from app.jurisdictions.ca_on import catalog as ontario
from app.jurisdictions.ca_on.catalog import (
    LIFT_CREDIT,
    ONTARIO_TAX,
    ONTARIO_TAX_AFTER_LIFT_CREDIT,
    ONTARIO_TAX_AFTER_REDUCTION,
)
from tests.jurisdictions.ca_on.end_to_end.support import D, compute


def return_aa(**overrides: Any) -> Worksheet:
    """Return AA's inputs (`returns/2025_return_aa.yaml`): a filer with a spouse at year end.

    `overrides` replace any keyword of `compute`, for the variants below.
    """
    given: dict[str, Any] = {
        "income_tax_deducted": "2500",
        "spouse_net_income": "50000",
        "lift_spouse_at_year_end": 1,
        "spouse_net_income_before_adjustments": "50000",
    }
    return compute("25217.17", "0", "0", "0", "4500", "0", "0", **{**given, **overrides})


def test_return_aas_lift_credit_is_375_from_part_b_and_comes_off_the_ontario_tax() -> None:
    # Return AA: employment income of 25217.17 (net income 25000.00 after the first additional
    # CPP contribution of 217.17), a spouse at the end of the year with a net income of 50000.
    # Schedule ON428-A line 41 is 875 - 5% of (75000.00 - 65000.00) = 875 - 500.00 = 375.00.
    # The Ontario tax on 25000.00 is 1262.50 less the credits 5.05% x (12747 + 1075.00 + 413.56 =
    # 14235.56) = 718.90, 543.60; the tax reduction is 588.00 - 543.60 = 44.40, so line 81 is
    # 499.20 and line 86 is 499.20 - 375.00 = 124.20. With the health premium of 300 the Ontario
    # tax is 424.20; the federal tax after credits is 3625.00 - 2767.84 = 857.16, so the total
    # payable is 857.16 + 424.20 = 1281.36 and, with the chosen tax deducted of 2500 and the
    # Canada workers benefit of 1633.00 (no eligible spouse is modelled), line 167 is 1281.36 -
    # 4133.00 = -2851.64, a refund.
    worksheet = return_aa()

    assert worksheet.get(NET_INCOME).value == D("25000.00")
    assert worksheet.get(ontario.LIFT_ADJUSTED_NET_INCOME).value == D("25000.00")
    assert worksheet.get(ontario.LIFT_SPOUSE_ADJUSTED_NET_INCOME).value == D("50000")
    assert worksheet.get(ontario.LIFT_FAMILY_NET_INCOME).value == D("75000.00")
    assert worksheet.get(ontario.LIFT_CREDIT_SINGLE).value == D("875")
    assert worksheet.get(ontario.LIFT_CREDIT_WITH_SPOUSE).value == D("375.00")
    assert worksheet.get(LIFT_CREDIT).value == D("375.00")
    assert worksheet.get(ONTARIO_TAX_AFTER_REDUCTION).value == D("499.20")
    assert worksheet.get(ONTARIO_TAX_AFTER_LIFT_CREDIT).value == D("124.20")
    assert worksheet.get(ONTARIO_TAX).value == D("424.20")
    assert worksheet.get(TOTAL_PAYABLE).value == D("1281.36")
    assert worksheet.get(TOTAL_CREDITS).value == D("4133.00")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-2851.64")


def test_return_aa_without_the_spouse_at_year_end_takes_the_whole_875() -> None:
    # The same return with a count of 0 (single, or the spouse died during the year): Part A's
    # line 20 is 875 - 0 = 875, so line 86 is 499.20 - 875, below zero, 0, and the Ontario tax is
    # the health premium of 300 alone.
    worksheet = return_aa(lift_spouse_at_year_end=0)

    assert worksheet.get(LIFT_CREDIT).value == D("875")
    assert worksheet.get(ONTARIO_TAX_AFTER_LIFT_CREDIT).value == D("0")
    assert worksheet.get(ONTARIO_TAX).value == D("300")
