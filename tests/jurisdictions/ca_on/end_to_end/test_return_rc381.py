"""CA-ON 2025 end to end: Form RC381 as a form of none or one copy."""

from __future__ import annotations

import pytest

from app.domain.errors import ValidationError
from app.jurisdictions.ca.catalog import (
    CPP_BASE_CONTRIBUTIONS_ON_RETURN,
    NET_INCOME,
    RC381_CPP_BASE_CONTRIBUTIONS_ON_RETURN,
    RC381_CPP_BASE_CONTRIBUTIONS_ON_SELF_EMPLOYMENT_AND_OTHER_EARNINGS,
    RC381_CPP_DEDUCTION_ON_SELF_EMPLOYMENT_AND_OTHER_EARNINGS,
    RC381_CPP_ENHANCED_CONTRIBUTIONS_ON_RETURN,
    RC381_CPP_OVERPAYMENT_ON_RETURN,
    RC381_CPP_PAYABLE_ON_SELF_EMPLOYMENT,
    TOTAL_INCOME,
)
from tests.jurisdictions.ca_on.end_to_end.support import D, run

LINES = (
    RC381_CPP_BASE_CONTRIBUTIONS_ON_RETURN,
    RC381_CPP_ENHANCED_CONTRIBUTIONS_ON_RETURN,
    RC381_CPP_OVERPAYMENT_ON_RETURN,
    RC381_CPP_PAYABLE_ON_SELF_EMPLOYMENT,
    RC381_CPP_BASE_CONTRIBUTIONS_ON_SELF_EMPLOYMENT_AND_OTHER_EARNINGS,
    RC381_CPP_DEDUCTION_ON_SELF_EMPLOYMENT_AND_OTHER_EARNINGS,
)


def test_a_return_with_no_rc381_gives_all_six_totals_0_and_no_form_worksheet() -> None:
    # Employment income of 60000 and a T4 box 16 total of 3361.75 would give a CPP overpayment on a
    # copy of Form RC381 (line 44800); with an empty list of copies the form does not run and each
    # total of its results is 0. The default is no copy of the form.
    result = run(
        "60000",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
        cpp_t4_base_and_first_additional_contributions="3361.75",
    )

    assert result["ca/rc381"] == ()
    (worksheet,) = result["ca-on/return"]
    for kind in LINES:
        assert worksheet.get(kind).value == D("0"), kind.identifier
    assert worksheet.get(TOTAL_INCOME).value == D("60000")


def test_a_return_with_one_rc381_totals_the_results_of_that_copy() -> None:
    result = run(
        "60000",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
        cpp_t4_base_and_first_additional_contributions="3361.75",
        schedule_8_copies=0,
        rc381_copies=1,
    )

    (rc381,) = result["ca/rc381"]
    (worksheet,) = result["ca-on/return"]
    assert rc381.get(RC381_CPP_OVERPAYMENT_ON_RETURN).value == D("3361.75")
    for kind in LINES:
        assert worksheet.get(kind).value == rc381.get(kind).value, kind.identifier


def test_the_t1_lines_are_still_schedule_8s_while_the_return_carries_form_rc381() -> None:
    # Until the T1 lines total both forms, a return that carries Form RC381 and no Schedule 8 has
    # no CPP contributions on the return, while a return that carries Schedule 8 has them.
    with_rc381 = run("60000", (), "0", "0", "0", "0", "0", schedule_8_copies=0, rc381_copies=1)
    with_schedule_8 = run("60000", (), "0", "0", "0", "0", "0")

    (rc381_return,) = with_rc381["ca-on/return"]
    (schedule_8_return,) = with_schedule_8["ca-on/return"]
    assert rc381_return.get(CPP_BASE_CONTRIBUTIONS_ON_RETURN).value == D("0")
    assert rc381_return.get(NET_INCOME).value == D("60000.00")
    assert schedule_8_return.get(CPP_BASE_CONTRIBUTIONS_ON_RETURN).value == D("2796.75")
    assert with_schedule_8["ca/rc381"] == ()


def test_a_second_rc381_is_refused_naming_the_form() -> None:
    with pytest.raises(ValidationError, match="ca/rc381"):
        run("60000", (), "0", "0", "0", "0", "0", schedule_8_copies=0, rc381_copies=2)


def test_schedule_8_and_form_rc381_together_are_refused_by_the_exclusive_group() -> None:
    with pytest.raises(ValidationError, match="ca/cpp_calculation"):
        run("60000", (), "0", "0", "0", "0", "0", schedule_8_copies=1, rc381_copies=1)
