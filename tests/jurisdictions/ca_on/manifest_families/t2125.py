"""The CA-ON manifest entries of Form T2125 (see `test_manifest.py` and `test_manifest_t2125.py`).

T2125 is a form of the manifest: its 55 selections belong to the form `ca/t2125` (`FORM_STEPS`),
run once for each statement of `ca/t2125_statements`, whose fields are the T2125 inputs
(`FORM_INPUTS`). The form exports three artifacts, each readable by the other forms as
`ca/t2125.<export>` (`FORM_EXPORTS`); the return reads one and declares no output for the two
nothing reads (`OUTPUTS` is empty). The return's own entries are the instances input, the total of
the net income over the statements that is T1 line 13500 (`STEPS` and `WIRING`), and the five
printed constants of Charts B and C that Form T2121 reads (the form has its own copy of
each).
"""

from __future__ import annotations

from app.domain.capabilities.apply_rate import ApplyRate
from app.domain.capabilities.apply_ratio import ApplyRatio
from app.domain.capabilities.choose_by_count import ChooseByCount
from app.domain.capabilities.credit_amount import CreditAmount
from app.domain.capabilities.greater_of import GreaterOf
from app.domain.capabilities.lesser_of import LesserOf
from app.domain.capabilities.record_total import RecordTotal
from app.domain.capabilities.subtract import Subtract
from app.domain.capabilities.subtract_not_below_zero import SubtractNotBelowZero
from app.domain.capabilities.sum import Sum
from app.domain.capabilities.sum_not_below_zero import SumNotBelowZero
from app.domain.manifest import CapabilitySelection
from app.domain.record_list import RecordListKind
from app.jurisdictions.ca.capabilities.apply_percentage import ApplyPercentage
from app.jurisdictions.ca.capabilities.apply_ratio_or_zero import ApplyRatioOrZero
from app.jurisdictions.ca.capabilities.cca_claim import CcaClaim
from app.jurisdictions.ca.capabilities.closing_ucc import ClosingUcc
from app.jurisdictions.ca.capabilities.recaptured_cca import RecapturedCca
from app.jurisdictions.ca.capabilities.terminal_loss import TerminalLoss
from app.jurisdictions.ca.catalog import (
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
    BUSINESS_VEHICLE_AVAILABLE_INTEREST,
    BUSINESS_VEHICLE_BUSINESS_KILOMETRES,
    BUSINESS_VEHICLE_BUSINESS_USE_PART,
    BUSINESS_VEHICLE_DAYS_DIVISOR,
    BUSINESS_VEHICLE_ELECTRICITY_ZEV,
    BUSINESS_VEHICLE_FUEL_AND_OIL,
    BUSINESS_VEHICLE_INSURANCE,
    BUSINESS_VEHICLE_INTEREST_DAYS,
    BUSINESS_VEHICLE_INTEREST_FOR_PERIOD,
    BUSINESS_VEHICLE_INTEREST_LIMIT,
    BUSINESS_VEHICLE_INTEREST_PAYABLE,
    BUSINESS_VEHICLE_LEASE_CHARGE_LIMIT,
    BUSINESS_VEHICLE_LEASE_CHARGE_LIMIT_TAX,
    BUSINESS_VEHICLE_LEASE_CHARGE_LIMIT_WITH_TAX,
    BUSINESS_VEHICLE_LEASE_CHARGE_PORTION,
    BUSINESS_VEHICLE_LEASE_CHARGES,
    BUSINESS_VEHICLE_LEASE_CHARGES_NET,
    BUSINESS_VEHICLE_LEASE_COST_LIMIT,
    BUSINESS_VEHICLE_LEASE_COST_LIMIT_TAX,
    BUSINESS_VEHICLE_LEASE_COST_LIMIT_WITH_TAX,
    BUSINESS_VEHICLE_LEASE_COST_PORTION,
    BUSINESS_VEHICLE_LEASE_DAYS,
    BUSINESS_VEHICLE_LEASE_PAYMENTS_BEFORE,
    BUSINESS_VEHICLE_LEASE_PRICE_85_PERCENT,
    BUSINESS_VEHICLE_LEASE_PRICE_BASE,
    BUSINESS_VEHICLE_LEASING_COST,
    BUSINESS_VEHICLE_LICENCE_AND_REGISTRATION,
    BUSINESS_VEHICLE_LIST_PRICE,
    BUSINESS_VEHICLE_LIST_PRICE_LIMIT,
    BUSINESS_VEHICLE_LIST_PRICE_LIMIT_TAX,
    BUSINESS_VEHICLE_LIST_PRICE_LIMIT_WITH_TAX,
    BUSINESS_VEHICLE_MAINTENANCE_AND_REPAIRS,
    BUSINESS_VEHICLE_OTHER_EXPENSES_10,
    BUSINESS_VEHICLE_OTHER_EXPENSES_11,
    BUSINESS_VEHICLE_PARKING_FEES,
    BUSINESS_VEHICLE_SALES_TAX_RATE,
    BUSINESS_VEHICLE_SUPPLEMENTARY_INSURANCE,
    BUSINESS_VEHICLE_TOTAL_EXPENSES,
    BUSINESS_VEHICLE_TOTAL_KILOMETRES,
)

NET_INCOME_PER_STATEMENT = RecordListKind("ca/t2125.business_income", fields=(BUSINESS_INCOME,))
BUSINESS_CLOSING_UCC_PER_STATEMENT = RecordListKind(
    "ca/t2125.business_closing_ucc", fields=(BUSINESS_CLOSING_UCC,)
)
BUSINESS_HOME_CARRY_FORWARD_PER_STATEMENT = RecordListKind(
    "ca/t2125.business_home_carry_forward", fields=(BUSINESS_HOME_CARRY_FORWARD,)
)

FORM_INPUTS = frozenset(
    {
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
        "ca/business_vehicle_business_kilometres",
        "ca/business_vehicle_total_kilometres",
        "ca/business_vehicle_fuel_and_oil",
        "ca/business_vehicle_insurance",
        "ca/business_vehicle_licence_and_registration",
        "ca/business_vehicle_maintenance_and_repairs",
        "ca/business_vehicle_electricity_zev",
        "ca/business_vehicle_other_expenses_10",
        "ca/business_vehicle_other_expenses_11",
        "ca/business_vehicle_parking_fees",
        "ca/business_vehicle_supplementary_insurance",
        "ca/business_vehicle_interest_payable",
        "ca/business_vehicle_interest_days",
        "ca/business_vehicle_lease_charges",
        "ca/business_vehicle_lease_payments_before",
        "ca/business_vehicle_lease_days",
        "ca/business_vehicle_list_price",
        "ca/business_vehicle_sales_tax_rate",
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
    }
)

FORM_STEPS = {
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
    # T2125 Chart B "Available interest expense for passenger vehicles and zero-emission passenger
    # vehicles" and Chart C "Eligible leasing cost for passenger vehicles": the printed constants
    # are datasets of the same name, one artifact each ("$350***", "÷ 30", "$44,706", "$1,100" and
    # "$38,000"), and the amounts of the charts are the steps that follow.
    CapabilitySelection(
        name="core/credit_amount",
        params={"amount": "ca/business_vehicle_interest_limit"},
        consumes={},
        produces={"output": "ca/business_vehicle_interest_limit"},
    ),
    CapabilitySelection(
        name="core/credit_amount",
        params={"amount": "ca/business_vehicle_days_divisor"},
        consumes={},
        produces={"output": "ca/business_vehicle_days_divisor"},
    ),
    CapabilitySelection(
        name="core/credit_amount",
        params={"amount": "ca/business_vehicle_list_price_limit"},
        consumes={},
        produces={"output": "ca/business_vehicle_list_price_limit"},
    ),
    CapabilitySelection(
        name="core/credit_amount",
        params={"amount": "ca/business_vehicle_lease_charge_limit"},
        consumes={},
        produces={"output": "ca/business_vehicle_lease_charge_limit"},
    ),
    CapabilitySelection(
        name="core/credit_amount",
        params={"amount": "ca/business_vehicle_lease_cost_limit"},
        consumes={},
        produces={"output": "ca/business_vehicle_lease_cost_limit"},
    ),
    # Chart B line 18 "($350*** ÷ 30) × the number of days in the fiscal period for which interest
    # was payable (accrual method) or paid (cash method)".
    CapabilitySelection(
        name="core/apply_ratio",
        params={"rounding": "ca/business_vehicle_interest_rounding"},
        consumes={
            "amount": "ca/business_vehicle_interest_limit",
            "numerator": "ca/business_vehicle_interest_days",
            "denominator": "ca/business_vehicle_days_divisor",
        },
        produces={"output": "ca/business_vehicle_interest_for_period"},
    ),
    # Chart B line 19 "Available interest expense: Amount 17 or 18, whichever is less (include this
    # in amount 4 of Chart A above)": the lesser of line 17 "Total interest payable (accrual method)
    # or paid (cash method) in the fiscal period" and line 18.
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={
            "amounts": (
                "ca/business_vehicle_interest_payable",
                "ca/business_vehicle_interest_for_period",
            ),
        },
        produces={"output": "ca/business_vehicle_available_interest"},
    ),
    # Chart C: the sales tax (GST and PST, or HST) on each printed amount at the rate of the
    # caller's province, "Use a GST rate of 5% or HST rate applicable to your province.", then the
    # printed amount plus that tax.
    CapabilitySelection(
        name="ca/apply_percentage",
        params={"rounding": "ca/business_vehicle_sales_tax_rounding"},
        consumes={
            "amount": "ca/business_vehicle_list_price_limit",
            "percentage": "ca/business_vehicle_sales_tax_rate",
        },
        produces={"output": "ca/business_vehicle_list_price_limit_tax"},
    ),
    CapabilitySelection(
        name="ca/apply_percentage",
        params={"rounding": "ca/business_vehicle_sales_tax_rounding"},
        consumes={
            "amount": "ca/business_vehicle_lease_charge_limit",
            "percentage": "ca/business_vehicle_sales_tax_rate",
        },
        produces={"output": "ca/business_vehicle_lease_charge_limit_tax"},
    ),
    CapabilitySelection(
        name="ca/apply_percentage",
        params={"rounding": "ca/business_vehicle_sales_tax_rounding"},
        consumes={
            "amount": "ca/business_vehicle_lease_cost_limit",
            "percentage": "ca/business_vehicle_sales_tax_rate",
        },
        produces={"output": "ca/business_vehicle_lease_cost_limit_tax"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/business_vehicle_list_price_limit",
                "ca/business_vehicle_list_price_limit_tax",
            ),
        },
        produces={"output": "ca/business_vehicle_list_price_limit_with_tax"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/business_vehicle_lease_charge_limit",
                "ca/business_vehicle_lease_charge_limit_tax",
            ),
        },
        produces={"output": "ca/business_vehicle_lease_charge_limit_with_tax"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/business_vehicle_lease_cost_limit",
                "ca/business_vehicle_lease_cost_limit_tax",
            ),
        },
        produces={"output": "ca/business_vehicle_lease_cost_limit_with_tax"},
    ),
    # Chart C line 23 "Amount 23 or ($44,706 + GST and PST, or $44,706 + HST), whichever is more".
    CapabilitySelection(
        name="core/greater_of",
        params={},
        consumes={
            "amounts": (
                "ca/business_vehicle_list_price",
                "ca/business_vehicle_list_price_limit_with_tax",
            ),
        },
        produces={"output": "ca/business_vehicle_lease_price_base"},
    ),
    # Chart C line 24 "Amount 23 or ($44,706 + GST and PST, or $44,706 + HST), whichever is more ×
    # 85%".
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/business_vehicle_lease_price_rate"},
        consumes={"base": "ca/business_vehicle_lease_price_base"},
        produces={"output": "ca/business_vehicle_lease_price_85_percent"},
    ),
    # Chart C line 25 "[($1,100 + GST and PST, or $1,100 + HST) × amount 22] ÷ 30".
    CapabilitySelection(
        name="core/apply_ratio",
        params={"rounding": "ca/business_vehicle_lease_charge_rounding"},
        consumes={
            "amount": "ca/business_vehicle_lease_charge_limit_with_tax",
            "numerator": "ca/business_vehicle_lease_days",
            "denominator": "ca/business_vehicle_days_divisor",
        },
        produces={"output": "ca/business_vehicle_lease_charge_portion"},
    ),
    # Chart C line 26, printed "Amount 25: amount 21" with a subtraction sign: amount 25 less amount
    # 21, signed (a negative result is kept).
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/business_vehicle_lease_charge_portion",
            "less": "ca/business_vehicle_lease_payments_before",
        },
        produces={"output": "ca/business_vehicle_lease_charges_net"},
    ),
    # Chart C line 27 "[($38,000 + GST and PST, or $38,000 + HST) × amount 20] ÷ amount 24".
    CapabilitySelection(
        name="core/apply_ratio",
        params={"rounding": "ca/business_vehicle_lease_cost_rounding"},
        consumes={
            "amount": "ca/business_vehicle_lease_cost_limit_with_tax",
            "numerator": "ca/business_vehicle_lease_charges",
            "denominator": "ca/business_vehicle_lease_price_85_percent",
        },
        produces={"output": "ca/business_vehicle_lease_cost_portion"},
    ),
    # Chart C line 28 "Eligible leasing cost: Amount 26 or 27, whichever is less (enter in amount 8
    # of Chart A above)".
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={
            "amounts": (
                "ca/business_vehicle_lease_charges_net",
                "ca/business_vehicle_lease_cost_portion",
            ),
        },
        produces={"output": "ca/business_vehicle_leasing_cost"},
    ),
    # Chart A line 12 "Total motor vehicle expenses: Add amounts 3 to 11.", amount 4 being line 19
    # and amount 8 being line 28.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/business_vehicle_fuel_and_oil",
                "ca/business_vehicle_available_interest",
                "ca/business_vehicle_insurance",
                "ca/business_vehicle_licence_and_registration",
                "ca/business_vehicle_maintenance_and_repairs",
                "ca/business_vehicle_leasing_cost",
                "ca/business_vehicle_electricity_zev",
                "ca/business_vehicle_other_expenses_10",
                "ca/business_vehicle_other_expenses_11",
            ),
        },
        produces={"output": "ca/business_vehicle_total_expenses"},
    ),
    # Chart A line 13 "Business use part: amount 1 ÷ amount 2 × amount 12 = 13".
    CapabilitySelection(
        name="ca/apply_ratio_or_zero",
        params={"rounding": "ca/business_vehicle_business_use_rounding"},
        consumes={
            "amount": "ca/business_vehicle_total_expenses",
            "numerator": "ca/business_vehicle_business_kilometres",
            "denominator": "ca/business_vehicle_total_kilometres",
        },
        produces={"output": "ca/business_vehicle_business_use_part"},
    ),
    # Chart A line 16 "Allowable motor vehicle expenses: Add amounts 13 to 15 (enter this total on
    # line 9281 of Part 4)": the line 9281 kind, produced here and no longer a caller input.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/business_vehicle_business_use_part",
                "ca/business_vehicle_parking_fees",
                "ca/business_vehicle_supplementary_insurance",
            ),
        },
        produces={"output": "ca/business_motor_vehicle_expenses"},
    ),
    # T2125 Part 4 "Total expenses: Total of amounts 4B to 4V 9368": the 19 expense lines 4B
    # to 4T ("Advertising" to "Motor vehicle expenses (not including CCA) (amount 16 of
    # Chart A)", the caller's inputs except 4T, which is the Chart A steps above), then 4U
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

INPUTS = frozenset({"ca/t2125_statements"})

FORM_EXPORTS = (
    "ca/business_income",
    "ca/business_closing_ucc",
    "ca/business_home_carry_forward",
)

# The form exports Area A column 22 "UCC at the end of the year" (for next year) and Part 7 line 7O
# "Business-use-of-home expenses available to carry forward", which no line of the return reads: an
# export nobody reads is fine, so the return declares no output for them.
OUTPUTS: frozenset[str] = frozenset()

# T1 line 13500 "Net": the total of T2125 line 9946 over the statements; and the five printed
# constants of Charts B and C that Form T2121 reads from the return.
STEPS = {
    CapabilitySelection(
        name="core/record_total",
        params={},
        consumes={"records": "ca/t2125.business_income"},
        produces={"output": "ca/business_income"},
    ),
    CapabilitySelection(
        name="core/credit_amount",
        params={"amount": "ca/business_vehicle_interest_limit"},
        consumes={},
        produces={"output": "ca/business_vehicle_interest_limit"},
    ),
    CapabilitySelection(
        name="core/credit_amount",
        params={"amount": "ca/business_vehicle_days_divisor"},
        consumes={},
        produces={"output": "ca/business_vehicle_days_divisor"},
    ),
    CapabilitySelection(
        name="core/credit_amount",
        params={"amount": "ca/business_vehicle_list_price_limit"},
        consumes={},
        produces={"output": "ca/business_vehicle_list_price_limit"},
    ),
    CapabilitySelection(
        name="core/credit_amount",
        params={"amount": "ca/business_vehicle_lease_charge_limit"},
        consumes={},
        produces={"output": "ca/business_vehicle_lease_charge_limit"},
    ),
    CapabilitySelection(
        name="core/credit_amount",
        params={"amount": "ca/business_vehicle_lease_cost_limit"},
        consumes={},
        produces={"output": "ca/business_vehicle_lease_cost_limit"},
    ),
}

FORM_WIRING = {
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
    (CreditAmount, frozenset(), frozenset({BUSINESS_VEHICLE_INTEREST_LIMIT})),
    (CreditAmount, frozenset(), frozenset({BUSINESS_VEHICLE_DAYS_DIVISOR})),
    (CreditAmount, frozenset(), frozenset({BUSINESS_VEHICLE_LIST_PRICE_LIMIT})),
    (CreditAmount, frozenset(), frozenset({BUSINESS_VEHICLE_LEASE_CHARGE_LIMIT})),
    (CreditAmount, frozenset(), frozenset({BUSINESS_VEHICLE_LEASE_COST_LIMIT})),
    (
        ApplyRatio,
        frozenset(
            {
                BUSINESS_VEHICLE_INTEREST_LIMIT,
                BUSINESS_VEHICLE_INTEREST_DAYS,
                BUSINESS_VEHICLE_DAYS_DIVISOR,
            }
        ),
        frozenset({BUSINESS_VEHICLE_INTEREST_FOR_PERIOD}),
    ),
    (
        LesserOf,
        frozenset({BUSINESS_VEHICLE_INTEREST_PAYABLE, BUSINESS_VEHICLE_INTEREST_FOR_PERIOD}),
        frozenset({BUSINESS_VEHICLE_AVAILABLE_INTEREST}),
    ),
    (
        ApplyPercentage,
        frozenset({BUSINESS_VEHICLE_LIST_PRICE_LIMIT, BUSINESS_VEHICLE_SALES_TAX_RATE}),
        frozenset({BUSINESS_VEHICLE_LIST_PRICE_LIMIT_TAX}),
    ),
    (
        ApplyPercentage,
        frozenset({BUSINESS_VEHICLE_LEASE_CHARGE_LIMIT, BUSINESS_VEHICLE_SALES_TAX_RATE}),
        frozenset({BUSINESS_VEHICLE_LEASE_CHARGE_LIMIT_TAX}),
    ),
    (
        ApplyPercentage,
        frozenset({BUSINESS_VEHICLE_LEASE_COST_LIMIT, BUSINESS_VEHICLE_SALES_TAX_RATE}),
        frozenset({BUSINESS_VEHICLE_LEASE_COST_LIMIT_TAX}),
    ),
    (
        Sum,
        frozenset({BUSINESS_VEHICLE_LIST_PRICE_LIMIT, BUSINESS_VEHICLE_LIST_PRICE_LIMIT_TAX}),
        frozenset({BUSINESS_VEHICLE_LIST_PRICE_LIMIT_WITH_TAX}),
    ),
    (
        Sum,
        frozenset({BUSINESS_VEHICLE_LEASE_CHARGE_LIMIT, BUSINESS_VEHICLE_LEASE_CHARGE_LIMIT_TAX}),
        frozenset({BUSINESS_VEHICLE_LEASE_CHARGE_LIMIT_WITH_TAX}),
    ),
    (
        Sum,
        frozenset({BUSINESS_VEHICLE_LEASE_COST_LIMIT, BUSINESS_VEHICLE_LEASE_COST_LIMIT_TAX}),
        frozenset({BUSINESS_VEHICLE_LEASE_COST_LIMIT_WITH_TAX}),
    ),
    (
        GreaterOf,
        frozenset({BUSINESS_VEHICLE_LIST_PRICE, BUSINESS_VEHICLE_LIST_PRICE_LIMIT_WITH_TAX}),
        frozenset({BUSINESS_VEHICLE_LEASE_PRICE_BASE}),
    ),
    (
        ApplyRate,
        frozenset({BUSINESS_VEHICLE_LEASE_PRICE_BASE}),
        frozenset({BUSINESS_VEHICLE_LEASE_PRICE_85_PERCENT}),
    ),
    (
        ApplyRatio,
        frozenset(
            {
                BUSINESS_VEHICLE_LEASE_CHARGE_LIMIT_WITH_TAX,
                BUSINESS_VEHICLE_LEASE_DAYS,
                BUSINESS_VEHICLE_DAYS_DIVISOR,
            }
        ),
        frozenset({BUSINESS_VEHICLE_LEASE_CHARGE_PORTION}),
    ),
    (
        Subtract,
        frozenset({BUSINESS_VEHICLE_LEASE_CHARGE_PORTION, BUSINESS_VEHICLE_LEASE_PAYMENTS_BEFORE}),
        frozenset({BUSINESS_VEHICLE_LEASE_CHARGES_NET}),
    ),
    (
        ApplyRatio,
        frozenset(
            {
                BUSINESS_VEHICLE_LEASE_COST_LIMIT_WITH_TAX,
                BUSINESS_VEHICLE_LEASE_CHARGES,
                BUSINESS_VEHICLE_LEASE_PRICE_85_PERCENT,
            }
        ),
        frozenset({BUSINESS_VEHICLE_LEASE_COST_PORTION}),
    ),
    (
        LesserOf,
        frozenset({BUSINESS_VEHICLE_LEASE_CHARGES_NET, BUSINESS_VEHICLE_LEASE_COST_PORTION}),
        frozenset({BUSINESS_VEHICLE_LEASING_COST}),
    ),
    (
        Sum,
        frozenset(
            {
                BUSINESS_VEHICLE_FUEL_AND_OIL,
                BUSINESS_VEHICLE_AVAILABLE_INTEREST,
                BUSINESS_VEHICLE_INSURANCE,
                BUSINESS_VEHICLE_LICENCE_AND_REGISTRATION,
                BUSINESS_VEHICLE_MAINTENANCE_AND_REPAIRS,
                BUSINESS_VEHICLE_LEASING_COST,
                BUSINESS_VEHICLE_ELECTRICITY_ZEV,
                BUSINESS_VEHICLE_OTHER_EXPENSES_10,
                BUSINESS_VEHICLE_OTHER_EXPENSES_11,
            }
        ),
        frozenset({BUSINESS_VEHICLE_TOTAL_EXPENSES}),
    ),
    (
        ApplyRatioOrZero,
        frozenset(
            {
                BUSINESS_VEHICLE_TOTAL_EXPENSES,
                BUSINESS_VEHICLE_BUSINESS_KILOMETRES,
                BUSINESS_VEHICLE_TOTAL_KILOMETRES,
            }
        ),
        frozenset({BUSINESS_VEHICLE_BUSINESS_USE_PART}),
    ),
    (
        Sum,
        frozenset(
            {
                BUSINESS_VEHICLE_BUSINESS_USE_PART,
                BUSINESS_VEHICLE_PARKING_FEES,
                BUSINESS_VEHICLE_SUPPLEMENTARY_INSURANCE,
            }
        ),
        frozenset({BUSINESS_MOTOR_VEHICLE_EXPENSES}),
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

WIRING = {
    (RecordTotal, frozenset({NET_INCOME_PER_STATEMENT}), frozenset({BUSINESS_INCOME})),
    (CreditAmount, frozenset(), frozenset({BUSINESS_VEHICLE_INTEREST_LIMIT})),
    (CreditAmount, frozenset(), frozenset({BUSINESS_VEHICLE_DAYS_DIVISOR})),
    (CreditAmount, frozenset(), frozenset({BUSINESS_VEHICLE_LIST_PRICE_LIMIT})),
    (CreditAmount, frozenset(), frozenset({BUSINESS_VEHICLE_LEASE_CHARGE_LIMIT})),
    (CreditAmount, frozenset(), frozenset({BUSINESS_VEHICLE_LEASE_COST_LIMIT})),
}
