"""The CA-ON manifest entries of one family of lines (see `test_manifest.py`)."""

from __future__ import annotations

from app.domain.capabilities.subtract import Subtract
from app.domain.capabilities.subtract_not_below_zero import SubtractNotBelowZero
from app.domain.capabilities.sum import Sum
from app.domain.manifest import CapabilitySelection
from app.jurisdictions.ca.catalog import (
    CANADA_WORKERS_BENEFIT,
    EDUCATOR_SCHOOL_SUPPLY_CREDIT,
    EMPLOYEE_AND_PARTNER_GST_HST_REBATE,
    INCOME_TAX_DEDUCTED,
    JOURNALISM_LABOUR_TAX_CREDIT,
    PART_XII_2_TAX_CREDIT,
    PROVINCIAL_CREDITS,
    REFUND,
    REFUND_OR_BALANCE_OWING,
    REFUNDABLE_MEDICAL_EXPENSE_SUPPLEMENT,
    TAX_PAID_BY_INSTALMENTS,
    TOTAL_CREDITS,
    TOTAL_PAYABLE,
)

INPUTS = frozenset[str]()

OUTPUTS = frozenset(
    {
        "ca/refund_or_balance_owing",
    }
)

STEPS = {
    # T1 line 166 (line 48200) "Add lines 150 to 165. Total credits": line 150 (43700), line 154
    # (45200) "Refundable medical expense supplement (use Federal Worksheet)", line 155 (45300)
    # "Canada workers benefit (CWB) (complete Schedule 6)", line 159 (45600) "Part XII.2 tax
    # credit (box 38 of all T3 slips and box 209 of all T5013 slips)", line 160 (45700)
    # "Employee and partner GST/HST rebate (complete Form GST370)", line 161 (46900), line 162
    # (47555) "Canadian journalism labour tax credit (box 236 of all T5013 slips)", line 164
    # (47600) "Tax paid by instalments" and line 165 (47900), in line order, as the other lines
    # are not triggered or not yet wired.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/income_tax_deducted",
                "ca/refundable_medical_expense_supplement",
                "ca/canada_workers_benefit",
                "ca/part_xii_2_tax_credit",
                "ca/employee_and_partner_gst_hst_rebate",
                "ca/educator_school_supply_credit",
                "ca/journalism_labour_tax_credit",
                "ca/tax_paid_by_instalments",
                "ca/provincial_credits",
            )
        },
        produces={"output": "ca/total_credits"},
    ),
    # T1 line 167 "Line 149 minus line 166 If the amount is negative, enter it on line
    # 48400 below. If the amount is positive, enter it on line 48500 below. Refund or
    # balance owing": not floored, so a negative result is a refund and a positive one a
    # balance owing.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ca/total_payable", "less": "ca/total_credits"},
        produces={"output": "ca/refund_or_balance_owing"},
    ),
    # T1 line 48400 "Refund": line 167 is entered on line 48400 "If the amount is negative", so
    # the total credits less the total payable, not below zero, a refund and never a negative.
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={"amount": "ca/total_credits", "less": "ca/total_payable"},
        produces={"output": "ca/refund"},
    ),
}

WIRING = {
    (
        Sum,
        frozenset(
            {
                INCOME_TAX_DEDUCTED,
                REFUNDABLE_MEDICAL_EXPENSE_SUPPLEMENT,
                CANADA_WORKERS_BENEFIT,
                PART_XII_2_TAX_CREDIT,
                EMPLOYEE_AND_PARTNER_GST_HST_REBATE,
                EDUCATOR_SCHOOL_SUPPLY_CREDIT,
                JOURNALISM_LABOUR_TAX_CREDIT,
                TAX_PAID_BY_INSTALMENTS,
                PROVINCIAL_CREDITS,
            }
        ),
        frozenset({TOTAL_CREDITS}),
    ),
    (
        Subtract,
        frozenset({TOTAL_PAYABLE, TOTAL_CREDITS}),
        frozenset({REFUND_OR_BALANCE_OWING}),
    ),
    (SubtractNotBelowZero, frozenset({TOTAL_CREDITS, TOTAL_PAYABLE}), frozenset({REFUND})),
}
