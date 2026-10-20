"""The CA-ON manifest entries of one family of lines (see `test_manifest.py`)."""

from __future__ import annotations

from app.domain.capabilities.credit_amount import CreditAmount
from app.domain.capabilities.multiple_over import MultipleOver
from app.domain.capabilities.per_unit_amount import PerUnitAmount
from app.domain.capabilities.subtract_not_below_zero import SubtractNotBelowZero
from app.domain.capabilities.sum import Sum
from app.domain.manifest import CapabilitySelection
from app.jurisdictions.ca_on.catalog import (
    DEPENDANTS,
    DEPENDENT_CHILDREN,
    ONTARIO_TAX_AFTER_DIVIDEND_CREDIT,
    ONTARIO_TAX_AFTER_REDUCTION,
    ONTARIO_TAX_REDUCTION,
    TAX_REDUCTION_AMOUNTS,
    TAX_REDUCTION_BASIC,
    TAX_REDUCTION_FOR_CHILDREN,
    TAX_REDUCTION_FOR_DEPENDANTS,
)

INPUTS = frozenset(
    {
        "ca-on/dependent_children",
        "ca-on/dependants",
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
    # 76 (line 60970) "Number of dependants multiplied by $544".
    CapabilitySelection(
        name="core/per_unit_amount",
        params={"amount": "ca-on/tax_reduction_per_dependant"},
        consumes={"count": "ca-on/dependent_children"},
        produces={"output": "ca-on/tax_reduction_for_children"},
    ),
    CapabilitySelection(
        name="core/per_unit_amount",
        params={"amount": "ca-on/tax_reduction_per_dependant"},
        consumes={"count": "ca-on/dependants"},
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
    # ON428 line 78 "Amount from line 77 above multiplied by 2", line 79 "Amount from line 73
    # above" and line 80 "Line 78 minus line 79 (if negative, enter "0") Ontario tax
    # reduction": line 73 is line 71, the Ontario tax after the dividend credit, while the
    # minimum tax (line 72) is not triggered.
    CapabilitySelection(
        name="core/multiple_over",
        params={"factor": "ca-on/tax_reduction_factor"},
        consumes={
            "amount": "ca-on/tax_reduction_amounts",
            "less": "ca-on/ontario_tax_after_dividend_credit",
        },
        produces={"output": "ca-on/ontario_tax_reduction"},
    ),
    # ON428 line 81 "Line 73 minus line 80 (if negative, enter "0")".
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca-on/ontario_tax_after_dividend_credit",
            "less": "ca-on/ontario_tax_reduction",
        },
        produces={"output": "ca-on/ontario_tax_after_reduction"},
    ),
}

WIRING = {
    (CreditAmount, frozenset(), frozenset({TAX_REDUCTION_BASIC})),
    (PerUnitAmount, frozenset({DEPENDENT_CHILDREN}), frozenset({TAX_REDUCTION_FOR_CHILDREN})),
    (PerUnitAmount, frozenset({DEPENDANTS}), frozenset({TAX_REDUCTION_FOR_DEPENDANTS})),
    (
        Sum,
        frozenset({TAX_REDUCTION_BASIC, TAX_REDUCTION_FOR_CHILDREN, TAX_REDUCTION_FOR_DEPENDANTS}),
        frozenset({TAX_REDUCTION_AMOUNTS}),
    ),
    (
        MultipleOver,
        frozenset({TAX_REDUCTION_AMOUNTS, ONTARIO_TAX_AFTER_DIVIDEND_CREDIT}),
        frozenset({ONTARIO_TAX_REDUCTION}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({ONTARIO_TAX_AFTER_DIVIDEND_CREDIT, ONTARIO_TAX_REDUCTION}),
        frozenset({ONTARIO_TAX_AFTER_REDUCTION}),
    ),
}
