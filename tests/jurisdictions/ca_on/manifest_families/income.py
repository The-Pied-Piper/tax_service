"""The CA-ON manifest entries of one family of lines (see `test_manifest.py`)."""

from __future__ import annotations

from app.domain.capabilities.apply_fraction import ApplyFraction
from app.domain.capabilities.apply_rate import ApplyRate
from app.domain.capabilities.apply_ratio import ApplyRatio
from app.domain.capabilities.choose_by_count import ChooseByCount
from app.domain.capabilities.greater_of import GreaterOf
from app.domain.capabilities.lesser_of import LesserOf
from app.domain.capabilities.subtract import Subtract
from app.domain.capabilities.subtract_not_below_zero import SubtractNotBelowZero
from app.domain.capabilities.sum import Sum
from app.domain.capabilities.sum_not_below_zero import SumNotBelowZero
from app.domain.manifest import CapabilitySelection
from app.jurisdictions.ca.capabilities.apply_percentage import ApplyPercentage
from app.jurisdictions.ca.capabilities.apply_ratio_or_zero import ApplyRatioOrZero
from app.jurisdictions.ca.capabilities.cca_claim import CcaClaim
from app.jurisdictions.ca.capabilities.closing_ucc import ClosingUcc
from app.jurisdictions.ca.capabilities.disposition_gains import DispositionGains
from app.jurisdictions.ca.capabilities.disposition_gains_only import DispositionGainsOnly
from app.jurisdictions.ca.capabilities.disposition_proceeds import DispositionProceeds
from app.jurisdictions.ca.capabilities.principal_residence_gain import PrincipalResidenceGain
from app.jurisdictions.ca.capabilities.recaptured_cca import RecapturedCca
from app.jurisdictions.ca.capabilities.terminal_loss import TerminalLoss
from app.jurisdictions.ca.catalog import (
    AMT_MINIMUM_TAX_CARRYOVER_APPLIED,
    BOND_DISPOSITIONS,
    BOND_GAIN_OR_LOSS,
    BOND_PROCEEDS,
    BUSINESS_INCOME,
    BUSINESS_INVESTMENT_LOSS_REDUCTION,
    BUSINESS_VEHICLE_DAYS_DIVISOR,
    BUSINESS_VEHICLE_INTEREST_LIMIT,
    BUSINESS_VEHICLE_LEASE_CHARGE_LIMIT,
    BUSINESS_VEHICLE_LEASE_COST_LIMIT,
    BUSINESS_VEHICLE_LIST_PRICE_LIMIT,
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
    FISH_BUSINESS_TAXES_LICENCES_AND_MEMBERSHIPS,
    FISH_CCA_CLAIM,
    FISH_CCA_CLAIM_LESS_PERSONAL_PART,
    FISH_CCA_CLASSES,
    FISH_CCA_PERSONAL_PART,
    FISH_CCA_TABLE_CLAIM,
    FISH_CLOSING_UCC,
    FISH_COMPENSATION_FOR_LOSS,
    FISH_CREW_SHARES,
    FISH_EXPENSES_SUBTOTAL,
    FISH_FISH_PRODUCTS,
    FISH_FISHING_GEAR,
    FISH_FUEL_COSTS,
    FISH_GRANTS_CREDITS_AND_REBATES,
    FISH_GROSS_INCOME,
    FISH_GROSS_INCOME_BEFORE_EXPENSES,
    FISH_HOME_ALLOWABLE_CLAIM,
    FISH_HOME_CARRIED_FORWARD,
    FISH_HOME_CARRY_FORWARD,
    FISH_HOME_CCA,
    FISH_HOME_ELECTRICITY,
    FISH_HOME_EXPENSES,
    FISH_HOME_EXPENSES_AVAILABLE,
    FISH_HOME_EXPENSES_BUSINESS_PART,
    FISH_HOME_EXPENSES_SUBTOTAL,
    FISH_HOME_HEAT,
    FISH_HOME_INCOME_LIMIT,
    FISH_HOME_INSURANCE,
    FISH_HOME_MAINTENANCE,
    FISH_HOME_MORTGAGE_INTEREST,
    FISH_HOME_OTHER_EXPENSES,
    FISH_HOME_PERSONAL_USE_PART,
    FISH_HOME_PROPERTY_TAXES,
    FISH_INSURANCE,
    FISH_INSURANCE_RECOVERY,
    FISH_INTEREST_AND_BANK_CHARGES,
    FISH_MEALS_AND_ENTERTAINMENT,
    FISH_MOTOR_VEHICLE_EXPENSES,
    FISH_NET_INCOME_AFTER_ADJUSTMENTS,
    FISH_NET_INCOME_BEFORE_ADJUSTMENTS,
    FISH_NETS_AND_TRAPS,
    FISH_OFFICE_EXPENSES,
    FISH_OTHER_EXPENSES,
    FISH_OTHER_EXPENSES_WITH_TERMINAL_LOSS,
    FISH_OTHER_INCOME,
    FISH_OTHER_INCOME_WITH_RECAPTURE,
    FISH_OTHER_MARINE_PRODUCTS,
    FISH_PARTNER,
    FISH_PARTNER_GST_HST_REBATE,
    FISH_PARTNER_OTHER_AMOUNT_A,
    FISH_PARTNER_OTHER_AMOUNT_B,
    FISH_PARTNER_OTHER_AMOUNT_C,
    FISH_PARTNER_OTHER_AMOUNT_D,
    FISH_PARTNER_OTHER_AMOUNT_E,
    FISH_PARTNER_OTHER_AMOUNTS,
    FISH_PARTNER_OTHER_AMOUNTS_TOTAL,
    FISH_PARTNER_SHARE,
    FISH_PARTNERSHIP_TOTAL,
    FISH_PROFESSIONAL_FEES,
    FISH_RECAPTURED_CCA,
    FISH_REPAIRS_ELECTRICAL_EQUIPMENT,
    FISH_REPAIRS_ENGINE,
    FISH_REPAIRS_FISHING_BOAT,
    FISH_REPAIRS_TOTAL,
    FISH_REPAIRS_YOUR_COST,
    FISH_SALARIES_WAGES_AND_BENEFITS,
    FISH_SALT_BAIT_AND_ICE,
    FISH_SHARE_OF_NET_INCOME,
    FISH_SHARESPERSON_INCOME,
    FISH_SUBSIDIES,
    FISH_TERMINAL_LOSS,
    FISH_TOTAL_EXPENSES,
    FISH_VEHICLE_AVAILABLE_INTEREST,
    FISH_VEHICLE_BUSINESS_KILOMETRES,
    FISH_VEHICLE_BUSINESS_USE_PART,
    FISH_VEHICLE_ELECTRICITY_ZEV,
    FISH_VEHICLE_FUEL_AND_OIL,
    FISH_VEHICLE_INSURANCE,
    FISH_VEHICLE_INTEREST_DAYS,
    FISH_VEHICLE_INTEREST_FOR_PERIOD,
    FISH_VEHICLE_INTEREST_PAYABLE,
    FISH_VEHICLE_LEASE_CHARGE_LIMIT_TAX,
    FISH_VEHICLE_LEASE_CHARGE_LIMIT_WITH_TAX,
    FISH_VEHICLE_LEASE_CHARGE_PORTION,
    FISH_VEHICLE_LEASE_CHARGES,
    FISH_VEHICLE_LEASE_CHARGES_NET,
    FISH_VEHICLE_LEASE_COST_LIMIT_TAX,
    FISH_VEHICLE_LEASE_COST_LIMIT_WITH_TAX,
    FISH_VEHICLE_LEASE_COST_PORTION,
    FISH_VEHICLE_LEASE_DAYS,
    FISH_VEHICLE_LEASE_PAYMENTS_BEFORE,
    FISH_VEHICLE_LEASE_PRICE_85_PERCENT,
    FISH_VEHICLE_LEASE_PRICE_BASE,
    FISH_VEHICLE_LEASING_COST,
    FISH_VEHICLE_LICENCE_AND_REGISTRATION,
    FISH_VEHICLE_LIST_PRICE,
    FISH_VEHICLE_LIST_PRICE_LIMIT_TAX,
    FISH_VEHICLE_LIST_PRICE_LIMIT_WITH_TAX,
    FISH_VEHICLE_MAINTENANCE_AND_REPAIRS,
    FISH_VEHICLE_OTHER_EXPENSES_10,
    FISH_VEHICLE_OTHER_EXPENSES_11,
    FISH_VEHICLE_PARKING_FEES,
    FISH_VEHICLE_SALES_TAX_RATE,
    FISH_VEHICLE_SUPPLEMENTARY_INSURANCE,
    FISH_VEHICLE_TOTAL_EXPENSES,
    FISH_VEHICLE_TOTAL_KILOMETRES,
    FISHING_INCOME,
    FOREIGN_INVESTMENT_INCOME,
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
    RRSP_INCOME,
    SHARE_DISPOSITIONS,
    SHARE_GAIN_OR_LOSS,
    SHARE_PROCEEDS,
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
        # Form T2121 (statement of fishing) Parts 3 to 7 and Area A: the caller's amounts, in the
        # form's order, and the Area A class list; T1 line 26 (line 14300) is T2121 line 9946,
        # computed.
        "ca/fish_fish_products",
        "ca/fish_other_marine_products",
        "ca/fish_grants_credits_and_rebates",
        "ca/fish_subsidies",
        "ca/fish_compensation_for_loss",
        "ca/fish_sharesperson_income",
        "ca/fish_other_income",
        "ca/fish_salt_bait_and_ice",
        "ca/fish_crew_shares",
        "ca/fish_fuel_costs",
        "ca/fish_fishing_gear",
        "ca/fish_insurance",
        "ca/fish_interest_and_bank_charges",
        "ca/fish_meals_and_entertainment",
        "ca/fish_business_taxes_licences_and_memberships",
        "ca/fish_vehicle_business_kilometres",
        "ca/fish_vehicle_total_kilometres",
        "ca/fish_vehicle_fuel_and_oil",
        "ca/fish_vehicle_insurance",
        "ca/fish_vehicle_licence_and_registration",
        "ca/fish_vehicle_maintenance_and_repairs",
        "ca/fish_vehicle_electricity_zev",
        "ca/fish_vehicle_other_expenses_10",
        "ca/fish_vehicle_other_expenses_11",
        "ca/fish_vehicle_parking_fees",
        "ca/fish_vehicle_supplementary_insurance",
        "ca/fish_vehicle_interest_payable",
        "ca/fish_vehicle_interest_days",
        "ca/fish_vehicle_lease_charges",
        "ca/fish_vehicle_lease_payments_before",
        "ca/fish_vehicle_lease_days",
        "ca/fish_vehicle_list_price",
        "ca/fish_vehicle_sales_tax_rate",
        "ca/fish_office_expenses",
        "ca/fish_nets_and_traps",
        "ca/fish_professional_fees",
        "ca/fish_salaries_wages_and_benefits",
        "ca/fish_repairs_fishing_boat",
        "ca/fish_repairs_engine",
        "ca/fish_repairs_electrical_equipment",
        "ca/fish_insurance_recovery",
        "ca/fish_other_expenses",
        "ca/fish_cca_personal_part",
        "ca/fish_cca_classes",
        "ca/fish_partner",
        "ca/fish_partner_share",
        "ca/fish_partner_gst_hst_rebate",
        "ca/fish_partner_other_amount_a",
        "ca/fish_partner_other_amount_b",
        "ca/fish_partner_other_amount_c",
        "ca/fish_partner_other_amount_d",
        "ca/fish_partner_other_amount_e",
        "ca/fish_home_heat",
        "ca/fish_home_electricity",
        "ca/fish_home_insurance",
        "ca/fish_home_maintenance",
        "ca/fish_home_mortgage_interest",
        "ca/fish_home_property_taxes",
        "ca/fish_home_other_expenses",
        "ca/fish_home_personal_use_part",
        "ca/fish_home_cca",
        "ca/fish_home_carried_forward",
        "ca/taxable_support_payments",
        "ca/rrsp_income",
        "ca/fhsa_income",
        "ca/other_fhsa_income",
        "ca/other_income",
        "ca/taxable_scholarships",
        "ca/professional_income",
        "ca/commission_income",
        "ca/workers_compensation_benefits",
        "ca/social_assistance_payments",
        "ca/net_federal_supplements",
    }
)

OUTPUTS = frozenset(
    {
        "ca/taxable_dividends_other_than_eligible",
        # Form T2121 Area A column 22 "UCC at the end of the year" (for next year) and Part 7 line
        # 7O "Business-use-of-home expenses available to carry forward": nothing else on the return
        # reads them.
        "ca/fish_closing_ucc",
        "ca/fish_home_carry_forward",
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
    # T1 line 125 "Add lines 122 to 124.": line 122 "Amount from line 35000", line 123 (40425),
    # the federal dividend tax credit, and line 124 (40427), the minimum tax carryover applied
    # on Form T691 Part 8 line 12, in line order.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/non_refundable_tax_credits",
                "ca/dividend_tax_credit",
                "ca/amt_minimum_tax_carryover_applied",
            )
        },
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
    # T2121 Area A endnote 3 "If you have a negative amount in column 7, add it to income as a
    # recapture in Part 3 on line 9600. If no property is left in the class and there is a
    # positive amount in this column, deduct the amount from income as a terminal loss in Part 4
    # on line 9270.": the recapture of each class of the Area A list (column 7 made positive when
    # negative), totalled.
    CapabilitySelection(
        name="ca/recaptured_cca",
        params={"class_rates": "ca/cca_class_rates"},
        consumes={"classes": "ca/fish_cca_classes"},
        produces={"output": "ca/fish_recaptured_cca"},
    ),
    # T2121 Part 3 line 9600 "Other income (specify):", which takes the recapture of Area A (the
    # Area A endnote "add it to income as a recapture in Part 3 on line 9600"): the other income
    # the caller specifies plus the recapture.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/fish_other_income", "ca/fish_recaptured_cca")},
        produces={"output": "ca/fish_other_income_with_recapture"},
    ),
    # T2121 Part 3 "Gross income: Total of amounts 3A to 3F and line 9600 (enter this amount on line
    # 14299 of your income tax and benefit return)" (line 8299): the caller's amounts 3A to 3F in
    # the form's order, and line 9600 with its recapture.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/fish_fish_products",
                "ca/fish_other_marine_products",
                "ca/fish_grants_credits_and_rebates",
                "ca/fish_subsidies",
                "ca/fish_compensation_for_loss",
                "ca/fish_sharesperson_income",
                "ca/fish_other_income_with_recapture",
            )
        },
        produces={"output": "ca/fish_gross_income"},
    ),
    # T2121 Part 4 "Gross income (line 8299 of Part 3)" (4A): line 8299 alone, the gross income that
    # the expenses are taken from.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/fish_gross_income",)},
        produces={"output": "ca/fish_gross_income_before_expenses"},
    ),
    # T2121 Area A endnote 3 "deduct the amount from income as a terminal loss in Part 4 on line
    # 9270": the terminal loss of each class of the Area A list, totalled.
    CapabilitySelection(
        name="ca/terminal_loss",
        params={"class_rates": "ca/cca_class_rates"},
        consumes={"classes": "ca/fish_cca_classes"},
        produces={"output": "ca/fish_terminal_loss"},
    ),
    # T2121 Part 4 "Other expenses (specify): 9270 4P": the other expenses the caller specifies plus
    # the terminal loss.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/fish_other_expenses", "ca/fish_terminal_loss")},
        produces={"output": "ca/fish_other_expenses_with_terminal_loss"},
    ),
    # T2121 Part 4 "Repairs and maintenance: Fishing boat", "Engine", "Electrical equipment"
    # (amounts 1 to 3) and "Total of amounts 1 to 3" (amount 4): the three caller amounts added.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/fish_repairs_fishing_boat",
                "ca/fish_repairs_engine",
                "ca/fish_repairs_electrical_equipment",
            )
        },
        produces={"output": "ca/fish_repairs_total"},
    ),
    # T2121 Part 4 "Your cost (amount 4 minus amount 5)" (line 8963, 4O): amount 4 less the
    # insurance recovery, amount 5 (a caller input). Signed: the form prints no floor.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ca/fish_repairs_total", "less": "ca/fish_insurance_recovery"},
        produces={"output": "ca/fish_repairs_your_cost"},
    ),
    # T2121 Part 4 "Subtotal: Add amounts 4B to 4P." (4Q): the expense lines 4B to 4N, amount 4O and
    # the other expenses of line 9270 with the terminal loss.
    # Chart B line 18 "($350*** ÷ 30) × the number of days in the fiscal period for which interest
    # was payable (accrual method) or paid (cash method)".
    CapabilitySelection(
        name="core/apply_ratio",
        params={"rounding": "ca/business_vehicle_interest_rounding"},
        consumes={
            "amount": "ca/business_vehicle_interest_limit",
            "numerator": "ca/fish_vehicle_interest_days",
            "denominator": "ca/business_vehicle_days_divisor",
        },
        produces={"output": "ca/fish_vehicle_interest_for_period"},
    ),
    # Chart B line 19 "Available interest expense: Amount 17 or 18, whichever is less (include this
    # in amount 4 of Chart A above)": the lesser of line 17 "Total interest payable (accrual method)
    # or paid (cash method) in the fiscal period" and line 18.
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={
            "amounts": (
                "ca/fish_vehicle_interest_payable",
                "ca/fish_vehicle_interest_for_period",
            ),
        },
        produces={"output": "ca/fish_vehicle_available_interest"},
    ),
    # Chart C: the sales tax (GST and PST, or HST) on each printed amount at the rate of the
    # caller's province, "Use a GST rate of 5% or HST rate applicable to your province.", then the
    # printed amount plus that tax.
    CapabilitySelection(
        name="ca/apply_percentage",
        params={"rounding": "ca/business_vehicle_sales_tax_rounding"},
        consumes={
            "amount": "ca/business_vehicle_list_price_limit",
            "percentage": "ca/fish_vehicle_sales_tax_rate",
        },
        produces={"output": "ca/fish_vehicle_list_price_limit_tax"},
    ),
    CapabilitySelection(
        name="ca/apply_percentage",
        params={"rounding": "ca/business_vehicle_sales_tax_rounding"},
        consumes={
            "amount": "ca/business_vehicle_lease_charge_limit",
            "percentage": "ca/fish_vehicle_sales_tax_rate",
        },
        produces={"output": "ca/fish_vehicle_lease_charge_limit_tax"},
    ),
    CapabilitySelection(
        name="ca/apply_percentage",
        params={"rounding": "ca/business_vehicle_sales_tax_rounding"},
        consumes={
            "amount": "ca/business_vehicle_lease_cost_limit",
            "percentage": "ca/fish_vehicle_sales_tax_rate",
        },
        produces={"output": "ca/fish_vehicle_lease_cost_limit_tax"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/business_vehicle_list_price_limit",
                "ca/fish_vehicle_list_price_limit_tax",
            ),
        },
        produces={"output": "ca/fish_vehicle_list_price_limit_with_tax"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/business_vehicle_lease_charge_limit",
                "ca/fish_vehicle_lease_charge_limit_tax",
            ),
        },
        produces={"output": "ca/fish_vehicle_lease_charge_limit_with_tax"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/business_vehicle_lease_cost_limit",
                "ca/fish_vehicle_lease_cost_limit_tax",
            ),
        },
        produces={"output": "ca/fish_vehicle_lease_cost_limit_with_tax"},
    ),
    # Chart C line 23 "Amount 23 or ($44,706 + GST and PST, or $44,706 + HST), whichever is more".
    CapabilitySelection(
        name="core/greater_of",
        params={},
        consumes={
            "amounts": (
                "ca/fish_vehicle_list_price",
                "ca/fish_vehicle_list_price_limit_with_tax",
            ),
        },
        produces={"output": "ca/fish_vehicle_lease_price_base"},
    ),
    # Chart C line 24 "Amount 23 or ($44,706 + GST and PST, or $44,706 + HST), whichever is more ×
    # 85%".
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/business_vehicle_lease_price_rate"},
        consumes={"base": "ca/fish_vehicle_lease_price_base"},
        produces={"output": "ca/fish_vehicle_lease_price_85_percent"},
    ),
    # Chart C line 25 "[($1,100 + GST and PST, or $1,100 + HST) × amount 22] ÷ 30".
    CapabilitySelection(
        name="core/apply_ratio",
        params={"rounding": "ca/business_vehicle_lease_charge_rounding"},
        consumes={
            "amount": "ca/fish_vehicle_lease_charge_limit_with_tax",
            "numerator": "ca/fish_vehicle_lease_days",
            "denominator": "ca/business_vehicle_days_divisor",
        },
        produces={"output": "ca/fish_vehicle_lease_charge_portion"},
    ),
    # Chart C line 26, printed "Amount 25: amount 21" with a subtraction sign: amount 25 less amount
    # 21, signed (a negative result is kept).
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/fish_vehicle_lease_charge_portion",
            "less": "ca/fish_vehicle_lease_payments_before",
        },
        produces={"output": "ca/fish_vehicle_lease_charges_net"},
    ),
    # Chart C line 27 "[($38,000 + GST and PST, or $38,000 + HST) × amount 20] ÷ amount 24".
    CapabilitySelection(
        name="core/apply_ratio",
        params={"rounding": "ca/business_vehicle_lease_cost_rounding"},
        consumes={
            "amount": "ca/fish_vehicle_lease_cost_limit_with_tax",
            "numerator": "ca/fish_vehicle_lease_charges",
            "denominator": "ca/fish_vehicle_lease_price_85_percent",
        },
        produces={"output": "ca/fish_vehicle_lease_cost_portion"},
    ),
    # Chart C line 28 "Eligible leasing cost: Amount 26 or 27, whichever is less (enter in amount 8
    # of Chart A above)".
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={
            "amounts": (
                "ca/fish_vehicle_lease_charges_net",
                "ca/fish_vehicle_lease_cost_portion",
            ),
        },
        produces={"output": "ca/fish_vehicle_leasing_cost"},
    ),
    # Chart A line 12 "Total motor vehicle expenses: Add amounts 3 to 11.", amount 4 being line 19
    # and amount 8 being line 28.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/fish_vehicle_fuel_and_oil",
                "ca/fish_vehicle_available_interest",
                "ca/fish_vehicle_insurance",
                "ca/fish_vehicle_licence_and_registration",
                "ca/fish_vehicle_maintenance_and_repairs",
                "ca/fish_vehicle_leasing_cost",
                "ca/fish_vehicle_electricity_zev",
                "ca/fish_vehicle_other_expenses_10",
                "ca/fish_vehicle_other_expenses_11",
            ),
        },
        produces={"output": "ca/fish_vehicle_total_expenses"},
    ),
    # Chart A line 13 "Business use part: amount 1 ÷ amount 2 × amount 12 = 13".
    CapabilitySelection(
        name="ca/apply_ratio_or_zero",
        params={"rounding": "ca/business_vehicle_business_use_rounding"},
        consumes={
            "amount": "ca/fish_vehicle_total_expenses",
            "numerator": "ca/fish_vehicle_business_kilometres",
            "denominator": "ca/fish_vehicle_total_kilometres",
        },
        produces={"output": "ca/fish_vehicle_business_use_part"},
    ),
    # Chart A line 16 "Allowable motor vehicle expenses: Add amounts 13 to 15 (enter this total on
    # line 9281 of Part 4)": the line 9281 kind, produced here and no longer a caller input.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/fish_vehicle_business_use_part",
                "ca/fish_vehicle_parking_fees",
                "ca/fish_vehicle_supplementary_insurance",
            ),
        },
        produces={"output": "ca/fish_motor_vehicle_expenses"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/fish_salt_bait_and_ice",
                "ca/fish_crew_shares",
                "ca/fish_fuel_costs",
                "ca/fish_fishing_gear",
                "ca/fish_insurance",
                "ca/fish_interest_and_bank_charges",
                "ca/fish_meals_and_entertainment",
                "ca/fish_business_taxes_licences_and_memberships",
                "ca/fish_motor_vehicle_expenses",
                "ca/fish_office_expenses",
                "ca/fish_nets_and_traps",
                "ca/fish_professional_fees",
                "ca/fish_salaries_wages_and_benefits",
                "ca/fish_repairs_your_cost",
                "ca/fish_other_expenses_with_terminal_loss",
            )
        },
        produces={"output": "ca/fish_expenses_subtotal"},
    ),
    # T2121 Area A "Total CCA claim for the year: Total of column 21 (enter on line 9936 of Part 4
    # amount ii minus any personal part and any CCA for business-use-of-home expenses)" (amount ii):
    # the CCA claimed on each class of the Area A list, at most its maximum, totalled.
    CapabilitySelection(
        name="ca/cca_claim",
        params={"class_rates": "ca/cca_class_rates"},
        consumes={"classes": "ca/fish_cca_classes"},
        produces={"output": "ca/fish_cca_table_claim"},
    ),
    # T2121 Part 4 "Capital cost allowance (CCA). Enter amount ii of Area A minus any personal part
    # and any CCA for business-use-of-home expenses." (line 9936), first step: amount ii minus the
    # personal part of CCA, a caller input.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ca/fish_cca_table_claim", "less": "ca/fish_cca_personal_part"},
        produces={"output": "ca/fish_cca_claim_less_personal_part"},
    ),
    # T2121 Part 4 line 9936, second step: that result minus the CCA for business-use-of-home
    # expenses, amount 7K "Capital cost allowance (business part only), which means amount ii of
    # Area A minus any portion of capital cost allowance that is for personal use or entered on
    # line 9936 of Part 4", a caller input.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ca/fish_cca_claim_less_personal_part", "less": "ca/fish_home_cca"},
        produces={"output": "ca/fish_cca_claim"},
    ),
    # T2121 Part 4 "Total expenses: Amount 4Q plus line 9936" (line 9368): the two added.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/fish_expenses_subtotal", "ca/fish_cca_claim")},
        produces={"output": "ca/fish_total_expenses"},
    ),
    # T2121 Part 4 "Net income (loss) before adjustments: Amount 4A minus line 9368" (line 9369):
    # signed, a loss is negative.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/fish_gross_income_before_expenses",
            "less": "ca/fish_total_expenses",
        },
        produces={"output": "ca/fish_net_income_before_adjustments"},
    ),
    # T2121 Part 5 "Your share of line 9369 or the amount from your T5013 slip, Statement of
    # Partnership Income" (5A): a count of 1 for a partner chooses the amount from the T5013 slip,
    # as entered; with a count of 0 it is line 9369.
    CapabilitySelection(
        name="core/choose_by_count",
        params={},
        consumes={
            "count": "ca/fish_partner",
            "when_none": "ca/fish_net_income_before_adjustments",
            "when_any": "ca/fish_partner_share",
        },
        produces={"output": "ca/fish_share_of_net_income"},
    ),
    # T2121 Part 5 "Total: Amount 5A plus line 9974" (5B): amount 5A and line 9974 "GST/HST rebate
    # for partners received in the year", a caller input.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/fish_share_of_net_income",
                "ca/fish_partner_gst_hst_rebate",
            )
        },
        produces={"output": "ca/fish_partnership_total"},
    ),
    # T2121 Part 6 "Total other amounts deductible from your share of the net partnership income
    # (loss): Add amounts 6A to 6E (enter this amount on line 9943 of Part 5)." (6F): 6A to 6E,
    # caller inputs.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/fish_partner_other_amount_a",
                "ca/fish_partner_other_amount_b",
                "ca/fish_partner_other_amount_c",
                "ca/fish_partner_other_amount_d",
                "ca/fish_partner_other_amount_e",
            )
        },
        produces={"output": "ca/fish_partner_other_amounts_total"},
    ),
    # T2121 Part 5 "Other amounts deductible from your share of net partnership income (loss)
    # (amount 6F)" (line 9943).
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/fish_partner_other_amounts_total",)},
        produces={"output": "ca/fish_partner_other_amounts"},
    ),
    # T2121 Part 5 "Net income (loss) after adjustments: Amount 5B minus line 9943" (5C): signed, a
    # loss is negative.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/fish_partnership_total",
            "less": "ca/fish_partner_other_amounts",
        },
        produces={"output": "ca/fish_net_income_after_adjustments"},
    ),
    # T2121 Part 7 "Subtotal: Add amounts 7A to 7G." (7H): 7A "Heat", 7B "Electricity", 7C
    # "Insurance", 7D "Maintenance", 7E "Mortgage interest", 7F "Property taxes" and 7G "Other
    # expenses (specify)", caller inputs.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/fish_home_heat",
                "ca/fish_home_electricity",
                "ca/fish_home_insurance",
                "ca/fish_home_maintenance",
                "ca/fish_home_mortgage_interest",
                "ca/fish_home_property_taxes",
                "ca/fish_home_other_expenses",
            )
        },
        produces={"output": "ca/fish_home_expenses_subtotal"},
    ),
    # T2121 Part 7 "Subtotal: Amount 7H minus amount 7I" (7J): amount 7I "Personal-use part of the
    # business-use-of-home expenses", a caller input.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/fish_home_expenses_subtotal",
            "less": "ca/fish_home_personal_use_part",
        },
        produces={"output": "ca/fish_home_expenses_business_part"},
    ),
    # T2121 Part 7 "Subtotal: Add amounts 7J to 7L." (7M): 7J, amount 7K (the CCA for the business
    # part, a caller input) and 7L "Amount carried forward from previous year", a caller input.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/fish_home_expenses_business_part",
                "ca/fish_home_cca",
                "ca/fish_home_carried_forward",
            )
        },
        produces={"output": "ca/fish_home_expenses_available"},
    ),
    # T2121 Part 7 "Net income (loss) after adjustments (amount 5C) (if negative, enter "0")." (7N):
    # amount 5C, or 0 when it is negative.
    CapabilitySelection(
        name="core/sum_not_below_zero",
        params={},
        consumes={"parts": ("ca/fish_net_income_after_adjustments",)},
        produces={"output": "ca/fish_home_income_limit"},
    ),
    # T2121 Part 7 "Business-use-of-home expenses available to carry forward: Amount 7M minus amount
    # 7N (if negative, enter "0")" (7O): the claim left over, 0 when amount 7N is the larger.
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/fish_home_expenses_available",
            "less": "ca/fish_home_income_limit",
        },
        produces={"output": "ca/fish_home_carry_forward"},
    ),
    # T2121 Part 7 "Allowable claim: Amount 7M or 7N above, whichever is less (enter your share of
    # this amount on line 9945 of Part 5)" (7P).
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={
            "amounts": ("ca/fish_home_expenses_available", "ca/fish_home_income_limit"),
        },
        produces={"output": "ca/fish_home_allowable_claim"},
    ),
    # T2121 Part 5 "Business-use-of-home expenses (amount 7P)" (line 9945).
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/fish_home_allowable_claim",)},
        produces={"output": "ca/fish_home_expenses"},
    ),
    # T2121 Part 5 "Your net income (loss): Amount 5C minus line 9945 (enter this amount on line
    # 14300 of your income tax and benefit return)" (line 9946): T1 "Line 26: Fishing income" and
    # "Line 14300: Net" are the same artifact, signed: a loss is negative.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/fish_net_income_after_adjustments",
            "less": "ca/fish_home_expenses",
        },
        produces={"output": "ca/fishing_income"},
    ),
    # T2121 Area A column 22 "UCC at the end of the year (col. 7 minus col. 21)": the class number
    # and column 22 of each class of the Area A list, a product of the return for next year's
    # column 1.
    CapabilitySelection(
        name="ca/closing_ucc",
        params={"class_rates": "ca/cca_class_rates"},
        consumes={"classes": "ca/fish_cca_classes"},
        produces={"output": "ca/fish_closing_ucc"},
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
        frozenset(
            {NON_REFUNDABLE_TAX_CREDITS, DIVIDEND_TAX_CREDIT, AMT_MINIMUM_TAX_CARRYOVER_APPLIED}
        ),
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
    # T2121 (Statement of Fishing Activities), Return BD: one tuple per step of the fishing block.
    (RecapturedCca, frozenset({FISH_CCA_CLASSES}), frozenset({FISH_RECAPTURED_CCA})),
    (
        Sum,
        frozenset({FISH_OTHER_INCOME, FISH_RECAPTURED_CCA}),
        frozenset({FISH_OTHER_INCOME_WITH_RECAPTURE}),
    ),
    (
        Sum,
        frozenset(
            {
                FISH_FISH_PRODUCTS,
                FISH_OTHER_MARINE_PRODUCTS,
                FISH_GRANTS_CREDITS_AND_REBATES,
                FISH_SUBSIDIES,
                FISH_COMPENSATION_FOR_LOSS,
                FISH_SHARESPERSON_INCOME,
                FISH_OTHER_INCOME_WITH_RECAPTURE,
            }
        ),
        frozenset({FISH_GROSS_INCOME}),
    ),
    (Sum, frozenset({FISH_GROSS_INCOME}), frozenset({FISH_GROSS_INCOME_BEFORE_EXPENSES})),
    (TerminalLoss, frozenset({FISH_CCA_CLASSES}), frozenset({FISH_TERMINAL_LOSS})),
    (
        Sum,
        frozenset({FISH_OTHER_EXPENSES, FISH_TERMINAL_LOSS}),
        frozenset({FISH_OTHER_EXPENSES_WITH_TERMINAL_LOSS}),
    ),
    (
        Sum,
        frozenset(
            {
                FISH_REPAIRS_FISHING_BOAT,
                FISH_REPAIRS_ENGINE,
                FISH_REPAIRS_ELECTRICAL_EQUIPMENT,
            }
        ),
        frozenset({FISH_REPAIRS_TOTAL}),
    ),
    (
        Subtract,
        frozenset({FISH_REPAIRS_TOTAL, FISH_INSURANCE_RECOVERY}),
        frozenset({FISH_REPAIRS_YOUR_COST}),
    ),
    (
        Sum,
        frozenset(
            {
                FISH_SALT_BAIT_AND_ICE,
                FISH_CREW_SHARES,
                FISH_FUEL_COSTS,
                FISH_FISHING_GEAR,
                FISH_INSURANCE,
                FISH_INTEREST_AND_BANK_CHARGES,
                FISH_MEALS_AND_ENTERTAINMENT,
                FISH_BUSINESS_TAXES_LICENCES_AND_MEMBERSHIPS,
                FISH_MOTOR_VEHICLE_EXPENSES,
                FISH_OFFICE_EXPENSES,
                FISH_NETS_AND_TRAPS,
                FISH_PROFESSIONAL_FEES,
                FISH_SALARIES_WAGES_AND_BENEFITS,
                FISH_REPAIRS_YOUR_COST,
                FISH_OTHER_EXPENSES_WITH_TERMINAL_LOSS,
            }
        ),
        frozenset({FISH_EXPENSES_SUBTOTAL}),
    ),
    (CcaClaim, frozenset({FISH_CCA_CLASSES}), frozenset({FISH_CCA_TABLE_CLAIM})),
    (
        Subtract,
        frozenset({FISH_CCA_PERSONAL_PART, FISH_CCA_TABLE_CLAIM}),
        frozenset({FISH_CCA_CLAIM_LESS_PERSONAL_PART}),
    ),
    (
        Subtract,
        frozenset({FISH_CCA_CLAIM_LESS_PERSONAL_PART, FISH_HOME_CCA}),
        frozenset({FISH_CCA_CLAIM}),
    ),
    (Sum, frozenset({FISH_CCA_CLAIM, FISH_EXPENSES_SUBTOTAL}), frozenset({FISH_TOTAL_EXPENSES})),
    (
        Subtract,
        frozenset({FISH_GROSS_INCOME_BEFORE_EXPENSES, FISH_TOTAL_EXPENSES}),
        frozenset({FISH_NET_INCOME_BEFORE_ADJUSTMENTS}),
    ),
    (
        ChooseByCount,
        frozenset({FISH_NET_INCOME_BEFORE_ADJUSTMENTS, FISH_PARTNER, FISH_PARTNER_SHARE}),
        frozenset({FISH_SHARE_OF_NET_INCOME}),
    ),
    (
        Sum,
        frozenset({FISH_SHARE_OF_NET_INCOME, FISH_PARTNER_GST_HST_REBATE}),
        frozenset({FISH_PARTNERSHIP_TOTAL}),
    ),
    (
        Sum,
        frozenset(
            {
                FISH_PARTNER_OTHER_AMOUNT_A,
                FISH_PARTNER_OTHER_AMOUNT_B,
                FISH_PARTNER_OTHER_AMOUNT_C,
                FISH_PARTNER_OTHER_AMOUNT_D,
                FISH_PARTNER_OTHER_AMOUNT_E,
            }
        ),
        frozenset({FISH_PARTNER_OTHER_AMOUNTS_TOTAL}),
    ),
    (Sum, frozenset({FISH_PARTNER_OTHER_AMOUNTS_TOTAL}), frozenset({FISH_PARTNER_OTHER_AMOUNTS})),
    (
        Subtract,
        frozenset({FISH_PARTNERSHIP_TOTAL, FISH_PARTNER_OTHER_AMOUNTS}),
        frozenset({FISH_NET_INCOME_AFTER_ADJUSTMENTS}),
    ),
    (
        Sum,
        frozenset(
            {
                FISH_HOME_HEAT,
                FISH_HOME_ELECTRICITY,
                FISH_HOME_INSURANCE,
                FISH_HOME_MAINTENANCE,
                FISH_HOME_MORTGAGE_INTEREST,
                FISH_HOME_PROPERTY_TAXES,
                FISH_HOME_OTHER_EXPENSES,
            }
        ),
        frozenset({FISH_HOME_EXPENSES_SUBTOTAL}),
    ),
    (
        Subtract,
        frozenset({FISH_HOME_EXPENSES_SUBTOTAL, FISH_HOME_PERSONAL_USE_PART}),
        frozenset({FISH_HOME_EXPENSES_BUSINESS_PART}),
    ),
    (
        Sum,
        frozenset({FISH_HOME_CARRIED_FORWARD, FISH_HOME_CCA, FISH_HOME_EXPENSES_BUSINESS_PART}),
        frozenset({FISH_HOME_EXPENSES_AVAILABLE}),
    ),
    (
        SumNotBelowZero,
        frozenset({FISH_NET_INCOME_AFTER_ADJUSTMENTS}),
        frozenset({FISH_HOME_INCOME_LIMIT}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({FISH_HOME_EXPENSES_AVAILABLE, FISH_HOME_INCOME_LIMIT}),
        frozenset({FISH_HOME_CARRY_FORWARD}),
    ),
    (
        LesserOf,
        frozenset({FISH_HOME_EXPENSES_AVAILABLE, FISH_HOME_INCOME_LIMIT}),
        frozenset({FISH_HOME_ALLOWABLE_CLAIM}),
    ),
    (Sum, frozenset({FISH_HOME_ALLOWABLE_CLAIM}), frozenset({FISH_HOME_EXPENSES})),
    (
        Subtract,
        frozenset({FISH_HOME_EXPENSES, FISH_NET_INCOME_AFTER_ADJUSTMENTS}),
        frozenset({FISHING_INCOME}),
    ),
    (ClosingUcc, frozenset({FISH_CCA_CLASSES}), frozenset({FISH_CLOSING_UCC})),
    (
        ApplyRatio,
        frozenset(
            {
                BUSINESS_VEHICLE_INTEREST_LIMIT,
                FISH_VEHICLE_INTEREST_DAYS,
                BUSINESS_VEHICLE_DAYS_DIVISOR,
            }
        ),
        frozenset({FISH_VEHICLE_INTEREST_FOR_PERIOD}),
    ),
    (
        LesserOf,
        frozenset({FISH_VEHICLE_INTEREST_PAYABLE, FISH_VEHICLE_INTEREST_FOR_PERIOD}),
        frozenset({FISH_VEHICLE_AVAILABLE_INTEREST}),
    ),
    (
        ApplyPercentage,
        frozenset({BUSINESS_VEHICLE_LIST_PRICE_LIMIT, FISH_VEHICLE_SALES_TAX_RATE}),
        frozenset({FISH_VEHICLE_LIST_PRICE_LIMIT_TAX}),
    ),
    (
        ApplyPercentage,
        frozenset({BUSINESS_VEHICLE_LEASE_CHARGE_LIMIT, FISH_VEHICLE_SALES_TAX_RATE}),
        frozenset({FISH_VEHICLE_LEASE_CHARGE_LIMIT_TAX}),
    ),
    (
        ApplyPercentage,
        frozenset({BUSINESS_VEHICLE_LEASE_COST_LIMIT, FISH_VEHICLE_SALES_TAX_RATE}),
        frozenset({FISH_VEHICLE_LEASE_COST_LIMIT_TAX}),
    ),
    (
        Sum,
        frozenset({BUSINESS_VEHICLE_LIST_PRICE_LIMIT, FISH_VEHICLE_LIST_PRICE_LIMIT_TAX}),
        frozenset({FISH_VEHICLE_LIST_PRICE_LIMIT_WITH_TAX}),
    ),
    (
        Sum,
        frozenset({BUSINESS_VEHICLE_LEASE_CHARGE_LIMIT, FISH_VEHICLE_LEASE_CHARGE_LIMIT_TAX}),
        frozenset({FISH_VEHICLE_LEASE_CHARGE_LIMIT_WITH_TAX}),
    ),
    (
        Sum,
        frozenset({BUSINESS_VEHICLE_LEASE_COST_LIMIT, FISH_VEHICLE_LEASE_COST_LIMIT_TAX}),
        frozenset({FISH_VEHICLE_LEASE_COST_LIMIT_WITH_TAX}),
    ),
    (
        GreaterOf,
        frozenset({FISH_VEHICLE_LIST_PRICE, FISH_VEHICLE_LIST_PRICE_LIMIT_WITH_TAX}),
        frozenset({FISH_VEHICLE_LEASE_PRICE_BASE}),
    ),
    (
        ApplyRate,
        frozenset({FISH_VEHICLE_LEASE_PRICE_BASE}),
        frozenset({FISH_VEHICLE_LEASE_PRICE_85_PERCENT}),
    ),
    (
        ApplyRatio,
        frozenset(
            {
                FISH_VEHICLE_LEASE_CHARGE_LIMIT_WITH_TAX,
                FISH_VEHICLE_LEASE_DAYS,
                BUSINESS_VEHICLE_DAYS_DIVISOR,
            }
        ),
        frozenset({FISH_VEHICLE_LEASE_CHARGE_PORTION}),
    ),
    (
        Subtract,
        frozenset({FISH_VEHICLE_LEASE_CHARGE_PORTION, FISH_VEHICLE_LEASE_PAYMENTS_BEFORE}),
        frozenset({FISH_VEHICLE_LEASE_CHARGES_NET}),
    ),
    (
        ApplyRatio,
        frozenset(
            {
                FISH_VEHICLE_LEASE_COST_LIMIT_WITH_TAX,
                FISH_VEHICLE_LEASE_CHARGES,
                FISH_VEHICLE_LEASE_PRICE_85_PERCENT,
            }
        ),
        frozenset({FISH_VEHICLE_LEASE_COST_PORTION}),
    ),
    (
        LesserOf,
        frozenset({FISH_VEHICLE_LEASE_CHARGES_NET, FISH_VEHICLE_LEASE_COST_PORTION}),
        frozenset({FISH_VEHICLE_LEASING_COST}),
    ),
    (
        Sum,
        frozenset(
            {
                FISH_VEHICLE_FUEL_AND_OIL,
                FISH_VEHICLE_AVAILABLE_INTEREST,
                FISH_VEHICLE_INSURANCE,
                FISH_VEHICLE_LICENCE_AND_REGISTRATION,
                FISH_VEHICLE_MAINTENANCE_AND_REPAIRS,
                FISH_VEHICLE_LEASING_COST,
                FISH_VEHICLE_ELECTRICITY_ZEV,
                FISH_VEHICLE_OTHER_EXPENSES_10,
                FISH_VEHICLE_OTHER_EXPENSES_11,
            }
        ),
        frozenset({FISH_VEHICLE_TOTAL_EXPENSES}),
    ),
    (
        ApplyRatioOrZero,
        frozenset(
            {
                FISH_VEHICLE_TOTAL_EXPENSES,
                FISH_VEHICLE_BUSINESS_KILOMETRES,
                FISH_VEHICLE_TOTAL_KILOMETRES,
            }
        ),
        frozenset({FISH_VEHICLE_BUSINESS_USE_PART}),
    ),
    (
        Sum,
        frozenset(
            {
                FISH_VEHICLE_BUSINESS_USE_PART,
                FISH_VEHICLE_PARKING_FEES,
                FISH_VEHICLE_SUPPLEMENTARY_INSURANCE,
            }
        ),
        frozenset({FISH_MOTOR_VEHICLE_EXPENSES}),
    ),
}
