"""The CA-ON manifest entries of one family of lines (see `test_manifest.py`)."""

from __future__ import annotations

from app.domain.capabilities.credit_amount import CreditAmount
from app.domain.capabilities.multiple_over import MultipleOver
from app.domain.capabilities.per_unit_amount import PerUnitAmount
from app.domain.capabilities.subtract_not_below_zero import SubtractNotBelowZero
from app.domain.capabilities.sum import Sum
from app.domain.capabilities.times_count import TimesCount
from app.domain.manifest import CapabilitySelection
from app.jurisdictions.ca.capabilities.count_by_conditions import CountByConditions
from app.jurisdictions.ca.catalog import (
    NET_INCOME,
    SPOUSE_NET_INCOME,
    SPOUSE_OR_COMMON_LAW_PARTNER_ON_DECEMBER_31,
)
from app.jurisdictions.ca_on.catalog import (
    BANKRUPT_IN_YEAR,
    CLAIMS_TAX_REDUCTION_AMOUNTS_AT_EQUAL_NET_INCOME,
    DEPENDANTS,
    DEPENDENT_CHILDREN,
    NOT_CLAIMING_ONTARIO_TAX_REDUCTION,
    NOT_RESIDENT_OF_CANADA_AT_START_OF_YEAR,
    NOT_RESIDENT_OF_ONTARIO_AT_YEAR_END,
    ONTARIO_MINIMUM_TAX,
    ONTARIO_TAX_AFTER_DIVIDEND_CREDIT,
    ONTARIO_TAX_AFTER_REDUCTION,
    ONTARIO_TAX_BEFORE_REDUCTION,
    ONTARIO_TAX_REDUCTION,
    ONTARIO_TAX_REDUCTION_BEFORE_CONDITIONS,
    RETURN_FILED_BY_TRUSTEE_IN_BANKRUPTCY,
    TAX_REDUCTION_AMOUNTS,
    TAX_REDUCTION_AMOUNTS_CLAIMABLE,
    TAX_REDUCTION_BASIC,
    TAX_REDUCTION_CLAIMABLE,
    TAX_REDUCTION_FOR_CHILDREN,
    TAX_REDUCTION_FOR_CHILDREN_BEFORE_SPOUSE_RULE,
    TAX_REDUCTION_FOR_DEPENDANTS,
    TAX_REDUCTION_FOR_DEPENDANTS_BEFORE_SPOUSE_RULE,
)

INPUTS = frozenset(
    {
        "ca-on/dependent_children",
        "ca-on/dependants",
        "ca-on/ontario_minimum_tax",
        "ca-on/not_resident_of_canada_at_start_of_year",
        "ca-on/not_resident_of_ontario_at_year_end",
        "ca-on/bankrupt_in_year",
        "ca-on/return_filed_by_trustee_in_bankruptcy",
        "ca-on/not_claiming_ontario_tax_reduction",
        "ca/spouse_or_common_law_partner_on_december_31",
        "ca-on/claims_tax_reduction_amounts_at_equal_net_income",
    }
)

OUTPUTS = frozenset[str]()

STEPS = {
    # ON428 line 74 "Basic reduction 294.00": the dataset becomes an artifact of the same
    # name, the first part of line 77.
    CapabilitySelection(
        name="core/credit_amount",
        params={"amount": "ca-on/tax_reduction_basic"},
        consumes={},
        produces={"output": "ca-on/tax_reduction_basic"},
    ),
    # ON428 line 75 (line 60969) "Number of dependent children multiplied by $544" and line
    # 76 (line 60970) "Number of dependants multiplied by $544", before the rule that "only the
    # individual with the higher net income can claim the amounts on lines 75 and 76".
    CapabilitySelection(
        name="core/per_unit_amount",
        params={"amount": "ca-on/tax_reduction_per_dependant"},
        consumes={"count": "ca-on/dependent_children"},
        produces={"output": "ca-on/tax_reduction_for_children_before_spouse_rule"},
    ),
    CapabilitySelection(
        name="core/per_unit_amount",
        params={"amount": "ca-on/tax_reduction_per_dependant"},
        consumes={"count": "ca-on/dependants"},
        produces={"output": "ca-on/tax_reduction_for_dependants_before_spouse_rule"},
    ),
    # ON428 "If you had a spouse or common-law partner on December 31, 2025, only the
    # individual with the higher net income can claim the amounts on lines 75 and 76.": 1 when
    # there was no spouse or common-law partner (the T1's "Marital status on December 31, 2025"
    # Box 1 Married and Box 2 Living common-law), when the net income (line 23600) is more than
    # the spouse's (ON428 line 12 "Your spouse's or common-law partner's net income from line
    # 23600 of their return"), or when the two are equal and the caller says this return claims.
    CapabilitySelection(
        name="ca/count_by_conditions",
        params={"conditions": "ca-on/tax_reduction_spouse_rule"},
        consumes={
            "counts": (
                "ca/spouse_or_common_law_partner_on_december_31",
                "ca-on/claims_tax_reduction_amounts_at_equal_net_income",
            ),
            "amounts": ("ca/net_income", "ca/spouse_net_income"),
        },
        produces={"output": "ca-on/tax_reduction_amounts_claimable"},
    ),
    # ON428 line 75 and line 76, each once if this return claims them, else 0.
    CapabilitySelection(
        name="core/times_count",
        params={},
        consumes={
            "amount": "ca-on/tax_reduction_for_children_before_spouse_rule",
            "count": "ca-on/tax_reduction_amounts_claimable",
        },
        produces={"output": "ca-on/tax_reduction_for_children"},
    ),
    CapabilitySelection(
        name="core/times_count",
        params={},
        consumes={
            "amount": "ca-on/tax_reduction_for_dependants_before_spouse_rule",
            "count": "ca-on/tax_reduction_amounts_claimable",
        },
        produces={"output": "ca-on/tax_reduction_for_dependants"},
    ),
    # ON428 line 77 "Add lines 74 to 76.", in line order.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca-on/tax_reduction_basic",
                "ca-on/tax_reduction_for_children",
                "ca-on/tax_reduction_for_dependants",
            )
        },
        produces={"output": "ca-on/tax_reduction_amounts"},
    ),
    # ON428 line 73 "Line 71 plus line 72 =": line 71 is the Ontario tax after the dividend
    # credit and line 72 the additional tax for minimum tax purposes, as entered.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca-on/ontario_tax_after_dividend_credit",
                "ca-on/ontario_minimum_tax",
            )
        },
        produces={"output": "ca-on/ontario_tax_before_reduction"},
    ),
    # ON428 line 78 "Amount from line 77 above multiplied by 2", line 79 "Amount from line 73
    # above" and line 80 "Line 78 minus line 79 (if negative, enter "0") Ontario tax
    # reduction", before the conditions on which the form enters "0" on line 80.
    CapabilitySelection(
        name="core/multiple_over",
        params={"factor": "ca-on/tax_reduction_factor"},
        consumes={
            "amount": "ca-on/tax_reduction_amounts",
            "less": "ca-on/ontario_tax_before_reduction",
        },
        produces={"output": "ca-on/ontario_tax_reduction_before_conditions"},
    ),
    # ON428 "Enter "0" on line 80 if any of the following applies to you:" the six printed
    # conditions in the form's order: "You were not a resident of Canada at the beginning of the
    # year", "You were not a resident of Ontario on December 31, 2025", "There is an amount on
    # line 72", "You were bankrupt at any time in 2025", "Your return is filed for you by a
    # trustee in bankruptcy" and "You are choosing not to claim an Ontario tax reduction": 0 when
    # any applies, else 1.
    CapabilitySelection(
        name="ca/count_by_conditions",
        params={"conditions": "ca-on/tax_reduction_conditions"},
        consumes={
            "counts": (
                "ca-on/not_resident_of_canada_at_start_of_year",
                "ca-on/not_resident_of_ontario_at_year_end",
                "ca-on/bankrupt_in_year",
                "ca-on/return_filed_by_trustee_in_bankruptcy",
                "ca-on/not_claiming_ontario_tax_reduction",
            ),
            "amounts": ("ca-on/ontario_minimum_tax",),
        },
        produces={"output": "ca-on/tax_reduction_claimable"},
    ),
    # ON428 line 80 "Ontario tax reduction": line 78 minus line 79 once if none of the six
    # conditions applies, else "0".
    CapabilitySelection(
        name="core/times_count",
        params={},
        consumes={
            "amount": "ca-on/ontario_tax_reduction_before_conditions",
            "count": "ca-on/tax_reduction_claimable",
        },
        produces={"output": "ca-on/ontario_tax_reduction"},
    ),
    # ON428 line 81 "Line 73 minus line 80 (if negative, enter "0")".
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca-on/ontario_tax_before_reduction",
            "less": "ca-on/ontario_tax_reduction",
        },
        produces={"output": "ca-on/ontario_tax_after_reduction"},
    ),
}

WIRING = {
    (CreditAmount, frozenset(), frozenset({TAX_REDUCTION_BASIC})),
    (
        PerUnitAmount,
        frozenset({DEPENDENT_CHILDREN}),
        frozenset({TAX_REDUCTION_FOR_CHILDREN_BEFORE_SPOUSE_RULE}),
    ),
    (
        PerUnitAmount,
        frozenset({DEPENDANTS}),
        frozenset({TAX_REDUCTION_FOR_DEPENDANTS_BEFORE_SPOUSE_RULE}),
    ),
    (
        CountByConditions,
        frozenset(
            {
                SPOUSE_OR_COMMON_LAW_PARTNER_ON_DECEMBER_31,
                CLAIMS_TAX_REDUCTION_AMOUNTS_AT_EQUAL_NET_INCOME,
                NET_INCOME,
                SPOUSE_NET_INCOME,
            }
        ),
        frozenset({TAX_REDUCTION_AMOUNTS_CLAIMABLE}),
    ),
    (
        TimesCount,
        frozenset({TAX_REDUCTION_FOR_CHILDREN_BEFORE_SPOUSE_RULE, TAX_REDUCTION_AMOUNTS_CLAIMABLE}),
        frozenset({TAX_REDUCTION_FOR_CHILDREN}),
    ),
    (
        TimesCount,
        frozenset(
            {TAX_REDUCTION_FOR_DEPENDANTS_BEFORE_SPOUSE_RULE, TAX_REDUCTION_AMOUNTS_CLAIMABLE}
        ),
        frozenset({TAX_REDUCTION_FOR_DEPENDANTS}),
    ),
    (
        Sum,
        frozenset({TAX_REDUCTION_BASIC, TAX_REDUCTION_FOR_CHILDREN, TAX_REDUCTION_FOR_DEPENDANTS}),
        frozenset({TAX_REDUCTION_AMOUNTS}),
    ),
    (
        Sum,
        frozenset({ONTARIO_TAX_AFTER_DIVIDEND_CREDIT, ONTARIO_MINIMUM_TAX}),
        frozenset({ONTARIO_TAX_BEFORE_REDUCTION}),
    ),
    (
        MultipleOver,
        frozenset({TAX_REDUCTION_AMOUNTS, ONTARIO_TAX_BEFORE_REDUCTION}),
        frozenset({ONTARIO_TAX_REDUCTION_BEFORE_CONDITIONS}),
    ),
    (
        CountByConditions,
        frozenset(
            {
                NOT_RESIDENT_OF_CANADA_AT_START_OF_YEAR,
                NOT_RESIDENT_OF_ONTARIO_AT_YEAR_END,
                BANKRUPT_IN_YEAR,
                RETURN_FILED_BY_TRUSTEE_IN_BANKRUPTCY,
                NOT_CLAIMING_ONTARIO_TAX_REDUCTION,
                ONTARIO_MINIMUM_TAX,
            }
        ),
        frozenset({TAX_REDUCTION_CLAIMABLE}),
    ),
    (
        TimesCount,
        frozenset({ONTARIO_TAX_REDUCTION_BEFORE_CONDITIONS, TAX_REDUCTION_CLAIMABLE}),
        frozenset({ONTARIO_TAX_REDUCTION}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({ONTARIO_TAX_BEFORE_REDUCTION, ONTARIO_TAX_REDUCTION}),
        frozenset({ONTARIO_TAX_AFTER_REDUCTION}),
    ),
}
