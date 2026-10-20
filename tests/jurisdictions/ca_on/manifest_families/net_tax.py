"""The CA-ON manifest entries of one family of lines (see `test_manifest.py`)."""

from __future__ import annotations

from app.domain.capabilities.sum import Sum
from app.domain.manifest import CapabilitySelection
from app.jurisdictions.ca.catalog import (
    ADVANCED_CANADA_WORKERS_BENEFIT,
    FEDERAL_TAX_LESS_CREDITS,
    NET_FEDERAL_TAX,
    RESP_AIPS_ADDITIONAL_TAX,
    RL_10_LABOUR_SPONSORED_FUND_AMOUNT,
    SPECIAL_TAXES,
    TOTAL_PAYABLE,
)
from app.jurisdictions.ca_on.catalog import ONTARIO_TAX

INPUTS = frozenset(
    {
        "ca/income_tax_deducted",
    }
)

OUTPUTS = frozenset[str]()

STEPS = {
    # T1 line 141 and line 41800 "Special taxes": the amount of Form T1172 (line 10 or 13) and
    # the RL-10 amount, the guide's "Report, on line 41800 of your return, the result of the
    # following calculation using your RL-10 slip: Tax Credit for a Labour-Sponsored Fund" whose
    # list the guide's .txt cuts off after "75% of box", so the amount is the caller's until the
    # rest is quoted (to be confirmed). The tax on excess EPSP amounts (Form RC359 line 9, per
    # employer) is not yet wired.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": ("ca/resp_aips_additional_tax", "ca/rl_10_labour_sponsored_fund_amount")
        },
        produces={"output": "ca/special_taxes"},
    ),
    # T1 line 142 (line 42000) "Add lines 139 to 141. Net federal tax": line 139 (41700), line
    # 140 (41500) "Advanced Canada workers benefit (ACWB) (complete Schedule 6)", the RC210 box
    # 10 amount the guide says to report, the caller's, and line 141 (41800), in line order.
    # Lines 120 and 124 (tax on split income, minimum tax carryover) are not modelled.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/federal_tax_less_credits",
                "ca/advanced_canada_workers_benefit",
                "ca/special_taxes",
            )
        },
        produces={"output": "ca/net_federal_tax"},
    ),
    # T1 line 148 (line 43500) "Add lines 143 to 147. Total payable": line 143 "Amount from
    # line 42000" and line 147 (42800), the Ontario tax, in line order; lines 144 to 146 are
    # not triggered.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/net_federal_tax", "ca-on/ontario_tax")},
        produces={"output": "ca/total_payable"},
    ),
}

WIRING = {
    (
        Sum,
        frozenset({RESP_AIPS_ADDITIONAL_TAX, RL_10_LABOUR_SPONSORED_FUND_AMOUNT}),
        frozenset({SPECIAL_TAXES}),
    ),
    (
        Sum,
        frozenset({FEDERAL_TAX_LESS_CREDITS, ADVANCED_CANADA_WORKERS_BENEFIT, SPECIAL_TAXES}),
        frozenset({NET_FEDERAL_TAX}),
    ),
    (Sum, frozenset({NET_FEDERAL_TAX, ONTARIO_TAX}), frozenset({TOTAL_PAYABLE})),
}
