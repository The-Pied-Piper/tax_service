"""The CA-ON manifest entries of one family of lines (see `test_manifest.py`)."""

from __future__ import annotations

from app.domain.capabilities.subtract_not_below_zero import SubtractNotBelowZero
from app.domain.capabilities.sum import Sum
from app.domain.manifest import CapabilitySelection
from app.jurisdictions.ca.catalog import (
    AMT_FILM_PROPERTY_ADJUSTMENT,
    AMT_FILM_PROPERTY_CCA_AND_CARRYING_CHARGES,
    AMT_FILM_PROPERTY_INCOME_BEFORE_CCA,
    AMT_LIMITED_PARTNER_CARRYING_CHARGES,
    AMT_PART_1_SUBTOTAL,
    AMT_RENTAL_PROPERTY_ADJUSTMENT,
    AMT_RENTAL_PROPERTY_CCA_AND_CARRYING_CHARGES,
    AMT_RENTAL_PROPERTY_INCOME_BEFORE_CCA,
    AMT_TAX_SHELTER_ADJUSTMENTS,
    AMT_TAX_SHELTER_DEDUCTIBLE_AMOUNTS,
    AMT_TAX_SHELTER_LOSSES,
    TAXABLE_INCOME,
)

INPUTS = frozenset(
    {
        "ca/amt_film_property_cca_and_carrying_charges",
        "ca/amt_film_property_income_before_cca",
        "ca/amt_rental_property_cca_and_carrying_charges",
        "ca/amt_rental_property_income_before_cca",
        "ca/amt_tax_shelter_losses",
        "ca/amt_tax_shelter_deductible_amounts",
        "ca/amt_limited_partner_carrying_charges",
    }
)

OUTPUTS = frozenset(
    {
        "ca/amt_part_1_subtotal",
    }
)

STEPS = {
    # Part 1 line 4 "Line 2 minus line 3 (if negative, enter "0")" and "67820 =", the film
    # property's adjustment, line 2 being the caller's CCA and carrying charges and line 3 the
    # caller's net income from film property before CCA.
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/amt_film_property_cca_and_carrying_charges",
            "less": "ca/amt_film_property_income_before_cca",
        },
        produces={"output": "ca/amt_film_property_adjustment"},
    ),
    # Part 1 line 7 "Line 5 minus line 6 (if negative, enter "0")" and "67830 =", the rental and
    # leasing property's adjustment, line 5 the caller's CCA and carrying charges and line 6 the
    # caller's net income from rental and leasing property before CCA.
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/amt_rental_property_cca_and_carrying_charges",
            "less": "ca/amt_rental_property_income_before_cca",
        },
        produces={"output": "ca/amt_rental_property_adjustment"},
    ),
    # Part 1 line 11 "Add lines 8 to 10." and "67840 =", the tax shelters, limited partnerships and
    # non-active partners: the caller's lines 8, 9 and 10 in line order.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/amt_tax_shelter_losses",
                "ca/amt_tax_shelter_deductible_amounts",
                "ca/amt_limited_partner_carrying_charges",
            )
        },
        produces={"output": "ca/amt_tax_shelter_adjustments"},
    ),
    # Part 1 line 12 "Add lines 1, 4, 7, and 11." (line 1 the taxable income from line 26000 of the
    # return, read from the taxable income artifact, and lines 4, 7 and 11 in line order).
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/taxable_income",
                "ca/amt_film_property_adjustment",
                "ca/amt_rental_property_adjustment",
                "ca/amt_tax_shelter_adjustments",
            )
        },
        produces={"output": "ca/amt_part_1_subtotal"},
    ),
}

WIRING = {
    (
        SubtractNotBelowZero,
        frozenset(
            {AMT_FILM_PROPERTY_CCA_AND_CARRYING_CHARGES, AMT_FILM_PROPERTY_INCOME_BEFORE_CCA}
        ),
        frozenset({AMT_FILM_PROPERTY_ADJUSTMENT}),
    ),
    (
        SubtractNotBelowZero,
        frozenset(
            {AMT_RENTAL_PROPERTY_CCA_AND_CARRYING_CHARGES, AMT_RENTAL_PROPERTY_INCOME_BEFORE_CCA}
        ),
        frozenset({AMT_RENTAL_PROPERTY_ADJUSTMENT}),
    ),
    (
        Sum,
        frozenset(
            {
                AMT_TAX_SHELTER_LOSSES,
                AMT_TAX_SHELTER_DEDUCTIBLE_AMOUNTS,
                AMT_LIMITED_PARTNER_CARRYING_CHARGES,
            }
        ),
        frozenset({AMT_TAX_SHELTER_ADJUSTMENTS}),
    ),
    (
        Sum,
        frozenset(
            {
                TAXABLE_INCOME,
                AMT_FILM_PROPERTY_ADJUSTMENT,
                AMT_RENTAL_PROPERTY_ADJUSTMENT,
                AMT_TAX_SHELTER_ADJUSTMENTS,
            }
        ),
        frozenset({AMT_PART_1_SUBTOTAL}),
    ),
}
