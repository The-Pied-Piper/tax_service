"""The CA-ON manifest entries of one family of lines (see `test_manifest.py`)."""

from __future__ import annotations

from app.domain.capabilities.apply_rate import ApplyRate
from app.domain.capabilities.greater_of import GreaterOf
from app.domain.capabilities.subtract import Subtract
from app.domain.capabilities.subtract_not_below_zero import SubtractNotBelowZero
from app.domain.capabilities.sum import Sum
from app.domain.capabilities.sum_not_below_zero import SumNotBelowZero
from app.domain.capabilities.times_count import TimesCount
from app.domain.manifest import CapabilitySelection
from app.jurisdictions.ca.catalog import (
    ADVANCED_CANADA_WORKERS_BENEFIT,
    CPP_PART_4_COMPLETED,
    CPP_PAYABLE_ON_SELF_EMPLOYMENT,
    DISABILITY_AMOUNT_FOR_SELF,
    DISABILITY_TRANSFERRED_AMOUNT,
    EI_PAYABLE_ON_SELF_EMPLOYMENT,
    EI_SPECIAL_BENEFITS_AGREEMENT,
    FEDERAL_TAX_LESS_CREDITS,
    FEDERAL_TAX_ON_SPLIT_INCOME,
    NET_FEDERAL_TAX,
    RESP_AIPS_ADDITIONAL_TAX,
    RL_10_LABOUR_SPONSORED_FUND_AMOUNT,
    SELF_EMPLOYED_CPP_CONTRIBUTIONS_PAYABLE,
    SELF_EMPLOYED_EI_PREMIUMS,
    SPECIAL_TAXES,
    SPLIT_INCOME_DIVIDENDS,
    SPLIT_INCOME_DIVIDENDS_OTHER_THAN_ELIGIBLE,
    SPLIT_INCOME_LINE_10,
    SPLIT_INCOME_LINE_13,
    SPLIT_INCOME_LINE_14,
    SPLIT_INCOME_LINE_15,
    SPLIT_INCOME_LINE_18,
    SPLIT_INCOME_LINE_19,
    SPLIT_INCOME_LINE_20,
    SPLIT_INCOME_LINE_21,
    SPLIT_INCOME_LINE_22,
    SPLIT_INCOME_LINE_24,
    SPLIT_INCOME_LINE_29,
    SPLIT_INCOME_LINE_30,
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
    # Form T1206 Part 2 line 10 "Line 8 plus line 9", line 9 being "Amount from line 41500 of your
    # return" (the advanced Canada workers benefit).
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/federal_tax_on_split_income",
                "ca/advanced_canada_workers_benefit",
            )
        },
        produces={"output": "ca/split_income_line_10"},
    ),
    # "Federal disability tax credit": line 11 "Amount from line 31600 of your return" (the caller's
    # amount under its T1 name, not yet computed) and line 12 "Amount from line 31800 of your
    # return" (the disability amount transferred from a dependant), line 13 "Line 11 plus line 12".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/disability_amount_for_self",
                "ca/disability_transferred_amount",
            )
        },
        produces={"output": "ca/split_income_line_13"},
    ),
    # Line 14, line 13 "× 14.5%".
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/split_income_disability_credit_rate"},
        consumes={"base": "ca/split_income_line_13"},
        produces={"output": "ca/split_income_line_14"},
    ),
    # Line 15 "Line 10 minus line 14", which prints no floor.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ca/split_income_line_10", "less": "ca/split_income_line_14"},
        produces={"output": "ca/split_income_line_15"},
    ),
    # "Federal dividend tax credit on split income": line 16 "Amount from line 1 of Part 1" and line
    # 17 "Amount from line 2 of Part 1" are the caller's lines 1 and 2, read as they are; line 18
    # "Line 16 minus line 17 (if negative, enter "0")".
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/split_income_dividends",
            "less": "ca/split_income_dividends_other_than_eligible",
        },
        produces={"output": "ca/split_income_line_18"},
    ),
    # Line 19, line 17 "× 9.0301%", and line 20, line 18 "× 15.0198%".
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/split_income_dividend_credit_rate_other_than_eligible"},
        consumes={"base": "ca/split_income_dividends_other_than_eligible"},
        produces={"output": "ca/split_income_line_19"},
    ),
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/split_income_dividend_credit_rate_eligible"},
        consumes={"base": "ca/split_income_line_18"},
        produces={"output": "ca/split_income_line_20"},
    ),
    # Line 21 "Line 19 plus line 20" and line 22 "Line 15 minus line 21", which prints no floor.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/split_income_line_19",
                "ca/split_income_line_20",
            )
        },
        produces={"output": "ca/split_income_line_21"},
    ),
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ca/split_income_line_15", "less": "ca/split_income_line_21"},
        produces={"output": "ca/split_income_line_22"},
    ),
    # Line 24 "Line 22 minus line 23 (if negative, enter "0")": line 23, the federal foreign tax
    # credit on split income, is not wired yet, so line 24 is line 22, not below zero, over one
    # part.
    CapabilitySelection(
        name="core/sum_not_below_zero",
        params={},
        consumes={"parts": ("ca/split_income_line_22",)},
        produces={"output": "ca/split_income_line_24"},
    ),
    # Line 25 "Amount from line 40600 of your return", line 26 "Amount from line 41600 of your
    # return" and line 27 "Line 25 minus line 26 (if negative, enter "0")" are the T1's line 139
    # (41700), the federal tax less credits, and line 28 "Amount from line 41500 of your return" is
    # line 140: line 29 "Line 27 plus line 28".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/federal_tax_less_credits",
                "ca/advanced_canada_workers_benefit",
            )
        },
        produces={"output": "ca/split_income_line_29"},
    ),
    # Line 30 "Enter whichever is more: the amount from line 24 or line 29."
    CapabilitySelection(
        name="core/greater_of",
        params={},
        consumes={"amounts": ("ca/split_income_line_24", "ca/split_income_line_29")},
        produces={"output": "ca/split_income_line_30"},
    ),
    # T1 line 142 (line 42000) "Add lines 139 to 141. Net federal tax", here by Form T1206 Part 2
    # "Add the amount from line 30 to the amount from line 41800 of your return, and enter the
    # result on line 42000 of your return.": line 30 (the more of line 24 and line 29, line 29 being
    # lines 139 and 140) and line 141 (41800), in line order. Line 124 (minimum tax carryover) is
    # not modelled.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/split_income_line_30",
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
        frozenset({FEDERAL_TAX_ON_SPLIT_INCOME, ADVANCED_CANADA_WORKERS_BENEFIT}),
        frozenset({SPLIT_INCOME_LINE_10}),
    ),
    (
        Sum,
        frozenset({DISABILITY_AMOUNT_FOR_SELF, DISABILITY_TRANSFERRED_AMOUNT}),
        frozenset({SPLIT_INCOME_LINE_13}),
    ),
    (ApplyRate, frozenset({SPLIT_INCOME_LINE_13}), frozenset({SPLIT_INCOME_LINE_14})),
    (
        Subtract,
        frozenset({SPLIT_INCOME_LINE_10, SPLIT_INCOME_LINE_14}),
        frozenset({SPLIT_INCOME_LINE_15}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({SPLIT_INCOME_DIVIDENDS, SPLIT_INCOME_DIVIDENDS_OTHER_THAN_ELIGIBLE}),
        frozenset({SPLIT_INCOME_LINE_18}),
    ),
    (
        ApplyRate,
        frozenset({SPLIT_INCOME_DIVIDENDS_OTHER_THAN_ELIGIBLE}),
        frozenset({SPLIT_INCOME_LINE_19}),
    ),
    (ApplyRate, frozenset({SPLIT_INCOME_LINE_18}), frozenset({SPLIT_INCOME_LINE_20})),
    (
        Sum,
        frozenset({SPLIT_INCOME_LINE_19, SPLIT_INCOME_LINE_20}),
        frozenset({SPLIT_INCOME_LINE_21}),
    ),
    (
        Subtract,
        frozenset({SPLIT_INCOME_LINE_15, SPLIT_INCOME_LINE_21}),
        frozenset({SPLIT_INCOME_LINE_22}),
    ),
    (SumNotBelowZero, frozenset({SPLIT_INCOME_LINE_22}), frozenset({SPLIT_INCOME_LINE_24})),
    (
        Sum,
        frozenset({FEDERAL_TAX_LESS_CREDITS, ADVANCED_CANADA_WORKERS_BENEFIT}),
        frozenset({SPLIT_INCOME_LINE_29}),
    ),
    (
        GreaterOf,
        frozenset({SPLIT_INCOME_LINE_24, SPLIT_INCOME_LINE_29}),
        frozenset({SPLIT_INCOME_LINE_30}),
    ),
    (
        Sum,
        frozenset({SPLIT_INCOME_LINE_30, SPECIAL_TAXES}),
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
