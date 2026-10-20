"""The CA-ON manifest entries of one family of lines (see `test_manifest.py`)."""

from __future__ import annotations

from app.domain.capabilities.sum import Sum
from app.domain.capabilities.times_count import TimesCount
from app.domain.manifest import CapabilitySelection
from app.jurisdictions.ca.catalog import (
    ADVANCED_CANADA_WORKERS_BENEFIT,
    CPP_PART_4_COMPLETED,
    CPP_PAYABLE_ON_SELF_EMPLOYMENT,
    EI_PAYABLE_ON_SELF_EMPLOYMENT,
    EI_SPECIAL_BENEFITS_AGREEMENT,
    FEDERAL_TAX_LESS_CREDITS,
    NET_FEDERAL_TAX,
    RESP_AIPS_ADDITIONAL_TAX,
    RL_10_LABOUR_SPONSORED_FUND_AMOUNT,
    SELF_EMPLOYED_CPP_CONTRIBUTIONS_PAYABLE,
    SELF_EMPLOYED_EI_PREMIUMS,
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
    # T1 line 144 and line 42100, entered from Schedule 8 Part 4 line 14: Part 4 is completed
    # only when the filer reports self-employment income alone, so the amount is counted once
    # for each Part 4 completed, 1 or 0.
    CapabilitySelection(
        name="core/times_count",
        params={},
        consumes={
            "amount": "ca/self_employed_cpp_contributions_payable",
            "count": "ca/cpp_part_4_completed",
        },
        produces={"output": "ca/cpp_payable_on_self_employment"},
    ),
    # T1 line 145 and line 42120, entered from Schedule 13 line 9, counted once for each
    # agreement with the Canada Employment Insurance Commission, 1 or 0.
    CapabilitySelection(
        name="core/times_count",
        params={},
        consumes={
            "amount": "ca/self_employed_ei_premiums",
            "count": "ca/ei_special_benefits_agreement",
        },
        produces={"output": "ca/ei_payable_on_self_employment"},
    ),
    # T1 line 148 (line 43500) "Add lines 143 to 147. Total payable": line 143 "Amount from line
    # 42000", line 144 (42100) "CPP contributions payable on self-employment income and other
    # earnings", line 145 (42120) "Employment insurance premiums payable on self-employment and
    # other eligible earnings" and line 147 (42800), the Ontario tax, in line order; line 146
    # (42200), the social benefits repayment, is not yet computed.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/net_federal_tax",
                "ca/cpp_payable_on_self_employment",
                "ca/ei_payable_on_self_employment",
                "ca-on/ontario_tax",
            )
        },
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
    (
        TimesCount,
        frozenset({SELF_EMPLOYED_CPP_CONTRIBUTIONS_PAYABLE, CPP_PART_4_COMPLETED}),
        frozenset({CPP_PAYABLE_ON_SELF_EMPLOYMENT}),
    ),
    (
        TimesCount,
        frozenset({SELF_EMPLOYED_EI_PREMIUMS, EI_SPECIAL_BENEFITS_AGREEMENT}),
        frozenset({EI_PAYABLE_ON_SELF_EMPLOYMENT}),
    ),
    (
        Sum,
        frozenset(
            {
                NET_FEDERAL_TAX,
                CPP_PAYABLE_ON_SELF_EMPLOYMENT,
                EI_PAYABLE_ON_SELF_EMPLOYMENT,
                ONTARIO_TAX,
            }
        ),
        frozenset({TOTAL_PAYABLE}),
    ),
}
