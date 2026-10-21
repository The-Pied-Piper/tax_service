"""The CA-ON manifest entries of one family of lines (see `test_manifest.py`)."""

from __future__ import annotations

from app.domain.capabilities.apply_fraction import ApplyFraction
from app.domain.capabilities.apply_rate import ApplyRate
from app.domain.capabilities.at_most import AtMost
from app.domain.capabilities.choose_by_count import ChooseByCount
from app.domain.capabilities.lesser_of import LesserOf
from app.domain.capabilities.subtract import Subtract
from app.domain.capabilities.subtract_not_below_zero import SubtractNotBelowZero
from app.domain.capabilities.sum import Sum
from app.domain.capabilities.sum_not_below_zero import SumNotBelowZero
from app.domain.manifest import CapabilitySelection
from app.jurisdictions.ca.capabilities.cca_claim import CcaClaim
from app.jurisdictions.ca.capabilities.closing_ucc import ClosingUcc
from app.jurisdictions.ca.capabilities.disposition_gains import DispositionGains
from app.jurisdictions.ca.capabilities.disposition_gains_only import DispositionGainsOnly
from app.jurisdictions.ca.capabilities.disposition_proceeds import DispositionProceeds
from app.jurisdictions.ca.capabilities.principal_residence_gain import PrincipalResidenceGain
from app.jurisdictions.ca.capabilities.recaptured_cca import RecapturedCca
from app.jurisdictions.ca.capabilities.rental_gross_rents import RentalGrossRents
from app.jurisdictions.ca.capabilities.short_term_rental_gross_rents import (
    ShortTermRentalGrossRents,
)
from app.jurisdictions.ca.capabilities.short_term_rental_non_compliant_cca import (
    ShortTermRentalNonCompliantCca,
)
from app.jurisdictions.ca.capabilities.short_term_rental_non_compliant_cca_by_class import (
    ShortTermRentalNonCompliantCcaByClass,
)
from app.jurisdictions.ca.capabilities.short_term_rental_non_compliant_expenses import (
    ShortTermRentalNonCompliantExpenses,
)
from app.jurisdictions.ca.capabilities.terminal_loss import TerminalLoss
from app.jurisdictions.ca.catalog import (
    BOND_DISPOSITIONS,
    BOND_GAIN_OR_LOSS,
    BOND_PROCEEDS,
    BUSINESS_ADJUSTED_GROSS_SALES,
    BUSINESS_ADVERTISING,
    BUSINESS_BAD_DEBTS,
    BUSINESS_BUSINESS_TAXES_LICENCES_AND_MEMBERSHIPS,
    BUSINESS_CCA_CLAIM,
    BUSINESS_CCA_CLAIM_LESS_PERSONAL_PART,
    BUSINESS_CCA_CLASSES,
    BUSINESS_CCA_PERSONAL_PART,
    BUSINESS_CCA_TABLE_CLAIM,
    BUSINESS_CLOSING_INVENTORY,
    BUSINESS_CLOSING_UCC,
    BUSINESS_COST_OF_GOODS_SOLD,
    BUSINESS_COST_OF_GOODS_SUBTOTAL,
    BUSINESS_DELIVERY_FREIGHT_AND_EXPRESS,
    BUSINESS_DIRECT_WAGE_COSTS,
    BUSINESS_FUEL_COSTS,
    BUSINESS_GROSS_INCOME,
    BUSINESS_GROSS_INCOME_BEFORE_EXPENSES,
    BUSINESS_GROSS_INCOME_FOR_GROSS_PROFIT,
    BUSINESS_GROSS_PROFIT,
    BUSINESS_GROSS_SALES,
    BUSINESS_HOME_ALLOWABLE_CLAIM,
    BUSINESS_HOME_CARRIED_FORWARD,
    BUSINESS_HOME_CARRY_FORWARD,
    BUSINESS_HOME_CCA,
    BUSINESS_HOME_ELECTRICITY,
    BUSINESS_HOME_EXPENSES,
    BUSINESS_HOME_EXPENSES_AVAILABLE,
    BUSINESS_HOME_EXPENSES_BUSINESS_PART,
    BUSINESS_HOME_EXPENSES_SUBTOTAL,
    BUSINESS_HOME_HEAT,
    BUSINESS_HOME_INCOME_LIMIT,
    BUSINESS_HOME_INSURANCE,
    BUSINESS_HOME_MAINTENANCE,
    BUSINESS_HOME_MORTGAGE_INTEREST,
    BUSINESS_HOME_OTHER_EXPENSES,
    BUSINESS_HOME_PERSONAL_USE_PART,
    BUSINESS_HOME_PROPERTY_TAXES,
    BUSINESS_INCOME,
    BUSINESS_INSURANCE,
    BUSINESS_INTEREST_AND_BANK_CHARGES,
    BUSINESS_INVESTMENT_LOSS_REDUCTION,
    BUSINESS_JOURNALISM_LABOUR_TAX_CREDIT,
    BUSINESS_MANAGEMENT_AND_ADMINISTRATION_FEES,
    BUSINESS_MEALS_AND_ENTERTAINMENT,
    BUSINESS_MOTOR_VEHICLE_EXPENSES,
    BUSINESS_NET_INCOME_AFTER_ADJUSTMENTS,
    BUSINESS_NET_INCOME_BEFORE_ADJUSTMENTS,
    BUSINESS_OFFICE_EXPENSES,
    BUSINESS_OFFICE_STATIONERY_AND_SUPPLIES,
    BUSINESS_OPENING_INVENTORY,
    BUSINESS_OTHER_COSTS,
    BUSINESS_OTHER_EXPENSES,
    BUSINESS_OTHER_EXPENSES_WITH_TERMINAL_LOSS,
    BUSINESS_OTHER_INCOME,
    BUSINESS_OTHER_INCOME_WITH_RECAPTURE,
    BUSINESS_PARTNER,
    BUSINESS_PARTNER_GST_HST_REBATE,
    BUSINESS_PARTNER_OTHER_AMOUNT_A,
    BUSINESS_PARTNER_OTHER_AMOUNT_B,
    BUSINESS_PARTNER_OTHER_AMOUNT_C,
    BUSINESS_PARTNER_OTHER_AMOUNT_D,
    BUSINESS_PARTNER_OTHER_AMOUNT_E,
    BUSINESS_PARTNER_OTHER_AMOUNTS,
    BUSINESS_PARTNER_OTHER_AMOUNTS_TOTAL,
    BUSINESS_PARTNER_SHARE,
    BUSINESS_PARTNERSHIP_TOTAL,
    BUSINESS_PROFESSIONAL_FEES,
    BUSINESS_PROPERTY_TAXES,
    BUSINESS_PURCHASES,
    BUSINESS_QUICK_METHOD_ASSISTANCE,
    BUSINESS_QUICK_METHOD_GST_HST,
    BUSINESS_QUICK_METHOD_REMITTED,
    BUSINESS_RECAPTURED_CCA,
    BUSINESS_RENT,
    BUSINESS_REPAIRS_AND_MAINTENANCE,
    BUSINESS_RESERVES_AND_OTHER_INCOME,
    BUSINESS_RESERVES_DEDUCTED_LAST_YEAR,
    BUSINESS_SALARIES_WAGES_AND_BENEFITS,
    BUSINESS_SALES_ADJUSTMENTS,
    BUSINESS_SALES_SUBTOTAL,
    BUSINESS_SHARE_OF_NET_INCOME,
    BUSINESS_SUBCONTRACTS,
    BUSINESS_TERMINAL_LOSS,
    BUSINESS_TOTAL_EXPENSES,
    BUSINESS_TRAVEL_EXPENSES,
    BUSINESS_UTILITIES,
    CAPITAL_GAIN,
    CAPITAL_GAINS_AFTER_DEFERRAL,
    CAPITAL_GAINS_BEFORE_INVESTMENT_LOSS_REDUCTION,
    CAPITAL_GAINS_BEFORE_RESERVES,
    CAPITAL_GAINS_DEFERRAL,
    CAPITAL_GAINS_OF_QUALIFIED_AND_OTHER_PROPERTIES,
    CAPITAL_GAINS_RESERVES,
    COMMISSION_INCOME,
    CPP_OR_QPP_BENEFITS,
    CREDITS_AGAINST_BASIC_FEDERAL_TAX,
    CRYPTO_ASSET_DISPOSITIONS,
    CRYPTO_ASSET_GAIN_OR_LOSS,
    CRYPTO_ASSET_PROCEEDS,
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
    INCLUDED_CAPITAL_GAIN,
    INCOME_SUPPORT_BENEFITS,
    INTEREST_AND_OTHER_INVESTMENT_INCOME,
    INVESTMENT_INCOME_BEFORE_PRIOR_YEARS,
    INVESTMENT_INCOME_CREDITED_NOT_RECEIVED,
    INVESTMENT_INCOME_REPORTED_IN_PREVIOUS_YEARS,
    INVESTMENT_INCOME_WITHOUT_A_SLIP,
    INVESTMENT_ROYALTIES,
    LISTED_PERSONAL_PROPERTY_DISPOSITIONS,
    LISTED_PERSONAL_PROPERTY_GAIN_OR_LOSS,
    LISTED_PERSONAL_PROPERTY_NET_GAIN,
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
    OTHER_FORECLOSURE_DISPOSITIONS,
    OTHER_FORECLOSURE_GAIN_OR_LOSS,
    OTHER_FORECLOSURE_PROCEEDS,
    OTHER_INCOME,
    OTHER_PENSIONS_AND_SUPERANNUATION,
    PARTNERSHIP_GAINS_AT_FULL_INCLUSION,
    PERSONAL_USE_PROPERTY_DISPOSITIONS,
    PERSONAL_USE_PROPERTY_GAIN,
    PERSONAL_USE_PROPERTY_GAIN_ROWS,
    PRINCIPAL_RESIDENCE_GAIN,
    PRINCIPAL_RESIDENCE_PROPERTIES,
    PROFESSIONAL_INCOME,
    QFFP_DISPOSITIONS,
    QFFP_FORECLOSURE_DISPOSITIONS,
    QFFP_FORECLOSURE_GAIN_OR_LOSS,
    QFFP_FORECLOSURE_PROCEEDS,
    QFFP_GAIN_OR_LOSS,
    QFFP_PROCEEDS,
    QSBCS_DISPOSITIONS,
    QSBCS_GAIN_OR_LOSS,
    QSBCS_PROCEEDS,
    RDSP_INCOME,
    REAL_ESTATE_DISPOSITIONS,
    REAL_ESTATE_GAIN_OR_LOSS,
    REAL_ESTATE_PROCEEDS,
    RENTAL_ADVERTISING,
    RENTAL_ADVERTISING_PERSONAL_PORTION,
    RENTAL_ADVERTISING_SHORT_TERM_PORTION,
    RENTAL_CCA_BUSINESS_USE_OF_HOME,
    RENTAL_CCA_CLAIM,
    RENTAL_CCA_CLAIM_BEFORE_LIMIT,
    RENTAL_CCA_CLAIM_LESS_PERSONAL_PART,
    RENTAL_CCA_CLAIM_SHARE,
    RENTAL_CCA_CLASSES,
    RENTAL_CCA_LIMIT,
    RENTAL_CCA_PERSONAL_PART,
    RENTAL_CCA_TABLE_CLAIM,
    RENTAL_CCA_TABLE_RECAPTURE,
    RENTAL_CCA_TABLE_TERMINAL_LOSS,
    RENTAL_CLOSING_UCC,
    RENTAL_COOWNER,
    RENTAL_COOWNER_CCA_CLAIM,
    RENTAL_COOWNER_OTHER_EXPENSES,
    RENTAL_COOWNER_RECAPTURED_CCA,
    RENTAL_COOWNER_SHARE,
    RENTAL_COOWNER_TERMINAL_LOSS,
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
    RENTAL_NON_COMPLIANT_CCA,
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
    SHARE_DISPOSITIONS,
    SHARE_GAIN_OR_LOSS,
    SHARE_PROCEEDS,
    SHORT_TERM_RENTAL_CCA_UNITS,
    SHORT_TERM_RENTAL_GROSS_RENTS,
    SHORT_TERM_RENTAL_NON_COMPLIANT_CCA_BY_CLASS,
    SHORT_TERM_RENTAL_UNITS,
    SLIP_CAPITAL_GAINS_OR_LOSSES,
    SLIP_DIVIDEND_TAX_CREDIT,
    SLIP_TAXABLE_DIVIDENDS,
    SLIP_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
    SOCIAL_ASSISTANCE_PAYMENTS,
    T3_CAPITAL_GAINS_OR_LOSSES,
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
    UNAPPLIED_LISTED_PERSONAL_PROPERTY_LOSSES,
    UNIVERSAL_CHILD_CARE_BENEFIT,
    WORKERS_COMPENSATION_BENEFITS,
)

INPUTS = frozenset(
    {
        "ca/employment_income",
        # Schedule 3 Part 3 and Part 4: the ten property lists (lines 1 to 10), the unapplied
        # listed personal property losses, the properties sold (Form T2091(IND)), line 13
        # (16100), line 15 (17400), line 16 (17600) and line 20 (19200); line 21 (19700) is
        # computed.
        "ca/qsbcs_dispositions",
        "ca/qffp_dispositions",
        "ca/qffp_foreclosure_dispositions",
        "ca/share_dispositions",
        "ca/real_estate_dispositions",
        "ca/bond_dispositions",
        "ca/crypto_asset_dispositions",
        "ca/other_foreclosure_dispositions",
        "ca/personal_use_property_dispositions",
        "ca/listed_personal_property_dispositions",
        "ca/unapplied_listed_personal_property_losses",
        "ca/principal_residence_properties",
        "ca/capital_gains_deferral",
        "ca/slip_capital_gains_or_losses",
        "ca/t3_capital_gains_or_losses",
        "ca/capital_gains_reserves",
        # Schedule 3 Part 5 line 25 and line 19890: "Capital gains from certain dispositions of an
        # interest in a partnership subject to 100% inclusion rate (if negative, enter "0")", a
        # starting amount.
        "ca/partnership_gains_at_full_inclusion",
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
        "ca/short_term_rental_cca_units",
        "ca/rental_coowner",
        "ca/rental_coowner_share",
        "ca/rental_coowner_other_expenses",
        "ca/rental_cca_classes",
        "ca/rental_coowner_recaptured_cca",
        "ca/rental_coowner_terminal_loss",
        "ca/rental_coowner_cca_claim",
        "ca/rental_cca_personal_part",
        "ca/rental_cca_business_use_of_home",
        "ca/rental_partner",
        "ca/rental_partner_share",
        "ca/rental_partner_gst_hst_rebate",
        "ca/rental_partner_other_expenses",
        # Form T2125 (business statement) Part 3A to Part 7 and Area A: the caller's amounts, in the
        # form's order; T1 line 22 (line 13500), `ca/business_income`, is no longer an input, it is
        # T2125 line 9946.
        "ca/business_gross_sales",
        "ca/business_sales_adjustments",
        "ca/business_quick_method_gst_hst",
        "ca/business_quick_method_remitted",
        "ca/business_reserves_deducted_last_year",
        "ca/business_other_income",
        "ca/business_opening_inventory",
        "ca/business_purchases",
        "ca/business_direct_wage_costs",
        "ca/business_subcontracts",
        "ca/business_other_costs",
        "ca/business_closing_inventory",
        "ca/business_advertising",
        "ca/business_meals_and_entertainment",
        "ca/business_bad_debts",
        "ca/business_insurance",
        "ca/business_interest_and_bank_charges",
        "ca/business_business_taxes_licences_and_memberships",
        "ca/business_office_expenses",
        "ca/business_office_stationery_and_supplies",
        "ca/business_professional_fees",
        "ca/business_management_and_administration_fees",
        "ca/business_rent",
        "ca/business_repairs_and_maintenance",
        "ca/business_salaries_wages_and_benefits",
        "ca/business_property_taxes",
        "ca/business_travel_expenses",
        "ca/business_utilities",
        "ca/business_fuel_costs",
        "ca/business_delivery_freight_and_express",
        "ca/business_motor_vehicle_expenses",
        "ca/business_cca_personal_part",
        "ca/business_other_expenses",
        "ca/business_journalism_labour_tax_credit",
        "ca/business_partner_gst_hst_rebate",
        "ca/business_partner_other_amount_a",
        "ca/business_partner_other_amount_b",
        "ca/business_partner_other_amount_c",
        "ca/business_partner_other_amount_d",
        "ca/business_partner_other_amount_e",
        "ca/business_home_heat",
        "ca/business_home_electricity",
        "ca/business_home_insurance",
        "ca/business_home_maintenance",
        "ca/business_home_mortgage_interest",
        "ca/business_home_property_taxes",
        "ca/business_home_other_expenses",
        "ca/business_home_personal_use_part",
        "ca/business_home_cca",
        "ca/business_home_carried_forward",
        "ca/business_partner_share",
        "ca/business_partner",
        "ca/business_cca_classes",
        "ca/taxable_support_payments",
        "ca/rrsp_income",
        "ca/fhsa_income",
        "ca/other_fhsa_income",
        "ca/other_income",
        "ca/taxable_scholarships",
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
        "ca/rental_closing_ucc",
        "ca/rental_non_compliant_cca",
        "ca/short_term_rental_non_compliant_cca_by_class",
        # T2125 Area A column 22 "UCC at the end of the year" (for next year) and Part 7 line 7O
        # "Business-use-of-home expenses available to carry forward": nothing else on the return
        # reads them.
        "ca/business_closing_ucc",
        "ca/business_home_carry_forward",
        # Schedule 3 Part 3: the eight "Total proceeds of disposition" lines feed no later line.
        "ca/qsbcs_proceeds",
        "ca/qffp_proceeds",
        "ca/qffp_foreclosure_proceeds",
        "ca/share_proceeds",
        "ca/real_estate_proceeds",
        "ca/bond_proceeds",
        "ca/crypto_asset_proceeds",
        "ca/other_foreclosure_proceeds",
    }
)

STEPS = {
    # Schedule 3 (form 5000-S3) Part 3: "For each Gain or loss enter as many lines as necessary."
    # Each property type lists one row per disposition: "(Column 2): Proceeds of disposition",
    # "(Column 3): Adjusted cost base", "(Column 4): Outlays and expenses", "(Column 5): Gain or
    # loss (column 2 minus columns 3 and 4)"; lines 1 to 8 (10700, 11000, 12400, 13200, 13800,
    # 15300, 15301, 15500) are each "Total gain or loss (add all the amounts under column 5)",
    # one step each.
    CapabilitySelection(
        name="ca/disposition_gains",
        params={},
        consumes={"dispositions": "ca/qsbcs_dispositions"},
        produces={"output": "ca/qsbcs_gain_or_loss"},
    ),
    CapabilitySelection(
        name="ca/disposition_gains",
        params={},
        consumes={"dispositions": "ca/qffp_dispositions"},
        produces={"output": "ca/qffp_gain_or_loss"},
    ),
    CapabilitySelection(
        name="ca/disposition_gains",
        params={},
        consumes={"dispositions": "ca/qffp_foreclosure_dispositions"},
        produces={"output": "ca/qffp_foreclosure_gain_or_loss"},
    ),
    CapabilitySelection(
        name="ca/disposition_gains",
        params={},
        consumes={"dispositions": "ca/share_dispositions"},
        produces={"output": "ca/share_gain_or_loss"},
    ),
    CapabilitySelection(
        name="ca/disposition_gains",
        params={},
        consumes={"dispositions": "ca/real_estate_dispositions"},
        produces={"output": "ca/real_estate_gain_or_loss"},
    ),
    CapabilitySelection(
        name="ca/disposition_gains",
        params={},
        consumes={"dispositions": "ca/bond_dispositions"},
        produces={"output": "ca/bond_gain_or_loss"},
    ),
    CapabilitySelection(
        name="ca/disposition_gains",
        params={},
        consumes={"dispositions": "ca/crypto_asset_dispositions"},
        produces={"output": "ca/crypto_asset_gain_or_loss"},
    ),
    CapabilitySelection(
        name="ca/disposition_gains",
        params={},
        consumes={"dispositions": "ca/other_foreclosure_dispositions"},
        produces={"output": "ca/other_foreclosure_gain_or_loss"},
    ),
    # Schedule 3 Part 3: lines 1 to 8 (10699, 10999, 12399, 13199, 13599, 15199, 15200, 15499) are
    # each "Total proceeds of disposition (add all the amounts under column 2)", one step each; the
    # totals feed no later line.
    CapabilitySelection(
        name="ca/disposition_proceeds",
        params={},
        consumes={"dispositions": "ca/qsbcs_dispositions"},
        produces={"output": "ca/qsbcs_proceeds"},
    ),
    CapabilitySelection(
        name="ca/disposition_proceeds",
        params={},
        consumes={"dispositions": "ca/qffp_dispositions"},
        produces={"output": "ca/qffp_proceeds"},
    ),
    CapabilitySelection(
        name="ca/disposition_proceeds",
        params={},
        consumes={"dispositions": "ca/qffp_foreclosure_dispositions"},
        produces={"output": "ca/qffp_foreclosure_proceeds"},
    ),
    CapabilitySelection(
        name="ca/disposition_proceeds",
        params={},
        consumes={"dispositions": "ca/share_dispositions"},
        produces={"output": "ca/share_proceeds"},
    ),
    CapabilitySelection(
        name="ca/disposition_proceeds",
        params={},
        consumes={"dispositions": "ca/real_estate_dispositions"},
        produces={"output": "ca/real_estate_proceeds"},
    ),
    CapabilitySelection(
        name="ca/disposition_proceeds",
        params={},
        consumes={"dispositions": "ca/bond_dispositions"},
        produces={"output": "ca/bond_proceeds"},
    ),
    CapabilitySelection(
        name="ca/disposition_proceeds",
        params={},
        consumes={"dispositions": "ca/crypto_asset_dispositions"},
        produces={"output": "ca/crypto_asset_proceeds"},
    ),
    CapabilitySelection(
        name="ca/disposition_proceeds",
        params={},
        consumes={"dispositions": "ca/other_foreclosure_dispositions"},
        produces={"output": "ca/other_foreclosure_proceeds"},
    ),
    # Form T2091(IND) Part 1 and Part 3, one form for each property sold: "Divide line 21 by line
    # 22." (line 23, the exempt part, rounded half up to the cent), "Line 18 minus line 23 (if
    # negative, enter "0")" (line 24) and "Total capital gain" (line 54, which is line 24 when
    # Part 2 is not completed), added over the properties.
    CapabilitySelection(
        name="ca/principal_residence_gain",
        params={"rounding": "ca/principal_residence_gain_rounding"},
        consumes={"properties": "ca/principal_residence_properties"},
        produces={"output": "ca/principal_residence_gain"},
    ),
    # Part 3, Personal-use property: "Line 9 and line 15800: Total gain only (add all the amounts
    # under column 5)": the rows' gains, a row's loss counting 0, then line 9 itself, a sum of
    # those rows and line 54 of T2091(IND) ("enter the amount from line 54 above on line 15800 of
    # Schedule 3").
    CapabilitySelection(
        name="ca/disposition_gains_only",
        params={},
        consumes={"dispositions": "ca/personal_use_property_dispositions"},
        produces={"output": "ca/personal_use_property_gain_rows"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/personal_use_property_gain_rows", "ca/principal_residence_gain")},
        produces={"output": "ca/personal_use_property_gain"},
    ),
    # Part 3, Listed personal property: the rows' gains and losses (column 5) added, then line 10
    # and line 15900 "Net gain only": that total less the unapplied listed personal property
    # losses from other years, not below zero.
    CapabilitySelection(
        name="ca/disposition_gains",
        params={},
        consumes={"dispositions": "ca/listed_personal_property_dispositions"},
        produces={"output": "ca/listed_personal_property_gain_or_loss"},
    ),
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/listed_personal_property_gain_or_loss",
            "less": "ca/unapplied_listed_personal_property_losses",
        },
        produces={"output": "ca/listed_personal_property_net_gain"},
    ),
    # Part 3 "Line 11: Add lines 1 to 10. Total gains or losses of qualified properties and
    # other properties ="; Part 4 "Line 12: Amount from line 11 of the previous page" is the same
    # artifact, so it has no step of its own.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/qsbcs_gain_or_loss",
                "ca/qffp_gain_or_loss",
                "ca/qffp_foreclosure_gain_or_loss",
                "ca/share_gain_or_loss",
                "ca/real_estate_gain_or_loss",
                "ca/bond_gain_or_loss",
                "ca/crypto_asset_gain_or_loss",
                "ca/other_foreclosure_gain_or_loss",
                "ca/personal_use_property_gain",
                "ca/listed_personal_property_net_gain",
            )
        },
        produces={"output": "ca/capital_gains_of_qualified_and_other_properties"},
    ),
    # Part 4 "Line 14: Line 12 minus line 13 =" (line 13 and line 16100 is an input).
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/capital_gains_of_qualified_and_other_properties",
            "less": "ca/capital_gains_deferral",
        },
        produces={"output": "ca/capital_gains_after_deferral"},
    ),
    # Part 4 "Line 17: Add lines 14 to 16. =" (lines 15 and 16, 17400 and 17600, are inputs).
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/capital_gains_after_deferral",
                "ca/slip_capital_gains_or_losses",
                "ca/t3_capital_gains_or_losses",
            )
        },
        produces={"output": "ca/capital_gains_before_investment_loss_reduction"},
    ),
    # Part 4 "Line 19 and line 19100: Total gains or losses before reserves: line 17 minus line
    # 18 =" (line 18 and line 17800 is the business investment loss reduction already computed).
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/capital_gains_before_investment_loss_reduction",
            "less": "ca/business_investment_loss_reduction",
        },
        produces={"output": "ca/capital_gains_before_reserves"},
    ),
    # Part 4 "Line 21 and line 19700: Line 19 plus line 20 Total capital gains or losses =" (line
    # 20 and line 19200, the reserves, is an input).
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/capital_gains_before_reserves", "ca/capital_gains_reserves")},
        produces={"output": "ca/capital_gain"},
    ),
    # Part 5 line 22 is the same artifact as line 21; line 24 "Line 22 multiplied by the
    # percentage on line 23" (signed, the included capital gain), then line 26 and line 19900
    # "Line 24 plus line 25 If positive, enter the result on line 12700 of your return": line 24
    # and line 25 (the partnership gains at full inclusion, a caller input) as the parts of a sum
    # not below zero, so the taxable capital gains stay non-negative.
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/capital_gains_inclusion_rate"},
        consumes={"base": "ca/capital_gain"},
        produces={"output": "ca/included_capital_gain"},
    ),
    CapabilitySelection(
        name="core/sum_not_below_zero",
        params={},
        consumes={"parts": ("ca/included_capital_gain", "ca/partnership_gains_at_full_inclusion")},
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
    # T776 Chart B "Column 7 ***: Non-compliant amount (column 4 multiplied by column 5
    # divided by column 6)" for each row of short-term rental CCA units, rounded to the cent,
    # and "Line C: Total non-compliant amount of CCA for short-term rentals: Total of column 7
    # (enter on line 9367 of Part 4)".
    CapabilitySelection(
        name="ca/short_term_rental_non_compliant_cca",
        params={"rounding": "ca/short_term_rental_non_compliant_cca_rounding"},
        consumes={"units": "ca/short_term_rental_cca_units"},
        produces={"output": "ca/rental_non_compliant_cca"},
    ),
    # T776 Chart B "*** For each class, add the amounts from column 7 of Chart B and enter each
    # total in column 22 of Area A, in the respective row.": one record for each class, the
    # class number and column 22.
    CapabilitySelection(
        name="ca/short_term_rental_non_compliant_cca_by_class",
        params={"rounding": "ca/short_term_rental_non_compliant_cca_rounding"},
        consumes={"units": "ca/short_term_rental_cca_units"},
        produces={"output": "ca/short_term_rental_non_compliant_cca_by_class"},
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
    # T776 Area A "Line ii: Total CCA claim for the year *: Total of column 23" and Note 3 "If you
    # have a negative amount in column 7, add it to income as a recapture under "Recaptured
    # capital cost allowance" on line 9947": the recapture of each class of the Area A list
    # (column 7 made positive when negative), totalled.
    CapabilitySelection(
        name="ca/recaptured_cca",
        params={"class_rates": "ca/cca_class_rates"},
        consumes={"classes": "ca/rental_cca_classes"},
        produces={"output": "ca/rental_cca_table_recapture"},
    ),
    # T776 "Line 9947: Recaptured capital cost allowance (co-owners: enter your share of the
    # amount)": a count of 1 for a co-owner (a caller's 0 or 1) chooses the co-owner's share, as
    # entered; with a count of 0 line 9947 is the recapture of Area A.
    CapabilitySelection(
        name="core/choose_by_count",
        params={},
        consumes={
            "count": "ca/rental_coowner",
            "when_none": "ca/rental_cca_table_recapture",
            "when_any": "ca/rental_coowner_recaptured_cca",
        },
        produces={"output": "ca/rental_recaptured_cca"},
    ),
    # T776 "Line 4: Subtotal (amount 3 plus line 9947)": line 9947 is computed from Area A.
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
    # T776 Area A Note 3 "If no property is left in the class and there is a positive amount in
    # this column, deduct the amount from your income as a terminal loss under "Terminal loss" on
    # line 9948. Recapture and terminal loss do not apply to a Class 10.1 property unless it is a
    # DIEP": the terminal loss of each class of the Area A list, totalled.
    CapabilitySelection(
        name="ca/terminal_loss",
        params={"class_rates": "ca/cca_class_rates"},
        consumes={"classes": "ca/rental_cca_classes"},
        produces={"output": "ca/rental_cca_table_terminal_loss"},
    ),
    # T776 "Line 9948: Terminal loss (co-owners: enter your share of the amount)": a count of 1
    # for a co-owner chooses the co-owner's share, as entered; with a count of 0 line 9948 is the
    # terminal loss of Area A.
    CapabilitySelection(
        name="core/choose_by_count",
        params={},
        consumes={
            "count": "ca/rental_coowner",
            "when_none": "ca/rental_cca_table_terminal_loss",
            "when_any": "ca/rental_coowner_terminal_loss",
        },
        produces={"output": "ca/rental_terminal_loss"},
    ),
    # T776 "Line 5: Subtotal (amount 4 minus line 9948)": line 9948 is computed from Area A.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/rental_net_income_with_recapture",
            "less": "ca/rental_terminal_loss",
        },
        produces={"output": "ca/rental_net_income_after_terminal_loss"},
    ),
    # T776 Area A "Line ii: Total CCA claim for the year *: Total of column 23": the CCA claimed
    # on each class of the Area A list, at most its maximum (column 19 multiplied by column 20),
    # totalled.
    CapabilitySelection(
        name="ca/cca_claim",
        params={"class_rates": "ca/cca_class_rates"},
        consumes={"classes": "ca/rental_cca_classes"},
        produces={"output": "ca/rental_cca_table_claim"},
    ),
    # T776 Area A "* Sole proprietors and partnerships: Enter the total CCA claim for the year
    # from amount ii on line 9936. Co-owners: Enter only your share of the total CCA claim for
    # the year from amount ii on line 9936": a count of 1 for a co-owner chooses the co-owner's
    # share, as entered; with a count of 0 it is amount ii.
    CapabilitySelection(
        name="core/choose_by_count",
        params={},
        consumes={
            "count": "ca/rental_coowner",
            "when_none": "ca/rental_cca_table_claim",
            "when_any": "ca/rental_coowner_cca_claim",
        },
        produces={"output": "ca/rental_cca_claim_share"},
    ),
    # T776 "Line 9936: Total CCA claim for the year (amount ii from Area A minus any personal
    # part of CCA, and any CCA for business-use-of home expenses)", first step: amount ii minus
    # the personal part of CCA, a caller input.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/rental_cca_claim_share",
            "less": "ca/rental_cca_personal_part",
        },
        produces={"output": "ca/rental_cca_claim_less_personal_part"},
    ),
    # T776 "Line 9936: Total CCA claim for the year (amount ii from Area A minus any personal
    # part of CCA, and any CCA for business-use-of home expenses)", second step: that result
    # minus the CCA for business-use-of-home expenses, a caller input.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/rental_cca_claim_less_personal_part",
            "less": "ca/rental_cca_business_use_of_home",
        },
        produces={"output": "ca/rental_cca_claim_before_limit"},
    ),
    # Guide T4036: "You cannot use CCA to create or increase a rental loss": the most line 9936
    # may be is amount 5 ("Line 5: Subtotal (amount 4 minus line 9948)"), or 0 when amount 5 is
    # negative.
    CapabilitySelection(
        name="core/sum_not_below_zero",
        params={},
        consumes={"parts": ("ca/rental_net_income_after_terminal_loss",)},
        produces={"output": "ca/rental_cca_limit"},
    ),
    # T776 "Line 9936: Total CCA claim for the year": the claim above, at most that limit. A claim
    # above it is refused, not capped, which also covers Classes 31 and 32.
    CapabilitySelection(
        name="core/at_most",
        params={},
        consumes={
            "amount": "ca/rental_cca_claim_before_limit",
            "bound": "ca/rental_cca_limit",
        },
        produces={"output": "ca/rental_cca_claim"},
    ),
    # T776 Area A "Column 24: UCC at the end of the year (column 7 minus column 23)": the class
    # number and column 24 of each class of the Area A list, a product of the return for next
    # year's column 2.
    CapabilitySelection(
        name="ca/closing_ucc",
        params={"class_rates": "ca/cca_class_rates"},
        consumes={"classes": "ca/rental_cca_classes"},
        produces={"output": "ca/rental_closing_ucc"},
    ),
    # T776 "Line 6: Net income (loss) (amount 5 minus line 9936)": line 9936 is computed above.
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
    # line 32); line 27 "Add lines 22 to 26. Net self-employment income" (line 28 is line 21 plus
    # line 27) comes after line 20, before lines 29 to 31 (line 32).
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
                "ca/net_self_employment_income",
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
    # order. Line 28 "Line 21 plus line 27" is not a step of its own: total income (line 15000)
    # adds line 27 to the lines 1 to 20, in line order.
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
    # T2125 Part 3A "Subtotal: Amount 3A minus amount 3B 3C": amount 3A "Gross sales,
    # commissions, or fees (include GST/HST collected or collectible)" less amount 3B
    # "GST/HST, provincial sales tax, returns, allowances, discounts, and GST/HST
    # adjustments (included in amount 3A)", both caller inputs.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/business_gross_sales",
            "less": "ca/business_sales_adjustments",
        },
        produces={"output": "ca/business_sales_subtotal"},
    ),
    # T2125 Part 3A "If you are using the quick method for GST/HST - Government assistance
    # calculated as follows:" "Subtotal: Amount 3D minus amount 3E 3F": amount 3D "GST/HST
    # collected or collectible on sales, commissions, and fees eligible for the quick
    # method" less amount 3E "GST/HST remitted: (sales, commissions, and fees eligible for
    # the quick method plus GST/HST collected or collectible) multiplied by the applicable
    # quick method remittance rate", both caller inputs (no capability multiplies by a rate
    # the caller enters). Signed: 3F may be below zero.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/business_quick_method_gst_hst",
            "less": "ca/business_quick_method_remitted",
        },
        produces={"output": "ca/business_quick_method_assistance"},
    ),
    # T2125 Part 3A "Adjusted gross sales: Amount 3C plus amount 3F (enter on line 8000 of
    # Part 3C)"; Part 3C line 8000 "Adjusted gross sales (amount 3G) or adjusted
    # professional fees (amount 3N)" is the same artifact, so it has no step of its own.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/business_sales_subtotal",
                "ca/business_quick_method_assistance",
            ),
        },
        produces={"output": "ca/business_adjusted_gross_sales"},
    ),
    # T2125 Area A endnote 3 "If you have a negative amount in column 7, add it to income as
    # a recapture in Part 3C on line 8230. ... Recapture and terminal loss do not apply to a
    # Class 10.1 property unless it is a DIEP.": the recapture of each class of the Area A
    # list (column 7 made positive when negative), totalled.
    CapabilitySelection(
        name="ca/recaptured_cca",
        params={"class_rates": "ca/cca_class_rates"},
        consumes={
            "classes": "ca/business_cca_classes",
        },
        produces={"output": "ca/business_recaptured_cca"},
    ),
    # T2125 Part 3C line 8230 "Other income (specify):", which takes the recapture of Area A
    # (endnote 3 "add it to income as a recapture in Part 3C on line 8230"): the other
    # income the caller specifies plus the recapture.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/business_other_income",
                "ca/business_recaptured_cca",
            ),
        },
        produces={"output": "ca/business_other_income_with_recapture"},
    ),
    # T2125 Part 3C "Subtotal: Line 8290 plus line 8230 3O": line 8290 "Reserves deducted
    # last year", a caller input, plus line 8230.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/business_reserves_deducted_last_year",
                "ca/business_other_income_with_recapture",
            ),
        },
        produces={"output": "ca/business_reserves_and_other_income"},
    ),
    # T2125 Part 3C "Gross business or professional income: Line 8000 plus amount 3O" (line
    # 8299), "Report the gross business or professional income from line 8299 on the
    # applicable line of your income tax and benefit return as indicated below: business
    # income on line 13499"; line 8000 is amount 3G above.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/business_adjusted_gross_sales",
                "ca/business_reserves_and_other_income",
            ),
        },
        produces={"output": "ca/business_gross_income"},
    ),
    # T2125 Part 3D "Gross business income (line 8299 of Part 3C). 3P".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": ("ca/business_gross_income",),
        },
        produces={"output": "ca/business_gross_income_for_gross_profit"},
    ),
    # T2125 Part 3D "Subtotal: Add amounts 3Q to 3U. 3V": 3Q "Opening inventory (include raw
    # materials, goods in process, and finished goods)", 3R "Purchases during the year (net
    # of returns, allowances, and discounts)", 3S "Direct wage costs", 3T "Subcontracts" and
    # 3U "Other costs", all caller inputs.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/business_opening_inventory",
                "ca/business_purchases",
                "ca/business_direct_wage_costs",
                "ca/business_subcontracts",
                "ca/business_other_costs",
            ),
        },
        produces={"output": "ca/business_cost_of_goods_subtotal"},
    ),
    # T2125 Part 3D "Cost of goods sold: Amount 3V minus line 8500 8518": line 8500 "Closing
    # inventory (include raw materials, goods in process, and finished goods)", a caller
    # input.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/business_cost_of_goods_subtotal",
            "less": "ca/business_closing_inventory",
        },
        produces={"output": "ca/business_cost_of_goods_sold"},
    ),
    # T2125 Part 3D "Gross profit (or loss): Amount 3P minus line 8518." (line 8519):
    # signed, a loss is negative.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/business_gross_income_for_gross_profit",
            "less": "ca/business_cost_of_goods_sold",
        },
        produces={"output": "ca/business_gross_profit"},
    ),
    # T2125 Part 4 "Gross business or professional income (line 8299 of Part 3C) or Gross
    # profit (line 8519 of Part 3D). 4A": for a business statement, which has a Part 3D, it
    # is line 8519.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": ("ca/business_gross_profit",),
        },
        produces={"output": "ca/business_gross_income_before_expenses"},
    ),
    # T2125 Area A "Total CCA claim for the year: Total of column 21 (enter on line 9936 of
    # Part 4 amount ii minus any personal part and any CCA for business-use-of-home
    # expenses)" (amount ii): the CCA claimed on each class of the Area A list, at most its
    # maximum (column 19 multiplied by column 20), totalled.
    CapabilitySelection(
        name="ca/cca_claim",
        params={"class_rates": "ca/cca_class_rates"},
        consumes={
            "classes": "ca/business_cca_classes",
        },
        produces={"output": "ca/business_cca_table_claim"},
    ),
    # T2125 Part 4 "Capital cost allowance (CCA). Enter amount ii of Area A minus any
    # personal part and any CCA for business-use-of-home expenses 9936 4U", first step:
    # amount ii minus the personal part of CCA, a caller input.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/business_cca_table_claim",
            "less": "ca/business_cca_personal_part",
        },
        produces={"output": "ca/business_cca_claim_less_personal_part"},
    ),
    # T2125 Part 4 line 9936 (amount 4U) "Capital cost allowance (CCA). Enter amount ii of
    # Area A minus any personal part and any CCA for business-use-of-home expenses", second
    # step: that result minus the CCA for business-use-of-home expenses, amount 7K "Capital
    # cost allowance (business part only)", a caller input.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/business_cca_claim_less_personal_part",
            "less": "ca/business_home_cca",
        },
        produces={"output": "ca/business_cca_claim"},
    ),
    # T2125 Area A endnote 3 "If no property is left in the class and there is a positive
    # amount in this column, deduct the amount from income as a terminal loss in Part 4 on
    # line 9270. Recapture and terminal loss do not apply to a Class 10.1 property unless it
    # is a DIEP.": the terminal loss of each class of the Area A list, totalled.
    CapabilitySelection(
        name="ca/terminal_loss",
        params={"class_rates": "ca/cca_class_rates"},
        consumes={
            "classes": "ca/business_cca_classes",
        },
        produces={"output": "ca/business_terminal_loss"},
    ),
    # T2125 Part 4 "Other expenses (specify): 9270 4V", which takes the terminal loss of
    # Area A (endnote 3 "deduct the amount from income as a terminal loss in Part 4 on line
    # 9270"): the other expenses the caller specifies plus the terminal loss.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/business_other_expenses",
                "ca/business_terminal_loss",
            ),
        },
        produces={"output": "ca/business_other_expenses_with_terminal_loss"},
    ),
    # T2125 Area A column 22 "UCC at the end of the year (col. 7 minus col. 21)": the class
    # number and column 22 of each class of the Area A list, a product of the return for
    # next year's column 1.
    CapabilitySelection(
        name="ca/closing_ucc",
        params={"class_rates": "ca/cca_class_rates"},
        consumes={
            "classes": "ca/business_cca_classes",
        },
        produces={"output": "ca/business_closing_ucc"},
    ),
    # T2125 Part 4 "Total expenses: Total of amounts 4B to 4V 9368": the 19 expense lines 4B
    # to 4T ("Advertising" to "Motor vehicle expenses (not including CCA) (amount 16 of
    # Chart A)", each a caller input, amount 16 of Chart A entered as its line), then 4U
    # (line 9936) and 4V (line 9270), in the form's order.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/business_advertising",
                "ca/business_meals_and_entertainment",
                "ca/business_bad_debts",
                "ca/business_insurance",
                "ca/business_interest_and_bank_charges",
                "ca/business_business_taxes_licences_and_memberships",
                "ca/business_office_expenses",
                "ca/business_office_stationery_and_supplies",
                "ca/business_professional_fees",
                "ca/business_management_and_administration_fees",
                "ca/business_rent",
                "ca/business_repairs_and_maintenance",
                "ca/business_salaries_wages_and_benefits",
                "ca/business_property_taxes",
                "ca/business_travel_expenses",
                "ca/business_utilities",
                "ca/business_fuel_costs",
                "ca/business_delivery_freight_and_express",
                "ca/business_motor_vehicle_expenses",
                "ca/business_cca_claim",
                "ca/business_other_expenses_with_terminal_loss",
            ),
        },
        produces={"output": "ca/business_total_expenses"},
    ),
    # T2125 Part 4 "Net income (loss) before adjustments: Amount 4A minus line 9368" (line
    # 9369): signed, a loss is negative.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/business_gross_income_before_expenses",
            "less": "ca/business_total_expenses",
        },
        produces={"output": "ca/business_net_income_before_adjustments"},
    ),
    # T2125 Part 5 "Your share of line 9369 or the amount from your T5013 slip, Statement of
    # Partnership Income. 5A": a count of 1 for a partner (a caller's 0 or 1) chooses the
    # amount from the T5013 slip, as entered; with a count of 0 it is line 9369.
    CapabilitySelection(
        name="core/choose_by_count",
        params={},
        consumes={
            "count": "ca/business_partner",
            "when_none": "ca/business_net_income_before_adjustments",
            "when_any": "ca/business_partner_share",
        },
        produces={"output": "ca/business_share_of_net_income"},
    ),
    # T2125 Part 6 "Total other amounts deductible from your share of the net partnership
    # income (loss): Add amounts 6A to 6E (enter this on line 9943 of Part 5). 6F": 6A to 6E
    # "List details of expenses: Expense amounts", caller inputs.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/business_partner_other_amount_a",
                "ca/business_partner_other_amount_b",
                "ca/business_partner_other_amount_c",
                "ca/business_partner_other_amount_d",
                "ca/business_partner_other_amount_e",
            ),
        },
        produces={"output": "ca/business_partner_other_amounts_total"},
    ),
    # T2125 Part 5 "Other amounts deductible from your share of net partnership income
    # (loss) (amount 6F)" (line 9943).
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": ("ca/business_partner_other_amounts_total",),
        },
        produces={"output": "ca/business_partner_other_amounts"},
    ),
    # T2125 Part 5 "Total: Amount 5A plus amount 5B plus line 9974 5C": amount 5B "Canadian
    # journalism labour tax credit allocated to you in the year (box 236 of your T5013
    # slip)" and line 9974 "GST/HST rebate for partners received in the year", caller
    # inputs.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/business_share_of_net_income",
                "ca/business_journalism_labour_tax_credit",
                "ca/business_partner_gst_hst_rebate",
            ),
        },
        produces={"output": "ca/business_partnership_total"},
    ),
    # T2125 Part 5 "Net income (loss) after adjustments: Amount 5C minus line 9943 5D":
    # signed, a loss is negative.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/business_partnership_total",
            "less": "ca/business_partner_other_amounts",
        },
        produces={"output": "ca/business_net_income_after_adjustments"},
    ),
    # T2125 Part 7 "Subtotal: Add amounts 7A to 7G. 7H": 7A "Heat", 7B "Electricity", 7C
    # "Insurance", 7D "Maintenance", 7E "Mortgage interest", 7F "Property taxes" and 7G
    # "Other expenses (specify)", caller inputs.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/business_home_heat",
                "ca/business_home_electricity",
                "ca/business_home_insurance",
                "ca/business_home_maintenance",
                "ca/business_home_mortgage_interest",
                "ca/business_home_property_taxes",
                "ca/business_home_other_expenses",
            ),
        },
        produces={"output": "ca/business_home_expenses_subtotal"},
    ),
    # T2125 Part 7 "Subtotal: Amount 7H minus amount 7I 7J": amount 7I "Personal-use part of
    # the business-use-of-home expenses", a caller input.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/business_home_expenses_subtotal",
            "less": "ca/business_home_personal_use_part",
        },
        produces={"output": "ca/business_home_expenses_business_part"},
    ),
    # T2125 Part 7 "Subtotal: Add amounts 7J to 7L. 7M": 7K "Capital cost allowance
    # (business part only), which means amount ii of Area A minus any portion of capital
    # cost allowance that is for personal use or entered on line 9936 of Part 4" and 7L
    # "Amount carried forward from previous year", caller inputs.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/business_home_expenses_business_part",
                "ca/business_home_cca",
                "ca/business_home_carried_forward",
            ),
        },
        produces={"output": "ca/business_home_expenses_available"},
    ),
    # T2125 Part 7 "Net income (loss) after adjustments (amount 5D) (if negative, enter
    # "0"). 7N": amount 5D, or 0 when it is negative.
    CapabilitySelection(
        name="core/sum_not_below_zero",
        params={},
        consumes={
            "parts": ("ca/business_net_income_after_adjustments",),
        },
        produces={"output": "ca/business_home_income_limit"},
    ),
    # T2125 Part 7 "Business-use-of-home expenses available to carry forward: Amount 7M
    # minus amount 7N (if negative, enter "0") 7O": the claim left over, 0 when amount 7N is
    # the larger.
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/business_home_expenses_available",
            "less": "ca/business_home_income_limit",
        },
        produces={"output": "ca/business_home_carry_forward"},
    ),
    # T2125 Part 7 "Allowable claim: Amount 7M or 7N above, whichever is less (enter your
    # share of this amount on line 9945 of Part 5) 7P".
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={
            "amounts": (
                "ca/business_home_expenses_available",
                "ca/business_home_income_limit",
            ),
        },
        produces={"output": "ca/business_home_allowable_claim"},
    ),
    # T2125 Part 5 "Business-use-of-home expenses (amount 7P)" (line 9945).
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": ("ca/business_home_allowable_claim",),
        },
        produces={"output": "ca/business_home_expenses"},
    ),
    # T2125 Part 5 "Your net income (loss): Amount 5D minus line 9945" (line 9946), "Report
    # the net income amount from line 9946 on the applicable line of your income tax and
    # benefit return as indicated below: business income on line 13500"; T1 "Line 22:
    # Business income" is the same artifact, signed: a loss is negative.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/business_net_income_after_adjustments",
            "less": "ca/business_home_expenses",
        },
        produces={"output": "ca/business_income"},
    ),
}

WIRING = {
    (ApplyRate, frozenset({CAPITAL_GAIN}), frozenset({INCLUDED_CAPITAL_GAIN})),
    (
        SumNotBelowZero,
        frozenset({INCLUDED_CAPITAL_GAIN, PARTNERSHIP_GAINS_AT_FULL_INCLUSION}),
        frozenset({TAXABLE_CAPITAL_GAINS}),
    ),
    (DispositionGains, frozenset({QSBCS_DISPOSITIONS}), frozenset({QSBCS_GAIN_OR_LOSS})),
    (DispositionGains, frozenset({QFFP_DISPOSITIONS}), frozenset({QFFP_GAIN_OR_LOSS})),
    (
        DispositionGains,
        frozenset({QFFP_FORECLOSURE_DISPOSITIONS}),
        frozenset({QFFP_FORECLOSURE_GAIN_OR_LOSS}),
    ),
    (DispositionGains, frozenset({SHARE_DISPOSITIONS}), frozenset({SHARE_GAIN_OR_LOSS})),
    (
        DispositionGains,
        frozenset({REAL_ESTATE_DISPOSITIONS}),
        frozenset({REAL_ESTATE_GAIN_OR_LOSS}),
    ),
    (DispositionGains, frozenset({BOND_DISPOSITIONS}), frozenset({BOND_GAIN_OR_LOSS})),
    (
        DispositionGains,
        frozenset({CRYPTO_ASSET_DISPOSITIONS}),
        frozenset({CRYPTO_ASSET_GAIN_OR_LOSS}),
    ),
    (
        DispositionGains,
        frozenset({OTHER_FORECLOSURE_DISPOSITIONS}),
        frozenset({OTHER_FORECLOSURE_GAIN_OR_LOSS}),
    ),
    (
        DispositionProceeds,
        frozenset({QSBCS_DISPOSITIONS}),
        frozenset({QSBCS_PROCEEDS}),
    ),
    (
        DispositionProceeds,
        frozenset({QFFP_DISPOSITIONS}),
        frozenset({QFFP_PROCEEDS}),
    ),
    (
        DispositionProceeds,
        frozenset({QFFP_FORECLOSURE_DISPOSITIONS}),
        frozenset({QFFP_FORECLOSURE_PROCEEDS}),
    ),
    (
        DispositionProceeds,
        frozenset({SHARE_DISPOSITIONS}),
        frozenset({SHARE_PROCEEDS}),
    ),
    (
        DispositionProceeds,
        frozenset({REAL_ESTATE_DISPOSITIONS}),
        frozenset({REAL_ESTATE_PROCEEDS}),
    ),
    (
        DispositionProceeds,
        frozenset({BOND_DISPOSITIONS}),
        frozenset({BOND_PROCEEDS}),
    ),
    (
        DispositionProceeds,
        frozenset({CRYPTO_ASSET_DISPOSITIONS}),
        frozenset({CRYPTO_ASSET_PROCEEDS}),
    ),
    (
        DispositionProceeds,
        frozenset({OTHER_FORECLOSURE_DISPOSITIONS}),
        frozenset({OTHER_FORECLOSURE_PROCEEDS}),
    ),
    (
        DispositionGainsOnly,
        frozenset({PERSONAL_USE_PROPERTY_DISPOSITIONS}),
        frozenset({PERSONAL_USE_PROPERTY_GAIN_ROWS}),
    ),
    (
        PrincipalResidenceGain,
        frozenset({PRINCIPAL_RESIDENCE_PROPERTIES}),
        frozenset({PRINCIPAL_RESIDENCE_GAIN}),
    ),
    (
        Sum,
        frozenset({PERSONAL_USE_PROPERTY_GAIN_ROWS, PRINCIPAL_RESIDENCE_GAIN}),
        frozenset({PERSONAL_USE_PROPERTY_GAIN}),
    ),
    (
        DispositionGains,
        frozenset({LISTED_PERSONAL_PROPERTY_DISPOSITIONS}),
        frozenset({LISTED_PERSONAL_PROPERTY_GAIN_OR_LOSS}),
    ),
    (
        SubtractNotBelowZero,
        frozenset(
            {LISTED_PERSONAL_PROPERTY_GAIN_OR_LOSS, UNAPPLIED_LISTED_PERSONAL_PROPERTY_LOSSES}
        ),
        frozenset({LISTED_PERSONAL_PROPERTY_NET_GAIN}),
    ),
    (
        Sum,
        frozenset(
            {
                QSBCS_GAIN_OR_LOSS,
                QFFP_GAIN_OR_LOSS,
                QFFP_FORECLOSURE_GAIN_OR_LOSS,
                SHARE_GAIN_OR_LOSS,
                REAL_ESTATE_GAIN_OR_LOSS,
                BOND_GAIN_OR_LOSS,
                CRYPTO_ASSET_GAIN_OR_LOSS,
                OTHER_FORECLOSURE_GAIN_OR_LOSS,
                PERSONAL_USE_PROPERTY_GAIN,
                LISTED_PERSONAL_PROPERTY_NET_GAIN,
            }
        ),
        frozenset({CAPITAL_GAINS_OF_QUALIFIED_AND_OTHER_PROPERTIES}),
    ),
    (
        Subtract,
        frozenset({CAPITAL_GAINS_OF_QUALIFIED_AND_OTHER_PROPERTIES, CAPITAL_GAINS_DEFERRAL}),
        frozenset({CAPITAL_GAINS_AFTER_DEFERRAL}),
    ),
    (
        Sum,
        frozenset(
            {CAPITAL_GAINS_AFTER_DEFERRAL, SLIP_CAPITAL_GAINS_OR_LOSSES, T3_CAPITAL_GAINS_OR_LOSSES}
        ),
        frozenset({CAPITAL_GAINS_BEFORE_INVESTMENT_LOSS_REDUCTION}),
    ),
    (
        Subtract,
        frozenset(
            {CAPITAL_GAINS_BEFORE_INVESTMENT_LOSS_REDUCTION, BUSINESS_INVESTMENT_LOSS_REDUCTION}
        ),
        frozenset({CAPITAL_GAINS_BEFORE_RESERVES}),
    ),
    (
        Sum,
        frozenset({CAPITAL_GAINS_BEFORE_RESERVES, CAPITAL_GAINS_RESERVES}),
        frozenset({CAPITAL_GAIN}),
    ),
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
        ShortTermRentalNonCompliantCca,
        frozenset({SHORT_TERM_RENTAL_CCA_UNITS}),
        frozenset({RENTAL_NON_COMPLIANT_CCA}),
    ),
    (
        ShortTermRentalNonCompliantCcaByClass,
        frozenset({SHORT_TERM_RENTAL_CCA_UNITS}),
        frozenset({SHORT_TERM_RENTAL_NON_COMPLIANT_CCA_BY_CLASS}),
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
    (RecapturedCca, frozenset({RENTAL_CCA_CLASSES}), frozenset({RENTAL_CCA_TABLE_RECAPTURE})),
    (
        ChooseByCount,
        frozenset({RENTAL_COOWNER, RENTAL_CCA_TABLE_RECAPTURE, RENTAL_COOWNER_RECAPTURED_CCA}),
        frozenset({RENTAL_RECAPTURED_CCA}),
    ),
    (TerminalLoss, frozenset({RENTAL_CCA_CLASSES}), frozenset({RENTAL_CCA_TABLE_TERMINAL_LOSS})),
    (
        ChooseByCount,
        frozenset({RENTAL_COOWNER, RENTAL_CCA_TABLE_TERMINAL_LOSS, RENTAL_COOWNER_TERMINAL_LOSS}),
        frozenset({RENTAL_TERMINAL_LOSS}),
    ),
    (CcaClaim, frozenset({RENTAL_CCA_CLASSES}), frozenset({RENTAL_CCA_TABLE_CLAIM})),
    (
        ChooseByCount,
        frozenset({RENTAL_COOWNER, RENTAL_CCA_TABLE_CLAIM, RENTAL_COOWNER_CCA_CLAIM}),
        frozenset({RENTAL_CCA_CLAIM_SHARE}),
    ),
    (
        Subtract,
        frozenset({RENTAL_CCA_CLAIM_SHARE, RENTAL_CCA_PERSONAL_PART}),
        frozenset({RENTAL_CCA_CLAIM_LESS_PERSONAL_PART}),
    ),
    (
        Subtract,
        frozenset({RENTAL_CCA_CLAIM_LESS_PERSONAL_PART, RENTAL_CCA_BUSINESS_USE_OF_HOME}),
        frozenset({RENTAL_CCA_CLAIM_BEFORE_LIMIT}),
    ),
    (
        SumNotBelowZero,
        frozenset({RENTAL_NET_INCOME_AFTER_TERMINAL_LOSS}),
        frozenset({RENTAL_CCA_LIMIT}),
    ),
    (
        AtMost,
        frozenset({RENTAL_CCA_CLAIM_BEFORE_LIMIT, RENTAL_CCA_LIMIT}),
        frozenset({RENTAL_CCA_CLAIM}),
    ),
    (ClosingUcc, frozenset({RENTAL_CCA_CLASSES}), frozenset({RENTAL_CLOSING_UCC})),
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
                NET_SELF_EMPLOYMENT_INCOME,
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
    (
        Subtract,
        frozenset(
            {
                BUSINESS_GROSS_SALES,
                BUSINESS_SALES_ADJUSTMENTS,
            }
        ),
        frozenset({BUSINESS_SALES_SUBTOTAL}),
    ),
    (
        Subtract,
        frozenset(
            {
                BUSINESS_QUICK_METHOD_GST_HST,
                BUSINESS_QUICK_METHOD_REMITTED,
            }
        ),
        frozenset({BUSINESS_QUICK_METHOD_ASSISTANCE}),
    ),
    (
        Sum,
        frozenset(
            {
                BUSINESS_SALES_SUBTOTAL,
                BUSINESS_QUICK_METHOD_ASSISTANCE,
            }
        ),
        frozenset({BUSINESS_ADJUSTED_GROSS_SALES}),
    ),
    (
        RecapturedCca,
        frozenset(
            {
                BUSINESS_CCA_CLASSES,
            }
        ),
        frozenset({BUSINESS_RECAPTURED_CCA}),
    ),
    (
        Sum,
        frozenset(
            {
                BUSINESS_OTHER_INCOME,
                BUSINESS_RECAPTURED_CCA,
            }
        ),
        frozenset({BUSINESS_OTHER_INCOME_WITH_RECAPTURE}),
    ),
    (
        Sum,
        frozenset(
            {
                BUSINESS_RESERVES_DEDUCTED_LAST_YEAR,
                BUSINESS_OTHER_INCOME_WITH_RECAPTURE,
            }
        ),
        frozenset({BUSINESS_RESERVES_AND_OTHER_INCOME}),
    ),
    (
        Sum,
        frozenset(
            {
                BUSINESS_ADJUSTED_GROSS_SALES,
                BUSINESS_RESERVES_AND_OTHER_INCOME,
            }
        ),
        frozenset({BUSINESS_GROSS_INCOME}),
    ),
    (
        Sum,
        frozenset(
            {
                BUSINESS_GROSS_INCOME,
            }
        ),
        frozenset({BUSINESS_GROSS_INCOME_FOR_GROSS_PROFIT}),
    ),
    (
        Sum,
        frozenset(
            {
                BUSINESS_OPENING_INVENTORY,
                BUSINESS_PURCHASES,
                BUSINESS_DIRECT_WAGE_COSTS,
                BUSINESS_SUBCONTRACTS,
                BUSINESS_OTHER_COSTS,
            }
        ),
        frozenset({BUSINESS_COST_OF_GOODS_SUBTOTAL}),
    ),
    (
        Subtract,
        frozenset(
            {
                BUSINESS_COST_OF_GOODS_SUBTOTAL,
                BUSINESS_CLOSING_INVENTORY,
            }
        ),
        frozenset({BUSINESS_COST_OF_GOODS_SOLD}),
    ),
    (
        Subtract,
        frozenset(
            {
                BUSINESS_GROSS_INCOME_FOR_GROSS_PROFIT,
                BUSINESS_COST_OF_GOODS_SOLD,
            }
        ),
        frozenset({BUSINESS_GROSS_PROFIT}),
    ),
    (
        Sum,
        frozenset(
            {
                BUSINESS_GROSS_PROFIT,
            }
        ),
        frozenset({BUSINESS_GROSS_INCOME_BEFORE_EXPENSES}),
    ),
    (
        CcaClaim,
        frozenset(
            {
                BUSINESS_CCA_CLASSES,
            }
        ),
        frozenset({BUSINESS_CCA_TABLE_CLAIM}),
    ),
    (
        Subtract,
        frozenset(
            {
                BUSINESS_CCA_TABLE_CLAIM,
                BUSINESS_CCA_PERSONAL_PART,
            }
        ),
        frozenset({BUSINESS_CCA_CLAIM_LESS_PERSONAL_PART}),
    ),
    (
        Subtract,
        frozenset(
            {
                BUSINESS_CCA_CLAIM_LESS_PERSONAL_PART,
                BUSINESS_HOME_CCA,
            }
        ),
        frozenset({BUSINESS_CCA_CLAIM}),
    ),
    (
        TerminalLoss,
        frozenset(
            {
                BUSINESS_CCA_CLASSES,
            }
        ),
        frozenset({BUSINESS_TERMINAL_LOSS}),
    ),
    (
        Sum,
        frozenset(
            {
                BUSINESS_OTHER_EXPENSES,
                BUSINESS_TERMINAL_LOSS,
            }
        ),
        frozenset({BUSINESS_OTHER_EXPENSES_WITH_TERMINAL_LOSS}),
    ),
    (
        ClosingUcc,
        frozenset(
            {
                BUSINESS_CCA_CLASSES,
            }
        ),
        frozenset({BUSINESS_CLOSING_UCC}),
    ),
    (
        Sum,
        frozenset(
            {
                BUSINESS_ADVERTISING,
                BUSINESS_MEALS_AND_ENTERTAINMENT,
                BUSINESS_BAD_DEBTS,
                BUSINESS_INSURANCE,
                BUSINESS_INTEREST_AND_BANK_CHARGES,
                BUSINESS_BUSINESS_TAXES_LICENCES_AND_MEMBERSHIPS,
                BUSINESS_OFFICE_EXPENSES,
                BUSINESS_OFFICE_STATIONERY_AND_SUPPLIES,
                BUSINESS_PROFESSIONAL_FEES,
                BUSINESS_MANAGEMENT_AND_ADMINISTRATION_FEES,
                BUSINESS_RENT,
                BUSINESS_REPAIRS_AND_MAINTENANCE,
                BUSINESS_SALARIES_WAGES_AND_BENEFITS,
                BUSINESS_PROPERTY_TAXES,
                BUSINESS_TRAVEL_EXPENSES,
                BUSINESS_UTILITIES,
                BUSINESS_FUEL_COSTS,
                BUSINESS_DELIVERY_FREIGHT_AND_EXPRESS,
                BUSINESS_MOTOR_VEHICLE_EXPENSES,
                BUSINESS_CCA_CLAIM,
                BUSINESS_OTHER_EXPENSES_WITH_TERMINAL_LOSS,
            }
        ),
        frozenset({BUSINESS_TOTAL_EXPENSES}),
    ),
    (
        Subtract,
        frozenset(
            {
                BUSINESS_GROSS_INCOME_BEFORE_EXPENSES,
                BUSINESS_TOTAL_EXPENSES,
            }
        ),
        frozenset({BUSINESS_NET_INCOME_BEFORE_ADJUSTMENTS}),
    ),
    (
        ChooseByCount,
        frozenset(
            {
                BUSINESS_PARTNER,
                BUSINESS_NET_INCOME_BEFORE_ADJUSTMENTS,
                BUSINESS_PARTNER_SHARE,
            }
        ),
        frozenset({BUSINESS_SHARE_OF_NET_INCOME}),
    ),
    (
        Sum,
        frozenset(
            {
                BUSINESS_PARTNER_OTHER_AMOUNT_A,
                BUSINESS_PARTNER_OTHER_AMOUNT_B,
                BUSINESS_PARTNER_OTHER_AMOUNT_C,
                BUSINESS_PARTNER_OTHER_AMOUNT_D,
                BUSINESS_PARTNER_OTHER_AMOUNT_E,
            }
        ),
        frozenset({BUSINESS_PARTNER_OTHER_AMOUNTS_TOTAL}),
    ),
    (
        Sum,
        frozenset(
            {
                BUSINESS_PARTNER_OTHER_AMOUNTS_TOTAL,
            }
        ),
        frozenset({BUSINESS_PARTNER_OTHER_AMOUNTS}),
    ),
    (
        Sum,
        frozenset(
            {
                BUSINESS_SHARE_OF_NET_INCOME,
                BUSINESS_JOURNALISM_LABOUR_TAX_CREDIT,
                BUSINESS_PARTNER_GST_HST_REBATE,
            }
        ),
        frozenset({BUSINESS_PARTNERSHIP_TOTAL}),
    ),
    (
        Subtract,
        frozenset(
            {
                BUSINESS_PARTNERSHIP_TOTAL,
                BUSINESS_PARTNER_OTHER_AMOUNTS,
            }
        ),
        frozenset({BUSINESS_NET_INCOME_AFTER_ADJUSTMENTS}),
    ),
    (
        Sum,
        frozenset(
            {
                BUSINESS_HOME_HEAT,
                BUSINESS_HOME_ELECTRICITY,
                BUSINESS_HOME_INSURANCE,
                BUSINESS_HOME_MAINTENANCE,
                BUSINESS_HOME_MORTGAGE_INTEREST,
                BUSINESS_HOME_PROPERTY_TAXES,
                BUSINESS_HOME_OTHER_EXPENSES,
            }
        ),
        frozenset({BUSINESS_HOME_EXPENSES_SUBTOTAL}),
    ),
    (
        Subtract,
        frozenset(
            {
                BUSINESS_HOME_EXPENSES_SUBTOTAL,
                BUSINESS_HOME_PERSONAL_USE_PART,
            }
        ),
        frozenset({BUSINESS_HOME_EXPENSES_BUSINESS_PART}),
    ),
    (
        Sum,
        frozenset(
            {
                BUSINESS_HOME_EXPENSES_BUSINESS_PART,
                BUSINESS_HOME_CCA,
                BUSINESS_HOME_CARRIED_FORWARD,
            }
        ),
        frozenset({BUSINESS_HOME_EXPENSES_AVAILABLE}),
    ),
    (
        SumNotBelowZero,
        frozenset(
            {
                BUSINESS_NET_INCOME_AFTER_ADJUSTMENTS,
            }
        ),
        frozenset({BUSINESS_HOME_INCOME_LIMIT}),
    ),
    (
        SubtractNotBelowZero,
        frozenset(
            {
                BUSINESS_HOME_EXPENSES_AVAILABLE,
                BUSINESS_HOME_INCOME_LIMIT,
            }
        ),
        frozenset({BUSINESS_HOME_CARRY_FORWARD}),
    ),
    (
        LesserOf,
        frozenset(
            {
                BUSINESS_HOME_EXPENSES_AVAILABLE,
                BUSINESS_HOME_INCOME_LIMIT,
            }
        ),
        frozenset({BUSINESS_HOME_ALLOWABLE_CLAIM}),
    ),
    (
        Sum,
        frozenset(
            {
                BUSINESS_HOME_ALLOWABLE_CLAIM,
            }
        ),
        frozenset({BUSINESS_HOME_EXPENSES}),
    ),
    (
        Subtract,
        frozenset(
            {
                BUSINESS_NET_INCOME_AFTER_ADJUSTMENTS,
                BUSINESS_HOME_EXPENSES,
            }
        ),
        frozenset({BUSINESS_INCOME}),
    ),
}
