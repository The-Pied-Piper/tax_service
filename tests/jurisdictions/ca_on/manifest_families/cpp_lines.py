"""The CA-ON manifest entries of one family of lines (see `test_manifest.py`).

The T1 lines for CPP that both forms give (`05j_cpp_lines.yaml`): the return carries Schedule 8 or
Form RC381, never both, so one of the two totals is 0 and each of lines 30800 (also ON428 line
58240), 22215 and 44800 is the Schedule 8 total plus the Form RC381 total. Lines 42100, 31000 and
22200 add the Form RC381 total to the sums of Part 4 and Part 5 that `net_tax.py`,
`non_refundable_credits.py` and `deductions.py` hold.
"""

from __future__ import annotations

from app.domain.capabilities.sum import Sum
from app.domain.manifest import CapabilitySelection
from app.jurisdictions.ca.catalog import (
    CPP_BASE_CONTRIBUTIONS_ON_RETURN,
    CPP_ENHANCED_CONTRIBUTIONS_ON_RETURN,
    CPP_OVERPAYMENT,
    RC381_CPP_BASE_CONTRIBUTIONS_ON_RETURN,
    RC381_CPP_ENHANCED_CONTRIBUTIONS_ON_RETURN,
    RC381_CPP_OVERPAYMENT_ON_RETURN,
    SCHEDULE_8_CPP_BASE_CONTRIBUTIONS_ON_RETURN,
    SCHEDULE_8_CPP_ENHANCED_CONTRIBUTIONS_ON_RETURN,
    SCHEDULE_8_CPP_OVERPAYMENT,
)

INPUTS = frozenset[str]()

OUTPUTS = frozenset[str]()

STEPS = {
    # T1 line 30800 and ON428 line 58240: Schedule 8 line 57 or Form RC381 line 98 (or Part 3a
    # line 70, Part 3b line 81), whichever form the return carries.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/schedule_8_cpp_base_contributions_on_return",
                "ca/rc381_cpp_base_contributions_on_return",
            )
        },
        produces={"output": "ca/cpp_base_contributions_on_return"},
    ),
    # T1 line 22215: Schedule 8 line 69 or Form RC381 line 110, whichever form the return carries.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/schedule_8_cpp_enhanced_contributions_on_return",
                "ca/rc381_cpp_enhanced_contributions_on_return",
            )
        },
        produces={"output": "ca/cpp_enhanced_contributions_on_return"},
    ),
    # T1 line 44800: Schedule 8 line 50 or Form RC381 line 91 (or Part 3a line 29, line 74),
    # whichever form the return carries.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/schedule_8_cpp_overpayment",
                "ca/rc381_cpp_overpayment_on_return",
            )
        },
        produces={"output": "ca/cpp_overpayment"},
    ),
}

WIRING = {
    (
        Sum,
        frozenset(
            {SCHEDULE_8_CPP_BASE_CONTRIBUTIONS_ON_RETURN, RC381_CPP_BASE_CONTRIBUTIONS_ON_RETURN}
        ),
        frozenset({CPP_BASE_CONTRIBUTIONS_ON_RETURN}),
    ),
    (
        Sum,
        frozenset(
            {
                SCHEDULE_8_CPP_ENHANCED_CONTRIBUTIONS_ON_RETURN,
                RC381_CPP_ENHANCED_CONTRIBUTIONS_ON_RETURN,
            }
        ),
        frozenset({CPP_ENHANCED_CONTRIBUTIONS_ON_RETURN}),
    ),
    (
        Sum,
        frozenset({SCHEDULE_8_CPP_OVERPAYMENT, RC381_CPP_OVERPAYMENT_ON_RETURN}),
        frozenset({CPP_OVERPAYMENT}),
    ),
}
