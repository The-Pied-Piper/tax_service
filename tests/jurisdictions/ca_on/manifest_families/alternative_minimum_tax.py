"""The CA-ON manifest entries of one family of lines (see `test_manifest.py`)."""

from __future__ import annotations

from app.domain.capabilities.apply_fraction import ApplyFraction
from app.domain.capabilities.apply_rate import ApplyRate
from app.domain.capabilities.at_most import AtMost
from app.domain.capabilities.credit_amount import CreditAmount
from app.domain.capabilities.lesser_of import LesserOf
from app.domain.capabilities.subtract import Subtract
from app.domain.capabilities.subtract_not_below_zero import SubtractNotBelowZero
from app.domain.capabilities.sum import Sum
from app.domain.manifest import CapabilitySelection
from app.jurisdictions.ca.capabilities.sign_chosen_difference import SignChosenDifference
from app.jurisdictions.ca.catalog import (
    AMT_ADJUSTED_INCOME_WITH_GAINS,
    AMT_ADJUSTED_INCOME_WITH_SECURITY_OPTIONS,
    AMT_ADJUSTED_TAXABLE_INCOME,
    AMT_ADJUSTMENTS_AFTER_RATE_TOTAL,
    AMT_ADJUSTMENTS_BEFORE_RATE_TOTAL,
    AMT_ADJUSTMENTS_WITH_LIFETIME_EXEMPTION_TOTAL,
    AMT_AMOUNT_A_MINUS_AMOUNT_B,
    AMT_APPLICABLE_RATE_AMOUNT,
    AMT_BASIC_EXEMPTION,
    AMT_BASIC_FEDERAL_TAX,
    AMT_CAPITAL_GAINS_ADDED,
    AMT_CAPITAL_GAINS_ADJUSTMENTS,
    AMT_CAPITAL_GAINS_DEDUCTIONS_TOTAL,
    AMT_CAPITAL_GAINS_DIFFERENCE,
    AMT_CLASS_43_1_INCOME,
    AMT_COMMISSION_EMPLOYMENT_EXPENSES,
    AMT_CREDITS_ADJUSTMENTS_TOTAL,
    AMT_CREDITS_TOTAL,
    AMT_DEDUCTIONS_TOTAL,
    AMT_DEFERRED_PROFIT_SHARING_PLAN_DEDUCTION,
    AMT_DIVIDENDS_ADJUSTMENTS_TOTAL,
    AMT_DIVIDENDS_DIFFERENCE_ADJUSTMENT,
    AMT_DIVIDENDS_OTHER_THAN_ELIGIBLE_ADJUSTMENT,
    AMT_DONATIONS_AND_GIFTS_ADJUSTMENT,
    AMT_EXCESS_EPSP_AMOUNTS,
    AMT_FEDERAL_LOGGING_TAX_CREDIT,
    AMT_FILM_PROPERTY_ADJUSTMENT,
    AMT_FILM_PROPERTY_CCA_AND_CARRYING_CHARGES,
    AMT_FILM_PROPERTY_INCOME_BEFORE_CCA,
    AMT_FINANCING_EXPENSES,
    AMT_FORFEITED_SALARY_DEFERRAL_AMOUNTS,
    AMT_GRADUATED_RATE_ESTATE_CAPITAL_GAINS,
    AMT_GROSS_MINIMUM_AMOUNT,
    AMT_INVESTMENT_COUNSEL_FEES,
    AMT_LEGAL_AND_ACCOUNTING_EXPENSES,
    AMT_LIFE_INSURANCE_PREMIUMS_AS_COLLATERAL,
    AMT_LIFETIME_EXEMPTION_ADJUSTMENT,
    AMT_LIMITED_PARTNER_CARRYING_CHARGES,
    AMT_LIMITED_PARTNERSHIP_DIFFERENCE_APPLIED,
    AMT_LIMITED_PARTNERSHIP_DIFFERENCE_ELECTION,
    AMT_LIMITED_PARTNERSHIP_DIFFERENCE_NO_ELECTION,
    AMT_LIMITED_PARTNERSHIP_LOSSES_ADJUSTMENT,
    AMT_LOSSES_AND_DEDUCTIONS_SUBTOTAL,
    AMT_MAXIMUM_CARRYOVER_APPLIED,
    AMT_MAXIMUM_CARRYOVER_CLAIM,
    AMT_MINIMUM_AMOUNT,
    AMT_MINIMUM_TAX_CARRYOVER_APPLIED,
    AMT_MINIMUM_TAX_CARRYOVER_CLAIM,
    AMT_MINIMUM_TAX_CARRYOVER_FROM_PREVIOUS_YEARS,
    AMT_MORTGAGE_FORECLOSURE_CAPITAL_GAINS,
    AMT_MOVING_EXPENSES_DEDUCTION,
    AMT_NET_ADJUSTED_TAXABLE_INCOME,
    AMT_NET_CAPITAL_GAINS_AFTER_ADJUSTMENTS,
    AMT_NET_CAPITAL_LOSSES_DIFFERENCE,
    AMT_NON_CAPITAL_LOSSES_ADJUSTMENT,
    AMT_NON_CAPITAL_LOSSES_DIFFERENCE,
    AMT_NON_DEDUCTIBLE_INTEREST,
    AMT_NON_DEDUCTIBLE_OFFICE_EXPENSES,
    AMT_NON_DEDUCTIBLE_PROPERTY_EXPENSES,
    AMT_NON_REFUNDABLE_CREDITS_ADJUSTMENT,
    AMT_OFFICE_EXPENSES_ADJUSTMENT,
    AMT_OTHER_YEARS_LOSSES_TOTAL,
    AMT_PART_1_SUBTOTAL,
    AMT_PPIP_PREMIUMS_DEDUCTION,
    AMT_PROSPECTOR_OR_GRUBSTAKER_DEDUCTION,
    AMT_PUBLICLY_LISTED_GIFTS_ADJUSTMENT,
    AMT_PUBLICLY_LISTED_GIFTS_NET,
    AMT_PUBLICLY_LISTED_GIFTS_T1170_LINE_68231,
    AMT_PUBLICLY_LISTED_GIFTS_TOTAL,
    AMT_QBT_CAPITAL_GAINS_DEDUCTION_DIFFERENCE,
    AMT_QBT_CAPITAL_GAINS_DEDUCTION_DOUBLED,
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
    AMT_SECTION_119_FORMER_RESIDENT_CREDIT,
    AMT_SECURITY_OPTION_GIFTS_DEDUCTION,
    AMT_SECURITY_OPTION_PUBLICLY_LISTED_GIFTS,
    AMT_SECURITY_OPTIONS_AND_LOSSES_TOTAL,
    AMT_SECURITY_OPTIONS_D1_TOTAL,
    AMT_SECURITY_OPTIONS_D_TOTAL,
    AMT_SECURITY_OPTIONS_NET,
    AMT_SPLIT_INCOME_AND_CREDITS_TOTAL,
    AMT_T4_SECURITY_OPTIONS_BOXES_39_AND_91,
    AMT_T4_SECURITY_OPTIONS_BOXES_41_AND_92,
    AMT_T1212_LINE_2_DEFERRED_SECURITY_OPTIONS,
    AMT_TAX_PAYABLE_AFTER_CREDITS,
    AMT_TAX_PAYABLE_BEFORE_MINIMUM_TAX_CARRYOVER,
    AMT_TAX_PAYABLE_WITH_ITC_RECAPTURE,
    AMT_TAX_SHELTER_ADJUSTMENTS,
    AMT_TAX_SHELTER_DEDUCTIBLE_AMOUNTS,
    AMT_TAX_SHELTER_LOSSES,
    AMT_TREATY_EXEMPT_CAPITAL_GAINS,
    CANADIAN_ARMED_FORCES_AND_POLICE_DEDUCTION,
    CAPITAL_GAIN,
    CAPITAL_GAINS_DEDUCTION,
    CHILD_CARE_EXPENSES,
    CLERGY_RESIDENCE_DEDUCTION,
    CPP_DEDUCTION_ON_SELF_EMPLOYMENT_AND_OTHER_EARNINGS,
    CPP_ENHANCED_CONTRIBUTIONS_ON_RETURN,
    CREDIT_AMOUNTS_AT_CREDIT_RATE,
    CREDITS_AGAINST_FEDERAL_TAX,
    DISABILITY_SUPPORTS_DEDUCTION,
    DIVIDEND_TAX_CREDIT,
    DONATIONS_AND_GIFTS_CREDIT,
    FEDERAL_TAX_ON_SPLIT_INCOME,
    FEDERAL_TAX_WITH_SPLIT_INCOME,
    ITC_RECAPTURE,
    LIMITED_PARTNERSHIP_LOSSES_OF_OTHER_YEARS,
    NON_CAPITAL_LOSSES_OF_OTHER_YEARS,
    NON_REFUNDABLE_TAX_CREDITS,
    NORTHERN_RESIDENTS_DEDUCTIONS,
    OTHER_EMPLOYMENT_EXPENSES,
    OTHER_FORECLOSURE_GAIN_OR_LOSS,
    QBT_CAPITAL_GAINS_DEDUCTION,
    QFFP_FORECLOSURE_GAIN_OR_LOSS,
    TAXABLE_CAPITAL_GAINS,
    TAXABLE_DIVIDENDS,
    TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
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
        "ca/amt_federal_logging_tax_credit",
        "ca/amt_section_119_former_resident_credit",
        "ca/amt_minimum_tax_carryover_from_previous_years",
        "ca/amt_minimum_tax_carryover_claim",
    }
)

OUTPUTS = frozenset(
    {
        "ca/amt_basic_federal_tax",
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
    # Part 1 line 22 "Line 20 minus line 21 (if negative, do not show in brackets.)", line 21 the
    # amount from line 12700 of the return (the taxable capital gains), left signed here.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/amt_net_capital_gains_after_adjustments",
            "less": "ca/taxable_capital_gains",
        },
        produces={"output": "ca/amt_capital_gains_difference"},
    ),
    # Part 1 line 23 "If line 20 is positive, enter the amount from line 22. If line 20 is negative,
    # enter whichever is less: the amount from line 21 or line 22 (show in brackets).", picked by
    # the sign of line 20.
    CapabilitySelection(
        name="ca/sign_chosen_difference",
        params={},
        consumes={
            "sign_amount": "ca/amt_net_capital_gains_after_adjustments",
            "reference": "ca/taxable_capital_gains",
            "difference": "ca/amt_capital_gains_difference",
        },
        produces={"output": "ca/amt_capital_gains_added"},
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
    # Part 1 line 27 "Add lines 13, 14, 23, and 26.", line 13 the amount from line 12 and line 14
    # the amount from line 6 of Part 9, in line order.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/amt_part_1_subtotal",
                "ca/amt_resource_property_and_flow_through_shares",
                "ca/amt_capital_gains_added",
                "ca/amt_publicly_listed_gifts_adjustment",
            )
        },
        produces={"output": "ca/amt_adjusted_income_with_gains"},
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
                "ca/cpp_deduction_on_self_employment_and_other_earnings",
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
    # Part 1 line 33 "Line 27 plus line 32".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/amt_adjusted_income_with_gains",
                "ca/amt_security_options_net",
            )
        },
        produces={"output": "ca/amt_adjusted_income_with_security_options"},
    ),
    # Part 1 line 44 "Add lines 34, 38, and 43.", line 34 the amount from line 33, then lines 38
    # and 43, in line order.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/amt_adjusted_income_with_security_options",
                "ca/amt_security_options_d1_total",
                "ca/amt_other_years_losses_total",
            )
        },
        produces={"output": "ca/amt_security_options_and_losses_total"},
    ),
    # Part 1 line 82 "Line 80 plus line 81", line 81 the amount from line 44 ("Enter the amount
    # from line 44.").
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/amt_applicable_rate_amount",
                "ca/amt_security_options_and_losses_total",
            )
        },
        produces={"output": "ca/amt_adjustments_after_rate_total"},
    ),
    # Part 1 line 84 "B × 13.0435%", B the taxable dividends other than eligible of line 12010
    # of the return, the printed rate from its dataset.
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/amt_dividends_other_than_eligible_rate"},
        consumes={"base": "ca/taxable_dividends_other_than_eligible"},
        produces={"output": "ca/amt_dividends_other_than_eligible_adjustment"},
    ),
    # Part 1 "Amount A minus Amount B", A the taxable dividends of line 12000 of the return and B
    # the amount of line 12010 of the return.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/taxable_dividends",
            "less": "ca/taxable_dividends_other_than_eligible",
        },
        produces={"output": "ca/amt_amount_a_minus_amount_b"},
    ),
    # Part 1 line 85 "C × 27.5362%", C the amount A minus amount B, the printed rate from its
    # dataset.
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/amt_dividends_difference_rate"},
        consumes={"base": "ca/amt_amount_a_minus_amount_b"},
        produces={"output": "ca/amt_dividends_difference_adjustment"},
    ),
    # Part 1 line 86 "Line 84 plus line 85".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/amt_dividends_other_than_eligible_adjustment",
                "ca/amt_dividends_difference_adjustment",
            )
        },
        produces={"output": "ca/amt_dividends_adjustments_total"},
    ),
    # Part 1 line 87 "Enter the amount from line 25400 of your return" "× 40% =", the lifetime
    # capital gains exemption, the printed rate from its dataset.
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/amt_lifetime_exemption_rate"},
        consumes={"base": "ca/capital_gains_deduction"},
        produces={"output": "ca/amt_lifetime_exemption_adjustment"},
    ),
    # Part 1 line 88 "Line 86 plus line 87".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/amt_dividends_adjustments_total",
                "ca/amt_lifetime_exemption_adjustment",
            )
        },
        produces={"output": "ca/amt_adjustments_with_lifetime_exemption_total"},
    ),
    # Part 1 line 89 "Amount from line 25395 of your return" "× 2 =", the amount from line 25395
    # of the return doubled, the printed 2 a fraction, 2/1, as it is above one.
    CapabilitySelection(
        name="core/apply_fraction",
        params={"fraction": "ca/amt_qbt_capital_gains_deduction_multiplier"},
        consumes={"base": "ca/qbt_capital_gains_deduction"},
        produces={"output": "ca/amt_qbt_capital_gains_deduction_doubled"},
    ),
    # Part 1 line 91 "line 89 minus line 90", line 90 the amount from line 25395 of your return.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/amt_qbt_capital_gains_deduction_doubled",
            "less": "ca/qbt_capital_gains_deduction",
        },
        produces={"output": "ca/amt_qbt_capital_gains_deduction_difference"},
    ),
    # Part 1 line 92 "Line 88 plus line 91".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/amt_adjustments_with_lifetime_exemption_total",
                "ca/amt_qbt_capital_gains_deduction_difference",
            )
        },
        produces={"output": "ca/amt_capital_gains_deductions_total"},
    ),
    # Part 1 line 93 "Line 83 minus line 92 (if negative, enter "0")", "Adjusted taxable income",
    # line 83 the amount from line 82 of the previous page.
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/amt_adjustments_after_rate_total",
            "less": "ca/amt_capital_gains_deductions_total",
        },
        produces={"output": "ca/amt_adjusted_taxable_income"},
    ),
    # Part 1 line 94 "Basic exemption" 177,882.00, a printed amount from its dataset.
    CapabilitySelection(
        name="core/credit_amount",
        params={"amount": "ca/amt_basic_exemption"},
        consumes={},
        produces={"output": "ca/amt_basic_exemption"},
    ),
    # Part 1 line 95 "Line 93 minus line 94 (if negative, enter "0")", "Net adjusted taxable
    # income".
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/amt_adjusted_taxable_income",
            "less": "ca/amt_basic_exemption",
        },
        produces={"output": "ca/amt_net_adjusted_taxable_income"},
    ),
    # Part 1 line 97 "Gross minimum amount: line 95 multiplied by the percentage on line 96.", the
    # federal tax rate of line 96, 20.5%, from its dataset.
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/amt_federal_tax_rate"},
        consumes={"base": "ca/amt_net_adjusted_taxable_income"},
        produces={"output": "ca/amt_gross_minimum_amount"},
    ),
    # Part 1 line 98 "Net non-refundable tax credits (line 33800 of your return)" "× 50% =".
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/amt_non_refundable_credits_rate"},
        consumes={"base": "ca/credit_amounts_at_credit_rate"},
        produces={"output": "ca/amt_non_refundable_credits_adjustment"},
    ),
    # Part 1 line 99 "Donations and gifts (line 34900 of your return)" "× 80% =".
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/amt_donations_and_gifts_rate"},
        consumes={"base": "ca/donations_and_gifts_credit"},
        produces={"output": "ca/amt_donations_and_gifts_adjustment"},
    ),
    # Part 1 line 102 "Add lines 98 to 101.", lines 100 and 101 the caller's amounts.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/amt_non_refundable_credits_adjustment",
                "ca/amt_donations_and_gifts_adjustment",
                "ca/amt_federal_logging_tax_credit",
                "ca/amt_section_119_former_resident_credit",
            )
        },
        produces={"output": "ca/amt_credits_adjustments_total"},
    ),
    # Part 1 line 103 "Line 97 minus line 102 (if negative, enter "0")", "Minimum amount".
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/amt_gross_minimum_amount",
            "less": "ca/amt_credits_adjustments_total",
        },
        produces={"output": "ca/amt_minimum_amount"},
    ),
    # Part 2 line 4 "Line 2 plus line 3": line 2 "Total non-refundable tax credits (line 35000 of
    # your return)" and line 3 "Dividend tax credit (line 40425 of your return)", in line order.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/non_refundable_tax_credits", "ca/dividend_tax_credit")},
        produces={"output": "ca/amt_credits_total"},
    ),
    # Part 2 line 5 "Line 1 minus line 4" "Tax payable before minimum tax carryover": line 1 is
    # "Enter the amount from line 40400 of your return", the federal tax with split income, less
    # line 4. The form shows no floor, so the difference may be negative.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/federal_tax_with_split_income",
            "less": "ca/amt_credits_total",
        },
        produces={"output": "ca/amt_tax_payable_before_minimum_tax_carryover"},
    ),
    # Part 2 line 7 "Line 5 minus line 6" "Basic federal tax": line 6 "Minimum tax carryover applied
    # in 2025 from line 12 of Part 8", the claim of Part 8 line 12, less line 5.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/amt_tax_payable_before_minimum_tax_carryover",
            "less": "ca/amt_minimum_tax_carryover_applied",
        },
        produces={"output": "ca/amt_basic_federal_tax"},
    ),
    # Part 8 line 4 "Line 2 plus line 3": line 2 "Tax payable before minimum tax carryover from line
    # 5 of Part 2" and line 3 "Recapture of investment tax credit from line 3 of Part C of Form
    # T2038(IND)", in line order.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/amt_tax_payable_before_minimum_tax_carryover",
                "ca/itc_recapture",
            )
        },
        produces={"output": "ca/amt_tax_payable_with_itc_recapture"},
    ),
    # Part 8 line 8 "Add lines 5 to 7": line 5 "Federal tax on split income from line 8 of Form
    # T1206", line 6 "Federal logging tax credit" (the caller's amount, as on Part 1 line 100) and
    # line 7 "Amount from line 41600 of your return", in line order.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/federal_tax_on_split_income",
                "ca/amt_federal_logging_tax_credit",
                "ca/credits_against_federal_tax",
            )
        },
        produces={"output": "ca/amt_split_income_and_credits_total"},
    ),
    # Part 8 line 9 "Line 4 minus line 8": the form shows no floor, so the difference may be
    # negative.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/amt_tax_payable_with_itc_recapture",
            "less": "ca/amt_split_income_and_credits_total",
        },
        produces={"output": "ca/amt_tax_payable_after_credits"},
    ),
    # Part 8 line 11 "Maximum carryover that can be applied in 2025: line 9 minus line 10 (if
    # negative, enter "0")", line 10 "Minimum amount from line 103 of Part 1".
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/amt_tax_payable_after_credits",
            "less": "ca/amt_minimum_amount",
        },
        produces={"output": "ca/amt_maximum_carryover_applied"},
    ),
    # Part 8 line 12 "Claim an amount that is not more than line 1 or 11, whichever is less.": the
    # cap on the claim, the lesser of line 1 "Minimum tax carryover from previous years (2018 to
    # 2024)" and line 11. Not printed on the form, it is the bound of the claim below.
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={
            "amounts": (
                "ca/amt_minimum_tax_carryover_from_previous_years",
                "ca/amt_maximum_carryover_applied",
            )
        },
        produces={"output": "ca/amt_maximum_carryover_claim"},
    ),
    # Part 8 line 12 "Enter this amount on line 40427 of your return.": the claim, an election the
    # filer makes, which may not be more than the cap; it is refused above it.
    CapabilitySelection(
        name="core/at_most",
        params={},
        consumes={
            "amount": "ca/amt_minimum_tax_carryover_claim",
            "bound": "ca/amt_maximum_carryover_claim",
        },
        produces={"output": "ca/amt_minimum_tax_carryover_applied"},
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
        frozenset({AMT_NET_CAPITAL_GAINS_AFTER_ADJUSTMENTS, TAXABLE_CAPITAL_GAINS}),
        frozenset({AMT_CAPITAL_GAINS_DIFFERENCE}),
    ),
    (
        SignChosenDifference,
        frozenset(
            {
                AMT_NET_CAPITAL_GAINS_AFTER_ADJUSTMENTS,
                TAXABLE_CAPITAL_GAINS,
                AMT_CAPITAL_GAINS_DIFFERENCE,
            }
        ),
        frozenset({AMT_CAPITAL_GAINS_ADDED}),
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
            {
                AMT_PART_1_SUBTOTAL,
                AMT_RESOURCE_PROPERTY_AND_FLOW_THROUGH_SHARES,
                AMT_CAPITAL_GAINS_ADDED,
                AMT_PUBLICLY_LISTED_GIFTS_ADJUSTMENT,
            }
        ),
        frozenset({AMT_ADJUSTED_INCOME_WITH_GAINS}),
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
                CPP_DEDUCTION_ON_SELF_EMPLOYMENT_AND_OTHER_EARNINGS,
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
    (
        Sum,
        frozenset({AMT_ADJUSTED_INCOME_WITH_GAINS, AMT_SECURITY_OPTIONS_NET}),
        frozenset({AMT_ADJUSTED_INCOME_WITH_SECURITY_OPTIONS}),
    ),
    (
        Sum,
        frozenset(
            {
                AMT_ADJUSTED_INCOME_WITH_SECURITY_OPTIONS,
                AMT_SECURITY_OPTIONS_D1_TOTAL,
                AMT_OTHER_YEARS_LOSSES_TOTAL,
            }
        ),
        frozenset({AMT_SECURITY_OPTIONS_AND_LOSSES_TOTAL}),
    ),
    (
        Sum,
        frozenset({AMT_APPLICABLE_RATE_AMOUNT, AMT_SECURITY_OPTIONS_AND_LOSSES_TOTAL}),
        frozenset({AMT_ADJUSTMENTS_AFTER_RATE_TOTAL}),
    ),
    (
        ApplyRate,
        frozenset({TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE}),
        frozenset({AMT_DIVIDENDS_OTHER_THAN_ELIGIBLE_ADJUSTMENT}),
    ),
    (
        Subtract,
        frozenset({TAXABLE_DIVIDENDS, TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE}),
        frozenset({AMT_AMOUNT_A_MINUS_AMOUNT_B}),
    ),
    (
        ApplyRate,
        frozenset({AMT_AMOUNT_A_MINUS_AMOUNT_B}),
        frozenset({AMT_DIVIDENDS_DIFFERENCE_ADJUSTMENT}),
    ),
    (
        Sum,
        frozenset(
            {AMT_DIVIDENDS_OTHER_THAN_ELIGIBLE_ADJUSTMENT, AMT_DIVIDENDS_DIFFERENCE_ADJUSTMENT}
        ),
        frozenset({AMT_DIVIDENDS_ADJUSTMENTS_TOTAL}),
    ),
    (
        ApplyRate,
        frozenset({CAPITAL_GAINS_DEDUCTION}),
        frozenset({AMT_LIFETIME_EXEMPTION_ADJUSTMENT}),
    ),
    (
        Sum,
        frozenset({AMT_DIVIDENDS_ADJUSTMENTS_TOTAL, AMT_LIFETIME_EXEMPTION_ADJUSTMENT}),
        frozenset({AMT_ADJUSTMENTS_WITH_LIFETIME_EXEMPTION_TOTAL}),
    ),
    (
        ApplyFraction,
        frozenset({QBT_CAPITAL_GAINS_DEDUCTION}),
        frozenset({AMT_QBT_CAPITAL_GAINS_DEDUCTION_DOUBLED}),
    ),
    (
        Subtract,
        frozenset({AMT_QBT_CAPITAL_GAINS_DEDUCTION_DOUBLED, QBT_CAPITAL_GAINS_DEDUCTION}),
        frozenset({AMT_QBT_CAPITAL_GAINS_DEDUCTION_DIFFERENCE}),
    ),
    (
        Sum,
        frozenset(
            {
                AMT_ADJUSTMENTS_WITH_LIFETIME_EXEMPTION_TOTAL,
                AMT_QBT_CAPITAL_GAINS_DEDUCTION_DIFFERENCE,
            }
        ),
        frozenset({AMT_CAPITAL_GAINS_DEDUCTIONS_TOTAL}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({AMT_ADJUSTMENTS_AFTER_RATE_TOTAL, AMT_CAPITAL_GAINS_DEDUCTIONS_TOTAL}),
        frozenset({AMT_ADJUSTED_TAXABLE_INCOME}),
    ),
    (
        CreditAmount,
        frozenset({}),
        frozenset({AMT_BASIC_EXEMPTION}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({AMT_ADJUSTED_TAXABLE_INCOME, AMT_BASIC_EXEMPTION}),
        frozenset({AMT_NET_ADJUSTED_TAXABLE_INCOME}),
    ),
    (
        ApplyRate,
        frozenset({AMT_NET_ADJUSTED_TAXABLE_INCOME}),
        frozenset({AMT_GROSS_MINIMUM_AMOUNT}),
    ),
    (
        ApplyRate,
        frozenset({CREDIT_AMOUNTS_AT_CREDIT_RATE}),
        frozenset({AMT_NON_REFUNDABLE_CREDITS_ADJUSTMENT}),
    ),
    (
        ApplyRate,
        frozenset({DONATIONS_AND_GIFTS_CREDIT}),
        frozenset({AMT_DONATIONS_AND_GIFTS_ADJUSTMENT}),
    ),
    (
        Sum,
        frozenset(
            {
                AMT_NON_REFUNDABLE_CREDITS_ADJUSTMENT,
                AMT_DONATIONS_AND_GIFTS_ADJUSTMENT,
                AMT_FEDERAL_LOGGING_TAX_CREDIT,
                AMT_SECTION_119_FORMER_RESIDENT_CREDIT,
            }
        ),
        frozenset({AMT_CREDITS_ADJUSTMENTS_TOTAL}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({AMT_GROSS_MINIMUM_AMOUNT, AMT_CREDITS_ADJUSTMENTS_TOTAL}),
        frozenset({AMT_MINIMUM_AMOUNT}),
    ),
    (
        Sum,
        frozenset({NON_REFUNDABLE_TAX_CREDITS, DIVIDEND_TAX_CREDIT}),
        frozenset({AMT_CREDITS_TOTAL}),
    ),
    (
        Subtract,
        frozenset({FEDERAL_TAX_WITH_SPLIT_INCOME, AMT_CREDITS_TOTAL}),
        frozenset({AMT_TAX_PAYABLE_BEFORE_MINIMUM_TAX_CARRYOVER}),
    ),
    (
        Subtract,
        frozenset(
            {AMT_TAX_PAYABLE_BEFORE_MINIMUM_TAX_CARRYOVER, AMT_MINIMUM_TAX_CARRYOVER_APPLIED}
        ),
        frozenset({AMT_BASIC_FEDERAL_TAX}),
    ),
    (
        Sum,
        frozenset({AMT_TAX_PAYABLE_BEFORE_MINIMUM_TAX_CARRYOVER, ITC_RECAPTURE}),
        frozenset({AMT_TAX_PAYABLE_WITH_ITC_RECAPTURE}),
    ),
    (
        Sum,
        frozenset(
            {
                FEDERAL_TAX_ON_SPLIT_INCOME,
                AMT_FEDERAL_LOGGING_TAX_CREDIT,
                CREDITS_AGAINST_FEDERAL_TAX,
            }
        ),
        frozenset({AMT_SPLIT_INCOME_AND_CREDITS_TOTAL}),
    ),
    (
        Subtract,
        frozenset({AMT_TAX_PAYABLE_WITH_ITC_RECAPTURE, AMT_SPLIT_INCOME_AND_CREDITS_TOTAL}),
        frozenset({AMT_TAX_PAYABLE_AFTER_CREDITS}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({AMT_TAX_PAYABLE_AFTER_CREDITS, AMT_MINIMUM_AMOUNT}),
        frozenset({AMT_MAXIMUM_CARRYOVER_APPLIED}),
    ),
    (
        LesserOf,
        frozenset({AMT_MINIMUM_TAX_CARRYOVER_FROM_PREVIOUS_YEARS, AMT_MAXIMUM_CARRYOVER_APPLIED}),
        frozenset({AMT_MAXIMUM_CARRYOVER_CLAIM}),
    ),
    (
        AtMost,
        frozenset({AMT_MINIMUM_TAX_CARRYOVER_CLAIM, AMT_MAXIMUM_CARRYOVER_CLAIM}),
        frozenset({AMT_MINIMUM_TAX_CARRYOVER_APPLIED}),
    ),
}
