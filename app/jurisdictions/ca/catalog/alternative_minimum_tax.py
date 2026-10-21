"""The federal catalog: alternative minimum tax, Form T691.

Part 1 of the form: the adjusted taxable income, from the film property, the rental and leasing
property, the tax shelter amounts, the resource property, the capital gains and the gifts of
publicly listed securities. Part 9 of the form: the resource property and flow-through shares.
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

AMT_RESOURCE_EXPENDITURES = CATALOG.declare("amt_resource_expenditures", Decimal, non_negative=True)
"""Resource expenditures, depletion allowances and carrying charges, Form T691 Part 9 line 1 "Total
of all resource expenditures, depletion allowances and carrying charges for resource property and
flow-through shares (included on lines 22100, 22400, and 23200 of your return)": a starting amount,
the caller's figure."""

AMT_RESOURCE_PRODUCTION_INCOME = CATALOG.declare(
    "amt_resource_production_income", Decimal, non_negative=True
)
"""Income from the production of petroleum, natural gas and minerals, Form T691 Part 9 line 2
"Income (including royalties) from production of petroleum, natural gas and minerals, before
carrying charges, resource expenditures, and depletion allowances included on line 1 (if negative,
enter "0")": a starting amount, the caller's figure, not below zero."""

AMT_RESOURCE_FOREIGN_PROPERTY_INCOME = CATALOG.declare(
    "amt_resource_foreign_property_income", Decimal, non_negative=True
)
"""Income from foreign resource properties, Form T691 Part 9 line 3 "Income from dispositions of
foreign resource properties, and recovery of exploration and development expenses before carrying
charges, resource expenditures and depletion allowances included on line 1 (if negative, enter
"0")": a starting amount, the caller's figure, not below zero."""

AMT_CLASS_43_1_INCOME = CATALOG.declare("amt_class_43_1_income", Decimal, non_negative=True)
"""Income from Class 43.1 or 43.2 property, Form T691 Part 9 line 4 "Income from property, or from a
business of selling the product of property, described in Class 43.1 or 43.2 in Schedule II of the
Income Tax Regulations before resource expenditures and depletion allowances included on line 1 (if
negative, enter "0")": a starting amount, the caller's figure, not below zero."""

AMT_RESOURCE_INCOME_TOTAL = CATALOG.declare("amt_resource_income_total", Decimal, non_negative=True)
"""Resource income total, Form T691 Part 9 line 5 "Add lines 2 to 4.": lines 2, 3 and 4 added."""

AMT_RESOURCE_PROPERTY_AND_FLOW_THROUGH_SHARES = CATALOG.declare(
    "amt_resource_property_and_flow_through_shares", Decimal, non_negative=True
)
"""Resource property and flow-through shares, Form T691 Part 9 line 6 "Line 1 minus line 5 (if
negative, enter "0")" and "Resource property and flow-through share 67860 =", the amount entered on
line 14 of Part 1: line 1 less line 5, not below zero."""

AMT_MORTGAGE_FORECLOSURE_CAPITAL_GAINS = CATALOG.declare(
    "amt_mortgage_foreclosure_capital_gains", Decimal
)
"""Capital gains or losses from mortgage foreclosures and conditional sales repossessions, Form
T691 Part 1 line 16 "Capital gains or losses arising from mortgage foreclosures and conditional
sales repossessions from lines 12400 and 15500 of Schedule 3": the two foreclosure totals of
Schedule 3, a loss in brackets."""

AMT_TREATY_EXEMPT_CAPITAL_GAINS = CATALOG.declare(
    "amt_treaty_exempt_capital_gains", Decimal, non_negative=True
)
"""Capital gains exempt under a tax treaty, Form T691 Part 1 line 17 "Part of total capital gains
included on line 15 that is exempt from Canadian tax under a tax treaty (included on line 25600 of
your return)": a starting amount, the caller's figure."""

AMT_GRADUATED_RATE_ESTATE_CAPITAL_GAINS = CATALOG.declare(
    "amt_graduated_rate_estate_capital_gains", Decimal, non_negative=True
)
"""Capital gains from graduated rate estates, Form T691 Part 1 line 18 "Certain capital gains from
graduated rate estates (for details, contact its legal representative)": a starting amount, the
caller's figure."""

AMT_CAPITAL_GAINS_ADJUSTMENTS = CATALOG.declare("amt_capital_gains_adjustments", Decimal)
"""Capital gains adjustments, Form T691 Part 1 line 19 "Add lines 16 to 18.": lines 16, 17 and 18
added, a loss in brackets."""

AMT_NET_CAPITAL_GAINS_AFTER_ADJUSTMENTS = CATALOG.declare(
    "amt_net_capital_gains_after_adjustments", Decimal
)
"""Capital gains after adjustments, Form T691 Part 1 line 20 "Line 15 minus line 19 (if negative,
show in brackets)": the capital gain of line 15 (`capital_gain`, from line 19700 of Schedule 3)
less line 19, shown in brackets when negative."""

AMT_PUBLICLY_LISTED_GIFTS_TOTAL = CATALOG.declare(
    "amt_publicly_listed_gifts_total", Decimal, non_negative=True
)
"""Capital gains on gifts of publicly listed securities, Form T691 Part 1 line 24 "Total amount of
lines 68230 and 68250 of Column 7 of Form T1170": a starting amount, the caller's figure."""

AMT_PUBLICLY_LISTED_GIFTS_T1170_LINE_68231 = CATALOG.declare(
    "amt_publicly_listed_gifts_t1170_line_68231", Decimal, non_negative=True
)
"""Amount from line 68231 of Form T1170, Form T691 Part 1 line 25 "Amount from line 68231 of Form
T1170": a starting amount, the caller's figure."""

AMT_PUBLICLY_LISTED_GIFTS_NET = CATALOG.declare("amt_publicly_listed_gifts_net", Decimal)
"""Capital gains on gifts of publicly listed securities less the T1170 amount, Form T691 Part 1 line
26 "Line 24 minus line 25": line 24 less line 25, a loss in brackets."""

AMT_PUBLICLY_LISTED_GIFTS_ADJUSTMENT = CATALOG.declare(
    "amt_publicly_listed_gifts_adjustment", Decimal
)
"""Adjustment for gifts of publicly listed securities, Form T691 Part 1 line 26 "× 30%" of "Line 24
minus line 25": the net of line 24 less line 25 at the 30% of its dataset, rounded to the cent,
a loss in brackets."""
