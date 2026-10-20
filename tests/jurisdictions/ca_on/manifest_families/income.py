"""The CA-ON manifest entries of one family of lines (see `test_manifest.py`)."""

from __future__ import annotations

from app.domain.capabilities.apply_fraction import ApplyFraction
from app.domain.capabilities.apply_rate import ApplyRate
from app.domain.capabilities.choose_by_count import ChooseByCount
from app.domain.capabilities.subtract import Subtract
from app.domain.capabilities.sum import Sum
from app.domain.manifest import CapabilitySelection
from app.jurisdictions.ca.capabilities.rental_gross_rents import RentalGrossRents
from app.jurisdictions.ca.capabilities.short_term_rental_gross_rents import (
    ShortTermRentalGrossRents,
)
from app.jurisdictions.ca.capabilities.short_term_rental_non_compliant_expenses import (
    ShortTermRentalNonCompliantExpenses,
)
from app.jurisdictions.ca.catalog import (
    BUSINESS_INCOME,
    CAPITAL_GAIN,
    COMMISSION_INCOME,
    CPP_OR_QPP_BENEFITS,
    CREDITS_AGAINST_BASIC_FEDERAL_TAX,
    DIVIDEND_TAX_CREDIT,
    DIVIDENDS_AMOUNT_A,
    DIVIDENDS_AMOUNT_A_LESS_B,
    DIVIDENDS_AMOUNT_B,
    DIVIDENDS_WITHOUT_A_SLIP_GROSSED_UP,
    EI_AND_OTHER_BENEFITS,
    ELECTED_SPLIT_PENSION_AMOUNT,
    ELIGIBLE_DIVIDENDS_CREDIT,
    ELIGIBLE_DIVIDENDS_GROSSED_UP,
    ELIGIBLE_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP,
    EMPLOYMENT_INCOME,
    FARMING_INCOME,
    FHSA_INCOME,
    FISHING_INCOME,
    FOREIGN_INVESTMENT_INCOME,
    GROSS_RENTAL_INCOME,
    INCOME_SUPPORT_BENEFITS,
    INTEREST_AND_OTHER_INVESTMENT_INCOME,
    INVESTMENT_INCOME_BEFORE_PRIOR_YEARS,
    INVESTMENT_INCOME_CREDITED_NOT_RECEIVED,
    INVESTMENT_INCOME_REPORTED_IN_PREVIOUS_YEARS,
    INVESTMENT_INCOME_WITHOUT_A_SLIP,
    INVESTMENT_ROYALTIES,
    NET_FEDERAL_SUPPLEMENTS,
    NET_PARTNERSHIP_INCOME,
    NET_RENTAL_INCOME,
    NET_SELF_EMPLOYMENT_INCOME,
    NO_SLIP_DIVIDEND_TAX_CREDIT,
    NON_REFUNDABLE_TAX_CREDITS,
    OLD_AGE_SECURITY,
    OTHER_DIVIDENDS_CREDIT,
    OTHER_DIVIDENDS_GROSSED_UP,
    OTHER_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP,
    OTHER_EMPLOYMENT_INCOME,
    OTHER_FHSA_INCOME,
    OTHER_INCOME,
    OTHER_PENSIONS_AND_SUPERANNUATION,
    PROFESSIONAL_INCOME,
    RDSP_INCOME,
    RENTAL_ADVERTISING,
    RENTAL_ADVERTISING_PERSONAL_PORTION,
    RENTAL_ADVERTISING_SHORT_TERM_PORTION,
    RENTAL_CCA_CLAIM,
    RENTAL_COOWNER,
    RENTAL_COOWNER_OTHER_EXPENSES,
    RENTAL_COOWNER_SHARE,
    RENTAL_DEDUCTIBLE_EXPENSES,
    RENTAL_EXPENSES_LESS_PERSONAL_PORTION,
    RENTAL_GROSS_RENTS,
    RENTAL_INSURANCE,
    RENTAL_INSURANCE_PERSONAL_PORTION,
    RENTAL_INSURANCE_SHORT_TERM_PORTION,
    RENTAL_INTEREST_AND_BANK_CHARGES,
    RENTAL_INTEREST_AND_BANK_CHARGES_PERSONAL_PORTION,
    RENTAL_INTEREST_AND_BANK_CHARGES_SHORT_TERM_PORTION,
    RENTAL_MANAGEMENT_AND_ADMINISTRATION_FEES,
    RENTAL_MANAGEMENT_AND_ADMINISTRATION_FEES_PERSONAL_PORTION,
    RENTAL_MANAGEMENT_AND_ADMINISTRATION_FEES_SHORT_TERM_PORTION,
    RENTAL_MOTOR_VEHICLE_EXPENSES,
    RENTAL_MOTOR_VEHICLE_EXPENSES_PERSONAL_PORTION,
    RENTAL_MOTOR_VEHICLE_EXPENSES_SHORT_TERM_PORTION,
    RENTAL_NET_INCOME_AFTER_CCA,
    RENTAL_NET_INCOME_AFTER_COOWNER_EXPENSES,
    RENTAL_NET_INCOME_AFTER_TERMINAL_LOSS,
    RENTAL_NET_INCOME_BEFORE_ADJUSTMENTS,
    RENTAL_NET_INCOME_SHARE,
    RENTAL_NET_INCOME_WITH_RECAPTURE,
    RENTAL_NON_COMPLIANT_EXPENSES,
    RENTAL_OFFICE_EXPENSES,
    RENTAL_OFFICE_EXPENSES_PERSONAL_PORTION,
    RENTAL_OFFICE_EXPENSES_SHORT_TERM_PORTION,
    RENTAL_OTHER_EXPENSES,
    RENTAL_OTHER_EXPENSES_PERSONAL_PORTION,
    RENTAL_OTHER_EXPENSES_SHORT_TERM_PORTION,
    RENTAL_OTHER_INCOME,
    RENTAL_PARTNER,
    RENTAL_PARTNER_GST_HST_REBATE,
    RENTAL_PARTNER_OTHER_EXPENSES,
    RENTAL_PARTNER_SHARE,
    RENTAL_PARTNER_SHARE_WITH_REBATE,
    RENTAL_PARTNERSHIP_NET_INCOME,
    RENTAL_PERSONAL_PORTION,
    RENTAL_PROFESSIONAL_FEES,
    RENTAL_PROFESSIONAL_FEES_PERSONAL_PORTION,
    RENTAL_PROFESSIONAL_FEES_SHORT_TERM_PORTION,
    RENTAL_PROPERTIES,
    RENTAL_PROPERTY_TAXES,
    RENTAL_PROPERTY_TAXES_PERSONAL_PORTION,
    RENTAL_PROPERTY_TAXES_SHORT_TERM_PORTION,
    RENTAL_RECAPTURED_CCA,
    RENTAL_REPAIRS_AND_MAINTENANCE,
    RENTAL_REPAIRS_AND_MAINTENANCE_PERSONAL_PORTION,
    RENTAL_REPAIRS_AND_MAINTENANCE_SHORT_TERM_PORTION,
    RENTAL_SALARIES_WAGES_AND_BENEFITS,
    RENTAL_SALARIES_WAGES_AND_BENEFITS_PERSONAL_PORTION,
    RENTAL_SALARIES_WAGES_AND_BENEFITS_SHORT_TERM_PORTION,
    RENTAL_SHORT_TERM_PORTION,
    RENTAL_TERMINAL_LOSS,
    RENTAL_TOTAL_EXPENSES,
    RENTAL_TRAVEL,
    RENTAL_TRAVEL_PERSONAL_PORTION,
    RENTAL_TRAVEL_SHORT_TERM_PORTION,
    RENTAL_UTILITIES,
    RENTAL_UTILITIES_PERSONAL_PORTION,
    RENTAL_UTILITIES_SHORT_TERM_PORTION,
    RRSP_INCOME,
    SHORT_TERM_RENTAL_GROSS_RENTS,
    SHORT_TERM_RENTAL_UNITS,
    SLIP_DIVIDEND_TAX_CREDIT,
    SLIP_TAXABLE_DIVIDENDS,
    SLIP_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
    SOCIAL_ASSISTANCE_PAYMENTS,
    T3_DIVIDEND_TAX_CREDIT,
    T3_INVESTMENT_INCOME,
    T3_TAXABLE_DIVIDENDS,
    T3_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
    T4PS_DIVIDEND_TAX_CREDIT,
    T4PS_TAXABLE_DIVIDENDS,
    T4PS_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
    T5_DIVIDEND_TAX_CREDIT,
    T5_INVESTMENT_INCOME,
    T5_TAXABLE_DIVIDENDS,
    T5_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
    T5013_DIVIDEND_TAX_CREDIT,
    T5013_INVESTMENT_INCOME,
    T5013_TAXABLE_DIVIDENDS,
    T5013_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
    TAX_REFUND_INTEREST,
    TAXABLE_CAPITAL_GAINS,
    TAXABLE_DIVIDENDS,
    TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
    TAXABLE_SCHOLARSHIPS,
    TAXABLE_SUPPORT_PAYMENTS,
    TOTAL_INCOME,
    UNIVERSAL_CHILD_CARE_BENEFIT,
    WORKERS_COMPENSATION_BENEFITS,
)

INPUTS = frozenset(
    {
        "ca/employment_income",
        "ca/capital_gain",
        "ca/other_employment_income",
        "ca/old_age_security",
        "ca/cpp_or_qpp_benefits",
        "ca/other_pensions_and_superannuation",
        "ca/elected_split_pension_amount",
        "ca/universal_child_care_benefit",
        "ca/ei_and_other_benefits",
        "ca/t3_taxable_dividends_other_than_eligible",
        "ca/t4ps_taxable_dividends_other_than_eligible",
        "ca/t5_taxable_dividends_other_than_eligible",
        "ca/t5013_taxable_dividends_other_than_eligible",
        "ca/t3_taxable_dividends",
        "ca/t4ps_taxable_dividends",
        "ca/t5_taxable_dividends",
        "ca/t5013_taxable_dividends",
        "ca/eligible_dividends_received_without_a_slip",
        "ca/other_dividends_received_without_a_slip",
        "ca/t3_dividend_tax_credit",
        "ca/t4ps_dividend_tax_credit",
        "ca/t5_dividend_tax_credit",
        "ca/t5013_dividend_tax_credit",
        "ca/t3_investment_income",
        "ca/t5_investment_income",
        "ca/t5013_investment_income",
        "ca/investment_income_credited_not_received",
        "ca/tax_refund_interest",
        "ca/foreign_investment_income",
        "ca/investment_income_without_a_slip",
        "ca/investment_royalties",
        "ca/investment_income_reported_in_previous_years",
        "ca/net_partnership_income",
        "ca/rdsp_income",
        "ca/rental_properties",
        "ca/rental_other_income",
        "ca/rental_advertising",
        "ca/rental_advertising_personal_portion",
        "ca/rental_advertising_short_term_portion",
        "ca/rental_insurance",
        "ca/rental_insurance_personal_portion",
        "ca/rental_insurance_short_term_portion",
        "ca/rental_interest_and_bank_charges",
        "ca/rental_interest_and_bank_charges_personal_portion",
        "ca/rental_interest_and_bank_charges_short_term_portion",
        "ca/rental_office_expenses",
        "ca/rental_office_expenses_personal_portion",
        "ca/rental_office_expenses_short_term_portion",
        "ca/rental_professional_fees",
        "ca/rental_professional_fees_personal_portion",
        "ca/rental_professional_fees_short_term_portion",
        "ca/rental_management_and_administration_fees",
        "ca/rental_management_and_administration_fees_personal_portion",
        "ca/rental_management_and_administration_fees_short_term_portion",
        "ca/rental_repairs_and_maintenance",
        "ca/rental_repairs_and_maintenance_personal_portion",
        "ca/rental_repairs_and_maintenance_short_term_portion",
        "ca/rental_salaries_wages_and_benefits",
        "ca/rental_salaries_wages_and_benefits_personal_portion",
        "ca/rental_salaries_wages_and_benefits_short_term_portion",
        "ca/rental_property_taxes",
        "ca/rental_property_taxes_personal_portion",
        "ca/rental_property_taxes_short_term_portion",
        "ca/rental_travel",
        "ca/rental_travel_personal_portion",
        "ca/rental_travel_short_term_portion",
        "ca/rental_utilities",
        "ca/rental_utilities_personal_portion",
        "ca/rental_utilities_short_term_portion",
        "ca/rental_motor_vehicle_expenses",
        "ca/rental_motor_vehicle_expenses_personal_portion",
        "ca/rental_motor_vehicle_expenses_short_term_portion",
        "ca/rental_other_expenses",
        "ca/rental_other_expenses_personal_portion",
        "ca/rental_other_expenses_short_term_portion",
        "ca/short_term_rental_units",
        "ca/rental_coowner",
        "ca/rental_coowner_share",
        "ca/rental_coowner_other_expenses",
        "ca/rental_recaptured_cca",
        "ca/rental_terminal_loss",
        "ca/rental_cca_claim",
        "ca/rental_partner",
        "ca/rental_partner_share",
        "ca/rental_partner_gst_hst_rebate",
        "ca/rental_partner_other_expenses",
        "ca/taxable_support_payments",
        "ca/rrsp_income",
        "ca/fhsa_income",
        "ca/other_fhsa_income",
        "ca/other_income",
        "ca/taxable_scholarships",
        "ca/business_income",
        "ca/professional_income",
        "ca/commission_income",
        "ca/farming_income",
        "ca/fishing_income",
        "ca/workers_compensation_benefits",
        "ca/social_assistance_payments",
        "ca/net_federal_supplements",
    }
)

OUTPUTS = frozenset(
    {
        "ca/taxable_dividends_other_than_eligible",
        "ca/short_term_rental_gross_rents",
        "ca/rental_short_term_portion",
    }
)

STEPS = {
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/capital_gains_inclusion_rate"},
        consumes={"base": "ca/capital_gain"},
        produces={"output": "ca/taxable_capital_gains"},
    ),
    # T1 line 9 (12000) "Amount of dividends (eligible and other than eligible)" and line
    # 12010 "Amount of dividends (other than eligible)" (use Federal Worksheet): the Federal
    # Worksheet's "Lines 12000 and 12010 - Taxable amount of dividends from taxable Canadian
    # corporations", line 5 "Add lines 1 to 4. Enter this amount on line 12010 of your
    # return." (the T3, T4PS, T5 and T5013 slip boxes of lines 1 to 4) and line 10 "Add lines
    # 6 to 9. Enter this amount on line 12000 of your return." (lines 6 to 9). For dividends
    # with no information slip, line 11 "Actual amount of eligible dividends received" and
    # line 12 "Applicable rate 138%" give line 13 "Line 11 multiplied by the percentage from
    # line 12"; line 14 "Actual amount of dividends other than eligible dividends received"
    # and line 15 "Applicable rate 115%" give line 16 "Line 14 multiplied by the percentage
    # from line 15 Include this amount on line 12010 of your return."; line 17 "Line 13 plus
    # line 16. Include this amount on line 12000 of your return." The rates are above one, so
    # they are fractions, not rates. Line 12010 is line 5 plus line 16 and line 12000 is line
    # 10 plus line 17.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/t3_taxable_dividends_other_than_eligible",
                "ca/t4ps_taxable_dividends_other_than_eligible",
                "ca/t5_taxable_dividends_other_than_eligible",
                "ca/t5013_taxable_dividends_other_than_eligible",
            )
        },
        produces={"output": "ca/slip_taxable_dividends_other_than_eligible"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/t3_taxable_dividends",
                "ca/t4ps_taxable_dividends",
                "ca/t5_taxable_dividends",
                "ca/t5013_taxable_dividends",
            )
        },
        produces={"output": "ca/slip_taxable_dividends"},
    ),
    CapabilitySelection(
        name="core/apply_fraction",
        params={"fraction": "ca/eligible_dividend_gross_up"},
        consumes={"base": "ca/eligible_dividends_received_without_a_slip"},
        produces={"output": "ca/eligible_dividends_grossed_up"},
    ),
    CapabilitySelection(
        name="core/apply_fraction",
        params={"fraction": "ca/other_dividend_gross_up"},
        consumes={"base": "ca/other_dividends_received_without_a_slip"},
        produces={"output": "ca/other_dividends_grossed_up"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/eligible_dividends_grossed_up", "ca/other_dividends_grossed_up")},
        produces={"output": "ca/dividends_without_a_slip_grossed_up"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/slip_taxable_dividends_other_than_eligible",
                "ca/other_dividends_grossed_up",
            )
        },
        produces={"output": "ca/taxable_dividends_other_than_eligible"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/slip_taxable_dividends", "ca/dividends_without_a_slip_grossed_up")},
        produces={"output": "ca/taxable_dividends"},
    ),
    # T1 Step 2 line 10 (12100) "Interest and other investment income (use Federal
    # Worksheet)": the Federal Worksheet's "Line 12100 - Interest and other investment
    # income" line 9 "Add lines 1 to 8.", in line order, then line 11 "Line 9 minus line
    # 10. Enter this amount on line 12100 of your return." with line 10 "Interest and other
    # investment income, included on line 9, received and reported in previous years".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/t3_investment_income",
                "ca/t5_investment_income",
                "ca/t5013_investment_income",
                "ca/investment_income_credited_not_received",
                "ca/tax_refund_interest",
                "ca/foreign_investment_income",
                "ca/investment_income_without_a_slip",
                "ca/investment_royalties",
            )
        },
        produces={"output": "ca/investment_income_before_prior_years"},
    ),
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/investment_income_before_prior_years",
            "less": "ca/investment_income_reported_in_previous_years",
        },
        produces={"output": "ca/interest_and_other_investment_income"},
    ),
    # T1 line 32 and line 14700 "Add lines 29 to 31 (see line 25000 in Step 4).": workers'
    # compensation benefits (14400), social assistance payments (14500) and net federal
    # supplements paid (14600), in line order.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/workers_compensation_benefits",
                "ca/social_assistance_payments",
                "ca/net_federal_supplements",
            )
        },
        produces={"output": "ca/income_support_benefits"},
    ),
    # T776 Part 3, "Line 8140: Total of your gross rents for short-term rentals in the
    # year you receive them (add amounts under "Gross rents for short-term rentals")":
    # the total of that column of the rental properties, one row for each property; it
    # feeds no other line.
    CapabilitySelection(
        name="ca/short_term_rental_gross_rents",
        params={},
        consumes={"properties": "ca/rental_properties"},
        produces={"output": "ca/short_term_rental_gross_rents"},
    ),
    # T776 Part 3, "Line 8141: Total of all your gross rents in the year you receive
    # them (add lines under "Gross rents for all units")": the total of that column of
    # the rental properties.
    CapabilitySelection(
        name="ca/rental_gross_rents",
        params={},
        consumes={"properties": "ca/rental_properties"},
        produces={"output": "ca/rental_gross_rents"},
    ),
    # T776 "Line 8299: Total gross rental income: Enter this amount on your income tax
    # and benefit return on line 12599 (line 8141 plus line 8230)"; T1 "Line 12599:
    # Gross".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/rental_gross_rents",
                "ca/rental_other_income",
            )
        },
        produces={"output": "ca/gross_rental_income"},
    ),
    # T776 Part 4, "Line A: Total expenses (add amounts listed under "Total expenses")":
    # the 13 expense lines (8521, 8690, 8710, 8810, 8860, 8871, 8960, 9060, 9180, 9200,
    # 9220, 9281 and 9270), in line order.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/rental_advertising",
                "ca/rental_insurance",
                "ca/rental_interest_and_bank_charges",
                "ca/rental_office_expenses",
                "ca/rental_professional_fees",
                "ca/rental_management_and_administration_fees",
                "ca/rental_repairs_and_maintenance",
                "ca/rental_salaries_wages_and_benefits",
                "ca/rental_property_taxes",
                "ca/rental_travel",
                "ca/rental_utilities",
                "ca/rental_motor_vehicle_expenses",
                "ca/rental_other_expenses",
            )
        },
        produces={"output": "ca/rental_total_expenses"},
    ),
    # T776 "Line 9949: Total for personal portion (add amounts listed under "Personal
    # portion of total expenses")": the same 13 expense lines, in line order.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/rental_advertising_personal_portion",
                "ca/rental_insurance_personal_portion",
                "ca/rental_interest_and_bank_charges_personal_portion",
                "ca/rental_office_expenses_personal_portion",
                "ca/rental_professional_fees_personal_portion",
                "ca/rental_management_and_administration_fees_personal_portion",
                "ca/rental_repairs_and_maintenance_personal_portion",
                "ca/rental_salaries_wages_and_benefits_personal_portion",
                "ca/rental_property_taxes_personal_portion",
                "ca/rental_travel_personal_portion",
                "ca/rental_utilities_personal_portion",
                "ca/rental_motor_vehicle_expenses_personal_portion",
                "ca/rental_other_expenses_personal_portion",
            )
        },
        produces={"output": "ca/rental_personal_portion"},
    ),
    # T776 "Line 9365: Total for short-term rental portion (add amounts listed under
    # "Short-term rental portion of total expenses")": the same 13 expense lines, in
    # line order; it feeds no other line (Chart A's column 3 is a starting amount).
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/rental_advertising_short_term_portion",
                "ca/rental_insurance_short_term_portion",
                "ca/rental_interest_and_bank_charges_short_term_portion",
                "ca/rental_office_expenses_short_term_portion",
                "ca/rental_professional_fees_short_term_portion",
                "ca/rental_management_and_administration_fees_short_term_portion",
                "ca/rental_repairs_and_maintenance_short_term_portion",
                "ca/rental_salaries_wages_and_benefits_short_term_portion",
                "ca/rental_property_taxes_short_term_portion",
                "ca/rental_travel_short_term_portion",
                "ca/rental_utilities_short_term_portion",
                "ca/rental_motor_vehicle_expenses_short_term_portion",
                "ca/rental_other_expenses_short_term_portion",
            )
        },
        produces={"output": "ca/rental_short_term_portion"},
    ),
    # T776 "Line 9366: Non-compliant amount for short-term rentals (amount B from Chart
    # A)": Chart A's column 3 times column 4 divided by column 5 for each row of
    # short-term rental units, rounded to the cent, and "Line B" the total of column 6.
    CapabilitySelection(
        name="ca/short_term_rental_non_compliant_expenses",
        params={"rounding": "ca/short_term_rental_non_compliant_rounding"},
        consumes={"units": "ca/short_term_rental_units"},
        produces={"output": "ca/rental_non_compliant_expenses"},
    ),
    # T776 "Line 1: Deductible expenses (amount A minus line 9949 minus line 9366)",
    # first step: amount A minus line 9949.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ca/rental_total_expenses", "less": "ca/rental_personal_portion"},
        produces={"output": "ca/rental_expenses_less_personal_portion"},
    ),
    # T776 "Line 1: Deductible expenses (amount A minus line 9949 minus line 9366)",
    # second step: that result minus line 9366.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/rental_expenses_less_personal_portion",
            "less": "ca/rental_non_compliant_expenses",
        },
        produces={"output": "ca/rental_deductible_expenses"},
    ),
    # T776 "Line 9369: Net income (loss) before adjustments (total gross rental income
    # from line 8299 minus deductible expenses from amount 1)": signed, a loss is
    # negative.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ca/gross_rental_income", "less": "ca/rental_deductible_expenses"},
        produces={"output": "ca/rental_net_income_before_adjustments"},
    ),
    # T776 "Line 2: Co-owners: calculate your share of net income from line 9369. Enter
    # your result on amount 2": a count of 1 for a co-owner (a caller's 0 or 1) chooses
    # the co-owner's share (line 2, as entered); with a count of 0 amount 2 is line
    # 9369.
    CapabilitySelection(
        name="core/choose_by_count",
        params={},
        consumes={
            "count": "ca/rental_coowner",
            "when_none": "ca/rental_net_income_before_adjustments",
            "when_any": "ca/rental_coowner_share",
        },
        produces={"output": "ca/rental_net_income_share"},
    ),
    # T776 "Line 3: Subtotal (amount 2 minus line 9945)": line 9945 is a caller input.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/rental_net_income_share",
            "less": "ca/rental_coowner_other_expenses",
        },
        produces={"output": "ca/rental_net_income_after_coowner_expenses"},
    ),
    # T776 "Line 4: Subtotal (amount 3 plus line 9947)": line 9947 is a caller input.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/rental_net_income_after_coowner_expenses",
                "ca/rental_recaptured_cca",
            )
        },
        produces={"output": "ca/rental_net_income_with_recapture"},
    ),
    # T776 "Line 5: Subtotal (amount 4 minus line 9948)": line 9948 is a caller input.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/rental_net_income_with_recapture",
            "less": "ca/rental_terminal_loss",
        },
        produces={"output": "ca/rental_net_income_after_terminal_loss"},
    ),
    # T776 "Line 6: Net income (loss) (amount 5 minus line 9936)": line 9936 is a caller
    # input.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/rental_net_income_after_terminal_loss",
            "less": "ca/rental_cca_claim",
        },
        produces={"output": "ca/rental_net_income_after_cca"},
    ),
    # T776 "Line 9946: ... For partnerships, enter the result from amount 7 plus line
    # 9974 minus line 9943", first step: amount 7 (line 7, "Partners: your share of
    # amount 6, or the amount from your T5013 slip, Statement of Partnership Income")
    # plus line 9974 ("Partners: GST/HST rebate for partners received in the year"),
    # both caller inputs.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/rental_partner_share",
                "ca/rental_partner_gst_hst_rebate",
            )
        },
        produces={"output": "ca/rental_partner_share_with_rebate"},
    ),
    # T776 "Line 9946: ... For partnerships, enter the result from amount 7 plus line
    # 9974 minus line 9943", second step: that result minus line 9943 ("Partners: other
    # expenses of the partner"), a caller input.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/rental_partner_share_with_rebate",
            "less": "ca/rental_partner_other_expenses",
        },
        produces={"output": "ca/rental_partnership_net_income"},
    ),
    # T776 "Line 9946: Your net income (loss): For sole proprietors or co-owners, enter
    # the result from amount 6. For partnerships, enter the result from amount 7 plus
    # line 9974 minus line 9943. Enter this amount on line 12600 of your income tax and
    # benefit return"; T1 "Line 12600: Net". A count of 1 for a partner (a caller's 0 or
    # 1) chooses the partnership figure, else amount 6.
    CapabilitySelection(
        name="core/choose_by_count",
        params={},
        consumes={
            "count": "ca/rental_partner",
            "when_none": "ca/rental_net_income_after_cca",
            "when_any": "ca/rental_partnership_net_income",
        },
        produces={"output": "ca/net_rental_income"},
    ),
    # T1 line 33 and line 15000 "Line 28 plus line 32 Total income": every income line
    # the return lists, in line order (lines 1 to 20, line 13 being the net rental
    # income, line 12600 "Net"; here with the amount of dividends of line 9 (12000), the
    # taxable capital gains of line 14 and the taxable support payments of line 15, then
    # line 32); self-employment income (lines 22 to 26) is not wired yet.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/employment_income",
                "ca/other_employment_income",
                "ca/old_age_security",
                "ca/cpp_or_qpp_benefits",
                "ca/other_pensions_and_superannuation",
                "ca/elected_split_pension_amount",
                "ca/universal_child_care_benefit",
                "ca/ei_and_other_benefits",
                "ca/taxable_dividends",
                "ca/interest_and_other_investment_income",
                "ca/net_partnership_income",
                "ca/rdsp_income",
                "ca/net_rental_income",
                "ca/taxable_capital_gains",
                "ca/taxable_support_payments",
                "ca/rrsp_income",
                "ca/fhsa_income",
                "ca/other_fhsa_income",
                "ca/other_income",
                "ca/taxable_scholarships",
                "ca/income_support_benefits",
            )
        },
        produces={"output": "ca/total_income"},
    ),
    # T1 line 123 (40425) "Federal dividend tax credit (use Federal Worksheet)": the Federal
    # Worksheet's "Line 40425 - Federal dividend tax credit", line 5 "Add lines 1 to 4." of
    # the credits shown on the T3, T4PS, T5 and T5013 slips. For dividends with no
    # information slip, line A "Amount from line 12000 of your return (Note 1)" and line B
    # "Amount from line 12010 of your return (Note 1)", Note 1 being "Enter only the amount
    # of dividends that were not shown on an information slip.", so line A is the
    # Worksheet's line 17 and line B its line 16, each its own step; line 6 is "Line B,
    # multiplied by 9.0301%"; line C is "Amount A minus amount B", and line 7 (printed
    # "Line 2") is line C "multiplied by 15.0198%"; line 8 is "Line 6 plus line 7" and
    # line 9 "Line 5 plus line 8 Enter this amount on line 40425 of your return."
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/t3_dividend_tax_credit",
                "ca/t4ps_dividend_tax_credit",
                "ca/t5_dividend_tax_credit",
                "ca/t5013_dividend_tax_credit",
            )
        },
        produces={"output": "ca/slip_dividend_tax_credit"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/dividends_without_a_slip_grossed_up",)},
        produces={"output": "ca/dividends_amount_a"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/other_dividends_grossed_up",)},
        produces={"output": "ca/dividends_amount_b"},
    ),
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/dividend_credit_rate_other_than_eligible"},
        consumes={"base": "ca/dividends_amount_b"},
        produces={"output": "ca/other_dividends_credit"},
    ),
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ca/dividends_amount_a", "less": "ca/dividends_amount_b"},
        produces={"output": "ca/dividends_amount_a_less_b"},
    ),
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/dividend_credit_rate_eligible"},
        consumes={"base": "ca/dividends_amount_a_less_b"},
        produces={"output": "ca/eligible_dividends_credit"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/other_dividends_credit", "ca/eligible_dividends_credit")},
        produces={"output": "ca/no_slip_dividend_tax_credit"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/slip_dividend_tax_credit", "ca/no_slip_dividend_tax_credit")},
        produces={"output": "ca/dividend_tax_credit"},
    ),
    # T1 line 125 "Add lines 122 to 124.": line 122 "Amount from line 35000" and line 123
    # (40425), in line order; line 124 (40427, minimum tax carryover) is not triggered.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/non_refundable_tax_credits", "ca/dividend_tax_credit")},
        produces={"output": "ca/credits_against_basic_federal_tax"},
    ),
    # T1 line 27 "Add lines 22 to 26. Net self-employment income": line 22 (13500) business
    # income, line 23 (13700) professional income, line 24 (13900) commission income, line 25
    # (14100) farming income and line 26 (14300) fishing income, the "Net" box of each, in line
    # order. Line 28 "Line 21 plus line 27" and total income (line 15000) are not yet computed
    # from it.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/business_income",
                "ca/professional_income",
                "ca/commission_income",
                "ca/farming_income",
                "ca/fishing_income",
            ),
        },
        produces={"output": "ca/net_self_employment_income"},
    ),
}

WIRING = {
    (ApplyRate, frozenset({CAPITAL_GAIN}), frozenset({TAXABLE_CAPITAL_GAINS})),
    (
        Sum,
        frozenset(
            {
                T3_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
                T4PS_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
                T5_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
                T5013_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
            }
        ),
        frozenset({SLIP_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE}),
    ),
    (
        Sum,
        frozenset(
            {
                T3_TAXABLE_DIVIDENDS,
                T4PS_TAXABLE_DIVIDENDS,
                T5_TAXABLE_DIVIDENDS,
                T5013_TAXABLE_DIVIDENDS,
            }
        ),
        frozenset({SLIP_TAXABLE_DIVIDENDS}),
    ),
    (
        ApplyFraction,
        frozenset({ELIGIBLE_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP}),
        frozenset({ELIGIBLE_DIVIDENDS_GROSSED_UP}),
    ),
    (
        ApplyFraction,
        frozenset({OTHER_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP}),
        frozenset({OTHER_DIVIDENDS_GROSSED_UP}),
    ),
    (
        Sum,
        frozenset({ELIGIBLE_DIVIDENDS_GROSSED_UP, OTHER_DIVIDENDS_GROSSED_UP}),
        frozenset({DIVIDENDS_WITHOUT_A_SLIP_GROSSED_UP}),
    ),
    (
        Sum,
        frozenset({SLIP_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE, OTHER_DIVIDENDS_GROSSED_UP}),
        frozenset({TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE}),
    ),
    (
        Sum,
        frozenset({SLIP_TAXABLE_DIVIDENDS, DIVIDENDS_WITHOUT_A_SLIP_GROSSED_UP}),
        frozenset({TAXABLE_DIVIDENDS}),
    ),
    (
        Sum,
        frozenset(
            {
                T3_INVESTMENT_INCOME,
                T5_INVESTMENT_INCOME,
                T5013_INVESTMENT_INCOME,
                INVESTMENT_INCOME_CREDITED_NOT_RECEIVED,
                TAX_REFUND_INTEREST,
                FOREIGN_INVESTMENT_INCOME,
                INVESTMENT_INCOME_WITHOUT_A_SLIP,
                INVESTMENT_ROYALTIES,
            }
        ),
        frozenset({INVESTMENT_INCOME_BEFORE_PRIOR_YEARS}),
    ),
    (
        Subtract,
        frozenset(
            {INVESTMENT_INCOME_BEFORE_PRIOR_YEARS, INVESTMENT_INCOME_REPORTED_IN_PREVIOUS_YEARS}
        ),
        frozenset({INTEREST_AND_OTHER_INVESTMENT_INCOME}),
    ),
    (
        Sum,
        frozenset(
            {WORKERS_COMPENSATION_BENEFITS, SOCIAL_ASSISTANCE_PAYMENTS, NET_FEDERAL_SUPPLEMENTS}
        ),
        frozenset({INCOME_SUPPORT_BENEFITS}),
    ),
    (
        ShortTermRentalGrossRents,
        frozenset({RENTAL_PROPERTIES}),
        frozenset({SHORT_TERM_RENTAL_GROSS_RENTS}),
    ),
    (RentalGrossRents, frozenset({RENTAL_PROPERTIES}), frozenset({RENTAL_GROSS_RENTS})),
    (
        Sum,
        frozenset({RENTAL_GROSS_RENTS, RENTAL_OTHER_INCOME}),
        frozenset({GROSS_RENTAL_INCOME}),
    ),
    (
        Sum,
        frozenset(
            {
                RENTAL_ADVERTISING,
                RENTAL_INSURANCE,
                RENTAL_INTEREST_AND_BANK_CHARGES,
                RENTAL_OFFICE_EXPENSES,
                RENTAL_PROFESSIONAL_FEES,
                RENTAL_MANAGEMENT_AND_ADMINISTRATION_FEES,
                RENTAL_REPAIRS_AND_MAINTENANCE,
                RENTAL_SALARIES_WAGES_AND_BENEFITS,
                RENTAL_PROPERTY_TAXES,
                RENTAL_TRAVEL,
                RENTAL_UTILITIES,
                RENTAL_MOTOR_VEHICLE_EXPENSES,
                RENTAL_OTHER_EXPENSES,
            }
        ),
        frozenset({RENTAL_TOTAL_EXPENSES}),
    ),
    (
        Sum,
        frozenset(
            {
                RENTAL_ADVERTISING_PERSONAL_PORTION,
                RENTAL_INSURANCE_PERSONAL_PORTION,
                RENTAL_INTEREST_AND_BANK_CHARGES_PERSONAL_PORTION,
                RENTAL_OFFICE_EXPENSES_PERSONAL_PORTION,
                RENTAL_PROFESSIONAL_FEES_PERSONAL_PORTION,
                RENTAL_MANAGEMENT_AND_ADMINISTRATION_FEES_PERSONAL_PORTION,
                RENTAL_REPAIRS_AND_MAINTENANCE_PERSONAL_PORTION,
                RENTAL_SALARIES_WAGES_AND_BENEFITS_PERSONAL_PORTION,
                RENTAL_PROPERTY_TAXES_PERSONAL_PORTION,
                RENTAL_TRAVEL_PERSONAL_PORTION,
                RENTAL_UTILITIES_PERSONAL_PORTION,
                RENTAL_MOTOR_VEHICLE_EXPENSES_PERSONAL_PORTION,
                RENTAL_OTHER_EXPENSES_PERSONAL_PORTION,
            }
        ),
        frozenset({RENTAL_PERSONAL_PORTION}),
    ),
    (
        Sum,
        frozenset(
            {
                RENTAL_ADVERTISING_SHORT_TERM_PORTION,
                RENTAL_INSURANCE_SHORT_TERM_PORTION,
                RENTAL_INTEREST_AND_BANK_CHARGES_SHORT_TERM_PORTION,
                RENTAL_OFFICE_EXPENSES_SHORT_TERM_PORTION,
                RENTAL_PROFESSIONAL_FEES_SHORT_TERM_PORTION,
                RENTAL_MANAGEMENT_AND_ADMINISTRATION_FEES_SHORT_TERM_PORTION,
                RENTAL_REPAIRS_AND_MAINTENANCE_SHORT_TERM_PORTION,
                RENTAL_SALARIES_WAGES_AND_BENEFITS_SHORT_TERM_PORTION,
                RENTAL_PROPERTY_TAXES_SHORT_TERM_PORTION,
                RENTAL_TRAVEL_SHORT_TERM_PORTION,
                RENTAL_UTILITIES_SHORT_TERM_PORTION,
                RENTAL_MOTOR_VEHICLE_EXPENSES_SHORT_TERM_PORTION,
                RENTAL_OTHER_EXPENSES_SHORT_TERM_PORTION,
            }
        ),
        frozenset({RENTAL_SHORT_TERM_PORTION}),
    ),
    (
        ShortTermRentalNonCompliantExpenses,
        frozenset({SHORT_TERM_RENTAL_UNITS}),
        frozenset({RENTAL_NON_COMPLIANT_EXPENSES}),
    ),
    (
        Subtract,
        frozenset({RENTAL_TOTAL_EXPENSES, RENTAL_PERSONAL_PORTION}),
        frozenset({RENTAL_EXPENSES_LESS_PERSONAL_PORTION}),
    ),
    (
        Subtract,
        frozenset({RENTAL_EXPENSES_LESS_PERSONAL_PORTION, RENTAL_NON_COMPLIANT_EXPENSES}),
        frozenset({RENTAL_DEDUCTIBLE_EXPENSES}),
    ),
    (
        Subtract,
        frozenset({GROSS_RENTAL_INCOME, RENTAL_DEDUCTIBLE_EXPENSES}),
        frozenset({RENTAL_NET_INCOME_BEFORE_ADJUSTMENTS}),
    ),
    (
        ChooseByCount,
        frozenset({RENTAL_COOWNER, RENTAL_NET_INCOME_BEFORE_ADJUSTMENTS, RENTAL_COOWNER_SHARE}),
        frozenset({RENTAL_NET_INCOME_SHARE}),
    ),
    (
        Subtract,
        frozenset({RENTAL_NET_INCOME_SHARE, RENTAL_COOWNER_OTHER_EXPENSES}),
        frozenset({RENTAL_NET_INCOME_AFTER_COOWNER_EXPENSES}),
    ),
    (
        Sum,
        frozenset({RENTAL_NET_INCOME_AFTER_COOWNER_EXPENSES, RENTAL_RECAPTURED_CCA}),
        frozenset({RENTAL_NET_INCOME_WITH_RECAPTURE}),
    ),
    (
        Subtract,
        frozenset({RENTAL_NET_INCOME_WITH_RECAPTURE, RENTAL_TERMINAL_LOSS}),
        frozenset({RENTAL_NET_INCOME_AFTER_TERMINAL_LOSS}),
    ),
    (
        Subtract,
        frozenset({RENTAL_NET_INCOME_AFTER_TERMINAL_LOSS, RENTAL_CCA_CLAIM}),
        frozenset({RENTAL_NET_INCOME_AFTER_CCA}),
    ),
    (
        Sum,
        frozenset({RENTAL_PARTNER_SHARE, RENTAL_PARTNER_GST_HST_REBATE}),
        frozenset({RENTAL_PARTNER_SHARE_WITH_REBATE}),
    ),
    (
        Subtract,
        frozenset({RENTAL_PARTNER_SHARE_WITH_REBATE, RENTAL_PARTNER_OTHER_EXPENSES}),
        frozenset({RENTAL_PARTNERSHIP_NET_INCOME}),
    ),
    (
        ChooseByCount,
        frozenset({RENTAL_PARTNER, RENTAL_NET_INCOME_AFTER_CCA, RENTAL_PARTNERSHIP_NET_INCOME}),
        frozenset({NET_RENTAL_INCOME}),
    ),
    (
        Sum,
        frozenset(
            {
                EMPLOYMENT_INCOME,
                OTHER_EMPLOYMENT_INCOME,
                OLD_AGE_SECURITY,
                CPP_OR_QPP_BENEFITS,
                OTHER_PENSIONS_AND_SUPERANNUATION,
                ELECTED_SPLIT_PENSION_AMOUNT,
                UNIVERSAL_CHILD_CARE_BENEFIT,
                EI_AND_OTHER_BENEFITS,
                TAXABLE_DIVIDENDS,
                INTEREST_AND_OTHER_INVESTMENT_INCOME,
                NET_PARTNERSHIP_INCOME,
                RDSP_INCOME,
                NET_RENTAL_INCOME,
                TAXABLE_CAPITAL_GAINS,
                TAXABLE_SUPPORT_PAYMENTS,
                RRSP_INCOME,
                FHSA_INCOME,
                OTHER_FHSA_INCOME,
                OTHER_INCOME,
                TAXABLE_SCHOLARSHIPS,
                INCOME_SUPPORT_BENEFITS,
            }
        ),
        frozenset({TOTAL_INCOME}),
    ),
    (
        Sum,
        frozenset(
            {
                T3_DIVIDEND_TAX_CREDIT,
                T4PS_DIVIDEND_TAX_CREDIT,
                T5_DIVIDEND_TAX_CREDIT,
                T5013_DIVIDEND_TAX_CREDIT,
            }
        ),
        frozenset({SLIP_DIVIDEND_TAX_CREDIT}),
    ),
    (
        Sum,
        frozenset({DIVIDENDS_WITHOUT_A_SLIP_GROSSED_UP}),
        frozenset({DIVIDENDS_AMOUNT_A}),
    ),
    (Sum, frozenset({OTHER_DIVIDENDS_GROSSED_UP}), frozenset({DIVIDENDS_AMOUNT_B})),
    (ApplyRate, frozenset({DIVIDENDS_AMOUNT_B}), frozenset({OTHER_DIVIDENDS_CREDIT})),
    (
        Subtract,
        frozenset({DIVIDENDS_AMOUNT_A, DIVIDENDS_AMOUNT_B}),
        frozenset({DIVIDENDS_AMOUNT_A_LESS_B}),
    ),
    (
        ApplyRate,
        frozenset({DIVIDENDS_AMOUNT_A_LESS_B}),
        frozenset({ELIGIBLE_DIVIDENDS_CREDIT}),
    ),
    (
        Sum,
        frozenset({OTHER_DIVIDENDS_CREDIT, ELIGIBLE_DIVIDENDS_CREDIT}),
        frozenset({NO_SLIP_DIVIDEND_TAX_CREDIT}),
    ),
    (
        Sum,
        frozenset({SLIP_DIVIDEND_TAX_CREDIT, NO_SLIP_DIVIDEND_TAX_CREDIT}),
        frozenset({DIVIDEND_TAX_CREDIT}),
    ),
    (
        Sum,
        frozenset({NON_REFUNDABLE_TAX_CREDITS, DIVIDEND_TAX_CREDIT}),
        frozenset({CREDITS_AGAINST_BASIC_FEDERAL_TAX}),
    ),
    (
        Sum,
        frozenset(
            {
                BUSINESS_INCOME,
                PROFESSIONAL_INCOME,
                COMMISSION_INCOME,
                FARMING_INCOME,
                FISHING_INCOME,
            }
        ),
        frozenset({NET_SELF_EMPLOYMENT_INCOME}),
    ),
}
