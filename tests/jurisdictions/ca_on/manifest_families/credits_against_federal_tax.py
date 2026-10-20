"""The CA-ON manifest entries of one family of lines (see `test_manifest.py`)."""

from __future__ import annotations

from app.domain.capabilities.apply_rate import ApplyRate
from app.domain.capabilities.capped_amount import CappedAmount
from app.domain.capabilities.credit_amount import CreditAmount
from app.domain.capabilities.subtract_not_below_zero import SubtractNotBelowZero
from app.domain.capabilities.sum import Sum
from app.domain.manifest import CapabilitySelection
from app.jurisdictions.ca.catalog import (
    CREDITS_AGAINST_FEDERAL_TAX,
    FEDERAL_TAX_LESS_CREDITS,
    FEDERAL_TAX_WITH_ITC_RECAPTURE,
    LABOUR_SPONSORED_FUNDS_CREDIT,
    LABOUR_SPONSORED_FUNDS_CREDIT_BEFORE_MAXIMUM,
    LABOUR_SPONSORED_FUNDS_NET_COST,
    POLITICAL_CONTRIBUTIONS,
    POLITICAL_CREDIT,
    POLITICAL_CREDIT_BEFORE_MAXIMUM,
    POLITICAL_CREDIT_CHOSEN_COLUMN,
    POLITICAL_CREDIT_COLUMN_1_LINE_2,
    POLITICAL_CREDIT_COLUMN_1_LINE_3,
    POLITICAL_CREDIT_COLUMN_1_LINE_5,
    POLITICAL_CREDIT_COLUMN_1_LINE_6,
    POLITICAL_CREDIT_COLUMN_1_LINE_7,
    POLITICAL_CREDIT_COLUMN_2_LINE_2,
    POLITICAL_CREDIT_COLUMN_2_LINE_3,
    POLITICAL_CREDIT_COLUMN_2_LINE_5,
    POLITICAL_CREDIT_COLUMN_2_LINE_6,
    POLITICAL_CREDIT_COLUMN_2_LINE_7,
    POLITICAL_CREDIT_COLUMN_3_LINE_2,
    POLITICAL_CREDIT_COLUMN_3_LINE_3,
    POLITICAL_CREDIT_COLUMN_3_LINE_5,
    POLITICAL_CREDIT_COLUMN_3_LINE_6,
    POLITICAL_CREDIT_COLUMN_3_LINE_7,
    POLITICAL_CREDIT_SHORTCUT_AMOUNT,
    POLITICAL_CREDIT_SHORTCUT_THRESHOLD,
)
from app.jurisdictions.ca_on.capabilities.choose_by_range import ChooseByRange

INPUTS = frozenset(
    {
        "ca/labour_sponsored_funds_net_cost",
    }
)

OUTPUTS = frozenset[str]()

STEPS = {
    # T1 line 135 and line 41000 "Total federal political contributions (attach receipts) Line
    # 40900" is a caller input, ca/political_contributions, taken as the T1 takes it; the
    # Federal Worksheet "Line 41000 - Federal political contribution tax credit" reads it as
    # line 40900 and builds each of its three columns as printed, then the one that applies is
    # picked.
    # Federal Worksheet "Column 1: Line 40900 is $400 or less".
    # Line 2: 0.00, a printed constant.
    CapabilitySelection(
        name="core/credit_amount",
        params={"amount": "ca/political_credit_column_1_line_2"},
        consumes={},
        produces={"output": "ca/political_credit_column_1_line_2"},
    ),
    # Column 1 line 3 "Line 1 minus line 2 (if negative, enter "0") =", line 1 being the
    # contributions.
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/political_contributions",
            "less": "ca/political_credit_column_1_line_2",
        },
        produces={"output": "ca/political_credit_column_1_line_3"},
    ),
    # Column 1 line 4 "Rate 75%" and line 5 "Line 3 multiplied by the percentage from line 4 =".
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/political_credit_column_1_line_4"},
        consumes={"base": "ca/political_credit_column_1_line_3"},
        produces={"output": "ca/political_credit_column_1_line_5"},
    ),
    # Column 1 line 6: 0.00, a printed constant.
    CapabilitySelection(
        name="core/credit_amount",
        params={"amount": "ca/political_credit_column_1_line_6"},
        consumes={},
        produces={"output": "ca/political_credit_column_1_line_6"},
    ),
    # Column 1 line 7 "Line 5 plus line 6 Enter this amount on line 41000 of your return. =".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/political_credit_column_1_line_5",
                "ca/political_credit_column_1_line_6",
            ),
        },
        produces={"output": "ca/political_credit_column_1_line_7"},
    ),
    # Federal Worksheet "Column 2: Line 40900 is more than $400 but not more than $750".
    # Line 2: 400.00, a printed constant.
    CapabilitySelection(
        name="core/credit_amount",
        params={"amount": "ca/political_credit_column_2_line_2"},
        consumes={},
        produces={"output": "ca/political_credit_column_2_line_2"},
    ),
    # Column 2 line 3 "Line 1 minus line 2 (if negative, enter "0") =", line 1 being the
    # contributions.
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/political_contributions",
            "less": "ca/political_credit_column_2_line_2",
        },
        produces={"output": "ca/political_credit_column_2_line_3"},
    ),
    # Column 2 line 4 "Rate 50%" and line 5 "Line 3 multiplied by the percentage from line 4 =".
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/political_credit_column_2_line_4"},
        consumes={"base": "ca/political_credit_column_2_line_3"},
        produces={"output": "ca/political_credit_column_2_line_5"},
    ),
    # Column 2 line 6: 300.00, a printed constant.
    CapabilitySelection(
        name="core/credit_amount",
        params={"amount": "ca/political_credit_column_2_line_6"},
        consumes={},
        produces={"output": "ca/political_credit_column_2_line_6"},
    ),
    # Column 2 line 7 "Line 5 plus line 6 Enter this amount on line 41000 of your return. =".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/political_credit_column_2_line_5",
                "ca/political_credit_column_2_line_6",
            ),
        },
        produces={"output": "ca/political_credit_column_2_line_7"},
    ),
    # Federal Worksheet "Column 3: Line 40900 is more than more than $750".
    # Line 2: 750.00, a printed constant.
    CapabilitySelection(
        name="core/credit_amount",
        params={"amount": "ca/political_credit_column_3_line_2"},
        consumes={},
        produces={"output": "ca/political_credit_column_3_line_2"},
    ),
    # Column 3 line 3 "Line 1 minus line 2 (if negative, enter "0") =", line 1 being the
    # contributions.
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/political_contributions",
            "less": "ca/political_credit_column_3_line_2",
        },
        produces={"output": "ca/political_credit_column_3_line_3"},
    ),
    # Column 3 line 4 "Rate 33.33%" and line 5 "Line 3 multiplied by the percentage from line 4
    # =".
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/political_credit_column_3_line_4"},
        consumes={"base": "ca/political_credit_column_3_line_3"},
        produces={"output": "ca/political_credit_column_3_line_5"},
    ),
    # Column 3 line 6: 475.00, a printed constant.
    CapabilitySelection(
        name="core/credit_amount",
        params={"amount": "ca/political_credit_column_3_line_6"},
        consumes={},
        produces={"output": "ca/political_credit_column_3_line_6"},
    ),
    # Column 3 line 7 "Line 5 plus line 6 Enter this amount on line 41000 of your return. =".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/political_credit_column_3_line_5",
                "ca/political_credit_column_3_line_6",
            ),
        },
        produces={"output": "ca/political_credit_column_3_line_7"},
    ),
    # The column that applies, "Use column 1 if the amount from line 40900 is $400 or less. Use
    # column 2 if the amount from line 40900 is more than $400 but not more than $750. Use
    # column 3 if the amount from line 40900 is more than $750.": the limits are the columns'
    # own line 2 constants, which their headings print again.
    CapabilitySelection(
        name="ca-on/choose_by_range",
        params={},
        consumes={
            "amount": "ca/political_contributions",
            "first_limit": "ca/political_credit_column_2_line_2",
            "second_limit": "ca/political_credit_column_3_line_2",
            "first": "ca/political_credit_column_1_line_7",
            "second": "ca/political_credit_column_2_line_7",
            "third": "ca/political_credit_column_3_line_7",
        },
        produces={"output": "ca/political_credit_chosen_column"},
    ),
    # The shortcut, "If your total federal political contributions from line 40900 of your
    # return were" "$1,275 or more, enter $650 on line 41000 of your return. If not, use the
    # amount from line 40900 of your return to decide which column to complete.": the printed
    # 1,275 and 650 are datasets. Nothing compares two amounts yet, so the same chooser tests
    # the 1,275 against the contributions: when it is at most the contributions it chooses the
    # 650, otherwise the chosen column's line 7. A chooser's six artifact slots must be six
    # different artifacts, so the middle range is given column 3's line 2 (750) as its limit
    # and column 3's line 7 as its value: 1,275 is never at most 750, so it is never chosen.
    CapabilitySelection(
        name="core/credit_amount",
        params={"amount": "ca/political_credit_shortcut_threshold"},
        consumes={},
        produces={"output": "ca/political_credit_shortcut_threshold"},
    ),
    CapabilitySelection(
        name="core/credit_amount",
        params={"amount": "ca/political_credit_shortcut_amount"},
        consumes={},
        produces={"output": "ca/political_credit_shortcut_amount"},
    ),
    CapabilitySelection(
        name="ca-on/choose_by_range",
        params={},
        consumes={
            "amount": "ca/political_credit_shortcut_threshold",
            "first_limit": "ca/political_contributions",
            "second_limit": "ca/political_credit_column_3_line_2",
            "first": "ca/political_credit_shortcut_amount",
            "second": "ca/political_credit_column_3_line_7",
            "third": "ca/political_credit_chosen_column",
        },
        produces={"output": "ca/political_credit_before_maximum"},
    ),
    # T1 line 135 and line 41000 "(maximum $650)", after the worksheet's line 7 or the
    # shortcut's $650.
    CapabilitySelection(
        name="core/capped_amount",
        params={"cap": "ca/political_credit_maximum"},
        consumes={"base": "ca/political_credit_before_maximum"},
        produces={"output": "ca/political_credit"},
    ),
    # T1 line 137 and line 41400 "Labour-sponsored funds tax credit Line 41300: Net cost of
    # shares of a provincially registered fund Line 41300: Allowable credit": the guide's "Claim
    # the amount of your allowable credit on line 41400 of your return that is equal to 15% of
    # the net cost reported on line 41300 of your return, to a maximum of $750." is 15% of line
    # 41300, the caller's net cost.
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/labour_sponsored_funds_rate"},
        consumes={"base": "ca/labour_sponsored_funds_net_cost"},
        produces={"output": "ca/labour_sponsored_funds_credit_before_maximum"},
    ),
    # The guide's "to a maximum of $750" comes after the percentage, so it caps the credit.
    CapabilitySelection(
        name="core/capped_amount",
        params={"cap": "ca/labour_sponsored_funds_maximum"},
        consumes={"base": "ca/labour_sponsored_funds_credit_before_maximum"},
        produces={"output": "ca/labour_sponsored_funds_credit"},
    ),
    # T1 line 138 (line 41600) "Add lines 135 to 137.": line 135 (41000, the federal political
    # contribution tax credit) and line 137 (41400), in line order, as line 136 (41200, the
    # investment tax credit) is not yet wired.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": ("ca/political_credit", "ca/labour_sponsored_funds_credit"),
        },
        produces={"output": "ca/credits_against_federal_tax"},
    ),
    # T1 line 139 (line 41700) "Line 134 minus line 138 (if negative, enter "0")": line 134
    # (40600) "Line 132 minus line 133 (if negative, enter "0") Federal tax" carries line 132,
    # as line 133 (the federal logging tax credit) is not yet wired.
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/federal_tax_with_itc_recapture",
            "less": "ca/credits_against_federal_tax",
        },
        produces={"output": "ca/federal_tax_less_credits"},
    ),
}

WIRING = {
    (CreditAmount, frozenset(), frozenset({POLITICAL_CREDIT_COLUMN_1_LINE_2})),
    (
        SubtractNotBelowZero,
        frozenset({POLITICAL_CONTRIBUTIONS, POLITICAL_CREDIT_COLUMN_1_LINE_2}),
        frozenset({POLITICAL_CREDIT_COLUMN_1_LINE_3}),
    ),
    (
        ApplyRate,
        frozenset({POLITICAL_CREDIT_COLUMN_1_LINE_3}),
        frozenset({POLITICAL_CREDIT_COLUMN_1_LINE_5}),
    ),
    (CreditAmount, frozenset(), frozenset({POLITICAL_CREDIT_COLUMN_1_LINE_6})),
    (
        Sum,
        frozenset({POLITICAL_CREDIT_COLUMN_1_LINE_5, POLITICAL_CREDIT_COLUMN_1_LINE_6}),
        frozenset({POLITICAL_CREDIT_COLUMN_1_LINE_7}),
    ),
    (CreditAmount, frozenset(), frozenset({POLITICAL_CREDIT_COLUMN_2_LINE_2})),
    (
        SubtractNotBelowZero,
        frozenset({POLITICAL_CONTRIBUTIONS, POLITICAL_CREDIT_COLUMN_2_LINE_2}),
        frozenset({POLITICAL_CREDIT_COLUMN_2_LINE_3}),
    ),
    (
        ApplyRate,
        frozenset({POLITICAL_CREDIT_COLUMN_2_LINE_3}),
        frozenset({POLITICAL_CREDIT_COLUMN_2_LINE_5}),
    ),
    (CreditAmount, frozenset(), frozenset({POLITICAL_CREDIT_COLUMN_2_LINE_6})),
    (
        Sum,
        frozenset({POLITICAL_CREDIT_COLUMN_2_LINE_5, POLITICAL_CREDIT_COLUMN_2_LINE_6}),
        frozenset({POLITICAL_CREDIT_COLUMN_2_LINE_7}),
    ),
    (CreditAmount, frozenset(), frozenset({POLITICAL_CREDIT_COLUMN_3_LINE_2})),
    (
        SubtractNotBelowZero,
        frozenset({POLITICAL_CONTRIBUTIONS, POLITICAL_CREDIT_COLUMN_3_LINE_2}),
        frozenset({POLITICAL_CREDIT_COLUMN_3_LINE_3}),
    ),
    (
        ApplyRate,
        frozenset({POLITICAL_CREDIT_COLUMN_3_LINE_3}),
        frozenset({POLITICAL_CREDIT_COLUMN_3_LINE_5}),
    ),
    (CreditAmount, frozenset(), frozenset({POLITICAL_CREDIT_COLUMN_3_LINE_6})),
    (
        Sum,
        frozenset({POLITICAL_CREDIT_COLUMN_3_LINE_5, POLITICAL_CREDIT_COLUMN_3_LINE_6}),
        frozenset({POLITICAL_CREDIT_COLUMN_3_LINE_7}),
    ),
    (
        ChooseByRange,
        frozenset(
            {
                POLITICAL_CONTRIBUTIONS,
                POLITICAL_CREDIT_COLUMN_2_LINE_2,
                POLITICAL_CREDIT_COLUMN_3_LINE_2,
                POLITICAL_CREDIT_COLUMN_1_LINE_7,
                POLITICAL_CREDIT_COLUMN_2_LINE_7,
                POLITICAL_CREDIT_COLUMN_3_LINE_7,
            }
        ),
        frozenset({POLITICAL_CREDIT_CHOSEN_COLUMN}),
    ),
    (CreditAmount, frozenset(), frozenset({POLITICAL_CREDIT_SHORTCUT_THRESHOLD})),
    (CreditAmount, frozenset(), frozenset({POLITICAL_CREDIT_SHORTCUT_AMOUNT})),
    (
        ChooseByRange,
        frozenset(
            {
                POLITICAL_CREDIT_SHORTCUT_THRESHOLD,
                POLITICAL_CONTRIBUTIONS,
                POLITICAL_CREDIT_COLUMN_3_LINE_2,
                POLITICAL_CREDIT_SHORTCUT_AMOUNT,
                POLITICAL_CREDIT_COLUMN_3_LINE_7,
                POLITICAL_CREDIT_CHOSEN_COLUMN,
            }
        ),
        frozenset({POLITICAL_CREDIT_BEFORE_MAXIMUM}),
    ),
    (CappedAmount, frozenset({POLITICAL_CREDIT_BEFORE_MAXIMUM}), frozenset({POLITICAL_CREDIT})),
    (
        ApplyRate,
        frozenset({LABOUR_SPONSORED_FUNDS_NET_COST}),
        frozenset({LABOUR_SPONSORED_FUNDS_CREDIT_BEFORE_MAXIMUM}),
    ),
    (
        CappedAmount,
        frozenset({LABOUR_SPONSORED_FUNDS_CREDIT_BEFORE_MAXIMUM}),
        frozenset({LABOUR_SPONSORED_FUNDS_CREDIT}),
    ),
    (
        Sum,
        frozenset({POLITICAL_CREDIT, LABOUR_SPONSORED_FUNDS_CREDIT}),
        frozenset({CREDITS_AGAINST_FEDERAL_TAX}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({FEDERAL_TAX_WITH_ITC_RECAPTURE, CREDITS_AGAINST_FEDERAL_TAX}),
        frozenset({FEDERAL_TAX_LESS_CREDITS}),
    ),
}
