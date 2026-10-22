"""The federal catalog: alternative minimum tax, Form T691.

Part 1 of the form: the adjusted taxable income, from the film property, the rental and leasing
property, the tax shelter amounts, the resource property, the capital gains, the gifts of
publicly listed securities, the security options deductions, the losses of other years, the
deductions, the non-deductible expenses and the applicable rate. Part 9 of the form: the resource
property and flow-through shares.
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

AMT_CAPITAL_GAINS_DIFFERENCE = CATALOG.declare("amt_capital_gains_difference", Decimal)
"""Capital gains after adjustments less the taxable capital gains, Form T691 Part 1 line 22 "Line 20
minus line 21 (if negative, do not show in brackets.)": line 20 less line 21 (line 12700 of the
return, the taxable capital gains), left signed."""

AMT_CAPITAL_GAINS_ADDED = CATALOG.declare("amt_capital_gains_added", Decimal)
"""Capital gains added, Form T691 Part 1 line 23 "If line 20 is positive, enter the amount from line
22. If line 20 is negative, enter whichever is less: the amount from line 21 or line 22 (show in
brackets).": line 22 when line 20 is not negative, otherwise the lesser of line 21 and line 22 as a
negative amount."""

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

AMT_ADJUSTED_INCOME_WITH_GAINS = CATALOG.declare("amt_adjusted_income_with_gains", Decimal)
"""Adjusted taxable income with the gains, Form T691 Part 1 line 27 "Add lines 13, 14, 23, and 26.":
line 13 (the amount from line 12), line 14 (the amount from line 6 of Part 9), line 23 and line 26
in line order, a loss in brackets."""

AMT_T4_SECURITY_OPTIONS_BOXES_39_AND_91 = CATALOG.declare(
    "amt_t4_security_options_boxes_39_and_91", Decimal, non_negative=True
)
"""Security options deduction under paragraph 110(1)(d), Form T691 Part 1 line 28 "Total of all
amounts in boxes 39 and 91 of your T4 slips": a starting amount, the caller's figure."""

AMT_T1212_LINE_2_DEFERRED_SECURITY_OPTIONS = CATALOG.declare(
    "amt_t1212_line_2_deferred_security_options", Decimal, non_negative=True
)
"""Deferred security options benefits, Form T691 Part 1 line 29 "Amount from line 2 of Form T1212,
Statement of Deferred Security Options Benefits": a starting amount, the caller's figure."""

AMT_SECURITY_OPTIONS_D_TOTAL = CATALOG.declare(
    "amt_security_options_d_total", Decimal, non_negative=True
)
"""Security options deduction under paragraph 110(1)(d), Form T691 Part 1 line 30 "Line 28 plus
line 29" "67910 =": lines 28 and 29 added."""

AMT_SECURITY_OPTION_PUBLICLY_LISTED_GIFTS = CATALOG.declare(
    "amt_security_option_publicly_listed_gifts", Decimal, non_negative=True
)
"""Gifts of publicly listed securities acquired under a security option plan, Form T691 Part 1
line 31 "Gifts of publicly listed securities acquired under a security option plan included on line
24900 of your return" "67914": a starting amount, the caller's figure."""

AMT_SECURITY_OPTION_GIFTS_DEDUCTION = CATALOG.declare(
    "amt_security_option_gifts_deduction", Decimal, non_negative=True
)
"""Security option gifts deduction, Form T691 Part 1 line 31 "× 40% =": the 40% of line 31's gifts,
from its dataset, rounded to the cent."""

AMT_SECURITY_OPTIONS_NET = CATALOG.declare("amt_security_options_net", Decimal, non_negative=True)
"""Security options deduction net of the gifts deduction, Form T691 Part 1 line 32 "Line 30 minus
line 31 (if negative, enter "0")": line 30 less line 31, not below zero."""

AMT_T4_SECURITY_OPTIONS_BOXES_41_AND_92 = CATALOG.declare(
    "amt_t4_security_options_boxes_41_and_92", Decimal, non_negative=True
)
"""Security options deduction under paragraph 110(1)(d.1), Form T691 Part 1 line 35 "total of all
amounts in boxes 41 and 92 of your T4 slips": a starting amount, the caller's figure."""

AMT_PROSPECTOR_OR_GRUBSTAKER_DEDUCTION = CATALOG.declare(
    "amt_prospector_or_grubstaker_deduction", Decimal, non_negative=True
)
"""Deduction for a security received as a prospector or grubstaker, Form T691 Part 1 line 36
"Deduction included on line 24900 of your return for a security received as a prospector or
grubstaker": a starting amount, the caller's figure."""

AMT_DEFERRED_PROFIT_SHARING_PLAN_DEDUCTION = CATALOG.declare(
    "amt_deferred_profit_sharing_plan_deduction", Decimal, non_negative=True
)
"""Deduction for certain dispositions of securities from a deferred profit-sharing plan, Form T691
Part 1 line 37 "Deduction included on line 24900 of your return for certain dispositions of
securities received from a deferred profit-sharing plan": a starting amount, the caller's figure."""

AMT_SECURITY_OPTIONS_D1_TOTAL = CATALOG.declare(
    "amt_security_options_d1_total", Decimal, non_negative=True
)
"""Security options deductions under paragraph 110(1)(d.1), Form T691 Part 1 line 38 "Add lines 35
to 37." "67918 =": lines 35, 36 and 37 added."""

AMT_LIMITED_PARTNERSHIP_DIFFERENCE_NO_ELECTION = CATALOG.declare(
    "amt_limited_partnership_difference_no_election", Decimal, non_negative=True
)
"""Limited partnership losses difference with no election, Form T691 Part 1 line 39 "If you have
not filed an election (8), enter the difference between those losses and the amount of losses
deductible (9) for AMT purposes": a starting amount, the caller's figure."""

AMT_LIMITED_PARTNERSHIP_DIFFERENCE_ELECTION = CATALOG.declare(
    "amt_limited_partnership_difference_election", Decimal, non_negative=True
)
"""Limited partnership losses difference with an election, Form T691 Part 1 line 40 "If you have
filed an election (8), enter the difference between those losses and the amount of losses
deductible (9) for AMT purposes": a starting amount, the caller's figure, from line 67920."""

AMT_NON_CAPITAL_LOSSES_DIFFERENCE = CATALOG.declare(
    "amt_non_capital_losses_difference", Decimal, non_negative=True
)
"""Non-capital losses difference, Form T691 Part 1 line 41 "If you claimed non-capital losses,
including restricted farm losses or farm losses, incurred in another year on line 25200 of your
2025 return, indicate the difference between those losses and the losses that are deductible for
AMT purposes": a starting amount, the caller's figure."""

AMT_NET_CAPITAL_LOSSES_DIFFERENCE = CATALOG.declare(
    "amt_net_capital_losses_difference", Decimal, non_negative=True
)
"""Net capital losses difference, Form T691 Part 1 line 42 "If you claimed net capital losses,
incurred in another year on line 25300 of your 2025 return, indicate the difference between those
losses and the losses that are deductible for AMT purposes": a starting amount, the caller's
figure, from line 67922."""

AMT_OTHER_YEARS_LOSSES_TOTAL = CATALOG.declare(
    "amt_other_years_losses_total", Decimal, non_negative=True
)
"""Losses of other years difference, Form T691 Part 1 line 43 "Line 39 or 40, as applicable, plus
line 41 and 42": the one of lines 39 and 40 that applies, with lines 41 and 42, in line order."""

AMT_LIMITED_PARTNERSHIP_DIFFERENCE_APPLIED = CATALOG.declare(
    "amt_limited_partnership_difference_applied", Decimal, non_negative=True
)
"""Limited partnership losses difference applied, Form T691 Part 1 line 46 "Amount from line 39 or
40, as applicable": the one of lines 39 and 40 that applies."""

AMT_LIMITED_PARTNERSHIP_LOSSES_ADJUSTMENT = CATALOG.declare(
    "amt_limited_partnership_losses_adjustment", Decimal
)
"""Limited partnership losses of other years adjustment, Form T691 Part 1 line 47 "Line 45 minus
line 46": the limited partnership losses of other years (line 25100 of the return) less line 46, a
loss in brackets."""

AMT_NON_CAPITAL_LOSSES_ADJUSTMENT = CATALOG.declare("amt_non_capital_losses_adjustment", Decimal)
"""Non-capital losses of other years adjustment, Form T691 Part 1 line 50 "Line 48 minus line 49":
the non-capital losses of other years (line 25200 of the return) less line 49, a loss in
brackets."""

AMT_LOSSES_AND_DEDUCTIONS_SUBTOTAL = CATALOG.declare("amt_losses_and_deductions_subtotal", Decimal)
"""Losses and deductions subtotal, Form T691 Part 1 line 53 "Add lines 47, 50, 51, and 52.": lines
47, 50, 51 (the union dues of line 21200) and 52 (the child care expenses of line 21400), a loss in
brackets when line 47 or 50 is one."""

AMT_MOVING_EXPENSES_DEDUCTION = CATALOG.declare(
    "amt_moving_expenses_deduction", Decimal, non_negative=True
)
"""Moving expenses deduction, Form T691 Part 1 line 56 "Moving expenses deduction from line 21900 of
your return": a starting amount, the caller's figure."""

AMT_PPIP_PREMIUMS_DEDUCTION = CATALOG.declare(
    "amt_ppip_premiums_deduction", Decimal, non_negative=True
)
"""Deduction for PPIP premiums on self-employment income, Form T691 Part 1 line 59 "Deduction for
PPIP premiums on self-employment income from line 22300 of your return (Quebec only)": a starting
amount, the caller's figure."""

AMT_DEDUCTIONS_TOTAL = CATALOG.declare("amt_deductions_total", Decimal)
"""Deductions total, Form T691 Part 1 line 63 "Add lines 54 to 62.": line 53 carried and lines 55
to 62 in line order, a loss in brackets when line 53 is one."""

AMT_NON_DEDUCTIBLE_INTEREST = CATALOG.declare(
    "amt_non_deductible_interest", Decimal, non_negative=True
)
"""Interest expenses on money borrowed to earn income, Form T691 Part 1 line 64 "Interest expenses
on money borrowed to earn income or to purchase an annuity contract (included on line 22100 of your
return)": a starting amount, the caller's figure."""

AMT_LIFE_INSURANCE_PREMIUMS_AS_COLLATERAL = CATALOG.declare(
    "amt_life_insurance_premiums_as_collateral", Decimal, non_negative=True
)
"""Premiums on life insurance policies used as collateral, Form T691 Part 1 line 65 "Premiums on
life insurance policies used as collateral for money borrowed to earn income from property
(included on line 22100 of your return)": a starting amount, the caller's figure."""

AMT_FINANCING_EXPENSES = CATALOG.declare("amt_financing_expenses", Decimal, non_negative=True)
"""Financing expenses on money borrowed to earn income from property, Form T691 Part 1 line 66
"Financing expenses on money borrowed to earn income from property (included on line 22100 of your
return)": a starting amount, the caller's figure."""

AMT_INVESTMENT_COUNSEL_FEES = CATALOG.declare(
    "amt_investment_counsel_fees", Decimal, non_negative=True
)
"""Investment counsel fees, Form T691 Part 1 line 67 "Investment counsel fees (included on line
22100 of your return)": a starting amount, the caller's figure."""

AMT_NON_DEDUCTIBLE_PROPERTY_EXPENSES = CATALOG.declare(
    "amt_non_deductible_property_expenses", Decimal, non_negative=True
)
"""Non-deductible property expenses, Form T691 Part 1 line 68 "Add lines 64 to 67" "67924 =": lines
64 to 67 added."""

AMT_COMMISSION_EMPLOYMENT_EXPENSES = CATALOG.declare(
    "amt_commission_employment_expenses", Decimal, non_negative=True
)
"""Employment expenses of a commission employee, Form T691 Part 1 line 70 "Employment expenses
claimed and calculated as a commission employee (excluding amounts claimed as a salaried
employee)": a starting amount, the caller's figure."""

AMT_LEGAL_AND_ACCOUNTING_EXPENSES = CATALOG.declare(
    "amt_legal_and_accounting_expenses", Decimal, non_negative=True
)
"""Legal and accounting expenses, Form T691 Part 1 line 71 "Legal and accounting expenses": a
starting amount, the caller's figure."""

AMT_REPAYMENT_OF_SALARY_AND_WAGES = CATALOG.declare(
    "amt_repayment_of_salary_and_wages", Decimal, non_negative=True
)
"""Repayment of salary and wages, Form T691 Part 1 line 72 "Repayment of salary and wages": a
starting amount, the caller's figure."""

AMT_EXCESS_EPSP_AMOUNTS = CATALOG.declare("amt_excess_epsp_amounts", Decimal, non_negative=True)
"""Excess Employee Profits Share Plan amounts, Form T691 Part 1 line 73 "Excess Employee Profits
Share Plan (EPSP) amounts": a starting amount, the caller's figure."""

AMT_FORFEITED_SALARY_DEFERRAL_AMOUNTS = CATALOG.declare(
    "amt_forfeited_salary_deferral_amounts", Decimal, non_negative=True
)
"""Forfeited amounts under a salary deferral arrangement or an EPSP, Form T691 Part 1 line 74
"Forfeited amounts under a salary deferral arrangement or an EPSP": a starting amount, the caller's
figure."""

AMT_REPAYMENT_OF_WAGE_LOSS_REPLACEMENT = CATALOG.declare(
    "amt_repayment_of_wage_loss_replacement", Decimal, non_negative=True
)
"""Repayment of a wage loss replacement, Form T691 Part 1 line 75 "Repayment of a wage loss
replacement that was a top-up disability payment": a starting amount, the caller's figure."""

AMT_NON_DEDUCTIBLE_OFFICE_EXPENSES = CATALOG.declare(
    "amt_non_deductible_office_expenses", Decimal, non_negative=True
)
"""Non-deductible office and employment expenses, Form T691 Part 1 line 76 "Add lines 70 to 75."
"67926 =": lines 70 to 75 added."""

AMT_OFFICE_EXPENSES_ADJUSTMENT = CATALOG.declare("amt_office_expenses_adjustment", Decimal)
"""Office and employment expenses adjustment, Form T691 Part 1 line 77 "Line 69 minus line 76": the
other employment expenses (line 22900 of the return) less line 76, a loss in brackets."""

AMT_ADJUSTMENTS_BEFORE_RATE_TOTAL = CATALOG.declare("amt_adjustments_before_rate_total", Decimal)
"""Adjustments before the applicable rate, Form T691 Part 1 line 78 "Add lines 63, 68, and 77.":
lines 63, 68 and 77 in line order, a loss in brackets when line 63 or 77 is one."""

AMT_APPLICABLE_RATE_AMOUNT = CATALOG.declare("amt_applicable_rate_amount", Decimal)
"""Applicable rate amount, Form T691 Part 1 line 80 "Line 78 multiply by the percentage from line
79": line 78 times the applicable rate of line 79 "Applicable Rate" "× 50%" from its dataset,
rounded to the cent, a loss in brackets when line 78 is one."""
