"""CA-ON 2025 end to end: return ct."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import pytest

from app.adapters.inbound.trace_english import EnglishTraceRenderer
from app.domain.errors import InvalidRecordError
from app.domain.worksheet import Worksheet
from app.jurisdictions.ca.catalog import (
    CCA_CLASS_NUMBER,
    CCA_UCC_AT_END,
    FARM_CCA_CLAIM,
    FARM_CCA_TABLE_CLAIM,
    FARM_CLOSING_UCC,
    FARM_RECAPTURED_CCA,
    FARM_TERMINAL_LOSS,
)
from tests.jurisdictions.ca_on.end_to_end.support import D, run

# Return CF's T2042, Return BC's with the wheat raised by 2200.68 to 52200.68 (a chosen figure, so
# that line 9946 stays Return BC's 30000): income lines of 82200.68 (wheat 52200.68 on line 9371,
# cattle 30000 on line 9471) and expenses of 50000 (fertilizers and lime 20000 on line 9662, seeds
# and plants 30000 on line 9664), with no inventory adjustment or partner. The farm started on
# August 1, 2025, so its first fiscal period, August 1 to December 31, 2025, is 153 days (Guide
# T4002, "You were asking?", which has 214 days for a start on June 1).
FARM = {
    "wheat": "52200.68",
    "cattle": "30000",
    "fertilizers_and_lime": "20000",
    "seeds_and_plants": "30000",
    # Charts A to C for one leased passenger vehicle that is used for no farming: business
    # kilometres 0 (amount 1), so line 9819 (amount 16 of Chart A) is 0, as in Return BC.
    "vehicle_sales_tax_rate": "13",
}
DAYS = 153
# Charts A to C for one leased passenger vehicle used for no farming, as in Return BC.
VEHICLE = {
    "business_kilometres": "0",
    "total_kilometres": "10000",
    "fuel_and_oil": "1000",
    "insurance": "600",
    "maintenance_and_repairs": "200",
    "other_expenses_10": "653",
    "interest_payable": "400",
    "interest_days": "183",
    "lease_charges": "2550",
    "lease_days": "183",
    "list_price": "60000",
}


def class_row(
    personal_part: str = "5000.00", claim: str = "2200.68"
) -> tuple[str, str, str, str, str, str, str, int, str, str, str, str]:
    """Area A row as (column 1, column 2, column 3, column 5, column 11, column 12, the claim, no
    property left, column 4, column 6, column 9, endnote 9's remaining personal part): Return
    CF's Class 10 bought in the year (column 3 35000, nothing at the start), so column 7 is
    35000.00, with the given remaining personal part of the property's cost."""
    return ("10", "0", "35000", "0", "0", "0", claim, 0, "0", "0", "0", personal_part)


def run_ct(
    changes: Mapping[str, Any] | None = None, personal_part: str = "5000.00", **overrides: Any
) -> dict[str, tuple[Worksheet, ...]]:
    """Return CT's inputs, as in `returns/2025_return_ct.yaml`: Return CF's T2042 with a
    remaining personal part of 5000.00 on its one class (endnote 9)."""
    statement: dict[str, Any] = {
        "farm": FARM,
        "farm_cca_classes_rows": (class_row(personal_part),),
        "farm_vehicles_rows": (VEHICLE,),
        "farm_fiscal_period_days_entered": DAYS,
    }
    return run(
        "0",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
        farm_statements=({**statement, **(changes or {})},),
        **overrides,
    )


def statement_ct(
    changes: Mapping[str, Any] | None = None, personal_part: str = "5000.00"
) -> Worksheet:
    """The worksheet of Return CT's one T2042 statement: its lines, as the form computes them."""
    return run_ct(changes, personal_part)["ca/t2042"][0]


def closing(statement: Worksheet) -> list[tuple[Any, Any]]:
    records = statement.get(FARM_CLOSING_UCC).value.records
    return [(record[CCA_CLASS_NUMBER], record[CCA_UCC_AT_END]) for record in records]


def test_return_cts_class_10_closes_at_27799_32_after_the_remaining_personal_part() -> None:
    # Column 22 is column 7 less column 21 (35000.00 - 2200.68 = 32799.32), less the remaining
    # personal part of the property's cost (endnote 9): 32799.32 - 5000.00 = 27799.32.
    statement = statement_ct()

    assert closing(statement) == [(D("10"), D("27799.32"))]


def test_return_cts_trace_names_the_remaining_personal_part() -> None:
    rendered = EnglishTraceRenderer().render_all(statement_ct().trace)

    assert (
        "farm_closing_ucc: item 1 class 10: column 7 35000 less claim 2200.68 "
        "(prorated 153/365) less personal part 5000 = 27799.32"
    ) in rendered


def test_return_cts_personal_part_does_not_change_the_claim_or_the_form_lines() -> None:
    # Endnote 9 changes only column 22: the claim (column 21), the recapture, the terminal loss
    # and the income lines are Return CF's.
    with_part = statement_ct()
    without = statement_ct(personal_part="0")

    assert with_part.get(FARM_CCA_TABLE_CLAIM).value == D("2200.68")
    assert with_part.get(FARM_CCA_CLAIM).value == without.get(FARM_CCA_CLAIM).value
    assert with_part.get(FARM_RECAPTURED_CCA).value == D("0")
    assert with_part.get(FARM_TERMINAL_LOSS).value == D("0")
    assert closing(without) == [(D("10"), D("32799.32"))]


def test_a_remaining_personal_part_above_column_7_less_the_claim_is_refused() -> None:
    # 32799.32 is column 7 less the claim, so a part of 32799.33 is refused.
    with pytest.raises(InvalidRecordError, match="item 1: personal part"):
        statement_ct(personal_part="32799.33")
