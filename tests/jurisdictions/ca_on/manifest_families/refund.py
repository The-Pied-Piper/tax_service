"""The CA-ON manifest entries of one family of lines (see `test_manifest.py`)."""

from __future__ import annotations

from app.domain.capabilities.capped_amount import CappedAmount
from app.domain.capabilities.contribution_tier import TieredContribution
from app.domain.capabilities.credit_amount import CreditAmount
from app.domain.capabilities.greater_of import GreaterOf
from app.domain.capabilities.lesser_of import LesserOf
from app.domain.capabilities.subtract import Subtract
from app.domain.capabilities.subtract_not_below_zero import SubtractNotBelowZero
from app.domain.capabilities.sum import Sum
from app.domain.capabilities.times_count import TimesCount
from app.domain.manifest import CapabilitySelection
from app.jurisdictions.ca.capabilities.count_by_conditions import CountByConditions
from app.jurisdictions.ca.catalog import (
    CANADA_TRAINING_CREDIT,
    CANADA_WORKERS_BENEFIT,
    CPP_OVERPAYMENT,
    EDUCATOR_SCHOOL_SUPPLY_CREDIT,
    EI_OVERPAYMENT,
    EI_PAYABLE_ON_SELF_EMPLOYMENT,
    EMPLOYEE_AND_PARTNER_GST_HST_REBATE,
    INCOME_TAX_DEDUCTED,
    INVESTMENT_TAX_CREDIT_REFUND,
    JOURNALISM_LABOUR_TAX_CREDIT,
    PART_XII_2_TAX_CREDIT,
    PROVINCIAL_CREDITS,
    REFUND,
    REFUND_OR_BALANCE_OWING,
    REFUNDABLE_MEDICAL_EXPENSE_SUPPLEMENT,
    T2204_EXEMPTION,
    T2204_INSURABLE_EARNINGS,
    T2204_LINE_1,
    T2204_LINE_1_COUNT,
    T2204_LINE_1_PLUS_2,
    T2204_LINE_3,
    T2204_LINE_6,
    T2204_LINE_7,
    T2204_LINE_8,
    T2204_LINE_9,
    T2204_LINE_10,
    T2204_LINE_12,
    T2204_LINE_13,
    T2204_LINE_14,
    T2204_LINE_15,
    T2204_LINE_15_COUNT,
    T2204_LINE_16,
    T2204_PREMIUMS_DEDUCTED,
    T2204_SELF_EMPLOYMENT_EARNINGS,
    TAX_PAID_BY_INSTALMENTS,
    TOTAL_CREDITS,
    TOTAL_PAYABLE,
)

INPUTS = frozenset(
    {
        "ca/t2204_insurable_earnings",
        "ca/t2204_self_employment_earnings",
        "ca/t2204_premiums_deducted",
    }
)

OUTPUTS = frozenset(
    {
        "ca/refund_or_balance_owing",
        # Form T2204 line 16, printed and not read by any line: it equals T1 line 31200 on the
        # worked return (Return DD), and the end-to-end test compares the two there.
        "ca/t2204_line_16",
    }
)

STEPS = {
    # T2204 line 1 "Total EI insurable earnings (box 24 or, if blank, box 14 of your T4 slips) (1)",
    # with note (1) "If you have no self-employment earnings and your total EI insurable earnings
    # on your T4 slips are less than $2,000, enter "0"." The count is 0 when the note applies and
    # 1 otherwise, so line 1 is the insurable earnings times the count. The Quebec variant of
    # line 11 is not modelled.
    CapabilitySelection(
        name="ca/count_by_conditions",
        params={"conditions": "ca/t2204_line_1_conditions"},
        consumes={
            "counts": (),
            "amounts": (
                "ca/t2204_self_employment_earnings",
                "ca/t2204_exemption",
                "ca/t2204_insurable_earnings",
            ),
        },
        produces={"output": "ca/t2204_line_1_count"},
    ),
    CapabilitySelection(
        name="core/times_count",
        params={},
        consumes={
            "amount": "ca/t2204_insurable_earnings",
            "count": "ca/t2204_line_1_count",
        },
        produces={"output": "ca/t2204_line_1"},
    ),
    # T2204 line 3 "Line 1 plus line 2 (maximum $65,700)": the sum, then the maximum insurable
    # earnings of the dataset.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/t2204_line_1", "ca/t2204_self_employment_earnings")},
        produces={"output": "ca/t2204_line_1_plus_2"},
    ),
    CapabilitySelection(
        name="core/capped_amount",
        params={"cap": "ca/t2204_maximum_insurable_earnings"},
        consumes={"base": "ca/t2204_line_1_plus_2"},
        produces={"output": "ca/t2204_line_3"},
    ),
    # T2204 line 7 "Amount from line 3 – $2,000 = (if negative, enter "0")": the $2,000 is a
    # dataset, claimed whole, and the line is not below zero.
    CapabilitySelection(
        name="core/credit_amount",
        params={"amount": "ca/t2204_exemption"},
        consumes={},
        produces={"output": "ca/t2204_exemption"},
    ),
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={"amount": "ca/t2204_line_3", "less": "ca/t2204_exemption"},
        produces={"output": "ca/t2204_line_7"},
    ),
    # T2204 line 6 "Line 4 plus line 5", where line 4 is the premiums deducted (the input) and
    # line 5 is Schedule 13 line 9 for each agreement (`ca/ei_payable_on_self_employment`).
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/t2204_premiums_deducted", "ca/ei_payable_on_self_employment")},
        produces={"output": "ca/t2204_line_6"},
    ),
    # T2204 line 8 "Line 6 minus line 7 (if negative, enter "0")".
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={"amount": "ca/t2204_line_6", "less": "ca/t2204_line_7"},
        produces={"output": "ca/t2204_line_8"},
    ),
    # T2204 line 9 "Total premiums deducted from line 4 above": line 4 carried over one part.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/t2204_premiums_deducted",)},
        produces={"output": "ca/t2204_line_9"},
    ),
    # T2204 line 10 "Residents of other than Quebec Amount from line 1 × 1.64% = (maximum
    # $1,077.48)": the EI premium tier, on line 1 (not line 3).
    CapabilitySelection(
        name="core/contribution_tier",
        params={"tier": "ca/ei_premium"},
        consumes={"earnings": "ca/t2204_line_1"},
        produces={"output": "ca/t2204_line_10"},
    ),
    # T2204 line 12 "Enter the amount from line 10 or line 11, whichever applies.": line 10, line
    # 11 being the Quebec variant.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/t2204_line_10",)},
        produces={"output": "ca/t2204_line_12"},
    ),
    # T2204 line 13 "Line 9 minus line 12 (if negative, enter "0")".
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={"amount": "ca/t2204_line_9", "less": "ca/t2204_line_12"},
        produces={"output": "ca/t2204_line_13"},
    ),
    # T2204 line 14 "Enter whichever is more: amount from line 8 or line 13.", and line 15 "Enter
    # whichever is less: amount from line 9 or line 14."
    CapabilitySelection(
        name="core/greater_of",
        params={},
        consumes={"amounts": ("ca/t2204_line_8", "ca/t2204_line_13")},
        produces={"output": "ca/t2204_line_14"},
    ),
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={"amounts": ("ca/t2204_line_9", "ca/t2204_line_14")},
        produces={"output": "ca/t2204_line_15"},
    ),
    # T1 line 153 and line 45000 "Employment insurance (EI) overpayment": T2204 line 15 "If this
    # amount is more than $1, enter it on line 45000 of your return." The count is 1 when line
    # 15 is more than $1 and 0 otherwise.
    CapabilitySelection(
        name="ca/count_by_conditions",
        params={"conditions": "ca/t2204_line_15_conditions"},
        consumes={"counts": (), "amounts": ("ca/t2204_line_15",)},
        produces={"output": "ca/t2204_line_15_count"},
    ),
    CapabilitySelection(
        name="core/times_count",
        params={},
        consumes={"amount": "ca/t2204_line_15", "count": "ca/t2204_line_15_count"},
        produces={"output": "ca/ei_overpayment"},
    ),
    # T2204 line 16 "Enter whichever amount is the least: line 7, line 9 or line 12." On the
    # worked return it equals T1 line 31200, and nothing reads it.
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={"amounts": ("ca/t2204_line_7", "ca/t2204_line_9", "ca/t2204_line_12")},
        produces={"output": "ca/t2204_line_16"},
    ),
    # T1 line 166 (line 48200) "Add lines 150 to 165. Total credits": line 150 (43700), line 152
    # (44800) "CPP or QPP overpayment" (Schedule 8 line 29, 0 when line 24 is not positive), line
    # 153 (45000) "Employment insurance (EI) overpayment" (T2204 line 15 when it is more than $1),
    # line 154 (45200) "Refundable medical expense supplement (use Federal Worksheet)", line 155
    # (45300) "Canada workers benefit (CWB) (complete Schedule 6)", line 156 (45350) "Canada
    # training credit (CTC) (complete Schedule 11)", line 158 (45400) "Refund of investment tax
    # credit (complete Form T2038(IND))", line 159 (45600) "Part XII.2 tax credit (box 38 of all
    # T3 slips and box 209 of all T5013 slips)", line 160 (45700) "Employee and partner
    # GST/HST rebate (complete Form GST370)", line 161 (46900), line 162 (47555) "Canadian
    # journalism labour tax credit (box 236 of all T5013 slips)", line 164 (47600) "Tax paid by
    # instalments" and line 165 (47900), in line order, as the other lines are not triggered or
    # not yet wired.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/income_tax_deducted",
                "ca/cpp_overpayment",
                "ca/ei_overpayment",
                "ca/refundable_medical_expense_supplement",
                "ca/canada_workers_benefit",
                "ca/canada_training_credit",
                "ca/investment_tax_credit_refund",
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
                CPP_OVERPAYMENT,
                EI_OVERPAYMENT,
                REFUNDABLE_MEDICAL_EXPENSE_SUPPLEMENT,
                CANADA_WORKERS_BENEFIT,
                CANADA_TRAINING_CREDIT,
                INVESTMENT_TAX_CREDIT_REFUND,
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
    (
        CountByConditions,
        frozenset({T2204_SELF_EMPLOYMENT_EARNINGS, T2204_EXEMPTION, T2204_INSURABLE_EARNINGS}),
        frozenset({T2204_LINE_1_COUNT}),
    ),
    (
        TimesCount,
        frozenset({T2204_INSURABLE_EARNINGS, T2204_LINE_1_COUNT}),
        frozenset({T2204_LINE_1}),
    ),
    (
        Sum,
        frozenset({T2204_LINE_1, T2204_SELF_EMPLOYMENT_EARNINGS}),
        frozenset({T2204_LINE_1_PLUS_2}),
    ),
    (CappedAmount, frozenset({T2204_LINE_1_PLUS_2}), frozenset({T2204_LINE_3})),
    (CreditAmount, frozenset(), frozenset({T2204_EXEMPTION})),
    (
        SubtractNotBelowZero,
        frozenset({T2204_LINE_3, T2204_EXEMPTION}),
        frozenset({T2204_LINE_7}),
    ),
    (
        Sum,
        frozenset({T2204_PREMIUMS_DEDUCTED, EI_PAYABLE_ON_SELF_EMPLOYMENT}),
        frozenset({T2204_LINE_6}),
    ),
    (SubtractNotBelowZero, frozenset({T2204_LINE_6, T2204_LINE_7}), frozenset({T2204_LINE_8})),
    (Sum, frozenset({T2204_PREMIUMS_DEDUCTED}), frozenset({T2204_LINE_9})),
    (TieredContribution, frozenset({T2204_LINE_1}), frozenset({T2204_LINE_10})),
    (Sum, frozenset({T2204_LINE_10}), frozenset({T2204_LINE_12})),
    (SubtractNotBelowZero, frozenset({T2204_LINE_9, T2204_LINE_12}), frozenset({T2204_LINE_13})),
    (GreaterOf, frozenset({T2204_LINE_8, T2204_LINE_13}), frozenset({T2204_LINE_14})),
    (LesserOf, frozenset({T2204_LINE_9, T2204_LINE_14}), frozenset({T2204_LINE_15})),
    (CountByConditions, frozenset({T2204_LINE_15}), frozenset({T2204_LINE_15_COUNT})),
    (
        TimesCount,
        frozenset({T2204_LINE_15, T2204_LINE_15_COUNT}),
        frozenset({EI_OVERPAYMENT}),
    ),
    (
        LesserOf,
        frozenset({T2204_LINE_7, T2204_LINE_9, T2204_LINE_12}),
        frozenset({T2204_LINE_16}),
    ),
}
