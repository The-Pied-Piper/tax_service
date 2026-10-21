"""The CA-ON manifest entries of one family of lines (see `test_manifest.py`)."""

from __future__ import annotations

from app.domain.capabilities.apply_rate import ApplyRate
from app.domain.capabilities.subtract import Subtract
from app.domain.capabilities.subtract_not_below_zero import SubtractNotBelowZero
from app.domain.capabilities.sum import Sum
from app.domain.manifest import CapabilitySelection
from app.jurisdictions.ca.catalog import (
    AMT_CAPITAL_GAINS_ADJUSTMENTS,
    AMT_CLASS_43_1_INCOME,
    AMT_FILM_PROPERTY_ADJUSTMENT,
    AMT_FILM_PROPERTY_CCA_AND_CARRYING_CHARGES,
    AMT_FILM_PROPERTY_INCOME_BEFORE_CCA,
    AMT_GRADUATED_RATE_ESTATE_CAPITAL_GAINS,
    AMT_LIMITED_PARTNER_CARRYING_CHARGES,
    AMT_MORTGAGE_FORECLOSURE_CAPITAL_GAINS,
    AMT_NET_CAPITAL_GAINS_AFTER_ADJUSTMENTS,
    AMT_PART_1_SUBTOTAL,
    AMT_PUBLICLY_LISTED_GIFTS_ADJUSTMENT,
    AMT_PUBLICLY_LISTED_GIFTS_NET,
    AMT_PUBLICLY_LISTED_GIFTS_T1170_LINE_68231,
    AMT_PUBLICLY_LISTED_GIFTS_TOTAL,
    AMT_RENTAL_PROPERTY_ADJUSTMENT,
    AMT_RENTAL_PROPERTY_CCA_AND_CARRYING_CHARGES,
    AMT_RENTAL_PROPERTY_INCOME_BEFORE_CCA,
    AMT_RESOURCE_EXPENDITURES,
    AMT_RESOURCE_FOREIGN_PROPERTY_INCOME,
    AMT_RESOURCE_INCOME_TOTAL,
    AMT_RESOURCE_PRODUCTION_INCOME,
    AMT_RESOURCE_PROPERTY_AND_FLOW_THROUGH_SHARES,
    AMT_TAX_SHELTER_ADJUSTMENTS,
    AMT_TAX_SHELTER_DEDUCTIBLE_AMOUNTS,
    AMT_TAX_SHELTER_LOSSES,
    AMT_TREATY_EXEMPT_CAPITAL_GAINS,
    CAPITAL_GAIN,
    OTHER_FORECLOSURE_GAIN_OR_LOSS,
    QFFP_FORECLOSURE_GAIN_OR_LOSS,
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
        "ca/amt_resource_expenditures",
        "ca/amt_resource_production_income",
        "ca/amt_resource_foreign_property_income",
        "ca/amt_class_43_1_income",
        "ca/amt_treaty_exempt_capital_gains",
        "ca/amt_graduated_rate_estate_capital_gains",
        "ca/amt_publicly_listed_gifts_total",
        "ca/amt_publicly_listed_gifts_t1170_line_68231",
    }
)

OUTPUTS = frozenset(
    {
        "ca/amt_part_1_subtotal",
        "ca/amt_resource_property_and_flow_through_shares",
        "ca/amt_net_capital_gains_after_adjustments",
        "ca/amt_publicly_listed_gifts_adjustment",
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
    # Part 9 line 5 "Add lines 2 to 4.", the three income lines of Part 9 in line order.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/amt_resource_production_income",
                "ca/amt_resource_foreign_property_income",
                "ca/amt_class_43_1_income",
            )
        },
        produces={"output": "ca/amt_resource_income_total"},
    ),
    # Part 9 line 6 "Line 1 minus line 5 (if negative, enter "0")" and "Resource property and
    # flow-through share 67860 =", the amount that goes to line 14 of Part 1.
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/amt_resource_expenditures",
            "less": "ca/amt_resource_income_total",
        },
        produces={"output": "ca/amt_resource_property_and_flow_through_shares"},
    ),
    # Part 1 line 16 "Capital gains or losses arising from mortgage foreclosures and conditional
    # sales repossessions from lines 12400 and 15500 of Schedule 3", the two foreclosure totals
    # of Schedule 3, a loss in brackets.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/qffp_foreclosure_gain_or_loss",
                "ca/other_foreclosure_gain_or_loss",
            )
        },
        produces={"output": "ca/amt_mortgage_foreclosure_capital_gains"},
    ),
    # Part 1 line 19 "Add lines 16 to 18.", lines 16, 17 and 18 in line order.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/amt_mortgage_foreclosure_capital_gains",
                "ca/amt_treaty_exempt_capital_gains",
                "ca/amt_graduated_rate_estate_capital_gains",
            )
        },
        produces={"output": "ca/amt_capital_gains_adjustments"},
    ),
    # Part 1 line 20 "Line 15 minus line 19 (if negative, show in brackets)", the capital gains
    # of line 15 (`capital_gain`, from line 19700 of Schedule 3) less line 19.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/capital_gain",
            "less": "ca/amt_capital_gains_adjustments",
        },
        produces={"output": "ca/amt_net_capital_gains_after_adjustments"},
    ),
    # Part 1 line 26 "Line 24 minus line 25", the net of the gifts before the 30% of line 26.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/amt_publicly_listed_gifts_total",
            "less": "ca/amt_publicly_listed_gifts_t1170_line_68231",
        },
        produces={"output": "ca/amt_publicly_listed_gifts_net"},
    ),
    # Part 1 line 26 "× 30%" of "Line 24 minus line 25", the rate from its dataset.
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/publicly_listed_gifts_rate"},
        consumes={"base": "ca/amt_publicly_listed_gifts_net"},
        produces={"output": "ca/amt_publicly_listed_gifts_adjustment"},
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
    (
        Sum,
        frozenset(
            {
                AMT_RESOURCE_PRODUCTION_INCOME,
                AMT_RESOURCE_FOREIGN_PROPERTY_INCOME,
                AMT_CLASS_43_1_INCOME,
            }
        ),
        frozenset({AMT_RESOURCE_INCOME_TOTAL}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({AMT_RESOURCE_EXPENDITURES, AMT_RESOURCE_INCOME_TOTAL}),
        frozenset({AMT_RESOURCE_PROPERTY_AND_FLOW_THROUGH_SHARES}),
    ),
    (
        Sum,
        frozenset({QFFP_FORECLOSURE_GAIN_OR_LOSS, OTHER_FORECLOSURE_GAIN_OR_LOSS}),
        frozenset({AMT_MORTGAGE_FORECLOSURE_CAPITAL_GAINS}),
    ),
    (
        Sum,
        frozenset(
            {
                AMT_MORTGAGE_FORECLOSURE_CAPITAL_GAINS,
                AMT_TREATY_EXEMPT_CAPITAL_GAINS,
                AMT_GRADUATED_RATE_ESTATE_CAPITAL_GAINS,
            }
        ),
        frozenset({AMT_CAPITAL_GAINS_ADJUSTMENTS}),
    ),
    (
        Subtract,
        frozenset({CAPITAL_GAIN, AMT_CAPITAL_GAINS_ADJUSTMENTS}),
        frozenset({AMT_NET_CAPITAL_GAINS_AFTER_ADJUSTMENTS}),
    ),
    (
        Subtract,
        frozenset({AMT_PUBLICLY_LISTED_GIFTS_TOTAL, AMT_PUBLICLY_LISTED_GIFTS_T1170_LINE_68231}),
        frozenset({AMT_PUBLICLY_LISTED_GIFTS_NET}),
    ),
    (
        ApplyRate,
        frozenset({AMT_PUBLICLY_LISTED_GIFTS_NET}),
        frozenset({AMT_PUBLICLY_LISTED_GIFTS_ADJUSTMENT}),
    ),
}
