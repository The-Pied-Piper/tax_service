"""CA-ON 2025 end to end: Schedule 8 as a form of none or one copy."""

from __future__ import annotations

import pytest

from app.domain.errors import ValidationError
from app.jurisdictions.ca.catalog import (
    CPP_BASE_CONTRIBUTIONS_ON_RETURN,
    CPP_ENHANCED_CONTRIBUTIONS_ON_RETURN,
    CPP_OVERPAYMENT,
    CPP_PART_5_LINE_49,
    CPP_PART_5_LINE_70,
    CPP_PART_5_LINE_88,
    CPP_ZERO,
    NET_INCOME,
    TOTAL_INCOME,
)
from tests.jurisdictions.ca_on.end_to_end.support import D, run

LINES = (
    CPP_BASE_CONTRIBUTIONS_ON_RETURN,
    CPP_ENHANCED_CONTRIBUTIONS_ON_RETURN,
    CPP_OVERPAYMENT,
    CPP_PART_5_LINE_49,
    CPP_PART_5_LINE_70,
    CPP_PART_5_LINE_88,
    CPP_ZERO,
)


def test_a_return_with_no_schedule_8_gives_all_seven_totals_0_and_no_form_worksheet() -> None:
    # Employment income of 60000 would give base contributions of 2796.75 and enhanced ones of
    # 565.00 on a copy of Schedule 8; with an empty list of copies the form does not run, each
    # total of its lines is 0, and the enhanced contributions are no deduction from total income.
    result = run("60000", (), "0", "0", "0", "0", "0", schedule_8_copies=0)

    assert result["ca/schedule_8"] == ()
    (worksheet,) = result["ca-on/return"]
    for kind in LINES:
        assert worksheet.get(kind).value == D("0"), kind.identifier
    assert worksheet.get(TOTAL_INCOME).value == D("60000")
    assert worksheet.get(NET_INCOME).value == D("60000.00")


def test_a_return_with_one_schedule_8_totals_the_lines_of_that_copy() -> None:
    result = run("60000", (), "0", "0", "0", "0", "0", schedule_8_copies=1)

    (schedule_8,) = result["ca/schedule_8"]
    (worksheet,) = result["ca-on/return"]
    assert worksheet.get(CPP_BASE_CONTRIBUTIONS_ON_RETURN).value == D("2796.75")
    assert worksheet.get(CPP_ENHANCED_CONTRIBUTIONS_ON_RETURN).value == D("565.00")
    for kind in LINES:
        assert worksheet.get(kind).value == schedule_8.get(kind).value, kind.identifier
    assert worksheet.get(NET_INCOME).value == D("59435.00")


def test_a_second_schedule_8_is_refused_naming_the_form() -> None:
    with pytest.raises(ValidationError, match="ca/schedule_8"):
        run("60000", (), "0", "0", "0", "0", "0", schedule_8_copies=2)
