"""The CA-ON manifest entries of one family of lines (see `test_manifest.py`)."""

from __future__ import annotations

from app.domain.capabilities.apply_rate import ApplyRate
from app.domain.capabilities.subtract import Subtract
from app.domain.capabilities.subtract_not_below_zero import SubtractNotBelowZero
from app.domain.capabilities.sum import Sum
from app.domain.manifest import CapabilitySelection
from app.jurisdictions.ca.catalog import (
    AMT_ADJUSTMENTS_BEFORE_RATE_TOTAL,
    AMT_APPLICABLE_RATE_AMOUNT,
    AMT_CAPITAL_GAINS_ADJUSTMENTS,
    AMT_CLASS_43_1_INCOME,
    AMT_COMMISSION_EMPLOYMENT_EXPENSES,
    AMT_DEDUCTIONS_TOTAL,
    AMT_DEFERRED_PROFIT_SHARING_PLAN_DEDUCTION,
    AMT_EXCESS_EPSP_AMOUNTS,
    AMT_FILM_PROPERTY_ADJUSTMENT,
    AMT_FILM_PROPERTY_CCA_AND_CARRYING_CHARGES,
    AMT_FILM_PROPERTY_INCOME_BEFORE_CCA,
    AMT_FINANCING_EXPENSES,
    AMT_FORFEITED_SALARY_DEFERRAL_AMOUNTS,
    AMT_GRADUATED_RATE_ESTATE_CAPITAL_GAINS,
    AMT_INVESTMENT_COUNSEL_FEES,
    AMT_LEGAL_AND_ACCOUNTING_EXPENSES,
    AMT_LIFE_INSURANCE_PREMIUMS_AS_COLLATERAL,
    AMT_LIMITED_PARTNER_CARRYING_CHARGES,
    AMT_LIMITED_PARTNERSHIP_DIFFERENCE_APPLIED,
    AMT_LIMITED_PARTNERSHIP_DIFFERENCE_ELECTION,
    AMT_LIMITED_PARTNERSHIP_DIFFERENCE_NO_ELECTION,
    AMT_LIMITED_PARTNERSHIP_LOSSES_ADJUSTMENT,
    AMT_LOSSES_AND_DEDUCTIONS_SUBTOTAL,
    AMT_MORTGAGE_FORECLOSURE_CAPITAL_GAINS,
    AMT_MOVING_EXPENSES_DEDUCTION,
    AMT_NET_CAPITAL_GAINS_AFTER_ADJUSTMENTS,
    AMT_NET_CAPITAL_LOSSES_DIFFERENCE,
    AMT_NON_CAPITAL_LOSSES_ADJUSTMENT,
    AMT_NON_CAPITAL_LOSSES_DIFFERENCE,
    AMT_NON_DEDUCTIBLE_INTEREST,
    AMT_NON_DEDUCTIBLE_OFFICE_EXPENSES,
    AMT_NON_DEDUCTIBLE_PROPERTY_EXPENSES,
    AMT_OFFICE_EXPENSES_ADJUSTMENT,
    AMT_OTHER_YEARS_LOSSES_TOTAL,
    AMT_PART_1_SUBTOTAL,
    AMT_PPIP_PREMIUMS_DEDUCTION,
    AMT_PROSPECTOR_OR_GRUBSTAKER_DEDUCTION,
    AMT_PUBLICLY_LISTED_GIFTS_ADJUSTMENT,
    AMT_PUBLICLY_LISTED_GIFTS_NET,
    AMT_PUBLICLY_LISTED_GIFTS_T1170_LINE_68231,
    AMT_PUBLICLY_LISTED_GIFTS_TOTAL,
    AMT_RENTAL_PROPERTY_ADJUSTMENT,
    AMT_RENTAL_PROPERTY_CCA_AND_CARRYING_CHARGES,
    AMT_RENTAL_PROPERTY_INCOME_BEFORE_CCA,
    AMT_REPAYMENT_OF_SALARY_AND_WAGES,
    AMT_REPAYMENT_OF_WAGE_LOSS_REPLACEMENT,
    AMT_RESOURCE_EXPENDITURES,
    AMT_RESOURCE_FOREIGN_PROPERTY_INCOME,
    AMT_RESOURCE_INCOME_TOTAL,
    AMT_RESOURCE_PRODUCTION_INCOME,
    AMT_RESOURCE_PROPERTY_AND_FLOW_THROUGH_SHARES,
    AMT_SECURITY_OPTION_GIFTS_DEDUCTION,
    AMT_SECURITY_OPTION_PUBLICLY_LISTED_GIFTS,
    AMT_SECURITY_OPTIONS_D1_TOTAL,
    AMT_SECURITY_OPTIONS_D_TOTAL,
    AMT_SECURITY_OPTIONS_NET,
    AMT_T4_SECURITY_OPTIONS_BOXES_39_AND_91,
    AMT_T4_SECURITY_OPTIONS_BOXES_41_AND_92,
    AMT_T1212_LINE_2_DEFERRED_SECURITY_OPTIONS,
    AMT_TAX_SHELTER_ADJUSTMENTS,
    AMT_TAX_SHELTER_DEDUCTIBLE_AMOUNTS,
    AMT_TAX_SHELTER_LOSSES,
    AMT_TREATY_EXEMPT_CAPITAL_GAINS,
    CANADIAN_ARMED_FORCES_AND_POLICE_DEDUCTION,
    CAPITAL_GAIN,
    CHILD_CARE_EXPENSES,
    CLERGY_RESIDENCE_DEDUCTION,
    CPP_DEDUCTION_ON_SELF_EMPLOYMENT,
    CPP_ENHANCED_CONTRIBUTIONS_ON_RETURN,
    DISABILITY_SUPPORTS_DEDUCTION,
    LIMITED_PARTNERSHIP_LOSSES_OF_OTHER_YEARS,
    NON_CAPITAL_LOSSES_OF_OTHER_YEARS,
    NORTHERN_RESIDENTS_DEDUCTIONS,
    OTHER_EMPLOYMENT_EXPENSES,
    OTHER_FORECLOSURE_GAIN_OR_LOSS,
    QFFP_FORECLOSURE_GAIN_OR_LOSS,
    TAXABLE_INCOME,
    UNION_DUES,
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
        "ca/amt_t4_security_options_boxes_39_and_91",
        "ca/amt_t1212_line_2_deferred_security_options",
        "ca/amt_security_option_publicly_listed_gifts",
        "ca/amt_t4_security_options_boxes_41_and_92",
        "ca/amt_prospector_or_grubstaker_deduction",
        "ca/amt_deferred_profit_sharing_plan_deduction",
        "ca/amt_limited_partnership_difference_no_election",
        "ca/amt_limited_partnership_difference_election",
        "ca/amt_non_capital_losses_difference",
        "ca/amt_net_capital_losses_difference",
        "ca/amt_moving_expenses_deduction",
        "ca/amt_ppip_premiums_deduction",
        "ca/amt_non_deductible_interest",
        "ca/amt_life_insurance_premiums_as_collateral",
        "ca/amt_financing_expenses",
        "ca/amt_investment_counsel_fees",
        "ca/amt_commission_employment_expenses",
        "ca/amt_legal_and_accounting_expenses",
        "ca/amt_repayment_of_salary_and_wages",
        "ca/amt_excess_epsp_amounts",
        "ca/amt_forfeited_salary_deferral_amounts",
        "ca/amt_repayment_of_wage_loss_replacement",
    }
)

OUTPUTS = frozenset(
    {
        "ca/amt_part_1_subtotal",
        "ca/amt_resource_property_and_flow_through_shares",
        "ca/amt_net_capital_gains_after_adjustments",
        "ca/amt_publicly_listed_gifts_adjustment",
        "ca/amt_security_options_net",
        "ca/amt_security_options_d1_total",
        "ca/amt_other_years_losses_total",
        "ca/amt_applicable_rate_amount",
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
    # Part 1 line 30 "Line 28 plus line 29" and "67910 =", the security options deduction under
    # paragraph 110(1)(d): the T4 slips' boxes 39 and 91 (line 28) and the T1212 amount (line 29).
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/amt_t4_security_options_boxes_39_and_91",
                "ca/amt_t1212_line_2_deferred_security_options",
            )
        },
        produces={"output": "ca/amt_security_options_d_total"},
    ),
    # Part 1 line 31 "× 40%" of "Gifts of publicly listed securities acquired under a security
    # option plan included on line 24900 of your return" "67914", the rate from its dataset.
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/security_option_gifts_rate"},
        consumes={"base": "ca/amt_security_option_publicly_listed_gifts"},
        produces={"output": "ca/amt_security_option_gifts_deduction"},
    ),
    # Part 1 line 32 "Line 30 minus line 31 (if negative, enter "0")", not below zero.
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/amt_security_options_d_total",
            "less": "ca/amt_security_option_gifts_deduction",
        },
        produces={"output": "ca/amt_security_options_net"},
    ),
    # Part 1 line 38 "Add lines 35 to 37." and "67918 =", lines 35, 36 and 37 in line order.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/amt_t4_security_options_boxes_41_and_92",
                "ca/amt_prospector_or_grubstaker_deduction",
                "ca/amt_deferred_profit_sharing_plan_deduction",
            )
        },
        produces={"output": "ca/amt_security_options_d1_total"},
    ),
    # Part 1 line 43 "Line 39 or 40, as applicable, plus line 41 and 42", the one of lines 39 and 40
    # that applies (the other is blank) with lines 41 and 42, in line order.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/amt_limited_partnership_difference_no_election",
                "ca/amt_limited_partnership_difference_election",
                "ca/amt_non_capital_losses_difference",
                "ca/amt_net_capital_losses_difference",
            )
        },
        produces={"output": "ca/amt_other_years_losses_total"},
    ),
    # Part 1 line 46 "Amount from line 39 or 40, as applicable", the one of lines 39 and 40 that
    # applies.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/amt_limited_partnership_difference_no_election",
                "ca/amt_limited_partnership_difference_election",
            )
        },
        produces={"output": "ca/amt_limited_partnership_difference_applied"},
    ),
    # Part 1 line 47 "Line 45 minus line 46", the limited partnership losses of other years (line
    # 25100 of the return, read from its artifact) less line 46, a loss in brackets.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/limited_partnership_losses_of_other_years",
            "less": "ca/amt_limited_partnership_difference_applied",
        },
        produces={"output": "ca/amt_limited_partnership_losses_adjustment"},
    ),
    # Part 1 line 50 "Line 48 minus line 49", the non-capital losses of other years (line 25200 of
    # the return, read from its artifact) less line 49, the amount from line 41.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/non_capital_losses_of_other_years",
            "less": "ca/amt_non_capital_losses_difference",
        },
        produces={"output": "ca/amt_non_capital_losses_adjustment"},
    ),
    # Part 1 line 53 "Add lines 47, 50, 51, and 52.", line 51 the union dues of line 21200 of the
    # return and line 52 the child care expenses of line 21400, read from their artifacts.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/amt_limited_partnership_losses_adjustment",
                "ca/amt_non_capital_losses_adjustment",
                "ca/union_dues",
                "ca/child_care_expenses",
            )
        },
        produces={"output": "ca/amt_losses_and_deductions_subtotal"},
    ),
    # Part 1 line 63 "Add lines 54 to 62.", line 53 carried and lines 55 to 62 in line order: the
    # deductions of the return on lines 21500, 21900 (a caller's amount), 22200, 22215, 22300 (a
    # caller's amount), 23100, 24400 and 25500.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/amt_losses_and_deductions_subtotal",
                "ca/disability_supports_deduction",
                "ca/amt_moving_expenses_deduction",
                "ca/cpp_deduction_on_self_employment",
                "ca/cpp_enhanced_contributions_on_return",
                "ca/amt_ppip_premiums_deduction",
                "ca/clergy_residence_deduction",
                "ca/canadian_armed_forces_and_police_deduction",
                "ca/northern_residents_deductions",
            )
        },
        produces={"output": "ca/amt_deductions_total"},
    ),
    # Part 1 line 68 "Add lines 64 to 67 (11)", the non-deductible property expenses, lines 64 to 67
    # in line order (caller's amounts).
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/amt_non_deductible_interest",
                "ca/amt_life_insurance_premiums_as_collateral",
                "ca/amt_financing_expenses",
                "ca/amt_investment_counsel_fees",
            )
        },
        produces={"output": "ca/amt_non_deductible_property_expenses"},
    ),
    # Part 1 line 76 "Add lines 70 to 75." and "67926 =", lines 70 to 75 in line order (caller's
    # amounts).
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/amt_commission_employment_expenses",
                "ca/amt_legal_and_accounting_expenses",
                "ca/amt_repayment_of_salary_and_wages",
                "ca/amt_excess_epsp_amounts",
                "ca/amt_forfeited_salary_deferral_amounts",
                "ca/amt_repayment_of_wage_loss_replacement",
            )
        },
        produces={"output": "ca/amt_non_deductible_office_expenses"},
    ),
    # Part 1 line 77 "Line 69 minus line 76", line 69 the other employment expenses of line 22900
    # of the return, read from its artifact, less line 76, a loss in brackets.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/other_employment_expenses",
            "less": "ca/amt_non_deductible_office_expenses",
        },
        produces={"output": "ca/amt_office_expenses_adjustment"},
    ),
    # Part 1 line 78 "Add lines 63, 68, and 77.", lines 63, 68 and 77 in line order.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/amt_deductions_total",
                "ca/amt_non_deductible_property_expenses",
                "ca/amt_office_expenses_adjustment",
            )
        },
        produces={"output": "ca/amt_adjustments_before_rate_total"},
    ),
    # Part 1 line 80 "Line 78 multiply by the percentage from line 79", the applicable rate of
    # line 79 "Applicable Rate" "50%" from its dataset.
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/amt_applicable_rate"},
        consumes={"base": "ca/amt_adjustments_before_rate_total"},
        produces={"output": "ca/amt_applicable_rate_amount"},
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
    (
        Sum,
        frozenset(
            {AMT_T4_SECURITY_OPTIONS_BOXES_39_AND_91, AMT_T1212_LINE_2_DEFERRED_SECURITY_OPTIONS}
        ),
        frozenset({AMT_SECURITY_OPTIONS_D_TOTAL}),
    ),
    (
        ApplyRate,
        frozenset({AMT_SECURITY_OPTION_PUBLICLY_LISTED_GIFTS}),
        frozenset({AMT_SECURITY_OPTION_GIFTS_DEDUCTION}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({AMT_SECURITY_OPTIONS_D_TOTAL, AMT_SECURITY_OPTION_GIFTS_DEDUCTION}),
        frozenset({AMT_SECURITY_OPTIONS_NET}),
    ),
    (
        Sum,
        frozenset(
            {
                AMT_T4_SECURITY_OPTIONS_BOXES_41_AND_92,
                AMT_PROSPECTOR_OR_GRUBSTAKER_DEDUCTION,
                AMT_DEFERRED_PROFIT_SHARING_PLAN_DEDUCTION,
            }
        ),
        frozenset({AMT_SECURITY_OPTIONS_D1_TOTAL}),
    ),
    (
        Sum,
        frozenset(
            {
                AMT_LIMITED_PARTNERSHIP_DIFFERENCE_NO_ELECTION,
                AMT_LIMITED_PARTNERSHIP_DIFFERENCE_ELECTION,
                AMT_NON_CAPITAL_LOSSES_DIFFERENCE,
                AMT_NET_CAPITAL_LOSSES_DIFFERENCE,
            }
        ),
        frozenset({AMT_OTHER_YEARS_LOSSES_TOTAL}),
    ),
    (
        Sum,
        frozenset(
            {
                AMT_LIMITED_PARTNERSHIP_DIFFERENCE_NO_ELECTION,
                AMT_LIMITED_PARTNERSHIP_DIFFERENCE_ELECTION,
            }
        ),
        frozenset({AMT_LIMITED_PARTNERSHIP_DIFFERENCE_APPLIED}),
    ),
    (
        Subtract,
        frozenset(
            {LIMITED_PARTNERSHIP_LOSSES_OF_OTHER_YEARS, AMT_LIMITED_PARTNERSHIP_DIFFERENCE_APPLIED}
        ),
        frozenset({AMT_LIMITED_PARTNERSHIP_LOSSES_ADJUSTMENT}),
    ),
    (
        Subtract,
        frozenset({NON_CAPITAL_LOSSES_OF_OTHER_YEARS, AMT_NON_CAPITAL_LOSSES_DIFFERENCE}),
        frozenset({AMT_NON_CAPITAL_LOSSES_ADJUSTMENT}),
    ),
    (
        Sum,
        frozenset(
            {
                AMT_LIMITED_PARTNERSHIP_LOSSES_ADJUSTMENT,
                AMT_NON_CAPITAL_LOSSES_ADJUSTMENT,
                UNION_DUES,
                CHILD_CARE_EXPENSES,
            }
        ),
        frozenset({AMT_LOSSES_AND_DEDUCTIONS_SUBTOTAL}),
    ),
    (
        Sum,
        frozenset(
            {
                AMT_LOSSES_AND_DEDUCTIONS_SUBTOTAL,
                DISABILITY_SUPPORTS_DEDUCTION,
                AMT_MOVING_EXPENSES_DEDUCTION,
                CPP_DEDUCTION_ON_SELF_EMPLOYMENT,
                CPP_ENHANCED_CONTRIBUTIONS_ON_RETURN,
                AMT_PPIP_PREMIUMS_DEDUCTION,
                CLERGY_RESIDENCE_DEDUCTION,
                CANADIAN_ARMED_FORCES_AND_POLICE_DEDUCTION,
                NORTHERN_RESIDENTS_DEDUCTIONS,
            }
        ),
        frozenset({AMT_DEDUCTIONS_TOTAL}),
    ),
    (
        Sum,
        frozenset(
            {
                AMT_NON_DEDUCTIBLE_INTEREST,
                AMT_LIFE_INSURANCE_PREMIUMS_AS_COLLATERAL,
                AMT_FINANCING_EXPENSES,
                AMT_INVESTMENT_COUNSEL_FEES,
            }
        ),
        frozenset({AMT_NON_DEDUCTIBLE_PROPERTY_EXPENSES}),
    ),
    (
        Sum,
        frozenset(
            {
                AMT_COMMISSION_EMPLOYMENT_EXPENSES,
                AMT_LEGAL_AND_ACCOUNTING_EXPENSES,
                AMT_REPAYMENT_OF_SALARY_AND_WAGES,
                AMT_EXCESS_EPSP_AMOUNTS,
                AMT_FORFEITED_SALARY_DEFERRAL_AMOUNTS,
                AMT_REPAYMENT_OF_WAGE_LOSS_REPLACEMENT,
            }
        ),
        frozenset({AMT_NON_DEDUCTIBLE_OFFICE_EXPENSES}),
    ),
    (
        Subtract,
        frozenset({OTHER_EMPLOYMENT_EXPENSES, AMT_NON_DEDUCTIBLE_OFFICE_EXPENSES}),
        frozenset({AMT_OFFICE_EXPENSES_ADJUSTMENT}),
    ),
    (
        Sum,
        frozenset(
            {
                AMT_DEDUCTIONS_TOTAL,
                AMT_NON_DEDUCTIBLE_PROPERTY_EXPENSES,
                AMT_OFFICE_EXPENSES_ADJUSTMENT,
            }
        ),
        frozenset({AMT_ADJUSTMENTS_BEFORE_RATE_TOTAL}),
    ),
    (
        ApplyRate,
        frozenset({AMT_ADJUSTMENTS_BEFORE_RATE_TOTAL}),
        frozenset({AMT_APPLICABLE_RATE_AMOUNT}),
    ),
}
