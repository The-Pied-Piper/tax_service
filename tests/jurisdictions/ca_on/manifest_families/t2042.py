"""The CA-ON manifest entries of Form T2042 (see `test_manifest.py` and `test_manifest_t2042.py`).

T2042 is a form of the manifest: its 39 selections belong to the form `ca/t2042` (`FORM_STEPS`),
run once for each statement of `ca/t2042_statements`, whose fields are the T2042 inputs
(`FORM_INPUTS`). The form exports four artifacts, each readable by the other forms as
`ca/t2042.<export>` (`FORM_EXPORTS`); the return reads one and declares no output for the three
nothing reads (`OUTPUTS` is empty). The return's own entries are the instances input and the total
of the net income over the statements that is T1 line 14100 (`STEPS` and `WIRING`); the form selects
one step over the statement's vehicles, whose printed constants of Charts B and C are datasets.
"""

from __future__ import annotations

from app.domain.capabilities.choose_by_count import ChooseByCount
from app.domain.capabilities.credit_amount import CreditAmount
from app.domain.capabilities.lesser_of import LesserOf
from app.domain.capabilities.record_total import RecordTotal
from app.domain.capabilities.subtract import Subtract
from app.domain.capabilities.subtract_not_below_zero import SubtractNotBelowZero
from app.domain.capabilities.sum import Sum
from app.domain.capabilities.sum_not_below_zero import SumNotBelowZero
from app.domain.capabilities.times_count import TimesCount
from app.domain.manifest import CapabilitySelection
from app.domain.record_list import RecordListKind
from app.jurisdictions.ca.capabilities.apply_percentage import ApplyPercentage
from app.jurisdictions.ca.capabilities.business_vehicle_expenses import BusinessVehicleExpenses
from app.jurisdictions.ca.capabilities.cca_claim_prorated import CcaClaimProrated
from app.jurisdictions.ca.capabilities.choose_by_sign import ChooseBySign
from app.jurisdictions.ca.capabilities.closing_ucc_prorated import ClosingUccProrated
from app.jurisdictions.ca.capabilities.fiscal_period_days import FiscalPeriodDays
from app.jurisdictions.ca.capabilities.immediate_expensing_claim import ImmediateExpensingClaim
from app.jurisdictions.ca.capabilities.recaptured_cca import RecapturedCca
from app.jurisdictions.ca.capabilities.terminal_loss import TerminalLoss
from app.jurisdictions.ca.catalog import (
    BUSINESS_VEHICLES,
    FARM_BARLEY,
    FARM_BUILDING_REPAIRS_AND_MAINTENANCE,
    FARM_CANOLA,
    FARM_CATTLE,
    FARM_CCA_CLAIM,
    FARM_CCA_CLAIM_LESS_PERSONAL_PART,
    FARM_CCA_CLASSES,
    FARM_CCA_PERSONAL_PART,
    FARM_CCA_TABLE_CLAIM,
    FARM_CLEARING_LEVELLING_AND_DRAINING,
    FARM_CLOSING_UCC,
    FARM_CONTAINERS_AND_TWINE,
    FARM_CORN,
    FARM_CROP_INSURANCE,
    FARM_CROP_INSURANCE_PREMIUMS,
    FARM_CUSTOM_WORK,
    FARM_CUSTOM_WORK_EXPENSES,
    FARM_DAIRY_SUBSIDIES,
    FARM_EGGS,
    FARM_ELECTRICITY,
    FARM_EPOP_AGREEMENT_FILED,
    FARM_EPOP_ASSOCIATED,
    FARM_EPOP_PERCENTAGE,
    FARM_EPOP_PERCENTAGE_MAXIMUM,
    FARM_EPOP_PERCENTAGE_ROOM,
    FARM_EPOP_PERCENTAGE_TOTAL,
    FARM_EXPENSES_SUBTOTAL,
    FARM_FEED_SUPPLEMENTS_STRAW_AND_BEDDING,
    FARM_FERTILIZERS_AND_LIME,
    FARM_FISCAL_PERIOD_DAYS,
    FARM_FISCAL_PERIOD_DAYS_ENTERED,
    FARM_FLAXSEED,
    FARM_FORAGE_CROPS_OR_SEEDS,
    FARM_FRUIT,
    FARM_FUEL_CHARGE_CREDIT,
    FARM_GASOLINE_DIESEL_AND_OIL,
    FARM_GRAINS_AND_OILSEEDS,
    FARM_GREENHOUSE_AND_NURSERY,
    FARM_GROSS_INCOME,
    FARM_GROSS_INCOME_BEFORE_EXPENSES,
    FARM_HEATING_AND_CURING_FUEL,
    FARM_HOME_ALLOWABLE_CLAIM,
    FARM_HOME_CARRIED_FORWARD,
    FARM_HOME_CARRY_FORWARD,
    FARM_HOME_CCA,
    FARM_HOME_ELECTRICITY,
    FARM_HOME_EXPENSES,
    FARM_HOME_EXPENSES_AVAILABLE,
    FARM_HOME_EXPENSES_BUSINESS_PART,
    FARM_HOME_EXPENSES_SUBTOTAL,
    FARM_HOME_HEAT,
    FARM_HOME_INCOME_LIMIT,
    FARM_HOME_INSURANCE,
    FARM_HOME_MAINTENANCE,
    FARM_HOME_MORTGAGE_INTEREST,
    FARM_HOME_OTHER_EXPENSES,
    FARM_HOME_PERSONAL_USE_PART,
    FARM_HOME_PROPERTY_TAXES,
    FARM_IMMEDIATE_EXPENSING_ALLOCATED,
    FARM_IMMEDIATE_EXPENSING_ASSOCIATED_LIMIT,
    FARM_IMMEDIATE_EXPENSING_CAP,
    FARM_IMMEDIATE_EXPENSING_CLAIM,
    FARM_IMMEDIATE_EXPENSING_LIMIT,
    FARM_IMMEDIATE_EXPENSING_LIMIT_BEFORE_MINISTER,
    FARM_IMMEDIATE_EXPENSING_SHARE,
    FARM_INCOME_BEFORE_CCA,
    FARM_INSURANCE,
    FARM_INSURANCE_PROCEEDS,
    FARM_INSURANCE_PROGRAM_OVERPAYMENT_RECAPTURE,
    FARM_INTEREST_AND_BANK_CHARGES,
    FARM_LIVESTOCK_AND_ANIMAL_PRODUCTS_REVENUE,
    FARM_LIVESTOCK_PURCHASED,
    FARM_MACHINERY_REPAIRS_LICENCES_AND_INSURANCE,
    FARM_MANDATORY_INVENTORY_ADJUSTMENT_CURRENT_YEAR,
    FARM_MANDATORY_INVENTORY_ADJUSTMENT_PREVIOUS_YEAR,
    FARM_MILK_AND_CREAM,
    FARM_MINISTER_ALLOCATION,
    FARM_MINISTER_ALLOCATION_GIVEN,
    FARM_MIXED_GRAINS,
    FARM_MOTOR_VEHICLE_EXPENSES,
    FARM_NET_INCOME_AFTER_ADJUSTMENTS,
    FARM_NET_INCOME_AFTER_INVENTORY_ADJUSTMENTS,
    FARM_NET_INCOME_BEFORE_ADJUSTMENTS,
    FARM_OATS,
    FARM_OFFICE_EXPENSES,
    FARM_OPTIONAL_INVENTORY_ADJUSTMENT_CURRENT_YEAR,
    FARM_OPTIONAL_INVENTORY_ADJUSTMENT_PREVIOUS_YEAR,
    FARM_OTHER_COMMODITIES,
    FARM_OTHER_CROPS,
    FARM_OTHER_EXPENSES,
    FARM_OTHER_EXPENSES_WITH_TERMINAL_LOSS,
    FARM_OTHER_INCOME,
    FARM_OTHER_INCOME_WITH_RECAPTURE,
    FARM_OTHER_PROGRAM_PAYMENTS,
    FARM_PARTNER,
    FARM_PARTNER_GST_HST_REBATE,
    FARM_PARTNER_OTHER_AMOUNT_A,
    FARM_PARTNER_OTHER_AMOUNT_B,
    FARM_PARTNER_OTHER_AMOUNT_C,
    FARM_PARTNER_OTHER_AMOUNT_D,
    FARM_PARTNER_OTHER_AMOUNT_E,
    FARM_PARTNER_OTHER_AMOUNTS,
    FARM_PARTNER_OTHER_AMOUNTS_TOTAL,
    FARM_PARTNER_SHARE,
    FARM_PARTNERSHIP_TOTAL,
    FARM_PATRONAGE_DIVIDENDS,
    FARM_PESTICIDES,
    FARM_POTATOES,
    FARM_POULTRY,
    FARM_PROFESSIONAL_FEES,
    FARM_PROPERTY_TAXES,
    FARM_REBATES,
    FARM_RECAPTURED_CCA,
    FARM_RENT,
    FARM_SALARIES_WAGES_AND_BENEFITS,
    FARM_SEEDS_AND_PLANTS,
    FARM_SHARE_OF_NET_INCOME,
    FARM_SHEEP_AND_LAMBS,
    FARM_SMALL_TOOLS,
    FARM_SOYBEANS,
    FARM_SWINE,
    FARM_TERMINAL_LOSS,
    FARM_TOBACCO,
    FARM_TOTAL_EXPENSES,
    FARM_VEGETABLES,
    FARM_VEHICLE_SALES_TAX_RATE,
    FARM_VETERINARY_FEES,
    FARM_WHEAT,
    FARMING_INCOME,
)

NET_INCOME_PER_STATEMENT = RecordListKind("ca/t2042.farming_income", fields=(FARMING_INCOME,))
FARM_CLOSING_UCC_PER_STATEMENT = RecordListKind(
    "ca/t2042.farm_closing_ucc", fields=(FARM_CLOSING_UCC,)
)
FARM_HOME_CARRY_FORWARD_PER_STATEMENT = RecordListKind(
    "ca/t2042.farm_home_carry_forward", fields=(FARM_HOME_CARRY_FORWARD,)
)

FARM_IMMEDIATE_EXPENSING_CLAIM_PER_STATEMENT = RecordListKind(
    "ca/t2042.farm_immediate_expensing_claim", fields=(FARM_IMMEDIATE_EXPENSING_CLAIM,)
)

FORM_INPUTS = frozenset(
    {
        "ca/farm_wheat",
        "ca/farm_oats",
        "ca/farm_barley",
        "ca/farm_mixed_grains",
        "ca/farm_corn",
        "ca/farm_canola",
        "ca/farm_flaxseed",
        "ca/farm_soybeans",
        "ca/farm_grains_and_oilseeds",
        "ca/farm_fruit",
        "ca/farm_potatoes",
        "ca/farm_vegetables",
        "ca/farm_tobacco",
        "ca/farm_greenhouse_and_nursery",
        "ca/farm_forage_crops_or_seeds",
        "ca/farm_other_crops",
        "ca/farm_cattle",
        "ca/farm_swine",
        "ca/farm_poultry",
        "ca/farm_sheep_and_lambs",
        "ca/farm_livestock_and_animal_products_revenue",
        "ca/farm_milk_and_cream",
        "ca/farm_eggs",
        "ca/farm_other_commodities",
        "ca/farm_dairy_subsidies",
        "ca/farm_crop_insurance",
        "ca/farm_other_program_payments",
        "ca/farm_rebates",
        "ca/farm_custom_work",
        "ca/farm_insurance_proceeds",
        "ca/farm_patronage_dividends",
        "ca/farm_other_income",
        "ca/farm_containers_and_twine",
        "ca/farm_fertilizers_and_lime",
        "ca/farm_pesticides",
        "ca/farm_seeds_and_plants",
        "ca/farm_feed_supplements_straw_and_bedding",
        "ca/farm_livestock_purchased",
        "ca/farm_veterinary_fees",
        "ca/farm_machinery_repairs_licences_and_insurance",
        "ca/farm_gasoline_diesel_and_oil",
        "ca/farm_building_repairs_and_maintenance",
        "ca/farm_clearing_levelling_and_draining",
        "ca/farm_crop_insurance_premiums",
        "ca/farm_custom_work_expenses",
        "ca/farm_electricity",
        "ca/farm_heating_and_curing_fuel",
        "ca/farm_insurance_program_overpayment_recapture",
        "ca/farm_insurance",
        "ca/farm_interest_and_bank_charges",
        "ca/farm_office_expenses",
        "ca/farm_professional_fees",
        "ca/farm_property_taxes",
        "ca/farm_rent",
        "ca/farm_salaries_wages_and_benefits",
        "ca/business_vehicles",
        "ca/farm_vehicle_sales_tax_rate",
        "ca/farm_small_tools",
        "ca/farm_mandatory_inventory_adjustment_previous_year",
        "ca/farm_optional_inventory_adjustment_previous_year",
        "ca/farm_other_expenses",
        "ca/farm_optional_inventory_adjustment_current_year",
        "ca/farm_mandatory_inventory_adjustment_current_year",
        "ca/farm_cca_personal_part",
        "ca/farm_partner",
        "ca/farm_partner_share",
        "ca/farm_fuel_charge_credit",
        "ca/farm_partner_gst_hst_rebate",
        "ca/farm_partner_other_amount_a",
        "ca/farm_partner_other_amount_b",
        "ca/farm_partner_other_amount_c",
        "ca/farm_partner_other_amount_d",
        "ca/farm_partner_other_amount_e",
        "ca/farm_home_heat",
        "ca/farm_home_electricity",
        "ca/farm_home_insurance",
        "ca/farm_home_maintenance",
        "ca/farm_home_mortgage_interest",
        "ca/farm_home_property_taxes",
        "ca/farm_home_other_expenses",
        "ca/farm_home_personal_use_part",
        "ca/farm_home_cca",
        "ca/farm_home_carried_forward",
        "ca/farm_cca_classes",
        "ca/farm_epop_associated",
        "ca/farm_epop_agreement_filed",
        "ca/farm_epop_percentage",
        "ca/farm_epop_percentage_total",
        "ca/farm_minister_allocation_given",
        "ca/farm_minister_allocation",
        "ca/farm_fiscal_period_days_entered",
    }
)

FORM_STEPS = {
    # T2042 Area A endnote 3 "If you have a negative amount in column 7, add it to income as a
    # recapture in Part 3 on line 9600. If no property is left in the class and there is a
    # positive amount in this column, deduct the amount from income as a terminal loss in Part 4
    # on line 9790.": the recapture of each class of the Area A list (column 7 made positive when
    # negative), totalled.
    CapabilitySelection(
        name="ca/recaptured_cca",
        params={"class_rates": "ca/cca_class_rates"},
        consumes={"classes": "ca/farm_cca_classes"},
        produces={"output": "ca/farm_recaptured_cca"},
    ),
    # T2042 Part 3 line 9600 "Other income (specify):", which takes the recapture of Area A (the
    # Area A note "add it to income as a recapture in Part 3 on line 9600"): the other income the
    # caller specifies plus the recapture.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/farm_other_income", "ca/farm_recaptured_cca")},
        produces={"output": "ca/farm_other_income_with_recapture"},
    ),
    # T2042 Part 3 "Gross income: Total of the income lines (enter this amount on line 14099 of
    # your income tax and benefit return)" (line 9659): the caller's income lines of Part 3, in
    # the form's order, including the subtotal lines 9370 ("Grains and oilseeds"), 9420 ("Other
    # crops") and 9470 ("Livestock and animal products revenue"), and line 9600 with its recapture.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/farm_wheat",
                "ca/farm_oats",
                "ca/farm_barley",
                "ca/farm_mixed_grains",
                "ca/farm_corn",
                "ca/farm_canola",
                "ca/farm_flaxseed",
                "ca/farm_soybeans",
                "ca/farm_grains_and_oilseeds",
                "ca/farm_fruit",
                "ca/farm_potatoes",
                "ca/farm_vegetables",
                "ca/farm_tobacco",
                "ca/farm_greenhouse_and_nursery",
                "ca/farm_forage_crops_or_seeds",
                "ca/farm_other_crops",
                "ca/farm_cattle",
                "ca/farm_swine",
                "ca/farm_poultry",
                "ca/farm_sheep_and_lambs",
                "ca/farm_livestock_and_animal_products_revenue",
                "ca/farm_milk_and_cream",
                "ca/farm_eggs",
                "ca/farm_other_commodities",
                "ca/farm_dairy_subsidies",
                "ca/farm_crop_insurance",
                "ca/farm_other_program_payments",
                "ca/farm_rebates",
                "ca/farm_custom_work",
                "ca/farm_insurance_proceeds",
                "ca/farm_patronage_dividends",
                "ca/farm_other_income_with_recapture",
            )
        },
        produces={"output": "ca/farm_gross_income"},
    ),
    # T2042 Part 4 "Gross income (line 9659 of Part 3)" (4A): line 9659 alone, the gross income
    # that the expenses are taken from.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/farm_gross_income",)},
        produces={"output": "ca/farm_gross_income_before_expenses"},
    ),
    # T2042 Area A endnote 3 "deduct the amount from income as a terminal loss in Part 4 on line
    # 9790": the terminal loss of each class of the Area A list, totalled.
    CapabilitySelection(
        name="ca/terminal_loss",
        params={"class_rates": "ca/cca_class_rates"},
        consumes={"classes": "ca/farm_cca_classes"},
        produces={"output": "ca/farm_terminal_loss"},
    ),
    # T2042 Part 4 "Other expenses (specify):" and "Total other expenses (see column 7 of Area A on
    # page 5)" (line 9790): the other expenses the caller specifies plus the terminal loss.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/farm_other_expenses", "ca/farm_terminal_loss")},
        produces={"output": "ca/farm_other_expenses_with_terminal_loss"},
    ),
    # T2042 Charts A to C, "Motor vehicle expenses", filled in for each vehicle of the statement's
    # list and added: Chart A line 16 "Allowable motor vehicle expenses: Add amounts 13 to 15 (enter
    # this total on line 9819 of Part 4)". The printed constants ("$350***", "÷ 30", "$44,706",
    # "$1,100", "$38,000" and the 85%) and the rounding are the datasets that T2125 uses, and the
    # sales tax rate of the province is the statement's one input.
    CapabilitySelection(
        name="ca/business_vehicle_expenses",
        params={
            "interest_limits": "ca/business_vehicle_interest_limits",
            "lease_limits": "ca/business_vehicle_lease_limits",
            "days_divisor": "ca/business_vehicle_days_divisor",
            "lease_price_rate": "ca/business_vehicle_lease_price_rate",
            "rounding": "ca/business_vehicle_rounding",
        },
        consumes={
            "vehicles": "ca/business_vehicles",
            "sales_tax_rate": "ca/farm_vehicle_sales_tax_rate",
        },
        produces={"output": "ca/farm_motor_vehicle_expenses"},
    ),
    # T2042 Part 4 "Subtotal of expenses" (4B), "Expenses (enter only the business part)": the
    # expense lines 9661 to 9820, the previous year's inventory adjustments 9937 and 9938, and
    # line 9790, in the form's order.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/farm_containers_and_twine",
                "ca/farm_fertilizers_and_lime",
                "ca/farm_pesticides",
                "ca/farm_seeds_and_plants",
                "ca/farm_feed_supplements_straw_and_bedding",
                "ca/farm_livestock_purchased",
                "ca/farm_veterinary_fees",
                "ca/farm_machinery_repairs_licences_and_insurance",
                "ca/farm_gasoline_diesel_and_oil",
                "ca/farm_building_repairs_and_maintenance",
                "ca/farm_clearing_levelling_and_draining",
                "ca/farm_crop_insurance_premiums",
                "ca/farm_custom_work_expenses",
                "ca/farm_electricity",
                "ca/farm_heating_and_curing_fuel",
                "ca/farm_insurance_program_overpayment_recapture",
                "ca/farm_insurance",
                "ca/farm_interest_and_bank_charges",
                "ca/farm_office_expenses",
                "ca/farm_professional_fees",
                "ca/farm_property_taxes",
                "ca/farm_rent",
                "ca/farm_salaries_wages_and_benefits",
                "ca/farm_motor_vehicle_expenses",
                "ca/farm_small_tools",
                "ca/farm_mandatory_inventory_adjustment_previous_year",
                "ca/farm_optional_inventory_adjustment_previous_year",
                "ca/farm_other_expenses_with_terminal_loss",
            )
        },
        produces={"output": "ca/farm_expenses_subtotal"},
    ),
    # T2042 Area A, the days of the fiscal period (Guide T4002 "You were asking?": "Since your
    # fiscal period is less than 365 days, you have to prorate your CCA claim. ... base your CCA
    # claim on the number of days in your fiscal period compared to 365 days. In this case, your
    # fiscal period is 214 days."): the days the caller enters, or the 365 of a full year when none
    # are.
    CapabilitySelection(
        name="ca/fiscal_period_days",
        params={"class_rates": "ca/cca_class_rates"},
        consumes={"entered": "ca/farm_fiscal_period_days_entered"},
        produces={"output": "ca/farm_fiscal_period_days"},
    ),
    # T2042 Area A "Total CCA claim for the year: Total of column 21 (enter on line 9936 of Part 4
    # amount ii minus any personal part and any CCA for business-use-of-home expenses)" (amount ii):
    # the CCA claimed on each class of the Area A list, at most its maximum (column 19 multiplied by
    # column 20), totalled.
    CapabilitySelection(
        name="ca/cca_claim_prorated",
        params={"class_rates": "ca/cca_class_rates"},
        consumes={
            "classes": "ca/farm_cca_classes",
            "fiscal_period_days": "ca/farm_fiscal_period_days",
        },
        produces={"output": "ca/farm_cca_table_claim"},
    ),
    # T2042 Part 4 "Capital cost allowance (CCA). Enter amount ii of Area A minus any personal part
    # and any CCA for business-use-of-home expenses." (line 9936), first step: amount ii minus the
    # personal part of CCA, a caller input.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ca/farm_cca_table_claim", "less": "ca/farm_cca_personal_part"},
        produces={"output": "ca/farm_cca_claim_less_personal_part"},
    ),
    # T2042 Part 4 line 9936 (Capital cost allowance), second step: that result minus the CCA for
    # business-use-of-home expenses, amount 7K "Capital cost allowance (business part only), which
    # means amount ii of Area A minus any portion of capital cost allowance that is for personal use
    # or entered on line 9936 of Part 4", a caller input.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ca/farm_cca_claim_less_personal_part", "less": "ca/farm_home_cca"},
        produces={"output": "ca/farm_cca_claim"},
    ),
    # T2042 Part 4 "Total farm expenses: Amount 4B plus line 9936" (line 9898): the two added.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/farm_expenses_subtotal", "ca/farm_cca_claim")},
        produces={"output": "ca/farm_total_expenses"},
    ),
    # T2042 Part 4 "Net income (loss) before inventory adjustments: Amount 4A minus line 9898"
    # (line 9899): signed, a loss is negative.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/farm_gross_income_before_expenses",
            "less": "ca/farm_total_expenses",
        },
        produces={"output": "ca/farm_net_income_before_adjustments"},
    ),
    # T2042 Part 4 "Net income (loss) after inventory adjustments: Total of lines 9899, 9941, and
    # 9942" (4C), with line 9941 "Optional inventory adjustment included in the current year" and
    # line 9942 "Mandatory inventory adjustment included in the current year", both caller inputs.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/farm_net_income_before_adjustments",
                "ca/farm_optional_inventory_adjustment_current_year",
                "ca/farm_mandatory_inventory_adjustment_current_year",
            )
        },
        produces={"output": "ca/farm_net_income_after_inventory_adjustments"},
    ),
    # T2042 Part 5 "Your share of amount 4C or the amount from your T5013 slip, Statement of
    # Partnership Income" (5A): a count of 1 for a partner chooses the amount from the T5013 slip,
    # as entered; with a count of 0 it is amount 4C.
    CapabilitySelection(
        name="core/choose_by_count",
        params={},
        consumes={
            "count": "ca/farm_partner",
            "when_none": "ca/farm_net_income_after_inventory_adjustments",
            "when_any": "ca/farm_partner_share",
        },
        produces={"output": "ca/farm_share_of_net_income"},
    ),
    # T2042 Part 5 "Total: Amount 5A plus line 9951 plus line 9974" (5B): line 9951 "Return of fuel
    # charge proceeds to farmers tax credit allocated to you in the year" and line 9974 "GST/HST
    # rebate for partners received in the year", both caller inputs.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/farm_share_of_net_income",
                "ca/farm_fuel_charge_credit",
                "ca/farm_partner_gst_hst_rebate",
            )
        },
        produces={"output": "ca/farm_partnership_total"},
    ),
    # T2042 Part 6 "Total other amounts deductible from your share of the net partnership income
    # (loss): Add amounts 6A to 6E (enter this amount on line 9943 of Part 5)." (6F): 6A to 6E,
    # caller inputs.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/farm_partner_other_amount_a",
                "ca/farm_partner_other_amount_b",
                "ca/farm_partner_other_amount_c",
                "ca/farm_partner_other_amount_d",
                "ca/farm_partner_other_amount_e",
            )
        },
        produces={"output": "ca/farm_partner_other_amounts_total"},
    ),
    # T2042 Part 5 "Other amounts deductible from your share of net partnership income (loss)
    # (amount 6F)" (line 9943).
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/farm_partner_other_amounts_total",)},
        produces={"output": "ca/farm_partner_other_amounts"},
    ),
    # T2042 Part 5 "Net income (loss) after adjustments: Amount 5B minus line 9943" (5C): signed, a
    # loss is negative.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ca/farm_partnership_total", "less": "ca/farm_partner_other_amounts"},
        produces={"output": "ca/farm_net_income_after_adjustments"},
    ),
    # T2042 Part 7 "Subtotal: Add amounts 7A to 7G." (7H): 7A "Heat", 7B "Electricity", 7C
    # "Insurance", 7D "Maintenance", 7E "Mortgage interest", 7F "Property taxes" and 7G "Other
    # expenses (specify)", caller inputs.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/farm_home_heat",
                "ca/farm_home_electricity",
                "ca/farm_home_insurance",
                "ca/farm_home_maintenance",
                "ca/farm_home_mortgage_interest",
                "ca/farm_home_property_taxes",
                "ca/farm_home_other_expenses",
            )
        },
        produces={"output": "ca/farm_home_expenses_subtotal"},
    ),
    # T2042 Part 7 "Subtotal: Amount 7H minus amount 7I" (7J): amount 7I "Personal-use part of the
    # business-use-of-home expenses", a caller input.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/farm_home_expenses_subtotal",
            "less": "ca/farm_home_personal_use_part",
        },
        produces={"output": "ca/farm_home_expenses_business_part"},
    ),
    # T2042 Part 7 "Subtotal: Add amounts 7J to 7L." (7M): amount 7K and 7L "Amount carried forward
    # from previous year", a caller input.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/farm_home_expenses_business_part",
                "ca/farm_home_cca",
                "ca/farm_home_carried_forward",
            )
        },
        produces={"output": "ca/farm_home_expenses_available"},
    ),
    # T2042 Part 7 "Net income (loss) after adjustments (amount 5C) (if negative, enter "0")." (7N):
    # amount 5C, or 0 when it is negative.
    CapabilitySelection(
        name="core/sum_not_below_zero",
        params={},
        consumes={"parts": ("ca/farm_net_income_after_adjustments",)},
        produces={"output": "ca/farm_home_income_limit"},
    ),
    # T2042 Part 7 "Business-use-of-home expenses available to carry forward: Amount 7M minus amount
    # 7N (if negative, enter "0")" (7O): the claim left over, 0 when amount 7N is the larger.
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={"amount": "ca/farm_home_expenses_available", "less": "ca/farm_home_income_limit"},
        produces={"output": "ca/farm_home_carry_forward"},
    ),
    # T2042 Part 7 "Allowable claim: Amount 7M or 7N above, whichever is less (enter your share of
    # this amount on line 9945 of Part 5)" (7P).
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={"amounts": ("ca/farm_home_expenses_available", "ca/farm_home_income_limit")},
        produces={"output": "ca/farm_home_allowable_claim"},
    ),
    # T2042 Part 5 "Business-use-of-home expenses (amount 7P)" (line 9945).
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/farm_home_allowable_claim",)},
        produces={"output": "ca/farm_home_expenses"},
    ),
    # T2042 Part 5 "Your net income (loss): Amount 5C minus line 9945 (enter this amount on line
    # 14100 of your income tax and benefit return)" (line 9946): T1 "Line 25: Farming income" and
    # "Line 14100: Net" are the same artifact, signed: a loss is negative.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/farm_net_income_after_adjustments",
            "less": "ca/farm_home_expenses",
        },
        produces={"output": "ca/farming_income"},
    ),
    # T2042 Area A column 22 "UCC at the end of the year (col. 7 minus col. 21)": the class number
    # and column 22 of each class of the Area A list, a product of the return for next year's
    # column 1.
    CapabilitySelection(
        name="ca/closing_ucc_prorated",
        params={"class_rates": "ca/cca_class_rates"},
        consumes={
            "classes": "ca/farm_cca_classes",
            "fiscal_period_days": "ca/farm_fiscal_period_days",
        },
        produces={"output": "ca/farm_closing_ucc"},
    ),
    # T2042 Area A endnote 5 "the immediate expensing limit, which is equal to one of the
    # following, whichever is applicable: $1.5 million, if you are not associated with any other
    # eligible person or partnership (EPOP) in the tax year" and Area G "Immediate expensing limit
    # allocated to your business: Multiply $1.5 million by the percentage assigned to your
    # business in column 3**" (amount iv): the printed $1.5 million, a dataset.
    CapabilitySelection(
        name="core/credit_amount",
        params={"amount": "ca/farm_immediate_expensing_cap"},
        consumes={},
        produces={"output": "ca/farm_immediate_expensing_cap"},
    ),
    # T2042 Area G "The total of all percentages assigned under the agreement should not be more
    # than 100%. If the total is more than 100%, then the associated group has an immediate
    # expensing limit of zero." and "** If the total of column 3 is more than 100%, enter "0."":
    # the printed 100%, a dataset, as the form prints a percentage (100 for 100%).
    CapabilitySelection(
        name="core/credit_amount",
        params={"amount": "ca/farm_epop_percentage_maximum"},
        consumes={},
        produces={"output": "ca/farm_epop_percentage_maximum"},
    ),
    # T2042 Area G "Immediate expensing limit allocated to your business: Multiply $1.5 million by
    # the percentage assigned to your business in column 3**" (amount iv), first step: $1.5
    # million times the percentage assigned to your business in column 3, a caller input as the
    # form prints it (40 for 40%).
    CapabilitySelection(
        name="ca/apply_percentage",
        params={"rounding": "ca/farm_immediate_expensing_rounding"},
        consumes={
            "amount": "ca/farm_immediate_expensing_cap",
            "percentage": "ca/farm_epop_percentage",
        },
        produces={"output": "ca/farm_immediate_expensing_share"},
    ),
    # T2042 Area G "** If the total of column 3 is more than 100%, enter "0."", first step: 100%
    # less "Total of percentage assigned: Total of column 3", a caller input; negative when the
    # total is more than 100%.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/farm_epop_percentage_maximum",
            "less": "ca/farm_epop_percentage_total",
        },
        produces={"output": "ca/farm_epop_percentage_room"},
    ),
    # T2042 Area G "Immediate expensing limit allocated to your business: Multiply $1.5 million by
    # the percentage assigned to your business in column 3**" (amount iv) and "** If the total of
    # column 3 is more than 100%, enter "0."": the multiple above when 100% less the total of
    # column 3 is zero or positive, else 0.
    CapabilitySelection(
        name="ca/choose_by_sign",
        params={},
        consumes={
            "sign": "ca/farm_epop_percentage_room",
            "when_positive": (),
            "when_zero": (),
            "when_negative": (),
            "when_non_positive": (),
            "when_non_negative": ("ca/farm_immediate_expensing_share",),
        },
        produces={"output": "ca/farm_immediate_expensing_allocated"},
    ),
    # T2042 Area A endnote 5 "amount iv of Area G, if you are associated with one or more EPOPs
    # in the tax year" and "zero, if you are associated with one or more EPOPs and an agreement
    # that assigns a percentage to one or more of the associated EPOPs was not filed with the
    # minister in a prescribed form": amount iv times the count of agreements filed (a caller's 0
    # or 1), so 0 when none was filed.
    CapabilitySelection(
        name="core/times_count",
        params={},
        consumes={
            "amount": "ca/farm_immediate_expensing_allocated",
            "count": "ca/farm_epop_agreement_filed",
        },
        produces={"output": "ca/farm_immediate_expensing_associated_limit"},
    ),
    # T2042 Area A endnote 5 "the immediate expensing limit, which is equal to one of the
    # following, whichever is applicable": a count of 1 for associated with one or more EPOPs (a
    # caller's 0 or 1) chooses the limit above ("amount iv of Area G" or "zero"); with a count of
    # 0 it is the $1.5 million ("if you are not associated with any other eligible person or
    # partnership (EPOP) in the tax year").
    CapabilitySelection(
        name="core/choose_by_count",
        params={},
        consumes={
            "count": "ca/farm_epop_associated",
            "when_none": "ca/farm_immediate_expensing_cap",
            "when_any": "ca/farm_immediate_expensing_associated_limit",
        },
        produces={"output": "ca/farm_immediate_expensing_limit_before_minister"},
    ),
    # T2042 Area A endnote 5 "any amount allocated by the minister under subsection 1104(3.4) of
    # the Regulations": a count of 1 (a caller's 0 or 1) chooses the amount allocated by the
    # minister, as entered, in place of the limit above; with a count of 0 the limit above stands.
    CapabilitySelection(
        name="core/choose_by_count",
        params={},
        consumes={
            "count": "ca/farm_minister_allocation_given",
            "when_none": "ca/farm_immediate_expensing_limit_before_minister",
            "when_any": "ca/farm_minister_allocation",
        },
        produces={"output": "ca/farm_immediate_expensing_limit"},
    ),
    # T2042 Area A endnote 5 "the amount of income, if any, earned from the source of income that
    # is a business (before any CCA deductions) in which the relevant DIEP is used for the tax
    # year": amount 4C "Net income (loss) after inventory adjustments" (the farm's final net
    # income; the form names no line for this) plus line 9936, the CCA it deducted (the recapture
    # on line 9600 is already in gross income and the terminal loss on line 9790 an expense), not
    # below zero.
    CapabilitySelection(
        name="core/sum_not_below_zero",
        params={},
        consumes={
            "parts": (
                "ca/farm_net_income_after_inventory_adjustments",
                "ca/farm_cca_claim",
            ),
        },
        produces={"output": "ca/farm_income_before_cca"},
    ),
    # T2042 Area A "Total immediate expensing claim for the year: Total of column 9" (line i) and
    # endnote 5 "The total immediate expensing amount for the tax year (total of column 9) is
    # limited to the lesser of: the immediate expensing limit"; "the UCC of DIEPs in column 8";
    # "the amount of income, if any, earned from the source of income that is a business (before
    # any CCA deductions) in which the relevant DIEP is used for the tax year": the total of
    # column 9 of the Area A list, refused when above the limit or above the income before CCA.
    CapabilitySelection(
        name="ca/immediate_expensing_claim",
        params={"class_rates": "ca/cca_class_rates"},
        consumes={
            "classes": "ca/farm_cca_classes",
            "immediate_expensing_limit": "ca/farm_immediate_expensing_limit",
            "income_before_cca": "ca/farm_income_before_cca",
        },
        produces={"output": "ca/farm_immediate_expensing_claim"},
    ),
}

INPUTS = frozenset({"ca/t2042_statements"})

FORM_EXPORTS = (
    "ca/farming_income",
    "ca/farm_closing_ucc",
    "ca/farm_home_carry_forward",
    "ca/farm_immediate_expensing_claim",
)

# The form exports Area A column 22 "UCC at the end of the year" (for next year), Part 7 line 7O
# "Business-use-of-home expenses available to carry forward" and Area A line i "Total immediate
# expensing claim for the year", which no line of the return reads: an export nobody reads is
# fine, so the return declares no output for them.
OUTPUTS: frozenset[str] = frozenset()

# T1 line 14100 "Net": the total of T2042 line 9946 over the statements.
STEPS = {
    CapabilitySelection(
        name="core/record_total",
        params={},
        consumes={"records": "ca/t2042.farming_income"},
        produces={"output": "ca/farming_income"},
    ),
}

FORM_WIRING = {
    (RecapturedCca, frozenset({FARM_CCA_CLASSES}), frozenset({FARM_RECAPTURED_CCA})),
    (
        Sum,
        frozenset({FARM_OTHER_INCOME, FARM_RECAPTURED_CCA}),
        frozenset({FARM_OTHER_INCOME_WITH_RECAPTURE}),
    ),
    (
        Sum,
        frozenset(
            {
                FARM_BARLEY,
                FARM_CANOLA,
                FARM_CATTLE,
                FARM_CORN,
                FARM_CROP_INSURANCE,
                FARM_CUSTOM_WORK,
                FARM_DAIRY_SUBSIDIES,
                FARM_EGGS,
                FARM_FLAXSEED,
                FARM_FORAGE_CROPS_OR_SEEDS,
                FARM_FRUIT,
                FARM_GRAINS_AND_OILSEEDS,
                FARM_GREENHOUSE_AND_NURSERY,
                FARM_INSURANCE_PROCEEDS,
                FARM_LIVESTOCK_AND_ANIMAL_PRODUCTS_REVENUE,
                FARM_MILK_AND_CREAM,
                FARM_MIXED_GRAINS,
                FARM_OATS,
                FARM_OTHER_COMMODITIES,
                FARM_OTHER_CROPS,
                FARM_OTHER_INCOME_WITH_RECAPTURE,
                FARM_OTHER_PROGRAM_PAYMENTS,
                FARM_PATRONAGE_DIVIDENDS,
                FARM_POTATOES,
                FARM_POULTRY,
                FARM_REBATES,
                FARM_SHEEP_AND_LAMBS,
                FARM_SOYBEANS,
                FARM_SWINE,
                FARM_TOBACCO,
                FARM_VEGETABLES,
                FARM_WHEAT,
            }
        ),
        frozenset({FARM_GROSS_INCOME}),
    ),
    (Sum, frozenset({FARM_GROSS_INCOME}), frozenset({FARM_GROSS_INCOME_BEFORE_EXPENSES})),
    (TerminalLoss, frozenset({FARM_CCA_CLASSES}), frozenset({FARM_TERMINAL_LOSS})),
    (
        Sum,
        frozenset({FARM_OTHER_EXPENSES, FARM_TERMINAL_LOSS}),
        frozenset({FARM_OTHER_EXPENSES_WITH_TERMINAL_LOSS}),
    ),
    (
        Sum,
        frozenset(
            {
                FARM_BUILDING_REPAIRS_AND_MAINTENANCE,
                FARM_CLEARING_LEVELLING_AND_DRAINING,
                FARM_CONTAINERS_AND_TWINE,
                FARM_CROP_INSURANCE_PREMIUMS,
                FARM_CUSTOM_WORK_EXPENSES,
                FARM_ELECTRICITY,
                FARM_FEED_SUPPLEMENTS_STRAW_AND_BEDDING,
                FARM_FERTILIZERS_AND_LIME,
                FARM_GASOLINE_DIESEL_AND_OIL,
                FARM_HEATING_AND_CURING_FUEL,
                FARM_INSURANCE,
                FARM_INSURANCE_PROGRAM_OVERPAYMENT_RECAPTURE,
                FARM_INTEREST_AND_BANK_CHARGES,
                FARM_LIVESTOCK_PURCHASED,
                FARM_MACHINERY_REPAIRS_LICENCES_AND_INSURANCE,
                FARM_MANDATORY_INVENTORY_ADJUSTMENT_PREVIOUS_YEAR,
                FARM_MOTOR_VEHICLE_EXPENSES,
                FARM_OFFICE_EXPENSES,
                FARM_OPTIONAL_INVENTORY_ADJUSTMENT_PREVIOUS_YEAR,
                FARM_OTHER_EXPENSES_WITH_TERMINAL_LOSS,
                FARM_PESTICIDES,
                FARM_PROFESSIONAL_FEES,
                FARM_PROPERTY_TAXES,
                FARM_RENT,
                FARM_SALARIES_WAGES_AND_BENEFITS,
                FARM_SEEDS_AND_PLANTS,
                FARM_SMALL_TOOLS,
                FARM_VETERINARY_FEES,
            }
        ),
        frozenset({FARM_EXPENSES_SUBTOTAL}),
    ),
    (
        FiscalPeriodDays,
        frozenset({FARM_FISCAL_PERIOD_DAYS_ENTERED}),
        frozenset({FARM_FISCAL_PERIOD_DAYS}),
    ),
    (
        CcaClaimProrated,
        frozenset({FARM_CCA_CLASSES, FARM_FISCAL_PERIOD_DAYS}),
        frozenset({FARM_CCA_TABLE_CLAIM}),
    ),
    (
        Subtract,
        frozenset({FARM_CCA_PERSONAL_PART, FARM_CCA_TABLE_CLAIM}),
        frozenset({FARM_CCA_CLAIM_LESS_PERSONAL_PART}),
    ),
    (
        Subtract,
        frozenset({FARM_CCA_CLAIM_LESS_PERSONAL_PART, FARM_HOME_CCA}),
        frozenset({FARM_CCA_CLAIM}),
    ),
    (Sum, frozenset({FARM_CCA_CLAIM, FARM_EXPENSES_SUBTOTAL}), frozenset({FARM_TOTAL_EXPENSES})),
    (
        Subtract,
        frozenset({FARM_GROSS_INCOME_BEFORE_EXPENSES, FARM_TOTAL_EXPENSES}),
        frozenset({FARM_NET_INCOME_BEFORE_ADJUSTMENTS}),
    ),
    (
        Sum,
        frozenset(
            {
                FARM_MANDATORY_INVENTORY_ADJUSTMENT_CURRENT_YEAR,
                FARM_NET_INCOME_BEFORE_ADJUSTMENTS,
                FARM_OPTIONAL_INVENTORY_ADJUSTMENT_CURRENT_YEAR,
            }
        ),
        frozenset({FARM_NET_INCOME_AFTER_INVENTORY_ADJUSTMENTS}),
    ),
    (
        ChooseByCount,
        frozenset({FARM_NET_INCOME_AFTER_INVENTORY_ADJUSTMENTS, FARM_PARTNER, FARM_PARTNER_SHARE}),
        frozenset({FARM_SHARE_OF_NET_INCOME}),
    ),
    (
        Sum,
        frozenset({FARM_FUEL_CHARGE_CREDIT, FARM_PARTNER_GST_HST_REBATE, FARM_SHARE_OF_NET_INCOME}),
        frozenset({FARM_PARTNERSHIP_TOTAL}),
    ),
    (
        Sum,
        frozenset(
            {
                FARM_PARTNER_OTHER_AMOUNT_A,
                FARM_PARTNER_OTHER_AMOUNT_B,
                FARM_PARTNER_OTHER_AMOUNT_C,
                FARM_PARTNER_OTHER_AMOUNT_D,
                FARM_PARTNER_OTHER_AMOUNT_E,
            }
        ),
        frozenset({FARM_PARTNER_OTHER_AMOUNTS_TOTAL}),
    ),
    (Sum, frozenset({FARM_PARTNER_OTHER_AMOUNTS_TOTAL}), frozenset({FARM_PARTNER_OTHER_AMOUNTS})),
    (
        Subtract,
        frozenset({FARM_PARTNERSHIP_TOTAL, FARM_PARTNER_OTHER_AMOUNTS}),
        frozenset({FARM_NET_INCOME_AFTER_ADJUSTMENTS}),
    ),
    (
        Sum,
        frozenset(
            {
                FARM_HOME_ELECTRICITY,
                FARM_HOME_HEAT,
                FARM_HOME_INSURANCE,
                FARM_HOME_MAINTENANCE,
                FARM_HOME_MORTGAGE_INTEREST,
                FARM_HOME_OTHER_EXPENSES,
                FARM_HOME_PROPERTY_TAXES,
            }
        ),
        frozenset({FARM_HOME_EXPENSES_SUBTOTAL}),
    ),
    (
        Subtract,
        frozenset({FARM_HOME_EXPENSES_SUBTOTAL, FARM_HOME_PERSONAL_USE_PART}),
        frozenset({FARM_HOME_EXPENSES_BUSINESS_PART}),
    ),
    (
        Sum,
        frozenset({FARM_HOME_CARRIED_FORWARD, FARM_HOME_CCA, FARM_HOME_EXPENSES_BUSINESS_PART}),
        frozenset({FARM_HOME_EXPENSES_AVAILABLE}),
    ),
    (
        SumNotBelowZero,
        frozenset({FARM_NET_INCOME_AFTER_ADJUSTMENTS}),
        frozenset({FARM_HOME_INCOME_LIMIT}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({FARM_HOME_EXPENSES_AVAILABLE, FARM_HOME_INCOME_LIMIT}),
        frozenset({FARM_HOME_CARRY_FORWARD}),
    ),
    (
        LesserOf,
        frozenset({FARM_HOME_EXPENSES_AVAILABLE, FARM_HOME_INCOME_LIMIT}),
        frozenset({FARM_HOME_ALLOWABLE_CLAIM}),
    ),
    (Sum, frozenset({FARM_HOME_ALLOWABLE_CLAIM}), frozenset({FARM_HOME_EXPENSES})),
    (
        Subtract,
        frozenset({FARM_HOME_EXPENSES, FARM_NET_INCOME_AFTER_ADJUSTMENTS}),
        frozenset({FARMING_INCOME}),
    ),
    (
        ClosingUccProrated,
        frozenset({FARM_CCA_CLASSES, FARM_FISCAL_PERIOD_DAYS}),
        frozenset({FARM_CLOSING_UCC}),
    ),
    (CreditAmount, frozenset(), frozenset({FARM_IMMEDIATE_EXPENSING_CAP})),
    (CreditAmount, frozenset(), frozenset({FARM_EPOP_PERCENTAGE_MAXIMUM})),
    (
        ApplyPercentage,
        frozenset({FARM_IMMEDIATE_EXPENSING_CAP, FARM_EPOP_PERCENTAGE}),
        frozenset({FARM_IMMEDIATE_EXPENSING_SHARE}),
    ),
    (
        Subtract,
        frozenset({FARM_EPOP_PERCENTAGE_MAXIMUM, FARM_EPOP_PERCENTAGE_TOTAL}),
        frozenset({FARM_EPOP_PERCENTAGE_ROOM}),
    ),
    (
        ChooseBySign,
        frozenset({FARM_EPOP_PERCENTAGE_ROOM, FARM_IMMEDIATE_EXPENSING_SHARE}),
        frozenset({FARM_IMMEDIATE_EXPENSING_ALLOCATED}),
    ),
    (
        TimesCount,
        frozenset({FARM_IMMEDIATE_EXPENSING_ALLOCATED, FARM_EPOP_AGREEMENT_FILED}),
        frozenset({FARM_IMMEDIATE_EXPENSING_ASSOCIATED_LIMIT}),
    ),
    (
        ChooseByCount,
        frozenset(
            {
                FARM_EPOP_ASSOCIATED,
                FARM_IMMEDIATE_EXPENSING_CAP,
                FARM_IMMEDIATE_EXPENSING_ASSOCIATED_LIMIT,
            }
        ),
        frozenset({FARM_IMMEDIATE_EXPENSING_LIMIT_BEFORE_MINISTER}),
    ),
    (
        ChooseByCount,
        frozenset(
            {
                FARM_MINISTER_ALLOCATION_GIVEN,
                FARM_IMMEDIATE_EXPENSING_LIMIT_BEFORE_MINISTER,
                FARM_MINISTER_ALLOCATION,
            }
        ),
        frozenset({FARM_IMMEDIATE_EXPENSING_LIMIT}),
    ),
    (
        SumNotBelowZero,
        frozenset({FARM_NET_INCOME_AFTER_INVENTORY_ADJUSTMENTS, FARM_CCA_CLAIM}),
        frozenset({FARM_INCOME_BEFORE_CCA}),
    ),
    (
        ImmediateExpensingClaim,
        frozenset({FARM_CCA_CLASSES, FARM_IMMEDIATE_EXPENSING_LIMIT, FARM_INCOME_BEFORE_CCA}),
        frozenset({FARM_IMMEDIATE_EXPENSING_CLAIM}),
    ),
    (
        BusinessVehicleExpenses,
        frozenset({BUSINESS_VEHICLES, FARM_VEHICLE_SALES_TAX_RATE}),
        frozenset({FARM_MOTOR_VEHICLE_EXPENSES}),
    ),
}

WIRING = {
    (RecordTotal, frozenset({NET_INCOME_PER_STATEMENT}), frozenset({FARMING_INCOME})),
}
