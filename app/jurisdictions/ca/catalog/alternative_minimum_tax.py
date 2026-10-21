"""The federal catalog: alternative minimum tax, Form T691.

Part 1 of the form: the adjusted taxable income, from the film property, the rental and leasing
property and the tax shelter amounts.
"""

from __future__ import annotations

from decimal import Decimal

from app.jurisdictions.ca.catalog.base import CATALOG

AMT_FILM_PROPERTY_CCA_AND_CARRYING_CHARGES = CATALOG.declare(
    "amt_film_property_cca_and_carrying_charges", Decimal, non_negative=True
)
"""Film property CCA and carrying charges, Form T691 Part 1 line 2 "Capital cost allowance (CCA)
and carrying charges (2) claimed on certified film property acquired before March 1996 (usually
included on lines 22100 and 23200 of your return)": a starting amount, the caller's figure."""

AMT_FILM_PROPERTY_INCOME_BEFORE_CCA = CATALOG.declare(
    "amt_film_property_income_before_cca", Decimal, non_negative=True
)
"""Net income from film property before CCA and carrying charges, Form T691 Part 1 line 3 "Net
income from film property before CCA and carrying charges (if negative, enter "0") (3)": a
starting amount, the caller's figure, not below zero."""

AMT_FILM_PROPERTY_ADJUSTMENT = CATALOG.declare(
    "amt_film_property_adjustment", Decimal, non_negative=True
)
"""Film property adjustment, Form T691 Part 1 line 4 (67820) "Line 2 minus line 3 (if negative,
enter "0")": line 2 less line 3, not below zero."""

AMT_RENTAL_PROPERTY_CCA_AND_CARRYING_CHARGES = CATALOG.declare(
    "amt_rental_property_cca_and_carrying_charges", Decimal, non_negative=True
)
"""Rental and leasing property CCA and carrying charges, Form T691 Part 1 line 5 "CCA and carrying
charges (2) claimed on rental and leasing property (included on line 12600 of your return)": a
starting amount, the caller's figure."""

AMT_RENTAL_PROPERTY_INCOME_BEFORE_CCA = CATALOG.declare(
    "amt_rental_property_income_before_cca", Decimal, non_negative=True
)
"""Net income from rental and leasing property before CCA and carrying charges, Form T691 Part 1
line 6 "Net income from rental and leasing property before CCA and carrying charges (if negative,
enter "0") (3)": a starting amount, the caller's figure, not below zero."""

AMT_RENTAL_PROPERTY_ADJUSTMENT = CATALOG.declare(
    "amt_rental_property_adjustment", Decimal, non_negative=True
)
"""Rental and leasing property adjustment, Form T691 Part 1 line 7 (67830) "Line 5 minus line 6 (if
negative, enter "0")": line 5 less line 6, not below zero."""

AMT_TAX_SHELTER_LOSSES = CATALOG.declare("amt_tax_shelter_losses", Decimal, non_negative=True)
"""Losses from partnerships that are tax shelters, Form T691 Part 1 line 8 "Losses from partnerships
that are tax shelters (4)": a starting amount, the caller's figure."""

AMT_TAX_SHELTER_DEDUCTIBLE_AMOUNTS = CATALOG.declare(
    "amt_tax_shelter_deductible_amounts", Decimal, non_negative=True
)
"""Amounts deductible for properties that are tax shelters, Form T691 Part 1 line 9 "Amounts
deductible for properties that are tax shelters (5)": a starting amount, the caller's figure."""

AMT_LIMITED_PARTNER_CARRYING_CHARGES = CATALOG.declare(
    "amt_limited_partner_carrying_charges", Decimal, non_negative=True
)
"""Carrying charges of a limited or non-active partner, Form T691 Part 1 line 10 "Carrying charges
(2) for acquiring an interest in a partnership of which you are a limited or non-active partner,
or which owns a rental or leasing property or a film property (included on line 22100 of your
return) (6)": a starting amount, the caller's figure."""

AMT_TAX_SHELTER_ADJUSTMENTS = CATALOG.declare(
    "amt_tax_shelter_adjustments", Decimal, non_negative=True
)
"""Tax shelters, limited partnerships and non-active partners adjustment, Form T691 Part 1 line 11
(67840) "Add lines 8 to 10.": lines 8, 9 and 10 added."""

AMT_PART_1_SUBTOTAL = CATALOG.declare("amt_part_1_subtotal", Decimal, non_negative=True)
"""Adjusted taxable income subtotal, Form T691 Part 1 line 12 "Add lines 1, 4, 7, and 11.": the
taxable income of line 1 (`taxable_income`, from line 26000 of the return) plus lines 4, 7 and 11,
in line order."""
